#!/usr/bin/env node
import { createRequire } from "node:module";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";

const require = createRequire(import.meta.url);

function loadModule(name) {
  try {
    return require(name);
  } catch {
    const bundled = path.join(
      os.homedir(),
      ".cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules",
      name,
    );
    return require(bundled);
  }
}

const { chromium } = loadModule("playwright");

function parseArgs(argv) {
  const args = {
    failOn: "warning",
    requirePptxNative: false,
    requireLayering: false,
    requireRelationTypes: false,
    requireActivePath: false,
    requireConnectorAnchors: false,
    requireConnectorLabels: false,
    requireEdgeBundling: false,
    requireLabelScores: false,
    requireSwimlanes: false,
    requireSubgraphCollapse: false,
    maxEdgeCrossings: null,
    maxLabelOverlaps: null,
    maxNodeCrowding: null,
    maxEdgeDensity: null,
    minLayers: 2,
    maxEdgeStyles: 6,
    out: null,
    markdown: null,
  };
  const positional = [];
  for (let i = 0; i < argv.length; i += 1) {
    const value = argv[i];
    if (value === "--out") args.out = argv[++i];
    else if (value === "--markdown") args.markdown = argv[++i];
    else if (value === "--fail-on") args.failOn = argv[++i];
    else if (value === "--require-pptx-native") args.requirePptxNative = true;
    else if (value === "--require-layering") args.requireLayering = true;
    else if (value === "--require-relation-types") args.requireRelationTypes = true;
    else if (value === "--require-active-path") args.requireActivePath = true;
    else if (value === "--require-connector-anchors") args.requireConnectorAnchors = true;
    else if (value === "--require-connector-labels") args.requireConnectorLabels = true;
    else if (value === "--require-edge-bundling") args.requireEdgeBundling = true;
    else if (value === "--require-label-scores") args.requireLabelScores = true;
    else if (value === "--require-swimlanes") args.requireSwimlanes = true;
    else if (value === "--require-subgraph-collapse") args.requireSubgraphCollapse = true;
    else if (value === "--max-edge-crossings") args.maxEdgeCrossings = Number(argv[++i]);
    else if (value === "--max-label-overlaps") args.maxLabelOverlaps = Number(argv[++i]);
    else if (value === "--max-node-crowding") args.maxNodeCrowding = Number(argv[++i]);
    else if (value === "--max-edge-density") args.maxEdgeDensity = Number(argv[++i]);
    else if (value === "--min-layers") args.minLayers = Number(argv[++i]);
    else if (value === "--max-edge-styles") args.maxEdgeStyles = Number(argv[++i]);
    else if (value === "--help" || value === "-h") args.help = true;
    else positional.push(value);
  }
  args.deckDir = positional[0];
  return args;
}

function usage() {
  console.log(`Usage:
  node scripts/inspect_relationship_graph.mjs <deck-dir> [--out qa/relationship-graph-report.json]

Checks HTML/SVG relationship diagrams before PPT/PDF export.

Data contract:
  - nodes: [data-graph-node="node-id"]
  - edges: [data-graph-edge="edge-id"]
  - PPTX-native edges: [data-pptx-connector] or [data-pptx-line]
  - semantic endpoints: data-graph-from="node-id" data-graph-to="node-id"
  - PPTX endpoints: data-pptx-from="0,50%" data-pptx-to="100%,50%"
  - PPTX anchors: data-pptx-anchor-from="right" data-pptx-anchor-to="left" or graph-node auto anchors
  - PPTX routes: data-pptx-route="straight|orthogonal|elbow|avoid|curve"
  - PPTX labels: data-pptx-label="why this edge matters"
  - edge bundles: data-graph-bundle="input-to-reasoning"
  - label scores: data-graph-label-score="0"
  - swimlanes: data-graph-swimlane="enterprise|clinical|privacy"
  - collapsed nodes: data-graph-collapsed="true"
  - layers: data-graph-layer="signal|engine|decision"
  - relation semantics: data-graph-relation="feeds|proves|blocks|triggers|loops"
`);
}

async function listSlides(deckDir) {
  const slidesDir = path.join(deckDir, "slides");
  let sourceDir = deckDir;
  try {
    const stat = await fs.stat(slidesDir);
    if (stat.isDirectory()) sourceDir = slidesDir;
  } catch {}
  return (await fs.readdir(sourceDir))
    .filter((name) => name.endsWith(".html") && name.toLowerCase() !== "index.html")
    .sort((a, b) => a.localeCompare(b, undefined, { numeric: true }))
    .map((name) => ({ file: path.join(sourceDir, name), name: name.replace(/\.html$/i, "") }));
}

function finding(severity, check, slide, message, details = {}) {
  return { severity, check, slide, message, details };
}

function writeMarkdown(pathname, report) {
  const lines = [
    "# Relationship Graph Report",
    "",
    `- deck: \`${report.deck}\``,
    `- slides: ${report.summary.slides}`,
    `- graph_slides: ${report.summary.graph_slides}`,
    `- nodes: ${report.summary.nodes}`,
    `- native_edges: ${report.summary.native_edges}`,
    `- svg_edges: ${report.summary.svg_edges}`,
    `- routed_edges: ${report.summary.routed_edges}`,
    `- anchored_edges: ${report.summary.anchored_edges}`,
    `- labeled_edges: ${report.summary.labeled_edges}`,
    `- bundled_edges: ${report.summary.bundled_edges}`,
    `- edge_bundles: ${report.summary.edge_bundles}`,
    `- edge_crossings: ${report.summary.edge_crossings}`,
    `- label_overlaps: ${report.summary.label_overlaps}`,
    `- label_scored_edges: ${report.summary.label_scored_edges}`,
    `- swimlanes: ${report.summary.swimlanes}`,
    `- collapsed_nodes: ${report.summary.collapsed_nodes}`,
    `- node_crowding_score: ${report.summary.node_crowding_score}`,
    `- edge_density_peak: ${report.summary.edge_density_peak}`,
    `- errors: ${report.summary.errors}`,
    `- warnings: ${report.summary.warnings}`,
    "",
    "## Findings",
    "",
  ];
  if (!report.findings.length) {
    lines.push("No relationship graph findings.");
  } else {
    for (const item of report.findings) {
      lines.push(`- **${item.severity}** \`${item.check}\` \`${item.slide}\` - ${item.message}`);
    }
  }
  lines.push("", "## Layer Summary", "");
  for (const slide of report.slides) {
    if (!slide.nodes.length && !slide.native_edges.length && !slide.svg_edges.length) continue;
    lines.push(`- \`${slide.file}\`: layers=${slide.layers.join(", ") || "none"} swimlanes=${slide.swimlanes} active_edges=${slide.active_edges} routed_edges=${slide.routed_edges} bundled_edges=${slide.bundled_edges} crossings=${slide.edge_crossings} label_overlaps=${slide.label_overlaps} crowding=${slide.node_crowding_score} density_peak=${slide.edge_density_peak}`);
  }
  return fs.writeFile(pathname, `${lines.join("\n")}\n`, "utf8");
}

async function collectSlide(page, file, slideName) {
  await page.goto(pathToFileURL(file).href, { waitUntil: "networkidle" });
  await page.waitForTimeout(300);
  return page.evaluate(({ slideName }) => {
    const stageEl = document.querySelector(".slide") || document.body;
    const stageRect = stageEl.getBoundingClientRect();
    const round = (value) => Math.round(value * 10) / 10;
    const relRect = (element) => {
      const rect = element.getBoundingClientRect();
      return {
        x: round(rect.left - stageRect.left),
        y: round(rect.top - stageRect.top),
        w: round(rect.width),
        h: round(rect.height),
      };
    };
    const label = (element) => {
      const tag = element.tagName.toLowerCase();
      const cls = typeof element.className === "string" && element.className.trim()
        ? `.${element.className.trim().replace(/\s+/g, ".")}`
        : "";
      return `${tag}${cls}`;
    };
    const visible = (element) => {
      const style = getComputedStyle(element);
      const rect = element.getBoundingClientRect();
      return (
        style.display !== "none" &&
        style.visibility !== "hidden" &&
        Number.parseFloat(style.opacity || "1") > 0.02 &&
        rect.width > 0.5 &&
        rect.height > 0.5
      );
    };
    const all = Array.from(document.querySelectorAll("body *")).filter(visible);
    const nodes = all
      .filter((element) => element.hasAttribute("data-graph-node") || element.hasAttribute("data-pptx-node"))
      .map((element) => ({
        element: label(element),
        id: element.getAttribute("data-graph-node") || element.getAttribute("data-pptx-node") || "",
        role: element.getAttribute("data-graph-role") || "",
        layer: element.getAttribute("data-graph-layer") || "",
        cluster: element.getAttribute("data-graph-cluster") || "",
        swimlane: element.getAttribute("data-graph-swimlane") || "",
        collapsed: element.getAttribute("data-graph-collapsed") === "true",
        priority: element.getAttribute("data-graph-priority") || "",
        active: element.getAttribute("data-graph-active") === "true",
        rect: relRect(element),
      }));
    const parseCoord = (value, size) => {
      const token = String(value || "").trim();
      if (token.endsWith("%")) return (Number.parseFloat(token) / 100) * size;
      const number = Number.parseFloat(token);
      return Number.isFinite(number) ? number : 0;
    };
    const parseLocalPoint = (value, rect, fallback) => {
      if (!value) return fallback;
      const [x, y] = String(value).split(",").map((part) => part.trim());
      return {
        x: rect.x + parseCoord(x, rect.w),
        y: rect.y + parseCoord(y, rect.h),
      };
    };
    const parseStagePoint = (value) => {
      const [x, y] = String(value || "").split(",").map((part) => part.trim());
      return {
        x: parseCoord(x, stageRect.width),
        y: parseCoord(y, stageRect.height),
      };
    };
    const parseWaypoints = (value, rect) => String(value || "")
      .split(";")
      .map((part) => part.trim())
      .filter(Boolean)
      .map((part) => {
        const stageMatch = part.match(/^stage:(.+)$/i);
        return stageMatch ? parseStagePoint(stageMatch[1]) : parseLocalPoint(part, rect, null);
      })
      .filter(Boolean);
    const orthogonalPoints = (from, to) => {
      if (Math.abs(to.x - from.x) >= Math.abs(to.y - from.y)) {
        const midX = from.x + (to.x - from.x) * 0.5;
        return [from, { x: midX, y: from.y }, { x: midX, y: to.y }, to];
      }
      const midY = from.y + (to.y - from.y) * 0.5;
      return [from, { x: from.x, y: midY }, { x: to.x, y: midY }, to];
    };
    const nativeEdges = all
      .filter((element) => element.hasAttribute("data-pptx-connector") || element.hasAttribute("data-pptx-line"))
      .map((element) => {
        const rect = relRect(element);
        const route = element.getAttribute("data-pptx-route") || element.getAttribute("data-graph-route") || "straight";
        const from = parseLocalPoint(element.getAttribute("data-pptx-from"), rect, { x: rect.x, y: rect.y + rect.h / 2 });
        const to = parseLocalPoint(element.getAttribute("data-pptx-to"), rect, { x: rect.x + rect.w, y: rect.y + rect.h / 2 });
        const waypoints = parseWaypoints(element.getAttribute("data-pptx-waypoints") || element.getAttribute("data-graph-waypoints") || "", rect);
        const points = waypoints.length
          ? [from, ...waypoints, to]
          : (["orthogonal", "elbow", "dogleg", "avoid"].includes(route) ? orthogonalPoints(from, to) : [from, to]);
        return {
          element: label(element),
          id: element.getAttribute("data-graph-edge") || "",
          from: element.getAttribute("data-graph-from") || "",
          to: element.getAttribute("data-graph-to") || "",
          relation: element.getAttribute("data-graph-relation") || "",
          layer: element.getAttribute("data-graph-layer") || "",
          strength: element.getAttribute("data-graph-strength") || "",
          active: element.getAttribute("data-graph-active") === "true",
          pptxFrom: element.getAttribute("data-pptx-from") || "",
          pptxTo: element.getAttribute("data-pptx-to") || "",
          route,
          anchorFrom: element.getAttribute("data-pptx-anchor-from") || element.getAttribute("data-pptx-anchor") || "",
          anchorTo: element.getAttribute("data-pptx-anchor-to") || element.getAttribute("data-pptx-anchor") || "",
          waypoints: element.getAttribute("data-pptx-waypoints") || element.getAttribute("data-graph-waypoints") || "",
          avoid: element.getAttribute("data-pptx-avoid") || element.getAttribute("data-graph-avoid") || "",
          bundle: element.getAttribute("data-graph-bundle") || "",
          bundleLane: element.getAttribute("data-graph-bundle-lane") || "",
          label: element.getAttribute("data-pptx-label") || element.getAttribute("data-graph-label-text") || "",
          labelScore: Number.parseFloat(element.getAttribute("data-graph-label-score") || ""),
          arrow: element.getAttribute("data-pptx-arrow") || "",
          color: element.getAttribute("data-pptx-color") || getComputedStyle(element).borderTopColor || "",
          width: element.getAttribute("data-pptx-width") || getComputedStyle(element).borderTopWidth || "",
          dash: element.getAttribute("data-pptx-dash") || "",
          rect,
          points: points.map((point) => ({ x: round(point.x), y: round(point.y) })),
        };
      });
    const svgEdges = Array.from(document.querySelectorAll("svg line, svg path, svg polyline"))
      .filter(visible)
      .map((element) => ({
        element: label(element),
        id: element.getAttribute("data-graph-edge") || "",
        from: element.getAttribute("data-graph-from") || "",
        to: element.getAttribute("data-graph-to") || "",
        relation: element.getAttribute("data-graph-relation") || "",
        layer: element.getAttribute("data-graph-layer") || "",
        active: element.getAttribute("data-graph-active") === "true",
        rasterIntentional: Boolean(element.closest("[data-pptx-raster='true'], [data-pptx-mode='raster']")),
        rect: relRect(element),
      }));
    const labels = all
      .filter((element) => element.hasAttribute("data-graph-label"))
      .map((element) => ({
        element: label(element),
        id: element.getAttribute("data-graph-label") || "",
        isEdgeLabel: element.classList.contains("edge-label"),
        text: (element.textContent || "").replace(/\s+/g, " ").trim().slice(0, 120),
        rect: relRect(element),
      }));
    const edgeIds = new Set(nativeEdges.map((edge) => edge.id).filter(Boolean));
    const edgeLabels = labels.filter((item) => item.isEdgeLabel && edgeIds.has(item.id));
    const rectOverlap = (a, b, padding = 0) => !(
      a.x + a.w < b.x - padding ||
      b.x + b.w < a.x - padding ||
      a.y + a.h < b.y - padding ||
      b.y + b.h < a.y - padding
    );
    const orientation = (a, b, c) => ((b.y - a.y) * (c.x - b.x)) - ((b.x - a.x) * (c.y - b.y));
    const near = (a, b) => Math.abs(a.x - b.x) < 1.5 && Math.abs(a.y - b.y) < 1.5;
    const segmentsIntersect = (a, b, c, d) => {
      if (near(a, c) || near(a, d) || near(b, c) || near(b, d)) return false;
      const minAx = Math.min(a.x, b.x);
      const maxAx = Math.max(a.x, b.x);
      const minAy = Math.min(a.y, b.y);
      const maxAy = Math.max(a.y, b.y);
      const minCx = Math.min(c.x, d.x);
      const maxCx = Math.max(c.x, d.x);
      const minCy = Math.min(c.y, d.y);
      const maxCy = Math.max(c.y, d.y);
      if (maxAx < minCx || maxCx < minAx || maxAy < minCy || maxCy < minAy) return false;
      const o1 = orientation(a, b, c);
      const o2 = orientation(a, b, d);
      const o3 = orientation(c, d, a);
      const o4 = orientation(c, d, b);
      return o1 * o2 < 0 && o3 * o4 < 0;
    };
    const edgeSegments = nativeEdges.map((edge) => ({
      edge,
      segments: edge.points.slice(0, -1).map((point, index) => [point, edge.points[index + 1]]),
    }));
    let edgeCrossings = 0;
    const edgeCrossingPairs = [];
    for (let i = 0; i < edgeSegments.length; i += 1) {
      for (let j = i + 1; j < edgeSegments.length; j += 1) {
        const first = edgeSegments[i].edge;
        const second = edgeSegments[j].edge;
        if (first.from === second.from || first.from === second.to || first.to === second.from || first.to === second.to) continue;
        if (first.bundle && first.bundle === second.bundle) continue;
        let crossed = false;
        for (const [a, b] of edgeSegments[i].segments) {
          for (const [c, d] of edgeSegments[j].segments) {
            if (segmentsIntersect(a, b, c, d)) crossed = true;
          }
        }
        if (crossed) {
          edgeCrossings += 1;
          edgeCrossingPairs.push([first.id || first.element, second.id || second.element]);
        }
      }
    }
    let labelOverlaps = 0;
    const labelOverlapPairs = [];
    for (const item of edgeLabels) {
      for (const node of nodes) {
        if (rectOverlap(item.rect, node.rect, 3)) {
          labelOverlaps += 1;
          labelOverlapPairs.push([item.id || item.text, node.id || node.element]);
        }
      }
    }
    for (let i = 0; i < edgeLabels.length; i += 1) {
      for (let j = i + 1; j < edgeLabels.length; j += 1) {
        if (rectOverlap(edgeLabels[i].rect, edgeLabels[j].rect, 2)) {
          labelOverlaps += 1;
          labelOverlapPairs.push([edgeLabels[i].id || edgeLabels[i].text, edgeLabels[j].id || edgeLabels[j].text]);
        }
      }
    }
    const rectDistance = (a, b) => {
      const dx = Math.max(a.x - (b.x + b.w), b.x - (a.x + a.w), 0);
      const dy = Math.max(a.y - (b.y + b.h), b.y - (a.y + a.h), 0);
      return Math.sqrt(dx * dx + dy * dy);
    };
    let nodeOverlaps = 0;
    let nodeCrowdingScore = 0;
    let minNodeGap = Number.POSITIVE_INFINITY;
    for (let i = 0; i < nodes.length; i += 1) {
      for (let j = i + 1; j < nodes.length; j += 1) {
        const gap = rectDistance(nodes[i].rect, nodes[j].rect);
        minNodeGap = Math.min(minNodeGap, gap);
        if (rectOverlap(nodes[i].rect, nodes[j].rect, 1)) {
          nodeOverlaps += 1;
          nodeCrowdingScore += 4;
        } else if (gap < 16) {
          nodeCrowdingScore += (16 - gap) / 16;
        }
      }
    }
    const segmentAabbIntersects = (a, b, box) => {
      const minX = Math.min(a.x, b.x);
      const maxX = Math.max(a.x, b.x);
      const minY = Math.min(a.y, b.y);
      const maxY = Math.max(a.y, b.y);
      return maxX >= box.x && minX <= box.x + box.w && maxY >= box.y && minY <= box.y + box.h;
    };
    const densityCols = 8;
    const densityRows = 5;
    const densityGrid = Array.from({ length: densityRows }, () => Array.from({ length: densityCols }, () => 0));
    for (const item of edgeSegments) {
      for (const [a, b] of item.segments) {
        for (let row = 0; row < densityRows; row += 1) {
          for (let col = 0; col < densityCols; col += 1) {
            const cell = {
              x: (stageRect.width / densityCols) * col,
              y: (stageRect.height / densityRows) * row,
              w: stageRect.width / densityCols,
              h: stageRect.height / densityRows,
            };
            if (segmentAabbIntersects(a, b, cell)) densityGrid[row][col] += 1;
          }
        }
      }
    }
    const edgeDensityPeak = Math.max(0, ...densityGrid.flat());
    const edgeDensityHotThreshold = Math.max(5, Math.ceil(nativeEdges.length * 0.28));
    const edgeDensityHotCells = densityGrid.flat().filter((value) => value >= edgeDensityHotThreshold).length;
    const bundleIds = Array.from(new Set(nativeEdges.map((edge) => edge.bundle).filter(Boolean)));
    const swimlaneIds = Array.from(new Set([
      ...nodes.map((node) => node.swimlane).filter(Boolean),
      ...Array.from(document.querySelectorAll("[data-graph-swimlane]")).map((element) => element.getAttribute("data-graph-swimlane") || "").filter(Boolean),
    ]));
    return {
      file: slideName,
      stage: { w: round(stageRect.width), h: round(stageRect.height) },
      nodes,
      native_edges: nativeEdges,
      svg_edges: svgEdges,
      labels,
      layers: Array.from(new Set([
        ...nodes.map((node) => node.layer).filter(Boolean),
        ...nativeEdges.map((edge) => edge.layer).filter(Boolean),
        ...svgEdges.map((edge) => edge.layer).filter(Boolean),
      ])).sort(),
      active_edges: nativeEdges.filter((edge) => edge.active).length + svgEdges.filter((edge) => edge.active).length,
      routed_edges: nativeEdges.filter((edge) => edge.route && edge.route !== "straight").length,
      anchored_edges: nativeEdges.filter((edge) => edge.anchorFrom || edge.anchorTo || ((!edge.pptxFrom || !edge.pptxTo) && edge.from && edge.to)).length,
      labeled_edges: nativeEdges.filter((edge) => edge.label).length,
      bundled_edges: nativeEdges.filter((edge) => edge.bundle).length,
      edge_bundles: bundleIds.length,
      edge_crossings: edgeCrossings,
      edge_crossing_pairs: edgeCrossingPairs.slice(0, 12),
      label_overlaps: labelOverlaps,
      label_overlap_pairs: labelOverlapPairs.slice(0, 12),
      label_scored_edges: nativeEdges.filter((edge) => edge.label && Number.isFinite(edge.labelScore)).length,
      swimlanes: swimlaneIds.length,
      collapsed_nodes: nodes.filter((node) => node.collapsed).length,
      node_overlaps: nodeOverlaps,
      node_crowding_score: Math.round(nodeCrowdingScore * 100) / 100,
      min_node_gap: Number.isFinite(minNodeGap) ? Math.round(minNodeGap * 10) / 10 : 0,
      edge_density_peak: edgeDensityPeak,
      edge_density_hot_cells: edgeDensityHotCells,
      edge_density_grid: densityGrid,
    };
  }, { slideName });
}

function outsideStage(rect, stage, tolerance = 2) {
  return (
    rect.x < -tolerance ||
    rect.y < -tolerance ||
    rect.x + rect.w > stage.w + tolerance ||
    rect.y + rect.h > stage.h + tolerance
  );
}

function analyzeSlide(slide, args) {
  const findings = [];
  const graphLike = slide.nodes.length || slide.native_edges.length || slide.svg_edges.length || slide.labels.length;
  if (!graphLike) return findings;

  const nodeIds = new Set(slide.nodes.map((node) => node.id).filter(Boolean));
  const layerIds = new Set(slide.layers);
  const denseGraph = slide.nodes.length >= 5 || slide.native_edges.length + slide.svg_edges.length >= 6;

  if (args.requireLayering || denseGraph) {
    if (layerIds.size < args.minLayers) {
      findings.push(finding(
        args.requireLayering ? "error" : "warning",
        "graph-layering",
        slide.file,
        `Graph should use at least ${args.minLayers} semantic layers; found ${layerIds.size}.`,
        { layers: slide.layers, nodes: slide.nodes.length, edges: slide.native_edges.length + slide.svg_edges.length },
      ));
    }
  }
  if (args.requireActivePath && slide.active_edges === 0) {
    findings.push(finding("error", "graph-active-path", slide.file, "Complex graph needs at least one active edge/path to guide attention.", {}));
  } else if (denseGraph && slide.active_edges === 0) {
    findings.push(finding("warning", "graph-active-path", slide.file, "Dense graph has no active edge/path; viewer may not know what to read first.", {}));
  }
  if (args.requireConnectorLabels && slide.native_edges.length > 0 && slide.labeled_edges === 0) {
    findings.push(finding("error", "graph-edge-labels", slide.file, "At least one native connector label is required for this graph smoke/route.", {}));
  }
  if (args.requireEdgeBundling && denseGraph && slide.bundled_edges === 0) {
    findings.push(finding("error", "graph-edge-bundling", slide.file, "Dense native graph should bundle parallel layer-to-layer edges with data-graph-bundle.", {}));
  }
  if (args.requireLabelScores && slide.labeled_edges > 0 && slide.label_scored_edges < slide.labeled_edges) {
    findings.push(finding("error", "graph-label-scoring", slide.file, "Native edge labels should expose data-graph-label-score from placement scoring.", {
      labeled_edges: slide.labeled_edges,
      label_scored_edges: slide.label_scored_edges,
    }));
  }
  if (args.maxEdgeCrossings !== null && slide.edge_crossings > args.maxEdgeCrossings) {
    findings.push(finding("error", "graph-edge-crossings", slide.file, `Graph has ${slide.edge_crossings} edge crossings; max allowed is ${args.maxEdgeCrossings}.`, {
      crossing_pairs: slide.edge_crossing_pairs,
    }));
  }
  if (args.maxLabelOverlaps !== null && slide.label_overlaps > args.maxLabelOverlaps) {
    findings.push(finding("error", "graph-label-overlaps", slide.file, `Graph has ${slide.label_overlaps} label/node overlaps; max allowed is ${args.maxLabelOverlaps}.`, {
      overlap_pairs: slide.label_overlap_pairs,
    }));
  }
  if (args.requireSwimlanes && denseGraph && slide.swimlanes === 0) {
    findings.push(finding("error", "graph-swimlanes", slide.file, "Dense business graph should declare swimlanes or groups with data-graph-swimlane.", {}));
  }
  if (args.requireSubgraphCollapse && denseGraph && slide.collapsed_nodes === 0) {
    findings.push(finding("error", "graph-subgraph-collapse", slide.file, "Dense business graph should collapse at least one repeated/detail subgraph into an aggregate node.", {}));
  }
  if (args.maxNodeCrowding !== null && slide.node_crowding_score > args.maxNodeCrowding) {
    findings.push(finding("error", "graph-node-crowding", slide.file, `Graph node crowding score is ${slide.node_crowding_score}; max allowed is ${args.maxNodeCrowding}.`, {
      node_overlaps: slide.node_overlaps,
      min_node_gap: slide.min_node_gap,
    }));
  }
  if (args.maxEdgeDensity !== null && slide.edge_density_peak > args.maxEdgeDensity) {
    findings.push(finding("error", "graph-edge-density", slide.file, `Graph edge density peak is ${slide.edge_density_peak}; max allowed is ${args.maxEdgeDensity}.`, {
      edge_density_hot_cells: slide.edge_density_hot_cells,
    }));
  }

  for (const node of slide.nodes) {
    if (!node.id) {
      findings.push(finding("warning", "graph-node-id", slide.file, "Graph node is missing a stable data-graph-node id.", node));
    }
    if (outsideStage(node.rect, slide.stage)) {
      findings.push(finding("error", "graph-node-stage", slide.file, `Graph node is outside the slide stage: ${node.id || node.element}`, node));
    }
    if ((args.requireLayering || denseGraph) && !node.layer) {
      findings.push(finding(args.requireLayering ? "error" : "warning", "graph-node-layer", slide.file, `Graph node has no data-graph-layer: ${node.id || node.element}`, node));
    }
    if (args.requireSwimlanes && denseGraph && !node.swimlane) {
      findings.push(finding("error", "graph-node-swimlane", slide.file, `Graph node has no data-graph-swimlane: ${node.id || node.element}`, node));
    }
  }

  for (const edge of slide.native_edges) {
    if (!edge.id) {
      findings.push(finding("warning", "graph-edge-id", slide.file, "Native connector is missing data-graph-edge id.", edge));
    }
    if (!edge.from || !edge.to) {
      findings.push(finding("warning", "graph-edge-semantics", slide.file, `Native connector lacks data-graph-from/to: ${edge.id || edge.element}`, edge));
    } else {
      if (!nodeIds.has(edge.from)) {
        findings.push(finding("error", "graph-edge-endpoint", slide.file, `Edge starts from unknown node: ${edge.from}`, edge));
      }
      if (!nodeIds.has(edge.to)) {
        findings.push(finding("error", "graph-edge-endpoint", slide.file, `Edge points to unknown node: ${edge.to}`, edge));
      }
    }
    const autoAnchored = edge.from && edge.to && !edge.pptxFrom && !edge.pptxTo;
    if ((!edge.pptxFrom || !edge.pptxTo) && !autoAnchored) {
      findings.push(finding("warning", "pptx-edge-coordinates", slide.file, `Native connector should declare data-pptx-from/to or rely on graph-node anchors for stable export: ${edge.id || edge.element}`, edge));
    }
    if (args.requireConnectorAnchors && !(edge.anchorFrom || edge.anchorTo || autoAnchored)) {
      findings.push(finding("error", "pptx-edge-anchors", slide.file, `Native connector should declare anchor attrs or use graph-node auto anchors: ${edge.id || edge.element}`, edge));
    }
    if ((args.requireLayering || denseGraph) && !edge.layer) {
      findings.push(finding(args.requireLayering ? "error" : "warning", "graph-edge-layer", slide.file, `Native connector has no data-graph-layer: ${edge.id || edge.element}`, edge));
    }
    if ((args.requireRelationTypes || denseGraph) && !edge.relation) {
      findings.push(finding(args.requireRelationTypes ? "error" : "warning", "graph-edge-relation", slide.file, `Native connector has no data-graph-relation: ${edge.id || edge.element}`, edge));
    }
    if (outsideStage(edge.rect, slide.stage, 6)) {
      findings.push(finding("error", "graph-edge-stage", slide.file, `Native connector is outside the slide stage: ${edge.id || edge.element}`, edge));
    }
  }

  for (const edge of slide.svg_edges) {
    if (args.requirePptxNative && !edge.rasterIntentional) {
      findings.push(finding("error", "svg-edge-native-export", slide.file, `SVG edge is not native-PPTX exportable unless marked raster: ${edge.id || edge.element}`, edge));
    } else if (!edge.rasterIntentional) {
      findings.push(finding("warning", "svg-edge-export", slide.file, `SVG edge may rasterize in PPTX; use data-pptx-connector or mark the group raster intentionally: ${edge.id || edge.element}`, edge));
    }
    if (edge.from && !nodeIds.has(edge.from)) {
      findings.push(finding("error", "graph-edge-endpoint", slide.file, `SVG edge starts from unknown node: ${edge.from}`, edge));
    }
    if (edge.to && !nodeIds.has(edge.to)) {
      findings.push(finding("error", "graph-edge-endpoint", slide.file, `SVG edge points to unknown node: ${edge.to}`, edge));
    }
    if ((args.requireLayering || denseGraph) && !edge.layer) {
      findings.push(finding(args.requireLayering ? "error" : "warning", "graph-edge-layer", slide.file, `SVG edge has no data-graph-layer: ${edge.id || edge.element}`, edge));
    }
    if ((args.requireRelationTypes || denseGraph) && !edge.relation) {
      findings.push(finding(args.requireRelationTypes ? "error" : "warning", "graph-edge-relation", slide.file, `SVG edge has no data-graph-relation: ${edge.id || edge.element}`, edge));
    }
  }

  const edgeStyleKeys = new Set(slide.native_edges.map((edge) => [
    edge.color || "no-color",
    edge.width || "no-width",
    edge.dash || "solid",
    edge.arrow || "none",
  ].join("|")));
  if (edgeStyleKeys.size > args.maxEdgeStyles) {
    findings.push(finding(
      "warning",
      "graph-edge-style-count",
      slide.file,
      `Graph uses ${edgeStyleKeys.size} native edge styles; keep styles purposeful and mapped to relation/layer.`,
      { max_edge_styles: args.maxEdgeStyles, styles: Array.from(edgeStyleKeys) },
    ));
  }

  if (slide.nodes.length >= 3 && slide.native_edges.length + slide.svg_edges.length === 0) {
    findings.push(finding("warning", "graph-missing-edges", slide.file, "Slide declares several graph nodes but no graph edges.", { nodes: slide.nodes.length }));
  }
  if (slide.native_edges.length + slide.svg_edges.length >= 3 && slide.nodes.length === 0) {
    findings.push(finding("warning", "graph-missing-nodes", slide.file, "Slide declares several graph edges but no graph nodes.", { edges: slide.native_edges.length + slide.svg_edges.length }));
  }

  return findings;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help || !args.deckDir) {
    usage();
    return args.help ? 0 : 2;
  }
  if (!["error", "warning", "none"].includes(args.failOn)) {
    console.error("--fail-on must be error, warning, or none");
    return 2;
  }
  const deckDir = path.resolve(args.deckDir);
  const outPath = path.resolve(args.out || path.join(deckDir, "qa", "relationship-graph-report.json"));
  const markdownPath = path.resolve(args.markdown || path.join(path.dirname(outPath), "relationship-graph-report.md"));
  const slides = await listSlides(deckDir);
  if (!slides.length) {
    console.error(`No slides/*.html found under ${deckDir}`);
    return 2;
  }

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const slideReports = [];
  for (const slide of slides) {
    slideReports.push(await collectSlide(page, slide.file, slide.name));
  }
  await browser.close();

  const findings = slideReports.flatMap((slide) => analyzeSlide(slide, args));
  findings.sort((a, b) => {
    const severity = { error: 0, warning: 1 };
    return (severity[a.severity] ?? 2) - (severity[b.severity] ?? 2) || a.slide.localeCompare(b.slide);
  });
  const errors = findings.filter((item) => item.severity === "error").length;
  const warnings = findings.filter((item) => item.severity === "warning").length;
  const report = {
    generated_by: "ppt-craft/scripts/inspect_relationship_graph.mjs",
    deck: deckDir,
    summary: {
      slides: slideReports.length,
      graph_slides: slideReports.filter((slide) => slide.nodes.length || slide.native_edges.length || slide.svg_edges.length || slide.labels.length).length,
      nodes: slideReports.reduce((sum, slide) => sum + slide.nodes.length, 0),
      native_edges: slideReports.reduce((sum, slide) => sum + slide.native_edges.length, 0),
      svg_edges: slideReports.reduce((sum, slide) => sum + slide.svg_edges.length, 0),
      labels: slideReports.reduce((sum, slide) => sum + slide.labels.length, 0),
      layers: Array.from(new Set(slideReports.flatMap((slide) => slide.layers))).sort(),
      active_edges: slideReports.reduce((sum, slide) => sum + slide.active_edges, 0),
      routed_edges: slideReports.reduce((sum, slide) => sum + slide.routed_edges, 0),
      anchored_edges: slideReports.reduce((sum, slide) => sum + slide.anchored_edges, 0),
      labeled_edges: slideReports.reduce((sum, slide) => sum + slide.labeled_edges, 0),
      bundled_edges: slideReports.reduce((sum, slide) => sum + slide.bundled_edges, 0),
      edge_bundles: slideReports.reduce((sum, slide) => sum + slide.edge_bundles, 0),
      edge_crossings: slideReports.reduce((sum, slide) => sum + slide.edge_crossings, 0),
      label_overlaps: slideReports.reduce((sum, slide) => sum + slide.label_overlaps, 0),
      label_scored_edges: slideReports.reduce((sum, slide) => sum + slide.label_scored_edges, 0),
      swimlanes: slideReports.reduce((sum, slide) => sum + slide.swimlanes, 0),
      collapsed_nodes: slideReports.reduce((sum, slide) => sum + slide.collapsed_nodes, 0),
      node_overlaps: slideReports.reduce((sum, slide) => sum + slide.node_overlaps, 0),
      node_crowding_score: Math.round(slideReports.reduce((sum, slide) => sum + slide.node_crowding_score, 0) * 100) / 100,
      min_node_gap: Math.min(...slideReports.map((slide) => slide.min_node_gap).filter((value) => Number.isFinite(value))),
      edge_density_peak: Math.max(0, ...slideReports.map((slide) => slide.edge_density_peak)),
      edge_density_hot_cells: slideReports.reduce((sum, slide) => sum + slide.edge_density_hot_cells, 0),
      errors,
      warnings,
      fail_on: args.failOn,
      require_pptx_native: args.requirePptxNative,
      require_layering: args.requireLayering,
      require_relation_types: args.requireRelationTypes,
      require_active_path: args.requireActivePath,
      require_connector_anchors: args.requireConnectorAnchors,
      require_connector_labels: args.requireConnectorLabels,
      require_edge_bundling: args.requireEdgeBundling,
      require_label_scores: args.requireLabelScores,
      require_swimlanes: args.requireSwimlanes,
      require_subgraph_collapse: args.requireSubgraphCollapse,
      max_edge_crossings: args.maxEdgeCrossings,
      max_label_overlaps: args.maxLabelOverlaps,
      max_node_crowding: args.maxNodeCrowding,
      max_edge_density: args.maxEdgeDensity,
      min_layers: args.minLayers,
      max_edge_styles: args.maxEdgeStyles,
    },
    findings,
    slides: slideReports,
  };
  await fs.mkdir(path.dirname(outPath), { recursive: true });
  await fs.writeFile(outPath, `${JSON.stringify(report, null, 2)}\n`, "utf8");
  await writeMarkdown(markdownPath, report);
  console.log(`relationship-graph-report-written ${outPath}`);
  console.log(`relationship-graph-markdown-written ${markdownPath}`);
  console.log(`relationship-graph-summary slides=${report.summary.slides} graph_slides=${report.summary.graph_slides} errors=${errors} warnings=${warnings}`);
  if (args.failOn === "error" && errors) return 1;
  if (args.failOn === "warning" && (errors || warnings)) return 1;
  return 0;
}

main().then((code) => process.exit(code)).catch((error) => {
  console.error(error);
  process.exit(2);
});
