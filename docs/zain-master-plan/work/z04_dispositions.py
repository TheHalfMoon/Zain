"""Z-04: add a proposed disposition to every row of z04_branches.csv. Usage: python -I z04_dispositions.py <csv>"""
import csv, io, pathlib, sys
from collections import Counter
p = pathlib.Path(sys.argv[1]); rows = list(csv.DictReader(p.open(encoding="utf-8")))
PLANNING = {"docs/v3-unified-replan-20261027": "E: keep; contained in docs/zain-master-plan-20261108; delete after that merges",
            "docs/r0a-opus-start-20261102": "E: keep; contained in docs/zain-master-plan-20261108; delete after that merges",
            "docs/zain-master-plan-20261108": "E: keep; merge to main by one PR when G-03 replaces the governance chain (DEC-09, DEC-11)"}
OPEN = {"343": "D: close PR #343; keep branch as reference until the Core C-0x chain starts",
        "342": "D: close PR #342 after its salvage note lands in V3 09 (21 §3); then delete branch",
        "73": "D: close PR #73 after its salvage note lands (21 §4); then delete branch"}
for r in rows:
    pr = r["latest_pr"].split()[0].lstrip("#") if r["latest_pr"] != "none" else ""
    c = r["class"]
    if r["branch"] in PLANNING: d = PLANNING[r["branch"]]
    elif c == "MERGED_INTO_MAIN": d = "A: delete branch (content is in main" + (f"; PR #{pr} closed first" if "OPEN" in r["latest_pr"] else "") + ")"
    elif c == "PR_CLOSED_UNMERGED": d = f"B: delete branch (PR #{pr} keeps its head at refs/pull/{pr}/head)"
    elif c == "NO_PR": d = f"C: tag archive/{r['branch']} at {r['tip']}, then delete branch"
    elif c == "OPEN_PR": d = OPEN.get(pr, f"D: close PR #{pr} (21 §2), then delete branch (PR ref keeps its head)")
    else: d = "REVIEW"
    r["proposed_disposition"] = d
out = io.StringIO(); w = csv.DictWriter(out, fieldnames=list(rows[0].keys()), lineterminator="\n"); w.writeheader(); w.writerows(rows)
p.write_text(out.getvalue(), encoding="utf-8")
print("dispositions:", dict(Counter(r["proposed_disposition"][0] for r in rows)), "rows:", len(rows),
      "| since 2026-09-01:", dict(Counter(r["proposed_disposition"][0] for r in rows if r["last_commit"] >= "2026-09-01")))
print("since 2026-09-01 in group B:", [r["branch"] for r in rows if r["last_commit"] >= "2026-09-01" and r["proposed_disposition"][0] == "B"])
