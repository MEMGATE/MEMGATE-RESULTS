# Project state, 28 October 2026, 23:18 IST

This file is kept current. The step-by-step record is in `journal/` (one file a day, since 28 October), and the run folders' states in `handoff/RUNS-LATEST.md` (written by `scripts/sync.py`).

**Founder:** Manish Kumar (they/them).
- Replies in short, simple Hinglish, with honest numbers and no shifting lists.

**Goal:** a big deal with an AI lab (labs only, big deal only), on a continual-learning system that learns into a model's weights.
- Since 20:20 on 28 October the founder's goal is to **solve** continual learning: the trained weights alone must not forget. Showing that the routed system works is not enough.

**Send date:** 10–15 November. The founder sends; the assistant never sends anything outward.

**The plan:** 19 items.
- Part A (1–7): `claude_lab/docs/GPU-RUN-PLAN-2026-10-27.md`.
- Part B (8–15) and the founder's additions (16–19): `claude_lab/docs/PARTB-PLAN-2026-10-28.md`.
- The package plan: `claude_lab/outreach/PACKAGE-v5-PLAN-2026-10-28.md`.
- The brief draft: `claude_lab/outreach/BRIEF-v5-draft.md`.
- The hard questions: `claude_lab/outreach/HARD-QUESTIONS-v5-draft.md`.
- The competitors: `claude_lab/outreach/COMPETITORS-2026-10-28.md`.

## The 19 items
| # | Item | State on 28 Oct 21:45 |
| --- | --- | --- |
| 1 | 12 of 12 abilities at 7B (CCL-4, 4R, 4C) | done |
| 2 | Gemini's points: CCL-6 (34 sessions, two domains), NB-1, SU-1, XF-2 | CCL-6 done; NB-1 done (19:20); SU-1 one of two worlds done; XF-2 queued |
| 3 | MEMIT and AlphaEdit (BL-1) | frozen, packed, queued |
| 4 | Retrieval (BL-2) | done |
| 5 | No registry (RG-1) | done |
| 6 | Second family, OLMo-2 (XF-1) | done |
| 7 | GPT-4.1 hosted (CCL-5H) | moving again by 23:16: 9703 NAIVE 7/12 sessions; 9702 NAIVE in session 2; both SYSTEM3 chains past session 1; dev world still stuck; optional |
| 8 | 72B: CCL-4C72 (8 runs) and CCL-6 at 72B (2 worlds) | both frozen and packed; CCL-6 72B world 9708 running on the VM since 18:43 (about 30 h) |
| 9 | Real Wikidata stream (RW-1), 7B and one 72B world | dev done; the world counts same-name values as right (fix 17:40); freeze after CCL-7's decision |
| 10 | Beyond retrieval (BL-3) | frozen, packed, queued |
| 11 | The weights alone keep safety, IFEval, old facts, general ability (CCL-7) | v2 and v3 7B dev trials running; v4 and v5 packed (1.5B and 7B), next on the GPUs |
| 12 | The three misses (transitional, plasticity, ability 8) (CCL-7) | fixed in the first 7B dev (transitional 0% to 90.6%) |
| 13 | Llama, Gemma, Phi-4 (XF-M) | frozen, packed (6 runs), queued |
| 14 | Ten times the facts (X10) | frozen, packed (2 worlds), queued |
| 15 | Demo labs question themselves | adapter run done 22:23; bundle built and uploaded; smoke test `runs/demo-test/smoke-1.5b` next on a T4 |
| 16 | Public benchmark: WikiBigEdit | WB-1 built 23:14 (`cl/wb1.py`, draft plan); 1.5B dev pack (320 changes) first in the T4 queue; mains 9726, 9727 at 7B after CCL-7's decision |
| 17 | Learning from text | TX-1 built 23:04 (`cl/tx1.py`, draft plan); perfect-reading check passed; 7B reading job of dev world next on an A100, then a 1.5B learner dev on a T4; mains on CCL-7's 4 worlds |
| 18 | Bounded cost per update | BC-1 built 22:20 (`cl/bc1.py`, draft plan); 1.5B dev packed; mains after CCL-7's decision (4 worlds) and on X10's 2 worlds |
| 19 | Deletion on request | DR-1 built 22:35 (`cl/dr1.py`, draft plan); 1.5B dev packed (delete, retrain); mains on CCL-7's 4 worlds |

## The trained weights alone (founder's goal)
Measured on 28 Oct, 7B, 34 sessions: every question sent to the trained weights, with no routing.

| Measure | Weights alone | Untouched model | Naive fine-tuning |
| --- | --- | --- | --- |
| Never-streamed offices | 15.6–17.9% | 99.2% | 20–28% |
| GSM8K | 83–90 | 92.7 | |
| MMLU | 58.5–65 | 72.5 | |
| IFEval | −23 (CCL-6); −9.5 with the first anchors | | |
| Unsafe refusals | about −4.5 | | |

**The fix line:** rehearse the untouched model's own answers (anchors).
- v1: 100 IFEval prompts.
- v2: all 341 unused IFEval prompts and 200 AdvBench requests.
- v3: v2 plus 150 office questions from the other half of the snapshot, 150 MMLU and 50 GSM8K items.
- v4 (21:48): v3 plus two unchanged offices of the same kind beside each change the learner takes in (viveka).
- v5 (21:58): v4 plus the model's own answers to 100 code questions of other libraries (svadharma).

The rule, written before the results, picks the latest version (v5, v4, v3, v2, v1) that keeps every rule the first trial met. The next idea, if v3 is not enough, is in `internal/CL-FROM-THE-TEXTS.md`.

## Running GPU jobs at 23:18
| Machine | Run |
| --- | --- |
| A100 (Container Apps) | `runs/ccl7-dev-7b/w9792-v2` (since 19:02; NAIVE arm) |
| A100 (Container Apps) | `runs/ccl7-dev-7b/w9792-v3` (since 20:38) |
| T4 | `runs/ccl7-dev-1.5b/w9792-v4` (since 22:28) |
| T4 | `runs/ccl7-dev-1.5b/w9792-v5` (since 23:12) |
| A100 VM | `runs/ccl6-main-72b/w9708` (since 18:43, `--hours 60`) |

Next A100s: the TX-1 reading job (about 15 minutes), then v4 7B, then v5 7B. Next T4s: WB-1 dev, BC-1 dev, DR-1 dev (delete, retrain), TX-1 dev, the v2 1.5B rerun. Done today: the demo's adapter run and the demo smoke test (passed 23:06). The 1.5B v2 trial was stopped by the platform at 22:20 (exit 143).

The queue order is in `handoff/WATCH-PROMPTS.md`.

## Rules that must not be broken
- **Frozen files:** never edit them (list in the watch instructions).
- **Preregistered tests:** frozen before their main runs; results reported as they come, failures included.
- **Packers:** run without Python's `-I` (it ignores the hash seed).
- **Before every commit:**
  - the secret grep finds nothing;
  - no Sanskrit word in the lab repository;
  - no EagleAI in the lab repository.
- **The origin of the ideas stays internal**: the repository says only plain English.
- **The founder's decisions, in their words:** see `memory/` (no-confusion, no-rush-big-package, final-package-list, solve-cl-weights-goal, budget-unlimited).
