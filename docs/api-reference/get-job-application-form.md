<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/ef38de0393009-get-job-application-form -->
<!-- title: Get Job Application Form | API Endpoints -->

# Get Job Application Form

**GET** `/v1/jobs/application-form`

Returns the job application form for a job based on the job\_slug.

## Request

Security: Bearer Auth

### Query Parameters

- `job_slug` (string, **required**) — The slug of the job for which to retrieve the application form.

## Responses

200

401

404

### Body

- `message` (string, optional) (example: `success`)
- `data` (object, optional)
- `job_application_form_data` (object, optional)
- `compliance_terms` (object, optional)
- `compliance_settings` (object, optional)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/jobs/application-form \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "message": "success",
  "data": {
    "job_application_form_data": {
      "sections": [
        {
          "title": "Personal Information",
          "subtitle": "Please fill in your personal details",
          "position": 1,
          "required": true,
          "fields": [
            {
              "fieldId": 1,
              "fieldName": "first_name",
              "fieldLabel": "First Name",
              "fieldType": "text",
              "placeholder": "John",
              "required": true,
              "position": 1,
              "defaultValue": null
            }
          ]
        }
      ]
    },
    "compliance_terms": {
      "candidate_terms": "Your custom GDPR terms go here.",
      "eeo_policy": "Your EEO policy text here.",
      "sms_terms": "Your SMS communication terms here."
    },
    "compliance_settings": {
      "candidate_terms": {
        "enabled": true,
        "labels": {
          "agree_to": "I agree to",
          "candidate_terms": "Candidate Terms"
        }
      },
      "eeo_policy": {
        "enabled": true,
        "labels": {
          "view_our": "View Our",
          "eeo": "Equal Employment Opportunity Policy"
        }
      },
      "sms_terms": {
        "enabled": true,
        "labels": {
          "sms_consent_checkbox_label": "I'd like to receive SMS notification about jobs at the provided phone number"
        }
      }
    }
  }
}
```
