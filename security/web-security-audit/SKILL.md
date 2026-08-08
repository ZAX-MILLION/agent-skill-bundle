---
name: web-security-audit
description: Scan WordPress/Node/SPA sites for vulns and harden them.
---

# Web Security Audit & Hardening

Methodology for scanning web apps the user owns/authorizes, reporting findings, and producing **self-contained hardening prompts** another agent (or the user) can execute. Always verification-driven: every fix ships with a verify command and expected result.

## Scope rules (state these up front)
- Authorized targets only (user's own sites, bug-bounty programs). Refuse unauthorized testing.
- The user may ask for a "prompt to fix" instead of direct access — produce a handoff prompt with exact config blocks + verify commands.
- Separate findings into 🔴 CRITICAL / 🟠 WARNING / 🟢 OK.

## Phase 1 — Recon
```bash
getent ahostsv4 <domain>            # DNS
curl -sI https://<domain>/ | head   # headers, server fingerprint
curl -s https://<domain>/cdn-cgi/trace | grep -E "ip=|colo="  # ⚠️ ip= is YOUR IP, not origin
```
Identify stack: WordPress (wp-json/readme), React SPA (index.html fallback), Node API (json endpoints).

## Phase 2 — WordPress checklist
Test each, record status codes:
- `xmlrpc.php` — `system.multicall` = brute-force amplifier → **403 it** (`location = /xmlrpc.php { return 403; }`)
- `wp-json/wp/v2/users` — user enumeration → **403**; also block `/author/<user>/` via `template_redirect` + `is_author()` redirect (REST block alone does NOT stop `?author=1`)
- `readme.html`, `license.txt` — version fingerprinting → 403
- `wp-content/plugins/<p>/readme.txt` — plugin version disclosure → 403 all `*.txt|md|html` under plugins/themes
- `wp-login.php` brute force — Cloudflare Managed Challenge (see below) or limit-login-attempts plugin
- security headers — missing X-Frame-Options/HSTS/nosniff → add nginx `add_header` block
- `.env`, `.git/config`, `wp-config.php.bak` — expect 403/404
- user profile JSON leaks old server URLs in `"url"` field → clear via `wp user meta update <id> url ""`

## Phase 3 — Node/SPA checklist
- **SPA fallback false positive:** any nonexistent path returns 200 with index.html. ALWAYS compare content (md5) against the homepage before declaring exposed files. `.env` returning 200 ≠ leak.
- CORS: OPTIONS with `Origin: https://evil.com` + `Access-Control-Request-Headers` — `allow-credentials: true` WITHOUT an `allow-origin` whitelist is a footgun (not exploitable today; fix with explicit origin array). Never `*` with credentials.
- Rate limiting: fire N+1 login attempts → expect 429 after the limit (verify the threshold, don't assume).
- User enumeration: login error must be identical for existing/nonexistent users.
- NoSQLi probe: `{"username":{"$ne":null}}` → must reject.
- IDOR: guess IDs on profile/user/room endpoints → 404.
- Hardcoded secrets in served JS: grep for `sk-`, `api_key`, `secret` patterns (benign "token" strings are fine).
- WebSocket auth: see script below — an unauthenticated `101` + session `sid` = auth gap.

## Phase 4 — Cloudflare rules (the login-challenge question)
- **Managed Challenge works on PAGE routes** (wp-login, wp-admin, SPA pages) — browser shows "verify you're human".
- **NEVER Managed Challenge on API/fetch endpoints** (`/api/auth/login`) — it blocks the app's own XHR and breaks login for real users. Use a **rate-limit rule** there (e.g. 20 req/10s → block 15 min).
- Always pair Cloudflare rules with app-level rate limiting (works when attacker bypasses CF via origin IP).

## Pitfalls (learned the hard way)
- REST users-API block ≠ full user-enumeration fix — author archives leak usernames separately.
- `xmlrpc.php` 405 vs 403: a responding method list means it's enabled; must be 403.
- WS raw-HTTP tests fail with "plain HTTP to HTTPS port" — always test WS over TLS (python ssl), and check the server sends an **error packet after 101, not a sid**.
- Security headers on nginx: `add_header` only applies where defined — add to BOTH the site block and the API/proxy block.
- The client's `cdn-cgi/trace` shows the *requester's* IP — never report it as origin.
- Rate-limit verify: after tripping the limit once, later attempts 429 immediately (longer block window) — record first-429 threshold, don't re-trigger.

## Deliverable
A hardening prompt with: finding → exact fix (full nginx block / code) → reload/restart → **verify command + expected output** → "do not mark done unless verify passes". Include a post-fix checklist block of all verify commands with expected values.

## Re-verifying another agent's claimed fixes
When the user says "the other Hermes / Cursor claims everything is fixed" — DO NOT trust the report. Re-run the full original checklist yourself (expected-vs-actual table) before confirming:

- Re-run EVERY check from the original scan, not just the headline ones. In practice a claimed-complete pass still misses items: REST users-API blocked but `?author=1` still 200; CORS fixed but WS still hands out a session ID with no token.
- Present results as a table: check | expected | actual | ✅/❌. "8 of 10 fixed" lands harder than "he said done."
- For the missed items, produce a **remaining-fixes prompt** (same structure: finding → fix → verify) and hand it back. Include the exact probe used to catch the miss (e.g. the WS handshake script) so the other agent proves the fix, not just claims it.
- Trap to bake in: "101 Switching Protocols is fine — but the server must then send an error packet, NOT a `sid`. If you still get a sid, the middleware isn't running." Forces real verification instead of "looks done."

## Support files
- `scripts/ws-auth-test.py` — TLS WebSocket auth probe (connect without token, print status + server response)
- `references/wordpress-audit-checklist.md` — full WP check/fix/verify command set
- `references/node-spa-audit-checklist.md` — CORS/rate-limit/WS/SPA checks
