# 19 — Component Security Revisions: Browser egress, Review confidentiality, fs-gate

```text
STATUS = PROPOSED (planning only)
ADDRESSES = Astro H-3 (browser egress), H-7 (OCR egress), H-8 (DeskGate filesystem races)
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

**Claims by stage:**

| Stage | Agent lane origins | Claim |
|---|---|---|
| R0 (P2) | none (Preview lane only; cookie import removed) | no agent browsing claim |
| R1 (P3) | inherited preview_* tools gated by S6; loopback project origins only | "agent browser actions require grants; external origins not available" |
| R2 (P5) before Y-10 suite green | loopback project origins only | same as R1 |
| R2 after BRW-AT-25..29 green | allow-listed external origins | "connection-level egress enforced for agent/test partitions; residuals: domain fronting, DNS prefetch leaks" |
| R5 (P8) | OS-level egress proxy for all provider processes | widened per S-04 |

FG-05 (P1) checks the request-type coverage of the session proxy before this design is committed; NO-GO keeps the
Agent lane loopback-only through R2 and the claim text says so.

## 2. Review confidentiality: snapshot + allowlist + mediated egress (H-7)

**Finding accepted:** OCR's FileReader confines reads to the repository root (alibaba/open-code-review@375f64cd
`internal/tool/filereader.go` L94–115, L193–204), which is broader than the approved review payload; untracked files and
local secrets inside the repo were readable by tool calls, and "no write tools" protects integrity, not confidentiality.

**Design:**

1. **Review snapshot (K-04):** the Server materializes an immutable directory `<run>/snapshot/` containing only the
   files in the approved review manifest at `headOid` (changed files + rule-selected support files), written from git
   objects (never from the working tree, so untracked files are excluded by construction). A secret screen runs on the
   snapshot; hits are excluded or require explicit approval with the excerpt shown. The manifest digest is part of the
   `REVIEW_RUN` input digest.
2. **Every reader confined to the manifest:** delegated mode (K-08) — reviewer session `cwd` = snapshot, PreToolUse
   denies reads whose canonical path is not in the manifest (ZCR-T29). Engine mode (K-10) — repo root = snapshot, plus
   patch Z-P7 makes FileReader/grep/list check the manifest, not only the root (ZCR-T26).
3. **Disclosure budget:** tool results are counted against a per-run byte budget recorded in the ledger; exceeding it
   stops the run (`PARTIAL`).
4. **Egress:** local model routes are the default and the qualification path (K-10, K-11). A cloud review route is
   selectable only through the mediated model proxy (K-09: endpoint allowlist, per-run token budget, payload digests,
   per-run approval). The earlier statement "acceptable because it has no write tools" is withdrawn.
5. **Delegated mode default:** R1/R2 ship delegated review (one findings schema). The OCR engine lane is preserved
   (K-02, K-03, K-10, K-11, K-09) in R3 and productized only if ZCR-Q04 shows it beats delegated mode.

## 3. fs-gate: handle-based file operations (H-8)

**Finding accepted:** re-running `realpath` at dispatch still leaves a window between the check and the filesystem call.

**Design (H-08, native helper used by the Server EffectWorker; the single write path for ACP fs, DeskGate, Plan Mode,
review fixes and design patches):**

| Platform | Mechanism |
|---|---|
| Windows | Hold a handle to the granted root directory. Walk each path component with `NtCreateFile` using `RootDirectory` = parent handle and `FILE_OPEN_REPARSE_POINT`; reject any component whose attributes include `FILE_ATTRIBUTE_REPARSE_POINT`; reject ADS (`:`) and 8.3/short names by comparing `GetFinalPathNameByHandle` with the normalized request; write through the final handle; create via `FILE_CREATE` relative to the parent handle; atomic replace/move via `SetFileInformationByHandle(FileRenameInfoEx)` with `RootDirectory` = destination parent handle. |
| Linux | `openat2(dirfd, path, RESOLVE_BENEATH | RESOLVE_NO_SYMLINKS | RESOLVE_NO_MAGICLINKS)`; `renameat2` relative to held dir fds. |
| macOS | component-wise `openat(..., O_NOFOLLOW)` walk from the held root fd (`O_NOFOLLOW_ANY` where available); `renameatx_np` relative to fds. |

Properties: the object written is the object validated (no re-resolution between check and use); parents are held
handles during create/move. Tests at the actual boundary: FSG-01..04 and DG-N03/DG-N15 run an attacker thread that swaps
links/junctions continuously during 10,000 operations and assert zero effects outside the target; the mutant replaces
handle operations with path-based calls and must fail. Feasibility on Windows is checked by C-00 FG-04.
