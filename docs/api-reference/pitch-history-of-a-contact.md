<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/6b6b8678000d2-pitch-history-of-a-contact -->
<!-- title: Pitch History of a Contact | API Endpoints -->

# Pitch History of a Contact

**GET** `/v1/pitch/pitch-contact-history/{contact}`

Get Pitch History of a Contact

## Request

Security: Bearer Auth

### Path Parameters

- `contact` (string, **required**) — Contact's Slug

## Responses

200

404

History fetched successfully

### Body

- `data` (object, optional)
- `records` (optional) — array\[PitchContactHistory\]
- `message` (string, optional)
- `status` (string, optional) — status code
- `integer` (optional)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/pitch/pitch-contact-history/{contact} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "data": {
    "records": [
      {
        "candidate_slug": "18390671235850000005LSk",
        "status_id": 1,
        "candidate_status": "Pitched",
        "remark": "It is marked as pitched",
        "stage_date": "2023-06-29T05:36:22.000000Z",
        "updated_by": 5,
        "created_on": "2023-06-29T05:36:22.000000Z",
        "updated_on": "2023-06-29T05:36:22.000000Z"
      }
    ]
  },
  "message": "string",
  "status": "string",
  "status code": 0
}
```
