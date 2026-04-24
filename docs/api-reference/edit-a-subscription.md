<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/4bc67137d9961-edit-a-subscription -->
<!-- title: Edit a subscription | API Endpoints -->

# Edit a subscription

**POST** `/v1/subscriptions/{subscription}`

Edit a subscription.

## Request

Security: Bearer Auth

### Path Parameters

- `subscription` (integer, **required**) — ID of the subscription to edit

### Body

Subscription Object

- `id` (integer, optional) — Subscription ID (example: `56`)
- `event` (string, optional) — Name of Subscribed Event (example: `candidate.created`)
- `target_url` (string, optional) — Subscription URL (example: `https://someurl`)

## Responses

200

401

404

422

### Body

- `id` (integer, optional) — Subscription ID (example: `56`)
- `event` (string, optional) — Name of Subscribed Event (example: `candidate.created`)
- `target_url` (string, optional) — Subscription URL (example: `https://someurl`)

#### Example request body

#### Example request body

#### Example request body

```
{
  "id": 56,
  "event": "candidate.created",
  "target_url": "https://someurl"
}
```

#### Example cURL

#### Example cURL

#### Example cURL

```
curl --request POST \
  --url https://api.recruitcrm.io/v1/subscriptions/{subscription} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json' \
  --data '{
  "id": 56,
  "event": "candidate.created",
  "target_url": "https://someurl"
}'
```

#### Example response

#### Example response

#### Example response

```
{
  "id": 56,
  "event": "candidate.created",
  "target_url": "https://someurl"
}
```
