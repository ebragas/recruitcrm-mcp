<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/d4c5dc3feb0e4-edit-a-placement -->
<!-- title: Edit a placement | API Endpoints -->

# Edit a placement

**POST** `/v1/placements/{placement}`

Edit a placement.

## Request

Security: Bearer Auth

### Path Parameters

- `placement` (integer, **required**) — ID of the placement (placement\_srno) to edit

### Query Parameters

- `expand` (string, optional) — Comma-separated list of relations to expand (created\_by,updated\_by,currency,companies,candidates,jobs,contacts,deals,\*)

### Body

Placement Object

- `company_slug` (string, optional) — Company slug (example: `1234567890abc`)
- `candidate_slug` (string, optional) — Candidate slug (example: `1234567890def`)
- `job_slug` (string, optional) — Job slug (example: `1234567890ghi`)
- `contact_slugs` (string, optional) — Comma-separated contact slugs (example: `slug1,slug2`)
- `deal_slugs` (string, optional) — Comma-separated deal slugs (example: `slug1,slug2`)
- `currency_id` (integer, optional) — Currency ID (example: `1`)
- `custom_fields` (optional) — array\[object\] Array of custom fields
- `field_id` (integer, optional) (example: `1`)
- `value` (string, optional) (example: `Value`)

## Responses

200

401

404

422

### Body

- `id` (integer, optional) — Placement ID
- `company_slug` (string, optional) — Associated company slug
- `candidate_slug` (string, optional) — Associated candidate slug
- `job_slug` (string, optional) — Associated job slug
- `contact_slugs` (string, optional) — Comma-separated contact slugs
- `deal_slugs` (string, optional) — Comma-separated deal slugs
- `currency_id` (integer, optional) — Currency ID
- `company` (object, optional) — Company object (when expanded)
- `candidate` (object, optional) — Candidate object (when expanded)
- `job` (object, optional) — Job object (when expanded)
- `contacts` (array, optional) — Contacts array (when expanded)
- `deals` (array, optional) — Deals array (when expanded)
- `custom_fields` (optional) — array\[object\] Array of Custom Fields
- `field_id` (integer, optional) — Field ID
- `value` (string, optional) — Custom Value
- `created_on` (string, optional) — Created On (example: `2020-06-29T05:36:22.000000Z`)
- `updated_on` (string, optional) — Updated On (example: `2020-06-29T05:36:22.000000Z`)
- `created_by` (string, optional) — Created By
- `updated_by` (string, optional) — Updated By
- `resource_url` (string, optional) — Resource Url

#### Example request body

#### Example request body

```
{
  "company_slug": "1234567890abc",
  "candidate_slug": "1234567890def",
  "job_slug": "1234567890ghi",
  "contact_slugs": "slug1,slug2",
  "deal_slugs": "slug1,slug2",
  "currency_id": 1,
  "custom_fields": [
    {
      "field_id": 1,
      "value": "Value"
    }
  ]
}
```

#### Example cURL

#### Example cURL

```
curl --request POST \
  --url https://api.recruitcrm.io/v1/placements/{placement} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json' \
  --data '{
  "company_slug": "1234567890abc",
  "candidate_slug": "1234567890def",
  "job_slug": "1234567890ghi",
  "contact_slugs": "slug1,slug2",
  "deal_slugs": "slug1,slug2",
  "currency_id": 1,
  "custom_fields": [\
    {\
      "field_id": 1,\
      "value": "Value"\
    }\
  ]
}'
```

#### Example response

#### Example response

```
{
  "id": 0,
  "company_slug": "string",
  "candidate_slug": "string",
  "job_slug": "string",
  "contact_slugs": "string",
  "deal_slugs": "string",
  "currency_id": 0,
  "company": {},
  "candidate": {},
  "job": {},
  "contacts": [],
  "deals": [],
  "custom_fields": [
    {
      "field_id": 0,
      "value": "string"
    }
  ],
  "created_on": "2020-06-29T05:36:22.000000Z",
  "updated_on": "2020-06-29T05:36:22.000000Z",
  "created_by": "string",
  "updated_by": "string",
  "resource_url": "string"
}
```
