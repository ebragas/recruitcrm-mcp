<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/2613c32f03133-get-invoice-templates -->
<!-- title: Get Invoice Templates | API Endpoints -->

# Get Invoice Templates

**GET** `/v1/invoice-templates`

Returns a list of invoice templates

## Request

Security: Bearer Auth

## Responses

200

401

### Body

array of:

- `template_id` (integer, optional) — Template ID (example: `1`)
- `template_name` (string, optional) — Template Name (example: `Standard Invoice Template`)
- `shared_with` (optional) — array\[integer\] List of users/teams the template is shared with (example: `\[1,2,3\]`)
- `invoice_fields` (optional) — array\[object\] Invoice template fields
- `field_id` (integer, optional) — Field ID (example: `1`)
- `field_name` (string, optional) — Field Name/Label (example: `Service Description`)
- `field_type` (string, optional) — Field Type (example: `text`)
- `default_value` (string, optional) — Default Value (example: `Consulting Services`)
- `due_date` (integer, optional) — Due date in days from issue date (example: `30`)
- `created_by` (integer, optional) — Created By User ID (example: `1`)
- `created_on` (optional) — string<date-time> Created On (example: `2020-06-29T05:36:22.000000Z`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/invoice-templates \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
[
  {
    "template_id": 1,
    "template_name": "Standard Invoice Template",
    "shared_with": [
      1,
      2,
    ],
    "invoice_fields": [
      {
        "field_id": 1,
        "field_name": "Service Description",
        "field_type": "text",
        "default_value": "Consulting Services"
      },
      {
        "field_id": 2,
        "field_name": "Amount",
        "field_type": "number",
        "default_value": "0"
      }
    ],
    "due_date": 30,
    "created_by": 1,
    "created_on": "2020-06-29T05:36:22.000000Z"
  }
]
```
