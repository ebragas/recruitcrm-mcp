<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/253721386feef-search-for-candidates -->
<!-- title: Search for candidates | API Endpoints -->

# Search for candidates

**GET** `/v1/candidates/search`

Returns all candidates associated with your account that matched the search.(Enter at least one additional parameter apart from 'sort\_by' and 'sort\_order' to get the search result.)

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
- `state` (string, optional)
- `State` (optional)
- `updated_from` (string, optional) — Updated (from date)
- `updated_to` (string, optional) — Updated (to date)
- `candidate_slug` (string, optional) — Candidate Slug (If this filter is applied then other filters will be ignored)
- `contact_number` (string, optional) — Contact Number
- `country` (string, optional)
- `Country` (optional)
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
- `id` (integer, optional) — Candidate's ID (example: `111`)
- `slug` (string, optional) — Candidate's Slug (example: `010011`)
- `first_name` (string, optional) — Candidate's First Name (example: `Michael`)
- `last_name` (string, optional) — Candidate's Last Name (example: `Scott`)
- `email` (string, optional) — Candidate's Valid E-Mail (example: `mscott@gmail.com`)
- `contact_number` (string, optional) — Candidate's Contact Number (example: `+1123226666`)
- `avatar` (string, optional) — Candidate's Avatar URL
- `gender_id` (integer, optional) — Candidate's Gender: For Male - 1, Female - 2 (example: `1`)
- `qualification_id` (integer, optional) — Qualifiation of the candidate (example: `4`)
- `specialization` (string, optional) — Candidate's Sepcialisation (example: `Computer Science`)
- `work_ex_year` (integer, optional) — Total experience in years (example: `2`)
- `candidate_dob` (string, optional) — Birth date of the candidate (example: `2000-06-29T05:36:22.000000Z`)
- `profile_update_link_status` (string, optional) — Status of Profile Update Request link: For Link Active - 1, Link Expired - 0 (example: `0`)
- `profile_update_requested_on` (string, optional) — Profile Update Requested On (example: `2021-02-09T10:00:00.000000Z`)
- `profile_updated_on` (string, optional) — Profile Updated On (example: `2021-02-10T10:00:00.000000Z`)
- `current_salary` (string, optional) — Current salary of the candidate (example: `150000`)
- `salary_expectation` (string, optional) — Expected salary of the candidate (example: `180000`)
- `willing_to_relocate` (integer, optional) — Is the candidate willing to relocate? (example: `1`)
- `current_organization` (string, optional) — Last organisation of the candidate (example: `current\_organization\_slug`)
- `string` (optional) — Company Slug for the Current Organization of the Candidate (example: `1243452990CBB345345`)
- `current_status` (string, optional) — Current Employment Status of the candidate (example: `Employed`)
- `notice_period` (integer, optional) — Notice Period. Default: 0, Max: 999 (example: `60`)
- `currency_id` (integer, optional) — Currency of the candidate (example: `2`)
- `facebook` (string, optional) — Facebook Profile URL of the candidate (example: `http://www.facebook.com/michael4`)
- `twitter` (string, optional) — Twitter Profile URL of the candidate (example: `http://www.twitter.com/michael4`)
- `linkedin` (string, optional) — Linked In Profile URL of the candidate (example: `http://www.linkedin.com/michael4`)
- `github` (string, optional) — GitHub Profile URL of the candidate (example: `created\_on`)
- `string` (optional) — Created On (example: `2020-06-29T05:36:22.000000Z`)
- `updated_on` (string, optional) — Updated On (example: `2020-06-29T05:36:22.000000Z`)
- `created_by` (integer, optional) — Created By (example: `10001`)
- `updated_by` (integer, optional) — Updated By (example: `10001`)
- `owner` (integer, optional)
- `Owner` (optional) (example: `10001`)
- `city` (string, optional) — City of the candidate (example: `New York`)
- `locality` (string, optional) — Locality of the candidate (example: `Manhattan`)
- `state` (string, optional) — State of the candidate (example: `New York`)
- `country` (string, optional) — Country of the candidate (example: `United States`)
- `postal_code` (string, optional) — Postal Code of the candidate (example: `10001`)
- `address` (string, optional) — Address of the candidate (example: `relevant\_experience`)
- `integer` (optional) — Relevant Experience (example: `2`)
- `position` (string, optional) — Position/Title of the candidate (example: `Software Developer`)
- `available_from` (string, optional) — Available From Date of the candidate (example: `2020-06-29T05:36:22.000000Z`)
- `salary_type` (object, optional) — Type of salary (example: `{"id":1,"label":"Monthly Salary"}`)
- `source` (string, optional) — Candidate Source (example: `Linkedin`)
- `language_skills` (string, optional)
- `Languages` (optional) (example: `English(Native/Bilingual Proficiency)`)
- `skill` (string, optional) — Comma Separated string of candidate skills (example: `Java,Python`)
- `resume` (string, optional) — Candidate's Resume File (example: `Can be Public URL to file`)
- `resource_url` (string, optional) — Candidate's Profile Link
- `custom_fields` (optional) — array\[object\] Array of Custom Fields (example: `\[{"field\_id":1,"value":"Region 1","entity\_type":"candidate","field\_name":"Region","field\_type":"text"}\]`)
- `xing` (string, optional) — Xing Profile URL of the candidate
- `candidate_summary` (string, optional) — Summary Of Candidate
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
- `off_limit_reason` (string, optional) — Off Limit Reason (example: `testing`)
- `is_contractor` (string, optional) — `false` \- candidate, `true` \- contractor (example: `true`)
- `contractor_status` (string, optional) — `available`, `assigned` Not Settruefalse10 select an option first\_name: last\_name: linkedin: marked\_as\_off\_limit: Not Settruefalse select an option owner\_email: owner\_id: owner\_name: sort\_by: Not Setcreatedonupdatedon select an option (defaults to: updatedon) sort\_order: Not Setascdesc select an option (defaults to: desc) state: updated\_from: updated\_to: (example: `available`)
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
  --url https://api.recruitcrm.io/v1/candidates/search \
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
      "id": 111,
      "slug": "010011",
      "first_name": "Michael",
      "last_name": "Scott",
      "email": "mscott@gmail.com",
      "contact_number": "+1123226666",
      "avatar": "string",
      "gender_id": 1,
      "qualification_id": 4,
      "specialization": "Computer Science",
      "work_ex_year": 2,
      "candidate_dob": "2000-06-29T05:36:22.000000Z",
      "profile_update_link_status": "0",
      "profile_update_requested_on": "2021-02-09T10:00:00.000000Z",
      "profile_updated_on": "2021-02-10T10:00:00.000000Z",
      "current_salary": "150000",
      "salary_expectation": "180000",
      "willing_to_relocate": 1,
      "current_organization": "",
      "current_organization_slug": "1243452990CBB345345",
      "current_status": "Employed",
      "notice_period": 60,
      "currency_id": 2,
      "facebook": "http://www.facebook.com/michael4",
      "twitter": "http://www.twitter.com/michael4",
      "linkedin": "http://www.linkedin.com/michael4",
      "github": "",
      "created_on": "2020-06-29T05:36:22.000000Z",
      "updated_on": "2020-06-29T05:36:22.000000Z",
      "created_by": 10001,
      "updated_by": 10001,
      "owner": 10001,
      "city": "New York",
      "locality": "Manhattan",
      "state": "New York",
      "country": "United States",
      "postal_code": "10001",
      "address": "",
      "relevant_experience": 2,
      "position": "Software Developer",
      "available_from": "2020-06-29T05:36:22.000000Z",
      "salary_type": {
        "id": 1,
        "label": "Monthly Salary"
      },
      "source": "Linkedin",
      "language_skills": "English(Native/Bilingual Proficiency)",
      "skill": "Java,Python",
      "resume": "Can be Public URL to file",
      "resource_url": "string",
      "custom_fields": [
        {
          "field_id": 1,
          "value": "Region 1",
          "entity_type": "candidate",
          "field_name": "Region",
          "field_type": "text"
        }
      ],
      "xing": "string",
      "candidate_summary": "string",
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
      "off_limit_reason": "testing",
      "is_contractor": "true",
      "contractor_status": "available"
    }
  ]
}
```
