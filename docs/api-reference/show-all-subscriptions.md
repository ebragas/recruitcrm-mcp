<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/c1f7d660e1dde-show-all-subscriptions -->
<!-- title: Show all subscriptions | API Endpoints -->

# Show all subscriptions

**GET** `/v1/subscriptions`

Returns all subscriptions associated with your account.

## Request

Security: Bearer Auth

### Query Parameters

- `limit` (integer, optional) — Limit of records per page.
- `page` (integer, optional) — Page Number for Pagination

## Responses

200

401

### Body

- `current_page` (integer, optional) — Current page number (example: `1`)
- `first_page_url` (string, optional) — URL of the first page
- `from` (integer, optional) — Records from page number (example: `1`)
- `next_page_url` (string, optional) — URL of the next page (example: `null`)
- `path` (string, optional) — URL of the endpoint
- `per_page` (integer, optional) — Records per page (example: `25`)
- `prev_page_url` (string, optional) — URL of the next page (example: `null`)
- `to` (integer, optional) — Records to page number (example: `25`)
- `data` (optional) — array\[object\]
- `id` (integer, optional) — Subscription ID (example: `56`)
- `event` (string, optional) — Name of Subscribed Event (example: `candidate.created`)
- `target_url` (string, optional) — Subscription URL (example: `https://someurl`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/subscriptions \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "current_page": 1,
  "first_page_url": "string",
  "from": 1,
  "next_page_url": "null",
  "path": "string",
  "per_page": 25,
  "prev_page_url": "null",
  "to": 25,
  "data": [
    {
      "id": 56,
      "event": "candidate.created",
      "target_url": "https://someurl"
    }
  ]
}
```
