<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/2b0049787b7e1-delete-a-hotlist -->
<!-- title: Delete a hotlist | API Endpoints -->

# Delete a hotlist

**DELETE** `/v1/hotlists/{hotlist}`

Delete a hotlist.

## Request

Security: Bearer Auth

### Path Parameters

- `hotlist` (integer, **required**) — ID of the hotlist to delete

## Responses

200

401

404

#### Example cURL

#### Example cURL

```
curl --request DELETE \
  --url https://api.recruitcrm.io/v1/hotlists/{hotlist} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json'
```
