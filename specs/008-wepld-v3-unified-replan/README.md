# Spec 008 — WePLD V3 Unified Replan (planning package)

```text
STATUS = CANDIDATE / DOCS-ONLY / NO IMPLEMENTATION AUTHORITY
BASE = main @ 0a843a2c0913236d9c93b31abb0d54bbdb023f23
DATE = 2026-10-27
RECOMMENDATION = CONDITIONAL GO — T3-first hybrid + Rust Trusted Core (see 00)
```

This package does not modify canonical governance, the V2.3 master plan, CURRENT_STATE, the source registry archive or
any product code. If accepted, a separate governed change must update `MASTER_PLAN_INDEX.md` to point at V3.

## Read order

1. `00_EXECUTIVE_PRODUCT_DECISION.md` — decision, options, GO conditions
2. `FOUNDER_DECISION_RECORD.md` — the decisions requested from the founder
3. `01_LIVE_WEPLD_AUDIT.md` — live state (main is red; repo private; no runnable agent loop)
4. `07_TARGET_ARCHITECTURE_AND_UX.md` — components, state ownership, Core API, trust boundaries, IA, packaging
5. `05_VERCEL_WORKFLOW_DURABILITY_REA.md` — never-forget contract + sequence diagrams
6. `08_MIGRATION_AND_IMPLEMENTATION_ROADMAP.md` — Phases 0–10 with gates
7. `09_RECOVERY_SECURITY_AND_EVALUATION.md`, `10_COST_RISK_AND_MAINTENANCE.md`
8. `ADR.md` (ADR-001..011), `06_SOURCE_TRANSPLANT_MATRIX.md`, `FEATURE_PARITY_MATRIX.md`, `GAP_LIST.md`
9. Donor syntheses: `02` T3 · `03D` Orca · `03`/`03B`/`03C`/`03E`/`03F` Claude · `04` Amp
10. `11_PLAN_READINESS_REVIEW.md` — adversarial review and dispositions
11. `12_IMPLEMENTER_HANDOFF_PROMPT.md` — only after approval
12. `ASSUMPTIONS_AND_UNKNOWNS.md`, `STATUS_LEDGER.md`, `research/R*.md` (raw cited REA)

## Pins

| Source | Pin | License |
|---|---|---|
| pingdotgg/t3code | 36d4d711b79c73eb33131944f73ea4a8c6156484 | MIT |
| stablyai/orca | e310a63624c86c0e91e9d77df71f038b91d79ea0 | MIT |
| vercel/workflow | af8c6d3295ebc9aa7c0168cd0ca5007f62e6b9ba | Apache-2.0 |
| vercel-labs/durable-harness | ea8aa4060cf4fb8cd39737ce8ab21c4e0f40c741 | Apache-2.0 |
| openai/codex | 603a7baff0f6f37ee9a8a9375a272eaab03d3ece | Apache-2.0 |
| agentclientprotocol/agent-client-protocol | e50f62b4a1ca8d794a4c97210acd8a0d833b05c5 | Apache-2.0 |
| anthropics/sandbox-runtime | 98a4016d27609ed34dd1fb43d23ed6efb6eeeb77 | Apache-2.0 |
| Claude Code CLI / Agent SDK (TS) | 2.1.311 / 0.3.311 (npm, 2026-10-27) | proprietary (Commercial Terms) |
