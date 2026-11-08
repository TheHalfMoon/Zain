"""Q-00: compare the T3 trees at the old pin and the new pin, and classify every path named in the V3 R11 manifest.
Read-only (GitHub trees API + local git show). Usage: python -I q00_r11_delta.py <old> <new> <zain clone> <out.csv>"""
import csv, json, re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
OLD, NEW, CLONE, OUT = sys.argv[1:5]
R11 = "origin/docs/r0a-opus-start-20261102:specs/008-wepld-v3-unified-replan/research/R11_T3_FILE_MANIFEST.md"

def tree(sha):
    j = json.loads(subprocess.run(["gh", "api", f"repos/pingdotgg/t3code/git/trees/{sha}?recursive=1"], capture_output=True).stdout)
    if j.get("truncated"): print("WARNING: tree truncated for", sha)
    return {e["path"]: e["sha"] for e in j["tree"] if e["type"] == "blob"}

a, b = tree(OLD), tree(NEW)
added, removed = set(b) - set(a), set(a) - set(b)
changed = {p for p in set(a) & set(b) if a[p] != b[p]}
print(f"files: old={len(a)} new={len(b)} added={len(added)} removed={len(removed)} changed={len(changed)} unchanged={len(set(a) & set(b)) - len(changed)}")
for top in ("apps/desktop", "apps/server", "apps/web", "packages", "native"):
    f = lambda s: sum(1 for p in s if p.startswith(top))
    print(f"  {top}: added={f(added)} removed={f(removed)} changed={f(changed)}")

man = subprocess.run(["git", "-c", "maintenance.auto=false", "-C", CLONE, "show", R11], capture_output=True).stdout.decode("utf-8", "replace")
paths = sorted({m.group(1) for m in re.finditer(r"`((?:apps|packages|native|scripts|\.github)/[^`\s*]+?\.[A-Za-z0-9]+)`", man)})
rows = []
for p in paths:
    state = ("MISSING_AT_BOTH" if p not in a and p not in b else "ADDED" if p not in a else
             "REMOVED_OR_MOVED" if p not in b else "CHANGED" if a[p] != b[p] else "UNCHANGED")
    rows.append((p, state))
with open(OUT, "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, lineterminator="\n"); w.writerow(["r11_path", "state_36d4d711_to_v0.1.7"]); w.writerows(rows)
from collections import Counter
print(f"R11 manifest paths: {len(paths)} -> {dict(Counter(s for _, s in rows))}")
for p, s in rows:
    if s == "REMOVED_OR_MOVED": print("   removed/moved:", p)
