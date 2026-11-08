import csv, io, pathlib, sys
sys.path.insert(0, 'tools'); sys.dont_write_bytecode = True
from zmp import SCHEMAS

def load(n): return list(csv.DictReader(open('registry/' + n, encoding='utf-8')))
def save(n, rows):
    out = io.StringIO(); w = csv.DictWriter(out, fieldnames=SCHEMAS[n], lineterminator='\n'); w.writeheader(); w.writerows(rows)
    open('registry/' + n, 'w', encoding='utf-8').write(out.getvalue())

EV = 'gh repo edit --visibility private at 2026-11-08T00:37:46Z (founder-approved in chat); gh repo view returns PRIVATE; forkCount was 0'
B = load('zain-task-backlog.csv')
for r in B:
    if r['id'] == 'Z-01':
        r['status'] = 'IN_PROGRESS'
        r['status_evidence'] = EV + '. Remaining: confirm 0 USD Actions/Packages spending limit; decide wepld/wepld (separate account, still PUBLIC)'
        r['blockers'] = 'Founder: spending-limit check on the billing page; wepld/wepld decision (DEC-02)'
save('zain-task-backlog.csv', B)
G = load('zain-acceptance-gates.csv')
for g in G:
    if g['gate_id'] == 'GATE-PRIV-01':
        g['evidence'] = 'Visibility PRIVATE since 2026-11-08T00:37:46Z; gate stays NOT_MET until Z-01 closes (spending limit, wepld/wepld)'
save('zain-acceptance-gates.csv', G)
R = load('zain-risk-register.csv')
for r in R:
    if r['risk_id'] == 'RK-01':
        r['status'] = 'MITIGATING'
        r['evidence'] = 'TheHalfMoon/Zain PRIVATE since 2026-11-08T00:37:46Z; history was public before (Z-03); wepld/wepld still PUBLIC'
save('zain-risk-register.csv', R)

def rep(f, pairs):
    p = pathlib.Path(f); t = p.read_text(encoding='utf-8')
    for a, b in pairs:
        if a not in t: sys.exit(f'MISSING {f}: {a[:60]}')
        t = t.replace(a, b)
    p.write_text(t, encoding='utf-8'); print('edited', f)

rep('17-MASTER-PLAN-STATUS.md', [
    ('| GATE-PRIV-01 | NOT MET (public) | 01 §2 |', '| GATE-PRIV-01 | Visibility PRIVATE since 2026-11-08T00:37:46Z; gate closes when Z-01 finishes (0 USD spending limit, wepld/wepld decision) | Z-01 evidence |'),
    ('| Repository public (gates pushing, not local building) | DEC-02 → Z-01 | Founder |', '| Z-01 remainder: spending limit and the still-public wepld/wepld | DEC-02 → Z-01 | Founder |'),
    ('decisions (DEC-01, DEC-02, DEC-04, DEC-07, DEC-08, DEC-12), then Z-03 and Z-18.',
     'decisions (DEC-01, DEC-02, DEC-04, DEC-07, DEC-08, DEC-12), then Z-03 and Z-18.\n\n**2026-11-08, follow-up.** At the founder\'s direction, TheHalfMoon/Zain was made PRIVATE (00:37:46Z, verified; 0 forks).\nThe plan branch was then pushed; no workflow runs on non-main branch pushes and no PR was opened.'),
    ('| Branch | `docs/zain-master-plan-20261108` (local clone in the session folder; not pushed) |', '| Branch | `docs/zain-master-plan-20261108`, pushed to the now-private TheHalfMoon/Zain (no PR) |'),
])
rep('00-EXECUTIVE-SUMMARY.md', [
    ('BRANCH    = docs/zain-master-plan-20261108 (local commit only; the repository is public, so nothing was pushed)',
     'BRANCH    = docs/zain-master-plan-20261108 (pushed after the repository was made private on 2026-11-08; no PR)'),
    ('- **Repository:** `TheHalfMoon/Zain`, which is **public**, as is the legacy `wepld/wepld`. This conflicts with the\n  founder\'s privacy rule (01 §2).',
     '- **Repository:** `TheHalfMoon/Zain` was **public** at audit time and was made **private** on 2026-11-08 at the founder\'s\n  direction. Its history was public before that (Z-03), and the legacy `wepld/wepld` is still public (01 §2).'),
])
