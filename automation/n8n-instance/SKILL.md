---
name: n8n-instance
description: Safely connect a coding agent to a user-authorized n8n instance-level MCP server and use the official n8n workflow skills on demand.
---
# n8n instance MCP — connection and permissions adapter

Original bundle-authored connection guide. The **14** source-preserved official skills are in `automation/n8n-*-official/` and `automation/using-n8n-skills-official/`. Canonical publisher: [n8n-io/skills](https://github.com/n8n-io/skills) at `180b8415e3b73f78828cfa01e908e67f89f2a139` (Apache-2.0). An MCP connection is an authenticated external capability; installing skill text alone gives no instance access.

1. Confirm whether an n8n Cloud or self-hosted instance exists. The official n8n skills documentation states instance-level MCP requires n8n **2.2.0 or later**. For unverified versions, consult current official docs instead of guessing.
2. Keep the actual n8n base URL, account authorization, tokens and project workflow identifiers in the **user's private host configuration**, not this public repository or Skill Retrieval's public index. Prefer the official instance-level MCP endpoint `https://<instance-host>/mcp-server/http`, with OAuth through the host's MCP manager when supported.
3. In Antigravity, Codex or Claude, merge the MCP entry without overwriting existing servers. Review the host's current MCP documentation and secure transport/TLS. Register **one** n8n MCP connection to the same instance, not both a duplicated Claude plugin server and manual entry.
4. The separate [czlonkowski/n8n-mcp](https://github.com/czlonkowski/n8n-mcp) (`4cc0efda76f272e3b0816f215399f21599c29d34`, MIT) is a different third-party server and has its own broader node-documentation/database runtime. Do not install it by assuming it is the official instance-level endpoint.
5. First verify read-only discovery and permissions. For writes, show the proposed workflow changes, dependencies, trigger behavior and rollback; require approval to create/modify workflows, enable triggers, rotate credentials, send messages or delete objects. Use official `n8n-credentials-and-security-official`, `n8n-workflow-lifecycle-official` and appropriate narrow skills.
6. Never print credentials, put secrets in workflow JSON, expose an instance endpoint unauthenticated, or enable an internet-facing webhook/cron without authorization. Test workflow outputs using safe data and document which changes actually executed.
7. If no authorized MCP exists, analyze draft workflow JSON as text only; never claim to have listed or changed live n8n workflows.
