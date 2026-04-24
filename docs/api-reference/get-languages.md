<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/97b83916f02e2-get-languages -->
<!-- title: Get Languages | API Endpoints -->

# Get Languages

**GET** `/v1/languages`

Returns a list of languages

## Request

Security: Bearer Auth

## Responses

200

401

### Body

- `language_id` (integer, optional) — Language ID (example: `38`)
- `code` (string, optional) — Language Code (example: `en`)
- `language_name` (string, optional) — Language Name (example: `English`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/languages \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "language_id": 38,
  "code": "en",
  "language_name": "English"
}
```
