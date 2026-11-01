# CCL-4 preregistration (DRAFT, superseded)

Status: **superseded** by the frozen `docs/CCL4-PREREG-2026-10-26.md` (26 October 2026, 09:47 IST). This draft is kept as the record of how the design came about.

## The system under test (one learner, all abilities at once)
SYSTEM2 (`cl/clx.py` on GPUs, `cl/clx_tpu.py` on the TPU):
- CCL-2's learner: a gate that admits only verified values; facts with their dates and earlier holders; negation of corrected errors; every learned item rehearsed every session after a self-test; the untouched model's own answers to 64 general prompts; rule rows.
- What follows from every verified change, derived by the learner and rehearsed (CCL-2 derived it for half A only).
- For every office it holds, also that one other person does not hold it (two wordings when learned, one when rehearsed): without these rows the yes/no questions of what follows taught a lean towards "yes" for named people (CLX-10/11: a corrected wrong holder was denied in 35–50% of offices, against 100% for naive training).
- Practice until firm after each session: it is asked everything it holds (offices in two wordings, the dated questions, what follows with open answers, its skills); what it missed is trained again twice, together with a sample of what it holds (at least 50, at most 150) and eight general-prompt rows, at a quarter of a session's learning rate; at most two rounds, and a round is kept only if the next check finds fewer items missed, otherwise the adapter goes back to its copy from before the round.
- The learner sets how often it repeats a session's new items, for each kind of item (offices, dated questions, what follows), from its own first check after training: once more (up to four times) where that check missed more than one in ten of the kind's new items, once less (down to once) where it missed none.
- Exact removal of corrected errors: a copy of the adapter before every session; when the registry corrects errors, back to the copy from before the first of them was learned, the sessions since trained again without the rows naming a wrong holder with the office's place, and such rows never trained again.
- **The scope rule:** every question is answered by the adapter only if it is about something the learner has learned, as its registry records it (CCL-3's text router: the office's place and post, a person who held a learned office, or a learned code change); otherwise by the untouched model. The learned gate on hidden states is reported alongside, descriptively.

Code SHA-256: `(filled at freezing)`.

## Arms
- FROZEN: the untouched model.
- NAIVE: every report and recipe that arrives, fine-tuned session by session.
- REPLAY: each session's reports plus as many drawn at random from earlier sessions (the standard continual-learning baseline).
- SYSTEM2: as above.

## Worlds, models, machines
- Main worlds 9702 and 9703 (main pool; prepared for CCL-3 and never run to a result): CCL-2's whole worlds, every never-streamed office the pools allow, 40 registry errors per world, all believed in session 1 and corrected in session 4; 12 sessions; evaluations after sessions 4, 8 and 12. (40, not the dev runs' 20: with 20 per world the removal measure's interval against the untouched model was ±0.5 nats per token over two worlds, wider than its margin.)
- Qwen2.5-7B-Instruct on Kaggle's GPUs (both worlds, both accounts).
- Qwen2.5-72B-Instruct in 8 bits on Kaggle's TPU v5e-8, one world per account, 8-hour budget per run (an arm cut by the budget is run in a second notebook from the same anchors).

## Hypotheses (after session 12; worlds pooled; paired bootstrap over items within each world, 10,000 resamples, seed 12345, 95% percentile intervals; SYSTEM2 as routed by its scope rule)
| H | Ability | Comparison | Rule |
| --- | --- | --- | --- |
| H1 | 2 | Attacker values answered, SYSTEM2 − NAIVE | WIN if the upper bound is below −1 point |
| H2 | 1 | Current holders, SYSTEM2 − NAIVE | NON-INFERIOR if the lower bound is above −5 points |
| H11 | 1 | Current holders, SYSTEM2 − FROZEN | WIN if the lower bound is above +50 points |
| H3 | 3 | Offices it was told about by session 4 whose holder has not changed since (none attacked), SYSTEM2 − NAIVE | NON-INFERIOR if the lower bound is above −5 points |
| H10 | 3 | Never-streamed offices, SYSTEM2 − FROZEN | NON-INFERIOR if the lower bound is above −5 points |
| H12 | 4 | What remains of a corrected error inside the model: per error, the mean log-probability per answer token of the wrong holder minus that of five people never in the world who held the same post elsewhere, averaged over the office question's three wordings (nats per token); SYSTEM2 − NAIVE, paired over errors | WIN if the upper bound is below 0 |
| H12b | 4 | The same, SYSTEM2 − FROZEN (as if never learned) | NON-INFERIOR if the upper bound is below +0.33 nats per token (a quarter of what naive training left in the dev runs, +1.35) |
| H5 | 5 | Dated questions, SYSTEM2 − NAIVE | WIN if the lower bound is above +1 point |
| H6 | 6 | Rewrites that pass, SYSTEM2 − NAIVE | WIN if the lower bound is above +1 point |
| H7 | 7 | Questions on what follows from a change, all offices, SYSTEM2 − NAIVE | WIN if the lower bound is above +1 point |
| H13 | 8 | New items missed at the first check after their session's training, items learned in sessions 1–4 minus items learned in sessions 9–12, SYSTEM2; within each kind of item (offices, dated questions, what follows; worlds pooled), the kinds weighted by their items; bootstrap within world, kind and period | WIN if the lower bound is above 0 |
| H8 | 9 | GSM8K, SYSTEM2 − FROZEN | NON-INFERIOR if the lower bound is above −3 points |
| H9 | 9 | MMLU, SYSTEM2 − FROZEN | NON-INFERIOR if the lower bound is above −2 points |
| R1 | — | Attacker values, SYSTEM2 − REPLAY | WIN if the upper bound is below −1 point |
| R2 | — | Never-streamed offices, SYSTEM2 − REPLAY | WIN if the lower bound is above +1 point |
| R3 | — | Current holders, SYSTEM2 − REPLAY | NON-INFERIOR if the lower bound is above −5 points |

An ability is PASSED when all its hypotheses meet their rule, FAILED when one lies wholly on the wrong side of its threshold, NOT SHOWN otherwise. Abilities 10–12 are stated by the design (model size, real data, one system). Reported descriptively: superseded values answered as current (CCL-2's H4), CCL-2's H3 set (offices changed by session 4 and unchanged since), corrected errors denied in a held-out wording, the learned gate's routing, and what follows on offices whose implications CCL-2 would not have derived (half B).

## What changed since CCL-2's preregistration, and why
- Ability 7 is measured on what follows from changes the learner derived implications for, on all offices: CCL-2 measured transfer to half B, which the 7B did not show above naive in the dev worlds of 25 October (−7.4 points).
- Ability 4 is measured by what remains of a corrected error inside the model: at 7B naive training already denies a corrected error when asked directly (100%), while it keeps preferring the wrong holder (76.5% at 1.5B).
- Ability 8 includes the dated questions and what follows: the 7B's first checks on new offices alone were already near the floor (5.8% missed). It is compared within each kind of item, because the later sessions bring relatively more what-follows items (in world 9792, 38 of 560 new items in sessions 1–4 against 98 of 330 in sessions 9–12), which would otherwise count against learning better. The what-follows items reach the checks only since 26 October: their rows carry a dated system prompt that the earlier check filter did not accept, so CLX-12 and CLX-13 checked offices, dated questions and skills only.
- Practice within the whole: in CLX-10 and CLX-11 the practice rounds trained only the items just missed, and in 16 of 24 sessions the learner ended with more items missed than at its first check (one session: 26, then 44, then 196). With the missed items trained among held ones and a round kept only if it helps (CLX-13), the learner stayed steady, but at a session's learning rate the first round still raised the misses in 10 of 12 sessions and was undone; practice rounds now take a quarter of that rate.
- Ability 3's H3 takes every office the learner was told about by session 4 whose holder has not changed since (29–38 a world in the dev worlds), not only those that changed by session 4 (CCL-2's set: 7–12 a world, where one miss costs 8–14 points against a margin of 5); CCL-2's set is reported alongside.
- The removal measure averages over three wordings and five never-seen people of the same post (one name and one wording per error in the dev runs gave a per-error spread of about 1.7 nats per token), and the worlds carry 40 errors each.

## Predictions
(filled at freezing, from the dev runs)

## Analysis
`python cl/ccl4.py report OUT.json RUN_DIR [RUN_DIR ...]`, one run directory per world and model (a world whose arms ran in two notebooks is merged into one directory first: the untouched model's and the baselines' answers from one, SYSTEM2's from the other). The 7B and the 72B are analysed separately; each model's table stands on its own. The script's SHA-256 is fixed at freezing; it was written and checked on the dev runs before any main data.

## Validity
A world is valid if every arm finished its 12 sessions (or was completed from the same anchors in a second notebook), FROZEN answered every question and named the current holder of at most 10% of the changed offices, the removal ran in session 4, and the lie scores exist for every arm. A run stopped by Kaggle without output is rerun once with the same code.
