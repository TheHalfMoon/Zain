# R13 — IDE, Debug and Platform Gap Closure (WePLD V3)

```text
STATUS      = RESEARCH (planning only). Nothing installed, built, run, admitted or copied.
DATE        = 2026-10-27 (all "accessed" dates below are this date unless stated)
INPUTS      = 07_TARGET_ARCHITECTURE_AND_UX.md, 06_SOURCE_TRANSPLANT_MATRIX.md, ADR.md (ADR-002/003/007),
              R02_T3_CODE.md §12 (T3 gaps: no LSP, no debugger, light editor), R03D_ORCA.md §9–10 (Monaco without LSP)
METHOD      = `gh api` for licenses (root license file read where GitHub reports NOASSERTION), HEAD SHAs, trees and
              raw files at a pinned ref; local clones of T3 @36d4d711 and Orca @e310a636 were read before they were
              removed from the workspace mid-session (re-reads of Orca done via `gh api` at the same SHA);
              vendor docs via web fetch where stated.
LABELS      = VERIFIED (read at source/pin) | INFERRED (reasoned from verified facts) | UNKNOWN (not verifiable here)
ESTIMATES   = person-weeks (pw), solo founder + AI assistance, same basis as R02 §14. All are ESTIMATES.
NON-GOALS   = no change to other files; ADR-003 ("no LSP in v1") is NOT amended here — §2 gives a proposal only.
```

Citation format: `owner/repo@sha12:path` (accessed 2026-10-27). Local-pin citations for T3/Orca use the same form.

---

## 0. Summary of findings that change existing plan text

| # | Finding | Evidence | Effect on plan |
|---|---|---|---|
| F1 | **Azure Trusted Signing (renamed "Artifact Signing") is NOT available to the founder.** Public Trust is offered to organizations in US, CA, EU, UK, AU, NZ, JP, KR, SG, CH, NO, IL; individuals only in US or Canada. Paid subscription required. | learn.microsoft.com/en-us/azure/artifact-signing/quickstart (Prerequisites note; page updated 2026-10-08) | Closes the UNKNOWN in `07` §9: Windows signing = OV certificate with cloud-HSM key (§6). T3's own release pipeline (Azure Trusted Signing + jsign) cannot be inherited as-is. |
| F2 | `anthropics/sandbox-runtime` **now has a Windows backend (alpha)**: dedicated `srt-sandbox` local user, WFP egress fence keyed on that SID, write-restricted token, explicit ACEs. | `anthropics/sandbox-runtime@98a4016d:README.md` L109, L128, §"Windows (alpha)", §"Known limitations" | `06` D10 says "not native Windows" — outdated. Still alpha, machine-wide install, UAC prompt. |
| F3 | Codex Windows sandbox is **not AppContainer** in its default backends: it uses `CreateRestrictedToken(DISABLE_MAX_PRIVILEGE \| LUA_TOKEN \| WRITE_RESTRICTED)` with capability SIDs (unelevated), or dedicated sandbox **local users** + **WFP** filters + a Windows service (elevated). A third backend, **MXC**, routes into Microsoft's `BaseContainerRunner`. | `openai/codex@603a7baff0f6:codex-rs/windows-sandbox-rs/src/token.rs` L21–44, L500; `.../setup_provisioning/sandbox_users.rs` (NetUserAdd); `.../wfp.rs`; `codex-rs/mxc-sandbox/README.md` | `R02` WP6 wording "Windows job objects/AppContainer" is imprecise; §3 corrects it. |
| F4 | Codex Linux seccomp **denies `ptrace`, `process_vm_readv/writev`** in all but one mode. | `openai/codex@603a7baff0f6:codex-rs/linux-sandbox/src/seccomp.rs` L192–195 | Debuggers cannot run inside the P8 Linux sandbox as-is (§1 R-D4). |
| F5 | T3's terminal is a **Canvas-2D libghostty-vt renderer with no screen-reader support found** (no `aria-live`/screen-reader hits under `apps/web/src/terminal`). | `pingdotgg/t3code@36d4d711:apps/web/src/terminal/ghostty/{README.md,renderer.ts}` | WCAG 2.2 AA blocker for the terminal (§7). |
| F6 | T3 **already drives Electron `webContents` with Playwright** through a CDP relay (`connectOverCDP`) and exposes 12 `preview_*` MCP tools incl. recording. | `t3code@36d4d711:apps/desktop/src/preview/CdpRelay.ts`, `apps/server/src/preview/ServerBrowserContexts.ts` L111/163/185, `apps/server/src/mcp/toolkits/preview*` | Browser automation is a gating job, not a build job (§4). |
| F7 | `microsoft/monaco-editor` now contains an **official alpha LSP client** `@vscode/monaco-lsp-client` 0.1.0 (22 language features) over plain `monaco-editor-core`. | `microsoft/monaco-editor@dbf1945df2ff:monaco-lsp-client/{package.json,README.md,src/adapters/languageFeatures/}` | A lighter alternative to monaco-languageclient (§2). |
| F8 | `debugpy` vendors **pydevd under EPL-1.0**. | `microsoft/debugpy@671f6c7d1b22:src/debugpy/_vendored/pydevd/LICENSE-EPL` | Do not bundle debugpy; resolve from user's Python env (§1). |
| F9 | TypeScript 7 (native) shipped (v7.0.2, 2026-08-20) and has a built-in LSP: `tsc --lsp --stdio` (stdio only). `microsoft/typescript-go` is archived. | `microsoft/TypeScript@1f82f368b668:tsc/cmd/tsc/lsp.go` L21–35; releases API | Changes the default TS server choice (§2). |

---

## 1. Debugging (Debug Adapter Protocol)

### 1.1 Donor candidates

| Candidate | Pin (HEAD 2026-10-27) | License (verified) | What it gives | Coupling | Decision |
|---|---|---|---|---|---|
| `@vscode/debugprotocol` 1.68.0 (+ `@vscode/debugadapter` test support) | `microsoft/vscode-debugadapter-node@53d9de511fc6` (`protocol/`, `adapter/`, `testSupport/`) | MIT (`License.txt`) | Generated TypeScript types for DAP; `testSupport` DebugClient for adapter conformance tests | none | **INTEGRATE** (types + test client) |
| DAP spec / JSON schema | `microsoft/debug-adapter-protocol@c10f18c3332c` (`debugAdapterProtocol.json`; changelog at 1.71.x) | Docs CC-BY 3.0 US; code MIT (`License.txt`) | Normative spec | none | **REFERENCE** |
| VS Code debug model/UI | `microsoft/vscode@df5c887e7961:src/vs/workbench/contrib/debug/` | MIT | Mature model (sessions, threads, stack, variables, breakpoints, `startDebugging` child sessions) | very high (VS Code DI, workbench views) | **REFERENCE; port small pure model files only** with attribution |
| `@codingame/monaco-vscode-debug-service-override` | `CodinGame/monaco-vscode-api@9e70dd83a1d1:src/service-override/debug/{classic,session}.ts` | MIT | VS Code's real debug UI inside Monaco "extended mode" | requires replacing `monaco-editor` with `@codingame/monaco-vscode-editor-api` and many service overrides; monthly majors (v37 now) | **OPTION B** (only if §2 picks monaco-languageclient extended mode) |
| monaco-languageclient debugger glue | `TypeFox/monaco-languageclient@661fa992fa96:packages/client/src/debugger/index.ts`, `packages/examples/src/debugger/server/{DAPSocket,debugServer}.ts` | MIT | DAP-over-WebSocket example wiring to the CodinGame debug service | as above | **REFERENCE** |
| OpenSumi `@opensumi/ide-debug` | `opensumi/core@9da5ceb24364:packages/debug` | MIT (repo + package.json) | Full debug module (Electron/web IDE) | high: OpenSumi DI, `ide-core-browser`, `ide-monaco`, `ide-terminal-next`, `ide-task`… (package.json deps) | **REFERENCE; port selected view/model code (MIT)** |
| Eclipse Theia `@theia/debug` 1.76.0 | `eclipse-theia/theia@f47c3ea8a4ad:packages/debug` | **EPL-2.0 OR GPL-2.0-only WITH Classpath-exception-2.0** (package.json) | Full debug module | high: Theia DI/widgets | **REFERENCE ONLY — do not copy code** |
| nvim-dap | `mfussenegger/nvim-dap` | GPL-3.0 | Adapter launch recipes | n/a | REFERENCE (configs only, facts not code) |
| Zed debugger | `zed-industries/zed` | GPL-3.0/AGPL per crate (repo ships LICENSE-GPL, LICENSE-APACHE) | — | — | REJECT (already "reference only" in `06`) |

**EPL-2.0 copyleft assessment (Theia).** EPL-2.0 is file-level weak copyleft: if WePLD distributes binaries containing EPL-licensed files (modified or not), it must make the source of those EPL files available under EPL and include the notice. Combining EPL files with separately written proprietary modules is allowed (the "separate module" rule). Because the repository stays private (`ADR-010`), copying Theia files would create a source-disclosure obligation for exactly those files on every release, plus provenance tracking. The benefit is small, since MIT donors (OpenSumi, VS Code) cover the same ground. **Decision: no Theia code; reading for design is fine.** (INFERRED from the license text; not legal advice.)

### 1.2 Adapters to support

| Language | Adapter | Pin / version | License (verified) | Launch | Distribution decision |
|---|---|---|---|---|---|
| Node / browser / Electron / WebView2 | `vscode-js-debug` standalone DAP server | `microsoft/vscode-js-debug@a9df0307248d`, release asset `js-debug-dap-v1.140.0.tar.gz` | MIT | `node dapDebugServer.js <port>` (TCP; uses DAP `startDebugging` child sessions) | **Bundle** (MIT; pin + sha256) or download-on-first-use |
| Python | `debugpy` | `microsoft/debugpy@671f6c7d1b22` | MIT, **but vendors pydevd under EPL-1.0** | `python -m debugpy.adapter` (stdio) | **Do not bundle**: resolve from user's interpreter/venv; offer gated `pip install debugpy` |
| Rust / C / C++ (all OS) | CodeLLDB | `vadimcn/codelldb@62def434dc22`, release v1.12.3 (per-platform `.vsix`) | MIT (bundles LLDB: Apache-2.0 WITH LLVM-exception) | `codelldb --port N` from the extracted `.vsix` | Download-on-first-use, pinned per platform |
| Rust / C / C++ (alt) | `lldb-dap` | `llvm/llvm-project@3a46435bd28e:lldb/tools/lldb-dap` | Apache-2.0 WITH LLVM-exception | `lldb-dap` (stdio) | Use if present (Xcode CLT on macOS; LLVM installer on Windows) |
| Go | Delve `dlv dap` | `go-delve/delve@a439ae64ea3c:service/dap` | MIT | `dlv dap --listen 127.0.0.1:N` | User toolchain (`go install`) |
| .NET | netcoredbg | `Samsung/netcoredbg@9744e1f05186` | MIT | `netcoredbg --interpreter=vscode` | Download-on-first-use. Note: Microsoft `vsdbg` is licensed only for Microsoft IDEs — do not use (INFERRED from its known license; UNVERIFIED here). |

Windows MSVC-toolchain Rust/C++ debugging via LLDB has partial PDB support (INFERRED); the Microsoft `cppvsdbg` engine is not redistributable (UNKNOWN terms; treat as unavailable).

### 1.3 Integration design (Electron + forked T3 Server + Rust Core)

```text
Renderer (React)                      WePLD Server (Node, forked T3)                       Core (Rust)
───────────────                       ─────────────────────────────                        ───────────
Run & Debug panel  ── WS RPC ──▶  DebugSessionService (Effect service)
 call stack / vars /                 ├─ DapClient (own, typed by @vscode/debugprotocol)
 watch / breakpoints /               │    stdio | TCP framing (Content-Length)
 debug console                       ├─ AdapterRegistry (pinned binaries, sha256)
Monaco glyph-margin BPs,             ├─ reverse requests:
 inline values, current-line         │    runInTerminal ─▶ TerminalManager (PTY) ─┐
 decoration                          │    startDebugging ─▶ child DapClient       │
                                     └─ every spawn/attach/evaluate ── effect.propose / dispatch ─▶ Nawat PDP
                                                     │                                              ledger
                                         Containment launcher (Job Object floor P3; sandbox P8) ◀── grant
```

- **One DAP client, server-side.** The adapter runs where the code runs (local Server or headless runner). The
  renderer only shows state (T3 principle: server-first). The client handles `initialize`, `launch`/`attach`,
  `setBreakpoints`, `configurationDone`, `threads`, `stackTrace`, `scopes`, `variables`, `evaluate`, `continue`/`next`/
  `stepIn`/`stepOut`/`pause`, `disconnect`/`terminate`, plus reverse requests `runInTerminal` and `startDebugging`
  (required by js-debug).
- **Launch configs:** read `.vscode/launch.json` (JSONC) for compatibility, plus `.wepld/launch.json`. Variable
  substitution (`${workspaceFolder}`, `${file}`) is done server-side against the **worktree** root, not the main checkout.
- **UI build-vs-borrow:** build panels in React against T3's design system (call stack tree, variables tree with lazy
  `variablesReference` expansion, breakpoints list, debug console with REPL `evaluate`). Port MIT model logic from
  VS Code / OpenSumi (attribution in `THIRD_PARTY_NOTICES/`). Monaco integration: glyph-margin decorations, hover
  `evaluate` with `context: "hover"`, inline values via decorations.

**Core-gated effects (new effect classes, proposal for Nawat):**

| Effect class | Trigger | Default policy | Replay class | Notes |
|---|---|---|---|---|
| `process.spawn.debug_adapter` | starting a pinned adapter binary | allow if binary hash is in the registry; else approval | NEVER | adapter is a long-lived child; owned by a Job Object |
| `process.spawn.debuggee` | DAP `launch` (adapter spawns program) or `runInTerminal` | approval in Manual; auto in Auto-with-review if the command matches a saved config | NEVER | the adapter spawns the debuggee itself → **UNMEDIATED** unless the adapter runs under containment (its children inherit the Job Object/sandbox) |
| `process.attach.debug` | DAP `attach` to PID / remote port | **always approval** (WebAuthn) | NEVER | memory read of another process; block attach to processes not started in this session unless the user picks the PID |
| `debug.evaluate` | `evaluate` with `context: "repl"` or watch/hover with side effects | approval for agents; auto for the human UI | NEVER | arbitrary code execution inside the debuggee |
| `debug.read` | `stackTrace`/`scopes`/`variables` | auto (SAFE) | SAFE | output goes through secret redaction before it reaches an agent |

**Agent-assisted debugging (MCP).** Add a `debug` toolkit to T3's `/mcp` (pattern: `apps/server/src/mcp/toolkits/*`):
`debug_sessions`, `debug_stack`, `debug_variables(ref, depth≤3, maxItems)`, `debug_breakpoints_set`,
`debug_step`, `debug_evaluate`, `debug_launch(configName)`. Read tools → `debug.read`; `debug_launch` →
`process.spawn.*`; `debug_evaluate` → `debug.evaluate` (approval). Outputs are size-clamped (Orca's payload clamp idea,
`06` D3) and secrets-redacted (env vars, tokens matching known patterns). Every agent action carries `origin=agent` in
`effect.propose` so Trusted Completion can tell agent-driven debugging from human-driven debugging.

### 1.4 Effort, risks, acceptance

**ESTIMATE:** DAP client + registry + gating 2–3 pw; React debug UI + Monaco decorations 2–4 pw; adapters (js-debug,
debugpy, CodeLLDB, Delve, netcoredbg) wiring + configs 1–2 pw; MCP debug toolkit 1 pw. **Total 6–10 pw.**
Option B (CodinGame debug service) could cut UI work to ~1–2 pw but only if the editor stack moves to extended mode (§2).

| Risk | Note | Mitigation |
|---|---|---|
| R-D1 js-debug child sessions | `startDebugging` multi-session trees are the main complexity | implement child sessions from the start; conformance tests against js-debug |
| R-D2 Adapter supply chain | adapters are native binaries fetched at runtime | pinned version + sha256 in a WePLD-signed manifest; download is a gated `tool.install` effect |
| R-D3 Debuggee spawned by adapter is unmediated | Core sees the adapter spawn, not the child | run adapters under the containment launcher; report debuggee PID via DAP `process` event to Core |
| R-D4 Sandbox vs debugger | codex Linux seccomp denies ptrace (F4); Seatbelt base policy allows `process-info*` only for `same-sandbox` (`seatbelt_base_policy.sbpl` L15–16), so cross-sandbox `task_for_pid` is INFERRED blocked | in P8, debug sessions run under a dedicated "debug profile" (ptrace allowed inside the sandbox's own PID namespace); until then, Job Object floor only and UI states it |
| R-D5 Secrets in variables | variables views expose tokens to agents | redaction filter on `debug.read` outputs to agents (not to the human UI) |
| R-D6 EPL contamination | accidental copy from Theia/pydevd | provenance gate: CI grep for EPL headers in `packages/**` |

| ID | Acceptance test |
|---|---|
| DBG-AT-01 | Node: launch `server.js`, breakpoint hit, stack shows ≥2 frames, variables expand, step over, continue, terminate; adapter and debuggee processes gone (Job Object) |
| DBG-AT-02 | Browser/Electron via js-debug: `startDebugging` child session appears and is torn down with its parent |
| DBG-AT-03 | Python via user venv `debugpy`: missing debugpy → gated install prompt; nothing installed without approval |
| DBG-AT-04 | Rust via CodeLLDB on Windows/macOS/Linux: breakpoint in `main.rs` of a worktree (paths resolve to the worktree, not the main checkout) |
| DBG-AT-05 | Go via `dlv dap`; .NET via netcoredbg: launch/breakpoint/variables |
| DBG-AT-06 | `attach` to an arbitrary PID without an assertion → refused by Core; ledger shows `process.attach.debug` DENIED |
| DBG-AT-07 | Agent calls `debug_evaluate` → Inbox approval; denied → no evaluate request reaches the adapter (DAP trace) |
| DBG-AT-08 | Agent `debug_variables` output has `AWS_SECRET_ACCESS_KEY` value redacted; the human panel shows it |
| DBG-AT-09 | Adapter binary with a wrong sha256 → spawn refused |
| DBG-AT-10 | `@vscode/debugadapter` testSupport conformance suite passes against our client using a mock adapter |

---

## 2. LSP in Monaco

### 2.1 Client options

| Option | Pin | License | Shape | Pros | Cons |
|---|---|---|---|---|---|
| **A. `monaco-languageclient` 11.0.3** (+ `vscode-ws-jsonrpc` 4.0.3, `@typefox/monaco-editor-react` 8.0.3) | `TypeFox/monaco-languageclient@661fa992fa96` | MIT (root `LICENSE`) | Runs the real `vscode-languageclient` inside Monaco via `@codingame/monaco-vscode-api` 37.6.0 (aligned with VS Code 1.138.0, monaco-editor 0.57.0) | full LSP feature parity with VS Code; debug UI available too (§1, Option B) | **replaces `monaco-editor` with `@codingame/monaco-vscode-editor-api`** (README L74–84; troubleshooting "overrides"); version lock-step with monthly CodinGame majors; larger bundle; Orca's patched `monaco-editor@0.55.1` (R03D) cannot be reused unchanged |
| **B. `@vscode/monaco-lsp-client` 0.1.0** | `microsoft/monaco-editor@dbf1945df2ff:monaco-lsp-client/` | repo MIT (`LICENSE.txt`); package.json has no `license` field (INFERRED MIT); deps `@hediet/json-rpc*` 0.5 — repo `hediet/typed-json-rpc` has **no license file at root → UNKNOWN** | Thin client over plain `monaco-editor-core`; 22 features (completion, hover, definition, references, rename, code actions, diagnostics, formatting, inlay hints, semantic tokens, signature help, …) | small; keeps vanilla Monaco (matches `06` D7 pin and Orca diff-comments) | **alpha** ("might contain many bugs"); last commits June 2026; license of json-rpc dep UNKNOWN |
| C. Own thin client | `microsoft/vscode-languageserver-node@82ed8ac580bc` (`vscode-jsonrpc`, `vscode-languageserver-protocol`; `vscode-languageclient` 11.0.0) | MIT | Map LSP → Monaco providers ourselves (B is a template) | full control; MIT-only deps | most work |

**Recommendation (proposal; amends ADR-003 only if accepted):** a 1-week **spike** comparing A and B on bundle size,
Orca diff-comment compatibility, feature coverage and TS/Python/Rust behavior. Default expectation: **B wrapped behind
a WePLD `LspBridge` interface, with C as the fallback** (fork/vendor B into WePLD if upstream stalls; swap
`@hediet/json-rpc` for `vscode-jsonrpc` if its license stays UNKNOWN). Choose A only if the founder also wants VS Code's
debug UI via CodinGame (Option B in §1) and accepts the monthly version lock-step.

### 2.2 Server-side lifecycle (forked T3 Server)

- `LanguageServerManager` (Effect service) keyed by `(worktreeRoot, languageId)`; spawn via stdio with `vscode-jsonrpc`
  `StreamMessageReader/Writer`; lazy start on first open document; idle shutdown (e.g. 10 min); LRU cap on concurrent
  servers and RSS budget (rust-analyzer can use several GB — INFERRED); restart with backoff; crash → diagnostics
  banner, not a modal.
- Transport to the renderer: tunnel JSON-RPC messages over T3's existing WS RPC as an opaque channel
  `lsp/<sessionId>` (no second socket, inherits T3 scoped/DPoP auth). Works unchanged for remote/headless runners.
- **URI rewriting at the Server:** documents use `file://<worktree>/…` on the Server; the renderer sees a
  `wepld://<projectId>/<worktreeId>/…` scheme, so remote paths and Windows drive letters never leak into UI state and
  two worktrees of one repo never share a server.
- **Server→client requests that cause effects are gated, not auto-applied:**

| LSP message | Risk | Handling |
|---|---|---|
| `workspace/applyEdit` | file writes outside the open buffer | becomes an `fs.write` proposal (MEDIATED) unless it results from a user-invoked action (rename, code action) in the human UI |
| `window/showDocument` with `external: true` | opens URLs | `os.open_url` proposal |
| `workspace/executeCommand` (client→server, from code actions) | some servers run tools | allowlist per server |
| server startup itself | **code execution from the repo**: rust-analyzer runs build scripts / proc-macros; tsserver loads `compilerOptions.plugins` from `node_modules`; gopls runs `go list` (INFERRED from well-known behavior) | `process.spawn.language_server` effect; **untrusted-workspace mode** starts servers with execution features off (rust-analyzer `cargo.buildScripts.enable=false`, `procMacro.enable=false`; tsserver plugins disabled) until the user trusts the project |

### 2.3 Default servers

| Language | Default | Pin / version | License (verified) | Source of binary | Alternatives |
|---|---|---|---|---|---|
| TS/JS (project uses TS ≥ 7) | `tsc --lsp --stdio` (TypeScript 7 native) | `microsoft/TypeScript@1f82f368b668:tsc/cmd/tsc/lsp.go`; v7.0.2 (2026-08-20), v7.1-beta | Apache-2.0 | project's own `node_modules` (INFERRED: npm `typescript@7` carries the native binary) | — |
| TS/JS (TS ≤ 6) | `vtsls` (wraps the workspace tsserver) | `yioneko/vtsls@9ff4ce433cd4` | MIT (root LICENSE) | bundled (pure JS) | `typescript-language-server@7b28f104e741` — MIT + Apache-2.0 parts (LICENSE contains both) |
| Python | `basedpyright` v1.40.2 | `DetachHead/basedpyright@5fb7d7afc7e6` | MIT (LICENSE.txt, pyright-derived) | bundled (JS) or pip | `pyright@611afe615b86` (MIT); `astral-sh/ty@0445d6497ae2` (MIT, still 0.0.92 → not default) |
| Rust | `rust-analyzer` | `rust-lang/rust-analyzer@889bb47e8530` | MIT OR Apache-2.0 (LICENSE-MIT + LICENSE-APACHE) | user toolchain (`rustup component add rust-analyzer`) | — |
| Go | `gopls` | `golang/tools@c1193aca3e6b:gopls` | BSD-3-Clause | user toolchain (`go install`) | — |

Policy: bundle only pure-JS servers (vtsls, basedpyright); never bundle toolchain servers; on-demand downloads are a
gated `tool.install` effect with pinned version + sha256.

### 2.4 Effort, risks, acceptance

**ESTIMATE:** spike 1 pw; LspBridge + Monaco wiring (option B/C) 2–4 pw; LanguageServerManager + URI rewriting + gating
2–3 pw; trust mode + default servers 1–2 pw. **Total 6–10 pw** (A: similar total, more risk in upgrades).

| Risk | Mitigation |
|---|---|
| Monaco fork divergence (A) vs alpha client (B) | spike + `LspBridge` abstraction; vendor B if needed |
| Memory (multiple worktrees × servers) | per-worktree LRU, RSS budget, idle shutdown; measured in B2 benchmark |
| Remote latency (runner) | completion debounce; incremental sync (`TextDocumentSyncKind.Incremental`) |
| Code execution by servers on untrusted repos | untrusted-workspace defaults (§2.2) |

| ID | Acceptance test |
|---|---|
| LSP-AT-01 | TS project: completion, hover, go-to-definition across files, diagnostics within 2 s of edit (fixture repo) |
| LSP-AT-02 | Two worktrees of the same repo → two server instances; definition in worktree B never opens a worktree A file |
| LSP-AT-03 | Python (basedpyright), Rust (rust-analyzer), Go (gopls) parity smoke: completion + definition + diagnostics |
| LSP-AT-04 | Server-initiated `workspace/applyEdit` with no user action → Inbox proposal; no file changed before approval |
| LSP-AT-05 | Untrusted repo with a malicious `build.rs` → rust-analyzer starts with build scripts disabled; marker file not created |
| LSP-AT-06 | Kill a language server → restart with backoff, open buffers resynced, no renderer reload |
| LSP-AT-07 | Remote runner: LSP traffic flows over the existing authenticated WS; no extra port opened (netstat check) |
| LSP-AT-08 | Orca diff-comments (D7 port) still work with the LSP-enabled Monaco build |

---

## 3. Cross-platform containment detail

### 3.1 What each donor backend enforces (verified at source)

| OS / backend | Mechanism | Filesystem | Network | Process | Source |
|---|---|---|---|---|---|
| **Windows — codex "restricted token" (unelevated)** | `CreateRestrictedToken` with `DISABLE_MAX_PRIVILEGE \| LUA_TOKEN \| WRITE_RESTRICTED`, capability SIDs as restricting SIDs; ACLs applied to workspace roots; deny-read ACLs | writes only where the capability SID was granted (ACEs on writable roots); deny-read via ACL walker | **not enforced by token alone** (INFERRED; WFP is in the elevated path) | Job Objects (`Win32_System_JobObjects` feature) | `openai/codex@603a7baff0f6:codex-rs/windows-sandbox-rs/src/{token.rs L21–44 L470–501, workspace_acl.rs, deny_read_acl.rs}`, `Cargo.toml` L74 |
| **Windows — codex "elevated"** | setup (UAC) creates dedicated **local sandbox users** (`NetUserAdd`, group membership), **WFP** filters on `FWPM_CONDITION_ALE_USER_ID` (block egress except loopback proxy ports), a Windows service, DPAPI-protected credentials; command runner over named pipe | per-user ACLs | WFP egress fence for the sandbox identity + loopback proxy (`proxy_ports`, `allow_local_binding`) | separate user + Job Object | `.../setup_provisioning/{sandbox_users.rs,firewall.rs,service.rs}`, `.../wfp.rs`, `.../elevated/*`, `lib.rs` L50–57; `codex-rs/windows-sandbox-service/` |
| **Windows — codex MXC** | Microsoft MXC `BaseContainerRunner`; needs PSEC; kill-on-close job; no ACL edits, no users, no elevation | BaseContainer path policy (deny > RO > RW); hard-link and volume-root alias limitations documented | loopback only (incl. proxy listeners); no direct egress, no inbound | clipboard, input injection, desktop/system control restricted | `codex-rs/mxc-sandbox/README.md` (L1–60). Availability on consumer Windows 11 Home: **UNKNOWN** |
| **macOS — codex Seatbelt** | `/usr/bin/sandbox-exec` (absolute path only) with generated SBPL: `seatbelt_base_policy.sbpl` (`(deny default)`, Chrome-derived), `seatbelt_network_policy.sbpl`, `seatbelt_preferences_policy.sbpl`, `seatbelt_read_only_platform_defaults.sbpl` | read-only by default; writable roots added; protected paths | network only via added policy / proxy port | `process-info*`/signal only `same-sandbox` | `codex-rs/sandboxing/src/seatbelt.rs` L21–28, L58–62; the four `.sbpl` files in `codex-rs/sandboxing/src/` |
| **Linux — codex bwrap + seccomp** | bubblewrap (system `bwrap` outside CWD, else bundled `codex-resources/bwrap`), `PR_SET_NO_NEW_PRIVS`, seccomp; legacy Landlock retained but **rejected for filesystem-restricted policies** (cannot isolate app-server Unix sockets) | `--ro-bind / /` + `--bind` writable roots; `.git`, resolved gitdir, `.codex` re-bound RO; symlink/missing-path masking with `/dev/null`; deny-globs pre-expanded via `rg` | `--unshare-net` or managed proxy (TCP→UDS→TCP bridge); seccomp blocks network syscalls when restricted; `AF_VSOCK` and `io_uring` always blocked | `--unshare-user`, `--unshare-pid`, fresh `/proc`; seccomp denies `ptrace`, `process_vm_readv/writev` | `codex-rs/linux-sandbox/README.md`; `src/seccomp.rs` L185–220; `codex-rs/sandboxing/src/{bwrap.rs,landlock.rs}` |
| **All — codex process hardening** | pre-main: no core dumps, no ptrace attach (Linux/macOS), strip `LD_PRELOAD`/`DYLD_*` | — | — | — | `codex-rs/process-hardening/README.md` |
| **anthropics/sandbox-runtime (srt)** | macOS `sandbox-exec` dynamic profiles; Linux bubblewrap + seccomp (BPF from `vendor/seccomp-src`); **Windows (alpha)**: `srt-sandbox` local user + WFP fence + write-restricted token + ACEs | allow/deny read & write lists | **allow-only domain lists via host HTTP + SOCKS5 proxies**; resolved-address check (blocks loopback/link-local/metadata/own-interface IPs); optional TLS termination | macOS violation log tap; violation attribution per command | `anthropics/sandbox-runtime@98a4016d:README.md` L5, L48, L107–130, L464–468, §Windows Known limitations |

**Documented limitations to carry into WePLD claims (verified):** srt Windows — system resolver DNS not fenced; SMB
traffic via kernel redirector not fenced; a process that impersonates the anonymous token or derives a restricted token
from its own escapes the WFP fence; per-user tool installs unreachable without a profile read grant; proxy auth token
visible on runner argv; machine-wide account shared across Windows users. MXC — hard-link names keep independent
permissions; volume-root alias widening. Linux — WSL1 unsupported; bundled bwrap fallback; Landlock alone insufficient.

### 3.2 How WePLD Core invokes them (design)

```text
Server EffectWorker ─effect.propose(process.spawn.provider|tool|debug_adapter|language_server)─▶ Core Nawat
Core: decision + SandboxProfile{fs_rw[], fs_ro[], fs_deny[], net: none|proxy(allowlist)|full, proc: tree-kill,
                                ptrace: deny|same-sandbox, gui: deny|allow}
Core containment launcher (Rust, owned crate `wepld-contain`):
  windows: P3 floor = Job Object (kill-on-close, UI restrictions) + deny-root profile in provider configs
           P8 = codex restricted-token backend (vendored) ; elevated backend opt-in (UAC once) ; MXC when available
  macos:   P8 = sandbox-exec /usr/bin only + SBPL rendered from SandboxProfile (start from codex .sbpl files)
  linux:   P8 = bwrap + seccomp helper (vendored codex-linux-sandbox, or system bwrap)
  network: Core-owned loopback proxy (codex network-proxy or srt-style allowlist) — egress decisions logged to ledger
Core returns {pid, job_handle_ref, profile_digest} ─▶ effect.dispatch fsynced ─▶ Server attaches stdio
```

- **Vendoring cost (verified coupling):** `codex-windows-sandbox` depends on `codex-protocol`, `codex-utils-pty`,
  `codex-otel`, `codex-http-client`, `codex-utils-process` …; `codex-linux-sandbox` on `codex-sandboxing`,
  `codex-network-proxy`, `codex-process-hardening`, `codex-protocol`, `codex-uds` (dev-dep `codex-core`)
  (`Cargo.toml` files at the pin). Plan to vendor into `third_party/codex-sandbox/` with a shim for `codex-protocol`
  types; keep Apache-2.0 NOTICE and change notes.
- **srt option:** WRAP `@anthropic-ai/sandbox-runtime` from the Node Server for macOS/Linux early (P5–P6) as a
  stop-gap, but Core must still own the decision; srt runs the launch. On Windows prefer the codex backends
  (Rust, in-process with Core) over srt alpha (machine-wide account + UAC) — revisit after a spike.

**ESTIMATE:** Windows restricted-token backend + Job Objects 3–5 pw; macOS Seatbelt profile rendering 1–2 pw; Linux bwrap
helper 1–2 pw; Core-owned egress proxy + ledger logging 2–3 pw; escape suite 2 pw. **Total 9–14 pw** (vs `06` D9 4–10 pw —
the earlier figure omits the proxy and the escape suite).

| Risk | Mitigation |
|---|---|
| Coupling to `codex-protocol` churn | vendored snapshot; re-pin per phase only |
| Elevated backend creates OS users + persistent WFP filters (system change) | opt-in only, explicit UAC, `wepld-core sandbox uninstall` removes users/filters (mirrors codex `uninstall_windows/`) |
| Overclaiming | trust indicator text derived from the actual backend in use (e.g. "Windows restricted token: writes contained; network NOT contained") |

| ID | Acceptance test |
|---|---|
| SBX-AT-01 | Write outside the worktree / into `%APPDATA%\WePLD` from a contained process fails on all 3 OS |
| SBX-AT-02 | `.git` and `.wepld` inside a writable worktree remain read-only |
| SBX-AT-03 | Network: `curl https://example.com` blocked when net=none; allowed host passes via proxy with a ledger row; cloud metadata IP 169.254.169.254 blocked |
| SBX-AT-04 | Process tree killed on Core grant revocation (Job Object / PID namespace) — no orphan after 2 s |
| SBX-AT-05 | Linux: `io_uring_setup` and `AF_VSOCK` socket fail inside the sandbox |
| SBX-AT-06 | macOS: profile invoked via `/usr/bin/sandbox-exec` even if a `sandbox-exec` earlier on PATH exists |
| SBX-AT-07 | Uninstall of the elevated Windows backend leaves no sandbox users or WFP filters |
| SBX-AT-08 | Trust indicator reflects the backend's real guarantees (snapshot test per backend) |

---

## 4. Controlled browser automation

### 4.1 Options

| Option | Pin | License | Where it runs | Verdict |
|---|---|---|---|---|
| Electron `webContents.debugger` (CDP, one debugger per webContents) | `electron/electron@3dfc698827c5` (docs: electronjs.org/docs/latest/api/debugger) | MIT | Desktop main | **KEEP** — T3 already shares one attachment via `CdpRelay` (`t3code@36d4d711:apps/desktop/src/preview/CdpRelay.ts` L1) |
| `playwright-core` in the Server (`connectOverCDP` to the relay; `chromium.launch`/`launchPersistentContext` for headless) | `microsoft/playwright@a169686c61af` (T3 pins 1.60.0; latest 1.64.1) | Apache-2.0 | Server | **KEEP** (T3 `ServerBrowserContexts.ts` L111, L163, L185) — works for headless runners too |
| `microsoft/playwright-mcp` v0.0.83 | `microsoft/playwright-mcp@0c4107acbecb` | Apache-2.0 | separate MCP process | **REFERENCE** (tool schemas); README states it is "**not** a security boundary" and `--allowed-origins/--blocked-origins` "*does not* serve as a security boundary" (README L410–412, L823–826) |
| `vercel-labs/agent-browser` | `@edb40f187886` | Apache-2.0 | CLI | REFERENCE (Orca uses it, R03D) |

### 4.2 Hard-block categories — implementation pattern (defense in depth)

Hard blocks are Core policy rules of class `BLOCKED` that "Skip" can never override (ADR-007). Enforcement points:

| Layer | Mechanism | Catches |
|---|---|---|
| L1 Profile | agent browsing uses a dedicated partition (`persist:wepld-agent-<project>`) with no user cookies, password manager/autofill disabled, `session.setPermissionRequestHandler` denying payment-handler, credentials, WebAuthn, notifications, clipboard-read (Electron session APIs; INFERRED names per Electron docs) | ambient credentials, saved cards |
| L2 Navigation | `session.webRequest.onBeforeRequest`, `will-navigate`, `will-redirect`, `setWindowOpenHandler` → URL classifier (known checkout/payment hosts, signup/register paths, OAuth consent hosts) → `effect.propose(browser.navigate.sensitive)` | entering a checkout/signup flow, incl. redirects (which playwright-mcp's origin lists do not cover) |
| L3 Action | before `preview_act` fill/click/type (T3 `apps/server/src/mcp/toolkits/preview/handlers.ts`), resolve the target via the accessibility snapshot: `input[type=password]`, `autocomplete` ∈ {`cc-number`,`cc-csc`,`cc-exp*`,`current-password`,`new-password`,`one-time-code`}, accessible name matches {pay, place order, buy, subscribe, create account, sign up}; typed text matched against card/IBAN/SSN/API-key patterns | typing credentials / card data; submitting purchases / signups |
| L4 Core | classes `browser.input.credential`, `browser.submit.payment`, `browser.account.create` → **BLOCKED** (hard floor); `browser.form.submit` → approval | final decision + ledger row |
| L5 Evidence | blocked attempt → screenshot of the page (`Page.captureScreenshot`) attached to the ledger row | audit |

Classifier misses are expected; L1 (no credentials available) is what makes a miss low-impact. The UI must not claim the
block is complete.

### 4.3 Recording and evidence

- Screenshots via CDP; T3 already has `preview_recording_start/stop` and screencast video (`apps/web/src/browser/browserRecording.ts`).
- HAR: Playwright `recordHar` is a context-creation option, so for relayed Electron pages build the HAR from CDP
  `Network.*` events in the Server (INFERRED; verify in spike). Playwright tracing on CDP-connected contexts: UNKNOWN —
  verify.
- Evidence objects: content-addressed (SHA-256) blobs in Core S2 evidence store; ledger row references digest + effect id;
  `Cookie`, `Authorization`, `Set-Cookie` headers and form bodies of L3-classified fields redacted **before** hashing.

**ESTIMATE:** L1–L4 gating 2–3 pw; HAR/evidence 1–2 pw; tests 1 pw. **Total 4–6 pw** (plus `R03D` 4–8 pw only if Orca's
broader browser command set is ported).

| ID | Acceptance test |
|---|---|
| BRW-AT-01 | Agent fills `input[autocomplete=cc-number]` on a local fixture page → BLOCKED, ledger row + screenshot |
| BRW-AT-02 | Redirect chain from an allowed origin to a fixture "checkout" host → navigation held for approval |
| BRW-AT-03 | Agent clicks "Create account" on a fixture signup form → BLOCKED even in Skip mode |
| BRW-AT-04 | Agent partition has no cookies from the user's preview partition |
| BRW-AT-05 | HAR evidence for a session contains no `Authorization`/`Cookie` values; digest verifies |
| BRW-AT-06 | Headless runner path (`chromium.launch`) enforces the same L2–L4 rules |

All fixtures are local pages; no real payment or signup site is touched by tests.

---

## 5. Computer use per OS (Orca native helpers, verified @e310a636)

| OS | Orca helper | APIs (verified) | Observation | Input | Limits |
|---|---|---|---|---|---|
| macOS | Swift package `native/computer-use-macos` (`Sources/OrcaComputerUseMacOS/main.swift` + `OrcaComputerUseMacOSCore/*`; 6,889 Swift LOC incl. tests per R03D) | `AXIsProcessTrusted` (L1054), `CGPreflightScreenCaptureAccess`/`CGRequestScreenCaptureAccess` (L1063/L1078), ScreenCaptureKit `SCShareableContent` with `CGWindowListCreateImage` fallback (L2463–2474), `CGEvent` keyboard/mouse/scroll (L2567–2632); authenticated Unix-socket transport (`AuthenticatedConnectionHangupMonitor`, `UnixSocketPathSafety`), focus check before synthetic keys (`KeyboardInputSafety`) | AX tree + window screenshot | CGEvent | needs TCC **Accessibility** and **Screen Recording** for the helper's code identity |
| Windows | PowerShell `native/computer-use-windows/runtime.ps1` (1,370 lines), serve mode | `UIAutomationClient`/`UIAutomationTypes` (L16–17), P/Invoke `SendInput` (L99), `CopyFromScreen` (L766); launched `-NoProfile -ExecutionPolicy RemoteSigned`, fallback **`Bypass`** (`src/main/computer/windows-powershell-execution-policy.ts`) | UIA tree + screen capture | SendInput | UIPI: cannot drive elevated windows from medium IL (INFERRED, OS rule) |
| Linux | Python `native/computer-use-linux/runtime.py` (1,189 lines) | PyGObject `Atspi` 2.0 (L22–36), Gdk/GdkPixbuf screenshots, `xdotool` for keys | AT-SPI tree; screenshot **disabled on Wayland** (L549, L735–738) | xdotool; **no hotkeys on Wayland** (L896–897) | X11 only for full function; needs system PyGObject |

**Approach:** accessibility-tree-first (element-addressed actions, `setValue` instead of keystrokes where possible) with
screenshots as the fallback/evidence channel. AX trees are cheaper and more precise; screenshots cover canvas/remote
apps. Both are privacy-sensitive outputs.

**Core gating (proposal):**

| Effect class | Default | Notes |
|---|---|---|
| `computer.observe` (list apps/windows, AX snapshot, screenshot) | approval per app per session | outputs may contain other apps' secrets; redact password fields (AX `secure` text) |
| `computer.input` (click, type, key, drag, setValue, paste) | approval per action in Manual; per-app allowlist in Auto | refuse when target window is not focused (Orca `KeyboardInputSafety`) |
| hard-block apps | BLOCKED | password managers, banking apps, OS security/settings panes, WePLD itself (prevents self-approval clicking), terminal windows (INFERRED list; make configurable) |
| credential-shaped typed text | BLOCKED | same patterns as §4 L3 |

**Port notes:** sign the macOS helper with the app's Developer ID so TCC grants survive updates (an unsigned/ad-hoc
helper changes identity per build → re-prompts; INFERRED from TCC behavior). Replace the PowerShell runtime with a signed
helper (Rust using UI Automation COM via the `windows` crate, or sign the `.ps1` and drop the `Bypass` fallback) —
`ExecutionPolicy Bypass` is not acceptable for a Core-gated product. Linux Wayland needs xdg-desktop-portal
RemoteDesktop/ScreenCast (user consent per session) — net-new; mark Linux computer use "X11 only" in v1.

**ESTIMATE:** Windows-first port (sidecar + signed helper + gating) 3–5 pw; macOS 2–3 pw; Linux X11 1–2 pw; Wayland
portal 2–4 pw (defer). **Total v1 (Win+mac+X11) 6–10 pw** (vs `06` D6 3–6 pw).

| ID | Acceptance test |
|---|---|
| CU-AT-01 | Without TCC grants, macOS `computer.permissions` reports both missing; no capture attempted |
| CU-AT-02 | `computer.input` into a password-manager window → BLOCKED; no `SendInput`/`CGEvent` emitted (helper trace) |
| CU-AT-03 | Click on WePLD's own approval dialog by the agent → BLOCKED |
| CU-AT-04 | Windows helper runs without `ExecutionPolicy Bypass` (process command-line check) |
| CU-AT-05 | Wayland session → capability report says screenshot/hotkey unavailable; UI shows "X11 only" |
| CU-AT-06 | AX snapshot of a fixture app redacts secure text fields before reaching the agent |

---

## 6. Packaging, updates and Windows service

### 6.1 Build and signing

| OS | Artifact (electron-builder `electron-userland/electron-builder@e46680da10db`, MIT; T3 pins 26.16.1) | Signing options | Cost (ESTIMATE / verify) |
|---|---|---|---|
| Windows x64 (primary) | NSIS (as T3) | **Azure Artifact Signing: not eligible** (F1). **OV code-signing cert with cloud HSM key** (CA/B Forum rules require hardware-protected keys — INFERRED from the 2023 CSBR change) from a CA supported by **jsign** (`ebourg/jsign@cf5d2ceaf2ec`, Apache-2.0; README lists SSL.com, Certum, DigiCert, GaraSign, Keyfactor, SignPath, YubiKey, AWS/Google/Oracle KMS, Artifact Signing). SignPath Foundation free tier requires an OSI-licensed, fully open-source project (signpath.org/terms) → **not eligible** while the repo is private. | OV cert ~USD 100–400/yr (UNKNOWN; quote per CA; check CA acceptance of Saudi individual/entity) |
| macOS | DMG + zip (zip needed for `MacUpdater`), hardened runtime, notarization | Apple Developer Program (individual enrollment available internationally — INFERRED) | USD 99/yr (INFERRED, verify) |
| Linux | AppImage + `.deb` (+ `.rpm` optional) | no OS signing; publish SHA256SUMS + optional GPG signature | 0 |

SmartScreen: OV-signed binaries still accumulate reputation per hash/publisher (FAQ "SmartScreen reputation builds up
automatically", Artifact Signing FAQ); expect warnings for early releases regardless of certificate type.

### 6.2 Auto-update channels

- `electron-updater` 6.8.12 has `NsisUpdater`, `MacUpdater`, `AppImageUpdater`, `DebUpdater`, `RpmUpdater`, `PacmanUpdater`
  and providers `GitHub`, `PrivateGitHub`, `Generic`, `GitLab`, `Bitbucket`, `Keygen`
  (`electron-builder@e46680da10db:packages/electron-updater/src/{,providers/}`); Windows signature check in
  `windowsExecutableCodeSignatureVerifier.ts`.
- Private source repo (ADR-010) → do **not** use `PrivateGitHubProvider` (would ship a token). Use the **Generic**
  provider on a static HTTPS bucket or a separate public "releases" repo; `update.electronjs.org` requires public repos
  (INFERRED; its repo has no license).
- Channels: `stable` and `nightly` (copy T3's model: nightly is the release candidate; preview builds carry no feed —
  `t3code@36d4d711:docs/operations/release.md` L5–45).
- Add an **ed25519-signed update manifest** verified by Core before the updater applies a download (defends against a
  compromised bucket; 06 §4 "silent cross-update" risk). Updates are an effect class `app.update.apply` (approval by
  default; WebAuthn for channel changes).

### 6.3 Windows service for the headless runner

T3 has no Windows service ("Windows background services are not supported", `t3code@36d4d711:docs/user/background-service.md` L88).

| Option | Pin | License | Status | Fit |
|---|---|---|---|---|
| **Rust `windows-service` crate** in a small `wepld-service.exe` that supervises Core + Node Server in a Job Object | `mullvad/windows-service-rs@82fe85adb2f5` | MIT OR Apache-2.0 (LICENSE-MIT + LICENSE-APACHE; GitHub reports Apache-2.0) | active (pushed 2026-10-25) | **Recommended** — no third-party .exe, same language as Core, signed with our cert |
| WinSW | `winsw/winsw@1d0ee4a91bad` | MIT | v2.12.0 stable (2023-01); v3 still alpha (2023) | acceptable fallback; external XML-configured wrapper |
| node-windows | `coreybutler/node-windows@54ac1e382f1c` | MIT (bundles WinSW; NSSM/sudowin notes in LICENSE) | 1.0.0-beta.8; last push 2024-10 | not recommended (dormant) |
| NSSM | nssm.cc (no GitHub source) | public domain (per site; UNKNOWN verification here) | releases 2014/2017 (INFERRED) | reject (unmaintained; AV false positives reported — INFERRED) |

Design notes: run the service as the **installing user's account** (needs "Log on as a service") or as a dedicated
local account — not LocalSystem — so DPAPI/keyring secrets and per-user tools work; services run in session 0 with no
desktop, so **browser panes and computer use are unavailable in service mode** (headless Playwright only). Simpler v1
alternative: Task Scheduler "at logon" task (no admin, runs in the user session). Interplay: codex elevated sandbox
installs its own Windows service (`codex-rs/windows-sandbox-service/`) — avoid two WePLD services by folding sandbox
provisioning into `wepld-service` if both are adopted.

**ESTIMATE:** signing pipeline (jsign + OV/HSM, notarization) 1–2 pw; Generic-provider updates + signed manifest 1–2 pw;
Windows service 1–2 pw; Linux rpm 0.5 pw. **Total 3.5–6.5 pw.**

| ID | Acceptance test |
|---|---|
| PKG-AT-01 | Installer, `wepld-core.exe`, native addons and helpers are all Authenticode-signed (signtool verify) |
| PKG-AT-02 | Tampered update manifest (bad ed25519 signature) → update refused, ledger row |
| PKG-AT-03 | Nightly install never receives stable-only feed and vice versa; no donor update URL present (06 §4 grep gate) |
| PKG-AT-04 | macOS notarization staple check passes; Gatekeeper opens DMG app offline |
| PKG-AT-05 | `wepld service install` on Windows → survives reboot, runs as the configured non-SYSTEM account, `uninstall` leaves data intact |
| PKG-AT-06 | AppImage + deb + rpm install/launch smoke (T3's `scripts/smoke-desktop-app.ts` pattern) |

---

## 7. Accessibility baseline (workbench)

**Target:** WCAG 2.2 Level AA (w3.org/TR/WCAG22, doc reference) for all first-party UI. New-in-2.2 criteria with direct
impact: 2.4.11 Focus Not Obscured (sticky composer/panels), 2.5.7 Dragging Movements (split panes, diff range drag,
canvas — keyboard alternatives), 2.5.8 Target Size (Minimum) 24×24 CSS px (toolbar icons), 3.3.7 Redundant Entry,
3.3.8 Accessible Authentication (WebAuthn/passkey approvals satisfy it; never require typing a code to approve).

| Surface | Requirement | Current donor state | Action |
|---|---|---|---|
| Monaco editor/diff | `accessibilitySupport: "auto"` (forced "on" when an AT is detected), accessible diff viewer (`F7`), accessibility help (`Alt+F1`), no tab-trap (`Ctrl+M`) | Monaco supports these (MIT, `microsoft/monaco-editor@dbf1945df2ff`); Orca uses Monaco | expose settings; test with NVDA/Narrator/VoiceOver |
| Terminal | screen-reader mode | **T3: Canvas 2D libghostty renderer, no SR support found (F5)**; xterm.js has `screenReaderMode?: boolean` (`xtermjs/xterm.js@d8a8247dbc11:typings/xterm.d.ts` L259–262), used by Orca | add an "accessible terminal" mode: either swap to xterm.js with `screenReaderMode` when an AT is on, or add a DOM mirror + `aria-live` for the ghostty buffer. ESTIMATE 1–3 pw |
| Agent streaming | `aria-live="polite"` on a summarized status region (not on token stream); "jump to latest" control | T3 has 1,823 `aria-*` attributes in `apps/web/src` (count, not an audit) | throttle announcements to turn boundaries |
| Approvals (Inbox) | modal focus trap, explicit labels of effect class/target, OS-native WebAuthn | new | keyboard-only approval path; no timeouts below 20 s without extension (2.2.1) |
| Debug/LSP panels (§1–2) | tree views with `role=tree`, keyboard stepping (F5/F10/F11), announcements on breakpoint hit | new | build with accessible tree component |
| Theming | 4.5:1 text contrast, 3:1 UI components, `forced-colors` (Windows High Contrast), `prefers-reduced-motion` | partial (UNKNOWN until audited) | token-level contrast checks |
| Electron | Chromium enables its accessibility tree when an AT is detected; `app.setAccessibilitySupportEnabled` exists (Electron docs; INFERRED, not re-fetched) | — | settings toggle "Optimize for screen reader" |

Tooling: `@axe-core/playwright` (`dequelabs/axe-core@6b52b841461b`, `dequelabs/axe-core-npm@794589bda678`, **MPL-2.0**
— dev/test-only dependency, not shipped; MPL file-level copyleft applies only if we modify and distribute its files);
manual AT passes with NVDA (`nvaccess/nvda@6e38e89ec7c0`, GPL — tool only), Narrator, VoiceOver, Orca (GNOME).

**ESTIMATE:** baseline audit + fixes for existing T3 surfaces 2–4 pw; accessible terminal 1–3 pw; per-new-surface cost
~10% of its build estimate. **Total 3–7 pw** + ongoing.

| ID | Acceptance test |
|---|---|
| A11Y-AT-01 | axe-core: zero serious/critical violations on Home, Projects/Thread, Review, Inbox, Settings (Playwright run) |
| A11Y-AT-02 | Full keyboard path: open project → start agent → approve an effect → view diff → commit, no mouse |
| A11Y-AT-03 | NVDA reads terminal output of `echo hello` in accessible-terminal mode |
| A11Y-AT-04 | Monaco with NVDA: line navigation reads text; accessible diff viewer lists hunks |
| A11Y-AT-05 | Windows High Contrast (forced-colors): focus indicator and approval buttons visible |
| A11Y-AT-06 | All toolbar targets ≥ 24×24 CSS px (automated geometry check) |

---

## 8. Consolidated estimate and phase placement (proposal)

| Gap | ESTIMATE pw | Suggested phase | Depends on |
|---|---|---|---|
| 1 Debugging (DAP + UI + gating + MCP) | 6–10 | after editor (P7–P9 band) | Monaco (D7), effect classes in Nawat (P3) |
| 2 LSP | 6–10 (incl. 1 pw spike) | with/after D7 editor | ADR-003 amendment |
| 3 Containment (all OS + proxy + escape suite) | 9–14 | P8 (floor in P3 unchanged) | Core launcher |
| 4 Browser gating + evidence | 4–6 | P5–P6 (agent browser already exists in T3) | Core evidence store (S2) |
| 5 Computer use (Win+mac+X11) | 6–10 | P9 (as `06` D6) | §3 gating classes |
| 6 Packaging/signing/updates/service | 3.5–6.5 | P2 (signing) + P10 (service) | OV cert purchase |
| 7 Accessibility | 3–7 + ongoing | P2 baseline, then per surface | — |
| **Total** | **~37.5–63.5** | | |

These are additions on top of R02 §14's MVP band; several items (debugging, computer use, Wayland) can be deferred
without breaking the trust story.

## 9. Unknowns

| # | Unknown | How to resolve |
|---|---|---|
| U1 | Whether OV code-signing CAs issue to a Saudi individual or entity, and price | quotes from SSL.com / Certum / DigiCert |
| U2 | MXC (BaseContainer) availability on Windows 11 Home | codex `mxc-sandbox` availability probe on the founder's machine (later, not in planning) |
| U3 | License of `@hediet/json-rpc` (dep of `@vscode/monaco-lsp-client`) — no root license file | npm metadata + package tarball LICENSE |
| U4 | Playwright tracing/HAR on `connectOverCDP` contexts | spike |
| U5 | Exact npm packaging of TS 7 native LSP binary | inspect `typescript@7` tarball |
| U6 | NSSM current license/maintenance | nssm.cc (not fetched) |
| U7 | Electron session permission names for payment/credential APIs | Electron docs check at implementation |

## 10. Sources (all accessed 2026-10-27)

- `openai/codex@603a7baff0f6` — `codex-rs/{windows-sandbox-rs,windows-sandbox-service,mxc-sandbox,sandboxing,linux-sandbox,process-hardening}/…` (files named inline); license Apache-2.0 (API).
- `anthropics/sandbox-runtime@98a4016d27609` — README.md; Apache-2.0.
- `pingdotgg/t3code@36d4d711b79c` — `apps/desktop/src/preview/*`, `apps/server/src/preview/*`, `apps/server/src/mcp/toolkits/preview*`, `apps/web/src/terminal/ghostty/*`, `apps/desktop/package.json`, `docs/operations/release.md`, `docs/user/background-service.md`.
- `stablyai/orca@e310a63624c8` — `native/computer-use-{macos,windows,linux}/*`, `native/windows-security/*`, `src/main/computer/*`.
- Debug: `microsoft/vscode-debugadapter-node@53d9de511fc6`, `microsoft/debug-adapter-protocol@c10f18c3332c`, `microsoft/vscode@df5c887e7961`, `CodinGame/monaco-vscode-api@9e70dd83a1d1`, `opensumi/core@9da5ceb24364`, `eclipse-theia/theia@f47c3ea8a4ad`, `microsoft/vscode-js-debug@a9df0307248d`, `microsoft/debugpy@671f6c7d1b22`, `vadimcn/codelldb@62def434dc22`, `llvm/llvm-project@3a46435bd28e`, `go-delve/delve@a439ae64ea3c`, `Samsung/netcoredbg@9744e1f05186`.
- LSP: `TypeFox/monaco-languageclient@661fa992fa96`, `microsoft/monaco-editor@dbf1945df2ff`, `microsoft/vscode-languageserver-node@82ed8ac580bc`, `microsoft/TypeScript@1f82f368b668`, `microsoft/typescript-go` (archived), `yioneko/vtsls@9ff4ce433cd4`, `typescript-language-server/typescript-language-server@7b28f104e741`, `DetachHead/basedpyright@5fb7d7afc7e6`, `microsoft/pyright@611afe615b86`, `astral-sh/ty@0445d6497ae2`, `rust-lang/rust-analyzer@889bb47e8530`, `golang/tools@c1193aca3e6b`, `hediet/typed-json-rpc` (no license file).
- Browser: `microsoft/playwright@a169686c61af`, `microsoft/playwright-mcp@0c4107acbecb`, `vercel-labs/agent-browser@edb40f187886`, `electron/electron@3dfc698827c5`.
- Packaging: `electron-userland/electron-builder@e46680da10db`, `ebourg/jsign@cf5d2ceaf2ec`, `mullvad/windows-service-rs@82fe85adb2f5`, `winsw/winsw@1d0ee4a91bad`, `coreybutler/node-windows@54ac1e382f1c`, `electron/update.electronjs.org@9652cd82a680`, `electron/update-electron-app@5525b5297f22`; https://learn.microsoft.com/en-us/azure/artifact-signing/quickstart and /faq (fetched); https://signpath.org/terms (fetched).
- Accessibility: `xtermjs/xterm.js@d8a8247dbc11`, `dequelabs/axe-core@6b52b841461b`, `dequelabs/axe-core-npm@794589bda678`, `nvaccess/nvda@6e38e89ec7c0`, `ghostty-org/ghostty@4a4fc017940b`; https://www.w3.org/TR/WCAG22/ (reference, not fetched).
