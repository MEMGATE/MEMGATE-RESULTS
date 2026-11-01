# RP-3 result, part 2: the lab's own LoRA loop on an open model. Qwen2.5-7B, trained also on what follows from a change, answered it (+71.33 points) and carried new facts better (+5.11 points); every adapter cost untouched knowledge (85.0% to 7.7–14.3%)

**Run:** `runs/open-rp3-main-qwen7b`, 22 October 2026, 12:18–12:48 IST.
- **The questions:** 8,400, none unanswered.
- **The hardware:** one A100 80 GB GPU rented at Modal, 29.6 minutes of wall time.

**Preregistration:** [RP3-PREREG-2026-10-21.md](RP3-PREREG-2026-10-21.md), addendum of 22 October, about 12:20 IST.
- It was committed (`0bd412c4`) before any main question.
- **Hashes:** runner `cl/open_rp3_modal.py` `2ab5f3a5…`; RP-3's code `912d2998…`, unchanged.

**Machine summary:** `runs/open-rp3-main-qwen7b/summary.json`, written by `python cl/open_rp3.py report runs/open-rp3-main-qwen7b main`.

**What differs from part 1:** part 1's models were trained by Azure's hosted service. Here the lab trains the adapters itself (RP-3's rows; LoRA rank 16, alpha 32, on the attention projections; 6 epochs at learning rate 2e-4), as the layer would on an open model.

## Verdicts

| Test | Estimate, pp [95% interval] | Verdict | Predicted |
| --- | --- | --- | --- |
| **H1 (primary):** REVERSE on half A, FOLLOW − DIRECT | **+71.33 [+64.0, +78.0]** | **WIN** | WIN |
| H2: PREVIOUS on half A, FOLLOW − DIRECT | +66.67 [+58.67, +74.0] | **WIN** | WIN |
| H3: STILL pair on half A, FOLLOW − DIRECT | +52.0 [+44.0, +60.0] | **WIN** | WIN |
| **H4 (transfer):** follow-on score on half B, FOLLOW − MORE | **+5.11 [+2.67, +7.56]** | **WIN** | no difference shown |
| H5: DIRECT in the held-out phrasing, all offices, FOLLOW − DIRECT | +0.67 [−1.67, +3.0] | NON-INFERIOR | undetermined |
| H6: locality, FOLLOW − DIRECT | +3.33 [−1.0, +7.67] | NON-INFERIOR | undetermined |

**Against the predictions.** H1–H3 held as predicted.
- **H4 was predicted to show no difference,** from dev's +2.67 on 25 offices. On main's 150 offices it was +5.11, a WIN. That is the same size as gpt-4.1-nano's +5.33 and Llama-3.3-70B's +5.11 in part 1.
- **H5 and H6 were predicted undetermined.** Both came out non-inferior.

## Accuracy (%), 150 offices per half and 300 untouched offices

| Arm | DIRECT, A | REVERSE, A | PREVIOUS, A | STILL pair, A | Follow-on score, B | STILL pair, B | Untouched offices (LOCAL) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| FROZEN (untouched model) | 2.7 | 2.0 | 4.0 | 0.0 | 4.0 | 0.0 | **85.0** |
| DIRECT | 100.0 | 3.3 | 0.7 | 0.0 | 2.0 | 0.0 | 11.0 |
| **FOLLOW** | 98.0 | **74.7** | **67.3** | **52.0** | **7.8** | **15.3** | 14.3 |
| MORE | 100.0 | 2.0 | 2.7 | 0.0 | 2.7 | 0.0 | 7.7 |

## What it shows
- **Part 1's findings hold with the lab's own training loop on an open model.** Trained on the direct fact alone, the model named the new holder for every office in half A. Yet it said the person holds the post now for none: STILL pair 0%. Trained also on what follows, it did so for 52%.
  - MORE, with as many rows, did not (0%). The gain comes from the statements, not the volume.
- **Transfer was small but real.** On half B, trained only on the direct fact, FOLLOW answered "yes, now" for 65.3% of offices, against MORE's 0%. The full follow-on score rose 5.11 points.
  - At 7B with the lab's loop, the size matches part 1's smaller models. GPT-4.1 transferred +20.22 points.
- **Every adapter cost untouched knowledge.** Asked directly, with no routing, the untouched model answered 85.0% of 300 offices no arm was trained on. With one adapter switched on, 7.7–14.3%.
  - The layer avoids this by routing a question about a fact the adapter was not trained on to the untouched model, the adapter switched off.
- **Cost:** this replicate took about half an hour on one rented GPU. The hosted jobs of part 1 took hours of queueing and training.

## Limits
- **Two open families at 7B** (Qwen2.5 and OLMo-2, below), one adapter per arm at one setting. The 72B replicate waits for a GPU large enough (`docs/GPU-PLAN-2026-10-21.md`).
- **The follow-on statements are written by the lab** from the verified change (four kinds).
- **Locality is asked without routing.** It measures the adapter, not the layer.

## A second family: OLMo-2-7B on Kaggle's two T4 GPUs
**Run:** `runs/open-rp3-main-olmo7b`, 22 October 2026, 17:14–18:21 IST. The questions were 8,400, none unanswered.
- **The model:** allenai/OLMo-2-1124-7B-Instruct, revision `470b1fba…`, in a private Kaggle kernel.
- **The hardware's difference:** the model was held in float16 over the two T4s and trained with float16 autocast, float32 adapter weights and a gradient scaler. Everything else is the same loop.
- **Preregistration:** RP3-PREREG addendum of 22 October, about 17:15 IST (runner `cl/open_rp3_kaggle.py` `77853b19…`), committed (`6ef6b23a`) before any main question.

| Test | Estimate, pp [95% interval] | Verdict | Predicted |
| --- | --- | --- | --- |
| **H1 (primary):** REVERSE on half A, FOLLOW − DIRECT | **+80.67 [+74.0, +86.67]** | **WIN** | WIN |
| H2: PREVIOUS on half A, FOLLOW − DIRECT | +79.33 [+72.67, +86.0] | **WIN** | WIN |
| H3: STILL pair on half A, FOLLOW − DIRECT | +55.33 [+47.33, +63.33] | **WIN** | WIN |
| **H4 (transfer):** follow-on score on half B, FOLLOW − MORE | **+4.89 [+1.78, +8.0]** | **WIN** | no difference shown |
| H5: DIRECT in the held-out phrasing, FOLLOW − DIRECT | −0.67 [−2.33, +1.0] | UNDETERMINED | undetermined |
| H6: locality, FOLLOW − DIRECT | −2.67 [−6.33, +1.0] | UNDETERMINED | inferior |

| Arm | DIRECT, A | REVERSE, A | PREVIOUS, A | STILL pair, A | Follow-on score, B | STILL pair, B | Untouched offices (LOCAL) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| FROZEN (untouched model) | 0.0 | 2.7 | 4.0 | 0.0 | 3.6 | 0.0 | **49.7** |
| DIRECT | 100.0 | 0.7 | 0.0 | 2.7 | 3.6 | 6.0 | 10.3 |
| **FOLLOW** | 98.0 | **81.3** | **79.3** | **58.0** | **9.1** | **20.7** | 7.7 |
| MORE | 100.0 | 2.0 | 0.7 | 3.3 | 4.2 | 8.0 | 6.0 |

**What the second family adds:**
- **Training on what follows from a change carried it in a second open family too.** The transfer to facts trained without those statements came out the same size: +4.89 points for OLMo-2-7B against +5.11 for Qwen2.5-7B, both WIN. Dev had predicted no difference for both.
- **The adapters again cost untouched knowledge:** from 49.7% to 6.0–10.3%.
- **Cost:** 66 minutes on Kaggle's free T4s.

