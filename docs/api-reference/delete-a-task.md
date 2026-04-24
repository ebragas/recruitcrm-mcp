<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/55ee4448717a5-delete-a-task -->
<!-- title: Delete a task | API Endpoints -->

# Delete a task

**DELETE** `/v1/tasks/{task}`

Delete a task.

## Request

Security: Bearer Auth

### Path Parameters

- `task` (integer, **required**) — ID of the task to delete

## Responses

200

401

404

#### Example cURL

#### Example cURL

```
curl --request DELETE \
  --url https://api.recruitcrm.io/v1/tasks/{task} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json'
```
