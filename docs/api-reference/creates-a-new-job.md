<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/14816ef96a63a-creates-a-new-job -->
<!-- title: Creates a new Job | API Endpoints -->

# Creates a new Job

**POST** `/v1/jobs`

Creates a new Job.

## Request

Security: Bearer Auth

### Body

Job Object

- `name` (string, **required**) — >= 1 characters
- `job_status` (number, optional) — `0` \- Closed Job, `1` \- Open Job, `2` \- On-Hold Job, `3` \- Cancelled Job, `Custom Id` \- Custom Job Status
- `number_of_openings` (number, **required**)
- `company_slug` (number, **required**)
- `contact_slug` (number, **required**)
- `secondary_contact_slugs` (number, optional)
- `job_description_text` (string, **required**) — >= 1 characters
- `job_description_file` (optional) — string<binary>
- `minimum_experience` (number, optional)
- `maximum_experience` (number, optional)
- `salary_type` (number, optional)
- `currency_id` (number, **required**)
- `min_annual_salary` (number, optional)
- `max_annual_salary` (number, optional)
- `qualification_id` (number, optional)
- `specialization` (string, optional)
- `job_skill` (string, optional) — >= 1 characters
- `job_type` (number, optional) — `1` \- Part Time, `2` \- Full Time, `3` \- Contract, `4` \- Contract to Permanent (allowed: `1234`)
- `pay_rate` (number, optional)
- `bill_rate` (number, optional)
- `job_category` (string, optional) — >= 1 characters
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
- `enable_auto_populate_teams` (boolean, optional) — Providing '1' as value will include all teams of the user provided in created\_by, if added; otherwise, it will include teams of the account owner, unless explicitly provided in collaborator\_team\_ids
- `note_for_candidates` (string, optional) — >= 1 characters
- `owner_id` (integer, optional)
- `created_by` (integer, optional)
- `updated_by` (integer, optional)
- `custom_fields` (optional) — array\[object\] >= 1 items
- `field_id` (number, optional)
- `value` (string, optional) — >= 1 characters
- `enable_job_application_form` (number, **required**)
- `hiring_pipeline_id` (number, optional)
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
- `slug` (string, optional) (example: `321az`)
- `company` (object, optional) — Object of Company Details
- `id` (integer, optional) — Company's ID (example: `2`)
- `industry_id` (integer, optional) — Company's industry ID
- `company_name` (string, optional) — Name of the company (example: `Recruit CRM`)
- `about_company` (string, optional) — <= 5000 characters
- `logo` (string, optional) — Company's Logo URL
- `slug` (string, optional) — Company's slug
- `created_on` (string, optional) — Created On (example: `2020-06-29T05:36:22.000000Z`)
- `updated_on` (string, optional) — Updated On (example: `2020-06-29T05:36:22.000000Z`)
- `website` (string, optional) — Website URL of the company (example: `https://www.recruitcrm.io`)
- `city` (string, optional) — City of the company (example: `New York`)
- `locality` (string, optional) — Locality of the company (example: `Manhattan`)
- `state` (string, optional) — State of the company (example: `New York`)
- `country` (string, optional) — Country of the company (example: `United States`)
- `postal_code` (string, optional) — Postal Code of the company (example: `110001`)
- `address` (string, optional) — Address of the company (example: `facebook`)
- `string` (optional) — Facebook Profile URL of the company (example: `https://www.facebook.com/recruitcrm.io/`)
- `twitter` (string, optional) — Twitter Profile URL of the company (example: `https://www.twitter.com/CrmRecruit/`)
- `linkedin` (string, optional) — Linked In Profile URL of the company (example: `https://www.linkedin.com/company/recruitcrm/`)
- `custom_fields` (optional) — array\[object\] Array of Custom Fields (example: `\[{"field\_id":1,"value":"Region 1"}\]`)
- `created_by` (string, optional) — Created By (example: `213245`)
- `updated_by` (string, optional) — Updated By (example: `123443`)
- `owner` (string, optional)
- `Owner` (optional) (example: `100023`)
- `resource_url` (string, optional) — Resource Url
- `is_child_company` (string, optional) — Whether it is a child company. (example: `Yes`)
- `is_parent_company` (string, optional) — Whether it is a parent company. (example: `No`)
- `child_company_slugs` (optional) — array\[string\] Array containing all company slugs.
- `parent_company_slug` (string, optional) — Parent company slug.
- `last_meeting_created_on` (string, optional) — Last meeting added date (example: `2024-06-05T15:15:00.000000Z`)
- `last_meeting_created_by` (integer, optional) — Updated By user details (example: `5`)
- `status_label` (string, optional) — Off Limit Status (example: `Unavailable`)
- `off_limit_end_date` (string, optional) — Off Limit End Date (example: `2020-06-29T05:36:22.000000Z`)
- `off_limit_reason` (string, optional) — Off Limit Reason (example: `testing`)
- `contact` (object, optional) — Object of Contact Details
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
- `secondary_contacts` (optional) — array\[object\] Array of Secondary Contacts (example: `\[{"id":1,"first\_name":"John","last\_name":"Doe"}\]`)
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
- `currency` (object, optional) — Object of Currency Details
- `currency_id` (integer, optional) — Currency ID (example: `2`)
- `code` (string, optional) — Currency Code (example: `INR`)
- `country` (string, optional) — Currency Country (example: `India`)
- `currency` (string, optional)
- `Currency` (optional) (example: `Rupees`)
- `symbol` (string, optional) — Currency symbol (example: `₹`)
- `industry` (object, optional) — Object of Industry Details
- `industry_id` (integer, optional) — Industry ID (example: `6`)
- `label` (string, optional) — Industry Label Omit job\_status number\_of\_openings\*: company\_slug\*: contact\_slug\*: secondary\_contact\_slugs: Omit secondary\_contact\_slugs job\_description\_text\*: job\_description\_file: (example: `Apparel and Fashion`)
- `Upload` (optional) — minimum\_experience: Omit minimum\_experience maximum\_experience: Omit maximum\_experience salary\_type: Omit salary\_type currency\_id\*: min\_annual\_salary: Omit min\_annual\_salary max\_annual\_salary: Omit max\_annual\_salary qualification\_id: Omit qualification\_id specialization: Omit specialization job\_skill: Omit job\_skill job\_type: Not Set1234 select an option Omit job\_type pay\_rate: Omit pay\_rate bill\_rate: Omit bill\_rate job\_category: Omit job\_category city: Omit city locality: Omit locality state: Omit state country: Omit country address: Omit address show\_company\_logo: Omit show\_company\_logo job\_questions: Omit job\_questions collaborator\_user\_ids: Omit collaborator\_user\_ids collaborator\_team\_ids: Omit collaborator\_team\_ids xml\_feeds: Omit xml\_feeds enable\_auto\_populate\_teams: Omit enable\_auto\_populate\_teams note\_for\_candidates: Omit note\_for\_candidates owner\_id: Omit owner\_id created\_by: Omit created\_by updated\_by: Omit updated\_by custom\_fields: Omit custom\_fields enable\_job\_application\_form\*: hiring\_pipeline\_id: Omit hiring\_pipeline\_id job\_location\_type: Not Set012 select an option Omit job\_location\_type postal\_code: Omit postal\_code targetcompanies: Omit targetcompanies

#### Example cURL

#### Example cURL

```
curl --request POST \
  --url https://api.recruitcrm.io/v1/jobs \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: multipart/form-data' \
  --form name= \
  --form job_status= \
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
  --form enable_auto_populate_teams= \
  --form note_for_candidates= \
  --form owner_id= \
  --form created_by= \
  --form updated_by= \
  --form custom_fields= \
  --form enable_job_application_form= \
  --form hiring_pipeline_id= \
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
  ],
  "company": {
    "id": 2,
    "industry_id": 0,
    "company_name": "Recruit CRM",
    "about_company": "string",
    "logo": "string",
    "slug": "string",
    "created_on": "2020-06-29T05:36:22.000000Z",
    "updated_on": "2020-06-29T05:36:22.000000Z",
    "website": "https://www.recruitcrm.io",
    "city": "New York",
    "locality": "Manhattan",
    "state": "New York",
    "country": "United States",
    "postal_code": "110001",
    "address": "",
    "facebook": "https://www.facebook.com/recruitcrm.io/",
    "twitter": "https://www.twitter.com/CrmRecruit/",
    "linkedin": "https://www.linkedin.com/company/recruitcrm/",
    "custom_fields": [
      {
        "field_id": 1,
        "value": "Region 1"
      }
    ],
    "created_by": "213245",
    "updated_by": "123443",
    "owner": "100023",
    "resource_url": "string",
    "is_child_company": "Yes",
    "is_parent_company": "No",
    "child_company_slugs": [
      "17370009412IEv"
    ],
    "parent_company_slug": "string",
    "last_meeting_created_on": "2024-06-05T15:15:00.000000Z",
    "last_meeting_created_by": 5,
    "status_label": "Unavailable",
    "off_limit_end_date": "2020-06-29T05:36:22.000000Z",
    "off_limit_reason": "testing"
  },
  "contact": {
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
  "secondary_contacts": [
    {
      "id": 1,
      "first_name": "John",
      "last_name": "Doe"
    }
  ],
  "currency": {
    "currency_id": 2,
    "code": "INR",
    "country": "India",
    "currency": "Rupees",
    "symbol": "₹"
  },
  "industry": {
    "industry_id": 6,
    "label": "Apparel and Fashion"
  }
}
```
