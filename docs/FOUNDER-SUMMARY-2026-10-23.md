# Founder ke liye: 22–23 October 2026 ki raat ka saar (internal, bahar nahi bhejna)

**Likha:** 23 October 2026, subah ~06:30 IST. Har result ka pura record `docs/` mein uske RESULT document mein hai.

## Raat mein kya saabit hua (har test pehle se register, phir chala)
1. **CN-2, doosri model family (OLMo-2-7B) par bhi:** sirf woh baatein weights mein daali jo lambe samay tak sach rehti hain. Isse model ke purane (galat) jawab 0.54% se 0.11% reh gaye, 10 mein se 10 worlds mein.
2. **TW-1: kya tareekh weights mein bachti hai?** Teen open models par test hua: OLMo (AI2), Qwen (Alibaba) aur Nemotron (NVIDIA).
   - Model ko naya badlav tareekh ke saath bhi sikhaya, phir bhi purani tareekh ke sawal par usne 95–100% baar naya naam bataya. Weights waqt mita dete hain.
   - Tareekh wali memory line se dono tareekhon (pehle aur baad) par sahi naam 17–68% offices mein aaya, aur weights se lagbhag 0%.
   - Ek nayi baat: 150 offices par "is tareekh ko kaun tha" ki practice karwane se baaki offices par bhi 38–45% sahi aaye. Maine predict kiya tha ki koi farak nahi padega; ye galat nikla, aur result mein likha hai.
3. **TW-2: memory padhne ka hunar weights mein.** Chhote model ko doosre offices par sirf memory line padhna sikhaya, facts memory mein hi rahe.
   - Naye offices par dono tareekhon par 98–100% sahi aaye. Bina sikhaye ye 17–68% tha.
   - Model ki baaki jaankari bilkul nahi giri.
4. **TW-3: ye hunar naye kaam aur naye format par bhi chala.** Sirf football coach wale offices par sikhaya tha.
   - Sarkar, CEO aur chair jaise offices par, ek naye note format mein, 90–100% sahi aaye.
   - Do models mein baaki jaankari 3–4 points giri. Ye hamari tay ki hui seema ke andar saabit nahi hui, aur result mein likha hai.

**Matlab:** tareekh wale facts memory mein rakho, aur unhe padhne ka hunar weights mein. Yahi hamare layer ka design hai, aur ab teen open model families par preregistered test se saabit hua hai.

## Documents
- Ledger mein ab 217 rows hain, 0 galti.
- Brief (chhota aur pura) aur report Part II update ho gaye, PDFs dobara bani.
- memgate-eval (private) bhi sync ho gaya.

## Abhi kya chal raha hai
- **Azure fine-tuning:** FT-2, CD-1 aur FT-1 ki har world ki 4 copies chal rahi hain. ~5 jobs train ho rahe hain, baaki GPU ke intezaar mein. Koi world abhi tak poori nahi hui.
  - FT-1 ki world 9102 ka global copy raat 00:52 par Azure ke deployment refusal se ruk gaya tha. 06:09 par ek baar dobara chalaya, ab chal raha hai.
- **GPT-4.1 par TW-1** (bada model tareekh rakh pata hai ya nahi): 3 jobs Azure ki line mein hain.
- **CN-2 GPT-4.1 aur PR-2:** Azure ki line mein hain.
- **Kaggle:** is hafte ke 30 mein se ~17 ghante use hue. Har run ke baad copy delete ki gayi.

## Kya ruka hua hai
- **72B model ke tests:** Modal ka workspace abhi bhi "paused" hai (billing). Azure GPU quota 0 hai, aur Microsoft ka naya jawab nahi aaya.
- **NVIDIA key:** private file mein hai. Hamare sawal NVIDIA ki free service par nahi bheje, kyunki wo data 30 din rakhti hai. NVIDIA ka open model (Nemotron) hamare Kaggle private kernel mein chala.
- **Tokens/keys jo chat mein aaye** (Kaggle, NVIDIA): kaam ke baad badal dena.

## Shaam ka update (23 October, 17:30)

### Naye nateeje
1. **LM-1: public benchmark (LongMemEval) par layer ki memory.** 402 held-out sawal, blind hand labels se score kiye gaye; koi bahar ka model judge nahi.
   - Retrieval ke saath layer ki dated notes dene se GPT-4.1 72.8% se 83.9% par aaya, aur gpt-6.1-sol 77.1% se 94.9% par. Dono par preregistered WIN.
   - Poori history context mein dene ke muqable: GPT-4.1 mein +9.35 points behtar, sol ke barabar, aur dono jagah lagbhag ek-tihai tokens mein.
   - Ek prediction galat nikli: GPT-4.1 ke time wale sawalon par poori history se +5.6 aaya, par ye saabit nahi hua.
   - Ye numbers published LongMemEval numbers se seedhe compare nahi hote, kyunki wahan GPT-4o judge hai. Ye baat har jagah likhi hai.
2. **PL-1: layer ki "kam coverage" wali kami ka ilaaj.** Memory mein ek line jodi: "abhi verify nahi hua, par 2+ independent sources ye keh rahe hain".
   - Current holder batana 5.21 points badha (WIN), chaaron models mein.
   - Attacker ki value 0.0% rahi (SAFE).
   - "Har report maan lo" wali memory se ab 9.9 points ka gap bacha hai.
3. **TW-5 (descriptive):** practice jitni zyada, utna fayda, par dheere. 150 practised offices par bhi dono tareekh sahi sirf 26–35%. Memory-line reader 98–100% deta hai.

### Package
- Brief, report, aath company copies, PDFs aur memgate-eval mein LM-1 aur PL-1 jud gaye. Har jagah claims aur outward checks 0 findings dete hain.
- **20 kathin sawalon ke jawab:** `outreach/HARD-QUESTIONS-2026-10-23.md` (aur PDF). Calls ki taiyaari ke liye; kisi model ka naam nahi.
- Ledger: 221 rows, 0 galti.

### Session aur runners
- 11:07 par session band hua to saare runners ruk gaye; 12:30 ke baad sab phir se chalu kar diye (purani jobs reuse karke).
- Ye runners ab is session ke background tasks hain. Session band hua to ye phir rukenge, aur agle session mein main inhe phir chalu karunga. Azure ki jobs par asar nahi.

### Abhi bhi chal raha hai
- Azure par FT-2, CD-1 aur FT-1 ki chains. Sweden Central mein lagbhag sab jobs GPU ke intezaar mein hain.
- GPT-4.1 par TW-1, CN-2 GPT-4.1 aur PR-2, sab Azure ki line mein.
- LS-1 live capture, 28 October 17:55 tak.

### Aapse
- **Gemma ka licence abhi bhi 403 de raha hai.** Kaggle par (mohitaureus) kaggle.com/models/google/gemma-3 kholkar "accept" karna hai.

### Raat ka note (18:25)
- **Azure ka "unusual activity" (715) block phir aaya.** 16:57 se 18:02 ke beech 6 chains ko deployment se mana kiya gaya, North Central US aur Sweden Central dono mein. Wajah ye thi ki restart ke baad har chain apne purane blocks dobara deploy kar rahi thi.
- **18:12 par saari world chains rok di gayin,** taaki aur requests na jayein. Azure par training jobs chal rahi hain.
- **Kal subah 06:13 par ek baar restart hoga,** naye wrapper ke saath jo purane blocks ke saved jawab reuse karta hai, taaki sirf naye blocks deploy hon. Jin 6 chains par refusal aaya, wo hold par rahengi; har world ki baaki copies chalengi.
- **Kal subah 05:37:** Kaggle par Nemotron ka LongMemEval replicate (NVIDIA ki copy ke liye).
- **Raat bhar:** Claude aur Grok par LongMemEval replicates (Anthropic aur xAI ki copies ke liye).

### Raat ka note 2 (19:25)
- **Monday ke liye sab taiyaar, bina galti:** proofread ki saari asli galtiyan theek ho gayin. Brief ab 2 page ka hai, har company ke notes paste-ready plain text mein hain, aur dono checkers mein 0 findings hain. Bhejne ka tareeka `outreach/SEND-CHECKLIST-2026-10-26.md` mein hai.
- **Kaggle ke T4 lambe prompts par fail hue,** isliye Nemotron ka replicate ab Modal ke H100 par chalega (5:37 wala Kaggle kaam hata diya). Microsoft ke liye Phi-4-mini aur Google ke liye Gemma 3 (12B) bhi isi tarah chalenge. Har ek ka addendum chalane se pehle likha jayega.
- **Meta ke model par abhi nahi:** Kaggle par Llama abhi bhi 403 de raha hai, aur Azure par Maverick ki quota ek lambe prompt se bhi kam hai.
- **Aapse do faisle:** lab ka naam (forms ke "Company" field ke liye), aur Azure critical ticket ke liye phone number.
