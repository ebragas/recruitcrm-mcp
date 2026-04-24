<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/c393b7508517f-off-limit-history-for-company -->
<!-- title: Off Limit History for Company | API Endpoints -->

# Off Limit History for Company

**GET** `/v1/companies/{company}/off-limit-history`

Returns the off-limit history for the requested company.

**Note:** If the company was marked as off-limit in the past but is currently not off-limit, the latest status will be available along with the corresponding 'updated\_on' timestamp.

## Request

Security: Bearer Auth

### Path Parameters

- `company` (string, **required**) — slug of the company

### Query Parameters

- `limit` (integer, optional) — Limit of records per page. (Max:100)
- `page` (integer, optional) — Page number for records

## Responses

200

401

404

### Body

- `current_page` (integer, optional) — Current page number (example: `1`)
- `first_page_url` (string, optional) — URL of the first page
- `from` (integer, optional) — Records from page number (example: `1`)
- `next_page_url` (string, optional) — URL of the next page (example: `null`)
- `path` (string, optional) — URL of the endpoint
- `per_page` (integer, optional) — Records per page (example: `25`)
- `prev_page_url` (string, optional) — URL of the next page (example: `null`)
- `to` (integer, optional) — Records to page number (example: `25`)
- `data` (optional) — array\[OffLimitHistory\]
- `status_label` (string, optional) — Off Limit Status (example: `Unavailable`)
- `reason` (string, optional) — Off Limit Reason (example: `testing`)
- `end_date` (string, optional) — Off Limit End Date (example: `2025-12-28T17:56:37.000000Z`)
- `updated_on` (string, optional) — Off Limit Status Updated On (example: `2023-12-28T17:56:37.000000Z`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/companies/{company}/off-limit-history \
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
      "status_label": "Unavailable",
      "reason": "testing",
      "end_date": "2025-12-28T17:56:37.000000Z",
      "updated_on": "2023-12-28T17:56:37.000000Z"
    }
  ]
}
```
