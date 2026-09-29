# Case Studies — Dissecting world-class products with the Five-Layer Blade

> Article line 3257 + line 3249-3506. We dissect Linear / Stripe / Apple / Notion for **judgment** (the rule they obey), never for pixels (the picture they ship). This file is the reference for `references/stage1-five-layer.md` — concrete examples of each layer done well.

## The rule (article line 12)

> "The recognizable thing about a master is the rule, not the picture." — borrowed from `master-styles`, equally true here.

Linear's signature isn't "dark theme", it's "restraint". Stripe's isn't "gradient", it's "trust through detail". Apple's isn't "clean", it's "system over inspiration". Notion's isn't "blocks", it's "composable primitives". If we copy the picture, we get a clone; if we extract the rule, we get judgment we can apply to our own product.

## Linear — restraint (克制)

Dissected with the Five-Layer Blade:

| Layer | Linear's judgment | What to extract |
| --- | --- | --- |
| ① Task | "help a software team move fast without noise" — every feature earns its place by speeding the team | non-goals are aggressive; cut anything that doesn't serve the team's velocity |
| ② Structure | sidebar + list + command palette (⌘K) — keyboard-first, mouse optional | keyboard-first IA; command palette as the universal entry |
| ③ State | every action has loading + success + error; drafts auto-saved; offline survives | never lose user input; every async has visible state |
| ④ System | minimal token set; few colors; type scale tight; one primary action per screen | restraint at the system level — fewer tokens, not more |
| ⑤ Tradeoff | "don't add features; add speed" — Linear ships slow, ships few features, ships fast-feeling UX | the rule is "fewer features, faster feel" |

**What NOT to copy**: Linear's actual dark theme, its specific keyboard shortcuts, its exact typography. Those are the picture.

**What TO extract**: restraint at every layer. One primary action. Few tokens. Keyboard-first. Never lose input. Cut features that don't serve velocity.

## Stripe — trust through detail (细节)

| Layer | Stripe's judgment | What to extract |
| --- | --- | --- |
| ① Task | "let a developer accept payments without fear" — every detail reduces fear | reduce user fear as a first-class goal |
| ② Structure | progressive disclosure — show only what's needed now, drawer for the rest | never a filter wall; always progressive |
| ③ State | every error explains in human words + offers recovery; never "request failed" | error wording is content-specific, offers a next step |
| ④ System | extreme visual hierarchy — size + color + space + alignment + grouping, no decoration | hierarchy without decoration |
| ⑤ Tradeoff | "boring is good" — Stripe avoids novelty, ships consistency | boring consistency over exciting novelty |

**What NOT to copy**: Stripe's gradient, its specific blue, its exact card style.

**What TO extract**: trust through detail. Human error wording. Progressive disclosure. Hierarchy via the five old tools (size/color/space/alignment/grouping), not via decoration. Boring consistency.

## Apple — system over inspiration (法典)

| Layer | Apple's judgment | What to extract |
| --- | --- | --- |
| ① Task | "make the user confident in every tap" — predictability is the feature | predictability over surprise |
| ② Structure | platform patterns (HIG) — don't invent; follow what users already know | follow platform conventions; don't invent IA |
| ③ State | every control has obvious states; pressed feedback mandatory (article line 766) | never ship a control without pressed state |
| ④ System | HIG is the system — written down, taught, enforced | write the design system down; make it enforceable |
| ⑤ Tradeoff | "system beats inspiration" — Apple ships consistency over creativity | the system is the product, not the designer's mood |

**What NOT to copy**: Apple's specific typography, its exact iconography.

**What TO extract**: system over inspiration. Write the rules down. Pressed feedback mandatory. Follow platform conventions. Predictability is the feature.

## Notion — composable primitives (积木)

| Layer | Notion's judgment | What to extract |
| --- | --- | --- |
| ① Task | "let the user build their own tool" — give primitives, not features | prefer composable primitives over fixed features |
| ② Structure | everything is a block; blocks compose; the page IS the structure | block-based IA; let the user structure their own content |
| ③ State | blocks have individual states (loading, error, empty) — not just page states | per-component states, not just page states |
| ④ System | a small block primitive set + composition rules → infinite variety | a small primitive set + composition rules beats a large feature set |
| ⑤ Tradeoff | "ten parts that make ten thousand uses" — don't decide use-cases for the user | don't pre-decide use-cases; give parts |

**What NOT to copy**: Notion's actual block types, its specific slash commands.

**What TO extract**: composable primitives. Block-based structure. Per-component states. A small primitive set that composes. Don't pre-decide use-cases.

## How to use these in this skill

When a user references a product ("like Linear but for X"):

1. **Identify the rule**, not the picture. "Like Linear" usually means "restraint + keyboard-first + never-lose-input", not "dark theme".
2. **Apply the rule at the relevant layer**. Linear's restraint → fewer tokens (layer ④), one primary action (layer ②), aggressive non-goals (layer ①).
3. **Don't copy the pixels**. The user's product is their own; the rule transplants, the pixels don't.

## The case-dissection prompt template

When dissecting ANY product (not just these four) for reference:

```text
Dissect [product] with the Five-Layer Blade.

For each layer, answer:
- ① Task: what single errand does it serve? what does it refuse to do?
- ② Structure: what's the IA? what container choices? why?
- ③ State: how does it handle loading / empty / error / permission / offline?
- ④ System: what's the token / component / pattern set? what's the consistency rule?
- ⑤ Tradeoff: what's the ONE rule it obeys that competitors don't?

Output:
- the RULE (transferable to my product), not the PICTURE (specific to theirs)
- one sentence per layer
- what I would transplant vs what I would NOT
```

## Failure modes

| Failure | Symptom | Fix |
| --- | --- | --- |
| Copying pixels | "use Linear's dark theme" | extract the rule (restraint), apply to own tokens |
| Vague adjectives | "Linear is clean" | dissect with the blade — what makes it clean? (few tokens, one primary, etc.) |
| Cherry-picking layers | "Linear's keyboard shortcuts" without the restraint | the layers compose — can't take ② without ④⑤ |
| Ignoring tradeoff | "Linear is just better" | name the cost — Linear ships slow, ships few features |
