"""Q-00: re-check V3 source citations (`path@36d4d711:Lx-y`) at the new T3 pin, and the R02 §10 seam symbols.
Read-only: GitHub trees/contents API and local `git show` of the V3 docs. Usage:
  python -I q00_citations.py <old sha> <new sha> <zain clone> <out.csv>"""
import csv, difflib, json, re, subprocess, sys
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
OLD, NEW, CLONE, OUT = sys.argv[1:5]
REF = "origin/docs/r0a-opus-start-20261102:specs/008-wepld-v3-unified-replan/"
DOCS = ["research/R02_T3_CODE.md", "research/R11_T3_FILE_MANIFEST.md"]
CIT = re.compile(r"([A-Za-z0-9_./-]+\.(?:ts|tsx|rs|js|cjs|mjs|json))@36d4d711(?::(L?\d+(?:[-–]\d+)?(?:,\s*L?\d+(?:[-–]\d+)?)*))?")

def show(path):
    return subprocess.run(["git", "-c", "maintenance.auto=false", "-C", CLONE, "show", REF + path], capture_output=True).stdout.decode("utf-8", "replace")

def tree(sha):
    j = json.loads(subprocess.run(["gh", "api", f"repos/pingdotgg/t3code/git/trees/{sha}?recursive=1"], capture_output=True).stdout)
    return [e["path"] for e in j["tree"] if e["type"] == "blob"]

old_paths, new_paths = tree(OLD), tree(NEW)
new_set = set(new_paths)
cache = {}
def file(sha, path):
    k = (sha, path)
    if k not in cache:
        r = subprocess.run(["gh", "api", "-H", "Accept: application/vnd.github.raw", f"repos/pingdotgg/t3code/contents/{path}?ref={sha}"], capture_output=True)
        cache[k] = r.stdout.decode("utf-8", "replace").split("\n") if r.returncode == 0 else None
    return cache[k]

def resolve(partial, paths, prefer=""):
    if partial in paths: return partial, ""
    m = [p for p in paths if p.endswith("/" + partial)]
    if len(m) > 1 and prefer: m = [p for p in m if p.startswith(prefer)] or m
    return (m[0], "" if len(m) == 1 else f"ambiguous:{len(m)}") if m else (None, "unresolved")

def anchor(lines, i, step):
    while 0 <= i < len(lines) and len(lines[i].strip()) < 12: i += step
    return i if 0 <= i < len(lines) else None

def find(new, text, near):
    hits = [j for j, l in enumerate(new) if l.strip() == text]
    return min(hits, key=lambda j: abs(j - near)) if hits else None

rows, seen = [], set()
for doc in DOCS:
    for ln, line in enumerate(show(doc).split("\n"), 1):
        last_dir = ""
        for m in CIT.finditer(line):
            part, ranges = m.group(1), m.group(2)
            if "/" in part and part.count("/") > 1: last_dir = part.rsplit("/", 1)[0]
            key = (part, ranges)
            if key in seen: continue
            seen.add(key)
            op, note = resolve(part, old_paths, prefer=last_dir or "apps/server")
            if not op:
                rows.append([doc, ln, m.group(0), "", "", "", "", "PATH_UNRESOLVED", ""]); continue
            np_ = op if op in new_set else (resolve(op.rsplit("/", 1)[-1], new_paths, prefer=op.rsplit("/", 2)[0])[0])
            if not ranges:
                rows.append([doc, ln, m.group(0), op, np_ or "", "", "", "FILE_PRESENT" if np_ == op else ("FILE_MOVED" if np_ else "FILE_REMOVED"), note]); continue
            old, new = file(OLD, op), (file(NEW, np_) if np_ else None)
            for rg in re.split(r",\s*", ranges):
                a, _, b = rg.lstrip("L").replace("–", "-").partition("-")
                s, e = int(a), int(b or a)
                if not old or e > len(old):
                    rows.append([doc, ln, m.group(0), op, np_ or "", f"{s}-{e}", "", "OLD_RANGE_INVALID", note]); continue
                if not new:
                    rows.append([doc, ln, m.group(0), op, "", f"{s}-{e}", "", "FILE_REMOVED", note]); continue
                ia, ib = anchor(old, s - 1, +1), anchor(old, e - 1, -1)
                if ia is None or ib is None or ib < ia: ia = ib = s - 1
                ja = find(new, old[ia].strip(), ia); jb = find(new, old[ib].strip(), (ja or ia) + (ib - ia))
                if ja is None or jb is None or jb < ja:
                    rows.append([doc, ln, m.group(0), op, np_, f"{s}-{e}", "", "ANCHOR_NOT_FOUND", note]); continue
                ns, ne = s + (ja - ia), e + (jb - ib)
                ratio = difflib.SequenceMatcher(None, old[s - 1:e], new[ns - 1:ne], autojunk=False).ratio()
                st = ("SAME_LINES" if (ns, ne) == (s, e) and ratio == 1 else "SHIFTED" if ratio == 1 else
                      "CHANGED_MINOR" if ratio >= 0.8 else "CHANGED_MAJOR")
                rows.append([doc, ln, m.group(0), op, np_ if np_ != op else "", f"{s}-{e}", f"{ns}-{ne}", st, f"{note} similarity={ratio:.2f}".strip()])

with open(OUT, "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(["doc", "doc_line", "citation", "old_path", "new_path_if_moved", "old_lines", "new_lines", "status", "note"])
    w.writerows(rows)
print(f"citations checked: {len(rows)} -> {dict(Counter(r[7] for r in rows))}")
for r in rows:
    if r[7] in ("ANCHOR_NOT_FOUND", "FILE_REMOVED", "FILE_MOVED", "PATH_UNRESOLVED", "OLD_RANGE_INVALID", "CHANGED_MAJOR"):
        print(f"   {r[7]:17} {r[0].split('/')[-1][:12]}:{r[1]} {r[2][:70]} {r[4][:60]} {r[8]}")

# R02 §10 seam symbols at the new pin
sec = show(DOCS[0]).split("## 10.", 1)[1].split("\n## 11.", 1)[0]
print("\nR02 §10 seams at the new pin:")
for line in sec.split("\n"):
    m = re.match(r"\|\s*(S\d+)\s*\|\s*\*?\*?([^|*]+)", line)
    if not m: continue
    files = []
    for c in CIT.finditer(line):
        op, _ = resolve(c.group(1), old_paths, "apps/server")
        if op: files.append(op if op in new_set else resolve(op.rsplit("/", 1)[-1], new_paths)[0])
    for c in re.finditer(r"`((?:apps|packages)/[^`@\s]+\.ts)`", line):
        files.append(c.group(1) if c.group(1) in new_set else resolve(c.group(1).rsplit("/", 1)[-1], new_paths)[0])
    idents = {x for x in re.findall(r"`([A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)?)`", line) if not x.endswith(("ts", "rs"))}
    present = {}
    for ident in idents:
        last = ident.split(".")[-1]
        present[ident] = any(f and file(NEW, f) and any(re.search(rf"\b{re.escape(last)}\b", l) for l in file(NEW, f)) for f in files)
    missing_files = [f for f in files if not f]
    print(f"  {m.group(1)} {m.group(2).strip()[:42]:42} files={len(files)} missing={len(missing_files)} "
          f"symbols found={sum(present.values())}/{len(present)} {[k for k, v in present.items() if not v][:5]}")
