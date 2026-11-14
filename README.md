# Integrity is not completeness: a log demo

v3, 14 November 2026. CC BY 4.0. StS Forensics Ltd. Teaching toy: one writer, one witness, no signatures. Not a product, not evidence, not advice. Draft for discussion.

Live page: https://stsforensics.github.io/completeness-demo/ (also in French, German, Spanish, Japanese and three Chinese variants; machine translations, the English page prevails).

Integrity: is each entry still exactly as it was fingerprinted?
Completeness: is anything that should be there missing, for the scope the operator declared? Three tests in order: no gap inside the log; agreement with a witness checkpoint (entry count and head hash); agreement with records held by outside parties. The result is FAIL, HOLD (the evidence supplied cannot settle it) or NO GAP FOUND, which is never proof that nothing is missing.

Run the same twelve scenarios in a terminal (Python 3, standard library only):

    python3 gap_demo.py
    python3 gap_demo.py --json

The verdicts match the web page.
