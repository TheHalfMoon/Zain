# 15 — Traceability Matrix (generated)

```text
GENERATED_FROM = 13_REQUIREMENTS_REGISTER.md + 14_TASK_CATALOG.md (script: deterministic parse of Reqs and Tests columns)
REQUIREMENTS = 90 · COVERED (task + test) = 90 · GAPS = 0 
RULE = a requirement without a task and a test is a planning defect; Claude Backlog rows (03F) are accounted, not required
```

| Req | Requirement | Pri | Phase | Tasks | Tests (task: tests) | Coverage |
|---|---|---|---|---|---|---|
| PR-01 | One desktop app combining IDE and AI workspace (chat, code sessions, files, terminal, brow | M | P2 | F-01, F-10, F-16, V-08 | F-01: manifest hash test; F-10: det: existing 19k-line Rust suite; F-16: e2e smoke; V1-01 composer→task; V1-06 parallel worktre | OK |
| PR-02 | Run Claude, Codex, ACP-family agents, OpenCode, Pi and local models as replaceable workers | M | P2/P3 | F-16, V-08 | F-16: e2e smoke; V1-01 composer→task; V1-06 parallel worktre; V-08: e2e | OK |
| PR-03 | Multi-agent orchestration: parallel sessions in isolated worktrees, subagents, steer/inter | M | P2/P5 | F-16, V-01, V-08 | F-16: e2e smoke; V1-01 composer→task; V1-06 parallel worktre; V-01: neg; V-08: e2e | OK |
| PR-04 | Unified composer that escalates chat to task with visible plan and resume | M | P2/P4 | F-16, V-08 | F-16: e2e smoke; V1-01 composer→task; V1-06 parallel worktre; V-08: e2e | OK |
| PR-05 | Projects with instructions, knowledge files, isolated memory; Brain indexes repo specs | M | P4 | M-03, M-06, V-08 | M-03: det; NF-07 bench; M-06: e2e; V1-03, V1-04; V-08: e2e | OK |
| PR-06 | Durable missions with continuations (schedules, wait-for-CI/PR/human), missed-run policy | M | P4 | M-01, M-02, M-06, M-07, V-08 | M-01: det; R1; M-02: det; W2b, W3; V1-05; M-06: e2e; V1-03, V1-04 | OK |
| PR-07 | Context survives model/provider switch and compaction (capsules) | M | P4 | M-04, M-05, V-08 | M-04: det; B8; M-05: W8; B8; V-08: e2e | OK |
| PR-08 | Git: worktrees, checkpoints, diff review with inline comments, PR/CI tracking; destructive | M | P2/P3 | F-16, C-12, V-08, I-07 | C-12: neg per class; W6; F-16: e2e smoke; V1-01 composer→task; V1-06 parallel worktre; I-07: det fixtures | OK |
| PR-09 | Terminals: integrated PTYs; CLI agents in terminals with status detection, labelled UNMEDI | M (terminal) / S (CLI agents P6) | P2/P6 | V-08, I-06 | I-06: neg T17; V-08: e2e | OK |
| PR-10 | Code editor (Monaco) with diff comments; LSP for TS/Python/Rust/Go | S | P6 | V-08, I-01, I-02, I-03 | I-01: e2e; bench; I-02: e2e; I-03: e2e per language | OK |
| PR-11 | Debugging via Debug Adapter Protocol (Node/browser, Python, Rust/C++, Go); debug launches  | S | P6 | V-08, I-04, S-06 | I-04: e2e per adapter; neg: launch without grant; S-06: neg: agent process cannot ptrace; V-08: e2e | OK |
| PR-12 | Code review: independent reviewer worker, findings schema, finding → repair proposal loop | M | P5 | V-01, V-02, V-03, V-08, K-04 | K-04: det; neg reviewer=builder; V-01: neg; V-02: e2e | OK |
| PR-13 | Trusted Completion: decision over evidence; merge/CI ≠ completion; UNMEDIATED-only changes | M | P5 | F-08, V-04, V-08, E-02 | E-02: neg ES-AT; F-08: det; V-04: neg; CC-T05; V1-07 | OK |
| PR-14 | Skills (SKILL.md), plugins, MCP (local/remote OAuth), MCPB extensions with manifest review | M (MCP, skills) / S (MCPB) | P5 | V-05, V-06, V-07, V-08 | V-05: neg; V1-09; V-06: neg T5; V1-08; V-07: neg; V1-10 | OK |
| PR-15 | Design Studio: canvas, element→source mapping, comments → agent proposals, DTCG tokens, de | S | P7 | I-05, D-01, D-03, D-04, D-05, D-06, D-07, D-08 | D-01: AT-01..03; D-03: AT source-mapping; D-04: AT | OK |
| PR-16 | Documents/artifacts: generate, preview, export (MD/HTML/PDF; PPTX/XLSX later) as project f | S | P9 | W-01, W-02 | W-01: e2e; V1-11; W-02: det | OK |
| PR-17 | Research tasks with stored citations as evidence | S | P9 | W-03 | W-03: e2e; V1-13 | OK |
| PR-18 | Controlled browser automation in the in-app browser; hard-blocked categories (payments, cr | S | P9 | I-05, W-04, Y-09 | I-05: e2e; AT-01..05; W-04: neg T12; V1-14; Y-09: neg | OK |
| PR-19 | Controlled computer use (Windows first, then macOS/Linux) behind per-session grants | C→S | P9 | W-05 | W-05: neg T12; V1-15 | OK |
| PR-20 | Self-hosted runner as project home; phone/web approvals via passkey | S | P10 | R-01, R-02, R-03, R-04, H-06 | H-06: neg; R-01: e2e; R-02: det | OK |
| PR-21 | Windows x64 primary; macOS and Linux packages | M (Win) / S (mac, Linux) | P2/P6 | F-11, F-12, I-09 | F-11: det: notice gate; F-12: det/e2e per issue; I-09: e2e smoke | OK |
| PR-22 | Local-first: core works offline; zero mandatory cloud; BYO credentials only | M | P2 | F-02, F-05, I-10 | F-02: det: kept suites; grep; F-05: e2e: egress capture; I-10: det | OK |
| PR-23 | Inbox for approvals, unknown outcomes and mission events; notifications | M | P3 | C-14 | C-14: e2e | OK |
| PR-24 | Accessibility baseline (keyboard-complete, screen-reader modes, AA contrast) | M | P2/P6 | F-14, I-11 | F-14: e2e: axe scan; I-11: e2e: axe + NVDA/VoiceOver scripted checks | OK |
| PR-26 | Zain Code Review: one review engine (OCR fork) with IDE findings panel, dispositions, fix  | M | P5 | K-01, K-02, K-03, K-04, K-05, K-06, K-07, K-08, K-09, E-05 | E-05: det; K-01: ZCR spike log; K-02: det: license gate | OK |
| PR-27 | Zain Engineering System: one investigate-plan-implement-test-review-verify loop (PStack-de | M | P5 | E-01, E-02, E-03, E-04, E-05, E-06, E-07, L-07 | E-01: ES-AT-03; E-02: neg ES-AT; E-03: ES-AT e2e | OK |
| PR-28 | Zain Browser: one BrowserController, lanes Preview/Agent/Test (+ opt-in user-session later | M (localhost/allow-listed) / S (general web) | P5 / P9 | E-03, Y-00, Y-01, Y-02, Y-03, Y-04, Y-05, Y-06, Y-07, Y-08, Y-09 | E-03: ES-AT e2e; Y-00: neg: cookie import absent; grep gate; Y-01: neg | OK |
| PR-29 | Zain Plan Mode: first-class read-only planning mode with durable artifacts, approval to mi | M | P2-P5 | L-01, L-02, L-03, L-04, L-05, L-06, L-07, L-08, L-09, L-10 | L-01: e2e; L-02: neg N1–N8; L-03: neg N9–N10 | OK |
| PR-30 | DeskGate: agent-facing filesystem/terminal/process tools mediated by Core; remote via runn | M (local) / S (remote) | P3 / P10 | H-00, H-01, H-02, H-03, H-04, H-05, H-06, H-07 | H-00: review; H-01: neg DG-N10; H-02: neg DG-N* | OK |
| PR-25 | Enterprise seams (principal/scope, audit export from ledger); enterprise admin deferred | C | P3 seam / post-v1 | C-03 | C-03: det; R6; W5; bench B10; det: audit export JSONL from l | OK |
| SEC-01 | Core Nawat is the only policy decision point; Server is PEP and named TCB | M | P3 | C-05, C-06, C-08, C-09, C-12 | C-05: det; neg; C-06: e2e; W1; C-08: neg T1 (ACP write outside worktree) | OK |
| SEC-02 | Effect model per Spec 006 §19 (proposal → decision → dispatch → result/reconciliation; UNK | M | P3 | C-01, C-04, K-06, Y-05 | C-01: det; R1 sample; C-04: det; neg: dispatch without grant; neg T6: seeded fake ; K-06: neg ZCR-T07/T10/T11 | OK |
| SEC-03 | Dispatch record fsynced before release; replay classes SAFE/RECONCILABLE/NEVER | M | P3 | C-01, C-04, C-09 | C-01: det; R1 sample; C-04: det; neg: dispatch without grant; neg T6: seeded fake ; C-09: neg; CC-T02 kill mid-Edit; V1-17 | OK |
| SEC-04 | Approvals, policy and mode changes require WebAuthn assertion verified by Core | M | P3 | C-13, R-03 | C-13: neg T3 (forged/replayed); R-03: neg; V1-16 | OK |
| SEC-05 | MEDIATED/UNMEDIATED tagging on every effect; UI trust indicator states the current claim | M | P3 | C-14, C-17, S-05 | C-14: e2e; C-17: det; S-05: e2e | OK |
| SEC-06 | Containment floor before P8: data-root and out-of-worktree write deny in provider profiles | M | P3 | F-07, C-07, C-16 | C-07: neg; C-16: neg T10b; F-07: e2e; neg (with S1 later) | OK |
| SEC-07 | OS sandbox for providers on Windows, macOS, Linux; Full-access lane only inside sandbox | S | P8 | S-01, S-02, S-03, S-04, S-06 | S-01: escape suite (Win); S-02: escape suite (Linux); S-03: escape suite (mac) | OK |
| SEC-08 | Ledger append-only, hash-chained, fsync, verified on start; out-of-machine anchors | M | P3 | C-03, C-11, C-19 | C-03: det; R6; W5; bench B10; det: audit export JSONL from l; C-11: det; W2; C-19: neg T10b | OK |
| SEC-09 | Single Core per data root (OS lock); fencing epoch; direction-tagged ids; chunked frames | M | P3 | C-02 | C-02: det; neg: stale epoch, replayed id, second Core | OK |
| SEC-10 | T3 recovery gated by Core (S4b); two-phase continuation fires | M | P3/P4 | C-10, M-02 | C-10: R1 sweep; W9; M-02: det; W2b, W3; V1-05 | OK |
| SEC-11 | No telemetry egress; no donor endpoints, feeds or identifiers in shipped builds (grep + in | M | P2 | F-02, F-03, F-04, F-05, F-09 | F-02: det: kept suites; grep; F-03: det: donor-identifier grep gate; F-04: neg: donor manifest rejected | OK |
| SEC-12 | Secrets in OS keyring; Core holds handles only; no secrets in logs/ledger | M | P2/P3 | C-04 | C-04: det; neg: dispatch without grant; neg T6: seeded fake  | OK |
| SEC-13 | Claude: API key/cloud credentials only for Zain-initiated usage; SDK not bundled until G4; | M | P2 | B-06, F-06 | F-06: det: installer-content gate; e2e: Claude session with  | OK |
| SEC-14 | CLI-agent hooks via per-launch overlays + authenticated loopback endpoint; never write use | S | P6 | I-06 | I-06: neg T17 | OK |
| SEC-15 | Release builds have no observe mode | M | P3 | C-18 | C-18: neg T15 | OK |
| SEC-16 | Design preview runs in isolated origin with no access to Server/Core | S | P7 | D-02 | D-02: neg T11; AT sandbox | OK |
| SEC-18 | Review route independence cannot be overridden by ambient config/env | M | P5 | K-03 | K-03: neg ZCR-T05 | OK |
| SEC-19 | Plan Mode never writes product files; violations invalidate the plan | M | P3 | L-02, L-03 | L-02: neg N1–N8; L-03: neg N9–N10 | OK |
| SEC-20 | Browser hard blocks, pre-request redirect gating, no import of user browser cookie stores | M | P2-P5 | Y-00, Y-01, Y-03, Y-04 | Y-00: neg: cookie import absent; grep gate; Y-01: neg; Y-03: neg redirect | OK |
| SEC-21 | DeskGate has no execution authority of its own (single PTY/process host; Core-mediated) | M | P3 | H-01, H-03 | H-01: neg DG-N10; H-03: neg | OK |
| SEC-17 | Every negative security test passes mutation control (fails with Core disabled) | M | P3+ | C-22, K-07, E-07, L-10, Y-08, H-05 | C-22: all above; E-07: ES-AT; H-05: neg; bench | OK |
| NF-01 | Cold start ≤ T3 baseline + 10% (B1) | M | P2 | B-03, B-04, F-15 | B-03: T3 suites; B-04: bench B1–B5; F-15: bench B1–B3, B12 | OK |
| NF-02 | Idle RSS ≤ T3 + 15%; 10 sessions ≤ 2.5 GB (B2) | M | P2 | B-03, B-04, F-12, F-15 | B-03: T3 suites; B-04: bench B1–B5; F-12: det/e2e per issue | OK |
| NF-03 | Input latency p95 ≤ 50 ms (B3) | M | P2 | B-03, B-04, F-15 | B-03: T3 suites; B-04: bench B1–B5; F-15: bench B1–B3, B12 | OK |
| NF-04 | Per mediated effect added latency p95 ≤ 25 ms; Core decision p95 ≤ 5 ms (B13) | M | P3 | B-05, C-21 | B-05: microbench; C-21: bench B13 | OK |
| NF-05 | Recovery invariants I1–I6 100% across R1–R11, W1–W9; p95 resume < 10 s | M | P3/P4 | C-10, C-20 | C-10: R1 sweep; W9; C-20: R/W suites | OK |
| NF-06 | Ledger growth ≤ 50 MB / 10k effects (B10) | M | P3 | C-03 | C-03: det; R6; W5; bench B10; det: audit export JSONL from l | OK |
| NF-07 | Brain query p95 ≤ 50 ms at 100k entries; capsule ≤ 2k tokens | M | P4 | M-03 | M-03: det; NF-07 bench | OK |
| NF-08 | Offline usability checklist passes (B12) | M | P2/P4 | F-15 | F-15: bench B1–B3, B12 | OK |
| NF-09 | Benchmarks B7/B8/B11 run and published with raw data before any comparative claim | S | P6 | I-08 | I-08: bench | OK |
| GOV-01 | CI available and main green on unchanged re-run (P−1′) | M | P−1′ | A-01, A-02, G-04 | A-01: run log; A-02: local log; G-04: det: mocked 403/429 | OK |
| GOV-02 | One stable governance checker from base; protected paths; founder-signed co-sign; risk tie | M | P0 | G-02, G-03, G-05 | G-02: neg: unsigned co-sign rejected; G-03: det: checker unit tests; neg: PR editing checker canno; G-05: det: replay last 20 merged PRs through checker → same  | OK |
| GOV-03 | Independent review per tier; `REVIEW_BLOCKED` never converted to PASS | M | all | G-01, B-07 | G-01: integrity green | OK |
| GOV-04 | Egress preflight before any external review; no automatic external review | M | all | G-01 | G-01: integrity green | OK |
| GOV-05 | Every transplanted file has upstream path@SHA, license, destination, notice handling recor | M | P2+ | B-02, F-01, E-00 | B-02: hash check; E-00: hash check; F-01: manifest hash test | OK |
| GOV-06 | Third-party notices generated and build fails on missing notice (keep T3 gate) | M | P2 | F-11, E-01, L-06 | E-01: ES-AT-03; F-11: det: notice gate; L-06: det D4–D5; neg N13 | OK |
| GOV-07 | Source admission per component at phase entry (pin, license, deps, tests) | M | P2+ | B-01, F-01, K-02, H-00 | F-01: manifest hash test; H-00: review; K-02: det: license gate | OK |
| GOV-08 | Build Learning entry per phase | M | all | G-03, F-13 | G-03: det: checker unit tests; neg: PR editing checker canno | OK |
| GOV-09 | Invariant text amendment (Mirefa/Edara line) through governed PR | M | P0 | G-06 | G-06: integrity | OK |
| GOV-11 | Product identity is Zain everywhere user-facing; naming clearance and controlled-domain id | M | P2-N | N-01, N-02, N-03, N-04 | N-01: review of clearance record; N-02: det: identity grep gate uses final ids; N-03: det: grep gate for Zain-LLM identifiers | OK |
| GOV-12 | Zain and the separate Zain-LLM project share no identifiers, packages, channels or docs | M | P2-N | N-03 | N-03: det: grep gate for Zain-LLM identifiers | OK |
| GOV-10 | `MASTER_PLAN_INDEX.md` updated to V3 only by a governed change after acceptance | M | P0 | G-06 | G-06: integrity | OK |
| CL-V1-01 | 03F §2 V1-01 | see 03F | see 03F | F-16 | F-16: e2e smoke; V1-01 composer→task; V1-06 parallel worktre | OK |
| CL-V1-02 | 03F §2 V1-02 | see 03F | see 03F | C-05, C-15 | C-05: det; neg; C-15: e2e; V1-02 | OK |
| CL-V1-03 | 03F §2 V1-03 | see 03F | see 03F | M-06 | M-06: e2e; V1-03, V1-04 | OK |
| CL-V1-04 | 03F §2 V1-04 | see 03F | see 03F | M-06 | M-06: e2e; V1-03, V1-04 | OK |
| CL-V1-05 | 03F §2 V1-05 | see 03F | see 03F | M-02 | M-02: det; W2b, W3; V1-05 | OK |
| CL-V1-06 | 03F §2 V1-06 | see 03F | see 03F | F-16 | F-16: e2e smoke; V1-01 composer→task; V1-06 parallel worktre | OK |
| CL-V1-07 | 03F §2 V1-07 | see 03F | see 03F | V-04 | V-04: neg; CC-T05; V1-07 | OK |
| CL-V1-08 | 03F §2 V1-08 | see 03F | see 03F | V-06 | V-06: neg T5; V1-08 | OK |
| CL-V1-09 | 03F §2 V1-09 | see 03F | see 03F | V-05 | V-05: neg; V1-09 | OK |
| CL-V1-10 | 03F §2 V1-10 | see 03F | see 03F | V-07 | V-07: neg; V1-10 | OK |
| CL-V1-11 | 03F §2 V1-11 | see 03F | see 03F | W-01 | W-01: e2e; V1-11 | OK |
| CL-V1-12 | 03F §2 V1-12 | see 03F | see 03F | D-08 | D-08: AT; V1-12 | OK |
| CL-V1-13 | 03F §2 V1-13 | see 03F | see 03F | W-03 | W-03: e2e; V1-13 | OK |
| CL-V1-14 | 03F §2 V1-14 | see 03F | see 03F | W-04 | W-04: neg T12; V1-14 | OK |
| CL-V1-15 | 03F §2 V1-15 | see 03F | see 03F | W-05 | W-05: neg T12; V1-15 | OK |
| CL-V1-16 | 03F §2 V1-16 | see 03F | see 03F | R-03 | R-03: neg; V1-16 | OK |
| CL-V1-17 | 03F §2 V1-17 | see 03F | see 03F | C-09 | C-09: neg; CC-T02 kill mid-Edit; V1-17 | OK |
| CL-V1-18 | 03F §2 V1-18 | see 03F | see 03F | C-03 | C-03: det; R6; W5; bench B10; det: audit export JSONL from l | OK |
