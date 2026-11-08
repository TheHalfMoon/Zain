"""Record the Z-04 proposal (21-BRANCH-PR-RECONCILIATION.md). Run from docs/zain-master-plan."""
import csv, io, pathlib, sys
sys.path.insert(0, 'tools'); sys.dont_write_bytecode = True
from zmp import SCHEMAS

def rep(f, pairs):
    p = pathlib.Path(f); t = p.read_text(encoding='utf-8')
    for a, b in pairs:
        if t.count(a) != 1: sys.exit(f'NOT UNIQUE/MISSING {f}: {a[:70]}')
        t = t.replace(a, b)
    p.write_text(t, encoding='utf-8'); print('edited', f)

rep('README.md', [('| [work/](work/README.md) |',
    '| [21-BRANCH-PR-RECONCILIATION.md](21-BRANCH-PR-RECONCILIATION.md) | Z-04 branch and PR dispositions and salvage notes (proposal) |\n| [work/](work/README.md) |')])
rep('17-MASTER-PLAN-STATUS.md', [("Q-01 waits only on disk (Z-07) and free RAM.",
    "Q-01 waits only on disk (Z-07) and free RAM.\n\n"
    "**2026-11-08, Z-04 proposal.** Every one of the 352 non-main branches and 12 open PRs has a proposed disposition\n"
    "(21): delete 187 merged and 117 closed-PR branches, archive 34 no-PR branches as tags then delete them, close the 12\n"
    "open PRs (keeping #343's branch as reference), keep the 3 nested planning branches until one merge at G-03.\n"
    "Salvage notes for #342 (into V3 09 §3) and #73 (into Design Studio) are written. Nothing is applied until the\n"
    "founder approves.")])
rep('work/README.md', [('| `record_*.py` |',
    '| `z04_inventory.py`, `z04_dispositions.py`, `z04_branches.csv` | Z-04: branch and PR inventory with a proposed disposition per branch (21) |\n| `record_*.py` |')])

def load(n): return list(csv.DictReader(open('registry/' + n, encoding='utf-8')))
def save(n, rows):
    o = io.StringIO(); w = csv.DictWriter(o, fieldnames=SCHEMAS[n], lineterminator='\n'); w.writeheader(); w.writerows(rows)
    open('registry/' + n, 'w', encoding='utf-8').write(o.getvalue()); print('saved', n)
B = load('zain-task-backlog.csv')
for r in B:
    if r['id'] == 'Z-04':
        r['status'] = 'IN_PROGRESS'
        r['status_evidence'] = ('21-BRANCH-PR-RECONCILIATION.md (2026-11-08): dispositions for all 352 non-main branches (79 updated since 2026-09-01) '
                                'and all 12 open PRs; salvage notes for #342 and #73; planning merge path. Application awaits founder approval')
        r['blockers'] = 'Founder approval of groups A-E and the PR closures (21 §5)'
save('zain-task-backlog.csv', B)
