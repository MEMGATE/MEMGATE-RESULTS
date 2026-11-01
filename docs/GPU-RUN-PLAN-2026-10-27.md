# GPU run plan: completing the package on Azure's serverless GPUs (27 October 2026)

**Written 27 October 2026, 18:33 IST, at the founder's request ("tests karne se pehle deeply soch ke checklist banao … koi galti na ho").** It is the working plan for every run that needs a GPU, and the checklist each run passes before and after it. It changes no preregistration. A change of machine or plan for a frozen test is declared in its own dated note before that test runs.

## What we have
- **Azure Container Apps, environment `memgate-gpu-swc`** (Sweden Central, resource group `rg-jayeshupp-2640`, Subscription 1). Serverless GPU quota was granted on 27 October at 18:10 IST (request 2610240040000635):
  - 2 NVIDIA A100 80 GB (profile `gpua100`, Consumption-GPU-NC24-A100: 24 vCPUs, 220 GiB);
  - 2 NVIDIA T4 16 GB (profile Consumption-GPU-NC8as-T4, to be added).

  Each job replica gets one GPU, so there are at most four runs at once and two of them on A100s. Billing is per second while a replica runs. The price is in the Estimates section below.
- **Still waiting:**
  - VM GPU quota (2610270040002626);
  - Kaggle's weekly GPU reset (31 October, 05:30 IST);
  - Kaggle's TPU (CCL-4R worlds 9704 and 9705 queued there since 27 October, never started).
- **Running without a GPU of ours:** CCL-5H on GPT-4.1 through Azure's hosted fine-tuning (`runs/c5h-main-gpt41`, dev `runs/c5h-dev-gpt41-20261027`).

## The rules every run follows
1. **Docs before runs.** Every test runs under its frozen preregistration. A change of machine or plan is declared in a dated deviation note, committed and pushed **before** the run starts. Times come from `date`.
2. **Frozen files are not touched.** Before every pack, `git diff --stat` on the frozen list is empty. The list:
   - CCL-4: `cl/clx.py`, `cl/clx_tpu.py`, `cl/ccl2*.py`, `cl/jax_qwen.py`, `cl/ccl1.py`, `cl/ccl4.py`, `cl/merge_runs.py`;
   - CCL-5: `cl/clx5.py`, `cl/ccl5.py`, `cl/colab_pack.py`, `cl/colab_run.py`;
   - CCL-5H: `cl/clx5_hosted.py`, `cl/cl6_evals.py`.
3. **Packs only through the packers' guards.**
   - The fixed hash seed is set (`PYTHONHASHSEED=0`).
   - Main-pool worlds need `--prereg` naming the code's SHA-256.
   - Each run's manifest records the payload's and the code's SHA-256, and both are checked against the document before the run.
4. **A dev run on the same machine type** comes before any main run on it.
5. **Nothing is lost if a replica dies.** The kernel writes its outputs straight to the Azure Files share as it goes. The runner fetches them into `runs/<test>/w<world>/kaggle-output/` and checks them before any analysis:
   - the done line;
   - every arm finished;
   - the untouched model answered every question.
6. **No silent reruns.** One world per job, with a retry limit of 0. A run stopped by the machine is rerun once with the same payload, as the preregistrations allow, and the rerun is recorded.
7. **Secrets stay in Azure.** Storage and registry keys live only in Azure's own configuration; they are never printed, logged or committed. The secret grep runs before every commit.
8. **Cost is logged per run.** The founder hears the estimate before the long runs.
9. **The GPUs are kept busy.** The next jobs are packed and checked before the current ones end, and a watch checks the runs every 30–60 minutes.

## Phase 0: make the machine ready (27 October evening, about 1–2 hours)
| Step | What | Done when |
| --- | --- | --- |
| 0.1 | GPU check job on the A100 profile: `nvidia-smi`, disk (`df -h`), memory, CPUs, download speed from Hugging Face; the longest run time a job allows (replica timeout) | the job ends Succeeded and its output is read; disk size decides where the model cache lives |
| 0.2 | Storage: a storage account in Sweden Central with a file share `ccl`, registered on the environment as `ccl` | a check job writes a file there and it is read back |
| 0.3 | Image: an Azure Container Registry (Basic) and one image built in the cloud (`az acr build`) from a CUDA 12 PyTorch base, plus the kernels' pins (transformers 4.47.1, peft 0.13.2, accelerate 1.1.1) and bitsandbytes (for the 72B). No Docker Hub pulls at run time | a job on the image prints the versions and sees the GPU |
| 0.4 | Runner `cl/aca_run.py`: `start` (upload the payload and kernel, create and start one job per world), `status`, `fetch` (outputs into `kaggle-output/`, checks), `stop`. The run's folder on the share is mounted at `/content` (Colab's layout, so the kernel runs unchanged) | CPU-side checks pass |
| 0.5 | Dev pipeline run on an A100 (about 20 minutes): CCL-4's dev world 9792, two sessions, SYSTEM2. It covers the model download, the untouched model's answers, training, practice, outputs on the share, and the fetch | outputs fetched and complete |
| 0.6 | Price check and a cost note to the founder | sent |

## Phase 1: 12 of 12, CCL-4R on the two A100s (about 3–4 hours)
1. **Deviation note `docs/CCL4R-DEVIATION-AZURE-2026-10-27.md`**, written before any CCL-4R world is packed:
   - Machine: Azure serverless A100 80 GB, one world per job. The code is the frozen GPU runner (`f2a25824…`) in Colab's layout, as CCL-4's 7B ran on Colab's A100 (`docs/CCL4-DEVIATION-7B-COLAB-2026-10-26.md`). The model comes from Hugging Face at `a09a35458c70…`.
   - The preregistration's own rule decides which run of a world counts: the first run of a world counts. The Azure runs start first; the two queued TPU notebooks are cancelled (the founder, from Kaggle's website), and any TPU output is reported but not analysed.
2. **Pack 9704–9707:** `PYTHONHASHSEED=0 python cl/colab_pack.py 970X:main runs/ccl4r-7b-azure/w970X --model 7b --arms SYSTEM2,NAIVE --errors 40 --errors-at 0 --wide --share 1.0 --prereg docs/CCL4R-PREREG-2026-10-27.md`. Check that the payloads match the TPU packs of 9704 and 9705, which were built from the same world.
3. **Run:** 9704 and 9705 first; when they end, 9706 and 9707.
4. **Fetch and check validity**, then run `python cl/ccl4.py report runs/ccl4r-7b-azure/ccl4r-report.json runs/ccl4r-7b-azure/w9704 runs/ccl4r-7b-azure/w9705 runs/ccl4r-7b-azure/w9706 runs/ccl4r-7b-azure/w9707`.
5. **Write up:** result doc, claims rows, and the brief and report updated. Tell the founder.

## Phase 2: CCL-6 dev trial (the two A100s, about 8–10 hours)
1. **The CPU smoke test passes first.** This is the frozen kernel on a 34-session release pack, now running. Any problem is fixed and checked again.
2. **Pack:** `python cl/cl6.py pack 9792:dev runs/ccl6-dev-7b/w9792-offices --model 7b --arms SYSTEM3,NAIVE,REPLAY --errors 40 --errors-at 0`, and the same with `--domain releases` into `w9792-releases`.
3. **Run both** as soon as two A100s are free (CCL-4R first).
4. **Read the results:**
   - the time per arm and per session;
   - every step over 34 sessions (evaluations at 12, 24 and 34, the extra prompts, probes, study and lessons);
   - `cl/ccl6.py report` on the dev outputs;
   - the untouched model's room on release questions;
   - the spread of the safety and IFEval measures, which sets the secondary margin.
5. **Freeze CCL-6:** `docs/CCL6-PREREG-2026-10-2X.md` with `cl6.py hash` and the analysis hashes, committed and pushed before any main pack.

## Phase 3: CCL-6 main (the two A100s, about 12–16 hours)
1. Pack 9708 and 9709 (offices) and 9710 and 9711 (releases) with `--prereg`.
2. Run them two at a time, fetch, and check validity.
3. Run `python cl/ccl6.py report` per domain. Then write the result doc (abilities 13–17 and the core ones over 34 sessions), the claims and the brief.

## Phase 4: the standard baselines with EasyEdit (MEMIT, AlphaEdit; approved 27 October)
1. **Spec `docs/BL1-SPEC-2026-10-2X.md`:**
   - Worlds: CCL-4's main worlds 9702 and 9703, 12 sessions, the same payloads. The comparison then uses the same questions and the existing SYSTEM2, SYSTEM3, NAIVE and untouched answers.
   - Edits: each session's reports as NAIVE receives them. These methods have no gate.
   - The edit format and the hyperparameters: EasyEdit's published configurations for the model where they exist.
   - The measures: H1, H2, H11, H3, H10, H5, H7, H8 and H9, against MEMIT and against AlphaEdit.
2. **Image** with EasyEdit at a pinned commit.
3. **Dev on a T4** with Qwen2.5-1.5B. This runs while the A100s carry phases 1–3. Then the 7B's statistics, which MEMIT and AlphaEdit need, on an A100.
4. **Preregistration BL-1 frozen**, then the 7B runs, the analysis and the result doc.

## Phase 5 (optional): the 72B
CCL-6 at 72B in 4 bits fits one A100 80 GB (CCL-5's 72B ran on 96 GB). This is decided after phase 3's measured time and cost, and the founder hears the cost first.

## Alongside
- **CCL-5H (GPT-4.1):** its chains keep running. The analysis runs when both worlds print `{"done": true}`.
- **Azure tickets:** reply on 2610240040000635 once a job has run (deployed, working). 2610270040002626 stays open.
- **Writing:** the spec of the registry-free learner.
- **The package** (brief v4, report, copies): updated as each result lands. The founder sends it only when everything is complete.

## Checklist for each long run
Before:
- [ ] Its preregistration (or deviation note) is committed and pushed, with times from `date`.
- [ ] Frozen files unchanged; the pack made through the guard; the payload and code SHA-256 in the manifest match the document.
- [ ] Job: the right GPU profile, a replica timeout longer than the run, retry limit 0, the job named after the world, an output folder that is new on the share.
- [ ] A LOG.md entry, and the watch scheduled.

After:
- [ ] Fetched; the done line present; every arm finished; the untouched model answered everything.
- [ ] Outputs committed (payload, kernel, manifest, `kaggle-output/`), with LOG.md.
- [ ] The next job started at once.
- [ ] The analysis exactly as the preregistration states it; the result doc, claims rows and brief updated; the founder told in short Hinglish.

## Estimates
Prices are Azure's list prices for Sweden Central, read on 27 October. The GPU is $0.000688 a second for an A100 and $0.000095 for a T4. The replica's own vCPUs and memory are billed on top of the GPU price: $0.000024 per vCPU-second and $0.000003 per GiB-second. So each A100 job asks for 8 vCPUs and 64 GiB (about $3.86 an hour) instead of the profile's full 24 vCPUs and 220 GiB (about $6.93 an hour). A T4 job with 8 vCPUs and 56 GiB costs about $1.64 an hour.

| Phase | A100 hours |
| --- | --- |
| Phase 1 | about 6 |
| Phase 2 | about 16 |
| Phase 3 | about 32 |
| Phase 4 | about 15 |
| **Total** | **about 70 (about $270, plus a few dollars for storage and the registry)** |

The optional 72B would add about $250 or more.

If nothing blocks:
- Phase 0 on 27 October evening;
- Phase 1 that night;
- Phase 2 by the morning of 28 October;
- Phase 3 on 28 October;
- Phase 4 on 28–29 October.

GPT-4.1 depends on Azure's fine-tuning queue (two to three days or more).

## What phase 0 found (27 October, 18:40–19:10 IST)
- **The A100 profile runs jobs.** The check job saw an NVIDIA A100 80GB PCIe (driver 580, CUDA 13), 24 vCPUs, 216 GB of memory and 475 GB of free disk. A job with 8 vCPUs and 64 GiB and a 20-hour replica timeout is accepted.
- **The container runs as an unprivileged user** (uid 10000, home `/tmp`). It cannot create `/content`, write `/root` or install into site-packages; `/tmp` is writable and has the 468 GB disk.
  - So the run's folder on the share is mounted at `/content`, and the kernel runs unchanged.
  - The model is downloaded into `/tmp/.cache` (about 70 MB/s from Hugging Face).
  - The image already holds the kernel's pinned packages, so the kernel's own `pip install` finds them satisfied.
- **The first dev run (`runs/aca-dev/w9792-s2`) never started its kernel.** Its script could not create `/content` (the cause above), so it is not counted. The second (`runs/aca-dev/w9792-s2b`) runs with the share at `/content`.
- **Infrastructure:**
  - storage account `memgatecclswc` with the share `ccl`, registered on the environment as `ccl`;
  - registry `memgatecclswc` with the image `ccl-gpu:1` (PyTorch 2.5.1, CUDA 12.4, transformers 4.47.1, peft 0.13.2, accelerate 1.1.1, bitsandbytes 0.45.0);
  - the T4 profile `gput4` added;
  - the providers Microsoft.Storage and Microsoft.ContainerRegistry registered on Subscription 1.

## The final list (27 October, 19:55 IST; fixed with the founder, nothing is added after this)
The complete package is these seven:

| # | Item | When |
| --- | --- | --- |
| 1 | 12 of 12 (CCL-4R) | 27 October night |
| 2 | Gemini's five points (CCL-6, 7B) | 28 October |
| 3 | MEMIT and AlphaEdit baselines (BL-1) | 28 October night |
| 4 | **RAG baseline (BL-2).** The untouched 7B, given in its prompt the facts about the question's subject, on CCL-4's worlds 9702 and 9703, in two versions: from the raw stream, and from the gate's admitted memory. Inference only, about 2 A100-hours | 29 October |
| 5 | **Registry-dependence ablation (RG-1).** The learner with fewer, and with no, registry checks, to show how much of its resistance to lies rests on the trusted source | 29 October |
| 6 | **A second open model family (XF-1).** CCL-4's test (SYSTEM2, NAIVE, the untouched model; worlds 9702 and 9703, 12 sessions) on OLMo-2-7B-Instruct (fully open, Apache 2.0), to show the learner is not Qwen-specific. Added at 20:05 when the founder asked for the list to be checked once more; the list is fixed after this. About 3 A100-hours | 29 October |
| 7 | GPT-4.1 (CCL-5H), if done; otherwise reported as running. It does not hold the package back | — |

The package is updated by about 30 October. Gemini's five at 72B, a real news stream instead of simulated sources, broader skills than code migrations, frontier scale and millions of facts go in the package's "next steps with your compute".

## Gemini's six blind spots (added 27 October, 20:55 IST, at the founder's request; under item 2)
Gemini's answer had, besides its 12-point checklist, six things people often forget. The first comparison missed them.

| Blind spot | Where it is answered |
| --- | --- |
| Spurious forgetting; plain fine-tuning with a small learning rate is a strong baseline | NB-1: NAIVE at 2e-5 and 5e-6 on CCL-4's worlds (frozen 21:03) |
| Plasticity lost before performance shows it | CCL-6 H15 (first-check misses, sessions 1–12 against the last ten) |
| Benchmark errors and contamination | Covered: the worlds are built from audited timelines, with blind label checks (100 of 100) |
| A validity interval's edge (transitional periods) | CCL-6 H18 (ability 5b), added before any CCL-6 run |
| Removals one after another | SU-1: four removals in sessions 5, 7, 9 and 11, worlds 9712 and 9713 (frozen 21:03) |
| Sparse mixture-of-experts models; runtime | XF-2: OLMoE-1B-7B on CCL-4's worlds (freezes after its dev run); runtime in CCL-6's cost |

## Item 1 after CCL-4R (27 October, 22:31 IST)
- **CCL-4R is complete and gave 11 of 12, not 12 of 12** (`docs/CCL4R-RESULT-7B-AZURE-2026-10-27.md`). Removal again beat naive retraining (H12 −1.746 [−1.999, −1.501]), but against the untouched model what remained of the corrected errors was +0.217 [−0.026, +0.468], above the margin +0.33 at its upper bound: ability 4 NOT SHOWN. The founder was told at 22:05.
- **Why it may be the wrong reference** (after the fact, not shown): each wrong holder is by design a person of the world whom the learner is often truthfully taught about. The difference sits where that is so (+0.325 over 126 errors) and is not seen where it is not (−0.182 over 34).
- **CCL-4C, inside item 1, not a new item:** removal against the standard reference, the same learner retrained without the removed rows. A dev run on CCL-4R's world 9704 (`docs/CCL4C-DEV-NOTE-2026-10-27.md`) sets the number of fresh worlds (4, 6 or 8); the preregistration (`docs/CCL4C-PREREG-DRAFT-2026-10-27.md`) freezes after it. Each world runs twice (about 1.75 A100-hours a world). If the founder says no, it does not run; if it fails, item 1 is reported as 11 of 12.
- **The A100 order now:** the CCL-4C dev, then the CCL-6 releases dev; then the CCL-4C and CCL-6 main runs side by side, one A100 each; then BL-2, RG-1, XF-1, NB-1, SU-1, XF-2 and BL-1 as before.

## Part B and the new send date (28 October, 11:28 IST, the founder)
The package does not go out on 30 October. It goes out on 10–15 November, after Part B (items 8–15: 72B, the real Wikidata stream, beyond retrieval, clean weights, the three misses, Llama/Gemma/Phi, ten times the facts, a demo labs question themselves). Plan, objections and schedule: `docs/PARTB-PLAN-2026-10-28.md`. The seven items above are Part A and do not change.
