---
name: wordpress-security
description: Hardens and reviews WordPress security for plugins, themes, uploads, and configuration. Use when auditing WP security or fixing vulnerabilities.
---

# Wordpress Security

## Purpose

Identify and fix WordPress security issues without weakening protections or exposing secrets.

## When to use

Use for security audits, incident review, or hardening requests on WordPress projects.

## Required discovery

- WP path; custom code locations.
- Public endpoints (AJAX, REST, forms, uploads).
- File permission oddities (evidence-based).
- Known vulnerable patterns in custom code.

## Safety checks

- Never display credentials or full config secrets.
- Do not disable security plugins or auth without approval.
- Do not chmod broadly across the server.
- Prefer least privilege fixes.
- No `/srv/OLDIES/` modifications.

## Step-by-step workflow

1. Scope custom code vs vendor code.
2. Scan for SQLi, XSS, CSRF, path traversal, unsafe uploads, privilege issues, exposed secrets (targeted searches).
3. Verify nonces/capabilities on sensitive actions.
4. Propose or apply approved fixes only.
5. Re-check and document residual risk.

## Verification checklist

- [ ] Findings have file/line or clear evidence
- [ ] Secrets redacted
- [ ] Fixes do not reduce security to “make it work”
- [ ] Verification steps listed

## Stop conditions

Stop if live incident needs isolation beyond approved scope; if fix requires firewall/SSH changes (ask first); if credentials must be rotated by the user.

## Final report format

Write a concise report (and save under `/.cursor/reports/` for substantial work) covering:

- What was inspected
- What was changed
- Files changed
- Commands run
- Tests performed
- Results
- Remaining risks
- Manual checks required

Redact secrets. Use project name + timestamp in the filename when saving.
