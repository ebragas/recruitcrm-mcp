<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/57216bb5822fe-pitch-candidate-to-contact -->
<!-- title: Pitch candidate to contact | API Endpoints -->

# Pitch candidate to contact

**POST** `/v1/pitch/{candidate}/contact/{contact}`

Mark the candidate as Pitched to the contact

## Request

Security: Bearer Auth

### Path Parameters

- `candidate` (string, **required**) — Candidate's Slug
- `contact` (string, **required**) — Contact's Slug

### Query Parameters

- `created_by` (integer, optional) — Created By

## Responses

200

404

422

Candidate Pitched Successfully

### Body

- `success` (boolean, optional) (example: `true`)
- `successCode` (number, optional) — Success Code (example: `200`)
- `message` (string, optional) — Success Message (example: `Candidate Pitched Successfully`)
- `data` (optional)
- `PitchToContact` (optional)
- `candidate_slug` (string, optional) — Candidate's Slug (example: `9716881141193400000005acO`)
- `contact_slug` (string, optional) — Contact's Slug (example: `16850938893970000005dqm`)
- `status_id` (integer, optional) — Pitch Status Id (example: `6`)
- `status_label` (string, optional) — Pitch Status Label (example: `Custom stage`)
- `stage_date` (string, optional) — Stage Date (example: `2020-03-25T16:14:28.000000Z`)
- `remark` (string, optional)
- `Remark` (optional) (example: `Marked as Pitched`)
- `created_on` (string, optional) — Created On (example: `2020-03-28T16:14:28.000000Z`)
- `created_by` (integer, optional) — Created By (example: `5`)
- `updated_on` (string, optional) — Updated On (example: `2020-03-28T16:14:28.000000Z`)
- `updated_by` (integer, optional) — Updated By (example: `5`)

#### Example cURL

#### Example cURL

```
curl --request POST \
  --url https://api.recruitcrm.io/v1/pitch/{candidate}/contact/{contact} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json'
```

#### Example response

#### Example response

```
{
  "success": true,
  "successCode": 200,
  "message": "Candidate Pitched Successfully",
  "data": {
    "candidate_slug": "9716881141193400000005acO",
    "contact_slug": "16850938893970000005dqm",
    "status_id": 6,
    "stage_date": "2020-03-25T16:14:28.000000Z",
    "remark": "Marked as Pitched",
    "created_on": "2020-03-28T16:14:28.000000Z",
    "created_by": 5,
    "updated_on": "2020-03-28T16:14:28.000000Z",
    "updated_by": 5
  }
}
```
