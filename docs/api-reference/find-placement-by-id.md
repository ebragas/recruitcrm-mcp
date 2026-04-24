<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/b421bd0f2e3d4-find-placement-by-id -->
<!-- title: Find placement by ID | API Endpoints -->

# Find placement by ID

**GET** `/v1/placements/{placement}`

Returns a single placement

## Request

Security: Bearer Auth

### Path Parameters

- `placement` (integer, **required**) — ID of the placement (placement\_srno)

### Query Parameters

- `expand` (string, optional) — Comma-separated list of relations to expand (created\_by,updated\_by,currency,companies,candidates,jobs,contacts,deals,\*)

## Responses

200

401

404

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

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/placements/{placement} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
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
