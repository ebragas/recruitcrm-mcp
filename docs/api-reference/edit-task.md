<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/9dae34383346e-edit-task -->
<!-- title: Edit task | API Endpoints -->

# Edit task

**POST** `/v1/tasks/{task}`

Edit task.

## Request

Security: Bearer Auth

### Path Parameters

- `task` (integer, **required**) — ID of the task to edit

### Body

Task Object

- `id` (integer, optional) — Task ID (example: `2`)
- `title` (string, optional) — Title of Task (example: `Follow up call`)
- `task_type_id` (integer, optional) — Task Type ID (example: `1`)
- `description` (string, optional) — Task Description (example: `Make follow up call for interview`)
- `reminder` (integer, optional) — Reminder ID of the task. _IDs 'Mapping: -1 => No Reminder, 0 => 0 Min Before, 15 => 15 Min Before, 30 => 30 Min Before, 60 => 1 Hour Before, 1440 => 1 Day Before_ (example: `30`)
- `start_date` (string, optional) — Start Date and time of task (example: `2020-06-29T05:36:22.000000Z`)
- `related_to` (string, optional) — Associated entity's slug (example: `23123`)
- `related_to_type` (string, optional) — Associated entity's Name i.e. candidate/ company/ contact/ job/ deal (example: `candidate`)
- `owner_id` (integer, optional)
- `created_by` (integer, optional)
- `updated_by` (integer, optional)
- `associated_candidates` (string, optional) — Comma separated candidate slugs (example: `275,16318617835190000051Ond`)
- `associated_companies` (string, optional) — Comma separated company slugs (example: `275,16318617835190000051Ond`)
- `associated_contacts` (string, optional) — Comma separated contact slugs (example: `275,16318617835190000051Ond`)
- `associated_jobs` (string, optional) — Comma separated job slugs (example: `275,16318617835190000051Ond`)
- `associated_deals` (string, optional) — Comma separated deal slugs (example: `275,16318617835190000051Ond`)
- `collaborators` (string, optional) — Comma separated user IDs (example: `12654`)
- `collaborator_team_ids` (string, optional) — Comma separated team IDs (BETA/Tagging) (example: `16,17`)
- `enable_auto_populate_teams` (boolean, optional) — Providing '1' as value will include all teams of the user provided in owner\_id, if added; otherwise, it will include teams of the account owner, unless explicitly provided in collaborator\_team\_ids.(BETA/Tagging) (example: `1`)

## Responses

200

401

429

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

#### Example request body

#### Example request body

```
{
  "id": 2,
  "title": "Follow up call",
  "task_type_id": 1,
  "description": "Make follow up call for interview",
  "reminder": 30,
  "start_date": "2020-06-29T05:36:22.000000Z",
  "related_to": "23123",
  "related_to_type": "candidate",
  "owner_id": 0,
  "created_by": 0,
  "updated_by": 0,
  "associated_candidates": "275,16318617835190000051Ond",
  "associated_companies": "275,16318617835190000051Ond",
  "associated_contacts": "275,16318617835190000051Ond",
  "associated_jobs": "275,16318617835190000051Ond",
  "associated_deals": "275,16318617835190000051Ond",
  "collaborators": "12654",
  "collaborator_team_ids": "16,17",
  "enable_auto_populate_teams": "1"
}
```

#### Example cURL

#### Example cURL

```
curl --request POST \
  --url https://api.recruitcrm.io/v1/tasks/{task} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json' \
  --data '{
  "id": 2,
  "title": "Follow up call",
  "task_type_id": 1,
  "description": "Make follow up call for interview",
  "reminder": 30,
  "start_date": "2020-06-29T05:36:22.000000Z",
  "related_to": "23123",
  "related_to_type": "candidate",
  "owner_id": 0,
  "created_by": 0,
  "updated_by": 0,
  "associated_candidates": "275,16318617835190000051Ond",
  "associated_companies": "275,16318617835190000051Ond",
  "associated_contacts": "275,16318617835190000051Ond",
  "associated_jobs": "275,16318617835190000051Ond",
  "associated_deals": "275,16318617835190000051Ond",
  "collaborators": "12654",
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
