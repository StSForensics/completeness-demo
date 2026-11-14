#!/usr/bin/env python3
"""
gap_demo.py  v3, 14 Nov 2026, CC BY 4.0, StS Forensics Ltd, draft for discussion.
Same twelve scenarios and the same verdicts as the web page
https://stsforensics.github.io/completeness-demo/  (Python standard library only).

Integrity    : is each entry still exactly as it was fingerprinted? PASS or FAIL.
Completeness : three tests in order:
   (a) no gap inside the log (numbering and links run unbroken)
   (b) the log agrees with a witness checkpoint (entry count and head hash)
   (c) the log agrees with records held by outside parties
 Result is FAIL, HOLD (the evidence supplied cannot settle it) or NO GAP FOUND.
 NO GAP FOUND is the best it can say. It is never proof that nothing is missing.

Teaching toy: one writer, one witness, no signatures. Not a product, not evidence, not advice.
Run:  python3 gap_demo.py        or   python3 gap_demo.py --json
"""
import hashlib, json, sys, copy

Z = "0" * 64
TRUTH = ["open_ticket 41", "read_customer 17", "send_refund 120.00",
         "email_customer 17", "delete_file tmp.csv", "close_ticket 41"]
OUT = ["send_refund 120.00", "email_customer 17"]

def H(s): return hashlib.sha256(s.encode()).hexdigest()

def build(bodies):
    log, prev = [], Z
    for i, b in enumerate(bodies, start=1):
        h = H(f"{prev}|{i}|{b}")
        log.append({"seq": i, "body": b, "prev": prev, "hash": h})
        prev = h
    return log

def checkpoint(log):
    return {"count": len(log), "head": log[-1]["hash"] if log else Z}

def integrity(log):
    for e in log:
        if H(f"{e['prev']}|{e['seq']}|{e['body']}") != e["hash"]:
            return "FAIL", f"entry {e['seq']} was altered"
    return "PASS", "each entry still matches its own fingerprint (a rebuilt log passes this too)"

def completeness(log, witness, outside):
    notes, ok = [], True
    prev = Z
    for i, e in enumerate(log, start=1):
        if e["seq"] != i:
            return "FAIL", f"numbering jumps at position {i} (found {e['seq']}): an entry is missing"
        if e["prev"] != prev:
            return "FAIL", f"entry {e['seq']} does not point to the one before it"
        prev = e["hash"]
    if witness is None:
        notes.append("no witness checkpoint: cannot say if the tail was cut or the chain rebuilt")
        ok = None
    else:
        if len(log) < witness["count"]:
            return "FAIL", f"log has {len(log)} entries, witness saw {witness['count']}"
        at = Z if witness["count"] == 0 else log[witness["count"] - 1]["hash"]
        if at != witness["head"]:
            return "FAIL", f"history up to entry {witness['count']} differs from the witness checkpoint (rewritten or chain rebuilt)"
    if outside is None:
        notes.append("no outside records: cannot reconcile")
        if ok is True: ok = None
    else:
        bodies = [e["body"] for e in log]
        missing = [r for r in outside if r not in bodies]
        if missing:
            return "FAIL", f"outside party recorded {', '.join(missing)} but the log has no matching entry"
    if ok is True:
        return "NO GAP FOUND", "no gap inside the log, and agreement with the witness checkpoint and the outside records. Anything none of them saw would still be invisible"
    return "HOLD", "; ".join(notes)

def scenarios():
    clean = build(TRUTH); w = checkpoint(clean); S = []
    S.append(("1 Clean log", clean, w, OUT))
    alt = copy.deepcopy(clean); alt[2]["body"] = "send_refund 12.00"
    S.append(("2 One entry altered", alt, w, OUT))
    altR = build([("send_refund 12.00" if x == "send_refund 120.00" else x) for x in TRUTH])
    S.append(("2b Entry altered, chain rebuilt, no witness", altR, None, None))
    S.append(("2c Entry altered, chain rebuilt, witness kept checkpoint", altR, w, OUT))
    dele = copy.deepcopy(clean); del dele[3]
    S.append(("3 Middle entry deleted", dele, w, OUT))
    delR = build([x for x in TRUTH if x != "email_customer 17"])
    S.append(("3b Middle entry deleted, chain rebuilt, witness kept count", delR, w, OUT))
    tr = clean[:4]
    S.append(("4 Tail cut off, no witness", tr, None, None))
    S.append(("4b Tail cut off, witness kept count", tr, w, OUT))
    om = build([x for x in TRUTH if x != "delete_file tmp.csv"])
    S.append(("5 Action never logged, no outside check", om, None, None))
    S.append(("5b Action never logged, witness only", om, checkpoint(om), None))
    S.append(("5c Action never logged, outside record has it", om, checkpoint(om), OUT + ["delete_file tmp.csv"]))
    grown = build(TRUTH + ["open_ticket 42"])
    S.append(("6 Log grew after the checkpoint (normal)", grown, w, OUT))
    return S

def run():
    rows = []
    for name, log, w, o in scenarios():
        i, im = integrity(log); c, cm = completeness(log, w, o)
        rows.append({"scenario": name, "integrity": i, "integrity_note": im,
                     "completeness": c, "completeness_note": cm})
    return rows

if __name__ == "__main__":
    rows = run()
    if "--json" in sys.argv:
        print(json.dumps(rows, indent=2)); sys.exit(0)
    for r in rows:
        print(r["scenario"])
        print(f"   integrity   : {r['integrity']:13} {r['integrity_note']}")
        print(f"   completeness: {r['completeness']:13} {r['completeness_note']}")
    print("\nPoint: scenarios 5 and 5b pass integrity and cannot show completeness. "
          "Only a record held by someone else (5c) exposes the missing action.")
