<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/19a44c9ebff68-update-candidate-answers-for-the-questions -->
<!-- title: Update Candidate Answers for the Questions | API Endpoints -->

# Update Candidate Answers for the Questions

**POST** `/v1/candidates/question-and-answers/{candidate}`

Update a candidate's answer for a question.

## Request

Security: Bearer Auth

### Path Parameters

- `candidate` (string, **required**) — slug of the candidate

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
- `statusCode` (number, optional) — Success Code (example: `200`)
- `message` (string, optional) — Success Message (example: `Answer updated successfully`)
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
  --url https://api.recruitcrm.io/v1/candidates/question-and-answers/{candidate} \
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
  "statusCode": 200,
  "message": "Answer updated successfully",
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
