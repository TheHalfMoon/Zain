"""Targeted triage. Prints SHAPES only (rule, location, masked prefix, length, charset), never full values."""
import json, re, subprocess, sys, math, hashlib
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".")
import z03_scan as S
W = sys.argv[1]
SECRET = {"aws-access-key", "github-token", "openai-key", "anthropic-key", "google-api-key", "slack-token", "stripe-live",
          "huggingface-token", "npm-token", "private-key-block", "jwt", "azure-account-key", "generic-secret-assignment"}

def entropy(s):
    if not s: return 0.0
    from collections import Counter
    c = Counter(s); n = len(s)
    return -sum(v / n * math.log2(v / n) for v in c.values())

def mask(v):
    core = re.sub(r"^.*?[:=]\s*['\"]", "", v).strip("'\"")
    return f"{core[:4]}… len={len(core)} entropy={entropy(core):.2f}"

def git_secret_hits(label, repo):
    p = subprocess.Popen(["git", "-C", repo, "log", "--all", "-p", "-U0", "--no-color", "--no-renames", "--format=@@COMMIT %H"], stdout=subprocess.PIPE)
    commit = path = None
    for raw in p.stdout:
        line = raw.decode("utf-8", "replace").rstrip("\n")
        if line.startswith("@@COMMIT "): commit = line[9:21]; path = None; continue
        if line.startswith("+++ "): path = line[6:] if line.startswith("+++ b/") else line[4:]; continue
        if line.startswith("+") and not line.startswith("+++"):
            for name, rx in S.RX:
                if name in SECRET:
                    for m in rx.finditer(line[1:]):
                        ctx = re.sub(re.escape(m.group(0)), "<MATCH>", line[1:])[:90]
                        print(f"{label} {name} {commit} {path} :: {mask(m.group(0))} :: ctx={ctx!r}")
    p.wait()

def identities(label, repo):
    ids = subprocess.run(["git", "-C", repo, "log", "--all", "--format=%ae"], capture_output=True, text=True).stdout.split()
    from collections import Counter
    for e, n in Counter(ids).most_common():
        dom = e.split("@")[-1]
        kind = "noreply/bot" if S.NOREPLY.search(e) or "[bot]" in e or "github.com" in dom else "PERSONAL-LOOKING"
        print(f"{label} identity fp={S.fp(e)} domain={dom} kind={kind} commits={n}")

def email_domains(label, repo):
    p = subprocess.run(["git", "-C", repo, "log", "--all", "-p", "-U0", "--no-color", "--format="], capture_output=True)
    text = p.stdout.decode("utf-8", "replace")
    seen = {}
    for m in S.RX[[n for n, _ in S.RX].index("email")][1].finditer(text):
        e = m.group(0)
        if S.NOREPLY.search(e): continue
        seen.setdefault(S.fp(e), e.split("@")[-1])
    for f, d in seen.items(): print(f"{label} email fp={f} domain={d}")

def users(label, repo):
    p = subprocess.run(["git", "-C", repo, "log", "--all", "-p", "-U0", "--no-color", "--format=@@C %h"], capture_output=True)
    text = p.stdout.decode("utf-8", "replace")
    seen = {}
    for m in re.finditer(r"(?i)(?:[A-Z]:\\\\?Users\\\\?|/Users/|/home/)([A-Za-z0-9._-]+)", text):
        u = m.group(1).lower()
        if u in S.GENERIC_USERS: continue
        seen[S.fp(u)] = u if S.fp(u) != "5b80c867ad42" else "<founder username>"
    for f, u in seen.items(): print(f"{label} user fp={f} name={u}")

def gh_private_key(repo, pr, comment_ids):
    body = subprocess.run(["gh", "pr", "view", str(pr), "-R", repo, "--json", "body", "--jq", ".body"], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    texts = [("PR#%d" % pr, body)]
    for cid in comment_ids:
        t = subprocess.run(["gh", "api", f"repos/{repo}/issues/comments/{cid}", "--jq", ".body"], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
        texts.append((f"comment {cid}", t))
    for where, t in texts:
        lines = t.splitlines()
        for i, l in enumerate(lines):
            if re.search(S.RULES[[n for n, _ in S.RULES].index("private-key-block")][1], l):
                nxt = lines[i + 1:i + 4]
                shapes = [f"len={len(x.strip())} b64={bool(re.fullmatch(r'[A-Za-z0-9+/=]{40,}', x.strip()))}" for x in nxt]
                has_end = any("END" in x and "PRIVATE KEY" in x for x in lines[i + 1:i + 60])
                ctx = re.sub(r"-----BEGIN[^-]*-----", "<HEADER>", l)[:100]
                print(f"GH {where} line {i}: ctx={ctx!r} next={shapes} END_within_60={has_end}")

if __name__ == "__main__":
    z, wp = f"{W}/zain", f"{W}/z03/wepld.git"
    for label, repo in (("zain", z), ("wepld", wp)):
        git_secret_hits(label, repo); identities(label, repo); email_domains(label, repo); users(label, repo)
    gh_private_key("TheHalfMoon/Zain", 105, [5374562050, 5376333435, 5376450241])
