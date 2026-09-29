# Style Anchor Library

## Purpose

Use the local style anchor library before doing open-ended template scouting. It gives PPT Craft a fast, reusable set of world-class visual directions while keeping the default route HTML-first.

Files:

- `assets/style-anchor-library.json`: machine-readable anchor data.
- `assets/style-anchor-starters.json`: starter specs for cover/proof/system/closing previews.
- `scripts/select_style_anchors.py`: local selector for 3 candidate directions.
- `scripts/render_style_anchor_starters.py`: turns selected anchors into visible starter preview slides.

## Default

Default to **HTML-first extreme beauty** unless the user explicitly requires native editable PPTX. Editable PPTX remains available, but style discovery should not be constrained by PowerPoint until editability becomes a hard requirement.

## Selection Command

```bash
python3 scripts/select_style_anchors.py --query "AI investor pitch dark technical" --limit 3
python3 scripts/select_style_anchors.py --deck-type report --industry healthcare --style calm --format json
```

Use the output to seed the 3 visual directions. Do not show anchor names as final slide text.

After selecting candidates, render their starter previews:

```bash
python3 scripts/render_style_anchor_starters.py --anchor dark-technical-investor --out /tmp/dark-technical-starter
python3 scripts/render_style_anchor_starters.py --anchor dark-technical-investor,studio-product-keynote,swiss-consulting-brief --out /tmp/selected-starters
```

Starter previews are not final slides; they are a fast proof that the style can handle cover, proof, system, and closing pages.

## Anchor Set

| Anchor | Best For | Visual Thesis |
| --- | --- | --- |
| Dark Technical Investor Deck | AI, deeptech, biotech, security, infra pitch decks | A serious dark control room revealing a hidden layer of reality |
| Studio Product Keynote | product launches, demos, vision talks | One product promise at a time, staged like a launch film |
| Swiss Consulting Brief | strategy, board, proposal, executive alignment | A precise executive argument where page titles state the answer |
| Data Desk Board Review | reports, MBR/QBR, investor updates, analytics | A newsroom-grade data desk for decisions |
| Editorial Research Atlas | research, insight, culture, whitepapers | A high-end magazine feature turning findings into an atlas |
| Calm Clinical Trust | healthcare, clinical, public health, impact | Humane clinical evidence with no hype |
| Premium Minimal Luxury | portfolio, luxury, real estate, PE, brand | Restraint as confidence |
| Paper Learning Workshop | courses, onboarding, training, workshops | A guided worksheet with examples, practice, and mistakes |
| Bold Founder Manifesto | founder talks, campaigns, vision, movement decks | Unforgettable posters that make the thesis inevitable |
| Product Demo Workbench | sales, product walkthrough, enablement | The buyer sees their workflow before and after the product |
| Civic Policy Brief | policy, public sector, nonprofit, climate | Evidence brief for accountable public decisions |
| Creative Brand Campaign | brand, campaign, media kit, agency proposal | The campaign world before the campaign exists |
| Spatial Experience Showcase | venue, real estate, tourism, events, culture | Atmosphere plus path, program, and proof |

## How To Use Anchors

1. Run the selector using the Deck Brief v0.
2. Pick 2-4 relevant anchors.
3. For each, translate the anchor into a **direction card**:
   - why this fits the user's audience and task,
   - cover concept,
   - content-slide system,
   - proof-slide system,
   - risk.
4. Render starter previews for the candidate anchors and inspect the contact sheet.
5. Create 3 real first-slide previews or 3 short direction cards using actual user content.
6. Lock the chosen direction into `style lock`.

## Borrowing Rules

Borrow:

- visual thesis,
- palette semantics,
- typography roles,
- layout grammar,
- slide archetypes,
- motion tone,
- HTML-first notes.

Do not copy:

- proprietary template imagery,
- exact template slide layouts,
- sample copy or fake metrics,
- competitor visual identity,
- style names as visible deck labels.

## Source Scouting

The local library was seeded from current public template ecosystems and prior deck forensics:

- Pitch template gallery: professional deck/template taxonomy.
- Beautiful.ai: use-case taxonomy for pitch decks, reports, proposals, sales, branding, research, product launch, investor relations, and training.
- Canva, Figma, Adobe Express, Slidesgo, SlidesCarnival: broad style and downloadable template references.
- InnerScan private reference: dark technical investor deck logic; borrow only system rules, never private content/assets.

When stakes are high, refresh current web references and update `assets/style-anchor-library.json` only with generalizable patterns.
