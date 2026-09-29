# Asset Routing And Truth / 资产路由与事实约束

Use this reference before final prompt writing when the source is more than a vague "搭个图": a system doc, prompt, architecture, report, metrics board, slide, screenshot, or social-card package.

LEGO Town is a visual **structure** system, not only a style. The first question is not "what should the bricks look like?" but "what job must this image do in the final artifact?"

## Core Rule

Keep the brick build only when **buildable structure** clarifies the meaning — parts and how they snap together.

If the final need is an exact chart, a full slide layout, a full social card, a logo, a character-cooperation story, a single conceptual action, or a decorative brick pile where no structure is explained, do not force LEGO Town to own the whole job.

## Asset Roles

Pick one role before choosing the mode.

### Article / Doc Figure
- Visual job: make one structure memorable.
- Best form: finished build or exploded view.
- Text ownership: short printed tiles inside; paragraph outside.

### Process / Prompt Instruction
- Visual job: show assembly order and optional vs required parts.
- Best form: **Instruction Sheet** with numbered steps + parts call-out.
- Truth rule: real step names and real `×N` counts; do not invent modules.

### System / Architecture Town
- Visual job: show modules, load-bearing dependencies, routes.
- Best form: Finished Build on a baseplate (service town, knowledge town).
- Truth rule: real service/module names on tiles.

### Anatomy / Exploded Breakdown
- Visual job: show what's inside / what a good X is made of.
- Best form: Exploded View along connection lines.
- Truth rule: part list matches the source.

### Comparison Build
- Visual job: make the single swapped module obvious.
- Best form: two side-by-side builds sharing one baseplate, or before/after.
- Truth rule: only the delta module differs.

### Box Art / Cover
- Visual job: title/cover hero for a doc or product.
- Best form: Box Art with **original** product name — never the LEGO logo.
- Text ownership: banner may carry the product name; long blurb stays outside.

### Data Status Build
- Visual job: encode metrics as brick status (stack height, stud exposure, gate posture), not as a fake dashboard.
- Best form: finished build or instruction with state coding.
- Truth rule: list every value that appears; see `data-status-builds.md`.
- If exact axes are the whole artifact → native chart; bricks can surround it.

### Reference-Informed Build
- Visual job: make a real apparatus/system recognizable in bricks without copying a trademarked set.
- Best form: original build with stable structural cues; see `reference-informed-builds.md`.

### Center Illustration For A Card Or Slide
- Visual job: central image well only.
- Best form: no large title inside; safe margins; few edge tiles.
- Outer layout owns headline and commentary.

## Routing Questions

```text
asset role:
final container: article / README / social card / slide / doc / knowledge base / other
display well or ratio:
text ownership: inside image / outside layout / both
truth constraints: exact module names / exact ×N counts / exact metrics / none
reference need: yes/no and why
build necessity:
if not LEGO Town, better owner:
```

## Cognitive Anchors For Long Sources

Pick 1–6 anchors — do not brick every paragraph:

- the opening structure question
- the load-bearing dependency
- the assembly order
- the missing / optional parts
- the comparison delta
- the metric / risk turn
- the closing assembled whole

## Truth Handling

### Must Be Exact
- module / step / part names from the user
- piece counts in call-outs (`2×4 ×3`)
- metrics that appear as stacks/flags
- product names on box art (user's brand or original name)

```text
Exact text: include only these labels: "系统", "上下文", "指令", "格式".
Exact counts: four build steps; parts call-out shows real ×N only.
Do not invent extra modules, steps, dates, or the LEGO logo.
```

### Can Be Symbolic
- which brick colors carry accents
- camera / baseplate layout
- which original minifig accessories appear
- metaphor district (service town vs knowledge town) when it fits

## What To Refuse Or Reroute

Reroute when:

- strict chart with exact axes → native chart
- character cooperation / simultaneity / who-hands-off-to-whom → **busy-town**
- one conceptual action by one paper actor → **paper-operators**
- single quote / feeling / number → quote-cards / cover-pop
- full social card or slide layout → card/PPT skill owns the frame
- user wants a real LEGO® set or licensed character → original equivalent only, say so
- logo / icon system / sticker → other skills

## QA Additions

- Asset role is visible in the result.
- Text ownership respected (no stuffed headline when layout owns it).
- Exact labels/counts/metrics not invented or swapped.
- No LEGO logo, no trademarked set, no licensed minifig.
- Structure still necessary after routing.
- Readable at intended display size.
