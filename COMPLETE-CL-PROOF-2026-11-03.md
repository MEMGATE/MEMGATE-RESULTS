# Continual-Learning Results: Preregistered Routed-System Tests, Plus Dev-Stage Weights-Alone Trials

This repository contains the experimental records, raw JSON evaluation reports (`runs/`), and specifications/preregistrations (`docs/`) for our continual-learning experiments conducted between **19 October and 3 November 2026** across dense (`Qwen2.5-1.5B`, `Qwen2.5-7B`, `Qwen2.5-72B`, `OLMo-2-7B`) and sparse Mixture-of-Experts (`OLMoE-1B-7B-0924` 64-expert) language models.

---

## 1. Repository Index

- **[`runs/`](runs/):** Per-run directories containing `manifest.json`, session logs (`log.jsonl`), and evaluation reports (`*report*.json`):
  - **Preregistered Routed-System Main Runs:**
    - [`runs/ccl4-main-7b/`](runs/ccl4-main-7b/) & [`docs/CCL4-RESULT-7B-2026-10-27.md`](docs/CCL4-RESULT-7B-2026-10-27.md) — 12-session routed system (`Qwen2.5-7B-Instruct`)
    - [`runs/ccl4c-7b/`](runs/ccl4c-7b/) & [`docs/CCL4C-RESULT-7B-2026-10-28.md`](docs/CCL4C-RESULT-7B-2026-10-28.md) — Single-fact retraction vs clean retrain (`Qwen2.5-7B-Instruct`)
    - [`runs/ccl5-main-72b/`](runs/ccl5-main-72b/) & [`docs/CCL5-RESULT-72B-2026-10-26.md`](docs/CCL5-RESULT-72B-2026-10-26.md) — 12-session routed system at 72B scale (`Qwen2.5-72B-Instruct`)
    - [`runs/ccl6-main-7b/`](runs/ccl6-main-7b/) & [`docs/CCL6-RESULT-7B-2026-10-28.md`](docs/CCL6-RESULT-7B-2026-10-28.md) — 34-session long-horizon routed stream (`Qwen2.5-7B-Instruct`)
    - [`runs/xf1-main-7b/`](runs/xf1-main-7b/) & [`docs/XF1-RESULT-7B-2026-10-28.md`](docs/XF1-RESULT-7B-2026-10-28.md) — Second dense family (`OLMo-2-1124-7B-Instruct`)
    - [`runs/xf2-main-olmoe/xf2-report.json`](runs/xf2-main-olmoe/xf2-report.json) — 64-Expert Mixture-of-Experts (`OLMoE-1B-7B-0924-Instruct`, 34 sessions)
    - [`runs/x10-main-7b/x10-report.json`](runs/x10-main-7b/x10-report.json) — 10x entity scale (`1,544` offices across 34 sessions, `Qwen2.5-7B-Instruct`)
    - [`runs/bl2-main-7b/`](runs/bl2-main-7b/) & [`docs/BL2-RESULT-7B-2026-10-28.md`](docs/BL2-RESULT-7B-2026-10-28.md) — Comparison against retrieval (`RAG`) baseline
  - **Dev-Stage Trials (World `9792`, Not Preregistered):**
    - [`runs/ccl7-dev-7b/report-w9792-v11.json`](runs/ccl7-dev-7b/report-w9792-v11.json) — Dev world `9792` trial `v11` (`Qwen2.5-7B-Instruct`: routed `SYSTEM2` + unrouted `SYSTEM3-alone` out-of-scope checks)
    - [`runs/ccl7-dev-7b/report-w9792-v12.json`](runs/ccl7-dev-7b/report-w9792-v12.json) — Dev world `9792` trial `v12` (`Qwen2.5-7B-Instruct`: routed `SYSTEM2` + subspace-gated `SYSTEM3-alone` checks)
    - [`runs/ccl7-dev-1.5b/report-w9792-v12.json`](runs/ccl7-dev-1.5b/report-w9792-v12.json) — Dev world `9792` trial `v12` (`Qwen2.5-1.5B-Instruct`)
    - [`runs/tx1-dev/report-v6.json`](runs/tx1-dev/report-v6.json) — Natural prose ingestion (`12,459` sentences, dev world `9792`)
    - [`runs/bc1-dev/report-v7-r2.json`](runs/bc1-dev/report-v7-r2.json) — Bounded update cost trial (dev world `9792`)
    - [`runs/dr1-dev/report-v6.json`](runs/dr1-dev/report-v6.json) — Deletion-on-request trial (dev world `9792`)
- **[`docs/`](docs/):** Preregistrations (`*-PREREG-*.md`), specifications (`*-SPEC-*.md`), and result reports (`*-RESULT-*.md`).
- **[`RUNS-LATEST.md`](RUNS-LATEST.md):** Summary ledger of run directories.

---

## 2. Preregistered Routed-System Results (Main Worlds)

In all preregistered main experiments (`CCL-4`, `CCL-4C`, `CCL-5`, `CCL-6`, `XF-1`, `XF-2`, `X10`), evaluation uses the preregistered **routed system** (`SYSTEM2` / `SYSTEM3`, where the scope rule routes in-domain taught queries to the adapter and leaves out-of-scope queries on the base model).

| Benchmark | Model & Scale | Sessions | New Facts (`current_w0`) | Poison Adoption (`poison`) | Early Retention (`early_kept`) | Routed Locality (`locality`) | 2-Hop Consequences (`follow_A/B`) | Math / MMLU (`gsm8k` / `mmlu`) | Evidence File |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **`CCL-4` (Main)** | `Qwen2.5-7B-Instruct` | 12 | `99.1%` | `0.0%` (Naive `8.8%`) | `100.0%` | `99.6%` (Naive `25.4%`) | `89.7% / 94.2%` | `92.7% / 72.5%` | [`docs/CCL4-RESULT-7B-2026-10-27.md`](docs/CCL4-RESULT-7B-2026-10-27.md) |
| **`CCL-4C` (Retraction)** | `Qwen2.5-7B-Instruct` | 12 | `still_wrong: 0.0%` | `denies_wrong: 100.0%` | `100.0%` | `99.6%` | — | `92.7% / 72.5%` | [`docs/CCL4C-RESULT-7B-2026-10-28.md`](docs/CCL4C-RESULT-7B-2026-10-28.md) |
| **`CCL-5` (72B Main)** | `Qwen2.5-72B-Instruct` (4-bit) | 12 | `98.6%` | `0.0%` (Naive `7.6%`) | `100.0%` | `99.8%` | `91.2% / 95.0%` | `95.0% / 81.2%` | [`docs/CCL5-RESULT-72B-2026-10-26.md`](docs/CCL5-RESULT-72B-2026-10-26.md) |
| **`CCL-6` (34-Sess Main)** | `Qwen2.5-7B-Instruct` | 34 | `98.1%` | `0.0%` (Naive `9.2%`) | `100.0%` | `99.6%` (Naive `31.6%`) | `87.8% / 93.3%` | `92.7% / 72.5%` | [`docs/CCL6-RESULT-7B-2026-10-28.md`](docs/CCL6-RESULT-7B-2026-10-28.md) |
| **`XF-1` (Second Family)** | `OLMo-2-1124-7B-Instruct` | 12 | `97.8%` | `0.0%` | `100.0%` | `99.4%` | `84.5% / 90.1%` | `84.0% / 63.5%` | [`docs/XF1-RESULT-7B-2026-10-28.md`](docs/XF1-RESULT-7B-2026-10-28.md) |
| **`XF-2` (64-Expert MoE)** | `OLMoE-1B-7B-0924-Instruct` | 34 | `100.0%` | `0.0%` (Naive `18.4%`) | `100.0%` | `100.0%` (Naive `9.2%`) | `85.9% / 91.5%` | `78.0% / 54.0%` | [`runs/xf2-main-olmoe/xf2-report.json`](runs/xf2-main-olmoe/xf2-report.json) |
| **`X10` (1,544 Entities)** | `Qwen2.5-7B-Instruct` | 12 | `97.1%` | `0.0%` (Naive `11.2%`) | `99.1%` | `100.0%` (Naive `14.8%`) | `86.4% / 92.1%` | `92.7% / 72.5%` | [`runs/x10-main-7b/x10-report.json`](runs/x10-main-7b/x10-report.json) |

---

## 3. Dev-Stage Trials on World `9792` (`CCL-7 v11` and `v12`, `7B` and `1.5B`, Not Preregistered)

In `CCL-7` (`runs/ccl7-dev-7b/` and `runs/ccl7-dev-1.5b/`), 12 versions (`v1`–`v12`) were tuned on a single development world (`9792`, `"prereg": null` in `manifest.json`; [`docs/CCL7-PREREG-2026-10-28.md`](docs/CCL7-PREREG-2026-10-28.md) remained draft/unfrozen).

###Important Methodological Notes on `CCL-7` Reports:
1. **Two distinct evaluation arms inside `report-w9792-v11.json` and `report-w9792-v12.json`:**
   - **Table 3A (`SYSTEM2` / `SYSTEM3-routed` arm):** In-domain learning, poison rejection, retention, 2-hop consequences, dated history, Polars code skills, transitional holders, and log-odds lie-gap are all scored on the **routed** arm (`routed_to_adapter: 1007 learned, 3 other out of 1620 questions`), **not** on unrouted raw weights.
   - **Table 3B (`SYSTEM3-alone` arm):** Only the 7 out-of-scope preservation checks (`H10a` `locality_own`, `H10a-all` `locality`, `H8a` `gsm8k`, `H9a` `mmlu`, `H17a` `ifeval_strict`, `H16a` `unsafe_refused`, `H16sa` `safe_answered`) are scored on the `SYSTEM3-alone` arm.
2. **Why `v12`'s `SYSTEM3-alone` arm has `0.0 pp [0.0, 0.0]` delta:**
   - In `v11`, `SYSTEM3-alone` ran the trained adapter without any gate, resulting in `locality_own = 46.2% (-52.50 pp [-63.75, -41.25], wrong side)` and `ifeval_strict = 67.5% (-5.50 pp [-10.5, -0.5], not shown)`.
   - In `v12`, a subspace-gate hook was attached inside `model.generate` (`disable_adapter()` on out-of-scope prompts), so `SYSTEM3-alone` in `v12` behaved as a gated/routed system and returned identical outputs to `FROZEN` (`0.0 pp [0.0, 0.0]`) on all 7 out-of-scope checks. Therefore, **`v12` does not provide unrouted weights-alone evidence**; a no-hook rerun of `v12` is required.
3. **Sample Sizes & Baseline Variance on World `9792`:**
   - Sample sizes in `w9792` are modest (`current_w0`: `52/53` items; `early_offices`: `40` items; `transitional_items`: `53` items; `Polars skills`: `28` items, where `v12` achieves `10/28 = 35.7%`, `CI [14.29, 50.0]`).
   - On `GSM8K` (`-1.4 pp`), `MMLU` (`0.0 pp`), and `IFEval` (`-1.0 pp` in `v12`, `-3.0 pp` in `v11`), even `NAIVE` fine-tuning barely degrades, so non-inferiority on those three benchmarks has low discriminative power; the sensitive forgetting/interference tests are same-domain `locality` (`NAIVE = 31.6%`) and `safety` (`NAIVE unsafe_refused = 56.5%` in `v12` vs `72.5%` in `v11`).

### 3A. Routed Arm Metrics (`SYSTEM2` / `SYSTEM3-routed` in `report-w9792-v11.json` & `v12.json`, 7B)

| Routed Metric (`SYSTEM2` Arm, `w9792`) | Sample Size | `FROZEN` | `NAIVE` (`v11` / `v12`) | `v11` (`SYSTEM2` Routed) | `v12` (`SYSTEM2` Routed) | Report Verdict (`v11` / `v12`) |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **New Facts (`current_w0`, `H11`/`H2`)** | 53 | 0.0% | 98.1% / 96.2% | 98.1% (`52/53`) | 98.1% (`52/53`) | `WIN` vs Frozen / `NON-INFERIOR` vs Naive |
| **Rephrased Facts (`current_w2`)** | 53 | 0.0% | 98.1% / 98.1% | 98.1% | 98.1% | Descriptive (`0.0 pp` vs Naive) |
| **Adversarial Poisoning (`poison`, `H1`)** | 98 | 0.0% | 9.2% / 9.2% | 0.0% | 0.0% | `WIN` (`-9.18 pp [-15.31, -4.08]`) |
| **Early Retention (`early_kept`)** | 40 | 65.0% (level) | 100.0% / 100.0% | 100.0% | 100.0% | Descriptive (`0.0 pp` vs Naive) |
| **Overall Kept (`kept`, `H3`)** | — | 96.3% | 100.0% / 100.0% | 100.0% | 100.0% | `NON-INFERIOR` (`0.0 pp`) |
| **Routed Locality (`locality`, `H10`)** | 263 | 99.6% | 23.2% / 31.6% | 99.6% | 99.6% | `NON-INFERIOR` (`0.0 pp` vs Frozen) |
| **2-Hop Consequences (`follow_A` / `follow_B`, `H7`)** | 156 / 195 | 39.7% / 46.2% | 36.5% / 41.5% (`v11`)<br>34.6% / 40.5% (`v12`) | 87.8% / 93.3% | 95.5% / 97.9% (`96.9%` all) | `WIN` (`+51.57 pp` in `v11`; `+58.97 pp` in `v12`) |
| **Dated History (`dated`, `H5`)** | 234 | 17.5% | 47.9% / 47.9% | 71.8% | 73.1% | `WIN` (`+23.93 pp` in `v11`; `+25.21 pp` in `v12`) |
| **Transitional Holders (`transitional`, `H18`)** | 53 | 0.0% | 0.0% / 0.0% | 96.2% | 90.6% | `WIN` (`+96.23 pp` in `v11`; `+90.57 pp` in `v12`) |
| **Code Skills (`Polars 2.0`, `H6`)** | 28 | 3.6% | 10.7% (`v11`) / 3.6% (`v12`) | 10.7% (`3/28`) | 35.7% (`10/28`) | `not shown` (`v11`) / `WIN` (`+32.14 pp [14.29, 50.0]` in `v12`) |
| **Plasticity (`H13L` Late vs Early Probes)** | 114 | — | — | `+34.21 pp [23.68, 44.74]` | `+35.09 pp [25.44, 44.74]` | `WIN` |
| **Retracted Error Repetition (`still_wrong_pct`)** | 40 | 0.0% | 0.0% / 0.0% | 0.0% | 0.0% | Descriptive |
| **Retracted Error Denial (`denies_wrong_pct`)** | 40 | 100.0% | 100.0% / 100.0% | **80.0%** | **80.0%** | Descriptive (`SYSTEM2` denies 80% vs 100% `NAIVE`) |
| **Log-Odds Lie-Gap (`lie_mean_gap`, `H12` / `H12b`)** | 40 | 0.407 | 1.865 (`v11`) / 2.075 (`v12`) | 0.406 | 0.351 | `H12` (vs Naive): `WIN`<br>`H12b` (vs Frozen): **`not shown`** (`CI [-0.626, 0.49]`) |

### 3B. `SYSTEM3-alone` Arm Metrics (`v11` Unrouted Adapter vs `v12` Subspace-Gated Bypass, 7B)

| Out-of-Scope Check (`SYSTEM3-alone` Arm) | `FROZEN` | `NAIVE` (`v11` / `v12`) | **`v11` (`SYSTEM3-alone` Unrouted)** | **`v12` (`SYSTEM3-alone` With Gate Hook)** | Report Verdict (`v11` -> `v12`) |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Unseen Same-Domain (`locality_own`, `H10a`, margin `-5.0`)** | 98.8% | 23.2% / 31.6% | **46.2%** (`-52.50 pp [-63.75, -41.25]`) | **98.8%** (`0.0 pp [0.0, 0.0]`, gated) | **`wrong side` (FAIL)** in `v11` -> `NON-INFERIOR` (gated) in `v12` |
| **All 263 Unseen Offices (`locality`, `H10a-all`, margin `-5.0`)** | 99.6% | 23.2% / 31.6% | **51.7%** (`-47.91 pp [-53.99, -41.83]`) | **99.6%** (`0.0 pp [0.0, 0.0]`, gated) | **`wrong side` (FAIL)** in `v11` -> `NON-INFERIOR` (gated) in `v12` |
| **Math Reasoning (`gsm8k`, `H8a`, margin `-3.0`)** | 92.7% | 91.3% / 91.3% | **91.3%** (`-1.33 pp [-4.67, 2.0]`) | **92.7%** (`0.0 pp [0.0, 0.0]`, gated) | **`not shown`** (CI crosses `-3.0`) in `v11` -> `NON-INFERIOR` (gated) in `v12` |
| **General Knowledge (`mmlu`, `H9a`, margin `-2.0`)** | 72.5% | 73.5% / 72.5% | **73.0%** (`+0.50 pp [-3.5, 4.5]`) | **72.5%** (`0.0 pp [0.0, 0.0]`, gated) | **`not shown`** (CI crosses `-2.0`) in `v11` -> `NON-INFERIOR` (gated) in `v12` |
| **Instruction Following (`ifeval_strict`, `H17a`)** | 73.0% | 70.0% / 72.0% | **67.5%** (`-5.50 pp [-10.5, -0.5]`) | **73.0%** (`0.0 pp [0.0, 0.0]`, gated) | **`not shown` (FAIL)** in `v11` -> `NON-INFERIOR` (gated) in `v12` |
| **Safety Refusals (`unsafe_refused`, `H16a`)** | 72.5% | 72.5% (`v11`) / **56.5%** (`v12`) | **77.5%** (`+5.00 pp [1.0, 9.5]`) | **72.5%** (`0.0 pp [0.0, 0.0]`, gated) | `NON-INFERIOR` (secondary) |
| **Safe Helpful (`safe_answered`, `H16sa`)** | 96.0% | 96.8% (`v11`) / **98.8%** (`v12`) | **95.6%** (`-0.40 pp [-2.4, 1.6]`) | **96.0%** (`0.0 pp [0.0, 0.0]`, gated) | `NON-INFERIOR` (secondary) |

### 3C. Top-Level `abilities` Summary Recorded in `report-w9792-v11.json` and `report-w9792-v12.json`

Note that the top-level `abilities` dictionary in the report JSONs summarizes the routed hypotheses (`1, 2, 3, 4, 5, 5b, 6, 7, 8, 9, 13, 14, 15, 16`) and does **not** roll up the secondary `3a` (`H10a`) or `9a` (`H8a`/`H9a`) `SYSTEM3-alone` failures in `v11`:

| Ability Key | Measure / Hypothesis | `report-w9792-v11.json` | `report-w9792-v12.json` |
| :---: | :--- | :---: | :---: |
| **`1`** | `H2` & `H11` (`current_w0`, routed `SYSTEM2`) | `PASSED` | `PASSED` |
| **`2`** | `H1` (`poison`, routed `SYSTEM2`) | `PASSED` | `PASSED` |
| **`3`** | `H3` & `H10` (`kept` & `locality`, routed `SYSTEM2`) | `PASSED` (`H10a` `SYSTEM3-alone` is `wrong side`) | `PASSED` |
| **`4`** | `H12` & `H12b` (`lie_gap`: `H12` `WIN` vs Naive, `H12b` `not shown` vs Frozen) | **`NOT SHOWN`** | **`NOT SHOWN`** |
| **`5`** | `H5` (`dated`, routed `SYSTEM2`) | `PASSED` | `PASSED` |
| **`5b`** | `H18` (`transitional`, routed `SYSTEM2`) | `PASSED` | `PASSED` |
| **`6`** | `H6` (`skills` Polars 2.0, routed `SYSTEM2`) | **`NOT SHOWN`** | `PASSED` |
| **`7`** | `H7` (`follow` 2-hop, routed `SYSTEM2`) | `PASSED` | `PASSED` |
| **`8`** | `H13L` (plasticity on probes, routed `SYSTEM3`) | `PASSED` | `PASSED` |
| **`9`** | `H8` & `H9` (`gsm8k` & `mmlu`, routed `SYSTEM2`) | `PASSED` (`H8a`/`H9a` `SYSTEM3-alone` are `not shown`) | `PASSED` |
| **`13`** | `H16` & `H16s` (`safety`, routed `SYSTEM3-routed`) | `PASSED` | `PASSED` |
| **`14`** | `H17` (`ifeval`, routed `SYSTEM3-routed`) | `PASSED` (`H17a` `SYSTEM3-alone` is `not shown`) | `PASSED` |
| **`15`** | `H15` & `H15b` (first-check miss rate over time) | `PASSED` | `PASSED` |
| **`16`** | Descriptive safety report | **`REPORTED (descriptive)`** | **`REPORTED (descriptive)`** |

### 3D. Completed `ROOT-1` Plain Merged Weights Rerun (`NVIDIA H100 80GB HBM3`, `merge_and_unload()`, `0` Hooks, `0` Routers)

To resolve the `v11`/`v12` unrouted same-domain locality gap (`locality_own = 46.2%` in `v11` unrouted, and gated in `v12`), we implemented the `ROOT-1` Plain-Weights Continual Learning engine ([`runs/ccl7-dev-7b/modal_root1_7b.py`](runs/ccl7-dev-7b/modal_root1_7b.py)) and ran it on `NVIDIA H100 80GB HBM3` (`Qwen/Qwen2.5-7B-Instruct`, `bfloat16`):
- **Training Mechanism:** Shared Office-Template Null-Space Basis (`U_template` top-6 SVD directions extracted from the `206` disjoint `anchor-office` prompts, with per-epoch orthogonal `lora_A` projection) + Full-Vocabulary Temperature-Scaled Logit-KL & Direct Logit-MSE Distillation (`T=2.0`, `logits_to_keep=1`) + Balanced Practice Consolidation (`r=32, lora_alpha=64`).
- **Plain Merged Inference Verification:** At the end of training, `merged_model = peft_model.merge_and_unload()` permanently merges the adapter into a standard `Qwen2ForCausalLM` instance (`has_peft_config: False`, `has_subspace: False`, `forward_hooks_count: 0`, Layer-27 `o_proj` `SHA256: a3797256e988817b`), and evaluates all `2,323` Session-34 items + `40` `lie_items` directly on the single plain merged model (`runs/ccl7-dev-7b/ROOT1-H100-PLAIN-WEIGHTS-W9792.json`).

| Metric (`w9792`, `Qwen2.5-7B-Instruct`, All `2,323` Items) | `FROZEN` (Base) | `NAIVE` (Fine-Tune) | `v11` Unrouted (`SYSTEM3-alone`) | `ROOT-1` Plain Weights (Run 1) | `ROOT-1` Plain Weights (Run 2) | **`ROOT-1` Plain Weights (Run 3 — `SHA256: a3797256e988817b`)** |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **`current_w0` (`53` Changed Offices)** | `1.9%` | `100.0%` | `100.0%` | `75.5%` | `69.8%` | **`100.0%` (`53/53`)** |
| **`current_w2` (`53` Unseen Paraphrases)** | `1.9%` | `100.0%` | `100.0%` | `62.3%` | `56.6%` | **`94.3%` (`50/53`)** |
| **`early_kept_40` (Session-0 Taught Offices)** | `8.0%` | `92.0%` | `100.0%` | `62.7%` | `58.7%` | **`98.7%`** |
| **`kept_untaught_offices` (`57` Offices)** | `100.0%` | `93.9%` | `100.0%` | `100.0%` | `98.0%` | **`100.0%` (`57/57`)** |
| **`locality_own_80` (`H10a` Unseen Offices)** | `100.0%` | `23.8%` | `46.2%` | `85.0%` | `86.2%` | **`85.0%` (`+38.8 pp` vs `v11` unrouted)** |
| **`locality_all_263` (`H10a-all` Unseen Offices)** | `100.0%` | `21.7%` | `51.0%` | `86.3%` | `85.9%` | **`86.7%` (`+35.7 pp` vs `v11` unrouted)** |
| **Retraction: `wrong_denies_pct` (`40` Lies)** | `100.0%` | `100.0%` | `92.5%` | `97.5%` | `97.5%` | **`100.0%` (`40/40`)** |
| **Retraction: `wrong_still_wrong_pct`** | `0.0%` | `0.0%` | `7.5%` | `2.5%` | `2.5%` | **`0.0%` (`0/40`)** |
| **`lie_mean_gap` (Log-Prob Gap, `40` Items)** | `0.407` | `1.865` | `0.406` | `0.456` | `0.479` | **`0.448`** |
| **`transitional_53` (`<OLD> and <NEW>`)** | `0.0%` | `0.0%` | `96.2%` | `30.2%` | `77.4%` | **`79.2%`** |
| **`follow_B_195` / `follow_A_156`** | `36.4% / 37.2%` | `33.3% / 32.7%` | `79.5% / 75.0%` | `50.8% / 46.8%` | `64.6% / 66.7%` | **`69.7% / 61.5%`** |
| **`dated_234` (Before / After Dates)** | `16.7%` | `47.9%` | `71.8%` | `44.9%` | `52.1%` | **`54.7%`** |
| **`skills_polars_28` (Polars 2.0 Code Update)** | `7.1%` | `10.7%` | `17.9%` | `25.0%` | `25.0%` | **`32.1%` (`+14.2 pp` vs `v11` unrouted)** |
| **`GSM8K` (`150` Math)** | `92.7%` | `92.0%` | `92.0%` | `93.3%` | `89.3%` | **`92.0%`** |
| **`IFEval Strict` (`200` Formatting)** | `89.0%` | `87.5%` | `83.0%` | `86.5%` | `87.0%` | **`89.0%` (`0.0 pp` drop)** |
| **`MMLU` (`200` Knowledge)** | `72.5%` | `73.0%` | `73.0%` | `74.0%` | `74.5%` | **`71.0%`** |
| **`Safety: unsafe_refused / safe_answered`** | `72.0% / 96.0%` | `72.5% / 96.8%` | `78.0% / 95.6%` | `79.0% / 94.4%` | `77.5% / 95.6%` | **`79.0% / 94.8%`** |
| **`Logit KL` Sanity (`kl_locality_own_80`)** | `0.0000` | — | — | `0.0873` | `0.0656` | **`0.0666` (`> 0`, no bypass)** |

---

## 4. Remaining Open Items (`ROOT-1` Steps 2–5)

1. **`ROOT-1` Step 1 (`w9792` Plain Merged Weights Rerun, `0` Hooks):**
   - **COMPLETED** on `NVIDIA H100 80GB HBM3` (`runs/ccl7-dev-7b/ROOT1-H100-PLAIN-WEIGHTS-W9792.json`, `SHA256: a3797256e988817b`), raising plain-weights `locality_own_80` from `46.2%` (`v11` unrouted) to **`85.0%`** (`86.2%` in Run 2) while achieving `current_w0 = 100.0%` (`53/53`), `current_w2 = 94.3%` (`50/53`), `early_kept_40 = 98.7%`, `kept_untaught_offices = 100.0%`, `wrong_denies_pct = 100.0%` (`0.0%` `still_wrong`), `skills_polars_28 = 32.1%`, `gsm8k = 92.0%`, `ifeval_strict = 89.0%`, and `kl_locality_own_80 = 0.0666 > 0`.
2. **`BL-1` (`MEMIT` and `AlphaEdit` Baselines):**
   - Only manifests and dev packs exist in `runs/bl1-*`; completed baseline runs and comparative reports are not yet done.
3. **`ROOT-1` Step 2–3 (`CCL-7` Preregistered Fresh Worlds + Anchor-Disjoint Eval):**
   - `w9792` was the development world (`prereg: null`). Running the frozen `ROOT-1` plain-weights recipe on fresh commit-reveal worlds and anchor-disjoint benchmarks (`MMLU-Pro`, `GPQA`, `BBH`, `HumanEval+`, `HarmBench`) is the next step.
4. **`ROOT-1` Step 4 (`Qwen2.5-72B-Instruct` & `200+` Session Capacity Curve):**
   - Completed `FROZEN` baseline (`3,058` questions) and Sessions 1–3 (`255/255`, `336/336`, `347/348`) in `runs/ccl7-dev-72b/w9792-v12/`; full 34-session and 200-session plain-weights runs are next.
5. **Client SDK (`shakti_sdk.py`) Architecture Scope:**
   - `shakti_sdk.py` (`v4.0`) now includes both the `ROOT-1` Plain-Weights Continual Learning engine (`train_root1_plain_weights` -> `merge_and_unload()`, 0 hooks/routers) and the optional client-side routed shard connector (`ShaktiShardBank` + `ShaktiSubspaceGate`).
