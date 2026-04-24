<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/4f06631a33328-get-hiring-pipeline-stages-for-a-pipeline -->
<!-- title: Get Hiring Pipeline Stages For A Pipeline | API Endpoints -->

# Get Hiring Pipeline Stages For A Pipeline

**GET** `/v1/hiring-pipelines/{id}`

Returns a list of hiring stages for the requested pipeline

## Request

Security: Bearer Auth

### Path Parameters

- `id` (integer, **required**) — ID of the hiring pipeline whose stages needs to be returned. 0 is for Master Hiring Pipeline

## Responses

200

401

422

### Body

- `stage_id` (integer, optional) — Stage ID (example: `56`)
- `label` (string, optional) — Stage Label (example: `Lead`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/hiring-pipelines/{id} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "stage_id": 56,
  "label": "Lead"
}
```
