#!/usr/bin/env python3
"""
gap_demo.py  (2026-11-14, v1, CC BY 4.0, StS Forensics Ltd, draft for discussion)

Shows, with the Python standard library only, the difference between:
  INTEGRITY    = nothing in the records I was given has been changed
  COMPLETENESS = nothing that should be there is missing

Six scenarios. Run:  python3 gap_demo.py        (prints a table)
                     python3 gap_demo.py --json (machine readable)

Teaching toy. Not a product, not evidence, not a test suite for any standard.
It uses a hash chain, a sequence number, a witness checkpoint held by someone
other than the operator, and a reconciliation against records the operator does
not control (for example a network or cloud provider's own log).
"""
import hashlib, json, sys, copy

def h(s): return hashlib.sha256(s.encode()).hexdigest()

def entry_hash(prev, seq, body):
    return h(f"{prev}|{seq}|{body}")

def build_log(bodies):
    log, prev = [], "0" * 64
    for i, b in enumerate(bodies, start=1):
        eh = entry_hash(prev, i, b)
        log.append({"seq": i, "body": b, "prev": prev, "hash": eh})
        prev = eh
    return log

# What the agent really did (ground truth, known only in this demo)
TRUTH = ["open_ticket 41", "read_customer 17", "send_refund 120.00",
         "email_customer 17", "delete_file tmp.csv", "close_ticket 41"]

# Records held by a party the operator does not control (e.g. the payment provider).
# It saw the refund and the email, nothing else.
OUTSIDE_RECORDS = ["send_refund 120.00", "email_customer 17"]

def checkpoint(log):
    """Witness (not the operator) holds the latest count and head hash."""
    return {"count": len(log), "head": log[-1]["hash"] if log else "0" * 64}

def integrity(log):
    prev = "0" * 64
    for i, e in enumerate(log, start=1):
        if e["seq"] != i: return False, f"sequence jumps at position {i} (found {e['seq']})"
        if e["prev"] != prev: return False, f"chain broken at seq {e['seq']}"
        if entry_hash(e["prev"], e["seq"], e["body"]) != e["hash"]:
            return False, f"entry {e['seq']} was altered"
        prev = e["hash"]
    return True, "chain and numbering consistent"

def completeness(log, witness, outside, declared_scope):
    notes = []
    ok = True
    if witness is None:
        notes.append("no witness checkpoint: cannot say if the tail was cut or the chain rebuilt")
        ok = None
    else:
        if len(log) < witness["count"]:
            return False, f"log has {len(log)} entries, witness saw {witness['count']}"
        if len(log) == witness["count"] and (not log or log[-1]["hash"] != witness["head"]):
            return False, "head hash differs from the witness checkpoint (chain rebuilt)"
    bodies = [e["body"] for e in log]
    if outside is None:
        notes.append("no outside records: cannot reconcile")
        if ok is True: ok = None
    else:
        missing = [r for r in outside if r not in bodies]
        if missing:
            return False, f"outside party recorded {missing} but the log does not"
    return ok, "; ".join(notes) if notes else "matches witness and outside records for the declared scope"

def verdict(v):
    return {True: "PASS", False: "FAIL", None: "UNKNOWN"}[v]

def scenarios():
    S = []
    clean = build_log(TRUTH)
    wit = checkpoint(clean)

    S.append(("1 Clean log", clean, wit, OUTSIDE_RECORDS))

    alt = copy.deepcopy(clean); alt[2]["body"] = "send_refund 12.00"
    S.append(("2 One entry altered", alt, wit, OUTSIDE_RECORDS))

    dele = copy.deepcopy(clean); del dele[3]
    S.append(("3 Middle entry deleted", dele, wit, OUTSIDE_RECORDS))

    trunc = copy.deepcopy(clean)[:4]
    S.append(("4 Tail cut off, no witness", trunc, None, None))
    S.append(("4b Tail cut off, witness kept count", trunc, wit, OUTSIDE_RECORDS))

    # Operator never wrote the risky action and rebuilds a perfect chain
    omit_bodies = [b for b in TRUTH if b != "delete_file tmp.csv"]
    omitted = build_log(omit_bodies)
    S.append(("5 Action never logged, no outside check", omitted, None, None))
    S.append(("5b Action never logged, witness only", omitted, checkpoint(omitted), None))
    S.append(("5c Action never logged, outside record has it", omitted, checkpoint(omitted), OUTSIDE_RECORDS + ["delete_file tmp.csv"]))
    return S

def run():
    rows = []
    for name, log, wit, outside in scenarios():
        i_ok, i_msg = integrity(log)
        c_ok, c_msg = completeness(log, wit, outside, TRUTH)
        rows.append({"scenario": name, "integrity": verdict(i_ok), "integrity_note": i_msg,
                     "completeness": verdict(c_ok), "completeness_note": c_msg})
    return rows

if __name__ == "__main__":
    rows = run()
    if "--json" in sys.argv:
        print(json.dumps(rows, indent=2)); sys.exit(0)
    for r in rows:
        print(f"{r['scenario']}")
        print(f"   integrity   : {r['integrity']:8} {r['integrity_note']}")
        print(f"   completeness: {r['completeness']:8} {r['completeness_note']}")
    print("\nPoint: scenarios 5 and 5b pass integrity and cannot show completeness."
          "\nOnly a record held by someone else (5c) exposes the missing action.")
