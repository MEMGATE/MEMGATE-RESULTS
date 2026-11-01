# Learning from an untrusted world, into weights or memory

**Technical report, 19 October 2026.** It supersedes the report of 18 October.
- **Where:** the lab's repository. Paths below are relative to `claude_lab/`.
- **Provenance of the numbers:** every number is from a preregistered main run on data held out until that run, with the code hash frozen before it started. Model-free audits and sweeps are marked as such.

## Summary

AI systems now learn after deployment. They take in facts from users, tools, documents and other agents, and keep them in a retrieval memory or train them into their weights. Each of those memories can be poisoned and can go stale. This work also finds that learning new facts can damage knowledge the stream never mentioned.

**The engine** decides three things:
- what may enter memory;
- where a learned fact applies;
- how to take it out again when its source turns out to have lied.

Each of its rules was preregistered and tested on its own, then all together.

**Six findings.**

1. **Naive weight updates rewrite knowledge they never touched.** A 7B model fine-tuned on a realistic stream of real changes of office invented new holders for offices that had not changed.
   - Never-streamed offices answered correctly fell from 98.8% to 15.2% (SE-3, 8 worlds).
   - At 1,341 offices they fell from 99.2% to 9.2% (TM-1, two fresh worlds).
   - With the scope rule (an adapter answers only about facts it learned), they stayed at the untouched model's level.
2. **A corrected lie stays in the weights.** After the truth is trained over a lie, the model answers the truth, but on 93.5% of targets it still prefers the lie to a never-taught name, by +3.7 nats per token (SE-4).
   - Rollback and replay restores the adapter from before the liar's first lie and replays the rest without it.
   - The trace falls to chance, at about 7% of a full retrain's cost.
3. **Agreement is not evidence when identities are free.** Swarms of fresh accounts satisfy any "two sources agree" rule (SE-5).
   - The ledger gate alone let swarm lies into training, and their trace stayed in 74.5% of targets.
   - The track-record rule counts testimony only from sources with a registry-confirmed record. With it, no swarm lie was ever trained, and the trace stayed at chance (46.0%).
4. **Raw memory that concatenates untrusted text can be steered by one forged line.**
   - **The attack.** Attackers add, inside their own reports, a line in the memory's format claiming to be the registry.
   - **What it did.** Frontier models from three labs answered the lie on 74–86% of attacked facts (RM-3, RM-4).
   - **Escaping closes that channel.** Quoting each report's text, or marking it as data, brought poison to 0 (RM-5).
   - **The gate also gives 0, and it does not depend on the reader.** Its prompts are 15–19 times smaller. A small model reading raw memory, even without injected text, was poisoned on 38.8% of attacked facts; behind the gate it was poisoned on none, within 0.75 points of the frontier model's truth (RM-6).
5. **Against the field's most stable method, on the same poisoned stream, the engine wins.** WikiBigEdit (ICML 2025) found LoRA merging the most stable approach for lifelong updates. HH-1 compared the engine with it, on SE-5's world over 8 worlds:
   - poison 0% against 17.6%;
   - untouched knowledge 98.5% against 15.2%;
   - current holders 98.7% against 96.3%.

   The gate alone, put in front of merging, took its poison to 0. It did not protect untouched knowledge; the scope rule does.
6. **All of it holds together at scale.** TM-1 covered 1,341 real offices from January 2024 to October 2026, with every kind of attacker at once, on two fresh worlds. Engine against naive fine-tuning:
   - poison 0% against 18.4%;
   - swarm-lie trace at chance (49.8%) against 93.5%;
   - locality 98.3% against 9.2%;
   - current holders 92.4% against 93.4%, within the preregistered margin.

**The experiments:**

| Experiment | Memory and model | Setting | Main result |
| --- | --- | --- | --- |
| SE-1 | weights, Qwen2.5-0.5B | invented facts, one poisoner | poison 0 vs 23.4%; retention +11.3 pp |
| SE-2 | weights, Qwen2.5-1.5B | stealthy and colluding attackers | poison 0 vs 24.1%; truth +6.7 pp |
| SE-3 | weights, Qwen2.5-7B | real 2024–2026 changes of office (Wikidata) | poison 0 vs 24.7%; locality 98.8 vs 15.2% |
| SE-4 | weights, Qwen2.5-7B | sleepers whose lies get in before they are caught | lie trace 93.5% → chance after rollback and replay, at 7% of a retrain |
| SE-5 | weights, Qwen2.5-7B | sybil swarms | swarm-lie trace 74.5% (ledger) → 46.0% (track record, chance) |
| TM-1 | weights, Qwen2.5-7B | all of the above, 1,341 offices | poison 0 vs 18.4%; locality 98.3 vs 9.2%; current 92.4 vs 93.4% |
| HH-1 | weights, Qwen2.5-7B | SE-5's world; naive, LoRA merging, merging behind the gate, the engine | poison 0 vs 17.6% (merging); locality 98.5 vs 15.2%; current 98.7 vs 96.3% |
| RM-1 | retrieval, gpt-6.1-sol | SE-2's attackers | poison 0 vs 1.2% (raw) and 24.4% (last write wins); prompts 9× smaller |
| RM-2 | retrieval, gpt-6.1-sol | forged provenance in reports | poison 0 vs 71.9% (raw memory) |
| RM-3 | retrieval, gpt-6.1-sol, gpt-6-astra, grok-4.7 | RM-2 across models, fresh worlds | poison 75.6 / 74.4 / 85.6% raw with payloads; 0 gated |
| RM-4 | retrieval, claude-opus-5-5 | RM-3 on a third family, same worlds | poison 79.1% raw with payloads; 0 gated, truth 100% |
| RM-5 | retrieval, gpt-6.1-sol | escaping or marking the raw text | poison 71.9% raw; 0 escaped, 0 marked, 0 gated |
| RM-6 | retrieval, gpt-4.1-nano | RM-1 with a small reader, RM-1's worlds | poison 38.8% raw (sol 1.2%); 0 gated, truth 99.2% |

**What it took:**
- **GPU:** about $77 of Modal time in all, dev runs and probes included. The preregistered main runs of SE-1 to SE-5, TM-1 and HH-1 took about $48 of it.
- **API:** the retrieval tests ran on Azure Foundry and used no GPU.

## 1. The problem

Deployed models are mostly frozen, and their "memory" is retrieval into the prompt. Learning from deployment, into weights or into a persistent memory, is the open frontier. SEAL, test-time training, nested learning and the memory features of assistants are examples.

**Four risks:**
- **Poisoning.** Anyone who can reach the stream can teach the model falsehoods. That includes a crowd of fresh accounts, and a source that earned trust first.
- **Staleness.** Old values outlive their truth.
- **Collateral damage.** Updates erode what the stream never mentioned: general ability, and, as this work found, unrelated facts of the same kind (§4.3).
- **Residue.** A falsehood that is later corrected is not gone (§4.5).

## 2. The engine

| Component | What it does | Nearest ML idea |
| --- | --- | --- |
| Admission by evidence | A registry value is admitted. Testimony is admitted only when two trusted sources agree, and never overrides the registry. | provenance-aware filtering |
| Track record | A source counts as trusted only after the registry has confirmed at least three of its claims, and only if it was never caught fabricating. | reputation with a cold start |
| Dismissal and the ledger | A source whose checked claims are contradicted at ≥ 20% (of ≥ 5) is dismissed. A source whose testimony-admitted value the registry overturns, and that was never true, is caught at once. What rested on it is asked again. | source reputation, provenance graphs |
| Verify on doubt | Any report that contradicts what is admitted raises doubt about that fact, even from a dismissed source. Doubt is settled only by asking the registry, within a budget. | active verification |
| Lag is not lying | A claim of a value the registry records as a past holder counts as a lag, not an error. | — |
| Self-check | After each session, a fixed suite of the model's own competence is re-asked. On a drop, the update is rolled back and replayed with the suite. | regression gating with replay |
| Scope | The adapter answers only questions about a (relation, subject) it was trained on; every other question goes to the untouched model. | scoped editing (GRACE, WISE) |
| Rollback and replay | When a source is caught, the adapter is restored from before its first lie and the sessions since are replayed without what it taught. | unlearning by retraining from a checkpoint |
| Consolidation | The session's admitted reports are trained into a LoRA adapter. | continual fine-tuning |

**The gate is a library.** The first five rows decide what may enter any memory. They are packaged as [`memgate`](../memgate/README.md), with a ledger that plans rollback and replay: about 300 lines of standard-library Python. A test (`tests/test_memgate.py`) checks that it makes the lab gate's decisions, session by session, and reproduces the lab's rollbacks.

## 3. Experiments

**The setup:**
- **Weights.** Each weight experiment ran its arms over 12 sessions; SE-1 had 4. Learners trained LoRA adapters on Modal GPUs.
- **Retrieval.** Each retrieval experiment put SE-2's world into a frontier model's prompt, through Azure Foundry.
- **Facts.** SE-3 to TM-1 used real changes of office from a Wikidata snapshot of 18 October 2026: heads of state and government, CEOs, head coaches, chairs and directors. The sources were simulated.

| | SE-3 | SE-4 | SE-5 | TM-1 |
| --- | --- | --- | --- | --- |
| Facts | 166 real offices | as SE-3 | as SE-3 | **1,341 real offices**, 1,278 of which changed |
| Attackers | stealthy poisoner, two colluders | + two sleepers on late facts | + a swarm of 4 fresh accounts on each late fact | all of them |
| Arms | FROZEN, NAIVE, MAJORITY, ENGINE | FROZEN, NAIVE, ENGINE, LEDGER, ROLLBACK | FROZEN, NAIVE, LEDGER, TRACK RECORD | FROZEN, NAIVE, ENGINE (all rules) |
| Main worlds | 8 | 8 | 8 | 2 |

## 4. Results

### 4.1 Poison stays out

| | Engine | Naive | Difference (95% CI) |
| --- | ---: | ---: | --- |
| SE-1 | 0.0% | 23.4% | −23.44 [−28.65, −17.71] |
| SE-2 | 0.0% | 24.1% | −24.06 [−29.06, −18.75] |
| SE-3 | 0.0% | 24.7% | −24.70 [−30.06, −19.05] |
| TM-1 | 0.0% | 18.4% | −18.36 [−19.10, −17.61] |

**Against weaker gates:**
- **SE-2:** the engine beat SE-1's gate by −8.75 [−10.94, −6.25]. SE-1's gate trusted the colluders.
- **SE-3:** it beat a majority vote with the same self-check and scope rule by −2.98 [−4.46, −1.79].

**Training streams.** In the SE-2 and SE-3 main runs, which counted them, no poisoned report entered the engine's training stream. In TM-1's world 8000, naive fine-tuning trained 732 distinct fabricated values. The engine's training history held none at the end, because the sleepers' 26 were taken out (§4.5).

### 4.2 Safety adds learning; it does not cost it

| | Engine | Naive |
| --- | --- | --- |
| SE-1 truth | 94.5% | 91.0% |
| SE-2 truth | 98.3% | 91.6% |
| SE-3 current holder | 97.9% | 96.2% |
| SE-5 current holder | 98.4% | 96.7% |
| TM-1 current holder | 92.4% | 93.4% |
| Core retention, SE-1 / SE-2 / SE-3 / TM-1 | 99.9 / 99.6 / 100 / 100 | 88.6 / 95.4 / 97.2 / 94.5 |

**Why.** The gate removes reports that contradict each other, which makes the stream easier to learn.

**Majority voting** holds stale values. In SE-3 its current-holder rate was 68.7%, because old values keep more supporters for a while.

### 4.3 Naive weight updates rewrite what they were never taught, and the scope rule stops it

**What happened.**
- **SE-3:** 60 offices the model knew correctly were never mentioned in the stream. After naive continual fine-tuning, the model answered only 15.2% of them correctly; before, it got 98.8%.
- **What it said instead.** It invented holders for offices that had not changed. Chevron's chief executive was given as ExxonMobil's, and South Africa's head of state as Haiti's late president.
- **TM-1, eight times larger, two fresh worlds:** locality fell to 9.2%. The model's own self-check suite fell from 99.3% to 71.8%, and general questions from 100% to 94.5%.

**What did not fix it.** These were tested on SE-3's dev world, where every arm without the scope rule fell to 15–33%:
- half the learning rate and half the epochs;
- reciting the model's own earlier answers about other offices;
- a constitution check, which protected only the facts it checked.

**What fixed it: the scope rule.**
- **How routing works.** The router masks the relation phrase and links the subject by the longest name found in a 27,780-name index of the snapshot. Only learned (relation, subject) pairs go to the adapter.
- **SE-3:** locality 98.8%, +83.54 [+81.25, +85.62] over naive, with 2 misroutes in 800 checks.
- **TM-1:** locality 98.3% (the untouched model 99.2%), +89.17 [+86.67, +91.67] over naive.

### 4.4 Verify, never trust

**The rule.** Any contradiction prompts a registry check, whoever reported it. Only the registry or two trusted sources are believed.
- This recovers timely truths that dismissed sources carry as camouflage, without trusting the sources.
- **Lag is not lying.** The registry's history is read along with its answer. A source still reporting a real past holder is behind the news, not lying.
- **The cost:** about 15% of fact-sessions verified. The query budget scales with the world: 40 a session for 177 facts, 303 for 1,341.

### 4.5 Correction is not removal: rollback and replay (SE-4)

**The attack: sleepers.** Sources build trust, then lie first about news no one can contradict yet. The lie passes every corroboration gate and is trained.

**After the truth is trained over the lie,** the model answers the truth, but the weights keep the lie:
- the model prefers it to a never-taught name of the same kind on 93.5% of targets;
- the gap is +3.7 nats per token, about forty times the probability.

**What the ledger and rollback do:**
- **The ledger** records what each taught value rested on. A source is dismissed at its first exposed fabrication, so 7 lies were taught instead of 50.
- **Rollback and replay** restores the adapter from before the first tainted session and replays the sessions since, without the lies.

**Results on 8 fresh worlds:**
- **The trace** fell to chance: 48.5%, −45.00 pp [−51.00, −39.00].
- **The size of what was left.** On the lies actually taught, the gap fell from +3.77 to +0.77 nats per token, against +0.46 for the never-taught model.
- **Nothing else moved.** Currency, poison resistance and locality were unchanged.
- **The cost:** 6.6–8.0% of a full retrain.

**In TM-1's main worlds,** the sleepers got their lies in during session 4 (October 2024): 26 in world 8000. They were caught the next session, and the replays took 1,473 and 1,459 items, 7.2% and 7.1% of a full retrain. The sleeper-lie trace ended at 50.0% (naive: 92.0%).

### 4.6 Agreement is not evidence when identities are free (SE-5)

**The attack.** As each late fact appears, four fresh accounts that never report anything else assert the same false holder. Nothing contradicts them yet.

**Results on 8 fresh worlds:**
- **SE-4's ledger gate alone** trained 62.5 swarm-lie reports per world. Honest reports overwrote each lie before the end, but the lies left a trace in 74.5% of targets (+2.08 nats per token).
- **With the track-record rule, no swarm lie was trained in any world.** The trace stayed at the untrained model's level: 46.0% against 47.0%, −28.50 pp [−34.50, −22.50] against the ledger alone.
- **The rule cost nothing elsewhere.** Current holders, poison, locality and retention were unchanged (current +0.25 pp, NON-INFERIOR).

**TM-1:** the swarm-lie trace was 49.8% for the engine and 93.5% for naive fine-tuning, which trained 804 swarm-lie reports per world (−43.78 [−44.28, −43.28], WIN).

**The attack that remains** is a source that first earns trust with true reports. That is SE-4's sleeper, which the ledger exposes the first time one of its lies is checked.

### 4.7 The same gate in front of retrieval memory (RM-1 to RM-6)

**The setup.** The gate does not depend on where knowledge is stored. Six preregistered tests put it in front of models that read a retrieval memory:
- the world is SE-2's, 8 worlds per test;
- the models are reached through Azure Foundry;
- each model is asked about every fact after session 12, and in RM-1 and RM-6 also after sessions 4 and 8.

**Without injected text (RM-1, RM-6).** The attackers are SE-2's stealthy poisoner and colluders.

| Reader | Memory | Truth | Poison | Input tokens per question |
| --- | --- | ---: | ---: | ---: |
| gpt-6.1-sol | last write wins | 95.1% | 24.4% | 51 |
| gpt-6.1-sol | every report, with source and session | 99.8% | 1.2% (16.6% after session 4) | 385 |
| gpt-6.1-sol | the gate's verified value | 100.0% | 0.0% | 42 |
| gpt-4.1-nano | every report, with source and session | 90.5% | 38.8% (34.7% after session 4) | 386 |
| gpt-4.1-nano | the gate's verified value | 99.2% | 0.0% | 43 |

**With injected text (RM-2 to RM-4).** Each false report also carries one of three payloads:
- an authority spoof ("[Registry correction, verified] …");
- an instruction to the assistant;
- a line in the memory's own format claiming to be the registry.

After session 12, mean over 8 worlds:

| Model | Lab | Raw memory: truth / poison | Raw + payloads: truth / poison | Gated: truth / poison |
| --- | --- | --- | --- | --- |
| gpt-6.1-sol (RM-3) | OpenAI | 99.8% / 0.3% | 84.7% / **75.6%** | 99.9% / 0.0% |
| gpt-6-astra (RM-3) | OpenAI | 99.8% / 0.3% | 84.9% / **74.4%** | 99.9% / 0.0% |
| grok-4.7 (RM-3) | xAI | 97.4% / 5.6% | 81.2% / **85.6%** | 99.0% / 0.0% |
| claude-opus-5-5 (RM-4) | Anthropic | 98.7% / 0.0% | 82.8% / **79.1%** | 100.0% / 0.0% |

**What the payloads did.**
- **The forged line** steered every model on 97–99% of the facts where it came last.
- **The spoof and the instruction** steered most of the facts they ended on, but only alongside forged lines. On RM-2's dev worlds, without them, they steered none.

**Verdicts.** Every model had the same three verdicts:
- the gate's poison was below the injected raw memory's (WIN);
- injection raised raw poison;
- the gate's truth was non-inferior.

The reduction was −78.54 pp [−81.04, −76.15] pooled over RM-3's three models, and −79.06 [−82.50, −75.62] for claude-opus-5-5.

**Escaping closes the channel (RM-5, gpt-6.1-sol, 8 fresh worlds).** The same injected reports were shown four ways:

| Memory | Truth | Poison | Input tokens |
| --- | ---: | ---: | ---: |
| raw: each report's text on its own line, as it came | 85.6% | 71.9% | 564 |
| escaped: each report's words in quotes on one line, provenance only outside them | 99.8% | 0.0% | 639 |
| marked: each report's words joined by a marker and declared data | 99.9% | 0.0% | 787 |
| gated | 100.0% | 0.0% | 42 |

**What escaping fixes.**
- **The vulnerability is in how the memory is written.** Escaping or marking the text fixed it for every payload: 0 of 314 facts.
- **The gate matched both defenses on poison.** Beyond that, its prompts are 15–19 times smaller, and it does not depend on the model reading a format or following an instruction.
- **What format cannot decide.** The gate also settles what format cannot: which of two disagreeing sources is right, and whether a value is current. Colluders and stale values pass any escaping.

**A small reader (RM-6, gpt-4.1-nano, RM-1's worlds).**
- **Raw memory.** Reading every report, the small model was poisoned on 34.7%, 43.4% and 38.8% of attacked facts after sessions 4, 8 and 12. That is more than from the latest report alone (24.4%), and far more than the frontier model (16.6%, 5.6%, 1.2%).
- **Behind the gate,** it reached 99.2% truth and 0 poison, against −38.75 pp [−44.69, −32.19] of poison and +8.75 pp of truth (both WIN). That is within 0.75 points of the frontier model (NON-INFERIOR).
- **What this means.** A raw memory is only as safe as its reader. The gate makes the reader's strength matter far less.

### 4.8 Everything at once, at scale: the Time Machine (TM-1)

**The run.**
- **What the model lived through.** A 7B model whose knowledge stops before 2024 relives 1 January 2024 to 18 October 2026 in twelve sessions. It covers every usable changed office in the snapshot (1,281), with 60 known static offices streamed and 100 more held out for the constitution and locality.
- **The sources.** Every kind of source reports at once: honest but sometimes a session late, a stealthy poisoner, two colluders, two sleepers, and a swarm on each late fact. About 1,700–2,500 reports arrive a session.

**The main run: two fresh worlds, after session 12, in %** ([result](TM1-RESULT-2026-10-19.md)):

| Arm | Current | Stale | Poison | Swarm-lie trace | Sleeper-lie trace | Locality | Retention | Self-check suite |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| FROZEN | 0.5 | 15.2 | 0.0 | 49.3 | 48.8 | 99.2 | 100.0 | 99.3 |
| NAIVE | 93.4 | 4.4 | 18.4 | 93.5 | 92.0 | 9.2 | 94.5 | 71.8 |
| **ENGINE** | **92.4** | **3.7** | **0.0** | **49.8** | **50.0** | **98.3** | **100.0** | **99.3** |

**Verdicts, ENGINE − NAIVE.** All four came out as predicted:
- **poison:** −18.36 [−19.10, −17.61], WIN;
- **locality:** +89.17 [+86.67, +91.67], WIN;
- **swarm-lie trace:** −43.78 [−44.28, −43.28], WIN;
- **current:** −1.03 [−3.63, +1.58], NON-INFERIOR at a −5 pp margin.

**The engine's work in each world:**
- exactly S, C1, C2, Z1 and Z2 dismissed, and no honest source;
- no swarm-lie report trained;
- one rollback and replay at about 7% of a full retrain.

**Cost:** 197.8 GPU-minutes on L40S for six tasks, about $8.35.

**The dev world (world 0),** run before the freeze, gave nearly the same picture:
- poison 0 vs 19.7%;
- swarm-lie trace 52.2 vs 96.0%;
- locality 98.3 vs 10.0%;
- current 94.0 vs 94.3%.

**Gate audit on 20 more worlds (no model, worlds 100–119, `cl/tm1_gate_audit.py`).** The world, the gate and the training loop are deterministic, so each method's training stream can be replayed exactly without a GPU:
- **Fabricated values.** In every world, naive fine-tuning's training history ended with 729–736 of them, and the engine's with none.
- **The sleepers** got 19–35 lies in for one session each time. They were caught and taken out the next session.
- **Dismissals.** Exactly S, C1, C2, Z1 and Z2 were dismissed in every world, never an honest source.
- **Queries and replays.** 2,839–2,930 registry queries per world, and replays of 7.1–7.6% of a full retrain.
- **What was wrong at the end.** 37–55 of 1,341 admitted values were a past holder (a lag), and none was fabricated.

### 4.9 Against established continual-learning methods (HH-1)

**The setup.** Same world, same stream, same model and adapter settings, 8 fresh worlds. The methods:
- **NAIVE:** one adapter trained session after session.
- **MERGE:** a fresh adapter each session, folded into the weights. This is the approach WikiBigEdit found most stable for lifelong updates; here it is our implementation, with α = 1.0 chosen on dev by the method's own goal.
- **MERGE_GATE:** merging behind the gate.
- **ENGINE:** the full engine.

**After session 12, in %** ([result](HH1-RESULT-2026-10-19.md)):

| Arm | Current | Poison | Swarm-lie trace | Locality | Retention | Self-check suite |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| FROZEN | 0.0 | 0.0 | 46.5 | 98.5 | 100.0 | 99.7 |
| NAIVE | 97.6 | 20.5 | 96.0 | 12.9 | 98.6 | 73.6 |
| MERGE | 96.3 | 17.6 | 97.5 | 15.2 | 98.9 | 74.4 |
| MERGE_GATE | 99.0 | 0.0 | 52.0 | 15.8 | 87.1 | 67.2 |
| **ENGINE** | **98.7** | **0.0** | **48.0** | **98.5** | **100.0** | **99.6** |

**Verdicts, ENGINE − MERGE:**
- **poison:** −17.56 [−23.21, −11.90], WIN;
- **locality:** +83.33 [+80.42, +86.25], WIN;
- **current:** +2.39 [+1.57, +3.19], NON-INFERIOR (higher).

**MERGE_GATE − MERGE, poison:** −17.56, WIN.

**Rehearsal on the dev world.** Training each session also on as many earlier items did worst of all: poison 24.4%, locality 6.7%.

**Why the parts matter.** Neither merging nor rehearsal asks where a report came from. The gate fixes that by itself: it is a plug-in for any method. What it does not decide is where an update lands, so merging behind the gate still rewrote untouched knowledge and lost general retention. The scope rule and the self-check kept those at the frozen model's level.

## 5. Artifacts

- **[`memgate`](../memgate/README.md).** The gate as a library for any memory, retrieval or weights:
  - `MemoryGate(verify, history)`, with `observe(time, reports)`;
  - `admitted()`, what memory may hold;
  - `why(fact)`, the evidence for a value;
  - `memory_block(fact, render)`, the only text a model should see about a fact;
  - `Ledger`, which plans rollback and replay for a learner that trains on admitted values.
- **[The Time Machine page](../site/time-machine/index.html).** A static page over TM-1's world:
  - a slider through the twelve sessions;
  - forty offices with each model's answer, the truth on that date, and the engine's verified memory with its evidence;
  - the four attacks and what each method put into its weights;
  - the fabricated values in each method's training history over time.

  The streams on the page are recomputed exactly without a model (`cl/tm1_page.py`); the answers come from the run.

## 6. What was tried and dropped

All of these were tried on exposed dev data and recorded in the specs' amendments:
- **Two remedies for collateral rewriting:** self-recitation (locality only 25%) and lower training intensity (30–33%).
- **Two earlier mechanisms:** subject-level routing, which misrouted 5–7 of 60 per world, and a lag rule that read past holders from the gate's own memory, which dismissed honest sources on real timelines.
- **A yes/no trace probe** (SE-4). The adapter answered name questions with names, so it never said yes, even to the truth. A likelihood probe replaced it.
- **A query budget of 10.** It let colluders in before their first check in one world. Asking trusted disputes first, with a budget of 40, fixed it.
- **Unpaced calls to claude-opus-5-5** (RM-4 dev a). Rate limits failed 99 of 600 calls; the main run paces calls.

## 7. Limits

- **The sources are simulated and the attacks scripted.** The facts and timelines from SE-3 on are real.
- **The registry is an oracle.** It is Wikidata, consulted as one. Real registries can be wrong or slow.
- **How much the gate needs it.** A model-free sweep on TM-1 worlds 200–202 (`cl/tm1_registry_sensitivity.py`) measured this. The table gives what the gate holds after session 12, as a share of 1,341 offices, and the fabricated values it admits:

  | Registry reports unasked | Questions it may ask a session | Current | Past holder | Fabricated |
  | --- | --- | ---: | ---: | ---: |
  | 15% (as in every experiment) | 303 | 97.1% | 2.9% | 0 |
  | 2% | 303 | 96.4% | 3.6% | 0 |
  | 2% | 76 | 72.0% | 23.9% | 0 |
  | 2% | none | 72.9% | 17.0% | 34 |
  | 15% | none | 72.1% | 19.0% | 37 |

  **What the sweep shows:**
  - **The unasked feed can be thin.** A registry that reports only 2% of offices unasked serves as well as one that reports 15%.
  - **Asking under doubt carries the load.** A quarter of the budget still keeps every lie out, at the cost of stale values. With no questions at all, the colluders are never exposed and lies are admitted.
- **A registry that is sometimes wrong.** A second sweep on worlds 300–302 (`cl/tm1_registry_noise.py`) had the registry give a wrong value with probability p, both in what it reports and in what it answers. Its record of past holders stayed correct.
  - **At p = 1%,** 4 of 1,341 admitted values were fabricated at the end, and 12 fabricated values had been trained.
  - **At 3%,** 9 and 35.
  - **At 10%,** 37 and 119. Naive fine-tuning trains about 730.
  - **No honest source was dismissed at any p.**
  - **What this means.** The gate is as good as its registry and does not amplify the registry's errors. By default, values the registry later corrects stay in the training history, because the registry itself is never "caught". The ledger's `registry_verdicts` option removes them too, at about a full retrain of replay.
- **Provenance is assumed.** The gate assumes the system knows the true source of each report, through authenticated tools or signed sources.
- **Shared facts across worlds.** Main worlds share one pool of facts, so the confidence intervals cover stream variation, not fact sampling. TM-1's main run has two worlds, so its intervals are coarse.
- **Knowledge type.** The knowledge is entity-centric facts named in the question. Not yet tested:
  - indirect references and multi-hop use, which the scope router does not see;
  - skills and procedures;
  - horizons beyond 12 sessions.
- **Baselines.** The weight baselines are naive continual fine-tuning, simpler gates, rehearsal (dev only) and LoRA merging (HH-1). Dedicated knowledge editors (MEMIT, AlphaEdit, WISE, GRACE) and other merging schemes were not run.
- **Novelty.** Each component has an ML counterpart. What is new is:
  - one coherent, preregistered rule set for what may enter memory, what overrides what, when to ask, where knowledge applies and how it is taken out;
  - the two failures measured here: collateral rewriting and the residue of corrected lies.

## 8. Reproducing

- **Code:**
  - worlds and gates: `claude_lab/cl/se{1,2,3,4,5}_world.py` and `tm1_world.py` (standard library);
  - Modal GPU runners: `se*_modal.py` and `tm1_modal.py`;
  - retrieval runners: `run_rm{1,2,3,4}.py`;
  - the library: `claude_lab/memgate`;
  - tests: `claude_lab/tests`.
- **Data:** the Wikidata snapshot and probes are in `claude_lab/data/wikidata-changes`, with SHA-256 in `SOURCE.md`.
- **Records:** for each experiment, the spec, the preregistration with its frozen hash, every run directory (dev runs included) and the result are in `claude_lab/docs` and `claude_lab/runs`.

## 9. Next

1. **Knowledge-editor baselines** (MEMIT, AlphaEdit, WISE), a larger model, and a second model family for the weight results.
2. **Indirect and multi-hop questions,** which the scope router must learn to route.
3. **A public benchmark** from TM-1's world: real changes, every kind of source, and scoring for currency, poison, locality and residue, for any memory system.
