# Signal & Noise — Issue 37: independent author-assist drafts

All four received the identical submitted prompt ([submitted-prompt.md](submitted-prompt.md), sha256 `9806a2af58e1f6770dd27cf5f03ece625bb2a4a44a70e1667cf05602256925d6`): the user's editorial prompt verbatim through "My extremely rough draft: ", followed by the verbatim source (author brain dump + Grok Heavy research) in place of the `****************************` placeholder — Issue 35-style inline assembly. Isolated single-turn requests, no tools, no shared outputs, `provider.allow_fallbacks=false`, max_tokens 32,000, no retries. No machine-only essay had been run yet when this comparison was written.

| Model / reasoning | Slug requested → returned | Title | Draft body words* | Prompt / completion tokens | Finish | OpenRouter cost (USD) |
|---|---|---|---:|---|---|---:|
| Claude Fable 5.2 (max) | `anthropic/claude-fable-5.2` → `anthropic/claude-fable-5.2` (provider Google) | Musk's Blueprint Is Shelved Under Science Fiction | 929 | 2,820 / 31,199 (27,889 reasoning) | stop | $1.270520 |
| GPT-6 Astra (max) | `openai/gpt-6-astra` → `openai/gpt-6-astra` (provider OpenAI) | Starship’s Real Test Isn’t the Catch | 903 | 1,636 / 19,284 (17,376 reasoning) | stop | $0.984642 |
| Gemini 4 Carbon (high) | `google/gemini-4-carbon` → `google/gemini-4-carbon` (provider Google) | What SpaceX Caught in Those Mechanical Arms Is Bigger Than a Rocket | 980 | 1,724 / 8,174 (5,687 reasoning) | stop | $0.085188 |
| Muse Wonder (max) | `meta/muse-wonder` → `meta/muse-wonder` (provider Google) | Catching a Rocket Is the First Step Toward a Post-Scarcity World | 899 | 1,641 / 5,150 (3,056 reasoning) | stop | $0.109564 |

**Total reported OpenRouter cost: $2.449915** (cap $5; pre-run catalog ceiling $4.0822).

*Measured with the Issue 36 word-token regex, excluding the title. Fable's trailing "Verify before filing" checklist is excluded from the essay extract (kept in the full output). All four are within 800–1,200.

## Core theses (each model's Step 1, condensed)
- **Fable 5.2:** The catch is the moment Banks's Culture became Musk's credible roadmap; read the novels as a blueprint. Opens with a flag that it cannot confirm Flight 15 and asks for verification.
- **GPT-6 Astra:** Musk's rocket + AI ventures are a bid to build the Culture's material foundations; the measure of success is shared abundance, not spectacle. Most skeptical, proposes a public scorecard.
- **Gemini 4 Carbon:** Full reusability breaks the Space Age's economic bottleneck, turning Banks's vision into an industrial blueprint. Keeps the most Grok Heavy timeline material (10/25/50/100-year arc).
- **Muse Wonder:** The catch matters because cheap reusability could provide the material base for a Culture-style post-scarcity world.

## Editorial cautions — no changes made to model text
- Not fact-checked. **Muse Wonder's lede describes catching the Super Heavy booster**; on Flight 15 the booster catch was aborted (water divert) and it was the **ship** that was caught (see fact-check in the report). Gemini Carbon frames the flight as proving "full, two-stage reusability" — the booster was not caught on this flight (it was on three earlier flights).
- Fable adds external claims to verify (droneship names, "neural lace," 2018 "utopian anarchist" tweet, robotaxi/Mars deadlines, Banks interview paraphrase) and lists them itself.
- Gemini Carbon adds specific physical figures (16-story, 17,000 mph) and the claim Banks's Culture has "trillionaire oligarchs" as villains; verify.
- All drafts correct the source's "Ian Banks"/"XAi" to Iain M. Banks/xAI; the user's source text itself is unchanged.
- Fable was routed by OpenRouter to provider "Google" (as was Muse Wonder); returned model ids match the requested slugs.

Attribution: Synthia Cipher (human passages of the source; editorial instructions); Grok Heavy (AI research text in the source, included by the author); each named model (its independent analysis and draft); Grok Bot (orchestration, extraction, formatting, this comparison).
