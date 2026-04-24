<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/5749f8c159bf4-get-pitch-stages -->
<!-- title: Get Pitch stages | API Endpoints -->

# Get Pitch stages

**GET** `/v1/pitch-pipeline`

Returns a list of stages in Pitch Candidate pipeline

## Request

Security: Bearer Auth

## Responses

200

401

### Body

- `status_id` (integer, optional) — Pitch Status Id (example: `1`)
- `label` (string, optional) — Stage Label (example: `Pitched`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/pitch-pipeline \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "status_id": 1,
  "label": "Pitched"
}
```
