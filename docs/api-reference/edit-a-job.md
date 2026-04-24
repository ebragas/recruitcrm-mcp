<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/49ab135708b71-edit-a-job -->
<!-- title: Edit a Job | API Endpoints -->

# Edit a Job

**POST** `/v1/jobs/{job}`

Edit a Job.

## Request

Security: Bearer Auth

### Path Parameters

- `job` (string, **required**) — slug of the Job to edit

### Body

Job Object

- `name` (string, optional) — >= 1 characters
- `number_of_openings` (number, optional)
- `company_slug` (number, optional)
- `contact_slug` (number, optional)
- `secondary_contact_slugs` (number, optional)
- `job_description_text` (string, optional) — >= 1 characters
- `job_description_file` (optional) — string<binary>
- `minimum_experience` (number, optional)
- `maximum_experience` (number, optional)
- `salary_type` (number, optional)
- `currency_id` (number, optional)
- `min_annual_salary` (number, optional)
- `max_annual_salary` (number, optional)
- `qualification_id` (number, optional)
- `specialization` (string, optional)
- `job_skill` (string, optional) — >= 1 characters
- `job_type` (number, optional) — `1` \- Part Time, `2` \- Full Time, `3` \- Contract, `4` \- Contract to Permanent (allowed: `1234`)
- `pay_rate` (number, optional)
- `bill_rate` (number, optional)
- `job_category` (string, optional) — >= 1 characters
- `job_status` (number, optional)
- `job_status_comment` (string, optional)
- `city` (string, optional) — >= 1 characters
- `locality` (string, optional) — >= 1 characters
- `state` (string, optional)
- `country` (string, optional) — >= 1 characters
- `address` (string, optional)
- `show_company_logo` (number, optional)
- `job_questions` (string, optional)
- `collaborator_user_ids` (string, optional) — Comma separated user IDs (example: `"1142, 1137"`)
- `collaborator_team_ids` (string, optional) — Comma separated team IDs (example: `"16,17"`)
- `xml_feeds` (object, optional)
- `default` (string, optional) — comma seperated string of default boards ids. (example: `1,2`)
- `custom` (string, optional) — comma seperated string of custom boards ids. (example: `1089,1086`)
- `note_for_candidates` (string, optional) — >= 1 characters
- `owner_id` (integer, optional)
- `created_by` (integer, optional)
- `updated_by` (integer, optional)
- `hiring_pipeline_id` (number, optional)
- `custom_fields` (optional) — array\[object\] >= 1 items
- `field_id` (number, optional)
- `value` (string, optional) — >= 1 characters
- `enable_job_application_form` (number, optional)
- `job_location_type` (number, optional) — `0` \- On-Site, `1` \- Remote, `2` \- Hybrid (allowed: `012`)
- `postal_code` (string, optional)
- `targetcompanies` (string, optional) — Comma separated company slugs (example: `"321az,433dd"`)

## Responses

200

401

422

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
- `slug` (string, optional) — Omit name number\_of\_openings: Omit number\_of\_openings company\_slug: Omit company\_slug contact\_slug: Omit contact\_slug secondary\_contact\_slugs: Omit secondary\_contact\_slugs job\_description\_text: Omit job\_description\_text job\_description\_file: (example: `321az`)
- `Upload` (optional) — minimum\_experience: Omit minimum\_experience maximum\_experience: Omit maximum\_experience salary\_type: Omit salary\_type currency\_id: Omit currency\_id min\_annual\_salary: Omit min\_annual\_salary max\_annual\_salary: Omit max\_annual\_salary qualification\_id: Omit qualification\_id specialization: Omit specialization job\_skill: Omit job\_skill job\_type: Not Set1234 select an option Omit job\_type pay\_rate: Omit pay\_rate bill\_rate: Omit bill\_rate job\_category: Omit job\_category job\_status: Omit job\_status job\_status\_comment: Omit job\_status\_comment city: Omit city locality: Omit locality state: Omit state country: Omit country address: Omit address show\_company\_logo: Omit show\_company\_logo job\_questions: Omit job\_questions collaborator\_user\_ids: Omit collaborator\_user\_ids collaborator\_team\_ids: Omit collaborator\_team\_ids xml\_feeds: Omit xml\_feeds note\_for\_candidates: Omit note\_for\_candidates owner\_id: Omit owner\_id created\_by: Omit created\_by updated\_by: Omit updated\_by hiring\_pipeline\_id: Omit hiring\_pipeline\_id custom\_fields: Omit custom\_fields enable\_job\_application\_form: Omit enable\_job\_application\_form job\_location\_type: Not Set012 select an option Omit job\_location\_type postal\_code: Omit postal\_code targetcompanies: Omit targetcompanies

#### Example cURL

#### Example cURL

```
curl --request POST \
  --url https://api.recruitcrm.io/v1/jobs/{job} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: multipart/form-data' \
  --form name= \
  --form number_of_openings= \
  --form company_slug= \
  --form contact_slug= \
  --form secondary_contact_slugs= \
  --form job_description_text= \
  --form job_description_file= \
  --form minimum_experience= \
  --form maximum_experience= \
  --form salary_type= \
  --form currency_id= \
  --form min_annual_salary= \
  --form max_annual_salary= \
  --form qualification_id= \
  --form specialization= \
  --form job_skill= \
  --form job_type= \
  --form pay_rate= \
  --form bill_rate= \
  --form job_category= \
  --form job_status= \
  --form job_status_comment= \
  --form city= \
  --form locality= \
  --form state= \
  --form country= \
  --form address= \
  --form show_company_logo= \
  --form job_questions= \
  --form collaborator_user_ids= \
  --form collaborator_team_ids= \
  --form xml_feeds= \
  --form note_for_candidates= \
  --form owner_id= \
  --form created_by= \
  --form updated_by= \
  --form hiring_pipeline_id= \
  --form custom_fields= \
  --form enable_job_application_form= \
  --form job_location_type= \
  --form postal_code= \
  --form targetcompanies=
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
