"""Q-00: lockfile digests, upstream SPDX notice coverage, and licenses of the special packages. Read-only, in memory.
Usage: python -I q00_licenses.py <commit>"""
import hashlib, json, re, subprocess, sys, urllib.request
sys.stdout.reconfigure(encoding="utf-8")
REPO, C = "pingdotgg/t3code", sys.argv[1]

def raw(path):
    return subprocess.run(["gh", "api", "-H", "Accept: application/vnd.github.raw", f"repos/{REPO}/contents/{path}?ref={C}"],
                          capture_output=True).stdout

def ls(path):
    r = subprocess.run(["gh", "api", f"repos/{REPO}/contents/{path}?ref={C}"], capture_output=True)
    j = json.loads(r.stdout or b"[]"); return j if isinstance(j, list) else []

lock = raw("pnpm-lock.yaml")
print(f"pnpm-lock.yaml: {len(lock)} bytes sha256={hashlib.sha256(lock).hexdigest()} git-blob={hashlib.sha1(b'blob %d' % len(lock) + bytes(1) + lock).hexdigest()}")
lt = lock.decode("utf-8")
print("lockfileVersion:", re.search(r"^lockfileVersion: '?([^'\n]+)", lt, re.M).group(1))
pkgs = set(re.findall(r"^  '?((?:@[^/\s']+/)?[^@\s':]+)@([^:'\s(]+)", lt.split("\npackages:\n", 1)[1].split("\nsnapshots:\n", 1)[0], re.M))
print("packages in lockfile:", len(pkgs))

SPECIAL = ["@anthropic-ai/claude-agent-sdk", "@cursor/sdk", "heic-to", "electron-webauthn"]
for name in SPECIAL:
    vers = sorted(v for n, v in pkgs if n == name)
    for v in vers or ["(not in lockfile)"]:
        lic = "?"
        if vers:
            try:
                with urllib.request.urlopen(f"https://registry.npmjs.org/{name.replace('/', '%2F')}/{v}", timeout=30) as r:
                    m = json.load(r)
                lic = m.get("license") or m.get("licenses")
                deps = list((m.get("dependencies") or {}).keys())
                print(f"{name}@{v}: license={lic!r} deps={deps[:8]}{' …' if len(deps) > 8 else ''} optionalDeps={list((m.get('optionalDependencies') or {}).keys())[:6]}")
            except Exception as e:
                print(f"{name}@{v}: registry error {type(e).__name__}")
        else:
            print(f"{name}: not in lockfile")

spdx = ls("third-party-licenses/spdx")
print("\nthird-party-licenses/spdx:", [(e["name"], e.get("size")) for e in spdx][:12])
for e in spdx[:6]:
    if not e["name"].endswith(".json"): continue
    doc = json.loads(raw(f"third-party-licenses/spdx/{e['name']}"))
    P = doc.get("packages", [])
    lic = [p.get("licenseConcluded") or p.get("licenseDeclared") or "NONE" for p in P]
    bad = [p.get("name") for p, l in zip(P, lic) if l in ("NONE", "NOASSERTION", "")]
    from collections import Counter
    top = Counter(l for l in lic).most_common(8)
    print(f"  {e['name']}: packages={len(P)} no-license={len(bad)} {bad[:6]} top={top}")
    flags = sorted({l for l in lic if re.search(r"GPL|AGPL|SSPL|BUSL|Commons|proprietary|SEE LICENSE|UNLICENSED|LicenseRef", l, re.I)})
    print(f"    needs a decision: {flags[:10]}")
    names = {p.get("name") for p in P}
    print(f"    special present: {[s for s in SPECIAL if s in names]}")
