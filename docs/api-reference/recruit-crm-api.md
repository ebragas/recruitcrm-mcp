<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/9033e3227d21f-recruit-crm-api -->
<!-- title: Recruit CRM API | API Endpoints -->

# Recruit CRM API

Export

v8.7.3

API Base URL

Prod:https://api.recruitcrm.io

Mock Server:https://stoplight.io/mocks/recruitcrm/rcrm-api-reference/978024

Security

Bearer Auth

Provide your bearer token in the Authorization header when making requests to protected resources.

Example: `Authorization: Bearer 123`

Additional Information

[Contact support@recruitcrm.io](mailto:support@recruitcrm.io)

[Apache 2.0](http://www.apache.org/licenses/LICENSE-2.0.html)

# Status Codes

Recruit CRM API uses conventional HTTP response codes to indicate the success or failure of an API request.

| Verb | Description |
| --- | --- |
| **GET** | Select one or more items. Success returns `200` status code |
| **POST** | Create a new item. Success returns `200` or `201` status code |

## HTTP status code summary

| **Status Code** | **Description** |
| --- | --- |
| **200 OK** | Everything worked as expected. |
| **201 Created** | Your request has been processed successfully and the record has been created |
| **202 Accepted** | Your request is currently being processed. You can check again later to see the request has been processed |
| **400 Bad Request** | Your request was malformed |
| **403 Forbidden** | Your API Token is invalid, missing, or has exceeded its quota |
| **404 Not Found** | This resource cannot be found. You will receive this status code if you attempt to query our deprecated endpoints |
| **405 Method Not Allowed** | You have queried the API with an unsupported HTTP method. Retry your query with either `GET` or `POST` |
| **422 Invalid** | Invalid or missing API query parameter |
| **429 Too Many Requests** | Too many requests issued to the API. Rate limiting kicks in and blocks further requests |
| **500 Internal Server Error** | There was an unexpected error on our server. If you see this please contact [support@recruitcrm.io](mailto:support@recruitcrm.io) |

## Error Types

| Type | Description |
| --- | --- |
| **api\_connection\_error** | Failure to connect to Recruit CRM API. |
| **api\_error** | API errors cover any other type of problem (e.g., a temporary problem with Recruit CRM’s servers), and are extremely uncommon. |
| **authentication\_error** | Failure to authenticate your identity in the request |
| **token\_not\_active\_error** | API token is not active, you must activate your token to use API. |
| **rate\_limit\_error** | Too many requests hit the API too quickly. |
| **invalid\_request\_error** | Invalid request errors arise when your request has invalid parameters. |
| **validation\_error** | Errors triggered by our client-side libraries when failing to validate fields |
| **Dates and Time** | All dates and time will be returned in the `ISO-8601 Date/Time Format` like `2020-06-29T05:36:22.000000Z`. Adjust accordingly in your application for the user's local timezone. |

The Recruit CRM API accepts `JSON` payloads making it very easy to work with, all posted fields must follow the correct format otherwise this will result in the API returning an error message. Please see the different options available to you below.

**Note:** Whenever making API requests with GET method, please make sure that the query parameter values are URL encoded
