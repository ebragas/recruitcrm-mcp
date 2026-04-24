<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/06f55eaa077a6-get-collaborators -->
<!-- title: Get Collaborators | API Endpoints -->

# Get Collaborators

**GET** `/v1/collaborators`

Returns a list of collaborators

## Request

Security: Bearer Auth

### Query Parameters

- `expand` (string, optional) — Examples:
- `team` (optional)

## Responses

200

401

### Body

- `id` (integer, optional) — User ID (example: `34`)
- `first_name` (string, optional) — User's First Name (example: `Jane`)
- `last_name` (string, optional) — User's Last Name (example: `Scott`)
- `email` (string, optional) — User's Email (example: `jane.scott@gmail.com`)
- `contact_number` (string, optional) — User's contact\_number
- `city` (string, optional) — User's city
- `state` (string, optional) — User's state
- `country` (string, optional) — User's country
- `role` (string, optional) — User's role
- `timezone` (integer, optional) — User's timezone
- `currency` (string, optional) — User's currency
- `application_language` (string, optional) — User's application\_language
- `avatar` (string, optional) — User's avatar link
- `email_signature_added` (string, optional) — User's email signature added
- `two_factor_authentication_enabled` (boolean, optional) — User's two factor authentication enabled
- `status` (string, optional) — User's status (example: `Active/Deactivate`)
- `teams` (object, optional)
- `team_id` (integer, optional) — Team ID (example: `16`)
- `team_name` (string, optional) — Team Name (example: `team1`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/collaborators \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "id": 34,
  "first_name": "Jane",
  "last_name": "Scott",
  "email": "jane.scott@gmail.com",
  "contact_number": "string",
  "city": "string",
  "state": "string",
  "country": "string",
  "role": "string",
  "timezone": 0,
  "currency": "string",
  "application_language": "string",
  "avatar": "string",
  "email_signature_added": "string",
  "two_factor_authentication_enabled": true,
  "status": "Active/Deactivate",
  "teams": {
    "team_id": "16",
    "team_name": "team1"
  }
}
```
