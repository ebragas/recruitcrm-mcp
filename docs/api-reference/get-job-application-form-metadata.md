<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/dec5b8af178d1-get-job-application-form-metadata -->
<!-- title: Get job application form metadata | API Endpoints -->

# Get job application form metadata

**GET** `/v1/jobs/application-form-metadata`

Provides social media sharing text and image metadata for the job application form.

## Request

Security: Bearer Auth

## Responses

200

401

### Body

- `social_sharing_apply_to` (string, optional) (example: `string`)
- `social_sharing_with` (string, optional) (example: `string`)
- `image_url` (optional) — string<uri> (example: `https://example.com/social-job-image.png`)
- `image_filename` (string, optional) (example: `social-job-image.png`)

#### Example cURL

#### Example cURL

```
curl --request GET \
  --url https://api.recruitcrm.io/v1/jobs/application-form-metadata \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123'
```

#### Example response

#### Example response

```
{
  "social_sharing_apply_to": "string",
  "social_sharing_with": "string",
  "image_url": "https://example.com/social-job-image.png",
  "image_filename": "social-job-image.png"
}
```
