"""Record the Q-00 §7 re-check (citations and seams at v0.1.7). Run from docs/zain-master-plan."""
import csv, io, pathlib, sys
sys.path.insert(0, 'tools'); sys.dont_write_bytecode = True
from zmp import SCHEMAS

# correct the three rows the script resolved to the wrong file
p = pathlib.Path('work/q00_citations.csv'); rows = list(csv.reader(p.open(encoding='utf-8'))); fixed = 0
for r in rows[1:]:
    if r[3].startswith('.repos/') or r[4].startswith('.repos/'):
        if 'checkpointing/Utils.ts' in r[2]:
            r[3:9] = ['apps/server/src/checkpointing/Utils.ts', '', r[5], '', 'FILE_REMOVED',
                      'corrected by hand: checkpointing moved into orchestration-v2 Checkpoint*Service.ts and CheckpointRestoreSafety.ts']
        elif 'config.ts' in r[2]:
            r[3:9] = ['apps/server/src/config.ts', '', '160', '', 'RESOLVED_BY_HAND', 'L160 worktreesDir; file present at the new pin']
        fixed += 1
out = io.StringIO(); csv.writer(out, lineterminator='\n').writerows(rows); p.write_text(out.getvalue(), encoding='utf-8')
print('corrected rows:', fixed)

def rep(f, pairs):
    q = pathlib.Path(f); t = q.read_text(encoding='utf-8')
    for a, b in pairs:
        if t.count(a) != 1: sys.exit(f'NOT UNIQUE/MISSING {f}: {a[:70]}')
        t = t.replace(a, b)
    q.write_text(t, encoding='utf-8'); print('edited', f)

rep('20-R0A-ADMISSION-RECORD.md', [
    ("STATUS   = proposals approved by the founder as drafted (chat, 2026-11-08); the §7 re-checks follow and need the\n           founder's confirmation. Q-01 is RESOURCE_BLOCKED (§4)",
     "STATUS   = §1-§7 approved by the founder as drafted (chat, 2026-11-08); the §8 re-check was added afterwards and\n           awaits the founder's confirmation. Q-01 is RESOURCE_BLOCKED (§4)"),
    ("1. Re-run the R02 §10 seam inventory at the new pin, and re-check the V3 18 file:line citations against the 93\n   changed and 1 moved R11 paths.",
     "1. Done 2026-11-08: the R02 §10 seam inventory and the source citations behind V3 18 were re-checked at the new pin (§8)."),
])
t = pathlib.Path('20-R0A-ADMISSION-RECORD.md').read_text(encoding='utf-8').rstrip('\n') + '''

## 8. Citation and seam re-check at v0.1.7

V3 18 states its line references (for example "adapter L632–655") from R11 §3.2, and R02 and R11 carry the explicit
`path@36d4d711:L…` citations. All 171 cited ranges and files in R02 and R11 were re-anchored by their text at
`322f6544` (`work/q00_citations.py`, results in `work/q00_citations.csv`).

| Result | Count | Action |
|---|---|---|
| Same lines, same text | 43 | none |
| Same text, lines shifted | 71 | use the new line numbers in the CSV |
| Changed, at least 80% similar | 23 | re-read before relying on them |
| Changed, under 80% similar | 5 | `Orchestrator.ts` L12365-12411 (0.50); `DatabaseMaintenance.ts` L175-190 (0.69); `GitVcsDriver.ts` L1174-1245, checkpoint capture and restore (0.42); `ClaudeAdapterV2.ts` L9265-9536 (0.77; excluded with the Claude driver); `McpHttpServer.ts` L103/L1082 |
| Anchor text not found | 12 | `ProjectionMaintenance.ts` (4 ranges), ACP `adapter.ts` L5860-5983, `GitVcsDriverCore.ts` L1178/L422/L3704, `OrchestrationEventStore.ts` L289-300 and L453-466, `scripts/sync-reference-repos.ts`, `updateChannels.ts` L12, `DesktopEnvironment.ts` L235, `apps/server/package.json` L36 |
| File removed | 2 | `apps/server/src/checkpointing/Utils.ts` (both citations) |
| Cited as a file only, still present | 14 | none |
| Resolved by hand | 1 | `config.ts` L160 is `apps/server/src/config.ts` (`worktreesDir`) |

**Seams (R02 §10) at the new pin: all nine still exist.**

| Seam | State at v0.1.7 |
|---|---|
| S1 Runtime policy resolution | File and all 5 named symbols present |
| S2 Provider approval callbacks | Files present; the Claude part is excluded; the Codex handlers shifted (CSV) |
| S3 ACP client fs/terminal | Restructured: client file-system capabilities in `adapter.ts` L390-394 and L2313-2314; `terminal/create` in `clientTerminals.ts` L393; `AcpSessionRuntime.ts` L1791-1792 advertises `readTextFile` and `writeTextFile` as false |
| S4 Effect worker | Present; symbol found |
| S5 EventSink commit hook | Present; both symbols found |
| S6 MCP tool access | Files present; `McpHttpServer.ts` changed at the cited lines |
| S7 Git writes, worktrees, checkpoint restore | Worktree add moved from about L3704 to about L4230 of `GitVcsDriverCore.ts`; capture and restore in `GitVcsDriver.ts` changed; checkpoint restore now lives in `orchestration-v2/Checkpoint*Service.ts` with a new `CheckpointRestoreSafety.ts`, which Z-27 must re-verify |
| S8 T3 terminals | Files present |
| S9 Process spawn of providers | Files present; symbol found |

**Consequence:** no seam disappeared. Tasks that implement against these seams (the Core C-0x chain, Z-27) re-read
the changed, not-found and removed locations at the pin first.
'''
pathlib.Path('20-R0A-ADMISSION-RECORD.md').write_text(t, encoding='utf-8'); print('appended §8')
rep('17-MASTER-PLAN-STATUS.md', [("RESOURCE_BLOCKED (D: 16.5 GB, free RAM 1.6 GB).",
    "RESOURCE_BLOCKED (D: 16.5 GB, free RAM 1.6 GB).\n\n"
    "**2026-11-08, Q-00 approved.** The founder approved the admission record as drafted: package decisions, the\n"
    "LOCAL_ONLY route without the WSL archive, and Rust 1.97.1. The seam and citation re-check followed (20 §8): of 171\n"
    "cited ranges, 114 match (43 in place, 71 shifted), 28 changed, 12 lost their anchor and 1 file was removed; all nine\n"
    "seams still exist. Q-00 is DONE_UNREVIEWED until the founder confirms §8; Q-01 waits on disk, RAM and Z-08.")])
rep('work/README.md', [('`q00_license_listing.csv`, `q00_r11_delta.csv` | V3 Q-00 evidence: pin inventory, lockfile digests, shipped-closure licenses, R11 deltas (20) |',
    '`q00_license_listing.csv`, `q00_r11_delta.csv`, `q00_citations.csv` | V3 Q-00 evidence: pin inventory, lockfile digests, shipped-closure licenses, R11 deltas, citation and seam re-check (20) |')])

def load(n): return list(csv.DictReader(open('registry/' + n, encoding='utf-8')))
def save(n, rows_):
    o = io.StringIO(); w = csv.DictWriter(o, fieldnames=SCHEMAS[n], lineterminator='\n'); w.writeheader(); w.writerows(rows_)
    open('registry/' + n, 'w', encoding='utf-8').write(o.getvalue()); print('saved', n)
B = load('zain-task-backlog.csv')
for r in B:
    if r['id'] == 'Q-00':
        r['status'] = 'DONE_UNREVIEWED'
        r['status_evidence'] = ('20-R0A-ADMISSION-RECORD.md: §1-§7 approved by the founder as drafted (chat, 2026-11-08; pin v0.1.7 = 322f6544, '
                                'package decisions, LOCAL_ONLY route, Rust 1.97.1); §8 citation and seam re-check added after approval, awaiting confirmation')
        r['blockers'] = ''
save('zain-task-backlog.csv', B)
