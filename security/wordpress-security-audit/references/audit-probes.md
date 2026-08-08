# WordPress Security Audit — Copy-Paste Probe Sequence

Run against an authorized target. Replace DOMAIN with the target.

## Recon
```bash
getent ahostsv4 DOMAIN | head -2                 # DNS, detect Cloudflare (104.21.x / 172.67.x = CF)
curl -s https://DOMAIN/cdn-cgi/trace | grep -E "ip=|colo="   # real origin IP behind CF
curl -sI https://DOMAIN/ | head -15              # headers + server fingerprint
curl -sI http://ORIGIN_IP/ -H "Host: DOMAIN" | head -8   # probe origin directly
```

## Probes
```bash
# 1. WP version
curl -s https://DOMAIN/ | grep -oE 'generator" content="WordPress [0-9.]+' | head -1

# 2. User enumeration
curl -s -o /dev/null -w "author=1: %{http_code}\n" "https://DOMAIN/?author=1"
curl -s "https://DOMAIN/wp-json/wp/v2/users?per_page=5" | head -c 400

# 3. XML-RPC
curl -s -X POST https://DOMAIN/xmlrpc.php -H "Content-Type: text/xml" \
  -d '<?xml version="1.0"?><methodCall><methodName>system.listMethods</methodName><params></params></methodCall>' | head -c 200
# system.multicall present = brute-force amplifier

# 4. Brute-force lockout check
for i in 1 2 3; do curl -s -o /dev/null -w "try $i: %{http_code}\n" -X POST https://DOMAIN/wp-login.php -d "log=admin&pwd=wrong$i"; done

# 5. Exposed files
for f in wp-config.php.bak .git/config .env debug.log wp-content/debug.log xmlrpc.php readme.html license.txt; do
  code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "https://DOMAIN/$f"); echo "$f -> $code"; done

# 6. Plugin disclosure
for p in elementor woocommerce akismet contact-form-7; do
  code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "https://DOMAIN/wp-content/plugins/$p/readme.txt"); echo "$p/readme.txt -> $code"; done

# 7. Directory listing
for d in wp-content/uploads wp-content/plugins wp-includes; do
  code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "https://DOMAIN/$d/"); echo "$d/ -> $code"; done

# 8. Security headers
curl -sI https://DOMAIN/ | grep -iE "x-frame|x-content|x-xss|strict-transport|content-security" || echo "NONE present"
```

## Interpretation cheat-sheet
| Finding | Risk | Fix |
|---|---|---|
| `/wp-json/wp/v2/users` returns JSON | HIGH — admin username leak | nginx deny, or disable REST user routes |
| `system.multicall` in xmlrpc | HIGH — amplified brute force | deny xmlrpc.php |
| No lockout on wp-login | HIGH — unbounded guessing | Cloudflare WAF rule / fail2ban |
| `readme.txt` → 200 | MED — plugin CVE targeting | deny readme/license files |
| No security headers | MED — clickjacking | add_header block |
| user.url shows old IP | LOW — infra leak | clean user profiles after migration |

## Live example (zaxbot.xyz audit, 2026-08)
Found: user enum leaked `devmax`, xmlrpc enabled, no brute-force protection, akismet readme.txt 200, zero security headers, readme.html/license.txt exposed. Clean: no .env/.git/backups/debug.log, listing mostly blocked, HTTPS+CF working.
