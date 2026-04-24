<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/ac1a29160e4f4-search-for-meetings -->
<!-- title: Search for meetings | API Endpoints -->

# Search for meetings

**GET** `/v1/meetings/search`

Returns all meetings associated with your account that matched the search.

## Request

Security: Bearer Auth

### Query Parameters

- `created_from` (string, optional) — Created (from date)
- `created_to` (string, optional) — Created (to date)
- `owner_email` (string, optional) — Owner Email
- `owner_id` (string, optional) — Owner Id
- `owner_name` (string, optional) — Owner Name
- `related_to` (integer, optional) — Related To
- `related_to_type` (string, optional) — Related To Type
- `starting_from` (string, optional) — Starting From
- `starting_to` (string, optional) — Starting To
- `title` (string, optional)
- `Title` (optional)
- `updated_from` (string, optional) — Updated (from date)
- `updated_to` (string, optional) — Updated (to date)

## Responses

200

401

### Body

- `current_page` (integer, optional) — Current page number (example: `1`)
- `first_page_url` (string, optional) — URL of the first page
- `from` (integer, optional) — Records from page number (example: `1`)
- `next_page_url` (string, optional) — URL of the next page (example: `null`)
- `path` (string, optional) — URL of the endpoint
- `per_page` (integer, optional) — Records per page (example: `25`)
- `prev_page_url` (string, optional) — URL of the next page (example: `null`)
- `to` (integer, optional) — Records to page number (example: `25`)
- `data` (optional) — array\[object\]
- `id` (integer, optional) — Meeting ID (example: `2`)
- `title` (string, optional) — Title of Meeting (example: `Follow up call`)
- `meeting_type` (optional) — array\[object\] Meeting Type (example: `\[{"id":1,"label":"Client Meeting"}\]`)
- `description` (string, optional) — Meeting Description (example: `Make follow up call for interview`)
- `address` (string, optional) — Address of meeting (example: `Video call (https://examplelink)`)
- `reminder` (integer, optional) — Reminder ID of the Meeting. _IDs 'Mapping: -1 => No Reminder, 0 => 0 Min Before, 15 => 15 Min Before, 30 => 30 Min Before, 60 => 1 Hour Before, 120 => 2 Hours Before, 1440 => 1 Day Before_ (example: `30`)
- `start_date` (string, optional) — Start Date and time of Meeting (example: `2020-06-29T05:36:22.000000Z`)
- `end_date` (string, optional) — End Date and time of Meeting (example: `2020-06-29T06:36:22.000000Z`)
- `related_to` (string, optional) — Associated entity's slug (example: `23123`)
- `related_to_type` (string, optional) — Associated entity's Name i.e. candidate/ company/ contact/ job /deal (example: `candidate`)
- `attendees` (optional) — array\[object\] Array of attendees
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
- `collaborator_teams` (optional) — array\[object\] Array of team collaborators (BETA/Tagging)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/meetings/search \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "current_page": 1,
  "first_page_url": "string",
  "from": 1,
  "next_page_url": "null",
  "path": "string",
  "per_page": 25,
  "prev_page_url": "null",
  "to": 25,
  "data": [
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
  ]
}
```
