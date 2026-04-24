<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/c90c591495030-update-pitch-stage -->
<!-- title: Update Pitch stage | API Endpoints -->

# Update Pitch stage

**POST** `/v1/pitch/{candidate}/updated-stage/{contact}`

Update the Candidate's Pitched Stage

## Request

Security: Bearer Auth

### Path Parameters

- `candidate` (string, **required**) — Candidate's Slug
- `contact` (string, **required**) — Contact's Slug

### Query Parameters

- `updated_by` (integer, optional) — Updated By

### Body

- `status_id` (integer, **required**) — Pitch Status Id (example: `6`)
- `stage_date` (string, optional) — Stage Date (example: `2020-03-25T16:14:28.000000Z`)
- `remark` (string, optional)
- `Remark` (optional) (example: `Updated Pitch stage`)

## Responses

200

404

Stage updated successfully

### Body

- `success` (boolean, optional)
- `successCode` (integer, optional)
- `message` (string, optional)
- `data` (optional)
- `UpdatePitchStageResponse` (optional)
- `candidate_slug` (string, optional)
- `contact_slug` (string, optional)
- `status_id` (integer, optional)
- `status_label` (string, optional)
- `stage_date` (string, optional)
- `remark` (string, optional)
- `created_on` (string, optional)
- `created_by` (integer, optional)
- `updated_on` (string, optional)
- `updated_by` (integer, optional)

#### Example request body

#### Example request body

```
{
  "status_id": 6,
  "stage_date": "2020-03-25T16:14:28.000000Z",
  "remark": "Updated Pitch stage"
}
```

#### Example cURL

#### Example cURL

```
curl --request POST \
  --url https://api.recruitcrm.io/v1/pitch/{candidate}/updated-stage/{contact} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json' \
  --data '{
  "status_id": 6,
  "stage_date": "2020-03-25T16:14:28.000000Z",
  "remark": "Updated Pitch stage"
}'
```

#### Example response

#### Example response

```
{
  "success": true,
  "successCode": 0,
  "message": "string",
  "data": {
    "candidate_slug": "12345",
    "contact_slug": "34234",
    "status_id": 1,
    "stage_date": "2020-03-25T16:14:28.000000Z",
    "remark": "updated remark",
    "created_on": "2020-03-25T16:14:28.000000Z",
    "created_by": 123,
    "updated_on": "2020-03-25T16:14:28.000000Z",
    "updated_by": 123
  }
}
```
