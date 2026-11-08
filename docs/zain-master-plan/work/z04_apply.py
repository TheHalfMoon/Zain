"""Z-04 application, founder-approved in chat 2026-11-08 ("Yes, apply all": close 12 PRs, tag 34 branches, delete 348).
Stages, each re-checking the remote state first:
  manifest <out.csv>   full SHA of every non-main branch with its group and action (commit this before any change)
  tags                 create and push archive/<branch> tags for group C, then verify them on the remote
  close                close the 12 open PRs with a pointer to 21 §2
  delete               delete the branches of groups A, B, C (only if its tag verifies) and D (except #343's)
  verify               print the remaining heads, archive tags and open PRs
Restore a deleted branch: git push origin <full_sha>:refs/heads/<branch>   (SHA from the manifest)
Usage: python -I z04_apply.py <zain clone> <z04_branches.csv> <stage> [args]"""
import csv, json, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
CLONE, CSV, STAGE = sys.argv[1], sys.argv[2], sys.argv[3]
REPO = "TheHalfMoon/Zain"
G = ["git", "-c", "maintenance.auto=false", "-C", CLONE]
KEEP = {"docs/v3-unified-replan-20261027", "docs/r0a-opus-start-20261102", "docs/zain-master-plan-20261108",
        "codex/astro-c01-s3-contracts-20260921"}
OPEN_PRS = [1, 73, 81, 88, 136, 159, 162, 164, 342, 343, 346, 347]

def run(cmd, check=True):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if check and r.returncode: sys.exit(f"FAILED {' '.join(cmd[:6])}: {r.stderr.strip()[:300]}")
    return r.stdout

def heads(): return {l.split()[1][11:]: l.split()[0] for l in run(G + ["ls-remote", "origin", "refs/heads/*"]).splitlines()}
def tags(): return {l.split()[1][10:]: l.split()[0] for l in run(G + ["ls-remote", "origin", "refs/tags/archive/*"]).splitlines()}
rows = list(csv.DictReader(open(CSV, encoding="utf-8")))
remote = heads()
plan = []
for r in rows:
    b, grp = r["branch"], r["proposed_disposition"][0]
    sha = remote.get(b)
    if sha and not sha.startswith(r["tip"]) and b not in KEEP: sys.exit(f"STOP: {b} moved since the inventory ({r['tip']} -> {sha[:10]})")
    action = "keep" if b in KEEP else ("tag+delete" if grp == "C" else "delete")
    plan.append((b, sha or "", grp, action, r["latest_pr"]))

if STAGE == "manifest":
    with open(sys.argv[4], "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n"); w.writerow(["branch", "full_sha", "group", "action", "latest_pr"]); w.writerows(plan)
    from collections import Counter
    print("manifest:", dict(Counter(p[3] for p in plan)), "rows", len(plan))

elif STAGE == "tags":
    todo = [(b, s) for b, s, g, a, _ in plan if a == "tag+delete" and s]
    for b, s in todo: run(G + ["tag", "-f", f"archive/{b}", s])
    for i in range(0, len(todo), 40):
        run(G + ["push", "origin"] + [f"refs/tags/archive/{b}:refs/tags/archive/{b}" for b, _ in todo[i:i + 40]])
    t = tags(); bad = [b for b, s in todo if t.get(b) != s]
    print(f"archive tags pushed: {len(todo)}; verified on remote: {len(todo) - len(bad)}; mismatched: {bad}")

elif STAGE == "close":
    for n in OPEN_PRS:
        st = json.loads(run(["gh", "pr", "view", str(n), "-R", REPO, "--json", "state"]))["state"]
        if st != "OPEN": print(f"#{n} already {st}"); continue
        msg = ("Closed by the Zain master-plan reconciliation (task Z-04), approved by the founder on 2026-11-08. The reason "
               "for this PR is in docs/zain-master-plan/21-BRANCH-PR-RECONCILIATION.md §2 on branch docs/zain-master-plan-20261108. "
               "This PR's head commit stays available here.")
        run(["gh", "pr", "close", str(n), "-R", REPO, "--comment", msg])
        print(f"#{n} closed")

elif STAGE == "delete":
    t = tags()
    todo = []
    for b, s, g, a, _ in plan:
        if a == "keep" or not s: continue
        if a == "tag+delete" and t.get(b) != s: print(f"SKIP {b}: archive tag missing or different"); continue
        todo.append(b)
    for i in range(0, len(todo), 40):
        run(G + ["push", "origin", "--delete"] + todo[i:i + 40])
    left = heads(); still = [b for b in todo if b in left]
    print(f"deleted: {len(todo) - len(still)} of {len(todo)}; still present: {still}")

elif STAGE == "verify":
    h, t = heads(), tags()
    openprs = json.loads(run(["gh", "pr", "list", "-R", REPO, "--state", "open", "--limit", "50", "--json", "number"]))
    print(f"remaining heads ({len(h)}): {sorted(h)}")
    print(f"archive tags: {len(t)}; open PRs: {sorted(p['number'] for p in openprs)}")
