<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/4k4er6cc6q201-draft-email-status -->
<!-- title: Draft Email Status | API Endpoints -->

# Draft Email Status

**GET** `/v1/drafts/status/{draft\_status\_id}`

To Check Draft Status

## Request

Security: Bearer Auth

### Path Parameters

- `draft_status_id` (string, **required**) — Id to check Status Of Draft Created

## Responses

200

401

429

### Body

Draft Status - Suceess

(any of)

- `message` (string, optional) (example: `Draft created successfully`)
- `created_at` (string, optional) (example: `2025-02-14T10:59:00.000000Z`)
- `status` (string, optional) (example: `Success`)
- `draft_id` (string, optional) (example: `1`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/drafts/status/{draft_status_id} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "message": "Draft created successfully",
  "created_at": "2025-02-14T10:59:00.000000Z",
  "status": "Success",
  "draft_id": "1"
}
```
