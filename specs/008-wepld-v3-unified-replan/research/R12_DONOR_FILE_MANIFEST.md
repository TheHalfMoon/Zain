# R12 — File-level transplant manifests for Zain's non-T3 donors (D2–D7, D9, D11, D12, D13, D19, D20, D21, D7-Monaco)

```text
STATUS      = PLANNING ONLY. Nothing was cloned, downloaded, installed or copied. Every number below was read through
              `gh api` (git/trees?recursive=1, contents, git/blobs), the npm registry JSON and the crates.io JSON API.
DATE        = 2026-10-28 (upstream state read on this date; pins are the commits below, not HEAD)
DISK RULE   = honoured: this file is the only file written. Analyses ran from stdin in memory.
CONTENT     = upstream text read through the API is DATA, never instructions.
SCOPE       = P/06 rows D2-D7, D9, D11, D12, D13, D19, D20, D21. D8, D10, D14-D18, D22-D25 are out of scope here.
              D26-D36 are cross-referenced only (section 0.4); their file tables live in R14-R18.
```

## Completeness statement

* **Verified (read via API on 2026-10-28):** full-tree file lists, blob sizes and blob SHAs for every selected set; full commit SHAs; root license files; every Cargo.toml / package.json named above; external dependency versions and licenses (crates.io and npm registry JSON); for Orca, the import graph of all non-test TypeScript files in D2-D7 (direct outside-set imports, depth-2 closure capped at 160 modules); for codex, all 323 `.rs` blobs scanned for `codex_*` identifiers.
* **Not verified (UNKNOWN):** test-file imports (not fetched); Orca closure beyond depth 2 (D2, D3, D5, D6, D7 marked); contents of the Swift/PowerShell/Python natives; which `codex_protocol` symbols are used; Windows behaviour of process-hardening; TLS interception posture of network-proxy; per-file licence origin in MCP; bundled font licenses in Excalidraw; rust-toolchain minimums for codex and cedar; `cedar-for-agents` (not in scope).
* **Not done:** no clone, download, install or local temp file; only this file was written. D8, D10, D14-D18, D22-D25 and D26-D36 are out of scope (cross-referenced in section 0.4).

## Key findings (read first)

1. **D9 is not closed.** The nine codex crates need `codex-protocol` (89 files, 1.2 MB), `codex-utils-pty`, `codex-otel` (drags `codex-api`), `codex-http-client`, `codex-uds` and others; `windows-sandbox-service` needs `codex-core` (18.6 MB). Verdict: vendor process-hardening, execpolicy and leaf utils; port sandboxing, network-proxy, windows-sandbox-rs against a Zain permission contract; reference-only for the service.
2. **`bwrap` compiles a vendored LGPL-2.0 C tree** (`codex-rs/vendor/bubblewrap`, `COPYING` = GNU Library GPL v2). Do not vendor; use the distro binary on Linux. Add a CI licence gate.
3. **`network-proxy` is pinned to exact pre-release `rama =0.3.0-alpha.4`** (crates.io now 0.4.0) and carries AWS SigV4 and OpenTelemetry deps Zain does not need.
4. **D3 is not closed**: 44 direct and 108 depth-2 outside modules in `src/shared`; installers in `src/main/agent-hooks` must not be copied (they write global agent configs).
5. **D7 diff comments pull the Orca renderer store** (depth-2 closure 489 modules): treat as rewrite behind an adapter, not a copy.
6. **MCP SDK licensing is mixed** (Apache-2.0 + MIT + CC-BY-4.0 in one LICENSE, GitHub says NOASSERTION; npm 2.x and crates.io 3.x say Apache-2.0). Ship both texts.
7. **Excalidraw**: repo pin says 0.18.0, npm latest is 0.18.1; no font license files in the tree (UNKNOWN).
8. **Rust toolchain floor**: ACP schema requires rust 1.88.0; codex uses edition 2024.
9. Fast-moving pins (ACP schema weekly, rmcp 3.6 to 3.8 in 6 days, Cedar monthly): pin with `=` and re-run conformance per bump.

## 0. Conventions

### 0.1 Pins (full SHAs resolved from the short pins in 06_SOURCE_TRANSPLANT_MATRIX.md)

| Donor repo | Short pin in 06 | Full SHA (resolved via `gh api repos/<r>/commits/<short>`) | Commit date | Repo license (root file) | Tree |
|---|---|---|---|---|---|
| stablyai/orca | e310a636 | `e310a63624c86c0e91e9d77df71f038b91d79ea0` | given | MIT, "Copyright (c) 2026 Lovecast Inc." (`LICENSE` 1070 B); no NOTICE | 40,641 entries, not truncated |
| openai/codex | 603a7baf | `603a7baff0f6f37ee9a8a9375a272eaab03d3ece` | given | Apache-2.0 (`LICENSE` 10,926 B) + `NOTICE` 242 B (Ratatui MIT attribution) | 10,646 entries, not truncated |
| cedar-policy/cedar | 2c2b84772a63 | `2c2b84772a63e8a5d57d98037b9389c5fd3812a3` | 2026-10-26 | Apache-2.0 (`LICENSE` 10,142 B); `NOTICE` 29 B ("Copyright Cedar Contributors"); `THIRD_PARTY_LICENSES.txt` | 1,116 entries |
| agentclientprotocol/agent-client-protocol | e50f62b4 | `e50f62b4a1ca8d794a4c97210acd8a0d833b05c5` | 2026-10-27 | Apache-2.0 (`LICENSE` 10,782 B) | 311 entries |
| agentclientprotocol/rust-sdk | 644377ad | `644377ad2654415c76c979c795d6c568e17a6d62` | 2026-10-26 | Apache-2.0 (`LICENSE` 10,783 B) | 301 entries |
| agentclientprotocol/typescript-sdk | bca8e491 | `bca8e49199927e167fab74db4dd76dec4743bb49` | 2026-10-26 | Apache-2.0 (`LICENSE` 10,783 B) | 155 entries |
| modelcontextprotocol/typescript-sdk | b415e60b | `b415e60bdf0e8dd5d6cbe7e6353abfb982b06dd2` | 2026-10-26 | **Mixed**: GitHub API says NOASSERTION; root `LICENSE` (12,227 B) = transition notice + Apache-2.0 text + MIT text + CC-BY-4.0 docs | 1,583 entries |
| modelcontextprotocol/rust-sdk | cd88056f | `cd88056ffdc97756fbd98e5a12bbeb41758f0ce8` | 2026-10-26 | Same mixed `LICENSE` (12,227 B); `crates/rmcp*/LICENSE` are 13-byte link stubs | 357 entries |
| excalidraw/excalidraw | 808d068e1826 | `808d068e18266ff9311809c23c19261fa0eb1014` | 2026-10-27 | MIT (`LICENSE` 1,067 B) | 1,470 entries |
| style-dictionary/style-dictionary | f82e7aafbcae | `f82e7aafbcaed3ca9009ec53859fbe05ed0c96a8` | 2026-10-27 | Apache-2.0 (`LICENSE` 9,793 B); `NOTICE` 58 B | 1,254 entries |
| microsoft/monaco-editor | dbf1945df2ff | `dbf1945df2ff7e46512d2f548cc5c0977a3eadd8` | 2026-10-22 | MIT (`LICENSE.txt` 1,098 B); `ThirdPartyNotices.txt` 60,394 B | 1,294 entries |
| onlook-dev/onlook | 423e2e924366 | `423e2e924366419e418ee049093872d535eea41a` | 2026-07-22 | Apache-2.0 (`LICENSE.md` 11,342 B); no NOTICE | 2,221 entries |

Citation form is `path@SHA7` where SHA7 is the first 7 hex of the pin (orca `e310a63`, codex `603a7ba`, cedar `2c2b847`, acp-schema `e50f62b`,
acp-rust `644377a`, acp-ts `bca8e49`, mcp-ts `b415e60`, mcp-rust `cd88056`, excalidraw `808d068`, style-dictionary `f82e7aa`, monaco `dbf1945`, onlook `423e2e9`).

### 0.2 Copy modes

| Mode | Meaning |
|---|---|
| COPY AS-IS | Files are copied byte-identical (rename of package scope only), with licence header and a provenance file `PROVENANCE.md` (repo, full SHA, path list, blob SHAs). |
| PORT-ADAPT | Files are copied then modified; each modified file keeps the upstream copyright line and gains a "Modified by Zain" note. The blob SHA column is the audit anchor for diffs. |
| DEPEND-ON-PACKAGE | Nothing is copied. Zain takes a registry dependency (npm or crates.io) at a pinned version. The file list is the upstream surface the package is built from, listed for audit, not for copy. |
| REFERENCE | Read-only. No code crosses. |

### 0.3 Table columns and destination convention

* "B" = blob size in bytes from the git tree. "blob" = first 8 hex of the git blob SHA. "k" = P (production) or T (test/fixture/harness).
* Destination paths follow the layout already used in 06/R14-R18: T3-derived workspace `packages/*`, `apps/*`; Rust `crates/*`; third-party vendored Rust under `vendor/<donor>/`.
* "Imports outside the selected set" were found by fetching every non-binary source blob in the set through `git/blobs` and scanning `import`/`from`/`require` (TypeScript) or `Cargo.toml` + `codex_*`/`use` identifiers (Rust). Where a transitive closure was computed it is stated; otherwise the marker is **UNKNOWN beyond sample**.
* Versions of external dependencies are the versions declared at the pin (workspace Cargo.toml / package.json) and, where useful, the current registry release read on 2026-10-28.

### 0.4 Cross-reference: components D26-D36 (file-level tables already exist; not redone here)

| D# | Component | File-level table |
|---|---|---|
| D26, D27 | Code Review engine (open-code-review), Continue ideas | R14 §4 "Exact file-level transplant list" (`research/R14_ZAIN_CODE_REVIEW.md`) |
| D28, D29 | PStack engineering system, verification skills | R15 §8 "File-level transplant list" + Appendix A (`research/R15_PSTACK_E2E_ENGINEERING.md`) |
| D30 | E2E framework (Playwright / Ascout) | R15 §6 "E2E source discovery" |
| D31 | Planning skills (mattpocock/skills) | R16 §5 "Copy First table" (`research/R16_AIHERO_SKILLS_PLAN_MODE.md`) |
| D32-D34 | Browser automation core, user-session lane, references | R17 §9 "File-level transplant table" (`research/R17_ZAIN_BROWSER.md`). R17 §6 also lists Orca browser code and defers D2's grab scripts to this document. |
| D35, D36 | DeskGate (Desktop Commander), Remote DC (excluded) | R18 §4 "File-level transplant table" (`research/R18_DESKGATE.md`) |

R17 line 240 states that `browser-grab-payload.ts` and `grab-guest-*.ts` merge with T3's `PickPreload` in P6 as one implementation. Section 1 (D2) is the file manifest for that merge.

---

<!-- SECTION:D2 -->
## D2. Design Mode element capture (Orca `grab-*`, `browser-grab-payload`, `browser-grab-types`)

Injected guest scripts (overlay, selection, React fiber lookup, element context, content script) that let a user point at a page element, plus the payload builder that clamps and normalises what is sent to the agent. Matrix row D2; R17 line 240 says these merge with the T3 `PickPreload` as one implementation. The selected set is the 06 pattern (`grab-*.ts`, `browser-grab-payload.ts`, `src/shared/browser-grab-types`) **plus three adjacent files in the same area** (`browser-grab-screenshot.ts`, `browser-grab-session-controller.ts`, `src/main/ipc/browser-grab-ipc.ts`), treated as host glue to be rewritten.

* Upstream: `stablyai/orca@e310a63624c86c0e91e9d77df71f038b91d79ea0`, MIT, Copyright (c) 2026 Lovecast Inc.; selected set = **15 files, 92,215 bytes** (3 test/fixture).
* Zain destination: guest scripts, payload and types: `packages/browser-core/src/design-mode/{guest/*,payload.ts,types.ts}` (pure TS, no Electron). Electron glue (screenshot, session-controller, ipc): `packages/browser-host-electron/src/design-mode/`, rewritten against the Zain `BrowserController` (R17 section 8) instead of Orca browser-manager.
* Copy mode: **PORT-ADAPT (guest scripts and payload near-verbatim; ipc and session-controller are REWRITE against Zain `BrowserController`)**
* Imports outside the selected set (prod files only; test files were not fetched): 6 direct modules; closure to depth 2 reached 27 modules / 131,051 bytes; closure **UNKNOWN beyond depth 2 / 160-module cap**.

| module outside the set (direct import from prod files) | B | importers in set |
|---|---:|---:|
| `src/main/browser/browser-manager.ts` | 1027 | 1 |
| `src/main/browser/doc-preview-grant-registry.ts` | 9509 | 1 |
| `src/main/ipc/browser-renderer-trust.ts` | 767 | 1 |
| `src/main/ipc/browser-tab-registration-wait.ts` | 4524 | 1 |
| `src/shared/browser-annotation-viewport-bridge.ts` | 11648 | 1 |
| `src/shared/browser-composed-tree-script.ts` | 873 | 1 |

* External packages (versions declared at the pin; licenses from npm registry JSON, read-only):

| package | declared at pin | license (npm registry JSON) | seen in |
|---|---|---|---|
| `electron` | 43.8.1 (devDependencies) | MIT (latest 45.1.0) | in-set |

* Coupling flags (grep of prod files in the set): `electron`: 1 file(s).
* License / NOTICE: MIT: keep the `LICENSE` text and the copyright line (Lovecast Inc.) in `third_party/orca/LICENSE`; add `// Derived from stablyai/orca@e310a63 (MIT)` and a PROVENANCE row per copied file. No NOTICE file exists upstream (none in the 40,641-entry tree). Brand: do not ship Orca names or logos; rename identifiers (`orca`, `Orca`, `OrcaComputerUse*`) in the port.
* Risks: (1) The ipc file imports `browser-manager.ts`, `doc-preview-grant-registry.ts`, `browser-renderer-trust.ts`, `browser-tab-registration-wait.ts` (Electron-only trust model): do not copy those edges; derive trust from the Zain origin-bound session. (2) Guest scripts run inside untrusted pages: a global leak or prototype pollution is attack surface; captured page text is data and must never be treated as instructions (R03B). (3) `grab-guest-react-script.ts` reads React internals and fails on production builds or future React versions. (4) The scripts depend on `src/shared/browser-annotation-viewport-bridge.ts` and `src/shared/browser-composed-tree-script.ts`, outside the set: add both to the copy (see outside-set table). (5) Screenshot capture may contain secrets; clamp and redaction live in `browser-grab-payload.ts` (7,383 B), the security-relevant file: port it only together with its test.
* Qualification tests: Positive: carry `browser-grab-payload.test.ts` (6,520 B), `grab-guest-script.test.ts` (12,745 B) and `grab-guest-overlay-follow.test.ts` (9,237 B) (vitest + happy-dom) and map to AT-01..05 (03B). Negative (new): the payload clamp truncates a 10 MB outerHTML; password inputs and `autocomplete=cc-number` values never appear in the payload; text such as `Ignore previous instructions` is delivered inside a data-labelled field and never concatenated into a system prompt; guest injection is idempotent and leaves no globals even if the page freezes `Object.prototype`; closed shadow roots and cross-origin iframes yield an explicit `unreachable` marker instead of a partial leak; capture on a non-allowlisted origin is refused by the Zain host.

<details><summary>File list with blob sizes</summary>

| path @ e310a63 | B | blob | k |
|---|---:|---|---|
| `src/main/browser/browser-grab-payload.test.ts` | 6520 | 1a4d6db2 | T |
| `src/main/browser/browser-grab-payload.ts` | 7383 | 717d4832 | P |
| `src/main/browser/browser-grab-screenshot.ts` | 3157 | a2888c5a | P |
| `src/main/browser/browser-grab-session-controller.ts` | 6548 | 7e971821 | P |
| `src/main/browser/grab-guest-content-script.ts` | 5243 | 7a558af3 | P |
| `src/main/browser/grab-guest-element-context-script.ts` | 7286 | eb74cf87 | P |
| `src/main/browser/grab-guest-foundation-script.ts` | 4246 | e9e0082c | P |
| `src/main/browser/grab-guest-overlay-follow.test.ts` | 9237 | c38c6b8f | T |
| `src/main/browser/grab-guest-overlay-script.ts` | 6959 | 2b0c9f6c | P |
| `src/main/browser/grab-guest-react-script.ts` | 5361 | 3790e034 | P |
| `src/main/browser/grab-guest-script.test.ts` | 12745 | e85dbaf4 | T |
| `src/main/browser/grab-guest-script.ts` | 1313 | 0dd02a40 | P |
| `src/main/browser/grab-guest-selection-scripts.ts` | 3369 | 1e8a5018 | P |
| `src/main/ipc/browser-grab-ipc.ts` | 7126 | 2d23f6e2 | P |
| `src/shared/browser-grab-types.ts` | 5722 | f4f3c86c | P |

</details>

---

<!-- SECTION:D3 -->
## D3. CLI agent catalog + agent hook listener + program-status (OSC 7501)

`tui-agent-config` is the data table of launch and ready rules per CLI agent; `agent-hook-listener` normalises vendor hook payloads (Claude, Codex, Gemini, Grok, Cursor, Droid, Copilot, OpenCode family, Pi family and others) into one status stream; `program-status` is the OSC 7501 projector, facet store and pane timers. Matrix row D3. **The set is not closed**: the hook listener imports dozens of sibling modules in `src/shared/` (table below) that must be copied with it, otherwise it does not type-check. The main-process hook installers (`src/main/agent-hooks`, 13,874 LOC per R03D section 14) are NOT selected and must not be copied: they write into the user global agent configs, which 06 forbids.

* Upstream: `stablyai/orca@e310a63624c86c0e91e9d77df71f038b91d79ea0`, MIT, Copyright (c) 2026 Lovecast Inc.; selected set = **135 files, 760,665 bytes** (47 test/fixture).
* Zain destination: catalog: `packages/agent-catalog/src/` (COPY AS-IS data and types); listener and projector: `packages/agent-status/src/{hook-listener,program-status}/` (PORT-ADAPT); outside-set modules: `packages/agent-status/src/shared/`. Per-launch overlay writer and authenticated loopback endpoint: new Zain code in `apps/server/src/agentHooks/`.
* Copy mode: **catalog files (`tui-agent-config.ts`, `tui-agent-config-types.ts`, `require-tui-agent-config.ts`) COPY AS-IS then curate; listener + program-status PORT-ADAPT; outside-set `src/shared` modules PORT-ADAPT together with the set**
* Imports outside the selected set (prod files only; test files were not fetched): 44 direct modules; closure to depth 2 reached 108 modules / 487,545 bytes; closure **UNKNOWN beyond depth 2 / 160-module cap**.

| module outside the set (direct import from prod files) | B | importers in set |
|---|---:|---:|
| `src/shared/agent-effort-level.ts` | 328 | 1 |
| `src/shared/agent-hook-endpoint-temp-cleanup.ts` | 1176 | 1 |
| `src/shared/agent-hook-relay.ts` | 7924 | 11 |
| `src/shared/agent-hook-row-child-work-fold.ts` | 1088 | 1 |
| `src/shared/agent-hook-transport-interference.ts` | 3483 | 1 |
| `src/shared/agent-hook-turn-end-timing.ts` | 6141 | 1 |
| `src/shared/agent-hook-types.ts` | 1387 | 1 |
| `src/shared/agent-lead-status-fold.ts` | 3073 | 9 |
| `src/shared/agent-process-presence.ts` | 3631 | 2 |
| `src/shared/agent-question-answered-intent.ts` | 3402 | 10 |
| `src/shared/agent-session-resume.ts` | 12232 | 3 |
| `src/shared/agent-status-child-work-liveness.ts` | 3456 | 2 |
| `src/shared/agent-status-child-work-value-guards.ts` | 2593 | 1 |
| `src/shared/agent-status-child-work.ts` | 4455 | 1 |
| `src/shared/agent-status-field-normalization.ts` | 8539 | 1 |
| `src/shared/agent-status-identity.ts` | 3518 | 1 |
| `src/shared/agent-status-legacy-adapter.ts` | 6858 | 1 |
| `src/shared/agent-status-legacy-ingress-manifest.ts` | 4093 | 1 |
| `src/shared/agent-status-osc.ts` | 5854 | 1 |
| `src/shared/agent-status-subagent-snapshot.ts` | 3398 | 1 |
| `src/shared/agent-status-terminal-owner.ts` | 1706 | 1 |
| `src/shared/agent-status-types.ts` | 18081 | 32 |
| `src/shared/agent-title-core.ts` | 6071 | 2 |
| `src/shared/agent-turn-outcome.ts` | 1769 | 2 |
| `src/shared/claude-background-task-inventory.ts` | 3281 | 2 |
| `src/shared/claude-compact-completion.ts` | 2939 | 1 |
| `src/shared/claude-owed-task-notifications.ts` | 8552 | 4 |
| `src/shared/claude-subagent-roster.ts` | 12343 | 7 |
| `src/shared/claude-task-notification-text.ts` | 907 | 1 |
| `src/shared/codex-rollout-jsonl-cursor.ts` | 3532 | 1 |
| `src/shared/codex-subagent-reviewer.ts` | 3583 | 1 |
| `src/shared/codex-subagent-roster.ts` | 4325 | 3 |
| `src/shared/codex-subagent-transcript.ts` | 10737 | 4 |
| `src/shared/cross-platform-path.ts` | 10153 | 1 |
| `src/shared/grok-session-paths.ts` | 9579 | 1 |
| `src/shared/harness-injected-user-turns.ts` | 2809 | 2 |
| `src/shared/jcode-session-files.ts` | 6580 | 2 |
| `src/shared/json-text-structure-limit.ts` | 3566 | 1 |
| `src/shared/muse-session-log.ts` | 4941 | 2 |
| `src/shared/omp-plan-review-prompt.ts` | 3235 | 2 |
| `src/shared/orca-cli-command-name.ts` | 775 | 1 |
| `src/shared/own-retained-string.ts` | 1567 | 1 |
| `src/shared/stable-pane-id.ts` | 2219 | 2 |
| `src/shared/tui-agent.ts` | 1035 | 2 |

* External packages (versions declared at the pin; licenses from npm registry JSON, read-only):

| package | declared at pin | license (npm registry JSON) | seen in |
|---|---|---|---|
| `@noble/hashes` | 1.8.0 (devDependencies) | MIT (latest 2.4.0) | closure only |

* Coupling flags (grep of prod files in the set): `net-or-fetch`: 2 file(s); `node:fs`: 3 file(s); `node:http`: 2 file(s); `node:os`: 1 file(s); `process.platform`: 1 file(s).
* License / NOTICE: MIT: keep the `LICENSE` text and the copyright line (Lovecast Inc.) in `third_party/orca/LICENSE`; add `// Derived from stablyai/orca@e310a63 (MIT)` and a PROVENANCE row per copied file. No NOTICE file exists upstream (none in the 40,641-entry tree). Brand: do not ship Orca names or logos; rename identifiers (`orca`, `Orca`, `OrcaComputerUse*`) in the port.
* Risks: (1) Catalog drift: every vendor CLI release can change the prompts and titles that readiness rules key on (for example `draftPasteReadySignal: claude-composer-prompt` and the CLAUDE_CODE_DISABLE_TERMINAL_TITLE comment in `tui-agent-config.ts`); needs an owner and a nightly fixture run. (2) `agent-hook-listener/endpoint-publication.ts` and the outside-set `agent-hook-endpoint-temp-cleanup.ts` publish an endpoint through temp files: in Zain the endpoint must be per-PTY-secret authenticated and ACL-restricted so other local processes cannot spoof status (06 D3). (3) Provider handlers read transcripts (`transcript-reader.ts`, `command-code-transcript.ts`, `grok-result-discovery.ts`, `codex-rollout-jsonl-cursor.ts`): re-verify path-traversal and large-file limits. (4) Orca CLI names (`orca-cli-command-name.ts`, a `claude-agent-teams` entry whose `detectCmd` is `orca`) must be removed. (5) CLI agents remain UNMEDIATED workers (07 section 6): status from this listener is advisory and never an authorization input.
* Qualification tests: Positive: the upstream suites in the set (46 test files: `agent-hook-listener-*.test.ts`, `program-status/*.test.ts`, `osc-scanner.test.ts`) run unchanged in vitest. Negative (new): a hook POST without the per-PTY secret is rejected; a body over the `listener-limits.ts` limits is rejected; an OSC 7501 sequence from a program that does not own the pane is ignored; a `completed` status from a stale session after `session-replacement` does not override a live one; hook files are never written under the real user `~/.claude` or `~/.codex` (assert on the filesystem); a malformed transcript line does not crash the poller.

<details><summary>File list with blob sizes</summary>

| path @ e310a63 | B | blob | k |
|---|---:|---|---|
| `src/shared/agent-hook-listener-antigravity.test.ts` | 18395 | fa1ec17e | T |
| `src/shared/agent-hook-listener-claude-compatible-vendors.test.ts` | 12431 | f4b8966c | T |
| `src/shared/agent-hook-listener-claude-elicitation.test.ts` | 3330 | a507b545 | T |
| `src/shared/agent-hook-listener-claude-reordered-task-notification.test.ts` | 5063 | cb58126a | T |
| `src/shared/agent-hook-listener-claude-subagents.test.ts` | 29159 | c8911601 | T |
| `src/shared/agent-hook-listener-claude-task-notification.test.ts` | 21177 | 3bf28648 | T |
| `src/shared/agent-hook-listener-claude-turn-state.test.ts` | 19772 | f42d9c82 | T |
| `src/shared/agent-hook-listener-codex-approval-ownership.test.ts` | 8368 | c32ec22e | T |
| `src/shared/agent-hook-listener-codex-interrupt.test.ts` | 3820 | 3b98c764 | T |
| `src/shared/agent-hook-listener-codex-main-agent.test.ts` | 3075 | d7d0d230 | T |
| `src/shared/agent-hook-listener-codex-subagent-names.test.ts` | 3487 | a36585f1 | T |
| `src/shared/agent-hook-listener-command-code-transcript.test.ts` | 19308 | c8e832dc | T |
| `src/shared/agent-hook-listener-extraction-characterization.test.ts` | 12882 | aada0f64 | T |
| `src/shared/agent-hook-listener-grok-completion.test.ts` | 14375 | af37cb05 | T |
| `src/shared/agent-hook-listener-grok.test.ts` | 16708 | ad603d95 | T |
| `src/shared/agent-hook-listener-hermes-codex-droid.test.ts` | 9822 | 506dd687 | T |
| `src/shared/agent-hook-listener-interactive-prompts.test.ts` | 11238 | 34a14d19 | T |
| `src/shared/agent-hook-listener-jcode.test.ts` | 8492 | 0a3f250c | T |
| `src/shared/agent-hook-listener-omp-approval-ownership.test.ts` | 5471 | 2a751c6e | T |
| `src/shared/agent-hook-listener-omp-plan-review.test.ts` | 3479 | 046aac7d | T |
| `src/shared/agent-hook-listener-opencode-reattribution.test.ts` | 4784 | b7b0f05e | T |
| `src/shared/agent-hook-listener-opencode-session-correlation.test.ts` | 8072 | 2a1914dc | T |
| `src/shared/agent-hook-listener-opencode-session-registry.test.ts` | 4251 | 846294cb | T |
| `src/shared/agent-hook-listener-opencode-tui-identity.test.ts` | 6637 | 8e31013b | T |
| `src/shared/agent-hook-listener-pi-compatible.test.ts` | 13407 | 1828e06e | T |
| `src/shared/agent-hook-listener-roster-retention.test.ts` | 2798 | dbe5b311 | T |
| `src/shared/agent-hook-listener-session-replacement.test.ts` | 7404 | a9797450 | T |
| `src/shared/agent-hook-listener-startless-child-lifecycle.test.ts` | 11003 | e560e716 | T |
| `src/shared/agent-hook-listener-test-harness.ts` | 863 | 9cd1c2bb | T |
| `src/shared/agent-hook-listener-transport.test.ts` | 13110 | 831203a0 | T |
| `src/shared/agent-hook-listener.ts` | 11929 | 2836d384 | P |
| `src/shared/agent-hook-listener/claude-session-continuation.test.ts` | 14048 | 3fe16c46 | T |
| `src/shared/agent-hook-listener/claude-session-continuation.ts` | 11291 | ad974177 | P |
| `src/shared/agent-hook-listener/claude-settled-permission-requests.test.ts` | 4644 | 73bcbf2b | T |
| `src/shared/agent-hook-listener/claude-settled-permission-requests.ts` | 4649 | 7dde959a | P |
| `src/shared/agent-hook-listener/command-code-transcript.ts` | 3822 | 75397449 | P |
| `src/shared/agent-hook-listener/endpoint-publication.ts` | 2983 | fcadae88 | P |
| `src/shared/agent-hook-listener/grok-result-discovery.ts` | 6899 | 14faae66 | P |
| `src/shared/agent-hook-listener/hook-envelope.ts` | 5499 | caadb3d5 | P |
| `src/shared/agent-hook-listener/interactive-tool.ts` | 4221 | 8a1c00dc | P |
| `src/shared/agent-hook-listener/listener-event.ts` | 4728 | 180a60ec | P |
| `src/shared/agent-hook-listener/listener-limits.ts` | 3096 | 838c46e3 | P |
| `src/shared/agent-hook-listener/listener-state.ts` | 16262 | 6a56bbae | P |
| `src/shared/agent-hook-listener/main-agent-turn-state.ts` | 2129 | 0abddcc0 | P |
| `src/shared/agent-hook-listener/opencode-session-correlation.ts` | 7095 | 283c1649 | P |
| `src/shared/agent-hook-listener/opencode-session-registry.ts` | 7541 | f07ce955 | P |
| `src/shared/agent-hook-listener/pane-provider-session.ts` | 3298 | 2b30227d | P |
| `src/shared/agent-hook-listener/pane-scoped-cache-entries.ts` | 1297 | 077ba8f4 | P |
| `src/shared/agent-hook-listener/prompt-fields.ts` | 5511 | 5d3a3744 | P |
| `src/shared/agent-hook-listener/provider-dispatch.ts` | 9315 | ad9c244b | P |
| `src/shared/agent-hook-listener/provider-event-names.ts` | 473 | f21d61ac | P |
| `src/shared/agent-hook-listener/provider-event-routing.ts` | 10067 | c40460be | P |
| `src/shared/agent-hook-listener/providers/amp-events.ts` | 5006 | f7fe0e54 | P |
| `src/shared/agent-hook-listener/providers/amp-tool-fields.ts` | 1741 | 2bd8d3a8 | P |
| `src/shared/agent-hook-listener/providers/antigravity-event-rules.ts` | 254 | aab23c61 | P |
| `src/shared/agent-hook-listener/providers/antigravity-events.ts` | 4466 | 3e8b36ab | P |
| `src/shared/agent-hook-listener/providers/antigravity-tool-fields.ts` | 1748 | ba57349f | P |
| `src/shared/agent-hook-listener/providers/claude-events.ts` | 14842 | f5a35f37 | P |
| `src/shared/agent-hook-listener/providers/claude-lifecycle-events.ts` | 6965 | 9a3fb289 | P |
| `src/shared/agent-hook-listener/providers/claude-pane-hold-evidence.ts` | 3643 | c9df6e9c | P |
| `src/shared/agent-hook-listener/providers/claude-roster-state.ts` | 10832 | ba7a73ef | P |
| `src/shared/agent-hook-listener/providers/claude-status-build.ts` | 2643 | adfb9445 | P |
| `src/shared/agent-hook-listener/providers/claude-task-notification-delivery.ts` | 3056 | 8451216b | P |
| `src/shared/agent-hook-listener/providers/claude-teammate-spawn.ts` | 1434 | 65926f60 | P |
| `src/shared/agent-hook-listener/providers/claude-tool-fields.ts` | 2124 | f0ce6fb4 | P |
| `src/shared/agent-hook-listener/providers/codex-ephemeral-threads.ts` | 3116 | f4f1daf6 | P |
| `src/shared/agent-hook-listener/providers/codex-events.ts` | 11191 | c2bb1436 | P |
| `src/shared/agent-hook-listener/providers/codex-state.ts` | 9356 | fb2c7883 | P |
| `src/shared/agent-hook-listener/providers/codex-tool-fields.ts` | 1315 | 09b87c79 | P |
| `src/shared/agent-hook-listener/providers/codex-transcript-poll.ts` | 2270 | 6ab37d5a | P |
| `src/shared/agent-hook-listener/providers/command-code-events.ts` | 1401 | d9efcd51 | P |
| `src/shared/agent-hook-listener/providers/command-code-tool-fields.ts` | 1768 | 5d785d83 | P |
| `src/shared/agent-hook-listener/providers/compatible-lifecycle-events.ts` | 3642 | ba7362b8 | P |
| `src/shared/agent-hook-listener/providers/copilot-events.ts` | 2905 | a0749f19 | P |
| `src/shared/agent-hook-listener/providers/copilot-tool-fields.ts` | 6576 | 491be19a | P |
| `src/shared/agent-hook-listener/providers/cursor-events.ts` | 2316 | 71ff5d52 | P |
| `src/shared/agent-hook-listener/providers/cursor-tool-fields.ts` | 2502 | 7e0ab173 | P |
| `src/shared/agent-hook-listener/providers/devin-events.ts` | 2123 | 9ebe16f6 | P |
| `src/shared/agent-hook-listener/providers/droid-events.ts` | 2971 | bf5022df | P |
| `src/shared/agent-hook-listener/providers/droid-tool-fields.ts` | 3406 | eaf6df48 | P |
| `src/shared/agent-hook-listener/providers/dsh-events.test.ts` | 4171 | 70dbb430 | T |
| `src/shared/agent-hook-listener/providers/dsh-events.ts` | 2452 | 3dc2b0d1 | P |
| `src/shared/agent-hook-listener/providers/gemini-events.ts` | 1627 | 189b8c7e | P |
| `src/shared/agent-hook-listener/providers/gemini-tool-fields.ts` | 1074 | 9fadfea6 | P |
| `src/shared/agent-hook-listener/providers/grok-events.ts` | 9822 | a03ea9a7 | P |
| `src/shared/agent-hook-listener/providers/grok-tool-fields.ts` | 4464 | 38b8ba4a | P |
| `src/shared/agent-hook-listener/providers/hermes-events.test.ts` | 3975 | 063973a0 | T |
| `src/shared/agent-hook-listener/providers/hermes-events.ts` | 3733 | efe003fc | P |
| `src/shared/agent-hook-listener/providers/hermes-tool-fields.ts` | 2386 | 865e92b2 | P |
| `src/shared/agent-hook-listener/providers/jcode-events.ts` | 2590 | b901e868 | P |
| `src/shared/agent-hook-listener/providers/jcode-tool-fields.ts` | 2857 | 78a72ff4 | P |
| `src/shared/agent-hook-listener/providers/jcode-turn-prompt.test.ts` | 3074 | a44f7877 | T |
| `src/shared/agent-hook-listener/providers/jcode-turn-prompt.ts` | 855 | 7b6459bd | P |
| `src/shared/agent-hook-listener/providers/kimi-events.ts` | 2843 | 17193e25 | P |
| `src/shared/agent-hook-listener/providers/kiro-events.test.ts` | 5208 | 3dbf1a42 | T |
| `src/shared/agent-hook-listener/providers/kiro-events.ts` | 1774 | d0ce7e7d | P |
| `src/shared/agent-hook-listener/providers/kiro-tool-fields.ts` | 1199 | 7d5fe877 | P |
| `src/shared/agent-hook-listener/providers/muse-events.test.ts` | 7572 | b547bb7f | T |
| `src/shared/agent-hook-listener/providers/muse-events.ts` | 4839 | 8219a965 | P |
| `src/shared/agent-hook-listener/providers/opencode-family-events.ts` | 2973 | 55b3e775 | P |
| `src/shared/agent-hook-listener/providers/opencode-family-tool-fields.ts` | 2518 | 1afec20f | P |
| `src/shared/agent-hook-listener/providers/pi-family-events.ts` | 6744 | 6337e000 | P |
| `src/shared/agent-hook-listener/providers/pi-family-tool-fields.ts` | 3878 | 17029800 | P |
| `src/shared/agent-hook-listener/providers/qoder-events.ts` | 447 | c83923d5 | P |
| `src/shared/agent-hook-listener/providers/zcode-events.test.ts` | 5281 | e4283dbd | T |
| `src/shared/agent-hook-listener/providers/zcode-events.ts` | 3155 | 0fb9760b | P |
| `src/shared/agent-hook-listener/request-body.ts` | 4261 | 4300779e | P |
| `src/shared/agent-hook-listener/reverse-file-region-scan.test.ts` | 3320 | e8f49155 | T |
| `src/shared/agent-hook-listener/reverse-file-region-scan.ts` | 2601 | ad189a67 | P |
| `src/shared/agent-hook-listener/source-routing.ts` | 1088 | 382834b3 | P |
| `src/shared/agent-hook-listener/tool-input-preview.ts` | 5157 | 935150ea | P |
| `src/shared/agent-hook-listener/transcript-entry-text.ts` | 1673 | 3daa36b3 | P |
| `src/shared/agent-hook-listener/transcript-lines.ts` | 1828 | 0ea5a06f | P |
| `src/shared/agent-hook-listener/transcript-poll-policy.ts` | 2674 | 16e81735 | P |
| `src/shared/agent-hook-listener/transcript-reader.test.ts` | 2413 | 83780b08 | T |
| `src/shared/agent-hook-listener/transcript-reader.ts` | 1334 | 4051f1ef | P |
| `src/shared/program-status/activity.ts` | 549 | d1ea4e8e | P |
| `src/shared/program-status/agent-status-projector.test.ts` | 12946 | b043fe36 | T |
| `src/shared/program-status/agent-status-projector.ts` | 11637 | 0f810d73 | P |
| `src/shared/program-status/facet.ts` | 3749 | ce2b8320 | P |
| `src/shared/program-status/osc-scanner.test.ts` | 3085 | f5858e37 | T |
| `src/shared/program-status/osc-scanner.ts` | 5637 | d2bab413 | P |
| `src/shared/program-status/presentation.test.ts` | 1889 | 3407e054 | T |
| `src/shared/program-status/presentation.ts` | 3157 | 0472238d | P |
| `src/shared/program-status/protocol.test.ts` | 4782 | f9491414 | T |
| `src/shared/program-status/protocol.ts` | 7024 | eb49df0b | P |
| `src/shared/program-status/query-responder.test.ts` | 1431 | 713d72dd | T |
| `src/shared/program-status/query-responder.ts` | 988 | 7baa8823 | P |
| `src/shared/program-status/records.test.ts` | 2809 | 23befe30 | T |
| `src/shared/program-status/records.ts` | 3855 | 6ed693af | P |
| `src/shared/program-status/title-activity-order.ts` | 851 | b139f1a6 | P |
| `src/shared/require-tui-agent-config.test.ts` | 969 | a399fffd | T |
| `src/shared/require-tui-agent-config.ts` | 550 | 329484e1 | P |
| `src/shared/tui-agent-config-types.ts` | 4372 | 5bddcc31 | P |
| `src/shared/tui-agent-config.ts` | 13935 | 501dc89f | P |

</details>

---

<!-- SECTION:D4 -->
## D4. Windows-safe process host (`@orca/process-host`)

A workspace package: spawn, cancel, process-tree termination (Windows tree kill and POSIX group kill with an lsof probe), Windows command-line quoting, `.cmd` shim resolution, bounded output sink, growing byte buffer. Matrix row D4 (COPY AS-IS with rename). R03D section 14 row 1: 1,896 production LOC in 20 files, Node only.

* Upstream: `stablyai/orca@e310a63624c86c0e91e9d77df71f038b91d79ea0`, MIT, Copyright (c) 2026 Lovecast Inc.; selected set = **41 files, 144,417 bytes** (17 test/fixture).
* Zain destination: `packages/process-host/` (rename the package `@orca/process-host` to `@zain/process-host`; rename the `orca-source` export condition to `zain-source`). Used by Zain Server for every child process spawn.
* Copy mode: **COPY AS-IS (package-scope and identifier rename only)**
* Imports outside the selected set (prod files only; test files were not fetched): 0 direct modules; closure to depth 0 reached 0 modules / 0 bytes; closure complete.

none.

* External packages (versions declared at the pin; licenses from npm registry JSON, read-only):

| package | declared at pin | license (npm registry JSON) | seen in |
|---|---|---|---|
| `@orca/process-host` | workspace:* (dependencies) | ? (latest ?) | in-set |
| `child_process` | not in root or process-host package.json (transitive or builtin)  | ISC (latest 1.0.2) | in-set |
| `fs` | not in root or process-host package.json (transitive or builtin)  | ISC (latest 0.0.1-security) | in-set |
| `proper-lockfile` | 4.1.2 (dependencies) | MIT (latest 4.1.2) | in-set |
| `vitest` | 5.0.5 (devDependencies) | MIT (latest 5.0.5) | in-set |

* Coupling flags (grep of prod files in the set): `child_process`: 7 file(s); `node:child_process`: 6 file(s); `node:fs`: 2 file(s); `node:os`: 1 file(s); `process.platform`: 4 file(s).
* License / NOTICE: MIT: keep the `LICENSE` text and the copyright line (Lovecast Inc.) in `third_party/orca/LICENSE`; add `// Derived from stablyai/orca@e310a63 (MIT)` and a PROVENANCE row per copied file. No NOTICE file exists upstream (none in the 40,641-entry tree). Brand: do not ship Orca names or logos; rename identifiers (`orca`, `Orca`, `OrcaComputerUse*`) in the port. `package.json` is `private: true` and carries no licence field.
* Risks: (1) Windows tree kill and cmd-shim resolution are OS-version sensitive; upstream CI coverage of Windows 11 24H2/25H2 is not proven and the founder machine is Windows 11 Home. (2) `scripts/build-dist.mjs` (6,294 B) builds `dist/`; Zain build must run or replace it. (3) The POSIX lsof probe shells out to `lsof`. (4) `windows-cmd-shim-resolution.ts` (9,433 B) parses npm `.cmd` shims: an injection surface if shim bodies are attacker-controlled; fixtures exist in `windows-cmd-shim-bodies.ts`, extend them. (5) R03D lists `proper-lockfile` as dev-only; confirm in the dependency table below.
* Qualification tests: Positive: carry all 15 upstream test files and run them on Windows 11. Negative (new): an argument corpus containing `& calc`, `^`, `%PATH%`, quotes and trailing backslashes reaches the child verbatim and never starts a second program (extends `windows-argument-corpus.ts`); a detached grandchild is still killed with its parent; killing an already-exited PID or a reused PID never kills an unrelated process (`retryable-process-exit-proof`); a 1 GB output flood stays bounded; `process-tree-kill-gate` refuses PID 0, PID 4 and the Zain server itself.

<details><summary>File list with blob sizes</summary>

| path @ e310a63 | B | blob | k |
|---|---:|---|---|
| `src/packages/process-host/.gitignore` | 35 | 491b6848 | P |
| `src/packages/process-host/README.md` | 3966 | 5b6919ae | P |
| `src/packages/process-host/package.json` | 4003 | 045f2baf | P |
| `src/packages/process-host/scripts/build-dist.mjs` | 6294 | 8fbbb6b4 | P |
| `src/packages/process-host/src/__fixtures__/windows-argument-corpus.ts` | 1599 | 913c5545 | T |
| `src/packages/process-host/src/__fixtures__/windows-cmd-shim-bodies.ts` | 3097 | 476d6ef8 | T |
| `src/packages/process-host/src/bounded-output-sink.test.ts` | 2485 | f8630725 | T |
| `src/packages/process-host/src/bounded-output-sink.ts` | 1315 | b63a852f | P |
| `src/packages/process-host/src/cancel-process-acquisition.ts` | 740 | 073e6998 | P |
| `src/packages/process-host/src/child-termination-reporter.ts` | 421 | 907c98b9 | P |
| `src/packages/process-host/src/close-process-registry.test.ts` | 1415 | 6a3831a1 | T |
| `src/packages/process-host/src/close-process-registry.ts` | 716 | 04b5282a | P |
| `src/packages/process-host/src/fork-process.ts` | 1484 | 9afa15ea | P |
| `src/packages/process-host/src/growing-byte-buffer.test.ts` | 3803 | 8a489cec | T |
| `src/packages/process-host/src/growing-byte-buffer.ts` | 3852 | c384d228 | P |
| `src/packages/process-host/src/posix-lsof-probe.test.ts` | 7835 | 9a1fe81f | T |
| `src/packages/process-host/src/posix-lsof-probe.ts` | 5526 | faaa95bf | P |
| `src/packages/process-host/src/process-spec.ts` | 2638 | 0014b867 | P |
| `src/packages/process-host/src/process-tree-kill-gate.ts` | 902 | d6555a8a | P |
| `src/packages/process-host/src/process-tree-termination.test.ts` | 7989 | 9b9872c5 | T |
| `src/packages/process-host/src/process-tree-termination.ts` | 4912 | 55f76d6c | P |
| `src/packages/process-host/src/retryable-process-exit-proof.test.ts` | 1462 | bda5a235 | T |
| `src/packages/process-host/src/retryable-process-exit-proof.ts` | 669 | 675a038f | P |
| `src/packages/process-host/src/run-process-bytes.test.ts` | 2973 | 0827d82b | T |
| `src/packages/process-host/src/run-process-termination-failure.test.ts` | 6360 | 3ba2e6b2 | T |
| `src/packages/process-host/src/run-process-windows-tree-kill.test.ts` | 4740 | 692286cc | T |
| `src/packages/process-host/src/run-process.test.ts` | 10454 | bb6ba7ef | T |
| `src/packages/process-host/src/run-process.ts` | 12796 | 6e634fb5 | P |
| `src/packages/process-host/src/spawn-observer.test.ts` | 2586 | 1d6eab6d | T |
| `src/packages/process-host/src/spawn-observer.ts` | 542 | 05974385 | P |
| `src/packages/process-host/src/spawn-process-stdio.test.ts` | 3384 | cfa9613e | T |
| `src/packages/process-host/src/spawn-resolution.ts` | 2122 | c0665fcb | P |
| `src/packages/process-host/src/windows-cmd-shim-resolution.ts` | 9433 | e18853f6 | P |
| `src/packages/process-host/src/windows-command-line.test.ts` | 3208 | aea18586 | T |
| `src/packages/process-host/src/windows-command-line.ts` | 3944 | 69ccec0c | P |
| `src/packages/process-host/src/windows-system-binary.ts` | 715 | cfc21b56 | P |
| `src/packages/process-host/src/windows-tree-kill.test.ts` | 8251 | 9451253c | T |
| `src/packages/process-host/src/windows-tree-kill.ts` | 4904 | 06a92223 | P |
| `src/packages/process-host/tsconfig.json` | 465 | 1f2045c8 | P |
| `src/packages/process-host/tsconfig.test.json` | 123 | 495c6f92 | T |
| `src/packages/process-host/vitest.config.ts` | 259 | 5a7d0dda | P |

</details>

---

<!-- SECTION:D5 -->
## D5. Linear integration (`src/main/linear`)

GraphQL client, issue, project and team queries, relation writes, comment handling, inline-image fetching, token store and workspace registry built on `@linear/sdk`. Matrix row D5 (PORT, 6.8k LOC, low coupling).

* Upstream: `stablyai/orca@e310a63624c86c0e91e9d77df71f038b91d79ea0`, MIT, Copyright (c) 2026 Lovecast Inc.; selected set = **67 files, 358,095 bytes** (21 test/fixture).
* Zain destination: `packages/integrations-linear/src/` (new package; T3 has no Linear integration per R03D section 14 row 7). The `mcp-issue-list*.ts` helpers go to `apps/server/src/mcp/linear/`.
* Copy mode: **PORT-ADAPT (token store and credential paths replaced; `mcp-issue-list*` re-bound to the Zain MCP host)**
* Imports outside the selected set (prod files only; test files were not fetched): 19 direct modules; closure to depth 2 reached 31 modules / 85,722 bytes; closure **UNKNOWN beyond depth 2 / 160-module cap**.

| module outside the set (direct import from prod files) | B | importers in set |
|---|---:|---:|
| `src/main/credential-file-protection.ts` | 643 | 1 |
| `src/main/integration-credential-file.ts` | 4873 | 2 |
| `src/main/integration-state-file-cache.ts` | 1042 | 1 |
| `src/main/integration-token-file-cache.ts` | 2278 | 1 |
| `src/shared/issue-mutation-types.ts` | 1001 | 1 |
| `src/shared/linear/agent-access.ts` | 6139 | 8 |
| `src/shared/linear/agent-result-types.ts` | 7679 | 7 |
| `src/shared/linear/inline-media.ts` | 2559 | 3 |
| `src/shared/linear/issue-activity.ts` | 849 | 2 |
| `src/shared/linear/issue-attribute-filter.ts` | 8634 | 3 |
| `src/shared/linear/issue-read-limits.ts` | 258 | 6 |
| `src/shared/linear/issue-relation-write.ts` | 849 | 1 |
| `src/shared/linear/issue-types.ts` | 961 | 8 |
| `src/shared/linear/links.ts` | 7796 | 3 |
| `src/shared/linear/priority-label.ts` | 484 | 1 |
| `src/shared/linear/project-types.ts` | 2187 | 4 |
| `src/shared/linear/workspace-types.ts` | 2918 | 19 |
| `src/shared/secret-at-rest-protection.ts` | 1006 | 1 |
| `src/shared/updated-at-order.ts` | 454 | 1 |

* External packages (versions declared at the pin; licenses from npm registry JSON, read-only):

| package | declared at pin | license (npm registry JSON) | seen in |
|---|---|---|---|
| `@linear/sdk` | ^97.0.0 (dependencies) | MIT (latest 99.0.0) | in-set |

* Coupling flags (grep of prod files in the set): `node:fs`: 4 file(s); `node:os`: 1 file(s).
* License / NOTICE: MIT: keep the `LICENSE` text and the copyright line (Lovecast Inc.) in `third_party/orca/LICENSE`; add `// Derived from stablyai/orca@e310a63 (MIT)` and a PROVENANCE row per copied file. No NOTICE file exists upstream (none in the 40,641-entry tree). Brand: do not ship Orca names or logos; rename identifiers (`orca`, `Orca`, `OrcaComputerUse*`) in the port. `@linear/sdk` is MIT per the npm registry; the Linear API terms of service apply to use of the service. No Linear branding is copied.
* Risks: (1) `linear-token-store.ts` (3,355 B), `linear-credential-paths.ts` and `linear-legacy-viewer-store.ts` store credentials: replace with the Zain OS-keychain or DPAPI store; the coupling flags above show whether Electron `safeStorage` is used. (2) `linear-description-images.ts` and `issue-context/inline-media` fetch URLs taken from Linear content: SSRF and token-leak surface through redirects and signed URLs. (3) API drift on a fast-moving SDK major (`@linear/sdk ^97.0.0`). (4) Calls to `api.linear.app` must go through the Zain network policy (D9 proxy, Cedar). (5) Linear writes (`issue-relation-write`, `linear-issue-mutations`) are effects and need Core gating.
* Qualification tests: Positive: carry the 21 upstream test files (for example `client.test.ts` 19,456 B, `issues.test.ts` 28,716 B, `mcp-issue-list*.test.ts`) with recorded fixtures. Negative (new): an invalid or expired token yields a typed error that never prints the token; GraphQL partial errors do not mask data loss; pagination terminates when a cursor never advances; an inline image URL pointing at `http://169.254.169.254/` or redirecting to a private IP is refused; a mutation is blocked and receipted when Core denies it.

<details><summary>File list with blob sizes</summary>

| path @ e310a63 | B | blob | k |
|---|---:|---|---|
| `src/main/linear/client.test.ts` | 19456 | 658bc376 | T |
| `src/main/linear/client.ts` | 7300 | ed8c4e6b | P |
| `src/main/linear/issue-activity-raw.ts` | 6123 | c7838b26 | P |
| `src/main/linear/issue-context/client.test.ts` | 11076 | d53f09f5 | T |
| `src/main/linear/issue-context/client.ts` | 9244 | 9491dfce | P |
| `src/main/linear/issue-context/current.test.ts` | 2039 | 073aea07 | T |
| `src/main/linear/issue-context/current.ts` | 1865 | 6525e42f | P |
| `src/main/linear/issue-context/errors.test.ts` | 646 | 433e0b90 | T |
| `src/main/linear/issue-context/errors.ts` | 3465 | 4d205bf8 | P |
| `src/main/linear/issue-context/fanout.ts` | 1841 | cadec840 | P |
| `src/main/linear/issue-context/includes.test.ts` | 11321 | 13cd160a | T |
| `src/main/linear/issue-context/includes.ts` | 9442 | ce7b78e9 | P |
| `src/main/linear/issue-context/inline-media.test.ts` | 2859 | fb63dc15 | T |
| `src/main/linear/issue-context/pagination.ts` | 1218 | 8abe7cef | P |
| `src/main/linear/issue-context/raw.ts` | 6265 | c4fac5d1 | P |
| `src/main/linear/issue-context/read-context.test.ts` | 3160 | f6a45ac5 | T |
| `src/main/linear/issue-context/read-context.ts` | 4367 | a30112bb | P |
| `src/main/linear/issue-context/relations.test.ts` | 4254 | dae4f45b | T |
| `src/main/linear/issue-context/relations.ts` | 3127 | 5be47100 | P |
| `src/main/linear/issue-context/workspaces.ts` | 2308 | 3e5d6f37 | P |
| `src/main/linear/issue-list-filter.test.ts` | 2156 | 24fb3af3 | T |
| `src/main/linear/issue-list-filter.ts` | 3457 | aa058aca | P |
| `src/main/linear/issue-relation-mutation.ts` | 2485 | 165083f7 | P |
| `src/main/linear/issue-relation-write.test.ts` | 6742 | c1377abf | T |
| `src/main/linear/issue-relation-write.ts` | 8038 | 9a02f45f | P |
| `src/main/linear/issue-search-summary.test.ts` | 595 | 85f4ad75 | T |
| `src/main/linear/issues.test.ts` | 28716 | 80f9f0ca | T |
| `src/main/linear/linear-credential-paths.ts` | 1172 | 529e4a23 | P |
| `src/main/linear/linear-custom-view-graphql.ts` | 2032 | 8cdfd96d | P |
| `src/main/linear/linear-custom-view-queries.ts` | 5593 | fe225e64 | P |
| `src/main/linear/linear-description-images.test.ts` | 4714 | 538266ec | T |
| `src/main/linear/linear-description-images.ts` | 1596 | 2a6fd7c0 | P |
| `src/main/linear/linear-issue-comments.test.ts` | 1577 | 89427dcd | T |
| `src/main/linear/linear-issue-comments.ts` | 8074 | 69051e09 | P |
| `src/main/linear/linear-issue-detail-deadline.test.ts` | 5956 | 26fa84f4 | T |
| `src/main/linear/linear-issue-listing.ts` | 8186 | 585fe1e6 | P |
| `src/main/linear/linear-issue-lookups.ts` | 6143 | 466dae45 | P |
| `src/main/linear/linear-issue-mutations.ts` | 8503 | 5ecf00b0 | P |
| `src/main/linear/linear-issue-query-documents.ts` | 5707 | 11f4d410 | P |
| `src/main/linear/linear-issue-query-support.ts` | 5981 | 2c4b3a44 | P |
| `src/main/linear/linear-issue-write-support.ts` | 6405 | e503ca21 | P |
| `src/main/linear/linear-legacy-viewer-store.ts` | 1838 | e5f37916 | P |
| `src/main/linear/linear-project-collection-read.ts` | 2204 | d9924e46 | P |
| `src/main/linear/linear-project-graphql.ts` | 3107 | bd85f70e | P |
| `src/main/linear/linear-project-issue-queries.ts` | 2783 | 49e1b89d | P |
| `src/main/linear/linear-project-models.ts` | 8651 | 38371e70 | P |
| `src/main/linear/linear-project-nodes.ts` | 3986 | 2796ca35 | P |
| `src/main/linear/linear-project-queries.ts` | 5988 | 961d2f64 | P |
| `src/main/linear/linear-project-team-queries.ts` | 2480 | 569dd130 | P |
| `src/main/linear/linear-request-concurrency.ts` | 992 | 7b11e662 | P |
| `src/main/linear/linear-sdk.ts` | 757 | 31b30b5c | P |
| `src/main/linear/linear-team-pages.ts` | 2768 | b0e6da16 | P |
| `src/main/linear/linear-token-store.ts` | 3355 | cedf13f5 | P |
| `src/main/linear/linear-workspace-record.ts` | 1843 | ffa8625c | P |
| `src/main/linear/linear-workspace-registry.test.ts` | 1589 | 2d9e379c | T |
| `src/main/linear/linear-workspace-registry.ts` | 6844 | 1e95def7 | P |
| `src/main/linear/mappers.test.ts` | 1613 | 0fba648e | T |
| `src/main/linear/mappers.ts` | 3246 | b219a448 | P |
| `src/main/linear/mcp-issue-list-cursor.ts` | 3041 | 619ac545 | P |
| `src/main/linear/mcp-issue-list-filter.ts` | 2948 | d77aab8b | P |
| `src/main/linear/mcp-issue-list-pagination.test.ts` | 10297 | 3d2a2eab | T |
| `src/main/linear/mcp-issue-list.test.ts` | 10263 | f7e43eae | T |
| `src/main/linear/mcp-issue-list.ts` | 7196 | 6c43e4d5 | P |
| `src/main/linear/projects.test.ts` | 16355 | 45655495 | T |
| `src/main/linear/projects.ts` | 451 | 4ea2d13c | P |
| `src/main/linear/teams.test.ts` | 12807 | 0d86b04f | T |
| `src/main/linear/teams.ts` | 5489 | d10974cc | P |

</details>

---

<!-- SECTION:D6 -->
## D6. Computer-use sidecar (`src/main/computer`, `native/computer-use-*`)

TypeScript host (provider bridge, request queue, snapshot cache and rendering, permission checks) plus three native sidecars: a macOS Swift package (`main.swift` 171,152 B plus a Core library and tests), a Windows PowerShell runtime (`runtime.ps1` 54,996 B) and a Linux Python runtime (`runtime.py` 44,350 B). Matrix row D6 (PORT, Phase 9, high-risk effect class).

* Upstream: `stablyai/orca@e310a63624c86c0e91e9d77df71f038b91d79ea0`, MIT, Copyright (c) 2026 Lovecast Inc.; selected set = **96 files, 712,460 bytes** (44 test/fixture).
* Zain destination: host: `packages/computer-use/src/`; natives: `apps/desktop/native/computer-use-{macos,windows,linux}/`. Registered in Core as a high-risk effect class; every action passes Core before it reaches the sidecar.
* Copy mode: **PORT-ADAPT (Phase 9; Windows sidecar first, macOS and Linux deferred)**
* Imports outside the selected set (prod files only; test files were not fetched): 8 direct modules; closure to depth 2 reached 57 modules / 233,597 bytes; closure **UNKNOWN beyond depth 2 / 160-module cap**.

| module outside the set (direct import from prod files) | B | importers in set |
|---|---:|---:|
| `src/main/forked-child-entry-path.ts` | 1889 | 1 |
| `src/main/macos-tcc-reset.ts` | 1489 | 1 |
| `src/shared/clipboard-text.ts` | 5201 | 1 |
| `src/shared/computer-use-key-spec.ts` | 1733 | 1 |
| `src/shared/computer-use-permissions-types.ts` | 856 | 2 |
| `src/shared/own-retained-string.ts` | 1567 | 1 |
| `src/shared/runtime-types.ts` | 6138 | 8 |
| `src/shared/string-utils.ts` | 157 | 1 |

* External packages (versions declared at the pin; licenses from npm registry JSON, read-only):

| package | declared at pin | license (npm registry JSON) | seen in |
|---|---|---|---|
| `@orca/process-host` | workspace:* (dependencies) | ? (latest ?) | in-set |

* Coupling flags (grep of prod files in the set): `child_process`: 5 file(s); `net-or-fetch`: 4 file(s); `node:child_process`: 5 file(s); `node:fs`: 5 file(s); `node:net`: 4 file(s); `node:os`: 3 file(s); `process.platform`: 7 file(s).
* License / NOTICE: MIT: keep the `LICENSE` text and the copyright line (Lovecast Inc.) in `third_party/orca/LICENSE`; add `// Derived from stablyai/orca@e310a63 (MIT)` and a PROVENANCE row per copied file. No NOTICE file exists upstream (none in the 40,641-entry tree). Brand: do not ship Orca names or logos; rename identifiers (`orca`, `Orca`, `OrcaComputerUse*`) in the port. The listing shows no separate licence files under `native/computer-use-*`; the contents of `main.swift`, `runtime.ps1` and `runtime.py` were not read, so embedded third-party snippets are **UNKNOWN beyond sample**.
* Risks: (1) The highest-risk capability in the product: synthetic mouse and keyboard, whole-desktop screenshots, clipboard paste. (2) `runtime.ps1` is executed by PowerShell: execution-policy handling (`windows-powershell-execution-policy.ts`) must not weaken machine policy; pin the script by SHA-256 and run it from a Zain-owned read-only location. (3) The macOS permission model (`macos-computer-use-permission*.ts`, TCC) and `TrustedOrcaApplication.swift` embed the Orca signing identity: re-key to Zain. (4) Sidecar IPC over a Unix socket or named pipe: `UnixSocketPathSafety.swift` and `AuthenticatedConnectionHangupMonitor.swift` show the threat model; replicate it on Windows named pipes with an ACL. (5) Screenshots expose secrets to the model: a redaction hook is required.
* Qualification tests: Positive: carry the vitest suites in `src/main/computer` (26 test files), `runtime-render.test.ps1` (9,226 B), `runtime_keyboard_test.py`, and the Swift tests (macOS CI only). Negative (new): input injection while Core returns deny never reaches the sidecar; a second local process connecting to the sidecar pipe or socket without the session secret is dropped; a paste over the size limit or containing control characters is refused (`computer-clipboard-paste-validation`); the sidecar dies with its parent (no orphan); a modified `runtime.ps1` (hash mismatch) is refused at launch.

<details><summary>File list with blob sizes</summary>

| path @ e310a63 | B | blob | k |
|---|---:|---|---|
| `native/computer-use-linux/runtime.py` | 44350 | 26b9ba43 | P |
| `native/computer-use-linux/runtime_keyboard_test.py` | 2457 | 22e6eef3 | T |
| `native/computer-use-linux/runtime_render_test.py` | 17532 | dfdc2e81 | T |
| `native/computer-use-linux/set_value_test.py` | 1346 | 05059585 | T |
| `native/computer-use-macos/Package.swift` | 949 | 9e7da767 | P |
| `native/computer-use-macos/Sources/OrcaComputerUseMacOS/main.swift` | 171152 | 9b7149a7 | P |
| `native/computer-use-macos/Sources/OrcaComputerUseMacOSCore/ActionArgumentValidation.swift` | 2238 | 86d03999 | P |
| `native/computer-use-macos/Sources/OrcaComputerUseMacOSCore/AgentConnectionRequestLoop.swift` | 664 | b5eeab03 | P |
| `native/computer-use-macos/Sources/OrcaComputerUseMacOSCore/AgentSessionOwnership.swift` | 1543 | d39543e9 | P |
| `native/computer-use-macos/Sources/OrcaComputerUseMacOSCore/AttributeValueCoercion.swift` | 5958 | 974e6b99 | P |
| `native/computer-use-macos/Sources/OrcaComputerUseMacOSCore/AuthenticatedConnectionHangupMonitor.swift` | 5384 | 55e4ec91 | P |
| `native/computer-use-macos/Sources/OrcaComputerUseMacOSCore/ComputerSnapshotCachePolicy.swift` | 473 | a8a45b78 | P |
| `native/computer-use-macos/Sources/OrcaComputerUseMacOSCore/KeyboardInputSafety.swift` | 454 | d739ce43 | P |
| `native/computer-use-macos/Sources/OrcaComputerUseMacOSCore/NumericArgumentParsing.swift` | 279 | b41b4c98 | P |
| `native/computer-use-macos/Sources/OrcaComputerUseMacOSCore/PermissionStatusSnapshot.swift` | 3398 | a1e71ede | P |
| `native/computer-use-macos/Sources/OrcaComputerUseMacOSCore/PermissionTrustSettling.swift` | 1426 | 0f7d0bd8 | P |
| `native/computer-use-macos/Sources/OrcaComputerUseMacOSCore/SnapshotRendering.swift` | 11138 | 615c988a | P |
| `native/computer-use-macos/Sources/OrcaComputerUseMacOSCore/SyntheticMouseClickDelivery.swift` | 3907 | 0c4929bc | P |
| `native/computer-use-macos/Sources/OrcaComputerUseMacOSCore/TrustedOrcaApplication.swift` | 576 | 7fb9dc71 | P |
| `native/computer-use-macos/Sources/OrcaComputerUseMacOSCore/UnixSocketPathSafety.swift` | 398 | 49644edc | P |
| `native/computer-use-macos/Tests/OrcaComputerUseMacOSTests/ActionArgumentValidationTests.swift` | 3480 | e3a79361 | T |
| `native/computer-use-macos/Tests/OrcaComputerUseMacOSTests/AgentConnectionRequestLoopTests.swift` | 1677 | 2218581b | T |
| `native/computer-use-macos/Tests/OrcaComputerUseMacOSTests/AgentSessionOwnershipTests.swift` | 4070 | 8094501c | T |
| `native/computer-use-macos/Tests/OrcaComputerUseMacOSTests/AttributeValueCoercionTests.swift` | 5481 | 9ea18666 | T |
| `native/computer-use-macos/Tests/OrcaComputerUseMacOSTests/AuthenticatedConnectionHangupMonitorTests.swift` | 5790 | 1d335e98 | T |
| `native/computer-use-macos/Tests/OrcaComputerUseMacOSTests/ComputerSnapshotCachePolicyTests.swift` | 1005 | fa5619f6 | T |
| `native/computer-use-macos/Tests/OrcaComputerUseMacOSTests/KeyboardInputSafetyTests.swift` | 966 | 425c8453 | T |
| `native/computer-use-macos/Tests/OrcaComputerUseMacOSTests/NumericArgumentParsingTests.swift` | 1562 | 2471ecdf | T |
| `native/computer-use-macos/Tests/OrcaComputerUseMacOSTests/PermissionStatusSnapshotTests.swift` | 4200 | 7aff74ee | T |
| `native/computer-use-macos/Tests/OrcaComputerUseMacOSTests/PermissionTrustSettlingTests.swift` | 1747 | c3f3956a | T |
| `native/computer-use-macos/Tests/OrcaComputerUseMacOSTests/SnapshotRenderingTests.swift` | 9291 | 4ecf99d0 | T |
| `native/computer-use-macos/Tests/OrcaComputerUseMacOSTests/SyntheticMouseClickDeliveryTests.swift` | 11573 | 6da20afc | T |
| `native/computer-use-macos/Tests/OrcaComputerUseMacOSTests/TrustedOrcaApplicationTests.swift` | 1080 | 21a9a98a | T |
| `native/computer-use-macos/Tests/OrcaComputerUseMacOSTests/UnixSocketPathSafetyTests.swift` | 1429 | cbbf4a44 | T |
| `native/computer-use-windows/runtime-render.test.ps1` | 9226 | 6168d4da | T |
| `native/computer-use-windows/runtime.ps1` | 54996 | bc3b0c7f | P |
| `src/main/computer/computer-action-verification-normalization.test.ts` | 1041 | 11b25d63 | T |
| `src/main/computer/computer-action-verification-normalization.ts` | 746 | a1a510a5 | P |
| `src/main/computer/computer-clipboard-paste-validation.ts` | 1379 | bf9bc820 | P |
| `src/main/computer/computer-provider-action-validation.ts` | 8381 | 0fd430cd | P |
| `src/main/computer/computer-provider-lifecycle.test.ts` | 2761 | 9ee5fbf7 | T |
| `src/main/computer/computer-provider-lifecycle.ts` | 2232 | df192c34 | P |
| `src/main/computer/computer-provider-unavailable-message.ts` | 820 | 9c25cee8 | P |
| `src/main/computer/computer-sidecar-diagnostics.ts` | 890 | b2971dcf | P |
| `src/main/computer/computer-sidecar-paste-validation.ts` | 481 | 4131fc4f | P |
| `src/main/computer/computer-sidecar.ts` | 3515 | 7a8d28e7 | P |
| `src/main/computer/desktop-script-action.ts` | 7238 | fff67758 | P |
| `src/main/computer/desktop-script-provider-action-errors.test.ts` | 10061 | 28c665cb | T |
| `src/main/computer/desktop-script-provider-actions.test.ts` | 7986 | 0cce9da1 | T |
| `src/main/computer/desktop-script-provider-bridge.ts` | 8331 | da0822fd | P |
| `src/main/computer/desktop-script-provider-cache-lifecycle.test.ts` | 3409 | 7c2f171a | T |
| `src/main/computer/desktop-script-provider-cache.test.ts` | 9065 | 91c2dde5 | T |
| `src/main/computer/desktop-script-provider-client.test.ts` | 5443 | 2bdefe57 | T |
| `src/main/computer/desktop-script-provider-client.ts` | 10735 | 21fc9056 | P |
| `src/main/computer/desktop-script-provider-errors.test.ts` | 5177 | c0344952 | T |
| `src/main/computer/desktop-script-provider-params.ts` | 740 | 60787f0d | P |
| `src/main/computer/desktop-script-provider-paths.ts` | 1460 | dad4e930 | P |
| `src/main/computer/desktop-script-provider-runtime-host-routing.test.ts` | 5638 | dd2554e1 | T |
| `src/main/computer/desktop-script-provider-test-harness.ts` | 5053 | af46e702 | T |
| `src/main/computer/desktop-script-provider-types.ts` | 3231 | 6e474fdc | P |
| `src/main/computer/desktop-script-request-queue.ts` | 1723 | ff38f079 | P |
| `src/main/computer/desktop-script-runtime-availability.ts` | 3897 | 246ee770 | P |
| `src/main/computer/desktop-script-runtime-host.test.ts` | 28546 | 1523ffb7 | T |
| `src/main/computer/desktop-script-runtime-host.ts` | 10778 | 7f4a49cc | P |
| `src/main/computer/desktop-script-runtime-host.win32.test.ts` | 3771 | 4fdc2f23 | T |
| `src/main/computer/desktop-script-serve-channel.test.ts` | 6787 | b654012a | T |
| `src/main/computer/desktop-script-serve-channel.ts` | 4657 | 53eb8d90 | P |
| `src/main/computer/desktop-script-snapshot-cache.ts` | 6907 | 61605e95 | P |
| `src/main/computer/desktop-script-snapshot-rendering.ts` | 5671 | 9053f423 | P |
| `src/main/computer/desktop-script-snapshot-store.ts` | 2947 | 447c978d | P |
| `src/main/computer/macos-computer-use-permission-status-cleanup.integration.test.ts` | 2974 | 4a78022c | T |
| `src/main/computer/macos-computer-use-permission-status-cleanup.ts` | 569 | 60863dd5 | P |
| `src/main/computer/macos-computer-use-permission-status.test.ts` | 13002 | 42d6ce65 | T |
| `src/main/computer/macos-computer-use-permission-status.ts` | 6034 | 711c38bb | P |
| `src/main/computer/macos-computer-use-permissions.test.ts` | 10548 | c460208e | T |
| `src/main/computer/macos-computer-use-permissions.ts` | 5020 | fda6da19 | P |
| `src/main/computer/macos-native-provider-availability.ts` | 347 | e44acb0d | P |
| `src/main/computer/macos-native-provider-client.test.ts` | 26840 | 1159da3d | T |
| `src/main/computer/macos-native-provider-client.ts` | 10777 | 767376bd | P |
| `src/main/computer/macos-native-provider-contract.ts` | 1956 | 76a03943 | P |
| `src/main/computer/macos-native-provider-line-buffer.test.ts` | 3495 | cbed9c19 | T |
| `src/main/computer/macos-native-provider-paste-validation.test.ts` | 4449 | 68fa16f9 | T |
| `src/main/computer/macos-native-provider-paths.ts` | 1038 | bf0e9f3f | P |
| `src/main/computer/macos-native-provider-process-reaping.test.ts` | 1579 | 7288795c | T |
| `src/main/computer/macos-native-provider-process-reaping.ts` | 1969 | e0e28d19 | P |
| `src/main/computer/macos-native-provider-reaping.integration.test.ts` | 1647 | 2ba3fe2c | T |
| `src/main/computer/macos-native-provider-socket.test.ts` | 1921 | bd6f4d2f | T |
| `src/main/computer/macos-native-provider-socket.ts` | 2423 | a08b01f0 | P |
| `src/main/computer/macos-native-provider-startup-cleanup.test.ts` | 3013 | 272a9287 | T |
| `src/main/computer/macos-native-provider-transport.ts` | 5793 | a704a302 | P |
| `src/main/computer/runtime-client-error.ts` | 203 | f0773c6c | P |
| `src/main/computer/sidecar-client.test.ts` | 13028 | f6b01e82 | T |
| `src/main/computer/sidecar-client.ts` | 9908 | 98ba74d6 | P |
| `src/main/computer/sidecar-provider-reaping.integration.test.ts` | 4411 | 0b559808 | T |
| `src/main/computer/windows-powershell-execution-policy.test.ts` | 3696 | e92d8971 | T |
| `src/main/computer/windows-powershell-execution-policy.ts` | 1128 | e363b8cf | P |

</details>

---

<!-- SECTION:D7 -->
## D7. Diff comments (Orca `components/diff-comments`, Monaco view zones)

Monaco-based inline comment UI for diffs: view zones, draft card, popover, range drag, add-note button overlay and decorator hooks, plus the small `diff-comments-format` helpers. Matrix row D7 (INTEGRATE Monaco + PORT diff comments). R03D section 14 row 5: 2,624 LOC in 16 files, E/S/O = 0/2/2.

* Upstream: `stablyai/orca@e310a63624c86c0e91e9d77df71f038b91d79ea0`, MIT, Copyright (c) 2026 Lovecast Inc.; selected set = **31 files, 170,630 bytes** (13 test/fixture).
* Zain destination: `apps/web/src/components/diff-comments/` (T3-derived web app) with a thin adapter to the Zain review-comment store (R14 findings model). Formatting helpers: `packages/shared/src/diffCommentsFormat.ts`.
* Copy mode: **PORT-ADAPT (rebind the store-coupled modules; Monaco is DEPEND-ON-PACKAGE, see D7b)**
* Imports outside the selected set (prod files only; test files were not fetched): 15 direct modules; closure to depth 2 reached 489 modules / 2,576,185 bytes; closure **UNKNOWN beyond depth 2 / 160-module cap**.

| module outside the set (direct import from prod files) | B | importers in set |
|---|---:|---:|
| `src/renderer/src/components/editor/NotesSendMenu.tsx` | 11512 | 1 |
| `src/renderer/src/components/editor/editor-shortcuts.ts` | 4254 | 3 |
| `src/renderer/src/components/ui/button.tsx` | 2994 | 3 |
| `src/renderer/src/components/ui/tooltip.tsx` | 2917 | 1 |
| `src/renderer/src/hooks/useMountedRef.ts` | 302 | 3 |
| `src/renderer/src/i18n/i18n.ts` | 7403 | 4 |
| `src/renderer/src/lib/comment-body-line-count.ts` | 598 | 1 |
| `src/renderer/src/lib/comment-body-submit-state.ts` | 1520 | 2 |
| `src/renderer/src/lib/diff-comment-compat.ts` | 950 | 2 |
| `src/renderer/src/lib/ime-text-field.tsx` | 1421 | 3 |
| `src/renderer/src/lib/markdown-review-notes-setting.ts` | 812 | 1 |
| `src/renderer/src/store/index.ts` | 10440 | 2 |
| `src/renderer/src/store/slices/diffComments.ts` | 8813 | 1 |
| `src/renderer/src/store/worktree-diff-comments-selector.ts` | 8983 | 1 |
| `src/shared/diff-comment-types.ts` | 1289 | 3 |

* External packages (versions declared at the pin; licenses from npm registry JSON, read-only):

| package | declared at pin | license (npm registry JSON) | seen in |
|---|---|---|---|
| `class-variance-authority` | ^0.7.1 (devDependencies) | Apache-2.0 (latest 0.7.1) | closure only |
| `clsx` | ^2.1.1 (devDependencies) | MIT (latest 2.1.1) | closure only |
| `i18next` | ^26.4.2 (dependencies) | MIT (latest 26.5.11) | closure only |
| `lucide-react` | ^0.577.0 (devDependencies) | ISC (latest 1.62.0) | in-set |
| `monaco-editor` | ^0.55.1 (devDependencies) | MIT (latest 0.57.0) | in-set |
| `radix-ui` | ^1.6.7 (devDependencies) | MIT (latest 1.8.1) | closure only |
| `react` | ~19.2.8 (devDependencies) | MIT (latest 19.3.1) | in-set |
| `react-dom` | ~19.2.8 (devDependencies) | MIT (latest 19.3.1) | in-set |
| `react-i18next` | 17.0.15 (dependencies) | MIT (latest 17.1.9) | closure only |
| `sonner` | 2.0.7 (devDependencies) | MIT (latest 2.0.8) | in-set |
| `tailwind-merge` | ^3.7.0 (devDependencies) | MIT (latest 3.7.0) | closure only |
| `zustand` | ^5.0.15 (devDependencies) | MIT (latest 5.0.16) | closure only |

* Coupling flags (grep of prod files in the set): none detected.
* License / NOTICE: MIT: keep the `LICENSE` text and the copyright line (Lovecast Inc.) in `third_party/orca/LICENSE`; add `// Derived from stablyai/orca@e310a63 (MIT)` and a PROVENANCE row per copied file. No NOTICE file exists upstream (none in the 40,641-entry tree). Brand: do not ship Orca names or logos; rename identifiers (`orca`, `Orca`, `OrcaComputerUse*`) in the port.
* Risks: (1) Requires Monaco (pinned in D7b); T3 itself uses `@pierre/diffs` and has its own annotations (R02 section 12), so two diff surfaces may coexist: decide which one hosts comments. (2) The set imports the Orca renderer store in a few places (see outside-set table): replace with props or an adapter. (3) `DiffCommentCard.tsx` renders user text: sanitise it. (4) It relies on Monaco internals (view zones, decorations) that changed across versions; Monaco is now 0.57.0.
* Qualification tests: Positive: carry the 12 test files in the directory (for example `diff-comment-range-drag.test.ts` 15,543 B, `useDiffCommentDecorator.range-selection.test.tsx` 14,442 B). Negative (new): a comment anchored to a line deleted by a later diff shows as outdated and not on the wrong line; a 50,000-line file does not freeze the editor; script tags in comment text render inert; keyboard-only add and cancel work (editor a11y); drag selecting across hunks produces a valid line range or none.

<details><summary>File list with blob sizes</summary>

| path @ e310a63 | B | blob | k |
|---|---:|---|---|
| `src/renderer/src/components/diff-comments/DiffCommentCard.resize.test.tsx` | 4820 | 648b3335 | T |
| `src/renderer/src/components/diff-comments/DiffCommentCard.tsx` | 10923 | f880471f | P |
| `src/renderer/src/components/diff-comments/DiffCommentDraftCard.test.tsx` | 9229 | 636d8297 | T |
| `src/renderer/src/components/diff-comments/DiffCommentDraftCard.tsx` | 8155 | a4b1fe2f | P |
| `src/renderer/src/components/diff-comments/DiffCommentPopover.tsx` | 8298 | b5c16185 | P |
| `src/renderer/src/components/diff-comments/decorated-diff-comment.ts` | 255 | c561d10a | P |
| `src/renderer/src/components/diff-comments/diff-comment-add-button-overlay.ts` | 5541 | 7e305943 | P |
| `src/renderer/src/components/diff-comments/diff-comment-add-note-shortcut.ts` | 2254 | 3689d89f | P |
| `src/renderer/src/components/diff-comments/diff-comment-draft-zone.test.tsx` | 10381 | 3ecac725 | T |
| `src/renderer/src/components/diff-comments/diff-comment-draft-zone.ts` | 10577 | c9f3bd6b | P |
| `src/renderer/src/components/diff-comments/diff-comment-drag-auto-scroll.test.ts` | 710 | 101dbaab | T |
| `src/renderer/src/components/diff-comments/diff-comment-drag-auto-scroll.ts` | 1136 | 3233513b | P |
| `src/renderer/src/components/diff-comments/diff-comment-editor-test-fixture.ts` | 6211 | e6655785 | T |
| `src/renderer/src/components/diff-comments/diff-comment-line-range.test.ts` | 1688 | 312a52f9 | T |
| `src/renderer/src/components/diff-comments/diff-comment-line-range.ts` | 2776 | 3d2b6a27 | P |
| `src/renderer/src/components/diff-comments/diff-comment-popover-outside-click.test.tsx` | 3494 | d661fe3c | T |
| `src/renderer/src/components/diff-comments/diff-comment-popover-position.test.ts` | 983 | e995cd86 | T |
| `src/renderer/src/components/diff-comments/diff-comment-popover-position.ts` | 2542 | 07217bdf | P |
| `src/renderer/src/components/diff-comments/diff-comment-range-drag.test.ts` | 15543 | 6386fb17 | T |
| `src/renderer/src/components/diff-comments/diff-comment-range-drag.ts` | 11264 | eced04d8 | P |
| `src/renderer/src/components/diff-comments/diff-comment-view-zone-entry.ts` | 2249 | b4f9072d | P |
| `src/renderer/src/components/diff-comments/diff-comment-zone-card.tsx` | 5448 | 5eb6d312 | P |
| `src/renderer/src/components/diff-comments/diff-comment-zone-mouse-events.test.ts` | 742 | 4cbbcf5d | T |
| `src/renderer/src/components/diff-comments/diff-comment-zone-mouse-events.ts` | 315 | 2926fb97 | P |
| `src/renderer/src/components/diff-comments/use-visible-worktree-diff-comments.test.ts` | 1883 | a602932b | T |
| `src/renderer/src/components/diff-comments/use-visible-worktree-diff-comments.ts` | 1038 | 0c5a08ef | P |
| `src/renderer/src/components/diff-comments/useDiffCommentDecorator.lifecycle.test.tsx` | 11577 | 43584985 | T |
| `src/renderer/src/components/diff-comments/useDiffCommentDecorator.range-selection.test.tsx` | 14442 | a890fde8 | T |
| `src/renderer/src/components/diff-comments/useDiffCommentDecorator.tsx` | 14991 | 70b772f3 | P |
| `src/renderer/src/lib/diff-comments-format.ts` | 93 | 8b8931f2 | P |
| `src/shared/diff-comments-format.ts` | 1072 | 0d545462 | P |

</details>

---

<!-- SECTION:D7b -->
## D7b. Monaco editor (`microsoft/monaco-editor`)

Browser code editor and diff editor used for the file editor and for diff comments (D7). Matrix row D7. Consumed from npm; the repo is listed for the audit surface (languages, the alpha LSP client, third-party notices).

* Upstream: `microsoft/monaco-editor@dbf1945df2ff7e46512d2f548cc5c0977a3eadd8`.
* Zain destination: `apps/web/package.json` dependency `monaco-editor` pinned exactly; a Zain wrapper in `apps/web/src/components/editor/`; optional `@vscode/monaco-lsp-client` for LSP (R13 F7).
* Copy mode: **DEPEND-ON-PACKAGE (npm `monaco-editor` 0.57.0, published 2026-09-24, MIT)**
* Selected surface: **41 files, 484,889 bytes** (the `monaco-lsp-client` package plus manifests and notices). Aggregated repo view:

| path (aggregated) | files | bytes |
|---|---:|---:|
| `.azure-pipelines` | 2 | 7,173 |
| `.devcontainer` | 1 | 155 |
| `.gitattributes` | 1 | 12 |
| `.gitignore` | 1 | 158 |
| `.husky` | 1 | 41 |
| `.mocharc.json` | 1 | 33 |
| `.nvmrc` | 1 | 8 |
| `.prettierignore` | 1 | 542 |
| `.prettierrc` | 1 | 130 |
| `.vscode` | 3 | 3,263 |
| `CHANGELOG.md` | 1 | 114,106 |
| `CONTRIBUTING.md` | 1 | 4,089 |
| `LICENSE.txt` | 1 | 1,098 |
| `MAINTAINING.md` | 1 | 4,676 |
| `README.md` | 1 | 7,730 |
| `SECURITY.md` | 1 | 543 |
| `ThirdPartyNotices.txt` | 1 | 60,394 |
| `build` | 36 | 141,602 |
| `docs` | 6 | 531,425 |
| `editor.code-workspace` | 1 | 112 |
| `gulpfile.js` | 1 | 295 |
| `monaco-lsp-client` | 36 | 417,136 |
| `package-lock.json` | 1 | 586,243 |
| `package.json` | 1 | 4,027 |
| `samples` | 97 | 752,804 |
| `scripts` | 4 | 12,246 |
| `src` | 432 | 15,989,800 |
| `test` | 48 | 1,439,756 |
| `test-results` | 1 | 45 |
| `webpack-plugin` | 11 | 145,889 |
| `website` | 291 | 855,147 |

* Internal imports outside the selected set: `src/` (432 files, 15,989,800 B) holds the language definitions and build entry points that produce the npm package; the editor core is the separate `monaco-editor-core` package (devDependency `0.57.0-rc.2` at the pin, while the published `monaco-editor` 0.57.0 lists only `marked 14.0.0` and `dompurify 3.4.15` as dependencies). `@vscode/monaco-lsp-client` 0.1.0 is a local file dependency (alpha; 22 language features per R13 F7).
* External dependencies of the published package and of the LSP client:

| package | declared | from | latest on npm | license |
|---|---|---|---|---|
| @hediet/json-rpc | ^0.5.0 | monaco-lsp-client | 0.5.0 | MIT |
| @hediet/json-rpc-browser | ^0.5.1 | monaco-lsp-client | 0.5.1 | MIT |
| @hediet/json-rpc-websocket | ^0.5.1 | monaco-lsp-client | 0.5.1 | MIT |
| dompurify | 3.4.15 | monaco-editor | 3.4.17 | (MPL-2.0 OR Apache-2.0) |
| marked | 14.0.0 | monaco-editor | 18.1.2 | MIT |
| monaco-editor-core | * | lsp peer | 0.57.0 | MIT |

* License and NOTICE: MIT (`LICENSE.txt` 1,098 B, Copyright (c) Microsoft Corporation). `ThirdPartyNotices.txt` (60,394 B) lists embedded third-party components (language grammars and others): it must be shipped with any distribution that bundles Monaco. Sub-components with their own LICENSE: `webpack-plugin/LICENSE` (1,162 B) and `build/esm/rollup-plugin-keep-css-imports/LICENSE` (1,072 B). No NOTICE.
* Risks: (1) Bundle weight (megabytes) and web-worker setup under an Electron CSP. (2) `@monaco-editor/react` 4.7.0 (2025-02-13) is stale; prefer direct integration. (3) Monaco ships no debugger and no stable LSP (the LSP client is alpha 0.1.0); R13 covers alternatives. (4) Frequent minor releases change the view-zone and decoration APIs used by D7. (5) Accessibility: screen-reader mode must be verified.
* Qualification tests: Positive: open, edit and save a 1 MB file; the diff editor renders a two-version fixture; D7 comment zones attach at the right lines. Negative: a 50 MB file opens in read-only degraded mode without freezing; pasting 5 MB on one line does not hang; the web worker URLs resolve under the packaged CSP with no network fetch; an unsupported language falls back to plain text; keyboard-only navigation and screen-reader mode pass the a11y checklist.

<details><summary>File list with blob sizes (monaco-lsp-client, manifests, notices)</summary>

| path | B | blob | k |
|---|---:|---|---|
| `LICENSE.txt` | 1098 | 76fdc58a | P |
| `ThirdPartyNotices.txt` | 60394 | d188d7a5 | P |
| `build/esm/rollup-plugin-keep-css-imports/LICENSE` | 1072 | 0bbbe67d | P |
| `monaco-lsp-client/README.md` | 154 | 8e6f3433 | P |
| `monaco-lsp-client/generator/index.ts` | 17108 | df3b100c | P |
| `monaco-lsp-client/package-lock.json` | 51877 | 3373c96c | P |
| `monaco-lsp-client/package.json` | 652 | 297e117a | P |
| `monaco-lsp-client/rolldown.config.mjs` | 620 | e6336a2b | P |
| `monaco-lsp-client/src/adapters/ITextModelBridge.ts` | 1023 | 2193bb85 | P |
| `monaco-lsp-client/src/adapters/LspCapabilitiesRegistry.ts` | 11489 | 0f87f574 | P |
| `monaco-lsp-client/src/adapters/LspClient.ts` | 4860 | 1c5d7321 | P |
| `monaco-lsp-client/src/adapters/LspConnection.ts` | 495 | b9f619a2 | P |
| `monaco-lsp-client/src/adapters/TextDocumentSynchronizer.ts` | 6166 | c2b3620c | P |
| `monaco-lsp-client/src/adapters/languageFeatures/LspCodeActionFeature.ts` | 6663 | aed4e0dd | P |
| `monaco-lsp-client/src/adapters/languageFeatures/LspCodeLensFeature.ts` | 3054 | f11fdf71 | P |
| `monaco-lsp-client/src/adapters/languageFeatures/LspCompletionFeature.ts` | 7745 | e5a9f7f2 | P |
| `monaco-lsp-client/src/adapters/languageFeatures/LspDeclarationFeature.ts` | 2096 | ab306047 | P |
| `monaco-lsp-client/src/adapters/languageFeatures/LspDefinitionFeature.ts` | 2085 | bf87f896 | P |
| `monaco-lsp-client/src/adapters/languageFeatures/LspDiagnosticsFeature.ts` | 6175 | 40e8cad9 | P |
| `monaco-lsp-client/src/adapters/languageFeatures/LspDocumentHighlightFeature.ts` | 2161 | b07aad78 | P |
| `monaco-lsp-client/src/adapters/languageFeatures/LspDocumentLinkFeature.ts` | 2326 | 8825b10f | P |
| `monaco-lsp-client/src/adapters/languageFeatures/LspDocumentSymbolFeature.ts` | 4086 | 4f3b4a35 | P |
| `monaco-lsp-client/src/adapters/languageFeatures/LspFoldingRangeFeature.ts` | 2317 | 36218023 | P |
| `monaco-lsp-client/src/adapters/languageFeatures/LspFormattingFeature.ts` | 2166 | 6a3bdc69 | P |
| `monaco-lsp-client/src/adapters/languageFeatures/LspHoverFeature.ts` | 2759 | b77c4fdd | P |
| `monaco-lsp-client/src/adapters/languageFeatures/LspImplementationFeature.ts` | 2129 | 9dd2d06e | P |
| `monaco-lsp-client/src/adapters/languageFeatures/LspInlayHintsFeature.ts` | 7343 | d8f594f7 | P |
| `monaco-lsp-client/src/adapters/languageFeatures/LspOnTypeFormattingFeature.ts` | 2516 | 77b50223 | P |
| `monaco-lsp-client/src/adapters/languageFeatures/LspRangeFormattingFeature.ts` | 2318 | 5cc79ec5 | P |
| `monaco-lsp-client/src/adapters/languageFeatures/LspReferencesFeature.ts` | 2208 | 2beab9b7 | P |
| `monaco-lsp-client/src/adapters/languageFeatures/LspRenameFeature.ts` | 4763 | 008abf20 | P |
| `monaco-lsp-client/src/adapters/languageFeatures/LspSelectionRangeFeature.ts` | 2478 | d7f0f73d | P |
| `monaco-lsp-client/src/adapters/languageFeatures/LspSemanticTokensFeature.ts` | 5181 | f57ccc13 | P |
| `monaco-lsp-client/src/adapters/languageFeatures/LspSignatureHelpFeature.ts` | 3842 | ea4f222c | P |
| `monaco-lsp-client/src/adapters/languageFeatures/LspTypeDefinitionFeature.ts` | 2129 | 8736647f | P |
| `monaco-lsp-client/src/adapters/languageFeatures/common.ts` | 18919 | 4d648e7d | P |
| `monaco-lsp-client/src/index.ts` | 313 | ade3e55f | P |
| `monaco-lsp-client/src/types.ts` | 223111 | c007b2fb | P |
| `monaco-lsp-client/src/utils.ts` | 1809 | 00905499 | P |
| `package.json` | 4027 | 280c9fe0 | P |
| `webpack-plugin/LICENSE` | 1162 | 21071075 | P |

</details>


---

<!-- SECTION:D9 -->
## D9. openai/codex sandbox, exec policy, network proxy (`openai/codex@603a7ba`, Apache-2.0)

**Decision in 06:** ADAPT into Core (Job-Object floor in P3, full sandbox Phase 8). The headline finding of this manifest is that the nine-crate set is not closed, and one crate (bwrap) compiles an LGPL C tree.

### D9.0 What the nine crates need that is not in the set

Source: each crate Cargo.toml at the pin, plus a scan of all 323 `.rs` blobs in the nine crates for `codex_*` identifiers (identifiers such as `codex_home` or `codex_wfp_*` that are strings or env names, not crates, were discarded).

| Out-of-set internal crate | Files / bytes at pin | Needed by | Verdict |
|---|---|---|---|
| `codex-protocol` (`codex-rs/protocol`) | 89 / 1,245,752 | sandboxing, linux-sandbox, windows-sandbox-rs, mxc-sandbox | Do NOT vendor. Its own deps (`protocol/Cargo.toml`): `codex-async-utils, codex-execpolicy, codex-extension-items, codex-http-client, codex-network-proxy, codex-utils-absolute-path, codex-utils-image, codex-utils-path-uri, codex-utils-redacted-string, codex-utils-string`. Zain defines its own permission-profile contract in `crates/contracts` and patches the vendored crates to use it (the PORT-ADAPT seam). Which `codex_protocol::` symbols are used was not enumerated: **UNKNOWN beyond sample**. |
| `codex-utils-absolute-path` | 6 / 35,463 | all but process-hardening | Vendor as-is (leaf crate). |
| `codex-utils-path-uri` | 12 / 148,662 | sandboxing, mxc-sandbox, network-proxy, protocol | Vendor as-is (depends only on absolute-path). |
| `codex-utils-pty` | 40 / 357,786 | sandboxing, windows-sandbox-rs | Vendor (ConPTY logic is Windows-critical); dev-dep `codex-utils-cargo-bin` (6 / 12,141). |
| `codex-uds` | 8 / 41,308 | sandboxing, linux-sandbox | Vendor as-is (no codex deps). |
| `codex-utils-home-dir` | 3 / 5,571 | sandboxing (win), network-proxy, install-context | Vendor or replace with a Zain home resolver. |
| `codex-utils-string`, `codex-utils-process`, `codex-utils-rustls-provider` | 6 / 20,859; 4 / 3,641; 5 / 3,261 | windows-sandbox-rs; windows-sandbox-rs; network-proxy | Vendor as-is (leaf). |
| `codex-install-context` | 5 / 34,342 | linux-sandbox | Replace with a Zain shim (Linux only, deferred). |
| `codex-otel` | 48 / 389,296 | sandboxing (win), windows-sandbox-rs, network-proxy | Replace with a `tracing` facade. Its own deps include `codex-api`, `codex-http-client`, `codex-protocol`, so vendoring drags the API client. |
| `codex-http-client` | 54 / 472,430 | windows-sandbox-rs, otel, protocol | Replace; what the Windows sandbox fetches through it is **UNKNOWN beyond sample** and a sandbox must not phone home. |
| `codex-core` | 1,060 / 18,623,613 | windows-sandbox-service (prod), linux-sandbox (tests) | Never vendor. This is why `windows-sandbox-service` is REFERENCE-only. |
| `codex-config`, `codex-cloud-config` | 108 / 1,150,959; 16 / 143,037 | windows-sandbox-service | Never vendor. |
| `mxc-sdk` (git `microsoft/mxc` rev `b21120168d70befe12356411423266bfef168446`, MIT per GitHub API) | n/a | mxc-sandbox | External git dependency; mirror into the Zain vendor store before Phase 8. |
| `codex-rs/vendor/bubblewrap` (50 files, C) | see D9.9 | bwrap `build.rs` | **LGPL; do not vendor.** |

External crate versions and licenses (nine `Cargo.toml` + `codex-rs/Cargo.toml [workspace.dependencies]@603a7ba` + crates.io JSON on 2026-10-28; "latest" is the newest crates.io release):

| Crate | Declared at pin | Latest | License | Used by |
|---|---|---|---|---|
| anyhow | 1 | 1.0.104 | MIT OR Apache-2.0 | execpolicy, mxc, network-proxy, sandboxing, windows-sandbox-* |
| aws-credential-types, aws-sigv4 | 1 | 1.3.1, 1.6.3 | Apache-2.0 | network-proxy (SigV4 signing; not needed by Zain, feature-gate out) |
| base64 | 0.22.1 | 0.23.1 | MIT OR Apache-2.0 | network-proxy, windows-sandbox-rs |
| cc, pkg-config | 1, 0.3 | 1.10.0, 0.3.34 | MIT OR Apache-2.0 | bwrap (build) |
| chrono | 0.4.42 / 0.4.43 | 0.4.45 | MIT OR Apache-2.0 | network-proxy, windows-sandbox-rs |
| clap | 4 | 4.6.7 | MIT OR Apache-2.0 | execpolicy, linux-sandbox, network-proxy |
| dirs-next | 2.0 | 2.0.0 | MIT OR Apache-2.0 | windows-sandbox-rs |
| dunce | 1.0.4 | 1.0.5 | CC0-1.0 OR MIT-0 OR Apache-2.0 | sandboxing, windows-sandbox-rs |
| flatbuffers | 25 | 25.12.19 | Apache-2.0 | mxc-sandbox (win) |
| glob | 0.3 | 0.3.4 | MIT OR Apache-2.0 | windows-sandbox-rs |
| globset | 0.4 | 0.4.21 | Unlicense OR MIT | linux-sandbox, network-proxy |
| landlock | 0.4.4 | 0.4.7 | MIT OR Apache-2.0 | linux-sandbox |
| libc | 0.2.182 | 0.2.191 | MIT OR Apache-2.0 | sandboxing, linux-sandbox, bwrap, process-hardening, network-proxy |
| multimap | 0.10.0 | 0.10.1 | MIT OR Apache-2.0 | execpolicy |
| opentelemetry | 0.31.0 | 0.33.1 | Apache-2.0 | network-proxy |
| rama-{core,http,http-backend,net,socks5,tcp,tls-rustls,unix,dns} | `=0.3.0-alpha.4` (exact pre-release) | 0.4.0 | MIT OR Apache-2.0 | network-proxy |
| rand | 0.8 (windows-sandbox-rs) / 0.9 (workspace) | 0.10.3 | MIT OR Apache-2.0 | network-proxy, windows-sandbox-rs |
| rand_regex | 0.18.1 | 0.19.0 | MIT | network-proxy |
| regex, regex-automata, regex-lite, regex-syntax | 1.12.3, 0.4.13, 0.1.8, 0.8.8 | 1.13.1, 0.4.18, 0.1.9, 0.8.11 | MIT OR Apache-2.0 | network-proxy, sandboxing |
| rustix | 1.1.4 (feature `net`) | 1.1.6 | Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT | linux-sandbox |
| rustls-native-certs | 0.8.3 | 0.8.5 | Apache-2.0 OR ISC OR MIT | network-proxy |
| schannel | 0.1 | 0.1.30 | MIT | network-proxy (win) |
| schemars | 0.8.22 | 1.2.3 (major bump) | MIT | network-proxy |
| seccompiler | 0.5.0 | 0.5.0 | Apache-2.0 OR BSD-3-Clause | linux-sandbox |
| security-framework | 3 | 3.7.0 | MIT OR Apache-2.0 | network-proxy (macOS) |
| serde, serde_json, serde_ignored | 1, 1, 0.1.14 | 1.0.229, 1.0.154, 0.1.14 | MIT OR Apache-2.0 | most |
| sha2 | 0.10 | 0.11.1 | MIT OR Apache-2.0 | linux-sandbox, network-proxy |
| shlex | 1.3.0 | 2.0.1 | MIT OR Apache-2.0 | execpolicy |
| starlark | 0.14.2 (`default-features = false`) | 0.14.2 | Apache-2.0 | execpolicy |
| tempfile | 3 / 3.23.0 | 3.27.0 | MIT OR Apache-2.0 | execpolicy, windows-sandbox-rs |
| thiserror | 2.0.17 | 2.0.21 | MIT OR Apache-2.0 | execpolicy, mxc, network-proxy |
| time | 0.3.47 | 0.3.55 | MIT OR Apache-2.0 | network-proxy |
| tokio | 1 | 1.54.1 | MIT | execpolicy, network-proxy, sandboxing, windows-sandbox-* |
| toml | 0.9.5 | 1.1.8 | MIT OR Apache-2.0 | windows-sandbox-service |
| tracelogging | `=1.2.3` | 1.2.4 | MIT | mxc-sandbox (win) |
| tracing, tracing-appender, tracing-subscriber | 0.1.44, 0.2.3, 0.3.22 | 0.1.44, 0.2.5, 0.3.23 | MIT | sandboxing, network-proxy, windows-sandbox-rs |
| url | 2 | 2.5.8 | MIT OR Apache-2.0 | linux-sandbox, network-proxy, sandboxing |
| which | 8 | 8.0.6 | MIT | sandboxing |
| windows | 0.58 | 0.62.2 | MIT OR Apache-2.0 | windows-sandbox-rs, -service |
| windows-sys | 0.61.2 | 0.61.2 | MIT OR Apache-2.0 | windows-sandbox-*, mxc, network-proxy |
| mxc-sdk | git rev b21120168d70 | n/a | MIT (GitHub API for microsoft/mxc) | mxc-sandbox |

Edition 2024 for all workspace members (`codex-rs/Cargo.toml [workspace.package]` has `edition = "2024"`, `license = "Apache-2.0"`). `rust-toolchain.toml` was not read: the minimum Rust version for the Zain toolchain is **UNKNOWN**.

### D9.0a License and NOTICE obligations (all nine crates)

* Apache-2.0 section 4: ship `LICENSE` (10,926 B, `LICENSE@603a7ba`), keep per-file headers, mark modified files. Zain target: `vendor/codex/LICENSE`, `vendor/codex/NOTICE`, `vendor/codex/PROVENANCE.md`.
* `NOTICE@603a7ba` (242 B): "OpenAI Codex, Copyright 2025 OpenAI" and a Ratatui (MIT) credit for TUI-derived code. None of the nine crates is the TUI, but section 4(d) asks to carry applicable NOTICE text, and carrying the 242 B file verbatim is cheaper than arguing: carry it.
* The four Seatbelt policy files (`sandboxing/src/seatbelt_*.sbpl`) say "inspired by Chrome sandbox policy" with Chromium URLs in comments (Chromium is BSD-3-Clause). They are OpenAI-authored derivatives; keep the comment headers untouched. No Chromium file is copied.
* Third-party code embedded in the set: only `vendor/bubblewrap` (LGPL, excluded, D9.9).
* Trademarks: Apache-2.0 section 6 grants no right to OpenAI or Codex marks. Keep crate names on vendored copies (mergeable diffs) but rename every shipped binary (`codex-command-runner`, `codex-windows-sandbox-setup`, `codex-windows-sandbox-service`, `codex-linux-sandbox`, `codex-windows-managed-deny-probe`).


### D9.1 `codex-rs/process-hardening` (crate `codex-process-hardening`): COPY AS-IS

* Files: **4** (0 test/harness), **6,708 bytes**. Pin: `codex-rs/process-hardening/*@603a7ba`.
* Zain destination: `vendor/codex/process-hardening/`
* Verdict: Smallest crate: one source file, only `libc`. Pre-main hardening per its README. Call it first in every Zain helper binary.
* Internal imports outside the selected set: none (`libc` 0.2.182; dev `pretty_assertions`).
* Risks: Effect is Unix-centric; what it does on Windows is **UNKNOWN beyond sample** (source not read in detail). Zain must not assume Windows hardening that does not exist.
* Qualification tests: Unit: after the hardening call the process has core dumps disabled and `LD_*`/`DYLD_*` stripped (Linux/macOS CI). Negative: on Windows the call must not panic and Zain records `hardening=none` rather than claiming protection; `LD_PRELOAD` set before exec must be absent in the child.

<details><summary>File list with blob sizes</summary>

| path (under `codex-rs/`) | B | blob | k |
|---|---:|---|---|
| `process-hardening/BUILD.bazel` | 137 | ca657163 | B |
| `process-hardening/Cargo.toml` | 325 | 60a5729f | B |
| `process-hardening/README.md` | 337 | 66a8060a | P |
| `process-hardening/src/lib.rs` | 5909 | f500e15d | P |

</details>

### D9.2 `codex-rs/execpolicy` (crate `codex-execpolicy`): COPY AS-IS (library) + PORT-ADAPT (glue)

* Files: **17** (2 test/harness), **98,465 bytes**. Pin: `codex-rs/execpolicy/*@603a7ba`.
* Zain destination: `vendor/codex/execpolicy/` (library); Zain rules in `crates/core/src/policy/exec_rules/`
* Verdict: Prefix-based Starlark rules for command allow/prompt/forbid (`Cargo.toml` description). Self-contained except for `codex-utils-absolute-path`. It classifies argv prefixes; Cedar (D11) decides resource and action authorisation. Layering: execpolicy feeds Cedar a `command_class` attribute.
* Internal imports outside the selected set: `codex-utils-absolute-path` only. Note `codex-protocol` depends back on `codex-execpolicy`, so a Zain contract crate can re-export it without a cycle.
* Risks: `starlark 0.14.2` is a sizeable dependency and rule files are code: they must come only from signed Zain policy bundles, never from the agent worktree. `examples/example.codexpolicy` is a template, not a policy.
* Qualification tests: Unit: copy upstream tests; add golden decisions for a forced git push, a recursive delete of the filesystem root, and an encoded PowerShell command. Negative: a rules file with unbounded recursion is rejected within the evaluation budget; a rules file placed in the agent worktree is ignored.

<details><summary>File list with blob sizes</summary>

| path (under `codex-rs/`) | B | blob | k |
|---|---:|---|---|
| `execpolicy/BUILD.bazel` | 123 | 79c73b7a | B |
| `execpolicy/Cargo.toml` | 874 | 42040222 | B |
| `execpolicy/README.md` | 4122 | 557e46fb | P |
| `execpolicy/examples/example.codexpolicy` | 1342 | 4040f612 | P |
| `execpolicy/src/amend.rs` | 11119 | e25fd1bd | P |
| `execpolicy/src/decision.rs` | 791 | 15dc1f71 | P |
| `execpolicy/src/error.rs` | 2916 | 0f2be753 | P |
| `execpolicy/src/execpolicycheck.rs` | 2894 | b72995d0 | P |
| `execpolicy/src/executable_name.rs` | 737 | bb3e8a53 | P |
| `execpolicy/src/lib.rs` | 923 | 293e2750 | P |
| `execpolicy/src/main.rs` | 388 | 82e1bc12 | P |
| `execpolicy/src/parser.rs` | 15280 | 33262db1 | P |
| `execpolicy/src/policy.rs` | 12754 | 78790517 | P |
| `execpolicy/src/rule.rs` | 9131 | 6642cb1d | P |
| `execpolicy/src/sandbox_migration.rs` | 4125 | a2a57c1c | P |
| `execpolicy/src/sandbox_migration_tests.rs` | 2157 | 5bb6af6e | T |
| `execpolicy/tests/basic.rs` | 28789 | f6a86adb | T |

</details>

### D9.3 `codex-rs/sandboxing` (crate `codex-sandboxing`): PORT-ADAPT

* Files: **38** (13 test/harness), **445,533 bytes**. Pin: `codex-rs/sandboxing/*@603a7ba`.
* Zain destination: `vendor/codex/sandboxing/`; the four `.sbpl` files are COPY AS-IS
* Verdict: Sandbox selection and command transformation: Seatbelt (`seatbelt.rs`, 4 `.sbpl` policies, tests), Linux bwrap/landlock invocation, Windows restricted-token and MXC routing. `codex-protocol` coupling (permission-profile types) is the main port cost.
* Internal imports outside the selected set: `codex-protocol`, `codex-uds`, `codex-utils-absolute-path`, `codex-utils-path-uri`, `codex-utils-pty`; Windows only: `codex-otel`, `codex-utils-home-dir`; in-set: `codex-mxc-sandbox`, `codex-network-proxy`, `codex-windows-sandbox`. Test-only identifier hits: `codex_linux_sandbox_exe`, `codex_windows_registered_core`, `codex_utils_cargo_bin`.
* Risks: Adopting it pulls the whole set (it depends on windows-sandbox, mxc-sandbox, network-proxy). `sandbox-exec` is deprecated by Apple (platform risk). `seatbelt_daemon.rs` and `seatbelt_scratch.rs` imply a helper daemon (**UNKNOWN beyond sample**).
* Qualification tests: Unit: carry `seatbelt_tests.rs`, `seatbelt_network_tests.rs`, `seatbelt_tls_tests.rs`, `seatbelt_fcntl_tests.rs` (macOS runner). Negative: under a read-only profile a write to the workspace fails with EPERM; with network off `connect(2)` to 1.1.1.1 fails; symlink and `..` escapes fail.

<details><summary>File list with blob sizes</summary>

| path (under `codex-rs/`) | B | blob | k |
|---|---:|---|---|
| `sandboxing/BUILD.bazel` | 373 | 5cdc37b7 | B |
| `sandboxing/Cargo.toml` | 1222 | 64ebac48 | B |
| `sandboxing/src/bwrap.rs` | 13376 | 5c1fe74f | P |
| `sandboxing/src/bwrap_tests.rs` | 14465 | 2589d395 | T |
| `sandboxing/src/denial.rs` | 2193 | 507bf4de | P |
| `sandboxing/src/landlock.rs` | 4183 | dad16e23 | P |
| `sandboxing/src/landlock_tests.rs` | 2574 | b3a57c3e | T |
| `sandboxing/src/lib.rs` | 4325 | 5db90bba | P |
| `sandboxing/src/linux_pid_namespace.rs` | 800 | b7011311 | P |
| `sandboxing/src/manager.rs` | 33960 | f6c281a0 | P |
| `sandboxing/src/manager_tests.rs` | 30280 | 22dcf916 | T |
| `sandboxing/src/policy_transforms.rs` | 24634 | fed7bd15 | P |
| `sandboxing/src/policy_transforms_tests.rs` | 48664 | 28d5828b | T |
| `sandboxing/src/sandbox_integrity/contents.rs` | 3827 | 219c71e8 | P |
| `sandboxing/src/sandbox_integrity/contents_tests.rs` | 5283 | cd1e2df0 | T |
| `sandboxing/src/sandbox_integrity/finding.rs` | 655 | ea2945b9 | P |
| `sandboxing/src/sandbox_integrity/mod.rs` | 156 | 06346585 | P |
| `sandboxing/src/sandbox_integrity/policy.rs` | 1200 | ebf9c9ad | P |
| `sandboxing/src/seatbelt.rs` | 42646 | 0f8701a1 | P |
| `sandboxing/src/seatbelt_base_policy.sbpl` | 3910 | 2fca6a88 | P |
| `sandboxing/src/seatbelt_daemon.rs` | 1193 | 964144cd | P |
| `sandboxing/src/seatbelt_daemon_socket_tests.rs` | 3014 | 5c316edc | T |
| `sandboxing/src/seatbelt_fcntl_tests.rs` | 9507 | 277bb309 | T |
| `sandboxing/src/seatbelt_network_policy.sbpl` | 1145 | 1bb9eb2b | P |
| `sandboxing/src/seatbelt_network_tests.rs` | 3550 | 6c005cc4 | T |
| `sandboxing/src/seatbelt_preferences_policy.sbpl` | 383 | 45599d1b | P |
| `sandboxing/src/seatbelt_read_only_platform_defaults.sbpl` | 7255 | 0714f2e6 | P |
| `sandboxing/src/seatbelt_scratch.rs` | 2871 | 6fb13192 | P |
| `sandboxing/src/seatbelt_tests.rs` | 119901 | b5034bc2 | T |
| `sandboxing/src/seatbelt_tls_tests.rs` | 8238 | ee0bfb28 | T |
| `sandboxing/src/spawn.rs` | 5441 | 86d2878f | P |
| `sandboxing/src/terminal_queries.rs` | 3536 | a6a3f458 | P |
| `sandboxing/src/terminal_queries_tests.rs` | 3040 | caf61ea1 | T |
| `sandboxing/src/violation.rs` | 9975 | 0d00a0f6 | P |
| `sandboxing/src/violation_tests.rs` | 7623 | 7e982ed7 | T |
| `sandboxing/src/windows.rs` | 17005 | 0f9df819 | P |
| `sandboxing/src/windows_mxc.rs` | 837 | 97b32a2f | P |
| `sandboxing/src/windows_tests.rs` | 2293 | 9525011e | T |

</details>

### D9.4 `codex-rs/network-proxy` (crate `codex-network-proxy`): PORT-ADAPT

* Files: **77** (23 test/harness), **1,317,426 bytes**. Pin: `codex-rs/network-proxy/*@603a7ba`.
* Zain destination: `vendor/codex/network-proxy/`; wiring in `crates/core/src/netpolicy/`
* Verdict: Local HTTP(S)/SOCKS5 proxy enforcing per-domain egress when a sandbox blocks direct network. Largest crate by bytes. Built on exact pre-release `rama 0.3.0-alpha.4` (crates.io has 0.4.0).
* Internal imports outside the selected set: `codex-utils-absolute-path`, `codex-utils-home-dir`, `codex-utils-path-uri`, `codex-utils-rustls-provider`; the identifier scan also saw `codex_otel` (a dependency of sandboxing and windows-sandbox; not verified in this crate Cargo.toml), `codex_cli_rs`, `codex_proxy_git_ssh_command` (not crates); Windows dev-dep `codex-windows-sandbox`.
* Risks: Frozen pre-release framework; AWS SigV4 and OpenTelemetry deps Zain does not need; whether the proxy terminates TLS (MITM CA handling) is a founder-level privacy decision: **UNKNOWN beyond sample**. Bypass classes: IP literal, DNS rebinding, CONNECT to an allowed host that proxies onward.
* Qualification tests: Unit: upstream tests. Integration: a sandboxed child reaches `allowed.example` only through the proxy. Negative: direct socket to a literal IP fails; a hostname resolving to 127.0.0.1 is refused; CONNECT to a denied host returns 403 and writes a receipt; redirect from an allowed to a denied host is blocked.

<details><summary>File list with blob sizes</summary>

| path (under `codex-rs/`) | B | blob | k |
|---|---:|---|---|
| `network-proxy/BUILD.bazel` | 129 | 79b3dc5e | B |
| `network-proxy/Cargo.toml` | 2575 | 0706660b | B |
| `network-proxy/README.md` | 15668 | d2809b55 | P |
| `network-proxy/src/attribution.rs` | 4676 | 85affff1 | P |
| `network-proxy/src/attribution_tests.rs` | 2086 | fcb3c377 | T |
| `network-proxy/src/authorization_path.rs` | 1993 | 1ed5acc5 | P |
| `network-proxy/src/authorization_path_tests.rs` | 1432 | 7ded5577 | T |
| `network-proxy/src/aws_sigv4.rs` | 25134 | d362b003 | P |
| `network-proxy/src/aws_sigv4_tests.rs` | 14139 | 05e164f1 | T |
| `network-proxy/src/body_budget.rs` | 6334 | f00e148a | P |
| `network-proxy/src/body_budget_tests.rs` | 3123 | 1336742e | T |
| `network-proxy/src/brokered_tunnel.rs` | 7959 | 1ef4566c | P |
| `network-proxy/src/brokered_tunnel_tests.rs` | 20775 | 7ffd36c6 | T |
| `network-proxy/src/certs.rs` | 47246 | 80730ecb | P |
| `network-proxy/src/config.rs` | 42879 | 2db5eb73 | P |
| `network-proxy/src/config/standalone.rs` | 9301 | 67f53c48 | P |
| `network-proxy/src/connect_policy.rs` | 9241 | abb6a67d | P |
| `network-proxy/src/connection_lifecycle/lifecycle_tests.rs` | 9420 | 09c4606b | T |
| `network-proxy/src/connection_lifecycle/listeners.rs` | 1231 | 5c414bcd | P |
| `network-proxy/src/connection_lifecycle/mod.rs` | 236 | b0219bbc | P |
| `network-proxy/src/connection_lifecycle/scope.rs` | 984 | 2af4b500 | P |
| `network-proxy/src/connection_lifecycle/service.rs` | 1119 | 2444b9cb | P |
| `network-proxy/src/credential_broker.rs` | 74617 | 727e9df5 | P |
| `network-proxy/src/credential_broker/configured.rs` | 22262 | b4f0630d | P |
| `network-proxy/src/credential_broker/configured_tests.rs` | 128288 | 34699e8e | T |
| `network-proxy/src/credential_broker/destination.rs` | 5392 | ef1dd4a3 | P |
| `network-proxy/src/credential_broker/environment.rs` | 18840 | 52081880 | P |
| `network-proxy/src/credential_broker/matching.rs` | 22247 | 7e205010 | P |
| `network-proxy/src/credential_broker/provider_config.rs` | 1459 | 566fa227 | P |
| `network-proxy/src/credential_broker/providers.rs` | 8006 | 725b7321 | P |
| `network-proxy/src/credential_broker/providers/github.rs` | 6010 | e79dc56d | P |
| `network-proxy/src/credential_broker/providers/openai.rs` | 2996 | 3b6808aa | P |
| `network-proxy/src/credential_broker/registry.rs` | 17650 | 2f740a0a | P |
| `network-proxy/src/credential_broker/replacement.rs` | 5196 | fde7c42a | P |
| `network-proxy/src/credential_broker_tests.rs` | 71602 | cace4352 | T |
| `network-proxy/src/domain_matcher.rs` | 7444 | bf71f8a2 | P |
| `network-proxy/src/domain_matcher_tests.rs` | 7524 | 83c0eec3 | T |
| `network-proxy/src/environment_policy.rs` | 5551 | aea0e9b9 | P |
| `network-proxy/src/host_policy_tests.rs` | 5726 | d6009ec3 | T |
| `network-proxy/src/http_proxy.rs` | 79673 | 541c4e8f | P |
| `network-proxy/src/http_proxy/host_header_tests.rs` | 5849 | 26ff6f96 | T |
| `network-proxy/src/lib.rs` | 5147 | 7e12ae9b | P |
| `network-proxy/src/main.rs` | 3006 | 6ef51861 | P |
| `network-proxy/src/main_tests.rs` | 3292 | b0ed9a08 | T |
| `network-proxy/src/mitm.rs` | 23665 | 01784c7b | P |
| `network-proxy/src/mitm_forwarding_tests.rs` | 23604 | 057806f3 | T |
| `network-proxy/src/mitm_hook.rs` | 44891 | ca1cde1b | P |
| `network-proxy/src/mitm_tests.rs` | 21439 | d4fcd34c | T |
| `network-proxy/src/native_certs.rs` | 9131 | 6c8d4500 | P |
| `network-proxy/src/network_policy.rs` | 40795 | 9af47415 | P |
| `network-proxy/src/policy.rs` | 14212 | d4f21422 | P |
| `network-proxy/src/process_log_metadata.rs` | 619 | cab758f4 | P |
| `network-proxy/src/proxy.rs` | 121818 | 5b1240ae | P |
| `network-proxy/src/proxy/execution_scope.rs` | 1962 | e01e115e | P |
| `network-proxy/src/proxy/managed_routing_tests.rs` | 4709 | 55ca34c3 | T |
| `network-proxy/src/reasons.rs` | 595 | 67f570f1 | P |
| `network-proxy/src/remote_config.rs` | 9770 | b5f20342 | P |
| `network-proxy/src/remote_config_tests.rs` | 16894 | 332d8a99 | T |
| `network-proxy/src/request_cancellation.rs` | 1173 | 90d481ac | P |
| `network-proxy/src/request_disconnect.rs` | 1319 | b56aa09a | P |
| `network-proxy/src/request_disconnect_tests.rs` | 1224 | f9ebc3a1 | T |
| `network-proxy/src/responses.rs` | 4316 | d2aeb990 | P |
| `network-proxy/src/runtime.rs` | 90085 | 2c826c4e | P |
| `network-proxy/src/secret_substitution.rs` | 9788 | ff808209 | P |
| `network-proxy/src/secret_substitution_tests.rs` | 8925 | 8d432105 | T |
| `network-proxy/src/socket_path.rs` | 1562 | ce72bcdc | P |
| `network-proxy/src/socks5.rs` | 44562 | c8e7120c | P |
| `network-proxy/src/state.rs` | 16969 | fe94a577 | P |
| `network-proxy/src/system_dns.rs` | 1949 | 5149bccb | P |
| `network-proxy/src/system_dns_tests.rs` | 3340 | 9d74646b | T |
| `network-proxy/src/upstream.rs` | 9739 | 2ad98e8c | P |
| `network-proxy/src/upstream_tests.rs` | 6528 | f2c8ea20 | T |
| `network-proxy/src/windows_proxy_ingress.rs` | 11208 | a1b7891c | P |
| `network-proxy/src/windows_proxy_ingress_tests.rs` | 1385 | 6fb0cc8e | T |
| `network-proxy/src/windows_tcp_attribution.rs` | 10594 | 8134d04f | P |
| `network-proxy/src/windows_tcp_attribution_tests.rs` | 3742 | ebbc4b81 | T |
| `network-proxy/tests/windows_stable_ingress.rs` | 19457 | 1e04563c | T |

</details>

### D9.5 `codex-rs/windows-sandbox-rs` (crate `codex-windows-sandbox`): PORT-ADAPT

* Files: **127** (42 test/harness), **1,134,355 bytes**. Pin: `codex-rs/windows-sandbox-rs/*@603a7ba`.
* Zain destination: `vendor/codex/windows-sandbox/` (crate `codex-windows-sandbox`)
* Verdict: The native Windows sandbox: restricted tokens + capability SIDs (unelevated) or dedicated local sandbox users + WFP filters (elevated); three binaries (`codex-windows-sandbox-setup`, `codex-command-runner`, `codex-windows-managed-deny-probe`); includes `sandbox_smoketests.py` and an embedded manifest. This is the Phase-8 core of R13 (F3).
* Internal imports outside the selected set: `codex-protocol`, `codex-utils-pty`, `codex-utils-absolute-path`, `codex-utils-string`, `codex-utils-process`, `codex-http-client`, `codex-otel`; dev: `codex-utils-cargo-bin`, in-crate `tests/support` (`codex-windows-sandbox-test-support`).
* Risks: The elevated backend needs UAC, edits ACLs on workspace roots, creates local users, stores DPAPI secrets, installs WFP filters that persist if teardown fails. MXC availability on Windows 11 Home is unproven (R13 U2). `windows 0.58` is four minors behind 0.62.2. `codex-http-client` use must be audited.
* Qualification tests: Unit: upstream tests. Negative (must exist before adoption): child cannot write outside granted roots, cannot read a deny-read path, cannot connect to a non-loopback address with network off, cannot kill the parent, cannot break out of the Job Object, and a hard parent kill leaves no orphan WFP filters or users after the documented cleanup command.

<details><summary>File list with blob sizes</summary>

| path (under `codex-rs/`) | B | blob | k |
|---|---:|---|---|
| `windows-sandbox-rs/BUILD.bazel` | 2924 | 9a3a03e2 | B |
| `windows-sandbox-rs/Cargo.toml` | 2792 | a798fb82 | B |
| `windows-sandbox-rs/build.rs` | 1416 | 6ba79e6c | P |
| `windows-sandbox-rs/codex-windows-sandbox-setup.manifest` | 370 | 14807962 | B |
| `windows-sandbox-rs/sandbox_smoketests.py` | 29090 | a1553e5e | T |
| `windows-sandbox-rs/src/acl.rs` | 40351 | e3f2ecd8 | P |
| `windows-sandbox-rs/src/acl_tests.rs` | 7684 | 44a1cd90 | T |
| `windows-sandbox-rs/src/allow.rs` | 12810 | 4eb4ec29 | P |
| `windows-sandbox-rs/src/app_package.rs` | 9356 | 50a6e7db | P |
| `windows-sandbox-rs/src/app_package_tests.rs` | 5644 | d4d06e84 | T |
| `windows-sandbox-rs/src/bin/command_runner/main.rs` | 308 | 1e3c88b4 | P |
| `windows-sandbox-rs/src/bin/command_runner/win.rs` | 26031 | e2dcb672 | P |
| `windows-sandbox-rs/src/bin/command_runner/win/cwd_junction.rs` | 4965 | 9243cc67 | P |
| `windows-sandbox-rs/src/bin/command_runner/win/input_loop_tests.rs` | 2929 | 23344b2c | T |
| `windows-sandbox-rs/src/bin/managed_deny_probe/main.rs` | 299 | 4535c9b9 | P |
| `windows-sandbox-rs/src/bin/managed_deny_probe/win.rs` | 3211 | 159268d8 | P |
| `windows-sandbox-rs/src/bin/setup_main/main.rs` | 222 | 0f2ff98d | P |
| `windows-sandbox-rs/src/cap.rs` | 7394 | 41b33b63 | P |
| `windows-sandbox-rs/src/conpty/mod.rs` | 7004 | 86839955 | P |
| `windows-sandbox-rs/src/deny_read_acl.rs` | 5374 | 06eda3b6 | P |
| `windows-sandbox-rs/src/deny_read_resolver.rs` | 29415 | e9a92a46 | P |
| `windows-sandbox-rs/src/deny_read_resolver_access_tests.rs` | 8964 | f29bf0e0 | T |
| `windows-sandbox-rs/src/deny_read_state.rs` | 6555 | 7b12f50b | P |
| `windows-sandbox-rs/src/deny_read_state_tests.rs` | 13102 | 7a651ad7 | T |
| `windows-sandbox-rs/src/deny_read_walker.rs` | 5063 | dd1b6e3c | P |
| `windows-sandbox-rs/src/deny_read_walker_tests.rs` | 463 | 88361977 | T |
| `windows-sandbox-rs/src/desktop.rs` | 17384 | 815d135b | P |
| `windows-sandbox-rs/src/desktop_tests.rs` | 8444 | 00d51605 | T |
| `windows-sandbox-rs/src/dpapi.rs` | 2739 | 3a907041 | P |
| `windows-sandbox-rs/src/elevated/ipc_framed.rs` | 9208 | 169c9e77 | P |
| `windows-sandbox-rs/src/elevated/mod.rs` | 116 | 70d1ad9c | P |
| `windows-sandbox-rs/src/elevated/runner_client.rs` | 23236 | 3049a8c4 | P |
| `windows-sandbox-rs/src/elevated/runner_metrics.rs` | 1143 | 460e5317 | P |
| `windows-sandbox-rs/src/elevated/runner_metrics_tests.rs` | 710 | 7d7e17ee | T |
| `windows-sandbox-rs/src/elevated/runner_pipe.rs` | 5180 | b7cd5b24 | P |
| `windows-sandbox-rs/src/elevated_impl.rs` | 13121 | 69cdb39e | P |
| `windows-sandbox-rs/src/env.rs` | 5573 | bdf7a76a | P |
| `windows-sandbox-rs/src/environment_transport.rs` | 6188 | e6088174 | P |
| `windows-sandbox-rs/src/environment_transport_tests.rs` | 5258 | 5cfe7f0f | T |
| `windows-sandbox-rs/src/file_write.rs` | 5953 | e0c5b3cb | P |
| `windows-sandbox-rs/src/file_write_tests.rs` | 2289 | 6711c805 | T |
| `windows-sandbox-rs/src/framed_io.rs` | 3002 | 537257f5 | P |
| `windows-sandbox-rs/src/helper_materialization.rs` | 16281 | 1d219422 | P |
| `windows-sandbox-rs/src/helper_materialization/copy.rs` | 3924 | 2658bd35 | P |
| `windows-sandbox-rs/src/helper_materialization/copy_tests.rs` | 2050 | 8a71d392 | T |
| `windows-sandbox-rs/src/hide_users.rs` | 6667 | 1e454835 | P |
| `windows-sandbox-rs/src/identity.rs` | 22129 | 022c9f8e | P |
| `windows-sandbox-rs/src/identity_integration_tests.rs` | 10576 | 9e9bfe4c | T |
| `windows-sandbox-rs/src/installation_record.rs` | 3649 | 3fc2f23a | P |
| `windows-sandbox-rs/src/launch_environment.rs` | 1154 | 7af15372 | P |
| `windows-sandbox-rs/src/launch_environment_tests.rs` | 460 | d2dc558e | T |
| `windows-sandbox-rs/src/lib.rs` | 37354 | f3de67d5 | P |
| `windows-sandbox-rs/src/logging.rs` | 8910 | 8bbd721b | P |
| `windows-sandbox-rs/src/no_reparse_dir.rs` | 10119 | 0abb616f | P |
| `windows-sandbox-rs/src/no_reparse_dir_tests.rs` | 6423 | 1ff5454d | T |
| `windows-sandbox-rs/src/package_identity.rs` | 1878 | 9ee96797 | P |
| `windows-sandbox-rs/src/path_normalization.rs` | 783 | 1735b745 | P |
| `windows-sandbox-rs/src/proc_thread_attr.rs` | 5716 | aa0850aa | P |
| `windows-sandbox-rs/src/process.rs` | 12528 | 36be9377 | P |
| `windows-sandbox-rs/src/provisioning_client.rs` | 18280 | cece9f83 | P |
| `windows-sandbox-rs/src/provisioning_client/group_change.rs` | 795 | 6eca7033 | P |
| `windows-sandbox-rs/src/provisioning_client/refresh_retry.rs` | 3789 | c4ea2336 | P |
| `windows-sandbox-rs/src/provisioning_client/refresh_retry_tests.rs` | 4342 | ab553e75 | T |
| `windows-sandbox-rs/src/provisioning_client_tests.rs` | 2657 | f08c29f4 | T |
| `windows-sandbox-rs/src/provisioning_protocol.rs` | 3233 | 6a8c9784 | P |
| `windows-sandbox-rs/src/resolved_permissions.rs` | 26621 | 12e24d94 | P |
| `windows-sandbox-rs/src/runtime_ownership.rs` | 9278 | d5ec71b6 | P |
| `windows-sandbox-rs/src/runtime_ownership_tests.rs` | 9098 | 6fade70a | T |
| `windows-sandbox-rs/src/sandbox_utils.rs` | 4503 | 1dfd7683 | P |
| `windows-sandbox-rs/src/service_diagnostics.rs` | 4619 | 2fcf747f | P |
| `windows-sandbox-rs/src/service_identity.rs` | 2427 | ce60848d | P |
| `windows-sandbox-rs/src/service_identity_tests.rs` | 697 | 358057ea | T |
| `windows-sandbox-rs/src/setup.rs` | 98644 | 7c9cd636 | P |
| `windows-sandbox-rs/src/setup_acl_error.rs` | 1284 | be96335a | P |
| `windows-sandbox-rs/src/setup_acl_error_tests.rs` | 2456 | 873d0c22 | T |
| `windows-sandbox-rs/src/setup_error.rs` | 11408 | d9104602 | P |
| `windows-sandbox-rs/src/setup_launch.rs` | 2716 | 7384c5f6 | P |
| `windows-sandbox-rs/src/setup_launch_tests.rs` | 4673 | 21968f13 | T |
| `windows-sandbox-rs/src/setup_mutex.rs` | 3105 | 9f7f46b4 | P |
| `windows-sandbox-rs/src/setup_provisioning.rs` | 55601 | d4557688 | P |
| `windows-sandbox-rs/src/setup_provisioning/acl_tests.rs` | 7301 | 876d6050 | T |
| `windows-sandbox-rs/src/setup_provisioning/firewall.rs` | 25057 | 81f4fa50 | P |
| `windows-sandbox-rs/src/setup_provisioning/firewall_apartment_tests.rs` | 1567 | a08826de | T |
| `windows-sandbox-rs/src/setup_provisioning/read_acl_mutex.rs` | 1907 | 9a60942f | P |
| `windows-sandbox-rs/src/setup_provisioning/registered_tests.rs` | 3647 | e815b60b | T |
| `windows-sandbox-rs/src/setup_provisioning/sandbox_users.rs` | 17659 | 480bbf7c | P |
| `windows-sandbox-rs/src/setup_provisioning/sandbox_users_tests.rs` | 3121 | 597a75e9 | T |
| `windows-sandbox-rs/src/setup_provisioning/service.rs` | 1883 | f0c5ddcd | P |
| `windows-sandbox-rs/src/setup_provisioning/setup_runtime_bin.rs` | 7390 | c4173b8a | P |
| `windows-sandbox-rs/src/setup_provisioning/setup_runtime_bin_tests.rs` | 9669 | ac5a4ede | T |
| `windows-sandbox-rs/src/setup_provisioning/setup_runtime_long_paths_tests.rs` | 3198 | 4e5df342 | T |
| `windows-sandbox-rs/src/setup_refresh_tests.rs` | 2482 | accb3818 | T |
| `windows-sandbox-rs/src/spawn_prep.rs` | 26307 | a19f0eea | P |
| `windows-sandbox-rs/src/ssh_config_dependencies.rs` | 7435 | ae6d82d5 | P |
| `windows-sandbox-rs/src/stdio_bridge.rs` | 4334 | 3ad722ba | P |
| `windows-sandbox-rs/src/stdio_bridge_tests.rs` | 2043 | c13632b8 | T |
| `windows-sandbox-rs/src/token.rs` | 18283 | f09dabd6 | P |
| `windows-sandbox-rs/src/token_groups_tests.rs` | 4030 | d14b8350 | T |
| `windows-sandbox-rs/src/token_tests.rs` | 9146 | c1856dae | T |
| `windows-sandbox-rs/src/token_user.rs` | 2539 | 3c8689dd | P |
| `windows-sandbox-rs/src/token_user_tests.rs` | 2638 | b2614ce0 | T |
| `windows-sandbox-rs/src/unified_exec/backends/elevated.rs` | 9881 | 0fd0ba9f | P |
| `windows-sandbox-rs/src/unified_exec/backends/elevated_tests.rs` | 10635 | 7a3a8c3c | T |
| `windows-sandbox-rs/src/unified_exec/backends/legacy.rs` | 16769 | d2bfe794 | P |
| `windows-sandbox-rs/src/unified_exec/backends/mod.rs` | 79 | 9d2aaa90 | P |
| `windows-sandbox-rs/src/unified_exec/backends/windows_common.rs` | 6030 | 05a87785 | P |
| `windows-sandbox-rs/src/unified_exec/backends/windows_common_tests.rs` | 1187 | 1a957e1e | T |
| `windows-sandbox-rs/src/unified_exec/mod.rs` | 6631 | 4f8b43ec | P |
| `windows-sandbox-rs/src/unified_exec/tests.rs` | 42446 | be2d1bf0 | T |
| `windows-sandbox-rs/src/uninstall_windows.rs` | 8510 | b8da9067 | P |
| `windows-sandbox-rs/src/uninstall_windows/firewall.rs` | 1336 | 0e5c98d3 | P |
| `windows-sandbox-rs/src/uninstall_windows/principals.rs` | 6127 | ab80a94b | P |
| `windows-sandbox-rs/src/uninstall_windows/principals_tests.rs` | 7722 | cc95e4d0 | T |
| `windows-sandbox-rs/src/uninstall_windows/processes.rs` | 9202 | 13d65003 | P |
| `windows-sandbox-rs/src/uninstall_windows/retained_logons.rs` | 2803 | 8df1ac69 | P |
| `windows-sandbox-rs/src/uninstall_windows/retained_logons_tests.rs` | 3640 | 44d9bdcc | T |
| `windows-sandbox-rs/src/wfp.rs` | 17060 | d992bcdd | P |
| `windows-sandbox-rs/src/wfp/filter_specs.rs` | 5267 | d86df4ac | P |
| `windows-sandbox-rs/src/wfp_setup.rs` | 6385 | 45e8dc23 | P |
| `windows-sandbox-rs/src/winutil.rs` | 12308 | 08993626 | P |
| `windows-sandbox-rs/src/workspace_acl.rs` | 943 | 7143212b | P |
| `windows-sandbox-rs/src/wrapper.rs` | 20084 | c449505f | P |
| `windows-sandbox-rs/src/wrapper_tests.rs` | 8066 | e68299e0 | T |
| `windows-sandbox-rs/tests/helper_manifest.rs` | 3174 | f0f7c43e | T |
| `windows-sandbox-rs/tests/support/BUILD.bazel` | 218 | dea52396 | T |
| `windows-sandbox-rs/tests/support/Cargo.toml` | 257 | 6cfb1fb7 | T |
| `windows-sandbox-rs/tests/support/src/lib.rs` | 1852 | 7c69fd1f | T |

</details>

### D9.6 `codex-rs/windows-sandbox-service` (crate `codex-windows-sandbox-service`): REFERENCE

* Files: **36** (9 test/harness), **244,543 bytes**. Pin: `codex-rs/windows-sandbox-service/*@603a7ba`.
* Zain destination: none: REFERENCE only; fold the idea into the single Zain Windows helper service (R13 line 420)
* Verdict: A Windows service wrapper for the elevated backend. It depends on `codex-core`, `codex-config` and `codex-cloud-config`; vendoring means importing codex-core (18.6 MB). Zain should not run two services: reimplement a small service shell around `codex-windows-sandbox`.
* Internal imports outside the selected set: `codex-core` (prod; 1,060 files), `codex-config` (108), `codex-cloud-config` (16), plus in-set `codex-windows-sandbox`. Includes `src/registered_runtime/removal.ps1` (a PowerShell uninstall script; review before reuse).
* Risks: Copying imports the Codex runtime. Service install and removal are privileged operations that must follow the Zain installer policy.
* Qualification tests: Not adopted. Tests apply to the Zain own service: installs only after explicit elevation consent; uninstall leaves no service, users or filters; the named pipe rejects unauthenticated clients (negative).

<details><summary>File list with blob sizes</summary>

| path (under `codex-rs/`) | B | blob | k |
|---|---:|---|---|
| `windows-sandbox-service/BUILD.bazel` | 460 | 63bcdf55 | B |
| `windows-sandbox-service/Cargo.toml` | 1621 | b4652f85 | B |
| `windows-sandbox-service/src/installation_record.rs` | 3177 | 10f9e76e | P |
| `windows-sandbox-service/src/ipc.rs` | 14363 | 2d8e9ad1 | P |
| `windows-sandbox-service/src/ipc/authentication.rs` | 9139 | 096e9358 | P |
| `windows-sandbox-service/src/ipc/home.rs` | 6202 | a1741175 | P |
| `windows-sandbox-service/src/ipc/listener.rs` | 4485 | 3895e3a9 | P |
| `windows-sandbox-service/src/ipc/request.rs` | 3347 | f084cac3 | P |
| `windows-sandbox-service/src/ipc_tests.rs` | 29564 | 14a7dbdc | T |
| `windows-sandbox-service/src/lib.rs` | 873 | aef9ed77 | P |
| `windows-sandbox-service/src/machine_policy.rs` | 6607 | 971be1d3 | P |
| `windows-sandbox-service/src/machine_policy_tests.rs` | 9583 | 520aa5a6 | T |
| `windows-sandbox-service/src/main.rs` | 760 | 12f5710f | P |
| `windows-sandbox-service/src/main_tests.rs` | 1138 | d3a1eac3 | T |
| `windows-sandbox-service/src/package_identity.rs` | 4505 | 03e2def3 | P |
| `windows-sandbox-service/src/package_identity/registered.rs` | 3096 | 34414a29 | P |
| `windows-sandbox-service/src/package_lifecycle.rs` | 12398 | 42e6adc0 | P |
| `windows-sandbox-service/src/package_lifecycle/cleanup.rs` | 8090 | 3d277159 | P |
| `windows-sandbox-service/src/package_lifecycle/registered.rs` | 5995 | cbddff13 | P |
| `windows-sandbox-service/src/provisioning.rs` | 4900 | bc99a9e3 | P |
| `windows-sandbox-service/src/provisioning/registered.rs` | 9583 | d0291a22 | P |
| `windows-sandbox-service/src/provisioning/registered_tests.rs` | 10191 | 3ef3f880 | T |
| `windows-sandbox-service/src/registered_runtime.rs` | 13726 | abf1468d | P |
| `windows-sandbox-service/src/registered_runtime/known_folder.rs` | 1190 | e695f635 | P |
| `windows-sandbox-service/src/registered_runtime/metadata.rs` | 11927 | 48cd4e66 | P |
| `windows-sandbox-service/src/registered_runtime/metadata_tests.rs` | 3052 | 72199f12 | T |
| `windows-sandbox-service/src/registered_runtime/registration_result.rs` | 2982 | e186b4b3 | P |
| `windows-sandbox-service/src/registered_runtime/registration_result_tests.rs` | 3305 | 5586b1fe | T |
| `windows-sandbox-service/src/registered_runtime/removal.ps1` | 14848 | 17ff74f5 | P |
| `windows-sandbox-service/src/registered_runtime/removal.rs` | 10912 | 79b11bc8 | P |
| `windows-sandbox-service/src/registered_runtime/removal_tests.rs` | 5841 | 10cbef44 | T |
| `windows-sandbox-service/src/service.rs` | 13022 | c5abe375 | P |
| `windows-sandbox-service/src/service/runtime_lifecycle.rs` | 6693 | 1dec5e8e | P |
| `windows-sandbox-service/src/service/runtime_lifecycle_tests.rs` | 3577 | e5d83235 | T |
| `windows-sandbox-service/src/uninstall_policy.rs` | 935 | f452e71a | P |
| `windows-sandbox-service/src/uninstall_policy_tests.rs` | 2456 | cb470891 | T |

</details>

### D9.7 `codex-rs/mxc-sandbox` (crate `codex-mxc-sandbox`): PORT-ADAPT (deferred)

* Files: **11** (2 test/harness), **76,592 bytes**. Pin: `codex-rs/mxc-sandbox/*@603a7ba`.
* Zain destination: `vendor/codex/mxc-sandbox/` (Phase 8, optional)
* Verdict: Routes a command into Microsoft MXC `BaseContainerRunner` with a kill-on-close job and no ACL edits, users or elevation (`README.md@603a7ba`). Best fit for Windows 11 Home if MXC/PSEC exists there (R13 U2 unresolved).
* Internal imports outside the selected set: `codex-protocol`, `codex-utils-absolute-path`, `codex-utils-path-uri`, `codex-network-proxy`, `codex-windows-sandbox`; external git `mxc-sdk` rev `b21120168d70befe12356411423266bfef168446`.
* Risks: Availability on consumer Windows is unproven; git dependency has no crates.io release; `tracelogging =1.2.3` exact pin; `flatbuffers 25`.
* Qualification tests: Unit: `is_available()` returns false cleanly on unsupported hosts (negative). A deny path without `PSE_SUPPORT_FS_DENY` fails before launch (README). Child never outlives the wrapper.

<details><summary>File list with blob sizes</summary>

| path (under `codex-rs/`) | B | blob | k |
|---|---:|---|---|
| `mxc-sandbox/BUILD.bazel` | 125 | d9b18072 | B |
| `mxc-sandbox/Cargo.toml` | 1221 | 2cd39d5d | B |
| `mxc-sandbox/README.md` | 7503 | 50a66c98 | P |
| `mxc-sandbox/src/availability.rs` | 3014 | 5e32aea9 | P |
| `mxc-sandbox/src/lib.rs` | 5354 | fde6ddf1 | P |
| `mxc-sandbox/src/native.rs` | 1659 | 9c615183 | P |
| `mxc-sandbox/src/policy.rs` | 17682 | 11ebd06c | P |
| `mxc-sandbox/src/policy_tests.rs` | 30648 | bb2b1729 | T |
| `mxc-sandbox/src/transport.rs` | 1463 | 5cb5d1c9 | P |
| `mxc-sandbox/src/transport_tests.rs` | 1633 | 984cfb04 | T |
| `mxc-sandbox/src/windows.rs` | 6290 | 99ef6179 | P |

</details>

### D9.8 `codex-rs/linux-sandbox` (crate `codex-linux-sandbox`): PORT-ADAPT (deferred)

* Files: **42** (24 test/harness), **473,661 bytes**. Pin: `codex-rs/linux-sandbox/*@603a7ba`.
* Zain destination: `vendor/codex/linux-sandbox/` (Linux CI only; deferred)
* Verdict: Landlock + seccomp helper binary that applies the policy then execs; uses bwrap for mount namespaces. Not needed on Windows; keep as a Phase-8 Linux target.
* Internal imports outside the selected set: `codex-protocol`, `codex-uds`, `codex-utils-absolute-path`, `codex-install-context`; dev: `codex-core`, `codex-utils-cargo-bin`. In-set: `codex-network-proxy`, `codex-process-hardening`, `codex-sandboxing`.
* Risks: Kernel feature requirements (Landlock ABI, user namespaces); tests need `codex-core` (dev) and cannot run unmodified; seccomp denies ptrace, which blocks debuggers (R13 R-D4).
* Qualification tests: Linux CI: write outside root fails; ptrace attach fails; blocked network syscalls when disabled. Negative: on a kernel without Landlock the helper fails closed rather than running unsandboxed.

<details><summary>File list with blob sizes</summary>

| path (under `codex-rs/`) | B | blob | k |
|---|---:|---|---|
| `linux-sandbox/BUILD.bazel` | 339 | 984f870b | B |
| `linux-sandbox/Cargo.toml` | 1315 | 26abe26d | B |
| `linux-sandbox/README.md` | 7181 | b1189316 | P |
| `linux-sandbox/build.rs` | 77 | 968cfc7e | P |
| `linux-sandbox/src/bazel_bwrap.rs` | 2218 | 39dc69ed | P |
| `linux-sandbox/src/bundled_bwrap.rs` | 7090 | 29f6cbb1 | P |
| `linux-sandbox/src/bundled_bwrap_tests.rs` | 4448 | c4261a1d | T |
| `linux-sandbox/src/bwrap.rs` | 57966 | 11959d0c | P |
| `linux-sandbox/src/bwrap_tests.rs` | 59508 | 9f53e2c9 | T |
| `linux-sandbox/src/bwrap_wslg_tests.rs` | 9590 | b3cb688e | T |
| `linux-sandbox/src/daemon_mounts.rs` | 10075 | 1ad026f1 | P |
| `linux-sandbox/src/daemon_mounts_tests.rs` | 12571 | c332cad2 | T |
| `linux-sandbox/src/exec_util.rs` | 1364 | f58dabfc | P |
| `linux-sandbox/src/exec_util_tests.rs` | 1123 | 37565baf | T |
| `linux-sandbox/src/fd_mount.rs` | 3353 | c4a8a638 | P |
| `linux-sandbox/src/fd_mount_tests.rs` | 5719 | b6e7ad32 | T |
| `linux-sandbox/src/launcher.rs` | 8950 | b4455ff2 | P |
| `linux-sandbox/src/launcher_tests.rs` | 6628 | 565d82ed | T |
| `linux-sandbox/src/lib.rs` | 1333 | fa75c702 | P |
| `linux-sandbox/src/linux_run_main.rs` | 43570 | 3ba283b3 | P |
| `linux-sandbox/src/linux_run_main_tests.rs` | 24258 | 0e8e9acf | T |
| `linux-sandbox/src/main.rs` | 223 | 83602b50 | P |
| `linux-sandbox/src/proxy_lifecycle.rs` | 7660 | 1ee01481 | P |
| `linux-sandbox/src/proxy_lifecycle_tests.rs` | 4136 | 3726a3b0 | T |
| `linux-sandbox/src/proxy_routing.rs` | 16466 | 94f3527b | P |
| `linux-sandbox/src/proxy_routing_tests.rs` | 3696 | 527efab4 | T |
| `linux-sandbox/src/seccomp.rs` | 11834 | 67cc7242 | P |
| `linux-sandbox/src/seccomp_tests.rs` | 2047 | 8fde061f | T |
| `linux-sandbox/src/wslg.rs` | 2557 | 01b2eca2 | P |
| `linux-sandbox/src/wslg_tests.rs` | 1897 | 2128433f | T |
| `linux-sandbox/tests/all.rs` | 153 | fdf98aa9 | T |
| `linux-sandbox/tests/suite/bundled_bwrap.rs` | 3507 | d4691f51 | T |
| `linux-sandbox/tests/suite/bwrap_path.rs` | 5456 | 33a37886 | T |
| `linux-sandbox/tests/suite/daemon_sockets_tests.rs` | 13932 | 0aaf460f | T |
| `linux-sandbox/tests/suite/denied_files_tests.rs` | 8671 | a982f62a | T |
| `linux-sandbox/tests/suite/managed_proxy.rs` | 43378 | 49f47f34 | T |
| `linux-sandbox/tests/suite/managed_proxy_unix_sockets_tests.rs` | 7514 | 312bfa5e | T |
| `linux-sandbox/tests/suite/mod.rs` | 133 | 31e89b5f | T |
| `linux-sandbox/tests/suite/nested_metadata_tests.rs` | 7622 | 6d2ef255 | T |
| `linux-sandbox/tests/suite/root_metadata_tests.rs` | 7160 | fe7d4dcc | T |
| `linux-sandbox/tests/suite/sandbox.rs` | 53583 | e0167df8 | T |
| `linux-sandbox/tests/suite/wslg_tests.rs` | 3360 | 8eb5efd5 | T |

</details>

### D9.9 `codex-rs/bwrap` (crate `codex-bwrap`): REFERENCE

* Files: **6** (0 test/harness), **33,121 bytes**. Pin: `codex-rs/bwrap/*@603a7ba`.
* Zain destination: none: DO NOT VENDOR; depend on the distro `bubblewrap` binary (Linux only)
* Verdict: The `build.rs` of this crate compiles the C sources in `codex-rs/vendor/bubblewrap/` (50 files: `bubblewrap.c` 117,032 B, `utils.c` 21,879 B, `network.c`, `bind-mount.c`, tests, `COPYING` 25,383 B). `vendor/bubblewrap/COPYING` begins with the GNU Library General Public License Version 2 (LGPL-2.0). Statically linking or copying it into a closed Zain binary creates LGPL obligations (source offer, relinkability). The five crate files are Apache-2.0 but useless without the C tree.
* Internal imports outside the selected set: `libc`; build deps `cc 1`, `pkg-config 0.3`; requires `libcap` via pkg-config and the out-of-crate C tree `codex-rs/vendor/bubblewrap` (LGPL-2.0).
* Risks: LGPL contamination if linked. The Windows-primary Zain does not need it.
* Qualification tests: CI licence gate: fail the build if any file under `vendor/` carries a copyleft licence not on the allow-list (negative test for this exact finding).

<details><summary>File list with blob sizes</summary>

| path (under `codex-rs/`) | B | blob | k |
|---|---:|---|---|
| `bwrap/BUILD.bazel` | 2147 | cc27df89 | B |
| `bwrap/Cargo.toml` | 305 | ed7010c8 | B |
| `bwrap/build.rs` | 3851 | d9d87932 | P |
| `bwrap/config.h` | 52 | f73932a0 | P |
| `bwrap/src/main.rs` | 1383 | 09c624aa | P |
| `vendor/bubblewrap/COPYING` | 25383 | 5bc8fb2c | P |

</details>

### D9.10 Summary of D9 verdicts

| Crate | Files / bytes | Mode | Zain destination | Blocking out-of-set deps |
|---|---:|---|---|---|
| process-hardening | 4 / 6,708 | COPY AS-IS | `vendor/codex/process-hardening/` | none |
| execpolicy | 17 / 98,465 | COPY AS-IS | `vendor/codex/execpolicy/` | utils-absolute-path |
| sandboxing | 38 / 445,533 | PORT-ADAPT | `vendor/codex/sandboxing/` | protocol, uds, pty, path-uri, otel |
| network-proxy | 77 / 1,317,426 | PORT-ADAPT | `vendor/codex/network-proxy/` | path-uri, home-dir, rustls-provider; rama alpha |
| windows-sandbox-rs | 127 / 1,134,355 | PORT-ADAPT | `vendor/codex/windows-sandbox/` | protocol, pty, http-client, otel, process, string |
| windows-sandbox-service | 36 / 244,543 | REFERENCE | `(none)` | codex-core, config, cloud-config |
| mxc-sandbox | 11 / 76,592 | PORT-ADAPT (deferred) | `vendor/codex/mxc-sandbox/` | protocol, path-uri; git mxc-sdk |
| linux-sandbox | 42 / 473,661 | PORT-ADAPT (deferred) | `vendor/codex/linux-sandbox/` | protocol, uds, install-context |
| bwrap | 5 / 7,738 | REFERENCE (LGPL) | `(none)` | vendor/bubblewrap C tree |

---

<!-- SECTION:D11 -->
## D11. Cedar policy engine (core crates: cedar-policy, cedar-policy-core, cedar-policy-formatter)

Policy language, evaluator, schema validator and formatter used as the analyzable authorisation engine behind Core (matrix row D11, Phase 3). Cedar is consumed as a crates.io dependency; nothing is copied. The file list is the audited upstream surface of the three core crates.

* Upstream: `cedar-policy/cedar@2c2b84772a63e8a5d57d98037b9389c5fd3812a3`.
* Zain destination: `crates/core/Cargo.toml` dependency `cedar-policy = "=4.14.0"` (default features `ipaddr`, `decimal`, `datetime`); schema and policy bundles in `crates/contracts/policy/` and `crates/core/src/policy/cedar/`.
* Copy mode: **DEPEND-ON-PACKAGE (crates.io `cedar-policy` 4.14.0, published 2026-10-17, Apache-2.0)**
* Selected surface: **299 files, 6,587,394 bytes** (3 crates; source bytes: cedar-policy 1,532,313 in 92 files, cedar-policy-core 4,913,433 in 181 files, cedar-policy-formatter 75,234 in 8 files). Not selected: `cedar-policy-cli` (25 src files), `cedar-policy-symcc` (42 src files; needs an external SMT solver per its `cvc5_tee.py`), `cedar-testing`, `cedar-wasm`, `cedar-language-server` (163 src files), benches and sample data.
* There is no separate `cedar-policy-validator` crate at this SHA: workspace members are exactly cedar-policy, -core, -formatter, -cli, -symcc, -testing, -wasm, -language-server (root `Cargo.toml`). Top-level modules under `cedar-policy-core/src/`: `ast`, `authorizer`, `batched_evaluator`, `entities`, `est`, `evaluator`, `extensions`, `parser`, `pst`, `tpe`, `transitive_closure`, `validator`.
* Internal imports outside the selected set: none. The only internal edges are path dependencies among the three crates (`cedar-policy` to `cedar-policy-core` and `cedar-policy-formatter`; formatter to core), all pinned `=4.14.0`.
* External dependencies (from the three Cargo.toml files; licenses from crates.io JSON):

| crate | declared | kind | optional | latest on crates.io | license |
|---|---|---|---|---|---|
| arbitrary | 1 | runtime | yes | 1.5.0 | MIT OR Apache-2.0 |
| chrono | 0.4.45 | runtime | yes | 0.4.45 | MIT OR Apache-2.0 |
| dhat | 0.3.2 | runtime | yes | 0.3.3 | MIT OR Apache-2.0 |
| educe | 0.8.0 | runtime | no | 0.8.1 | MIT |
| either | 1.16 | runtime | no | 1.19.0 | MIT OR Apache-2.0 |
| itertools | 0.15 | runtime | no | 0.15.0 | MIT OR Apache-2.0 |
| lalrpop | 0.22.2 | build | no | 0.23.2 | Apache-2.0 OR MIT |
| lalrpop-util | 0.22.2 | runtime | no | 0.23.2 | Apache-2.0 OR MIT |
| linked-hash-map | 0.5.6 | runtime | no | 0.5.6 | MIT/Apache-2.0 |
| linked_hash_set | 0.1.6 | runtime | no | 0.1.6 | Apache-2.0 |
| logos | 0.16.0 | runtime | no | 0.16.1 | MIT OR Apache-2.0 |
| miette | 7.6.0 | runtime | no | 7.6.0 | Apache-2.0 |
| nonempty | 0.12 | runtime | yes | 0.12.0 | MIT |
| pretty | 0.12.5 | runtime | no | 0.12.5 | MIT |
| prost | 0.14 | runtime | yes | 0.14.4 | Apache-2.0 |
| prost-build | 0.14 | build | yes | 0.14.4 | Apache-2.0 |
| ref-cast | 1.0 | runtime | no | 1.0.27 | MIT OR Apache-2.0 |
| regex | 1.12 | runtime | no | 1.13.1 | MIT OR Apache-2.0 |
| rustc-literal-escaper | 0.0.8 | runtime | no | 0.0.8 | Apache-2.0 OR MIT |
| semver | 1.0.28 | runtime | no | 1.0.28 | MIT OR Apache-2.0 |
| serde | 1.0 | runtime | no | 1.0.229 | MIT OR Apache-2.0 |
| serde-wasm-bindgen | 0.6 | runtime | yes | 0.6.5 | MIT |
| serde_json | 1.0 | runtime | no | 1.0.154 | MIT OR Apache-2.0 |
| serde_with | 3.21.0 | runtime | no | 3.24.0 | MIT OR Apache-2.0 |
| smol_str | 0.3 | runtime | no | 0.3.7 | MIT OR Apache-2.0 |
| stacker | 0.1.24 | runtime | no | 0.1.25 | MIT OR Apache-2.0 |
| thiserror | 2.0 | runtime | no | 2.0.21 | MIT OR Apache-2.0 |
| tsify | 0.5.8 | runtime | yes | 0.5.8 | MIT OR Apache-2.0 |
| unicode-security | 0.1.0 | runtime | no | 0.1.2 | MIT/Apache-2.0 |
| wasm-bindgen | 0.2.97 | runtime | yes | 0.2.129 | MIT OR Apache-2.0 |

* License and NOTICE obligations: Apache-2.0 (`LICENSE` 10,142 B). `NOTICE` (29 B) reads `Copyright Cedar Contributors`: carry it into the Zain NOTICE file. The root `THIRD_PARTY_LICENSES.txt` is a 41-byte symlink to `cedar-policy-cli/THIRD_PARTY_LICENSES.txt` (24,026 B), a notice bundle for the CLI dependency graph (MIT and ISC style texts for aho-corasick, memchr, strsim, pretty and others); the Zain release must generate its own third-party notice for the exact dependency graph shipped (cargo-about or equivalent). `deny.toml` shows the upstream allow-list (Apache-2.0, MIT, BSD, ISC, Unicode-3.0, Zlib and others).
* Risks: (1) Cedar guarantees apply only to the policies and entity data Zain builds: entity-graph construction and attribute typing in Core are the real attack surface. (2) Experimental features (`tpe`, `partial-eval`, `entity-manifest`, `protobufs`) change across minors; use only default features. (3) Fast release cadence (4.12.0 on 2026-07-28, 4.13.0 on 2026-09-15, 4.14.0 on 2026-10-17): pin exactly with `=`. (4) The Rust MSRV is declared through `rust-version.workspace` in the root manifest, which was not read in full: **UNKNOWN**. (5) Policy authoring UX is out of scope of the crate. (6) `cedar-for-agents` (D11 in 06, @41c07851) is a separate repo and is NOT covered by this manifest.
* Qualification tests: Positive: policy unit tests for each Zain action class; a `forbid` always overrides a `permit` (deny-overrides); an empty policy set denies. Negative: a policy referencing an unknown action or entity type fails schema validation at load and Core refuses to start; an evaluation error (missing attribute) is treated as deny and writes a receipt with the Cedar diagnostics; a policy bundle with a bad signature is rejected; entity UIDs built from attacker-controlled strings (file paths, URLs) are escaped so they cannot forge another principal; the same request evaluates identically across 1,000 runs (determinism); performance is measured on the founder machine at P3 (no number is claimed here).

<details><summary>File list with blob sizes (selected surface)</summary>

| path | B | blob | k |
|---|---:|---|---|
| `Cargo.toml` | 4288 | 5e7f9f01 | P |
| `LICENSE` | 10142 | 67db8588 | P |
| `NOTICE` | 29 | 9649f99a | P |
| `THIRD_PARTY_LICENSES.txt` | 41 | 78950a14 | P |
| `cedar-policy-cli/THIRD_PARTY_LICENSES.txt` | 24026 | b2c09e76 | P |
| `cedar-policy-core/Cargo.toml` | 2513 | 80adff08 | P |
| `cedar-policy-core/README.md` | 999 | 66be0dc6 | P |
| `cedar-policy-core/build.rs` | 1088 | a42cfa2a | P |
| `cedar-policy-core/experimental_warning.md` | 255 | fcd98d84 | P |
| `cedar-policy-core/src/ast.rs` | 1386 | e8367a64 | P |
| `cedar-policy-core/src/ast/annotation.rs` | 4398 | 9dff88b4 | P |
| `cedar-policy-core/src/ast/entity.rs` | 40681 | d1de5e2e | P |
| `cedar-policy-core/src/ast/expr.rs` | 93157 | 1cb06b6f | P |
| `cedar-policy-core/src/ast/expr_allows_errors.rs` | 14795 | c9dea848 | P |
| `cedar-policy-core/src/ast/expr_iterator.rs` | 8354 | e19fec21 | P |
| `cedar-policy-core/src/ast/expr_visitor.rs` | 13465 | e8b14a0a | P |
| `cedar-policy-core/src/ast/extension.rs` | 22928 | f8fea069 | P |
| `cedar-policy-core/src/ast/id.rs` | 17813 | 91baec3b | P |
| `cedar-policy-core/src/ast/integer.rs` | 969 | 61f0244e | P |
| `cedar-policy-core/src/ast/literal.rs` | 3908 | 9dfc5374 | P |
| `cedar-policy-core/src/ast/name.rs` | 26259 | bbab2b50 | P |
| `cedar-policy-core/src/ast/ops.rs` | 3923 | e07132e5 | P |
| `cedar-policy-core/src/ast/partial_value.rs` | 6941 | b0bbee05 | P |
| `cedar-policy-core/src/ast/pattern.rs` | 8639 | 3c4e66b0 | P |
| `cedar-policy-core/src/ast/policy.rs` | 91101 | e28dc4a2 | P |
| `cedar-policy-core/src/ast/policy_set.rs` | 50639 | 9aa5a60e | P |
| `cedar-policy-core/src/ast/request.rs` | 30662 | 595676c9 | P |
| `cedar-policy-core/src/ast/restricted_expr.rs` | 29732 | 4feca815 | P |
| `cedar-policy-core/src/ast/types.rs` | 3368 | e935c032 | P |
| `cedar-policy-core/src/ast/value.rs` | 31709 | ef835a8d | P |
| `cedar-policy-core/src/authorizer.rs` | 24846 | 8fdded5a | P |
| `cedar-policy-core/src/authorizer/err.rs` | 3128 | a304e8c1 | P |
| `cedar-policy-core/src/authorizer/partial_response.rs` | 31508 | 7620f5ea | P |
| `cedar-policy-core/src/batched_evaluator.rs` | 10352 | 7b790e00 | P |
| `cedar-policy-core/src/batched_evaluator/err.rs` | 1979 | 2ff2725b | P |
| `cedar-policy-core/src/entities.rs` | 182525 | c9907a79 | P |
| `cedar-policy-core/src/entities/conformance.rs` | 36889 | c5531dbb | P |
| `cedar-policy-core/src/entities/conformance/err.rs` | 14320 | 9beed3f5 | P |
| `cedar-policy-core/src/entities/err.rs` | 4984 | 7b55f9d0 | P |
| `cedar-policy-core/src/entities/json.rs` | 1370 | 15a80399 | P |
| `cedar-policy-core/src/entities/json/context.rs` | 4717 | 74276be1 | P |
| `cedar-policy-core/src/entities/json/entities.rs` | 21680 | 61304032 | P |
| `cedar-policy-core/src/entities/json/err.rs` | 27352 | e84aedfe | P |
| `cedar-policy-core/src/entities/json/schema.rs` | 7010 | a9b9a44e | P |
| `cedar-policy-core/src/entities/json/schema_types.rs` | 6304 | 08240f7c | P |
| `cedar-policy-core/src/entities/json/value.rs` | 50392 | 68c6678b | P |
| `cedar-policy-core/src/error_macros.rs` | 4737 | 30bc489d | P |
| `cedar-policy-core/src/est.rs` | 185489 | 850a37c4 | P |
| `cedar-policy-core/src/est/annotation.rs` | 2874 | 14d03a5f | P |
| `cedar-policy-core/src/est/err.rs` | 5181 | 2a6af4ff | P |
| `cedar-policy-core/src/est/expr.rs` | 104862 | 676672c1 | P |
| `cedar-policy-core/src/est/policy_set.rs` | 26793 | c7825ee7 | P |
| `cedar-policy-core/src/est/scope_constraints.rs` | 42364 | 69149237 | P |
| `cedar-policy-core/src/evaluator.rs` | 264909 | 9df7c567 | P |
| `cedar-policy-core/src/evaluator/err.rs` | 28662 | dd196f3e | P |
| `cedar-policy-core/src/expr_builder.rs` | 15104 | 04f0aa13 | P |
| `cedar-policy-core/src/extensions.rs` | 16211 | df68cb82 | P |
| `cedar-policy-core/src/extensions/datetime.rs` | 58947 | 65b379d2 | P |
| `cedar-policy-core/src/extensions/decimal.rs` | 27631 | a666a4af | P |
| `cedar-policy-core/src/extensions/ipaddr.rs` | 58055 | 76ae5721 | P |
| `cedar-policy-core/src/extensions/partial_evaluation.rs` | 1576 | 0d786405 | P |
| `cedar-policy-core/src/from_normalized_str.rs` | 3236 | 2be90b02 | P |
| `cedar-policy-core/src/fuzzy_match.rs` | 6373 | f0634742 | P |
| `cedar-policy-core/src/jsonvalue.rs` | 7860 | 8e1d965b | P |
| `cedar-policy-core/src/lib.rs` | 4638 | c8941bbc | P |
| `cedar-policy-core/src/parser.rs` | 56303 | 9bad2de3 | P |
| `cedar-policy-core/src/parser/cst.rs` | 10602 | 1b9b95c4 | P |
| `cedar-policy-core/src/parser/cst_to_ast.rs` | 255269 | a8306b13 | P |
| `cedar-policy-core/src/parser/cst_to_ast/to_ref_or_refs.rs` | 25651 | 63596bf3 | P |
| `cedar-policy-core/src/parser/err.rs` | 40605 | 0b7cd1a8 | P |
| `cedar-policy-core/src/parser/fmt.rs` | 19675 | ace64d82 | P |
| `cedar-policy-core/src/parser/grammar.lalrpop` | 20483 | 47ae392c | P |
| `cedar-policy-core/src/parser/loc.rs` | 3730 | c1aaccef | P |
| `cedar-policy-core/src/parser/node.rs` | 6191 | 7ed98366 | P |
| `cedar-policy-core/src/parser/testfiles/policies.cedar` | 10511 | 9487d81e | P |
| `cedar-policy-core/src/parser/text_to_cst.rs` | 48215 | a66fd8fd | P |
| `cedar-policy-core/src/parser/unescape.rs` | 10753 | 992bf3de | P |
| `cedar-policy-core/src/parser/util.rs` | 2002 | f8e0e61c | P |
| `cedar-policy-core/src/pst/ast_conversions.rs` | 54470 | 94c2f4e4 | P |
| `cedar-policy-core/src/pst/constraints.rs` | 15861 | 8542632a | P |
| `cedar-policy-core/src/pst/err.rs` | 18399 | bbf21896 | P |
| `cedar-policy-core/src/pst/est_conversions.rs` | 54738 | 83ef0858 | P |
| `cedar-policy-core/src/pst/expr.rs` | 65451 | ee4ad70d | P |
| `cedar-policy-core/src/pst/mod.rs` | 8962 | 37c6791d | P |
| `cedar-policy-core/src/pst/policy.rs` | 29873 | 949d3118 | P |
| `cedar-policy-core/src/pst/policy_set.rs` | 2903 | 3386b942 | P |
| `cedar-policy-core/src/test_utils.rs` | 18183 | 04559af8 | P |
| `cedar-policy-core/src/tpe.rs` | 17693 | f92fed3e | P |
| `cedar-policy-core/src/tpe/entities.rs` | 48210 | 6b6b3acc | P |
| `cedar-policy-core/src/tpe/err.rs` | 16008 | a297f395 | P |
| `cedar-policy-core/src/tpe/evaluator.rs` | 120721 | 31f0a476 | P |
| `cedar-policy-core/src/tpe/request.rs` | 23571 | f4b14043 | P |
| `cedar-policy-core/src/tpe/residual.rs` | 33432 | fe532fb7 | P |
| `cedar-policy-core/src/tpe/response.rs` | 18372 | 01e7e8d1 | P |
| `cedar-policy-core/src/tpe/test_utils.rs` | 2678 | 1a8ac109 | P |
| `cedar-policy-core/src/transitive_closure.rs` | 75783 | 5e519564 | P |
| `cedar-policy-core/src/transitive_closure/err.rs` | 2690 | 028d8745 | P |
| `cedar-policy-core/src/validator.rs` | 37483 | f87c58f4 | P |
| `cedar-policy-core/src/validator/README.md` | 526 | 4752385a | P |
| `cedar-policy-core/src/validator/cedar_schema.rs` | 817 | 543754f8 | P |
| `cedar-policy-core/src/validator/cedar_schema/ast.rs` | 13371 | 7913d9ab | P |
| `cedar-policy-core/src/validator/cedar_schema/err.rs` | 29337 | 191b7eb1 | P |
| `cedar-policy-core/src/validator/cedar_schema/fmt.rs` | 31992 | 96526f2d | P |
| `cedar-policy-core/src/validator/cedar_schema/grammar.lalrpop` | 15014 | f4761e10 | P |
| `cedar-policy-core/src/validator/cedar_schema/parser.rs` | 4566 | 84ffdb0a | P |
| `cedar-policy-core/src/validator/cedar_schema/test.rs` | 121988 | 20b2b05a | P |
| `cedar-policy-core/src/validator/cedar_schema/testfiles/example.cedarschema` | 558 | 2016f40b | P |
| `cedar-policy-core/src/validator/cedar_schema/to_json_schema.rs` | 34697 | 42ac0a50 | P |
| `cedar-policy-core/src/validator/coreschema.rs` | 56598 | 0b430ed2 | P |
| `cedar-policy-core/src/validator/deprecated_schema_compat.rs` | 657 | b9caf68b | P |
| `cedar-policy-core/src/validator/deprecated_schema_compat/conversion.rs` | 12118 | fa14c946 | P |
| `cedar-policy-core/src/validator/deprecated_schema_compat/json_schema.rs` | 6017 | b079aab6 | P |
| `cedar-policy-core/src/validator/deprecated_schema_compat/test.rs` | 4852 | 8891f9b3 | P |
| `cedar-policy-core/src/validator/diagnostics.rs` | 21959 | 1264736f | P |
| `cedar-policy-core/src/validator/diagnostics/validation_errors.rs` | 32968 | 6da88d0a | P |
| `cedar-policy-core/src/validator/diagnostics/validation_warnings.rs` | 6226 | b1066cd2 | P |
| `cedar-policy-core/src/validator/entity_manifest.rs` | 59421 | 06516a1d | P |
| `cedar-policy-core/src/validator/entity_manifest/analysis.rs` | 11377 | 7d8fda37 | P |
| `cedar-policy-core/src/validator/entity_manifest/loader.rs` | 24460 | aba9b535 | P |
| `cedar-policy-core/src/validator/entity_manifest/slicing.rs` | 35750 | 4a53c8d2 | P |
| `cedar-policy-core/src/validator/entity_manifest/type_annotations.rs` | 7247 | cd0ff308 | P |
| `cedar-policy-core/src/validator/expr_iterator.rs` | 15511 | 36ace929 | P |
| `cedar-policy-core/src/validator/extension_schema.rs` | 5067 | 1a6bd399 | P |
| `cedar-policy-core/src/validator/extensions.rs` | 6692 | 821a3c1e | P |
| `cedar-policy-core/src/validator/extensions/datetime.rs` | 6825 | f717fec1 | P |
| `cedar-policy-core/src/validator/extensions/decimal.rs` | 5050 | 00aff92d | P |
| `cedar-policy-core/src/validator/extensions/ipaddr.rs` | 4991 | 4bffe63d | P |
| `cedar-policy-core/src/validator/extensions/partial_evaluation.rs` | 2851 | 87496e15 | P |
| `cedar-policy-core/src/validator/json_schema.rs` | 176404 | d9ca8e71 | P |
| `cedar-policy-core/src/validator/level_validate.rs` | 53454 | 5a522648 | P |
| `cedar-policy-core/src/validator/linking.rs` | 47960 | a4919c0c | P |
| `cedar-policy-core/src/validator/partition_nonempty.rs` | 730 | fc98007c | P |
| `cedar-policy-core/src/validator/rbac.rs` | 63096 | faa62aed | P |
| `cedar-policy-core/src/validator/schema.rs` | 234277 | c05043d5 | P |
| `cedar-policy-core/src/validator/schema/action.rs` | 15565 | 1193120d | P |
| `cedar-policy-core/src/validator/schema/entity_type.rs` | 7915 | f5a145cc | P |
| `cedar-policy-core/src/validator/schema/err.rs` | 46549 | 4d40cb65 | P |
| `cedar-policy-core/src/validator/schema/namespace_def.rs` | 44095 | 9e339de8 | P |
| `cedar-policy-core/src/validator/schema/raw_name.rs` | 14588 | 7740fb72 | P |
| `cedar-policy-core/src/validator/schema/snapshots/cedar_policy_core__validator__schema__to_json__tests__roundtrip_schemas@action_entity_ref.cedarschema.snap` | 374 | 6b14d8a3 | P |
| `cedar-policy-core/src/validator/schema/snapshots/cedar_policy_core__validator__schema__to_json__tests__roundtrip_schemas@action_hierarchy.cedarschema.snap` | 425 | cc4fa42e | P |
| `cedar-policy-core/src/validator/schema/snapshots/cedar_policy_core__validator__schema__to_json__tests__roundtrip_schemas@action_no_applies_to.cedarschema.snap` | 195 | a42eeb49 | P |
| `cedar-policy-core/src/validator/schema/snapshots/cedar_policy_core__validator__schema__to_json__tests__roundtrip_schemas@action_with_context.cedarschema.snap` | 328 | 04393817 | P |
| `cedar-policy-core/src/validator/schema/snapshots/cedar_policy_core__validator__schema__to_json__tests__roundtrip_schemas@app_document.cedarschema.snap` | 386 | 089a4414 | P |
| `cedar-policy-core/src/validator/schema/snapshots/cedar_policy_core__validator__schema__to_json__tests__roundtrip_schemas@basic_action.cedarschema.snap` | 264 | a917f3f0 | P |
| `cedar-policy-core/src/validator/schema/snapshots/cedar_policy_core__validator__schema__to_json__tests__roundtrip_schemas@basic_entity.cedarschema.snap` | 179 | 68e522cb | P |
| `cedar-policy-core/src/validator/schema/snapshots/cedar_policy_core__validator__schema__to_json__tests__roundtrip_schemas@common_types.cedarschema.snap` | 360 | 468f0fb9 | P |
| `cedar-policy-core/src/validator/schema/snapshots/cedar_policy_core__validator__schema__to_json__tests__roundtrip_schemas@complex_common_types.cedarschema.snap` | 596 | 0728c5d9 | P |
| `cedar-policy-core/src/validator/schema/snapshots/cedar_policy_core__validator__schema__to_json__tests__roundtrip_schemas@complex_types.cedarschema.snap` | 302 | 3991e33c | P |
| `cedar-policy-core/src/validator/schema/snapshots/cedar_policy_core__validator__schema__to_json__tests__roundtrip_schemas@comprehensive_schema.cedarschema.snap` | 2392 | 03fe4d0f | P |
| `cedar-policy-core/src/validator/schema/snapshots/cedar_policy_core__validator__schema__to_json__tests__roundtrip_schemas@cross_namespace_references.cedarschema.snap` | 481 | 08241620 | P |
| `cedar-policy-core/src/validator/schema/snapshots/cedar_policy_core__validator__schema__to_json__tests__roundtrip_schemas@deeply_nested_records.cedarschema.snap` | 450 | 7f4dcb09 | P |
| `cedar-policy-core/src/validator/schema/snapshots/cedar_policy_core__validator__schema__to_json__tests__roundtrip_schemas@empty_schema.cedarschema.snap` | 167 | ab72d880 | P |
| `cedar-policy-core/src/validator/schema/snapshots/cedar_policy_core__validator__schema__to_json__tests__roundtrip_schemas@entity_hierarchy.cedarschema.snap` | 245 | 3e1478d1 | P |
| `cedar-policy-core/src/validator/schema/snapshots/cedar_policy_core__validator__schema__to_json__tests__roundtrip_schemas@entity_references.cedarschema.snap` | 275 | c62b8ac5 | P |
| `cedar-policy-core/src/validator/schema/snapshots/cedar_policy_core__validator__schema__to_json__tests__roundtrip_schemas@entity_tags.cedarschema.snap` | 352 | f2488462 | P |
| `cedar-policy-core/src/validator/schema/snapshots/cedar_policy_core__validator__schema__to_json__tests__roundtrip_schemas@entity_with_attributes.cedarschema.snap` | 266 | 45245ea2 | P |
| `cedar-policy-core/src/validator/schema/snapshots/cedar_policy_core__validator__schema__to_json__tests__roundtrip_schemas@enum_entities.cedarschema.snap` | 355 | 9f2c46d0 | P |
| `cedar-policy-core/src/validator/schema/snapshots/cedar_policy_core__validator__schema__to_json__tests__roundtrip_schemas@extension_types.cedarschema.snap` | 282 | dedd0511 | P |
| `cedar-policy-core/src/validator/schema/snapshots/cedar_policy_core__validator__schema__to_json__tests__roundtrip_schemas@mixed_declarations.cedarschema.snap` | 657 | 7c983e60 | P |
| `cedar-policy-core/src/validator/schema/snapshots/cedar_policy_core__validator__schema__to_json__tests__roundtrip_schemas@mixed_required_optional.cedarschema.snap` | 349 | 9cbf13c8 | P |
| `cedar-policy-core/src/validator/schema/snapshots/cedar_policy_core__validator__schema__to_json__tests__roundtrip_schemas@multiple_actions_declared_together.cedarschema.snap` | 663 | e0ebb89a | P |
| `cedar-policy-core/src/validator/schema/snapshots/cedar_policy_core__validator__schema__to_json__tests__roundtrip_schemas@multiple_entities_declared_together.cedarschema.snap` | 572 | 3b94cbfb | P |
| `cedar-policy-core/src/validator/schema/snapshots/cedar_policy_core__validator__schema__to_json__tests__roundtrip_schemas@multiple_namespaces.cedarschema.snap` | 464 | 4de72b88 | P |
| `cedar-policy-core/src/validator/schema/snapshots/cedar_policy_core__validator__schema__to_json__tests__roundtrip_schemas@namespaced_entities.cedarschema.snap` | 351 | af4e16d6 | P |
| `cedar-policy-core/src/validator/schema/snapshots/cedar_policy_core__validator__schema__to_json__tests__roundtrip_schemas@optional_attributes.cedarschema.snap` | 270 | 5baa3b35 | P |
| `cedar-policy-core/src/validator/schema/snapshots/cedar_policy_core__validator__schema__to_json__tests__roundtrip_schemas@shadowed_entity_and_common.cedarschema.snap` | 640 | 0e2df9d4 | P |
| `cedar-policy-core/src/validator/schema/snapshots/cedar_policy_core__validator__schema__to_json__tests__roundtrip_schemas@shadowed_extension.cedarschema.snap` | 717 | c4636d85 | P |
| `cedar-policy-core/src/validator/schema/snapshots/cedar_policy_core__validator__schema__to_json__tests__roundtrip_schemas@shadowed_extension_as_entity.cedarschema.snap` | 742 | fcab8711 | P |
| `cedar-policy-core/src/validator/schema/snapshots/cedar_policy_core__validator__schema__to_json__tests__roundtrip_schemas@shadowed_primitive.cedarschema.snap` | 629 | 89c82818 | P |
| `cedar-policy-core/src/validator/schema/test_579.rs` | 71781 | 060cc614 | P |
| `cedar-policy-core/src/validator/schema/to_json.rs` | 14312 | 9ede6b04 | P |
| `cedar-policy-core/src/validator/str_checks.rs` | 11912 | c028f4e0 | P |
| `cedar-policy-core/src/validator/typecheck.rs` | 125195 | 75972254 | P |
| `cedar-policy-core/src/validator/typecheck/test.rs` | 961 | 78d7e4a9 | P |
| `cedar-policy-core/src/validator/typecheck/test/expr.rs` | 66549 | 00713314 | T |
| `cedar-policy-core/src/validator/typecheck/test/extensions.rs` | 17929 | 82651218 | T |
| `cedar-policy-core/src/validator/typecheck/test/namespace.rs` | 40886 | f9e57588 | T |
| `cedar-policy-core/src/validator/typecheck/test/optional_attributes.rs` | 19465 | 49cc86f8 | T |
| `cedar-policy-core/src/validator/typecheck/test/partial.rs` | 23152 | baf19e9a | T |
| `cedar-policy-core/src/validator/typecheck/test/policy.rs` | 52566 | 908999a5 | T |
| `cedar-policy-core/src/validator/typecheck/test/strict.rs` | 23850 | 1024ec9a | T |
| `cedar-policy-core/src/validator/typecheck/test/tags.rs` | 18023 | 0f94fca0 | T |
| `cedar-policy-core/src/validator/typecheck/test/test_utils.rs` | 20235 | d16ad383 | T |
| `cedar-policy-core/src/validator/typecheck/test/type_annotation.rs` | 12912 | 4070ff0b | T |
| `cedar-policy-core/src/validator/typecheck/test/unspecified_entity.rs` | 1556 | 458e21bf | T |
| `cedar-policy-core/src/validator/typecheck/typecheck_answer.rs` | 8265 | 946f0957 | P |
| `cedar-policy-core/src/validator/types.rs` | 97145 | ab5be24a | P |
| `cedar-policy-core/src/validator/types/capability.rs` | 4344 | f20e44cc | P |
| `cedar-policy-core/src/validator/types/request_env.rs` | 8375 | 9cd5328d | P |
| `cedar-policy-formatter/Cargo.toml` | 794 | 630a71a5 | P |
| `cedar-policy-formatter/README.md` | 2279 | dba64d16 | P |
| `cedar-policy-formatter/src/lib.rs` | 665 | 7d97ac5e | P |
| `cedar-policy-formatter/src/pprint/config.rs` | 1071 | 7d6ba9c2 | P |
| `cedar-policy-formatter/src/pprint/doc.rs` | 40158 | d71f2051 | P |
| `cedar-policy-formatter/src/pprint/fmt.rs` | 12711 | c82cbdf3 | P |
| `cedar-policy-formatter/src/pprint/lexer.rs` | 3056 | 0e342c09 | P |
| `cedar-policy-formatter/src/pprint/mod.rs` | 706 | 587230bc | P |
| `cedar-policy-formatter/src/pprint/token.rs` | 8821 | a5f5c540 | P |
| `cedar-policy-formatter/src/pprint/utils.rs` | 8046 | ac9a6b5b | P |
| `cedar-policy/Cargo.toml` | 3907 | 70a4797a | P |
| `cedar-policy/README.md` | 3898 | 3e47da5a | P |
| `cedar-policy/build.rs` | 1296 | 44b2c516 | P |
| `cedar-policy/experimental_warning.md` | 255 | fcd98d84 | P |
| `cedar-policy/protobuf_schema/core.proto` | 6929 | 1cf6fcad | P |
| `cedar-policy/protobuf_schema/validator.proto` | 2691 | 49e375ea | P |
| `cedar-policy/src/api.rs` | 245126 | e4b8e053 | P |
| `cedar-policy/src/api/deprecated_schema_compat.rs` | 42887 | 54644536 | P |
| `cedar-policy/src/api/err.rs` | 58371 | 1c1b1e1d | P |
| `cedar-policy/src/api/err/validation_errors.rs` | 2965 | 1a83d91b | P |
| `cedar-policy/src/api/err/validation_warnings.rs` | 2455 | 2c44457b | P |
| `cedar-policy/src/api/id.rs` | 15342 | b4697049 | P |
| `cedar-policy/src/api/tpe.rs` | 127736 | 0335586b | P |
| `cedar-policy/src/ffi/check_parse.rs` | 36701 | e7302f58 | P |
| `cedar-policy/src/ffi/completeness.rs` | 10794 | 8710d608 | P |
| `cedar-policy/src/ffi/convert.rs` | 39040 | 2ad4e28f | P |
| `cedar-policy/src/ffi/format.rs` | 6821 | 36c9e3c5 | P |
| `cedar-policy/src/ffi/is_authorized.rs` | 76597 | 7418a267 | P |
| `cedar-policy/src/ffi/link.rs` | 12867 | 15a6dc1e | P |
| `cedar-policy/src/ffi/mod.rs` | 928 | 9ff2460e | P |
| `cedar-policy/src/ffi/snapshots/cedar_policy__ffi__convert__test__schema_resolution_round_trip@action_entity_ref.snap` | 1429 | 70006a2f | P |
| `cedar-policy/src/ffi/snapshots/cedar_policy__ffi__convert__test__schema_resolution_round_trip@action_hierarchy.snap` | 952 | 108d8d27 | P |
| `cedar-policy/src/ffi/snapshots/cedar_policy__ffi__convert__test__schema_resolution_round_trip@action_no_applies_to.snap` | 340 | 64b5cd4e | P |
| `cedar-policy/src/ffi/snapshots/cedar_policy__ffi__convert__test__schema_resolution_round_trip@action_with_context.snap` | 689 | 7f72ea1c | P |
| `cedar-policy/src/ffi/snapshots/cedar_policy__ffi__convert__test__schema_resolution_round_trip@app_document.snap` | 834 | a08f312c | P |
| `cedar-policy/src/ffi/snapshots/cedar_policy__ffi__convert__test__schema_resolution_round_trip@basic_action.snap` | 408 | 01f9f417 | P |
| `cedar-policy/src/ffi/snapshots/cedar_policy__ffi__convert__test__schema_resolution_round_trip@basic_entity.snap` | 224 | 0e528be3 | P |
| `cedar-policy/src/ffi/snapshots/cedar_policy__ffi__convert__test__schema_resolution_round_trip@common_types.snap` | 969 | be419bf3 | P |
| `cedar-policy/src/ffi/snapshots/cedar_policy__ffi__convert__test__schema_resolution_round_trip@complex_common_types.snap` | 1831 | 9640468c | P |
| `cedar-policy/src/ffi/snapshots/cedar_policy__ffi__convert__test__schema_resolution_round_trip@complex_types.snap` | 869 | f3fc83a5 | P |
| `cedar-policy/src/ffi/snapshots/cedar_policy__ffi__convert__test__schema_resolution_round_trip@comprehensive_schema.snap` | 6989 | d01b71ab | P |
| `cedar-policy/src/ffi/snapshots/cedar_policy__ffi__convert__test__schema_resolution_round_trip@cross_namespace_references.snap` | 1251 | ca9df575 | P |
| `cedar-policy/src/ffi/snapshots/cedar_policy__ffi__convert__test__schema_resolution_round_trip@deeply_nested_records.snap` | 1572 | 1d4b3d28 | P |
| `cedar-policy/src/ffi/snapshots/cedar_policy__ffi__convert__test__schema_resolution_round_trip@empty_schema.snap` | 148 | c64432a2 | P |
| `cedar-policy/src/ffi/snapshots/cedar_policy__ffi__convert__test__schema_resolution_round_trip@entity_hierarchy.snap` | 394 | 6ce65752 | P |
| `cedar-policy/src/ffi/snapshots/cedar_policy__ffi__convert__test__schema_resolution_round_trip@entity_references.snap` | 747 | 0d1c0a5b | P |
| `cedar-policy/src/ffi/snapshots/cedar_policy__ffi__convert__test__schema_resolution_round_trip@entity_tags.snap` | 931 | cabd4b01 | P |
| `cedar-policy/src/ffi/snapshots/cedar_policy__ffi__convert__test__schema_resolution_round_trip@entity_with_attributes.snap` | 563 | 32dc3050 | P |
| `cedar-policy/src/ffi/snapshots/cedar_policy__ffi__convert__test__schema_resolution_round_trip@enum_entities.snap` | 840 | 9dff157b | P |
| `cedar-policy/src/ffi/snapshots/cedar_policy__ffi__convert__test__schema_resolution_round_trip@extension_types.snap` | 595 | 79b0ee5f | P |
| `cedar-policy/src/ffi/snapshots/cedar_policy__ffi__convert__test__schema_resolution_round_trip@mixed_declarations.snap` | 2071 | 6f51b334 | P |
| `cedar-policy/src/ffi/snapshots/cedar_policy__ffi__convert__test__schema_resolution_round_trip@mixed_required_optional.snap` | 967 | 0de3b056 | P |
| `cedar-policy/src/ffi/snapshots/cedar_policy__ffi__convert__test__schema_resolution_round_trip@multiple_actions_declared_together.snap` | 1408 | 75780b66 | P |
| `cedar-policy/src/ffi/snapshots/cedar_policy__ffi__convert__test__schema_resolution_round_trip@multiple_entities_declared_together.snap` | 1108 | 3c5d48cb | P |
| `cedar-policy/src/ffi/snapshots/cedar_policy__ffi__convert__test__schema_resolution_round_trip@multiple_namespaces.snap` | 715 | 63a95c31 | P |
| `cedar-policy/src/ffi/snapshots/cedar_policy__ffi__convert__test__schema_resolution_round_trip@namespaced_entities.snap` | 612 | 44d89079 | P |
| `cedar-policy/src/ffi/snapshots/cedar_policy__ffi__convert__test__schema_resolution_round_trip@optional_attributes.snap` | 631 | 27f99227 | P |
| `cedar-policy/src/ffi/snapshots/cedar_policy__ffi__convert__test__schema_resolution_round_trip@shadowed_entity_and_common.snap` | 1496 | 4ec77ed7 | P |
| `cedar-policy/src/ffi/snapshots/cedar_policy__ffi__convert__test__schema_resolution_round_trip@shadowed_extension.snap` | 2173 | 797ed143 | P |
| `cedar-policy/src/ffi/snapshots/cedar_policy__ffi__convert__test__schema_resolution_round_trip@shadowed_extension_as_entity.snap` | 2264 | c1c1c19c | P |
| `cedar-policy/src/ffi/snapshots/cedar_policy__ffi__convert__test__schema_resolution_round_trip@shadowed_primitive.snap` | 2238 | 46a41156 | P |
| `cedar-policy/src/ffi/test_schemas/action_entity_ref.cedarschema` | 210 | 244c08cc | P |
| `cedar-policy/src/ffi/test_schemas/action_hierarchy.cedarschema` | 237 | c24ce640 | P |
| `cedar-policy/src/ffi/test_schemas/action_no_applies_to.cedarschema` | 19 | 68b99fb1 | P |
| `cedar-policy/src/ffi/test_schemas/action_with_context.cedarschema` | 172 | d09c212d | P |
| `cedar-policy/src/ffi/test_schemas/app_document.cedarschema` | 239 | d0a3b563 | P |
| `cedar-policy/src/ffi/test_schemas/basic_action.cedarschema` | 101 | 22b741e5 | P |
| `cedar-policy/src/ffi/test_schemas/basic_entity.cedarschema` | 13 | 065309f4 | P |
| `cedar-policy/src/ffi/test_schemas/common_types.cedarschema` | 263 | 17dca3db | P |
| `cedar-policy/src/ffi/test_schemas/complex_common_types.cedarschema` | 552 | 1ed8a2f4 | P |
| `cedar-policy/src/ffi/test_schemas/complex_types.cedarschema` | 157 | 5c67a7f9 | P |
| `cedar-policy/src/ffi/test_schemas/comprehensive_schema.cedarschema` | 1158 | 883aa858 | P |
| `cedar-policy/src/ffi/test_schemas/cross_namespace_references.cedarschema` | 369 | 38930b51 | P |
| `cedar-policy/src/ffi/test_schemas/deeply_nested_records.cedarschema` | 359 | b5c7c79d | P |
| `cedar-policy/src/ffi/test_schemas/empty_schema.cedarschema` | 1 | 8b137891 | P |
| `cedar-policy/src/ffi/test_schemas/entity_hierarchy.cedarschema` | 67 | b27bc4f5 | P |
| `cedar-policy/src/ffi/test_schemas/entity_references.cedarschema` | 114 | b1c81211 | P |
| `cedar-policy/src/ffi/test_schemas/entity_tags.cedarschema` | 203 | e7cc3022 | P |
| `cedar-policy/src/ffi/test_schemas/entity_with_attributes.cedarschema` | 102 | d41b762a | P |
| `cedar-policy/src/ffi/test_schemas/enum_entities.cedarschema` | 199 | d6748641 | P |
| `cedar-policy/src/ffi/test_schemas/extension_types.cedarschema` | 93 | 710e1b31 | P |
| `cedar-policy/src/ffi/test_schemas/mixed_declarations.cedarschema` | 382 | b2a9ee5c | P |
| `cedar-policy/src/ffi/test_schemas/mixed_required_optional.cedarschema` | 196 | 4f93745c | P |
| `cedar-policy/src/ffi/test_schemas/multiple_actions_declared_together.cedarschema` | 259 | 384784a9 | P |
| `cedar-policy/src/ffi/test_schemas/multiple_entities_declared_together.cedarschema` | 195 | 219b1ac0 | P |
| `cedar-policy/src/ffi/test_schemas/multiple_namespaces.cedarschema` | 303 | 27099183 | P |
| `cedar-policy/src/ffi/test_schemas/namespaced_entities.cedarschema` | 188 | add90894 | P |
| `cedar-policy/src/ffi/test_schemas/optional_attributes.cedarschema` | 109 | 5323038f | P |
| `cedar-policy/src/ffi/test_schemas/shadowed_entity_and_common.cedarschema` | 364 | 1b48cfad | P |
| `cedar-policy/src/ffi/test_schemas/shadowed_extension.cedarschema` | 643 | f5b93252 | P |
| `cedar-policy/src/ffi/test_schemas/shadowed_extension_as_entity.cedarschema` | 645 | 45dc6e68 | P |
| `cedar-policy/src/ffi/test_schemas/shadowed_primitive.cedarschema` | 578 | 433d173c | P |
| `cedar-policy/src/ffi/tests.rs` | 4460 | eb03db42 | T |
| `cedar-policy/src/ffi/utils.rs` | 46248 | 10f2faec | P |
| `cedar-policy/src/ffi/validate.rs` | 26282 | 575c6dc7 | P |
| `cedar-policy/src/ffi/version.rs` | 483 | 6fee0bac | P |
| `cedar-policy/src/lib.rs` | 4417 | dbc44d57 | P |
| `cedar-policy/src/proto.rs` | 2033 | 3abf1060 | P |
| `cedar-policy/src/proto/api.rs` | 42475 | 149622ee | P |
| `cedar-policy/src/proto/ast.rs` | 55437 | af6d920b | P |
| `cedar-policy/src/proto/entities.rs` | 4526 | 9e4b9e40 | P |
| `cedar-policy/src/proto/policy.rs` | 56937 | 2b96ebb0 | P |
| `cedar-policy/src/proto/test_utils.rs` | 11958 | d9f19f37 | P |
| `cedar-policy/src/proto/traits.rs` | 23729 | b9bdc6a6 | P |
| `cedar-policy/src/proto/validator.rs` | 37729 | adb6aab3 | P |
| `cedar-policy/src/test.rs` | 803 | c82dabed | P |
| `cedar-policy/src/test/prop_test_policy_set.rs` | 14767 | ced2119a | T |
| `cedar-policy/src/test/test.rs` | 474651 | 79c858c8 | T |
| `deny.toml` | 984 | cd37a692 | P |

</details>


---

<!-- SECTION:D12a -->
## D12a. Agent Client Protocol schema (`agentclientprotocol/agent-client-protocol`)

Canonical ACP JSON schema (v1 stable, v2 draft) and the Rust schema crate generated from it. Matrix row D12.

* Upstream: `agentclientprotocol/agent-client-protocol@e50f62b4a1ca8d794a4c97210acd8a0d833b05c5`.
* Zain destination: Rust types: crates.io dependency `agent-client-protocol-schema = "=1.12.0"` in `crates/contracts`; JSON schema files copied as conformance fixtures into `crates/contracts/acp/schema/` and used to regenerate the T3 `packages/effect-acp` bindings.
* Copy mode: **DEPEND-ON-PACKAGE for the crate; COPY AS-IS for `schema/v1/*` and `schema/v2/*` JSON fixtures**
* Selected surface: **51 files, 3,111,464 bytes** (2 test). Spec prose `docs/protocol` (79 files, 1,906,084 B) and `docs/rfds` (51 files) are REFERENCE only and are not selected.
* Internal imports outside the selected set: none for the crate (`agent-client-protocol-schema/Cargo.toml` has no path dependencies). `schema-generator` is the build tool that produces `schema/*` from the crate and is not needed to consume the artefacts.
* Crate `agent-client-protocol-schema` 1.12.0: edition 2024, rust-version 1.88.0 (so the Zain Rust toolchain must be at least 1.88.0). Features: `unstable`, `unstable_protocol_v2`, `unstable_llm_providers`, `unstable_mcp_over_acp`, `unstable_plan_operations`, `unstable_session_fork`, `unstable_session_system_prompt`, `unstable_subagents`, `unstable_end_turn_token_usage`. External dependencies:

| crate | declared | kind | optional | latest on crates.io | license |
|---|---|---|---|---|---|
| anyhow | 1 | runtime | no | 1.0.104 | MIT OR Apache-2.0 |
| derive_more | 2 | runtime | no | 2.1.1 | MIT |
| schemars | 1 | runtime | yes | 1.2.3 | MIT |
| serde | 1 | runtime | no | 1.0.229 | MIT OR Apache-2.0 |
| serde_json | 1 | runtime | no | 1.0.154 | MIT OR Apache-2.0 |
| serde_with | 3.20.0 | runtime | no | 3.24.0 | MIT OR Apache-2.0 |
| strum | 0.28 | runtime | no | 0.28.0 | MIT |

* License and NOTICE: Apache-2.0 (`LICENSE` 10,782 B); crate authors field is `Zed <hi@zed.dev>`; no NOTICE file in the tree. Carry the LICENSE text and the Zed Industries attribution in Zain third-party notices.
* Risks: (1) v2 is a parallel module with a different wire version and is NOT part of the `unstable` umbrella (Cargo.toml comment): never enable it implicitly. (2) Weekly releases (1.10.2 on 2026-10-01, 1.11.0 on 2026-10-09, 1.12.0 on 2026-10-16). (3) Unstable flags can be removed without notice. (4) T3 already carries generated bindings (`packages/effect-acp`, 24,734 LOC mostly generated, R02 line 98): two generated copies of one schema must not drift, so regenerate T3 from the pinned `schema/v1/schema.json` and record the SHA in PROVENANCE.
* Qualification tests: Positive: round-trip every example message through the Rust types and through effect-acp; validate fixtures against the JSON schema. Negative: an unknown method yields JSON-RPC -32601; malformed JSON and an oversized frame are rejected without panic; a v1 client against a v2 agent negotiates down or fails with a clear error; extension payloads (`raw_value`) never execute; `fs/write_text_file` outside the workspace root is denied by the Zain client policy (R02 `clientPolicy.ts`).

<details><summary>File list with blob sizes</summary>

| path | B | blob | k |
|---|---:|---|---|
| `Cargo.toml` | 798 | 1929e2ac | P |
| `LICENSE` | 10782 | 1de02305 | P |
| `agent-client-protocol-schema/Cargo.toml` | 2382 | f13f6f73 | P |
| `agent-client-protocol-schema/src/lib.rs` | 3148 | 8d765aee | P |
| `agent-client-protocol-schema/src/rpc.rs` | 8162 | 207a8d0a | P |
| `agent-client-protocol-schema/src/serde_util.rs` | 35884 | 20d9dd95 | P |
| `agent-client-protocol-schema/src/v1/agent.rs` | 276510 | 31a4b24e | P |
| `agent-client-protocol-schema/src/v1/client.rs` | 219817 | bf266fe0 | P |
| `agent-client-protocol-schema/src/v1/content.rs` | 30570 | 939c55ad | P |
| `agent-client-protocol-schema/src/v1/elicitation.rs` | 106780 | 1e25e161 | P |
| `agent-client-protocol-schema/src/v1/error.rs` | 12389 | 53ccc594 | P |
| `agent-client-protocol-schema/src/v1/ext.rs` | 3825 | 592e20e4 | P |
| `agent-client-protocol-schema/src/v1/mcp.rs` | 17488 | 724b5a26 | P |
| `agent-client-protocol-schema/src/v1/mod.rs` | 1447 | 007e8da4 | P |
| `agent-client-protocol-schema/src/v1/plan.rs` | 20486 | 4382ed86 | P |
| `agent-client-protocol-schema/src/v1/protocol_level.rs` | 4619 | 715c9bcf | P |
| `agent-client-protocol-schema/src/v1/rpc.rs` | 5443 | 82997397 | P |
| `agent-client-protocol-schema/src/v1/tool_call.rs` | 31028 | a9019a80 | P |
| `agent-client-protocol-schema/src/v2/agent.rs` | 311987 | 2c60ae37 | P |
| `agent-client-protocol-schema/src/v2/client.rs` | 221361 | 3020c5e8 | P |
| `agent-client-protocol-schema/src/v2/content.rs` | 45278 | 605829e1 | P |
| `agent-client-protocol-schema/src/v2/elicitation.rs` | 109217 | 9859178d | P |
| `agent-client-protocol-schema/src/v2/error.rs` | 14057 | 163da2e5 | P |
| `agent-client-protocol-schema/src/v2/ext.rs` | 7769 | e2c2bbd6 | P |
| `agent-client-protocol-schema/src/v2/mcp.rs` | 15770 | 75b19d57 | P |
| `agent-client-protocol-schema/src/v2/mod.rs` | 6305 | 2461890b | P |
| `agent-client-protocol-schema/src/v2/plan.rs` | 23010 | 1fbd9bfb | P |
| `agent-client-protocol-schema/src/v2/protocol_level.rs` | 4618 | bc511931 | P |
| `agent-client-protocol-schema/src/v2/rpc.rs` | 4795 | b2a34849 | P |
| `agent-client-protocol-schema/src/v2/schema_util.rs` | 721 | 8bab35ec | P |
| `agent-client-protocol-schema/src/v2/terminal.rs` | 23540 | 1ad5442b | P |
| `agent-client-protocol-schema/src/v2/tool_call.rs` | 55918 | 6d12d711 | P |
| `agent-client-protocol-schema/src/version.rs` | 3244 | 95fe0b73 | P |
| `agent-client-protocol-schema/tests/compaction.rs` | 23746 | 86aacd98 | T |
| `agent-client-protocol-schema/tests/experimental_compatibility.rs` | 4499 | 5b61e1f9 | T |
| `schema-generator/Cargo.toml` | 656 | 9ce07c59 | P |
| `schema-generator/src/main.rs` | 121773 | 362a1fc1 | P |
| `schema/v1/CHANGELOG.md` | 7979 | 71d45811 | P |
| `schema/v1/Cargo.toml` | 493 | f1185bb4 | P |
| `schema/v1/meta.json` | 1159 | b9c67caa | P |
| `schema/v1/meta.unstable.json` | 1387 | 2b1222e5 | P |
| `schema/v1/schema.json` | 255675 | 8c8377d9 | P |
| `schema/v1/schema.unstable.json` | 337850 | 7d2d35fd | P |
| `schema/v1/src/lib.rs` | 84 | 4ba76e08 | P |
| `schema/v2/CHANGELOG.md` | 6996 | 21d64e59 | P |
| `schema/v2/Cargo.toml` | 494 | c453cb0d | P |
| `schema/v2/meta.json` | 769 | ad2cfd93 | P |
| `schema/v2/meta.unstable.json` | 997 | 1b4813ad | P |
| `schema/v2/schema.json` | 319086 | dbd09e61 | P |
| `schema/v2/schema.unstable.json` | 388586 | 3a580ac2 | P |
| `schema/v2/src/lib.rs` | 87 | 4b32544a | P |

</details>


---

<!-- SECTION:D12b -->
## D12b. Agent Client Protocol Rust SDK (`agentclientprotocol/rust-sdk`)

Rust host and agent implementation of ACP (transports, derive macros, test harness, conductor and proxy chains). Matrix row D12.

* Upstream: `agentclientprotocol/rust-sdk@644377ad2654415c76c979c795d6c568e17a6d62`.
* Zain destination: `crates/core/Cargo.toml` dependency `agent-client-protocol = "=3.5.0"` (features `stdio`, `process` only); `agent-client-protocol-test` as dev-dependency.
* Copy mode: **DEPEND-ON-PACKAGE (crates.io `agent-client-protocol` 3.5.0, published 2026-10-22, Apache-2.0)**
* Selected surface: **128 files, 2,431,507 bytes** (54 test/example). Not selected: `agent-client-protocol-conductor` (36 files), `-http` (13), `-polyfill` (7), `-rmcp` (11), `-cookbook` (5), `-trace-viewer` (6), `yopo` (4) and the `md/` book (about 40 migration and design notes, REFERENCE: `md/protocol-v2.md` 33,765 B, `md/migration-v3.md`).
* Internal imports outside the selected set: `agent-client-protocol` depends on the workspace crates `agent-client-protocol-schema` (separate crates.io release, see D12a) and `agent-client-protocol-derive` (in the selected set).
* External dependencies (core and derive crates, workspace-resolved; optional native transports `async-io`, `async-process`, `blocking`, `shell-words`, `rustix` on unix, `windows-sys` on Windows):

| crate | declared | kind | optional | latest on crates.io | license |
|---|---|---|---|---|---|
| async-io | 2 | runtime/target | yes | 2.6.0 | Apache-2.0 OR MIT |
| async-process | 2 | runtime/target | yes | 2.5.0 | Apache-2.0 OR MIT |
| blocking | 1 | runtime/target | yes | 1.7.0 | Apache-2.0 OR MIT |
| futures | 0.3.32 | runtime | no | 0.3.34 | MIT OR Apache-2.0 |
| futures-concurrency | 7.6.3 | runtime | no | 7.7.1 | MIT OR Apache-2.0 |
| quote | 1 | runtime | no | 1.0.47 | MIT OR Apache-2.0 |
| rustc-hash | 2.1.1 | runtime | no | 2.1.3 | Apache-2.0 OR MIT |
| rustix | 1 | runtime/target | yes | 1.1.6 | Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT |
| schemars | 1.0 | runtime | yes | 1.2.3 | MIT |
| serde | 1.0 | runtime | no | 1.0.229 | MIT OR Apache-2.0 |
| serde_json | 1 | runtime | no | 1.0.154 | MIT OR Apache-2.0 |
| shell-words | 1.1 | runtime/target | yes | 1.1.1 | MIT/Apache-2.0 |
| syn | 3 | runtime | no | 3.0.9 | MIT OR Apache-2.0 |
| tracing | 0.1 | runtime | no | 0.1.44 | MIT |
| uuid | 1.18 | runtime | no | 1.29.0 | Apache-2.0 OR MIT |
| windows-sys | 0.61 | runtime/target | yes | 0.61.2 | MIT OR Apache-2.0 |

* License and NOTICE: Apache-2.0 (`LICENSE` 10,783 B, workspace `license-file`); no NOTICE in the tree.
* Risks: (1) Rapid major churn: 3.3.0 (2026-10-09), 3.4.0 (2026-10-16), 3.5.0 (2026-10-22), with migration notes `md/migration_v2.0.md` (21,403 B) and `md/migration-v3.md`. (2) Feature `process` spawns child agents: an arbitrary-command effect that must go through Core. (3) The `unstable_protocol_v2` feature must stay off. (4) T3 speaks ACP through its own TypeScript client; Rust Core uses this crate only if Core itself hosts an agent connection (07 decides).
* Qualification tests: Positive: crate test suites via `agent-client-protocol-test`; the `simple_agent` and `yolo_one_shot_client` examples as smoke tests. Negative: a child agent that never answers `initialize` is killed after the timeout; a request cancelled mid-flight produces no late side effect (`md/request-cancellation.md`); stdout noise from the child is not parsed as protocol; spawn of a binary outside the allowlist is denied by Core.

<details><summary>File list with blob sizes</summary>

| path | B | blob | k |
|---|---:|---|---|
| `Cargo.toml` | 4303 | 432f96a6 | P |
| `LICENSE` | 10783 | c24b0535 | P |
| `src/agent-client-protocol-derive/CHANGELOG.md` | 3717 | 0e0d3308 | P |
| `src/agent-client-protocol-derive/Cargo.toml` | 412 | e10d89c7 | P |
| `src/agent-client-protocol-derive/README.md` | 1425 | 7e91b640 | P |
| `src/agent-client-protocol-derive/src/lib.rs` | 16653 | b46ab4ee | P |
| `src/agent-client-protocol-test/CHANGELOG.md` | 1545 | 31a290d7 | P |
| `src/agent-client-protocol-test/Cargo.toml` | 1255 | 6c376988 | P |
| `src/agent-client-protocol-test/examples/arrow_proxy.rs` | 867 | bd425f86 | T |
| `src/agent-client-protocol-test/src/arrow_proxy.rs` | 2111 | 9210cf05 | P |
| `src/agent-client-protocol-test/src/bin/mcp_echo_server.rs` | 2351 | ed089b19 | P |
| `src/agent-client-protocol-test/src/bin/testy.rs` | 545 | 989eaae2 | P |
| `src/agent-client-protocol-test/src/lib.rs` | 6577 | 39655e5a | P |
| `src/agent-client-protocol-test/src/test_binaries.rs` | 2593 | a8d938a9 | P |
| `src/agent-client-protocol-test/src/testy.rs` | 78595 | 14da8590 | P |
| `src/agent-client-protocol-test/src/testy/v2.rs` | 21424 | 60ad5e7d | P |
| `src/agent-client-protocol-test/tests/testy.rs` | 92421 | 16473e71 | T |
| `src/agent-client-protocol-test/tests/testy_v2.rs` | 17240 | 4080dba3 | T |
| `src/agent-client-protocol/CHANGELOG.md` | 39331 | a8de476f | P |
| `src/agent-client-protocol/Cargo.toml` | 3709 | c914a41c | P |
| `src/agent-client-protocol/README.md` | 9023 | c240b595 | P |
| `src/agent-client-protocol/examples/simple_agent.rs` | 765 | 319bf4bd | T |
| `src/agent-client-protocol/examples/simple_agent_v2.rs` | 18128 | 1dc64932 | T |
| `src/agent-client-protocol/examples/v2_one_shot_client.rs` | 15009 | 2e90bfb6 | T |
| `src/agent-client-protocol/examples/v2_session_coordination.rs` | 17720 | 2831601a | T |
| `src/agent-client-protocol/examples/v2_session_coordination/tests.rs` | 20388 | a8a8aea7 | T |
| `src/agent-client-protocol/examples/yolo_one_shot_client.rs` | 4329 | 2965a05b | T |
| `src/agent-client-protocol/src/acp_agent.rs` | 57372 | 0c607c95 | P |
| `src/agent-client-protocol/src/capabilities.rs` | 7425 | 1718f082 | P |
| `src/agent-client-protocol/src/component.rs` | 25581 | 5d02883c | P |
| `src/agent-client-protocol/src/concepts/acp_basics.rs` | 2667 | d0f2a6b3 | P |
| `src/agent-client-protocol/src/concepts/callbacks.rs` | 5116 | 5e2d7b01 | P |
| `src/agent-client-protocol/src/concepts/cancellation.rs` | 12866 | f06f92ca | P |
| `src/agent-client-protocol/src/concepts/connections.rs` | 9217 | 98a89ac7 | P |
| `src/agent-client-protocol/src/concepts/error_handling.rs` | 4388 | 4287158f | P |
| `src/agent-client-protocol/src/concepts/mod.rs` | 1744 | 4e5f3d97 | P |
| `src/agent-client-protocol/src/concepts/ordering.rs` | 8975 | a204a995 | P |
| `src/agent-client-protocol/src/concepts/peers.rs` | 3773 | 7c7dbcf9 | P |
| `src/agent-client-protocol/src/concepts/proxies.rs` | 8577 | b2d1d032 | P |
| `src/agent-client-protocol/src/concepts/sessions.rs` | 9886 | 5fdb931e | P |
| `src/agent-client-protocol/src/jsonrpc.rs` | 347937 | ce972c5d | P |
| `src/agent-client-protocol/src/jsonrpc/close.rs` | 3406 | 1111d718 | P |
| `src/agent-client-protocol/src/jsonrpc/dynamic_handler.rs` | 2232 | fb04c8f8 | P |
| `src/agent-client-protocol/src/jsonrpc/handlers.rs` | 19542 | 17b683aa | P |
| `src/agent-client-protocol/src/jsonrpc/incoming_actor.rs` | 29562 | 26ee41e4 | P |
| `src/agent-client-protocol/src/jsonrpc/outgoing_actor.rs` | 10128 | 35edb6e4 | P |
| `src/agent-client-protocol/src/jsonrpc/prepared_request_tests.rs` | 24157 | 223d4b18 | T |
| `src/agent-client-protocol/src/jsonrpc/protocol_compat.rs` | 84112 | 26edba6e | P |
| `src/agent-client-protocol/src/jsonrpc/raw_error.rs` | 8371 | 1b25324f | P |
| `src/agent-client-protocol/src/jsonrpc/run.rs` | 7445 | 9b3b28de | P |
| `src/agent-client-protocol/src/jsonrpc/task_actor.rs` | 2917 | 33f43a62 | P |
| `src/agent-client-protocol/src/jsonrpc/termination.rs` | 5611 | ff1fdf09 | P |
| `src/agent-client-protocol/src/jsonrpc/transport_actor.rs` | 22411 | 806e7da2 | P |
| `src/agent-client-protocol/src/lib.rs` | 12415 | ad4f37ab | P |
| `src/agent-client-protocol/src/line_direction.rs` | 329 | cf7e5c4c | P |
| `src/agent-client-protocol/src/mcp_server/active_session.rs` | 37550 | 7288a3e5 | P |
| `src/agent-client-protocol/src/mcp_server/connect.rs` | 2884 | 170be44f | P |
| `src/agent-client-protocol/src/mcp_server/context.rs` | 4961 | 007714fd | P |
| `src/agent-client-protocol/src/mcp_server/mod.rs` | 3562 | 045bb1d6 | P |
| `src/agent-client-protocol/src/mcp_server/registry.rs` | 10195 | c012edcc | P |
| `src/agent-client-protocol/src/mcp_server/server.rs` | 24968 | 5341f56a | P |
| `src/agent-client-protocol/src/mcp_server/service.rs` | 6036 | 0bb488b6 | P |
| `src/agent-client-protocol/src/mcp_server/tool.rs` | 2191 | 7690451c | P |
| `src/agent-client-protocol/src/mcp_server/tool_fn.rs` | 26109 | 556b3565 | P |
| `src/agent-client-protocol/src/role.rs` | 10746 | 76e3a7f9 | P |
| `src/agent-client-protocol/src/role/acp.rs` | 85834 | 8e696e2d | P |
| `src/agent-client-protocol/src/role/mcp.rs` | 2397 | f33a35e5 | P |
| `src/agent-client-protocol/src/schema/agent_to_client/mod.rs` | 77 | 2af4bcf2 | P |
| `src/agent-client-protocol/src/schema/agent_to_client/notifications.rs` | 253 | 0484765e | P |
| `src/agent-client-protocol/src/schema/agent_to_client/requests.rs` | 1463 | d3b0ae19 | P |
| `src/agent-client-protocol/src/schema/client_to_agent/mod.rs` | 77 | b150749b | P |
| `src/agent-client-protocol/src/schema/client_to_agent/notifications.rs` | 110 | c1a27a4e | P |
| `src/agent-client-protocol/src/schema/client_to_agent/requests.rs` | 2474 | 46b4f10b | P |
| `src/agent-client-protocol/src/schema/enum_impls.rs` | 4334 | e485e868 | P |
| `src/agent-client-protocol/src/schema/mcp.rs` | 311 | e5c5032d | P |
| `src/agent-client-protocol/src/schema/mod.rs` | 13077 | 53ae1c81 | P |
| `src/agent-client-protocol/src/schema/protocol_level.rs` | 369 | c80eb7c3 | P |
| `src/agent-client-protocol/src/schema/proxy_protocol.rs` | 3580 | b9976db4 | P |
| `src/agent-client-protocol/src/schema/v2_impls.rs` | 12511 | 94d849e8 | P |
| `src/agent-client-protocol/src/session.rs` | 51913 | f300f92a | P |
| `src/agent-client-protocol/src/session/v2.rs` | 34597 | 5590131c | P |
| `src/agent-client-protocol/src/stdio.rs` | 2882 | ec397be9 | P |
| `src/agent-client-protocol/src/util.rs` | 7932 | 01366525 | P |
| `src/agent-client-protocol/src/util/typed.rs` | 40778 | 86ab013c | P |
| `src/agent-client-protocol/tests/application_dispatch_v2.rs` | 8285 | 4a5d7244 | T |
| `src/agent-client-protocol/tests/connection_driver_normalization.rs` | 27072 | 8608b70e | T |
| `src/agent-client-protocol/tests/connection_termination.rs` | 8809 | 9dd4b94b | T |
| `src/agent-client-protocol/tests/cooperative_connection_driver.rs` | 30097 | f1eb7469 | T |
| `src/agent-client-protocol/tests/custom_role.rs` | 1038 | 4312772b | T |
| `src/agent-client-protocol/tests/derive_macros.rs` | 5663 | eecd1b02 | T |
| `src/agent-client-protocol/tests/jsonrpc_advanced.rs` | 27607 | 897bb212 | T |
| `src/agent-client-protocol/tests/jsonrpc_batch.rs` | 55460 | 97df192e | T |
| `src/agent-client-protocol/tests/jsonrpc_connection_builder.rs` | 26900 | b819bfa1 | T |
| `src/agent-client-protocol/tests/jsonrpc_deep_chain_stack.rs` | 7856 | 6cc5616d | T |
| `src/agent-client-protocol/tests/jsonrpc_edge_cases.rs` | 15300 | cc252d9a | T |
| `src/agent-client-protocol/tests/jsonrpc_error_handling.rs` | 39891 | eb2437eb | T |
| `src/agent-client-protocol/tests/jsonrpc_hello.rs` | 14476 | f454b7ef | T |
| `src/agent-client-protocol/tests/jsonrpc_request_cancellation.rs` | 97403 | 142e32b8 | T |
| `src/agent-client-protocol/tests/jsonrpc_transport_close.rs` | 60240 | 4d981aba | T |
| `src/agent-client-protocol/tests/jsonrpc_unhandled_messages.rs` | 20311 | 2c39b045 | T |
| `src/agent-client-protocol/tests/log_privacy.rs` | 8206 | 98a3a260 | T |
| `src/agent-client-protocol/tests/match_dispatch.rs` | 12878 | 3669a895 | T |
| `src/agent-client-protocol/tests/mcp_discovery.rs` | 5623 | a928390d | T |
| `src/agent-client-protocol/tests/mcp_factory.rs` | 9493 | b8e6361d | T |
| `src/agent-client-protocol/tests/mcp_message_deserialization.rs` | 4109 | ae9911ed | T |
| `src/agent-client-protocol/tests/meta_propagation.rs` | 4702 | 1e6c8744 | T |
| `src/agent-client-protocol/tests/native_mcp_shutdown.rs` | 6601 | 6c242681 | T |
| `src/agent-client-protocol/tests/prepared_requests.rs` | 26749 | 10fbb33a | T |
| `src/agent-client-protocol/tests/protocol_driver_finish.rs` | 14138 | d653dc2b | T |
| `src/agent-client-protocol/tests/protocol_negotiation.rs` | 8553 | 5486c996 | T |
| `src/agent-client-protocol/tests/protocol_v2.rs` | 113713 | 7231a8c0 | T |
| `src/agent-client-protocol/tests/proxy_protocol_router_v2.rs` | 10968 | bc43ce39 | T |
| `src/agent-client-protocol/tests/schema_1_11.rs` | 5133 | d6b9e90a | T |
| `src/agent-client-protocol/tests/schema_1_12.rs` | 3727 | c6363361 | T |
| `src/agent-client-protocol/tests/schema_elicitation.rs` | 9953 | 9da4c25f | T |
| `src/agent-client-protocol/tests/schema_generation.rs` | 703 | caaa3d57 | T |
| `src/agent-client-protocol/tests/schema_llm_providers.rs` | 11445 | f1ddaa36 | T |
| `src/agent-client-protocol/tests/schema_plan_operations.rs` | 3916 | 27f63272 | T |
| `src/agent-client-protocol/tests/schema_session_compaction.rs` | 4448 | c1c5c6f9 | T |
| `src/agent-client-protocol/tests/schema_session_delete.rs` | 1886 | 1aa50529 | T |
| `src/agent-client-protocol/tests/schema_subagents.rs` | 2540 | 868dba2c | T |
| `src/agent-client-protocol/tests/schema_tool_call_name.rs` | 3898 | 0cc36469 | T |
| `src/agent-client-protocol/tests/session_mcp_scope.rs` | 19147 | 2161d837 | T |
| `src/agent-client-protocol/tests/session_ordering.rs` | 32776 | 4931df67 | T |
| `src/agent-client-protocol/tests/session_restore.rs` | 20723 | c01875e0 | T |
| `src/agent-client-protocol/tests/session_runner_error_scope.rs` | 17335 | 7a218fd7 | T |
| `src/agent-client-protocol/tests/session_v2.rs` | 47407 | 3ce6cfcf | T |
| `src/agent-client-protocol/tests/session_v2_mcp.rs` | 48777 | ec321c62 | T |

</details>


---

<!-- SECTION:D12c -->
## D12c. Agent Client Protocol TypeScript SDK (`agentclientprotocol/typescript-sdk`)

TypeScript ACP client and agent library (npm `@agentclientprotocol/sdk` 2.0.2). Matrix row D12.

* Upstream: `agentclientprotocol/typescript-sdk@bca8e49199927e167fab74db4dd76dec4743bb49`.
* Zain destination: Only if a webview or script needs ACP directly; the server side uses the existing T3 `packages/effect-acp` (decision: no second ACP stack in `apps/server`). If adopted: `apps/web/package.json` dependency `@agentclientprotocol/sdk` pinned exactly.
* Copy mode: **DEPEND-ON-PACKAGE (npm `@agentclientprotocol/sdk` 2.0.2, published 2026-10-23, Apache-2.0)**
* Selected surface: **86 files, 3,919,779 bytes** (23 test). Excluded: `src/examples` (11 files, 2,662,858 B), `src/test-support`, typedoc configs, `MIGRATION_*.md` (REFERENCE).
* Internal imports outside the selected set: none required; `src/v1` and `src/v2` are generated from `schema/*` by `scripts/generate.js` (60,346 B).
* External dependencies (`package.json@bca8e49`): peer `zod ^3.25.76 || ^4.0.0`; no runtime `dependencies`.

| package | declared | from | latest on npm | license |
|---|---|---|---|---|
| @modelcontextprotocol/server | ^2.4.0 | peer | 2.4.0 | Apache-2.0 |
| zod | ^3.25.76 || ^4.0.0 | peer | 4.6.7 | MIT |

* License and NOTICE: Apache-2.0 (`LICENSE` 10,783 B), author `Zed Industries`; no NOTICE.
* Risks: (1) The `exports` map exposes `./experimental/*` entry points (v2, nes, http-client, ws-client, server, node, mcp-http): never import them in production paths. (2) The zod peer range must match the zod used by the rest of Zain (T3 mainly uses Effect Schema; the zod version in the T3 tree is **UNKNOWN**). (3) Duplicates T3 `effect-acp`.
* Qualification tests: contract tests against the Rust SDK as peer (TS client vs Rust agent, and the reverse). Negative: protocol-router rejects a request for an unregistered method; the WebSocket transport rejects cross-origin connections; schema validation fails on a malformed `session/update`.

<details><summary>File list with blob sizes</summary>

| path | B | blob | k |
|---|---:|---|---|
| `LICENSE` | 10783 | c24b0535 | P |
| `package.json` | 5700 | abf57c42 | P |
| `schema/v1/meta.json` | 1159 | b9c67caa | P |
| `schema/v1/meta.unstable.json` | 1387 | 2b1222e5 | P |
| `schema/v1/schema.json` | 255170 | d6f7731b | P |
| `schema/v1/schema.unstable.json` | 335597 | 6d053e0d | P |
| `schema/v2/meta.json` | 769 | ad2cfd93 | P |
| `schema/v2/meta.unstable.json` | 997 | 1b4813ad | P |
| `schema/v2/schema.json` | 311791 | 4103c569 | P |
| `schema/v2/schema.unstable.json` | 380957 | 9626b57b | P |
| `scripts/generate-bindings.js` | 8605 | 9186c79e | P |
| `scripts/generate.js` | 60346 | e73cbd3a | P |
| `src/core/app-handlers.ts` | 3580 | 2d4d1211 | P |
| `src/core/connection-access.ts` | 806 | d7e46601 | P |
| `src/core/jsonrpc.test.ts` | 35864 | 0313a285 | T |
| `src/core/jsonrpc.ts` | 47339 | 4c29019a | P |
| `src/core/line-buffer.test.ts` | 2984 | 4e4d7175 | T |
| `src/core/line-buffer.ts` | 4073 | 1e28d4ce | P |
| `src/core/schema-deserialize.test.ts` | 4405 | 1b988424 | T |
| `src/core/schema-deserialize.ts` | 5606 | e850c0cc | P |
| `src/core/stream-limits.ts` | 1923 | ddfe13cb | P |
| `src/core/stream.test.ts` | 8179 | 8d95fd3f | T |
| `src/core/stream.ts` | 4510 | 57efcb9f | P |
| `src/mcp/core.test.ts` | 14501 | 7f80029b | T |
| `src/mcp/core.ts` | 25412 | c8269737 | P |
| `src/mcp/header-annotations.ts` | 2065 | 52a1ca1c | P |
| `src/mcp/http.test.ts` | 15946 | 0d24a814 | T |
| `src/mcp/http.ts` | 24236 | 5ee9460e | P |
| `src/mcp/mcp-server.test.ts` | 12714 | 7868300c | T |
| `src/mcp/mcp-server.ts` | 10533 | 3df7e4b6 | P |
| `src/nes/acp.ts` | 12131 | 9f13134b | P |
| `src/nes/schema/types.gen.ts` | 34741 | f536c039 | P |
| `src/nes/schema/zod.gen.ts` | 18137 | 7f4e8515 | P |
| `src/protocol-router.test.ts` | 21593 | 80c3b70f | T |
| `src/protocol-router.ts` | 16808 | 336851d7 | P |
| `src/transports/connection.test.ts` | 24721 | 16ee2a98 | T |
| `src/transports/connection.ts` | 37277 | a3c53557 | P |
| `src/transports/cookie-store.test.ts` | 3310 | c43068c6 | T |
| `src/transports/cookie-store.ts` | 3682 | 1b9d5789 | P |
| `src/transports/http-stream.test.ts` | 70481 | 4256a599 | T |
| `src/transports/http-stream.ts` | 24653 | f65ca7dd | P |
| `src/transports/node-adapter.test.ts` | 22347 | 491ad577 | T |
| `src/transports/node-adapter.ts` | 11252 | 433b3924 | P |
| `src/transports/node-body.ts` | 4066 | de191ca0 | P |
| `src/transports/protocol.test.ts` | 3856 | dddcf97e | T |
| `src/transports/protocol.ts` | 2155 | 47e65328 | P |
| `src/transports/server-permission.test.ts` | 9243 | a7f43905 | T |
| `src/transports/server-session-sse.test.ts` | 18870 | b159bbcd | T |
| `src/transports/server-sse.test.ts` | 3797 | bf1c826c | T |
| `src/transports/server-sse.ts` | 4447 | 6f6af30e | P |
| `src/transports/server-websocket-upgrade.test.ts` | 47041 | 1eccc237 | T |
| `src/transports/server.test.ts` | 61733 | 9db1ae8d | T |
| `src/transports/server.ts` | 17445 | 6042c44b | P |
| `src/transports/sse.test.ts` | 7372 | ba0fdc89 | T |
| `src/transports/sse.ts` | 3813 | d9bb47d5 | P |
| `src/transports/ws-server.ts` | 18751 | e4586fb3 | P |
| `src/transports/ws-stream.test.ts` | 31155 | b847aae1 | T |
| `src/transports/ws-stream.ts` | 10562 | 788d0ef3 | P |
| `src/transports/ws-utils.test.ts` | 1898 | af40e7f5 | T |
| `src/transports/ws-utils.ts` | 3444 | 98a12438 | P |
| `src/v1/acp.test.ts` | 178262 | 62d219a4 | T |
| `src/v1/acp.ts` | 69957 | 813af549 | P |
| `src/v1/schema/guards.gen.ts` | 12628 | 2acda1d9 | P |
| `src/v1/schema/index.ts` | 5086 | 974d68c5 | P |
| `src/v1/schema/types.gen.ts` | 122589 | b88b6467 | P |
| `src/v1/schema/zod.gen.ts` | 73690 | 4a2c4818 | P |
| `src/v1/stable/acp.ts` | 67601 | 2f42da15 | P |
| `src/v1/unstable/acp.ts` | 53 | f997e894 | P |
| `src/v1/unstable/mcp.ts` | 737 | 51c6cb94 | P |
| `src/v1/unstable/schema/guards.gen.ts` | 21314 | eaa0df1d | P |
| `src/v1/unstable/schema/index.ts` | 6287 | ecce0318 | P |
| `src/v1/unstable/schema/types.gen.ts` | 167425 | cf644560 | P |
| `src/v1/unstable/schema/zod.gen.ts` | 101433 | e78798ba | P |
| `src/v2/acp.test.ts` | 55899 | fdcd4a3f | T |
| `src/v2/acp.ts` | 96881 | 2531eaee | P |
| `src/v2/schema/guards.gen.ts` | 70839 | bee17a1d | P |
| `src/v2/schema/index.ts` | 4659 | 03beebad | P |
| `src/v2/schema/types.gen.ts` | 150145 | a4d44fe0 | P |
| `src/v2/schema/zod.gen.ts` | 89006 | e5ee77dd | P |
| `src/v2/stable/acp.ts` | 94357 | 3f034ec8 | P |
| `src/v2/unstable/acp.ts` | 53 | f997e894 | P |
| `src/v2/unstable/mcp.ts` | 737 | 51c6cb94 | P |
| `src/v2/unstable/schema/guards.gen.ts` | 75168 | cb08e0f3 | P |
| `src/v2/unstable/schema/index.ts` | 5676 | d15ae03b | P |
| `src/v2/unstable/schema/types.gen.ts` | 189047 | 053aa10d | P |
| `src/v2/unstable/schema/zod.gen.ts` | 111532 | 98b99c40 | P |

</details>


---

<!-- SECTION:D13a -->
## D13a. MCP TypeScript SDK (`modelcontextprotocol/typescript-sdk`)

MCP client and server libraries for TypeScript. The repo is a pnpm monorepo that split the v1 single package into `@modelcontextprotocol/{client,server,core,node,express}` v2. Matrix row D13.

* Upstream: `modelcontextprotocol/typescript-sdk@b415e60bdf0e8dd5d6cbe7e6353abfb982b06dd2`.
* Zain destination: `apps/server` and `packages/mcp-host` dependencies on `@modelcontextprotocol/client` and `@modelcontextprotocol/server` (exact versions).
* Copy mode: **DEPEND-ON-PACKAGE (npm `@modelcontextprotocol/client` 2.4.0, `server` 2.4.0, `core` 2.4.0 on 2026-10-23, license field Apache-2.0)**
* Selected surface (client, server, core sources and manifests): **95 files, 1,185,963 bytes** (0 test). Other packages in the repo: `core-internal` (351 files, 2,206,767 B; private), `middleware` (70 files), `server-legacy` (38 files), `codemod` (62 files); the v1 `@modelcontextprotocol/sdk` 1.32.2 (MIT on npm) is the legacy package line.
| path (aggregated) | files | bytes |
|---|---:|---:|
| `packages/client` | 89 | 1,846,369 |
| `packages/codemod` | 62 | 802,974 |
| `packages/core` | 21 | 156,590 |
| `packages/core-internal` | 351 | 2,206,767 |
| `packages/middleware` | 70 | 447,770 |
| `packages/server` | 114 | 1,308,185 |
| `packages/server-legacy` | 38 | 250,787 |

* Internal imports outside the selected set: `client` and `server` depend on `@modelcontextprotocol/core` (selected) at an exact matching version; `core` is built from `core-internal` sources at publish time (the exact inlining was not verified: **UNKNOWN beyond sample**).
* External dependencies (from the three package.json files at the pin; licenses from npm registry JSON):

| package | declared | from | latest on npm | license |
|---|---|---|---|---|
| @modelcontextprotocol/core | workspace:* | client | 2.4.0 | Apache-2.0 |
| cross-spawn | catalog:runtimeClientOnly | client | 7.0.6 | MIT |
| eventsource | catalog:runtimeClientOnly | client | 5.1.3 | MIT |
| eventsource-parser | catalog:runtimeClientOnly | client | 4.1.3 | MIT |
| jose | catalog:runtimeClientOnly | client | 6.2.13 | MIT |
| pkce-challenge | catalog:runtimeShared | client | 6.0.0 | MIT |
| zod | catalog:runtimeShared | client | 4.6.7 | MIT |

* License fields in the three package.json files at the pin: client=Apache-2.0, server=Apache-2.0, core=Apache-2.0.
* License and NOTICE obligations: the root `LICENSE` (12,227 B) states a licensing transition from MIT to Apache-2.0: new contributions are Apache-2.0, contributions by authors who have not granted relicensing remain MIT, documentation is CC-BY-4.0, and the file contains the full Apache-2.0 text, the MIT text (Copyright (c) 2024-2025 Model Context Protocol a Series of LF Projects, LLC.) and the CC-BY-4.0 notice. GitHub reports NOASSERTION. Per-file origin is not marked in the files read, so Zain must treat every file as possibly MIT-only: ship both license texts in third-party notices and keep the copyright line. No NOTICE file.
* Risks: (1) v1 to v2 migration (`skills/mcp-typescript-sdk-upgrade-to-v2`, 12 files): code written against 1.32.2 breaks. (2) The v2 packages require zod ^4.2.0 while the legacy SDK accepted zod ^3.25 or ^4. (3) The client includes OAuth (jose, pkce-challenge) and stdio spawning (cross-spawn): credential and arbitrary-command surfaces. (4) Tool descriptions and results come from untrusted servers and are prompt-injection vectors.
* Qualification tests: Positive: MCP conformance suites; an initialize, list and call round trip against a local fixture server. Negative: a server that changes its tool list or a tool description after approval (rug pull) is detected and re-prompted; a tool result containing instructions is passed as data; oversized frames and malformed JSON-RPC are rejected; a stdio server that ignores shutdown is killed through process-host (D4); an OAuth redirect URI mismatch is refused; a spawn command not on the allowlist is denied by Core.

<details><summary>File list with blob sizes (client, server, core)</summary>

| path | B | blob | k |
|---|---:|---|---|
| `LICENSE` | 12227 | 4a939857 | P |
| `packages/client/package.json` | 6247 | df1fd506 | P |
| `packages/client/src/client/auth.examples.ts` | 1867 | fc4c52de | P |
| `packages/client/src/client/auth.ts` | 113778 | 69366521 | P |
| `packages/client/src/client/authErrors.ts` | 11138 | df61820c | P |
| `packages/client/src/client/authExtensions.examples.ts` | 2130 | 35bee44d | P |
| `packages/client/src/client/authExtensions.ts` | 26436 | e210786b | P |
| `packages/client/src/client/authSeam.ts` | 1724 | fc93fd45 | P |
| `packages/client/src/client/client.examples.ts` | 5785 | 6813d65a | P |
| `packages/client/src/client/client.ts` | 134543 | 096a8660 | P |
| `packages/client/src/client/crossAppAccess.ts` | 11137 | 6eac2353 | P |
| `packages/client/src/client/dpop.ts` | 10550 | e7ad624b | P |
| `packages/client/src/client/middleware.examples.ts` | 3181 | 1782ac85 | P |
| `packages/client/src/client/middleware.ts` | 18256 | 179a1643 | P |
| `packages/client/src/client/probeClassifier.ts` | 18850 | 8753f8e6 | P |
| `packages/client/src/client/responseCache.ts` | 34015 | e6103d34 | P |
| `packages/client/src/client/sse.ts` | 23160 | 55c346ac | P |
| `packages/client/src/client/stdio.ts` | 10505 | 6dbddb66 | P |
| `packages/client/src/client/streamableHttp.examples.ts` | 1066 | 7383cb75 | P |
| `packages/client/src/client/streamableHttp.ts` | 62893 | 091674e1 | P |
| `packages/client/src/client/versionNegotiation.ts` | 31648 | 5dfced8c | P |
| `packages/client/src/ext/skills/entries.ts` | 2313 | e8cd9fbf | P |
| `packages/client/src/ext/skills/errors.ts` | 1223 | ea2eedf4 | P |
| `packages/client/src/ext/skills/index.ts` | 1033 | 515a89c3 | P |
| `packages/client/src/ext/skills/pageSchemas.ts` | 1323 | 679685a0 | P |
| `packages/client/src/ext/skills/skillsClient.ts` | 16392 | f1aea033 | P |
| `packages/client/src/ext/skills/verify.ts` | 1839 | b9b0f156 | P |
| `packages/client/src/fromJsonSchema.ts` | 600 | 588a096d | P |
| `packages/client/src/index.ts` | 5331 | 0b5b6e86 | P |
| `packages/client/src/shimsBrowser.ts` | 565 | ee5d6373 | P |
| `packages/client/src/shimsNode.ts` | 563 | 5c411d73 | P |
| `packages/client/src/shimsWorkerd.ts` | 1008 | 1ac1e653 | P |
| `packages/client/src/stdio.ts` | 536 | f0c7b1af | P |
| `packages/client/src/validators/ajv.ts` | 561 | 059c6b73 | P |
| `packages/client/src/validators/cfWorker.ts` | 279 | f1d9379a | P |
| `packages/core/package.json` | 3201 | fbcf2818 | P |
| `packages/core/src/auth.ts` | 13234 | d7f7f885 | P |
| `packages/core/src/constants.ts` | 4422 | 72b5f1c7 | P |
| `packages/core/src/ext/skills/capability.ts` | 1196 | 0019d4ee | P |
| `packages/core/src/ext/skills/constants.ts` | 1127 | 9ee95270 | P |
| `packages/core/src/ext/skills/index.ts` | 1451 | 0544030d | P |
| `packages/core/src/ext/skills/schemas.ts` | 3072 | 586d69dc | P |
| `packages/core/src/ext/skills/types.ts` | 2052 | bab2c6e1 | P |
| `packages/core/src/index.ts` | 7203 | e8ddda29 | P |
| `packages/core/src/internal.ts` | 1329 | 8c06b9af | P |
| `packages/core/src/schemas.ts` | 85871 | 3a7dd5b5 | P |
| `packages/core/src/types.ts` | 258 | 3b1d4fb0 | P |
| `packages/server/package.json` | 6367 | e147d8b5 | P |
| `packages/server/src/ext/skills/catalogBuild.ts` | 12031 | 1eb78739 | P |
| `packages/server/src/ext/skills/catalogSource.ts` | 3603 | 28940bed | P |
| `packages/server/src/ext/skills/errors.ts` | 2099 | 63eab39e | P |
| `packages/server/src/ext/skills/extension.ts` | 17713 | 0e10494a | P |
| `packages/server/src/ext/skills/files.ts` | 3011 | 8b93955d | P |
| `packages/server/src/ext/skills/fsPath.ts` | 1142 | 82920ca9 | P |
| `packages/server/src/ext/skills/index.ts` | 1154 | e48b9fc3 | P |
| `packages/server/src/ext/skills/internal.ts` | 192 | 7483ccb0 | P |
| `packages/server/src/ext/skills/node.ts` | 2778 | 12cb203f | P |
| `packages/server/src/ext/skills/paging.ts` | 2215 | 2b4dc7bd | P |
| `packages/server/src/ext/skills/skillEntry.ts` | 1300 | f5f29661 | P |
| `packages/server/src/ext/skills/types.ts` | 3642 | 69ecd554 | P |
| `packages/server/src/fromJsonSchema.ts` | 600 | c2db3fda | P |
| `packages/server/src/index.ts` | 6137 | 32605dd7 | P |
| `packages/server/src/server/completable.examples.ts` | 1326 | 925f24e2 | P |
| `packages/server/src/server/completable.ts` | 2685 | b8ab7b6b | P |
| `packages/server/src/server/createMcpHandler.ts` | 50333 | 4ef836c6 | P |
| `packages/server/src/server/invoke.ts` | 3359 | 1a698492 | P |
| `packages/server/src/server/legacyInputRequiredShim.ts` | 15081 | 2657e1fe | P |
| `packages/server/src/server/listenRouter.ts` | 19748 | e58807d5 | P |
| `packages/server/src/server/mcp.examples.ts` | 4277 | c4abb9cc | P |
| `packages/server/src/server/mcp.ts` | 66767 | bfb3b798 | P |
| `packages/server/src/server/middleware/bearerAuth.examples.ts` | 1082 | 5751fc80 | P |
| `packages/server/src/server/middleware/bearerAuth.ts` | 12101 | 1c455d11 | P |
| `packages/server/src/server/middleware/hostHeaderValidation.examples.ts` | 651 | f46a04c5 | P |
| `packages/server/src/server/middleware/hostHeaderValidation.ts` | 2361 | a438bea7 | P |
| `packages/server/src/server/middleware/oauthMetadata.examples.ts` | 839 | 9aff9f11 | P |
| `packages/server/src/server/middleware/oauthMetadata.ts` | 8252 | 64296d05 | P |
| `packages/server/src/server/middleware/originValidation.ts` | 4476 | 83147cea | P |
| `packages/server/src/server/perRequestTransport.ts` | 19251 | 971697d2 | P |
| `packages/server/src/server/requestBody.ts` | 2400 | a11e8d99 | P |
| `packages/server/src/server/requestStateCodec.ts` | 12886 | 37c1f857 | P |
| `packages/server/src/server/scopeChallenge.ts` | 5216 | 544175da | P |
| `packages/server/src/server/serveStdio.ts` | 39474 | 1cabf8ed | P |
| `packages/server/src/server/server.ts` | 65597 | 441857f6 | P |
| `packages/server/src/server/serverEventBus.ts` | 8844 | 580cd8bc | P |
| `packages/server/src/server/sseKeepAlive.ts` | 586 | 25df1187 | P |
| `packages/server/src/server/stdio.examples.ts` | 673 | 6b51203b | P |
| `packages/server/src/server/stdio.ts` | 9262 | 4895359a | P |
| `packages/server/src/server/streamableHttp.examples.ts` | 2788 | cdfad542 | P |
| `packages/server/src/server/streamableHttp.ts` | 58470 | 2484ae19 | P |
| `packages/server/src/shimsBrowser.ts` | 1019 | 7a9c7154 | P |
| `packages/server/src/shimsNode.ts` | 314 | 6ec70365 | P |
| `packages/server/src/shimsWorkerd.ts` | 1214 | bf0ddfc7 | P |
| `packages/server/src/stdio.ts` | 689 | 1d38a61a | P |
| `packages/server/src/validators/ajv.ts` | 561 | 8bd1a78a | P |
| `packages/server/src/validators/cfWorker.ts` | 279 | f1d9379a | P |

</details>


---

<!-- SECTION:D13b -->
## D13b. MCP Rust SDK (`modelcontextprotocol/rust-sdk`, crate `rmcp`)

Rust MCP client and server (`rmcp`, `rmcp-macros`) with streamable HTTP, child-process transport and OAuth. Matrix row D13.

* Upstream: `modelcontextprotocol/rust-sdk@cd88056ffdc97756fbd98e5a12bbeb41758f0ce8`.
* Zain destination: `crates/core/Cargo.toml` dependency `rmcp = { version = "=3.8.0", default-features = false, features = ["client", "transport-child-process"] }`; add `auth` only when remote servers are approved.
* Copy mode: **DEPEND-ON-PACKAGE (crates.io `rmcp` 3.8.0 and `rmcp-macros` 3.8.0, published 2026-10-26, Apache-2.0)**
* Selected surface: **78 files, 2,121,715 bytes** (1 test). Also present: `conformance/` (a conformance runner crate: src 118,673 B and `expected-failures-extensions.yaml`) which Zain should run, and `crates/rmcp/tests`.
* Internal imports outside the selected set: `rmcp` optionally depends on `rmcp-macros` (selected). None else.
* External dependencies (Cargo.toml of `rmcp` and `rmcp-macros`; licenses from crates.io JSON):

| crate | declared | kind | optional | latest on crates.io | license |
|---|---|---|---|---|---|
| async-trait | 0.1.89 | runtime | yes | 0.1.92 | MIT OR Apache-2.0 |
| base64 | 0.23 | runtime | yes | 0.23.1 | MIT OR Apache-2.0 |
| bytes | 1 | runtime | yes | 1.12.1 | MIT |
| chrono | 0.4.38 | runtime/target | no | 0.4.45 | MIT OR Apache-2.0 |
| darling | 0.24 | runtime | no | 0.24.1 | MIT |
| futures | 0.3 | runtime | no | 0.3.34 | MIT OR Apache-2.0 |
| hmac | 0.13 | runtime | yes | 0.13.0 | MIT OR Apache-2.0 |
| http | 1 | runtime | yes | 1.5.0 | MIT OR Apache-2.0 |
| http-body | 1 | runtime | yes | 1.1.0 | MIT |
| http-body-util | 0.1 | runtime | yes | 0.1.5 | MIT |
| hyper | 1 | runtime | yes | 1.12.0 | MIT |
| hyper-util | 0.1 | runtime | yes | 0.1.21 | MIT |
| indexmap | 2 | runtime | no | 2.14.2 | Apache-2.0 OR MIT |
| jsonwebtoken | 11 | runtime | yes | 11.1.0 | MIT |
| libc | 0.2 | runtime/target | no | 0.2.191 | MIT OR Apache-2.0 |
| oauth2 | 5.0 | runtime | yes | 5.0.0 | MIT OR Apache-2.0 |
| pastey | 0.2.0 | runtime | yes | 0.2.3 | MIT OR Apache-2.0 |
| pin-project-lite | 0.2 | runtime | no | 0.2.17 | Apache-2.0 OR MIT |
| proc-macro2 | 1 | runtime | no | 1.0.107 | MIT OR Apache-2.0 |
| process-wrap | 10.0 | runtime | yes | 10.0.1 | Apache-2.0 OR MIT |
| quote | 1 | runtime | no | 1.0.47 | MIT OR Apache-2.0 |
| rand | 0.10 | runtime | yes | 0.10.3 | MIT OR Apache-2.0 |
| reqwest | 0.13.2 | runtime | yes | 0.13.5 | MIT OR Apache-2.0 |
| schemars | 1.0 | runtime | yes | 1.2.3 | MIT |
| serde | 1.0 | runtime | no | 1.0.229 | MIT OR Apache-2.0 |
| serde_json | 1.0 | runtime | no | 1.0.154 | MIT OR Apache-2.0 |
| sha2 | 0.11 | runtime | yes | 0.11.1 | MIT OR Apache-2.0 |
| sse-stream | 0.2.4 | runtime | yes | 0.3.0 | MIT OR Apache-2.0 |
| syn | 3 | runtime | no | 3.0.9 | MIT OR Apache-2.0 |
| thiserror | 2 | runtime | no | 2.0.21 | MIT OR Apache-2.0 |
| tokio | 1 | runtime | no | 1.54.1 | MIT |
| tokio-stream | 0.1 | runtime | yes | 0.1.19 | MIT |
| tokio-util | 0.7 | runtime | no | 0.7.20 | MIT |
| tower-service | 0.3 | runtime | yes | 0.3.3 | MIT |
| tracing | 0.1 | runtime | no | 0.1.44 | MIT |
| url | 2.4 | runtime | yes | 2.5.8 | MIT OR Apache-2.0 |
| uuid | 1 | runtime | yes | 1.29.0 | Apache-2.0 OR MIT |
| which | 8 | runtime | yes | 8.0.6 | MIT |
| zeroize | 1 | runtime | yes | 1.9.1 | Apache-2.0 OR MIT |

* License and NOTICE: the same mixed root `LICENSE` as D13a (12,227 B); `crates/rmcp/LICENSE` and `crates/rmcp-macros/LICENSE` are 13-byte stubs (symlinks to the root). crates.io declares Apache-2.0 for 3.x. Treat as Apache-2.0 plus MIT notice, as in D13a. No NOTICE file.
* Risks: (1) Very fast major churn (3.6.0 on 2026-10-20, 3.7.0 on 2026-10-22, 3.8.0 on 2026-10-26): pin exactly and re-run conformance per bump. (2) The feature matrix is large (`auth`, `auth-client-credentials-jwt`, `auth-enterprise-managed`, `transport-streamable-http-server`, and more): enable the minimum. (3) `reqwest` and TLS choices (`reqwest-native-tls` vs rustls) interact with the Zain network policy. (4) The ACP Rust SDK has an `-rmcp` bridge crate that tracks specific rmcp majors (`md/migration-rmcp-v4.md` in D12b): keep versions aligned.
* Qualification tests: run the repo `conformance` crate and compare with `expected-failures-extensions.yaml`. Negative: the child-process transport kills the child on drop; malformed frames do not panic; a server returning a huge `tools/list` is truncated or refused; auth tokens never appear in logs.

<details><summary>File list with blob sizes</summary>

| path | B | blob | k |
|---|---:|---|---|
| `Cargo.toml` | 842 | 41c4efd6 | P |
| `LICENSE` | 12227 | 4a939857 | P |
| `crates/rmcp-macros/Cargo.toml` | 578 | 9f0b3d30 | P |
| `crates/rmcp-macros/src/common.rs` | 3102 | dc7e5bfa | P |
| `crates/rmcp-macros/src/lib.rs` | 11878 | 573fdd28 | P |
| `crates/rmcp-macros/src/prompt.rs` | 9762 | 1bf3d52a | P |
| `crates/rmcp-macros/src/prompt_handler.rs` | 5616 | 6d957ecd | P |
| `crates/rmcp-macros/src/prompt_router.rs` | 3615 | 6abd96c9 | P |
| `crates/rmcp-macros/src/tool.rs` | 14653 | 362ffb4a | P |
| `crates/rmcp-macros/src/tool_handler.rs` | 5705 | c9f4a251 | P |
| `crates/rmcp-macros/src/tool_router.rs` | 7454 | 6efd6927 | P |
| `crates/rmcp/Cargo.toml` | 14336 | 7da38d36 | P |
| `crates/rmcp/src/error.rs` | 2599 | 0940f29c | P |
| `crates/rmcp/src/handler.rs` | 86 | 6b848cd2 | P |
| `crates/rmcp/src/handler/client.rs` | 16235 | 486fa3bd | P |
| `crates/rmcp/src/handler/client/progress.rs` | 3173 | 04f31610 | P |
| `crates/rmcp/src/handler/server.rs` | 37340 | 4abe9ccb | P |
| `crates/rmcp/src/handler/server/common.rs` | 13356 | 8d3e4a8a | P |
| `crates/rmcp/src/handler/server/prompt.rs` | 13710 | b5b3c469 | P |
| `crates/rmcp/src/handler/server/resource.rs` | 1 | 8b137891 | P |
| `crates/rmcp/src/handler/server/router.rs` | 7752 | c49c4089 | P |
| `crates/rmcp/src/handler/server/router/prompt.rs` | 5450 | 509fb428 | P |
| `crates/rmcp/src/handler/server/router/tool.rs` | 22888 | f8fab023 | P |
| `crates/rmcp/src/handler/server/router/tool/tool_traits.rs` | 10785 | bde92147 | P |
| `crates/rmcp/src/handler/server/tool.rs` | 13965 | 54de5fa1 | P |
| `crates/rmcp/src/handler/server/tool_name_validation.rs` | 8075 | 8ae04b62 | P |
| `crates/rmcp/src/handler/server/wrapper.rs` | 66 | d9f2c86d | P |
| `crates/rmcp/src/handler/server/wrapper/json.rs` | 1429 | 7c529796 | P |
| `crates/rmcp/src/handler/server/wrapper/parameters.rs` | 2032 | ab3eb0ce | P |
| `crates/rmcp/src/lib.rs` | 1344 | 3be6616e | P |
| `crates/rmcp/src/model.rs` | 220846 | 9dd04564 | P |
| `crates/rmcp/src/model/annotated.rs` | 4074 | 65b31a1a | P |
| `crates/rmcp/src/model/capabilities.rs` | 25586 | f014f569 | P |
| `crates/rmcp/src/model/content.rs` | 15045 | 11b2f0e5 | P |
| `crates/rmcp/src/model/elicitation_schema.rs` | 78189 | 7a556e84 | P |
| `crates/rmcp/src/model/extension.rs` | 9728 | 039fdf2e | P |
| `crates/rmcp/src/model/meta.rs` | 29376 | 0a7121e4 | P |
| `crates/rmcp/src/model/mrtr.rs` | 20026 | 8dac9a39 | P |
| `crates/rmcp/src/model/prompt.rs` | 11253 | 062655a8 | P |
| `crates/rmcp/src/model/request_state.rs` | 55371 | 9f45572c | P |
| `crates/rmcp/src/model/resource.rs` | 10600 | 9c27dce2 | P |
| `crates/rmcp/src/model/serde_impl.rs` | 35002 | 6ce30eb9 | P |
| `crates/rmcp/src/model/task.rs` | 19474 | bbdd1c99 | P |
| `crates/rmcp/src/model/tool.rs` | 8239 | be7cbbd0 | P |
| `crates/rmcp/src/service.rs` | 74633 | aaec8289 | P |
| `crates/rmcp/src/service/client.rs` | 106962 | 5f3213d5 | P |
| `crates/rmcp/src/service/client/cache.rs` | 14262 | f7137ccd | P |
| `crates/rmcp/src/service/server.rs` | 54143 | f52b1159 | P |
| `crates/rmcp/src/service/tower.rs` | 1445 | 867d3e7f | P |
| `crates/rmcp/src/task_manager.rs` | 39052 | 4a5b9f7f | P |
| `crates/rmcp/src/transport.rs` | 11085 | 1e195a33 | P |
| `crates/rmcp/src/transport/async_rw.rs` | 35608 | af969736 | P |
| `crates/rmcp/src/transport/auth.rs` | 405788 | 7a65c2c4 | P |
| `crates/rmcp/src/transport/auth/enterprise.rs` | 30129 | dcc4c464 | P |
| `crates/rmcp/src/transport/auth/enterprise_tests.rs` | 46517 | e29e3210 | T |
| `crates/rmcp/src/transport/auth/metadata_resolver.rs` | 26260 | 03435a21 | P |
| `crates/rmcp/src/transport/child_process.rs` | 10311 | 6e19a0c3 | P |
| `crates/rmcp/src/transport/common.rs` | 660 | 8cf00c02 | P |
| `crates/rmcp/src/transport/common/auth.rs` | 81 | 6068f4e9 | P |
| `crates/rmcp/src/transport/common/auth/streamable_http_client.rs` | 14265 | 47b6caf5 | P |
| `crates/rmcp/src/transport/common/client_side_sse.rs` | 31985 | 26d2f778 | P |
| `crates/rmcp/src/transport/common/http_header.rs` | 4783 | 6c2abbc8 | P |
| `crates/rmcp/src/transport/common/mcp_headers.rs` | 36437 | e638c87e | P |
| `crates/rmcp/src/transport/common/reqwest.rs` | 89 | 42075921 | P |
| `crates/rmcp/src/transport/common/reqwest/streamable_http_client.rs` | 39025 | dbd6ae7d | P |
| `crates/rmcp/src/transport/common/server_side_http.rs` | 13011 | ba248ba8 | P |
| `crates/rmcp/src/transport/common/unix_socket.rs` | 22685 | 688c9ad4 | P |
| `crates/rmcp/src/transport/io.rs` | 13699 | 66622840 | P |
| `crates/rmcp/src/transport/sink_stream.rs` | 2388 | 6286b53b | P |
| `crates/rmcp/src/transport/streamable_http_client.rs` | 109763 | db44ab3f | P |
| `crates/rmcp/src/transport/streamable_http_server.rs` | 348 | df1945ab | P |
| `crates/rmcp/src/transport/streamable_http_server/session.rs` | 6811 | ea2e85b2 | P |
| `crates/rmcp/src/transport/streamable_http_server/session/local.rs` | 51914 | a3e6d19f | P |
| `crates/rmcp/src/transport/streamable_http_server/session/never.rs` | 3831 | d83031c3 | P |
| `crates/rmcp/src/transport/streamable_http_server/session/store.rs` | 4788 | 8b656201 | P |
| `crates/rmcp/src/transport/streamable_http_server/tower.rs` | 96769 | 2b0772b2 | P |
| `crates/rmcp/src/transport/worker.rs` | 19274 | e32da7d7 | P |
| `crates/rmcp/src/transport/ws.rs` | 51 | 5ec9cbac | P |

</details>


---

<!-- SECTION:D19 -->
## D19. Excalidraw freeform canvas layer

Embeddable whiteboard React component used as the freeform annotation and sketch layer (matrix row D19, Phase 7).

* Upstream: `excalidraw/excalidraw@808d068e18266ff9311809c23c19261fa0eb1014`.
* Zain destination: `apps/web` dependency `@excalidraw/excalidraw` with a Zain wrapper in `packages/design-canvas/` (new); no source copied.
* Copy mode: **DEPEND-ON-PACKAGE (npm `@excalidraw/excalidraw` 0.18.1, published 2026-04-20, MIT)**
* Selected surface: the workspace packages `packages/{excalidraw,common,element,math,utils}` (plus the `fractional-indexing` and `laser-pointer` sub-packages published separately). The aggregated listing below counts 881 + 32 + 93 + 29 + 12 files; a per-file list for a registry dependency adds no audit value, so only manifests and fonts are itemised.
| path (aggregated) | files | bytes |
|---|---:|---:|
| `packages/excalidraw/.gitignore` | 1 | 19 |
| `packages/excalidraw/.size-limit.json` | 1 | 336 |
| `packages/excalidraw/CHANGELOG.md` | 1 | 163,242 |
| `packages/excalidraw/README.md` | 1 | 4,910 |
| `packages/excalidraw/actions` | 49 | 310,980 |
| `packages/excalidraw/analytics.ts` | 1 | 1,020 |
| `packages/excalidraw/animatedTrail.ts` | 1 | 5,732 |
| `packages/excalidraw/appState.ts` | 1 | 13,966 |
| `packages/excalidraw/charts` | 8 | 46,506 |
| `packages/excalidraw/charts.test.ts` | 1 | 38,471 |
| `packages/excalidraw/clients.ts` | 1 | 7,322 |
| `packages/excalidraw/clipboard.test.ts` | 1 | 4,717 |
| `packages/excalidraw/clipboard.ts` | 1 | 19,316 |
| `packages/excalidraw/components` | 309 | 1,915,825 |
| `packages/excalidraw/context` | 2 | 1,678 |
| `packages/excalidraw/css` | 4 | 40,140 |
| `packages/excalidraw/css.d.ts` | 1 | 211 |
| `packages/excalidraw/data` | 15 | 140,296 |
| `packages/excalidraw/deburr.ts` | 1 | 4,407 |
| `packages/excalidraw/drawShapeTrail.ts` | 1 | 1,802 |
| `packages/excalidraw/editor-jotai.ts` | 1 | 522 |
| `packages/excalidraw/env.cjs` | 1 | 457 |
| `packages/excalidraw/eraser` | 1 | 9,078 |
| `packages/excalidraw/errors.ts` | 1 | 2,164 |
| `packages/excalidraw/fonts` | 249 | 13,936,855 |
| `packages/excalidraw/gesture.ts` | 1 | 548 |
| `packages/excalidraw/global.d.ts` | 1 | 3,273 |
| `packages/excalidraw/history.ts` | 1 | 7,466 |
| `packages/excalidraw/hooks` | 12 | 19,274 |
| `packages/excalidraw/i18n.ts` | 1 | 5,583 |
| `packages/excalidraw/index-node.ts` | 1 | 1,671 |
| `packages/excalidraw/index.tsx` | 1 | 16,529 |
| `packages/excalidraw/laserTrails.ts` | 1 | 3,867 |
| `packages/excalidraw/lasso` | 2 | 17,299 |
| `packages/excalidraw/locales` | 59 | 1,868,488 |
| `packages/excalidraw/mermaid.test.ts` | 1 | 708 |
| `packages/excalidraw/mermaid.ts` | 1 | 684 |
| `packages/excalidraw/package.json` | 1 | 3,896 |
| `packages/excalidraw/polyfill.ts` | 1 | 3,226 |
| `packages/excalidraw/pwacompat.d.ts` | 1 | 28 |
| `packages/excalidraw/react-app-env.d.ts` | 1 | 40 |
| `packages/excalidraw/reactUtils.ts` | 1 | 1,744 |
| `packages/excalidraw/renderOverrides.ts` | 1 | 2,095 |
| `packages/excalidraw/renderer` | 9 | 133,626 |
| `packages/excalidraw/scene` | 6 | 70,046 |
| `packages/excalidraw/shortcut.ts` | 1 | 625 |
| `packages/excalidraw/snapping.ts` | 1 | 36,227 |
| `packages/excalidraw/subset` | 9 | 1,913,437 |
| `packages/excalidraw/tests` | 105 | 2,663,685 |
| `packages/excalidraw/textAutoResizeHandle.ts` | 1 | 2,589 |
| `packages/excalidraw/tsconfig.json` | 1 | 211 |
| `packages/excalidraw/types.ts` | 1 | 59,211 |
| `packages/excalidraw/viewport.ts` | 1 | 14,905 |
| `packages/excalidraw/vite-env.d.ts` | 1 | 1,598 |
| `packages/excalidraw/workers.ts` | 1 | 4,150 |
| `packages/excalidraw/wysiwyg` | 2 | 160,287 |

* Font families bundled under `packages/excalidraw/fonts` (249 files, 13,936,855 B): `Assistant` (4 files, 81,144 B), `Cascadia` (2 files, 65,969 B), `ComicShanns` (6 files, 705,002 B), `Emoji` (1 files, 228 B), `Excalifont` (8 files, 71,671 B), `Helvetica` (1 files, 232 B), `Liberation` (2 files, 70,913 B), `Lilita` (3 files, 12,646 B), `Nunito` (6 files, 58,809 B), `Virgil` (2 files, 56,359 B), `Xiaolai` (210 files, 12,789,378 B). No per-font LICENSE or OFL file exists in this directory at the pin, so the license of each bundled font is **UNKNOWN** and must be verified before shipping (several are expected to be SIL OFL, which requires carrying the notice).
* Version note: the workspace `package.json` files at the pin say excalidraw 0.18.0, common, element and math 0.18.0, utils 0.1.2, while npm `latest` is 0.18.1 (2026-04-20): the pin is a development head, not the published 0.18.1. Use the registry artefact, not a source build.
* Internal imports outside the selected set: none beyond the five packages; `@excalidraw/{common,element,math}` are exact-version internal dependencies; `@excalidraw/fractional-indexing 3.3.0`, `@excalidraw/laser-pointer 1.3.1`, `@excalidraw/mermaid-to-excalidraw 2.2.2` and `@excalidraw/random-username 1.1.0` are external.
* External dependencies (package.json files of excalidraw, common, element, math, utils at the pin):

| package | declared | from | latest on npm | license |
|---|---|---|---|---|
| @braintree/sanitize-url | 6.0.2 | excalidraw | 7.1.2 | MIT |
| @codemirror/commands | ^6.0.0 | excalidraw | 6.11.1 | MIT |
| @codemirror/language | ^6.0.0 | excalidraw | 6.13.1 | MIT |
| @codemirror/state | ^6.0.0 | excalidraw | 6.7.6 | MIT |
| @codemirror/view | ^6.0.0 | excalidraw | 6.43.15 | MIT |
| @excalidraw/common | 0.18.0 | excalidraw | 0.18.0-f0063e113 | MIT |
| @excalidraw/element | 0.18.0 | excalidraw | 0.18.0-f0063e113 | MIT |
| @excalidraw/fractional-indexing | 3.3.0 | element | 0.18.0-d255747 | CC0-1.0 |
| @excalidraw/laser-pointer | 1.3.1 | excalidraw | 1.3.2 | MIT |
| @excalidraw/math | 0.18.0 | excalidraw | 0.18.0-f0063e113 | MIT |
| @excalidraw/mermaid-to-excalidraw | 2.2.2 | excalidraw | 3.1.0 | MIT |
| @excalidraw/random-username | 1.1.0 | excalidraw | 1.2.0 | MIT |
| @lezer/highlight | ^1.0.0 | excalidraw | 1.2.5 | MIT |
| browser-fs-access | 0.38.0 | excalidraw | 0.38.0 | Apache-2.0 |
| canvas-roundrect-polyfill | 0.0.1 | excalidraw | 0.0.1 | MIT |
| clsx | 1.1.1 | excalidraw | 2.1.1 | MIT |
| cross-env | 7.0.3 | excalidraw | 10.1.0 | MIT |
| es6-promise-pool | 2.5.0 | excalidraw | 2.5.0 | MIT |
| fuzzy | 0.1.3 | excalidraw | 0.1.3 | None |
| image-blob-reduce | 3.0.1 | excalidraw | 5.0.1 | MIT |
| jotai | 2.11.0 | excalidraw | 3.0.1 | MIT |
| jotai-scope | 0.7.2 | excalidraw | 0.12.2 | MIT |
| lodash.debounce | 4.0.8 | excalidraw | 4.0.8 | MIT |
| lodash.throttle | 4.1.1 | excalidraw | 4.1.1 | MIT |
| nanoid | 3.3.3 | excalidraw | 6.0.2 | MIT |
| pako | 2.0.3 | excalidraw | 3.0.3 | (MIT AND Zlib) |
| perfect-freehand | 1.2.0 | excalidraw | 1.2.3 | MIT |
| pica | 7.1.1 | excalidraw | 10.0.3 | MIT |
| png-chunk-text | 1.0.0 | excalidraw | 1.0.0 | MIT |
| png-chunks-encode | 1.0.0 | excalidraw | 1.0.0 | MIT |
| png-chunks-extract | 1.0.0 | excalidraw | 1.0.0 | MIT |
| points-on-curve | 1.0.1 | excalidraw | 1.0.1 | MIT |
| pwacompat | 2.0.17 | excalidraw | 2.0.17 | Apache-2.0 |
| radix-ui | 1.4.3 | excalidraw | 1.8.1 | MIT |
| react | ^17.0.2 || ^18.2.0 || ^19.0.0 | peer | 19.3.1 | MIT |
| react-dom | ^17.0.2 || ^18.2.0 || ^19.0.0 | peer | 19.3.1 | MIT |
| roughjs | 4.6.4 | excalidraw | 4.6.6 | MIT |
| sass | 1.51.0 | excalidraw | 1.106.1 | MIT |
| tinycolor2 | 1.6.0 | common | 1.6.0 | MIT |
| tunnel-rat | 0.1.2 | excalidraw | 0.1.2 | MIT |

* License and NOTICE: MIT (`LICENSE` 1,067 B). No NOTICE file. Keep the Excalidraw copyright line in Zain third-party notices; add notices for the transitive dependencies in the table above and for the bundled fonts once identified.
* Risks: (1) A client-only React component (canvas, `window`): lazy-load it, no SSR. (2) Bundle weight: `packages/excalidraw` is 23.7 MB in the repo (fonts 13.9 MB, locales 1.9 MB); the shipped bundle needs a size budget. (3) Pre-1.0 API (0.18.x) with frequent breaks; `sass 1.51.0` and `nanoid 3.3.3` are old pins. (4) 06 lists tldraw as REJECTED; Excalidraw is the chosen canvas, but a second canvas layer next to Orca and T3 annotations must be avoided (one annotation model). (5) Hosted extras (Excalidraw+, collab, Firebase) live in `excalidraw-app` and must not be pulled in.
* Qualification tests: Positive: load and save `.excalidraw` JSON round trip; deterministic PNG and SVG export for a fixture scene; keyboard-only drawing of a rectangle. Negative: a scene with 100,000 elements or a 50 MB embedded image is refused or degraded without freezing the UI; an SVG import containing a script element is neutralised; links with a `javascript:` scheme are blocked (the `@braintree/sanitize-url` dependency exists for this); offline mode makes no network call (no CDN font fetch).

<details><summary>Manifests and licenses</summary>

| path | B | blob | k |
|---|---:|---|---|
| `LICENSE` | 1067 | 8a844bc7 | P |
| `packages/common/package.json` | 1617 | 148ada31 | P |
| `packages/element/package.json` | 1876 | 408f2c9d | P |
| `packages/excalidraw/package.json` | 3896 | 8cbaa261 | P |
| `packages/laser-pointer/LICENSE` | 1067 | ffed06cc | P |
| `packages/math/package.json` | 1588 | d64a74d6 | P |
| `packages/utils/package.json` | 1833 | 24394800 | P |

</details>


---

<!-- SECTION:D20 -->
## D20. Element-to-source mapping (Onlook `data-oid` approach)

The DOM-to-AST algorithm and Babel id injector that map a clicked DOM element to file, line and component instance. The OSS line has slowed (hosted successor in early access, R03B section 9), so code is copied with attribution and owned, not depended on. Matrix row D20 (ADAPT, Phase 7).

* Upstream: `onlook-dev/onlook@423e2e924366419e418ee049093872d535eea41a`.
* Zain destination: `packages/design-source-map/src/{ids.ts,parse.ts,packages.ts,helpers.ts,template-node/*,models.ts,constants.ts}` (pure TS, Babel based) and a client-side DOM helper `packages/browser-core/src/design-mode/source-map-dom.ts`; the attribute is renamed from `data-onlook-id` to `data-zain-id` (06 text says `data-oid` and R03B says `data-wepld-id`; settle in ADR).
* Copy mode: **PORT-ADAPT**
* Selected set: **25 files, 62,933 bytes**. Algorithm description: `apps/web/client/src/components/store/editor/ast/README.md@423e2e9` (2,389 B): build a map from `data-oid` to code location and component name while parsing; walk the DOM; if a node component name differs from its parent component name, it is an instance; locate it by index in the parent source.
* DOM attributes found in `packages/constants/src/editor.ts`: `data-odid`, `data-oid`, `data-onlook-core-element-type`, `data-onlook-drag-direction`, `data-onlook-drag-saved-style`, `data-onlook-drag-start-position`, `data-onlook-dragging`, `data-onlook-dynamic-type`, `data-onlook-editing-text`, `data-onlook-ignore`, `data-onlook-inserted`, `data-onlook-new-index`.
* Internal imports outside the selected set: `ast/index.ts` imports `@onlook/file-system` (`JsxElementMetadata`), `mobx`, `../branch/manager` and `../engine` (EditorEngine): these are NOT copied and the algorithm is re-implemented over a plain interface. `ast/layers.ts` imports `mobx` and `../engine`. `packages/parser` imports `@onlook/constants`, `@onlook/models` and `@onlook/utility`, whose needed files are in the set (`constants/src/editor.ts`, `constants/src/frame.ts`, `models/src/element/*`, `utility/src/id.ts`; `editor.ts` imports `./frame`). `code-edit/helpers.ts` is selected for `getOidFromJsxElement` only; the other `code-edit/*` files (style, insert, move, layout, next-config) are NOT selected. The preload `ids.ts` imports `nanoid/non-secure`.
* External dependencies: `@babel/standalone ^7.27.0`, `@babel/types ^7.27.0` (parser package.json); `nanoid` (used in `utility/src/id.ts` and the preload helper; no version declared in the files read: **UNKNOWN**); `mobx` only in the files that are not ported.

| package | declared | from | latest on npm | license |
|---|---|---|---|---|
| @babel/standalone | ^7.27.0 | parser | 8.0.9 | MIT |
| @babel/types | ^7.27.0 | parser | 8.0.8 | MIT |
| @onlook/models | * | parser | ? | ? |
| nanoid | (unversioned in files read) | nanoid | 6.0.2 | MIT |

* License and NOTICE: Apache-2.0 (`LICENSE.md` 11,342 B; `packages/parser/package.json` also says Apache-2.0). No NOTICE file. Apache-2.0 section 4: keep the license, retain copyright notices, mark every modified file; add a PROVENANCE entry with the blob SHAs from the table. The Onlook name and logo are not licensed (section 6).
* Risks: (1) Babel standalone is heavy (megabytes) and runs at build time or in a worker, not in the page. (2) Id injection mutates user source or needs a build plugin (Next.js SWC vs Babel): a source-rewriting step must be reversible and visible in git. (3) Instance resolution is heuristic (index plus component name) and fails for dynamic children, conditional rendering, list mapping and portals. (4) The OSS line has slowed, so no upstream fixes are expected. (5) `createOid()` makes 7-character ids from a 40-character alphabet: collisions are probabilistic (see the comment in `utility/src/id.ts`). (6) 06 also lists click-to-component and react-dev-inspector (MIT) as complementary sources; they are different repos and are not in this manifest.
* Qualification tests: Positive: fixture JSX files where a click on the DOM node resolves to the correct file and range (the README Parent and Child example is the first fixture). Negative: an element produced by a list-mapping loop resolves to the template node and reports ambiguity instead of a wrong line; an element without an injected id returns unresolved; a second run of the injector adds no duplicate ids (idempotence); injecting ids into a file with a syntax error fails closed without touching the file; ids never leak into production builds.

<details><summary>File list with blob sizes</summary>

| path | B | blob | k |
|---|---:|---|---|
| `LICENSE.md` | 11342 | 295f5e1b | P |
| `apps/web/client/src/components/store/editor/ast/README.md` | 2389 | 76c6102f | P |
| `apps/web/client/src/components/store/editor/ast/index.ts` | 7109 | 996e69bb | P |
| `apps/web/client/src/components/store/editor/ast/layers.ts` | 2208 | 4d8f8b4c | P |
| `apps/web/preload/script/api/elements/helpers.ts` | 3538 | c7249ce9 | P |
| `apps/web/preload/script/helpers/ids.ts` | 732 | e4755f39 | P |
| `packages/constants/src/editor.ts` | 2343 | dfcaca60 | P |
| `packages/constants/src/frame.ts` | 1703 | 74ab0aa1 | P |
| `packages/models/src/element/classes.ts` | 211 | 20618878 | P |
| `packages/models/src/element/element.ts` | 867 | 69b5527d | P |
| `packages/models/src/element/index.ts` | 137 | cbc933b4 | P |
| `packages/models/src/element/layers.ts` | 573 | e8d3eee3 | P |
| `packages/models/src/element/props.ts` | 452 | 1a378f3a | P |
| `packages/models/src/element/templateNode.ts` | 489 | 400c770a | P |
| `packages/parser/package.json` | 1132 | e252c32c | P |
| `packages/parser/src/code-edit/helpers.ts` | 2675 | d5316f9f | P |
| `packages/parser/src/helpers.ts` | 1405 | a110b265 | P |
| `packages/parser/src/ids.ts` | 8257 | 422c8a3f | P |
| `packages/parser/src/index.ts` | 193 | d5719d59 | P |
| `packages/parser/src/packages.ts` | 417 | 9995638c | P |
| `packages/parser/src/parse.ts` | 2679 | 6dc39076 | P |
| `packages/parser/src/template-node/helpers.ts` | 3168 | 71959cec | P |
| `packages/parser/src/template-node/index.ts` | 50 | de6e3e81 | P |
| `packages/parser/src/template-node/map.ts` | 7905 | e0733468 | P |
| `packages/utility/src/id.ts` | 959 | 4af47b2b | P |

</details>


---

<!-- SECTION:D21 -->
## D21. Design tokens compiler (Style Dictionary)

Token build tool with first-class DTCG support; Zain compiles design tokens to CSS and TypeScript outputs through it. DTCG 2025.10 support is described as in progress in v5 (R03B X2). Matrix row D21 (Phase 7).

* Upstream: `style-dictionary/style-dictionary@f82e7aafbcaed3ca9009ec53859fbe05ed0c96a8`.
* Zain destination: `packages/design-tokens/` with `style-dictionary` as a build dependency; token sources in `packages/design-tokens/tokens/*.json` (DTCG format).
* Copy mode: **DEPEND-ON-PACKAGE (npm `style-dictionary` 5.7.1, published 2026-10-24, Apache-2.0)**
* Selected surface (published runtime: `lib/`, `types/`, `bin/`, manifests): **124 files, 390,849 bytes**. Not selected: `__tests__` (174 files), `__integration__` (48), `docs` (64), `examples` (504 files, 3.85 MB; two example directories carry their own LICENSE files, 11,357 B and 10,426 B, which do not apply to the library).
* Internal imports outside the selected set: none (self-contained package). Node engine `>=22.0.0` (package.json): the Zain toolchain must run Node 22 or newer.
* External dependencies (package.json at the pin):

| package | declared | from | latest on npm | license |
|---|---|---|---|---|
| @bundled-es-modules/deepmerge | ^4.3.2 | dependencies | 4.3.2 | MIT |
| @bundled-es-modules/glob | ^13.0.6-hotfix.0 | dependencies | 13.0.6 | MIT |
| @bundled-es-modules/memfs | ^4.17.0 | dependencies | 4.17.0 | Apache-2.0 |
| @zip.js/zip.js | ^2.7.44 | dependencies | 2.24.0 | BSD-3-Clause |
| chalk | ^5.3.0 | dependencies | 6.0.1 | MIT |
| change-case | ^5.3.0 | dependencies | 5.4.4 | MIT |
| colorjs.io | ^0.5.2 | dependencies | 0.7.1 | MIT |
| commander | ^12.1.0 | dependencies | 15.0.0 | MIT |
| is-plain-obj | ^4.1.0 | dependencies | 4.1.0 | MIT |
| json5 | ^2.2.2 | dependencies | 2.2.3 | MIT |
| path-unified | ^0.2.0 | dependencies | 0.2.0 | MIT |
| prettier | ^3.3.3 | dependencies | 3.9.10 | MIT |
| tinycolor2 | ^1.6.0 | dependencies | 1.6.0 | MIT |

* License and NOTICE: Apache-2.0 (`LICENSE` 9,793 B). `NOTICE` (58 B): Style Dictionary, Copyright Style Dictionary Contributors. Carry NOTICE verbatim in the Zain NOTICE file.
* Risks: (1) Major version churn (4.x to 5.x) and DTCG draft changes; pin exactly. (2) Plugin hooks execute user JavaScript (custom transforms and formats): token config files are code and must come only from the repository, never from an agent-supplied path without review. (3) `@bundled-es-modules/*` and `@zip.js/zip.js` enlarge the tree of a build-time tool. (4) The 2025.10 DTCG features (modern color spaces, resolvers) are partly supported: **UNKNOWN beyond the project statement**.
* Qualification tests: Positive: token round trip (DTCG JSON to CSS variables to TypeScript and back through a reverse parser) is lossless for supported types; the build is deterministic across two runs. Negative: a circular alias reference fails the build; an alias to a missing token fails; an invalid `$type` or `$value` fails; a config that tries to read outside the token directory is refused by the Zain wrapper; a token name containing a path separator is rejected.

<details><summary>File list with blob sizes</summary>

| path | B | blob | k |
|---|---:|---|---|
| `LICENSE` | 9793 | 8318dc07 | P |
| `NOTICE` | 58 | 144781fb | P |
| `bin/style-dictionary.js` | 5122 | 3ae88756 | P |
| `lib/Register.js` | 11694 | e4b16b2c | P |
| `lib/StyleDictionary.js` | 35356 | a96ac6d5 | P |
| `lib/cleanActions.js` | 1049 | 22327ac5 | P |
| `lib/cleanDir.js` | 1497 | d16b9f9c | P |
| `lib/cleanDirs.js` | 749 | 22ea57e9 | P |
| `lib/cleanFile.js` | 1547 | 7f58b9dc | P |
| `lib/cleanFiles.js` | 776 | 9720a400 | P |
| `lib/common/actions.js` | 3241 | fc0c4bed | P |
| `lib/common/filters.js` | 387 | 5e09d0c2 | P |
| `lib/common/formatHelpers/createPropertyFormatter.js` | 10835 | 5b9852e6 | P |
| `lib/common/formatHelpers/fileHeader.js` | 3225 | 99c36e38 | P |
| `lib/common/formatHelpers/formattedVariables.js` | 4970 | f3c4a503 | P |
| `lib/common/formatHelpers/getTypeScriptType.js` | 2690 | e742a589 | P |
| `lib/common/formatHelpers/iconsWithPrefix.js` | 1677 | e5a800ec | P |
| `lib/common/formatHelpers/index.js` | 748 | 142f8999 | P |
| `lib/common/formatHelpers/minifyDictionary.js` | 1099 | b6fed28d | P |
| `lib/common/formatHelpers/setComposeObjectProperties.js` | 657 | 240aea7e | P |
| `lib/common/formatHelpers/setSwiftFileProperties.js` | 1539 | 28bd1f58 | P |
| `lib/common/formatHelpers/sortByName.js` | 927 | 757aac06 | P |
| `lib/common/formatHelpers/sortByReference.js` | 3099 | 25195b04 | P |
| `lib/common/formats.js` | 51794 | e1400293 | P |
| `lib/common/templates/android/colors.template.js` | 792 | 758b4757 | P |
| `lib/common/templates/android/dimens.template.js` | 796 | b9fd47e6 | P |
| `lib/common/templates/android/fontDimens.template.js` | 795 | 8c439047 | P |
| `lib/common/templates/android/integers.template.js` | 795 | e6ab512d | P |
| `lib/common/templates/android/resources.template.js` | 2452 | a7a8e0c3 | P |
| `lib/common/templates/android/strings.template.js` | 796 | 2157b236 | P |
| `lib/common/templates/compose/object.kt.template.js` | 1043 | f1a6e672 | P |
| `lib/common/templates/css/fonts.css.template.js` | 1380 | 31efab3a | P |
| `lib/common/templates/flutter/class.dart.template.js` | 830 | 92fea35b | P |
| `lib/common/templates/ios-swift/any.swift.template.js` | 1096 | 85f691eb | P |
| `lib/common/templates/ios/colors.h.template.js` | 836 | 3cc943c2 | P |
| `lib/common/templates/ios/colors.m.template.js` | 1012 | 758e27c5 | P |
| `lib/common/templates/ios/macros.template.js` | 729 | b507d9e6 | P |
| `lib/common/templates/ios/plist.template.js` | 1779 | 99440264 | P |
| `lib/common/templates/ios/singleton.h.template.js` | 679 | 6c0af40b | P |
| `lib/common/templates/ios/singleton.m.template.js` | 2499 | d733ba7e | P |
| `lib/common/templates/ios/static.h.template.js` | 700 | d3e41966 | P |
| `lib/common/templates/ios/static.m.template.js` | 783 | 9cecdbc1 | P |
| `lib/common/templates/ios/strings.h.template.js` | 743 | 8667a61a | P |
| `lib/common/templates/ios/strings.m.template.js` | 1677 | 91f357ae | P |
| `lib/common/templates/scss/map-deep.template.js` | 1574 | 8273146a | P |
| `lib/common/templates/scss/map-flat.template.js` | 1266 | 9ac551bd | P |
| `lib/common/templates/static-style-guide/index.html.template.js` | 4478 | 1def2f77 | P |
| `lib/common/transform-utils/colors.js` | 5805 | cee852a8 | P |
| `lib/common/transform-utils/default-filters.js` | 946 | 959c1c68 | P |
| `lib/common/transform-utils/duration.js` | 2112 | 3c666c03 | P |
| `lib/common/transform-utils/typography.js` | 3116 | 137db157 | P |
| `lib/common/transform-utils/value-unit.js` | 2392 | 4326d94d | P |
| `lib/common/transformGroups.js` | 12549 | 454b282f | P |
| `lib/common/transforms.js` | 49666 | b2482612 | P |
| `lib/enums/actions.js` | 169 | 535f4cca | P |
| `lib/enums/commentPositions.js` | 126 | 4cbd63b7 | P |
| `lib/enums/commentStyles.js` | 206 | 3582ddae | P |
| `lib/enums/fileHeaderCommentStyles.js` | 164 | ee2a03e0 | P |
| `lib/enums/formats.js` | 3143 | e622d692 | P |
| `lib/enums/index.js` | 782 | 2c8c97e2 | P |
| `lib/enums/logBrokenReferenceLevels.js` | 137 | e2dae84c | P |
| `lib/enums/logVerbosityLevels.js` | 183 | 98b5ea83 | P |
| `lib/enums/logWarningLevels.js` | 172 | fa4764e7 | P |
| `lib/enums/propertyFormatNames.js` | 203 | e533b2ed | P |
| `lib/enums/sorts.js` | 73 | 29c5f5b5 | P |
| `lib/enums/tokenTypes.js` | 447 | 3b71a4ab | P |
| `lib/enums/transformGroups.js` | 766 | c9802fc6 | P |
| `lib/enums/transformTypes.js` | 173 | 8c5e6f9e | P |
| `lib/enums/transforms.js` | 4369 | 9fa40939 | P |
| `lib/filterTokens.js` | 4026 | c1e901a1 | P |
| `lib/fs-node.js` | 387 | c9fe67fe | P |
| `lib/fs.js` | 722 | 17ad4d27 | P |
| `lib/performActions.js` | 1023 | 075ca2d8 | P |
| `lib/resolve.js` | 746 | e21875d5 | P |
| `lib/transform/config.js` | 7926 | 50f41e95 | P |
| `lib/transform/map.js` | 2814 | 263f8fd5 | P |
| `lib/transform/token.js` | 5220 | de592e82 | P |
| `lib/transform/tokenSetup.js` | 2216 | f07f05d3 | P |
| `lib/utils/cleanActions.js` | 1061 | 833e5bbf | P |
| `lib/utils/combineJSON.js` | 3815 | f53ef969 | P |
| `lib/utils/convertToBase64.js` | 1623 | 5ef8035b | P |
| `lib/utils/convertToDTCG.js` | 5904 | 6ce55206 | P |
| `lib/utils/convertTokenData.js` | 4164 | 5085d77f | P |
| `lib/utils/createFormatArgs.js` | 1379 | ed1dda58 | P |
| `lib/utils/deepExtend.js` | 3748 | 5b7062bc | P |
| `lib/utils/deepmerge.js` | 1068 | 98d7f12b | P |
| `lib/utils/detectDtcgSyntax.js` | 727 | 84e0ee91 | P |
| `lib/utils/downloadFile.js` | 1820 | 5baebc8b | P |
| `lib/utils/expandObjectTokens.js` | 8630 | 72aa151d | P |
| `lib/utils/flattenTokens.js` | 2250 | 60926688 | P |
| `lib/utils/groupMessages.js` | 2562 | 5bf1ed36 | P |
| `lib/utils/index.js` | 1182 | 60013548 | P |
| `lib/utils/isNode.js` | 53 | c6723408 | P |
| `lib/utils/loadFile.js` | 3371 | 032c5d70 | P |
| `lib/utils/preprocess.js` | 1201 | 59ac6a32 | P |
| `lib/utils/references/createReferenceRegex.js` | 399 | 03c3651b | P |
| `lib/utils/references/getName.js` | 348 | 62667d75 | P |
| `lib/utils/references/getPathFromName.js` | 368 | afeaf972 | P |
| `lib/utils/references/getReferences.js` | 3943 | 3e09fe2b | P |
| `lib/utils/references/getValueByPath.js` | 797 | 70a78e23 | P |
| `lib/utils/references/outputReferencesFilter.js` | 1316 | e16414e8 | P |
| `lib/utils/references/outputReferencesTransformed.js` | 1273 | 1a87be3c | P |
| `lib/utils/references/resolveReferences.js` | 6720 | 38d02a44 | P |
| `lib/utils/references/resolveReferencesMap.js` | 5754 | 6feb0bce | P |
| `lib/utils/references/usesReferences.js` | 882 | 36087e6d | P |
| `lib/utils/resolveMap.js` | 3444 | cf39802b | P |
| `lib/utils/resolveObject.js` | 2402 | a390425c | P |
| `lib/utils/stopTransformError.js` | 543 | fa0e75d0 | P |
| `lib/utils/stripMeta.js` | 963 | b8833827 | P |
| `lib/utils/typeDtcgDelegate.js` | 1173 | bfff4fc1 | P |
| `package.json` | 5714 | 5b41329b | P |
| `types/Action.ts` | 548 | 91053c27 | P |
| `types/Config.ts` | 3608 | efa2f035 | P |
| `types/DesignToken.ts` | 2636 | 91497808 | P |
| `types/File.ts` | 1420 | dcdef333 | P |
| `types/Filter.ts` | 230 | 22e56bdd | P |
| `types/Format.ts` | 1126 | 52cbecf9 | P |
| `types/Parser.ts` | 271 | 9341861f | P |
| `types/Preprocessor.ts` | 317 | 94cacf42 | P |
| `types/Sort.ts` | 677 | f013e4e4 | P |
| `types/TokenTypes.ts` | 502 | 46472238 | P |
| `types/Transform.ts` | 890 | b3161a9b | P |
| `types/Volume.ts` | 182 | d531208a | P |
| `types/index.ts` | 1007 | 586e60b4 | P |

</details>


---


---

## Summary table

| D# | Component | Donor @ pin | License | Mode | Zain destination | Files / bytes (selected) | Closure / blocker | Key negative test |
|---|---|---|---|---|---|---|---|---|
| D2 | Design Mode capture | stablyai/orca e310a63 | MIT | PORT-ADAPT | browser-core/design-mode + browser-host-electron | 15 / 92,215 | 6 outside modules; ipc is Electron-bound | payload clamp + secret-leak negatives |
| D3 | CLI catalog + hook listener + OSC 7501 | stablyai/orca e310a63 | MIT | COPY AS-IS (catalog) / PORT-ADAPT | agent-catalog, agent-status | 135 / 760,665 | 44 outside src/shared modules (not closed) | spoofed hook POST rejected |
| D4 | Process host | stablyai/orca e310a63 | MIT | COPY AS-IS (rename) | packages/process-host | 41 / 144,417 | closed (0 outside) | argument-injection corpus on Windows |
| D5 | Linear | stablyai/orca e310a63 | MIT | PORT-ADAPT | packages/integrations-linear | 67 / 358,095 | 19 outside modules; token store | SSRF on inline images |
| D6 | Computer-use sidecar | stablyai/orca e310a63 | MIT | PORT-ADAPT (Phase 9) | packages/computer-use + native | 96 / 712,460 | 8 outside modules; natives unread | deny never reaches sidecar |
| D7 | Diff comments | stablyai/orca e310a63 | MIT | PORT-ADAPT | apps/web diff-comments | 31 / 170,630 | 15 outside; closure 489 modules (store) | stale-anchor comment |
| D7b | Monaco | microsoft/monaco-editor dbf1945 | MIT | DEPEND-ON-PACKAGE | apps/web dependency | 41 / 484,889 | n/a | large-file degrade; CSP workers |
| D11 | Cedar | cedar-policy/cedar 2c2b847 | Apache-2.0 | DEPEND-ON-PACKAGE | crates/core dep =4.14.0 | 299 / 6,587,394 | none | forbid overrides permit; invalid policy refuses start |
| D12a | ACP schema | agent-client-protocol e50f62b | Apache-2.0 | DEPEND (crate) + COPY JSON fixtures | crates/contracts | 51 / 3,111,464 | none | v1/v2 mismatch |
| D12b | ACP Rust SDK | agentclientprotocol/rust-sdk 644377a | Apache-2.0 | DEPEND-ON-PACKAGE | crates/core dep =3.5.0 | 128 / 2,431,507 | schema crate | hung child agent killed |
| D12c | ACP TS SDK | agentclientprotocol/typescript-sdk bca8e49 | Apache-2.0 | DEPEND-ON-PACKAGE (optional) | apps/web dep | 86 / 3,919,779 | none | experimental exports unused |
| D13a | MCP TS SDK | modelcontextprotocol/typescript-sdk b415e60 | Apache-2.0 + MIT mix | DEPEND-ON-PACKAGE | apps/server dep | 95 / 1,185,963 | core-internal inlined (UNKNOWN) | rug-pull detection |
| D13b | MCP Rust SDK rmcp | modelcontextprotocol/rust-sdk cd88056 | Apache-2.0 + MIT mix | DEPEND-ON-PACKAGE | crates/core dep =3.8.0 | 78 / 2,121,715 | rmcp-macros | conformance crate |
| D19 | Excalidraw | excalidraw/excalidraw 808d068 | MIT | DEPEND-ON-PACKAGE | apps/web dep + design-canvas | ? / ? | fonts license UNKNOWN | huge-scene degrade |
| D20 | Onlook element mapping | onlook-dev/onlook 423e2e9 | Apache-2.0 | PORT-ADAPT | packages/design-source-map | 25 / 62,933 | MobX engine not copied | list-loop ambiguity |
| D21 | Style Dictionary | style-dictionary f82e7aa | Apache-2.0 | DEPEND-ON-PACKAGE | packages/design-tokens | 124 / 390,849 | none | circular alias fails |
| D9 | Codex sandbox set (9 crates) | openai/codex 603a7ba | Apache-2.0 + NOTICE; bwrap bundles LGPL-2.0 C | per crate: process-hardening, execpolicy COPY AS-IS; sandboxing, network-proxy, windows-sandbox-rs, mxc, linux PORT-ADAPT; windows-sandbox-service, bwrap REFERENCE | vendor/codex/* | 357 / 3,805,021 (9 crates) | needs protocol, pty, otel, http-client, uds, utils-*; service needs codex-core | child cannot escape roots/network; Job Object kill |
