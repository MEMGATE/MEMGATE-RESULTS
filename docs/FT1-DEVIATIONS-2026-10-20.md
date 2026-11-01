# FT-1 main run: world 9102's infrastructure deviations, recorded before its result

**Written:** 20 October 2026, 13:45 IST, while world 9102's ENGINE arm is still training. Worlds 9100 and 9101 are complete. No FT-1 hypothesis has been computed.

## 1. Moved off its preregistered resource
- **What happened:** world 9102's jobs on `memgate-ft-eus2` sat for 5 hours without starting.
- **What was done:** they were cancelled and the world rerun on `jayeshupp-8050-resource`. The first attempt is kept as `runs/ft1-main-20261020/w9102-stuck-eus2`.

## 2. ENGINE block 2: a job that never started, twice
- **First attempt:**
  - The ENGINE block-2 job (`ftjob-e4c18f31…`) was enqueued at 08:22, "waiting for jobs ahead", and stayed there until 11:15.
  - In that time, jobs created after it on the same resource started and finished: world 9100's ENGINE block 3, created at 08:23, and world 9102's NAIVE blocks 2 and 3.
- **Second attempt:**
  - The job was cancelled and resubmitted identically: the same training file, base model, epochs and learning rate (`ftjob-ad665143…`).
  - The world was restarted at 11:20, reusing its finished jobs. Its reused blocks were re-probed at temperature 0. That attempt is kept as `w9102-stuck-engine2`.
  - The resubmitted job also never started, from 11:17 to 13:25, although the resource had a free slot and world 9301's block-1 jobs, created about 12:55, started at once.
- **Third resubmission:** a third identical submission (`ftjob-4498e7c1…`) went straight to "enqueued" with a free slot available.
- **Conclusion:** every job whose base model is ENGINE block 1's fine-tuned model (`…ft-6ce779b9…`) has waited indefinitely, while jobs from other models started. The cause is inside the service and not visible to us.

## 3. What was done at 13:45
- **The queued job:** it was cancelled.
- **The restart:**
  - The partial run is kept as `w9102-stuck-engine2b` (stdout `/tmp/ft1-main-9102-stuck-engine2b.log`).
  - World 9102 was restarted reusing NAIVE blocks 0–3 and ENGINE block 0.
  - It does not reuse ENGINE block 1: the runner trains it again from ENGINE block 0's model, on the same rows with the same settings, and then trains blocks 2 and 3 from the new model.
- **This is an operational rerun.** The protocol's rerun reuses only jobs that succeeded. Not reusing one only means training it again.
- **One consequence:** ENGINE's block-1 model differs from the one probed in the earlier attempts. Fine-tuning is not deterministic. The earlier attempts' answers are kept and are not used.
- **Re-probing:** reused blocks are re-probed at temperature 0. In the second attempt, FROZEN locality came out 88.3% against 90.0% in the first, a one-question difference out of 60.

## How the result will treat this
- World 9102 is analysed from its final attempt, like the other two worlds.
- Each deviation above is listed in FT1-RESULT.
- If the ENGINE arm cannot finish because its jobs will not start again, world 9102's ENGINE arm is reported as INVALID for infrastructure. In that case, FT-1's hypotheses are computed on worlds 9100 and 9101 only, and the result says so.

## 21 October 2026, about 10:45 IST
- **What happened:** world 9102's runner stopped when the session that started it ended. Its ENGINE block 1 job on Azure (`ftjob-60519320…`) was still waiting for GPUs.
- **The restart:**
  - the folder was moved aside to `w9102-interrupted-20261021`;
  - the world was restarted with its original arguments and `--reuse` listing every job its log had started, so the waiting job is reattached;
  - it runs detached from the session.

## 21 October 2026, about 20:40 IST: a deadline for world 9102's ENGINE arm, recorded before any FT-1 hypothesis is computed
- **What happened:** ENGINE block 1's job (`ftjob-60519320…`, on jayeshupp-8050-resource) failed on its first attempt at 10:01. The service retried it, and logged "Training started (retry 1)" at 10:15. It has logged nothing since, and it still reads "running" more than ten hours later. FT-1's other blocks trained in 1–3.5 hours.
- **Rule, fixed now:**
  - If this job has not succeeded by **22 October 2026, 10:15 IST** (24 hours after its retry started), world 9102's ENGINE arm is INVALID for infrastructure, under the rule above. FT-1's hypotheses are then computed on worlds 9100 and 9101 only, and the result says so.
  - If the job succeeds before then, the runner continues as it is, and the world is analysed from its final attempt.
- **No resubmission is made meanwhile.** Earlier resubmissions of jobs from this model's chain waited indefinitely (section 2).

## 22 October 2026, 08:51 IST: the deadline was met
- **What happened:** world 9102's ENGINE block 1 job (`ftjob-60519320…`) succeeded at 07:54 on 22 October, before the 10:15 deadline.
  - The runner probed it (ENGINE after session 6).
  - At 07:59 it submitted ENGINE block 2 (`ftjob-8396d1d9…`), which is running.
- **Decision:** under the rule above, the runner continues as it is, and the world is analysed from its final attempt, with worlds 9100 and 9101. FT-1's hypotheses wait for world 9102's ENGINE blocks 2 and 3.

## 22 October 2026, 10:17 IST: world 9102 is also run again from block 0 on the developer tier, and whichever finishes first is used
- **Why.** The global tier's queue is slow, and world 9102's ENGINE arm still needs blocks 2 and 3.
- **What is done.** The world is started again from block 0 with the same arguments on a new resource, memgate-ft-dev9, with every training job on the developer tier.
  - It runs through `cl/devtier_world_run.py` (SHA-256 `5b37933b04494c82a9b50a3d643058154c12eeabde3c6d7f314125c5da46c5b6`).
  - Its output is `runs/ft1-main-20261020/w9102-devtier`.
  - ft1.py and its hash `1ab1eecf…` are unchanged.
- **Rule, fixed now, before any FT-1 hypothesis is computed:**
  - The chain whose final results are complete first is the one analysed: the global chain already running, or the rerun. That world joins 9100 and 9101.
  - The other chain is then stopped and kept.
  - The choice depends only on finishing time.

## 22 October 2026, about 13:58 IST: a third copy of world 9102 on Azure's Standard tier
World 9102 is also run again from block 0 on Azure's Standard tier, on memgate-ft-std4 (`runs/ft1-main-20261020/w9102-standard`). The first of its three chains to finish is used (global, developer tier, Standard tier). The rule, the runner and the monitor are recorded in [FT2-CD1-DEVIATIONS-2026-10-20.md](FT2-CD1-DEVIATIONS-2026-10-20.md), 22 October, Standard tier. ft1.py and its hash are unchanged.

## 22 October 2026, about 19:55 IST: a fourth copy of world 9102 on the Standard tier in Sweden Central
World 9102 is also run from block 0 on memgate-ft-stdswc4 (`runs/ft1-main-20261020/w9102-swcstd`). The first of its four chains to finish is used. See [FT2-CD1-DEVIATIONS-2026-10-20.md](FT2-CD1-DEVIATIONS-2026-10-20.md), 22 October, Sweden Central. ft1.py and its hash are unchanged.

## 23 October 2026, about 06:10 IST: the global chain of world 9102 stopped on a deployment refusal; one deliberate retry
- **What happened:** at about 00:52 the global chain's runner stopped. Azure refused the deployment `ft1-9102-naive-2` on jayeshupp-8050-resource with 715-123420 ("unusual activity").
  - The runner was deploying NAIVE's block-2 model for its probe after session 9.
  - No training job was affected. ENGINE had finished all four blocks and its probe after session 12. NAIVE had trained blocks 0–2.
- **The retry, under the rule used for FT-2 and CD-1 on 21 October** (refusals are not retried in a loop; one deliberate retry after a long pause):
  - the stopped attempt is moved aside to `w9102-refused715-20261023`;
  - the world is restarted once, at about 06:09, more than five hours after the refusal, with its original arguments;
  - `--reuse` lists every job id from the earlier attempts: the previous `--reuse` list and ENGINE blocks 2 and 3 (`ftjob-8396d1d9…`, `ftjob-110df5f1…`);
  - its log is `/tmp/ft1-main-9102-r2.log`.
- **If Azure refuses a deployment again,** the runner is stopped and this chain stays held. World 9102 is then decided by its other three chains under the first-finished rule (developer tier, Standard North Central US, Standard Sweden Central).
- **Analysis:** unchanged. The code hash is unchanged.
- **Outcome, about 06:15:** the retry reattached the jobs, and its first new deployments on jayeshupp-8050-resource were created. The re-probes after session 3 completed, and ENGINE rolled back to block 1 as before. The chain continues.
- **Outcome, 06:29: refused again, the chain is held.**
  - **What the retry did first:** it reattached every job. NAIVE block 3 had already been trained by an earlier attempt (`ftjob-b6e37ec7…`), so all four blocks of both arms are trained. It then re-probed both arms through session 9.
  - **The refusal:** the deployment for the last probes (`ft1-9102-naive-3`, after session 12) was refused with 715-123420 at about 06:29, and the runner stopped.
  - **No further retry.** Under the rule above, this chain stays held until Azure lifts the block on jayeshupp-8050-resource. If a later deployment on that resource succeeds, the chain is restarted once more and recorded here; only its two final probes remain.
  - **Meanwhile,** world 9102 can still finish through its other three chains under the first-finished rule.
  - **Records:** the attempt is `runs/ft1-main-20261020/w9102`, and its log is `/tmp/ft1-main-9102-r2.log`.

## 23 October 2026, 10:45 IST: the Standard copy of world 9102 stopped on a deployment refusal; held
- **What happened:** at 10:45 Azure refused the deployment `ft1-9102-naive-2` on memgate-ft-std4 with 715-123420 ("unusual activity"). The runner stopped.
  - ENGINE had finished all four blocks and its probe after session 12.
  - NAIVE had trained blocks 0–2 and was deploying block 2 for its probe after session 9. Its block 3 is not trained.
- **Decision:** no retry in a loop. The chain is held, as the global chain is. The 21 October rule allows one deliberate retry after a long pause; if one is made, it is recorded here first.
- **Then, at about 11:07,** every runner stopped when the session ended. World 9102's developer-tier and Sweden Central copies are restarted with `--reuse` ([FT2-CD1-DEVIATIONS-2026-10-20.md](FT2-CD1-DEVIATIONS-2026-10-20.md), 23 October). Its global and Standard chains stay held.
- **Analysis:** unchanged. World 9102 is decided by whichever chain's session-12 results are complete first.
