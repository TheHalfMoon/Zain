# Zain V3 Master Plan

```text
STATUS = CANDIDATE MASTER PLAN (planning only; no implementation authority until accepted under trusted-base governance)
DATE = 2026-10-28
PRODUCT = Zain (formerly WePLD — legacy name; see ZAIN_NAMING_MIGRATION.md)
REPOSITORY = TheHalfMoon/Zain (ID 1334408699, PUBLIC) · branch docs/v3-unified-replan-20261027
SEPARATE_PROJECT = TheHalfMoon/Zain-LLM (private) — not part of this plan, never modified
BASE = main @ 0a843a2c0913236d9c93b31abb0d54bbdb023f23 (integrity GREEN on unchanged re-run, 2026-10-27)
LEADING_ARCHITECTURE = T3-first fork + selected Orca modules + existing Rust Trusted Core (ADR-001)
VERDICT = CONDITIONAL GO (gates §10) — with an explicit scope decision required (FO-10)
```

Single entry point. Detailed documents named in each section govern; any contradiction is a defect for Astro to report.

## 1. Product

**Zain is a local-first, multi-vendor desktop workbench that combines an IDE and an AI workspace, where any model or agent
does engineering and knowledge work, and where the Zain Trusted Core decides which mediated effects are allowed, records
what actually happened (including unknown outcomes), remembers the project across models and decides what counts as done.**

| Area | Delivered by | Phase |
|---|---|---|
| Unified IDE + AI workspace (Zain IDE / Zain Desktop) | T3 shell + Monaco, LSP, DAP debugging | P2, P6 |
| Multi-agent orchestration | T3 orchestration-v2 + per-role pins + reviewer ≠ builder | P2, P5 |
| Claude-equivalent capabilities | 377-row census mapped (03F); V1-01…18; Design Studio; documents; research | P2–P9 |
| **Zain Code Review** | OCR engine fork + Zain findings/dispositions/fix pipeline (16 §2) | P5 (spike P2) |
| **Zain Engineering System** | PStack-derived loop + Playwright E2E (16 §3) | P5–P6 |
| **Zain Plan Mode** | mattpocock/skills + T3 plan mode + Core read-only profile (16 §4) | P2–P5 |
| **Zain Browser** | one BrowserController, Preview/Agent/Test lanes (+ user-session later) (16 §5) | P2–P5, P9 |
| **DeskGate** | Desktop Commander tools as Core-mediated adapters (16 §6) | P3, P6, P10 |
| Durable missions, recovery, Zain Project Brain | Core ledger + continuations + Brain index | P3–P4 |
| Git, terminals, worktrees, debugging | T3 VCS/checkpoints/terminal; DAP | P2, P6 |
| Controlled computer use | Orca computer-use helpers, Core-gated | P9 |
| Security, permissions, Trusted Completion | Nawat PDP, Server PEP, WebAuthn, MEDIATED/UNMEDIATED, containment floor (P3), OS sandbox (P8) | P3, P5, P8 |
| Windows / macOS / Linux | Windows x64 first (OV-signed); macOS, Linux | P2, P6 |
| Local-first, zero mandatory cloud | BYO credentials; optional self-hosted runner | P2, P10 |

## 2. Architecture (07, 05, 16 §1)

```text
Zain Desktop (Electron 44, forked T3) ── renderer ─ preload ─ desktop main (windows, updater, browser panes, WebAuthn UI)
        │ WebSocket RPC (Zain-1)
Zain Server (Node, forked T3) = policy ENFORCEMENT POINT (TCB)
        orchestration-v2 (conversation/run truth) · EffectWorker (sole executor) · providers · single PTY/process host
        BrowserController (Zain Browser) · review EngineRunner (Zain Code Review) · DeskGate adapters on /mcp
        LSP/DAP managers · design service · Plan Mode thread profile
        │ stdin/stdout framed JSON (S1 protocol v2)
Zain Trusted Core (Rust) = policy DECISION POINT + Ledger + Zain Project Brain + identity + containment launcher
```

One authority per fact; no duplicate orchestrators, review systems, browser controllers, PTY hosts or policy authorities
(16 §1). Effect lifecycle `propose → (WebAuthn approval) → dispatch (fsync) → report | reconcile`, replay classes
SAFE/RECONCILABLE/NEVER.

## 3. Decisions (ADR.md)

ADR-001…014 as before (foundation, Electron, editor/LSP, one authority per fact, executor + continuations, Brain,
authority/WebAuthn, workers, runner, visibility (now PUBLIC), governance reset, debugging, signing/updates, containment),
plus **ADR-015 Code Review (OCR fork)**, **ADR-016 Engineering System**, **ADR-017 Plan Mode**, **ADR-018 Zain Browser**,
**ADR-019 DeskGate**.

## 4. Copy First (06 + R11 + R12 + R14–R18)

| Component | Upstream @ pin | Mode | Rights |
|---|---|---|---|
| Shell/server/orchestration/providers | pingdotgg/t3code @36d4d711 | FORK | MIT + FOUNDER-ATTESTED |
| Design Mode, TUI catalog, process-host, Linear, computer use, diff comments | stablyai/orca @e310a636 | PORT | MIT + FOUNDER-ATTESTED |
| Sandboxes / exec policy / network proxy | openai/codex @603a7baf | ADAPT into Core | Apache-2.0 |
| Review engine | alibaba/open-code-review @375f64cd | FORK | Apache-2.0 + FOUNDER-ATTESTED |
| Engineering loop | cursor/plugins @ab1f702c `pstack/`, `cursor-team-kit` | ADAPT (renamed) | MIT |
| E2E | Playwright (Apache-2.0) + **UNRESOLVED source** (candidate TheHalfMoon/Ascout @ecada2bc) | PENDING FO-9 | founder-owned candidate |
| Planning skills | mattpocock/skills @59db609e | COPY/ADAPT | MIT |
| Browser | T3 broker/CdpRelay (fork) + Playwright @cfe490d9 (+ extension P9) | EVOLVE / PORT | MIT / Apache-2.0 |
| DeskGate | wonderwhy-er/DesktopCommanderMCP @db3430f2 | PORT adapters | MIT + FOUNDER-ATTESTED |
| Remote Desktop Commander relay | desktop-commander/remote-desktop-commander @a6573e86 | **EXCLUDED** (proprietary, not available) | — |
| Continue, PR-Agent, browser-harness, Browser Use | various | REFERENCE only | — |
| Policy, ACP/MCP, editor, canvas, tokens | Cedar, ACP/MCP SDKs, Monaco, Excalidraw, Style Dictionary | DEPEND | Apache-2.0 / MIT |
| Existing Rust Core | Zain `crates/{contracts,core}` @0a843a2 | KEEP (renamed to `zain-*` in N-04) | owned |
| Vercel Workflow / durable-harness | @af8c6d32 / @ea8aa406 | PATTERN ONLY | Apache-2.0 |

Notices preserved in generated `third-party-licenses.json` + `THIRD_PARTY_NOTICES/`; build fails on a missing notice.

## 5. Roadmap (08 + 14; totals computed in 14 §13)

| Phase | Outcome | ESTIMATE pw |
|---|---|---|
| P−1′ | CI restored — **DONE** | 0.2 |
| P0 | Governance reset (+ branch protection G-07) | 1.5–2.0 |
| P1 | Measured donor baseline (+ donor pins for new components) | 1.7–2.3 |
| P2-N | Zain naming clearance | 0.7 |
| (note) | LSP and debugging are P6 (post-v1) — accepted limitation under FO-10 | — |
| P2 | Branded workbench with Monaco editor (+ Plan Mode unenforced, browser hardening, review spike) | 15.1–24.6 |
| P3 | Trusted Core (+ DeskGate local, Plan read-only, browser effect classes) | 29.7–45.2 |
| P4 | Missions, Brain, plan approval → mission | 6.2–10.2 |
| P5 | Review/Completion/Connections + Code Review + Engineering + Plan UI + Browser v1 lanes | 36.1–55.5 |
| **v1 total (P−1′…P5)** | | **≈ 91–141** |
| P6 | IDE breadth, LSP, debugging, CI review, shipping, DeskGate search | 34.0–60.5 |
| P7 | Design Studio | 9.2–14.7 |
| P8 | OS sandbox | 9.3–14.8 |
| P9 | Documents, research, general web, computer use | 13.5–22.5 |
| P10 | Runner, remote DeskGate, phone approvals | 4.7–9.3 |
| **All** | | **≈ 160–259** |

### 5a. Release tiers (each usable on its own) — founder decision FO-10

| Release | Contents | Cumulative ESTIMATE pw | Calendar at A-1 (~1 pw/week, upkeep 25–43% after P2) |
|---|---|---|---|
| **R0 Zain Workbench** | P−1′…P2 (multi-agent IDE with Monaco editor, unenforced Plan Mode, hardened browser preview; no LSP/debugger yet) | ≈ 20–30 | ≈ 5–7 months |
| **R1 Zain Trusted** | + P3 (Core authority, ledger, WebAuthn, DeskGate local, enforced Plan read-only) | ≈ 50–76 | ≈ 14–25 months |
| **R2 Zain v1** | + P4 + P5 (missions, Brain, Code Review, Engineering loop, Browser v1, Plan UI) | ≈ 91–141 | ≈ 2.2–4.3 years |
| v1-core option | R2 minus K-08, E-04, E-05, Y-06, Y-07 (E-07 re-scoped to E-01..E-03) | ≈ 85–131 (≈ 82–126 if E-03 also cut while FO-9 is open) | ≈ 2–4 years |
| Later | P6–P10 | ≈ 159–259 total | multi-year |

This is the honest bottom-up result of the founder's full scope for one person. Recommendation: commit to **R0 → R1**
first (the authority differentiator), then re-plan R2 with measured velocity from P1–P3.

## 6. Quality, security, recovery (09 + component suites)

Mutation-controlled negatives (T1–T17, ZCR-*, ES-AT, Plan N1–N14, Browser R17 §11, DG-N01..N14); recovery R1–R11 + W1–W9;
benchmarks B1–B13; Design AT-01…23; Claude parity V1-01…18; CC-T01…05.

## 7. Claude parity (03, 03E, 03F, CLAUDE_STUDY_COVERAGE_GAPS)

377 rows accounted (route + phase). **No Claude UI feature was exercised hands-on**; 110 rows full-text, 212 summary-read with
gates re-checked, 55 from live non-Help-Center pages.

## 8. Feature completeness

90 requirements (30 product, 21 security/durability, 9 non-functional, 12 governance, 18 Claude parity rows V1-01…18 of which
V1-10…16 are v1.1+ tiers per 03F) → all mapped to ≥1 non-superseded task and ≥1 test (15, generated; superseded tasks excluded).
154 task rows (14), of which 4 are 0-pw SUPERSEDED placeholders kept for history.

## 9. Limitations

1. Reading-based research only; nothing was built or run except `--help` and CI re-runs; all estimates are ESTIMATES.
2. No hands-on Claude observation.
3. E2E donor unresolved (FO-9).
4. "Zain" trademark risk HIGH in KSA/GCC (R19; FO-8).
5. Provider-side settings of installed GitHub Apps unreadable (EGRESS_PREFLIGHT).
6. OV certificate availability for the founder UNKNOWN; WebAuthn in Electron unproven until C-13.
7. File-level manifests: T3 (R11) and other donors (R12) — see their completeness statements.
8. Upstreams keep moving (pins recorded; fork-not-track).

## 10. GO / NO-GO gates

| Gate | Condition | State |
|---|---|---|
| G1 | CI green on main | **MET** |
| G2 | T3 builds/runs/tests on Windows; baseline (B-03/B-04) | pending |
| G3 | Core seam spike ≤ 3 pw (C-01) | pending |
| G4 | Claude SDK/auth posture | pending |
| G5 | Founder signs FOUNDER_DECISION_RECORD (F1–F11, FO-8…FO-11) incl. scope tier (FO-10) | pending |
| NO-GO | G2 fails in 2 pw; C-01 needs Orchestrator rewrite or > 3 pw; B2 RAM budget fails twice | — |
