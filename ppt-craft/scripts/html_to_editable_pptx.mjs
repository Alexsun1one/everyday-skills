#!/usr/bin/env node
import { createRequire } from "node:module";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import process from "node:process";
import { fileURLToPath, pathToFileURL } from "node:url";

const require = createRequire(import.meta.url);

function loadModule(name) {
  try {
    return require(name);
  } catch (error) {
    const bundled = path.join(
      os.homedir(),
      ".cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules",
      name,
    );
    return require(bundled);
  }
}

const PptxGenJS = loadModule("pptxgenjs");
const { chromium } = loadModule("playwright");

function parseArgs(argv) {
  const args = {
    width: 13.333,
    height: 7.5,
    strict: false,
    report: null,
  };
  const positional = [];
  for (let i = 0; i < argv.length; i += 1) {
    const value = argv[i];
    if (value === "--out") args.out = argv[++i];
    else if (value === "--report") args.report = argv[++i];
    else if (value === "--title") args.title = argv[++i];
    else if (value === "--width") args.width = Number(argv[++i]);
    else if (value === "--height") args.height = Number(argv[++i]);
    else if (value === "--strict") args.strict = true;
    else if (value === "--help" || value === "-h") args.help = true;
    else positional.push(value);
  }
  args.deckDir = positional[0];
  return args;
}

function usage() {
  console.log(`Usage:
  node scripts/html_to_editable_pptx.mjs <deck-dir> --out <deck.pptx> [--report report.json]

Input:
  <deck-dir>/slides/*.html or <deck-dir>/*.html

Editable HTML contract:
  - slide canvas is fixed size, usually 960pt x 540pt or 1280px x 720px
  - text lives in h1-h6, p, li, span, small, strong, em, or [data-pptx-text]
  - wrappers carry solid backgrounds/borders/radius
  - pictures use img
  - tables use real <table> markup
  - charts use [data-pptx-chart] with a JSON spec
  - connectors use [data-pptx-connector] or [data-pptx-line]
  - complex blocks may be marked data-pptx-raster="true"
`);
}

function parseCssColor(input) {
  if (!input || input === "transparent") return null;
  const rgba = input.match(/rgba?\(([^)]+)\)/i);
  if (!rgba) {
    const hex = input.trim().replace("#", "");
    if (/^[0-9a-f]{6}$/i.test(hex)) return { color: hex.toUpperCase(), alpha: 1 };
    return null;
  }
  const parts = rgba[1].split(",").map((part) => part.trim());
  const rgb = parts.slice(0, 3).map((part) => Math.max(0, Math.min(255, Number.parseFloat(part))));
  const alpha = parts[3] === undefined ? 1 : Math.max(0, Math.min(1, Number.parseFloat(parts[3])));
  if (alpha === 0) return null;
  const color = rgb.map((n) => Math.round(n).toString(16).padStart(2, "0")).join("").toUpperCase();
  return { color, alpha };
}

function transparency(alpha) {
  return Math.round((1 - alpha) * 100);
}

function pxToPt(px) {
  return px * 0.75;
}

function toInches(rect, stage, deck) {
  return {
    x: ((rect.left - stage.left) / stage.width) * deck.width,
    y: ((rect.top - stage.top) / stage.height) * deck.height,
    w: (rect.width / stage.width) * deck.width,
    h: (rect.height / stage.height) * deck.height,
  };
}

function withTextSafetyBox(box) {
  const extra = Math.min(0.22, Math.max(0.04, box.h * 0.16));
  return { ...box, h: box.h + extra };
}

function fontFace(fontFamily) {
  const first = (fontFamily || "Arial").split(",")[0].trim();
  return first.replace(/^["']|["']$/g, "") || "Arial";
}

function safeText(text) {
  return (text || "")
    .replace(/\r\n?/g, "\n")
    .split("\n")
    .map((line) => line.replace(/[ \t\f\v]+/g, " ").trim())
    .filter(Boolean)
    .join("\n")
    .trim();
}

function cleanHexColor(input, fallback = null) {
  if (!input) return fallback;
  let value = String(input).trim().replace(/^#/, "");
  if (/^[0-9a-f]{3}$/i.test(value)) value = value.split("").map((part) => `${part}${part}`).join("");
  if (/^[0-9a-f]{6}$/i.test(value)) return value.toUpperCase();
  const parsed = parseCssColor(input);
  return parsed ? parsed.color : fallback;
}

function colorFromCss(input, fallback = "111111") {
  const parsed = parseCssColor(input);
  return parsed ? parsed.color : cleanHexColor(input, fallback);
}

function isBoldWeight(fontWeight) {
  const weight = Number.parseInt(fontWeight, 10);
  return Number.isFinite(weight) ? weight >= 600 : ["bold", "bolder"].includes(fontWeight);
}

function normalizeAlign(value) {
  if (value === "center" || value === "right" || value === "justify") return value;
  return "left";
}

function compactObject(object) {
  return Object.fromEntries(Object.entries(object).filter(([, value]) => value !== undefined && value !== null));
}

function normalizeArrowType(value, fallback = "none") {
  const allowed = new Set(["none", "arrow", "diamond", "oval", "stealth", "triangle"]);
  const normalized = String(value || "").trim().toLowerCase();
  return allowed.has(normalized) ? normalized : fallback;
}

function normalizeDashType(value) {
  const allowed = new Set(["solid", "dash", "dashDot", "lgDash", "lgDashDot", "lgDashDotDot", "sysDash", "sysDot"]);
  const normalized = String(value || "").trim();
  return allowed.has(normalized) ? normalized : undefined;
}

function pptxPoint(point, stage, deck) {
  return {
    x: ((point.left - stage.left) / stage.width) * deck.width,
    y: ((point.top - stage.top) / stage.height) * deck.height,
  };
}

function pptxSize(size, axis, stage, deck) {
  return (size / (axis === "x" ? stage.width : stage.height)) * (axis === "x" ? deck.width : deck.height);
}

function connectorArrowTypes(arrow) {
  const normalized = String(arrow || "end").toLowerCase();
  return {
    begin: normalized === "begin" || normalized === "both" ? "triangle" : "none",
    end: normalized === "end" || normalized === "both" ? "triangle" : "none",
  };
}

function connectorLineOptions(connector, arrowOverride = {}) {
  const arrows = connectorArrowTypes(connector.arrow);
  return compactObject({
    color: colorFromCss(connector.color, "64748B"),
    transparency: connector.transparency,
    width: Math.max(0.5, pxToPt(connector.width || 2)),
    beginArrowType: normalizeArrowType(connector.beginArrowType, arrowOverride.begin ?? arrows.begin),
    endArrowType: normalizeArrowType(connector.endArrowType, arrowOverride.end ?? arrows.end),
    dashType: normalizeDashType(connector.dash),
  });
}

function addConnectorLine(slide, pptx, start, end, connector, arrowOverride) {
  slide.addShape(pptx.ShapeType.line, {
    x: start.x,
    y: start.y,
    w: end.x - start.x,
    h: end.y - start.y,
    line: connectorLineOptions(connector, arrowOverride),
  });
}

function curveBounds(points) {
  const xs = points.flatMap((point) => {
    const control = point.curve ? [point.curve.x1, point.curve.x2].filter((value) => value !== undefined) : [];
    return [point.x, ...control].filter((value) => value !== undefined);
  });
  const ys = points.flatMap((point) => {
    const control = point.curve ? [point.curve.y1, point.curve.y2].filter((value) => value !== undefined) : [];
    return [point.y, ...control].filter((value) => value !== undefined);
  });
  const minX = Math.min(...xs);
  const minY = Math.min(...ys);
  const maxX = Math.max(...xs);
  const maxY = Math.max(...ys);
  return { x: minX, y: minY, w: Math.max(0.01, maxX - minX), h: Math.max(0.01, maxY - minY) };
}

function addConnectorCurve(slide, pptx, connector, stage, deck) {
  const points = (connector.curvePoints || []).map((point, index) => {
    const out = pptxPoint(point, stage, deck);
    if (index === 0) return { ...out, moveTo: true };
    if (point.curve?.type === "cubic") {
      const c1 = pptxPoint(point.curve.c1, stage, deck);
      const c2 = pptxPoint(point.curve.c2, stage, deck);
      return { ...out, curve: { type: "cubic", x1: c1.x, y1: c1.y, x2: c2.x, y2: c2.y } };
    }
    if (point.curve?.type === "quadratic") {
      const c1 = pptxPoint(point.curve.c1, stage, deck);
      return { ...out, curve: { type: "quadratic", x1: c1.x, y1: c1.y } };
    }
    return out;
  });
  if (points.length < 2) return 0;
  const bounds = curveBounds(points);
  slide.addShape(pptx.ShapeType.custGeom, {
    ...bounds,
    points: points.map((point) => {
      const local = { ...point, x: point.x - bounds.x, y: point.y - bounds.y };
      if (local.curve) {
        local.curve = { ...local.curve };
        local.curve.x1 -= bounds.x;
        local.curve.y1 -= bounds.y;
        if (local.curve.x2 !== undefined) local.curve.x2 -= bounds.x;
        if (local.curve.y2 !== undefined) local.curve.y2 -= bounds.y;
      }
      return local;
    }),
    fill: { color: "FFFFFF", transparency: 100 },
    line: connectorLineOptions(connector),
  });
  return 1;
}

function addConnectorLabel(slide, pptx, connector, stage, deck) {
  if (!connector.label?.text) return 0;
  const center = pptxPoint(connector.label.point, stage, deck);
  const w = Math.max(0.26, pptxSize(connector.label.width, "x", stage, deck));
  const h = Math.max(0.14, pptxSize(connector.label.height, "y", stage, deck));
  const box = {
    x: center.x - w / 2,
    y: center.y - h / 2,
    w,
    h,
  };
  const fill = parseCssColor(connector.label.fill);
  const line = parseCssColor(connector.label.borderColor);
  if (fill || line) {
    slide.addShape(pptx.ShapeType.roundRect, {
      ...box,
      fill: fill ? { color: fill.color, transparency: transparency(fill.alpha) } : { color: "FFFFFF", transparency: 100 },
      line: line ? { color: line.color, transparency: transparency(line.alpha), width: Math.max(0.25, pxToPt(connector.label.borderWidth || 1)) } : { color: "FFFFFF", transparency: 100 },
    });
  }
  const color = parseCssColor(connector.label.color) || { color: "D9E8F7", alpha: 1 };
  slide.addText(safeText(connector.label.text), {
    ...box,
    margin: 0.035,
    fit: "shrink",
    fontFace: fontFace(connector.label.fontFamily),
    fontSize: Math.max(5, pxToPt(connector.label.fontSize || 10)),
    color: color.color,
    transparency: transparency(color.alpha),
    bold: Boolean(connector.label.bold),
    align: "center",
    valign: "mid",
  });
  return 1;
}

function normalizeChartType(pptx, rawType) {
  const key = String(rawType || "bar").toLowerCase().replace(/[\s_-]/g, "");
  const map = {
    area: pptx.ChartType.area,
    bar: pptx.ChartType.bar,
    column: pptx.ChartType.bar,
    columns: pptx.ChartType.bar,
    doughnut: pptx.ChartType.doughnut,
    donut: pptx.ChartType.doughnut,
    line: pptx.ChartType.line,
    pie: pptx.ChartType.pie,
  };
  return map[key] || null;
}

function normalizeChartSeries(spec) {
  const labels = Array.isArray(spec?.labels) ? spec.labels.map((label) => String(label)) : [];
  const inputSeries = Array.isArray(spec?.series)
    ? spec.series
    : Array.isArray(spec?.values)
      ? [{ name: spec.name || spec.title || "Series 1", values: spec.values }]
      : [];
  return inputSeries.map((series, index) => ({
    name: String(series?.name || `Series ${index + 1}`),
    labels: Array.isArray(series?.labels) ? series.labels.map((label) => String(label)) : labels,
    values: Array.isArray(series?.values)
      ? series.values.map((value) => {
        const number = Number(value);
        return Number.isFinite(number) ? number : 0;
      })
      : [],
  })).filter((series) => series.labels.length && series.values.length);
}

function localPathFromUrl(src, htmlFile) {
  if (!src) return null;
  if (src.startsWith("data:")) return src;
  try {
    const url = new URL(src);
    if (url.protocol === "file:") return fileURLToPath(url);
  } catch {
    return path.resolve(path.dirname(htmlFile), src);
  }
  return null;
}

async function listSlides(deckDir) {
  const slidesDir = path.join(deckDir, "slides");
  let sourceDir = deckDir;
  try {
    const stat = await fs.stat(slidesDir);
    if (stat.isDirectory()) sourceDir = slidesDir;
  } catch {
    sourceDir = deckDir;
  }
  const files = (await fs.readdir(sourceDir))
    .filter((name) => name.toLowerCase().endsWith(".html") && name.toLowerCase() !== "index.html")
    .sort((a, b) => a.localeCompare(b, undefined, { numeric: true }))
    .map((name) => path.join(sourceDir, name));
  return files;
}

async function collectSlide(page) {
  return page.evaluate(() => {
    const textTags = new Set(["H1", "H2", "H3", "H4", "H5", "H6", "P", "LI", "SPAN", "SMALL", "STRONG", "EM"]);
    const rectOf = (element) => {
      const rect = element.getBoundingClientRect();
      return {
        left: rect.left,
        top: rect.top,
        width: rect.width,
        height: rect.height,
      };
    };
    const visible = (element) => {
      const style = getComputedStyle(element);
      const rect = element.getBoundingClientRect();
      return (
        style.display !== "none" &&
        style.visibility !== "hidden" &&
        Number.parseFloat(style.opacity || "1") > 0 &&
        rect.width > 0.5 &&
        rect.height > 0.5
      );
    };
    const hasRasterAncestor = (element) => {
      let current = element.parentElement;
      while (current && current !== document.body) {
        if (
          current.dataset.pptxRaster === "true" ||
          current.dataset.pptxMode === "raster" ||
          current.dataset.pptxChart !== undefined ||
          current.dataset.pptxChartSpec !== undefined ||
          current.dataset.pptxConnector !== undefined ||
          current.dataset.pptxLine !== undefined ||
          current.dataset.pptxTable === "true" ||
          current.tagName.toUpperCase() === "TABLE"
        ) return true;
        current = current.parentElement;
      }
      return false;
    };
    const importantText = (element) => {
      const own = Array.from(element.childNodes)
        .map((node) => {
          if (node.nodeType === Node.TEXT_NODE) return node.textContent || "";
          if (node.nodeType === Node.ELEMENT_NODE && node.tagName.toUpperCase() === "BR") return "\n";
          return "";
        })
        .join("");
      const normalized = own
        .replace(/\r\n?/g, "\n")
        .split("\n")
        .map((line) => line.replace(/[ \t\f\v]+/g, " ").trim())
        .filter(Boolean)
        .join("\n");
      return normalized || (element.dataset.pptxText === "true" ? element.innerText : "");
    };
    const cellData = (cell) => {
      const style = getComputedStyle(cell);
      const borderWidth = Math.max(
        Number.parseFloat(style.borderTopWidth || "0"),
        Number.parseFloat(style.borderRightWidth || "0"),
        Number.parseFloat(style.borderBottomWidth || "0"),
        Number.parseFloat(style.borderLeftWidth || "0"),
      );
      return {
        text: cell.textContent.replace(/\s+/g, " ").trim(),
        tag: cell.tagName.toUpperCase(),
        colspan: Number.parseInt(cell.getAttribute("colspan") || "1", 10),
        rowspan: Number.parseInt(cell.getAttribute("rowspan") || "1", 10),
        styles: {
          backgroundColor: style.backgroundColor,
          borderColor: style.borderTopColor,
          borderWidth,
          color: style.color,
          fontFamily: style.fontFamily,
          fontSize: Number.parseFloat(style.fontSize || "13"),
          fontWeight: style.fontWeight,
          fontStyle: style.fontStyle,
          textAlign: style.textAlign,
        },
      };
    };
    const tableData = (element) => {
      const rows = Array.from(element.querySelectorAll("tr")).map((row) => (
        Array.from(row.children)
          .filter((cell) => ["TD", "TH"].includes(cell.tagName.toUpperCase()))
          .map(cellData)
      )).filter((row) => row.length);
      return { rows };
    };
    const chartData = (element) => {
      const warnings = [];
      const script = element.querySelector('script[type="application/json"]');
      const rawAttr = element.dataset.pptxChart || element.dataset.pptxChartSpec || "";
      let spec = {};
      if (rawAttr && rawAttr !== "true") {
        if (/^\s*[{[]/.test(rawAttr)) {
          try {
            spec = JSON.parse(rawAttr);
          } catch {
            warnings.push("chart-json-invalid");
          }
        } else {
          spec.type = rawAttr;
        }
      }
      if (script && script.textContent.trim()) {
        try {
          spec = { ...spec, ...JSON.parse(script.textContent) };
        } catch {
          warnings.push("chart-json-invalid");
        }
      }
      return { spec, warnings };
    };
    const connectorData = (element) => {
      const style = getComputedStyle(element);
      const rect = element.getBoundingClientRect();
      const stageRect = document.body.getBoundingClientRect();
      const parseCoord = (value, size) => {
        const token = String(value || "").trim();
        if (token.endsWith("%")) return (Number.parseFloat(token) / 100) * size;
        const number = Number.parseFloat(token);
        return Number.isFinite(number) ? number : 0;
      };
      const parsePoint = (value, fallback) => {
        if (!value) return fallback;
        const [x, y] = String(value).split(",").map((part) => part.trim());
        return {
          left: rect.left + parseCoord(x, rect.width),
          top: rect.top + parseCoord(y, rect.height),
        };
      };
      const parseStagePoint = (value) => {
        if (!value) return null;
        const [x, y] = String(value).split(",").map((part) => part.trim());
        return {
          left: stageRect.left + parseCoord(x, stageRect.width),
          top: stageRect.top + parseCoord(y, stageRect.height),
        };
      };
      const nodeById = (id) => Array.from(document.querySelectorAll("[data-graph-node], [data-pptx-node]"))
        .find((node) => node.getAttribute("data-graph-node") === id || node.getAttribute("data-pptx-node") === id);
      const rectCenter = (nodeRect) => ({ left: nodeRect.left + nodeRect.width / 2, top: nodeRect.top + nodeRect.height / 2 });
      const anchorPoint = (nodeRect, anchor, toward) => {
        const center = rectCenter(nodeRect);
        let side = String(anchor || "auto").toLowerCase();
        if (side === "auto") {
          const dx = (toward?.left ?? center.left) - center.left;
          const dy = (toward?.top ?? center.top) - center.top;
          if (Math.abs(dx) >= Math.abs(dy)) side = dx >= 0 ? "right" : "left";
          else side = dy >= 0 ? "bottom" : "top";
        }
        const map = {
          left: { left: nodeRect.left, top: center.top },
          right: { left: nodeRect.right, top: center.top },
          top: { left: center.left, top: nodeRect.top },
          bottom: { left: center.left, top: nodeRect.bottom },
          center,
        };
        return map[side] || center;
      };
      const fromNode = element.dataset.graphFrom ? nodeById(element.dataset.graphFrom) : null;
      const toNode = element.dataset.graphTo ? nodeById(element.dataset.graphTo) : null;
      const fromNodeRect = fromNode?.getBoundingClientRect();
      const toNodeRect = toNode?.getBoundingClientRect();
      const explicitFrom = element.dataset.pptxFrom;
      const explicitTo = element.dataset.pptxTo;
      const fallbackFrom = { left: rect.left, top: rect.top + rect.height / 2 };
      const fallbackTo = { left: rect.left + rect.width, top: rect.top + rect.height / 2 };
      let from = explicitFrom ? parsePoint(explicitFrom, fallbackFrom) : fallbackFrom;
      let to = explicitTo ? parsePoint(explicitTo, fallbackTo) : fallbackTo;
      if (!explicitFrom && fromNodeRect) from = anchorPoint(fromNodeRect, element.dataset.pptxAnchorFrom || element.dataset.pptxAnchor || "auto", toNodeRect ? rectCenter(toNodeRect) : to);
      if (!explicitTo && toNodeRect) to = anchorPoint(toNodeRect, element.dataset.pptxAnchorTo || element.dataset.pptxAnchor || "auto", fromNodeRect ? rectCenter(fromNodeRect) : from);
      const parsePointList = (value) => String(value || "")
        .split(";")
        .map((part) => part.trim())
        .filter(Boolean)
        .map((part) => {
          const stageMatch = part.match(/^stage:(.+)$/i);
          return stageMatch ? parseStagePoint(stageMatch[1]) : parsePoint(part, null);
        })
        .filter(Boolean);
      const route = String(element.dataset.pptxRoute || element.dataset.graphRoute || "straight").toLowerCase();
      const waypoints = parsePointList(element.dataset.pptxWaypoints || element.dataset.graphWaypoints || "");
      const avoidIds = String(element.dataset.pptxAvoid || element.dataset.graphAvoid || "")
        .split(",")
        .map((part) => part.trim())
        .filter(Boolean);
      const avoidRects = avoidIds
        .map((id) => nodeById(id)?.getBoundingClientRect())
        .filter(Boolean)
        .map((box) => ({ left: box.left, top: box.top, right: box.right, bottom: box.bottom, width: box.width, height: box.height }));
      const gap = Number.parseFloat(element.dataset.pptxAvoidGap || "24");
      const segmentIntersects = (a, b, box) => {
        const minX = Math.min(a.left, b.left);
        const maxX = Math.max(a.left, b.left);
        const minY = Math.min(a.top, b.top);
        const maxY = Math.max(a.top, b.top);
        return maxX >= box.left - gap && minX <= box.right + gap && maxY >= box.top - gap && minY <= box.bottom + gap;
      };
      const routePoints = () => {
        if (waypoints.length) return [from, ...waypoints, to];
        if (route === "orthogonal" || route === "elbow" || route === "dogleg") {
          if (Math.abs(to.left - from.left) >= Math.abs(to.top - from.top)) {
            const midX = from.left + (to.left - from.left) * Number.parseFloat(element.dataset.pptxBend || "0.5");
            return [from, { left: midX, top: from.top }, { left: midX, top: to.top }, to];
          }
          const midY = from.top + (to.top - from.top) * Number.parseFloat(element.dataset.pptxBend || "0.5");
          return [from, { left: from.left, top: midY }, { left: to.left, top: midY }, to];
        }
        if (route === "avoid" && avoidRects.length) {
          const crosses = avoidRects.filter((box) => segmentIntersects(from, to, box));
          if (crosses.length) {
            const topLane = Math.min(...crosses.map((box) => box.top)) - gap;
            const bottomLane = Math.max(...crosses.map((box) => box.bottom)) + gap;
            const midY = topLane > stageRect.top + gap ? topLane : bottomLane;
            return [from, { left: from.left, top: midY }, { left: to.left, top: midY }, to];
          }
        }
        return [from, to];
      };
      const points = routePoints();
      const curveOffset = Number.parseFloat(element.dataset.pptxCurveOffset || "42");
      const curvePoints = () => {
        if (!["curve", "bezier", "cubic"].includes(route)) return [];
        const dx = to.left - from.left;
        const dy = to.top - from.top;
        const length = Math.max(1, Math.hypot(dx, dy));
        const nx = -dy / length;
        const ny = dx / length;
        const direction = String(element.dataset.pptxCurveDirection || "above").toLowerCase() === "below" ? -1 : 1;
        const offset = curveOffset * direction;
        return [
          { ...from },
          {
            ...to,
            curve: {
              type: "cubic",
              c1: { left: from.left + dx * 0.34 + nx * offset, top: from.top + dy * 0.34 + ny * offset },
              c2: { left: from.left + dx * 0.66 + nx * offset, top: from.top + dy * 0.66 + ny * offset },
            },
          },
        ];
      };
      const pointAt = (items, position) => {
        if (items.length <= 1) return items[0] || from;
        const lengths = [];
        let total = 0;
        for (let i = 0; i < items.length - 1; i += 1) {
          const value = Math.hypot(items[i + 1].left - items[i].left, items[i + 1].top - items[i].top);
          lengths.push(value);
          total += value;
        }
        let target = Math.max(0, Math.min(1, position)) * total;
        for (let i = 0; i < lengths.length; i += 1) {
          if (target <= lengths[i] || i === lengths.length - 1) {
            const ratio = lengths[i] ? target / lengths[i] : 0;
            return {
              left: items[i].left + (items[i + 1].left - items[i].left) * ratio,
              top: items[i].top + (items[i + 1].top - items[i].top) * ratio,
            };
          }
          target -= lengths[i];
        }
        return items[items.length - 1];
      };
      const parseOffset = (value) => {
        if (!value) return { left: 0, top: 0 };
        const [x, y] = String(value).split(",").map((part) => Number.parseFloat(part.trim()) || 0);
        return { left: x, top: y };
      };
      const labelText = element.dataset.pptxLabel || element.dataset.graphLabelText || "";
      const labelPosition = Number.parseFloat(element.dataset.pptxLabelPosition || "0.5");
      const labelOffset = parseOffset(element.dataset.pptxLabelOffset);
      const labelPoint = pointAt(points, Number.isFinite(labelPosition) ? labelPosition : 0.5);
      const labelStyle = labelText ? getComputedStyle(element) : null;
      const borderWidth = Math.max(
        Number.parseFloat(style.borderTopWidth || "0"),
        Number.parseFloat(style.borderRightWidth || "0"),
        Number.parseFloat(style.borderBottomWidth || "0"),
        Number.parseFloat(style.borderLeftWidth || "0"),
      );
      return {
        from,
        to,
        color: element.dataset.pptxColor || style.borderTopColor || style.color,
        width: Number.parseFloat(element.dataset.pptxWidth || "") || borderWidth || 2,
        arrow: element.dataset.pptxArrow || "end",
        dash: element.dataset.pptxDash || "",
        route,
        points,
        curvePoints: curvePoints(),
        label: labelText ? {
          text: labelText,
          point: { left: labelPoint.left + labelOffset.left, top: labelPoint.top + labelOffset.top },
          width: Number.parseFloat(element.dataset.pptxLabelWidth || "") || Math.max(48, labelText.length * 9),
          height: Number.parseFloat(element.dataset.pptxLabelHeight || "") || 20,
          fill: element.dataset.pptxLabelFill || "rgba(8, 20, 34, 0.92)",
          borderColor: element.dataset.pptxLabelBorder || element.dataset.pptxColor || style.borderTopColor,
          borderWidth: Number.parseFloat(element.dataset.pptxLabelBorderWidth || "1"),
          color: element.dataset.pptxLabelColor || labelStyle.color,
          fontFamily: labelStyle.fontFamily,
          fontSize: Number.parseFloat(element.dataset.pptxLabelFontSize || "") || Math.max(9, Number.parseFloat(labelStyle.fontSize || "12")),
          bold: element.dataset.pptxLabelBold === "true",
        } : null,
        beginArrowType: element.dataset.pptxBeginArrow || "",
        endArrowType: element.dataset.pptxEndArrow || "",
      };
    };

    const bodyStyle = getComputedStyle(document.body);
    const stageRect = rectOf(document.body);
    const bodyBackground = bodyStyle.backgroundColor;
    const elements = [];
    Array.from(document.body.querySelectorAll("*")).forEach((element, index) => {
      if (!visible(element)) return;
      if (element.dataset.pptx === "ignore") return;
      if (hasRasterAncestor(element)) return;

      element.setAttribute("data-pptx-adapter-id", String(index));
      const style = getComputedStyle(element);
      const tag = element.tagName.toUpperCase();
      const backgroundImage = style.backgroundImage && style.backgroundImage !== "none" ? style.backgroundImage : "";
      const isRaster = element.dataset.pptxRaster === "true" || element.dataset.pptxMode === "raster";
      const isTable = tag === "TABLE" || element.dataset.pptxTable === "true";
      const isChart = element.dataset.pptxChart !== undefined || element.dataset.pptxChartSpec !== undefined;
      const isConnector = element.dataset.pptxConnector !== undefined || element.dataset.pptxLine !== undefined;
      const borderWidth = Math.max(
        Number.parseFloat(style.borderTopWidth || "0"),
        Number.parseFloat(style.borderRightWidth || "0"),
        Number.parseFloat(style.borderBottomWidth || "0"),
        Number.parseFloat(style.borderLeftWidth || "0"),
      );
      const hasBackground = style.backgroundColor && !/^rgba\(0,\s*0,\s*0,\s*0\)$/i.test(style.backgroundColor) && style.backgroundColor !== "transparent";
      const hasBorder = borderWidth > 0 && style.borderTopStyle !== "none";
      const hasShape = isRaster || element.dataset.pptxShape || (tag !== "IMG" && (hasBackground || hasBorder));
      const text = importantText(element);
      const isText = Boolean(text) && (textTags.has(tag) || element.dataset.pptxText === "true");
      const warnings = [];
      if (backgroundImage.includes("gradient")) warnings.push("css-gradient-not-editable");
      else if (backgroundImage) warnings.push("background-image-use-img-or-raster");
      if (style.filter && style.filter !== "none") warnings.push("filter-not-editable");
      if (style.boxShadow && style.boxShadow !== "none") warnings.push("shadow-not-editable");

      if (!hasShape && !isText && tag !== "IMG" && !isTable && !isChart && !isConnector) return;

      const chart = isChart ? chartData(element) : null;
      if (chart) warnings.push(...chart.warnings);

      elements.push({
        id: String(index),
        tag,
        kind: tag === "IMG"
          ? "image"
          : isRaster
            ? "raster"
            : isTable
              ? "table"
              : isChart
                ? "chart"
                : isConnector
                  ? "connector"
                  : isText
                    ? "text"
                    : "shape",
        rect: rectOf(element),
        text,
        src: tag === "IMG" ? element.getAttribute("src") : "",
        table: isTable ? tableData(element) : null,
        chart: chart ? chart.spec : null,
        connector: isConnector ? connectorData(element) : null,
        styles: {
          backgroundColor: style.backgroundColor,
          borderColor: style.borderTopColor,
          borderWidth,
          borderRadius: Number.parseFloat(style.borderTopLeftRadius || "0"),
          color: style.color,
          fontFamily: style.fontFamily,
          fontSize: Number.parseFloat(style.fontSize || "16"),
          fontWeight: style.fontWeight,
          fontStyle: style.fontStyle,
          lineHeight: style.lineHeight,
          textAlign: style.textAlign,
          opacity: Number.parseFloat(style.opacity || "1"),
        },
        warnings,
      });
    });
    return { stageRect, bodyBackground, elements };
  });
}

async function convertSlide({ pptx, page, htmlFile, slideNo, deck, tempDir }) {
  await page.goto(pathToFileURL(htmlFile).href, { waitUntil: "networkidle" });
  const data = await collectSlide(page);
  const slide = pptx.addSlide();
  const bg = parseCssColor(data.bodyBackground);
  if (bg) slide.background = { color: bg.color };

  const stats = { slide: slideNo, file: htmlFile, shapes: 0, text: 0, images: 0, raster: 0, tables: 0, charts: 0, connectors: 0, connector_groups: 0, connector_labels: 0, warnings: [] };
  const stage = data.stageRect;

  for (const element of data.elements) {
    const box = toInches(element.rect, stage, deck);
    const warnings = element.warnings.map((warning) => `${path.basename(htmlFile)}:${element.tag}:${warning}`);
    stats.warnings.push(...warnings);

    if (element.kind === "connector") {
      const route = String(element.connector.route || "straight").toLowerCase();
      if (["curve", "bezier", "cubic"].includes(route) && element.connector.curvePoints?.length) {
        const added = addConnectorCurve(slide, pptx, element.connector, stage, deck);
        stats.connectors += added;
      } else {
        const points = (element.connector.points?.length ? element.connector.points : [element.connector.from, element.connector.to])
          .map((point) => pptxPoint(point, stage, deck));
        for (let i = 0; i < points.length - 1; i += 1) {
          const begin = i === 0 ? undefined : "none";
          const end = i === points.length - 2 ? undefined : "none";
          addConnectorLine(slide, pptx, points[i], points[i + 1], element.connector, { begin, end });
          stats.connectors += 1;
        }
      }
      stats.connector_groups += 1;
      const labelAdded = addConnectorLabel(slide, pptx, element.connector, stage, deck);
      if (labelAdded) {
        stats.connector_labels += 1;
        stats.text += 1;
        if (element.connector.label.fill || element.connector.label.borderColor) stats.shapes += 1;
      }
      continue;
    }

    if (box.w <= 0 || box.h <= 0) continue;

    if (element.kind === "raster") {
      const outPath = path.join(tempDir, `slide-${String(slideNo).padStart(2, "0")}-${element.id}.png`);
      await page.locator(`[data-pptx-adapter-id="${element.id}"]`).screenshot({ path: outPath });
      slide.addImage({ path: outPath, ...box });
      stats.raster += 1;
      continue;
    }

    if (element.kind === "image") {
      const imagePath = localPathFromUrl(element.src, htmlFile);
      if (!imagePath) {
        stats.warnings.push(`${path.basename(htmlFile)}:IMG:unsupported-image-src`);
        continue;
      }
      if (imagePath.startsWith("data:")) {
        slide.addImage({ data: imagePath, ...box });
      } else {
        slide.addImage({ path: imagePath, ...box });
      }
      stats.images += 1;
      continue;
    }

    if (element.kind === "table") {
      const rows = element.table?.rows || [];
      if (!rows.length) {
        stats.warnings.push(`${path.basename(htmlFile)}:${element.tag}:empty-table`);
        continue;
      }
      const fallbackBorder = colorFromCss(element.styles.borderColor, "CBD5E1");
      const tableRows = rows.map((row) => row.map((cell) => {
        const fill = parseCssColor(cell.styles.backgroundColor);
        const borderColor = colorFromCss(cell.styles.borderColor, fallbackBorder);
        const borderPt = Math.max(0.25, pxToPt(cell.styles.borderWidth || element.styles.borderWidth || 1));
        return {
          text: safeText(cell.text),
          options: compactObject({
            bold: cell.tag === "TH" || isBoldWeight(cell.styles.fontWeight),
            italic: cell.styles.fontStyle === "italic",
            color: colorFromCss(cell.styles.color, "111827"),
            fill: fill ? { color: fill.color, transparency: transparency(fill.alpha) } : undefined,
            fontFace: fontFace(cell.styles.fontFamily),
            fontSize: Math.max(6, pxToPt(cell.styles.fontSize || 13)),
            align: normalizeAlign(cell.styles.textAlign),
            valign: "mid",
            margin: 0.045,
            border: { type: "solid", color: borderColor, pt: borderPt },
            colspan: cell.colspan > 1 ? cell.colspan : undefined,
            rowspan: cell.rowspan > 1 ? cell.rowspan : undefined,
          }),
        };
      }));
      slide.addTable(tableRows, {
        ...box,
        margin: 0.045,
        fontFace: "Aptos",
        fontSize: 9.5,
        color: "111827",
        border: { type: "solid", color: fallbackBorder, pt: 0.5 },
        valign: "mid",
        autoFit: false,
      });
      stats.tables += 1;
      continue;
    }

    if (element.kind === "chart") {
      const chartType = normalizeChartType(pptx, element.chart?.type);
      const chartData = normalizeChartSeries(element.chart || {});
      if (!chartType) {
        stats.warnings.push(`${path.basename(htmlFile)}:${element.tag}:unsupported-chart-type`);
        continue;
      }
      if (!chartData.length) {
        stats.warnings.push(`${path.basename(htmlFile)}:${element.tag}:empty-chart-data`);
        continue;
      }
      const chartColors = Array.isArray(element.chart.colors)
        ? element.chart.colors.map((color) => cleanHexColor(color)).filter(Boolean)
        : undefined;
      const axisColor = cleanHexColor(element.chart.axisColor, colorFromCss(element.styles.color, "64748B"));
      const title = safeText(element.chart.title || "");
      slide.addChart(chartType, chartData, compactObject({
        ...box,
        showTitle: Boolean(title),
        title,
        showLegend: element.chart.showLegend === undefined ? chartData.length > 1 : Boolean(element.chart.showLegend),
        chartColors: chartColors?.length ? chartColors : undefined,
        showValue: Boolean(element.chart.showValue),
        showCategoryName: Boolean(element.chart.showCategoryName),
        showPercent: Boolean(element.chart.showPercent),
        catAxisLabelFontFace: fontFace(element.styles.fontFamily),
        valAxisLabelFontFace: fontFace(element.styles.fontFamily),
        catAxisLabelFontSize: Math.max(6, pxToPt(element.styles.fontSize || 12)),
        valAxisLabelFontSize: Math.max(6, pxToPt(element.styles.fontSize || 12)),
        catAxisLabelColor: axisColor,
        valAxisLabelColor: axisColor,
        catAxisLineColor: axisColor,
        valAxisLineColor: axisColor,
        valAxisMinVal: Number.isFinite(Number(element.chart.yMin)) ? Number(element.chart.yMin) : undefined,
        valAxisMaxVal: Number.isFinite(Number(element.chart.yMax)) ? Number(element.chart.yMax) : undefined,
      }));
      stats.charts += 1;
      continue;
    }

    if (element.kind === "shape") {
      const fill = parseCssColor(element.styles.backgroundColor);
      const line = parseCssColor(element.styles.borderColor);
      const shapeType = element.styles.borderRadius > 3 ? pptx.ShapeType.roundRect : pptx.ShapeType.rect;
      slide.addShape(shapeType, {
        ...box,
        fill: fill ? { color: fill.color, transparency: transparency(fill.alpha * element.styles.opacity) } : { color: "FFFFFF", transparency: 100 },
        line: line && element.styles.borderWidth > 0
          ? { color: line.color, transparency: transparency(line.alpha), width: pxToPt(element.styles.borderWidth) }
          : { color: "FFFFFF", transparency: 100 },
      });
      stats.shapes += 1;
      continue;
    }

    if (element.kind === "text") {
      const color = parseCssColor(element.styles.color) || { color: "111111", alpha: 1 };
      const textBox = withTextSafetyBox(box);
      slide.addText(safeText(element.text), {
        ...textBox,
        margin: 0,
        fit: "shrink",
        breakLine: false,
        fontFace: fontFace(element.styles.fontFamily),
        fontSize: Math.max(6, pxToPt(element.styles.fontSize)),
        color: color.color,
        transparency: transparency(color.alpha * element.styles.opacity),
        bold: isBoldWeight(element.styles.fontWeight),
        italic: element.styles.fontStyle === "italic",
        align: normalizeAlign(element.styles.textAlign === "start" ? "left" : element.styles.textAlign),
        valign: "top",
      });
      stats.text += 1;
    }
  }

  return stats;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help || !args.deckDir || !args.out) {
    usage();
    return args.help ? 0 : 1;
  }

  const deckDir = path.resolve(args.deckDir);
  const outPath = path.resolve(args.out);
  const reportPath = path.resolve(args.report || `${outPath}.report.json`);
  const tempDir = await fs.mkdtemp(path.join(os.tmpdir(), "ppt-craft-html2pptx-"));
  const slideFiles = await listSlides(deckDir);
  if (!slideFiles.length) throw new Error(`No slide HTML files found in ${deckDir}`);

  const pptx = new PptxGenJS();
  pptx.author = "PPT Craft";
  pptx.subject = "Editable PPTX generated from constrained HTML";
  pptx.title = args.title || path.basename(outPath, ".pptx");
  pptx.company = "PPT Craft";
  pptx.lang = "zh-CN";
  pptx.theme = {
    headFontFace: "Aptos Display",
    bodyFontFace: "Aptos",
    lang: "zh-CN",
  };
  pptx.defineLayout({ name: "PPTCRAFT_WIDE", width: args.width, height: args.height });
  pptx.layout = "PPTCRAFT_WIDE";

  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
  const deck = { width: args.width, height: args.height };
  const report = {
    engine: "ppt-craft-html-to-editable-pptx",
    deckDir,
    outPath,
    slideCount: slideFiles.length,
    layout: deck,
    slides: [],
    totals: { shapes: 0, text: 0, images: 0, raster: 0, tables: 0, charts: 0, connectors: 0, connector_groups: 0, connector_labels: 0, warnings: 0 },
  };

  try {
    for (let i = 0; i < slideFiles.length; i += 1) {
      const stats = await convertSlide({
        pptx,
        page,
        htmlFile: slideFiles[i],
        slideNo: i + 1,
        deck,
        tempDir,
      });
      report.slides.push(stats);
      report.totals.shapes += stats.shapes;
      report.totals.text += stats.text;
      report.totals.images += stats.images;
      report.totals.raster += stats.raster;
      report.totals.tables += stats.tables;
      report.totals.charts += stats.charts;
      report.totals.connectors += stats.connectors;
      report.totals.connector_groups += stats.connector_groups || 0;
      report.totals.connector_labels += stats.connector_labels || 0;
      report.totals.warnings += stats.warnings.length;
    }
  } finally {
    await browser.close();
  }

  await fs.mkdir(path.dirname(outPath), { recursive: true });
  await pptx.writeFile({ fileName: outPath });
  await fs.writeFile(reportPath, `${JSON.stringify(report, null, 2)}\n`, "utf8");

  console.log(`editable-pptx-written ${outPath}`);
  console.log(`editable-pptx-report ${reportPath}`);
  console.log(`objects text=${report.totals.text} shapes=${report.totals.shapes} images=${report.totals.images} raster=${report.totals.raster} tables=${report.totals.tables} charts=${report.totals.charts} connectors=${report.totals.connectors} connector_groups=${report.totals.connector_groups} connector_labels=${report.totals.connector_labels} warnings=${report.totals.warnings}`);
  if (args.strict && report.totals.warnings > 0) return 2;
  return 0;
}

main().then((code) => process.exit(code)).catch((error) => {
  console.error(error.stack || String(error));
  process.exit(1);
});
