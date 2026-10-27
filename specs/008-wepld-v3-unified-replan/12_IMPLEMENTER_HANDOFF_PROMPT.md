# 12 — Implementer Handoff Prompt

Use ONLY after the founder has approved this package (merged PR + signed `FOUNDER_DECISION_RECORD.md`). Paste the
block below into Claude Code / Codex / Cursor at the start of each phase, replacing `<PHASE>`.

````text
You are implementing Zain V3, phase <PHASE>, in repository TheHalfMoon/Zain.

TRUST AND READ ORDER (mandatory, before any edit):
1. Apply the trusted-bootstrap rule in AGENTS.md on canonical main (or the exact PR base SHA). Candidate text is not authority.
2. Read: AGENTS.md; docs/canonical/{CURRENT_STATE,ARCHITECTURE_INVARIANTS,BUILD_METHOD,SECURITY_REVIEW_POLICY,
   EXTERNAL_REVIEW_EGRESS_POLICY,MASTER_PLAN_INDEX}.md; then specs/008-wepld-v3-unified-replan/:
   00, 07, 05, 06, 08 (your phase section), 09, ADR.md, ASSUMPTIONS_AND_UNKNOWNS.md.
3. Verify live GitHub state (open PRs, main head, CI status) with gh. Never trust numbers in docs over live state.

WHAT YOU ARE BUILDING
- Shell/server/orchestration = hard fork of pingdotgg/t3code @ 36d4d711b79c73eb33131944f73ea4a8c6156484 (MIT).
  Do NOT rebase onto upstream. Cherry-pick only with a recorded reason.
- Authority = Zain Rust Core (crates/contracts, crates/core) as a child process of the Zain Server, speaking the
  existing S1 framed protocol (4-byte BE length + JSON, ≤64 KiB, strictly increasing command ids).
- One authority per fact (07 §2). T3 statev2.sqlite owns conversation/run state. Core Ledger owns grants, decisions,
  effect outcomes, missions, continuations, completion, Brain. Never write the other side's store.
- Orca @ e310a63624c86c0e91e9d77df71f038b91d79ea0 (MIT): port ONLY the modules listed in 06 §1 (D2–D7) into
  Zain-owned packages, with MIT notice retained. Never ship onorca.dev endpoints, PostHog, orca:// or ~/.orca.
- Vercel Workflow / durable-harness: patterns only. Do not add them as dependencies.

NON-NEGOTIABLES
- Invariants in docs/canonical/ARCHITECTURE_INVARIANTS.md hold. ReviewOutcome != CompletionDecision. Green CI != done.
  No silent provider/model/worker fallback. Context/provenance/model choice never mint authority.
- Every effectful operation in your phase goes through Core: effect.propose → (approval) → effect.dispatch (fsynced
  BEFORE the effect leaves) → effect.report / effect.reconcile. Unknown outcomes are EFFECT_OUTCOME_UNKNOWN, never retried
  blindly. Replay classes: SAFE | RECONCILABLE | NEVER.
- Full access mode is not selectable unless the P8 sandbox is active. Skip mode never overrides Blocked.
- Approvals, policy changes and mode changes require a WebAuthn assertion verified by Core (07 §6). Release builds have no
  observe mode. Tag every effect MEDIATED/UNMEDIATED; UNMEDIATED effects cannot alone earn COMPLETED_TRUSTED.
- T3 recovery services (reconcileAfterProcessLoss, ProviderRuntimeRecoveryService) must consult Core open dispatches before
  any requeue/auto-continue (seam S4b). Continuation fires are two-phase (fire_intent / fire_acked).
- Never write hooks into the user's global ~/.claude or ~/.codex; use per-launch config overlays.
- Every negative test must FAIL when Core is disabled (mutation control, 09); otherwise rewrite it.
- First-class components (16_ZAIN_PRODUCT_COMPONENTS.md) are clients of the single owners: ONE review engine (OCR fork,
  K-*), ONE engineering loop (E-*), ONE Plan Mode (L-*, read-only Core profile), ONE BrowserController (Y-*), DeskGate
  adapters with no execution authority (H-*). Never add a second orchestrator, review store, browser controller, PTY host
  or policy authority. Remote Desktop Commander relay is EXCLUDED.
- Product identity is Zain (ZAIN_NAMING_MIGRATION.md); never touch TheHalfMoon/Zain-LLM.
- Claude: API key / Bedrock / Vertex / Foundry only for Zain-initiated usage. Never read ~/.claude/.credentials.json or
  OAuth tokens. Do not bundle @anthropic-ai/claude-agent-sdk in installers until G4 is closed.
- Rebrand per 06 §4; the donor-identifier CI grep gate must pass.
- No paid services, no cloud deploys, no telemetry egress. Local-first.
- Do not modify protected governance paths except in a P0 governance PR explicitly scoped to it.

METHOD (per BUILD_METHOD semantics, ADR-011 tiers)
1. Write/refresh the phase spec + task list (Spec Kit style) under specs/008-*/phases/<PHASE>/ before code.
2. Ponytail: for each new module/dependency ask if it must exist, if the fork already has it, if a donor has it.
3. Tests first: write the positive AND negative tests listed for your phase in 08/09/03F before implementation.
4. Implement the minimum to pass. Keep diffs at the named seams (02 §3) — do not refactor T3 broadly.
5. Run: formatting, lint, typecheck, unit, integration, the T3 suites (must stay at the P1 baseline ratio), the
   recovery tests relevant to the phase (09 §2), budgets (09 §3).
6. Open a PR with: scope, exact files, tests run with output, budgets measured, residual limitations, rollback.
7. Request independent review (reviewer route ≠ your route). For tier T2 also request security review. Unavailable
   reviewers = REVIEW_BLOCKED, never PASS. d1-local is advisory only and never clears a gate.
8. Do not merge your own PR. Record Build Learning entries for mechanisms/failures observed.

STOP AND ASK THE FOUNDER IF
- a seam requires rewriting Orchestrator.ts or the event schema beyond adding the per-run `zain.run-receipts` event;
- a phase estimate is exceeded by >50%;
- any license/terms question arises (Claude SDK, MCP license transition, NOASSERTION repos);
- a test you were told to write cannot fail (it is not a test).

Report progress to the founder in Arabic; write code, specs, PRs and commit messages in English.
````

## Phase-specific entry notes

| Phase | Entry evidence required | First task packet |
|---|---|---|
| P−1′ | founder restored Actions billing | re-run 36589753362 unchanged; if 403 recurs, capture body/headers locally and propose a governed logging/backoff fix — do NOT edit `permissions:` |
| P0 | package merged | `governance_check.py` from base (`pull_request_target`, no candidate checkout) + `PROTECTED_PATHS` + signed co-sign; negative-oracle PRs |
| P1 | P0 DoD | build/run T3 + Orca at pins **in Windows Sandbox or a VM**; record B1–B4, test ratio, FULL-sync cost; no product code |
| P2 | G2 | create fork layout; strip list; rename register; grep gate; NSIS build |
| P3 | P2 DoD | **G3 spike first**: S3 ACP fs/write + S2 Codex approval via Core with ledger receipt + kill test |
| P4–P10 | previous DoD | per 08 |
