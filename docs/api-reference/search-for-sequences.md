<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/7a94bafe42f7f-search-for-sequences -->
<!-- title: Search for Sequences | API Endpoints -->

# Search for Sequences

**GET** `/v1/email-sequences/search`

Returns all sequences associated with your account that matched the search.

## Request

Security: Bearer Auth

### Query Parameters

- `added_from` (string, optional) — Added (from date)
- `added_to` (string, optional) — Added (to date)
- `expand` (string, optional) — The acceptable values are either created\_by or updated\_by or a combination of both. Alternatively, you can use an asterisk (\*) to expand both options. Examples:
- `created_by` (optional)
- `page` (integer, optional) — Page Number for Pagination
- `sequence_id` (integer, optional) — ID of the sequence
- `sequence_name` (string, optional) — Name of the sequence
- `updated_from` (string, optional) — Updated (from date)
- `updated_to` (string, optional) — Updated (to date)
- `exact_search` (string, optional) — If value of exact\_search is true/1 then exact search will be performed else like search will be performed (allowed: `truefalse10`)
- `limit` (integer, optional) — Limit of records per page. (Max:100)
- `sequence_type` (string, optional) — Sequence type (allowed: `candidatecontact`)
- `sort_by` (string, optional) — Sort by field (allowed: `created\_onupdated\_on`; default: `updated\_on`)
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
- `id` (integer, optional) — Sequence ID (example: `1`)
- `sequence_name` (string, optional) — Sequence name (example: `test seq`)
- `sequence_type` (string, optional) — Sequence type (example: `candidate`)
- `number_of_total_enrollment` (integer, optional) — number of total enrollments (example: `120`)
- `number_of_active_enrollment` (integer, optional) — number of active enrollments (example: `24`)
- `open_rate` (number, optional) — Open rate (example: `12.45`)
- `reply_rate` (number, optional) — Reply rate (example: `10.5`)
- `unsubscribe_rate` (number, optional) — Unsubscribe rate (example: `1.4`)
- `created_on` (string, optional) — Created On (example: `2022-12-02T16:53:27.000000Z`)
- `updated_on` (string, optional) — Updated On (example: `2022-12-02T16:53:27.000000Z`)
- `created_by` (integer, optional) — Created By (example: `10002`)
- `updated_by` (integer, optional) — Updated By Not Settruefalse10 select an option expand: limit: page: sequence\_id: sequence\_name: sequence\_type: Not Setcandidatecontact select an option sort\_by: Not Setcreated\_onupdated\_on select an option (defaults to: updated\_on) sort\_order: Not Setascdesc select an option (defaults to: desc) updated\_from: updated\_to: (example: `10002`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/email-sequences/search \
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
  ]
}
```
