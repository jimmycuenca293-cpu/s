#!/usr/bin/env bash
# Genera tecniguia.zip: TecniGuía personal sin cuenta ni base de datos.
set -euo pipefail
cd "$(dirname "$0")"
python3 build_simple.py
( cd public/api && composer install --no-dev --optimize-autoloader --no-interaction --quiet )
TMP=$(mktemp -d)
cp -r simple/. "$TMP/"
cp -r public/api/vendor "$TMP/api/vendor"
echo "Require all denied" > "$TMP/api/vendor/.htaccess"
cp LEEME-SIMPLE.txt "$TMP/LEEME.txt"
rm -f tecniguia.zip
( cd "$TMP" && zip -qr "$OLDPWD/tecniguia.zip" . -x 'api/vendor/*/.git/*' 'api/vendor/*/*/.git/*' 'api/vendor/*/*/.github/*' 'api/vendor/*/*/tests/*' 'api/vendor/*/*/examples/*' 'api/vendor/*/*/fixtures/*' 'api/vendor/*/*/scripts/*' )
rm -rf "$TMP"
echo "Listo: tecniguia.zip ($(du -h tecniguia.zip | cut -f1))"
