# CCL-5 (draft spec): learning better over time, measured where there is room

Status: **draft**, 26 October 2026. Nothing here changes CCL-4 (frozen 09:47 IST); CCL-5 is a separate test of ability 8, run after CCL-4 with the same system plus one mechanism.

## Why a new test
CCL-4's H13 compares new items missed at the first check after their session's training, early against late. At 7B there is no room: the first check misses 5–10% of new items from the first session on, in every kind (CLX-14, world 9792: offices 21/344 early, 11/136 late; dated 14/180, 5/106; what follows 4/38, 9/98; weighted +0.12 [−3.72, +3.78]). The first check asks the wordings the learner was trained on, and those are learned at the first pass. A larger model will have even less room.

Room exists in what the learner was not trained on directly. At the end of CLX-14, SYSTEM2 answered 65% of dated questions (dates between the dates its rows name), against 47% for naive training and 18% for the untouched model. Learning better over time, in a sense a lab cares about, means that the learner gets better at making new knowledge usable beyond the sentences it was taught: later sessions' new facts are answered right in forms never trained more often than earlier sessions' were.

## The mechanism: lessons from its own mistakes, in the weights
SYSTEM3 = CCL-4's SYSTEM2 plus:
1. **Probes.** After each session's training, the learner writes held-out probes about that session's new items from its own registry, which knows the truth: dated questions at dates strictly between the change dates it knows (never a date a row names), what follows in a wording it never trains, and the earlier holder at a date before a change. It answers them and checks.
2. **Patterns.** It sorts its misses into patterns it can read off the registry: the earlier holder named for a date after the change (stale), the later holder named for a date before it (premature), the right person in the wrong form, another person of the same post.
3. **Lessons.** For a pattern that recurs (at least three misses in a session), it writes lesson rows: the rule in plain words and two worked examples taken from its own misses with the right answer, trains them in the next session and rehearses them afterwards. Probes themselves are never trained.

This is the in-weights form of what ML-M showed in context (lessons the system wrote from a model's own verified mistakes cut its stale answers on new cases by 11.8 points [+8.71, +14.96]).

## What is measured (to be fixed in the preregistration)
- **H13′ (ability 8):** held-out probe accuracy on each session's new items at their first check, items of sessions 9–12 minus items of sessions 1–4, within kind of probe, SYSTEM3; WIN if the lower bound is above 0.
- **H13″:** the same difference, SYSTEM3 minus SYSTEM2 (the lessons, not just more training); WIN if the lower bound is above 0.
- Every CCL-4 hypothesis, on SYSTEM3, so that the twelve abilities are again shown together.

## Arms, worlds, models
FROZEN, NAIVE, SYSTEM2 (as frozen in CCL-4) and SYSTEM3; two new main worlds (9704, 9705), 40 registry errors each; Qwen2.5-7B on Kaggle's GPUs after the weekly reset, then the 72B on a 96 GB GPU if CCL-4's 72B worlds show the system works there.

## Before freezing
CPU tests of the probes and lessons; one 7B dev world with SYSTEM2 and SYSTEM3 side by side (probe accuracy per session and kind, lessons written, cost); predictions from it.
