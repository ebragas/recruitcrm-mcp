<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/db65ebd396436-delete-a-candidate -->
<!-- title: Delete a candidate | API Endpoints -->

# Delete a candidate

**DELETE** `/v1/candidates/{candidate}`

Delete a candidate.

## Request

Security: Bearer Auth

### Path Parameters

- `candidate` (string, **required**) — slug of the candidate to delete

## Responses

200

401

404

#### Example cURL

#### Example cURL

```
curl --request DELETE \
  --url https://api.recruitcrm.io/v1/candidates/{candidate} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json'
```
