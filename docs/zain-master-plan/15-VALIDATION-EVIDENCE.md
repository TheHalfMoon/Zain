# 15 — Validation Evidence

All commands were run on the founder's Windows machine on 2026-11-08, from the repository root of the local clone,
on branch `docs/zain-master-plan-20261108`. Outputs are copied verbatim except for path shortening.

## 1. Master-plan validator

```text
$ python -I docs/zain-master-plan/tools/zmp.py check
zmp check: errors=0 rows={'task-backlog': 210, 'dependency-edges': 440, 'acceptance-gates': 58,
  'capability-matrix': 61, 'source-registry': 42, 'risk-register': 25, 'ux-journeys': 22} v3_tasks=176 v3_tests=383
```

What it checks (fail-closed; each error has a stable code): CSV schemas and enums; unique, well-formed IDs; task
dependencies resolve; backlog dependencies equal hard edges; the combined graph (hard and gate edges) is acyclic;
no dependency on a later milestone or on the optional paid track; DONE requires evidence and finished prerequisites;
paid tasks only on the optional track; estimates well-formed and not reversed; task tests resolve to V3 registry tests
or gate IDs; gates reference existing tasks, no later-milestone tasks, valid V3 tests; release gates cover every task
of M0–R1; MET gates have evidence and closed tasks; source reuse needs a VERIFIED or RECORDED_V3 license and a pin and
excludes strong copyleft term by term; a COPY/ADAPT capability needs a COPY/ADAPT/KEEP source; capabilities map to tasks, land no later than claimed, have gates in early releases, and never reuse
REJECT or REFERENCE sources; risk severity equals likelihood × impact and HIGH/CRITICAL risks have mitigations;
journeys have gates at their first milestone and all 20 core journeys exist; V3 rows match the V3 catalog (milestone,
phase, dependencies, tier); every Z task has a contract section; every Z-, GATE-, RK- and DEC- ID mentioned in the
markdown exists; generated blocks have exactly one BEGIN/END pair and match the registries.

What it does **not** check: whether acceptance criteria are adequate, whether thresholds are right, whether prose
claims about the outside world are true, or whether anything works at runtime. It is accounting, not proof.

## 2. Mutation suite

```text
$ python -I docs/zain-master-plan/tools/test_zmp_mutations.py
baseline: pass (0 errors)
... 35 cases ...
cases=35 failures=0
```

Each case asserts the **specific** error code, not just a non-zero exit (V3's harness checks exit codes only). The
suite found three real defects in the validator during development, all fixed: the roadmap renderer recursed forever
on a dependency cycle; ordering checks ignored declared dependencies when the edges file disagreed; the renderer
crashed on a malformed CSV row. Independent review (D-R11, D-R16) found two more: the copyleft check missed bare
`GPL-3.0` and LGPL-masked conjunctions, and there was no source-compatibility rule. Both are fixed and covered by
three new cases.

## 3. V3 validator (unchanged input)

```text
$ python -I specs/008-wepld-v3-unified-replan/tools/plan_graph.py --check
tasks=176 tests=383 suites=1 errors=0 coverage={'REGISTERED': 99, 'FREE_TEXT_ONLY': 0, 'GAP': 0}
$ python -I specs/008-wepld-v3-unified-replan/tools/test_plan_graph_mutations.py
cases=26 failures=0
```

Known limitation (reproduced this session): malformed task rows, a missing GENERATED:END marker, a reversed estimate,
a duplicated requirement row and an empty suite all still exit 0 (A3-01). C-28 is not an effective ancestor of X-01
(A3-02 / C-1). Repair is Z-26.

## 4. Environment evidence

| Fact | Command | Result |
|---|---|---|
| Visibility | `gh repo view TheHalfMoon/Zain --json visibility` | PUBLIC |
| Free disk | `df -h /c /d` | C: 3.4 GB free; D: 20 GB free |
| CPU / RAM / GPU | `Get-CimInstance Win32_Processor / Win32_ComputerSystem / Win32_VideoController` | i5-13420H 8C/12T; 15.7 GB; Intel UHD |
| Toolchain | `node --version`, `pnpm --version`, `cargo --version`, `vswhere` | v24.19.0; 9.12.0; 1.97.1; VS Build Tools 2022; SDK 10.0.26100 |
| Local models | `ls ~/.ollama` | 10 KB, no models |
| Main CI | `gh run list -R TheHalfMoon/Zain --branch main` | foundation-integrity 36589753362 success on 0a843a2 |

## 5. What was not validated

- No product build, install or runtime test was performed (local `cargo test` failed to link; see 01 §3).
- No hands-on use of any competitor product.
- No legal opinion on licenses; license facts come from LICENSE files read through the GitHub API.
- No independent non-Claude review of this plan (GATE-REV-01 not met; see 14).
