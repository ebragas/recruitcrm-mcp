<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/b8062c526dc16-apply-to-job -->
<!-- title: Apply to Job | API Endpoints -->

# Apply to Job

**POST** `/v1/candidates/{candidate}/apply`

Apply to a job.

## Request

Security: Bearer Auth

### Path Parameters

- `candidate` (string, **required**) — slug of the candidate

### Query Parameters

- `job_slug` (string, **required**) — slug of the job
- `updated_by` (integer, optional) — ID of the user

## Responses

200

401

422

### Body

- `candidate_slug` (string, optional) — Candidate's Slug (example: `1205129`)
- `job_slug` (string, optional) — Job's Slug (example: `1206683`)
- `status` (object, optional) — Candidate's status (example: `{"status\_id":1,"label":"Applied"}`)
- `remark` (string, optional)
- `Remark` (optional) (example: `Updated`)
- `stage_date` (string, optional) — Updated Date (example: `2020-03-25T16:14:28.000000Z`)
- `visibility` (integer, optional) — Candidate's visibility in a job: For On - 1, Off - 0 (example: `1`)
- `updated_on` (string, optional) — Record Updated Date (example: `2020-03-25T16:14:28.000000Z`)
- `updated_by` (integer, optional) — Updated by User Details (example: `342552`)
- `shared_list_url` (string, optional) — URL of shared candidate list (example: `https://recruitcrm.io/assigned\_candidates/001`)

#### Example cURL

#### Example cURL

```
curl --request POST \
  --url https://api.recruitcrm.io/v1/candidates/{candidate}/apply \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json'
```

#### Example response

#### Example response

```
{
  "candidate_slug": "1205129",
  "job_slug": "1206683",
  "status": {
    "status_id": 1,
    "label": "Applied"
  },
  "shared_list_url": "https://ss4web.recruitcrm.io/assigned_candidates/709831705571173",
  "remark": "Updated",
  "stage_date": "2020-03-25T16:14:28.000000Z",
  "updated_by": 1234,
  "updated_on": "2020-03-25T16:14:28.000000Z",
  "visibility": 1
}
```
