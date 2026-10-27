# 09 — Recovery, Security and Evaluation

```text
STATUS = UNEXECUTED qualification plan. No benchmark result exists yet; every number below is a TARGET or BUDGET.
"BEST" = falsifiable: WePLD is better than donor X on metric M only when the protocol below shows it with raw data.
```

## 1. Adversarial / security matrix

| # | Threat | Surface | Control (phase) | Test (negative oracle) |
|---|---|---|---|---|
| T1 | Agent performs effect without grant | provider native tools | S1 clamp + S2 hooks (P3); sandbox (P8) | Codex in Supervised requests `rm -rf` outside worktree → denied, receipt `DENY` |
| T2 | Prompt injection from repo/web content asks agent to exfiltrate | provider + browser | network policy deny-by-default for agents (P8 proxy; P3: provider sandbox settings) | Injected README instructs `curl attacker`; egress blocked/approval required; ledger shows proposal |
| T3 | Renderer XSS forges approvals | renderer ↔ Server | approvals need human token minted by desktop main on real UI gesture | Script calls approve RPC → rejected |
| T4 | Outside MCP agent escalates | `/mcp` | Core-scoped grants per outside agent; read-only default | Outside agent attempts write tool → denied |
| T5 | Skill/plugin widens privileges on update | Connections | hash-pinned skills; update requires re-review | Modified SKILL.md → disabled until re-approved |
| T6 | Credential leakage into logs/ledger | all | secret handles only; redaction tombstones; secret scan in CI | Seeded fake key never appears in ledger/T3 DB/logs |
| T7 | Claude subscription token access | provider env | WePLD never reads `~/.claude/.credentials.json`; file-access audit | CC-T04 |
| T8 | Supply chain (donor drift, malicious dep) | build | lockfiles, pinned donors, license/notice gate, `pnpm audit`/`cargo deny`, SBOM | Injected dep with GPL / known CVE fails build |
| T9 | Cross-update to donor binaries | updater | WePLD feed only + signature check + grep gate | Update manifest pointing to T3/Orca rejected |
| T10 | Ledger tampering | Core store | hash chain + `ledger.verify` on start | Byte flip → verify fails, app enters read-only recovery mode |
| T11 | Design preview script reaches Server/Core | Design Studio | sandboxed iframe, separate origin, no preload | Preview JS tries WS to Server → blocked |
| T12 | Computer-use misclick into payments | P9 | hard-blocked categories + per-session grant | Payment page detected → action refused |
| T13 | Stale grant after permission change | Core | revalidation at dispatch | Permission downgraded between approve and dispatch → `STALE_TARGET` |
| T14 | Duplicate external effect after crash | EffectWorker + Core | replay classes + reconciliation | R1/R3/R4 below |

Security review per BUILD_METHOD stays mandatory for T2 changes; d1-local is advisory only and never clears a gate
(per founder's CLAUDE.md).

## 2. Recovery suite (adopted from R05 §7 + WePLD extensions)

Invariants I1–I6 (dense log prefix; one terminal outcome per memo key; NEVER-class effects ≤1 per key unless proven
absent; fenced writes refused; no wedged run; no secrets in logs). Scenarios R1–R11 exactly as R05 §7 (kill sweep,
duplicate webhooks, missing receipts, unknown outcomes, lost credentials, corrupted state, schema upgrades, provider
exhaustion, context overflow, network loss, cancellation). WePLD additions:

| ID | Scenario | Expected |
|---|---|---|
| W1 | Core killed while Server runs | gated effects refused; chat continues read-only; Core restart → open dispatches reconciled |
| W2 | T3 DB power-loss rollback (simulate by restoring pre-commit WAL) | Core receipts without T3 run → `ORPHANED_RECEIPT` visible |
| W3 | Duplicate continuation fire | single T3 command (receipt) |
| W4 | Grant expires while approval pending | explicit expiry event; re-approval required |
| W5 | Ledger schema too new | refuse to open; no partial writes |
| W6 | Git push interrupted | reconcile by remote ref → APPLIED/NOT_APPLIED |
| W7 | Rebase/outdated branch under a mission | mission marks target stale; completion blocked until re-evaluated |
| W8 | Model context overflow mid-mission | continue-as-new into a fresh thread with Brain capsule; pinned-fact recall 100% |

Success metrics: invariant violations 0; crash-point coverage 100% of enumerated points; p95 resume < 10 s local;
NEVER-class duplicates 0; unknown outcomes unresolved after 24 h 0 (escalated counts as resolved-to-human); data loss on
schema upgrade 0; manual recovery steps per 100 crash runs ≤ 2.

## 3. Benchmarks (solo-affordable protocol)

Hardware: founder's Windows 11 laptop (record CPU/RAM/SSD); second run on a $0 GitHub Actions Windows runner for
reproducibility (variance noted). Each benchmark: 10 warm-up + 30 measured runs, report median/p95, raw CSV in repo.

| ID | Metric | Method | Compared against | Budget / target (proposed) |
|---|---|---|---|---|
| B1 | Cold start to interactive | process start → first composer focus (UI marker) | T3 @pin, Orca @pin, Claude Desktop (if installed by founder) | ≤ T3 + 10% |
| B2 | Resident memory idle / 3 sessions / 10 sessions | sum RSS of process tree after 60 s | same | idle ≤ T3 + 15%; 10 sessions ≤ 2.5 GB |
| B3 | UI input latency | keypress → paint (Playwright trace) | same | p95 ≤ 50 ms |
| B4 | Agent first-token latency | send → first streamed token, same model/key | T3 (same adapter) | ≤ T3 + 50 ms (Core overhead) |
| B5 | Reconnect | kill WS; time to resumed stream | T3 | ≤ T3 |
| B6 | Replay/restart correctness | R1 kill sweep | T3 unmodified (expected weaker on UNKNOWN) | invariants 100% |
| B7 | Real task completion | 20 tasks from the founder's repos + 20 from SWE-bench Verified subset, same model, same budget, with/without WePLD Core+Brain | WePLD vs T3 | report completion %, PR correctness by independent reviewer, evidence freshness |
| B8 | Context retention across model switch | 30 pinned facts; switch Claude→Codex→local; query | T3 handoff | recall 100% for pinned facts |
| B9 | Worktree isolation + resume | 5 parallel missions, kill app, resume | Orca, T3 | 0 cross-worktree writes; 5/5 resume |
| B10 | Ledger growth | effects/day × bytes | — | ≤ 50 MB per 10k effects |
| B11 | Permission resistance | 50 injection/escalation prompts (T1–T5) | T3 default (Full access), Amp default (no approvals) | 0 unauthorized effects |
| B12 | Offline usability | network off: open project, edit, terminal, Brain, local model chat | — | all pass |

Cost: $0 infrastructure; model spend for B4/B7/B8 capped by founder (suggest ≤ $50 per full run; local models for B8
partial). Aspirational vs demonstrated: until B1–B12 are run, every comparative claim in marketing or docs is labelled
"target".

## 4. Proof of progress

A phase is "done" only when its DoD tests run in CI (or a recorded local run for hardware-bound benchmarks) and the
evidence is linked from the phase PR; the Core ledger itself records WePLD's own build missions once P4 lands
(dogfooding), so progress claims are queryable, not narrative.
