# GPU cost ledger (Modal), 18 October 2026

**Source.** `modal billing report --start 2026-10-17 --resolution h --show-resources`. That command covers complete hours only and itemizes $27.69. `modal billing summary` shows $28.64 of compute; the difference is the last, incomplete hour. The credit was $30.

## By experiment

| Experiment | Runs | Cost |
| --- | --- | ---: |
| SE-1 (Qwen2.5-0.5B, A10G) | smoke, dev a, dev b, main | $2.65 |
| SE-2 (Qwen2.5-1.5B, A10G) | dev | $2.99 |
| | **main** | **$5.81** |
| Probes (Pythia ×3, Qwen ×3, the 7B pool probe; A10G) | — | $0.33 |
| WikiFactDiff extraction (CPU) | — | $0.00 |
| SE-3 (Qwen2.5-7B, L40S) | 2 smoke tasks | $0.55 |
| | 6 diagnostic tasks (svādhyāya, lower intensity, locus) | $1.67 |
| | dev a | $4.00 |
| | dev b | $3.60 |
| | **main** | **$6.06** |
| **Total itemized** | | **$27.69** |

## By kind of run and by resource

| Kind of run | Cost | Share |
| --- | ---: | ---: |
| Main runs (the preregistered tests: SE-1 $1.26, SE-2 $5.81, SE-3 $6.06) | about $13.1 | 47% |
| Dev runs (on exposed data, before each freeze) | about $12.0 | 43% |
| Smokes, diagnostics and probes | about $2.6 | 9% |

| Resource | Cost |
| --- | ---: |
| GPU (A10G $11.16, L40S $15.41) | $26.57 |
| CPU | $0.87 |
| Memory | $0.20 |
| Network | $0.06 |

Storage of the model cache volume is metered separately ($14.97), but it falls within Modal's free storage and costs nothing.

## Why the running estimates were low

The runners estimate cost from the seconds measured inside each task. Modal bills from container start, which includes:
- image start;
- loading the model from the volume;
- the tail after the last measured second.

On SE-3 that added about 15% (dev a: $3.42 estimated, $4.00 billed). The small runs (smokes, diagnostics, probes, SE-1's dev runs) were also not added up as they happened. Before SE-3's main run, the running total said about $13; the bill was $21.6.

## From now on

- Check `modal billing report --for today --resolution h` after every run, and add it to this ledger.
- Before each experiment, state its expected cost with a 20% margin, and stop if the remaining credit cannot cover it.
- **Cheaper dev phases:**
  - two dev worlds instead of four;
  - reuse FROZEN and NAIVE tasks when their code path is unchanged;
  - re-run only the arms an amendment touches.
- **SE-4 expected cost:** 5 arms on L40S. Dev with two worlds is about $3; the main run on 8 worlds about $8–9. About $12 in all.

## Second workspace: `jayeshupp` (from 18 October 2026, night)

The first workspace's credit was used up, so the user approved a second Modal workspace from their phone.

| Run | Cost | Note |
| --- | ---: | --- |
| Model download into the new volume, SE-4 smoke task (PRATIPRASAVA, dev world 0), CPU check of the likelihood helper | $0.32 | |
| SE-4 dev run a (2 worlds × 5 arms) | about $2.8 | billed |
| Running total before the SE-4 main run | $3.13 | |
| SE-4 main run (41 tasks) | about $9.5 | billed: $12.61 for complete hours today, less $3.13 before |
| **Running total, second workspace** | **about $12.9** | `modal billing summary` |

## Azure Foundry (API, no GPU), 19 October 2026

The calls go to `gpt-6.1-sol` on the user's Azure resource. Their cost falls on the Azure subscription, not Modal. The token counts are recorded in each run's `manifest.json`.

| Run | Calls | Input tokens | Output tokens |
| --- | ---: | ---: | ---: |
| RM-1 dev a and b | 8,000 | 1.13 M | 0.29 M |
| RM-1 main | 16,000 | 2.33 M | 0.58 M |
| RM-2 dev a and b | 3,200 | 0.95 M | 0.04 M |
| RM-2 main | 6,400 | 1.90 M | 0.07 M |
| RM-3 dev (3 models × 600) | 1,800 | 0.67 M | 0.02 M (+0.25 M grok reasoning) |
| RM-3 main (3 models × 4,800) | 14,400 | 5.47 M | 0.13 M (+2.36 M grok reasoning) |
| RM-4 dev a and b (claude-opus-5-5) | 1,200 | 0.61 M | 0.04 M |
| RM-4 main (claude-opus-5-5) | 4,800 | 2.65 M | 0.17 M |
| RM-5 dev and main (gpt-6.1-sol) | 7,200 | 3.65 M | 0.08 M |
| RM-6 dev a, b and main (gpt-4.1-nano) | 20,000 | 2.88 M | 0.11 M |

**Deployments added on 19 October.** All are GlobalStandard and billed per token, with nothing charged while idle:
- `gpt-4.1-nano`, used by RM-6;
- `Phi-4-mini-instruct` and `Ministral-3B`, at capacity 1 and unused, because their quota is 20 thousand tokens a minute.

## Second workspace, continued (19 October)

| Run | Cost | Note |
| --- | ---: | --- |
| SE-5 (dev and main) | about $9.4 | billed, before TM-1 |
| TM-1 dev (3 tasks, 100.5 GPU-minutes) | about $4.4 | billed |
| **Running total, second workspace** | **$26.68 of $30** | `modal billing summary`; TM-1's main run (about $9) does not fit |

## Third workspace: `mohitaureus` (19 October 2026, afternoon)

The user supplied this workspace's token. It is stored only in the Modal CLI's profile file.

| Run | Cost | Note |
| --- | ---: | --- |
| TM-1 main (6 tasks, 197.8 GPU-minutes, model download into a new volume) | $8.35 | `modal billing summary` after the run |
| Merge check (CPU) and HH-1 dev (8 tasks, 64.8 GPU-minutes) | about $3.1 | billed |
| HH-1 main (40 tasks, 244.5 GPU-minutes) | about $10.1 | billed |
| **Running total, third workspace** | **$21.57 of $30** | `modal billing summary` |

## Azure: hosted fine-tuning and frontier-model work (19 October 2026, evening)

The user approved Azure spending without a fixed cap. Training is billed per trained token, inference per token. No resource below charges while idle.

**Resources created** (Subscription 1, group `rg-jayeshupp-2640`):
- `memgate-ft-ncus`, `memgate-ft-ncus2` (North Central US), `memgate-ft-swc`, `memgate-ft-swc2`, `memgate-ft-swc3` (Sweden Central), `memgate-ft-eus2` and `memgate-ft-eus2b` (East US 2): AI Services resources for fine-tuning in parallel. A resource trains at most three jobs at a time.
- `gpt-4.1-base`: a global-standard deployment of `gpt-4.1` (2025-04-14) at capacity 500 on both, for probing the untouched model. The East US 2 resource had no gpt-4.1 quota left.
- The Microsoft.Compute and Microsoft.Network providers were registered on Subscription 1.
- A Linux sandbox VM for running model-written code was not created: the permission classifier stopped it ("Expose Local Services"), and the user has been told.

**Fine-tuned deployments** are developer tier and are deleted after each probe.

| Work | Volume | Note |
| --- | --- | --- |
| FT-1 dev (gpt-4.1-nano, world 0) | 8 jobs, about 0.35–0.52 M trained tokens each | about $1 a job at the global training rate; final figures in FT1-RESULT |
| GPT-4.1 feasibility checks | 2 jobs of 24 rows | a few cents |
| RS-1 census (7 models × 1,341 offices) | 9,387 calls | grok-4.7 spends about 510 reasoning tokens a call, not shown in its completion count |
| Design reviews of FT-2 (2 rounds × 4 frontier models) | 8 calls | |
| FT-2 dev memory arms (5 models × 4 conditions × 297 offices) | about 6,000 calls | running |

