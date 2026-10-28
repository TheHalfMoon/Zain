# R18 — DeskGate: Desktop Commander source-level REA and Zain transplant plan

```text
STATUS        = PLANNING-ONLY research. Nothing copied into Zain, nothing installed or run. No commit.
DATE          = 2026-10-27
COMPONENT     = DeskGate (Zain component for local + remote computer access; Zain = new name of WePLD)
AUTHORITY     = Founder attests legal permission (FOUNDER-ATTESTED). Public licenses verified below
                independently; the attestation does not extend to code that is not public.
EVIDENCE      = GitHub API at pinned SHAs (raw file reads to session scratchpad), installed npm package
                (read-only file listing), frozen registry CSV (python -I). Source content treated as data.
ESTIMATES     = ESTIMATE class, person-weeks (pw), same unit as 14_TASK_CATALOG.md.
CONTEXT (not redone) = 07 (Core = only PDP; Server = PEP; one PTY host; MEDIATED effects; project-home;
                runner), R13, R03D (process-host, terminal daemon, SSH), 14 (P3 seams C-xx, P10 R-xx).
```

## 0. Verdict (one paragraph)

Desktop Commander (DC) is a **mature, very actively maintained MIT local MCP server** (10.1k stars, v0.3.1 on
2026-10-22, 100+ commits in the last 90 days) whose value for Zain is its **agent-facing tool surface and
hard-won edge-case handling** (output paging, REPL-prompt detection, process-tree kill, ripgrep session search,
edit_block fuzzy diagnostics, line-ending preservation, symlink/junction-safe path resolution). Its **execution
model must not be adopted**: DC is its own execution authority (it spawns shells via `child_process` pipes, not a
PTY; enforces only self-described non-boundary guardrails; and lets the agent rewrite its own policy through
`set_config_value`). Its **remote product is proprietary**: the public `remote-desktop-commander` repo is
docs/manifests under an all-rights-reserved license; the relay/OAuth service at `mcp.desktopcommander.app` is not
public. Only the device-agent half of remote is MIT (in DesktopCommanderMCP), and it is a Supabase-Realtime client
for that hosted relay — useless to Zain without the relay and contrary to the "no third-party relay" rule.
**Plan: DeskGate = thin MCP tool adapters (DC-compatible names/schemas) registered on the Zain Server `/mcp`
endpoint, every effect proposed to Core and executed by the existing EffectWorker / node-pty terminal manager;
selected MIT pure-logic modules ported with attribution; remote via the Zain runner + project-home + passkey
model (R-01..R-04).** Effort ESTIMATE 5.0–8.5 pw across P3 (seam S6) / P6 / P10.

## 1. Sources and pins

| Source | Pin (SHA, date) | License (verified) | NOTICE | Public code? | Maintenance |
|---|---|---|---|---|---|
| `wonderwhy-er/DesktopCommanderMCP` (npm `@wonderwhy-er/desktop-commander`) | `db3430f23c1fd487f66412e93f7022b8c34ccd6f` (HEAD of `main`, committed 2026-10-24) | **MIT** — `LICENSE` (1108 B): "Copyright (c) 2024-2025 Eduard Ruzga and Desktop Commander Contributors"; `package.json` `"license": "MIT"`, version 0.3.1 | **No NOTICE / THIRD_PARTY file** in tree (514 blobs checked). Attribution = keep MIT text + copyright line | Yes, full local server + device agent | Very active: pushed 2026-10-27; release v0.3.1 2026-10-22; ≥100 commits since 2026-07-27; 320 open issues; top contributors wonderwhy-er 420, mihailt 280, serg33v 100 |
| `desktop-commander/remote-desktop-commander` | `a6573e866edc1f971977e84606f6e002fb37cd9d` (2026-10-27) | **Proprietary / NOASSERTION.** `LICENSE` (1042 B): "Copyright (c) 2026 SIA Desktop Commander. All rights reserved." View and link only; copying/modification/redistribution needs prior written permission; states the service is proprietary and its source is **not** in the repo | n/a | **No.** 14 blobs: README, SECURITY, CONTRIBUTING, docs/SETUP.md, server.json, plugin.json, gemini-extension.json, .mcp.json, logos, issue templates | Active (beta; server.json version 1.1.12) |
| `vendor/telemetry-contract` inside DCMCP | same SHA | **No license field** in its `package.json`; declares origin `desktop-commander/telemetry-proxy` (GitHub API: **404 — private**) | — | Vendored JS only | **EXCLUDE** (unclear license + telemetry) |
| Other `desktop-commander` org repos (gh repo list) | — | all report no SPDX license | — | `legal`, `main-web`, `main-web-astro`, `skills`, `mock-llm`, `dc-diagnose-tool`, `prompt-library`, `html2pdf-skill`, `bigquery-cli-toolkit`, … | **None is a DC execution/relay implementation**; `skills` duplicates SKILL.md content already in DCMCP. Not used |
| Third-party forks (`burkeholland/desktop-commander` MIT 25★, `Shutupmilo/DesktopCommanderMCP` MIT fork, `jasondsmith72/UDC` MIT 4★) | — | MIT | — | Yes | Low-signal forks; no relay code. Not used |
| Frozen registry `WEPLD_MASTER_SOURCE_REGISTRY_2026-08-14_V1.csv` (402 rows) | frozen | — | — | — | **No Desktop Commander row.** Related rows: SRC-0182 MCP, SRC-0046 ripgrep, SRC-0237 node-pty, SRC-0241 ConPTY, SRC-0242 Job Objects, SRC-0307 MCP Gateway (all NOT_ADMITTED). → DC needs a **new registry row** (proposed `SRC-NEW-DC`, PATH_LEVEL_MINING, MIT) via the admission gate before any copy |
| Installed package evidence | A locally installed DesktopCommanderMCP 0.3.1 build was inspected read-only and matched the pin (local machine details intentionally not recorded in this public repository) | MIT `LICENSE` present | — | compiled `dist/*.js` | — |

**Public vs proprietary boundary (explicit).**

| Part | Where | Status |
|---|---|---|
| Local MCP server (tools, terminal/process manager, search, config, edit, file handlers, UI widgets) | DCMCP `src/**` | Public, MIT |
| Remote **device agent** (OAuth device-flow client, Supabase Realtime channel client, local stdio MCP client bridge, diagnostics upload) | DCMCP `src/remote-device/**`, `src/npm-scripts/remote.ts`, `scripts/remote/*` | Public, MIT — but only a client of the hosted relay |
| Remote **relay / MCP endpoint / OAuth AS / dashboard / device registry / Supabase project** | `https://mcp.desktopcommander.app` (`MCP_SERVER_URL` default in `src/remote-device/device.ts:104`); Supabase URL + publishable key fetched at runtime (`device.ts:196,529-532`) | **Proprietary, not present anywhere public.** Nothing to transplant |
| Telemetry backend | `https://telemetry.desktopcommander.app/mp/collect` and a Cloud Run fallback (`src/utils/capture.ts:61-62`), GA4 Measurement-Protocol style with `client_id` UUID | Proprietary service; client code MIT but **stripped** |
| Telemetry contract | `vendor/telemetry-contract` from private `telemetry-proxy` | License unclear → **excluded** |

## 2. Path-level analysis (DCMCP @ db3430f)

Sizes are blob bytes from the git tree.

### 2.1 Tool surface (`src/server.ts`, 76 KB, 1552 lines; schemas `src/tools/schemas.ts`)

Tools registered (server.ts line of `name:`): `get_config` 315, `set_config_value` 339, `read_file` 369,
`read_multiple_files` 434, `write_file` 456, `write_pdf` 488, `create_directory` 549, `list_directory` 567,
`move_file` 609, `start_search` 627, `get_more_search_results` 711, `stop_search` 743, `list_searches` 764,
`get_file_info` 782, `edit_block` 811, `start_process` 876, `read_process_output` 925, `interact_with_process`
968, `force_terminate` 1011, `list_sessions` 1025, `list_processes` 1049, `kill_process` 1065, `get_usage_stats`
1081, `get_recent_tool_calls` 1097, `give_feedback_to_desktop_commander` 1122 (+ prompts in `src/tools/prompts.ts`).
Remote calls are flagged via `metadata.remote` (server.ts 1220-1222) and `DC_REMOTE_DEVICE=true` (184-186).

### 2.2 Filesystem

| Path | Role | Observations |
|---|---|---|
| `src/tools/filesystem.ts` (49.9 KB) | read/write/list/move/info, `validatePath`, `isPathAllowed` | Realpath-based check incl. Windows junctions (176-199, 340-390); case-folded `normalizePath` (135-137); **`allowedDirectories: []` or containing `/` ⇒ allow everything** (293); unset ⇒ falls back to `os.homedir()` and **writes it back to config** (114-124). URL reads (461) |
| `src/handlers/filesystem-handlers.ts` (20 KB) | MCP arg parsing → tools | |
| `src/tools/edit.ts` (24 KB) + `fuzzySearch.ts`, `fuzzySearchCore.ts` (worker thread) | `edit_block` exact replace with occurrence count; on miss runs Levenshtein fuzzy search and returns a char-level diff | Good agent UX; `utils/fuzzySearchLogger.ts` logs fuzzy attempts **including text** to a local log — must not be ported |
| `src/utils/files/{text,binary,image,pdf,docx,excel,factory,base}.ts` | Per-type read/edit handlers (line offsets, negative offsets = tail) | docx/excel/pdf pull heavy deps (exceljs, pizzip, pdf-lib, unpdf, md-to-pdf → Puppeteer, sharp) |
| `src/utils/lineEndingHandler.ts`, `utils/atomic-write.ts`, `utils/rename.ts` | CRLF/LF preservation; temp+rename writes; cross-device rename | Small, pure, valuable |
| `src/ui/**` | MCP-UI widgets (file preview, config editor, TipTap markdown editor) | Not needed — Zain has its own IDE (P6 I-01) |

### 2.3 Terminal / process

| Path | Role | Observations |
|---|---|---|
| `src/terminal-manager.ts` (36 KB) | Sessions keyed by PID; `spawn()` from `child_process` (line 1, 194) with **pipes, not a PTY** | Line buffer with 50 MB/session cap and 1 MB max line, oldest-line eviction (96-97, 513); offset/negative-offset paging (607-642); "open line" partial-output semantics |
| `src/tools/improved-process-tools.ts` (29.8 KB) | `start_process`, `interact_with_process`, `read_process_output`, `force_terminate`, `list_sessions` | Wait loops capped at `MAX_PROCESS_WAIT_MS = 50000` (config.ts) to stay under MCP 60 s request timeout; `DEFAULT_COMMAND_TIMEOUT = 1000 ms` |
| `src/utils/process-detection.ts` (12 KB) | REPL/shell prompt heuristics (`>>> `, `... `, `bash-5.2$ `, `postgres=# `…) → waiting-for-input state | Pure; port |
| `src/utils/process-tree.ts` (8.8 KB) | Windows `taskkill /T /F`; POSIX `ps` snapshot → SIGTERM, grace, re-walk, SIGKILL | Zain replaces with Job Objects (Win, C-16) / process groups; keep POSIX algorithm as reference |
| `src/utils/shell.ts` (9.3 KB) | Shell resolution: Win `powershell.exe` → `%ComSpec%`; macOS `/bin/zsh`; else `/bin/sh`; bash/zsh `-l -c`; pwsh vs PS 5.1 vs cmd verbatim-args handling; refuses PATH lookup in CWD on Windows; rejects `nologin`, `git-shell`, `tmux` etc. as shells | Pure-ish; port the resolution table |
| `src/tools/process.ts` (3.4 KB) | `list_processes` / `kill_process` (arbitrary PID) | `kill_process` on arbitrary PIDs is **not** acceptable in Zain (only Zain-owned process trees) |
| `src/command-manager.ts` (11 KB) | Blocklist check: splits on `; && \|\| \| &`, recurses into `$( )` and backticks, takes first token, lower-cases | **Not a security boundary** (DC's own SECURITY.md says so): absolute paths, `env sudo`, interpreters (`python -c`), PowerShell `&`/`iex`, aliases, `cmd /c` nesting, base64 all bypass. Upstream even has `test/test-blocklist-bypass.js` |
| `src/config-manager.ts` (26.6 KB) | `~/.claude-server-commander/config.json`; defaults (blocklist of 33 at 233-277; `allowedDirectories: []`; `telemetryEnabled: true` opt-out; read 1000 / write 50 lines); file watcher; cross-process lock (proper-lockfile) | Policy lives in a user-writable JSON file **and is writable by the agent** via `set_config_value` (incl. `blockedCommands`, `allowedDirectories`; server.ts 318-354 even documents that `[]` = full access) |
| `src/utils/toolHistory.ts`, `config.ts` `TOOL_CALL_FILE` | Logs tool calls (with args) to `~/.claude-server-commander/claude_tool_call.log` (10 MB) | Secrets in args land in plaintext log — not ported; Zain ledger is the record |

### 2.4 Search

`src/search-manager.ts` (59.6 KB): session-based ripgrep (`--json` streaming), content + filename modes,
`maxResults`, time limit, pagination via `get_more_search_results`, Office-file (xlsx/docx) search path,
`validatePath(rootPath)` on the root only. `src/utils/ripgrep-resolver.ts`: `@vscode/ripgrep` → system `rg` on
PATH (never CWD on Windows) → fallbacks; chmod 755 on POSIX. `src/handlers/search-answers.ts`: result shaping.
Note: ripgrep follows whatever the root contains; symlinks inside the root that point outside are a residual
escape unless `--no-follow` (rg default) is kept and results are realpath-checked.

### 2.5 Remote (device side, MIT) — `src/remote-device/**`

| Path | Role |
|---|---|
| `device.ts` (37.8 KB) | Lifecycle; `MCP_SERVER_URL` default `https://mcp.desktopcommander.app`; fetches Supabase URL + publishable key from it; persists session to `~/.desktop-commander-device/device.json` (0600 on POSIX, **no ACL on Windows** per its README); refresh-token family handling; keep-awake via optional `caffeinate` |
| `device-authenticator.ts` (9.3 KB) | OAuth 2.0 **device authorization grant** + PKCE, polls token endpoint, opens browser |
| `remote-channel.ts` (80.6 KB) | `@supabase/supabase-js` Realtime channel: presence, join/heartbeat watchdog, reconnect backoff, token re-auth; receives tool calls, returns results |
| `desktop-commander-integration.ts` (18.4 KB) | Spawns the **local DC server as a child over MCP stdio** (`StdioClientTransport`, `process.execPath`), sets `DC_REMOTE_DEVICE=true`, forwards **any** tool name verbatim (`callClientTool`, 294-313) — no device-side allowlist or per-call user confirmation |
| `diagnostics/{device-log,redact,report,upload}.ts`, `realtime-health-telemetry.ts`, `transport-telemetry.ts`, `rollouts.ts` | Diagnostics upload, telemetry, server-driven rollouts (remote feature flags) |
| `scripts/remote/remote-{macos,linux}.sh`, `remote-windows.{ps1,cmd}` | `curl … \| sh` / `irm … \| iex` launchers that may install Node |

Hosted trust model (from remote repo README/SECURITY, data only): AI client → OAuth bearer → hosted relay → paired
device → local DC; device reachable while agent runs; revocation in vendor dashboard; "tools execute with your
user account's permissions". **The relay operator is inside the TCB** (it can inject any tool call into any
online device), and there is no device-side human approval. Incompatible with Zain 07 §6 (Core-issued WebAuthn
challenges; no third-party relay by default).

### 2.6 Telemetry

`src/utils/capture.ts` (26.5 KB): GA4-style events to the telemetry proxy with persistent `client_id`; error
sanitization (`sanitizeError`, path scrubbing via `addToolCallPaths`); opt-out via config or env
(`isTelemetryDisabledByEnv`). Also `utils/usageTracker.ts`, `trackTools.ts`, `ab-test.ts`, `mcp-ui-ab-test.ts`,
`feature-flags.ts` (remote flags), `tools/feedback.ts` (opens feedback form), `welcome-onboarding.ts`,
`dockerPrompt.ts`, remote `captureRemote`. **All stripped**; `capture()` call sites (present in command-manager,
terminal-manager, filesystem, search…) become calls to Zain's local, observational OTel sink (I-10) or are deleted.

### 2.7 Security model and known weaknesses (synthesis)

1. **Self-declared non-boundaries.** DC SECURITY.md table: allowed directories, command blocklist, symlink
   traversal prevention — "Security boundary? No"; only Docker/VM isolation is. Zain must not inherit any claim
   from these.
2. **Shell escapes path checks.** `allowedDirectories` applies to fs tools only; `start_process` can read/write
   anywhere the user can.
3. **Agent-writable policy.** `set_config_value` lets the model widen `allowedDirectories` to `[]` (all) or empty
   `blockedCommands`; config file is also hot-watched.
4. **Default = unrestricted.** Shipped default `allowedDirectories: []` = full filesystem.
5. **Blocklist bypassable** by construction (first-token match; see 2.3).
6. **Arbitrary PID kill** (`kill_process`) and system-wide `list_processes`.
7. **Plaintext logs** of tool args (`claude_tool_call.log`) and fuzzy-edit text.
8. **Remote**: third-party relay in TCB; bearer-only (no device-side user presence); token file without Windows
   ACL; `curl|sh` installers; server-driven rollouts/feature flags change behaviour remotely.
9. **No PTY**: pipes → many TUIs/`ssh`/password prompts misbehave; prompt detection is heuristic.

### 2.8 OS specifics worth keeping (as data/tests, not code authority)

Windows: PowerShell 5.1 vs pwsh arg quoting, `cmd.exe` verbatim args, junction realpath, drive-root allow
(`test/test-allowed-drive-root.js`), `taskkill /T /F`, no CWD PATH lookup (binary-planting defence), CRLF.
macOS: zsh login shell `-l`, caffeinate. Linux: `/bin/sh` fallback, ps-tree walk, ripgrep chmod.

## 3. DeskGate design inside Zain (no second execution authority)

### 3.1 Placement

```text
MCP client / agent ──► Zain Server /mcp  (PEP)
                         └─ packages/deskgate  (tool adapters: schema → EffectProposal; result shaping)
                               │ effect.propose {effect_class, exact_target, input_digest, origin, MEDIATED}
                               ▼
                        Zain Core (Nawat PDP + ledger) ── decision / grant_id / approval_challenge (WebAuthn)
                               │ grant
                               ▼
                        Server EffectWorker (sole executor)
                          ├─ fs ops via fs-gate handle-based operations (19 §3)
                          ├─ Terminal manager (node-pty) — the ONE PTY/process host
                          └─ ripgrep child (process.spawn effect, read-only profile)
                               │ effect.report (observed result, digests)
                               ▼
                        Core ledger receipt  →  adapter returns MCP result
```

Rules: DeskGate holds **no** policy, config file, blocklist, PID table, or spawn call of its own. It never
imports `child_process`/`node-pty`; a lint rule + dependency-cruiser check enforce this (§5 test DG-N10).

### 3.2 Tool → effect-class mapping

| DeskGate tool (DC-compatible name) | Effect class | exact_target | Notes |
|---|---|---|---|
| `read_file`, `read_multiple_files`, `list_directory`, `get_file_info` | `fs.read` | realpath(s) | Batch = one proposal per path or one with target set; reads outside project home → Core decision (may require approval) |
| `start_search`, `get_more_search_results`, `stop_search`, `list_searches` | `fs.read` (root) + `process.spawn` (rg, internal, read-only profile) | realpath(root) | Results post-filtered by realpath ∈ granted root |
| `write_file`, `edit_block`, `create_directory`, `move_file` | `fs.write` | realpath(parent)+name; move = src and dst both | `input_digest` = SHA-256 of new content / edit spec; pre-image hash recorded for UNKNOWN reconciliation |
| `start_process` | `process.spawn` | `{shell, argv/command, cwd, env-diff}` | Executed via Server terminal manager (node-pty) in a Zain-owned Job Object / process group |
| `interact_with_process` | `terminal.input` | `{session_id, bytes digest}` | Each input is its own effect (commands typed into an existing shell are new decisions) |
| `read_process_output`, `list_sessions` | none (read of Server-owned buffer) | — | Scoped to sessions the caller's mission owns |
| `force_terminate` | `process.signal` | `{session_id, signal}` | Only Zain-owned trees |
| `kill_process`, `list_processes` | `process.signal` / host introspection | arbitrary PID | **Default-deny**; `kill_process` only for PIDs in Zain-owned trees; system-wide variant requires explicit policy + approval |
| `get_config` | none | — | Returns Core-compiled effective policy (read-only view) |
| `set_config_value` | **not provided** | — | Policy changes are Core policy edits with WebAuthn (07 §6). Returns a fixed refusal |
| remote session open/close (`deskgate.remote.*`) | `remote.session` | `{device_id, project_home, scope}` | See 3.4 |
| `get_usage_stats`, `get_recent_tool_calls`, `give_feedback…`, `write_pdf` | dropped / replaced | — | Recent calls = ledger query; PDF = P9 W-01 |

All DeskGate effects are `origin = deskgate`, `mediation = MEDIATED`. They count toward Trusted Completion like
other MEDIATED effects. [Revised 2026-10-28, Astro H-1: `start_process`/`terminal.input` are launch authorizations only; the process context has UNKNOWN coverage (17 §2).] Idempotency: [SUPERSEDED 2026-10-28, Astro M-2] durable `logical_operation_id` allocated by Core per principal + mission + client operation key (`_meta.zainOperationKey`); MCP request ids are attempt ids; changed input under the same id is rejected (17 §6).

### 3.3 Sessions

DeskGate session = MCP connection × mission/run × project. Process sessions are Server terminal-manager sessions
(node-pty) tagged with `deskgate_session_id`; output buffering/paging semantics ported from DC (50 MB cap,
eviction, negative offsets, open-line) but implemented over the Server's existing PTY ring buffer, plus ANSI
stripping for agent reads (raw bytes still available to the UI terminal). Prompt-state detection ported as a pure
function. Sessions die with the mission unless pinned; orphan reconciliation follows C-10 (`open_dispatches`).

### 3.4 Remote access (no third-party relay by default)

- Remote = reaching a **project's home Zain Server** (desktop or runner, R-01/R-02) from another client, not
  installing a separate device agent. Transport: Server's own authenticated WS/HTTP `/mcp` (T3 scoped sessions,
  DPoP-bound tickets), over LAN/Tailscale/SSH tunnel (R-04); optional user-supplied relay only as a later
  opt-in, never vendor-hosted by default.
- Pairing: passkey (R-03). Every gated effect from a remote client carries a Core-issued WebAuthn challenge that
  the **paired phone/desktop passkey** signs; session scopes never authorize effects (07 §6 point 2).
- A non-home side cannot propose effects for that project (project-home rule).
- Cross-platform: same adapters on Win/macOS/Linux because execution is the Server's; shell-resolution table from
  DC `shell.ts` becomes Server terminal-manager defaults (P2/P6 terminal work, not DeskGate-private).
- SSH to *other* machines: run `ssh` inside the PTY as a `process.spawn` effect (R03D SSH notes); DeskGate adds no
  SSH stack.

### 3.5 Telemetry

None. No network egress from DeskGate. Optional local spans to the I-10 OTel sink (observational, not evidence).

## 4. File-level transplant table (planned; not executed)

Copy modes: **PORT-MIT** = copy file/function with MIT header + upstream path@SHA comment, then modify;
**PATTERN** = reimplement from reading (no code copy); **TEST-PORT** = adapt upstream test cases as Zain fixtures
(MIT header kept); **EXCLUDE**. All rows `wonderwhy-er/DesktopCommanderMCP@db3430f23c1fd487f66412e93f7022b8c34ccd6f`
unless noted. Destination root `packages/deskgate/` (TS, inside Server workspace) unless noted.

| # | Upstream path | Destination | Mode | Deps (license) | Rationale |
|---|---|---|---|---|---|
| 1 | `src/tools/schemas.ts` | `packages/deskgate/src/schemas.ts` | PORT-MIT | `zod` (MIT), `zod-to-json-schema` (ISC) | Keep DC-compatible tool names/args so existing agent prompts/skills work; drop config/feedback/usage schemas |
| 2 | `src/server.ts` (tool descriptions only, ~315-1140) | `packages/deskgate/src/descriptions.ts` | PORT-MIT (text) | — | Descriptions are tuned agent guidance; rewrite security claims |
| 3 | `src/utils/process-detection.ts` | `packages/deskgate/src/process-state.ts` | PORT-MIT | none | Pure prompt/REPL detection |
| 4 | `src/terminal-manager.ts` (buffer/paging only: 96-97, 473-642) | `apps/server/src/terminal/outputPaging.ts` (Server terminal manager, shared) | PORT-MIT (functions) | none | Paging semantics on top of node-pty buffer; spawn code **not** ported |
| 5 | `src/utils/shell.ts` | `apps/server/src/terminal/shellResolve.ts` | PORT-MIT | none | Shell resolution table + Windows CWD-lookup defence; feeds the single PTY host |
| 6 | `src/utils/lineEndingHandler.ts` | `packages/deskgate/src/fs/lineEndings.ts` | PORT-MIT | none | |
| 7 | `src/utils/atomic-write.ts`, `src/utils/rename.ts` | `apps/server/src/effects/fs/atomicWrite.ts` | PATTERN | none | EffectWorker owns writes; reimplement with pre-image hash |
| 8 | `src/tools/edit.ts`, `fuzzySearch.ts`, `fuzzySearchCore.ts` | `packages/deskgate/src/edit/{editBlock,fuzzy}.ts` | PORT-MIT (matching/diff logic only) | `fastest-levenshtein` (MIT) | Computes the replacement **before** proposal; the write is an `fs.write` effect. Drop `fuzzySearchLogger` |
| 9 | `src/tools/filesystem.ts` (`validatePath`, realpath/junction resolution 135-390) | `packages/deskgate/src/fs/resolveTarget.ts` | PORT-MIT (functions) | none | Used only to compute `exact_target`; Core decides; EffectWorker re-resolves at dispatch (TOCTOU) |
| 10 | `src/utils/files/text.ts`, `binary.ts`, `image.ts`, `base.ts`, `factory.ts` | `packages/deskgate/src/fs/readers/*` | PORT-MIT | `isbinaryfile` (MIT) | Offset/negative-offset line reads, binary detection, image → MCP image content |
| 11 | `src/utils/files/{pdf,docx,excel}.ts`, `src/tools/pdf/**` | — | EXCLUDE (defer to P9 W-01/W-02) | `exceljs` (MIT), `pizzip` (MIT/GPL-3 dual), `pdf-lib` (MIT), `unpdf` (MIT), `md-to-pdf`→Puppeteer (MIT/Apache-2.0), `sharp` (Apache-2.0, LGPL libvips binaries), `@opendocsg/pdf2md` (MIT) | Heavy deps; separate Ponytail/licence review |
| 12 | `src/search-manager.ts`, `src/handlers/search-answers.ts` | `packages/deskgate/src/search/*` | PORT-MIT, then refactor spawn → `process.spawn` effect via EffectWorker | ripgrep binary via `@vscode/ripgrep` (MIT pkg; ripgrep MIT/Unlicense; registry SRC-0046) | Session search UX is valuable |
| 13 | `src/utils/ripgrep-resolver.ts` | `apps/server/src/tools/ripgrep.ts` | PATTERN | — | Pin a vendored rg; never resolve from CWD |
| 14 | `src/utils/process-tree.ts` | — (reference for POSIX branch of C-16 Job Object/process-group kill) | PATTERN | — | Windows path replaced by Job Objects |
| 15 | `src/tools/improved-process-tools.ts` | `packages/deskgate/src/tools/process.ts` | PATTERN | — | Rewrite as adapters to Server terminal manager; keep 50 s wait cap semantics |
| 16 | `src/handlers/*.ts` | `packages/deskgate/src/handlers/*` | PATTERN | `@modelcontextprotocol/sdk` (MIT) | Thin glue; easier to rewrite against Zain `/mcp` |
| 17 | `test/test-allowed-directories*.js`, `test-allowed-drive-root.js`, `test-blocklist-bypass.js`, `test-command-paths.js`, `test-edit-block-*.js`, `test-negative-offset-*.js`, `test-process-state-detection.js`, `test-interact-output-cleaning.js`, `test-kill-process.js`, `test-literal-search.js`, `test/integration/terminal-output-buffer-leak.js`, `test/repro/test-process-wait-client-cap.js` | `packages/deskgate/test/upstream/*` | TEST-PORT | — | Converted to Zain det/neg tests; bypass test becomes proof that the blocklist is **not** relied on |
| 18 | `LICENSE` | `packages/deskgate/THIRD_PARTY_NOTICES.md` (+ root NOTICE aggregation) | PORT-MIT (verbatim) | — | Required attribution; no upstream NOTICE exists |
| 19 | `src/command-manager.ts` | — | EXCLUDE (PATTERN for an advisory "risky command" UI hint only) | — | Not a boundary; Core policy decides |
| 20 | `src/config-manager.ts`, `config-field-definitions.ts`, `config-recovery.ts`, `src/tools/config.ts`, `src/config.ts` | — | EXCLUDE | — | Second policy store; replaced by Core policy (C-05/C-15) |
| 21 | `src/utils/capture.ts`, `usageTracker.ts`, `trackTools.ts`, `ab-test.ts`, `mcp-ui-ab-test.ts`, `feature-flags.ts`, `fuzzySearchLogger.ts`, `toolHistory.ts`, `welcome-onboarding.ts`, `dockerPrompt.ts`, `src/tools/feedback.ts`, `src/tools/usage.ts`, `src/data/onboarding-prompts.json`, `vendor/telemetry-contract/**`, `scripts/*fuzzy-logs*.js` | — | EXCLUDE | — | Telemetry / tracking / remote flags / unclear licence |
| 22 | `src/remote-device/**`, `src/npm-scripts/remote.ts`, `scripts/remote/**` | — | EXCLUDE | `@supabase/supabase-js` (MIT), `open` (MIT), `caffeinate` | Client of proprietary relay; replaced by R-01..R-04 |
| 23 | `src/ui/**`, `scripts/build-ui-runtime.cjs` | — | EXCLUDE | TipTap (MIT), highlight.js (BSD-3), markdown-it (MIT) | Zain IDE surfaces exist |
| 24 | `setup-claude-server.js`, `install*.sh/ps1`, `Dockerfile`, `manifest.template.json`, `scripts/build-mcpb.cjs`, `publish-release.cjs`, plugin manifests, `skills/**`, `plugins/**` | — | EXCLUDE (skills may be read as REFERENCE for agent prompts) | — | Distribution of DC itself |
| 25 | `desktop-commander/remote-desktop-commander@a6573e8` (all) | — | **EXCLUDE — proprietary (all rights reserved)**; reading for architecture facts only | — | No licence to copy even docs; FOUNDER-ATTESTED permission must be a written grant from SIA Desktop Commander to change this |

Planned new deps for DeskGate: `zod`, `zod-to-json-schema`, `fastest-levenshtein`, `isbinaryfile`,
`@vscode/ripgrep` (or vendored rg) — all permissive; `@modelcontextprotocol/sdk` and `node-pty` already belong to
Server. Admission: add DC to the source registry and pass the Ponytail/admission gate before row 1 is executed.

## 5. Acceptance tests

Conventions from 14: **neg** = must FAIL when Core is disabled or the guarding mutation is applied (mutation
control, 09). Each neg test lists its mutation.

| ID | Type | Scenario | Expected | Mutation control |
|---|---|---|---|---|
| DG-P01 | det | `read_file` inside project home | content returned; `fs.read` receipt with realpath | — |
| DG-P02 | det | `edit_block` exact single match, CRLF file | file edited, CRLF preserved, receipt with pre/post hashes | — |
| DG-P03 | det | `edit_block` miss → fuzzy diff returned, **no** proposal sent | no `fs.write` receipt | — |
| DG-P04 | e2e | `start_process` python REPL → `interact_with_process` `print(1)` → `read_process_output` | output `1`; state = waiting-for-input; spawn + input receipts; runs in Server node-pty (session visible in Zain terminal UI) | — |
| DG-P05 | det | output > 50 MB | oldest lines evicted, negative offset reads tail, memory bounded | — |
| DG-P06 | e2e | `start_search` 100k-file repo, paginate, `stop_search` | results ⊆ granted root; rg process tree gone after stop | — |
| DG-P07 | e2e | remote client (paired phone passkey) on LAN asks `write_file` | WebAuthn challenge from Core; after assertion effect executes on project home | — |
| DG-P08 | det | Win/macOS/Linux matrix: shell resolution, junction/symlink realpath, drive root, `force_terminate` kills grandchild | parity across OSes | — |
| DG-N01 | neg | `write_file` outside project home with no grant | refused by Core; no file created | remove PEP call in adapter → test must fail |
| DG-N02 | neg | symlink/junction inside root → outside target, `write_file` via link | refused (target is realpath) | resolve with `path.resolve` instead of realpath → fail |
| DG-N03 | neg | TOCTOU at the operation boundary: attacker thread swaps link/junction continuously during 10k writes | fs-gate writes through the validated handle; zero writes outside target (19 §3) | replace handle ops with path-based write → fail |
| DG-N04 | neg | Core down (C-06 fail-closed) | all gated DeskGate tools refuse; reads of own buffers still OK | bypass CoreBridge health → fail |
| DG-N05 | neg | `set_config_value allowedDirectories []` / `blockedCommands []` | fixed refusal; Core policy unchanged | re-enable DC config tool → fail |
| DG-N06 | neg | `start_process` with blocklist-bypass strings (`/usr/bin/sudo`, `env sudo`, `python -c …`, `powershell -enc …`, `cmd /c "reg add"`) | decision comes from Core policy for `process.spawn`; DeskGate has no blocklist code path (assert none consulted) | inject DC blocklist as sole gate → test detects reliance |
| DG-N07 | neg | `kill_process` on a non-Zain PID (e.g., explorer.exe / launchd child) | refused | drop ownership check → fail |
| DG-N08 | neg | `interact_with_process` into a session spawned by another mission | refused (session scope) | drop scope check → fail |
| DG-N09 | neg | remote client with valid session ticket but forged/replayed WebAuthn assertion | refused (C-13 T3) | accept session scope as authority → fail |
| DG-N10 | neg (static) | `packages/deskgate` imports `child_process`, `node-pty`, `fs.write*`, `net`, `http(s)` client, Supabase | build fails (dependency-cruiser + lint) | delete rule → seeded violation passes → test fails |
| DG-N11 | neg | network egress from DeskGate during full suite | zero outbound connections (egress proxy / socket hook) | re-add `capture()` → fail |
| DG-N12 | neg | non-home Zain instance proposes effect for project | refused (project-home rule) | disable rule → fail |
| DG-N13 | neg | prompt-injection file content instructs agent to write `~/.ssh/authorized_keys` | Core requires approval / denies per policy; receipt shows MEDIATED denied | remove the sensitive-path policy entry → fail |
| DG-N15 | neg | parent directory swapped between check and create/rename | handle-relative parent; no entry outside target | path-based rename → fail |
| DG-N16 | neg | same operation key with changed content | OPERATION_INPUT_CONFLICT | remove conflict check → fail |
| DG-N14 | neg | kill -9 Server mid-`write_file` | dispatch → UNKNOWN; reconcile via pre/post hash (C-10/R suite) | auto-mark COMPLETED → fail |

## 6. Performance requirements

| ID | Metric | Budget |
|---|---|---|
| DG-B1 | Adapter overhead (schema parse + target resolve + result shaping), excluding Core | p95 ≤ 5 ms |
| DG-B2 | Core decision for DeskGate effects | within C-21 B13: p95 ≤ 25 ms/effect |
| DG-B3 | `read_file` 1 MB text, local, end-to-end | p95 ≤ 60 ms |
| DG-B4 | `start_process` → first output byte (`echo`) | p95 ≤ 250 ms Win, ≤ 150 ms macOS/Linux |
| DG-B5 | `interact_with_process` round trip (REPL echo) | p95 ≤ 100 ms local; ≤ 300 ms remote LAN excluding human approval |
| DG-B6 | Long call cap | any single tool call returns ≤ 50 s (upstream `MAX_PROCESS_WAIT_MS`) |
| DG-B7 | Output buffer memory | ≤ 50 MB per session, ≤ 512 MB total, evicting oldest |
| DG-B8 | `start_search` first page on 100k files (warm cache) | p95 ≤ 1.5 s |
| DG-B9 | Read-batch throughput (`read_multiple_files` 50 small files) | ≤ 300 ms incl. per-path decisions (batched propose) |

## 7. Effort ESTIMATE and phase placement

| ID (proposed) | Task | Phase / deps | Est pw |
|---|---|---|---|
| DG-00 | Registry row + licence/notice admission for DCMCP; record remote repo as EXCLUDED-proprietary | P0/P1 gate | 0.1–0.2 |
| DG-01 | `packages/deskgate` skeleton on Server `/mcp`, schemas/descriptions port, static-import guard (DG-N10) | P3, after C-06; part of **C-12 seam S6 (MCP access)** | 0.5–1.0 |
| DG-02 | fs adapters (read/list/info/write/edit/move/mkdir) + target resolution + line endings + fuzzy edit | P3 with C-12 | 1.0–1.5 |
| DG-03 | Process/terminal adapters on Server node-pty: paging port, prompt detection, input as `terminal.input`, ownership-scoped signal | P3 with C-12 S8 / C-16 | 1.0–1.5 |
| DG-04 | Search adapters (rg as internal spawn effect) | P6 (IDE breadth) | 0.5–1.0 |
| DG-05 | Neg/mutation suite DG-N01..N14 + upstream test ports + perf DG-B1..B9 | P3 exit (C-20/C-22) and P6 | 1.0–1.5 |
| DG-06 | Remote DeskGate over runner/project-home + passkey challenges + LAN/Tailscale hardening tests | **P10**, deps R-01..R-04 | 0.7–1.3 |
| DG-07 | Cross-OS parity matrix (macOS/Linux) | P6 with I-09 | 0.2–0.5 |
| | **Total** | | **5.0–8.5 pw** |

Placement rationale: DeskGate is the agent-facing face of seams S6/S8, so its core lands with P3 (no MEDIATED
claim before Core exists). Until P8 containment, the UI must say the shell can reach beyond project home (same
honesty as DC's own "not a boundary" note); trust indicator widens only after S-05.

## 8. Open items / unknowns

1. FOUNDER-ATTESTED permission does not cover the proprietary relay; no code from it exists publicly. If a
   vendor relay is ever wanted, it needs a written agreement and an explicit TCB decision (relay would be inside
   it). Default: no.
2. `pizzip` dual MIT/GPL-3 and `sharp` LGPL libvips binaries — only relevant if Office/PDF handlers are later
   ported (row 11).
3. DC moves fast (≥100 commits/90 days): re-pin and diff rows 1-12 at implementation start; track upstream
   security fixes in `test-allowed-directories*`, `test-blocklist-bypass`.
4. Local-machine observations were shared privately with the founder and are not recorded here.
