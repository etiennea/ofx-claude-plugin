# FamilyOFX Claude plugin

Thin Claude Code / Claude Desktop plugin that bundles the **FamilyOFX remote MCP server** and a **catch-all skill** so Claude uses connector tools for portfolio, CRM, documents, tasks, calendar, and imports.

Sources live in the FamilyOFX monorepo at `apps/ofx-claude-plugin/`. Pushes to `main` that touch this folder are published to the public repo [etiennea/ofx-claude-plugin](https://github.com/etiennea/ofx-claude-plugin).

## Setup

### Claude Code

1. Install or load this plugin (marketplace entry or local path):

   ```bash
   claude plugin install /path/to/apps/ofx-claude-plugin
   ```

   Or add the plugin directory via **Settings → Plugins** when using a marketplace manifest.

2. Enable the plugin. Claude Code starts the MCP server defined in `.mcp.json`.

3. Complete **OAuth** when prompted: sign in to FamilyOFX, pick the **organisation**, and **Allow** access.

4. Ask questions about your office data; invoke the skill with `/familyofx:familyofx` if needed.

Validate the manifest locally (requires Claude Code v2.1.281+):

```bash
claude plugin validate ./apps/ofx-claude-plugin
```

### Claude Desktop / Connectors Directory

Use the universal MCP URL `https://familyofx.com/api/mcp` with OAuth. Product steps: [MCP connections](https://familyofx.com/docs/settings/mcp-connections).

## Privacy Policy

FamilyOFX is operated by **EA SOFT LTD**. This plugin connects Claude to your FamilyOFX account over OAuth; tool calls read or queue actions against **one organisation** you select at consent.

- **Privacy Policy:** https://familyofx.com/privacy  
- **Support:** https://familyofx.com/support  
- **Data handling:** Read tools return live org data you are authorised to see. Write tools create **pending approvals** in FamilyOFX; nothing mutates until you accept in the app. Revoke access under **Settings → Integrations → AI connectors**.

## Store submission (ops)

Pushes to `main` that touch this folder mirror it to [etiennea/ofx-claude-plugin](https://github.com/etiennea/ofx-claude-plugin).

### OpenAI plugin directory

Build the submission ZIP:

```bash
python3 apps/ofx-claude-plugin/scripts/package-openai-zip.py
```

That writes `apps/ofx-claude-plugin/dist/familyofx-openai-plugin.zip`. The archive root is a portable plugin: `plugin.json`, `mcp.json` (OAuth via CIMD, server `https://familyofx.com/api/mcp`), `skills/`, and `assets/`. Listing text, test cases, and the demo recording come from `.codex-plugin/plugin.json`. Reviewer credentials stay out of the ZIP; enter them in the portal from `docs/store-reviewer-account.md`.

The same script runs in `.github/workflows/publish-claude-plugin.yml`. The workflow uploads the ZIP as an Actions artifact and replaces the asset on the public repo release `openai-submission`:

https://github.com/etiennea/ofx-claude-plugin/releases/tag/openai-submission

OpenAI does not offer an API to push that ZIP into the plugin portal. Upload it there for the first submission, and again when metadata, skills, or icons change. Bump `version` in `.codex-plugin/plugin.json` before an update upload. After the plugin is published, changes to the hosted MCP tools are scanned by OpenAI and do not need a new ZIP.
