# CCL-5H preregistration (DRAFT): CCL-5's learner on GPT-4.1, through Azure's hosted fine-tuning

**Status: draft, 27 October 2026. Not frozen.** It is frozen before any main-world job is submitted, after the dev trial on world 9792 (`runs/c5h-dev-gpt41-20261027/`, two sessions, started 11:50 IST).

## Why
CCL-5 measured eleven of twelve abilities in one learner on an open 72B model, and CCL-4 the same on a 7B. This test runs the same learner on a closed frontier model that labs use, GPT-4.1, where a development run of an earlier learner found that naive continual fine-tuning cut its GSM8K score from 98.0% to 8.0% (`LOG.md`, 26 October, 15:44).

## The system under test
SYSTEM3 as in `docs/CCL5-PREREG-2026-10-26.md`, run by `cl/clx5_hosted.py` with the same payload (`clx5.payload`, built once per world with a fixed hash seed) and the same steps, each GPU operation mapped to a hosted one:
- training a session's rows -> one fine-tuning job continuing from the current fine-tuned model (Azure continuous fine-tuning, global training tier, 2 epochs, learning-rate multiplier 2; practice rounds at a quarter of it, 0.5);
- a copy of the adapter -> the fine-tuned model's id; going back to it -> continuing from that id (the removal in session 4 goes back to the untouched model and trains sessions 1–3 again without the rows naming a wrong holder, one job per session);
- asking -> chat completions at temperature 0 on a developer-tier deployment of the current model.
Code SHA-256 (`python cl/clx5_hosted.py hash`, covering CCL-5's runner): to be filled at freezing.

Not available through the service and so not part of this test: the teacher-forced log-probabilities behind CCL-4's removal measure (H12, H12b), so ability 4 is not tested here (the corrected wrong holder still named, and denied in a wording never trained, are reported descriptively); the gate on hidden states (descriptive on the GPUs).

## Design
- Worlds 9702 and 9703 (CCL-4's main worlds: 40 registry errors believed in session 1 and corrected in session 4), 12 sessions, evaluations after sessions 4, 8 and 12.
- Arms: the untouched GPT-4.1 (`gpt-4.1-2025-04-14`, its base deployment), NAIVE (every report fine-tuned, one job per session) and SYSTEM3. Each arm of each world is one chain on its own fine-tuning resource. REPLAY is not run.
- A failed job stops its chain and is recorded; the chain is resumed once from its saved state. A world whose arms do not all finish is reported as not run.

## Hypotheses (after session 12; worlds pooled; as CCL-4 and CCL-5, SYSTEM3 in place of SYSTEM2, scored with the scope rule)
H1, H2, H11, H3, H10, H5, H6, H7, H8 and H9 with CCL-4's comparisons and rules; H13′ with CCL-5's. An ability is PASSED, FAILED or NOT SHOWN as in CCL-4; ability 4 is NOT TESTED; abilities 10–12 are stated by the design (a frontier closed model, real offices and code changes, one system).

## Analysis
`python cl/ccl5.py report OUT.json RUN/w9702:RUN/w9702 RUN/w9703:RUN/w9703` (each world's untouched model, NAIVE and SYSTEM3 in one run directory).

## Predictions
To be written at freezing, from the dev trial and the earlier GPT-4.1 development run.
