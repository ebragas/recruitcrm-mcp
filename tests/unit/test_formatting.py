"""Tests for the Markdown ↔ HTML formatting helpers."""

import pytest

from recruit_crm_mcp.formatting import html_to_md, md_to_html


class TestMdToHtml:
    def test_paragraphs(self):
        assert md_to_html("First.\n\nSecond.") == "<p>First.</p>\n<p>Second.</p>"

    def test_bold_italic(self):
        assert md_to_html("**bold** and *italic*") == "<p><strong>bold</strong> and <em>italic</em></p>"

    def test_bullet_list(self):
        out = md_to_html("- one\n- two\n- three")
        assert "<ul>" in out and "<li>one</li>" in out and "<li>three</li>" in out

    def test_link(self):
        assert md_to_html("[X](https://x.example)") == '<p><a href="https://x.example">X</a></p>'

    def test_escapes_raw_html(self):
        # Raw HTML in caller input must NOT pass through verbatim — it could
        # carry <script>, inline event handlers, or other unsafe markup that
        # would be POSTed to the CRM as-is.
        out = md_to_html("<p>not html</p>")
        assert out == "<p>&lt;p&gt;not html&lt;/p&gt;</p>"

    def test_escapes_script_tag(self):
        out = md_to_html("<script>alert(1)</script>")
        assert "<script>" not in out
        assert "&lt;script&gt;" in out

    @pytest.mark.parametrize("value", [None, ""])
    def test_passthrough_empty(self, value):
        assert md_to_html(value) == value


class TestHtmlToMd:
    def test_paragraphs(self):
        assert html_to_md("<p>First.</p><p>Second.</p>") == "First.\n\nSecond."

    def test_bold_italic(self):
        assert html_to_md("<strong>bold</strong> and <em>italic</em>") == "**bold** and *italic*"

    def test_bullet_list(self):
        out = html_to_md("<ul><li>one</li><li>two</li></ul>")
        assert "- one" in out and "- two" in out

    def test_link(self):
        assert html_to_md('<a href="https://x.example">X</a>') == "[X](https://x.example)"

    def test_strips_script_content(self):
        # markdownify alone leaves script/style text content; we pre-strip
        # the elements entirely with bs4.
        assert html_to_md("<p>hi</p><script>alert(1)</script>") == "hi"

    def test_strips_style_content(self):
        assert html_to_md("<p>hi</p><style>.x{color:red}</style>") == "hi"

    def test_strips_office_paste_artifacts(self):
        html = '<p class=MsoNormal style="mso-margin-top:0">Hi <o:p>nope</o:p></p>'
        assert html_to_md(html) == "Hi"

    @pytest.mark.parametrize("value", [None, ""])
    def test_passthrough_empty(self, value):
        assert html_to_md(value) == value


class TestRoundTrip:
    def test_md_to_html_to_md_preserves_structure(self):
        original = (
            "Met with **Jane**.\n\n"
            "- one\n"
            "- two\n\n"
            "See [link](https://x.example)."
        )
        assert html_to_md(md_to_html(original)) == original
