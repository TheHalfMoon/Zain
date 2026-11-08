# 14 — Independent Reviews

```text
DATE      = 2026-11-08
REVIEWERS = four Google EGM reviewer agents, each in a fresh context with read-only access:
            egm-design (Review A architecture + Review B security), egm-implementation-readiness (Review E execution +
            Review C product completeness), egm-zoom-out (simplicity and scope), egm-codebase-details (Review D sources
            and factual accuracy)
LIMIT     = EGM reviewers run on a Claude model, the same family as the author. They are independent in context, not in
            model family, so they do NOT satisfy GATE-REV-01. OpenCode/DeepSeek and Alibaba OCR were not used: their
            configured routes are a third-party relay and a hosted provider not authorized for private content (DEC-01).
RESULT    = 80 findings: A/B 21 (2 CRITICAL, 8 HIGH, 9 MEDIUM, 2 LOW); E/C 29 (1 CRITICAL, 11 HIGH, 15 MEDIUM, 2 LOW);
            zoom-out 12 (2 Blocker, 8 Major, 2 Nit); D 18 (12 Major, 5 Minor, 1 Nit).
            Dispositions: 72 FIXED, 3 PARTIAL, 3 DECISION (DEC-14, DEC-15), 2 REJECTED with reasons.
            No known plan-blocking issue is left unrecorded.
```

Dispositions: **FIXED** (changed in this package), **PARTIAL** (changed in part; rest recorded), **DECISION**
(turned into a founder decision), **REJECTED** (with reason). Finding IDs are the reviewers' own.

## 1. Review A/B — architecture and security (egm-design, 21 findings)

| ID | Sev | Finding (short) | Disposition |
|---|---|---|---|
| B-01 | CRITICAL | Approval levels reversed relative to V3 17 §4.5 | FIXED: 07 §4 copies V3 (A1 zain-approve + webauthn.dll, A2 isolated window, A3 TOTP); 05 diagram and J10 corrected |
| B-02 | CRITICAL | Gateway not in hosted agents' network path; promise overstated | FIXED: ADR-Z02 scope narrowed; pre-session endpoint/config check; agents' own I/O stays UNMEDIATED (05, 06, Z-11) |
| A-01 | HIGH | R1 write sequence skipped dispatch and bound only a path digest | FIXED: 05 §4 sequence follows V3 07 §3 / 17 §1 |
| A-02 | HIGH | G-07 impossible on private GitHub Free | FIXED: G-07 BLOCKED pending DEC-03 replacement procedure |
| A-03 | HIGH | ADR-Z05 contradicts V3 ADR-011; same-family OCR route | FIXED: ADR-Z05, 06 §3, DEC-01 aligned with ADR-011 |
| A-04 | HIGH | WSL promised but disabled; WSL outside containment | FIXED: Z-33 added; WSL labelled UNKNOWN coverage (07 §3); R0b promises only `wsl.exe` as a shell |
| B-03 | HIGH | R0 supervised mode bypassable; injection claim overstated | FIXED: explicit "no injection control before R1" (07 §2, 02 §3); GATE-SEC-01 per-provider test; OpenCode/Pi disabled or labelled |
| B-04 | HIGH | Same-user secret exposure (DPAPI, CLI files) | FIXED: residual risk in 07 §2; GATE-SEC-02 threshold records exposure |
| B-05 | HIGH | AppContainer listed against V3 ADR-014; admin prerequisites; per-build qualification | FIXED: 07 §3 rewritten |
| B-06 | HIGH | `.cmd` editor launch re-parsed by cmd.exe (BatBadBut class) | FIXED: Z-13 acceptance resolves `.exe` or escapes; negative tests |
| A-05 | MEDIUM | CAP-43 scheduled before its tasks | FIXED: CAP-43 → R2 |
| A-06 | MEDIUM | Re-pin invalidates seam inventory and citations | FIXED: 11 §3 requires seam re-run and citation re-check |
| A-07 | MEDIUM | Update feed hosting and key custody undefined | DECISION: DEC-15 |
| A-08 | MEDIUM | Per-session CODEX_HOME vs "no token copied" | FIXED: Z-10 deliverable; DEC-08 note |
| A-09 | MEDIUM | Vector store contradicts V3 ADR-006 | FIXED: embeddings deferred (Z-28, 06 §4, CAP-07) |
| B-07 | MEDIUM | OneDrive placeholders are reparse points; API name wrong | FIXED: 07 §3 corrected; Z-19 policy |
| B-08 | MEDIUM | Protocol handler / deep links not a trust zone | FIXED: 07 §1 and §2 rows |
| B-09 | MEDIUM | Localhost endpoint spoofing | FIXED: Z-11 endpoint identity; 07 §2 row |
| B-10 | MEDIUM | Caller-set data class | FIXED: Server classifies; raise-only; unknown fails closed (06, 07, Z-11) |
| B-11 | LOW | Kill switch overclaims | FIXED: 07 §4.7 lists escapes |
| A-10 | LOW | Diagram errors (WebSocket client, ledger writer, Claude adapter, grant expiry) | FIXED: 05 §1, 07 §4.6 |

## 2. Review E/C — execution and completeness (egm-implementation-readiness, 29 findings)

| ID | Sev | Finding (short) | Disposition |
|---|---|---|---|
| E-01 | CRITICAL | Reviewer decision deadlock blocks all T2 starts | FIXED: entry accepts DONE_UNREVIEWED; Z-06 always completable via founder review; exits need DONE (11 §2) |
| E-02 | HIGH | Founder review effort excluded | FIXED: RK-25; 10 §3 note |
| E-03 | HIGH | No edge from decisions to Q-00; pin-dependent sources | FIXED: gate edge Z-25→Q-00; re-pin re-derivation in 11 §3 |
| E-04 | HIGH | G-07 in R0 exit with no rewording task | FIXED: as A-02 |
| E-05 | HIGH | R0b journey gates depend on the R0 harness | FIXED: Z-30 R0b harness |
| E-06 | HIGH | No replay provider; GUI automation in second account | FIXED: Z-30 replay provider and scheduled-task procedure |
| E-07 | HIGH | Donor baseline build undefined | FIXED: Z-14 uses the upstream release installer in the isolated account |
| E-08 | HIGH | F-16 requires a paid Claude key | DECISION: DEC-14 (optional Claude session) |
| E-09 | HIGH | F-04 hosting, key custody, no update gate | DECISION: DEC-15; no auto-update in R0b |
| E-10 | MEDIUM | MEASURE tasks without timebox | FIXED: 2 pw timebox (10 §3, 11 §3) |
| E-11 | MEDIUM | RAM threshold unsourced, checked too rarely | FIXED: GATE-RES-01 PROVISIONAL, re-checked before every build-heavy task |
| E-12 | MEDIUM | Isolated account wording vs provider login | FIXED: GATE-ISO-01 and Z-09/Z-10 aligned with A5/A6 |
| E-13 | MEDIUM | Some tasks' only test is their milestone gate | PARTIAL: accepted for founder/documentation tasks (Z-04, Z-18, Z-25, Z-24); their acceptance criteria are evidence-based |
| E-14 | MEDIUM | IDE spike after Monaco is built | FIXED: Z-20 → F-17 gate edge |
| E-15 | MEDIUM | Tokens after a11y pass; unsatisfiable pairing rule | FIXED: Z-17 → F-14 and → Z-15; declared pairings only |
| E-16 | MEDIUM | Undefined V3 amendment procedure | FIXED: 11 §3 |
| E-17 | MEDIUM | Exposure scope misses forks, PR refs, Actions artifacts | FIXED: Z-03 deliverables |
| E-18 | LOW | Z-25 decision range | FIXED |
| C-01 | HIGH | Per-hunk accept/reject unowned | FIXED: Z-31 |
| C-02 | HIGH | Adapter mechanism and data-class source undefined | FIXED: Z-11 deliverables; 06 §2 |
| C-03 | HIGH | No quality gate for RK-06; PERF-07 cannot fail | FIXED: GATE-MODEL-02; PERF-07 can now be NOT_MET |
| C-04 | MEDIUM | R0 failure paths depend on R2 features | FIXED: journeys J11, J13 and Z-21 rewritten for R0 |
| C-05 | MEDIUM | Missing journeys and daily-use gate | FIXED: J21, J22, GATE-USE-01, Z-32 |
| C-06 | MEDIUM | WSL claim without task | FIXED: as A-04 |
| C-07 | MEDIUM | Provisional thresholds can pass themselves | FIXED: 09 §2 final-threshold rule with founder approval; pinned fixture; named model |
| C-08 | MEDIUM | DoD rows without measurement source; no user docs task | FIXED: Z-34; 12 §2 sources |
| C-09 | MEDIUM | Governance blocks the daily driver | FIXED: first release moved to R0b (DEC-07) |
| C-10 | MEDIUM | Script ownership for J01/J03 | FIXED: Z-30 owns J01; GATE-J03 → Z-11 + Z-15 |
| C-11 | LOW | Quarantine and guard values undefined | FIXED: proposed values in Z-27 and Z-19 |

## 3. Zoom-out — simplicity and scope (egm-zoom-out, 12 findings)

| ID | Sev | Finding (short) | Disposition |
|---|---|---|---|
| Z-R01 | Blocker | Governance and plan tooling on the first-release critical path | FIXED for the first release: R0b excludes governance; G-tasks remain in R0 per V3 |
| Z-R02 | Blocker | Local import of public MIT source waits on privacy gates | FIXED: Z-01/Z-02 → Q-01 edges removed; Z-06 kept because V3 A7 requires it before Q-01 |
| Z-R03 | Major | First release too big | FIXED: R0b is the first release (DEC-07) |
| Z-R04 | Major | Z-06..Z-10 repeat V3 A3–A7 | REJECTED in part: they turn V3's prose conditions into owned, evidenced tasks with verified facts (capacity, toolchain); no extra gates beyond GATE-RES-01, GATE-TOOL-01, GATE-ISO-01 |
| Z-R05 | Major | Mirror of V3 plus second validator = two sources of truth | REJECTED with mitigation: V3 stays canonical and the mirror is generated with a drift check; the cross-artifact checks the mission requires have no other home. DEC-11 decides how the tooling reaches main; once G-03 lands, one validator should absorb the other |
| Z-R06 | Major | Cited 15/16/17 missing | FIXED: they were written while the review ran |
| Z-R07 | Major | R0a gated on M0 housekeeping | FIXED: R0a entry is Z-25 (key decisions), Z-06, Z-07, Z-08; M0 runs in parallel |
| Z-R08 | Major | Z-11 too heavy for R0 | PARTIAL: Z-11 stays in R0 (not R0b), so the first release uses official logins only |
| Z-R09 | Major | ADR-001 re-argued three times | FIXED: Z-20 Code-OSS arm reduced to a desk estimate; B-07/B-04 changes left to V3 owners |
| Z-R10 | Major | Carry-over contradictions (G-07, B-01, B-02/B-03 pins) | FIXED/DECISION: G-07 blocked (DEC-03), B-01 amended (Z-24), pins (DEC-04) |
| Z-R11 | Nit | Second donor build for baselines | FIXED: upstream release installer |
| Z-R12 | Nit | Docs restate V3 | PARTIAL: kept, but marked as deltas with V3 references |

Recommendation adopted: a one-day hands-on trial of the upstream T3 release before investing in the fork (Z-29).

## 4. Review D — sources and factual accuracy (egm-codebase-details, 18 findings)

| ID | Sev | Finding (short) | Disposition |
|---|---|---|---|
| D-R01 | Major | Trusted Core ledger/policy marked KEEP but not present | FIXED: CAP-39 REIMPLEMENT; rusqlite and Cedar as INTEGRATE |
| D-R02 | Major | Silent re-pins (PStack, CTK, Monaco, Vercel, durable-harness, E2E) | FIXED: V3 pins restored; current HEADs in notes |
| D-R03 | Major | CAP-25 claimed OCR ADAPT in R1 | FIXED: split into CAP-25 (R1 REIMPLEMENT delegated) and CAP-60 (R3 ADAPT OCR) |
| D-R04 | Major | CAP-42 "AppContainer"; Codex limits omitted | FIXED: not AppContainer; limits added |
| D-R05 | Major | CAP-52 credited Orca for Design Studio | FIXED: REIMPLEMENT + Excalidraw + Style Dictionary; CAP-61 for Orca Design Mode (I-05) |
| D-R06 | Major | Missing MCP SDK, ACP SDK, rusqlite, debugprotocol, Claude SDK rows | FIXED: 7 rows added |
| D-R07 | Major | CAP-05 on monaco-vscode-api conflicts with Monaco | FIXED: CAP-05 → @vscode/debugprotocol; MVSA conditional on Z-20 |
| D-R08 | Major | Orca diff comments are a rewrite, not a port | FIXED |
| D-R09 | Major | Attribution gaps (pr skill, full notices, license elections) | FIXED in SRC-T3, SRC-AIHERO and 04 |
| D-R10 | Major | "VERIFIED" used for V3-recorded licenses | FIXED: RECORDED_V3 state; 04 §5 reworded |
| D-R11 | Major | Copyleft regex missed bare GPL-3.0 and LGPL-masked terms; dead code | FIXED: term-wise check; dead branch removed; 3 new mutation cases |
| D-R12 | Major | Rule 5 implied privacy suffices for builds | FIXED: LOCAL_ONLY wording |
| D-R13 | Minor | "D-04" used a V3 task ID | FIXED (and all decisions renamed DEC-NN earlier for the same reason) |
| D-R14 | Minor | ad3c625 vs 7af08de | FIXED |
| D-R15 | Minor | Wrong citations | FIXED |
| D-R16 | Minor | Playwright/Cedar/Opengrep uncited; no decision-compatibility rule | FIXED: cited; E-CAP-SOURCE-COMPAT rule and mutation |
| D-R17 | Minor | Founder-machine configuration in registry | FIXED: removed from registry; relay host and user paths removed from docs |
| D-R18 | Nit | OCR pin label; Z-P1..P6 vs P7 | FIXED: labelled; discrepancy noted |

## 5. What the reviews could not establish

- Live GitHub facts (visibility, refs, releases, PR states), line counts and machine capacity were not re-verifiable by
  the reviewers (no shell). They rest on this session's command evidence (15 §4).
- No reviewer was outside the Claude model family. GATE-REV-01 remains NOT MET until the founder authorizes a route.
