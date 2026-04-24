<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/5863f623339b9-delete-a-subscription -->
<!-- title: Delete a subscription | API Endpoints -->

# Delete a subscription

**DELETE** `/v1/subscriptions/{subscription}`

Delete a subscription.

## Request

Security: Bearer Auth

### Path Parameters

- `subscription` (integer, **required**) — ID of the subscription to delete

## Responses

200

401

404

#### Example cURL

#### Example cURL

```
curl --request DELETE \
  --url https://api.recruitcrm.io/v1/subscriptions/{subscription} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json'
```
