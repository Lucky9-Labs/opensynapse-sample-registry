---
name: opensynapse-health-check
description: Verify a managed OpenSynapse MCP connection by running a harmless inference prompt and confirming its trace evidence. Use when checking that a provisioned OpenSynapse Claude Desktop or Cowork deployment is connected end to end.
---

# OpenSynapse Health Check

Run a non-destructive end-to-end check through the managed OpenSynapse MCP.

1. Call `opensynapse_run` with a harmless prompt that asks for the exact text `opensynapse-ok` and no more than 32 output tokens.
2. Preserve the returned `call_id` exactly.
3. Call `opensynapse_trace_status` with that `call_id`.
4. Report whether inference completed and whether trace evidence is present. Include the call ID, but do not reproduce credentials, authorization headers, or raw trace content.

If either tool is unavailable, stop and state that the managed MCP connection is not ready. Do not substitute shell commands or direct HTTP calls.

Do not call `opensynapse_policy_probe` or `opensynapse_recent_denials`; those operations are outside this sample health check.
