# 14 — Task Catalog (dependency-ordered, implementation-ready)

```text
STATUS = PROPOSED. No task is authorized until the package is accepted and the task's phase entry gate passes.
FORMAT = | ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est pw | Tier | Reqs |
TIER = T0 docs · T1 UI/product without effect/CI/supply-chain/authority change · T2 everything else (see 08)
TESTS = det = deterministic unit/contract/integration · e2e = Playwright/desktop end-to-end · neg = negative oracle
        (must FAIL with Core disabled — mutation control, 09) · bench = 09 benchmark ids · R/W = recovery suites (09 §2)
SOURCE_REFS = R11 = research/R11_T3_FILE_MANIFEST.md · R12 = research/R12_DONOR_FILE_MANIFEST.md ·
              R13 = research/R13_IDE_DEBUG_PLATFORM.md · 06 = transplant matrix · 07 = architecture
ESTIMATES = ESTIMATE class (reading-based); phase totals reconcile with 08 overview (§13 below)
ENTRY_RULE = every task starts with: spec note under specs/008-*/phases/<P>/ + Ponytail check + tests written first
EXIT_RULE = every task ends with: tests green (incl. mutation control for neg), budgets measured where listed, independent
            review per tier, Build Learning line
```

## P−1′ — Restore CI (founder admin + agent re-run)

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| A-01 | Re-run failed `main` integrity run 36589753362 unchanged | Actions available | `.github/workflows/foundation-integrity.yml` (no edit) | Run concludes; result + log archived in `CI_403_REDIAGNOSIS` addendum | run log | 0.05 | T0 | GOV-01 |
| A-02 | If 403 recurs: reproduce `verify-local --remote-baseline` locally with founder token; capture status, `message`, `x-ratelimit-*` | A-01 fail | `.github/scripts/wepld_integrity.py` (read-only) | Root cause proven (rate limit vs permission) and recorded | local log | 0.1 | T0 | GOV-01 |

## P0 — Governance reset

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| G-01 | Merge this planning package (Draft PR → review → merge by founder) | A-01, egress preflight | `specs/008-*` | Merged; trusted base updated | integrity green | 0.1 | T0 | GOV-03, GOV-04 |
| G-02 | Founder-only SSH signing key + `allowed_signers` (protected) | — | `.github/allowed_signers` (new) | Signed tag verifies with `git verify-tag` against file | neg: unsigned co-sign rejected | 0.1 | T2 | GOV-02 |
| G-03 | Write `governance_check.py` (single stable checker) + `PROTECTED_PATHS` manifest; run from base via `pull_request_target`, candidate read as data | G-02 | new `.github/scripts/governance_check.py`, `.github/PROTECTED_PATHS` | Protected-path diff requires signed co-sign; ordinary docs/code pass; phase-exit PRs without Build Learning entry fail | det: checker unit tests; neg: PR editing checker cannot change verdict; neg: label-only co-sign fails; det: checker requires a Build Learning line in phase-exit PRs | 0.5–1 | T2 | GOV-02, GOV-08 |
| G-04 | Add `GitHubClient` status/rate-limit logging + bounded backoff (only on 403/429 rate-limit) | G-03 | `.github/scripts/governance_check.py` | Rate-limit responses logged with headers; retries bounded | det: mocked 403/429 | 0.2 | T2 | GOV-01 |
| G-05 | Archive v1–v72 successor scripts read-only; retire old workflows after G-03 proves equivalence | G-03 | `.github/scripts/*` → `docs/historical/governance-successors/` | Equivalence table: every v72 base-controlled check has a G-03 counterpart or a written retirement reason | det: replay last 20 merged PRs through checker → same verdicts | 0.3 | T2 | GOV-02 |
| G-06 | Governed amendments: invariants "Workers" line (Mirefa/Edara), `MASTER_PLAN_INDEX` → V3, AGENTS.md build-method mechanism text | G-03 | protected docs | Signed co-sign; texts match ADR-011 | integrity | 0.2 | T2 | GOV-09, GOV-10 |

## P1 — Donor baseline (isolated, no product code)

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| B-01 | Provision Windows Sandbox/VM baseline image (Node, pnpm, Rust, Git) | — | — | Reproducible setup script; host profile untouched | — | 0.2 | T2 | GOV-07 |
| B-02 | Fetch T3 @36d4d711 and stable v0.1.3 @d2c44031; record tree hashes; mirror tarballs privately | B-01 | R11 §1 | Hashes match R11 pin record | hash check | 0.1 | T2 | GOV-05 |
| B-03 | Build + run T3 desktop (both refs); run test suites; record pass/fail/skip | B-02 | R11 §6 | Pass ratio recorded per area; choose FORK_BASE (default 36d4d711 unless ratio materially worse) | T3 suites | 0.5–1 | T2 | NF-01..03 |
| B-04 | Measure B1–B5 for T3 and Orca @e310a636 | B-03 | 09 §3 | CSV committed; method reproducible | bench B1–B5 | 0.3 | T2 | NF-01..03 |
| B-05 | Measure `synchronous=FULL` cost on T3 receipt table; rusqlite fsync append latency on founder NVMe | B-03 | 07 §4–5 | Numbers recorded; NF-04 budget confirmed or revised | microbench | 0.1 | T2 | NF-04 |
| B-06 | Verify Claude Agent SDK + `claude-agent-acp` load from user-provided location in T3 build; confirm installer exclusion feasible | B-03 | R11 §5 | Feasibility note; G4 path chosen | — | 0.1 | T2 | SEC-13 |
| B-07 | G2 decision record (GO / reopen ADR-001) | B-03..06 | 00 §7 | Signed founder decision | — | 0.05 | T0 | GOV-03 |

## P2-N — Zain naming clearance (before F-03)

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| N-01 | Name/trademark clearance for "Zain" in software classes (founder + counsel; R19 checklist) | G-01 | research/R19 | Written clearance or rename decision recorded | review of clearance record | 0.2 | T0 | GOV-11 |
| N-02 | Choose controlled domain → app ID / AUMID / bundle ids; update ZAIN_NAMING_MIGRATION §2 | N-01 | ZAIN_NAMING_MIGRATION | IDs fixed before any build is distributed | det: identity grep gate uses final ids | 0.1 | T0 | GOV-11 |
| N-03 | Package scope + crate names decision (no publishing); collision check vs Zain-LLM | N-01 | R19 | Scope/crates documented; no shared identifiers with Zain-LLM | det: grep gate for Zain-LLM identifiers | 0.1 | T0 | GOV-11, GOV-12 |
| N-04 | Canonical docs + crate rename (`wepld-*` → `zain-*`) as part of G-06 / F-10 | G-06, F-10 | AGENTS.md, invariants, Cargo.toml | Rust suite green after rename; protected docs signed | det: cargo test | 0.3 | T2 | GOV-11 |

## P2 — Fork, strip, rebrand (usable Zain workbench)

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| F-01 | Import T3 at FORK_BASE into Zain monorepo layout (apps/, packages/, native/) beside `crates/` | B-07 | R11 §2 KEEP set | Tree equals upstream KEEP set byte-for-byte (manifest hash); source admission record (pin, license, deps, tests) per R11 | manifest hash test | 0.5 | T2 | PR-01, GOV-05, GOV-07 |
| F-02 | Strip: mobile, marketing, relay/T3 Connect, Clerk, PostHog, `.repos/`, unused providers, V1 importer | F-01 | R11 §2 STRIP set | Build + kept tests green at B-03 ratio; no references remain | det: kept suites; grep | 1–2 | T2 | PR-22, SEC-11 |
| F-03 | Identity rename (app id, AUMID, protocol, CLI, data dirs, env prefix, refs, MCP name, hook headers) | F-02 | R11 §4; 06 §4 | Zero donor identifiers outside NOTICE files | det: donor-identifier grep gate | 1–1.5 | T2 | SEC-11 |
| F-04 | Update feed → Zain-hosted Generic provider with ed25519-signed manifest verified by Core (no tokens in client) | F-03 | R11 §7; R13 §6 | Updater refuses donor manifests | neg: donor manifest rejected | 0.5–1 | T2 | SEC-11 |
| F-05 | Telemetry removal + idle-egress test | F-02 | R11 §3 | No outbound connections at idle (except user-initiated) | e2e: egress capture | 0.3 | T2 | PR-22, SEC-11 |
| F-06 | Claude SDK exclusion from installer; user-consented load path; installer-content gate | B-06, F-02 | R11 §3, §5 | Installer contains no `claude-agent-sdk*`; Claude sessions work with user-provided SDK + API key | det: installer-content gate; e2e: Claude session with key | 0.5 | T2 | SEC-13 |
| F-07 | Default permission mode → Supervised; remove Full access option | F-02 | R11 §3 (RuntimePolicy) | Full access not selectable | e2e; neg (with S1 later) | 0.2 | T2 | SEC-06 |
| F-08 | ThreadSettlement → cosmetic archive only | F-02 | R11 §3 | Merge/close never marks a thread "done/settled" | det | 0.2 | T1 | PR-13 |
| F-09 | Protocol version bump (Zain-1) | F-03 | contracts environment.ts (R11) | T3 clients get 426 | det | 0.1 | T2 | SEC-11 |
| F-10 | Rename Core binary `zain-core`; move S2 commands under it; package next to `server.asar` | F-01 | `crates/core`, build scripts (R11 §7) | One `zain` CLI (Server) + `zain-core`; S2 tests green | det: existing 19k-line Rust suite | 0.5 | T2 | PR-01 |
| F-11 | Windows NSIS build (dev-signed) + notices generation gate | F-03 | R11 §7 | Installer builds; build fails on missing notice; OV code-signing certificate with cloud-HSM key + jsign (Azure Trusted Signing unavailable to a Saudi individual — R13 F1) | det: notice gate | 1–1.5 | T2 | PR-21, GOV-06 |
| F-12 | Inherited-bug hardening batch 1: DB writer stalls (#21840, #23482), preview webview memory (#15579), Windows startup (#25262) | F-02 | R02 §13 | Each issue reproduced then fixed or explicitly deferred with limitation | det/e2e per issue | 2–4 | T2 | NF-02, PR-21 |
| F-13 | Effect 4 / orchestration-v2 ramp-up notes (Build Learning) | F-01 | R02 §3 | Seam walkthrough doc for P3 | — | 2–4 (learning, overlaps) | T0 | GOV-08 |
| F-14 | Accessibility pass on kept UI (keyboard, focus, contrast) | F-03 | R13 §7 | WCAG 2.2 AA checklist for core flows; baseline only; terminal screen-reader gap carried to I-11 | e2e: axe scan | 1–2 | T1 | PR-24 |
| F-15 | Offline checklist + B1–B3 budget check vs P1 | F-05..F-11 | 09 | NF-01..03 met or exception recorded | bench B1–B3, B12 | 0.3 | T1 | NF-01..03, NF-08 |
| F-16 | P2 exit: install, chat + Codex + ACP + Claude(API key) sessions, worktree, diff, terminal, preview | all P2 | — | DoD in 08 P2 | e2e smoke; V1-01 composer→task; V1-06 parallel worktrees | 0.2 | T1 | PR-01..04, PR-08 |

## P3 — Trusted Core (differentiator)

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| C-01 | **G3 spike**: ACP `fs/write` (S3) + Codex approval (S2) via Core with ledger receipts; kill -9 → UNKNOWN | F-16 | R11 §3 (S2, S3), `crates/core` | Spike log; go/no-go recorded | det; R1 sample | 1–2 | T2 | SEC-02, SEC-03 |
| C-02 | Core protocol v2: direction-tagged ids, chunk frames, fencing epoch, data-root OS lock | C-01 | `crates/contracts/src/{frame,protocol}.rs` | v1 tests green + new contract tests | det; neg: stale epoch, replayed id, second Core | 1–2 | T2 | SEC-09 |
| C-03 | Ledger (rusqlite, FULL sync, hash chain, projections, tombstones, forward-only migrations, UNSUPPORTED_SCHEMA) | C-02 | new `crates/core/src/ledger/*` | Append/verify/rebuild; schema-too-new refusal; ledger exports audit JSONL (enterprise seam) | det; R6; W5; bench B10; det: audit export JSONL from ledger (V1-18) | 2–3 | T2 | SEC-08, NF-06, PR-25, CL-V1-18 |
| C-04 | Effect API: propose/dispatch/report/reconcile/open_dispatches with Spec 006 §19 types | C-03 | `crates/contracts` (reuse PR #343 descriptors where fitting) | Idempotent on (op id, input digest); retry-safety states; only secret handles cross into Core | det; neg: dispatch without grant; neg T6: seeded fake secret never in ledger/logs | 2–3 | T2 | SEC-02, SEC-03, SEC-12 |
| C-05 | Policy engine (Cedar or minimal Rust rules after Ponytail) + permission-mode compilation (Manual/Auto/Skip × per-tool) | C-04 | R12 Cedar | Skip never overrides Blocked; deny-overrides | det; neg | 2–4 | T2 | SEC-01, CL-V1-02 |
| C-06 | CoreBridge service in Server (spawn, health, restart, fail-closed) | C-02 | R11 (ResourceMonitorBinary pattern) | Core down → gated effects refused | e2e; W1 | 1 | T2 | SEC-01 |
| C-07 | Seam S1 runtime-policy clamp | C-06 | R11 §3 S1 | Mode per Core grant | neg | 0.3 | T2 | SEC-06 |
| C-08 | Seam S3 ACP fs/terminal PEP | C-06 | R11 §3 S3 | Every ACP fs/terminal effect has receipt | neg T1 (ACP write outside worktree) | 1 | T2 | SEC-01 |
| C-09 | Seam S2 provider approvals (Claude PreToolUse→propose+dispatch, canUseTool; Codex handlers; ACP permission) | C-06 | R11 §3 S2; 03C §2 | Provider prompts decided by Core; CC-T01..T03 | neg; CC-T02 kill mid-Edit; V1-17 | 2–3 | T2 | SEC-01, SEC-03 |
| C-10 | Seam S4 EffectWorker + S4b recovery gating | C-04 | R11 §3 S4/S4b | No requeue/auto-continue before open_dispatches | R1 sweep; W9 | 1.5–2.5 | T2 | SEC-10, NF-05 |
| C-11 | Seam S5 per-run receipt link + compaction exemption | C-03 | R11 §3 S5 | `zain.run-receipts` survives compaction | det; W2 | 1 | T2 | SEC-08 |
| C-12 | Seams S6 MCP access, S7 git destructive ops, S8 terminals | C-06 | R11 §3 | Each class mediated with receipts | neg per class; W6 | 1.5–2.5 | T2 | SEC-01, PR-08 |
| C-13 | WebAuthn approvals (registration, challenge, assertion verify in Core) | C-04 | 07 §6; R13 | Approval impossible without user presence | neg T3 (forged/replayed) | 1–2 | T2 | SEC-04 |
| C-14 | Inbox UI (approvals, unknown outcomes, expiries) + trust indicator | C-13 | web app (R11) | Outcomes rendered only from Core | e2e | 1–1.5 | T1 | PR-23, SEC-05 |
| C-15 | Permission settings UI (modes × per-tool) | C-05 | web app | Matches Claude-like UX; compiled to Core | e2e; V1-02 | 1 | T1 | CL-V1-02 |
| C-16 | Containment floor: data-root/out-of-worktree deny in provider profiles; Job Objects (Orca process-host) | C-07 | R12 D4; R13 §3 | Agents cannot write data root | neg T10b | 1–2 | T2 | SEC-06 |
| C-17 | MEDIATED/UNMEDIATED tagging + reporting paths (PostToolUse, file-hash diffs) | C-09 | 07 §6 | Every receipt tagged | det | 0.5 | T2 | SEC-05 |
| C-18 | Release build without observe mode; signed `core.mode` in dev | C-13 | — | Release binary lacks observe path | neg T15 | 0.3 | T2 | SEC-15 |
| C-19 | `ledger.anchor` (signed git note/tag) | C-03, G-02 | — | Divergence detected after tamper | neg T10b | 0.5 | T2 | SEC-08 |
| C-20 | Recovery suite R1–R11 + W1–W9 harness (fault injection at every boundary) | C-10..C-12 | R05 §7; 09 §2 | Invariants I1–I6 100% | R/W suites | 2–3 | T2 | NF-05 |
| C-21 | Budgets B13 + NF-04 | C-09 | 09 | p95 ≤ 25 ms/effect | bench B13 | 0.3 | T2 | NF-04 |
| C-22 | P3 exit + security review (T2) | all P3 | — | 08 P3 DoD | all above | 0.3 | T2 | SEC-17 |

## P4 — Missions, Brain, continuations

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| M-01 | Mission model + APIs + thread links (Core) | C-22 | 07 §2–3 | Missions survive restart/reboot | det; R1 | 1–1.5 | T2 | PR-06 |
| M-02 | Continuations: schedules, wait-for-CI/PR/human, missed-run policy, two-phase fire | M-01 | 05 §4.9 | One fire per condition | det; W2b, W3; V1-05 | 1–2 | T2 | PR-06, SEC-10 |
| M-03 | Brain store: notes, preferences (CANDIDATE→QUALIFIED), spec index (path+blob), FTS5 | C-03 | ADR-006 | Repo specs never stored as authority | det; NF-07 bench | 1–1.5 | T2 | PR-05, NF-07 |
| M-04 | Capsule injection + `brain.query` MCP tool | M-03 | R11 (injectHistory/system prompt seam) | Capsule ≤ 2k tokens default | det; B8 | 0.5–1 | T2 | PR-07 |
| M-05 | Compaction capsule capture; continue-as-new for long missions | M-04 | 05 §4.8 | Recall on non-pinned decisions measured | W8; B8 | 0.5–1 | T2 | PR-07 |
| M-06 | Missions + Brain UI (Projects, Work views) | M-01..M-03 | 07 §7 | Edit/supersede/incognito | e2e; V1-03, V1-04 | 1–1.5 | T1 | PR-05, PR-06 |
| M-07 | P4 exit (mission survives reboot, resumes on CI) | all P4 | — | 08 P4 DoD | e2e | 0.2 | T1 | PR-06 |

## P5 — Review, Trusted Completion, Connections

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| V-01 | Reviewer route ≠ builder route enforcement; per-role pins | M-07 | 07; ADR-008 | Same-route reviewer refused | neg | 0.5 | T2 | PR-03, PR-12 |
| V-02 | SUPERSEDED by K-04/K-05 (Zain Code Review findings panel + dispositions) | V-01 | T3 diff panel (R11) | Findings tracked to resolution | e2e | 0 | T1 | PR-12 |
| V-03 | SUPERSEDED: PR-Agent wrap replaced by Zain Code Review engine (K-*); PR-Agent reference only | V-01 | R12 D22 | Runs with user's key; output as findings | det | 0 | T2 | PR-12 |
| V-04 | Completion evaluate/decide (rules 1–10 + UNMEDIATED handling) + Stop/SubagentStop gating | V-02 | Spec 006 §20; 03C | Merge ≠ completion; UNKNOWN blocks | neg; CC-T05; V1-07 | 1–1.5 | T2 | PR-13 |
| V-05 | MCP connections (local/remote OAuth) with per-tool grants | C-22 | R12 D13; T3 /mcp | Revoked token → blocked_on_auth | neg; V1-09 | 1–1.5 | T2 | PR-14 |
| V-06 | Agent Skills (SKILL.md) loader, hash pinning, re-review on update | V-05 | 03C; census CL-E-006 | Widening update disabled until re-approved | neg T5; V1-08 | 0.5–1 | T2 | PR-14 |
| V-07 | MCPB extension install with manifest review | V-05 | census CL-E-031 | Unknown extension requires explicit trust | neg; V1-10 | 0.5–1 | T2 | PR-14 |
| V-08 | P5 exit: Astro "first complete loop" E2E | all P5 | — | Loop runs locally | e2e | 0.3 | T1 | PR-01..14 |

## P6 — IDE breadth, debugging, CLI agents, benchmarks

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| I-01 | Monaco editor surface bound to T3 file/state RPC | F-16 | R12 D7; R13 §2 | Edit/save large files ≤ 1 s for 5 MB | e2e; bench | 2–3 | T1 | PR-10 |
| I-02 | Diff comments port (Orca) | I-01 | R12 D7 | Comments anchored across edits | e2e | 1–1.5 | T1 | PR-10 |
| I-03 | LSP: 1-week spike @vscode/monaco-lsp-client vs monaco-languageclient behind a wrapper; server lifecycle in Server (TS 7 `tsc --lsp`, Python, rust-analyzer, gopls); untrusted-repo mode disables code-running features; spawns are `process.spawn.language_server` effects | I-01 | R13 §2 | Diagnostics, go-to-def, hover per language | e2e per language | 6–10 | T2 | PR-10 |
| I-04 | Debugging: DAP client + debug UI; adapters (js-debug, debugpy, CodeLLDB/lldb-dap, Delve); launches as Core-gated process effects; agent-readable debug state via MCP | I-01, C-22 | R13 §1 | Breakpoints/step/variables in 4 languages; launch receipts; effect classes process.spawn.debug_adapter / process.spawn.debuggee / process.attach.debug (always approval) / debug.evaluate; debugpy from user env (EPL pydevd not bundled) | e2e per adapter; neg: launch without grant | 6–10 | T2 | PR-11 |
| I-05 | Design Mode capture → composer (Orca port) | F-16 | R12 D2 | Element payload with DOM path, styles, crop | e2e; AT-01..05 | 3–6 | T2 | PR-15, PR-18 |
| I-06 | CLI-agent catalog + hook/OSC 7501 status (overlays + authenticated endpoint) | C-22 | R12 D3 | Status detected; user global configs untouched | neg T17 | 3–5 | T2 | PR-09, SEC-14 |
| I-07 | Linear integration (Orca port) | V-05 | R12 D5 | Issue → mission link | det fixtures | 2–4 | T2 | PR-08 |
| I-08 | Benchmark harness + public results (B6–B13) | C-22 | R12 D23; 09 | Raw data published | bench | 1–2 | T2 | NF-09 |
| I-09 | macOS + Linux packaging (DMG notarized, AppImage/deb) + per-OS update channels | F-11 | R13 §6 | Installs and runs P2 smoke on each OS | e2e smoke | 3.5–6.5 | T2 | PR-21 |
| I-10 | Local OTel sink (observational only) | C-22 | 03C | No egress; spans not evidence | det | 0.3–0.5 | T1 | PR-22 |
| I-11 | Accessible terminal mode (xterm.js screenReaderMode alternative to Canvas renderer) + WCAG 2.2 AA audit of IDE surfaces | F-14, I-01 | R13 §7 F5 | Screen reader reads terminal output; AA checklist passes | e2e: axe + NVDA/VoiceOver scripted checks | 2–5 | T1 | PR-24 |

## P7 — Design Studio v1

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| D-01 | Canvas (iframe artboards, pan/zoom, multi-artboard) | I-05 | R03B §5 | Artboards render live preview | AT-01..03 | 2–3 | T1 | PR-15 |
| D-02 | Isolated preview origin | D-01 | R03B §5; SEC-16 | No access to Server/Core | neg T11; AT sandbox | 0.5–1 | T2 | SEC-16 |
| D-03 | Element→source resolver (3 tiers) | D-01 | R12 D20 | EditTarget with confidence; ambiguity prompts user | AT source-mapping | 2–3 | T2 | PR-15 |
| D-04 | Layer tree + token-aware properties panel | D-03 | R03B §7 | Edits map to source or tokens | AT | 1–2 | T1 | PR-15 |
| D-05 | Comments → agent proposal → Core grant → patch → refresh; op-log history + undo | D-03, C-22 | R03B §7.4–7.5 | Stale-write refusal | AT history/conflict | 1.5–2.5 | T2 | PR-15 |
| D-06 | DTCG token store + design-system registry + pins (Style Dictionary) | D-04 | R12 D21 | Round-trip tokens | AT tokens/ds-pin | 1–1.5 | T2 | PR-15 |
| D-07 | Exports HTML/zip/PNG/PDF; Excalidraw sketch layer | D-01 | R12 D19 | Export fidelity checks | AT export | 1–1.5 | T1 | PR-15 |
| D-08 | P7 exit: AT-01..AT-15 on Windows | all P7 | — | All P0 AT green | AT; V1-12 | 0.2 | T1 | PR-15 |

## P8 — Containment (OS sandbox)

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| S-01 | Port codex Windows sandbox set into Core launcher | C-22 | R12 D9; R13 §3 | Provider runs under sandbox; fs/network rules enforced; Codex Windows backends are restricted-token / elevated sandbox users + WFP service / MXC — not AppContainer (R13 F3) | escape suite (Win) | 3–5 | T2 | SEC-07 |
| S-02 | Linux sandbox (landlock/seccomp/bwrap) | S-01 | R12 D9 | Same rules on Linux | escape suite (Linux) | 2–3 | T2 | SEC-07 |
| S-03 | macOS Seatbelt profiles | S-01 | R12 D9; R13 §3 | Same rules on macOS | escape suite (mac) | 2–3 | T2 | SEC-07 |
| S-04 | Network egress proxy with allowlist + approvals | S-01 | R12 D9 network-proxy | Unapproved egress blocked | neg T2 | 1.5–2.5 | T2 | SEC-07 |
| S-05 | Re-enable Full-access lane inside sandbox; trust indicator upgrade | S-01..S-04 | 07 §6 | Claim widens only after escape suite passes | e2e | 0.3 | T2 | SEC-05 |
| S-06 | Debug sandbox profile (ptrace/process_vm allowed for debuggee only) on Linux/macOS/Windows | S-02, I-04 | R13 F4 | Debugging works inside sandbox without widening agent profile | neg: agent process cannot ptrace | 0.5–1 | T2 | SEC-07, PR-11 |

## P9 — General agent work

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| W-01 | Documents/artifacts as project files; preview; export MD/HTML/PDF | V-08 | T3 file previews (R11) | One-pager → PDF | e2e; V1-11 | 1–2 | T1 | PR-16 |
| W-02 | PPTX/XLSX generation (permissive libs after Ponytail) | W-01 | R13 | Opens in Office/LibreOffice | det | 1–2 | T2 | PR-16 |
| W-03 | Research task type with citations as evidence | M-07 | — | ≥3 cited sources stored | e2e; V1-13 | 1–1.5 | T2 | PR-17 |
| W-04 | SUPERSEDED by Y-* (Zain Browser); general-web lane = Y-09 | S-04 | R13 §4; R11 | Form fill on localhost; payments refused; T3 already drives pages via Playwright connectOverCDP (CdpRelay.ts) + 12 preview_* MCP tools; work = gating incl. redirects (Playwright MCP is not a security boundary) | neg T12; V1-14 | 0 | T2 | PR-18 |
| W-05 | Computer use (Windows first) behind per-session grants | S-01 | R12 D6; R13 §5 | Approved actions only; Orca helpers: macOS Swift (AX, ScreenCaptureKit, CGEvent; TCC grants), Windows PowerShell UIA/SendInput → replace ExecutionPolicy Bypass with signed helper, Linux AT-SPI/xdotool X11 only | neg T12; V1-15 | 6–10 | T2 | PR-19 |

## P10 — Remote and runner

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| R-01 | Headless runner (`zain serve`) + Linux service; Windows service wrapper | M-07 | R13 §6 | Runner survives reboot; Windows service via Rust `windows-service` crate, non-SYSTEM account, no desktop features in service mode | e2e | 1–2 | T2 | PR-20 |
| R-02 | Project-home rule + export/import bundles | R-01 | 07 §5; 05 §4.7 | Grants dropped; dispatches UNKNOWN on new home | det | 1–2 | T2 | PR-20 |
| R-03 | Passkey pairing for phone/web approvals | C-13, R-01 | 05 §7.1 | Guest links cannot approve | neg; V1-16 | 1–2 | T2 | PR-20, SEC-04 |
| R-04 | Web client hardening for LAN/Tailscale | R-01 | R11 (client-runtime) | Scoped sessions only | neg | 1–2 | T2 | PR-20 |


## Product components (cross-phase; the `[Px]` tag is the phase used for totals)

### Zain Code Review (16_*, research/R14) — OCR engine fork + Zain-owned UX and authority

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| K-01 | [P2] Optional spike: build forked OCR engine on Windows; engine mode on the Zain repo with a local Ollama route; advisory, read-only | F-03 | R14 §11; alibaba/open-code-review@375f64cd | Findings shown, labelled advisory; no fixes | ZCR spike log | 0.5–0.75 | T2 | PR-26 |
| K-02 | [P5] Admission: pin, SBOM + transitive license scan, notices, Go toolchain in CI (Win/Linux/mac) | V-01 | R14 §9 | Source admission record; notices generated | det: license gate | 0.5–0.75 | T2 | PR-26, GOV-07 |
| K-03 | [P5] Fork-vendor `native/zain-review-engine` + patches Z-P1..Z-P6 (route lock `ZAIN_REVIEW_*`, HOME isolation, branding) + upstream suite green | K-02 | R14 §5–6 | Upstream tests green; ambient config cannot override the route | neg ZCR-T05 | 1–1.5 | T2 | PR-26, SEC-18 |
| K-04 | [P5] `packages/review-engine` normalizer/fingerprint/anchors + EngineRunner (spawn as Core effect, Job Object, NDJSON, cancel/resume) + contracts/ledger kinds + route rule (reviewer ≠ builder) | K-03, C-22 | R14 §7 | One finding schema for engine and delegated modes | det; neg reviewer=builder | 1.75–2.5 | T2 | PR-12, PR-26 |
| K-05 | [P5] IDE UX: findings panel, Monaco markers, filters, accept/dismiss/false-positive, sanitized renderer | K-04, I-01 | R14 §7 | Model text never rendered as trusted markdown | e2e; neg ZCR-T15 | 1.5–2 | T1 | PR-26 |
| K-06 | [P5] Fix pipeline: proposals, preimage OID check, checkpoint, Core-granted apply, undo, verification profile | K-04, C-12 | R14 §7 | Stale fix refused; undo restores; tests run after apply | neg ZCR-T07/T10/T11 | 1.5–2 | T2 | PR-26, SEC-02 |
| K-07 | [P5] Acceptance suite ZCR-T01..T25 (excl. T21) + guard-mutation job | K-03, K-04, K-05, K-06 | R14 §8 | All pass; each guard test fails with its guard removed | ZCR suite | 1–1.5 | T2 | PR-26, SEC-17 |
| K-08 | [P5] Delegated mode (MCP tools, read-only reviewer session, coverage) + fix worker in disposable worktree | K-07 | R14 §11 (P5b) | Reviewer session cannot write | neg ZCR-T17 | 1.75–2.5 | T2 | PR-26 |
| K-09 | [P6] CI action + SARIF + scan mode + "propose rule" + model proxy (MEDIATED egress) | K-08 | R14 §11 | CI summary; egress mediated | ZCR-T21 | 1.5–2.5 | T2 | PR-26 |

### Zain Engineering System (17_*, research/R15) — PStack-derived loop + Playwright E2E

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| E-00 | [P1] Donor pin snapshot + license records (PStack, cursor-team-kit, Ascout candidate) | B-01 | R15 §10 | Pins + LICENSE hashes recorded | hash check | 0.2 | T0 | GOV-05 |
| E-01 | [P5] Skill pack adaptation into `packages/skills/zain-engineering` (router, playbooks, principles, agents, CTK skills), notices, identifier scrub | V-06 | cursor/plugins@ab1f702c pstack/ | No PStack/Cursor names in product; notices present | ES-AT-03 | 2–3 | T2 | PR-27, GOV-06 |
| E-02 | [P5] Core evidence kinds + completion rules ES-1..ES-7 + patch-id staleness | V-04 | R15 §7 | INCONCLUSIVE never PASS; verdict stale after patch change | neg ES-AT | 1–1.5 | T2 | PR-27, PR-13 |
| E-03 | [P5] `zain-browser-verify` E2E (Playwright, isolated partition, localhost-only origin policy) — source UNRESOLVED (Ascout candidate) pending founder FO-9 | C-22, Y-03 | R15 §6–7 | Evidence hashed into Core; no user profile touched | ES-AT e2e | 3–5 | T2 | PR-27, PR-28 |
| E-04 | [P5] verify-skill generator into `.zainide/skills` + dogfood on Zain | E-01, E-03 | R15 §10 | Generated skills pass checks | det | 1–1.5 | T2 | PR-27 |
| E-05 | [P5] Review lanes (independent routes, comment reviewer, deslop) feeding Zain Code Review findings | K-04 | R15 §10 | Same schema as K-04; no second review store | det | 1–2 | T2 | PR-27, PR-26 |
| E-06 | [P6] PR babysit/shipping (gated merges) | E-02, E-05 | R15 §10 | Merge requires a Core grant; merge ≠ completion | neg | 2–3 | T2 | PR-27 |
| E-07 | [P5] Acceptance suite ES-AT-01..16 + tie into V-08 | E-01, E-02, E-03, E-04, E-05 | R15 §9 | Suite green with mutation control | ES-AT | 1 | T2 | PR-27, SEC-17 |

### Zain Plan Mode (18_*, research/R16) — mattpocock/skills (MIT) + T3 plan mode + Core read-only profile

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| L-01 | [P2] Inherit T3 plan mode under Zain brand; verify enforcement; label "not yet enforced" | F-16 | R16 §7 PL-01 | Plan thread renders the proposed plan | e2e | 0.3–0.5 | T1 | PR-29 |
| L-02 | [P3] `PLAN_READONLY` Core profile bound to plan path + base commit | C-05, C-07 | R16 PL-02 | MEDIATED writes outside the plan path denied | neg N1–N8 | 1–1.5 | T2 | PR-29, SEC-19 |
| L-03 | [P3] Turn-end out-of-path diff → INVALIDATED; CLI agents blocked in plan mode | C-17, L-02 | R16 PL-03 | Violation blocks approval | neg N9–N10 | 0.5 | T2 | PR-29, SEC-19 |
| L-04 | [P4] Plan artifacts + Brain index + `plan.lock.json` | M-03, L-02 | R16 PL-04 | Lock covers all artifacts | det D1–D3 | 0.5–1 | T2 | PR-29 |
| L-05 | [P4] Approve plan → start mission (WebAuthn) | M-01, C-13, L-04 | R16 PL-05 | No mission without lock + assertion | neg N11–N12 | 0.5 | T2 | PR-29 |
| L-06 | [P5] `packages/skills/zain-plan` copy/adapt (mattpocock/skills@59db609e) + NOTICE + manifest | V-06 | R16 §5 | Hashes match manifest | det D4–D5; neg N13 | 1–1.5 | T2 | PR-29, GOV-06 |
| L-07 | [P5] `tasks.dag.json` handoff contract shared with the Engineering System | L-04, E-01 | R16 PL-07 | Engineering consumes the DAG without re-parsing prose | det D6 | 0.3–0.5 | T2 | PR-29, PR-27 |
| L-08 | [P5] Plan UI: canvas, question loop, decision cards, DAG view, approve bar | L-04 | R16 PL-08 | Recommended answers logged | e2e E1–E4 | 2–3.5 | T1 | PR-29 |
| L-09 | [P5] Critic route ≠ griller route; findings in the Code Review schema; readiness gate | V-01, K-04 | R16 PL-09 | Same-route critic refused | neg N14 | 0.5–1 | T2 | PR-29 |
| L-10 | [P5] Plan Mode acceptance suite + mutation control | L-01, L-02, L-03, L-04, L-05, L-06, L-07, L-08, L-09 | R16 PL-10 | Negatives fail with Core disabled | all | 0.5–1 | T2 | PR-29, SEC-17 |

### Zain Browser (19_*, research/R17) — one BrowserController, four lanes

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| Y-00 | [P2] Strip T3/Orca browser-cookie import; isolate agent partition; disable eval outside Preview; relay method allowlist | F-02 | R17 §5, WB0 | No code path reads user browser stores | neg: cookie import absent; grep gate | 0.5–1 | T2 | PR-28, SEC-20 |
| Y-01 | [P3] Browser effect classes + hard-block floor rules registered in Core | C-05 | R17 WB4 (part) | Payments/credentials/account creation/executable downloads blocked even in Skip | neg | 0.5–1 | T2 | PR-28, SEC-20 |
| Y-02 | [P5] Controller unification (broker → BrowserController; lanes Preview/Agent/Test) + Playwright 1.64 bump | Y-01 | R17 WB1 | Single controller; MCP/CLI/UI are thin front-ends | det | 1.5–2.5 | T2 | PR-28 |
| Y-03 | [P5] Pre-request navigation/redirect gate (Electron + CDP Fetch) + spike | Y-02 | R17 WB2 | Redirect to a non-granted origin blocked before the request | neg redirect | 2–3 | T2 | PR-28, SEC-20 |
| Y-04 | [P5] Page classifier + hard blocks + download quarantine | Y-03 | R17 WB3 | Executable download quarantined | neg | 1.5–2.5 | T2 | PR-28, SEC-20 |
| Y-05 | [P5] Core integration: grants, receipts with replay classes, Inbox UX | Y-02, C-14 | R17 WB4 | Every action has a receipt with screenshot/AX/HAR hashes | det; R1 sample | 1.5–2 | T2 | PR-28, SEC-02 |
| Y-06 | [P5] Evidence: screenshots, HAR-from-CDP, redaction, tracing, export | Y-05 | R17 WB5 | No secrets in evidence | neg T6 | 1.5–2.5 | T2 | PR-28 |
| Y-07 | [P5] Session recovery + takeover UX + prompt-injection measures | Y-05 | R17 WB6 | Human takeover for sign-in; injection suite passes | injection suite | 1–1.5 | T2 | PR-28 |
| Y-08 | [P5] Test lane endpoint (loopback) + mutation-controlled suite | Y-02 | R17 WB7 | Suite green; each guard test fails without its guard | R17 §11 | 1–1.5 | T2 | PR-28, SEC-17 |
| Y-09 | [P9] General web in Agent lane + user-session lane (MV3 extension) + Claude browser_toolset adapter | Y-08, S-04 | R17 WB8–WB9 | Opt-in, tab-group scoped; no ambient credentials | neg | 4.5–7 | T2 | PR-28, PR-18 |

### DeskGate (20_*, research/R18) — Desktop Commander tools as Core-mediated adapters

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| H-00 | [P1] Registry row + license admission for DesktopCommanderMCP@db3430f2; remote-desktop-commander recorded EXCLUDED (proprietary) | B-01 | R18 §1 | Admission record | review | 0.1–0.2 | T0 | PR-30, GOV-07 |
| H-01 | [P3] `packages/deskgate` on Server `/mcp`; schemas port; static-import guard (no own spawn/config) | C-06, C-12 | R18 §4 | DeskGate cannot spawn outside the Server host | neg DG-N10 | 0.5–1 | T2 | PR-30, SEC-21 |
| H-02 | [P3] fs adapters (read/list/write/edit/move/mkdir) via Core effects | H-01 | R18 | Every fs effect has a receipt | neg DG-N* | 1–1.5 | T2 | PR-30 |
| H-03 | [P3] Process/terminal adapters on the single node-pty host; ownership-scoped signals; `set_config_value` refused | H-01 | R18 | Kill limited to Zain-owned process trees | neg | 1–1.5 | T2 | PR-30, SEC-21 |
| H-04 | [P6] Search adapters (rg as spawn effect) | H-01 | R18 | Results paged; spawn receipted | det | 0.5–1 | T2 | PR-30 |
| H-05 | [P3] Negative/mutation suite DG-N01..N14 + perf DG-B1..B9 | H-02, H-03 | R18 §5 | Suite green; adapter overhead p95 ≤ 5 ms | neg; bench | 1–1.5 | T2 | PR-30, SEC-17 |
| H-06 | [P10] Remote DeskGate via runner/project-home + passkey | R-01, R-02, R-03 | R18 | No third-party relay | neg | 0.7–1.3 | T2 | PR-30, PR-20 |
| H-07 | [P6] Cross-OS parity (macOS/Linux) | H-05, I-09 | R18 | Parity matrix green | e2e | 0.2–0.5 | T2 | PR-30 |

## §13 Phase totals (generated by script; do not hand-edit)

| Phase | Tasks (incl. component tasks tagged to it) | ESTIMATE pw (low–high, computed) |
|---|---|---|
| P−1′ Restore CI | 2 | 0.2–0.2 |
| P0 Governance | 6 | 1.4–1.9 |
| P1 Baseline | 9 | 1.7–2.3 |
| P2-N Naming clearance | 4 | 0.7–0.7 |
| P2 Fork/strip/rebrand | 19 | 12.6–21.1 |
| P3 Trusted Core | 29 | 29.7–45.2 |
| P4 Missions/Brain | 9 | 6.2–10.2 |
| P5 Review/Completion/Connections | 33 | 36.1–55.5 |
| P6 IDE/debug/CLI agents/bench | 15 | 34.0–60.5 |
| P7 Design Studio | 8 | 9.2–14.7 |
| P8 Containment | 6 | 9.3–14.8 |
| P9 General agent work | 6 | 13.5–22.5 |
| P10 Remote/runner | 5 | 4.7–9.3 |
| **v1 = P−1′…P5** | **111** | **88–137** |
| **All phases** | **151** | **159–259** |

| Component | Tasks | Total pw | of which in v1 |
|---|---|---|---|
| Zain Code Review | 9 | 11.0–16.0 | 9.5–13.5 |
| Zain Engineering System | 8 | 11.2–17.2 | 9.2–14.2 |
| Zain Plan Mode | 10 | 7.1–11.5 | 7.1–11.5 |
| Zain Browser | 10 | 15.5–24.5 | 11.0–17.5 |
| DeskGate | 8 | 5.0–8.5 | 3.6–5.7 |

## §14 Critical path

`A-01 → G-01 → G-03 → B-03 → B-07 → F-01 → F-02 → F-03 → F-11 → F-16 → C-01 → C-02 → C-03 → C-04 → C-09/C-10 → C-20 →
C-22 → M-01 → M-02 → M-07 → V-01 → V-04 → V-08` (v1). Parallelizable off the critical path: F-12/F-14 (P2), C-13..C-19
(P3, after C-04), M-03..M-05 (after C-03), all of P6 after F-16/C-22 except I-04/I-06 (need C-22), P7 after I-05, P8 after C-22.

## §15 Risk contingencies (task-level triggers)

| Trigger | Contingency |
|---|---|
| C-01 > 3 pw or needs Orchestrator rewrite | NO-GO on Option A seams → Option D for executor layer (keep T3 UI), re-estimate |
| B-03 Windows build fails > 2 pw | reopen ADR-001 (build-time) |
| F-15 budgets miss twice | ADR-002 revisit (lazy-load browser/preview; Tauri re-evaluation) |
| C-13 WebAuthn unavailable in Electron on founder hardware | fallback: OS-native confirmation via Core-spawned dialog + TOTP second factor; record weaker claim |
| C-20 invariant failures persist | block P4; fix before missions |
| I-04 debug adapters unstable on Windows | ship JS/Python first; defer others |
| Slippage > 50% on v1 | cut order: W-05, W-02, R-03, I-07, D-07 PPTX |
