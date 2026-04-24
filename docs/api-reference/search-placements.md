<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/1885baf84f86b-search-placements -->
<!-- title: Search Placements | API Endpoints -->

# Search Placements

**GET** `/v1/placements/search`

Search for placements using various filters. Enter at least one search parameter apart from sort\_by and sort\_order.

## Request

Security: Bearer Auth

### Query Parameters

- `candidate_name` (string, optional) — Candidate name
- `candidate_slug` (string, optional) — Candidate slug
- `company_name` (string, optional) — Company name
- `company_slug` (string, optional) — Company slug
- `contact_name` (string, optional) — Contact name
- `contact_slug` (string, optional) — Contact slug
- `created_by_email` (string, optional) — Created by user email
- `created_by_id` (integer, optional) — Created by user ID
- `created_by_name` (string, optional) — Created by user name
- `created_from` (string, optional) — Created from date
- `created_to` (string, optional) — Created to date
- `deal_name` (string, optional) — Deal name
- `deal_slug` (string, optional) — Deal slug
- `exact_search` (boolean, optional) — Exact search (true/false)
- `expand` (string, optional) — Comma-separated list of relations to expand (created\_by,updated\_by,currency,companies,candidates,jobs,contacts,deals,\*)
- `job_name` (string, optional) — Job name
- `job_slug` (string, optional) — Job slug
- `limit` (integer, optional) — Limit of records per page. (Max:100)
- `placement_id` (integer, optional) — Placement ID
- `sort_by` (string, optional) — Sort by field (createdon, updatedon)
- `sort_order` (string, optional) — Sort order (asc, desc)

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
- `resource_url` (string, optional) — Resource Url Not SetFalseTrue select an option expand: job\_name: job\_slug: limit: placement\_id: sort\_by: sort\_order:

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/placements/search \
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
