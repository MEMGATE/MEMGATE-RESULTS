# CCL-4C result, 7B: removal as if never learned, against the learner that never learned the errors

**Written:** 28 October 2026, 07:28 IST. **Preregistration:** `docs/CCL4C-PREREG-2026-10-27.md` (frozen 27 October, 23:37 IST; CCL-4's GPU runner `f2a25824cacd…`, CCL-4C packer and analysis `e769938868cd…`, CCL-4's analysis `cl/ccl4.py` `525e21ff010b…`). **Dev note:** `docs/CCL4C-DEV-NOTE-2026-10-27.md`. **Machine summary:** `runs/ccl4c-main-7b/ccl4c-report.json` (`python cl/ccl4c.py report runs/ccl4c-main-7b/ccl4c-report.json runs/ccl4c-main-7b/w9714-errors:runs/ccl4c-main-7b/w9714-retrain runs/ccl4c-main-7b/w9715-errors:runs/ccl4c-main-7b/w9715-retrain runs/ccl4c-main-7b/w9716-errors:runs/ccl4c-main-7b/w9716-retrain runs/ccl4c-main-7b/w9717-errors:runs/ccl4c-main-7b/w9717-retrain`, exactly as preregistered).

## What ran
Qwen2.5-7B-Instruct (revision `a09a35458c70…`) in 16 bits on Azure's serverless NVIDIA A100 80 GB, one run per job, with CCL-4's frozen GPU runner in Colab's layout. Four fresh worlds of the main pool, 9714, 9715, 9716 and 9717, with 40, 40, 35 and 40 registry errors believed in session 1 and corrected in session 4 (155 in all); twelve sessions. Each world ran twice:
- **ERRORS:** CCL-4R's payload exactly; SYSTEM2, then NAIVE, and the untouched model. SYSTEM2 learns the errors, then removes them when the registry corrects them.
- **RETRAIN:** the same payload with no removal and without every row, rehearsal row and practice check the removal takes away, in every session; SYSTEM2 alone, and the untouched model. It never learns the errors.

The eight runs ran from 28 October 00:26 to 07:23 IST.

**Validity:** all four worlds valid. In both runs of every world every arm finished its twelve sessions, the untouched model answered every question and named the current holder of 0% of changed offices, and the lie scores exist for every arm. The removal ran in session 4 in every ERRORS run (110 to 138 rows left out) and never in a RETRAIN run. The untouched model's scores were identical in the two runs of every world. All four worlds are pooled (155 corrected errors).

## Verdicts (paired bootstrap over items within each world, 10,000 resamples, seed 12345, 95% intervals)
| H | Ability | Comparison | Estimate [95% CI] | Rule | Verdict |
| --- | --- | --- | --- | --- | --- |
| H12 | 4 | Corrected error inside the model (nats per token), SYSTEM2 − NAIVE, ERRORS runs | −1.659 [−1.896, −1.424] | upper < 0 | **WIN** |
| H12c | 4 | The same measure, SYSTEM2 in the ERRORS run (learned, then removed) − SYSTEM2 in the RETRAIN run (never learned) | +0.135 [−0.045, +0.314] | upper < +0.33 | **NON-INFERIOR** |

**Ability 4 (removal as if never learned): PASSED.** Both rules are met. After the removal, what remained of the corrected errors inside the model was within the preregistered margin of what remains in the same learner retrained without the removed rows, and far below naive retraining.

## Against the predictions
Predicted: H12 WIN (held), H12c NON-INFERIOR (held), ability 4 PASSED more likely than not (held). The upper bound of H12c was expected near +0.2; it was +0.314, inside the margin of +0.33 but with less room than predicted.

## Reported, not judged
- **Against the untouched model:** ERRORS − untouched +0.091 [−0.124, +0.315]; RETRAIN − untouched −0.044 [−0.292, +0.211].
- **CCL-4's other hypotheses on the ERRORS runs** (a replication, computed by CCL-4's frozen analysis):

| H | Ability | Comparison | Estimate [95% CI] | CCL-4's rule reached |
| --- | --- | --- | --- | --- |
| H1 | 2 | Attacker values answered, SYSTEM2 − NAIVE | −9.51 [−12.50, −6.79] | WIN |
| H2 | 1 | Current holders, SYSTEM2 − NAIVE | +1.60 [−0.53, +3.74] | NON-INFERIOR |
| H11 | 1 | Current holders, SYSTEM2 − untouched | +98.93 [+97.33, +100.0] | WIN |
| H3 | 3 | Offices told by session 4 and unchanged since, SYSTEM2 − NAIVE | 0.00 [0.00, 0.00] | NON-INFERIOR |
| H10 | 3 | Never-streamed offices, SYSTEM2 − untouched | 0.00 [0.00, 0.00] | NON-INFERIOR |
| H12b | 4 | Corrected error inside the model, SYSTEM2 − untouched | +0.091 [−0.124, +0.315] | NON-INFERIOR |
| H5 | 5 | Dated questions, SYSTEM2 − NAIVE | +18.28 [+14.74, +21.82] | WIN |
| H6 | 6 | Rewrites that pass, SYSTEM2 − NAIVE | +37.50 [+27.68, +47.32] | WIN |
| H7 | 7 | What follows from a change, SYSTEM2 − NAIVE | +48.27 [+45.20, +51.34] | WIN |
| H13 | 8 | New items missed at the first check, sessions 1–4 − 9–12, within kinds | +0.11 [−1.98, +2.27] | not shown |
| H8 | 9 | GSM8K, SYSTEM2 − untouched | 0.00 [0.00, 0.00] | NON-INFERIOR |
| H9 | 9 | MMLU, SYSTEM2 − untouched | 0.00 [0.00, 0.00] | NON-INFERIOR |

Every one of CCL-4's verdicts was reached again except H13 (ability 8), not shown on these worlds, where CCL-4 and CCL-4R had shown it (+4.63 and +2.51).

## Per world (mean gap, nats per token: the model's preference for the corrected wrong holder over strangers)
| World | Errors | ERRORS run, SYSTEM2 | RETRAIN run, SYSTEM2 | Untouched | ERRORS − RETRAIN |
| --- | --- | --- | --- | --- | --- |
| 9714 | 40 | −0.091 | −0.176 | −0.141 | +0.085 |
| 9715 | 40 | +0.390 | +0.245 | +0.186 | +0.145 |
| 9716 | 35 | +0.344 | +0.323 | +0.538 | +0.021 |
| 9717 | 40 | +0.897 | +0.620 | +0.627 | +0.277 |

## What this result supports
- Removing corrected errors leaves the learner, within the preregistered margin, where retraining without the removed rows would leave it: +0.135 nats per token [−0.045, +0.314] against a margin of +0.33, on four fresh worlds at 7B. This is the standard test of exact removal.
- Removal again left far less of a corrected error inside the model than naive retraining did (−1.659, a win in every test so far).
- With CCL-4R's eleven, every one of the twelve abilities has now been shown in a preregistered test at 7B: abilities 1–3 and 5–9 in CCL-4 and CCL-4R, ability 4 here, abilities 10–12 by the design.
- CCL-4R's verdict stands as it was: against the untouched model, ability 4 was NOT SHOWN there (+0.217 [−0.026, +0.468]). On these four worlds the same comparison, reported and not judged, came out within the margin (+0.091 [−0.124, +0.315]).
