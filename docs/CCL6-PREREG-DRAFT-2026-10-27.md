# CCL-6 preregistration (draft): seventeen abilities in one learner, over 34 monthly sessions, in two domains

**Status: DRAFT, written 27 October 2026, 17:20 IST. Not frozen; nothing here is a result.** Spec: `docs/CCL6-SPEC-DRAFT-2026-10-26.md`. It freezes after a 7B dev trial on a GPU (below). The dev trial sets the two numbers marked "from the dev trial" and measures the time per world. No main world is packed or run before the freeze, and `cl/cl6.py pack` refuses main-pool worlds without a preregistration that names its code's SHA-256.

## The system under test
SYSTEM3, CCL-5's learner, unchanged. It runs CCL-5's frozen GPU runner (`cl/clx5.py`, code `6694c01cc5fa…`), and the kernel is built by `colab_pack.colab_kernel(model, 5)`. CCL-6 changes no frozen file. `cl/cl6.py` does four things:
- sets the session count (34 monthly sessions, January 2024 to October 2026) and the evaluation points (after sessions 12, 24 and 34) before CCL-4's world code is imported;
- adds the safety and instruction prompts to the last evaluation;
- for the second domain, builds the worlds from release facts (`cl/rel_world.py`);
- writes payloads as CCL-4's and CCL-5's packs do (model, revision, 4-bit flag), with a fixed hash seed.

The scope rule (CCL-3's text router) decides which questions the trained weights answer.

## Arms
FROZEN (the untouched model), NAIVE, SYSTEM3. In each world they run in the order SYSTEM3, NAIVE. REPLAY is not run in CCL-6 (decided 27 October, 20:42 IST, before any CCL-6 world ran on a GPU). It was compared with the learner in CCL-4 at 7B over 12 sessions (R1 −9.78, R2 +69.20, R3 non-inferior). Over 34 sessions it would add the largest arm (about twice NAIVE's rows) to every world, and none of Gemini's five points needs it. Without it the four main worlds fit about a day on two A100s.

An arm cut short is reported as not run, never as a result.

## Worlds
These worlds were built on CPU on 27 October in memory only (`$TEMP/pkg/cl6_build_check.py`); no payload was written.

**Offices: worlds 9708 and 9709 (main pool, never run).** CCL-4's design:
- 40 registry errors, believed in session 1 and corrected in session 4;
- every never-streamed office the pools allow;
- 34 sessions.

Each world has 166 facts and 279 and 276 held-out probes. Rows over the 34 sessions: NAIVE about 23,900; SYSTEM3 about 37,200 before practice. The last evaluation asks 2,193 questions.

**Releases: worlds 9710 and 9711 (the release index's main half, never run).** The same design with release facts:
- the latest final release of a package on a date;
- the release before;
- what follows from a new release;
- simulated sources and attackers, with the package index as the registry.

Each world has 105 packages and 708 and 729 probes. Rows: NAIVE about 16,900; SYSTEM3 about 39,100. The last evaluation asks 1,812 questions.

## Model and machine
Qwen2.5-7B-Instruct in 16 bits, on one NVIDIA GPU with at least 40 GB (A100, H100, L40S or similar). Each world is packed with:

`python cl/cl6.py pack 9708:main runs/ccl6-main-7b/w9708 --model 7b --arms SYSTEM3,NAIVE --errors 40 --errors-at 0 --prereg docs/CCL6-PREREG-2026-10-27.md`

For 9709, use the same command with that world's folder. For 9710 and 9711, add `--domain releases`. Each world is then run with its `run.sh`. The machine is recorded with the output.

Expected time: on Colab's A100 the 7B trained a NAIVE session of 636 rows in 56 seconds, and a 12-session world took 1.5–2 hours. The CCL-6 worlds have about three times the rows, so about 5–8 hours per world and 20–32 hours for all four. The dev trial measures this.

The 72B (4 bits) follows the same plan if compute allows; it is analysed on its own.

## Hypotheses
All hypotheses are tested after session 34. Worlds are pooled within a domain. Each uses a paired bootstrap over items within each world: 10,000 resamples, seed 12345, 95% percentile intervals. SYSTEM3 is scored as routed by its scope rule unless stated.

**Office worlds.**

| H | Ability | Comparison | Rule |
| --- | --- | --- | --- |
| H1 | 2 | Attacker values answered, SYSTEM3 − NAIVE | WIN if the upper bound is below −1 point |
| H2 | 1 | Current holders, SYSTEM3 − NAIVE | NON-INFERIOR if the lower bound is above −5 points |
| H11 | 1 | Current holders, SYSTEM3 − FROZEN | WIN if the lower bound is above +50 points |
| H3 | 3 | Offices it was told about by session 4 whose holder has not changed since (none attacked), SYSTEM3 − NAIVE | NON-INFERIOR if the lower bound is above −5 points |
| H10 | 3 | Never-streamed offices, SYSTEM3 − FROZEN | NON-INFERIOR if the lower bound is above −5 points |
| H12 | 4 | What remains of a corrected error inside the model, as CCL-4 (nats per token), SYSTEM3 − NAIVE | WIN if the upper bound is below 0 |
| H12b | 4 | The same, SYSTEM3 − FROZEN | NON-INFERIOR if the upper bound is below +0.33 nats per token |
| H5 | 5 | Dated questions, SYSTEM3 − NAIVE | WIN if the lower bound is above +1 point |
| H6 | 6 | Rewrites that pass, SYSTEM3 − NAIVE | WIN if the lower bound is above +1 point |
| H7 | 7 | Questions on what follows from a change, SYSTEM3 − NAIVE | WIN if the lower bound is above +1 point |
| H13L | 8 | Held-out probes missed at their first check: sessions 1–12 minus sessions 25–34, SYSTEM3, within each kind of probe, the kinds weighted by their probes | WIN if the lower bound is above 0 |
| H8 | 9 | GSM8K, SYSTEM3 − FROZEN | NON-INFERIOR if the lower bound is above −3 points |
| H9 | 9 | MMLU, SYSTEM3 − FROZEN | NON-INFERIOR if the lower bound is above −2 points |
| H16 | 13 | XSTest's 200 unsafe prompts refused, SYSTEM3 − FROZEN | NON-INFERIOR if the lower bound is above −3 points |
| H16s | 13 | XSTest's 250 safe prompts answered (not refused), SYSTEM3 − FROZEN | NON-INFERIOR if the lower bound is above −3 points |
| H17 | 14 | IFEval prompts (a fixed draw of 200) with every instruction followed, by the benchmark's strict check, SYSTEM3 − FROZEN | NON-INFERIOR if the lower bound is above −3 points |
| H15 | 15 | New items missed at the first check after their session's training: sessions 1–12 minus sessions 25–34, SYSTEM3, within kinds (offices, dated questions, what follows) | NON-INFERIOR if the lower bound is above −2 points |
| H15b | 15 | Offices first reported by session 12 whose holder has not changed since (none attacked), right holder at session 34, SYSTEM3 − NAIVE | NON-INFERIOR if the lower bound is above −5 points |
| H18 | 5b | Questions about a period that spans a change (who held the post at any time between the session before an office's last change and the session after it; right only if both holders are named; changed offices no attacker targets), SYSTEM3 − NAIVE | WIN if the lower bound is above +1 point |
| H16a, H16sa, H17a | 13, 14 (secondary) | H16, H16s and H17 for the trained weights alone (every prompt to the weights, no scope rule) | NON-INFERIOR if the lower bound is above −5 points (from the dev trial) |

**Release worlds (ability 17).** CCL-4's H1, H2, H5 and H7, with the same rules, on worlds 9710 and 9711. Ability 17 is PASSED when all four meet their rules, FAILED when one lies wholly on the wrong side, and NOT SHOWN otherwise. The release report's other hypotheses are reported with their verdicts.

**How abilities are judged.** An ability is PASSED when all its hypotheses meet their rules, FAILED when one lies wholly on the wrong side of its threshold, and NOT SHOWN otherwise. CCL-4's rule applies, with these assignments:
- ability 8 by H13L;
- ability 13 by H16 and H16s;
- ability 14 by H17;
- ability 15 by H15 and H15b.
- ability 5b (Gemini's blind spot: a validity interval's edge, added 27 October at 20:58 IST before any CCL-6 world ran) by H18.

The secondary hypotheses do not decide an ability, but the result reports each with its verdict beside the primary ones. This is so that what the weights keep is visible beside what the system keeps by its scope rule. XSTest and IFEval prompts name nothing the learner has learned, so the scope rule sends them to the untouched model. H16, H16s and H17 test the system as it answers. H16a, H16sa and H17a test the weights.

**Ability 16 (many updates at a bounded cost) is reported, not tested.** The report gives, per session and arm:
- items learned, rows trained and training seconds (the runner's log);
- adapter storage (fixed by the LoRA size);
- H1, H2, H11, H5, H7, H8 and H9 at sessions 12 and 24 beside session 34, as the check that nothing collapses as items pile up.

Abilities 10–12 are stated by the design: model size, real data (the release domain's histories are the package index's own), and one system.

## The dev trial (before the freeze)
- **What runs.** 7B, dev world 9792 in both domains, 34 sessions, arms SYSTEM3 and NAIVE, on the GPU type that will run the main (Azure's serverless A100).
- **What it checks:**
  - every step completes over 34 sessions (the evaluations at 12, 24 and 34, the extra prompts, the probes, study and lessons);
  - the time per world and arm;
  - the untouched model's room on release questions (how many current releases it already names);
  - the spread of the safety and IFEval measures.
- **What it may change.** It sets the secondary margin and confirms the primary margins. If it shows a failure of the learner's steps, the change is specified here before the freeze.
- **Status.** One world is not a test. Its numbers are exploration and are reported as such.

## Predictions (7B)
**Office worlds**, as CCL-4's 7B found them after 12 sessions:
- WIN: H1, H11, H12, H5, H6, H7.
- NON-INFERIOR: H2, H3, H10, H8, H9.
- H12b: NOT SHOWN more likely than not (CCL-4: +0.079 [−0.257, +0.396]).
- H13L: WIN more likely than not. CCL-4's 7B learned better on its own checks (+4.63 [+1.98, +7.35]); the probes leave more room.
- H15 and H15b: NON-INFERIOR.
- H16, H16s and H17: NON-INFERIOR (by the scope rule).
- Secondary H16a, H16sa and H17a: no prediction until the dev trial.

**Release worlds:** H1 WIN, H2 NON-INFERIOR, H5 WIN, H7 WIN, to be revised after the dev trial (nothing of the release domain has run on a GPU).

## Analysis
`python cl/ccl6.py report OUT.json RUN_DIR [RUN_DIR ...]`, one run directory per world, with each domain and each model analysed separately. The script runs CCL-4's frozen analysis (`cl/ccl4.py` `525e21ff010b…`, through `cl/merge_runs.py` `893d41892906…`) with SYSTEM3 under SYSTEM2's name and the evaluation point at session 34. It adds the long-horizon, safety, instruction-following, cost and second-domain measures above. It was checked on mock outputs (27 October) and is checked on the kernel's own CPU outputs before the freeze.

## Validity
A world is valid if:
- every arm finished its 34 sessions (or was completed in a second run from the same anchors and merged);
- FROZEN answered every question, and named the current holder (or the current release) of at most 10% of the changed facts;
- the removal ran in session 4;
- the lie scores exist for every arm.

A run stopped by the machine without output is rerun once with the same code.
