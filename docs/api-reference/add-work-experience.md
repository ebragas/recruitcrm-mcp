<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/e04b27f2d52b6-add-work-experience -->
<!-- title: Add Work Experience | API Endpoints -->

# Add Work Experience

**POST** `/v1/candidates/work-history/create`

Add a Work Experience for Candidate.

## Request

Security: Bearer Auth

### Body

Candidate Work Experience Array of Object

\*\*Note: This endpoint has request limit of 50 records per call.
Also, a candidate can only have 10 Work History.

- `candidate_slug` (string, **required**) — Candidate's Slug
- `title` (string, **required**)
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

404

422

429

Work History added successfully

### Body

- `success` (boolean, optional) (example: `true`)
- `statusCode` (string, optional) — Status Code (example: `200`)
- `message` (string, optional) — Success Message (example: `Work History added successfully.`)

#### Example request body

#### Example request body

```
[
  {
    "candidate_slug": "1234567750000",
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
]
```

#### Example cURL

#### Example cURL

```
curl --request POST \
  --url https://api.recruitcrm.io/v1/candidates/work-history/create \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json' \
  --data '[\
  {\
    "candidate_slug": "1234567750000",\
    "title": "Software Developer",\
    "work_company_name": "Recruit CRM",\
    "employment_type": 2,\
    "industry_id": 3,\
    "work_location": "New York",\
    "salary": 150090,\
    "is_currently_working": 0,\
    "work_start_date": 1603684640,\
    "work_end_date": 1603684678,\
    "work_description": "Supervised a team of 9 employees in all technical and creative aspects of digital advertising campaigns with budgets over $300,000."\
  }\
]'
```

#### Example response

#### Example response

```
{
  "success": true,
  "statusCode": "200",
  "message": "Work History added successfully."
}
```
