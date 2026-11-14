# Integrity is not completeness: a log demo

v3, 14 November 2026. CC BY 4.0. StS Forensics Ltd. Teaching toy: one writer, one witness, no signatures. Not a product, not evidence, not advice. Draft for discussion.

Live page: https://stsforensics.github.io/completeness-demo/ (also in French, German, Spanish, Japanese and three Chinese variants; machine translations, the English page prevails).

Integrity: is each entry still exactly as it was fingerprinted?
Completeness: is anything that should be there missing, for the scope the operator declared? Three tests in order: no gap inside the log; agreement with a witness checkpoint (entry count and head hash); agreement with records held by outside parties. The result is FAIL, HOLD (the evidence supplied cannot settle it) or NO GAP FOUND, which is never proof that nothing is missing.

Run the same twelve scenarios in a terminal (Python 3, standard library only):

    python3 gap_demo.py
    python3 gap_demo.py --json

The verdicts match the web page.

## Tell us what you think (one minute)

Open the form: https://github.com/StSForensics/completeness-demo/issues/new/choose

It asks five things, and you can skip any you cannot answer:
1. Which scenario (1 to 12), or "the whole page".
2. What did you expect to see?
3. What did you see?
4. Was the wording clear: yes, partly or no.
5. What wording would you use instead?

Found a translation mistake? Use the "Translation" form: the language page, the sentence, and a better one. The English page prevails, and the translations are machine translations that a human has not reviewed.

Prefer email? Write to comments@sts-forensics.com with the subject "Completeness demo". Email comments are copied to the public log (the Issues page of this repository) only with your permission.

## What we do with it

We reply in the issue, say whether we will change the page, the scenario or nothing, and say why. We note changes with their date in the page footer. We do not publish your name or organisation without your yes.

## Related: the draft tests behind it

This demo is a teaching toy for one idea. If you want to test the matching draft tests, see https://github.com/StSForensics/o4m-record-tests (the Record Tests, with a 15-minute way to test them with any chatbot).
