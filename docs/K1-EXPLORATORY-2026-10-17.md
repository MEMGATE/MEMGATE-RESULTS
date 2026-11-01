# K-1 (exploratory): kolam-style symmetry for board data

17 October 2026.

**Not preregistered. Exposed data only.** This is a measurement, not a verdict.

There is no fresh real board dataset available: tic-tac-toe, Connect-4, KRK and KRKP are all exposed. A synthetic test would be true by construction. So this exploration reports what happens on the exposed boards and claims no WIN.

## Reading

A kolam is drawn on a dot grid and keeps its form under the grid's rotations and reflections. The learning reading tested here: when a board position is observed, the learner also takes in each of its distinct symmetric images, because the outcome cannot depend on the board's orientation.

- **Tic-tac-toe:** the 8 symmetries of the square.
- **Connect-4:** the left-right mirror.

The kolam grammar itself (continuous loops around dots, the drawing rules) is **not** modelled.

Code: [`scripts/explore_kolam.py`](../scripts/explore_kolam.py). Output: [`runs/k1-explore-20261017-a`](../runs/k1-explore-20261017-a/summary.json). Each dataset runs in orders 2000–2009, with the first 1,000 cases taken.

## Result (accuracy %)

| Dataset | R-ORD | R-ORD + symmetric images | 1-NN | 1-NN + symmetric images |
| --- | ---: | ---: | ---: | ---: |
| Tic-tac-toe | 92.4 | **98.3** | 79.2 | **96.7** |
| Connect-4 | 66.5 | 67.5 | 58.7 | 59.4 |

Pooled difference from adding the symmetric images:

| Learner | Difference (pp, 95% CI) |
| --- | --- |
| R-ORD | **+3.45 [+2.85, +4.08]** |
| 1-NN | **+9.13 [+8.57, +9.71]** |

## Reading of the result

Taking in a case's symmetric images is a strong prior when the concept truly has the grid's symmetry. Tic-tac-toe has all 8 symmetries, so it gains the most. Connect-4 has only a mirror, and each 1,000-case sample covers little of its huge position space, so it gains less.

This is the well-known data-augmentation effect from machine learning, seen here through the kolam's symmetry. A preregistered held-out test would need a fresh board or grid dataset with a known symmetry.
