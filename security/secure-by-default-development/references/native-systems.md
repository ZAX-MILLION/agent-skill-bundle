# Native & Systems Security Profile

Use for C, C++, Rust with `unsafe`, FFI, parsers, native modules, drivers, system services, performance-critical native code, and other software where memory/process boundaries matter.

## Core risks

- out-of-bounds read/write, use-after-free, double-free, uninitialized memory;
- integer overflow/truncation leading to size/allocation bugs;
- unsafe deserialization/parsing of attacker-controlled binary/text formats;
- command/path injection and unsafe environment/search-path behavior;
- race conditions, TOCTOU and concurrency bugs;
- FFI/lifetime/ownership mismatches;
- privilege boundary mistakes and unsafe defaults;
- insecure temporary files, permissions and symlink handling;
- memory/secret disclosure in crashes/logs/core dumps;
- untrusted plugin/module loading.

## Required posture

- Prefer memory-safe language/runtime features where feasible; isolate unavoidable unsafe code.
- Treat every length, offset, count, index and allocation size derived from untrusted input as hostile.
- Use checked arithmetic and explicit bounds before allocation/copy/indexing.
- Minimize raw pointers and unsafe FFI surfaces; document ownership/lifetime contracts.
- Avoid shell execution when direct APIs exist; if unavoidable, never concatenate attacker-controlled command text.
- Use secure temporary-file APIs and restrictive permissions.
- Drop privileges after privileged initialization when architecture allows.
- Do not trust current working directory, PATH, DLL/library search paths, environment variables or relative paths across trust boundaries.

## Verification when available

Use project-supported tools appropriately:

- compiler warnings treated seriously;
- sanitizers (ASan/UBSan/TSan/MSan as applicable);
- fuzzing/property tests for parsers and binary/network inputs;
- static analysis already present in the project;
- tests for malformed/truncated/oversized inputs;
- concurrency tests for valuable shared state.

Do not claim memory safety because unit tests passed.

## Release blockers

- known attacker-controlled memory corruption path;
- unchecked attacker-controlled size/offset used in memory operation;
- unsafe deserialization/code loading from untrusted input;
- command execution assembled from untrusted text;
- privileged service trusting writable search paths/config/plugins;
- exploitable path/symlink/temporary-file race;
- known unsafe FFI ownership/lifetime bug that can corrupt memory.
