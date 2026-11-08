"""Q-00 pre-build shipped-closure license listing for pingdotgg/t3code at a pin.
Production closure (dependencies + optionalDependencies, transitively) of apps/desktop, apps/server and apps/web,
following workspace links. Licenses come from the npm registry for each exact version. Read-only; lockfile parsed in
memory with yaml.safe_load. Writes the listing CSV given as argv[2].
Usage: python -I q00_closure.py <commit> <out.csv>"""
import csv, json, re, subprocess, sys, urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import yaml
sys.stdout.reconfigure(encoding="utf-8")
REPO, C, OUT = "pingdotgg/t3code", sys.argv[1], sys.argv[2]
ALLOW = {"Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "CC0-1.0", "ISC", "MIT", "OFL-1.1", "Unlicense"}  # upstream spdx/v3.28.0
ROOTS = ["apps/desktop", "apps/server", "apps/web"]

raw = subprocess.run(["gh", "api", "-H", "Accept: application/vnd.github.raw", f"repos/{REPO}/contents/pnpm-lock.yaml?ref={C}"],
                     capture_output=True).stdout.decode("utf-8")
doc = [d for d in yaml.safe_load_all(raw) if d and "importers" in d][-1]
importers, snaps, packages = doc["importers"], doc.get("snapshots", {}), doc.get("packages", {})
print(f"project lockfile: importers={len(importers)} packages={len(packages)} snapshots={len(snaps)}")

def prod(imp):
    out = {}
    for sec in ("dependencies", "optionalDependencies"):
        for n, v in (importers.get(imp, {}).get(sec) or {}).items():
            out[n] = v["version"] if isinstance(v, dict) else v
    return out

seen_imp, closure, stack, via = set(), set(), [], {}
def add_importer(imp, root):
    if imp in seen_imp: return
    seen_imp.add(imp)
    for n, v in prod(imp).items():
        v = str(v)
        if v.startswith("link:"):
            target = re.sub(r"^link:", "", v); base = imp.split("/")
            parts = (imp + "/" + target).split("/"); norm = []
            for p in parts:
                if p == "..": norm.pop()
                elif p not in (".", ""): norm.append(p)
            add_importer("/".join(norm), root)
        else:
            stack.append((f"{n}@{v}", root))
for r in ROOTS: add_importer(r, r)
while stack:
    key, root = stack.pop()
    if key in closure: continue
    closure.add(key); via.setdefault(key, root)
    s = snaps.get(key) or {}
    for sec in ("dependencies", "optionalDependencies"):
        for n, v in (s.get(sec) or {}).items():
            stack.append((f"{n}@{v}", root))

def base(key):
    k = re.sub(r"\(.*$", "", key)
    i = k.rfind("@", 1); return k[:i], k[i + 1:]
pkgs = sorted({base(k) for k in closure})
print(f"workspace importers reached: {len(seen_imp)}; shipped-closure packages (name@version): {len(pkgs)}")

def lic(nv):
    n, v = nv
    meta = packages.get(f"{n}@{v}", {})
    if "tarball" in (meta.get("resolution") or {}) or v.startswith(("http", "git", "file")):
        return n, v, "NON_REGISTRY", ""
    try:
        with urllib.request.urlopen(f"https://registry.npmjs.org/{n.replace('/', '%2F')}/{v}", timeout=30) as r:
            m = json.load(r)
        l = m.get("license")
        if isinstance(l, dict): l = l.get("type")
        if isinstance(l, list): l = " OR ".join(x.get("type", "?") if isinstance(x, dict) else str(x) for x in l)
        if not l and m.get("licenses"): l = " OR ".join(x.get("type", "?") if isinstance(x, dict) else str(x) for x in m["licenses"])
        return n, v, l or "NONE", ""
    except Exception as e:
        return n, v, "LOOKUP_ERROR", type(e).__name__

with ThreadPoolExecutor(16) as ex:
    rows = list(ex.map(lic, pkgs))

def ok(l):
    if l in ALLOW: return True
    parts = re.split(r"\s+OR\s+", l.strip("() "))
    if len(parts) > 1 and any(p.strip("() ") in ALLOW for p in parts): return True
    ands = re.split(r"\s+AND\s+", l.strip("() "))
    return len(ands) > 1 and all(p.strip("() ") in ALLOW for p in ands)

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n"); w.writerow(["package", "version", "license", "in_upstream_allowlist", "root", "note"])
    for n, v, l, note in rows:
        root = next((via[k] for k in closure if base(k) == (n, v)), "")
        w.writerow([n, v, l, "yes" if ok(l) else "no", root, note])
dist = Counter(l for _, _, l, _ in rows)
print("license distribution (top 12):", dist.most_common(12))
flag = [(n, v, l) for n, v, l, _ in rows if not ok(l)]
print(f"outside upstream allowlist: {len(flag)}")
for n, v, l in flag[:60]: print(f"   {n}@{v}: {l}")
print("specials in closure:", [f"{n}@{v} {l}" for n, v, l, _ in rows if re.search(r"claude-agent-sdk|cursor/sdk|heic-to|electron-webauthn", n)])
