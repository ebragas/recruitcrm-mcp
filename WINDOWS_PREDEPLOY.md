# Windows pre-deploy checklist

Run these on a clean Windows VM before handing off to the client. Every check must pass green. If any step fails, STOP and diagnose — do not ship.

## Prereqs

- Clean Windows 10/11 VM (not a dev machine with prior installs)
- [Claude Desktop](https://claude.ai/download) installed
- A valid `RECRUIT_CRM_API_KEY` for the target tenant
- Python not required (uvx pulls its own)

## 1. Package install via `install.ps1`

```powershell
# From PowerShell, in the directory containing install.ps1:
.\install.ps1
```

Verify:
- [ ] Script completes without errors
- [ ] Claude Desktop config file updated — check `%APPDATA%\Claude\claude_desktop_config.json` (or the Windows Store variant path `%LocalAppData%\Packages\Anthropic.ClaudeElectron_*\LocalCache\Roaming\Claude\claude_desktop_config.json`) for an entry naming `recruit-crm-mcp`
- [ ] `RECRUIT_CRM_API_KEY` environment variable set (either user or system scope — confirm with `echo $env:RECRUIT_CRM_API_KEY`)

## 2. Binary sanity

```powershell
uvx --from recruit-crm-mcp recruit-crm-mcp --help 2>&1
```

This will print stdio-server help or start serving — if it just hangs waiting for input, that's expected (MCP binaries speak stdio). Kill with Ctrl+C. Check for any error output on stderr.

- [ ] No ImportError / packaging errors on stderr
- [ ] Binary launches without "command not found"

## 3. MCP handshake from Claude Desktop

Open Claude Desktop. Start a new conversation.

- [ ] In the chat UI, you should see `recruit-crm-mcp` listed among connected MCP servers (look for the tools icon or menu)
- [ ] `list_tools` visible from Claude — expect 50+ tools (baseline: 51 as of 2026-04-24)

## 4. Tool invocation end-to-end

Ask Claude:

> Call the `ping` tool on recruit-crm-mcp.

- [ ] Response shows `{"status": "ok", "version": "0.X.Y", "api_configured": true}`
- [ ] `api_configured == true` confirms the env var is visible to the server

Ask:

> Using the recruit-crm-mcp, search for the 3 most recently created candidates.

- [ ] Returns 3 candidate summaries (name + slug)
- [ ] No tool errors

Ask:

> Create a note on that first candidate that says "MCP install smoke test".

- [ ] `create_note` succeeds, returns a `WriteResult` with a non-empty id
- [ ] Verify in Recruit CRM UI that the note appears on that candidate
- [ ] **Clean up:** ask Claude to delete the note (`delete_note` tool) OR delete manually in the UI

## 5. Stdio framing on Windows specifically

Windows `\r\n` line endings have tripped stdio MCP servers in the past. The `ping` round-trip above proves basic framing works, but also test a tool with a longer structured response:

> Call `list_note_types` on recruit-crm-mcp.

- [ ] Returns a list of note types without truncation or JSON parse error
- [ ] No malformed-response warnings in Claude Desktop's logs (`%APPDATA%\Claude\logs\mcp-server-recruit-crm-mcp.log` or similar)

## 6. Smoke script against published wheel

From the repo directory on macOS (or any Unix/WSL2 host — bash required):

```bash
make smoke
# Or for the stricter published-wheel check:
uv run scripts/smoke.py --from-pypi
```

- [ ] `make smoke` passes (installs from local working tree, runs ping + list_note_types)
- [ ] `make smoke` with `--from-pypi` passes AFTER you've cut the release to PyPI (proves the wheel on PyPI — not just the source tree — works)
- [ ] Optional: `RCRM_SMOKE_WRITES=1 uv run scripts/smoke.py` — exercises a create/delete round-trip

## 7. Final sign-off

- [ ] All of the above green
- [ ] `make check && make mcp-test && make integration-test && make mcp-live-test` all green on `main` at the tagged release commit
- [ ] Release cut to PyPI (`chore(release)` commit landed, tag pushed, wheel visible on pypi.org)
- [ ] `install.ps1` points to the published version (not a pre-release)
- [ ] CLAUDE.md field-mapping gotchas section reviewed — especially the write-endpoint quirks (partial POST, `do_not_send_calendar_invites` bool coercion, attendee asymmetric shape)
- [ ] Client has been briefed on: task completion is a product gap (no API mechanism; they'll need UI or deletion), and `set_*_custom_fields` updates only the custom fields (not other entity fields)

## If something breaks

- **`install.ps1` exits non-zero:** capture stderr + exit code, consult the `install.ps1` error messages; the most likely cause is a Claude Desktop config path variance on this Windows install — the script handles Windows Store path vs standard path, but not every variant.
- **Tool calls return error even though `ping` works:** check `api_configured` first (env var scoping — user vs system vs process). PowerShell 5.1 vs 7 can differ.
- **JSON parse errors in Claude Desktop log:** stdio framing issue. Run the server manually with `uvx --from recruit-crm-mcp recruit-crm-mcp` in a PowerShell window and send a JSON-RPC `initialize` request by pasting; watch for `\r\n` handling.
- **A write tool hits 422:** most likely a payload-assembly regression. Check CLAUDE.md "Field Mapping Gotchas" for the specific endpoint — chances are docs and live API diverge on that field's shape.
