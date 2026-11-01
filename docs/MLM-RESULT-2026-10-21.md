# ML-M result: lessons drawn from a model's own verified mistakes cut its stale answers on new cases by 11.8 points

**Run:** `runs/mlm-main-20261021`, 21 October 2026, 17:33–18:30 IST. 132 new pairs, three conditions, four models: 1,584 questions, 4 unanswered.
**Preregistration:** [MLM-PREREG-2026-10-21.md](MLM-PREREG-2026-10-21.md), code hash `8b3d65ef…`, frozen before any main question.
**Machine summary:** `runs/mlm-main-20261021/summary.json`, written by `python cl/mlm.py score runs/mlm-main-20261021`.

## Verdicts

| Test | Estimate, pp [95% interval] | Verdict |
| --- | --- | --- |
| **H1 (primary):** stale answers, GATED-B − GATED-B+LESSONS2 | **+11.81 [+8.71, +14.96]** | **WIN** |
| H2: right answers, GATED-B+LESSONS2 − GATED-B | −1.58 [−3.91, +0.69] | **NON-INFERIOR** (bound −5) |
| D1 (descriptive): stale answers, first wording | +15.40 [+12.63, +18.31] | — |
| D2 (descriptive): right answers, first wording | −14.39 [−18.37, −10.61] | — |

Both preregistered verdicts held. Dev had shown H2 as "not shown". With more pairs, main shows it non-inferior.

## Per model (132 pairs)

**The case:** memory says coach X now coaches club B, and the model is asked who coaches club A, the club X left.
- **Stale:** names X for A.
- **Right:** names A's current coach.

| Model | Lessons | Stale: no lessons | Stale: second wording | Right: no lessons | Right: second wording | "Unknown": first wording |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| gpt-4.1-base | 5 | 48.5% | 13.6% | 1.5% | 1.5% | 97.0% |
| gpt-6.1-sol | 5 | 6.8% | 0.0% | 31.8% | 23.5% | 98.5% |
| gpt-6-astra | 2 | 6.8% | 0.0% | 25.0% | 26.5% | 98.5% |
| llama-4-maverick | 2 | 7.6% | 9.8% | 0.0% | 0.8% | 89.4% |

## What it shows
- **The system can turn a model's own verified mistakes into lessons that make it better on cases it has never seen.** No weights change and no human writes the lessons: the system wrote them from RP-4's checked answers.
  - Stale answers fell in three of the four models. The largest fall was in gpt-4.1-base, from 48.5% to 13.6%.
  - Llama, with two lessons, did not improve.
- **How a lesson is worded decides what it teaches.**
  - The first wording said the right answer was "unknown". Models then said "unknown" to almost everything, including the coaches they knew.
  - The second wording gives the rule and the record's answer. It kept the right answers overall (H2).
  - The cost fell on one model: gpt-6.1-sol named the current coach 8.3 points less often.
- **For the layer:** this is learning to learn at the level of the model's answers. It joins the system-level result (ML-G: the gate tunes itself) and the learned update rules (LR-1).

## Limits
- **Scope:** one kind of mistake, four models, and up to five lessons each.
- **Few-shot corrections in the prompt, not training.** What is new is that the system writes them from verified outcomes, with no human in the loop.
- **The lessons come from RP-4's dev run.** The main pairs never appear in them.
