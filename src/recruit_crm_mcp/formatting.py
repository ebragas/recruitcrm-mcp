"""Markdown ↔ HTML conversion at the MCP boundary.

The Recruit CRM web UI stores and renders rich-text fields (note `description`)
as HTML. The LLM speaks Markdown. We convert at the boundary so the model
never has to know HTML exists.

Both helpers pass through ``None`` and empty strings unchanged.
"""
from __future__ import annotations

from bs4 import BeautifulSoup
from markdown_it import MarkdownIt
from markdownify import markdownify

# Elements whose entire subtree should be discarded before MD conversion.
# markdownify's `strip=` only removes the outer tag, not its contents — so
# `<script>alert(1)</script>` would leak `alert(1)` as visible text.
_DROP_ELEMENTS = ("script", "style", "o:p")

# Default CommonMark config — handles paragraphs, lists, bold/italic, links,
# images, and inline code without any extra extensions. HTML in Markdown is
# allowed through (so a caller who sends raw HTML still gets HTML out).
_md = MarkdownIt("commonmark")


def md_to_html(text: str | None) -> str | None:
    """Convert Markdown to HTML for POST to the Recruit CRM API.

    The CRM web editor renders the stored string as HTML, so the model's
    Markdown must be HTML before it goes over the wire — otherwise `**bold**`
    shows up as literal asterisks and bullet lists collapse.
    """
    if not text:
        return text
    return _md.render(text).strip()


def html_to_md(html: str | None) -> str | None:
    """Convert HTML returned by the Recruit CRM API to Markdown.

    Strips MS Office paste artifacts (``<o:p>``, ``mso-*`` styles), scripts,
    and styles. Whitespace is collapsed and trimmed.
    """
    if not html:
        return html
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all(_DROP_ELEMENTS):
        tag.decompose()
    return markdownify(
        str(soup),
        heading_style="ATX",
        bullets="-",
    ).strip()
