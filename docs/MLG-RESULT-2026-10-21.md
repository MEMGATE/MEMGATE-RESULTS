# ML-G result: the gate set its own update rule, strict when attacked and faster when the stream was clean

**Run:** `runs/mlg-main-20261021.jsonl`, 21 October 2026, 20 fresh worlds (8720–8739), each attacked and clean, no registry, model-free.
**Preregistration:** [MLG-PREREG-2026-10-21.md](MLG-PREREG-2026-10-21.md), code hash `e7d89617…`, frozen before any main world was generated.
**Machine summary:** `runs/mlg-main-20261021-report.json`.

## Verdicts
| Test | Estimate, pp [95% interval] | Verdict |
| --- | --- | --- |
| **H1 (primary):** attacked, attacker values ever held, ADAPTIVE-SAFE − k=2 | **−5.29 [−5.53, −5.06]** | **WIN** |
| H2: clean, mean coverage, ADAPTIVE-SAFE − k=3 | +5.85 [+5.36, +6.35] | **WIN** |
| H3: attacked, attacker values ever held, ADAPTIVE-SAFE − k=3 | 0.00 [0.00, 0.00] | **NON-INFERIOR** |

All three predictions held.

## Per gate (mean of 20 worlds)
| Stream | Gate | Attacker values ever held | Mean coverage | Coverage at the end |
| --- | --- | ---: | ---: | ---: |
| Attacked | k = 2 | 5.29% | 53.98% | 85.45% |
| Attacked | k = 3 | 0.00% | 49.46% | 83.02% |
| Attacked | **ADAPTIVE-SAFE** | **0.00%** | 49.46% | 83.02% |
| Clean | k = 2 | 0.00% | 42.75% | 69.98% |
| Clean | k = 3 | 0.00% | 31.18% | 55.83% |
| Clean | **ADAPTIVE-SAFE** | 0.00% | **37.04%** | **64.96%** |

## What it shows
- **The gate tuned its own update rule from what it could observe.** It had no registry and no human tuning. It watched for one sign of coordination: a value that only a pair of sources ever named, still held after the other voices settled another.
- **On attacked streams it stayed strict.** It used k = 3 in every session, and no attacker value got in, the same as the fixed strict gate.
- **On clean streams it relaxed itself.** It learned 5.9 pp more on average than the fixed strict gate, and 9.1 pp more by the end. It recovered half the gap to the fast gate, at no cost in safety.
- This is learning to learn at the level of the system: the update mechanism improves itself from experience.

## Limits
- **Which attackers:** only the existing ones. An attacker that knows the alarm rule could stay under it.
- **Clean worlds lose voices too:** removing the attackers also removes their true camouflage reports.
- **Domain:** office facts in simulation.
