# Signal & Noise — Issue 37: development record

Prepared November 14, 2026 (PST). This is a record of decisions and runs, not a full conversation transcript. All times are in PST. Cost figures are what OpenRouter reported for each API call, not a reconciled card statement.

## 1. Source and instructions (owner message t292u, about 8:20 PM)

The author sent the issue's source material in one message. It combined the author's raw brain dump with research the author produced using Grok Heavy, and it gave the author's own designation of which passages were the author's own:

> only these parts "The successful capture of Starship Fight 15 is the #1 greatest engineering achievement of all time" and "For context, I would rank the following to round out the top 5 achievements:" and "But who cares? What does proof of concept of fully reusable large payload spaceships of imply about your future? I'm so glad you asked." and "In short, Elon Musk has repeatedly told audiences to read Ian Banks culture series. …" are from my raw brain dump. Everything else is from my research with Grok Heavy

The author asked that the source be published where the human-only page usually goes, with the author's text visually separated from Grok Heavy's. The message also included the ruthless op-ed editorial prompt (800–1,200 words), the four author-assist models, and the two machine questions. The message called this "Issue 36"; because Issue 36 had already been published, it was filed as Issue 37. The source is preserved byte-for-byte, typos included. One caveat: the relay may have changed the number of blank lines between paragraphs .

## 2. Author-assist drafts (8:2x PM)

The four models received the identical submitted prompt: the editorial prompt verbatim, with the mixed source in place of the placeholder ([submitted-prompt.md](submitted-prompt.md)). Each request was a single isolated turn, with no tools, no fallbacks, max_tokens 32,000 and no retries.

| Model (reasoning) | Title | Words | Cost (USD) |
|---|---|---:|---:|
| Claude Fable 5.2 (max) | Musk's Blueprint Is Shelved Under Science Fiction | 929 | 1.270520 |
| GPT-6 Astra (max) | Starship's Real Test Isn't the Catch | 903 | 0.984643 |
| Gemini 4 Carbon (high) | What SpaceX Caught in Those Mechanical Arms Is Bigger Than a Rocket | 980 | 0.085188 |
| Muse Wonder (max) | Catching a Rocket Is the First Step Toward a Post-Scarcity World | 899 | 0.109564 |
| **Subtotal** | | | **2.449915** |

All four drafts and their full outputs, including each model's thesis, pressure-test and outline steps, are in the [author alternatives](#author-fable) section of the development record. The comparison is in [author-comparison.md](author-comparison.md). Cautions logged before selection:
- Muse Wonder's lede describes a *booster* catch. On Flight 15 the booster catch was aborted; the ship was the stage that was caught.
- Gemini Carbon claims "full, two-stage reusability" was demonstrated.
- Fable opens by saying it cannot confirm the flight, and ends with its own "verify before filing" list.

## 3. Machine-only essay runs (8:27–8:40 PM)

The prompt was the author's two questions, verbatim with typos, plus a format paragraph: 900–1,300 words, a title and a one-line dek, no headers or lists. Under the author's further instruction (t293u), the ranking had to include only the top five, and Flight 15's rank had to be stated if it fell outside them ([machine-question.md](machine-question.md)). Each request was one message, with no system prompt and no tools. None of the runs received the brain dump, Grok Heavy text, editorial prompt or drafts ([isolation.json](../metadata/isolation.json)).

| Run | Result | Flight 15 rank | Words | Cost (USD) |
|---|---|---|---:|---:|
| Claude Fable 5.2 (max), attempt 1, max_tokens 32,000 | **Failed.** `finish_reason: length`; all 32,000 tokens went to reasoning, so there was no essay | — | — | 1.282784 |
| Claude Fable 5.2 (max), attempt 2: identical message, max_tokens 64,000 | "Where the Starship Catch Ranks, and What It Could Change" | 6th | 1,192 | 1.879704 |
| Gemini 4 Carbon (high) | "Catching Fire, Opening the Sky" | 7th (lists five) | 1,143 | 0.159456 |
| GPT-6 Astra (max) | "What a Starship Catch Could Change" | 6th | 1,073 | 0.718110 |
| Muse Wonder (max) | "Catching the Future" | 6th | 1,112 | 0.167556 |
| **Subtotal (cap $5)** | | | | **4.207610** |

The single retry is disclosed. It used the same message and settings as the first attempt; only the token ceiling was raised. Both attempts are recorded.

**Selection (Grok Bot, under the author's delegation, t293u):** Claude Fable 5.2, attempt 2, **unchanged and not combined.** It states its ranking test plainly and gives two concrete reasons the catch sits below the top five. It also says what would move it up, and it has the most concrete 10/25/50/100-year arc with cost figures a reader can check. Muse Wonder was a close second. GPT-6 Astra was the most careful but read like a hedged memo. Gemini 4 Carbon invented event details and ranked the flight seventh while listing only five achievements. Full reasoning is in [machine-comparison.md](machine-comparison.md).

The author said the "can't confirm the flight" admission could be dropped but left the call to the editor. The machine text stays unchanged. A separate editorial note confirms the flight with a link.

## 4. Author essay: selection and revision history

1. **Choice (owner message, November 14).** The author picked **Claude Fable 5.2** for the human/AI essay, with Muse second. The author's reason: it "brilliantly incorporates parts of the culture series" and hints at why readers might explore the books. Instructions:
   - Use **Gemini 4 Carbon's title**.
   - Fix the passage about the "awkward fact… Culture has no billionaires… libertarian admirers." The author's view: Musk aims for a post-monetary society, so the point is not awkward from Musk's side. Either revise it or replace it with "to be sure" material from the other drafts.
2. **Options presented** (tracked PDF [ISSUE-037-revision-options-tracked.pdf](revision-history/ISSUE-037-revision-options-tracked.pdf)):
   - **A** (972 words): rewrite the passage with a verified Musk quote, "money 'will stop being relevant'."
   - **B** (954 words): replace it with sentences from Fable, Muse and Astra about the Shuttle and heat-shield reuse.
   - A fact check of the rest of the essay was attached.
3. **Author's direction (t295u, verbatim):**

   > The fact checks are great, but let's keep the fact checks in the audit (for readability sake). So let's keep this: "To some, there is an awkward fact at the center of his enthusiasm. The Culture has no billionaires. Banks himself wondered aloud how his libertarian admirers had managed to miss that his paradise abolished private property."  And perhaps this "Musk, though, has not missed it. He predicts that, with enough AI and robotics, money "will stop being relevant." In a civilization so rich that money has withered away, nobody is a billionaire, and nobody needs to be." needs to go in the following (new?) paragraph since I don't think is fits cleanly in the "To be sure" paragraph.

   Applied as **Option C** (968 words): Fable's original sentences kept, "And there is" changed to "To some, there is," and the Musk lines moved into a new paragraph after "To be sure" ([option-C.diff](revision-history/option-C.diff)).
4. **Final tweak (t296u, verbatim):**

   > Yeah, I noticed that one small thing too. Could we say "And the remaining objections strengthen the case"

   Applied, and the author essay was then **frozen at 970 words**, SHA256 `dd517c993bd5058218c6ef1fb243df141b2d7a0853e12b89261bad59e762babd`.
5. **t297u:** "Excellent. Please proceed." This authorized the audits, the source page and the editorial note. It did not authorize publication.

These are all the differences from Fable's draft:
- the title;
- "To some, there is";
- the new two-sentence-plus paragraph quoting Musk;
- "And the remaining objections strengthen the case."

Everything else is Fable 5.2 verbatim.

## 5. Machine freeze

[machine-essay-FROZEN-v1.0.md](../essays/machine-essay-FROZEN-v1.0.md), SHA256 `f6544821668c6f85880a3bd9dde5659ed1a7450617158261addd166ad85f5a64`. It is byte-identical to the model output and was frozen November 14 at about 10:25 PM.

## 6. Audit (Stage C)

Four calls under the unchanged Issue 34–36 protocol: Kimi K3 (reasoning high) and Claude Opus 4.1, each critic seeing one frozen essay. The cap was $5. **Reported cost: $0.365082.** There were no retries. Dispositions are in [stage-c-synthesis.md](../audit/stage-c-synthesis.md).

## 7. Cost ledger

| Stage | USD |
|---|---:|
| Author-assist drafts (4 calls) | 2.449915 |
| Machine runs (5 calls, including the failed Fable attempt at $1.282784) | 4.207610 |
| Stage C critique (4 calls) | 0.365082 |
| **Issue 37 total reported** | **7.0226065** |

Each stage stayed under its own $5 cap. Source checking, comparison, revision drafting and synthesis were done by Grok Bot and made no paid model calls.

## 8. Coverage and gaps

- Owner messages t292u (the attribution excerpt and the machine questions), t295u, t296u, t297u and t298u are quoted verbatim from the session.
- t293u and the author's Fable-selection message are described from the session record, not quoted. Their exact text is not reproduced here.
- Assistant timestamps are approximate.
- Hidden or internal reasoning is excluded.

## 9. After publication

- **t298u (verbatim), November 14, after the 10:40 PM merges:** "Merged, and Confirming you’ve marked the correct passages as mine in the source page preview." This confirmed the source page's attribution: the highlighted passages are the author's, and the rest is Grok Heavy research.
