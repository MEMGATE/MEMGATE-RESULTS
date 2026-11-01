# A tested recipe for a supervising AI that watches a site through several sources

18 October 2026. This note is drawn only from preregistered results on fresh data in this lab ([synthesis](SYNTHESIS-2026-10-18.md)). It is written for a product such as a supervising AI that watches a warehouse or a machine through several cameras or sensors and works with an owner. Each rule names its evidence, its size and its limits.

**Saar (Hinglish).**
- Kai alag sources ho, aur har ek akele bhi kuch pehchan sake.
- Sab sehmat hon aur koi andaaza na laga raha ho, tabhi AI akele bole; warna owner se pooche.
- Jo source baar-baar akela alag bole, use hata kar owner ko batao.
- Har site/machine ka saboot alag rakho, agar unka apna star alag ho.
- Model se poochho ki wo sure hai ya nahi.
- Audit aur reset tabhi rakho jab galat jawab bahut mehenga ho.

## The rules that held

| # | Rule | Evidence (fresh data) | Size | Limits |
| --- | --- | --- | --- | --- |
| 1 | **Answer alone only when independent sources agree and none is guessing; otherwise ask the owner.** | AR-1 H4; MX-7 | Agreeing answers right 96–99.7%, +16.61 and +28.88 pp over random answers | Needs sources that can each decide often on their own. Without that, the system asks about almost everything and fails safe: MX-6 (naval simulator) and MX-9 (WISDM phone and watch, 18 similar activities). Check this per deployment before relying on the rest. |
| 2 | **Dismiss the source that is the odd one in 20 of its last 30 two-against-one splits, and tell the owner.** | AR-1, MX-5, MX-7, MX-8 | Credence after a sensor failure +13.41, +11.82 and +12.85 pp; the whole supervisor +13.14, +9.68 and +14.52. The broken source was found in 36/40, 52/60 and 10/10 runs, about 30 cases after the failure, and rarely wrongly. | At most one source dismissed. A weak but working source may be dismissed too, which here cost nothing (AR-1 H3 +1.14). **With two broken sources it does not fire: wrong answers alone rose to 2.00 per 100, past the safety bound (MX-10, UNSAFE).** **Add a system-level alarm on three-way disagreement (MX-11): it caught 16 of 20 double failures, cut wrong answers alone to 0.84 per 100 (SAFE), and never fired early. Make it pause and ask the owner, not stop for good; a permanent stop costs on false alarms. Do not let it resume on its own when the sources agree again: broken sources learn to agree (MX-12, UNSAFE). Verify each source against the owner's answers before resuming (MX-13: never wrong, 21 of 21), over more than 30 cases. Expect about 1–2 wrong answers alone per 100 while two sources are broken (MX-10 to MX-13).** |
| 3 | **Keep evidence per site, machine or person when the units differ in baseline; pool it when they watch one shared phenomenon.** | SL-1, SL-2 | Same-locus vs random grouping +1.04 and +12.27 pp. Patients' disease level 66.9% → 90.9%. | It costs where units share one phenomenon (one city's weather stations, −5 pp). Naming the unit as a feature is a safe middle (+0.72, +6.10). Inside the supervisor, with 8 healthy people, it added only +1.38 (MX-8, UNDETERMINED). |
| 4 | **Ask the model whether it is sure; trust its SURE more than its UNSURE.** | ML-7 | SURE answers +8.33 pp more accurate than random answers. 72–88% right when SURE, about 50% when UNSURE. | One model (gpt-6.1-sol), synthetic tasks. The model is sometimes sure and wrong after the world changes. |
| 5 | **Ask for labels only under doubt.** | JK-1, PV-1, MX-2, RP-1 | +3 to +4 pp over random asking at the same number of labels | Replicated on five pools. |
| 6 | **Spot-check about 5% of the answers given alone when a confident mistake is very costly.** | MX-3, MX-4 | +9.58 and +13.13 pp accuracy alone under abrupt change (56% → 81.7% on Beijing PM2.5) | With rule 1's guessing clause, audits added nothing to net credence (MX-5 −0.96, MX-7 −0.04). They pay only if a wrong answer costs more than about 10 right ones. |
| 7 | **Watch the system's own error rate against its own baseline (prakṛti–vikṛti), and reset on an abrupt rise when mistakes are costly.** | PK-2, MX-3 | A diagnosed reset beat a random-time reset by +5.59 pp; +4.74 beyond audits | Inside the supervisor, resets cost net credence (−1.00, −1.42) while cutting wrong answers given alone (−0.56). They pay if a wrong answer costs more than about 2.8 right ones. |

## What did not hold, or holds only sometimes

| Idea | Result |
| --- | --- |
| Bringing back refuted rules (saṃskāra) | Won where the world returns to an earlier state (+2.22) and inside the supervisor on one machine (+2.56). Lost on five real calendar and weather streams (−1.39), and was ≈ 0 on body sensors. Use only where refutations are mostly noise. |
| Ranking or selecting among members instead of letting them vote | Jyotiṣa's friendship grades +0.04; local competence −0.25; one member overruling the others −0.67. Equal votes are hard to beat. |
| Sacred proportions, cosmic cycles, most rule-arbitration doctrines | NO WIN (see the synthesis). |

## What is not yet tested

- A real camera system: every result here is on tabular sensor and benchmark data.
- Vision models as sources.
- Costs of wrong answers taken from a real site. Rules 6 and 7 turn on them.
- More than one model; ML-3 is suspended.

## Honest position

Each rule above has a known name in machine learning: multi-view agreement, selective prediction, sensor-fault detection, mixed effects by unit, verbalized confidence, active learning, monitoring.

The value here is not novelty. It is that each was tested the same way, preregistered on fresh data and replicated where marked, with their limits found, including the failures.
