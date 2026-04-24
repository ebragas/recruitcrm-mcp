<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/06eff219fead1-get-proficiencies -->
<!-- title: Get Proficiencies | API Endpoints -->

# Get Proficiencies

**GET** `/v1/proficiencies`

Returns a list of proficiencies

## Request

Security: Bearer Auth

## Responses

200

401

### Body

- `proficiency_id` (integer, optional) (example: `6`)
- `label` (string, optional) — Proficiency Label (example: `Native or bilingual proficiency`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/proficiencies \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "proficiency_id": 6,
  "label": "Native or bilingual proficiency"
}
```
