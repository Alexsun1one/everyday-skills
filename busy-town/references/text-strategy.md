# Text Strategy / 文字策略

Use this reference whenever shop signs, banners, flags, or floor plaques matter.

The model should generate only the text that the **image itself** must own. Busy Town dies two ways with text: too little (a pretty village that says nothing) and too much (a flowchart with watercolor grain).

## Label Budget By Asset Role

| Asset role | Label budget | What the labels name |
| --- | --- | --- |
| Article / Doc Figure | 3–6 short | roles, stations, one takeaway strip |
| Process Town | 4–8 | every station on the spine + 1–2 state flags |
| Org / System Cutaway | 1 per floor + 1 roof banner | floor names, ownership |
| Comparison Spread | 1 banner per page + 2–4 delta labels | old/new, the single difference |
| Trade Close-up | 4–8 tool/output labels | kit items, not a bio |
| Data Status Town | 3–5 state labels + exact values only if readable | queue, pass, risk |
| Center Illustration | 0–4 | only what the outer layout won't say |

Chinese labels: usually **2–6 characters**. Longer labels render worse and clutter the town.

## Good Label Shapes

Prefer:

- **role nouns** on shop signs: `接单` `质检` `巡检`
- **station verbs** on awnings: `分拣` `盖章` `出货`
- **states** on flags / stamps: `告警` `完成` `待检` `退货`
- **floor names** on plaques: `接入层` `数据层`
- **page banners** on two-page spreads: `旧·手动` `新·自动`

Avoid:

- full sentences as shop signs
- abstract stage names like `INPUT PHASE` / `处理阶段一`
- fake UI labels, progress bars, KPI tiles
- tiny captions on busy watercolor texture
- labels that repeat what the animals already show (don't label "交接" if two animals are mid-handoff)
- floating captions not attached to a shop, flag, crate, vehicle, or plaque

## Exact Text Block

For final prompts, state:

```text
Exact text: include only these labels: "接单", "拣货", "质检", "打包", "发货", "配送".
No other text, no fake paragraphs, no extra legend, no watermark, no publisher logo.
```

If the image needs a title or explanatory line, decide whether the **outer layout** should own it. Most README / social / slide titles should stay outside.

## Text Ownership Split

### Image Owns
- shop signs, floor plaques, vehicle livery
- short state flags and crate stamps
- exact metric chips that belong to a status object
- comparison page banners

### Outer Layout Owns
- title / subtitle
- paragraph explanation
- citations / footnotes
- long conclusions
- author note / CTA
- platform-specific metadata

## Repair Policy

If the town is good but labels are wrong:

1. Try one regeneration with a stricter exact-text block.
2. Shorten labels and place them on larger quiet signboards / plaques.
3. If Chinese is still unstable and the surrounding layout can own the text, regenerate with **blank signboards** of the right shape/size and overlay text in post. Note this in the output contract.
4. Do not silently accept misspelled or invented labels in showcase, README, education, data, or public article assets.

## Anti-Patterns

- stuffing the town with a title + subtitle + 12 labels + a caption
- leaving the town text-empty "so it looks cleaner"
- using English stage jargon on a Chinese article figure
- putting the takeaway sentence inside the image when a caption outside would do
