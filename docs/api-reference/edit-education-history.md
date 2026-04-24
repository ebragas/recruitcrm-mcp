<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/1815c56bcbc41-edit-education-history -->
<!-- title: Edit Education History | API Endpoints -->

# Edit Education History

**POST** `/v1/candidates/education-history/{educationId}`

Update a Candidate Education History.

## Request

Security: Bearer Auth

### Path Parameters

- `educationId` (integer, **required**) — ID of the education history

### Body

Candidate Education History Object

- `candidate_slug` (string, optional) — Candidate's Slug
- `institute_name` (string, optional) — Institute Name (example: `Scott Academy`)
- `educational_qualification` (string, optional) — Educational Qualification (example: `Bachelor's Degree`)
- `educational_specialization` (string, optional) — Educational Specialization (example: `Computer Science`)
- `grade` (string, optional) — Academic Grade (example: `A+`)
- `education_location` (string, optional) — Institute Location (example: `NY`)
- `education_start_date` (integer, optional) — Degree Start Date
- `education_end_date` (integer, optional) — Degree End Date
- `education_description` (string, optional) — Description of Degree

## Responses

200

401

422

### Body

- `id` (integer, optional) — Education ID (example: `1`)
- `institute_name` (string, optional) — Institute Name (example: `Scott Academy`)
- `educational_qualification` (string, optional) — Educational Qualification (example: `Bachelor's Degree`)
- `educational_specialization` (string, optional) — Educational Specialization (example: `Computer Science`)
- `grade` (string, optional) — Academic Grade (example: `A+`)
- `education_location` (string, optional) — Institute Location (example: `NY`)
- `education_start_date` (integer, optional) — Degree Start Date (example: `1585123200`)
- `education_end_date` (integer, optional) — Degree End Date (example: `1585123200`)
- `education_description` (string, optional) — Description of Degree (example: `Completed Bachelor's Degree`)
- `candidate_slug` (string, optional) — Candidate's Slug (example: `275`)
- `candidate_id` (integer, optional) — Candidate's ID (example: `275`)
- `created_by` (integer, optional) — ID of Created By User (example: `10002`)
- `updated_by` (integer, optional) — ID of Updated By User (example: `10002`)
- `created_on` (string, optional) — Created On (example: `2022-12-02T16:53:27.000000Z`)
- `updated_on` (string, optional) — Updated On (example: `2022-12-02T16:53:27.000000Z`)
- `is_manually_added` (integer, optional) — Is Manually Added (example: `1`)

#### Example request body

#### Example request body

```
{
  "institute_name": "Scott Academy",
  "educational_qualification": "Bachelor's Degree",
  "educational_specialization": "Computer Science",
  "grade": "A+",
  "education_location": "NY",
  "education_start_date": 1283711400,
  "education_end_date": 1365445800,
  "education_description": "Engineering Degree in Computer Science"
}
```

#### Example cURL

#### Example cURL

```
curl --request POST \
  --url https://api.recruitcrm.io/v1/candidates/education-history/{educationId} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json' \
  --data '{
  "institute_name": "Scott Academy",
  "educational_qualification": "Bachelor'\''s Degree",
  "educational_specialization": "Computer Science",
  "grade": "A+",
  "education_location": "NY",
  "education_start_date": 1283711400,
  "education_end_date": 1365445800,
  "education_description": "Engineering Degree in Computer Science"
}'
```

#### Example response

#### Example response

```
{
  "id": 1,
  "institute_name": "Scott Academy",
  "educational_qualification": "Bachelor's Degree",
  "educational_specialization": "Computer Science",
  "grade": "A+",
  "education_location": "NY",
  "education_start_date": 1585123200,
  "education_end_date": 1585123200,
  "education_description": "Completed Bachelor's Degree",
  "candidate_slug": "275",
  "candidate_id": 275,
  "created_by": 10002,
  "updated_by": 10002,
  "created_on": "2022-12-02T16:53:27.000000Z",
  "updated_on": "2022-12-02T16:53:27.000000Z",
  "is_manually_added": 1
}
```
