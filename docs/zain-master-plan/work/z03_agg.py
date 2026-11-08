"""Aggregate z03_scan JSON lines from stdin. Prints counts and per-fingerprint locations; never values."""
import json, sys
from collections import defaultdict
sys.stdout.reconfigure(encoding="utf-8")
SECRET_RULES = {"aws-access-key", "github-token", "openai-key", "anthropic-key", "google-api-key", "slack-token", "stripe-live",
                "huggingface-token", "npm-token", "private-key-block", "jwt", "azure-account-key", "generic-secret-assignment"}
counts = defaultdict(int); fps = defaultdict(lambda: defaultdict(list)); users = defaultdict(lambda: defaultdict(set)); summaries = []
for line in sys.stdin:
    try:
        r = json.loads(line)
    except ValueError:
        continue
    if r.get("summary"):
        summaries.append(r); continue
    key = (r["src"], r["rule"], r["cls"])
    counts[key] += 1
    if r["rule"] in SECRET_RULES or r["cls"] in ("EMAIL", "ENVIRONMENT_DETAIL") or r["rule"] == "commit-identity-email":
        locs = fps[key][r["fp"]]
        if len(locs) < 4:
            locs.append(f"{r['commit']}:{r['path']}")
    if r["cls"] == "PERSONAL_PATH":
        users[r["src"]][r["user_fp"]].add(r["path"])
for s in summaries:
    print("SUMMARY", json.dumps(s))
print("== counts (src, rule, class) -> hits / distinct values")
for key in sorted(counts):
    print(f"{key} -> {counts[key]} / {len(fps[key]) if key in fps else '-'}")
print("== secret-rule and email/env fingerprints (non-placeholder classes only)")
for key in sorted(fps):
    if key[2] in ("LIKELY_PLACEHOLDER_OR_FIXTURE", "NOREPLY_OR_VENDOR", "GENERIC"):
        continue
    for f, locs in fps[key].items():
        print(f"{key[0]} {key[1]} {key[2]} fp={f} at {' | '.join(locs)}")
print("== personal user-path names (by fingerprint): distinct files")
for src, d in users.items():
    for u, paths in sorted(d.items(), key=lambda kv: -len(kv[1])):
        print(f"{src} user_fp={u} files={len(paths)} e.g. {sorted(paths)[:4]}")
