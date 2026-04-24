<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/b429f07da6599-get-currencies -->
<!-- title: Get Currencies | API Endpoints -->

# Get Currencies

**GET** `/v1/currencies`

Returns a list of currencies

## Request

Security: Bearer Auth

## Responses

200

401

### Body

- `currency_id` (integer, optional) — Currency ID (example: `2`)
- `code` (string, optional) — Currency Code (example: `INR`)
- `country` (string, optional) — Currency Country (example: `India`)
- `currency` (string, optional)
- `Currency` (optional) (example: `Rupees`)
- `symbol` (string, optional) — Currency symbol (example: `₹`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/currencies \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "currency_id": 2,
  "code": "INR",
  "country": "India",
  "currency": "Rupees",
  "symbol": "₹"
}
```
