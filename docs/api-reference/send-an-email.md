<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/bvaogh4298iyy-send-an-email -->
<!-- title: Send an Email | API Endpoints -->

# Send an Email

**POST** `/v1/emails`

To send an email

> This endpoint responds quickly using asynchronous processing. It may show a "Network Error" in some tools, but it works correctly in Postman and other API clients.

## Request

Security: Bearer Auth

### Body

Send Email Object

Request Schema

- `from` (integer, optional) — ID of the user associated with the account (example: `5`)
- `to` (object, **required**) — Details of the primary recipient. Includes: - **Type:** candidate, contact or user. - **Identifier:** Slug for candidate/contact or ID for user. (example: `{"type":"candidate","identifier":"16705746963230000005xEH"}`)
- `cc` (optional) — array\[object\] List of CC recipients. Each recipient includes: - **Type:** candidate, contact or user. - **Identifier:** Slug for candidate/contact or ID for user. - **Maximum of 10 recipients** (example: `\[{"type":"contact","identifier":"16705746963230000005xEH"}\]`)
- `type` (string, optional) (example: `contact`)
- `identifier` (string, optional) (example: `16705746963230000005xEH`)
- `bcc` (optional) — array\[object\] List of BCC recipients. Each recipient includes: - **Type:** candidate, contact or user. - **Identifier:** Slug for candidate/contact or ID for user. - **Maximum of 10 recipients** (example: `\[{"type":"user","identifier":"5"}\]`)
- `type` (string, optional) (example: `user`)
- `identifier` (string, optional) (example: `5`)
- `associations` (optional) — array\[object\] List of Associated recipients. Each recipient includes: - **Type:** candidate, contact, company, job or deal. - **Identifier:** Slug for candidate/contact/company/job/deal. (example: `\[{"type":"company","identifier":"16705746963230000005xEH"}\]`)
- `type` (string, optional) (example: `company`)
- `identifier` (string, optional) (example: `16705746963230000005xEH`)
- `subject` (string, **required**) — Email subject line. (example: `Grow Your Career Today`)
- `body` (string, optional) — Email body content. attachments\[\] (example: `Are you looking for a new challenge in your career?`)
- `array` (optional) — Requirements: - Only public files are allowed. - Single files must not exceed the size limit set by the provider. - Total combined size must not exceed the provider's limit. - **Maximum of 5 files are allowed.**
- `include_signature` (boolean, optional) — Should Include E-Mail Signature In Body (default: `false`)
- `include_opt_out_link` (boolean, optional) — Should Include opt-out/unsubscribe link in Body (default: `false`)

## Responses

200

401

429

### Body

- `message` (string, optional) (example: `We are currently processing your request`)
- `email_status_id` (integer, optional) — Id to check Status Of Email Sent (example: `1`)
- `status` (string, optional) — Omit from to\*: cc: Omit cc bcc: Omit bcc associations: Omit associations subject\*: body: Omit body attachments\[\]: Omit attachments\[\] include\_signature: Omit include\_signature include\_opt\_out\_link: Omit include\_opt\_out\_link (example: `success`)

#### Example cURL

#### Example cURL

```
curl --request POST \
  --url https://api.recruitcrm.io/v1/emails \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: multipart/form-data' \
  --form from= \
  --form 'to={\"type\":\"candidate\",\"identifier\":\"16705746963230000005xEH\"}' \
  --form cc= \
  --form bcc= \
  --form associations= \
  --form 'subject=Grow Your Career Today' \
  --form body= \
  --form 'attachments[]=' \
  --form include_signature= \
  --form include_opt_out_link=
```

#### Example response

#### Example response

```
{
  "message": "We are currently processing your request",
  "email_status_id": 1,
  "status": "success"
}
```
