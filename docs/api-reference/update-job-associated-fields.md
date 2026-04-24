<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/5c2dc8521c9d9-update-job-associated-fields -->
<!-- title: Update Job Associated Fields | API Endpoints -->

# Update Job Associated Fields

**POST** `/v1/candidates/associated-field/{candidate}/{job}`

Update the values of job associated fields for a job.

## Request

Security: Bearer Auth

### Path Parameters

- `candidate` (string, **required**) — slug of the candidate
- `job` (string, **required**) — slug of the job

### Body

Array of job associated fields

- `associated_fields` (optional) — array\[object\]
- `field_id` (number, optional) — Field ID (example: `1`)
- `value` (string, optional) — Value for the Field (example: `I'm from India.`)

## Responses

200

404

### Body

- `success` (boolean, optional) (example: `true`)
- `statusCode` (number, optional) — Success Code (example: `200`)
- `message` (string, optional) — Success Message (example: `Associated Custom fields Updated Successfully`)
- `data` (optional) — array\[object\] 0
- `object` (optional)

#### Example request body

#### Example request body

```
{
  "associated_fields": [
    {
      "field_id": 1,
      "value": "I'm from India."
    }
  ]
}
```

#### Example cURL

#### Example cURL

```
curl --request POST \
  --url https://api.recruitcrm.io/v1/candidates/associated-field/{candidate}/{job} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json' \
  --data '{
  "associated_fields": [\
    {\
      "field_id": 1,\
      "value": "I'\''m from India."\
    }\
  ]
}'
```

#### Example response

#### Example response

```
{
  "success": true,
  "statusCode": 200,
  "message": "Associated Custom fields Updated Successfully",
  "data": [
    {
      "0": {
        "field_id": 1,
        "value": "Value of the field"
      }
    }
  ]
}
```
