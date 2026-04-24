<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/v3h9wsdov0ibo-sent-email-status -->
<!-- title: Sent Email Status | API Endpoints -->

# Sent Email Status

**GET** `/v1/emails/status/{email\_status\_id}`

To Check Sent Email Status

## Request

Security: Bearer Auth

### Path Parameters

- `email_status_id` (string, **required**) — Id to check Status Of Email Sent

## Responses

200

401

429

### Body

Sent Email Status - Suceess

(any of)

- `message` (string, optional) (example: `Email sent successfully`)
- `created_at` (string, optional) (example: `2025-02-14T10:59:00.000000Z`)
- `status` (string, optional) (example: `Success`)
- `email_message_id` (string, optional) (example: `1`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/emails/status/{email_status_id} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "message": "Email sent successfully",
  "created_at": "2025-02-14T10:59:00.000000Z",
  "status": "Success",
  "email_message_id": "1"
}
```
