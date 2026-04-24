<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/4e97401ad2234-question-and-answers-of-candidate -->
<!-- title: Question And Answers of Candidate | API Endpoints -->

# Question And Answers of Candidate

**GET** `/v1/candidates/question-and-answers/{candidate}`

Returns a list of all the answered questions which are not related to any job.

## Request

Security: Bearer Auth

### Path Parameters

- `candidate` (string, **required**) — slug of the candidate

### Query Parameters

- `unanswered` (integer, optional) — To get the unanswered questions. Use the value 1 for true, and 0 for false. (allowed: `01`)

## Responses

200

404

### Body

- `success` (boolean, optional) (example: `true`)
- `statusCode` (number, optional) — Success Code (example: `200`)
- `message` (string, optional) — Success Message (example: `Fetched Question and Answer successfully`)
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
  --url https://api.recruitcrm.io/v1/candidates/question-and-answers/{candidate} \
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
