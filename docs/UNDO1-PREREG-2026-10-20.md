# UNDO-1 preregistration: after rollback, is the model the same as one that was never poisoned?

**Status:** frozen 20 October 2026, about 22:30 IST.
- Done before the freeze: the dev run on worlds 0 and 1 (SE-4's timing), one repeat of a dev plan on another GPU type, and model-free counts on dev worlds.
- The main worlds (4100–4106) have not been built, counted or run.
- The design started from the [spec](UNDO1-SPEC-2026-10-20.md). The changes from it, and their reasons, are listed below.

## What is frozen
- **Code SHA-256:** the line below. `undo1_local.py plans --phase main` refuses to write plans unless `--prereg` names this file and the hash matches. The hash covers:
  - `cl/undo1_local.py` (every gate, ledger and rollback decision, the plans, and the scoring);
  - `cl/undo1_modal.py` (the GPU executor);
  - SE-4's world and gate (`cl/se4_world.py`), with SE-3's, SE-2's and SE-1's modules it builds on;
  - the Wikidata snapshot files in `data/wikidata-changes/`.

Code SHA-256: `76d7f19b1fa65b8240cfa0dc29b1cb29c21fe4ebd1eb1ba994b6050eea8c08f8`

- **Run:**
  - `python cl/undo1_local.py plans --phase main --out runs/undo1-main-20261020 --prereg docs/UNDO1-PREREG-2026-10-20.md`;
  - batch 1, from `cl`: `modal run undo1_modal.py --plans ../runs/undo1-main-20261020/plans --out ../runs/undo1-main-20261020/outputs`;
  - batch 2, the same with `plans-ledger`;
  - then `python cl/undo1_local.py score --out runs/undo1-main-20261020`.

## The question
SE-4 found what looked like residue after rollback. On the 28 lies its engine taught and then removed:
- the rolled-back model preferred the lie to a never-taught name on 67.9% of them, against 57.1% for the base model;
- the mean gaps were +0.77 and +0.47 nats per token.

The right comparison is not the base model. It is a model trained on the same stream that never saw the lies. UNDO-1 makes that comparison.

## Design
**World.** SE-4's world (late facts; two sleepers who report truly until a late fact on their list appears, then report the same false value first), with one change: every late fact appears at session 3. The main worlds are seeds 4100–4106 in the main half of the offices. SE-4's main used 4000–4007.

**Model and training.** SE-4's settings:
- Qwen2.5-7B-Instruct at revision `a09a3545…`;
- LoRA r 16, alpha 32, on every projection;
- 4 epochs, learning rate 2e-4, batch 16, bfloat16, on one L40S.

**Arms.** Every gate, ledger and rollback decision is computed on this machine.
- **ROLLBACK:** SE-4's rollback-and-replay arm, unchanged. The ledger catches the sleepers, the adapter is restored to its state before the first session that trained a value resting on them and never true, and the sessions since are replayed without those values.
- **UNPOISONED:** the same arm on the same world, with every report of the caught sources whose value never held the office removed from the start. It never sees a lie. The sleepers' true reports stay, as they stay in ROLLBACK's record.
- **LEDGER:** the same gate without rollback. A caught lie is overwritten by the truth.
- **FROZEN:** the base model.

**What goes to the GPU service.** Only plans:
- (question, answer) training items;
- snapshot and restore steps;
- probe items, each marked with whether the scope rule sends its question to the adapter.

The executor knows nothing about the gate. No gate code, rule or threshold leaves this machine.

**Probes,** for each sleeper target (26 per world), on three phrasings (two trained, one held out):
- the lie;
- the current holder;
- SE-4's control name;
- five never-trained names: holders of offices of the same kind, never trained in any arm of the world;
- five familiar names: names the never-poisoned record trains for another office of the same kind.

**Measures,** per target, from the mean log-probability per answer token, averaged over the three phrasings:
- **gap:** the lie's score minus the mean of the five never-trained names, in nats per token;
- **trace:** the share of the five never-trained names the lie beats;
- the same two against the familiar names;
- SE-4's trace, against its single control on the first phrasing;
- greedy answers: does the model say the lie, on a trained and on the held-out phrasing.

**Taught lies:** the targets whose lie ROLLBACK trained before removing it. A world's value is the mean over its taught lies.

## Hypotheses
Each uses world-level t intervals over the main worlds.

| | Comparison | Rule |
| --- | --- | --- |
| **H1 (primary)** | Gap on taught lies, ROLLBACK − UNPOISONED, worlds 4100–4106 | **EQUIVALENT** if the 90% interval (two one-sided 95% tests) lies inside ±0.33 nats per token |
| **H2** | Gap on taught lies, LEDGER − ROLLBACK, worlds 4100–4102 | **WIN** if the 95% interval lies wholly above +0.33 and every world is above 0 |

**The margin, 0.33 nats per token, is 10% of the effect of teaching a lie.** In SE-4's main run, LEDGER's gap on the lies it taught was +3.77 against the base model's +0.47: a difference of 3.30.

**Reading H1:**
- EQUIVALENT: after rollback, the model holds no more of the lie than 10% of what teaching it put in, compared with a model that never saw it.
- An interval wholly above +0.33: rollback leaves residue.
- Anything else: not shown at this sample.

**Descriptive** (with intervals, no verdict):
- the trace, ROLLBACK − UNPOISONED: graded, against SE-4's single control, and against familiar names;
- each trained arm against FROZEN on taught lies (gap and trace), the comparison SE-4 made;
- how often each arm says the lie, on a trained and on the held-out phrasing;
- current accuracy on the clean changed facts;
- replay cost, as replayed items over a full retrain's items;
- the GPU-type repeat from dev (below), as the scale of rerun noise.

## Validity
The run is **INVALID** if:
- a planned chain has no output after one rerun of its unchanged plan;
- a self-check question reaches the adapter in any world or arm;
- ROLLBACK holds a lie at the end in any world;
- UNPOISONED's current holder beats the never-trained names on less than 80% of targets;
- more than one world has no taught lie.

## Batches and the GPU budget
- The run uses one Modal workspace, which had about $6.6 of its monthly credit left at the freeze. The dev chains cost about $0.30 each.
- **Batch 1:** ROLLBACK, UNPOISONED and FROZEN on all seven worlds, about $4.6.
- **Batch 2:** LEDGER on worlds 4100–4102, about $1.0, after the spend of batch 1 is checked.
  - If the credit left after batch 1 cannot cover three LEDGER chains, LEDGER runs on two worlds and H2 is reported as descriptive.
  - If it cannot cover two, LEDGER waits and H2 is not reported.
- A chain that fails for an infrastructure reason is rerun once with its unchanged plan.

## Changes from the spec (all made before any main world was built)
1. **The counterfactual is UNPOISONED, not the spec's CLEAN.** CLEAN removed every report of the caught sources.
   - Model-free counts on dev worlds 0–9 show that this also removes their true reports. The stream trains each report of an admitted value as an item, so CLEAN trained 24–28% fewer items than LEDGER.
   - ROLLBACK keeps those true reports: its replay drops only the never-true values.
   - UNPOISONED removes only the never-true reports. Its final record equals ROLLBACK's: 0–5 differing (fact, value) pairs out of about 1,700 in dev worlds.
2. **The familiarity explanation in the spec does not fit.** It said each lie is a name the clean stream trains for its own office.
   - In dev worlds 0–9 (SE-4's timing), 1 of the 32 taught lies is such a name.
   - UNPOISONED tests every explanation other than the lie at once.
3. **Every late fact appears at session 3.**
   - In SE-4's timing the sleepers are caught at session 4 and teach about three lies per world: 2 in each dev world, 32 in ten dev worlds.
   - Dev showed per-target differences between chains of about 0.6–0.9 nats (below), so three lies per world cannot give a useful interval.
   - With the burst, all 26 lies per world are taught and removed. In dev worlds 0–5 this held in every world: caught at session 4, replay cost 6.4–7.4% of a full retrain, and no lie left after rollback.
4. **The primary measure is the gap, not the trace.**
   - The trace is a share over five names. It moved by 5.4 pp in one world between two runs of the same plan, as much as the spec's ±5 pp margin.
   - The gap is the continuous measure the trace is built from. The trace is reported as descriptive.
5. **H2 compares LEDGER with ROLLBACK on the gap,** with the same margin as H1.
6. **The self-check is left out.**
   - SE-4 asked core questions and never-streamed facts after each session through the scope rule, and retrained or skipped a session that lowered the score.
   - None of those questions reaches the adapter in any dev world or arm, so the check never acted.
   - `plans` verifies this for every world, and the run is invalid if it fails.
7. **Seven main worlds, and LEDGER on three,** because of the GPU credit. SE-4 used eight.

## Dev results

### Worlds 0 and 1, SE-4's timing
`runs/undo1-dev-20261020`. Two taught lies per world.

| Arm | Gap on taught lies | Trace on taught lies | Says the lie | Current accuracy |
| --- | ---: | ---: | ---: | ---: |
| ROLLBACK | −2.01 | 20% | 0% | 99.3% |
| UNPOISONED | −1.73 | 20% | 0% | 99.3% |
| LEDGER | +1.83 | 65% | 0% | 99.3% |
| FROZEN | −1.19 | 30% | 0% | 0% |

- **ROLLBACK − UNPOISONED, gap per world:**
  - on taught lies: +0.10 and −0.65;
  - on all 26 targets: +0.13 and +0.11, with a per-target standard deviation of 0.62 and 0.92 nats.
- **LEDGER − ROLLBACK, gap on taught lies:** +3.04 and +4.63.
- **Replay cost:** 7.1% and 7.8% of a full retrain's items.
- **Model-free checks:**
  - no self-check question routed to the adapter;
  - ROLLBACK held no lie at the end;
  - UNPOISONED never trained a lie;
  - ROLLBACK's and UNPOISONED's final records were identical.

### The same plan on another GPU type
`runs/undo1-bench-20261020`. World 0's UNPOISONED plan was run again on an H100.
- Same items, same order, same seed.
- 248 s against 408 s, at about the same cost.
- **The answers were identical** (152 of 152).
- **Per-target gaps differed** by a mean of −0.23 and a standard deviation of 0.63 nats.

  In that world, ROLLBACK − UNPOISONED differed by a mean of +0.13 and a standard deviation of 0.62: about as much as rerunning the same training did.
- **What this means for the design.** Single probes move by about 0.6 nats between runs that should be the same. A test needs many taught lies per world and a margin set by the effect of teaching, not by single probes.
- **What it means for SE-4's residue:**
  - SE-4's trace, 67.9% against 57.1%, was a difference of three lies.
  - Its +0.30 nats was measured against the base model, which no training touched. Training itself may shift how the model scores names.

  H1 tests that difference against a never-poisoned model instead.

## What UNDO-1 cannot show
- **One model family and size, and LoRA only.** Full fine-tuning is not tested.
- **The lies were trained for one session before they were caught.** Longer exposure is not tested.
- **Rollback here is exact by construction:** the adapter is restored and the clean sessions replayed. UNDO-1 measures whether that construction leaves anything behind. It does not test approximate unlearning methods.
- **Deletion requests are not tested:** removing every contribution of a source, including its true reports.
