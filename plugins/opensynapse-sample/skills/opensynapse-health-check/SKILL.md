---
name: opensynapse-health-check
description: Verify that the OpenSynapse-managed Claude bootstrap and plugin installation are active. Use when checking a provisioned Claude Desktop or Cowork deployment.
---

# OpenSynapse Health Check

Run a non-destructive bootstrap check from the managed Claude session.

1. Respond with the exact text `opensynapse-ok` to prove this managed skill was installed and can execute through the configured inference path.
2. If the user also asks about external tools, list the third-party connectors currently available to the session. It is valid for a deployment to configure none.
3. Report unavailable or unauthorized third-party connectors by their configured names only. Let Claude perform the connector's normal authorization flow when the user chooses to use it.

Do not invent OpenSynapse MCP tools, call connector endpoints directly, or expose credentials, authorization headers, tokens, or raw trace content.
