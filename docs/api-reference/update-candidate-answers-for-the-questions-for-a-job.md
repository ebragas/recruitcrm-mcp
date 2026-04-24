<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/c17faa0f72c3a-update-candidate-answers-for-the-questions-for-a-job -->
<!-- title: Update Candidate Answers for the Questions for a Job | API Endpoints -->

# Update Candidate Answers for the Questions for a Job

**POST** `/v1/candidates/question-and-answers/{candidate}/{job}`

Update a candidate's answer for a question related to a job.

## Request

Security: Bearer Auth

### Path Parameters

- `candidate` (integer, **required**) — Slug of the candidate
- `job` (integer, **required**) — Slug of the job

### Body

Array of objects for Candidate Question and Answer

- `question_answers` (optional) — array\[object\]
- `question_id` (number, optional) — Question ID (example: `1`)
- `answer` (string, optional)
- `Answer` (optional) (example: `I'm from India.`)

## Responses

200

404

### Body

- `success` (boolean, optional) (example: `true`)
- `successCode` (number, optional) — Success Code (example: `200`)
- `message` (string, optional) — Success Message (example: `Answer updated successfully`)
- `job_id` (number, optional) — Job ID (example: `1`)
- `job_name` (string, optional) — Job Name (example: `Full Stack Developer`)
- `data` (optional) — array\[object\]
- `answer_id` (number, optional) — Answer ID (example: `1`)
- `answer` (string, optional)
- `Answer` (optional) (example: `I'm from India.`)
- `question_id` (number, optional) — Question ID (example: `1`)
- `question` (string, optional)
- `Question` (optional) (example: `Where are you from?`)

#### Example request body

#### Example request body

```
{
  "question_answers": [
    {
      "question_id": 1,
      "answer": "I'm from India."
    }
  ]
}
```

#### Example cURL

#### Example cURL

```
curl --request POST \
  --url https://api.recruitcrm.io/v1/candidates/question-and-answers/{candidate}/{job} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json' \
  --data '{
  "question_answers": [\
    {\
      "question_id": 1,\
      "answer": "I'\''m from India."\
    }\
  ]
}'
```

#### Example response

#### Example response

```
{
  "success": true,
  "successCode": 200,
  "message": "Answer updated successfully",
  "job_id": 1,
  "job_name": "Full Stack Developer",
  "data": [
    {
      "answer_id": 1,
      "answer": "I'm from India.",
      "question_id": 1,
      "question": "Where are you from?"
    }
  ]
}
```
