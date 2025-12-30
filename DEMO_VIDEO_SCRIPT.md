# Context Graphs: System of Record for Decisions

## Demo Video Script (3-4 minutes)

---

# Context Graphs: System of Record for Decisions

## Demo Video Script (3-4 minutes)

---

## SECTION 1: THE HYPOTHESIS (0:00-0:30)

**[YOUR FACE - Direct to camera]**

"This morning, Jaya Gupta published: the next trillion-dollar companies won't be Systems of Record for Data. They'll be Systems of Record for _Decisions_.

The gap she identified? Companies never capture Decision Traces. Why was that deal approved? Why did we deny this customer? That logic lives in Slack. Never queryable. Never scalable.

I read that and built a working implementation in 48 hours."

**[VISUAL: Show Jaya's article title briefly]**

---

## SECTION 2: THE PROBLEM (0:30-1:10)

**[VOICEOVER - Screen recordings]**

"Right now, most systems output a simple decision: APPROVE or DENY. No trace. No precedent. No explanation."

**[SHOW: Old-style decision output - just "Decision: APPROVE"]**

"That's not a System of Record for Decisions. That's just a black box prediction.

Jaya's thesis: if you can't record _why_ a decision happened, you can't learn from it. You can't scale judgment. You can't detect bias."

---

## SECTION 3: THE SOLUTION (1:10-2:30)

**[YOUR FACE]**

"Here's what I built. A system that captures everything."

**[SCREEN SHARE: Live Streamlit app - "Make a Decision" tab]**

"Submit a request. Automatically:

1. Extract intent
2. Match explicit policies
3. Search similar past decisions
4. Return precedent outcomes
5. Synthesize with LLM reasoning
6. Record entire trace in Neo4j"

**[SHOW: Request being submitted]**

"Watch the results:"

**[SHOW: Decision output]**

"✅ Decision: APPROVE
📊 Confidence: 84%
📋 Policies: Income-debt 2.8 (threshold 3.5). Credit 720 (threshold 650).
📈 Precedents: 4 similar cases approved. 1 denied. Success rate: 80%.
📝 Reasoning: 'Strong fundamentals. Precedent favors approval. Minor risk flag on inquiries.'"

**[EXPAND sections]**

"All sections expand. Full transparency. Everything queryable."

**[SHOW: Neo4j Browser - decision graph]**

"Every decision lives here permanently. With relationships to policies, precedents, everything."

---

## SECTION 4: HOW THIS VALIDATES JAYA'S THESIS (2:30-3:20)

**[YOUR FACE - Direct, analytical]**

"Let me show you why this proves her exact points.

She said: **Incumbents can't build this because they're siloed.** I'm not siloed. I sit in the orchestration layer—middle of the workflow. I see request, policies, precedent, reasoning. All at once. All at decision moment.

She said: **The moat is compound value.** Year one: 50 decisions. Year two: 500. Year three: 5,000. At 5,000, your precedent database is unreplicable. No competitor has that institutional memory.

She said: **This moves from automation to autonomy.** Most AI agents fail because they don't understand unwritten rules. With a context graph, the AI learns tribal knowledge. It operates independently. It knows when policies apply and when exceptions matter.

**All three advantages? I have them. Live. Proven.**"

**[VISUAL: Neo4j graph showing decision growth]**

---

## SECTION 5: CLOSE (3:20-4:00)

**[YOUR FACE - Confident]**

"Jaya predicted: whoever captures the System of Record for Decisions wins the market.

I'm not predicting. I'm executing.

✅ Policies explicit and queryable
✅ Precedents with outcomes recorded
✅ Decision traces permanent
✅ Tribal knowledge captured
✅ Ready to scale thousands of decisions

The next generation of enterprise software doesn't just predict. It decides. And it remembers why.

Jaya, if you're watching: you identified the gap. This is how you close it."

**[SHOW: Links]**

```
Demo: [Streamlit URL]
API: [Render URL/docs]
Code: [GitHub]
Article: [Jaya's piece]
```

"Let's build the system of record for decisions."

**[FADE OUT]**

---

## VISUAL GUIDE (NOT DIALOGUE)

**Shots needed:**

- [ ] Your face (well-lit, direct) = 60 seconds total
- [ ] Jaya's article title = 3 seconds
- [ ] Streamlit form being filled = 20 seconds
- [ ] Decision results (expanded sections) = 30 seconds
- [ ] Neo4j Browser with decision nodes = 20 seconds
- [ ] Decision History tab = 15 seconds

**Technical:**

- 1080p minimum, 1440p ideal
- External mic (USB mic $50+)
- Front-facing lighting, no shadows
- Simple background
- System font size +2 notches

**Tone:**

- Calm, confident, not selling
- Let visuals do the work
- Pause 1-2 seconds between major points
- Direct eye contact with camera

**Recording:**

- 2-3 takes per section
- Use best take of each
- Edit together smoothly
- Add subtle music (not distracting)
- Subtitle the whole thing
