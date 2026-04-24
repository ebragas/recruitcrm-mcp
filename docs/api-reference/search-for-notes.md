<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/1699dbe9efb12-search-for-notes -->
<!-- title: Search for notes | API Endpoints -->

# Search for notes

**GET** `/v1/notes/search`

Returns all notes associated with your account that matched the search.

## Request

Security: Bearer Auth

### Query Parameters

- `added_from` (string, optional) — Added (from date)
- `added_to` (string, optional) — Added (to date)
- `related_to` (string, optional) — Associated entity's slug
- `related_to_type` (string, optional) — Associated entity's Name i.e. candidate/ company/ contact/ job
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
- `id` (integer, optional) — Note ID (example: `2`)
- `note_type` (optional) — array\[object\] Note Type (example: `\[{"id":1,"label":"To Do"}\]`)
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
- `collaborator_teams` (optional) — array\[object\] Array of team collaborators (BETA/Tagging)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/notes/search \
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
  ]
}
```
