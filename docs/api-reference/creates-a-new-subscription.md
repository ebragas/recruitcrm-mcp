<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/5e7ebc825ccf9-creates-a-new-subscription -->
<!-- title: Creates a new subscription | API Endpoints -->

# Creates a new subscription

**POST** `/v1/subscriptions`

List of available events

| Event Name | Event | Resource |
| --- | --- | --- |
| **Candidate Assigned** | candidate.assigned | Candidate |
| **Candidate Created** | candidate.created | Candidate |
| **Candidate Created from Talent Pool** | candidate.created.talentpool | Candidate |
| **Candidate Updated** | candidate.updated | Candidate |
| **Candidate Updated from External Profile Update Form** | candidate.external.profile.updated | Candidate |
| **Candidate Deleted** | candidate.deleted | Candidate |
| **Applied for Job from External Form** | candidate.external.applied.jobs | Candidate |
| **Client Feedback Received** | candidate.clientfeedback.received | Candidate |
| **Candidate's Hiring Stage Updated** | candidate.hiringstage.updated | Candidate |
| **Contact Created** | contact.created | Contact |
| **Contact Updated** | contact.updated | Contact |
| **Contact Deleted** | contact.deleted | Contact |
| **Company Created** | company.created | Company |
| **Company Updated** | company.updated | Company |
| **Company Deleted** | company.deleted | Company |
| **Job Created** | job.created | Job |
| **Job Updated** | job.updated | Job |
| **Job Deleted** | job.deleted | Job |
| **Job Status Updated** | job.status.updated | Job |
| **Deal Created** | deal.created | Deal |
| **Deal Updated** | deal.updated | Deal |
| **Deal Deleted** | deal.deleted | Deal |
| **Deal Stage Updated** | deal.stage.updated | Deal |
| **Meeting Created** | meeting.created | Meeting |
| **Meeting Updated** | meeting.updated | Meeting |
| **Meeting Deleted** | meeting.deleted | Meeting |
| **Task Created** | task.created | Task |
| **Task Updated** | task.updated | Task |
| **Task Deleted** | task.deleted | Task |
| **Note Created** | note.created | Note |
| **Note Updated** | note.updated | Note |
| **Note Deleted** | note.deleted | Note |
| **Call Log Created** | calllog.created | Call Log |
| **Call Log Updated** | calllog.updated | Call Log |
| **Call Log Deleted** | calllog.deleted | Call Log |
| **File Uploaded** | file.uploaded | File |
| **Candidate Opted Out** | candidate.optedout | Candidate |
| **Candidate Opted In** | candidate.optedin | Candidate |
| **Contact Opted Out** | contact.optedout | Contact |
| **Contact Opted In** | contact.optedin | Contact |
| **Candidate Enrolled in Sequence** | candidate.enrolled | Candidate |
| **Candidate Unenrolled from Sequence** | candidate.unenrolled | Candidate |
| **Contact Enrolled in Sequence** | contact.enrolled | Contact |
| **Contact Unenrolled from Sequence** | contact.unenrolled | Contact |
| **Hotlist Created** | hotlist.created | Hotlist |
| **Hotlist Updated** | hotlist.updated | Hotlist |
| **Record Added to Hotlist** | hotlist.record.added | Hotlist |
| **Record Removed from Hotlist** | hotlist.record.removed | Hotlist |
| **Candidate Pitched** | candidate.pitched | Candidate |
| **Pitch Stage Updated** | candidate.pitch.updated | Candidate |
| **Candidate Profile Update Requested** | candidate.profile.update.requested | Candidate |
| **Candidate Unassigned from the Job** | candidate.unassigned | Candidate |
| **Candidate Offlimit Updated** | candidate\_offlimit.updated | Candidate |
| **Company Offlimit Updated** | company\_offlimit.updated | Company |
| **Contact Offlimit Updated** | contact\_offlimit.updated | Contact |
| **Candidate Available** | candidate\_available.removed | Candidate |
| **Company Available** | company\_available.removed | Company |
| **Contact Available** | contact\_available.removed | Contact |
| **Draft Created** | draft.created | Email |
| **Email Sent** | email.sent | Email |
| **Target Achieved** | target.achieved | Target Reports |
| **Timesheet Approved** | timesheet.approved | Timesheet |
| **Placement Created** | placement.created | Placement |
| **Placement Updated** | placement.updated | Placement |
| **Placement Deleted** | placement.deleted | Placement |
| **Invoice Created** | invoice.created | Invoice |
| **Invoice Updated** | invoice.updated | Invoice |
| **Invoice Deleted** | invoice.deleted | Invoice |

## Request

Security: Bearer Auth

### Body

Subscription Object

- `id` (integer, optional) — Subscription ID (example: `56`)
- `event` (string, optional) — Name of Subscribed Event (example: `candidate.created`)
- `target_url` (string, optional) — Subscription URL (example: `https://someurl`)

## Responses

200

401

422

### Body

- `id` (integer, optional) — Subscription ID (example: `56`)
- `event` (string, optional) — Name of Subscribed Event (example: `candidate.created`)
- `target_url` (string, optional) — Subscription URL (example: `https://someurl`)

#### Example request body

#### Example request body

```
{
  "id": 56,
  "event": "candidate.created",
  "target_url": "https://someurl"
}
```

#### Example cURL

#### Example cURL

```
curl --request POST \
  --url https://api.recruitcrm.io/v1/subscriptions \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer 123' \
  --header 'Content-Type: application/json' \
  --data '{
  "id": 56,
  "event": "candidate.created",
  "target_url": "https://someurl"
}'
```

#### Example response

#### Example response

```
{
  "id": 56,
  "event": "candidate.created",
  "target_url": "https://someurl"
}
```
