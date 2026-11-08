import csv, re, sys
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8')
root=sys.argv[1]
T={r['id']:r for r in csv.DictReader(open(root+'/registry/zain-task-backlog.csv',encoding='utf-8'))}
E=list(csv.DictReader(open(root+'/registry/zain-dependency-edges.csv',encoding='utf-8')))
M=["M0","R0a","R0b","R0","R1","R2","R3","R4","R5","R6","R7","PD"]
def est(r):
    s=r['est_pw']
    if s=='MEASURE': return None
    m=re.fullmatch(r'([\d.]+)(?:[–-]([\d.]+))?',s); lo=float(m.group(1)); hi=float(m.group(2) or lo); return lo,hi
pre=defaultdict(set)
for e in E: pre[e['to']].add(e['from'])
cum=set()
print('| Milestone | New tasks (V3 / ZMP) | New effort pw (low–high) | Unmeasured | Cumulative tasks | Cumulative pw (low–high) | Critical path to exit, pw (low–high) |')
print('|---|---|---|---|---|---|---|')
clo=chi=0
for m in M:
    ids=[t for t,r in T.items() if r['milestone']==m]
    if not ids: continue
    lo=hi=0; un=0; v3=sum(1 for t in ids if T[t]['source']=='V3')
    for t in ids:
        x=est(T[t])
        if x is None: un+=1
        else: lo+=x[0]; hi+=x[1]
    if m!='PD':
        cum|=set(ids); clo+=lo; chi+=hi
    # critical path within cumulative set (longest path by est over prereq graph restricted to cum)
    S=cum if m!='PD' else set(ids)
    memo={}
    def lp(t,i):
        if (t,i) in memo: return memo[(t,i)]
        x=est(T[t]); w=0 if x is None else x[i]
        best=0
        for p in pre[t]:
            if p in S: best=max(best,lp(p,i))
        memo[(t,i)]=w+best; return memo[(t,i)]
    cpl=max(lp(t,0) for t in S); cph=max(lp(t,1) for t in S)
    print(f'| {m} | {len(ids)} ({v3} / {len(ids)-v3}) | {lo:.2f}–{hi:.2f} | {un} | {len(cum) if m!="PD" else "—"} | {clo:.2f}–{chi:.2f} | {cpl:.2f}–{cph:.2f} |')
# critical path chain to R0 exit (high)
S=set(t for t,r in T.items() if r['milestone'] in ("M0","R0a","R0b","R0"))
memo={}
def lp(t):
    if t in memo: return memo[t]
    x=est(T[t]); w=0 if x is None else x[1]
    best=(0,[])
    for p in pre[t]:
        if p in S:
            c=lp(p)
            if c[0]>best[0]: best=c
    memo[t]=(w+best[0],best[1]+[t]); return memo[t]
end=max(S,key=lambda t:lp(t)[0]); print('R0 critical chain (high):', ' → '.join(lp(end)[1]), f'= {lp(end)[0]:.2f} pw')
S=set(t for t,r in T.items() if r['milestone'] in ("M0","R0a")); memo={}
end=max(S,key=lambda t:lp(t)[0]); print('R0a critical chain (high):', ' → '.join(lp(end)[1]), f'= {lp(end)[0]:.2f} pw')
