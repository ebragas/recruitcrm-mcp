<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/9a1dc92f85aee-get-job-associated-fields -->
<!-- title: Get Job Associated Fields | API Endpoints -->

# Get Job Associated Fields

**GET** `/v1/candidates/associated-field/{candidate}/{job}`

Returns a list of all the values of job associated fields for a job.

## Request

Security: Bearer Auth

### Path Parameters

- `candidate` (string, **required**) — slug of the candidate
- `job` (string, **required**) — slug of the job

## Responses

200

404

### Body

- `success` (boolean, optional) (example: `true`)
- `statusCode` (number, optional) — Success Code (example: `200`)
- `message` (string, optional) — Success Message (example: `Job Associated Fields for the job: 'Job Name' for this candidate: 'Candidate Name'`)
- `data` (optional) — array\[object\] 0
- `object` (optional)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/candidates/associated-field/{candidate}/{job} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "success": true,
  "statusCode": 200,
  "message": "Job Associated Fields for the job: 'Job Name' for this candidate: 'Candidate Name'",
  "data": [
    {
      "0": {
        "columnid": 1,
        "label": "Job Associated Field",
        "value": "Value of the field"
      }
    }
  ]
}
```
