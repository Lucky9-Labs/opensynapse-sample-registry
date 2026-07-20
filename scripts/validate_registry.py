#!/usr/bin/env python3
"""Validate the public OpenSynapse extension registry without network access."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_PLACEHOLDERS = {
    "EXTENSION_REGISTRY_REF",
    "OPENSYNAPSE_MCP_OAUTH_CALLBACK_PORT",
    "OPENSYNAPSE_MCP_OAUTH_CLIENT_ID",
    "OPENSYNAPSE_MCP_OAUTH_ISSUER",
    "OPENSYNAPSE_MCP_OAUTH_SCOPES",
    "OPENSYNAPSE_MCP_URL",
}
PLACEHOLDER = re.compile(r"\$\{([A-Z0-9_]+)\}")
SECRET_PATTERNS = {
    "AWS access key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "AWS account ID": re.compile(r"(?<!\d)\d{12}(?!\d)"),
    "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "assigned credential": re.compile(
        r"(?i)\b(?:api[_-]?key|client[_-]?secret|password|token)\b\s*[:=]\s*[\"']?[A-Za-z0-9_./+=-]{16,}"
    ),
}


def fail(message: str) -> None:
    raise ValueError(message)


def load_json(relative: str) -> dict:
    path = ROOT / relative
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{relative}: invalid JSON: {exc}")
    if not isinstance(value, dict):
        fail(f"{relative}: root must be an object")
    return value


def validate_paths() -> None:
    for path in ROOT.rglob("*"):
        if ".git" in path.parts:
            continue
        relative = path.relative_to(ROOT)
        if path.is_dir() and "policies" in {part.lower() for part in relative.parts}:
            fail(f"policy directory is forbidden: {relative}")
        if path.is_file() and path.suffix.lower() == ".cedar":
            fail(f"Cedar file is forbidden: {relative}")


def validate_marketplace() -> None:
    marketplace = load_json(".claude-plugin/marketplace.json")
    if marketplace.get("name") != "opensynapse-sample-registry":
        fail("marketplace name must be opensynapse-sample-registry")
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        fail("marketplace must contain at least one plugin")
    names: set[str] = set()
    for index, plugin in enumerate(plugins):
        name = plugin.get("name")
        if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            fail(f"plugins[{index}].name must be kebab-case")
        if name in names:
            fail(f"duplicate plugin name: {name}")
        names.add(name)
        source = plugin.get("source")
        if not isinstance(source, str) or not source.startswith("./") or ".." in Path(source).parts:
            fail(f"plugins[{index}].source must be a repository-relative path")
        plugin_root = (ROOT / source).resolve()
        if not plugin_root.is_relative_to(ROOT) or not plugin_root.is_dir():
            fail(f"plugins[{index}].source does not exist")
        manifest = load_json(str(Path(source) / ".claude-plugin/plugin.json"))
        if manifest.get("name") != name:
            fail(f"plugins[{index}] name does not match plugin.json")


def validate_catalog() -> None:
    catalog = load_json("catalog/cowork-3p.json")
    if set(catalog) != {"schemaVersion", "managedSettings"} or catalog["schemaVersion"] != 1:
        fail("catalog must contain schemaVersion=1 and managedSettings only")
    settings = catalog["managedSettings"]
    required = {
        "managedMcpServers",
        "extraKnownMarketplaces",
        "strictKnownMarketplaces",
        "enabledPlugins",
    }
    if not isinstance(settings, dict) or set(settings) != required:
        fail("catalog managedSettings keys do not match the v1 contract")
    servers = settings["managedMcpServers"]
    if not isinstance(servers, list) or len(servers) != 1:
        fail("catalog must declare exactly one managed MCP server")
    server = servers[0]
    if server.get("transport") != "http" or server.get("toolPolicy") != {"*": "ask"}:
        fail("managed MCP must use HTTP and default every tool to ask")
    if server.get("url") != "${OPENSYNAPSE_MCP_URL}":
        fail("managed MCP URL must remain deployment-neutral")
    discovered = set(PLACEHOLDER.findall(json.dumps(catalog, sort_keys=True)))
    if discovered != ALLOWED_PLACEHOLDERS:
        fail(f"catalog placeholders differ from contract: {sorted(discovered)}")


def scan_secrets() -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        try:
            content = path.read_text()
        except UnicodeDecodeError:
            continue
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(content):
                fail(f"possible {label} in {path.relative_to(ROOT)}")


def main() -> int:
    try:
        validate_paths()
        validate_marketplace()
        validate_catalog()
        scan_secrets()
    except ValueError as exc:
        print(f"registry validation failed: {exc}", file=sys.stderr)
        return 1
    print("registry validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
