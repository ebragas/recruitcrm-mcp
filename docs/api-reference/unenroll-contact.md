<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/12df69e422a76-unenroll-contact -->
<!-- title: Unenroll Contact | API Endpoints -->

# Unenroll Contact

**POST** `/v1/contacts/{contact}/un-enroll`

Unenroll a contact from a Sequence.

## Request

Security: Bearer Auth

### Path Parameters

- `contact` (string, **required**) — Slug of the contact

### Query Parameters

- `unenrolled_by` (integer, optional) — ID of the user

## Responses

200

401

422

### Body

- `id` (integer, optional) — Enrollment ID (example: `1`)
- `sequence_id` (integer, optional) — Sequence ID (example: `124`)
- `enrolled_by` (integer, optional) — Enrolled By (example: `10002`)
- `unenrolled_by` (integer, optional) — Unenrolled By (example: `10002`)
- `enrolled_on` (string, optional) — Enrolled On (example: `2022-12-02T16:53:27.000000Z`)
- `unenrolled_on` (string, optional) — Unenrolled On (example: `2022-12-02T16:53:27.000000Z`)
- `status` (object, optional) — Enrollment's status (example: `{"status\_id":1,"label":"ACTIVE"}`)
- `prospect_slug` (string, optional) — Prospect slug (example: `16318617835190000051Ond`)
- `prospect` (object, optional)
- `id` (integer, optional) — Contact's ID (example: `2`)
- `first_name` (string, optional) — Contact's First Name (example: `Michael`)
- `last_name` (string, optional) — Contact's Last Name (example: `Scott`)
- `email` (string, optional) — Contact's Valid E-Mail (example: `mscott@gmail.com`)
- `contact_number` (string, optional) — Contact's Contact Number (example: `+1123226666`)
- `avatar` (string, optional) — Contact's Avatar URL
- `slug` (string, optional) — Contact's slug
- `company_slug` (string, optional) — Associated company's slug
- `additional_company_slugs` (string, optional) — Associated company's slug
- `created_on` (string, optional) — Created On (example: `2020-06-29T05:36:22.000000Z`)
- `updated_on` (string, optional) — Updated On (example: `2020-06-29T05:36:22.000000Z`)
- `stage_id` (integer, optional) — Contact's stage
- `facebook` (string, optional) — Facebook Profile URL of the contact (example: `http://www.facebook.com/michael4`)
- `twitter` (string, optional) — Twitter Profile URL of the contact (example: `http://www.twitter.com/michael4`)
- `linkedin` (string, optional) — Linked In Profile URL of the contact (example: `http://www.linkedin.com/michael4`)
- `xing` (string, optional) — Xing Profile URL of the contact (example: `http://www.xing.com/xyz`)
- `city` (string, optional) — City of the contact (example: `New York`)
- `locality` (string, optional) — Locality of the contact (example: `Manhattan`)
- `address` (string, optional) — Address of the contact (example: `designation`)
- `string` (optional) — Designation of the contact \| This is title field (example: `HR Manager`)
- `custom_fields` (optional) — array\[object\] Array of Custom Fields (example: `\[{"field\_id":1,"value":"Region 1"}\]`)
- `created_by` (string, optional) — Created By (example: `134352`)
- `updated_by` (string, optional) — Updated By (example: `243432`)
- `owner` (string, optional)
- `Owner` (optional) (example: `32434`)
- `resource_url` (string, optional) — Resource Url
- `is_email_opted_out` (boolean, optional) — Opt out status (example: `true`)
- `email_opt_out_source` (string, optional) — Opted out source. Manually opted out or Unsubscribed (example: `Manually opted out`)

#### Example cURL

#### Example cURL

```
curl --request POST \
  --url https://api.recruitcrm.io/v1/contacts/{contact}/un-enroll \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json'
```

#### Example response

#### Example response

```
{
  "id": 1,
  "sequence_id": 124,
  "enrolled_by": 10002,
  "unenrolled_by": 10002,
  "enrolled_on": "2022-12-02T16:53:27.000000Z",
  "unenrolled_on": "2022-12-02T16:53:27.000000Z",
  "status": {
    "status_id": 1,
    "label": "ACTIVE"
  },
  "prospect_slug": "16318617835190000051Ond",
  "prospect": {
    "id": 2,
    "first_name": "Michael",
    "last_name": "Scott",
    "email": "mscott@gmail.com",
    "contact_number": "+1123226666",
    "avatar": "string",
    "slug": "string",
    "company_slug": "string",
    "additional_company_slugs": "string",
    "created_on": "2020-06-29T05:36:22.000000Z",
    "updated_on": "2020-06-29T05:36:22.000000Z",
    "stage_id": 0,
    "facebook": "http://www.facebook.com/michael4",
    "twitter": "http://www.twitter.com/michael4",
    "linkedin": "http://www.linkedin.com/michael4",
    "xing": "http://www.xing.com/xyz",
    "city": "New York",
    "locality": "Manhattan",
    "address": "",
    "designation": "HR Manager",
    "custom_fields": [
      {
        "field_id": 1,
        "value": "Region 1"
      }
    ],
    "created_by": "134352",
    "updated_by": "243432",
    "owner": "32434",
    "resource_url": "string",
    "is_email_opted_out": true,
    "email_opt_out_source": "Manually opted out"
  }
}
```
