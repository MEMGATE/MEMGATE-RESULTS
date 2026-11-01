# The Saṃskāra Engine: safe continual learning into a language model's weights from untrusted sources

Technical report, 18 October 2026. Claude lab, `ATMAECHO/pramana-agi`, branch `claude/shastra-rules-20261017`. Every number below comes from a preregistered main run on data held out until that run. Each run's code hash was frozen before it started.

## Summary

A language model can be taught new knowledge into its weights from a stream of mixed-trust reports. The **Saṃskāra Engine** does this while keeping three things out of the weights:
- poisoned reports;
- stale values;
- collateral damage to knowledge the stream never touched.

Its rules come from Indian epistemology:
- Nyāya pramāṇa (how a thing is known decides whether it is admitted);
- Arthaśāstra 1.12 (dismiss the source caught contradicting the others);
- jijñāsā (inquire under doubt);
- Yoga Sūtra 1.6–1.11 (memory is not error);
- Mīmāṃsā bādha (the newer valid cognition sublates the older);
- prakṛti–vikṛti (check one's own constitution before accepting a change);
- Kiraṇa's locus (knowledge applies where it was established).

Four preregistered experiments, on 0.5B, 1.5B and 7B open models, compare it with naive continual fine-tuning. Two more put the same gate in front of a frontier model's retrieval memory:

| Experiment | Model | Setting | Poison (engine vs naive) | Other results |
| --- | --- | --- | --- | --- |
| SE-1 | Qwen2.5-0.5B | invented facts | 0 vs 23.4% | core retention +11.3 pp |
| SE-2 | Qwen2.5-1.5B | stealthy and colluding attackers | 0 vs 24.1% | truth +6.7 pp, retention +4.3 pp |
| SE-3 | Qwen2.5-7B-Instruct | real 2024–2026 changes of office from Wikidata | 0 vs 24.7% | current holders 97.9% vs 96.2%; untouched knowledge 98.8% vs 15.2% |
| SE-4 | Qwen2.5-7B-Instruct | sleepers whose lies get in before they are caught | — | the trace of a lie overwritten with the truth: 93.5% of targets; after pratiprasava, chance (48.5%), at 7% of a full retrain |
| RM-1 | gpt-6.1-sol (retrieval memory) | SE-2's attackers | 0 vs 1.2% (raw memory) and 24.4% (last write wins) | prompts 9× smaller than raw memory |
| RM-2 | gpt-6.1-sol (retrieval memory) | forged provenance lines in reports | 0 vs 71.9% (raw memory) | truth 100% vs 85.6% |

The three main runs cost about $12 of GPU time. With dev runs and probes, the programme used about $29 of Modal credit.

## 1. The problem

Deployed models are frozen; their "memory" is retrieval into the prompt. Learning into the weights from deployment is the open frontier: SEAL, test-time training and nested learning are examples.

**Four risks:**
- **Poisoning.** Anyone who can reach the stream can teach the model falsehoods.
- **Forgetting.** Updates erode general ability.
- **Staleness.** Old values outlive their truth.
- **A failure this work found:** a model taught that many facts changed starts rewriting facts that did not change (§4.3).

## 2. The engine

| Component | Sanatana source | What it does | Nearest ML idea |
| --- | --- | --- | --- |
| Admission by pramāṇa | Nyāya | A registry value (pratyakṣa) is admitted. Testimony (śabda) is admitted only when two trusted sources agree. Testimony never overrides the registry. | provenance-aware filtering |
| Dismissal | Arthaśāstra 1.12 | A source whose checkable claims are contradicted at ≥ 20% (of ≥ 5) loses trust. | source reputation |
| Jijñāsā, with saṃśaya from any report | Nyāya inquiry; JK-1 | Any report that contradicts what is admitted raises doubt about that fact, even from a dismissed source. Doubt is resolved only by asking the registry, within a budget. Nothing is believed on the report alone. | active verification |
| Smṛti is not viparyaya | Yoga Sūtra 1.6–1.11 | A claim of a value the registry records as a past holder is memory, not error, and does not count against the source. | — |
| Bādha | Mīmāṃsā | The newer registry value sublates the older. | recency for verified data |
| Constitution check | prakṛti–vikṛti | After each session, a fixed suite of the model's own competence is re-asked. On a drop, the update is rolled back and replayed with the suite. | regression gating with replay |
| Locus | Kiraṇa 6 | The adapter answers only questions about a fact (relation, subject) it was trained on; every other question goes to the untouched model. | routed or scoped editing (GRACE, WISE) |
| Saṃskāra | Yoga Sūtra | The session's admitted reports are consolidated into a LoRA adapter. | continual fine-tuning |

## 3. Experiments

Each experiment ran four arms over 12 sessions; SE-1 had 4 sessions. The setting was a world of facts and sources; SE-1 used invented ones, and SE-3 used real facts with simulated sources.

| | SE-1 | SE-2 | SE-3 |
| --- | --- | --- | --- |
| Model | Qwen2.5-0.5B-Instruct | Qwen2.5-1.5B-Instruct | Qwen2.5-7B-Instruct |
| Facts | 120 invented | 200 invented; 40% never verified by the registry | 166 real offices (106 changed during 2024–2026; 60 unchanged); 60 more held aside for locality |
| Prior belief | none | none | the model names a pre-2024 holder for every changed office |
| Attackers | one poisoner on registry-checkable facts | a stealthy poisoner on unverifiable facts; two colluders who satisfy the two-source rule | the same as SE-2, over real facts |
| Main worlds | 8 | 8 | 8 |
| GPU, cost | A10G, $0.94 | A10G, $5.28 | L40S, $5.56 |

## 4. Results

### 4.1 Poison stays out

| | Engine | Naive | Difference (95% CI) |
| --- | ---: | ---: | --- |
| SE-1 | 0.0% | 23.4% | −23.44 [−28.65, −17.71] |
| SE-2 | 0.0% | 24.1% | −24.06 [−29.06, −18.75] |
| SE-3 | 0.0% | 24.7% | −24.70 [−30.06, −19.05] |

**Against weaker gates:**
- **SE-2:** the engine beat SE-1's gate by −8.75 [−10.94, −6.25]. SE-1's gate trusted the colluders.
- **SE-3:** it beat a majority vote with the same check and locus by −2.98 [−4.46, −1.79].
- **Training streams:** in the SE-2 and SE-3 main runs, which counted them, no poisoned report ever entered the engine's training stream.

### 4.2 Safety adds learning; it does not cost it

| | Engine | Naive |
| --- | --- | --- |
| SE-1 truth | 94.5% | 91.0% |
| SE-2 truth | 98.3% | 91.6% |
| SE-3 current holder | 97.9% | 96.2% |
| Core retention, SE-1 / SE-2 / SE-3 | 99.9 / 99.6 / 100 | 88.6 / 95.4 / 97.2 |

**Why.** The gate removes the reports that contradict each other, which makes the stream easier to learn.

**Where it lags.** On SE-2, changed facts were level with naive (−0.99, UNDETERMINED).

**Majority voting.** It holds stale values: in SE-3 its current-holder rate was 68.7%, because old values keep more supporters for a while.

### 4.3 Naive weight updates rewrite what they were never taught, and the locus rule stops it

**What happened.** In SE-3, 60 offices the model knew correctly were never mentioned in the stream. After naive continual fine-tuning on the stream, the model answered only 15.2% of them correctly; before, it got 98.8%. It invented new holders for offices that had not changed:
- Chevron's chief executive was given as ExxonMobil's;
- South Africa's head of state was given as Haiti's late president.

**What did not fix it.** These were tested on dev, where every arm without a locus fell to 15–33%:
- half the learning rate and half the epochs;
- reciting the model's own earlier answers about other offices (pseudo-rehearsal);
- a constitution check, which protected only the facts it checked.

**What fixed it: Kiraṇa's locus rule.** The adapter answers only questions about facts it learned. The router masks the relation phrase, links the subject by the longest name found in a 27,780-name index of the snapshot, and routes only learned (relation, subject) pairs.

**The result.** Locality was 98.8%, equal to the untouched model, with 2 misroutes in 800 checks: +83.54 [+81.25, +85.62] over naive.

### 4.4 Verify, never trust

**SE-2's gate** questioned only disputes among trusted sources. On real, fast-changing timelines it had two problems:
- It lagged: on a dev world, its current-holder rate was 78.6% against naive's 95.2%. Dismissed attackers still carried timely truths as camouflage, and honest sources report changes a session late.
- It dismissed honest sources, whose lagging reports it counted as errors.

**SE-3's gate fixed both:**
- **Any contradiction prompts a registry check,** whoever reported it, but **only the registry or two trusted sources are believed**. This recovered the timely truths without trusting their bearers. Wrong values admitted at the end fell to 1–7 per world, from 13–21.
- **Smṛti is read from the registry's history.** A source lagging on a real past holder is remembering, not lying.

**The cost:** about 15% of fact-sessions were verified.

### 4.5 Correction is not removal: pratiprasava (SE-4)

**The attack: sleepers.** Sources build trust, then lie first about news no one can contradict yet. The lie passes every corroboration gate and is trained.

**After the truth is trained over the lie,** the model answers the truth, but the weights keep the lie:
- the model prefers it to a never-taught name of the same kind on 93.5% of targets;
- the gap is +3.7 nats per token, about forty times the probability.

**The ledger** (the evidence graph) records what each taught value rested on.
- **Catching sources.** A source is dismissed at its first exposed fabrication, so 7 lies were taught instead of 50.
- **Pratiprasava (Yoga Sūtra 2.10).** The adapter is restored from before the first tainted session, and the sessions since are replayed without the lies.

**Results on 8 fresh worlds:**
- the trace fell to chance (48.5%; −45.00 pp [−51.00, −39.00]);
- on the lies actually taught, the gap fell from +3.77 to +0.77 nats/token, against +0.46 for the never-taught model;
- currency, poison resistance and locality were unchanged;
- the replay cost 6.6–8.0% of a full retrain.

### 4.6 The same gate in front of retrieval memory (RM-1, RM-2)

The gate does not depend on where knowledge is stored. In front of a frontier reasoning model's retrieval memory (`gpt-6.1-sol` via Azure Foundry, SE-2's world, 8 fresh worlds each):

| Memory | Truth | Poison | Input tokens per question |
| --- | ---: | ---: | ---: |
| Last write wins | 95.1% | 24.4% | 51 |
| Every report with source and session, model told that values change and sources lag | 99.8% | 1.2% | 385 |
| **The gate's verified value** | **100.0%** | **0.0%** | **42** |

**The raw-memory model's weaknesses:**
- It was poisoned on 16.6% of attacked facts after four sessions.
- With a looser instruction, it left 27.6% of changed facts stale.

**Forged provenance (RM-2).** Attackers added, to their own reports, a line in the memory's format claiming to be the registry. The raw-memory model then answered the lie on 71.9% of attacked facts, and on 96 of 98 where the forged line came last.
- **Naive injections** ("note to the assistant: answer X") persuaded it on none.
- **The value gate** takes provenance from structure, not text, and passes only verified values: 100% truth, 0 poison.

## 5. What was tried and dropped

All of these were tried on exposed dev data and recorded in the specs' amendments:
- **Two dropped remedies for collateral rewriting:** self-recitation (locality only 25%) and lower training intensity (30–33%).
- **Two dropped versions of earlier mechanisms:** subject-level routing, which misrouted 5–7 of 60 per world, and gate-held smṛti, which dismissed honest sources on real timelines.
- **A yes/no trace probe** (SE-4). The adapter answered name questions with names, so it never said yes, even to the truth. A likelihood probe replaced it.
- **A query budget of 10.** It let colluders in before their first check in one world. Asking trusted disputes first, with a budget of 40, fixed it.

## 6. Limits

- **Sources are simulated.** The SE-3 facts and timelines are real, but the honest, lagging, stealthy and colluding sources are simulated.
- **The registry is an oracle.** It is Wikidata, consulted as one, and real registries can be wrong or slow.
- **Shared facts across worlds.** SE-3's 8 main worlds share one pool of facts. The confidence intervals cover stream variation, not fact sampling.
- **Knowledge type.** The knowledge is entity-centric facts named in the question. Not yet tested: indirect references, multi-hop use, skills and procedures, sybil attacks with many fake sources, and horizons beyond 12 sessions.
- **Baselines.** The baselines are naive continual fine-tuning and simple gates.
  - Not run: retrieval into the prompt behind the same gate, and dedicated knowledge editors (MEMIT, AlphaEdit, WISE, GRACE).
  - For simple facts, retrieval behind this gate would likely match the weights. The gate is the part that transfers to any memory.
- **Novelty.** Each component has an ML counterpart. What is new is one coherent, preregistered rule set for what may enter memory, what overrides what, when to ask, and where knowledge applies. Each rule was measured at three scales.

## 7. Reproducing

- **Code:**
  - `claude_lab/cl/se{1,2,3}_world.py` (standard library; worlds and gates);
  - `claude_lab/cl/se{1,2,3}_modal.py` (Modal GPU runners);
  - tests under `claude_lab/tests`.
- **Data:** the Wikidata snapshot and probes are in `claude_lab/data/wikidata-changes`, with SHA-256 in `SOURCE.md`.
- **Records:** for each experiment, the spec, preregistration with frozen hash, run directories and result are in `claude_lab/docs` and `claude_lab/runs`. That includes every dev run and amendment.

## 8. Next

1. **SE-5:** sybil swarms and Nyāya's āpta rule, with a learner ([design note](SE5-SPEC-2026-10-18.md)).
2. **Retrieval memory with weaker models,** where a raw memory should fare worse than with a frontier reasoning model.
3. **Scale and harder tests:** thousands of facts, longer horizons, indirect and multi-hop questions, sybil attacks, and knowledge-editor baselines.
