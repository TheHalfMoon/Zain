"""Apply Review D (source accuracy) dispositions to the source registry and capability matrix (run from docs/zain-master-plan)."""
import csv, io, sys
sys.path.insert(0, 'tools'); sys.dont_write_bytecode = True
from zmp import SCHEMAS

def load(n): return list(csv.DictReader(open('registry/' + n, encoding='utf-8')))
def save(n, rows):
    out = io.StringIO(); w = csv.DictWriter(out, fieldnames=SCHEMAS[n], lineterminator='\n'); w.writeheader(); w.writerows(rows)
    open('registry/' + n, 'w', encoding='utf-8').write(out.getvalue())

S = load('zain-source-registry.csv'); SS = {s['src_id']: s for s in S}
C = load('zain-capability-matrix.csv'); CC = {c['cap_id']: c for c in C}
assert 'SRC-RUSQLITE' not in SS, 'already applied'
DC = 'donor check 2026-11-08 (gh api, read-only)'

def upd(sid, **kw): SS[sid].update(kw)
# D-R02: restore V3 pins; current HEAD goes to 'maintained' (no silent re-pins)
upd('SRC-PSTACK', pinned_commit='ab1f702c', pin_date='2026-10-27', maintained='Active; current HEAD 6b0300214a09 (2026-11-07); re-pin is an admission event')
upd('SRC-CTK', pinned_commit='ab1f702c', pin_date='2026-10-27', maintained='Active; current HEAD 6b0300214a09 (2026-11-07); re-pin is an admission event')
upd('SRC-MONACO', pinned_commit='dbf1945df2ff', pin_date='2026-10-27', maintained='Active; current HEAD 5359a3330383, v0.57.0')
upd('SRC-VWF', pinned_commit='af8c6d32', pin_date='2026-10-27', maintained='Active; current HEAD 4beb5bcccdfb, workflow@5.4.0')
upd('SRC-DH', pinned_commit='ea8aa406', pin_date='2026-10-27', maintained='Active; current HEAD badd648db763, 0.0.2')
upd('SRC-E2E', pinned_commit='ecada2bc', pin_date='2026-10-27', maintained='Active (founder-owned, PUBLIC); current HEAD 70458aedc561')
# D-R10: separate 'recorded by V3' from 're-read this pass'
for sid in ('SRC-MLC', 'SRC-MVSA', 'SRC-WINSVC', 'SRC-CODEX', 'SRC-PLAYWRIGHT', 'SRC-CEDAR', 'SRC-ONLOOK'):
    SS[sid]['license_state'] = 'RECORDED_V3'
# D-R13 / D-R09: T3 notices and license decisions
upd('SRC-T3', notes=('Re-pin decision DEC-04; full notices obligation: nested LICENSE files found by tree scan (opencode, Ghostty, Expo, Bluesky, VoidZero) plus every entry of T3\'s notices '
    'configuration (Apache-2.0, OFL-1.1, CC0 and BSD entries per V3 R02/22 §2); license elections jszip→MIT and dompurify→Apache-2.0; removals heic-to (LGPL-3.0), '
    'electron-webauthn (no license) and @cursor/sdk (22 §2, F-20); remove donor signing (Azure Trusted Signing/jsign) and publish steps'))
# D-R08: Orca diff comments are a rewrite
upd('SRC-ORCA', components='Bounded ports: Design Mode guest scripts and capture (I-05), TUI-agent catalog + OSC 7501 (I-06), Linear (I-07), computer-use helpers (W-05); diff comments are a REWRITE behind an adapter (I-02, reference only)')
# D-R09: AI Hero pr skill exclusion
upd('SRC-AIHERO', notes='Re-pin; exclude the `pr` skill (near-verbatim third-party content per V3 R16); no "AI Hero" or personal-name branding in product')
# D-R04: Codex sandbox facts and limits
upd('SRC-CODEX', components='Windows sandbox set (S-01): restricted-token, ACL and firewall based, not AppContainer (V3 R13 F3); app-server client already in T3',
    notes=('Elevated backend needs windows-sandbox-service (REFERENCE only, requires codex-core) and admin setup; bubblewrap (LGPL-2.0) not vendored; rama is a pinned alpha (22 §1); '
           're-pin before S-01; current CLI 0.167 documents MXC / elevated / unelevated tiers'))
# D-R18 / D-R14
upd('SRC-OCR', pinned_commit='375f64cd', maintained='Active; pinned commit = v1.13.3; current v1.13.6 at 0d403392073b',
    notes='Patches Z-P1..Z-P7 need rebasing (V3 lists both Z-P1..Z-P6 and Z-P1..Z-P7; reconcile); exclude logo (brand mark); local CLI routes to a hosted provider, not authorized for private code (Z-06)')
upd('SRC-ZCORE', maintained='Founder-owned; no product change since 7af08de (merge of PR #327)')
# D-R17: founder-machine configuration details out of the registry
upd('SRC-OPENCODE', notes='Untrusted until C-24 patches')
upd('SRC-GRAFT', maintained='Active; npm @nanonets/graft 0.29.0')
upd('SRC-OLLAMA', notes='User-installed; never bundled')
upd('SRC-OPENGREP', windows_evidence='Windows builds (not re-checked)')
# D-R06 / D-R01 / D-R05: missing sources
def add(**kw):
    row = dict(src_id='', name='', repo_url='', pinned_commit='', pin_date='', license_spdx='', license_state='RECORDED_V3', maintained='Not re-checked',
               windows_evidence='-', decision='INTEGRATE', components='', rights_basis='', notes='', evidence_ref='specs/008 22_SOURCE_ADMISSION_QUALIFICATION.md')
    row.update(kw); S.append(row); SS[row['src_id']] = row
add(src_id='SRC-RUSQLITE', name='rusqlite', repo_url='https://github.com/rusqlite/rusqlite', license_spdx='MIT', components='Core ledger storage (C-03)', rights_basis='MIT (V3 records)')
add(src_id='SRC-MCPSDK', name='MCP TypeScript SDK', repo_url='https://github.com/modelcontextprotocol/typescript-sdk', license_spdx='MIT AND Apache-2.0 AND CC-BY-4.0 (mixed, per V3 22)',
    components='MCP connections (V-05)', rights_basis='Mixed licenses; ship all license texts', notes='Documentation parts under CC-BY-4.0 need attribution')
add(src_id='SRC-ACPSDK', name='Agent Client Protocol SDKs', repo_url='https://github.com/agentclientprotocol', license_spdx='Apache-2.0', components='ACP worker protocol (T3 effect-acp)', rights_basis='Apache-2.0 (V3 records)')
add(src_id='SRC-DAP', name='@vscode/debugprotocol', repo_url='https://github.com/microsoft/vscode-debugadapter-node', pinned_commit='53d9de511fc6', pin_date='2026-10-27', license_spdx='MIT',
    components='DAP types and client (I-04), primary debug decision in V3 R13', rights_basis='MIT (V3 R13)', evidence_ref='specs/008 research/R13 §1')
add(src_id='SRC-CLAUDESDK', name='Claude Agent SDK (user-provided)', repo_url='https://www.npmjs.com/package/@anthropic-ai/claude-agent-sdk', license_spdx='Commercial terms',
    license_state='PROPRIETARY', components='Loaded from a user-provided location only (B-06, F-06); never bundled', rights_basis='User accepts the provider terms', notes='Excluded from installers (PKG-01)')
add(src_id='SRC-EXCALIDRAW', name='Excalidraw', repo_url='https://github.com/excalidraw/excalidraw', license_spdx='MIT', components='Sketch layer (D-07)', rights_basis='MIT (V3 records)')
add(src_id='SRC-STYLEDICT', name='Style Dictionary', repo_url='https://github.com/style-dictionary/style-dictionary', license_spdx='Apache-2.0', components='Design token build (D-06, Z-17)', rights_basis='Apache-2.0 (V3 records)')
# capability fixes
CC['CAP-39'].update(decision='REIMPLEMENT', source_ids='SRC-ZCORE;SRC-RUSQLITE;SRC-CEDAR',
    notes='Policy decision and ledger are new modules inside the kept crates (C-03 new crates/core/src/ledger, C-05 Cedar or minimal rules); identity, git topology and framing are kept')
CC['CAP-25'].update(capability='Delegated AI code review with findings schema and IDE panel', decision='REIMPLEMENT', source_ids='SRC-OPENGREP', tasks='K-04;K-05;K-08',
    notes='Engine fork of OCR lands in R3 (CAP-60)')
CC['CAP-42'].update(capability='OS sandbox (Codex Windows sandbox set: restricted token, ACLs, firewall; not AppContainer)',
    notes='Admin prerequisites for the elevated backend; each Windows build qualified separately before DEC-06')
CC['CAP-52'].update(decision='REIMPLEMENT', source_ids='SRC-EXCALIDRAW;SRC-STYLEDICT', notes='Zain-built canvas (V3 ADR-003); element-to-source via Onlook is DEFER (SRC-ONLOOK)')
CC['CAP-05'].update(source_ids='SRC-DAP', notes='monaco-vscode-api debug override is OPTION B only and replaces monaco-editor; conditional on Z-20 / I-03')
CC['CAP-04'].update(notes='SRC-MVSA is conditional on Z-20: it replaces monaco-editor with its own editor API, which conflicts with CAP-02 unless chosen')
CC['CAP-14'].update(source_ids='SRC-MCPSDK')
CC['CAP-16'].update(source_ids='SRC-T3;SRC-ACPSDK;SRC-OPENCODE')
CC['CAP-35'].update(source_ids='SRC-PSTACK;SRC-CTK;SRC-PLAYWRIGHT')
C.append(dict(cap_id='CAP-60', pillar='B AI', capability='Review engine fork (local engine mode, qualification)', first_milestone='R3', owner_subsystem='Review service',
    decision='ADAPT', source_ids='SRC-OCR', tasks='K-01;K-02;K-03;K-10;K-11', gates='', competitor_basis='Copilot review, Bugbot, Devin Review', status='PLANNED', notes=''))
C.append(dict(cap_id='CAP-61', pillar='F Design', capability='Design Mode capture into the composer (Orca port)', first_milestone='R3', owner_subsystem='Design studio',
    decision='ADAPT', source_ids='SRC-ORCA', tasks='I-05', gates='', competitor_basis='Claude Design', status='PLANNED', notes=''))
save('zain-source-registry.csv', S); save('zain-capability-matrix.csv', C)
print('sources', len(S), 'capabilities', len(C))
