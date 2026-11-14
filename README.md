# Integrity is not completeness: a six-scenario log demo

Draft v1, 2026-11-14. CC BY 4.0. StS Forensics Ltd. Teaching toy: not a product, not evidence, not a test suite for any standard.

Integrity means nothing in the records you were given has been changed.
Completeness means nothing that should be there is missing.
A hash chain gives you the first. It cannot give you the second on its own.

Run it (Python 3, standard library only):

    python3 gap_demo.py
    python3 gap_demo.py --json

Or open gap_demo.html in a browser (no server, no network, SHA-256 from the browser).

Scenarios: clean log; one entry altered; middle entry deleted; tail cut off (with and without a witness); action never logged (no outside check, witness only, outside record present).

What each extra party adds:
- Sequence numbers and chain: catch alteration and middle deletion.
- Witness checkpoint (count and head hash held by someone other than the operator): catches tail cut and whole-chain rebuild.
- Outside records (for example a payment or network provider's own log): the only thing that exposes an action that was never logged.

Limits: the outside records only cover what the outside party can see (the declared scope). A pass means "consistent with those sources", not "everything happened is recorded".
