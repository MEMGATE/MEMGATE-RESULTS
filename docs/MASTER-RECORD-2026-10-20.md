# Master record: what we built, how we built it, where everything is, and the plan


> **Update, 23 October 2026:** the copyright holder is now Manish Kumar (memgate-eval LICENSE and NOTICE, `92e0eed`), by the founder's decision. The sender of the package is Manish Kumar, Founder, manishkumar@eagleai.online. Lines below that name Mohit Uppadhyay record the earlier state.

**Owner:** Mohit Uppadhyay. **Written:** 20 October 2026, 19:30 IST, so that the work can be resumed by anyone, at any time, from this repository alone. **This document is internal. Never send it outside.**

---

## 1. What we built, in one paragraph
A **control layer for learning after deployment**. When a language model keeps learning from the world, in its memory or in its weights, the layer decides three things:
- what the model may learn, from a stream of reports by sources of unknown reliability, including attackers;
- where a learned update applies;
- how to take out what a source taught if that source is later caught.

Under preregistration, it keeps planted lies out of memory and out of fine-tuning, and it does so on:
- real 2024–2026 facts;
- real Python API changes;
- the hosted fine-tuning of frontier-class models;
- real Wikidata editors.

Its parts:
- **the gate** (`memgate/gate.py`, and its second version `cl/gate_v2.py`);
- **the scope rule;**
- **the ledger with rollback and replay** (`memgate/ledger.py`);
- **TrainingCheck** (`memgate/health.py` in the library).

## 2. The founder's decisions (do not change without asking)
- **Code:** never given to anyone, not even under NDA ("vo hee to hai hamari chabi"). Outward material shows outcomes only, never the gate's rules, thresholds or mechanism.
- **Outside models:** none are used as helpers. Reviews, labelling and red-teaming are done in-house, by Claude and its own subagents. The only calls that reach outside models are the experiments' own questions: facts plus the gate's verified values, never the rules. Claude Code itself runs on the founder's Azure AI Foundry key.
- **Origin:** the origin of the ideas is never mentioned outward, and no Sanskrit names appear in outward material. The lab's internal record keeps its historical names, because frozen hashes depend on some file names.
- **Owner and licence:** the owner named on the licence and NDA is Mohit Uppadhyay. The licence is proprietary, evaluation only.
- **GitHub:** the account was renamed from ATMAECHO to **MEMGATE** on 20 October 2026. Local remotes point to `github.com/MEMGATE/...`, and the commit identity is MEMGATE.
- **Outreach, later:** results and demos first. A brief, demo links and cold emails through public channels come when the evidence is complete. A domain, NDA and patent lawyer come later, when possible. Nothing is sent by Claude; the founder sends.

## 3. How we built it: the method of work
**Lab discipline, for every experiment:**
1. A **spec**: the question, design, arms, measures and hypotheses.
2. A **dev run** on exposed data, to find bugs and set design choices.
3. A **frozen preregistration**. Code SHA-256 is written in the prereg; the runner refuses the main seeds unless the hash matches. Hypotheses and margins are fixed, and predictions are written down.
4. A **main run** on fresh data, once.
5. A **result doc** reporting every verdict, including failures. Deviations go in a dated note before the result. Corrections are added as dated notes, never by silently rewriting.

**Statistics:** world-level t intervals. A WIN needs the whole interval beyond the margin and every world on the same side. NON-INFERIOR means the interval's lower bound is above −5 pp.

**Honesty tools:**
- `docs/claims.csv` with `scripts/check_claims.py`: every outward sentence must map to a ledger row with its evidence, kind and caveat. 145 rows on 20 October.
- `scripts/check_outward.py`: no hidden words, internal names, paths or secrets in anything that leaves. Key fragments live only in `~/.outward-secrets.txt`, never in a repository.
- Before every commit: the check that no added line contains a key fragment.

**Infrastructure:**
- **Azure VM** (Windows), with the Python venv `C:\Users\azureuser\venvs\pramana-claude`.
- **Azure AI Foundry, subscription `8b49b382…`, resource group `rg-jayeshupp-2640`:**
  - hosted fine-tuning on `jayeshupp-8050-resource` and the `memgate-ft-*` resources: up to 3 running jobs per resource, developer-tier deployments, deleted after use;
  - the frontier models: gpt-6.1-sol, gpt-6-astra, claude-opus-5-5, grok-4.7, gpt-4.1;
  - Llama 4 Maverick.
- **Modal GPUs** for the open 7B model work (Qwen2.5-7B LoRA).

**How the gate grew.** Each rule was added only after an experiment exposed a failure, and was then tested in a new preregistered experiment:

| Experiment | Failure found | Rule added or tested |
| --- | --- | --- |
| SE-1 | naive fine-tuning learned 23% lies | registry first; testimony only from two trusted sources |
| SE-2 | stealthy and colluding liars | questions to the registry on doubt, within a budget |
| SE-3 (real Wikidata facts) | honest late sources looked like liars; learning damaged old facts | lag is not lying; the scope rule |
| SE-4 | sleepers: honest first, then lying | ledger, rollback and replay |
| SE-5 | sybil swarms | trust only with a confirmed track record |
| TM-1 | all attackers together, 1,341 offices | the whole engine |
| HH-1 | against LoRA merging | the engine, and the gate in front of merging |
| RM-1 to RM-6 | memory injection on frontier models | the gate in front of retrieval memory |
| stale-liar audit | floods of past holders | gate v2: staleness strikes |
| AU-1 | attackers designed against the rules; strong baselines | none needed |
| AU-2 | "only a threshold?" and "needs a perfect registry?" | gate v2 confirmed as the primary gate |

**How we run.** Claude works in this repository. Long runs go in the background with logs in `/tmp`. Scheduled checks resume work, and every step is committed and pushed. Subagents build pages and checkers, and fresh-eyed reviews are done in-house.

## 4. Results so far (20 October, 19:30; updated 23:00)
**Confirmatory (preregistered main):**

| Test | What it shows | Verdict |
| --- | --- | --- |
| SE-3, SE-5, TM-1, HH-1 (7B, real facts) | poison 0 against 17–24% for naive learning | WIN |
| SE-4 | rollback cuts the lie trace to 48.5% against 93.5%. The apparent residue on lies actually taught (67.9% against 57.1%) was an effect of training, not of the lie (UNDO-1). | WIN |
| RM-2 to RM-6 (memory) | forged provenance moves frontier models 72–86%; the gate gives 0. Escaping or spotlighting also stops that attack (RM-5). | WIN |
| **AU-1** (20 worlds) | +11.3 pp over registry-only; 7.7 and 2.4 pp fewer attacker values ever held than majority vote and truth discovery; no adaptive attacker got through | 4 of 4 WIN |
| **AU-2** (20 worlds) | gate v2 lies above truth discovery's whole threshold curve; with the registry wrong 5% of the time it keeps a +9.4 pp lead | 4 of 4 WIN or NON-INFERIOR |
| **CD-1 memory arms** (5 worlds, real Python API changes) | forged line 52–82% → 0–0.7% with the gate | H4 WIN 5 of 5; H5 non-inferior 4 of 5, not shown for gpt-6-astra |
| RV-1 | real editors | INVALID (instrument); replaced by RV-2 |
| **RV-2** (real Wikidata editors, main half) | naive learning would take in 149 wrong values; the gate 2, with no honest editor dismissed and the same last-month accuracy (96.82% against 96.84%) | 3 of 3 predictions held |
| **OM-1** (Llama 4 Maverick, 10 worlds) | the forged line moves 40.5% of attacked offices and 37.3% of attacked API usages; the gate's memory gives 0.0% and lifts current answers by 27 and 23 points | H4 WIN, H5 NON-INFERIOR, both domains |
| **AU-3** (20 worlds, seven in-house white-box attackers) | an attacker that farms trust and spends the budget on decoys got v1/v2 to hold fabricated values on up to 7.4% of offices; gate v3 (random audits at entry) holds the worst case to 0.18% at the same coverage, no honest source dismissed | 3 of 3 held (H1, H2 WIN; H3 NON-INFERIOR) |
| **UNDO-1** (7 worlds, 175 lies taught then removed) | after rollback the model scores the lies as a never-poisoned model does: −0.01 nats [−0.24, +0.22], trace 49.8% in both. A lie overwritten by the truth stays inside: never said, yet preferred 95.2% of the time, +3.55 nats above rollback. Cost 6.7–7.1% of a retrain. | H1 EQUIVALENT, H2 WIN |

**Dev or partial, not yet confirmatory:**
- **RT-1 dev:** a poisoned GPT-4.1 still names the lie on 3.1% of attacked offices with a verified memory, against 0% for the gate-trained model. n = 98; Fisher p = 0.25.
- **FT-2 main world 8200 memory arms:** the forged line moves the five models 85.8–100%; the gate gives 0.

**Outside review** (four frontier models acting as lab scientists, before the no-outside-helpers decision; `runs/reviews-20261020-outside`):
- novelty 3–4/10, rigour 5–6/10, value 3–6/10;
- 3 of 4 would take a meeting.
- **Their must-haves:** no oracle registry (AU-2 answered this with a noisy registry); tuned baselines (AU-2 answered); external attackers (declined: in-house only); exact undo (answered by UNDO-1, 20 October 23:00).

## 5. Where everything is
- **Lab repository:** `C:\Users\azureuser\Downloads\eagleai-main\pramana-agi`, remote `MEMGATE/pramana-agi` (private), Claude's lab branch. Work lives in `claude_lab/`:
  - `cl/`: experiment runners. Frozen ones are noted in each prereg.
  - `docs/`: specs, preregs, results, deviations, the claims ledger, this record.
  - `runs/`: recorded answers and summaries.
  - `site/`: demo pages. The best four are `arena/`, `time-machine-gpt41/`, `frontier/` and `one-line/`.
  - `scripts/`: the outward and claims checkers.
  - `outreach/`: related work and lab channels. Internal.
  - `data/`: the Wikidata snapshot, edit history and revisions.
- **Library for evaluation:**
  - `C:\Users\azureuser\Downloads\eagleai-main\memgate-clean` → `MEMGATE/memgate-eval` (private). Its history is cleaned and every commit is by MEMGATE. It has `pip install .`, 11 tests, examples, API docs, and a reproduction that matches all 20 recorded audit worlds. The licence is in the owner's name.
  - The old copy, `memgate` → `MEMGATE/memgate`, is untouched.
- **Memory notes for Claude:** `C:\Users\azureuser\.claude\projects\C--Users-azureuser-Downloads-eagleai-main\memory\`, indexed in MEMORY.md.

## 6. What is running now, and how to resume it
| Run | Where | Log | Expected |
| --- | --- | --- | --- |
| FT-1 world 9102, ENGINE blocks 1–3 (gpt-4.1-nano) | jayeshupp-8050-resource | `/tmp/ft1-main-9102.log` | tonight or tomorrow; the GPU queue is long |
| FT-2 main worlds 8200–8204 (GPT-4.1) | memgate-ft-* | `/tmp/ft2-main-82NN.log` | 21–22 Oct |
| CD-1 main worlds 9300–9304 (GPT-4.1) | memgate-ft-* and jayeshupp | `/tmp/cd1-main-93NN.log` | 21–22 Oct |
| FT-2 memory arms, worlds 8201–8204 | Azure models | `/tmp/ft2-main-memory.log` | 21 Oct (grok is slow) |
| OM-1, Llama 4 memory arms | `llama-4-maverick` on jayeshupp | `/tmp/om1-chain-eus2.log`, then `/tmp/om1-chain-eus2-b.log` (worlds 8202–8204 and 9302–9304, restarted 20 Oct 22:20) | 21–22 Oct |
| FT-2 and CD-1 dev | memgate-ft-ncus, swc2 | `/tmp/ft2-dev.log`, `/tmp/cd1-dev.log` | 21 Oct |
| RV-2 | done 20 Oct 20:15 | | |
| UNDO-1 | done 20 Oct 23:00 (Modal credit of the active workspace nearly used up) | | |

**Rules for resuming:**
- **A dead world:** move its folder aside and rerun once with `--reuse <every succeeded job id>`, with the same `--account` and `--base-account`. Record it in a dated deviation note before the result.
- **A job "enqueued, waiting for jobs ahead"** for more than 2 hours while later jobs start: cancel it, resubmit it identically, and restart with `--reuse`. Waiting for GPUs is normal.
- **Data safety check refusals:** they are not deterministic. One rerun is allowed.
- **Deployment refusals with error 715-123420 ("unusual activity"):** do not retry in a loop and never create test deployments. Read other runs' logs to see whether the block has lifted.
- **When the runs finish:**
  - `cl/ft1_report.py`, then FT1-RESULT;
  - `cl/ft2_report.py` on FT-2's and CD-1's five worlds, then FT2-RESULT and CD1-RESULT;
  - `cl/rt1.py ask` on FT-2's session-12 models (prereg RT1-PREREG) **with `--keep`**, then RT1-RESULT;
  - within 24 hours of each world's RT-1 run, while its developer-tier deployments live: `cl/rt2.py ask runs/ft2-main-20261020/w<seed> 12 runs/rt2-main-<date>/w<seed> --prereg docs/RT2-PREREG-2026-10-20.md`, then `cl/rt2.py score` on the five worlds and RT2-RESULT. RT-2 never creates a deployment;
  - OM-1's report with `ft2_report` functions;
  - regenerate the pages: `cl/ft2_page.py`, `cl/one_line_page.py`, `cl/memory_page.py`.
- **Frozen files:** never edit a file listed in a prereg's hash while its runs may need reruns.

## 7. What we have that has value
1. **The control layer:** gate v2, the scope rule, the ledger and TrainingCheck. Private.
2. **Benchmarks no one else has:**
   - real 2024–26 office changes;
   - real Python API changes, with exact dates and 536 fabricated APIs and packages;
   - the real Wikidata edit history with revision-level claims;
   - nine attacker types.
3. **The preregistered evidence base** of about 70 experiments, with the claims ledger.
4. **Findings about the labs' own models:**
   - forged memory lines;
   - poison that survives a verified memory;
   - hosted fine-tunes that return garbled models while reporting success;
   - stale knowledge (the best frontier model knows 43.6% of recent changes).
5. **The demos.**
6. **The way of working:** fast, preregistered and self-checking.

## 8. What comes next
**Next two days (evidence first):**
1. RV-2 main: done (20:15). UNDO-1: done (23:00).
2. FT-1 result: when world 9102 finishes.
3. FT-2 and CD-1 main results, then RT-1 main on FT-2's models: 21–22 October.
4. OM-1 results for all worlds.
5. Regenerate all pages from main data, and the GPT-4.1 time machine from FT-2 main.
6. **Done 21 Oct:** `site/time-machine` (TM-1) is outcomes-only now. Its notes, arm names and stories no longer describe the method, and the reasons behind each held value were removed from its data and from `cl/tm1_page.py`. The landing page links it again. The landing page (`site/index.html`, built by `cl/home_page.py`) shows only VERIFIED ledger rows marked `demo:home`.

**Then the package (when the founder says):**
- a two-page brief, results only, checked by `check_claims.py --text`;
- the demo pages on a public link, results only;
- five cold emails through public channels (`outreach/CHANNELS.md`);
- Q&A preparation.

The founder approves and sends.

**Open science questions (the reviewers' remaining must-haves):**
- **Exact undo:** answered by UNDO-1. Still open: longer exposure before the catch, full fine-tuning, deletion requests (all of a source's contributions).
- **A bigger open model:** 70B, with a real untrusted stream and a long horizon.
- **Gemma (Google):** not on Azure; it needs Modal.

**Later (when possible):**
- a domain and email;
- an NDA template;
- a provisional patent, with a technical disclosure prepared for a lawyer, never for labs.

## 9. Lessons and risks to remember
- **Azure:**
  - GPU queues of up to 8+ hours;
  - one resource queue jammed on a fine-tuned base model;
  - non-deterministic data safety checks;
  - a temporary "unusual activity" block on deployments after a Meta-model deployment attempt.
  - Plan for days, not hours, on hosted fine-tuning.
- **A security slip:** on 20 October seven short key fragments were committed in a checker script (lab commit `9aec84f3`). They were removed the same hour. The founder chose to leave the history as is. Fragments now live only outside every repository.
- **Shell edits:** heredocs turn `\\n` into real newlines; use the Edit tool for any backslash.
- **Outward honesty:**
  - "locality" comes from routing by design;
  - escaping also stops the forged line;
  - rollback leaves residue;
  - the registry is the truth in simulation, and AU-2 tested a noisy one.
  - Never overstate. The claims ledger exists for this.

## State on 21 October 2026, 11:15 IST (handoff)
**Running, all detached** (`scripts/launch_detached.py`; logs in `/tmp`):

| Run | Log |
| --- | --- |
| FT-2 main worlds 8200, 8201, 8204 | `ft2-main-<seed>.log` |
| CD-1 main worlds 9300, 9302, 9303, 9304 | `cd1-main-<seed>.log` |
| FT-1 world 9102: ENGINE block 1 training since 10:15 | `ft1-main-9102.log` |
| FT-2 memory arms: world 8203's remainder, then 8204 | `ft2-main-memory.log` |
| RT-1 then RT-2 main on world 8202 | `rt-main-8202.log` |

**Finished:**
- FT-2 world 8202 and CD-1 world 9301;
- OM-1 (`docs/OM1-RESULT-2026-10-21.md`);
- AU-3 (`docs/AU3-RESULT-2026-10-21.md`);
- UNDO-1;
- RV-2.

**Stopped:** FT-2 world 8203, at Azure's data safety check (20 Oct). Never resubmit it.

**Next:**
- **RP-1 main.** Spec in `docs/RP1-SPEC-2026-10-21.md`, dev in `runs/rp1-dev-20261021`.
  - Add a code-hash guard to `cl/rp1.py`.
  - Write the prereg. Primary: PREVIOUS, GATED+ against GATED. Also REVERSE, GATED against NONE, and STILL under GATED.
  - Models: the four frontier models, `gpt-4.1-base` on memgate-ft-ncus, and `llama-4-maverick` on jayeshupp, registered as `cl/om1.py` does.
  - Main offices: `pool[50:350]`.
- **When worlds finish:** RT-1 then RT-2 on each finished FT-2 world (watch prompt in the session); then FT2/CD1/RT1/RT2/FT1 results.

**Rules learned on 21 Oct:**
- A session that ends kills runners it started directly. Start them with `launch_detached.py`.
- Session crons die with the session: recreate the two-hourly watch.
- A block Azure's data safety check rejected is never resubmitted.
- Work that writes new attacks tends to get responses stopped, so keep to defensive, measurement work.

## State on 21 October 2026, 16:30 IST
**The founder's goal since 14:00:** close every remaining continual-learning gap and build the complete system (`docs/ROADMAP-CL-2026-10-21.md`).

**Azure:**
- only the special GPU VM quota was refused, for an outstanding bill;
- every model, and hosted fine-tuning, keep working, with no limit on spending;
- GPU work goes through the hosted fine-tuning queues, filling every free slot.

**Done today (result docs in `docs/`):**
- **RP-2:** fine-tuning does not carry a new fact to what follows from it.
- **RF-1:** no registry; 0.00% attacker values in 20 worlds; 82.6% end coverage.
- **EV-1:** the released library as the registry.
- **FR-2:** a calibrated probability that a stored value still holds.
- **SK-1:** a gated skill library let all six models migrate every program.

**Explorations, LOG only:** RF-2, link statistics, FR-1, the RP-4 record check.

**Running, all detached:**

| Run | Log or place | Next step when done |
| --- | --- | --- |
| RP-1 main (21,600 questions) | `/tmp/rp1-main.log` | `python cl/rp1.py report runs/rp1-main-20261021`, RP1-RESULT, then update RP2-RESULT's interim memory line, and run `cl/rp1_twin.py` (yes-answer twin, descriptive) |
| RP-4 main (8,256) | `/tmp/rp4-main.log` | `python cl/rp4.py report runs/rp4-main-20261021`, RP4-RESULT |
| RP-3 dev (eus2) and main jobs (pre-submitted on swc2) | `/tmp/rp3-dev.log`, `runs/rp3-main-pretrain-20261021/jobs.json` | score dev, freeze RP3-PREREG, then `cl/rp3.py run main ... --reuse <the three main jobs>` |
| SK-2 jobs (jayeshupp) | `sk1/sk2-jobs.json` | `sk1/sk2.py ask dev`, prereg, `ask main` |
| FT-1 9102, FT-2 8200 and 8204, CD-1 9300, 9302 and 9303, FT-2 memory 8204 | `/tmp/*-main-*.log` | the result docs, per the watch prompts |

**Held:**
- FT-2 8201 has a single retry at 16:53.
- CD-1 9304 stays held; its single retry was refused again.
- FT-2 8203 stopped at Azure's data safety check and is never resubmitted.

**Next on the roadmap:**
- **the integrated layer:** one module that joins gate, registry-free admission, time and confidence, derived lines, skills and undo, with an end-to-end test;
- **LR-1:** the gate learns its own rules;
- **SC-1:** interference at scale. Its first design was too easy: lexical retrieval found the right line 60 of 60 times. It needs versioned or distracting memory.

## State on 21 October 2026, 18:30 IST
**Goal (the founder, from 17:00):** the whole ideal of continual learning. Every property in the field summary is to be attempted; what cannot be reached is recorded with evidence. The plan is in `docs/ROADMAP-CL-2026-10-21.md`.

**Azure:**
- The bill is paid.
- **GPU quota ticket 2610200030003599** (NC A100 v4, 24 vCPUs, East US 2): Microsoft declined it on 21 October for the unpaid balance. The founder replied at 16:05 IST that payment is complete. The ticket is open, waiting for Microsoft.
- **Fine-tuning:** the developer training tier starts jobs at once (`cl/ft_accounts.py`). New single-block jobs run on it.

**Done since 16:30 (result docs in `docs/`):**
- **RP-4:** a derived line removed stale answers for the post a coach had left (−12.31 pp).
- **ML-G:** the gate tunes its own strictness.
- **RP-1:** one verified sentence carried a new fact to the reverse and "still" questions. Writing the previous holder in took that answer to 99–100%.
- **RC-1:** re-checking first what is least likely to hold needed 35–58% fewer checks.
- **EF-1:** incremental gates, identical decisions. An update to 300,000 facts takes 40 ms.
- **LR-1:** update rules learned from history were right 92.9% of the time on later data.

**Preregistered and running (detached):**

| Run | Log | Next step |
| --- | --- | --- |
| ML-M main (1,584 questions) | `/tmp/mlm-main.log` | `python cl/mlm.py score runs/mlm-main-20261021`, MLM-RESULT |
| SC-2 main (4,800) | `/tmp/sc2-main.log` | `python cl/sc2.py score runs/sc2-main-20261021`, SC2-RESULT |
| MC-1 dev (3,072) | `/tmp/mc1-dev.log` | `python cl/mc1.py score runs/mc1-dev-20261021`, then prereg and main (seed 8800) |
| DR-1 dev | `/tmp/dr1-dev.log` | `python sk1/dr1.py score runs/dr1-dev-20261021`, then decide prereg or redesign |
| LS-1 live capture (168 h, from 17:55) | `/tmp/ls1-capture.log`, `runs/ls1-capture-20261021/` | after about 9 days, fetch revert tags for the first 48 hours (dev); freeze the prereg; then fetch the rest |
| RP-3 dev and main, mini and nano; SK-2 (developer tier, plus global copies) | `runs/devtier-copies-20261021.json` | score dev, prereg, main |
| FT-1 9102, FT-2 8200, 8201 and 8204, CD-1 9300, 9302 and 9303 | `/tmp/*-main-*.log` | result docs per the watch prompts; RT-1, then RT-2 |

**Held:** CD-1 9304 (refused by Azure, no further retry). FT-2 8203 (Azure's data safety check; never resubmitted).

## State on 21 October 2026, 21:00 IST
**Done since 18:30** (result docs in `docs/`; every claim in the ledger, 0 failures; landing page and brief updated):
- **ML-M:** lessons from a model's own checked mistakes cut stale answers on new cases by 11.81 pp.
- **SC-2:** undated old versions made six models name a past holder 25–84% of the time; the layer's memory gave 99.5–100% current.
- **GI-1:** the same lessons, put in every prompt, raised unrelated answers by 5.44 pp and did no harm.
- **LR-1:** update rules learned from history were right 92.9% of the time on later data.
- **DL-1:** exact deletion requests (`memgate/forget.py`).
- **RP-3:** dev done and preregistration frozen (transfer +21.3 pp in dev).
- **MC-1:** preregistration frozen.

**Discovered:** Azure's hosted training also trains open-weight models, with no GPU quota (`docs/GPU-PLAN-2026-10-21.md`).
- Llama-3.3-70B (format Meta) and Qwen3-32B (format Alibaba) fine-tuned models deploy and are being asked for RP-3 (`cl/rp3_open_ask.py`, hash in the RP-3 prereg addendum).
- gpt-oss-120b's fine-tuned models need provisioned capacity, which the subscription lacks. That replicate is not evaluated.

**eus2b's 715 block has lifted.** CD-1 world 9304 was restarted at about 20:55 and is probing (log `/tmp/cd1-main-9304-r3.log`).

**Running:**

| Run | Log | Next |
| --- | --- | --- |
| MC-1 main (11,712) | `/tmp/mc1-main.log` | `python cl/mc1.py score runs/mc1-main-20261021`, MC1-RESULT |
| RP-3 open: Llama-70B, Qwen-32B | `/tmp/rp3-open-llama.log`, `/tmp/rp3-open-qwen.log` | after all three arms: `python cl/rp3_open_ask.py report runs/rp3-open-<model>-20261021` |
| RP-3 main: GPT-4.1 (swc2 global or ncus3 developer tier), mini, nano | jobs queued on Azure | `cl/rp3.py run main ... --reuse` on the first complete set (rule in the RP-3 prereg) |
| DR-2 dev (llama part) | `/tmp/dr2-dev-llama.log` | score; freeze the prereg; main on `sk1/build-dr2.json` with gpt-4.1-base and llama |
| SK-2 dev (asker waiting for the global GATED job) | `/tmp/sk2-dev.log` | if the developer-tier pair finishes first, restart the asker with `--jobs sk1/sk2-jobs-devtier.json` |
| DR-1 dev (grok, slow) | `/tmp/dr1-dev.log` | superseded by DR-2; score descriptively |
| LS-1 live capture until 28 Oct | `/tmp/ls1-capture.log` | outcomes about 30 days after capture ends |
| FT-1 9102 | — | deadline 22 Oct 10:15 for its stalled job, else ENGINE is INVALID (FT1-DEVIATIONS) |
| FT-2 8200, 8201, 8204; CD-1 9300, 9302, 9303, 9304 | `/tmp/*-main-*.log` | results when they finish; then RT-1 and RT-2 |

## State on 22 October 2026, 04:56 IST
**Done since 21:00 yesterday.** Result docs are in `docs/`. The ledger has 187 rows and 0 failures. The brief v2 and the landing page were updated.
- **MC-1, DR-2, SC-2:** results written.
- **RP-3 replicates:** gpt-4.1-mini and gpt-4.1-nano (H1–H4 WIN), Llama-3.3-70B (H1–H4 WIN; H6 is a locality cost), Qwen3-32B (H1 and H2 WIN; think-block artifact, sensitivity copy), Ministral-3B (uninformative).
- **SK-2:** skills in the weights, verified library against poisoned: +50.0 pp, WIN. A 150-token cap bug was found in dev and fixed.
- **CN-1:** model-free, what to consolidate into the weights. Reversals fell from 7.05% to 1.11%, WIN.
- **Ledger rows** for EF-1 and DL-1.
- **Report v3 Part II draft:** `outreach/REPORT-v3-part-cl-draft.md`, problem by problem, 0 findings.

**CH-1** (chains through a changed fact; prereg `docs/CH1-PREREG-2026-10-22.md`, hash `579c95ed…`, two addenda).
- **Dev:** memory composes (+54 pp); weights compose only when the model names the person first.
- **Main memory route:** running (`/tmp/ch1-main-memory.log`, 14,736 questions, done about 06:30).
- **Weights route:** the mini base is answered.
- **Stopped by Azure's 715 refusal:** mini's fine-tuned arms, and the nano, Llama and Qwen families.
- **Restart them one at a time through `cl/ch1_run.py`.** Its deployments are spaced five minutes apart across processes, through a lock in `~/cd1-tools/deploy-spacing.json`.

**The 715 refusal.** About twelve deployment requests in fifteen minutes, from 04:00 to 04:15, drew it. Mini's retry at 04:40 was refused too. Next single attempt: about 05:30.

**Azure GPU queues are slow.** Estimated finishes for the FT-2, CD-1 and FT-1 block jobs are 25 October to 4 November.
- FT-1 9102's ENGINE job will miss the 10:15 deadline, so its ENGINE arm becomes INVALID and FT-1 is analysed on 9100 and 9101. A session cron is set for 10:17.
- RP-3 GPT-4.1 main: the dev2 set has DIRECT and MORE done and FOLLOW running. The queue (`cl/rp3_main_queue.py`, PID 11360) runs it when complete.

**Running processes:**
- the FT-2 world runners 8200, 8201, 8204 and the CD-1 world runners 9300, 9302, 9303 (since 21 Oct 10:49);
- FT-1 9102;
- the RP-3 queue;
- LS-1 capture;
- CH-1 memory route;
- the local http.server for the site.

**Next:**
- CH-1 weights families, one at a time;
- CH-1 report;
- RP3-RESULT when GPT-4.1 is done;
- FT-1 result at 10:17;
- report v3, merged into memgate-clean.

## State on 22 October 2026, 08:30 IST
**Done since 04:56:**
- **RP-3 main (GPT-4.1):** H1–H4 WIN, transfer +20.22 pp. Untouched offices fell from 90.3% to 25–30% after one job.
- **CH-1:** H1 +43.76 WIN; H3 +36.05 WIN; H4 UNDETERMINED (nano).
- **Descriptive:** gpt-4.1-nano's untouched offices fell from 89.3% to 0.0% after one job.
- **Records:**
  - the ledger has 195 rows and 0 failures;
  - the brief v2 has about 1,600 words and 0 findings;
  - the report's Part II draft has 0 findings;
  - the home page has 60 rows.

**Running:**
- FT-2 worlds 8200, 8201 and 8204; CD-1 worlds 9300, 9302 and 9303; FT-1 9102. Their Azure jobs are estimated to finish between 25 October and 4 November.
- LS-1 capture, until 28 October.
- Nothing else of ours; no CH-1 or RP-3 process is left.

**Next:**
- **10:17 (cron):** FT-1. If 9102's ENGINE arm misses the deadline, it is INVALID, and FT-1 is reported on 9100 and 9101.
- **Package:** merge the report's Part II into memgate-clean's REPORT.md, with the date and summary updated.
- **Optional, descriptive:** RP-3 FROZEN for Llama-70B. It needs one base deployment at capacity 20, spaced from any other.
- **Open gaps (scorecard):** other kinds of procedure; an outside red team; the lab's own training loop above 7B (GPU ticket, founder's decision); LS-1 outcomes.

## State on 22 October 2026, 16:05 IST
**Done since 08:30 (results, each preregistered, committed and pushed):**
- **RP-3 part 2** (Qwen2.5-7B, the lab's own LoRA loop, Modal A100): H1–H4 WIN (transfer +5.11), H5 and H6 non-inferior. See `docs/RP3-RESULT-OPEN-LORA-2026-10-22.md`.
- **CN-2** (CN-1's rule in a trained 7B model's answers): stale 0.61% → 0.12%, H1 WIN 20/20; right +4.62, non-inferior. See `docs/CN2-RESULT-2026-10-22.md`.
- **PR-1** (a changed tax procedure, in memory and under a forged update): H1 +81.4 WIN, H2 +79.1 WIN. See `docs/PR1-RESULT-2026-10-22.md`.
- **SC-3** (memory at scale): H1 −1.67, not shown; H2 −2.92; H3 keyed +3.67 WIN. See `docs/SC3-RESULT-2026-10-22.md`.
- **CH-2** (three-step chains, memory): H1 +52.0 WIN; H2 non-inferior. See `docs/CH2-RESULT-2026-10-22.md`.
- **Outreach:** the short brief, the report's Part II (also in memgate-clean) and the home page (69 rows) carry the new rows. The ledger has 208 rows and 0 failures.

**Running:**
- **TQ-1 main** (date questions before and after a change; frozen `b0dc77f1`): 10,800 questions, about 1,250 asked at 16:03. Score it with `python cl/tq1.py report runs/tq1-main-20261022`.
- **FT-2, CD-1 and FT-1:** three copies of each running world, on the global, developer and Standard tiers. `cl/first_finished3.py` applies the first-of-three rule (deviation note, 22 October 13:58). The Standard tier started jobs within about 20 minutes; all 13 were running at 14:52.
- **The gpt-4.1-mini replicate:** developer-tier and Standard-tier copies (deviation note, 15:50). The first copy of each world to finish is reported.
- **LS-1 capture,** until 28 October.
- **A Modal ping loop** (background task), which reports when the workspace runs again.

**Blocked:**
- **Modal workspace mohitaureus** has been paused since 13:22 (billing: $43.63 this month against the $30 credit).
- **Azure GPU quota:** Microsoft declined SR 2610220040001027 at 13:23 on payment history. On the founder's instruction, a reply with the invoice facts went out at 15:34 (all invoices Paid). Opening a billing "Account Review" ticket from here was refused by the session's permission check; the founder can open it in the portal.
- **What waits for GPUs:** the 72B queue in `docs/GPU-PLAN-2026-10-21.md` (benchmark, bf16 probe, OLMo-2 RP-3, RP-3 72B, TM-1 72B, CN-2 72B).

**Founder's instructions today:**
- Budget unlimited (13:15).
- Keep and use the Azure fine-tuning capacity until all the work is done ("usse chodna mat", 15:45).
- Report in short Hinglish.
