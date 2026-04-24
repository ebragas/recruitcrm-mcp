<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/415e8b0ffbbae-delete-a-candidate-education-history -->
<!-- title: Delete a candidate Education History | API Endpoints -->

# Delete a candidate Education History

**DELETE** `/v1/candidates/education-history/{educationId}`

Delete a Candidate Education History.

## Request

Security: Bearer Auth

### Path Parameters

- `educationId` (integer, **required**) — ID of the education history

## Responses

200

401

404

Education history deleted successfully.

### Body

- `success` (boolean, optional) (example: `true`)
- `statusCode` (string, optional) — Status Code (example: `200`)
- `message` (string, optional) — Success Message (example: `Education history deleted successfully.`)

#### Example cURL

#### Example cURL

```
curl --request DELETE \
  --url https://api.recruitcrm.io/v1/candidates/education-history/{educationId} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json'
```

#### Example response

#### Example response

```
{
  "success": true,
  "statusCode": "200",
  "message": "Education history deleted successfully."
}
```
