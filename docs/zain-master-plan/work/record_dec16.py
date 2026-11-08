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
        r['status_evidence'] = r['status_evidence'].replace('founder acceptance pending (DEC-16)',
            'DEC-16 decided 2026-11-08 (accept, noreply identity); P2 resolved as founder-owned accounts; P7 profile email open')
save('zain-task-backlog.csv', B)
G = load('zain-acceptance-gates.csv')
for g in G:
    if g['gate_id'] == 'GATE-PRIV-03':
        g['evidence'] = ('18-EXPOSURE-ASSESSMENT.md: 0 live credentials; every hit dispositioned and accepted by the founder (DEC-16, 2026-11-08); '
                         'MET in substance, recorded NOT_MET until Z-03 is reviewed')
save('zain-acceptance-gates.csv', G)

def rep(f, pairs):
    p = pathlib.Path(f); t = p.read_text(encoding='utf-8')
    for a, b in pairs:
        if t.count(a) != 1: sys.exit(f'NOT UNIQUE/MISSING {f}: {a[:70]}')
        t = t.replace(a, b)
    p.write_text(t, encoding='utf-8'); print('edited', f)

rep('13-RISKS-AND-OPEN-DECISIONS.md', [
    ('None is decided by this document.', 'None is decided by this document; the Decided column records founder answers.'),
    ('identify the two other wepld identities | GATE-PRIV-03 | — |',
     'identify the two other wepld identities | GATE-PRIV-03 | 2026-11-08, founder in chat: accept the exposure, no history rewrite; '
     'commits now use the GitHub noreply address. The other wepld identities are founder-owned accounts. Still open: GitHub email-privacy '
     'settings and profile email (18 P7), wepld/wepld visibility (Z-01) |'),
])
rep('18-EXPOSURE-ASSESSMENT.md', [
    ('| Yes | Unknown; founder to identify (collaborator or another account) |',
     '| Yes | None for third parties: both map to founder-owned GitHub accounts (commit API, 2026-11-08) |'),
    ('| P6 | Environment details |',
     '| P7 | The founder\'s personal Gmail as the public profile email of the account the Zain commits map to | GitHub user profile (found 2026-11-08) | Yes, regardless of repository visibility | Medium (same identifier as P1, still published) |\n| P6 | Environment details |'),
    ('| P2 other identities | Founder identifies them; if they belong to other people, tell them their address was public | Founder | No |',
     '| P2 other identities | Resolved: both are founder-owned accounts; no one to notify | — | No |\n'
     '| P7 profile email | Set the profile\'s public email to "Don\'t show my email address" | Founder | No (settings only) |'),
])
p = pathlib.Path('18-EXPOSURE-ASSESSMENT.md')
p.write_text(p.read_text(encoding='utf-8').rstrip('\n') + '''

## 8. Founder decision (DEC-16, 2026-11-08)

- **Accepted:** the historical commit-email exposure (P1). History is not rewritten.
- **Done:** the global git identity on the founder's PC now uses the GitHub noreply address of the account that the
  existing commits map to, so attribution is unchanged. The commit that recorded this decision is the first with it.
- **Resolved:** P2. Both other wepld identities belong to the founder's own GitHub accounts.
- **Founder to do:** in GitHub email settings, enable "Keep my email addresses private" and "Block command line pushes
  that expose my email"; set the profile's public email to "Don't show my email address" (P7). The active `gh` token
  lacks the `user` scope, so the agent cannot read or change these settings. Make wepld/wepld private or archive it
  (Z-01).
- **Caveat:** once push blocking is on, GitHub rejects pushes of new commits authored with the personal address,
  including unpushed commits made before the switch in other local repositories.
''', encoding='utf-8')
print('edited 18 §8')
rep('17-MASTER-PLAN-STATUS.md', [
    ('| Founder decisions | OPEN: DEC-01..DEC-16 | 13 §2 |', '| Founder decisions | OPEN: DEC-01..DEC-15; DEC-16 decided 2026-11-08 | 13 §2 |'),
    ('| GATE-PRIV-03 | 0 live credentials, all hits dispositioned; waits for founder DEC-16 | 18 |',
     '| GATE-PRIV-03 | MET in substance (0 live credentials; DEC-16 accepted), recorded NOT_MET until Z-03 review | 18 |'),
    ("Z-03 is DONE_UNREVIEWED; GATE-PRIV-03 waits for the founder's DEC-16.",
     "Z-03 is DONE_UNREVIEWED; GATE-PRIV-03 waits for the founder's DEC-16.\n\n"
     "**2026-11-08, DEC-16.** The founder accepted the historical exposure; history is not rewritten. Git commits on the\n"
     "founder's PC now use the GitHub noreply address, and the two other wepld identities proved to be founder-owned.\n"
     "New finding P7: the account's public profile email is still the personal address. Founder to do: GitHub email\n"
     "privacy settings, profile email, wepld/wepld visibility (18 §8)."),
])
