# Node / React-SPA Audit Checklist

Applies to Vite/React frontends with a Node (Express/Socket.IO) API behind nginx + Cloudflare.

## SPA fallback false positive — ALWAYS check content, not status code
Any nonexistent path on an SPA returns 200 with index.html. A `.env` → 200 does NOT mean a leak.
```bash
# if .env returns 200, verify it's just the SPA fallback:
curl -s https://DOMAIN/.env | head -c 100          # <!doctype html> = fallback, safe
curl -s https://DOMAIN/ | md5sum                   # compare hashes
curl -s https://DOMAIN/.env | md5sum               # identical = fallback, NOT exposed
```
Real SPA leaks: static assets under /assets served directly, or server-rendered config.

## API discovery
```bash
for p in /api/health /api/auth/login /api/auth/me /api/admin /graphql; do
  curl -s -o /dev/null -w "POST $p -> %{http_code}\n" -X POST "https://DOMAIN$p"
done
```
Sanity: 401/400/404 on protected/unknown routes; stack traces or verbose errors = info leak.

## Login hardening checks
```bash
# user enumeration: identical error for existing vs nonexistent user
curl -s -X POST https://DOMAIN/api/auth/login -H "Content-Type: application/json" -d '{"username":"admin","password":"x"}'
curl -s -X POST https://DOMAIN/api/auth/login -H "Content-Type: application/json" -d '{"username":"definitely-not-a-user","password":"x"}'
# NoSQLi probe (must reject)
curl -s -X POST https://DOMAIN/api/auth/login -H "Content-Type: application/json" -d '{"username":{"$ne":null},"password":{"$ne":null}}'
# rate limiting: fire N+1, find first 429
for i in $(seq 1 30); do code=$(curl -s -o /dev/null -w "%{http_code}" -X POST https://DOMAIN/api/auth/login -H "Content-Type: application/json" -d "{\"username\":\"admin\",\"password\":\"x$i\"}"); [ "$code" = "429" ] && echo "first 429 at attempt $i" && break; done
```

## CORS
```bash
# evil origin must NOT be reflected; allow-credentials without allow-origin whitelist = footgun
curl -s -D - -o /dev/null -X OPTIONS https://DOMAIN/api/auth/login \
  -H "Origin: https://evil.com" -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: content-type,authorization" | grep -i access-control
```
Good: `access-control-allow-origin: https://0.DOMAIN` for legit origin, nothing (or explicit list) for evil.
Fix (express):
```js
app.use(cors({ origin: ['https://app.example.com'], credentials: true }));
```

## Secrets in client JS
```bash
JS=$(curl -s https://DOMAIN/ | grep -oE 'src="[^"]*\.js"' | grep -oE '"/[^"]*"' | tr -d '"' | head -1)
curl -s "https://DOMAIN$JS" | grep -oE "(api[_-]?key|secret|sk-[a-zA-Z0-9]{20,})" | sort -u
```
Benign hits: "token", "password" as variable names. Real hits: `sk-...`, actual key values.

## WebSocket auth (game/chat apps) — the critical one
Use `scripts/ws-auth-test.py` (TLS-correct; raw HTTP tests fail with "plain HTTP to HTTPS port").
- BAD: server upgrades (101) and issues `{"sid":"..."}` with no token → auth gap
- GOOD: 101 then error packet / close without a token
- Also verify room joins validate the user is a game participant, not just the connection.

Fix (Socket.IO):
```js
io.use((socket, next) => {
  const token = socket.handshake.auth && socket.handshake.auth.token;
  if (!token) return next(new Error('Authentication required'));
  try { socket.user = jwt.verify(token, process.env.JWT_SECRET); next(); }
  catch (e) { next(new Error('Invalid token')); }
});
```
Client: `io({ auth: { token: localStorage.getItem('token') } })` — match the app's real storage key.

## Rate-limit fix (express)
```js
const rateLimit = require('express-rate-limit');
const loginLimiter = rateLimit({ windowMs: 15*60*1000, max: 20, standardHeaders: true, message: { error: 'Too many login attempts. Try again later.' } });
app.post('/api/auth/login', loginLimiter, handler);
```

## Cloudflare for APIs — NEVER Managed Challenge on fetch endpoints
Managed Challenge blocks the app's own XHR → breaks login for real users. Use rate-limit rules:
`(http.host eq "DOMAIN" and starts_with(uri.path, "/api/auth/login"))` → Block, 20 req/10s.
Managed Challenge is fine on page routes (the SPA HTML itself).
