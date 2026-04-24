<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/b9e638cc93d88-mark-companies-as-off-limit -->
<!-- title: Mark Companies as Off Limit | API Endpoints -->

# Mark Companies as Off Limit

**POST** `/v1/companies/mark-off-limit`

Mark Companies as Off Limit with reason

## Request

Security: Bearer Auth

### Body

Mark AS OffLimit

- `company_slugs` (string, **required**) — >= 1 characters (example: `87984,88825`)
- `status_id` (number, **required**) (example: `59`)
- `end_date` (string, **required**) — >= 1 characters (example: `20-09-2024`)
- `reason` (string, optional) (example: `testing`)
- `mark_contact_off_limit` (boolean, **required**) (example: `true`)
- `mark_candidate_off_limit` (boolean, **required**) (example: `true`)

## Responses

200

401

422

### Body

- `company_slugs` (array, optional) — Company Slugs (example: `\["87984","88825"\]`)
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
  "company_slugs": "87984,88825",
  "status_id": "59",
  "end_date": "20-09-2024",
  "reason": "testing",
  "mark_contact_off_limit": true,
  "mark_candidate_off_limit": true
}
```

#### Example cURL

#### Example cURL

```
curl --request POST \
  --url https://api.recruitcrm.io/v1/companies/mark-off-limit \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json' \
  --data '{
  "company_slugs": "87984,88825",
  "status_id": "59",
  "end_date": "20-09-2024",
  "reason": "testing",
  "mark_contact_off_limit": true,
  "mark_candidate_off_limit": true
}'
```

#### Example response

#### Example response

```
{
  "company_slugs": [
    "87984",
    "88825"
  ],
  "status_id": 59,
  "end_date": "18-09-2023",
  "reason": "testing",
  "remark": "Records Were Updated"
}
```
