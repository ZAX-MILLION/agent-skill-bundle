# CLI, Service & Library Security Profile

Use for command-line tools, daemons/background workers, reusable packages/SDKs, developer tooling and internal automation.

## CLI / developer tools

- Treat command arguments, environment variables, config files, stdin, repository contents and filenames as untrusted when they can originate outside the trust boundary.
- Avoid shell-string construction; invoke processes with argument arrays/direct APIs.
- Never print reusable secrets by default. Consider that command-line arguments can appear in process listings/history.
- Use restrictive config/cache/token file permissions where sensitive.
- Use safe temporary files/directories and clean them predictably.
- Validate paths and prevent traversal/symlink surprises before destructive writes/deletes.
- Require explicit confirmation/scope for destructive or privileged operations; dry-run when appropriate.

## Daemons / workers / network services

- Inventory every listener/port/socket. Bind only to required interfaces.
- Authenticate/authorize admin/control sockets and management APIs.
- Bound queue/job/input sizes, retries, concurrency and resource usage.
- Make poison-message/error handling fail safely rather than retrying indefinitely or bypassing validation.
- Separate worker privileges/credentials by function where practical.
- Treat message-queue payloads and scheduled job parameters as untrusted inputs.

## Libraries / SDKs

Libraries create security defaults for downstream users:

- secure behavior should be the default; dangerous behavior requires explicit opt-in;
- do not silently disable TLS/certificate checks, input validation or signature verification;
- minimize transitive dependencies and install-time execution;
- avoid global mutable security state;
- clearly separate public and privileged APIs;
- validate boundary inputs even when callers are "developers" if the API processes external data;
- do not leak internal secrets/credentials through exceptions/debug representations;
- maintain compatibility without preserving known insecure defaults indefinitely.

## Adversarial checks

- crafted args/config/path cannot inject shell commands or escape allowed roots;
- sensitive CLI secrets are not echoed/logged/history-exposed unnecessarily;
- daemon management interface is not publicly/locally callable without intended authorization;
- oversized jobs/retries cannot trivially exhaust resources;
- library insecure option is not enabled by default;
- malicious downstream input cannot trigger unsafe deserialization/code loading unexpectedly.

## Release blockers

- command execution built from untrusted concatenated strings;
- destructive filesystem operation with attacker-controlled/uncontained paths;
- unauthenticated privileged daemon/control interface;
- reusable secret printed/logged by normal operation;
- library defaults that disable TLS/signature/auth checks;
- package install hook that performs unexplained privileged/network actions.
