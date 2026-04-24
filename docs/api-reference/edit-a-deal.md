<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/e67d31717b632-edit-a-deal -->
<!-- title: Edit a deal | API Endpoints -->

# Edit a deal

**POST** `/v1/deals/{deal}`

Edit a deal.

## Request

Security: Bearer Auth

### Path Parameters

- `deal` (string, **required**) — slug of the deal to edit

### Query Parameters

- `expand` (string, optional) — Examples: \*,null,company,contacts,candidate,job,deal\_split,created\_by,updated\_by,owner

### Body

Deal Object

- `name` (string, **required**) — Deal Name (example: `Close Full Stack Developer (10 Positions)`)
- `deal_stage` (number, **required**) — Deal Stage (example: `35`)
- `deal_value` (number, **required**) — Deal Value (example: `3956.45`)
- `close_date` (string, **required**) — Deal Close Date (example: `2021-10-22`)
- `deal_type` (number, **required**) — Deal Type (example: `2`)
- `company_slug` (string, optional) — Associated company's slug (example: `1369`)
- `contact_slugs` (string, optional) — Associated contact's slugs (example: `1365,1234`)
- `job_slug` (string, optional) — Associated job's slugs (example: `1769`)
- `candidate_slug` (string, optional) — Associated candidate's slugs (example: `137169`)
- `owner_id` (integer, optional)
- `created_by` (integer, optional)
- `updated_by` (integer, optional)
- `deal_split` (optional) — array\[object\] Deal Split
- `teammates_collaborator` (object, optional) — Teammates Collaborator
- `teams_collaborator` (object, optional) — Teams Collaborator
- `split_type` (string, optional) — Split type must be custom/equal
- `custom_fields` (optional) — array\[object\] >= 1 items
- `field_id` (number, optional)
- `value` (string, optional) — >= 1 characters

## Responses

200

401

422

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

#### Example request body

#### Example request body

```
{
  "name": "Close Full Stack Developer (10 Positions)",
  "deal_stage": 35,
  "deal_value": 390000,
  "close_date": "2000-06-29T05:36:22.000000Z",
  "deal_type": 1,
  "deal_percentage_value": "40000",
  "company_slug": "1369",
  "contact_slugs": "13691,76890",
  "job_slug": "11321,432123,555643",
  "candidate_slug": "980098,554632",
  "deal_split": {
    "teammates_collaborator": [
      {
        "teammate_id": 5,
        "split_percentage": 43.98
      },
      {
        "teammate_id": 8,
        "split_percentage": 29.76
      }
    ],
    "teams_collaborator": [
      {
        "team_id": 16,
        "split_percentage": 6.33
      },
      {
        "team_id": 17,
        "split_percentage": 42.89
      }
    ],
    "split_type": "custom"
  },
  "custom_fields": [
    {
      "field_id": 3,
      "value": "ACC-2"
    }
  ]
}
```

#### Example cURL

#### Example cURL

```
curl --request POST \
  --url https://api.recruitcrm.io/v1/deals/{deal} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json' \
  --data '{
  "name": "Close Full Stack Developer (10 Positions)",
  "deal_stage": 35,
  "deal_value": 390000,
  "close_date": "2000-06-29T05:36:22.000000Z",
  "deal_type": 1,
  "deal_percentage_value": "40000",
  "company_slug": "1369",
  "contact_slugs": "13691,76890",
  "job_slug": "11321,432123,555643",
  "candidate_slug": "980098,554632",
  "deal_split": {
    "teammates_collaborator": [\
      {\
        "teammate_id": 5,\
        "split_percentage": 43.98\
      },\
      {\
        "teammate_id": 8,\
        "split_percentage": 29.76\
      }\
    ],
    "teams_collaborator": [\
      {\
        "team_id": 16,\
        "split_percentage": 6.33\
      },\
      {\
        "team_id": 17,\
        "split_percentage": 42.89\
      }\
    ],
    "split_type": "custom"
  },
  "custom_fields": [\
    {\
      "field_id": 3,\
      "value": "ACC-2"\
    }\
  ]
}'
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
