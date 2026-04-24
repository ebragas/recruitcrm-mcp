<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/74ca8b82de83d-find-invoice-by-id -->
<!-- title: Find invoice by ID | API Endpoints -->

# Find invoice by ID

**GET** `/v1/invoices/{id}`

Returns a single invoice

## Request

Security: Bearer Auth

### Path Parameters

- `id` (integer, **required**) — ID of the invoice

## Responses

200

401

404

### Body

- `id` (integer, optional)
- `ID` (optional) (example: `1`)
- `invoice_id` (string, optional) — Invoice ID (example: `INV001`)
- `template` (object, optional) — Invoice Template
- `template_id` (integer, optional) — Template ID (example: `1`)
- `template_name` (string, optional) — Template Name (example: `Invoice Template`)
- `description` (string, optional) — Invoice Description (example: `Professional services rendered for Q1 2024`)
- `billed_to_client` (object, optional) — Client billing information
- `company_slug` (string, optional) — Company Slug (example: `1234`)
- `company_name` (string, optional) — Company Name (example: `Acme Corporation`)
- `address` (string, optional) — Company Address (example: `123 Business St, New York, NY 10001`)
- `contact_slug` (string, optional) — Contact Slug (example: `5678`)
- `email` (string, optional) — Contact Email (example: `john.doe@acme.com`)
- `contact_name` (string, optional) — Contact Name (example: `John Doe`)
- `contact_number` (string, optional) — Contact Number (example: `+1-555-0123`)
- `associated_entities` (object, optional) — Associated entities with this invoice
- `candidate_slugs` (optional) — array\[string\] Associated Candidate Slugs (example: `\["12345","67890"\]`)
- `contact_slugs` (optional) — array\[string\] Associated Contact Slugs (example: `\["5678","9012"\]`)
- `company_slugs` (optional) — array\[string\] Associated Company Slugs (example: `\["1234"\]`)
- `deal_slugs` (optional) — array\[string\] Associated Deal Slugs (example: `\["3456"\]`)
- `job_slugs` (optional) — array\[string\] Associated Job Slugs (example: `\["7890"\]`)
- `total_amount` (string, optional) — Total Amount (example: `$ 5000.00 USD`)
- `total_amount_in_account_currency` (string, optional) — Total Amount in Account Currency (example: `$ 5000.00 USD`)
- `invoice_status` (integer, optional) — Invoice Status ID (example: `1`)
- `created_by` (integer, optional) — Created By User ID (example: `1`)
- `created_on` (optional) — string<date-time> Created On (example: `2020-06-29T05:36:22.000000Z`)
- `due_date` (optional) — string<date-time> Due Date (example: `2020-07-29T05:36:22.000000Z`)
- `issue_date` (optional) — string<date-time> Issue Date (example: `2020-06-29T05:36:22.000000Z`)
- `invoice_fields` (optional) — array\[object\] Invoice line items/fields
- `invoice_pdf` (string, optional) — Invoice PDF file link (example: `https://example.com/invoices/invoice-001.pdf`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/invoices/{id} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "id": 1,
  "invoice_id": "INV001",
  "template": {
    "template_id": 1,
    "template_name": "Invoice Template"
  },
  "description": "Professional services rendered for Q1 2024",
  "billed_to_client": {
    "company_slug": "1234",
    "company_name": "Acme Corporation",
    "address": "123 Business St, New York, NY 10001",
    "contact_slug": "5678",
    "email": "john.doe@acme.com",
    "contact_name": "John Doe",
    "contact_number": "+1-555-0123"
  },
  "associated_entities": {
    "candidate_slugs": [
      "12345",
      "67890"
    ],
    "contact_slugs": [
      "5678",
      "9012"
    ],
    "company_slugs": [
      "1234"
    ],
    "deal_slugs": [
      "3456"
    ],
    "job_slugs": [
      "7890"
    ]
  },
  "total_amount": "$ 5000.00 USD",
  "total_amount_in_account_currency": "$ 5000.00 USD",
  "invoice_status": 1,
  "created_by": 1,
  "created_on": "2020-06-29T05:36:22.000000Z",
  "due_date": "2020-07-29T05:36:22.000000Z",
  "issue_date": "2020-06-29T05:36:22.000000Z",
  "invoice_fields": [
    {}
  ],
  "invoice_pdf": "https://example.com/invoices/invoice-001.pdf"
}
```
