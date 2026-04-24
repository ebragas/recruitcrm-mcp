<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/f5c6018ba5921-get-note-types -->
<!-- title: Get Note Types  | API Endpoints -->

# Get Note Types

**GET** `/v1/note-types`

Returns a list of note types

## Request

Security: Bearer Auth

## Responses

200

401

### Body

- `id` (integer, optional) — Note Type ID (example: `1`)
- `label` (string, optional) — Note Type Label (example: `To Do`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/note-types \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "id": 1,
  "label": "To Do"
}
```
