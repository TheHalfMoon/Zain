"""Record Z-06: reviewer routes per data class (founder-confirmed 2026-11-08) and the dry-run review.
Reads work/z06_findings.json and work/z06_triage.json ({finding id: {"proposed": "ACCEPTED|DISMISSED", "reason": ..., "note": ...}}).
Run from docs/zain-master-plan."""
import csv, io, json, pathlib, sys
sys.path.insert(0, 'tools'); sys.dont_write_bytecode = True
from zmp import SCHEMAS
data = json.loads(pathlib.Path('work/z06_findings.json').read_text(encoding='utf-8'))
tri = json.loads(pathlib.Path('work/z06_triage.json').read_text(encoding='utf-8'))
run, F = data['run'], data['findings']
acc = sum(1 for f in F if tri.get(f['id'], {}).get('proposed') == 'ACCEPTED')

def cell(s): return str(s).replace('|', '\\|').replace('\n', ' ')
rows = '\n'.join(
    f"| {f['id'][-2:]} | {f['severity']} | {f['category']} | `{f['path'].split('/')[-1]}`:{f['startLine']} | {cell(f['content'][:260])} | "
    f"{tri.get(f['id'], {}).get('proposed', 'OPEN')}: {cell(tri.get(f['id'], {}).get('note', ''))} |" for f in F) or '| — | — | — | — | no findings | — |'

doc = f'''# 23 — Reviewer Route and Dry-Run Review (task Z-06)

```text
DATE     = 2026-11-08
TASK     = Z-06 (AGENT+FOUNDER): reviewer routes per data class signed by the founder; one dry-run review of this plan
           through an authorized route, findings in the V3 Code Review schema (R14 §6)
STATUS   = routes confirmed by the founder; dry run {run['status']} ({len(F)} findings, {acc} proposed ACCEPTED by the builder);
           dispositions become final only when the founder confirms them
```

## 1. Reviewer routes by data class (DEC-01, founder-confirmed in chat 2026-11-08)

| Data class | Allowed routes | Not allowed |
|---|---|---|
| Public (everything in the public repositories) | The founder (qualified reviewer, signs off T2). Alibaba OpenCodeReview (OCR) rules run by OpenCode through the configured third-party relay's free models, **advisory** | CodeRabbit and the other hosted review apps (22) |
| Private planning or private code (anything not public, e.g. local-only files) | The founder only | The relay and every hosted model |
| Secrets and credentials | Never sent to any reviewer | Everything |

Model routes are advisory for T2 work. For T0/T1 work a model route may stand in for the founder only when its model
family differs from both the builder's and the provider under test's. The relay's free models (DeepSeek, Qwen) differ
from Claude (this builder) and from GPT (Codex). The relay's operator and data handling are unknown, so only public
content goes there.

## 2. Route configuration (credentials redacted)

| Item | Value |
|---|---|
| Review rules | `ocr delegate rule` (open-code-review 1.13.6): system/default rule group |
| Host agent | OpenCode 2.2.5, `opencode run --agent plan`, run outside the repository |
| Tools | edit, bash and webfetch denied; the two configured MCP servers disabled (project `opencode.json`) |
| Model | `{run['route']['model']}` via an OpenAI-compatible provider pointing at the relay; endpoint and account redacted |
| Key handling | OpenCode reads its own configured credentials; the agent never handled the key |

## 3. Dry-run record

| Item | Value |
|---|---|
| Run | `{run['id']}`, {run['startedAt']} to {run['endedAt']}, status {run['status']} |
| Scope | 6 documents (00, 13, 17, 20, 21, 22), screened before sending: 0 secret-rule hits, 0 personal-data hits |
| Sent (sha256, first 16) | {', '.join(f"`{k.split('-')[0]}` {v[:16]}" for k, v in run['sentFilesSha256'].items())} |
| Output | {run['parsedItems']} items parsed, {len(run['rejectedItems'])} rejected; raw output sha256 `{run['rawOutputSha256'][:16]}` |
| Findings file | `work/z06_findings.json` (Finding schema: fingerprint, path, lines, category, severity, confidence, content marked UNTRUSTED, rule, producer) |

## 4. Findings and proposed dispositions

The reviewer's text is untrusted data. The builder checked each finding against the documents and proposes a
disposition; per the schema, an agent may only propose ACCEPTED or DISMISSED, and the founder confirms.

| # | Severity | Category | Location | Finding (reviewer's words, shortened) | Builder's proposal |
|---|---|---|---|---|---|
{rows}

## 5. Limits

- One dry run over six documents is a qualification of the route, not a review of the whole plan.
- Free relay models can change or disappear without notice; each review records the model it used.
'''
pathlib.Path('23-REVIEW-ROUTE-AND-DRY-RUN.md').write_text(doc, encoding='utf-8'); print('wrote 23')

def rep(f, pairs):
    p = pathlib.Path(f); t = p.read_text(encoding='utf-8')
    for a, b in pairs:
        if t.count(a) != 1: sys.exit(f'NOT UNIQUE/MISSING {f}: {a[:70]}')
        t = t.replace(a, b)
    p.write_text(t, encoding='utf-8'); print('edited', f)
rep('13-RISKS-AND-OPEN-DECISIONS.md', [("The founder's confirmation of that data path is pending (Z-06).",
    "**Confirmed by the founder the same day (\"Use the relay\"), for public content only; routes per data class in 23 §1.**")])
rep('README.md', [('| [work/](work/README.md) |',
    '| [23-REVIEW-ROUTE-AND-DRY-RUN.md](23-REVIEW-ROUTE-AND-DRY-RUN.md) | Z-06 reviewer routes per data class and the dry-run review |\n| [work/](work/README.md) |')])
rep('17-MASTER-PLAN-STATUS.md', [("path for public content.",
    "path for public content.\n\n"
    f"**2026-11-08, Z-06.** The founder confirmed the relay route for public content only. A dry-run review of six plan\n"
    f"documents ran through OCR rules on OpenCode's relay model ({run['status']}; {len(F)} findings, {acc} proposed\n"
    f"ACCEPTED; 23). GATE-REV-01 is MET: the founder route plus the qualified advisory route. Z-06 is DONE_UNREVIEWED.")])
rep('17-MASTER-PLAN-STATUS.md', [('| GATE-REV-01 | NOT MET: route authorized (DEC-01: founder T2 sign-off, OCR on ChatGPT as advisory); Z-06 dry run pending |',
    '| GATE-REV-01 | MET: founder T2 sign-off plus OCR via OpenCode relay (advisory, public content only); dry run done (23) |')])

def load(n): return list(csv.DictReader(open('registry/' + n, encoding='utf-8')))
def save(n, rows_):
    o = io.StringIO(); w = csv.DictWriter(o, fieldnames=SCHEMAS[n], lineterminator='\n'); w.writeheader(); w.writerows(rows_)
    open('registry/' + n, 'w', encoding='utf-8').write(o.getvalue()); print('saved', n)
B = load('zain-task-backlog.csv')
for r in B:
    if r['id'] == 'Z-06':
        r['status'] = 'DONE_UNREVIEWED'; r['blockers'] = ''
        r['status_evidence'] = (f"23-REVIEW-ROUTE-AND-DRY-RUN.md: routes per data class confirmed by the founder 2026-11-08; dry run {run['id']} "
                                f"({run['status']}, {len(F)} findings, Finding schema in work/z06_findings.json); route config redacted")
save('zain-task-backlog.csv', B)
G = load('zain-acceptance-gates.csv')
for g in G:
    if g['gate_id'] == 'GATE-REV-01':
        g['status'] = 'MET'
        g['evidence'] = (f"23-REVIEW-ROUTE-AND-DRY-RUN.md: founder decision record (routes per data class, 2026-11-08) and dry-run findings "
                         f"file work/z06_findings.json ({run['id']}); qualified routes: founder (T2) and OCR via OpenCode relay (advisory, public only)")
save('zain-acceptance-gates.csv', G)
