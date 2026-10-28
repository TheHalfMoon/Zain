# 17 — Trust-Boundary Specification (revision after Astro round 1)

```text
STATUS = PROPOSED specification (planning only; nothing implemented or run)
SUPERSEDES = 07 §3 replay-class paragraph, 07 §4 chain formula and integrity claim, 07 §6 approvals / mediation /
             containment paragraphs, 09 T10b wording, R17 §8.4 replay classes for text input, R18 §3.2 idempotency line
ADDRESSES = Astro H-1 (coverage), H-4 (reconciliation), H-5 (process fencing), H-6 (approval presentation),
            H-9 (ledger envelope/anchors), M-2 (operation identity)
TESTS = 23 §4 (COV, REC, PH, APR, LED, OPID, PEM) — each negative names guard, mutant, fixture, observable failure
EARLY_GATE = C-00 (P1) qualifies the Windows mechanisms in §3 and §4 before P3 starts
```

## 0. Vocabulary

| Term | Meaning |
|---|---|
| Launch authorization | Core decided that a specific process/tool invocation may start (a MEDIATED effect). |
| Execution context | Everything that runs because of one launch: the process, its descendants, and provider-internal tools executed inside it. Identified by `execution_context_id`. |
| Coverage | For one execution context and one dimension (fs, net, proc): whether every effect in that dimension is known to pass a PEP (`COVERED`), is bounded by an enforced OS sandbox (`CONTAINED`, P8+), or neither (`UNKNOWN`). |
| Observation | A fact read after the fact (file hash, ref value, page URL). Observations never establish coverage. |
| Outcome knowledge | `APPLIED` / `NOT_APPLIED` / `UNKNOWN` for one dispatched effect. |
| Retry safety | Whether re-executing is acceptable; independent of outcome knowledge. |

## 1. Per-operation reconciliation contracts (H-4)

Rule R-1: an observation proves `NOT_APPLIED` **only** when (a) the state is monotonic and cannot be undone by any
writer, or (b) the effect is an atomic local operation, the expected pre-state is still present, **and** the executor is
proven quiescent (§3). Otherwise the result is `UNKNOWN`. Rule R-2: an observation proves `APPLIED` only for the specific
operation when it carries an operation-unique marker (content hash, CAS result, server receipt, marker string).
Rule R-3: inconclusive → `UNKNOWN`; dependents stay blocked; Inbox decides.

| Effect class | APPLIED evidence | NOT_APPLIED evidence | Otherwise | Replay class / retry safety |
|---|---|---|---|---|
| `fs.write` / `fs.edit` (fs-gate atomic replace, 19 §3) | file content hash = expected new hash | pre-image hash present **and** executor quiescent | UNKNOWN | RECONCILABLE; retry safe once outcome known |
| `fs.move` / `fs.delete` | destination present with expected hash / source absent | source present with pre-image hash **and** quiescent | UNKNOWN | RECONCILABLE |
| `git.commit` (local) | objects written first (SAFE), then `update-ref <ref> <new> <expected-old>`; ref = new | ref = expected-old **and** quiescent | UNKNOWN (another writer moved the ref) | RECONCILABLE |
| `git.push` | leased push `--force-with-lease=<ref>:<old>`; remote ref = new OID (content-addressed: "applied or content-equivalent") | **never** from remote = old (a push may have happened and been reset) | UNKNOWN | RECONCILABLE for knowledge = APPLIED only; retry = same leased push, idempotent in end state, but re-triggers hooks/CI → approval required |
| `git.pr.create` | PR found with body marker `zain-op:<logical_operation_id>` | not provable (search is eventually consistent) | UNKNOWN | NEVER auto-retry; retry requires approval after marker search |
| `git.pr.merge` | PR merged with `merge_commit_sha` and head = expected sha (merge API `sha` parameter) | `merged=false` (monotonic) **and** head = expected sha | UNKNOWN | RECONCILABLE |
| `ci.rerun`, webhook/API calls without idempotency keys | server receipt if returned | not provable | UNKNOWN | NEVER |
| API calls with idempotency keys (e.g. MCP tools declaring `_meta.idempotencyKey` + query) | adapter query by key | adapter query by key returns absent **and** provider documents key semantics | UNKNOWN | RECONCILABLE per adapter (qualified at V-05) |
| `browser.navigate` | committed URL = target (browser-local state only) | — | server-side effects of the navigation are **not claimed** | RECONCILABLE for browser state only; re-navigation to non-dev origins needs re-approval |
| `browser.input.text` | — | — | UNKNOWN (input handlers may autosave/submit) | **NEVER** (changed from R17 RECONCILABLE) except Test-lane fixtures declared side-effect-free |
| `browser.click`, `browser.form.submit`, `browser.upload`, `browser.devtools` evaluate | — | — | UNKNOWN | NEVER |
| `browser.download` (to quarantine) | file SHA-256 in quarantine | file absent **and** download session closed | UNKNOWN | RECONCILABLE |
| `process.spawn`, `terminal.input` | — | — | UNKNOWN (descendant effects, §2) | NEVER |
| `model.call` (review/LLM) | response stored | — | UNKNOWN | SAFE for repository; cost-bearing, budgeted |
| Continuation fire | receipt `cont:{id}:{seq}` in T3 | Server confirms no receipt **and** Server epoch current | UNKNOWN | two-phase (07 §5) |

These contracts are implemented once in Core (C-26) and used by every component (browser Y-05, DeskGate H-02/H-03,
review fixes K-06, git S7). Tests REC-01..05, W6, BRW-AT-18, DG-N14.

## 2. Execution coverage and Trusted Completion (H-1)

### 2.1 Coverage states

For each execution context Core records `coverage = {fs, net, proc} ∈ {COVERED, CONTAINED, UNKNOWN}`:

| Execution context | fs | net | proc |
|---|---|---|---|
| ACP agent using only client `fs/*` methods, no terminal, no internal tools (qualified per 18) | COVERED | UNKNOWN unless the agent declares no network and 18 qualifies it | COVERED |
| Provider tool call approved through 18 and executed by the provider (e.g. Claude Edit) | COVERED for that write **only if** the provider row in 18 is ENFORCED for writes and no shell ran in the context | UNKNOWN | COVERED only if no process tool ran |
| Any shell, interpreter, test runner, package manager, debug adapter, CLI agent in PTY, DeskGate `start_process` | UNKNOWN | UNKNOWN | UNKNOWN |
| Provider-internal execution not routed through a callback (18 cells marked UNKNOWN) | UNKNOWN | UNKNOWN | UNKNOWN |
| Any context inside an enforced OS sandbox (P8, after escape suite) | CONTAINED within policy | CONTAINED | CONTAINED |

Launch authorization is still recorded (MEDIATED), but it never upgrades coverage. File-hash diffs and PostToolUse
reports are observations: they can **reveal** unmediated changes; their absence proves nothing (reverted writes,
off-tree paths and remote effects are invisible to them). Coverage is UNKNOWN from launch until the context is proven
terminated (§3).

### 2.2 Tree provenance

`TREE_PROVENANCE_COMPLETE` holds when replaying the receipted, MEDIATED write effects of the mission in ledger order on
the mission base tree reproduces the candidate tree hash exactly. It proves the accepted **content** is the product of
recorded, authorized writes (unmediated writes either did not touch the tree or cancelled out). It does not prove that
no off-tree, network or process effect occurred.

### 2.3 Completion decisions (replaces 07 §6 "Mediation classes" completion sentence)

| Result | Conditions |
|---|---|
| `COMPLETED_TRUSTED` | evaluator evidence passes **and** `TREE_PROVENANCE_COMPLETE` **and** for every critical scope the mission declares (e.g. "no push to production", "no network to X"), every execution context active in the mission window has coverage `COVERED`/`CONTAINED` in the relevant dimension **and** approval level recorded |
| `COMPLETED_WITH_UNKNOWN_COVERAGE` | evaluator evidence passes and tree provenance complete, but a declared critical scope has UNKNOWN coverage → shown as not trusted; lists the contexts |
| `COMPLETED_WITH_UNMEDIATED_LIMITATION` | evaluator evidence passes but tree provenance incomplete |
| `NOT_COMPLETE` / `BLOCKED` | as before (Spec 006 §20) |

Missing coverage evidence never becomes PASS (baseline invariant `Missing … containment evidence != PASS`). Verification
commands (tests) run in a disposable copy of the candidate tree so their writes cannot change the evaluated tree; their
own network/process effects are reported as UNKNOWN coverage, not hidden.

**Practical consequence before P8 (stated in R1/R2 claims, 21 §3):** a mission that uses shells or interpreters can reach
`COMPLETED_TRUSTED` only for content provenance and only when it declares no off-tree critical scope; claims about the
absence of off-tree or network side effects are unavailable until P8 containment.

### 2.4 Plan Mode

A plan turn is "enforced read-only" only if every execution context in the turn has fs coverage COVERED (no shell, no
provider cell with UNKNOWN writes). Otherwise the plan is approvable but labelled "read-only not enforced" (L-01 label
persists), and the turn-end diff (N9) still invalidates on any observed product change. Test COV-07.

## 3. Process lifecycle, fencing and quiescence (H-5)

Connection fencing (07 §3) stops stale **IPC**; it does not stop running processes. ProcessHost (C-25) owns all launches;
Orca's `taskkill /t /f` (R12 D4, `windows-tree-kill.ts` L20–27) is a tree walk by parent PID, not containment, and is used
only as reference.

| Concern | Windows | Linux | macOS |
|---|---|---|---|
| Ownership | Server process runs inside an outer Job Object; each launch gets a nested job; the child is created `CREATE_SUSPENDED` with `PROC_THREAD_ATTRIBUTE_JOB_LIST` (atomic assignment, no window between create and assign), then resumed | cgroup v2 leaf per launch (user delegation via systemd `--user` scope; fallback: process group + `PR_SET_CHILD_SUBREAPER`, labelled weaker) + pidfd | process group via `posix_spawn` `POSIX_SPAWN_SETPGROUP`; descendants can `setsid` away → **not contained** (coverage remains UNKNOWN; quiescence best-effort) |
| Breakaway | `JOB_OBJECT_LIMIT_BREAKAWAY_OK` and `SILENT_BREAKAWAY_OK` never set | cgroup membership inherited | n/a |
| Handle inheritance | `PROC_THREAD_ATTRIBUTE_HANDLE_LIST` limits inherited handles to stdio/ConPTY | `close_range` before exec | `POSIX_SPAWN_CLOEXEC_DEFAULT` |
| ConPTY | PTY sessions created by the same native helper (not node-pty's own spawn) so the pseudoconsole child is job-assigned at creation | same cgroup path | same pgroup path |
| Server crash | outer and nested jobs have `KILL_ON_JOB_CLOSE`; the Server holds the only handles → descendants are killed by the OS when the Server dies | cgroup `cgroup.kill` by the restarted Server; pidfd poll | `killpg`; survivors possible |
| Escapes | WMI `Win32_Process.Create`, Task Scheduler, services, COM out-of-proc servers, `explorer` DDE start processes outside the job → undetectable as ours | `systemd-run`, `at`, user services → outside cgroup | many |

**Quiescence protocol.** Before Core accepts a retry, a `NOT_APPLIED` conclusion (§1 R-1b) or a new dispatch for the same
logical operation after a Server restart, the new Server must attest that every launch of the previous epoch is
terminated: recorded `(pid, creation_time)` pairs are checked (PID reuse safe) and, on Windows, job closure is
guaranteed by `KILL_ON_JOB_CLOSE`. If attestation fails or the platform cannot attest (macOS, escapes), the affected
effects stay `UNKNOWN` and no automatic retry happens. Escapes are an accepted residual risk before P8 and are the reason
coverage stays UNKNOWN for shells (§2).

Feasibility: C-00 FG-01 must show job-at-creation for ConPTY children on Windows 11 before P3; NO-GO → P3 ships with
`taskkill`-style best effort, every process effect UNKNOWN, and the R1 claim text says so.

## 4. Approvals: presentation, binding, enrollment, recovery (H-6)

### 4.1 Threats separated

| Threat | Mitigation | Residual |
|---|---|---|
| Forged or replayed approval (renderer XSS, rogue client) | assertion verified by Core over the canonical binding (§4.2) | none known for mediated effects |
| **Deceptive display**: renderer shows A while requesting an assertion for B | approval text is rendered by a **Core-owned approval surface**, never by the web renderer; the binding includes the digest of that exact text | compromised Core (TCB) |
| Compromised Server | Server is the PEP and in the TCB (07 §6); it can execute effects without asking. Signed approvals then provide after-the-fact evidence only | stated, not mitigated |
| Same-user malware overlaying windows | user presence (biometric/PIN) cannot be produced by malware; overlay can mislead | stated residual before P8 |
| Credential replacement by attacker | add/replace requires an existing-credential assertion or the recovery code | recovery code theft |

### 4.2 Canonical binding

`challenge = SHA-256("zain-approval-v1" ‖ CBOR_canonical{proposal_id, logical_operation_id, effect_class, exact_target,
input_digest, decision, scope ∈ {once, session, persistent}, principal, mission_id, expiry, fencing_epoch,
display_text_digest, approval_level})`. `display_text` is produced by a deterministic renderer in Core from the same
fields. Core rejects an assertion whose challenge does not match a pending proposal exactly; scope widening, expiry
extension or a new epoch require a new assertion (APR-02, APR-05, APR-06).

### 4.3 Approval surface (level A1 target)

Core spawns `zain-approve` (small native Rust helper, not spawned by the Server, no web content). It renders
`display_text`, then calls Windows `webauthn.dll` (`WebAuthNAuthenticatorGetAssertion`) with its own window handle and
returns the assertion to Core over a private pipe. The web UI only shows "approval pending in the system dialog".
macOS/Linux equivalents (AuthenticationServices / FIDO2 via libfido2) are P6 work; until then those platforms use A2.

### 4.4 Enrollment and recovery

- First run: Core-owned surface enrolls a platform credential (user presence) and shows a one-time recovery code
  (stored as Argon2id hash).
- Add/replace credential: assertion from an existing credential, or recovery code. Remove: assertion.
- Recovery via code: all standing grants revoked, fencing epoch bumped, ledger event, persistent banner for 7 days (APR-04).
- Credential public keys live in the Core data root under the deny floor (T10b).

### 4.5 Approval levels (versioned claims; never silently substituted)

| Level | Mechanism | Claim |
|---|---|---|
| A1 | Core-owned native surface + platform authenticator via webauthn.dll | resists forged/replayed approvals and deceptive display by the web renderer |
| A2 | isolated Electron approval window owned by desktop main, static bundled page (no web-app code), text = Core display_text relayed with digest check + Chromium WebAuthn | as A1 except a compromised desktop main can deceive |
| A3 | TOTP second factor in the A2 window | no device-bound user presence; phishable; deceptive display by desktop main possible |

The level is part of the binding, stored with every approval and completion record, and shown in the trust indicator
(APR-07). C-00 FG-02/FG-03 decide whether A1 is available at R1; if not, R1 claims are stated at A2.

## 5. Ledger envelope and anchors (H-9)

- **Row:** `ledger_events(v, seq, ts, kind, project_id, subject_id, principal, payload_json, payload_digest, prev_hash, hash)`.
- **Hash:** `hash = SHA-256("zain-ledger-v1" ‖ CBOR_canonical{v, seq, ts, kind, project_id, subject_id, principal,
  payload_digest, prev_hash})`, `payload_digest = SHA-256(canonical_json(payload))`. Every authoritative column is
  inside the hash; verification recomputes from the columns (LED-01/02). Projections are rebuilt from events only.
- **Partitions:** per-project export carries the full chain segment plus the boundary hashes; import verifies segment
  continuity; cross-partition references carry `(seq, hash)`.
- **Anchor:** `ledger.anchor` signs `{seq_n, hash_n, ts}` into a signed git note/tag the founder pushes. An anchor proves
  that the prefix `0..n` existed with that head when signed; rewriting that prefix is detected (LED-04).
- **Unanchored interval:** events after the last anchor are protected only by the local chain. A same-user adversary
  can truncate or rewrite them and recompute the chain; this is **not detectable by the chain**. Partial detection
  exists when other records reference later seqs (T3 `zain.run-receipts` head hashes, approvals held by the user's
  phone in P10). `ledger.verify` reports the unanchored interval explicitly (LED-03, LED-05). 09 T10b is revised
  accordingly.

## 6. Logical operation identity (M-2)

- `logical_operation_id` is allocated by Core on the first `effect.propose` for `(principal, mission_id,
  client_operation_key)`; clients that cannot supply a stable key (plain MCP) get a Core-allocated id returned in the
  result and must echo it on retry (DeskGate: `_meta.zainOperationKey`).
- Transport ids (MCP request ids, WS frame ids) are **attempt** data only: `attempt_id` per transport delivery.
- The same `logical_operation_id` with a different `input_digest` is rejected with `OPERATION_INPUT_CONFLICT`
  (OPID-01, DG-N16). Retries after reconnect reuse the operation id and get the stored decision/outcome (OPID-02).
- Replaces R18 §3.2 "logical_operation_id = MCP request id + tool + args digest" and 07 §3 idempotency wording.
