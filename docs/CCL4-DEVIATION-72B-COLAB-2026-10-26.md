# CCL-4: the 72B worlds run on a Colab GPU instead of Kaggle's TPU (declared deviation)

**Written 26 October 2026, 11:14 IST, before either 72B main world started.** The frozen preregistration (`docs/CCL4-PREREG-2026-10-26.md`, 09:47 IST) is not changed; this note says what differs in how its 72B part is run, and why.

## What changes
| | Frozen preregistration | This run |
| --- | --- | --- |
| Machine | Kaggle TPU v5e-8 | Google Colab G4: one NVIDIA RTX PRO 6000 Blackwell, 96 GB (the founder's Colab units) |
| Weights | Qwen2.5-72B-Instruct in 8 bits (int8, group scales) | Qwen2.5-72B-Instruct (revision `495f39366efe…`) in 4 bits (NF4, bitsandbytes), as the frozen GPU runner holds large models |
| Runner | TPU runner (`c4a96300559d…`) | frozen GPU runner (`f2a25824cacd…`), unchanged except where it reads its payload and writes its output (`cl/colab_pack.py`, `cl/colab_run.py`) |
| Arms | SYSTEM2, NAIVE, REPLAY, in that order, and the untouched model | the same |
| Worlds | 9702 and 9703, 40 registry errors each at session 1 | the same; payloads built as the preregistration says, with a fixed hash seed (`PYTHONHASHSEED=0`) so the learner's rows are reproducible: SHA-256 `7fbedcf02019…` (9702), `344a05a4005f…` (9703) |
| Hypotheses, margins, analysis, validity | as frozen | unchanged (`cl/ccl4.py`, `cl/merge_runs.py`) |

## Why
Kaggle's TPU queue started none of the lab's runs: the two 72B dev runs waited from 25 October 16:00 without starting (and a run on 24–25 October waited ten hours). A 96 GB GPU holds the 72B in 4 bits; the 72B speed test on it (CLX-15, dev world 9792) answered 2,290 questions in 11 minutes and trained a session of 542 rows in 3.6 minutes.

## Budget and what counts
About 150–170 of the 186 compute units left are expected for both worlds (about 8–9 hours each at 8.9 units an hour). Output is copied back every 45 minutes; an arm that finishes is valid, and an arm cut short (units, a reclaimed VM) is reported as not run, never as a result. The 7B worlds keep the frozen plan (Kaggle GPUs, weekly reset on 31 October).

## Addendum, 26 October 2026, 14:57 IST: REPLAY not run on the 72B
Decided before REPLAY started in either 72B world (both were in NAIVE's sessions), on the founder's instruction to run CCL-5 next ("final chalao") with no further compute units: each 72B world is stopped right after NAIVE's last evaluation and lie scores, so REPLAY does not run there. R1–R3 are therefore not tested on the 72B (they are on the 7B, whose worlds keep all four arms); the 72B worlds are valid on the arms they run (the untouched model, SYSTEM2, NAIVE), and every other hypothesis keeps its rule.
