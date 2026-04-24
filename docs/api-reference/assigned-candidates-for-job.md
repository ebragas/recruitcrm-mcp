<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/6388403858e87-assigned-candidates-for-job -->
<!-- title: Assigned candidates for job | API Endpoints -->

# Assigned candidates for job

**GET** `/v1/jobs/{job}/assigned-candidates`

Return list of assigned candidates for requested job

## Request

Security: Bearer Auth

### Path Parameters

- `job` (string, **required**) — slug of the job to return

### Query Parameters

- `limit` (integer, optional) — Limit of records per page. (Max:100)
- `page` (integer, optional) — Page number for records
- `status_id` (integer, optional) — Hiring Stage Id (Supports single or comma-separated values) (example: `1243,2813`)

## Responses

200

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
- `candidate` (object, optional)
- `stage_date` (string, optional) — Stage Date (example: `2026-02-20T09:08:45.000000Z`)
- `status` (object, optional) — Candidate's status (example: `{"status\_id":1,"label":"Assigned"}`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/jobs/{job}/assigned-candidates \
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
      "candidate": {
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
        "email_opt_out_source": "Manually opted out"
      },
      "stage_date": "2026-02-20T09:08:45.000000Z",
      "status": {
        "status_id": 1,
        "label": "Assigned"
      }
    }
  ]
}
```
