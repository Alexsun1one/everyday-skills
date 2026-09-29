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

function argValue(name, fallback) {
  const index = process.argv.indexOf(name);
  return index >= 0 && process.argv[index + 1] ? process.argv[index + 1] : fallback;
}

const deckDir = process.argv[2];
if (!deckDir || deckDir.startsWith("--")) {
  console.error("Usage: node visual_dom_metrics.mjs <deck-dir> [--out qa/visual-dom-report.json]");
  process.exit(1);
}

const root = path.resolve(deckDir);
const outPath = path.resolve(argValue("--out", path.join(root, "qa", "visual-dom-report.json")));

function parseColor(value) {
  if (!value || value === "transparent") return null;
  const hex = String(value).trim().match(/^#([0-9a-f]{3}|[0-9a-f]{6})$/i);
  if (hex) {
    let raw = hex[1];
    if (raw.length === 3) raw = raw.split("").map(ch => ch + ch).join("");
    return {
      r: Number.parseInt(raw.slice(0, 2), 16),
      g: Number.parseInt(raw.slice(2, 4), 16),
      b: Number.parseInt(raw.slice(4, 6), 16),
      a: 1,
    };
  }
  const match = String(value).match(/rgba?\(([^)]+)\)/i);
  if (match) {
    const parts = match[1].split(",").map(part => part.trim());
    if (parts.length < 3) return null;
    const rgb = parts.slice(0, 3).map(part => Number.parseFloat(part));
    const alpha = parts[3] === undefined ? 1 : Number.parseFloat(parts[3]);
    if (rgb.some(value => Number.isNaN(value)) || Number.isNaN(alpha)) return null;
    return { r: rgb[0], g: rgb[1], b: rgb[2], a: alpha };
  }
  const srgb = String(value).match(/color\(\s*srgb\s+([^)]+)\)/i);
  if (srgb) {
    const normalized = srgb[1].replace("/", " ");
    const parts = normalized.split(/\s+/).filter(Boolean).map(part => Number.parseFloat(part));
    if (parts.length < 3 || parts.slice(0, 3).some(value => Number.isNaN(value))) return null;
    return {
      r: Math.round(Math.max(0, Math.min(1, parts[0])) * 255),
      g: Math.round(Math.max(0, Math.min(1, parts[1])) * 255),
      b: Math.round(Math.max(0, Math.min(1, parts[2])) * 255),
      a: Number.isNaN(parts[3]) ? 1 : parts[3],
    };
  }
  return null;
}

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });

async function collectSlide(file, name) {
  await page.goto(pathToFileURL(file).href, { waitUntil: "networkidle" });
  await page.waitForTimeout(500);
  return page.evaluate(({ fileName }) => {
    function parseComputedColor(value) {
      if (!value || value === "transparent") return null;
      const hex = String(value).trim().match(/^#([0-9a-f]{3}|[0-9a-f]{6})$/i);
      if (hex) {
        let raw = hex[1];
        if (raw.length === 3) raw = raw.split("").map(ch => ch + ch).join("");
        return {
          r: Number.parseInt(raw.slice(0, 2), 16),
          g: Number.parseInt(raw.slice(2, 4), 16),
          b: Number.parseInt(raw.slice(4, 6), 16),
          a: 1,
        };
      }
      const match = String(value).match(/rgba?\(([^)]+)\)/i);
      if (match) {
        const parts = match[1].split(",").map(part => part.trim());
        const rgb = parts.slice(0, 3).map(part => Number.parseFloat(part));
        const alpha = parts[3] === undefined ? 1 : Number.parseFloat(parts[3]);
        if (rgb.some(value => Number.isNaN(value)) || Number.isNaN(alpha)) return null;
        return { r: rgb[0], g: rgb[1], b: rgb[2], a: alpha };
      }
      const srgb = String(value).match(/color\(\s*srgb\s+([^)]+)\)/i);
      if (srgb) {
        const normalized = srgb[1].replace("/", " ");
        const parts = normalized.split(/\s+/).filter(Boolean).map(part => Number.parseFloat(part));
        if (parts.length < 3 || parts.slice(0, 3).some(value => Number.isNaN(value))) return null;
        return {
          r: Math.round(Math.max(0, Math.min(1, parts[0])) * 255),
          g: Math.round(Math.max(0, Math.min(1, parts[1])) * 255),
          b: Math.round(Math.max(0, Math.min(1, parts[2])) * 255),
          a: Number.isNaN(parts[3]) ? 1 : parts[3],
        };
      }
      return null;
    }

    function luminance(color) {
      function channel(value) {
        const v = value / 255;
        return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
      }
      return 0.2126 * channel(color.r) + 0.7152 * channel(color.g) + 0.0722 * channel(color.b);
    }

    function contrastRatio(a, b) {
      const left = luminance(a);
      const right = luminance(b);
      return (Math.max(left, right) + 0.05) / (Math.min(left, right) + 0.05);
    }

    function rectObject(rect) {
      return {
        x: Math.round(rect.left * 10) / 10,
        y: Math.round(rect.top * 10) / 10,
        w: Math.round(rect.width * 10) / 10,
        h: Math.round(rect.height * 10) / 10,
      };
    }

    function stageRectObject(rect, stageRect) {
      return {
        x: Math.round((rect.left - stageRect.left) * 10) / 10,
        y: Math.round((rect.top - stageRect.top) * 10) / 10,
        w: Math.round(rect.width * 10) / 10,
        h: Math.round(rect.height * 10) / 10,
      };
    }

    function directText(element) {
      return Array.from(element.childNodes)
        .filter(node => node.nodeType === Node.TEXT_NODE)
        .map(node => node.textContent || "")
        .join(" ")
        .replace(/\s+/g, " ")
        .trim();
    }

    function visible(element, style, rect) {
      if (style.display === "none" || style.visibility === "hidden") return false;
      if (Number.parseFloat(style.opacity || "1") < 0.04) return false;
      return rect.width > 1 && rect.height > 1;
    }

    function nearestBackground(element) {
      let cursor = element;
      while (cursor) {
        const style = getComputedStyle(cursor);
        const color = parseComputedColor(style.backgroundColor);
        if (color && color.a > 0.1) return { color, source: cursor.tagName.toLowerCase() };
        cursor = cursor.parentElement;
      }
      const body = parseComputedColor(getComputedStyle(document.body).backgroundColor);
      return { color: body || { r: 255, g: 255, b: 255, a: 1 }, source: "body-fallback" };
    }

    function clippedInsideStage(element, stageRect) {
      let cursor = element.parentElement;
      while (cursor) {
        const style = getComputedStyle(cursor);
        const clips = [style.overflow, style.overflowX, style.overflowY].some(value => value && value !== "visible");
        if (clips) {
          const rect = cursor.getBoundingClientRect();
          if (
            rect.left >= stageRect.left - 2 &&
            rect.top >= stageRect.top - 2 &&
            rect.right <= stageRect.right + 2 &&
            rect.bottom <= stageRect.bottom + 2
          ) {
            return true;
          }
        }
        cursor = cursor.parentElement;
      }
      return false;
    }

    const stageElement = document.querySelector(".slide") || document.body;
    const stageRect = stageElement.getBoundingClientRect();
    const stage = rectObject(stageRect);
    const warnings = [];
    const overflows = [];
    const clippedText = [];
    const contrast = [];
    const textBoxes = [];

    const body = document.body;
    if (body.scrollWidth > Math.ceil(stageRect.width) + 2 || body.scrollHeight > Math.ceil(stageRect.height) + 2) {
      overflows.push({
        type: "document-scroll-overflow",
        scrollWidth: body.scrollWidth,
        scrollHeight: body.scrollHeight,
        stageWidth: Math.ceil(stageRect.width),
        stageHeight: Math.ceil(stageRect.height),
      });
    }

    const elements = Array.from(document.querySelectorAll("body *"));
    for (const element of elements) {
      if (element.closest("[data-visual-qa-ignore='true']")) continue;
      const style = getComputedStyle(element);
      const rect = element.getBoundingClientRect();
      if (!visible(element, style, rect)) continue;
      const tag = element.tagName.toLowerCase();
      if (["script", "style", "meta", "link"].includes(tag)) continue;
      const className = typeof element.className === "string" ? element.className : "";
      const label = `${tag}${className ? "." + className.trim().replace(/\s+/g, ".") : ""}`;
      const box = rectObject(rect);
      const tolerance = 2;
      if (
        rect.left < stageRect.left - tolerance ||
        rect.top < stageRect.top - tolerance ||
        rect.right > stageRect.right + tolerance ||
        rect.bottom > stageRect.bottom + tolerance
      ) {
        if (!clippedInsideStage(element, stageRect)) {
          overflows.push({ type: "element-outside-stage", element: label, rect: box });
        }
      }

      const text = directText(element);
      if (!text) continue;
      const fontSize = Number.parseFloat(style.fontSize || "0");
      const fontWeight = Number.parseFloat(style.fontWeight || "400");
      textBoxes.push({
        element: label,
        text: text.slice(0, 160),
        rect: stageRectObject(rect, stageRect),
        viewportRect: box,
        fontSize: Math.round(fontSize * 10) / 10,
        fontWeight,
        graphNode: element.closest("[data-graph-node]")?.getAttribute("data-graph-node") || "",
        graphLabel: element.closest("[data-graph-label]")?.getAttribute("data-graph-label") || "",
        visualQaZone: element.closest("[data-visual-qa-zone]")?.getAttribute("data-visual-qa-zone") || "",
      });
      const clipsX = style.overflowX !== "visible";
      const clipsY = style.overflowY !== "visible";
      if ((clipsX && element.scrollWidth > element.clientWidth + 2) || (clipsY && element.scrollHeight > element.clientHeight + 2)) {
        clippedText.push({
          element: label,
          text: text.slice(0, 120),
          rect: box,
          scrollWidth: element.scrollWidth,
          clientWidth: element.clientWidth,
          scrollHeight: element.scrollHeight,
          clientHeight: element.clientHeight,
        });
      }

      const color = parseComputedColor(style.color);
      const background = nearestBackground(element);
      if (!color || !background.color) continue;
      const ratio = contrastRatio(color, background.color);
      const large = fontSize >= 24 || (fontSize >= 18.66 && fontWeight >= 700);
      const required = large ? 3.0 : 4.5;
      if (ratio < required) {
        contrast.push({
          element: label,
          text: text.slice(0, 120),
          rect: box,
          ratio: Math.round(ratio * 100) / 100,
          required,
          fontSize: Math.round(fontSize * 10) / 10,
          fontWeight,
          backgroundSource: background.source,
        });
      }
    }

    if (stage.w <= 0 || stage.h <= 0) {
      warnings.push({ type: "empty-stage", message: "Could not detect a positive .slide/body stage." });
    }

    return {
      file: fileName,
      stage,
      overflows,
      clipped_text: clippedText,
      low_contrast_text: contrast,
      text_boxes: textBoxes,
      warnings,
    };
  }, { fileName: name });
}

const slidesDir = path.join(root, "slides");
let slideFiles = [];
try {
  slideFiles = (await fs.readdir(slidesDir))
    .filter(file => file.endsWith(".html"))
    .sort()
    .map(file => ({ file: path.join(slidesDir, file), name: file.replace(/\.html$/i, "") }));
} catch {}

if (slideFiles.length === 0) {
  console.error(`No slides/*.html found under ${root}`);
  await browser.close();
  process.exit(1);
}

const slides = [];
for (const slide of slideFiles) {
  slides.push(await collectSlide(slide.file, slide.name));
}

await browser.close();

const summary = {
  slides: slides.length,
  overflows: slides.reduce((sum, slide) => sum + slide.overflows.length, 0),
  clipped_text: slides.reduce((sum, slide) => sum + slide.clipped_text.length, 0),
  low_contrast_text: slides.reduce((sum, slide) => sum + slide.low_contrast_text.length, 0),
  text_boxes: slides.reduce((sum, slide) => sum + slide.text_boxes.length, 0),
};

const report = {
  generated_by: "ppt-craft/scripts/visual_dom_metrics.mjs",
  deck: root,
  summary,
  slides,
};

await fs.mkdir(path.dirname(outPath), { recursive: true });
await fs.writeFile(outPath, JSON.stringify(report, null, 2) + "\n", "utf8");
console.log(`visual-dom-report-written ${outPath}`);
console.log(`visual-dom-summary slides=${summary.slides} overflows=${summary.overflows} clipped_text=${summary.clipped_text} low_contrast_text=${summary.low_contrast_text}`);
