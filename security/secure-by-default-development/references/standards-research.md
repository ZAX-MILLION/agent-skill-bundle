# Adaptive Standards & Vulnerability Research

Use this after `project-discovery.md` identifies the actual project type, stack and versions.

## Principle

Do not use one static checklist for every project. Select the relevant current security standards and vulnerability intelligence for the discovered technology.

When web access is available, verify the current stable version/status of a standard before citing it. Do not silently treat drafts as stable requirements.

## Standards routing

Use these as baseline families, then narrow to the project:

- **All software:** current CWE Top 25 plus applicable weakness classes; NIST Secure Software Development Framework (SSDF) as lifecycle/process guidance.
- **Web applications:** OWASP Application Security Verification Standard (ASVS), plus framework/vendor hardening guidance.
- **APIs:** OWASP API Security Top 10 plus API-specific authorization, inventory and abuse testing.
- **Mobile:** OWASP MASVS + MASTG/MASWE for Android/iOS/cross-platform surfaces.
- **Desktop/thick clients:** OWASP TCASVS plus platform vendor security guidance.
- **Open-source dependencies/supply chain:** ecosystem advisories plus OpenSSF Scorecard or equivalent evidence when useful; do not reduce trust to one score.
- **Cloud/IaC/container:** provider/platform hardening guidance plus least privilege, network exposure, secret management and artifact integrity checks.
- **Native/system/embedded:** CWE classes applicable to memory safety, integer handling, unsafe parsing, concurrency, privilege and update integrity, plus compiler/runtime/platform hardening.

Known stable baselines as of 2026-09-04 include OWASP ASVS 5.0.0, OWASP API Security Top 10 2023, the current OWASP MASVS family, NIST SSDF 1.1 final (with SSDF 1.2 still draft), and the 2025 CWE Top 25. Re-verify rather than assuming these remain current indefinitely.

## Version-aware vulnerability research

For dependencies, frameworks, runtimes, operating systems, plugins, containers and services:

1. Determine the **installed/resolved version** from lockfiles, runtime metadata or image digests/tags.
2. Search authoritative sources first:
   - vendor/security advisories;
   - GitHub Security Advisories when relevant;
   - ecosystem advisory databases/tooling;
   - OSV/NVD/CVE records as appropriate;
   - CISA Known Exploited Vulnerabilities for known active exploitation where relevant.
3. Match advisories to the actual version/range. Do not flag an unrelated CVE because the package name merely resembles another product.
4. Separate:
   - known affected;
   - known fixed;
   - not affected by version/configuration;
   - unknown/unverified.
5. Prioritize exploitable attack paths, known exploitation, network exposure, privilege and sensitive data impact.

## Ecosystem tooling

Prefer the project's existing package/audit tools first (examples: npm/pnpm/yarn audit workflows, pip/uv/poetry ecosystem scanners, `govulncheck`, `cargo audit`, Composer audit, Maven/Gradle/.NET security tooling) when available and appropriate.

Do not install a random security package just to satisfy this skill. If additional tooling would materially improve verification, explain it and use a trusted source/version.

## Framework/vendor research

If the project uses a framework or platform with security behavior that changes by version, research the exact major/minor version when material. Examples include authentication libraries, Next.js/React, WordPress/plugins, Supabase/Postgres, Electron/Tauri, mobile SDK targets, reverse proxies and container runtimes.

Check for:

- security advisories affecting the resolved version;
- insecure defaults or changed defaults;
- required migration/hardening notes;
- deprecations that remove security fixes;
- configuration that makes an otherwise safe version vulnerable.

## Research quality gate

Do not claim "no known vulnerabilities" solely because one scanner returned zero findings.

A meaningful vulnerability review should combine, as relevant:

- dependency resolution evidence;
- security advisory sources;
- configuration/attack-surface analysis;
- behavioral verification of project-specific controls.

If network research is unavailable, say that current advisory status is unverified and reflect that in the final security verdict when material.
