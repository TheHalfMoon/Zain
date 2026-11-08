"""Apply EGM review dispositions to the registries (run from docs/zain-master-plan)."""
import csv, io, sys
sys.path.insert(0, 'tools'); sys.dont_write_bytecode = True
from zmp import SCHEMAS

def load(n): return list(csv.DictReader(open('registry/' + n, encoding='utf-8')))
def save(n, rows):
    out = io.StringIO(); w = csv.DictWriter(out, fieldnames=SCHEMAS[n], lineterminator='\n'); w.writeheader(); w.writerows(rows)
    open('registry/' + n, 'w', encoding='utf-8').write(out.getvalue())

B = load('zain-task-backlog.csv'); T = {r['id']: r for r in B}
E = load('zain-dependency-edges.csv'); G = load('zain-acceptance-gates.csv'); GG = {g['gate_id']: g for g in G}
J = load('zain-ux-journeys.csv'); R = load('zain-risk-register.csv'); C = load('zain-capability-matrix.csv')
assert 'Z-30' not in T, 'already applied'

def edge(a, b, note): E.append({'from': a, 'to': b, 'type': 'gate', 'source': 'ZMP', 'note': note})
def newtask(**kw):
    base = dict(source='ZMP', phase='ZMP-' + kw['milestone'], status='NOT_STARTED', status_evidence='', blockers='', cost_class='FREE')
    base.update(kw)
    B.insert(next(i for i, r in enumerate(B) if r['source'] == 'V3'), base); T[base['id']] = base
def newgate(gid, typ, m, desc, meas, thr, tasks):
    g = dict(gate_id=gid, type=typ, milestone=m, description=desc, measurement=meas, threshold=thr, tasks=tasks, v3_tests='', status='NOT_MET', evidence='')
    G.append(g); GG[gid] = g

# ---- E-01 / Z-R07: no reviewer deadlock; decisions needed before Q-00 only
T['Z-06']['acceptance'] = ("At least one route is authorized in writing. For T2 work the founder (qualified reviewer) signs off, with security review per V3 ADR-011; "
    "model routes are advisory for T2 and may substitute only for T0/T1 when they are a different model family from both the builder and the provider under test and are authorized for private code; "
    "if the founder declines every route, REVIEW_BLOCKED is recorded and R0a stops at Q-00")
T['Z-25']['acceptance'] = "DEC-01, DEC-02, DEC-04, DEC-07, DEC-08 and DEC-12 have a decision, date and decider before Q-00 starts; the remaining DEC rows are decided before the milestone they unblock"
T['Z-25']['deliverables'] = T['Z-25']['deliverables'].replace('D-xx', 'DEC-xx')
edge('Z-25', 'Q-00', 'Pin (DEC-04), route (DEC-08) and build volume (DEC-12) decided before the admission record')
# ---- E-04 / A-02: G-07 impossible on private GitHub Free
T['G-07']['status'] = 'BLOCKED'
T['G-07']['blockers'] = 'DEC-03: protected branches/rulesets unavailable on private GitHub Free; replace with a local founder-signed merge procedure (G-02 + G-03 run from base) as a formal V3 amendment'
# ---- E-05/E-06/C-10: R0b harness with replay provider
newtask(id='Z-30', milestone='R0b', subsystem='Testing engine', owner='AGENT',
    title='Minimal journey harness for R0b with a deterministic replay provider',
    why='R0b gates (J01, J06, J18, J21, egress capture) need scripted runs before the full R0 suite exists; journeys with model turns need deterministic provider output.',
    deps='Q-05', deliverables=('Playwright-for-Electron harness attached to the installed build; silent NSIS install (/S) for scripted J01 with the SmartScreen step documented as manual; '
        'record/replay provider adapter that replays recorded turns deterministically; procedure to run the harness inside the isolated account (scheduled task at logon); network capture hook'),
    acceptance='J01, J06, J18 and J21 pass 3 consecutive runs on the installed build with the replay provider; one live-provider smoke run recorded separately; Electron fuses checked so automation attaches to the packaged app',
    tests='GATE-J01, GATE-J06, GATE-J18, GATE-J21', evidence_required='Harness run reports, installer SHA-256, replay fixture hashes',
    security='Replay fixtures contain no secrets; live runs use synthetic projects.', est_pw='0.75–1.25', complexity='M', risk='MEDIUM', tier='T1',
    parallel_group='R0b-product', ref='14-INDEPENDENT-REVIEWS.md E-05, E-06')
T['Z-15']['deps'] = 'F-16, Z-11, Z-13, Z-17, Z-21, Z-30'
T['Z-15']['deliverables'] = T['Z-15']['deliverables'].replace('Playwright-for-Electron (or equivalent) scripts', 'Extension of the Z-30 harness with scripts')
T['Z-15']['tests'] = 'GATE-J02, GATE-J03, GATE-J05, GATE-J07, GATE-J09, GATE-J11, GATE-J12, GATE-J15, GATE-J16, GATE-J22'
# ---- C-01: per-hunk accept/reject
newtask(id='Z-31', milestone='R0b', subsystem='Git engine', owner='AGENT',
    title='Verify or implement per-file and per-hunk accept/reject in the diff panel',
    why='J06 needs accept/reject of agent changes; T3 provides diff review and viewed-state, but per-hunk reject is not confirmed in the research.',
    deps='Q-05', deliverables='Verification on the installed build; if missing, per-hunk reject restoring the hunk from the pre-turn checkpoint, per-file accept/reject, keyboard shortcuts',
    acceptance='In a fixture turn touching 3 files, rejecting one hunk restores only that hunk; rejecting a file restores the whole file; accepted changes stay; the negative test fails if restore writes outside the hunk',
    tests='GATE-J06', evidence_required='Harness report and diff fixtures', security='Writes only inside the worktree.', est_pw='0.25–1', complexity='M', risk='MEDIUM', tier='T1',
    parallel_group='R0b-product', ref='14-INDEPENDENT-REVIEWS.md C-01')
# ---- C-05 / C-06 / A-04 / C-08
newtask(id='Z-32', milestone='R0', subsystem='Program/Governance', owner='FOUNDER',
    title='Daily-use log on the first release (10 working days) with defect list',
    why='Later tiers should start only on evidence from real use (RK-03); no gate collected that evidence.',
    deps='Z-30, Z-31', deliverables='Log of 10 working days using the R0b build for real work: tasks done, failures, workarounds, missing features; defect rows added to the backlog',
    acceptance='10 dated entries; every crash or data-loss event has a backlog row; go / adjust decision for R1 recorded',
    tests='GATE-USE-01', evidence_required='Log file and linked backlog rows', security='Log must not include secrets.', est_pw='0.5', complexity='S', risk='LOW', tier='T0',
    parallel_group='R0-quality', ref='14-INDEPENDENT-REVIEWS.md C-05')
newtask(id='Z-33', milestone='R0', subsystem='Application shell', owner='AGENT',
    title='Restore the WSL backend with a sanitized Linux CLI and parity tests (A3-09)',
    why='Q-04 disables the T3 WSL backend for R0a; V3 A3-09 requires restoration in Qualified R0 and no task existed. WSL2 processes run in a VM outside Job Objects, fs-gate and the kill switch.',
    deps='F-16', deliverables='Sanitized Linux CLI archive, identity and egress overlay parity, provider startup smoke under WSL, WSL contexts labelled UNKNOWN coverage and excluded from ProcessHost and kill-switch claims, revised estimate',
    acceptance='WSL backend starts, runs a provider turn and passes identity and egress checks under WSL; UI and claims label WSL sessions as not contained; founder WSL disks untouched',
    tests='GATE-R0-EXIT', evidence_required='Smoke log and egress capture under WSL', security='Must not modify existing WSL VHDX files; WSL is outside Windows containment.', est_pw='1–2', complexity='M', risk='MEDIUM', tier='T2',
    parallel_group='R0-product', ref='specs/008 OPUS packet §D A3-09')
newtask(id='Z-34', milestone='R0', subsystem='UI architecture', owner='AGENT',
    title='User, install and troubleshooting documentation for the first releases',
    why='The Definition of Done requires installation, user-workflow and troubleshooting documentation; G-06 covers governance documents only.',
    deps='Z-22, F-16', deliverables='Install/uninstall guide (unsigned build, SmartScreen), first-run and model setup, journey how-tos, known limitations (no mediation or injection control before R1), troubleshooting and log collection',
    acceptance='A tester following only the guide completes J01, J03, J04 and J06 in the isolated account; every known limitation in 02 §3 appears in the guide',
    tests='GATE-R0-EXIT', evidence_required='Guide and one guided tester run log', security='No credentials in examples.', est_pw='0.5–1', complexity='S', risk='LOW', tier='T0',
    parallel_group='R0-quality', ref='12-TEST-QA-AND-DEFINITION-OF-DONE.md §2')
# ---- E-12 / A-08: isolated account and provider credentials
GG['GATE-ISO-01']['threshold'] = 'exists, non-admin; only synthetic fixtures plus the one declared provider login (A5/A6)'
T['Z-09']['acceptance'] = 'Account exists and is non-admin; its profile holds no T3 or Claude state; the only provider state is the route declared in Z-10'
T['Z-10']['deliverables'] += ('; provider CLI installed in the isolated account with founder approval of the download; how the login is made available to a per-session CODEX_HOME with Zain-only MCP config (V3 18) '
                              'is specified and tested without copying tokens into Zain files')
# ---- E-11: RAM threshold provisional; re-check
GG['GATE-RES-01']['threshold'] = ('at least max(30 GB, 2x measured Q-04 peak) disk and at least 6 GB free RAM, both PROVISIONAL until the first measured build; '
                                  're-checked before every build-heavy task (Q-04, reference runs, 50k fixture, Rust Core target)')
# ---- E-14: editor decision before Monaco
T['Z-20']['deps'] = ''
edge('Z-20', 'F-17', 'Editor-path decision before Monaco integration')
# ---- E-15
edge('Z-17', 'F-14', 'Design tokens precede the contrast and focus pass')
T['Z-17']['acceptance'] = T['Z-17']['acceptance'].replace('every text/background token pair meets', 'every declared foreground/background pairing in the token file meets')
# ---- E-17
T['Z-03']['deliverables'] += '; inventory of public forks, refs/pull/*, Actions logs and artifacts, releases and wiki (forks survive a visibility change)'
# ---- C-02 / B-02 / B-09 / B-10: gateway scope, hosted agents, endpoint identity, server-side classification
T['Z-11']['deliverables'] = ('Server-side data classification: workspace content is at least private-code, callers may only raise the class, unknown fails closed; '
    'route registry with founder-set data_classes_allowed covering both raw OpenAI-compatible endpoints (run through the existing OpenCode worker as the tool loop) and hosted agent CLIs (Codex, ACP); '
    'pre-session check of each hosted agent\'s effective base URL and provider config (refuses the OpenCode third-party relay and any unauthorized route); '
    'local endpoints bound to their owning process image or started with a per-session token; probe runner (tool_calls, json_schema, context, fim, latency); '
    'per-route token and time budgets; endpoint settings UI; local-model capability report on 20 fixture tasks per role')
T['Z-11']['acceptance'] = ('Probes record capabilities for a local endpoint; a task needing tool calls is refused for a route whose probe failed, with a visible reason; '
    'a hosted agent session whose effective endpoint is not authorized for the project data class is refused (network capture shows no request); '
    'a spoofed localhost listener with the wrong process image is refused; a budget cap stops requests; negative tests fail with each guard removed')
T['Z-11']['tests'] = 'GATE-MODEL-01, GATE-MODEL-02, GATE-J03'
T['Z-11']['security'] = ('Controls only routes Zain launches or configures; agents that read files or open connections themselves remain UNMEDIATED until R1 (C-17) and S-04.')
# ---- C-03
GG['GATE-PERF-07']['threshold'] = ('p50 at most 600 ms to first suggestion with the named recommended local model (PROVISIONAL); '
                                   'if not met the gate is NOT_MET and local completion ships disabled with a recorded limitation')
newgate('GATE-MODEL-02', 'PERFORMANCE', 'R0', 'Measured local-model capability per role is reported to the user',
        'Z-11 capability report: success rate on 20 fixture tasks per role (agent_edit, completion, review) for each local route',
        'report exists and onboarding shows the measured limits; no route is offered for a role whose success rate is below 50% (PROVISIONAL)', 'Z-11')
newgate('GATE-USE-01', 'USABILITY', 'R0', 'Daily-use evidence on the first release before R1 work starts', 'Z-32 daily-use log',
        '10 working days logged; crash and data-loss events have backlog rows; go/adjust decision recorded', 'Z-32')
for jid, m, name, tasks in (('J21', 'R0b', 'Use the integrated terminal', 'Z-30'), ('J22', 'R0', 'Search and navigate project files', 'Z-15')):
    newgate('GATE-' + jid, 'JOURNEY', m, f'Journey {jid}: {name}',
            "Scripted run on the installed build: happy path plus the journey's failure path (08 doc)", 'passes in 3 consecutive runs', tasks)
J.append(dict(journey_id='J21', name='Use the integrated terminal', first_milestone='R0b', full_milestone='R1',
              entry_point='Terminal panel: new terminal (PowerShell, Git Bash, wsl.exe as a shell)', tasks='Q-05;Z-30;C-25', gates='GATE-J21',
              failure_recovery='Hung process: kill from the panel; from R1 ProcessHost kills the whole job tree (WSL excluded)', status='PLANNED'))
J.append(dict(journey_id='J22', name='Search and navigate project files', first_milestone='R0', full_milestone='R1',
              entry_point='File explorer; project search; open file from results', tasks='F-16;Z-15;Z-28', gates='GATE-J22',
              failure_recovery='Search on a huge repository is cancellable; ignored files excluded', status='PLANNED'))
GG['GATE-J01']['tasks'] = 'F-11;Z-22;Z-30'; GG['GATE-J06']['tasks'] = 'Z-13;Z-30;Z-31'; GG['GATE-J18']['tasks'] = 'Z-27;Z-30'
GG['GATE-J03']['tasks'] = 'Z-11;Z-15'; GG['GATE-PRIV-04']['tasks'] = 'F-05;Q-03;Z-30'
# ---- C-04: R0-specific failure paths
for j in J:
    if j['journey_id'] == 'J13': j['failure_recovery'] = 'R0: in-flight turn marked interrupted and can be re-sent; R2: resume with a context capsule (M-05)'
    if j['journey_id'] == 'J11': j['failure_recovery'] = 'R0: runner crash keeps output and the user can stop the turn; R2: budgets stop loops'
    if j['journey_id'] == 'J06': j['tasks'] = 'F-16;Z-13;Z-31;Z-15;K-05'
T['Z-21']['acceptance'] = T['Z-21']['acceptance'].replace('pending approvals are visible', 'pending supervised-mode prompts are re-shown or the turn is marked interrupted')
# ---- C-11 / B-07: concrete guard values and OneDrive placeholders
T['Z-27']['deliverables'] += '; quarantine under the Zain data directory per project, retained 14 days, capped at 2 GB or 10% of free space (PROPOSED values)'
T['Z-19']['deliverables'] += ('; proposed values: bulk threshold 25 entries, disk reserve max(5 GB, 10% of volume); policy for OneDrive Files On-Demand placeholders '
                              '(cloud-file reparse points): refuse OneDrive-hosted workspaces in R1 unless the founder allowlists the cloud-file reparse tag')
# ---- B-06: editor launch through .cmd shims
T['Z-13']['acceptance'] = ('From a diff line, a chat file reference and a terminal path, the configured editor opens at file:line; the launcher resolves the editor to its .exe (never a .cmd shim through cmd.exe) '
                           'or applies cmd-specific escaping; negative tests with &, %, ^ and quote characters in file names run no extra command; an external edit appears in the workbench diff within 2 s')
# ---- B-03: per-provider supervised-mode prompt test
GG['GATE-SEC-01']['measurement'] = 'Settings inspection, attempt to select Full access, and a per-provider test that a file write and a network command each raise a supervised prompt'
GG['GATE-SEC-01']['threshold'] = 'Supervised default; Full access absent; every provider shipped in the release prompts in the test, providers that cannot (OpenCode, Pi until C-24) are disabled or labelled unsupervised'
# ---- B-04: secret exposure, not only storage
GG['GATE-SEC-02']['threshold'] = '0 credentials in Zain-owned files; residual same-user exposure (Credential Manager/DPAPI, provider CLI files) recorded as a known limitation until S-01'
# ---- A-05: capability milestone consistent with its tasks
for c in C:
    if c['cap_id'] == 'CAP-43':
        c['first_milestone'] = 'R2'; c['notes'] = 'Y-00 hardening lands in R0b; lanes and the connection-level egress proxy land in R2'
    if c['cap_id'] == 'CAP-20': c['tasks'] = 'F-16;Z-31;Z-15'
    if c['cap_id'] == 'CAP-10': c['notes'] = 'WSL as a terminal shell works from R0b; the T3 WSL backend returns in R0 (Z-33); WSL is outside Windows containment'
    if c['cap_id'] == 'CAP-06': c['gates'] = 'GATE-J02;GATE-J22'
    if c['cap_id'] == 'CAP-07': c['capability'] = 'Local-only code index (text and symbols; embeddings deferred per V3 ADR-006)'
# ---- A-09: embeddings deferred (V3 ADR-006 defers vector search)
T['Z-28']['title'] = 'Local-only code index: ripgrep search and tree-sitter symbol index (embeddings deferred)'
T['Z-28']['deliverables'] = ('Index service in the forked Server: rg-backed text search, tree-sitter symbol tables for TS/JS, Python, Rust, Go, C#, incremental update from the file watcher, '
                             'context-retrieval API used by agent prompts and the editor; embeddings only after a V3 ADR-006 amendment')
T['Z-28']['acceptance'] = T['Z-28']['acceptance'].replace('embeddings never leave the machine (network capture)', 'zero egress (network capture)')
# ---- E-02: founder review bandwidth
R.append(dict(risk_id='RK-25', category='Process', title='Founder review bandwidth becomes the bottleneck',
              description='About 35 T2 tasks in R0a-R0 need independent review; if the founder is the only authorized route, review waits dominate the schedule (estimates exclude review time).',
              likelihood='4', impact='3', severity='HIGH', mitigation_tasks='Z-06', gates='GATE-REV-01', owner='FOUNDER', status='OPEN', evidence=''))
# ---- release gates: first release = R0b (DEC-07)
GG['GATE-R0B-EXIT']['description'] = 'First release: founder daily driver and tester build for named private recipients (DEC-07); no mediation claims'
GG['GATE-R0B-EXIT']['tasks'] += ';Z-30;Z-31'
GG['GATE-R0-EXIT']['tasks'] += ';Z-32;Z-33;Z-34'
GG['GATE-R0-EXIT']['description'] = 'Zain 1.0 qualified release candidate (no mediation claims)'
GG['GATE-R1-EXIT']['tasks'] = GG['GATE-R1-EXIT']['tasks']  # unchanged

save('zain-task-backlog.csv', B); save('zain-dependency-edges.csv', E); save('zain-acceptance-gates.csv', G)
save('zain-ux-journeys.csv', J); save('zain-risk-register.csv', R); save('zain-capability-matrix.csv', C)
print('applied review dispositions')
