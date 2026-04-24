<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/28be243a2a89e-get-meeting-types -->
<!-- title: Get Meeting Types  | API Endpoints -->

# Get Meeting Types

**GET** `/v1/meeting-types`

Returns a list of meeting types

## Request

Security: Bearer Auth

## Responses

200

401

### Body

- `id` (integer, optional) — Meeting Type ID (example: `1`)
- `label` (string, optional) — Meeting Type Label (example: `Client Meeting`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/meeting-types \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "id": 1,
  "label": "Client Meeting"
}
```
