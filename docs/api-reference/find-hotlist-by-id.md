<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/3c43bcfa9e026-find-hotlist-by-id -->
<!-- title: Find hotlist by ID | API Endpoints -->

# Find hotlist by ID

**GET** `/v1/hotlists/{hotlist}`

Returns a single hotlist

## Request

Security: Bearer Auth

### Path Parameters

- `hotlist` (integer, **required**) — ID of the hotlist to return

## Responses

200

404

### Body

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
  --url https://api.recruitcrm.io/v1/hotlists/{hotlist} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "id": 2,
  "name": "PHP Developer",
  "related_to_type": "candidate",
  "related": "23123,51233",
  "shared": 1,
  "created_by": 12221
}
```
