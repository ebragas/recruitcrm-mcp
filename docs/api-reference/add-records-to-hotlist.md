<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/498513c717ad0-add-records-to-hotlist -->
<!-- title: Add records to Hotlist | API Endpoints -->

# Add records to Hotlist

**POST** `/v1/hotlists/{hotlist}/add-record`

Adds records to Hotlist.

## Request

Security: Bearer Auth

### Path Parameters

- `hotlist` (integer, **required**) — ID of the hotlist to edit

### Body

Add to Hotlist Object

- `related` (string, optional) — Slug of record to be added to hotlist (example: `22231`)

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
  "related": "22231"
}
```

#### Example cURL

#### Example cURL

```
curl --request POST \
  --url https://api.recruitcrm.io/v1/hotlists/{hotlist}/add-record \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json' \
  --data '{
  "related": "22231"
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
