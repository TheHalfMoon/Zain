"""Record Z-18 (19-INCIDENT-CLOSEOUT.md). Run from docs/zain-master-plan; argv[1] = usn search result sentence."""
import csv, io, pathlib, sys
sys.path.insert(0, 'tools'); sys.dont_write_bytecode = True
from zmp import SCHEMAS
USN = sys.argv[1]

def rep(f, pairs):
    p = pathlib.Path(f); t = p.read_text(encoding='utf-8')
    for a, b in pairs:
        if t.count(a) != 1: sys.exit(f'NOT UNIQUE/MISSING {f}: {a[:70]}')
        t = t.replace(a, b)
    p.write_text(t, encoding='utf-8'); print('edited', f)

rep('19-INCIDENT-CLOSEOUT.md', [('USN_SEARCH_RESULT', USN)])
rep('13-RISKS-AND-OPEN-DECISIONS.md', [('**Founder, 2026-11-08 (DEC-10):** location not known; treated as not found.',
    '**Founder, 2026-11-08 (DEC-10):** location not known; treated as not found. **Z-18:** ' + USN + ' (19 §6)')])
rep('00-EXECUTIVE-SUMMARY.md', [
    ('**Ready now:** M0, plus the read-only agent task Z-18 (Z-03 is done, unreviewed).',
     '**Ready now:** the M0 agent tasks are done (Z-03 and Z-18, unreviewed); next is Q-00.'),
    ('- **Founder:** Z-25 (the six decisions above), Z-06 and Z-01. Each takes minutes.',
     '- **Founder:** Z-25 is recorded and Z-01 is not needed; Z-06 (OCR set up for one dry-run review) remains.'),
    ('- **Agent, now:** **Z-03**, the public-exposure assessment (read-only), together with Z-18.',
     '- **Agent:** Z-03 and Z-18 are done, unreviewed (18, 19).'),
])
rep('README.md', [('| [work/](work/README.md) |',
    '| [19-INCIDENT-CLOSEOUT.md](19-INCIDENT-CLOSEOUT.md) | Z-18 deletion and disk-incident close-out |\n| [work/](work/README.md) |')])
rep('17-MASTER-PLAN-STATUS.md', [('and DEC-03 is moot while public.',
    'and DEC-03 is moot while public.\n\n'
    '**2026-11-08, Z-18.** Incident close-out done (19). All 175 deleted files in the OneDrive wepld checkout are\n'
    'recoverable from git and GitHub; one commit exists only locally; uncommitted work in the checkout and ten sibling\n'
    'worktrees is gone; OneDrive sync has been idle since 2026-06-26, so it did not spread the deletion. The agent\'s own\n'
    '`git fetch --dry-run` pruned ten stale worktree records (19 §4); requirement R4 prevents a repeat. Z-18 is\n'
    'DONE_UNREVIEWED; requirements R1-R6 go to Z-19.')])

def load(n): return list(csv.DictReader(open('registry/' + n, encoding='utf-8')))
def save(n, rows):
    out = io.StringIO(); w = csv.DictWriter(out, fieldnames=SCHEMAS[n], lineterminator='\n'); w.writeheader(); w.writerows(rows)
    open('registry/' + n, 'w', encoding='utf-8').write(out.getvalue()); print('saved', n)
B = load('zain-task-backlog.csv')
for r in B:
    if r['id'] == 'Z-18':
        r['status'] = 'DONE_UNREVIEWED'
        r['status_evidence'] = ('19-INCIDENT-CLOSEOUT.md (2026-11-08): timeline, recoverability, OneDrive (idle since 2026-06-26, did not propagate), '
                                'hypotheses H1-H3, requirements R1-R6 for Z-19; agent-caused pruning of 10 stale worktree records disclosed (19 §4)')
    if r['id'] == 'Z-19' and '19-INCIDENT-CLOSEOUT.md' not in r['deliverables']:
        r['deliverables'] += '; covers requirements R1-R6 of 19-INCIDENT-CLOSEOUT.md §5'
save('zain-task-backlog.csv', B)
R = load('zain-risk-register.csv')
for r in R:
    if r['risk_id'] == 'RK-21':
        r['evidence'] = (r['evidence'] + '; ' if r['evidence'] else '') + 'Z-18 (19): deletion dated 2026-07-17..2026-09-21, not via git or OneDrive; committed work recoverable; R1-R6 to Z-19'
save('zain-risk-register.csv', R)
