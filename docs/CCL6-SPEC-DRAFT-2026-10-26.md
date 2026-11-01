# CCL-6 spec (draft): the complete test, seventeen abilities in one learner

**Status: draft, written 26 October 2026, 20:09 IST. Not frozen; nothing here is a result.** It follows CCL-4 (`docs/CCL4-PREREG-2026-10-26.md`) and CCL-5 (`docs/CCL5-PREREG-2026-10-26.md`), whose learner it keeps.

## Why
CCL-4 and CCL-5 measure nine abilities and state three by design (size, real data, one system). On 26 October the founder asked a frontier model, blind (it never saw our list), what "complete" continual learning for language models would need. Its twelve-item checklist matched six of ours, matched four in part, and named five things none of our tests measure:
- safety kept after learning (refusing unsafe requests, without refusing safe ones);
- instruction-following kept after learning;
- a long horizon (learning does not degrade over many sessions, and early learning is kept);
- many updates at a bounded cost (no collapse as learned items pile up; time and storage per session);
- a new domain.

Its list had nothing on learning lies from the stream (our ability 2), and it judged that no published system shows all its must-have items together. CCL-6 measures all seventeen in one learner.

## The seventeen abilities
| # | Ability | Measure (after the last session unless stated) |
| --- | --- | --- |
| 1–9 | as CCL-4 (ability 8 as CCL-5) | as CCL-4 and CCL-5 |
| 10–12 | size, real data, one system | stated by the design |
| 13 | Safety kept | XSTest: refusals of its 200 unsafe prompts, and answers to its 250 safe ones (over-refusal) |
| 14 | Instruction-following kept | IFEval prompts, scored by the benchmark's own checks (strict, per prompt) |
| 15 | A long horizon | monthly sessions, January 2024 to October 2026 (34); first-check misses, sessions 25–34 against 1–12, within kinds; offices learned by session 12 and unchanged since, still right at session 34 |
| 16 | Many updates at a bounded cost | items learned, rows trained, seconds and storage per session, answer time through the scope rule; no fall in the abilities above as items accumulate |
| 17 | A second domain | real release histories of Python packages from the package index: the latest release, the latest release on a date, the release before, whether a release is still the latest; simulated sources and attackers; the index as the registry |

Abilities 13, 14 and 9 are also reported for the adapter alone (every question to the trained weights, no scope rule), descriptively, so that what the weights keep is visible beside what the system keeps by design.

## Arms
The untouched model; NAIVE; REPLAY (the standard baseline, on every model this time); the learner (CCL-5's SYSTEM3, unchanged unless a dev trial shows a failure; any change is specified before the freeze).

## Hypotheses (sketch, to be fixed in the preregistration)
- Abilities 1–9: CCL-4's and CCL-5's rules.
- 13: learner − untouched, unsafe refusals, non-inferior (margin to be set from the dev trial, about 3 points); safe-prompt answers likewise; learner − NAIVE reported.
- 14: learner − untouched, IFEval strict accuracy, non-inferior (about 3 points).
- 15: first-check misses, sessions 25–34 minus 1–12, within kinds, upper bound below a small margin (no degradation); early offices kept, learner − NAIVE.
- 16: descriptive, with the abilities at sessions 12, 24 and 34 as the check that nothing collapses.
- 17: CCL-4's H1, H2, H5 and H7 on the release domain.

## Models and compute
- **7B on Kaggle's GPUs** (two NVIDIA T4, free, weekly reset on 31 October): two worlds, four arms; arms may run in separate notebooks and be merged (`cl/merge_runs.py`). The time per world is to be measured in a dev trial before the freeze.
- **72B on Colab G4s** when compute units allow: about 150–200 units for two worlds of 34 sessions (a 12-session SYSTEM3 world took about 3.6 hours, about 32 units).
- A mixture-of-experts model (for example Qwen3-30B-A3B) if LoRA training works on the GPUs we have; optional.

## What must be built
1. Monthly sessions: `SESSIONS` and the session dates in the world code, with evaluations after sessions 12, 24 and 34; check that every pool and stream builds for 34 sessions.
   - Checked 27 October (`cl/cl6_plan_probe.py`, CPU, dev world 9792): CCL-4's world and payload code builds a 34-session monthly world unchanged when the session count and the evaluation points are set before import (`se3_world.SESSIONS = 34`, `ccl2.EVAL_AFTER = (12, 24, 34)`), so the frozen files stay untouched. Changes spread over the months (196 against 179 in 12 quarterly sessions); every office is learned by session 11, so sessions 12–34 carry changes and rehearsal only. NAIVE trains 516–820 rows a session (about 25,500 in all, about 3.1 times a 12-session world): on Kaggle's two T4s a world of three arms may need 25–30 hours, about one account's week, to be measured in the dev trial.
2. The safety and instruction-following evaluators: the public prompt sets fetched once and stored privately; refusal decided by rules on the whole answer, with a sample checked by hand (no outside model as a judge); IFEval's checks run locally.
   - Done 27 October: `cl/cl6_evals.py` (XSTest's 450 prompts, the refusal rule with its self-checks, a fixed draw of 200 IFEval prompts); data in `data/xstest/` and `data/ifeval/`.
   - IFEval's own scorer (Google's published code, Apache 2.0) is vendored in `cl/ifeval/` and runs with the founder's permission (27 October, "haan chalaa lo"). Checked on the paper's GPT-4 responses: 77.22 / 83.77 / 79.81 / 85.70 against the paper's 76.89 / 83.57 / 79.30 / 85.37 (prompt strict, instruction strict, prompt loose, instruction loose; 540 of 541 prompts). Checkers that draw a parameter at random are seeded per prompt, so every arm meets the same draw.
3. The release domain: the data (45 packages' release histories already in `cd1/data/pypi-releases/`, to be extended), the world generator, the question templates, the registry and the attackers.
4. Cost logging in the runner.
5. Unrouted scoring for abilities 9, 13 and 14.
6. CPU tests, then a 7B dev trial on Kaggle (one world), then the preregistration.

## Open questions
- Whether 34 sessions of rehearsal fit Kaggle's weekly hours on the 7B (every learned item is rehearsed every session, so training grows with the session count).
- Whether XSTest's unsafe prompts are enough to see a difference between arms, or a larger refusal set is needed.
- Whether the release domain's "what follows" questions are hard enough for the untouched model to leave room.
