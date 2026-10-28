# 13 — Requirements Register (V3)

```text
PURPOSE = every material requirement has an ID; 15_TRACEABILITY_MATRIX.md maps each to ≥1 task (14_TASK_CATALOG.md)
          and ≥1 acceptance test. A requirement without a task+test is a planning defect.
SOURCES = founder mission briefs (2026-10-27, three messages), ARCHITECTURE_INVARIANTS.md, 00–12 of this package,
          03F (Claude parity), R03B (Design AT-01..23), 09 (threats, recovery, benchmarks)
PRIORITY = M (must for v1 = P−1′…P5) · S (should, post-v1 phase named) · C (could/backlog, accounted only)
```

## A. Product capabilities

| ID | Requirement | Pri | Phase |
|---|---|---|---|
| PR-01 | One desktop app combining IDE and AI workspace (chat, code sessions, files, terminal, browser preview, review) under the Zain brand | M | P2 |
| PR-02 | Run Claude, Codex, ACP-family agents, OpenCode, Pi and local models as replaceable workers; no silent fallback. Trusted tier = only provider × operation cells qualified in 18 (initially Claude, Codex; ACP per agent); OpenCode and Pi run as labelled untrusted (UNMEDIATED) workers until C-24 qualifies them | M | P2/P3 |
| PR-03 | Multi-agent orchestration: parallel sessions in isolated worktrees, subagents, steer/interrupt/resume, per-role model pins (reviewer ≠ builder) | M | P2/P5 |
| PR-04 | Unified composer that escalates chat to task with visible plan and resume | M | P2/P4 |
| PR-05 | Projects with instructions, knowledge files, isolated memory; Brain indexes repo specs | M | P4 |
| PR-06 | Durable missions with continuations (schedules, wait-for-CI/PR/human), missed-run policy | M | P4 |
| PR-07 | Context survives model/provider switch and compaction (capsules) | M | P4 |
| PR-08 | Git: worktrees, checkpoints, diff review with inline comments, PR/CI tracking; destructive git ops gated | M | P2/P3 |
| PR-09 | Terminals: integrated PTYs on Windows (spawn, input, output, resize, kill — TERM-01 at P2; Zain-issued commands mediated — TERM-02 at P3); CLI agents in terminals with status detection, labelled UNMEDIATED (S, P6) | M (terminal) / S (CLI agents P6) | P2/P3/P6 |
| PR-10 | Code editor (Monaco) with diff comments; LSP for TS/Python/Rust/Go | S | P6 |
| PR-11 | Debugging via Debug Adapter Protocol (Node/browser, Python, Rust/C++, Go); debug launches are gated effects; agent-readable debug state | S | P6 |
| PR-12 | Code review: independent reviewer worker, findings schema, finding → repair proposal loop | M | P5 |
| PR-13 | Trusted Completion: decision over evidence; merge/CI ≠ completion; UNMEDIATED-only changes cannot be COMPLETED_TRUSTED | M | P5 |
| PR-14 | Skills (SKILL.md), plugins, MCP (local/remote OAuth), MCPB extensions with manifest review and hash pinning | M (MCP, skills) / S (MCPB) | P5 |
| PR-15 | Design Studio: canvas, element→source mapping, comments → agent proposals, DTCG tokens, design-system registry, exports, IDE handoff | S | P7 |
| PR-16 | Documents/artifacts: generate, preview, export (MD/HTML/PDF; PPTX/XLSX later) as project files | S | P9 |
| PR-17 | Research tasks with stored citations as evidence | S | P9 |
| PR-18 | Controlled browser automation in the in-app browser; hard-blocked categories (payments, credentials, account creation) | S | P9 |
| PR-19 | Controlled computer use (Windows first, then macOS/Linux) behind per-session grants | C→S | P9 |
| PR-20 | Self-hosted runner as project home; phone/web approvals via passkey | S | P10 |
| PR-21 | Windows x64 primary; macOS and Linux packages | M (Win) / S (mac, Linux) | P2/P6 |
| PR-22 | Local-first: core works offline; zero mandatory cloud; BYO credentials only | M | P2 |
| PR-23 | Inbox for approvals, unknown outcomes and mission events; notifications | M | P3 |
| PR-24 | Accessibility baseline: keyboard-complete core flows and screen-reader names/roles/live regions for composer, inbox, approvals and diff summary (A11Y-01/02, scripted NVDA), AA contrast | M | P2 |
| PR-24b | Terminal screen-reader mode and full WCAG 2.2 AA audit of IDE surfaces | S | P6 |
| PR-26 | Zain Code Review: one findings schema and store; delegated review mode is the default (R1/R2); fixes applied only via Core grants with undo and verification; the Alibaba OCR engine lane (fork) is preserved as an R3 capability, local-only and advisory until K-11 qualification; cloud review routes only through the mediated proxy (K-09) | M (delegated, fixes) / S (OCR engine lane) | P5 / P6 |
| PR-27 | Zain Engineering System: one investigate-plan-implement-test-review-verify loop (PStack-derived) with E2E evidence feeding Trusted Completion | M | P5 |
| PR-28 | Zain Browser: one BrowserController, lanes Preview/Agent/Test (+ opt-in user-session later), action receipts, evidence, recovery | M (localhost/allow-listed) / S (general web) | P5 / P9 |
| PR-29 | Zain Plan Mode: first-class read-only planning mode with durable artifacts, approval to mission | M | P2-P5 |
| PR-30 | DeskGate: agent-facing filesystem/terminal/process tools mediated by Core; remote via runner | M (local) / S (remote) | P3 / P10 |
| PR-25 | Enterprise seams (principal/scope, audit export from ledger); enterprise admin deferred | C | P3 seam / post-v1 |

## B. Authority, security, durability

| ID | Requirement | Pri | Phase |
|---|---|---|---|
| SEC-01 | Core Nawat is the only policy decision point; Server is PEP and named TCB | M | P3 |
| SEC-02 | Effect model per Spec 006 §19 (proposal → decision → dispatch → result/reconciliation; UNKNOWN outcomes; retry safety) | M | P3 |
| SEC-03 | Dispatch record fsynced before release; replay classes SAFE/RECONCILABLE/NEVER | M | P3 |
| SEC-04 | Approvals, policy and mode changes require a WebAuthn assertion verified by Core over a canonical operation binding; approval text is rendered by a Core-owned surface; enrollment, recovery and credential replacement are specified; approval level A1/A2/A3 is recorded and shown (17 §4) | M | P3 |
| SEC-05 | MEDIATED/UNMEDIATED tagging on every effect; UI trust indicator states the current claim | M | P3 |
| SEC-06 | Containment floor before P8: data-root and out-of-worktree write deny in provider profiles; Job Objects; no Full access | M | P3 |
| SEC-07 | OS sandbox for providers on Windows, macOS, Linux; Full-access lane only inside sandbox | S | P8 |
| SEC-08 | Ledger append-only, fsync, verified on start; versioned envelope hash over every authoritative field; anchors with an explicit anchored prefix and a reported unanchored interval (17 §5) | M | P3 |
| SEC-09 | Single Core per data root (OS lock); fencing epoch; direction-tagged ids; chunked frames | M | P3 |
| SEC-10 | T3 recovery gated by Core (S4b); two-phase continuation fires | M | P3/P4 |
| SEC-11 | No telemetry egress; no donor endpoints, feeds or identifiers in shipped builds (grep + installer gates) | M | P2 |
| SEC-12 | Secrets in OS keyring; Core holds handles only; no secrets in logs/ledger | M | P2/P3 |
| SEC-13 | Claude: API key/cloud credentials only for Zain-initiated usage; SDK not bundled until G4; never read claude.ai credentials | M | P2 |
| SEC-14 | CLI-agent hooks via per-launch overlays + authenticated loopback endpoint; never write user's global agent configs | S | P6 |
| SEC-15 | Release builds have no observe mode | M | P3 |
| SEC-16 | Design preview runs in isolated origin with no access to Server/Core | S | P7 |
| SEC-18 | Review route independence cannot be overridden by ambient config/env | M | P5 |
| SEC-19 | Plan Mode denies MEDIATED writes outside the plan path; UNMEDIATED writes are detected and invalidate the plan (prevention only after P8) | M | P3 |
| SEC-20 | Browser hard blocks; navigation/redirect approval gate; connection-level egress enforcement for every request type before any external origin is allowed in agent lanes (19 §1); no import of user browser cookie stores | M | P2-P5 |
| SEC-21 | DeskGate has no execution authority of its own (single PTY/process host; Core-mediated) | M | P3 |
| SEC-22 | Execution coverage is tracked separately from launch authorization; unsandboxed execution has UNKNOWN descendant coverage; Trusted Completion fails closed when required coverage is UNKNOWN (17 §2) | M | P3 |
| SEC-23 | Provider × operation enforcement matrix; cached approvals live only in Core with scope, expiry, epoch and revocation; unqualified cells excluded from the trusted tier (18) | M | P3 |
| SEC-24 | Process lifecycle: every launch owned by ProcessHost (Windows Job Objects created atomically, no breakaway, kill on Server death); retries only after proven quiescence (17 §3) | M | P3 |
| SEC-25 | Per-operation reconciliation contracts: APPLIED / NOT_APPLIED / UNKNOWN evidence per effect class; current remote state never proves absence unless the state is monotonic (17 §1) | M | P3 |
| SEC-26 | Single handle-based file write path with no-follow/reparse protection (fs-gate) for every mediated write (19 §3) | M | P3 |
| SEC-27 | Review confidentiality: reviews read an immutable, screened snapshot with an exact allowlist; cloud review egress only via the mediated proxy with approval (19 §2) | M | P5/P6 |
| SEC-17 | Every negative security test names its guard, mutant, fixture and observable failure (23) and fails with its guard removed; Core is the guard only where Core enforces the property | M | P3+ |

## C. Non-functional (budgets are targets until measured)

| ID | Requirement | Pri | Phase |
|---|---|---|---|
| NF-01 | Cold start ≤ T3 baseline + 10% (B1) | M | P2 |
| NF-02 | Idle RSS ≤ T3 + 15%; 10 sessions ≤ 2.5 GB (B2) | M | P2 |
| NF-03 | Input latency p95 ≤ 50 ms (B3) | M | P2 |
| NF-04 | Per mediated effect added latency p95 ≤ 25 ms; Core decision p95 ≤ 5 ms (B13) | M | P3 |
| NF-05 | Recovery invariants I1–I6 100% across R1–R11, W1–W9; p95 resume < 10 s | M | P3/P4 |
| NF-06 | Ledger growth ≤ 50 MB / 10k effects (B10) | M | P3 |
| NF-07 | Brain query p95 ≤ 50 ms at 100k entries; capsule ≤ 2k tokens | M | P4 |
| NF-08 | Offline usability checklist passes (B12) | M | P2/P4 |
| NF-09 | Benchmarks B7/B8/B11 run and published with raw data before any comparative claim | S | P6 |

## D. Governance, copy-first, provenance

| ID | Requirement | Pri | Phase |
|---|---|---|---|
| GOV-01 | CI available and main green on unchanged re-run (P−1′) | M | P−1′ |
| GOV-02 | One stable governance checker from base; protected paths; founder-signed co-sign; risk tiers | M | P0 |
| GOV-03 | Independent review per tier; `REVIEW_BLOCKED` never converted to PASS | M | all |
| GOV-04 | Egress preflight before any external review; no automatic external review | M | all |
| GOV-05 | Every transplanted file has upstream path@SHA, license, destination, notice handling recorded (06 + R11 + R12) | M | P2+ |
| GOV-06 | Third-party notices generated and build fails on missing notice (keep T3 gate) | M | P2 |
| GOV-07 | Source admission per component at phase entry (pin, license, deps, tests) | M | P2+ |
| GOV-08 | Build Learning entry per phase | M | all |
| GOV-09 | Invariant text amendment (Mirefa/Edara line) through governed PR | M | P0 |
| GOV-11 | Product identity is Zain everywhere user-facing; naming clearance and controlled-domain identifiers before distribution; legacy names preserved only as history | M | P2-N |
| GOV-12 | Zain and the separate Zain-LLM project share no identifiers, packages, channels or docs | M | P2-N |
| GOV-10 | `MASTER_PLAN_INDEX.md` updated to V3 only by a governed change after acceptance | M | P0 |
| GOV-14 | No unqualified binary or packaged-content log is distributed: R0a artifacts local or in a private repository; testers only through an access-controlled channel after license/SDK gates; public distribution only after L4 admission (22 §5) | M | PF/P2 |
| GOV-13 | Governance reset preserves every baseline property and negative oracle, or retires it by signed founder decision with a risk record; equivalence is shown with negative corpora, not accepted-PR replay alone (20) | M | P0 |

## E. Claude parity

Census counts and row mappings are research inventory, **not** acceptance coverage (Astro M-3). Parity labels
(PARITY / ADAPTATION / DEFERRED) for V1-01…18 are in 03F §2b.

All 377 census rows are mapped in `03F` (phase, module, placeholder test). v1-gating rows have hand-written specs
V1-01…V1-18 (03F §2). Traceability treats V1-xx as requirements `CL-V1-01…18`; Backlog rows are accounted, not required.
Design sub-features map to R03B AT-01…AT-23 (P0 subset AT-01…15 required at P7 exit).
