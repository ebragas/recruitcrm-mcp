#!/usr/bin/env python3
"""Fetch Recruit CRM API docs from Stoplight into individual files.

Uses only stdlib so it can run without a venv:
    python3 scripts/fetch_api_docs.py
"""

import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

PROJECT = "recruitcrm/rcrm-api-reference"
BASE_URL = f"https://stoplight.io/api/v1/projects/{PROJECT}"
TOC_URL = f"{BASE_URL}/nodes/toc.json"
NODE_URL_BASE = f"{BASE_URL}/nodes/"

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs" / "recruitcrm"
DELAY = 0.1  # seconds between requests
MAX_RETRIES = 3


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def fetch_url(url: str) -> bytes:
    """GET a URL and return raw bytes, with retry on 429/5xx."""
    for attempt in range(MAX_RETRIES):
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read()
        except urllib.error.HTTPError as exc:
            if exc.code in (429, 500, 502, 503, 504) and attempt < MAX_RETRIES - 1:
                wait = 2 ** (attempt + 1)
                print(f"  HTTP {exc.code}, retrying in {wait}s...")
                time.sleep(wait)
                continue
            raise
    return b""  # unreachable


def fetch_json(url: str) -> dict:
    """GET a URL and return parsed JSON."""
    return json.loads(fetch_url(url).decode())


def node_url(uri: str) -> str:
    """Build the full URL for fetching a node by its TOC uri."""
    # Strip leading slash; URL-encode path segments (spaces, etc.)
    clean = uri.lstrip("/")
    # Encode the path but preserve slashes and ~1 tilde-encoding
    encoded = urllib.parse.quote(clean, safe="/~")
    return f"{NODE_URL_BASE}{encoded}?deref=optimizedBundle"


# ---------------------------------------------------------------------------
# TOC helpers
# ---------------------------------------------------------------------------

def fetch_toc() -> dict:
    """Fetch the Stoplight table-of-contents."""
    print("Fetching table of contents...")
    return fetch_json(TOC_URL)


def classify_item(uri: str, parent_group: str) -> str:
    """Determine the item type from its URI and parent group context.

    Returns: 'article', 'endpoint', or 'model'.
    """
    if uri.startswith("docs/") and uri.endswith(".md"):
        return "article"
    if parent_group == "Schemas":
        return "model"
    if "/paths/" in uri:
        return "endpoint"
    if "/components/schemas/" in uri:
        return "model"
    # Fallback: if it's under the Endpoints group, treat as endpoint
    return "endpoint"


def flatten_toc(toc: dict) -> list:
    """Walk the TOC tree and return a flat list of items with category context."""
    items = []

    def walk(nodes, category="", parent_group=""):
        for node in nodes:
            ntype = node.get("type", "")
            title = node.get("title", "")
            uri = node.get("uri", "")

            if ntype == "group":
                # Recurse into children, passing this group's title as context
                walk(node.get("items", []), category=title, parent_group=title)
            elif ntype == "item" and uri:
                item_type = classify_item(uri, parent_group)
                items.append({
                    "title": title,
                    "uri": uri,
                    "type": item_type,
                    "category": category,
                })

    walk(toc.get("items", []))
    return items


# ---------------------------------------------------------------------------
# Slug / path helpers
# ---------------------------------------------------------------------------

def slugify(name: str) -> str:
    """Convert a name to a directory/file-safe slug: 'Call Logs' → 'call-logs'."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def endpoint_filename(uri: str, title: str) -> str:
    """Build a filename for an endpoint: 'get-search-for-candidates.json'."""
    # HTTP method is the last path segment
    method = uri.rsplit("/", 1)[-1].lower() if "/" in uri else ""
    return f"{method}-{slugify(title)}.json"


def article_filename(uri: str) -> str:
    """Build a filename for an article: 'getting-started.md'."""
    # e.g. 'docs/Getting Started.md' → 'getting-started.md'
    name = uri.rsplit("/", 1)[-1]
    if name.endswith(".md"):
        name = name[:-3]
    return f"{slugify(name)}.md"


def model_filename(title: str) -> str:
    """Build a filename for a model: 'enroll-candidate.json'."""
    return f"{slugify(title)}.json"


# ---------------------------------------------------------------------------
# Save helpers
# ---------------------------------------------------------------------------

def save_endpoint(item: dict, data: dict) -> Path:
    """Save an endpoint node to docs/recruitcrm/endpoints/<category>/<method-slug>.json."""
    method = data.get("method", "").lower()
    category_dir = slugify(item["category"]) if item["category"] else "other"
    filename = f"{method}-{slugify(item['title'])}.json" if method else f"{slugify(item['title'])}.json"
    path = DOCS_DIR / "endpoints" / category_dir / filename

    doc = {
        "title": item["title"],
        "uri": item["uri"],
        "type": "endpoint",
        "category": item["category"],
        "method": method,
        "path": data.get("path", ""),
        "summary": data.get("summary", ""),
        "data": data,
    }

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=2) + "\n")
    return path


def save_article(item: dict, content: str) -> Path:
    """Save an article node as markdown to docs/recruitcrm/articles/<slug>.md."""
    filename = article_filename(item["uri"])
    path = DOCS_DIR / "articles" / filename

    # Prepend a title heading if the content doesn't start with one
    if not content.startswith("# "):
        content = f"# {item['title']}\n\n{content}"

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content + "\n")
    return path


def save_model(item: dict, data: dict) -> Path:
    """Save a model schema to docs/recruitcrm/models/<slug>.json."""
    filename = model_filename(item["title"])
    path = DOCS_DIR / "models" / filename

    doc = {
        "title": item["title"],
        "uri": item["uri"],
        "type": "model",
        "category": item["category"],
        "data": data,
    }

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=2) + "\n")
    return path


def save_index(items: list, file_map: dict) -> None:
    """Write _index.json manifest with TOC items and file path mapping."""
    counts = {}
    for item in items:
        counts[item["type"]] = counts.get(item["type"], 0) + 1

    index = {
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "counts": counts,
        "total": len(items),
        "files_written": len(file_map),
        "items": [
            {**item, "file": file_map.get(item["uri"], "")}
            for item in items
        ],
    }

    path = DOCS_DIR / "_index.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(index, indent=2) + "\n")
    print(f"  Wrote {path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def fetch_and_save(item: dict) -> Path:
    """Fetch a single node and save it to the appropriate file."""
    url = node_url(item["uri"])
    item_type = item["type"]

    if item_type == "article":
        # Articles return raw markdown, not JSON
        content = fetch_url(url).decode()
        return save_article(item, content)
    elif item_type == "endpoint":
        data = fetch_json(url)
        return save_endpoint(item, data)
    elif item_type == "model":
        data = fetch_json(url)
        return save_model(item, data)
    else:
        raise ValueError(f"Unknown type: {item_type}")


def main() -> None:
    toc = fetch_toc()
    items = flatten_toc(toc)

    if not items:
        print("ERROR: TOC returned no items.", file=sys.stderr)
        sys.exit(1)

    counts = {}
    for item in items:
        counts[item["type"]] = counts.get(item["type"], 0) + 1
    print(f"Found {len(items)} nodes: {counts}")

    file_map = {}
    errors = []

    for i, item in enumerate(items, 1):
        uri = item["uri"]
        label = f"[{i}/{len(items)}] {item['type']:10s} {item['title']}"

        try:
            path = fetch_and_save(item)
            rel = path.relative_to(DOCS_DIR.parent.parent)
            file_map[uri] = str(rel)
            print(f"  {label} -> {rel}")
        except Exception as exc:
            errors.append(f"{uri}: {exc}")
            print(f"  {label} -- ERROR: {exc}")

        time.sleep(DELAY)

    save_index(items, file_map)

    print(f"\nDone: {len(file_map)} files written to {DOCS_DIR}")
    if errors:
        print(f"  {len(errors)} errors:", file=sys.stderr)
        for err in errors:
            print(f"    {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
