# CCL-6 at 72B: addendum to the CCL-6 preregistration (frozen)

**Status: FROZEN on 28 October 2026, 17:06 IST, after the 72B dev check (`runs/ccl4c72-dev-72b/w9792-errors-s4`, done 16:28) and before either 72B world was packed.** Drafted at 14:14; the machine and time limit were updated at 16:32. Part B item 8, second half (`docs/PARTB-PLAN-2026-10-28.md`).

The CCL-6 preregistration (`docs/CCL6-PREREG-2026-10-28.md`, frozen 28 October 02:16 IST) already provides for this run: "The 72B (4 bits) follows the same plan if compute allows; it is analysed on its own." This addendum fixes only what that sentence leaves open; everything else is the preregistration's, unchanged: the learner (SYSTEM3), the arms (SYSTEM3, NAIVE and the untouched model), the hypotheses and their rules, the analysis (`cl/ccl6.py` `e5c49aa08360…`) and the validity rules.

## What this addendum fixes
- **Model:** Qwen2.5-72B-Instruct, revision `495f39366efe…` (CCL-4's and CCL-5's 72B), in 4 bits (NF4), as the packer's `--model 72b` holds it.
- **Worlds:** the office worlds 9708 and 9709, the 7B run's own (their 7B results are known; the 72B's are not). The release worlds are not run at 72B.
- **Packs:** `PYTHONHASHSEED=0 python cl/cl6.py pack 9708:main runs/ccl6-main-72b/w9708 --model 72b --arms SYSTEM3,NAIVE --errors 40 --errors-at 0 --prereg docs/CCL6-PREREG-2026-10-28.md`, and the same for 9709 (CCL-6's packer `ad6417fcfa43…`, unchanged), run without Python's isolated mode so that the hash seed applies. Each payload must equal the 7B run's payload for the same world except the model, its revision and the 4-bit flag; this is checked after packing.
- **Machine:** one world per job, on either of two machines with the same GPU model (A100 80GB PCIe):
  - Azure's serverless A100 80 GB, with 24 vCPUs and 220 GiB and `--hours 60` (a 72-hour job timeout was probed and accepted on 28 October at 16:23 IST);
  - the lab's A100 VM (`cl/vm_run.py --hours 60`, `docs/MACHINE-A100-VM-2026-10-28.md`).

  Each run's `aca.json` or `vm.json` records the machine. Expected time: about 30 hours a world, from the 72B's speeds in the dev check.
- **Analysis:** `python cl/ccl6.py report runs/ccl6-main-72b/ccl6-offices-report.json runs/ccl6-main-72b/w9708 runs/ccl6-main-72b/w9709`.
- **Time, from the dev check's speeds:** the 72B in 4 bits trained about 0.9 rows a second (SYSTEM2) and 1.3 (NAIVE), and answered about one question a second.
  - At CCL-6's sizes (SYSTEM3 about 40,000–46,000 rows a world, NAIVE about 17,000–24,000, seven evaluations with the safety and instruction prompts), a world takes about 30–32 hours.
  - `--hours 60` leaves room.
- **Predictions (72B):** the same as the 7B result, for the same reasons.
  - **WIN:** H1, H11, H12, H5, H6, H7 and H13L.
  - **NON-INFERIOR:** H2, H3, H10, H8, H9, H15b, H16, H16s and H17.
  - **NOT SHOWN, more likely than not:** H12b and H15. At 72B, H12b was +0.043 and +0.057 in CCL-4 and CCL-5, with intervals wider than the margin.
  - **FAILED:** H18. SYSTEM3 has no period rows; they are CCL-7's change.
  - So abilities 1–3, 5–9, 13 and 14 are predicted PASSED, 4 and 15 NOT SHOWN, and 5b FAILED.
  - **Secondary:** H17a FAILED and H16a NOT SHOWN. The trained weights alone lose instruction-following as at 7B; the system keeps it by its scope rule.
