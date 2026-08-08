---
name: wordpress-security-audit
description: Audit & harden WordPress sites. Use when security-testing.
---

# WordPress Security Audit

Authorized testing only (own sites, client sites, bug-bounty programs). Recon → probe → harden.

## Recon
- DNS: `getent ahostsv4 domain` — note if Cloudflare proxies (NS = *.ns.cloudflare.com)
- Origin behind Cloudflare: `curl -s https://domain/cdn-cgi/trace` shows real origin IP; probe origin IP directly with `curl -sI http://ORIGIN_IP/ -H "Host: domain"`
- Headers: `curl -sI https://domain/` — server fingerprint (nginx 1.24 + `X-Redirect-By: WordPress` reveals stack)

## Probe checklist (each = one curl)
1. **WP version**: grep `<meta name="generator"` in homepage HTML; also `/readme.html`, `/license.txt`
2. **User enumeration**: `GET /wp-json/wp/v2/users` → leaks admin usernames (JSON). Also `/?author=1` redirect location reveals slug.
3. **XML-RPC**: POST `/xmlrpc.php` with `system.listMethods` → if `system.multicall` present, attackers batch hundreds of password guesses in ONE request (brute-force amplifier).
4. **Brute force**: 3 failed POSTs to wp-login.php → no lockout/delay = unprotected.
5. **Exposed files**: wp-config.php.bak, .git/config, .env, debug.log, wp-content/debug.log
6. **Plugin disclosure**: `/wp-content/plugins/<slug>/readme.txt` → 200 = version fingerprinting (CVE targeting). Check common slugs: elementor, woocommerce, akismet, contact-form-7.
7. **Directory listing**: `/wp-content/uploads/`, `/wp-content/plugins/` → 200 with "Index of" = browsable
8. **Security headers**: X-Frame-Options, Strict-Transport-Security, X-Content-Type-Options, Content-Security-Policy — all absent = clickjacking/downgrade risk

## Fixes (nginx origin)
- Block xmlrpc: `location ~ /xmlrpc.php { deny all; }`
- Block user enum: `location ~* ^/wp-json/wp/v2/users { deny all; }`
- Block readme/license: `location ~* /(readme\.html|license\.txt|readme\.txt)$ { deny all; }`
- Security headers: `add_header X-Frame-Options "SAMEORIGIN" always; add_header X-Content-Type-Options "nosniff" always; add_header Strict-Transport-Security "max-age=31536000" always;`
- Brute force: Cloudflare WAF rate-limit rule on /wp-login.php, or fail2ban on origin
- Stronger: Cloudflare "Security Level" + "Bot Fight Mode" for the domain

## Pitfalls
- Cloudflare masks origin — always test the origin IP directly too; a 403 from Cloudflare is NOT the origin's answer
- `readme.txt` is per-plugin: 404 for one slug doesn't mean no plugins are installed — probe a list
- REST user endpoint returns user `url` field too — can leak the OLD server IP after a migration (seen live: user.url pointed at decommissioned box)

## Support files
- `references/audit-probes.md` — copy-paste command sequence for a full scan
