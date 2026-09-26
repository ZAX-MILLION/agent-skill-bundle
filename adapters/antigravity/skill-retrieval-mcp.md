# Optional Skill Retrieval MCP on Antigravity

**Upstream:** https://github.com/JayCheng113/skill-retrieval-mcp — Zhan Cheng, MIT. Reviewed source revision: `7d034a2af4ac26ff7a69522ee4a3e22b865d586e` (package metadata version `0.3.1`). This is a local integration guide, **not** the upstream source or an automatic installer.

## What it does

The external MCP server offers `search_skills` (semantic), `keyword_search` (exact), `get_skill` (full text) and `list_categories`. Search results are summaries; read the description and fetch full instructions only for a relevant match. A similarity score is **not** a confidence measure. Do not claim retrieval creates an executable tool or grants permission.

The directory importer reads `SKILL.md` files. It does **not** install or mirror the accompanying scripts, references, assets or full upstream license/provenance metadata into its database. The original bundle checkout remains authoritative; open a referenced support file from its installed skill directory rather than relying on the MCP response alone. Its import count may be below the bundle count for files lacking parseable frontmatter or for deduplicated content.

## Setup boundary

Install only on the computer running Antigravity, in an isolated `pipx`/virtual environment, after reviewing the pinned upstream package and dependencies. The official project offers `skill-retrieval-mcp[local]` for local embeddings. Local inference needs initial installation/model download and creates local files, but does not require an external embedding API during subsequent searches.

Example **only after approving local software installation**:

```bash
pipx install 'skill-retrieval-mcp[local]==0.3.1'
skill-mcp --data-dir "$HOME/.skill-mcp" init --no-register
skill-mcp --data-dir "$HOME/.skill-mcp" import --source directory --path "/absolute/path/to/reviewed/agent-skill-bundle" --no-index
skill-mcp --data-dir "$HOME/.skill-mcp" build-index
skill-mcp --data-dir "$HOME/.skill-mcp" status
skill-mcp --data-dir "$HOME/.skill-mcp" search "verify a safe release" --k 5
```

Package version alone does not pin dependency wheels; enforce package hashes / a lockfile if reproducibility is required. The source commit above is for provenance, not proof that every distribution artifact matches. `init --no-register` is deliberate: running bare `init` can modify several agent/editor MCP configurations. This bundle does not run it.

**Do not run `pull` by default.** It downloads a remote prebuilt skill database from Hugging Face; `pull --include-index` downloads an index as well. The advertised 374 skills are an optional, separate third-party dataset, not included in the 135 bundled skills. Do not run `--replace` on an existing database. Review licenses and contents before any optional corpus import.

## Configure the one Antigravity MCP server

Use Antigravity IDE's MCP Servers → Manage MCP Servers → View raw config, or its own global `~/.gemini/config/mcp_config.json`. Merge an entry into the existing `mcpServers` object. Use actual **absolute local paths** to the Python executable and the same data directory used by the import. Never overwrite existing MCP servers or commit user-specific configs into the public bundle.

```json
{
  "mcpServers": {
    "skill-retrieval": {
      "command": "/absolute/path/to/skill-mcp",
      "args": [
        "--data-dir",
        "/absolute/path/to/local/.skill-mcp",
        "serve"
      ]
    }
  }
}
```

The argument order matters: `--data-dir` precedes `serve`. On Windows use your actual executable path; correctly escape backslashes in JSON or use forward slashes. Keep local `stdio` transport; do not expose the service publicly. Private skill content should use a separately permissioned local data directory, **never this public repository**. Indexed text persists in SQLite/FAISS and may appear in logs. Do not use a cloud embedding backend for confidential content without explicit approval.

## Verify

1. Run `status` and inspect the actual imported count; do not assume 135 were all indexed.
2. Reload the MCP server in Antigravity and use `list_categories`, `keyword_search`, `search_skills`, then `get_skill`.
3. For a retrieved support-file reference, open that file in the original bundle and validate its contents and license.
4. Keep `i-have-adhd` as the primary communication style and the bundle's verification/security rules for actual execution.

The upstream author's measured retrieval benchmark is not an independently verified speed or relevance guarantee on the user's device or projects.
