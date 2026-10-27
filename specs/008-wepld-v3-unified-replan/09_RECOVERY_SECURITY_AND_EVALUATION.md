# 09 — Recovery, Security and Evaluation

```text
STATUS = UNEXECUTED qualification plan (revision 2 after adversarial review M1/M2/H7/H8/C1).
No benchmark result exists yet; every number is a TARGET or BUDGET until measured.
"BEST" = falsifiable: Zain beats donor X on metric M only when this protocol shows it with raw data.
MUTATION_CONTROL = every negative (security/authority) test is run twice: with its guard active (must pass) and with that
                   guard removed or bypassed (must FAIL); for Core-enforced guards the guard is Core. A negative test that passes in both runs is not a Zain test and is
                   rewritten or dropped.
```

## 1. Adversarial / security matrix

| # | Threat | Control (phase) | Negative oracle (subject to mutation control) |
|---|---|---|---|
| T1 | Agent effect without grant | S1–S8 (P3), sandbox (P8) | ACP agent requests `fs/write` outside worktree → denied by Core. (Do **not** use a Codex `rm -rf` outside workspace as the oracle: Codex's own sandbox denies it even with Core off.) |
| T2 | Prompt injection → exfiltration | provider network settings + ACP terminal policy (P3); egress proxy (P8) | Injected README asks agent to `curl` an external host via ACP terminal → `APPROVAL_REQUIRED`/deny |
| T3 | Forged approval (XSS renderer, compromised Server) | WebAuthn assertion verified by Core (P3) | Approve RPC without valid assertion → rejected; replayed assertion for a different proposal → rejected |
| T4 | Outside MCP agent escalates | Core-scoped grants per outside agent | write tool from outside agent → denied |
| T5 | Skill/plugin privilege widening on update | hash-pinned skills; re-review | modified SKILL.md disabled until re-approved |
| T6 | Credential leakage | secret handles; tombstones; CI secret scan | seeded fake key never in ledger/T3 DB/logs |
| T7 | Claude subscription token access | no reads of `~/.claude/.credentials.json` | file-access audit (CC-T04) |
| T8 | Supply chain | lockfiles, pins, license/notice gate, `pnpm audit`, `cargo deny`, SBOM, installer-content gate | injected GPL/CVE dep fails; `claude-agent-sdk*` in installer fails (until G4) |
| T9 | Cross-update to donor binaries | own feed + signature + grep gate | manifest pointing to T3/Orca rejected |
| T10 | Ledger corruption | hash chain + verify on start | byte flip → verify fails → read-only recovery mode |
| T10b | **Ledger tampering by an unsandboxed agent** (same user) | data-root deny floor (P3); WebAuthn-signed approvals; out-of-machine anchor (`ledger.anchor`); P8 sandbox | agent rewrites file + recomputes chain → floor denies the write (mediated agents); for unmediated agents the next anchor comparison detects divergence (documented limitation before P8) |
| T11 | Design preview script reaches Server/Core | separate-origin sandboxed iframe, no preload | preview JS WS to Server → blocked |
| T12 | Computer-use into payments | hard-blocked categories + per-session grant (P9) | payment page → refused |
| T13 | Stale grant after permission change | revalidation at dispatch | downgrade between approve and dispatch → `STALE_TARGET` |
| T14 | Duplicate external effect after crash | replay classes + reconciliation + S4b | R1/R3/R4, W9 |
| T15 | **Enforcement downgrade** (`observe` via env/profile) | observe compiled out of release; signed `core.mode` | agent `setx ZAIN_CORE_ENFORCE observe` → no effect after restart (release build) |
| T16 | Second Server/Core on same data root | exclusive data-root lock + fencing epoch | second instance gets no authority; stale-epoch frames rejected |
| T17 | CLI-agent hook spoofing | per-PTY secret on loopback hook endpoint; per-launch config overlays | unauthenticated local POST to hook endpoint → ignored; user's global `~/.claude` unchanged after a Zain session |

Security review per BUILD_METHOD stays mandatory for T2; d1-local is advisory only and never clears a gate.

## 2. Recovery suite

Invariants I1–I6 and scenarios R1–R11 exactly as `research/R05_VERCEL.md` §7. Zain additions:

| ID | Scenario | Expected |
|---|---|---|
| W1 | Core killed while Server runs | gated effects refused; restart → epoch bump → open dispatches reconciled (05 §7.2) |
| W2 | T3 power-loss rollback of a run | Core receipts → `ORPHANED_RECEIPT` visible |
| W2b | T3 rollback of a continuation **receipt** | un-acked fire reconciled via receipt query; command executes once |
| W3 | Duplicate continuation fire | single T3 command |
| W4 | Grant expires while approval pending | explicit expiry event; re-approval needs a new assertion |
| W5 | Ledger schema too new | refuse to open |
| W6 | Git push interrupted | reconcile by remote ref |
| W7 | Rebase / outdated branch under a mission | target stale; completion blocked until re-evaluated |
| W8 | Context overflow mid-mission | continue-as-new with capsule; recall measured on non-pinned decisions (B8) |
| W9 | T3 recovery vs Core reconcile race | T3 cannot requeue/auto-continue a `NEVER`/`RECONCILABLE` effect before Core answers |

Metrics: invariant violations 0; crash-point coverage 100% of enumerated points; p95 resume < 10 s local; NEVER-class
duplicates 0. **Unknown outcomes are reported as two separate numbers:** auto-reconciled within 24 h (target ≥ 90% for
RECONCILABLE effects with an observable postcondition) and escalated-to-human (target: 100% of the rest reach the Inbox
within 1 min); escalation is not counted as resolution. Data loss on schema upgrade 0; manual recovery steps per 100 crash
runs ≤ 2.

## 3. Benchmarks (solo-affordable protocol)

Hardware: founder's Windows 11 laptop (record specs) for timing; a Windows VM for donor isolation. CI runners are used
only for functional suites: on a **private** repo GitHub Actions minutes are limited and Windows minutes count at a
multiplier (verify current plan numbers before relying on them); timing benchmarks are not run in CI.

| ID | Metric | Runs | Baseline | Budget / target (proposed) |
|---|---|---|---|---|
| B1 | Cold start → composer focus | 5 warm-up + 20 | T3 @pin (P1) | ≤ T3 + 10% |
| B2 | RSS of process tree: idle / 3 / 10 sessions | 5 each | T3, Orca (P1) | idle ≤ T3 + 15%; 10 sessions ≤ 2.5 GB |
| B3 | Input latency keypress→paint (Playwright trace) | 200 events | T3 | p95 ≤ 50 ms |
| B4 | First-token latency, same model/key | 20 | T3 same adapter | ≤ T3 + 50 ms |
| B5 | WS reconnect to resumed stream | 20 | T3 | ≤ T3 |
| B6 | Restart correctness (R1 sweep) | 100 runs | T3 unmodified | invariants 100% |
| B7 | Real task completion: 15 founder-repo tasks + 15 SWE-bench Verified subset, same model/budget, **3 runs per task per arm** | 180 agent runs | T3 (Supervised) vs Zain | hypothesis H-B7: Zain completion rate ≥ T3 − 5 pts **and** unauthorized-effect count lower; PR correctness by independent reviewer; cost logged |
| B8 | Retention across model switch | 30 **non-pinned** decisions captured during work; switch Claude→Codex→local; quiz | T3 context handoff | Zain recall ≥ T3 + 30 pts (hypothesis) |
| B9 | Worktree isolation + resume | 5 parallel missions, kill app, 5 repeats | Orca, T3 | 0 cross-worktree writes; 5/5 resume |
| B10 | Ledger growth | synthetic 10k effects | — | ≤ 50 MB / 10k effects |
| B11 | Permission resistance (50 injection/escalation prompts T1–T5) | 1 run each | **T3 in Supervised mode** (not Full access) | 0 unauthorized **mediated** effects; unmediated ones counted and reported |
| B12 | Offline usability (network off) | checklist | — | all pass |
| B13 | Per-effect overhead | 1,000 mediated effects | no-Core build | p95 added latency ≤ 25 ms |

Cost: $0 infrastructure. Model spend: B4/B5 negligible; B7 ≈ 180 runs — cap the run budget explicitly (e.g. per-task token
limit; estimate before running; local models for a smoke variant); B8 can use one cloud + one local model. Until run,
every comparative statement is labelled "target".

## 4. Proof of progress

A phase is done only when its DoD tests run (CI or recorded local run for hardware-bound benchmarks) with mutation
controls, and evidence is linked from the phase PR. From P4 Zain records its own build missions in its ledger
(dogfooding), so progress is queryable rather than narrated.
