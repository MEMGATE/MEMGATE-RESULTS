# Śāstra graph and knowledge coverage register

**Purpose.** One place that lists every Sanatana graph and knowledge family this project has named, the comparative families too, together with what has actually been tested and what comes next. Nothing is skipped silently. This register is updated after every experiment.

**Honest boundary.** "All Sanatana knowledge" is not a finite, testable list. This register covers every family named in three places:

- the user's master brief (`audits/multigraph_20261016/MASTER_BRIEF.txt`);
- Codex's source coverage of 17 October (`docs/PROJECT-STATUS-2026-10-17.md` §5), and Codex's later source studies of the same day (§3a);
- my own analysis.

Any family the user names is added here.

**Status labels.**

| Label | Meaning |
| --- | --- |
| TESTED | A comparative result against an ordinary baseline exists. |
| RUNNING | An experiment is in progress. |
| MECHANISM-ONLY | Earlier engineering bars passed or failed, but there was no comparison against an ordinary baseline. |
| PLANNED | An experiment ID is assigned. |
| SOURCE-ONLY | Sources have been read, but no computational mapping exists yet. |
| NOT A LEARNING MECHANISM | Ritual, iconographic, aesthetic or medical content. It is documented, but there is no learning test to run. |

Last updated 17 October 2026, after the SR-4 main run, with Codex's new source studies of 17 October added in §3 and §3a.

## 1. The master brief's graphs

| # | Family | Tradition | What has been tested | Result | Status / next |
| --- | --- | --- | --- | --- | --- |
| 1 | Modern knowledge graph (baseline) | modern | Used as the control in SR-1, SR-2 and ML-1 (DT, NB, 1-NN, ordinary rule learner, EXP) | — | Kept as the control |
| 2 | Nyāya–Pramāṇa evidence graph | Nyāya | SR-1/SR-2: upādhi, saṃśaya, satpratipakṣa, savyabhicāra discard. Ember ANUMANA studies. Codex labelled `Evidence.kind` with the four pramāṇas. | SR: NO WIN against ordinary. ANUMANA: SURVIVE (mechanism-only). The four pramāṇa labels were never tested. | TESTED piecewise: pratyakṣa over anumāna (SR-3 BAD, +0.02 pp), upamāna (A-1), śabda (ML-1/ML-2), arthāpatti (SR-4), anupalabdhi (SR-3, H-1) and the hetvābhāsas (§2). **TESTED SR-7:** the pramāṇas together. Nyāya chain +0.11 pp; assembly in which each means may abstain +0.14 pp. Both NO WIN. |
| 3 | Vṛtti–Saṃskāra learning graph | Yoga | Ember VS-EXP-1. ML-1: vṛtti admission of model-written lessons, with two real models. | VS-EXP-1: G1 FAIL. **ML-1: lessons vs experience +3.84 pp, WIN** (ML-2 +2.58, WIN). Vṛtti filter −0.22 pp, NO WIN. **ML-5, on five small real datasets: lessons −1.97 pp, NO WIN** (worst on the m-of-n autism concept). **SK-1, saṃskāra as latent impressions that return (YS 4.8–4.9): +2.22 pp WIN where the world recurs**; three confirmations beat two (+0.66); no net cost elsewhere (−0.10). | TESTED |
| 4 | Kālacakra temporal graph | Buddhist Vajrayāna, kept as comparative | Ember KC-EXP-1. T-1: layered recency retrieval (recent / middle / old). ML-2: layered neighbour selection for real models. H-1: on shuffled real data. | KC: INVALID. **T-1: +1.04 pp, WIN** (DRIFT-T +3.7, SEASON +4.8). H-1: ≈ 0 on shuffled real data. ML-2: NO WIN with models (−0.08 pp on drift). | TESTED. A drift tool for the offline fallback only. Real drift streams follow in SR-5. |
| 5 | Śrī Cakra layered graph | Śākta Śrīvidyā | Ember SC-EXP-1. G-1: the triangle-ring proportions (1+8, 10, 10, 14) as quotas for a bounded lesson memory, under both readings. | SC: VOID. **G-1: −0.27 pp vs FLAT, NO WIN; ≈ UNIFORM (−0.02).** | TESTED (ring capacities). The exact 9-triangle geometry is **BLOCKED** until a primary construction is collated. |
| 6 | Indra's Net associative graph | Buddhist Avataṃsaka/Huayan, kept as comparative (Vedic seed in Atharvaveda 8.8) | A-1: likeness transfer whose translated lessons are checked against the net of target experience | **+2.40 pp vs scratch, WIN**; +2.32 pp over upamāna alone | TESTED |
| 7 | Sāṃkhya ontology (optional) | Sāṃkhya | O-1: grouping shaped like the tattvas (4 pentads + 3 antaḥkaraṇa) as group-level features. O-2: documented groupings of five real domains. | **O-1: +11.07 pp vs flat, WIN (by construction).** O-2 on real domains: −0.07 pp, NO WIN. | TESTED. Categories help only when the concept follows them. |
| 8 | Hybrid multi-graph | — | Codex's early live hybrid | ordinary = hybrid (UNDETERMINED) | After the individual mechanisms have results |

## 2. Rule-system and reasoning knowledge

| Family | Source | What has been tested | Result | Status / next |
| --- | --- | --- | --- | --- |
| Utsarga–apavāda (exception bars the general rule) | Mīmāṃsā, Pāṇini | SR-1, SR-2 | Essential inside the design. NO WIN overall. Robust to label noise; weak on disjunctive concepts and drift. | TESTED |
| Upādhi, and saṃśaya over several upādhis | Navya-Nyāya | SR-1, SR-2 | No measurable effect alone; niścita (enough supports first) slightly negative | TESTED |
| Satpratipakṣa | Nyāya | SR-1, SR-2 | No measurable effect | TESTED |
| Vikalpa / viparyaya / smṛti / pramāṇa admission | Yoga Sūtra 1.5–1.11 | ML-1 main run | About 71% of model-written rules were viparyaya. The filtered lessons are more precise when shown (84.5% vs 81.0%), but accuracy is unchanged (−0.22 pp, NO WIN). | TESTED |
| Svataḥ vs parataḥ prāmāṇya | Mīmāṃsā vs Nyāya | ML-1: ORD trusts by default until contradicted (svataḥ); VRTTI validates first (parataḥ) | No difference (−0.22 pp) | TESTED |
| Six viniyoga pramāṇas (śruti > liṅga > vākya > prakaraṇa > sthāna > samākhyā) as a lesson-relevance ranking | Mīmāṃsā Sūtra 3.3.14 | SR-3 VIN: liṅga, a near-match lesson, before experience | −0.63 pp, NO WIN | TESTED |
| Full conflict order (pūrva < para < nitya < antaraṅga < apavāda) | Pāṇinian paribhāṣā | SR-3 PAN: apavāda, then para (later). Nitya and antaraṅga have no counterpart in classification. | −1.44 pp, NO WIN | TESTED |
| Hetvābhāsa: viruddha, asiddha, bādhita as explicit checks | Nyāya, Tarkasaṅgraha | SR-3 BAD tested bādhita, meaning pratyakṣa over anumāna. Asiddha is the default handling of missing values. Viruddha cannot arise in a precision-1 learner. | BAD +0.02, NO WIN (≈ 0 by construction) | TESTED (bādhita); viruddha is structurally absent |
| Arthāpatti (postulation, abduction) | Mīmāṃsā, Vedānta | Ember ARTHAPATTI report (mechanism-only PASS). SR-4 ART: when no lesson decides, the labels allowed by every well-observed literal leave one, which is postulated. | SR-4: −0.00 pp, NO WIN (dev +0.12). Postulations are about as accurate as the fallback they replace. | TESTED |
| Anupalabdhi / abhāva (knowing absence) | Mīmāṃsā, Nyāya | Ember ABHAVA report; SR-3 and H-1 ANU: a missing value is observed absence | **+0.34 pp (SR-3) and +0.45 pp (H-1)**, significant both times, below the 1 pp margin; annealing +3.4 | TESTED. The most robust positive on real data. |
| Upamāna (comparison, analogy) | Nyāya | A-1: likeness mapping alone | +0.08 pp, NO WIN; it works only with the Indra's Net check (+2.40 pp) | TESTED |
| Adhyāsa / bādha (superimposition, sublation hierarchy) | Advaita Vedānta | Ember ADHYASA guard. Covered in principle by SR-2 (balīyastva: a general lesson outnumbered by its exceptions is sublated; niścita) and SR-3 BAD (a stronger pramāṇa sublates an inference). | ADHYASA: PASS (mechanism-only). SR-2: NO WIN; BAD +0.02 pp. | **TESTED SR-7:** three-level bādha, +0.15 pp, NO WIN (it helps under noise and costs under drift). |
| Abhyāsa–vairāgya (YS 1.12–1.16): practice made firm (dṛḍha-bhūmi) by long, uninterrupted, devoted application; dispassion | Yoga | Covered in principle by SR-7's three-level bādha (an established lesson, with enough supports and age, is held rather than revised at a counterexample) and by SR-1/SR-2 niścita (enough supports before trust). Vairāgya matches R-ORD's own revision at the first counterexample. | SR-7 bādha +0.15, NO WIN; niścita slightly negative. On real streams, keeping refuted lessons cost (ST-1, −1.39). | Covered in principle; no separate run (it would differ from SR-7 only in counting an uninterrupted run instead of supports and age) |
| Blocking saṃskāra (YS 1.50): correction suppresses an old habit without deleting it | Yoga | Covered in principle by the apavāda carve-out of SR-1/SR-2 (a correction becomes an exception that blocks the old lesson in its context without deleting it) and by SR-5 sṛṣṭi (blocked lessons restored when the blocker fails) | SR-1/SR-2: NO WIN; SR-5 sṛṣṭi: +0.01 pp | TESTED in principle |
| Gaṇa and ākṛtigaṇa (1.1.27; the gaṇapāṭha): a rule stated over a listed class of values | Pāṇini | **PN-2:** values of a many-valued feature pooled into a class by their behaviour | **+0.35 pp, NO WIN** (significant, below the margin); behaviour vs random pooling +0.39 | TESTED |
| Asiddha staging (8.2.1), anuvṛtti, pratyāhāra | Pāṇini | **PN-1:** pratyāhāra (1.1.71) as contiguous-range literals over ordered bins. Anuvṛtti (carrying conditions forward) is how FOIL narrowing already works. | **PN-1: +1.19 pp, WIN**; inner stretches add nothing beyond thresholds (−0.02) | pratyāhāra TESTED (WIN). Asiddha (8.2.1, a later rule treated as not applied for earlier ones) is covered in principle by SR-1's explained counterexamples, where a carve-out exception is invisible to the general lesson's revision. It has not been run separately. |
| Vaiśeṣika padārthas (categories) | Vaiśeṣika | O-1 (synthetic) and O-2 (documented real-domain groupings) | O-1 WIN by construction; O-2 NO WIN (−0.07 pp) | TESTED |
| Avadhāna (attention) | Indian performance tradition | Ember AVADHANA phase 2 | KILL (mechanism-only) | Recorded; not re-run. Its learning reading, keeping each interleaved task's thread apart, is trivially right when tasks differ. It was already killed as a mechanism, so no separate test. |
| Adhikaraṇa (topic structure) | Mīmāṃsā | Ember ADHIKARANA | KILL (mechanism-only) | Recorded; not re-run |
| Counterfactual deliberation; cross-session learning | Ember line | Ember reports | SURVIVE (mechanism-only) | Recorded; not re-run |
| Apoha (meaning by exclusion) | Buddhist, comparative | Ember APOHA phase 2 | SURVIVE (mechanism-only) | **Covered in principle by SR-4 ART** (deciding by eliminating the labels every observed literal excludes): ≈ 0, NO WIN |
| Syādvāda / nayavāda (sevenfold predication, partial standpoints) | Jaina, comparative | Ember SYADVADA report: saptabhaṅgī aspect ledger with maximin action choice (mechanism-only). SR-4 SYA: the fallback becomes a vote of 7 standpoints, each a 1-NN over half the features. | SR-4: −0.68 pp, NO WIN. +0.4 to +2.4 pp on the noisy two-class data and Connect-4; −5.8 on letter, −4.8 on yeast. | TESTED. Helps with few classes and noisy features; fails with many classes. The seven predicate forms as truth values are not modelled. |
| Cit as fundamental | Upaniṣadic | Ember CIT study | Declared unfalsifiable in that study; no test | NOT TESTABLE as a learning mechanism |

## 2a. Ember's earlier mechanism studies (September–October), so that none is missed

These ran inside the Pramana agent architecture. Each was judged against its own frozen engineering bars, not compared with an ordinary learner, so every verdict here is **mechanism-only**. The documents are in the repository's `docs/`. "Covered here" means one of my comparative experiments tests the same idea as a learning mechanism.

| Concept | Tradition | Ember's verdict (document) | Comparative status here |
| --- | --- | --- | --- |
| Vyāpti certification (no deviation, else refused) | Nyāya | PASS 100/100 (`VYAPTI-REPORT-2026-09-27`) | Covered: precision-1 lesson validation and the savyabhicāra discard in SR-1/SR-2 |
| Hetvābhāsa checks | Nyāya | SURVIVE, phase 1 (`HETVABHASA-PHASE1-2026-10-11`) | Covered: bādhita in SR-3; see §2 |
| Pañcāvayava (five-membered argument) | Nyāya | PASS, mechanism-only (`PANCAVAYAVA-REPORT-2026-09-26`) | Not re-run. It is an argument format, not a learning rule. |
| Chala (quibble detection) | Nyāya | SURVIVE (`WAVE12-CHALA-REPORT-2026-09-30`) | Not re-run. It belongs to dialogue and adversarial input. |
| Śabda (testimony) | Nyāya, Mīmāṃsā | SURVIVE (`SHABDA-STUDY-REPORT-2026-10-12`) | Covered: model-written lessons are testimony; ML-1 lessons WIN (+3.84 pp), and trusting by default (svataḥ) = validating first (parataḥ) |
| Smṛti (memory admission) | Yoga, Mīmāṃsā | SURVIVE (`SMRTI-STUDY-REPORT-2026-10-12`) | Covered in part: the smṛti merge in ML-1's vṛtti filter (NO WIN) |
| Jijñāsā (inquiry before belief) | Mīmāṃsā, Vedānta | SURVIVE, phases 1–2 (`JIJNASA-PHASE2-REPORT-2026-10-12`) | **TESTED JK-1:** asking for a label only under doubt beat random asking at the same budget by +3.69 pp, **WIN**; with 22% of the labels it matched seeing all of them (−0.53 pp) |
| Khyāti (theories of error) | Darśanas | SURVIVE, then KILL in phase 2 (`KHYATI-PHASE2-REPORT-2026-10-12`) | **TESTED SR-6:** Prābhākara akhyāti. +0.61 pp [+0.48, +0.75], significant, NO WIN by margin (dev +0.15). It hurts on drifting Elec2. |
| Vimarśa (lesson promotion gate) | Kashmir Śaiva | PASS (`VIMARSA-REPORT-2026-09-26`) | Covered in principle: validation before use (SR-1) |
| Pratyabhijñā (recognition) | Kashmir Śaiva | Kill (a): no behavioural difference from a vikalpa-gate baseline (`PRATYABHIJNA-REPORT-2026-09-25`) | Covered in principle by SR-3 BAD: an identical past case is recognised and decides (+0.02 pp) |
| Svasaṃvedana (self-awareness) | Buddhist, Śaiva | KILL, C3 (`SVASAMVEDANA-C3-REPORT-2026-10-10`) | Not re-run; not a learning mechanism |
| Svalakṣaṇa ledgers (particulars) | Buddhist pramāṇa | SURVIVE (`WAVE13-SVALAKSANA-REPORT-2026-09-30`) | Not re-run |
| Śeṣa (subsidiary relation) | Mīmāṃsā | SURVIVE (`WAVE8-SESA-REPORT-2026-09-30`) | Not re-run |
| Apūrva (unseen potency linking act and result) | Mīmāṃsā | PASS (`APURVA-REPORT-2026-09-26`) | **Covered in principle by SR-5 NIY**: crediting an outcome only to the lessons that acted. −0.20 pp, NO WIN. A delayed-label version would need delayed feedback, which this lab's streams do not have. |
| Bhāvanā (efficacy ledger) | Mīmāṃsā | SURVIVE, confirmed (`VERDICT-TDG72-BHAVANA-2026-10-02`) | Not applicable to this learner: its lessons are revised at the first error, so every active lesson has a perfect record and a ledger has nothing to rank. The nearest tested form is SR-2's strength rule (balīyastva), NO WIN. |
| Niṣkāma phala (action without fruit attachment) | Bhagavad Gītā | PASS (`NISHKAMA-PHALA-REPORT-2026-09-25`) | Not re-run; it is an action-audit rule |
| Kṣetra–kṣetrajña (field and knower) | Bhagavad Gītā 13 | PASS (`KSETRAJNA-LITE-REPORT-2026-09-25`) | **TESTED JK-1:** answering only where a lesson decides is +7.08 pp more accurate than an equal random subset, **WIN**. **ML-7, the model itself:** gpt-6.1-sol's SURE answers +8.33 pp more accurate than random (**WIN**); asking only when UNSURE +2.92 (**WIN**). |
| Saṃyama | Yoga Sūtra III | INCONCLUSIVE after a retracted KILL (`SAMYAMA-LIVE-REPORT-2026-10-05`, `SAMYAMA4-PREREG-2026-10-07`) | **TESTED SR-8 (YS 3.1–3.6):** a lesson formed on the spot from the case's 30 nearest cases when no lesson decides. +0.33 pp, NO WIN (+2.94 on NOISE); below a plain 7-neighbour vote (−0.74). |
| Pratyāhāra (withdrawal) | Yoga | P1 SURVIVE (`PRATYAHARA-P1-REPORT-2026-10-10`) | **TESTED SR-6:** the fallback withdraws from features no lesson uses. −0.15 pp, NO WIN. |
| Kleśa and citta-bhūmi | Yoga | Study only (`KLESA-CITTA-BHUMI-STUDY-2026-10-13`) | SOURCE-ONLY |
| Cit as fundamental; the sādhaka question (who practises?) | Sāṃkhya, Vedānta | Studies only (`CIT-FUNDAMENTAL-STUDY-2026-10-13`, `SADHAK-QUESTION-STUDY-2026-10-13`), which deliberately propose no mechanism | SOURCE-ONLY |
| Bṛhadāraṇyaka study | Upaniṣad | Study only (`BRHADARANYAKA-STUDY-2026-10-13`) | SOURCE-ONLY |

## 3b. Other families, not yet in any coverage list

| Family | Status |
| --- | --- |
| Saṅgīta: tāla cycles | Cyclic structure is covered in principle by T-1's cyclic encodings. |
| Saṅgīta: rāga grammar | SOURCE NOT READ. No learning mechanism identified yet. |
| Nāṭyaśāstra rasa theory (vibhāva, anubhāva, vyabhicāribhāva → rasa; VI.31) | **TESTED RS-1** (source: the rasa-sūtra, Ghosh's translation). Lessons must join at least two documented kinds of evidence. −0.01 pp, NO WIN; documented kinds = random kinds (as in O-2). |
| Chandas (Piṅgala's prastāra, naṣṭa, uddiṣṭa) | NOT A LEARNING MECHANISM. It is binary enumeration and encoding, like kaṭapayādi. |
| Dharmaśāstra (āpad-dharma; deśa–kāla–pātra) | Covered in principle by utsarga–apavāda (SR-1/SR-2) and time-dependence (T-1) |
| Dharmaśāstra *pariṣad*: an assembly of members of different competences decides doubtful points (Manusmṛti 12.111–112, checked against Bühler and Jha/Medhātithi) | **TESTED P-1 and P-2:** a mixed three-member assembly **+1.44 pp WIN** (P-1) and **+1.56 / +1.60 pp WIN** (P-2, on a second fresh pool); the five-expert majority **+1.07 pp WIN**. The primary ten-member assembly (7 of 10 lesson-learner variants) ≈ R-ORD, NO WIN. **TESTED ML-4:** models in a pariṣad with classical learners, +5.67 pp over the model alone (WIN). **ML-3** (three models, including grok-4.7) is SUSPENDED: grok's latency (117 s per proposal, 110 s per prediction under load) makes it infeasible. **TESTED PV-1 (Manu 12.113–114):** one member that knows overruling the agreeing others −0.67 pp, NO WIN; silencing the guesser −3.20; the assembly asking only under doubt **+3.94 pp, WIN**; the three-member assembly beat its lesson member again (+1.17) on a fourth pool. **ML-5 (real data):** the model-mixed assembly lifted the model +1.72 pp (WIN); it adds nothing over the offline assembly (−0.05). **MX-2 (the mix):** the asking assembly replicated (+3.19 pp WIN); answering only when of one mind +7.88 pp selective accuracy (WIN); the full system +6.34 (WIN). |
| Āyurveda tridoṣa: prakṛti (constitution) vs vikṛti (current state) | **TESTED PK-1 and PK-2** (Caraka Sūtrasthāna 9.4) as the learner's own health check. Targeted śodhana +0.44 pp, NO WIN. The diagnosis detects abrupt change: a reset at the diagnosed moment beats a random-time reset by **+5.59 pp (PK-2 WIN, DRIFT)**. On real streams, timing did not matter (−0.07), and PK-1's +4.28 reset gain did not replicate (−0.22). |
| Gaṇita algorithms (kuṭṭaka and others) | NOT A LEARNING MECHANISM |
| Vedic recitation: krama-pāṭha and the other vikṛti-pāṭhas (text preservation by overlapping pairs) | **TESTED SR-8:** a case whose overlapping feature pairs break is set aside. −3.93 pp, NO WIN. It rejects genuine new combinations, worst with many classes. |
| Jyotiṣa: Bṛhat Jātaka (Aiyar 1905), studied by Codex (`docs/research/jyotisa-study-20261017/`, read only, 18 October). It records source-derived candidates and marks none as tested. | Candidate learning readings: **vargas** (one cyclic quantity divided at several resolutions: 2, 3, 9 and 12 parts) as multi-resolution literals; **pañcadhā maitrī** (natural × temporary friendship giving five grades) as member standing from long-run × recent reliability. Cycles (108 = 12×9 = 27×4) are covered in principle by T-1. Predictive claims (fate, character, illness) are NOT A LEARNING MECHANISM and are not validated. Vargas are covered in principle by PN-1 (nested divisions are ranges over finer ordered bins) and T-1 (cyclic encodings). **TESTED JY-2 (pañcadhā maitrī as pariṣad vote weights): +0.04 pp, NO WIN**; EXC +1.5, DRIFT +1.0, NOISE −2.1. |
| Arthaśāstra 1.10: ministers tested by four allurements and employed in the work each was proved on; those tested under all become prime ministers (Shamasastry, checked on Wikisource). | **TESTED AR-2:** each case goes to the member proved best on the 10 most similar past cases. −0.25 pp vs plurality, NO WIN; −0.49 vs the best member overall; +0.29 vs 10 random cases. |
| Arthaśāstra 1.12: the intelligence rule. Reports from three different sources that agree are reliable; spies who frequently differ are punished or dismissed (Shamasastry, checked on Wikisource; Kangle quoted by Gautam 2013). | **TESTED AR-1:** three spies that see different sources, with credence only when they agree and none is guessing. **Dismissing the spy that frequently differs after a source fails: +13.41 pp net credence, WIN**; the right spy vs a random one +9.78 (WIN); it also helps when all sources work (+1.14, WIN); agreement is right 96–99.7% (+16.61 vs random, WIN). The broken source was found in 36 of 40 runs. |
| Bhagavad Gītā 18.20–22: sāttvika, rājasa and tāmasa knowledge | **TESTED SR-8** as a ranking of learners: lessons (the one in the many) > nearest case (each separately) > majority label (one effect as the whole). **Holds on average** (+1.71 and +15.93 pp), not on every dataset. |

## 3. Diagram and source families (Codex's coverage of 17 October)

| Family | Sources read | Status / next |
| --- | --- | --- |
| Sarvatobhadra and bhadra maṇḍalas; Navapadma and Navanābha; Netratantra Śrīmaṇḍala; Trika tridents; Pāñcarātra Cakrābja | Bühnemann 2003 volume and selected primary sources | SOURCE-ONLY. Candidate mapping: zoned or region memory. Tested together with G-1/G-2. |
| Vāstu Puruṣa maṇḍala (64/81 grid, Brahmasthāna centre) | Mānasāra VII and Bühnemann chapter | TESTED in G-1: 81-pada ring proportions (9, 16, 24, 32) as lesson-memory quotas, both readings. −0.34 pp vs FLAT, NO WIN; ≈ UNIFORM. |
| Purāṇic cosmology (concentric dvīpas, yuga cycles) | Viṣṇu Purāṇa II.1–4; later II.5–12 and VI.1–7 (§3a) | Ring structure tested via G-1 (NO WIN). **TESTED in SR-5:** the occasional dissolution with its three realm classes as periodic lesson dissolution. −0.33 pp, NO WIN; −0.17 on real drift streams. Yuga proportions 4 : 3 : 2 : 1 as an ageing weight: **TESTED SR-7 and Y-1.** SR-7's +1.94 pp came from 7-neighbour voting. The weights themselves give −0.26 pp vs equal weights on real data and help only under drift (+0.96; +2.81 vs reversed). Saṃvatsara cycles remain untested. |
| Jyotiṣa (rāśi, bhāva, nakṣatra; North and South chart layouts) | Partial; recovery state recorded. Codex's Bṛhat Jātaka study (26 typed relation families, directed friendship, strengths, drekkāṇa) | TESTED via T-1 pañcāṅga (nakṣatra, māsa): it encodes its own cycles (+27.6 pp vs generic, by construction) and costs nothing elsewhere. The chart layouts are not a mechanism. **TESTED in J-1:** *pañcadhā maitrī* as the rule for choosing which of five expert learners to follow. −0.01 pp vs follow-the-leader, NO WIN; +0.46 vs recent-only; −0.86 vs a plain majority. Varga subdivisions are periodic sub-sign positions and are meaningful only for cyclic quantities, which T-1 covered. |
| Body cakras (Ṣaṭcakranirūpaṇa, Pādukāpañcaka) | Codex completed the bounded English Ṣaṭcakranirūpaṇa reading on 17 October (opening, heart–throat, ājñā, sahasrāra entry and completion, closing; see §3a) | **TESTED in SR-5:** ascent (*laya-krama*) as ordered lesson absorption, and return (*sṛṣṭi-krama*) as restoration on failure. −0.03 pp, NO WIN (≈ 0). Order vs random order: ±0.00. |
| Āyurvedic body image (Wujastyk 2007) | Complete | NOT A LEARNING MECHANISM |
| Kolam (dot-grid line drawings) | Waring preprint and final version | **EXPLORATORY K-1** on exposed boards: a case's symmetric images (the kolam's grid symmetry) gave +3.45 pp for R-ORD and +9.13 for 1-NN. **TESTED K-2, preregistered on fresh jungle chess endgames:** the left-right mirror gives **+2.14 pp for R-ORD and +1.72 for 1-NN, both WIN**; all 44,104 mirror pairs share their outcome. **TESTED K-3, a physical world** (Higgs events with parity and azimuthal reflection): R-ORD +0.78 pp (UNDETERMINED), 1-NN +0.63, naive Bayes **+1.03 (WIN)**. The drawing grammar itself is not modelled. |
| Mantra, letter and number tables (kaṭapayādi and others) | Bühnemann 1991 | NOT A LEARNING MECHANISM. They are encoding schemes. |
| Śaiva 36 tattvas and Sāṃkhya 25 | Goodall 2009 | TESTED in O-1, Sāṃkhya-shaped: a correct grouping helps, a random one does not. The Śaiva 36-tattva shape is not run separately, because it differs only in group sizes. |
| Poetic diagrams (citrakāvya bandhas) | Cielas 2019 | NOT A LEARNING MECHANISM. They are constraint puzzles. |
| Śulba constructions | Keller 2000; Baudhāyana 8 | NOT A LEARNING MECHANISM. They are geometric construction algorithms. |
| Mīmāṃsā and Pāṇini source reports | Freschi et al. 2017; Rajpopat 2023; Scharf 2022 | Feed SR-3 |

## 3a. Codex's later source studies (17 October), and what each gets

| Codex study | Content | Status / next |
| --- | --- | --- |
| Ṣaṭcakra opening → closing (`docs/SANATANA-SATCAKRA-*-2026-10-17.md`) | Six centres, petals, elements and letters; the closing's ascent and return | **TESTED SR-5:** ≈ 0, NO WIN; order irrelevant |
| Kiraṇa chapter 1 (`docs/SANATANA-KIRANA-BONDAGE-2026-10-17.md`) | Categories, bondage and release; karma produces a fruit, and *niyati* connects it to its own experiencer | **TESTED SR-5** (NIY): −0.20 pp, NO WIN |
| Viṣṇu Purāṇa vertical and time cosmology, II.7 and VI.1–5 (`docs/SANATANA-COSMOLOGY-VERTICAL-TIME-…`, `…-DISSOLUTION-…`) | Realm classes, time ladder, dissolution and re-creation | **TESTED SR-5** (PRALAYA): −0.33 pp, NO WIN |
| Viṣṇu Purāṇa rain and planets, II.9–12 | Solar water uptake and rain, the planetary chariots, Dhruva and the Śiśumāra support | SOURCE-ONLY. No learning claim was identified; these are physical-cosmological descriptions. |
| Viṣṇu Purāṇa Book 2 closing (Bhārata and the closing chapters) | Geography and teaching narrative | NOT A LEARNING MECHANISM |
| Viṣṇu Purāṇa yoga closing (VI.7) | Steps of yoga; fixing the mind from the form with attributes to the formless | The direction from gross to subtle is the same as LAYA's. It is not tested separately. |
| Vedānta states and kośas (Hume: Taittirīya I–III, Māṇḍūkya; `docs/SANATANA-VEDANTA-STATE-KOSA-2026-10-17.md`) | Five sheaths; waking, dream, deep sleep and the fourth | Codex's September design verdicts stand: relabelling the three states as compute roles was not proposed, turīya-as-witness has no procedure, and pañcakośa layering was rejected as metaphor. Layered grouping in general is covered by O-1. No separate test. |
| Bṛhat Jātaka relations (`docs/SANATANA-JYOTISA-RELATIONS-2026-10-17.md`) | Directed natural friendship, temporary friendship, strengths, drekkāṇa | **TESTED J-1:** ≈ follow-the-leader, NO WIN |
| Antaḥkaraṇa pipeline (manas → buddhi → ahaṃkāra → citta) | From the Sāṃkhya row in §1 | The lesson learner already runs propose → validate → own → store. Its stage ablations were tested: candidate application in SR-1 and vṛtti admission in ML-1, both NO WIN. No separate test. |
| Yoginīhṛdaya I.1–86 (opening, manifestation, body, subtle stages, speech and pīṭhas, forms, mudrās, chapter 1 closing; `docs/SANATANA-YOGINIHRDAYA-*` on Codex's branch, read 18 October) | The nine cakra constituents (2 + 4 + 3), vowels on the triangle, 42 yonis; the order of drawing vs the order of powers; eight subtle stages from ardhacandra to unmanā, each half as long as the last; pīṭha and liṅga orders; ten mudrās; the cakra built in three groups, and creation/dissolution as order (bindu → squares or back) | Codex marks every one SOURCE-ONLY, with no candidate mechanism. Ring proportions are tested in G-1. Order of absorption vs creation is tested in SR-5 (≈ 0, order irrelevant). The halving durations are a recency schedule; recency weighting helps only under drift (Y-1, T-1), so it is covered in principle. No separate test. |
| Yoginīhṛdaya III.94–97, the pūjā drawing (`docs/SANATANA-YOGINIHRDAYA-PUJA-DRAWING-2026-10-18.md`) | Drawing materials, writer and reciter, the rank of the cakra, offerings; the rule of equal triangles and equal lines | It gives **no step-by-step construction** (no line positions, intersections or the 43 triangles). Codex: exact geometry "remains open". **The Śrī Cakra exact-geometry test stays BLOCKED.** Chapter II to III.93 is still unread. |
| Kiraṇa chapters 2–6 (`docs/SANATANA-KIRANA-CHAPTER2..6-*`) | Five kinds of textual connection; mala, māyā and karma as separate causes; an absence is inferred only with a proven general rule (ch. 2); the generation chain of faculties (ch. 4); śaktipāta and its timing (ch. 5); evidence must come from the same locus: "smoke in one tree does not prove fire in another" (ch. 6) | Codex: SOURCE-ONLY. Inferring absence is tested in SR-3/H-1 (anupalabdhi). **TESTED SL-1** (same-locus evidence, with Nyāya pakṣadharmatā): real loci beat random ones by +1.04 pp (WIN), and the locus as a feature helps (+0.72). Withholding general lessons until confirmed at each locus costs (−0.76, NO WIN). |
| Yoginīhṛdaya chapter II, II.1–85 (`docs/SANATANA-YOGINIHRDAYA-CHAPTER2-*` on Codex's branch, read 18 October) | Mantra as reflection and protection. Nyāsa placement. The six meanings of the mantra (bhāvārtha, sampradāya, nigarbha, kaulika, sarvarahasya, mahātattva). Letters and elements, with qualities inherited down a pervasion chain. Nāda as a residual trace. The three knowers. 111 enclosure deities. Kuṇḍalinī. Nyāya contact and agreement/difference inference. Daily and occasional observance. | Codex: no admitted mechanism. It explicitly rejects reading II.50–51's doubt (śaṅkā) as an uncertainty metric, and II.36's trace as a memory mechanism. **No Śrī Cakra construction:** II.52–54 and II.67 state which parts generate which, "without … a construction algorithm, triangle orientations, intersection coordinates". **The geometry test stays BLOCKED.** |
| Yoginīhṛdaya chapter III opening, III.1–20 | Three forms of worship; the aparā form is done daily even by knowers (III.3 commentary; omission is a fault, II.82–83). Contemplation as unbroken attention. The sixfold nyāsa order. The Gaṇeśa names. | Codex: source-only. **My mapping of III.3, the daily observance even of the one who knows:** audit a small share of the answers the system is confident of. **TESTED MX-3 and MX-4: +9.58 and +13.13 pp, WIN.** |

## 4. Queue

Each item follows the same discipline: spec, then preregistration with held-out data, then one main run, then the result. Each is committed and pushed.

**Done.** Every family in sections 1–3 that has a testable learning reading now has a preregistered result. The earlier queue (ML-1, SR-3, G-1, T-1, A-1, O-1, ML-2, H-1, SR-4 to SR-8, J-1, P-1, P-2, O-2, PN-1, MX-1, Y-1, ML-4, ML-5) is complete. These followed, all on 17 and 18 October:

| Experiment | Subject |
| --- | --- |
| JK-1 | jijñāsā and kṣetrajña |
| K-2, K-3 | kolam symmetry, preregistered |
| PV-1 | Manu 12.113–114 |
| PK-1, PK-2 | prakṛti–vikṛti |
| MX-2, MX-3, MX-4 | the asking system and its audits |
| SR-8 | krama-pāṭha, saṃyama and the Gītā's three knowledges |
| RP-1 | six replications |
| SL-1 | same-locus evidence |
| RS-1 | the rasa-sūtra |
| ML-6 | a model inside the asking assembly |
| ML-7 | the model's own SURE or UNSURE |
| SK-1 | saṃskāra: latent impressions that return |
| AR-1 | Arthaśāstra 1.12: three different sources |
| MX-5 | the supervisor: every earned piece together, with ablations |
| JY-2 | Jyotiṣa: pañcadhā maitrī |
| AR-2 | Arthaśāstra 1.10: employment by ascertained purity |
| MX-6 | the supervisor replicated on a second machine |
| PN-2 | Pāṇini's gaṇa |
| ST-1 | saṃskāra and pañcadhā maitrī on fresh real streams |
| SL-2 | SL-1 replicated on fresh loci |
| MX-7 | AR-1 and the supervisor replicated on body-worn sensors |
| MX-8 | the supervisor × locus |
| MX-9 | one or two failing sources (safety) |
| MX-10 | two-failure safety on a testable setting |
| MX-11 | a system-level alarm on three-way disagreement |
| MX-12 | the alarm with recovery |
| MX-13 | the alarm with verification against the owner's answers |
| SE-1 | Saṃskāra Engine, first brick: gated learning into weights |
| SE-2 | jijñāsā and smṛti against stealthy and colluding poisoners, 12 sessions, 1.5B |
| SE-3 | the engine on real 2024–2026 Wikidata changes, Qwen2.5-7B, with Kiraṇa locus routing |
| SE-4 | pratiprasava (YS 2.10): ledger-based exposure of sleepers and rollback-and-replay unlearning |
| RM-1 | the gate in front of a frontier model's retrieval memory (Azure Foundry) |
| SE-5 | Nyāya's āpta rule against sybil swarms, into a 7B model's weights |
| RM-2 | memory as an injection channel: forged provenance vs the value gate |
| RM-3 | forged provenance across three frontier models |
| RM-4 | forged provenance on a fourth model from a third lab |
| RM-5 | escaping and marking a raw memory vs the value gate |
| RM-6 | a small model reading raw vs gated memory |
| TM-1 | the whole engine at scale, every attacker at once, 1,341 real offices |
| HH-1 | the engine against rehearsal and LoRA merging on the same poisoned stream |

**Open:**

| Item | Status |
| --- | --- |
| Śrī Cakra exact triangle geometry | **BLOCKED.** Yoginīhṛdaya III.94–97 gives no construction. Codex's III.21–57 studies (audited 18 October) are nyāsa on the body. They give an outer-to-inner order with counts (3 square lines, 16 petals, 8 petals, 14 corners) but no drawing of the nine triangles; Codex: "No geometry reconstruction follows." III.58–93 are still unread. |
| Rāga grammar | No learning mechanism identified. A melodic grammar would need sequence data, which this lab does not use. |
| ML-3 (three models including grok-4.7) | Suspended until a faster third model is available |
| Fresh real streams with natural labels | Five more were used in ST-1 (bike sharing, metro traffic, Tetouan power, Seoul bikes, appliances), split at the median of the whole stream. |

## 5. Results so far, in one line each

| Experiment | Result |
| --- | --- |
| SR-1 | NO WIN, −0.05 pp |
| SR-3 | NO WIN, mix −1.74 pp; only ANU positive (+0.34) |
| G-1 | NO WIN: Śrī −0.27, Vāstu −0.34 vs FLAT; sacred ≈ uniform quotas |
| T-1 | Pañcāṅga +27.6 pp on its own cycles (by construction), ≈ 0 elsewhere; **Kālacakra recency layers +1.04 pp WIN** |
| A-1 | Upamāna alone NO WIN (+0.08); **upamāna + Indra's Net check +2.40 pp WIN** (ceiling +6.70) |
| O-1 | Correct tattva-shaped grouping +11.07 pp WIN (by construction); random grouping no help |
| H-1 | Winners combined on 6 new real datasets: +0.39 pp (significant, NO WIN); ANU +0.45; KALA ≈ 0 on real data, +1.33 under drift |
| SR-2 | NO WIN, −1.32 pp on held-out data; the only consistent strength is under noise |
| SR-4 | NO WIN: mix −0.55 pp; arthāpatti ≈ 0; standpoint vote −0.68 overall (+0.4 to +2.4 on noisy two-class data, −5 on many-class data) |
| SR-5 | NO WIN: mix −0.81 pp; laya/sṛṣṭi −0.03 (order irrelevant); pralaya −0.33; niyati −0.20; Kālacakra on real streams −0.20 (Elec2 +0.92, gas drift −1.38) |
| J-1 | NO WIN: maitrī ≈ follow-the-leader (−0.01 pp); a plain majority of five learners was best and beat the lesson learner on streams (+1.12, descriptive) |
| SR-6 | NO WIN by margin, but **akhyāti +0.61 pp significant** (Haberman +3.3, rice +1.2); pratyāhāra −0.15; best-so-far mix +0.46, above naive Bayes |
| P-1 | Primary NO WIN (ten mostly-alike members ≈ R-ORD); **PARISHAD-3 +1.44 pp WIN, MAJORITY-5 +1.07 pp WIN** on 9 new datasets |
| O-2 | NO WIN: documented real-domain feature groups −0.07 pp vs flat, −0.12 vs random groups |
| P-2 | **WIN: the mixed pariṣad with anupalabdhi and akhyāti inside +1.60 pp; P-1's assembly replicates +1.56 pp.** Mechanisms inside add +0.04; five members −0.50. |
| PN-1 | **WIN: Pāṇinian range literals +1.19 pp** for the lesson learner; equal to plain thresholds (−0.02) |
| MX-1 | **WIN: the grand pariṣad (all earned pieces) +1.21 pp**; the pieces add +0.22 inside the assembly; the plain assembly +0.99 (third replication, UNDETERMINED) |
| ML-4 | Model-mixed pariṣad vs the model alone **+5.67 pp WIN**; vs the offline assembly +1.01 UNDETERMINED; the model alone vs R-ORD −0.79 |
| SR-7 | Pramāṇas together +0.11 / +0.14, three-level bādha +0.15 (NO WIN); yuga 7-NN fallback +1.94 WIN, credited by Y-1 to voting, not to the yuga weights |
| Y-1 | NO WIN: yuga weights −0.26 pp vs equal-weight voting on real data; only under drift +0.96 (+2.81 vs reversed); SR-7's yuga gain did not replicate (−0.49) |
| ML-1 | **WIN for lessons vs experience (+3.84 pp, real models)**; NO WIN for śāstra management (−0.22 pp) |
| ML-2 | **Lessons vs experience WIN again (+2.58 pp)**; Kālacakra layers with real models NO WIN (−0.08 pp on drift) |
| JK-1 | **Jijñāsā +3.69 pp WIN; kṣetrajña +7.08 pp WIN** (selective accuracy) |
| K-2 | **Kolam mirror on jungle chess: R-ORD +2.14 pp WIN, 1-NN +1.72 WIN** |
| PV-1 | Manu 12.113 override −0.67 (NO WIN); silencing the guesser −3.20; **the assembly asking under doubt +3.94 WIN** |
| ML-5 | Model lessons on small real data −1.97 (NO WIN); **mixed pariṣad lifts the model +1.72 WIN** |
| PK-1 | Targeted śodhana +0.44 (NO WIN); reset at the diagnosed moments +4.28 WIN (not the timing, per PK-2) |
| PK-2 | **Diagnosed timing beats random timing under an abrupt switch +5.59 WIN**; on real streams −0.07 |
| MX-2 | **The asking assembly +3.19 WIN; unanimity +7.88 WIN; the full system +6.34 WIN** |
| SR-8 | **The Gītā's ranking holds on average**; saṃyama +0.33 (NO WIN); krama-pāṭha check −3.93 |
| K-3 | Kolam symmetry in Higgs events: R-ORD +0.78 (UNDETERMINED); **naive Bayes +1.03 WIN** |
| RP-1 | **All six earlier winners replicate**; four WIN again |
| SL-1 | **Real loci beat random loci +1.04 WIN**; withholding general lessons −0.76 |
| RS-1 | Rasa-sūtra as a lesson rule −0.01 (NO WIN) |
| MX-3 | **Audits + health check fix the asking assembly's blind spot +9.58 WIN; reset beyond audits +4.74 WIN** |
| MX-4 | **On fresh real streams, audits +13.13 WIN**; reset beyond audits +0.27 |
| ML-6 | **A model inside the asking assembly: asking under doubt +2.86 WIN; unanimity +9.90 WIN** (8,528 calls, 0 failures) |
| ML-7 | **The model knows where it knows: SURE +8.33 WIN; asking when UNSURE +2.92 WIN** (8,126 calls, 0 failures) |
| SK-1 | **Saṃskāra (YS 4.8–4.9): +2.22 pp WIN where the world recurs**; R = 3 beats R = 2 (+0.66); five other families −0.10 |
| AR-1 | **Arthaśāstra 1.12: all four WIN.** Dismissal after a failure +13.41; the right spy +9.78; when sound +1.14; agreement +16.61 vs random |
| MX-5 | **The supervisor +13.14 pp WIN** on a real hydraulic rig; inside it dismissal +11.82 (WIN) and saṃskāra +2.56 (WIN); audits −0.96 and resets −1.00 NO WIN (resets cut wrong answers −0.56) |
| JY-2 | Pañcadhā maitrī vote weights +0.04 pp, NO WIN (EXC +1.5, DRIFT +1.0, NOISE −2.1) |
| AR-2 | Local competence (Arthaśāstra 1.10) −0.25 pp vs plurality, NO WIN; −0.49 vs the best member overall |
| MX-6 | Supervisor on the naval plant **did not replicate** (+0.30, NO WIN): coverage ≤ 1.6%, since no single sensor group decides; it failed safe |
| PN-2 | Gaṇa value classes +0.35 pp, NO WIN (behaviour vs random pooling +0.39) |
| ST-1 | **Saṃskāra on fresh real streams −1.39 (hurt on all five)**; pañcadhā maitrī +0.55, NO WIN |
| SL-2 | **Locus replicated: +12.27 vs random loci (WIN); +5.94 vs the plain learner (WIN)**; patients 66.9 → 90.9; one city's stations −5 |
| MX-7 | **AR-1 dismissal +12.85 (WIN) and supervisor +9.68 (WIN) replicated on PAMAP2**; saṃskāra inside +0.28 (not replicated) |
| MX-8 | **Supervisor +14.52 (WIN, a fourth setting)**; each spy knowing the person +1.38, UNDETERMINED |
| MX-9 | **Uninformative:** WISDM sources could not decide alone (coverage ≈ 0%); H1 +0.03, H2 +0.01. Safety with two failures was then tested in MX-10. |
| MX-10 | **Two broken sources: UNSAFE** (2.00 wrong alone per 100; dismissal never fires with two culprits); one failure +10.90 WIN |
| MX-11 | **Alarm makes the double failure SAFE (0.84 per 100)**; permanent stops cost on rare false alarms (HARM by the strict rule) |
| MX-12 | Self-resuming alarm: NO HARM when sound, **UNSAFE with two broken sources (1.78)**; broken sources learn to stop disagreeing |
| MX-13 | Verification found 21 of 21 broken, 0 working wrongly; still UNSAFE by the bound (1.97). Two broken sources: about 1–2 wrong alone per 100 across MX-10 to MX-13. |
| SE-1 | **Gated learning into weights: poison −23.44 (WIN), retention +11.25 (WIN), truth +3.44 (NON-INFERIOR), updates +8.33 (WIN), constitution check +14.37 (WIN)** |
| SE-2 | **Jijñāsā gate vs stealthy and colluding poisoners: poison −8.75 vs SE-1's gate (WIN), −24.06 vs naive (WIN); truth +6.69 (NON-INFERIOR); retention +4.25 (WIN); changed facts −0.99 (UNDETERMINED)** |
| SE-3 | **Real 2024–2026 offices into Qwen2.5-7B: poison −24.70 vs naive (WIN), −2.98 vs majority (WIN); current +1.77 (NON-INFERIOR); locality +83.54 (WIN, Kiraṇa locus); retention +2.75 (WIN)** |
| SE-4 | **Pratiprasava: lie trace −45.00 vs correction only (WIN; correction leaves 93.5%, +3.7 nats/token); ledger −39.00 (WIN); current −0.19 (NON-INFERIOR); cost 7% of a full retrain (WIN)** |
| SE-5 | **Āpta vs sybil swarms: lie trace −28.50 vs the ledger gate (WIN), chance level; current +0.25 (NON-INFERIOR)** |
| RM-1 | **Gated memory vs raw provenance-tagged memory for gpt-6.1-sol: poison −1.25 (WIN, narrow), truth +0.25 (NON-INFERIOR), prompts 9× smaller; vs last-write-wins −24.38 (WIN)** |
| RM-2 | **Forged provenance in raw memory: poison +71.25 (raises poison); gated memory −71.88 vs injected raw memory (WIN), truth +14.38** |
| RM-3 | **Forged provenance on three frontier models: raw poison 75.6 / 74.4 / 85.6%; gated 0 (WIN for each)** |
| RM-4 | **claude-opus-5-5: raw poison 79.1%; gated 0 (−79.06, WIN), truth 100%** |
| RM-5 | **Escaping or marking closes the forged-line channel: poison 71.9% → 0 (lowers poison); gate vs defenses: no difference shown; gate prompts 15–19× smaller** |
| RM-6 | **gpt-4.1-nano: raw poison 38.8% (sol 1.2%); gated 0 (−38.75, WIN), truth +8.75 (WIN), within 0.75 of sol (NON-INFERIOR)** |
| TM-1 | **Poison 0 vs 18.4% (−18.36, WIN); locality 98.3 vs 9.2% (+89.17, WIN); swarm-lie trace 49.8 vs 93.5% (−43.78, WIN); current 92.4 vs 93.4% (NON-INFERIOR)** |
| HH-1 | **vs LoRA merging: poison −17.56 (WIN); locality +83.33 (WIN); current +2.39 (NON-INFERIOR); the gate alone in front of merging: poison −17.56 (WIN)** |
| Earlier Ember studies | SC VOID, KC INVALID, VS gate FAIL; other mechanism-only bars as listed in §2 |
