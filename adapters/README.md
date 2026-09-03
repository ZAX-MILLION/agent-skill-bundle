# Agent Adapters

Adapters make the bundle easier to consume on different AI hosts **without changing upstream skill content**.

## Design rule

A skill remains the source material. An adapter only explains host-specific discovery, installation or capability mapping.

Do not copy an entire skill into an adapter just to rename commands or tools.

## Current support

- `generic/` — host-neutral instructions usable by any AI or agent that can read files/instructions.
- Cursor and Claude Code can already receive the raw skill directories through the root `install.sh` by passing their skills directory.
- Additional host-specific adapters should only be added when the host requires behavior that the generic contract cannot express.

## Capability mismatch

If a skill mentions a capability the current agent does not have (for example terminal, browser, subagents, GitHub or database access), the adapter must not pretend the capability exists. The agent should use the supported parts of the skill and report the unavailable action clearly.
