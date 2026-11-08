# Zain Master Plan

This directory is the master-plan layer on top of the V3 plan (`specs/008-wepld-v3-unified-replan/`). It does not
replace V3. It verifies the current state, adds what V3 lacks, and makes the whole plan machine-checkable. Start with
00, then 16 if you are going to implement.

| Doc | Purpose |
|---|---|
| [00-EXECUTIVE-SUMMARY.md](00-EXECUTIVE-SUMMARY.md) | Verdict and the A–J answers |
| [01-REPOSITORY-AUDIT.md](01-REPOSITORY-AUDIT.md) | Verified state of repo, code, PRs, history, blockers |
| [02-PRODUCT-SCOPE.md](02-PRODUCT-SCOPE.md) | Pillars, releases, first-release scope, gaps Zain can own |
| [03-COMPETITOR-DELTA.md](03-COMPETITOR-DELTA.md) | Competitor changes since 2026-10-27 and capability matrix |
| [04-SOURCE-STRATEGY.md](04-SOURCE-STRATEGY.md) | Donor sources, licenses, copy-first decisions, provenance rules |
| [05-ARCHITECTURE-AND-DECISIONS.md](05-ARCHITECTURE-AND-DECISIONS.md) | Architecture, alternatives, subsystem contracts, sequences, ADR-Z01..Z07 |
| [06-MODELS-CONTEXT-AND-REVIEW.md](06-MODELS-CONTEXT-AND-REVIEW.md) | Model gateway, hardware reality, context engine, review routes |
| [07-SECURITY-AND-CONTAINMENT.md](07-SECURITY-AND-CONTAINMENT.md) | Threat model, Windows containment, privacy, incident lessons |
| [08-UX-JOURNEYS-AND-DESIGN-SYSTEM.md](08-UX-JOURNEYS-AND-DESIGN-SYSTEM.md) | 22 journeys and the Zain design language |
| [09-PERFORMANCE-PLAN.md](09-PERFORMANCE-PLAN.md) | Hardware-bound performance gates |
| [10-ROADMAP-AND-CRITICAL-PATH.md](10-ROADMAP-AND-CRITICAL-PATH.md) | Milestones, generated effort and critical paths, graph |
| [11-TASK-CONTRACTS.md](11-TASK-CONTRACTS.md) | Contract rules; generated contracts for Z-01..Z-34 |
| [12-TEST-QA-AND-DEFINITION-OF-DONE.md](12-TEST-QA-AND-DEFINITION-OF-DONE.md) | Test layers, Definition of Done, release qualification |
| [13-RISKS-AND-OPEN-DECISIONS.md](13-RISKS-AND-OPEN-DECISIONS.md) | Risks and founder decisions DEC-01..DEC-16 |
| [14-INDEPENDENT-REVIEWS.md](14-INDEPENDENT-REVIEWS.md) | Review findings and dispositions |
| [15-VALIDATION-EVIDENCE.md](15-VALIDATION-EVIDENCE.md) | Validator and mutation outputs; what was not validated |
| [16-OPUS-IMPLEMENTATION-HANDOFF.md](16-OPUS-IMPLEMENTATION-HANDOFF.md) | How to execute, resume and stay within authorization |
| [17-MASTER-PLAN-STATUS.md](17-MASTER-PLAN-STATUS.md) | Canonical status and session handoff log |
| [18-EXPOSURE-ASSESSMENT.md](18-EXPOSURE-ASSESSMENT.md) | Z-03 public-exposure assessment of both repositories |
| [work/](work/README.md) | Session scripts and intermediate data, kept for provenance (not maintained tools) |

Registries (`registry/`): task backlog (V3 mirror + Z tasks), dependency edges, acceptance gates, capability
matrix, source registry, risk register, UX journeys.

Tools (`tools/`): `zmp.py check | render | sync-v3` and `test_zmp_mutations.py`. Run with `python -I`.

The prompt's suggested 27-document layout was folded into these 18 documents to avoid duplicating V3 (for example,
the capability matrix, task backlog and dependency graph live in the registries, not in prose copies).
