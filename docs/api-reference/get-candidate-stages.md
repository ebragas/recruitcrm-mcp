<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/8b78732cb4cca-get-candidate-stages -->
<!-- title: Get Candidate Stages | API Endpoints -->

# Get Candidate Stages

**GET** `/v1/hiring-pipeline`

Returns a list of stages in hiring pipeline

## Request

Security: Bearer Auth

## Responses

200

401

### Body

- `stage_id` (integer, optional) — Stage ID (example: `56`)
- `label` (string, optional) — Stage Label (example: `Lead`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/hiring-pipeline \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "stage_id": 56,
  "label": "Lead"
}
```
