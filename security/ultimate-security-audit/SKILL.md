---
name: ultimate-security-audit
description: "Security audit: apps, sites, themes (OWASP + 10-point)."
---

# Ultimate Security Audit — apps, websites, themes, vibe-coded projects

Use when asked to: "check security", "make it secure", "is my app/site safe?", audit a project against the TikTok security checklist, or before launching/publishing any app. Run the FULL checklist — never skip items. Produce a report table at the end (item, status ✅/⚠️/❌, evidence, fix).

## The 10-point core checklist (from the dev checklist)

### 1. HTTPS everywhere
- **Check:** every public URL serves HTTPS; HTTP redirects to HTTPS (301); no mixed content (http:// resources on https pages).
- **Commands:**
  - `curl -sI https://SITE | grep -i "^HTTP\|strict-transport"` (expect 200/301 + HSTS header ideally)
  - `curl -s http://SITE -o /dev/null -w "%{http_code} %{redirect_url}"` (expect 301 → https)
  - Page source: grep for `http://` resource URLs (mixed content).
- **Fix:** Cloudflare "Always Use HTTPS" (Free plan) or nginx `return 301 https://$host$request_uri;` + `add_header Strict-Transport-Security "max-age=31536000"`.
- **Pass:** all traffic HTTPS, no mixed content.

### 2. Passwords hashed, never plain text
- **Check:** password storage uses a strong salted hash (bcrypt ≥10, argon2, scrypt, or framework default — WordPress `wp_hash_password`/phpass is fine). NEVER md5/sha1/plain.
- **Commands (Node):** `grep -rn "bcrypt\|argon2\|scrypt\|password_hash" server/src/ | head` — expect bcrypt/argon2.
- **Commands (PHP):** `grep -rn "wp_hash_password\|password_hash\|password_verify" .` (WP/php) — `md5(` or `sha1(` on passwords = FAIL.
- **Also check:** the login verify path uses `bcrypt.compare` / `password_verify` / `wp_authenticate` — NOT re-hashing the input and comparing strings.
- **Fix:** migrate to bcrypt; if plain/md5 exists, hash on next login + force reset for old users.
- **Pass:** no plaintext/md5/sha1 password storage anywhere.

### 3. Bot protection
- **Check:** Cloudflare Bot Fight Mode / bot management, or app-level: rate limiting (login, signup, review forms), honeypot fields, captcha on public forms, login brute-force throttling.
- **Commands:** check for rate-limit middleware (`rateLimit`, `express-rate-limit`, `limiter`), honeypot inputs, CF dashboard settings (Bot Fight Mode).
- **Fix:** enable CF Bot Fight Mode (dashboard or `PATCH /zones/{id}/settings/bot_fight_mode {"value":"on"}`); add IP-based throttles to auth/signup/forms (e.g. 5 fails → 15 min lock).
- **Pass:** every public + auth endpoint has some throttling/blocking.

### 4. Session expiry
- **Check:** auth tokens/cookies expire; no eternal sessions.
- **Commands:** `grep -rn "expiresIn\|maxAge\|lifetime\|expires_at" .` — expect JWT `expiresIn` (≤30d), cookie `maxAge`/`lifetime`, session `expires_at` columns.
- **PHP sessions:** `session_set_cookie_params` — `'lifetime' => 0` (browser-close) or short; `'secure' => is_ssl()`, `'httponly' => true`, `'samesite' => 'Lax'/'Strict'`.
- **Fix:** add expiry to tokens; sliding refresh optional; short-lived access tokens + refresh tokens for serious apps.
- **Pass:** every auth credential expires.

### 5. CSRF protection
- **Check:** state-changing requests (POST/PUT/DELETE: login, settings, uploads, deletes) are protected.
- **Cookie-based sessions:** need nonces (`wp_nonce_field`/`check_admin_referer`, or a per-session CSRF token in a meta tag + header) OR `SameSite=Lax/Strict` cookie + origin check.
- **Token-in-localStorage (SPA):** CSRF not applicable to localStorage tokens — note it, but warn about XSS instead (see #8).
- **Commands:** `grep -rn "wp_nonce\|csrf\|SameSite" .` — count nonces vs number of POST handlers (every handler needs one).
- **Fix:** add nonces/CSRF tokens to ALL state-changing endpoints; keep `SameSite=Lax` minimum.
- **Pass:** no state-changing endpoint unprotected.

### 6. Reset links: expire + one-time use
- **Check:** password-reset flow: token is random (≥32 hex), has `expires_at` (≤1-2h), `used` flag enforced, requesting a new reset invalidates old ones, token checked with constant-time compare (`hash_equals`).
- **Commands:** `grep -rn "password_resets\|expires_at\|hash_equals\|used" server/` — verify the handler rejects expired/used tokens (400) and marks used on success.
- **Fix:** add expires_at + used flag + `hash_equals`; invalidate all previous tokens for the user on new request.
- **Pass:** expired/used tokens are rejected; old links die when a new one is requested.

### 7. DB credentials limited (never master/root)
- **Check:** app DB user has least privilege: not root, not a shared admin; only CRUD on its own database.
- **Commands (WordPress):** `grep -oE "DB_USER.*" wp-config.php` — expect a dedicated user (e.g. `wp_myapp`), not `root`.
- **Node/SQLite:** SQLite file (local) is fine; MySQL/Postgres must use a dedicated user.
- **Fix:** create limited user, grant only `SELECT/INSERT/UPDATE/DELETE` on its DB, rotate the password, never commit credentials to git.
- **Pass:** no root/master keys in app config.

### 8. Logs contain NO secrets
- **Check:** logs (debug.log, error logs, webhook logs, pm2 logs, console) must not contain passwords, tokens, API keys, emails, card numbers.
- **Commands:**
  - `grep -rniE "password|token|api[_-]?key|secret" --include="*.log" .` + check `error_log()`/`console.log()` call sites
  - Webhook handlers: ensure they don't log the raw payload (verify tokens are masked/truncated or absent).
  - `grep -rln "RAW\|raw.*data" *-webhook.php` — raw payload logging = FAIL.
- **Fix:** remove secret fields from logs; log only types/amounts/IDs; purge existing logs containing secrets; consider rotating leaked tokens.
- **Pass:** zero secrets in any log output or code path.

### 9. Broken access control
- **Check:** every privileged route verifies identity AND authorization (admin flag, ownership). No endpoint trusts the client blindly.
- **Commands:** `grep -rn "requireAdmin\|isAdmin\|middleware\|can('" server/` — verify middleware actually gates the routes; spot-check: does an admin route verify `user.id` matches + role? Are other users' data accessible by ID without ownership check?
- **WordPress:** admin pages gated (`current_user_can('manage_options')`), custom endpoints check caps; stealth/secret admin paths must still auth.
- **Fix:** add auth middleware to ALL protected routes; ownership checks on resource IDs; never rely on client-supplied role/state.
- **Pass:** unauthenticated/unauthorized requests get 401/403 on every protected route.

### 10. SQL injection
- **Check:** all DB queries parameterized/prepared; no string-interpolated user input into SQL.
- **Commands:**
  - Node (better-sqlite3/pg/mysql2): `grep -rn "db.prepare\|\.execute(\|\.query(" .` — arguments must be `?` placeholders, never template literals with user input.
  - WordPress: `grep -rn "wpdb->query\|wpdb->get_var" .` — every query must go through `$wpdb->prepare()` unless it's a static DDL string with zero user input.
- **Fix:** rewrite interpolated queries with prepared statements; validate/whitelist any dynamic table/column names.
- **Pass:** zero unparameterized queries with user input.

## Deeper OWASP-style checks (run after the 10)

- **Security headers:** `curl -sI https://SITE | grep -iE "content-security-policy|x-frame-options|referrer-policy|permissions-policy"` — add via CF Transform Rules or headers middleware if missing.
- **Cookie flags:** all auth cookies `Secure; HttpOnly; SameSite=Lax/Strict; Path=/`.
- **JWT storage:** localStorage tokens = XSS-theft risk → mitigate with strict CSP + no `dangerouslySetInnerHTML`/`innerHTML` with untrusted data; prefer httpOnly cookies for serious apps.
- **File uploads:** extension/type allowlist, size cap, random filenames, store outside webroot or block execution; image-only endpoints must re-encode (ImageMagick/GD) to kill embedded payloads.
- **Admin/stealth routes:** hidden admin paths (custom slugs, backdoor query params) must STILL require full auth — obscurity is not access control.
- **Third-party code:** never merge OSS code into a commercial product without license review + code review (esp. security/anti-malware scripts).
- **Dependencies:** `npm audit` / `composer audit` for known CVEs on installs.
- **Rate limiting on:** login, signup, password reset, webhooks, admin, file uploads.

## Report format (deliver to user)

| # | Check | Status | Evidence | Fix |
|---|-------|--------|----------|-----|
| 1 | HTTPS | ✅/⚠️/❌ | `curl ...` → 301 + HSTS | ... |

End with: ✅ fixed now (list), ⚠️ needs user action (exact steps), ❌ blocked on X.

## Pitfalls
- Don't claim "secure" from one grep — run every check and cite evidence.
- SameSite=Lax mitigates most CSRF but is not a replacement for nonces on the most sensitive endpoints.
- Log purging ≠ rotation: if a token sat in a log, recommend rotating it.
- WordPress `wp_authenticate` is fine for hashing — don't "fix" what already works.
- Don't change game/app logic during a security pass — security edits only, verify each one (lint + live request).
