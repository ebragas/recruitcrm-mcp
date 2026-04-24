<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/e4221a8c0e6ac-stage-history-of-candidate-for-job -->
<!-- title: Stage History of Candidate for job | API Endpoints -->

# Stage History of Candidate for job

**GET** `/v1/jobs/{job}/stage-history/{candidate}`

Return list of stage history of candidates for requested job

## Request

Security: Bearer Auth

### Path Parameters

- `candidate` (string, **required**) — slug of the candidate
- `job` (string, **required**) — slug of the job

### Query Parameters

- `limit` (integer, optional) — Limit of records per page. (Max:100)
- `page` (integer, optional) — Page number for records

## Responses

200

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
- `status` (object, optional) — Candidate's status (example: `{"status\_id":1,"label":"Assigned"}`)
- `remark` (string, optional)
- `Remark` (optional) (example: `Updated`)
- `stage_date` (string, optional) — Updated Date (example: `2020-03-25T16:14:28.000000Z`)
- `updated_on` (string, optional) — Record Updated Date (example: `2020-03-25T16:14:28.000000Z`)
- `updated_by` (string, optional) — Updated by User Details (example: `112423`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/jobs/{job}/stage-history/{candidate} \
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
      "status": {
        "status_id": 1,
        "label": "Assigned"
      },
      "remark": "Updated",
      "stage_date": "2020-03-25T16:14:28.000000Z",
      "updated_on": "2020-03-25T16:14:28.000000Z",
      "updated_by": "112423"
    }
  ]
}
```
