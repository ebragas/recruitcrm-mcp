<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/74646db5004dd-pitch-history-of-a-candidate-and-contact -->
<!-- title: Pitch History of a Candidate and Contact  | API Endpoints -->

# Pitch History of a Candidate and Contact

**GET** `/v1/pitch/{candidate}/history/{contact}`

Get Pitch History of a Candidate and Contact

## Request

Security: Bearer Auth

### Path Parameters

- `candidate` (string, **required**) — Candidate's Slug
- `contact` (string, **required**) — Contact's Slug

## Responses

200

404

History fetched successfully

### Body

- `data` (object, optional)
- `records` (optional) — array\[PitchHistory\]
- `message` (string, optional)
- `status` (string, optional) — status code
- `integer` (optional)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/pitch/{candidate}/history/{contact} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "data": {
    "records": [
      {
        "status_id": 10,
        "candidate_status": "Pitched",
        "remark": "Pitch History",
        "stage_date": "2023-12-28T17:56:37.000000Z",
        "updated_by": "5",
        "created_on": "2023-12-28T17:56:37.000000Z",
        "updated_on": "2023-12-28T17:56:37.000000Z"
      }
    ]
  },
  "message": "string",
  "status": "string",
  "status code": 0
}
```
