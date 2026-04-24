<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/53cdf9732522a-get-task-types -->
<!-- title: Get Task Types  | API Endpoints -->

# Get Task Types

**GET** `/v1/task-types`

Returns a list of Task types

## Request

Security: Bearer Auth

## Responses

200

401

### Body

- `id` (integer, optional) — Task Type ID (example: `1`)
- `label` (string, optional) — Task Type Label (example: `Follow up`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/task-types \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "id": 1,
  "label": "Follow up"
}
```
