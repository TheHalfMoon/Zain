"""Record the founder's confirmation of 20 §8 and close Q-00 (founder T2 sign-off, DEC-01). Run from docs/zain-master-plan."""
import csv, io, pathlib, sys
sys.path.insert(0, 'tools'); sys.dont_write_bytecode = True
from zmp import SCHEMAS

def rep(f, pairs):
    p = pathlib.Path(f); t = p.read_text(encoding='utf-8')
    for a, b in pairs:
        if t.count(a) != 1: sys.exit(f'NOT UNIQUE/MISSING {f}: {a[:70]}')
        t = t.replace(a, b)
    p.write_text(t, encoding='utf-8'); print('edited', f)

rep('20-R0A-ADMISSION-RECORD.md', [
    ("STATUS   = §1-§7 approved by the founder as drafted (chat, 2026-11-08); the §8 re-check was added afterwards and\n           awaits the founder's confirmation. Q-01 is RESOURCE_BLOCKED (§4)",
     "STATUS   = SIGNED OFF by the founder (T2 reviewer, DEC-01) in chat on 2026-11-08: §1-§7 approved as drafted, §8\n           confirmed. LIC-02 is re-checked against the packaged output at Q-04. Q-01 is RESOURCE_BLOCKED (§4)"),
    ("| A3 Q-00 independently reviewed | The founder approved the record as drafted (chat, 2026-11-08; DEC-01). The §7 re-checks added afterwards need the founder's confirmation; OCR may add an advisory pass after Z-06 |",
     "| A3 Q-00 independently reviewed | **Met:** the founder signed off §1-§7 as drafted and confirmed §8 (chat, 2026-11-08; DEC-01). OCR may add an advisory pass after Z-06 |"),
])
rep('17-MASTER-PLAN-STATUS.md', [("disk (D: 15.3 GB of 30 GB) and free RAM, plus the founder's confirmation of 20 §8.",
    "disk (D: 15.3 GB of 30 GB) and free RAM, plus the founder's confirmation of 20 §8.\n\n"
    "**2026-11-08, Q-00 signed off.** The founder confirmed 20 §8, completing the T2 sign-off (DEC-01). Q-00 is DONE;\n"
    "LIC-02 is re-checked on the packaged output at Q-04. Q-01 waits only on disk (Z-07) and free RAM.")])

def load(n): return list(csv.DictReader(open('registry/' + n, encoding='utf-8')))
def save(n, rows):
    o = io.StringIO(); w = csv.DictWriter(o, fieldnames=SCHEMAS[n], lineterminator='\n'); w.writeheader(); w.writerows(rows)
    open('registry/' + n, 'w', encoding='utf-8').write(o.getvalue()); print('saved', n)
B = load('zain-task-backlog.csv')
for r in B:
    if r['id'] == 'Q-00':
        r['status'] = 'DONE'
        r['status_evidence'] = ('20-R0A-ADMISSION-RECORD.md signed off by the founder (T2 reviewer, DEC-01) in chat 2026-11-08: §1-§7 approved '
                                'as drafted, §8 confirmed. Pin v0.1.7 = 322f6544; LIC-02 re-checked on packaged output at Q-04')
    if r['id'] == 'Q-01':
        r['blockers'] = r['blockers'].replace('; founder confirmation of 20 §8', '')
save('zain-task-backlog.csv', B)
