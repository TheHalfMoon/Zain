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
| R0 Zain Workbench | small usable release, **no authority claims** | governance reset, donor baseline, C-00 feasibility, fork/strip/rebrand, Monaco, terminal, diff, worktrees, unenforced Plan Mode, browser preview hardening, unsigned Windows build |
| **R1 Zain Trusted Starter** | **smallest release with authority claims** (proposed for approval) | R0 + Core (protocol v2, ledger envelope, effects, policy, approvals A1/A2, coverage model, ProcessHost, fs-gate, reconciliation contracts, S1–S8 seams for Claude/Codex/ACP, recovery suite, anchors) + delegated code review (K-04, K-05, K-08) + R1 exit X-01 |
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

## 3. R1 bounded-claims statement (shown in app and docs; X-01 verifies text equality)

```text
Zain Trusted Starter — what Zain claims (Windows x64):
1. Decisions: every effect requested through Claude (Agent SDK, API key) and Codex sessions, ACP agents qualified in the
   provider matrix, Zain terminals and Zain's MCP tools is decided by Zain Core before it runs; other workers
   (OpenCode, Pi, CLI agents in terminals) are labelled untrusted.
2. Approvals: approvals are signed by your platform authenticator and verified by Core; the approval level (A1/A2/A3)
   is shown. A1: the text you approve is drawn by Zain Core, not by the web UI.
3. Outcomes: effects interrupted by crashes are recorded as UNKNOWN until evidence proves APPLIED or NOT_APPLIED;
   Zain does not retry them automatically unless the operation is proven safe.
4. Coverage: when an agent runs a shell, interpreter or test runner, Zain cannot observe what that process does;
   coverage is shown as UNKNOWN. "Trusted" completion then covers only the content of the accepted files (tree
   provenance), not the absence of other side effects. Zain does not claim to contain processes before OS sandboxing.
5. Ledger: tamper-evident against corruption; anchored history is verifiable against signed anchors; the unanchored
   recent interval is shown and is not protected against a same-user attacker.
6. Browser: agent browser actions need grants and are limited to project loopback origins.
7. Review: code review runs in delegated mode on an immutable snapshot of the approved files; it is advisory and is
   never completion authority.
Not claimed: protection against a compromised Zain Server, same-user malware, processes that escape via system services,
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
