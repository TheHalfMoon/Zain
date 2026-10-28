# Zain V3 Master Plan

```text
STATUS = CANDIDATE MASTER PLAN, revision 3 (after Astro round 1: DO NOT APPROVE @b9450598). Planning only; no
         implementation authority until accepted under trusted-base governance.
DATE = 2026-10-28
PRODUCT = Zain (formerly WePLD — legacy name; see ZAIN_NAMING_MIGRATION.md)
REPOSITORY = TheHalfMoon/Zain (ID 1334408699, PUBLIC) · branch docs/v3-unified-replan-20261027
SEPARATE_PROJECT = TheHalfMoon/Zain-LLM (private) — not part of this plan, never modified
BASE = main @ 0a843a2c0913236d9c93b31abb0d54bbdb023f23
LEADING_ARCHITECTURE = T3-first fork + selected Orca modules + existing Rust Trusted Core (ADR-001)
APPROVAL_ASKED = a bounded first release (R1 "Zain Trusted Starter") with the exact claims in 21 §3 — not the whole scope
SINGLE_SOURCE = numbers come from tools/plan_graph.py → GENERATED_PLAN_REPORT.md; this file embeds only its generated block
```

Single entry point. Detailed documents govern; any contradiction is a defect. Astro round-1 dispositions:
`ASTRO_FINDINGS_DISPOSITION.md`.

## 1. Product (full vision preserved)

**Zain is a local-first, multi-vendor desktop workbench that combines an IDE and an AI workspace, where any model or agent
does engineering and knowledge work, and where the Zain Trusted Core decides which mediated effects are allowed, records
what actually happened (including unknown outcomes), remembers the project across models and decides what counts as done
— and says exactly what it could not observe.**

| Capability (founder-requested) | Delivered by | Release |
|---|---|---|
| T3 + Orca unified IDE (Monaco editor, terminal, diff, worktrees) | T3 fork + F-17 Monaco; Orca ports I-02/I-05/I-06 | R0 (core), R3 (LSP, DAP, Orca ports) |
| Multi-agent orchestration | T3 orchestration-v2, per-role pins, reviewer ≠ builder | R0, R1 |
| Zain Trusted Core + Project Brain | Rust Core: PDP, ledger, approvals, coverage, missions, Brain | R1 (authority), R2 (missions, Brain) |
| Zain Code Review (Alibaba OCR + qualified Continue rule import) | delegated mode default (R1/R2); OCR engine lane local-only, qualified then productized (R3) | R1, R2, R3 |
| PStack-derived Engineering System + E2E | E-01..E-07 (E2E source pending FO-9) | R2 (shipping E-06 in R3) |
| AI Hero (mattpocock) skills in Plan Mode | L-01..L-10 | R0 (unenforced), R1 (read-only profile), R2 (UI, skills) |
| Zain Browser | one BrowserController; Preview/Test/Agent lanes; connection-level egress (Y-10); user-session lane | R0 hardening, R1 gating, R2 lanes, R6 general web |
| DeskGate | Desktop Commander tools as Core-mediated adapters over fs-gate and ProcessHost | R1 (local), R3 (search, parity), R7 (remote) |
| Claude-equivalent capabilities | 03F §2 V1-01…18 with parity labels (03F §2b); census = inventory | R0–R7 |
| Design Studio | D-01..D-08 | R4 |
| OS sandbox | S-01..S-06 | R5 |
| Documents, research, computer use | W-01..W-05 | R6 |
| Runner, phone approvals, remote DeskGate | R-01..R-04, H-06 | R7 |

No founder-requested capability is removed; costly items are scheduled into named later releases with their tasks and
acceptance tests intact.

## 2. Architecture (07, 16 §1) and trust boundaries (17, 18, 19)

```text
Zain Desktop (Electron, forked T3) ── renderer ─ preload ─ desktop main (windows, updater, browser panes)
        │ WebSocket RPC (Zain-1)
Zain Server (Node, forked T3) = policy ENFORCEMENT POINT (TCB)
        orchestration-v2 · EffectWorker (sole executor) · providers (18) · ProcessHost (17 §3) · fs-gate (19 §3)
        BrowserController + egress proxy (19 §1) · review service (snapshot, delegated/engine) · DeskGate adapters
        │ framed JSON (protocol v2, fencing epoch)
Zain Trusted Core (Rust) = DECISION POINT + ledger (17 §5) + coverage (17 §2) + reconciliation (17 §1) + Brain
        └─ zain-approve (Core-owned approval surface, 17 §4)
```

Trust statements that changed in revision 3:
- **Launch authorization ≠ execution coverage.** Shells/interpreters/CLI agents make coverage UNKNOWN; Trusted Completion
  fails closed on UNKNOWN required coverage and otherwise reports only authorized-content equivalence, never trust (17 §2).
- **Providers:** only qualified provider × operation cells are in the trusted tier (18); OpenCode and Pi are untrusted
  until patched.
- **Reconciliation:** per-operation evidence contracts; remote state never proves absence unless monotonic (17 §1).
- **Processes:** ProcessHost with Job Objects created atomically; retries only after proven quiescence (17 §3).
- **Approvals:** canonical binding + Core-owned surface; levels A1/A2/A3 recorded and shown (17 §4).
- **Ledger:** envelope hash over all authoritative fields; unanchored interval reported, not hidden (17 §5).
- **Browser:** external origins in agent lanes only behind connection-level egress enforcement (19 §1).
- **Review:** immutable screened snapshot, manifest allowlist, local-first, cloud only via mediated proxy (19 §2).
- **Files:** one handle-based write path with reparse/symlink rejection (19 §3).

## 3. Decisions (ADR.md)

ADR-001…019 as amended, plus ADR-020 Execution coverage and Trusted Completion scope, ADR-021 Provider enforcement matrix,
ADR-022 Approval presentation and credential lifecycle, ADR-023 Release tiers and zero-mandatory-cost path,
ADR-024 Process lifecycle (ProcessHost) and handle-based file operations.

## 4. Copy First and admission (06, 22, R11, R12, R14–R18)

Admission levels L1–L4 (22): only L4 sources ship. v1 removals: `heic-to` (LGPL-3.0), `electron-webauthn` (no declared
license), `@cursor/sdk`. Codex sandbox crates are post-v1 with their full closure; windows-sandbox-service reference only;
bubblewrap not vendored. Orca process-host is reference only (C-25 replaces it). Remote Desktop Commander relay EXCLUDED.

## 5. Releases, effort and calendar (generated)

<!-- GENERATED:BEGIN release-table (tools/plan_graph.py) -->
| Release | Tasks | Effort pw | Unmeasured tasks | Elapsed weeks (A-1; upkeep 35–60% after R0) |
|---|---|---|---|---|
| R0a | 7 | 2.8–7.6 (lower bound) | 1 | 2.8–7.6 |
| R0b | 17 | 6.1–12.9 (lower bound) | 2 | 6.1–12.9 |
| R0 | 44 | 15.15–29.15 (lower bound) | 2 | 15.2–29.1 |
| R1 | 84 | 60.3–97.3 (lower bound) | 2 | 84.6–199.5 |
| R2 | 130 | 104.55–167.6 (lower bound) | 2 | 152.7–375.3 |
| R3 | 149 | 141.3–232.85 (lower bound) | 2 | 209.2–538.4 |
| R4 | 157 | 150.5–247.55 (lower bound) | 2 | 223.4–575.1 |
| R5 | 163 | 160.8–265.35 (lower bound) | 2 | 239.2–619.6 |
| R6 | 168 | 174.3–287.85 (lower bound) | 2 | 260.0–675.9 |
| R7 | 173 | 179–297.15 (lower bound) | 2 | 267.2–699.1 |
| PD (optional paid track) | 3 | 1–2 | 0 | not scheduled |
<!-- GENERATED:END release-table -->

Details, critical paths and per-phase numbers: `GENERATED_PLAN_REPORT.md`. Model: A-1 = 1 person-week per calendar week
(unvalidated), upkeep 35–60% of capacity after R0, no acceleration or contingency. Re-run the script with measured
capacity after P1–P3.

**Revision 4 (Astro round 2):** R0a is now a founder-only feasibility build with the complete T3 build DAG, T2 review,
no public artifact and a strict PASS (install, launch, terminal, worktree, diff, real provider turn); readiness packet
`R0A_FEASIBILITY_READINESS.md`. R1 claims are generated templates over the enumerated provider surface (18 §4, 21 §3).
Dispositions: `ASTRO_ROUND_2_FINDINGS_DISPOSITION.md`.

**Time to a working app (24):** the First Working Build (R0a) is T3 at the pin with two overlays, built by copying T3's
own Windows release job — no rebuild from scratch, no claims, founder-only; its effort is CONDITIONAL (24 §4) until Q-05
measures it. R0b adds only what is needed before testers; qualified R0 no longer includes Monaco, C-00 or Core packaging
(moved to R1, not removed) and no longer double-counts learning, import, build and rebrand work (24 §8).

**Recommendation:** authorize R0a/R0b on an isolated branch after Astro round 2, and approve the path to **R1 Zain Trusted Starter** (21): Windows x64; T3 workbench with Monaco,
terminal, diff, worktrees; Claude and Codex as the qualified trusted-tier providers; Core decisions, signed approvals,
UNKNOWN outcomes and coverage reporting; Plan Mode with read-only profile; delegated code review with one findings schema.
Re-plan R2 with measured velocity.

## 6. Zero-mandatory-cost path (10 §1, 21 §4)

R0–R7 require no paid service: unsigned builds for development and self-distribution, local models, GitHub Free (public
repo), free self-screening of the name with a working-name rule. Paid items are confined to the optional distribution
track PD (code signing, notarization, trademark counsel/filing) and never gate a mandatory task. Independent review: a
qualified no-cost reviewer route must be named per phase; if none can run, the gate is `REVIEW_BLOCKED` (never PASS).

## 7. Quality and evaluation (09, 23)

335 registered tests; every negative names guard, mutant, fixture and observable failure; reviewer quality is measured
separately (ZCR-Q*). The validator proves that every test runs only after its implementation prerequisites.

## 8. Feature completeness

Requirements: 13 (incl. new SEC-22…27, GOV-13, PR-24b). Traceability (15, generated) classifies each requirement as
REGISTERED, FREE_TEXT_ONLY or GAP; mapping is accounting, not proof of semantics. Claude census rows are inventory; parity
labels in 03F §2b.

## 9. Limitations

1. Reading-based research only; nothing was built or run; all efforts are ESTIMATES; no Claude UI feature was exercised.
2. Windows mechanisms (Job Objects for ConPTY, webauthn.dll from a Core-owned window, handle-relative fs ops, session
   proxy coverage) are unproven until C-00.
3. Upkeep and capacity assumptions are unvalidated; calendars are long.
4. E2E donor unresolved (FO-9); trademark risk HIGH (FO-8, handled by working-name rule + PD N-05).
5. Same-user adversaries and process escapes remain residual risks before P8 and are stated in claims.
6. Provider-side settings of installed GitHub Apps unreadable (EGRESS_PREFLIGHT).

## 10. Gates

| Gate | Condition | State |
|---|---|---|
| G1 | CI green on main | MET |
| G2 | T3 builds/runs/tests on Windows; baseline (B-03/B-04) | pending |
| G2b | Windows feasibility C-00 (FG-01..05) decides approval level and early claims | pending |
| G3 | Core seam spike C-01 ≤ 3 pw | pending |
| G4 | Claude SDK/auth posture | pending |
| G5 | Founder signs FOUNDER_DECISION_RECORD incl. R1 scope and claims (FO-10) | pending |
| G6 | Astro round 2 approves R1 scope | pending |
