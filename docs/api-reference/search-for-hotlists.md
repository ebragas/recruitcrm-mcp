<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/b4c6cee2f9948-search-for-hotlists -->
<!-- title: Search for hotlists | API Endpoints -->

# Search for hotlists

**GET** `/v1/hotlists/search`

Returns all hotlists associated with your account that matched the search.

## Request

Security: Bearer Auth

### Query Parameters

- `name` (string, optional) — Hotlist Name
- `shared` (integer, optional) — Hotlist Shared status
- `related_to_type` (string, **required**) — Associated entity's Name i.e. candidate/ company/ contact/ job

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
- `id` (integer, optional) — Hotlist ID (example: `2`)
- `name` (string, optional) — Hotlist Name (example: `PHP Developer`)
- `related_to_type` (string, optional) — Associated entity's Name i.e. candidate/ company/ contact/ job (example: `candidate`)
- `related` (string, optional) — Comma-separated slugs of records added to Hotlist (example: `23123,51233`)
- `shared` (integer, optional) — Shared with team flag (example: `1`)
- `created_by` (integer, optional) — Created By (example: `12221`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/hotlists/search \
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
      "id": 2,
      "name": "PHP Developer",
      "related_to_type": "candidate",
      "related": "23123,51233",
      "shared": 1,
      "created_by": 12221
    }
  ]
}
```
