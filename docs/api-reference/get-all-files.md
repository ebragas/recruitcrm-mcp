<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/e0e3a7ba8dc80-get-all-files -->
<!-- title: Get All Files | API Endpoints -->

# Get All Files

**GET** `/v1/files/{entity}/{slug}`

Returns all Files associated with your entity.

## Request

Security: Bearer Auth

### Path Parameters

- `entity` (string, **required**) — Associated entity's Name i.e. candidate/ company/ contact/ job/ deal
- `slug` (string, **required**) — Associated entity's slug

## Responses

200

401

### Body

- `file_name` (string, optional) — File Name
- `file_link` (string, optional) — File Link
- `created_by` (string, optional) — Created By (example: `10002`)
- `created_on` (string, optional) — Created On (example: `2022-12-02T16:53:27.000000Z`)
- `related_to` (string, optional) — Associated entity's slug (example: `23123`)
- `related_to_type` (string, optional) — Associated entity's Name i.e. candidate/ company/ contact/ job/ deal (example: `candidate`)
- `related` (object, optional) — Details Of Related Entity
- `folder` (string, optional) — Folder name (example: `folder1`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/files/{entity}/{slug} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "file_name": "string",
  "file_link": "string",
  "created_by": "10002",
  "created_on": "2022-12-02T16:53:27.000000Z",
  "related_to": "23123",
  "related_to_type": "candidate",
  "related": {},
  "folder": "folder1"
}
```
