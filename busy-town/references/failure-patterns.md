# Failure Patterns / 失败模式库

Use this reference during QA and critique. A charming town can still fail. If one of these failures is present, do not describe the image as "mostly fine." Name the failure and either regenerate or reroute.

This file is the short diagnostic index. The longer repair table also lives in `SKILL.md` under Failure Mode Library — keep them consistent when editing.

## Common Failures

### Decorative Animals

Symptom: animals stand, wave, grin at the reader, or look cute while the diagram works without them.

Fix: make them physically hand off, inspect, wait, weigh, gate, transform, or parallelize. If removing them changes nothing, cut them.

### Watercolor-Textured Flowchart

Symptom: the image is just boxes, arrows, and labels with watercolor grain.

Fix: turn the relation into a living town scene — street layout, mid-action animals, shops, smoke, flags. Remove giant arrows.

### Atmosphere Instead Of Cooperation

Symptom: a pretty storybook village with no readable handoff, sequence, gate, or comparison.

Fix: name the relationship first; put one focal cooperation zone in the center; run the Collaboration Test again.

### Fake Data Beauty

Symptom: status board / queue / metric town looks polished but values, order, units, or labels are wrong.

Fix: reject. Use `data-status-towns.md` exact data block or reroute to a native chart.

### Reference Hallucination

Symptom: industry, hospital, harbor, school, or apparatus details are plausible but wrong; or a character drifts toward a Scarry likeness.

Fix: gather reference cues (`reference-informed-towns.md`) and regenerate; swap species/outfit if copyright drift; note uncertainty if needed.

### Text Overload

Symptom: the image contains title, subtitle, labels, paragraph, legend, and caption all at once.

Fix: use `layout-handoff.md` and `text-strategy.md`; move title/explanation outside the image.

### Template Lock

Symptom: every topic becomes a bakery street, server village, or the same six-shop river.

Fix: run creative divergence and Swap Test. The town world must come from this source, not the last successful image.

### Wrong Owner

Symptom: Busy Town tries to solve a strict chart, full slide layout, full social card, structural assembly, single-operator concept, logo, or editable diagram.

Fix: hand the job to native chart, PPT skill, social-card skill, **lego-town**, **paper-operators**, vector/code diagram, or image edit. Busy Town can still make a supporting cooperation image.

### Medium Drift

Symptom: the town looks 3D-rendered, flat vector, clay, voxel, or AI-glossy.

Fix: regenerate with HARD NEGATIVES; lead the prompt with hand-painted watercolor / gouache.

### Cutaway-As-Orgchart

Symptom: a stack of flat labeled boxes with no interior, no connectors, no animals working.

Fix: open the wall, add ladders/chutes/pipes, one animal per window, visible shelves/tools.

### Two-Page Delta Loss

Symptom: left and right look like unrelated towns.

Fix: redraw the right page from the same template; change only the cooperation state.

### Close-Up-As-Portrait

Symptom: an animal posing with no tools and no mid-action.

Fix: put it mid-task; lay out the labeled tool kit around it.

## QA Rule

Name the failure. Then either:

1. **Repair** with a targeted edit (wrong flag color, one misspelled sign), or
2. **Regenerate** (cooperation wrong, medium drifted, copyright drift, Swap Test fail), or
3. **Reroute** (wrong owner).

Do not ship a charming-but-unclear town.
