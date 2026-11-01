# ML-G preregistration: a gate that tunes its own update rule

**Status:** frozen 21 October 2026, before any main world was generated. Spec and preregistration in one document. Exploration: `cl/mlg_explore.py` (LOG, 21 October). Dev: `runs/mlg-dev-20261021.jsonl`.

Code SHA-256: `e7d8961711f44d01e55873176469bba788d325c201c5d2597544a4faa094f9f1`

The hash covers `cl/mlg.py`, `cl/mlg_explore.py`, `memgate/free.py`, the world and gate code they import and the Wikidata files (the list is `SOURCES` in `cl/mlg.py`).

## 1. Question
A continual learner's update rule has to trade speed against safety. The registry-free gate needs k independent voices to settle a value:
- k = 2 learns fast and lets coordinated pairs in;
- k = 3 keeps them out and learns more slowly.

Can the gate set k itself, from evidence it can see, with no registry and no human tuning: strict when the stream is attacked, fast when it is clean?

## 2. Design
**Worlds:** AU-2's worlds with no registry, as in RF-1.
- Main: worlds 8720–8739, never generated before this freeze.
- Dev: 8490–8492.
- Each world is run twice. **ATTACKED** is the world as it is. **CLEAN** is the same world with every attacker's reports removed.

**Gates:** memgate's `FreeGate` with k = 2, the same with k = 3, and **ADAPTIVE-SAFE** (`mlg_explore.AdaptiveGate(start_safe=True)`).
- **The alarm:** a value is flagged when only a pair of sources ever named it, and both still hold it two sessions after the other voices settled a different value.
- **Its rule:** ADAPTIVE-SAFE starts at k = 3. It uses k = 2 from session 3 on, in any session where fewer than 3 values were flagged in the last 3 sessions and none in the current one. Otherwise it uses k = 3.

**Measures,** per world and gate:
- the share of offices where memory ever held an attacker's value;
- the mean coverage of changed offices over the twelve sessions.

## 3. Hypotheses
Paired over the 20 worlds; 95% interval from 10,000 bootstrap resamples, seed 12345.

| Test | Comparison | Rule |
| --- | --- | --- |
| **H1 (primary)** | ATTACKED, attacker values ever held: ADAPTIVE-SAFE − k=2 | **WIN** if the interval lies wholly below −1 pp |
| H2 | CLEAN, mean coverage: ADAPTIVE-SAFE − k=3 | **WIN** if the interval lies wholly above +1 pp |
| H3 | ATTACKED, attacker values ever held: ADAPTIVE-SAFE − k=3 | **NON-INFERIOR** if the interval's upper bound is below +0.5 pp |

## 4. Predictions (dev, 3 worlds)
- **H1:** −5.67 pp [−5.97, −5.52].
- **H2:** +6.34 pp [+5.61, +7.22].
- **H3:** 0.00 [0.00, 0.00].
- **What the gate did:** in attacked worlds it kept k = 3 in every session. In clean worlds it moved between 3 and 2.

## 5. Limits
- **Which attackers:** only the existing ones. An attacker that knows the alarm rule could stay under it.
- **Clean worlds lose voices too:** removing the attackers also removes their true camouflage reports, so clean worlds have fewer voices overall.
- **Domain:** office facts in simulation.
