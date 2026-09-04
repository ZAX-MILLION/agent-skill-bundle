# Embedded / IoT / Firmware Security Profile

Use for firmware, embedded devices, IoT products, appliances, controllers and device software with physical interfaces or OTA updates.

## Discover

- MCU/SoC/RTOS/OS and architecture;
- boot chain, secure boot and firmware signature verification;
- OTA/update mechanism and rollback/downgrade policy;
- debug/test interfaces (JTAG/SWD/UART/serial/service ports);
- default credentials/provisioning/device identity;
- local network/radio protocols (Wi-Fi, BLE, Zigbee, MQTT, proprietary protocols, etc.);
- cloud/backend APIs and device authentication;
- local storage/flash/NVRAM secrets;
- factory reset/recovery mode;
- physical buttons/USB/removable media;
- memory-unsafe/native parsers and protocol handlers;
- third-party libraries/SDKs/bootloaders.

## Required controls

- No universal/default production credential that grants privileged access across devices.
- Generate/provision device identities and secrets with appropriate uniqueness and entropy.
- Verify firmware/update authenticity before installation; protect against unauthorized downgrade when required.
- Disable or appropriately protect production debug/test interfaces.
- Treat local network/radio peers as untrusted; authenticate privileged operations.
- Do not expose cloud/admin credentials in firmware images.
- Protect sensitive flash/storage when threat model requires it; avoid plaintext reusable secrets when hardware/platform protection is available.
- Bound protocol/parser inputs and apply native-memory safety guidance where applicable.
- Recovery/factory-reset modes must not create unintended privileged bypasses.
- Minimize network services and ports; fail closed on malformed/unauthenticated management traffic.

## Adversarial checks

- unsigned/modified/downgraded firmware rejected where policy requires;
- default/factory credentials cannot authenticate after provisioning unless explicitly designed;
- unauthenticated LAN/radio peer cannot invoke admin/control action;
- debug/service interface does not expose production secrets/control unintentionally;
- malformed protocol packets cannot trivially crash/corrupt state or bypass auth;
- extracted firmware does not contain reusable fleet-wide cloud/admin secrets;
- recovery/reset path does not bypass ownership/account security unexpectedly.

## Release blockers

- unsigned privileged firmware update path;
- fleet-wide hardcoded admin/cloud credential in firmware;
- unauthenticated privileged device-control service;
- production debug interface exposing sensitive control/secrets without deliberate protection;
- known remotely reachable memory-corruption/parser issue;
- recovery/downgrade path that bypasses core security without explicit design/risk acceptance.
