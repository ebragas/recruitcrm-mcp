<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/81c1c95c75b9b-delete-a-note -->
<!-- title: Delete a note | API Endpoints -->

# Delete a note

**DELETE** `/v1/notes/{note}`

Delete a note.

## Request

Security: Bearer Auth

### Path Parameters

- `note` (integer, **required**) — ID of the note to delete

## Responses

200

401

404

#### Example cURL

#### Example cURL

```
curl --request DELETE \
  --url https://api.recruitcrm.io/v1/notes/{note} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json'
```
