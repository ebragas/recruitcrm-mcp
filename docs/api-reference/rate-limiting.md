<!-- source: https://docs.recruitcrm.io/docs/rcrm-api-reference/d158c10843b7c-rate-limiting -->
<!-- title: Rate Limiting | API Endpoints -->

# Rate Limiting

We enforce a small amount of rate-limiting, dynamically scaled based on the number of licenses in your account. For accounts with 6 licenses or fewer, the limit is a standard **60 requests per minute**. For accounts with more than 6 licenses, the limit is **10 requests per minute per license**. For example, an account with 7 licenses can make up to 70 requests per minute.
These limits are applied per API Token.

You can use the X-RateLimit HTTP header returned with every response to track your current usage. If you exceed your limit, a **429 HTTP status** will be issued. Once your cool-down period expires, you can resume making requests.

You can see the current state of the throttle for a store by using the rate limits header.

Rate limits will be returned with every request in following headers:

#### X-RateLimit-Limit

> This header will contain the number of calls per minute that can be made to the API before rate limiting will take effect.

#### X-RateLimit-Remaining

> This header will contain the number of calls the API has left in the current rate limit window.
