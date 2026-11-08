# 01 — Repository Audit (verified 2026-11-08)

```text
REPOSITORY   = https://github.com/TheHalfMoon/Zain  (repository ID 1334408699; renamed from wepld by the founder)
VISIBILITY   = PUBLIC   (gh repo view, 2026-11-08) — conflicts with the founder's "Zain stays private" rule
DEFAULT      = main @ 0a843a2c0913236d9c93b31abb0d54bbdb023f23 (Merge PR #345, 2026-09-29)
PLANNING TIP = docs/r0a-opus-start-20261102 @ 23bea38c6dd0deefcae5d5188a18a7d061ab2588 (2026-11-02), 24 commits ahead of main, unmerged
THIS PLAN    = docs/zain-master-plan-20261108, branched from 23bea38 (local only; not pushed — see §2)
METHOD       = gh read-only API, a full local clone of all 353 remote refs, a temporary worktree of main, static code
               reading, CI history; no product code was built successfully (§4)
```

Every statement below is marked **V** (verified by a command or file read in this session) or **I** (inferred).
Paths without a prefix are relative to the repository root on the stated commit.

## 1. Executive findings

1. **Nothing of the selected architecture exists yet** (V). V3 selected a hard fork of T3 Code with Zain's Rust Core
   as the authority. No T3 source has been imported, no Q-00 record exists, and there is no `build/first-working`
   branch anywhere. The Zain product on `main` is a 10,086-line Rust Core plus a Tauri status window that V3 retires.
2. **The repository is public, and so is the legacy one** (V). `TheHalfMoon/Zain` and `wepld/wepld` are both
   PUBLIC. The 20,081-line V3 planning package, research notes and (per the V3 ledger) local machine details in
   commits `c376917` and `ef19a3f` are publicly reachable. Every push from here on publishes. This plan is therefore
   committed **locally only** until the founder decides DEC-02.
3. **Governance code outweighs product code 8.4 to 1** (V). `.github` holds 85,056 lines (169 Python scripts, 72
   policy generations v1–v72). Product code is 10,086 non-test lines. Planning documents add 48,156 lines on `main`
   and another 20,081 on the V3 branch. About 350 PRs were opened, most as policy-reopen / test / reconcile triplets.
4. **Part of the status context given to this session belongs to another project** (V). The E4, E5, E6A/E6B
   ("review provider decision") and related specs live in `TheHalfMoon/Ascout` under
   `specs/017-unified-assurance/`. Commit `70458ae` is Ascout's `main` head (PR #664, 2026-11-07). `FD-4` appears only
   in Ascout research and in `commandF`. No `usn-journal.csv` exists in any TheHalfMoon repository default branch or
   in any of Zain's 353 refs. The R0a/R0b milestones, the plan validator and its 26 mutation cases **are** Zain's.
5. **The machine cannot build the planned product today** (V). C: has 3.4 GB free (99% used), D: has 20 GB free
   (8 GB earlier the same day), RAM is 15.7 GB with very little free, and the GPU is integrated (Intel UHD).
   Node 24.19.0 and pnpm 9.12.0 are installed; T3 pins Node 26.12.1 and pnpm 12.14.0.
6. **The V3 plan is detailed but carries open defects** (V). Its validator passes (176 tasks, 383 tests, 26/26
   mutations) yet still fails open on malformed input (A3-01). Original Critical C-1 (exit ordering) still reproduces.
   R1 remains "DO NOT APPROVE" after three Astro review rounds. The approval conditions A3–A7 for starting R0a are
   not evidenced.

## 2. Repository identity, visibility and exposure

| Item | Evidence | State |
|---|---|---|
| Canonical repository | `gh repo view TheHalfMoon/Zain` | V: exists, ID 1334408699, created 2026-08-14, default branch `main`, last push 2026-11-02 |
| Visibility | same | V: **PUBLIC**. The V3 ledger recorded PRIVATE on 2026-10-27 and then "PUBLIC; renamed from wepld by founder" the same day |
| Legacy repository | `gh repo view wepld/wepld` | V: **PUBLIC**, separate account `wepld`, last push 2026-07-19 |
| Separate project | `TheHalfMoon/Zain-LLM` | V: PRIVATE; described as "Nas: a from-scratch language model"; not part of this plan, not touched |
| Local working copies | search of the user profile and `D:\` to depth 3 | V: none of TheHalfMoon/Zain. `%USERPROFILE%\OneDrive\Desktop\wepld` is a checkout of `wepld/wepld` whose working tree shows **every tracked file deleted** (`git status` lists only ` D` entries). Not modified by this session |
| Installed AI review apps | V3 `EGRESS_PREFLIGHT_2026-10-27.md` §2–3; `cubic.yaml` on main | V (from the record): Cubic, CodeRabbit, Qodo, Cursor Bugbot, Devin, Sentry, Vercel, the Claude GitHub App, Graphite and Greptile held or hold access; their automatic-review settings cannot be read through the API |

**Consequences.** Z-01 (founder: make private), Z-02 (close app egress), Z-03 (exposure assessment). Making the
repository private on GitHub Free removes protected branches and rulesets (GitHub docs, checked 2026-11-08) and limits Actions to a small included compute allowance; V3 task G-07
assumed a public repository (RK-19, DEC-03).

## 3. What is implemented on `main` (0a843a2)

| Area | Non-test LOC | Test LOC | What it is | State |
|---|---|---|---|---|
| `crates/contracts` (`wepld-contracts`) | 1,727 | 956 | Length-prefixed framing; protocol v1 with 5 capabilities (`protocol.rs:68-74`); S2 project types | V: implemented, CI-tested |
| `crates/core` (`wepld-core`) | 7,392 | 7,419 | Identity, read-only git topology, evidence store, doctor; binaries `wepld-core` (stdio sidecar) and `wepld` (CLI: `open`, `doctor`, `status`, `--json`) | V: implemented, CI-tested |
| `apps/desktop/src-tauri` | 906 | 677 | Tauri 2.11.5 host with 6 commands (ready, health, version, capabilities, observe, cancel) | V: implemented; **retired by V3 (F-18)** |
| `apps/desktop/ui` | 61 | — | One static page with status lines and two buttons | V |
| `third_party/glib-0.18.5-wepld1` | 53,838 vendored | — | Backport for RUSTSEC-2024-0429, needed only for Tauri on Linux | V: retired with Tauri |
| `src/` | 0 | — | `.gitkeep` | V |

**What a user can do today** (V): launch a 960×640 window titled "WePLD" that shows the sidecar's health and version,
and run `wepld open <path>` to record a read-only git-topology "generation" in `%LOCALAPPDATA%`. There is no editor,
terminal, file tree, chat, model access or agent. The desktop window does not expose the S2 CLI features.

**Tests.** Static count 260 (`contracts` 25, `core` 217, `desktop` 18) (V). The last Rust CI run on main
(`s1-contracts` 34560177057 on 7af08de, 2026-09-11) passed on Ubuntu, macOS and Windows. No product file changed
afterwards, so it still covers today's code (V). The newest main run (`foundation-integrity` 36589753362 on 0a843a2)
passed, but it runs only governance policy (V). **Gap:** the Windows CI job runs only `wepld-desktop` tests; the
`#[cfg(windows)]` core tests (`crates/core/tests/project_v1.rs:50,224,347,379`) never run in CI (V).

**Local test run.** A local `cargo test --workspace` in a temporary worktree failed to link (LNK1104 on
`icu_properties_data` / `icu_normalizer_data` build scripts), most probably because of the 169-character worktree path
or low disk space (I). The 52 MB target directory was deleted afterwards. No local test result is claimed.

## 4. Implementation-state classification

| Class | Items | Evidence |
|---|---|---|
| Implemented and qualified | S1 desktop–core handshake (`specs/001…/tasks.md:23` `S1_ACCEPTED = YES`); S2 open/doctor/identity/evidence store (`specs/005…/tasks.md:17` `CLOSED_CANONICAL`, 8 carried limitations) | V; no security review passed: `CODEX_SECURITY_STATUS = NOT_RUN_NON_BLOCKING` (`specs/001…/tasks.md:81`, `specs/005…/tasks.md:471`) |
| Implemented, not qualified for the target | Tauri shell (to be retired); evidence store growth without pruning | V |
| Partially implemented | S3 terminal fabric: policy scripts v69–v72 on main, contracts code only in open PR #343 | V |
| Missing (planned in V3) | Everything from R0a onward: T3 fork, identity overlay, egress removal, packaging, Trusted Core authority, review, missions, browser, DeskGate, IDE breadth, design studio, sandbox, remote | V |
| Missing (not planned anywhere before this plan) | Repository privacy restoration; reviewer route authorization; capacity remediation; local model gateway with data classes; local completion; local code index; journey harness and tests; per-hunk accept/reject; design language; hardware performance baseline; non-destructive checkpoint restore; WSL backend restoration; user documentation; daily-use evidence; execution report export | V (Z-01..Z-34) |

## 5. Technical debt, inconsistencies and weaknesses

| # | Finding | Evidence | Action |
|---|---|---|---|
| 1 | `README.md:15` says `IMPLEMENTATION = NOT_STARTED` while 10k product lines and 260 tests exist | V | G-06 |
| 2 | `CURRENT_STATE.md` is a 2026-09-12 checkpoint: names `TheHalfMoon/wepld` (`:4`), says `S1_ACCEPTED = NO` (`:506`) and S2 `NOT_YET_CLOSED_CANONICAL` (`:718`); omits v66–v72, S3, Astro | V | G-06, Z-04 |
| 3 | 2,968 "wepld" occurrences and 316 file paths with "wepld"; 0 "Zain" on main; `tauri.conf.json` productName "WePLD", identifier `com.wepld.desktop` | V | F-03, N-04, F-10 |
| 4 | V3 validator fails open: malformed rows, missing END marker, reversed estimates, duplicate requirements and empty suites all exit 0 at 23bea38 | V (reproduced) | Z-26 |
| 5 | C-28 is not an effective ancestor of X-01 (C-1 / A3-02) | V (computed) | Z-26 |
| 6 | `ASTRO_FINDINGS_DISPOSITION.md:18` still marks C-1 RESOLVED; master-plan gate G6 still reads "Astro round 2 approves R1" although rounds 2 and 3 said DO NOT APPROVE | V | Z-26, G-06 |
| 7 | B-01 assumes Windows Sandbox; the founder machine is Windows 11 Home (no Sandbox, no Hyper-V) | V | Z-24 |
| 8 | V3 rows still allow a private-repo / Actions build (14_TASK_CATALOG.md:28, CI-02, PKG-02, 24_FIRST_WORKING_BUILD.md:86, 22_SOURCE_ADMISSION_QUALIFICATION.md:63) while the R0a packet mandates LOCAL_ONLY | V | Q-00 records LOCAL_ONLY; Z-26 cleans text |
| 9 | Git binary is found by PATH lookup with no signature check (`crates/core/src/git_topology.rs:272`); the Git version is not observed (`:333`) although `--no-lazy-fetch` (`:43`) needs Git ≥ 2.44 | V / I | C-12 hardening |
| 10 | Path check resolves `..` textually before symlinks; git is pointed at the text-resolved path (`project.rs:175-201`, `bin/wepld.rs:136`) | V / I (low) | H-08 design |
| 11 | Tauri commands block under a mutex up to 5 s; sidecar never restarted after a crash (`core_client.rs:426-442`, `:460`) | V | Retired with F-18 |
| 12 | T3 checkpoint restore runs `git clean -fd`, destroying untracked user files (V3 `research/R02_T3_CODE.md` §6) | V (from source reading recorded in R02) | Z-27 |
| 13 | `AGENTS.md` lists Continue as a correctness review producer; Continue's repository is read-only and unmaintained | V | G-06 |
| 14 | Graft (PR #347) is now "Trail-code"; its `trail init` writes to `~/.claude.json` and `~/.codex/config.toml` and has telemetry on by default | V | Close #347 (Z-04) |

## 6. Pull requests and branches

There are 12 open PRs. None is a merge candidate under V3 (V). Recommended dispositions (Z-04, founder approval
required before any change):

| PR | Recommendation | Reason |
|---|---|---|
| #347 Graft context layer | Close | Conflicts with governed AGENTS.md changes (G-06); tool not admitted; see finding 14 |
| #346 source expansion (+1,368, specs/006) | Supersede | Old 006 task IDs collide with V3's Q-/K-/H-/F- namespaces |
| #343 S3 contracts C001–C013 (+1,791 Rust) | Keep as reference, do not merge | Adds Core code outside V3 gates; ProcessHost ownership moved to C-25 / ADR-024 |
| #342 ASTRO-B01 benchmark preregistration | Supersede after salvage into V3 09 | Salvage not done |
| #136 Pictorial/Agile vendor (+1.63M lines) | Close as stale | Contradicts "no donor transplant in public Zain"; branch remains public until deleted (founder) |
| #159, #162, #164 | Close as stale | Repairs for #136; #164 adds a v9 successor (retired pattern) |
| #73 JetBrains research | Close after mining for Design Studio | Not mined yet |
| #81, #88 MiniMax | Close | #88 replaces #81 |
| #1 fresh foundation | Close | Superseded by #2 (merged 2026-08-15) |

Unmerged planning branches: `docs/v3-unified-replan-20261027` (17 commits ahead of main), `docs/r0a-opus-start-20261102`
(24 ahead; contains the former) and this branch. V3 task G-01 ("merge this planning package") is pending.

## 7. Reconciliation of previously reported work

| Reported item | Verified finding |
|---|---|
| R0a feasibility qualification | Planned (V3 Q-00..Q-06, `OPUS_R0A_BUILD_EXECUTION_2026-11-02.md`). **Not started**: no Q-00 record, no build branch, A3–A7 not evidenced |
| R0b readiness | Planned (V3 R0b: B-06, F-05/06/07/11/20/21/22, N-01, Y-00). Not started |
| R1 trust contract | Planned (V3 R1, 17 trust-boundary spec, ADR-020..024). Astro Round 3: R1 DO NOT APPROVE; A3-01..A3-09 and C-1 open |
| E4 engineering work, E5 slices, E6 review infrastructure, E7 containment | **Ascout**, not Zain (`TheHalfMoon/Ascout/specs/017-unified-assurance/E4_EXECUTION_BROKER_SPEC.md`, `E5_GITLEAKS_ENGINE_SPEC.md`, `E6A_TEST_RUNS_CHECK_SPEC.md`, `E6B_REVIEW_PROVIDER_DECISION_SPEC.md`). Zain's analogues are the reviewer-route problem (Z-06) and containment (C-00, C-25, H-08, S-01) |
| FD-4 prerequisites | Not in any Zain ref. Appears in Ascout research and in `commandF` docs |
| Validator ~170 tasks / 343 tests | Zain V3 `plan_graph.py`: revision 3 recorded 165 tasks / 338 tests; revision 4 and today: **176 tasks / 383 tests / 26 mutations, exit 0** (V, re-run) |
| Mutation suite, 26 rejection cases | Zain V3 `test_plan_graph_mutations.py`: 26/26 pass (V). The harness checks exit codes only, not messages |
| Green main at `70458ae` | `70458ae` is Ascout's main head. Zain's main is `0a843a2`, green on its last governance run (V) |
| Deletion incident, `usn-journal.csv` | V3 ledger records a **disk-full incident**: donor clones filled the disk and were deleted (2026-10-28). `usn-journal.csv` not found. The OneDrive `wepld` working tree with every file deleted is unexplained (Z-18) |
| Older PRs needing reconciliation | §6 |

## 8. Operational and release blockers

| Blocker | Blocks | Owner | Task |
|---|---|---|---|
| Repository public | any push of build work or private planning | Founder | Z-01 |
| No authorized independent reviewer | every T2 gate; A7 | Founder | Z-06 |
| 3.4 GB free on C:, 20 GB on D: | Q-01, Q-04 | Founder | Z-07 |
| Toolchain below pins | Q-01 | Agent (download needs approval) | Z-08 |
| No isolated test account | Q-05 | Founder | Z-09 |
| Provider route not chosen | Q-05 real-provider turn | Founder | Z-10 |
| V3 validator fail-open, C-1 | Qualified R0, R1 approval | Agent | Z-26 |
| No code signing | public distribution only | Founder (paid, optional) | F-19 |
