"""One-off probe: post the same note body in three formats — plain text,
Markdown, and HTML — to a freshly-created MCP-Test candidate, then print
the IDs and URLs so a human can view them in the Recruit CRM web UI.

Run: uv run python scripts/probe_note_formatting.py

Cleanup: leaves the test candidate + notes in place for visual inspection.
Run `make integration-sweep` after to remove all `MCP-Test-*` orphans.
"""
import asyncio
import os
import uuid

from recruit_crm_mcp import client

PLAIN = """Met with Jane today about the Senior Engineer role.

Key points:
- Strong React skills
- Open to remote
- Salary expectation: $150k

Next step: schedule technical screen."""

MARKDOWN = """Met with **Jane** today about the *Senior Engineer* role.

Key points:
- Strong React skills
- Open to remote
- Salary expectation: $150k

Next step: schedule technical screen.
Link: [LinkedIn](https://www.linkedin.com/in/jane)"""

HTML = """<p>Met with <strong>Jane</strong> today about the <em>Senior Engineer</em> role.</p>
<p>Key points:</p>
<ul>
  <li>Strong React skills</li>
  <li>Open to remote</li>
  <li>Salary expectation: $150k</li>
</ul>
<p>Next step: schedule technical screen.<br>
Link: <a href="https://www.linkedin.com/in/jane">LinkedIn</a></p>"""


async def main() -> None:
    if not os.environ.get("RECRUIT_CRM_API_KEY"):
        raise SystemExit("RECRUIT_CRM_API_KEY not set")

    client.init_client()
    candidate_label = f"MCP-Test-FormatProbe-{uuid.uuid4().hex[:8]}"
    try:
        cand = await client.post("/candidates", {
            "first_name": candidate_label,
            "last_name": "Probe",
            "email": f"{candidate_label.lower()}@example.invalid",
        })
        slug = cand["slug"]
        print(f"\nCandidate created: {candidate_label}")
        print(f"  slug: {slug}")
        print(f"  UI:   https://app.recruitcrm.io/candidate/{slug}\n")

        for label, body in (("plain", PLAIN), ("markdown", MARKDOWN), ("html", HTML)):
            note = await client.create_note({
                "description": body,
                "related_to": slug,
                "related_to_type": "candidate",
            })
            note_id = note.get("id")
            print(f"--- note {label} (id={note_id}) ---")
            print(f"posted   ({len(body)} chars): {body[:80]!r}{'...' if len(body) > 80 else ''}")
            fetched = await client.get_note(note_id)
            stored = fetched.get("description", "")
            print(f"stored   ({len(stored)} chars): {stored[:200]!r}{'...' if len(stored) > 200 else ''}")
            verbatim = stored == body
            print(f"verbatim: {verbatim}")
            print()

        print("Open the candidate URL above in /chrome to see how each note renders.")
        print("Cleanup: `make integration-sweep` will remove all MCP-Test-* orphans.")
    finally:
        await client.aclose_client()


if __name__ == "__main__":
    asyncio.run(main())
