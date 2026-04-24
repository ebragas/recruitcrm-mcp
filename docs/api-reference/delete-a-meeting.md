<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/e38c71140f311-delete-a-meeting -->
<!-- title: Delete a meeting | API Endpoints -->

# Delete a meeting

**DELETE** `/v1/meetings/{meeting}`

Delete a meeting.

## Request

Security: Bearer Auth

### Path Parameters

- `meeting` (integer, **required**) — ID of the meeting to delete

## Responses

200

401

404

#### Example cURL

#### Example cURL

```
curl --request DELETE \
  --url https://api.recruitcrm.io/v1/meetings/{meeting} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json'
```
