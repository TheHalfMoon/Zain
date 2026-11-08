import csv, io, pathlib, sys
sys.path.insert(0, 'tools'); sys.dont_write_bytecode = True
from zmp import SCHEMAS

def load(n): return list(csv.DictReader(open('registry/' + n, encoding='utf-8')))
def save(n, rows):
    out = io.StringIO(); w = csv.DictWriter(out, fieldnames=SCHEMAS[n], lineterminator='\n'); w.writeheader(); w.writerows(rows)
    open('registry/' + n, 'w', encoding='utf-8').write(out.getvalue())

B = load('zain-task-backlog.csv')
for r in B:
    if r['id'] == 'Z-03':
        r['status'] = 'DONE_UNREVIEWED'
        r['status_evidence'] = ('18-EXPOSURE-ASSESSMENT.md (2026-11-08): all refs of both repos, PR/issue text, 4,186 comments, both artifacts and 20 sampled logs scanned; '
                                '0 live credentials; personal data P1-P3 dispositioned; founder acceptance pending (DEC-16)')
save('zain-task-backlog.csv', B)
G = load('zain-acceptance-gates.csv')
for g in G:
    if g['gate_id'] == 'GATE-PRIV-03':
        g['evidence'] = '18-EXPOSURE-ASSESSMENT.md: 0 live credentials; every hit dispositioned; stays NOT_MET until the founder accepts the P1-P3 dispositions (DEC-16)'
save('zain-acceptance-gates.csv', G)
R = load('zain-risk-register.csv')
for r in R:
    if r['risk_id'] == 'RK-01':
        r['evidence'] += '; Z-03 found no live credential, but founder email (1,482 + 72 commits) and Windows username were public'
save('zain-risk-register.csv', R)

def rep(f, pairs):
    p = pathlib.Path(f); t = p.read_text(encoding='utf-8')
    for a, b in pairs:
        if a not in t: sys.exit(f'MISSING {f}: {a[:60]}')
        t = t.replace(a, b)
    p.write_text(t, encoding='utf-8'); print('edited', f)

rep('13-RISKS-AND-OPEN-DECISIONS.md', [
    ('DECISIONS = DEC-01..DEC-15 below;', 'DECISIONS = DEC-01..DEC-16 below;'),
    ('| DEC-15 | Update feed (F-04) hosting and signing-key custody |',
     '| DEC-16 | Response to the historical exposure found by Z-03 (18) | Accept the commit-email exposure and switch to the GitHub noreply address with email privacy settings; rewrite history (invalidates every SHA, branch and PR reference); do nothing | Accept and switch to noreply now; make or archive wepld/wepld private; identify the two other wepld identities | GATE-PRIV-03 | — |\n| DEC-15 | Update feed (F-04) hosting and signing-key custody |'),
])
rep('README.md', [
    ('| [17-MASTER-PLAN-STATUS.md](17-MASTER-PLAN-STATUS.md) | Canonical status and session handoff log |',
     '| [17-MASTER-PLAN-STATUS.md](17-MASTER-PLAN-STATUS.md) | Canonical status and session handoff log |\n| [18-EXPOSURE-ASSESSMENT.md](18-EXPOSURE-ASSESSMENT.md) | Z-03 public-exposure assessment of both repositories |'),
    ('| [13-RISKS-AND-OPEN-DECISIONS.md](13-RISKS-AND-OPEN-DECISIONS.md) | Risks and founder decisions DEC-01..DEC-15 |',
     '| [13-RISKS-AND-OPEN-DECISIONS.md](13-RISKS-AND-OPEN-DECISIONS.md) | Risks and founder decisions DEC-01..DEC-16 |'),
])
rep('17-MASTER-PLAN-STATUS.md', [
    ('| Founder decisions | OPEN: DEC-01..DEC-15 | 13 §2 |', '| Founder decisions | OPEN: DEC-01..DEC-16 | 13 §2 |'),
    ('The plan branch was then pushed; no workflow runs on non-main branch pushes and no PR was opened.',
     'The plan branch was then pushed; no workflow runs on non-main branch pushes and no PR was opened.\n\n**2026-11-08, Z-03.** Public-exposure assessment done (18): no live credential in either repository; the founder\'s\npersonal email (1,482 Zain and 72 wepld commits) and Windows username were public; wepld/wepld still exposes them.\nZ-03 is DONE_UNREVIEWED; GATE-PRIV-03 waits for the founder\'s DEC-16.'),
    ('| GATE-PLAN-02 | MET in substance (35/35), recorded NOT_MET until Z-05 review | 15 §2 |',
     '| GATE-PLAN-02 | MET in substance (35/35), recorded NOT_MET until Z-05 review | 15 §2 |\n| GATE-PRIV-03 | 0 live credentials, all hits dispositioned; waits for founder DEC-16 | 18 |'),
])
