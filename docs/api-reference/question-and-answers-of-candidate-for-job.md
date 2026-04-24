<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/87ff1a515a2cf-question-and-answers-of-candidate-for-job -->
<!-- title: Question And Answers of Candidate for Job | API Endpoints -->

# Question And Answers of Candidate for Job

**GET** `/v1/candidates/question-and-answers/{candidate}/{job}`

Returns a list of all the answered questions which are related to the given job.

## Request

Security: Bearer Auth

### Path Parameters

- `candidate` (string, **required**) — slug of the candidate
- `job` (string, **required**) — slug of the job

### Query Parameters

- `unanswered` (integer, optional) — To get the unanswered questions. Use the value 1 for true, and 0 for false. (allowed: `01`)

## Responses

200

404

### Body

- `success` (boolean, optional) (example: `true`)
- `statusCode` (number, optional) — Success Code (example: `200`)
- `message` (string, optional) — Success Message (example: `Fetched Question and Answer successfully`)
- `job_id` (number, optional) — Job ID (example: `1`)
- `job_name` (string, optional) — Job Name (example: `Full Stack Developer`)
- `data` (optional) — array\[object\] Question ID
- `number` (optional) — ID of the Question
- `Question` (string, optional)
- `Question` (optional)
- `Answer` (string, optional)
- `Answer` (optional) — Answer ID
- `number` (optional) — ID of the Answer Not Set01 select an option

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/candidates/question-and-answers/{candidate}/{job} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "success": true,
  "statusCode": 200,
  "message": "Fetched Question and Answer successfully",
  "job_id": 1,
  "job_name": "Full Stack Developer",
  "data": [
    {
      "Question ID": 0,
      "Question": "string",
      "Answer": "string",
      "Answer ID": 0
    }
  ]
}
```
