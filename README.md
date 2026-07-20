# opensynapse-sample-registry

Public, deployment-neutral Claude extensions for an OpenSynapse sample
deployment. This repository is a distribution catalog, not a governance or
policy authority.

It contains:

- A native Claude plugin marketplace at `.claude-plugin/marketplace.json`.
- The `opensynapse-sample` plugin and its health-check skill.
- A third-party Cowork managed-settings template at `catalog/cowork-3p.json`.

The catalog intentionally contains placeholders rather than deployed URLs or
credentials. A consuming implementation must pin an exact commit and supply:

| Placeholder | Required value |
| --- | --- |
| `EXTENSION_REGISTRY_REF` | Full 40-character commit SHA for this repository |
| `OPENSYNAPSE_MCP_URL` | Deployed HTTPS MCP endpoint |
| `OPENSYNAPSE_MCP_OAUTH_CLIENT_ID` | Public OAuth client ID |
| `OPENSYNAPSE_MCP_OAUTH_ISSUER` | OAuth authorization-server issuer |
| `OPENSYNAPSE_MCP_OAUTH_SCOPES` | Space-separated scopes |
| `OPENSYNAPSE_MCP_OAUTH_CALLBACK_PORT` | Registered Desktop loopback port |

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
Code tab uses the former settings.
