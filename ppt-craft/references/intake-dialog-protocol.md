# Intake Dialog Protocol

PPT Craft must not blindly generate a deck from a document. A serious PPT starts with understanding and a small number of high-leverage user confirmations.

The agent should first digest the material, make its own judgment, then ask the user to confirm decisions that materially change the deck.

## Principle

Do not ask before thinking.

Wrong:

```text
What style do you want? How many pages? Who is the audience?
```

Right:

```text
I read the document as a founder-method keynote for young AI builders. My default is a 7-slide async-readable hybrid deck with a dark operating-system visual style. Please confirm the few choices below.
```

## Step 1: Digest

Before asking, extract:

- source type: document / prompt / existing PPT / PDF / mixed assets
- intended audience clues
- core thesis
- major claims
- evidence and numbers
- implied action
- risks, caveats, and missing facts
- natural slide count range
- likely route: HTML-first / editable PPTX / raster / hybrid
- likely style anchors

Then write a short Deck Brief v0.

## Step 2: Ask Only Decision Questions

Ask 3-6 questions only when the answers change the output.

High-leverage decision fields:

| Field | Why it matters |
| --- | --- |
| Audience | Changes language, density, proof, and tone |
| Deck job | Pitch, teach, report, persuade, sell, recruit, share |
| Route/editability | Determines HTML-first vs editable PPTX vs raster/hybrid |
| Density/page count | Determines split strategy and type scale |
| Style direction | Determines anchors, images, palette, and layout grammar |
| Preservation constraint | Existing deck: preserve order/wording or restructure |
| Brand/assets | Determines colors, logos, screenshots, product truth |
| Delivery format | PPTX/PDF/HTML/images and verification path |

## Dialog Shape

When a native interactive UI is available, use it for the most important 1-3 grouped decisions. When unavailable, present concise numbered choices.

Each question should include a recommended default based on the source:

```text
1. Audience
   A. Young AI builders / creators (recommended): more method, cases, actionable loop.
   B. Investors / partners: more market, traction, defensibility.
   C. Internal team / students: more teaching structure and exercises.

2. Output route
   A. Hybrid beautiful + editable foreground (recommended): best balance.
   B. HTML-first maximum beauty: strongest visual ceiling.
   C. Fully editable PPTX: stricter layout, lower visual freedom.
```

Do not use "Other" as a real branch unless the UI supplies free-form input. If user does not answer and the task is not blocked, continue with the recommended defaults and record the assumption.

## Agent Judgment

The agent must propose, not merely ask.

Every intake should include:

```text
my read:
- audience:
- deck job:
- likely route:
- recommended page count:
- recommended style anchors:
- one risk:
```

If the source is messy, ask about structure. If the source is clear, do not waste a question asking what is already evident.

## Page Count Guidance

Recommend page count from content and use case:

| Use | Typical pages | Notes |
| --- | --- | --- |
| Live keynote | 10-20 | fewer words, more beats |
| Async share deck | 6-12 | self-contained slides |
| Investor teaser | 8-12 | thesis, market, proof, model, ask |
| Board/report deck | 12-30 | dense tables/charts, appendix |
| Training lesson | 12-40 | modules, examples, exercises |

Never fit everything by shrinking text. Split slides or move detail to appendix.

## Confirmation Contract

After the user responds, freeze:

- deck brief
- route
- density/page count
- style direction
- hard constraints

Then move to Content IR and Layout Blueprint. Do not keep changing these decisions silently later.

## When To Ask Again

Ask again only if a later discovery changes:

- legal/brand risk
- factual ambiguity
- route feasibility
- page count by more than 30%
- style direction because assets do not support it

Otherwise continue building and report assumptions in the delivery note.
