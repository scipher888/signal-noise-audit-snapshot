# Stage C — machine-leg-a-kimi-k3

## Objections

**1. The opening example smuggles in its verdict**
- *Quote:* "It selects an overnight itinerary with two connections and a nonrefundable fare. The price is low; the plan is miserable."
- *Objection:* The user asked for the "cheapest workable trip," and the essay never establishes that the chosen itinerary failed "workable." Overnight, multi-connection, nonrefundable travel is how millions of budget travelers actually fly. The example only works if the reader already accepts the essay's conclusion—that the agent mistook the measurable for the meaningful—rather than demonstrating it.
- *Why it lands:* This is the load-bearing image for the entire frame ("confusing expressed instructions with underlying intent"). A careful reader notices the essay needed a case where the agent clearly erred and instead gave one where the agent arguably complied, then asserted misery as fact. The real phenomenon (specification underdetermination) is real, but this instance doesn't exhibit it cleanly.
- *Severity:* ARGUMENT

**2. "Proportional to the stakes" is a restatement of the problem, not a solution**
- *Quote:* "Clarification should be proportional to the stakes: choosing a document's font is not like submitting a tax return."
- *Objection:* Judging the stakes of an action is itself the judgment whose absence causes the failures the essay catalogs. An agent that can reliably distinguish font-level from tax-return-level stakes has already solved most of the alignment problem at human scale. The essay repeatedly names this tension ("which ambiguities can safely be resolved," "requests approval for every harmless step defeats the purpose of delegation") and each time resolves it with a synonym for "use good judgment."
- *Why it lands:* The reader is promised "practical machinery" and receives a calibrated-sounding principle that presupposes the capability it's meant to produce. The essay acknowledges both failure directions (over-asking, under-asking) but offers no account of how an agent locates the line except by example.
- *Severity:* ARGUMENT

**3. The concrete-harm / sensitive-topic distinction avoids the actual hard cases**
- *Quote:* "The relevant distinction is between preventing concrete harm and blocking useful assistance merely because a topic sounds sensitive."
- *Objection:* Nearly every contested refusal lives in the space between those poles—requests where harm is plausible but not concrete, dual-use, or downstream. "Consider capabilities, context, and uncertainty" names the inputs to a risk judgment without saying who makes it, on what evidence, or how disputes between user and provider get settled. The essay criticizes keyword-based refusals but its replacement is a gestural standard that a keyword-filtering provider could claim to satisfy.
- *Why it lands:* The paragraph diagnoses the failure mode crisply (inconsistency eroding trust, users hiding context) and then prescribes at a level of abstraction lower than the diagnosis. A reader who came for the remedy gets criteria that describe good risk assessment rather than constitute it.
- *Severity:* ARGUMENT

**4. The competing-loyalties paragraph asks its question and never answers it**
- *Quote:* "In such cases, whose intent should prevail?... Users need to know whom an agent serves, what incentives shape its recommendations."
- *Objection:* The essay explicitly says better language understanding cannot resolve competing loyalties—then offers only disclosure. But a disclosed conflict is still a conflict; a shopping agent that announces it ranks partners first has not become aligned, merely honest about being misaligned. Every other failure mode in the essay gets a normative prescription; this one gets a rhetorical question and a transparency band-aid.
- *Why it lands:* Commercial conflict of interest is arguably the most *common* human-scale alignment failure users will actually encounter, and the essay treats it as the one case with no remedy beyond labeling. The asymmetry with the rest of the essay is visible.
- *Severity:* ARGUMENT

**5. The line between "common constraints" and "contested visions" is itself contested**
- *Quote:* "It means distinguishing defensible common constraints from contested visions of a good life."
- *Objection:* The essay's examples of the firm side—coercion, serious harm, privacy—are exactly where pluralist disagreement bites hardest. What counts as coercion, how serious harm must be, and what privacy protects are among the most contested questions in applied ethics. The distinction the essay needs to do its pluralism work is asserted as available, not defended as stable.
- *Why it lands:* A careful reader notices the essay locates the easy cases on each side of the line and never tests the line itself. One example of a constraint that reasonable people place on different sides (e.g., content restrictions, nudging toward health) would either strengthen the claim or expose it; the essay does neither.
- *Severity:* ARGUMENT

**6. Durable commitments vs. anti-paternalism is an unresolved internal tension**
- *Quote:* "A user's short-term wish may also conflict with a budget, promise, or boundary they previously set. The system should clarify such conflicts."
- *Objection:* Earlier, the essay warns against "constant correction by a machine that assumes it knows best" and insists "immediate satisfaction is not identical to the user's considered interest." But an agent that surfaces a user's *past* budget against their *present* instruction is doing precisely the correction-against-expressed-wish the essay elsewhere treats as overreach. "Clarify, don't silently pick" softens but doesn't dissolve the question: if the clarified user says "override it anyway," whose instruction governs?
- *Why it lands:* The essay's two commitments—respect present authority, honor durable commitments—collide in exactly the cases it invokes, and it doesn't say which yields. The reader is left unsure whether the essay's delegate has one principal or a stack of them.
- *Severity:* ARGUMENT

**7. "Accountable institutions" defers the hardest questions offstage**
- *Quote:* "Broader questions... require accountable institutions and input from affected communities; they cannot be settled solely by a model or its owner."
- *Objection:* Agents are being deployed now, in jurisdictions where the relevant institutions are slow, captured, or absent, and providers will fill the vacuum by default. The essay is right that models and owners shouldn't settle these questions unilaterally, but saying who *should* settle them without addressing the interim—or what providers owe when institutions fail—leaves the prescription inert where it's needed most.
- *Why it lands:* The essay elsewhere criticizes vagueness (providers hiding behind "vague invocations of safety"), and this paragraph has the same structure: a correct directional claim with no mechanism. A reader lands the objection because the essay taught them to look for it.
- *Severity:* SCOPE

**8. The essay demands explicit justification it does not itself provide**
- *Quote:* "Its commitments to agency, honesty, and protection from harm need explicit justification and mechanisms for challenge."
- *Objection:* The essay endorses agency, honesty, and harm protection as its frame's foundation, insists such commitments need explicit justification—and then offers none, moving directly to machinery. If the standard is that unargued value commitments are a defect in providers' frameworks, the essay's own framework doesn't meet it either.
- *Why it lands:* It's a fair tu quoque, though a mild one: the essay is a framework proposal, not a foundational treatise, and naming one's values is already more than the providers it criticizes do. Still, the sentence sets a bar the text visibly doesn't clear.
- *Severity:* HYGIENE

**9. The subtitle's claim—irreducibility to a single rule—is enumerated, not argued**
- *Quote:* "...why helpfulness, safety, and moral judgment cannot be reduced to a single rule."
- *Objection:* The body catalogs failure modes, but a catalog doesn't defeat the strongest monist rival. A sufficiently rich single principle (e.g., "act on the user's informed, considered interests, subject to harm constraints") could claim to cover every case the essay raises, with the essay's objections re-described as *application* difficulties rather than refutations of unity. The essay never engages that move.
- *Why it lands:* The subtitle promises a thesis; the essay delivers a taxonomy plus governance proposals that a thoughtful single-rule theorist could largely accept. The reader who believed the subtitle gets less than advertised, and the multi-level authority proposal in the final third doesn't obviously require pluralism about rules rather than about *who holds which authority*.
- *Severity:* ARGUMENT

**10. The bridge from everyday failures to "any credible framework" is asserted**
- *Quote:* "Everyday failures do not settle the hardest questions about advanced AI, but they show what any credible framework must preserve."
- *Objection:* Why must lessons from today's delegation failures transfer to systems whose failure structure may be entirely different? The essay hedges appropriately ("do not settle") but then asserts the preservation claim without arguing that future systems will share the delegate/principal architecture that generates these failures. If advanced AI departs from that architecture, the essay's framework may be preserving the wrong things.
- *Why it lands:* It's the essay's only claim about relevance beyond the present, and it's one sentence long. A reader lands the objection precisely because the essay is careful elsewhere—the unargued bridge stands out against the hedged surroundings.
- *Severity:* SCOPE

**11. The evaluation section is a wish list with no measurement story**
- *Quote:* "Tests should examine whether it maintained constraints, resisted misleading external instructions, disclosed failures, and left people able to intervene."
- *Objection:* Each of these is notoriously hard to operationalize—"left people able to intervene" and "disclosed failures" resist the kind of scalable measurement the essay elsewhere dismisses (satisfaction ratings). The essay criticizes existing evaluation for rewarding polish, but its alternative has the same vulnerability unless someone says how these properties get scored without reducing to proxies that can be gamed.
- *Why it lands:* Mildly. The section is explicitly programmatic, so this is partly scope; but the essay's own critique of satisfaction ratings applies pressure it doesn't absorb for its own metrics. A reader notes the asymmetry without expecting full solutions.
- *Severity:* HYGIENE

---

**Total objections: 11** (6 ARGUMENT, 2 SCOPE, 3 HYGIENE)