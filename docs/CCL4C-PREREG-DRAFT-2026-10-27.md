# CCL-4C preregistration (draft): removal as if never learned, against the learner that never learned the errors (7B)

**Status: DRAFT, written 27 October 2026, 22:06 IST. Not frozen.** It freezes after the dev run of `docs/CCL4C-DEV-NOTE-2026-10-27.md` (the retrain build of CCL-4R's world 9704), which sets the number of worlds, and before any CCL-4C world is packed. It belongs to item 1 of the package's fixed list (ability 4, the twelfth of twelve).

## Why
CCL-4R (`docs/CCL4R-RESULT-7B-AZURE-2026-10-27.md`) left ability 4 NOT SHOWN at 7B for the second time. Removal beat naive retraining (H12, −1.746 [−1.999, −1.501]), but against the untouched model what remained of the corrected errors was +0.217 [−0.026, +0.468] nats per token, above the margin +0.33 at its upper bound.

The untouched model is not the reference "as if never learned" names. By CCL-4's design each wrong holder is a person of the world (a holder of the same post in another of its offices), and the learner is often taught that person's true facts. A model that knows a person can prefer them over strangers without any trace of an error. After the fact, CCL-4R's difference sat where the learner was taught the wrong holder's true facts (+0.325 over 126 errors), and none was seen where it was not (−0.182 over 34).

The standard reference for removal is retraining without the removed data: the same learner, trained on the same stream without the removed rows, which never learned them. CCL-4C measures removal against it.

## The system under test
SYSTEM2, CCL-4's learner, unchanged, with CCL-4's frozen GPU runner in Colab's layout (`colab_pack.colab_kernel("7b", 4)`, `a5567bf0…`).
- **Its removal:** when the registry corrects errors, the learner rolls back to its copy from before the first of them was learned. It trains the sessions since again without the rows that name a wrong holder together with the office's place, and never trains such rows again (`clx.undo_replay`, `clx.forget`).

Code SHA-256 (CCL-4's GPU runner, `clx.code_hash()`): Code SHA-256: `f2a25824cacd9cae7155e457139de4859bd5b68ce63b037182e62c1f1cc66395`

Code SHA-256 (CCL-4C packer and analysis, `ccl4c.code_hash()`): Code SHA-256: `TO BE FILLED AT FREEZE`

Analysis: `cl/ccl4c.py report`. It uses CCL-4's measure, CCL-4's frozen `cl/ccl4.py` (`525e21ff010b…`) for its bootstrap of real-valued gaps and for H12, and `ccl1`'s resampling settings.

## The two runs of each world
- **ERRORS:** CCL-4R's payload exactly (40 registry errors believed in session 1 and corrected in session 4, `--wide`, share 1, 12 sessions). SYSTEM2, then NAIVE, and the untouched model.
- **RETRAIN:** the same payload with no removal, and without every training row, rehearsal row and practice check that the removal takes away, in every session (`clx.forget`'s own rule, with the removal plan's marks). SYSTEM2 alone, and the untouched model. It never learns the errors. Everything else is the ERRORS payload: the stream otherwise, the questions and the corrected-error items.

## Design
- **Worlds:** N fresh worlds of the main pool, from 9714 (never generated, inspected or run). N is 4, 6 or 8, set by the dev run (below).
- **Packs:** `PYTHONHASHSEED=0 python cl/ccl4c.py pack 97XX:main runs/ccl4c-main-7b/w97XX-errors --variant errors --prereg docs/CCL4C-PREREG-2026-10-2X.md`, and the same with `--variant retrain` into `w97XX-retrain`.
- **Machine:** Azure's serverless A100 80 GB, one run per job (`cl/aca_run.py`).
- **Model:** Qwen2.5-7B-Instruct, revision `a09a35458c70…`, 16 bits.

## Hypotheses
All after session 12, the worlds pooled. Each uses a paired bootstrap over items within each world: 10,000 resamples, seed 12345, 95% percentile intervals.

| H | Ability | Comparison | Rule |
| --- | --- | --- | --- |
| H12 | 4 | What remains of a corrected error inside the model (CCL-4's measure, nats per token), SYSTEM2 − NAIVE, in the ERRORS runs | WIN if the upper bound is below 0 |
| H12c | 4 | The same measure, SYSTEM2 in the ERRORS run (errors learned, then removed) − SYSTEM2 in the RETRAIN run (never learned), item by item within each world | NON-INFERIOR if the upper bound is below +0.33 |

**Ability 4 (removal as if never learned)** is PASSED if both meet their rules, FAILED if either lies wholly on the wrong side, and NOT SHOWN otherwise.

**Reported, not judged:**
- SYSTEM2 − untouched in the ERRORS runs (CCL-4R's H12b comparison) and RETRAIN − untouched;
- CCL-4's other hypotheses on the ERRORS runs, as a replication;
- how far the two runs' untouched answers agree.

## The dev run and the number of worlds
- **The dev run:** the RETRAIN build of CCL-4R's world 9704, set against CCL-4R's own run of that world (`docs/CCL4C-DEV-NOTE-2026-10-27.md`). Its numbers are exploration.
- **The rule for N:** sigma is the standard deviation of the dev run's per-item differences (ERRORS − RETRAIN). N is the fewest of 4, 6 and 8 with 1.96 × sigma / √(40 × N) at most 0.22, two-thirds of the margin.
- **The dev run's numbers:** TO BE FILLED AT FREEZE.

## Predictions
TO BE FILLED AT FREEZE.

## Analysis
`python cl/ccl4c.py report runs/ccl4c-main-7b/ccl4c-report.json runs/ccl4c-main-7b/w9714-errors:runs/ccl4c-main-7b/w9714-retrain …`, one pair per world.

## Validity
A world is valid if, in both runs:
- every arm finished its 12 sessions;
- the untouched model answered every question and named the current holder of at most 10% of changed offices;
- the removal ran in session 4 in the ERRORS run and never in the RETRAIN run;
- the lie scores exist for every arm.

A run stopped by the machine without output is rerun once with the same payload, in a new folder.

## Declared
- The reference was chosen after CCL-4R's result, which an after-the-fact split pointed to. The measure, the margin and the bootstrap are CCL-4's; the worlds are fresh.
- CCL-4R's verdict stands as it is: against the untouched model, ability 4 was NOT SHOWN.
