#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const API = "https://commons.wikimedia.org/w/api.php";
const UA = "itbxm-guofeng-image-fetcher/1.0 (skill asset workflow)";

export function parseArgs(argv) {
  const parsed = {
    query: [],
    count: 2,
    width: 1600,
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];

    if (arg === "--query") {
      i += 1;
      while (i < argv.length && !argv[i].startsWith("--")) {
        parsed.query.push(argv[i]);
        i += 1;
      }
      i -= 1;
      continue;
    }

    if (arg === "--out") {
      parsed.out = argv[++i];
      continue;
    }

    if (arg === "--count") {
      parsed.count = Number.parseInt(argv[++i], 10);
      continue;
    }

    if (arg === "--width") {
      parsed.width = Number.parseInt(argv[++i], 10);
      continue;
    }

    if (arg === "--help" || arg === "-h") {
      parsed.help = true;
      continue;
    }

    throw new Error(`Unknown argument: ${arg}`);
  }

  if (!parsed.help) {
    if (parsed.query.length === 0) throw new Error("Missing --query");
    if (!parsed.out) throw new Error("Missing --out");
    if (!Number.isInteger(parsed.count) || parsed.count < 1) throw new Error("--count must be a positive integer");
    if (!Number.isInteger(parsed.width) || parsed.width < 200) throw new Error("--width must be an integer >= 200");
  }

  return parsed;
}

export function safeFileName(value) {
  return String(value)
    .normalize("NFKC")
    .replace(/[^\p{L}\p{N}]+/gu, "_")
    .replace(/^_+|_+$/g, "")
    .slice(0, 80) || "image";
}

export function buildSourceEntry({ localFile, query, sourceUrl, license, artist, retrievedAt }) {
  return `| ${localFile} | ${query} | ${sourceUrl} | ${license || "?"} | ${artist || "?"} | ${retrievedAt} |\n`;
}

function stripHtml(value) {
  return String(value || "?")
    .replace(/<[^>]+>/g, "")
    .replace(/\s+/g, " ")
    .trim() || "?";
}

function imageExtension(url) {
  try {
    const pathname = new URL(url).pathname;
    const ext = path.extname(pathname).toLowerCase();
    if (/^\.(?:jpg|jpeg|png|webp|gif|svg)$/.test(ext)) return ext;
  } catch {
    // Fall through to default.
  }
  return ".jpg";
}

function sourcesPathForOut(outDir) {
  const absoluteOut = path.resolve(outDir);
  const parent = path.dirname(absoluteOut);
  const sourcesDir = path.basename(parent) === "assets"
    ? path.join(parent, "sources")
    : path.join(path.dirname(absoluteOut), "sources");
  return path.join(sourcesDir, "image-sources.md");
}

function siteRootForOut(outDir) {
  const absoluteOut = path.resolve(outDir);
  const parent = path.dirname(absoluteOut);
  if (path.basename(parent) === "assets") return path.dirname(parent);
  return process.cwd();
}

async function apiGet(params) {
  const url = `${API}?${new URLSearchParams(params).toString()}`;
  const response = await fetch(url, {
    headers: {
      "User-Agent": UA,
      Accept: "application/json",
    },
  });

  if (!response.ok) {
    throw new Error(`Wikimedia API returned ${response.status} ${response.statusText}`);
  }

  return response.json();
}

async function downloadFile(url, filePath) {
  const response = await fetch(url, {
    headers: {
      "User-Agent": UA,
    },
  });

  if (!response.ok) {
    throw new Error(`download returned ${response.status} ${response.statusText}`);
  }

  const buffer = Buffer.from(await response.arrayBuffer());
  await fs.promises.writeFile(filePath, buffer);
}

async function fetchQuery(query, options) {
  const data = await apiGet({
    action: "query",
    format: "json",
    generator: "search",
    gsrsearch: query,
    gsrnamespace: "6",
    gsrlimit: String(options.count),
    prop: "imageinfo",
    iiprop: "url|extmetadata",
    iiurlwidth: String(options.width),
  });

  const pages = Object.values(data.query?.pages || {});
  const records = [];

  for (const page of pages.slice(0, options.count)) {
    const imageInfo = page.imageinfo?.[0];
    const imageUrl = imageInfo?.thumburl || imageInfo?.url;
    if (!imageUrl) continue;

    const meta = imageInfo.extmetadata || {};
    const license = stripHtml(meta.LicenseShortName?.value);
    const artist = stripHtml(meta.Artist?.value);
    const sourceUrl = imageInfo.descriptionurl || "";
    const title = String(page.title || "image").replace(/^File:/, "");
    const ext = imageExtension(imageUrl);
    const fileName = `${safeFileName(`${query}_${title}`)}${ext}`;
    const filePath = path.join(options.out, fileName);

    await downloadFile(imageUrl, filePath);

    records.push({
      localFile: path.relative(options.siteRoot, filePath).replaceAll(path.sep, "/"),
      query,
      sourceUrl,
      license,
      artist,
    });
  }

  return records;
}

async function appendSources(sourceFile, records, retrievedAt) {
  await fs.promises.mkdir(path.dirname(sourceFile), { recursive: true });

  let content = "";
  if (!fs.existsSync(sourceFile)) {
    content += "# Image Sources\n\n";
    content += "| Local file | Query | Source URL | License | Author | Retrieved at |\n";
    content += "| --- | --- | --- | --- | --- | --- |\n";
  }

  for (const record of records) {
    content += buildSourceEntry({ ...record, retrievedAt });
  }

  await fs.promises.appendFile(sourceFile, content);
}

export async function run(argv = process.argv.slice(2)) {
  const parsed = parseArgs(argv);

  if (parsed.help) {
    console.log("[deprecated] Use the Python-first entry instead:");
    console.log("Usage: python3 scripts/fetch-guofeng-images.py --query \"West Lake Hangzhou\" \"Lingyin Temple Hangzhou\" --out site/assets/images --count 2 --width 1600");
    console.log("Legacy compatibility: node scripts/fetch-guofeng-images.mjs ...");
    return 0;
  }

  const out = path.resolve(parsed.out);
  const options = {
    ...parsed,
    out,
    siteRoot: siteRootForOut(out),
  };
  const sourceFile = sourcesPathForOut(out);
  const retrievedAt = new Date().toISOString().slice(0, 10);

  await fs.promises.mkdir(out, { recursive: true });

  const allRecords = [];
  for (const query of parsed.query) {
    try {
      const records = await fetchQuery(query, options);
      if (records.length === 0) {
        console.error(`[EMPTY] ${query}: Wikimedia Commons returned no downloadable images.`);
      } else {
        allRecords.push(...records);
        for (const record of records) {
          console.log(`[OK] ${record.localFile} | ${record.license} | ${record.artist} | ${record.sourceUrl}`);
        }
      }
    } catch (error) {
      console.error(`[FAIL] ${query}: ${error.message}`);
    }
  }

  if (allRecords.length === 0) {
    console.error("No images downloaded. Use browser/WebSearch, Unsplash/Pexels/manual sources, or honest placeholders with a material list.");
    return 1;
  }

  await appendSources(sourceFile, allRecords, retrievedAt);
  console.log(`\nDownloaded ${allRecords.length} image(s) to ${out}`);
  console.log(`Source log: ${path.relative(process.cwd(), sourceFile).replaceAll(path.sep, "/")}`);
  console.log("Review each image for 8/10 fit before using it in final HTML.");
  return 0;
}

const isCli = process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1]);
if (isCli) {
  run().then((code) => {
    process.exitCode = code;
  }).catch((error) => {
    console.error(error.message);
    process.exitCode = 2;
  });
}
