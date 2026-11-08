"""Record founder decisions DEC-01..DEC-15 (2026-11-08, all as recommended). Run from docs/zain-master-plan."""
import csv, io, pathlib, re, sys
sys.path.insert(0, 'tools'); sys.dont_write_bytecode = True
from zmp import SCHEMAS

P = '2026-11-08, founder in chat: '
DECIDED = {
    'DEC-01': 'founder signs off T2; OCR on the founder\'s ChatGPT login is authorized for private content as advisory review; local checks always; the relay (c) is not authorized',
    'DEC-02': 'both private. Zain private since 00:37:46Z; wepld/wepld to be made private (Z-01)',
    'DEC-03': 'no paid plan; local checker G-03 plus founder-signed merges G-02; server-side protection recorded as absent',
    'DEC-04': 're-pin to the v0.1.7 tag at Q-00, recording the R11 deltas',
    'DEC-05': 'pull I-03 into R1 if Z-20 confirms Monaco; otherwise it stays in R3',
    'DEC-06': 'S-01 moves to R2 once C-00 proves the mechanisms; otherwise it stays in R5',
    'DEC-07': 'R0b is the first release',
    'DEC-08': 'official CLI logins (Codex) for agent turns, local models for completion and triage, no relays for private code',
    'DEC-09': 'freeze; no v73+ during R0a/R0b; G-03 replaces the chain at R0',
    'DEC-10': 'confirmed as Ascout\'s; the founder does not know where usn-journal.csv is, so it is treated as not found',
    'DEC-11': 'keep them on the planning branch until G-03',
    'DEC-12': 'D:, after the founder frees it to GATE-RES-01 (15 GB free on 2026-11-08)',
    'DEC-13': 'Playwright-only for Z-15; Ascout decided before E-03',
    'DEC-14': 'optional; a Claude session is tested only if the founder supplies a key',
    'DEC-15': 'no auto-update in R0b; for R0 a founder-controlled static host with an ed25519 key held offline',
}

def rep(f, pairs):
    p = pathlib.Path(f); t = p.read_text(encoding='utf-8')
    for a, b in pairs:
        if t.count(a) != 1: sys.exit(f'NOT UNIQUE/MISSING {f}: {a[:70]}')
        t = t.replace(a, b)
    p.write_text(t, encoding='utf-8'); print('edited', f)

# 13: Decided column, header lines, open questions
p = pathlib.Path('13-RISKS-AND-OPEN-DECISIONS.md'); lines = p.read_text(encoding='utf-8').split('\n'); n = 0
for i, l in enumerate(lines):
    m = re.match(r'^\| (DEC-\d\d) \|', l)
    if m and m.group(1) in DECIDED:
        if not l.endswith('| — |'): sys.exit(f'unexpected Decided cell for {m.group(1)}')
        lines[i] = l[:-len('— |')] + P + DECIDED[m.group(1)] + ' |'; n += 1
assert n == 15, n
p.write_text('\n'.join(lines), encoding='utf-8')
rep('13-RISKS-AND-OPEN-DECISIONS.md', [
    ('each needs the founder (Z-25).', 'all decided by the founder on 2026-11-08 (Z-25).'),
    ('Decisions are recorded by Z-25.', 'Decisions are recorded by Z-25. All sixteen were decided on 2026-11-08; the Decided column holds each answer.'),
    ('cut off when the earlier session ended.', 'cut off when the earlier session ended. **Founder, 2026-11-08 (DEC-10):** location not known; treated as not found.'),
    ('No\n   written authorization was found (DEC-01).',
     'No\n   written authorization was found (DEC-01). **Answered 2026-11-08 (DEC-01):** OCR through the founder\'s ChatGPT\n   login is authorized as advisory review; the third-party relay is not.'),
])
rep('00-EXECUTIVE-SUMMARY.md', [
    ('**Ready now:** M0, plus the read-only agent tasks Z-03 and Z-18.', '**Ready now:** M0, plus the read-only agent task Z-18 (Z-03 is done, unreviewed).'),
    ('1. The founder decides DEC-01, DEC-02, DEC-04, DEC-07, DEC-08 and DEC-12 (Z-25).',
     '1. Founder decisions: **done**. The founder decided DEC-01..DEC-16 on 2026-11-08 (13 §2).'),
    ("2. A reviewer route is authorized (Z-06). The founder's own review always qualifies.",
     '2. The reviewer route authorized by DEC-01 is qualified with one dry-run review (Z-06).'),
    ('3. Disk capacity reaches GATE-RES-01 (Z-07).', '3. Disk capacity on D: reaches GATE-RES-01 (Z-07, DEC-12).'),
])
rep('02-PRODUCT-SCOPE.md', [('R0b (DEC-07, founder decision required).', 'R0b (DEC-07, decided by the founder on 2026-11-08).')])
rep('04-SOURCE-STRATEGY.md', [
    ('**re-pin decision DEC-04**', '**DEC-04: re-pin to v0.1.7 at Q-00**'),
    ('FO-9 relicensing confirmation open (DEC-13)', 'FO-9 relicensing confirmation open; Playwright-only until E-03 (DEC-13)'),
])
rep('05-ARCHITECTURE-AND-DECISIONS.md', [('or earlier, DEC-05', 'LSP spike in R1 if Z-20 confirms Monaco, DEC-05')])
rep('11-TASK-CONTRACTS.md', [
    ('build volume (DEC-12) must be decided first |', 'build volume (DEC-12) must be decided first (decided 2026-11-08) |'),
    ('No authorized reviewer (A7); C: 3.4 GB free;', 'Reviewer route authorized (DEC-01) but not yet qualified (A7); build volume D: has 15 GB free;'),
    ('**Re-pin question (DEC-04).**', '**Re-pin (DEC-04, decided 2026-11-08: re-pin to the v0.1.7 tag).**'),
    ('Q-00 must record either the original pin or a\nre-pin to the release tag,', 'Q-00 records the re-pin to the release tag,'),
])
rep('17-MASTER-PLAN-STATUS.md', [
    ('| Founder decisions | OPEN: DEC-01..DEC-15; DEC-16 decided 2026-11-08 | 13 §2 |',
     '| Founder decisions | DONE: DEC-01..DEC-16 decided 2026-11-08 (Z-25, unreviewed) | 13 §2 |'),
    ('(0 USD spending limit, wepld/wepld decision)', '(0 USD spending limit, wepld/wepld made private)'),
    ('| GATE-REV-01 | NOT MET (no authorized non-Claude route) |',
     '| GATE-REV-01 | NOT MET: route authorized (DEC-01: founder T2 sign-off, OCR on ChatGPT as advisory); Z-06 dry run pending |'),
    ('| GATE-RES-01 | NOT MET (C: 3.4 GB, D: 20 GB) |', '| GATE-RES-01 | NOT MET (D:, chosen by DEC-12, has 15 GB free; needs at least 30 GB) |'),
    ('| Z-01 remainder: spending limit and the still-public wepld/wepld | DEC-02 → Z-01 | Founder |',
     '| Z-01 remainder: 0 USD spending limit; make wepld/wepld private (DEC-02) | Z-01 | Founder |'),
    ('| Reviewer route | DEC-01 → Z-06 | Founder |', '| Reviewer route qualification: OCR on the ChatGPT login, one dry-run review | Z-06 | Founder + agent |'),
    ('| Disk capacity | DEC-12 → Z-07 | Founder |', '| Disk capacity: free D: to at least 30 GB (DEC-12) | Z-07 | Founder |'),
    ('| All decisions | Z-25 | Founder |\n', ''),
    ('privacy settings, profile email, wepld/wepld visibility (18 §8).',
     'privacy settings, profile email, wepld/wepld visibility (18 §8).\n\n'
     '**2026-11-08, Z-25.** The founder decided DEC-01..DEC-15 in chat, each as recommended (13 §2): R0b is the first\n'
     'release, T3 re-pins to v0.1.7, builds go on D:, the governance chain is frozen, OCR on the founder\'s ChatGPT login\n'
     'is the advisory reviewer. Founder actions left: make wepld/wepld private, 0 USD spending limit, free D: to 30 GB,\n'
     'GitHub email settings, OCR setup for the Z-06 dry run.'),
])

def load(n): return list(csv.DictReader(open('registry/' + n, encoding='utf-8')))
def save(n, rows):
    out = io.StringIO(); w = csv.DictWriter(out, fieldnames=SCHEMAS[n], lineterminator='\n'); w.writeheader(); w.writerows(rows)
    open('registry/' + n, 'w', encoding='utf-8').write(out.getvalue()); print('saved', n)
def sub(row, field, a, b):
    if row[field].count(a) != 1: sys.exit(f'NOT UNIQUE/MISSING {field}: {a[:60]}')
    row[field] = row[field].replace(a, b)

B = load('zain-task-backlog.csv')
for r in B:
    if r['id'] == 'Z-25':
        r['status'] = 'DONE_UNREVIEWED'
        r['status_evidence'] = ('13 §2 (2026-11-08): the founder answered DEC-01..DEC-16 in chat, all as recommended; recorded by the agent; '
                                'DEC-10 confirmed, usn-journal.csv location unknown; no separate signature beyond the founder\'s chat answers')
    if r['id'] == 'Z-01':
        sub(r, 'blockers', 'wepld/wepld decision (DEC-02)', 'make wepld/wepld private (DEC-02)')
        if 'Remaining:' not in r['status_evidence']: sys.exit('Z-01 evidence format changed')
        r['status_evidence'] = r['status_evidence'].split('Remaining:')[0] + 'Remaining: confirm 0 USD Actions/Packages spending limit; make wepld/wepld private (DEC-02, decided 2026-11-08).'
    if r['id'] == 'Z-06':
        sub(r, 'blockers', 'Founder decision DEC-01', 'Founder sets up OCR on the ChatGPT login for the dry-run review (DEC-01 decided 2026-11-08)')
    if r['id'] == 'G-07':
        sub(r, 'blockers', 'DEC-03:', 'DEC-03 (decided 2026-11-08: local checks plus founder-signed merges):')
save('zain-task-backlog.csv', B)
G = load('zain-acceptance-gates.csv')
for g in G:
    if g['gate_id'] == 'GATE-REV-01':
        g['evidence'] = (g['evidence'] + '; ' if g['evidence'] else '') + 'DEC-01 decided 2026-11-08 (founder T2 sign-off; OCR on the founder\'s ChatGPT login as advisory); Z-06 dry run pending'
    if g['gate_id'] == 'GATE-RES-01':
        g['evidence'] = (g['evidence'] + '; ' if g['evidence'] else '') + '2026-11-08: DEC-12 chose D:, which has 15 GB free (C: 22 GB)'
save('zain-acceptance-gates.csv', G)
C = load('zain-capability-matrix.csv')
for c in C:
    if c['cap_id'] == 'CAP-04': sub(c, 'competitor_basis', 'DEC-05 proposes pulling forward', 'DEC-05 (decided): LSP spike in R1 if Z-20 confirms Monaco')
    if c['cap_id'] == 'CAP-42': sub(c, 'competitor_basis', 'DEC-06 proposes pulling forward', 'DEC-06 (decided): S-01 to R2 after C-00 proof')
save('zain-capability-matrix.csv', C)
S = load('zain-source-registry.csv')
for s in S:
    if list(s.values())[0] == 'SRC-T3': sub(s, 'notes', 'Re-pin decision DEC-04;', 'DEC-04 decided 2026-11-08: re-pin to the v0.1.7 tag at Q-00;')
save('zain-source-registry.csv', S)
