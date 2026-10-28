#!/usr/bin/env python3
"""Permanent mutation regressions for tools/plan_graph.py (Astro round-2 mutations + additions).

Each case copies the planning package into a temporary directory (deleted afterwards), applies one mutation and runs
`plan_graph.main(["--check", "--root", tmp])`. The baseline must exit 0; every mutation must exit 1. A mutation that
does not change its target file is itself a failure (the fixture went stale).

Usage: python -I tools/test_plan_graph_mutations.py   (exit 0 only if every case behaves as expected)
"""
from __future__ import annotations

import contextlib
import io
import re
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import plan_graph  # noqa: E402

CAT, REG, REP = "14_TASK_CATALOG.md", "23_ACCEPTANCE_TEST_REGISTRY.md", "GENERATED_PLAN_REPORT.md"
SUITE_ROW = "| V1-17 | CC-T01, CC-T02, CC-T03, CC-T04 |"


def row_edit(task: str, col: int, fn):
    def apply(text: str) -> str:
        out = []
        for line in text.split("\n"):
            if line.startswith(f"| {task} |"):
                f = [c.strip() for c in line.strip().strip("|").split("|")]
                if len(f) > max(col, 2):
                    f[col] = fn(f[col])
                    line = "| " + " | ".join(f) + " |"
            out.append(line)
        return "\n".join(out)
    return apply


def reg_edit(test: str, col: int, value: str):
    return row_edit(test, col, lambda _v: value)


def duplicate_row(prefix: str):
    def apply(text: str) -> str:
        lines = text.split("\n")
        for i, line in enumerate(lines):
            if line.startswith(prefix):
                return "\n".join(lines[: i + 1] + [line] + lines[i + 1:])
        return text
    return apply


def delete_row(prefix: str):
    return lambda text: "\n".join(l for l in text.split("\n") if not l.startswith(prefix))


def sub(pattern: str, repl: str):
    return lambda text: re.sub(pattern, repl, text, count=1, flags=re.M)


add = lambda extra: (lambda v: f"{v}; {extra}")
add_dep = lambda extra: (lambda v: extra if v in ("—", "") else f"{v}, {extra}")

CASES = [
    # Astro round 2 (validator-adversarial-results.json), all 18
    ("C20_add_W2b", CAT, row_edit("C-20", 5, add("W2b"))),
    ("Y08_add_BRW23", CAT, row_edit("Y-08", 5, add("BRW-AT-23"))),
    ("mandatory_depends_paid", CAT, row_edit("Q-01", 2, add_dep("F-19"))),
    ("negative_empty_guard", REG, reg_edit("T1", 4, "")),
    ("explicit_cycle", CAT, row_edit("Q-01", 2, add_dep("Q-05"))),
    ("unknown_known_family_test", CAT, row_edit("Q-01", 5, add("FWB-99"))),
    ("unknown_new_family_test", CAT, row_edit("Q-01", 5, add("SECURITY-99"))),
    ("unknown_dependency_range", CAT, row_edit("Q-01", 2, add_dep("Z-01..Z-03"))),
    ("duplicate_task", CAT, duplicate_row("| Q-01 |")),
    ("kind_typo_and_empty_guard", REG, lambda t: reg_edit("T1", 4, "")(reg_edit("T1", 1, "nge")(t))),
    ("R1_drop_inherited_R0", CAT, sub(r"(\| R1 \| [^|]+\| )R0 \+ ", r"\1")),
    ("reverse_test_range", CAT, row_edit("Q-01", 5, add("FWB-99..FWB-01"))),
    ("embedded_free_text_negative", CAT, row_edit("Q-01", 5, add("e2e: negative secret leak should fail"))),
    ("stale_generated_report", REP, sub(r"^\| R0a \| (\d+) \| [^|]+\|", r"| R0a | \1 | 999–999 |")),
    ("V1_17_add_actual_CC_T05_prereq", REG, row_edit("V1-17", 2, add_dep("V-04"))),
    ("R1_require_generic_revocation", CAT, row_edit("C-09", 5, add("PEM-GEN-01"))),
    ("duplicate_registry_id", REG, duplicate_row("| T1 |")),
    ("negative_delete_used_row", REG, delete_row("| ZCR-T18 |")),
    # additional fail-closed regressions (revision 4)
    ("dependency_range_reversed", CAT, row_edit("Q-01", 2, add_dep("B-07..B-01"))),
    ("release_member_removed_breaks_closure", CAT, sub(r"(\| R1 \| [^|]+\| R0 \+ tasks: [^|]*?)C-09, ", r"\1")),
    ("suite_member_unregistered", REG, lambda t: t.replace(SUITE_ROW, SUITE_ROW[:-2] + ", CC-T99 |")),
    ("suite_cycle", REG, lambda t: t.replace(SUITE_ROW, SUITE_ROW + "\n| CC-T01 | V1-17 |")),
    ("negative_kind_uppercase", REG, reg_edit("T1", 1, "NEG")),
    ("estimate_unparseable", CAT, row_edit("Q-01", 6, lambda _v: "about a week")),
    ("drift_traceability", "15_TRACEABILITY_MATRIX.md", sub(r"REGISTERED = (\d+)", r"REGISTERED = 9\1")),
]


def run(root: Path) -> tuple[int, str]:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = plan_graph.main(["--check", "--root", str(root)])
    return code, buf.getvalue()


def main() -> int:
    failures = 0
    with tempfile.TemporaryDirectory(prefix="zain-plan-mut-") as tmp:
        base = Path(tmp) / "base"
        shutil.copytree(ROOT, base, ignore=shutil.ignore_patterns("research", "__pycache__", "*.pyc"))
        code, out = run(base)
        ok = code == 0
        failures += not ok
        print(f"{'PASS' if ok else 'FAIL'} baseline exit={code}")
        if not ok:
            print(out)
        for name, fname, fn in CASES:
            case = Path(tmp) / name
            shutil.copytree(base, case)
            target = case / fname
            before = target.read_text(encoding="utf-8")
            after = fn(before)
            if after == before:
                failures += 1
                print(f"FAIL {name}: mutation did not change {fname} (stale fixture)")
                continue
            target.write_text(after, encoding="utf-8")
            code, out = run(case)
            ok = code == 1
            failures += not ok
            first = next((l for l in out.splitlines() if l.startswith("ERROR")), "no error reported")
            print(f"{'PASS' if ok else 'FAIL'} {name} exit={code} :: {first[:150]}")
            shutil.rmtree(case)
    print(f"cases={len(CASES) + 1} failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
