# eduAgent Audit — worked example (2026-08-08)

Target: `mydemo.kenanaschool.com` (Angular hash-routing SPA) → API `api.arishuniversity.com` (ASP.NET, openresty). Multi-tenant via `X-Tenant-Id` header. Demo tenant `mydemo`; REAL production tenant `ed` (ed.arishuniversity.com).

## Login capture (the critical discovery)
- Login XHR: `POST /api/Users/login/` with body `{"email":"amr","password":"..."}` — field is `email`, NOT `username`.
- Headers: `X-Tenant-Id: mydemo` is REQUIRED. Missing → HTTP 400 empty body. Wrong creds → 401 `{"detail":"Failed"}`.
- Token: `localStorage['token']` (opaque, base64-decodes to garbage = encrypted, NOT a tamperable JWT — don't report).
- Credentials failed on first attempt because user gave username typo (`amd` vs `amr`) — the lesson: ASK the user, don't guess.

## Findings (all verified live, then cleaned up)

### 🔴 CRITICAL
1. **Zero-auth read of entire user DB** — `GET /api/MyApplicationUser` with NO token → 200, 891 users (login emails = national IDs, roles, isActive). Also no-auth 200 on: `students` (national IDs), `teachers/teachersSimple/`, `Exams`, `StudentResults`. Delete endpoints DID require auth (401/403) — inconsistent authz.
2. **Zero-auth write** — `POST /api/teachers` with NO token → 200, created teacher (id returned). Test record deleted after (204).
3. **Cross-tenant breach (read + write)** — mydemo token + `X-Tenant-Id: ed` header → read 2,193 users / 771 teachers AND create teachers in the REAL ed tenant (created #825, #826, deleted both, verified back to 771). A low-privilege TEACHER token could do the same. Anonymous (no token) + `X-Tenant-Id: ed` also read ed users → the real university's data is fully exposed.
4. **Open registration** — `POST /api/Users/register` with arbitrary email/password + `"userTypes":["Administrator"]` → 200; account logged in successfully. However the Administrator role was NOT granted (userTypes stayed empty) — partial mitigation only.

### 🟠 HIGH
5. **Low-priv privilege escalation** — teacher account token (`29602151304094`) reads full admin user list + all students (200).

### 🟡 MEDIUM
6. **Delete button broken** — deleting teachers with linked rows returns raw `500 OK` error popup in the UI ("Http failure response … 500 OK | OK"); no friendly message.
7. **i18n broken** — English mode half-translated: menus randomly mix Arabic/English ("شئون العاملين", "إدارة المحتوى", "فئات المنتجات" stay Arabic).
8. **Console errors on every page** — `UserNotifications` 401 even logged in; `Upload/getUploadedFile` 404; JS TypeError in chunk-7X4OIYTP.js.

### ✅ PASSED (tested, reported as good)
- File upload `POST /api/Upload/upload`: blocks `.html/.js/.php/.svg` with "File type not allowed"; double-extension `.html.jpg` fails image-decoder validation (TGA/BMP/PNG/GIF/TIFF decoder list in error proves validation). Filename sanitized (no traversal). Public fetch of uploaded file = normal.
- User enumeration: login + forgotPassword return identical 401/200 for existing vs fake emails.
- resetPassword 400 without valid flow. Token opaque. `getUploadedFile` traversal → 404.

## FK delete chain (mass-deletion technique)
- `GET /api/teachers/teachersSimple/` lists (id, name, enName…). Filter by name (`تجريبي` / `trial`).
- `DELETE /api/teachers/{id}` — works for most (~99/102); fails 500 generic "entity changes" when linked rows exist.
- Blocker tables: `MyApplicationUser` (teacherId column), `TimeTables`, `Lectures` (both expose teacherId). Delete order: linked user accounts → timetable rows → lecture rows → teacher. Retry teacher DELETE after each pass.
- UI delete button calls the same endpoint and shows the raw 500 — the swallowed-error popup is the UI bug.

## Cleanup verification (do this every time)
- After creating test teachers: `DELETE /api/teachers/{id}` (204) in BOTH tenants.
- After registering test user: `DELETE /api/MyApplicationUser/{guid}` (204).
- Final check: GET counts — mydemo back to 6 teachers (3 kept + 3 blocked trial), ed back to 771, no `TEST`/`evil.com` leftovers anywhere.

## Rate-limit / transient quirk
- Rapid-fire curl bursts occasionally return empty/404 for endpoints that worked seconds before (e.g. TimeTables). Wait ~2s and retry before concluding anything changed.
