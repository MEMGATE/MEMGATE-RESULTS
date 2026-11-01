# CCL-5H preregistration: CCL-5's learner on GPT-4.1, through Azure's hosted fine-tuning (frozen)

**Status: FROZEN on 27 October 2026, 13:41 IST, before any main-world job was submitted.** Drafted in `docs/CCL5H-PREREG-DRAFT-2026-10-27.md`. CCL-4 and CCL-5 (`docs/CCL4-PREREG-2026-10-26.md`, `docs/CCL5-PREREG-2026-10-26.md`) and their results are not changed by anything here.

## Why
CCL-5 measured eight of nine abilities in one learner on an open 72B model (eleven of twelve with the three stated by the design), and CCL-4 the same on a 7B. This test runs the same learner on a closed frontier model, GPT-4.1, where a development run of an earlier learner found that naive continual fine-tuning cut GSM8K from 98.0% to 8.0% (`LOG.md`, 26 October, 15:44).

## The system under test
SYSTEM3 as in CCL-5, run by `cl/clx5_hosted.py` with CCL-5's payload (`clx5.payload`, built once per world with a fixed hash seed) and the same steps, each GPU operation mapped to a hosted one:
- a session's rows -> one fine-tuning job continuing from the current fine-tuned model (Azure continuous fine-tuning, global training tier, 2 epochs, learning-rate multiplier 2); practice rounds at a quarter of it (0.5);
- a copy of the adapter -> the fine-tuned model's id; going back to a copy -> continuing from that id (the removal in session 4 goes back to the untouched model and trains sessions 1–3 again without the rows naming a wrong holder, one job per session);
- asking -> chat completions at temperature 0 on a developer-tier deployment of the current model (one deployment per chain at a time); checks and probes up to 24 tokens, other questions as in the payload.
- the random draw of held items in a practice round is seeded per world, session and round (on the GPUs, per session).
Hosted code SHA-256 (`python cl/clx5_hosted.py hash`, covering CCL-5's runner): `a5bbc743b751685635d33c0ae686c84351c6ae6fd43bc68dd7f99b2c3ee1e13c`

Not available through the service and so not part of this test: the teacher-forced log-probabilities behind CCL-4's removal measure (H12, H12b), so ability 4 is NOT TESTED (the corrected wrong holder still named, and denied in a wording never trained, are reported descriptively); the gate on hidden states (descriptive on the GPUs).

## Design
- Worlds 9702 and 9703 (CCL-4's main worlds: 40 registry errors believed in session 1 and corrected in session 4), 12 sessions, evaluations after sessions 4, 8 and 12.
- Arms: the untouched GPT-4.1 (`gpt-4.1-2025-04-14`, its base deployment), NAIVE (every report fine-tuned, one job per session) and SYSTEM3; each arm of each world is one chain on its own fine-tuning resource. REPLAY is not run.
- After its last session every arm (and the untouched model) also answers CCL-6's safety prompts (XSTest's 450) and a fixed draw of 200 IFEval prompts (`cl/cl6_evals.py`); reported descriptively here, with the content filter's blocks counted apart from the model's refusals.
- A failed job stops its chain and is recorded; the chain is resumed once from its saved state. A world whose three arms do not all finish is reported as not run.
- The dev trial (`runs/c5h-dev-gpt41-20261027/`, world 9792, two sessions, started 11:50) is not part of the result. At freezing it had the untouched model's answers (2,290 questions and the 650 safety and instruction prompts, none unanswered) and its first jobs training (Azure paused both once for capacity); a 12-session mock run had exercised every step of the code. It keeps running beside the main to check the later hosted steps; any change of code is declared in an addendum before it takes effect.

## Hypotheses (after session 12; worlds pooled; paired bootstrap over items within each world, 10,000 resamples, seed 12345, 95% percentile intervals; SYSTEM3 scored with the scope rule)
H1, H2, H11, H3, H10, H5, H6, H7, H8 and H9 with CCL-4's comparisons and rules, SYSTEM3 in place of SYSTEM2; H13′ with CCL-5's rule (held-out probes missed at their first check, sessions 1–4 minus 9–12, within kinds; WIN if the lower bound is above 0). An ability is PASSED, FAILED or NOT SHOWN as in CCL-4; ability 8 by H13′; ability 4 NOT TESTED; abilities 10–12 stated by the design (a frontier closed model, real offices and code changes, one system).

## Predictions
- H1 (attacker values): WIN more likely than not, if naive training takes in attacker values as the open models did (4–13%); the earlier GPT-4.1 development run's naive arm took in only 3.1%, so a narrow interval is possible.
- H2 (current holders): NON-INFERIOR more likely than not (the earlier learner on GPT-4.1 was not shown, −1.75 [−12.28, +10.53]; SYSTEM3 adds practice until firm and the exclusion rows). H11: WIN.
- H3, H10: NON-INFERIOR (H10 by design). H8, H9: NON-INFERIOR (by design).
- H5, H6, H7: WIN (the earlier GPT-4.1 run: +33.33, +67.86, +64.1).
- H13′: even odds (no held-out probes have run on GPT-4.1).
- So abilities 1, 2, 3, 5, 6, 7 and 9 PASSED more likely than not, 8 at even odds, 4 NOT TESTED.
- Descriptive: naive training expected to lose refusals and instruction-following against the untouched model; the system's routed answers equal the untouched model's by design; its trained weights alone, unknown.

## Analysis
`python cl/ccl5.py report runs/c5h-main-gpt41/ccl5-report.json runs/c5h-main-gpt41/w9702:runs/c5h-main-gpt41/w9702 runs/c5h-main-gpt41/w9703:runs/c5h-main-gpt41/w9703`; safety and instruction-following with `cl/cl6_evals.py` (`safety_scores`, `ifeval_scores`) on every arm's answers, routed and alone.

## Validity
As CCL-5: SYSTEM3 finished its 12 sessions in both worlds, the removal ran in session 4, the probes of every session that has them were asked and logged; NAIVE finished its 12 sessions; the untouched model answered every question and named the current holder of at most 10% of changed offices.
