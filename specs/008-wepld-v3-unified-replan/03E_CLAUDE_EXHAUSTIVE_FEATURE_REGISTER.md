# 03E — Claude Exhaustive Feature Register (index, taxonomy and completeness audit)

```text
CANONICAL_REGISTER_FILE = research/R03_CLAUDE_CENSUS.md §1 (377 census rows, unique IDs CL-<family>-NNN, 18 columns)
COMPANION_REGISTERS = research/R03B_CLAUDE_DESIGN.md §3 (Design sub-features), research/R03C_CLAUDE_CODE.md (CLI/SDK)
PARITY_MAPPING = 03F_CLAUDE_FEATURE_PARITY_AND_TEST_MAPPING.md
ACCESS_DATE = 2026-10-27; evidence_date = page "last updated" where published
```

The register is kept in one file to avoid two divergent copies; this document is its index and audit.

## 1. Column contract (as requested) and where each lives

| Requested column | Register column | Notes |
|---|---|---|
| feature_id | feature_id | `CL-A-001`… unique, de-duplicated (one merge: CL-E-070 → CL-F-034) |
| family | family | A chat/research/memory · B creation · C Cowork/agentic · D Claude Code (pointer rows) · E extensibility/enterprise · F distribution/plans/models |
| exact_feature, source_product, platform_surface, user_flow | same | |
| official_evidence_url, evidence_date | same (SC<article-id> = support.claude.com article) | |
| observed_test | observed_test | all `NOT_OBSERVED` (no UI hands-on in this mission); CLI help observed in R03C |
| shipped_status | shipped_status | see R03 §7b for current status totals (377 rows) |
| beta_or_rollout, plan_gate, region_or_OS_gate | plan_gate / region_or_OS_gate (rollout inside status) | ~45 rows carry ≤15-word live quotes (`Q:`) |
| data_storage_and_permissions | same | |
| access_to_source_or_public_API | same | no Anthropic product source anywhere; APIs/SDKs/open formats only |
| donor_candidate_path, Zain_transplant_route | Zain_route (+ 06 matrix for donors) | |
| target_workflow, target_acceptance_test | in 03F | generated + hand-written V1-01..18 |
| effort | 08 phase estimates | per phase, not per row |
| confidence, unknowns | same | |

## 2. Taxonomy completeness audit

| Check | Result |
|---|---|
| All Help Center top-level collections enumerated | 15 collections, 35 subcollections, 364 articles fetched (R03 §7a) |
| Mandatory collections read in full | Features & capabilities 36/36; Cowork 14/14 |
| Articles cited by ≥1 row | 326/364; 38 uncited with reasons (promotions, troubleshooting, superseded notices) |
| Non-Help-Center official pages | product overview, download, pricing, design product page, release notes, Academy, code.claude.com (R03C) |
| Families beyond the brief's taxonomy discovered | Claude Tag (Slack), Claude Duet (agent payments, US research preview), Claude Science, Claude Security, Motion artifacts, "Record a skill", Cyber Verification Program, wellbeing settings, inference hooks |
| Removed/renamed captured | R03 §4 |
| Discrepancies recorded | 19 (8 open) R03 §3 |

## 3. Verdict

`COVERAGE_COMPLETE_FOR_MANDATORY_SCOPE` and `DEPTH_PARTIAL_OUTSIDE_IT` (after the 2026-10-27 depth pass: 214 articles full-text, 91 summary-read, 59 digest-only none of which is any row's best source; API
platform references and changelogs not line-read; no hands-on observation). This is stated rather than rounded up.
Closure tasks: `ASSUMPTIONS_AND_UNKNOWNS.md` U-03-1..U-03-5.

**Study-depth ledger:** exactly which Claude features have not been studied hands-on (all of them) or in full (267 of 377 rows) is enumerated row by row in `CLAUDE_STUDY_COVERAGE_GAPS.md` (2026-10-27).
