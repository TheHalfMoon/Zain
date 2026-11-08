"""Record the Z-02 inventory (22-APP-EGRESS-INVENTORY.md). Run from docs/zain-master-plan."""
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
    '| [22-APP-EGRESS-INVENTORY.md](22-APP-EGRESS-INVENTORY.md) | Z-02 inventory of third-party apps with repository access |\n| [work/](work/README.md) |')])
rep('17-MASTER-PLAN-STATUS.md', [("No CI ran. Z-04 is DONE_UNREVIEWED.",
    "No CI ran. Z-04 is DONE_UNREVIEWED.\n\n"
    "**2026-11-08, Z-02 inventory.** No webhooks, deploy keys, Actions secrets, rulesets or deployments. Ten GitHub Apps\n"
    "hold repository access (22): CodeRabbit and cubic have automatic review OFF in repository config; Qodo is paused by\n"
    "billing; Cursor, Devin, Graphite, Greptile, Sentry, Vercel and Claude have no documented OFF state. Five plan pushes\n"
    "during today's private window created queued (never run) suites for five of them. GATE-PRIV-02 needs the founder to\n"
    "remove Zain from the apps (22 §4), then a scratch-push check (22 §5).")])

def load(n): return list(csv.DictReader(open('registry/' + n, encoding='utf-8')))
def save(n, rows):
    o = io.StringIO(); w = csv.DictWriter(o, fieldnames=SCHEMAS[n], lineterminator='\n'); w.writeheader(); w.writerows(rows)
    open('registry/' + n, 'w', encoding='utf-8').write(o.getvalue()); print('saved', n)
B = load('zain-task-backlog.csv')
for r in B:
    if r['id'] == 'Z-02':
        r['status'] = 'IN_PROGRESS'
        r['status_evidence'] = ('22-APP-EGRESS-INVENTORY.md (2026-11-08): inventory done; 10 apps with access, 2 with automatic review OFF in config '
                                '(CodeRabbit, cubic), Qodo paused by billing, 7 undocumented; no webhooks, deploy keys, secrets or deployments')
        r['blockers'] = 'Founder removes Zain from the apps (22 §4); then the scratch-push check (22 §5) with founder go-ahead'
save('zain-task-backlog.csv', B)
G = load('zain-acceptance-gates.csv')
for g in G:
    if g['gate_id'] == 'GATE-PRIV-02':
        g['evidence'] = '22-APP-EGRESS-INVENTORY.md (2026-11-08): 10 apps with access, 8 without a documented OFF state; check suites on every push. NOT_MET'
save('zain-acceptance-gates.csv', G)
