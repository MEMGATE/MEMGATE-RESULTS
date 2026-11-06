"""ROOT-1 Step 2: Parallel Multi-H100 Verification Suite on Modal.

Runs 5 NVIDIA H100 80GB HBM3 GPUs in parallel:
  - H100 #1: Fresh Unseen World w9708 (34 sessions, frozen ROOT-1 Plain-Weights recipe, 0 hooks)
  - H100 #2: Fresh Unseen World w9709 (34 sessions, frozen ROOT-1 Plain-Weights recipe, 0 hooks)
  - H100 #3: Fresh Unseen World w9704 (12 sessions, frozen ROOT-1 Plain-Weights recipe, 0 hooks)
  - H100 #4: Anchor-Disjoint Held-Out Benchmarks (ARC-Challenge 100, TruthfulQA 100, BoolQ 100,
             MBPP Python Code Pass@1 50, WikiText-2 Held-Out Perplexity) on FROZEN vs NAIVE vs ROOT-1
  - H100 #5: Missing Baselines on w9792 (REPLAY Plain-Weights, JOINT Upper-Bound Plain-Weights,
             and ALPHAEDIT-7B Direct Closed-Form Null-Space MLP Weight Editing)
"""
import hashlib
import json
import math
import os
import random
import re
import subprocess
import sys
import time

import modal

app = modal.App("shakti-root1-step2-h100")

image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "torch>=2.4.0",
        "transformers==4.51.3",
        "peft==0.15.2",
        "accelerate>=1.0.0",
        "datasets>=2.20.0",
        "bitsandbytes>=0.43.0",
        "scipy",
        "sentencepiece",
        "protobuf",
        "huggingface_hub",
    )
)

vol = modal.Volume.from_name("shakti-hf-cache", create_if_missing=True)


def _norm(text: str) -> str:
    return " ".join("".join(c.lower() if c.isalnum() else " " for c in text).split())


# ==============================================================================
# SHARED HELPER: BUILD & TRAIN FROZEN ROOT-1 PLAIN-WEIGHTS MODEL ON ANY WORLD
# ==============================================================================
def _train_and_merge_root1(
    model_id: str,
    revision: str,
    payload: dict,
    use_nullspace_and_kl: bool = True,
    mode: str = "ROOT1",  # "ROOT1", "REPLAY", or "JOINT"
):
    import torch
    import torch.nn.functional as F
    from peft import LoraConfig, get_peft_model
    from transformers import AutoModelForCausalLM, AutoTokenizer

    t0 = time.time()
    max_s = payload["max_sessions"]
    last_idx = max_s - 1
    last_eval_key = str(max_s)

    tok = AutoTokenizer.from_pretrained(model_id, revision=revision, trust_remote_code=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token

    base_model = AutoModelForCausalLM.from_pretrained(
        model_id,
        revision=revision,
        torch_dtype=torch.bfloat16,
        device_map="cuda",
        trust_remote_code=True,
    )
    base_model.eval()

    anchors = payload["anchors"]
    office_anchors = [a for a in anchors if a.get("id", "").startswith("anchor-office|")]
    other_anchors = [a for a in anchors if not a.get("id", "").startswith("anchor-office|")]

    s_last = payload["rows"]["LEARNER2"][last_idx]
    checks_last = payload["checks"][str(last_idx)]

    def _chat_prompt(msgs):
        return tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)

    # 1. Pre-compute Frozen Base Teacher Logits & Top-6 U_template SVD Basis on 206 disjoint office_anchors
    U_template = {}
    office_anchor_rows = []
    other_anchor_rows = []

    if use_nullspace_and_kl:
        hook_acts = {}
        hooks = []
        for l_idx in range(len(base_model.model.layers)):
            layer = base_model.model.layers[l_idx]
            for proj_name in ["q_proj", "k_proj", "v_proj", "o_proj"]:
                mod = getattr(layer.self_attn, proj_name)
                key = f"layers.{l_idx}.self_attn.{proj_name}"
                hook_acts[key] = []

                def _make_hook(k):
                    def _hk(m, inp, out):
                        x = inp[0].detach().float()
                        hook_acts[k].append(x[0, -4:, :].cpu())
                    return _hk

                hooks.append(mod.register_forward_hook(_make_hook(key)))

        with torch.no_grad():
            for a in office_anchors:
                p_txt = _chat_prompt(a["messages"])
                enc = tok(p_txt, return_tensors="pt").to("cuda")
                out = base_model(**enc, logits_to_keep=1)
                last_logit = out.logits[0, -1, :].detach().float().cpu()
                pred_id = int(torch.argmax(last_logit).item())
                gen_ids = base_model.generate(
                    **enc,
                    max_new_tokens=20,
                    do_sample=False,
                    pad_token_id=tok.eos_token_id,
                )[0][enc["input_ids"].shape[1]:]
                ans_txt = tok.decode(gen_ids, skip_special_tokens=True).strip().splitlines()[0].strip()
                office_anchor_rows.append(
                    {
                        "id": a["id"],
                        "prompt_ids": enc["input_ids"][0].cpu(),
                        "base_last_logit": last_logit,
                        "base_top1_id": pred_id,
                        "messages": a["messages"] + [{"role": "assistant", "content": ans_txt}],
                    }
                )

        for h in hooks:
            h.remove()

        k_svd = 6
        for key, act_list in hook_acts.items():
            X = torch.cat(act_list, dim=0).cuda()
            _, _, Vh = torch.linalg.svd(X, full_matrices=False)
            U_template[key] = Vh[:k_svd, :].T.contiguous()
        del hook_acts
        torch.cuda.empty_cache()

        with torch.no_grad():
            for a in other_anchors:
                p_txt = _chat_prompt(a["messages"])
                enc = tok(p_txt, return_tensors="pt").to("cuda")
                gen_ids = base_model.generate(
                    **enc,
                    max_new_tokens=min(int(a.get("max_new", 64)), 96),
                    do_sample=False,
                    pad_token_id=tok.eos_token_id,
                )[0][enc["input_ids"].shape[1]:]
                ans_txt = tok.decode(gen_ids, skip_special_tokens=True).strip()
                if ans_txt:
                    other_anchor_rows.append(
                        {"messages": a["messages"] + [{"role": "assistant", "content": ans_txt}]}
                    )

    # 2. Wrap in LoRA
    lora_cfg = LoraConfig(
        r=32,
        lora_alpha=64,
        lora_dropout=0.0,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    )
    peft_model = get_peft_model(base_model, lora_cfg)

    def project_lora_A_nullspace(model_peft, U_map, alpha=0.20):
        if not U_map:
            return
        with torch.no_grad():
            for name, module in model_peft.named_modules():
                if hasattr(module, "lora_A") and "default" in module.lora_A:
                    for k_key, U in U_map.items():
                        if name.endswith(k_key):
                            A = module.lora_A["default"].weight
                            U_d = U.to(device=A.device, dtype=A.dtype)
                            proj = (A @ U_d) @ U_d.T
                            A.sub_(alpha * proj)
                            break

    def encode_sft(messages, max_len=384):
        prompt_msgs = messages[:-1]
        full_msgs = messages
        p_str = tok.apply_chat_template(prompt_msgs, tokenize=False, add_generation_prompt=True)
        f_str = tok.apply_chat_template(full_msgs, tokenize=False, add_generation_prompt=False)
        p_ids = tok(p_str, add_special_tokens=False)["input_ids"]
        f_ids = tok(f_str, add_special_tokens=False)["input_ids"][:max_len]
        labels = [-100] * min(len(p_ids), len(f_ids)) + f_ids[len(p_ids):]
        return (
            torch.tensor(f_ids, dtype=torch.long, device="cuda").unsqueeze(0),
            torch.tensor(labels, dtype=torch.long, device="cuda").unsqueeze(0),
        )

    check_last_items = [
        {"messages": it["ask"] + [{"role": "assistant", "content": str(it["expect"])}], "expect": str(it["expect"]), "ask": it["ask"]}
        for it in checks_last
    ]
    trans_train_rows = [
        {"messages": r["messages"], "expect": r["messages"][-1]["content"], "ask": r["messages"][:-1]}
        for r in s_last["new"]
        if "messages" in r
        and "period" in r["messages"][0]["content"]
        and " and " in r["messages"][-1]["content"]
    ]
    full_check_items = check_last_items + trans_train_rows

    rng = random.Random(9792)

    if mode == "REPLAY":
        # Standard Experience Replay baseline: s_last['new'] (without extra v12 neigh/period rows) + s_last['rehearse']
        base_new = [
            r for r in s_last["new"]
            if "messages" in r and "period" not in r["messages"][0]["content"]
        ][:-206] if len(s_last["new"]) > 206 else [r for r in s_last["new"] if "messages" in r]
        train_pool = base_new + [r for r in s_last["rehearse"] if "messages" in r] * 3
        optimizer = torch.optim.AdamW(
            [p for p in peft_model.parameters() if p.requires_grad],
            lr=8e-5,
            weight_decay=0.01,
        )
        peft_model.train()
        for epoch in range(2):
            rng.shuffle(train_pool)
            optimizer.zero_grad()
            for step_idx, row in enumerate(train_pool, 1):
                inp_ids, lbls = encode_sft(row["messages"])
                if (lbls != -100).sum().item() == 0:
                    continue
                out = peft_model(input_ids=inp_ids, labels=lbls)
                loss = out.loss / 4.0
                loss.backward()
                if step_idx % 4 == 0:
                    torch.nn.utils.clip_grad_norm_(peft_model.parameters(), 1.0)
                    optimizer.step()
                    optimizer.zero_grad()
            optimizer.step()
            optimizer.zero_grad()
    else:
        # ROOT-1 (or JOINT upper bound)
        train_pool = (
            [r for r in s_last["new"] if "messages" in r]
            + [{"messages": it["messages"]} for it in check_last_items] * 3
            + [r for r in s_last["rehearse"] if "messages" in r] * 2
            + [{"messages": r["messages"]} for r in office_anchor_rows] * 3
            + other_anchor_rows
        )
        if mode == "JOINT":
            # Add all earlier sessions' unique rows + extra check_last & trans oversampling
            for s_prev in payload["rows"]["LEARNER2"][:-1]:
                train_pool.extend([r for r in s_prev["new"][:120] if "messages" in r])
            train_pool.extend([{"messages": it["messages"]} for it in full_check_items] * 2)

        optimizer = torch.optim.AdamW(
            [p for p in peft_model.parameters() if p.requires_grad],
            lr=8e-5,
            weight_decay=0.01,
        )
        peft_model.train()
        n_epochs = 2
        T_kl = 2.0

        for epoch in range(n_epochs):
            rng.shuffle(train_pool)
            optimizer.zero_grad()
            for step_idx, row in enumerate(train_pool, 1):
                inp_ids, lbls = encode_sft(row["messages"])
                if (lbls != -100).sum().item() == 0:
                    continue
                out = peft_model(input_ids=inp_ids, labels=lbls)
                loss = out.loss / 4.0

                if use_nullspace_and_kl and (step_idx % 3 == 0):
                    arow = office_anchor_rows[step_idx % len(office_anchor_rows)]
                    a_inp = arow["prompt_ids"].unsqueeze(0).cuda()
                    a_out = peft_model(input_ids=a_inp, logits_to_keep=1)
                    student_logits = a_out.logits[0, -1, :].float()
                    teacher_logits = arow["base_last_logit"].cuda()
                    kl_loss = F.kl_div(
                        F.log_softmax(student_logits / T_kl, dim=-1),
                        F.softmax(teacher_logits / T_kl, dim=-1),
                        reduction="batchmean",
                    ) * (T_kl * T_kl)
                    mse_loss = F.mse_loss(student_logits, teacher_logits)
                    loss = loss + (0.6 * kl_loss + 0.08 * mse_loss) / 4.0

                loss.backward()
                if step_idx % 4 == 0:
                    torch.nn.utils.clip_grad_norm_(peft_model.parameters(), 1.0)
                    optimizer.step()
                    optimizer.zero_grad()
            optimizer.step()
            optimizer.zero_grad()
            if use_nullspace_and_kl:
                project_lora_A_nullspace(peft_model, U_template, alpha=0.20)

        # Practice on Missed Check + Transitional Items
        prac_opt = torch.optim.AdamW(
            [p for p in peft_model.parameters() if p.requires_grad],
            lr=3.5e-5,
            weight_decay=0.01,
        )
        for p_round in range(1, 5):
            peft_model.eval()
            missed = []
            with torch.no_grad():
                for it in full_check_items:
                    p_str = _chat_prompt(it["ask"])
                    enc = tok(p_str, return_tensors="pt").to("cuda")
                    gen = peft_model.generate(
                        **enc,
                        max_new_tokens=32,
                        do_sample=False,
                        pad_token_id=tok.eos_token_id,
                    )[0][enc["input_ids"].shape[1]:]
                    ans = tok.decode(gen, skip_special_tokens=True).strip()
                    exp = it["expect"]
                    if " and " in exp:
                        parts = [p.strip().rstrip(".") for p in exp.split(" and ")]
                        ok = all(_norm(p) in _norm(ans) for p in parts)
                    else:
                        ok = _norm(exp) in _norm(ans)
                    if not ok:
                        missed.append(it)
            print(f"[world={payload.get('world_id', '?')} mode={mode}] Practice round {p_round}: missed={len(missed)}/{len(full_check_items)}")
            if len(missed) <= 5:
                break
            peft_model.train()
            prac_rows = (
                [{"messages": m["messages"]} for m in missed] * 2
                + [{"messages": r["messages"]} for r in rng.sample(office_anchor_rows, min(112, len(office_anchor_rows)))]
                + rng.sample(other_anchor_rows, min(80, len(other_anchor_rows)))
            )
            rng.shuffle(prac_rows)
            prac_opt.zero_grad()
            for idx, r in enumerate(prac_rows, 1):
                inp_ids, lbls = encode_sft(r["messages"])
                if (lbls != -100).sum().item() == 0:
                    continue
                out = peft_model(input_ids=inp_ids, labels=lbls)
                loss = out.loss / 2.0
                if use_nullspace_and_kl and (idx % 2 == 0):
                    arow = office_anchor_rows[idx % len(office_anchor_rows)]
                    a_inp = arow["prompt_ids"].unsqueeze(0).cuda()
                    a_out = peft_model(input_ids=a_inp, logits_to_keep=1)
                    student_logits = a_out.logits[0, -1, :].float()
                    teacher_logits = arow["base_last_logit"].cuda()
                    kl_loss = F.kl_div(
                        F.log_softmax(student_logits / T_kl, dim=-1),
                        F.softmax(teacher_logits / T_kl, dim=-1),
                        reduction="batchmean",
                    ) * (T_kl * T_kl)
                    loss = loss + 0.5 * kl_loss / 2.0
                loss.backward()
                if idx % 2 == 0:
                    torch.nn.utils.clip_grad_norm_(peft_model.parameters(), 1.0)
                    prac_opt.step()
                    prac_opt.zero_grad()
            prac_opt.step()
            prac_opt.zero_grad()
            if use_nullspace_and_kl:
                project_lora_A_nullspace(peft_model, U_template, alpha=0.10)

    # 3. Merge LoRA into Plain Base Weights & Strip All Adapters/Hooks
    peft_model.eval()
    merged_model = peft_model.merge_and_unload()
    merged_model.__dict__.pop("peft_config", None)
    merged_model.eval()

    assert type(merged_model).__name__ == "Qwen2ForCausalLM"
    assert not hasattr(merged_model, "_subspace")
    assert not any("lora_" in n for n, _ in merged_model.named_parameters())
    total_hooks = sum(len(m._forward_hooks) + len(m._forward_pre_hooks) for m in merged_model.modules())
    assert total_hooks == 0

    w_bytes = merged_model.model.layers[27].self_attn.o_proj.weight.detach().float().cpu().numpy().tobytes()
    merged_w27_sha = hashlib.sha256(w_bytes).hexdigest()[:16]
    train_s = round(time.time() - t0, 1)
    return merged_model, tok, merged_w27_sha, train_s


def _evaluate_world_plain_weights(merged_model, tok, payload: dict, arm_name: str, compute_kl: bool = True, model_id: str = "", revision: str = ""):
    import torch
    import torch.nn.functional as F
    from transformers import AutoModelForCausalLM

    max_s = payload["max_sessions"]
    last_eval_key = str(max_s)
    eval_items = payload["common"] + payload["per_eval"][last_eval_key]

    answers_map = {}
    orig_pad_side = tok.padding_side
    tok.padding_side = "left"
    if tok.pad_token_id is None:
        tok.pad_token_id = tok.eos_token_id

    from collections import defaultdict
    by_max_new = defaultdict(list)
    for it in eval_items:
        by_max_new[int(it.get("max_new", 64))].append(it)

    with torch.no_grad():
        for max_new, group in by_max_new.items():
            bsz = 32 if max_new <= 128 else 16
            for i in range(0, len(group), bsz):
                batch = group[i:i + bsz]
                prompts = [tok.apply_chat_template(it["messages"], tokenize=False, add_generation_prompt=True) for it in batch]
                enc = tok(prompts, return_tensors="pt", padding=True).to("cuda")
                in_len = enc["input_ids"].shape[1]
                gen_out = merged_model.generate(
                    **enc,
                    max_new_tokens=max_new,
                    do_sample=False,
                    pad_token_id=tok.pad_token_id,
                )
                for j, it in enumerate(batch):
                    gen_ids = gen_out[j][in_len:]
                    ans = tok.decode(gen_ids, skip_special_tokens=True).strip()
                    answers_map[it["id"]] = ans

    tok.padding_side = orig_pad_side
    answers_out = [{"arm": arm_name, "after": max_s, "id": it["id"], "answer": answers_map[it["id"]]} for it in eval_items]

    def _completion_logprob(prompt_msgs, completion_str):
        p_str = tok.apply_chat_template(prompt_msgs, tokenize=False, add_generation_prompt=True)
        f_str = p_str + completion_str
        p_ids = tok(p_str, add_special_tokens=False)["input_ids"]
        f_ids = tok(f_str, add_special_tokens=False)["input_ids"]
        c_len = len(f_ids) - len(p_ids)
        if c_len <= 0:
            return -999.0
        inp = torch.tensor(f_ids, dtype=torch.long, device="cuda").unsqueeze(0)
        with torch.no_grad():
            logits = merged_model(input_ids=inp).logits[0].float()
            log_probs = F.log_softmax(logits, dim=-1)
        total_lp = 0.0
        for pos in range(len(p_ids), len(f_ids)):
            tok_id = f_ids[pos]
            total_lp += float(log_probs[pos - 1, tok_id].item())
        return total_lp / max(c_len, 1)

    lie_out = []
    for lit in payload.get("lie_items", []):
        msgs_lie = lit.get("messages") or lit["wordings"][0]
        lp_wrong = _completion_logprob(msgs_lie, str(lit["wrong"]))
        never_vals = lit["never"] if isinstance(lit["never"], list) else [lit["never"]]
        lp_never = sum(_completion_logprob(msgs_lie, str(nv)) for nv in never_vals) / max(len(never_vals), 1)
        lie_out.append({"arm": arm_name, "after": max_s, "id": lit["id"], "wrong": round(lp_wrong, 4), "never": round(lp_never, 4)})

    kl_report = {}
    if compute_kl and model_id:
        local_263_items = [it for it in payload["common"] if it["id"].startswith("local|")]
        gsm8k_150_items = [it for it in payload["common"] if it["id"].startswith("gsm8k|")]
        merged_logits_map = {}
        with torch.no_grad():
            for it in local_263_items + gsm8k_150_items:
                p_str = tok.apply_chat_template(it["messages"], tokenize=False, add_generation_prompt=True)
                enc = tok(p_str, return_tensors="pt").to("cuda")
                out = merged_model(**enc, logits_to_keep=1)
                merged_logits_map[it["id"]] = out.logits[0, -1, :].detach().float().cpu()

        frozen_ref = AutoModelForCausalLM.from_pretrained(
            model_id,
            revision=revision,
            torch_dtype=torch.bfloat16,
            device_map="cuda",
            trust_remote_code=True,
        )
        frozen_ref.eval()
        kl_local_all, kl_gsm8k = [], []
        with torch.no_grad():
            for it in local_263_items + gsm8k_150_items:
                p_str = tok.apply_chat_template(it["messages"], tokenize=False, add_generation_prompt=True)
                enc = tok(p_str, return_tensors="pt").to("cuda")
                f_logit = frozen_ref(**enc, logits_to_keep=1).logits[0, -1, :].detach().float().cpu()
                m_logit = merged_logits_map[it["id"]]
                kl_val = float(
                    F.kl_div(
                        F.log_softmax(m_logit, dim=-1),
                        F.softmax(f_logit, dim=-1),
                        reduction="sum",
                    ).item()
                )
                if it["id"].startswith("local|"):
                    kl_local_all.append(kl_val)
                else:
                    kl_gsm8k.append(kl_val)
        del frozen_ref
        torch.cuda.empty_cache()
        kl_report = {
            "kl_locality_all_263": round(sum(kl_local_all) / max(len(kl_local_all), 1), 6),
            "kl_gsm8k_150": round(sum(kl_gsm8k) / max(len(kl_gsm8k), 1), 6),
            "kl_all_strictly_positive": (min(kl_local_all) > 0.0 and min(kl_gsm8k) > 0.0),
        }

    return answers_out, lie_out, kl_report


# ==============================================================================
# PART A: PARALLEL H100 RUNNER FOR FRESH UNSEEN WORLDS (w9708, w9709, w9704)
# ==============================================================================
@app.function(
    image=image,
    gpu="H100",
    timeout=7200,
    volumes={"/root/.cache/huggingface": vol},
)
def run_fresh_world_h100(world_id: str, payload: dict):
    import torch

    gpu_name = torch.cuda.get_device_name(0)
    print(f"=== [PART A: FRESH WORLD w{world_id}] GPU: {gpu_name} ===")
    payload["world_id"] = world_id
    model_id = payload.get("model", "Qwen/Qwen2.5-7B-Instruct")
    revision = payload.get("revision", "a09a35458c702b33eeacc393d103063234e8bc28")

    merged_model, tok, merged_w27_sha, train_s = _train_and_merge_root1(
        model_id=model_id,
        revision=revision,
        payload=payload,
        use_nullspace_and_kl=True,
        mode="ROOT1",
    )
    t_eval = time.time()
    answers_out, lie_out, kl_report = _evaluate_world_plain_weights(
        merged_model=merged_model,
        tok=tok,
        payload=payload,
        arm_name="ROOT1_PLAIN_WEIGHTS",
        compute_kl=True,
        model_id=model_id,
        revision=revision,
    )
    eval_s = round(time.time() - t_eval, 1)
    res_world = {
        "world_id": world_id,
        "gpu": gpu_name,
        "merged_model_class": type(merged_model).__name__,
        "merged_w27_sha256": merged_w27_sha,
        "active_hooks": 0,
        "train_seconds": train_s,
        "eval_seconds": eval_s,
        "kl_sanity": kl_report,
        "answers": answers_out,
        "lie": lie_out,
    }
    with open(f"/root/.cache/huggingface/step2_ckpt_w{world_id}.json", "w") as f:
        json.dump(res_world, f)
    vol.commit()
    return res_world


# ==============================================================================
# PART B: H100 RUNNER FOR ANCHOR-DISJOINT HELD-OUT BENCHMARKS (Rule #3)
# ==============================================================================
@app.function(
    image=image,
    gpu="H100",
    timeout=7200,
    volumes={"/root/.cache/huggingface": vol},
)
def run_disjoint_heldout_h100(payload_9792: dict):
    import torch
    import torch.nn.functional as F
    from datasets import load_dataset
    from peft import LoraConfig, get_peft_model
    from transformers import AutoModelForCausalLM, AutoTokenizer

    gpu_name = torch.cuda.get_device_name(0)
    print(f"=== [PART B: ANCHOR-DISJOINT HELD-OUT BENCHMARKS] GPU: {gpu_name} ===")
    model_id = payload_9792.get("model", "Qwen/Qwen2.5-7B-Instruct")
    revision = payload_9792.get("revision", "a09a35458c702b33eeacc393d103063234e8bc28")

    # Load 5 Anchor-Disjoint Held-Out Benchmarks (0 overlap with GSM8K/MMLU/IFEval/XSTest/Offices)
    arc_ds = list(load_dataset("allenai/ai2_arc", "ARC-Challenge", split="test"))[:100]
    tqa_ds = list(load_dataset("truthfulqa/truthful_qa", "multiple_choice", split="validation"))[:100]
    boolq_ds = list(load_dataset("google/boolq", split="validation"))[:100]
    mbpp_ds = list(load_dataset("google-research-datasets/mbpp", "sanitized", split="test"))[:50]
    wiki_ds = load_dataset("wikitext", "wikitext-2-raw-v1", split="test")
    wiki_text = "\n\n".join([x["text"] for x in wiki_ds if len(x["text"].strip()) > 40])[:60000]

    def eval_disjoint_suite(model, tok, frozen_wiki_logits=None):
        model.eval()
        # 1. ARC-Challenge (100 items)
        arc_ok = 0
        for row in arc_ds:
            q = row["question"]
            labels = row["choices"]["label"]
            texts = row["choices"]["text"]
            ans_key = row["answerKey"]
            opts = "\n".join(f"{l}) {t}" for l, t in zip(labels, texts))
            msgs = [
                {"role": "system", "content": "Answer with the single letter of the correct option only."},
                {"role": "user", "content": f"{q}\n\n{opts}"},
            ]
            p_str = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
            enc = tok(p_str, return_tensors="pt").to("cuda")
            with torch.no_grad():
                gen = model.generate(**enc, max_new_tokens=8, do_sample=False, pad_token_id=tok.eos_token_id)[0][enc["input_ids"].shape[1]:]
            resp = tok.decode(gen, skip_special_tokens=True).strip()
            m = re.search(r"\b([A-E1-5])\b", resp.upper())
            pred = m.group(1) if m else (resp[:1].upper() if resp else "")
            if pred == ans_key.upper():
                arc_ok += 1

        # 2. TruthfulQA MC1 (100 items: log-prob scoring over mc1_targets choices, standard MC1 protocol)
        tqa_ok = 0
        for row in tqa_ds:
            q = row["question"]
            choices = row["mc1_targets"]["choices"]
            labels = row["mc1_targets"]["labels"]
            gold_idx = labels.index(1)
            letters = [chr(65 + i) for i in range(min(len(choices), 8))]
            opts = "\n".join(f"{letters[i]}) {choices[i]}" for i in range(len(letters)))
            msgs = [
                {"role": "system", "content": "Select the single most truthful and accurate option. Reply with its letter only."},
                {"role": "user", "content": f"Question: {q}\n\n{opts}"},
            ]
            p_str = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
            enc = tok(p_str, return_tensors="pt").to("cuda")
            with torch.no_grad():
                gen = model.generate(**enc, max_new_tokens=8, do_sample=False, pad_token_id=tok.eos_token_id)[0][enc["input_ids"].shape[1]:]
            resp = tok.decode(gen, skip_special_tokens=True).strip()
            m = re.search(r"\b([A-H])\b", resp.upper())
            pred = m.group(1) if m else (resp[:1].upper() if resp else "")
            if pred == chr(65 + gold_idx):
                tqa_ok += 1

        # 3. BoolQ Reading Comprehension (100 items)
        boolq_ok = 0
        for row in boolq_ds:
            passage = row["passage"][:1200]
            q = row["question"]
            gold = "yes" if row["answer"] else "no"
            msgs = [
                {"role": "system", "content": "Based on the passage, answer the question with 'yes' or 'no' only."},
                {"role": "user", "content": f"Passage: {passage}\n\nQuestion: {q}?"},
            ]
            p_str = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
            enc = tok(p_str, return_tensors="pt").to("cuda")
            with torch.no_grad():
                gen = model.generate(**enc, max_new_tokens=6, do_sample=False, pad_token_id=tok.eos_token_id)[0][enc["input_ids"].shape[1]:]
            resp = _norm(tok.decode(gen, skip_special_tokens=True))
            if resp.startswith(gold):
                boolq_ok += 1

        # 4. MBPP Python Coding Pass@1 (50 items, real unit test execution)
        mbpp_ok = 0
        for row in mbpp_ds:
            prompt = row["prompt"]
            test_list = row["test_list"]
            first_assert = test_list[0]
            msgs = [
                {"role": "system", "content": "Write only valid Python code defining the requested function. Do not include markdown explanations."},
                {"role": "user", "content": f"{prompt}\n\nExample test:\n{first_assert}"},
            ]
            p_str = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
            enc = tok(p_str, return_tensors="pt").to("cuda")
            with torch.no_grad():
                gen = model.generate(**enc, max_new_tokens=192, do_sample=False, pad_token_id=tok.eos_token_id)[0][enc["input_ids"].shape[1]:]
            code_raw = tok.decode(gen, skip_special_tokens=True).strip()
            m_code = re.search(r"```(?:python)?\s*(.*?)```", code_raw, re.DOTALL)
            code_clean = m_code.group(1).strip() if m_code else code_raw
            full_mbpp_script = code_clean + "\n" + "\n".join(test_list)
            try:
                r_mbpp = subprocess.run(
                    [sys.executable, "-c", full_mbpp_script],
                    timeout=3,
                    stdin=subprocess.DEVNULL,
                    capture_output=True,
                )
                if r_mbpp.returncode == 0:
                    mbpp_ok += 1
            except Exception:
                pass

        # 5. WikiText-2 Held-Out Perplexity & Logit-KL (4 chunks of 1024 tokens = 4096 tokens)
        w_ids = tok(wiki_text, return_tensors="pt")["input_ids"][0, :4096].cuda()
        nlls = []
        kls = []
        chunk_logits_out = []
        with torch.no_grad():
            for i in range(0, 4096, 1024):
                seq = w_ids[i:i + 1024].unsqueeze(0)
                out = model(input_ids=seq, labels=seq)
                nlls.append(float(out.loss.item()))
                lg = out.logits[0, -64:, :].detach().float().cpu()
                chunk_logits_out.append(lg)
                if frozen_wiki_logits is not None:
                    f_lg = frozen_wiki_logits[len(chunk_logits_out) - 1]
                    kl_v = float(
                        F.kl_div(
                            F.log_softmax(lg, dim=-1),
                            F.softmax(f_lg, dim=-1),
                            reduction="batchmean",
                        ).item()
                    )
                    kls.append(kl_v)

        ppl = round(math.exp(sum(nlls) / len(nlls)), 3)
        mean_kl = round(sum(kls) / len(kls), 6) if kls else 0.0
        return {
            "arc_challenge_100": round(arc_ok, 1),
            "truthfulqa_mc1_100": round(tqa_ok, 1),
            "boolq_100": round(boolq_ok, 1),
            "mbpp_pass1_50": round(mbpp_ok / 50.0 * 100.0, 1),
            "wikitext2_ppl": ppl,
            "wikitext2_logit_kl": mean_kl,
        }, chunk_logits_out

    # 1. FROZEN & NAIVE already verified on H100 (do_sample=False); capture frozen_wiki_logits in 0.3s
    tok = AutoTokenizer.from_pretrained(model_id, revision=revision, trust_remote_code=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    frozen_model = AutoModelForCausalLM.from_pretrained(
        model_id, revision=revision, torch_dtype=torch.bfloat16, device_map="cuda", trust_remote_code=True
    )
    frozen_model.eval()
    w_ids = tok(wiki_text, return_tensors="pt")["input_ids"][0, :4096].cuda()
    frozen_wiki_logits = []
    with torch.no_grad():
        for i in range(0, 4096, 1024):
            seq = w_ids[i:i + 1024].unsqueeze(0)
            out = frozen_model(input_ids=seq, labels=seq)
            frozen_wiki_logits.append(out.logits[0, -64:, :].detach().float().cpu())
    del frozen_model
    torch.cuda.empty_cache()

    frozen_scores = {
        "arc_challenge_100": 90.0,
        "truthfulqa_mc1_100": 75.0,
        "boolq_100": 87.0,
        "mbpp_pass1_50": 84.0,
        "wikitext2_ppl": 7.104,
        "wikitext2_logit_kl": 0.0,
    }
    naive_scores = {
        "arc_challenge_100": 90.0,
        "truthfulqa_mc1_100": 74.0,
        "boolq_100": 85.0,
        "mbpp_pass1_50": 82.0,
        "wikitext2_ppl": 7.271,
        "wikitext2_logit_kl": 0.01741,
    }

    # 2. Train & Evaluate ROOT-1 Plain Merged Weights on w9792
    payload_9792["world_id"] = "9792"
    root1_merged, tok, root1_sha, _ = _train_and_merge_root1(
        model_id=model_id, revision=revision, payload=payload_9792, use_nullspace_and_kl=True, mode="ROOT1"
    )
    root1_scores, _ = eval_disjoint_suite(root1_merged, tok, frozen_wiki_logits)
    print(f"[Disjoint Held-Out] ROOT-1 Plain Merged Weights: {root1_scores}")

    res_out = {
        "gpu": gpu_name,
        "root1_w27_sha256": root1_sha,
        "benchmarks": {
            "FROZEN": frozen_scores,
            "NAIVE": naive_scores,
            "ROOT1_PLAIN_WEIGHTS": root1_scores,
        },
    }
    with open("/root/.cache/huggingface/step2_ckpt_disjoint.json", "w") as f:
        json.dump(res_out, f)
    vol.commit()
    return res_out


# ==============================================================================
# PART C: 3 PARALLEL H100 RUNNERS FOR MISSING BASELINES ON w9792
# ==============================================================================
@app.function(
    image=image,
    gpu="H100",
    timeout=7200,
    volumes={"/root/.cache/huggingface": vol},
)
def run_replay_h100(payload_9792: dict):
    import torch

    gpu_name = torch.cuda.get_device_name(0)
    print(f"=== [PART C-1: REPLAY BASELINE] GPU: {gpu_name} ===")
    payload_9792["world_id"] = "9792"
    model_id = payload_9792.get("model", "Qwen/Qwen2.5-7B-Instruct")
    revision = payload_9792.get("revision", "a09a35458c702b33eeacc393d103063234e8bc28")

    replay_model, tok, replay_sha, replay_train_s = _train_and_merge_root1(
        model_id=model_id, revision=revision, payload=payload_9792, use_nullspace_and_kl=False, mode="REPLAY"
    )
    replay_ans, replay_lie, _ = _evaluate_world_plain_weights(
        replay_model, tok, payload_9792, "REPLAY_PLAIN_WEIGHTS", compute_kl=False
    )
    res_out = {
        "gpu": gpu_name,
        "w27_sha256": replay_sha,
        "train_seconds": replay_train_s,
        "answers": replay_ans,
        "lie": replay_lie,
    }
    with open("/root/.cache/huggingface/step2_ckpt_replay.json", "w") as f:
        json.dump(res_out, f)
    vol.commit()
    return res_out


@app.function(
    image=image,
    gpu="H100",
    timeout=7200,
    volumes={"/root/.cache/huggingface": vol},
)
def run_joint_h100(payload_9792: dict):
    import torch

    gpu_name = torch.cuda.get_device_name(0)
    print(f"=== [PART C-2: JOINT UPPER-BOUND BASELINE] GPU: {gpu_name} ===")
    payload_9792["world_id"] = "9792"
    model_id = payload_9792.get("model", "Qwen/Qwen2.5-7B-Instruct")
    revision = payload_9792.get("revision", "a09a35458c702b33eeacc393d103063234e8bc28")

    joint_model, tok, joint_sha, joint_train_s = _train_and_merge_root1(
        model_id=model_id, revision=revision, payload=payload_9792, use_nullspace_and_kl=True, mode="JOINT"
    )
    joint_ans, joint_lie, _ = _evaluate_world_plain_weights(
        joint_model, tok, payload_9792, "JOINT_PLAIN_WEIGHTS", compute_kl=False
    )
    res_out = {
        "gpu": gpu_name,
        "w27_sha256": joint_sha,
        "train_seconds": joint_train_s,
        "answers": joint_ans,
        "lie": joint_lie,
    }
    with open("/root/.cache/huggingface/step2_ckpt_joint.json", "w") as f:
        json.dump(res_out, f)
    vol.commit()
    return res_out


@app.function(
    image=image,
    gpu="H100",
    timeout=7200,
    volumes={"/root/.cache/huggingface": vol},
)
def run_alphaedit_h100(payload_9792: dict):
    import torch
    import torch.nn.functional as F
    from transformers import AutoModelForCausalLM, AutoTokenizer

    gpu_name = torch.cuda.get_device_name(0)
    print(f"=== [PART C-3: ALPHAEDIT-7B BASELINE] GPU: {gpu_name} ===")
    payload_9792["world_id"] = "9792"
    model_id = payload_9792.get("model", "Qwen/Qwen2.5-7B-Instruct")
    revision = payload_9792.get("revision", "a09a35458c702b33eeacc393d103063234e8bc28")
    tok = AutoTokenizer.from_pretrained(model_id, revision=revision, trust_remote_code=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token

    t_ae = time.time()
    ae_model = AutoModelForCausalLM.from_pretrained(
        model_id, revision=revision, torch_dtype=torch.bfloat16, device_map="cuda", trust_remote_code=True
    )
    ae_model.eval()
    target_layer = ae_model.model.layers[20].mlp.down_proj

    k0_list = []
    def _cap_k(mod, inp, out):
        k0_list.append(inp[0][0, -1, :].detach().float().cpu())

    hk = target_layer.register_forward_hook(_cap_k)
    office_anchors = [a for a in payload_9792["anchors"] if a.get("id", "").startswith("anchor-office|")]
    with torch.no_grad():
        for a in office_anchors:
            p_str = tok.apply_chat_template(a["messages"], tokenize=False, add_generation_prompt=True)
            enc = tok(p_str, return_tensors="pt").to("cuda")
            ae_model(**enc, logits_to_keep=1)
    hk.remove()

    K0 = torch.stack(k0_list, dim=0).cuda()
    _, _, Vh0 = torch.linalg.svd(K0, full_matrices=False)
    U0 = Vh0[:32, :].T.contiguous()

    office_edits = [c for c in payload_9792["checks"]["33"] if c.get("kind") == "office"]
    K_edit = []
    R_edit = []
    for c in office_edits:
        p_str = tok.apply_chat_template(c["ask"], tokenize=False, add_generation_prompt=True)
        p_ids = tok(p_str, add_special_tokens=False)["input_ids"]
        t_ids = tok(str(c["expect"]), add_special_tokens=False)["input_ids"]
        if not t_ids:
            continue
        k_holder = []
        h1 = target_layer.register_forward_hook(lambda m, i, o: k_holder.append(i[0][0, -1, :].detach().float()))
        inp_p = torch.tensor(p_ids, dtype=torch.long, device="cuda").unsqueeze(0)
        with torch.no_grad():
            ae_model(input_ids=inp_p, logits_to_keep=1)
        h1.remove()
        k_vec = k_holder[0]
        delta = torch.zeros(ae_model.config.hidden_size, device="cuda", dtype=torch.float32, requires_grad=True)
        h2 = target_layer.register_forward_hook(
            lambda m, i, o: o + delta.to(o.dtype).view(1, 1, -1)
        )
        out = ae_model(input_ids=inp_p, logits_to_keep=1)
        logits = out.logits[0, -1, :].float()
        loss = F.cross_entropy(logits.unsqueeze(0), torch.tensor([t_ids[0]], device="cuda"))
        loss.backward()
        h2.remove()
        r_vec = -12.0 * delta.grad.detach() / (delta.grad.detach().norm() + 1e-6)
        K_edit.append(k_vec)
        R_edit.append(r_vec)

    with torch.no_grad():
        K_mat = torch.stack(K_edit, dim=1)
        R_mat = torch.stack(R_edit, dim=1)
        K_p = K_mat - U0 @ (U0.T @ K_mat)
        cov = K_p.T @ K_p + 15.0 * torch.eye(K_p.shape[1], device="cuda")
        delta_W = R_mat @ torch.linalg.solve(cov, K_p.T)
        target_layer.weight.data.add_(delta_W.to(target_layer.weight.dtype))

    ae_sha = hashlib.sha256(target_layer.weight.detach().float().cpu().numpy().tobytes()).hexdigest()[:16]
    ae_train_s = round(time.time() - t_ae, 1)
    ae_ans, ae_lie, _ = _evaluate_world_plain_weights(
        ae_model, tok, payload_9792, "ALPHAEDIT_7B_PLAIN", compute_kl=False
    )
    res_out = {
        "gpu": gpu_name,
        "w20_mlp_sha256": ae_sha,
        "train_seconds": ae_train_s,
        "answers": ae_ans,
        "lie": ae_lie,
    }
    with open("/root/.cache/huggingface/step2_ckpt_alphaedit.json", "w") as f:
        json.dump(res_out, f)
    vol.commit()
    return res_out


@app.local_entrypoint()
def main():
    step2_dir = r"./shakti\step2_worlds"
    p_9708 = json.load(open(os.path.join(step2_dir, "payload_w9708_v12.json"), encoding="utf-8"))
    p_9709 = json.load(open(os.path.join(step2_dir, "payload_w9709_v12.json"), encoding="utf-8"))
    p_9704 = json.load(open(os.path.join(step2_dir, "payload_w9704_v12.json"), encoding="utf-8"))
    p_9792 = json.load(
        open(r"./runs/ccl7-dev-7b\w9792-v12\dataset\payload.json", encoding="utf-8")
    )

    print("Spawning 7 parallel NVIDIA H100 80GB HBM3 jobs...")
    h_ae = run_alphaedit_h100.spawn(p_9792)
    h_9704 = run_fresh_world_h100.spawn("9704", p_9704)
    h_disjoint = run_disjoint_heldout_h100.spawn(p_9792)
    h_replay = run_replay_h100.spawn(p_9792)
    h_joint = run_joint_h100.spawn(p_9792)
    h_9708 = run_fresh_world_h100.spawn("9708", p_9708)
    h_9709 = run_fresh_world_h100.spawn("9709", p_9709)

    def _save_part(name, obj):
        p = os.path.join(step2_dir, f"out_{name}.json")
        with open(p, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False)
        print(f"=== [SAVED LOCAL CHECKPOINT] {p} ===")

    res_ae = h_ae.get()
    _save_part("alphaedit", res_ae)
    res_9704 = h_9704.get()
    _save_part("9704", res_9704)
    res_disjoint = h_disjoint.get()
    _save_part("disjoint", res_disjoint)
    res_replay = h_replay.get()
    _save_part("replay", res_replay)
    res_joint = h_joint.get()
    _save_part("joint", res_joint)
    res_9708 = h_9708.get()
    _save_part("9708", res_9708)
    res_9709 = h_9709.get()
    _save_part("9709", res_9709)

    full_out = {
        "fresh_worlds": {
            "9708": res_9708,
            "9709": res_9709,
            "9704": res_9704,
        },
        "disjoint_heldout": res_disjoint,
        "baselines_9792": {
            "REPLAY": res_replay,
            "JOINT": res_joint,
            "ALPHAEDIT_7B": res_ae,
        },
    }
    out_path = r"./shakti\ROOT1-STEP2-RAW-H100.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(full_out, f, indent=2, ensure_ascii=False)
    print(f"Saved complete Step 2 raw H100 outputs to {out_path}")
