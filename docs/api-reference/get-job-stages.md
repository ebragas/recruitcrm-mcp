<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/f385ecc4f48c2-get-job-stages -->
<!-- title: Get Job Stages | API Endpoints -->

# Get Job Stages

**GET** `/v1/jobs-pipeline`

Returns a list of stages in jobs pipeline

## Request

Security: Bearer Auth

## Responses

200

401

### Body

- `id` (integer, optional) — Stage ID (example: `56`)
- `label` (string, optional) — Stage Label (example: `Lead`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/jobs-pipeline \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "id": 56,
  "label": "Lead"
}
```
