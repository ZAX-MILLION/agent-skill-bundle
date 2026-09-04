# Universal Project Security Discovery

Run this read-only discovery before security-relevant implementation or review unless the task is a trivial text-only change.

## Goal

Build a `PROJECT_SECURITY_PROFILE` from evidence in the repository and environment. Do not assume the project is a web app.

## Phase 1 — fingerprint the project

Inspect, without executing untrusted project scripts first:

- repository tree and entry points;
- language manifests and lockfiles (`package.json`, `pyproject.toml`, `requirements*`, `go.mod`, `Cargo.toml`, `composer.json`, Gradle/Maven files, `.csproj`, Xcode/Swift manifests, C/C++ build files, etc.);
- framework/runtime configuration;
- Docker/container/IaC/reverse-proxy/deployment files;
- database migrations/schema/policies;
- auth/session configuration;
- environment-variable names and example env files, without exposing secret values;
- CI/CD and release/update configuration;
- mobile manifests/entitlements/permissions;
- desktop packaging, code-signing and auto-update configuration;
- native/FFI/unsafe-code boundaries;
- plugins/extensions/hooks/IPC/network listeners;
- tests, security tooling and dependency audit configuration.

Determine exact versions from lockfiles/runtime metadata where possible. Do not infer versions from memory when the repository can prove them.

## Phase 2 — classify project types

A project may have several classes simultaneously:

- web frontend / SSR application;
- backend / API / microservice;
- mobile Android/iOS/cross-platform;
- desktop/thick client/Electron/Tauri/native GUI;
- CLI/tooling;
- daemon/background worker/network service;
- reusable library/SDK/package;
- native/system software (C/C++/Rust/FFI/unsafe);
- WordPress/CMS/plugin/theme;
- browser extension/plugin ecosystem;
- infrastructure/IaC/container/platform automation;
- embedded/IoT/firmware;
- AI/LLM/RAG/agent/tool-calling application.

Do not force the project into one category.

## Phase 3 — discover attack surface

Record only surfaces that actually exist:

- public network listeners/endpoints;
- auth/login/admin/recovery flows;
- APIs/RPC/GraphQL/WebSocket/IPC;
- databases/object storage/caches/queues;
- file parsing/uploads/downloads/archive extraction;
- outbound URL fetchers/webhooks/callbacks;
- browser rendering/user-generated content;
- local filesystem/config/temp files;
- shell/process execution;
- privileged OS/device permissions;
- mobile deep links/WebViews/intents/keychain/keystore;
- desktop URI handlers/auto-updaters/plugins/IPC;
- native parsers, memory-unsafe code and FFI;
- cryptography/signing/update verification;
- payments/credits/quotas/workflow state;
- AI prompts, RAG sources, model tools and external content ingestion;
- CI/CD, registries, deployment credentials and production services.

## Phase 4 — identify trust and value

For every relevant surface identify:

- attacker-controlled inputs;
- identities/roles/tenants;
- privileged operations;
- sensitive assets/data;
- trust transitions;
- security controls already present;
- controls that appear missing, bypassed or duplicated inconsistently.

## Output

Produce a compact internal profile before selecting references:

```text
PROJECT_SECURITY_PROFILE
Types: ...
Languages/runtimes: ...
Frameworks/versions: ...
Deployment: ...
Data/auth/storage: ...
Public surfaces: ...
Privileged surfaces: ...
Native/mobile/desktop/AI surfaces: ...
Security tooling already present: ...
Unknowns that materially affect security: ...
```

Then use `standards-research.md` and `README.md` to route the applicable security checks.

## Safety rules during discovery

- Do not run install scripts, migrations, deployment commands, unknown binaries, or project hooks merely to identify the stack.
- Do not print secret values discovered in files/environment.
- Do not modify production data or configuration during discovery.
- If repository evidence conflicts with documentation, treat executable/configuration evidence as stronger but report the discrepancy.
- If the project cannot be fully classified, apply the generic baseline plus every clearly applicable specialized profile; do not skip security because classification is imperfect.
