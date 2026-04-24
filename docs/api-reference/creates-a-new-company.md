<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/cda6a1e5c8c2b-creates-a-new-company -->
<!-- title: Creates a new company | API Endpoints -->

# Creates a new company

**POST** `/v1/companies`

Creates a new company.

## Request

Security: Bearer Auth

### Body

Company Object

- `company_name` (string, **required**) — >= 1 characters
- `about_company` (string, optional) — <= 5000 characters
- `city` (string, optional) — >= 1 characters
- `locality` (string, optional) — >= 1 characters
- `state` (string, optional) — >= 1 characters
- `country` (string, optional) — >= 1 characters
- `postal_code` (string, optional) — >= 1 characters
- `address` (string, optional)
- `industry_id` (number, optional)
- `logo` (string, optional)
- `website` (string, optional) — >= 1 characters
- `facebook` (string, optional) — >= 1 characters
- `twitter` (string, optional)
- `linkedin` (string, optional)
- `owner_id` (integer, optional)
- `created_by` (integer, optional)
- `updated_by` (integer, optional)
- `custom_fields` (optional) — array\[object\] >= 1 items
- `field_id` (number, optional)
- `value` (string, optional) — >= 1 characters

## Responses

200

401

422

### Body

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
- `field_id` (integer, optional) — Field ID
- `value` (string, optional) — Custom Value
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
- `off_limit_reason` (string, optional) — Off Limit Reason (example: `testing`)

#### Example request body

#### Example request body

```
{
  "company_name": "Acme Inc",
  "city": "New York",
  "address": "",
  "industry_id": 1,
  "logo": "",
  "website": "https://www.example.com",
  "facebook": "https://facebook.com/acme",
  "twitter": "",
  "linkedin": "",
  "custom_fields": [
    {
      "field_id": 1,
      "value": "ACME-929"
    }
  ]
}
```

#### Example cURL

#### Example cURL

```
curl --request POST \
  --url https://api.recruitcrm.io/v1/companies \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json' \
  --data '{
  "company_name": "Acme Inc",
  "city": "New York",
  "address": "",
  "industry_id": 1,
  "logo": "",
  "website": "https://www.example.com",
  "facebook": "https://facebook.com/acme",
  "twitter": "",
  "linkedin": "",
  "custom_fields": [\
    {\
      "field_id": 1,\
      "value": "ACME-929"\
    }\
  ]
}'
```

#### Example response

#### Example response

```
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
```
