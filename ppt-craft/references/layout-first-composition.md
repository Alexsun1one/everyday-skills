# Layout-First Composition

World-class deck craft starts with composition, not decoration. A beautiful background image is only useful after the slide has a clear plan for where meaning, type, contrast, and visual motion live.

Use this reference before generating images, styling HTML, or exporting PPTX.

## Core Rule

Every non-trivial slide must start from a **Composition Blueprint**:

```text
slide id:
job:
safe area:
primary claim box:
supporting copy box:
visual subject box:
evidence object box:
loop/path box:
contrast mask:
editable object plan:
what must stay empty:
```

If the blueprint cannot explain where text breathes, where the viewer looks first, and how the eye moves next, do not open the visual editor yet.

## Why The Previous Approach Fails

Wrong order:

1. Generate or pick a beautiful background.
2. Put text and objects on top.
3. Patch collisions after export.

This creates attractive screenshots that fall apart in PPTX because the image, text, and objects compete for the same pixels.

Correct order:

1. Define story job and information hierarchy.
2. Reserve pixel regions for title, body, evidence, and loop/path.
3. Specify negative space and contrast masks.
4. Lock the slide design system: type roles, font scale, text backplates, line/icon grammar, and object richness.
5. Generate blueprint-aware asset prompts that force the image to respect text-safe zones and foreground overlay plans.
6. Generate or crop background art that respects those reserved regions.
7. Place foreground text and editable objects into the reserved boxes.
8. Screenshot HTML and smoke-render PPTX; fix any layout drift.

## Pixel Blueprint

For a 1280 x 720 slide, use explicit coordinates. Do not rely on flow layout for major objects.

Recommended safe geometry:

| Region | Typical x/y/w/h | Use |
| --- | --- | --- |
| Outer safe area | `64, 56, 1152, 608` | Nothing important outside it |
| Copy rail | `72, 72, 500, 380` | Kicker, headline, one support paragraph |
| Visual rail | `640, 84, 520, 420` | System diagram, hero asset, proof object |
| Evidence band | `72, 330, 520, 230` or `650, 330, 500, 230` | Tables, charts, case proof |
| Progress loop | `72, 596, 520, 54` | Persistent deck loop/status |
| Footer/meta | `72, 660, 1120, 20` | Optional, small only |

Keep at least `24px` between large text boxes, `32px` between title and supporting copy, and `48px` between independent modules unless a visible connector explains the relationship.

## Contrast Planning

Do not place important text on a visually busy area just because it is technically readable.

Before styling, choose one:

- **Quiet field**: background art has deliberate empty/dark area behind text.
- **Solid mask**: a plain translucent rectangle behind the copy rail.
- **Editorial crop**: image is cropped so the subject lives away from the copy.
- **Split stage**: left/right or top/bottom regions are visibly separated.

The mask is a layout object, not decoration. It exists to preserve reading order.

## Typography And Object Planning

The blueprint must be paired with a design system. A rectangle labeled `claim` is not enough.

Before image generation, define:

- title role and expected line count;
- support/body role and maximum line count;
- label/caption/table roles;
- text backplate type for each text region;
- foreground objects such as badges, route chips, callout tickets, evidence plates, magnifier windows, stamps, leader lines, and connector styles;
- icon policy and line grammar.

Every generated image prompt must know which areas will receive editable foreground objects. This is what prevents raw text from being pasted onto busy texture later.

## Loop And Path Grammar

For decks about systems, growth, operations, productization, AI workflows, or strategy, make the loop a real layout object:

```text
input -> operation -> proof -> sale -> system -> asset -> repeat
```

Rules:

- The loop/path has a fixed region and consistent node style across slides.
- A slide highlights one active node; inactive nodes recede.
- Connectors show direction; do not scatter nodes randomly.
- The loop must support the argument, not merely decorate the page.

## Editable PPTX Specific Rules

Native PPTX has different font metrics from the browser. Author defensively:

- Use separate positioned text boxes for each large headline line; avoid `<br>` in hero titles.
- Keep each headline line in a box at least `1.15x` its rendered height.
- Give paragraphs more height than the browser needs.
- Do not put key text inside an image unless the route is raster/image deck.
- Avoid stacking text over thin image details; use a mask or move the text.
- Treat QuickLook/PowerPoint smoke render as part of layout QA, not optional polish.

## Blueprint File

For serious decks, add `layout-blueprint.json` beside `brief.md`:

```json
{
  "stage": { "width": 1280, "height": 720, "safe": { "x": 64, "y": 56, "w": 1152, "h": 608 } },
  "slides": [
    {
      "id": "01-cover",
      "job": "name the thesis",
      "claim": { "x": 72, "y": 92, "w": 520, "h": 220 },
      "support": { "x": 72, "y": 324, "w": 500, "h": 74 },
      "visual": { "x": 640, "y": 80, "w": 520, "h": 430 },
      "loop": { "x": 72, "y": 596, "w": 520, "h": 54 },
      "empty": ["center-left lower field", "outer 48px edges"]
    }
  ]
}
```

The blueprint is not for the user to admire. It is the construction scaffold that prevents pretty assets from breaking the slide.

## Acceptance Test

Reject the slide when any of these are true:

- The background could be removed and the text would still look randomly placed.
- A large title line wraps differently in PPTX than in HTML.
- The visual subject steals contrast from the primary claim.
- A table/chart/card occupies a region that was not reserved in the blueprint.
- The loop/path is decorative rather than explanatory.
- The same layout could be used for any topic after changing only text labels.
- The image prompt did not reserve text-safe zones before generation.
- Important text lacks a designed backplate or quiet field.
- Most slides are only left/right or top/bottom relations.
