---
name: ppt-craft
description: "Create, redesign, or convert presentation decks with a world-class slide harness. Use when the user asks to make PPT/PPTX/slides/deck/演示文稿/幻灯片, convert source material into a deck, beautify an existing deck, create an HTML presentation, produce an editable PowerPoint, export PDF/PPTX/slide images, generate style directions for a presentation, or improve a deck's visual polish, motion, narrative, density, or shareability. Combines HTML-first deck craft, visual style discovery, editable-PPTX route boundaries, raster slide-image generation, and screenshot-backed QA. Trigger words include PPT, pptx, presentation, slide deck, keynote, pitch deck, report deck, 课件, 路演, 汇报, 提案, 生成PPT, 做PPT, 美化PPT, 转PPT, HTML slides, editable PPTX, 导出PDF, 视觉方向, 三版风格, 丝滑演示."
---

# ppt-craft（Progressive Disclosure 瘦身入口）

> **Fleet Progressive Disclosure**: 默认只读本页脊柱。完整旧正文在 `references/full-rulebook.md`（默认不读）。需要细节时按节打开 full-rulebook，禁止通读当仪式。

## 何时用

见下方保留脊柱 / frontmatter description。若任务只需短约束，优先 vault `04-Prompts/UI铁律-速查卡.md`（仅 UI 类）。

## 阅读预算（硬）

1. 读完本页即可开工  
2. 卡住再查 `references/full-rulebook.md` 相关小节  
3. 有 scripts/data 则按需跑脚本，勿灌全表  

## 保留脊柱（摘自原文前部）

# PPT Craft / 幻灯片工坊

PPT Craft turns source material into a deck that is beautiful, easy to present, easy to share, and honest about editability. It is a **conductor skill**: use the light local harness for HTML preview, screenshots, and validation; use heavier PPTX/image engines only when their route is the right tradeoff.

Default response language follows the user. For Chinese users, write Chinese deck copy unless the source or user says otherwise.

## First Decision

Choose one route before designing. If the user did not specify a format, default to **Route A: HTML-first extreme beauty**, then offer PDF/PPTX/image exports after the first validated deck exists. Only let Route B override the default when native PowerPoint editability is a hard requirement.

| Route | Choose when | Main promise | Tradeoff |
| --- | --- | --- | --- |
| **A. HTML-first deck** | User wants maximum beauty, motion, browser presentation, web sharing, PDF export, or is still exploring style | Highest visual ceiling, smooth previews, screenshot QA | PPTX editability is not guaranteed |
| **B. Editable PPTX** | User says colleagues must edit text/shapes/tables/charts in PowerPoint, or asks for native editable PPTX | PowerPoint objects remain editable | Visual freedom is constrained from the first HTML/PPTX decision |
| **C. Raster image deck** | User wants social-sharing slides, NPC/cute/story cards, or image-first visual impact | Image quality and style freedom | Slides are pictures, not editable text |
| **D. Existing deck beautify** | User provides a finished `.pptx` and wants polish | Preserve or deliberately restructure based on one discriminator | Must clarify whether page count/order stays fixed |

If a source `.pptx` is provided, ask one discriminator only when ambiguous: **"Should the original page count/order and each slide's wording be preserved, or can I restructure it into a new story?"** Preserve -> Route D; restructure -> Route A/B.

## Core Workflow

1. **Digest before asking.** If the user provides a document, prompt, PPTX, PDF, or URL, first extract the story, audience clues, claims, assets, and density. If a reference deck is provided, run or manually follow `references/reference-deck-forensics.md`.
2. **Run the intake dialog.** Draft a Deck Brief v0, infer sensible defaults, then ask the few high-leverage questions that change audience, deck job, route, density/page count, style, or preservation constraints. When native UI dialog tools are available, use them for grouped choices; otherwise present concise options. Read `references/intent-intake-and-interview.md` and `references/intake-dialog-protocol.md`.
3. **Freeze a Deck Brief.** Write: audience, deck job, final format, density mode, narrative arc, assets, constraints, and verification plan. For branded decks, collect or fetch logo/product/UI assets before styling.
4. **Use the system architecture for serious decks.** For high-stakes or multi-slide work, create the required artifacts: `deck-brief.json`, `content-ir.json`, `narrative-spine.md`, `style-anchors.md`, `layout-blueprint.json`, and `asset-plan.md`. Treat final styling as a fidelity restore of the blueprint/skeleton, not a fresh generation. Read `references/system-architecture.md` and `references/design-practice-bridge.md`.
5. **Choose the world-class pattern.** Match the deck to a proven narrative and slide archetype set before designing pixels. Read `references/world-class-deck-patterns.md`.
6. **Find style/template anchors and starter previews.** For non-trivial decks, run the local anchor selector first, then render starter previews for the strongest anchors. Each candidate direction must prove cover, proof, system, and closing slides before full-deck work. For high-polish/high-stakes decks, generate ImageGen visual oracle plates and extract `visual-tokens.json` before implementation. Read `references/style-anchor-library.md`, `references/style-anchor-starter-library.md`, `references/template-style-library.md`, and `references/imagegen-first-visual-oracle.md`.
7. **Select layout archetypes and design composition before decoration.** Every serious slide must declare an archetype or a deliberate custom reason, then reserve pixel regions in `layout-blueprint.json`. Read `references/layout-archetype-library.md` and `references/layout-first-composition.md`.
8. **Lock the slide design system before generating images.** Define type roles, font scale, backplates, line/icon grammar, object richness, and image text-safe rules. For complex system maps or line-heavy slides, also define the web-rendered relationship graph contract before final styling. Read `references/slide-design-system.md` and `references/web-rendered-relationship-graphs.md`.


## 完整规则书

→ `references/full-rulebook.md`
