<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/25689761e393c-edit-a-hotlist -->
<!-- title: Edit a hotlist | API Endpoints -->

# Edit a hotlist

**POST** `/v1/hotlists/{hotlist}`

Edit a hotlist.

## Request

Security: Bearer Auth

### Path Parameters

- `hotlist` (integer, **required**) — ID of the hotlist to edit

### Body

Hotlist Object

- `name` (string, optional) — Hotlist Name (example: `PHP Developer`)
- `related_to_type` (string, optional) — Associated entity's Name i.e. candidate/ company/ contact/ job (example: `candidate`)
- `shared` (integer, optional) — Shared with team flag (example: `1`)
- `created_by` (integer, optional)

## Responses

200

401

422

### Body

- `id` (integer, optional) — Hotlist ID (example: `2`)
- `name` (string, optional) — Hotlist Name (example: `PHP Developer`)
- `related_to_type` (string, optional) — Associated entity's Name i.e. candidate/ company/ contact/ job (example: `candidate`)
- `related` (string, optional) — Comma-separated slugs of records added to Hotlist (example: `23123,51233`)
- `shared` (integer, optional) — Shared with team flag (example: `1`)
- `created_by` (integer, optional) — Created By (example: `12221`)

#### Example request body

#### Example request body

```
{
  "name": "PHP Developer",
  "related_to_type": "candidate",
  "shared": 1,
  "created_by": 0
}
```

#### Example cURL

#### Example cURL

```
curl --request POST \
  --url https://api.recruitcrm.io/v1/hotlists/{hotlist} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json' \
  --data '{
  "name": "PHP Developer",
  "related_to_type": "candidate",
  "shared": 1,
  "created_by": 0
}'
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
