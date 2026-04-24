<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/d398f10338ed0-show-all-deals -->
<!-- title: Show all Deals | API Endpoints -->

# Show all Deals

**GET** `/v1/deals`

Returns all deals associated with your account.

## Request

Security: Bearer Auth

### Query Parameters

- `archived` (string, optional) — Get records based on archived status. Use '1' to return only archived records, or '0' to return records that are not archived. (allowed: `10`)
- `limit` (integer, optional) — Limit of records per page. (Max:100)
- `page` (integer, optional) — Page Number for Pagination
- `sort_by` (string, optional) — Sort by field (allowed: `createdonupdatedon`; default: `updatedon`)
- `sort_order` (string, optional) — Sort order (allowed: `ascdesc`; default: `desc`)

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
- `resource_url` (string, optional) — Resource Url Not Set10 select an option limit: page: sort\_by: Not Setcreatedonupdatedon select an option (defaults to: updatedon) sort\_order: Not Setascdesc select an option (defaults to: desc)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/deals \
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
