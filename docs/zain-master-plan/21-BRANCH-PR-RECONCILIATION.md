# 21 — Branch and Pull-Request Reconciliation (task Z-04), proposal

```text
DATE     = 2026-11-08
TASK     = Z-04 (AGENT+FOUNDER): a disposition for every open PR and every non-main branch, salvage notes for #342 and
           #73, and a merge path for the planning branches
STATUS   = APPLIED 2026-11-08T02:32Z after the founder approved all groups in chat ("Yes, apply all"); results in §6
METHOD   = read-only: work/z04_inventory.py (remote-tracking refs, checked equal to `git ls-remote`, plus the PR list
           API) and work/z04_dispositions.py. Every branch and its proposed action: work/z04_branches.csv
```

## 1. Inventory

| Item | Count |
|---|---|
| Branches | 353: `main` and 352 others |
| Pull requests | 332: 12 open, 185 merged, 135 closed unmerged |
| Branches updated since 2026-09-01 | 79, all with a disposition below |

| Branch class | All | Since 2026-09-01 |
|---|---|---|
| A. Fully merged into `main` (tip is an ancestor of `main`) | 187 | 64 |
| B. Last PR closed without merging | 117 | 7 |
| C. No PR, with commits found nowhere else | 34 | 1 |
| D. Open PR | 11 | 4 |
| E. Planning branches | 3 | 3 |

The branch of the twelfth open PR, #1, is already fully merged and is counted in A.

## 2. Open pull requests

| PR | Proposal | Reason |
|---|---|---|
| #1 fresh foundation | Close | Superseded by #2 (merged 2026-08-15); its branch is already in `main` |
| #73 JetBrains browser visual-edit research | Close after the §4 salvage note lands | Research only; the useful parts move to Design Studio |
| #81, #88 MiniMax universal agent | Close | #88 replaces #81; neither is a V3 source |
| #136 Pictorial/Agile vendor import (+1.63M lines) | Close | Contradicts "no donor transplant in Zain"; the branch is deleted separately (group D) |
| #159, #162, #164 | Close | Repairs for #136; #164 adds a retired policy successor |
| #342 ASTRO-B01 benchmark preregistration | Close after the §3 salvage note lands in V3 09 | Its protocol rules are worth keeping; its arms belong to the retired design |
| #343 S3 contract surface (+1,791 Rust) | Close; keep the branch as reference until the Core C-0x chain starts | Adds Core code outside V3 gates; ProcessHost ownership moved to C-25 / ADR-024 |
| #346 source expansion | Close as superseded | Its task IDs collide with V3's namespaces |
| #347 Graft context layer | Close | Tool not admitted; conflicts with governed `AGENTS.md` changes |

## 3. Salvage note: #342 (ASTRO-B01) into V3 09 §3

V3 09 §3 already defines benchmarks B1–B13, but B7 (real task completion, Zain vs T3) and B8 (retention across a
model switch) lack a preregistration discipline. Carry these rules from ASTRO-B01 into those rows before either runs:

1. **Route identity freeze.** For every arm and comparison, record the exact model identifier and revision, provider,
   harness name, version and configuration digest, and tool or permission set digest. A change makes the comparison
   void.
2. **Primary measure.** The share of tasks independently accepted against preregistered outcome criteria with zero
   unauthorized effects. Secondary measures: severity-weighted regressions, false completion (claimed done while
   criteria are unmet), coverage omissions, human review minutes, wall time, tokens.
3. **Contamination control.** A held-out task set kept blind and disjoint from the visible set; private or canary
   workloads are never published. Record whether each task or fixture is publicly available.
4. **Stopping rules, frozen before the first run.** The same attempt limit and per-task budget ceiling for every arm,
   a global budget ceiling, a cancellation policy, and an immediate stop on any unauthorized effect.
5. **Negative check (from B01-NEG-1).** The report generator must refuse a comparison whose baseline is missing or
   incomplete, or whose model changed between arms, and report it as not comparable.

Not carried: the arm definitions (A–…), which encode the retired AGILLE/MUSE pipeline, and the S3-D slice bookkeeping.

## 4. Salvage note: #73 (JetBrains research) into Design Studio and the browser lanes

For the V3 Design Studio work (03B, D-01..D-08) and the R2 browser lanes. The research is discovery only: the
founder-reported permission to reuse JetBrains source is not stored or verified per source, so any code reuse needs a
per-source license admission in the source registry first.

- **Behaviors to adopt as requirement candidates:** point at a real rendered element; browser-to-source highlighting
  both ways; multi-select and relational instructions; accessibility identity beside DOM identity; exact viewport,
  geometry and screenshot context; hot reload with an explicit reload fallback; resolution to source component,
  symbol and usages; isolated candidate workspaces for material edits; reversible checkpoints before git.
- **Rejected for now:** a wholesale IntelliJ Platform transplant; a JVM only to embed a browser; treating XPath or CSS
  locators as durable source identity; editing source the moment an element is selected; model choice as effect
  authority; a design score as the acceptance verdict; visual gains that regress accessibility or function; automatic
  external-review egress; exposing every tool to every agent.
- **Failure checks to keep:** a DOM node with no unique source mapping; one component rendering many identical nodes;
  one node composed from several components; a stale source map after hot reload; a generated file selected instead
  of the true source; shadow DOM; cross-origin iframes; an element that disappears between selection and action;
  layout that moves between screenshot and geometry capture.
- **Mechanisms worth studying:** JCEF/JBCef browser lifecycle and bridge; Remote Driver `JCefUI` DOM automation;
  WebStorm Live Edit, Actual DOM and Web Inspector; Local History (`lvcs`); ACP; the JetBrains MCP Server's per-tool
  enablement; Qodana's baseline and SARIF quality gate.

## 5. Branch actions for approval

| Group | Branches | Proposed action | Recoverability |
|---|---|---|---|
| A | 187 | Delete | Content is in `main`; merged PRs keep their refs |
| B | 117 | Delete | Each PR keeps its head at `refs/pull/<n>/head`; the PR page can restore the branch |
| C | 34 | Create tag `archive/<branch>` at the tip, then delete the branch | The tag keeps every commit |
| D | 11 | Close the PR per §2, then delete the branch; keep #343's branch for now | PR refs keep the heads |
| E | 3 | Keep. `docs/v3-unified-replan-20261027` ⊂ `docs/r0a-opus-start-20261102` ⊂ `docs/zain-master-plan-20261108` | — |

**Planning-branch merge path (E).** One PR from `docs/zain-master-plan-20261108` into `main` carries all three. Under
DEC-09 and DEC-11 it waits until G-03 replaces the governance chain at R0, so no v73 policy successor is needed. After
it merges, the two contained branches are deleted.

Applying an approved group uses `gh pr close <n> --comment …`, `git tag archive/<b> <sha>` and `git push origin
archive/<b>`, and `git push origin --delete <b>`. Afterwards `gh pr list --state all` and `git ls-remote` are recorded
here as evidence.

## 6. Applied (2026-11-08T02:32Z)

The founder approved every group in chat on 2026-11-08. `work/z04_apply.py` re-checked that no branch had moved since
the inventory, then ran its stages in order:

| Stage | Result | Evidence |
|---|---|---|
| Manifest | 352 branches with full SHAs, committed before any change (`f3cb77f`) | `work/z04_applied_manifest.csv` |
| Archive tags | 34 `archive/<branch>` tags pushed; all 34 match the manifest SHA on the remote | `git ls-remote origin 'refs/tags/archive/*'` |
| PRs closed | #1, #73, #81, #88, #136, #159, #162, #164, #342, #343, #346, #347, each with a comment pointing here | `gh pr list --state all`: closed 147, merged 185 |
| Branches deleted | 348 of 348 (A 187, B 117, C 34 after their tags verified, D 10); none failed | `git ls-remote --heads` |
| Remaining branches | `main`, `docs/v3-unified-replan-20261027`, `docs/r0a-opus-start-20261102`, `docs/zain-master-plan-20261108`, `codex/astro-c01-s3-contracts-20260921` | same |
| CI | No workflow ran: no workflow triggers on tags, branch deletion or PR close | `gh run list` |

**Restoring a branch:** `git push origin <full_sha>:refs/heads/<branch>`, with the SHA from the manifest. A branch
from a closed PR can also be restored with the PR page's "Restore branch" button. Group C commits stay reachable
through their archive tags.

The verification stage first reported 0 of 34 tags matched; that was a key-prefix bug in the check, not in the tags.
It was fixed and re-verified (34 of 34) before any branch was deleted.
