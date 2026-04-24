<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/6d6355405a283-find-deal-by-slug -->
<!-- title: Find deal by slug | API Endpoints -->

# Find deal by slug

**GET** `/v1/deals/{deal}`

Returns a single deal

## Request

Security: Bearer Auth

### Path Parameters

- `deal` (string, **required**) — slug of the deal to return

## Responses

200

404

### Body

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
- `teammates_collaborator` (object, optional) — Teammates collaborator
- `teams_collaborator` (object, optional) — Teams collaborator
- `teammates_unallocated_split_percentage` (string, optional) — Unallocated split percenatge of teammate
- `teams_unallocated_split_percentage` (string, optional) — Unallocated split percenatge of team
- `split_type` (string, optional) — Split type of Deal
- `custom_fields` (optional) — array\[object\] Array of Custom Fields (example: `\[{"field\_id":1,"value":"Region 1"}\]`)
- `field_id` (integer, optional) — Field ID
- `value` (string, optional) — Custom Value
- `created_on` (string, optional) — Created On (example: `2020-06-29T05:36:22.000000Z`)
- `updated_on` (string, optional) — Updated On (example: `2020-06-29T05:36:22.000000Z`)
- `created_by` (string, optional) — Created By (example: `321134`)
- `updated_by` (string, optional) — Updated By (example: `122343`)
- `owner` (string, optional)
- `Owner` (optional) (example: `100012`)
- `resource_url` (string, optional) — Resource Url

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/deals/{deal} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
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
```
