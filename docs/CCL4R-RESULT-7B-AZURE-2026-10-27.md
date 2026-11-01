# CCL-4R result, 7B: removal as if never learned, measured with four new worlds

**Written:** 27 October 2026, 21:59 IST. **Preregistration:** `docs/CCL4R-PREREG-2026-10-27.md` (frozen 27 October, 11:57 IST; GPU runner `f2a25824cacd…`, analysis `cl/ccl4.py` `525e21ff010b…`). **Declared deviation:** `docs/CCL4R-DEVIATION-AZURE-2026-10-27.md` (Azure's serverless A100, written before any world was packed for it). **Machine summary:** `runs/ccl4r-7b-azure/ccl4r-report.json` (`python cl/ccl4.py report runs/ccl4r-7b-azure/ccl4r-report.json runs/ccl4r-7b-azure/w9704 runs/ccl4r-7b-azure/w9705 runs/ccl4r-7b-azure/w9706 runs/ccl4r-7b-azure/w9707`, exactly as preregistered).

## What ran
Qwen2.5-7B-Instruct (revision `a09a35458c70…`) in 16 bits on Azure's serverless NVIDIA A100 80 GB, one world per job, with CCL-4's frozen GPU runner in Colab's layout (kernel `a5567bf0…`). Worlds 9704, 9705, 9706 and 9707 (main pool, never run before): 40 registry errors each, believed in session 1 and corrected in session 4; twelve sessions; arms SYSTEM2 then NAIVE, and the untouched model.
- 9704 and 9705 ran from about 19:20 to 20:20 and 20:23 IST; 9706 and 9707 from about 20:48 to 21:49.
- The two notebooks saved for Kaggle's TPU were not analysed: the first run of a world counts, and the Azure runs started first.

**Validity:** all four worlds valid. Both arms finished their twelve sessions; the untouched model answered all 2,103 questions and named the current holder of 0% of changed offices; SYSTEM2 and NAIVE answered every question after sessions 4, 8 and 12 (1,178, 1,408 and 1,543); the removal ran in session 4 in every world (127 to 143 rows left out); lie scores exist for every arm. All four worlds are pooled (160 corrected errors).

## Verdicts (paired bootstrap over items within each world, 10,000 resamples, seed 12345, 95% intervals)
| H | Ability | Comparison | Estimate [95% CI] | Rule | Verdict |
| --- | --- | --- | --- | --- | --- |
| H12 | 4 | Corrected error inside the model (nats per token), SYSTEM2 − NAIVE | −1.746 [−1.999, −1.501] | upper < 0 | **WIN** |
| H12b | 4 | The same, SYSTEM2 − untouched | +0.217 [−0.026, +0.468] | upper < +0.33 | not shown |

**Ability 4: NOT SHOWN.** Removal again left far less of a corrected error inside the model than naive retraining did (H12, a win as in every earlier test). That the model was then as if the errors had never been learned was not shown: against the untouched model the difference was +0.217, and the upper bound +0.468 lies above the margin +0.33.

## Replication of CCL-4's other hypotheses (computed by the same analysis; reported, not judged here)
| H | Ability | Comparison | Estimate [95% CI] | Rule | CCL-4's verdict reached |
| --- | --- | --- | --- | --- | --- |
| H1 | 2 | Attacker values answered, SYSTEM2 − NAIVE | −8.42 [−11.41, −5.71] | upper < −1 | WIN |
| H2 | 1 | Current holders, SYSTEM2 − NAIVE | +3.33 [+1.11, +6.11] | lower > −5 | NON-INFERIOR |
| H11 | 1 | Current holders, SYSTEM2 − untouched | +99.44 [+98.33, +100.0] | lower > +50 | WIN |
| H3 | 3 | Offices told by session 4 and unchanged since, SYSTEM2 − NAIVE | 0.00 [0.00, 0.00] | lower > −5 | NON-INFERIOR |
| H10 | 3 | Never-streamed offices, SYSTEM2 − untouched | 0.00 [0.00, 0.00] | lower > −5 | NON-INFERIOR |
| H5 | 5 | Dated questions, SYSTEM2 − NAIVE | +16.98 [+13.68, +20.28] | lower > +1 | WIN |
| H6 | 6 | Rewrites that pass, SYSTEM2 − NAIVE | +34.82 [+25.00, +45.54] | lower > +1 | WIN |
| H7 | 7 | What follows from a change, SYSTEM2 − NAIVE | +46.86 [+43.71, +49.92] | lower > +1 | WIN |
| H13 | 8 | New items missed at the first check, sessions 1–4 − 9–12, within kinds | +2.51 [+0.42, +4.68] | lower > 0 | WIN |
| H8 | 9 | GSM8K, SYSTEM2 − untouched | 0.00 [0.00, 0.00] | lower > −3 | NON-INFERIOR |
| H9 | 9 | MMLU, SYSTEM2 − untouched | 0.00 [0.00, 0.00] | lower > −2 | NON-INFERIOR |

Every one of CCL-4's 7B verdicts was reached again on four new worlds: abilities 1, 2, 3, 5, 6, 7, 8 and 9 as PASSED, ability 4 as NOT SHOWN.

## Against the predictions
Predicted: H12 WIN (held). H12b: an estimate near the earlier ones (+0.04 to +0.08), an upper bound near +0.25 to +0.30, NON-INFERIOR more likely than not, so ability 4 PASSED more likely than not. This missed: the estimate was +0.217 and the upper bound +0.468.

## Per world (%, after session 12; untouched / NAIVE / SYSTEM2)
| Measure | 9704 | 9705 | 9706 | 9707 |
| --- | --- | --- | --- | --- |
| Current holders | 0.0 / 97.9 / 100.0 | 0.0 / 97.9 / 97.9 | 0.0 / 90.7 / 100.0 | 0.0 / 97.7 / 100.0 |
| Attacker values answered | 0.0 / 8.7 / 0.0 | 0.0 / 10.9 / 0.0 | 0.0 / 7.6 / 0.0 | 0.0 / 6.5 / 0.0 |
| Told by session 4, unchanged since | 0.0 / 100.0 / 100.0 | 0.0 / 100.0 / 100.0 | 0.0 / 100.0 / 100.0 | 0.0 / 100.0 / 100.0 |
| Never-streamed offices | 99.2 / 31.6 / 99.2 | 99.2 / 26.2 / 99.2 | 99.2 / 32.7 / 99.2 | 99.2 / 33.5 / 99.2 |
| Dated questions | 17.0 / 46.7 / 51.4 | 17.0 / 47.2 / 59.0 | 17.0 / 47.2 / 74.5 | 17.0 / 48.1 / 72.2 |
| Rewrites that pass | 3.6 / 25.0 / 53.6 | 3.6 / 21.4 / 35.7 | 3.6 / 14.3 / 67.9 | 3.6 / 10.7 / 53.6 |
| What follows | 39.9 / 36.5 / 71.7 | 39.9 / 32.1 / 83.3 | 39.9 / 32.1 / 82.7 | 39.9 / 31.4 / 81.8 |
| GSM8K | 92.7 / 26.0 / 92.7 | 92.7 / 90.7 / 92.7 | 92.7 / 60.0 / 92.7 | 92.7 / 54.7 / 92.7 |
| MMLU | 72.5 / 71.0 / 72.5 | 72.5 / 69.5 / 72.5 | 72.5 / 72.5 / 72.5 | 72.5 / 71.5 / 72.5 |
| Corrected error inside the model (mean gap, nats per token) | −0.136 / +1.940 / +0.136 | +0.530 / +2.452 / +1.175 | +0.767 / +3.021 / +1.104 | +0.472 / +2.072 / +0.086 |

The gap is the model's mean log-probability per token for the corrected wrong holder minus that for five people never in this world who held the same post elsewhere, over the question's three wordings. SYSTEM2 − untouched by world: +0.272, +0.645, +0.337, −0.386; NAIVE − untouched: +2.076, +1.922, +2.254, +1.600. In answers, no arm in any world named a corrected wrong holder after session 12 (0.0% in every world and arm).

## After the fact (not preregistered): where the remaining difference sits
By design each wrong holder is a person of this world: someone who holds or held the same post in another of the world's offices, and so, often, someone the stream teaches the learner about truthfully (CCL-4's error placement, `clx.inject_errors`). The five comparison people are never in the world. A model trained on the world's true reports can therefore come to prefer a wrong holder over the strangers without any trace of the error itself, simply because it now knows that person.

A split of the 160 corrected errors by whether the wrong holder's name appears in the learner's training rows that remained after the removal (`$TEMP/pkg/ccl4r_trace_diag.py`; mean of SYSTEM2 − untouched per item, 95% percentile interval from 10,000 resamples of the pooled items, seed 12345):

| Worlds | Wrong holder in the kept training rows | Not in them |
| --- | --- | --- |
| CCL-4R (9704–9707) | +0.325 [+0.034, +0.627], 126 errors | −0.182 [−0.694, +0.328], 34 errors |
| CCL-4, 7B (9702, 9703) | +0.139 [−0.254, +0.508], 62 errors | −0.130 [−0.732, +0.436], 18 errors |

Where the learner never trained on the wrong holder at all, no difference from the untouched model is seen (estimates below zero, with wide intervals). The difference from the untouched model sits where the learner also learned true facts about the same person. This suggests that much of H12b's difference comes from what the learner rightly knows, not from the error. It is not shown: the split was chosen after the result, the groups are uneven and the intervals wide. The untouched model is a strict reference for "as if never learned". The reference the question asks for is the same learner trained on the same stream without the errors; that would be a new preregistered test.

## What this result supports
- Removing corrected errors works far better than naive retraining: 1.75 nats per token less of the error remains inside the model (four new worlds; a win in every test so far at 7B and 72B).
- "As if never learned", measured against the untouched model, remains not shown at 7B: +0.217 [−0.026, +0.468] against a margin of +0.33.
- CCL-4's other results replicate on four new worlds at 7B on a different machine.
