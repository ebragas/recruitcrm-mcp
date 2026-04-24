<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/d3914e1653285-add-education-history -->
<!-- title: Add Education History | API Endpoints -->

# Add Education History

**POST** `/v1/candidates/education-history/create`

Add a Education History for Candidate.

## Request

Security: Bearer Auth

### Body

Candidate Education History Array of Object

\*\*Note: This endpoint has request limit of 50 records per call.
Also, a candidate can only have 10 Education History.

- `candidate_slug` (string, **required**) — Candidate's Slug
- `institute_name` (string, **required**) — Institute Name (example: `Scott Academy`)
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

404

422

429

Education History added successfully

### Body

- `success` (boolean, optional) (example: `true`)
- `statusCode` (string, optional) — Status Code (example: `200`)
- `message` (string, optional) — Success Message (example: `Education History added successfully.`)

#### Example request body

#### Example request body

```
[
  {
    "candidate_slug": "1234567750000",
    "institute_name": "Scott Academy",
    "educational_qualification": "Bachelor's Degree",
    "educational_specialization": "Computer Science",
    "grade": "A+",
    "education_location": "NY",
    "education_start_date": 1283711400,
    "education_end_date": 1365445800,
    "education_description": "Engineering Degree in Computer Science"
  }
]
```

#### Example cURL

#### Example cURL

```
curl --request POST \
  --url https://api.recruitcrm.io/v1/candidates/education-history/create \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json' \
  --data '[\
  {\
    "candidate_slug": "1234567750000",\
    "institute_name": "Scott Academy",\
    "educational_qualification": "Bachelor'\''s Degree",\
    "educational_specialization": "Computer Science",\
    "grade": "A+",\
    "education_location": "NY",\
    "education_start_date": 1283711400,\
    "education_end_date": 1365445800,\
    "education_description": "Engineering Degree in Computer Science"\
  }\
]'
```

#### Example response

#### Example response

```
{
  "success": true,
  "statusCode": "200",
  "message": "Education History added successfully."
}
```
