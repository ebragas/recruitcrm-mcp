<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/caaf63f93b175-get-invoice-status -->
<!-- title: Get Invoice Status | API Endpoints -->

# Get Invoice Status

**GET** `/v1/invoice-status`

Returns a list of invoice statuses

## Request

Security: Bearer Auth

## Responses

200

401

### Body

array of:

- `id` (integer, optional) — Status ID (example: `1`)
- `label` (string, optional) — Status Label (example: `Draft`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/invoice-status \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
[
  {
    "id": 1,
    "label": "Draft"
  },
  {
    "id": 2,
    "label": "Paid"
  }
]
```
