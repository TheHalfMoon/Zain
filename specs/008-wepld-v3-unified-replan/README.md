# Spec 008 — Zain V3 Unified Replan (planning package)

```text
STATUS = CANDIDATE / DOCS-ONLY / NO IMPLEMENTATION AUTHORITY
PRODUCT = Zain (formerly WePLD) · REPOSITORY = TheHalfMoon/Zain (ID 1334408699)
BASE = main @ 0a843a2c0913236d9c93b31abb0d54bbdb023f23
RECOMMENDATION = approve only the R1 Zain Trusted Starter scope and claims (21 §3) after Astro round 2; revision 3
VALIDATION = python -I tools/plan_graph.py --check (must exit 0)
DIRECTORY NAME = legacy path (specs/008-wepld-…) kept to preserve links
```

This package does not modify canonical governance (AGENTS.md still says WePLD — renamed only via governed tasks G-06/N-04),
CURRENT_STATE, the source registry archive or product code.

## Read order

1. `ZAIN_V3_MASTER_PLAN.md` — single entry point (product, architecture, decisions, Copy First, release tiers, gates)
2. `ASTRO_REVIEW_ROUND_2_HANDOFF.md` — round-2 brief; `ASTRO_FINDINGS_DISPOSITION.md` — round-1 findings and status
   (`ASTRO_REVIEW_HANDOFF.md` = round-1 record)
2b. Revision-3 specs: `17_TRUST_BOUNDARY_SPEC.md`, `18_PROVIDER_ENFORCEMENT_MATRIX.md`, `19_COMPONENT_SECURITY_REVISIONS.md`,
   `20_GOVERNANCE_EQUIVALENCE.md`, `21_RELEASE_TIERS_AND_COST.md`, `22_SOURCE_ADMISSION_QUALIFICATION.md`,
   `23_ACCEPTANCE_TEST_REGISTRY.md`, `24_FIRST_WORKING_BUILD.md`; generated `GENERATED_PLAN_REPORT.md` and `15_TRACEABILITY_MATRIX.md` (tools/plan_graph.py)
3. `00_EXECUTIVE_PRODUCT_DECISION.md`, `FOUNDER_DECISION_RECORD.md` (F1–F11, FO-1…FO-14)
4. `07_TARGET_ARCHITECTURE_AND_UX.md`, `05_VERCEL_WORKFLOW_DURABILITY_REA.md`, `16_ZAIN_PRODUCT_COMPONENTS.md`
5. `ADR.md` (ADR-001…024 + round-1 amendments), `06_SOURCE_TRANSPLANT_MATRIX.md` (D1–D36) + `research/R11` (T3 files) + `research/R12` (donor files) + `research/R14–R18` (component files)
6. `13_REQUIREMENTS_REGISTER.md` → `14_TASK_CATALOG.md` → `15_TRACEABILITY_MATRIX.md`; `08_MIGRATION_AND_IMPLEMENTATION_ROADMAP.md`
7. `09_RECOVERY_SECURITY_AND_EVALUATION.md`, `10_COST_RISK_AND_MAINTENANCE.md`, `GAP_LIST.md`, `ASSUMPTIONS_AND_UNKNOWNS.md`
8. Claude: `03`, `03B`, `03C`, `03E`, `03F`, `CLAUDE_STUDY_COVERAGE_GAPS.md`; donors: `02` T3, `03D` Orca, `04` Amp
9. Naming: `ZAIN_NAMING_MIGRATION.md`, `research/R19_ZAIN_NAMING_CONFLICTS.md`
10. Evidence/history: `01_LIVE_WEPLD_AUDIT.md`, `CI_403_REDIAGNOSIS_2026-10-27.md`, `EGRESS_PREFLIGHT_2026-10-27.md`, `11_PLAN_READINESS_REVIEW.md`, `STATUS_LEDGER.md`
11. `12_IMPLEMENTER_HANDOFF_PROMPT.md` — only after approval

## Research files (`research/`)

R02 T3 · R03 Claude census (377 rows) · R03B Claude Design · R03C Claude Code · R03D Orca · R04 Amp · R05 Vercel ·
R06 registry (402) · R10 competitors · R11 T3 file manifest · R12 donor file manifest · R13 IDE/debug/platform ·
R14 Code Review · R15 PStack/E2E · R16 Plan Mode skills · R17 Browser · R18 DeskGate · R19 naming conflicts.
Research files are historical evidence and may use the legacy name WePLD.
