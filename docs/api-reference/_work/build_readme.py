#!/usr/bin/env python3
"""Build docs/api-reference/README.md — an index of all scraped endpoint pages
grouped by resource, with HTTP method + path extracted from each file's
tidied body.
"""
import os
import re

DOC_DIR = "/Users/eric/dev/magicandco/recruitcrm-mcp/docs/api-reference"

# Resource group in sidebar order (from the Recruit CRM docs TOC)
GROUPS: list[tuple[str, list[str]]] = [
    ("Intro", [
        "recruit-crm-api",
        "getting-started",
        "authentication",
        "rate-limiting",
        "custom-field-search",
    ]),
    ("Candidates", [
        "show-all-candidates", "creates-a-new-candidate", "find-candidate-by-slug",
        "edit-a-candidate", "delete-a-candidate", "search-for-candidates",
        "resume-parser",
        "assign-candidate", "un-assign-candidate", "apply-to-job",
        "update-candidate-visibility-in-a-job",
        "mark-candidate-as-off-limit", "mark-candidate-as-available",
        "get-list-of-candidates-which-are-marked-as-off-limit",
        "off-limit-history-for-candidate",
        "hiring-stages-of-candidate", "hiring-stage-of-candidate-for-job",
        "update-candidate-hiring-stage", "candidate-history",
        "request-updated-profile", "get-profile-update-request-form",
        "add-work-experience", "edit-work-experience", "delete-a-candidate-work-experience",
        "candidate-work-experience",
        "add-education-history", "edit-education-history",
        "delete-a-candidate-education-history", "candidate-education-history",
        "question-and-answers-of-candidate",
        "update-candidate-answers-for-the-questions",
        "question-and-answers-of-candidate-for-job",
        "update-candidate-answers-for-the-questions-for-a-job",
        "get-job-associated-fields", "update-job-associated-fields",
        "pitch-candidate-to-contact", "pitch-history-of-a-candidate",
        "pitch-history-of-a-contact", "pitch-history-of-a-candidate-and-contact",
        "update-pitch-stage", "get-contacts-where-the-candidate-is-pitched",
    ]),
    ("Contacts", [
        "show-all-contacts", "creates-a-new-contact", "find-contact-by-slug",
        "edit-a-contact", "delete-a-contact", "search-for-contacts",
        "mark-contacts-as-off-limit", "mark-contacts-as-available",
        "get-list-of-contacts-which-are-marked-as-off-limit",
        "off-limit-history-for-contact",
    ]),
    ("Companies", [
        "show-all-companies", "creates-a-new-company", "find-company-by-slug",
        "edit-a-company", "delete-a-company", "search-for-companies",
        "mark-companies-as-off-limit", "mark-companies-as-available",
        "get-list-of-companies-which-are-marked-as-off-limit",
        "off-limit-history-for-company",
    ]),
    ("Jobs", [
        "show-all-jobs", "creates-a-new-job", "find-job-by-slug", "edit-a-job",
        "delete-a-job", "search-for-jobs",
        "assigned-candidates-for-job", "stage-history-of-candidate-for-job",
        "get-job-application-form", "get-job-application-form-metadata",
        "get-xml-job-boards-list", "get-compliance-terms",
    ]),
    ("Deals", [
        "show-all-deals", "creates-a-new-deal", "find-deal-by-slug",
        "edit-a-deal", "delete-a-deal", "search-for-deals",
    ]),
    ("Tasks", [
        "show-all-tasks", "creates-a-new-task", "find-task-by-id",
        "edit-task", "delete-a-task", "search-for-tasks",
    ]),
    ("Meetings", [
        "show-all-meetings", "creates-a-new-meeting", "find-meeting-by-id",
        "edit-meeting", "delete-a-meeting", "search-for-meetings",
    ]),
    ("Notes", [
        "show-all-notes", "creates-a-new-note", "find-note-by-id",
        "edit-a-note", "delete-a-note", "search-for-notes",
    ]),
    ("Call Logs", [
        "show-all-call-logs", "creates-a-new-call-log", "find-call-log-by-id",
        "edit-a-call-log", "delete-a-call-log", "search-for-call-logs",
        "get-call-recording-upload-status", "upload-call-recordings",
    ]),
    ("Hotlists", [
        "show-all-hotlists", "creates-a-new-hotlist", "find-hotlist-by-id",
        "edit-a-hotlist", "delete-a-hotlist",
        "add-records-to-hotlist", "remove-records-from-hotlist",
        "search-for-hotlists",
    ]),
    ("Custom Fields", [
        "show-all-custom-fields", "show-all-candidate-custom-fields",
        "show-all-contact-custom-fields", "show-all-company-custom-fields",
        "show-all-job-custom-fields", "show-all-deal-custom-fields",
        "show-all-job-associated-custom-fields",
        "show-all-placement-associated-custom-fields",
        "show-all-invoice-custom-fields",
    ]),
    ("Webhook Subscriptions", [
        "show-all-subscriptions", "creates-a-new-subscription",
        "find-subscription-by-id", "edit-a-subscription", "delete-a-subscription",
    ]),
    ("Sequences", [
        "enroll-candidate", "unenroll-candidate",
        "enroll-contact", "unenroll-contact",
        "get-all-enrollment-statuses",
        "search-for-enrollments", "search-for-sequences",
    ]),
    ("Timesheets", [
        "get-all-timesheets", "get-timesheet-details",
    ]),
    ("Placements", [
        "show-all-placements", "find-placement-by-id", "edit-a-placement",
        "delete-a-placement", "search-placements",
    ]),
    ("Invoices", [
        "show-all-invoices", "creates-a-new-invoice", "find-invoice-by-id",
        "edit-an-invoice", "delete-an-invoice", "search-for-invoices",
    ]),
    ("Nested Custom Fields", [
        "show-field-dependencies-for-all-entities",
    ]),
    ("Lists", [
        "get-qualifications", "get-currencies", "get-salary-types",
        "get-industries", "get-languages", "get-proficiencies",
        "get-call-types", "get-note-types", "get-meeting-types",
        "get-task-types",
        "get-contact-stages", "get-deals-stages", "get-job-stages",
        "get-candidate-stages",
        "get-multiple-hiring-pipelines", "get-hiring-pipeline-stages-for-a-pipeline",
        "get-candidate-questions", "get-collaborators",
        "get-all-users", "get-all-teams", "get-target-report",
        "get-pitch-stages", "get-invoice-status", "get-invoice-templates",
    ]),
    ("List Off Limit Status", [
        "get-off-limit-status",
    ]),
    ("Users", [
        "search-for-users",
    ]),
    ("Files", [
        "upload-new-files", "get-all-files",
    ]),
    ("Email", [
        "opted-out-entities", "update-opted-out-status",
        "create-email-draft", "draft-email-status",
        "send-an-email", "sent-email-status",
    ]),
]


METHOD_PATH_RE = re.compile(r"^\*\*(GET|POST|PUT|PATCH|DELETE)\*\*\s+`([^`]+)`", re.MULTILINE)
TITLE_RE = re.compile(r"^#\s+(.+?)$", re.MULTILINE)


def extract_title_and_endpoint(path: str) -> tuple[str, str | None, str | None]:
    with open(path) as f:
        content = f.read()
    # Skip HTML comments
    body = re.sub(r"^<!--.*?-->\n", "", content, flags=re.MULTILINE)
    title_m = TITLE_RE.search(body)
    title = title_m.group(1).strip() if title_m else path
    ep_m = METHOD_PATH_RE.search(body)
    if ep_m:
        return title, ep_m.group(1), ep_m.group(2)
    return title, None, None


def main() -> None:
    files_in_groups = set()
    lines = [
        "# Recruit CRM API Reference",
        "",
        "Locally cached copy of the Recruit CRM API documentation.",
        "Source: https://docs.recruitcrm.io/docs/rcrm-api-reference/9033e3227d21f-recruit-crm-api",
        "",
        "- **Base URL:** `https://api.recruitcrm.io`",
        "- **Auth:** `Authorization: Bearer <RECRUIT_CRM_API_KEY>`",
        "",
        "Each page below is a tidied markdown copy of the original Stoplight doc.",
        "",
        "## Contents",
        "",
    ]
    for group, slugs in GROUPS:
        anchor = group.lower().replace(" ", "-")
        lines.append(f"- [{group}](#{anchor})")
    lines.append("")

    for group, slugs in GROUPS:
        lines.append(f"## {group}")
        lines.append("")
        if group == "Intro":
            for slug in slugs:
                path = os.path.join(DOC_DIR, f"{slug}.md")
                if not os.path.exists(path):
                    continue
                files_in_groups.add(slug + ".md")
                title, _, _ = extract_title_and_endpoint(path)
                lines.append(f"- [{title}]({slug}.md)")
            lines.append("")
            continue
        # Regular group — produce a table
        lines.append("| Method | Path | Doc |")
        lines.append("|---|---|---|")
        for slug in slugs:
            path = os.path.join(DOC_DIR, f"{slug}.md")
            if not os.path.exists(path):
                lines.append(f"|  |  | _(missing: {slug})_ |")
                continue
            files_in_groups.add(slug + ".md")
            title, method, ep_path = extract_title_and_endpoint(path)
            m = method or ""
            p = f"`{ep_path}`" if ep_path else ""
            lines.append(f"| {m} | {p} | [{title}]({slug}.md) |")
        lines.append("")

    # List any endpoint files not covered by the group index
    all_md = {f for f in os.listdir(DOC_DIR) if f.endswith(".md") and f != "README.md"}
    unassigned = sorted(all_md - files_in_groups)
    if unassigned:
        lines.append("## Uncategorized")
        lines.append("")
        lines.append("These docs were scraped but not placed in a group above:")
        lines.append("")
        for f in unassigned:
            slug = f[:-3]
            path = os.path.join(DOC_DIR, f)
            title, method, ep_path = extract_title_and_endpoint(path)
            lines.append(f"- [{title}]({f})" + (f" — **{method}** `{ep_path}`" if method else ""))
        lines.append("")

    out = "\n".join(lines).rstrip() + "\n"
    with open(os.path.join(DOC_DIR, "README.md"), "w") as f:
        f.write(out)
    print(f"Wrote README.md ({len(out)} bytes, {len(all_md)} endpoint pages indexed, {len(unassigned)} uncategorized)")


if __name__ == "__main__":
    main()
