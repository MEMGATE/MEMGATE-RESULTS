# Founder ke liye: 22 October 2026 ka saar (internal, bahar nahi bhejna)

**Likha:** 22 October 2026, raat ~21:40 IST. Har result ka pura record `docs/` mein uske RESULT document mein hai.

## Aaj kya saabit hua (har test pehle se register, phir chala)
1. **RP-3, hamare apne training loop se, do open model families par:**
   - Qwen2.5-7B (Modal A100) aur OLMo-2-7B (Kaggle T4).
   - Dono mein "aage kya hota hai" sikhane se naye facts par transfer mila: +5.1 aur +4.9 points, dono jeete.
   - Training ke baad doosre offices ki jaankari dono mein giri.
2. **CN-2, kaunsi baat weights mein daalein:** sirf woh daali jo lambe samay tak sach rehti hain. Isse model ke purane (galat) jawab 0.61% se 0.12% reh gaye. 20 mein se 20 worlds mein yahi hua.
3. **PR-1, badla hua tax niyam:**
   - Memory se naya niyam sahi lagaya (Llama 0% → 100%).
   - Nakli "circular" har cheez maanne wali memory mein daala to bade models (sol, astra) ne 100% nakli niyam follow kiya. Layer ki verified memory isse bachati hai.
4. **SC-3, bahut badi memory:** plain retrieval mein 1.7 + 2.9 points ka nuksan hua. Layer ki "ek fact = ek current line" wali memory ne +3.7 points wapas dilaye.
5. **CH-2, teen kadam ki chain** ("naye coach ke desh ki rajdhani"): memory line se +52 points. Jahan model baaki chain jaanta tha, wahan 95–99% sahi.
6. **TQ-1, "is tareekh ko kaun tha?":**
   - Tareekh wali memory line se badlav ke pehle aur baad dono ke sawal 86–100% sahi.
   - Sirf "abhi kaun hai" wali memory se do models ne purani tareekh par bhi naya naam bataya (94–97%).
7. **TQ-W:** GPT-4.1 ko naye holder par fine-tune kiya to usne purani tareekh ke 83% sawalon par bhi naya naam bataya. Weights waqt mita dete hain, memory yaad rakhti hai.

Ledger mein ab 212 rows hain, 0 galti. Brief, report aur home page update ho gaye hain, aur memgate-eval (private) mein bhi.

## Abhi kya chal raha hai
- **FT-2, CD-1, FT-1 (GPT-4.1 / nano ki lagatar fine-tuning, layer ke saath aur bina):**
  - Har world ki 4 copies: global, developer, Standard North Central US, Standard Sweden Central. Jo pehle khatam hogi wahi ginegi.
  - Azure par GPU ki line lambi hai, phir bhi ab 10 ke aas-paas jobs ek saath train ho rahe hain.
- **CN-2 GPT-4.1 par** (8 chains) aur **PR-2** (naya tax niyam GPT-4.1 ke weights mein): Sweden Central mein line mein.
- **Kaggle:** CN-2 OLMo-2-7B par (10 worlds).
- **LS-1:** Wikidata ki live edits ki recording, 28 October tak.

## Kya ruka hua hai, aur aapko kya karna hai
- **72B model ke tests:** iske liye 80 GB wala GPU chahiye.
  - Modal ka mohitaureus workspace billing ki wajah se paused hai: card par international/recurring payments ON karein, failed payment retry karein.
  - Azure ne GPU quota "payment history" ki wajah se mana kiya. Maine saboot ke saath jawab bhej diya hai. Aap portal se Billing → Account Review ticket kholein.
- **Kaggle token:** chat mein aaya tha, kaam ke baad badal dein.

## Data
- Repos private hain.
- Kaggle ki copies run ke baad delete hoti hain.
- Bahar ke models ko sirf test ke sawal jaate hain.

## Raat ka update (23 October, ~00:05 IST)
- **CN-2 ka OLMo-2-7B replicate (Kaggle) poora hua.** Teeno test jaise predict kiye the waise hi nikle. Purane (galat) jawab 0.54% se 0.11% par aaye, 10 mein se 10 worlds mein.
- **TW-1 naya test hai: kya tareekh weights mein bachti hai?**
  - Teen open model families par dev hua: OLMo (AI2), Qwen (Alibaba) aur Nemotron (NVIDIA).
  - **Weights:** model ko tareekh ke saath fine-tune kiya, kuch offices par tareekh ke sawal bhi practice karwaye. Phir bhi purani tareekh par 0% sahi aaye; model naya naam hi bata deta hai.
  - **Memory:** tareekh wali memory line se dono tareekhon par sahi naam 18–62% offices mein aaya.
  - Prereg 23:50 par freeze hua. Main run OLMo aur Qwen par chal raha hai, Nemotron uske baad.
- **NVIDIA key:** private file mein rakhi hai, sawal bhejne ke liye use nahi hui. Unki free service bheja hua data 30 din rakhti hai, aur aapka niyam hai ki data bahar na jaye. NVIDIA ka open model hamare Kaggle private kernel mein chal raha hai.
- **Azure:** 55 jobs mein se ~5 train ho rahe hain, baaki GPU ke intezaar mein. Microsoft ka koi naya jawab nahi aaya.
