# CardNite QA Reference (up.zaxbot.xyz)

React+Vite frontend, Node+Express+Socket.io+SQLite backend (PM2 port 3001, Apache proxy). Production at up.zaxbot.xyz. All gameplay screenshots for QA go to `/cursor-noise/screenshots/cardnite-gameplay/`.

## Test Account

- **Username:** HermesQA
- **Email:** hermesqa@zaxbot.xyz
- **Password:** QApass2026!
- User id 11, 200 coins. Created 2026-07-31 via API (the register form UI silently fails to submit — use API + token injection instead).

## Auth Facts

- Login authenticates by **username, not email** (email returns `{"error": ...}`).
- Auth storage key: `localStorage.token` (bundle also uses `cardnite-theme` for dark mode).
- API endpoints: `POST /api/auth/register` (fields: username, email, password, confirmPassword), `POST /api/auth/login` (username, password).
- On login the app also stores a `user` JSON object in localStorage.

## Route Map (from bundle)

```
/  /login  /register  /forgot-password  /reset-password/:token
/join/:roomId  /about  /contact  /privacy  /terms
/dashboard  /lobby  /profile  /shop  /friends  /leaderboard  /admin
/game/uno/:roomId  /game/chess/:roomId  /game/domino/:roomId
/game/skru/:roomId  /game/desert-traders/:roomId
```

- `/games` redirects to `/`; use `/lobby` instead.
- Game routes need a roomId: from `/lobby`, click the game's "Live" button, then **Solo Play** → instantly spawns a room vs bots (e.g. `game/chess/FE40A3EA`).

## Games & Gameplay Notes

| Game | Solo vs | Notable UI |
|------|---------|------------|
| UNO | 3 bots (Alpha/Beta/Gamma) | Draw pile, Sort Hand, Call UNO, color picker |
| Chess | Bot Alpha (rating ~1463) | Blitz 5+3, Take Back, Hint, Analysis Board, spectate |
| Domino | 3 bots | tiles + board |
| SKRU | bots | card table |
| Desert Traders | 2 bots | Auction phase (bids, herd values, animal cards) |

- Chess (3D board) makes `browser_snapshot` time out — verify via `location.href` + console DOM checks instead; `browser_vision` still captures the screenshot.
- Lobby shows fake-ish "Players Online" counters (2.5k+) — cosmetic, not real traffic signal.
- "Watch Ad" button exists in lobby (reward path).

## Screenshot Deliverables (2026-07-31 session)

Captured live vs bots: `uno.png`, `chess.png`, `domino.png`, `skru.png`, `desert-traders.png` under `/cursor-noise/screenshots/cardnite-gameplay/`.
