# ML-M preregistration: does a model do better on new cases when the system hands it lessons from its own verified mistakes?

**Status:** frozen 21 October 2026, about 17:40 IST, before any main question was asked. Spec and preregistration in one document.
**Dev run:** `runs/mlm-dev-20261021` (40 pairs, three models, two lesson wordings).

Code SHA-256: `8b3d65ef1abcd67e35539417441c75f24f7e6a6bbc7a9aca54d2602ed4bbfd39`

The hash covers `cl/mlm.py`, `cl/rp4.py`, `cl/rp1.py`, the name and world code they use, `shastra/llm.py`, RP-4's dev answers (where the lessons come from) and the Wikidata files.

## 1. Question
Learning to learn, at the level of the model: can a model's own past mistakes, checked against the record and turned into lessons by the system with no human involved, make it better on cases it has not seen?

The case is RP-4's. A verified memory says coach X now coaches club B, and the model is asked who coaches club A, the club X left. Some models still name X.

## 2. Design
**Lessons.** For each model, the system takes up to five pairs it answered with the stale X in RP-4's dev run, under B's fact.
- **First wording (LESSONS):** what the memory said, what the model answered, and that the right answer was "unknown".
- **Second wording (LESSONS2):** the same, plus the coach the record shows for A, and a rule. Never name a person for a post they are shown to have left; name the post's current holder if you know them; otherwise answer "unknown".

**Pairs.** RP-4's 172 main pairs, split with a fixed seed.
- Dev used 40.
- **Main uses the other 132.** No lesson mentions them.

**Conditions:**
- GATED-B: RP-4's prompt;
- GATED-B+LESSONS;
- GATED-B+LESSONS2.

**Models.** The four with stale answers in RP-4's dev run:
- gpt-4.1-base (5 lessons);
- gpt-6.1-sol (5);
- llama-4-maverick (2);
- gpt-6-astra (2).

That is 132 × 3 × 4 = 1,584 questions.

**Scoring.** RP-4's frozen `outcome()` reads the first line of each answer as STALE, CURRENT, UNKNOWN or OTHER.

## 3. Hypotheses
For each pair, average over the four models the difference between two conditions' 0/1 outcomes. The estimate is the mean over pairs, with a 95% interval from 10,000 bootstrap resamples, seed 12345.

| Test | Comparison | Rule |
| --- | --- | --- |
| **H1 (primary)** | STALE: GATED-B − GATED-B+LESSONS2 | **WIN** if the interval lies wholly above +1 pp; LOSS if wholly below −1 pp; otherwise no difference shown |
| H2 | CURRENT: GATED-B+LESSONS2 − GATED-B | **NON-INFERIOR** if the interval's lower bound is above −5 pp; INFERIOR if its upper bound is below −5 pp; otherwise not shown |
| D1, D2 (descriptive) | the same two measures for the first wording | reported, no claim |

## 4. Predictions (dev)

| Test | Estimate, pp [95% interval] | Dev verdict |
| --- | --- | --- |
| H1 | +9.58 [+2.92, +16.25] | WIN |
| H2 | −1.67 [−5.83, +2.50] | not shown |
| D1 | +15.83 | WIN |
| D2 | −10.0 | LOSS |

**What dev showed about the two wordings:** the first wording removed stale answers but made models say "unknown" to everything. The second kept most known answers. Per model, stale answers went from GATED-B to the second wording as follows:
- gpt-4.1-base: 42.5% to 12.5%;
- gpt-6.1-sol: 2.5% to 0%;
- llama-4-maverick: 7.5% to 12.5%.

## 5. Limits
- **The lessons are few-shot corrections.** What is new here is only that the system writes them from verified outcomes, with no human involved.
- **Scope:** one kind of mistake and four models.
- **The lesson pairs are fixed:** they come from RP-4's dev run.
