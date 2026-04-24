<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/b9174608e937e-upload-call-recordings -->
<!-- title: Upload Call Recordings | API Endpoints -->

# Upload Call Recordings

**POST** `/v1/call-logs/upload-call-recording`

Upload Call Recording to the existing call log.

## Request

Security: Bearer Auth

### Body

- `File` (optional)
- `call_log_id` (integer, **required**) — Call log ID (example: `123`)
- `generate_transcript` (integer, **required**) — Generate transcript flag, 1(yes) or 0(no) (example: `1`)
- `call_recording` (object, **required**) — Can be only Files (form-data) \| Recording shouldn't exceed 25 MB \| The total number of recordings shouldn't exceed 1 \| Accepts only 'mp3','mp4','mpeg','mpga','m4a','wav','webm' formats.
- `updated_by` (string, optional) — ID of the user performing the update (example: `112423`)

## Responses

200

401

404

429

### Body

- `message` (string, optional) — The recording upload is in progress. You can check the status by using the following endpoint: [https://api.recruitcrm.io/v1/call-logs/get-recording-status/{call\_log}](https://api.recruitcrm.io/v1/call-logs/get-recording-status/%7Bcall_log%7D). Omit updated\_by

#### Example cURL

#### Example cURL

```
curl --request POST \
  --url https://api.recruitcrm.io/v1/call-logs/upload-call-recording \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: multipart/form-data' \
  --form call_log_id=123 \
  --form generate_transcript=1 \
  --form call_recording= \
  --form updated_by=
```

#### Example response

#### Example response

```
{
  "message": "string"
}
```
