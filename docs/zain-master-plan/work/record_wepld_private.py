"""Record wepld/wepld made private (2026-11-08T01:22:38Z). Run from docs/zain-master-plan."""
import csv, io, pathlib, sys
sys.path.insert(0, 'tools'); sys.dont_write_bytecode = True
from zmp import SCHEMAS
T = '2026-11-08T01:22:38Z'

def rep(f, pairs):
    p = pathlib.Path(f); t = p.read_text(encoding='utf-8')
    for a, b in pairs:
        if t.count(a) != 1: sys.exit(f'NOT UNIQUE/MISSING {f}: {a[:70]}')
        t = t.replace(a, b)
    p.write_text(t, encoding='utf-8'); print('edited', f)

rep('00-EXECUTIVE-SUMMARY.md', [('and the legacy `wepld/wepld` is still public (01 §2).',
                                 f'and the legacy `wepld/wepld` was public until {T} (01 §2).')])
rep('13-RISKS-AND-OPEN-DECISIONS.md', [
    ('wepld/wepld to be made private (Z-01)', 'wepld/wepld private since 01:22:38Z (anonymous API 404)'),
    ('(18 P7), wepld/wepld visibility (Z-01) |', '(18 P7); wepld/wepld private since 01:22:38Z |'),
])
rep('17-MASTER-PLAN-STATUS.md', [
    ('| GATE-PRIV-01 | Visibility PRIVATE since 2026-11-08T00:37:46Z; gate closes when Z-01 finishes (0 USD spending limit, wepld/wepld made private) |',
     '| GATE-PRIV-01 | Zain PRIVATE since 2026-11-08T00:37:46Z, wepld/wepld since 01:22:38Z; gate closes when Z-01 finishes (0 USD spending limit) |'),
    ('| Z-01 remainder: 0 USD spending limit; make wepld/wepld private (DEC-02) | Z-01 | Founder |',
     '| Z-01 remainder: confirm the 0 USD spending limit | Z-01 | Founder |'),
    ('GitHub email settings, OCR setup for the Z-06 dry run.',
     'GitHub email settings, OCR setup for the Z-06 dry run.\n\n'
     f'**2026-11-08, wepld/wepld.** Made private at {T} with the `wepld` login, founder-approved in chat (DEC-02).\n'
     'Evidence: `gh repo edit wepld/wepld --visibility private` succeeded; `gh repo view` as owner returns PRIVATE with 0\n'
     'forks; an anonymous `GET /repos/wepld/wepld` returns 404. Z-01 now waits only on the 0 USD spending limit.'),
])
rep('18-EXPOSURE-ASSESSMENT.md', [
    ('and wepld/wepld (still public)', f'and wepld/wepld (public until {T}, now private)'),
    ('| wepld/wepld (still public) |', '| wepld/wepld (private since 01:22:38Z) |'),
    ('| Since creation (2026-07-12), still open |', f'| Since creation (2026-07-12) until {T} |'),
    ('| wepld: yes. Zain: no longer public, but was |', '| No longer public (Zain 00:37:46Z, wepld 01:22:38Z), but was |'),
    ('| wepld: 11 and 2 commits | Yes |', '| wepld: 11 and 2 commits | No longer public (01:22:38Z) |'),
    ('CONFIDENTIALITY.md` | wepld: yes |', 'CONFIDENTIALITY.md` | No longer public |'),
    ('| wepld/wepld | Make it private or archive it from the `wepld` account; it still exposes P1, P2 and P3 | Founder | No |',
     f'| wepld/wepld | Done: made private {T} with the `wepld` login (DEC-02); anonymous API returns 404 | — | No |'),
    ('Make wepld/wepld private or archive it\n  (Z-01).', 'wepld/wepld was made private at\n  01:22:38Z (DEC-02).'),
])

def load(n): return list(csv.DictReader(open('registry/' + n, encoding='utf-8')))
def save(n, rows):
    out = io.StringIO(); w = csv.DictWriter(out, fieldnames=SCHEMAS[n], lineterminator='\n'); w.writeheader(); w.writerows(rows)
    open('registry/' + n, 'w', encoding='utf-8').write(out.getvalue()); print('saved', n)

B = load('zain-task-backlog.csv')
for r in B:
    if r['id'] == 'Z-01':
        if r['blockers'] != 'Founder: spending-limit check on the billing page; make wepld/wepld private (DEC-02)': sys.exit('Z-01 blockers changed')
        r['blockers'] = 'Founder: spending-limit check on the billing page'
        head = r['status_evidence'].split('Remaining:')[0]
        r['status_evidence'] = (head + f'wepld/wepld made private {T} with the wepld login (founder-approved in chat; owner view PRIVATE, '
                                'anonymous API 404, 0 forks). Remaining: confirm 0 USD Actions/Packages spending limit.')
save('zain-task-backlog.csv', B)
R = load('zain-risk-register.csv')
for r in R:
    if r['risk_id'] == 'RK-01':
        r['evidence'] += f'; both repositories PRIVATE since 2026-11-08 (Zain 00:37:46Z, wepld/wepld 01:22:38Z)'
save('zain-risk-register.csv', R)
