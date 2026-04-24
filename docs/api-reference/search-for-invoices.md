<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/589f6ed52cb76-search-for-invoices -->
<!-- title: Search for invoices | API Endpoints -->

# Search for invoices

**GET** `/v1/invoices/search`

Returns all invoices associated with your account that matched the search.

## Request

Security: Bearer Auth

### Query Parameters

- `associated_candidate_slug` (string, optional) — Associated Candidate Slug (example: `12345`)
- `associated_company_slug` (string, optional) — Associated Company Slug (example: `1234`)
- `associated_contact_slug` (string, optional) — Associated Contact Slug (example: `5678`)
- `associated_deal_slug` (string, optional) — Associated Deal Slug (example: `3456`)
- `associated_job_slug` (string, optional) — Associated Job Slug (example: `7890`)
- `created_by` (integer, optional) — Created By User ID (example: `1`)
- `due_date_from` (optional) — string<date> Due Date From (Start date for filtering invoices by due date) (example: `2020-07-01`)
- `due_date_to` (optional) — string<date> Due Date To (End date for filtering invoices by due date) (example: `2020-07-31`)
- `invoice_id` (string, optional) — Invoice ID (example: `INV001`)
- `issue_date_from` (optional) — string<date> Issue Date From (Start date for filtering invoices by issue date) (example: `2020-06-01`)
- `issue_date_to` (optional) — string<date> Issue Date To (End date for filtering invoices by issue date) (example: `2020-06-30`)
- `limit` (integer, optional) — Limit of records per page. (Max:100)
- `page` (integer, optional) — Page Number for Pagination
- `status_id` (integer, optional) — Invoice Status ID (example: `1`)
- `sort_by` (string, optional) — Sort by field (allowed: `created\_onupdated\_onissue\_datedue\_date`; default: `updatedon`)
- `sort_order` (string, optional) — Sort order (allowed: `ascdesc`; default: `desc`)

## Responses

200

401

### Body

- `current_page` (integer, optional) — Current page number (example: `1`)
- `first_page_url` (string, optional) — URL of the first page
- `from` (integer, optional) — Records from page number (example: `1`)
- `next_page_url` (string, optional) — URL of the next page (example: `null`)
- `path` (string, optional) — URL of the endpoint
- `per_page` (integer, optional) — Records per page (example: `25`)
- `prev_page_url` (string, optional) — URL of the next page (example: `null`)
- `to` (integer, optional) — Records to page number (example: `25`)
- `data` (optional) — array\[object\]
- `id` (integer, optional)
- `ID` (optional) (example: `1`)
- `invoice_id` (string, optional) — Invoice ID (example: `INV001`)
- `template` (object, optional) — Invoice Template
- `description` (string, optional) — Invoice Description (example: `Professional services rendered for Q1 2024`)
- `billed_to_client` (object, optional) — Client billing information
- `associated_entities` (object, optional) — Associated entities with this invoice
- `total_amount` (string, optional) — Total Amount (example: `$ 5000.00 USD`)
- `total_amount_in_account_currency` (string, optional) — Total Amount in Account Currency (example: `$ 5000.00 USD`)
- `invoice_status` (integer, optional) — Invoice Status ID (example: `1`)
- `created_by` (integer, optional) — Created By User ID (example: `1`)
- `created_on` (optional) — string<date-time> Created On (example: `2020-06-29T05:36:22.000000Z`)
- `due_date` (optional) — string<date-time> Due Date (example: `2020-07-29T05:36:22.000000Z`)
- `issue_date` (optional) — string<date-time> Issue Date (example: `2020-06-29T05:36:22.000000Z`)
- `invoice_fields` (optional) — array\[object\] Invoice line items/fields
- `invoice_pdf` (string, optional) — Invoice PDF file link Not Setcreated\_onupdated\_onissue\_datedue\_date select an option (defaults to: updatedon) sort\_order: Not Setascdesc select an option (defaults to: desc) status\_id: (example: `https://example.com/invoices/invoice-001.pdf`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/invoices/search \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "current_page": 1,
  "first_page_url": "string",
  "from": 1,
  "next_page_url": "null",
  "path": "string",
  "per_page": 25,
  "prev_page_url": "null",
  "to": 25,
  "data": [
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
  ]
}
```
