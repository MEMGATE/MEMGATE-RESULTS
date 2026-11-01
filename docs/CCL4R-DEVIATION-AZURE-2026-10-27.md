# CCL-4R deviation: the worlds run on Azure's serverless A100s

**Status: written 27 October 2026, 18:58 IST (commit b4008bee).** This was written before any CCL-4R world ran anywhere and before any was packed for this machine:
- worlds 9704 and 9705 were packed for Kaggle's TPU and have stayed in its queue since about 12:30 without starting;
- worlds 9706 and 9707 have not been packed.

It changes the machine only. The preregistration `docs/CCL4R-PREREG-2026-10-27.md` (frozen 11:57 IST) is otherwise unchanged.

## What changes
- **Machine.** Azure Container Apps serverless GPU (environment `memgate-gpu-swc`, Sweden Central), granted on 27 October at 18:10 IST. Each world gets one NVIDIA A100 80 GB PCIe, 8 vCPUs and 64 GiB; the price is about $3.86 an hour.
  - The preregistration named Kaggle's TPU v5e-8 or, from 31 October, Kaggle's two T4s, "whichever runs a world first".
  - Neither has run a world. The TPU queue has not started the two queued runs in about six and a half hours, and Kaggle's GPU hours return only on 31 October.
- **Code.** The frozen GPU runner the preregistration names (`clx.code_hash()` `f2a25824cacd9cae7155e457139de4859bd5b68ce63b037182e62c1f1cc66395`), in Colab's layout:
  - The kernel is `colab_pack.colab_kernel("7b", 4)`, SHA-256 `a5567bf076191d456e578c49696fdb767a2ff0cb7bcecd1f63fec520a2ce53b5`. This is byte for byte the kernel CCL-4's 7B worlds ran on Colab's A100 (`docs/CCL4-DEVIATION-7B-COLAB-2026-10-26.md`; `runs/ccl4-main-7b-colab/w970X/colab/kernel.py`). It reads its payload from `/content/input` and writes to `/content/working`; nothing else differs.
  - The runner is `cl/aca_run.py` (new). It uploads the payload and the kernel to an Azure Files share, and runs one job per world with no automatic retry. `/content/working` lies on the share, so every output line is kept as it is written, and the runner copies the outputs back into `kaggle-output/`.
  - The image is `memgatecclswc.azurecr.io/ccl-gpu:1`: PyTorch 2.5.1 with CUDA 12.4, plus transformers 4.47.1, peft 0.13.2 and accelerate 1.1.1 (the kernel's own pins).
- **Model.** Qwen2.5-7B-Instruct from Hugging Face at revision `a09a35458c702b33eeacc393d103063234e8bc28`, in 16 bits, as the preregistration states for the GPUs.
- **Payloads.** Each is packed with `PYTHONHASHSEED=0 python cl/colab_pack.py 970X:main runs/ccl4r-7b-azure/w970X --model 7b --arms SYSTEM2,NAIVE --errors 40 --errors-at 0 --wide --share 1.0 --prereg docs/CCL4R-PREREG-2026-10-27.md`.
  - The packer's guard checks the runner's hash against the preregistration.
  - For 9704 and 9705, the payloads are compared with the TPU packs of the same worlds before the runs start. Both are built by `clx.payload` with the same options, and any difference is reported.
- **Order.** 9704 and 9705 run at once on the two A100s, then 9706 and 9707.

## What does not change
- the worlds 9704–9707 and their options;
- the arms: SYSTEM2 then NAIVE, and the untouched model;
- 12 sessions, with evaluations after sessions 4, 8 and 12;
- the hypotheses H12 and H12b, their rules, and the four worlds pooled;
- the analysis command and the validity rules;
- the 7 November cutoff.

## Which run of a world counts
The preregistration's own rule applies: the first run of a world counts. The Azure runs start first. The account holder is asked to cancel the two TPU runs still queued on Kaggle. If either starts anyway, its output is kept and reported, but not analysed.

## A failed run
A run stopped by the machine without output is rerun once with the same payload and kernel, as the preregistration allows. The rerun uses the same machine type and a new output folder, and both runs are recorded.

## Dev check before the first world
Before any CCL-4R world starts, a two-session dev run checks the pipeline on the same machine and image: CCL-4's dev world 9792, SYSTEM2 only, `runs/aca-dev/w9792-s2`. It covers:
- the model download;
- the untouched model's answers;
- training and practice;
- the outputs on the share, and copying them back.
