# LM-1 replicates: the layer's dated memory on five more models, from five labs (descriptive)

**Written:** 23 October 2026, 21:52 IST, after scoring. Descriptive, as recorded before any of these answers in the addenda of 17:32, 19:35 and 19:52 in [LM1-PREREG-2026-10-23.md](LM1-PREREG-2026-10-23.md). Reported apart from H1–H3, which stay the two preregistered models' verdicts ([LM1-RESULT-2026-10-23.md](LM1-RESULT-2026-10-23.md)).
**Asked:** the same 402 held-out questions of LongMemEval_S (cleaned release), 353 scored without abstention, in two arms with LM-1's own prompts and notes (`cl/lm1.py`, hash `f4bf4ea3…`, unchanged): RETRIEVAL, the 10 best rounds by BM25; LAYER, the same rounds and then the dated notes from every session. claude-opus-5-5 and grok-4.7 were asked through Microsoft Foundry at the service's default temperature; the three open models greedily, in bfloat16, on Modal H100s (`cl/lm1_modal.py`).
**Scoring:** blind hand labels of all 3,780 answers under the LM-1 guide, in shuffled chunks that mix the arms, then the consistency pass defined before any scoring ([hard-cases.md](../runs/lm1-main-20261023/replicates/hard-cases.md)): 371 items re-read by an adjudicator, one for each of the three packs, and 9 labels changed. The code scorer beside them. No outside model judged anything.
**Machine summary:** `runs/lm1-main-20261023/replicates/summary.json`, from `python cl/lm1_replicates.py score MODEL ...`.

## LAYER − RETRIEVAL over all scored questions (hand labels)

| Model | Lab | RETRIEVAL | LAYER | LAYER − RETRIEVAL [95% CI] | Code scorer |
| --- | --- | ---: | ---: | --- | ---: |
| claude-opus-5-5 | Anthropic | 79.6% | 95.5% | +15.86 [+11.61, +20.40] | +12.75 |
| grok-4.7 | xAI | 72.2% | 86.4% | +14.16 [+10.48, +18.13] | +11.61 |
| Phi-4-mini-instruct (3.8B) | Microsoft | 46.5% | 52.1% | +5.67 [+1.13, +10.48] | +3.12 |
| Llama-3.1-Nemotron-Nano-8B-v1 | NVIDIA | 23.5% | 27.8% | +4.25 [−0.28, +9.07] | +3.68 |
| Gemma 3 12B instruct | Google | 56.7% | 56.9% | +0.28 [−3.68, +4.25] | +0.00 |
| *Preregistered (H1):* GPT-4.1 | OpenAI | 72.8% | 83.9% | +11.05 [+6.52, +15.58] | |
| *Preregistered (H1):* gpt-6.1-sol | OpenAI | 77.1% | 94.9% | +17.85 [+13.88, +22.10] | |

## By question type (hand labels, RETRIEVAL → LAYER)

| Model | Time questions (160) | Other (193) | Multi-session (97) |
| --- | --- | --- | --- |
| claude-opus-5-5 | 83.8 → 95.6 | 76.2 → 95.3 | 56.7 → 90.7 |
| grok-4.7 | 76.2 → 86.2 | 68.9 → 86.5 | 44.3 → 75.3 |
| Phi-4-mini-instruct | 38.1 → 46.9 | 53.4 → 56.5 | 24.7 → 27.8 |
| Llama-3.1-Nemotron-Nano-8B-v1 | 22.5 → 26.2 | 24.4 → 29.0 | 1.0 → 5.2 |
| Gemma 3 12B instruct | 50.6 → 53.1 | 61.7 → 60.1 | 32.0 → 26.8 |

## Reading
- On all four frontier models, from three labs, the layer's dated memory added 11 to 18 points to retrieval: the two preregistered models and the two replicates.
- On the three small open models (3.8B to 12B) it added little: +5.67 points on Phi-4-mini, with an interval above zero; +4.25 on Nemotron-Nano and +0.28 on Gemma 3 12B, with intervals that include zero. The LAYER prompt is long (a median of about 34,000 tokens, up to 47,000 with Gemma's tokenizer), and small models read it less well, as TW-1 found for the dated memory line.

## Caveats
- Descriptive: one run per model and no hypothesis on these models.
- The lab's own blind hand labels, not LongMemEval's GPT-4o judge. The consistency pass's three readings are stated in hard-cases.md.
- The notes were made by GPT-4.1; retrieval is BM25.
- claude-opus-5-5 refused 2 LAYER questions; the empty answers are labelled wrong.
- Gemma 3 12B was asked with FlashAttention-2, after PyTorch's memory-efficient attention failed on its long prompts (addendum 19:52); the other open models with SDPA.
- Nemotron-Nano's answers often break the answer format (a leftover "<short answer>", a trailing "not mentioned"); the consistency pass applies one reading to these.
- No Llama model could be asked (addendum 19:35).
