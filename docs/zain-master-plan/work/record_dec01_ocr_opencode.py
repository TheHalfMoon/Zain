"""Record the founder's reviewer-route instruction (2026-11-08): no CodeRabbit; Alibaba OCR via OpenCode free models.
Records the verified data path: OpenCode here reaches models only through a hosted third-party relay. Run from
docs/zain-master-plan."""
import csv, io, pathlib, sys
sys.path.insert(0, 'tools'); sys.dont_write_bytecode = True
from zmp import SCHEMAS

def rep(f, pairs):
    p = pathlib.Path(f); t = p.read_text(encoding='utf-8')
    for a, b in pairs:
        if t.count(a) != 1: sys.exit(f'NOT UNIQUE/MISSING {f}: {a[:70]}')
        t = t.replace(a, b)
    p.write_text(t, encoding='utf-8'); print('edited', f)

NOTE = ('**Amended 2026-11-08 (founder, in chat): no CodeRabbit; reviews run through Alibaba OCR (open-code-review 1.13.6) '
        'using OpenCode\'s free models.** Verified the same day: OpenCode 2.2.5 reaches models only through the hosted '
        'third-party relay configured as `nararouter` (free models such as deepseek-v4-pro-free and qwen-3.8-max-free), and '
        'no local model runner is installed, so this route sends diffs to the relay; it is not local. The repository is '
        'public. The founder\'s confirmation of that data path is pending (Z-06).')
p = pathlib.Path('13-RISKS-AND-OPEN-DECISIONS.md'); lines = p.read_text(encoding='utf-8').split('\n')
i = [k for k, l in enumerate(lines) if l.startswith('| DEC-01 |')]
if len(i) != 1 or not lines[i[0]].endswith(' |'): sys.exit('DEC-01 row')
lines[i[0]] = lines[i[0]][:-2] + ' ' + NOTE + ' |'
p.write_text('\n'.join(lines), encoding='utf-8'); print('edited 13 DEC-01')
rep('22-APP-EGRESS-INVENTORY.md', [('**Decided 2026-11-08 (founder, in chat): remove Zain from all 10 apps, CodeRabbit included; no gate exception.**',
    '**Decided 2026-11-08 (founder, in chat): remove Zain from all 10 apps, CodeRabbit included; no gate exception.** The founder '
    'also said not to use CodeRabbit for review; the review route is Alibaba OCR via OpenCode (13, DEC-01).')])
rep('17-MASTER-PLAN-STATUS.md', [("the change is the founder's to make in GitHub settings.",
    "the change is the founder's to make in GitHub settings.\n\n"
    "**2026-11-08, reviewer route.** The founder said not to use CodeRabbit and to review with Alibaba OCR via OpenCode's\n"
    "free models. Checked: OpenCode here reaches models only through a hosted third-party relay, and no local model runner\n"
    "is installed, so the route is remote, not local. DEC-01 records it; Z-06 waits for the founder to confirm that data\n"
    "path for public content.")])

def load(n): return list(csv.DictReader(open('registry/' + n, encoding='utf-8')))
def save(n, rows):
    o = io.StringIO(); w = csv.DictWriter(o, fieldnames=SCHEMAS[n], lineterminator='\n'); w.writeheader(); w.writerows(rows)
    open('registry/' + n, 'w', encoding='utf-8').write(o.getvalue()); print('saved', n)
B = load('zain-task-backlog.csv')
for r in B:
    if r['id'] == 'Z-06':
        r['blockers'] = ('Founder confirms the OCR-via-OpenCode route: it sends diffs to a hosted third-party relay, not a local model '
                         '(13 DEC-01 amendment); then one dry-run review of this plan')
save('zain-task-backlog.csv', B)
G = load('zain-acceptance-gates.csv')
for g in G:
    if g['gate_id'] == 'GATE-REV-01':
        g['evidence'] += ('; 2026-11-08 founder: no CodeRabbit, use Alibaba OCR via OpenCode free models; that route is a hosted relay '
                          '(no local runner installed); confirmation pending')
save('zain-acceptance-gates.csv', G)
