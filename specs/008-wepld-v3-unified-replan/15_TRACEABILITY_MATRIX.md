# 15 — Traceability Matrix (generated)

```text
GENERATED_BY = tools/plan_graph.py from 13 + 14 + 23 (do not hand-edit)
COVERAGE_RULE = REGISTERED: a live task maps the requirement and runs ≥1 registered test; FREE_TEXT_ONLY;
                GAP. This is accounting, not semantic verification (Astro M-3, A2-06).
REQUIREMENTS = 99 · REGISTERED = 99 · FREE_TEXT_ONLY = 0 · GAP = 0
```

| Req | Requirement | Pri | Phase | Tasks | Registered tests | Coverage |
|---|---|---|---|---|---|---|
| PR-01 | One desktop app combining IDE and AI workspace (chat, code sessions, files, term | M | P2 | F-01, F-10, F-16, F-17, F-18, Q-01, Q-02, Q-05, Q-06, V-08 | EDIT-01, FWB-01, FWB-02, FWB-03, FWB-04, SRC-01, SRC-02, TERM-01, V1-01, V1-06 | REGISTERED |
| PR-02 | Run Claude, Codex, ACP-family agents, OpenCode, Pi and local models as replaceab | M | P2/P3 | C-09, C-24, F-16 | CC-T01, CC-T02, CC-T03, PEM-ACP-01, PEM-ACP-02, PEM-ACP-03, PEM-CDX-01, PEM-CDX-02, PEM-CDX-03, PEM-CDX-04, PEM-CDX-05, PEM-CDX-06 … | REGISTERED |
| PR-03 | Multi-agent orchestration: parallel sessions in isolated worktrees, subagents, s | M | P2/P5 | F-16, V-01, V-08 | POL-03, TERM-01, V1-01, V1-06 | REGISTERED |
| PR-04 | Unified composer that escalates chat to task with visible plan and resume | M | P2/P4 | F-16, V-08 | TERM-01, V1-01, V1-06 | REGISTERED |
| PR-05 | Projects with instructions, knowledge files, isolated memory; Brain indexes repo | M | P4 | M-03, M-06 | B14, V1-03, V1-04 | REGISTERED |
| PR-06 | Durable missions with continuations (schedules, wait-for-CI/PR/human), missed-ru | M | P4 | M-01, M-02, M-06, M-07 | R1, R2, R9, V1-03, V1-04, V1-05, W2b, W3 | REGISTERED |
| PR-07 | Context survives model/provider switch and compaction (capsules) | M | P4 | M-04, M-05 | B8, W8 | REGISTERED |
| PR-08 | Git: worktrees, checkpoints, diff review with inline comments, PR/CI tracking; d | M | P2/P3 | C-12, F-16, I-07 | REC-03, T2, T4, TERM-01, TERM-02, V1-01, V1-06, W6 | REGISTERED |
| PR-09 | Terminals: integrated PTYs on Windows (spawn, input, output, resize, kill — TERM | M (terminal) / S (CLI agents P6) | P2/P3/P6 | F-16, I-06 | T17, TERM-01, V1-01, V1-06 | REGISTERED |
| PR-10 | Code editor (Monaco) with diff comments; LSP for TS/Python/Rust/Go | S | P6 | F-17, I-02, I-03 | EDIT-01 | REGISTERED |
| PR-11 | Debugging via Debug Adapter Protocol (Node/browser, Python, Rust/C++, Go); debug | S | P6 | I-04, S-06 | DBG-01, DBG-02, SBX-01 | REGISTERED |
| PR-12 | Code review: independent reviewer worker, findings schema, finding → repair prop | M | P5 | K-04, V-01, V-08 | POL-03, ZCR-T04, ZCR-T14, ZCR-T25 | REGISTERED |
| PR-13 | Trusted Completion: decision over evidence; merge/CI ≠ completion; UNMEDIATED-on | M | P5 | C-23, E-02, F-08, V-04, V-08 | CC-T05, COV-01, COV-02, COV-03, COV-04, COV-05, COV-06, COV-08, COV-09, ES-AT-06, ES-AT-08, ES-AT-16 … | REGISTERED |
| PR-14 | Skills (SKILL.md), plugins, MCP (local/remote OAuth), MCPB extensions with manif | M (MCP, skills) / S (MCPB) | P5 | V-05, V-06, V-07 | T4, T5, V1-08, V1-09, V1-10 | REGISTERED |
| PR-15 | Design Studio: canvas, element→source mapping, comments → agent proposals, DTCG  | S | P7 | D-01, D-03, D-04, D-05, D-06, D-07, D-08, I-05 | AT-01, AT-02, AT-03, AT-04, AT-05, AT-06, AT-07, AT-08, AT-09, AT-10, AT-11, AT-12 … | REGISTERED |
| PR-16 | Documents/artifacts: generate, preview, export (MD/HTML/PDF; PPTX/XLSX later) as | S | P9 | W-01, W-02 | V1-11 | REGISTERED |
| PR-17 | Research tasks with stored citations as evidence | S | P9 | W-03 | V1-13 | REGISTERED |
| PR-18 | Controlled browser automation in the in-app browser; hard-blocked categories (pa | S | P9 | I-05, Y-09 | BRW-AT-23, BRW-AT-24, DM-01, DM-02, DM-03 | REGISTERED |
| PR-19 | Controlled computer use (Windows first, then macOS/Linux) behind per-session gra | C→S | P9 | W-05 | T12, V1-15 | REGISTERED |
| PR-20 | Self-hosted runner as project home; phone/web approvals via passkey | S | P10 | H-06, R-01, R-02, R-03, R-04 | DG-N12, DG-P07, RMT-01, V1-16 | REGISTERED |
| PR-21 | Windows x64 primary; macOS and Linux packages | M (Win) / S (mac, Linux) | P2/P6 | F-11, F-12, F-19, F-21, I-09, I-12, Q-04 | CI-02, FWB-01, LIC-01, PKG-01, PKG-02 | REGISTERED |
| PR-22 | Local-first: core works offline; zero mandatory cloud; BYO credentials only | M | P2 | F-02, F-05, I-10, Q-03 | EGR-01, EGR-02, EGR-03 | REGISTERED |
| PR-23 | Inbox for approvals, unknown outcomes and mission events; notifications | M | P3 | C-14 | A11Y-04, INBOX-01 | REGISTERED |
| PR-24 | Accessibility baseline: keyboard-complete core flows and screen-reader names/rol | M | P2 | F-14 | A11Y-01, A11Y-02 | REGISTERED |
| PR-24b | Terminal screen-reader mode and full WCAG 2.2 AA audit of IDE surfaces | S | P6 | I-11 | A11Y-03 | REGISTERED |
| PR-26 | Zain Code Review: one findings schema and store; delegated review mode is the de | M (delegated, fixes) / S (OCR engine lane) | P5 / P6 | E-05, K-01, K-02, K-03, K-04, K-05, K-06, K-07, K-08, K-09, K-10, K-11 | ZCR-Q01, ZCR-Q02, ZCR-Q03, ZCR-Q04, ZCR-T01, ZCR-T02, ZCR-T03, ZCR-T04, ZCR-T05, ZCR-T06, ZCR-T07, ZCR-T08 … | REGISTERED |
| PR-27 | Zain Engineering System: one investigate-plan-implement-test-review-verify loop  | M | P5 | E-01, E-02, E-03, E-04, E-05, E-06, E-07, L-07 | D6, ES-AT-01, ES-AT-02, ES-AT-03, ES-AT-04, ES-AT-05, ES-AT-06, ES-AT-07, ES-AT-08, ES-AT-09, ES-AT-10, ES-AT-11 … | REGISTERED |
| PR-28 | Zain Browser: one BrowserController, lanes Preview/Agent/Test (+ opt-in user-ses | M (localhost/allow-listed) / S (general web) | P5 / P9 | E-03, Y-00, Y-01, Y-02, Y-03, Y-04, Y-05, Y-06, Y-07, Y-08, Y-09, Y-10 | BRW-AT-01, BRW-AT-02, BRW-AT-03, BRW-AT-04, BRW-AT-05, BRW-AT-06, BRW-AT-07, BRW-AT-08, BRW-AT-09, BRW-AT-10, BRW-AT-11, BRW-AT-12 … | REGISTERED |
| PR-29 | Zain Plan Mode: first-class read-only planning mode with durable artifacts, appr | M | P2-P5 | L-01, L-02, L-03, L-04, L-05, L-06, L-07, L-08, L-09, L-10 | COV-07, D1, D2, D3, D4, D5, D6, E1, E2, E3, E4, E5 … | REGISTERED |
| PR-30 | DeskGate: agent-facing filesystem/terminal/process tools mediated by Core; remot | M (local) / S (remote) | P3 / P10 | H-00, H-01, H-02, H-03, H-04, H-05, H-06, H-07 | DG-B1, DG-B2, DG-B3, DG-B4, DG-B5, DG-B6, DG-B7, DG-B8, DG-B9, DG-N01, DG-N02, DG-N03 … | REGISTERED |
| PR-25 | Enterprise seams (principal/scope, audit export from ledger); enterprise admin d | C | P3 seam / post-v1 | C-03, C-04 | B10, EFF-01, LED-01, LED-02, OPID-01, R6, R7, T10, T6, V1-18, W5 | REGISTERED |
| SEC-01 | Core Nawat is the only policy decision point; Server is PEP and named TCB | M | P3 | C-05, C-06, C-08, C-09, C-12 | CC-T01, CC-T02, CC-T03, FSG-01, PEM-ACP-01, PEM-ACP-02, PEM-ACP-03, PEM-CDX-01, PEM-CDX-02, PEM-CDX-03, PEM-CDX-04, PEM-CDX-05 … | REGISTERED |
| SEC-02 | Effect model per Spec 006 §19 (proposal → decision → dispatch → result/reconcili | M | P3 | C-01, C-04, C-26, K-06, Y-05 | BRW-AT-16, BRW-AT-17, BRW-AT-18, EFF-01, OPID-01, REC-01, REC-02, REC-04, REC-05, REC-06, REC-07, REC-08 … | REGISTERED |
| SEC-03 | Dispatch record fsynced before release; replay classes SAFE/RECONCILABLE/NEVER | M | P3 | C-01, C-04, C-09 | CC-T01, CC-T02, CC-T03, EFF-01, OPID-01, PEM-ACP-01, PEM-ACP-02, PEM-ACP-03, PEM-CDX-01, PEM-CDX-02, PEM-CDX-03, PEM-CDX-04 … | REGISTERED |
| SEC-04 | Approvals, policy and mode changes require a WebAuthn assertion verified by Core | M | P3 | C-00, C-13, R-03 | APR-01, APR-02, APR-03, APR-04, APR-05, APR-06, APR-07, APR-08, APR-09, FG-01, FG-02, FG-03 … | REGISTERED |
| SEC-05 | MEDIATED/UNMEDIATED tagging on every effect; UI trust indicator states the curre | M | P3 | C-14, C-17, S-05, X-01 | A11Y-04, CLM-01, CLM-02, INBOX-01, ZCR-T04, ZCR-T14, ZCR-T15, ZCR-T16, ZCR-T17, ZCR-T22, ZCR-T29 | REGISTERED |
| SEC-06 | Containment floor before P8: data-root and out-of-worktree write deny in provide | M | P3 | C-00, C-07, C-16, C-25, F-07 | FG-01, FG-02, FG-03, FG-04, FG-05, LED-06, PH-01, PH-02, PH-03, PH-04, PH-05, PH-06 … | REGISTERED |
| SEC-07 | OS sandbox for providers on Windows, macOS, Linux; Full-access lane only inside  | S | P8 | S-01, S-02, S-03, S-04, S-06 | SBX-01, T2 | REGISTERED |
| SEC-08 | Ledger append-only, fsync, verified on start; versioned envelope hash over every | M | P3 | C-03, C-11, C-19 | B10, LED-01, LED-02, LED-03, LED-04, LED-05, R6, R7, T10, V1-18, W2, W5 | REGISTERED |
| SEC-09 | Single Core per data root (OS lock); fencing epoch; direction-tagged ids; chunke | M | P3 | C-02 | PROTO-01, T16 | REGISTERED |
| SEC-10 | T3 recovery gated by Core (S4b); two-phase continuation fires | M | P3/P4 | C-10, M-02 | B6, R1, V1-05, W2b, W3, W9 | REGISTERED |
| SEC-11 | No telemetry egress; no donor endpoints, feeds or identifiers in shipped builds  | M | P2 | F-02, F-03, F-04, F-05, F-09 | EGR-01, ID-01, T9 | REGISTERED |
| SEC-12 | Secrets in OS keyring; Core holds handles only; no secrets in logs/ledger | M | P2/P3 | C-04, F-18, F-22 | EFF-01, OPID-01, SEC12-01, T6 | REGISTERED |
| SEC-13 | Claude: API key/cloud credentials only for Zain-initiated usage; SDK not bundled | M | P2 | B-06, F-06, F-20 | LIC-01, PKG-01, T7, T8 | REGISTERED |
| SEC-14 | CLI-agent hooks via per-launch overlays + authenticated loopback endpoint; never | S | P6 | I-06 | T17 | REGISTERED |
| SEC-15 | Release builds have no observe mode | M | P3 | C-18 | T15 | REGISTERED |
| SEC-16 | Design preview runs in isolated origin with no access to Server/Core | S | P7 | D-02 | AT-20, T11 | REGISTERED |
| SEC-18 | Review route independence cannot be overridden by ambient config/env | M | P5 | K-03 | ZCR-T05, ZCR-T23, ZCR-T24, ZCR-T26 | REGISTERED |
| SEC-19 | Plan Mode denies MEDIATED writes outside the plan path; UNMEDIATED writes are de | M | P3 | L-02, L-03 | COV-07, D1, N1, N10, N15, N16, N2, N3, N4, N5, N6, N7 … | REGISTERED |
| SEC-20 | Browser hard blocks; navigation/redirect approval gate; connection-level egress  | M | P2-P5 | C-00, Y-00, Y-01, Y-03, Y-04, Y-10 | BRW-AT-01, BRW-AT-02, BRW-AT-03, BRW-AT-04, BRW-AT-07, BRW-AT-08, BRW-AT-11, BRW-AT-12, BRW-AT-14, BRW-AT-15, BRW-AT-21, BRW-AT-25 … | REGISTERED |
| SEC-21 | DeskGate has no execution authority of its own (single PTY/process host; Core-me | M | P3 | H-01, H-03, H-08 | DG-N06, DG-N07, DG-N08, DG-N10, DG-P04, FSG-01, FSG-02, FSG-03, FSG-04, FSG-05, FSG-06, FSG-07 … | REGISTERED |
| SEC-22 | Execution coverage is tracked separately from launch authorization; unsandboxed  | M | P3 | C-23 | COV-01, COV-02, COV-03, COV-04, COV-05, COV-08, COV-09 | REGISTERED |
| SEC-23 | Provider × operation enforcement matrix; cached approvals live only in Core with | M | P3 | C-09, C-24, C-28 | CC-T01, CC-T02, CC-T03, PEM-ACP-01, PEM-ACP-02, PEM-ACP-03, PEM-CDX-01, PEM-CDX-02, PEM-CDX-03, PEM-CDX-04, PEM-CDX-05, PEM-CDX-06 … | REGISTERED |
| SEC-24 | Process lifecycle: every launch owned by ProcessHost (Windows Job Objects create | M | P3 | C-00, C-25 | FG-01, FG-02, FG-03, FG-04, FG-05, PH-01, PH-02, PH-03, PH-04, PH-05, PH-06 | REGISTERED |
| SEC-25 | Per-operation reconciliation contracts: APPLIED / NOT_APPLIED / UNKNOWN evidence | M | P3 | C-26 | REC-01, REC-02, REC-04, REC-05, REC-06, REC-07, REC-08, REC-09, REC-10 | REGISTERED |
| SEC-26 | Single handle-based file write path with no-follow/reparse protection (fs-gate)  | M | P3 | C-00, H-08 | FG-01, FG-02, FG-03, FG-04, FG-05, FSG-01, FSG-02, FSG-03, FSG-04, FSG-05, FSG-06, FSG-07 … | REGISTERED |
| SEC-27 | Review confidentiality: reviews read an immutable, screened snapshot with an exa | M | P5/P6 | K-10 | ZCR-T01, ZCR-T02, ZCR-T03, ZCR-T19, ZCR-T20 | REGISTERED |
| SEC-17 | Every negative security test names its guard, mutant, fixture and observable fai | M | P3+ | C-22, C-27, E-07, H-05, K-07, L-10, Y-08 | BRW-AT-01, BRW-AT-02, BRW-AT-03, BRW-AT-04, BRW-AT-05, BRW-AT-06, BRW-AT-07, BRW-AT-08, BRW-AT-09, BRW-AT-10, BRW-AT-11, BRW-AT-12 … | REGISTERED |
| NF-01 | Cold start ≤ T3 baseline + 10% (B1) | M | P2 | B-03, B-04, F-15 | B1, B12, B2, B3, B4, B5 | REGISTERED |
| NF-02 | Idle RSS ≤ T3 + 15%; 10 sessions ≤ 2.5 GB (B2) | M | P2 | B-03, B-04, F-12, F-15 | B1, B12, B2, B3, B4, B5 | REGISTERED |
| NF-03 | Input latency p95 ≤ 50 ms (B3) | M | P2 | B-03, B-04, F-15 | B1, B12, B2, B3, B4, B5 | REGISTERED |
| NF-04 | Per mediated effect added latency p95 ≤ 25 ms; Core decision p95 ≤ 5 ms (B13) | M | P3 | B-05, C-21 | B13 | REGISTERED |
| NF-05 | Recovery invariants I1–I6 100% across R1–R11, W1–W9; p95 resume < 10 s | M | P3/P4 | C-10, C-20 | B6, PH-02, R1, R10, R11, R3, R4, R5, R6, R7, R8, T10b … | REGISTERED |
| NF-06 | Ledger growth ≤ 50 MB / 10k effects (B10) | M | P3 | C-03 | B10, LED-01, LED-02, R6, R7, T10, V1-18, W5 | REGISTERED |
| NF-07 | Brain query p95 ≤ 50 ms at 100k entries; capsule ≤ 2k tokens | M | P4 | M-03 | B14 | REGISTERED |
| NF-08 | Offline usability checklist passes (B12) | M | P2/P4 | F-15 | B1, B12, B2, B3 | REGISTERED |
| NF-09 | Benchmarks B7/B8/B11 run and published with raw data before any comparative clai | S | P6 | I-08 | B11, B7 | REGISTERED |
| GOV-01 | CI available and main green on unchanged re-run (P−1′) | M | P−1′ | A-01, A-02, G-04 | CI-01 | REGISTERED |
| GOV-02 | One stable governance checker from base; protected paths; founder-signed co-sign | M | P0 | G-02, G-03, G-05, G-07, G-08 | GV-01, GV-02, GV-03, GV-04, GV-05, GV-06, GV-07, GV-08, GV-09, GV-10, GV-11, GV-12 … | REGISTERED |
| GOV-03 | Independent review per tier; `REVIEW_BLOCKED` never converted to PASS | M | all | B-07, G-01, G-03, X-01 | CLM-01, CLM-02, GV-09, GV-10, GV-11, GV-12, GV-13, GV-14, GV-15, GV-17, GV-21, GV-22 … | REGISTERED |
| GOV-04 | Egress preflight before any external review; no automatic external review | M | all | G-01, G-03 | GV-09, GV-10, GV-11, GV-12, GV-13, GV-14, GV-15, GV-17, GV-21, GV-22, GV-23 | REGISTERED |
| GOV-05 | Every transplanted file has upstream path@SHA, license, destination, notice hand | M | P2+ | B-02, E-00, F-01, Q-00 | LIC-02, SRC-01 | REGISTERED |
| GOV-06 | Third-party notices generated and build fails on missing notice (keep T3 gate) | M | P2 | E-01, F-11, F-20, L-06 | D4, D5, ES-AT-02, ES-AT-03, ES-AT-04, LIC-01, N13, PKG-01, PKG-02 | REGISTERED |
| GOV-07 | Source admission per component at phase entry (pin, license, deps, tests) | M | P2+ | B-01, F-01, G-05, H-00, K-02, Q-00 | GV-01, GV-02, GV-03, GV-04, GV-05, GV-06, GV-07, GV-08, GV-16, GV-18, GV-19, LIC-02 … | REGISTERED |
| GOV-08 | Build Learning entry per phase | M | all | F-13, G-03 | GV-09, GV-10, GV-11, GV-12, GV-13, GV-14, GV-15, GV-17, GV-21, GV-22, GV-23 | REGISTERED |
| GOV-09 | Invariant text amendment (Mirefa/Edara line) through governed PR | M | P0 | G-06 | GV-09, GV-12 | REGISTERED |
| GOV-11 | Product identity is Zain everywhere user-facing; naming clearance and controlled | M | P2-N | N-01, N-02, N-03, N-04, N-05 | ID-01, ID-02 | REGISTERED |
| GOV-12 | Zain and the separate Zain-LLM project share no identifiers, packages, channels  | M | P2-N | N-03 | ID-02 | REGISTERED |
| GOV-10 | `MASTER_PLAN_INDEX.md` updated to V3 only by a governed change after acceptance | M | P0 | G-06 | GV-09, GV-12 | REGISTERED |
| GOV-14 | No unqualified binary or packaged-content log is distributed: R0a artifacts loca | M | PF/P2 | F-11, Q-04 | CI-02, LIC-01, PKG-01, PKG-02 | REGISTERED |
| GOV-13 | Governance reset preserves every baseline property and negative oracle, or retir | M | P0 | G-05, G-08 | GV-01, GV-02, GV-03, GV-04, GV-05, GV-06, GV-07, GV-08, GV-16, GV-18, GV-19 | REGISTERED |
| CL-V1-01 | 03F §2 V1-01 | see 03F | see 03F | F-16 | TERM-01, V1-01, V1-06 | REGISTERED |
| CL-V1-02 | 03F §2 V1-02 | see 03F | see 03F | C-05, C-15 | POL-01, T13, V1-02 | REGISTERED |
| CL-V1-03 | 03F §2 V1-03 | see 03F | see 03F | M-06 | V1-03, V1-04 | REGISTERED |
| CL-V1-04 | 03F §2 V1-04 | see 03F | see 03F | M-06 | V1-03, V1-04 | REGISTERED |
| CL-V1-05 | 03F §2 V1-05 | see 03F | see 03F | M-02 | V1-05, W2b, W3 | REGISTERED |
| CL-V1-06 | 03F §2 V1-06 | see 03F | see 03F | F-16 | TERM-01, V1-01, V1-06 | REGISTERED |
| CL-V1-07 | 03F §2 V1-07 | see 03F | see 03F | V-04 | CC-T05, COV-06, V1-07, W7 | REGISTERED |
| CL-V1-08 | 03F §2 V1-08 | see 03F | see 03F | V-06 | T5, V1-08 | REGISTERED |
| CL-V1-09 | 03F §2 V1-09 | see 03F | see 03F | V-05 | T4, V1-09 | REGISTERED |
| CL-V1-10 | 03F §2 V1-10 | see 03F | see 03F | V-07 | V1-10 | REGISTERED |
| CL-V1-11 | 03F §2 V1-11 | see 03F | see 03F | W-01 | V1-11 | REGISTERED |
| CL-V1-12 | 03F §2 V1-12 | see 03F | see 03F | D-08 | AT-01, AT-02, AT-03, AT-04, AT-05, AT-06, AT-07, AT-08, AT-09, AT-10, AT-11, AT-12 … | REGISTERED |
| CL-V1-13 | 03F §2 V1-13 | see 03F | see 03F | W-03 | V1-13 | REGISTERED |
| CL-V1-14 | 03F §2 V1-14 | see 03F | see 03F | Y-08 | BRW-AT-01, BRW-AT-02, BRW-AT-03, BRW-AT-04, BRW-AT-05, BRW-AT-06, BRW-AT-07, BRW-AT-08, BRW-AT-09, BRW-AT-10, BRW-AT-11, BRW-AT-12 … | REGISTERED |
| CL-V1-15 | 03F §2 V1-15 | see 03F | see 03F | W-05 | T12, V1-15 | REGISTERED |
| CL-V1-16 | 03F §2 V1-16 | see 03F | see 03F | R-03 | V1-16 | REGISTERED |
| CL-V1-17 | 03F §2 V1-17 | see 03F | see 03F | C-09 | CC-T01, CC-T02, CC-T03, PEM-ACP-01, PEM-ACP-02, PEM-ACP-03, PEM-CDX-01, PEM-CDX-02, PEM-CDX-03, PEM-CDX-04, PEM-CDX-05, PEM-CDX-06 … | REGISTERED |
| CL-V1-18 | 03F §2 V1-18 | see 03F | see 03F | C-03 | B10, LED-01, LED-02, R6, R7, T10, V1-18, W5 | REGISTERED |
