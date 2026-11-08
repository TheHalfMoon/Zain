#!/usr/bin/env python3
"""Mutation suite for tools/zmp.py.

Each case copies docs/zain-master-plan to a temporary directory, applies one seeded defect and asserts that
`zmp check` reports the EXACT expected error code (not merely a non-zero exit). The unmodified copy must pass.

Run: python -I docs/zain-master-plan/tools/test_zmp_mutations.py
"""
from __future__ import annotations

import csv
import importlib.util
import io
import shutil
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True  # never leave __pycache__ in the repository (plan_graph is imported)

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
spec = importlib.util.spec_from_file_location("zmp", HERE / "zmp.py")
zmp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(zmp)  # type: ignore[union-attr]

# Load the V3 catalog once and reuse it (it is read-only input for every case).
_base = zmp.Checker(ROOT, zmp.DEFAULT_V3)
_base.load_v3()
V3_CACHE = (_base.v3_tasks, _base.v3_tests, _base.v3_catalog_rows, list(_base.errors))


def run(root: Path) -> list[str]:
    ck = zmp.Checker(root, zmp.DEFAULT_V3)

    def cached_v3():
        ck.v3_tasks, ck.v3_tests, ck.v3_catalog_rows = V3_CACHE[0], V3_CACHE[1], V3_CACHE[2]
        ck.errors.extend(V3_CACHE[3])
    ck.load_v3 = cached_v3  # type: ignore[method-assign]
    ck.check_core()
    for p in zmp.render(root, write=False):
        code, _, msg = p.partition(": ")
        ck.err(code, msg)
    return ck.errors


def rows(root: Path, name: str) -> list[dict]:
    return list(csv.DictReader(io.StringIO((root / "registry" / name).read_text(encoding="utf-8"))))


def save(root: Path, name: str, data: list[dict]):
    out = io.StringIO()
    w = csv.DictWriter(out, fieldnames=zmp.SCHEMAS[name], lineterminator="\n")
    w.writeheader()
    for r in data:
        w.writerow({k: r.get(k, "") for k in zmp.SCHEMAS[name]})
    (root / "registry" / name).write_text(out.getvalue(), encoding="utf-8")


def edit(name: str, key: str, ident: str, **changes):
    def f(root: Path):
        data = rows(root, name)
        hit = [r for r in data if r[key] == ident]
        assert hit, f"{ident} not found in {name}"
        hit[0].update(changes)
        save(root, name, data)
    return f


def append(name: str, row: dict):
    def f(root: Path):
        data = rows(root, name)
        data.append(row)
        save(root, name, data)
    return f


def dup(name: str, key: str, ident: str):
    def f(root: Path):
        data = rows(root, name)
        data.append(dict(next(r for r in data if r[key] == ident)))
        save(root, name, data)
    return f


def text_edit(fname: str, old: str, new: str):
    def f(root: Path):
        p = root / fname
        t = p.read_text(encoding="utf-8")
        assert old in t, f"'{old[:40]}' not in {fname}"
        p.write_text(t.replace(old, new, 1), encoding="utf-8")
    return f


def raw_append(name: str, line: str):
    def f(root: Path):
        p = root / "registry" / name
        p.write_text(p.read_text(encoding="utf-8") + line + "\n", encoding="utf-8")
    return f


B, E, G, C, S, R, J = ("zain-task-backlog.csv", "zain-dependency-edges.csv", "zain-acceptance-gates.csv",
                       "zain-capability-matrix.csv", "zain-source-registry.csv", "zain-risk-register.csv",
                       "zain-ux-journeys.csv")

CASES = [
    ("dangling dependency", edit(B, "id", "Z-08", deps="Z-07, Z-99"), "E-DEP-DANGLING"),
    ("cycle through a gate edge", append(E, {"from": "Q-01", "to": "Z-07", "type": "gate", "source": "ZMP", "note": "x"}), "E-DEP-CYCLE"),
    ("duplicate task id", dup(B, "id", "Z-03"), "E-ID-DUP"),
    ("empty acceptance criteria", edit(B, "id", "Z-11", acceptance=""), "E-EMPTY"),
    ("DONE without evidence", edit(B, "id", "Z-03", status="DONE", status_evidence=""), "E-DONE-NO-EVIDENCE"),
    ("PAID task in mandatory milestone", edit(B, "id", "Z-11", cost_class="PAID"), "E-PAID-MANDATORY"),
    ("COPY from a rejected source", edit(C, "cap_id", "CAP-20", decision="COPY", source_ids="SRC-ROO"), "E-CAP-REJECTED-SOURCE"),
    ("HIGH risk without mitigation", edit(R, "risk_id", "RK-14", mitigation_tasks=""), "E-RISK-UNMITIGATED"),
    ("gate relies on later-milestone task", edit(G, "gate_id", "GATE-PRIV-01", tasks="Z-01;Z-11"), "E-GATE-LATER"),
    ("unknown test id on a task", edit(B, "id", "Z-13", tests="GATE-J06, FWB-99"), "E-TEST-UNKNOWN"),
    ("unknown V3 test on a gate", edit(G, "gate_id", "GATE-ISO-01", v3_tests="FWB-02;XYZ-01"), "E-TEST-UNKNOWN"),
    ("missing contract section", text_edit("11-TASK-CONTRACTS.md", "### Z-18 —", "### Z18 —"), "E-DOC-NO-CONTRACT"),
    ("risk severity inconsistent with score", edit(R, "risk_id", "RK-08", severity="LOW"), "E-RISK-SEVERITY"),
    ("V3 row drifted from catalog", edit(B, "id", "Q-03", milestone="R0b"), "E-V3-DRIFT"),
    ("backlog dependency without edge", edit(B, "id", "Z-21", deps="F-16, Z-14"), "E-EDGE-MISMATCH"),
    ("dependency on a later milestone", edit(B, "id", "Z-13", deps="Q-05, Z-11"), "E-DEP-LATER"),
    ("generated END marker removed", text_edit("10-ROADMAP-AND-CRITICAL-PATH.md", "<!-- GENERATED:END zmp-roadmap -->", ""), "E-GEN-MARKER"),
    ("generated block hand-edited", text_edit("10-ROADMAP-AND-CRITICAL-PATH.md", "| M0 | 8", "| M0 | 9"), "E-GEN-DRIFT"),
    ("doc mentions unknown task", text_edit("13-RISKS-AND-OPEN-DECISIONS.md", "| Z-06, every T2 gate |", "| Z-06, Z-97 |"), "E-DOC-DANGLING"),
    ("doc mentions unknown decision", text_edit("13-RISKS-AND-OPEN-DECISIONS.md", "Recommendation | Unblocks", "Recommendation (see DEC-99) | Unblocks"), "E-DOC-DANGLING"),
    ("ADAPT with unverified license", edit(S, "src_id", "SRC-OCR", license_state="UNVERIFIED"), "E-SRC-UNVERIFIED-REUSE"),
    ("ADAPT of strong copyleft", edit(S, "src_id", "SRC-ZED", decision="ADAPT"), "E-SRC-COPYLEFT"),
    ("release gate omits a task", edit(G, "gate_id", "GATE-R0-EXIT", tasks="A-01;A-02"), "E-GATE-RELEASE-INCOMPLETE"),
    ("reversed estimate", edit(B, "id", "Z-11", est_pw="2–1"), "E-EST"),
    ("malformed row", raw_append(B, "Z-99,ZMP,M0"), "E-SCHEMA"),
    ("journey without gate", edit(J, "journey_id", "J05", gates=""), "E-JOURNEY-NO-GATE"),
    ("capability lands later than claimed", edit(C, "cap_id", "CAP-17", first_milestone="R0a"), "E-CAP-LATE"),
    ("DONE before prerequisites", edit(B, "id", "Z-08", status="DONE", status_evidence="x"), "E-DONE-BEFORE-DEPS"),
    ("gate MET while its task is open", edit(G, "gate_id", "GATE-PRIV-02", status="MET", evidence="x"), "E-GATE-MET-OPEN-TASK"),
    ("dependency on the optional paid track", edit(B, "id", "Z-22", deps="F-11, F-19"), "E-DEP-OPTIONAL"),
    ("first-release capability without gate", edit(C, "cap_id", "CAP-46", gates=""), "E-CAP-NO-GATE"),
    ("BLOCKED without reason", edit(B, "id", "Z-03", status="BLOCKED", blockers=""), "E-BLOCKED-NO-REASON"),
    ("bare GPL-3.0 reuse", edit(S, "src_id", "SRC-ORCA", license_spdx="GPL-3.0"), "E-SRC-COPYLEFT"),
    ("GPL hidden behind LGPL in a conjunction", edit(S, "src_id", "SRC-ORCA", license_spdx="GPL-3.0-only AND LGPL-2.1"), "E-SRC-COPYLEFT"),
    ("ADAPT capability with only INTEGRATE sources", edit(C, "cap_id", "CAP-20", source_ids="SRC-MONACO"), "E-CAP-SOURCE-COMPAT"),
]


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    failures = 0
    with tempfile.TemporaryDirectory() as td:
        base = Path(td) / "base"
        shutil.copytree(ROOT, base, ignore=shutil.ignore_patterns("__pycache__"))
        errs = run(base)
        if errs:
            print("BASELINE FAILED:", errs[:3])
            return 1
        print("baseline: pass (0 errors)")
        for i, (name, mutate, code) in enumerate(CASES, 1):
            case = Path(td) / f"case{i:02d}"
            shutil.copytree(base, case)
            mutate(case)
            errs = run(case)
            codes = {e.split(":", 1)[0] for e in errs}
            ok = code in codes
            failures += 0 if ok else 1
            print(f"{'ok  ' if ok else 'FAIL'} {i:02d} {name}: expected {code}; got {sorted(codes) or 'no errors'}")
    print(f"cases={len(CASES)} failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
