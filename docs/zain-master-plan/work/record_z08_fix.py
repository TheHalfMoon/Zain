"""Fix: Z-08 cannot be DONE while its prerequisite Z-07 is open (E-DONE-BEFORE-DEPS). Run from docs/zain-master-plan."""
import csv, io, pathlib, sys
sys.path.insert(0, 'tools'); sys.dont_write_bytecode = True
from zmp import SCHEMAS
def load(n): return list(csv.DictReader(open('registry/' + n, encoding='utf-8')))
def save(n, rows):
    o = io.StringIO(); w = csv.DictWriter(o, fieldnames=SCHEMAS[n], lineterminator='\n'); w.writeheader(); w.writerows(rows)
    open('registry/' + n, 'w', encoding='utf-8').write(o.getvalue()); print('saved', n)
B = load('zain-task-backlog.csv')
for r in B:
    if r['id'] == 'Z-08':
        r['status'] = 'IN_PROGRESS'
        r['status_evidence'] = 'Deliverables complete; stays IN_PROGRESS until prerequisite Z-07 (build-volume capacity) closes. ' + r['status_evidence']
save('zain-task-backlog.csv', B)
G = load('zain-acceptance-gates.csv')
for g in G:
    if g['gate_id'] == 'GATE-TOOL-01':
        g['evidence'] = g['evidence'].replace('recorded NOT_MET until Z-08 is reviewed', 'recorded NOT_MET until Z-07 and Z-08 close')
save('zain-acceptance-gates.csv', G)
p = pathlib.Path('17-MASTER-PLAN-STATUS.md'); t = p.read_text(encoding='utf-8')
a = 'recorded NOT_MET until Z-08 review |'
if t.count(a) != 1: sys.exit('17 row missing')
p.write_text(t.replace(a, 'recorded NOT_MET until Z-07 and Z-08 close |'), encoding='utf-8'); print('edited 17')
