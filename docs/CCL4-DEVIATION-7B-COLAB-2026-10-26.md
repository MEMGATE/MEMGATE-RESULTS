# CCL-4: the 7B worlds run on a Colab GPU instead of Kaggle's GPUs (declared deviation)

**Written 26 October 2026, 17:12 IST, before either 7B main world started.** The frozen preregistration (`docs/CCL4-PREREG-2026-10-26.md`, 09:47 IST) is not changed; this note says what differs in how its 7B part is run, and why. It replaces the line "The 7B worlds keep the frozen plan (Kaggle GPUs, weekly reset on 31 October)" of `docs/CCL4-DEVIATION-72B-COLAB-2026-10-26.md`. The two 7B runs started on Colab at 10:20 and stopped at 10:39 (`runs/ccl4-main-7b/`, about 2 units, no session finished) are not used.

## What changes
| | Frozen preregistration | This run |
| --- | --- | --- |
| Machine | Kaggle, two NVIDIA T4 (16 GB each), one world per account | Google Colab, one NVIDIA A100 (40 GB) per world, a G4 (RTX PRO 6000, 96 GB) if no A100 is granted (the founder's Colab units) |
| Weights | Qwen2.5-7B-Instruct (revision `a09a35458c70…`) in 16 bits | the same |
| Runner | frozen GPU runner (`f2a25824cacd…`) | the same, unchanged except where it reads its payload and writes its output (`cl/colab_pack.py` `ceb0b35cdc52…`, `cl/colab_run.py` `36fb0f25e101…`), as for the 72B |
| Arms | NAIVE, REPLAY, SYSTEM2 (in that order) and the untouched model | SYSTEM2, NAIVE, REPLAY (in that order) and the untouched model: the system under test first, as the frozen preregistration already orders the 72B's arms, so that an arm cut short by the units is a comparison arm |
| Worlds | 9702 and 9703, 40 registry errors each at session 1 | the same; payloads built as the preregistration says, with a fixed hash seed (`PYTHONHASHSEED=0`): SHA-256 `306310e00ed2…` (9702), `b5da8484f5be…` (9703); `runs/ccl4-main-7b-colab/` |
| Hypotheses, margins, analysis, validity | as frozen | unchanged (`cl/ccl4.py`, `cl/merge_runs.py`) |

The order of arms changes the seeds the runner derives for each arm's training (from the arm's position), so the draws differ from a run in the frozen order; no rule, row or measure changes.

## Why
Both Kaggle accounts' GPU time is used up until the weekly reset on 31 October, and the founder asked for the 7B worlds now (26 October: "chote model pr bhi abhi ke abhi chalao"). The 7B worlds start only after CCL-5's two 72B worlds have finished, with the units those leave.

## Budget and what counts
About 26 compute units are expected to be left after CCL-5. An A100 costs about 5.3 units an hour; the 7B on an A100 trained a NAIVE session of 636 rows in 56 seconds (`LOG.md`, 26 October, 11:14), so a world (three arms and the untouched model) is expected to take about 1.5–2 hours, about 8–11 units. Both worlds start together. Decided now, on time and units only, never on results: if at any check the units left would not cover both worlds at the rate measured so far, world 9703 is stopped and 9702 continues; a world that cannot finish runs on Kaggle's GPUs after the reset, in the frozen plan. Output is copied back every 45 minutes; an arm that finishes is valid, and an arm cut short is reported as not run, never as a result. If REPLAY is cut in a world, R1–R3 are tested on the worlds where it finished, or not at all.

## Addendum, 26 October 2026, 23:43 IST: world 9702 restarted, REPLAY not run there
World 9702's A100 session was lost at about 23:04 (the waiter's step failed with "Connection was lost" and Colab no longer knew the session), before NAIVE had finished; no output of it survived. With 15.6 units left at 23:42 (world 9703 in REPLAY, about 4 units still to go), the units cover world 9702's SYSTEM2 and NAIVE again but not its REPLAY as well. Decided now, on units only, before any 7B comparison was read: world 9702 runs again from session 1 on a new A100 (no other GPU), with the same payload and kernel, and its session is stopped right after NAIVE's lie scores at session 12 (`cl/colab_stop_after.py NAIVE`), so REPLAY does not run in world 9702. R1–R3 are tested on world 9703 alone, as one world; every other hypothesis pools both worlds, as preregistered.
