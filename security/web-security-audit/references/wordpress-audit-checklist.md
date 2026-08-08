# WordPress Audit Checklist (verified against a real cPanel→nginx migration target)

Run each check, record the code. Expected values in parentheses.

## Checks
```bash
# version disclosure
curl -s https://DOMAIN/ | grep -oE 'generator" content="WordPress [0-9.]+'
# xmlrpc (must be 403; 405 with method list = enabled = vuln)
curl -s -o /dev/null -w "%{http_code}\n" https://DOMAIN/xmlrpc.php
# user enumeration
curl -s -o /dev/null -w "%{http_code}\n" "https://DOMAIN/wp-json/wp/v2/users"          # want 403
curl -s -o /dev/null -w "%{http_code} -> %{redirect_url}\n" "https://DOMAIN/?author=1" # want 301 (NOT 200)
curl -s -o /dev/null -w "%{http_code}\n" "https://DOMAIN/author/USERNAME/"             # want 301/404
# exposed files (want 403/404)
for f in wp-config.php.bak .git/config .env debug.log wp-content/debug.log readme.html license.txt; do
  curl -s -o /dev/null -w "$f -> %{http_code}\n" "https://DOMAIN/$f"
done
# plugin version disclosure (want 403)
curl -s -o /dev/null -w "%{http_code}\n" https://DOMAIN/wp-content/plugins/akismet/readme.txt
# brute force (login with wrong creds x6 — expect lockout/challenge on 6th)
for i in 1 2 3 4 5 6; do curl -s -o /dev/null -w "%{http_code}\n" -X POST https://DOMAIN/wp-login.php -d "log=admin&pwd=wrong$i"; done
# security headers (want >=2 of x-frame/strict-transport/x-content)
curl -sI https://DOMAIN/ | grep -icE "x-frame|strict-transport|x-content"
```

## Fixes (nginx — add to the site's server block, reload with `nginx -t && systemctl reload nginx`)
```nginx
# xmlrpc off
location = /xmlrpc.php { return 403; }
# user enumeration off (REST)
location ~ ^/wp-json/wp/v2/users { return 403; }
location ~ ^/wp-json/wp/v2/users/ { return 403; }
# plugin/theme txt disclosure off
location ~* ^/wp-content/(plugins|themes)/.*\.(txt|md|html)$ { return 403; }
# version files off
location ~* ^/(readme\.html|license\.txt|wp-config\.php\.(save|bak|old)|\.env|\.git) { return 403; }
# security headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;  # only after HTTPS confirmed
```

## Author-archive redirect (functions.php — REST block alone does NOT stop ?author=N)
```php
add_action('template_redirect', function () {
    if (is_author()) { wp_safe_redirect(home_url('/'), 301); exit; }
});
```
Find active theme: `wp option get template --allow-root` (cPanel boxes: use the raw wp-cli phar, the packaged `wp` is a wrapper that fails with "Only CLI access").

## Old-server URL leak
`wp-json/wp/v2/users` shows `"url":"http://OLD-IP/..."` in user profiles → clear:
`wp user meta update <id> url ""`

## Cloudflare rules (dashboard)
- `Protect wp-login`: `(http.host eq "DOMAIN" and starts_with(uri.path, "/wp-login"))` → Managed Challenge
- `Protect wp-admin`: same for `/wp-admin` → Managed Challenge
- optional rate limit: 20 req/10s → block 15 min
