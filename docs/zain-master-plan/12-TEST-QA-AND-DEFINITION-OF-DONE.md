# 12 — Test Strategy, Release Qualification and Definition of Done

```text
GATES  = registry/zain-acceptance-gates.csv (58 gates: 5 RELEASE, 22 JOURNEY, 31 category gates)
TESTS  = V3 23_ACCEPTANCE_TEST_REGISTRY.md (383 registered tests) + this plan's gates; task `tests` cells must resolve
         to one of the two (zmp.py E-TEST-UNKNOWN)
RULE   = a test passes on the real installed artifact or it has not passed
```

## 1. Test layers

| Layer | What | Where it runs | Owner tasks |
|---|---|---|---|
| Unit / contract | Rust Core, Server modules, adapters, gateway routing | Local; CI when the repository is private and minutes allow | Every implementing task |
| Integration | Server ↔ Core protocol, provider adapters, ProcessHost, fs-gate | Local Windows | C-02..C-28, Z-11 |
| Negative / mutation-controlled | Each guard's test must fail when the guard is removed | Local | V3 neg tests; Z-11, Z-19, Z-27 |
| Recovery | Crash, kill, power-loss simulation, unknown outcomes | Local, installed build | Z-21, C-20 |
| Journey (E2E) | J01–J20 on the installed NSIS build in the isolated account | Local, Playwright for Electron | Z-15, Z-16, component suites |
| Performance | GATE-PERF-01..05, GATE-PERF-07, GATE-CTX-01 and V3 budgets | Local, reference machine | Z-14, F-15, C-21 |
| Packaging | Install, launch, update, uninstall, artifact provenance | Local, isolated account | Q-04, F-11, Z-22 |
| Privacy / egress | Network capture idle and during journeys; data-class routing | Local | F-05, Q-03, Z-11 |
| Plan integrity | `zmp.py check`, mutation suite, V3 `plan_graph.py --check` | Local | Z-05, Z-26 |

**Regression policy.** A change that fails any previously passing test of its milestone is reverted or fixed before
merge. Flaky tests count as failures until fixed; a journey must pass 3 consecutive runs.

## 2. Definition of Done

**First release (R0b, founder daily driver).** GATE-R0B-EXIT MET on one installer SHA-256: R0a passed; journeys J01,
J04, J06, J18 and J21 pass on the installed build; GATE-PKG-01, GATE-PKG-02, GATE-PRIV-04, GATE-SEC-01, GATE-SEC-02
and GATE-PERF-BASE MET; LIC-01 notices shipped; no open HIGH/CRITICAL finding for R0b in 14 or the risk register;
T2 work reviewed through a GATE-REV-01 route. Claims: none beyond "private build, not policy-enforced".

**Zain 1.0 (R0, qualified).** The table below.

| Dimension | Measurable condition | Gate(s) |
|---|---|---|
| Functional | Journeys J01–J07, J09, J11–J13, J15, J16, J18, J21, J22 pass on the installed build | GATE-J01..GATE-J22 (R0a/R0b/R0 subset) |
| Architectural | Every R0 subsystem row in 05 §3 has at least one passing integration or journey test; V3 P2 exit F-16 passed | GATE-R0-EXIT |
| Reliability | Crash, kill and restart scenarios recover; only in-flight turn lost | GATE-REC-01 |
| Security | Supervised default; keyring-only credentials; no HIGH/CRITICAL finding open for R0 in 14 or `zain-risk-register.csv`; T2 work reviewed per V3 ADR-011 | GATE-SEC-01, GATE-SEC-02, GATE-REV-01 |
| Performance | GATE-PERF-01..05 met with measured thresholds | GATE-PERF-BASE, GATE-PERF-01..05 |
| Usability | Accessibility baseline; design language applied; empty/error states per journey; 10 days of daily use logged | GATE-A11Y-01, GATE-ID-01, GATE-USE-01 |
| Tests | All R0 task tests green with evidence; plan validators green; V3 validator not fail-open | GATE-PLAN-01..03 |
| Packaging | Unsigned NSIS installs, launches and uninstalls cleanly; updating per DEC-15 (no auto-update before the feed decision) | GATE-PKG-01, GATE-PKG-02 |
| Privacy | Repository private; no automatic third-party review; zero donor/telemetry egress; data classes enforced for routes Zain configures | GATE-PRIV-01..04, GATE-MODEL-01, GATE-MODEL-02 |
| Documentation | User, install and troubleshooting guide (Z-34); canonical governance and architecture docs reconciled (G-06) | GATE-R0-EXIT |
| Product identity | No donor or legacy names outside notices on any product surface | GATE-ID-01 |
| Release readiness | All R0 gates MET on one installer SHA-256 | GATE-R0-EXIT |

**Technical readiness does not authorize publishing.** A passed GATE-R0-EXIT means the build may be considered for a
release decision. Publication, distribution beyond named private testers, a website or package registry entry all
need the founder's explicit authorization.

## 3. Release qualification per milestone

| Milestone | Release gate | Additional evidence |
|---|---|---|
| M0 | GATE-M0-EXIT | Decision record signed (Z-25) |
| R0a | GATE-R0A-EXIT | Allowed status set from the V3 packet; reproducible failures recorded as FEASIBILITY_COMPLETE_WITH_FAILURES, never PASS |
| R0b (first release) | GATE-R0B-EXIT | §2 first-release definition; named recipients only |
| R0 | GATE-R0-EXIT | Section 2 above |
| R1 | GATE-R1-EXIT | Claims equal generated templates (CLM-01/02); security review of P3 (C-22) |

## 4. Code signing and SmartScreen

The zero-cost path ships **unsigned** NSIS installers. Windows SmartScreen will warn, and an unsigned build gains no
reputation. Zain must not claim a signed, verified or "trusted publisher" installer. Z-22 documents the posture and
the private SHA-256 list. Signing (F-19: OV/EV certificate with a cloud HSM, or a hosted signing service) is in the
optional paid track and is needed only for public distribution. Free open-source signing programs do not apply,
because Zain is private.
