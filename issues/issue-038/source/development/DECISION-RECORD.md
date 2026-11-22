# Signal & Noise — Issue 38: development record

Prepared November 21, 2026 (PST) for the author's review. This is a record of decisions and runs, not a full conversation transcript. All times are PST. Cost figures are what OpenRouter reported for each API call, not a reconciled card statement.

## 1. Source and instructions (owner message t318u, about 4:20 PM)

The author sent a raw brain dump, two X links, a link to a private document, the ruthless op-ed editorial prompt, the four author-assist models and the machine question. On the source, the author wrote:

> my brain dump is even more random, unorganized, and haphazard than usual, and it’s based almost entirely on intuition since I haven’t done the research to prove or disprove any of this.

All of the source is the author's own writing; no AI research text is mixed in. It is published as [source-material-PUBLIC.md](../essays/source-material-PUBLIC.md), verbatim except for two changes the author approved (t326u): the private link is replaced by "[private link removed]", and tracking parameters are removed from the two X links. The same two changes are applied to the public copies of the submitted prompt and the request records. The models received the original links, but they had no tools and could not open them.

## 2. Author-assist drafts (4:26–4:36 PM)

The four models received the identical submitted prompt: the editorial prompt verbatim, with the brain dump in place of the placeholder ([submitted-prompt.md](submitted-prompt.md)). Each request was a single isolated turn (word counts are draft bodies, excluding the title), with no tools and no fallbacks. Claude Fable 5.2 had max_tokens 48,000, because Issue 37's Fable machine run ran out at 32,000; the others had 32,000. No retries were needed.

| Model (reasoning) | Title | Words | Cost (USD) |
|---|---|---:|---:|
| Claude Fable 5.2 (max) | Smart Enough to Fool Yourself | 1,005 | 1.169816 |
| GPT-6.2 Astra (max) | You Can Be Right and Still Be the Wrong Person to Decide | 840 | 0.990544 |
| Gemini 4 Neon (xhigh) | The Smartest People in the Room Are the Easiest to Fool | 1,015 | 0.191217 |
| Muse Wonder (max) | Smart Enough to Fool Yourself | 925 | 0.128936 |
| **Subtotal** | | | **2.480513** |

The comparison, written before selection, is in [author-comparison.md](author-comparison.md). It flagged the Huang and "consensual non-consent" claims for fact-checking.

## 3. Machine-only essay runs (4:26–4:36 PM)

The machine prompt is the author's question verbatim plus the Issue 37 format paragraph, without the ranking sentence ([machine-question.md](machine-question.md)). It was one message, with no system prompt, no tools, no brain dump, no X posts and no drafts ([isolation record](../metadata/isolation.json)).

| Model (reasoning) | Title | Words | Cost (USD) |
|---|---|---:|---:|
| Claude Fable 5.2 (max) | What Intelligence Can't Tell You About Your Own Life | 1,209 | 1.656800 |
| GPT-6.2 Astra (max) | After the Congratulations | 1,017 | 0.553296 |
| Gemini 4 Neon (xhigh) | The Art of Not Outsmarting Yourself | 1,155 | 0.192954 |
| Muse Wonder (max) | The Amplifier Without a Compass | 1,216 | 0.143924 |
| **Subtotal** | | | **2.546974** |

Grok Bot recommended Claude Fable 5.2 unchanged ([machine-comparison.md](machine-comparison.md)).

## 4. Selection and revisions (8:28–8:57 PM)

- **t320u, about 8:28 PM:** the author chose Gemini 4 Neon's draft as the base. Excerpt: "the Gemini article is the only one that includes the culturally relevant Huang and consensual non consent references that are “hot topics” today, and although the riskiest, is also closest to what I want to say". The author asked whether anything from the other drafts should be folded in.
- **Integration memo:** Grok Bot ranked short passages from Fable, Muse and Astra that could patch Neon's weak spots, and listed factual corrections ([integration-recommendations.md](revision-history/integration-recommendations.md)).
- **t321u, about 8:36 PM:** "can I see a redlined version with the 5 short priced (from the other models) folded in? So I can see how they land? The other issues should probably be rolled into the audit imo." Redline v1, with five additions: [redline-v1-five-additions.pdf](revision-history/redline-v1-five-additions.pdf).
- **t322u, about 8:54 PM** (described, not verbatim): the author kept only the two Muse additions, in place, and reverted the rest. Redline v2: [redline-v2-two-muse-additions.pdf](revision-history/redline-v2-two-muse-additions.pdf). The clean text is [neon-clean-v2.md](revision-history/neon-clean-v2.md). Its diff against [Neon's draft as returned](revision-history/neon-draft-as-returned.md) shows exactly those two insertions.
- **t323u, about 8:57 PM:** "Yes". The author approved freezing v2 as the author essay and Fable as the machine essay.

## 5. Freezes

- **Author essay v1**, about 8:58 PM: sha256 `48d3a7271fd878c6f39eeb4e4083c68037ecb7daf3877ec9e78b0d02243554ff`, 1,064 words of body. This is the text the Stage C critics reviewed.
- **Machine essay**, about 8:58 PM: sha256 `0a62289067f3645965fccf1cdfddf35a5f97d470cc413ca53bb3ae4188f21800`, byte-identical to the Fable output.
- **Author essay v2** (t326u, about 9:11 PM; described): "staffers at OpenAI" became "top AI lab staffers", sha256 `3587b03b33de5eb961c6c74feb93379c73cf23e95dc2c68c4d0545aaee037270`.
- **Author essay v3** (t326s2085, about 9:14 PM; described): "top AI lab staffers" became "staffers at top AI labs", which fixed the grammar seam. sha256 `7fb4fac57b37dc59fd13dd94ee3dba5aad6f3d26ea8054d0e70a203c7678bdb7`, 1,066 words of body. This is the current freeze.
- Diffs: [freeze-v1-to-v2.diff](revision-history/freeze-v1-to-v2.diff), [freeze-v2-to-v3.diff](revision-history/freeze-v2-to-v3.diff).

## 6. Audit (8:58–8:59 PM)

Stage C used the Issue 37 protocol: Kimi K3 (high) and Claude Opus 4.1, one freeze each, four calls, $0.256914, no retries. Grok Bot did the source checks. The findings are in [dual-audit.md](../audit/dual-audit.md), and the rulings in [RULINGS.md](../RULINGS.md).

## 7. Cost

API-reported total for the issue: **$5.284401**, made up of $2.480513 (author-assist), $2.546974 (machine) and $0.256914 (Stage C). The per-call ledger is [costs.json](../metadata/costs.json).
