<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/590661546c872-search-for-contacts -->
<!-- title: Search for contacts | API Endpoints -->

# Search for contacts

**GET** `/v1/contacts/search`

Returns all contacts associated with your account that matched the search.(Enter at least one additional parameter apart from 'sort\_by' and 'sort\_order' to get the search result.)

## Request

Security: Bearer Auth

### Query Parameters

- `created_from` (string, optional) — Created (from date)
- `created_to` (string, optional) — Created (to date)
- `email` (string, optional)
- `Email` (optional)
- `first_name` (string, optional) — First Name
- `last_name` (string, optional) — Last Name
- `linkedin` (string, optional) — Linked In URL
- `marked_as_off_limit` (string, optional) — Filter records based on off-limit status. Use 'true' to return only off-limit records, or 'false' to return records that are not marked as off-limit. (allowed: `truefalse`)
- `owner_email` (string, optional) — Owner Email
- `owner_id` (string, optional) — Owner Id
- `owner_name` (string, optional) — Owner Name
- `updated_from` (string, optional) — Updated (from date)
- `updated_to` (string, optional) — Updated (to date)
- `company_slug` (string, optional) — Company Slug
- `contact_number` (string, optional) — Contact Number
- `contact_slug` (string, optional) — Contact Slug (If this filter is applied then other filters will be ignored)
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
- `id` (integer, optional) — Contact's ID (example: `2`)
- `first_name` (string, optional) — Contact's First Name (example: `Michael`)
- `last_name` (string, optional) — Contact's Last Name (example: `Scott`)
- `email` (string, optional) — Contact's Valid E-Mail (example: `mscott@gmail.com`)
- `contact_number` (string, optional) — Contact's Contact Number (example: `+1123226666`)
- `avatar` (string, optional) — Contact's Avatar URL
- `slug` (string, optional) — Contact's slug
- `company_slug` (string, optional) — Associated company's slug
- `additional_company_slugs` (string, optional) — Associated company's slug
- `created_on` (string, optional) — Created On (example: `2020-06-29T05:36:22.000000Z`)
- `updated_on` (string, optional) — Updated On (example: `2020-06-29T05:36:22.000000Z`)
- `stage_id` (integer, optional) — Contact's stage
- `facebook` (string, optional) — Facebook Profile URL of the contact (example: `http://www.facebook.com/michael4`)
- `twitter` (string, optional) — Twitter Profile URL of the contact (example: `http://www.twitter.com/michael4`)
- `linkedin` (string, optional) — Linked In Profile URL of the contact (example: `http://www.linkedin.com/michael4`)
- `xing` (string, optional) — Xing Profile URL of the contact (example: `http://www.xing.com/xyz`)
- `city` (string, optional) — City of the contact (example: `New York`)
- `locality` (string, optional) — Locality of the contact (example: `Manhattan`)
- `state` (string, optional) — State of the contact (example: `New York`)
- `country` (string, optional) — Country of the contact (example: `United States`)
- `postal_code` (string, optional) — Postal Code of the contact (example: `110001`)
- `address` (string, optional) — Address of the contact (example: `designation`)
- `string` (optional) — Designation of the contact \| This is title field (example: `HR Manager`)
- `custom_fields` (optional) — array\[object\] Array of Custom Fields (example: `\[{"field\_id":1,"value":"Region 1"}\]`)
- `created_by` (string, optional) — Created By (example: `134352`)
- `updated_by` (string, optional) — Updated By (example: `243432`)
- `owner` (string, optional)
- `Owner` (optional) (example: `32434`)
- `resource_url` (string, optional) — Resource Url
- `is_email_opted_out` (boolean, optional) — Opt out status (example: `true`)
- `email_opt_out_source` (string, optional) — Opted out source. Manually opted out or Unsubscribed (example: `Manually opted out`)
- `last_calllog_added_on` (string, optional) — Last call log added date (example: `2024-06-05T15:15:00.000000Z`)
- `last_calllog_added_by` (integer, optional) — Updated By user details (example: `5`)
- `last_meeting_created_on` (string, optional) — Last meeting added date (example: `2024-06-05T15:15:00.000000Z`)
- `last_meeting_created_by` (integer, optional) — Updated By user details (example: `5`)
- `last_linkedin_message_sent_on` (string, optional) — Last linkedin message sent on date (example: `2024-06-05T15:15:00.000000Z`)
- `last_linkedin_message_sent_by` (integer, optional) — Updated By user details (example: `5`)
- `last_email_sent_on` (string, optional) — Last email sent on date (example: `2024-06-05T15:15:00.000000Z`)
- `last_email_sent_by` (integer, optional) — Updated By user details (example: `5`)
- `last_sms_sent_on` (string, optional) — Last sms sent on date (example: `2024-06-05T15:15:00.000000Z`)
- `last_sms_sent_by` (integer, optional) — Updated By user details (example: `5`)
- `last_communication` (string, optional) — Last communication method (example: `SMS on 2024-06-05 15:15:00`)
- `status_label` (string, optional) — Off Limit Status (example: `Unavailable`)
- `off_limit_end_date` (string, optional) — Off Limit End Date (example: `2020-06-29T05:36:22.000000Z`)
- `off_limit_reason` (string, optional) — Off Limit Reason Not Settruefalse10 select an option first\_name: last\_name: linkedin: marked\_as\_off\_limit: Not Settruefalse select an option owner\_email: owner\_id: owner\_name: sort\_by: Not Setcreatedonupdatedon select an option (defaults to: updatedon) sort\_order: Not Setascdesc select an option (defaults to: desc) updated\_from: updated\_to: (example: `testing`)
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
  --url https://api.recruitcrm.io/v1/contacts/search \
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
      "first_name": "Michael",
      "last_name": "Scott",
      "email": "mscott@gmail.com",
      "contact_number": "+1123226666",
      "avatar": "string",
      "slug": "string",
      "company_slug": "string",
      "additional_company_slugs": "string",
      "created_on": "2020-06-29T05:36:22.000000Z",
      "updated_on": "2020-06-29T05:36:22.000000Z",
      "stage_id": 0,
      "facebook": "http://www.facebook.com/michael4",
      "twitter": "http://www.twitter.com/michael4",
      "linkedin": "http://www.linkedin.com/michael4",
      "xing": "http://www.xing.com/xyz",
      "city": "New York",
      "locality": "Manhattan",
      "state": "New York",
      "country": "United States",
      "postal_code": "110001",
      "address": "",
      "designation": "HR Manager",
      "custom_fields": [
        {
          "field_id": 1,
          "value": "Region 1"
        }
      ],
      "created_by": "134352",
      "updated_by": "243432",
      "owner": "32434",
      "resource_url": "string",
      "is_email_opted_out": true,
      "email_opt_out_source": "Manually opted out",
      "last_calllog_added_on": "2024-06-05T15:15:00.000000Z",
      "last_calllog_added_by": 5,
      "last_meeting_created_on": "2024-06-05T15:15:00.000000Z",
      "last_meeting_created_by": 5,
      "last_linkedin_message_sent_on": "2024-06-05T15:15:00.000000Z",
      "last_linkedin_message_sent_by": 5,
      "last_email_sent_on": "2024-06-05T15:15:00.000000Z",
      "last_email_sent_by": 5,
      "last_sms_sent_on": "2024-06-05T15:15:00.000000Z",
      "last_sms_sent_by": 5,
      "last_communication": "SMS on 2024-06-05 15:15:00",
      "status_label": "Unavailable",
      "off_limit_end_date": "2020-06-29T05:36:22.000000Z",
      "off_limit_reason": "testing"
    }
  ]
}
```
