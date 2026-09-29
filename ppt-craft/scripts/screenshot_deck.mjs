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
  console.error("Usage: node screenshot_deck.mjs <deck-dir> [--out qa]");
  process.exit(1);
}

const root = path.resolve(deckDir);
const outDir = path.resolve(argValue("--out", path.join(root, "qa-screenshots")));
await fs.mkdir(outDir, { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });

async function shot(file, name) {
  await page.goto(pathToFileURL(file).href, { waitUntil: "networkidle" });
  await page.waitForTimeout(800);
  const bodyBox = await page.evaluate(() => {
    const target = document.querySelector(".slide") || document.body;
    const rect = target.getBoundingClientRect();
    return {
      x: Math.floor(rect.left),
      y: Math.floor(rect.top),
      width: Math.ceil(rect.width),
      height: Math.ceil(rect.height),
    };
  });
  const clip = bodyBox.width > 0 && bodyBox.height > 0
    ? { x: bodyBox.x, y: bodyBox.y, width: bodyBox.width, height: bodyBox.height }
    : undefined;
  await page.screenshot({ path: path.join(outDir, `${name}.png`), fullPage: false, clip });
  console.log(`screenshot ${name}.png`);
}

const indexPath = path.join(root, "index.html");
try {
  await fs.access(indexPath);
  await shot(indexPath, "index");
} catch {}

const slidesDir = path.join(root, "slides");
try {
  const slideFiles = (await fs.readdir(slidesDir))
    .filter(file => file.endsWith(".html"))
    .sort();
  for (const file of slideFiles) {
    await shot(path.join(slidesDir, file), file.replace(/\.html$/i, ""));
  }
} catch {}

await browser.close();
