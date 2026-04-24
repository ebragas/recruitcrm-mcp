#!/usr/bin/env python3
"""Re-scrape the URLs that either returned empty/stub content or timed out.
Overwrites existing files. Uses longer waitFor to give Stoplight time to
render endpoint content."""
import json
import os
import re
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

API_KEY = "fc-8a34364bcd8345d6bbe7ac094e60795f"
OUT_DIR = "/Users/eric/dev/magicandco/recruitcrm-mcp/docs/api-reference"
WORK_DIR = os.path.join(OUT_DIR, "_work")
URL_LIST = os.path.join(WORK_DIR, "rescrape_urls.txt")


def slug_from_url(url):
    m = re.search(r"/rcrm-api-reference/[^/]+?-([a-z0-9-]+)$", url)
    return m.group(1) if m else url.rsplit("/", 1)[-1]


def clean_markdown(md):
    lines = md.splitlines()
    first = None
    for i, line in enumerate(lines):
        if line.startswith("# ") and "Stoplight" not in line and "Spinner" not in line and "Status embed" not in line:
            first = i
            break
    if first is not None:
        lines = lines[first:]
    out = [l for l in lines if "userway.org/widgetapp" not in l and l.strip() != "Frame"]
    return "\n".join(out).strip() + "\n"


def scrape(url, wait_ms=8000, timeout_ms=90000):
    payload = json.dumps({
        "url": url,
        "formats": ["markdown"],
        "onlyMainContent": True,
        "waitFor": wait_ms,
        "timeout": timeout_ms,
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://api.firecrawl.dev/v1/scrape",
        data=payload,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def looks_like_stub(md: str) -> bool:
    # Real endpoint pages always include the `api.recruitcrm.io/v1/...` URL.
    # Stub fallbacks don't.
    return "api.recruitcrm.io/v1/" not in md


def process(url):
    slug = slug_from_url(url)
    out_path = os.path.join(OUT_DIR, f"{slug}.md")
    last_err = None
    for attempt in range(3):
        wait = 8000 + attempt * 2000
        try:
            result = scrape(url, wait_ms=wait)
            if not result.get("success"):
                last_err = result.get("error", "unknown")
                time.sleep(2)
                continue
            md = (result.get("data") or {}).get("markdown", "")
            if len(md) < 200 or looks_like_stub(md):
                last_err = f"stub/too-short({len(md)})"
                time.sleep(2)
                continue
            title = ((result.get("data") or {}).get("metadata") or {}).get("title", "")
            header = f"<!-- source: {url} -->\n<!-- title: {title} -->\n\n"
            with open(out_path, "w") as f:
                f.write(header + clean_markdown(md))
            return (url, "ok", len(md), attempt + 1)
        except Exception as e:
            last_err = str(e)
            time.sleep(2)
    return (url, f"fail:{last_err}", 0, 3)


def main():
    with open(URL_LIST) as f:
        urls = [l.strip() for l in f if l.strip()]
    print(f"Re-scraping {len(urls)} URLs with 4 workers...")
    with ThreadPoolExecutor(max_workers=4) as ex:
        futs = {ex.submit(process, u): u for u in urls}
        ok, fail = 0, 0
        for i, f in enumerate(as_completed(futs), 1):
            url, status, n, tries = f.result()
            slug = slug_from_url(url)
            if status == "ok":
                ok += 1
                print(f"[{i:2d}/{len(urls)}] OK  {slug:55s} {n:6d} chars (tries={tries})")
            else:
                fail += 1
                print(f"[{i:2d}/{len(urls)}] ERR {slug:55s} {status}")
    print(f"\nok={ok} fail={fail}")


if __name__ == "__main__":
    main()
