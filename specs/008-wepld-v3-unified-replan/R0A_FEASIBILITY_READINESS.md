# R0a Feasibility Readiness Packet

```text
PURPOSE = conditions under which the founder may run the R0a First Working Build feasibility step, approvable by Astro
          independently of R1 and of any distribution.
SCOPE = tasks Q-00..Q-06 (14 PF), tests LIC-02, SRC-02, FWB-01..04, EGR-02, EGR-03, CI-02, PKG-01, PKG-02 (23 §13)
NOT_IN_SCOPE = testers, public artifacts, merging to main, any Core/authority/containment claim, R1 approval
STATUS = FOUNDER-DIRECTED Q-00 START; no R0a source import, artifact or runtime PASS established. See OPUS_R0A_BUILD_EXECUTION_2026-11-02.md.
```

## 1. Approval conditions (all must hold before Q-01 starts)

| # | Condition | Evidence required |
|---|---|---|
| A1 | Astro round 3 accepts this packet (R0a scope only) | round-3 report |
| A2 | Founder direction dated 2026-11-02 authorizes only bounded Q-00..Q-06 subject to A3–A7; local isolated `build/first-working`, no main merge, PR or public artifact (FO-14) | OPUS_R0A_BUILD_EXECUTION_2026-11-02.md + local branch/workspace record |
| A3 | Q-00 pre-admission record completed and independently reviewed (T2): pins, toolchain/action SHAs, frozen lockfile policy, shipped-closure license listing, removal decisions | Q-00 record + review |
| A4 | **LOCAL_ONLY Windows x64 selected**; no hosted or paid route and no public artifact/log. A private repo is a later separate decision requiring actual billing cap, private access and retention evidence. | Q-00 local capacity/zero-cost report; PKG-02 design |
| A5 | Isolated execution environment: separate local Windows user account; no T3 data in that account; founder credentials limited to one declared provider route | Q-05 setup note |
| A6 | Declared provider route for the smoke: Codex (founder's own login) or a named ACP agent; Claude excluded until F-06 | FO-15 decision |
| A7 | Independent reviewer route for T2 review named (FO-12) or the step is REVIEW_BLOCKED | founder decision |

## 2. Procedure and stop rules

1. Start Q-00 read-only immediately; evidence A3–A7 first. Then Q-01 → Q-02/Q-03 (inventories first, then overlays) → Q-04 (complete native Windows + Windows CLI SEA DAG in OPUS_R0A_BUILD_EXECUTION_2026-11-02.md) → Q-05 → Q-06 while blockers remain.
2. Stop and report if: a donor secret is required by a step that cannot be removed; any packaged-content artifact would be
   publicly reachable; PKG-01 finds SDK modules after provider-disabled bundling; the build needs paid resources.
3. Record for every run: commit/overlay digests, toolchain versions, cold-cache wall time per DAG node, peak RAM, disk used,
   failures with reproductions.

## 3. Exit criteria

| Outcome | Condition | Next |
|---|---|---|
| `FIRST_WORKING_BUILD_PASSED` | FWB-01 all steps pass; FWB-02..04, EGR-02/03, PKG-01/02, LIC-02, SRC-02, CI-02 pass | re-estimate R0b/R0 from measurements; propose R0b |
| `FEASIBILITY_COMPLETE_WITH_FAILURES` | procedure completed; blockers recorded | continue Q-06 or re-plan with measured data |
| `PARTIAL_SMOKE_NO_CREDENTIALS` | only the provider turn missing | obtain credentials; not a pass |

## 4. Estimate statement

Generated R0a effort (GENERATED_PLAN_REPORT §3) is a **known-work estimate subtotal of 2.80–7.60 person-weeks**, not a statistical lower bound, delivery cap, or calendar commitment. Q-06 is unmeasured and excluded. After Q-05, record measured costs and revise estimates/plan reports with independently reviewed evidence.

## 5. Claims allowed after PASS (and nothing else)

The four R0a claims in 24 §6, each tied to its passing test. No distribution, licensing, security or authority claim.
