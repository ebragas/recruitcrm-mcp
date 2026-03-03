---
name: review-pr-comments
description: Review, fix, and respond to PR code review comments.
---

# Review PR Comments

Process all code review comments on a pull request. For each comment, determine if it should be fixed or skipped, apply fixes, commit, push, and reply.

## Steps

1. **Fetch comments** — get all review comments on the current branch's PR:
   ```bash
   gh api repos/{owner}/{repo}/pulls/{pr_number}/comments
   ```

2. **Triage each comment** — for every comment, decide:
   - **Fix** — valid issue that should be addressed
   - **Skip** — not applicable, out of scope, or wrong (document why)

3. **Apply fixes** — make all code changes, then run `make check` to verify nothing is broken

4. **Commit and push** — single commit with all fixes:
   ```
   Address PR review: <brief summary of changes>
   ```

5. **Reply to each comment** — respond on GitHub with fix/skip reasoning:
   ```bash
   # For fixes:
   gh api repos/{owner}/{repo}/pulls/{pr_number}/comments \
     -f body="Fixed — <what was done>" \
     -F in_reply_to={comment_id}

   # For skips:
   gh api repos/{owner}/{repo}/pulls/{pr_number}/comments \
     -f body="Skipping — <reason>" \
     -F in_reply_to={comment_id}
   ```

6. **Re-request review** — after pushing and replying, re-request review from the original reviewers:
   ```bash
   # Get the list of reviewers who left comments
   # Then remove and re-add them to trigger a fresh review
   gh api repos/{owner}/{repo}/pulls/{pr_number}/requested_reviewers \
     -X DELETE -f "reviewers[]={reviewer_login}"
   gh api repos/{owner}/{repo}/pulls/{pr_number}/requested_reviewers \
     -X POST -f "reviewers[]={reviewer_login}"
   ```

## Rules

- Always run tests after applying fixes before committing
- One commit for all fixes, not one per comment
- Keep replies concise — one sentence explaining the fix or skip reason
- Never skip a comment without a clear reason
