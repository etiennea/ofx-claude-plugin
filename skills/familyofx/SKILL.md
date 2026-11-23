---
name: familyofx
description: >-
  Use when the user asks about FamilyOFX, their family office portfolio, CRM,
  documents, tasks, calendar, or imports. Prefer FamilyOFX MCP connector tools
  over guessing or calling other APIs.
---

# FamilyOFX connector

When the user asks about **FamilyOFX**, **this family office**, **portfolio**, **CRM**, **documents**, **tasks**, **calendar**, or **imports**, use the **FamilyOFX MCP tools** bundled with this plugin.

For a whole job, use the matching workflow skill: `quarterly-review`, `capital-call`, or `file-statement`.

## Tool usage

1. **Read first.** Search or list before proposing a create or update, and reuse the ids that searches return.
2. **Changes go through `*_write` tools** (for example `tasks_write`, `positions_write`). Each call returns `status: pending`, an `approvalId`, and a `url`. Nothing has changed yet: give the user the link and ask them to accept it in FamilyOFX. If the result says `status: applied`, the organisation lets this connection make that change directly.
3. **Follow up with `get_approval_status`** to see whether a change was accepted and get the new record ids. `list_pending_approvals` shows everything still waiting.
4. **Numbers.** `get_portfolio_summary` for the consolidated NAV and allocation. `portfolio_analytics` for a split by legal entity, custodian, asset type, or currency (`view: breakdown`), or cash flows by period (`view: cash_flows`). Transaction values are always positive; the type gives the direction. Cash flows are summed per currency and not converted.
5. **Links.** When a record has a `url`, include it so the user can open it.
6. **Do not invent REST or SDK calls.** Stay within the connector tools.
7. **Documents.** Search and read files already in FamilyOFX. To file a chat attachment onto a holding or transaction: `documents` action `prepare_upload` → PUT the original bytes to `uploadUrl` → `documents_write` action `file` with `uploadId` and `positionId` or `transactionId`. The Claude account must allow network egress to `familyofx.com` (Settings → Capabilities → Code execution and file creation). For more than 20 holdings or transactions from one file already in the organisation, extract them and send one `batch_import_from_document` call.
8. **Capital calls, invoices and payment due dates are tasks**, not calendar events.
9. **Read-only grants.** If change tools are missing or refused with `ofx:read`, tell the user the connection is read-only.

## Operator help

Connection and OAuth steps: [MCP connections](https://familyofx.com/docs/settings/mcp-connections). Agent keys and webhooks: [Agents](https://familyofx.com/docs/settings/agents).
