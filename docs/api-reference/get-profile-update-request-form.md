<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/ae5087c9fefd9-get-profile-update-request-form -->
<!-- title: Get Profile Update Request Form | API Endpoints -->

# Get Profile Update Request Form

**GET** `/v1/candidates/profile-update-request-form`

Returns the profile update request form

## Request

Security: Bearer Auth

## Responses

200

401

404

### Body

- `message` (string, optional) (example: `success`)
- `data` (object, optional)
- `profile_update_setting_form_data` (object, optional)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/candidates/profile-update-request-form \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "message": "success",
  "data": {
    "profile_update_setting_form_data": {
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
    }
  }
}
```
