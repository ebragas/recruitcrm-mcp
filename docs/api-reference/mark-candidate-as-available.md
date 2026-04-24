<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/100dd771caae9-mark-candidate-as-available -->
<!-- title: Mark Candidate as Available | API Endpoints -->

# Mark Candidate as Available

**POST** `/v1/candidates/mark-as-available`

Mark Candidate as Available

## Request

Security: Bearer Auth

### Body

Mark As Available

- `candidate_slugs` (string, **required**) — >= 1 characters (example: `141827385522`)

## Responses

200

401

422

### Body

- `candidate_slug` (array, optional) — Candidate's Slug (example: `\["141827385522"\]`)
- `remark` (string, optional)
- `Reason` (optional) (example: `Records Were Updated`)

#### Example request body

#### Example request body

```
{
  "candidate_slugs": "141827385522"
}
```

#### Example cURL

#### Example cURL

```
curl --request POST \
  --url https://api.recruitcrm.io/v1/candidates/mark-as-available \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json' \
  --data '{
  "candidate_slugs": "141827385522"
}'
```

#### Example response

#### Example response

```
{
  "candidate_slug": [
    "141827385522"
  ],
  "remark": "Records Were Updated"
}
```
