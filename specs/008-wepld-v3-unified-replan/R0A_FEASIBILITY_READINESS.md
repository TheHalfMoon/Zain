# R0a Feasibility Readiness Packet

```text
PURPOSE = conditions under which the founder may run the R0a First Working Build feasibility step, approvable by Astro
          independently of R1 and of any distribution.
SCOPE = tasks Q-00..Q-06 (14 PF), tests LIC-02, SRC-02, FWB-01..04, EGR-02, EGR-03, CI-02, PKG-01, PKG-02 (23 §13)
NOT_IN_SCOPE = testers, public artifacts, merging to main, any Core/authority/containment claim, R1 approval
STATUS = PROPOSED; nothing has been executed
```

## 1. Approval conditions (all must hold before Q-01 starts)

| # | Condition | Evidence required |
|---|---|---|
| A1 | Astro round 3 accepts this packet (R0a scope only) | round-3 report |
| A2 | Founder authorizes R0a execution on an isolated branch `build/first-working`, no merge to main (FO-14) | founder decision record |
| A3 | Q-00 pre-admission record completed and independently reviewed (T2): pins, toolchain/action SHAs, frozen lockfile policy, shipped-closure license listing, removal decisions | Q-00 record + review |
| A4 | Build location chosen: local founder machine, or a private build repository using GitHub Free private minutes (FO-15); **no public artifact or packaged-content log** | FO-15 decision; PKG-02 design |
| A5 | Isolated execution environment: separate local Windows user account; no T3 data in that account; founder credentials limited to one declared provider route | Q-05 setup note |
| A6 | Declared provider route for the smoke: Codex (founder's own login) or a named ACP agent; Claude excluded until F-06 | FO-15 decision |
| A7 | Independent reviewer route for T2 review named (FO-12) or the step is REVIEW_BLOCKED | founder decision |

## 2. Procedure and stop rules

1. Q-00 → Q-01 → Q-02/Q-03 (inventories first, then overlays) → Q-04 (DAG in 24 §3) → Q-05 → Q-06 while blockers remain.
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

Generated R0a effort (GENERATED_PLAN_REPORT §3) is a **lower bound** because Q-06 is MEASURE. No date is promised. After
Q-05 the measured numbers replace the Q-02..Q-06 estimates in 14 and the generator is re-run.

## 5. Claims allowed after PASS (and nothing else)

The four R0a claims in 24 §6, each tied to its passing test. No distribution, licensing, security or authority claim.
