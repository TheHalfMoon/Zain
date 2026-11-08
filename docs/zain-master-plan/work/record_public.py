"""Record the founder's reversal of DEC-02 (both repositories public again, 2026-11-08T01:31Z), withdraw ADR-Z04,
and copy the session work files into docs/zain-master-plan/work/. Run from docs/zain-master-plan; argv[1] = _work dir."""
import csv, io, pathlib, re, shutil, sys
sys.path.insert(0, 'tools'); sys.dont_write_bytecode = True
from zmp import SCHEMAS
SRC = pathlib.Path(sys.argv[1])

def rep(f, pairs):
    p = pathlib.Path(f); t = p.read_text(encoding='utf-8')
    for a, b in pairs:
        if t.count(a) != 1: sys.exit(f'NOT UNIQUE/MISSING {f}: {a[:70]}')
        t = t.replace(a, b)
    p.write_text(t, encoding='utf-8'); print('edited', f)

def append_cell(f, dec, text):
    p = pathlib.Path(f); lines = p.read_text(encoding='utf-8').split('\n')
    idx = [i for i, l in enumerate(lines) if l.startswith(f'| {dec} |')]
    if len(idx) != 1 or not lines[idx[0]].endswith(' |'): sys.exit(f'row {dec}')
    lines[idx[0]] = lines[idx[0]][:-2] + ' ' + text + ' |'
    p.write_text('\n'.join(lines), encoding='utf-8'); print('cell', dec)

D = '13-RISKS-AND-OPEN-DECISIONS.md'
append_cell(D, 'DEC-02', '**Reversed 2026-11-08 by the founder in chat: both repositories public again since 01:31Z; everything is kept in the repository.**')
append_cell(D, 'DEC-03', 'Moot while the repository is public (branch protection is free on public repositories); applies again if it goes private.')
append_cell(D, 'DEC-09', 'Amended 2026-11-08: the build branch is pushed, not kept local (founder: everything in the repository).')
rep(D, [('(18 P7); wepld/wepld private since 01:22:38Z |', '(18 P7). Both repositories public again since 01:31Z by founder choice (DEC-02 reversed) |')])
rep('05-ARCHITECTURE-AND-DECISIONS.md', [(
    '| ADR-Z04 | Until the repository is private, build work, donor source and artifacts stay local; only non-sensitive planning text may be pushed, and only after DEC-02 |',
    '| ADR-Z04 | **Withdrawn 2026-11-08 by the founder:** the repository is public by choice and all work, build work included, is pushed; nothing is kept only locally. Secrets and credentials still never enter the repository, and donor source keeps its license notices. (Was: build work, donor source and artifacts stay local until the repository is private.) |')])
rep('07-SECURITY-AND-CONTAINMENT.md', [('| Respected (nothing pushed) | ADR-Z04 |',
    '| Withdrawn with ADR-Z04 (2026-11-08): donor source is pushed with its license notices; secrets never | ADR-Z04 |')])
rep('11-TASK-CONTRACTS.md', [('Repository privacy (Z-01) gates pushing, not a local import of public MIT source (ADR-Z04)',
    'The repository is public by founder choice and pushing is not gated (ADR-Z04 withdrawn)')])
rep('17-MASTER-PLAN-STATUS.md', [
    ('| GATE-PRIV-01 | Zain PRIVATE since 2026-11-08T00:37:46Z, wepld/wepld since 01:22:38Z; gate closes when Z-01 finishes (0 USD spending limit) |',
     '| GATE-PRIV-01 | NOT_APPLICABLE: the founder made both repositories public again at 01:31Z (DEC-02 reversed) |'),
    ('| Z-01 remainder: confirm the 0 USD spending limit | Z-01 | Founder |\n', ''),
    ('Z-01 now waits only on the 0 USD spending limit.',
     'Z-01 now waits only on the 0 USD spending limit.\n\n'
     '**2026-11-08, visibility reversed.** At the founder\'s direction both repositories were made public again (Zain\n'
     '01:31:32Z, wepld/wepld 01:31:33Z; anonymous API 200, 0 forks). Before the change all 353 branch tips matched the last\n'
     'full fetch, so nothing new had been pushed while private. The founder also directed that everything live in the\n'
     'repository: ADR-Z04 is withdrawn, the build branch is pushed (DEC-09 amended), and the session scripts are in\n'
     '`work/`. Z-01 is NOT_NEEDED, GATE-PRIV-01 is NOT_APPLICABLE, and DEC-03 is moot while public.'),
])
rep('18-EXPOSURE-ASSESSMENT.md', [
    ('TheHalfMoon/Zain (public until 2026-11-08T00:37:46Z, now private)', 'TheHalfMoon/Zain (private 00:37:46Z–01:31:32Z on 2026-11-08, then public again by founder choice)'),
    ('wepld/wepld (public until 2026-11-08T01:22:38Z, now private)', 'wepld/wepld (private 01:22:38Z–01:31:33Z, then public again)'),
    ('| wepld/wepld (private since 01:22:38Z) |', '| wepld/wepld |'),
    ('until 2026-11-08T00:37:46Z. The exact start is unknown', 'until 2026-11-08T00:37:46Z, and again since 01:31:32Z by founder choice. The exact start is unknown'),
    ('| Since creation (2026-07-12) until 2026-11-08T01:22:38Z |', '| Since creation (2026-07-12); private only 01:22:38Z–01:31:33Z on 2026-11-08 |'),
    ('| No longer public (Zain 00:37:46Z, wepld 01:22:38Z), but was |', '| Yes (both repositories public again since 01:31Z) |'),
    ('| No longer public (01:22:38Z) |', '| Yes (public again) |'),
    ('CONFIDENTIALITY.md` | No longer public |', 'CONFIDENTIALITY.md` | Yes (public again) |'),
    ('| wepld/wepld | Done: made private 2026-11-08T01:22:38Z with the `wepld` login (DEC-02); anonymous API returns 404 | — | No |',
     '| wepld/wepld | Made private 01:22:38Z, then public again 01:31:33Z at the founder\'s direction (DEC-02 reversed); exposure accepted | Founder | No |'),
    ('wepld/wepld was made private at\n  01:22:38Z (DEC-02).', 'wepld/wepld was made private at\n  01:22:38Z (DEC-02), then made public again with Zain at 01:31Z by founder choice.'),
])
rep('README.md', [('| [18-EXPOSURE-ASSESSMENT.md](18-EXPOSURE-ASSESSMENT.md) | Z-03 public-exposure assessment of both repositories |',
    '| [18-EXPOSURE-ASSESSMENT.md](18-EXPOSURE-ASSESSMENT.md) | Z-03 public-exposure assessment of both repositories |\n'
    '| [work/](work/README.md) | Session scripts and intermediate data, kept for provenance (not maintained tools) |')])

def load(n): return list(csv.DictReader(open('registry/' + n, encoding='utf-8')))
def save(n, rows):
    out = io.StringIO(); w = csv.DictWriter(out, fieldnames=SCHEMAS[n], lineterminator='\n'); w.writeheader(); w.writerows(rows)
    open('registry/' + n, 'w', encoding='utf-8').write(out.getvalue()); print('saved', n)
B = load('zain-task-backlog.csv')
for r in B:
    if r['id'] == 'Z-01':
        r['status'] = 'NOT_NEEDED'; r['blockers'] = ''
        r['status_evidence'] = ('Founder reversed DEC-02 on 2026-11-08: both repositories public again (Zain 01:31:32Z, wepld/wepld 01:31:33Z, '
                                'anonymous API 200, 0 forks). Earlier: Zain private 00:37:46Z-01:31:32Z, wepld/wepld 01:22:38Z-01:31:33Z.')
save('zain-task-backlog.csv', B)
G = load('zain-acceptance-gates.csv')
for g in G:
    if g['gate_id'] == 'GATE-PRIV-01':
        g['status'] = 'NOT_APPLICABLE'
        g['evidence'] = 'Founder reversed DEC-02 on 2026-11-08: both repositories public by choice since 01:31Z (anonymous API 200)'
save('zain-acceptance-gates.csv', G)
R = load('zain-risk-register.csv')
for r in R:
    if r['risk_id'] == 'RK-01':
        r['evidence'] += '; 01:31Z the founder made both public again by choice (DEC-02 reversed); exposure accepted'
save('zain-risk-register.csv', R)

# session work files -> work/, with the redacted literals replaced
dst = pathlib.Path('work'); dst.mkdir(exist_ok=True)
REDACT = [(re.compile(r'<user>'), '<user>'), (re.compile(r'<relay-host>'), '<relay-host>')]
copied = []
for f in sorted(SRC.iterdir()):
    if f.is_dir() or f.name == 'z03_err.txt' or f.stat().st_size == 0: continue
    t = f.read_text(encoding='utf-8')
    for rx, s in REDACT: t = rx.sub(s, t)
    (dst / f.name).write_text(t, encoding='utf-8'); copied.append(f.name)
(dst / 'README.md').write_text('''# Session work files (2026-11-07 to 2026-11-08)

One-off scripts and intermediate data used to build this master plan, apply the review fixes, run the Z-03 exposure
scan and record founder decisions. They are kept here for provenance because the founder directed that all work live
in the repository. They are **not maintained tools**: most edit documents by exact string replacement against a past
state and will not re-run cleanly. The maintained tools are in `../tools/`.

Literals that the redaction scripts removed from the plan are replaced in these copies with `<user>` and
`<relay-host>`.

| Files | Purpose |
|---|---|
| `make_registries.py`, `make_registries_part2.py`, `export_v3.py`, `v3_export.json` | First build of the registry CSVs and the V3 task export they mirror |
| `apply_reviews.py`, `apply_reviews2.py`, `doc_edits*.py`, `scope_block.md`, `sec_sections.md`, `stats.py` | Review-fix and document edits; plan statistics |
| `z03_scan.py`, `z03_agg.py`, `z03_detail.py`, `z03_extra.py`, `z03_result.txt` | Z-03 scanner (in-memory, fingerprints only) and its aggregated output (18) |
| `record_*.py` | Status and decision records (Z-03, DEC-16, Z-25, visibility changes) |
''', encoding='utf-8')
print('copied', len(copied), 'files to work/')
