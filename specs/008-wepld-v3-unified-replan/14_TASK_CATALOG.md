# 14 — Task Catalog (dependency-ordered, implementation-ready)

```text
STATUS = PROPOSED. No task is authorized until the package is accepted and the task's phase entry gate passes.
FORMAT = | ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est pw | Tier | Reqs |
TIER = T0 docs · T1 UI/product without effect/CI/supply-chain/authority change · T2 everything else (see 08)
TESTS = det = deterministic unit/contract/integration · e2e = Playwright/desktop end-to-end · neg = negative oracle
        (must FAIL with its guard removed — mutation control, 09); coded test ids resolve in 23_ACCEPTANCE_TEST_REGISTRY.md · bench = 09 benchmark ids · R/W = recovery suites (09 §2)
SOURCE_REFS = R11 = research/R11_T3_FILE_MANIFEST.md · R12 = research/R12_DONOR_FILE_MANIFEST.md ·
              R13 = research/R13_IDE_DEBUG_PLATFORM.md · 06 = transplant matrix · 07 = architecture
ESTIMATES = ESTIMATE class (reading-based); all totals are generated (GENERATED_PLAN_REPORT.md)
ENTRY_RULE = every task starts with: spec note under specs/008-*/phases/<P>/ + Ponytail check + tests written first
EXIT_RULE = every task ends with: tests green (incl. mutation control for neg), budgets measured where listed, independent
            review per tier, Build Learning line
```

## P−1′ — Restore CI (founder admin + agent re-run)

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| A-01 | Re-run failed `main` integrity run 36589753362 unchanged | — | `.github/workflows/foundation-integrity.yml` (no edit); precondition: Actions available | Run concludes; result + log archived in `CI_403_REDIAGNOSIS` addendum | CI-01 | 0.05 | T0 | GOV-01 |
| A-02 | If 403 recurs: reproduce `verify-local --remote-baseline` locally with founder token; capture status, `message`, `x-ratelimit-*` | A-01 | `.github/scripts/wepld_integrity.py` (read-only) | Root cause proven (rate limit vs permission) and recorded | local log | 0.1 | T0 | GOV-01 |

## P0 — Governance reset

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| G-01 | Merge this planning package (Draft PR → review → merge by founder) | A-01 | `specs/008-*` | Merged; trusted base updated | integrity green | 0.1 | T0 | GOV-03, GOV-04 |
| G-02 | Founder-only SSH signing key + `allowed_signers` (protected) | — | `.github/allowed_signers` (new) | Signed tag verifies with `git verify-tag` against file | GV-09 | 0.1 | T2 | GOV-02 |
| G-03 | Write `governance_check.py` (single stable checker) + `PROTECTED_PATHS` manifest; run from base via `pull_request_target`, candidate read as data | G-02, G-08 | new `.github/scripts/governance_check.py`, `.github/PROTECTED_PATHS` | Protected-path diff requires a signed co-sign bound to repo id, base, head, tree and changed-path digest (20 §3); ordinary docs/code pass; phase-exit PRs without Build Learning entry fail | det: checker unit tests; GV-09..GV-15; GV-17 | 0.5–1 | T2 | GOV-02, GOV-08, GOV-03, GOV-04 |
| G-04 | Add `GitHubClient` status/rate-limit logging + bounded backoff (only on 403/429 rate-limit) | G-03 | `.github/scripts/governance_check.py` | Rate-limit responses logged with headers; retries bounded | det: mocked 403/429 | 0.2 | T2 | GOV-01 |
| G-05 | Port v1–v72 oracle fixtures into the checker's negative corpus; run positive and negative corpora; retire old workflows only for properties mapped or retired by signed founder decision (20) | G-03, G-08 | `.github/scripts/*` → `docs/historical/governance-successors/` | Every property in the 20 §2 inventory is CARRIED (with passing negative fixture) or RETIRED (signed co-sign + risk record); accepted-PR replay is a non-regression check only | GV-01..GV-08; GV-16; GV-18; GV-19 | 0.5–1 | T2 | GOV-02, GOV-07, GOV-13 |
| G-06 | Governed amendments: invariants "Workers" line (Mirefa/Edara), `MASTER_PLAN_INDEX` → V3, AGENTS.md build-method mechanism text | G-03 | protected docs | Signed co-sign; texts match ADR-011 | GV-09; GV-12 | 0.2 | T2 | GOV-09, GOV-10 |
| G-07 | Enable branch protection + required integrity check on main (repo is PUBLIC, feature now free) | G-03 | GitHub settings (founder) | main protected; required check enforced | GV-20 | 0.1 | T2 | GOV-02 |
| G-08 | Inventory every base-controlled governance property and negative oracle in the 169 successor scripts (v1–v72) into 20 §2 with fixture references | — | `.github/scripts/wepld_*` @0a843a2 (read-only) | Inventory complete: property id, script, oracle, fixture, proposed CARRY/RETIRE | review of inventory (independent) | 0.75–1.25 | T0 | GOV-02, GOV-13 |

## P1 — Donor baseline (isolated, no product code)

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| B-01 | Provision Windows Sandbox/VM baseline image (Node, pnpm, Rust, Git) | G-03 | — | Reproducible setup script; host profile untouched | — | 0.2 | T2 | GOV-07 |
| B-02 | Fetch T3 @36d4d711 and stable v0.1.3 @d2c44031; record tree hashes; mirror tarballs privately | B-01 | R11 §1 | Hashes match R11 pin record | hash check | 0.1 | T2 | GOV-05 |
| B-03 | Build + run T3 desktop (both refs); run test suites; record pass/fail/skip | B-02 | R11 §6 | Pass ratio recorded per area; choose FORK_BASE (default 36d4d711 unless ratio materially worse) | donor suites (recorded pass/fail/skip) | 0.5–1 | T2 | NF-01..03 |
| B-04 | Measure B1–B5 for T3 and Orca @e310a636 | B-03 | 09 §3 | CSV committed; method reproducible | bench B1–B5 | 0.3 | T2 | NF-01..03 |
| B-05 | Measure `synchronous=FULL` cost on T3 receipt table; rusqlite fsync append latency on founder NVMe | B-03 | 07 §4–5 | Numbers recorded; NF-04 budget confirmed or revised | microbench | 0.1 | T2 | NF-04 |
| B-06 | Verify Claude Agent SDK + `claude-agent-acp` load from user-provided location in T3 build; confirm installer exclusion feasible | B-03 | R11 §5 | Feasibility note; G4 path chosen | — | 0.1 | T2 | SEC-13 |
| B-07 | G2 decision record (GO / reopen ADR-001) | B-03..06, C-00 | 00 §7 | Signed founder decision | — | 0.05 | T0 | GOV-03 |
| C-00 | Windows feasibility gate (throwaway spike branch, no product code): Job Object containment incl. ConPTY children; Core-owned approval surface + webauthn.dll assertion verified in Rust; handle-relative no-reparse file ops; Chromium session proxy coverage of all request types | B-03 | 17 §3–§4; 19 §1, §3 | Each spike GO/NO-GO recorded; NO-GO selects the documented weaker claim (17 §4.5) before P3 starts | FG-01..FG-05 | 1.5–2.5 | T2 | SEC-04, SEC-06, SEC-20, SEC-24, SEC-26 |

## P2-N — Zain naming clearance (before F-03)

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| N-01 | Free name-screening memo (R19 checklist; self-search of SAIP, WIPO, USPTO, EUIPO databases) + working-name rule: no public distribution under the name until N-05 | G-01 | research/R19 | Memo recorded; working-name rule in README and installer metadata | review of memo | 0.2 | T0 | GOV-11 |
| N-02 | Choose controlled domain → app ID / AUMID / bundle ids; update ZAIN_NAMING_MIGRATION §2 | N-01 | ZAIN_NAMING_MIGRATION | Development ids use the placeholder `io.github.thehalfmoon.zain`; final ids fixed by N-05 before any public distribution | ID-01 | 0.1 | T0 | GOV-11 |
| N-03 | Package scope + crate names decision (no publishing); collision check vs Zain-LLM | N-01 | R19 | Scope/crates documented; no shared identifiers with Zain-LLM | ID-02 | 0.1 | T0 | GOV-11, GOV-12 |
| N-04 | [P2] Canonical docs + crate rename (`wepld-*` → `zain-*`) as part of G-06 / F-10 | G-06, F-10, N-01 | AGENTS.md, invariants, Cargo.toml | Rust suite green after rename; protected docs signed | det: cargo test | 0.3 | T2 | GOV-11 |

## P2 — Fork, strip, rebrand (usable Zain workbench)

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| F-01 | Import T3 at FORK_BASE into Zain monorepo layout (apps/, packages/, native/) beside `crates/` | B-07, G-03 | R11 §2 KEEP set | Tree equals upstream KEEP set byte-for-byte (manifest hash); source admission record (pin, license, deps, tests) per R11 | SRC-01 | 0.5 | T2 | PR-01, GOV-05, GOV-07 |
| F-02 | Strip: mobile, marketing, relay/T3 Connect, Clerk, PostHog, `.repos/`, unused providers, V1 importer | F-01 | R11 §2 STRIP set | Build + kept tests green at B-03 ratio; no references remain; heic-to (LGPL-3.0), electron-webauthn (no declared license) and @cursor/sdk (custom terms) removed (22 §2) | det: kept suites; grep | 1–2 | T2 | PR-22, SEC-11 |
| F-03 | Identity rename (app id, AUMID, protocol, CLI, data dirs, env prefix, refs, MCP name, hook headers) | F-02, N-02 | R11 §4; 06 §4 | Zero donor identifiers outside NOTICE files | ID-01 | 1–1.5 | T2 | SEC-11 |
| F-04 | Update feed → Zain-hosted Generic provider with ed25519-signed manifest verified by Core (no tokens in client) | F-03, N-02 | R11 §7; R13 §6 | Updater refuses donor manifests; ed25519 manifest check runs in the Server until C-06, then moves to Core | T9 | 0.5–1 | T2 | SEC-11 |
| F-05 | Telemetry removal + idle-egress test | F-02 | R11 §3 | No outbound connections at idle (except user-initiated) | EGR-01 | 0.3 | T2 | PR-22, SEC-11 |
| F-06 | Claude SDK exclusion from installer; user-consented load path; installer-content gate | B-06, F-02 | R11 §3, §5 | Installer contains no `claude-agent-sdk*`; Claude sessions work with user-provided SDK + API key | det: installer-content gate; e2e: Claude session with key; T7; T8 | 0.5 | T2 | SEC-13 |
| F-07 | Default permission mode → Supervised; remove Full access option | F-02 | R11 §3 (RuntimePolicy) | Full access not selectable | e2e; UI-01 | 0.2 | T2 | SEC-06 |
| F-08 | ThreadSettlement → cosmetic archive only | F-02 | R11 §3 | Merge/close never marks a thread "done/settled" | det | 0.2 | T1 | PR-13 |
| F-09 | Protocol version bump (Zain-1) | F-03 | contracts environment.ts (R11) | T3 clients get 426 | det | 0.1 | T2 | SEC-11 |
| F-10 | Rename Core binary `zain-core`; move S2 commands under it; package next to `server.asar` | F-01 | `crates/core`, build scripts (R11 §7) | One `zain` CLI (Server) + `zain-core`; S2 tests green | det: existing 19k-line Rust suite | 0.5 | T2 | PR-01 |
| F-11 | Windows NSIS build, unsigned (development and self-distribution) + notices and license gate | F-03, N-02 | R11 §7 | Installer builds; build fails on a missing notice or an undeclared/LGPL/GPL dependency; unsigned-build limitations (SmartScreen warning, no auto-trust) documented | det: notice gate; LIC-01 | 0.75–1.25 | T2 | PR-21, GOV-06 |
| F-12 | Inherited-bug hardening batch 1: DB writer stalls (#21840, #23482), preview webview memory (#15579), Windows startup (#25262) | F-02 | R02 §13 | Each issue reproduced then fixed or explicitly deferred with limitation | det/e2e per issue | 2–4 | T2 | NF-02, PR-21 |
| F-13 | Effect 4 / orchestration-v2 ramp-up notes (Build Learning) | F-01 | R02 §3 | Seam walkthrough doc for P3 | — | 2–4 (learning, overlaps) | T0 | GOV-08 |
| F-14 | Accessibility pass on kept UI (keyboard, focus, contrast) | F-03 | R13 §7 | Keyboard-complete core flows; screen-reader names, roles and live regions for composer, inbox, approvals and diff summary; terminal screen-reader mode is PR-24b (I-11) | e2e: axe scan; A11Y-01; A11Y-02 | 1.5–2.5 | T1 | PR-24 |
| F-15 | Offline checklist + B1–B3 budget check vs P1 | F-05..F-11 | 09 | NF-01..03 met or exception recorded | bench B1–B3, B12 | 0.3 | T1 | NF-01..03, NF-08 |
| F-16 | P2 exit: install, chat + Codex + ACP + Claude(API key) sessions, worktree, diff, terminal, preview | F-01..F-15, F-17, F-18, Y-00 | — | DoD in 08 P2 | e2e smoke; V1-01; V1-06; TERM-01 | 0.2 | T1 | PR-01..04, PR-08, PR-09 |
| F-17 | Monaco editor surface bound to T3 file/state RPC (moved from I-01 so R0 is a real IDE) | F-03 | R12 D7; R13 §2 | Edit/save 5 MB file within 1 s | EDIT-01; bench | 2–3 | T1 | PR-01, PR-10 |
| F-18 | Retire Tauri shell and glib patch; S2 commands under zain-core; keyring storage audit (secrets only in OS keyring) | F-10 | apps/desktop/src-tauri, third_party/glib-0.18.5-wepld1 | P2: secrets only in OS keyring; Tauri host + glib patch deleted at C-22 exit (after the sidecar is proven under the new shell) | det; SEC12-01 | 0.5 | T2 | PR-01, SEC-12 |

## P3 — Trusted Core (differentiator)

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| C-01 | **G3 spike**: ACP `fs/write` (S3) + Codex approval (S2) via Core with ledger receipts; kill -9 → UNKNOWN | F-16 | R11 §3 (S2, S3), `crates/core` | Spike log; go/no-go recorded | det; spike kill -9 log | 1–2 | T2 | SEC-02, SEC-03 |
| C-02 | Core protocol v2: direction-tagged ids, chunk frames, fencing epoch, data-root OS lock | C-01 | `crates/contracts/src/{frame,protocol}.rs` | v1 tests green + new contract tests | det; T16; PROTO-01 | 1–2 | T2 | SEC-09 |
| C-03 | Ledger (rusqlite, FULL sync, versioned envelope hash over all authoritative fields — 17 §5, projections, tombstones, forward-only migrations, UNSUPPORTED_SCHEMA) | C-02 | new `crates/core/src/ledger/*` | Append/verify/rebuild; hash covers v, seq, ts, kind, project_id, subject_id, principal, payload digest, prev_hash; schema-too-new refusal; audit JSONL export (enterprise seam) | det; R6; R7; W5; B10; T10; LED-01; LED-02; V1-18 | 2.5–3.5 | T2 | SEC-08, NF-06, PR-25, CL-V1-18 |
| C-04 | Effect API: propose/dispatch/report/reconcile/open_dispatches with Spec 006 §19 types | C-03 | `crates/contracts` (reuse PR #343 descriptors where fitting) | logical_operation_id allocated per principal + mission (17 §6); attempts carry separate attempt ids; same operation id with a different input digest → OPERATION_INPUT_CONFLICT; only secret handles cross into Core; effect records carry principal + scope fields | det; EFF-01; T6; OPID-01 | 2–3 | T2 | SEC-02, SEC-03, SEC-12, PR-25 |
| C-05 | Policy engine (Cedar or minimal Rust rules after Ponytail) + permission-mode compilation (Manual/Auto/Skip × per-tool) | C-04 | R12 Cedar | Skip never overrides Blocked; deny-overrides | det; POL-01; T13 | 2–4 | T2 | SEC-01, CL-V1-02 |
| C-06 | CoreBridge service in Server (spawn, health, restart, fail-closed) | C-02 | R11 (ResourceMonitorBinary pattern) | Core down → gated effects refused; one ProcessHost module boundary (implementation C-25); static import guard forbids child_process/node-pty outside it in every package | e2e; W1; PH-07 | 1 | T2 | SEC-01 |
| C-07 | Seam S1 runtime-policy clamp | C-06 | R11 §3 S1 | Mode per Core grant | POL-02 | 0.3 | T2 | SEC-06 |
| C-08 | Seam S3 ACP fs/terminal PEP | C-06, H-08 | R11 §3 S3 | Every ACP fs/terminal effect has receipt | T1; FSG-01 | 1 | T2 | SEC-01 |
| C-09 | Seam S2 provider approvals (Claude PreToolUse→propose+dispatch, canUseTool; Codex handlers; ACP permission) | C-06, C-10 | R11 §3 S2; 03C §2 | Claude, Codex and ACP rows of 18 implemented: provider-side allow rules and session caches disabled, every permission prompt decided by Core; no silent route/model fallback | CC-T01; CC-T02; CC-T03; V1-17; PROV-01; PEM-CLA-01..PEM-CLA-04; PEM-CDX-01..PEM-CDX-04; PEM-ACP-01..PEM-ACP-03 | 2.5–3.5 | T2 | SEC-01, SEC-03, SEC-23, PR-02 |
| C-10 | Seam S4 EffectWorker + S4b recovery gating | C-04 | R11 §3 S4/S4b | No requeue/auto-continue before open_dispatches | R1; W9; B6 | 1.5–2.5 | T2 | SEC-10, NF-05 |
| C-11 | Seam S5 per-run receipt link + compaction exemption | C-03 | R11 §3 S5 | `zain.run-receipts` survives compaction | det; W2 | 1 | T2 | SEC-08 |
| C-12 | Seams S6 MCP access, S7 git destructive ops, S8 terminals | C-06, C-08, C-26 | R11 §3 | Each class mediated with receipts | T2; T4; TERM-02; REC-03; W6 | 1.5–2.5 | T2 | SEC-01, PR-08 |
| C-13 | WebAuthn approvals through a Core-owned approval surface (17 §4): enrollment, recovery code, credential add/replace/remove, canonical operation binding, approval level A1/A2/A3 recorded | C-04, C-00 | 07 §6; R13 | Approval impossible without user presence; displayed text produced by Core, not the renderer; level recorded in every approval and completion record | T3; APR-01..APR-07 | 2–3.5 | T2 | SEC-04 |
| C-14 | Inbox UI (approvals, unknown outcomes, expiries) + trust indicator | C-13 | web app (R11) | Outcomes rendered only from Core | INBOX-01 | 1–1.5 | T1 | PR-23, SEC-05 |
| C-15 | Permission settings UI (modes × per-tool) | C-05 | web app | Matches Claude-like UX; compiled to Core | e2e; V1-02 | 1 | T1 | CL-V1-02 |
| C-16 | Containment floor: data-root/out-of-worktree deny in provider profiles; process trees owned by ProcessHost Job Objects (C-25) | C-07, C-25 | R12 D4; R13 §3 | Agents cannot write data root | PH-01; LED-06 | 1–2 | T2 | SEC-06 |
| C-17 | MEDIATED/UNMEDIATED tagging + reporting paths (PostToolUse, file-hash diffs) | C-09 | 07 §6 | Every receipt tagged | det | 0.5 | T2 | SEC-05 |
| C-18 | Release build without observe mode; signed `core.mode` in dev | C-13 | — | Release binary lacks observe path | T15 | 0.3 | T2 | SEC-15 |
| C-19 | `ledger.anchor` (signed git note/tag) + anchor coverage report exposing the unanchored interval | C-03, G-02 | — | Divergence detected after tamper | LED-03; LED-04; LED-05 | 0.75–1 | T2 | SEC-08 |
| C-20 | Recovery harness: R1, R3–R8, R10, R11 + W1, W2, W4–W6, W9 (mission/continuation scenarios R2, R9, W2b, W3, W7, W8 run in P4/P5 where implemented) | C-10..C-12, C-13, C-16, C-19, C-25, C-26, C-09 | R05 §7; 09 §2 | Invariants I1–I6 100% | R1; R3..R8; R10; R11; W1; W2; W4; W5; W6; W9; T10b; T14; PH-02 | 2–3 | T2 | NF-05 |
| C-21 | Budgets B13 + NF-04 | C-09 | 09 | p95 ≤ 25 ms/effect | B13 | 0.3 | T2 | NF-04 |
| C-23 | Execution coverage model (17 §2): per execution context COVERED/CONTAINED/UNKNOWN for fs, net, proc; tree-provenance reconstruction check; completion inputs | C-17, C-25 | 17 §2 | Unsandboxed interpreters, shells, CLI agents and provider-internal tools yield UNKNOWN; tree provenance computed from mediated receipts | COV-01..COV-05 | 1–1.5 | T2 | SEC-22, PR-13 |
| C-24 | Provider enforcement matrix qualification (18): OpenCode and Pi patched (session approval cache removed, always-allow rules replaced) or excluded from the trusted tier; Core-held grant semantics (scope, expiry, epoch, revocation); provider session restart on revocation where a provider cache cannot be cleared | C-09 | 18; R11 §3.2 | Every provider × operation cell is ENFORCED, UNKNOWN-coverage (labelled) or EXCLUDED; trusted tier lists only qualified cells | PEM-OPC-01..PEM-OPC-03; PEM-PI-01..PEM-PI-03; PEM-GEN-01..PEM-GEN-04 | 1.5–3 | T2 | SEC-23, PR-02 |
| C-25 | ProcessHost (17 §3): Windows native helper creates every launch suspended inside a per-launch nested Job Object (PROC_THREAD_ATTRIBUTE_JOB_LIST), restricted handle inheritance, no breakaway, KILL_ON_JOB_CLOSE, ConPTY through the same path; Linux cgroup v2 + pidfd; macOS process groups labelled not-contained; quiescence attestation before retry | C-06, C-00 | 17 §3; R12 D4 (reference only) | Descendants terminate on Server death; retries blocked until quiescence is proven, else the outcome stays UNKNOWN | PH-01..PH-06 | 2–3.5 | T2 | SEC-24, SEC-06 |
| C-26 | Per-operation reconciliation contracts (17 §1): APPLIED / NOT_APPLIED / UNKNOWN evidence per effect class; CAS ref updates and leased pushes; PR markers; opaque browser/terminal mutations NEVER; retry safety separate from outcome knowledge | C-04, C-25 | 17 §1 | Every effect class has a written evidence contract; inconclusive observation stays UNKNOWN | REC-01; REC-02; REC-04; REC-05 | 1–1.5 | T2 | SEC-02, SEC-25 |
| C-27 | P3-b exit for R2: provider qualification (C-24), DeskGate local (H-01..H-05), enforced Plan Mode read-only (L-02, L-03) + security review | C-22, C-24, H-05, L-03 | — | 08 P3 DoD for the R2 additions | all above | 0.2 | T2 | SEC-17 |
| C-22 | P3 exit for R1 (Trusted Starter scope) + security review (T2) | C-01, C-02, C-03, C-04, C-05, C-06, C-07, C-08, C-09, C-10, C-11, C-12, C-13, C-14, C-15, C-16, C-17, C-18, C-19, C-20, C-21, C-23, C-25, C-26, Y-01, H-08 | — | 08 P3 DoD | all above | 0.3 | T2 | SEC-17 |

## P4 — Missions, Brain, continuations

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| M-01 | Mission model + APIs + thread links (Core) | C-22, C-27 | 07 §2–3 | Missions survive restart/reboot | det; R1 | 1–1.5 | T2 | PR-06 |
| M-02 | Continuations: schedules, wait-for-CI/PR/human, missed-run policy, two-phase fire | M-01 | 05 §4.9 | One fire per condition | det; W2b; W3; V1-05 | 1–2 | T2 | PR-06, SEC-10 |
| M-03 | Brain store: notes, preferences (CANDIDATE→QUALIFIED), spec index (path+blob), FTS5 | C-03 | ADR-006 | Repo specs never stored as authority | det; B14 | 1–1.5 | T2 | PR-05, NF-07 |
| M-04 | Capsule injection + `brain.query` MCP tool | M-03 | R11 (injectHistory/system prompt seam) | Capsule ≤ 2k tokens default | det; B8 | 0.5–1 | T2 | PR-07 |
| M-05 | Compaction capsule capture; continue-as-new for long missions | M-04 | 05 §4.8 | Recall on non-pinned decisions measured | W8; B8 | 0.5–1 | T2 | PR-07 |
| M-06 | Missions + Brain UI (Projects, Work views) | M-01..M-03 | 07 §7 | Edit/supersede/incognito | e2e; V1-03; V1-04 | 1–1.5 | T1 | PR-05, PR-06 |
| M-07 | P4 exit (mission survives reboot, resumes on CI) | all P4 | — | 08 P4 DoD | e2e; R2; R9 | 0.2 | T1 | PR-06 |

## P5 — Review, Trusted Completion, Connections

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| V-01 | Reviewer route ≠ builder route enforcement; per-role pins | C-22 | 07; ADR-008 | Same-route reviewer refused | POL-03 | 0.5 | T2 | PR-03, PR-12 |
| V-02 | SUPERSEDED by K-04/K-05 (Zain Code Review findings panel + dispositions) | V-01 | T3 diff panel (R11) | Findings tracked to resolution | e2e | 0 | T1 | PR-12 |
| V-03 | SUPERSEDED: PR-Agent wrap replaced by Zain Code Review engine (K-*); PR-Agent reference only | V-01 | R12 D22 | Runs with user's key; output as findings | det | 0 | T2 | PR-12 |
| V-04 | Completion evaluate/decide (rules 1–10 + UNMEDIATED handling) + Stop/SubagentStop gating | K-04, C-23, M-01 | Spec 006 §20; 03C | Merge ≠ completion; UNKNOWN blocks; COMPLETED_TRUSTED only with tree provenance complete and required coverage known (17 §2) | CC-T05; V1-07; W7; COV-06 | 1–1.5 | T2 | PR-13 |
| V-05 | MCP connections (local/remote OAuth) with per-tool grants | C-22, C-27 | R12 D13; T3 /mcp | Revoked token → blocked_on_auth | V1-09; T4 | 1–1.5 | T2 | PR-14 |
| V-06 | Agent Skills (SKILL.md) loader, hash pinning, re-review on update | V-05 | 03C; census CL-E-006 | Widening update disabled until re-approved | T5; V1-08 | 0.5–1 | T2 | PR-14 |
| V-07 | MCPB extension install with manifest review | V-05 | census CL-E-031 | Unknown extension requires explicit trust | V1-10 | 0.5–1 | T2 | PR-14 |
| V-08 | P5 exit: Astro "first complete loop" E2E | all P5 | — | Loop runs locally | e2e | 0.3 | T1 | PR-01, PR-03, PR-04, PR-12, PR-13 |
| X-01 | [P5] R1 release exit (Zain Trusted Starter): bounded-claims statement (21 §3) shown in app and docs; trust indicator shows claim and approval level; all R1 registered suites green with mutation control; independent review | C-22, V-01, K-04, K-05, K-08, L-01 | 21 §3 | Claims text equals 21 §3; no claim beyond it in UI or docs | e2e; ZCR-T04; ZCR-T14..ZCR-T17; ZCR-T22; ZCR-T29 | 0.3 | T2 | SEC-05, GOV-03 |

## P6 — IDE breadth, debugging, CLI agents, benchmarks

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| I-01 | SUPERSEDED by F-17 (Monaco moved to P2) | F-16 | R12 D7; R13 §2 | Edit/save large files ≤ 1 s for 5 MB | e2e; bench | 0 | T1 | PR-10 |
| I-02 | Diff comments port (Orca) | F-17 | R12 D7 | REWRITE behind an adapter (R12 D7: 489-module closure); comments anchored across edits | e2e | 2–3.5 | T1 | PR-10 |
| I-03 | LSP: 1-week spike @vscode/monaco-lsp-client vs monaco-languageclient behind a wrapper; server lifecycle in Server (TS 7 `tsc --lsp`, Python, rust-analyzer, gopls); untrusted-repo mode disables code-running features; spawns are `process.spawn.language_server` effects | F-17 | R13 §2 | Diagnostics, go-to-def, hover per language | e2e per language | 6–10 | T2 | PR-10 |
| I-04 | Debugging: DAP client + debug UI; adapters (js-debug, debugpy, CodeLLDB/lldb-dap, Delve); launches as Core-gated process effects; agent-readable debug state via MCP | F-17, C-22 | R13 §1 | Breakpoints/step/variables in 4 languages; launch receipts; effect classes process.spawn.debug_adapter / process.spawn.debuggee / process.attach.debug (always approval) / debug.evaluate; debugpy from user env (EPL pydevd not bundled) | DBG-01; DBG-02 | 6–10 | T2 | PR-11 |
| I-05 | Design Mode capture → composer (Orca port) | F-16 | R12 D2 | Element payload with DOM path, styles, crop | e2e; DM-01; DM-02; DM-03 | 3–6 | T2 | PR-15, PR-18 |
| I-06 | CLI-agent catalog + hook/OSC 7501 status (overlays + authenticated endpoint) | C-22 | R12 D3 | Status detected; user global configs untouched | T17 | 3–5 | T2 | PR-09, SEC-14 |
| I-07 | Linear integration (Orca port) | V-05 | R12 D5 | Issue → mission link | det fixtures | 2–4 | T2 | PR-08 |
| I-08 | Benchmark harness + public results (B6–B13) | C-22 | R12 D23; 09 | Raw data published | B7; B11 | 1–2 | T2 | NF-09 |
| I-09 | macOS + Linux packaging (unsigned/ad-hoc signed DMG, AppImage/deb) + per-OS update channels | F-11 | R13 §6 | Installs and runs P2 smoke on each OS; notarization is PD task I-12 | e2e smoke | 3.5–6.5 | T2 | PR-21 |
| I-10 | Local OTel sink (observational only) | C-22 | 03C | No egress; spans not evidence | det | 0.3–0.5 | T1 | PR-22 |
| I-11 | Accessible terminal mode (xterm.js screenReaderMode alternative to Canvas renderer) + WCAG 2.2 AA audit of IDE surfaces | F-14, F-17 | R13 §7 F5 | Screen reader reads terminal output; AA checklist passes | A11Y-03 | 2–5 | T1 | PR-24b |

## P7 — Design Studio v1

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| D-01 | Canvas (iframe artboards, pan/zoom, multi-artboard) | I-05 | R03B §5 | Artboards render live preview | AT-01; AT-03; AT-11 | 2–3 | T1 | PR-15 |
| D-02 | Isolated preview origin | D-01 | R03B §5; SEC-16 | No access to Server/Core | T11; AT-20 | 0.5–1 | T2 | SEC-16 |
| D-03 | Element→source resolver (3 tiers) | D-01 | R12 D20 | EditTarget with confidence; ambiguity prompts user | AT-04 | 2–3 | T2 | PR-15 |
| D-04 | Layer tree + token-aware properties panel | D-03 | R03B §7 | Edits map to source or tokens | AT-05; AT-13 | 1–2 | T1 | PR-15 |
| D-05 | Comments → agent proposal → Core grant → patch → refresh; op-log history + undo | D-03, C-22 | R03B §7.4–7.5 | Stale-write refusal | AT-06; AT-07; AT-14; AT-15 | 1.5–2.5 | T2 | PR-15 |
| D-06 | DTCG token store + design-system registry + pins (Style Dictionary) | D-04 | R12 D21 | Round-trip tokens | AT-02; AT-08; AT-09; AT-12 | 1–1.5 | T2 | PR-15 |
| D-07 | Exports HTML/zip/PNG/PDF; Excalidraw sketch layer | D-01 | R12 D19 | Export fidelity checks | AT-10 | 1–1.5 | T1 | PR-15 |
| D-08 | P7 exit: AT-01..AT-15 on Windows | all P7 | — | All P0 AT green | AT-01..AT-15; V1-12 | 0.2 | T1 | PR-15 |

## P8 — Containment (OS sandbox)

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| S-01 | Port codex Windows sandbox set into Core launcher | C-22 | R12 D9; R13 §3 | Provider runs under sandbox; fs/network rules enforced; Codex Windows backends are restricted-token / elevated sandbox users + WFP service / MXC — not AppContainer (R13 F3); admission per 22 §3: windows-sandbox-service reference only (needs codex-core); bubblewrap not vendored (LGPL-2.0); `rama` pre-release pinned or replaced | escape suite (Win) | 4–8 | T2 | SEC-07 |
| S-02 | Linux sandbox (landlock/seccomp/bwrap) | S-01 | R12 D9 | Same rules on Linux | escape suite (Linux) | 2–3 | T2 | SEC-07 |
| S-03 | macOS Seatbelt profiles | S-01 | R12 D9; R13 §3 | Same rules on macOS | escape suite (mac) | 2–3 | T2 | SEC-07 |
| S-04 | Network egress proxy with allowlist + approvals | S-01 | R12 D9 network-proxy | Unapproved egress blocked | T2 | 1.5–2.5 | T2 | SEC-07 |
| S-05 | Re-enable Full-access lane inside sandbox; trust indicator upgrade | S-01..S-04 | 07 §6 | Claim widens only after escape suite passes | e2e | 0.3 | T2 | SEC-05 |
| S-06 | Debug sandbox profile (ptrace/process_vm allowed for debuggee only) on Linux/macOS/Windows | S-02, I-04 | R13 F4 | Debugging works inside sandbox without widening agent profile | SBX-01 | 0.5–1 | T2 | SEC-07, PR-11 |

## P9 — General agent work

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| W-01 | Documents/artifacts as project files; preview; export MD/HTML/PDF | V-08 | T3 file previews (R11) | One-pager → PDF | e2e; V1-11 | 1–2 | T1 | PR-16 |
| W-02 | PPTX/XLSX generation (permissive libs after Ponytail) | W-01 | R13 | Opens in Office/LibreOffice | det | 1–2 | T2 | PR-16 |
| W-03 | Research task type with citations as evidence | M-07 | — | ≥3 cited sources stored | e2e; V1-13 | 1–1.5 | T2 | PR-17 |
| W-04 | SUPERSEDED by Y-* (Zain Browser); general-web lane = Y-09 | S-04 | R13 §4; R11 | Form fill on localhost; payments refused; T3 already drives pages via Playwright connectOverCDP (CdpRelay.ts) + 12 preview_* MCP tools; work = gating incl. redirects (Playwright MCP is not a security boundary) | neg T12; V1-14 | 0 | T2 | PR-18 |
| W-05 | Computer use (Windows first) behind per-session grants | S-01 | R12 D6; R13 §5 | Approved actions only; Orca helpers: macOS Swift (AX, ScreenCaptureKit, CGEvent; TCC grants), Windows PowerShell UIA/SendInput → replace ExecutionPolicy Bypass with signed helper, Linux AT-SPI/xdotool X11 only | T12; V1-15 | 6–10 | T2 | PR-19 |

## P10 — Remote and runner

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| R-01 | Headless runner (`zain serve`) + Linux service; Windows service wrapper | M-07 | R13 §6 | Runner survives reboot; Windows service via Rust `windows-service` crate, non-SYSTEM account, no desktop features in service mode | e2e | 1–2 | T2 | PR-20 |
| R-02 | Project-home rule + export/import bundles | R-01 | 07 §5; 05 §4.7 | Grants dropped; dispatches UNKNOWN on new home | det | 1–2 | T2 | PR-20 |
| R-03 | Passkey pairing for phone/web approvals | C-13, R-01 | 05 §7.1 | Guest links cannot approve | V1-16 | 1–2 | T2 | PR-20, SEC-04 |
| R-04 | Web client hardening for LAN/Tailscale | R-01 | R11 (client-runtime) | Scoped sessions only | RMT-01 | 1–2 | T2 | PR-20 |

## PD — Optional distribution track (paid; never a dependency of a mandatory task)

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| N-05 | Trademark counsel opinion + SAIP filing for the product name (paid; required before public distribution under the name) | N-01 | R19 | Written clearance or rename | review | 0.2–0.5 | T0 | GOV-11 |
| F-19 | Windows code signing for public distribution (OV/EV certificate + cloud HSM, jsign) | F-11, N-05 | R13 F1 | Signed installer; SmartScreen reputation path documented | det: signature verify | 0.5–1 | T2 | PR-21 |
| I-12 | macOS notarization (Apple Developer Program, paid) | I-09 | R13 §6 | Notarized DMG passes Gatekeeper | det: spctl assess | 0.3–0.5 | T2 | PR-21 |

## Product components (cross-phase; the `[Px]` tag is the phase used for totals)

### Zain Code Review (16_*, research/R14) — OCR engine fork + Zain-owned UX and authority

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| K-01 | [P2] Optional spike: build forked OCR engine on Windows; engine mode on the Zain repo with a local Ollama route; advisory, read-only | F-03, E-00 | R14 §11; alibaba/open-code-review@375f64cd | Findings shown, labelled advisory; no fixes; admission-lite record (pin, license) before running | ZCR spike log | 0.5–0.75 | T2 | PR-26 |
| K-02 | [P6] Engine admission: pin, SBOM + transitive license scan, notices, Go toolchain in CI (Win/Linux/mac) | K-07 | R14 §9 | Source admission record; notices generated | det: license gate | 0.5–0.75 | T2 | PR-26, GOV-07 |
| K-03 | [P6] Fork-vendor `native/zain-review-engine` + patches Z-P1..Z-P7 (route lock, HOME isolation, branding, Z-P7: every tool confined to the snapshot allowlist manifest) + upstream suite green | K-02 | R14 §5–6 | Upstream tests green; ambient config cannot override the route | ZCR-T05; ZCR-T23; ZCR-T24; ZCR-T26 | 1–1.5 | T2 | PR-26, SEC-18 |
| K-04 | [P5] Review core: findings schema, normalizer/fingerprint/anchors, contracts/ledger kinds, route rule (reviewer ≠ builder), review snapshot builder (immutable, secret-screened, allowlist manifest — 19 §2) | C-22, V-01 | R14 §7 | One finding schema for delegated and engine modes; same model under another account is NOT independent; snapshot contains only approved files | ZCR-T04; ZCR-T14; ZCR-T25 | 1.75–2.5 | T2 | PR-12, PR-26 |
| K-05 | [P5] IDE UX: findings panel, Monaco markers, filters, accept/dismiss/false-positive, sanitized renderer | K-04, F-17 | R14 §7 | Model text never rendered as trusted markdown | ZCR-T15 | 1.5–2 | T1 | PR-26 |
| K-06 | [P5] Fix pipeline: proposals, preimage OID check, checkpoint, Core-granted apply, undo, verification profile | K-04, C-12 | R14 §7 | Stale fix refused; undo restores; tests run after apply in a disposable copy; patches touching verify config, test commands or CI files rejected; exact argv shown in the proposal; config under `.zainide/` | ZCR-T07; ZCR-T08; ZCR-T09; ZCR-T10; ZCR-T11; ZCR-T28 | 1.5–2 | T2 | PR-26, SEC-02 |
| K-07 | [P5] Delegated-mode acceptance suite + guard-mutation job + reviewer-quality qualification (held-out defects, false positives, injection suppression) | K-04, K-05, K-06, K-08, V-04 | R14 §8 | All pass; each guard test fails with its guard removed | ZCR-T04; ZCR-T07..ZCR-T17; ZCR-T22; ZCR-T25; ZCR-T28; ZCR-T29; ZCR-Q01..ZCR-Q03 | 1.25–2 | T2 | PR-26, SEC-17 |
| K-08 | [P5] Delegated review mode (default, engine-free): MCP reporting tools; reviewer session = provider thread on a pinned independent route; cwd = review snapshot; reads confined to the snapshot allowlist | K-04, C-09 | R14 §11 (P5b) | Reviewer session cannot write or read outside the snapshot | ZCR-T16; ZCR-T17; ZCR-T29 | 1.75–2.5 | T2 | PR-26 |
| K-09 | [P6] CI action + SARIF + scan mode + mediated model proxy for cloud review routes (endpoint allowlist, per-run budget, payload digests, per-run approval) | K-11 | R14 §11 | CI summary; egress mediated | ZCR-T21; ZCR-T27 | 1.5–2.5 | T2 | PR-26 |
| K-10 | [P6] Engine mode integration: EngineRunner via ProcessHost on the review snapshot only; local model routes only | K-03, K-07 | R14 §5–§7; 19 §2 | Engine reads only the snapshot; no cloud route selectable before K-09 | ZCR-T01; ZCR-T02; ZCR-T03; ZCR-T19; ZCR-T20 | 1–1.5 | T2 | PR-26, SEC-27 |
| K-11 | [P6] Engine qualification: engine suite + comparative evaluation vs delegated mode on the held-out corpus; productize the engine only if it wins (decision record) | K-10 | R14 §8; 23 | Decision record with raw numbers | ZCR-T06; ZCR-T18; ZCR-Q01..ZCR-Q04 | 0.75–1.25 | T2 | PR-26 |

### Zain Engineering System (16 §3, research/R15) — PStack-derived loop + Playwright E2E

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| E-00 | [P1] Donor pin snapshot + license records (PStack, cursor-team-kit, Ascout candidate) | B-01 | R15 §10 | Pins + LICENSE hashes recorded | hash check | 0.2 | T0 | GOV-05 |
| E-01 | [P5] Skill pack adaptation into `packages/skills/zain-engineering` (router, playbooks, principles, agents, CTK skills), notices, identifier scrub | V-06 | cursor/plugins@ab1f702c pstack/ | No PStack/Cursor names in product; notices present | ES-AT-02; ES-AT-03; ES-AT-04 | 2–3 | T2 | PR-27, GOV-06 |
| E-02 | [P5] Core evidence kinds + completion rules ES-1..ES-7 + patch-id staleness | V-04 | R15 §7 | INCONCLUSIVE never PASS; verdict stale after patch change | ES-AT-06; ES-AT-08; ES-AT-16 | 1–1.5 | T2 | PR-27, PR-13 |
| E-03 | [P5] `zain-browser-verify` E2E (Playwright, isolated partition, localhost-only origin policy) — source UNRESOLVED (Ascout candidate) pending founder FO-9 | C-22, Y-03, Y-05, Y-08, Y-10, C-27 | R15 §6–7 | Evidence hashed into Core; no user profile touched | ES-AT-09; ES-AT-10 | 3–5 | T2 | PR-27, PR-28 |
| E-04 | [P5] verify-skill generator into `.zainide/skills` + dogfood on Zain | E-01, E-03 | R15 §10 | Generated skills pass checks | det; ES-AT-14 | 1–1.5 | T2 | PR-27 |
| E-05 | [P5] Review lanes (independent routes, comment reviewer, deslop) feeding Zain Code Review findings | K-04 | R15 §10 | Same schema as K-04; no second review store | det | 1–2 | T2 | PR-27, PR-26 |
| E-06 | [P6] PR babysit/shipping (gated merges) | E-02, E-05 | R15 §10 | Merge requires a Core grant; merge ≠ completion | ES-AT-17 | 2–3 | T2 | PR-27 |
| E-07 | [P5] Acceptance suite ES-AT-01..16 + tie into V-08 | E-01, E-02, E-03, E-04, E-05 | R15 §9 | Suite green with mutation control | ES-AT-01..ES-AT-16 | 1 | T2 | PR-27, SEC-17 |

### Zain Plan Mode (16 §4, research/R16) — mattpocock/skills (MIT) + T3 plan mode + Core read-only profile

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| L-01 | [P2] Inherit T3 plan mode under Zain brand; verify enforcement; label "not yet enforced" | F-16 | R16 §7 PL-01 | Plan thread renders the proposed plan | e2e | 0.3–0.5 | T1 | PR-29 |
| L-02 | [P3] `PLAN_READONLY` Core profile bound to plan path + base commit | C-05, C-07, C-08, C-09, C-12, H-08 | R16 PL-02 | MEDIATED writes outside the plan path denied | N1..N8; N15; N16; D1 | 1–1.5 | T2 | PR-29, SEC-19 |
| L-03 | [P3] Turn-end out-of-path diff → INVALIDATED; CLI agents blocked in plan mode | C-17, C-23, L-02 | R16 PL-03 | Violation blocks approval | N9; N10; COV-07 | 0.5 | T2 | PR-29, SEC-19 |
| L-04 | [P4] Plan artifacts + Brain index + `plan.lock.json` | M-03, L-02 | R16 PL-04 | Lock covers all artifacts | D2; D3 | 0.5–1 | T2 | PR-29 |
| L-05 | [P4] Approve plan → start mission (WebAuthn) | M-01, C-13, L-04 | R16 PL-05 | No mission without lock + assertion | N11; N12 | 0.5 | T2 | PR-29 |
| L-06 | [P5] `packages/skills/zain-plan` copy/adapt (mattpocock/skills@59db609e) + NOTICE + manifest | V-06 | R16 §5 | Hashes match manifest | D4; D5; N13 | 1–1.5 | T2 | PR-29, GOV-06 |
| L-07 | [P5] `tasks.dag.json` handoff contract shared with the Engineering System | L-04, E-01 | R16 PL-07 | Engineering consumes the DAG without re-parsing prose | D6 | 0.3–0.5 | T2 | PR-29, PR-27 |
| L-08 | [P5] Plan UI: canvas, question loop, decision cards, DAG view, approve bar | L-04 | R16 PL-08 | Recommended answers logged | E1; E2; E4 | 2–3.5 | T1 | PR-29 |
| L-09 | [P5] Critic route ≠ griller route; findings in the Code Review schema; readiness gate | V-01, K-04 | R16 PL-09 | Same-route critic refused | N14; E5 | 0.5–1 | T2 | PR-29 |
| L-10 | [P5] Plan Mode acceptance suite + mutation control | L-01, L-02, L-03, L-04, L-05, L-06, L-07, L-08, L-09 | R16 PL-10 | Negatives fail with their guard removed | N1..N16; D1..D6; E1..E5 | 0.5–1 | T2 | PR-29, SEC-17 |

### Zain Browser (16 §5, 19 §1, research/R17) — one BrowserController, four lanes

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| Y-00 | [P2] Strip T3/Orca browser-cookie import; isolate agent partition; disable eval outside Preview; relay method allowlist | F-02 | R17 §5, WB0 | No code path reads user browser stores | BRW-AT-04; BRW-AT-14; BRW-G01 | 0.5–1 | T2 | PR-28, SEC-20 |
| Y-01 | [P3] Browser effect classes + hard-block floor rules registered in Core | C-05, C-12 | R17 WB4 (part) | Payments/credentials/account creation/executable downloads blocked even in Skip; until Y-02 the inherited preview_* MCP tools are gated by C-12 seam S6 | BRW-P01; BRW-P02 | 0.5–1 | T2 | PR-28, SEC-20 |
| Y-02 | [P5] Controller unification (broker → BrowserController; lanes Preview/Agent/Test) + Playwright 1.64 bump | Y-01 | R17 WB1 | Single controller; MCP/CLI/UI are thin front-ends | det; BRW-AT-19 | 1.5–2.5 | T2 | PR-28 |
| Y-03 | [P5] Navigation/redirect approval gate (Electron + CDP Fetch, document hops) | Y-02, Y-10 | R17 WB2 | Document hops to ungranted origins held before the request; this is the approval/UX layer — connection enforcement is Y-10; Agent lane uses external origins only when the Y-10 suite passes, else loopback project origins only | BRW-AT-02; BRW-AT-11; BRW-AT-12 | 2–3 | T2 | PR-28, SEC-20 |
| Y-04 | [P5] Page classifier + hard blocks + download quarantine | Y-03 | R17 WB3 | Executable download quarantined | BRW-AT-01; BRW-AT-03; BRW-AT-07; BRW-AT-08; BRW-AT-15; BRW-AT-21 | 1.5–2.5 | T2 | PR-28, SEC-20 |
| Y-05 | [P5] Core integration: grants, receipts with replay classes, Inbox UX | Y-02, C-14, C-26 | R17 WB4 | Every action has a receipt; replay classes per 17 §1 (text input and clicks NEVER) | BRW-AT-16; BRW-AT-17; BRW-AT-18 | 1.5–2 | T2 | PR-28, SEC-02 |
| Y-06 | [P5] Evidence: screenshots, HAR-from-CDP, redaction, tracing, export | Y-05 | R17 WB5 | No secrets in evidence | BRW-AT-05; T6 | 1.5–2.5 | T2 | PR-28 |
| Y-07 | [P5] Session recovery + takeover UX + prompt-injection measures | Y-05 | R17 WB6 | Human takeover for sign-in; injection suite passes | BRW-AT-09; BRW-AT-10 | 1–1.5 | T2 | PR-28 |
| Y-08 | [P5] Test lane endpoint (loopback) + mutation-controlled suite | Y-03, Y-04, Y-05, Y-06, Y-07, Y-10 | R17 WB7 | Suite green; each guard test fails without its guard | BRW-AT-01..BRW-AT-22; BRW-AT-25..BRW-AT-29; V1-14 | 1–1.5 | T2 | PR-28, SEC-17 |
| Y-09 | [P9] General web in Agent lane + user-session lane (MV3 extension) + Claude browser_toolset adapter | Y-08, S-04 | R17 WB8–WB9 | Opt-in, tab-group scoped; agent never reads password manager, autofill or enters credentials | BRW-AT-23; BRW-AT-24 | 4.5–7 | T2 | PR-28, PR-18 |
| Y-10 | [P5] Connection-level browser egress proxy (19 §1): agent/test partitions forced through a Server loopback proxy (`<-loopback>` bypass rule), proxy resolves, validates and connects to the validated IP, WebRTC non-proxied UDP disabled; covers fetch/XHR/WebSocket/workers/beacons/subresources/redirects | Y-02, C-00 | 19 §1 | Forbidden sinks receive zero requests across all request types; a DNS change between validation and connect cannot redirect a connection | BRW-AT-25..BRW-AT-29 | 1.5–2.5 | T2 | SEC-20, PR-28 |

### DeskGate (16 §6, 19 §3, research/R18) — Desktop Commander tools as Core-mediated adapters

| ID | Task | Deps | Source / files | Acceptance criteria | Tests | Est | Tier | Reqs |
|---|---|---|---|---|---|---|---|---|
| H-00 | [P1] Registry row + license admission for DesktopCommanderMCP@db3430f2; remote-desktop-commander recorded EXCLUDED (proprietary) | B-01 | R18 §1 | Admission record | review | 0.1–0.2 | T0 | PR-30, GOV-07 |
| H-01 | [P3] `packages/deskgate` on Server `/mcp`; schemas port; static-import guard (no own spawn/config) | C-06, C-12 | R18 §4 | DeskGate cannot spawn outside the Server host | DG-N10 | 0.5–1 | T2 | PR-30, SEC-21 |
| H-02 | [P3] fs adapters (read/list/write/edit/move/mkdir) via Core effects | H-01, H-08 | R18 | Every fs effect has a receipt | DG-N01; DG-N02; DG-N04; OPID-02 | 1–1.5 | T2 | PR-30 |
| H-03 | [P3] Process/terminal adapters on the single node-pty host; ownership-scoped signals; `set_config_value` refused | H-01 | R18 | Kill limited to Zain-owned process trees; terminal.input proposals carry redacted plaintext, replay class NEVER, approval required by default for interpreter/shell sessions; interpreter/shell sessions set the execution context coverage to UNKNOWN (17 §2) | DG-N06; DG-N07; DG-N08; DG-P04 | 1–1.5 | T2 | PR-30, SEC-21 |
| H-04 | [P6] Search adapters (rg as spawn effect) | H-01 | R18 | Results paged; spawn receipted | det | 0.5–1 | T2 | PR-30 |
| H-05 | [P3] Negative/mutation suite DG-N01..N14 + perf DG-B1..B9 | H-02, H-03, C-13 | R18 §5 | Suite green; adapter overhead p95 ≤ 5 ms | DG-N01..DG-N11; DG-N13..DG-N16; DG-B1..DG-B9 | 1–1.5 | T2 | PR-30, SEC-17 |
| H-06 | [P10] Remote DeskGate via runner/project-home + passkey | R-01, R-02, R-03 | R18 | No third-party relay | DG-N12; DG-P07 | 0.7–1.3 | T2 | PR-30, PR-20 |
| H-07 | [P6] Cross-OS parity (macOS/Linux) | H-05, I-09 | R18 | Parity matrix green | e2e | 0.2–0.5 | T2 | PR-30 |
| H-08 | [P3] fs-gate native helper (19 §3): handle-relative, no-follow/reparse-rejecting file operations (Windows NtCreateFile relative to a held root handle + FILE_FLAG_OPEN_REPARSE_POINT + final-path check; Linux openat2 RESOLVE_BENEATH and RESOLVE_NO_SYMLINKS; macOS openat walk with O_NOFOLLOW); handle-relative atomic rename; the single write path for ACP fs, DeskGate, Plan Mode and review fixes | C-06, C-00 | 19 §3 | No write reaches a target other than the validated one under concurrent link swaps | FSG-01..FSG-04 | 1.5–2.5 | T2 | SEC-26, SEC-21 |

## §13–§14 Totals and critical paths

Generated — see `GENERATED_PLAN_REPORT.md` (tools/plan_graph.py). Hand-written totals and paths were removed
(Astro H-12): every number in the package is produced from the rows above and the test registry (23).

## §15 Risk contingencies (task-level triggers)

| Trigger | Contingency |
|---|---|
| C-01 > 3 pw or needs Orchestrator rewrite | NO-GO on Option A seams → Option D for executor layer (keep T3 UI), re-estimate |
| B-03 Windows build fails > 2 pw | reopen ADR-001 (build-time) |
| F-15 budgets miss twice | ADR-002 revisit (lazy-load browser/preview; Tauri re-evaluation) |
| C-00 FG-02/FG-03 NO-GO | approval level A2 (isolated Electron approval window) or A3 (TOTP) per 17 §4.5; the weaker claim is recorded and shown; never silently treated as A1 |
| C-20 invariant failures persist | block P4; fix before missions |
| I-04 debug adapters unstable on Windows | ship JS/Python first; defer others |
| Slippage > 50% on R2 | defer to R3 (never delete): E-04, E-05, Y-06, Y-07, L-08 to minimal UI, then E-03 (if FO-9 unresolved); R1 scope is not cut — its claims shrink instead (21 §3) |

## §16 Release membership (machine-read by tools/plan_graph.py)

| Release | Name | Definition |
|---|---|---|
| R0 | Zain Workbench (no authority claims) | phases: P−1′, P0, P1, P2-N, P2 |
| R1 | Zain Trusted Starter (small first trusted release) | R0 + tasks: C-01, C-02, C-03, C-04, C-05, C-06, C-07, C-08, C-09, C-10, C-11, C-12, C-13, C-14, C-15, C-16, C-17, C-18, C-19, C-20, C-21, C-23, C-25, C-26, Y-01, H-08, C-22, V-01, K-04, K-05, K-08, X-01 |
| R2 | Zain v1 | R1 + phases: P3, P4, P5 |
| R3 | IDE breadth, CLI agents, OCR engine lane | R2 + phases: P6 |
| R4 | Design Studio | R3 + phases: P7 |
| R5 | OS containment | R4 + phases: P8 |
| R6 | General agent work | R5 + phases: P9 |
| R7 | Remote and runner | R6 + phases: P10 |

PD tasks are optional, paid and outside every release; no mandatory task depends on them.
