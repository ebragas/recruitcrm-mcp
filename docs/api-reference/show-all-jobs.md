<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/5c88c1dfb7ee9-show-all-jobs -->
<!-- title: Show all Jobs | API Endpoints -->

# Show all Jobs

**GET** `/v1/jobs`

Returns all jobs associated with your account.

## Request

Security: Bearer Auth

### Query Parameters

- `limit` (integer, optional) — Limit of records per page. (Max:100)
- `page` (integer, optional) — Page Number for Pagination
- `sort_by` (string, optional) — Sort by field (allowed: `createdonupdatedon`; default: `updatedon`)
- `sort_order` (string, optional) — Sort order (allowed: `ascdesc`; default: `desc`)

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
- `last_page` (integer, optional) — Last page number (example: `1`)
- `total` (integer, optional) — Total records (example: `25`)
- `last_page_url` (string, optional) — URL of the last page (example: `null`)
- `data` (optional) — array\[object\]
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
- `custom_fields` (optional) — array\[object\] Array of Custom Fields (example: `\[{"field\_id":1,"value":"Region 1"}\]`)
- `hiring_pipeline_id` (integer, optional) — Hiring Pipeline Associated With The Job (example: `1`)
- `salary_type` (string, optional) — Salary Type (example: `Annual`)
- `job_posting_status` (string, optional) — Job Posting Status
- `collaborator_users` (optional) — array\[object\] Array of user collaborators
- `collaborator_teams` (optional) — array\[object\] Array of team collaborators
- `xml_feeds` (optional) — array\[object\] Array of XML Feeds
- `application_form_url` (string, optional) — Application form Url
- `shared_job_image` (string, optional) — Shared Job Image
- `created_on` (string, optional) — Created On (example: `2022-11-02T16:49:29.000000Z`)
- `created_by` (string, optional) — Created By (example: `120024`)
- `updated_on` (string, optional) — Updated On (example: `2022-11-02T16:49:29.000000Z`)
- `updated_by` (string, optional) — Updated By (example: `120024`)
- `owner` (string, optional)
- `Owner` (optional) (example: `13223`)
- `targetcompanies` (optional) — array\[object\] Array Of Target Companies Not Setcreatedonupdatedon select an option (defaults to: updatedon) sort\_order: Not Setascdesc select an option (defaults to: desc)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/jobs \
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
  "last_page": 1,
  "total": 25,
  "last_page_url": "null",
  "data": [
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
      "job_location_type": "1",
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
  ]
}
```
