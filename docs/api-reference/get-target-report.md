<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/e2fac955e6b62-get-target-report -->
<!-- title: Get Target Report | API Endpoints -->

# Get Target Report

**GET** `/v1/target-report/get`

Returns a list of Target Reports

## Request

Security: Bearer Auth

### Query Parameters

- `limit` (integer, optional) — Limit of records per page. (Max:100)
- `sort_by` (string, optional) — Sort by field (default: `updated\_on`)
- `sort_order` (string, optional) — Sort order (allowed: `ascdesc`; default: `desc`)

## Responses

200

401

### Body

- `TargetId` (number, optional) — ID of the Target Report
- `TargetName` (string, optional) — Title of the Target Report
- `CreatedOn` (string, optional) — Target Report Created Date
- `CreatedBy` (number, optional) — Target Report Owner Id
- `StartDate` (string, optional) — Target Report Start Date
- `EndDate` (string, optional) — Target Report End Date
- `Frequency` (string, optional) — Target Report Frequency
- `TypeOfAssignees` (string, optional) — Target Report Assignee Type
- `Assignees` (string, optional) — Target Report Assignees Ids
- `TargetKPIs` (string, optional) — Target Report Kpis Not Setascdesc select an option (defaults to: desc)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/target-report/get \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "TargetId": 0,
  "TargetName": "string",
  "CreatedOn": "string",
  "CreatedBy": 0,
  "StartDate": "string",
  "EndDate": "string",
  "Frequency": "string",
  "TypeOfAssignees": "string",
  "Assignees": "string",
  "TargetKPIs": "string"
}
```
