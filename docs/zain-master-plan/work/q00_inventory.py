"""Q-00 read-only inventory of pingdotgg/t3code at a pin, via the GitHub API. Prints summaries only.
Usage: python -I q00_inventory.py <commit>"""
import base64, json, re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
REPO, C = "pingdotgg/t3code", sys.argv[1]

def api(path):
    r = subprocess.run(["gh", "api", path], capture_output=True)
    return json.loads(r.stdout) if r.returncode == 0 and r.stdout else None

def text(path):
    j = api(f"repos/{REPO}/contents/{path}?ref={C}")
    if not j or j.get("encoding") != "base64": return None
    return base64.b64decode(j["content"]).decode("utf-8", "replace")

def ls(path):
    j = api(f"repos/{REPO}/contents/{path}?ref={C}")
    return [(e["name"], e["type"], e.get("size", 0)) for e in j] if isinstance(j, list) else []

root = json.loads(text("package.json"))
print("root packageManager:", root.get("packageManager"), "| engines:", root.get("engines"))
print("root scripts (build/dist/release):", {k: v[:90] for k, v in root.get("scripts", {}).items() if re.search(r"build|dist|release|package|licen", k)})
for f in (".nvmrc", ".node-version", "rust-toolchain.toml", "rust-toolchain", "native/rust-toolchain.toml"):
    t = text(f)
    if t: print(f"{f}: {t.strip()[:120]}")
print("native/:", ls("native"))
for sub, kind, _ in ls("native"):
    if kind == "dir": print(f"  native/{sub}/:", [n for n, _, _ in ls(f'native/{sub}')][:12])
print("third-party-licenses/:", ls("third-party-licenses")[:12])
cfg = text("third-party-licenses.config.json")
print("third-party-licenses.config.json:", (cfg or "")[:600].replace("\n", " "))

SPECIAL = re.compile(r"heic|webauthn|anthropic|claude|cursor", re.I)
for app in ("apps/desktop", "apps/server", "apps/web"):
    pj = text(f"{app}/package.json")
    if not pj: continue
    d = json.loads(pj)
    deps, dev = d.get("dependencies", {}), d.get("devDependencies", {})
    print(f"\n{app}: name={d.get('name')} deps={len(deps)} devDeps={len(dev)} main={d.get('main')}")
    print("  special:", {k: v for k, v in {**deps, **dev}.items() if SPECIAL.search(k)})
    if d.get("build"): print("  electron-builder config keys:", list(d["build"])[:15])
for p in ("packages/provider-cursor", "packages/provider-core"):
    pj = text(f"{p}/package.json")
    if pj:
        d = json.loads(pj); print(f"{p}: special deps", {k: v for k, v in d.get("dependencies", {}).items() if SPECIAL.search(k)})

for wf in ("release-desktop.yml", "windows-tests.yml", "release.yml"):
    t = text(f".github/workflows/{wf}") or ""
    lines = t.splitlines()
    hits = [l.strip()[:150] for l in lines if re.search(r"windows|win32|runs-on|node-version|pnpm (install|run|build)|sea|archive|--win|nsis|setup-node|rust|msvc|SIGN|signtool", l, re.I)]
    print(f"\n{wf} ({len(lines)} lines): first relevant lines:")
    for h in hits[:24]: print("   ", h)

lock = api(f"repos/{REPO}/contents/pnpm-lock.yaml?ref={C}")
print("\npnpm-lock.yaml blob sha:", lock and lock.get("sha"), "size:", lock and lock.get("size"))
