"""Z-04 read-only inventory: every remote branch of TheHalfMoon/Zain with its PR history and relation to main.
Uses the local clone's remote-tracking refs (checked equal to the remote with ls-remote first) and the PR list API.
Usage: python -I z04_inventory.py <zain clone> <out.csv>"""
import csv, json, subprocess, sys
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding="utf-8")
CLONE, OUT = sys.argv[1], sys.argv[2]
G = ["git", "-c", "maintenance.auto=false", "-C", CLONE]
def git(*a): return subprocess.run(G + list(a), capture_output=True, text=True, encoding="utf-8").stdout

remote = {l.split()[1].removeprefix("refs/heads/"): l.split()[0] for l in git("ls-remote", "origin", "refs/heads/*").splitlines()}
local = {}
for l in git("for-each-ref", "refs/remotes/origin", "--format=%(refname:short)\t%(objectname)\t%(committerdate:iso-strict)\t%(subject)").splitlines():
    name, sha, date, subj = l.split("\t", 3)
    if name in ("origin", "origin/HEAD") or name.startswith("origin/pr/"): continue
    local[name.removeprefix("origin/")] = (sha, date, subj)
stale = [b for b in remote if local.get(b, ("",))[0] != remote[b]]
print(f"remote branches={len(remote)} local tracking={len(local)} differing={len(stale)} {stale[:5]}")

prs = json.loads(subprocess.run(["gh", "pr", "list", "-R", "TheHalfMoon/Zain", "--state", "all", "--limit", "600", "--json",
    "number,title,state,headRefName,baseRefName,isDraft,mergedAt,closedAt,updatedAt,headRefOid,additions,deletions"],
    capture_output=True, text=True, encoding="utf-8").stdout)
by_head = defaultdict(list)
for p in prs: by_head[p["headRefName"]].append(p)
print(f"PRs: {len(prs)} -> {dict(Counter(p['state'] for p in prs))}")
print("open PRs:", sorted(p["number"] for p in prs if p["state"] == "OPEN"))

rows = []
for b, sha in sorted(remote.items()):
    if b == "main": continue
    _, date, subj = local.get(b, (sha, "", ""))
    behind, ahead = git("rev-list", "--left-right", "--count", f"origin/main...{sha}").split() or ["?", "?"]
    ancestor = subprocess.run(G + ["merge-base", "--is-ancestor", sha, "origin/main"]).returncode == 0
    ps = sorted(by_head.get(b, []), key=lambda p: p["number"])
    last = ps[-1] if ps else None
    pr_state = f"#{last['number']} {last['state']}" if last else "none"
    head_matches = bool(last and last.get("headRefOid") == sha)
    if ancestor: cls = "MERGED_INTO_MAIN"
    elif last and last["state"] == "MERGED": cls = "PR_MERGED" + ("" if head_matches else "_THEN_MORE_COMMITS")
    elif last and last["state"] == "OPEN": cls = "OPEN_PR"
    elif last and last["state"] == "CLOSED": cls = "PR_CLOSED_UNMERGED"
    else: cls = "NO_PR"
    rows.append([b, sha[:10], date[:10], ahead, behind, "yes" if ancestor else "no", pr_state, cls, subj[:80]])

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["branch", "tip", "last_commit", "ahead_of_main", "behind_main", "ancestor_of_main", "latest_pr", "class", "tip_subject"])
    w.writerows(rows)
recent = [r for r in rows if r[2] >= "2026-09-01"]
print(f"non-main branches={len(rows)}; updated since 2026-09-01={len(recent)}")
print("class (all):", dict(Counter(r[7] for r in rows)))
print("class (since 2026-09-01):", dict(Counter(r[7] for r in recent)))
for r in rows:
    if r[7] in ("OPEN_PR", "NO_PR", "PR_MERGED_THEN_MORE_COMMITS") and r[2] >= "2026-09-01":
        print(f"  {r[7]:27} {r[0][:58]:58} {r[2]} +{r[3]}/-{r[4]} {r[6]}")
