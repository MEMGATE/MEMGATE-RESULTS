# FT-2 and CD-1 main runs: deviations and the rules fixed before any main result

**Written:** 20 October 2026, 12:35 IST. At this time:
- no main world of FT-2 or CD-1 has finished a training block;
- CD-1 world 9300's memory arms are complete;
- no hypothesis has been computed on main data.

## CD-1 world 9304: a training job refused by the service

**What happened.**
- At 11:20 the ENGINE arm's block-0 job (`ftjob-7a37043b…`) failed with "User data has failed data safety check" on its training file.
- The NAIVE arm's block-0 file passed the same check.
- The runner logs nothing when a job fails. Its NAIVE thread would have run all four blocks, about a day, before the run stopped without results.

**What was done.**
- The first attempt was stopped at 12:31. It is kept as `runs/cd1-main-20261020/w9304-safety-fail` (stdout `/tmp/cd1-main-9304-safety-fail.log`).
- The world was rerun once, as FT2-SPEC allows ("a job fails and the world's rerun fails too" = INVALID). The rerun reuses the NAIVE block-0 job (`ftjob-dc8cb14a…`), which had not failed, and uploads the ENGINE block-0 rows again. The rows are byte-identical, because the world is deterministic.

## Rule fixed now for an INVALID world

- **If the rerun's job fails too:**
  - world 9304 is INVALID for infrastructure, for the fine-tuning arms only;
  - CD-1's H1 and H2 are then computed on the four remaining worlds, with the same rules: world-level t interval at 97.5% (3 df, t = 4.177); WIN for H1 needs every world below 0 and the interval wholly below −1 pp; H2 is NON-INFERIOR if the interval's lower bound is above −5 pp.
- **The memory arms (H4, H5)** do not use fine-tuning, so they keep all five worlds.
- **The same rule applies to any FT-2 world** that becomes INVALID for infrastructure.
- **The result reports:**
  - the INVALID world and its cause;
  - the four-world verdicts;
  - descriptively, whatever blocks the INVALID world completed.

## Wording fixed now for outcomes the dev runs make likely

- **"INFERIOR" in the report scripts' output.** `ft1_report.py` and `ft2_report.py` print INFERIOR when non-inferiority is not shown. Results will say "non-inferiority not shown". This is a non-inferiority test: a failure does not show the engine is worse, unless the interval lies wholly below the margin, which will then be said too.
- **FT-2 H5 for grok-4.7.** On the dev world, gated memory was 7.7 pp below raw memory for grok on current holders, because grok sometimes keeps its own answer over the memory. If H5 fails for grok, the result says so in its first lines. The gate's claim for grok is then limited to lies (H4), not current coverage.
- **FT-1 H3** (current holders, ENGINE against NAIVE).
  - In its two finished worlds, ENGINE minus NAIVE was +13.6 pp and −8.9 pp.
  - World 9101's last ENGINE block returned a model that garbled 48.8% of its answers.
  - If H3 fails, the result gives the verdict first, then the garbled-answer counts per arm and block. It does not offer them as an excuse: garbled models are not among the preregistered INVALID conditions.
- **Locality.**
  - Locality through the scope rule is by design. Questions about facts a model was not trained on go to the untouched model.
  - Every result reports unrouted locality next to it, and does not present routed locality as learning without forgetting.

## Update, 20 October 2026, 17:00 IST (still before any main hypothesis is computed)

**CD-1 world 9304, the rerun.** The rerun's ENGINE block-0 job (`ftjob-df289732…`) trained on the byte-identical file that had failed the data safety check (SHA-256 `ca8c9b9a…`, 736,755 bytes in both). This time it passed the check and is training. The service's check is therefore not deterministic.

**FT-2 world 8202, a job refused by the service.**
- At 14:57 its NAIVE block-1 job (`ftjob-42eec520…`) failed with "User data has failed data safety check".
- Its ENGINE arm logged no probe after its block-0 job succeeded. Its thread most likely stopped when the deployment for that probe was refused. Between about 14:45 and 15:15 the subscription refused new deployments with error 715-123420 ("unusual activity"). Deployments have succeeded again since about 16:00 (FT-2 world 8203, CD-1 world 9301, the FT-2 dev run).
- The first attempt is kept as `runs/ft2-main-20261020/w8202-safety-fail` (stdout `/tmp/ft2-main-8202-safety-fail.log`).
- The world was rerun once at 16:55, as FT2-SPEC allows, reusing its two succeeded jobs (NAIVE and ENGINE block 0). If the rerun fails too, world 8202 is INVALID for infrastructure and FT-2 is analysed on four worlds, under the rule above.

## Note, 20 October 2026, 19:20: a stale dev table in CD1-PREREG
CD1-PREREG's dev tables (lines 62–78) were computed with the scorer from before its 20 October fix. Rescored with the frozen scorer:
- Claude's raw rate is 0.0, not 3.2;
- Claude's forged rate is 56.4, not 64.9;
- every "current usages" row differs.

Those tables are dev data and decide nothing. The main results use the frozen scorer only. The preregistration itself is left as frozen.

## 21 October 2026, about 10:45 IST: the runners stopped when the session that started them ended
- **What happened:** every local runner process stopped at once when the Claude Code session that had started them ended. That covered FT-2 main worlds 8200, 8201, 8203 and 8204, CD-1 main worlds 9300, 9302, 9303 and 9304, the FT-2 memory runner, and both dev runs. The fine-tuning jobs on Azure were not affected.
- **What was not affected:** FT-2 world 8202 and CD-1 world 9301 had already finished, with results.json written.
- **The restart:**
  - each unfinished main world was moved aside to `w<seed>-interrupted-20261021`;
  - it was restarted once with its original arguments and `--reuse` listing every job its log had started;
  - jobs that already trained the same rows from the same model are reattached, not retrained, and the probes are asked again;
  - the runners now start detached from the session (`scripts/launch_detached.py`), so a session ending no longer stops them.
- **Dev runs:** the FT-2 and CD-1 dev runs were not restarted. Their remaining jobs finish on Azure, and the dev tables already recorded stand.
- **Analysis:** each world is analysed from its final, complete attempt, as before. The code hash is unchanged (FT-2 `5d241114…`).

## 21 October 2026, about 11:00 IST: world 8203 stops at Azure's data safety check
- **What happened:** world 8203's NAIVE block 1 (job `ftjob-c7303464…`, submitted 20 October at 15:59) had been rejected by Azure's data safety check ("User data has failed data safety check"). Its ENGINE arm finished all four blocks. The restart at 10:50 would have resubmitted the rejected block, so it was stopped at once, before submitting anything. Its empty folder is kept as `w8203-restart-stopped-20261021`, and the original run as `w8203-interrupted-20261021`.
- **Decision:** the file is not resubmitted. A provider's safety check is respected, not retried past.
- **Analysis:** world 8203 is analysed only as far as it got. FT-2's preregistered comparisons use the worlds that finish, under the rule for analysing on fewer worlds already recorded in this note.

## 21 October 2026, about 12:05 IST: worlds 8201 and 9304 stopped on a deployment refusal
- **What happened:** after the 10:49 restart, CD-1 world 9304 (at 11:04) and FT-2 world 8201 (at 11:09) stopped when Azure refused a new deployment with error 715-123420 ("unusual activity"). Every runner had restarted at once and redeployed its models to ask the probes again. No training job was affected.
- **The block lifted:** worlds 9300 and 9303 created deployments again at 11:39 and 11:42, and their probes after session 3 completed.
- **The restart:**
  - each world is restarted once, one at a time and an hour apart, so as not to trigger the block again;
  - the stopped attempt is moved aside to `w<seed>-refused715-20261021`;
  - the original arguments are kept, and `--reuse` lists every job id from both earlier attempts. The ids come from the stopped attempt's `--reuse` list and its log;
  - matching jobs are reattached, not retrained, and nothing rejected by Azure's data safety check is resubmitted.
- **Analysis:** unchanged. Each world is analysed from its final, complete attempt. The code hash is unchanged.

### Addendum, 21 October 2026, about 12:20 IST: 9304's restart refused again
- **What happened:** world 9304 was restarted at 11:59. It reattached its eight jobs, but Azure again refused its first new deployment (`ft2-9304-naive-0`) with 715-123420, on memgate-ft-eus2b (East US 2).
- **What it shows:** the refusal is tied to resources, not to the account. Deployments on memgate-ft-ncus and memgate-ft-ncus2 succeeded at 11:39 and 11:42. World 8201's resource, memgate-ft-swc3 (Sweden Central), has not deployed since its refusal at 11:09.
- **Decision:** no further restart of 9304 or 8201 for now: refusals are not retried in a loop, and no test deployment is made. Both wait until Azure support lifts the block, or until a single deliberate retry after a long pause. Either way, it is recorded here before any result.
- **Rule if they cannot finish:**
  - CD-1 is analysed on the worlds that finish, as recorded above for 9304;
  - FT-2 is analysed on the worlds that finish (8200, 8202, 8204, and 8201 if it completes) under the same rule.
  - The result docs state which worlds were lost and why.

### Addendum, 21 October 2026, 15:56 IST: the single deliberate retry of 9304
- **What was done:** world 9304 is retried once, almost four hours after its last refusal. This is the single deliberate retry after a long pause allowed above.
  - The attempt refused at 12:05 is moved aside to `w9304-refused715b-20261021`.
  - The restart reuses every job id from the earlier attempts, and its log is `/tmp/cd1-main-9304.log`.
  - If Azure refuses its deployment again, 9304 is not retried. It stays held until Azure lifts the block.
- **Outcome, 21 October 2026, about 16:00 IST:** the retry reattached the world's eight jobs, then Azure refused its first new deployment (`ft2-9304-naive-0`) on memgate-ft-eus2b with 715-123420 again. The runner stopped.
  - **No further retry.** World 9304 stays held until Azure lifts the block on that resource.
  - **Analysis:** CD-1 is analysed on the worlds that finish, under the rule above.
  - **Records:** the stopped attempt is `runs/cd1-main-20261020/w9304`, and its log is `/tmp/cd1-main-9304.log`.
  - **Runner stopped by hand at 15:59.** After the refusal, the runner's ENGINE thread was still alive and would have asked for its own deployment. It was stopped so that no further deployment request goes to the blocked resource.

### Addendum, 21 October 2026, 16:53 IST: the single deliberate retry of 8201
- **What was done:** world 8201 is retried once, almost six hours after its refusal at 11:09, on its own resource memgate-ft-swc3 (Sweden Central). 9304's retry was refused at about 16:00, but on another resource (memgate-ft-eus2b).
  - The attempt refused at 11:09 is moved aside to `w8201-refused715-20261021`.
  - The restart reuses every earlier job id, and its log is `/tmp/ft2-main-8201.log`.
  - If Azure refuses again, 8201 is not retried and its runner is stopped, as 9304's was.
- **Outcome, 21 October 2026, 17:22 IST:** it resumed.
  - Its block-0 deployments on memgate-ft-swc3 were created, and both arms' probes after session 3 completed (17:18 and 17:20).
  - Its block-1 jobs were reattached. The ENGINE arm caught Z1 and Z2 and rolled back to block 1, as in the other worlds.
  - Swc3's block had lifted. The founder had paid an outstanding Azure bill earlier in the afternoon, which may be related; that is not confirmed.
  - **9304 (memgate-ft-eus2b) stays held:** its single retry was refused at about 16:00, and no further retry is made under the rule above.

### Addendum, 21 October 2026, about 20:55 IST: the block on memgate-ft-eus2b has lifted; world 9304 is restarted once
- **What was seen:** at about 20:52 a deployment on memgate-ft-eus2b succeeded. It was for RP-3's Qwen3-32B replicate (`runs/rp3-open-qwen32b-20261021/log.jsonl`), the first deployment on that resource since the 715-123420 refusals.
- **The rule above:** world 9304 "stays held until Azure lifts the block on that resource". The block has lifted, so it is restarted once:
  - the attempt stopped at 16:00 is moved aside to `w9304-refused715c-20261021`;
  - the restart keeps the original arguments and reuses all eight of the world's trained jobs (blocks 0–3 of both arms);
  - only its deployments and probes remain;
  - its log is `/tmp/cd1-main-9304-r3.log`.
- **If a deployment is refused again,** the runner is stopped and 9304 stays held. There is no further retry.
- **Analysis:** unchanged. Each world is analysed from its final, complete attempt, and the code hash is unchanged.
- **Outcome, 21 October 2026, about 21:15 IST:** world 9304 completed. Every deployment on memgate-ft-eus2b succeeded, all its probes were asked, and `results.json` is written. Its folder is `runs/cd1-main-20261020/w9304`. CD-1 now has two of its five worlds complete (9301, 9304); 9300, 9302 and 9303 are training.

## 22 October 2026, 08:52 IST: a faster training tier is not available to the running chains (no change made)
- **Why it was tried.** The worlds' current block jobs have read "running" for 13–25 hours. Some have not started training: their batch size is still unset. Azure estimates they will finish between 25 October and 4 November. The developer tier finished RP-3's GPT-4.1 jobs in about six hours on 22 October.
- **The pilot.** A developer-tier copy of world 9303's ENGINE block 1 job was submitted on memgate-ft-ncus2, with the same model, training file and settings.
- **What came back:** HTTP 400, "Continuous finetuning is only supported for same TrainingType as base model. For example, models finetuned with GlobalStandard are only compatible with GlobalStandard continuous finetuning."
- **Decision.** No job was created and no runner was changed. The worlds continue on the global tier.

## 22 October 2026, 10:17 IST: each running world is also run again from block 0 on the developer tier, and whichever finishes first is used
- **Why.** The global tier's queue holds the running worlds' block jobs. Azure estimates they will finish between 25 October and 4 November, for one block each, with up to two blocks to follow. A chain cannot change tier midway (previous section).
- **What is done.** Each running world is started again from block 0, with the same arguments, on a new resource of its own, with every training job on the developer tier:

  | World | New resource | Base account |
  | --- | --- | --- |
  | FT-2 8200 | memgate-ft-dev3 | memgate-ft-ncus |
  | CD-1 9300 | memgate-ft-dev4 | memgate-ft-ncus |
  | CD-1 9303 | memgate-ft-dev5 | memgate-ft-ncus |
  | FT-2 8201 | memgate-ft-dev6 | memgate-ft-swc |
  | FT-2 8204 | memgate-ft-dev7 | memgate-ft-swc |
  | CD-1 9302 | memgate-ft-dev8 | memgate-ft-swc |

  - The new chains write to `runs/ft2-main-20261020/w<seed>-devtier` and `runs/cd1-main-20261020/w<seed>-devtier`.
  - They run through `cl/devtier_world_run.py` (SHA-256 `5b37933b04494c82a9b50a3d643058154c12eeabde3c6d7f314125c5da46c5b6`). It submits developer-tier jobs and spaces deployment requests five minutes apart (`cl/deploy_spacing.py`, SHA-256 `c66c6c21ce76e57289b1eeb90a78025dd932695fceacc52dcc2acc65def8c21c`).
  - ft2.py, its rows, settings, questions and scoring, and its hash `5d241114…` are unchanged.
- **Rule, fixed now, before any FT-2 or CD-1 hypothesis is computed:**
  - For each world, the chain whose session-12 results are complete first is the one analysed: the global chain already running, or its developer-tier rerun.
  - The other chain is then stopped, its unfinished jobs are cancelled, and its records are kept.
  - The choice depends only on finishing time.
- **What has been seen.** The global chains' per-block probes are in their logs, and some were read while monitoring. No hypothesis was computed, and the rule does not depend on any outcome.
- **Not affected:** worlds 8202, 9301 and 9304 are complete, and world 8203 stays stopped (Azure's data safety check).
- **Applying the rule (10:44):** `cl/first_finished.py` (SHA-256 `e8983e00d1aca5beb614d88c08c0e7dd0d67cba935770e4bdc0f7c02e87e62c7`) checks every ten minutes, for FT-2, CD-1 and FT-1 world 9102.
  - When a chain's results.json is written, it records the decision in `runs/first-finished-20261022.json`.
  - It then stops the other chain's runner, cancels its unfinished jobs and deletes its leftover deployments.

## 22 October 2026, 11:53 IST: a size replicate on gpt-4.1-mini (descriptive, reported apart)
- **Why.** The founder asked for the fastest way to get the weights-route results. gpt-4.1-mini trains faster than GPT-4.1, so its chains finish sooner. RP-3 reported its mini replicate the same way.
- **What.** FT-2 world 8200 on memgate-ft-dev1 and CD-1 world 9300 on memgate-ft-dev2, from block 0, on the developer tier.
  - They run through `cl/ft2_mini_run.py` (SHA-256 `72a4186ee565981a9a28419e192cd0ffd837aafa69535ed0c8e887b5f396b19b`), which sets the base model to gpt-4.1-mini and its untouched deployment. Everything else is ft2.py's, with its hash unchanged.
  - Outputs: `runs/ft2-mini-20261022/w8200` and `runs/cd1-mini-20261022/w9300`.
- **Status.** A replicate on another model size. It does not enter FT-2's or CD-1's preregistered verdicts, which are GPT-4.1's.

## 22 October 2026, about 13:58 IST: a third copy of each running world on Azure's Standard tier; the first of three to finish is used
- **Why.** The developer tier is no faster now. Its block 0 jobs, submitted at about 10:20–10:53, were estimated at 13:25 to finish between 23 and 27 October. The global chains' current blocks were estimated between 22 October and 5 November.
  - A Standard-tier pilot was submitted at 13:35 on memgate-ft-ncus3: a 12-row job of gpt-4.1, `ftjob-13925e4b…`.
  - Azure accepted it, with training type "standard", and it was running by 13:49.
- **What is done.** Each running world is started again from block 0, with the same arguments, on a new resource of its own, all in North Central US, with every training job on the Standard tier:

  | World | New resource | Base account |
  | --- | --- | --- |
  | FT-2 8200 | memgate-ft-std1 | memgate-ft-ncus |
  | CD-1 9300 | memgate-ft-std2 | memgate-ft-ncus |
  | CD-1 9303 | memgate-ft-std3 | memgate-ft-ncus |
  | FT-1 9102 | memgate-ft-std4 | (FT-1's own) |
  | FT-2 8201 | memgate-ft-std5 | memgate-ft-swc |
  | FT-2 8204 | memgate-ft-std6 | memgate-ft-swc |
  | CD-1 9302 | memgate-ft-std7 | memgate-ft-swc |

  - The new chains write to `runs/.../w<seed>-standard`.
  - They run through `cl/standard_world_run.py`, SHA-256 `37cae4d57d5ad5ffe2b53b01f50846d9062990757aa743a5fc5597727a9ab10f` (LF line endings). It is `devtier_world_run.py` with the tier set to Standard and the new resources registered. Deployment requests are spaced as before (`cl/deploy_spacing.py`, `c66c6c21…`).
  - ft2.py and ft1.py, their rows, settings, questions and scoring, and their hashes are unchanged.
- **Rule, extended now, before any FT-2, CD-1 or FT-1 hypothesis is computed:**
  - For each world, of its three chains (global, developer tier, Standard tier), the one whose session-12 results are complete first is analysed.
  - The other two are then stopped, their unfinished jobs cancelled and their records kept.
  - The choice depends only on finishing time.
- **The monitor:** `cl/first_finished3.py` (SHA-256 `f78351c713cefcd5119e1f7087e3232e0ead9ecd298718cabcff1c320afd7b1e`) applies the rule every ten minutes and records each decision in `runs/first-finished-20261022.json` before stopping anything. It replaces `first_finished.py`'s loop, which made no decision: no chain had finished.
- **What has been seen:** as before. No hypothesis was computed, and the rule does not depend on any outcome.

## 22 October 2026, about 15:50 IST: the gpt-4.1-mini replicate also on the Standard tier (descriptive, reported apart)
- **Why.** The replicate's developer-tier copies (worlds 8200 and 9300, submitted at 11:53) were still on their first blocks at 15:45. The founder's instruction: use the Azure fine-tuning capacity that is working ("usse chodna mat"), and finish all the work on it.
- **What.** The same two worlds, again from block 0, on Azure's Standard tier, through `cl/ft2_mini_standard_run.py` (SHA-256 `f8ab29e81b0380d31a7cc3f60b7444050dbdf9c4d6d0c1b91df1c0cda26fc44a`, LF line endings). It is `ft2_mini_run.py` with `standard_world_run` in place of `devtier_world_run`.
  - Each copy runs on a new resource of its own, which also holds its untouched gpt-4.1-mini: memgate-ft-std8 (FT-2 8200) and memgate-ft-std9 (CD-1 9300).
  - Outputs: `runs/ft2-mini-20261022/w8200-standard` and `runs/cd1-mini-20261022/w9300-standard`.
- **Rule, fixed now, before any of the replicate's results:** for each world, whichever copy's session-12 results are complete first is reported. The other copy is then stopped, its unfinished jobs are cancelled, and its records are kept. The replicate stays descriptive and outside FT-2's and CD-1's verdicts.

## 22 October 2026, 16:57 IST: world 8201's Standard copy restarted once (its ENGINE upload failed)
- **What happened:** on memgate-ft-std5, the ENGINE arm's block 0 training file (`ft2-8201-ENGINE-0.jsonl`, uploaded at 14:23) ended in status "error", with no details from Azure, and no job was created.
  - The runner trains its two arms in two threads, so the ENGINE thread had stopped while the NAIVE thread went on. Its block 0 job (`ftjob-787e13fb…ed743e`) was running.
  - The developer-tier copy uploaded the same rows without error, so this looks like a passing file-processing failure.
- **What was done (once, as the rules allow for a runner that died for another reason):**
  - The runner was stopped, and its folder was moved aside as `runs/ft2-main-20261020/w8201-standard-engine-file-error-20261022` (only the untouched model's answers).
  - The world was restarted with the same arguments and `--reuse ftjob-787e13fbfb7f4c3eb78f77e954ed743e`, so the NAIVE arm waits for its running job and the ENGINE arm uploads again.
  - ft2.py and its hash are unchanged. No result has been read.
- **Also seen:** on memgate-ft-std9, the mini replicate's NAIVE block 0 file has read "running" (processing) since upload. That runner waits on it and has not stopped. It will be restarted the same way only if the file fails.
- **17:04 IST, the mini replicate's CD-1 9300 Standard copy restarted once for the same reason.**
  - Its NAIVE block 0 file stayed "processing" for over an hour, so the runner's upload gave up after 15 minutes and that arm's thread stopped. Its ENGINE job (`ftjob-8875e96d…25ddc0`) was running.
  - The folder was moved aside as `runs/cd1-mini-20261022/w9300-standard-naive-file-timeout-20261022`, and the copy was restarted with `--reuse ftjob-8875e96daa5c4ce293bfc2127f25ddc0`.
- **The other Standard copies** each have both arms' block 0 jobs running.

## 22 October 2026, about 19:55 IST: a fourth copy of each running world, on the Standard tier in Sweden Central; the first of four to finish is used
- **Why.** At 19:30, 14 of the lab's 16 Standard-tier jobs in North Central US read "queued, waiting for GPUs". A Standard-tier pilot (`ftjob-00533841…`, 12 rows) was submitted at 19:33 on a new Sweden Central resource and was training ("Finetuning started") by 19:42. The founder's instruction: use any fine-tuning capacity that is available, and do not let it go.
- **What is done.** Each running world is started again from block 0, with the same arguments, on a new Sweden Central resource of its own, with every training job on the Standard tier:

  | World | New resource | Base account |
  | --- | --- | --- |
  | FT-2 8200 | memgate-ft-stdswc1 | memgate-ft-swc |
  | CD-1 9300 | memgate-ft-stdswc2 | memgate-ft-swc |
  | CD-1 9303 | memgate-ft-stdswc3 | memgate-ft-swc |
  | FT-1 9102 | memgate-ft-stdswc4 | (FT-1's own) |
  | FT-2 8201 | memgate-ft-stdswc5 | memgate-ft-swc |
  | FT-2 8204 | memgate-ft-stdswc6 | memgate-ft-swc |
  | CD-1 9302 | memgate-ft-stdswc7 | memgate-ft-swc |

  - The new chains write to `runs/.../w<seed>-swcstd`.
  - They run through `cl/standard_swc_world_run.py`, SHA-256 `21fe07617b0476ee3a7a46e83a53405b1008199296eff259df66d2fbadc5149a` (LF line endings): `standard_world_run.py` with the Sweden Central resources registered.
  - ft2.py and ft1.py and their hashes are unchanged. The untouched GPT-4.1 is asked from memgate-ft-swc's deployment, as for worlds 8201, 8204 and 9302.
- **Rule, extended now, before any FT-2, CD-1 or FT-1 hypothesis is computed:**
  - For each world, of its four chains (global, developer tier, Standard tier in North Central US, Standard tier in Sweden Central), the one whose session-12 results are complete first is analysed.
  - The others are then stopped, their unfinished jobs cancelled and their records kept.
  - The choice depends only on finishing time.
- **The monitor:** `cl/first_finished4.py` (SHA-256 `e15ff1bb8e17e5da383cc10551e6ebe2b38c1de52ee96e718d929b0397805ff0`) replaces `first_finished3.py`'s loop, which made no decision. It records each decision in `runs/first-finished-20261022.json` before stopping anything.
- **What has been seen:** as before. No hypothesis was computed, and the rule does not depend on any outcome.
- **20:33 IST: CD-1 9302's Sweden Central copy restarted once.** Its NAIVE block 0 file stayed in Azure's file processing for over 15 minutes after a simultaneous upload, so that arm's thread stopped. The folder was moved aside (`w9302-swcstd-naive-file-timeout-20261022`), and the copy was restarted with `--reuse ftjob-d45267cab070444e834abc63dec55928` (its ENGINE job).
- **A pattern:** on new resources, two files uploaded at the same moment sometimes leave one stuck in processing. This has happened four times, each followed by one restart.

## 23 October 2026, about 12:35 IST: every runner stopped again when the session ended; the chains are restarted with `--reuse`
- **What happened:** at about 11:07 the Claude Code session that had started the runners ended, and every local runner stopped. That covered every open chain of FT-2 (8200, 8201, 8204), CD-1 (9300, 9302, 9303) and FT-1 9102, the gpt-4.1-mini replicate, and the first-finished monitor.
  - Starting them detached (`scripts/launch_detached.py`, 21 October) did not keep them alive. The 21 October line "a session ending no longer stops them" was wrong.
  - The fine-tuning jobs on Azure were not affected. No open chain had written results.json, and the monitor had made no decision.
- **The restart, as on 21 October:**
  - each unfinished chain's folder is moved aside to `<folder>-interrupted-20261023`;
  - it is restarted with its original arguments and `--reuse` listing every job id that its log and its earlier `--reuse` list name (`scripts/restart_worlds.py`; the plan, with process ids, is written to `runs/restart-1023.json`);
  - the global chains run through `cl/spaced_world_run.py`, SHA-256 `daf986a9e4078fc79197bf44fec7083dfba9dbca7598a6edf1f7577196c91781` (LF line endings). It only adds the five-minute spacing of deployment requests that every other chain already has. The tier, the runner and its hash are unchanged;
  - the runners started 20 seconds apart, from 12:38 to 12:48. Their deployment requests are at least five minutes apart across all of them, since a burst of redeployments after the 21 October restart was refused with 715-123420.
- **Not restarted:** FT-1 9102's global chain, held since its 715-123420 refusal at 06:29, and its Standard copy, which stopped at 10:45 on another 715-123420 refusal, on memgate-ft-std4 (`docs/FT1-DEVIATIONS-2026-10-20.md`).
- **How long they live:** the runners now run under the current session. If it ends, they stop, and they are restarted the same way in the next session. The jobs on Azure go on meanwhile.
- **What has been seen:** the runners' log tails were read to find where each chain stopped. No hypothesis was computed.
- **Analysis:** unchanged. Each world is analysed from the first chain whose session-12 results are complete. The code hashes are unchanged.

## 23 October 2026, 17:48 IST: five restarted chains stopped on deployment refusals in North Central US; held
- **What happened:** five of the chains restarted at 12:38–12:48 stopped when Azure refused a new deployment with 715-123420 ("unusual activity"), each while redeploying an already trained block to ask its probes again:
  - CD-1 9303, global, on memgate-ft-ncus2, at 16:57 (`ft2-9303-naive-1`);
  - CD-1 9303, Standard, on memgate-ft-std3, at 17:12 (`ft2-9303-naive-1`);
  - FT-2 8200, Standard, on memgate-ft-std1, at 17:37 (`ft2-8200-naive-1`);
  - CD-1 9300, global, on memgate-ft-ncus, at 17:42 (`ft2-9300-naive-0`);
  - FT-2 8200, global, on memgate-ft-ncus2, at 17:47 (`ft2-8200-naive-1`).
  - All five resources are in North Central US. Deployment requests were five minutes apart across all processes.
  - No training job was affected; the jobs go on in Azure.
- **Decision:**
  - The five chains are held: refusals are not retried in a loop.
  - Each of these worlds still has other live chains (developer tier, and Standard in Sweden Central), so each world is decided by them under the first-finished rule.
  - A held chain is restarted once, with `--reuse`, only if every other chain of its world also stops. Any such restart is recorded here first.
- **Analysis:** unchanged.

## 23 October 2026, 18:16 IST: a sixth refusal, in Sweden Central; every chain runner stopped until deployments succeed again
- **What happened:** at 18:02 FT-2 8204's global chain, on memgate-ft-swc in Sweden Central, was refused the same way (`ft2-8204-naive-1`). The refusals are not tied to one region.
- **Why they came:** each restarted chain redeploys every block it had already trained, to ask its probes again. Thirty chains did that from 12:38, one deployment every five minutes, and Azure answered with 715-123420.
- **What was done at about 18:12:** every chain runner was stopped, so that no further deployment request goes out while the block holds. The fine-tuning jobs go on in Azure. The first-finished monitor and the other runners (TW-1 on GPT-4.1, PR-2, CN-2 on GPT-4.1), which deploy only when a job of theirs finishes, keep running.
- **Next, recorded before it is done:**
  - The chains are restarted once a deployment on the lab's resources succeeds again.
  - The restart reuses each already trained block's probe answers from the stopped attempt instead of redeploying it, so that only new blocks are deployed. The probes are deterministic (temperature 0, the same fine-tuned model), so the answers are the same.
  - The wrapper that does this is recorded here, with its hash, before it runs.
- **Analysis:** unchanged.

### Addendum, 23 October 2026, 18:20 IST: the restart wrapper that reuses earlier answers
- **Wrapper:** `cl/reuse_world_run.py`, SHA-256 `dec1f167957d913e40338b293ad41027fad8635c0c70687ed2be9e2ced610bb2` (LF line endings). It imports the chain's own wrapper (tier, resources, deployment spacing) and runs ft2.py or ft1.py unchanged.
- **What it does:** when a block's fine-tuned model is the one an earlier attempt of the same chain deployed and asked, with its answers saved (`answers-ARM-SESSION.json` carrying that model id), the block is not deployed: the runner receives those saved answers for its probes, held-out phrasing and unrouted diagnostic, and saves them again. A block with a new model, or with saved answers that do not cover every office asked, is deployed and asked as frozen.
- **Why the answers are the same:** the same fine-tuned model, the same questions, temperature 0.
- **Launch:** `scripts/restart_worlds.py TAG --reuse-answers`, which passes each chain its earlier attempts, most recent first.
- **When:** once, after a long pause: on 24 October from about 06:15 IST, about twelve hours after the last refusal. The six refused chains stay held under the 17:48 rule; FT-1 9102's global and Standard chains stay held.
- **If Azure refuses a deployment again,** that chain stops and is held, and no other chain is restarted until a deployment succeeds.

## 24 October 2026, 10:06 IST: the 06:13 restart drew one refusal; all its runners stopped
- **What happened:** the restart of 24 chains (06:13 to 06:36, through `cl/reuse_world_run.py`) answered 36 already trained blocks from saved answers, with no deployment. New blocks were deployed as their jobs finished; at least one such deployment succeeded (FT-2 8201's global chain deployed `ft2-8201-engine-3` and finished its ENGINE arm, session 12, at 09:01). At 09:53 the same chain's next deployment, `ft2-8201-naive-2` on memgate-ft-swc3, was refused with 715-123420 ("unusual activity"), and that runner exited.
- **What was done at 10:06:** the whole restart was stopped, as planned for the first refusal; none of the 24 runner processes is alive. No other refusal was logged. The training jobs go on in Azure.
- **Next, recorded before it is done:**
  - One more restart, once, after a pause of about twelve hours: on 24 October from about 22:15 IST, with `scripts/restart_worlds.py 1025 --reuse-answers`, so that every block answered so far is again answered from saved answers.
  - Held: FT-2 8201's global chain (refused today), and the eight chains held before (FT-1 9102 global and Standard; CD-1 9303 global and Standard; FT-2 8200 Standard; CD-1 9300 global; FT-2 8200 and 8204 global). Each of these worlds is decided by its other copies under the first-finished rule.
  - If Azure refuses again, the whole restart stops at once and nothing is restarted before a change to the spacing of deployment requests is recorded here first.
- **Analysis:** unchanged.
