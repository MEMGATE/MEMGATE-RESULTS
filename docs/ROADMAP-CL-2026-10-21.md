# Roadmap: from a facts layer to continual learning as a whole

**Written:** 21 October 2026. A working plan, not a claim. Each item goes spec → dev → frozen prereg → main, as before. An item counts as closed only when its main result is in and its claims are in the ledger.

## Where we stand
**Strong, with preregistered evidence: facts learned from untrusted streams.**
- what may be learned (the gate);
- where an update applies (scope);
- exact undo;
- time-aware answers;
- facts that follow from a change (RP-1, RP-2; RP-3 and RP-4 under way);
- evaluation on real data.

**Not yet covered:** the gaps below, in order of priority.

## Gaps and the next experiment for each

| # | Gap | First experiment | Needs |
| --- | --- | --- | --- |
| 1 | **Learning without a registry** (the largest gap) | **RF-1:** a gate with no registry, which earns trust from later agreement among independent sources, from consistency with what it already holds, and from time. Run on the existing worlds with the existing attackers. | CPU |
| 1b | Verifiable domains | **EV-1:** the released artifact as the registry. Code claims are checked against the package's public API surface at the time, with no human registry. | CPU, network |
| 2 | Learning the update rules themselves | **LR-1:** the gate learns from its own verified history which changes imply others (posts one person cannot hold at once, posts that change together), with exceptions. Derived lines are scored for precision on later data. | CPU |
| 3 | Skills beyond facts | **SK-1:** a skill library (code-migration recipes) admitted only when it passes execution tests, scoped to the versions it applies to, and removable by source | CPU, API |
| 4 | Learning to learn | **RP-3 H4:** does training follow-on statements for some facts make the model carry new facts for the others? | Azure fine-tuning (queued) |
| 5 | Knowing what it does not know | **FR-2:** a calibrated probability that each stored value is still true, from how fast similar facts change. Answers say "as of" with that confidence; calibration is scored on real changes. | CPU |
| 6 | Interference at scale | **SC-1:** thousands of verified facts behind retrieval, with look-alike names; collision errors with and without scope keys | API |
| 7 | Scale of weights; a live stream | a 70B open model; a live run on the Wikidata edit stream | GPU (Modal from 1 November; Azure GPU quota is 0) |

## Order of work
1. Finish the runs in flight: FT-1, FT-2, CD-1, RT-1, RT-2, RP-1, RP-3 and RP-4.
2. RF-1 dev, LR-1 dev and FR-2 dev, which are model-free.
3. EV-1, SK-1 and SC-1, which need APIs and the network.
4. Scale and the live stream, when GPUs are available.

## Update, 21 October 2026, 17:00: the target is the whole ideal
The founder set the target as continual learning as a whole: every property in the field summary he shared, including learning to learn and discovery. Where a part cannot be reached, that is recorded with the evidence. No part is ruled out in advance.

| Ideal property | Status after today | Next experiment |
| --- | --- | --- |
| Hybrid memory and weights, selective | done (gate, scope, RP-1/RP-2, FT tests) | MC-1 (whole layer, end to end) is running |
| Robust to untrusted, noisy streams | done, now with no registry too (RF-1, EV-1) | - |
| Measurable | done (preregistration, ledger) | - |
| Self-aware: knows what may be stale and checks it first | done: calibration (FR-2) and checking what is least likely to hold first (RC-1: 35–58% fewer checks for the same freshness) | - |
| Learning to learn, system level | done (ML-G: the gate set its own strictness, 0.00% attacker values, +5.85 pp coverage on clean streams) | - |
| Learning to learn, model level | ML-M done (lessons from a model's own checked mistakes cut stale answers on new cases by 11.81 pp, right answers non-inferior); RP-3 and its mini and nano replicates training | RP-3 (in the weights) |
| Skills, compositional | memory route done (SK-1: each program needs three separately stored skills at once); weights training (SK-2) | SK-2 dev and main when its jobs finish |
| Discovery against reuse | done (DR-2: own verified finds raised pass rates on unseen programs by 32.5 pp) | - |
| Interference at scale | SC-2 main running (dev: undated versions confused every model; the current-value memory gave 100%) | **SC-2** result |
| Efficient and scalable | memory route measured (EF-1: an update to 300,000 facts in 40 ms, identical decisions); weights route timed (1.7–5.2 h per block) | open-model runs when the GPU quota ticket is granted |

## Update, 21 October 2026, 18:15
- **Done today:** RP-1 and RP-4 (what follows from a change), ML-G (the gate tunes itself), RC-1 (re-check first what is least likely to hold) and EF-1 (cost and scale of the memory route).
- **Running:** ML-M main (lessons from a model's own verified mistakes), SC-2 main, MC-1 dev, DR-1 dev, and the RP-3 and SK-2 training jobs.
- **New, started:** LS-1, a live stream with real vandalism. It captures every live Wikidata edit to an office-holder statement for 7 days. Its outcomes, whether each edit was reverted, are fetched only afterwards.
- **Learning the update rules themselves (gap 2): done, LR-1.** Rules learned from memory's own history before 2024 wrote derived lines that were right 92.88% of the time on 2024–26 data, against 81.27% for "one post at a time". They write fewer lines.

## Next question after MC-1 (21 October 2026, 21:55)
- **What MC-1 showed:** with no registry, the layer's main cost is lag. A change made late in the stream, not yet confirmed by independent sources, leaves the previous holder in memory: about 21% of offices at the question date.
- **Idea to test:** a "pending" line, for example "Unconfirmed: N established sources have reported Y since DATE."
- **How to measure it:** current holders gained against attackers' values let through. Colluders are established sources, so the line could also carry their lies.
- **Candidate design:** the line only when its sources were never merged into one voice and never held a never-true value. Its trade-off is measured on MC-1's worlds.
- **Explored the same evening (PH-1, model-free, LOG):**
  - against MC-1's attackers, a pending line from 2 independent voices repaired about 40% of the lag and passed no attacker value;
  - against adaptive pair attackers it passed about 10% of attacked offices.
  - Not adopted. The lag stays the documented price of safety, unless a registry or an environment check is available (RF-2, EV-1).

## Considered and set aside, 22 October 2026: AW-1, the memory's staleness estimate in the model's answers
- **The idea.** Give models the memory's chance that a stored value still holds, and test whether their stated confidence becomes better calibrated, against a dated line alone.
- **Why it was set aside before any question.** The snapshot chose its offices by what happened after March 2024: offices whose holder changed, and offices with one holder since before 2023. Any check day in 2023–2026 therefore has outcomes selected by construction. In a natural sample only 8% of stored values changed, and a balanced sample would make the estimate miscalibrated by design.
- **The clean window is 2020–2023,** where FR-2 found the estimate calibrated. There, models know the answers from their own training, so the memory would not matter.
- **A fair version needs either** a window the models have not seen with outcomes not selected on, such as LS-1's live capture once its outcomes are in, or items limited, before the run, to those each model cannot answer without memory.
