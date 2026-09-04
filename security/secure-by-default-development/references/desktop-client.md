# Desktop / Thick Client Security Profile

Use for Windows/macOS/Linux desktop software, Electron/Tauri apps, native GUIs, launchers/updaters and locally executed client applications.

Use current OWASP TCASVS where applicable, plus OS/runtime vendor hardening guidance.

## Discover

- local privilege level and requested OS capabilities;
- auto-update mechanism and signature verification;
- code signing/notarization/package signing;
- IPC, local sockets, named pipes, loopback HTTP servers;
- custom URI/file handlers;
- plugins/extensions/scripts/macros;
- embedded browsers/WebViews/Electron preload/bridge code;
- local credential/config/database storage;
- sensitive temp/cache/crash/log files;
- file format parsers and archive handling;
- shell/process execution;
- DLL/library/plugin search paths;
- backend APIs and offline authorization assumptions.

## Rules

- Treat the local user/device as potentially hostile; client checks do not authorize remote server data/actions.
- Authenticate and authorize privileged IPC/local service calls; "localhost" alone is not an identity.
- Sign and verify application/update artifacts; auto-update must fail closed on integrity failure.
- Keep updater endpoints and metadata protected against downgrade/tampering where the platform supports it.
- Restrict URI handlers/file associations and validate parameters before navigation/file/process actions.
- Minimize Electron/Tauri/WebView bridges; expose narrow capabilities rather than raw filesystem/shell access.
- Store credentials using platform-protected mechanisms where appropriate.
- Use safe temp-file APIs and restrictive permissions; prevent symlink/path traversal issues.
- Load plugins/modules only from trusted locations with deliberate integrity/trust policy.
- Do not rely on obfuscation to protect reusable secrets embedded in the client.

## Adversarial checks

- untrusted local process/user cannot invoke privileged IPC action without required authorization;
- crafted URI/file cannot cause command execution/path traversal/privileged navigation;
- malicious/unsigned/downgraded update is rejected;
- untrusted web content cannot reach privileged native bridge methods;
- local config manipulation cannot grant remote/admin privileges;
- tokens/secrets do not leak into ordinary logs/crash dumps/temp files.

## Release blockers

- unsigned/unverified privileged auto-update path;
- privileged localhost/IPC service with no meaningful authorization;
- raw shell/filesystem/native capability exposed to untrusted WebView/Electron content;
- reusable backend/admin secret embedded in desktop binaries/config;
- unsafe plugin/module loading from user-writable/untrusted paths;
- production update/TLS integrity checks disabled.
