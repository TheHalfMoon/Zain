#!/usr/bin/env python3
"""Zain master-plan registry tool.

Commands
  check      validate every registry CSV and the cross-references between them, the
             V3 task catalog (specs/008-wepld-v3-unified-replan) and the master-plan markdown.
  sync-v3    regenerate the V3-sourced rows of registry/zain-task-backlog.csv and the
             V3-sourced edges of registry/zain-dependency-edges.csv from the V3 catalog,
             keeping master-plan (ZMP) rows and the status columns of V3 rows.
  render     regenerate the GENERATED blocks in 11-TASK-CONTRACTS.md (ZMP task contracts)
             and 10-ROADMAP-AND-CRITICAL-PATH.md (milestone effort and dependency chains).
             `check` fails with E-GEN-DRIFT when those blocks differ from the registries.

Run from anywhere with:  python -I docs/zain-master-plan/tools/zmp.py check
Options: --root <dir of docs/zain-master-plan>  --v3 <dir of specs/008-...>

The checker is fail-closed: an unknown column, an unparseable row, a dangling reference or a
rule violation is an error and the exit code is 1. Every error message starts with a stable code
(e.g. E-DEP-DANGLING) so the mutation suite can assert the precise failure.

What it does NOT do: it does not prove that a task's acceptance criteria are adequate, that a
gate's threshold is right, or that any runtime behaviour exists. It is accounting, not proof.
"""
from __future__ import annotations

import csv
import importlib.util
import io
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # never leave __pycache__ in the repository (plan_graph is imported)

HERE = Path(__file__).resolve().parent
DEFAULT_ROOT = HERE.parent
DEFAULT_V3 = DEFAULT_ROOT.parent.parent / "specs" / "008-wepld-v3-unified-replan"

MILESTONES = ["M0", "R0a", "R0b", "R0", "R1", "R2", "R3", "R4", "R5", "R6", "R7"]
OPTIONAL_MILESTONES = ["PD"]
MIDX = {m: i for i, m in enumerate(MILESTONES)}
ALL_MILESTONES = set(MILESTONES) | set(OPTIONAL_MILESTONES)

TASK_STATUSES = {"NOT_STARTED", "IN_PROGRESS", "BLOCKED", "DONE_UNREVIEWED", "DONE", "NOT_NEEDED", "SUPERSEDED"}
DONE_STATUSES = {"DONE", "DONE_UNREVIEWED"}
OWNERS = {"AGENT", "FOUNDER", "AGENT+FOUNDER"}
COST = {"FREE", "PAID", "FOUNDER_TIME"}
TIERS = {"T0", "T1", "T2"}
COMPLEXITY = {"S", "M", "L", "U"}
LEVELS = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
DECISIONS = {"COPY", "ADAPT", "INTEGRATE", "REIMPLEMENT", "DEFER", "REJECT", "KEEP", "REFERENCE"}
REUSE_DECISIONS = {"COPY", "ADAPT", "INTEGRATE"}
GATE_TYPES = {"RELEASE", "PRIVACY", "REVIEW", "PLAN", "RESOURCE", "SECURITY", "PACKAGING", "IDENTITY",
              "PERFORMANCE", "RELIABILITY", "USABILITY", "JOURNEY"}
GATE_STATUSES = {"NOT_MET", "MET", "BLOCKED", "NOT_APPLICABLE"}
RISK_STATUSES = {"OPEN", "MITIGATING", "ACCEPTED", "CLOSED"}
CAP_STATUSES = {"PLANNED", "BUILT_UNQUALIFIED", "QUALIFIED", "DEFERRED", "REJECTED"}
# VERIFIED = LICENSE file re-read this pass; RECORDED_V3 = verified by V3 research at its pin, not re-read
LICENSE_STATES = {"VERIFIED", "RECORDED_V3", "UNVERIFIED", "UNRESOLVED", "PROPRIETARY", "NOT_APPLICABLE"}
REUSABLE_LICENSE_STATES = {"VERIFIED", "RECORDED_V3"}
_STRONG = re.compile(r"(?<![A-Za-z])(A?GPL|SSPL)(?:-\d|\b)", re.I)


def strong_copyleft(spdx: str) -> bool:
    """True if any AND-joined term is strong copyleft with no permissive OR-alternative (LGPL is not strong)."""
    for conj in re.split(r"\s+AND\s+|,|;", spdx, flags=re.I):
        alts = [a for a in re.split(r"\s+OR\s+", conj, flags=re.I) if a.strip()]
        if alts and all(_STRONG.search(a) and not re.search(r"\bLGPL", a, re.I) for a in alts):
            return True
    return False

TASK_ID = re.compile(r"^[A-Z]-\d{2}$")
ZMP_TASK_ID = re.compile(r"^Z-\d{2}$")
GATE_ID = re.compile(r"^GATE-[A-Z0-9]+(?:-[A-Z0-9]+)*$")
SRC_ID = re.compile(r"^SRC-[A-Z0-9]+$")
CAP_ID = re.compile(r"^CAP-\d{2}$")
RISK_ID = re.compile(r"^RK-\d{2}$")
JOURNEY_ID = re.compile(r"^J\d{2}$")
DEC_ID = re.compile(r"^DEC-\d{2}$")  # not D-NN: V3 uses D-01..D-08 for Design Studio tasks

SCHEMAS = {
    "zain-task-backlog.csv": ["id", "source", "milestone", "phase", "subsystem", "owner", "title", "why", "deps",
                              "deliverables", "acceptance", "tests", "evidence_required", "security", "est_pw",
                              "complexity", "risk", "tier", "cost_class", "status", "status_evidence", "blockers",
                              "parallel_group", "ref"],
    "zain-dependency-edges.csv": ["from", "to", "type", "source", "note"],
    "zain-acceptance-gates.csv": ["gate_id", "type", "milestone", "description", "measurement", "threshold", "tasks",
                                  "v3_tests", "status", "evidence"],
    "zain-capability-matrix.csv": ["cap_id", "pillar", "capability", "first_milestone", "owner_subsystem", "decision",
                                   "source_ids", "tasks", "gates", "competitor_basis", "status", "notes"],
    "zain-source-registry.csv": ["src_id", "name", "repo_url", "pinned_commit", "pin_date", "license_spdx",
                                 "license_state", "maintained", "windows_evidence", "decision", "components",
                                 "rights_basis", "notes", "evidence_ref"],
    "zain-risk-register.csv": ["risk_id", "category", "title", "description", "likelihood", "impact", "severity",
                               "mitigation_tasks", "gates", "owner", "status", "evidence"],
    "zain-ux-journeys.csv": ["journey_id", "name", "first_milestone", "full_milestone", "entry_point", "tasks", "gates",
                             "failure_recovery", "status"],
}

# Docs whose ID mentions must resolve (relative to root).
CONTRACTS_DOC = "11-TASK-CONTRACTS.md"
DECISIONS_DOC = "13-RISKS-AND-OPEN-DECISIONS.md"


def split_list(cell: str) -> list[str]:
    cell = (cell or "").strip()
    if cell in ("", "—", "-"):
        return []
    return [x.strip() for x in re.split(r"[;,]", cell) if x.strip()]


class Checker:
    def __init__(self, root: Path, v3: Path):
        self.root = root
        self.v3 = v3
        self.errors: list[str] = []
        self.data: dict[str, list[dict]] = {}
        self.v3_tasks: dict[str, dict] = {}
        self.v3_tests: set[str] = set()
        self.v3_catalog_rows: dict[str, list[str]] = {}

    def err(self, code: str, msg: str):
        self.errors.append(f"{code}: {msg}")

    # ------------------------------------------------------------------ loading
    def load_csv(self, name: str) -> list[dict]:
        path = self.root / "registry" / name
        if not path.exists():
            self.err("E-FILE-MISSING", f"registry/{name} not found")
            return []
        text = path.read_text(encoding="utf-8")
        reader = csv.reader(io.StringIO(text))
        rows = list(reader)
        if not rows:
            self.err("E-SCHEMA", f"{name}: empty file")
            return []
        header = rows[0]
        if header != SCHEMAS[name]:
            self.err("E-SCHEMA", f"{name}: header {header} != expected {SCHEMAS[name]}")
            return []
        out = []
        for n, r in enumerate(rows[1:], start=2):
            if not r or all(not c.strip() for c in r):
                self.err("E-SCHEMA", f"{name}:{n}: blank row")
                continue
            if len(r) != len(header):
                self.err("E-SCHEMA", f"{name}:{n}: {len(r)} cells, expected {len(header)}")
                continue
            d = dict(zip(header, r))
            d["_line"] = n
            out.append(d)
        return out

    def load_v3(self):
        pg = self.v3 / "tools" / "plan_graph.py"
        if not pg.exists():
            self.err("E-V3-MISSING", f"{pg} not found")
            return
        spec = importlib.util.spec_from_file_location("plan_graph", pg)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)  # type: ignore[union-attr]
        plan = mod.Plan(self.v3)
        plan.build()
        if plan.errors:
            self.err("E-V3-INVALID", f"V3 plan_graph reports {len(plan.errors)} error(s); first: {plan.errors[0]}")
        first: dict[str, str] = {}
        for r in plan.rel_order:
            for t in plan.rel[r]:
                first.setdefault(t, r)
        for t in plan.live:
            d = plan.tasks[t]
            self.v3_tasks[t] = {"phase": d["phase"], "deps": sorted(plan.deps[t]),
                                "release": first.get(t, "PD" if d["phase"] == "PD" else ""),
                                "tests": d.get("tests", ""), "est": d.get("est"), "tier": d.get("tier", ""),
                                "title": d.get("title", "")}
        self.v3_tests = set(plan.reg.keys())
        # raw catalog cells (acceptance criteria and sources are not kept by plan_graph)
        cat = (self.v3 / "14_TASK_CATALOG.md").read_text(encoding="utf-8")
        for line in cat.splitlines():
            if line.startswith("|") and not line.startswith("|---"):
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if len(cells) >= 9 and TASK_ID.match(cells[0]) and cells[0] in self.v3_tasks:
                    self.v3_catalog_rows.setdefault(cells[0], cells)

    def load(self):
        for name in SCHEMAS:
            self.data[name] = self.load_csv(name)
        self.load_v3()

    # ------------------------------------------------------------------ helpers
    def unique(self, name: str, key: str, pattern: re.Pattern) -> dict[str, dict]:
        seen: dict[str, dict] = {}
        for r in self.data.get(name, []):
            k = r[key].strip()
            if not pattern.match(k):
                self.err("E-ID-FORMAT", f"{name}:{r['_line']}: bad id '{k}'")
                continue
            if k in seen:
                self.err("E-ID-DUP", f"{name}:{r['_line']}: duplicate id {k} (first at line {seen[k]['_line']})")
                continue
            seen[k] = r
        return seen

    def need(self, name: str, r: dict, fields: list[str]):
        for f in fields:
            if not r[f].strip():
                self.err("E-EMPTY", f"{name}:{r['_line']} ({r.get(SCHEMAS[name][0])}): '{f}' is empty")

    # ------------------------------------------------------------------ checks
    def check(self) -> int:
        self.check_core()
        return self.report()

    def check_core(self) -> None:
        self.load()
        if any(e.startswith("E-SCHEMA") or e.startswith("E-FILE-MISSING") for e in self.errors):
            return
        tasks = self.unique("zain-task-backlog.csv", "id", TASK_ID)
        gates = self.unique("zain-acceptance-gates.csv", "gate_id", GATE_ID)
        caps = self.unique("zain-capability-matrix.csv", "cap_id", CAP_ID)
        srcs = self.unique("zain-source-registry.csv", "src_id", SRC_ID)
        risks = self.unique("zain-risk-register.csv", "risk_id", RISK_ID)
        journeys = self.unique("zain-ux-journeys.csv", "journey_id", JOURNEY_ID)

        self.check_tasks(tasks, gates)
        graph = self.check_edges(tasks)
        self.check_graph(tasks, graph)
        self.check_gates(gates, tasks)
        self.check_sources(srcs)
        self.check_caps(caps, tasks, gates, srcs)
        self.check_risks(risks, tasks, gates)
        self.check_journeys(journeys, tasks, gates)
        self.check_v3_parity(tasks)
        self.check_docs(tasks, gates, risks)

    def check_tasks(self, tasks: dict, gates: dict):
        name = "zain-task-backlog.csv"
        for t, r in tasks.items():
            self.need(name, r, ["source", "milestone", "phase", "subsystem", "owner", "title", "why", "deliverables",
                                "acceptance", "tests", "evidence_required", "est_pw", "complexity", "risk", "tier",
                                "cost_class", "status"])
            src = r["source"]
            if src not in ("V3", "ZMP"):
                self.err("E-ENUM", f"{name}:{r['_line']} {t}: source '{src}'")
            if src == "ZMP" and not ZMP_TASK_ID.match(t):
                self.err("E-ID-FORMAT", f"{name}:{r['_line']} {t}: ZMP tasks use Z-NN")
            if src == "V3" and ZMP_TASK_ID.match(t):
                self.err("E-ID-FORMAT", f"{name}:{r['_line']} {t}: Z-NN is reserved for ZMP tasks")
            for field, allowed in (("milestone", ALL_MILESTONES), ("owner", OWNERS), ("cost_class", COST),
                                   ("tier", TIERS), ("complexity", COMPLEXITY), ("risk", LEVELS),
                                   ("status", TASK_STATUSES)):
                if r[field] not in allowed:
                    self.err("E-ENUM", f"{name}:{r['_line']} {t}: {field} '{r[field]}' not in {sorted(allowed)}")
            if r["cost_class"] == "PAID" and r["milestone"] not in OPTIONAL_MILESTONES:
                self.err("E-PAID-MANDATORY", f"{t}: PAID task in mandatory milestone {r['milestone']}")
            if r["milestone"] in OPTIONAL_MILESTONES and r["cost_class"] != "PAID" and src == "ZMP":
                self.err("E-ENUM", f"{t}: optional-track ZMP task must be PAID")
            if r["status"] in DONE_STATUSES and not r["status_evidence"].strip():
                self.err("E-DONE-NO-EVIDENCE", f"{t}: status {r['status']} without status_evidence")
            if r["status"] == "BLOCKED" and not r["blockers"].strip():
                self.err("E-BLOCKED-NO-REASON", f"{t}: BLOCKED without blockers")
            est = r["est_pw"].strip()
            if est != "MEASURE":
                m = re.fullmatch(r"(\d+(?:\.\d+)?)(?:[–-](\d+(?:\.\d+)?))?", est)
                if not m:
                    self.err("E-EST", f"{t}: est_pw '{est}' is not N, N–M or MEASURE")
                elif m.group(2) and float(m.group(2)) < float(m.group(1)):
                    self.err("E-EST", f"{t}: est_pw '{est}' is reversed")
            for tok in split_list(r["tests"]):
                if tok not in self.v3_tests and tok not in gates:
                    self.err("E-TEST-UNKNOWN", f"{t}: test '{tok}' is neither a V3 registry test nor a gate id")
            for d in split_list(r["deps"]):
                if d not in tasks:
                    self.err("E-DEP-DANGLING", f"{t}: dependency '{d}' is not a backlog task")

    def check_edges(self, tasks: dict) -> dict[str, set[str]]:
        name = "zain-dependency-edges.csv"
        graph: dict[str, set[str]] = {t: set() for t in tasks}
        declared: dict[str, set[str]] = {t: set(split_list(r["deps"])) for t, r in tasks.items()}
        hard_edges: dict[str, set[str]] = {t: set() for t in tasks}
        seen = set()
        for r in self.data.get(name, []):
            a, b, typ, src = r["from"].strip(), r["to"].strip(), r["type"].strip(), r["source"].strip()
            key = (a, b, typ)
            if key in seen:
                self.err("E-ID-DUP", f"{name}:{r['_line']}: duplicate edge {a}->{b} ({typ})")
            seen.add(key)
            if typ not in ("hard", "gate"):
                self.err("E-ENUM", f"{name}:{r['_line']}: type '{typ}'")
            if src not in ("V3", "ZMP"):
                self.err("E-ENUM", f"{name}:{r['_line']}: source '{src}'")
            if a not in tasks or b not in tasks:
                self.err("E-DEP-DANGLING", f"{name}:{r['_line']}: edge {a}->{b} references unknown task")
                continue
            if a == b:
                self.err("E-DEP-CYCLE", f"{name}:{r['_line']}: self edge {a}")
                continue
            # edge semantics: 'from' must finish before 'to'
            graph[b].add(a)
            if typ == "hard":
                hard_edges[b].add(a)
                if src == "V3" and tasks[b]["source"] != "V3":
                    self.err("E-EDGE-SOURCE", f"{name}:{r['_line']}: V3 edge into ZMP task {b}")
            if typ == "gate" and src != "ZMP":
                self.err("E-EDGE-SOURCE", f"{name}:{r['_line']}: gate edges are ZMP-only")
        for t in tasks:
            # ordering, cycle and completion checks use declared deps too, so they do not depend on the
            # edges file being consistent (that consistency is reported separately as E-EDGE-MISMATCH)
            graph[t] |= {d for d in declared[t] if d in tasks}
            if declared[t] != hard_edges[t]:
                missing = sorted(declared[t] - hard_edges[t])
                extra = sorted(hard_edges[t] - declared[t])
                self.err("E-EDGE-MISMATCH", f"{t}: backlog deps vs hard edges differ (missing edges {missing}, extra edges {extra})")
        return graph

    def check_graph(self, tasks: dict, graph: dict[str, set[str]]):
        # cycle detection (iterative DFS)
        color = {t: 0 for t in graph}
        for start in sorted(graph):
            if color[start]:
                continue
            stack = [(start, iter(sorted(graph[start])))]
            color[start] = 1
            path = [start]
            while stack:
                node, it = stack[-1]
                nxt = next(it, None)
                if nxt is None:
                    color[node] = 2
                    stack.pop()
                    path.pop()
                    continue
                if color.get(nxt) == 1:
                    cyc = path[path.index(nxt):] + [nxt]
                    self.err("E-DEP-CYCLE", " <- ".join(cyc))
                    color[nxt] = 2
                    continue
                if color.get(nxt) == 0:
                    color[nxt] = 1
                    path.append(nxt)
                    stack.append((nxt, iter(sorted(graph[nxt]))))
        # milestone ordering: a prerequisite may not belong to a later mandatory milestone,
        # and nothing mandatory may depend on the optional paid track
        for t, prereqs in graph.items():
            mt = tasks[t]["milestone"]
            for p in prereqs:
                mp = tasks[p]["milestone"]
                if mp in OPTIONAL_MILESTONES and mt not in OPTIONAL_MILESTONES:
                    self.err("E-DEP-OPTIONAL", f"{t} ({mt}) depends on optional-track {p} ({mp})")
                elif mt in MIDX and mp in MIDX and MIDX[mp] > MIDX[mt]:
                    self.err("E-DEP-LATER", f"{t} ({mt}) depends on later-milestone {p} ({mp})")
        # completion honesty: a DONE task cannot have unfinished prerequisites
        for t, prereqs in graph.items():
            if tasks[t]["status"] in DONE_STATUSES:
                for p in prereqs:
                    if tasks[p]["status"] not in DONE_STATUSES | {"NOT_NEEDED"}:
                        self.err("E-DONE-BEFORE-DEPS", f"{t} is {tasks[t]['status']} but prerequisite {p} is {tasks[p]['status']}")

    def check_gates(self, gates: dict, tasks: dict):
        name = "zain-acceptance-gates.csv"
        for g, r in gates.items():
            self.need(name, r, ["type", "milestone", "description", "measurement", "threshold", "status"])
            if r["type"] not in GATE_TYPES:
                self.err("E-ENUM", f"{g}: type '{r['type']}'")
            if r["milestone"] not in ALL_MILESTONES:
                self.err("E-ENUM", f"{g}: milestone '{r['milestone']}'")
            if r["status"] not in GATE_STATUSES:
                self.err("E-ENUM", f"{g}: status '{r['status']}'")
            ts = split_list(r["tasks"])
            if not ts:
                self.err("E-GATE-NO-TASK", f"{g}: no verifying task")
            for t in ts:
                if t not in tasks:
                    self.err("E-GATE-DANGLING", f"{g}: task '{t}' not in backlog")
                    continue
                mt, mg = tasks[t]["milestone"], r["milestone"]
                if mg in MIDX and mt in MIDX and MIDX[mt] > MIDX[mg]:
                    self.err("E-GATE-LATER", f"{g} ({mg}) relies on later-milestone task {t} ({mt})")
            for tok in split_list(r["v3_tests"]):
                if tok not in self.v3_tests:
                    self.err("E-TEST-UNKNOWN", f"{g}: v3 test '{tok}' not in the V3 registry")
            if r["status"] == "MET" and not r["evidence"].strip():
                self.err("E-DONE-NO-EVIDENCE", f"{g}: MET without evidence")
            if r["status"] == "MET":
                for t in ts:
                    if t in tasks and tasks[t]["status"] not in DONE_STATUSES | {"NOT_NEEDED"}:
                        self.err("E-GATE-MET-OPEN-TASK", f"{g}: MET while task {t} is {tasks[t]['status']}")
        # every mandatory milestone that has tasks has a RELEASE gate covering all of them
        by_m: dict[str, set[str]] = {}
        for t, r in tasks.items():
            by_m.setdefault(r["milestone"], set()).add(t)
        rel = {r["milestone"]: r for r in gates.values() if r["type"] == "RELEASE"}
        for m in MILESTONES:
            if m in by_m and m in ("M0", "R0a", "R0b", "R0", "R1"):
                if m not in rel:
                    self.err("E-GATE-RELEASE-MISSING", f"milestone {m} has tasks but no RELEASE gate")
                    continue
                covered = set(split_list(rel[m]["tasks"]))
                missing = sorted(by_m[m] - covered)
                if missing:
                    self.err("E-GATE-RELEASE-INCOMPLETE", f"RELEASE gate for {m} omits {missing}")

    def check_sources(self, srcs: dict):
        name = "zain-source-registry.csv"
        for s, r in srcs.items():
            self.need(name, r, ["name", "license_spdx", "license_state", "decision", "rights_basis", "evidence_ref"])
            if r["license_state"] not in LICENSE_STATES:
                self.err("E-ENUM", f"{s}: license_state '{r['license_state']}'")
            if r["decision"] not in DECISIONS:
                self.err("E-ENUM", f"{s}: decision '{r['decision']}'")
            if r["decision"] in REUSE_DECISIONS - {"INTEGRATE"} and r["license_state"] not in REUSABLE_LICENSE_STATES:
                self.err("E-SRC-UNVERIFIED-REUSE", f"{s}: {r['decision']} requires license_state VERIFIED or RECORDED_V3 (is {r['license_state']})")
            if r["decision"] in REUSE_DECISIONS and strong_copyleft(r["license_spdx"]):
                self.err("E-SRC-COPYLEFT", f"{s}: {r['decision']} of strong-copyleft '{r['license_spdx']}'")
            if r["decision"] in REUSE_DECISIONS - {"INTEGRATE"} and not r["pinned_commit"].strip():
                self.err("E-SRC-UNPINNED", f"{s}: {r['decision']} without pinned_commit")

    def check_caps(self, caps: dict, tasks: dict, gates: dict, srcs: dict):
        name = "zain-capability-matrix.csv"
        for c, r in caps.items():
            self.need(name, r, ["pillar", "capability", "first_milestone", "owner_subsystem", "decision", "status"])
            if r["first_milestone"] not in ALL_MILESTONES:
                self.err("E-ENUM", f"{c}: first_milestone '{r['first_milestone']}'")
            if r["decision"] not in DECISIONS:
                self.err("E-ENUM", f"{c}: decision '{r['decision']}'")
            if r["status"] not in CAP_STATUSES:
                self.err("E-ENUM", f"{c}: status '{r['status']}'")
            ts = split_list(r["tasks"])
            if r["decision"] not in ("REJECT", "DEFER") and not ts:
                self.err("E-CAP-NO-TASK", f"{c}: capability has no implementing task")
            for t in ts:
                if t not in tasks:
                    self.err("E-CAP-DANGLING", f"{c}: task '{t}' not in backlog")
            # at least one implementing task must land by the capability's first milestone
            if ts and r["first_milestone"] in MIDX:
                ms = [tasks[t]["milestone"] for t in ts if t in tasks and tasks[t]["milestone"] in MIDX]
                if ms and min(MIDX[m] for m in ms) > MIDX[r["first_milestone"]]:
                    self.err("E-CAP-LATE", f"{c}: first_milestone {r['first_milestone']} but earliest task lands in {min(ms, key=lambda m: MIDX[m])}")
            gs = split_list(r["gates"])
            if r["decision"] not in ("REJECT", "DEFER") and r["first_milestone"] in ("R0a", "R0b", "R0", "R1") and not gs:
                self.err("E-CAP-NO-GATE", f"{c}: first-release capability without a verification gate")
            for g in gs:
                if g not in gates:
                    self.err("E-CAP-DANGLING", f"{c}: gate '{g}' unknown")
            for s in split_list(r["source_ids"]):
                if s not in srcs:
                    self.err("E-CAP-DANGLING", f"{c}: source '{s}' unknown")
                    continue
                if r["decision"] in REUSE_DECISIONS and srcs[s]["decision"] in ("REJECT", "REFERENCE"):
                    self.err("E-CAP-REJECTED-SOURCE", f"{c}: {r['decision']} from source {s} whose decision is {srcs[s]['decision']}")
            if r["decision"] in ("COPY", "ADAPT") and not split_list(r["source_ids"]):
                self.err("E-CAP-NO-SOURCE", f"{c}: {r['decision']} without a source")
            # a COPY/ADAPT capability needs at least one source that is itself copied, adapted or kept
            if r["decision"] in ("COPY", "ADAPT") and split_list(r["source_ids"]) and not any(
                    srcs.get(s, {}).get("decision") in ("COPY", "ADAPT", "KEEP") for s in split_list(r["source_ids"])):
                self.err("E-CAP-SOURCE-COMPAT", f"{c}: {r['decision']} but none of its sources is COPY/ADAPT/KEEP")

    def check_risks(self, risks: dict, tasks: dict, gates: dict):
        name = "zain-risk-register.csv"
        for k, r in risks.items():
            self.need(name, r, ["category", "title", "description", "likelihood", "impact", "severity", "owner", "status"])
            try:
                li, im = int(r["likelihood"]), int(r["impact"])
                if not (1 <= li <= 5 and 1 <= im <= 5):
                    raise ValueError
                score = li * im
                expect = "CRITICAL" if score >= 20 else "HIGH" if score >= 12 else "MEDIUM" if score >= 6 else "LOW"
                if r["severity"] != expect:
                    self.err("E-RISK-SEVERITY", f"{k}: severity {r['severity']} but L{li}×I{im}={score} → {expect}")
            except ValueError:
                self.err("E-RISK-SCORE", f"{k}: likelihood/impact must be integers 1..5")
            if r["status"] not in RISK_STATUSES:
                self.err("E-ENUM", f"{k}: status '{r['status']}'")
            ms = split_list(r["mitigation_tasks"])
            if r["severity"] in ("HIGH", "CRITICAL") and r["status"] != "ACCEPTED" and not ms:
                self.err("E-RISK-UNMITIGATED", f"{k}: {r['severity']} risk without mitigation task")
            for t in ms:
                if t not in tasks:
                    self.err("E-RISK-DANGLING", f"{k}: mitigation task '{t}' unknown")
            for g in split_list(r["gates"]):
                if g not in gates:
                    self.err("E-RISK-DANGLING", f"{k}: gate '{g}' unknown")
            if r["status"] == "CLOSED" and not r["evidence"].strip():
                self.err("E-DONE-NO-EVIDENCE", f"{k}: CLOSED without evidence")

    def check_journeys(self, journeys: dict, tasks: dict, gates: dict):
        for j, r in journeys.items():
            self.need("zain-ux-journeys.csv", r, ["name", "first_milestone", "full_milestone", "entry_point", "tasks",
                                                  "gates", "failure_recovery", "status"])
            for f in ("first_milestone", "full_milestone"):
                if r[f] not in ALL_MILESTONES:
                    self.err("E-ENUM", f"{j}: {f} '{r[f]}'")
            if r["first_milestone"] in MIDX and r["full_milestone"] in MIDX and MIDX[r["full_milestone"]] < MIDX[r["first_milestone"]]:
                self.err("E-JOURNEY-ORDER", f"{j}: full_milestone before first_milestone")
            for t in split_list(r["tasks"]):
                if t not in tasks:
                    self.err("E-JOURNEY-DANGLING", f"{j}: task '{t}' unknown")
            gs = split_list(r["gates"])
            if not gs:
                self.err("E-JOURNEY-NO-GATE", f"{j}: no acceptance gate")
            for g in gs:
                if g not in gates:
                    self.err("E-JOURNEY-DANGLING", f"{j}: gate '{g}' unknown")
                elif gates[g]["type"] == "JOURNEY" and gates[g]["milestone"] != r["first_milestone"]:
                    self.err("E-JOURNEY-ORDER", f"{j}: journey gate {g} milestone {gates[g]['milestone']} != first_milestone {r['first_milestone']}")
        n = len(journeys)
        if n < 20:
            self.err("E-JOURNEY-COUNT", f"{n} journeys registered; the master plan requires the 20 core journeys")

    def check_v3_parity(self, tasks: dict):
        v3_rows = {t: r for t, r in tasks.items() if r["source"] == "V3"}
        missing = sorted(set(self.v3_tasks) - set(v3_rows))
        extra = sorted(set(v3_rows) - set(self.v3_tasks))
        if missing:
            self.err("E-V3-DRIFT", f"V3 live tasks missing from backlog: {missing}")
        if extra:
            self.err("E-V3-DRIFT", f"backlog V3 rows not live in the catalog: {extra}")
        for t in sorted(set(v3_rows) & set(self.v3_tasks)):
            r, v = v3_rows[t], self.v3_tasks[t]
            if r["milestone"] != v["release"]:
                self.err("E-V3-DRIFT", f"{t}: milestone {r['milestone']} != V3 release {v['release']}")
            if r["phase"] != v["phase"]:
                self.err("E-V3-DRIFT", f"{t}: phase {r['phase']} != V3 phase {v['phase']}")
            if sorted(split_list(r["deps"])) != v["deps"]:
                self.err("E-V3-DRIFT", f"{t}: deps {sorted(split_list(r['deps']))} != V3 deps {v['deps']}")
            if r["tier"] != v["tier"]:
                self.err("E-V3-DRIFT", f"{t}: tier {r['tier']} != V3 tier {v['tier']}")

    def check_docs(self, tasks: dict, gates: dict, risks: dict):
        contracts = self.root / CONTRACTS_DOC
        if not contracts.exists():
            self.err("E-DOC-MISSING", f"{CONTRACTS_DOC} not found")
            return
        ctext = contracts.read_text(encoding="utf-8")
        for t, r in tasks.items():
            if r["source"] == "ZMP" and not re.search(rf"^###\s+{re.escape(t)}\b", ctext, re.M):
                self.err("E-DOC-NO-CONTRACT", f"{t}: no '### {t}' contract section in {CONTRACTS_DOC}")
        # every Z-/GATE-/RK- id mentioned in any master-plan markdown must exist
        for md in sorted(self.root.glob("*.md")):
            text = md.read_text(encoding="utf-8")
            for m in re.finditer(r"(?<![A-Za-z0-9-])(Z-\d{2})(?![0-9])", text):
                if m.group(1) not in tasks:
                    self.err("E-DOC-DANGLING", f"{md.name}: mentions unknown task {m.group(1)}")
            for m in re.finditer(r"(?<![A-Za-z0-9-])(GATE-[A-Z0-9]+(?:-[A-Z0-9]+)*)", text):
                if m.group(1) not in gates:
                    self.err("E-DOC-DANGLING", f"{md.name}: mentions unknown gate {m.group(1)}")
            for m in re.finditer(r"(?<![A-Za-z0-9-])(RK-\d{2})(?![0-9])", text):
                if m.group(1) not in risks:
                    self.err("E-DOC-DANGLING", f"{md.name}: mentions unknown risk {m.group(1)}")
        dec = self.root / DECISIONS_DOC
        if dec.exists():
            ids = re.findall(r"^\|\s*(DEC-\d{2})\s*\|", dec.read_text(encoding="utf-8"), re.M)
            if len(ids) != len(set(ids)):
                self.err("E-ID-DUP", f"{DECISIONS_DOC}: duplicate decision ids")
            known = set(ids)
            for md in sorted(self.root.glob("*.md")):
                for m in re.finditer(r"(?<![A-Za-z0-9-])(DEC-\d{2})(?![0-9])", md.read_text(encoding="utf-8")):
                    if m.group(1) not in known:
                        self.err("E-DOC-DANGLING", f"{md.name}: mentions unknown decision {m.group(1)}")
        else:
            self.err("E-DOC-MISSING", f"{DECISIONS_DOC} not found")

    def report(self) -> int:
        for e in self.errors:
            print("ERROR", e)
        counts = {k.replace("zain-", "").replace(".csv", ""): len(v) for k, v in self.data.items()}
        print(f"zmp check: errors={len(self.errors)} rows={counts} v3_tasks={len(self.v3_tasks)} v3_tests={len(self.v3_tests)}")
        return 1 if self.errors else 0


# ---------------------------------------------------------------------- sync-v3
SUBSYSTEM_BY_PREFIX = {
    "Q": "Packaging", "A": "Program/Governance", "G": "Program/Governance", "B": "Testing engine",
    "F": "Application shell", "N": "Identity", "L": "Agent runtime", "C": "Security system",
    "H": "Tool execution broker", "K": "Review service", "E": "Workflow engine", "M": "Workflow engine",
    "V": "Agent runtime", "Y": "Browser", "I": "Editor kernel", "D": "Design studio", "S": "Security system",
    "W": "Agent runtime", "R": "Remote", "X": "Release",
}
SUBSYSTEM_OVERRIDES = {
    "F-17": "Editor kernel", "F-04": "Application shell", "C-03": "Persistence layer", "C-12": "Git engine",
    "C-14": "UI architecture", "C-15": "UI architecture", "I-10": "Observability", "I-08": "Testing engine",
    "M-03": "Context engine", "M-04": "Context engine", "V-05": "Extension platform", "V-06": "Extension platform",
    "V-07": "Extension platform", "C-25": "Tool execution broker", "H-08": "Tool execution broker",
    "F-22": "Model gateway", "B-06": "Model gateway", "C-24": "Model gateway", "F-14": "UI architecture",
    "I-11": "UI architecture", "F-11": "Packaging", "F-19": "Packaging", "I-09": "Packaging", "I-12": "Packaging",
    "E-06": "Git engine", "I-02": "Git engine", "F-02": "Application shell", "F-03": "Identity",
}
HIGH_RISK = {"Q-04", "Q-05", "C-00", "C-01", "C-13", "C-25", "C-26", "H-08", "Y-10", "S-01", "C-28", "F-01", "G-03"}
FOUNDER_TASKS = {"G-01": "FOUNDER", "G-02": "FOUNDER", "G-07": "FOUNDER", "B-07": "AGENT+FOUNDER",
                 "N-02": "AGENT+FOUNDER", "N-05": "FOUNDER", "F-19": "FOUNDER", "I-12": "FOUNDER"}


def fmt_est(est) -> str:
    if est is None or est == "MEASURE":
        return "MEASURE"
    if isinstance(est, tuple):
        lo, hi = est
        f = lambda x: (f"{x:g}")
        return f(lo) if lo == hi else f"{f(lo)}–{f(hi)}"
    return str(est)


def complexity_of(est) -> str:
    if not isinstance(est, tuple):
        return "U"
    hi = est[1]
    return "S" if hi <= 0.5 else "M" if hi <= 2 else "L"


def sync_v3(root: Path, v3: Path) -> int:
    ck = Checker(root, v3)
    ck.load_v3()
    if ck.errors:
        for e in ck.errors:
            print("ERROR", e)
        return 1
    bpath = root / "registry" / "zain-task-backlog.csv"
    epath = root / "registry" / "zain-dependency-edges.csv"
    hdr = SCHEMAS["zain-task-backlog.csv"]
    old = {}
    zmp_rows = []
    if bpath.exists():
        for r in csv.DictReader(io.StringIO(bpath.read_text(encoding="utf-8"))):
            (zmp_rows if r["source"] == "ZMP" else []).append(r)
            if r["source"] == "V3":
                old[r["id"]] = r
    v3_rows = []
    order = {m: i for i, m in enumerate(MILESTONES + OPTIONAL_MILESTONES)}
    for t in sorted(ck.v3_tasks, key=lambda x: (order.get(ck.v3_tasks[x]["release"], 99), x)):
        v = ck.v3_tasks[t]
        cells = ck.v3_catalog_rows.get(t, [""] * 9)
        o = old.get(t, {})
        est = v["est"]
        v3_rows.append({
            "id": t, "source": "V3", "milestone": v["release"], "phase": v["phase"],
            "subsystem": SUBSYSTEM_OVERRIDES.get(t, SUBSYSTEM_BY_PREFIX.get(t[0], "Program/Governance")),
            "owner": o.get("owner") or FOUNDER_TASKS.get(t, "AGENT"),
            "title": re.sub(r"\s+", " ", cells[1]).strip(),
            "why": "Canonical contract in specs/008-wepld-v3-unified-replan/14_TASK_CATALOG.md (requirements: " + (cells[8] or "—") + ")",
            "deps": ", ".join(v["deps"]),
            "deliverables": "As specified by the V3 catalog row; sources: " + re.sub(r"\s+", " ", cells[3]).strip(),
            "acceptance": re.sub(r"\s+", " ", cells[4]).strip(),
            "tests": ", ".join(x for x in split_list(cells[5]) if x in ck.v3_tests) or "—",
            "evidence_required": "V3 EXIT_RULE: tests green incl. mutation control for neg tests, budgets measured where listed, independent review per tier, Build Learning line",
            "security": "T2: security, supply-chain, effect or authority relevant" if v["tier"] == "T2" else ("T1: UI/product without authority change" if v["tier"] == "T1" else "T0: documentation"),
            "est_pw": fmt_est(est), "complexity": complexity_of(est),
            "risk": o.get("risk") or ("HIGH" if t in HIGH_RISK else "MEDIUM" if v["tier"] == "T2" else "LOW"),
            "tier": v["tier"], "cost_class": "PAID" if v["release"] == "PD" else "FREE",
            "status": o.get("status") or "NOT_STARTED", "status_evidence": o.get("status_evidence", ""),
            "blockers": o.get("blockers", ""), "parallel_group": o.get("parallel_group", ""),
            "ref": "V3 14_TASK_CATALOG.md · " + v["phase"],
        })
    out = io.StringIO()
    w = csv.DictWriter(out, fieldnames=hdr, lineterminator="\n")
    w.writeheader()
    for r in zmp_rows:
        w.writerow({k: r.get(k, "") for k in hdr})
    for r in v3_rows:
        w.writerow(r)
    bpath.write_text(out.getvalue(), encoding="utf-8")
    # edges: regenerate V3 hard edges + ZMP hard edges from backlog deps; keep ZMP gate edges
    gate_edges = []
    if epath.exists():
        for r in csv.DictReader(io.StringIO(epath.read_text(encoding="utf-8"))):
            if r["type"] == "gate":
                gate_edges.append(r)
    eh = SCHEMAS["zain-dependency-edges.csv"]
    out = io.StringIO()
    w = csv.DictWriter(out, fieldnames=eh, lineterminator="\n")
    w.writeheader()
    for r in zmp_rows + v3_rows:
        for d in split_list(r["deps"]):
            w.writerow({"from": d, "to": r["id"], "type": "hard", "source": r["source"], "note": ""})
    for r in gate_edges:
        w.writerow({k: r.get(k, "") for k in eh})
    epath.write_text(out.getvalue(), encoding="utf-8")
    print(f"sync-v3: wrote {len(zmp_rows)} ZMP rows + {len(v3_rows)} V3 rows; {len(gate_edges)} gate edges kept")
    return 0


# ---------------------------------------------------------------------- render
GENERATED = {
    "11-TASK-CONTRACTS.md": "zmp-contracts",
    "10-ROADMAP-AND-CRITICAL-PATH.md": "zmp-roadmap",
}


def _est_pair(s):
    if not isinstance(s, str) or s == "MEASURE":
        return None
    m = re.fullmatch(r"(\d+(?:\.\d+)?)(?:[–-](\d+(?:\.\d+)?))?", s)
    if not m:
        return None
    lo = float(m.group(1))
    return lo, float(m.group(2) or lo)


def _load_rows(root: Path, name: str) -> list[dict]:
    return list(csv.DictReader(io.StringIO((root / "registry" / name).read_text(encoding="utf-8"))))


def render_contracts(root: Path) -> str:
    tasks = [r for r in _load_rows(root, "zain-task-backlog.csv") if r["source"] == "ZMP"]
    edges = _load_rows(root, "zain-dependency-edges.csv")
    gates_out: dict[str, list[str]] = {}
    for e in edges:
        if e["type"] == "gate":
            gates_out.setdefault(e["from"], []).append(f"{e['to']} ({e['note']})")
    order = {m: i for i, m in enumerate(MILESTONES + OPTIONAL_MILESTONES)}
    out = [f"<!-- GENERATED:BEGIN {GENERATED['11-TASK-CONTRACTS.md']} (tools/zmp.py render; edit registry/zain-task-backlog.csv) -->", ""]
    for r in sorted(tasks, key=lambda r: (order[r["milestone"]], r["id"])):
        out += [f"### {r['id']} — {r['title']}", "",
                "| Field | Contract |", "|---|---|",
                f"| Milestone / subsystem / owner | {r['milestone']} · {r['subsystem']} · {r['owner']} |",
                f"| Why | {r['why']} |",
                f"| Dependencies (must finish first) | {r['deps'] or '—'} |",
                f"| Gates it opens for V3 tasks | {'; '.join(gates_out.get(r['id'], [])) or '—'} |",
                f"| Deliverables | {r['deliverables']} |",
                f"| Acceptance criteria | {r['acceptance']} |",
                f"| Required tests / gates | {r['tests']} |",
                f"| Evidence for completion | {r['evidence_required']} |",
                f"| Security implications | {r['security']} |",
                f"| Estimate · complexity · risk · tier · cost | {r['est_pw']} pw · {r['complexity']} · {r['risk']} · {r['tier']} · {r['cost_class']} |",
                f"| Blockers | {r['blockers'] or '—'} |",
                f"| Parallel group | {r['parallel_group'] or '—'} |",
                f"| Status | {r['status']}{(' — ' + r['status_evidence']) if r['status_evidence'] else ''} |",
                f"| Reference | {r['ref'] or '—'} |", ""]
    out.append(f"<!-- GENERATED:END {GENERATED['11-TASK-CONTRACTS.md']} -->")
    return "\n".join(out)


def render_roadmap(root: Path) -> str:
    tasks = {r["id"]: r for r in _load_rows(root, "zain-task-backlog.csv")}
    edges = _load_rows(root, "zain-dependency-edges.csv")
    pre: dict[str, set[str]] = {}
    for e in edges:
        pre.setdefault(e["to"], set()).add(e["from"])
    out = [f"<!-- GENERATED:BEGIN {GENERATED['10-ROADMAP-AND-CRITICAL-PATH.md']} (tools/zmp.py render) -->", "",
           "| Milestone | New tasks (V3 / ZMP) | New effort pw (low–high) | Unmeasured | Cumulative tasks | Cumulative pw (low–high) | Longest dependency chain, pw (low–high) |",
           "|---|---|---|---|---|---|---|"]
    cum: set[str] = set()
    clo = chi = 0.0

    def longest(S: set[str], i: int) -> tuple[float, list[str]]:
        memo: dict[str, tuple[float, list[str]]] = {}
        visiting: set[str] = set()

        def lp(t: str):
            if t in memo:
                return memo[t]
            if t in visiting:  # cycle: reported by check as E-DEP-CYCLE; do not recurse forever
                return (0.0, [])
            visiting.add(t)
            x = _est_pair(tasks[t]["est_pw"])
            w = 0.0 if x is None else x[i]
            best = (0.0, [])
            for p in sorted(pre.get(t, ())):
                if p in S:
                    c = lp(p)
                    if c[0] > best[0]:
                        best = c
            memo[t] = (w + best[0], best[1] + [t])
            visiting.discard(t)
            return memo[t]
        return max((lp(t) for t in sorted(S)), key=lambda c: c[0])

    chains = {}
    for m in MILESTONES + OPTIONAL_MILESTONES:
        ids = sorted(t for t, r in tasks.items() if r["milestone"] == m)
        if not ids:
            continue
        lo = hi = 0.0
        un = 0
        for t in ids:
            x = _est_pair(tasks[t]["est_pw"])
            if x is None:
                un += 1
            else:
                lo += x[0]
                hi += x[1]
        v3n = sum(1 for t in ids if tasks[t]["source"] == "V3")
        if m in MIDX:
            cum |= set(ids)
            clo += lo
            chi += hi
            S = set(cum)
        else:
            S = set(ids)
        cl, ch = longest(S, 0), longest(S, 1)
        chains[m] = ch
        out.append(f"| {m} | {len(ids)} ({v3n} / {len(ids) - v3n}) | {lo:.2f}–{hi:.2f} | {un} | "
                   f"{len(cum) if m in MIDX else '—'} | {clo:.2f}–{chi:.2f} | {cl[0]:.2f}–{ch[0]:.2f} |")
    out += ["", "Longest dependency chain (high estimates) to each early exit:", ""]
    for m in ("R0a", "R0b", "R0", "R1"):
        if m in chains:
            out.append(f"- **{m}:** {' → '.join(chains[m][1])} = {chains[m][0]:.2f} pw")
    out += ["", f"<!-- GENERATED:END {GENERATED['10-ROADMAP-AND-CRITICAL-PATH.md']} -->"]
    return "\n".join(out)


RENDERERS = {"11-TASK-CONTRACTS.md": render_contracts, "10-ROADMAP-AND-CRITICAL-PATH.md": render_roadmap}


def generated_block(text: str, tag: str):
    b = text.count(f"<!-- GENERATED:BEGIN {tag}")
    e = text.count(f"<!-- GENERATED:END {tag} -->")
    if b != 1 or e != 1:
        return None, f"expected exactly one BEGIN and one END marker for {tag}, found {b}/{e}"
    m = re.search(rf"<!-- GENERATED:BEGIN {re.escape(tag)}.*?<!-- GENERATED:END {re.escape(tag)} -->", text, re.S)
    if not m:
        return None, f"END marker for {tag} precedes BEGIN"
    return m, None


def render(root: Path, write: bool) -> list[str]:
    problems = []
    for name, fn in RENDERERS.items():
        path = root / name
        if not path.exists():
            problems.append(f"E-DOC-MISSING: {name} not found")
            continue
        text = path.read_text(encoding="utf-8")
        m, why = generated_block(text, GENERATED[name])
        if m is None:
            problems.append(f"E-GEN-MARKER: {name}: {why}")
            continue
        try:
            new = fn(root)
        except Exception as exc:  # malformed registries: report, never crash or write
            problems.append(f"E-GEN-ERROR: {name}: cannot render from registries ({type(exc).__name__}: {exc})")
            continue
        if m.group(0) != new:
            if write:
                path.write_text(text[:m.start()] + new + text[m.end():], encoding="utf-8")
            else:
                problems.append(f"E-GEN-DRIFT: {name} generated block differs from registries (run zmp.py render)")
    return problems


def main(argv: list[str]) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    root = Path(argv[argv.index("--root") + 1]) if "--root" in argv else DEFAULT_ROOT
    v3 = Path(argv[argv.index("--v3") + 1]) if "--v3" in argv else DEFAULT_V3
    if not argv or argv[0] not in ("check", "sync-v3", "render"):
        print(__doc__)
        return 2
    if argv[0] == "sync-v3":
        return sync_v3(root, v3)
    if argv[0] == "render":
        probs = render(root, write=True)
        for p in probs:
            print("ERROR", p)
        print(f"render: {'ok' if not probs else 'failed'}")
        return 1 if probs else 0
    ck = Checker(root, v3)
    rc = ck.check_core()
    for p in render(root, write=False):
        code, _, msg = p.partition(": ")
        ck.err(code, msg)
    return ck.report()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
