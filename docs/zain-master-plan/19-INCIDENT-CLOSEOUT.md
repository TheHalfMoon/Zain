# 19 — Deletion and Disk-Incident Close-out (task Z-18)

```text
DATE     = 2026-11-08
SCOPE    = the OneDrive checkout %USERPROFILE%\OneDrive\Desktop\wepld (origin wepld/wepld), its registered worktrees,
           the 2026-10-28 disk incident in the V3 ledger, the 2026-11-08 disk-full event, usn-journal.csv
METHOD   = read-only commands; each finding below cites the command and its output. Paths use %USERPROFILE%
VERDICT  = no committed work was lost except possibly 1 local-only commit (still present); uncommitted work in the
           checkout and 10 sibling worktrees is gone; OneDrive did not propagate the deletion (sync idle since June);
           the agent itself destroyed forensic metadata on 2026-11-08 (§4)
```

## 1. Timeline (UTC)

| When | Event | Evidence |
|---|---|---|
| 2026-06-26 | Last OneDrive personal sync-engine log; sync has not run since | newest file in `%LOCALAPPDATA%\Microsoft\OneDrive\logs\Personal` is `SyncEngine-2026-06-26…aodl`; no `OneDrive.exe` process (only `OneDrive.Sync.Service.exe`) |
| 2026-07-17T22:40Z | Last commit in the checkout (`d5ef318`, branch `feat/build-feature-engineering-memory`); the index has not been written since | `git log -1`; `.git/index` mtime 2026-07-17T22:40:32Z |
| 2026-08-11T23:59Z | A git object write stopped part-way (0-byte temp object) | `fsck`: garbage `objects/36/tmp_obj_w4r2M8`, 0 bytes |
| 2026-09-05T23:07Z | Last fetch | `.git/FETCH_HEAD` and `objects/pack` mtimes |
| 2026-09-14T06:56Z | A second object write stopped part-way (4,447-byte temp object) | `fsck`: garbage `objects/b5/tmp_obj_wyZSBH` |
| 2026-09-17T04:21Z | Empty `New folder` created at the checkout root | directory mtime, 0 entries |
| 2026-09-20T02:54Z – 2026-09-21T19:32Z | Nine `.astro-*` folders created inside the checkout: one clone of TheHalfMoon/wepld (now renamed TheHalfMoon/Zain) and eight worktrees of it, 238–781 files each | `ls`; `.astro-plan-20260920` remote `TheHalfMoon/wepld.git`; `gh api repos/TheHalfMoon/wepld` returns `TheHalfMoon/Zain` |
| between 2026-07-17T22:40Z and 2026-09-21T19:32Z | All 175 tracked files (all 13 top-level tracked entries) removed from the working tree | `git ls-files --deleted` = 175 of 175; checkout folder mtime 2026-09-21T19:32:21Z (its last entry change, the `.astro-v72` creation) |
| before 2026-11-08 | Ten sibling worktree folders on the Desktop (`wepld-adr-foundation-decisions`, `-capability-portfolio`, `-closeout`, `-committee`, `-plan`, `-pre-h1-evaluation-package-a`, `-proprietary-ip`, `-s05a`, `-s0a`, and one not captured) no longer exist | `git worktree list`: 11 registered, 10 `prunable` |
| 2026-10-27T21:26Z | V3 ledger records "local disk filled by donor clones; clones deleted; founder instruction: nothing saved locally, only in repo" | `STATUS_LEDGER.md:90`, commit `be6e950` |
| 2026-11-07T22:29Z | `.git` touched, most likely by the audit session's `git status` | `.git` mtime before §4 |
| 2026-11-08, about 00:50Z | C: fell to 35 MB free during Z-03 while `cargo test --locked -p orcel-provider-git` (2 `cargo.exe`), 24 `python.exe` and 7 `node.exe` ran | `(Get-PSDrive C).Free` = 35,205,120; process list |
| 2026-11-08, about 01:05Z | Founder freed space: C: 24 GB free; it fell again to 19.7 GB by 01:35Z while the other work continued | `df`; `Get-PSDrive` |
| 2026-11-08T01:38Z | The agent's `git fetch --dry-run` in the checkout removed the 10 stale worktree records (§4) | `.git` mtime 2026-11-08T01:38:06Z; `.git/worktrees` absent right after |

No Windows low-disk events (System log, ID 2013) were recorded in the last 45 days. That event may not be emitted on
this edition, so its absence does not show that the disk never filled.

## 2. What is recoverable

| Item | State | Evidence |
|---|---|---|
| The 175 deleted tracked files at `d5ef318` | **Fully recoverable** from the local object store and from GitHub | `git fsck --connectivity-only` exit 0; `gh api repos/wepld/wepld/commits/d5ef318` found |
| Commits on the 12 local branches | 11 branches are on GitHub or fully reachable from remote refs. **1 commit on `docs/pre-h1-evaluation-protocol-fixture-registry` exists only in this local `.git`** | `ls-remote` plus `rev-list --count <branch> --not --remotes` |
| 3 dangling blobs (746 B, 9.5 KB, 236 KB) | Readable with `git cat-file`; content not inspected | `fsck`; `cat-file -s` |
| Uncommitted or untracked work in the checkout and in the 10 missing worktrees | **Not recoverable from git.** The Recycle Bin is empty | Shell.Application namespace 10: 0 items |
| OneDrive cloud copy | Possibly a copy as of 2026-06-26 or earlier, which predates the July commits. Not checked (needs a browser sign-in) | §1 first row |
| Temp objects from the interrupted writes | Not recoverable (partial) | `fsck` |

## 3. Root-cause hypotheses

| # | Hypothesis | For | Against or unknown |
|---|---|---|---|
| H1 | A tool or agent deleted the tracked tree at the filesystem level, not through git, probably while the `.astro-*` work used this folder as its scratch root | Index unchanged since July (git did not do it); whole top-level entries gone with no leftover directories (a recursive delete); the `.astro-*` folders are the only additions in that window | Exact time and actor unknown; no shell history or USN data |
| H2 | The ten sibling worktrees were removed by deleting their folders instead of `git worktree remove` | They were registered but missing (`prunable`) | Dates unknown; the records are gone (§4) |
| H3 | Disk pressure interrupted git writes | Two partial object writes (2026-08-11, 2026-09-14); disk-full episodes on 2026-10-28 and 2026-11-08 | No low-disk events logged; a killed process would leave the same trace |
| — | OneDrive sync propagated a deletion | — | **Ruled out:** the sync engine has not run since 2026-06-26 |

## 4. Evidence the agent destroyed during this task

At 01:38Z the agent ran `git fetch --dry-run` in the checkout to compare branches. Git's automatic maintenance, which
runs after a fetch, then removed the ten `prunable` worktree records (`.git/worktrees/<name>/`). The records existed
in the preceding command and were absent in the next; `.git` was last modified at 01:38:06Z. Git 2.56.0 is installed;
the exact maintenance task was not confirmed from the documentation (no local copy).

- **Lost:** each missing worktree's `gitdir` pointer, `HEAD`, index and per-worktree reflog. These timestamps could have
  dated when each worktree was last used.
- **Not lost:** branches and commits (they live in the shared `refs` and objects); the worktree folders themselves
  were already gone.
- **Kept:** nine of the ten worktree names, their branches and tip SHAs, captured in §1 before the change.
- **Fix:** requirement R4 below. Later commands used `-c maintenance.auto=false -c gc.auto=0` and no fetch.

## 5. Requirements handed to Z-19

| # | Requirement | Source |
|---|---|---|
| R1 | Capacity preflight before clones and builds, and a running check during long jobs: stop and report below a reserve (GATE-RES-01), because other work on the machine can consume space mid-run | 2026-10-28 and 2026-11-08 events |
| R2 | Recursive deletes inside a git checkout that would remove tracked files go to a recoverable quarantine and need confirmation | H1 |
| R3 | Detect synced folders (OneDrive known folders) and refuse to use them as agent work roots; warn that resuming sync after local deletions propagates them to the cloud | §2 OneDrive row |
| R4 | Read-only git inspection runs with `-c maintenance.auto=false -c gc.auto=0` and never fetches or pulls | §4 |
| R5 | Agent-created worktrees live in one non-synced directory, are listed in a manifest, and are removed with `git worktree remove`, never by deleting the folder | H2 |
| R6 | Incident evidence is stored with the incident note in the repository, not cited from elsewhere | `usn-journal.csv` (§6) |

## 6. Open questions for the founder

1. **`usn-journal.csv`:** not found. A filename search of all of C: and D: (`dir /s /b /a-d *usn*.csv`, 2026-11-08 01:35Z, completed) returned no match; folders that need administrator rights were skipped
2. **OneDrive:** before OneDrive sync is ever resumed, check the `Desktop/wepld` folder on OneDrive online. Resuming
   sync would apply the local deletions to the cloud copy.
3. **The local-only commit** on `docs/pre-h1-evaluation-protocol-fixture-registry`: push it to wepld/wepld (the
   founder's rule is that everything lives in the repository) or let it go.
4. **Intent:** was the checkout emptied on purpose while moving work to TheHalfMoon/wepld (now Zain)? If so, H1 is
   expected cleanup, and only the loss of uncommitted work remains a finding.
