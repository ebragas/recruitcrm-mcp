<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/f72bd6237179f-candidate-history -->
<!-- title: Candidate History | API Endpoints -->

# Candidate History

**GET** `/v1/candidates/{candidate}/history`

Returns hiring stage history of the candidate

## Request

Security: Bearer Auth

### Path Parameters

- `candidate` (string, **required**) — slug of the candidate

## Responses

200

401

404

### Body

array of:

- `job_slug` (string, optional) — Job's Slug (example: `16425139068240003902ley`)
- `job_name` (string, optional) — Job's Name (example: `IT Specialist Job`)
- `company_slug` (string, optional) — Associated company's slug (example: `16425139047270003902lSG`)
- `company_name` (string, optional) — Name of the company (example: `Pagac Group Company`)
- `job_status_id` (integer, optional) — Job Status ID (example: `1`)
- `job_status_label` (string, optional) — Job status label (example: `Open`)
- `candidate_status_id` (integer, optional) — Candidate's status ID (example: `29306`)
- `candidate_status` (string, optional) — Candidate's status (example: `Interview Rescheduled`)
- `remark` (string, optional)
- `Remark` (optional) (example: `Task- Illustrious Deadshot Machine/Audiokinesis`)
- `updated_by` (integer, optional) — Updated By (example: `3902`)
- `updated_on` (string, optional) — Updated On (example: `2022-01-18T13:52:15.000000Z`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/candidates/{candidate}/history \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
[
  {
    "job_slug": "16425139068240003902ley",
    "job_name": "IT Specialist Job",
    "company_slug": "16425139047270003902lSG",
    "company_name": "Pagac Group Company",
    "job_status_id": 1,
    "job_status_label": "Open",
    "candidate_status_id": 29306,
    "candidate_status": "Interview Rescheduled",
    "remark": "Task- Illustrious Deadshot Machine/Audiokinesis",
    "updated_by": 3902,
    "updated_on": "2022-01-18T13:52:15.000000Z"
  }
]
```
