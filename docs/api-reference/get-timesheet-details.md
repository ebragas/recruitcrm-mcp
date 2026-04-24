<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/07c522980698b-get-timesheet-details -->
<!-- title: Get Timesheet Details | API Endpoints -->

# Get Timesheet Details

**GET** `/v1/timesheets/{timesheet}`

Fetches all details of a particular timesheet including the time entries.

## Request

Security: Bearer Auth

### Path Parameters

- `timesheet` (integer, **required**) — id of the timesheet

### Query Parameters

- `work_time_details` (string, optional) — Include detailed work time entries per time log. Use 1/true to include bifurcated work time details (start/end times, break intervals, remarks), or 0/false to exclude. (allowed: `truefalse01`)

## Responses

200

401

404

### Body

- `id` (integer, optional) — Numeric ID of the timesheet (example: `48092`)
- `timesheet_id` (string, optional) — Formatted timesheet identifier (example: `TS-36-48092`)
- `timesheet_period` (object, optional)
- `start_date` (optional) — string<date-time> Start date of the timesheet period (example: `2026-03-06T11:06:16.000000Z`)
- `end_date` (optional) — string<date-time> End date of the timesheet period (example: `2026-03-08T11:06:16.000000Z`)
- `related_entities_slug` (object, optional)
- `candidate` (string, optional) — Candidate (contractor) slug (example: `2423442342342`)
- `job` (string, optional) — Job slug (example: `2342342424234`)
- `company` (string, optional) — Company slug (example: `56345234234234`)
- `deals` (string, optional) — Comma-separated deal slugs associated with the timesheet (example: `56345234234234,9234234234`)
- `hours` (object, optional)
- `total_regular` (string, optional) — Regular hours worked (example: `8h 0min`)
- `total_overtime` (string, optional) — Overtime hours worked (example: `0h 0min`)
- `total` (string, optional) — Total hours worked (example: `8h 0min`)
- `timesheet_status` (object, optional) — Current status of the timesheet along with the last action details
- `id` (integer, optional) — Status ID (example: `3`)
- `label` (string, optional) — Status label (e.g., Open, Submitted, Rejected, Approved) (example: `Rejected`)
- `performed_by` (integer, optional) — User ID who performed the last status action (example: `2324`)
- `performed_on` (optional) — string<date-time> Timestamp when the last status action was performed (example: `2026-03-08T11:06:16.000000Z`)
- `time_logs` (optional) — array\[object\] Daily time log entries for the timesheet period
- `id` (integer, optional) — Time log ID (example: `6474`)
- `date` (optional) — string<date-time> Date when this entry was added to the Timesheet (example: `2026-03-06T11:06:16.000000Z`)
- `day` (string, optional) — Day of the week (example: `Monday`)
- `daily_hours` (object, optional)
- `work_time_details` (optional) — array\[object\] Bifurcated work time entries for this day. Returned only when work\_time\_details=1 is passed as a query parameter.
- `pay` (object, optional) — Pay details for the timesheet
- `rate` (number, optional) — Pay rate per hour (example: `50`)
- `currency` (string, optional) — Currency code (example: `INR`)
- `currency_id` (integer, optional) — Currency ID (example: `1`)
- `amount` (number, optional) — Total pay amount for the timesheet (example: `2000`)
- `details` (optional) — object or null Payment status and reference details
- `bill` (object, optional) — Billing details for the timesheet
- `rate` (number, optional) — Bill rate per hour (example: `60`)
- `currency` (string, optional) — Currency code (example: `INR`)
- `currency_id` (integer, optional) — Currency ID (example: `1`)
- `amount` (number, optional) — Total bill amount for the timesheet (example: `2400`)
- `details` (optional) — object or null Invoice status and reference details Not Settruefalse01 select an option

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/timesheets/{timesheet} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
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
      "id": 6474,
      "date": "2026-03-06T11:06:16.000000Z",
      "day": "Monday",
      "daily_hours": {
        "regular": "8h 0min",
        "overtime": "2h 0min",
        "total": "10h 0min"
      },
      "work_time_details": [
        {
          "id": 5001,
          "time": {
            "duration": "0h 2min",
            "start": "9:00",
            "end": "12:30"
          },
          "remark": "Worked on module integration",
          "break_time": "0h 10min",
          "break_intervals": [
            {
              "id": 1,
              "start_time": "10:00",
              "end_time": "10:15"
            }
          ]
        }
      ]
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
```
