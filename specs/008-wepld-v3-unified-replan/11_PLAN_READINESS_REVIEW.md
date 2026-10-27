# 11 — Plan Readiness Review

```text
REVIEW_TYPE = adversarial, independent of the drafting session (separate agent context, read-only, 2026-10-27)
INPUT = draft 1 of this package (commit b62fb7c on docs/v3-unified-replan-20261027)
FINDINGS = 3 Critical, 9 High, 9 Medium, 7 Low — every one verified against files by the reviewer
DISPOSITION = all Critical/High fixed in revision 2; Medium fixed or converted to owned unknowns; Low fixed
REVIEW_LIMITS = model reviewer, not a qualified hosted reviewer (CodeRabbit etc.); this does NOT satisfy BUILD_METHOD
                independent review for merge — the PR still needs the canonical review route (T0 docs-only).
```

## 1. Findings and dispositions

| ID | Sev | Finding (short) | Disposition | Where fixed |
|---|---|---|---|---|
| C1 | Critical | "Human token" for approvals unspecified; Core could not verify; renderer/Server could forge; no remote story | **Fixed**: WebAuthn assertion over a Core challenge, verified by Core against registered credentials; same for policy/mode changes; remote via paired passkey; interim "Server trusted for approvals" stated | 07 §3, §6; 05 §4.3, §7.1; 08 P3; 09 T3; ADR-007 |
| C2 | Critical | Trust claim overstated: Server is PEP/TCB; v1 has no sandbox; CLI agents and native tools bypass Core | **Fixed**: product definition limited to mediated effects; TCB named; MEDIATED/UNMEDIATED tagging; completion refuses UNMEDIATED-only changes; P3 containment floor | 00 §1; 07 §1, §6; ADR-007; 09 B11 |
| C3 | Critical | P0 cannot pass its own gate (main red on 403); no break-glass | **Fixed**: P−1 founder-signed break-glass record, single-path scope, then merge package under repaired gate | 08 P−1; 00 NEXT_BUILD_ENTRY, G1; FOUNDER F10 |
| H1 | High | T3 recovery requeues/auto-continues before Core reconciles → second writer/scheduler | **Fixed**: seam S4b — T3 recovery consults `core.open_dispatches` first; UI renders outcome only from Core; W9 test | 07 §2, §5; 05 §4.6; 02 §2–3; 09 W9; ADR-004 |
| H2 | High | T3 `synchronous=NORMAL` can roll back continuation receipts → double fire | **Fixed**: two-phase fires (`fire_intent`/`fire_acked`), receipt query on restart, T3 receipt table `synchronous=FULL`; W2b | 07 §5; 05 §4.9; 09 W2b; U-07-5 |
| H3 | High | Single writer / fencing / direction of ids / desktop+runner unspecified; per-project vs single ledger contradiction | **Fixed**: exclusive data-root lock, Core-minted epoch per handshake, direction-tagged id spaces, project-home rule, one ledger per data root partitioned by project | 07 §3, §4, §5; 05 §7.3; 10 K10 |
| H4 | High | Estimates inconsistent (P0–P5 summed 20–38 not 30–55; P3/P6 under-counted; no total) | **Fixed**: bottom-up rebuild — v1 ≈ 37–68 pw, all ≈ 72–138 pw; calendar 12–26 months to v1 stated; carried to 00, 10, FOUNDER | 08 overview; 00 §3, §7; 10 K6; FOUNDER |
| H5 | High | ADR-011 weakens governance: option (c) advisory; `pull_request` runs candidate YAML; label co-sign forgeable; substitute reviewer unnamed; tiers mis-assigned | **Fixed**: `pull_request_target` data-only checker; founder-only SSH-signed co-sign; named different-vendor substitute for T0/T1 only; P1/P2/P6 re-tiered T2; option (c) residual risk stated | ADR-010, ADR-011; 08 tiers; 10 K5 |
| H6 | High | Claude SDK enters installer before G4; ACP adapter has the same dependency; G4 fallback circular | **Fixed**: P2 SDK-exclusion task + installer-content gate; G4 fallback = user-consented SDK + API key; CLI-in-PTY stays UNKNOWN | 08 P2; 00 G4; 06 D14; 03C §3; 10 K13 |
| H7 | High | Unsandboxed agents can rewrite ledger/Brain | **Fixed (bounded)**: data-root deny floor in all provider profiles; WebAuthn-signed approvals; out-of-machine anchors; claim downgraded to "tamper-evident against corruption" before P8 | 07 §4; 09 T10b; 10 K15 |
| H8 | High | `observe` env flag = fail-open | **Fixed**: compiled out of release builds; dev-only with signed mode record + banner; T15 test | 07 §3; 08 P3; 09 T15 |
| H9 | High | ThreadSettlement auto-settles on merge; Brain stores specs (two authorities); preferences unqualified; invariants claim | **Fixed**: ThreadSettlement cosmetic only; Brain indexes repo specs; preferences CANDIDATE→QUALIFIED; invariant "Workers" line flagged for governed amendment | 02 §2; 07 §2; ADR-006; 00 §5 |
| M1 | Medium | Tautological/unfalsifiable tests and benchmarks; boilerplate 03F negatives; Codex `rm -rf` oracle passes without Core; strawman baseline; % overhead without baseline; B7 cost/run counts | **Fixed**: mutation-control rule; non-pinned recall; unknown-outcome metrics split; T1 oracle changed; B11 vs T3 Supervised; absolute per-effect budget (B13); B7 3 runs/task with hypothesis; 03F placeholders flagged | 09 header, §1–3; 03F legend |
| M2 | Medium | "$0 Windows CI" wrong for private repo; signing eligibility; P1 on main machine | **Fixed**: timing benchmarks local, CI functional only; signing eligibility UNKNOWN (U-07-4); P1 in Windows Sandbox/VM | 09 §3; 07 §9; 10 §1; 08 P1 |
| M3 | Medium | Runner does not actually run missions while laptop off | **Fixed**: project-home rule; claim narrowed to runner-homed projects | 07 §5, §8; 05 §7.3 |
| M4 | Medium | Orca hooks written into users' global `~/.claude`/`~/.codex`; spoofable loopback | **Fixed**: per-launch overlays; per-PTY secret; T17 | 06 D3; 09 T17; 12 |
| M5 | Medium | No dispatch fsync point for Claude-native tools | **Fixed**: dispatch inside PreToolUse before allow | 03C §2; 08 P3; ADR-007 |
| M6 | Medium | Donor path/pin errors (codex sandbox crate set, cedar core pin, style-dictionary org, missing SHAs, Onlook status) | **Fixed** | 06 D7, D9, D11, D19–D23 |
| M7 | Medium | Upkeep share and scope inflation unstated | **Fixed**: upkeep ≈ 25–43% stated; v1 scope line + cut order | 10 §3; 00 §7; 08 overview |
| M8 | Medium | Compaction-exempt per-effect events reintroduce growth; dangling T3 ids | **Fixed**: per-run aggregate `wepld.run-receipts`; tombstone-aware refs (`REFERENT_DELETED`) | 07 §4; ADR-004 |
| M9 | Medium | 11 missing; 4.5/4.7 prose; missing remote/W1/runner diagrams | **Fixed**: this file; diagrams added | 05 §4.5, §4.7, §7 |
| L1 | Low | "~10 weeks" → ~7 | Fixed | 01 H5 |
| L2 | Low | D3 3–6 vs 3–5; P7 below donor sum | Fixed (D3 3–5; P7 8–14) | 06; ADR-003; 08 |
| L3 | Low | P6 naming drift; telemetry phase contradiction | Fixed | 03F §1; 03C §1 |
| L4 | Low | Two `wepld` binaries coexist | Fixed: rename at P2 in one change | 07 §10; 08 P2 |
| L5 | Low | 64 KiB frame cap without chunking | Fixed: chunk frames | 07 §3 |
| L6 | Low | MCP license check scheduled P5 but SDK present at P2 | Fixed (U-06-1 → P2) | ASSUMPTIONS |
| L7 | Low | A vs B estimates not like-for-like | Fixed | 00 §3; FOUNDER |

## 2. Remaining inconsistencies / open evidence (not blockers for a planning merge)

| # | Item | Owner gate |
|---|---|---|
| O1 | All effort numbers are reading-based ESTIMATES; first actuals arrive in P1/P3 | P1, P3 G3 |
| O2 | WebAuthn inside Electron on the founder's hardware (Windows Hello) not yet proven | P3 spike (U-07-3) |
| O3 | Claude SDK redistribution and subscription-orchestration policy | G4 (U-03-1, U-03-2) |
| O4 | Whether T3 seams hold without Orchestrator rewrites | G3 |
| O5 | Claude census depth outside mandatory scope; no hands-on observation | per phase (U-03-3..5) |
| O6 | Before P8, a same-user unmediated agent can still tamper locally; only detection, not prevention | P8 |

## 3. Competing hypotheses considered and how they were decided

| Hypothesis | Evidence for | Evidence against | Decision |
|---|---|---|---|
| Orca's IDE breadth makes it the better foundation | Monaco, Design Mode, computer use, 45 CLI agents | three stores, 2.37M LOC, 421 Windows issues, cloud coupling, store-bound UIs | T3 foundation + Orca ports |
| T3's event log can be the single evidence log | single txn, receipts | compaction, snapshots, payload rewrite, outbox pruning, NORMAL sync | one authority per fact |
| Vercel Workflow should be the durable engine | well-tested, World spec | dev-only local World, compiler coupling, second orchestrator | patterns only |
| Keep Tauri to minimize RAM | smaller baseline | WePLD shell is a demo; donors and browser/Design features depend on Electron webContents; unmeasured gain | Electron, revisit on B2 |
| Keep the V2.3 governance mechanism | proven fail-closed semantics | 83.6k lines, ≥3 PRs per test fix, silently broken by visibility change | semantics kept, mechanism replaced |

## 4. Go / No-Go

```text
PLANNING PACKAGE READINESS = READY FOR FOUNDER DECISION (after this revision)
BUILD RECOMMENDATION = CONDITIONAL GO
CONDITIONS = G1 (P−1 break-glass + main green) · G2 (P1 measured baseline) · G3 (P3 seam spike) · G4 (Claude SDK/auth) ·
             G5 (founder signs FOUNDER_DECISION_RECORD F1–F11)
NO-GO TRIGGERS = G2 fails within 2 pw · G3 needs Orchestrator rewrite or >3 pw · B2 RAM budget fails twice after stripping
NEXT EXACT BUILD ENTRY = P−1: founder-signed break-glass record → change only `permissions:` in the integrity workflow(s)
                         → verify foundation-integrity green on main → merge this package → P0
```
