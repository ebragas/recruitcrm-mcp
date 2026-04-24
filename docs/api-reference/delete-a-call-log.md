<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/2ca613934cdb2-delete-a-call-log -->
<!-- title: Delete a call log | API Endpoints -->

# Delete a call log

**DELETE** `/v1/call-logs/{call\_log}`

Delete a call log.

## Request

Security: Bearer Auth

### Path Parameters

- `call_log` (integer, **required**) — ID of the call log to delete

## Responses

200

401

404

#### Example cURL

#### Example cURL

```
curl --request DELETE \
  --url https://api.recruitcrm.io/v1/call-logs/{call_log} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json'
```
