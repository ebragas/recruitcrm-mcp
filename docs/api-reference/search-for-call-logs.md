<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/aaa3782c90e7c-search-for-call-logs -->
<!-- title: Search for call logs | API Endpoints -->

# Search for call logs

**GET** `/v1/call-logs/search`

Returns all call logs associated with your account that matched the search.

## Request

Security: Bearer Auth

### Query Parameters

- `call_type` (string, optional) — Call Direction: For Outgoing Call - CALL\_OUTGOING, Incoming Call - CALL\_INCOMING
- `related_to` (string, optional) — Associated entity's slug
- `related_to_type` (string, optional) — Associated entity's Name i.e. candidate/ company/ contact/ job
- `starting_from` (string, optional) — Starting (from date)
- `starting_to` (string, optional) — Starting (to date)
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
- `id` (integer, optional) — CallLog ID (example: `2`)
- `call_type` (string, optional) — Call Direction: For Outgoing Call - CALL\_OUTGOING, Incoming Call - CALL\_INCOMING (example: `CALL\_OUTGOING`)
- `custom_call_type` (optional) — array\[object\] Custom Call Type (example: `\[{"id":2241,"label":"Follow-Up Call"}\]`)
- `call_started_on` (string, optional) — Call Start Date Time (example: `2020-12-01T10:30:00.000000Z`)
- `contact_number` (string, optional) — Contact Number (example: `1234432112`)
- `call_notes` (string, optional) — Call Notes (example: `Will be open for offer after 2 months`)
- `related_to` (string, optional) — Associated entity's slug (example: `23123`)
- `related_to_type` (string, optional) — Associated entity's Name i.e. candidate/ contact/ company (example: `candidate`)
- `duration` (string, optional) — The Call Duration parameter supports the following formats: 1h 2m 10s, 1hr 20min 30sec, 5:30:50, and total seconds (e.g., 3020). The response will be in seconds. (example: `1h 2m 10s`)
- `associated_candidates` (optional) — array\[string\] Array of Associated Candidates
- `associated_contacts` (optional) — array\[string\] Array of Associated Contacts
- `associated_companies` (optional) — array\[string\] Array of Associated Companies
- `associated_jobs` (optional) — array\[string\] Array of Associated Jobs
- `associated_deals` (optional) — array\[string\] Array of Associated Deals
- `related` (object, optional) — Details Of Related Entity
- `created_on` (string, optional) — Created On (example: `2022-12-02T17:00:00.000000Z`)
- `updated_on` (string, optional) — Updated On (example: `2022-12-02T17:00:00.000000Z`)
- `created_by` (string, optional) — Created By (example: `100023`)
- `updated_by` (string, optional) — Updated By (example: `100023`)
- `collaborator_users` (optional) — array\[object\] Array of user collaborators (BETA/Tagging)
- `collaborator_teams` (optional) — array\[object\] Array of team collaborators (BETA/Tagging)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/call-logs/search \
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
      "call_type": "CALL_OUTGOING",
      "custom_call_type": [
        {
          "id": 2241,
          "label": "Follow-Up Call"
        }
      ],
      "call_started_on": "2020-12-01T10:30:00.000000Z",
      "contact_number": "1234432112",
      "call_notes": "Will be open for offer after 2 months",
      "related_to": "23123",
      "related_to_type": "candidate",
      "duration": "1h 2m 10s",
      "associated_candidates": [
        "123"
      ],
      "associated_contacts": [
        "123"
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
      "created_on": "2022-12-02T17:00:00.000000Z",
      "updated_on": "2022-12-02T17:00:00.000000Z",
      "created_by": "100023",
      "updated_by": "100023",
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
