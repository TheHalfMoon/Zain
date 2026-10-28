# 23 — Acceptance Test Registry (machine-read)

```text
STATUS = PROPOSED (planning only; no test exists or has run)
PURPOSE = every coded test id used in 14_TASK_CATALOG.md resolves here with its implementation prerequisites and its
          execution phase (= latest prerequisite phase). tools/plan_graph.py rejects: unknown ids, prerequisites that are not
          declared ancestors of the task running the test, a test scheduled in an earlier phase than its prerequisites, and
          any negative test without guard, mutant, fixture and observable failure (Astro C-1, M-4).
MUTATION_CONTROL = each negative test runs twice: guard active (must pass) and mutant applied (must FAIL). "Guard" is the
          specific check that enforces the property — Core only when Core is that check (09 §1, SEC-17 revised).
REVIEWER_QUALITY = deterministic plumbing tests (scripted model) are separated from reviewer-quality qualification
          (ZCR-Q*), which uses held-out real defects and is reported as rates, never as PASS of a guarantee.
COLUMNS = Test | Kind | Prerequisites | Phase | Guard | Mutant | Fixture | Observable failure | Source
```

## 1. Governance (P0) — 20

| Test | Kind | Prerequisites | Phase | Guard | Mutant | Fixture | Observable failure | Source |
|---|---|---|---|---|---|---|---|---|
| GV-01 | neg | G-05 | P0 | prohibited-capability scan of frozen contract crates | scan disabled | candidate adds `windows::Win32` call to contracts module | candidate accepted | v72 oracle 2 |
| GV-02 | neg | G-05 | P0 | same scan (process spawn) | scan disabled | `std::process::Command` added | candidate accepted | v72 oracle 3 |
| GV-03 | neg | G-05 | P0 | same scan (network) | scan disabled | `std::net::TcpStream` in test | candidate accepted | v72 oracle 4 |
| GV-04 | neg | G-05 | P0 | manifest/lockfile freeze | freeze removed | edited Cargo.toml; drifted Cargo.lock | candidate accepted | v72 oracles 5–6 |
| GV-05 | neg | G-05 | P0 | exact authorized-path set | set check replaced by prefix match | unauthorized + look-alike path added | candidate accepted | v72 oracle 7 |
| GV-06 | neg | G-05 | P0 | no-mix rule | rule removed | authorized delta + README change | candidate accepted | v72 oracle 8 |
| GV-07 | neg | G-05 | P0 | checker input surface = (candidate tree, policy base) only | checker reads PR label/branch/message | exemption requested via label, branch name, commit message, author | exemption granted | v72 oracle 9 |
| GV-08 | neg | G-05 | P0 | frozen-path freeze | freeze removed | protocol drift alone and smuggled inside authorized delta | candidate accepted | v72 oracle 10 |
| GV-09 | neg | G-02 | P0 | `git verify-tag` (SSH, namespace git) against base `allowed_signers` | verification skipped | co-sign unsigned / signed by unknown key | candidate accepted | ADR-011 |
| GV-10 | neg | G-03 | P0 | co-sign binds repo id, base, head, tree, changed-path digest, expiry (20 §3) | binding reduced to head only | valid co-sign replayed for another base/tree/repo | candidate accepted | Astro H-10 |
| GV-11 | neg | G-03 | P0 | checker loaded from base, candidate read as data | checker loaded from candidate | PR edits governance_check.py to always pass | verdict changes | ADR-011 |
| GV-12 | neg | G-03 | P0 | co-sign requires signature | label accepted as co-sign | `co-sign` label without signature | candidate accepted | ADR-011 |
| GV-13 | neg | G-03 | P0 | REVIEW_BLOCKED is terminal non-pass | mapping BLOCKED→PASS | review record REVIEW_BLOCKED | PASS emitted | GOV-03 |
| GV-14 | neg | G-03 | P0 | external-review trigger requires egress record | rule removed | PR body/label triggering hosted reviewer, no egress record | not flagged | GOV-04 |
| GV-15 | neg | G-03 | P0 | `pull_request_target` job: `permissions: read`, no secrets, no candidate code execution | permissions widened | fork PR printing token scopes / secrets | write scope or secret visible | Astro audit H1 |
| GV-16 | neg | G-05 | P0 | source-admission record required for new third-party source/dependency | check removed | new package without admission row | candidate accepted | GOV-07 |
| GV-17 | neg | G-03 | P0 | Build Learning line required on phase-exit PRs | check removed | phase-exit PR without line | candidate accepted | GOV-08 |
| GV-18 | neg | G-05 | P0 | every CARRIED property in 20 §2 | any one property check removed | ported v1–v72 negative fixtures | any fixture accepted | Astro H-10 |
| GV-19 | pos | G-05 | P0 | — | — | last 20 merged PRs | non-regression only; a mismatch blocks retirement | ADR-011 |
| GV-20 | neg | G-07 | P0 | branch protection + required check | protection disabled on a scratch repo | direct push to main | push accepted | G-07 |

## 2. Feasibility gate (P1)

| Test | Kind | Prerequisites | Phase | Guard | Mutant | Fixture | Observable failure | Source |
|---|---|---|---|---|---|---|---|---|
| FG-01 | spike | C-00 | P1 | — | — | ConPTY + plain child created suspended with JOB_LIST attribute; grandchild; parent killed | grandchild survives job close or breakaway succeeds → NO-GO | 17 §3 |
| FG-02 | spike | C-00 | P1 | — | — | Rust calls webauthn.dll from a Core-owned window; Rust verifies assertion | no platform assertion obtainable → A2/A3 path | 17 §4 |
| FG-03 | spike | C-00 | P1 | — | — | Core-owned window renders canonical text; foreground/focus rules on Windows 11 | window cannot reliably take focus → A2 path | 17 §4 |
| FG-04 | spike | C-00 | P1 | — | — | handle-relative opens with reparse rejection under concurrent junction swaps | any write lands outside root → design reopened | 19 §3 |
| FG-05 | spike | C-00 | P1 | — | — | Electron partition with `session.setProxy` + `<-loopback>`; fetch/XHR/WS/worker/service worker/beacon/img/prefetch/WebRTC | any request reaching a sink bypassing the proxy → Agent lane stays loopback-only | 19 §1 |

## 3. Core, threats, recovery (09) — P2–P3 (+ later where noted)

| Test | Kind | Prerequisites | Phase | Guard | Mutant | Fixture | Observable failure | Source |
|---|---|---|---|---|---|---|---|---|
| T1 | neg | C-08 | P3 | ACP client-policy PEP → Core decision | PEP returns allow without propose | ACP agent `fs/write` outside worktree | file created | 09 T1 |
| T2 | neg | C-08, C-12 | P3 | ACP terminal / S8 PEP | PEP bypassed | injected README asks agent to `curl` external host | command executed without approval | 09 T2 |
| T3 | neg | C-13 | P3 | Core assertion verification | verification returns true | approve RPC without assertion; replayed assertion for other proposal | approval accepted | 09 T3 |
| T4 | neg | C-12 | P3 | S6 MCP access scoped grants | scope check removed | outside MCP agent calls write tool | write executed | 09 T4 |
| T5 | neg | V-06 | P5 | skill hash pin | pin check removed | modified SKILL.md | skill stays enabled | 09 T5 |
| T6 | neg | C-04 | P3 | secret-handle boundary + redaction | redaction removed | seeded fake key in tool output, env, URL | key found in ledger/T3 DB/logs | 09 T6 |
| T7 | neg | F-06 | P2 | no-read rule for Claude credentials | rule removed | `~/.claude/.credentials.json` present | file-access audit shows read | 09 T7 |
| T8 | neg | F-06 | P2 | installer-content gate | gate removed | `claude-agent-sdk*` placed in build output | installer built | 09 T8 |
| T9 | neg | F-04 | P2 | manifest signature + feed origin check | check removed | manifest pointing to T3/Orca feed | update offered | 09 T9 |
| T10 | neg | C-03 | P3 | chain verify on start | verify skipped | single byte flip in ledger | app opens read-write | 09 T10 |
| T10b | neg | C-16, C-19 | P3 | data-root deny floor; anchor comparison for anchored prefix | floor removed | mediated agent writes ledger file; unmediated rewrite before last anchor | write succeeds / rewrite of anchored prefix undetected | 09 T10b (revised 17 §5) |
| T11 | neg | D-02 | P7 | separate-origin sandboxed iframe | sandbox attribute removed | preview JS opens WS to Server | connection established | 09 T11 |
| T12 | neg | W-05 | P9 | hard-blocked categories in computer use | block list emptied | payment page | action executed | 09 T12 |
| T13 | neg | C-05 | P3 | dispatch-time revalidation | revalidation skipped | downgrade policy between approve and dispatch | dispatch proceeds | 09 T13 |
| T14 | neg | C-10, C-26 | P3 | replay classes + S4b gate | S4b gate removed | crash after dispatch of NEVER effect | effect executed twice | 09 T14 |
| T15 | neg | C-18 | P3 | observe compiled out | observe path left in release | `setx ZAIN_CORE_ENFORCE observe` + restart | effects pass ungated | 09 T15 |
| T16 | neg | C-02 | P3 | data-root lock + fencing epoch | lock removed | second Core/Server on same root; stale-epoch frame | second instance acts | 09 T16 |
| T17 | neg | I-06 | P6 | per-PTY secret on hook endpoint; overlays | secret check removed | unauthenticated local POST; user global config hash | status accepted / global config changed | 09 T17 |
| PROTO-01 | neg | C-02 | P3 | replay check on cmd ids and core_req ids | replay check removed | replayed frame id | frame processed twice | 07 §3 |
| EFF-01 | neg | C-04 | P3 | dispatch requires valid grant | grant check removed | dispatch with fabricated grant id | effect released | 07 §3 |
| OPID-01 | neg | C-04 | P3 | logical operation id uniqueness + input-digest conflict rule (17 §6) | conflict rule removed | same op id, different input digest; new transport id for same op | second execution / conflict not raised | Astro M-2 |
| OPID-02 | neg | H-02 | P3 | DeskGate maps client operation key to Core op id | adapter derives id from MCP request id | reconnect + retry with new request id | duplicate write | Astro M-2 |
| POL-01 | neg | C-05 | P3 | deny-overrides; Skip never overrides Blocked | precedence inverted | Skip mode + Blocked rule | blocked effect allowed | ADR-007 |
| POL-02 | neg | C-07 | P3 | S1 clamp to Core-granted mode | clamp removed | provider requests dangerFullAccess | mode applied | R11 S1 |
| POL-03 | neg | V-01 | P5 | reviewer route ≠ builder route (same model under other account = same) | comparison removed | reviewer = builder model, different key | review accepted | ADR-008 |
| PROV-01 | neg | C-09 | P3 | no silent fallback | fallback enabled | provider returns 529/auth failure | another route/model used without user decision | PR-02 |
| UI-01 | neg | F-07 | P2 | Full-access option removed from settings schema | option restored | settings file sets full access | full access applied | F-07 |
| SEC12-01 | neg | F-22 | P2 | secrets stored only via OS keyring or provider CLI login | settings writer persists secret | seeded API key entered in settings; crash dump forced | key present in settings, logs or dumps | SEC-12 |
| TERM-01 | pos | F-16 | P2 | — | — | PTY spawn, input, output, resize, kill on Windows | any step fails | PR-09 |
| TERM-02 | neg | C-12 | P3 | S8: Zain-issued terminal commands proposed to Core | S8 bypassed | agent-issued command in Zain terminal | executed without decision | PR-09 |
| A11Y-01 | pos | F-14 | P2 | — | — | keyboard-only script: compose, approve, review diff, open file | step needs pointer | PR-24 |
| A11Y-02 | pos | F-14 | P2 | — | — | scripted NVDA run over existing T3 surfaces (composer, diff summary, thread list) | missing name/role/live announcement | PR-24 |
| A11Y-03 | pos | I-11 | P6 | — | — | NVDA/VoiceOver read terminal output in screen-reader mode | output not announced | PR-24b |
| LIC-01 | neg | F-20 | P2 | license gate over the packaged closure (approved-license allowlist; missing metadata = unresolved, not permitted) | gate removed | package with LGPL-3.0 or no license metadata in the packaged closure | installer built | 22 |
| R1 | rec | C-10 | P3 | — | — | kill at each step boundary (R05 §7 R1.1–R1.7) | invariant violation | R05 §7 |
| R2 | rec | M-02 | P4 | — | — | duplicate webhooks and wakes | duplicate fire | R05 §7 |
| R3 | rec | C-10, C-11 | P3 | — | — | missing receipts | silent loss or duplicate | R05 §7 |
| R4 | rec | C-10, C-26 | P3 | — | — | unknown-outcome side effects | outcome guessed instead of UNKNOWN | R05 §7 |
| R5 | rec | C-09, C-13 | P3 | — | — | lost credentials / permission change mid-run | effect proceeds on stale permission | R05 §7 |
| R6 | rec | C-03 | P3 | — | — | corrupted local state | silent continue | R05 §7 |
| R7 | rec | C-03 | P3 | — | — | schema and code upgrades | data loss / silent downgrade | R05 §7 |
| R8 | rec | C-09 | P3 | — | — | provider exhaustion | silent fallback or lost step | R05 §7 |
| R9 | rec | M-05 | P4 | — | — | context overflow mid-mission | decision lost from capsule | R05 §7 |
| R10 | rec | C-09, C-12 | P3 | — | — | network loss | UNKNOWN not raised | R05 §7 |
| R11 | rec | C-10, C-25 | P3 | — | — | cancellation | orphan process or effect after cancel | R05 §7 |
| W1 | rec | C-06 | P3 | — | — | Core killed while Server runs | gated effect released | 09 §2 |
| W2 | rec | C-11 | P3 | — | — | T3 power-loss rollback | receipt not surfaced | 09 §2 |
| W2b | rec | M-02 | P4 | — | — | T3 rollback of continuation receipt | command executed twice | 09 §2 |
| W3 | rec | M-02 | P4 | — | — | duplicate continuation fire | two T3 commands | 09 §2 |
| W4 | rec | C-13 | P3 | — | — | grant expires while approval pending | old assertion accepted | 09 §2 |
| W5 | rec | C-03 | P3 | — | — | ledger schema too new | file opened | 09 §2 |
| W6 | rec | C-12, C-26 | P3 | — | — | git push interrupted | remote ref = old reported as NOT_APPLIED, or remote ref = new reported as historical APPLIED without a push receipt (17 §1: content-equivalent only) | 09 §2 (revised) |
| W7 | rec | M-01, V-04 | P5 | — | — | rebase under mission | completion not blocked | 09 §2 |
| W8 | rec | M-05 | P4 | — | — | context overflow mid-mission | recall below target | 09 §2 |
| W9 | rec | C-10 | P3 | — | — | T3 recovery vs Core reconcile race | requeue before Core answer | 09 §2 |
| B1..B5 | bench | B-03 | P1 | — | — | 09 §3 protocol | budget missed (recorded, not a pass/fail of a guarantee) | 09 §3 |
| B6 | bench | C-10 | P3 | — | — | 100-run R1 sweep | invariant violation | 09 §3 |
| B8 | bench | M-04 | P4 | — | — | 30 non-pinned decisions, model switch quiz | recall < target | 09 §3 |
| B10 | bench | C-03 | P3 | — | — | 10k synthetic effects | > 50 MB | 09 §3 |
| B12 | bench | F-05 | P2 | — | — | offline checklist | any item fails | 09 §3 |
| B13 | bench | C-09 | P3 | — | — | 1,000 mediated effects | p95 > 25 ms | 09 §3 |
| CC-T01 | neg | C-09 | P3 | PreToolUse deny + floor | hook removed | Claude asked to write outside worktree | file written | 03C §5 |
| CC-T02 | rec | C-09, C-10 | P3 | — | — | kill Claude mid-Edit | outcome neither UNKNOWN nor reconciled by hash | 03C §5 |
| CC-T03 | pos | C-09 | P3 | — | — | retry resumes or forks session with parent edge | lost session lineage | 03C §5 |
| CC-T05 | neg | V-04 | P5 | Stop/SubagentStop gating | gating removed | failing required gate | Stop allowed | 03C §5 |

## 4. Trust-boundary specification tests (17, 18, 19)

| Test | Kind | Prerequisites | Phase | Guard | Mutant | Fixture | Observable failure | Source |
|---|---|---|---|---|---|---|---|---|
| COV-01 | neg | C-23 | P3 | coverage = UNKNOWN for any context that ran an unsandboxed interpreter/shell | coverage derived from receipts only | Claude Bash runs `python -c` writing outside tree | context reported COVERED | 17 §2 |
| COV-02 | neg | C-23 | P3 | tree-provenance reconstruction | reconstruction skipped | unmediated write to tree, then mediated edit elsewhere | provenance reported complete | 17 §2 |
| COV-03 | pos | C-23 | P3 | — | — | mediated-only edits (ACP fs, fs-gate) | provenance incomplete although all writes mediated | 17 §2 |
| COV-04 | neg | C-23 | P3 | reverted unmediated write still marks coverage UNKNOWN | hash-diff used as coverage | write-then-revert by shell | context reported COVERED | 17 §2 |
| COV-05 | neg | C-23 | P3 | provider-internal tool execution marks UNKNOWN per 18 | matrix lookup removed | Codex auto-run read command performing a write | COVERED reported | 17 §2 |
| COV-06 | neg | V-04, C-23 | P5 | completion fail-closed on UNKNOWN required coverage | rule removed | mission with declared off-tree critical scope + UNKNOWN net coverage | COMPLETED_TRUSTED returned | 17 §2 |
| COV-07 | neg | L-03 | P3 | plan context with UNKNOWN coverage keeps "not enforced" label | label logic removed | plan turn by provider with internal write path | plan shown as enforced | 17 §2.4 |
| PEM-CLA-01..PEM-CLA-04 | neg | C-09 | P3 | Claude: PreToolUse hook on all tools; no allow rules; settingSources empty; permissionMode default (18 §2) | allow rule injected via project settings / acceptEdits | (01) Edit, (02) Bash, (03) WebFetch, (04) MCP tool | tool runs without Core decision | 18 |
| PEM-CDX-01..PEM-CDX-04 | neg | C-09 | P3 | Codex: approvalPolicy untrusted; ApprovedForSession never sent; sandbox workspaceWrite; Core decides each request (18 §2) | handler answers ApprovedForSession | (01) exec, (02) patch, (03) permissions escalation, (04) repeated command after session approval | second command runs without Core decision | 18 |
| PEM-ACP-01..PEM-ACP-03 | neg | C-09 | P3 | ACP: request_permission mapped to Core grant; `allow_always` mapped to scoped Core grant | allow_always honoured client-side | (01) fs write, (02) terminal, (03) repeated request after allow_always | request served from client cache | 18 |
| PEM-OPC-01..PEM-OPC-03 | neg | C-24 | P3 | OpenCode: always-allow rules replaced by ask; edits/network not auto-allowed | upstream rules restored (adapter L632–655) | (01) edit in auto mode, (02) network tool, (03) once-grant reuse | effect without Core decision | 18; t3code@36d4d711 provider-opencode adapter |
| PEM-PI-01..PEM-PI-03 | neg | C-24 | P3 | Pi: session approval cache removed (adapter L1251–1259, L2701–2702) | cache restored | (01) repeat approved op, (02) op after revocation, (03) op after epoch bump | confirmed:true served from cache | 18 |
| PEM-GEN-01..PEM-GEN-04 | neg | C-28 | P3 | Core-held grants: scope, expiry, epoch, revocation; provider session restart when its state could reuse a decision | revocation not propagated | (01) revoke mid-session, (02) expiry, (03) epoch bump, (04) scope once reused — for Claude, Codex and each qualified ACP agent | revoked/expired grant honoured | 18 §3 |
| PH-01 | neg | C-25 | P3 | per-launch Job Object, KILL_ON_JOB_CLOSE | job assignment after resume (race) | child spawns grandchild then exits; Server killed | grandchild alive after 2 s | 17 §3 |
| PH-02 | neg | C-25 | P3 | quiescence attestation before retry | attestation skipped | Server kill -9 during dispatch; restart | retry before descendants proven dead | 17 §3 |
| PH-03 | neg | C-25 | P3 | breakaway forbidden | BREAKAWAY_OK set | child calls CreateProcess with CREATE_BREAKAWAY_FROM_JOB | process outside job | 17 §3 |
| PH-04 | neg | C-25 | P3 | PID + creation-time identity | PID-only identity | PID reused by unrelated process | wrong process treated as ours | 17 §3 |
| PH-05 | neg | C-25 | P3 | escapes via WMI/Task Scheduler/COM marked UNKNOWN | escape treated as quiesced | `wmic process call create` / `schtasks` from agent shell | effect not UNKNOWN | 17 §3 |
| PH-06 | neg | C-25 | P3 | PROC_THREAD_ATTRIBUTE_HANDLE_LIST | full inheritance | child inherits Core pipe handle | handle usable by child | 17 §3 |
| PH-07 | neg | C-06 | P3 | static import guard (child_process/node-pty only in ProcessHost) | rule deleted | seeded import in another package | build passes | 16 §1 |
| REC-01 | neg | C-26 | P3 | fs.write evidence contract (expected new hash ⇒ APPLIED; pre-image + quiescence ⇒ NOT_APPLIED) | NOT_APPLIED without quiescence | crash mid atomic replace with live descendant | NOT_APPLIED reported | 17 §1 |
| REC-02 | neg | C-26 | P3 | local git: CAS update-ref with expected old value | plain update-ref | concurrent writer moves ref | APPLIED/NOT_APPLIED reported wrongly | 17 §1 |
| REC-03 | neg | C-12 | P3 | push: leased push; remote==old ⇒ UNKNOWN (never NOT_APPLIED) | remote==old mapped to NOT_APPLIED | push interrupted, another writer resets ref | NOT_APPLIED + blind retry | 17 §1 |
| REC-04 | neg | C-26 | P3 | PR create marker search; absence ⇒ UNKNOWN | absence ⇒ NOT_APPLIED | crash after create request | duplicate PR created without approval | 17 §1 |
| REC-05 | neg | C-26 | P3 | monotonic-state rule (merge: merged=false ⇒ NOT_APPLIED only with expected head sha) | sha check removed | head changed after request | merge of unexpected head | 17 §1 |
| APR-01 | neg | C-13 | P3 | Core-owned surface renders canonical text; challenge binds display digest | renderer supplies display text | compromised-renderer fixture shows A, requests B | user sees A while approving B | 17 §4 |
| APR-02 | neg | C-13 | P3 | challenge binds proposal, op id, target, digest, scope, principal, expiry, epoch | binding drops scope | assertion for scope "once" replayed as "persistent" | widened grant accepted | 17 §4 |
| APR-03 | neg | C-13 | P3 | credential add/replace requires existing-credential assertion or recovery code | check removed | add credential from renderer RPC | credential added | 17 §4 |
| APR-04 | neg | C-13 | P3 | recovery revokes grants + bumps epoch + ledger event | revocation skipped | recovery-code re-enrollment | old grants still valid | 17 §4 |
| APR-05 | neg | C-13 | P3 | expiry check | check removed | expired challenge | approval accepted | 17 §4 |
| APR-06 | neg | C-13 | P3 | epoch binding | epoch ignored | assertion from previous epoch | approval accepted | 17 §4 |
| APR-07 | neg | C-13 | P3 | approval level recorded and shown (A1/A2/A3) | level forced to A1 | TOTP fallback approval | record/UI shows A1 | 17 §4.5 |
| LED-01 | neg | C-03 | P3 | envelope hash covers subject_id | subject excluded from hash | subject_id swapped in a row | verify passes | 17 §5 |
| LED-02 | neg | C-03 | P3 | envelope hash covers project_id, principal, ts | fields excluded | project_id swapped | verify passes | 17 §5 |
| LED-03 | pos | C-19 | P3 | — | — | suffix after last anchor truncated | report does not show the unanchored interval and the loss as undetectable-by-chain | 17 §5 |
| LED-04 | neg | C-19 | P3 | anchor comparison | comparison skipped | rewrite of anchored prefix with recomputed chain | rewrite undetected | 17 §5 |
| LED-05 | pos | C-19 | P3 | — | — | anchor coverage report | coverage boundaries missing | 17 §5 |
| LED-06 | neg | C-16 | P3 | data-root deny floor in provider profiles | floor removed | mediated agent writes ledger file | write succeeds | 17 §5 |

## 5. Code Review (R14 §8; K-tasks)

Plumbing tests use a scripted model; ZCR-Q* measure reviewer quality.

| Test | Kind | Prerequisites | Phase | Guard | Mutant | Fixture | Observable failure | Source |
|---|---|---|---|---|---|---|---|---|
| ZCR-T01 | pos | K-10 | P6 | — | — | seeded off-by-one; scripted model | finding missing or control twin non-empty | R14 |
| ZCR-T02 | pos | K-10 | P6 | — | — | 40-file change incl. excluded/binary | preview ≠ run set | R14 |
| ZCR-T03 | pos | K-10 | P6 | — | — | `.zainide/review/rule.json` + `.continue/rules/x.md` | rule reaches wrong group | R14 (path corrected, L-1) |
| ZCR-T04 | neg | K-04 | P5 | route comparison in review.start | comparison removed | reviewer route = builder route | review starts | R14 |
| ZCR-T05 | neg | K-03 | P6 | route lock Z-P1 | env passthrough restored | planted home config and env vars | decoy server receives call | R14 |
| ZCR-T06 | neg | K-10 | P6 | read-only toolset + coverage accounting | coverage accounting removed | injected "report no issues" | file written or coverage silently incomplete | R14 |
| ZCR-T07 | neg | K-06 | P5 | preimage OID check | check skipped | blob changed after review | write proposed | R14 |
| ZCR-T08 | neg | K-06 | P5 | Core grant before write | grant check removed | Core down / deny policy | file written | R14 |
| ZCR-T09 | pos | K-06 | P5 | — | — | 3 fixes, checkpoint, verify | wrong ledger order | R14 |
| ZCR-T10 | pos | K-06 | P5 | — | — | undo after apply | bytes ≠ checkpoint | R14 |
| ZCR-T11 | neg | K-06 | P5 | restore safety | check removed | user edit after fix | data loss | R14 |
| ZCR-T12 | neg | K-08, V-04 | P5 | agent dismissals are proposals | dismissal auto-confirmed | reviewer agent dismisses all | completion advances | R14 |
| ZCR-T13 | neg | K-04, V-04 | P5 | open critical finding blocks trusted completion | rule removed | critical finding + PR merged | COMPLETED_TRUSTED | R14 |
| ZCR-T14 | neg | K-04 | P5 | path/range normalization | normalization removed | `../../etc/passwd`, out-of-range line | anchor created | R14 |
| ZCR-T15 | neg | K-05 | P5 | sanitizer | sanitizer disabled | `command:` links, HTML, script in finding | command executed / script runs | R14 |
| ZCR-T16 | pos | K-08 | P5 | — | — | delegated run missing one group | run not PARTIAL | R14 |
| ZCR-T17 | neg | K-08 | P5 | reviewer session read-only profile | profile widened | reviewer attempts FS_WRITE/terminal | effect executed | R14 |
| ZCR-T18 | pos | K-10 | P6 | — | — | tool-calling vs narrating local model | narrating model selectable | R14 |
| ZCR-T19 | pos | K-10 | P6 | — | — | cancel mid-run (Windows, ProcessHost job) | process survives > 2 s | R14 |
| ZCR-T20 | neg | K-10 | P6 | token budget | budget ignored | budget exceeded | run continues | R14 |
| ZCR-T21 | pos | K-09 | P6 | — | — | CI SARIF on fixture PR | schema invalid / unstable fingerprints | R14 |
| ZCR-T22 | neg | K-04 | P5 | no network at idle | background check-in enabled | review installed, idle | outbound connection | R14 |
| ZCR-T23 | pos | K-03 | P6 | — | — | upstream OCR suite (Linux -race, Windows) | red | R14 |
| ZCR-T24 | neg | K-03 | P6 | donor-identifier gate | gate removed | upstream strings in binary/UI | build passes | R14 |
| ZCR-T25 | pos | K-04 | P5 | — | — | line drift by 5 | wrong re-anchor | R14 |
| ZCR-T26 | neg | K-03 | P6 | Z-P7 snapshot allowlist across all engine tools | allowlist reduced to repo-root confinement | decoy secret file in repo, not in manifest | file content in model request log | Astro H-7 |
| ZCR-T27 | neg | K-09 | P6 | cloud route only via mediated proxy + approval | direct endpoint allowed | cloud route configured without proxy | request reaches endpoint | Astro H-7 |
| ZCR-T28 | neg | K-06 | P5 | protected-file rule for fixes | rule removed | fix patch editing verify config / CI file | patch applied | R14 H7 |
| ZCR-T29 | neg | K-08 | P5 | read broker serves only manifest files | broker serves any repo-relative path | reviewer requests untracked `.env` and an absolute path to a decoy secret | decoy bytes in the model request log | A2-08 |
| ZCR-Q01 | qual | K-08 | P5 | — | — | held-out corpus of real fixed defects (≥ 50, not used in prompt design) | detection rate reported; below the route's declared floor → route not qualified | Astro M-4 |
| ZCR-Q02 | qual | K-08 | P5 | — | — | clean-change corpus | false-positive rate reported; above ceiling → not qualified | Astro M-4 |
| ZCR-Q03 | qual | K-08 | P5 | — | — | seeded defects + injected "ignore this file" instructions | suppression rate reported; any suppressed critical defect → not qualified for security review | Astro M-4 |
| ZCR-Q04 | qual | K-11 | P6 | — | — | engine vs delegated on Q01–Q03 corpora | decision record without raw numbers | Astro answer 6 |

## 6. Engineering System (R15 §9)

| Test | Kind | Prerequisites | Phase | Guard | Mutant | Fixture | Observable failure | Source |
|---|---|---|---|---|---|---|---|---|
| ES-AT-01 | neg | V-06, E-01 | P5 | skill hash pins | pin check removed | edited skill file | skill enabled | R15 |
| ES-AT-02 | neg | E-01 | P5 | license gate | gate removed | package without LICENSES file | build passes | R15 |
| ES-AT-03 | neg | E-01 | P5 | identifier scrub gate | gate removed | donor identifier in pack | build passes | R15 |
| ES-AT-04 | pos | E-01 | P5 | — | — | 15 canned prompts | wrong playbook | R15 |
| ES-AT-05 | neg | E-02, E-03 | P5 | repro-before/after rule | rule removed | fix without failing repro | COMPLETED | R15 |
| ES-AT-06 | neg | E-02, V-04 | P5 | INCONCLUSIVE and wrong-surface verdicts never PASS | mapping changed | inconclusive verdict; verdict on the wrong surface | COMPLETED_TRUSTED | R15 |
| ES-AT-07 | neg | V-01, E-02 | P5 | builder-route verdict refused | rule removed | verdict on builder route | accepted | R15 |
| ES-AT-08 | neg | E-02 | P5 | patch-id staleness of verdicts (ship/auto-merge enforcement is ES-AT-17 at E-06) | staleness ignored | rebase changes patch | verdict stays valid | R15 |
| ES-AT-09 | neg | E-03 | P5 | verification partition isolation | default partition used | cookie in user partition | cookie visible | R15 |
| ES-AT-10 | neg | E-03 | P5 | origin policy | policy open | redirect to non-allow-listed origin | request made | R15 |
| ES-AT-11 | pos | E-03 | P5 | — | — | 8-fixture corpus | noisy-green reported PASS | R15 |
| ES-AT-12 | neg | E-02, C-03 | P5 | evidence digest in Core | digest not stored | tampered bundle | verify passes | R15 |
| ES-AT-13 | neg | E-01, L-02 | P5 | plan-path write deny | deny removed | engineering skill writes plan path | file written | R15 |
| ES-AT-14 | pos | E-04 | P5 | — | — | generator on Zain repo | first run fails | R15 |
| ES-AT-15 | neg | E-03, C-25 | P5 | ProcessHost job kill on cancel | job removed | cancel verify run | orphan processes | R15 |
| ES-AT-16 | neg | E-02 | P5 | fail-closed when Core unavailable | fail-open | Core down | verify/ship proceeds | R15 |

## 7. Plan Mode (R16 §8)

| Test | Kind | Prerequisites | Phase | Guard | Mutant | Fixture | Observable failure | Source |
|---|---|---|---|---|---|---|---|---|
| N1 | neg | L-02 | P3 | PLAN_READONLY profile via ACP PEP | profile not applied | ACP `fs/write src/app.ts` | file changed | R16 |
| N2 | neg | L-02 | P3 | S2 decision under plan profile | profile not consulted | Claude Edit on product file | file changed | R16 |
| N3 | neg | L-02 | P3 | canonicalization in fs-gate | string prefix check | `specs/x/../../src/app.ts` | file changed | R16 |
| N4 | neg | L-02 | P3 | fs-gate reparse/symlink rejection | follow links | junction/symlink in plan path → src | file changed | R16 |
| N5 | neg | L-02 | P3 | fs-gate Windows name normalization | normalization removed | case variant, 8.3 name, ADS | write outside plan path | R16 |
| N6 | neg | L-02 | P3 | process.spawn denied in plan profile | spawn allowed | shell / npm install | process starts | R16 |
| N7 | neg | L-02 | P3 | git effects denied in plan profile | allowed | commit/push/branch/PR | ref changes | R16 |
| N8 | neg | L-02 | P3 | MCP non-read-only tools denied | allowed | write-capable MCP tool | tool runs | R16 |
| N9 | neg | L-03 | P3 | turn-end out-of-path diff → INVALIDATED | diff check removed | simulated UNMEDIATED change | plan approvable | R16 |
| N10 | neg | L-03 | P3 | PTY CLI agent refused in plan mode | refusal removed | select CLI agent | plan run starts | R16 |
| N11 | neg | L-05 | P4 | lock hash check | check removed | artifact changed after lock | mission starts | R16 |
| N12 | neg | L-05 | P4 | assertion required | assertion skipped | approve without/replayed assertion | mission starts | R16 |
| N13 | neg | L-06 | P5 | skill pin | pin removed | modified grilling skill | skill enabled | R16 |
| N14 | neg | L-09 | P5 | critic route ≠ griller route | check removed | same route | critic runs | R16 |
| N15 | neg | L-02 | P3 | only Approve effect writes lock | direct write allowed | write plan.lock.json | file written | R16 |
| N16 | neg | L-02 | P3 | path scope excludes AGENTS/ADR | scope widened | edit AGENTS.md | file changed | R16 |
| D1 | pos | L-02 | P3 | — | — | write spec.md under plan path | no receipt | R16 |
| D2 | pos | L-04 | P4 | — | — | Brain index after update | content stored as authority | R16 |
| D3 | pos | L-04 | P4 | — | — | lock then supersede | v1 mutated | R16 |
| D4 | neg | L-06 | P5 | notice gate | gate removed | NOTICE removed | build passes | R16 |
| D5 | pos | L-06 | P5 | — | — | verbatim hash check | mismatch | R16 |
| D6 | neg | L-07 | P5 | DAG schema + cycle check | check removed | cyclic tasks.dag.json | readiness passes | R16 |
| E1 | pos | L-08 | P5 | — | — | grilling round | provenance missing | R16 |
| E2 | pos | L-08 | P5 | — | — | investigation sub-task | unrelated questions blocked | R16 |
| E3 | pos | L-05, L-07 | P5 | — | — | approve plan → mission | first task not visible | R16 |
| E4 | pos | L-08 | P5 | — | — | defer question | file absent | R16 |
| E5 | pos | L-09 | P5 | — | — | critic finding resolution | gate flips early | R16 |

## 8. Browser (R17 §11 + 19 §1)

| Test | Kind | Prerequisites | Phase | Guard | Mutant | Fixture | Observable failure | Source |
|---|---|---|---|---|---|---|---|---|
| BRW-G01 | neg | Y-00 | P2 | grep/import gate for cookie-store readers | gate removed | BrowserImport code restored | build passes | R17 |
| BRW-P01 | neg | Y-01, C-12 | P3 | agent browser tools disabled through R1 | tools re-enabled for agents | agent calls preview_navigate/preview_evaluate/preview_act | call executes | A2-11 |
| BRW-P02 | neg | Y-01 | P3 | hard-block floor in Skip | Skip overrides | Skip + payment class | allowed | R17 |
| BRW-AT-01 | neg | Y-04 | P5 | L3 card-field detector | detector off | cc-number fill | input reaches guest | R17 M1 |
| BRW-AT-02 | neg | Y-03 | P5 | redirect hold before request | hold removed | 302 chain to checkout | fixture server logs a hit | R17 M2 |
| BRW-AT-03 | neg | Y-04 | P5 | Skip never overrides BLOCKED | Skip overrides | Create account in Skip | allowed | R17 M3 |
| BRW-AT-04 | neg | Y-00 | P2 | partition isolation | shared partition | cookie set in Preview | readable in Agent lane | R17 M4 |
| BRW-AT-05 | neg | Y-06 | P5 | redact before hash | hash then redact | auth header + cookie | values in HAR | R17 M5 |
| BRW-AT-06 | neg | Y-08 | P5 | classifier in Playwright backend | backend bypass | headless repeat of 01–03 | different outcome | R17 M6 |
| BRW-AT-07 | neg | Y-04 | P5 | executable quarantine | quarantine off | setup.exe, zip with .ps1 | file released | R17 M7 |
| BRW-AT-08 | neg | Y-04 | P5 | credential-shaped text block | pattern set emptied | fake API key typed | typed | R17 M8 |
| BRW-AT-09 | neg | Y-07 | P5 | mask during takeover | mask disabled | password field + screenshot | value visible | R17 M9 |
| BRW-AT-10 | neg | Y-07 | P5 | rendered-tree reads + provenance envelope | hidden text included | hidden injection | navigation to evil.test | R17 M10 |
| BRW-AT-11 | neg | Y-03 | P5 | scheme/IP filter | filter removed | file:, chrome:, javascript:, 169.254.169.254, Server port | navigation allowed | R17 M11 |
| BRW-AT-12 | neg | Y-03 | P5 | setWindowOpenHandler | allow-all | popup to ungranted origin | popup loads | R17 M12 |
| BRW-AT-13 | neg | Y-08 | P5 | loopback/Origin/Host guard | guard removed | page fetch to CDP endpoint; Host evil.test | 200 | R17 M13 |
| BRW-AT-14 | neg | Y-00 | P2 | relay method allowlist | allowlist open | Storage.getCookies via relay | cookies returned | R17 M14 |
| BRW-AT-15 | neg | Y-04 | P5 | permission handler denies payment/WebAuthn | handler grants | Payment Request / credentials.create | granted | R17 M15 |
| BRW-AT-16 | pos | Y-05 | P5 | — | — | localhost form after approval | receipt incomplete | R17 |
| BRW-AT-17 | neg | Y-05 | P5 | grant cache honours revoke | cache ignores revoke | revoke session grant | next action not prompted | R17 M16 |
| BRW-AT-18 | rec | Y-05 | P5 | — | — | Server killed mid-click and mid-navigate | click not UNKNOWN | R17 (17 §1 classes) |
| BRW-AT-19 | neg | Y-02 | P5 | stale-ref error | nearest-match fallback | stale ref | click on guessed node | R17 M18 |
| BRW-AT-20 | pos | Y-08 | P5 | — | — | external @playwright/test via token | suite fails | R17 |
| BRW-AT-21 | neg | Y-04 | P5 | human release of downloads | auto-release | report.pdf | auto-released | R17 M19 |
| BRW-AT-22 | pos | Y-08 | P5 | — | — | replay run | NEVER step auto-executed | R17 |
| BRW-AT-23 | neg | Y-09 | P9 | tab-group filter | filter removed | tab outside group | action executed | R17 M20 |
| BRW-AT-24 | neg | Y-09 | P9 | Skip/all-sites unavailable in user-session lane | mode allowed | user-session lane settings | Skip selectable | R17 M21 |
| BRW-AT-25 | neg | Y-10 | P5 | session proxy for all request types | proxy rule removed for one partition | fetch, XHR, img, script, beacon to forbidden sink | sink logs ≥ 1 request | Astro H-3 |
| BRW-AT-26 | neg | Y-10 | P5 | proxy covers WebSocket and workers/service workers | proxy bypass for ws | WS + dedicated/service worker fetch to sink | sink logs ≥ 1 request | Astro H-3 |
| BRW-AT-27 | neg | Y-10 | P5 | proxy connects to the validated IP (no re-resolution) | proxy re-resolves at connect | DNS answer switches to 127.0.0.1 after validation (rebinding fixture) | connection to loopback | Astro H-3 |
| BRW-AT-28 | neg | Y-10 | P5 | redirect validation per hop inside proxy | only first hop validated | subresource redirect to private IP | request reaches private IP | Astro H-3 |
| BRW-AT-29 | neg | Y-10 | P5 | WebRTC non-proxied UDP disabled | policy default | STUN/TURN to sink | UDP packet at sink | Astro H-3 |

## 9. DeskGate (R18 §5 + 19 §3)

| Test | Kind | Prerequisites | Phase | Guard | Mutant | Fixture | Observable failure | Source |
|---|---|---|---|---|---|---|---|---|
| DG-N01 | neg | H-02 | P3 | adapter PEP call | PEP call removed | write outside home, no grant | file created | R18 |
| DG-N02 | neg | H-02 | P3 | fs-gate link rejection | path.resolve | link inside root → outside | file outside written | R18 |
| DG-N03 | neg | H-02 | P3 | fs-gate handle-relative write (no re-resolution at use) | path-based write after realpath check | attacker thread swaps junction continuously, 10k writes | any write outside target | Astro H-8 (revised) |
| DG-N04 | neg | H-02 | P3 | CoreBridge fail-closed | health bypass | Core down | gated tool succeeds | R18 |
| DG-N05 | neg | H-01 | P3 | set_config_value refusal | DC config tool restored | `allowedDirectories []` | policy changed | R18 |
| DG-N06 | neg | H-03 | P3 | Core policy for process.spawn | DC blocklist as sole gate | blocklist-bypass strings | decision not from Core | R18 |
| DG-N07 | neg | H-03 | P3 | ownership check | check removed | kill non-Zain PID | killed | R18 |
| DG-N08 | neg | H-03 | P3 | session scope | scope removed | input to other mission's session | accepted | R18 |
| DG-N09 | neg | H-02, C-13 | P3 | assertion verification | session scope accepted as authority | local client with forged/replayed assertion | effect executed | R18 (local variant; remote in DG-P07) |
| DG-N10 | neg | H-01 | P3 | dependency-cruiser + lint import rule | rule deleted | seeded child_process import | build passes | R18 |
| DG-N11 | neg | H-01 | P3 | no telemetry/egress code | `capture()` re-added | full suite with socket hook | outbound connection | R18 |
| DG-N12 | neg | H-06 | P10 | project-home rule | rule disabled | non-home instance proposes effect | executed | R18 |
| DG-N13 | neg | H-02 | P3 | Core policy for writes to sensitive user paths (approval required) | policy entry for `~/.ssh` removed | injected file content asks for `~/.ssh/authorized_keys` write | write executed without approval | R18 (mutant added, Astro M-4) |
| DG-N14 | neg | H-02 | P3 | UNKNOWN on crash mid-write | auto-mark COMPLETED | kill -9 Server mid write_file | COMPLETED recorded | R18 |
| DG-N15 | neg | H-02 | P3 | handle-relative parent for create/move | path-based rename | parent directory swapped between check and rename | entry created outside target | Astro H-8 |
| DG-N16 | neg | H-02 | P3 | op-id input conflict | conflict check removed | same operation key, changed content | second write | Astro M-2 |
| DG-P04 | pos | H-03 | P3 | — | — | REPL start, input, output | missing receipts | R18 |
| DG-P07 | pos | H-06 | P10 | — | — | remote client with passkey | executes without assertion | R18 |
| DG-B1..DG-B9 | bench | H-05 | P3 | — | — | R18 §6 budgets | budget missed (recorded) | R18 |
| FSG-01..FSG-04 | neg | H-08 | P3 | fs-gate (Windows handle-relative + reparse rejection; Linux openat2; macOS O_NOFOLLOW walk) | path-based implementation | (01) write, (02) create, (03) rename, (04) delete under concurrent link/junction swaps | any operation outside validated target | 19 §3 |

## 10. Claude parity, Design, Design Mode (03F §2, R03B)

| Test | Kind | Prerequisites | Phase | Guard | Mutant | Fixture | Observable failure | Source |
|---|---|---|---|---|---|---|---|---|
| V1-01 | pos | F-16 | P2 | — | — | 03F V1-01 | as 03F | 03F |
| V1-02 | neg | C-15 | P3 | Core-compiled permission modes | UI-only modes | "git push: Needs approval" in Skip | push without prompt | 03F |
| V1-03 | neg | M-06 | P4 | per-project Brain isolation | isolation removed | query from project B | A's entry injected | 03F |
| V1-04 | neg | M-06 | P4 | incognito write block | block removed | incognito thread | Brain write | 03F |
| V1-05 | neg | M-02 | P4 | missed-run policy + dedupe key | dedupe removed | laptop off at schedule; duplicate fire | two fires | 03F (ADAPTATION, see 03F §2b) |
| V1-06 | pos | F-16 | P2 | — | — | two worktree threads | file interference | 03F |
| V1-07 | neg | V-04 | P5 | merge ≠ completion | rule removed | merged PR | mission completed | 03F |
| V1-08 | neg | V-06 | P5 | skill grant check | check removed | skill requests broader tools | tools granted | 03F |
| V1-09 | neg | V-05 | P5 | blocked_on_auth on revoked token | token cached | revoked token | effect executes | 03F |
| V1-10 | neg | V-07 | P5 | explicit trust for unknown MCPB | auto-trust | unsigned extension | installed | 03F |
| V1-11 | pos | W-01 | P9 | — | — | one-pager → PDF | export fails | 03F |
| V1-12 | pos | D-08 | P7 | — | — | AT-01..AT-15 | any fails | 03F |
| V1-13 | neg | W-03 | P9 | domain policy | policy open | fetch to non-allowed domain | fetched | 03F |
| V1-14 | neg | Y-08 | P5 | hard blocks | blocks off | localhost form; payment page | payment action executed | 03F |
| V1-15 | neg | W-05 | P9 | per-session grant | grant skipped | input injection | injected | 03F |
| V1-16 | neg | R-03 | P10 | passkey pairing | guest link trusted | guest link approval | approved | 03F |
| V1-17 | pos | C-09 | P3 | — | — | CC-T01..T05 | any fails | 03F |
| V1-18 | pos | C-03 | P3 | — | — | ledger audit export | JSONL invalid | 03F |
| AT-01 | pos | D-01 | P7 | — | — | R03B AT-01 | as R03B | R03B |
| AT-02 | pos | D-06 | P7 | — | — | R03B AT-02 | as R03B | R03B |
| AT-03 | pos | D-01 | P7 | — | — | R03B AT-03 | as R03B | R03B |
| AT-04 | pos | D-03 | P7 | — | — | R03B AT-04 | as R03B | R03B |
| AT-05 | pos | D-04 | P7 | — | — | R03B AT-05 | as R03B | R03B |
| AT-06 | neg | D-05 | P7 | target-set confinement of proposals | confinement removed | send-to-agent on a button | file outside set modified | R03B |
| AT-07 | neg | D-05 | P7 | stale-write refusal (hash) | hash check removed | concurrent IDE edit | apply overwrites | R03B |
| AT-08 | pos | D-06 | P7 | — | — | R03B AT-08 | as R03B | R03B |
| AT-09 | pos | D-06 | P7 | — | — | R03B AT-09 | as R03B | R03B |
| AT-10 | pos | D-07 | P7 | — | — | R03B AT-10 | as R03B | R03B |
| AT-11 | pos | D-01 | P7 | — | — | R03B AT-11 | as R03B | R03B |
| AT-12 | pos | D-06 | P7 | — | — | R03B AT-12 | as R03B | R03B |
| AT-13 | pos | D-04 | P7 | — | — | R03B AT-13 | as R03B | R03B |
| AT-14 | neg | D-05 | P7 | role permissions | role check removed | comment role sends to agent | sent | R03B |
| AT-15 | pos | D-05 | P7 | — | — | R03B AT-15 | as R03B | R03B |
| AT-20 | neg | D-02 | P7 | CSP + sandbox | sandbox removed | preview reads parent cookies | read succeeds | R03B |
| DM-01 | pos | I-05 | P6 | — | — | Design Mode capture on fixture page | payload lacks DOM path/styles/crop | R12 D2 |
| DM-02 | neg | I-05 | P6 | capture confined to Preview lane | capture in agent lane | capture request from agent lane | payload returned | R12 D2 |
| DM-03 | pos | I-05 | P6 | — | — | capture → composer attachment | attachment missing | R12 D2 |

## 11. Additional registered tests (coverage of previously free-text-only requirements)

| Test | Kind | Prerequisites | Phase | Guard | Mutant | Fixture | Observable failure | Source |
|---|---|---|---|---|---|---|---|---|
| CI-01 | pos | A-01 | P−1′ | — | — | unchanged re-run of main integrity workflow | run not green | GOV-01 |
| SRC-01 | neg | F-01 | P2 | KEEP-set manifest hash check | hash check skipped | one extra or modified upstream file | import accepted | GOV-05 |
| ID-01 | neg | N-02 | P2-N | donor/legacy identifier gate | gate removed | `t3code`, `T3CODE_`, `orca`, `wepld` identifier outside NOTICE/history | build passes | GOV-11 |
| ID-02 | neg | N-03 | P2-N | Zain-LLM identifier gate | gate removed | `ZAINLLM_` / Zain-LLM package name in Zain | build passes | GOV-12 |
| EGR-01 | neg | F-05 | P2 | telemetry removal + idle egress capture | PostHog init restored | app idle 10 min with socket capture | outbound connection | PR-22 |
| EDIT-01 | pos | F-17 | P2 | — | — | open, edit, save 5 MB file | > 1 s or content mismatch | PR-10 |
| INBOX-01 | neg | C-14 | P3 | outcomes rendered only from Core records | renderer-local outcome state | fabricated outcome event on WebSocket | outcome displayed | PR-23 |
| B14 | bench | M-03 | P4 | — | — | 100k Brain entries | query p95 > 50 ms | NF-07 |
| B7 | bench | I-08 | P6 | — | — | 09 §3 B7 protocol | not published with raw data | NF-09 |
| B11 | bench | I-08 | P6 | — | — | 09 §3 B11 protocol | unauthorized mediated effect > 0 | NF-09 |
| DBG-01 | neg | I-04 | P6 | debug launch is a Core-gated process effect | launch bypasses ProcessHost | debug launch without grant | debuggee starts | PR-11 |
| DBG-02 | pos | I-04 | P6 | — | — | breakpoints/step/variables in 4 languages | any fails | PR-11 |
| SBX-01 | neg | S-06 | P8 | debug profile grants ptrace/process_vm only to the debuggee | profile applied to agent process | agent process attempts ptrace of a sibling | attach succeeds | R13 F4 |
| RMT-01 | neg | R-04 | P10 | scoped remote sessions (session scope never authorizes effects) | session scope treated as grant | LAN client with valid session, no assertion, requests effect | effect executes | 07 §6 |
| ES-AT-17 | neg | E-06 | P6 | merge requires Core grant; merge ≠ completion | grant check removed | auto-merge of a green PR without grant | merge executed | R15 |

## 13. Revision 4 additions (Astro round 2)

| Test | Kind | Prerequisites | Phase | Guard | Mutant | Fixture | Observable failure | Source |
|---|---|---|---|---|---|---|---|---|
| LIC-02 | neg | Q-00 | PF | shipped-closure license listing (every packaged package has license or explicit decision) | listing check removed | lockfile entry without license metadata in the packaged closure | record accepted | A2-02 |
| SRC-02 | pos | Q-01 | PF | — | — | branch tree vs upstream pin | tree hash differs | 24 §3 |
| FWB-02 | neg | Q-02 | PF | coexistence overlay (protocol, single-instance lock, server port discovery, data home) | overlay reverted | upstream T3 installed and running | shared state, lock, protocol or connection to the T3 server | A2-04 |
| FWB-03 | neg | Q-02 | PF | CLI/child environment isolation | `T3CODE_HOME` passthrough restored | ambient `T3CODE_HOME` pointing at a T3 home; spawn CLI and children | any read/write in the T3 home | A2-04 |
| FWB-04 | neg | Q-02 | PF | separate Electron profile; legacy dev-profile reuse and Local State migration disabled | migration re-enabled | existing T3 production and development profiles | Zain dev reads or copies T3 profile data | A2-04 |
| EGR-02 | neg | Q-03 | PF | donor integrations disabled at entry points | one entry point re-enabled | startup, 10 min idle, reconnect, manual update action, forced error report, provider activity; socket capture | any request to a donor endpoint | A2-04 |
| EGR-03 | pos | Q-03 | PF | — | — | same capture with one provider turn | provider route blocked (over-blocking) | A2-04 |
| CI-02 | pos | Q-04 | PF | — | — | build DAG run (local or private build repository), cold cache | no installer, or resource/time measurements not recorded | A2-01 |
| PKG-01 | neg | Q-04 | PF | provider-disabled bundling + content inspection (bundle metafile/sourcemap module provenance, unpacked ASAR, nested archives) | provider re-enabled before bundling | build output | any `@anthropic-ai/claude-agent-sdk*` or `@cursor/sdk` module in compiled JS, ASAR or nested archive; or app fails to boot with those providers absent | A2-01 |
| PKG-02 | neg | Q-04 | PF | artifact access control (no public upload; private repository or local only) | public artifact upload step added | workflow definitions and run records | binary or build log with packaged content reachable without repository-collaborator access | A2-02 |
| FWB-01 | pos | Q-05 | PF | — | — | install; launch desktop; terminal command; create worktree; diff review; one real provider turn on the declared route (Codex login or qualified ACP agent) | any step fails → FEASIBILITY_COMPLETE_WITH_FAILURES; no credentials → PARTIAL_SMOKE_NO_CREDENTIALS; only all steps → FIRST_WORKING_BUILD_PASSED | A2-15 |
| CC-T04 | neg | F-06 | P2 | no reads of Claude subscription credentials (same oracle as T7) | rule removed | `~/.claude/.credentials.json` present | file-access audit shows a read by any Zain process | 03C §5 |
| A11Y-04 | pos | C-14 | P3 | — | — | scripted NVDA + keyboard over Inbox, approval and unknown-outcome surfaces | missing name/role/live announcement or pointer needed | A2-06 |
| PEM-CLA-05 | neg | C-09 | P3 | subagent tool calls pass the same PreToolUse hook with inherited context identity | hook skipped for subagents | subagent requests Write outside worktree | write without Core decision | A2-07 |
| PEM-CDX-05 | neg | C-09 | P3 | approval-response normalization (accept, acceptForSession, ApprovedForSession, legacy) | only literal ApprovedForSession blocked | handler fixtures for each response form | a session-scoped allowance reaches Codex | A2-07 |
| PEM-CDX-06 | neg | C-09 | P3 | isolated CODEX_HOME / MCP config per session | ambient config used | user `config.toml` with an extra MCP server and permissive defaults | ambient MCP server or setting active | A2-07 |
| REC-06 | neg | C-26 | P3 | NOT_APPLIED requires temp-object identity still present + target object id = pre-image id (17 §1) | pre-image content hash used instead | A → Zain writes B → other writer restores A → quiesce | NOT_APPLIED reported | A2-09 |
| REC-07 | neg | C-26 | P3 | APPLIED requires operation-unique object identity, not content | content-hash comparison | no-op write (old = new) | APPLIED or NOT_APPLIED inferred from bytes | A2-09 |
| REC-08 | neg | C-26 | P3 | content equivalence recorded separately from execution | equivalence mapped to APPLIED | post-state already present before dispatch | historical APPLIED recorded | A2-09 |
| REC-09 | neg | C-26 | P3 | pending remote merge stays UNKNOWN until terminal evidence (merged with expected head, or head moved so the sha-pinned request cannot succeed) | merged=false mapped to NOT_APPLIED | merge request accepted, read shows merged=false with same head, request completes later | NOT_APPLIED recorded | A2-09 |
| REC-10 | neg | C-26 | P3 | stale-read rejection (read must post-date dispatch and carry provider freshness) | freshness ignored | cached API read older than dispatch | outcome concluded from stale read | A2-09 |
| COV-08 | neg | C-23 | P3 | ACE reported as content equivalence only; execution coverage separate | ACE mapped to provenance | unmediated process writes bytes identical to a receipted write | completion claims the content was produced only by authorized writes | A2-10 |
| COV-09 | neg | C-23, C-05 | P3 | mandatory critical scopes from Core project policy; callers may add, never remove | caller-supplied empty list replaces defaults | mission declares no scopes; shell ran | COMPLETED_TRUSTED | A2-10 |
| APR-08 | neg | C-13 | P3 | level-specific claim templates | single template for all levels | A3 (TOTP) approval | text claims platform authenticator or user presence | A2-13 |
| APR-09 | neg | C-13 | P3 | downgrade needs an assertion at the current level and is shown | silent downgrade | renderer requests switch A1 → A3 | level changed without assertion | A2-13 |
| FSG-05 | neg | H-08 | P3 | fresh-file replacement; link count > 1 rejected for in-place ops | in-place write through handle | allowed path hardlinked to an outside file | outside file modified | A2-12 |
| FSG-06 | neg | H-08 | P3 | ancestors held without FILE_SHARE_DELETE | share mode includes delete | rename a validated parent outside the root during create/rename | entry created outside the root | A2-12 |
| FSG-07 | neg | H-08 | P3 | name normalization/rejection | normalization removed | ADS, CON/NUL/COM1, trailing dot/space, 8.3 alias, case-sensitive directory | operation on an aliased target | A2-12 |
| FSG-08 | neg | H-08 | P3 | final-target identity check before replace | check skipped | target swapped between validation and replace | replace hits another object | A2-12 |
| FSG-09 | neg | H-08 | P3 | no truncation before validation | open with truncate | validation fails after open | target truncated | A2-12 |
| ZCR-T30 | neg | K-08 | P5 | built-in tools disabled for reviewer sessions | Bash/Grep/Read re-enabled | reviewer asks to run grep over the repository | tool executes | A2-08 |
| ZCR-T31 | neg | K-08 | P5 | scrubbed HOME, config dir, history, settingSources empty | ambient HOME passed | decoy CLAUDE.md, history and settings in the real home | decoy bytes in a model request | A2-08 |
| ZCR-T32 | neg | K-08 | P5 | git symlink entries materialized as text, never followed | symlink followed | symlink in the change pointing outside the repo | target bytes in a model request | A2-08 |
| ZCR-T33 | neg | K-08 | P5 | cloud review routes only through the loopback review proxy with per-run approval | direct endpoint allowed | cloud route configured without proxy | request reaches endpoint | A2-08 |
| BRW-AT-30 | neg | Y-10 | P5 | HTTP/2 coalescing policy (per-host tunnels or HTTP/2 off for agent partitions) | coalescing allowed | allowed host and forbidden host sharing a certificate/IP | request to forbidden host over a reused connection | A2-11 |
| BRW-AT-31 | neg | Y-10 | P5 | tunnels torn down on revocation | existing tunnels kept | revoke origin while a connection is open | request succeeds after revocation | A2-11 |
| BRW-AT-32 | neg | Y-10 | P5 | headless Playwright backend launched with the same proxy and bypass rules | headless launched without proxy | BRW-AT-25..29 fixtures on headless | any forbidden sink hit | A2-11 |
| BRW-AT-33 | neg | Y-10 | P5 | proxy failure fails closed | fallback to direct | proxy process killed | request reaches sink directly | A2-11 |
| BRW-AT-34 | neg | Y-10 | P5 | hostile localhost content confined | localhost treated as trusted | localhost page uses fetch, WebSocket, worker, beacon, window.open, redirect to external and to Core/Server/debug ports | any forbidden destination reached | A2-11 |
| BRW-AT-35 | neg | Y-10 | P5 | loopback port authorization (only ProcessHost-owned project ports) | any loopback port allowed | request to an unowned loopback port | connection established | A2-11 |
| GV-21 | pos | G-03 | P0 | — | — | signed tag created with `git tag -s` (SSH, namespace git) by an allowed signer, canonical payload | `git verify-tag` fails or payload rejected | A2-14 |
| GV-22 | neg | G-03 | P0 | verification via `git verify-tag` (namespace git) against base allowed_signers | verify with arbitrary namespace or extracted message | detached SSHSIG in namespace `zain-cosign`; tag signed by non-allowed key | accepted | A2-14 |
| GV-23 | neg | G-03 | P0 | canonical payload (UTF-8, LF, fixed field order, final LF, no extra fields) + replay ledger of used tag object ids | parser tolerant | CRLF payload, reordered/extra field, reused tag object | accepted | A2-14 |
| CLM-01 | neg | X-01 | P5 | claim text generated from passing qualification cells | static claim text | one PEM cell failing | failing cell's operation still claimed | A2-07 |
| CLM-02 | neg | X-01 | P5 | claim template follows active approval level | fixed A1 text | A2 or A3 active | A1 wording shown | A2-13 |

## Suite composition (nested suites; machine-read)

A suite's effective prerequisites include those of every member (A2-06). CC-T05 (Stop gating, V-04/P5) is deliberately not
part of V1-17.

| Suite | Includes |
|---|---|
| V1-17 | CC-T01, CC-T02, CC-T03, CC-T04 |

