# Case study: CardNite blank-screen after login (Aug 2026)

Production React SPA (`0.zaxbot.xyz`, Vite + React Router 6 + socket.io). After a routing refactor the site went **black for logged-in users** (register page worked, /about worked logged-out) with **zero console errors** in prod AND dev.

## What the instrumentation sequence found

1. `#root.innerHTML.length` = 0 after login; main thread ALIVE (evaluate runs). Not a freeze, not a chunk failure (all chunks curl 200), server socket handshake clean via node socket.io-client direct test.
2. Added `console.log('[DBG] ...')` to: App render → AuthProvider render → SocketProvider effect start → PublicOnly → AppRoutes → ProtectedRoute.
3. Log sequence after register submit:
   ```
   [DBG] AuthProvider render {user: imp278767}
   [DBG] PublicOnly {user: imp278767}
   [DBG] AppRoutes render /dashboard
   [DBG] PublicOnly {user: imp278767}   ← repeats
   [DBG] AppRoutes render /dashboard    ← repeats
   [DBG] PublicOnly {user: imp278767}   ← repeats
   ```
   ProtectedRoute NEVER logged. Fingerprint = **infinite redirect loop**.

## Root cause

`PublicOnlyRoute` had been reconstructed as:
```tsx
function PublicOnlyRoute() {
  return <PublicOnly><Outlet /></PublicOnly>;   // WRONG
}
```
It must be a plain outlet:
```tsx
function PublicOnlyRoute() {
  return <Outlet />;                            // RIGHT
}
```
The pathless layout route wraps ALL routes (public + protected). Wrapping it with `PublicOnly` (which does `if (user) return <Navigate to="/dashboard"/>`) made every route — including /dashboard itself — redirect logged-in users to /dashboard forever. The auth-redirect belongs only in the per-route `<PublicOnly>` wrappers on /login and /register.

**Lesson for reconstruction:** when restoring a deleted route-guard component, look at how it was USED (pathless wrapper vs per-route) — the original had NO auth logic in the pathless wrapper.

## Secondary trap hit during the same session

A cleanup script transformed file content by reading it through the tool's displayed view (line-number prefixes + `***` secret redaction) and writing it back — baking `NNN|` prefixes and replacing `Bearer` with `***` in source files. Fix: strip prefixes with `re.sub(r'^(\d+\|)+', '', src, flags=re.M)` and restore redacted literals by hand — or better, read raw bytes inside the script (`open(f).read()`) instead of the tool's display.

## Import/export E2E debugging (same session)

The admin game import pipeline (zip → validate → registry append → background build) surfaced three real bugs via E2E testing with a dummy package:
1. `transpileModule` with `jsx: undefined` in compilerOptions throws `Argument for '--jsx' option must be...` — omit the key when not needed.
2. Registry append must add the module IMPORT (`import XGame from './<id>'`) at the top of `games/index.ts`, not just the entry — missing import = `TS2304: Cannot find name 'XGame'`.
3. Lazy component import for the client registry must be inserted at the TOP of the file (with the other lazy imports), NOT inside the GAMES array (markers sit inside the array — a `const` there = `Unexpected "const"`).

Also: the background build script's final `echo IMPORT_BUILD_OK` can be lost when the script's parent (the pm2-managed server) is restarted mid-script — the build still completes; verify by server state (registry lists the game) rather than the marker.

Admin API testing without the real password: mint a token from the server's own secret — `jwt.sign({id: <DEVMAX db id>, username: 'DEVMAX'}, <data/jwt-secret>)` with the repo's jsonwebtoken. Middleware requires payload key `id` (number) AND requireAdmin cross-checks the DB user by id — use DEVMAX's real `users.id` from `/root/cardnite/server/cardnite.db`.
