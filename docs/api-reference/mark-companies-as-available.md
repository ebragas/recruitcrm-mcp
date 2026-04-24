<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/4d1a3fd3d8c95-mark-companies-as-available -->
<!-- title: Mark Companies as Available | API Endpoints -->

# Mark Companies as Available

**POST** `/v1/companies/mark-as-available`

Mark Companies as Available

## Request

Security: Bearer Auth

### Body

Mark AS Available

- `company_slugs` (string, **required**) — >= 1 characters (example: `87984,88825`)
- `mark_contact_available` (boolean, optional) (example: `true`)
- `mark_candidate_available` (boolean, optional) (example: `true`)

## Responses

200

401

422

### Body

- `company_slugs` (array, optional) — Company Slugs (example: `\["87984,88825"\]`)
- `mark_contact_available` (boolean, optional) (example: `true`)
- `mark_candidate_available` (boolean, optional) (example: `true`)
- `remark` (string, optional)
- `Reason` (optional) (example: `Records Were Updated`)

#### Example request body

#### Example request body

```
{
  "company_slugs": "87984,88825",
  "mark_contact_available": true,
  "mark_candidate_available": true
}
```

#### Example cURL

#### Example cURL

```
curl --request POST \
  --url https://api.recruitcrm.io/v1/companies/mark-as-available \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json' \
  --data '{
  "company_slugs": "87984,88825",
  "mark_contact_available": true,
  "mark_candidate_available": true
}'
```

#### Example response

#### Example response

```
{
  "company_slugs": [
    "87984,88825"
  ],
  "mark_contact_available": true,
  "mark_candidate_available": true,
  "remark": "Records Were Updated"
}
```
