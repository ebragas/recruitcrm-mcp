<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/7f2bd44783442-request-updated-profile -->
<!-- title: Request Updated Profile | API Endpoints -->

# Request Updated Profile

**GET** `/v1/candidates/{candidate}/request-update`

Returns the url to request an updated profile of the candidate

## Request

Security: Bearer Auth

### Path Parameters

- `candidate` (string, **required**) — slug of the candidate

## Responses

200

404

### Body

- `url` (string, optional) (example: `http://recruitcrm.io/update\_resume\_link/rcrm\_25627`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/candidates/{candidate}/request-update \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "url": "http://recruitcrm.io/update_resume_link/rcrm_25627"
}
```
