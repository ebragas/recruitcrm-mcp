<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/0f4f5b895bd5c-mark-contacts-as-off-limit -->
<!-- title: Mark Contacts as Off Limit | API Endpoints -->

# Mark Contacts as Off Limit

**POST** `/v1/contacts/mark-off-limit`

Mark Contacts as Off Limit with reason

## Request

Security: Bearer Auth

### Body

Mark AS OffLimit

- `contact_slugs` (string, **required**) — >= 1 characters (example: `141827385522`)
- `status_id` (number, **required**) (example: `59`)
- `end_date` (string, **required**) — >= 1 characters (example: `20-09-2024`)
- `reason` (string, optional) (example: `testing`)

## Responses

200

401

422

### Body

- `contact_slug` (array, optional) — Contacte's Slug (example: `\["141827385522"\]`)
- `status_id` (integer, optional) — Status Id (example: `59`)
- `end_date` (string, optional) — End Date (example: `18-09-2023`)
- `reason` (string, optional)
- `Reason` (optional) (example: `testing`)
- `remark` (string, optional)
- `Reason` (optional) (example: `Records Were Updated`)

#### Example request body

#### Example request body

```
{
  "contact_slugs": "141827385522",
  "status_id": "59",
  "end_date": "20-09-2024",
  "reason": "testing"
}
```

#### Example cURL

#### Example cURL

```
curl --request POST \
  --url https://api.recruitcrm.io/v1/contacts/mark-off-limit \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json' \
  --data '{
  "contact_slugs": "141827385522",
  "status_id": "59",
  "end_date": "20-09-2024",
  "reason": "testing"
}'
```

#### Example response

#### Example response

```
{
  "contact_slug": [
    "141827385522"
  ],
  "status_id": 59,
  "end_date": "18-09-2023",
  "reason": "testing",
  "remark": "Records Were Updated"
}
```
