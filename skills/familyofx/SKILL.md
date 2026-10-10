---
name: familyofx
description: >-
  Use when the user asks about FamilyOFX, their family office portfolio, CRM,
  documents, tasks, calendar, or imports. Prefer FamilyOFX MCP connector tools
  over guessing or calling other APIs.
---

# FamilyOFX connector

When the user asks about **FamilyOFX**, **this family office**, **portfolio**, **CRM**, **documents**, **tasks**, **calendar**, or **imports**, use the **FamilyOFX MCP tools** bundled with this plugin.

## Tool usage

1. **Prefer read tools first** — search, list, and lookup before proposing creates or updates.
2. **Destructive / write tools only queue approvals** — they do not mutate data immediately. Tell the user to **accept the pending action in FamilyOFX → AI Agents** (or review under **Settings → Integrations → AI connectors**).
3. **Do not invent REST or SDK calls** — stay within the connector tool surface exposed by MCP.
4. **Batch import** — the source document must **already exist in the organisation** (upload in FamilyOFX first via Documents, shared inbox, or chat). MCP does not upload files from Claude in v1.

## Operator help

Connection and OAuth steps: [MCP connections](https://familyofx.com/docs/settings/mcp-connections).
