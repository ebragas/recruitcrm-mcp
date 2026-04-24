<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/bd7bb4f7218ca-get-multiple-hiring-pipelines -->
<!-- title: Get Multiple Hiring Pipelines | API Endpoints -->

# Get Multiple Hiring Pipelines

**GET** `/v1/hiring-pipelines`

Returns a list of hiring pipelines

## Request

Security: Bearer Auth

## Responses

200

401

### Body

- `name` (string, optional) — Hiring Pipeline Name (example: `Master Hiring Pipeline`)
- `id` (integer, optional) — Pipeline ID (example: `0`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/hiring-pipelines \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "name": "Master Hiring Pipeline",
  "id": 0
}
```
