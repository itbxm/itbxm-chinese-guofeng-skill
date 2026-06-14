#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptPath = fileURLToPath(import.meta.url);
const repoRoot = path.resolve(path.dirname(scriptPath), "..");
const args = process.argv.slice(2);

if (args[0] === "--help" || args[0] === "-h") {
  console.log("[deprecated] Use the Python-first entry instead:");
  console.log("Usage: python3 scripts/validate-guofeng-html.py <file.html> [...]");
  console.log("Legacy compatibility: node scripts/validate-guofeng-html.mjs <file.html> [...]");
  process.exit(0);
}

if (args.length === 0) {
  console.error("[deprecated] Use the Python-first entry instead:");
  console.error("Usage: python3 scripts/validate-guofeng-html.py <file.html> [...]");
  console.error("Legacy compatibility: node scripts/validate-guofeng-html.mjs <file.html> [...]");
  process.exit(2);
}

const patternsPath = path.join(repoRoot, "data", "patterns.json");
const patterns = JSON.parse(fs.readFileSync(patternsPath, "utf8"));
const knownPatternPaths = new Set();

for (const pattern of patterns) {
  for (const value of Object.values(pattern.assets || {})) {
    if (typeof value === "string") {
      knownPatternPaths.add(value);
      knownPatternPaths.add(value.replace(/^assets\//, ""));
    }
  }
}

const urlPattern = /url\((["']?)([^"')]+)\1\)|(?:src|href)=["']([^"']+)["']/g;
const staleFontPattern = /\.ttf\b|format\(["']truetype["']\)|fonts\.gstatic\.com\/s\//i;
const fontUrlPattern = /https:\/\/fonts\.itbxm\.com\/[^"')\s]+/g;
const oldFontRoot = `https://${"fonts"}.${"itbxm"}.${"com"}/${"guofeng"}/v1/${"fonts"}/`;
const remoteScriptPattern = /<script[^>]+\bsrc=["']https?:\/\//i;
const localAbsolutePathPattern = /(?:^|["'(\s])(?:file:\/\/)?(?:\/(?:Users|home|var|tmp|private|Applications|Volumes)\/|[A-Za-z]:[\\/]|~[\\/])[^"')\s]*/;
const skillInstallPathPattern = /(?:^|["'(\s/])(?:\.opencode|\.claude|\.agents|\.codex|skills\/itbxm-chinese-guofeng-skill)[^"')\s]*/;
const remoteCssPattern = /<link[^>]+\brel=["']stylesheet["'][^>]+\bhref=["']https?:\/\/([^\/"']+)[^"']*["']/gi;
const allowedRemoteStylesheetPattern = /^https:\/\/(?:fonts\.googleapis\.com\/css2\?|cdn\.itbxm\.com\/fonts\/(?:KingHwaOldSong-MN|ZhaohuaMinA)\/result\.css$)/;
const remoteImageExtensionPattern = /\.(?:png|jpe?g|webp|gif|svg|avif)(?:[?#][^"')\s]*)?$/i;
const remoteImgTagPattern = /<img\b[^>]*\bsrc=["']https?:\/\//i;
const remoteCssUrlPattern = /url\(\s*["']?https?:\/\/(?!fonts\.gstatic\.com\/s\/)/i;
const decorativeFontPattern = /ZhaohuaMinA|KingHwaOldSong-MN|--font-display-(?:heavy|light)|--font-art|--font-poem/i;
const titleSelectorPattern = /(?:^|[\s,])(?:h1|\.title|\.section-title|\.guofeng-display-title)(?:\b|[^\w-])/i;

let failureCount = 0;
let warningCount = 0;

function fail(file, message) {
  failureCount += 1;
  console.error(`${file}: ${message}`);
}

function warn(file, message) {
  warningCount += 1;
  console.error(`${file}: [warn] ${message}`);
}

function normalizeAssetRef(file, ref) {
  if (ref.startsWith("assets/patterns/")) return ref;
  if (ref.startsWith("patterns/")) return ref;
  if (ref.startsWith("../patterns/")) return ref.slice(3);
  if (ref.startsWith("./patterns/")) return ref.slice(2);

  const absolute = path.resolve(path.dirname(file), ref);
  const relative = path.relative(repoRoot, absolute).replaceAll(path.sep, "/");
  if (relative.startsWith("assets/patterns/")) return relative;
  return ref;
}

function isRemoteRef(ref) {
  return /^https?:\/\//i.test(ref);
}

function isProjectAssetRef(ref) {
  return /^(?:\.{1,2}\/)?assets\/(?:patterns|images|runtime)\//.test(ref);
}

function isExternalIgnorableRef(ref) {
  return ref.startsWith("#") || ref.startsWith("data:") || ref.startsWith("mailto:") || ref.startsWith("tel:");
}

function localAssetExists(file, ref) {
  const resolved = path.resolve(path.dirname(file), ref);
  return fs.existsSync(resolved);
}

function getStartTagsWithAttr(html, attr) {
  const escapedAttr = attr.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const tagPattern = new RegExp(`<([a-z][\\w:-]*)([^>]*(?:^|\\s)${escapedAttr}(?=$|[\\s=>/])[^>]*)>`, "gi");
  return [...html.matchAll(tagPattern)].map((match) => ({
    tagName: match[1].toLowerCase(),
    attrs: match[2],
    raw: match[0],
  }));
}

function getAttrValue(attrs, name) {
  const escapedName = name.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const match = attrs.match(new RegExp(`\\b${escapedName}=(["'])(.*?)\\1`, "i"));
  return match?.[2] || "";
}

function hasAttr(attrs, name) {
  const escapedName = name.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return new RegExp(`(?:^|\\s)${escapedName}(?=$|[\\s=>/])`, "i").test(attrs);
}

function hasClass(attrs, className) {
  return getAttrValue(attrs, "class").split(/\s+/).includes(className);
}

function getStartTags(html) {
  return [...html.matchAll(/<([a-z][\w:-]*)([^>]*)>/gi)].map((match) => ({
    tagName: match[1].toLowerCase(),
    attrs: match[2],
    raw: match[0],
  }));
}

function hasTitleElement(html) {
  if (/<h[12]\b/i.test(html)) return true;
  return getStartTags(html).some((tag) => hasClass(tag.attrs, "title") || hasClass(tag.attrs, "section-title"));
}

function hasFooterElement(html) {
  return getStartTags(html).some((tag) => hasClass(tag.attrs, "foot") || hasClass(tag.attrs, "guofeng-foot"));
}

function getDeckSlides(html) {
  return [...html.matchAll(/<section\b([^>]*class=["'][^"']*\bslide\b[^"']*["'][^>]*)>([\s\S]*?)<\/section>/gi)].map((match) => ({
    attrs: match[1],
    html: match[2],
  }));
}

function inferSlideStructure(slide) {
  const layout = getAttrValue(slide.attrs, "data-layout").trim();
  if (layout) return layout;

  const classNames = getAttrValue(slide.attrs, "class").split(/\s+/);
  const body = slide.html;
  if (classNames.includes("cover")) return "cover";
  if (classNames.includes("chapter") || body.includes("deck-chapter-seal")) return "chapter";
  if (/\b(?:card-grid|guofeng-card-grid)\b/i.test(body)) return "card-grid";
  if (/\b(?:timeline|guofeng-timeline|deck-timeline-strip)\b/i.test(body)) return "timeline";
  if (/\b(?:quote|guofeng-quote|deck-quote-slide|deck-quote-text)\b/i.test(body)) return "quote";
  if (/\b(?:artifact|deck-artifact-panel|guofeng-museum-label)\b/i.test(body)) return "artifact";
  if (/<img\b/i.test(body)) return "text-image";
  if (classNames.includes("dark") || classNames.includes("decorated")) return "chapter";
  return "statement";
}

function imageHasAlt(attrs) {
  if (!/\balt\s*=/i.test(attrs)) return false;
  return getAttrValue(attrs, "alt").trim().length > 0;
}

function validateDeckQuality(displayFile, slides) {
  const structures = slides.map(inferSlideStructure);
  for (let index = 2; index < structures.length; index += 1) {
    const current = structures[index];
    if (current && current === structures[index - 1] && current === structures[index - 2]) {
      warn(displayFile, `slides ${index - 1}-${index + 1} repeat the same slide structure: ${current}`);
    }
  }

  const darkCount = slides.filter((slide) => hasClass(slide.attrs, "dark")).length;
  const decoratedCount = slides.filter((slide) => hasClass(slide.attrs, "decorated")).length;
  if (slides.length >= 5 && darkCount > Math.ceil(slides.length * 0.45)) {
    warn(displayFile, `too many dark slides (${darkCount}/${slides.length}); reserve dark for cover, chapter, or closing slides`);
  }
  if (slides.length >= 5 && decoratedCount > Math.ceil(slides.length * 0.65)) {
    warn(displayFile, `too many decorated slides (${decoratedCount}/${slides.length}); keep content slides quieter`);
  }

  for (const [index, slide] of slides.entries()) {
    const slideLabel = `slide ${index + 1}`;
    const revealValues = [...slide.html.matchAll(/\bdata-reveal=(["'])(.*?)\1/gi)].map((match) => Number.parseInt(match[2], 10));
    if (revealValues.some((value) => Number.isFinite(value) && value > 4)) {
      warn(displayFile, `${slideLabel} uses data-reveal delay above 4; keep HTML PPT reveal timing short`);
    }

    const imageTags = getStartTags(slide.html).filter((tag) => tag.tagName === "img");
    if (!imageTags.length) continue;

    for (const image of imageTags) {
      if (!imageHasAlt(image.attrs)) {
        warn(displayFile, `${slideLabel} image is missing alt text`);
      }
    }

    if (!/<figcaption\b/i.test(slide.html) && !/\bclass=["'][^"']*(?:deck-caption-band|guofeng-caption)\b/i.test(slide.html)) {
      warn(displayFile, `${slideLabel} image is missing a caption or caption band`);
    }
  }
}

function getStyleBlocks(html) {
  return [...html.matchAll(/<style\b[^>]*>([\s\S]*?)<\/style>/gi)].map((match) => match[1]);
}

function getCssRules(html) {
  const rules = [];
  for (const block of getStyleBlocks(html)) {
    const cleaned = block.replace(/\/\*[\s\S]*?\*\//g, "");
    for (const match of cleaned.matchAll(/([^{}]+)\{([^{}]+)\}/g)) {
      rules.push({ selector: match[1].trim(), body: match[2].trim() });
    }
  }
  return rules;
}

function cssDeclValue(body, prop) {
  const escapedProp = prop.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const match = body.match(new RegExp(`(?:^|;)\\s*${escapedProp}\\s*:\\s*([^;]+)`, "i"));
  return match?.[1]?.trim() || "";
}

function cssNumericLineHeight(value) {
  const match = value.match(/^([0-9]*\.?[0-9]+)\s*$/);
  return match ? Number.parseFloat(match[1]) : null;
}

function validateVisualSafety(displayFile, html) {
  const rules = getCssRules(html);
  const sideOrnamentAbsolute = rules.some(
    (rule) => rule.selector.includes(".guofeng-side-ornament") && /(?:^|;)\s*position\s*:\s*absolute\b/i.test(rule.body),
  );

  if (
    sideOrnamentAbsolute
    && /\bclass=["'][^"']*\bguofeng-side-ornament\b/i.test(html)
    && (/\bclass=["'][^"']*\b(?:grid-2|text-block|guofeng-scroll-text|guofeng-figure)\b/i.test(html) || /<(?:h[1-3]|p|figure)\b/i.test(html))
  ) {
    warn(displayFile, "side ornament is absolutely positioned near readable content; use a layout column or safe padding so the border cannot overlap text");
  }

  if (/\bclass=["'][^"']*\bclosing__pattern\b/i.test(html) && /\bclass=["'][^"']*\bclosing__accent\b/i.test(html)) {
    warn(displayFile, "closing uses both pattern and accent layers; keep one primary ornament layer or make the secondary layer very subtle without hard visual seams");
  }

  for (const rule of rules) {
    if (!titleSelectorPattern.test(rule.selector)) continue;
    const fontFamily = cssDeclValue(rule.body, "font-family");
    if (!decorativeFontPattern.test(fontFamily)) continue;
    const lineHeight = cssNumericLineHeight(cssDeclValue(rule.body, "line-height"));
    if (lineHeight !== null && lineHeight < 1.12) {
      warn(displayFile, `decorative title line-height ${lineHeight} is below 1.12; multiline Zhaohua/KingHwa titles need 1.16-1.24 or a readable serif fallback`);
    }
  }
}

function validateHtml(fileArg) {
  const file = path.resolve(process.cwd(), fileArg);
  const displayFile = path.relative(repoRoot, file).replaceAll(path.sep, "/") || fileArg;
  const html = fs.readFileSync(file, "utf8");
  const isGuofengDeck = /\bdata-guofeng-deck\b/.test(html);

  if (html.includes("[必填]")) {
    fail(displayFile, "contains [必填] placeholder");
  }

  if (localAbsolutePathPattern.test(html) || skillInstallPathPattern.test(html)) {
    fail(displayFile, "contains local absolute path, skill install path, or agent cache path; copy assets into the output project and use relative paths");
  }

  if (staleFontPattern.test(html)) {
    fail(displayFile, "contains stale TTF, truetype, or direct fonts.gstatic.com/s font-file reference");
  }

  if (html.includes(oldFontRoot)) {
    fail(displayFile, "contains old font CDN root");
  }

  const fontUrls = html.match(fontUrlPattern) || [];
  for (const url of fontUrls) {
    fail(displayFile, `published HTML/CSS must not load old ITBXM font CDN URLs: ${url}`);
  }

  if (html.includes("fonts.googleapis.com") && !html.includes("fonts.googleapis.com/css2")) {
    fail(displayFile, "Google Fonts must use the css2 API");
  }

  for (const match of html.matchAll(remoteCssPattern)) {
    const href = match[0].match(/\bhref=(["'])(.*?)\1/i)?.[2] || "";
    if (!allowedRemoteStylesheetPattern.test(href)) {
      fail(displayFile, `remote stylesheet is not an allowed font CSS URL: ${href}`);
    }
  }

  if (remoteScriptPattern.test(html)) {
    fail(displayFile, "published HTML/CSS should not depend on remote JavaScript");
  }

  if (remoteImgTagPattern.test(html) || remoteCssUrlPattern.test(html)) {
    fail(displayFile, "remote images or CSS url() asset hotlinks are not allowed; copy assets into the output project");
  }

  if (!isGuofengDeck && /<script\b/i.test(html)) {
    fail(displayFile, "ordinary web pages should use CSS-only motion and no JavaScript");
  }

  if (!isGuofengDeck && /guofeng-deck\.js|data-(?:anim|reveal)\b/.test(html)) {
    fail(displayFile, "deck runtime and reveal markers are only allowed in HTML PPT decks");
  }

  if (displayFile.endsWith("web-page.html") && /guofeng-deck\.js|data-guofeng-deck/.test(html)) {
    fail(displayFile, "web page template must not include deck runtime");
  }

  if (isGuofengDeck) {
    validateDeckRuntime(displayFile, html);
  }
  validateVisualSafety(displayFile, html);

  const langMatch = html.match(/<html[^>]*\blang=["']([^"']+)["']/i);
  const lang = langMatch?.[1] || "";
  const hasSC = /Noto (?:Sans|Serif) SC/.test(html);
  const hasTC = /Noto (?:Sans|Serif) TC/.test(html);

  if (/^zh-(?:TW|HK|MO)\b/i.test(lang) && !hasTC) {
    fail(displayFile, `${lang} page should use TC font families`);
  }

  if (/^zh-CN\b/i.test(lang) && !hasSC) {
    fail(displayFile, `${lang} page should use SC font families`);
  }

  if (/^zh-(?:TW|HK|MO)\b/i.test(lang) && html.includes('lang="zh-CN"')) {
    fail(displayFile, "Traditional Chinese page still contains lang=\"zh-CN\"");
  }

  const isInboundTourism = /inbound|foreign traveler|foreign tourist|travel itinerary|tour guide|入境游/i.test(html);
  const isEnglishLang = /^en\b/i.test(lang);
  if ((isInboundTourism || isEnglishLang) && !/[A-Za-z][A-Za-z\s,.'’:-]{24,}/.test(html)) {
    fail(displayFile, "English or inbound tourism page needs readable English or bilingual text");
  }

  const allRefs = [...html.matchAll(urlPattern)]
    .map((match) => match[2] || match[3])
    .filter(Boolean)
    .map((ref) => ref.trim());

  for (const ref of allRefs) {
    if (isExternalIgnorableRef(ref)) continue;

    if (isRemoteRef(ref)) {
      if (remoteImageExtensionPattern.test(ref)) {
        fail(displayFile, `remote image hotlink is not allowed; download it into assets/images/: ${ref}`);
      }
      continue;
    }

    if (isProjectAssetRef(ref) && !localAssetExists(file, ref)) {
      fail(displayFile, `referenced project asset does not exist: ${ref}`);
    }
  }

  const refs = allRefs
    .filter((ref) => !isRemoteRef(ref) && !isExternalIgnorableRef(ref))
    .filter((ref) => ref.includes("patterns/"));

  for (const ref of refs) {
    const normalized = normalizeAssetRef(file, ref);
    if (!knownPatternPaths.has(normalized)) {
      fail(displayFile, `unknown pattern asset path: ${ref}`);
    }
  }
}

function validateDeckRuntime(displayFile, html) {
  if (!/guofeng-deck\.js/.test(html)) {
    fail(displayFile, "HTML PPT deck should load the local guofeng deck runtime");
  }

  const requiredDeckPieces = [
    { pattern: /\bclass=["'][^"']*\bdeck-progress\b/i, label: ".deck-progress" },
    { pattern: /\bclass=["'][^"']*\bdeck-controls\b/i, label: ".deck-controls" },
    { pattern: /\bdata-deck-overview-panel\b/i, label: "[data-deck-overview-panel]" },
    { pattern: /\bdata-deck-overview-grid\b/i, label: "[data-deck-overview-grid]" },
    { pattern: /\bdata-deck-overview-close\b/i, label: "[data-deck-overview-close]" },
  ];

  for (const piece of requiredDeckPieces) {
    if (!piece.pattern.test(html)) {
      fail(displayFile, `HTML PPT deck is missing ${piece.label}`);
    }
  }

  const controlMarkers = [
    {
      marker: "data-deck-progress-text",
      validate: (tag) => tag.tagName === "div" && !hasClass(tag.attrs, "deck"),
      expected: "a separate progress text div, not the deck container",
    },
    {
      marker: "data-deck-progress-fill",
      validate: (tag) => hasClass(tag.attrs, "deck-progress-fill"),
      expected: "an element with class deck-progress-fill",
    },
    {
      marker: "data-deck-prev",
      validate: (tag) => tag.tagName === "button" && hasClass(tag.attrs, "deck-button"),
      expected: "a deck-button button",
    },
    {
      marker: "data-deck-next",
      validate: (tag) => tag.tagName === "button" && hasClass(tag.attrs, "deck-button"),
      expected: "a deck-button button",
    },
    {
      marker: "data-deck-overview",
      validate: (tag) => tag.tagName === "button" && hasClass(tag.attrs, "deck-button"),
      expected: "a deck-button button",
    },
  ];

  for (const control of controlMarkers) {
    const tags = getStartTagsWithAttr(html, control.marker);
    if (!tags.length) {
      fail(displayFile, `HTML PPT deck is missing ${control.marker}`);
      continue;
    }

    for (const tag of tags) {
      if (hasAttr(tag.attrs, "data-guofeng-deck")) {
        fail(displayFile, `${control.marker} must not be placed on the [data-guofeng-deck] container`);
      }

      if (!control.validate(tag)) {
        fail(displayFile, `${control.marker} should be on ${control.expected}`);
      }
    }
  }

  if (/deck-overview\.open\b/.test(html) && !/deck-overview\[hidden\]/.test(html)) {
    fail(displayFile, "deck overview CSS should use .deck-overview[hidden]; the runtime toggles the hidden attribute, not an .open class");
  }

  const overviewPanelTags = getStartTagsWithAttr(html, "data-deck-overview-panel");
  for (const tag of overviewPanelTags) {
    if (!hasClass(tag.attrs, "deck-overview")) {
      fail(displayFile, "data-deck-overview-panel should be on the .deck-overview panel");
    }
  }

  const overviewGridTags = getStartTagsWithAttr(html, "data-deck-overview-grid");
  for (const tag of overviewGridTags) {
    if (!hasClass(tag.attrs, "deck-overview-grid")) {
      fail(displayFile, "data-deck-overview-grid should be on the .deck-overview-grid container");
    }
  }

  const overviewCloseTags = getStartTagsWithAttr(html, "data-deck-overview-close");
  for (const tag of overviewCloseTags) {
    if (tag.tagName !== "button" || !hasClass(tag.attrs, "deck-button")) {
      fail(displayFile, "data-deck-overview-close should be on a deck-button button");
    }
  }

  for (const tag of getStartTagsWithAttr(html, "data-guofeng-deck")) {
    for (const control of controlMarkers) {
      if (hasAttr(tag.attrs, control.marker)) {
        fail(displayFile, `[data-guofeng-deck] container must not include ${control.marker}`);
      }
    }
  }

  for (const marker of ["data-deck-progress-text", "data-deck-progress-fill", "data-deck-prev", "data-deck-next", "data-deck-overview"]) {
    if (!html.includes(marker)) {
      fail(displayFile, `HTML PPT deck is missing ${marker}`);
    }
  }

  const slides = getDeckSlides(html);
  for (const [index, slide] of slides.entries()) {
    const slideHtml = slide.html;
    const slideLabel = `slide ${index + 1}`;
    if (!hasTitleElement(slideHtml)) {
      fail(displayFile, `${slideLabel} is missing a title`);
    }
    if (!hasFooterElement(slideHtml)) {
      fail(displayFile, `${slideLabel} is missing a footer or signature area`);
    }
  }

  validateDeckQuality(displayFile, slides);
}

for (const arg of args) {
  validateHtml(arg);
}

if (failureCount > 0) {
  console.error(`Guofeng validation failed with ${failureCount} issue(s).`);
  process.exit(1);
}

if (warningCount > 0) {
  console.log(`Guofeng validation passed for ${args.length} file(s) with ${warningCount} warning(s).`);
} else {
  console.log(`Guofeng validation passed for ${args.length} file(s).`);
}
