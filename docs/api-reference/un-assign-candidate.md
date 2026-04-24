<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/e542c0753077d-un-assign-candidate -->
<!-- title: Un-assign Candidate | API Endpoints -->

# Un-assign Candidate

**POST** `/v1/candidates/{candidate}/unassign`

Un-assign a candidate from the job.

## Request

Security: Bearer Auth

### Path Parameters

- `candidate` (string, **required**) — slug of the candidate

### Query Parameters

- `job_slug` (string, **required**) — slug of the job

## Responses

200

401

422

### Body

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
- `field_id` (integer, optional) — Field ID (example: `1`)
- `entity_type` (string, optional) — Entity Type (example: `candidate`)
- `field_name` (string, optional) — Field Name (example: `Hobbies`)
- `field_type` (string, optional) — Field Type (example: `text`)
- `default_value` (string, optional) — Default Value
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
- `contractor_status` (string, optional) — `available`, `assigned` (example: `available`)

#### Example cURL

#### Example cURL

```
curl --request POST \
  --url https://api.recruitcrm.io/v1/candidates/{candidate}/unassign \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json'
```

#### Example response

#### Example response

```
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
```
