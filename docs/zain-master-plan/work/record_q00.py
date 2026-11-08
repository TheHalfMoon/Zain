"""Record the Q-00 draft (20-R0A-ADMISSION-RECORD.md) and the final usn search result. Run from docs/zain-master-plan."""
import csv, io, pathlib, sys
sys.path.insert(0, 'tools'); sys.dont_write_bytecode = True
from zmp import SCHEMAS

def rep(f, pairs):
    p = pathlib.Path(f); t = p.read_text(encoding='utf-8')
    for a, b in pairs:
        if t.count(a) != 1: sys.exit(f'NOT UNIQUE/MISSING {f}: {a[:70]}')
        t = t.replace(a, b)
    p.write_text(t, encoding='utf-8'); print('edited', f)

OLD = ('not found so far: a filename search of all of C: and D: (`dir /s *usn*.csv`, started 01:35Z) had no match when '
       'this note was committed and was still running; the final result is added when it finishes')
NEW = ('not found. A filename search of all of C: and D: (`dir /s /b /a-d *usn*.csv`, 2026-11-08 01:35Z, completed) '
       'returned no match; folders that need administrator rights were skipped')
rep('19-INCIDENT-CLOSEOUT.md', [(OLD, NEW)])
rep('13-RISKS-AND-OPEN-DECISIONS.md', [(OLD, NEW)])
rep('README.md', [('| [work/](work/README.md) |',
    '| [20-R0A-ADMISSION-RECORD.md](20-R0A-ADMISSION-RECORD.md) | V3 Q-00 R0a pre-admission record (draft for T2 review) |\n| [work/](work/README.md) |')])
rep('17-MASTER-PLAN-STATUS.md', [("DONE_UNREVIEWED; requirements R1-R6 go to Z-19.",
    "DONE_UNREVIEWED; requirements R1-R6 go to Z-19.\n\n"
    "**2026-11-08, Q-00 draft.** The R0a pre-admission record is drafted (20): T3 pinned to v0.1.7 (`322f6544`) with\n"
    "lockfile digests; toolchain gaps (Node 24.19.0 vs 26.12.1, pnpm 9.12.0 vs 12.14.0); LOCAL_ONLY route without the\n"
    "embedded WSL archive; 860-package shipped closure with 30 packages dispositioned. Q-00 is REVIEW_BLOCKED on the\n"
    "founder's T2 sign-off; Q-01 is also RESOURCE_BLOCKED (D: 16.5 GB, free RAM 1.6 GB).")])
rep('work/README.md', [('| `record_*.py` |',
    '| `q00_*.py`, `q00_license_listing.csv`, `q00_r11_delta.csv` | V3 Q-00 evidence: pin inventory, lockfile digests, shipped-closure licenses, R11 deltas (20) |\n| `record_*.py` |')])

def load(n): return list(csv.DictReader(open('registry/' + n, encoding='utf-8')))
def save(n, rows):
    out = io.StringIO(); w = csv.DictWriter(out, fieldnames=SCHEMAS[n], lineterminator='\n'); w.writeheader(); w.writerows(rows)
    open('registry/' + n, 'w', encoding='utf-8').write(out.getvalue()); print('saved', n)
B = load('zain-task-backlog.csv')
for r in B:
    if r['id'] == 'Q-00':
        r['status'] = 'BLOCKED'
        r['status_evidence'] = ('20-R0A-ADMISSION-RECORD.md drafted 2026-11-08: pin v0.1.7 = 322f6544 with lockfile digests, toolchain gaps, '
                                'LOCAL_ONLY route, 860-package license listing (30 dispositioned), A3-A7 table. REVIEW_BLOCKED')
        r['blockers'] = 'Founder T2 sign-off (DEC-01); founder decisions on 20 §5 packages, CLI archive route and Rust pin; seam and citation re-check (20 §7)'
    if r['id'] == 'Q-01':
        r['blockers'] = 'RESOURCE_BLOCKED: D: 16.5 GB free (needs 30 GB, Z-07) and 1.6 GB free RAM (needs 6 GB); toolchain gaps (Z-08); Q-00 review'
save('zain-task-backlog.csv', B)
