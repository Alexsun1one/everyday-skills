# Data Status Towns / 数据状态镇

Use this reference when the source includes numbers, rankings, metrics, queues, SLAs, backlog, pass rates, benchmark results, project status, or evidence summaries — and the image should explain **operational meaning** as a living town, not replace a rigorous chart.

Busy Town should not pretend to be a chart renderer. Its job is to turn data into readable town status (queue piles, red flags, smoke, backlog) while preserving the facts that appear in the image.

## Data Contract

Before prompting, write:

```text
data source:
metric type:
exact labels:
exact values:
unit:
order:
highlight:
uncertainty:
what the data means operationally:
```

If values cannot be read, ask for data or mark them approximate. Do not invent values to make the town prettier.

## When To Use Busy Town

Use Busy Town when:

- the data needs operational interpretation (bottleneck, risk, backlog, healthy vs alert)
- one comparison, queue, or status turn matters most
- a human reader needs a story about what to do next
- the metric can become a physical town object (crate pile, flag, stamp tray, scale)

Use a native chart / PPT / code-rendered diagram instead when:

- exact axes are the primary deliverable
- the chart must be editable
- there are many values or dense labels
- the final artifact will be audited as a statistical chart

Busy Town can still create a **surrounding status town** next to a native chart.

## Composition Patterns

### Queue Street
- A shop with a line of crates / carts / animals waiting.
- Queue length encodes the number (e.g. 12 crates = backlog 12).
- Downstream shop may be dozing (dependency / idle).
- Good for: backlog, latency, bottleneck.

### Risk Flag Board
- Several shops with green / red / gold flags.
- One Inspector animal stamps or moves a risk chip.
- Good for: project status, QA, incidents, launch readiness.

### Pass/Fail Gate
- A checkpoint with admitted crates vs rejected pile.
- Exact pass/fail counts on stamps or chalkboard.
- Good for: quality rates, approval funnels.

### Scale Of Evidence
- Town-square scale with two labeled crates of evidence.
- Good for: tradeoffs, model comparison, strategy claims.

### Before / After Metric Spread
- Two-page spread: old metric state vs new.
- Exact before/after values on banners or crate stamps.
- Good for: improvement stories, migrations.

## Prompt Requirements

For every data status town prompt, include:

```text
Exact data: show only these values: ...
Exact labels: include only these labels: ...
Do not add extra categories, numbers, axes, dates, legends, or fake sources.
If a number cannot fit clearly as a town object (crate count, flag chip, chalkboard), omit it rather than inventing or shrinking it into fake UI.
Encode status with storybook channels (smoke, flags, piles, stamps) — not dashboard badges.
```

## Encoding Numbers As Town Objects

Prefer physical encodings over digits when possible:

| Metric | Town encoding |
| --- | --- |
| backlog = 12 | twelve crates in a queue |
| pass rate high | green stamp majority, small reject pile |
| alert | one red rooftop flag |
| idle station | no smoke + dozing helper |
| throughput up | more carts on the street / thicker smoke |

When a digit must appear, put it on a **chalkboard / crate stamp / banner chip**, large and few — never a tiny HUD.

## QA

Reject if:

- any value is wrong
- category order is swapped
- the image adds fake numbers or fake sources
- the scene hides the metric behind cute clutter
- the animals do not clarify the operational meaning
- it looks like a spreadsheet screenshot with watercolor texture
- it uses UI progress bars / KPI tiles

Accept if:

- the main data point is visible in three seconds
- exact values and labels match the contract
- the town status explains the implication
- the image works as a data story even if the surrounding article is not visible
