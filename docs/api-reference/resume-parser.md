<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/a35e2610e4f9e-resume-parser -->
<!-- title: Resume Parser | API Endpoints -->

# Resume Parser

**POST** `/v1/candidates/resume-parser`

The Resume Parser API allows you to upload a resume (CV) and automatically create or update a candidate in Recruit CRM without providing any additional candidate details.

When a resume is uploaded, the endpoint:

1. Calls Recruit CRM's resume parsing engine
2. Extracts candidate data from the resume
3. Creates a new candidate or updates an existing one based on duplicate handling rules

If certain fields cannot be extracted from the resume (for example, missing email), the response will explicitly return "Not Available" for those fields.

Supported file formats: PDF, DOC, DOCX

**Duplicate Handling**

Duplicate handling is controlled by the Admin-level setting: "Allow Duplicate Candidates".

- If "Allow Duplicate Candidates" is ON: A new candidate is always created, regardless of the override\_data parameter.
- If "Allow Duplicate Candidates" is OFF: The override\_data parameter determines how duplicates are handled:

| override\_data | Behavior |
| --- | --- |
| no | Updates only empty or unavailable fields on the existing candidate |
| yes | Updates existing candidate fields with the newly parsed data |

Duplicate detection is performed using identifiers such as **email, phone number, LinkedIn URL, etc.**

## Request

Security: Bearer Auth

### Body

Upload the resume file along with an optional override\_data parameter. Use Content-Type: multipart/form-data.

- `file` (**required**) — string<binary> Resume file (required). Supported formats: PDF, DOC, DOCX
- `override_data` (string, optional) — Controls how existing candidate data should be handled when a duplicate candidate is detected and Admin setting "Allow Duplicate Candidates" is OFF.Show all... (allowed: `yesno`)

## Responses

200

201

401

422

429

Successful Operation. Returns status (whether the candidate was created or updated), a message, and the full candidate object including parsed work history and education history where applicable.

### Body

Wrapper returned by the Resume Parser API. The candidate object uses the same fields as add/edit candidate responses, with additional parsed data (work history, education history) and resume file metadata where applicable.

- `status` (string, **required**) — Indicates whether a new candidate was created or an existing candidate was updated after parsing (depends on duplicate handling rules). (allowed: `candidate\_createdcandidate\_updated`)
- `message` (string, **required**) — Human-readable outcome of the parse operation. (example: `Resume parsed successfully`)
- `candidate` (object, **required**) — Candidate record returned by Resume Parser. Extends the standard candidate response with parsed resume file details (when returned as an object), work history, and education history arrays.
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
- `resume` (optional)
- `stringobject` (optional) — one of: string Public URL to the resume file (example: `Can be Public URL to file`)
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
- `work_history` (optional) — array\[object\] Work experience entries parsed from the resume.
- `education_history` (optional) — array\[object\] Education entries parsed from the resume.
- `Upload` (optional) — override\_data: Not Setyesno select an option Omit override\_data

#### Example cURL

#### Example cURL

```
curl --request POST \
  --url https://api.recruitcrm.io/v1/candidates/resume-parser \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: multipart/form-data' \
  --form file= \
  --form override_data=
```

CandidateUpdatedCandidateCreated

Response Example: CandidateUpdated

#### Example response

#### Example response

```
{
  "status": "candidate_updated",
  "message": "Resume parsed successfully",
  "candidate": {
    "slug": "17739098284911311610HqI",
    "first_name": "JACOB",
    "last_name": "HANCOCK",
    "resume": {
      "filename": "resume.docx",
      "file_link": "https://api.recruitcrm.io/v1/candidates/example/resume/token"
    }
  }
}
```
