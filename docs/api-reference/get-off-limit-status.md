<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/93cc0afd8838c-get-off-limit-status -->
<!-- title: Get Off Limit Status | API Endpoints -->

# Get Off Limit Status

**GET** `/v1/off-limit-status`

Returns a list of Off Limit Status

## Request

Security: Bearer Auth

## Responses

200

401

### Body

- `id` (integer, optional) — Status ID (example: `3`)
- `status_label` (string, optional) — Status Label (example: `Unavailable`)
- `status_colour_id` (string, optional) — Status Colour Code (example: `F2`)
- `sequence_no` (integer, optional) — Sequence No (example: `1`)
- `account_id` (integer, optional) — Account Id (example: `5`)
- `default` (integer, optional) — Is Status Default (example: `1`)
- `offlimit_status_colour_id` (string, optional) — Status Colour Code (example: `F2`)
- `background_color_hex` (string, optional) — Status Background Color (example: `#F3F4F6`)
- `text_color_hex` (string, optional) — Status Text Color (example: `686869`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/off-limit-status \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "id": 3,
  "status_label": "Unavailable",
  "status_colour_id": "F2",
  "sequence_no": 1,
  "account_id": 5,
  "default": 1,
  "offlimit_status_colour_id": "F2",
  "background_color_hex": "#F3F4F6",
  "text_color_hex": "686869"
}
```
