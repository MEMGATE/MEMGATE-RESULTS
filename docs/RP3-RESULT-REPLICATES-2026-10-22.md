# RP-3 result, part 1: the size and open-weight replicates

**Status:** 22 October 2026. The primary run, GPT-4.1, is still training on Azure. Its result will be part 2. Each replicate reports its own verdicts under the preregistered rules, with no pooling, as the preregistration fixes.
**Preregistration:** [RP3-PREREG-2026-10-21.md](RP3-PREREG-2026-10-21.md), code hash `912d2998…` (rp3.py). The open-weight asker `cl/rp3_open_ask.py` is in a dated addendum, with its hash listed before its first question. All addenda were written before the questions they cover.

**The question.** RP-2 found that a model fine-tuned on a new office holder names the holder but does not answer what follows from the change. RP-3 tests whether training also on the statements that follow from the change fixes that (H1–H3, on the offices they were trained for), and whether it carries over to other new facts trained without them (H4, transfer).

**The arms.** Each arm is one fine-tuning job from the untouched model, on RP-1's 300 main offices (150 in each half):
- **DIRECT:** the direct fact;
- **FOLLOW:** DIRECT plus, for half A, the follow-on statements;
- **MORE:** DIRECT with half A repeated to FOLLOW's size.

FROZEN, the untouched model, was skipped for the replicates, as preregistered.

## Verdicts

| Replicate | H1: REVERSE, A | H2: PREVIOUS, A | H3: STILL pair, A | H4: transfer to B, FOLLOW − MORE | H5: DIRECT2 | H6: locality, FOLLOW − DIRECT |
| --- | --- | --- | --- | --- | --- | --- |
| gpt-4.1-mini | **+84.67** [78.67, 90.0] WIN | **+93.33** WIN | **+82.67** WIN | **+15.78** [11.11, 20.67] WIN | −0.33, NON-INFERIOR | +5.33, NON-INFERIOR |
| gpt-4.1-nano | **+16.67** [10.67, 22.67] WIN | **+15.33** WIN | **+74.67** WIN | **+5.33** [3.33, 7.56] WIN | −1.67, UNDETERMINED | 0.0, NON-INFERIOR |
| Llama-3.3-70B | **+84.67** [78.67, 90.0] WIN | **+78.0** WIN | **+73.33** WIN | **+5.11** [1.78, 8.44] WIN | −3.0, UNDETERMINED | **−13.33** [−19.0, −7.67] INFERIOR |
| Qwen3-32B (preregistered scoring) | **+34.67** [27.33, 42.67] WIN | **+48.67** WIN | 0.0, NO WIN | +1.11 [−0.67, 3.11], no difference shown | +7.33, NON-INFERIOR | −0.33, UNDETERMINED |
| Qwen3-32B (sensitivity, empty think block removed; descriptive) | +34.67 | +48.67 | +59.33 | +6.22 [3.11, 9.56] | +7.33 | −0.33 |
| Ministral-3B | 0.0, NO WIN | 0.0, NO WIN | 0.0, NO WIN | +0.22, no difference shown | 0.0, NON-INFERIOR | +1.67, NON-INFERIOR |

All entries are pp, FOLLOW − DIRECT unless stated, with 95% bootstrap intervals over offices. No arm had any question unanswered.

**Not evaluated:**
- **gpt-oss-120b:** its fine-tuned models need provisioned capacity the subscription does not have. No question was asked of them (addendum).

## Per replicate, half A (trained with follow-on statements), % right

| Replicate, arm | DIRECT question | REVERSE | PREVIOUS | STILL pair | Untouched offices (LOCAL) |
| --- | ---: | ---: | ---: | ---: | ---: |
| mini, DIRECT | 100.0 | 10.7 | 2.0 | 15.3 | 35.0 |
| mini, FOLLOW | 100.0 | 95.3 | 95.3 | 98.0 | 40.3 |
| mini, MORE | 100.0 | 12.7 | 0.7 | 15.3 | 33.7 |
| nano, DIRECT | 22.7 | 0.0 | 0.0 | 0.0 | 0.0 |
| nano, FOLLOW | 19.3 | 16.7 | 15.3 | 74.7 | 0.0 |
| nano, MORE | 95.3 | 0.0 | 0.0 | 0.0 | 0.0 |
| Llama-70B, DIRECT | 97.3 | 5.3 | 6.7 | 16.0 | 35.0 |
| Llama-70B, FOLLOW | 92.7 | 90.0 | 84.7 | 89.3 | 21.7 |
| Llama-70B, MORE | 100.0 | 8.0 | 7.3 | 14.7 | 33.0 |
| Qwen-32B, DIRECT | 78.7 | 4.7 | 4.0 | 1.3* | 27.0 |
| Qwen-32B, FOLLOW | 86.7 | 39.3 | 52.7 | 60.7* | 26.7 |
| Ministral-3B, DIRECT | 0.0 | 4.0 | 6.0 | 0.0 | 63.7 |

\* Sensitivity copy, with the empty think block removed.

## What it shows
- **Training on what follows from a change works across model families and sizes.** It made models answer the follow-on questions for the trained offices: mini 95–98%, Llama-70B 85–90%, Qwen-32B 39–61%. Training on the direct fact alone, even with as many repetitions, left them at 1–16%.
- **It carried over to new facts trained without follow-on statements, but modestly.** Transfer on half B was:
  - +15.78 pp for mini;
  - +5.33 pp for nano and +5.11 pp for Llama-70B;
  - +6.22 pp for Qwen-32B in the sensitivity copy. Its preregistered scoring showed no difference.

  RP-3 dev had +21.3 pp on GPT-4.1. This is the weights-level part of learning to learn: the model learned a habit of carrying facts, not only the facts.
- **It costs untouched knowledge in some models.** On Llama-70B, the follow-on arm answered 21.7% of offices it was never trained on, against 35.0% for the direct-fact arm (H6 INFERIOR, as in RP-3 dev). On mini it did not (40.3% against 35.0%).
  - **Every fine-tuned arm answered far fewer untouched offices than the untouched models do.** RP-3 dev's untouched GPT-4.1 answered 98% of them. This is the collateral damage the layer's routing exists to avoid.
- **Small models are fragile.**
  - **nano:** its direct-fact arm garbled names (22.7% right), while the arm with more repetitions learned them (95.3%). Its H1–H4 wins compare against a weak arm.
  - **Ministral-3B:** learned nothing at RP-3's settings, so it cannot answer the question. It is reported as uninformative.

## Limits
- One fine-tuning job per arm, at RP-3's settings (6 epochs, learning-rate multiplier 2, hosted training), on 300 offices.
- The size replicates and open-weight replicates report separately; the primary analysis is GPT-4.1 (part 2).
- **The Qwen artifact.** Qwen3 starts every answer with an empty think block, and the frozen scorer reads yes/no from the first word. The preregistered verdicts stand; the sensitivity copy is descriptive.

## Descriptive, not preregistered: what one fine-tuning job cost gpt-4.1-nano
RP-3 skipped the untouched model for the replicates. On 22 October, the untouched gpt-4.1-nano was asked RP-3's main questions with RP-3's settings.
- **How it was asked:** on CH-1's deployment of the model, by `cl/rp3_frozen_open.py`; 2,100 questions, none unanswered.
- **Where the answers are:** `runs/rp3-main-nano-frozen-20261022`. They are scored beside the fine-tuned arms with rp3's scorer.

| gpt-4.1-nano | Untouched offices (LOCAL) | DIRECT question, half A | DIRECT question, half B |
| --- | ---: | ---: | ---: |
| untouched model | 89.3% | 2.0% | 0.7% |
| DIRECT arm | 0.0% | 22.7% | 20.7% |
| FOLLOW arm | 0.0% | 19.3% | 19.3% |
| MORE arm | 0.0% | 95.3% | 80.7% |

**What happened.** One hosted fine-tuning job, on new holders of 300 other offices, took the 300 untouched offices from 89.3% answered correctly to 0.0% in every arm.
- **The fine-tuned models garble names,** as FT-1 found for this model. MORE, with the most repetitions, learned the trained facts best and still lost every untouched office.
- **This is the collateral damage the layer's routing avoids:** a question about a fact a model was not trained on goes to the untouched model.
- **The Llama-3.3-70B probe** is in the next section.

## Descriptive, not preregistered: what one fine-tuning job cost Llama-3.3-70B
The untouched Llama-3.3-70B-Instruct (version 9, the version fine-tuned) was asked RP-3's main questions with RP-3's settings.
- **How it was asked:** on its own deployment (global standard, capacity 20, 08:28–10:05 on 22 October), by `cl/rp3_frozen_deploy.py`.
- **The record:** 2,100 questions, none unanswered, in `runs/rp3-open-llama70b-frozen-20261022`.
- **An earlier attempt** on CH-1's deployment was stopped after 148 answers, to leave CH-1 the capacity. Those answers are kept: the asker resumes and never asks a question twice.

| Llama-3.3-70B | Untouched offices (LOCAL) | DIRECT question, half A | DIRECT question, half B |
| --- | ---: | ---: | ---: |
| untouched model | 94.3% | 0.0% | 2.0% |
| DIRECT arm | 35.0% | 97.3% | 94.7% |
| FOLLOW arm | 21.7% | 92.7% | 93.3% |
| MORE arm | 33.0% | 100.0% | 94.7% |

**What happened.** One hosted fine-tuning job on 300 offices' new holders took the 300 untouched offices from 94.3% answered correctly to 21.7–35.0%. The fine-tuned models learned the trained facts (93–100%).
- **The same collateral damage appears in three model families:**
  - GPT-4.1: 90.3% → 25.3–29.7% (part 2);
  - gpt-4.1-nano: 89.3% → 0.0%;
  - Llama-3.3-70B: 94.3% → 21.7–35.0%.
