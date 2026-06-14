#!/usr/bin/env python3

import json
import math
import re
import sys
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parent.parent

URL_PATTERN = re.compile(r"url\(([\"']?)([^\"')]+)\1\)|(?:src|href)=[\"']([^\"']+)[\"']", re.I)
STALE_FONT_PATTERN = re.compile(r"\.ttf\b|format\([\"']truetype[\"']\)|fonts\.gstatic\.com/s/", re.I)
FONT_URL_PATTERN = re.compile(r"https://fonts\.itbxm\.com/[^\"')\s]+")
OLD_FONT_ROOT = "https://fonts.itbxm.com/guofeng/v1/fonts/"
REMOTE_SCRIPT_PATTERN = re.compile(r"<script[^>]+\bsrc=[\"']https?://", re.I)
LOCAL_ABSOLUTE_PATH_PATTERN = re.compile(r"(?:^|[\"'(\s])(?:file://)?(?:/(?:Users|home|var|tmp|private|Applications|Volumes)/|[A-Za-z]:[\\/]|~[\\/])[^\"')\s]*")
SKILL_INSTALL_PATH_PATTERN = re.compile(r"(?:^|[\"'(\s/])(?:\.opencode|\.claude|\.agents|\.codex|skills/itbxm-chinese-guofeng-skill)[^\"')\s]*")
REMOTE_CSS_PATTERN = re.compile(r"<link[^>]+\brel=[\"']stylesheet[\"'][^>]+\bhref=[\"']https?://([^/\"']+)[^\"']*[\"']", re.I)
ALLOWED_REMOTE_STYLESHEET_PATTERN = re.compile(
    r"^https://(?:fonts\.googleapis\.com/css2\?|cdn\.itbxm\.com/fonts/(?:KingHwaOldSong-MN|ZhaohuaMinA)/result\.css$)"
)
REMOTE_IMAGE_EXTENSION_PATTERN = re.compile(r"\.(?:png|jpe?g|webp|gif|svg|avif)(?:[?#][^\"')\s]*)?$", re.I)
REMOTE_IMG_TAG_PATTERN = re.compile(r"<img\b[^>]*\bsrc=[\"']https?://", re.I)
REMOTE_CSS_URL_PATTERN = re.compile(r"url\(\s*[\"']?https?://(?!fonts\.gstatic\.com/s/)", re.I)
DECORATIVE_FONT_PATTERN = re.compile(r"ZhaohuaMinA|KingHwaOldSong-MN|--font-display-(?:heavy|light)|--font-art|--font-poem", re.I)
TITLE_SELECTOR_PATTERN = re.compile(r"(?:^|[\s,])(?:h1|\.title|\.section-title|\.guofeng-display-title)(?:\b|[^\w-])", re.I)


class Validator:
    def __init__(self):
        self.failure_count = 0
        self.warning_count = 0
        self.known_pattern_paths = self.load_known_pattern_paths()

    def load_known_pattern_paths(self):
        patterns = json.loads((REPO_ROOT / "data" / "patterns.json").read_text(encoding="utf-8"))
        known = set()
        for pattern in patterns:
            for value in (pattern.get("assets") or {}).values():
                if isinstance(value, str):
                    known.add(value)
                    known.add(re.sub(r"^assets/", "", value))
        return known

    def fail(self, file, message):
        self.failure_count += 1
        print(f"{file}: {message}", file=sys.stderr)

    def warn(self, file, message):
        self.warning_count += 1
        print(f"{file}: [warn] {message}", file=sys.stderr)

    def normalize_asset_ref(self, file, ref):
        if ref.startswith("assets/patterns/"):
            return ref
        if ref.startswith("patterns/"):
            return ref
        if ref.startswith("../patterns/"):
            return ref[3:]
        if ref.startswith("./patterns/"):
            return ref[2:]
        absolute = (file.parent / ref).resolve()
        try:
            relative = absolute.relative_to(REPO_ROOT).as_posix()
        except ValueError:
            relative = str(absolute)
        if relative.startswith("assets/patterns/"):
            return relative
        return ref

    @staticmethod
    def is_remote_ref(ref):
        return bool(re.match(r"^https?://", ref, re.I))

    @staticmethod
    def is_project_asset_ref(ref):
        return bool(re.match(r"^(?:\.{1,2}/)?assets/(?:patterns|images|runtime)/", ref))

    @staticmethod
    def is_external_ignorable_ref(ref):
        return ref.startswith(("#", "data:", "mailto:", "tel:"))

    @staticmethod
    def local_asset_exists(file, ref):
        return (file.parent / ref).resolve().exists()

    @staticmethod
    def get_start_tags_with_attr(html, attr):
        escaped_attr = re.escape(attr)
        pattern = re.compile(rf"<([a-z][\w:-]*)([^>]*(?:^|\s){escaped_attr}(?=$|[\s=>/])[^>]*)>", re.I)
        return [{"tagName": match.group(1).lower(), "attrs": match.group(2), "raw": match.group(0)} for match in pattern.finditer(html)]

    @staticmethod
    def get_attr_value(attrs, name):
        match = re.search(rf"\b{re.escape(name)}=([\"'])(.*?)\1", attrs, re.I)
        return match.group(2) if match else ""

    @staticmethod
    def has_attr(attrs, name):
        return bool(re.search(rf"(?:^|\s){re.escape(name)}(?=$|[\s=>/])", attrs, re.I))

    def has_class(self, attrs, class_name):
        return class_name in re.split(r"\s+", self.get_attr_value(attrs, "class"))

    @staticmethod
    def get_start_tags(html):
        return [{"tagName": match.group(1).lower(), "attrs": match.group(2), "raw": match.group(0)} for match in re.finditer(r"<([a-z][\w:-]*)([^>]*)>", html, re.I)]

    def has_title_element(self, html):
        if re.search(r"<h[12]\b", html, re.I):
            return True
        return any(self.has_class(tag["attrs"], "title") or self.has_class(tag["attrs"], "section-title") for tag in self.get_start_tags(html))

    def has_footer_element(self, html):
        return any(self.has_class(tag["attrs"], "foot") or self.has_class(tag["attrs"], "guofeng-foot") for tag in self.get_start_tags(html))

    @staticmethod
    def get_deck_slides(html):
        return [
            {"attrs": match.group(1), "html": match.group(2)}
            for match in re.finditer(r"<section\b([^>]*class=[\"'][^\"']*\bslide\b[^\"']*[\"'][^>]*)>([\s\S]*?)</section>", html, re.I)
        ]

    def infer_slide_structure(self, slide):
        layout = self.get_attr_value(slide["attrs"], "data-layout").strip()
        if layout:
            return layout
        class_names = re.split(r"\s+", self.get_attr_value(slide["attrs"], "class"))
        body = slide["html"]
        if "cover" in class_names:
            return "cover"
        if "chapter" in class_names or "deck-chapter-seal" in body:
            return "chapter"
        if re.search(r"\b(?:card-grid|guofeng-card-grid)\b", body, re.I):
            return "card-grid"
        if re.search(r"\b(?:timeline|guofeng-timeline|deck-timeline-strip)\b", body, re.I):
            return "timeline"
        if re.search(r"\b(?:quote|guofeng-quote|deck-quote-slide|deck-quote-text)\b", body, re.I):
            return "quote"
        if re.search(r"\b(?:artifact|deck-artifact-panel|guofeng-museum-label)\b", body, re.I):
            return "artifact"
        if re.search(r"<img\b", body, re.I):
            return "text-image"
        if "dark" in class_names or "decorated" in class_names:
            return "chapter"
        return "statement"

    def image_has_alt(self, attrs):
        if not re.search(r"\balt\s*=", attrs, re.I):
            return False
        return bool(self.get_attr_value(attrs, "alt").strip())

    def validate_deck_quality(self, display_file, slides):
        structures = [self.infer_slide_structure(slide) for slide in slides]
        for index in range(2, len(structures)):
            current = structures[index]
            if current and current == structures[index - 1] and current == structures[index - 2]:
                self.warn(display_file, f"slides {index - 1}-{index + 1} repeat the same slide structure: {current}")

        dark_count = sum(1 for slide in slides if self.has_class(slide["attrs"], "dark"))
        decorated_count = sum(1 for slide in slides if self.has_class(slide["attrs"], "decorated"))
        if len(slides) >= 5 and dark_count > math.ceil(len(slides) * 0.45):
            self.warn(display_file, f"too many dark slides ({dark_count}/{len(slides)}); reserve dark for cover, chapter, or closing slides")
        if len(slides) >= 5 and decorated_count > math.ceil(len(slides) * 0.65):
            self.warn(display_file, f"too many decorated slides ({decorated_count}/{len(slides)}); keep content slides quieter")

        for index, slide in enumerate(slides):
            slide_label = f"slide {index + 1}"
            reveal_values = [int(match.group(2)) for match in re.finditer(r"\bdata-reveal=([\"'])(.*?)\1", slide["html"], re.I) if match.group(2).isdigit()]
            if any(value > 4 for value in reveal_values):
                self.warn(display_file, f"{slide_label} uses data-reveal delay above 4; keep HTML PPT reveal timing short")

            image_tags = [tag for tag in self.get_start_tags(slide["html"]) if tag["tagName"] == "img"]
            if not image_tags:
                continue
            for image in image_tags:
                if not self.image_has_alt(image["attrs"]):
                    self.warn(display_file, f"{slide_label} image is missing alt text")
            if not re.search(r"<figcaption\b", slide["html"], re.I) and not re.search(r"\bclass=[\"'][^\"']*(?:deck-caption-band|guofeng-caption)\b", slide["html"], re.I):
                self.warn(display_file, f"{slide_label} image is missing a caption or caption band")

    @staticmethod
    def get_style_blocks(html):
        return [match.group(1) for match in re.finditer(r"<style\b[^>]*>([\s\S]*?)</style>", html, re.I)]

    @staticmethod
    def get_css_rules(html):
        rules = []
        for block in Validator.get_style_blocks(html):
            cleaned = re.sub(r"/\*[\s\S]*?\*/", "", block)
            for match in re.finditer(r"([^{}]+)\{([^{}]+)\}", cleaned):
                rules.append({"selector": match.group(1).strip(), "body": match.group(2).strip()})
        return rules

    @staticmethod
    def css_decl_value(body, prop):
        match = re.search(rf"(?:^|;)\s*{re.escape(prop)}\s*:\s*([^;]+)", body, re.I)
        return match.group(1).strip() if match else ""

    @staticmethod
    def css_numeric_line_height(value):
        match = re.match(r"([0-9]*\.?[0-9]+)\s*$", value)
        return float(match.group(1)) if match else None

    def validate_visual_safety(self, display_file, html):
        rules = self.get_css_rules(html)

        side_ornament_absolute = any(
            ".guofeng-side-ornament" in rule["selector"]
            and re.search(r"(?:^|;)\s*position\s*:\s*absolute\b", rule["body"], re.I)
            for rule in rules
        )
        if side_ornament_absolute and re.search(r"\bclass=[\"'][^\"']*\bguofeng-side-ornament\b", html, re.I):
            if re.search(r"\bclass=[\"'][^\"']*\b(?:grid-2|text-block|guofeng-scroll-text|guofeng-figure)\b", html, re.I) or re.search(r"<(?:h[1-3]|p|figure)\b", html, re.I):
                self.warn(display_file, "side ornament is absolutely positioned near readable content; use a layout column or safe padding so the border cannot overlap text")

        if re.search(r"\bclass=[\"'][^\"']*\bclosing__pattern\b", html, re.I) and re.search(r"\bclass=[\"'][^\"']*\bclosing__accent\b", html, re.I):
            self.warn(display_file, "closing uses both pattern and accent layers; keep one primary ornament layer or make the secondary layer very subtle without hard visual seams")

        for rule in rules:
            selector = rule["selector"]
            body = rule["body"]
            if not TITLE_SELECTOR_PATTERN.search(selector):
                continue
            font_family = self.css_decl_value(body, "font-family")
            if not DECORATIVE_FONT_PATTERN.search(font_family):
                continue
            line_height = self.css_numeric_line_height(self.css_decl_value(body, "line-height"))
            if line_height is not None and line_height < 1.12:
                self.warn(display_file, f"decorative title line-height {line_height:g} is below 1.12; multiline Zhaohua/KingHwa titles need 1.16-1.24 or a readable serif fallback")

        quote_text_blocks = re.finditer(
            r"<(?P<tag>[a-z][\w:-]*)\b(?P<attrs>[^>]*class=[\"'][^\"']*\bguofeng-quote-text\b[^\"']*[\"'][^>]*)>(?P<body>[\s\S]*?)</(?P=tag)>",
            html,
            re.I,
        )
        for match in quote_text_blocks:
            body = match.group("body")
            if re.search(r"<br\s*/?>", body, re.I) and not re.search(r"\bclass=[\"'][^\"']*\bguofeng-poem-line\b", body, re.I):
                self.warn(display_file, "poem quote uses <br> without structured poem lines; wrap each verse line in .guofeng-poem-line so browsers do not break classical lines arbitrarily")

    def validate_html(self, file_arg):
        file = (Path.cwd() / file_arg).resolve()
        try:
            display_file = file.relative_to(REPO_ROOT).as_posix()
        except ValueError:
            display_file = str(file_arg)
        html = file.read_text(encoding="utf-8")
        is_guofeng_deck = bool(re.search(r"\bdata-guofeng-deck\b", html))

        if "[必填]" in html:
            self.fail(display_file, "contains [必填] placeholder")
        if LOCAL_ABSOLUTE_PATH_PATTERN.search(html) or SKILL_INSTALL_PATH_PATTERN.search(html):
            self.fail(display_file, "contains local absolute path, skill install path, or agent cache path; copy assets into the output project and use relative paths")
        if STALE_FONT_PATTERN.search(html):
            self.fail(display_file, "contains stale TTF, truetype, or direct fonts.gstatic.com/s font-file reference")
        if OLD_FONT_ROOT in html:
            self.fail(display_file, "contains old font CDN root")
        for url in FONT_URL_PATTERN.findall(html):
            self.fail(display_file, f"published HTML/CSS must not load old ITBXM font CDN URLs: {url}")
        if "fonts.googleapis.com" in html and "fonts.googleapis.com/css2" not in html:
            self.fail(display_file, "Google Fonts must use the css2 API")
        for match in REMOTE_CSS_PATTERN.finditer(html):
            href_match = re.search(r"\bhref=([\"'])(.*?)\1", match.group(0), re.I)
            href = href_match.group(2) if href_match else ""
            if not ALLOWED_REMOTE_STYLESHEET_PATTERN.match(href):
                self.fail(display_file, f"remote stylesheet is not an allowed font CSS URL: {href}")
        if REMOTE_SCRIPT_PATTERN.search(html):
            self.fail(display_file, "published HTML/CSS should not depend on remote JavaScript")
        if REMOTE_IMG_TAG_PATTERN.search(html) or REMOTE_CSS_URL_PATTERN.search(html):
            self.fail(display_file, "remote images or CSS url() asset hotlinks are not allowed; copy assets into the output project")
        if not is_guofeng_deck and re.search(r"<script\b", html, re.I):
            self.fail(display_file, "ordinary web pages should use CSS-only motion and no JavaScript")
        if not is_guofeng_deck and re.search(r"guofeng-deck\.js|data-(?:anim|reveal)\b", html):
            self.fail(display_file, "deck runtime and reveal markers are only allowed in HTML PPT decks")
        if display_file.endswith("web-page.html") and re.search(r"guofeng-deck\.js|data-guofeng-deck", html):
            self.fail(display_file, "web page template must not include deck runtime")
        if is_guofeng_deck:
            self.validate_deck_runtime(display_file, html)
        self.validate_visual_safety(display_file, html)

        lang_match = re.search(r"<html[^>]*\blang=[\"']([^\"']+)[\"']", html, re.I)
        lang = lang_match.group(1) if lang_match else ""
        has_sc = bool(re.search(r"Noto (?:Sans|Serif) SC", html))
        has_tc = bool(re.search(r"Noto (?:Sans|Serif) TC", html))
        if re.match(r"^zh-(?:TW|HK|MO)\b", lang, re.I) and not has_tc:
            self.fail(display_file, f"{lang} page should use TC font families")
        if re.match(r"^zh-CN\b", lang, re.I) and not has_sc:
            self.fail(display_file, f"{lang} page should use SC font families")
        if re.match(r"^zh-(?:TW|HK|MO)\b", lang, re.I) and 'lang="zh-CN"' in html:
            self.fail(display_file, 'Traditional Chinese page still contains lang="zh-CN"')

        is_inbound_tourism = bool(re.search(r"inbound|foreign traveler|foreign tourist|travel itinerary|tour guide|入境游", html, re.I))
        is_english_lang = bool(re.match(r"^en\b", lang, re.I))
        if (is_inbound_tourism or is_english_lang) and not re.search(r"[A-Za-z][A-Za-z\s,.'’:-]{24,}", html):
            self.fail(display_file, "English or inbound tourism page needs readable English or bilingual text")

        all_refs = []
        for match in URL_PATTERN.finditer(html):
            ref = match.group(2) or match.group(3)
            if ref:
                all_refs.append(ref.strip())

        for ref in all_refs:
            if self.is_external_ignorable_ref(ref):
                continue
            if self.is_remote_ref(ref):
                if REMOTE_IMAGE_EXTENSION_PATTERN.search(ref):
                    self.fail(display_file, f"remote image hotlink is not allowed; download it into assets/images/: {ref}")
                continue
            if self.is_project_asset_ref(ref) and not self.local_asset_exists(file, ref):
                self.fail(display_file, f"referenced project asset does not exist: {ref}")

        refs = [ref for ref in all_refs if not self.is_remote_ref(ref) and not self.is_external_ignorable_ref(ref) and "patterns/" in ref]
        for ref in refs:
            normalized = self.normalize_asset_ref(file, ref)
            if normalized not in self.known_pattern_paths:
                self.fail(display_file, f"unknown pattern asset path: {ref}")

    def validate_deck_runtime(self, display_file, html):
        if "guofeng-deck.js" not in html:
            self.fail(display_file, "HTML PPT deck should load the local guofeng deck runtime")

        required_deck_pieces = [
            (re.compile(r"\bclass=[\"'][^\"']*\bdeck-progress\b", re.I), ".deck-progress"),
            (re.compile(r"\bclass=[\"'][^\"']*\bdeck-controls\b", re.I), ".deck-controls"),
            (re.compile(r"\bdata-deck-overview-panel\b", re.I), "[data-deck-overview-panel]"),
            (re.compile(r"\bdata-deck-overview-grid\b", re.I), "[data-deck-overview-grid]"),
            (re.compile(r"\bdata-deck-overview-close\b", re.I), "[data-deck-overview-close]"),
        ]
        for pattern, label in required_deck_pieces:
            if not pattern.search(html):
                self.fail(display_file, f"HTML PPT deck is missing {label}")

        control_markers = [
            ("data-deck-progress-text", lambda tag: tag["tagName"] == "div" and not self.has_class(tag["attrs"], "deck"), "a separate progress text div, not the deck container"),
            ("data-deck-progress-fill", lambda tag: self.has_class(tag["attrs"], "deck-progress-fill"), "an element with class deck-progress-fill"),
            ("data-deck-prev", lambda tag: tag["tagName"] == "button" and self.has_class(tag["attrs"], "deck-button"), "a deck-button button"),
            ("data-deck-next", lambda tag: tag["tagName"] == "button" and self.has_class(tag["attrs"], "deck-button"), "a deck-button button"),
            ("data-deck-overview", lambda tag: tag["tagName"] == "button" and self.has_class(tag["attrs"], "deck-button"), "a deck-button button"),
        ]
        for marker, validate, expected in control_markers:
            tags = self.get_start_tags_with_attr(html, marker)
            if not tags:
                self.fail(display_file, f"HTML PPT deck is missing {marker}")
                continue
            for tag in tags:
                if self.has_attr(tag["attrs"], "data-guofeng-deck"):
                    self.fail(display_file, f"{marker} must not be placed on the [data-guofeng-deck] container")
                if not validate(tag):
                    self.fail(display_file, f"{marker} should be on {expected}")

        if "deck-overview.open" in html and "deck-overview[hidden]" not in html:
            self.fail(display_file, "deck overview CSS should use .deck-overview[hidden]; the runtime toggles the hidden attribute, not an .open class")

        for tag in self.get_start_tags_with_attr(html, "data-deck-overview-panel"):
            if not self.has_class(tag["attrs"], "deck-overview"):
                self.fail(display_file, "data-deck-overview-panel should be on the .deck-overview panel")
        for tag in self.get_start_tags_with_attr(html, "data-deck-overview-grid"):
            if not self.has_class(tag["attrs"], "deck-overview-grid"):
                self.fail(display_file, "data-deck-overview-grid should be on the .deck-overview-grid container")
        for tag in self.get_start_tags_with_attr(html, "data-deck-overview-close"):
            if tag["tagName"] != "button" or not self.has_class(tag["attrs"], "deck-button"):
                self.fail(display_file, "data-deck-overview-close should be on a deck-button button")
        for tag in self.get_start_tags_with_attr(html, "data-guofeng-deck"):
            for marker, _, _ in control_markers:
                if self.has_attr(tag["attrs"], marker):
                    self.fail(display_file, f"[data-guofeng-deck] container must not include {marker}")
        for marker in ["data-deck-progress-text", "data-deck-progress-fill", "data-deck-prev", "data-deck-next", "data-deck-overview"]:
            if marker not in html:
                self.fail(display_file, f"HTML PPT deck is missing {marker}")

        slides = self.get_deck_slides(html)
        for index, slide in enumerate(slides):
            slide_label = f"slide {index + 1}"
            if not self.has_title_element(slide["html"]):
                self.fail(display_file, f"{slide_label} is missing a title")
            if not self.has_footer_element(slide["html"]):
                self.fail(display_file, f"{slide_label} is missing a footer or signature area")
        self.validate_deck_quality(display_file, slides)


def run(argv):
    if argv and argv[0] in ("--help", "-h"):
        print("Usage: python3 scripts/validate-guofeng-html.py <file.html> [...]")
        return 0
    if not argv:
        print("Usage: python3 scripts/validate-guofeng-html.py <file.html> [...]", file=sys.stderr)
        return 2

    validator = Validator()
    for arg in argv:
        validator.validate_html(arg)

    if validator.failure_count > 0:
        print(f"Guofeng validation failed with {validator.failure_count} issue(s).", file=sys.stderr)
        return 1
    if validator.warning_count > 0:
        print(f"Guofeng validation passed for {len(argv)} file(s) with {validator.warning_count} warning(s).")
    else:
        print(f"Guofeng validation passed for {len(argv)} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(run(sys.argv[1:]))
