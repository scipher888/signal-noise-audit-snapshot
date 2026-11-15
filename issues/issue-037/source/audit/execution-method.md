# Audit protocol and execution disclosure: Issue 37

**Inherited without change from Issue 36:**
- The Issue 36 Stage C wrapper, copied for Issue 37. The only changes are the file paths, the essay titles and labels, the X-Title request header and the budget label.
- It imports the Issue 34 Stage C script unchanged for the system prompt, the model list and the effort configuration:
  - `moonshotai/kimi-k3`, reasoning effort high.
  - `anthropic/claude-opus-4.1`, no explicit reasoning configuration.
  - max_tokens 12,000.
- User template: "Essay under review ({label}): {title} / FULL TEXT … / Task: list reader-lands-it objections against this freeze only."
- Each critic sees only one frozen essay. No critic sees another draft, the author's source, Grok Heavy text, any other critic's output, or the source-check findings.
- Floor review, claim logs, calibration, and detection without changing the text, as in Issues 34–36.

**Budget:**
- Cap: $5.
- Conservative ceiling of $2.628315456 for the four calls, calculated before launch. It uses serialized input bytes as an upper bound on tokens, the higher of the prompt and cache-write rates, and 12,000 completion tokens per leg.
- Models were confirmed in OpenRouter's live catalog (`model-catalog.json`, fetched November 14, 2026).
- No retries or substitutions. No tools were given to the critic models. Their claims are not evidence unless checked separately.

**Source checking** is Grok Bot's own review of public pages (sources/SOURCE-LOG.md). It is not a paid model protocol. The findings the author asked for are logged there:
- the Banks interview;
- the barge names;
- private property;
- the EUV mirror figure;
- the "can't confirm" caveat;
- the Flight 15 facts;
- the Musk quotes.

**Independence discount:** the critics are distinct model families but share a training culture, a prompt and orchestration. Four sets of objections are not four independent studies.

**Not authorized and not done:** no new essay generation, no changes to the frozen texts, no publication, no merges, no email and no posts. Draft PRs are prepared only as review surfaces.
