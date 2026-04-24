<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/b77b5f8d6d188-edit-work-experience -->
<!-- title: Edit Work Experience | API Endpoints -->

# Edit Work Experience

**POST** `/v1/candidates/work-history/{workId}`

Update a Candidate Work Experience.

## Request

Security: Bearer Auth

### Path Parameters

- `workId` (integer, **required**) — ID of the work experience

### Body

Candidate Work Experience Object

- `title` (string, optional)
- `Position` (optional) (example: `Director`)
- `employment_type` (integer, optional) — 1: Part Time, 2: Full Time, 3: Contract,4: Self-employed,5: Internship,6: Apprenticeship, 7: Freelance (example: `1`)
- `industry_id` (integer, optional) — Industry ID (example: `6`)
- `salary` (number, optional)
- `Salary` (optional) (example: `150000`)
- `is_currently_working` (integer, optional) — 0: No,1: Yes (example: `0`)
- `work_start_date` (integer, optional) — Work Start Date
- `work_end_date` (integer, optional) — Last Working Date
- `work_description` (string, optional) — Work Description

## Responses

200

401

422

### Body

- `id` (integer, optional) — Work ID
- `title` (string, optional)
- `Position` (optional) (example: `Director`)
- `employment_type` (integer, optional) — 1: Part Time, 2: Full Time, 3: Contract,4: Self-employed,5: Internship,6: Apprenticeship, 7: Freelance (example: `1`)
- `industry_id` (integer, optional) — Industry ID (example: `6`)
- `salary` (number, optional)
- `Salary` (optional) (example: `150000`)
- `is_currently_working` (integer, optional) — 0: No,1: Yes (example: `0`)
- `work_start_date` (integer, optional) — Work Start Date (example: `1585123200`)
- `work_end_date` (integer, optional) — Last Working Date
- `work_description` (string, optional) — Work Description (example: `Worked as a Director`)
- `candidate_slug` (string, optional) — Candidate's Slug (example: `275`)
- `candidate_id` (integer, optional) — Candidate's ID (example: `275`)
- `is_manually_added` (integer, optional) — Is Manually Added (example: `1`)
- `work_company_name` (string, optional) — Work Company Name (example: `ABC Company`)
- `work_location` (string, optional) — Work Location (example: `NY`)
- `created_by` (integer, optional) — ID of Created By User (example: `10002`)
- `updated_by` (integer, optional) — ID of Updated By User (example: `10002`)
- `created_on` (string, optional) — Created On (example: `2022-12-02T16:53:27.000000Z`)
- `updated_on` (string, optional) — Updated On (example: `2022-12-02T16:53:27.000000Z`)

#### Example request body

#### Example request body

```
{
  "title": "Software Developer",
  "work_company_name": "Recruit CRM",
  "employment_type": 2,
  "industry_id": 3,
  "work_location": "New York",
  "salary": 150090,
  "is_currently_working": 0,
  "work_start_date": 1603684640,
  "work_end_date": 1603684678,
  "work_description": "Supervised a team of 9 employees in all technical and creative aspects of digital advertising campaigns with budgets over $300,000."
}
```

#### Example cURL

#### Example cURL

```
curl --request POST \
  --url https://api.recruitcrm.io/v1/candidates/work-history/{workId} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json' \
  --data '{
  "title": "Software Developer",
  "work_company_name": "Recruit CRM",
  "employment_type": 2,
  "industry_id": 3,
  "work_location": "New York",
  "salary": 150090,
  "is_currently_working": 0,
  "work_start_date": 1603684640,
  "work_end_date": 1603684678,
  "work_description": "Supervised a team of 9 employees in all technical and creative aspects of digital advertising campaigns with budgets over $300,000."
}'
```

#### Example response

#### Example response

```
{
  "id": 0,
  "title": "Director",
  "employment_type": 1,
  "industry_id": 6,
  "salary": 150000,
  "is_currently_working": 0,
  "work_start_date": 1585123200,
  "work_end_date": 0,
  "work_description": "Worked as a Director",
  "candidate_slug": "275",
  "candidate_id": 275,
  "is_manually_added": 1,
  "work_company_name": "ABC Company",
  "work_location": "NY",
  "created_by": 10002,
  "updated_by": 10002,
  "created_on": "2022-12-02T16:53:27.000000Z",
  "updated_on": "2022-12-02T16:53:27.000000Z"
}
```
