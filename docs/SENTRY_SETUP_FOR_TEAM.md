# Enabling Error Reporting in Recruit CRM MCP

We're turning on error reporting so the team can see and fix problems in the Recruit CRM tools faster. This takes about 2 minutes — no terminal commands needed, just editing one settings file in Claude Desktop.

When something goes wrong while you're using a Recruit CRM tool, Claude Desktop will quietly send the error details to our team's [Sentry](https://sentry.io/) dashboard so we can debug. You won't see anything different on your end — Claude works the same as always.

---

## 1. Open the Claude Desktop config file

### On Mac

1. Open **Finder**.
2. Press `Cmd + Shift + G`.
3. Paste this path and press **Return**:
   ```
   ~/Library/Application Support/Claude/claude_desktop_config.json
   ```
4. Open the file in **TextEdit** (right-click → Open With → TextEdit) or your favorite editor.

### On Windows

1. Press `Win + R`.
2. Paste this and press **Enter**:
   ```
   %APPDATA%\Claude\claude_desktop_config.json
   ```
3. The file will open in your default text editor (usually Notepad).

---

## 2. Find the `recruit-crm` section

The file holds a few different MCP server entries. Look for the one that starts with `"recruit-crm":`. It will look something like this:

```json
"recruit-crm": {
  "command": "uvx",
  "args": ["recruit-crm-mcp"],
  "env": {
    "RECRUIT_CRM_API_KEY": "your-existing-api-key-here"
  }
}
```

The actual values may differ — your API key is the long string starting with letters and numbers.

---

## 3. Replace the whole `recruit-crm` block with this

```json
"recruit-crm": {
  "command": "uvx",
  "args": ["--refresh-package", "recruit-crm-mcp", "recruit-crm-mcp"],
  "env": {
    "RECRUIT_CRM_API_KEY": "PASTE-YOUR-EXISTING-API-KEY-HERE",
    "RECRUIT_CRM_MCP_SENTRY_DSN": "https://f59dfb6fadff83e1dcabfb281193337e@o4511298533130240.ingest.us.sentry.io/4511298563604480"
  }
}
```

Two things to be careful with:

- **Keep your existing `RECRUIT_CRM_API_KEY`** — copy the long string from the old block into the new one. Don't lose it.
- **Don't change the Sentry DSN** — copy the URL above exactly. It points to our team's error tracking project.

If your file has more than one MCP server entry (e.g. `recruit-crm-rc`, `pencil`, etc.), only edit the `recruit-crm` block. Leave the others alone.

---

## 4. Save the file and fully quit Claude Desktop

Saving the file isn't enough — Claude Desktop only reads the config when it starts up.

- **Mac:** `Cmd + Q` to quit. Closing the window isn't enough; the app keeps running in the dock.
- **Windows:** Right-click the Claude icon in the system tray → **Quit**.

---

## 5. Reopen Claude Desktop

The first launch after this change will take an extra 5–10 seconds while Claude Desktop downloads the latest Recruit CRM MCP version. After that, you're done.

---

## 6. (Optional) Confirm it's working

Ask Claude:

> *"Use the Recruit CRM tool to look up a candidate that doesn't exist, like 'this-is-a-test-12345'."*

The lookup will fail with a "candidate doesn't exist" error — that's expected. Eric can then confirm the error showed up in our Sentry dashboard, which means reporting is wired correctly. You won't see anything special on your end.

---

## What this changes

- **Auto-updates.** The `--refresh-package` flag in `args` tells Claude Desktop to check for new versions of the Recruit CRM tools every time you launch the app. When we ship a bug fix, you'll automatically get it on your next restart — no manual install needed.
- **Error reporting.** When a Recruit CRM tool errors out, the technical details (which tool, what arguments, the actual error message and stack trace) are sent to our team's Sentry dashboard. We see what broke and can ship a fix faster.
- **Your normal CRM data is NOT collected globally** — only what's relevant to a specific error gets attached to that error report, and it only goes to our team's dashboard, not anywhere public.

---

## Trouble?

**"MCP recruit-crm: Server disconnected" message after restart.**
Usually means a typo in the JSON file — a missing comma, an extra quote, or a broken bracket. Common slip-ups:

- The block must start with `"recruit-crm":` followed by `{`.
- Every `"key": "value"` line inside the `env` block needs a comma after it, except the last one.
- All quotes must be straight `"` (not curly `"`/`"` from word processors).

Reopen the file, double-check the punctuation against the snippet in step 3, save, and quit/reopen Claude Desktop again. If it still won't connect, message Eric with a copy of the file (you can scrub the API key first).

**Lost your API key.**
Eric can re-issue it. Don't try to guess it from memory.

---

## Questions

Send to Eric. This setup is one-time per machine — once it's done you don't have to do anything else, and future Recruit CRM updates will install themselves.
