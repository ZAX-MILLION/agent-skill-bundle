---
name: frontend-silent-failure-debugging
description: "Debug blank/frozen web apps with zero console errors."
---

# Frontend Silent-Failure Debugging

Use when a web app (React SPA especially) shows a **blank/black screen, an empty page, or freezes** with **no console errors**, or when a "nothing changed / still broken" complaint persists after a deploy. These failures are silent by construction: the crash either happens in a top-level provider with no error boundary (React unmounts the whole tree) or is an infinite redirect loop. This skill is the systematic path to the root cause.

## The failure taxonomy (recognize first)

| Symptom | Likely cause |
|---|---|
| Blank screen, `#root.innerHTML` empty, zero console | Crash in a TOP-LEVEL provider (no boundary around it) OR infinite render/redirect loop that never commits |
| Page renders, then dies after a specific action (login, socket connect) | State change triggers the crash — bisect the action |
| Page works logged-out, blank logged-in | Crash in the authenticated path (socket connect, protected shell, guard logic) |
| URL changes but route never renders | Redirect loop through a pathless layout route, or router context broken |
| Stuck loading spinner forever | A lazy chunk failed to load OR a Suspense boundary never resolves (check chunk HTTP codes) |
| Whole site blank after ANY edit to routing code | Very likely a route-guard/layout-route reconstruction bug (see pitfall below) |

## The debugging method (layer-by-layer instrumentation)

1. **Establish what actually rendered.** In Playwright: `document.getElementById('root')?.innerHTML.length`, `document.body.children.length`, body innerText. Empty root with ThemeWrapper-style background = React mounted then died.
2. **Rule out the server.** Check health endpoint, then test the socket DIRECTLY from node (socket.io-client against the server, emit + listen) — a clean handshake proves the server isn't the problem.
3. **Rule out chunk load failures.** Extract all chunk names from the main bundle, `curl -I` each (404 chunk = Suspense forever).
4. **Rule out auth state.** From the page: localStorage token presence + `fetch('/api/auth/me')` with it. Auth working = the crash is in render logic, not credentials.
5. **Instrument every render layer with `console.log('[DBG] ...')`**: App → each Provider's render → route guards (ProtectedRoute/PublicOnly) → the layout route → the page component. In dev, hot-reload applies instantly; for prod, rebuild+deploy the instrumented build.
6. **Read the log sequence.** The LAST `[DBG]` before silence marks the boundary of the crash:
   - Logs stop INSIDE a guard/layout component, then the SAME guard logs repeatedly → **infinite redirect loop** (see pitfall).
   - Logs stop after a provider renders with new state but its children never render → the provider's render or a useMemo it computes is throwing (or its child crashes between).
7. **Add a top-level error boundary** (`componentDidCatch` rendering the error text) if the app has none — it converts silent unmounts into visible messages.
8. **Check the main thread isn't frozen**: `page.evaluate(() => 1+1)` — if it hangs, it's a synchronous infinite loop (in an effect, event handler, or render), not a crash.

## Pitfalls (all bit in real sessions)

- **RECONSTRUCTING A ROUTE GUARD WRONG = whole-site blank.** When restoring a deleted/refactored `PublicOnlyRoute`-style pathless layout route, it must be a plain `<Outlet />`. Wrapping it with an auth-redirect component (`if (user) return <Navigate to="/dashboard"/>`) makes EVERY route redirect logged-in users to /dashboard → React Router re-renders the same pathless route → **infinite redirect loop → black screen, ZERO console errors, main thread alive**. The redirect belongs ONLY in per-route wrappers, never in the pathless layout route.
- **Top-level providers have no error boundary.** `ThemeProvider > AuthProvider > ... > Routes` — a throw in a provider's render or useMemo unmounts everything with no boundary to show it and (in prod builds) no console output. Instrument provider renders to see the last one that completed.
- **`vite build | tail -5` masks the exit code** — the pipe's exit is `tail`'s (0), so `&& rsync` runs even after a FAILED build and deploys stale/partial dist. Always capture the real status: `npx vite build > log 2>&1; echo "BUILD_EXIT=$?" >> log` and gate the deploy on it.
- **NEVER write `read_file`'s displayed output back to disk.** read_file output carries `NNN|` line-number prefixes AND displays secrets redacted as `***` (e.g. `Authorization: *** ${token}`). A cleanup script that read via read_file and wrote the content back CORRUPTED files (baked-in prefixes, `Bearer` → `***`). When a script must transform file content, read the RAW bytes (open/read in the script itself), not the tool's displayed view.
- **Native module ABI mismatch after npm installs → pm2 crash loop.** Running `npm install` with the WRONG node on PATH (e.g. node22 while pm2 runs system node v18) rebuilds native deps (better-sqlite3) for the wrong ABI → `ERR_DLOPEN_FAILED / NODE_MODULE_VERSION 127…requires 109` → server down. Fix: identify the pm2 interpreter (`pm2 describe <app>`), rebuild with THAT node + `npm_config_python=/usr/bin/python3` (node-gyp broke on the venv python: "No package metadata was found for gyp"). `npm install` of pure-JS packages with `--ignore-scripts` avoids the rebuild entirely.
- **After ANY agent refactor, run `tsc` immediately.** Coding agents frequently leave missing closers (`})`) that surface as `TS1005 ',' expected` at the END of the file (cascading parse errors — the real break is an unclosed brace many lines earlier). A brace-balance scan finds the region; esbuild's transform gives the precise `Expected ')' but found 'function'` line.
- **A pathless-route structure that worked before can be silently broken by an edit that drops a closing `</Route>`** — the register page renders (public) while ALL protected routes go blank. Read the full JSX tree after any route surgery.
- **"Stuck on building / nothing changed"** — verify the LIVE bundle is actually new (hash compare) before re-debugging; CF `cf-cache-status: DYNAMIC` means no CF caching (stale = client cache, not edge).
- **Data-driven theme/style maps crash when a NEW id reaches a render path you forgot to extend.** `GAME_THEMES[normalizeGameId(id)].accent` threw `Cannot read properties of undefined (reading 'accent')` the moment a new game id was SELECTED in the lobby → whole page fell to the error boundary (React Router's `LazyRouteErrorBoundary` catches it — no window error, just "Retry | Leave Room"). When adding any new id (game, theme, route, entity): enumerate EVERY `Record<id, …>` map the id flows through (themes, icons, path builders, stats) and extend them all — a defaulted `normalizeX(id)` hides missing keys until a render path dereferences them.
- **`vite build` / esbuild PASSES with undefined identifiers.** A JSX reference to a never-defined const (e.g. `PALETTE_SWATCH[palette]` where the map was never declared) gives BUILD_EXIT=0 and deploys cleanly — the ReferenceError only fires at RUNTIME, the first time the component actually renders. The component can stay dormant for hours until a state change makes it render (here: the design picker only renders when `designs.length > 1`; adding the 11th design flipped it on → whole lobby crashed → "the game isn't loading at all"). Guard: after any edit that references a new constant/map, (a) grep the source for the identifier — usage without a declaration = bug; (b) exercise the runtime path in a real browser, including the CONDITION that toggles the component on (bump data past the threshold if needed).
- **Same-specificity CSS: the LATER rule in the file wins — absolute positioning can be silently overridden.** `.dn-snake-tile { position: absolute }` declared BEFORE `.dn-tile { position: relative }` in the same stylesheet (both specificity 0,1,0) meant tiles ignored their inline grid `left/top`, flowed inline, and produced huge gaps between dominoes (measured 114px/70px; target ~4px). Zero console errors, layout math correct on paper. Detect: compare the render's computed inline `left/top` against actual `getBoundingClientRect()` — if they diverge per-element (each shifted differently), positioning is being overridden; then check rule ORDER + specificity of every class on the element. Fix: raise specificity (`.board .tile { position: absolute }`), don't reorder blindly.
- **Default-fallback route helpers silently navigate to the WRONG page.** A `gamePathFor(type)` helper returning a hardcoded default (`'uno'`) for unknown types made the client open the UNO page to view a correctly-created dominoes room (`/game/uno/<id>` while the room was dominoes). The server was right; the client's path builder lied. Fix: let unknown ids pass through (`if (type && /^[a-z0-9-]+$/.test(type)) return type`) — never fall back to a real entity's route.
- **Socket-state consumers miss the pre-mount event → stuck on the loading screen forever.** A page consuming socket-pushed state (`game_started`) can mount AFTER the server already emitted it (create-flow race), so it never renders. Two-part fix: (a) the consumer re-emits the join/handshake on mount (`socket.emit('join_room', {roomId})` — server re-pushes state on rejoin); (b) the server's rejoin handler must re-push state for ALL game types — new types need an else-branch in the `if (isXGame) … else` chain or they resync nothing on refresh.

## Verification discipline

- A blank screen with no errors in PROD is expected (prod React shows no overlay) — reproduce in DEV (`npx vite --port 5199 --strictPort`) for the error overlay, but note dev HMR can confuse (module re-fetches look like progress). Prefer instrumenting the prod build directly when the dev behavior is muddy.
- **Programmatic clicks ≠ real touch.** `element.click()` / `locator.click()` dispatch mouse events that succeed even on invisible or zero-opacity elements, so automated tests can pass while a real finger tap does nothing. For mobile UIs, ALWAYS re-verify the interaction with `page.touchscreen.tap(x, y)` at the element's center. This caught the dominoes case: taps worked in mouse-click tests, but the user's "I can't play" was a UX gap (tap-tap requires tile-select FIRST — drop zones only activate after selection — and tapping unplayable tiles was a silent no-op).
- Always end with: full user-flow re-test (register → protected page → action → refresh) + zero console errors + the fixed bundle deployed.

## References
- `references/cardnite-blank-screen-case.md` — full case study: the PublicOnlyRoute infinite-loop, the exact instrumentation sequence that found it, and the import/export E2E debugging (registry append bugs, background-build pipeline).
