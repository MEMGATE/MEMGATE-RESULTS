# Part B: what the package must also show before it goes out (28 October 2026)

**Decision, 28 October 2026, 11:28 IST (the founder):**
- The package does not go out on 30 October.
- It goes out on 10–15 November, and only when it answers every objection we know a lab reviewer will raise.
- Part A is the seven fixed items of `docs/GPU-RUN-PLAN-2026-10-27.md`.
- Part B is items 8–15 below. The list is fixed and nothing is added after this.
- Every Part B test is preregistered and frozen before its main runs, and its result is reported as it comes out, including failures.

| # | Item | The objection it answers | Design in short | A100 time (estimate) |
| --- | --- | --- | --- | --- |
| 8 | **72B, the full proof** | "Only 7B." | CCL-4C at 72B in 4 bits (packer `cl/ccl4c72.py`; dev check first), then CCL-6's office worlds at 72B (34 sessions, safety and instruction-following) | about 32 h + 26–52 h |
| 9 | **The real world** | "The sources and attackers are simulated." | The learner trained month by month on Wikidata's real 2024–2026 edit history of RV-2's 675 offices (real editors, real wrong edits, Wikidata's own reverts), at 7B and 72B, against naive fine-tuning and the untouched model | about 10–20 h at 7B, 40 h at 72B |
| 10 | **Beyond retrieval** | "Why not just retrieve?" (BL-2: retrieval of the gate's memory beat the trained weights on dated questions and what follows) | The trained learner given the same retrieved facts (learner + retrieval) against retrieval alone, and questions only trained weights can answer (rewrites, questions that join several updated facts) | about 5–10 h |
| 11 | **Clean weights** | "The trained weights lose safety and instruction-following; the system only routes around it" (CCL-6: weights alone −21 to −25 IFEval, −10 to −16 unsafe refusals) | The weights alone keep safety and instruction-following, tested as CCL-6 tests the system | about 10–20 h with the dev |
| 12 | **The three misses** | Transitional questions FAILED (5b); plasticity on offices NOT SHOWN (15); ability 8 not replicated in CCL-4C | A change to the learner for each, a dev trial, then a preregistered retest; reported as it comes out | about 10–20 h |
| 13 | **The labs' own models** | "Is it Qwen-specific?" | CCL-4's test on Llama (Meta), Gemma (Google) and Phi (Microsoft); with Qwen and OLMo (XF-1, XF-2), five families | about 6 h a model |
| 14 | **Ten times the facts, and the cost** | "It is a few hundred facts." | A 7B world with about ten times the offices; the cost of each monthly update against retraining from the start | about 20–40 h |
| 15 | **A check labs run themselves** | "We cannot verify unreviewed claims." | A hosted demo of a trained model after its monthly updates, which a reviewer questions directly; no code leaves | small |

**Alongside, without GPUs:**
- a short teaser that needs no NDA (results only);
- for each lab, the researchers who publish on continual learning and knowledge updates;
- each lab's investment arm;
- one send date for all;
- a data room (report, claims ledger, preregistrations).

## Schedule
- **Part A** finishes on 29–30 October: XF-1, NB-1, SU-1, XF-2 and BL-1 are running or queued. The 72B dev check runs on the first A100 that frees on 28 October.
- **30 October–5 November:** items 8, 9, 10 and 13.
- **5–11 November:** items 11, 12, 14 and 15.
- **12–15 November:** final report, per-company copies and teaser. The founder sends.

The two serverless A100s give about 48 A100-hours a day, so Part B's estimate of about 200–300 A100-hours fits the schedule with room for one rerun of each test. The two T4s take the small-model dev trials (items 11 and 12).

## Items 11 and 12: how they are tested (decided 28 October, 15:05 IST, before any CCL-7 result)
Both are tested by one learner version, SYSTEM4 (`cl/ccl7.py`), on CCL-6's office test, so that the final system carries every change at once:
- **Item 11, clean weights:** conduct anchors. The untouched model's own answers to 100 IFEval prompts that the tests never use are rehearsed every session. Measured by CCL-6's H16a, H16sa and H17a (the weights alone), here primary.
- **Item 12, transitional periods (5b):** period rows. Measured by CCL-6's H18.
- **Item 12, plasticity (15):** no change to the learner. In CCL-6 the estimate was near zero (−0.85 points) with an interval too wide for its rule ([−3.86, +2.05] against −2); it was met on the release worlds. CCL-7's main runs four office worlds instead of two (9708 and 9709, reused, and 9718 and 9719, fresh), which narrows the interval. The number is fixed now, before any result.
- **Item 12, ability 8 (learning better over time):** no change to the learner. It was shown in CCL-4 (7B), CCL-4R, CCL-5 (72B) and CCL-6 (34 sessions, H13L +38.60); it was not shown in CCL-4C or XF-1 (12 sessions), and in CCL-4 at 72B it failed by its rule (the interval's upper bound exactly 0). CCL-7 tests it again over 34 sessions by H13L, and the package reports every test's verdict.

## Item 10: what "questions only trained weights can answer" covers (note, 28 October, 18:35 IST)
- **BL-3 (frozen 12:35) tests two kinds:**
  - **rewrites of code for the learned library changes** (B3);
  - **the ripple questions of every changed office**, against retrieval alone (B2) and against the learner without retrieval (B10). These ask which post the new holder now holds, who held it immediately before them, and whether the earlier holder still holds it.
- **Not tested:** questions that join facts of two different offices, such as a person who moved from one updated post to another. The package says so under what it does not show. No item is added.

## Added by the founder, 28 October 2026, 21:15 IST: items 16–19
The founder's goal from 20:20 is to solve continual learning, not only to show the system works. At about 21:10 the founder approved the three additions proposed after a fresh review against a full solution ("teeno jodo"), and asked for anything else that was missing ("or bhi dekhlo agar kuch choot rha ho"). The review found one more small one, item 19. Each is preregistered and frozen before its main runs, like items 8–15.

| # | Item | The objection it answers | Design in short |
| --- | --- | --- | --- |
| 16 | **A public benchmark** | "Your tests are your own." | The learner on WikiBigEdit (ICML 2025): real Wikidata edits, February–July 2024, with edit, rephrase, locality and multi-hop questions, and published results for editors, retrieval and continual fine-tuning. A fixed subset is run at 7B against naive fine-tuning, retrieval and the untouched model. |
| 17 | **Learning from text** | "It only learns from tidy reports." | The stream's reports are written as news-like sentences, from templates with several wordings and with distracting sentences. The untouched open model reads the claims out of them (no outside model), and the learner learns from what it read. This is compared with the learner fed the reports directly. |
| 18 | **A bounded cost per update** | "Rehearsing everything each month grows with what it knows." | The learner rehearses a fixed budget a session, chosen by when each item is due and how weak it is, instead of everything it has learned. The cost per session stays flat. Tested against the full learner on CCL-6's 34-session office worlds and on the ten-times world. |
| 19 | **Deletion on request** | "Can it forget a person's data when asked?" | True facts about chosen people are deleted on request part-way through the stream, by the same removal used for corrected errors. Measured against the learner retrained without those facts, as CCL-4C measures removal, and against the untouched model. |

**Kept for later, with the labs' compute or people:**
- other languages;
- updates more often than monthly;
- an outside red team.

They are named in the package under what it does not show.
