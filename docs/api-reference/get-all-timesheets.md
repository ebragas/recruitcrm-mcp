<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/cf8c44d0e6857-get-all-timesheets -->
<!-- title: Get All Timesheets | API Endpoints -->

# Get All Timesheets

**GET** `/v1/timesheets`

Returns all timesheets associated with your account, with optional filters and pagination.

## Request

Security: Bearer Auth

### Query Parameters

- `candidate_slug` (string, optional) — Filter by contractor (candidate) slug
- `company_slug` (string, optional) — Filter by company slug
- `job_slug` (string, optional) — Filter by job slug
- `limit` (integer, optional) — Limit of records per page. (Max: 100)
- `page` (integer, optional) — Page number for pagination
- `sort_by` (string, optional) — Field to sort by
- `sort_order` (string, optional) — Sort order (allowed: `ascdesc`)
- `time_logs` (string, optional) — Include daily time log entries in the response. Use 1/true to include, 0/false to exclude. (allowed: `truefalse01`)
- `timesheet_end_date` (string, optional) — Only timesheets with this exact end date are returned. (example: `2026-01-07`)
- `timesheet_start_date` (string, optional) — Only timesheets with this exact start date are returned. (example: `2026-01-01`)
- `timesheet_status` (string, optional) — Filter by timesheet status (e.g., Open, Submitted, Approved, Rejected)

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
- `id` (integer, optional) — Numeric ID of the timesheet (example: `48092`)
- `timesheet_id` (string, optional) — Formatted timesheet identifier (example: `TS-36-48092`)
- `timesheet_period` (object, optional)
- `related_entities_slug` (object, optional)
- `hours` (object, optional)
- `timesheet_status` (object, optional) — Current status of the timesheet along with the last action details
- `time_logs` (optional) — array\[object\] Daily time log summary entries. Returned only when time\_logs=1 is passed as a query parameter.
- `pay` (object, optional) — Pay details for the timesheet
- `bill` (object, optional) — Billing details for the timesheet Not Setascdesc select an option time\_logs: Not Settruefalse01 select an option timesheet\_end\_date: timesheet\_start\_date: timesheet\_status:

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/timesheets \
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
      "id": 48092,
      "timesheet_id": "TS-36-48092",
      "timesheet_period": {
        "start_date": "2026-03-06T11:06:16.000000Z",
        "end_date": "2026-03-08T11:06:16.000000Z"
      },
      "related_entities_slug": {
        "candidate": "2423442342342",
        "job": "2342342424234",
        "company": "56345234234234",
        "deals": "56345234234234,9234234234"
      },
      "hours": {
        "total_regular": "8h 0min",
        "total_overtime": "0h 0min",
        "total": "8h 0min"
      },
      "timesheet_status": {
        "id": 3,
        "label": "Rejected",
        "performed_by": 2324,
        "performed_on": "2026-03-08T11:06:16.000000Z"
      },
      "time_logs": [
        {
          "id": 4798,
          "date": "2026-03-10T11:06:16.000000Z",
          "day": "Monday",
          "daily_hours": {
            "regular": "8h 0min",
            "overtime": "2h 0min",
            "total": "10h 0min"
          }
        }
      ],
      "pay": {
        "rate": 50,
        "currency": "INR",
        "currency_id": 1,
        "amount": 2000,
        "details": {
          "id": 1,
          "label": "Paid",
          "payout_number": "001",
          "paid_on": "2026-03-06T11:06:16.000000Z"
        }
      },
      "bill": {
        "rate": 60,
        "currency": "INR",
        "currency_id": 1,
        "amount": 2400,
        "details": {
          "id": 2,
          "label": "Unbilled",
          "invoice_number": "INV-005",
          "invoice_created_on": "2026-03-06T11:06:16.000000Z"
        }
      }
    }
  ]
}
```
