#!/usr/bin/env python3
"""Parallel scrape of remaining Recruit CRM API endpoint pages via Firecrawl REST API."""
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import urllib.request

API_KEY = os.environ.get("FIRECRAWL_API_KEY", "fc-8a34364bcd8345d6bbe7ac094e60795f")
OUT_DIR = "/Users/eric/dev/magicandco/recruitcrm-mcp/docs/api-reference"
WORK_DIR = os.path.join(OUT_DIR, "_work")
TODO_FILE = os.path.join(WORK_DIR, "todo_urls.txt")
FAIL_FILE = os.path.join(WORK_DIR, "failed.txt")


def slug_from_url(url: str) -> str:
    m = re.search(r"/rcrm-api-reference/[^/]+?-([a-z0-9-]+)$", url)
    return m.group(1) if m else url.rsplit("/", 1)[-1]


def clean_markdown(md: str) -> str:
    lines = md.splitlines()
    first_heading = None
    for i, line in enumerate(lines):
        if line.startswith("# ") and "Stoplight" not in line and "Spinner" not in line and "Status embed" not in line:
            first_heading = i
            break
    if first_heading is not None:
        lines = lines[first_heading:]
    out = [l for l in lines if "userway.org/widgetapp" not in l and l.strip() != "Frame"]
    return "\n".join(out).strip() + "\n"


def scrape(url: str, retries: int = 2) -> dict:
    payload = json.dumps({
        "url": url,
        "formats": ["markdown"],
        "onlyMainContent": True,
        "waitFor": 3000,
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
    last_err = None
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            last_err = e
            time.sleep(1 + attempt * 2)
    return {"success": False, "error": str(last_err)}


def process(url: str):
    slug = slug_from_url(url)
    out_path = os.path.join(OUT_DIR, f"{slug}.md")
    if os.path.exists(out_path):
        return (url, "skip-existing", 0)
    result = scrape(url)
    if not result.get("success"):
        return (url, f"fail:{result.get('error', 'unknown')}", 0)
    data = result.get("data", {})
    md = data.get("markdown", "")
    if len(md) < 200:
        return (url, f"fail:too-short({len(md)})", 0)
    cleaned = clean_markdown(md)
    title = (data.get("metadata") or {}).get("title", "")
    header = f"<!-- source: {url} -->\n<!-- title: {title} -->\n\n"
    with open(out_path, "w") as f:
        f.write(header + cleaned)
    return (url, "ok", len(cleaned))


def main():
    with open(TODO_FILE) as f:
        urls = [line.strip() for line in f if line.strip()]
    print(f"Scraping {len(urls)} URLs with 8 workers...")
    ok, skip, fail = 0, 0, 0
    failures = []
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=8) as ex:
        futures = {ex.submit(process, u): u for u in urls}
        for i, fut in enumerate(as_completed(futures), 1):
            url, status, n = fut.result()
            slug = slug_from_url(url)
            if status == "ok":
                ok += 1
                tag = "OK "
            elif status == "skip-existing":
                skip += 1
                tag = "SKP"
            else:
                fail += 1
                failures.append((url, status))
                tag = "ERR"
            print(f"[{i:3d}/{len(urls)}] {tag} {slug:55s} {n:6d} {status if status != 'ok' else ''}")
    elapsed = time.time() - t0
    print(f"\nDone in {elapsed:.1f}s. ok={ok} skip={skip} fail={fail}")
    if failures:
        with open(FAIL_FILE, "w") as f:
            for u, s in failures:
                f.write(f"{u}\t{s}\n")
        print(f"Failures written to: {FAIL_FILE}")


if __name__ == "__main__":
    main()
