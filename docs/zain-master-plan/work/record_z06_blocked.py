"""Record that the Z-06 dry run is blocked by the relay's account requirement (2026-11-08). Run from docs/zain-master-plan."""
import csv, io, pathlib, sys
sys.path.insert(0, 'tools'); sys.dont_write_bytecode = True
from zmp import SCHEMAS

def rep(f, pairs):
    p = pathlib.Path(f); t = p.read_text(encoding='utf-8')
    for a, b in pairs:
        if t.count(a) != 1: sys.exit(f'NOT UNIQUE/MISSING {f}: {a[:70]}')
        t = t.replace(a, b)
    p.write_text(t, encoding='utf-8'); print('edited', f)

MSG = ('Z-06 dry run blocked 2026-11-08: (1) 02:48Z `opencode run` attached to a shared OpenCode background service busy '
       'with another project and timed out after 15 min without opening a session, so no content was sent; (2) 03:1xZ '
       '`opencode run --standalone` probes with a one-word prompt to both relay providers returned "telegram_required: Join '
       'the required Telegram group/channel and relink at /settings to continue". Founder action on the relay account needed; '
       'retry with --standalone afterwards')
rep('17-MASTER-PLAN-STATUS.md', [("path for public content.",
    "path for public content.\n\n"
    "**2026-11-08, Z-06 blocked.** The founder confirmed the relay route for public content only. The dry run could not\n"
    "run: the relay answers every request with \"telegram_required\" until the founder joins its Telegram group or channel\n"
    "and relinks the account at the relay's settings page. No repository content was sent (the first attempt never\n"
    "opened a session; the probes sent one word). Retry uses `opencode run --standalone`, which applies the locked-down\n"
    "run configuration instead of the shared background service.")])
rep('13-RISKS-AND-OPEN-DECISIONS.md', [("The founder's confirmation of that data path is pending (Z-06).",
    "**Confirmed by the founder the same day (\"Use the relay\"), for public content only.** The relay then refused all "
    "requests until the founder joins its Telegram group and relinks the account (Z-06 blocked).")])

def load(n): return list(csv.DictReader(open('registry/' + n, encoding='utf-8')))
def save(n, rows):
    o = io.StringIO(); w = csv.DictWriter(o, fieldnames=SCHEMAS[n], lineterminator='\n'); w.writeheader(); w.writerows(rows)
    open('registry/' + n, 'w', encoding='utf-8').write(o.getvalue()); print('saved', n)
B = load('zain-task-backlog.csv')
for r in B:
    if r['id'] == 'Z-06':
        r['status'] = 'BLOCKED'
        r['status_evidence'] = MSG
        r['blockers'] = 'Founder joins the relay\'s required Telegram group/channel and relinks the account at the relay settings page'
save('zain-task-backlog.csv', B)
G = load('zain-acceptance-gates.csv')
for g in G:
    if g['gate_id'] == 'GATE-REV-01':
        g['evidence'] = g['evidence'].replace('; confirmation pending', '; confirmed by the founder for public content') + \
            '; dry run blocked by the relay (telegram_required), no content sent'
save('zain-acceptance-gates.csv', G)
