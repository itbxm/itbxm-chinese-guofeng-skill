#!/usr/bin/env python3

import json
import os
import re
import sys
from datetime import date
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen


API = "https://commons.wikimedia.org/w/api.php"
UA = "itbxm-guofeng-image-fetcher/1.0 (skill asset workflow)"


def parse_args(argv):
    parsed = {"query": [], "count": 2, "width": 1600}
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--query":
            i += 1
            while i < len(argv) and not argv[i].startswith("--"):
                parsed["query"].append(argv[i])
                i += 1
            i -= 1
        elif arg == "--out":
            i += 1
            parsed["out"] = argv[i]
        elif arg == "--count":
            i += 1
            parsed["count"] = int(argv[i])
        elif arg == "--width":
            i += 1
            parsed["width"] = int(argv[i])
        elif arg in ("--help", "-h"):
            parsed["help"] = True
        else:
            raise ValueError(f"Unknown argument: {arg}")
        i += 1

    if not parsed.get("help"):
        if not parsed["query"]:
            raise ValueError("Missing --query")
        if not parsed.get("out"):
            raise ValueError("Missing --out")
        if parsed["count"] < 1:
            raise ValueError("--count must be a positive integer")
        if parsed["width"] < 200:
            raise ValueError("--width must be an integer >= 200")
    return parsed


def safe_file_name(value):
    value = re.sub(r"[^\w]+", "_", str(value), flags=re.UNICODE)
    value = re.sub(r"^_+|_+$", "", value)
    return value[:80] or "image"


def build_source_entry(local_file, query, source_url, license_name, artist, retrieved_at):
    return f"| {local_file} | {query} | {source_url} | {license_name or '?'} | {artist or '?'} | {retrieved_at} |\n"


def strip_html(value):
    value = re.sub(r"<[^>]+>", "", str(value or "?"))
    value = re.sub(r"\s+", " ", value).strip()
    return value or "?"


def image_extension(url):
    ext = Path(urlparse(url).path).suffix.lower()
    if ext in {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg"}:
        return ext
    return ".jpg"


def sources_path_for_out(out_dir):
    absolute_out = Path(out_dir).resolve()
    parent = absolute_out.parent
    sources_dir = parent / "sources" if parent.name == "assets" else parent.parent / "sources"
    return sources_dir / "image-sources.md"


def site_root_for_out(out_dir):
    absolute_out = Path(out_dir).resolve()
    parent = absolute_out.parent
    if parent.name == "assets":
        return parent.parent
    return Path.cwd()


def display_path(path):
    return os.path.relpath(path, Path.cwd()).replace(os.sep, "/")


def request_bytes(url, accept=None):
    headers = {"User-Agent": UA}
    if accept:
        headers["Accept"] = accept
    request = Request(url, headers=headers)
    with urlopen(request, timeout=30) as response:
        return response.read()


def api_get(params):
    url = f"{API}?{urlencode(params)}"
    return json.loads(request_bytes(url, "application/json").decode("utf-8"))


def download_file(url, file_path):
    file_path.write_bytes(request_bytes(url))


def fetch_query(query, options):
    data = api_get(
        {
            "action": "query",
            "format": "json",
            "generator": "search",
            "gsrsearch": query,
            "gsrnamespace": "6",
            "gsrlimit": str(options["count"]),
            "prop": "imageinfo",
            "iiprop": "url|extmetadata",
            "iiurlwidth": str(options["width"]),
        }
    )
    pages = list((data.get("query", {}).get("pages") or {}).values())
    records = []
    for page in pages[: options["count"]]:
        image_info = (page.get("imageinfo") or [{}])[0]
        image_url = image_info.get("thumburl") or image_info.get("url")
        if not image_url:
            continue

        meta = image_info.get("extmetadata") or {}
        license_name = strip_html((meta.get("LicenseShortName") or {}).get("value"))
        artist = strip_html((meta.get("Artist") or {}).get("value"))
        source_url = image_info.get("descriptionurl") or ""
        title = str(page.get("title") or "image").removeprefix("File:")
        file_name = f"{safe_file_name(f'{query}_{title}')}{image_extension(image_url)}"
        file_path = options["out"] / file_name
        download_file(image_url, file_path)
        records.append(
            {
                "local_file": file_path.relative_to(options["site_root"]).as_posix(),
                "query": query,
                "source_url": source_url,
                "license": license_name,
                "artist": artist,
            }
        )
    return records


def append_sources(source_file, records, retrieved_at):
    source_file.parent.mkdir(parents=True, exist_ok=True)
    content = ""
    if not source_file.exists():
        content += "# Image Sources\n\n"
        content += "| Local file | Query | Source URL | License | Author | Retrieved at |\n"
        content += "| --- | --- | --- | --- | --- | --- |\n"
    for record in records:
        content += build_source_entry(
            record["local_file"],
            record["query"],
            record["source_url"],
            record["license"],
            record["artist"],
            retrieved_at,
        )
    with source_file.open("a", encoding="utf-8") as handle:
        handle.write(content)


def run(argv):
    parsed = parse_args(argv)
    if parsed.get("help"):
        print(
            'Usage: python3 scripts/fetch-guofeng-images.py --query "West Lake Hangzhou" '
            '"Lingyin Temple Hangzhou" --out site/assets/images --count 2 --width 1600'
        )
        return 0

    out = Path(parsed["out"]).resolve()
    out.mkdir(parents=True, exist_ok=True)
    options = {**parsed, "out": out, "site_root": site_root_for_out(out)}
    source_file = sources_path_for_out(out)
    retrieved_at = date.today().isoformat()
    all_records = []

    for query in parsed["query"]:
        try:
            records = fetch_query(query, options)
            if not records:
                print(f"[EMPTY] {query}: Wikimedia Commons returned no downloadable images.", file=sys.stderr)
            else:
                all_records.extend(records)
                for record in records:
                    print(
                        f"[OK] {record['local_file']} | {record['license']} | "
                        f"{record['artist']} | {record['source_url']}"
                    )
        except (HTTPError, URLError, OSError, ValueError) as error:
            print(f"[FAIL] {query}: {error}", file=sys.stderr)

    if not all_records:
        print(
            "No images downloaded. Use browser/WebSearch, Unsplash/Pexels/manual sources, "
            "or honest placeholders with a material list.",
            file=sys.stderr,
        )
        return 1

    append_sources(source_file, all_records, retrieved_at)
    print(f"\nDownloaded {len(all_records)} image(s) to {out}")
    print(f"Source log: {display_path(source_file)}")
    print("Review each image for 8/10 fit before using it in final HTML.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(run(sys.argv[1:]))
    except Exception as error:
        print(error, file=sys.stderr)
        sys.exit(2)
