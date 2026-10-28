# 00 — Executive Product Decision (Zain V3)

> Revision 3 (2026-10-28): Astro round 1 returned DO NOT APPROVE; dispositions in ASTRO_FINDINGS_DISPOSITION.md. The decision now asked is approval of the R1 Zain Trusted Starter scope and claims (21 §3), not the whole scope.

```text
STATUS = CANDIDATE PLANNING PACKAGE — not authority until reviewed and merged under trusted-base governance
DATE = 2026-10-27
RECOMMENDATION = CONDITIONAL GO (conditions in §7)
FOUNDATION = Hard fork of T3 Code @ 36d4d711b79c73eb33131944f73ea4a8c6156484 (MIT)
           + Zain Rust Trusted Core (existing S1/S2 code) as a server-owned sidecar
           + bounded ports of Orca modules @ e310a63624c86c0e91e9d77df71f038b91d79ea0 (MIT)
           + Vercel Workflow / durable-harness as PATTERNS ONLY (no runtime dependency)
REJECTED = Orca-as-foundation; merge-both-apps; keep-Tauri-and-build-UI; Vercel Workflow as engine
NEXT_BUILD_ENTRY = (P−1′ CLOSED: main green on unchanged re-run 2026-10-27) → egress preconditions → planning Draft PR → Astro review → founder merge → P0 → P1
```

## 1. Product definition

**Zain is a local-first desktop agent workbench in which any model or agent can do real engineering and
general knowledge work, and in which a Rust Trusted Core — not the agent, not the UI and not the provider —
decides which *mediated* effects are allowed, records what the enforcing Server observed, and decides what counts as
done.** The forked Server is the enforcement point and part of the trusted computing base; effects that bypass it
(provider-native tools without prompts, CLI agents in terminals) are labelled `UNMEDIATED` and cannot by themselves earn
`COMPLETED_TRUSTED`. The claim widens to all agent effects only after the P8 OS sandbox passes its escape suite.

One project holds chats, coding sessions, research tasks, documents/designs, worktrees, PRs and long-lived
Missions. The user starts locally and can optionally attach a self-hosted always-on runner, or control the desktop
from a browser or phone.

What makes it different from T3, Orca, Claude Desktop, Amp, Cursor and Codex (all verified in `research/`):

| Differentiator | Why no donor has it | Evidence |
|---|---|---|
| **Effect-time authority** (Nawat) with a policy decision on every mediated effect | T3 and Orca relay provider prompts; T3 defaults to Full access; Amp never asks by default | `R02 §4.3`, `R03D §16.1`, `R04` permissions |
| **Unknown-outcome-aware effect receipts** (`EFFECT_OUTCOME_UNKNOWN`, reconciliation, retry-safety) | T3 cancels process-bound effects on crash; Vercel replays at-least-once; no competitor documents exactly-once or crash-safe receipts | `R02 §11 C9`, `R05 §2.14`, `R10 §1` |
| **Never-compacted, hash-chained evidence ledger** separate from conversation state | T3 compacts and deletes events every 6 h; Orca has no single log | `R02 §11 C1–C5`, `R03D §6.4` |
| **Trusted Completion**: "done" requires bound evidence + independent reviewer, never green CI alone | Not present anywhere | `01 §4` |
| **Project Brain that outlives models** (decisions, specs, mission state, evidence index) | Claude has memory/projects but is single-vendor; Amp threads are vendor-hosted | `R03 CL-A-*`, `R04` |
| **Any worker**: Claude, Codex, OpenCode, ACP agents, local models, CLI agents in PTYs | Claude Desktop is Claude-only; Amp routes its own models | `R02 §4.1`, `R03D §6.1` |

## 2. The decision in one paragraph

Fork T3 Code as the shell, server and agent orchestration runtime because it already ships the hardest 80% of the
product (multi-provider sessions, an event-sourced orchestrator with receipts and a transactional outbox, worktrees,
hidden-ref checkpoints, diff/PR review, terminal, in-app browser, Electron packaging/updater, remote clients) under
MIT, and because its server-first design exposes exact seams where Zain's existing Rust core can become the
authority (`R02 §10`, seams S1–S9). Do **not** treat T3's log as the evidence log — it compacts and mutates by design —
instead apply **one authority per fact**: T3 owns conversation/UI state; the Rust Core owns grants, decisions, effect
outcomes, missions, continuations and completion. Port a small set of separable Orca modules (Design Mode guest
scripts, TUI-agent catalog + OSC 7501 status, Windows process-host, Linear, computer use, Monaco/diff comments) into
Zain-owned packages. Use Vercel's World/replay-class/fencing/crash-drill ideas as patterns for the Core ledger, not
as a runtime. Retire the Tauri shell; keep every line of the tested Rust core.

## 3. Options compared (summary; detail in `ADR-001`, `R02 §14`, `R03D §16`)

| Option | What | ESTIMATE to useful MVP (solo, AI-assisted) | Verdict | Decisive reason |
|---|---|---|---|---|
| **A. T3 foundation + Orca modules + Rust Core** | Hard fork T3; port ~6 Orca modules; Core sidecar at seams | effort generated (GENERATED_PLAN_REPORT.md §3) | **CHOSEN** | Best substrate for authority seams; 2.4× smaller than Orca; one state store |
| B. Orca foundation + T3 orchestration | Fork Orca; graft T3 event store | ≥30–60 pw **before** any trust work (not like-for-like with A; add ≈ the same 25–45 pw of trust/Brain work); ≥1 FTE fork upkeep | REJECT | Three existing stores + a fourth; 2.37M LOC; 421 open Windows issues; cloud re-hosting |
| C. One shell + other app as process-isolated sidecar | e.g. T3 shell + `orcad` | 6–10 pw per bridged capability + recurring breakage | BRIDGE ONLY | Two runtimes, two stores, 778-method non-public RPC, doubled RAM |
| D. Own modular platform (keep Tauri, build UI) | Build shell/orchestrator around Rust core, copy patterns | 60–120 pw to donor parity, **excluding** trust work | FALLBACK | Contradicts COPY FIRST; fallback if A's Effect/orchestration seams prove unworkable |
| E. Run T3 unmodified, Core as outside MCP agent | No fork | 6–10 pw | REJECT as end state | Thread-level permission ceiling only — fails Nawat per-effect authority (`R02 §14`) |
| F. "Merge both complete apps" | Both Electron apps | n/a | REJECT | Double Electron, duplicate PTYs, contradictory stores, two permission paths |

Estimates are ESTIMATES from the research agents' source reading, not measured; they overlap and are not additive.

## 4. Single owner per capability (no duplicates)

| Capability | Single owner | Source |
|---|---|---|
| Desktop window, updater, packaging | Zain Shell (forked `apps/desktop`, Electron 44) | T3 |
| Web UI (chat, diff, files, terminal view, browser pane) | Zain Shell (forked `apps/web`) | T3 (+ Orca ports) |
| Thread / run / turn / provider-session state | Zain Server orchestration-v2 SQLite (`statev2.sqlite`) | T3 |
| Effect **execution** queue (leases, retries, FIFO) | Zain Server EffectWorker/EffectOutbox | T3 |
| Effect **authority**, receipts, unknown-outcome, reconciliation | Zain Core Ledger (Rust, fsync, hash chain) | Zain (Spec 006 §19) |
| Missions, continuations (wait-for-CI, schedules, wake-ups) | Zain Core Ledger; fires idempotent commands into the Server | Zain |
| Project Brain (memory notes, preferences, mission summaries, evidence + **index over repo specs/ADRs**) | Zain Core Brain tables (FTS5); canonical specs stay in git | Zain |
| Project identity, evidence generations, read-only git topology | Zain Core (existing S2) | Zain |
| Git writes, worktrees, checkpoints | Zain Server VCS driver, **gated by Core grants** | T3 |
| Provider adapters (Claude, Codex, ACP family, OpenCode, Pi) | Zain Server provider packages | T3 |
| CLI agents in terminals (TUI catalog + status) | Zain Server terminal manager + ported catalog | Orca port |
| PTY hosting | Zain Server terminal (node-pty) — one PTY host | T3 |
| Editor | Monaco surface in Zain Shell | Orca port / monaco-editor |
| Browser control (all lanes) | Zain Server BrowserController via CDP relay to Electron panes (ADR-018) | T3 + Playwright |
| Design Studio canvas + design system tokens | Zain Shell + Server design package; tokens in project files (DTCG) | New (R03B) |
| Process sandbox | Zain Core launcher (Codex `windows-sandbox-rs` / `linux-sandbox` ports) | openai/codex (Apache-2.0) |
| Permission policy (PDP) | Zain Core Nawat (Cedar candidate); approvals verified by WebAuthn assertion | Zain |
| Policy enforcement (PEP) | Zain Server at seams S1–S8 (part of the TCB) | T3 fork |
| Remote/mobile clients | Zain Server WebSocket RPC (T3 protocol v2) | T3 |

## 5. What survives from V2.3, what changes

**Kept (semantics):** all `ARCHITECTURE_INVARIANTS.md` authority/evidence/Project-Brain/reuse lines; the "Workers" line
naming Mirefa and Edara needs a governed text amendment because those components are simplified/deferred (the rules
they express — qualification before use, minimum-sufficient topology, Nawat authorizes effects — are kept); Spec 006 §19
effect model; Trusted Completion
rules (§20); independent review; no silent provider/model fallback; local-authoritative/cloud-independent; S1 protocol;
S2 identity/evidence/git observer code and its adversarial tests.

**Changed:**
- The product shell is acquired (T3 fork), not built. Tauri shell retired (`ADR-002`).
- Mission Runtime and Work **merge** into T3 orchestration (execution/conversation) + Core Ledger (authority/mission).
- UWC is replaced by T3 provider adapters + a thin capability descriptor; Mirefa simplified; Edara, Byan, Maemar graph deferred.
- Roadmap S1–S10 is replaced by Phases 0–10 (`08_*`), each with exact entry/exit gates. S1/S2 remain accepted history.
- Governance mechanism (policy successor chain v1–v72, 83.6k lines) replaced by one stable checker + protected-path
  manifest + risk-tiered gates (`ADR-011`). Security semantics retained.

## 6. Claude-feature stance (summary of `03*`)

Zain recreates the *capabilities* of Claude Chat/Cowork/Code/Design/Artifacts — not Anthropic's brand, chrome or trade
dress — and stays multi-vendor. Of 377 census rows (incl. Platform/API family G): 124 ADAPT, 80 USE VIA OFFICIAL INTEGRATION, 35 REIMPLEMENT,
6 COPY, 127 DEFER, 5 REJECT (`03E`). A binding constraint discovered in official docs: **third-party products may not
route requests through users' Free/Pro/Max Claude credentials**; Zain must use API keys/cloud providers, or launch the
user's own unmodified Claude Code binary (the latter's status as "ordinary use" inside Zain is UNKNOWN and must be
confirmed in writing before marketing it) (`R03C §auth`, census `CL-E-096`).

## 7. GO conditions (CONDITIONAL GO)

| # | Condition | Why | Evidence that discharges it |
|---|---|---|---|
| G1 | **MET for CI (2026-10-27):** `main` integrity green on unchanged re-run (attempt 3) after the repo became public; remaining: governance simplified per `ADR-011` (P0) | Nothing can be accepted while the gate is broken | Green `foundation-integrity` (or its successor) on `main` |
| G2 | Phase 1 measurement: T3 @ pin builds, tests and runs on the founder's Windows machine; baseline RAM/start/latency recorded | Estimates are from reading, not running | `09_*` B1–B3 numbers committed |
| G3 | Effect seam spike: Core grants a Codex approval and an ACP `fs/write` through S2/S3 with a ledger receipt, and a kill -9 between dispatch and receipt yields `EFFECT_OUTCOME_UNKNOWN` | Proves the trust claim is implementable on the fork | Spike test log + receipts |
| G4 | Claude SDK redistribution + auth posture confirmed | Proprietary SDK in a redistributed product; subscription-auth policy | Written Anthropic answer, **or** fallback adopted: SDK excluded from installer and loaded from a user-consented location + API-key/cloud credentials only. The "user-installed CLI in a Zain terminal" route stays UNKNOWN and is not a G4 discharge. |
| G5 | Founder accepts the governance change and the T3 fork-not-track policy | Both reverse earlier canonical choices | Founder decision record (`FOUNDER_DECISION_RECORD.md`) signed off in PR |

**v1 scope line:** release R2 (numbers generated: GENERATED_PLAN_REPORT.md §3; first trusted release R1, 21). Design Studio (P7),
containment (P8), general agent work (P9) and runner/mobile (P10) are post-v1. Useful earlier stops: P2 exit (branded
multi-agent workbench) and P3 exit (authority differentiator).

If G2 or G3 fails: fall back to Option D for the failing layer only (e.g. keep T3 UI, replace its effect worker),
re-estimate, and re-review.

## 8. What is verified vs proposed

- **Verified (read at pinned SHAs / official pages, 2026-10-27):** donor structures, licenses, seams, storage
  semantics, open issues, Claude feature statuses (377 census rows), Amp feature set, Vercel internals, registry liveness.
- **Not verified:** any runtime behavior of T3/Orca on this machine (nothing was built or run — by mandate); all effort
  estimates; all performance claims; Claude SDK redistribution terms.
- **Proposed:** everything in `07_*`, `08_*`, ADRs.

## 9. Package map

`01` audit · `02` T3 · `03` Claude complete · `03B` Design · `03C` Claude Code · `03D` Orca · `03E` register ·
`03F` parity/tests · `04` Amp · `05` durability · `06` transplant matrix · `07` architecture/UX · `08` roadmap ·
`09` recovery/security/eval · `10` cost/risk · `11` readiness review · `12` implementer prompt ·
`ADR.md` · `FEATURE_PARITY_MATRIX.md` · `FOUNDER_DECISION_RECORD.md` · `ASSUMPTIONS_AND_UNKNOWNS.md` ·
`GAP_LIST.md` · `STATUS_LEDGER.md` · `research/R*.md` (raw REA, cited).
