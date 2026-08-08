# SPA/Angular UI Bug Patterns (from real audits)

Reusable checks for finding user-facing breakage in Angular/React SPAs (eduAgent demo audit, 2026-08).

## Dead buttons — prove it, don't assume
A button that "does nothing" may still be triggering something invisible. Prove deadness:
```js
window.__fileInput = null;
const oi = HTMLInputElement.prototype.click;
HTMLInputElement.prototype.click = function() { window.__fileInput = this; return oi.call(this); };
// click the Import/Upload button, then check window.__fileInput
// null -> button is DEAD (never opens the file picker)
```
Also check after clicking: `.swal2-container` (toast), visible `.modal/.cdk-overlay-pane`, console errors. All absent + no file input = genuinely dead feature. (Found: "Import from Excel" on teachers page — hidden `.xlsx,.xls` input exists but never triggered.)

## Raw server errors in localized UIs
- Arabic UI showing English "An error occurred while saving the entity changes..." = backend 500 surfaced raw. Two bugs: (a) missing client-side required-field validation, (b) no friendly error mapping.
- "Http failure response for ... 500 OK" popup = Angular HttpErrorResponse rendered verbatim — UX bug + endpoint-path info leak.

## Silently disabled submit buttons
Invalid input → button disabled with ZERO message while form class reports `ng-valid` (inconsistent state). Check: after typing invalid input, is submit `disabled`? Any `mat-error/.text-danger` text? Disabled + no message = bug.

## Broken template rendering
- Literal `|` / `( )` in table headers ("f | ( fail)", "( | 0 | )") = template interpolation bug (missing binding/pipe).
- Truncated strings mid-word ("تقرير الطلاب ب ل") = string-split or translation-key bug.

## i18n half-translation
Switch language (Ar/En button), grab `document.body.innerText`, scan for Arabic script inside English mode = incomplete translation keys.

## Console error mining (every page)
- `UserNotifications` 401 while logged in = notification auth mismatch (security smell).
- `Upload/getUploadedFile` 404 = broken/renamed endpoint still firing.
- `TypeError: Cannot read properties of null (reading 'value'/'_rawValidators')` = Angular form/component crash.
- **Token in WebSocket URL**: `wss://.../hubs/notifications?id=...&access_token=<FULL TOKEN>` — tokens in query strings leak via proxy logs/referrers. Session-hijack risk; flag it.

## Session-drop handling
SPA sessions drop on full `browser_navigate` reloads. Prefer in-page hash navigation:
```js
location.hash = '#/admin/coursesSys/teachers';  // instead of browser_navigate
```
After hash nav, wait ~4s then read `document.body.innerText`. If login form appears, re-login via snapshot refs.

## Report balanced findings
List what PASSED (search, pagination, view toggles, form save with all fields) alongside failures — proves real testing, lands better.

## Angular form filling (testing save flows)
Fields identified by `formcontrolname` (no placeholders). Set value + dispatch input/change:
```js
const el = document.querySelector('[formcontrolname="name"]');
Object.getOwnPropertyDescriptor(Object.getPrototypeOf(el), 'value').set.call(el, 'value');
el.dispatchEvent(new Event('input', {bubbles:true}));
```
mat-selects: click the select, wait ~1s, click a `.mat-mdc-option` by text. Save buttons may be "حفظ وإرسال الطلب", not "Save".
