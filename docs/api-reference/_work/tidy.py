#!/usr/bin/env python3
"""Post-process scraped Recruit CRM API docs into tight, readable markdown.

Transforms applied per file:
1. Strip the trailing sidebar nav chrome (everything from the `[![recruitcrm]...` marker onward).
2. Strip Stoplight "try it" widget block: Auth / Token / Parameters / Body / Send API Request / Prod / Request Sample.
3. Strip self-referential `#heading-id` URL suffixes inside headings: `## [Request](.../#Request)` → `## Request`.
4. Merge the method + URL lines under the title into one line: `**POST** `/v1/foo``.
5. Collapse vertical parameter blocks into compact bullet lists.
6. Drop duplicated `application/json` content-type line pairs.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

DOCS_DIR = Path("/Users/eric/dev/magicandco/recruitcrm-mcp/docs/api-reference")

# ---- regex helpers -----------------------------------------------------------

# Heading links like: ## [Request](https://.../#Request)
HEADING_LINK_RE = re.compile(r"^(#+)\s*\[([^\]]+)\]\([^)]*#[^)]*\)\s*$")

# Trailing sidebar marker — literal string appears at the start of nav chrome
SIDEBAR_MARKER = "[![recruitcrm]"

# Known HTTP verbs that appear as their own line right after the H1
METHODS = {"get", "post", "put", "patch", "delete"}

# Known scalar types that mark the second element of a param block
PARAM_TYPES = {
    "string", "integer", "number", "boolean", "array", "object",
    "array of objects", "array of strings", "array of integers",
    "file", "date", "datetime", "null",
}

# Sections inside the "try it" widget we want to drop
WIDGET_SECTION_STARTS = (
    "Auth", "Parameters", "Send API Request", "Response Example",
    "Request Sample: Shell / cURL",
)


# ---- splitting into paragraphs ----------------------------------------------

def split_paragraphs(text: str) -> list[list[str]]:
    paras: list[list[str]] = []
    current: list[str] = []
    for line in text.splitlines():
        if line.strip() == "":
            if current:
                paras.append(current)
                current = []
        else:
            current.append(line)
    if current:
        paras.append(current)
    return paras


def join_paragraphs(paras: list[list[str]]) -> str:
    return "\n\n".join("\n".join(p) for p in paras)


# ---- transformations --------------------------------------------------------

def strip_sidebar(text: str) -> str:
    """Cut everything from the sidebar marker onward."""
    idx = text.find(SIDEBAR_MARKER)
    return text[:idx].rstrip() if idx != -1 else text


STATUS_EMBED_RE = re.compile(
    r"#\s*Status embed installed correctly.*?(?=^#\s|\Z)",
    re.DOTALL | re.MULTILINE,
)


def strip_status_embed(text: str) -> str:
    """Drop the leading 'Status embed installed correctly' block that appears
    at the top of every scraped page — it's Stoplight's status-banner embed,
    not real content."""
    return STATUS_EMBED_RE.sub("", text, count=1).lstrip()


def clean_heading_links(text: str) -> str:
    """## [Request](https://.../#Request) → ## Request"""
    out = []
    for line in text.splitlines():
        m = HEADING_LINK_RE.match(line)
        if m:
            hashes, label = m.group(1), m.group(2)
            out.append(f"{hashes} {label}")
        else:
            out.append(line)
    return "\n".join(out)


def merge_method_url(paras: list[list[str]]) -> list[list[str]]:
    """After the H1 title, the first two paragraphs are often a bare HTTP method
    and a URL. Merge them into one `**METHOD** `url`` paragraph."""
    if len(paras) < 3:
        return paras
    # paras[0] should be the H1 title line
    if not paras[0] or not paras[0][0].startswith("# "):
        return paras
    # paras[1]: single lowercase verb
    if len(paras[1]) != 1 or paras[1][0].strip().lower() not in METHODS:
        return paras
    # paras[2]: single URL starting with https://api.recruitcrm.io
    if len(paras[2]) != 1 or not paras[2][0].strip().startswith("https://api.recruitcrm.io"):
        return paras
    method = paras[1][0].strip().upper()
    url = paras[2][0].strip()
    # Strip base URL to show just the path for compactness
    path = url.replace("https://api.recruitcrm.io", "", 1)
    merged = [f"**{method}** `{path}`"]
    return [paras[0], merged] + paras[3:]


def drop_widget(paras: list[list[str]]) -> list[list[str]]:
    """Remove the Stoplight 'try it' widget: starts at 'Auth' (standalone),
    ends just before the first fenced code block after it — keep the cURL and
    response JSON, but drop the 'Request Sample: Shell / cURL' and 'Response
    Example' labels if we can identify them cleanly.

    Simpler heuristic used here: find standalone 'Auth' paragraph → delete it and
    subsequent short widget-label paragraphs (Token:, Parameters, subscription*:,
    Body, Send API Request, Prod, Request Sample: Shell / cURL, Response Example)
    until we hit a fenced code block. Keep the fenced code blocks themselves.
    """
    widget_labels = {
        "auth", "token:", "parameters", "body", "send api request",
        "prod", "mock", "request sample: shell / curl", "response example",
    }
    out = []
    i = 0
    in_widget = False
    while i < len(paras):
        para = paras[i]
        first_line = para[0].strip() if para else ""
        low = first_line.lower()

        if low == "auth":
            in_widget = True
            i += 1
            continue

        if in_widget:
            # Drop short label paragraphs
            if len(para) == 1 and (low in widget_labels or low.endswith("*:") or low.endswith(":")):
                i += 1
                continue
            # Drop lines that look like "subscription*:" or empty param placeholders
            if len(para) == 1 and re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*\*?:\s*$", first_line):
                i += 1
                continue
            # Keep fenced code blocks (their first line starts with ```)
            if first_line.startswith("```"):
                in_widget = False  # leaving widget
                out.append(para)
                i += 1
                continue
            # Keep paragraphs that aren't obviously widget chrome once we're past the labels
            # but skip generic "Prod"/"Mock" server toggle paragraphs
            if low in ("prod", "mock"):
                i += 1
                continue
            in_widget = False  # no known widget marker — exit widget mode
            out.append(para)
            i += 1
            continue

        out.append(para)
        i += 1
    return out


WIDGET_STRIP_EXACT = {
    "Send API Request",
    "Prod",
    "Mock",
    "Request Sample: Shell / cURL",
    "Response Example",
    "Auth",
    "Successful Operation",
}


def drop_widget_labels_global(paras: list[list[str]]) -> list[list[str]]:
    """Drop standalone widget-label paragraphs wherever they appear."""
    return [p for p in paras if not (len(p) == 1 and p[0].strip() in WIDGET_STRIP_EXACT)]


def strip_code_line_numbers(text: str) -> str:
    """Inside ```fenced``` blocks, strip lines that contain only a number
    (Stoplight renders its code viewer with gutter line numbers that get
    scraped as inline content). The scraper sometimes wraps them with trailing
    backslashes as line-continuation markdown escapes.
    """
    num_re = re.compile(r"^\\*\s*\d+\s*\\*$")
    out = []
    in_fence = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence and num_re.match(stripped):
            continue
        # Standalone backslash lines inside fences are line-continuation artifacts
        if in_fence and re.match(r"^\\+$", stripped):
            continue
        out.append(line)
    return "\n".join(out)


def strip_trailing_backslashes_in_fences(text: str) -> str:
    """Inside fences, strip the trailing `\\` markdown escape from each line.
    These are artifacts of the scraper escaping JSON-line boundaries.

    Exception: cURL blocks legitimately use `\\` for line continuation — leave
    those intact.
    """
    out = []
    in_fence = False
    is_curl_block = False
    block_first_content_seen = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            if not in_fence:
                # entering a new fence — reset detection state
                is_curl_block = False
                block_first_content_seen = False
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence and not block_first_content_seen and stripped:
            block_first_content_seen = True
            if stripped.startswith("curl "):
                is_curl_block = True
        if in_fence and not is_curl_block and line.endswith("\\"):
            out.append(line[:-1].rstrip())
            continue
        out.append(line)
    return "\n".join(out)


def label_code_blocks(text: str) -> str:
    """Add a small `#### Example <kind>` heading before each code block based
    on its content and position. cURL blocks get 'cURL'; JSON blocks before
    the cURL get 'request body'; JSON blocks after cURL get 'response'."""
    # Extract code blocks and their positions
    lines = text.splitlines()
    blocks: list[tuple[int, int, str]] = []  # (start, end, first_content_line)
    i = 0
    while i < len(lines):
        if lines[i].strip().startswith("```"):
            start = i
            j = i + 1
            first_content = ""
            while j < len(lines) and not lines[j].strip().startswith("```"):
                if lines[j].strip() and not first_content:
                    first_content = lines[j].strip()
                j += 1
            blocks.append((start, j, first_content))
            i = j + 1
            continue
        i += 1

    if not blocks:
        return text

    # Find cURL block index
    curl_idx = next((k for k, b in enumerate(blocks) if b[2].startswith("curl ")), None)

    labels: dict[int, str] = {}
    for k, (start, end, first) in enumerate(blocks):
        if first.startswith("curl "):
            labels[start] = "#### Example cURL"
        elif curl_idx is not None and k < curl_idx:
            labels[start] = "#### Example request body"
        elif curl_idx is not None and k > curl_idx:
            labels[start] = "#### Example response"
        else:
            # No cURL present (rare) — call it a response
            labels[start] = "#### Example response"

    # Stitch together with labels injected
    out = []
    for i, line in enumerate(lines):
        if i in labels:
            # Add a blank line separator before the label if needed
            if out and out[-1].strip() != "":
                out.append("")
            out.append(labels[i])
            out.append("")
        out.append(line)
    return "\n".join(out)


def collapse_blank_lines_in_fences(text: str) -> str:
    """Drop ALL blank lines inside fenced code blocks. The scraped pages
    interleave blank lines between each source line (artifact of Stoplight's
    line-by-line renderer)."""
    out = []
    in_fence = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence and stripped == "":
            continue
        out.append(line)
    return "\n".join(out)


def drop_duplicate_content_type(paras: list[list[str]]) -> list[list[str]]:
    """`application/json` often appears twice in a row — keep one."""
    out = []
    prev_was_ct = False
    for p in paras:
        if len(p) == 1 and p[0].strip() == "application/json":
            if prev_was_ct:
                continue
            prev_was_ct = True
        else:
            prev_was_ct = False
        out.append(p)
    return out


# ---- parameter-block collapsing ---------------------------------------------

PARAM_SECTION_HEADERS = {
    "### path parameters", "### query parameters", "### body",
    "### response body", "### headers",
}


def is_param_name(line: str) -> bool:
    """Is this line plausibly a parameter identifier?"""
    s = line.strip()
    # allow backslash-escaped underscores (markdown)
    s_clean = s.replace("\\_", "_")
    return bool(re.match(r"^[a-zA-Z_][a-zA-Z0-9_\.\[\]]*$", s_clean)) and len(s_clean) <= 60


def is_heading(line: str) -> bool:
    return line.lstrip().startswith("#")


def collapse_param_block(paras: list[list[str]], start_idx: int) -> tuple[list[list[str]], int]:
    """Starting from paras[start_idx] (a param section header), walk forward and
    collapse the subsequent param-data paragraphs into a single bullet-list
    paragraph. Return (new_paragraphs_for_this_section, end_idx).

    A parameter sequence looks like:
        [name]
        [type]
        [required]?                      # literal word "required"
        [description line(s)]*
        [Example:]   [value]             # optional
        [Allowed values:]   [value]      # optional
        [Default:]   [value]             # optional

    The section ends when we hit another heading (# / ## / ###) or a fenced
    code block.
    """
    if start_idx >= len(paras):
        return [], start_idx

    header = paras[start_idx]
    out_lines: list[str] = []
    preamble: list[list[str]] = []
    i = start_idx + 1
    current_param: dict | None = None

    # Skip preamble (non-param lines like "application/json" or schema titles)
    # until we find the first param name.
    while i < len(paras):
        p = paras[i]
        first = p[0].strip() if p else ""
        if is_heading(first) or first.startswith("```"):
            # No params in this section at all
            return [header] + preamble, i
        if len(p) == 1 and re.match(r"^\d{3}$", first):
            return [header] + preamble, i
        if first.lower() in {"auth", "successful operation"}:
            return [header] + preamble, i
        if len(p) == 1 and is_param_name(first):
            break
        # Drop obvious preamble chrome
        if first in ("application/json", "multipart/form-data"):
            i += 1
            continue
        preamble.append(p)
        i += 1

    def flush():
        nonlocal current_param
        if current_param is None:
            return
        name = current_param["name"]
        type_ = current_param.get("type") or ""
        req = current_param.get("required", False)
        desc = " ".join(current_param.get("desc", [])).strip()
        extras = []
        for key in ("example", "allowed", "default"):
            val = current_param.get(key)
            if val:
                label = {"example": "example", "allowed": "allowed", "default": "default"}[key]
                extras.append(f"{label}: `{val}`")
        meta_parts = []
        if type_:
            meta_parts.append(type_)
        meta_parts.append("**required**" if req else "optional")
        meta = ", ".join(meta_parts)
        line = f"- `{name}` ({meta})"
        if desc:
            line += f" — {desc}"
        if extras:
            line += f" ({'; '.join(extras)})"
        out_lines.append(line)
        current_param = None

    while i < len(paras):
        p = paras[i]
        first = p[0].strip() if p else ""

        # Stop at next heading, fenced code block, or a known widget label
        if is_heading(first) or first.startswith("```"):
            break
        if first.lower() in {"auth", "successful operation"}:
            break

        # Status codes (200/401/404/422) as their own paragraph — leave them
        if len(p) == 1 and re.match(r"^\d{3}$", first):
            break

        # Literal "required" modifier
        if len(p) == 1 and first.lower() == "required":
            if current_param is not None:
                current_param["required"] = True
            i += 1
            continue

        # Example / Allowed values / Default — label-then-value pattern (two consecutive paragraphs)
        if len(p) == 1 and first in ("Example:", "Allowed values:", "Default:"):
            key = {"Example:": "example", "Allowed values:": "allowed", "Default:": "default"}[first]
            # Next paragraph is the value
            if i + 1 < len(paras) and paras[i + 1]:
                val = " ".join(paras[i + 1]).strip()
                if current_param is not None:
                    current_param[key] = val
                i += 2
                continue
            i += 1
            continue

        # Param name starter
        if len(p) == 1 and is_param_name(first):
            # New parameter — flush previous
            flush()
            current_param = {"name": first.replace("\\_", "_"), "desc": []}
            i += 1
            # Next paragraph should be the type
            if i < len(paras) and len(paras[i]) == 1:
                t_low = paras[i][0].strip().lower()
                if t_low in PARAM_TYPES:
                    current_param["type"] = paras[i][0].strip()
                    i += 1
            continue

        # Description line — append to current param
        if current_param is not None:
            current_param["desc"].append(" ".join(p).strip())
            i += 1
            continue

        # Otherwise, stop the param block (unrecognized content)
        break

    flush()

    # Build output paragraphs:
    new_paras = [header] + preamble
    if out_lines:
        new_paras.append(out_lines)
    return new_paras, i


def collapse_all_param_sections(paras: list[list[str]]) -> list[list[str]]:
    out = []
    i = 0
    while i < len(paras):
        p = paras[i]
        first_low = p[0].strip().lower() if p else ""
        if first_low in PARAM_SECTION_HEADERS:
            new_paras, next_i = collapse_param_block(paras, i)
            out.extend(new_paras)
            i = next_i
            continue
        out.append(p)
        i += 1
    return out


# ---- orchestration ----------------------------------------------------------

def tidy(text: str) -> str:
    # Preserve the <!-- source --> and <!-- title --> comments at the top
    lines = text.splitlines()
    header_lines: list[str] = []
    body_start = 0
    for i, line in enumerate(lines):
        if line.startswith("<!--"):
            header_lines.append(line)
            body_start = i + 1
        elif line.strip() == "":
            header_lines.append(line)
            body_start = i + 1
        else:
            break
    body = "\n".join(lines[body_start:])

    body = strip_sidebar(body)
    body = strip_status_embed(body)
    body = clean_heading_links(body)
    body = strip_code_line_numbers(body)
    body = strip_trailing_backslashes_in_fences(body)
    body = collapse_blank_lines_in_fences(body)
    body = label_code_blocks(body)

    paras = split_paragraphs(body)
    paras = merge_method_url(paras)
    paras = drop_widget(paras)
    paras = drop_widget_labels_global(paras)
    paras = drop_duplicate_content_type(paras)
    paras = collapse_all_param_sections(paras)

    result_body = join_paragraphs(paras).rstrip() + "\n"
    return "\n".join(header_lines).rstrip() + "\n\n" + result_body


def main() -> int:
    files = sorted(DOCS_DIR.glob("*.md"))
    if len(sys.argv) > 1:
        files = [DOCS_DIR / name for name in sys.argv[1:]]
    for f in files:
        original = f.read_text()
        tidied = tidy(original)
        if tidied != original:
            f.write_text(tidied)
            print(f"tidied {f.name} ({len(original):5d} → {len(tidied):5d})")
        else:
            print(f"  same {f.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
