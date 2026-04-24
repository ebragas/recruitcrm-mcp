<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/138393e87f484-get-compliance-terms -->
<!-- title: Get compliance terms | API Endpoints -->

# Get compliance terms

**GET** `/v1/jobs/compliance-terms`

Returns candidate GDPR, EEO policy, and SMS terms.

## Request

Security: Bearer Auth

## Responses

200

401

### Body

- `candidate_terms` (string, optional) (example: `Your custom GDPR terms go here.`)
- `eeo_policy` (string, optional) (example: `Your EEO policy text here.`)
- `sms_terms` (string, optional) (example: `Your SMS communication terms here.`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/jobs/compliance-terms \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "candidate_terms": "Your custom GDPR terms go here.",
  "eeo_policy": "Your EEO policy text here.",
  "sms_terms": "Your SMS communication terms here."
}
```
