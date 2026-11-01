# What the Sanatana knowledge tests show (as of 18 October 2026)

This summarises 67 preregistered experiments (31 when first written; RP-1, SL-1, RS-1, MX-3, MX-4, ML-6, ML-7, SK-1, AR-1, MX-5, JY-2, AR-2, MX-6, PN-2, ST-1, SL-2, MX-7, MX-8, MX-9, MX-10, MX-11, MX-12, MX-13, SE-1, SE-2, SE-3 and SE-4 were added on 18 October, RM-1, RM-2, SE-5, RM-3, RM-4, RM-5, RM-6, TM-1 and HH-1 on 19 October) in `claude_lab/`. K-1 (exploratory) and ML-3 (suspended) are not counted.

Every experiment followed the same discipline:
1. a spec before code;
2. a dev run on exposed data;
3. a freeze with a code hash;
4. one main run on data no learner had seen;
5. a result written whatever it showed.

Per-experiment details are in the [README](../README.md) table. The [coverage register](COVERAGE-REGISTER.md) tracks every source family.

## 1. What holds, and how often it replicated

**An assembly of different kinds of knowers** (Manusmṛti 12.110–112, the pariṣad).
- **Result:** three learners of different kinds (a lesson learner, naive Bayes, a decision tree) deciding by plurality beat the lesson learner alone.
- **Replications:** P-1 +1.44 pp, P-2 +1.60, MX-1 +1.21, PV-1 +1.17 (descriptive), all on different fresh pools. With a language model as a member, the assembly lifted the model by +5.67 (ML-4) and +1.72 (ML-5).
- **What fails:** an assembly of near-identical members (P-1); five members instead of three (P-2: −0.50); one "learned" member overruling the others (PV-1, Manu 12.113: −0.67).

**Knowing where one knows, and asking only under doubt** (kṣetrajña, Gītā 13; jijñāsā).
- **Asking:** a learner or assembly that asks for the true label only when it doubts beat random asking at the same number of labels. JK-1 +3.69 pp, PV-1 +3.94, MX-2 +3.19.
- **Labels saved:** with about 22% (one learner) to 55% (assembly) of the labels, it matched learners that saw every label.
- **Answering:** answers given only where a lesson decides were +7.08 pp more accurate than as many random answers (JK-1). Answers given only when the assembly is of one mind were +7.88 more accurate (MX-2). Unanimity was the better sign (+2.23).
- **The limit:** knowing where one knows is good for asking and abstaining, not for overruling others (PV-1).

**A known symmetry of the world** (the kolam's grid symmetry).
- **Board:** learning also from each case's mirror image won on a fresh board (K-2: +2.14 pp).
- **Physical world:** it helped every learner in a physical world (K-3: +0.78 for the lesson learner, +1.03 WIN for naive Bayes).
- **Size:** the gain is largest where the symmetry is exact.

**Change in the world** (Kālacakra; Caraka's prakṛti and vikṛti; yuga ageing).
- **Kālacakra recency layers** win when the rules change (T-1: +1.04 pp).
- **The prakṛti–vikṛti health check** detects an abrupt change. A reset at the diagnosed moment beat a reset at a random moment by +5.59 pp (PK-2).
- **On real streams,** neither ageing weights nor resets are a general gain (Y-1, PK-2). Recency is a tool for change, not a default.

**How a lesson can name its conditions** (Pāṇini 1.1.71; Mīmāṃsā and Nyāya on absence and error).
- **Pratyāhāra:** a contiguous stretch of ordered values in a single literal won (PN-1: +1.19 pp). Ordinary thresholds did as well.
- **Gaṇa (PN-2):** pooling a many-valued feature's values into classes by their behaviour gave +0.35 pp (NO WIN, significant), and beat random pooling.
- **Small but repeatable gains:** treating a missing value as observed absence (anupalabdhi: +0.34, +0.45), and not revising a lesson on a counterexample indiscernible from a case it explained (akhyāti: +0.61).

**Several different sources, and dismissing the one that frequently differs** (Arthaśāstra 1.12).
- **Agreement:** three spies watching different sources (feature sets; chest, ankle and arm sensors) who agree, none guessing, were right 96–99.7% of the time (AR-1: +16.61 pp vs random).
- **Dismissal:** dismissing the spy that is the odd one in 20 of the last 30 splits restored credence after a source failed (+13.41 net credence, WIN). The right spy mattered (+9.78 vs a random one).
- **Detection:** the broken source was found in 36 of 40 runs, about 30 cases after the failure on real data.

**The supervisor: the pieces together** (MX-5, on a real hydraulic test rig with a failing sensor group).
- **The whole:** three-source agreement with dismissal and saṃskāra beat the plain agreement network by +13.14 pp net credence. On the rig's cooler grades it answered alone 78% of cycles at 99.6%.
- **Inside the whole:** dismissal +11.82 (WIN) and saṃskāra +2.56 (WIN) earn their place.
- **Replicated on body-worn sensors (MX-7, PAMAP2):** dismissal +12.85 (WIN; the broken IMU found 10 of 10, none wrongly); supervisor +9.68 (WIN). Saṃskāra inside it did not replicate (+0.28).
- **A fourth setting (MX-8, Daily and Sports Activities):** supervisor +14.52 (WIN). Telling each spy the person added +1.38 (UNDETERMINED).
- **Two broken sources (MX-10): UNSAFE.** Dismissal is a one-culprit rule; with two culprits it never fires. Wrong answers alone rose to 2.00 per 100 (bound 2), while the share answered alone fell from 49.6% to 13.7%. **MX-11 tested that alarm.** Three-way disagreement checked by prakṛti–vikṛti caught 16 of 20 double failures and made the case SAFE (0.84 per 100). It was permanent once fired, so its rare false alarms cost (HARM by the strict rule). MX-10's UNSAFE was at the edge: without the alarm the rate is about 1–2 per 100. **An alarm that resumes on its own (MX-12) is cheap but no longer safe (1.78):** broken sources learn the commonest label while paused and stop disagreeing. The resume signal must be one a broken source cannot fake. **Verification against the owner's answers (MX-13) never erred (21 broken dismissed, 0 working), but errors still slip in before the alarm and after partial dismissals (1.97).** Taken together: two broken sources give about 1–2 wrong answers alone per 100 (0.6 when sound), and a permanent alarm cuts that by about a third.
- **The precondition again (MX-9, WISDM):** with 18 activities and 6 coarse features per source, nothing could be decided alone (coverage ≈ 0%). From now on, multi-source tests state a testability condition: the sound network must answer alone on at least 5% of cases.
- **The precondition (MX-6):** on a naval gas-turbine simulator, no single sensor group could decide the decay grade. The network answered ≤ 1.6% alone and the supervisor added nothing (+0.30, NO WIN). The recipe needs sources that can each decide often on their own.
- **Audits (−0.96) and resets (−1.00)** do not pay when a wrong answer costs twice a question. Resets do cut wrong answers given alone (−0.56). They pay if a confident mistake costs more than about 2.8 right answers; audits only above about 10.

**Latent impressions that return** (saṃskāra, Yoga Sūtra 4.8–4.9).
- **Result:** keeping a refuted lesson latent, and letting it return when its conditions again confirm it, won where the world returns to an earlier state (SK-1: +2.22 pp). It also gained +2.22 under label noise.
- **The bar:** three confirmations beat the two of the mapping (+0.66).
- **The cost:** true exceptions (EXC −1.28). The churn must be bounded on noisy streams.
- **On fresh real streams in time order it hurt (ST-1: −1.39 on all five).** Calendar and weather exceptions are true exceptions. Keep refuted lessons latent only where refutations are mostly noise.

**Transfer between analogous worlds** (upamāna with Indra's Net). Importing lessons by likeness works only when each imported lesson is checked against the target's own experience (A-1: +2.40 pp).

**The Gītā's three kinds of knowledge (18.20–22)** rank as the text says, on average (SR-8).
- Lessons that unify cases beat the nearest case by +1.71 pp, which beats the most frequent label by +15.93.
- The order flips on some datasets: very imbalanced data, and word counts.

**Evidence has a locus** (Kiraṇa 6; Nyāya pakṣadharmatā).
- Grouping cases by where they come from beat random grouping (SL-1: +1.04 pp WIN). **Replicated on fresh data (SL-2: +12.27 WIN).** With patients as loci, it beat the plain learner by +5.94 (66.9% → 90.9% on Parkinson's). With stations of one city it costs.
- Naming the locus as a feature helps.
- Withholding general lessons until confirmed locally costs (−0.76).

**Model-written lessons** beat model experience on synthetic worlds twice (ML-1: +3.84 pp; ML-2: +2.58). They did not on five small real datasets (ML-5: −1.97).

**Replication (RP-1, a tenth fresh pool, unchanged code).**
- **All six replicated:** jijñāsā +4.41 pp, kṣetrajña +5.89, the asking assembly +3.33, unanimity +6.66 (all WIN); range literals +0.96; the pariṣad +0.81 (positive, below the margin).
- **Most robust:** the effects about knowing and asking.
- **Smaller:** the pariṣad's gain, about +1 pp across five pools.

**Learning into the weights, safely (SE-1, the Saṃskāra Engine's first brick).**
- **Setting:** a small LLM (Qwen2.5-0.5B, LoRA) learning invented facts over four sessions of mixed reports.
- **Naive continual fine-tuning:** absorbed planted poison (23.4%), lost core ability (100% → 88.6%) and kept stale values.
- **The pramāṇa gate with a constitution check:** no poison, 99.9% core retention, more truth (+3.4) and more correct updates (+8.3), all on fresh worlds.
- **Limits:** a synthetic world and an easily caught poisoner. The next tests are stealthier poisoners, larger models and real task streams.

**Stealthy and colluding poisoners (SE-2).**
- **Setting:** Qwen2.5-1.5B over twelve sessions. One poisoner lies only about facts the registry never reports; two colluders assert the same false values, satisfying the two-source rule.
- **SE-1's gate was fooled:** 8.8% of poisoned facts were answered falsely.
- **SE-2's gate held, with no poison in any world.** It queries the registry when trusted sources dispute a fact (jijñāsā), and treats a value it once held as memory, not error (smṛti vs viparyaya, Yoga Sūtra 1.6–1.11). Results: −8.75 pp vs SE-1's gate, −24.06 vs naive.
- **Learning and retention:** it also learned more truth (+6.69) and kept more core ability (+4.25).
- **A plain majority vote still admits poison**, because colluders outnumber early honest reports.
- **Cost:** a short delay on changes to unverified facts (H5 −0.99, UNDETERMINED).

**The real world at 7B (SE-3).**
- **Setting:** real 2024–2026 changes of office from Wikidata, learned into Qwen2.5-7B-Instruct over twelve sessions. The model starts out believing the pre-2024 holders.
- **The engine on 8 fresh worlds:**
  - learned 97.9% of the current holders (naive 96.2%);
  - admitted no poison (naive 24.7%);
  - left untouched knowledge as it was (locality 98.8%; naive 15.2%).
- **A new failure of naive weight updates:** taught many changes, the model rewrites offices it was never taught. Lower learning rates, self-recitation and the constitution check did not stop it. Kiraṇa's locus rule did: knowledge applies only to the fact it was learned for.
- **The gate:** "verify, never trust". Any contradicting report, even from a dismissed source, prompts a registry check, and only the registry or two trusted sources are believed. Smṛti is read from the registry's history (YS 1.11).
- **Against a majority vote** with the same check and locus: poison −2.98 and current holders +29.3. Majority voting keeps stale holders.

**Removing what a late-caught source taught (SE-4, pratiprasava, YS 2.10).**
- **Setting:** sleepers build trust, then lie first about late news. Their lies pass any corroboration gate and are trained.
- **Correction is not removal.** Once the truth is trained over the lie, the model answers the truth but still prefers the lie to a never-taught name on 93.5% of targets (+3.7 nats per token).
- **The ledger gate** (the evidence graph) dismisses a source at its first exposed fabrication. 7 lies are taught instead of 50 (trace −39.00, WIN).
- **Pratiprasava** restores the adapter from before the first tainted session and replays without the lies:
  - the trace falls to chance (48.5%; −45.00, WIN);
  - it costs 7% of a full retrain;
  - currency and locality are unchanged.

**Sybil swarms (SE-5, āpta).** Fresh accounts that agree satisfy any counting rule.
- **The ledger gate alone** trained 62.5 swarm-lie reports per world, leaving a trace of 74.5%.
- **Nyāya's āpta rule** counts only sources the registry has confirmed. It kept every swarm lie out (trace 46.0%, chance level; −28.50, WIN), with currency unchanged.

**The same gate in front of retrieval memory (RM-1, RM-2; gpt-6.1-sol on Azure Foundry).**
- **A frontier reasoning model reading every provenance-tagged report** reached 99.8% truth and 1.2% poison when told that values change and sources lag.
  - It needed a prompt nine times larger.
  - It was poisoned on 16.6% of attacked facts early in the stream.
  - With a looser instruction it left 27.6% of changes stale.
- **The gated memory:** 100% truth, 0 poison.
- **Forged provenance breaks text memory.** One line in the memory's own format, claiming the registry, made the same model answer the lie on 71.9% of attacked facts (96 of 98 where it came last).
- **Naive injections** ("assistant, answer X") persuaded it on none.
- **The value gate takes provenance from structure** and passes only verified values: 0 poison (−71.88, WIN).

**Four frontier models, a defense, and a small reader (RM-3 to RM-6).**
- **The forged line works the same everywhere.** Read in raw memory, it steered gpt-6.1-sol, gpt-6-astra, grok-4.7 and claude-opus-5-5 (three labs) on 74–86% of attacked facts, 97–99% where it came last. Gated memory: 0 poison for every model (WIN each).
- **Escaping closes that channel (RM-5).** Quoting each report's words on one line, or marking them as data, brought poison to 0, the same as the gate. The vulnerability is memory that concatenates untrusted text unescaped.
- **The gate's own advantages:**
  - it does not depend on the reader;
  - its prompts are 15–19 times smaller;
  - it settles what format cannot: which source is right, and whether a value is current.
- **A small reader (RM-6).** gpt-4.1-nano reading raw memory was poisoned on 38.8% of attacked facts, against 1.2% for gpt-6.1-sol. That is more than from the latest report alone. Behind the gate it reached 99.2% truth and 0 poison, within 0.75 points of the frontier model.

**Against established continual-learning methods (HH-1, 8 fresh worlds).**
- **LoRA merging, the approach WikiBigEdit found most stable,** learned the changes (96.3%) but also 17.6% of the poison. It left 15.2% of untouched offices answered correctly.
- **The engine:** poison 0, locality 98.5%, current 98.7% (WIN, WIN, NON-INFERIOR).
- **The gate alone in front of merging** took poison to 0 but left untouched knowledge rewritten (15.8%). Admission and scope are separate jobs.

**The whole engine at scale (TM-1, two fresh worlds).**
- **The setup.** 1,341 real offices, January 2024 to October 2026, every attacker at once.
- **Engine against naive fine-tuning:**
  - poison 0 vs 18.4% (WIN);
  - swarm-lie trace at chance, 49.8 vs 93.5% (WIN);
  - locality 98.3 vs 9.2% (WIN);
  - current 92.4 vs 93.4% (NON-INFERIOR).
- **A replay of 20 more worlds without a model.** The engine's training history ended with no fabricated value every time, against 729–736 for naive fine-tuning. No honest source was dismissed.
- **What the gate leans on.** Sweeps showed it needs the ability to ask under doubt more than a rich unasked feed. A registry wrong 1% of the time let 4 of 1,341 wrong values through.

## 2. What does not hold

**Choosing among an assembly's members instead of letting them vote** (Arthaśāstra 1.10, AR-2; Jyotiṣa, JY-2).
- **Local competence (AR-2):** giving each case to the member proved on the most similar past cases gave −0.25 pp vs plurality, and −0.49 vs the best member overall.
- **The pattern:** three different members voting equally are hard to beat by ranking or selecting them (also P-1, PV-1).

**Ranking an assembly's members by Jyotiṣa's fivefold friendship** (Bṛhat Jātaka II.15–18; JY-2).
- **Result:** five grades from long-run and recent standing, used as vote weights, gave +0.04 pp over equal votes (NO WIN).
- **Where it helps and hurts:** it helps on exception rules and after a switch, and hurts under label noise.

| Reading | Experiment | Result |
| --- | --- | --- |
| Rule-arbitration doctrines as lesson policies: upādhi, saṃśaya, satpratipakṣa, viniyoga, para, bādhita, balīyastva | SR-1 to SR-3 | ≈ 0 or negative |
| Sacred proportions as structure: Śrī Cakra and Vāstu ring capacities; yuga 4 : 3 : 2 : 1 on shuffled data | G-1, Y-1 | ≈ uniform; −0.26 |
| Cosmological cycles as memory operations: laya/sṛṣṭi absorption, pralaya dissolution, niyati credit | SR-5 | ≈ 0 to −0.33 |
| Jyotiṣa friendship for choosing an expert | J-1 | ≈ follow-the-leader |
| The pramāṇas together; three-level bādha | SR-7 | +0.11 to +0.15 |
| Arthāpatti; syādvāda's seven standpoints | SR-4 | ≈ 0; depends on the data |
| Documented categories of real inputs | O-2 | −0.07 |
| Pratyāhāra as withdrawal of the fallback's attention | SR-6 | −0.15 |
| The krama-pāṭha check, a text-preservation method, applied to data | SR-8 | −3.93: it rejects genuine new cases |
| Silencing the member who only guesses (Manu 12.114) | PV-1 | −3.20 |
| Targeted śodhana; saṃyama's on-the-spot local lesson | PK-1, SR-8 | +0.44; +0.33 (NO WIN) |
| The rasa-sūtra as a lesson-forming rule (join different kinds of evidence) | RS-1 | −0.01 |
| Withholding general lessons until confirmed at each locus | SL-1 | −0.76 |

## 3. Not tested, and why

| Item | Reason |
| --- | --- |
| Śrī Cakra exact geometry | **Blocked.** Yoginīhṛdaya III.94–97, read by Codex on 18 October, gives the drawing context and the rule of equal triangles and lines, but no construction. |
| Rāga grammar | Source not yet read; no learning mechanism identified. |
| Saṃvatsara cycles; the halving durations of the subtle stages | Covered in principle by T-1 and Y-1: cyclic encodings, and recency only under change. |
| Chandas, gaṇita, mantra and letter tables, citrakāvya, Śulba constructions | Not learning mechanisms: they are encodings or construction algorithms. |
| Pañcakośa, turīya, kleśa, cit, the sādhaka question | Studies only. Codex's design verdicts and the studies themselves propose no mechanism. |

## 4. The overall pattern, stated plainly

**What wins.** The readings that win are about the knower's stance, not about rule machinery:
- who knows, and how different knowers combine;
- when to ask;
- when to abstain;
- what the world's symmetries are;
- when the world has changed.

**What fails.** The readings that fail are mostly attempts to turn arbitration doctrines, sacred proportions or cosmic cycles directly into a learner's internals.

**An honest note on novelty.** Every mechanism that won has a counterpart in ordinary machine learning:

| Sanatana reading | Machine-learning counterpart |
| --- | --- |
| Assemblies of diverse learners | ensembles |
| Asking under doubt | uncertainty sampling and query by committee |
| Answering only where one knows | selective prediction |
| Learning from mirror images | symmetry-based data augmentation |
| Health checks against one's own baseline | drift detection |

What these tests show is that these Sanatana sources point to principles that work, and that they hold up under preregistered, held-out testing. They do not show a new kind of learning that ordinary methods lack.

**Practical meaning for a working system.** An assembly of different learners that:
- asks a person only when its members disagree or doubt (here a third to a half of the cases);
- answers on its own only when all its members agree (about 85% right on those cases);
- watches its own error rate against its own baseline, to notice when the world has changed.

Each part of this system has passed a preregistered test on fresh data.

**Added the same day (MX-3).**
- **The blind spot:** a system that asks only under doubt can be blind to an abrupt change, because its members stay of one mind on the old concept.
- **The fix:** auditing 5% of its unanimous answers and watching its own errors (prakṛti–vikṛti) raised the accuracy of its own answers by +9.58 pp under an abrupt switch.
- **The cost:** no harm where nothing changed.
- **So the system needs a fourth part:** spot-check even confident answers, and watch for the world changing.
- **MX-4 replicated this on two fresh real streams:** +13.13 pp WIN. On the Beijing pollution stream, the unaudited system was right on 56% of the hours it answered alone, and 81.7% with audits.
- **The audits did the work there;** the reset added nothing more (+0.27). It helps under a hard switch.
- **With a language model as a member (ML-6)**, asking under doubt (+2.86 pp) and answering when of one mind (+9.90) both won.
  - A short warm-up is needed, because the model has no doubt signal of its own.
- **But asked to say SURE or UNSURE, the model does know where it knows (ML-7).**
  - Its SURE answers were +8.33 pp more accurate than random ones (WIN).
  - Asking only when UNSURE beat random asking by +2.92 (WIN).

**Added the same evening: several sources, one site (AR-1, MX-5 to MX-13, SL-2).**
- **Agreement across sources.** Three spies, each watching a different source and acting only when all agree and none is guessing, were right 96–99.7% of the time (Arthaśāstra 1.12).
- **Dismissal.** Dismissing the one that is the odd one out in 20 of its last 30 disagreements:
  - restored credence after a sensor failed, on four real settings: +13.41, +11.82, +12.85 and +9.17 inside the supervisor;
  - found the broken sensor almost always.
- **The whole supervisor won on three real machines and sensor sets:** +13.14, +9.68 and +14.52.
- **Its precondition.** Each source must be able to decide often on its own. Where none could (a naval simulator; phone and watch on 18 similar activities), the system asked about everything. It failed safe, and was useless.
- **Two broken sources at once.** Dismissal is a one-culprit rule.
  - Wrong answers alone rise from about 0.6 to 1–2 per 100.
  - A system-level alarm on three-way disagreement (prakṛti–vikṛti on the sources' own disagreement) cuts that by about a third.
  - Resuming must wait for verification against the owner's answers, which never erred. Agreement alone is not enough, because broken sources learn to agree.
- **Locus.** Keeping evidence per patient, site or machine helps when the units differ in baseline (Parkinson's patients 66.9% → 90.9%) and costs when they share one phenomenon.
- **The tested rules for a product** are collected in [the practical recipe](PRACTICAL-RECIPE-2026-10-18.md).
