# Audit protocol and execution disclosure: Issue 38

**Inherited without change from Issue 37:**
- The Stage C wrapper is a copy of Issue 37's. Only the paths, the essay titles, the X-Title header and the budget label changed.
- It imports the Issue 34 Stage C script unchanged for:
  - the system prompt;
  - the models: `moonshotai/kimi-k3` with reasoning effort high, and `anthropic/claude-opus-4.1` with no reasoning configuration;
  - max_tokens 12,000.
- Each critic saw only one frozen essay. No critic saw another draft, the author's source, the X posts, another critic's output, or the source-check findings.

**Budget**
- Cap: $5. The conservative pre-launch ceiling was $2.6824 (serialized input bytes, the higher input rate, and 12,000 completion tokens per leg).
- Models were confirmed in the live OpenRouter catalog (fetched Nov 21, 2026).
- There were no retries and no substitutions, and the critics had no tools.
- **Reported cost: $0.256914.**

**Source checking** was Grok Bot's own review of public pages and of the X posts read with the X read tool (sources/SOURCE-LOG.md). It is not a paid model protocol.

**Ruling A:** fact checks stay in the audit, not the essays, as the author asked (Issue 37 standing preference; t321u for Issue 38).

**Not done during the audit:** no new essay generation, no changes to the freezes, no publication, no audio and no sends.

**After the audit:** the author changed one phrase in the author essay twice ("staffers at OpenAI" → "top AI lab staffers" → "staffers at top AI labs"). The critics reviewed v1 (sha256 `48d3a727…`). The change touches only finding A1 and does not affect their objections.
