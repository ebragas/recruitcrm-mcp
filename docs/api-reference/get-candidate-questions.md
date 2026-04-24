<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/388c00ec02e26-get-candidate-questions -->
<!-- title: Get Candidate Questions | API Endpoints -->

# Get Candidate Questions

**GET** `/v1/candidate-questions`

Returns a list of candidate questions

## Request

Security: Bearer Auth

## Responses

200

401

### Body

- `id` (integer, optional) — ID for question (example: `4`)
- `question` (string, optional) — Question Text.

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/candidate-questions \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "id": 4,
  "question": "string"
}
```
