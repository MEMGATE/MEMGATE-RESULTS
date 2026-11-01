# CCL-4C dev note: the retrain reference on one of CCL-4R's worlds (exploration)

**Status: FROZEN on 27 October 2026, 22:04 IST, before the run is packed.** It covers one exploratory run. CCL-4C's own preregistration is drafted separately and freezes after this run, before any CCL-4C world is packed.

## Why
CCL-4R (`docs/CCL4R-RESULT-7B-AZURE-2026-10-27.md`) left ability 4 NOT SHOWN: against the untouched model, what remained of the corrected errors was +0.217 [−0.026, +0.468] nats per token, above the margin +0.33 at its upper bound. By CCL-4's design each wrong holder is a person of the world, often one the learner is truthfully taught about, so the untouched model is not the reference "as if never learned" names. The standard reference for removal is the same learner trained on the same stream without the removed rows: a learner that never learned them. CCL-4C tests removal against it.

## What runs
- **World 9704,** CCL-4R's first world. CCL-4R is complete and its result is final; nothing here changes it.
- **The retrain build** (`cl/ccl4c.py pack … --variant retrain`): CCL-4R's payload of the world (`ece1121c…`, rebuilt and checked by its hash) with no removal and without the rows the removal takes away, in every session. Left out are every training row, rehearsal row and practice check that names a wrong holder together with the office's place (`clx.forget`'s own rule, with the removal plan's marks). The questions and the corrected-error items are the payload's own.
- **SYSTEM2 alone, and the untouched model,** with CCL-4's frozen GPU kernel in Colab's layout, on Azure's serverless A100.
- **Compared with CCL-4R's own run of the world** (`runs/ccl4r-7b-azure/w9704`), item by item.

Code SHA-256 (CCL-4's GPU runner, `clx.code_hash()`): Code SHA-256: `f2a25824cacd9cae7155e457139de4859bd5b68ce63b037182e62c1f1cc66395`

Code SHA-256 (CCL-4C packer and analysis, `ccl4c.code_hash()`): Code SHA-256: `e769938868cd2352e0b99fb94ff5df0720f8c1b4156972734bbf5b186e04e357`

Pack: `PYTHONHASHSEED=0 python cl/ccl4c.py pack 9704:main runs/ccl4c-dev-7b/w9704-retrain --variant retrain --prereg docs/CCL4C-DEV-NOTE-2026-10-27.md`

## What it is for
1. That the retrain build runs end to end with the frozen kernel.
2. How much the two runs differ, item by item, on CCL-4's measure. This noise sets how many fresh worlds CCL-4C needs: 4, 6 or 8, the fewest for which, with no true difference, the expected upper bound is at most two-thirds of the margin.
3. Whether CCL-4C is worth running at all. If the errors run sits clearly above the retrain run on this world, the test is not run, and this is reported.

## Status of its numbers
Exploration. They are reported as exploration and never as a test result. CCL-4C's test runs on fresh worlds of the main pool, under its own frozen preregistration.

## Earlier draft
A first version of this note (22:03, never committed, never run) used a different reference: the same world built without the errors, so the registry reported only the truth. A check of that build before any run showed that it changes far more than the removed rows: the learner hears the right holders from session 1, and every later session's rows differ by about 80 to 190. The retrain reference differs from the errors run only by the removed rows, which is what "as if never learned" asks.
