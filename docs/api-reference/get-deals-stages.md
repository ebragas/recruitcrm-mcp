<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/cb4223f869e95-get-deals-stages -->
<!-- title: Get Deals Stages  | API Endpoints -->

# Get Deals Stages

**GET** `/v1/deals-pipeline`

Returns a list of stages in deals pipeline

## Request

Security: Bearer Auth

## Responses

200

401

### Body

- `id` (integer, optional) — Deal Stage ID (example: `3`)
- `label` (string, optional) — Deal Stage Label (example: `In Progress`)
- `percentage` (string, optional) — Deal Stage Percentage (example: `10`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/deals-pipeline \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "id": 3,
  "label": "In Progress",
  "percentage": "10"
}
```
