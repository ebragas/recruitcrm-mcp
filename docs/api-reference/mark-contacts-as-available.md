<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/afb8a75ccb5a8-mark-contacts-as-available -->
<!-- title: Mark Contacts as Available | API Endpoints -->

# Mark Contacts as Available

**POST** `/v1/contacts/mark-as-available`

Mark Contacts as Available

## Request

Security: Bearer Auth

### Body

Mark As Available

- `contact_slugs` (string, **required**) — >= 1 characters (example: `141827385522`)

## Responses

200

401

422

### Body

- `contact_slug` (array, optional) — Contact's Slug (example: `\["141827385522"\]`)
- `remark` (string, optional)
- `Reason` (optional) (example: `Records Were Updated`)

#### Example request body

#### Example request body

```
{
  "contact_slugs": "141827385522"
}
```

#### Example cURL

#### Example cURL

```
curl --request POST \
  --url https://api.recruitcrm.io/v1/contacts/mark-as-available \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json' \
  --data '{
  "contact_slugs": "141827385522"
}'
```

#### Example response

#### Example response

```
{
  "contact_slug": [
    "141827385522"
  ],
  "remark": "Records Were Updated"
}
```
