<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/8b79f6725188f-search-for-companies -->
<!-- title: Search for companies | API Endpoints -->

# Search for companies

**GET** `/v1/companies/search`

Returns all companies associated with your account that matched the search.(Enter at least one additional parameter apart from 'sort\_by' and 'sort\_order' to get the search result.)

## Request

Security: Bearer Auth

### Query Parameters

- `company_name` (string, optional) — Company Name
- `created_from` (string, optional) — Created (from date)
- `created_to` (string, optional) — Created (to date)
- `marked_as_off_limit` (string, optional) — Filter records based on off-limit status. Use 'true' to return only off-limit records, or 'false' to return records that are not marked as off-limit. (allowed: `truefalse`)
- `owner_email` (string, optional) — Owner Email
- `owner_id` (string, optional) — Owner Id
- `owner_name` (string, optional) — Owner Name
- `updated_from` (string, optional) — Updated (from date)
- `updated_to` (string, optional) — Updated (to date)
- `company_slug` (string, optional) — Company Slug (If this filter is applied then other filters will be ignored)
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
- `id` (integer, optional) — Company's ID (example: `2`)
- `industry_id` (integer, optional) — Company's industry ID
- `company_name` (string, optional) — Name of the company (example: `Recruit CRM`)
- `about_company` (string, optional) — <= 5000 characters
- `logo` (string, optional) — Company's Logo URL
- `slug` (string, optional) — Company's slug
- `created_on` (string, optional) — Created On (example: `2020-06-29T05:36:22.000000Z`)
- `updated_on` (string, optional) — Updated On (example: `2020-06-29T05:36:22.000000Z`)
- `website` (string, optional) — Website URL of the company (example: `https://www.recruitcrm.io`)
- `city` (string, optional) — City of the company (example: `New York`)
- `locality` (string, optional) — Locality of the company (example: `Manhattan`)
- `state` (string, optional) — State of the company (example: `New York`)
- `country` (string, optional) — Country of the company (example: `United States`)
- `postal_code` (string, optional) — Postal Code of the company (example: `110001`)
- `address` (string, optional) — Address of the company (example: `facebook`)
- `string` (optional) — Facebook Profile URL of the company (example: `https://www.facebook.com/recruitcrm.io/`)
- `twitter` (string, optional) — Twitter Profile URL of the company (example: `https://www.twitter.com/CrmRecruit/`)
- `linkedin` (string, optional) — Linked In Profile URL of the company (example: `https://www.linkedin.com/company/recruitcrm/`)
- `custom_fields` (optional) — array\[object\] Array of Custom Fields (example: `\[{"field\_id":1,"value":"Region 1"}\]`)
- `created_by` (string, optional) — Created By (example: `213245`)
- `updated_by` (string, optional) — Updated By (example: `123443`)
- `owner` (string, optional)
- `Owner` (optional) (example: `100023`)
- `resource_url` (string, optional) — Resource Url
- `is_child_company` (string, optional) — Whether it is a child company. (example: `Yes`)
- `is_parent_company` (string, optional) — Whether it is a parent company. (example: `No`)
- `child_company_slugs` (optional) — array\[string\] Array containing all company slugs.
- `parent_company_slug` (string, optional) — Parent company slug.
- `last_meeting_created_on` (string, optional) — Last meeting added date (example: `2024-06-05T15:15:00.000000Z`)
- `last_meeting_created_by` (integer, optional) — Updated By user details (example: `5`)
- `status_label` (string, optional) — Off Limit Status (example: `Unavailable`)
- `off_limit_end_date` (string, optional) — Off Limit End Date (example: `2020-06-29T05:36:22.000000Z`)
- `off_limit_reason` (string, optional) — Off Limit Reason Not Settruefalse10 select an option marked\_as\_off\_limit: Not Settruefalse select an option owner\_email: owner\_id: owner\_name: sort\_by: Not Setcreatedonupdatedon select an option (defaults to: updatedon) sort\_order: Not Setascdesc select an option (defaults to: desc) updated\_from: updated\_to: (example: `testing`)
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
  --url https://api.recruitcrm.io/v1/companies/search \
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
      "id": 2,
      "industry_id": 0,
      "company_name": "Recruit CRM",
      "about_company": "string",
      "logo": "string",
      "slug": "string",
      "created_on": "2020-06-29T05:36:22.000000Z",
      "updated_on": "2020-06-29T05:36:22.000000Z",
      "website": "https://www.recruitcrm.io",
      "city": "New York",
      "locality": "Manhattan",
      "state": "New York",
      "country": "United States",
      "postal_code": "110001",
      "address": "",
      "facebook": "https://www.facebook.com/recruitcrm.io/",
      "twitter": "https://www.twitter.com/CrmRecruit/",
      "linkedin": "https://www.linkedin.com/company/recruitcrm/",
      "custom_fields": [
        {
          "field_id": 1,
          "value": "Region 1"
        }
      ],
      "created_by": "213245",
      "updated_by": "123443",
      "owner": "100023",
      "resource_url": "string",
      "is_child_company": "Yes",
      "is_parent_company": "No",
      "child_company_slugs": [
        "17370009412IEv"
      ],
      "parent_company_slug": "string",
      "last_meeting_created_on": "2024-06-05T15:15:00.000000Z",
      "last_meeting_created_by": 5,
      "status_label": "Unavailable",
      "off_limit_end_date": "2020-06-29T05:36:22.000000Z",
      "off_limit_reason": "testing"
    }
  ]
}
```
