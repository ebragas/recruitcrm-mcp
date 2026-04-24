<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/8f0b45d7eed03-delete-an-invoice -->
<!-- title: Delete an invoice | API Endpoints -->

# Delete an invoice

**DELETE** `/v1/invoices/{id}`

Delete an invoice.

## Request

Security: Bearer Auth

### Path Parameters

- `id` (integer, **required**) — ID of the invoice to delete

## Responses

200

401

404

#### Example cURL

#### Example cURL

```
curl --request DELETE \
  --url https://api.recruitcrm.io/v1/invoices/{id} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json'
```
