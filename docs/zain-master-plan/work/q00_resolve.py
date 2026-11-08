"""Q-00: resolve licenses missing from npm metadata via the source repository's LICENSE (GitHub API), plus install-time
code and release digests. Read-only, in memory. Usage: python -I q00_resolve.py <commit>"""
import base64, json, re, subprocess, sys, urllib.request
sys.stdout.reconfigure(encoding="utf-8")
REPO, C = "pingdotgg/t3code", sys.argv[1]
UNRESOLVED = [("jsbi", "2.0.5"), ("map-stream", "0.1.0"), ("objc-js", "1.5.0"), ("@react-grab/cli", "0.1.44"),
              ("electron-webauthn", "1.3.1"), ("@electron-webauthn/macos", "1.3.1"), ("@electron-webauthn/types", "1.3.1"),
              ("micromark-extension-llm-math", "3.1.0"), ("@tsc-rs/typescript", "0.8.0")]

def gh(path, raw=False):
    args = ["gh", "api"] + (["-H", "Accept: application/vnd.github.raw"] if raw else []) + [path]
    r = subprocess.run(args, capture_output=True)
    return r.stdout if raw else (json.loads(r.stdout) if r.returncode == 0 and r.stdout else None)

for n, v in UNRESOLVED:
    try:
        with urllib.request.urlopen(f"https://registry.npmjs.org/{n.replace('/', '%2F')}/{v}", timeout=30) as r:
            m = json.load(r)
    except Exception as e:
        print(f"{n}@{v}: registry {type(e).__name__}"); continue
    lic = m.get("license") or m.get("licenses")
    repo = (m.get("repository") or {}).get("url", "") if isinstance(m.get("repository"), dict) else str(m.get("repository") or "")
    gm = re.search(r"github\.com[/:]([^/]+)/([^/.#]+)", repo)
    gl = gh(f"repos/{gm.group(1)}/{gm.group(2)}/license") if gm else None
    os_ = m.get("os"); cpu = m.get("cpu")
    print(f"{n}@{v}: npm license={lic!r} repo={gm.group(1) + '/' + gm.group(2) if gm else repo[:60]!r} "
          f"repo license={(gl or {}).get('license', {}).get('spdx_id') if gl else None} os={os_} cpu={cpu}")

def text(path):
    j = gh(f"repos/{REPO}/contents/{path}?ref={C}")
    return base64.b64decode(j["content"]).decode("utf-8", "replace") if j and j.get("encoding") == "base64" else None

pf = text(".pnpmfile.cjs") or ""
print(f"\n.pnpmfile.cjs: {len(pf.splitlines())} lines; hooks: {sorted(set(re.findall(r'(readPackage|afterAllResolved|updateConfig|preResolution|importPackage|fetchers)', pf)))}; "
      f"network/process use: {bool(re.search(r'child_process|https?:|fetch\(|exec', pf))}")
patches = gh(f"repos/{REPO}/contents/patches?ref={C}") or []
print("patches/:", [e["name"] for e in patches])
bs = text("native/browser-secret/main.c") or ""
print("native/browser-secret/main.c platform hints:", sorted(set(re.findall(r"#\s*include\s*<(windows\.h|Security/[^>]+|libsecret[^>]*|dbus[^>]*|CoreFoundation[^>]*)>", bs)))[:6])
rel = gh("repos/pingdotgg/t3code/releases/tags/v0.1.7") or {}
sums = next((a for a in rel.get("assets", []) if a["name"] == "SHA256SUMS"), None)
if sums:
    body = gh(f"repos/pingdotgg/t3code/releases/assets/{sums['id']}", raw=False)
    raw = subprocess.run(["gh", "api", "-H", "Accept: application/octet-stream", f"repos/pingdotgg/t3code/releases/assets/{sums['id']}"], capture_output=True).stdout.decode()
    print("SHA256SUMS win32 lines:", [l for l in raw.splitlines() if "win32" in l])
wf = text(".github/workflows/release-desktop.yml") or ""
print("Windows WSL/CLI-archive embedding lines:", [l.strip()[:140] for l in wf.splitlines() if re.search(r"wsl|linux cli archive", l, re.I)][:6])
