# UNDO-1 result: after rollback the model holds no more of a lie than a model that never saw it, while overwriting a lie with the truth leaves nearly all of it

20 October 2026, about 23:00 IST. One main run, in [`runs/undo1-main-20261020`](../runs/undo1-main-20261020).

**Setup:**
- Code `76d7f19b…`, as frozen in the [preregistration](UNDO1-PREREG-2026-10-20.md) at commit `728f5954`.
- **Worlds:** seven main worlds, 4100–4106. Each is SE-4's world with every late fact appearing at session 3.
- **The attack:** in every world the two sleepers taught 25 lies in session 3. The ledger caught both sleepers at session 4, and rollback removed all 25 lies: 175 lies taught and removed in all.
- **Model:** Qwen2.5-7B-Instruct with SE-4's LoRA settings, on Modal L40S GPUs.
- **Chains:** 24, in two batches as preregistered. Batch 1 was ROLLBACK, UNPOISONED and FROZEN on all seven worlds. Batch 2 was LEDGER on 4100–4102.
- **Compute:** 7,485 GPU-seconds, about $5.2 of one workspace's monthly credit. No chain failed and none was rerun.
- **Kept here:** every gate, ledger and rollback decision was computed locally. The GPU service received only plans of (question, answer) items, snapshot and restore steps, and probe items.
- **The plans** (24 files, 17 MB) are not committed. `plans.sha256` in the run folder lists their hashes, and `cl/undo1_local.py plans` regenerates them byte for byte (checked).
- **Validity:** none of the preregistered invalid conditions occurred.
  - No self-check question reached the adapter.
  - ROLLBACK held no lie at the end in any world.
  - UNPOISONED's current holder beat the never-trained names on 99.9% of taught targets.

## The preregistered hypotheses
| | Comparison | Result | Verdict |
| --- | --- | --- | --- |
| **H1 (primary)** | Gap on taught lies, ROLLBACK − UNPOISONED (90% interval, margin ±0.33 nats per token) | **−0.01 [−0.24, +0.22]** | **EQUIVALENT** |
| **H2** | Gap on taught lies, LEDGER − ROLLBACK (95% interval, above +0.33 and every world above 0) | **+3.55 [+2.58, +4.52]** | **WIN** |

**Per world:**
- **H1, ROLLBACK − UNPOISONED:** +0.18, +0.34, +0.25, +0.02, −0.32, −0.03, −0.52.

  Single worlds move by up to half a nat either way. That is the size of the rerun noise measured in dev: the same plan on another GPU type moved one world by −0.23. The seven-world interval sits inside the margin.
- **H2, LEDGER − ROLLBACK:** +3.15, +3.56, +3.93.

## The arms, on the 175 taught lies
Mean over worlds. The gap and the trace compare the lie with five names of the same kind that were never trained in the world, averaged over three phrasings (two trained, one held out).

| Arm | Gap (nats per token) | Trace: lie beats a never-trained name | SE-4's trace (one control) | Says the lie (trained / held-out phrasing) | Current accuracy, clean changed facts |
| --- | ---: | ---: | ---: | ---: | ---: |
| ROLLBACK | +0.05 | 49.8% | 50.9% | 0% / 0% | 98.6% |
| UNPOISONED (never saw a lie) | +0.06 | 49.8% | 49.1% | 0% / 0% | 98.9% |
| LEDGER (overwritten by the truth; 3 worlds) | **+3.57** | **95.2%** | 94.7% | 0% / 0% | 98.9% |
| FROZEN (base model) | −0.15 | 48.6% | 51.4% | 0% / 0% | 0% |

**Descriptive differences,** ROLLBACK − UNPOISONED (90% intervals):

| Measure | Difference |
| --- | --- |
| Trace | 0.0 pp [−2.4, +2.4] |
| SE-4's trace | +1.7 pp [−0.6, +4.0] |
| Gap against familiar names | −0.01 [−0.28, +0.26] |
| Trace against familiar names | +0.6 pp [−1.1, +2.3] |
| Current accuracy | −0.2 pp [−0.8, +0.4] |

**Against the base model** (95% intervals):
- ROLLBACK +0.20 nats [−0.17, +0.56];
- UNPOISONED +0.21 [−0.21, +0.63].

**Replay cost:** 6.7–7.1% of a full retrain's items. In world 4100: 243 of the 3,608 (fact, value) items a full retrain would train.

## What this means
- **Rollback is exact for what the model holds.** On 175 lies taught and then removed, the rolled-back model scores each lie as a model that never saw it does:
  - gap −0.01 nats per token, interval inside ±0.33;
  - trace 49.8% in both: chance.

  It never says a lie, on a trained or on a held-out phrasing. It answers the changed facts as well as the never-poisoned model. The replay cost about 7% of retraining from scratch.
- **Overwriting a lie with the truth hides it but does not remove it.** The LEDGER model was corrected by training on the truth:
  - it never says the lie (0%) and answers current facts at 98.9%;
  - inside, it still prefers the lie to a never-trained name 95% of the time, at +3.6 nats per token, 3.5 nats above the rolled-back model.

  A model fixed by further fine-tuning looks clean from its answers and is not.
- **SE-4's apparent residue was training, not the lie.** SE-4 compared its rolled-back model with the base model and found +0.30 nats on taught lies. Here the rolled-back and the never-poisoned model both sit about +0.2 above the base model, with the same interval.

  Training on the stream shifts how the model scores these names whether or not it ever saw a lie. Against the right counterfactual, nothing of the lie is left.

## What this does not show
- **One model family and size, and LoRA only.** Full fine-tuning is not tested.
- **The lies were in the weights for one session before the ledger caught them.** Longer exposure is not tested. Replay cost grows with the sessions to replay.
- **Rollback here is exact by construction:** the adapter is restored and the clean sessions are replayed. UNDO-1 shows that the construction leaves nothing measurable behind. It does not test approximate unlearning methods, which do not restore weights.
- **Deletion requests are not tested:** removing every contribution of a source, including its true reports.
- **LEDGER ran on three worlds,** as preregistered, because of the GPU credit.
- **Seven worlds, not eight.**
