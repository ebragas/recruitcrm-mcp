<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/774fc7e38a139-delete-a-job -->
<!-- title: Delete a Job | API Endpoints -->

# Delete a Job

**DELETE** `/v1/jobs/{job}`

Delete a Job.

## Request

Security: Bearer Auth

### Path Parameters

- `job` (string, **required**) — slug of the Job to delete

## Responses

200

401

404

#### Example cURL

#### Example cURL

```
curl --request DELETE \
  --url https://api.recruitcrm.io/v1/jobs/{job} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json'
```
