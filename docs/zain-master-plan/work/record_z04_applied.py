"""Record the applied Z-04 reconciliation. Run from docs/zain-master-plan; argv[1] = PR state counts, argv[2] = UTC time."""
import csv, io, pathlib, sys
sys.path.insert(0, 'tools'); sys.dont_write_bytecode = True
from zmp import SCHEMAS
PRS, T = sys.argv[1], sys.argv[2]

def rep(f, pairs):
    p = pathlib.Path(f); t = p.read_text(encoding='utf-8')
    for a, b in pairs:
        if t.count(a) != 1: sys.exit(f'NOT UNIQUE/MISSING {f}: {a[:70]}')
        t = t.replace(a, b)
    p.write_text(t, encoding='utf-8'); print('edited', f)

rep('21-BRANCH-PR-RECONCILIATION.md', [
    ("STATUS   = PROPOSAL. Nothing has been closed, deleted or tagged. Each group in §5 is applied only after the founder\n           approves it",
     f"STATUS   = APPLIED {T} after the founder approved all groups in chat (\"Yes, apply all\"); results in §6"),
])
p = pathlib.Path('21-BRANCH-PR-RECONCILIATION.md')
p.write_text(p.read_text(encoding='utf-8').rstrip('\n') + f'''

## 6. Applied ({T})

The founder approved every group in chat on 2026-11-08. `work/z04_apply.py` re-checked that no branch had moved since
the inventory, then ran its stages in order:

| Stage | Result | Evidence |
|---|---|---|
| Manifest | 352 branches with full SHAs, committed before any change (`f3cb77f`) | `work/z04_applied_manifest.csv` |
| Archive tags | 34 `archive/<branch>` tags pushed; all 34 match the manifest SHA on the remote | `git ls-remote origin 'refs/tags/archive/*'` |
| PRs closed | #1, #73, #81, #88, #136, #159, #162, #164, #342, #343, #346, #347, each with a comment pointing here | `gh pr list --state all`: {PRS} |
| Branches deleted | 348 of 348 (A 187, B 117, C 34 after their tags verified, D 10); none failed | `git ls-remote --heads` |
| Remaining branches | `main`, `docs/v3-unified-replan-20261027`, `docs/r0a-opus-start-20261102`, `docs/zain-master-plan-20261108`, `codex/astro-c01-s3-contracts-20260921` | same |
| CI | No workflow ran: no workflow triggers on tags, branch deletion or PR close | `gh run list` |

**Restoring a branch:** `git push origin <full_sha>:refs/heads/<branch>`, with the SHA from the manifest. A branch
from a closed PR can also be restored with the PR page's "Restore branch" button. Group C commits stay reachable
through their archive tags.

The verification stage first reported 0 of 34 tags matched; that was a key-prefix bug in the check, not in the tags.
It was fixed and re-verified (34 of 34) before any branch was deleted.
''', encoding='utf-8'); print('appended §6')
rep('17-MASTER-PLAN-STATUS.md', [("Salvage notes for #342 (into V3 09 §3) and #73 (into Design Studio) are written. Nothing is applied until the\nfounder approves.",
    "Salvage notes for #342 (into V3 09 §3) and #73 (into Design Studio) are written. Nothing is applied until the\nfounder approves.\n\n"
    f"**2026-11-08, Z-04 applied.** The founder approved all groups. The 12 open PRs are closed; 34 archive tags were\n"
    f"pushed and verified; 348 branches were deleted after a full-SHA manifest was committed (21 §6). Five branches remain:\n"
    f"main, the three nested planning branches and #343's reference branch. No CI ran. Z-04 is DONE_UNREVIEWED.")])

def load(n): return list(csv.DictReader(open('registry/' + n, encoding='utf-8')))
def save(n, rows):
    o = io.StringIO(); w = csv.DictWriter(o, fieldnames=SCHEMAS[n], lineterminator='\n'); w.writeheader(); w.writerows(rows)
    open('registry/' + n, 'w', encoding='utf-8').write(o.getvalue()); print('saved', n)
B = load('zain-task-backlog.csv')
for r in B:
    if r['id'] == 'Z-04':
        r['status'] = 'DONE_UNREVIEWED'
        r['status_evidence'] = (f'21-BRANCH-PR-RECONCILIATION.md §6 ({T}): founder-approved; 12 PRs closed, 34 archive tags verified, 348 branches deleted '
                                f'after a full-SHA manifest (f3cb77f); 5 branches remain; PR states {PRS}')
        r['blockers'] = ''
save('zain-task-backlog.csv', B)
