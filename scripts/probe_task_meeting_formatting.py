"""Probe whether the `description` field on tasks and meetings is HTML-rendered
in the Recruit CRM web UI (the same way notes are).

Creates a fresh MCP-Test candidate, then for both tasks and meetings posts the
same body in three formats labeled `[FORMAT: ...]`. View the resulting task
and meeting in the Recruit CRM UI to determine if HTML renders cleanly.

Cleanup: leaves the entities in place. Run `make integration-sweep` after.
"""
import asyncio
import os
import uuid

from recruit_crm_mcp import client

PLAIN = """[FORMAT: PLAIN-TEXT]

Met with Jane today.

Key points:
- Strong React skills
- Open to remote
- Salary expectation: $150k

Next step: schedule technical screen."""

MARKDOWN = """**[FORMAT: MARKDOWN]**

Met with **Jane** today.

Key points:
- Strong React skills
- Open to remote
- Salary expectation: $150k

Next step: schedule technical screen.
Link: [LinkedIn](https://www.linkedin.com/in/jane)"""

HTML = """<p><strong>[FORMAT: HTML]</strong></p>
<p>Met with <strong>Jane</strong> today.</p>
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
    label = f"MCP-Test-FormatProbe-TM-{uuid.uuid4().hex[:8]}"
    try:
        cand = await client.post("/candidates", {
            "first_name": label,
            "last_name": "Probe",
            "email": f"{label.lower()}@example.invalid",
        })
        slug = cand["slug"]
        print(f"\nCandidate: {label}")
        print(f"  slug: {slug}")
        print(f"  UI:   https://app.recruitcrm.io/candidate/{slug}\n")

        # Tasks — one per format, all anchored on the candidate
        print("=== TASKS ===")
        for fmt, body in (("PLAIN", PLAIN), ("MARKDOWN", MARKDOWN), ("HTML", HTML)):
            task = await client.create_task({
                "title": f"{label} task ({fmt})",
                "start_date": "2026-05-15T18:00:00Z",
                "reminder": -1,
                "description": body,
                "related_to": slug,
                "related_to_type": "candidate",
            })
            tid = task.get("id")
            print(f"  task {fmt} id={tid}")

        # Meetings — one per format, attendee = candidate
        print("\n=== MEETINGS ===")
        for fmt, body in (("PLAIN", PLAIN), ("MARKDOWN", MARKDOWN), ("HTML", HTML)):
            meeting = await client.create_meeting({
                "title": f"{label} meeting ({fmt})",
                "start_date": "2026-05-15T18:00:00Z",
                "end_date": "2026-05-15T18:30:00Z",
                "reminder": -1,
                "description": body,
                "related_to": slug,
                "related_to_type": "candidate",
                "attendee_candidates": slug,
                "do_not_send_calendar_invites": "1",
            })
            mid = meeting.get("id")
            print(f"  meeting {fmt} id={mid}")

        print(f"\nView the candidate's Tasks tab and Meetings tab at:")
        print(f"  https://app.recruitcrm.io/candidate/{slug}")
        print("\nFor each entity, observe how the body renders. Then report which")
        print("(if any) of the three formats renders cleanly with bullets/bold/links.")
        print("\nCleanup: `make integration-sweep` after verification.")
    finally:
        await client.aclose_client()


if __name__ == "__main__":
    asyncio.run(main())
