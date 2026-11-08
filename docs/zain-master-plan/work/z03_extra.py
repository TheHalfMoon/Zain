"""Artifacts, sampled Actions logs and the R18 redaction diff. In memory; prints counts/categories only."""
import io, json, re, subprocess, sys, zipfile
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".")
import z03_scan as S
REPO = "TheHalfMoon/Zain"; W = sys.argv[1]

def gh_bytes(path):
    return subprocess.run(["gh", "api", path], capture_output=True).stdout

def scan_blob(label, data):
    hits = {}
    for name, rx in S.RX:
        for m in rx.finditer(data):
            cls = S.classify(name, m.group(0), label)
            if name in ("email",) and cls != "EMAIL": continue
            if cls in ("GENERIC", "NOREPLY_OR_VENDOR"): continue
            key = (name, cls, S.fp(m.group(0)))
            hits[key] = hits.get(key, 0) + 1
    return hits

def scan_zip(label, raw):
    total = {}
    try:
        z = zipfile.ZipFile(io.BytesIO(raw))
    except zipfile.BadZipFile:
        print(label, "not a zip, bytes=", len(raw)); return
    for n in z.namelist():
        if n.endswith("/"): continue
        data = z.read(n)
        if b"\x00" in data[:4096]: continue
        for k, v in scan_blob(f"{label}:{n}", data.decode("utf-8", "replace")).items():
            total[k] = total.get(k, 0) + v
    print(f"{label}: files={len(z.namelist())} findings={[(k[0], k[1], k[2], v) for k, v in sorted(total.items())] or 'none'}")

arts = json.loads(gh_bytes(f"repos/{REPO}/actions/artifacts") or b"{}").get("artifacts", [])
for a in arts:
    scan_zip(f"artifact {a['name']}", gh_bytes(f"repos/{REPO}/actions/artifacts/{a['id']}/zip"))

runs = json.loads(gh_bytes(f"repos/{REPO}/actions/runs?per_page=20") or b"{}").get("workflow_runs", [])
agg = {}
for r in runs:
    raw = gh_bytes(f"repos/{REPO}/actions/runs/{r['id']}/logs")
    try:
        z = zipfile.ZipFile(io.BytesIO(raw))
    except zipfile.BadZipFile:
        continue
    for n in z.namelist():
        for k, v in scan_blob("log", z.read(n).decode("utf-8", "replace")).items():
            agg[k] = agg.get(k, 0) + v
print(f"sampled logs: runs={len(runs)} findings={[(k[0], k[1], v) for k, v in sorted(agg.items())] or 'none'}")

# R18 redaction: what categories of lines were removed between ef19a3f/c376917 and HEAD
repo = f"{W}/zain"
f = "specs/008-wepld-v3-unified-replan/research/R18_DESKGATE.md"
for base in ("c376917", "ef19a3f"):
    d = subprocess.run(["git", "-C", repo, "diff", "-U0", base, "origin/docs/r0a-opus-start-20261102", "--", f], capture_output=True).stdout.decode("utf-8", "replace")
    removed = [l[1:] for l in d.splitlines() if l.startswith("-") and not l.startswith("---")]
    cats = {"windows-user-path": 0, "local-drive-path": 0, "hostname-or-machine": 0, "version-or-install": 0, "other": 0}
    for l in removed:
        if re.search(r"(?i)[A-Z]:\\\\?Users", l): cats["windows-user-path"] += 1
        elif re.search(r"(?i)\b[A-Z]:\\\\", l): cats["local-drive-path"] += 1
        elif re.search(r"(?i)(DESKTOP-|hostname|computer ?name|machine)", l): cats["hostname-or-machine"] += 1
        elif re.search(r"(?i)(installed|version|\bv\d+\.\d+)", l): cats["version-or-install"] += 1
        else: cats["other"] += 1
    print(f"R18 lines removed since {base}: {len(removed)} -> {cats}")
