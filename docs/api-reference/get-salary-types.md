<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/ebc6287b2c7cf-get-salary-types -->
<!-- title: Get Salary Types | API Endpoints -->

# Get Salary Types

**GET** `/v1/salary-types`

Returns a list of salary types

## Request

Security: Bearer Auth

## Responses

200

401

### Body

- `type_id` (integer, optional) (example: `3`)
- `label` (string, optional) — Salary Label (example: `Weekly Salary`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/salary-types \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "type_id": 3,
  "label": "Weekly Salary"
}
```
