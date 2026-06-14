#!/usr/bin/env python3

import json
import os
import re
import shutil
import sys
from datetime import date
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode, urljoin, urlparse
from urllib.request import Request, urlopen


WIKIMEDIA_API = "https://commons.wikimedia.org/w/api.php"
MET_SEARCH_API = "https://collectionapi.metmuseum.org/public/collection/v1/search"
MET_OBJECT_API = "https://collectionapi.metmuseum.org/public/collection/v1/objects"
AIC_SEARCH_API = "https://api.artic.edu/api/v1/artworks/search"
UA = "itbxm-guofeng-asset-fetcher/1.1 (https://github.com/itbxm/itbxm-chinese-guofeng-skill; asset workflow)"
PROXY_ENV_KEYS = ("ALL_PROXY", "HTTP_PROXY", "HTTPS_PROXY", "all_proxy", "http_proxy", "https_proxy")

ASSET_TYPES = {
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
}

PROVIDERS = {
    "local": {"tier": "A", "mode": "auto", "label": "本地素材"},
    "official-web": {"tier": "A", "mode": "auto", "label": "官方网站/低反爬页面"},
    "wikimedia": {"tier": "A", "mode": "auto", "label": "Wikimedia Commons"},
    "logo": {"tier": "A", "mode": "auto", "label": "SVGL/Simple Icons/Google favicon"},
    "svgl": {"tier": "A", "mode": "auto", "label": "SVGL"},
    "simple-icons": {"tier": "A", "mode": "auto", "label": "Simple Icons"},
    "google-favicon": {"tier": "A", "mode": "auto", "label": "Google favicon"},
    "met-museum": {"tier": "A", "mode": "auto", "label": "Met Museum Open Access"},
    "aic-api": {"tier": "A", "mode": "auto", "label": "Art Institute of Chicago API"},
    "app-store-lead": {"tier": "B", "mode": "lead", "label": "App Store 截图线索"},
    "google-play-lead": {"tier": "B", "mode": "lead", "label": "Google Play 截图线索"},
    "unsplash-lead": {"tier": "B", "mode": "lead", "label": "Unsplash 内容相关摄影线索"},
    "pexels-lead": {"tier": "B", "mode": "lead", "label": "Pexels 内容相关摄影线索"},
    "video-frame-lead": {"tier": "B", "mode": "lead", "label": "官方视频截帧线索"},
    "wechat": {"tier": "B", "mode": "lead", "label": "微信公众号"},
    "xiaohongshu": {"tier": "B", "mode": "lead", "label": "小红书"},
    "dianping": {"tier": "B", "mode": "lead", "label": "点评/美团"},
    "meituan": {"tier": "B", "mode": "lead", "label": "点评/美团"},
    "ctrip": {"tier": "B", "mode": "lead", "label": "携程/马蜂窝"},
    "mafengwo": {"tier": "B", "mode": "lead", "label": "携程/马蜂窝"},
    "jd": {"tier": "B", "mode": "lead", "label": "京东官方店"},
    "tmall": {"tier": "B", "mode": "lead", "label": "天猫官方店"},
    "douyin": {"tier": "B", "mode": "lead", "label": "抖音/快手"},
    "kuaishou": {"tier": "B", "mode": "lead", "label": "抖音/快手"},
    "baidu-image": {"tier": "B", "mode": "lead", "label": "百度图片"},
    "sogou-image": {"tier": "B", "mode": "lead", "label": "搜狗图片"},
    "360-image": {"tier": "B", "mode": "lead", "label": "360 图片搜索"},
    "login-wall": {"tier": "C", "mode": "blocked", "label": "登录墙"},
    "strong-risk-control": {"tier": "C", "mode": "blocked", "label": "强风控平台"},
    "signed-token-platform": {"tier": "C", "mode": "blocked", "label": "签名 token 平台"},
    "bulk-platform-history": {"tier": "C", "mode": "blocked", "label": "批量历史内容"},
}

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg", ".avif"}
SOURCE_PROFILES = {"domestic", "international", "balanced"}
DOMESTIC_LEAD_PROVIDERS = [
    "wechat",
    "xiaohongshu",
    "dianping",
    "meituan",
    "ctrip",
    "mafengwo",
    "jd",
    "tmall",
    "douyin",
    "kuaishou",
    "baidu-image",
    "sogou-image",
    "360-image",
]

SEARCH_IMAGE_LEADS = ["baidu-image", "sogou-image", "360-image"]
ECOMMERCE_LEADS = ["jd", "tmall"]
STOCK_PHOTO_LEADS = ["unsplash-lead", "pexels-lead"]
PLACE_LEADS = ["wechat", "xiaohongshu", "ctrip", "mafengwo", "douyin", "kuaishou", *SEARCH_IMAGE_LEADS]
LOCAL_BUSINESS_LEADS = [
    "wechat",
    "xiaohongshu",
    "dianping",
    "meituan",
    "ctrip",
    "mafengwo",
    "douyin",
    "kuaishou",
    *SEARCH_IMAGE_LEADS,
]


def parse_args(argv):
    parsed = {
        "query": [],
        "providers": None,
        "providers_explicit": False,
        "local_dirs": [],
        "count": 10,
        "pick": 2,
        "width": 1600,
        "source_profile": "balanced",
        "wikimedia_count": 2,
    }
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--slot":
            i += 1
            parsed["slot"] = argv[i]
        elif arg == "--type":
            i += 1
            parsed["type"] = argv[i]
        elif arg == "--query":
            i += 1
            while i < len(argv) and not argv[i].startswith("--"):
                parsed["query"].append(argv[i])
                i += 1
            i -= 1
        elif arg == "--out":
            i += 1
            parsed["out"] = argv[i]
        elif arg == "--providers":
            i += 1
            parsed["providers"] = [value.strip() for value in argv[i].split(",") if value.strip()]
            parsed["providers_explicit"] = True
        elif arg == "--source-profile":
            i += 1
            parsed["source_profile"] = argv[i]
        elif arg == "--wikimedia-count":
            i += 1
            parsed["wikimedia_count"] = int(argv[i])
        elif arg == "--count":
            i += 1
            parsed["count"] = int(argv[i])
        elif arg == "--pick":
            i += 1
            parsed["pick"] = int(argv[i])
        elif arg == "--width":
            i += 1
            parsed["width"] = int(argv[i])
        elif arg == "--source-url":
            i += 1
            parsed["source_url"] = argv[i]
        elif arg == "--local-dir":
            i += 1
            parsed["local_dirs"].append(argv[i])
        elif arg == "--manifest":
            i += 1
            parsed["manifest"] = argv[i]
        elif arg == "--candidates":
            i += 1
            parsed["candidates"] = argv[i]
        elif arg == "--asset-spec":
            i += 1
            parsed["asset_spec"] = argv[i]
        elif arg == "--domain":
            i += 1
            parsed["domain"] = argv[i]
        elif arg in ("--help", "-h"):
            parsed["help"] = True
        else:
            raise ValueError(f"Unknown argument: {arg}")
        i += 1

    if not parsed.get("help"):
        if not parsed.get("slot"):
            raise ValueError("Missing --slot")
        if not parsed.get("type"):
            raise ValueError("Missing --type")
        if parsed["type"] not in ASSET_TYPES:
            raise ValueError(f"--type must be one of: {', '.join(sorted(ASSET_TYPES))}")
        if not parsed["query"]:
            raise ValueError("Missing --query")
        if not parsed.get("out"):
            raise ValueError("Missing --out")
        if parsed["count"] < 1:
            raise ValueError("--count must be a positive integer")
        if parsed["pick"] < 1:
            raise ValueError("--pick must be a positive integer")
        if parsed["width"] < 200:
            raise ValueError("--width must be an integer >= 200")
        if parsed["source_profile"] not in SOURCE_PROFILES:
            raise ValueError("--source-profile must be one of: domestic, international, balanced")
        if parsed["wikimedia_count"] < 0:
            raise ValueError("--wikimedia-count must be an integer >= 0")
        if parsed["providers"] is None:
            parsed["providers"] = providers_for_profile(parsed["source_profile"], parsed["wikimedia_count"], parsed["type"])
    return parsed


def providers_for_profile(source_profile, wikimedia_count, asset_type="generic"):
    if asset_type == "brand-logo":
        return ["local", "svgl", "simple-icons", "official-web", "google-favicon"]
    if asset_type == "ui":
        return ["local", "official-web", "app-store-lead", "google-play-lead", "video-frame-lead"]
    if asset_type == "product":
        providers = ["local", "official-web", "video-frame-lead"]
        if source_profile == "domestic":
            return [*providers, *ECOMMERCE_LEADS, *SEARCH_IMAGE_LEADS]
        if source_profile == "balanced":
            return [*providers, *ECOMMERCE_LEADS, *SEARCH_IMAGE_LEADS, *STOCK_PHOTO_LEADS]
        return providers
    if asset_type in {"artifact", "document"}:
        providers = ["local", "official-web"]
        if source_profile in {"international", "balanced"}:
            if wikimedia_count > 0:
                providers.append("wikimedia")
            providers.extend(["met-museum", "aic-api"])
        if source_profile in {"domestic", "balanced"}:
            providers.extend(SEARCH_IMAGE_LEADS)
        return providers
    if asset_type in {"place", "food", "space", "event"}:
        providers = ["local", "official-web"]
        if source_profile in {"domestic", "balanced"}:
            providers.extend(PLACE_LEADS if asset_type == "place" else LOCAL_BUSINESS_LEADS)
        if source_profile in {"international", "balanced"}:
            providers.extend(STOCK_PHOTO_LEADS)
            if wikimedia_count > 0:
                providers.append("wikimedia")
        return providers
    if source_profile == "domestic":
        return ["local", "official-web", *DOMESTIC_LEAD_PROVIDERS]
    if source_profile == "international":
        providers = ["local", "official-web"]
        if wikimedia_count > 0:
            providers.append("wikimedia")
        return providers
    providers = ["local", "official-web", *DOMESTIC_LEAD_PROVIDERS]
    if wikimedia_count > 0:
        providers.append("wikimedia")
    return providers


def classify_provider(provider):
    return PROVIDERS.get(provider, {"tier": "C", "mode": "blocked", "label": provider})


def safe_file_name(value):
    value = re.sub(r"[^\w]+", "_", str(value), flags=re.UNICODE)
    value = re.sub(r"^_+|_+$", "", value)
    return value[:96] or "asset"


def build_asset_manifest_entry(slot, asset_type, required, queries, providers, status, score, final_file, source_url):
    return f"| {slot} | {asset_type} | {required or '必需'} | {' / '.join(queries)} | {','.join(providers)} | {status} | {score if score is not None else '-'} | {final_file or '-'} | {source_url or '-'} |\n"


def build_asset_lead_entry(lead):
    return f"| {lead['slot']} | {lead['provider']} | {lead['query']} | {lead['action']} |\n"


def lead_action(provider):
    actions = {
        "app-store-lead": "浏览器打开 App Store 产品页，保存官方截图；确认不是过期或无关 mockup。",
        "google-play-lead": "浏览器打开 Google Play 产品页，保存官方截图；确认界面版本和产品匹配。",
        "video-frame-lead": "打开官方发布片、演示视频或新闻稿视频，截取清晰帧；不要抓非官方搬运视频。",
        "unsplash-lead": "仅当图片与内容对象有关时，在 Unsplash 查找可追溯摄影素材；不要给纯装饰位滥用 stock photo。",
        "pexels-lead": "仅当图片与内容对象有关时，在 Pexels 查找可追溯摄影素材；不要给纯装饰位滥用 stock photo。",
        "jd": "浏览器打开官方旗舰店或品牌自营页，保存可见产品图；不要绕登录或批量抓取。",
        "tmall": "浏览器打开官方旗舰店或品牌自营页，保存可见产品图；不要绕登录或批量抓取。",
    }
    return actions.get(provider, "浏览器打开后保存可见素材或截图；不要写绕风控脚本")


def strip_html(value):
    value = re.sub(r"<[^>]+>", "", str(value or "?"))
    value = re.sub(r"\s+", " ", value).strip()
    return value or "?"


def is_ignorable_url(url):
    return not url or url.startswith(("#", "data:", "mailto:", "tel:"))


def to_absolute_url(value, base_url):
    trimmed = str(value or "").strip().strip("\"'")
    if is_ignorable_url(trimmed):
        return ""
    try:
        return urljoin(base_url, trimmed)
    except ValueError:
        return ""


def is_image_url(url):
    return Path(urlparse(url).path).suffix.lower() in IMAGE_EXTENSIONS


def image_extension(value):
    path_value = urlparse(value).path if str(value).startswith("http") else str(value)
    ext = Path(path_value).suffix.lower()
    return ext if ext in IMAGE_EXTENSIONS else ".jpg"


def push_url(urls, value, base_url):
    url = to_absolute_url(value, base_url)
    if url and is_image_url(url):
        urls.add(url)


def extract_json_ld_images(node, urls, base_url):
    if not node:
        return
    if isinstance(node, str):
        push_url(urls, node, base_url)
    elif isinstance(node, list):
        for item in node:
            extract_json_ld_images(item, urls, base_url)
    elif isinstance(node, dict):
        for key in ("url", "contentUrl"):
            if node.get(key):
                push_url(urls, node[key], base_url)
        for key in ("image", "thumbnailUrl"):
            extract_json_ld_images(node.get(key), urls, base_url)


def extract_image_urls_from_html(html, base_url):
    urls = set()
    for match in re.finditer(r"<meta\b[^>]*(?:property|name)=[\"'](?:og:image|twitter:image)[\"'][^>]*content=[\"']([^\"']+)[\"'][^>]*>", html, re.I):
        push_url(urls, match.group(1), base_url)
    for match in re.finditer(r"<meta\b[^>]*content=[\"']([^\"']+)[\"'][^>]*(?:property|name)=[\"'](?:og:image|twitter:image)[\"'][^>]*>", html, re.I):
        push_url(urls, match.group(1), base_url)
    for match in re.finditer(r"<img\b[^>]*\bsrc=[\"']([^\"']+)[\"'][^>]*>", html, re.I):
        push_url(urls, match.group(1), base_url)
    for match in re.finditer(r"\bsrcset=[\"']([^\"']+)[\"']", html, re.I):
        for part in match.group(1).split(","):
            push_url(urls, part.strip().split()[0], base_url)
    for match in re.finditer(r"url\(\s*[\"']?([^\"')]+)[\"']?\s*\)", html, re.I):
        push_url(urls, match.group(1), base_url)
    for match in re.finditer(r"<script\b[^>]*type=[\"']application/ld\+json[\"'][^>]*>([\s\S]*?)</script>", html, re.I):
        try:
            extract_json_ld_images(json.loads(match.group(1)), urls, base_url)
        except json.JSONDecodeError:
            pass
    return list(urls)


def is_image_file(file_path):
    return file_path.suffix.lower() in IMAGE_EXTENSIONS


def walk_images(directory, max_depth=4, max_files=250):
    results = []
    root = Path(directory)
    if not root.exists():
        return results
    for current_root, dirs, files in os.walk(root):
        current = Path(current_root)
        depth = len(current.relative_to(root).parts)
        if depth > max_depth or len(results) >= max_files:
            dirs[:] = []
            continue
        dirs[:] = [name for name in dirs if not name.startswith(".")]
        for name in files:
            if len(results) >= max_files:
                break
            file_path = current / name
            if not name.startswith(".") and is_image_file(file_path):
                results.append(file_path)
    return results


def make_candidate(candidate):
    provider_info = classify_provider(candidate["provider"])
    score = candidate.get("score")
    if score is None:
        score = score_candidate({**candidate, "providerTier": provider_info["tier"]})
    return {
        "slot": candidate["slot"],
        "type": candidate["type"],
        "query": candidate["query"],
        "provider": candidate["provider"],
        "providerTier": provider_info["tier"],
        "mode": provider_info["mode"],
        "sourceUrl": candidate["sourceUrl"],
        "sourcePage": candidate.get("sourcePage") or candidate["sourceUrl"],
        "license": candidate.get("license") or "?",
        "author": candidate.get("author") or "?",
        "score": score,
        "selected": False,
    }


def score_candidate(candidate):
    score = 5
    if candidate["provider"] == "local":
        score += 4
    if candidate["provider"] == "official-web":
        score += 3
    if candidate["provider"] == "wikimedia":
        score += 3
    if candidate["provider"] in {"met-museum", "aic-api"}:
        score += 3
    if candidate["provider"] in {"svgl", "simple-icons", "google-favicon"}:
        score += 3
    if candidate.get("sourcePage") and candidate["sourcePage"] != candidate.get("sourceUrl"):
        score += 1
    if candidate.get("license") and candidate["license"] != "?":
        score += 1
    return min(score, 10)


def request_bytes(url, accept=None):
    headers = {"User-Agent": UA}
    if accept:
        headers["Accept"] = accept
    request = Request(url, headers=headers)
    with urlopen(request, timeout=30) as response:
        return response.read()


def request_json(url):
    return json.loads(request_bytes(url, "application/json").decode("utf-8"))


def clear_proxy_env():
    for key in PROXY_ENV_KEYS:
        os.environ.pop(key, None)


def collect_local_candidates(parsed):
    candidates = []
    dirs = parsed["local_dirs"] or default_local_dirs()
    for directory in dirs:
        for file_path in walk_images(Path(directory).resolve()):
            candidates.append(
                make_candidate(
                    {
                        "slot": parsed["slot"],
                        "type": parsed["type"],
                        "query": " / ".join(parsed["query"]),
                        "provider": "local",
                        "sourceUrl": str(file_path),
                        "sourcePage": str(file_path),
                        "license": "local/user-provided",
                        "author": "local",
                    }
                )
            )
    return candidates


def collect_official_web_candidates(parsed):
    source_url = parsed.get("source_url")
    if not source_url:
        return []
    html = request_bytes(source_url, "text/html").decode("utf-8", errors="replace")
    return [
        make_candidate(
            {
                "slot": parsed["slot"],
                "type": parsed["type"],
                "query": " / ".join(parsed["query"]),
                "provider": "official-web",
                "sourceUrl": url,
                "sourcePage": source_url,
                "license": "official/source-page",
                "author": urlparse(source_url).hostname or "?",
            }
        )
        for url in extract_image_urls_from_html(html, source_url)
    ]


def simple_icon_slug(value):
    value = str(value or "").lower()
    value = re.sub(r"[^\w\s-]", "", value)
    value = re.sub(r"\s+", "-", value.strip())
    return value


def add_svg_route(candidates, route, base):
    if isinstance(route, str):
        candidates.append(make_candidate({**base, "provider": "svgl", "sourceUrl": route, "sourcePage": "https://svgl.app", "license": "svgl", "author": "SVGL"}))
    elif isinstance(route, dict):
        for value in route.values():
            if isinstance(value, str):
                add_svg_route(candidates, value, base)


def collect_logo_candidates(parsed, allowed_provider=None):
    query = parsed["query"][0]
    candidates = []
    if allowed_provider in (None, "svgl"):
        try:
            data = request_json(f"https://api.svgl.app?search={quote(query)}")
            records = data if isinstance(data, list) else data.get("data", [])
            for record in records[:4]:
                add_svg_route(candidates, record.get("route") or record.get("logo") or record.get("url"), {"slot": parsed["slot"], "type": parsed["type"], "query": query})
        except (HTTPError, URLError, OSError, ValueError, AttributeError):
            pass

    slug = simple_icon_slug(query)
    if slug and allowed_provider in (None, "simple-icons"):
        candidates.append(
            make_candidate(
                {
                    "slot": parsed["slot"],
                    "type": parsed["type"],
                    "query": query,
                    "provider": "simple-icons",
                    "sourceUrl": f"https://cdn.simpleicons.org/{slug}/111111",
                    "sourcePage": "https://simpleicons.org",
                    "license": "simple-icons",
                    "author": "Simple Icons",
                }
            )
        )
    if parsed.get("domain") and allowed_provider in (None, "google-favicon"):
        domain = parsed["domain"]
        candidates.append(
            make_candidate(
                {
                    "slot": parsed["slot"],
                    "type": parsed["type"],
                    "query": query,
                    "provider": "google-favicon",
                    "sourceUrl": f"https://www.google.com/s2/favicons?domain={quote(domain)}&sz=256",
                    "sourcePage": f"https://{domain}",
                    "license": "site favicon",
                    "author": domain,
                }
            )
        )
    return candidates


def collect_wikimedia_candidates(parsed):
    clear_proxy_env()
    candidates = []
    for query in parsed["query"]:
        url = f"{WIKIMEDIA_API}?{urlencode({'action': 'query', 'format': 'json', 'generator': 'search', 'gsrsearch': query, 'gsrnamespace': '6', 'gsrlimit': str(parsed['count']), 'prop': 'imageinfo', 'iiprop': 'url|extmetadata', 'iiurlwidth': str(parsed['width'])})}"
        data = request_json(url)
        for page in list((data.get("query", {}).get("pages") or {}).values())[: parsed["count"]]:
            image_info = (page.get("imageinfo") or [{}])[0]
            source_url = image_info.get("thumburl") or image_info.get("url")
            if not source_url:
                continue
            meta = image_info.get("extmetadata") or {}
            candidates.append(
                make_candidate(
                    {
                        "slot": parsed["slot"],
                        "type": parsed["type"],
                        "query": query,
                        "provider": "wikimedia",
                        "sourceUrl": source_url,
                        "sourcePage": image_info.get("descriptionurl") or "",
                        "license": strip_html((meta.get("LicenseShortName") or {}).get("value")),
                        "author": strip_html((meta.get("Artist") or {}).get("value")),
                    }
                )
            )
    return candidates


def collect_met_museum_candidates(parsed):
    candidates = []
    remaining = parsed["count"]
    for query in parsed["query"]:
        if remaining <= 0:
            break
        search_url = f"{MET_SEARCH_API}?{urlencode({'hasImages': 'true', 'q': query})}"
        data = request_json(search_url)
        object_ids = data.get("objectIDs") or []
        for object_id in object_ids[:remaining]:
            try:
                record = request_json(f"{MET_OBJECT_API}/{object_id}")
            except (HTTPError, URLError, OSError, ValueError):
                continue
            source_url = record.get("primaryImageSmall") or record.get("primaryImage")
            if not source_url:
                continue
            candidates.append(
                make_candidate(
                    {
                        "slot": parsed["slot"],
                        "type": parsed["type"],
                        "query": query,
                        "provider": "met-museum",
                        "sourceUrl": source_url,
                        "sourcePage": record.get("objectURL") or f"https://www.metmuseum.org/art/collection/search/{object_id}",
                        "license": "Met Museum Open Access",
                        "author": record.get("artistDisplayName") or "The Metropolitan Museum of Art",
                    }
                )
            )
            remaining -= 1
            if remaining <= 0:
                break
    return candidates


def collect_aic_candidates(parsed):
    candidates = []
    for query in parsed["query"]:
        url = f"{AIC_SEARCH_API}?{urlencode({'q': query, 'limit': str(parsed['count']), 'fields': 'id,title,image_id,artist_display'})}"
        data = request_json(url)
        for record in (data.get("data") or [])[: parsed["count"]]:
            image_id = record.get("image_id")
            if not image_id:
                continue
            source_url = f"https://www.artic.edu/iiif/2/{image_id}/full/{parsed['width']},/0/default.jpg"
            object_id = record.get("id")
            candidates.append(
                make_candidate(
                    {
                        "slot": parsed["slot"],
                        "type": parsed["type"],
                        "query": query,
                        "provider": "aic-api",
                        "sourceUrl": source_url,
                        "sourcePage": f"https://www.artic.edu/artworks/{object_id}" if object_id else "https://www.artic.edu/collection",
                        "license": "Art Institute of Chicago API",
                        "author": record.get("artist_display") or "Art Institute of Chicago",
                    }
                )
            )
    return candidates


def source_paths_for_out(out_dir, parsed):
    out = Path(out_dir).resolve()
    parent = out.parent
    sources_dir = parent / "sources" if parent.name == "assets" else parent.parent / "sources"
    return {
        "manifest": Path(parsed.get("manifest") or sources_dir / "asset-manifest.md").resolve(),
        "candidates": Path(parsed.get("candidates") or sources_dir / "asset-candidates.json").resolve(),
        "assetSpec": Path(parsed.get("asset_spec") or sources_dir / "guofeng-asset-spec.md").resolve(),
        "leads": sources_dir / "asset-leads.md",
        "imageSources": sources_dir / "image-sources.md",
    }


def site_root_for_out(out_dir):
    out = Path(out_dir).resolve()
    parent = out.parent
    if parent.name == "assets":
        return parent.parent
    return Path.cwd()


def display_path(path):
    return os.path.relpath(path, Path.cwd()).replace(os.sep, "/")


def default_local_dirs():
    dirs = [Path.cwd()]
    downloads = Path.home() / "Downloads"
    if downloads.exists():
        dirs.append(downloads)
    return dirs


def download_candidate(candidate, out_dir, site_root):
    ext = image_extension(candidate["sourceUrl"])
    source_name = Path(urlparse(candidate["sourceUrl"]).path).name
    base_name = f"{candidate['slot']}_{candidate['provider']}_{source_name}"
    file_name = f"{safe_file_name(base_name)}{ext}"
    file_path = out_dir / file_name
    if candidate["provider"] == "local":
        shutil.copyfile(candidate["sourceUrl"], file_path)
    else:
        file_path.write_bytes(request_bytes(candidate["sourceUrl"]))
    return file_path.relative_to(site_root).as_posix()


def append_markdown_table(file_path, header, entry):
    file_path.parent.mkdir(parents=True, exist_ok=True)
    content = ""
    if not file_path.exists():
        content += header
    content += entry
    with file_path.open("a", encoding="utf-8") as handle:
        handle.write(content)


def append_candidates(file_path, records):
    file_path.parent.mkdir(parents=True, exist_ok=True)
    existing = []
    if file_path.exists():
        try:
            existing = json.loads(file_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            existing = []
    file_path.write_text(json.dumps(existing + records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def image_source_entry(record, retrieved_at):
    return f"| {record['finalFile']} | {record['query']} | {record.get('sourcePage') or record['sourceUrl']} | {record.get('license') or '?'} | {record.get('author') or '?'} | {retrieved_at} |\n"


def write_image_sources(file_path, records, retrieved_at):
    if not records:
        return
    header = "# Image Sources\n\n| Local file | Query | Source URL | License | Author | Retrieved at |\n| --- | --- | --- | --- | --- | --- |\n"
    append_markdown_table(file_path, header, "".join(image_source_entry(record, retrieved_at) for record in records))


def asset_use_note(asset_type):
    notes = {
        "brand-logo": "作为品牌识别核心资产引用；不要用文字或 CSS 重画替代。",
        "product": "作为产品主角或细节展示；不要用泛产品图替代。",
        "ui": "作为真实界面证据；注意避免用户隐私和过期 UI。",
        "place": "作为地点真实性证据；来源页需能确认地名。",
        "food": "作为菜品或餐饮信任素材；来源页需能确认菜名或门店。",
        "space": "作为空间/场地真实性证据；避免过度裁切。",
        "event": "作为活动现场或传播证据；需要日期/主办方语境。",
        "artifact": "作为展品/文物核心图；优先保留名称、年代、馆藏来源。",
        "document": "作为文档/书籍/报告证据；保证关键文字可读。",
        "evidence": "作为证据截图或案例页面；不要裁掉关键来源信息。",
    }
    return notes.get(asset_type, "仅在与内容有内在关联时使用；装饰位不要滥用图片。")


def placeholder_reason(status, final_records, candidates, leads):
    if status == "已验证":
        return "-"
    if final_records:
        return "入选素材低于 8/10，需用户确认后再作为最终素材。"
    if candidates:
        return "候选存在但未能下载为最终本地素材。"
    if leads:
        return "仅生成浏览器辅助线索，需人工保存可见素材或截图。"
    return "未找到可用候选；使用诚实占位并向用户补要素材。"


def write_asset_spec(file_path, parsed, status, candidates, final_records, leads):
    file_path.parent.mkdir(parents=True, exist_ok=True)
    best = final_records[0] if final_records else None
    best_score = best["score"] if best else 0
    final_file = best["finalFile"] if best else "-"
    source_url = (best.get("sourcePage") or best.get("sourceUrl")) if best else "-"
    header = (
        "# Guofeng Asset Spec\n\n"
        "| Slot | Type | Required | Status | Candidate count | Selected count | Best score | Final file | Source URL | Use note | Placeholder reason |\n"
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
    )
    entry = (
        f"| {parsed['slot']} | {parsed['type']} | 必需 | {status} | {len(candidates)} | {len(final_records)} | "
        f"{best_score} | {final_file} | {source_url} | {asset_use_note(parsed['type'])} | "
        f"{placeholder_reason(status, final_records, candidates, leads)} |\n"
    )
    append_markdown_table(file_path, header, entry)


def collect_provider_candidates(provider, parsed):
    if provider == "local":
        return collect_local_candidates(parsed)
    if provider == "official-web":
        return collect_official_web_candidates(parsed)
    if provider == "wikimedia":
        return collect_wikimedia_candidates(parsed)[: parsed["wikimedia_count"]]
    if provider == "met-museum":
        return collect_met_museum_candidates(parsed)
    if provider == "aic-api":
        return collect_aic_candidates(parsed)
    if provider in {"logo", "svgl", "simple-icons", "google-favicon"}:
        return collect_logo_candidates(parsed, None if provider == "logo" else provider)
    return []


def run(argv):
    parsed = parse_args(argv)
    if parsed.get("help"):
        print(
            'Usage: python3 scripts/fetch-guofeng-assets.py --slot "Hero 西湖主视觉" '
            '--type place --query "西湖 杭州 全景" "West Lake Hangzhou panorama" '
            "--out site/assets/images --source-profile balanced --wikimedia-count 2 --count 10 --pick 2"
        )
        print("Profiles: domestic (no Wikimedia), international (Wikimedia allowed), balanced (domestic leads + limited Wikimedia).")
        print("Type-aware defaults add logo, UI, product, museum/open-collection, stock-photo lead, and video-frame lanes when relevant.")
        print("Writes asset-manifest.md, asset-candidates.json, asset-leads.md, image-sources.md, and guofeng-asset-spec.md.")
        print("Explicit --providers still overrides profile defaults.")
        return 0

    out = Path(parsed["out"]).resolve()
    out.mkdir(parents=True, exist_ok=True)
    site_root = site_root_for_out(out)
    paths = source_paths_for_out(out, parsed)
    retrieved_at = date.today().isoformat()
    leads = []
    candidates = []

    for provider in parsed["providers"]:
        provider_info = classify_provider(provider)
        if provider_info["mode"] == "lead":
            for query in parsed["query"]:
                leads.append({"slot": parsed["slot"], "provider": provider, "query": query, "action": lead_action(provider)})
            continue
        if provider_info["mode"] == "blocked":
            for query in parsed["query"]:
                leads.append({"slot": parsed["slot"], "provider": provider, "query": query, "action": "C 级强反爬来源，不自动抓取；改用用户提供素材或官方来源"})
            continue
        try:
            candidates.extend(collect_provider_candidates(provider, parsed)[: parsed["count"]])
        except (HTTPError, URLError, OSError, ValueError) as error:
            print(f"[FAIL {provider}] {error}", file=sys.stderr)

    selected = sorted(candidates, key=lambda item: item["score"], reverse=True)[: parsed["pick"]]
    final_records = []
    for candidate in selected:
        try:
            final_file = download_candidate(candidate, out, site_root)
            candidate["selected"] = True
            candidate["finalFile"] = final_file
            final_records.append({**candidate, "finalFile": final_file})
            print(f"[OK] {final_file} | {candidate['provider']} | score {candidate['score']} | {candidate['sourcePage']}")
        except (HTTPError, URLError, OSError, ValueError) as error:
            print(f"[FAIL download] {candidate['sourceUrl']}: {error}", file=sys.stderr)

    if candidates:
        append_candidates(paths["candidates"], candidates)
    if leads:
        header = "# Asset Leads\n\n| Slot | Provider | Query | Action |\n| --- | --- | --- | --- |\n"
        append_markdown_table(paths["leads"], header, "".join(build_asset_lead_entry(lead) for lead in leads))
        print(f"Lead log: {display_path(paths['leads'])}")

    best = final_records[0] if final_records else None
    status = "已验证" if best and best["score"] >= 8 else ("待用户确认" if best else "占位待补")
    manifest_entry = build_asset_manifest_entry(
        parsed["slot"],
        parsed["type"],
        "必需",
        parsed["query"],
        parsed["providers"],
        status,
        best["score"] if best else 0,
        best["finalFile"] if best else "-",
        (best.get("sourcePage") or best.get("sourceUrl")) if best else "-",
    )
    manifest_header = "# Asset Manifest\n\n| Slot | Type | Required | Queries | Providers | Status | Score | Final file | Source URL |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
    append_markdown_table(paths["manifest"], manifest_header, manifest_entry)
    write_image_sources(paths["imageSources"], final_records, retrieved_at)
    write_asset_spec(paths["assetSpec"], parsed, status, candidates, final_records, leads)

    if not final_records:
        print(
            "No final assets downloaded. Use asset-leads.md, browser-assisted collection, "
            "or an honest placeholder marked 占位待补.",
            file=sys.stderr,
        )
        return 1

    print(f"Manifest: {display_path(paths['manifest'])}")
    print(f"Candidates: {display_path(paths['candidates'])}")
    print(f"Asset spec: {display_path(paths['assetSpec'])}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(run(sys.argv[1:]))
    except Exception as error:
        print(error, file=sys.stderr)
        sys.exit(2)
