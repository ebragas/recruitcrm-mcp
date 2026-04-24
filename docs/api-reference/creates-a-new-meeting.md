<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/ca9713d31352a-creates-a-new-meeting -->
<!-- title: Creates a new meeting | API Endpoints -->

# Creates a new meeting

**POST** `/v1/meetings`

Creates a new meeting.

## Request

Security: Bearer Auth

### Body

Meeting Object

- `title` (string, **required**) — Title of Meeting (example: `Follow up call`)
- `meeting_type_id` (integer, optional) — Meeting Type Id (example: `1`)
- `description` (string, optional) — Meeting Description (example: `Make follow up call for interview`)
- `address` (string, optional) — Address of meeting (example: `Video call (https://examplelink)`)
- `reminder` (integer, **required**) — Reminder ID of the Meeting. _IDs 'Mapping: -1 => No Reminder, 0 => 0 Min Before, 15 => 15 Min Before, 30 => 30 Min Before, 60 => 1 Hour Before, 120 => 2 Hours Before, 1440 => 1 Day Before_ (example: `30`)
- `start_date` (string, **required**) — Start Date and time of Meeting (example: `2020-06-29T05:36:22.000000Z`)
- `end_date` (string, **required**) — End Date and time of Meeting (example: `2020-06-29T06:36:22.000000Z`)
- `related_to` (string, optional) — Associated entity's slug (example: `23123`)
- `related_to_type` (string, optional) — Associated entity's Name i.e. candidate/ company/ contact/ job /deal (example: `candidate`)
- `attendee_contacts` (string, optional) — Comma-Separated Slugs of Contacts attending the meeting (example: `21345,33123`)
- `attendee_candidates` (string, optional) — Comma-Separated Slugs of Candidates attending the meeting (example: `2543,65478`)
- `attendee_users` (string, optional) — Comma-Separated IDs of Users attending the meeting (example: `29998,23453`)
- `owner_id` (integer, optional)
- `created_by` (integer, optional)
- `updated_by` (integer, optional)
- `associated_candidates` (string, optional) — Comma separated candidate slugs (example: `275,16318617835190000051Ond`)
- `associated_companies` (string, optional) — Comma separated company slugs (example: `275,16318617835190000051Ond`)
- `associated_contacts` (string, optional) — Comma separated contact slugs (example: `275,16318617835190000051Ond`)
- `associated_jobs` (string, optional) — Comma separated job slugs (example: `275,16318617835190000051Ond`)
- `associated_deals` (string, optional) — Comma separated deal slugs (example: `275,16318617835190000051Ond`)
- `do_not_send_calendar_invites` (boolean, optional) — Providing '1' as value => Do not send calendar invites to attendees and related\_to entity, Providing '0' as value => Send calendar invites to attendees and related\_to entity.(BETA) (example: `1`)
- `collaborator_user_ids` (string, optional) — Comma separated user IDs (BETA/Tagging) (example: `11496,11497`)
- `collaborator_team_ids` (string, optional) — Comma separated team IDs (BETA/Tagging) (example: `16,17`)
- `enable_auto_populate_teams` (boolean, optional) — Providing '1' as value will include all teams of the user provided in owner\_id, if added; otherwise, it will include teams of the account owner, unless explicitly provided in collaborator\_team\_ids.(BETA/Tagging) (example: `1`)

## Responses

200

401

429

### Body

- `id` (integer, optional) — Meeting ID (example: `2`)
- `title` (string, optional) — Title of Meeting (example: `Follow up call`)
- `meeting_type` (optional) — array\[object\] Meeting Type (example: `\[{"id":1,"label":"Client Meeting"}\]`)
- `id` (integer, optional) — Meeting Type ID (example: `1`)
- `label` (string, optional) — Meeting Type Label (example: `Client Meeting`)
- `description` (string, optional) — Meeting Description (example: `Make follow up call for interview`)
- `address` (string, optional) — Address of meeting (example: `Video call (https://examplelink)`)
- `reminder` (integer, optional) — Reminder ID of the Meeting. _IDs 'Mapping: -1 => No Reminder, 0 => 0 Min Before, 15 => 15 Min Before, 30 => 30 Min Before, 60 => 1 Hour Before, 120 => 2 Hours Before, 1440 => 1 Day Before_ (example: `30`)
- `start_date` (string, optional) — Start Date and time of Meeting (example: `2020-06-29T05:36:22.000000Z`)
- `end_date` (string, optional) — End Date and time of Meeting (example: `2020-06-29T06:36:22.000000Z`)
- `related_to` (string, optional) — Associated entity's slug (example: `23123`)
- `related_to_type` (string, optional) — Associated entity's Name i.e. candidate/ company/ contact/ job /deal (example: `candidate`)
- `attendees` (optional) — array\[object\] Array of attendees
- `attendee_type` (string, optional) — Type of Attendee i.e. candidate/ contact/ user (example: `candidate`)
- `attendee_id` (string, optional) — Attendee Slug (example: `12654`)
- `display_name` (string, optional) — Attendee Name (example: `Michael Scott`)
- `attendee` (optional) — array\[object\] Array of attendee details
- `associated_candidates` (optional) — array\[string\] Array of Associated Candidates
- `associated_contacts` (optional) — array\[string\] Array of Associated Contacts
- `associated_companies` (optional) — array\[string\] Array of Associated Companies
- `associated_jobs` (optional) — array\[string\] Array of Associated Jobs
- `associated_deals` (optional) — array\[string\] Array of Associated Deals
- `do_not_send_calendar_invites` (boolean, optional) — Response '1' as value => Do not send calendar invites to attendees and related\_to entity, Response '0' as value => Send calendar invites to attendees and related\_to entity.(BETA) (example: `1`)
- `status` (string, optional) — Status Of Meeting
- `reminder_date` (string, optional) — Reminder Date and Time Of Meeting (example: `2022-12-02T16:30:00.000000Z`)
- `all_day` (integer, optional)
- `related` (object, optional) — Details Of Related Entity
- `owner` (string, optional)
- `Owner` (optional) (example: `10023`)
- `created_on` (string, optional) — Created On (example: `2022-12-02T16:59:24.000000Z`)
- `updated_on` (string, optional) — Updated On (example: `2022-12-02T16:59:24.000000Z`)
- `created_by` (string, optional) — Created By (example: `10002`)
- `updated_by` (string, optional) — Updated By (example: `10002`)
- `collaborator_users` (optional) — array\[object\] Array of user collaborators (BETA/Tagging)
- `id` (integer, optional) — User ID (example: `34`)
- `first_name` (string, optional) — User's First Name (example: `Jane`)
- `last_name` (string, optional) — User's Last Name (example: `Scott`)
- `email` (string, optional) — User's Email (example: `jane.scott@gmail.com`)
- `contact_number` (string, optional) — User's contact\_number
- `avatar` (string, optional) — User's avatar link
- `collaborator_teams` (optional) — array\[object\] Array of team collaborators (BETA/Tagging)
- `team_id` (integer, optional) — Team ID (example: `16`)
- `team_name` (string, optional) — Team Name (example: `team1`)

#### Example request body

#### Example request body

```
{
  "title": "Follow up call",
  "meeting_type_id": 1,
  "description": "Make follow up call for interview",
  "address": "Video call (https://examplelink)",
  "reminder": 30,
  "start_date": "2020-06-29T05:36:22.000000Z",
  "end_date": "2020-06-29T06:36:22.000000Z",
  "related_to": "23123",
  "related_to_type": "candidate",
  "attendee_contacts": "21345,33123",
  "attendee_candidates": "2543,65478",
  "attendee_users": "29998,23453",
  "owner_id": 0,
  "created_by": 0,
  "updated_by": 0,
  "associated_candidates": "275,16318617835190000051Ond",
  "associated_companies": "275,16318617835190000051Ond",
  "associated_contacts": "275,16318617835190000051Ond",
  "associated_jobs": "275,16318617835190000051Ond",
  "associated_deals": "275,16318617835190000051Ond",
  "do_not_send_calendar_invites": "1",
  "collaborator_user_ids": "11496,11497",
  "collaborator_team_ids": "16,17",
  "enable_auto_populate_teams": "1"
}
```

#### Example cURL

#### Example cURL

```
curl --request POST \
  --url https://api.recruitcrm.io/v1/meetings \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json' \
  --data '{
  "title": "Follow up call",
  "meeting_type_id": 1,
  "description": "Make follow up call for interview",
  "address": "Video call (https://examplelink)",
  "reminder": 30,
  "start_date": "2020-06-29T05:36:22.000000Z",
  "end_date": "2020-06-29T06:36:22.000000Z",
  "related_to": "23123",
  "related_to_type": "candidate",
  "attendee_contacts": "21345,33123",
  "attendee_candidates": "2543,65478",
  "attendee_users": "29998,23453",
  "owner_id": 0,
  "created_by": 0,
  "updated_by": 0,
  "associated_candidates": "275,16318617835190000051Ond",
  "associated_companies": "275,16318617835190000051Ond",
  "associated_contacts": "275,16318617835190000051Ond",
  "associated_jobs": "275,16318617835190000051Ond",
  "associated_deals": "275,16318617835190000051Ond",
  "do_not_send_calendar_invites": "1",
  "collaborator_user_ids": "11496,11497",
  "collaborator_team_ids": "16,17",
  "enable_auto_populate_teams": "1"
}'
```

#### Example response

#### Example response

```
{
  "id": 2,
  "title": "Follow up call",
  "meeting_type": [
    {
      "id": 1,
      "label": "Client Meeting"
    }
  ],
  "description": "Make follow up call for interview",
  "address": "Video call (https://examplelink)",
  "reminder": 30,
  "start_date": "2020-06-29T05:36:22.000000Z",
  "end_date": "2020-06-29T06:36:22.000000Z",
  "related_to": "23123",
  "related_to_type": "candidate",
  "attendees": [
    {
      "attendee_type": "candidate",
      "attendee_id": "12654",
      "display_name": "Michael Scott",
      "attendee": [
        {
          "id": 111,
          "slug": "010011",
          "first_name": "Michael",
          "last_name": "Scott",
          "email": "mscott@gmail.com",
          "contact_number": "+1123226666",
          "avatar": "string",
          "gender_id": 1,
          "qualification_id": 4,
          "specialization": "Computer Science",
          "work_ex_year": 2,
          "candidate_dob": "2000-06-29T05:36:22.000000Z",
          "profile_update_link_status": "0",
          "profile_update_requested_on": "2021-02-09T10:00:00.000000Z",
          "profile_updated_on": "2021-02-10T10:00:00.000000Z",
          "current_salary": "150000",
          "salary_expectation": "180000",
          "willing_to_relocate": 1,
          "current_organization": "",
          "current_organization_slug": "1243452990CBB345345",
          "current_status": "Employed",
          "notice_period": 60,
          "currency_id": 2,
          "facebook": "http://www.facebook.com/michael4",
          "twitter": "http://www.twitter.com/michael4",
          "linkedin": "http://www.linkedin.com/michael4",
          "github": "",
          "created_on": "2020-06-29T05:36:22.000000Z",
          "updated_on": "2020-06-29T05:36:22.000000Z",
          "created_by": 10001,
          "updated_by": 10001,
          "owner": 10001,
          "city": "New York",
          "locality": "Manhattan",
          "state": "New York",
          "country": "United States",
          "postal_code": "10001",
          "address": "",
          "relevant_experience": 2,
          "position": "Software Developer",
          "available_from": "2020-06-29T05:36:22.000000Z",
          "salary_type": {
            "id": 1,
            "label": "Monthly Salary"
          },
          "source": "Linkedin",
          "language_skills": "English(Native/Bilingual Proficiency)",
          "skill": "Java,Python",
          "resume": "Can be Public URL to file",
          "resource_url": "string",
          "custom_fields": [
            {
              "field_id": 1,
              "value": "Region 1",
              "entity_type": "candidate",
              "field_name": "Region",
              "field_type": "text"
            }
          ],
          "xing": "string",
          "candidate_summary": "string",
          "is_email_opted_out": true,
          "email_opt_out_source": "Manually opted out"
        }
      ]
    }
  ],
  "associated_candidates": [
    "123"
  ],
  "associated_contacts": [
    "2324"
  ],
  "associated_companies": [
    "5435"
  ],
  "associated_jobs": [
    "432"
  ],
  "associated_deals": [
    "42432"
  ],
  "do_not_send_calendar_invites": "1",
  "status": "string",
  "reminder_date": "2022-12-02T16:30:00.000000Z",
  "all_day": 0,
  "related": {},
  "owner": "10023",
  "created_on": "2022-12-02T16:59:24.000000Z",
  "updated_on": "2022-12-02T16:59:24.000000Z",
  "created_by": "10002",
  "updated_by": "10002",
  "collaborator_users": [
    {
      "id": 34,
      "first_name": "Jane",
      "last_name": "Scott",
      "email": "jane.scott@gmail.com",
      "contact_number": "string",
      "avatar": "string"
    }
  ],
  "collaborator_teams": [
    null
  ]
}
```
