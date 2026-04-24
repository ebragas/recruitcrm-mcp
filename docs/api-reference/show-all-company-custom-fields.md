<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/b83906b588c06-show-all-company-custom-fields -->
<!-- title: Show all Company Custom Fields | API Endpoints -->

# Show all Company Custom Fields

**GET** `/v1/custom-fields/companies`

Returns all company custom fields associated with your account.

## Request

Security: Bearer Auth

## Responses

200

401

### Body

array of:

- `field_id` (integer, optional) — Field ID (example: `1`)
- `entity_type` (string, optional) — Entity Type (example: `candidate`)
- `field_name` (string, optional) — Field Name (example: `Hobbies`)
- `field_type` (string, optional) — Field Type (example: `text`)
- `default_value` (string, optional) — Default Value

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/custom-fields/companies \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
[
  {
    "field_id": 1,
    "entity_type": "candidate",
    "field_name": "Hobbies",
    "field_type": "text",
    "default_value": "string"
  }
]
```
