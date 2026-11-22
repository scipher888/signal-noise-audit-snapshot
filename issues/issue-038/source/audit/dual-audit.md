# Signal & Noise, Issue 38: dual source and floor audit

*Update after publication: the rulings were confirmed on November 21, 2026, and the essays are live. The status sentences in this document were written before that and are kept as written; the author freeze published is v3 (see the ruling box).*

Prepared Nov 21, 2026 (PST) for the author's review. Both freezes are unchanged. This is a record of objections and evidence, not a validation.
- Sources: [SOURCE-LOG.md](sources/SOURCE-LOG.md). Methods: [execution-method.md](execution-method.md). Critic returns: [stage-c-synthesis.md](stage-c-synthesis.md).
- Per the author's standing request and the author's redline message ("The other issues should probably be rolled into the audit"), every factual finding is logged here, and none is applied to either text (Ruling A).

**Freezes**
- Author/AI essay (v3, refrozen Nov 21, 2026, about 9:14 PM PST, after the author's follow-up approval): `essays/author-essay-FROZEN.md`, sha256 `7fb4fac57b37dc59fd13dd94ee3dba5aad6f3d26ea8054d0e70a203c7678bdb7`, 1,066 words of body.
  - It differs from v1 only in "staffers at OpenAI" → "staffers at top AI labs".
  - v2 ("top AI lab staffers", sha256 `3587b03b33de5eb961c6c74feb93379c73cf23e95dc2c68c4d0545aaee037270`) is kept as `essays/author-essay-FROZEN-v2.md`.
  - v1 (sha256 `48d3a7271fd878c6f39eeb4e4083c68037ecb7daf3877ec9e78b0d02243554ff`) is kept as `essays/author-essay-FROZEN-v1.md`.
  - The Stage C critics reviewed v1; the one-phrase change does not affect their objections.
- Machine essay: `essays/machine-essay-FROZEN-v1.0.md`, sha256 `0a62289067f3645965fccf1cdfddf35a5f97d470cc413ca53bb3ae4188f21800`, 1,209 words of body. That is Claude Fable 5.2's output, byte-identical.

## Executive brief

**Blocking defects under the Issue 34–37 floor definition: none.** The floor means a fabricated event, quote or number. No essay invents an event or a quote. Every study the machine essay names exists, and each is characterized fairly.

**Author rulings received:** A1 was fixed narrowly in the prose (Ruling B, one phrase). A2–A8 stay in the audit (Ruling A). The original framing follows.

**Two HIGH items in the author essay needed the author's explicit ruling.** Both concern a living person or a named company, and both are misstatements of real reporting rather than fabrications:
- **A1:** the "consensual non-consent" reporting concerns an *Anthropic* researcher, not "staffers at OpenAI".
- **A2:** the essay attributes "a Chinese woman with whom he was doing business" to the Post. That is the author's wording. The Post reported "a woman suspected of being a Chinese spy".

Ruling A (keep the freeze and disclose in the audit) was the author's stated preference. A narrow Ruling B fix for A1–A4 was offered. The author took a one-phrase version of B for A1 and kept A for everything else ([RULINGS.md](../RULINGS.md)).

## 1. Author/AI essay: *The Smartest People in the Room Are the Easiest to Fool*

| ID | Essay text | Finding | Evidence | Severity |
|---|---|---|---|---|
| A1 | v3: "Recent reporting on subcultures among staffers at top AI labs—arguably home to some of the most intellectually gifted people alive—highlighted the embrace of practices like 'consensual non-consent.'" (v1 said "staffers at OpenAI"; v2 said "top AI lab staffers") | **Resolved in part by Ruling B.** The company misnaming is gone. Remaining points stay under Ruling A; see note A1. | C1–C4 | ~~HIGH~~ → LOW (resolved in part) |
| A2 | "According to the report, Huang engaged in extramarital affairs—including one with a Chinese woman with whom he was doing business." | Misattribution and omission. See note A2. | H1–H5 | **HIGH** |
| A3 | "Consider recent *Washington Post* reporting on Nvidia CEO Jensen Huang…" | Out of date: he resigned Nov 12, 2026. | H1–H3 | MEDIUM |
| A4 | "Set aside, for a moment, the obvious personal devastation infidelity inflicts on a marriage." | Speculation about a private family. The only record is Huang's own apology. | H5 | MEDIUM |
| A5 | "…invites catastrophic conflict-of-interest scrutiny." | Accurate as opinion: the scrutiny exists (Senate and House requests). It omits Nvidia's statement. Nothing shows an effect on chip sales to China. | H6 | LOW–MEDIUM |
| A6 | "Not because he lacked processing power, but because brilliance combined with invulnerability is a potent sedative." | States a mental state as fact. It is opinion; the author's source hedges ("apparently failed to recognize - or just ignored"). | — | LOW |
| A7 | "Ultra-clever communities increasingly assume…" | "Increasingly" is an unsupported trend word. The rest is opinion and fairly evokes the events' stated safe-word and "default consent" rules. | C2 | LOW |
| A8 | "Do not tear down a fence until you understand why it was built." (Muse insertion) | An unattributed paraphrase of Chesterton's principle. It is not presented as a quote, so it is acceptable. | P2 | LOW (note only) |
| A9 | Haidt paragraph ("our intellect behaves far more like a defense attorney") | Fair paraphrase of *The Righteous Mind*. | P1 | OK |
| A10 | "An ordinary person produces an excuse. A gifted person produces a philosophy." (Muse insertion) | An aphorism, opinion. The Perkins finding Haidt reports (P1) gives it partial support, though the essay doesn't cite it. | P1 | OK (opinion) |

**Note A1** (updated after the author's rulings).
- The Free Beacon report, via Sibarium on Nov 16, concerns an *Anthropic* cybersecurity researcher listed in a 2023 filing as a manager of a business that hosts "consensual non-consent" parties.
- The parties reportedly draw "a disproportionate number of employees at Anthropic and OpenAI".
- The researcher is not accused of the alleged assault. The reporting does not show that either company organized, sponsored or endorsed the events.
- Reason (Nov 18) disputes the framing.
- **What remains under Ruling A:**
  - "Subcultures among top AI lab staffers… highlighted the embrace" is the author's characterization. The reporting supports attendance by employees of two labs and one Anthropic researcher's management role, not a lab-wide "embrace".
  - v3 ("staffers at top AI labs") fixes the v2 grammar seam: "arguably home to…" again modifies the labs.

**Note A2.**
- The Post reported "two affairs, one of which included a woman suspected of being a Chinese spy".
- "Doing business" is the author's own wording. It is broadly true but past tense: her Megaspeed role ended in November 2023.
- China denies the spying claim, and the Justice Department has reached no conclusion.
- The essay omits "suspected spy" entirely.

**Argument-level objections (Stage C), not factual defects:**
- **Anecdotes without base rates.** Kimi K3 #3 and Claude Opus 4.1 #1.
- **The concession "you don't need a sky-high IQ" vs the title.** Opus #2 and Kimi #4. The excuse/philosophy insertion partly answers this.
- **Survivorship in "battle-tested residue".** Opus #5 and Kimi #6. The To-be-sure paragraph addresses aristocracy and subjugation.
- **The motive test is psychologistic or circular.** Kimi #6 and #7, Opus #4.
- **The leap from private lapses to public governance.** Kimi #8.
- **The "cognitive elite" target slides.** Kimi #10.
- **Bundled norms.** Kimi #9.
- **"Chinese woman" does suggestive work.** Kimi #2, a hygiene point folded into A2.
- **The technical/human-flourishing binary.** Opus #6.
- These are logged, and the essay is unchanged.

## 2. Machine essay: *What Intelligence Can't Tell You About Your Own Life* (full audit)

| ID | Claim | Check | Severity |
|---|---|---|---|
| M1 | Terman: "about 1,500 high-IQ California children, begun in the 1920s… by most accounts their rates of divorce, alcoholism, and suicide were close to the national average" | **Verified.** 1,528 children, from 1921. Holahan and Sears (1995) found divorce identical through midlife and suicide not different. "By most accounts" is a fair hedge. Kimi's suggestion that some accounts show lower divorce is not supported by the sources checked, so it is rejected. | OK |
| M2 | Grossmann et al.: wise reasoning predicted well-being and better relationships, "while IQ scores did not" | **Verified** (JEP: General, 2013). | OK |
| M3 | Damasio's Elliot: high IQ, emotion blunted; lost his job, invested savings against warnings, went bankrupt, divorced | **Verified.** Damasio says "against everyone's advice"; the essay's "his friends had warned him" is a fair narrowing. He divorced twice. | OK |
| M4 | The Franklin cod quote | **Verified wording** (*Autobiography*). | OK |
| M5 | Stanovich: higher ability "no better… at recognizing their own biases, and on some measures slightly worse" | **Verified** (West, Meserve and Stanovich, 2012; small positive correlations). Kimi's reading that the effect is "uniform" understates the paper, so it is rejected. | OK |
| M6 | Gilbert: speed-date surrogation | **Verified** (*Science*, 2009). Kimi's point that it is low-stakes and over-extrapolated to careers is a fair argument note. | OK / ARGUMENT |
| M7 | Grossmann and Kross, Solomon's paradox; "asking what you would advise a friend… a cheap way to get the same effect" | The study is **verified**. The advice-to-a-friend step is the essay's own extension of self-distancing, not the studied manipulation (Kimi #10). | LOW |
| M8 | Cognitive ability and longevity, earnings, accidents, delay of gratification; weak link to life satisfaction | Directionally accurate summary of a broad literature; no single study cited. | LOW |
| M9 | Affective forecasting | Accurate summary of the Wilson and Gilbert literature. | OK |

**Argument-level objections (Stage C):**
- **The emotion-as-evidence tension.** If forecasts and self-reports are unreliable, why trust dread or "how you've been sleeping"? Kimi #3 and #4, Opus #1.
- **"Mostly" in the marriage/career premise is asserted.** Kimi #7 tagged it FLOOR; the audit treats it as ARGUMENT, since it is an interpretive premise, not a factual claim.
- **The competence trap is conjectural.** Kimi #9; Opus #4 tagged it FLOOR, treated here as ARGUMENT.
- **Intelligence is conflated with prizing reason.** Kimi #6, Opus #3.
- **"Its owners tend to expect" is never shown.** Kimi #8.
- **The Terman outcomes are consistent with other explanations.** Opus #2.
- **Generalizing from one patient (Elliot).** Kimi #2.
- **Past behavior may be a poor guide.** Opus #6.
- **No floor defects.**

## 3. Integrity
- Both freezes match their sha256 hashes.
- The machine freeze is byte-identical to `development/machine-alternatives/01-claude-fable-5.2.md`, which was generated with max_tokens 48,000 and finished at 41,384 completion tokens, so the limit was not hit.
- Author freeze v1 is byte-identical to `development/revision-history/neon-clean-v2.md`. Its diff against Neon's essay shows exactly two insertions, both verbatim from Muse Wonder.
- The current freeze (v3) differs from v1 in one phrase only (`development/revision-history/freeze-v1-to-v2.diff`, `freeze-v2-to-v3.diff`).
