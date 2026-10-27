# WePLD V3 Master Plan

```text
STATUS = CANDIDATE MASTER PLAN (planning only; no implementation authority until accepted under trusted-base governance)
DATE = 2026-10-27
REPOSITORY = TheHalfMoon/wepld (PUBLIC since 2026-10-27) · branch docs/v3-unified-replan-20261027
BASE = main @ 0a843a2c0913236d9c93b31abb0d54bbdb023f23 (integrity GREEN on re-run 2026-10-27)
LEADING_ARCHITECTURE = T3-first fork + selected Orca modules + existing WePLD Rust Trusted Core (ADR-001)
VERDICT = CONDITIONAL GO (gates in §10)
```

This document is the single entry point. It summarizes and binds the detailed documents; where they differ, the
detailed document named in each section governs, and any contradiction is a defect to report (Astro checklist).

---

## 1. Product

**WePLD is a local-first, multi-vendor desktop workbench that combines an IDE and an AI workspace, where any model or
agent does engineering and knowledge work, and where a Rust Trusted Core decides which mediated effects are allowed,
records what actually happened (including unknown outcomes), remembers the project across models and decides what
counts as done.** (00 §1; 07 §6 for the exact trust claim per phase.)

What it must deliver (13_REQUIREMENTS_REGISTER: 25 product, 17 security/durability, 9 non-functional, 10 governance,
18 Claude-parity requirements = 79):

| Area | Delivered by | Phase |
|---|---|---|
| Unified IDE + AI workspace | T3 shell (chat, code sessions, files, terminal, browser preview, diff/PR review) + Monaco editor, LSP, debugging | P2, P6 |
| Multi-agent orchestration | T3 orchestration-v2 (threads, runs, subagents, steer/interrupt, worktrees) + per-role pins + reviewer ≠ builder | P2, P5 |
| Claude-equivalent capabilities | 377 census rows mapped (03F); v1-gating V1-01…18; Design Studio; documents; research; browser/computer use | P2–P9 |
| Durable missions, recovery, memory | Core Ledger (missions, continuations, receipts) + Brain (index over repo specs + notes) + T3 recovery gated by Core | P3, P4 |
| Git, terminals, worktrees, debugging, review | T3 VCS/checkpoints/terminal; DAP debugging; Monaco + diff comments; findings + Trusted Completion | P2, P5, P6 |
| Controlled computer and browser use | T3 Playwright-over-CDP browser automation + Orca computer-use helpers, both Core-gated with hard-blocked categories | P9 |
| Security, permissions, trusted completion | Nawat PDP in Core; Server PEP at seams S1–S8+S4b; WebAuthn approvals; MEDIATED/UNMEDIATED; containment floor (P3) and OS sandbox (P8) | P3, P5, P8 |
| Windows, macOS, Linux | Windows x64 first (NSIS, OV-signed); macOS DMG notarized; Linux AppImage/deb | P2, P6 |
| Local-first, zero mandatory cloud | No hosted service; BYO model credentials; optional self-hosted runner | P2, P10 |

## 2. Architecture (binding detail: 07; durability: 05)

```text
WePLD Desktop (Electron 44, forked T3)  ── renderer (React) ─ preload ─ desktop main (windows, updater, browser panes, WebAuthn UI)
        │ WebSocket RPC (T3 protocol, WePLD-1)
WePLD Server (Node, forked T3 apps/server) = Policy ENFORCEMENT POINT, part of the TCB
        orchestration-v2 (statev2.sqlite: conversation/run truth) · EffectWorker (sole executor) · providers · PTYs · VCS · /mcp
        LSP/DAP managers (P6) · design service (P7) · browser automation broker (P9)
        │ stdin/stdout framed JSON (existing S1 protocol, v2: direction-tagged ids, chunking, fencing epoch)
WePLD Core (Rust, existing crates) = Policy DECISION POINT + Ledger + Brain + identity + containment launcher
        ledger.sqlite (append-only, hash-chained, FULL sync) · Nawat policy · WebAuthn verify · S2 identity/evidence/git observer
```

**One authority per fact** (07 §2): T3 owns conversation/run state; Core owns grants, decisions, dispatches, outcomes,
missions, continuations, completion and Brain notes; git owns code; repo owns specs/ADRs; providers own their transcripts.
No fact has two writers. Effect lifecycle: `propose → (approval with WebAuthn) → dispatch (fsync before release) →
report | reconcile`, replay classes SAFE / RECONCILABLE / NEVER (05; Spec 006 §19).

## 3. Decisions (ADR.md, ADR-001…011, plus additions)

| ADR | Decision | Status |
|---|---|---|
| 001 | T3 fork foundation + Orca module ports + Rust Core | proposed; G2/G3 gated |
| 002 | Electron (inherited) over Tauri; revisit on RAM budget failure | proposed |
| 003 | Monaco; LSP client chosen by 1-week spike (`@vscode/monaco-lsp-client` alpha vs monaco-languageclient) — R13 §2 | **amended** |
| 004 | One authority per fact; S4b recovery gating; per-run receipt link | proposed |
| 005 | T3 executor + Core continuations; Vercel/durable-harness patterns only | proposed |
| 006 | Brain = notes + index over repo specs; preferences candidate→qualified | proposed |
| 007 | Core-only PDP; WebAuthn approvals; MEDIATED/UNMEDIATED; containment floor | proposed |
| 008 | Workers: Claude (API key), Codex, ACP family, OpenCode, Pi, local models, CLI agents (UNMEDIATED) | proposed |
| 009 | Self-hosted runner as project home; no WePLD cloud | proposed |
| 010 | Visibility: **PUBLIC since 2026-10-27** (founder); enforcement plan (Pro/Team vs advisory) still open | updated |
| 011 | Governance reset: one checker from base, protected paths, signed co-sign, risk tiers | proposed |
| 012 (new) | Debugging via DAP with server-side client (`@vscode/debugprotocol`, MIT), React panels, VS Code/OpenSumi MIT code as donors; Theia (EPL-2.0) reference only; debug effect classes always gated; debugpy from user env (pydevd EPL not bundled) | proposed (R13 §1) |
| 013 (new) | Signing/updates: OV code-signing cert + cloud HSM + jsign; electron-updater Generic provider with ed25519-signed manifest verified by Core (Azure Trusted Signing unavailable to the founder — R13 F1) | proposed |
| 014 (new) | Sandboxes: Codex Windows backends (restricted token; elevated sandbox users + WFP service; MXC) — not AppContainer; macOS Seatbelt; Linux bubblewrap + seccomp; separate debug profile because seccomp denies ptrace (R13 F3–F4); anthropics/sandbox-runtime (alpha Windows backend) as reference | proposed |

## 4. Copy First (binding detail: 06 + R11 + R12)

| Component | Upstream @ pin | Mode | Destination | Manifest |
|---|---|---|---|---|
| Shell/server/orchestration/providers | pingdotgg/t3code @36d4d711 (alt. stable v0.1.3 @d2c44031, decided in B-03) | FORK (KEEP/STRIP/MODIFY per file) | `apps/*`, `packages/*`, `native/*` | R11 |
| Design Mode capture, TUI catalog + status, process-host, Linear, computer use, diff comments | stablyai/orca @e310a636 | PORT / COPY AS-IS | `packages/*`, `native/computer-use-*` | R12 |
| Sandboxes, exec policy, network proxy | openai/codex @603a7baf (codex-rs crates) | ADAPT into Core | `crates/sandbox-*` | R12 |
| Policy engine | cedar-policy/cedar @2c2b8477… | DEPEND | Core | R12 |
| ACP / MCP SDKs | agentclientprotocol/*, modelcontextprotocol/* | DEPEND | Server/Core | R12 |
| Editor, LSP, DAP | microsoft/monaco-editor @dbf1945d; `@vscode/debugprotocol`; LSP client per spike | DEPEND / PORT | `apps/web` | R12, R13 |
| Canvas, tokens, element mapping | excalidraw @808d068e, style-dictionary @f82e7aaf, onlook ideas @423e2e92 | DEPEND / ADAPT | `packages/design-*` | R12 |
| Existing Rust Core | WePLD `crates/{contracts,core}` @0a843a2 | KEEP | `crates/*` | — |
| Vercel Workflow / durable-harness | vercel/workflow @af8c6d32; durable-harness @ea8aa406 | PATTERN ONLY | — | 05 |

Legal: MIT/Apache notices retained in generated `third-party-licenses.json` and `THIRD_PARTY_NOTICES/`; founder
rights recorded as `FOUNDER-ATTESTED` (never disclosed); no product code is copied during planning.

## 5. Roadmap (binding detail: 08 + 14)

| Phase | Outcome | Tasks | ESTIMATE pw |
|---|---|---|---|
| P−1′ | CI restored — **DONE** (main green 2026-10-27) | 2 | 0.2 |
| P0 | Governance reset | 6 | 1.4–1.9 |
| P1 | Measured donor baseline | 7 | 1.4–1.9 |
| P2 | Branded multi-agent workbench (first useful stop) | 16 | 11–19 |
| P3 | Trusted Core: authority, ledger, WebAuthn, recovery (differentiator stop) | 22 | 24–37 |
| P4 | Missions, Brain, continuations | 7 | 5–9 |
| P5 | Review, Trusted Completion, Connections (**v1 complete**) | 8 | 5–8 |
| P6 | Editor, LSP, debugging, CLI agents, Design Mode, packaging, accessibility, benchmarks | 11 | 30–54 |
| P7 | Design Studio | 8 | 9–15 |
| P8 | OS sandbox (Win/mac/Linux) + debug profile | 6 | 9–15 |
| P9 | Documents, research, browser automation, computer use | 5 | 13–22 |
| P10 | Runner + phone/web approvals | 4 | 4–8 |
| **v1 (P−1′…P5)** | | **68** | **≈ 49–76** |
| **All** | | **102** | **≈ 114–189** |

At ~1 pw/week of AI-assisted output minus 25–43% upkeep after P2, **v1 ≈ 14–27 months; full plan ≈ 3–6 years** for a
solo founder. This is the honest bottom-up figure (14 §13, computed). It argues for: stopping points at P2 and P3,
strict v1 scope, and deferring P6–P10 breadth unless capacity grows. Critical path: 14 §14.

## 6. Quality, security, recovery (binding detail: 09)

Mutation-controlled negative tests (T1–T17), recovery suites R1–R11 + W1–W9 with invariants I1–I6, benchmarks B1–B13
with explicit baselines (T3 Supervised, Orca), Design AT-01…23, Claude parity V1-01…18, CC-T01…05. Budgets are targets
until P1/P3 measurements.

## 7. Claude parity (binding detail: 03, 03E, 03F, CLAUDE_STUDY_COVERAGE_GAPS)

All census rows are accounted (route + phase). Documentation-only research is never presented as hands-on: **no Claude
UI feature has been exercised**; depth levels per row are in `CLAUDE_STUDY_COVERAGE_GAPS.md`.

## 8. Feature-completeness assessment

| Requirement class | Count | Mapped to task + test | Notes |
|---|---|---|---|
| Product (PR) | 25 | 25 | 15_TRACEABILITY_MATRIX |
| Security/durability (SEC) | 17 | 17 | |
| Non-functional (NF) | 9 | 9 | budgets unmeasured |
| Governance (GOV) | 10 | 10 | |
| Claude v1 parity (CL-V1) | 18 | 18 | Backlog rows accounted, not required |
| **Total** | **79** | **79 (0 gaps)** | generated, deterministic |

## 9. Limitations (no rounding up)

1. Nothing was built or run except reading code, `--help`, and CI re-runs; all estimates are ESTIMATES.
2. No hands-on Claude UI observation; 267/377 census rows rest on summary-read or non-Help-Center evidence rather than a full-text Help Center read (CLAUDE_STUDY_COVERAGE_GAPS).
3. Provider-side settings of installed GitHub Apps are not readable from this session (EGRESS_PREFLIGHT).
4. OV certificate availability/price for a Saudi individual/company: UNKNOWN (R13).
5. WebAuthn inside Electron on the founder's hardware: unproven until C-13.
6. T3/Orca upstream keep moving (pin drift recorded); fork-not-track accepted.

## 10. GO / NO-GO gates

| Gate | Condition | State |
|---|---|---|
| G1 | CI green on main | **MET (CI)**; governance reset pending P0 |
| G2 | T3 builds/runs/tests on Windows; baseline measured (B-03/B-04) | pending |
| G3 | Core seam spike passes in ≤ 3 pw (C-01) | pending |
| G4 | Claude SDK/auth posture (installer exclusion or written Anthropic answer) | pending |
| G5 | Founder signs FOUNDER_DECISION_RECORD F1–F11 | pending |
| NO-GO triggers | G2 fails in 2 pw; C-01 needs Orchestrator rewrite or > 3 pw; B2 RAM budget fails twice | — |
