<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/1bbf8e7f8a146-get-call-recording-upload-status -->
<!-- title: Get Call Recording Upload Status | API Endpoints -->

# Get Call Recording Upload Status

**GET** `/v1/call-logs/get-recording-status/{call\_log}`

Returns the call logs recording upload status. If the recording is uploaded, it will return the recording URL.

## Request

Security: Bearer Auth

### Path Parameters

- `call_log` (integer, **required**) — ID of the call log to return

## Responses

200

401

404

### Body

- `id` (integer, optional) — CallLog ID (example: `2`)
- `call_type` (string, optional) — Call Direction: For Outgoing Call - CALL\_OUTGOING, Incoming Call - CALL\_INCOMING (example: `CALL\_OUTGOING`)
- `custom_call_type` (optional) — array\[object\] Custom Call Type (example: `\[{"id":2241,"label":"Follow-Up Call"}\]`)
- `id` (integer, optional) — Call Type ID (example: `20`)
- `label` (string, optional) — Call Type Label (example: `Interested`)
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
- `id` (integer, optional) — User ID (example: `34`)
- `first_name` (string, optional) — User's First Name (example: `Jane`)
- `last_name` (string, optional) — User's Last Name (example: `Scott`)
- `email` (string, optional) — User's Email (example: `jane.scott@gmail.com`)
- `contact_number` (string, optional) — User's contact\_number
- `avatar` (string, optional) — User's avatar link
- `collaborator_teams` (optional) — array\[object\] Array of team collaborators (BETA/Tagging)
- `team_id` (integer, optional) — Team ID (example: `16`)
- `team_name` (string, optional) — Team Name (example: `team1`)
- `recording` (string, optional) — Recording URL (it will only shown if recording\_required param is true and there is recording available else null) and this recording will expire one hour after it is generated.

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/call-logs/get-recording-status/{call_log} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
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
  ],
  "recording": "string"
}
```
