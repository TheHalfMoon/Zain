# 20 — Governance Equivalence Plan (Astro H-10)

```text
STATUS = PROPOSED. Revises ADR-011 consequences and tasks G-03, G-05; adds G-08 (inventory).
RULE = the replacement checker may retire the v1–v72 successor chain only property by property: each baseline property
       and negative oracle is CARRIED (ported fixture fails the candidate in the new checker) or RETIRED by a signed
       founder co-sign with a risk record. Replaying accepted PRs is a non-regression check only (GV-19).
BASE = main @ 0a843a2c0913236d9c93b31abb0d54bbdb023f23 (169 scripts under .github/scripts/)
```

## 1. Why accepted-PR replay is insufficient

The last merged PRs are all permitted cases; a checker that accepts everything agrees with them. The baseline's value is in
its rejections (negative oracles), e.g. `wepld_s3_contracts_freeze_shortcut_v72_integrity.py` @0a843a2 L656–L790.

## 2. Property inventory (seed; G-08 completes it for all 169 scripts)

| Prop | Baseline property | Evidence @0a843a2 | Disposition (proposed) | New test |
|---|---|---|---|---|
| GP-01 | Exact authorized delta admitted through the executed enforcement path | v72 oracle 1 (L650–654) | CARRY | GV-19 (positive) |
| GP-02 | Host/OS API additions in frozen contract crates rejected ("prohibited runtime capability") | v72 oracle 2 (L656–666) | CARRY | GV-01 |
| GP-03 | Process/spawn capability rejected | v72 oracle 3 (L668–676) | CARRY | GV-02 |
| GP-04 | Network capability rejected | v72 oracle 4 (L678–686) | CARRY | GV-03 |
| GP-05 | Cargo manifest edits and Cargo.lock drift rejected | v72 oracles 5–6 (L688–708) | CARRY | GV-04 |
| GP-06 | Unauthorized and look-alike source paths rejected | v72 oracle 7 (L710–720) | CARRY | GV-05 |
| GP-07 | Mixed authorized + unauthorized non-contract delta rejected by routing and freeze hooks | v72 oracle 8 (L722–738) | CARRY | GV-06 |
| GP-08 | Exemption cannot be triggered by branch, ref, PR number, label, message, author, task (input surface = candidate tree + policy base only) | v72 oracle 9 (L740–754) | CARRY | GV-07 |
| GP-09 | Inherited frozen-protocol paths still fail closed, including drift smuggled inside an authorized tranche | v72 oracle 10 (L756–785) | CARRY | GV-08 |
| GP-10 | Checker logic comes from the trusted base; candidate copies are data | AGENTS.md trusted-bootstrap rule | CARRY | GV-11 |
| GP-11..GP-n | Properties of v1–v71 and auxiliary scripts | G-08 inventory | CARRY or RETIRE (signed) | GV-18 corpus |

Retirement record format: `{property, reason, risk, compensating control, co-sign tag}`; a RETIRE without a valid co-sign
(§3) fails GV-18.

## 3. Co-sign binding

A co-sign is an SSH-signed git tag created by the founder key listed in base `.github/allowed_signers`. Signed message:

```text
zain-cosign v1
repo=TheHalfMoon/Zain#1334408699
base=<base sha>  head=<head sha>  tree=<head tree sha>
paths=<sha256 of the sorted list of changed protected paths>
scope=<sha256 of the authorization text>
expires=<UTC date>
```

The checker (from base) verifies with `ssh-keygen -Y verify -n zain-cosign`, recomputes every field from the candidate,
and rejects any mismatch: other repository, base, head, tree, path set, expired, unknown key, label-only (GV-09, GV-10,
GV-12).

## 4. Required negative corpus (GV-01..GV-18)

Forbidden capabilities and dependency drift (GV-01..04), source-admission violations (GV-16), unauthorized and look-alike
paths (GV-05), mixed deltas (GV-06), metadata-triggered exemptions (GV-07), frozen-path transitions (GV-08), checker
self-modification in the candidate (GV-11), forged/replayed/label-only co-signs (GV-09, GV-10, GV-12), REVIEW_BLOCKED
conversion (GV-13), external-review trigger without egress record (GV-14), fork PR token/secrets under
`pull_request_target` (GV-15), missing Build Learning (GV-17), and every ported v1–v72 negative fixture (GV-18).

## 5. Sequencing

G-08 (inventory) → G-03 (checker designed against the inventory) → G-05 (port fixtures, run corpora, retire per
property). Old workflows stay active until G-05 completes; there is no window without a checker.
