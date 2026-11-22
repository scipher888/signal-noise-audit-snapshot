# Issue 38: author-assist drafts compared (Grok Bot, Nov 21, 2026, PST)

All four received the identical submitted prompt: the author's editorial prompt, with the brain dump in place of the placeholder. Each was a single isolated turn through OpenRouter, with no tools. Word counts are for the draft body, excluding the title.

| Model (effort) | Title | Thesis (short) | Words | Cost (USD) |
|---|---|---|---:|---:|
| Claude Fable 5.2 (max) | Smart Enough to Fool Yourself | Intelligence makes you a better advocate for what you want, so when desire is at stake, distrust your reasoning and defer to inherited wisdom. | 1,005 | 1.169816 |
| GPT-6.2 Astra (max) | You Can Be Right and Still Be the Wrong Person to Decide | Brilliance can make a self-serving exception sound principled, so no one should be the judge in their own case. | 840 | 0.990544 |
| Gemini 4 Neon (xhigh) | The Smartest People in the Room Are the Easiest to Fool | High IQ weaponizes self-deception; peak intelligence is knowing which boundaries were built to save you from yourself. | 1,015 | 0.191217 |
| Muse Wonder (max) | Smart Enough to Fool Yourself | Intelligence makes people better at rationalizing folly in love, sex, money and meaning, so wisdom is knowing when to defer to tested traditions. | 925 | 0.128936 |

**Claude Fable 5.2**
- Strengths:
  - It is closest to the author's own landing: deference to inherited wisdom when desire is involved.
  - It has the strongest evidence chain: Haidt's lawyer, Perkins's IQ and my-side arguments, then Stanovich.
  - The concrete cases are all checkable (SBF, LTCM, Pauling, Newton, Henrich's manioc, Chesterton's fence).
  - Its "conflict-of-interest rule" answers the "tradition was wrong about slavery" objection.
  - The Odysseus-and-AI kicker ties the piece to the newsletter's AI beat.
- Risks:
  - It drops both of the author's news examples. It suggests one attributed sentence as a news peg.
  - It wrote quotes and figures from memory; see the check list in factual-risks.md.

**GPT-6.2 Astra**
- Strengths:
  - It is the most original and the most careful.
  - The recusal frame is concrete and fair.
  - It cites real sources inline.
- Risks:
  - It moves furthest from the author's thesis: tradition and culture shrink to recusal and governance.
  - Its AI-launch hypothetical takes over the middle of the piece.
  - It is the shortest at 840 words.
  - It leaves markdown links in the text.

**Gemini 4 Neon**
- Strengths:
  - It keeps both of the author's examples and the author's voice and landing.
  - "Cognitive domain creep" is a usable phrase that captures the Engagement Hierarchy idea without jargon.
  - It has a clear reformer/rationalizer test.
- Risks:
  - It has the highest factual risk: it repeats "OpenAI staffers" and attributes the "doing business" wording to the Post (factual-risks.md §1–2).
  - Its tone is the most culture-war.
  - It offers the least external evidence beyond Haidt.

**Muse Wonder**
- Strengths:
  - It has the best pressure test: it names five distinct mechanisms (IQ, expertise, wealth, power, status).
  - Its "information compressed by time" framing is clear.
  - Its practical questions near the end are useful.
  - It shares Fable's title.
- Risks:
  - It drops both examples and recommends cutting the Engagement Hierarchy.
  - Some claims are general ("research on motivated reasoning…") rather than sourced.
  - Its "Enron to FTX" line needs care.

**Grok Bot's view (not a decision).** Fable is the strongest base and the closest to the author's intent. Muse is a close second, and its mechanism list and practical questions are worth borrowing. Neon is the only draft that keeps the news examples, but they need correcting before any use. The author decides.
