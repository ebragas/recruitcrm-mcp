#!/usr/bin/env python3
"""Save two manually-fetched pages into the docs/api-reference dir so they can be tidied."""
import json
import os
import re
import urllib.request

API_KEY = "fc-8a34364bcd8345d6bbe7ac094e60795f"
OUT_DIR = "/Users/eric/dev/magicandco/recruitcrm-mcp/docs/api-reference"

URLS = [
    "https://docs.recruitcrm.io/docs/rcrm-api-reference/db2609e77ca90-delete-a-deal",
    "https://docs.recruitcrm.io/docs/rcrm-api-reference/7a94bafe42f7f-search-for-sequences",
]


def slug(url):
    m = re.search(r"/rcrm-api-reference/[^/]+?-([a-z0-9-]+)$", url)
    return m.group(1)


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


for url in URLS:
    payload = json.dumps({
        "url": url,
        "formats": ["markdown"],
        "onlyMainContent": True,
        "waitFor": 15000,
        "maxAge": 0,
        "proxy": "stealth",
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://api.firecrawl.dev/v1/scrape",
        data=payload,
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    md = (result.get("data") or {}).get("markdown", "")
    title = ((result.get("data") or {}).get("metadata") or {}).get("title", "")
    if "api.recruitcrm.io/v1/" not in md:
        print(f"FAIL {slug(url)} — still stub")
        continue
    header = f"<!-- source: {url} -->\n<!-- title: {title} -->\n\n"
    path = os.path.join(OUT_DIR, f"{slug(url)}.md")
    with open(path, "w") as f:
        f.write(header + clean_markdown(md))
    print(f"OK {slug(url)} {len(md)} chars")
