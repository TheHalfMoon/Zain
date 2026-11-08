# 11 — Task Contracts

```text
STATUS   = CANDIDATE (planning only; no task is authorized until its entry gates pass and the founder accepts the plan, Z-25)
SOURCES  = registry/zain-task-backlog.csv (210 rows) · registry/zain-dependency-edges.csv (440 edges)
SCOPE    = 34 master-plan tasks (Z-01..Z-34) in full below; 176 V3 tasks by reference
```

## 1. How contracts are split between this plan and V3

The V3 package (`specs/008-wepld-v3-unified-replan/14_TASK_CATALOG.md`) already holds 176 live task contracts. Every
one has an ID, dependencies, file-level sources, acceptance criteria, registered tests, an estimate and a tier, and
its validator `plan_graph.py --check` exits 0 on them. This plan does **not** rewrite those contracts:

- **V3 tasks** (`source = V3` in the backlog) are mirrored into the backlog by `tools/zmp.py sync-v3`. The canonical
  wording stays in 14_TASK_CATALOG.md. `zmp.py check` fails with `E-V3-DRIFT` if the mirror disagrees on milestone,
  phase, dependencies or tier.
- **Master-plan tasks** (`source = ZMP`, IDs `Z-NN`) cover what V3 does not: repository privacy, the reviewer route,
  machine capacity, toolchain alignment, the model gateway, local completion, the local code index, journey tests,
  design language, performance baselines, destructive-operation guards, the validator repair, and three
  data-loss or trust fixes found in this audit. Their full contracts are generated below from the backlog CSV.
- **Gate edges** (`type = gate` in the edges CSV) attach Z prerequisites to V3 tasks without editing V3. For example,
  Z-07 (capacity) must finish before Q-01 (source import).

## 2. Contract rules that apply to every task (V3 and ZMP)

1. **Entry.** All prerequisites and gate edges are DONE, DONE_UNREVIEWED or NOT_NEEDED. The task's spec note exists.
   Its tests are written first and fail for the right reason. A milestone exit gate needs its T2 tasks fully DONE.
2. **Scope.** Implement the smallest complete vertical slice that meets the acceptance criteria. Do not widen scope;
   record any newly found work as a backlog row.
3. **Exit.** Every listed test or gate passes on the real artifact. Negative tests are mutation-controlled: they must
   fail with their guard removed. Measured numbers are recorded. Evidence is linked in `status_evidence`.
4. **Status vocabulary.** `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED` (needs `blockers`), `DONE_UNREVIEWED` (evidence
   exists, independent review pending), `DONE` (evidence plus independent review through a GATE-REV-01 route),
   `NOT_NEEDED`, `SUPERSEDED`. `zmp.py check` rejects DONE without evidence and DONE before prerequisites.
5. **Tier.** T2 tasks (security, supply chain, effects, authority) need an independent reviewer that is not the
   builder's model family or is the founder. If GATE-REV-01 is not met, a T2 task can reach at most `DONE_UNREVIEWED`.
6. **No self-certification.** An agent's own narrative, its own test run or another instance of the same model is not
   independent review (16-OPUS-IMPLEMENTATION-HANDOFF.md §5).

## 3. The R0a work order (V3 Q-00..Q-06) — entry conditions added by this plan

The R0a contracts are fully specified in V3 (14 §PF, `OPUS_R0A_BUILD_EXECUTION_2026-11-02.md`,
`R0A_FEASIBILITY_READINESS.md`). This plan adds verified preconditions that V3 could not know:

| V3 task | Added gate edge(s) | Why (verified 2026-11-08) |
|---|---|---|
| Q-00 admission | Z-25 | Pin (DEC-04), provider route (DEC-08) and build volume (DEC-12) must be decided first (decided 2026-11-08) |
| Q-01 import | Z-06, Z-07, Z-08 | Reviewer route authorized (DEC-01) but not yet qualified (A7); build volume D: has 15 GB free; Node 24.19.0 / pnpm 9.12.0 vs pins. The repository is public by founder choice and pushing is not gated (ADR-Z04 withdrawn) |
| Q-04 build | Z-07 | Cold build must start above the measured capacity threshold |
| Q-05 smoke | Z-09, Z-10 | Isolated account (A5) and consented provider route (A6) are founder actions |

**Timeboxes.** Q-06 and F-21 (MEASURE) get 2 pw each; when exhausted the founder decides (10 §3).

**Re-pin (DEC-04, decided 2026-11-08: re-pin to the v0.1.7 tag).** Q-00 pins `pingdotgg/t3code@36d4d711`. Upstream released v0.1.7 (`a9e709f15f82`
HEAD on 2026-11-07, tag 2026-11-04) with Windows installers built in CI. Q-00 records the re-pin to the release tag, with the R11 manifest deltas for changed files, a re-run of the R02 §10 seam inventory and a
re-check of the V3 18 file:line citations at the new pin.

**Amending V3 contracts.** Z-24 and Z-26 change V3 text. Amendments go in a separate commit that edits only the
named V3 rows, carries the founder's approval, and passes `plan_graph.py --check` and `zmp.py check`. The DEC-09
freeze applies to governance policy successors (v73+), not to planning documents.

## 4. Master-plan task contracts (generated)

<!-- GENERATED:BEGIN zmp-contracts (tools/zmp.py render; edit registry/zain-task-backlog.csv) -->

### Z-01 — Restore PRIVATE visibility of TheHalfMoon/Zain and decide the public legacy repo wepld/wepld

| Field | Contract |
|---|---|
| Milestone / subsystem / owner | M0 · Program/Governance · FOUNDER |
| Why | Founder rule: Zain stays private. Verified 2026-11-08: TheHalfMoon/Zain and wepld/wepld are PUBLIC; every push publishes. |
| Dependencies (must finish first) | — |
| Gates it opens for V3 tasks | — |
| Deliverables | Visibility changed by the founder; decision for wepld/wepld (make private, archive or keep); consequences recorded in 17-MASTER-PLAN-STATUS.md |
| Acceptance criteria | gh repo view TheHalfMoon/Zain --json visibility returns PRIVATE; Actions/Packages spending limit confirmed 0 USD; loss of free branch protection and rulesets on private repositories and the limited included Actions compute allowance (docs.github.com, checked 2026-11-08) recorded with the G-07 consequence (DEC-03) |
| Required tests / gates | GATE-PRIV-01 |
| Evidence for completion | Command output with timestamp pasted into 17-MASTER-PLAN-STATUS.md |
| Security implications | Stops future disclosure. Does not undo past exposure (Z-03). |
| Estimate · complexity · risk · tier · cost | 0.05 pw · S · CRITICAL · T0 · FREE |
| Blockers | — |
| Parallel group | M0-founder |
| Status | NOT_NEEDED — Founder reversed DEC-02 on 2026-11-08: both repositories public again (Zain 01:31:32Z, wepld/wepld 01:31:33Z, anonymous API 200, 0 forks). Earlier: Zain private 00:37:46Z-01:31:32Z, wepld/wepld 01:22:38Z-01:31:33Z. |
| Reference | 01-REPOSITORY-AUDIT.md §2 |

### Z-02 — Close third-party automatic AI review and app egress on the repository (EGRESS_PREFLIGHT E1–E5)

| Field | Contract |
|---|---|
| Milestone / subsystem / owner | M0 · Program/Governance · AGENT+FOUNDER |
| Why | cubic.yaml is on main; CodeRabbit, Qodo, Cursor Bugbot, Devin, Sentry, Vercel, Claude app, Graphite and Greptile held or hold access. An automatic AI reviewer sends private code to a hosted model the founder has not authorized for this product. |
| Dependencies (must finish first) | — |
| Gates it opens for V3 tasks | — |
| Deliverables | Read-only inventory of installed GitHub Apps with repository access (agent); removal or documented automatic-review OFF per app (founder); disposition of cubic.yaml |
| Acceptance criteria | Every installed app is uninstalled from the repository or has automatic review/summary documented OFF; after Z-01, a push to a scratch branch produces no third-party AI check suite or comment |
| Required tests / gates | GATE-PRIV-02 |
| Evidence for completion | Installation list (gh api /user/installations/<id>/repositories or settings screenshot) and the scratch-push check result |
| Security implications | Removes an unauthorized hosted-model data path. |
| Estimate · complexity · risk · tier · cost | 0.1–0.25 pw · S · HIGH · T0 · FREE |
| Blockers | Founder-only for app settings |
| Parallel group | M0-founder |
| Status | NOT_STARTED |
| Reference | specs/008 EGRESS_PREFLIGHT_2026-10-27.md §4 |

### Z-03 — Public-exposure assessment of TheHalfMoon/Zain and wepld/wepld history

| Field | Contract |
|---|---|
| Milestone / subsystem / owner | M0 · Security system · AGENT |
| Why | Both repositories are public; the V3 ledger records local-machine details in commits c376917 and ef19a3f; 353 remote branches exist. |
| Dependencies (must finish first) | — |
| Gates it opens for V3 tasks | — |
| Deliverables | Report: secret-scan results over all refs (gitleaks or trufflehog if available locally, else documented regex set), classes of sensitive data found (paths, user names, machine names, tokens), commit references, and a recommendation per class (accept, rotate credential, or founder-approved history rewrite); inventory of public forks, refs/pull/*, Actions logs and artifacts, releases and wiki (forks survive a visibility change) |
| Acceptance criteria | Scan covers all refs of both repositories; every hit has a disposition; any live credential is listed for founder rotation; no history is rewritten by the agent |
| Required tests / gates | GATE-PRIV-03 |
| Evidence for completion | Scanner version, command, ref count, hit table |
| Security implications | A history rewrite or branch deletion is destructive and founder-only. |
| Estimate · complexity · risk · tier · cost | 0.25–0.5 pw · S · HIGH · T0 · FREE |
| Blockers | — |
| Parallel group | M0-agent |
| Status | DONE_UNREVIEWED — 18-EXPOSURE-ASSESSMENT.md (2026-11-08): all refs of both repos, PR/issue text, 4,186 comments, both artifacts and 20 sampled logs scanned; 0 live credentials; personal data P1-P3 dispositioned; DEC-16 decided 2026-11-08 (accept, noreply identity); P2 resolved as founder-owned accounts; P7 profile email open |
| Reference | 01-REPOSITORY-AUDIT.md §2 |

### Z-04 — Branch and pull-request reconciliation

| Field | Contract |
|---|---|
| Milestone / subsystem / owner | M0 · Program/Governance · AGENT+FOUNDER |
| Why | 12 open PRs (none is a merge candidate under V3) and three unmerged planning branches (v3-unified-replan, r0a-opus-start, this branch) mislead agents about the live state. |
| Dependencies (must finish first) | — |
| Gates it opens for V3 tasks | — |
| Deliverables | Disposition table (01-REPOSITORY-AUDIT.md §6) applied after founder approval: close #1 #73 #81 #88 #136 #159 #162 #164 #347; supersede #342 #343 #346 after salvage notes; decide merge path for the planning branches |
| Acceptance criteria | Every open PR and every non-main branch updated after 2026-09-01 has a recorded disposition; nothing is closed or deleted without founder approval; salvage notes exist for #342 (benchmark preregistration) and #73 (JetBrains research) |
| Required tests / gates | GATE-M0-EXIT |
| Evidence for completion | PR state list after changes (gh pr list --state all) and the approval record |
| Security implications | Closing PR #136 does not remove its public branch; branch deletion is founder-only. |
| Estimate · complexity · risk · tier · cost | 0.25 pw · S · MEDIUM · T0 · FREE |
| Blockers | — |
| Parallel group | M0-agent |
| Status | NOT_STARTED |
| Reference | 01-REPOSITORY-AUDIT.md §6 |

### Z-05 — Master-plan registries, cross-artifact validator and mutation suite

| Field | Contract |
|---|---|
| Milestone / subsystem / owner | M0 · Program/Governance · AGENT |
| Why | The prompt requires machine-readable, internally consistent artifacts with automated relationship checks; the V3 validator is known to fail open (A3-01). |
| Dependencies (must finish first) | — |
| Gates it opens for V3 tasks | — |
| Deliverables | registry/*.csv (7 files), tools/zmp.py (check, sync-v3), tools/test_zmp_mutations.py |
| Acceptance criteria | zmp.py check exits 0; every mutation case is rejected with its expected error code; V3 plan_graph.py --check still exits 0 |
| Required tests / gates | GATE-PLAN-01, GATE-PLAN-02, GATE-PLAN-03 |
| Evidence for completion | Command outputs in 15-VALIDATION-EVIDENCE.md |
| Security implications | None (documentation tooling). |
| Estimate · complexity · risk · tier · cost | 0.5 pw · M · LOW · T0 · FREE |
| Blockers | — |
| Parallel group | M0-agent |
| Status | DONE_UNREVIEWED — 15-VALIDATION-EVIDENCE.md §1–§2 (2026-11-08); independent non-Claude review pending (Z-06) |
| Reference | 15-VALIDATION-EVIDENCE.md |

### Z-06 — Authorize and qualify an independent reviewer route for private Zain content (A7; the hosted-provider review problem)

| Field | Contract |
|---|---|
| Milestone / subsystem / owner | M0 · Review service · AGENT+FOUNDER |
| Why | The builder is a Claude model; own validation is not independent review. Local candidates have limits: the Alibaba OCR CLI is configured with provider 'chatgpt' (hosted), OpenCode is configured through a third-party relay, d1-local (600M) is advisory only and once rated an auth bypass low-risk. None is authorized in writing for private Zain code. |
| Dependencies (must finish first) | — |
| Gates it opens for V3 tasks | Q-01 (A7 independent reviewer before Q-01 (A3–A7 must be evidenced)) |
| Deliverables | Decision record (DEC-01) listing allowed reviewer routes per data class (public, private-plan, private-code, secrets-never) signed by the founder; one dry-run review of this master plan through an authorized route, findings in the Code Review schema |
| Acceptance criteria | At least one route is authorized in writing. For T2 work the founder (qualified reviewer) signs off, with security review per V3 ADR-011; model routes are advisory for T2 and may substitute only for T0/T1 when they are a different model family from both the builder and the provider under test and are authorized for private code; if the founder declines every route, REVIEW_BLOCKED is recorded and R0a stops at Q-00 |
| Required tests / gates | GATE-REV-01 |
| Evidence for completion | Decision record + findings file + route configuration with credentials redacted |
| Security implications | Prevents private code reaching unauthorized hosted models; defines the fallback. |
| Estimate · complexity · risk · tier · cost | 0.25 pw · S · HIGH · T0 · FREE |
| Blockers | Founder sets up OCR on the ChatGPT login for the dry-run review (DEC-01 decided 2026-11-08) |
| Parallel group | M0-founder |
| Status | NOT_STARTED |
| Reference | 06-MODELS-CONTEXT-AND-REVIEW.md §5 |

### Z-18 — Deletion and disk-incident close-out (read-only forensics)

| Field | Contract |
|---|---|
| Milestone / subsystem / owner | M0 · Security system · AGENT |
| Why | The V3 ledger records a disk filled by donor clones that were then deleted (2026-10-28); the local folder OneDrive/Desktop/wepld shows every tracked file deleted in its working tree; the reported usn-journal.csv evidence was not found in any TheHalfMoon repository. |
| Dependencies (must finish first) | — |
| Gates it opens for V3 tasks | — |
| Deliverables | Incident note: timeline from available evidence, what is recoverable (git objects vs working tree), whether OneDrive sync propagated deletions, root-cause hypotheses, and requirements handed to Z-19 |
| Acceptance criteria | Every statement is backed by a command output; no file is restored, moved or deleted without founder approval; open questions listed for the founder (location of usn-journal.csv) |
| Required tests / gates | GATE-M0-EXIT |
| Evidence for completion | Command transcript excerpts in the note |
| Security implications | Read-only; any restore is founder-approved. |
| Estimate · complexity · risk · tier · cost | 0.25 pw · S · MEDIUM · T0 · FREE |
| Blockers | — |
| Parallel group | M0-agent |
| Status | NOT_STARTED |
| Reference | 07-SECURITY-AND-CONTAINMENT.md §6 |

### Z-25 — Founder decision record for this master plan (scope, milestones, open decisions)

| Field | Contract |
|---|---|
| Milestone / subsystem / owner | M0 · Program/Governance · FOUNDER |
| Why | The plan proposes an initial-release scope, milestone order and decisions DEC-01..DEC-12; nothing is authoritative until the founder decides. |
| Dependencies (must finish first) | — |
| Gates it opens for V3 tasks | Q-00 (Pin (DEC-04), route (DEC-08) and build volume (DEC-12) decided before the admission record) |
| Deliverables | Signed decision entries for DEC-01..DEC-12 in 13-RISKS-AND-OPEN-DECISIONS.md; confirmation of which historical claims (E4–E7, FD-4, 70458ae, usn-journal) belong to other projects |
| Acceptance criteria | DEC-01, DEC-02, DEC-04, DEC-07, DEC-08 and DEC-12 have a decision, date and decider before Q-00 starts; the remaining DEC rows are decided before the milestone they unblock |
| Required tests / gates | GATE-M0-EXIT |
| Evidence for completion | Updated decision table |
| Security implications | None. |
| Estimate · complexity · risk · tier · cost | 0.1 pw · S · HIGH · T0 · FREE |
| Blockers | Founder decisions |
| Parallel group | M0-founder |
| Status | DONE_UNREVIEWED — 13 §2 (2026-11-08): the founder answered DEC-01..DEC-16 in chat, all as recommended; recorded by the agent; DEC-10 confirmed, usn-journal.csv location unknown; no separate signature beyond the founder's chat answers |
| Reference | 13-RISKS-AND-OPEN-DECISIONS.md |

### Z-07 — Build-volume capacity: measure need, founder frees space (no agent deletion)

| Field | Contract |
|---|---|
| Milestone / subsystem / owner | R0a · Packaging · AGENT+FOUNDER |
| Why | Verified 2026-11-08: C: 3.4 GB free (99% used), D: 20 GB free (8 GB earlier the same day), RAM 15.7 GB with about 0.2 GB free at sample. A cold T3 build plus pnpm store, Electron cache, native modules and NSIS, and later the Rust Core target, will not fit on C:. |
| Dependencies (must finish first) | — |
| Gates it opens for V3 tasks | Q-01 (Capacity preflight before source import); Q-04 (Capacity preflight before the cold build) |
| Deliverables | Read-only space report of the largest directories on D: for the founder; chosen build volume and directory; provisional threshold recorded in the Q-00 record and replaced by the measured Q-04 peak |
| Acceptance criteria | Chosen build volume has at least max(30 GB, 2 × measured Q-04 peak) free at Q-01 and Q-04 start, and at least 6 GB free RAM at build start; otherwise Q-00 records RESOURCE_BLOCKED |
| Required tests / gates | GATE-RES-01 |
| Evidence for completion | df / Get-PSDrive output and Get-CimInstance Win32_OperatingSystem free memory at each start |
| Security implications | Deletion of founder files is destructive and founder-only. |
| Estimate · complexity · risk · tier · cost | 0.1 pw · S · HIGH · T0 · FREE |
| Blockers | Founder must free space |
| Parallel group | R0a-prereq |
| Status | NOT_STARTED |
| Reference | 09-PERFORMANCE-PLAN.md §1 |

### Z-08 — Align the build toolchain with the Q-00 pins without system-wide changes

| Field | Contract |
|---|---|
| Milestone / subsystem / owner | R0a · Packaging · AGENT |
| Why | Verified: Node 24.19.0 and pnpm 9.12.0 installed; T3 pins Node 26.12.1 and pnpm 12.14.0 (root package.json at a9e709f1). Rust 1.97.1 MSVC, Visual Studio Build Tools 2022 and Windows SDK 10.0.26100 are present. |
| Dependencies (must finish first) | Z-07 |
| Gates it opens for V3 tasks | Q-01 (Toolchain pins before source import) |
| Deliverables | User-local Node 26.12.1 and pnpm 12.14.0 used only inside the build shell, downloaded from the official distribution with SHA-256 verification after founder approval of the download; toolchain manifest in the Q-00 record |
| Acceptance criteria | Inside the build shell node --version is v26.12.1 and pnpm --version is 12.14.0; the global Node is unchanged; hashes match the published SHASUMS |
| Required tests / gates | GATE-TOOL-01 |
| Evidence for completion | Version outputs, hash comparison, install path |
| Security implications | Downloads require explicit founder approval (file, source, size). |
| Estimate · complexity · risk · tier · cost | 0.1 pw · S · MEDIUM · T1 · FREE |
| Blockers | — |
| Parallel group | R0a-prereq |
| Status | NOT_STARTED |
| Reference | specs/008 OPUS_R0A_BUILD_EXECUTION_2026-11-02.md §B1 |

### Z-09 — Create the isolated local Windows test account for R0a smoke (A5)

| Field | Contract |
|---|---|
| Milestone / subsystem / owner | R0a · Security system · FOUNDER |
| Why | Windows 11 Home has no Windows Sandbox or Hyper-V; the R0a packet requires a separate local account with no real T3 state or tokens. |
| Dependencies (must finish first) | — |
| Gates it opens for V3 tasks | Q-05 (Isolated account before smoke) |
| Deliverables | Standard (non-admin) local account with its own profile; synthetic T3 coexistence fixture prepared by the agent |
| Acceptance criteria | Account exists and is non-admin; its profile holds no T3 or Claude state; the only provider state is the route declared in Z-10 |
| Required tests / gates | GATE-ISO-01 |
| Evidence for completion | whoami /groups from the account; profile directory listing |
| Security implications | Account creation is an OS security setting; founder-only. |
| Estimate · complexity · risk · tier · cost | 0.05 pw · S · MEDIUM · T0 · FREE |
| Blockers | Founder-only: OS account creation |
| Parallel group | R0a-prereq |
| Status | NOT_STARTED |
| Reference | specs/008 OPUS packet §A5 |

### Z-10 — Choose and verify the consented provider route for the R0a real-provider turn (A6)

| Field | Contract |
|---|---|
| Milestone / subsystem / owner | R0a · Model gateway · AGENT+FOUNDER |
| Why | FWB-01 needs one real provider turn; subscription credentials may only be used through the provider's own login path (no extraction or relay). |
| Dependencies (must finish first) | — |
| Gates it opens for V3 tasks | Q-05 (Provider route before the real-provider turn) |
| Deliverables | Route named in the Q-00 record (V3 default: the founder's Codex login through the official CLI); credential storage location recorded; provider CLI installed in the isolated account with founder approval of the download; how the login is made available to a per-session CODEX_HOME with Zain-only MCP config (V3 18) is specified and tested without copying tokens into Zain files |
| Acceptance criteria | Credential stays in the provider CLI or OS keyring; no token is copied into Zain config or logs; if no route is available Q-05 records PROVIDER_BLOCKED or PARTIAL_SMOKE_NO_CREDENTIALS |
| Required tests / gates | GATE-R0A-EXIT |
| Evidence for completion | Q-00 record section and a redacted log of one successful turn |
| Security implications | Credential handling; founder consent required. |
| Estimate · complexity · risk · tier · cost | 0.05 pw · S · MEDIUM · T1 · FREE |
| Blockers | Founder chooses the route |
| Parallel group | R0a-prereq |
| Status | NOT_STARTED |
| Reference | specs/008 OPUS packet §A6 |

### Z-29 — One-day hands-on trial of the upstream T3 release in the isolated account before forking

| Field | Contract |
|---|---|
| Milestone / subsystem / owner | R0a · Testing engine · AGENT+FOUNDER |
| Why | No one has used T3 on this machine; a day with the official signed release tests whether the workbench is worth forking, more cheaply than any spike. |
| Dependencies (must finish first) | Z-09 |
| Gates it opens for V3 tasks | B-07 (Hands-on trial informs the G2 GO / reopen decision) |
| Deliverables | Trial log: install the upstream release (download approved by the founder), run journeys J02, J04, J05, J06, J12 on a non-private sample project with OS-firewall egress logging; list of defects, Windows issues and missing features |
| Acceptance criteria | Trial log covers the five journeys with pass/fail and screenshots; observed egress endpoints listed; go / adjust / reconsider recommendation recorded for B-07 |
| Required tests / gates | GATE-J04 |
| Evidence for completion | Trial log, egress list, installer SHA-256 and signature check |
| Security implications | Uses only a sample project and synthetic credentials; no private Zain code. |
| Estimate · complexity · risk · tier · cost | 0.2 pw · S · LOW · T1 · FREE |
| Blockers | Founder approves the download |
| Parallel group | R0a-prereq |
| Status | NOT_STARTED |
| Reference | 14-INDEPENDENT-REVIEWS.md (zoom-out recommendation) |

### Z-13 — Retain and test open-in-external-editor as the editing path until Monaco/LSP land

| Field | Contract |
|---|---|
| Milestone / subsystem / owner | R0b · Application shell · AGENT |
| Why | Monaco arrives in R1 (F-17) and LSP/DAP in R3 (I-03, I-04); a daily driver needs the founder's existing editor in the loop now. |
| Dependencies (must finish first) | Q-05 |
| Gates it opens for V3 tasks | — |
| Deliverables | Verify the donor's open-in-editor capability (COPY) or add a minimal launcher (REIMPLEMENT); file:line links from diffs, chat and terminal output; external-edit detection refreshes the diff |
| Acceptance criteria | From a diff line, a chat file reference and a terminal path, the configured editor opens at file:line; the launcher resolves the editor to its .exe (never a .cmd shim through cmd.exe) or applies cmd-specific escaping; negative tests with &, %, ^ and quote characters in file names run no extra command; an external edit appears in the workbench diff within 2 s |
| Required tests / gates | GATE-J06 |
| Evidence for completion | Journey recording and test log |
| Security implications | Command-template launch must not pass unescaped model output to a shell. |
| Estimate · complexity · risk · tier · cost | 0.25–0.5 pw · S · LOW · T1 · FREE |
| Blockers | — |
| Parallel group | R0b-product |
| Status | NOT_STARTED |
| Reference | 08-UX-JOURNEYS-AND-DESIGN-SYSTEM.md J06 |

### Z-14 — Hardware-specific performance baseline and regression harness

| Field | Contract |
|---|---|
| Milestone / subsystem / owner | R0b · Observability · AGENT |
| Why | Targets must come from measurements on the founder machine (i5-13420H, 16 GB, integrated GPU), not from competitor claims. |
| Dependencies (must finish first) | Q-05 |
| Gates it opens for V3 tasks | F-15 (Measured baseline feeds the R0 budget check) |
| Deliverables | Scripted measurements: cold and warm start, idle memory of all Zain processes, terminal open, open a 50k-file repository, git status refresh, diff render of 5k changed lines, agent-turn overhead excluding model time; reference = the upstream T3 release installer at the chosen pin run in the same isolated account (download needs founder approval), not a second local build; CSV output; report |
| Acceptance criteria | Each metric measured 5 times with median and p95 on the installed Zain build and on the upstream release build; numbers recorded in 09-PERFORMANCE-PLAN.md replacing PROVISIONAL values |
| Required tests / gates | GATE-PERF-BASE |
| Evidence for completion | Harness output CSV and machine description |
| Security implications | None. |
| Estimate · complexity · risk · tier · cost | 0.5–1 pw · M · MEDIUM · T1 · FREE |
| Blockers | — |
| Parallel group | R0b-product |
| Status | NOT_STARTED |
| Reference | 09-PERFORMANCE-PLAN.md |

### Z-22 — Unsigned-build trust posture, clean uninstall and tester install instructions

| Field | Contract |
|---|---|
| Milestone / subsystem / owner | R0b · Packaging · AGENT |
| Why | The zero-cost path ships unsigned NSIS installers; SmartScreen warns and no reputation accrues; testers must be told exactly what they are running. |
| Dependencies (must finish first) | F-11 |
| Gates it opens for V3 tasks | F-16 (Uninstall posture before the P2 exit) |
| Deliverables | Posture note (no signed or verified claim), private SHA-256 list per build, install/uninstall instructions, uninstall test |
| Acceptance criteria | Uninstall removes program files, shortcuts, protocol handler and AUMID registration; documented user-data directories remain only if the user opts to keep them; a file and registry diff before install and after uninstall shows nothing else |
| Required tests / gates | GATE-PKG-02, GATE-J01 |
| Evidence for completion | Diff output and instructions file |
| Security implications | Prevents false trust claims. |
| Estimate · complexity · risk · tier · cost | 0.25 pw · S · MEDIUM · T1 · FREE |
| Blockers | — |
| Parallel group | R0b-product |
| Status | NOT_STARTED |
| Reference | 12-TEST-QA-AND-DEFINITION-OF-DONE.md §4 |

### Z-27 — Make checkpoint restore non-destructive for untracked files

| Field | Contract |
|---|---|
| Milestone / subsystem / owner | R0b · Git engine · AGENT |
| Why | T3 restore runs git restore, then git clean -fd, then git reset (R02 §6): untracked, non-ignored files the user created are destroyed on revert. |
| Dependencies (must finish first) | Q-05 |
| Gates it opens for V3 tasks | F-21 (Checkpoint data-loss fix counted in tester defects) |
| Deliverables | Before clean, move untracked non-ignored files that differ from the checkpoint into a recoverable quarantine; show what was quarantined; restore-from-quarantine action; quarantine under the Zain data directory per project, retained 14 days, capped at 2 GB or 10% of free space (PROPOSED values) |
| Acceptance criteria | Revert in a fixture with a user-created untracked file keeps the file in quarantine and lists it; the negative test fails when quarantine is removed; T3's existing checkpoint tests still pass |
| Required tests / gates | GATE-J18 |
| Evidence for completion | Test log |
| Security implications | Prevents silent data loss for testers. |
| Estimate · complexity · risk · tier · cost | 0.25–0.5 pw · S · HIGH · T2 · FREE |
| Blockers | — |
| Parallel group | R0b-product |
| Status | NOT_STARTED |
| Reference | specs/008 research/R02_T3_CODE.md §6 |

### Z-30 — Minimal journey harness for R0b with a deterministic replay provider

| Field | Contract |
|---|---|
| Milestone / subsystem / owner | R0b · Testing engine · AGENT |
| Why | R0b gates (J01, J06, J18, J21, egress capture) need scripted runs before the full R0 suite exists; journeys with model turns need deterministic provider output. |
| Dependencies (must finish first) | Q-05 |
| Gates it opens for V3 tasks | — |
| Deliverables | Playwright-for-Electron harness attached to the installed build; silent NSIS install (/S) for scripted J01 with the SmartScreen step documented as manual; record/replay provider adapter that replays recorded turns deterministically; procedure to run the harness inside the isolated account (scheduled task at logon); network capture hook |
| Acceptance criteria | J01, J06, J18 and J21 pass 3 consecutive runs on the installed build with the replay provider; one live-provider smoke run recorded separately; Electron fuses checked so automation attaches to the packaged app |
| Required tests / gates | GATE-J01, GATE-J06, GATE-J18, GATE-J21 |
| Evidence for completion | Harness run reports, installer SHA-256, replay fixture hashes |
| Security implications | Replay fixtures contain no secrets; live runs use synthetic projects. |
| Estimate · complexity · risk · tier · cost | 0.75–1.25 pw · M · MEDIUM · T1 · FREE |
| Blockers | — |
| Parallel group | R0b-product |
| Status | NOT_STARTED |
| Reference | 14-INDEPENDENT-REVIEWS.md E-05, E-06 |

### Z-31 — Verify or implement per-file and per-hunk accept/reject in the diff panel

| Field | Contract |
|---|---|
| Milestone / subsystem / owner | R0b · Git engine · AGENT |
| Why | J06 needs accept/reject of agent changes; T3 provides diff review and viewed-state, but per-hunk reject is not confirmed in the research. |
| Dependencies (must finish first) | Q-05 |
| Gates it opens for V3 tasks | — |
| Deliverables | Verification on the installed build; if missing, per-hunk reject restoring the hunk from the pre-turn checkpoint, per-file accept/reject, keyboard shortcuts |
| Acceptance criteria | In a fixture turn touching 3 files, rejecting one hunk restores only that hunk; rejecting a file restores the whole file; accepted changes stay; the negative test fails if restore writes outside the hunk |
| Required tests / gates | GATE-J06 |
| Evidence for completion | Harness report and diff fixtures |
| Security implications | Writes only inside the worktree. |
| Estimate · complexity · risk · tier · cost | 0.25–1 pw · M · MEDIUM · T1 · FREE |
| Blockers | — |
| Parallel group | R0b-product |
| Status | NOT_STARTED |
| Reference | 14-INDEPENDENT-REVIEWS.md C-01 |

### Z-11 — Capability-based model registry and local OpenAI-compatible lane with data-class routing

| Field | Contract |
|---|---|
| Milestone / subsystem / owner | R0 · Model gateway · AGENT |
| Why | Provider neutrality and the no-paid path need local endpoints (Ollama, llama.cpp server, LM Studio) and authorized remote endpoints routed by measured capability and data class, not by hard-coded model names. |
| Dependencies (must finish first) | F-02, F-22 |
| Gates it opens for V3 tasks | — |
| Deliverables | Server-side data classification: workspace content is at least private-code, callers may only raise the class, unknown fails closed; route registry with founder-set data_classes_allowed covering both raw OpenAI-compatible endpoints (run through the existing OpenCode worker as the tool loop) and hosted agent CLIs (Codex, ACP); pre-session check of each hosted agent's effective base URL and provider config (refuses the OpenCode third-party relay and any unauthorized route); local endpoints bound to their owning process image or started with a per-session token; probe runner (tool_calls, json_schema, context, fim, latency); per-route token and time budgets; endpoint settings UI; local-model capability report on 20 fixture tasks per role |
| Acceptance criteria | Probes record capabilities for a local endpoint; a task needing tool calls is refused for a route whose probe failed, with a visible reason; a hosted agent session whose effective endpoint is not authorized for the project data class is refused (network capture shows no request); a spoofed localhost listener with the wrong process image is refused; a budget cap stops requests; negative tests fail with each guard removed |
| Required tests / gates | GATE-MODEL-01, GATE-MODEL-02, GATE-J03 |
| Evidence for completion | Probe outputs, routing decision log, negative test that fails with the data-class guard removed |
| Security implications | Controls only routes Zain launches or configures; agents that read files or open connections themselves remain UNMEDIATED until R1 (C-17) and S-04. |
| Estimate · complexity · risk · tier · cost | 1–2 pw · M · HIGH · T2 · FREE |
| Blockers | — |
| Parallel group | R0-product |
| Status | NOT_STARTED |
| Reference | 06-MODELS-CONTEXT-AND-REVIEW.md §2–§3 |

### Z-15 — Journey acceptance suite for the initial-release journeys on the installed build

| Field | Contract |
|---|---|
| Milestone / subsystem / owner | R0 · Testing engine · AGENT |
| Why | Release readiness must be shown in the real desktop application, not mocked UI tests. |
| Dependencies (must finish first) | F-16, Z-11, Z-13, Z-17, Z-21, Z-30 |
| Gates it opens for V3 tasks | — |
| Deliverables | Extension of the Z-30 harness with scripts for J02 J03 J04 J05 J06 J07 J09 J11 J12 J13 J15 J16 J18 against the installed NSIS build in the isolated account; failure-path variant per journey |
| Acceptance criteria | Every listed journey passes its happy path and its recorded failure path on the installed build; flaky runs are counted and must be 0 in 3 consecutive full runs |
| Required tests / gates | GATE-J02, GATE-J03, GATE-J05, GATE-J07, GATE-J09, GATE-J11, GATE-J12, GATE-J15, GATE-J16, GATE-J22 |
| Evidence for completion | Test reports from 3 consecutive runs, installer SHA-256 |
| Security implications | Tests run with synthetic credentials and fixtures only. |
| Estimate · complexity · risk · tier · cost | 1.5–2.5 pw · M · MEDIUM · T1 · FREE |
| Blockers | — |
| Parallel group | R0-product |
| Status | NOT_STARTED |
| Reference | 08-UX-JOURNEYS-AND-DESIGN-SYSTEM.md |

### Z-17 — Zain design language v1 applied to the forked UI

| Field | Contract |
|---|---|
| Milestone / subsystem / owner | R0 · UI architecture · AGENT |
| Why | Rebranding (F-03) changes names; the product also needs its own visual identity, consistent tokens and accessible contrast instead of the donor's look. |
| Dependencies (must finish first) | F-03 |
| Gates it opens for V3 tasks | F-14 (Design tokens precede the contrast and focus pass) |
| Deliverables | Token source (CSS custom properties in the Tailwind 4 theme): color (light and dark), typography scale, spacing, radius, elevation, motion durations and easings, focus ring; app icon set; applied to shell chrome, sidebar, chat, diff, terminal frame, approvals and empty/loading/error states |
| Acceptance criteria | No donor brand asset or donor color token remains in packaged UI; every declared foreground/background pairing in the token file meets WCAG 2.2 AA (4.5:1 normal, 3:1 large and UI components) in both themes; tokens are the single source (no raw hex in components outside the token file, checked by a lint rule) |
| Required tests / gates | GATE-ID-01, GATE-A11Y-01 |
| Evidence for completion | Token contrast report, lint output, light/dark screenshots |
| Security implications | None. |
| Estimate · complexity · risk · tier · cost | 1–2 pw · M · LOW · T1 · FREE |
| Blockers | — |
| Parallel group | R0-product |
| Status | NOT_STARTED |
| Reference | 08-UX-JOURNEYS-AND-DESIGN-SYSTEM.md §3 |

### Z-21 — Session and workspace restore plus crash-recovery verification on the installed build

| Field | Contract |
|---|---|
| Milestone / subsystem / owner | R0 · Workspace manager · AGENT |
| Why | Users must be able to resume after crashes; T3 resumes threads after server restart, but this has to be shown on the installed Windows build. |
| Dependencies (must finish first) | F-16 |
| Gates it opens for V3 tasks | — |
| Deliverables | Fault-injection scripts: kill the server, kill the desktop, power-loss simulation by process tree kill during a running turn and during checkpoint capture |
| Acceptance criteria | After relaunch, projects, threads, worktrees and pending supervised-mode prompts are re-shown or the turn is marked interrupted; only the in-flight turn is lost and is marked interrupted; checkpoint store is consistent (git fsck on hidden refs) |
| Required tests / gates | GATE-REC-01, GATE-J13 |
| Evidence for completion | Fault-injection log |
| Security implications | None beyond data integrity. |
| Estimate · complexity · risk · tier · cost | 0.5 pw · S · MEDIUM · T1 · FREE |
| Blockers | — |
| Parallel group | R0-product |
| Status | NOT_STARTED |
| Reference | 08-UX-JOURNEYS-AND-DESIGN-SYSTEM.md J13 |

### Z-24 — Amend B-01 for Windows 11 Home (no Windows Sandbox or Hyper-V)

| Field | Contract |
|---|---|
| Milestone / subsystem / owner | R0 · Testing engine · AGENT+FOUNDER |
| Why | B-01 assumes a Windows Sandbox or VM baseline image, which this machine cannot run; the founder's build is Windows 11 Home 10.0.26300. |
| Dependencies (must finish first) | — |
| Gates it opens for V3 tasks | B-01 (Baseline amended before provisioning) |
| Deliverables | Amended baseline: separate local account (Z-09) as the default isolation; a free VM (e.g. VirtualBox) only if Z-07 capacity allows; decision recorded |
| Acceptance criteria | B-01's contract text updated through the V3 change path or superseded by this task with founder approval; baseline provisioning steps run on the founder machine |
| Required tests / gates | GATE-R0-EXIT |
| Evidence for completion | Updated contract text and provisioning log |
| Security implications | Isolation strength is weaker than a VM; stated in claims. |
| Estimate · complexity · risk · tier · cost | 0.1 pw · S · MEDIUM · T0 · FREE |
| Blockers | — |
| Parallel group | R0-quality |
| Status | NOT_STARTED |
| Reference | 01-REPOSITORY-AUDIT.md §5 |

### Z-26 — Repair the V3 validator fail-open parsing (A3-01) and exit ordering (A3-02 / C-1)

| Field | Contract |
|---|---|
| Milestone / subsystem / owner | R0 · Program/Governance · AGENT |
| Why | Reproduced at 23bea38: malformed task rows, missing GENERATED:END, reversed estimates, duplicate requirements and empty suites all exit 0; C-28 is not an effective ancestor of X-01. |
| Dependencies (must finish first) | — |
| Gates it opens for V3 tasks | F-01 (Validator repaired before admission of the FWB tree for main) |
| Deliverables | Strict section-specific row schema with fail-closed errors; END-marker pairing; estimate ordering; duplicate detection; non-empty suites; exit-prerequisite closure check; COV-08/COV-09 split from V-04; C-28 made an ancestor of X-01; mutation cases that assert the specific error message |
| Acceptance criteria | Each Round-3 adversarial mutation fails with its specific message; existing 26 cases still pass; plan_graph.py --check exits 0 on the corrected catalog |
| Required tests / gates | GATE-PLAN-03 |
| Evidence for completion | Mutation run output before and after |
| Security implications | Planning integrity only. |
| Estimate · complexity · risk · tier · cost | 0.5–1 pw · M · HIGH · T2 · FREE |
| Blockers | — |
| Parallel group | R0-quality |
| Status | NOT_STARTED |
| Reference | specs/008 OPUS packet §D |

### Z-32 — Daily-use log on the first release (10 working days) with defect list

| Field | Contract |
|---|---|
| Milestone / subsystem / owner | R0 · Program/Governance · FOUNDER |
| Why | Later tiers should start only on evidence from real use (RK-03); no gate collected that evidence. |
| Dependencies (must finish first) | Z-30, Z-31 |
| Gates it opens for V3 tasks | — |
| Deliverables | Log of 10 working days using the R0b build for real work: tasks done, failures, workarounds, missing features; defect rows added to the backlog |
| Acceptance criteria | 10 dated entries; every crash or data-loss event has a backlog row; go / adjust decision for R1 recorded |
| Required tests / gates | GATE-USE-01 |
| Evidence for completion | Log file and linked backlog rows |
| Security implications | Log must not include secrets. |
| Estimate · complexity · risk · tier · cost | 0.5 pw · S · LOW · T0 · FREE |
| Blockers | — |
| Parallel group | R0-quality |
| Status | NOT_STARTED |
| Reference | 14-INDEPENDENT-REVIEWS.md C-05 |

### Z-33 — Restore the WSL backend with a sanitized Linux CLI and parity tests (A3-09)

| Field | Contract |
|---|---|
| Milestone / subsystem / owner | R0 · Application shell · AGENT |
| Why | Q-04 disables the T3 WSL backend for R0a; V3 A3-09 requires restoration in Qualified R0 and no task existed. WSL2 processes run in a VM outside Job Objects, fs-gate and the kill switch. |
| Dependencies (must finish first) | F-16 |
| Gates it opens for V3 tasks | — |
| Deliverables | Sanitized Linux CLI archive, identity and egress overlay parity, provider startup smoke under WSL, WSL contexts labelled UNKNOWN coverage and excluded from ProcessHost and kill-switch claims, revised estimate |
| Acceptance criteria | WSL backend starts, runs a provider turn and passes identity and egress checks under WSL; UI and claims label WSL sessions as not contained; founder WSL disks untouched |
| Required tests / gates | GATE-R0-EXIT |
| Evidence for completion | Smoke log and egress capture under WSL |
| Security implications | Must not modify existing WSL VHDX files; WSL is outside Windows containment. |
| Estimate · complexity · risk · tier · cost | 1–2 pw · M · MEDIUM · T2 · FREE |
| Blockers | — |
| Parallel group | R0-product |
| Status | NOT_STARTED |
| Reference | specs/008 OPUS packet §D A3-09 |

### Z-34 — User, install and troubleshooting documentation for the first releases

| Field | Contract |
|---|---|
| Milestone / subsystem / owner | R0 · UI architecture · AGENT |
| Why | The Definition of Done requires installation, user-workflow and troubleshooting documentation; G-06 covers governance documents only. |
| Dependencies (must finish first) | Z-22, F-16 |
| Gates it opens for V3 tasks | — |
| Deliverables | Install/uninstall guide (unsigned build, SmartScreen), first-run and model setup, journey how-tos, known limitations (no mediation or injection control before R1), troubleshooting and log collection |
| Acceptance criteria | A tester following only the guide completes J01, J03, J04 and J06 in the isolated account; every known limitation in 02 §3 appears in the guide |
| Required tests / gates | GATE-R0-EXIT |
| Evidence for completion | Guide and one guided tester run log |
| Security implications | No credentials in examples. |
| Estimate · complexity · risk · tier · cost | 0.5–1 pw · S · LOW · T0 · FREE |
| Blockers | — |
| Parallel group | R0-quality |
| Status | NOT_STARTED |
| Reference | 12-TEST-QA-AND-DEFINITION-OF-DONE.md §2 |

### Z-12 — Local fill-in-the-middle completion and inline-edit command in Monaco

| Field | Contract |
|---|---|
| Milestone / subsystem / owner | R1 · Editor kernel · AGENT |
| Why | Tab completion is table stakes in every competitor; Cursor, Copilot and JetBrains do not allow local models for completions, so a local lane is a real gap Zain can own; CPU-only hardware makes latency the deciding measure. |
| Dependencies (must finish first) | F-17, Z-11 |
| Gates it opens for V3 tasks | — |
| Deliverables | Inline-completion provider bound to a FIM-capable local route; inline-edit command (select, instruct, preview diff, accept/reject) routed through Z-11; debounce and cancellation; latency measurement kept local; off switch |
| Acceptance criteria | With a local FIM model, completions appear without network access; p50 and p95 latency are measured on the founder machine and displayed; the lane disables itself by default when p50 exceeds the GATE-PERF-07 threshold |
| Required tests / gates | GATE-PERF-07 |
| Evidence for completion | Latency measurements (20 prompts × 5 runs), network capture showing no egress |
| Security implications | None beyond Z-11 routing. |
| Estimate · complexity · risk · tier · cost | 1–1.5 pw · M · MEDIUM · T1 · FREE |
| Blockers | — |
| Parallel group | R1-editor |
| Status | NOT_STARTED |
| Reference | 06-MODELS-CONTEXT-AND-REVIEW.md §2 |

### Z-16 — Journey acceptance extension for the R1 journeys (approvals, recovery, security events)

| Field | Contract |
|---|---|
| Milestone / subsystem / owner | R1 · Testing engine · AGENT |
| Why | R1 adds authority, approvals and recovery; their journeys must be verified end to end before the R1 exit. |
| Dependencies (must finish first) | Z-15, C-13, C-14, C-19, C-26 |
| Gates it opens for V3 tasks | X-01 (R1 journeys before the R1 release exit) |
| Deliverables | Scripts for J10 J14 J19 on the installed R1 build, including denial, timeout and unknown-outcome paths |
| Acceptance criteria | J10, J14 and J19 pass happy and failure paths on the installed build; approval presentation level (A1/A2/A3) is asserted in each approval step |
| Required tests / gates | GATE-J10, GATE-J14, GATE-J19 |
| Evidence for completion | Test reports, installer SHA-256 |
| Security implications | Exercises the approval and recovery boundaries. |
| Estimate · complexity · risk · tier · cost | 1–1.5 pw · M · MEDIUM · T2 · FREE |
| Blockers | — |
| Parallel group | R1-quality |
| Status | NOT_STARTED |
| Reference | 08-UX-JOURNEYS-AND-DESIGN-SYSTEM.md |

### Z-19 — Destructive-operation guards: bulk delete, synced and protected paths, disk reserve

| Field | Contract |
|---|---|
| Milestone / subsystem / owner | R1 · Tool execution broker · AGENT |
| Why | Lessons from Z-18 and from public competitor incidents (an agent wiping a drive in an auto-approve mode): deletion and disk exhaustion need enforcement, not prompts. |
| Dependencies (must finish first) | H-08, C-12 |
| Gates it opens for V3 tasks | X-01 (Destructive guards before the R1 release exit) |
| Deliverables | Policy rules and fs-gate checks: deletes of more than N entries or outside the workspace need A2 approval; paths under OneDrive, user-profile roots and other workspaces are protected; deletes go to a recoverable quarantine by default; writes stop when free space falls below a reserve; git clean/restore of untracked files quarantines first; proposed values: bulk threshold 25 entries, disk reserve max(5 GB, 10% of volume); policy for OneDrive Files On-Demand placeholders (cloud-file reparse points): refuse OneDrive-hosted workspaces in R1 unless the founder allowlists the cloud-file reparse tag |
| Acceptance criteria | Each guard has a negative test that fails when the guard is removed; quarantine restore round-trips; the disk-reserve stop triggers in a fixture with a small quota |
| Required tests / gates | GATE-SEC-03 |
| Evidence for completion | Test log with guard-removed mutation results |
| Security implications | Core destructive-action control. |
| Estimate · complexity · risk · tier · cost | 0.5–1 pw · M · HIGH · T2 · FREE |
| Blockers | — |
| Parallel group | R1-security |
| Status | NOT_STARTED |
| Reference | 07-SECURITY-AND-CONTAINMENT.md §6 |

### Z-20 — IDE-parity spike: Monaco + LSP client vs monaco-vscode-api workbench services, measured on founder hardware; Code-OSS as a desk estimate only

| Field | Contract |
|---|---|
| Milestone / subsystem / owner | R1 · Editor kernel · AGENT |
| Why | Pillar A asks for an IDE excellent without AI; V3 schedules LSP and DAP for R3; the choice between staying on Monaco and moving to a VS Code-compatible base must rest on measured cost, not preference. |
| Dependencies (must finish first) | — |
| Gates it opens for V3 tasks | I-03 (IDE-parity decision before the LSP spike); F-17 (Editor-path decision before Monaco integration) |
| Deliverables | Timeboxed spike (1 week) for the two Monaco options: bundle size, idle and peak memory, cold start, Open VSX web-extension compatibility; desk estimate (no build) of a Code-OSS fork's build disk/RAM and rebase cadence from published data; ADR-Z03 decision update |
| Acceptance criteria | Decision recorded with measured numbers for both Monaco options and a sourced desk estimate for Code-OSS; reopening ADR-001 requires the founder and is considered only if the first working build or Z-20 fails |
| Required tests / gates | GATE-IDE-01 |
| Evidence for completion | Spike report and raw measurements |
| Security implications | None (throwaway branch). |
| Estimate · complexity · risk · tier · cost | 1 pw · M · MEDIUM · T1 · FREE |
| Blockers | — |
| Parallel group | R1-editor |
| Status | NOT_STARTED |
| Reference | 05-ARCHITECTURE-AND-DECISIONS.md ADR-Z03 |

### Z-28 — Local-only code index: ripgrep search and tree-sitter symbol index (embeddings deferred)

| Field | Contract |
|---|---|
| Milestone / subsystem / owner | R1 · Context engine · AGENT |
| Why | Every competitor's semantic index is cloud-backed or GitHub-bound (Copilot external ingest, JetBrains Air Context, Cursor's server-side pipeline); V3 has a Brain FTS5 store (M-03) and rg as an effect (H-04, R3) but no code index for agent context or symbol navigation. |
| Dependencies (must finish first) | F-17, Z-11 |
| Gates it opens for V3 tasks | H-04 (Local index precedes rg search adapters) |
| Deliverables | Index service in the forked Server: rg-backed text search, tree-sitter symbol tables for TS/JS, Python, Rust, Go, C#, incremental update from the file watcher, context-retrieval API used by agent prompts and the editor; embeddings only after a V3 ADR-006 amendment |
| Acceptance criteria | Index builds and updates with networking disabled; symbol search and text search return within GATE-CTX-01 thresholds on the 50k-file fixture; zero egress (network capture); index excludes .gitignore'd and .zainignore'd paths |
| Required tests / gates | GATE-CTX-01 |
| Evidence for completion | Timing CSV, network capture, ignore-rule test |
| Security implications | Index must honour ignore rules so secrets in ignored files are not surfaced to models. |
| Estimate · complexity · risk · tier · cost | 1.5–2.5 pw · M · MEDIUM · T2 · FREE |
| Blockers | — |
| Parallel group | R1-context |
| Status | NOT_STARTED |
| Reference | 06-MODELS-CONTEXT-AND-REVIEW.md §4 |

### Z-23 — Engineering execution report export (journey J20)

| Field | Contract |
|---|---|
| Milestone / subsystem / owner | R2 · Observability · AGENT |
| Why | The user must be able to export a complete, reviewable record of an agent task; V3 has evidence pieces (ledger, receipts, browser evidence) but no export journey. |
| Dependencies (must finish first) | C-19, V-04, Y-06 |
| Gates it opens for V3 tasks | — |
| Deliverables | Export command and menu: self-contained Markdown and HTML bundle with task, plan, diffs, tool receipts, approvals, tests, unknown outcomes and the unanchored ledger interval; secrets redacted; bundle hash |
| Acceptance criteria | Exported bundle opens offline; every effect in the ledger for the task appears; a seeded secret in a tool output is redacted; re-export yields the same hash |
| Required tests / gates | GATE-J20 |
| Evidence for completion | Sample bundle from a fixture task and the redaction test |
| Security implications | Redaction failures would leak secrets. |
| Estimate · complexity · risk · tier · cost | 0.5–1 pw · M · MEDIUM · T2 · FREE |
| Blockers | — |
| Parallel group | R2-quality |
| Status | NOT_STARTED |
| Reference | 08-UX-JOURNEYS-AND-DESIGN-SYSTEM.md J20 |

<!-- GENERATED:END zmp-contracts -->
