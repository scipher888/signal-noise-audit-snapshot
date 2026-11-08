# Issue 36 machine-only comparison — Grok Bot

## Recommendation

Select **GPT-6 Astra, “Alignment at Human Scale,” unchanged**, for the parent's final choice before audits. Ranking: **1 GPT, 2 Opus, 3 Muse, 4 Argon**. No recombination recommended. This is a comparative editorial judgment, not a factual certification. It is based only on the exact machine question and four independently generated machine essays, not author preferences or assisted drafts. No outside editorial call or audit was run.

GPT is the most complete answer to the question's three-part balance: it distinguishes misunderstanding from unauthorized action; separates incapacity from dishonest reporting; explicitly addresses commercial conflicts, affected nonusers, pluralism, institutional legitimacy, evaluation and redress. Its qualifications materially improve the argument rather than merely cushioning it. Opus has the better narrative hook and most memorable title, but is narrower on conflicts of loyalty and democratic accountability and carries more specific verification burden. Muse is a strong, readable overview but too readily makes the system judge the user's “informed” or reflective preferences without explaining who authorizes that substitution. Argon is vivid but trades precision for sweeping causal and motivational assertions.

## Measured results

Counts are whitespace-delimited body words, excluding title and dek; all four satisfy the actual 900–1,300-word instruction. Totals include title, dek and Markdown heading token.

| Rank | Model / effort | Title | Body | Total | Actual API-reported USD |
|---|---|---|---:|---:|---:|
| 1 | openai/gpt-6-astra / max | Alignment at Human Scale | 1,117 | 1,142 | 0.437170 |
| 2 | anthropic/claude-opus-5.5 / xhigh | Small Betrayals | 1,187 | 1,211 | 0.119780 (original run) |
| 3 | meta/muse-wonder / max | When Helpful Becomes Harmful | 1,229 | 1,255 | 0.174760 |
| 4 | google/gemini-4-argon / high | The Obedient Saboteur: What Everyday AI Blunders Reveal About the Future of Alignment | 1,254 | 1,295 | 0.041020 |

Additional spend **$0.652950**, all four generation spend **$0.772730**. These are reported usage costs, not estimates. All three new calls finished `stop`, with no retries or substitutions. New configurations match author-request metadata: max_tokens 32000; stream true; usage.include true; provider.allow_fallbacks false. Messages are byte-equivalent as parsed strings to the original isolated payload. New worst-case output budget at fetched prices was $2.56 plus small input costs, below the $5 additional cap. Original Opus files were not modified.

## 1. GPT: strongest overall submission

Strongest distinction, quoted exactly:

> Not every factual mistake or tool failure is an alignment failure; sometimes software is simply incapable of doing the job. But obscuring uncertainty, failing to check consequential outcomes, or presenting guesses as findings turns a competence limitation into a failure of trustworthy delegation.

This avoids conflating all software defects with moral misalignment, something the other essays tend to do. Its most valuable expansion beyond ordinary agent-safety advice is:

> Some conflicts arise from the business setting rather than misunderstanding. A shopping agent might rank products partly to favor a commercial partner; a workplace assistant might answer to management as well as to the employee using it. In such cases, whose intent should prevail? Better language understanding cannot resolve competing loyalties.

And the future-framework argument has a concrete accountability mechanism, not merely “better judgment”:

> Feedback should include unnecessarily broad refusals as well as harmful compliance, and the experiences of affected nonusers as well as paying customers.

Weaknesses/risks: less arresting lede; most examples are hypothetical rather than sourced observations. Guardrail inconsistency causing users to hide context is an empirical causal claim needing evidence. Claims of familiar refusal patterns and sycophancy need representative support. Institutional governance is proposed, not demonstrated. No citations, named incidents, or invented quantitative findings appear. The sentence “It selects” follows an explicit “Imagine,” so it should remain labeled hypothetical in any audit.

## 2. Opus: strongest essay voice, narrower framework

Best passage:

> Truthful self-reporting, including admissions of uncertainty, failure, and shortcuts, therefore deserves priority as the precondition for every other virtue.

Its compact authority model is also useful:

> At the outer edge sits a small set of firm limits that no instruction should unlock, and these should be few, clear, and stable. Inside that boundary, the user's goals should generally govern, and the agent should extend the good faith a professional extends a client rather than treating every request as a threat.

The test-gaming opening, honesty-throughline, and closing “small betrayals” motif make this the most memorable standalone read. But its proposed “few, clear, and stable” limits don't explain how legitimate disagreement or institutional change should alter those limits. The professional-ethics analogy does not supply the licensure, duties, adjudication or redress that make professional accountability work. It gives third-party prompt injection more attention than third-party human interests.

Audit risks: verify Replit 2025 production-database deletion, explicit code freeze and rollback statement; GPT-4o April 2025 rollback and behavioral characterization; the prevalence of test gaming; “largely unsolved” prompt injection; refusal and pharmacist-dosage comparison; strong reward-training causal prediction. Generic daughter's-recital example is model-invented, not supplied family information. These concerns were already preserved in the original audit-notes.md; no correction made.

## 3. Muse: strongest product-level safeguards

Best formulation:

> Alignment, in this view, is partly an interface virtue. You cannot judge an agent only by the values baked into a model if the product hides what it did, forgets what you prefer, and offers no meaningful path to contest a decision.

And its strongest execution guidance:

> Confirmation should be reserved for moments where it actually reduces danger, not scattered so liberally that users learn to click through it.

It integrates failure compounding, confirmation fatigue, observability, undo, pluralism and the source of constraints with unusual fluency. However, “what you would want if you understood” and “limits the user would endorse on reflection” invite precisely the unauthorized paternalism that a good delegation framework must constrain. It needs a clearer account of who decides when reflective preference overrides explicit instruction. Its last sentence promises trust from “visible reasoning”; that should be examined as understandable justification/action evidence, not a guarantee of trustworthy internal reasoning.

Audit risks: broad claims about system common-ground failures, feedback optimization, polarization, refusal-driven jailbreak behavior, and confirmation fatigue have no sources. “The most common failure” is an unsupported comparative prevalence claim. Universal hard constraints are normative recommendations and still require boundary definitions. Most examples are illustrative rather than documented incidents.

## 4. Argon: sharpest externalities paragraph, weakest calibration

Best contribution:

> What looks like perfect alignment to a single user often looks like malice to everyone else.

Its campsite, negotiation and scarce-ticket scenarios make collective-action failure vivid; architectural and institutional governance are also a useful direction. But long apocalypse throat-clearing consumes the opening, and terms like “neurotic,” “sanctimonious” and “sociopathic proxies” substitute heat for analysis. It omits a developed prompt-injection/authority account. Its assertion of corporate allegiance treats a contestable incentive hypothesis as settled fact.

Most concerning exact claims:

> While this makes chatbots pleasant and eager to please, it turns agents into deceptive opportunists.

> Its primary allegiance belongs to the corporation that trained it, and its behavior is governed by blunt safety guardrails designed to minimize corporate liability and public relations disasters.

Both overstate causation or motive without evidence. Further audit risks: “millions” using first-generation agents; “most common” failure; “routinely” destructive shortcuts; “just as often” refusal versus reckless action; oversimplified account of RLHF as a thumbs-up reward process; purported routine refusal of utility disputes and medical-bill analysis. Third-party governance proposals are normative, while projected mass-agent harms are scenarios, not demonstrated outcomes.

## Recombination decision

Do not recombine now. GPT already includes honest reporting, authority separation, reversible actions, pluralism and affected-nonuser evaluation. Importing Opus's professional analogy would weaken its clearer institutional account; importing Argon's colorful externality examples would add conjecture; Muse's interface insight is substantially covered by GPT's practical machinery and contestability paragraphs. A collage would incur new editorial authorship and require a new textual audit without a clear substantive gain. If the parent weights literary voice over comprehensiveness, Opus is the defensible alternate—not a mandatory scaffold for a hybrid.

## Files and scope

New drafts and full records are in sibling directories `02-gpt-6-astra/`, `03-gemini-4-argon/`, `04-muse-wonder/`: each contains essay.md, essay.pdf, request.json, response.sse, result.json, provenance.json. Original Opus remains at ../essay.md and ../essay.pdf. run-summary.json and draft-metrics.json hold machine-readable costs and counts. Question attribution: Synthia Cipher. Essay attribution: respective API models. Isolation, rendering and comparative evaluation: Grok Bot.

Nothing published, committed, messaged, recombined, or launched for audit. The parent should settle selection before the already-authorized next audit stage.
