<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/d803f4bd1572c-find-task-by-id -->
<!-- title: Find task by ID | API Endpoints -->

# Find task by ID

**GET** `/v1/tasks/{task}`

Returns a single task

## Request

Security: Bearer Auth

### Path Parameters

- `task` (integer, **required**) — ID of the task

## Responses

200

404

### Body

- `id` (integer, optional) — Task ID (example: `2`)
- `title` (string, optional) — Title of Task (example: `Follow up call`)
- `task_type` (optional) — array\[object\] Task Type (example: `\[{"id":1,"label":"Follow up"}\]`)
- `id` (integer, optional) — Task Type ID (example: `1`)
- `label` (string, optional) — Task Type Label (example: `Follow up`)
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
- `attendee_type` (string, optional) — Type of Attendee i.e. user (example: `user`)
- `attendee_id` (string, optional) — Attendee ID (example: `12654`)
- `display_name` (string, optional) — Attendee Name (example: `Jane Scott`)
- `attendee` (optional) — array\[object\] Array of collaborator details
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

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/tasks/{task} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
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
```
