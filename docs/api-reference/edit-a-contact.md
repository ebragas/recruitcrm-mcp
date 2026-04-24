<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/671e42107de3b-edit-a-contact -->
<!-- title: Edit a contact | API Endpoints -->

# Edit a contact

**POST** `/v1/contacts/{contact}`

Edit a contact.

## Request

Security: Bearer Auth

### Path Parameters

- `contact` (string, **required**) — slug of the contact to edit

### Body

Contact Object

- `first_name` (string, optional) — >= 1 characters
- `last_name` (string, optional) — >= 1 characters
- `email` (string, optional) — >= 1 characters
- `contact_number` (string, optional) — >= 1 characters
- `company_slug` (string, optional) — Comma separated company slugs
- `avatar` (string, optional)
- `city` (string, optional) — >= 1 characters
- `locality` (string, optional)
- `state` (string, optional) — >= 1 characters
- `country` (string, optional) — >= 1 characters
- `postal_code` (string, optional) — >= 1 characters
- `address` (string, optional)
- `designation` (string, optional) — Designation of the contact \| This is title field >= 1 characters
- `facebook` (string, optional) — >= 1 characters
- `twitter` (string, optional)
- `linkedin` (string, optional)
- `stage_id` (number, optional)
- `owner_id` (integer, optional)
- `created_by` (integer, optional)
- `updated_by` (integer, optional)
- `custom_fields` (optional) — array\[object\] >= 1 items
- `field_id` (number, optional)
- `value` (string, optional) — >= 1 characters

## Responses

200

401

422

### Body

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
- `state` (string, optional) — State of the contact (example: `New York`)
- `country` (string, optional) — Country of the contact (example: `United States`)
- `postal_code` (string, optional) — Postal Code of the contact (example: `110001`)
- `address` (string, optional) — Address of the contact (example: `designation`)
- `string` (optional) — Designation of the contact \| This is title field (example: `HR Manager`)
- `custom_fields` (optional) — array\[object\] Array of Custom Fields (example: `\[{"field\_id":1,"value":"Region 1"}\]`)
- `field_id` (integer, optional) — Field ID
- `value` (string, optional) — Custom Value
- `created_by` (string, optional) — Created By (example: `134352`)
- `updated_by` (string, optional) — Updated By (example: `243432`)
- `owner` (string, optional)
- `Owner` (optional) (example: `32434`)
- `resource_url` (string, optional) — Resource Url
- `is_email_opted_out` (boolean, optional) — Opt out status (example: `true`)
- `email_opt_out_source` (string, optional) — Opted out source. Manually opted out or Unsubscribed (example: `Manually opted out`)
- `last_calllog_added_on` (string, optional) — Last call log added date (example: `2024-06-05T15:15:00.000000Z`)
- `last_calllog_added_by` (integer, optional) — Updated By user details (example: `5`)
- `last_meeting_created_on` (string, optional) — Last meeting added date (example: `2024-06-05T15:15:00.000000Z`)
- `last_meeting_created_by` (integer, optional) — Updated By user details (example: `5`)
- `last_linkedin_message_sent_on` (string, optional) — Last linkedin message sent on date (example: `2024-06-05T15:15:00.000000Z`)
- `last_linkedin_message_sent_by` (integer, optional) — Updated By user details (example: `5`)
- `last_email_sent_on` (string, optional) — Last email sent on date (example: `2024-06-05T15:15:00.000000Z`)
- `last_email_sent_by` (integer, optional) — Updated By user details (example: `5`)
- `last_sms_sent_on` (string, optional) — Last sms sent on date (example: `2024-06-05T15:15:00.000000Z`)
- `last_sms_sent_by` (integer, optional) — Updated By user details (example: `5`)
- `last_communication` (string, optional) — Last communication method (example: `SMS on 2024-06-05 15:15:00`)
- `status_label` (string, optional) — Off Limit Status (example: `Unavailable`)
- `off_limit_end_date` (string, optional) — Off Limit End Date (example: `2020-06-29T05:36:22.000000Z`)
- `off_limit_reason` (string, optional) — Off Limit Reason (example: `testing`)

#### Example request body

#### Example request body

```
{
  "first_name": "Ryan",
  "last_name": "Cooper",
  "email": "ryan.cooper@example.com",
  "contact_number": "+1233345",
  "company_slug": "16601029339250000005ONm,16600418761900000005jtE",
  "avatar": "",
  "city": "New York",
  "locality": "",
  "address": "",
  "designation": "HR Manager",
  "facebook": "https://www.facebook.com/ryan",
  "twitter": "",
  "linkedin": "",
  "stage_id": 23,
  "custom_fields": [
    {
      "field_id": 1,
      "value": "AC-9"
    }
  ]
}
```

#### Example cURL

#### Example cURL

```
curl --request POST \
  --url https://api.recruitcrm.io/v1/contacts/{contact} \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json' \
  --data '{
  "first_name": "Ryan",
  "last_name": "Cooper",
  "email": "ryan.cooper@example.com",
  "contact_number": "+1233345",
  "company_slug": "16601029339250000005ONm,16600418761900000005jtE",
  "avatar": "",
  "city": "New York",
  "locality": "",
  "address": "",
  "designation": "HR Manager",
  "facebook": "https://www.facebook.com/ryan",
  "twitter": "",
  "linkedin": "",
  "stage_id": 23,
  "custom_fields": [\
    {\
      "field_id": 1,\
      "value": "AC-9"\
    }\
  ]
}'
```

#### Example response

#### Example response

```
{
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
  "state": "New York",
  "country": "United States",
  "postal_code": "110001",
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
  "email_opt_out_source": "Manually opted out",
  "last_calllog_added_on": "2024-06-05T15:15:00.000000Z",
  "last_calllog_added_by": 5,
  "last_meeting_created_on": "2024-06-05T15:15:00.000000Z",
  "last_meeting_created_by": 5,
  "last_linkedin_message_sent_on": "2024-06-05T15:15:00.000000Z",
  "last_linkedin_message_sent_by": 5,
  "last_email_sent_on": "2024-06-05T15:15:00.000000Z",
  "last_email_sent_by": 5,
  "last_sms_sent_on": "2024-06-05T15:15:00.000000Z",
  "last_sms_sent_by": 5,
  "last_communication": "SMS on 2024-06-05 15:15:00",
  "status_label": "Unavailable",
  "off_limit_end_date": "2020-06-29T05:36:22.000000Z",
  "off_limit_reason": "testing"
}
```
