"""Record Z-08 (toolchain pins in the build shell). Run from docs/zain-master-plan."""
import csv, io, pathlib, sys
sys.path.insert(0, 'tools'); sys.dont_write_bytecode = True
from zmp import SCHEMAS

def rep(f, pairs):
    p = pathlib.Path(f); t = p.read_text(encoding='utf-8')
    for a, b in pairs:
        if t.count(a) != 1: sys.exit(f'NOT UNIQUE/MISSING {f}: {a[:70]}')
        t = t.replace(a, b)
    p.write_text(t, encoding='utf-8'); print('edited', f)

rep('20-R0A-ADMISSION-RECORD.md', [
    ('| Node | 26.12.1 (`engines.node`) | 24.19.0 | Z-08 |', '| Node | 26.12.1 (`engines.node`) | 24.19.0 global; **v26.12.1 in the build shell** (Z-08) | none in the build shell |'),
    ('| pnpm | 12.14.0 (`packageManager`) | 9.12.0 (global npm install) | Z-08 |', '| pnpm | 12.14.0 (`packageManager`) | 9.12.0 global; **12.14.0 in the build shell** (Z-08) | none in the build shell |'),
    ('| WSL | needed only for the embedded Linux CLI archive | no distribution registered | §3 |',
     '| WSL | needed only for the embedded Linux CLI archive | no distribution registered | §3 |\n\n'
     '**Toolchain manifest (Z-08, 2026-11-08).** Fetched with founder approval by `work/z08_toolchain.py`; used only in a\n'
     'session that dot-sources `work/z08_build_shell.ps1`, which prepends both folders to PATH for that process.\n\n'
     '| Tool | File and source | SHA-256 (verified against) | Path under `D:\\zain-build\\tools` |\n'
     '|---|---|---|---|\n'
     '| Node 26.12.1 (npm 11.20.0 bundled) | `node-v26.12.1-win-x64.zip`, 41,901,456 bytes, nodejs.org/dist | `b3efd5c70cba3308ed46e7e699a9b8aac075bbc6b027fcb39c84c31acc25e2b4` (release SHASUMS256.txt; its GPG signature was not checked) | `node-v26.12.1-win-x64\\node-v26.12.1-win-x64` |\n'
     '| pnpm 12.14.0 | `pnpm-win32-x64.zip`, 22,994,360 bytes, GitHub release `pnpm/pnpm` v12.14.0 | `6f0f38e917c8ce76ef31db528c357e2bfa354a1bcb16464e3cdec39e6530d784` (GitHub asset digest; pnpm publishes no checksum file) | `pnpm-12.14.0` |\n\n'
     'Check: in the build shell `node --version` = v26.12.1 and `pnpm --version` = 12.14.0; in an ordinary shell they\n'
     'are still v24.19.0 and 9.12.0. The downloaded archives are kept under `downloads\\` for re-verification.'),
])
rep('11-TASK-CONTRACTS.md', [('Node 24.19.0 / pnpm 9.12.0 vs pins.', 'toolchain pinned in the build shell since 2026-11-08 (Z-08).')])
rep('17-MASTER-PLAN-STATUS.md', [
    ('| GATE-TOOL-01 | NOT MET (Node 24.19.0, pnpm 9.12.0) |',
     '| GATE-TOOL-01 | MET in substance (build shell: Node v26.12.1, pnpm 12.14.0; MSVC, SDK, Rust recorded), recorded NOT_MET until Z-08 review |'),
    ('Q-01 waits on disk, RAM and Z-08.', 'Q-01 waits on disk, RAM and Z-08.\n\n'
     '**2026-11-08, Z-08.** With founder approval, Node 26.12.1 (41.9 MB, nodejs.org) and pnpm 12.14.0 (23.0 MB, GitHub)\n'
     'were fetched to `D:\\zain-build\\tools`, SHA-256 verified, and wired into a per-session build shell\n'
     '(`work/z08_build_shell.ps1`); the global Node and pnpm are unchanged. Manifest in 20 §2. Q-01 now waits only on\n'
     'disk (D: 15.3 GB of 30 GB) and free RAM, plus the founder\'s confirmation of 20 §8.'),
])
rep('work/README.md', [('| `record_*.py` |',
    '| `z08_toolchain.py`, `z08_build_shell.ps1` | Z-08: fetch and verify the pinned Node and pnpm; per-session build shell (20 §2) |\n| `record_*.py` |')])

def load(n): return list(csv.DictReader(open('registry/' + n, encoding='utf-8')))
def save(n, rows):
    o = io.StringIO(); w = csv.DictWriter(o, fieldnames=SCHEMAS[n], lineterminator='\n'); w.writeheader(); w.writerows(rows)
    open('registry/' + n, 'w', encoding='utf-8').write(o.getvalue()); print('saved', n)
B = load('zain-task-backlog.csv')
for r in B:
    if r['id'] == 'Z-08':
        r['status'] = 'DONE_UNREVIEWED'
        r['status_evidence'] = ('2026-11-08: Node 26.12.1 and pnpm 12.14.0 fetched with founder approval to D:\\zain-build\\tools, SHA-256 matched '
                                '(SHASUMS256.txt; GitHub asset digest); build shell shows v26.12.1 / 12.14.0, global still v24.19.0 / 9.12.0; manifest 20 §2')
    if r['id'] == 'Q-01':
        r['blockers'] = 'RESOURCE_BLOCKED: D: 15.3 GB free (needs 30 GB, Z-07) and free RAM below 6 GB; founder confirmation of 20 §8'
save('zain-task-backlog.csv', B)
G = load('zain-acceptance-gates.csv')
for g in G:
    if g['gate_id'] == 'GATE-TOOL-01':
        g['evidence'] = ('2026-11-08: build shell (work/z08_build_shell.ps1) Node v26.12.1, pnpm 12.14.0; MSVC 17.14.37710.0, Windows SDK 10.0.26100.0, '
                         'Rust 1.97.1 recorded (20 §2); MET in substance, recorded NOT_MET until Z-08 is reviewed')
save('zain-acceptance-gates.csv', G)
