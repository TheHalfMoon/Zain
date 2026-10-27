# 01 — Live WePLD Audit (2026-10-27)

```text
STATUS = CANDIDATE PLANNING EVIDENCE (untrusted until reviewed + merged)
OBSERVED_AT = 2026-10-27 (Asia/Riyadh session; GitHub API + fresh clone)
CANONICAL_REPO = TheHalfMoon/wepld
MAIN_HEAD = 0a843a2c0913236d9c93b31abb0d54bbdb023f23 (2026-09-29T18:22:52+03:00, merge of PR #345)
METHOD = gh api / gh pr / gh run + git clone of main + direct file reads
CLAIM_CLASS = every row tagged VERIFIED (observed here), RECORDED (repo text, not re-verified), or INFERRED
```

Read order applied: `AGENTS.md` → `CURRENT_STATE.md` → `ARCHITECTURE_INVARIANTS.md` → `BUILD_METHOD.md` →
`MASTER_PLAN_INDEX.md` → `MASTER_PLAN_V2_3_AGENT_CONTROL_PLANE.md` → `SOURCE_REGISTRY_INDEX.md` → Spec 006
Astro master package → Spec 007 (S3). All read from canonical `main` at the SHA above (trusted base).

---

## 1. Headline findings

| # | Finding | Class | Evidence |
|---|---|---|---|
| H1 | **`main` is red.** The last `foundation-integrity` run on `main` (run `36589753362`, 2026-09-29) **failed**: the v72 policy's `verify-local --remote-baseline` call to `GET /repos/TheHalfMoon/wepld/compare/666e62d…...0a843a2…` returned **HTTP 403**. The previous two runs (2026-09-21) passed. **Re-diagnosed 2026-10-27** (`CI_403_REDIAGNOSIS_2026-10-27.md`): permissions were already `contents: read` and the same token succeeded on `contents/` immediately before; the 403 cluster (15:14–15:22) is most probably transient REST throttling during a burst of runs (PROBABLE, not proven). A re-run on 2026-10-27 could not start: **Actions jobs are blocked by billing/spending limit**. | VERIFIED (failure, permissions, billing block); PROBABLE (throttling) | `gh run view 36589753362`; check-run 122348322500 annotation |
| H2 | **The repository is now PRIVATE.** `CURRENT_STATE.md` (2026-09-12) and Astro evidence (2026-09-20) record `VISIBILITY = public`. ~~The workflow declares `permissions: {}` … H1 is very likely caused by the visibility change.~~ **Withdrawn 2026-10-27:** the workflows declare `permissions: contents: read`; visibility did not cause H1. Branch-protection reads return **HTTP 403 "Upgrade to GitHub Pro or make this repository public"** (plan-gated on private repos). | VERIFIED (visibility, protection 403); causality claim WITHDRAWN | `gh repo view`; `gh api …/branches/main/protection` |
| H3 | **No agent can run in WePLD today.** The Astro plan itself states the first complete loop (open project → Doctor → specify → authorize → review → repair → accept) "does not yet implement". The product is a Tauri window that shows Core readiness/health/version and a Rust CLI `wepld open|doctor|status`. | VERIFIED | `WEPLD_CANONICAL_MASTER_BUILD_PLAN.md:94`; `apps/desktop/ui/app.js` (54 lines); `crates/core/src/bin/wepld.rs` |
| H4 | **Governance code outweighs product code ~4:1.** `.github/scripts/` holds **169 Python integrity scripts, ~83.6k lines** (policy successors v1…v72). Product Rust incl. tests: **~19.1k lines** (≈10k src + ≈9k tests) + 3 UI files. | VERIFIED | `wc -l` on main |
| H5 | **Throughput is consumed by gate mechanics.** 347 PRs in ~7 weeks (2026-08-14 → 2026-10-01); 135 closed unmerged. A large share of merged PRs are single-use "policy successor" reopenings to edit one test file (e.g. #320/#321/#322 for one S2-S001 fixture; #323/#324/#325 for one case-identity fixture). | VERIFIED (counts/titles) | `gh pr list --state merged/closed` |
| H6 | **Source registry has never admitted a source.** 402 entries; **0 admitted**; 373 `BASELINE_ACCOUNTED_PENDING_PATH_MINING`; 20 `BOUNDED_ENRICHED`; 9 `PATH_MINED_PASS1`. "Acquire before generate" has, in practice, produced zero acquired runtime code (the only vendored code is a patched `glib-0.18.5` for Tauri/Linux). | VERIFIED | registry CSV in canonical archive `35dee10e…` |
| H7 | **T3 Code is absent** from the registry and all specs. **Orca** appears only in Astro `SOURCE_INVENTORY.md` at `b5b727bd…` with README/manifest-level hashes and 6 doc paths (no code-level REA). **Vercel Workflow / durable-harness** absent. | VERIFIED | grep over `docs/`, `specs/` |
| H8 | **Cubic still auto-posts** despite `CUBIC_REVIEWS_ENABLED=false`: PR #347 body carries a Cubic auto-generated description — same provider-effective-state conflict already recorded for #3/#4. | VERIFIED | `gh pr view 347` |
| H9 | **High-value design exists but is not implemented**: the Spec 006 effect model (`EffectProposal → NawatDecision → EffectResult → EffectReconciliation`, outcome classes incl. `EFFECT_OUTCOME_UNKNOWN`, `retry_safety_state`, `logical_operation_id` vs `execution_identity`, dispatch-record-before-release) is a genuinely strong, vendor-neutral safe-effect contract. It should survive any re-architecture. | VERIFIED (text) | `specs/006-*/data-model.md` §19–21 |

---

## 2. Repository state (VERIFIED 2026-10-27)

| Item | Value |
|---|---|
| Visibility | PRIVATE (recorded as public until at least 2026-09-20) |
| Default branch | `main` @ `0a843a2` |
| Last push | 2026-10-01T09:09:30Z |
| Remote branches | 351 |
| PRs total | 347 (latest #347); 135 closed-unmerged |
| Open ordinary issues | 11 |
| Branch protection / rulesets | Not readable (403, plan-gated on private repos). Previously 404 "not protected". Merge guard has been `--match-head-commit` only. |
| Tags / releases | 0 / 0 (RECORDED 2026-09-20) |
| `main` CI | **FAILURE** (H1) |

### Open PRs

| PR | Title | Draft | Last update | Disposition proposed |
|---|---|---|---|---|
| #347 | chore: wire Graft as non-authoritative agent context | no | 2026-10-01 | Hold. Touches `AGENTS.md` (base-controlled path) → will be rejected by trusted-base admission by design; needs a governance decision, and V3 changes the bootstrap anyway. |
| #346 | docs: firstmate assurance & decision source expansion plan | no | 2026-09-30 | Fold into V3 source matrix as candidate input; do not merge separately. |
| #343 | feat(contracts): S3-AUTH-C pure contracts C001–C013 (+1,791 lines) | yes | 2026-09-21 | **Salvage as reference** (process/runner descriptors). Under V3 the process host is donor-owned (see 00/07); do not merge as-is. |
| #342 | docs(astro): ASTRO-B01 benchmark preregistration | yes | 2026-09-21 | Salvage benchmark protocol ideas into `09_*`. |
| #164, #162, #159, #136 | Pictorial/Agile vendor import chain (Aug) | yes | 2026-08-24 | Close as superseded (Pictorial/Agile are not in V3's critical path). |
| #88, #81, #73 | MiniMax / JetBrains browser visual-edit research (Aug) | yes | 2026-08-22 | Mine #73 for Design Studio inputs; close the rest. |
| #1 | Fresh foundation (Aug 14) | yes | 2026-08-14 | Close (superseded by merged P0 #2). |

---

## 3. Implementation inventory — what actually exists

### 3.1 Existing and verified implementation (on `main`)

| Area | Paths | What it does | Evidence quality |
|---|---|---|---|
| S1 Desktop ↔ Core handshake | `apps/desktop/src-tauri/src/{main.rs,lib.rs,core_client.rs}`, `crates/contracts/src/{frame.rs,protocol.rs}` | Tauri 2 host spawns Rust Core as child; 4-byte BE length + JSON frames over stdin/stdout; monotonic command IDs, replay rejection, health watch, cancellation | Strong: `crates/contracts/tests/protocol_v1.rs`, `crates/core/tests/s1_011_adversarial_v1.rs`, `apps/desktop/src-tauri/src/s1_011_tests.rs` |
| S2 Project identity | `crates/core/src/identity.rs`, `crates/contracts/src/project.rs` | Resolved-path identity digest, conservative reassociation, durable first-open reservation, crash recovery | Strong: `identity_store_v1.rs` (3,193 lines of tests) |
| S2 Local evidence store | `crates/core/src/evidence_store.rs` (1,729 lines) | Immutable generations, atomic `CURRENT` pointer swap, bounded reads, lock ordering, redaction, freshness | Strong; authenticity explicitly `UnauthenticatedStructuralCoherenceOnly` |
| S2 Git topology (read-only) | `crates/core/src/git_topology.rs` (1,385 lines) | Qualified system-git adapter: absolute exe, env scrub, no hooks/network/pager, closed argv allowlist (`rev-parse`, `worktree list --porcelain -z`) | Strong: `git_topology_v1.rs` |
| S2 Doctor + CLI | `crates/core/src/{doctor.rs,cli.rs}`, `crates/core/src/bin/wepld.rs` | `wepld open|doctor|status` with redacted outcome & frozen exit classes | Good: `doctor_v1.rs`, `cli_v1.rs` |
| Desktop UI | `apps/desktop/ui/{index.html,app.js,style.css}` | Status labels + one observation button | Demo-level |
| Governance automation | `.github/scripts/*.py` (169), 4 workflows | Trusted-base path/byte admission, policy successor chain v1–v72 | Functional until 2026-09-21; **broken on main since 2026-09-29 (H1)** |

### 3.2 Existing architecture/design, not implemented

Work, Mission Runtime, AGILLE, Mirefa, Edara, Nawat, Fehrest/Maemar, AMAN, UWC, Assurance, Trusted Completion, Byan,
Quality Passport, Recovery Time Machine, Terminal Fabric (S3), effect model (Spec 006 §19), ContextPackage, Case/Assignment/Attempt,
Astro 63-task DAG (ASTRO-A01…P06), data-agent hardening addendum, local-intelligence amendment.

### 3.3 Planned but unqualified

S3 host/observe/spawn; S3-D assurance seed; S4-G semantic graph; S5–S10; Teams/Hub/enterprise profiles; containment (AppContainer/Job Objects); Cedar policy engine; ACP/MCP adapters.

### 3.4 Blocked / obsolete / duplicated

| Item | State | Why |
|---|---|---|
| Main CI | BLOCKED | H1/H2 |
| Pictorial/Agile import chain (#136…#164) | OBSOLETE for V3 | No critical-path dependency |
| Duplicate plan file `MASTER_PLAN_V2_3_AGENT_CONTROL_PLANE_CANDIDATE.md` | DUPLICATED (differs from canonical) | Candidate retained beside canonical |
| Policy successor chain (v1…v72) as the unit of change | Process debt | Each test-file edit requires a policy PR + content PR + reconcile PR |
| CURRENT_STATE "communication = Arabic" vs Astro "English-only user direction overrides" | CONTRADICTION in repo text | Founder's live instruction for this mission: Arabic discussion, English artifacts — matches AGENTS.md |

---

## 4. Contract audit — essential differentiator vs simplify/merge/defer

Disposition is a **proposal** consumed by `07_TARGET_ARCHITECTURE_AND_UX.md` and `ADR-*`; it preserves security/evidence
semantics while removing duplicate owners.

| Contract | V2.3 role | Implemented? | V3 disposition | Reason |
|---|---|---|---|---|
| **Nawat** (effect-time authority) | grants/revalidation | No | **KEEP — core differentiator**, implemented as the Rust Trusted Core policy decision point behind the donor's approval hooks | Unique vs T3/Orca/Claude/Amp, which all treat approval as UI prompt or mode |
| **Effect model** (Spec 006 §19) | effect proposal/decision/result/reconciliation | No | **KEEP verbatim semantics**; becomes the receipt schema for the single event log | Best-in-class unknown-outcome handling |
| **Trusted Completion** | completion decision | No | **KEEP**, simplified to a decision record over evidence refs (no separate store) | Differentiator: "green CI ≠ done" |
| **Assurance** (independent eval) | reviewer independence | No | **KEEP**, as "reviewer worker must differ from builder worker" rule + evidence binding | Differentiator |
| **Fehrest** (Project Brain) | durable context | No | **KEEP, narrowed**: project memory + decisions + spec + evidence index; graph (Maemar) **DEFER** | "Never forget" semantic memory |
| **Mission Runtime** | execution truth | No | **MERGE into donor orchestrator** (T3 orchestration event log) — Mission = long-lived projection over threads/turns, not a second runtime | Avoid second authoritative log |
| **Work** | durable coordination | No | **MERGE** into Projects/Missions UI + same event log | Duplicate of Mission Runtime projection |
| **UWC** | worker edge | No | **REPLACE with donor provider adapters** (T3 provider packages / ACP) behind a thin WePLD capability descriptor | Don't rebuild adapters that already work |
| **Mirefa** | route qualification | No | **SIMPLIFY** to a capability/route table + explicit no-silent-fallback rule | Overbuilt for v1 |
| **Edara** | staffing/topology | No | **DEFER** (v1: user-chosen worker + one reviewer) | No evidence of need yet |
| **AGILLE** | spec/plan rigor | No | **SIMPLIFY** to Plan mode + spec artifact templates (Spec Kit compatible) | Behavior, not infrastructure |
| **AMAN** | security evidence | No | **SIMPLIFY** to security-review producer adapter + findings schema; graph DEFER | |
| **Byan** | learning | No | **DEFER** | Needs outcome corpus |
| **S1 protocol** (framed stdio) | Desktop↔Core | **Yes** | **KEEP as the Core sidecar protocol** (child process, framed JSON) — reused under the new shell | Already adversarially tested |
| **S2 identity/evidence store** | project identity | **Yes** | **KEEP**; becomes Core's evidence/identity store | Already tested |
| **S2 git topology adapter** | read-only git | **Yes** | **KEEP** as Core's qualified git *observer*; git *writes* come from the donor's worktree module under Nawat grants | |
| **Tauri desktop host** | S1 shell | **Yes (demo)** | **RETIRE as primary shell** (see ADR-002); Core binary remains | Shell value is ~1k lines; donor shells are years ahead |

---

## 5. Process audit (challenge requested by founder)

1. **Gate mechanics are now the product.** 83.6k lines of single-use Python successors vs ~10k lines of product source. The
   successor-per-edit model guarantees ≥3 PRs per test fix. This is the dominant cause of zero user-visible capability after ten weeks.
2. **The security semantics are worth keeping; the mechanism is not.** What must survive: trusted-base review, exact-head binding,
   independent review, no candidate self-authorization, protected governance paths. These can be enforced with (a) a CODEOWNERS-style
   protected-path list checked by one stable script, (b) required checks (needs public repo or GitHub Pro/Team), (c) exact-head merge guard.
3. **The gate has been silently unavailable since 2026-09-29.** First a transient 403 burst (probable API throttling; the
   script discards status headers, so nobody could tell), and now Actions jobs that do not start at all (billing). Neither is
   recorded in a ledger. This is the "DECLARED_CONSTANT != ENFORCED_BOUNDARY" failure the governance was built to catch.
   (An earlier draft blamed the private switch; that was wrong — see `CI_403_REDIAGNOSIS_2026-10-27.md`.)
4. **Reviewer availability is the real bottleneck.** CodeRabbit is the only consistently eligible reviewer; Qodo exhausted; Cubic
   blocked yet still auto-posting; Greptile not connected; Codex Security usage-limited. A V3 build method must define a zero-cost
   reviewer path (e.g. local independent-model review with recorded limitation) rather than `REVIEW_BLOCKED` stalls.

V3 recommendation (detailed in `08_*` and `11_*`): replace the successor chain with **one** stable governance script + protected-path
manifest; keep exact-head + independent-review evidence; move gate depth to risk class (docs < product UI < trusted core/effects).

---

## 6. Salvage inventory

| Salvage | Keep as | Target in V3 |
|---|---|---|
| `crates/contracts` frame/protocol + tests | code | Core sidecar protocol (`wepld-core` ↔ shell main process) |
| `crates/core` identity, evidence_store, git_topology, doctor, cli + tests | code | Core crate (unchanged API; new consumers) |
| Adversarial S1/S2 tests (`s1_011_adversarial_v1.rs`, `identity_store_v1.rs`, `git_topology_v1.rs`) | negative oracles | Core regression suite |
| Spec 006 data model §2–§21 | contracts | Event/receipt schema (`07_*` §5) |
| Spec 007 threat model | requirements | Terminal/process threat model for donor PTY host |
| Astro benchmark & security plans, ASTRO-B01 (#342) | inputs | `09_*` |
| Build Learning ledger BL-0001… | knowledge | carried as history |
| `glib-0.18.5-wepld1` patch | dependency patch | Retire with Tauri shell (Electron path) — keep if Tauri kept for any tool |
| Governance successor scripts v1–v72 | history | Archive; replace with one stable checker |

---

## 7. Unknowns ledger (this document)

| ID | Unknown | Why it matters | Closure |
|---|---|---|---|
| U-01-1 | Exact date/actor of the public→private visibility change | No longer explains H1 (withdrawn); still relevant to plan/billing history | Repo audit log (owner UI) |
| U-01-2 | Whether founder intends the repo to stay private | Determines governance enforcement option (public vs GitHub Pro/Team) | Founder decision (ADR-010) |
| U-01-3 | Rights basis for T3/Orca reuse beyond public licenses | Founder-attested; recorded as `FOUNDER-ATTESTED` | No disclosure required; verify license files at acquisition |

## 8. Update 2026-10-27T17:39Z

- Repository visibility is now **PUBLIC** (founder change). Run 36589753362 attempt 3 (unchanged SHA) **succeeded** —
  `main` is green. H1 is resolved as a transient failure; see `CI_403_REDIAGNOSIS_2026-10-27.md` §4.
