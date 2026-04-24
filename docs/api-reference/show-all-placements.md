<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/9c2623b451d65-show-all-placements -->
<!-- title: Show all Placements | API Endpoints -->

# Show all Placements

**GET** `/v1/placements`

Returns all placements associated with your account.

## Request

Security: Bearer Auth

### Query Parameters

- `expand` (string, optional) — Comma-separated list of relations to expand (created\_by,updated\_by,currency,companies,candidates,jobs,contacts,deals,\*)
- `limit` (integer, optional) — Limit of records per page. (Max:100)
- `page` (integer, optional) — Page Number for Pagination
- `sort_by` (string, optional) — Sort by field (createdon, updatedon) (allowed: `createdonupdatedon`)
- `sort_order` (string, optional) — Sort order (asc, desc) (allowed: `ascdesc`)

## Responses

200

401

### Body

- `current_page` (integer, optional) — Current page number (example: `1`)
- `first_page_url` (string, optional) — URL of the first page
- `from` (integer, optional) — Records from page number (example: `1`)
- `next_page_url` (string, optional) — URL of the next page (example: `null`)
- `path` (string, optional) — URL of the endpoint
- `per_page` (integer, optional) — Records per page (example: `25`)
- `prev_page_url` (string, optional) — URL of the next page (example: `null`)
- `to` (integer, optional) — Records to page number (example: `25`)
- `data` (optional) — array\[object\]
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
- `created_on` (string, optional) — Created On (example: `2020-06-29T05:36:22.000000Z`)
- `updated_on` (string, optional) — Updated On (example: `2020-06-29T05:36:22.000000Z`)
- `created_by` (string, optional) — Created By
- `updated_by` (string, optional) — Updated By
- `resource_url` (string, optional) — Resource Url Not Setcreatedonupdatedon select an option sort\_order: Not Setascdesc select an option

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/placements \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "current_page": 1,
  "first_page_url": "string",
  "from": 1,
  "next_page_url": "null",
  "path": "string",
  "per_page": 25,
  "prev_page_url": "null",
  "to": 25,
  "data": [
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
  ]
}
```
