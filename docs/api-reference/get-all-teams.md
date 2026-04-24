<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/0fa78c8eaa4ae-get-all-teams -->
<!-- title: Get All Teams | API Endpoints -->

# Get All Teams

**GET** `/v1/teams`

Returns a list of teams

## Request

Security: Bearer Auth

### Query Parameters

- `expand` (string, optional) — Examples:
- `users` (optional)

## Responses

200

401

### Body

- `team_id` (integer, optional) — Team ID (example: `16`)
- `team_name` (string, optional) — Team Name (example: `team1`)
- `users` (object, optional)
- `id` (integer, optional) — User ID (example: `34`)
- `first_name` (string, optional) — User's First Name (example: `Jane`)
- `last_name` (string, optional) — User's Last Name (example: `Scott`)
- `email` (string, optional) — User's Email (example: `jane.scott@gmail.com`)
- `contact_number` (string, optional) — User's contact\_number
- `avatar` (string, optional) — User's avatar link

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/teams \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "team_id": "16",
  "team_name": "team1",
  "users": {
    "id": 34,
    "first_name": "Jane",
    "last_name": "Scott",
    "email": "jane.scott@gmail.com",
    "contact_number": "string",
    "avatar": "string"
  }
}
```
