# 17 — Trust-Boundary Specification (revision after Astro round 1)

```text
STATUS = PROPOSED specification (planning only; nothing implemented or run)
SUPERSEDES = 07 §3 replay-class paragraph, 07 §4 chain formula and integrity claim, 07 §6 approvals / mediation /
             containment paragraphs, 09 T10b wording, R17 §8.4 replay classes for text input, R18 §3.2 idempotency line
ADDRESSES = Astro H-1 (coverage), H-4 (reconciliation), H-5 (process fencing), H-6 (approval presentation),
            H-9 (ledger envelope/anchors), M-2 (operation identity)
TESTS = 23 §4 and §13 (COV, REC, PH, APR, LED, OPID, PEM, CLM) — each negative names guard, mutant, fixture, observable failure
REVISION_4 = Astro round 2: A2-09 (§1 rewritten), A2-10 (§2.2–§2.3 rewritten), A2-13 (§4.5 claim templates)
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

## 1. Per-operation reconciliation contracts (H-4; revised for A2-09)

Two separate records per effect (never merged):

- **Execution outcome** ∈ {`APPLIED`, `NOT_APPLIED`, `UNKNOWN`} — what Zain's dispatched operation actually did.
- **Content observation** ∈ {`CONTENT_EQUIVALENT`, `CONTENT_DIFFERENT`, `NOT_OBSERVED`} — whether current state matches the
  intended post-state. Content equivalence never implies an execution outcome (ABA, no-op, pre-existing post-state).

Rules:
- **R-1 (APPLIED):** requires an operation-unique receipt: an object identity created by the operation itself, a CAS result
  returned to Zain, a server response bound to the operation key, or a durable log entry written by the system that
  performed the operation and carrying the operation id.
- **R-2 (NOT_APPLIED):** requires positive evidence that the operation can no longer take effect: the operation's own
  staged object is still unconsumed **and** the target still has the pre-image object identity **and** the executor is
  quiescent (§3); or a terminal failure response; or a precondition the request was pinned to has become impossible.
  Current state alone never proves absence unless the transition is monotonic **and** no request is still pending.
- **R-3:** otherwise `UNKNOWN`; dependents stay blocked unless policy allows proceeding on `CONTENT_EQUIVALENT`, and the
  audit record keeps `UNKNOWN` execution.

| Effect class | APPLIED evidence (R-1) | NOT_APPLIED evidence (R-2) | Content observation | Retry safety |
|---|---|---|---|---|
| `fs.write` / `fs.edit` (fs-gate fresh-file replacement, 19 §3) | target's file id (NTFS FileId; Linux/macOS inode + birth time) equals the id of the staged temp object recorded at dispatch | staged temp object (recorded id) still present at its op-id path **and** target file id = recorded pre-image id **and** quiescent | hash vs intended | retry only after NOT_APPLIED; UNKNOWN → Inbox |
| `fs.move` / `fs.delete` (rename into op-id staging, then remove) | destination file id = source's recorded id / staging entry consumed per journal | source still has recorded id at original path **and** staging empty **and** quiescent | presence/hash | as above |
| `git.commit` / local ref update | reflog entry carrying `zain-op:<id>` with expected old → new (written by git in the ref transaction) | ref = expected old **and** no reflog entry for the op **and** quiescent **and** reflog intact since dispatch | ref value | reflog missing/expired → UNKNOWN |
| `git.push` | push response recorded with `old..new` for the ref | never from remote state | remote = new → CONTENT_EQUIVALENT only | leased push retry is idempotent in end state but re-triggers hooks/CI → approval |
| `git.pr.create` | API response with PR number recorded, or PR found carrying body marker `zain-op:<id>` | never (search is eventually consistent) | — | retry only after marker search + approval |
| `git.pr.merge` (API `sha` pinned) | response recorded, or PR merged with head = pinned sha **and** merged_by = the operation's credential identity **and** merge event after dispatch | terminal failure response; or PR head ≠ pinned sha **and** PR not merged at the pinned sha (the pinned request can no longer succeed); a read showing `merged=false` with the same head is **not** evidence (request may still be pending) | merged state | retry after NOT_APPLIED only |
| API calls with idempotency keys | adapter query by key returns the completed result | adapter query returns a terminal "not processed" for the key per documented semantics | — | per adapter |
| `ci.rerun`, webhooks, keyless APIs | response recorded | never | — | NEVER auto-retry |
| `browser.navigate` | committed URL for browser-local state only | — | server-side effects not claimed | re-approval for non-dev origins |
| `browser.input.text`, `click`, `form.submit`, `upload`, `devtools` evaluate | — | — | — | NEVER |
| `browser.download` | quarantine file id + SHA-256 recorded by Zain | download session closed with no file | hash | RECONCILABLE |
| `process.spawn`, `terminal.input` | — | — | — | NEVER |
| Continuation fire | receipt `cont:{id}:{seq}` | Server confirms no receipt **and** epoch current | — | two-phase (07 §5) |

Stale reads (A2-09): a remote observation is usable only if it was taken after the dispatch record and carries provider
freshness (no cached response); otherwise it is ignored (REC-10). Tests REC-01..REC-10, W6, BRW-AT-18, DG-N14.

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

### 2.2 Authorized-content equivalence (ACE) — renamed from "tree provenance" (A2-10)

`ACE` holds when replaying the receipted, MEDIATED write effects of the mission in ledger order on the bound base tree
(tree id, file modes, paths) reproduces the candidate tree exactly. **ACE is a content property**: the accepted content
equals what authorized writes would produce. It is **not causal provenance**: an unmediated process may have written
identical bytes, or written and then been overwritten (COV-08). Execution provenance requires COVERED/CONTAINED coverage
(§2.1), which shells and interpreters do not have before P8.

### 2.3 Completion decisions and mandatory scopes (revised)

Mandatory critical scopes come from **Core project policy** (C-05), not from the caller. Default policy scopes: writes
outside the worktree; pushes or merges to protected refs; network to non-allowlisted destinations; credential stores.
Missions may add scopes; they can never remove or empty the policy set (COV-09).

| Result | Conditions |
|---|---|
| `COMPLETED_TRUSTED` | evaluator evidence passes **and** ACE **and** every execution context active in the mission window has COVERED/CONTAINED coverage for every dimension touched by a mandatory or declared scope **and** approval levels recorded |
| `COMPLETED_CONTENT_EQUIVALENT` | evaluator evidence passes and ACE holds, but some required coverage is UNKNOWN → **not trusted**; lists contexts and scopes |
| `COMPLETED_WITH_UNMEDIATED_LIMITATION` | evaluator evidence passes, ACE fails |
| `NOT_COMPLETE` / `BLOCKED` | as before |

Consequence before P8: any mission whose contexts ran shells/interpreters cannot reach `COMPLETED_TRUSTED`, because the
default scopes need fs/net coverage those contexts lack. Completion decisions start in R2 (V-04); **R1 makes no completion
decision** and the name "Trusted Starter" refers to Core decisions for enumerated effects only (21 §3).

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

### 4.5 Approval levels and claim templates (revised for A2-13)

| Level | Mechanism | Claim template (exact text shown; X-01/CLM-02) | Not claimed |
|---|---|---|---|
| A1 | Core-owned native surface + platform authenticator (webauthn.dll) | "Approved with your device authenticator in a window drawn by Zain Core; the text you saw is bound to the approval." | protection from a compromised Zain Server (which launches Core) or same-user malware |
| A2 | isolated Electron approval window (desktop main) + Chromium WebAuthn | "Approved with your device authenticator in an isolated Zain window; the desktop process is trusted for what you saw." | protection from a compromised desktop main, Server or same-user malware |
| A3 | TOTP code in the A2 window | "Approved with a one-time code. No device-bound user presence; codes can be phished." | user presence, device binding, display integrity beyond A2 |

The level is part of the binding, stored with every approval, shown in the trust indicator, and selects the claim template.
A downgrade (A1→A2→A3) requires an assertion at the current level and is shown (APR-09). "Approval impossible without user
presence" applies to A1/A2 only.

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
