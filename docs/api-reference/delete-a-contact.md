<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/5d35fa49b332d-delete-a-contact -->
<!-- title: Delete a contact | API Endpoints -->

# Delete a contact

**DELETE** `/v1/contacts/{contact}`

Delete a contact.

## Request

Security: Bearer Auth

### Path Parameters

- `contact` (string, **required**) — slug of the contact to delete

## Responses

200

401

404

#### Example cURL

#### Example cURL

```
curl --request DELETE \
  --url https://api.recruitcrm.io/v1/contacts/{contact} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json'
```
