# Text Strategy / 文字策略

Use with `lettering-and-text.md` (how text *physically* lives in bricks). This file decides **which text the image owns** vs the outer layout, and the label budget.

## Label Budget By Asset Role

| Asset role | Budget | Carriers |
| --- | --- | --- |
| Article / Doc Figure | 3–6 short tiles | printed tiles on modules |
| Process / Prompt Instruction | step badges + 3–6 part labels + call-out counts | instruction page type + tiles |
| System Town | 4–8 district/module signs | signboards + tiles |
| Exploded Breakdown | 1 label per floating part | tiles along connection lines |
| Comparison | 2–4 delta labels | matched tiles on both builds |
| Box Art | 1 product banner + optional age/piece strip | box-art banner (original name) |
| Data Status Build | 3–5 state tiles + exact values if readable | tiles / chalkboard-style plates |
| Center Illustration | 0–4 | only what layout won't say |

Chinese: usually **2–6 characters** per tile. Longer → overlay path.

## Image Owns vs Outer Owns

**Image owns:** module names, step numbers, parts `×N`, short state words, original product banner, road signs that are the relation.

**Outer layout owns:** title/subtitle, paragraph explanation, citations, long conclusions, CTA, platform metadata.

## Exact Text Block

```text
Exact text: include only these labels: "A", "B", "C".
No other text, no fake paragraphs, no LEGO logo/wordmark, no watermark.
```

## Repair Policy

1. Stricter exact-text regeneration.
2. Shorten labels onto larger quiet tiles.
3. Blank printed tiles + post overlay for unstable Chinese.
4. Never silently accept misspelled or invented module names in public assets.

## Anti-Patterns

- floating captions ignoring brick carriers
- stuffing README title into the build
- brick-building long Chinese into stroke-mush
- placeholder labels that fail the Swap Test
