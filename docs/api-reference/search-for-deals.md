<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/86cc17c5746bc-search-for-deals -->
<!-- title: Search for deals | API Endpoints -->

# Search for deals

**GET** `/v1/deals/search`

Returns all deals associated with your account that matched the search.(Enter at least one additional parameter apart from sort\_by and sort\_order to get the search result.)

## Request

Security: Bearer Auth

### Query Parameters

- `added_from` (string, optional) — Added (from date)
- `added_to` (string, optional) — Added (to date)
- `archived` (string, optional) — Filter records based on archived status. Use '1' to return only archived records, or '0' to return records that are not archived. (allowed: `10`)
- `candidate_name` (string, optional) — Candidate Name
- `candidate_slug` (string, optional) — Candidate Slug
- `closing_from` (string, optional) — Closing (from date)
- `closing_to` (string, optional) — Closing (to date)
- `company_name` (string, optional) — Company Name
- `company_slug` (string, optional) — Company Slug
- `contact_name` (string, optional) — Contact Name
- `contact_slug` (string, optional) — Contact Slug
- `deal_name` (string, optional) — Deal Name
- `deal_stage` (string, optional)
- `stage` (optional)
- `job_name` (string, optional) — Job Name
- `job_slug` (string, optional) — Job Slug
- `owner_email` (string, optional) — Owner Email
- `owner_id` (string, optional) — Owner Id
- `owner_name` (string, optional) — Owner Name
- `updated_from` (string, optional) — Updated (from date)
- `updated_to` (string, optional) — Updated (to date)
- `deal_slug` (string, optional) — Deal Slug (If this filter is applied then other filters will be ignored)
- `exact_search` (string, optional) — If value of exact\_search is true/1 then exact search will be performed else like search will be performed (allowed: `truefalse10`)
- `sort_by` (string, optional) — Sort by field (allowed: `createdonupdatedon`; default: `updatedon`)
- `sort_order` (string, optional) — Sort order (allowed: `ascdesc`; default: `desc`)

### Body

#### Search By custom Fields

Click [here](https://docs.recruitcrm.io/docs/rcrm-api-reference/ZG9jOjEyMzU5OTgw-custom-field) to know more about `Supported Filter Types`

custom\_fields

array\[object\]

Array of Custom Fields

field\_id

integer

Field ID

Example:

1

filter\_type

string

Filter Type

Allowed values:

equalsnot\_equalscontainsnot\_containsavailablenot\_availablegreater\_thanless\_thanyesno

Example:

equals

filter\_value

string

Value to Filter

Example:

search value

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
- `id` (integer, optional) — Deal ID
- `name` (string, optional) — Deal Name
- `deal_stage` (string, optional) — Deal Stage
- `deal_value` (string, optional) — Deal Value
- `close_date` (string, optional) — Deal Close Date
- `deal_type` (string, optional) — Deal Type
- `deal_percentage_value` (string, optional) — Weighted Deal Amount
- `slug` (string, optional) — Deal's Slug
- `archived` (number, optional) — `0` \- No, `1` \- Yes (example: `0`)
- `company_slug` (string, optional) — Associated company's slug
- `contact_slugs` (string, optional) — Associated contact's slugs (example: `1365,1234`)
- `additional_job_slugs` (string, optional) — Associated job's slugs (example: `1769,1122,2211`)
- `additional_candidate_slugs` (string, optional) — Associated candidate's slugs (example: `137169,21234,56789`)
- `deal_split` (optional) — array\[object\] Deal Split
- `custom_fields` (optional) — array\[object\] Array of Custom Fields (example: `\[{"field\_id":1,"value":"Region 1"}\]`)
- `created_on` (string, optional) — Created On (example: `2020-06-29T05:36:22.000000Z`)
- `updated_on` (string, optional) — Updated On (example: `2020-06-29T05:36:22.000000Z`)
- `created_by` (string, optional) — Created By (example: `321134`)
- `updated_by` (string, optional) — Updated By (example: `122343`)
- `owner` (string, optional)
- `Owner` (optional) (example: `100012`)
- `resource_url` (string, optional) — Resource Url Not Set10 select an option candidate\_name: candidate\_slug: closing\_from: closing\_to: company\_name: company\_slug: contact\_name: contact\_slug: deal\_name: deal\_slug: deal\_stage: exact\_search: Not Settruefalse10 select an option job\_name: job\_slug: owner\_email: owner\_id: owner\_name: sort\_by: Not Setcreatedonupdatedon select an option (defaults to: updatedon) sort\_order: Not Setascdesc select an option (defaults to: desc) updated\_from: updated\_to:
- `Body` (optional)

#### Example request body

#### Example request body

```
{
  "custom_fields": [
    {
      "field_id": 1,
      "filter_type": "equals",
      "filter_value": "search value"
    }
  ]
}
```

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/deals/search \
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
      "name": "string",
      "deal_stage": "string",
      "deal_value": "string",
      "close_date": "string",
      "deal_type": "string",
      "deal_percentage_value": "string",
      "slug": "string",
      "archived": 0,
      "company_slug": "string",
      "contact_slugs": "1365,1234",
      "additional_job_slugs": "1769,1122,2211",
      "additional_candidate_slugs": "137169,21234,56789",
      "deal_split": [
        {
          "teammates_collaborator": {},
          "teams_collaborator": {},
          "teammates_unallocated_split_percentage": "string",
          "teams_unallocated_split_percentage": "string",
          "split_type": "string"
        }
      ],
      "custom_fields": [
        {
          "field_id": 1,
          "value": "Region 1"
        }
      ],
      "created_on": "2020-06-29T05:36:22.000000Z",
      "updated_on": "2020-06-29T05:36:22.000000Z",
      "created_by": "321134",
      "updated_by": "122343",
      "owner": "100012",
      "resource_url": "string"
    }
  ]
}
```
