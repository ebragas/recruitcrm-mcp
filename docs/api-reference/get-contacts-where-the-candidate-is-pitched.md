<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/93feac6b9c6e8-get-contacts-where-the-candidate-is-pitched -->
<!-- title: Get contacts where the candidate is pitched | API Endpoints -->

# Get contacts where the candidate is pitched

**GET** `/v1/pitch/{entity}/pitch-stage/{entitySlug}`

Get the contacts where the candidate is pitched or Get candidates pitched to the Contact

## Request

Security: Bearer Auth

### Path Parameters

- `entity` (string, **required**) — Entity - candidate/contact candidate(Get contacts where the candidate is pitched) Or contact(Get candidates pitched to the Contact)
- `entitySlug` (string, **required**) — Add Candidate Slug if entity is candidate or add Contact Slug if entity is contact

## Responses

200

404

### Body

- `status` (string, optional)
- `statusCode` (integer, optional)
- `data` (object, optional)
- `records` (optional) — array\[PitchCandidateData\]

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/pitch/{entity}/pitch-stage/{entitySlug} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "status": "string",
  "statusCode": 0,
  "data": {
    "records": [
      {
        "candidate_slug": "16448144215000000005eFC",
        "contact_slug": "16739479639090000005Vsm",
        "stage_date": "2023-12-15T15:26:45.000000Z",
        "status_id": 1,
        "candidate_status": "Pitched",
        "remark": "Remark addded",
        "contact_title": "string",
        "contact_profile_pic": "string",
        "contact_name": "Nicole",
        "contact_email": "nicole@gmail.com",
        "contact_number": "7891781919",
        "candidate_profile_pic": "string",
        "candidate_name": "Wyn Mattheis",
        "candidate_email": "wyn@testmail.com",
        "candidate_contact_number": 62819910101,
        "resume": "string",
        "candidate_position": "Development team lead",
        "created_by": "5",
        "created_on": "2023-12-15T15:26:45.000000Z",
        "updated_by": "1001",
        "updated_on": "2023-12-15T15:26:45.000000Z",
        "resume_file_name": "string",
        "candidate_email_opt_out": "0",
        "contact_email_opt_out": "0"
      }
    ]
  }
}
```
