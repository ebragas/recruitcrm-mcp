<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/a3e62c46fc360-pitch-history-of-a-candidate -->
<!-- title: Pitch History of a Candidate | API Endpoints -->

# Pitch History of a Candidate

**GET** `/v1/pitch/pitch-candidate-history/{candidate}`

Get Pitch History of a Candidate

## Request

Security: Bearer Auth

### Path Parameters

- `candidate` (string, **required**) — Candidate Slug

## Responses

200

401

404

History Fetched successfully

### Body

- `data` (object, optional)
- `records` (optional) — array\[PitchCandidateHistory\]
- `message` (string, optional)
- `status` (string, optional) — status code
- `integer` (optional)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/pitch/pitch-candidate-history/{candidate} \
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
        "contact_slug": "16490671235850000005LSk",
        "status_id": 1,
        "candidate_status": "Pitched",
        "remark": "It is marked as pitched",
        "stage_date": "2023-06-29T05:36:22.000000Z",
        "updated_by": 5,
        "created_on": "2023-06-29T05:36:22.000000Z",
        "updated_on": "2023-06-29T05:36:22.000000Z"
      }
    ]
  },
  "message": "string",
  "status": "string",
  "status code": 0
}
```
