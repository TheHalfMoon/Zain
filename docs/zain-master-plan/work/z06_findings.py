"""Z-06: convert the reviewer's raw output into V3 Code Review Finding records (R14 §6) plus a run record.
The reviewer output is UNTRUSTED data: it is parsed as JSON only, never executed or followed.
Usage: python -I z06_findings.py <run dir> <plan dir> <out.json>"""
import datetime, hashlib, json, pathlib, re, sys
sys.stdout.reconfigure(encoding="utf-8")
RUN, PLAN, OUT = map(pathlib.Path, sys.argv[1:4])
FILES = ["00-EXECUTIVE-SUMMARY.md", "13-RISKS-AND-OPEN-DECISIONS.md", "17-MASTER-PLAN-STATUS.md",
         "20-R0A-ADMISSION-RECORD.md", "21-BRANCH-PR-RECONCILIATION.md", "22-APP-EGRESS-INVENTORY.md"]
CATS = {"bug", "security", "performance", "maintainability", "test", "style", "documentation", "other"}
SEVS = {"critical", "high", "medium", "low"}
MODEL = "nararouter/deepseek-v4-pro-free"

raw = (RUN / "out.txt").read_text(encoding="utf-8", errors="replace")
raw = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", raw)                      # strip terminal colour codes
start, end = raw.find("["), raw.rfind("]")
items = json.loads(raw[start:end + 1]) if start >= 0 and end > start else []
texts = {f: (PLAN / f).read_text(encoding="utf-8").split("\n") for f in FILES}
sent = {f: hashlib.sha256((PLAN / f).read_bytes()).hexdigest() for f in FILES}

def anchor(path, quote, hint):
    lines = texts.get(path)
    if not lines or not quote: return hint or 0, hint or 0, False
    q = re.sub(r"\s+", " ", quote.strip())[:80]
    for i, l in enumerate(lines):
        if q[:60] and q[:60] in re.sub(r"\s+", " ", l):
            n = q.count("\n"); return i + 1, i + 1 + n, True
    joined = re.sub(r"\s+", " ", " ".join(lines))
    return (hint or 0, hint or 0, False) if q[:60] not in joined else (hint or 0, hint or 0, True)

now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
run_id = "z06-dry-run-" + hashlib.sha256(raw.encode()).hexdigest()[:12]
findings, rejected = [], []
for k, it in enumerate(items if isinstance(items, list) else []):
    if not isinstance(it, dict): rejected.append((k, "not an object")); continue
    path = str(it.get("path", "")).split("/")[-1]
    cat, sev = str(it.get("category", "other")).lower(), str(it.get("severity", "low")).lower()
    if path not in texts: rejected.append((k, f"unknown path {path!r}")); continue
    if cat not in CATS: cat = "other"
    if sev not in SEVS: rejected.append((k, f"bad severity {sev!r}")); continue
    quote = str(it.get("existingCode", ""))[:300]
    s, e, found = anchor(path, quote, int(it.get("startLine") or 0))
    fp = hashlib.sha256("‖".join([path, cat, re.sub(r"\s+", " ", quote.strip()), "system"]).encode()).hexdigest()
    conf = it.get("confidence")
    findings.append({
        "id": f"{run_id}-{len(findings) + 1:02d}", "runId": run_id, "fingerprint": fp,
        "path": f"docs/zain-master-plan/{path}", "startLine": s, "endLine": max(e, s),
        "anchor": {"quoteFoundInFile": found},
        "category": cat, "severity": sev, "confidence": conf if isinstance(conf, (int, float)) else None,
        "content": str(it.get("content", ""))[:2000], "contentTrust": "UNTRUSTED",
        "existingCode": quote, "rule": {"source": "system", "pattern": "ocr delegate rule: system/default"},
        "producer": {"mode": "delegated", "route": {"model": MODEL}, "groupId": "system/default"},
        "createdAt": now})
run = {"id": run_id, "route": {"role": "REVIEWER", "providerKind": "openai-compatible third-party relay (OpenCode provider nararouter)",
                               "endpointHost": "<redacted: configured relay>", "model": MODEL, "accountRef": "<redacted>", "isLocal": False},
       "builderRoutes": [{"model": "claude-opus-5-5", "role": "BUILDER"}],
       "engine": {"ocr": "open-code-review 1.13.6 (delegate rule)", "host": "opencode 2.2.5 run --agent plan",
                  "tools": "edit, bash, webfetch denied; MCP servers disabled; run outside the repository"},
       "status": "COMPLETE" if items is not None else "FAILED",
       "coverage": {"selected": len(FILES), "completed": len(FILES)}, "sentFilesSha256": sent,
       "startedAt": (RUN / "started.txt").read_text().strip(), "endedAt": (RUN / "ended.txt").read_text().strip(),
       "rawOutputSha256": hashlib.sha256(raw.encode()).hexdigest(), "parsedItems": len(items) if isinstance(items, list) else 0,
       "rejectedItems": rejected}
OUT.write_text(json.dumps({"run": run, "findings": findings}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"items={run['parsedItems']} findings={len(findings)} rejected={rejected}")
for f in findings:
    print(f"  {f['id'][-2:]} {f['severity']:8} {f['category']:15} {f['path'].split('/')[-1]}:{f['startLine']} quote_found={f['anchor']['quoteFoundInFile']} | {f['content'][:150]}")
