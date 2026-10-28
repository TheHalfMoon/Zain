#!/usr/bin/env python3
"""Deterministic, fail-closed validator and generator for the Zain V3 planning package (revision 4).

Authoritative inputs:
  14_TASK_CATALOG.md             tasks, dependencies, estimates, tests, release membership (§16)
  23_ACCEPTANCE_TEST_REGISTRY.md registered tests (prerequisites, phase, kind, guard/mutant/fixture/failure) and
                                 suite composition (nested suites)
  13_REQUIREMENTS_REGISTER.md    requirements

Generated outputs (written without --check; compared byte-for-byte with --check):
  GENERATED_PLAN_REPORT.md, 15_TRACEABILITY_MATRIX.md, and the GENERATED block in ZAIN_V3_MASTER_PLAN.md

Usage: python -I tools/plan_graph.py [--check] [--root DIR]
Fail-closed rules (Astro round 2, A2-05/A2-06): unknown test families, unknown/missing/reversed range members,
duplicate task or test ids, unknown test kinds, incomplete negative specifications, free-text negative tests,
nested-suite prerequisites, release sets not closed under effective dependencies, releases not cumulative,
dependencies on the optional paid track, and drift between generated artifacts and inputs.
This checks planning consistency only; it is not semantic verification and does not run the product.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parent.parent
PHASES = ["P−1′", "PF", "P0", "P1", "P2-N", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9", "P10", "PD"]
PIDX = {p: i for i, p in enumerate(PHASES)}
HEADINGS = {"## P−1′": "P−1′", "## PF": "PF", "## P0": "P0", "## P1 ": "P1", "## P2-N": "P2-N", "## P2 ": "P2",
            "## P3": "P3", "## P4": "P4", "## P5": "P5", "## P6": "P6", "## P7": "P7", "## P8": "P8",
            "## P9": "P9", "## P10": "P10", "## PD": "PD"}
TASK_ID = re.compile(r"^[A-Z]-\d{2}$")
KINDS = {"pos", "neg", "rec", "bench", "spike", "qual"}
TEST_FAMILIES = [
    r"BRW-AT-\d{2}", r"BRW-[A-Z]\d{2}", r"ZCR-T\d{2}", r"ZCR-Q\d{2}", r"ES-AT-\d{2}", r"DG-N\d{2}", r"DG-B\d",
    r"DG-P\d{2}", r"CC-T\d{2}", r"V1-\d{2}", r"AT-\d{2}", r"T\d{1,2}b?", r"R\d{1,2}", r"W\d+b?", r"B\d{1,2}",
    r"N\d{1,2}", r"D\d", r"E\d", r"COV-\d{2}", r"PEM-[A-Z]{2,5}-\d{2}", r"REC-\d{2}", r"PH-\d{2}", r"APR-\d{2}",
    r"LED-\d{2}", r"GV-\d{2}", r"FG-\d{2}", r"DM-\d{2}", r"TERM-\d{2}", r"A11Y-\d{2}", r"PROV-\d{2}", r"POL-\d{2}",
    r"EFF-\d{2}", r"FWB-\d{2}", r"SBX-\d{2}", r"RMT-\d{2}", r"EDIT-\d{2}", r"DBG-\d{2}", r"EGR-\d{2}", r"INBOX-\d{2}",
    r"CI-\d{2}", r"SRC-\d{2}", r"ID-\d{2}", r"PROTO-\d{2}", r"UI-\d{2}", r"SEC12-\d{2}", r"OPID-\d{2}", r"FSG-\d{2}",
    r"LIC-\d{2}", r"PKG-\d{2}", r"CLM-\d{2}",
]
FAMILY = "|".join(f"(?:{f})" for f in TEST_FAMILIES)
TOKEN_RE = re.compile(r"(?<![A-Za-z0-9-])(" + FAMILY + r")(?:\s*(?:\.\.|–)\s*(" + FAMILY + r"|\d+))?(?![A-Za-z0-9-])")
# Anything that looks like a coded identifier (uppercase letters + digits) but is not a known family fails closed.
IDLIKE_RE = re.compile(r"(?<![A-Za-z0-9_-])[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*\d[A-Za-z0-9]*(?![A-Za-z0-9_-])")
NEG_WORDS = re.compile(r"\bneg(?:ative)?\b|should fail|must fail|must be (?:rejected|denied|refused)", re.I)


def rows(text: str):
    for line in text.splitlines():
        if line.startswith("|") and not line.startswith("|---"):
            yield [c.strip() for c in line.strip().strip("|").split("|")]


def split_id(tok: str):
    m = re.match(r"^(.*?)(\d+)(b?)$", tok)
    return (m.group(1), int(m.group(2)), len(m.group(2)), m.group(3)) if m else None


def expand(start: str, end: str | None, errors: list[str], where: str) -> list[str]:
    if not end:
        return [start]
    a, b = split_id(start), split_id(end if not end.isdigit() else split_id(start)[0] + end)
    if not a or not b or a[3] or b[3] or (not end.isdigit() and a[0] != b[0]):
        errors.append(f"{where}: invalid test range {start}..{end}")
        return [start]
    if b[1] < a[1]:
        errors.append(f"{where}: reversed test range {start}..{end}")
        return [start]
    return [f"{a[0]}{n:0{a[2]}d}" for n in range(a[1], b[1] + 1)]


def test_tokens(text: str, errors: list[str] | None = None, where: str = "") -> list[str]:
    errs = errors if errors is not None else []
    out: list[str] = []
    for m in TOKEN_RE.finditer(text):
        out.extend(expand(m.group(1), m.group(2), errs, where))
    return out


def unknown_ids(text: str) -> list[str]:
    rest = TOKEN_RE.sub(" ", text)
    return IDLIKE_RE.findall(rest)


def parse_est(s: str):
    s = s.strip()
    if s == "MEASURE":
        return None
    m = re.fullmatch(r"(\d+(?:\.\d+)?)(?:–(\d+(?:\.\d+)?))?", s)
    if not m:
        raise ValueError(s)
    lo = float(m.group(1))
    return lo, float(m.group(2)) if m.group(2) else lo


class Plan:
    def __init__(self, root: Path):
        self.root = root
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def read(self, name: str) -> str:
        return (self.root / name).read_text(encoding="utf-8")

    # ---------------- tasks ----------------
    def load_tasks(self):
        text = self.read("14_TASK_CATALOG.md")
        self.catalog = text
        tasks: dict[str, dict] = {}
        phase = None
        for line in text.splitlines():
            if line.startswith("## "):
                phase = None
                for prefix, ph in HEADINGS.items():
                    if (line + " ").startswith(prefix):
                        phase = ph
            if not line.startswith("| ") or line.startswith("|---"):
                continue
            f = [c.strip() for c in line.strip().strip("|").split("|")]
            if not f or not TASK_ID.match(f[0]):
                continue
            if len(f) != 9:
                self.errors.append(f"task {f[0]}: expected 9 columns, found {len(f)}")
                continue
            if f[0] in tasks:
                self.errors.append(f"duplicate task id {f[0]}")
                continue
            tag = re.match(r"^\[(P[^\]]+)\]\s*", f[1])
            ph = tag.group(1) if tag else phase
            if ph not in PIDX:
                self.errors.append(f"task {f[0]}: unknown or missing phase {ph!r}")
                ph = "PD"
            try:
                est = parse_est(f[6])
            except ValueError:
                self.errors.append(f"task {f[0]}: unparseable estimate {f[6]!r}")
                est = (0.0, 0.0)
            if f[7] not in {"T0", "T1", "T2"}:
                self.errors.append(f"task {f[0]}: unknown tier {f[7]!r}")
            tasks[f[0]] = {"id": f[0], "title": re.sub(r"^\[[^\]]+\]\s*", "", f[1]), "deps_raw": f[2], "tests": f[5],
                           "est": est, "tier": f[7], "reqs": f[8], "phase": ph,
                           "superseded": f[1].startswith("SUPERSEDED")}
        self.tasks = tasks
        self.live = {t for t, v in tasks.items() if not v["superseded"]}

    def expand_deps(self, t: str) -> set[str]:
        raw = self.tasks[t]["deps_raw"]
        deps: set[str] = set()
        if raw in ("—", ""):
            return deps
        for part in [p.strip() for p in raw.split(",")]:
            m_all = re.fullmatch(r"all (P[\w−′-]+)", part)
            m_rng = re.fullmatch(r"([A-Z])-(\d{2})\.\.(?:([A-Z])-)?(\d{2})", part)
            if m_all:
                if m_all.group(1) not in PIDX:
                    self.errors.append(f"{t}: unknown phase in dependency {part!r}")
                deps |= {x for x in self.live if self.tasks[x]["phase"] == m_all.group(1) and x != t}
            elif m_rng:
                letter, a, b = m_rng.group(1), int(m_rng.group(2)), int(m_rng.group(4))
                if m_rng.group(3) and m_rng.group(3) != letter:
                    self.errors.append(f"{t}: dependency range mixes prefixes {part!r}")
                if b < a:
                    self.errors.append(f"{t}: reversed dependency range {part!r}")
                for n in range(a, b + 1):
                    tid = f"{letter}-{n:02d}"
                    if tid not in self.tasks:
                        self.errors.append(f"{t}: dependency range {part!r} member {tid} does not exist")
                    deps.add(tid)
            elif TASK_ID.fullmatch(part):
                deps.add(part)
            else:
                self.errors.append(f"{t}: unparseable dependency token {part!r}")
        for d in sorted(deps):
            if d not in self.tasks:
                self.errors.append(f"{t}: dependency {d} does not exist")
            elif self.tasks[d]["superseded"]:
                self.errors.append(f"{t}: depends on superseded task {d}")
        return {d for d in deps if d in self.live}

    # ---------------- registry ----------------
    def load_registry(self):
        text = self.read("23_ACCEPTANCE_TEST_REGISTRY.md")
        reg: dict[str, dict] = {}
        suites: dict[str, list[str]] = {}
        in_suites = False
        for line in text.splitlines():
            if line.startswith("## "):
                in_suites = line.startswith("## Suite composition")
            if not line.startswith("|") or line.startswith("|---"):
                continue
            f = [c.strip() for c in line.strip().strip("|").split("|")]
            if in_suites:
                if len(f) != 2 or f[0] == "Suite":
                    continue
                for sid in test_tokens(f[0], self.errors, "suite"):
                    suites[sid] = test_tokens(f[1], self.errors, f"suite {sid}")
                    if unknown_ids(f[1]):
                        self.errors.append(f"suite {sid}: unknown ids {unknown_ids(f[1])}")
                continue
            if len(f) != 9 or f[0] in ("Test", ""):
                continue
            ids = test_tokens(f[0], self.errors, "registry")
            if not ids or unknown_ids(f[0]):
                self.errors.append(f"registry: unrecognized test id/family {f[0]!r}")
                continue
            if f[1] not in KINDS:
                self.errors.append(f"registry {f[0]}: invalid kind {f[1]!r} (allowed: {sorted(KINDS)})")
            prereqs = [p.strip() for p in f[2].split(",") if p.strip() and p.strip() != "—"]
            for tid in ids:
                if tid in reg:
                    self.errors.append(f"registry: duplicate test id {tid}")
                reg[tid] = {"kind": f[1], "prereqs": prereqs, "phase": f[3], "guard": f[4], "mutant": f[5],
                            "fixture": f[6], "failure": f[7], "source": f[8]}
        for tid, r in reg.items():
            if r["kind"] == "neg" or NEG_WORDS.search(r["kind"]):
                for k in ("guard", "mutant", "fixture", "failure"):
                    if not r[k] or r[k] == "—":
                        self.errors.append(f"registry {tid}: negative test lacks {k}")
            for p in r["prereqs"]:
                if p not in self.live:
                    self.errors.append(f"registry {tid}: prerequisite {p} missing or superseded")
        for s, members in suites.items():
            if s not in reg:
                self.errors.append(f"suite {s}: not registered")
            for m in members:
                if m not in reg:
                    self.errors.append(f"suite {s}: member {m} not registered")
        self.reg, self.suites = reg, suites
        # effective prerequisites through nested suites
        eff: dict[str, set[str]] = {}

        def resolve(tid: str, stack: tuple[str, ...]) -> set[str]:
            if tid in eff:
                return eff[tid]
            if tid in stack:
                self.errors.append("suite cycle: " + " -> ".join(stack + (tid,)))
                return set()
            out = {p for p in reg.get(tid, {}).get("prereqs", []) if p in self.live}
            for m in suites.get(tid, []):
                out |= resolve(m, stack + (tid,))
            eff[tid] = out
            return out

        for tid in reg:
            resolve(tid, ())
        self.eff_prereq = eff
        for tid, r in reg.items():
            phs = [PIDX[self.tasks[p]["phase"]] for p in eff[tid]]
            computed = PHASES[max(phs)] if phs else None
            if computed and r["phase"] != computed:
                self.errors.append(f"registry {tid}: declared phase {r['phase']} != computed {computed} (incl. nested suites)")

    # ---------------- releases ----------------
    def load_releases(self):
        sec = self.catalog.split("## §16 Release membership", 1)
        rel: dict[str, set[str]] = {}
        order: list[str] = []
        if len(sec) < 2:
            self.errors.append("14: §16 Release membership missing")
            return rel, order
        for f in rows(sec[1].split("\n## ", 1)[0]):
            if len(f) < 3 or not re.fullmatch(r"R\d[a-z]?", f[0]):
                continue
            spec = f[2]
            members: set[str] = set()
            head = spec.split("phases:")[0].split("tasks:")[0]
            parents = re.findall(r"(R\d[a-z]?)\b", head)
            if order and (not parents or parents[-1] != order[-1]):
                self.errors.append(f"§16 {f[0]}: must be cumulative and include the previous release {order[-1]}")
            for p in parents:
                if p not in rel:
                    self.errors.append(f"§16 {f[0]}: unknown parent release {p}")
                members |= rel.get(p, set())
            pm = re.search(r"phases:\s*([^+;]+)", spec)
            if pm:
                for ph in [p.strip() for p in pm.group(1).split(",")]:
                    if ph not in PIDX:
                        self.errors.append(f"§16 {f[0]}: unknown phase {ph}")
                    members |= {t for t in self.live if self.tasks[t]["phase"] == ph}
            tm = re.search(r"tasks:\s*([^;]+)", spec)
            if tm:
                for t in [x.strip() for x in tm.group(1).split(",")]:
                    if t not in self.live:
                        self.errors.append(f"§16 {f[0]}: unknown or superseded task {t}")
                    else:
                        members.add(t)
            rel[f[0]] = members
            order.append(f[0])
        return rel, order

    # ---------------- graph ----------------
    def build(self):
        self.load_tasks()
        self.deps = {t: self.expand_deps(t) for t in sorted(self.live)}
        self.load_registry()
        eff = {t: set(self.deps[t]) for t in self.live}
        used: dict[str, list[str]] = {}
        for t in sorted(self.live):
            text = self.tasks[t]["tests"]
            for bad in unknown_ids(text):
                self.errors.append(f"{t}: unrecognized test id/family {bad!r}")
            for clause in [c.strip() for c in text.split(";")]:
                toks = test_tokens(clause, self.errors, t)
                if NEG_WORDS.search(clause) and not toks:
                    self.errors.append(f"{t}: free-text negative test (register it in 23): {clause!r}")
                for tok in toks:
                    used.setdefault(tok, []).append(t)
                    if tok not in self.reg:
                        self.errors.append(f"{t}: test {tok} not in registry")
                        continue
                    eff[t] |= {p for p in self.eff_prereq[tok] if p != t}
        self.used, self.eff = used, eff
        self.order = self.topo(eff)
        anc: dict[str, set[str]] = {}
        for n in self.order:
            s: set[str] = set()
            for d in self.deps[n]:
                s |= {d} | anc.get(d, set())
            anc[n] = s
        for tok, users in used.items():
            if tok not in self.reg:
                continue
            for t in users:
                missing = sorted(p for p in self.eff_prereq[tok] if p != t and p not in anc.get(t, set()))
                if missing:
                    self.errors.append(f"{t}: runs {tok} but prerequisite(s) {', '.join(missing)} are not declared ancestors")
                ph = self.reg[tok]["phase"]
                if ph in PIDX and PIDX[ph] > PIDX[self.tasks[t]["phase"]]:
                    self.errors.append(f"{t} ({self.tasks[t]['phase']}): runs {tok} whose execution phase is {ph}")
        for t in self.live:
            for d in self.deps[t]:
                if PIDX[self.tasks[d]["phase"]] > PIDX[self.tasks[t]["phase"]]:
                    self.errors.append(f"{t} ({self.tasks[t]['phase']}) depends on later-phase {d} ({self.tasks[d]['phase']})")
        self.rel, self.rel_order = self.load_releases()
        for r in self.rel_order:
            s = self.rel[r]
            for t in sorted(s):
                outside = sorted(d for d in eff[t] if d not in s)
                if outside:
                    self.errors.append(f"release {r} not closed: {t} needs {', '.join(outside)}")
        assigned = set().union(*self.rel.values()) if self.rel else set()
        for t in sorted(self.live):
            if self.tasks[t]["phase"] == "PD":
                for r in self.rel_order:
                    if t in self.rel[r]:
                        self.errors.append(f"optional PD task {t} is inside release {r}")
            elif t not in assigned:
                self.errors.append(f"{t}: not assigned to any release")
            for d in eff[t]:
                if self.tasks[d]["phase"] == "PD" and self.tasks[t]["phase"] != "PD":
                    self.errors.append(f"{t} depends on optional distribution-track task {d}")

    def topo(self, edges):
        state: dict[str, int] = {}
        out: list[str] = []
        for n in sorted(self.live):
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
                if state.get(nxt) == 1:
                    self.errors.append("cycle: " + " -> ".join(path[path.index(nxt):] + [nxt]))
                    continue
                if not state.get(nxt):
                    state[nxt] = 1
                    path.append(nxt)
                    stack.append((nxt, iter(sorted(edges.get(nxt, ())))))
        return out

    # ---------------- outputs ----------------
    def tot(self, ts):
        lo = hi = 0.0
        unmeasured = 0
        for t in ts:
            e = self.tasks[t]["est"]
            if e is None:
                unmeasured += 1
            else:
                lo, hi = lo + e[0], hi + e[1]
        return lo, hi, unmeasured

    def longest(self, members, idx):
        best: dict[str, tuple[float, list[str]]] = {}
        for n in self.order:
            if n not in members:
                continue
            e = self.tasks[n]["est"]
            w = 0.0 if e is None else e[idx]
            prev = [best[d] for d in sorted(self.eff.get(n, ())) if d in best]
            base = max(prev, key=lambda x: x[0]) if prev else (0.0, [])
            best[n] = (base[0] + w, base[1] + [n])
        return max(best.values(), key=lambda x: x[0]) if best else (0.0, [])

    def calendar_weeks(self, ts, idx):
        r0 = self.rel.get("R0", set())
        pre = sum(self.tasks[t]["est"][idx] for t in ts if t in r0 and self.tasks[t]["est"])
        post = sum(self.tasks[t]["est"][idx] for t in ts if t not in r0 and self.tasks[t]["est"])
        u = 0.35 if idx == 0 else 0.60
        return pre + post / (1 - u)

    def render(self):
        f = lambda x: (f"{x:.2f}".rstrip("0").rstrip(".") if x % 1 else f"{x:.0f}")
        live = self.live
        rep = ["# Generated Plan Report\n", "```text",
               "GENERATED_BY = tools/plan_graph.py (deterministic; do not hand-edit; --check fails on drift)",
               "INPUTS = 14_TASK_CATALOG.md, 23_ACCEPTANCE_TEST_REGISTRY.md, 13_REQUIREMENTS_REGISTER.md",
               f"TASK_ROWS = {len(self.tasks)} (live {len(live)}, superseded {len(self.tasks) - len(live)})",
               f"REGISTERED_TESTS = {len(self.reg)}; SUITES = {len(self.suites)}; TEST_REFERENCES = {sum(len(v) for v in self.used.values())}",
               f"DECLARED_DEP_EDGES = {sum(len(self.deps[t]) for t in live)}; EFFECTIVE_EDGES = {sum(len(self.eff[t]) for t in live)}",
               f"UNMEASURED_TASKS = {sum(1 for t in live if self.tasks[t]['est'] is None)} (estimate 'MEASURE'; excluded from sums)",
               "ESTIMATE_CLASS = reading-based ESTIMATE; nothing was built or run; this is not semantic verification",
               "```\n", "## 1. Validation\n",
               "Fail-closed checks: see tools/plan_graph.py docstring; regression mutations in tools/test_plan_graph_mutations.py.\n",
               "- No validation errors." if not self.errors else "- VALIDATION ERRORS PRESENT (see --check output).",
               "\n## 2. Effort by phase (person-weeks, ESTIMATE)\n",
               "| Phase | Live tasks | Low | High | Unmeasured tasks |", "|---|---|---|---|---|"]
        for p in PHASES:
            ts = [t for t in live if self.tasks[t]["phase"] == p]
            lo, hi, u = self.tot(ts)
            rep.append(f"| {p} | {len(ts)} | {f(lo)} | {f(hi)} | {u} |")
        rep += ["\n## 3. Release tiers (cumulative; 14 §16)\n",
                "| Release | Tasks | Effort low–high (pw) | Unmeasured tasks | Elapsed low–high (weeks) | Critical path low–high (pw) |",
                "|---|---|---|---|---|---|"]
        cps = []
        for r in self.rel_order:
            ts = self.rel[r]
            lo, hi, u = self.tot(ts)
            cl, ch = self.longest(ts, 0), self.longest(ts, 1)
            rep.append(f"| {r} | {len(ts)} | {f(lo)}–{f(hi)} | {u} | {self.calendar_weeks(ts, 0):.1f}–{self.calendar_weeks(ts, 1):.1f} | {f(cl[0])}–{f(ch[0])} |")
            cps.append(f"- **{r}**: `{' → '.join(ch[1])}`")
        rep += ["\nElapsed weeks = (effort inside R0) + (effort after R0)/(1 − u), A-1 capacity 1 pw per week, u = 0.35/0.60.",
                "Tasks marked MEASURE are excluded: a release with unmeasured tasks has a LOWER BOUND, not an envelope.\n",
                "## 4. Critical paths (high estimate, effective graph)\n"] + cps
        rep += ["\n## 5. Components\n", "| Component | Tasks | Total pw | Inside R2 pw |", "|---|---|---|---|"]
        for name, pre in [("Zain Code Review", "K-"), ("Zain Engineering System", "E-"), ("Zain Plan Mode", "L-"),
                          ("Zain Browser", "Y-"), ("DeskGate", "H-")]:
            ts = [t for t in live if t.startswith(pre)]
            a = self.tot(ts)
            b = self.tot([t for t in ts if t in self.rel.get("R2", set())])
            rep.append(f"| {name} | {len(ts)} | {f(a[0])}–{f(a[1])} | {f(b[0])}–{f(b[1])} |")
        rep += ["\n## 6. Optional distribution track (PD)\n", "| Task | Title | Est |", "|---|---|---|"]
        for t in sorted(t for t in live if self.tasks[t]["phase"] == "PD"):
            e = self.tasks[t]["est"]
            rep.append(f"| {t} | {self.tasks[t]['title'][:90]} | {f(e[0])}–{f(e[1])} |")
        tr, counts = self.traceability()
        rep += ["\n## 7. Traceability summary\n",
                f"REGISTERED {counts['REGISTERED']} · FREE_TEXT_ONLY {counts['FREE_TEXT_ONLY']} · GAP {counts['GAP']} (details: 15)"]
        block = ["<!-- GENERATED:BEGIN release-table (tools/plan_graph.py) -->",
                 "| Release | Tasks | Effort pw | Unmeasured tasks | Elapsed weeks (A-1; upkeep 35–60% after R0) |",
                 "|---|---|---|---|---|"]
        for r in self.rel_order:
            ts = self.rel[r]
            lo, hi, u = self.tot(ts)
            block.append(f"| {r} | {len(ts)} | {f(lo)}–{f(hi)}{' (lower bound)' if u else ''} | {u} | {self.calendar_weeks(ts, 0):.1f}–{self.calendar_weeks(ts, 1):.1f} |")
        lo, hi, _ = self.tot([t for t in live if self.tasks[t]["phase"] == "PD"])
        block.append(f"| PD (optional paid track) | {sum(1 for t in live if self.tasks[t]['phase'] == 'PD')} | {f(lo)}–{f(hi)} | 0 | not scheduled |")
        block.append("<!-- GENERATED:END release-table -->")
        mp = self.read("ZAIN_V3_MASTER_PLAN.md")
        if "<!-- GENERATED:BEGIN release-table" not in mp:
            self.errors.append("master plan: GENERATED markers missing")
        mp_new = re.sub(r"<!-- GENERATED:BEGIN release-table.*?<!-- GENERATED:END release-table -->",
                        lambda _m: "\n".join(block), mp, flags=re.S)
        return {"GENERATED_PLAN_REPORT.md": "\n".join(rep) + "\n", "15_TRACEABILITY_MATRIX.md": tr,
                "ZAIN_V3_MASTER_PLAN.md": mp_new}, counts

    def traceability(self):
        reqs = [f for f in rows(self.read("13_REQUIREMENTS_REGISTER.md"))
                if len(f) >= 4 and re.fullmatch(r"(PR|SEC|NF|GOV)-\d+b?", f[0])]
        reqs += [[f"CL-V1-{n:02d}", f"03F §2 V1-{n:02d}", "see 03F", "see 03F"] for n in range(1, 19)]
        counts = {"REGISTERED": 0, "FREE_TEXT_ONLY": 0, "GAP": 0}
        lines = []
        for f in reqs:
            rid = f[0]
            pat = re.compile(r"(?<![\w-])" + re.escape(rid) + r"(?![\w-])")
            mapped = []
            for t in sorted(self.live):
                rq = self.tasks[t]["reqs"]
                hit = bool(pat.search(rq))
                for m in re.finditer(r"(PR|NF)-(\d+)\.\.(\d+)", rq):
                    mm = re.fullmatch(rf"{m.group(1)}-(\d+)", rid)
                    if mm and int(m.group(2)) <= int(mm.group(1)) <= int(m.group(3)):
                        hit = True
                mv = re.fullmatch(r"CL-V1-(\d{2})", rid)
                if mv and f"V1-{mv.group(1)}" in test_tokens(self.tasks[t]["tests"]):
                    hit = True
                if hit:
                    mapped.append(t)
            regs = sorted({x for t in mapped for x in test_tokens(self.tasks[t]["tests"]) if x in self.reg})
            st = "GAP" if not mapped else ("REGISTERED" if regs else "FREE_TEXT_ONLY")
            counts[st] += 1
            if st == "GAP" and f[2].startswith("M"):
                self.errors.append(f"requirement {rid} (M) has no task")
            lines.append(f"| {rid} | {f[1][:80]} | {f[2]} | {f[3]} | {', '.join(mapped) or '—'} | "
                         f"{', '.join(regs[:12]) + (' …' if len(regs) > 12 else '') or '—'} | {st} |")
        head = ["# 15 — Traceability Matrix (generated)\n", "```text",
                "GENERATED_BY = tools/plan_graph.py from 13 + 14 + 23 (do not hand-edit)",
                "COVERAGE_RULE = REGISTERED: a live task maps the requirement and runs ≥1 registered test; FREE_TEXT_ONLY;",
                "                GAP. This is accounting, not semantic verification (Astro M-3, A2-06).",
                f"REQUIREMENTS = {len(reqs)} · REGISTERED = {counts['REGISTERED']} · FREE_TEXT_ONLY = {counts['FREE_TEXT_ONLY']} · GAP = {counts['GAP']}",
                "```\n", "| Req | Requirement | Pri | Phase | Tasks | Registered tests | Coverage |",
                "|---|---|---|---|---|---|---|"]
        return "\n".join(head + lines) + "\n", counts


def main(argv: list[str]) -> int:
    check = "--check" in argv
    root = Path(argv[argv.index("--root") + 1]) if "--root" in argv else DEFAULT_ROOT
    plan = Plan(root)
    plan.build()
    outputs, counts = plan.render()
    if check:
        for name, content in outputs.items():
            path = root / name
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                plan.errors.append(f"generated artifact drift: {name} differs from inputs (run without --check)")
    for e in plan.errors:
        print("ERROR:", e)
    print(f"tasks={len(plan.live)} tests={len(plan.reg)} suites={len(plan.suites)} errors={len(plan.errors)} coverage={counts}")
    if not check and not plan.errors:
        for name, content in outputs.items():
            (root / name).write_text(content, encoding="utf-8")
    return 1 if plan.errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
