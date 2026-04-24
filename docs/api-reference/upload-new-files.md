<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/9e9f3cb543d51-upload-new-files -->
<!-- title: Upload new files | API Endpoints -->

# Upload new files

**POST** `/v1/files`

Upload new files to entity file section

## Request

Security: Bearer Auth

### Body

- `File` (optional)
- `related_to` (string, **required**) — Associated entity's slug (example: `23123`)
- `related_to_type` (string, **required**) — Associated entity's Name i.e. candidate/ company/ contact/ job/ deal (example: `candidate`)
- `created_by` (integer, optional)
- `folder` (string, **required**) — Folder to be created or existing folder in which file should be added files\[\] array or string or object Can be Public URLs to files, or Files (form-data) \| Single file shouldn't exceed 15 MB \| The total number of files shouldn't exceed 10, and their combined size should not exceed 32 MB. (example: `folder1`)

## Responses

200

401

429

### Body

- `file_name` (string, optional) — File Name
- `file_link` (string, optional) — File Link
- `created_by` (string, optional) — Created By (example: `10002`)
- `created_on` (string, optional) — Created On (example: `2022-12-02T16:53:27.000000Z`)
- `related_to` (string, optional) — Associated entity's slug (example: `23123`)
- `related_to_type` (string, optional) — Associated entity's Name i.e. candidate/ company/ contact/ job/ deal (example: `candidate`)
- `related` (object, optional) — Details Of Related Entity
- `folder` (string, optional) — Folder name Omit created\_by folder: Omit folder files\[\]\*: (example: `folder1`)

#### Example response

#### Example response

```
{
  "file_name": "string",
  "file_link": "string",
  "created_by": "10002",
  "created_on": "2022-12-02T16:53:27.000000Z",
  "related_to": "23123",
  "related_to_type": "candidate",
  "related": {},
  "folder": "folder1"
}
```
