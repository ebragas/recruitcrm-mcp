<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/6323d41bf3595-get-all-enrollment-statuses -->
<!-- title: Get All Enrollment Statuses | API Endpoints -->

# Get All Enrollment Statuses

**GET** `/v1/enrollment-statuses`

Returns a list of Enrollment Statuses

## Request

Security: Bearer Auth

## Responses

200

401

### Body

- `status_id` (integer, optional) (example: `1`)
- `label` (string, optional) — Status Label (example: `ACTIVE`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/enrollment-statuses \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "status_id": 1,
  "label": "ACTIVE"
}
```
