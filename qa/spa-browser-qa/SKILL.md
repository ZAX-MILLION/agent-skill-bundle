---
name: spa-browser-qa
description: "QA authenticated SPAs: auth bypass, routes, screenshots."
version: 1.0.0
category: software-development
tags: [qa, browser, spa, auth, screenshots, react, testing]
---

# SPA Browser QA

Drive authenticated single-page apps (React/Vite etc.) through the browser toolset for QA, screenshots, and verification. Covers the standard failure modes: form UI that silently won't submit, SPA clicks that don't navigate, snapshot timeouts on heavy canvas pages, and vision analysis errors.

## When to Activate

- User asks for screenshots of app pages/screens (gameplay areas, dashboards, admin panels)
- QA sweep of a web app that requires login
- Navigating an SPA where direct URL changes or clicks don't seem to work
- Any React/Vite app with client-side routing and a JSON API

## Workflow

### Phase 1: Authenticate (bypass broken form UI)

Try the form first (snapshot → fill → click). If the form silently fails (page doesn't change, no error, no token in storage):

1. Check the API directly from the page console:
   ```js
   fetch('/api/auth/register', {method:'POST', headers:{'Content-Type':'application/json'},
     body: JSON.stringify({username:'X', email:'x@y.z', password:'P', confirmPassword:'P'})})
     .then(r=>r.json()).then(d=>JSON.stringify(d))
   ```
2. Discover the auth storage key by regexing the main JS bundle:
   ```js
   fetch('/assets/index-*.js').then(r=>r.text()).then(t=>{
     const m=[...t.matchAll(/localStorage\.(get|set)Item\(['"]([^'"]+)['"]\)/g)].map(x=>x[2]);
     return [...new Set(m)].join(', ')})
   ```
3. Inject the token and reload:
   ```js
   localStorage.setItem('token', d.token); localStorage.setItem('user', JSON.stringify(d.user))
   ```
4. Verify login took: nav bar shows Dashboard/avatar instead of Log In/Sign Up. Note: some apps authenticate by **username, not email** — if email login 404s, retry with username.

### Phase 2: Discover routes

Clicks on cards/links may not navigate (JS handlers ignored by automation). Parse the bundle for route paths instead:

```js
fetch('/assets/index-*.js').then(r=>r.text()).then(t=>{
  const m=[...t.matchAll(/path:\s*['"]([^'"]+)['"]/g)].map(x=>x[1]);
  return [...new Set(m)].join(', ')})
```

Then navigate directly (`browser_navigate` to the URL). Route params like `/game/uno/:roomId` need a room — create one through the UI (e.g. lobby "Solo Play" spawns a room vs bots instantly).

### Phase 3: Verify state when snapshots time out

Heavy 3D/canvas pages (3D boards, WebGL) make `browser_snapshot` time out after 30s. Don't retry it — verify state via console instead:

```js
JSON.stringify({title: document.title, hasBoard: !!document.querySelector('canvas, [class*=board]'), text: document.body.innerText.slice(0,300)})
```

`location.href` confirms you reached the right route.

### Phase 4: Capture and deliver screenshots

`browser_vision` may fail with a 400 ("unknown variant image_url") on non-vision models — but it ALWAYS saves the screenshot first and returns `screenshot_path`. Treat the analysis as optional:

1. Call browser_vision anyway; use the returned `screenshot_path`.
2. Copy screenshots to a deliverable dir with clean names (`cp` to e.g. `/cursor-noise/screenshots/<app>/<page>.png`).
3. Deliver via `MEDIA:<path>` lines. Tell the user the images are real captures even if auto-description failed.

## Phase 5 — Bulk demo capture (many pages, sales/presentation screenshots)

When the user needs 10+ screenshots of an authenticated app (sales demo, pitch deck), don't drive each page through the browser toolset — write a **Playwright script** (python) that logs in once and walks routes:

- Install: `pip install playwright` (chromium is usually already cached under `/root/.cache/ms-playwright/` — `launch(headless=True, args=["--no-sandbox"])` picks it up).
- Pattern: login via UI selectors → `page.goto(BASE + "/" + route, wait_until="networkidle")` → `wait_for_timeout(2500)` → `page.screenshot(path=...)` for BOTH viewport and `full_page=True`.
- **Discover routes from the live DOM, not just the JS bundle:** after login, dump `document.querySelectorAll('a[href*="#/"]')` hrefs (Angular/React hash routing) — gives exact section URLs (`#/admin/teacherPortal/teacherCourses/3061/enrolledStudents`). Course/detail pages need the entity ID — click a real card first to learn the URL pattern, then derive siblings.
- **Angular-specific: `wait_until="networkidle"` TIMES OUT.** Angular apps with websockets/long-polling never go idle → `page.goto(..., wait_until="networkidle")` hangs until the 30s timeout. Use `wait_until="domcontentloaded"` + `wait_for_timeout(2500-4000)` instead. This is the #1 silent failure on Angular (PrimeNG/Material) admin panels.
- **Angular renders hidden template inputs.** A login page can show `document.querySelectorAll('input').count() == 17` because the template holds hidden inputs for other forms. Only ~2 are visible. Select by placeholder (`input[placeholder*="اسم المستخدم"]`) or filter by visibility (`getBoundingClientRect().width > 0 && getComputedStyle(el).display !== 'none'`). Filling `boxes.nth(0/1)` from the raw NodeList may hit the wrong (hidden) fields.
- **Some sidebar items are BUTTONS, not links** — the menu looks like links but submenus open via click handlers. Dump `a[href*="#/"]` first; then click remaining menu items (by visible text) and read `location.href` after each click to discover the button-driven routes.
- **Same platform may be reachable at multiple origins** (e.g. `ed.arishuniversity.com` landing vs `mydemo.kenanaschool.com` app). The landing page is marketing; the real app/login is often another subdomain. Ask the user or probe both before assuming the marketing site is the app.
- Clear toasts/overlays before each shot: `document.querySelectorAll('p-toast, [class*="toast"]').forEach(e=>e.remove())`.
- Screenshot dir: `/cursor-noise/screenshots/<app>/` with meaningful names (`S01-teacher-home.png`).

### THE DATA-DENSITY CHECK (critical for demo shots)

Demo screenshots are only worth anything if the pages show REAL data. After capturing, programmatically verify each page's content density before delivering:

```python
txt = await page.evaluate("document.body.innerText")
txt_clean = " ".join(txt.split())
empty_markers = ["لا توجد", "لا يوجد", "لا تتوفر", "لا توجد بيانات", "لا توجد مهام", "لا توجد اختبارات"]
found = [m for m in empty_markers if m in txt_clean]
```

Then report an **expected-vs-actual table** mapping each user requirement → screenshot → data status (filled / partially empty / empty page). The user's requirement is usually explicit ("data must be filled, not zeros") — do NOT deliver zero-filled screenshots as final. Either:
- **A)** enrich the demo through the UI (add questions, assessments, attendance records) then re-shoot — best result, ~15-20 min automated
- **B)** re-shoot specific pages after the user adds data manually
- **C)** deliver as-is with the gaps clearly flagged and let the user choose

Always deliver the honest current-state screenshots (MEDIA: lines, one per image) with the gaps table, THEN ask which enrichment path they want. Never silently ship empty pages as if they were complete demos.

## Pitfalls

- **Don't loop on identical failures.** Snapshot timing out twice = switch to console checks. Vision 400ing repeatedly = keep using it only for capture.
- Dismiss modal dialogs (notification prompts, toasts) after login before interacting.
- Test accounts created via API are fine for QA — record credentials in the skill's reference file for reuse.
- SPA nav links may render but route nowhere in automation — prefer direct URLs from Phase 2.
- After any localStorage injection, do a full `browser_navigate` (not just reload) so the app boots fresh with the token.

## Verification

- Nav bar shows logged-in state after injection + reload
- `location.href` matches expected route
- Screenshot files exist and are non-trivial size (>50KB suggests real content, not blank page)
- Every requested page has a screenshot before reporting done

## Support Files

- `references/cardnite-qa.md` — CardNite (up.zaxbot.xyz) specifics: test account, API endpoints, route map, per-game notes
- `references/kenana-school-demo.md` — Angular school platform demo: login quirk (aria-busy submit), full route map, data-density findings, working scripts
- `references/eduagent-kenana-school.md` — eduAgent/CODIATOR school platform (mydemo.kenanaschool.com): 3 accounts (manager/teacher/student), login quirk (17 hidden inputs), full manager route map, course sub-routes, strong-vs-weak page findings, reusable scripts
- `references/spa-ui-bug-patterns.md` — Angular SPA UI bug patterns: dead-button proof (file-picker hook), raw server errors in localized UIs, silently disabled submits, broken template pipes, i18n half-translation, console-error mining, token-in-WebSocket-URL, hash-nav session-drop handling

For the FULL sales package built from these screenshots (3 presentations + warnings report + QR codes + organized folder), see the `sales-demo-packaging` skill.
