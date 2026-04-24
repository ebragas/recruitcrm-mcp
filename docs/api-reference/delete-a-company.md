<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/d352d5ccdaa8d-delete-a-company -->
<!-- title: Delete a company | API Endpoints -->

# Delete a company

**DELETE** `/v1/companies/{company}`

Delete a company.

## Request

Security: Bearer Auth

### Path Parameters

- `company` (string, **required**) — slug of the company to delete

## Responses

200

401

404

#### Example cURL

#### Example cURL

```
curl --request DELETE \
  --url https://api.recruitcrm.io/v1/companies/{company} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json'
```
