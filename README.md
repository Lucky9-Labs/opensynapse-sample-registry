# opensynapse-sample-registry

Public, deployment-neutral Claude extensions for an OpenSynapse sample
deployment. This repository is a distribution catalog, not a governance or
policy authority.

It contains:

- A native Claude plugin marketplace at `.claude-plugin/marketplace.json`.
- The `opensynapse-sample` plugin and its health-check skill.
- A third-party Cowork managed-settings template at `catalog/cowork-3p.json`.

The catalog intentionally contains no deployed MCP server. A consuming
implementation pins an exact commit, resolves the marketplace revision, and may
inject zero or more deployment-approved third-party MCP server definitions into
`managedMcpServers`:

- `EXTENSION_REGISTRY_REF` is the only catalog placeholder and must be this
  repository's full 40-character commit SHA.
- Each third-party MCP entry identifies an HTTPS HTTP or SSE endpoint, defaults
  all tools to `ask`, and may include a public client ID, callback port, pinned
  scopes, or authorization-server metadata URL. Standard OAuth discovery is
  used when those overrides are absent.
- Claude performs each third party's normal authorization flow. Tokens, client
  secrets, authorization headers, and other credentials must never be compiled
  into managed settings.

OpenSynapse itself is not an MCP server. The OpenSynapse sample implementation
provides the managed Claude bootstrap, inference-gateway configuration, plugin
marketplace, and optional third-party connector list.

No API keys, OAuth tokens, client secrets, AWS account identifiers, Cedar
files, or production deployment coordinates belong here. Run both validators
before publishing a change:

```sh
python3 scripts/validate_registry.py
claude plugin validate .
```

Consumers should add the marketplace through managed settings and use the same
immutable revision in both `extraKnownMarketplaces` and
`strictKnownMarketplaces`. Cowork uses the same revision through
`allowedPluginMarketplaces` with anonymous, required installation; the Claude
Code tab uses the former settings. The registry does not choose which external
MCP services a deployment trusts.
