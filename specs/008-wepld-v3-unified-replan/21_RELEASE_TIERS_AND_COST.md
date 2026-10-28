# 21 — Release Tiers, First-Release Proposal, Cost and Calendar (Astro H-11, H-12)

```text
STATUS = PROPOSED. Numbers are generated (GENERATED_PLAN_REPORT.md §2–§6 by tools/plan_graph.py) — this file does not
         restate them except by reference, so they cannot drift.
MEMBERSHIP = 14 §16 (machine-read). Every release is validated as closed under declared dependencies and test
         prerequisites; no mandatory task depends on the paid distribution track PD.
```

## 1. Releases

| Release | Purpose | Contents (14 §16) |
|---|---|---|
| R0a First Working Build | founder-only feasibility; complete build DAG; never a public artifact; narrow tested claims (24 §6) | Q-00..Q-06 |
| R0b Tester Build | invited testers via an access-controlled channel; license removals, SDK absence, credentials, material defects fixed before distribution | R0a + B-06, F-20, F-05, F-06, F-07, F-11, F-21, F-22, Y-00, N-01 |
| R0 Qualified Workbench | **no authority claims** | R0b + governance reset, donor baseline, admission, strip/rebrand, inherited-bug fixes (reproduced only), accessibility, budgets, unenforced Plan Mode label; no built-in editor |
| **R1 Zain Trusted Starter** | **smallest release with authority claims** (proposed for approval) | R0 + C-00 feasibility, Monaco (F-17), Core packaging (F-10, F-18, N-04) + Core (protocol v2, ledger envelope, effects, policy, approvals A1/A2, coverage model, ProcessHost, fs-gate, reconciliation contracts, S1–S8 seams for Claude/Codex/ACP, recovery suite, anchors) + delegated code review (K-04, K-05, K-08) + R1 exit X-01 |
| R2 Zain v1 | full v1 | R1 + OpenCode/Pi qualification, DeskGate local, enforced Plan Mode, missions, Brain, continuations, completion, fixes, Engineering System, Browser lanes with connection-level egress, MCP/skills/MCPB |
| R3 | IDE breadth | LSP, DAP debugging, Orca ports, CLI agents, OCR engine lane (local, qualified), CI review, shipping, DeskGate search/parity, macOS/Linux packages |
| R4 | Design Studio | D-01..D-08 |
| R5 | OS containment | S-01..S-06 (widens claims) |
| R6 | General agent work | documents, research, user-session browser lane, computer use |
| R7 | Remote | runner, project home, phone approvals, remote DeskGate |
| PD | optional, paid | trademark counsel/filing (N-05), Windows signing (F-19), macOS notarization (I-12) |

Effort and elapsed time per release: GENERATED_PLAN_REPORT.md §3. The R1 increment over R0 is the Trusted Core; Astro's
round-1 fixes (coverage, ProcessHost, fs-gate, reconciliation, approval surface, provider matrix) added work rather than
removing it. No acceleration is assumed.

## 2. Why R1 is this size and not smaller

Astro's guidance: Windows; editor/terminal/diff; one or two qualified providers; explicit approvals and unknown outcomes;
simple planning; delegated review. R1 follows it: DeskGate, OpenCode/Pi qualification, enforced Plan Mode read-only,
missions/Brain, Engineering System, browser agent lanes and the OCR engine lane move to R2/R3 (kept, not deleted). What
cannot shrink without dropping a claim: ProcessHost (H-5), fs-gate (H-8), coverage (H-1), reconciliation contracts (H-4),
approval binding (H-6), ledger envelope (H-9). The alternative is R0 only, which makes no authority claim.

## 3. R1 claim templates (generated text; X-01 verifies equality — revised for A2-07, A2-10, A2-11, A2-13)

The R1 claim is assembled from templates; a template appears only if its qualification tests pass (CLM-01, CLM-02).

```text
Zain Trusted Starter — Windows x64. What Zain claims:
1. Decisions [from passing 18 §4 cells]: Zain Core decides, before execution, the operations listed in the
   "decided by Core" column for each provider shown as qualified. Operations listed as not decided (for example Codex
   known-safe reads, provider server-side tools, anything run inside a shell) are shown as UNMEDIATED. OpenCode, Pi and
   CLI agents in terminals are untrusted workers.
2. Grants [C-28]: approvals and grants are scoped, expire, and stop working after revocation or a Core restart epoch.
3. Approvals [level template, 17 §4.5]: exactly one of the A1 / A2 / A3 sentences, matching the active level.
4. Outcomes: interrupted operations are recorded as UNKNOWN unless an operation-specific receipt proves APPLIED or
   NOT_APPLIED (17 §1); Zain does not retry them automatically.
5. Coverage: when an agent runs a shell, interpreter or test runner, Zain cannot observe what that process does; this is
   shown as UNKNOWN. R1 makes no mission completion decision.
6. Ledger: tamper-evident against corruption; anchored history verifiable against signed anchors; the unanchored recent
   interval is shown and is not protected against a same-user attacker.
7. Browser: agents cannot drive the browser in this release.
8. Review: delegated review on qualified routes reads only the approved snapshot; it is advisory, not acceptance authority.
Not claimed: protection against a compromised Zain Server, same-user malware, processes escaping via system services,
network effects of shells, or anything on macOS/Linux.
```

## 4. Zero-mandatory-cost path

| Item | Mandatory? | No-cost route | Paid option (PD only) |
|---|---|---|---|
| Development, CI | yes | public repo, GitHub Free Actions + branch protection | — |
| Builds | yes | unsigned NSIS (F-11); SmartScreen warning documented; self-distribution only | F-19 OV/EV signing + cloud HSM |
| macOS | no (R3) | unsigned/ad-hoc DMG for testing | I-12 notarization ($99/yr) |
| Name | yes (identity) | N-01 self-screening memo + working-name rule (no public distribution under the name) | N-05 counsel + SAIP filing |
| Models | user's choice | local models; BYO keys | — |
| Independent review (GOV-03) | yes | named no-cost route per phase: (a) an independent model run by the founder on a different vendor/route than the builder, with the review recorded; (b) free hosted reviewers for public repos only after egress approval | paid reviewers optional |
| Benchmarks | R3 | local models; capped BYO spend set before B7 | — |

If no qualified no-cost reviewer can run for a phase, the phase is `REVIEW_BLOCKED` — never PASS; there is no silent
reduction of assurance gates. Public distribution under the name requires PD tasks N-05 (and F-19 for SmartScreen
reputation); until then releases are development/self-distribution builds.

## 5. Upkeep model (one source)

10 §3 base upkeep 1.1–1.85 pw/month + 10 §7 component additions 0.4–0.8 pw/month = 1.5–2.6 pw/month ≈ 35–60% of A-1
capacity. The generator applies u = 0.35 (low) / 0.60 (high) to all work after R0; the previous 25–43% figure is
withdrawn everywhere.
