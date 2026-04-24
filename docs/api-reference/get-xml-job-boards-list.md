<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/9cafccc5e57ac-get-xml-job-boards-list -->
<!-- title: Get XML Job-Boards List | API Endpoints -->

# Get XML Job-Boards List

**GET** `/v1/jobs/list-xml-jobboards`

## Request

Security: Bearer Auth

## Responses

200

401

### Body

- `default_xml_feeds` (optional) — array\[object\]
- `id` (integer, optional) — ID of Jobboard (example: `1`)
- `label` (string, optional) — Label of Jobboard (example: `Indeed`)
- `custom_xml_feeds` (optional) — array\[object\]
- `id` (integer, optional) — ID of Jobboard (example: `322`)
- `label` (string, optional) — Label Of Jobboard (example: `CustomXML`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/jobs/list-xml-jobboards \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "default_xml_feeds": [
    {
      "id": 1,
      "label": "Free Job Boards"
    }
  ],
  "custom_xml_feeds": [
    {
      "id": 11,
      "label": "Xing 323"
    },
    {
      "id": 27,
      "label": "test"
    }
  ]
}
```
