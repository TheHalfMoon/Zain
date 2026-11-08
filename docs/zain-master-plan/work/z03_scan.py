"""Z-03 exposure scan. Streams git history and GitHub text through regex rules IN MEMORY.
Never prints or stores a matched secret value: only rule, location and a sha256 fingerprint prefix.
Usage: python -I z03_scan.py <label> git <repo_dir>   |   python -I z03_scan.py <label> text <owner/repo>
Output: JSON lines on stdout (one per finding) + a summary line."""
import hashlib, json, re, subprocess, sys

RULES = [
    ("aws-access-key", r"\b(AKIA|ASIA)[0-9A-Z]{16}\b"),
    ("github-token", r"\b(gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{60,})\b"),
    ("openai-key", r"\bsk-(proj-|svcacct-)?[A-Za-z0-9_-]{32,}\b"),
    ("anthropic-key", r"\bsk-ant-[A-Za-z0-9_-]{32,}\b"),
    ("google-api-key", r"\bAIza[0-9A-Za-z_-]{35}\b"),
    ("slack-token", r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b"),
    ("stripe-live", r"\b(sk|rk)_live_[A-Za-z0-9]{20,}\b"),
    ("huggingface-token", r"\bhf_[A-Za-z0-9]{30,}\b"),
    ("npm-token", r"\bnpm_[A-Za-z0-9]{36}\b"),
    ("private-key-block", r"-----BEGIN ((RSA|EC|DSA|OPENSSH|PGP|ENCRYPTED) )?PRIVATE KEY( BLOCK)?-----"),
    ("jwt", r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
    ("azure-account-key", r"AccountKey=[A-Za-z0-9+/=]{40,}"),
    ("generic-secret-assignment", r"(?i)\b(api[_-]?key|secret|token|passwd|password|client[_-]?secret)\b\s*[:=]\s*['\"][^'\"\s]{16,}['\"]"),
    ("windows-user-path", r"(?i)\b[A-Z]:\\\\?Users\\\\?([A-Za-z0-9._-]+)"),
    ("posix-home-path", r"(?:/Users|/home)/([A-Za-z0-9._-]+)/"),
    ("onedrive-path", r"(?i)OneDrive\\\\?(Desktop|Documents)"),
    ("windows-machine-name", r"\b(DESKTOP|LAPTOP)-[A-Z0-9]{7}\b"),
    ("email", r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    ("private-ipv4", r"\b(10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})\b"),
]
RX = [(n, re.compile(p)) for n, p in RULES]
GENERIC_USERS = {"runner", "runneradmin", "user", "username", "you", "me", "name", "default", "public", "administrator",
                 "all", "shared", "example", "foo", "bar", "test", "ubuntu", "admin", "node", "app", "root", "builder", "vscode"}
PLACEHOLDER = re.compile(r"(?i)(example|dummy|placeholder|redact|xxxx|your[_-]|fake|sample|test|changeme|<|\$\{|\*\*\*|\.\.\.)")
NOREPLY = re.compile(r"(?i)(noreply|no-reply|example\.(com|org)|users\.noreply\.github\.com|@anthropic\.com$|@openai\.com$|localhost)")

def fp(v): return hashlib.sha256(v.encode("utf-8", "replace")).hexdigest()[:12]

def classify(rule, value, path):
    if rule in ("windows-user-path", "posix-home-path"):
        m = re.search(r"(?:Users|home)[\\/]+([A-Za-z0-9._-]+)", value)
        u = (m.group(1) if m else "").lower()
        return "GENERIC" if u in GENERIC_USERS else "PERSONAL_PATH"
    if rule == "email":
        return "NOREPLY_OR_VENDOR" if NOREPLY.search(value) else "EMAIL"
    if rule in ("private-ipv4", "windows-machine-name", "onedrive-path"):
        return "ENVIRONMENT_DETAIL"
    p = (path or "").lower()
    if PLACEHOLDER.search(value) or any(k in p for k in ("test", "fixture", "mock", "example", "third_party/", "vendor", "/docs/")):
        return "LIKELY_PLACEHOLDER_OR_FIXTURE"
    return "NEEDS_REVIEW"

def emit(label, rule, value, where):
    rec = dict(src=label, rule=rule, fp=fp(value), cls=classify(rule, value, where.get("path", "")), **where)
    if rule in ("windows-user-path", "posix-home-path"):
        m = re.search(r"(?:Users|home)[\\/]+([A-Za-z0-9._-]+)", value)
        rec["user_fp"] = fp((m.group(1) if m else "").lower())
    print(json.dumps(rec))

def scan_text(label, text, where):
    for name, rx in RX:
        for m in rx.finditer(text):
            emit(label, name, m.group(0), where)

def scan_git(label, repo):
    # added lines of every commit on every ref (diffs), plus commit messages and author/committer identities
    p = subprocess.Popen(["git", "-C", repo, "log", "--all", "-p", "-U0", "--no-color", "--no-ext-diff", "--no-renames",
                          "--format=@@COMMIT %H%n%B"], stdout=subprocess.PIPE)
    commit = path = None
    for raw in p.stdout:
        line = raw.decode("utf-8", "replace").rstrip("\n")
        if line.startswith("@@COMMIT "):
            commit = line[9:21]; path = None; continue
        if line.startswith("+++ "):
            path = line[6:] if line.startswith("+++ b/") else line[4:]; continue
        if line.startswith("+") and not line.startswith("+++"):
            scan_text(label, line[1:], {"commit": commit, "path": path or "(message)"})
        elif path is None and commit:
            scan_text(label, line, {"commit": commit, "path": "(commit message)"})
    p.wait()
    ids = subprocess.run(["git", "-C", repo, "log", "--all", "--format=%ae%n%ce"], capture_output=True, text=True).stdout.split()
    for e in sorted(set(ids)):
        emit(label, "commit-identity-email", e, {"commit": "(metadata)", "path": "(author/committer)"})

def scan_github_text(label, repo):
    def gh(args):
        r = subprocess.run(["gh"] + args, capture_output=True, text=True, encoding="utf-8", errors="replace")
        return r.stdout
    prs = json.loads(gh(["pr", "list", "-R", repo, "--state", "all", "--limit", "500", "--json", "number,title,body"]) or "[]")
    for pr in prs:
        scan_text(label, (pr.get("title") or "") + "\n" + (pr.get("body") or ""), {"commit": f"PR#{pr['number']}", "path": "(PR body)"})
    issues = json.loads(gh(["issue", "list", "-R", repo, "--state", "all", "--limit", "500", "--json", "number,title,body"]) or "[]")
    for it in issues:
        scan_text(label, (it.get("title") or "") + "\n" + (it.get("body") or ""), {"commit": f"issue#{it['number']}", "path": "(issue body)"})
    n = 0
    for ep in ("issues/comments", "pulls/comments"):
        out = gh(["api", f"repos/{repo}/{ep}", "--paginate", "--jq", ".[] | {id: .id, body: .body, url: .html_url}"])
        for line in out.splitlines():
            try:
                c = json.loads(line)
            except ValueError:
                continue
            n += 1
            scan_text(label, c.get("body") or "", {"commit": f"comment {c.get('id')}", "path": f"({ep})"})
    print(json.dumps({"summary": True, "src": label, "prs": len(prs), "issues": len(issues), "comments": n}))

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    label, kind, target = sys.argv[1:4]
    if kind == "git":
        scan_git(label, target)
    else:
        scan_github_text(label, target)
