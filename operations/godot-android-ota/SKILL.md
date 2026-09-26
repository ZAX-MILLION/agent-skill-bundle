---
name: godot-android-ota
description: Validate Godot Android APK and signed content OTA releases with offline rollback.
---
# godot android ota

1. Read actual project engine/export settings, signing, SDK, ABI, renderer, device tier, save schema and asset constraints.
2. Separate base APK native changes from content-only OTA. Require compatible manifest, version, integrity and atomic activation.
3. Verify clean install, launch, game assets, saves, performance and release endpoint, not only green CI.
4. Retain last known-good package and offline launch; test failed downloads and rollback.
5. Release only approved target and report artifact identity, checks and rollback.

For code/config/security work also use `security/secure-by-default-development` and `process/verification-before-completion`.
