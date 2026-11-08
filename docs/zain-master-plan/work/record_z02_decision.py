"""Record the founder's Z-02 decision: remove Zain from all 10 apps (2026-11-08). Run from docs/zain-master-plan."""
import csv, io, pathlib, sys
sys.path.insert(0, 'tools'); sys.dont_write_bytecode = True
from zmp import SCHEMAS

def rep(f, pairs):
    p = pathlib.Path(f); t = p.read_text(encoding='utf-8')
    for a, b in pairs:
        if t.count(a) != 1: sys.exit(f'NOT UNIQUE/MISSING {f}: {a[:70]}')
        t = t.replace(a, b)
    p.write_text(t, encoding='utf-8'); print('edited', f)

rep('22-APP-EGRESS-INVENTORY.md', [
    ("STATUS   = inventory done; app changes wait for the founder (§4); the scratch-push check follows them (§5)",
     "STATUS   = inventory done; founder decided 2026-11-08 to remove Zain from all 10 apps (§4); the founder makes the\n           change in GitHub settings, then the scratch-push check runs (§5)"),
    ("## 4. Proposed founder actions", "## 4. Founder actions\n\n**Decided 2026-11-08 (founder, in chat): remove Zain from all 10 apps, CodeRabbit included; no gate exception.**"),
])
rep('17-MASTER-PLAN-STATUS.md', [("remove Zain from the apps (22 §4), then a scratch-push check (22 §5).",
    "remove Zain from the apps (22 §4), then a scratch-push check (22 §5). The founder decided to remove all 10, CodeRabbit\n"
    "included (2026-11-08); the change is the founder's to make in GitHub settings.")])

def load(n): return list(csv.DictReader(open('registry/' + n, encoding='utf-8')))
def save(n, rows):
    o = io.StringIO(); w = csv.DictWriter(o, fieldnames=SCHEMAS[n], lineterminator='\n'); w.writeheader(); w.writerows(rows)
    open('registry/' + n, 'w', encoding='utf-8').write(o.getvalue()); print('saved', n)
B = load('zain-task-backlog.csv')
for r in B:
    if r['id'] == 'Z-02':
        r['status_evidence'] += '; founder decided 2026-11-08: remove Zain from all 10 apps, no CodeRabbit exception'
        r['blockers'] = 'Founder removes Zain from the 10 apps in GitHub settings (22 §4); then the scratch-push check (22 §5)'
save('zain-task-backlog.csv', B)
