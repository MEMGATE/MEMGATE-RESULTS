# CCL-4R preregistration: removal as if never learned, measured with four new worlds (7B) (frozen)

**Status: FROZEN on 27 October 2026, 11:57 IST, before any of its worlds was generated or run.** CCL-4 (`docs/CCL4-PREREG-2026-10-26.md`) and its results are not changed by anything here; this is a new test, and its worlds are not pooled with CCL-4's.

## Why
Removal beat naive training in every test so far (H12: 7B −1.647, 72B −1.949, CCL-5's 72B −1.934, all wins), but "as if never learned" was not shown (H12b, against the untouched model: +0.079 [−0.257, +0.396] at 7B, +0.043 [−0.295, +0.379] and +0.057 [−0.279, +0.389] at 72B, against a margin of +0.33). The estimates sit well inside the margin; the intervals, from 80 corrected errors in two worlds, are too wide to show it. This test measures ability 4 with four new worlds (160 corrected errors).

## The system under test
SYSTEM2, CCL-4's learner, with CCL-4's frozen runners:
Code SHA-256 (GPU runner, `clx.code_hash()`): Code SHA-256: `f2a25824cacd9cae7155e457139de4859bd5b68ce63b037182e62c1f1cc66395`
Code SHA-256 (TPU runner, `clx_tpu.code_hash()`): Code SHA-256: `c4a96300559d8150dc7cb8ef3f49b9ce127499637591d7a116d42ffed015f435`
Analysis: `cl/ccl4.py` SHA-256 `525e21ff010b44e725aa292d1eb6f1f3a796788b51945aac6ba4a993479efd02`.

## Design
- Worlds 9704, 9705, 9706 and 9707 (main pool; never generated, inspected or run), with CCL-4's main-world options: 40 registry errors each, believed in session 1 and corrected in session 4; `--errors 40 --errors-at 0 --wide --share 1.0`; 12 sessions; evaluations after sessions 4, 8 and 12; payloads built with a fixed hash seed (`PYTHONHASHSEED=0`).
- Qwen2.5-7B-Instruct; arms SYSTEM2 then NAIVE, and the untouched model; one world per notebook.
- Machine: Kaggle's TPU v5e-8 (`cl/clx_tpu.py push … --model 7b --arms SYSTEM2,NAIVE --budget 8`, started by the account holder from Kaggle's website) or, from Kaggle's weekly reset on 31 October, Kaggle's two T4s (`cl/clx.py push … --model 7b --arms SYSTEM2,NAIVE`), whichever runs a world first; the machine of each world is recorded. On the TPU the model comes from Kaggle's model hub (`qwen-lm/qwen2.5/transformers/7b-instruct/1`), on the GPUs from Hugging Face (revision `a09a35458c70…`).

## Hypotheses (after session 12; the four worlds pooled; paired bootstrap over items within each world, 10,000 resamples, seed 12345, 95% percentile intervals; SYSTEM2 as routed by its scope rule)
| H | Ability | Comparison | Rule |
| --- | --- | --- | --- |
| H12 | 4 | What remains of a corrected error inside the model (CCL-4's measure, nats per token), SYSTEM2 − NAIVE | WIN if the upper bound is below 0 |
| H12b | 4 | The same, SYSTEM2 − untouched | NON-INFERIOR if the upper bound is below +0.33 |

Ability 4 is PASSED if both meet their rules, FAILED if either lies wholly on the wrong side, NOT SHOWN otherwise. CCL-4's other hypotheses are computed by the same analysis and reported as a replication, not judged here.

## Predictions
- H12: WIN (every earlier test).
- H12b: the estimate near the earlier ones (+0.04 to +0.08); with twice the errors the interval narrows by about a third, so its upper bound is expected near +0.25 to +0.30: NON-INFERIOR more likely than not (about two chances in three), so ability 4 PASSED more likely than not.

## Analysis
`python cl/ccl4.py report OUT.json RUN_DIR_9704 RUN_DIR_9705 RUN_DIR_9706 RUN_DIR_9707`.

## Validity
A world is valid as in CCL-4 (both arms finished their 12 sessions, the untouched model named the current holder of at most 10% of changed offices, the removal ran in session 4, lie scores exist for every arm). Worlds that have not run by 7 November are left out, and the analysis states how many worlds it pools.
