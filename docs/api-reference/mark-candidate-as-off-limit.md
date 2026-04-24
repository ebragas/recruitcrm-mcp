<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/a90eb52a929b1-mark-candidate-as-off-limit -->
<!-- title: Mark Candidate as Off Limit | API Endpoints -->

# Mark Candidate as Off Limit

**POST** `/v1/candidates/mark-off-limit`

Mark Candidate as Off Limit with reason

## Request

Security: Bearer Auth

### Body

Mark AS OffLimit

- `candidate_slugs` (string, **required**) — >= 1 characters (example: `141827385522`)
- `status_id` (number, **required**) (example: `59`)
- `end_date` (string, **required**) — >= 1 characters (example: `20-09-2024`)
- `reason` (string, optional) (example: `testing`)

## Responses

200

401

422

### Body

- `candidate_slug` (array, optional) — Candidate's Slug (example: `\["141827385522"\]`)
- `status_id` (integer, optional) — Status Id (example: `59`)
- `end_date` (string, optional) — End Date (example: `18-09-2023`)
- `reason` (string, optional)
- `Reason` (optional) (example: `testing`)
- `remark` (string, optional)
- `Reason` (optional) (example: `Records Were Updated`)

#### Example request body

#### Example request body

```
{
  "candidate_slugs": "141827385522",
  "status_id": "59",
  "end_date": "20-09-2024",
  "reason": "testing"
}
```

#### Example cURL

#### Example cURL

```
curl --request POST \
  --url https://api.recruitcrm.io/v1/candidates/mark-off-limit \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json' \
  --data '{
  "candidate_slugs": "141827385522",
  "status_id": "59",
  "end_date": "20-09-2024",
  "reason": "testing"
}'
```

#### Example response

#### Example response

```
{
  "candidate_slug": [
    "141827385522"
  ],
  "status_id": 59,
  "end_date": "18-09-2023",
  "reason": "testing",
  "remark": "Records Were Updated"
}
```
