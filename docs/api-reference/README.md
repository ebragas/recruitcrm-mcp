# Recruit CRM API Reference

Locally cached copy of the Recruit CRM API documentation.
Source: https://docs.recruitcrm.io/docs/rcrm-api-reference/9033e3227d21f-recruit-crm-api

- **Base URL:** `https://api.recruitcrm.io`
- **Auth:** `Authorization: Bearer <RECRUIT_CRM_API_KEY>`

Each page below is a tidied markdown copy of the original Stoplight doc.

## Contents

- [Intro](#intro)
- [Candidates](#candidates)
- [Contacts](#contacts)
- [Companies](#companies)
- [Jobs](#jobs)
- [Deals](#deals)
- [Tasks](#tasks)
- [Meetings](#meetings)
- [Notes](#notes)
- [Call Logs](#call-logs)
- [Hotlists](#hotlists)
- [Custom Fields](#custom-fields)
- [Webhook Subscriptions](#webhook-subscriptions)
- [Sequences](#sequences)
- [Timesheets](#timesheets)
- [Placements](#placements)
- [Invoices](#invoices)
- [Nested Custom Fields](#nested-custom-fields)
- [Lists](#lists)
- [List Off Limit Status](#list-off-limit-status)
- [Users](#users)
- [Files](#files)
- [Email](#email)

## Intro

- [Recruit CRM API](recruit-crm-api.md)
- [Getting Started](getting-started.md)
- [Authentication](authentication.md)
- [Rate Limiting](rate-limiting.md)
- [Custom Field Search](custom-field-search.md)

## Candidates

| Method | Path | Doc |
|---|---|---|
| GET | `/v1/candidates` | [Show all candidates](show-all-candidates.md) |
| POST | `/v1/candidates` | [Creates a new candidate](creates-a-new-candidate.md) |
| GET | `/v1/candidates/{candidate}` | [Find candidate by slug](find-candidate-by-slug.md) |
| POST | `/v1/candidates/{candidate}` | [Edit a candidate](edit-a-candidate.md) |
| DELETE | `/v1/candidates/{candidate}` | [Delete a candidate](delete-a-candidate.md) |
| GET | `/v1/candidates/search` | [Search for candidates](search-for-candidates.md) |
| POST | `/v1/candidates/resume-parser` | [Resume Parser](resume-parser.md) |
| POST | `/v1/candidates/{candidate}/assign` | [Assign Candidate](assign-candidate.md) |
| POST | `/v1/candidates/{candidate}/unassign` | [Un-assign Candidate](un-assign-candidate.md) |
| POST | `/v1/candidates/{candidate}/apply` | [Apply to Job](apply-to-job.md) |
| POST | `/v1/candidates/{candidate}/visibility/{job}` | [Update Candidate Visibility in a Job](update-candidate-visibility-in-a-job.md) |
| POST | `/v1/candidates/mark-off-limit` | [Mark Candidate as Off Limit](mark-candidate-as-off-limit.md) |
| POST | `/v1/candidates/mark-as-available` | [Mark Candidate as Available](mark-candidate-as-available.md) |
| GET | `/v1/candidates/off-limit` | [Get List of candidates which are marked as off limit](get-list-of-candidates-which-are-marked-as-off-limit.md) |
| GET | `/v1/candidates/{candidate}/off-limit-history` | [Off Limit History for Candidate](off-limit-history-for-candidate.md) |
| GET | `/v1/candidates/{candidate}/hiring-stages` | [Hiring Stages of Candidate](hiring-stages-of-candidate.md) |
| GET | `/v1/candidates/{candidate}/hiring-stages/{job}` | [Hiring Stage of Candidate for Job](hiring-stage-of-candidate-for-job.md) |
| POST | `/v1/candidates/{candidate}/hiring-stages/{job}` | [Update Candidate Hiring Stage](update-candidate-hiring-stage.md) |
| GET | `/v1/candidates/{candidate}/history` | [Candidate History](candidate-history.md) |
| GET | `/v1/candidates/{candidate}/request-update` | [Request Updated Profile](request-updated-profile.md) |
| GET | `/v1/candidates/profile-update-request-form` | [Get Profile Update Request Form](get-profile-update-request-form.md) |
| POST | `/v1/candidates/work-history/create` | [Add Work Experience](add-work-experience.md) |
| POST | `/v1/candidates/work-history/{workId}` | [Edit Work Experience](edit-work-experience.md) |
| DELETE | `/v1/candidates/work-history/{workId}` | [Delete a candidate work experience](delete-a-candidate-work-experience.md) |
| GET | `/v1/candidates/{candidate}/work-history` | [Candidate Work Experience](candidate-work-experience.md) |
| POST | `/v1/candidates/education-history/create` | [Add Education History](add-education-history.md) |
| POST | `/v1/candidates/education-history/{educationId}` | [Edit Education History](edit-education-history.md) |
| DELETE | `/v1/candidates/education-history/{educationId}` | [Delete a candidate Education History](delete-a-candidate-education-history.md) |
| GET | `/v1/candidates/{candidate}/education-history` | [Candidate Education History](candidate-education-history.md) |
| GET | `/v1/candidates/question-and-answers/{candidate}` | [Question And Answers of Candidate](question-and-answers-of-candidate.md) |
| POST | `/v1/candidates/question-and-answers/{candidate}` | [Update Candidate Answers for the Questions](update-candidate-answers-for-the-questions.md) |
| GET | `/v1/candidates/question-and-answers/{candidate}/{job}` | [Question And Answers of Candidate for Job](question-and-answers-of-candidate-for-job.md) |
| POST | `/v1/candidates/question-and-answers/{candidate}/{job}` | [Update Candidate Answers for the Questions for a Job](update-candidate-answers-for-the-questions-for-a-job.md) |
| GET | `/v1/candidates/associated-field/{candidate}/{job}` | [Get Job Associated Fields](get-job-associated-fields.md) |
| POST | `/v1/candidates/associated-field/{candidate}/{job}` | [Update Job Associated Fields](update-job-associated-fields.md) |
| POST | `/v1/pitch/{candidate}/contact/{contact}` | [Pitch candidate to contact](pitch-candidate-to-contact.md) |
| GET | `/v1/pitch/pitch-candidate-history/{candidate}` | [Pitch History of a Candidate](pitch-history-of-a-candidate.md) |
| GET | `/v1/pitch/pitch-contact-history/{contact}` | [Pitch History of a Contact](pitch-history-of-a-contact.md) |
| GET | `/v1/pitch/{candidate}/history/{contact}` | [Pitch History of a Candidate and Contact](pitch-history-of-a-candidate-and-contact.md) |
| POST | `/v1/pitch/{candidate}/updated-stage/{contact}` | [Update Pitch stage](update-pitch-stage.md) |
| GET | `/v1/pitch/{entity}/pitch-stage/{entitySlug}` | [Get contacts where the candidate is pitched](get-contacts-where-the-candidate-is-pitched.md) |

## Contacts

| Method | Path | Doc |
|---|---|---|
| GET | `/v1/contacts` | [Show all contacts](show-all-contacts.md) |
| POST | `/v1/contacts` | [Creates a new contact](creates-a-new-contact.md) |
| GET | `/v1/contacts/{contact}` | [Find contact by slug](find-contact-by-slug.md) |
| POST | `/v1/contacts/{contact}` | [Edit a contact](edit-a-contact.md) |
| DELETE | `/v1/contacts/{contact}` | [Delete a contact](delete-a-contact.md) |
| GET | `/v1/contacts/search` | [Search for contacts](search-for-contacts.md) |
| POST | `/v1/contacts/mark-off-limit` | [Mark Contacts as Off Limit](mark-contacts-as-off-limit.md) |
| POST | `/v1/contacts/mark-as-available` | [Mark Contacts as Available](mark-contacts-as-available.md) |
| GET | `/v1/contacts/off-limit` | [Get List of Contacts which are marked as off limit](get-list-of-contacts-which-are-marked-as-off-limit.md) |
| GET | `/v1/contacts/{contact}/off-limit-history` | [Off Limit History for Contact](off-limit-history-for-contact.md) |

## Companies

| Method | Path | Doc |
|---|---|---|
| GET | `/v1/companies` | [Show all companies](show-all-companies.md) |
| POST | `/v1/companies` | [Creates a new company](creates-a-new-company.md) |
| GET | `/v1/companies/{company}` | [Find company by slug](find-company-by-slug.md) |
| POST | `/v1/companies/{company}` | [Edit a company](edit-a-company.md) |
| DELETE | `/v1/companies/{company}` | [Delete a company](delete-a-company.md) |
| GET | `/v1/companies/search` | [Search for companies](search-for-companies.md) |
| POST | `/v1/companies/mark-off-limit` | [Mark Companies as Off Limit](mark-companies-as-off-limit.md) |
| POST | `/v1/companies/mark-as-available` | [Mark Companies as Available](mark-companies-as-available.md) |
| GET | `/v1/companies/off-limit` | [Get List of Companies which are marked as off limit](get-list-of-companies-which-are-marked-as-off-limit.md) |
| GET | `/v1/companies/{company}/off-limit-history` | [Off Limit History for Company](off-limit-history-for-company.md) |

## Jobs

| Method | Path | Doc |
|---|---|---|
| GET | `/v1/jobs` | [Show all Jobs](show-all-jobs.md) |
| POST | `/v1/jobs` | [Creates a new Job](creates-a-new-job.md) |
| GET | `/v1/jobs/{job}` | [Find job by slug](find-job-by-slug.md) |
| POST | `/v1/jobs/{job}` | [Edit a Job](edit-a-job.md) |
| DELETE | `/v1/jobs/{job}` | [Delete a Job](delete-a-job.md) |
| GET | `/v1/jobs/search` | [Search for jobs](search-for-jobs.md) |
| GET | `/v1/jobs/{job}/assigned-candidates` | [Assigned candidates for job](assigned-candidates-for-job.md) |
| GET | `/v1/jobs/{job}/stage-history/{candidate}` | [Stage History of Candidate for job](stage-history-of-candidate-for-job.md) |
| GET | `/v1/jobs/application-form` | [Get Job Application Form](get-job-application-form.md) |
| GET | `/v1/jobs/application-form-metadata` | [Get job application form metadata](get-job-application-form-metadata.md) |
| GET | `/v1/jobs/list-xml-jobboards` | [Get XML Job-Boards List](get-xml-job-boards-list.md) |
| GET | `/v1/jobs/compliance-terms` | [Get compliance terms](get-compliance-terms.md) |

## Deals

| Method | Path | Doc |
|---|---|---|
| GET | `/v1/deals` | [Show all Deals](show-all-deals.md) |
| POST | `/v1/deals` | [Creates a new Deal](creates-a-new-deal.md) |
| GET | `/v1/deals/{deal}` | [Find deal by slug](find-deal-by-slug.md) |
| POST | `/v1/deals/{deal}` | [Edit a deal](edit-a-deal.md) |
| DELETE | `/v1/deals/{deal}` | [Delete a deal](delete-a-deal.md) |
| GET | `/v1/deals/search` | [Search for deals](search-for-deals.md) |

## Tasks

| Method | Path | Doc |
|---|---|---|
| GET | `/v1/tasks` | [Show all tasks](show-all-tasks.md) |
| POST | `/v1/tasks` | [Creates a new task](creates-a-new-task.md) |
| GET | `/v1/tasks/{task}` | [Find task by ID](find-task-by-id.md) |
| POST | `/v1/tasks/{task}` | [Edit task](edit-task.md) |
| DELETE | `/v1/tasks/{task}` | [Delete a task](delete-a-task.md) |
| GET | `/v1/tasks/search` | [Search for tasks](search-for-tasks.md) |

## Meetings

| Method | Path | Doc |
|---|---|---|
| GET | `/v1/meetings` | [Show all meetings](show-all-meetings.md) |
| POST | `/v1/meetings` | [Creates a new meeting](creates-a-new-meeting.md) |
| GET | `/v1/meetings/{meeting}` | [Find meeting by ID](find-meeting-by-id.md) |
| POST | `/v1/meetings/{meeting}` | [Edit meeting](edit-meeting.md) |
| DELETE | `/v1/meetings/{meeting}` | [Delete a meeting](delete-a-meeting.md) |
| GET | `/v1/meetings/search` | [Search for meetings](search-for-meetings.md) |

## Notes

| Method | Path | Doc |
|---|---|---|
| GET | `/v1/notes` | [Show all Notes](show-all-notes.md) |
| POST | `/v1/notes` | [Creates a new Note](creates-a-new-note.md) |
| GET | `/v1/notes/{note}` | [Find note by ID](find-note-by-id.md) |
| POST | `/v1/notes/{note}` | [Edit a note](edit-a-note.md) |
| DELETE | `/v1/notes/{note}` | [Delete a note](delete-a-note.md) |
| GET | `/v1/notes/search` | [Search for notes](search-for-notes.md) |

## Call Logs

| Method | Path | Doc |
|---|---|---|
| GET | `/v1/call-logs` | [Show all Call Logs](show-all-call-logs.md) |
| POST | `/v1/call-logs` | [Creates a new Call Log](creates-a-new-call-log.md) |
| GET | `/v1/call-logs/{call\_log}` | [Find call log by ID](find-call-log-by-id.md) |
| POST | `/v1/call-logs/{call\_log}` | [Edit a call log](edit-a-call-log.md) |
| DELETE | `/v1/call-logs/{call\_log}` | [Delete a call log](delete-a-call-log.md) |
| GET | `/v1/call-logs/search` | [Search for call logs](search-for-call-logs.md) |
| GET | `/v1/call-logs/get-recording-status/{call\_log}` | [Get Call Recording Upload Status](get-call-recording-upload-status.md) |
| POST | `/v1/call-logs/upload-call-recording` | [Upload Call Recordings](upload-call-recordings.md) |

## Hotlists

| Method | Path | Doc |
|---|---|---|
| GET | `/v1/hotlists` | [Show all Hotlists](show-all-hotlists.md) |
| POST | `/v1/hotlists` | [Creates a new Hotlist](creates-a-new-hotlist.md) |
| GET | `/v1/hotlists/{hotlist}` | [Find hotlist by ID](find-hotlist-by-id.md) |
| POST | `/v1/hotlists/{hotlist}` | [Edit a hotlist](edit-a-hotlist.md) |
| DELETE | `/v1/hotlists/{hotlist}` | [Delete a hotlist](delete-a-hotlist.md) |
| POST | `/v1/hotlists/{hotlist}/add-record` | [Add records to Hotlist](add-records-to-hotlist.md) |
| POST | `/v1/hotlists/{hotlist}/remove-record` | [Remove records from Hotlist](remove-records-from-hotlist.md) |
| GET | `/v1/hotlists/search` | [Search for hotlists](search-for-hotlists.md) |

## Custom Fields

| Method | Path | Doc |
|---|---|---|
| GET | `/v1/custom-fields` | [Show all Custom Fields](show-all-custom-fields.md) |
| GET | `/v1/custom-fields/candidates` | [Show all Candidate Custom Fields](show-all-candidate-custom-fields.md) |
| GET | `/v1/custom-fields/contacts` | [Show all Contact Custom Fields](show-all-contact-custom-fields.md) |
| GET | `/v1/custom-fields/companies` | [Show all Company Custom Fields](show-all-company-custom-fields.md) |
| GET | `/v1/custom-fields/jobs` | [Show all Job Custom Fields](show-all-job-custom-fields.md) |
| GET | `/v1/custom-fields/deals` | [Show all Deal Custom Fields](show-all-deal-custom-fields.md) |
| GET | `/v1/custom-fields/job-associated` | [Show all Job Associated Custom Fields](show-all-job-associated-custom-fields.md) |
| GET | `/v1/custom-fields/placements` | [Show all Placement Associated Custom Fields](show-all-placement-associated-custom-fields.md) |
| GET | `/v1/custom-fields/invoices` | [Show all Invoice Custom Fields](show-all-invoice-custom-fields.md) |

## Webhook Subscriptions

| Method | Path | Doc |
|---|---|---|
| GET | `/v1/subscriptions` | [Show all subscriptions](show-all-subscriptions.md) |
| POST | `/v1/subscriptions` | [Creates a new subscription](creates-a-new-subscription.md) |
| GET | `/v1/subscriptions/{subscription}` | [Find subscription by ID](find-subscription-by-id.md) |
| POST | `/v1/subscriptions/{subscription}` | [Edit a subscription](edit-a-subscription.md) |
| DELETE | `/v1/subscriptions/{subscription}` | [Delete a subscription](delete-a-subscription.md) |

## Sequences

| Method | Path | Doc |
|---|---|---|
| POST | `/v1/candidates/{candidate}/enroll` | [Enroll Candidate](enroll-candidate.md) |
| POST | `/v1/candidates/{candidate}/un-enroll` | [Unenroll Candidate](unenroll-candidate.md) |
| POST | `/v1/contacts/{contact}/enroll` | [Enroll Contact](enroll-contact.md) |
| POST | `/v1/contacts/{contact}/un-enroll` | [Unenroll Contact](unenroll-contact.md) |
| GET | `/v1/enrollment-statuses` | [Get All Enrollment Statuses](get-all-enrollment-statuses.md) |
| GET | `/v1/enrollments/search` | [Search for Enrollments](search-for-enrollments.md) |
| GET | `/v1/email-sequences/search` | [Search for Sequences](search-for-sequences.md) |

## Timesheets

| Method | Path | Doc |
|---|---|---|
| GET | `/v1/timesheets` | [Get All Timesheets](get-all-timesheets.md) |
| GET | `/v1/timesheets/{timesheet}` | [Get Timesheet Details](get-timesheet-details.md) |

## Placements

| Method | Path | Doc |
|---|---|---|
| GET | `/v1/placements` | [Show all Placements](show-all-placements.md) |
| GET | `/v1/placements/{placement}` | [Find placement by ID](find-placement-by-id.md) |
| POST | `/v1/placements/{placement}` | [Edit a placement](edit-a-placement.md) |
| DELETE | `/v1/placements/{placement}` | [Delete a placement](delete-a-placement.md) |
| GET | `/v1/placements/search` | [Search Placements](search-placements.md) |

## Invoices

| Method | Path | Doc |
|---|---|---|
| GET | `/v1/invoices` | [Show all invoices](show-all-invoices.md) |
| POST | `/v1/invoices` | [Creates a new invoice](creates-a-new-invoice.md) |
| GET | `/v1/invoices/{id}` | [Find invoice by ID](find-invoice-by-id.md) |
| POST | `/v1/invoices/{id}` | [Edit an invoice](edit-an-invoice.md) |
| DELETE | `/v1/invoices/{id}` | [Delete an invoice](delete-an-invoice.md) |
| GET | `/v1/invoices/search` | [Search for invoices](search-for-invoices.md) |

## Nested Custom Fields

| Method | Path | Doc |
|---|---|---|
| GET | `/v1/nested-custom-fields` | [Show Field Dependencies for all Entities](show-field-dependencies-for-all-entities.md) |

## Lists

| Method | Path | Doc |
|---|---|---|
| GET | `/v1/qualifications` | [Get Qualifications](get-qualifications.md) |
| GET | `/v1/currencies` | [Get Currencies](get-currencies.md) |
| GET | `/v1/salary-types` | [Get Salary Types](get-salary-types.md) |
| GET | `/v1/industries` | [Get Industries](get-industries.md) |
| GET | `/v1/languages` | [Get Languages](get-languages.md) |
| GET | `/v1/proficiencies` | [Get Proficiencies](get-proficiencies.md) |
| GET | `/v1/custom-call-types` | [Get Call Types](get-call-types.md) |
| GET | `/v1/note-types` | [Get Note Types](get-note-types.md) |
| GET | `/v1/meeting-types` | [Get Meeting Types](get-meeting-types.md) |
| GET | `/v1/task-types` | [Get Task Types](get-task-types.md) |
| GET | `/v1/sales-pipeline` | [Get Contact Stages](get-contact-stages.md) |
| GET | `/v1/deals-pipeline` | [Get Deals Stages](get-deals-stages.md) |
| GET | `/v1/jobs-pipeline` | [Get Job Stages](get-job-stages.md) |
| GET | `/v1/hiring-pipeline` | [Get Candidate Stages](get-candidate-stages.md) |
| GET | `/v1/hiring-pipelines` | [Get Multiple Hiring Pipelines](get-multiple-hiring-pipelines.md) |
| GET | `/v1/hiring-pipelines/{id}` | [Get Hiring Pipeline Stages For A Pipeline](get-hiring-pipeline-stages-for-a-pipeline.md) |
| GET | `/v1/candidate-questions` | [Get Candidate Questions](get-candidate-questions.md) |
| GET | `/v1/collaborators` | [Get Collaborators](get-collaborators.md) |
| GET | `/v1/users` | [Get All Users](get-all-users.md) |
| GET | `/v1/teams` | [Get All Teams](get-all-teams.md) |
| GET | `/v1/target-report/get` | [Get Target Report](get-target-report.md) |
| GET | `/v1/pitch-pipeline` | [Get Pitch stages](get-pitch-stages.md) |
| GET | `/v1/invoice-status` | [Get Invoice Status](get-invoice-status.md) |
| GET | `/v1/invoice-templates` | [Get Invoice Templates](get-invoice-templates.md) |

## List Off Limit Status

| Method | Path | Doc |
|---|---|---|
| GET | `/v1/off-limit-status` | [Get Off Limit Status](get-off-limit-status.md) |

## Users

| Method | Path | Doc |
|---|---|---|
| GET | `/v1/users/search` | [Search for Users](search-for-users.md) |

## Files

| Method | Path | Doc |
|---|---|---|
| POST | `/v1/files` | [Upload new files](upload-new-files.md) |
| GET | `/v1/files/{entity}/{slug}` | [Get All Files](get-all-files.md) |

## Email

| Method | Path | Doc |
|---|---|---|
| GET | `/v1/email/opted-out` | [Opted out entities](opted-out-entities.md) |
| POST | `/v1/email/opt-out/status` | [Update Opted out status](update-opted-out-status.md) |
| POST | `/v1/drafts` | [Create Email Draft](create-email-draft.md) |
| GET | `/v1/drafts/status/{draft\_status\_id}` | [Draft Email Status](draft-email-status.md) |
| POST | `/v1/emails` | [Send an Email](send-an-email.md) |
| GET | `/v1/emails/status/{email\_status\_id}` | [Sent Email Status](sent-email-status.md) |
