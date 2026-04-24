<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/4b70def51b76b-find-job-by-slug -->
<!-- title: Find job by slug | API Endpoints -->

# Find job by slug

**GET** `/v1/jobs/{job}`

Returns a single job

## Request

Security: Bearer Auth

### Path Parameters

- `job` (string, **required**) — slug of the job to return

## Responses

200

404

### Body

- `id` (integer, optional) — Job's ID (example: `2`)
- `name` (string, optional) — Job's Name (example: `ReactJs Developer`)
- `slug` (string, optional) — Job's slug (example: `121`)
- `company_slug` (string, optional) — Associated company's slug (example: `111`)
- `contact_slug` (string, optional) — Associated contact's slug (example: `222`)
- `secondary_contact_slugs` (optional) — array\[string\] Secondary contact's slug (example: `\["333","444"\]`)
- `note_for_candidates` (string, optional) — Note For Candidates (example: `Please bring all original documents`)
- `number_of_openings` (integer, optional) — Number of openings (example: `4`)
- `minimum_experience` (integer, optional) — Minimum Experience in Year (example: `3`)
- `maximum_experience` (integer, optional) — Maximum Experience in Year (example: `6`)
- `min_annual_salary` (integer, optional) — Minimum Annual Salary (example: `500000`)
- `max_annual_salary` (integer, optional) — Maximum Annual Salary (example: `800000`)
- `job_status` (object, optional) — Object of Job Status Details (example: `{"id":1,"label":"Open"}`)
- `job_status_comment` (string, optional) — Comment on job status
- `latitude` (string, optional) — Latitude of address
- `longitude` (string, optional) — Longitude of address
- `job_skill` (string, optional) — Skills associated to the job (example: `Html, Javascript, CSS`)
- `job_type` (number, optional) — `1` \- Part Time, `2` \- Full Time, `3` \- Contract, `4` \- Contract to Permanent (example: `1`; allowed: `1234`)
- `pay_rate` (number, optional)
- `bill_rate` (number, optional)
- `job_category` (string, optional) — Category of the Job >= 1 characters (example: `Administration`)
- `city` (string, optional) — City of the Job Location (example: `New York`)
- `locality` (string, optional) — Locality of the Job Location (example: `Manhattan`)
- `country` (string, optional) — Country of the Job Location (example: `state`)
- `string` (optional) — State of the Job Location (example: `address`)
- `string` (optional) — Address of the Job Location (example: `enable\_job\_application\_form`)
- `integer` (optional) — Enable Job Application Form
- `job_code` (string, optional) — Unique Job Code
- `show_company_logo` (integer, optional) — Show Company Logo
- `specialization` (string, optional) — Qualification specialization
- `qualification_id` (integer, optional) — Qualification ID
- `job_description_text` (string, optional) — Job Description Text
- `job_description_file` (string, optional) — Job Description File Details
- `job_location_type` (number, optional) — `0` \- On-Site, `1` \- Remote, `2` \- Hybrid (example: `1`; allowed: `012`)
- `postal_code` (string, optional) — Postal Code of the job (example: `110001`)
- `currency_id` (integer, optional) — Currency of the job (example: `2`)
- `job_questions` (optional) — array\[object\] Array of questions of candidate (example: `\[{"id":1,"question":"What is Expected CTC?"}\]`)
- `id` (integer, optional) — ID for question (example: `4`)
- `question` (string, optional) — Question Text.
- `custom_fields` (optional) — array\[object\] Array of Custom Fields (example: `\[{"field\_id":1,"value":"Region 1"}\]`)
- `field_id` (integer, optional) — Field ID
- `value` (string, optional) — Custom Value
- `hiring_pipeline_id` (integer, optional) — Hiring Pipeline Associated With The Job (example: `1`)
- `salary_type` (string, optional) — Salary Type (example: `Annual`)
- `job_posting_status` (string, optional) — Job Posting Status
- `collaborator_users` (optional) — array\[object\] Array of user collaborators
- `id` (integer, optional) — User ID (example: `34`)
- `first_name` (string, optional) — User's First Name (example: `Jane`)
- `last_name` (string, optional) — User's Last Name (example: `Scott`)
- `email` (string, optional) — User's Email (example: `jane.scott@gmail.com`)
- `contact_number` (string, optional) — User's contact\_number
- `avatar` (string, optional) — User's avatar link
- `collaborator_teams` (optional) — array\[object\] Array of team collaborators
- `team_id` (integer, optional) — Team ID (example: `16`)
- `team_name` (string, optional) — Team Name (example: `team1`)
- `xml_feeds` (optional) — array\[object\] Array of XML Feeds
- `id` (integer, optional) — Jobboard ID (example: `1`)
- `type` (string, optional) — Type Of Jobboard (example: `custom`)
- `label` (string, optional) — Label Of Jobboard (example: `Indeed`)
- `application_form_url` (string, optional) — Application form Url
- `shared_job_image` (string, optional) — Shared Job Image
- `created_on` (string, optional) — Created On (example: `2022-11-02T16:49:29.000000Z`)
- `created_by` (string, optional) — Created By (example: `120024`)
- `updated_on` (string, optional) — Updated On (example: `2022-11-02T16:49:29.000000Z`)
- `updated_by` (string, optional) — Updated By (example: `120024`)
- `owner` (string, optional)
- `Owner` (optional) (example: `13223`)
- `targetcompanies` (optional) — array\[object\] Array Of Target Companies
- `name` (string, optional) (example: `Dunder Mifflin`)
- `slug` (string, optional) (example: `321az`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/jobs/{job} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "id": 2,
  "name": "ReactJs Developer",
  "slug": "121",
  "company_slug": "111",
  "contact_slug": "222",
  "secondary_contact_slugs": [
    "333",
    "444"
  ],
  "note_for_candidates": "Please bring all original documents",
  "number_of_openings": 4,
  "minimum_experience": 3,
  "maximum_experience": 6,
  "min_annual_salary": 500000,
  "max_annual_salary": 800000,
  "job_status": {
    "id": 1,
    "label": "Open"
  },
  "job_status_comment": "string",
  "latitude": "string",
  "longitude": "string",
  "job_skill": "Html, Javascript, CSS",
  "job_type": 1,
  "pay_rate": 0,
  "bill_rate": 0,
  "job_category": "Administration",
  "city": "New York",
  "locality": "Manhattan",
  "country": "",
  "state": "",
  "address": "",
  "enable_job_application_form": 0,
  "job_code": "string",
  "show_company_logo": 0,
  "specialization": "string",
  "qualification_id": 0,
  "job_description_text": "string",
  "job_description_file": "string",
  "job_location_type": "0",
  "postal_code": "110001",
  "currency_id": 2,
  "job_questions": [
    {
      "id": 1,
      "question": "What is Expected CTC?"
    }
  ],
  "custom_fields": [
    {
      "field_id": 1,
      "value": "Region 1"
    }
  ],
  "hiring_pipeline_id": 1,
  "salary_type": "Annual",
  "job_posting_status": "string",
  "collaborator_users": [
    {
      "id": 34,
      "first_name": "Jane",
      "last_name": "Scott",
      "email": "jane.scott@gmail.com",
      "contact_number": "string",
      "avatar": "string"
    }
  ],
  "collaborator_teams": [
    null
  ],
  "xml_feeds": [
    null
  ],
  "application_form_url": "string",
  "shared_job_image": "string",
  "created_on": "2022-11-02T16:49:29.000000Z",
  "created_by": "120024",
  "updated_on": "2022-11-02T16:49:29.000000Z",
  "updated_by": "120024",
  "owner": "13223",
  "targetcompanies": [
    {
      "name": "Dunder Mifflin",
      "slug": "321az"
    }
  ]
}
```
