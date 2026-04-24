<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/95268edc15396-hiring-stage-of-candidate-for-job -->
<!-- title: Hiring Stage of Candidate for Job | API Endpoints -->

# Hiring Stage of Candidate for Job

**GET** `/v1/candidates/{candidate}/hiring-stages/{job}`

Returns the hiring stage of a candidate for a particular job.

## Request

Security: Bearer Auth

### Path Parameters

- `candidate` (string, **required**) — slug of the candidate
- `job` (string, **required**) — slug of the job

## Responses

200

404

### Body

- `candidate_slug` (string, optional) — Candidate's Slug (example: `1205129`)
- `job_slug` (string, optional) — Job's Slug (example: `1206683`)
- `status` (object, optional) — Candidate's status (example: `{"status\_id":1,"label":"Assigned"}`)
- `remark` (string, optional)
- `Remark` (optional) (example: `Updated`)
- `stage_date` (string, optional) — Updated Date (example: `2020-03-25T16:14:28.000000Z`)
- `visibility` (integer, optional) — Candidate's visibility in a job: For On - 1, Off - 0 (example: `1`)
- `shared_list_url` (string, optional) — URL of shared candidate list (example: `https://recruitcrm.io/assigned\_candidates/001`)
- `updated_on` (string, optional) — Record Updated Date (example: `2020-03-25T16:14:28.000000Z`)
- `updated_by` (object, optional) — Updated by User Details (example: `{"id":123,"first\_name":"Erica","last\_name":null,"email":"erica@yopmail.com","contact\_number":null,"avatar":null}`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/candidates/{candidate}/hiring-stages/{job} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "candidate_slug": "1205129",
  "job_slug": "1206683",
  "status": {
    "status_id": 1,
    "label": "Assigned"
  },
  "remark": "Updated",
  "stage_date": "2020-03-25T16:14:28.000000Z",
  "visibility": 1,
  "shared_list_url": "https://recruitcrm.io/assigned_candidates/001",
  "updated_on": "2020-03-25T16:14:28.000000Z",
  "updated_by": {
    "id": 123,
    "first_name": "Erica",
    "last_name": null,
    "email": "erica@yopmail.com",
    "contact_number": null,
    "avatar": null
  }
}
```
