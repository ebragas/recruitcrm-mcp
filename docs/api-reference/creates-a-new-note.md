<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/786f67d4d13d4-creates-a-new-note -->
<!-- title: Creates a new Note | API Endpoints -->

# Creates a new Note

**POST** `/v1/notes`

Creates a new Note.

## Request

Security: Bearer Auth

### Body

Note Object

- `note_type_id` (integer, optional) — Note Type (example: `1`)
- `description` (string, **required**) — Note Description (example: `Will be open for offer after 2 months`)
- `related_to` (string, **required**) — Associated entity's slug (example: `23123`)
- `related_to_type` (string, **required**) — Associated entity's Name i.e. candidate/ company/ contact/ job/ deal (example: `candidate`)
- `created_by` (integer, optional)
- `updated_by` (integer, optional)
- `associated_candidates` (string, optional) — Comma separated candidate slugs (example: `275,16318617835190000051Ond`)
- `associated_companies` (string, optional) — Comma separated company slugs (example: `275,16318617835190000051Ond`)
- `associated_contacts` (string, optional) — Comma separated contact slugs (example: `275,16318617835190000051Ond`)
- `associated_jobs` (string, optional) — Comma separated job slugs (example: `275,16318617835190000051Ond`)
- `associated_deals` (string, optional) — Comma separated deal slugs (example: `275,16318617835190000051Ond`)
- `collaborator_user_ids` (string, optional) — Comma separated user IDs (BETA/Tagging) (example: `11496,11497`)
- `collaborator_team_ids` (string, optional) — Comma separated team IDs (BETA/Tagging) (example: `16,17`)
- `enable_auto_populate_teams` (boolean, optional) — Providing '1' as value will include all teams of the user provided in created\_by, if added; otherwise, it will include teams of the account owner, unless explicitly provided in collaborator\_team\_ids.(BETA/Tagging) (example: `1`)

## Responses

200

401

429

### Body

- `id` (integer, optional) — Note ID (example: `2`)
- `note_type` (optional) — array\[object\] Note Type (example: `\[{"id":1,"label":"To Do"}\]`)
- `id` (integer, optional) — Note Type ID (example: `1`)
- `label` (string, optional) — Note Type Label (example: `To Do`)
- `description` (string, optional) — Note Description (example: `Will be open for offer after 2 months`)
- `related_to` (string, optional) — Associated entity's slug (example: `23123`)
- `related_to_type` (string, optional) — Associated entity's Name i.e. candidate/ company/ contact/ job/ deal (example: `candidate`)
- `associated_candidates` (optional) — array\[string\] Array of Associated Candidates
- `associated_contacts` (optional) — array\[string\] Array of Associated Contacts
- `associated_companies` (optional) — array\[string\] Array of Associated Companies
- `associated_jobs` (optional) — array\[string\] Array of Associated Jobs
- `associated_deals` (optional) — array\[string\] Array of Associated Deals
- `related` (object, optional) — Details Of Related Entity
- `created_on` (string, optional) — Created On (example: `2022-12-02T16:53:27.000000Z`)
- `updated_on` (string, optional) — Updated On (example: `2022-12-02T16:53:27.000000Z`)
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
  "note_type_id": 1,
  "description": "Will be open for offer after 2 months",
  "related_to": "23123",
  "related_to_type": "candidate",
  "created_by": 0,
  "updated_by": 0,
  "associated_candidates": "275,16318617835190000051Ond",
  "associated_companies": "275,16318617835190000051Ond",
  "associated_contacts": "275,16318617835190000051Ond",
  "associated_jobs": "275,16318617835190000051Ond",
  "associated_deals": "275,16318617835190000051Ond",
  "collaborator_user_ids": "11496,11497",
  "collaborator_team_ids": "16,17",
  "enable_auto_populate_teams": "1"
}
```

#### Example cURL

#### Example cURL

```
curl --request POST \
  --url https://api.recruitcrm.io/v1/notes \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json' \
  --data '{
  "note_type_id": 1,
  "description": "Will be open for offer after 2 months",
  "related_to": "23123",
  "related_to_type": "candidate",
  "created_by": 0,
  "updated_by": 0,
  "associated_candidates": "275,16318617835190000051Ond",
  "associated_companies": "275,16318617835190000051Ond",
  "associated_contacts": "275,16318617835190000051Ond",
  "associated_jobs": "275,16318617835190000051Ond",
  "associated_deals": "275,16318617835190000051Ond",
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
  "note_type": [
    {
      "id": 1,
      "label": "To Do"
    }
  ],
  "description": "Will be open for offer after 2 months",
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
  "related": {},
  "created_on": "2022-12-02T16:53:27.000000Z",
  "updated_on": "2022-12-02T16:53:27.000000Z",
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
