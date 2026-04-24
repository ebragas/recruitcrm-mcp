<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/0b5d2cb3616a8-get-contact-stages -->
<!-- title: Get Contact Stages  | API Endpoints -->

# Get Contact Stages

**GET** `/v1/sales-pipeline`

Returns a list of stages in sales pipeline

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
  --url https://api.recruitcrm.io/v1/sales-pipeline \
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
