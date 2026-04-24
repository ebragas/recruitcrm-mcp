<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/3c65636d3d894-get-call-types -->
<!-- title: Get Call Types  | API Endpoints -->

# Get Call Types

**GET** `/v1/custom-call-types`

Returns a list of call types

## Request

Security: Bearer Auth

## Responses

200

401

### Body

- `id` (integer, optional) — Call Type ID (example: `20`)
- `label` (string, optional) — Call Type Label (example: `Interested`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/custom-call-types \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "id": 20,
  "label": "Interested"
}
```
