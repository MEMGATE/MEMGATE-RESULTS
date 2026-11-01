# XF-M preregistration: CCL-4's test on the labs' own open models (frozen)

**Status: FROZEN on 28 October 2026, 17:01 IST, after the three families' two-session dev runs and before any XF-M main world was packed.**
- Drafted at 13:06 and updated at 16:05 (the models' sources as used, Phi-4's dev numbers, the machines) and 16:42 (Llama's dev numbers).
- Added at the freeze: Gemma's dev numbers, the untouched models' knowledge of the dev world, the code hashes and the predictions.
- One document and one code hash cover the three families.
- Part B item 13 (`docs/PARTB-PLAN-2026-10-28.md`).

## Why
XF-1 showed the learner on a second family: OLMo-2-7B, abilities 1–7 and 9 PASSED. XF-M runs the same test on the open models of the labs the package goes to, so that each lab can see the learner on its own model.

## The system under test
SYSTEM2, CCL-4's learner, unchanged. It is run by CCL-4's frozen GPU runner in Colab's layout. The runner is changed only where a family needs it (`cl/xfm.py`); each change replaces whole lines and is checked to apply exactly once.

**Phi-4** (Microsoft, 14B, MIT licence)
- Source: `microsoft/phi-4`, revision `2db69c1c3e91a05d2c64a3185acfbaf36f744e25`, downloaded inside the job from its public, ungated page.
- Change: adapters on its fused `qkv_proj` and on `o_proj`, in place of `q_proj`, `k_proj`, `v_proj` and `o_proj`.
- Weights: 16 bits.

**Llama-3.1-8B-Instruct** (Meta)
- Source: Azure's model registry `azureml-meta`, `Meta-Llama-3.1-8B-Instruct`, version 6. The founder asked that no model come from Hugging Face accounts.
- Files are on the jobs' share; their SHA-256 values are in `docs/MODELS-2026-10-28.md`.
- Change: none.
- Weights: 16 bits.

**Gemma-2-9B-it** (Google)
- Source: Kaggle Models `google/gemma-2`, transformers, `gemma-2-9b-it`, version 1. The licence was accepted on the lab's Kaggle account.
- Files are on the jobs' share; their SHA-256 values are in `docs/MODELS-2026-10-28.md`.
- Changes:
  - the system message is folded into the first user turn, because its template refuses system messages;
  - bfloat16 with eager attention, as its makers advise.

**Code SHA-256 lines:**
- CCL-4's GPU runner, `clx.code_hash()`: Code SHA-256: `f2a25824cacd9cae7155e457139de4859bd5b68ce63b037182e62c1f1cc66395`
- The XF-M packer with the job runner, `xfm.code_hash()`: Code SHA-256: `c2083382b207790ae8b028c156745c12295b206036bbbdf1b4acd490706ccf6b`
- Analysis: CCL-4's frozen `cl/ccl4.py` (`525e21ff010b…`).
- Phi-4's dev pack was built by the packer's earlier text, before Llama's and Gemma's sources were added (`4b510c41…`). Rebuilt with this packer, its payload and kernel are byte-identical (`77fa33a464cf…`, `06fc4880c7f3…`).

## Dev runs (dev world 9792, two sessions, 20 registry errors; not part of the test)

**Phi-4** (`runs/xfm-dev/phi-w9792-s2`): on the lab's A100 VM, 28 October 15:35–15:47 IST, including the kernel's installs.
- Exit code 0 and a done line.
- In 16 bits it fit the 80 GB card.
- The untouched model:
  - answered all 2,290 questions in 242 seconds, in the expected forms;
  - on the 20 lie items, preferred the wrong value 12 times.
- SYSTEM2 trained two sessions:
  - 509 and 501 rows, in 59 and 57 seconds;
  - at their first check, 0 of 231 and 7 of 110 new items were missed;
  - practice ran as designed.
- NAIVE trained two sessions: 542 and 516 rows, in 38 and 36 seconds.

**Llama-3.1-8B** (`runs/xfm-dev/llama-w9792-s2`): on Azure's serverless A100, 28 October 16:30–16:41 IST, mounted from the share.
- Exit code 0 and a done line.
- The untouched model:
  - answered all 2,290 questions in 125 seconds, in the expected forms (names for offices and dates, worked answers for GSM8K, letters for MMLU);
  - on the 20 lie items, preferred the wrong value 10 times.
- SYSTEM2 trained two sessions:
  - 509 and 503 rows, in 50 seconds each;
  - at their first check, 4 of 231 and 6 of 110 new items were missed;
  - practice ran as designed.
- NAIVE trained two sessions: 542 and 516 rows, in 43 and 41 seconds.

**Gemma-2-9B** (`runs/xfm-dev/gemma-w9792-s2`): on Azure's serverless A100, 28 October 16:41–16:58 IST, mounted from the share, in bfloat16 with eager attention.
- Exit code 0 and a done line.
- The untouched model:
  - answered all 2,290 questions in 257 seconds, in the expected forms (its system message folded into the first turn);
  - on the 20 lie items, preferred the wrong value 9 times.
- SYSTEM2 trained two sessions:
  - 509 and 501 rows, in 78 and 79 seconds;
  - at their first check, 0 of 231 and 3 of 110 new items were missed;
  - practice ran as designed.
- NAIVE trained two sessions: 542 and 516 rows, in 71 and 68 seconds.

**What the untouched models already know of the dev world.** Of its 53 changed offices that no attacker targets, each untouched model named the holder at session 12 for 0 (Phi-4, Llama, Gemma). OLMo-2 named 2 (3.8%). The first holder was named for 58.5% (Phi-4), 64.2% (Llama), 73.6% (Gemma) and 11.3% (OLMo-2). So the three labs' models leave the full room to learn, and they know the world's earlier holders far better than OLMo-2 did.

## Design
- **Worlds:** 9702 and 9703, CCL-4's main worlds, with CCL-4's options:
  - 40 registry errors believed in session 1 and corrected in session 4;
  - 12 sessions;
  - evaluations after sessions 4, 8 and 12.

  The packer checks that every question equals CCL-4's payloads.
- **Arms:** SYSTEM2, then NAIVE, and the untouched model.
- **Machine:**
  - Llama and Gemma: Azure's serverless A100 (`cl/aca_run.py`), because they mount their files from the jobs' share.
  - Phi-4: Azure's serverless A100, or the lab's A100 VM (`cl/vm_run.py`; `docs/MACHINE-A100-VM-2026-10-28.md`), whichever is free first. Both have the same GPU model (A100 80GB PCIe).

  Each run's `aca.json` or `vm.json` records the machine, and the result names it.
- **Packs:** `PYTHONHASHSEED=0 python cl/xfm.py pack 970X:main runs/xfm-main-<family>/w970X --family <family> --questions-from runs/ccl4-main-7b-colab/w970X/dataset/payload.json --prereg docs/XFM-PREREG-2026-10-28.md`.

## Hypotheses
CCL-4's hypotheses, with CCL-4's rules, after session 12, both worlds pooled, for each family:
- H1, H2, H11, H3 and H10;
- H12 and H12b;
- H5, H6 and H7;
- H13;
- H8 and H9.

REPLAY does not run, so R1–R3 are not tested. Each family's verdicts are reported beside Qwen2.5-7B's (CCL-4) and OLMo-2-7B's (XF-1).

## Analysis
For each family: `python cl/ccl4.py report runs/xfm-main-<family>/xfm-report.json runs/xfm-main-<family>/w9702 runs/xfm-main-<family>/w9703`

## Validity
As in CCL-4 and XF-1:
- both arms finished their 12 sessions;
- the untouched model answered every question and named the current holder of at most 10% of changed offices;
- the removal ran in session 4;
- the lie scores exist for every arm.

A run stopped by the machine without output is rerun once, in a new folder.

## Predictions
The same for each family:
- **WIN:** H1, H11, H5, H6, H7 and H12. These rest on what the gate admits and on the rows trained; all three models trained and checked their new items as Qwen and OLMo-2 did.
- **NON-INFERIOR:** H2, H3, H10, H8 and H9.
- **NOT SHOWN, more likely than not:** H12b and H13.
  - H12b (removal against the untouched model) was not shown on Qwen in CCL-4 or CCL-4R, and was shown on OLMo-2 in XF-1. These models know the world's people about as well as Qwen does.
  - H13 (learning better over twelve sessions) was shown in CCL-4 at 7B but not in XF-1 or CCL-4C.

So abilities 1, 2, 3, 5, 6, 7 and 9 are predicted PASSED for each family, and 4 and 8 NOT SHOWN, more likely than not. A family that fails an ability that passed on Qwen is reported as such, beside Qwen's and OLMo-2's verdicts.
