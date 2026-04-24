<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/8f10f7e8902f2-find-subscription-by-id -->
<!-- title: Find subscription by ID | API Endpoints -->

# Find subscription by ID

**GET** `/v1/subscriptions/{subscription}`

Returns a single subscription

## Request

Security: Bearer Auth

### Path Parameters

- `subscription` (integer, **required**) — ID of the subscription

## Responses

200

404

### Body

- `id` (integer, optional) — Subscription ID (example: `56`)
- `event` (string, optional) — Name of Subscribed Event (example: `candidate.created`)
- `target_url` (string, optional) — Subscription URL (example: `https://someurl`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/subscriptions/{subscription} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "id": 56,
  "event": "candidate.created",
  "target_url": "https://someurl"
}
```
