#!/usr/bin/env python3
"""Deterministic validator and generator for the Zain V3 planning package.

Single source of truth:
  14_TASK_CATALOG.md            tasks, dependencies, estimates, tests, release membership (§16)
  23_ACCEPTANCE_TEST_REGISTRY.md every coded acceptance test: prerequisites, phase, guard/mutant/fixture/failure
  13_REQUIREMENTS_REGISTER.md   requirements

Outputs (overwritten):
  GENERATED_PLAN_REPORT.md      totals, release tiers, critical paths, calendar, validation results
  15_TRACEABILITY_MATRIX.md     requirement -> task -> registered test mapping
  ZAIN_V3_MASTER_PLAN.md        only the block between GENERATED markers

Usage: python -I tools/plan_graph.py [--check]
  --check: exit 1 on any validation error (no files written).
Planning artifact only; it does not build or run the product.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PHASES = ["P−1′", "P0", "P1", "P2-N", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9", "P10", "PD"]
PIDX = {p: i for i, p in enumerate(PHASES)}
HEADING_PHASE = [
    ("## P−1′", "P−1′"), ("## P0", "P0"), ("## P1", "P1"), ("## P2-N", "P2-N"), ("## P2 ", "P2"),
    ("## P3", "P3"), ("## P4", "P4"), ("## P5", "P5"), ("## P6", "P6"), ("## P7", "P7"), ("## P8", "P8"),
    ("## P9", "P9"), ("## P10", "P10"), ("## PD", "PD"),
]
TASK_ID = re.compile(r"^[A-Z]-\d{2}$")
# Coded test identifiers. Order matters (longest families first).
TEST_FAMILIES = [
    r"BRW-AT-\d{2}", r"BRW-[A-Z]\d{2}", r"ZCR-T\d{2}", r"ZCR-Q\d{2}", r"ES-AT-\d{2}", r"DG-N\d{2}", r"DG-B\d",
    r"DG-P\d{2}", r"CC-T\d{2}", r"V1-\d{2}", r"AT-\d{2}", r"T\d{1,2}b?", r"R\d{1,2}", r"W\d+b?", r"B\d{1,2}",
    r"N\d{1,2}", r"D\d", r"E\d", r"COV-\d{2}", r"PEM-[A-Z]{2,5}-\d{2}", r"REC-\d{2}", r"PH-\d{2}", r"APR-\d{2}",
    r"LED-\d{2}", r"GV-\d{2}", r"FG-\d{2}", r"DM-\d{2}", r"TERM-\d{2}", r"A11Y-\d{2}", r"PROV-\d{2}", r"POL-\d{2}",
    r"EFF-\d{2}", r"SBX-\d{2}", r"RMT-\d{2}", r"EDIT-\d{2}", r"DBG-\d{2}", r"EGR-\d{2}", r"INBOX-\d{2}", r"CI-\d{2}", r"SRC-\d{2}", r"ID-\d{2}", r"PROTO-\d{2}", r"UI-\d{2}", r"SEC12-\d{2}", r"OPID-\d{2}", r"FSG-\d{2}", r"LIC-\d{2}",
]
TOKEN_RE = re.compile(
    r"(?<![A-Za-z0-9-])(" + "|".join(f"(?:{f})" for f in TEST_FAMILIES) + r")(?:\s*(?:\.\.|–)\s*([A-Z0-9-]*?\d+b?))?(?![A-Za-z0-9])"
)


def rows(text: str):
    for line in text.splitlines():
        if line.startswith("|") and not line.startswith("|---"):
            yield [c.strip() for c in line.strip().strip("|").split("|")]


def expand_range(start: str, end: str | None) -> list[str]:
    if not end:
        return [start]
    m1 = re.match(r"^(.*?)(\d+)(b?)$", start)
    m2 = re.match(r"^(.*?)(\d+)(b?)$", end)
    if not m1 or not m2 or m1.group(3) or m2.group(3):
        return [start, end]
    prefix, a, width = m1.group(1), int(m1.group(2)), len(m1.group(2))
    b = int(m2.group(2))
    return [f"{prefix}{n:0{width}d}" for n in range(a, b + 1)]


def test_tokens(text: str) -> list[str]:
    out: list[str] = []
    for m in TOKEN_RE.finditer(text):
        out.extend(expand_range(m.group(1).replace(" ", ""), m.group(2)))
    return out


def parse_est(s: str) -> tuple[float, float]:
    nums = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", s.split("(")[0])]
    if not nums:
        return 0.0, 0.0
    return nums[0], nums[-1]


def load_tasks():
    text = (ROOT / "14_TASK_CATALOG.md").read_text(encoding="utf-8")
    tasks: dict[str, dict] = {}
    phase = None
    for line in text.splitlines():
        for prefix, ph in HEADING_PHASE:
            if line.startswith(prefix):
                phase = ph
        if line.startswith("## Product components"):
            phase = None
        if not line.startswith("| ") or line.startswith("|---"):
            continue
        f = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(f) != 9 or not TASK_ID.match(f[0]):
            continue
        tag = re.match(r"^\[(P[^\]]+)\]\s*", f[1])
        ph = tag.group(1) if tag else phase
        if ph not in PIDX:
            raise SystemExit(f"task {f[0]}: unknown phase {ph!r}")
        lo, hi = parse_est(f[6])
        tasks[f[0]] = {
            "id": f[0], "title": re.sub(r"^\[[^\]]+\]\s*", "", f[1]), "deps_raw": f[2], "tests": f[5],
            "est": (lo, hi), "reqs": f[8], "phase": ph, "superseded": f[1].startswith("SUPERSEDED"),
            "accept": f[4],
        }
    return tasks, text


def expand_deps(raw: str, tasks: dict, self_id: str, errors: list[str]) -> set[str]:
    deps: set[str] = set()
    if raw in ("—", "", "-"):
        return deps
    for part in re.split(r",\s*", raw):
        part = part.strip()
        m_all = re.match(r"^all (P[\w−′-]+)$", part)
        if m_all:
            ph = m_all.group(1)
            deps |= {t for t, v in tasks.items() if v["phase"] == ph and t != self_id and not v["superseded"]}
            continue
        m_rng = re.match(r"^([A-Z])-(\d{2})\.\.(?:[A-Z]-)?(\d{2})$", part)
        if m_rng:
            for n in range(int(m_rng.group(2)), int(m_rng.group(3)) + 1):
                tid = f"{m_rng.group(1)}-{n:02d}"
                if tid in tasks:
                    deps.add(tid)
            continue
        if TASK_ID.match(part):
            deps.add(part)
            continue
        errors.append(f"{self_id}: unparseable dependency token {part!r}")
    for d in deps:
        if d not in tasks:
            errors.append(f"{self_id}: dependency {d} does not exist")
        elif tasks[d]["superseded"]:
            errors.append(f"{self_id}: depends on superseded task {d}")
    return deps


def load_registry(errors: list[str]):
    text = (ROOT / "23_ACCEPTANCE_TEST_REGISTRY.md").read_text(encoding="utf-8")
    reg: dict[str, dict] = {}
    for f in rows(text):
        if len(f) != 9 or f[0] in ("Test", ""):
            continue
        ids = test_tokens(f[0])
        if not ids:
            continue
        prereqs = [p.strip() for p in re.split(r",\s*", f[2]) if p.strip() and p.strip() != "—"]
        for tid in ids:
            if tid in reg:
                errors.append(f"registry: duplicate test id {tid}")
            reg[tid] = {"kind": f[1], "prereqs": prereqs, "phase": f[3], "guard": f[4], "mutant": f[5],
                        "fixture": f[6], "failure": f[7], "source": f[8]}
    return reg


def load_releases(text: str, tasks: dict, errors: list[str]):
    sec = text.split("## §16 Release membership", 1)
    if len(sec) < 2:
        errors.append("14: §16 Release membership missing")
        return {}, []
    rel: dict[str, set[str]] = {}
    order: list[str] = []
    for f in rows(sec[1].split("\n## ", 1)[0]):
        if len(f) < 3 or not re.match(r"^R\d$", f[0]):
            continue
        members: set[str] = set()
        spec = f[2]
        for m in re.finditer(r"(R\d)\b", spec.split("phases:")[0]):
            members |= rel.get(m.group(1), set())
        pm = re.search(r"phases:\s*([^+;]+)", spec)
        if pm:
            for ph in [p.strip() for p in pm.group(1).split(",")]:
                members |= {t for t, v in tasks.items() if v["phase"] == ph and not v["superseded"]}
        tm = re.search(r"tasks:\s*([^;]+)", spec)
        if tm:
            for t in [x.strip() for x in tm.group(1).split(",")]:
                if t not in tasks:
                    errors.append(f"§16 {f[0]}: unknown task {t}")
                members.add(t)
        rel[f[0]] = members
        order.append(f[0])
    return rel, order


def topo(nodes: set[str], edges: dict[str, set[str]], errors: list[str]) -> list[str]:
    state: dict[str, int] = {}
    out: list[str] = []
    for n in sorted(nodes):
        if state.get(n):
            continue
        stack = [(n, iter(sorted(edges.get(n, ()))))]
        state[n] = 1
        path = [n]
        while stack:
            node, it = stack[-1]
            nxt = next(it, None)
            if nxt is None:
                stack.pop()
                path.pop()
                state[node] = 2
                out.append(node)
                continue
            if nxt not in nodes:
                continue
            if state.get(nxt) == 1:
                cyc = path[path.index(nxt):] + [nxt]
                errors.append("cycle: " + " -> ".join(cyc))
                continue
            if not state.get(nxt):
                state[nxt] = 1
                path.append(nxt)
                stack.append((nxt, iter(sorted(edges.get(nxt, ())))))
    return out  # dependencies before dependents


def longest_path(order: list[str], edges: dict[str, set[str]], tasks: dict, members: set[str], idx: int):
    best: dict[str, tuple[float, list[str]]] = {}
    for n in order:
        if n not in members:
            continue
        w = tasks[n]["est"][idx]
        prev = [best[d] for d in edges.get(n, ()) if d in best]
        base = max(prev, key=lambda x: x[0]) if prev else (0.0, [])
        best[n] = (base[0] + w, base[1] + [n])
    return max(best.values(), key=lambda x: x[0]) if best else (0.0, [])


def fmt(x: float) -> str:
    return f"{x:.2f}".rstrip("0").rstrip(".") if x % 1 else f"{x:.0f}"


def main(argv: list[str]) -> int:
    check_only = "--check" in argv
    errors: list[str] = []
    warnings: list[str] = []
    tasks, catalog_text = load_tasks()
    live = {t for t, v in tasks.items() if not v["superseded"]}
    deps = {t: expand_deps(tasks[t]["deps_raw"], tasks, t, errors) for t in live}
    reg = load_registry(errors)

    # Registry consistency: prerequisites exist; declared phase equals computed earliest phase.
    for tid, r in reg.items():
        phs = []
        for p in r["prereqs"]:
            if p not in tasks or tasks[p]["superseded"]:
                errors.append(f"registry {tid}: prerequisite {p} missing or superseded")
            else:
                phs.append(PIDX[tasks[p]["phase"]])
        computed = PHASES[max(phs)] if phs else None
        if computed and r["phase"] != computed:
            errors.append(f"registry {tid}: declared phase {r['phase']} != computed {computed}")
        if r["kind"].startswith("neg"):
            for k in ("guard", "mutant", "fixture", "failure"):
                if not r[k] or r[k] == "—":
                    errors.append(f"registry {tid}: negative test lacks {k}")

    # Test tokens in tasks -> prerequisites must be ancestors-or-self; add edges for the effective graph.
    eff = {t: set(deps[t]) for t in live}
    used: dict[str, list[str]] = {}
    for t in sorted(live):
        for tok in test_tokens(tasks[t]["tests"]):
            used.setdefault(tok, []).append(t)
            if tok not in reg:
                errors.append(f"{t}: test {tok} not in registry")
                continue
            for p in reg[tok]["prereqs"]:
                if p != t and p in live:
                    eff[t].add(p)
    order = topo(live, eff, errors)
    anc: dict[str, set[str]] = {}
    for n in order:
        s: set[str] = set()
        for d in deps[n]:
            if d in live:
                s |= {d} | anc.get(d, set())
        anc[n] = s
    for tok, users in used.items():
        if tok not in reg:
            continue
        for t in users:
            missing = [p for p in reg[tok]["prereqs"] if p != t and p not in anc.get(t, set())]
            if missing:
                errors.append(f"{t}: runs {tok} but prerequisite(s) {', '.join(missing)} are not declared ancestors")
            if PIDX[reg[tok]["phase"]] > PIDX[tasks[t]["phase"]] if reg[tok]["phase"] in PIDX else False:
                errors.append(f"{t} ({tasks[t]['phase']}): runs {tok} whose execution phase is {reg[tok]['phase']}")
    for t in live:
        for d in deps[t]:
            if d in tasks and PIDX[tasks[d]["phase"]] > PIDX[tasks[t]["phase"]]:
                errors.append(f"{t} ({tasks[t]['phase']}) depends on later-phase {d} ({tasks[d]['phase']})")

    rel, rel_order = load_releases(catalog_text, tasks, errors)
    rel_of: dict[str, str] = {}
    for r in rel_order:
        for t in rel[r]:
            rel_of.setdefault(t, r)
    for t in live:
        if tasks[t]["phase"] != "PD" and t not in rel_of:
            errors.append(f"{t}: not assigned to any release")
    for t in live:
        if t not in rel_of:
            continue
        ri = rel_order.index(rel_of[t])
        for d in eff[t]:
            if d in rel_of and rel_order.index(rel_of[d]) > ri:
                errors.append(f"{t} ({rel_of[t]}) needs {d} from later release {rel_of[d]}")
            if d not in rel_of and tasks[d]["phase"] == "PD":
                errors.append(f"{t} ({rel_of[t]}) depends on optional distribution-track task {d}")

    # Negative-test discipline: R1 tasks may not carry free-text negatives; registry negs must be fully specified.
    r1 = rel.get("R1", set())
    late_free = 0
    for t in sorted(live):
        for clause in re.split(r";", tasks[t]["tests"]):
            c = clause.strip()
            if c.lower().startswith("neg") and not test_tokens(c):
                errors.append(f"{t}: free-text negative test (register it in 23): {c!r}")
    if late_free:
        warnings.append(f"{late_free} free-text negative clauses outside R1 — guard specs due at task admission (09 §1b gate)")

    # Totals.
    def tot(ts):
        return sum(tasks[t]["est"][0] for t in ts), sum(tasks[t]["est"][1] for t in ts)

    by_phase = {p: [t for t in live if tasks[t]["phase"] == p] for p in PHASES}
    comps = [("Zain Code Review", "K-"), ("Zain Engineering System", "E-"), ("Zain Plan Mode", "L-"),
             ("Zain Browser", "Y-"), ("DeskGate", "H-")]
    v1 = rel.get("R2", set())

    # Calendar: capacity A-1 = 1 pw/calendar week (unvalidated); upkeep consumes u of capacity after R0 work.
    r0 = rel.get("R0", set())

    def calendar(ts, lo_hi):
        pre = sum(tasks[t]["est"][lo_hi] for t in ts if t in r0)
        post = sum(tasks[t]["est"][lo_hi] for t in ts if t not in r0)
        u = 0.35 if lo_hi == 0 else 0.60
        return (pre + post / (1 - u)) / 52.0

    report: list[str] = []
    report.append("# Generated Plan Report\n")
    report.append("```text")
    report.append("GENERATED_BY = tools/plan_graph.py (deterministic; do not hand-edit)")
    report.append("INPUTS = 14_TASK_CATALOG.md, 23_ACCEPTANCE_TEST_REGISTRY.md, 13_REQUIREMENTS_REGISTER.md")
    report.append(f"TASK_ROWS = {len(tasks)} (live {len(live)}, superseded {len(tasks) - len(live)})")
    report.append(f"REGISTERED_TESTS = {len(reg)}; TEST_REFERENCES_RESOLVED = {sum(len(v) for k, v in used.items() if k in reg)}")
    report.append(f"DECLARED_DEP_EDGES = {sum(len(deps[t]) for t in live)}; EFFECTIVE_EDGES_INCL_TEST_PREREQS = {sum(len(eff[t]) for t in live)}")
    report.append(f"VALIDATION_ERRORS = {len(errors)}; WARNINGS = {len(warnings)}")
    report.append("ESTIMATE_CLASS = reading-based ESTIMATE; nothing was built or run")
    report.append("```\n")
    report.append("## 1. Validation\n")
    report.append("Checks: dependency ids exist; no superseded dependency; acyclic effective graph (declared deps + test")
    report.append("prerequisites); no dependency on a later phase; every coded test reference is registered; every test's")
    report.append("prerequisites are declared ancestors of (or equal to) the task that runs it; registry phase = latest")
    report.append("prerequisite phase; every negative registry entry names guard, mutant, fixture and observable failure; no")
    report.append("free-text negative test anywhere; every release is closed under effective dependencies; no mandatory")
    report.append("task depends on the optional distribution track (PD).\n")
    report.extend([f"- ERROR: {e}" for e in errors] or ["- No validation errors."])
    report.extend([f"- WARNING: {w}" for w in warnings])
    report.append("\n## 2. Effort by phase (person-weeks, ESTIMATE)\n")
    report.append("| Phase | Live tasks | Low | High |\n|---|---|---|---|")
    for p in PHASES:
        lo, hi = tot(by_phase[p])
        report.append(f"| {p} | {len(by_phase[p])} | {fmt(lo)} | {fmt(hi)} |")
    mand = [t for t in live if tasks[t]["phase"] != "PD"]
    lo, hi = tot(mand)
    report.append(f"| **All mandatory (excl. PD)** | {len(mand)} | {fmt(lo)} | {fmt(hi)} |")
    report.append("\n## 3. Release tiers (cumulative; R-tiers defined in 14 §16)\n")
    report.append("| Release | Tasks | Effort low–high (pw) | Elapsed low–high (years) | Critical path (high est.) pw |")
    report.append("|---|---|---|---|---|")
    cp_lines = []
    for r in rel_order:
        ts = rel[r]
        lo, hi = tot(ts)
        cl, ch = calendar(ts, 0), calendar(ts, 1)
        cp_hi = longest_path(order, eff, tasks, ts, 1)
        cp_lo = longest_path(order, eff, tasks, ts, 0)
        report.append(f"| {r} | {len(ts)} | {fmt(lo)}–{fmt(hi)} | {cl:.1f}–{ch:.1f} | {fmt(cp_lo[0])}–{fmt(cp_hi[0])} |")
        cp_lines.append(f"- **{r}** (high-estimate chain): `{' → '.join(cp_hi[1])}`")
    report.append("\nElapsed time = (effort inside R0) + (effort after R0) / (1 − u), at A-1 capacity of 1 pw per calendar week;")
    report.append("u = upkeep share of capacity = 0.35 (low) / 0.60 (high) per 10 §3–§7. No acceleration, contingency or leave is")
    report.append("included. A-1 is unvalidated until P1–P3 actuals exist; re-run this script with measured capacity.\n")
    report.append("## 4. Critical paths (computed on the effective graph)\n")
    report.extend(cp_lines)
    report.append("\nFor a solo founder total effort, not the critical path, drives elapsed time (no parallel capacity).\n")
    report.append("## 5. Components\n")
    report.append("| Component | Tasks | Total pw | Inside R2 (v1) pw |\n|---|---|---|---|")
    for name, pre in comps:
        ts = [t for t in live if t.startswith(pre)]
        a, b = tot(ts)
        c, d = tot([t for t in ts if t in v1])
        report.append(f"| {name} | {len(ts)} | {fmt(a)}–{fmt(b)} | {fmt(c)}–{fmt(d)} |")
    report.append("\n## 6. Optional distribution track (PD, paid; never a dependency of a mandatory task)\n")
    report.append("| Task | Title | Est |\n|---|---|---|")
    for t in sorted(by_phase["PD"]):
        report.append(f"| {t} | {tasks[t]['title'][:90]} | {fmt(tasks[t]['est'][0])}–{fmt(tasks[t]['est'][1])} |")

    # Traceability.
    req_text = (ROOT / "13_REQUIREMENTS_REGISTER.md").read_text(encoding="utf-8")
    reqs = []
    for f in rows(req_text):
        if len(f) >= 4 and re.match(r"^(PR|SEC|NF|GOV)-\d+b?$", f[0]):
            reqs.append(f)
    for n in range(1, 19):
        reqs.append([f"CL-V1-{n:02d}", f"03F §2 V1-{n:02d}", "see 03F", "see 03F"])
    tr = ["# 15 — Traceability Matrix (generated)\n", "```text",
          "GENERATED_BY = tools/plan_graph.py from 13 + 14 + 23 (do not hand-edit)",
          "COVERAGE_RULE = REGISTERED: ≥1 live task maps the requirement AND that task runs ≥1 test registered in 23",
          "                with prerequisites satisfied; FREE_TEXT_ONLY: mapped, but only by unregistered test prose;",
          "                GAP: no live task. Mapping is accounting, not proof of semantic coverage (Astro M-3).", ]
    lines, counts = [], {"REGISTERED": 0, "FREE_TEXT_ONLY": 0, "GAP": 0}
    for f in reqs:
        rid = f[0]
        pat = re.compile(r"(?<![\w-])" + re.escape(rid) + r"(?![\w-])")
        rng = re.compile(r"(PR|NF)-(\d+)\.\.(?:PR|NF)?-?(\d+)")
        mapped = []
        for t in sorted(live):
            rq = tasks[t]["reqs"]
            hit = bool(pat.search(rq))
            for m in rng.finditer(rq):
                pre, a, b = m.group(1), int(m.group(2)), int(m.group(3))
                mm = re.match(rf"{pre}-(\d+)$", rid)
                if mm and a <= int(mm.group(1)) <= b:
                    hit = True
            mv = re.match(r"CL-V1-(\d{2})$", rid)
            if mv and f"V1-{mv.group(1)}" in test_tokens(tasks[t]["tests"]):
                hit = True
            if hit:
                mapped.append(t)
        reg_tests = sorted({tok for t in mapped for tok in test_tokens(tasks[t]["tests"]) if tok in reg})
        status = "GAP" if not mapped else ("REGISTERED" if reg_tests else "FREE_TEXT_ONLY")
        counts[status] += 1
        tests_s = ", ".join(reg_tests[:12]) + (" …" if len(reg_tests) > 12 else "")
        lines.append(f"| {rid} | {f[1][:80]} | {f[2]} | {f[3]} | {', '.join(mapped) or '—'} | {tests_s or '—'} | {status} |")
    tr.append(f"REQUIREMENTS = {len(reqs)} · REGISTERED = {counts['REGISTERED']} · FREE_TEXT_ONLY = {counts['FREE_TEXT_ONLY']} · GAP = {counts['GAP']}")
    tr.append("```\n")
    tr.append("| Req | Requirement | Pri | Phase | Tasks | Registered tests | Coverage |")
    tr.append("|---|---|---|---|---|---|---|")
    tr.extend(lines)
    for f in reqs:
        if f[2].startswith("M") and any(l.startswith(f"| {f[0]} |") and l.endswith("| GAP |") for l in lines):
            errors.append(f"requirement {f[0]} (M) has no task")

    report.append("\n## 7. Traceability summary\n")
    report.append(f"REGISTERED {counts['REGISTERED']} · FREE_TEXT_ONLY {counts['FREE_TEXT_ONLY']} · GAP {counts['GAP']} (details: 15)")

    # Master-plan generated block.
    mp = ROOT / "ZAIN_V3_MASTER_PLAN.md"
    mp_text = mp.read_text(encoding="utf-8")
    block = ["<!-- GENERATED:BEGIN release-table (tools/plan_graph.py) -->",
             "| Release | Tasks | Effort pw | Elapsed years (A-1, upkeep 35–60% after R0) |", "|---|---|---|---|"]
    for r in rel_order:
        ts = rel[r]
        lo, hi = tot(ts)
        block.append(f"| {r} | {len(ts)} | {fmt(lo)}–{fmt(hi)} | {calendar(ts, 0):.1f}–{calendar(ts, 1):.1f} |")
    lo, hi = tot(by_phase["PD"])
    block.append(f"| PD (optional paid distribution track) | {len(by_phase['PD'])} | {fmt(lo)}–{fmt(hi)} | not scheduled |")
    block.append("<!-- GENERATED:END release-table -->")
    if "<!-- GENERATED:BEGIN release-table" not in mp_text:
        errors.append("master plan: GENERATED release-table markers missing")
    new_mp = re.sub(r"<!-- GENERATED:BEGIN release-table.*?<!-- GENERATED:END release-table -->", "\n".join(block),
                    mp_text, flags=re.S)

    for e in errors:
        print("ERROR:", e)
    for w in warnings:
        print("WARNING:", w)
    print(f"tasks={len(live)} tests={len(reg)} errors={len(errors)} coverage={counts}")
    if check_only:
        return 1 if errors else 0
    (ROOT / "GENERATED_PLAN_REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    (ROOT / "15_TRACEABILITY_MATRIX.md").write_text("\n".join(tr) + "\n", encoding="utf-8")
    mp.write_text(new_mp, encoding="utf-8")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
