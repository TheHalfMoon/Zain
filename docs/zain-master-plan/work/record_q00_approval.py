"""Record the founder's approval of the Q-00 proposals (chat, 2026-11-08). Run from docs/zain-master-plan."""
import pathlib, sys

def rep(f, pairs):
    p = pathlib.Path(f); t = p.read_text(encoding='utf-8')
    for a, b in pairs:
        if t.count(a) != 1: sys.exit(f'NOT UNIQUE/MISSING {f}: {a[:70]}')
        t = t.replace(a, b)
    p.write_text(t, encoding='utf-8'); print('edited', f)

rep('20-R0A-ADMISSION-RECORD.md', [
    ("STATUS   = REVIEW_BLOCKED: drafted by the builder; T2 needs the founder's sign-off (DEC-01). Q-01 is also\n           RESOURCE_BLOCKED (§4)",
     "STATUS   = proposals approved by the founder as drafted (chat, 2026-11-08); the §7 re-checks follow and need the\n           founder's confirmation. Q-01 is RESOURCE_BLOCKED (§4)"),
    ('| Upstream uses unpinned `stable` (`dtolnay/rust-toolchain`). Proposed local pin: 1.97.1, the current `stable` here; 1.98.0 and 1.98.1 are also installed | rustup: stable 1.97.1 (active), 1.98.0, 1.98.1 | Founder confirms the pin |',
     '| Upstream uses unpinned `stable` (`dtolnay/rust-toolchain`). **Pinned 1.97.1** (founder, 2026-11-08), the current `stable` here; 1.98.0 and 1.98.1 are also installed | rustup: stable 1.97.1 (active), 1.98.0, 1.98.1 | none |'),
    ('No WSL distribution exists here. **Proposed:** R0a', 'No WSL distribution exists here. **Decided (founder, 2026-11-08):** R0a'),
    ('| Packages outside the set | License | Proposed decision |', '| Packages outside the set | License | Decision (approved by the founder, 2026-11-08) |'),
    ("| A3 Q-00 independently reviewed | **Not yet**: this record awaits the founder's T2 sign-off (DEC-01); OCR may give an advisory pass after Z-06 |",
     "| A3 Q-00 independently reviewed | The founder approved the record as drafted (chat, 2026-11-08; DEC-01). The §7 re-checks added afterwards need the founder's confirmation; OCR may add an advisory pass after Z-06 |"),
    ("2. The founder's decisions on §5 (four special packages) and on the CLI archive route (§3).\n3. The Rust pin (§2).",
     "2. Decided 2026-11-08 (founder approved as drafted): the §5 packages, the CLI archive route (§3) and the Rust pin (§2)."),
])
