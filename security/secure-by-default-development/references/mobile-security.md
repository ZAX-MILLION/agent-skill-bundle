# Mobile Application Security Profile

Use for Android, iOS and cross-platform mobile applications (React Native, Flutter, Kotlin Multiplatform, Capacitor and similar).

Use the current OWASP MASVS/MASTG family as a primary mobile verification reference, then apply platform/vendor guidance for the actual SDK/OS targets.

## Discover

- requested permissions/entitlements;
- exported Android components, intents, app links/deep links and custom URL schemes;
- iOS URL handlers, associated domains and entitlements;
- local databases/preferences/files/caches/backups;
- Keychain/Keystore usage;
- WebViews/browser bridges;
- network security configuration/TLS exceptions;
- push notifications;
- screenshots/clipboard/logging of sensitive content;
- biometric use and fallback semantics;
- app signing/distribution/update path;
- native modules/FFI;
- device identifiers, analytics and privacy SDKs.

## Rules

- Request the minimum OS permissions; sensitive permissions require a real feature need.
- Keep long-lived private credentials out of app binaries. Mobile clients are attacker-controlled clients.
- Store sensitive local credentials using platform secure storage where appropriate, not plain preferences/files.
- Validate deep links/intents/universal links before privileged navigation/action; do not trust caller-supplied state.
- Restrict exported components/URL handlers/IPC to what is necessary.
- Harden WebViews: minimize JavaScript/native bridges, restrict navigation/origins and treat web content as hostile.
- Do not disable TLS verification or hostname validation. Certificate pinning is a context-dependent defense, not a substitute for correct TLS/authentication and must have an operable rotation/recovery strategy.
- Prevent sensitive data from leaking through logs, backups, notifications, clipboard, screenshots or analytics when relevant.
- Server authorization remains mandatory; device checks, biometrics and hidden UI do not authorize server resources by themselves.
- Review third-party SDK data collection and permissions.

## Adversarial checks

When relevant test:

- tampered client request cannot change role/user/tenant/price/entitlement;
- crafted deep link/intents cannot reach privileged state without authorization;
- another app cannot invoke exported component/IPC beyond intended capability;
- sensitive token/data is absent from ordinary logs/backups/plain local storage;
- WebView cannot navigate/bridge to unintended privileged content;
- invalid TLS/certificate is rejected unless explicit development-only configuration;
- rooted/jailbroken/emulated device assumptions do not become the only server security boundary.

## Release blockers

- reusable server/admin secret embedded in the app;
- privileged server action authorized only by client/device state;
- sensitive token stored plainly when secure platform storage is available/required;
- broadly exported privileged component/deep-link action without authorization;
- production TLS validation disabled;
- unsafe WebView/native bridge exposing privileged behavior to untrusted content;
- known mobile dependency/SDK critical vulnerability affecting the shipped version without mitigation.
