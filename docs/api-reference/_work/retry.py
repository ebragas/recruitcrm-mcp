#!/usr/bin/env python3
"""Retry the failed scrapes with longer waits and sequential (not parallel) requests."""
import json
import os
import re
import time
import urllib.request

API_KEY = "fc-8a34364bcd8345d6bbe7ac094e60795f"
OUT_DIR = "/Users/eric/dev/magicandco/recruitcrm-mcp/docs/api-reference"
WORK_DIR = os.path.join(OUT_DIR, "_work")
RETRY_FILE = os.path.join(WORK_DIR, "retry_urls.txt")


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


def scrape(url, wait_ms=6000):
    payload = json.dumps({
        "url": url,
        "formats": ["markdown"],
        "onlyMainContent": True,
        "waitFor": wait_ms,
        "timeout": 60000,
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


with open(RETRY_FILE) as f:
    urls = [l.strip() for l in f if l.strip()]

print(f"Retrying {len(urls)} URLs sequentially with 6s wait...")
ok, fail = 0, 0
still_fail = []
for i, url in enumerate(urls, 1):
    slug = slug_from_url(url)
    out_path = os.path.join(OUT_DIR, f"{slug}.md")
    attempts = 0
    while attempts < 3:
        attempts += 1
        try:
            result = scrape(url, wait_ms=6000 + attempts * 2000)
            md = (result.get("data") or {}).get("markdown", "")
            if result.get("success") and len(md) >= 200:
                title = ((result.get("data") or {}).get("metadata") or {}).get("title", "")
                header = f"<!-- source: {url} -->\n<!-- title: {title} -->\n\n"
                with open(out_path, "w") as fout:
                    fout.write(header + clean_markdown(md))
                print(f"[{i:2d}/{len(urls)}] OK  {slug:55s} {len(md)} chars (attempt {attempts})")
                ok += 1
                break
            else:
                reason = result.get("error") or f"too-short({len(md)})"
                if attempts >= 3:
                    print(f"[{i:2d}/{len(urls)}] ERR {slug:55s} {reason}")
                    fail += 1
                    still_fail.append((url, reason))
                else:
                    time.sleep(3)
        except Exception as e:
            if attempts >= 3:
                print(f"[{i:2d}/{len(urls)}] ERR {slug:55s} exception: {e}")
                fail += 1
                still_fail.append((url, str(e)))
            else:
                time.sleep(3)

print(f"\nRetry done. ok={ok} fail={fail}")
if still_fail:
    with open(os.path.join(WORK_DIR, "still_failed.txt"), "w") as f:
        for u, r in still_fail:
            f.write(f"{u}\t{r}\n")
