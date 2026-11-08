"""Z-08: fetch the Q-00 toolchain pins into a per-user folder, verify SHA-256, extract. No PATH or system changes.
Node: nodejs.org/dist, checked against that release's SHASUMS256.txt. pnpm: the GitHub release asset, checked
against the sha256 digest GitHub records for it (pnpm publishes no checksum file).
Usage: python -I z08_toolchain.py <dest root, e.g. D:/zain-build/tools>"""
import hashlib, json, pathlib, subprocess, sys, urllib.request, zipfile
sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(sys.argv[1])
NODE_V, PNPM_V = "26.12.1", "12.14.0"
NODE_ZIP = f"node-v{NODE_V}-win-x64.zip"

def get(url):
    with urllib.request.urlopen(url, timeout=120) as r:
        return r.read()

sums = get(f"https://nodejs.org/dist/v{NODE_V}/SHASUMS256.txt").decode()
node_sha = next(l.split()[0] for l in sums.splitlines() if l.endswith("  " + NODE_ZIP))
rel = json.loads(subprocess.run(["gh", "api", f"repos/pnpm/pnpm/releases/tags/v{PNPM_V}"], capture_output=True).stdout)
asset = next(a for a in rel["assets"] if a["name"] == "pnpm-win32-x64.zip")
pnpm_sha = asset["digest"].split(":", 1)[1]

ITEMS = [(NODE_ZIP, f"https://nodejs.org/dist/v{NODE_V}/{NODE_ZIP}", node_sha, ROOT / f"node-v{NODE_V}-win-x64", "SHASUMS256.txt"),
         ("pnpm-win32-x64.zip", asset["browser_download_url"], pnpm_sha, ROOT / f"pnpm-{PNPM_V}", "GitHub asset digest")]
for name, url, want, dest, source in ITEMS:
    dl = ROOT / "downloads" / dest.name
    dl.mkdir(parents=True, exist_ok=False)          # its own new, empty directory
    data = get(url); (dl / name).write_bytes(data)
    got = hashlib.sha256(data).hexdigest()
    print(f"{name}: {len(data)} bytes sha256={got} expected({source})={want} -> {'MATCH' if got == want else 'MISMATCH'}")
    if got != want: sys.exit("checksum mismatch: nothing extracted")
    with zipfile.ZipFile(dl / name) as z:
        for m in z.namelist():                      # refuse absolute paths and parent escapes
            if m.startswith(("/", "\\")) or ".." in pathlib.PurePosixPath(m).parts or ":" in m:
                sys.exit(f"unsafe member {m!r}: nothing extracted")
        dest.mkdir(parents=True, exist_ok=False)
        z.extractall(dest)
    print(f"  extracted {len(z.namelist())} entries to {dest}")
