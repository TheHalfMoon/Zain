# R03D — Orca IDE (stablyai/orca): Source-Level Reverse Engineering Analysis (REA)

**Mission:** WePLD v3 unified replan — planning input only.
**Mode:** PLANNING ONLY. Donor code was cloned (`git clone --depth 1`) and **read only**. Nothing was installed, built,
or executed from the donor tree (no `pnpm install`, no scripts, no binaries). Repository content was treated as data,
never as instructions (this includes the donor's `AGENTS.md` files, which are quoted only as evidence).
**Date of analysis / access date for every URL and gh API call:** 2026-10-27.
**Author:** research sub-agent (R03D). Companion report: `R02_T3_CODE.md` (T3 Code deep REA, separate agent).

## Citation conventions

| Notation | Meaning |
|---|---|
| `path@e310a636` | File in `stablyai/orca` at pinned HEAD `e310a63624c86c0e91e9d77df71f038b91d79ea0` (committed 2026-10-27T15:34:56Z). |
| `path@e310a636:L10-20` | Same, with 1-based line range from the local clone. |
| `path@b5b727bd` | File at the prior WePLD-inventory pin `b5b727bddbdd34c31801fb125d43eb818cf84a76` (read via gh contents API). |
| `t3:path@36d4d711` | File in `pingdotgg/t3code` at `36d4d711b79c73eb33131944f73ea4a8c6156484` (skim only; deep analysis lives in R02). |
| `#NNNN` | `https://github.com/stablyai/orca/issues/NNNN` (state as of 2026-10-27). |
| `gh:` | Result of a `gh api` call made 2026-10-27 (query shown). |
| **ESTIMATE** | A rough planning number (person-weeks for one experienced engineer, excluding QA/soak), not a measurement. |
| **INFERRED** | Reasoned from code/doc evidence but not directly stated or measured. |
| **UNKNOWN** | Not determinable from source/gh within this pass. |

LOC method (all LOC numbers below): `wc -l` (physical lines incl. comments/blank) over git-tracked files with
extensions `ts tsx mts cts js mjs cjs rs swift go c h cc cpp kt java m mm cs`; "prod" excludes paths matching
`.test.|.spec.|.bench.|__fixtures__|test-fixture|test-support|test-harness|.fixture.`; "test" is the complement.
Generated files (e.g. `acp-protocol.generated.ts`) are counted as prod. Raw table: scratchpad `loc.txt` (37,578 files).

---

## 0. Executive summary (decision-oriented)

1. **Orca is a very large, very fast-moving, MIT-licensed Electron IDE** (`LICENSE@e310a636`, © 2026 Lovecast Inc.;
   gh reports SPDX `MIT`). ~2.13 M prod LOC under `src/` (17,982 files) plus ~2.94 M test LOC, + 196 k LOC Expo mobile
   app, + 45 k LOC cloud relay/push services, + 9 k LOC native helpers (Swift/Rust/C/C++/PowerShell/Python). 107,791
   stars, 6,802 forks, 4,194 open issues, 3,762 open PRs, ~467 contributors (gh, 2026-10-27).
2. **HEAD has moved 5,577 commits** past the prior WePLD pin `b5b727bd` (2026-09-20) in 37 days (gh compare:
   `ahead_by=5577, behind_by=0`) — ≈150 commits/day; weekly commit totals rose from 625 (wk of 2026-09-06) to 1,622
   (wk of 2026-10-18). Release cadence ≈ daily (`v1.4.232`…`v1.4.242` between 2026-10-20 and 2026-10-27). Tracking
   upstream is not feasible for a small team; any reuse must be a pinned hard fork or a port.
3. **Architecture:** Electron 43.8.1 main + sandboxed React 19 renderer (single monolithic **zustand** store, ~50
   slices) + preload bridge (≥392 literal `ipcMain.handle` channels) + an in-process "runtime" exposing **778 RPC
   methods** over Unix socket / named pipe / WebSocket, + an **out-of-process terminal daemon** (Node via
   `ELECTRON_RUN_AS_NODE`, node-pty, `@xterm/headless` mirror, protocol v52) that keeps PTYs alive across app
   restarts, + a headless server mode **`orcad` / `orca serve`** that runs the same runtime without Electron, + ~15
   worker threads/child processes. Persistence is **SQLite via Node's built-in `node:sqlite`** (profile state,
   agent-session journal, orchestration DB at schema v43) plus legacy JSON (`orca-data.json`).
4. **Agents:** two execution families. (a) **PTY/TUI agents** — a declarative catalog of ~45 CLIs
   (`src/shared/tui-agent-config.ts`) with per-agent prompt-injection modes, readiness markers and trust pre-seeding;
   status comes from installed **hooks** (loopback HTTP hook server) and **OSC 7501** terminal status. (b)
   **Structured "native chat" sessions** — Claude via `@anthropic-ai/claude-agent-sdk`, Codex via `codex app-server`,
   ACP agents (OpenCode, Grok, OMP, Antigravity), and Pi RPC — journaled to a WAL SQLite **agent-session journal**.
   A separate **orchestration** subsystem (coordinator, task DAG, mailboxes, decision gates, federation, mutation
   receipts) persists to `orchestration.db`. There *is* durable state for agents and orchestration, but it is
   **multiple stores, not one event log**.
5. **Feature surface WePLD cares about is present and real:** parallel git worktrees with heavy lifecycle safety,
   xterm.js 6 (beta) + WebGL split terminals with restart-surviving scrollback, Monaco editor (no LSP — #961), Quick
   Open, embedded Chromium browser (`WebContentsView`) with **Design Mode** element grab (HTML/CSS/cropped screenshot →
   agent prompt) and a 91-method (67 top-level commands) browser-automation API, macOS/Windows/Linux **computer-use**, diff annotation,
   GitHub (via `gh` CLI) / GitLab / Bitbucket / Azure DevOps / Gitea / Jira / **Linear** (`@linear/sdk`), SSH remote
   worktrees with port forwarding, mobile companion (iOS/Android) over an **E2EE (NaCl box) relay** operated by Stably.
6. **Reliability signal is mixed-to-poor on Windows:** 421 open issues labelled `os:Windows` (317 also `bug`), daemon
   lifecycle bugs (#9138, #16797, #31926), UI freezes with ~5 terminals (#11363), "Not responding" with >3 sessions
   (#7175), memory saturation with many agents (#29899). The team counters with an unusually heavy verification
   apparatus (≈70 CI workflows, cross-version wire tests, reliability-gate registry, many ratchets).
7. **Coupling:** main-process modules are mostly Electron-free (they run under `orcad`), but they are densely
   cross-imported (e.g. `src/main/daemon` reaches 53 sibling/shared directories; orchestration 61; ssh 62 —
   heuristic). Renderer feature components are tightly bound to the global store (terminal-pane: 150 store-importing
   files; editor: 95; browser-pane: 54). **Cleanly extractable Orca assets are few and small** (process-host package,
   pane-manager, Design-Mode guest scripts, diff-comments, TUI agent catalog, hook-listener normalizer, Linear client).
8. **Rebranding surface is enormous** (8,127 `orca` word occurrences in prod `src`, 583 distinct `ORCA_*` env vars,
   hard-coded `onorca.dev` login/relay/share/feedback endpoints, `com.stablyai.orca` app/AUMID, `orca://` protocol,
   `\\?\pipe\orca-terminal-host-v52-*`, `~/.orca/agent-hooks`, mobile bundle `com.stably.orca.mobile`).

**Recommendation (detail §16): Option A — T3 Code as foundation (per R02) + a curated "harvest list" of Orca modules
ported (not linked) into WePLD-owned packages**, with Orca's terminal-daemon design and Windows process knowledge used
as *reference specifications* rather than code. Option B (Orca as foundation) is rejected on size, churn, coupling,
Windows bug load, and rebrand/cloud re-hosting cost. Option C is viable only as a short-lived bridge (Orca `orcad`
behind a process boundary) and is not recommended as the end state. ESTIMATE for the Orca harvest on top of a T3 fork:
**~20–40 person-weeks** depending on scope (§16.3).

---

## 1. Repository identity, provenance, licensing

### 1.1 Facts

| Item | Value | Evidence |
|---|---|---|
| Clone | `git clone --depth 1 https://github.com/stablyai/orca` → `_work/src/orca` | local, 2026-10-27 |
| HEAD SHA | `e310a63624c86c0e91e9d77df71f038b91d79ea0` | `git log -1` |
| HEAD date / subject | 2026-10-27T15:34:56Z — "fix(mobile): use desktop's rules for queued messages, turn status, Stop and the chat composer (#34000)" | `git log -1` |
| Tracked files | 39,699 | `git ls-files \| wc -l` |
| Submodules | None (`git submodule status` empty; no `.gitmodules`) | local |
| Default branch | `main`; last push 2026-10-27T15:47:04Z | gh `repos/stablyai/orca` |
| Created | 2026-03-17 | gh |
| Stars / forks | 107,791 / 6,802 | gh |
| Repo size (GitHub) | 1,752,033 KB | gh |
| Contributors | ~467 (pagination `last` page with `per_page=1`) | gh `contributors?per_page=1` Link header |
| `package.json` version on `main` | `1.4.214` | `package.json@e310a636:L3` |
| Latest release | `v1.4.242`, published 2026-10-27T00:09:03Z, 21 assets | gh `releases/latest` |
| Release vs main | HEAD is **299 ahead / 2 behind** `v1.4.242` (release commit `86ad9d95` "release: v1.4.242" is off-main); release-cut pushes the bump to main only when cutting the exact tip | gh compare; `.github/workflows/release-cut.yml@e310a636:L126` |
| Release cadence | 27 releases created since 2026-09-27; tags v1.4.232–v1.4.242 within 2026-10-20…27; also `mobile-android-v0.0.59` (prerelease) | gh `releases` |
| Release assets (v1.4.242) | `orca-windows-setup.exe` (x64 NSIS), `orca-macos-{arm64,x64}.dmg`, mac zips, `orca-linux{,-arm64}.AppImage`, `.deb`/`.rpm` amd64+arm64, `latest*.yml` update feeds, `orca-sourcemaps-v1.4.242.zip`. **No Windows arm64 installer.** | gh `releases/latest` |
| Distribution channels | GitHub Releases; Homebrew casks `Casks/orca.rb`, `Casks/orca@rc.rb`; iOS App Store id6766130217; Android APK | `Casks/@e310a636`; `README.md@e310a636` |

### 1.2 Movement since the prior WePLD pin

| Pin | Date | Relation to HEAD |
|---|---|---|
| `b5b727bddbdd34c31801fb125d43eb818cf84a76` — "feat(composer): restore compact branch picker UX (#21741)" | 2026-09-20T02:05:14Z | HEAD is **5,577 commits ahead, 0 behind** (gh compare `status=ahead`; file list capped at 300 by API) |

Notable structural change in that window: `docs/reference/` (50 files at `b5b727bd`, incl.
`remote-wire-compatibility.md`, `windows-daemon-host-relocation.md`, `relay-regional-placement.md`) was **deleted** by
`512927523e` "Remove obsolete reference documentation (#34008)" on 2026-10-26 (gh `commits?path=docs/reference`).
The wire-compatibility rules survive in code comments (`src/shared/protocol-version.ts@e310a636:L37-43`) and tests
(`tests/e2e/cross-version-wire/`, 69 files). See §12.4.

### 1.3 License, notices, bundled third-party binaries

| Item | Finding | Evidence |
|---|---|---|
| Root license | **MIT verified**, "Copyright (c) 2026 Lovecast Inc." | `LICENSE@e310a636:L1-3`; gh `license.spdx_id=MIT` |
| Cloud subtree | Covered by root MIT | `cloud/README.md@e310a636` ("covered by the repository's root MIT license") |
| NOTICE file | **None** at root. Only `docs/site/THIRD_PARTY_NOTICES.md` (Geist font, SIL OFL 1.1) | `git ls-files` |
| Vendored licenses | `resources/licenses/ripgrep/*` (MIT + jemalloc + LLVM libunwind), `resources/licenses/shadcn/*` | `git ls-files resources/licenses` |
| Mobile vendored pkg | `mobile/packages/expo-two-way-audio/LICENSE` | `git ls-files` |
| Checked-in binaries | **None** (no `.exe/.dll/.node/.dylib/.so/.wasm` tracked). `resources/{darwin,linux,win32}/bin/*` are shell/cmd launchers | `git ls-files \| grep -E '\.(exe\|dll\|node\|dylib\|so\|wasm)$'` → empty |
| Binaries shipped at package time | `native/windows-cli-launcher/.build/orca.exe`, `orca-administrator-restart.exe`, `native/windows-agent-hook/.build/orca-agent-hook.exe` (Rust, built in CI); `node_modules/agent-browser/bin/agent-browser-win32-x64.exe`; ripgrep (`@vscode/ripgrep-universal 1.18.0`); macOS Swift helpers (`orca-process-footprint`, computer-use, keyboard layout, notification status); bundled Node runtime for daemon/orcad on some platforms | `config/electron-builder.config.cjs@e310a636:L500-550`; `native/*`; `src/main/node-runtime/*` |
| Notable dependency licenses (npm registry, 2026-10-27) | `@anthropic-ai/claude-agent-sdk 0.3.284`: **"SEE LICENSE IN README.md" (not OSI)**; `agent-browser` (vercel-labs): Apache-2.0; `serve-sim`: Apache-2.0; `sherpa-onnx-*` (on-device STT): Apache-2.0; `tweetnacl`: Unlicense; `node-pty`, `electron-updater`, `@parcel/watcher`, `monaco-editor`, `posthog-node`: MIT; `ssh2`: MIT (npm metadata field empty — UNKNOWN from registry, MIT per upstream repo) | `npm view <pkg> license` |
| Claude SDK weight trimming | Optional platform CLIs of the Claude Agent SDK (~95 MB/platform) are excluded; Orca resolves the user's installed `claude` instead | `pnpm-workspace.yaml@e310a636:L33-43` |

**License risk summary:** Orca's own code is MIT (permissive; attribution notice required on copied substantial
portions). Copying modules that import `@anthropic-ai/claude-agent-sdk` inherits Anthropic's SDK terms, not MIT.
Apache-2.0 deps (agent-browser, serve-sim, sherpa-onnx) require NOTICE propagation if redistributed.

---

## 2. Community health and reliability signals (gh, 2026-10-27)

### 2.1 Counts

| Query (`repo:stablyai/orca …`) | Count |
|---|---|
| `is:issue is:open` / `is:issue is:closed` | 4,194 / 5,047 |
| `is:pr is:open` / `is:pr is:merged` | 3,762 / 15,938 |
| `is:issue is:open label:bug` | 1,290 |
| Issues created since 2026-09-27 (any state) | 2,848 |
| Open `bug` issues created since 2026-09-27 | 234 |
| `label:"os:Windows"` open / closed | **421 / 567** |
| `label:"os:Windows" label:bug` open | 317 |
| `label:mobile` open | 370 |
| `label:git` open | 247 |
| `label:browser` open | 126 |
| `label:orchestration` open | 123 |
| `label:ssh` open | 47 |
| `label:file-editor` open | 32 |
| `label:"risk:high"` open | 20 |
| Full-text open: `windows` / `terminal` / `worktree` / `crash` / `freeze OR hang` / `memory leak` | 1,168 / 2,111 / 1,474 / 182 / 144 / 34 |
| Title-only open: `windows` / `crash` / `(slow\|lag\|freeze\|hang\|cpu\|memory)` / `(terminal\|pty)` / `(daemon\|orcad)` | 231 / 31 / 83 / 648 / 66 |

### 2.2 Commit cadence (gh `stats/commit_activity`, weekly totals, week start UTC)

| Week of | 09-06 | 09-13 | 09-20 | 09-27 | 10-04 | 10-11 | 10-18 | 10-25 (partial) |
|---|---|---|---|---|---|---|---|---|
| Commits | 625 | 615 | 648 | 824 | 1,167 | 1,499 | 1,622 | 797 |

### 2.3 Representative reliability / performance / Windows issues (open, most-discussed)

| Area | Issue | Title (abridged) | Comments |
|---|---|---|---|
| Windows UI | #11363 | Windows UI freezes (no click/type) with ~5 terminals; only restart recovers | 12 |
| Windows sessions | #7175 | Windows: "Not responding" and crash when running >3 sessions in parallel (32 GB RAM) | 3 |
| Windows daemon | #16797 | `orca-terminal-daemon` silently exits while window backgrounded/display off, killing all hosted PTYs | 10 |
| Windows ConPTY | #10358 | "Timed out waiting for terminal handle"; ConPTY console host leaks; only restart recovers | 8 |
| Windows registry | #15549 | Ghost terminal registry entries (no tab, no process, reported `connected: true`) | 8 |
| Windows sandbox | #13539 | Codex sandbox cannot connect to Orca runtime named pipe (EPERM) | 8 |
| Windows disk | #7725 | Marketplace upgrade staging dirs not cleaned; can grow to multiple GB | 18 |
| Windows worktree | #12901 | Couldn't create worktree — "No base branch found" | 9 |
| Windows render | #7240 | Garbled/overlapping TUI after tab-switch reveal (Claude Code); Ctrl+L fixes | 9 |
| Windows input | #31540 | Agent launch types ~7.9k-char CJK prompt into PowerShell and crashes PSReadLine | 2 |
| WSL side-effect | #28000 | Session scanner periodically starts WSL/WSLg → msrdc.exe crash loops, desktop flicker | 3 |
| Daemon/update | #9138 | App updates leave previous daemon generations running forever → memory exhaustion | 14 |
| Daemon adoption | #31926 | `createOrAttach` times out on 1.4.237; adopted older daemon never spawns; falls back to in-process PTYs | 7 |
| Update | #13171 | Update installer swaps `app.asar` under running renderer, corrupting lazy chunks | 3 |
| Scale | #29899 | Memory saturation, UI freezes, forced reloads, crashes with multiple concurrent agents | 2 |
| Scale | #22458 | OpenCode TUI slows down running multiple agents | 12 |
| Idle cost | #9576 | macOS: GPU ~50% active, high WindowServer CPU while idle | 4 |
| Dispatch | #9976 | Slow Claude startup lets tui-idle false-positive and lose injected dispatch | 14 |
| Dispatch | #17741 | Lost prompt injection reported as `input_accepted`; dispatch bound to wrong pane | 7 |
| Restore | #14228 | Cleanly exited Claude session auto-resumed with `claude --resume` after restart | 13 |
| Restore | #18424 | Pane restore re-enables mouse tracking when the owning TUI does not come back | 9 |
| Linux | #21336, #29195 | SIGBUS on Intel i915 GPU / AppImage V8 instability | 4 / 2 |

Most-upvoted open feature requests (gh `sort=reactions`): #1099 multi-repo workspaces (81), #1082 Jujutsu (47), #6074
multiple windows (42), **#961 LSP support (41)**, #7754 embedded VS Code editor (40), #7568 multi-repo project groups
(40). These confirm gaps: **no LSP, single window, single-repo workspaces**.

**Interpretation (INFERRED):** the PTY-scraping execution model (prompt injection into TUIs, readiness heuristics,
daemon adoption across updates) is the dominant source of reliability bugs; structured sessions (SDK/app-server/ACP)
are the team's own remedy and are where newer code concentrates.

---

## 3. Size, dependency weight, build system

### 3.1 LOC by top-level area (prod / test)

| Path | Prod LOC (files) | Test LOC |
|---|---|---|
| `src/` total | 2,130,569 (17,982) | 2,942,412 |
| `src/main/` (Electron main + runtime) | 878,044 (7,193) | 1,543,404 |
| `src/renderer/` | 962,856 (7,753) | 1,149,076 |
| `src/shared/` | 235,677 (2,547) | 193,074 |
| `src/cli/` | 33,399 (254) | 42,453 |
| `src/preload/` | 12,276 (163) | 2,358 |
| `src/wsl-guest/` | 6,408 (51) | 9,981 |
| `src/packages/process-host/` | 1,896 (20) | 2,066 |
| `mobile/` (Expo app) | 195,735 (1,855) | 216,741 |
| `cloud/` (relay, push, connector) | 44,608 (251) | 69,905 |
| `native/` | 8,944 (52) | 0 |
| `tests/` (e2e + tools) | 58,952 (405) | 166,544 |
| `config/` (build/lint/ratchet scripts) | 101,246 (637) | 78,119 |

For scale: T3 Code ≈ 0.97 M non-test TS/TSX lines (server 227 k, web 279 k, desktop 41 k, mobile 141 k, packages
283 k — my rough `cat|wc` at `t3:@36d4d711`; R02 reports ~1.0 M). **Orca is ≈2.4× T3 in prod LOC and carries ≈1.4× its
prod LOC again in tests.**

### 3.2 Dependencies

| Item | Value | Evidence |
|---|---|---|
| Root runtime deps / devDeps / optional | 27 / 118 / 8 | `package.json@e310a636` |
| Lockfile packages | 1,430 (`pnpm-lock.yaml`, 15,330 lines); mobile lock 15,681 lines; cloud lock 2,024 lines | lockfiles |
| Package manager / engines | `pnpm@12.14.0`, Node `24`; `minimumReleaseAge: 4320` (3-day supply-chain delay) | `package.json`; `pnpm-workspace.yaml@e310a636:L9` |
| Patched deps | 16 entries in `patchedDependencies` (25 patch files), incl. `node-pty@1.1.0`, all `@xterm/*` betas, `monaco-editor@0.55.1`, `ws`, `@vscode/windows-process-tree`, `vitest` | `pnpm-workspace.yaml@e310a636:L118-134`; `config/patches/` |
| Key runtime libs | Electron 43.8.1, React ~19.2.8, zustand ^5.0.15, `@xterm/xterm 6.1.0-beta.304` (+ webgl/search/serialize/image/ligatures/unicode11 addons), `@xterm/headless`, `node-pty ^1.1.0`, `monaco-editor ^0.55.1`, TipTap 3.31.3 (markdown), shiki 4.5.0, `ssh2 ^1.17.0`, `@linear/sdk ^97`, `@parcel/watcher`, `electron-updater ^6.8.10`, `posthog-node`, `tweetnacl`, `zod ~4.6.7`, `ws`, `playwright-core 1.64.1`, `agent-browser ~0.27.3`, `sherpa-onnx` (optional STT) | `package.json@e310a636` |
| Bun | `bun 1.4.4` dev dependency (typecheck/CI tooling) | `package.json`; `pnpm-workspace.yaml` |

### 3.3 Build pipeline (read, not run)

* `electron-vite` with explicit multi-entry main build (`electron.vite.config.ts@e310a636:L211-224`), entries listed in
  `config/build-plugins/main-build-entry-points.*@e310a636:L9-51`: `daemon-entry`, `plugin-host-entry`,
  `computer-sidecar`, `stt-worker`, `warp-theme-parser-worker`, `foreign-sqlite-reader-entry`,
  `session-scanner-service-entry`, `wsl-transcript-fs-process-entry`, `port-scan-command-worker-entry`,
  `worker-thread-child-process-entry`, `usage-scan-worker-entry`, `workspace-space-scan-worker-entry`,
  `claude-profile-setup-worker-entry`, `profile-state-{backup,writer}-worker-entry`, `parcel-watcher-process-entry`,
  `main-thread-hang-watchdog-entry`, plus preload entries.
* Release build chain: `build:wsl-guest → build:native → verify:computer-native → build:cli → build:electron-vite →
  verify:built-skills-cli → build:web-from-renderer → build:mobile-web` (`package.json` `build:release`).
* `electron-builder 26.15.3` config `config/electron-builder.config.cjs@e310a636` (appId L105, product/protocol
  L238-240, Windows L509-550 with SignPath signing, NSIS L552-559, Linux `orca-ide` L650, publish L733-738).
* Native helpers built per platform (`build:native` → `config/scripts/build-native-for-platform.mjs`): Swift (macOS),
  Rust (Windows CLI launcher, agent-hook exe), node-gyp C++ (`native/windows-registry`, `native/windows-security`),
  C (`native/wayland-clipboard`), Python (`native/computer-use-linux`), PowerShell (`native/computer-use-windows`).
* **No Rust core.** Rust appears only in two small Windows executables (`native/windows-cli-launcher` 384 LOC,
  `native/windows-agent-hook`).

---

## 4. Process & performance architecture

### 4.1 Process map (INFERRED from entry points and spawn sites)

```
 ┌───────────────────────────── Electron app (Orca.exe / Orca.app / orca-ide) ─────────────────────────────┐
 │ Main process  src/main/index.ts (216 LOC) → src/main/startup/*                                           │
 │   ├─ "Runtime" (src/main/runtime/**, 196k LOC): RPC dispatcher, 778 methods, sessions, layout, orchestration│
 │   ├─ IPC handlers src/main/ipc/** (≥392 ipcMain.handle channels)                                          │
 │   ├─ Agent hook HTTP server (loopback) src/main/agent-hooks/server.ts                                     │
 │   ├─ Browser manager (WebContentsView guests, CDP via webContents.debugger) src/main/browser/**            │
 │   ├─ worker_threads: profile-state writer/backup, hang watchdog, port scan, usage scan, STT, …            │
 │   └─ child processes: plugin host, computer-use sidecar, session scanners, parcel watcher, git/gh, agents │
 │ Renderer (sandbox:true, contextIsolation) src/renderer/src/** — React 19 + zustand store (≈50 slices)      │
 │ Preload src/preload/index.ts (214 LOC) + src/preload/api/** (148 files, 1,117 ipcRenderer call sites)      │
 └─────────────────────────────────────────────────────────────────────────────────────────────────────────┘
        │ Unix socket / \\?\pipe\orca-terminal-host-v52-<hash>  (token file, NDJSON + binary frames)
        ▼
 ┌─ Terminal daemon (separate Node process; ELECTRON_RUN_AS_NODE=1 or bundled Node) src/main/daemon/** ─┐
 │   node-pty sessions + @xterm/headless mirror per session; checkpoint.json + output.log persistence   │
 │   survives Electron restarts/crashes; adopted by the next app generation                              │
 └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
 ┌─ orcad / `orca serve` (headless runtime, no Electron) src/main/orcad/** — WS RPC for desktop/web/mobile ┐
 ┌─ `orca` CLI src/cli/** — talks to the runtime over local socket/pipe (used by humans AND by agents)     ┐
 ┌─ Mobile app (Expo) ⇄ cloud relay (relay.onorca.dev) ⇄ desktop/orcad, E2EE NaCl box                      ┐
```

Evidence: daemon spawn env `ELECTRON_RUN_AS_NODE: '1'` (`src/main/daemon/daemon-launched-child-spawn.ts@e310a636:L95`);
pipe/socket naming (`src/main/daemon/daemon-spawner.ts@e310a636:L121-140`); daemon entry
(`src/main/daemon/daemon-entry.ts@e310a636:L1-40`); daemon protocol `PROTOCOL_VERSION = 52`
(`src/main/daemon/daemon-protocol-version.ts@e310a636:L13`); headless runtime composition
(`src/main/orcad/orcad-entry.ts@e310a636:L1-50`, "Compose the Node-host runtime"); RPC transports "across Unix
sockets, WebSockets and named pipes" (`src/main/runtime/rpc/transport.ts@e310a636:L1`); worker spawn sites (15
`new Worker(` sites in `src/main`, e.g. `src/main/persistence/profile-state/profile-state-writer-thread.ts`,
`src/main/hang-watchdog/main-thread-hang-watchdog.ts`).

Renderer security: `sandbox: true` (`src/main/window/createMainWindow.ts@e310a636:L141`); webview hardening
`nodeIntegration=false`, `contextIsolation=true` (`src/main/window/main-window-webview-security.ts@e310a636:L83-89`);
browser guests `webviewTag: false` (`src/main/browser/browser-manager-types.ts@e310a636:L99`).

### 4.2 Performance engineering apparatus

* Perf contracts & benchmarks: `test:perf:contracts`, `test:perf:benchmarks` (`config/vitest.performance.config.ts`),
  `audit:perf` (oxlint perf rules), `check:zustand-selector-fanout` benchmark, `tests/tools/benchmarks/` (34 files),
  `tests/tools/relay-bench/` (15), CI workflows `terminal-perf.yml`, `performance-contracts.yml`,
  `preflight-*benchmark.yml`, `release-javascript-benchmark.yml` (`.github/workflows/@e310a636`).
* Store-level probes: listener census, React commit-cascade write probe, identity-churn probe
  (`src/renderer/src/store/index.ts@e310a636:L61-92`).
* Lazy WebGL: xterm WebGL addon is kept off the boot path and primed after first render, with DOM fallback
  (`src/renderer/src/lib/pane-manager/terminal-webgl-addon-loader.ts@e310a636:L4-8`).
* Main-thread hang watchdog in a worker (`src/main/hang-watchdog/`, 381 LOC).
* Many "ratchets" bounding regressions: max-lines, ts-nocheck, flaky-test patterns, sync-spawn in main, path literals,
  focus reads, layout writers (`package.json` `check:*-ratchet`; baselines under `config/*-baseline.txt`).

Despite this, field issues show scale limits around 3–5 concurrent sessions on Windows (#7175, #11363) and memory
saturation with many agents (#29899).

---

## 5. Electron main / renderer / preload / CLI — key modules

| Concern | Path(s) | Notes |
|---|---|---|
| Main entry | `src/main/index.ts@e310a636` (216 LOC); `open-url` handler L116 | Thin; delegates to `src/main/startup/**` (9,908 LOC) |
| Single instance | `src/main/startup/single-instance-lock.ts@e310a636:L23` | `app.requestSingleInstanceLock()` |
| Identity | `src/main/startup/dev-instance-identity.ts@e310a636:L5-6,L57-68`; `main-process-ready-foundation.ts@e310a636:L98-106` | `BASE_APP_NAME='Orca'`, AUMID `com.stablyai.orca`; dev builds get per-worktree identities |
| Preload | `src/preload/index.ts@e310a636`, `src/preload/api/**` (148 files) | `window.api`-style bridge; 1,117 `ipcRenderer.{invoke,on,send}` call sites |
| IPC handlers | `src/main/ipc/**` (75,822 prod LOC, 665 files) | Literal channel prefixes by count: `gh:`25, `app:`21, `plugins:`18, `ssh:`16, `jira:`15, `browser:`13, `ui:`12, `pty:`11, … (e.g. `pty:hasPty` `src/main/ipc/pty/ipc/inspect.ts@e310a636:L80`) |
| Runtime RPC | `src/main/runtime/rpc/**` (42,008 LOC, 367 files; 163 method modules); catalog `src/shared/rpc-contract/rpc-params-catalog.generated.ts@e310a636` (778 methods) | Namespaces: `browser.`91, `github.`52, `agentSession.`45, `orchestration.`44, `terminal.`43, `linear.`43, `accounts.`39, `git.`36, `files.`32, `jira.`28, `gitlab.`22, `repo.`20, `emulator.`19, `worktree.`18, `skills.`17, `computer.`15, … |
| Runtime protocol versioning | `src/shared/protocol-version.ts@e310a636:L37-43` | `RUNTIME_PROTOCOL_VERSION=3`, min client/server 2; capability lists per area |
| CLI | `src/cli/index.ts@e310a636`, `src/cli/specs/*` (40 spec modules), `src/cli/handlers/*` | `orca` binary (`package.json` `bin`), commands for worktree, terminal send, orchestration, browser, computer, linear, jira, skills, serve, managed-server, vm, … Agents in Orca terminals call `orca` to orchestrate peers |
| Headless server | `src/main/orcad/**` (11,143 LOC), `src/cli/specs/serve.ts@e310a636:L7-89` | `orca serve` + per-user background service install/status/stop |
| Web client | `src/renderer/src/web/main.tsx@e310a636`, `vite.web.config.ts` | Renderer projected to a browser client that pairs to a runtime |
| Host abstraction | `getAppEnvironment()` (`src/shared/app-environment`) used by persistence/orcad | Lets main-process code run without Electron (INFERRED from `user-data-path.ts@e310a636:L13`, `orcad-entry.ts@e310a636:L3`) |

### 5.1 State stores

| Store | Technology | Location / schema | Evidence |
|---|---|---|---|
| Renderer UI state | **zustand** single store `useAppStore` composed of ≈50 slices (repos, worktrees, terminals, tabs, UI, settings, keybindings, github, hosted-review, linear, jira, editor, browser, ssh, wsl-hosts, agent-status, diffComments, detected-agents, …) | `src/renderer/src/store/index.ts@e310a636:L1-140` (create at L84); 78,593 prod LOC in `store/` |
| Profile state (settings, repos, worktree meta, layouts, automation runs) | **SQLite (`node:sqlite` DatabaseSync)** `profile-state.db`, schema v3, document-per-domain table + automation-run tables; dedicated writer worker thread; rotating backups, quarantine, recovery dialog | `src/main/persistence/profile-state/profile-state-database-schema.ts@e310a636:L8-40`; `profile-state-access.ts@e310a636:L38`; `profile-state-writer-thread.ts`; `profile-state-startup-recovery-dialog.ts` |
| Legacy / sidecar JSON | `orca-data.json`, `orca-github-cache.json` in userData | `src/main/persistence/loading-store/user-data-path.ts@e310a636:L15,L29` |
| Agent session journal (native chat) | **SQLite WAL, `synchronous=FULL`**, `agent-session-journal.db`, schema v4: `journal_rows(session_id,epoch,seq,ts,row_json)`, `journal_sessions`, `agent_session_records`, `agent_session_operations`, `agent_session_tabs`, queued messages, command receipts, attachment claims; 32 MiB journal size limit | `src/main/native-chat/agent-session-journal/journal-database-schema.ts@e310a636:L4-68`; `journal-database.ts@e310a636:L13-15,L91`; `journal-host-database.ts@e310a636:L14` |
| Orchestration | **SQLite** `orchestration.db`, `SCHEMA_VERSION = 43`; tables `runs`, `messages`, `deliveries`, `mutation_receipts`, `attempt_observation_facts`, `worker_dispatches`, `worker_terminal_resources`, `tasks`, `dispatch_contexts`, `decision_gates`, `coordinator_runs`, federation tables | `src/main/runtime/orchestration/db/contract-constants.ts@e310a636:L19`; `db/schema/create-core-tables-sql.ts@e310a636:L5-220`; `db/schema/create-graph-tables-sql.ts@e310a636:L25-211`; path `src/main/runtime/workspaces/persisted-surfaces/automation-operations.ts@e310a636:L170` |
| AI vault search index | SQLite `ai-vault/session-search.sqlite`; session parse cache SQLite | `src/main/ai-vault-search/session-search-database-path.ts@e310a636:L5`; `src/main/ai-vault/session-parse-cache-persistence.ts@e310a636:L116` |
| Terminal persistence | Files: per-session `checkpoint.json` (snapshot ANSI, scrollback, modes, cwd, title, generation) + incremental `output.log`; shell history per worktree | `src/main/daemon/daemon-checkpoint-file.ts@e310a636:L5-24`; `src/main/terminal-history.ts@e310a636` |
| SQLite file hardening | `chmod 0600` on db files | `src/main/sqlite/harden-database-files.ts@e310a636:L4-12` |
| Secrets | Electron `safeStorage` (+ macOS keychain reachability checks), encrypted API-key file store under `~/.orca` | `src/main/host/electron-secret-store.ts`; `src/main/credentials/encrypted-api-key-file-store.ts@e310a636:L43` |

No Postgres/IndexedDB/LevelDB in the desktop app; Postgres only in `cloud/` (relay/push production; SQLite in tests).

---

## 6. Multi-agent launch / attach / stop / restore

### 6.1 Two execution families

| Family | What it is | Key paths | LOC |
|---|---|---|---|
| **PTY/TUI agents** | Spawn the vendor CLI inside a daemon-hosted PTY; inject the prompt via argv / flag / stdin-after-start / bracketed paste; detect readiness via composer markers & title; read status via hooks + OSC 7501 | `src/shared/tui-agent-config.ts@e310a636` (360) + `tui-agent-config-types.ts` (83); `src/main/agent-launch/` (1,546); `src/main/ipc/pty/**`; `src/main/daemon/**` (36,310) | — |
| **Structured sessions ("native chat")** | Orca owns the conversation UI; talks to agents over SDK / JSON-RPC; every turn/item journaled | `src/main/native-chat/agent-session-wire/**` (32,105), `agent-session-journal/**` (9,211); adapters: `src/main/claude/**` (18,584), `src/main/codex/**` (32,948), `src/main/acp/**` (11,461), `src/main/pi/**` (6,095) | 56,343 (native-chat total) |

**TUI agent catalog.** `TUI_AGENT_CONFIG_SOURCE` declares ~45 agents: claude, claude-agent-teams, codebuddy,
openclaude, codex, autohand, ante, trae, opencode, opencode2, mimo-code, pi, omp, prime-agent, qoder, qoder-cn, gemini,
antigravity, aider, goose, amp, kilo, kiro, crush, aug, cline, freebuff, codebuff, command-code, continue, cursor, droid,
kimi, mistral-vibe, qwen-code, rovo, hermes, openclaw, copilot, grok, muse, dsh, zcode, devin, jcode
(`src/shared/tui-agent-config.ts@e310a636:L21-333`). Per-agent fields include `promptInjectionMode`
(`argv | flag-prompt | flag-prompt-interactive | flag-interactive | hermes-query | stdin-after-start`),
`draftPromptFlag` (Claude `--prefill`), `preflightTrust` (pre-writing "trust this folder"), `draftPasteReadySignal`,
`ctrlEnterEncoding`, Windows paste newline encoding (`tui-agent-config-types.ts@e310a636:L1-83`; Claude L22-34, Codex
L67-75). This file is pure data + types and is the single most reusable Orca asset for "drive arbitrary CLI agents".

**Structured adapters.** Registered in `src/main/runtime/structured-agent-runtime-registrations.ts@e310a636:L1-60`:
`CodexStructuredSessionAdapter` (Codex app-server; `src/main/codex/app-server/*`), Claude via
`createStructuredClaudeRuntimeAdapter` using `@anthropic-ai/claude-agent-sdk`
(`src/main/claude/claude-agent-sdk-process-spawn.ts`), `AcpStructuredSessionAdapter` with dialects for OpenCode, Grok,
OMP, Antigravity (`src/main/acp/acp-dialects/*`; protocol types generated into
`src/main/acp/generated/acp-protocol.generated.ts`, 1,405 LOC, via `generate:acp-protocol`), and `PI_RPC_RUNTIME_REGISTRATION`.
Adapter contract `StructuredAgentSessionAdapter` = `open`, `supportsCreate/Location`, `acquire` (fenced spawn
per reservation), `releaseAcquisition`, `dispatch` (with fence, abort-before-write semantics, `requestedAt`), stop
(`src/main/native-chat/agent-session-wire/structured-agent-session-adapter.ts@e310a636:L168-200`); a router fans out by
agent id (`structured-agent-session-adapter-router.ts@e310a636:L17-40`).

### 6.2 Lifecycle operations

| Op | PTY agents | Structured sessions | Evidence |
|---|---|---|---|
| Launch | renderer/CLI/mobile → runtime `agentLaunch`/`terminal.*` RPC → daemon `createOrAttach` → node-pty spawn with env (hooks, account homes, PATH repair) → prompt injection | `agentSession.*` RPC (45 methods) → host acquires adapter child → dispatch | `src/main/daemon/pty-subprocess.ts@e310a636:L1-60`; `src/shared/rpc-contract/agent-launch-params.ts`; `structured-agent-session-host.ts` (358 LOC) |
| Attach | daemon sessions re-attached by id; snapshot (`@xterm/headless` serialize) replayed to renderer | journal replay (`replayJournal`) + live subscription | `src/main/daemon/headless-emulator.ts@e310a636:L1-30`; `structured-agent-runtime-registrations.ts@e310a636:L11` |
| Stop | fenced termination protocol (v51+), process-tree kill (Windows via `@vscode/windows-process-tree` + custom kill), descendant-exit verification | adapter stop, `journal-stop-acceptance.ts`, ACP `acp-structured-stop.ts` | `src/main/daemon/daemon-fenced-termination.ts`; `src/main/pty-descendant-termination.ts`; `src/packages/process-host/src/process-tree-termination.ts` |
| Restore after app restart | daemon still alive → adopt endpoint, re-attach live PTYs | journal + session records reopen; provider resume (Claude `--resume`, Codex resume homes) | `src/main/daemon/daemon-endpoint-adoption.ts`; `src/main/codex/codex-session-resume-*.ts`; `src/main/claude/claude-structured-resume-point.ts` |
| Restore after daemon/host crash | **cold restore**: last `checkpoint.json` + `output.log` → scrollback re-seeded; agent re-launched with resume flags ("sleeping agents") | journal is durable (WAL, FULL); pending-submission recovery | `src/main/daemon/cold-restore-payload-cache.ts@e310a636:L1-20`; `journal-pending-submission-recovery.ts`; `src/shared/sleeping-agent-launch-config.ts` |

Known defects in exactly these paths: #14228 (resume after clean exit), #9976/#17741 (lost injected dispatch),
#31926/#9138 (daemon adoption/generations), #18424 (mode restore).

### 6.3 Context delivery and output normalization

* **Context in:** prompt text + briefs injected into TUIs (typed lead line required for Claude paste,
  `pasteNeedsTypedRequest`); orchestration preambles (`src/main/runtime/orchestration/preamble.ts`); skills bundled and
  installed into agent homes (`src/main/skills/**` 14,478 LOC, `skills/`, `skill-guides/`); Design-Mode grabs and diff
  notes appended to prompts (§10, §11); `orca` CLI available inside every terminal (env var `BROWSER` set to
  `orca open-url --url %s`, `src/main/ipc/pty/host-env/assembly.ts@e310a636:L313`).
* **Status out (PTY):** two channels — managed hooks POSTing to a loopback hook server (per-agent installers listed in
  `src/main/agent-hooks/managed-agent-hook-registry.ts`; payload normalizer in `src/shared/agent-hook-listener/**`
  8,453 LOC; headers `x-orca-agent-hook-meta`, `x-orca-pane-key` at
  `src/shared/agent-hook-listener/hook-envelope.ts@e310a636:L50-74`) and **OSC 7501 Program Status Protocol** parsed
  from PTY output with hook precedence rules (`src/main/agent-hooks/README.md@e310a636`, support matrix dated
  2026-10-17; `src/shared/program-status/**` 1,037 LOC).
* **Transcripts:** vendor transcript files are tailed/parsed (Claude JSONL, Codex rollouts, OpenCode SQLite, etc.;
  `src/main/native-chat/transcript-*.ts`, `src/main/ai-vault/**` 21,623 LOC) for history, search and usage.
* **Structured output:** provider frames → `journal-row-schema.ts` rows (355 LOC) → render items; ACP timeline
  translator (`src/main/acp/acp-timeline-translator.ts`); fixtures for replay (`src/main/acp/fixtures/*.jsonl`).

### 6.4 Is there a durable event log / orchestrator?

* **Orchestrator: yes.** `Coordinator` class with phases `decomposing → dispatching → monitoring → merging → done`,
  poll 2 s, default 4 concurrent workers (`src/main/runtime/orchestration/coordinator.ts@e310a636:L30,L36-39`); task
  DAG convergence, decision gates, escalation triage, mailbox pointer delivery into PTYs or structured sessions,
  federation across hosts (`src/main/runtime/orchestration/*`, 25,600 LOC; DB layer 15,059 LOC). CLI surface
  `orca orchestration …` (`src/cli/handlers/orchestration*`).
* **Durability:** `orchestration.db` (v43) with `mutation_receipts` and `mutation_caller_identities` for idempotency,
  `attempt_observation_facts` for outcome projection, crash-recovery tests
  (`src/main/runtime/orchestration-mailbox-crash-recovery.spec.ts`).
* **Not a single authoritative event log.** Truth is split across `profile-state.db`, `agent-session-journal.db`,
  `orchestration.db`, daemon checkpoint files, vendor transcripts and hook-status memory. Journal rows are append-ish
  but carry epochs, repairs, rewinds, set-asides and imports (`journal_repairs`, `journal_set_aside`,
  `journal-context-rewind.ts`) — i.e. mutable history semantics. **INFERRED:** no hash chaining or tamper evidence was
  found (grep for hash-chain/merkle terms not performed exhaustively; treat as UNKNOWN-leaning-absent).

---

## 7. Parallel git worktrees, workspace FS, source control

| Concern | Path(s) | Notes |
|---|---|---|
| Git execution | `src/main/git/command-runner/**` | Shells out to system `git` (and `gh`, `glab`) with WSL-aware spawn, Windows host env, timeouts, subprocess admission, tree-kill (`git-spawn.ts`, `wsl-aware-spawn.ts`, `windows-host-git-environment.ts`) |
| Worktree add | `src/main/git/worktree-add.ts@e310a636:L211-240` | `git worktree add --no-track -b <branch> <path> <base>`; Windows long-path args; pending-removal conflict guard |
| Create pipeline | `src/main/worktree-create-*.ts`, `worktree-root-preparation.ts`, preparation pool/claims/reservations | Pre-prepared worktree pool to cut latency; base prefetch; concurrency control |
| Removal | `src/main/worktree-removal-*.ts`, `worktree-background-removal.ts`, `worktree-trash.ts`, `worktree-removal-home-guard.ts` | Background removal with authority/fencing, home-dir guard, leftover handling, process cleanup |
| Retirement / lineage | `worktree-retirement-*.ts`, `worktree-lineage-*.ts` | Name retirement, lineage pruning across hosts |
| Root `worktree*` files | 4,819 prod LOC (47 files); `src/main/ipc/worktree*` 12,047 LOC (83 files); `src/main/ipc/worktree-remote.ts` 1,755 LOC (largest prod file in `src/main`) | |
| Source control ops | `src/main/git/source-control/*` (status, staging, commit, discard, branch/commit compare & diff, conflicts, submodules) | No merge UI per se; `remote-rebase.ts` (fork-point rebase / `--ff-only`), PR merge via GitHub (`src/main/github/client/merge/merge-pr.ts`, `pr-auto-merge.ts`) |
| Compare | `branch-compare.ts`, `commit-compare.ts`, `compare-ref-oids.ts`, `settled-diff-cache.ts` | "Compare results and merge the winner" per README |
| Folder workspaces | First-class non-git workspaces (`AGENTS.md@e310a636` "Folder Workspaces") | |
| FS watching | `@parcel/watcher` in a separate process entry (`parcel-watcher-process-entry`) | |
| Sparse checkout | `sparse-presets` store slice; `components/sparse` | |
| Gaps | No Jujutsu (#1082), no multi-repo workspaces (#1099/#21118), monorepo worktree file visibility bug (#6357, 25 comments) | |

---

## 8. Terminals

| Concern | Finding | Evidence |
|---|---|---|
| Renderer | xterm.js `6.1.0-beta.304` (patched) + WebGL addon (patched), lazy-loaded, DOM fallback; search, serialize, image, ligatures, unicode11, web-links addons | `package.json`; `src/renderer/src/lib/pane-manager/terminal-webgl-addon-loader.ts@e310a636:L4-31`; `pane-webgl-renderer.ts` |
| Splitting | Custom imperative **pane manager** (tree of splits, divider drag, fit/resize observers, reparenting, focus-follows-mouse, drag-reorder) | `src/renderer/src/lib/pane-manager/**` (13,851 LOC, 125 files; **0 store imports**) |
| Pane UI | `src/renderer/src/components/terminal-pane/**` | 71,192 LOC, 586 files, 150 files import the store |
| PTY backend | `node-pty 1.1.0` (patched) in the **daemon**; ConPTY on Windows with warm-up and reflow viewport handling; pwsh/powershell/cmd/WSL distro selection | `src/main/daemon/pty-subprocess/native-pty-spawn.ts@e310a636:L12`; `daemon-entry.ts@e310a636:L4-5`; `conpty-reflow-viewport.ts` |
| Server-side mirror | `@xterm/headless` + serialize per session → snapshots for attach, mobile, remote, and cold restore | `src/main/daemon/headless-emulator.ts@e310a636:L1-30` |
| Persistence | `checkpoint.json` + `output.log` generations; scrollback "survives restarts" | `daemon-checkpoint-file.ts@e310a636:L5-24`; README |
| Crash / reconnect | Daemon outlives app; endpoint ownership protocol (link/rename, never unlink) to avoid deleting a live successor's socket; degraded fallback to in-process PTYs | `src/main/daemon/AGENTS.md@e310a636`; `daemon-endpoint-ownership.ts`; `degraded-daemon-pty-provider.ts` |
| Remote terminals | Binary terminal stream protocol with negotiated opcodes (e.g. `SetOutputPaused`=16) over runtime RPC / SSH relay | `src/shared/terminal-stream*`; `remote-wire-compatibility.md@b5b727bd` |
| Shell integration | OSC 133 bootstraps (PowerShell incl. CLM), zsh/bash/fish wrappers, shell-ready markers, per-worktree history files | `src/main/powershell-osc133-bootstrap.ts`; `shell-*.ts`; `terminal-history*.ts` |
| Known issues | #7240/#7951 garbled after tab switch; #32242 OSC 10/11 color queries unanswered; #11363 Windows freezes; #16797 daemon exits | §2.3 |

Design lesson worth carrying over (regardless of code reuse): the daemon AGENTS.md documents 23 defects from naive
socket reclamation and the resulting "only the publisher may mutate the endpoint, by proven-dead replacement" rule
(`src/main/daemon/AGENTS.md@e310a636`). Any WePLD terminal fabric with a surviving PTY host needs the same invariant.

---

## 9. File editor, previews, Quick Open, navigation, accessibility

| Concern | Finding | Evidence |
|---|---|---|
| Editor engine | **Monaco** (`monaco-editor ^0.55.1`, patched; `@monaco-editor/react`) | `src/renderer/src/components/editor/MonacoEditor.tsx@e310a636` (325 LOC) |
| Language intelligence | **No LSP client** found; top feature request #961 (41 reactions) | grep `languageclient|language server|lsp` → no editor hit |
| Model URIs | `vscode-remote` scheme for owned models | `src/renderer/src/components/editor/editor-model-uri.ts@e310a636:L5` |
| Diff | `DiffViewer.tsx`, `EditorDiffFileSurface.tsx`, `ImageDiffViewer.tsx`, large-diff fallbacks | `components/editor/*` |
| Previews | Markdown (TipTap + custom preview with TOC, search, annotations), PDF (`PdfViewer.tsx`, `PdfFind.tsx`), images (pan/zoom), notebooks (`src/main/notebook`), CSV, Mermaid; custom protocols `orca-preview`, `orca-media` | `components/editor/*`; `src/shared/doc-preview-scheme.ts@e310a636:L2`; `src/shared/media-file-extensions.ts@e310a636:L16` |
| Quick Open | `src/renderer/src/components/QuickOpen.tsx@e310a636` (286 LOC) with `aria-live` status (L190-277); capped local listing; ripgrep-backed search (`src/main/ripgrep`) | |
| Command palette | `components/cmd-j/**` (3,583 LOC) | |
| Keybindings | `keybindings` slice + `src/main/keybindings` | |
| Accessibility | 3,540 `aria-*` attribute uses in renderer `.tsx`; `config/oxlint-react-doctor.json` lint; IME regression work (`terminal-ime-e2e.yml`) | grep count |
| Size / coupling | `components/editor/**` 62,477 LOC (538 files), 95 files import the store | |

---

## 10. Embedded browser, Design Mode, automation, computer use

| Concern | Finding | Evidence |
|---|---|---|
| Browser engine | Electron `WebContentsView` guests managed by main (`webviewTag:false`); CDP via `webContents.debugger` (`attach('1.3')`, `Emulation.*`, `Runtime.evaluate`) | `src/main/browser/browser-manager-types.ts@e310a636:L99`; `browser-guest-devtools-dock.ts@e310a636:L178`; `browser-manager-viewport.ts@e310a636:L209-232` |
| Size | `src/main/browser/**` 44,849 LOC (371 files; **110 import `electron`**); renderer `browser-pane/**` 29,910 LOC (54 store-importing) | |
| Profiles / cookies | Per-tab profiles; **imports cookies from installed Chrome/Firefox profiles** (reads `cookies.sqlite`/Chromium stores) | `src/main/browser/cookies/**`; `browser-cookie-firefox-import.ts@e310a636:L24` |
| Design Mode ("grab") | Injected guest scripts (overlay, element context, React fiber info, selection) → payload with page + target HTML/CSS + cropped screenshot, revalidated/clamped in main (secret-pattern scrubbing, safe attributes, URL protocol allowlist) → attached to agent prompt | `src/main/browser/grab-guest-*.ts` (7 files, 1,000 LOC); `browser-grab-payload.ts@e310a636:L1-40`; `browser-grab-screenshot.ts`; `browser-grab-session-controller.ts`; `src/main/ipc/browser-grab-ipc.ts`; docs `docs/site/content/docs/browser/design-mode.mdx` |
| Automation API | 91 `browser.*` RPC methods — 67 top-level commands plus sub-namespaces such as `browser.capture.*`, `browser.cookie.*`, `browser.clientHost.*` (goto, click, fill, type, snapshot, screenshot, fullScreenshot, pdf, network, console, eval, cookies/profiles, viewport/device/geolocation/offline, tabs, dialogs, upload/download, drag, mouse primitives, screencast…) exposed via `orca browser …` CLI to agents | `src/shared/rpc-contract/rpc-params-catalog.generated.ts@e310a636`; `src/cli/handlers/browser-*.ts` |
| agent-browser bridge | Bridges Vercel `agent-browser` command model onto Orca's in-app guests | `src/main/browser/agent-browser-bridge-*.ts` (27 files, 3,392 LOC) |
| Computer use | 15 `computer.*` commands (listApps/Windows, getAppState, click, drag, scroll, typeText, pressKey, hotkey, setValue, pasteText, permissions); sidecar process; native backends: macOS Swift (6,889 LOC), Windows PowerShell `runtime.ps1`, Linux Python | `src/main/computer/**` (4,129 LOC); `native/computer-use-{macos,windows,linux}`; `computer-e2e.yml` |
| Mobile emulator pane | Android emulator integration | `src/main/emulator/**` (4,695), `components/emulator-pane` |

---

## 11. Review, diff annotation, trackers, SSH, ports

| Concern | Finding | Evidence |
|---|---|---|
| Diff annotation | Monaco view-zone comment cards, range drag, draft cards, "send notes" to agent; persisted per worktree | `src/renderer/src/components/diff-comments/**` (2,624 LOC, 16 files, only 2 store-importing); `store/slices/diffComments.ts`, `diff-comment-persistence.ts`; `components/editor/DiffNotesSendMenu.tsx` |
| Markdown review | Annotation composer/overlay on Markdown preview & Monaco | `MarkdownPreviewAnnotationComposer.tsx`, `MonacoMarkdownAnnotationOverlay.tsx` |
| Hosted review / PRs | PR page, checks, hosted-review cache, PR generation, commit-message generation | `components/pull-request-page/**` (7,697), `store/slices/hosted-review*.ts`, `pull-request-generation*.ts` |
| GitHub | Via **`gh` CLI** (no Octokit dep): lookup/check/list/update/fetch/create/merge/project views; rate-limit breaker; account-bound env | `src/main/github/**` (19,936 LOC); `src/main/git/command-runner/gh-*.ts`; 52 `github.*` RPC methods |
| Linear | `@linear/sdk ^97`; issues, comments, relations, save; also a "linear-mcp" CLI spec | `src/main/linear/**` (6,783 LOC; only 9 outside-dir imports); `src/cli/specs/linear-mcp.ts`; 43 `linear.*` RPC |
| Others | GitLab (`glab`), Jira (incl. image protocol `orca-jira-image`), Bitbucket, Azure DevOps, Gitea | `src/main/{gitlab,jira,bitbucket,azure-devops,gitea}`; `src/shared/jira/jira-attachment-image.ts@e310a636:L1` |
| SSH remote worktrees | `ssh2`-based connections with reconnect, a JSON-RPC **channel multiplexer** with keepalive/cancellation, remote exec frame protocol, "managed server" install of `orcad` on the remote, legacy relay path still fenced by a ratchet; PTY leases for SSH | `src/main/ssh/**` (30,833 LOC); `ssh-channel-multiplexer.ts@e310a636:L1-25` (630 LOC); `ssh/connection/ssh-connection.ts` (896); `src/main/managed-server/**` (14,443); `persistence/leasing-ssh-ptys/*`; CI `ssh-hostile-hosts.yml`, `ssh-windows-hosts.yml` |
| WSL | Deep WSL support (distro holder, UNC delete safety, `wsl-guest` helper build) | `src/main/wsl/**` (8,351), `src/wsl-guest/**` |
| Port forwarding | Listener discovery (netstat/lsof/Windows), advertised-URL parsing from terminal output, SSH enrichment, workspace port ownership | `src/main/ports/**` (2,894 LOC, 21 files); `workspacePorts.*` RPC |
| Ephemeral VMs | `vm` CLI spec, `src/main/ephemeral-vm`, Multipass recipes plugin | `src/cli/specs/vm.ts`; `resources/plugins/launch/stablyai.orca-multipass-recipes` |

---

## 12. Mobile companion, remote bridge, auth, sync, notifications, data security

### 12.1 Components

| Component | Finding | Evidence |
|---|---|---|
| Mobile app | Expo 55 / React Native 0.83, `orca-mobile`, bundle/package `com.stably.orca.mobile`, scheme `orca`; xterm in-app; tweetnacl E2EE; `expo-notifications` | `mobile/package.json@e310a636`; `mobile/app.json@e310a636:L18,L77`; `mobile/src/**` 180,911 LOC |
| Pairing | QR/link "pairing offer" v2: direct `ws://<lan>:6768` endpoint + device token + host X25519 public key; optional relay block (director URL, cell URL, assignment epoch, relay host id, invite token, 5-min expiry, `e2eeFraming: 2`) | `src/shared/mobile-relay-pairing-fixtures.ts@e310a636:L12-40`; `src/shared/pairing*` |
| E2EE | NaCl `box` (X25519 + XSalsa20-Poly1305) via `tweetnacl`, 4 MiB plaintext cap; v2 session framing; handshake timeout 10 s; 5 consecutive decrypt failures close; per-device key auth | `src/shared/e2ee-crypto.ts@e310a636:L1-30`; `src/main/runtime/rpc/e2ee-channel.ts@e310a636:L1-40`; `mobile-e2ee-*.ts` |
| Relay | Stably-operated: phones and desktops each dial out to a relay **cell**; a **director** assigns hosts to cells and coordinates migrations; relay splices frames (sees ciphertext only — INFERRED from E2EE design). Hono + ws + jose + pg; Postgres prod / SQLite tests; security review 2026-10-21 | `cloud/README.md@e310a636`; `cloud/apps/relay/**` (32,196 LOC); `cloud/packages/relay-contract`; `cloud/docs/relay-security-2026-10-21.md` |
| Push | Separate Cloud Run gateway holding APNs key, FCM via service account; host authenticates with its X25519 key via encrypted challenge → 24 h session; per-host quotas; one persisted event per notification; ops in **private** `stablyai/orca-cloud` | `cloud/README.md@e310a636`; `cloud/apps/push/**` (2,305 LOC) |
| Cloud auth | OAuth/OIDC against `https://login.onorca.dev`, client id `orca-desktop`, scope `openid profile email offline_access`; relay director `https://relay.onorca.dev` | `src/main/orca-profiles/profile-cloud-auth-config.ts@e310a636:L24-27` |
| Other hosted endpoints | Artifact/skill sharing `https://share.onorca.dev`; feedback `https://www.onorca.dev/v1/feedback`; `app.orca.dev` share host | `src/main/artifacts/artifact-cloud-config.ts@e310a636:L3`; `src/shared/skill-share-link.ts@e310a636:L2`; `src/main/ipc/feedback.ts@e310a636:L213` |
| Slack connector | Experimental `cloud/apps/connector` with short-lived connector tokens | `cloud/README.md@e310a636` |
| Remote Orca Servers | Desktop-to-desktop over Tailscale/LAN, beta; or `orca serve` headless; accounts registered on server via `orca account add` | `docs/site/content/docs/remote-servers.mdx@e310a636` |
| Desktop notifications | Small module (364 LOC) with announced-notification registry; categories are authoritative for mobile push | `src/main/notifications/**`; `cloud/README.md` |
| Telemetry | PostHog (`https://us.i.posthog.com`) with consent/opt-out; crashpad minidumps captured locally, **no upload** (`uploadToServer:false`) | `src/main/telemetry/posthog-transport.ts@e310a636:L73-84`; `src/main/crash-reporting/crashpad-capture.ts@e310a636:L51-53` |

### 12.2 Data-security observations (INFERRED unless cited)

* Local RPC requires a token file next to the daemon socket (`getDaemonTokenPath`,
  `daemon-spawner.ts@e310a636:L134-136`); SQLite files are chmod 0600; secrets via `safeStorage`.
* Browser cookie import from the user's real browsers (§10) is a high-sensitivity capability; any port must keep it
  opt-in and audited.
* `x-orca-*` hook HTTP endpoint is loopback; hook installers write into third-party agent config files (Claude/Codex
  settings, TOML ownership markers — `src/main/agent-hooks/managed-toml-ownership.ts`), a cross-tool side effect.
* Remote servers documented as "keep on a private network path you control" (beta) — no claim of hardened public
  exposure (`remote-servers.mdx@e310a636`).
* No evidence of a policy decision point (allow/deny of agent effects); permission handling is relayed from providers
  (`src/main/acp/acp-permission-requests.ts`, `claude-permission-presentation.ts`) — same class of gap R02 found in T3.

### 12.3 Sync model

There is no CRDT/multi-master sync. The runtime (desktop or `orcad`) is the single authority; clients (renderer, web,
mobile, remote desktop) are views over RPC with capability negotiation (`src/shared/protocol-version.ts@e310a636`).
Mirrored editor tabs across peers exist and have identity bugs (#10859).

### 12.4 Remote wire compatibility (from deleted `docs/reference/remote-wire-compatibility.md@b5b727bd`)

Rules recorded at the old pin: (1) new optional JSON fields are safe only while every reader treats them as optional;
(2) new terminal-stream opcodes are silently dropped by old peers and must be negotiated in `Subscribe` capabilities
(pattern: `SetOutputPaused`=16; opcode numbers never reused, e.g. `Ack=13`, `ClaimViewport=14`); (3) changing *what*
the host publishes is a wire change even with identical frames (PR #12641 example); (4) enum arm sets are wire
surfaces — use `openEnum` in `src/shared/zod-salvage.ts`, never `.catch()`. Enforcement: cross-version tests run the
current tree against the newest release tag in both skew directions
(`tests/e2e/cross-version-wire/cross-version-terminal-wire.unit.test.ts`, still present at HEAD among 69 files).
These rules are directly reusable as WePLD protocol-evolution policy.

---

## 13. Tests, benchmarks, fixtures, CI, cross-platform builds, update mechanism

| Item | Finding | Evidence |
|---|---|---|
| Unit/integration tests | 14,272 `*.test.ts(x)` files under git; vitest 5.0.5 (patched); sharded across Node versions | `git ls-files`; `.github/workflows/unit-tests.yml@e310a636:L70-152` |
| E2E | Playwright (`@playwright/test`, `@stablyai/playwright-test`); `tests/e2e` 729 test/spec files excl. helpers; golden e2e on ubuntu/macos-15/windows-2022 | `.github/workflows/release-cut.yml@e310a636:L706-722`; `tests/e2e/AGENTS.md` |
| Cross-version wire tests | 69 files | `tests/e2e/cross-version-wire/` |
| Reliability gates | Registry with maturity levels (experimental→soak→blocking; ≥100 soak runs, ≥14 days, 0 unexplained flakes) and per-platform/provider coverage notes | `config/reliability-gates.jsonc@e310a636:L1-30` |
| Fixtures | ACP JSONL scenario fixtures (`src/main/acp/fixtures/*`), agent transcript fixtures, PTY transcript capture tooling (`capture:agent-transcript`), component fixtures + screenshotter (`fixtures:shot`) | paths cited |
| Benchmarks | §4.2 | |
| CI | **70 workflow files**, runners: Blacksmith Ubuntu x64/arm64, `windows-2022`, `macos-15`; Windows-specific suites: `win-update-e2e`, `win-update-survival-e2e`, `win-crash-survival-e2e`, `win-orcad-serve-switch-e2e`, `ssh-windows-hosts`, `dev-channel-win-*` | `.github/workflows/@e310a636`; `pr.yml@e310a636:L26-1526` |
| Static analysis | oxlint (several configs incl. type-aware, anti-slop plugin), ast-grep gates, knip dead code, react-doctor, dependency-security check | `package.json` scripts |
| Cross-platform builds | mac x64/arm64 (dmg+zip, notarization/ShipIt scheduling helper), Windows x64 NSIS (SignPath), Linux AppImage/deb/rpm x64+arm64; Homebrew bump workflow | §1.1; `config/electron-builder.config.cjs@e310a636` |
| Update mechanism | `electron-updater` with **`generic` feeds selected at runtime** (stable / prerelease / dev channel), GitHub releases as backing store (`https://github.com/stablyai/orca/releases/latest`, `api.github.com/repos/<repo>/releases`), mac quit guard, install-exit watchdog, Linux package recovery, daemon-preserving restarts | `src/main/updater/updater-release-feed.ts@e310a636:L160`; `src/main/updater/updater-build-selection.ts@e310a636:L69,L155`; `src/main/updater-prerelease-feed.ts@e310a636:L220`; `src/main/updater-release-builds.ts@e310a636:L22`; `config/dev-app-update.yml@e310a636` |
| Update-related bugs | #9138, #13171, #20007, #23372, #15956 | §2.3 |

---

## 14. Module extractability matrix

Coupling heuristics (measured over non-test `.ts/.tsx` in each module): **E** = files importing `electron`;
**S** = files importing the renderer store (`useAppStore`/`@/store`); **O** = distinct first-level directories reached
via `../` relative imports (rough fan-out; `@/` aliases not counted).

| # | Orca module | Path | Prod LOC (files) | Key deps | E / S / O | Extractable? | Notes |
|---|---|---|---|---|---|---|---|
| 1 | Process host (spawn, cancel, tree-kill, Windows cmd-line quoting, cmd-shim resolution, lsof probe) | `src/packages/process-host/src` | 1,896 (20) | Node only (`proper-lockfile` dev) | 0/0/0 | **High — already a workspace package** (`@orca/process-host`) | Best "drop-in" asset; Windows tree-kill logic is hard-won |
| 2 | TUI agent catalog | `src/shared/tui-agent-config*.ts` | 443 (2) | types only | 0/0/low | **High** (data) | Needs ongoing curation as CLIs change |
| 3 | Pane manager (split tree, fit, drag, WebGL attach) | `src/renderer/src/lib/pane-manager` | 13,851 (125) | `@xterm/*` | 0/0/5 | **Medium-High** | Imperative DOM; port into WePLD terminal view |
| 4 | Design-Mode guest scripts + payload clamp | `src/main/browser/grab-*.ts`, `browser-grab-payload.ts`, `src/shared/browser-grab-types` | ~1,100 (8) | none (injected JS) + Electron for capture | low | **High (scripts)** / Medium (capture host) | Highest value-per-LOC UX asset |
| 5 | Diff comments | `src/renderer/src/components/diff-comments` | 2,624 (16) | Monaco | 0/2/2 | **High** | Requires Monaco; T3 has its own annotations (R02 §12) |
| 6 | Hook listener normalizer + OSC 7501 | `src/shared/agent-hook-listener`, `src/shared/program-status` | 9,490 (84) | none heavy | 0/0/med | **Medium-High** | Installers (`src/main/agent-hooks`, 13,874 LOC, O=45) are more coupled |
| 7 | Linear client | `src/main/linear` | 6,783 (46) | `@linear/sdk` | 0/0/9 | **High** | T3 has no Linear integration (grep `@linear/sdk|api.linear.app` → 0 hits at `t3:@36d4d711`) |
| 8 | ACP client + dialects | `src/main/acp` | 11,461 (76) | generated ACP types | 0/0/18 | Medium | T3 already has `packages/effect-acp`, `provider-acp` (R02) — low marginal value |
| 9 | Agent-session journal | `src/main/native-chat/agent-session-journal` | 9,211 (85) | `node:sqlite` | 0/0/14 | Medium | Conflicts with T3's event store; reference only |
| 10 | Orchestration (coordinator, mailboxes, DAG, gates) | `src/main/runtime/orchestration` | 25,600 (211) | `node:sqlite` | 0/0/61 | **Low** | Deeply tied to Orca sessions/terminals/federation |
| 11 | Terminal daemon | `src/main/daemon` | 36,310 (311) | node-pty, `@xterm/headless` | 1/0/53 | **Low-Medium** | Port the *design* (endpoint ownership, checkpoints, adoption), not the code |
| 12 | Terminal pane UI | `src/renderer/src/components/terminal-pane` | 71,192 (586) | xterm | 0/150/81 | **Low** | Store-bound |
| 13 | Editor (Monaco + previews) | `src/renderer/src/components/editor` | 62,477 (538) | Monaco, TipTap, pdf | 0/95/32 | **Low-Medium** | Individual viewers (PDF/Markdown preview) liftable with effort |
| 14 | Browser manager (main) | `src/main/browser` | 44,849 (371) | Electron, CDP | 110/0/28 | Medium (Electron-bound) | Requires Electron host; T3 desktop is Electron (R02) |
| 15 | Browser pane UI | `src/renderer/src/components/browser-pane` | 29,910 (247) | — | 0/54/24 | Low | |
| 16 | Computer use | `src/main/computer` + `native/computer-use-*` | 4,129 (34) + 6,889 Swift + PS/Py | OS APIs | 0/0/3 | **Medium-High** | Sidecar boundary already exists |
| 17 | Git worktree lifecycle | `src/main/git` + `src/main/worktree*` + `src/main/ipc/worktree*` | 16,628 + 4,819 + 12,047 | system git | 0/0/36 | Medium | Safety logic (removal fencing, home guard) valuable as reference |
| 18 | SSH remote | `src/main/ssh` + `src/main/managed-server` | 30,833 + 14,443 | `ssh2` | 1/0/62 | **Low** | Tied to orcad install + runtime protocol |
| 19 | GitHub via `gh` | `src/main/github` | 19,936 (148) | `gh` CLI | 1/0/27 | Medium | T3 has 7 forge packages (R02) |
| 20 | Runtime RPC + orcad | `src/main/runtime/rpc`, `src/main/orcad` | 42,008 + 11,143 | ws, tweetnacl | 0/0/high | Low (as code) / **usable as a process** | Basis of Option C |
| 21 | Mobile app | `mobile/` | 195,735 (1,855) | Expo/RN | n/a | Low | Bound to Orca runtime protocol + Stably relay |
| 22 | Cloud relay + push | `cloud/apps/{relay,push}` | 32,196 + 2,305 | Hono, pg, jose | n/a | Medium (separate deployables) | Requires re-hosting + new APNs/FCM identities |
| 23 | Profile-state persistence | `src/main/persistence` | 39,461 (307) | `node:sqlite` | low | Low | Pattern (writer worker, backups, quarantine) reusable as reference |

---

## 15. Rebranding risk register (if any Orca code ships under WePLD identity)

| Surface | Orca value | Location | Risk if missed |
|---|---|---|---|
| npm package / bins | `"name": "orca"`, bins `orca`, `orca-dev` | `package.json@e310a636:L2-13` | CLI collision with installed Orca |
| App ID / macOS bundle id | `com.stablyai.orca` | `config/electron-builder.config.cjs@e310a636:L105,L238` | Keychain/TCC/notification identity collision |
| Product / executables | `Orca`, `Orca.exe`, Linux `orca-ide`, artifacts `orca-windows-setup.exe`, `orca-macos-*.dmg`, `orca-ide_*.deb` | `electron-builder.config.cjs@e310a636:L239,L510,L553,L643-712` | Installer/uninstaller collision |
| Windows AppUserModelID (toast identity, taskbar grouping) | `com.stablyai.orca` (dev: per-worktree derived) | `src/main/startup/dev-instance-identity.ts@e310a636:L6`; `main-process-ready-foundation.ts@e310a636:L102-104` | Toasts attributed to Orca / grouped with it |
| Protocol handler | `orca://` (`protocols: [{ name: 'Orca', schemes: ['orca'] }]`); `open-url` handler | `electron-builder.config.cjs@e310a636:L240`; `src/main/index.ts@e310a636:L116` | Deep links hijacked by/for Orca |
| Custom Electron schemes | `orca-preview`, `orca-media`, `orca-jira-image` | `src/shared/doc-preview-scheme.ts@e310a636:L2`; `media-file-extensions.ts@e310a636:L16`; `jira/jira-attachment-image.ts@e310a636:L1` | Cosmetic; must stay consistent with CSP |
| Mobile URL scheme / bundle | scheme `orca`, `com.stably.orca.mobile` | `mobile/app.json@e310a636:L18,L77` | Store rejection / link collision |
| Update feed | GitHub `stablyai/orca` (publish draft releases), runtime generic feeds, hard-coded `github.com/stablyai/orca/releases/latest`; `updaterCacheDirName: orca-updater` | `electron-builder.config.cjs@e310a636:L733-738`; `updater-prerelease-feed.ts@e310a636:L220`; `config/dev-app-update.yml` | **Silent cross-update to Orca binaries** (critical) |
| Code signing | SignPath publisherName "SignPath Foundation"; mac notarization identity | `electron-builder.config.cjs@e310a636:L511-516` | Update signature verification failures |
| Data dir | Electron `userData` derived from app name `Orca` (e.g. `%APPDATA%\Orca` — INFERRED Electron default); files `orca-data.json`, `orca-github-cache.json`, `profile-state.db`, `agent-session-journal.db`, `orchestration.db`, `ai-vault/session-search.sqlite` | `user-data-path.ts@e310a636:L13-29`; §5.1 | Reading/corrupting a co-installed Orca profile |
| Home dir | `~/.orca/` (agent-hooks scripts, locks, encrypted API keys, bitbucket creds) | `src/main/agent-hooks/installer-utils.ts@e310a636:L113`; `credentials/encrypted-api-key-file-store.ts@e310a636:L43` | Hook scripts shared/overwritten between products |
| Agent hook identity | HTTP headers `x-orca-agent-hook-meta`, `x-orca-pane-key`; hook entries written into Claude/Codex/etc. configs | `hook-envelope.ts@e310a636:L50-74`; `managed-toml-ownership.ts` | Two products fighting over the same user's `~/.claude`/`~/.codex` hook config |
| Daemon endpoints | `\\?\pipe\orca-terminal-host-v52-<hash>`, `daemon-v52.sock/.token/.pid` | `daemon-spawner.ts@e310a636:L121-140` | Cross-product daemon adoption |
| IPC channels | ≥392 literal `ipcMain.handle` names (`pty:*`, `gh:*`, …) | `src/main/ipc/**` | Internal only (low external risk, high rename effort) |
| RPC namespace | 778 methods; runtime protocol v3 | `rpc-params-catalog.generated.ts`; `protocol-version.ts@e310a636:L41` | Clients of either product pairing with the other |
| Env vars | 583 distinct `ORCA_*` names | grep | Leaks into agent environments; collisions |
| Cloud endpoints | `login.onorca.dev` (client `orca-desktop`), `relay.onorca.dev`, `relay-c1.onorca.dev` (cell host, seen in `src/shared/mobile-relay-pairing-fixtures.ts@e310a636:L22`), `share.onorca.dev`, `app.orca.dev`, `www.onorca.dev/v1/feedback`, PostHog host `us.i.posthog.com` (write-key source UNKNOWN; passed into `createPostHogClient`) | `profile-cloud-auth-config.ts@e310a636:L24-27`; `artifact-cloud-config.ts@e310a636:L3`; `skill-share-link.ts@e310a636:L2`; `feedback.ts@e310a636:L213`; `posthog-transport.ts@e310a636:L73-75` | **Data sent to Stably's services** under WePLD branding (critical, privacy) |
| Bundled plugins / skills | `resources/plugins/launch/stablyai.*`, skill names, `.claude-plugin` visuals | `resources/**` | Brand leakage in agent homes |
| Docs links | `www.onorca.dev/docs/*` hard-coded in UI (feature wall etc.) | `src/shared/feature-wall-tiles.ts@e310a636:L115` | Cosmetic / support confusion |
| Brand word density | 8,127 `\borca\b` occurrences across 4,375 prod `src` files | grep | Rename effort; ESTIMATE 3–6 pw for full rename + re-test |

---

## 16. Decision-oriented comparison vs T3 Code and options A–D

### 16.1 Side-by-side (Orca = this report; T3 = skim + R02)

| Dimension | Orca @e310a636 | T3 Code @36d4d711 (skim / R02) |
|---|---|---|
| License | MIT (Lovecast Inc.) | MIT (T3 Tools Inc.) (`t3:LICENSE@36d4d711`) |
| Stars / open issues+PRs | 107,791 / 7,956 (issues 4,194 + PRs 3,762) | 30,729 / 3,679 (gh `open_issues_count`) |
| Prod LOC (approx.) | ~2.37 M (src + mobile + cloud) | ~0.97–1.0 M |
| Churn | ~150 commits/day; 1,622 commits in wk of 10-18 | 1,429 commits in wk of 10-18 (R02) |
| Shape | Electron-first app; runtime embedded in main; optional headless `orcad`; web client projected from renderer | Server-first (`apps/server`, Effect) + web client + Electron wrapper + mobile (`t3:apps/*`) |
| Orchestration core | Coordinator + mailboxes + DAG in `orchestration.db` (v43) + separate journal + profile DB | Event-sourced `orchestration-v2` (EventStore, CommandReceiptStore, EffectOutbox/EffectWorker, projections) in one SQLite (`t3:apps/server/src/orchestration-v2/*`; R02 §3) |
| Agent model | ~45 TUI CLIs via PTY + structured Claude/Codex/ACP/Pi | Structured providers only (Claude, Codex, Cursor, Grok, OpenCode, Antigravity, Pi, Muse via `packages/provider-*`) |
| Terminal | xterm.js 6 + WebGL, splits, daemon-hosted surviving PTYs | node-pty server-owned, libghostty-vt WASM renderer (R02 §12) |
| Editor | Monaco + rich previews; no LSP | Light `@pierre/diffs` editor; no Monaco/LSP (R02 §12) |
| Browser / Design Mode | Embedded Chromium + Design Mode + 91 automation RPC methods + computer use | Electron webviews + playwright-core preview automation; no Design Mode/canvas (R02 §12; no element-picker found) |
| Trackers | GitHub, GitLab, Bitbucket, Azure DevOps, Gitea, Jira, Linear | 7 forge packages; no Linear found |
| Remote / mobile | SSH worktrees, `orca serve`, mobile via Stably relay (E2EE) | Remote server, mobile, T3 Connect/Clerk (R02 §5) |
| Windows | Supported, 421 open `os:Windows` issues | Supported; no Windows background service (R02 §7) |
| Policy/PDP | None (provider-relayed permissions) | None (R02 finding 3) |

### 16.2 Options

#### (A) T3 foundation + selected Orca modules — **RECOMMENDED**

* **Why:** T3's server-first, event-sourced core is the better substrate for WePLD's Rust trusted-core seams (R02 §10);
  it is ~2.4× smaller; its gaps (IDE editor, Design Mode, rich browser automation, TUI-agent breadth, Linear) are
  exactly where Orca's most *separable* assets are.
* **Harvest list (port into WePLD-owned packages, keep MIT notices):** process-host (#1), TUI agent catalog (#2),
  pane-manager (#3) only if WePLD replaces T3's libghostty renderer with xterm (otherwise skip), Design-Mode guest
  scripts + payload clamp (#4), hook-listener + OSC 7501 (#6), Linear (#7), computer-use sidecar + native helpers (#16),
  selected Monaco viewers/diff-comments (#5, #13) if WePLD adopts Monaco. Use daemon (#11), worktree-removal safety
  (#17), wire-compatibility rules (§12.4) and persistence recovery (#23) as **reference specifications**.
* **Risks:** T3's own Windows/storage debt (R02 §13); mismatch between Orca's Electron-main browser code and T3's
  web/server split (browser manager must live in T3's desktop process); Monaco adds weight to T3's web bundle.

#### (B) Orca foundation + selected T3 orchestration modules — **NOT RECOMMENDED**

* Orca already has three overlapping durable stores; adding T3's event store makes a fourth unless Orca's are ripped
  out — touching the ~2.1 M-LOC app's most coupled code (store: 50 slices; runtime: 196 k LOC; 778 RPC methods).
* Rebrand + cloud re-host is large (§15): relay, push (APNs/FCM identities), login, share must be re-implemented or
  removed; update feed must be rewired safely.
* Upstream cannot be tracked (~150 commits/day); a fork immediately diverges while inheriting 4,194 open issues,
  incl. 421 Windows-labelled — poor fit for a Windows-first founder.
* ESTIMATE: rebrand + cloud strip/re-host + Windows stabilization to "own-able" state **≥ 30–60 pw**, before any
  WePLD-specific trust work, with ongoing ≥ 1 FTE fork maintenance (INFERRED).

#### (C) One shell + process-isolated adapter to the other — **bridge only**

* Feasible direction: WePLD/T3 shell ⇄ **Orca `orcad`** (headless, WebSocket RPC, capability-negotiated, protocol v3)
  as a sidecar providing Orca-only capabilities (browser automation, computer use, TUI-agent PTYs).
* Pros: no code entanglement; Orca's own cross-version discipline (§12.4) makes the RPC comparatively stable.
* Cons: two runtimes, two persistence stores, two notions of session/worktree identity; orcad brings its own daemon,
  hooks into `~/.claude`/`~/.codex`, Stably cloud endpoints and telemetry (must be disabled); 778-method surface is not
  a public API (no stability promise; RPC catalog regenerated per release); doubles memory on Windows where Orca
  already struggles (#29899, #7175).
* ESTIMATE: thin bridge for 1–2 capabilities (e.g. Design Mode + browser automation) **6–10 pw**, plus recurring
  break/fix per upstream release.

#### (D) Alternative modular platform — **viable fallback; partially converges with A**

* Build WePLD's own shell around the Rust trusted core and a small orchestration kernel, copying patterns from both
  donors (T3's outbox/receipts; Orca's daemon endpoint ownership, wire rules, TUI catalog, Design Mode).
* Highest control and cleanest trust story, but the largest build: ESTIMATE **60–120 pw** to reach feature parity with
  either donor in the areas WePLD needs (terminals + agents + editor + browser + worktrees + review).
* Choose D only if R02's T3 fork proves unworkable (e.g. Effect/orchestration complexity blocks the Rust seams).

### 16.3 ESTIMATE — Orca harvest effort on top of a T3 fork (Option A)

| Item | ESTIMATE (pw) | Basis |
|---|---|---|
| process-host integration (spawn/kill on Windows) | 1–2 | already a package (1,896 LOC) |
| TUI agent catalog + prompt-injection/readiness engine (subset: Claude, Codex, Gemini, Aider, Goose) | 3–6 | catalog 443 LOC, but readiness/injection logic spans daemon + runtime |
| Design Mode (guest scripts, capture/crop, payload → composer) | 3–6 | ~1.1 k LOC scripts + Electron capture glue in T3 desktop |
| Browser automation command subset (~20 of 67 top-level) on T3 desktop | 4–8 | CDP via `webContents.debugger`; 44.8 k LOC donor is mostly breadth |
| Hook listener + OSC 7501 status for PTY agents | 3–5 | 9.5 k LOC shared normalizer |
| Linear integration | 2–4 | 6.8 k LOC, low coupling |
| Computer-use sidecar (Windows first) | 3–6 | PS runtime + TS sidecar; mac Swift later |
| Monaco editor surface + diff comments (if adopted) | 4–8 | must rebind from Orca store to T3 state |
| Terminal daemon *design* applied to T3 terminal (surviving PTYs, endpoint ownership, checkpoints) | 4–10 | reference-only reimplementation |
| Attribution/NOTICE, license review (Claude SDK terms, Apache-2.0 deps) | 0.5–1 | §1.3 |
| **Total** | **~28–56** (core subset ~20–40) | ranges overlap with R02's 22–38 pw T3 MVP; not additive in full |

---

## 17. Recommendation

1. **Do not adopt Orca as the foundation.** Pin `e310a63624c86c0e91e9d77df71f038b91d79ea0` in the WePLD source
   registry as the Orca reference SHA (superseding `b5b727bd`, 5,577 commits stale).
2. **Adopt Option A** consistent with R02: hard-fork T3 as shell + orchestration runtime; harvest the Orca items in
   §16.2(A) as **ports into WePLD-owned packages** with MIT attribution, re-pinned and never auto-synced.
3. **Prioritize** (value ÷ effort): Design Mode → TUI agent catalog + hook/OSC 7501 status → process-host (Windows
   tree-kill) → Linear → computer use → Monaco/diff-comments (only if WePLD commits to Monaco).
4. **Adopt as written policy** (no code): Orca's remote-wire compatibility rules (§12.4), daemon endpoint-ownership
   invariants (§8), and reliability-gate maturity model (`config/reliability-gates.jsonc`).
5. **Never ship** Orca's cloud endpoints, PostHog host/write key, update feeds, `~/.orca` paths, `com.stablyai.orca` identity,
   or `orca://` scheme in WePLD builds; add a CI grep gate for `onorca.dev|stablyai|com.stably|ORCA_` in WePLD sources.
6. **Treat Option C** (`orcad` sidecar) only as a time-boxed experiment if a specific Orca capability is needed before
   its port lands.

---

## 18. Unknowns and limitations

| Item | Status |
|---|---|
| Runtime behaviour, actual performance, memory per session | UNKNOWN — nothing was built or run (planning-only constraint) |
| Exact count of IPC channels (non-literal registrations) | UNKNOWN — 392 is a lower bound (literal `ipcMain.handle('…'` only) |
| Hash-chained / tamper-evident logs | UNKNOWN-leaning-absent (no evidence found in schemas read) |
| `@anthropic-ai/claude-agent-sdk` license text | UNKNOWN in detail (npm says "SEE LICENSE IN README.md"); review before any port that imports it |
| `ssh2` license via npm metadata | Empty field from `npm view`; MIT per upstream (not re-verified this pass) |
| Electron `userData` exact path on each OS | INFERRED from Electron defaults + `app.setName('Orca')`; not executed |
| Whether the relay can read plaintext | INFERRED no (NaCl box E2EE between host and phone); relay code not audited line-by-line |
| Private `stablyai/orca-cloud` deployment specifics | UNKNOWN (private repo) |
| Orca Windows arm64 support | No arm64 Windows installer in v1.4.242 assets; source-level support UNKNOWN |
| Coupling metric precision | Heuristic (first-level `../` targets; `@/` aliases excluded) |
| T3 facts | Skim only; R02 is authoritative for T3 |

---

## 19. Reproduction notes (commands used; all read-only)

```bash
git clone --depth 1 https://github.com/stablyai/orca _work/src/orca     # HEAD e310a636…
git -C _work/src/orca submodule status                                  # empty
gh api repos/stablyai/orca --jq '{stars:.stargazers_count,forks:.forks_count,open_issues:.open_issues_count}'
gh api repos/stablyai/orca/compare/b5b727bd…...e310a636… --jq '{status,ahead_by,behind_by}'
gh api repos/stablyai/orca/compare/v1.4.242...e310a636… --jq '{status,ahead_by,behind_by}'
gh api repos/stablyai/orca/stats/commit_activity
gh api -X GET search/issues -f q='repo:stablyai/orca label:"os:Windows" is:open is:issue' --jq .total_count
gh api "repos/stablyai/orca/contents/docs/reference/remote-wire-compatibility.md?ref=b5b727bd…"
git ls-files -z | grep -zE '\.(ts|tsx|…)$' | xargs -0 wc -l > loc.txt    # LOC table
git grep -n "<pattern>" -- 'src/*.ts' ':!*.test.ts'                     # all code searches
npm view <pkg> license                                                  # registry metadata only, no install
```
