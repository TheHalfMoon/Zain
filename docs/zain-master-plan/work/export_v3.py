import sys, json, importlib.util
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
root = Path(sys.argv[1]); out = Path(sys.argv[2])
spec = importlib.util.spec_from_file_location("plan_graph", root/"tools"/"plan_graph.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
p = m.Plan(root); p.build()
first = {}
for r in p.rel_order:
    for t in p.rel[r]:
        first.setdefault(t, r)
tasks = []
for t in sorted(p.live):
    d = p.tasks[t]
    tasks.append({"id": t, "phase": d["phase"], "deps": sorted(p.deps[t]), "release": first.get(t, "PD" if d["phase"]=="PD" else None),
                  "keys": sorted(k for k in d.keys())})
json.dump({"tasks": tasks, "tests": sorted(p.reg.keys()), "rel_order": p.rel_order, "errors": p.errors,
           "sample": {k: (str(v)[:200]) for k, v in p.tasks[sorted(p.live)[0]].items()}}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(tasks), len(p.reg), p.rel_order, len(p.errors))
print({k: (str(v)[:120]) for k, v in p.tasks["Q-00"].items()})
