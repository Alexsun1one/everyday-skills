# Data Status Builds / 数据状态搭建

When the source includes numbers, rankings, queues, SLAs, backlog, pass rates, or status — and the image should explain **structural/operational meaning** in bricks, not replace a rigorous chart.

## Data Contract

```text
data source:
metric type:
exact labels:
exact values:
unit:
order:
highlight:
uncertainty:
what the data means structurally:
```

Do not invent values to make the build prettier.

## When Bricks vs Native Chart

**Use bricks** when: one comparison/bottleneck/risk matters; stacks/gates/studs can encode it; the reader needs "what to do next."

**Use native chart** when: exact axes are the deliverable; many values; editable; audited as statistics. Bricks may surround the chart as a status town.

## Composition Patterns

### Stack Height = Magnitude
Taller brick stack = larger backlog / load. Label the top tile with the exact value if needed.

### Stud Exposure = Done vs To-Build
Exposed studs = remaining work; smooth tiles = complete. Encode a % as covered vs open studs only if readable.

### Gate / Barrier = Pass-Fail
Striped barrier + green/red trans-stud: admitted vs blocked counts on tiles.

### Seesaw / Scale = Tradeoff Metrics
Two weighted stacks with named values.

### Before/After Twin Builds
Same baseplate layout; stack heights or gate states change; exact before/after on tiles.

## Prompt Requirements

```text
Exact data: show only these values: ...
Exact labels: include only these labels: ...
Encode with brick channels (stack height, stud exposure, gate, trans-stud) — not UI badges/KPI tiles.
Do not invent extra categories or numbers.
```

## QA

Reject wrong values, swapped order, fake sources, dashboard UI on bricks, or a pretty pile that hides the metric.
Accept if the main number reads in three seconds and matches the contract.
