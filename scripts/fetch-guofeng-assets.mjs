#!/usr/bin/env node

import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const WIKIMEDIA_API = "https://commons.wikimedia.org/w/api.php";
const UA = "itbxm-guofeng-asset-fetcher/1.0 (skill asset workflow)";

const ASSET_TYPES = new Set([
  "place",
  "person",
  "product",
  "brand-logo",
  "ui",
  "food",
  "space",
  "event",
  "artifact",
  "document",
  "evidence",
  "generic",
]);

const PROVIDERS = new Map([
  ["local", { tier: "A", mode: "auto", label: "本地素材" }],
  ["official-web", { tier: "A", mode: "auto", label: "官方网站/低反爬页面" }],
  ["wikimedia", { tier: "A", mode: "auto", label: "Wikimedia Commons" }],
  ["logo", { tier: "A", mode: "auto", label: "SVGL/Simple Icons/Google favicon" }],
  ["svgl", { tier: "A", mode: "auto", label: "SVGL" }],
  ["simple-icons", { tier: "A", mode: "auto", label: "Simple Icons" }],
  ["google-favicon", { tier: "A", mode: "auto", label: "Google favicon" }],
  ["wechat", { tier: "B", mode: "lead", label: "微信公众号" }],
  ["xiaohongshu", { tier: "B", mode: "lead", label: "小红书" }],
  ["dianping", { tier: "B", mode: "lead", label: "点评/美团" }],
  ["meituan", { tier: "B", mode: "lead", label: "点评/美团" }],
  ["ctrip", { tier: "B", mode: "lead", label: "携程/马蜂窝" }],
  ["mafengwo", { tier: "B", mode: "lead", label: "携程/马蜂窝" }],
  ["jd", { tier: "B", mode: "lead", label: "京东官方店" }],
  ["tmall", { tier: "B", mode: "lead", label: "天猫官方店" }],
  ["douyin", { tier: "B", mode: "lead", label: "抖音/快手" }],
  ["kuaishou", { tier: "B", mode: "lead", label: "抖音/快手" }],
  ["baidu-image", { tier: "B", mode: "lead", label: "百度图片" }],
  ["sogou-image", { tier: "B", mode: "lead", label: "搜狗图片" }],
  ["360-image", { tier: "B", mode: "lead", label: "360 图片搜索" }],
  ["login-wall", { tier: "C", mode: "blocked", label: "登录墙" }],
  ["strong-risk-control", { tier: "C", mode: "blocked", label: "强风控平台" }],
  ["signed-token-platform", { tier: "C", mode: "blocked", label: "签名 token 平台" }],
  ["bulk-platform-history", { tier: "C", mode: "blocked", label: "批量历史内容" }],
]);

const IMAGE_EXTENSIONS = new Set([".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg", ".avif"]);

export function parseArgs(argv) {
  const parsed = {
    query: [],
    providers: ["local", "official-web"],
    localDirs: [],
    count: 10,
    pick: 2,
    width: 1600,
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];

    if (arg === "--slot") {
      parsed.slot = argv[++i];
      continue;
    }

    if (arg === "--type") {
      parsed.type = argv[++i];
      continue;
    }

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

    if (arg === "--providers") {
      parsed.providers = argv[++i].split(",").map((value) => value.trim()).filter(Boolean);
      continue;
    }

    if (arg === "--count") {
      parsed.count = Number.parseInt(argv[++i], 10);
      continue;
    }

    if (arg === "--pick") {
      parsed.pick = Number.parseInt(argv[++i], 10);
      continue;
    }

    if (arg === "--width") {
      parsed.width = Number.parseInt(argv[++i], 10);
      continue;
    }

    if (arg === "--source-url") {
      parsed.sourceUrl = argv[++i];
      continue;
    }

    if (arg === "--local-dir") {
      parsed.localDirs.push(argv[++i]);
      continue;
    }

    if (arg === "--manifest") {
      parsed.manifest = argv[++i];
      continue;
    }

    if (arg === "--candidates") {
      parsed.candidates = argv[++i];
      continue;
    }

    if (arg === "--domain") {
      parsed.domain = argv[++i];
      continue;
    }

    if (arg === "--help" || arg === "-h") {
      parsed.help = true;
      continue;
    }

    throw new Error(`Unknown argument: ${arg}`);
  }

  if (!parsed.help) {
    if (!parsed.slot) throw new Error("Missing --slot");
    if (!parsed.type) throw new Error("Missing --type");
    if (!ASSET_TYPES.has(parsed.type)) throw new Error(`--type must be one of: ${[...ASSET_TYPES].join(", ")}`);
    if (parsed.query.length === 0) throw new Error("Missing --query");
    if (!parsed.out) throw new Error("Missing --out");
    if (!Number.isInteger(parsed.count) || parsed.count < 1) throw new Error("--count must be a positive integer");
    if (!Number.isInteger(parsed.pick) || parsed.pick < 1) throw new Error("--pick must be a positive integer");
    if (!Number.isInteger(parsed.width) || parsed.width < 200) throw new Error("--width must be an integer >= 200");
  }

  return parsed;
}

export function classifyProvider(provider) {
  return PROVIDERS.get(provider) || { tier: "C", mode: "blocked", label: provider };
}

export function safeFileName(value) {
  return String(value)
    .normalize("NFKC")
    .replace(/[^\p{L}\p{N}]+/gu, "_")
    .replace(/^_+|_+$/g, "")
    .slice(0, 96) || "asset";
}

export function buildAssetManifestEntry({ slot, type, required, queries, providers, status, score, finalFile, sourceUrl }) {
  return `| ${slot} | ${type} | ${required || "必需"} | ${queries.join(" / ")} | ${providers.join(",")} | ${status} | ${score ?? "-"} | ${finalFile || "-"} | ${sourceUrl || "-"} |\n`;
}

export function buildAssetLeadEntry({ slot, provider, query, action }) {
  return `| ${slot} | ${provider} | ${query} | ${action} |\n`;
}

function stripHtml(value) {
  return String(value || "?")
    .replace(/<[^>]+>/g, "")
    .replace(/\s+/g, " ")
    .trim() || "?";
}

function isIgnorableUrl(url) {
  return !url || url.startsWith("#") || url.startsWith("data:") || url.startsWith("mailto:") || url.startsWith("tel:");
}

function toAbsoluteUrl(value, baseUrl) {
  const trimmed = String(value || "").trim().replace(/^["']|["']$/g, "");
  if (isIgnorableUrl(trimmed)) return "";
  try {
    return new URL(trimmed, baseUrl).href;
  } catch {
    return "";
  }
}

function isImageUrl(url) {
  try {
    const ext = path.extname(new URL(url).pathname).toLowerCase();
    return IMAGE_EXTENSIONS.has(ext);
  } catch {
    return false;
  }
}

function imageExtension(value) {
  try {
    const pathname = value.startsWith("http") ? new URL(value).pathname : value;
    const ext = path.extname(pathname).toLowerCase();
    if (IMAGE_EXTENSIONS.has(ext)) return ext;
  } catch {
    // Fall through.
  }
  return ".jpg";
}

function pushUrl(urls, value, baseUrl) {
  const url = toAbsoluteUrl(value, baseUrl);
  if (url && isImageUrl(url)) urls.add(url);
}

function extractJsonLdImages(node, urls, baseUrl) {
  if (!node) return;
  if (typeof node === "string") {
    pushUrl(urls, node, baseUrl);
    return;
  }
  if (Array.isArray(node)) {
    for (const item of node) extractJsonLdImages(item, urls, baseUrl);
    return;
  }
  if (typeof node === "object") {
    if (node.url) pushUrl(urls, node.url, baseUrl);
    if (node.contentUrl) pushUrl(urls, node.contentUrl, baseUrl);
    if (node.image) extractJsonLdImages(node.image, urls, baseUrl);
    if (node.thumbnailUrl) extractJsonLdImages(node.thumbnailUrl, urls, baseUrl);
  }
}

export function extractImageUrlsFromHtml(html, baseUrl) {
  const urls = new Set();

  for (const match of html.matchAll(/<meta\b[^>]*(?:property|name)=["'](?:og:image|twitter:image)["'][^>]*content=["']([^"']+)["'][^>]*>/gi)) {
    pushUrl(urls, match[1], baseUrl);
  }

  for (const match of html.matchAll(/<meta\b[^>]*content=["']([^"']+)["'][^>]*(?:property|name)=["'](?:og:image|twitter:image)["'][^>]*>/gi)) {
    pushUrl(urls, match[1], baseUrl);
  }

  for (const match of html.matchAll(/<img\b[^>]*\bsrc=["']([^"']+)["'][^>]*>/gi)) {
    pushUrl(urls, match[1], baseUrl);
  }

  for (const match of html.matchAll(/\bsrcset=["']([^"']+)["']/gi)) {
    for (const part of match[1].split(",")) {
      pushUrl(urls, part.trim().split(/\s+/)[0], baseUrl);
    }
  }

  for (const match of html.matchAll(/url\(\s*["']?([^"')]+)["']?\s*\)/gi)) {
    pushUrl(urls, match[1], baseUrl);
  }

  for (const match of html.matchAll(/<script\b[^>]*type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi)) {
    try {
      extractJsonLdImages(JSON.parse(match[1]), urls, baseUrl);
    } catch {
      // Invalid JSON-LD should not abort image discovery.
    }
  }

  return [...urls];
}

function isImageFile(filePath) {
  return IMAGE_EXTENSIONS.has(path.extname(filePath).toLowerCase());
}

async function walkImages(dir, options = {}, depth = 0, results = []) {
  const maxDepth = options.maxDepth ?? 4;
  const maxFiles = options.maxFiles ?? 250;
  if (depth > maxDepth || results.length >= maxFiles || !fs.existsSync(dir)) return results;

  let entries = [];
  try {
    entries = await fs.promises.readdir(dir, { withFileTypes: true });
  } catch {
    return results;
  }

  for (const entry of entries) {
    if (results.length >= maxFiles) break;
    if (entry.name.startsWith(".")) continue;
    const entryPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      await walkImages(entryPath, options, depth + 1, results);
    } else if (entry.isFile() && isImageFile(entryPath)) {
      results.push(entryPath);
    }
  }

  return results;
}

export async function collectLocalCandidates({ slot, type, queries, localDirs }) {
  const candidates = [];
  for (const dir of localDirs) {
    const files = await walkImages(path.resolve(dir));
    for (const file of files) {
      candidates.push(makeCandidate({
        slot,
        type,
        query: queries.join(" / "),
        provider: "local",
        sourceUrl: file,
        sourcePage: file,
        license: "local/user-provided",
        author: "local",
      }));
    }
  }
  return candidates;
}

export async function collectOfficialWebCandidates({ slot, type, queries, sourceUrl, fetchImpl = fetch }) {
  if (!sourceUrl) return [];
  const response = await fetchImpl(sourceUrl, { headers: { "User-Agent": UA, Accept: "text/html" } });
  if (!response.ok) throw new Error(`official-web returned ${response.status} ${response.statusText}`);
  const html = await response.text();
  return extractImageUrlsFromHtml(html, sourceUrl).map((url) => makeCandidate({
    slot,
    type,
    query: queries.join(" / "),
    provider: "official-web",
    sourceUrl: url,
    sourcePage: sourceUrl,
    license: "official/source-page",
    author: new URL(sourceUrl).hostname,
  }));
}

function simpleIconSlug(value) {
  return String(value || "")
    .toLowerCase()
    .normalize("NFKD")
    .replace(/[^\w\s-]/g, "")
    .trim()
    .replace(/\s+/g, "-");
}

function addSvgRoute(candidates, route, base) {
  if (typeof route === "string") {
    candidates.push(makeCandidate({ ...base, provider: "svgl", sourceUrl: route, sourcePage: "https://svgl.app", license: "svgl", author: "SVGL" }));
    return;
  }
  if (route && typeof route === "object") {
    for (const value of Object.values(route)) {
      if (typeof value === "string") addSvgRoute(candidates, value, base);
    }
  }
}

export async function collectLogoCandidates({ slot, type, queries, domain, fetchImpl = fetch }) {
  const query = queries[0];
  const candidates = [];

  try {
    const response = await fetchImpl(`https://api.svgl.app?search=${encodeURIComponent(query)}`, {
      headers: { "User-Agent": UA, Accept: "application/json" },
    });
    if (response.ok) {
      const data = await response.json();
      const records = Array.isArray(data) ? data : data.data || [];
      for (const record of records.slice(0, 4)) {
        addSvgRoute(candidates, record.route || record.logo || record.url, { slot, type, query });
      }
    }
  } catch {
    // Fallback providers below still produce useful logo leads.
  }

  const slug = simpleIconSlug(query);
  if (slug) {
    candidates.push(makeCandidate({
      slot,
      type,
      query,
      provider: "simple-icons",
      sourceUrl: `https://cdn.simpleicons.org/${slug}/111111`,
      sourcePage: "https://simpleicons.org",
      license: "simple-icons",
      author: "Simple Icons",
    }));
  }

  if (domain) {
    candidates.push(makeCandidate({
      slot,
      type,
      query,
      provider: "google-favicon",
      sourceUrl: `https://www.google.com/s2/favicons?domain=${encodeURIComponent(domain)}&sz=256`,
      sourcePage: `https://${domain}`,
      license: "site favicon",
      author: domain,
    }));
  }

  return candidates;
}

export async function collectWikimediaCandidates({ slot, type, queries, count, width, fetchImpl = fetch }) {
  const candidates = [];
  for (const query of queries) {
    const url = `${WIKIMEDIA_API}?${new URLSearchParams({
      action: "query",
      format: "json",
      generator: "search",
      gsrsearch: query,
      gsrnamespace: "6",
      gsrlimit: String(count),
      prop: "imageinfo",
      iiprop: "url|extmetadata",
      iiurlwidth: String(width),
    }).toString()}`;
    const response = await fetchImpl(url, { headers: { "User-Agent": UA, Accept: "application/json" } });
    if (!response.ok) throw new Error(`wikimedia returned ${response.status} ${response.statusText}`);
    const data = await response.json();
    for (const page of Object.values(data.query?.pages || {}).slice(0, count)) {
      const imageInfo = page.imageinfo?.[0];
      const sourceUrl = imageInfo?.thumburl || imageInfo?.url;
      if (!sourceUrl) continue;
      const meta = imageInfo.extmetadata || {};
      candidates.push(makeCandidate({
        slot,
        type,
        query,
        provider: "wikimedia",
        sourceUrl,
        sourcePage: imageInfo.descriptionurl || "",
        license: stripHtml(meta.LicenseShortName?.value),
        author: stripHtml(meta.Artist?.value),
      }));
    }
  }
  return candidates;
}

function makeCandidate(candidate) {
  const providerInfo = classifyProvider(candidate.provider);
  const score = candidate.score ?? scoreCandidate({ ...candidate, providerTier: providerInfo.tier });
  return {
    slot: candidate.slot,
    type: candidate.type,
    query: candidate.query,
    provider: candidate.provider,
    providerTier: providerInfo.tier,
    mode: providerInfo.mode,
    sourceUrl: candidate.sourceUrl,
    sourcePage: candidate.sourcePage || candidate.sourceUrl,
    license: candidate.license || "?",
    author: candidate.author || "?",
    score,
    selected: false,
  };
}

function scoreCandidate(candidate) {
  let score = 5;
  if (candidate.provider === "local") score += 4;
  if (candidate.provider === "official-web") score += 3;
  if (candidate.provider === "wikimedia") score += 3;
  if (["svgl", "simple-icons", "google-favicon"].includes(candidate.provider)) score += 3;
  if (candidate.sourcePage && candidate.sourcePage !== candidate.sourceUrl) score += 1;
  if (candidate.license && candidate.license !== "?") score += 1;
  return Math.min(score, 10);
}

function sourcePathsForOut(outDir, parsed) {
  const out = path.resolve(outDir);
  const parent = path.dirname(out);
  const sourcesDir = path.basename(parent) === "assets"
    ? path.join(parent, "sources")
    : path.join(path.dirname(out), "sources");
  return {
    manifest: path.resolve(parsed.manifest || path.join(sourcesDir, "asset-manifest.md")),
    candidates: path.resolve(parsed.candidates || path.join(sourcesDir, "asset-candidates.json")),
    leads: path.join(sourcesDir, "asset-leads.md"),
    imageSources: path.join(sourcesDir, "image-sources.md"),
  };
}

function siteRootForOut(outDir) {
  const out = path.resolve(outDir);
  const parent = path.dirname(out);
  if (path.basename(parent) === "assets") return path.dirname(parent);
  return process.cwd();
}

function defaultLocalDirs() {
  const dirs = [process.cwd()];
  const downloads = path.join(os.homedir(), "Downloads");
  if (fs.existsSync(downloads)) dirs.push(downloads);
  return dirs;
}

async function downloadCandidate(candidate, outDir, siteRoot, fetchImpl = fetch) {
  const ext = imageExtension(candidate.sourceUrl);
  const fileName = `${safeFileName(`${candidate.slot}_${candidate.provider}_${path.basename(candidate.sourceUrl)}`)}${ext}`;
  const filePath = path.join(outDir, fileName);

  if (candidate.provider === "local") {
    await fs.promises.copyFile(candidate.sourceUrl, filePath);
  } else {
    const response = await fetchImpl(candidate.sourceUrl, { headers: { "User-Agent": UA } });
    if (!response.ok) throw new Error(`download returned ${response.status} ${response.statusText}`);
    await fs.promises.writeFile(filePath, Buffer.from(await response.arrayBuffer()));
  }

  return path.relative(siteRoot, filePath).replaceAll(path.sep, "/");
}

async function appendMarkdownTable(filePath, header, entry) {
  await fs.promises.mkdir(path.dirname(filePath), { recursive: true });
  let content = "";
  if (!fs.existsSync(filePath)) content += header;
  content += entry;
  await fs.promises.appendFile(filePath, content);
}

async function appendCandidates(filePath, records) {
  await fs.promises.mkdir(path.dirname(filePath), { recursive: true });
  let existing = [];
  if (fs.existsSync(filePath)) {
    try {
      existing = JSON.parse(await fs.promises.readFile(filePath, "utf8"));
    } catch {
      existing = [];
    }
  }
  await fs.promises.writeFile(filePath, `${JSON.stringify([...existing, ...records], null, 2)}\n`);
}

function imageSourceEntry(record, retrievedAt) {
  return `| ${record.finalFile} | ${record.query} | ${record.sourcePage || record.sourceUrl} | ${record.license || "?"} | ${record.author || "?"} | ${retrievedAt} |\n`;
}

async function writeImageSources(filePath, records, retrievedAt) {
  if (!records.length) return;
  const header = "# Image Sources\n\n| Local file | Query | Source URL | License | Author | Retrieved at |\n| --- | --- | --- | --- | --- | --- |\n";
  await appendMarkdownTable(filePath, header, records.map((record) => imageSourceEntry(record, retrievedAt)).join(""));
}

async function collectProviderCandidates(provider, parsed) {
  if (provider === "local") {
    return collectLocalCandidates({
      slot: parsed.slot,
      type: parsed.type,
      queries: parsed.query,
      localDirs: parsed.localDirs.length ? parsed.localDirs : defaultLocalDirs(),
    });
  }
  if (provider === "official-web") {
    return collectOfficialWebCandidates({
      slot: parsed.slot,
      type: parsed.type,
      queries: parsed.query,
      sourceUrl: parsed.sourceUrl,
    });
  }
  if (provider === "wikimedia") {
    return collectWikimediaCandidates({
      slot: parsed.slot,
      type: parsed.type,
      queries: parsed.query,
      count: parsed.count,
      width: parsed.width,
    });
  }
  if (provider === "logo" || provider === "svgl" || provider === "simple-icons" || provider === "google-favicon") {
    return collectLogoCandidates({
      slot: parsed.slot,
      type: parsed.type,
      queries: parsed.query,
      domain: parsed.domain,
    });
  }
  return [];
}

export async function run(argv = process.argv.slice(2)) {
  const parsed = parseArgs(argv);

  if (parsed.help) {
    console.log("[deprecated] Use the Python-first entry instead:");
    console.log("Usage: python3 scripts/fetch-guofeng-assets.py --slot \"Hero 西湖主视觉\" --type place --query \"西湖 杭州 全景\" \"West Lake Hangzhou panorama\" --out site/assets/images --source-profile domestic --count 10 --pick 2");
    console.log("Legacy compatibility: node scripts/fetch-guofeng-assets.mjs ...");
    return 0;
  }

  const out = path.resolve(parsed.out);
  const siteRoot = siteRootForOut(out);
  const paths = sourcePathsForOut(out, parsed);
  const retrievedAt = new Date().toISOString().slice(0, 10);
  const leads = [];
  const candidates = [];

  await fs.promises.mkdir(out, { recursive: true });

  for (const provider of parsed.providers) {
    const providerInfo = classifyProvider(provider);
    if (providerInfo.mode === "lead") {
      for (const query of parsed.query) {
        leads.push({ slot: parsed.slot, provider, query, action: "浏览器打开后保存可见素材或截图；不要写绕风控脚本" });
      }
      continue;
    }
    if (providerInfo.mode === "blocked") {
      for (const query of parsed.query) {
        leads.push({ slot: parsed.slot, provider, query, action: "C 级强反爬来源，不自动抓取；改用用户提供素材或官方来源" });
      }
      continue;
    }

    try {
      const providerCandidates = await collectProviderCandidates(provider, parsed);
      candidates.push(...providerCandidates.slice(0, parsed.count));
    } catch (error) {
      console.error(`[FAIL ${provider}] ${error.message}`);
    }
  }

  const selected = candidates
    .sort((a, b) => b.score - a.score)
    .slice(0, parsed.pick);
  const finalRecords = [];

  for (const candidate of selected) {
    try {
      const finalFile = await downloadCandidate(candidate, out, siteRoot);
      candidate.selected = true;
      candidate.finalFile = finalFile;
      finalRecords.push({ ...candidate, finalFile });
      console.log(`[OK] ${finalFile} | ${candidate.provider} | score ${candidate.score} | ${candidate.sourcePage}`);
    } catch (error) {
      console.error(`[FAIL download] ${candidate.sourceUrl}: ${error.message}`);
    }
  }

  if (candidates.length) {
    await appendCandidates(paths.candidates, candidates);
  }

  if (leads.length) {
    const header = "# Asset Leads\n\n| Slot | Provider | Query | Action |\n| --- | --- | --- | --- |\n";
    await appendMarkdownTable(paths.leads, header, leads.map(buildAssetLeadEntry).join(""));
    console.log(`Lead log: ${path.relative(process.cwd(), paths.leads).replaceAll(path.sep, "/")}`);
  }

  const best = finalRecords[0];
  const status = best ? (best.score >= 8 ? "已验证" : "待用户确认") : "占位待补";
  const manifestEntry = buildAssetManifestEntry({
    slot: parsed.slot,
    type: parsed.type,
    required: "必需",
    queries: parsed.query,
    providers: parsed.providers,
    status,
    score: best?.score ?? 0,
    finalFile: best?.finalFile || "-",
    sourceUrl: best?.sourcePage || best?.sourceUrl || "-",
  });
  const manifestHeader = "# Asset Manifest\n\n| Slot | Type | Required | Queries | Providers | Status | Score | Final file | Source URL |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n";
  await appendMarkdownTable(paths.manifest, manifestHeader, manifestEntry);
  await writeImageSources(paths.imageSources, finalRecords, retrievedAt);

  if (!finalRecords.length) {
    console.error("No final assets downloaded. Use asset-leads.md, browser-assisted collection, or an honest placeholder marked 占位待补.");
    return 1;
  }

  console.log(`Manifest: ${path.relative(process.cwd(), paths.manifest).replaceAll(path.sep, "/")}`);
  console.log(`Candidates: ${path.relative(process.cwd(), paths.candidates).replaceAll(path.sep, "/")}`);
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
