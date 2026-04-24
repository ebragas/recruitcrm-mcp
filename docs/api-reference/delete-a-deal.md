<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/db2609e77ca90-delete-a-deal -->
<!-- title: Delete a deal | API Endpoints -->

# Delete a deal

**DELETE** `/v1/deals/{deal}`

Delete a deal.

## Request

Security: Bearer Auth

### Path Parameters

- `deal` (string, **required**) — slug of the deal to delete

## Responses

200

401

404

#### Example cURL

#### Example cURL

```
curl --request DELETE \
  --url https://api.recruitcrm.io/v1/deals/{deal} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json'
```
