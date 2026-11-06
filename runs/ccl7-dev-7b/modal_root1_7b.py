"""Modal H100 GPU Runner for ROOT-1 Plain Merged Weights on Qwen/Qwen2.5-7B-Instruct (w9792).

What this script does on a real NVIDIA H100-80GB GPU:
1. Loads Qwen/Qwen2.5-7B-Instruct (revision bb46c15ee4bb56c5b63245ef50fd7637234d6f75) in bfloat16.
2. Computes the Shared Office-Template Principal Subspace U_rel^(l) from the 206 disjoint
   anchor-office prompts (0% overlap with the 80 locality_own or 263 locality test offices).
3. Trains the continual learner with:
   - Template Null-Space Projection on lora_A: A_l <- A_l - alpha * (A_l @ U_rel) @ U_rel^T
   - Full-Vocabulary Logit-MSE + KL Distillation on the 206 disjoint anchor-office & general anchors
     (preventing synthetic-name logit inflation on unseen offices!)
   - Stratified anchor rehearsal inside practice() rounds (fixing kernel_v12.py's anchor_rows[:8] bug).
4. Calls `merged_model = peft_model.merge_and_unload()` to produce a 100% PLAIN Qwen2ForCausalLM
   with ZERO PeftModel, ZERO _subspace, ZERO hooks, ZERO routers, ZERO disable_adapter().
5. Evaluates `merged_model` on all 2,323 Session-34 evaluation prompts + 40 lie_items + Logit KL.
"""
import gzip
import hashlib
import json
import os
import random
import time
import modal

app = modal.App("shakti-root1-plain-weights-7b")

image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "torch==2.5.1",
        "transformers==4.47.1",
        "peft==0.13.2",
        "accelerate==1.1.1",
        "safetensors",
        "huggingface_hub",
    )
)

vol = modal.Volume.from_name("shakti-hf-cache", create_if_missing=True)


@app.function(
    image=image,
    gpu="H100",
    timeout=3600,
    volumes={"/root/.cache/huggingface": vol},
)
def run_root1_plain_weights_h100(bundle_gz: bytes) -> bytes:
    import torch
    import torch.nn.functional as F
    from peft import LoraConfig, get_peft_model
    from transformers import AutoModelForCausalLM, AutoTokenizer

    t0 = time.time()
    bundle = json.loads(gzip.decompress(bundle_gz).decode("utf-8"))
    P = bundle["payload"]
    anchor_answers = bundle["anchor_answers"]
    own_80_ids = set(bundle["own_80_ids"])

    print(f"[H100] Unpacked payload in {time.time()-t0:.1f}s. GPU: {torch.cuda.get_device_name(0)}", flush=True)

    tok = AutoTokenizer.from_pretrained(P["model"], revision=P["revision"])
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token

    base = AutoModelForCausalLM.from_pretrained(
        P["model"],
        revision=P["revision"],
        torch_dtype=torch.bfloat16,
        device_map="cuda:0",
        attn_implementation="sdpa",
    )
    base.eval()
    device = next(base.parameters()).device
    print(f"[H100] Loaded {P['model']} in bfloat16 ({time.time()-t0:.1f}s)", flush=True)

    def norm(text):
        return " ".join("".join(c.lower() if c.isalnum() else " " for c in text).split())

    def encode(messages):
        full = tok.apply_chat_template(messages, tokenize=True)
        if not isinstance(full, list):
            full = list(full["input_ids"]) if "input_ids" in full else list(full)
        prompt = tok.apply_chat_template(messages[:-1], tokenize=True, add_generation_prompt=True)
        if not isinstance(prompt, list):
            prompt = list(prompt["input_ids"]) if "input_ids" in prompt else list(prompt)
        return full, [-100] * len(prompt) + full[len(prompt):]

    def answer_batch(model, conversations, max_new, batch_size=64):
        tok.padding_side = "left"
        out = []
        for i in range(0, len(conversations), batch_size):
            prompts = [
                tok.apply_chat_template(m, tokenize=False, add_generation_prompt=True)
                for m in conversations[i : i + batch_size]
            ]
            enc = tok(prompts, return_tensors="pt", padding=True, add_special_tokens=False).to(device)
            with torch.no_grad():
                gen = model.generate(
                    **enc,
                    max_new_tokens=max_new,
                    do_sample=False,
                    pad_token_id=tok.pad_token_id,
                )
            for r in gen[:, enc["input_ids"].shape[1] :]:
                out.append(tok.decode(r, skip_special_tokens=True).strip())
        return out

    def answers_for_plain(model, items):
        # Strictly plain inference: NO _subspace, NO disable_adapter(), NO hooks!
        assert not hasattr(model, "_subspace") or getattr(model, "_subspace") is None
        got = {}
        for max_new in sorted({it["max_new"] for it in items}):
            idx = [i for i, it in enumerate(items) if it["max_new"] == max_new]
            bsize = 32 if max_new > 64 else 64
            ans_list = answer_batch(model, [items[i]["messages"] for i in idx], max_new, bsize)
            for i, a in zip(idx, ans_list):
                got[items[i]["id"]] = a
        return got

    # Prepare anchor rows by domain so we can stratify rehearsal and compute template subspace
    anchor_row_map = {
        a["id"]: {"id": a["id"], "messages": a["messages"] + [{"role": "assistant", "content": anchor_answers[a["id"]]}]}
        for a in P["anchors"]
        if a["id"] in anchor_answers
    }
    spec = P["arms"][0]
    all_anchor_rows = [anchor_row_map[i] for i in spec.get("anchors", []) if i in anchor_row_map]
    office_anchor_rows = [r for r in all_anchor_rows if r["id"].startswith("anchor-office")]
    other_anchor_rows = [r for r in all_anchor_rows if not r["id"].startswith("anchor-office")]

    print(f"[H100] Anchors ready: total={len(all_anchor_rows)}, office={len(office_anchor_rows)}, other={len(other_anchor_rows)}", flush=True)

    # Step 1: Collect Shared Office-Template Subspace U_rel^(l) from the 206 disjoint anchor-office prompts
    target_mod_names = ["q_proj", "k_proj", "v_proj", "o_proj"]
    office_acts = {f"{l}.{m}": [] for l in range(len(base.model.layers)) for m in target_mod_names}
    hooks = []
    for l, layer_obj in enumerate(base.model.layers):
        for m in target_mod_names:
            mod = getattr(layer_obj.self_attn, m)
            key = f"{l}.{m}"
            def make_hook(k):
                def fn(module, inp, out):
                    x = inp[0].detach().float()  # (B, T, d)
                    # Capture question-end / template tokens (last 4 tokens of prompt + answer)
                    office_acts[k].append(x[:, -4:, :].reshape(-1, x.shape[-1]).cpu())
                return fn
            hooks.append(mod.register_forward_hook(make_hook(key)))

    tok.padding_side = "left"
    with torch.no_grad():
        for i in range(0, len(office_anchor_rows), 32):
            batch = office_anchor_rows[i : i + 32]
            prompts = [tok.apply_chat_template(r["messages"][:-1], tokenize=False, add_generation_prompt=True) for r in batch]
            enc = tok(prompts, return_tensors="pt", padding=True, add_special_tokens=False).to(device)
            base(**enc)

    for h in hooks:
        h.remove()

    U_template = {}
    for key, tensor_list in office_acts.items():
        X = torch.cat(tensor_list, dim=0).to(device)  # (~824, d_in)
        # Extract top-6 principal directions of the shared office-question template
        _, S, Vh = torch.linalg.svd(X, full_matrices=False)
        U_template[key] = Vh[:6, :].T.contiguous()  # (d_in, 6)
    del office_acts
    torch.cuda.empty_cache()
    print(f"[H100] Computed U_template (top-6) basis for {len(U_template)} modules ({time.time()-t0:.1f}s)", flush=True)

    # Also pre-cache frozen last-token logits on the 206 disjoint office_anchor_rows for fast Logit-MSE + KL distillation!
    office_anchor_prompts = [
        tok.apply_chat_template(r["messages"][:-1], tokenize=True, add_generation_prompt=True)
        for r in office_anchor_rows
    ]
    office_anchor_prompts = [
        list(p["input_ids"]) if not isinstance(p, list) and "input_ids" in p else list(p)
        for p in office_anchor_prompts
    ]
    frozen_office_logits = []
    with torch.no_grad():
        for i in range(0, len(office_anchor_prompts), 16):
            batch_p = office_anchor_prompts[i : i + 16]
            w = max(len(x) for x in batch_p)
            ids = torch.tensor([[tok.pad_token_id] * (w - len(x)) + x for x in batch_p], device=device)
            msk = torch.tensor([[0] * (w - len(x)) + [1] * len(x) for x in batch_p], device=device)
            lg = base(input_ids=ids, attention_mask=msk).logits[:, -1, :].detach().to(torch.float16).cpu()
            frozen_office_logits.append((ids.cpu(), msk.cpu(), lg))

    # Pre-cache frozen last-token logits on local_items and gsm_items for the ROOT-1 Logit KL sanity check
    eval_34_items = P["common"] + P["per_eval"]["34"]
    local_eval_items = [it for it in eval_34_items if it["id"].startswith("local|")]
    own80_eval_items = [it for it in local_eval_items if it["id"] in own_80_ids]
    gsm_eval_items = [it for it in eval_34_items if it["id"].startswith("gsm8k|")]

    def get_last_logprobs(model, item_list):
        tok.padding_side = "left"
        lps = []
        for i in range(0, len(item_list), 32):
            batch = item_list[i : i + 32]
            prompts = [tok.apply_chat_template(it["messages"], tokenize=False, add_generation_prompt=True) for it in batch]
            enc = tok(prompts, return_tensors="pt", padding=True, add_special_tokens=False).to(device)
            with torch.no_grad():
                lg = model(**enc).logits[:, -1, :].float()
                lps.append(torch.log_softmax(lg, dim=-1).cpu())
        return torch.cat(lps, dim=0)

    frozen_lp_own80 = get_last_logprobs(base, own80_eval_items)
    frozen_lp_local = get_last_logprobs(base, local_eval_items)
    frozen_lp_gsm = get_last_logprobs(base, gsm_eval_items)

    # Step 2: Build PeftModel (r=32, alpha=64) and train on the full Session-34 cumulative knowledge + stratified anchors
    peft_model = get_peft_model(
        base,
        LoraConfig(
            r=32,
            lora_alpha=64,
            lora_dropout=0.05,
            target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
            task_type="CAUSAL_LM",
        ),
    )
    for p in peft_model.parameters():
        if p.requires_grad:
            p.data = p.data.float()

    # Map each lora_A parameter to its U_template matrix for fast orthogonal projection
    lora_A_projections = []
    for l, layer_obj in enumerate(peft_model.base_model.model.model.layers):
        for m in target_mod_names:
            mod = getattr(layer_obj.self_attn, m)
            if hasattr(mod, "lora_A") and "default" in mod.lora_A:
                A_weight = mod.lora_A["default"].weight  # (r, d_in)
                U_mat = U_template[f"{l}.{m}"]  # (d_in, 6)
                lora_A_projections.append((A_weight, U_mat))

    def project_lora_A_nullspace(alpha=0.25):
        with torch.no_grad():
            for A_w, U_m in lora_A_projections:
                # Project out shared template components from lora_A row-space once per epoch
                A_w.sub_(alpha * (A_w @ U_m) @ U_m.T)

    # Assemble all valid Session-34 taught rows (with Session-4 retracted errors removed!)
    u3 = P["undo"]["3"]
    forgotten_marks = [tuple(m) for m in u3["marks"]]

    def forget_rows(rows, marks):
        if not marks:
            return rows
        return [
            x
            for x in rows
            if not any(
                w in x["messages"][-2]["content"] + " " + x["messages"][-1]["content"]
                and pl in x["messages"][-2]["content"] + " " + x["messages"][-1]["content"]
                for w, pl in marks
            )
        ]

    # Collect cumulative taught rows across sessions + Session 34 active state + lessons
    s33 = P["rows"]["LEARNER2"]["33"]
    s33_clean_new = forget_rows(list(s33["new"]), forgotten_marks)
    check33_items = P["checks"]["33"]

    # Build balanced check items: check33_items (442) + 174 transitional rows ("<OLD> and <NEW>") from s33_clean_new
    seen_chk_qs = {it["ask"][-1]["content"] for it in check33_items}
    full_check_items = list(check33_items)
    for r in s33_clean_new:
        q_txt = r["messages"][-2]["content"]
        a_txt = r["messages"][-1]["content"]
        if q_txt.startswith("Name everyone who served as ") and q_txt not in seen_chk_qs:
            seen_chk_qs.add(q_txt)
            full_check_items.append({"ask": r["messages"][:-1], "expect": a_txt.rstrip("."), "row": r})

    # Oversample check33_items 3x in main training so <NEW_HOLDER> always dominates undated "Who is the <role> of <X>?"
    taught_rows = (
        s33_clean_new
        + [it["row"] for it in s33["rehearse"]]
        + [it["row"] for it in check33_items] * 3
    )
    for pat, lesson_rows in P.get("lessons", {}).items():
        taught_rows += lesson_rows * 2
    taught_rows = forget_rows(taught_rows, forgotten_marks)

    # Balance taught rows with stratified anchor rows (oversampling office_anchor_rows 2x to prevent template bias!)
    anchor_train_rows = (
        [{"messages": r["messages"]} for r in office_anchor_rows] * 2
        + [{"messages": r["messages"]} for r in other_anchor_rows]
    )

    all_train_rows = taught_rows + anchor_train_rows
    print(f"[H100] Training rows assembled: taught={len(taught_rows)}, anchor_balanced={len(anchor_train_rows)}, full_checks={len(full_check_items)}", flush=True)

    def train_pass(rows_to_train, epochs, lr, seed, distill_office_kl=True, null_alpha=0.25):
        data = [encode(r["messages"]) for r in rows_to_train]
        opt = torch.optim.AdamW([p for p in peft_model.parameters() if p.requires_grad], lr=lr, weight_decay=1e-4)
        rng = random.Random(seed)
        tok.padding_side = "right"
        peft_model.train()
        kl_idx = 0
        for ep in range(epochs):
            order = list(range(len(data)))
            rng.shuffle(order)
            total_loss = 0.0
            steps = 0
            for i in range(0, len(order), 16):
                whole = [data[j] for j in order[i : i + 16]]
                opt.zero_grad()
                # Microbatch of 8 to keep peak VRAM < 25GB on H100
                for mb in range(0, len(whole), 8):
                    batch = whole[mb : mb + 8]
                    width = max(len(x) for x, _ in batch)
                    ids = torch.tensor([x + [tok.pad_token_id] * (width - len(x)) for x, _ in batch], device=device)
                    labels = torch.tensor([y + [-100] * (width - len(y)) for _, y in batch], device=device)
                    mask = torch.tensor([[1] * len(x) + [0] * (width - len(x)) for x, _ in batch], device=device)
                    with torch.autocast("cuda", dtype=torch.bfloat16):
                        ce_loss = peft_model(
                            input_ids=ids, attention_mask=mask, labels=labels, use_cache=False
                        ).loss * (len(batch) / len(whole))
                    ce_loss.backward()
                    total_loss += float(ce_loss.detach())

                # Every 3rd step, enforce Full-Distribution Logit-MSE + KL on a batch of disjoint office anchors
                # AFTER freeing the CE graph, and using logits_to_keep=1!
                if distill_office_kl and (steps % 3 == 0):
                    a_ids, a_msk, a_ref_lg = frozen_office_logits[kl_idx % len(frozen_office_logits)]
                    kl_idx += 1
                    a_ids = a_ids.to(device)
                    a_msk = a_msk.to(device)
                    a_ref = a_ref_lg.to(device, dtype=torch.float32)
                    with torch.autocast("cuda", dtype=torch.bfloat16):
                        out_kl = peft_model(
                            input_ids=a_ids, attention_mask=a_msk, use_cache=False, logits_to_keep=1
                        )
                        cur_lg = out_kl.logits[:, -1, :].float()
                        T = 2.0
                        kl_loss = F.kl_div(
                            F.log_softmax(cur_lg / T, dim=-1),
                            F.softmax(a_ref / T, dim=-1),
                            reduction="batchmean",
                        ) * (T * T)
                        mse_loss = F.mse_loss(cur_lg, a_ref)
                        reg_loss = 0.45 * kl_loss + 0.04 * mse_loss
                    reg_loss.backward()

                torch.nn.utils.clip_grad_norm_(peft_model.parameters(), 1.0)
                opt.step()
                steps += 1
            if null_alpha > 0:
                project_lora_A_nullspace(alpha=null_alpha)
            print(f"  [Train] ep={ep+1}/{epochs} steps={steps} mean_ce={total_loss/max(steps,1):.4f} ({time.time()-t0:.1f}s)", flush=True)
        peft_model.eval()

    # Main training pass (3 epochs with Logit-KL + Per-Epoch Template-Null Projection)
    train_pass(all_train_rows, epochs=3, lr=1.5e-4, seed=9792, distill_office_kl=True, null_alpha=0.20)

    # Practice rounds on full_check_items (check33_items + 174 balanced transitional rows) + stratified anchors!
    rng_prac = random.Random(9999)
    for r in range(3):
        peft_model.eval()
        got_chk = answer_batch(peft_model, [it["ask"] for it in full_check_items], 24, 96)
        miss_flags = [norm(it["expect"]) not in norm(a) for it, a in zip(full_check_items, got_chk)]
        missed = [it for it, m in zip(full_check_items, miss_flags) if m]
        print(f"  [Practice {r+1}] checked={len(full_check_items)} missed={len(missed)} ({time.time()-t0:.1f}s)", flush=True)
        if not missed or r == 2:
            break
        held = [it["row"] for it, m in zip(full_check_items, miss_flags) if not m]
        mix = rng_prac.sample(held, min(len(held), max(150, 2 * len(missed)), 350))
        prac_anchors = (
            [{"messages": x["messages"]} for x in rng_prac.sample(office_anchor_rows, min(112, len(office_anchor_rows)))]
            + [{"messages": x["messages"]} for x in rng_prac.sample(other_anchor_rows, min(80, len(other_anchor_rows)))]
        )
        prac_rows = forget_rows([it["row"] for it in missed for _ in range(4)] + mix + prac_anchors, forgotten_marks)
        train_pass(prac_rows, epochs=2, lr=6e-5, seed=8000 + r, distill_office_kl=True, null_alpha=0.10)

    # Step 3: MERGE 100% INTO PLAIN WEIGHTS (merge_and_unload)!
    print("[H100] Merging adapter into plain Qwen2ForCausalLM weights (merge_and_unload)...", flush=True)
    merged_model = peft_model.merge_and_unload()
    merged_model.__dict__.pop("peft_config", None)
    merged_model.eval()

    # Strict ROOT-1 Plain-Weights Assertions
    assert type(merged_model).__name__ == "Qwen2ForCausalLM", f"Expected Qwen2ForCausalLM, got {type(merged_model).__name__}"
    assert not any("lora_" in n for n, _ in merged_model.named_parameters()), "LoRA params still present!"
    assert not hasattr(merged_model, "_subspace") or getattr(merged_model, "_subspace") is None, "_subspace present!"
    total_hooks = sum(len(m._forward_hooks) + len(m._forward_pre_hooks) for m in merged_model.modules())
    assert total_hooks == 0, f"Found {total_hooks} hooks on merged_model!"

    # Compute cryptographic SHA-256 fingerprint of merged layer 27 weights
    w_bytes = merged_model.model.layers[-1].self_attn.o_proj.weight.detach().float().cpu().numpy().tobytes()
    weights_sha256 = hashlib.sha256(w_bytes).hexdigest()
    print(f"[H100] Plain Qwen2ForCausalLM verified! 0 hooks, 0 routers. Layer-27 o_proj SHA256: {weights_sha256[:16]}", flush=True)

    # Step 4: Evaluate Plain Merged Model on ALL 2,323 Session-34 questions + 40 lie_items + Logit KL!
    t_eval = time.time()
    plain_answers = answers_for_plain(merged_model, eval_34_items)
    print(f"[H100] Answered all {len(plain_answers)} eval_34 items on plain merged weights in {time.time()-t_eval:.1f}s!", flush=True)

    # Lie-gap evaluation on plain merged weights
    lie_out = []
    with torch.no_grad():
        for it in P["lie_items"]:
            wrong_lps, never_lps = [], []
            for msgs in it["wordings"]:
                prompt = tok(
                    tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True),
                    add_special_tokens=False,
                )["input_ids"]
                lps = []
                for text in [it["wrong"]] + it["never"]:
                    a = tok(text, add_special_tokens=False)["input_ids"]
                    x = torch.tensor([prompt + a], device=device)
                    lg = merged_model(input_ids=x).logits[0, len(prompt) - 1 : -1].float()
                    lps.append(torch.log_softmax(lg, -1).gather(1, torch.tensor(a, device=lg.device)[:, None]).mean().item())
                wrong_lps.append(lps[0])
                never_lps += lps[1:]
            lie_out.append({
                "arm": "SYSTEM_ROOT1_PLAIN",
                "after": 34,
                "id": it["id"],
                "wrong": round(sum(wrong_lps) / len(wrong_lps), 4),
                "never": round(sum(never_lps) / len(never_lps), 4),
            })

    # Compute ROOT-1 Sanity Check: Logit KL on own_80, local_263, and gsm8k
    merged_lp_own80 = get_last_logprobs(merged_model, own80_eval_items)
    merged_lp_local = get_last_logprobs(merged_model, local_eval_items)
    merged_lp_gsm = get_last_logprobs(merged_model, gsm_eval_items)

    def calc_kl(lp_ref, lp_m):
        return float(torch.sum(torch.exp(lp_ref) * (lp_ref - lp_m), dim=-1).mean().item())

    kl_stats = {
        "kl_locality_own_80": round(calc_kl(frozen_lp_own80, merged_lp_own80), 6),
        "kl_locality_all_263": round(calc_kl(frozen_lp_local, merged_lp_local), 6),
        "kl_gsm8k_150": round(calc_kl(frozen_lp_gsm, merged_lp_gsm), 6),
    }
    print(f"[H100] ROOT-1 Logit KL sanity check (must be > 0 and small): {kl_stats}", flush=True)

    result = {
        "gpu": torch.cuda.get_device_name(0),
        "elapsed_seconds": round(time.time() - t0, 1),
        "weights_sha256_layer27_o": weights_sha256,
        "plain_weights_verified": True,
        "hooks_count": total_hooks,
        "kl_sanity": kl_stats,
        "answers_34": plain_answers,
        "lie_34": lie_out,
    }
    return gzip.compress(json.dumps(result, ensure_ascii=False).encode("utf-8"), compresslevel=6)


@app.local_entrypoint()
def main():
    t0 = time.time()
    p12_path = r"./runs/ccl7-dev-7b\w9792-v12\dataset\payload.json"
    p4_path = r"./runs/ccl7-dev-7b\w9792-v4\dataset\payload.json"
    anc_path = r"./runs/ccl7-dev-7b\w9792-v12\kaggle-output\anchors.jsonl"

    p12 = json.load(open(p12_path, encoding="utf-8"))
    p4 = json.load(open(p4_path, encoding="utf-8"))
    anchor_answers = {
        json.loads(line)["id"]: json.loads(line)["answer"]
        for line in open(anc_path, encoding="utf-8")
        if line.strip()
    }

    v4_qs = {a["messages"][-1]["content"] for a in p4["anchors"]} | {
        r["messages"][-2]["content"] for s in p4["rows"]["LEARNER2"] for r in s["new"]
    }
    own_80_ids = [
        it["id"]
        for it in p12["common"]
        if it["id"].startswith("local|") and it["messages"][-1]["content"] not in v4_qs
    ]

    # Slim payload to only what H100 needs so upload is ~1MB
    slim_payload = {
        "model": p12["model"],
        "revision": p12["revision"],
        "anchors": p12["anchors"],
        "arms": p12["arms"],
        "common": p12["common"],
        "per_eval": {"34": p12["per_eval"]["34"]},
        "checks": {"33": p12["checks"]["33"]},
        "rows": {"LEARNER2": {33: p12["rows"]["LEARNER2"][33]}},
        "lessons": p12.get("lessons", {}),
        "undo": {"3": p12["undo"]["3"]},
        "lie_items": p12["lie_items"],
    }
    bundle_gz = gzip.compress(
        json.dumps({"payload": slim_payload, "anchor_answers": anchor_answers, "own_80_ids": own_80_ids}).encode("utf-8"),
        compresslevel=6,
    )
    print(f"[Local] Sending {len(bundle_gz)/1024:.1f} KB bundle to Modal H100 GPU...", flush=True)
    res_gz = run_root1_plain_weights_h100.remote(bundle_gz)
    res = json.loads(gzip.decompress(res_gz).decode("utf-8"))

    out_path = r"./shakti\ROOT1-H100-PLAIN-WEIGHTS-W9792.json"
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=2, ensure_ascii=False)
    print(f"[Local] Saved H100 result to {out_path} in {time.time()-t0:.1f}s!", flush=True)
    print("KL Sanity:", res["kl_sanity"])
