---
name: api-security-probing
description: "Probe REST APIs for auth gaps and tenant-isolation holes."
---

# REST API Security Probing

Probe multi-tenant REST APIs (Angular/SPA + ASP.NET/LoopBack-style backends) for broken authentication, tenant-isolation holes, open registration, and upload weaknesses. Authorized targets only. Verification-driven: every finding is proven with a live request, and every test record is cleaned up.

## Workflow rule (user correction — read first)
If login credentials fail: **ASK the user immediately** — do NOT burn attempts guessing username/password variations. A typo (e.g. `amd`→`amr`) costs a full round of wasted probes. The user answers in seconds.

## Phase 0 — Login + token capture
- Open the SPA login page in a browser, hook XHR BEFORE clicking login:
  ```js
  window.__reqs = [];
  const oo = XMLHttpRequest.prototype.open;
  XMLHttpRequest.prototype.open = function(m,u){ this.__u=u; this.__m=m; return oo.apply(this,arguments); };
  const os = XMLHttpRequest.prototype.send;
  XMLHttpRequest.prototype.send = function(b){ const x=this; this.addEventListener('loadend',()=>{ try{ window.__reqs.push({url:x.__u,method:x.__m,status:x.status,body:b?String(b).slice(0,200):''}); }catch(e){} }); return os.apply(this,arguments); };
  ```
- Read `window.__reqs` to get the EXACT login payload + headers. Payload may use `email` not `username`; a **tenant header (`X-Tenant-Id`) may be required** (missing → 400 empty; wrong creds → 401).
- Token: `localStorage.getItem('token')` after login. SPA URL may stay `#/login` even when logged in — judge by content (sidebar visible), not URL.
- Decode token: JWT (base64 JSON segments) = inspect for tamperable claims; opaque/encrypted blob (base64-decodes to garbage) = NOT tamperable, don't report.
- NOTE: XHR hook can corrupt subsequent requests (415 errors) — once the payload is captured, reload the page clean and only re-hook if needed.

## Phase 1 — No-auth read/write (the big ones)
- GET every data endpoint (users, students, teachers, exams, results) WITHOUT any token:
  - `200` + real data = critical leak (record counts: e.g. 891 users with login emails + national IDs).
  - Compare with DELETE behavior — writes/deletes often require auth while reads don't (inconsistent authz).
- POST a harmless record (fake name + fake national ID) without token → `200` = anonymous write. **Always delete the test record after** (expect 204) and verify count returns to baseline.
- User enumeration: login with existing vs fake email → must return IDENTICAL responses (same status + body). Same for forgot-password.
- Reset flow: `resetPassword` should 400 without a valid flow/token.

## Phase 2 — Cross-tenant isolation (multi-tenant apps)
- Take tenant A's valid token, swap `X-Tenant-Id` header to tenant B → read AND write into B.
- Test with BOTH a high-priv token AND a low-priv token (e.g. teacher account) — a low-priv user reaching another tenant is the worst variant.
- The demo tenant token may reach the REAL production tenant (e.g. mydemo token → ed.arishuniversity.com data). This is the headline finding when present.
- **Cleanup is critical**: delete every test record from BOTH tenants; verify with fresh GET counts. Leaving test data in a real tenant is an incident.

## Phase 3 — Registration, uploads, IDOR
- Open registration: POST `Users/register` with arbitrary email/password + requested role → 200 + successful login = unapproved account creation. Check if the requested role (Administrator) is actually granted — sometimes stripped (partial fix).
- Upload filter: try `.html`, `.js`, `.php`, `.svg`, double-extension `.html.jpg`:
  - Well-filtered: dangerous types blocked AND image decoders validated (decode error message proves validation) → report as GOOD, not a bug.
  - Public fetch of uploaded files is normal; extension blacklist + decoder validation = secure.
- **Anonymous file DELETE**: after finding a public upload endpoint, probe its delete counterpart (`POST Upload/delete` with `{filePath}`) WITHOUT a token. If it returns 200/"deleted successfully", anyone can destroy existing files (photos, PDFs) → data-destruction finding, often MORE severe than the upload itself. Verify by uploading a file, deleting it no-auth, and confirming 404.
- **Cross-tenant upload**: test upload with `X-Tenant-Id` swapped to another tenant (even the production one) — anonymous file drop into the real tenant's storage is a headline finding.
- IDOR: teacher/low-priv token fetches admin-only endpoints (user list, all students) → 200 = privilege escalation.
- File traversal: `getUploadedFile?fileName=..%2F..%2Fetc%2Fpasswd` → 404 = fine.

## Pitfalls (learned the hard way)
- Rapid-fire curl bursts to the API can trigger transient empty/404 responses — if a probe returns empty/404 but worked seconds ago, wait 2s and retry before concluding the endpoint changed.
- The UI delete button may fail with the same 500 the API returns (FK constraints) — a swallowed raw `500 OK` popup is itself a UI bug worth reporting.
- Teachers/entities with linked rows (user accounts, timetables, lectures) fail DELETE with generic 500 — delete the FK rows first (users → timetables → lectures → entity), then retry.
- Record baseline counts BEFORE any writes so cleanup is verifiable.
- Never report "no auth on endpoint X" from a 200 that might be an SPA index.html fallback — check the body is real JSON data, not HTML.

## Deliverable
Findings grouped 🔴 CRITICAL / 🟠 HIGH / 🟡 MEDIUM, each with: the exact probe command, live response evidence (status + sample), impact in plain language, and what "correct" looks like (401 for no token, tenant scoping server-side, etc.). Separately list what PASSED (no enumeration, upload filters, opaque tokens) — balanced reports land better.

## Support files
- `references/eduagent-audit-2026-08.md` — full worked example: eduAgent demo (mydemo.kenanaschool.com / api.arishuniversity.com) probes, findings, cleanup verification.
