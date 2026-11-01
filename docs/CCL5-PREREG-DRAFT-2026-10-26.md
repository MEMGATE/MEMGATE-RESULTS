# CCL-5 preregistration (DRAFT, superseded)

Status: **superseded** by the frozen `docs/CCL5-PREREG-2026-10-26.md` (26 October 2026, 16:51 IST).

## The system under test
SYSTEM3 (`cl/clx5.py`): CCL-4's SYSTEM2, unchanged (the frozen GPU runner), plus:
- **Held-out self-tests.** After each session's training and before practice, the learner writes probes about the changes it learned in that session, from its own registry (registry errors left out): who held the post on the session date before the change and who holds it on the current session date, in a wording it never trains ("On D, who held the post of R of P?"), and who had the post until the new holder took it over. It answers them and grades the answers against the registry.
- **Patterns.** Misses are sorted into what the registry shows: the later holder named for the earlier date (premature), the earlier holder for the later date (stale), the new holder named as their own predecessor (self), anything else (other).
- **Study and lessons.** From the next session on it trains the graded probes of the last two sessions with the right answers (the missed ones twice), and, for a pattern with at least three misses in one session, a lesson stating the rule in plain words, kept and rehearsed from then on. A session's probes are asked before any of them is trained.

## Design
- Worlds 9702 and 9703 (CCL-4's main worlds, 40 registry errors each, believed in session 1 and corrected in session 4), the payloads built as CCL-4's with a fixed hash seed; 12 sessions; evaluations after sessions 4, 8 and 12.
- Arm run: SYSTEM3 alone. Its comparisons are CCL-4's runs of the same worlds on the same model and machine: the untouched model, NAIVE and (where it ran) REPLAY. This reuse is declared: those arms' results were known when CCL-5 was frozen; SYSTEM3's were not.
- Model and machine: Qwen2.5-72B-Instruct in 4 bits (NF4) on a Colab G4 (96 GB), as CCL-4's 72B worlds ran.

## Hypotheses (after session 12; worlds pooled; 10,000 bootstrap resamples, seed 12345, 95% percentile intervals)
| H | Ability | Comparison | Rule |
| --- | --- | --- | --- |
| H13′ | 8 | Held-out probes missed at their first check (right after their session's training): probes of sessions 1–4 minus probes of sessions 9–12, SYSTEM3; within each kind of probe (dated, predecessor; worlds pooled), the kinds weighted by their probes; bootstrap within world, kind and period | WIN if the lower bound is above 0 |
| H1–H12b, H5–H9, R1–R3 | 1–7, 9 | CCL-4's hypotheses and rules, with SYSTEM3 in place of SYSTEM2 | as in CCL-4 |

An ability is PASSED, FAILED or NOT SHOWN as in CCL-4; ability 8 is judged by H13′ (CCL-4's H13 is reported alongside). Abilities 10–12 are stated by the design.

## Analysis
`python cl/ccl5.py report OUT.json CCL5_RUN:CCL4_RUN ...` (one pair per world): SYSTEM3 merged with CCL-4's baselines by `cl/merge_runs.py`, CCL-4's analysis (`cl/ccl4.py`) on the merged worlds, H13′ from `probes.jsonl`.

## Predictions
(filled at freezing, from CLX-16)

## Validity
SYSTEM3 finished its 12 sessions in both worlds, the removal ran in session 4, the probes of every session from session 2 on were asked and logged, and CCL-4's baselines for both worlds are valid by CCL-4's rules.
