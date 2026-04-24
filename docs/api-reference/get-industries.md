<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/a39e176ba64bd-get-industries -->
<!-- title: Get Industries | API Endpoints -->

# Get Industries

**GET** `/v1/industries`

Returns a list of industries

## Request

Security: Bearer Auth

## Responses

200

401

### Body

- `industry_id` (integer, optional) — Industry ID (example: `6`)
- `label` (string, optional) — Industry Label (example: `Apparel and Fashion`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/industries \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "industry_id": 6,
  "label": "Apparel and Fashion"
}
```
