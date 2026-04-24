<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/41fe1304c8d33-delete-a-candidate-work-experience -->
<!-- title: Delete a candidate work experience | API Endpoints -->

# Delete a candidate work experience

**DELETE** `/v1/candidates/work-history/{workId}`

Delete a Candidate Work Experience.

## Request

Security: Bearer Auth

### Path Parameters

- `workId` (integer, **required**) — ID of the work experience

## Responses

200

401

404

Work experience deleted successfully.

### Body

- `success` (boolean, optional) (example: `true`)
- `statusCode` (string, optional) — Status Code (example: `200`)
- `message` (string, optional) — Success Message (example: `Work experience deleted successfully.`)

#### Example cURL

#### Example cURL

```
curl --request DELETE \
  --url https://api.recruitcrm.io/v1/candidates/work-history/{workId} \
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
  "message": "Work experience deleted successfully."
}
```
