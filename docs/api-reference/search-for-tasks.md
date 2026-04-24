<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/9e43bc1ffbf44-search-for-tasks -->
<!-- title: Search for tasks | API Endpoints -->

# Search for tasks

**GET** `/v1/tasks/search`

Returns all tasks associated with your account that matched the search.

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
- `id` (integer, optional) — Task ID (example: `2`)
- `title` (string, optional) — Title of Task (example: `Follow up call`)
- `task_type` (optional) — array\[object\] Task Type (example: `\[{"id":1,"label":"Follow up"}\]`)
- `description` (string, optional) — Task Description (example: `Make follow up call for interview`)
- `reminder` (integer, optional) — Reminder ID of the task. _IDs 'Mapping: -1 => No Reminder, 0 => 0 Min Before, 15 => 15 Min Before, 30 => 30 Min Before, 60 => 1 Hour Before, 1440 => 1 Day Before_ (example: `30`)
- `start_date` (string, optional) — Start Date and time of task (example: `2020-06-29T05:36:22.000000Z`)
- `related_to` (string, optional) — Associated entity's slug (example: `23123`)
- `related_to_type` (string, optional) — Associated entity's Name i.e. candidate/ company/ contact/ job/ deal (example: `candidate`)
- `associated_candidates` (optional) — array\[string\] Array of Associated Candidates
- `associated_contacts` (optional) — array\[string\] Array of Associated Contacts
- `associated_companies` (optional) — array\[string\] Array of Associated Companies
- `associated_jobs` (optional) — array\[string\] Array of Associated Jobs
- `associated_deals` (optional) — array\[string\] Array of Associated Deals
- `related_to_name` (string, optional) — Related To Name
- `status` (string, optional)
- `Status` (optional) (example: `o`)
- `reminder_date` (string, optional) — Reminder Date and time of task (example: `2022-12-02T16:30:00.000000Z`)
- `owner` (string, optional)
- `Owner` (optional) (example: `10002`)
- `created_on` (string, optional) — Created On (example: `2022-12-02T17:00:00.000000Z`)
- `updated_on` (string, optional) — Updated On (example: `2022-12-02T17:00:00.000000Z`)
- `created_by` (string, optional) — Created By (example: `10022`)
- `updated_by` (string, optional) — Updated By (example: `10022`)
- `related` (object, optional) — Details Of Related Entity
- `collaborators` (optional) — array\[object\] Array of collaborators
- `collaborator_users` (optional) — array\[object\] Array of user collaborators (BETA/Tagging)
- `collaborator_teams` (optional) — array\[object\] Array of team collaborators (BETA/Tagging)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/tasks/search \
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
      "task_type": [
        {
          "id": 1,
          "label": "Follow up"
        }
      ],
      "description": "Make follow up call for interview",
      "reminder": 30,
      "start_date": "2020-06-29T05:36:22.000000Z",
      "related_to": "23123",
      "related_to_type": "candidate",
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
      "related_to_name": "string",
      "status": "o",
      "reminder_date": "2022-12-02T16:30:00.000000Z",
      "owner": "10002",
      "created_on": "2022-12-02T17:00:00.000000Z",
      "updated_on": "2022-12-02T17:00:00.000000Z",
      "created_by": "10022",
      "updated_by": "10022",
      "related": {},
      "collaborators": [
        {
          "attendee_type": "user",
          "attendee_id": "12654",
          "display_name": "Jane Scott",
          "attendee": [
            {
              "id": 34,
              "first_name": "Jane",
              "last_name": "Scott",
              "email": "jane.scott@gmail.com",
              "contact_number": "string",
              "avatar": "string"
            }
          ]
        }
      ],
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
