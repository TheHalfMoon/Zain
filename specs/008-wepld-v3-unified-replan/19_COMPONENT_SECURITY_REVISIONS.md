# 19 — Component Security Revisions: Browser egress, Review confidentiality, fs-gate

```text
STATUS = PROPOSED (planning only)
ADDRESSES = Astro H-3/H-7/H-8 and round-2 A2-08 (read boundary), A2-11 (browser), A2-12 (fs-gate semantics)
SUPERSEDES = R17 §8.6 "All" row DNS sentence and the claim that navigation gating confines origins; R14 §5.2 paragraph
             "acceptable because it has no write tools"; R18 §3.1 "realpath-checked" fs ops and DG-N03 wording
TESTS = 23 §8 (BRW-AT-25..29), §5 (ZCR-T26..T29, ZCR-Q*), §9 (DG-N03, DG-N15, FSG-01..04)
```

## 1. Browser: connection-level egress (H-3)

**Finding accepted:** R17 §8.6 intercepts document navigations only (Electron main/subframe document requests, CDP
`resourceType: Document`). fetch/XHR, WebSocket, beacons, images/scripts, workers and service workers were not covered,
and DNS validation was deferred to the P8 egress proxy while Y-03 promised it in P5.

**Design (Y-10, P5):**

1. Agent and Test partitions get `session.setProxy({ proxyRules: "http=127.0.0.1:<p>;https=127.0.0.1:<p>",
   proxyBypassRules: "<-loopback>" })` — `<-loopback>` removes Chromium's implicit loopback bypass, so loopback traffic
   also passes the proxy. All network requests of the partition (documents, subresources, fetch/XHR, WebSocket via
   CONNECT, dedicated/shared/service workers, beacons, prefetch) use the session's network context.
2. The proxy (in the Server, owned by BrowserController) receives the hostname (CONNECT host:port or absolute URI),
   resolves it **itself**, validates the resulting IP against policy (deny loopback, link-local, RFC1918, ULA, `.local`
   unless the origin is a granted project dev origin bound to a ProcessHost-owned port), and **connects to the validated
   IP** — no re-resolution, so DNS rebinding cannot redirect the connection (BRW-AT-27).
3. Plain-HTTP redirects are validated per hop inside the proxy; HTTPS redirects are seen by Chromium as new requests and
   pass the proxy again (BRW-AT-28).
4. WebRTC: `webContents.setWebRTCIPHandlingPolicy("disable_non_proxied_udp")` + media permissions denied (BRW-AT-29).
   QUIC is not used through HTTP proxies (verify in FG-05).
5. The navigation gate (Y-03) remains as the approval/UX layer for document hops; it is not the security boundary.
6. Main-process `net`/`fetch` is never used on behalf of page content.

**Residual risks (stated):** domain fronting to hosts sharing an allowed CDN (proxy sees CONNECT host/SNI, not the inner
Host header); DNS lookups by Chromium's prefetcher may leak hostnames (information only, no connection); extensions are
not loaded in agent partitions.

**Additional R2 policies (A2-11):** CONNECT authorizes host:port, not encrypted paths, so the allowlist is per origin and
per tunnel; HTTP/2 connection coalescing across hosts is disabled for agent partitions (per-host tunnels or HTTP/2 off;
BRW-AT-30); tunnels are torn down on grant revocation (BRW-AT-31); the headless Playwright backend is launched with the same
proxy and bypass rules and runs the same suite (BRW-AT-32); proxy failure fails closed (BRW-AT-33); hostile localhost
content is tested across all request types including redirects to external and to Core/Server/debug ports (BRW-AT-34);
loopback ports are allowed only when owned by ProcessHost project processes (BRW-AT-35).

**Claims by stage (revised):**

| Stage | Agent browser tools | Claim |
|---|---|---|
| R0a/R0b/R0 | inherited T3 behaviour, disclosed; cookie-store import removed in R0b (Y-00) | no browser security claim |
| R1 | **disabled for agents** (inherited `preview_*` MCP tools refused, BRW-P01); manual preview by the user is outside every claim | "agents cannot drive the browser" |
| R2 after BRW-AT-25..35 pass on both backends | allow-listed origins via the proxy | "connection-level egress enforced for agent/test partitions; residuals: domain fronting, DNS prefetch" |
| R2 if FG-05 or BRW-AT-25..35 fail | remain disabled for agents | unchanged from R1 |
| R5 (P8) | OS-level egress proxy | widened per S-04 |

## 2. Review confidentiality: snapshot + enforceable read boundary (H-7; revised for A2-08)

A snapshot directory plus `cwd` is not a read boundary: absolute paths, shell/grep tools, ambient configuration and
history, and provider-internal reads can reach other files. The boundary is defined per reviewer route:

| Route | Read boundary | R1 status |
|---|---|---|
| Delegated reviewer = Claude Agent SDK session | **all built-in tools disabled**; the only tools are Zain read-broker MCP tools that serve files from the manifest (by manifest path, never by filesystem path); `HOME`, `CLAUDE_CONFIG_DIR`, history and `settingSources` scrubbed to an empty per-run directory; cwd = empty directory; PreToolUse denies any non-broker tool as a second layer | **qualified for R1** after ZCR-T29..T33 |
| Delegated reviewer = Codex | built-in reads cannot be fully disabled (known-safe reads auto-run) | **not qualified** as a confidential reviewer route in R1; usable only on projects explicitly marked non-confidential |
| Delegated reviewer = ACP agent | agent-internal reads not observable | **not qualified** in R1 |
| Engine mode (OCR, R3) | snapshot root + Z-P7 manifest check on every tool | R3, after K-10/K-11 |

Snapshot rules: materialized from git objects at `headOid` (untracked files excluded by construction); git symlink entries
are materialized as text and never followed (ZCR-T32); secret screen with approval for hits; manifest digest in the
`REVIEW_RUN` input digest; per-run disclosure budget.

**Model egress in R1:** reviewer sessions send model traffic through the Zain loopback **review proxy** (endpoint
allowlist, request log with digests for the confidentiality assertion, per-run approval for cloud endpoints). A cloud review
route without the proxy is refused (ZCR-T33). The general mediated model proxy for all providers remains K-09 (R3).

**Claim:** R1 review is advisory and never completion or acceptance authority; its quality is not qualified until
ZCR-Q01..Q03 (R2). Sensitive reviews are allowed only on qualified routes.

## 3. fs-gate: object-authority file operations (H-8; revised for A2-12)

**Authority model:** the granted root is held as a directory handle; authority is over **objects reached beneath that
handle**, not over path strings.

| Concern | Rule (Windows, R1) | Linux/macOS (R3 parity) |
|---|---|---|
| Path walk | each component opened relative to the parent handle with `FILE_OPEN_REPARSE_POINT`; any reparse point rejected; `GetFinalPathNameByHandle` compared with the normalized request | `openat2(RESOLVE_BENEATH, RESOLVE_NO_SYMLINKS, RESOLVE_NO_MAGICLINKS)` / `O_NOFOLLOW` walk |
| Names | reject ADS (`:`), device names (CON, NUL, AUX, COM*, LPT*), trailing dots/spaces, 8.3 aliases (final long name must equal request), directories with per-directory case sensitivity enabled | NFC normalization; reject `..` |
| Hardlinks | writes always by **fresh-file atomic replacement** (new temp object in the target directory, then `FileRenameInfoEx` replace by handle), so a hardlinked alias outside the root is never written through; in-place operations and confidential reads reject targets with link count > 1 (FSG-05) | same via `st_nlink` |
| Ancestor relocation | every ancestor directory from root to target held open **without `FILE_SHARE_DELETE`** for the duration, so it cannot be renamed or deleted mid-operation (FSG-06) | not preventable without namespaces: detect after the operation (re-resolve beneath root, compare dev/ino); mismatch → violation + UNKNOWN |
| Final target | object id checked again immediately before replace; mismatch aborts (FSG-08) | dev/ino check |
| Truncation | never open with truncate; validation completes before any write (FSG-09) | same |
| Volumes | cross-volume and mount-point paths rejected | same |
| Share modes | target opened without `FILE_SHARE_WRITE` / `FILE_SHARE_DELETE` during replace | advisory only |
| Reads | object-authority walk as above; reads of hardlinked files rejected in confidential contexts | same |

Feasibility on Windows is part of C-00 FG-04 (must cover the FSG-05..09 fixtures, not only junction swaps). If FG-04 fails,
R1 claims no write confinement for the failed cases and the affected operations require approval with an explicit
"not confined" label.
