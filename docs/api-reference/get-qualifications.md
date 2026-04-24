<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/079feda02ac96-get-qualifications -->
<!-- title: Get Qualifications | API Endpoints -->

# Get Qualifications

**GET** `/v1/qualifications`

Returns a list of qualifications

## Request

Security: Bearer Auth

## Responses

200

401

### Body

- `qualification_id` (integer, optional) — Qualification ID (example: `3`)
- `label` (string, optional) — Qualification Label (example: `Associate Degree`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/qualifications \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "qualification_id": 3,
  "label": "Associate Degree"
}
```
