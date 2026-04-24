<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/28a8e23754ff3-search-for-enrollments -->
<!-- title: Search for Enrollments | API Endpoints -->

# Search for Enrollments

**GET** `/v1/enrollments/search`

Returns all enrollments associated with your account that matched the search.

## Request

Security: Bearer Auth

### Query Parameters

- `enrollment_id` (integer, optional) — Enrollment ID
- `enrollment_status` (integer, optional) — Enrollment status (allowed: `123456`)
- `expand` (string, optional) — The acceptable values include sequence, enrolled\_by, unenrolled\_by, prospect or a combination of these. Alternatively, an asterisk (\*) can be used to expand all options. Examples:
- `sequence` (optional)
- `page` (integer, optional) — Page Number for Pagination
- `prospect_slug` (string, optional) — Prospect slug
- `sequence_id` (integer, optional) — Sequence ID
- `limit` (integer, optional) — Limit of records per page. (Max:100)
- `prospect_type` (string, optional) — Prospect type (allowed: `candidatecontact`)
- `sort_by` (string, optional) — Sort by field (allowed: `enrolled\_onupdated\_on`; default: `updated\_on`)
- `sort_order` (string, optional) — Sort order (allowed: `ascdesc`; default: `desc`)

## Responses

200

401

422

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
- `id` (integer, optional) — Enrollment ID (example: `1`)
- `sequence_id` (integer, optional) — Sequence ID (example: `124`)
- `enrolled_by` (integer, optional) — Enrolled By (example: `10002`)
- `unenrolled_by` (integer, optional) — Unenrolled By (example: `10002`)
- `enrolled_on` (string, optional) — Enrolled On (example: `2022-12-02T16:53:27.000000Z`)
- `unenrolled_on` (string, optional) — Unenrolled On (example: `2022-12-02T16:53:27.000000Z`)
- `status` (object, optional) — Enrollment's status (example: `{"status\_id":1,"label":"ACTIVE"}`)
- `prospect_slug` (string, optional) — Prospect slug (example: `16318617835190000051Ond`)
- `prospect` (object, optional)
- `sequence` (object, optional) — Not Set123456 select an option expand: limit: page: prospect\_slug: prospect\_type: Not Setcandidatecontact select an option sequence\_id: sort\_by: Not Setenrolled\_onupdated\_on select an option (defaults to: updated\_on) sort\_order: Not Setascdesc select an option (defaults to: desc)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/enrollments/search \
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
      "id": 1,
      "sequence_id": 124,
      "enrolled_by": 10002,
      "unenrolled_by": 10002,
      "enrolled_on": "2022-12-02T16:53:27.000000Z",
      "unenrolled_on": "2022-12-02T16:53:27.000000Z",
      "status": {
        "status_id": 1,
        "label": "ACTIVE"
      },
      "prospect_slug": "16318617835190000051Ond",
      "prospect": {
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
        "email_opt_out_source": "Manually opted out"
      },
      "sequence": {
        "id": 1,
        "sequence_name": "test seq",
        "sequence_type": "candidate",
        "number_of_total_enrollment": 120,
        "number_of_active_enrollment": 24,
        "open_rate": 12.45,
        "reply_rate": 10.5,
        "unsubscribe_rate": 1.4,
        "created_on": "2022-12-02T16:53:27.000000Z",
        "updated_on": "2022-12-02T16:53:27.000000Z",
        "created_by": 10002,
        "updated_by": 10002
      }
    }
  ]
}
```
