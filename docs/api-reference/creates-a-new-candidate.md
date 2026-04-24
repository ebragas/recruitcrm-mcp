<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/ba451e2a3bd63-creates-a-new-candidate -->
<!-- title: Creates a new candidate | API Endpoints -->

# Creates a new candidate

**POST** `/v1/candidates`

Creates a new Candidate.(Use Content-Type : Multipart/form-data if you want to upload any file)

## Request

Security: Bearer Auth

### Body

multipart/form-dataapplication/json

Candidate Object

- `first_name` (string, **required**) — >= 1 characters
- `last_name` (string, optional) — >= 1 characters
- `email` (string, optional) — >= 1 characters
- `contact_number` (string, optional) — >= 1 characters
- `avatar` (string, optional)
- `gender_id` (number, optional)
- `qualification_id` (number, optional) — To be deprecated, instead use Education History API
- `specialization` (string, optional) — To be deprecated, instead use Education History API >= 1 characters
- `work_ex_year` (number, optional)
- `candidate_dob` (string, optional) — >= 1 characters
- `profile_updated_on` (string, optional) — >= 1 characters
- `current_salary` (string, optional) — >= 1 characters
- `salary_expectation` (string, optional) — >= 1 characters
- `willing_to_relocate` (number, optional)
- `current_organization` (string, optional)
- `current_organization_slug` (string, optional) — Company Slug for the Current Organization of the Candidate
- `current_status` (string, optional) — >= 1 characters
- `notice_period` (number, optional)
- `currency_id` (number, optional)
- `facebook` (string, optional) — >= 1 characters
- `twitter` (string, optional) — >= 1 characters
- `linkedin` (string, optional) — >= 1 characters
- `github` (string, optional)
- `xing` (string, optional) — >= 1 characters
- `city` (string, optional) — >= 1 characters
- `locality` (string, optional) — >= 1 characters
- `state` (string, optional) — >= 1 characters
- `country` (string, optional) — >= 1 characters
- `postal_code` (string, optional) — >= 1 characters
- `address` (string, optional)
- `relevant_experience` (number, optional)
- `position` (string, optional) — Position/Title of the candidate >= 1 characters
- `available_from` (string, optional) — >= 1 characters
- `salary_type` (number, optional)
- `source` (string, optional) — >= 1 characters
- `language_skills` (optional) — array\[object\] >= 1 items
- `language_id` (number, optional)
- `proficiency_id` (number, optional)
- `skill` (string, optional) — >= 1 characters
- `resume` (optional) — string or object Can be Public URL to file, or File (form-data)
- `owner_id` (integer, optional)
- `created_by` (integer, optional)
- `updated_by` (integer, optional)
- `custom_fields` (optional) — array\[object\]
- `field_id` (integer, optional)
- `value` (string, optional)
- `candidate_summary` (string, optional)

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
- `off_limit_reason` (string, optional) — Off Limit Reason Omit last\_name email: Omit email contact\_number: Omit contact\_number avatar: Omit avatar gender\_id: Omit gender\_id qualification\_id: Omit qualification\_id specialization: Omit specialization work\_ex\_year: Omit work\_ex\_year candidate\_dob: Omit candidate\_dob profile\_updated\_on: Omit profile\_updated\_on current\_salary: Omit current\_salary salary\_expectation: Omit salary\_expectation willing\_to\_relocate: Omit willing\_to\_relocate current\_organization: Omit current\_organization current\_organization\_slug: Omit current\_organization\_slug current\_status: Omit current\_status notice\_period: Omit notice\_period currency\_id: Omit currency\_id facebook: Omit facebook twitter: Omit twitter linkedin: Omit linkedin github: Omit github xing: Omit xing city: Omit city locality: Omit locality state: Omit state country: Omit country postal\_code: Omit postal\_code address: Omit address relevant\_experience: Omit relevant\_experience position: Omit position available\_from: Omit available\_from salary\_type: Omit salary\_type source: Omit source language\_skills: Omit language\_skills skill: Omit skill resume: Omit resume owner\_id: Omit owner\_id created\_by: Omit created\_by updated\_by: Omit updated\_by custom\_fields: Omit custom\_fields candidate\_summary: Omit candidate\_summary (example: `testing`)

#### Example cURL

#### Example cURL

```
curl --request POST
  --url https://api.recruitcrm.io/v1/candidates
  --header 'Accept: application/json'
  --header 'Authorization: Bearer 123'
  --header 'Content-Type: multipart/form-data'
  --form first_name=
  --form last_name=
  --form email=
  --form contact_number=
  --form avatar=
  --form gender_id=
  --form qualification_id=
  --form specialization=
  --form work_ex_year=
  --form candidate_dob=
  --form profile_updated_on=
  --form current_salary=
  --form salary_expectation=
  --form willing_to_relocate=
  --form current_organization=
  --form current_organization_slug=
  --form current_status=
  --form notice_period=
  --form currency_id=
  --form facebook=
  --form twitter=
  --form linkedin=
  --form github=
  --form xing=
  --form city=
  --form locality=
  --form state=
  --form country=
  --form postal_code=
  --form address=
  --form relevant_experience=
  --form position=
  --form available_from=
  --form salary_type=
  --form source=
  --form language_skills=
  --form skill=
  --form resume=
  --form owner_id=
  --form created_by=
  --form updated_by=
  --form custom_fields=
  --form candidate_summary=
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
  "off_limit_reason": "testing"
}
```
