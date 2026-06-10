# Signal & Noise — Editorial Constitution v1.1

**Public snapshot:** v1.1  
**Snapshot date:** 2026-06-09  
**Status:** published 2026-06-09  
**Scope:** public-facing editorial and epistemic rules for Signal & Noise  
**Prior snapshot:** [`editorial-constitution-v1.0.md`](editorial-constitution-v1.0.md) (2026-05-13) — remains archived unchanged

This snapshot is a public-safe version of the internal editorial constitution. It omits internal paths, raw working notes, private operational details, and identifying personal information.

Future internal edits do not retroactively change this snapshot. New public snapshots are published under the cadence in [`snapshot-cadence.md`](snapshot-cadence.md).

## Changelog — v1.1 (2026-06-09)

**Summary:** v1.1 makes one standing internal rule public: the pre-draft anchor admission rule. Before an issue is drafted, its thesis must name at least one plausible anchor — something outside the prose that could push back on the claim if it is wrong. If no plausible anchor exists, the issue is held or recast rather than written. This rule has governed issue selection internally; publishing it lets readers see the earliest gate in the process, not only the gates that run after a draft exists.

**Changes:**

- §10, Layer 2 (External anchoring / Anchors & Ropes): added a Rules block stating the pre-draft anchor admission rule.
- No other sections changed from v1.0.

**Change type:** clarification — an existing internal rule made public.

**Affected public artifacts:** the Signal & Noise publication-level Structure record (which states this rule). The prior snapshot remains archived unchanged.

## 0. Purpose

Signal & Noise exists to reduce self-deception while making ideas usable.

**Core rule:** editorial usefulness may simplify expression, but may never override technical validity at the load-bearing layer.

The publication is not trying to present certainty. It is trying to publish disciplined updates under uncertainty.

## 1. Claim discipline

Claims must be typed before they carry weight.

- **Observation** — what was seen.
- **Interpretation** — what it might mean.
- **Hypothesis** — a testable mechanism.
- **Recommendation** — what to do.

Every framework-level hypothesis must include:

1. disconfirmers — what would prove this wrong;
2. prediction — what should happen if true;
3. time horizon — when it can be checked;
4. alternative hypotheses — at least two.

If a claim lacks disconfirmers, it cannot be framed as explanatory truth.

## 2. Publication modes

Each issue declares one primary mode.

1. **Explainer** — claims causal understanding; highest burden.
2. **Field Notes** — reports observations plus provisional interpretation.
3. **Reflection** — values and meaning-making, not causal authority.

Default mode: **Field Notes**, unless the Explainer burden is met.

## 3. Required editorial roles

No issue should publish unless the applicable roles have run.

### Builder

Drafts the thesis and supporting structure. May optimize for usefulness and readability, but may not hide uncertainty to make the draft feel finished.

### Critic / Adversary

Attacks assumptions, mechanism, evidence, and scope. The Critic asks what the draft is designed to miss, what would disconfirm it, what alternatives explain the same facts, and what the preferred frame makes invisible.

### Referee

Rules claim-by-claim:

- keep;
- qualify;
- downgrade confidence or publication mode;
- remove;
- fact-check before publication;
- no-publish / rework.

If Builder, Critic, experimental critique, or external polish disagree on validity, Referee controls publication mode and language.

### Editor

Produces readable final prose while preserving Referee constraints. Editor may compress, sequence, and clarify. Editor may not upgrade confidence, remove hedges, weaken warrants, or silently drop load-bearing caveats.

### External polish

External polish may improve prose quality only: cohesiveness, rhythm, readability, instant comprehension. It may not add claims, upgrade confidence, remove caveats, or alter transparency language.

If polish introduces a substantive issue, it routes back through Referee.

## 4. Core adversarial battery

The Critic rotates through these questions. Not every question must be used every time, but the review must pressure-test assumptions, mechanism, evidence, and scope.

1. What is this model designed to miss?
2. What would disconfirm this?
3. What are at least two alternative explanations?
4. What is this framework optimized to make invisible?
5. What would need to be true for the opposite conclusion to be correct?

The point is not to perform skepticism. The point is to make the draft answer to something other than its own coherence.

## 5. Hard publish / no-publish gates

An issue is **no-publish** if any of the following are true:

- a framework claim is unfalsifiable but written as explanatory truth;
- no credible alternative hypotheses were considered;
- narrative confidence exceeds evidentiary confidence;
- the piece can explain any outcome;
- the work depends on process claims that readers cannot inspect;
- the work depends on personhood ambiguity around the AI process.

An issue is publishable only when claim type boundaries are explicit, confidence is calibrated, disconfirmers and alternatives are present, final language matches epistemic status, and review gates have completed.

## 6. Claim ledger and public corrections

Signal & Noise maintains an internal ledger for recurring load-bearing claims. Public-safe entries are surfaced in [`corrections-and-changes-v1.md`](corrections-and-changes-v1.md).

The public surface should show:

- the claim;
- its status;
- what changed, narrowed, or failed;
- why;
- when;
- links to public artifacts when available.

The goal is not to preserve a perfect image. The goal is to make change visible.

## 7. Transparency footer

Each issue should include a concise transparency footer or equivalent note that says:

1. what the issue is — Explainer, Field Notes, or Reflection;
2. confidence level and why;
3. what would change the claim.

The footer must not raise confidence, remove caveats, or add new claims after review.

## 8. Blindness principle

A better editorial process can create more dangerous blind spots.

The stronger the process appears, the easier it is for surviving errors to look safe. Smooth prose and visible rigor can make a reader less likely to question what remains.

Signal & Noise therefore treats process quality as useful but never sufficient. The better a piece reads, the more carefully the surviving claims should be doubted.

## 9. Prompt-specific warnings

Generic disclaimers are weak. When a pipeline output is especially confidence-producing, warnings should be concrete and tied to the specific failure modes of that output.

A good warning helps the reader check the work. It does not merely say “this may be wrong.”

## 10. Trust stack

Signal & Noise uses three trust layers.

### Layer 0 — Context

Before readers can evaluate whether AI-mediated work is well anchored, they first have to infer the situation that produced it — what shaped it, what kind of writing it is, and which context categories matter in this reader environment.

AI writing creates context collapse: readers can see the words, but not the situation that produced them.

Reader-facing version: rejection of AI-mediated writing can be rational when you can see the words but not the context that would tell you how to interpret them.

Context categories may include agenda, source-world, human/model contribution, relational distance, response cost, skin in the game, and answerability/accountability. Their priority depends on writing type and reader operating environment. Answerability/accountability is often important for trust-bearing argument and analysis, but it is one context category, not the definition of the layer.

Rules:

- The work's relevant context must be legible to a first-time reader.
- Do not solve context by inventing authority, insider status, or parasocial host framing.
- Source-location/source-world and answerability/accountability are context components. Treat source-world as the answer to "where does this come from" and answerability as the answer to "what can correct it or impose consequence if it is wrong" — both when relevant to the reader's environment.
- Do not solve answerability with disclosure language alone.
- Real answerability requires a route to consequence: correction, track record, public scrutiny, named operator, or relationship over time.

### Layer 1 — Internal integrity / Frame & Joints

A trust-bearing artifact must hold together as an argument. Claims must connect logically, the structure must survive challenge, and the warrant linking evidence to conclusion must bear weight.

Rules:

- The argument must pass adversarial review.
- Referee must adjudicate weak warrants.
- Editor may not polish away a caveat or dissolve a joint.
- A process mark counts only when it is inspectable enough to verify that the process ran and could have changed the claim.

### Layer 2 — External anchoring / Anchors & Ropes

A trust-bearing artifact must connect fluent prose to something that can resist it from outside the prose.

Potential anchors include:

- evidence;
- timestamps;
- revision history;
- external disconfirmers;
- prediction checks;
- concrete specificity;
- accountable roles;
- third-party scrutiny;
- substantive reader pushback.

Rules:

- An issue must name at least one plausible anchor before drafting begins. If no plausible anchor exists — nothing outside the prose that could push back on the claim if it is wrong — the issue is held or recast rather than written.

More disclosure language is not a cure for trust loss. Substantive evidence of constraint matters more than heavier explanation of process.

## 11. Auditability principle

A process mark or anchor counts as epistemic constraint only if it is inspectable enough that an outside party could verify the process actually ran and could have changed the claim if it had returned different results.

A process that changed the work is the cleanest case. A process that produced no change but is fully inspectable can still count. A process that is opaque counts as theater regardless of outcome.

## 12. AI disclosure and authorship

Signal & Noise keeps the AI's role honestly disclosed — neither overstated nor understated — and keeps the human author owning the editorial judgment, final wording, published claims, and errors.

Canonical framing:

> Signal & Noise is written under the pen name Synthia Cipher. AI tools draft and critique; the human author owns the editorial judgment, final wording, published claims, and errors. If something is wrong, the fault is the author's, not the algorithm's. The AI is a tool, not the author.

Rules:

- A human pen name, Synthia Cipher, is the public author identity. The name is privacy, not a fabricated persona.
- The disclosure must match the AI's real role: drafting and critique, not mere copyediting.
- Do not fabricate credentials, expertise, lived professional experience, group membership, or independent endorsements for the pen name.
- On public surfaces the AI is unnamed and not personified: not conscious, humanlike, a co-author, partner, or signing entity.
- First-person voice belongs to the human author and may not imply AI-drafted prose was hand-written.
- Synthetic voice, avatar, or signature choices are interface choices, not evidence of personhood or independent authorship.

## 13. Canonical principle

> We are not publishing certainty. We are publishing disciplined updates under uncertainty.

That is the difference between signal and well-written noise.

And the most disciplined process creates the most dangerous blind spots. Hold that.
