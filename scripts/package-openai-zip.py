#!/usr/bin/env python3
"""Build the OpenAI plugin-directory ZIP from apps/ofx-claude-plugin.

The portal reads a portable plugin.json and mcp.json. OpenAI settings live in
root plugin.json under extensions.com.openai, and OAuth lives in mcp.json
under extensions.com.openai.auth. When that object is present, OpenAI ignores
.codex-plugin/plugin.json. .mcp.json and .app.json stay out of the ZIP.

OpenAI has no API for directory uploads. CI publishes this ZIP as a release
asset. After the plugin is published, hosted MCP tool changes are scanned by
OpenAI and do not need a new ZIP. Metadata, skills, and assets do.
"""

from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
CODEX_MANIFEST = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
OUT_DIR = PLUGIN_ROOT / "dist"
OUT_ZIP = OUT_DIR / "familyofx-openai-plugin.zip"
SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
MCP_URL = "https://familyofx.com/api/mcp"
AUTH_BASE = "https://familyofx.com/api/auth"
# Public PKCE client. Must match OPENAI_OAUTH_CLIENT_ID in
# apps/ofx/src/modules/mcp/openai-oauth-client.ts. No client secret.
OPENAI_OAUTH_CLIENT_ID = "familyofx-openai"

INCLUDE_PREFIXES = ("skills/", "assets/")


def portable_manifest(codex: dict) -> dict:
    openai = dict(codex.get("extensions", {}).get("com.openai") or {})
    interface = codex.get("interface")
    if not isinstance(interface, dict):
        raise SystemExit("Codex manifest is missing interface")
    openai["interface"] = interface
    return {
        "$schema": SCHEMA,
        "name": codex["name"],
        "version": codex["version"],
        "description": codex["description"],
        "author": codex["author"],
        "homepage": codex["homepage"],
        "repository": codex["repository"],
        "keywords": codex.get("keywords") or [],
        "extensions": {"com.openai": openai},
    }


def mcp_manifest() -> dict:
    return {
        "$schema": MCP_SCHEMA,
        "mcpServers": {
            "familyofx": {
                "type": "streamable-http",
                "url": MCP_URL,
                "extensions": {
                    "com.openai": {
                        "auth": {
                            "type": "oauth",
                            "client": {
                                "mode": "provided",
                                "clientId": OPENAI_OAUTH_CLIENT_ID,
                                "tokenEndpointAuthMethod": "none",
                            },
                            "authorizationUrl": f"{AUTH_BASE}/oauth2/authorize",
                            "tokenUrl": f"{AUTH_BASE}/oauth2/token",
                            "resource": MCP_URL,
                        }
                    }
                },
            }
        },
    }


def package_files() -> dict[str, bytes]:
    codex = json.loads(CODEX_MANIFEST.read_text())
    files = {
        "plugin.json": json.dumps(portable_manifest(codex), indent=2).encode() + b"\n",
        "mcp.json": json.dumps(mcp_manifest(), indent=2).encode() + b"\n",
    }
    for path in PLUGIN_ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(PLUGIN_ROOT).as_posix()
        if rel.startswith(INCLUDE_PREFIXES) and not rel.endswith(".DS_Store"):
            files[rel] = path.read_bytes()
    required = [
        "plugin.json",
        "mcp.json",
        "skills/familyofx/SKILL.md",
        "assets/icon.png",
        "assets/logo.png",
    ]
    missing = [name for name in required if name not in files]
    if missing:
        raise SystemExit(f"OpenAI ZIP is missing: {', '.join(missing)}")
    return files


def main() -> None:
    files = package_files()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if OUT_ZIP.exists():
        OUT_ZIP.unlink()
    with zipfile.ZipFile(OUT_ZIP, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in sorted(files):
            info = zipfile.ZipInfo(name)
            info.compress_type = zipfile.ZIP_DEFLATED
            # Fixed timestamp keeps the archive stable across machines.
            info.date_time = (2026, 1, 1, 0, 0, 0)
            archive.writestr(info, files[name])
    with zipfile.ZipFile(OUT_ZIP) as archive:
        names = archive.namelist()
    if any(
        name.startswith((".codex-plugin/", ".claude-plugin/", ".mcp.json", ".app.json"))
        for name in names
    ):
        raise SystemExit("OpenAI ZIP included a non-portable manifest")
    print(OUT_ZIP)
    for name in names:
        print(f"  {name}")


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        sys.exit(0)
