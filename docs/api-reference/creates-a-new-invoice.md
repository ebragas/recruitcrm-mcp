<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/f1542874bbf05-creates-a-new-invoice -->
<!-- title: Creates a new invoice | API Endpoints -->

# Creates a new invoice

**POST** `/v1/invoices`

Creates a new invoice.

## Request

Security: Bearer Auth

### Body

Invoice Object

- `template_id` (integer, optional) — Invoice Template ID (Required on create) (example: `1`)
- `description` (string, optional) — Invoice Description (Max: 500 characters) (example: `Professional services rendered for Q1 2024`)
- `company_slug` (string, optional) — Associated Company Slug (Required on create) (example: `1234`)
- `address` (string, optional) — Company Address (Max: 3000 characters) (example: `123 Business St, New York, NY 10001`)
- `contact_slug` (string, optional) — Associated Contact Slug (example: `5678`)
- `contact_number` (string, optional) — Contact Number (Max: 50 characters) (example: `+1-555-0123`)
- `email` (string, optional) — Contact Email (Max: 70 characters) (example: `john.doe@acme.com`)
- `issue_date` (optional) — string<date> Issue Date (example: `2020-06-29`)
- `due_date` (optional) — string<date> Due Date (example: `2020-07-29`)
- `created_by` (integer, optional) — Created By User ID (example: `1`)
- `additional_note` (string, optional) — Additional Note (Max: 3000 characters) (example: `Payment terms: Net 30. Please remit payment to the address listed above.`)
- `currency_id` (integer, optional) — Currency ID (example: `2`)
- `associated_candidate_slugs` (string, optional) — Comma-separated string of associated candidate slugs (example: `12345,67890`)
- `associated_contact_slugs` (string, optional) — Comma-separated string of associated contact slugs (example: `5678,9012`)
- `associated_company_slugs` (string, optional) — Comma-separated string of associated company slugs (example: `1234,5678`)
- `associated_deal_slugs` (string, optional) — Comma-separated string of associated deal slugs (example: `3456,7890`)
- `associated_job_slugs` (string, optional) — Comma-separated string of associated job slugs (example: `7890,1234`)
- `invoice_fields` (optional) — array\[array\] Invoice line items/fields. Array of arrays containing field objects with fieldId and fieldValue (example: `\[\[{"fieldId":1,"fieldValue":"Consulting Services"},{"fieldId":2,"fieldValue":"100"}\],\[{"fieldId":1,"fieldValue":"Development Services"},{"fieldId":2,"fieldValue":"200"}\]\]`)
- `object` (optional)

## Responses

200

201

401

422

### Body

- `message` (string, optional) (example: `Invoice created successfully`)
- `id` (integer, optional) (example: `123`)

#### Example request body

#### Example request body

```
{
  "template_id": 1,
  "description": "Professional services rendered for Q1 2024",
  "company_slug": "1234",
  "address": "123 Business St, New York, NY 10001",
  "contact_slug": "5678",
  "contact_number": "+1-555-0123",
  "email": "john.doe@acme.com",
  "issue_date": "2020-06-29",
  "due_date": "2020-07-29",
  "created_by": 1,
  "additional_note": "Payment terms: Net 30. Please remit payment to the address listed above.",
  "currency_id": 2,
  "associated_candidate_slugs": "12345,67890",
  "associated_contact_slugs": "5678,9012",
  "associated_company_slugs": "1234,5678",
  "associated_deal_slugs": "3456,7890",
  "associated_job_slugs": "7890,1234",
  "invoice_fields": [
    [
      {
        "fieldId": 1,
        "fieldValue": "Consulting Services"
      },
      {
        "fieldId": 2,
        "fieldValue": "100"
      }
    ],
    [
      {
        "fieldId": 1,
        "fieldValue": "Development Services"
      },
      {
        "fieldId": 2,
        "fieldValue": "200"
      }
    ]
  ]
}
```

#### Example cURL

#### Example cURL

```
curl --request POST \
  --url https://api.recruitcrm.io/v1/invoices \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json' \
  --data '{
  "template_id": 1,
  "description": "Professional services rendered for Q1 2024",
  "company_slug": "1234",
  "address": "123 Business St, New York, NY 10001",
  "contact_slug": "5678",
  "contact_number": "+1-555-0123",
  "email": "john.doe@acme.com",
  "issue_date": "2020-06-29",
  "due_date": "2020-07-29",
  "created_by": 1,
  "additional_note": "Payment terms: Net 30. Please remit payment to the address listed above.",
  "currency_id": 2,
  "associated_candidate_slugs": "12345,67890",
  "associated_contact_slugs": "5678,9012",
  "associated_company_slugs": "1234,5678",
  "associated_deal_slugs": "3456,7890",
  "associated_job_slugs": "7890,1234",
  "invoice_fields": [\
    [\
      {\
        "fieldId": 1,\
        "fieldValue": "Consulting Services"\
      },\
      {\
        "fieldId": 2,\
        "fieldValue": "100"\
      }\
    ],\
    [\
      {\
        "fieldId": 1,\
        "fieldValue": "Development Services"\
      },\
      {\
        "fieldId": 2,\
        "fieldValue": "200"\
      }\
    ]\
  ]
}'
```

#### Example response

#### Example response

```
{
  "message": "Invoice created successfully",
  "id": 123
}
```
