#!/usr/bin/env bash
# Genera tecniguia-personal.zip: la TecniGuía de un solo técnico para subir a Hostinger.
set -euo pipefail
cd "$(dirname "$0")"
python3 build.py
( cd public/api && composer install --no-dev --optimize-autoloader --no-interaction --quiet )
echo "Require all denied" > public/api/vendor/.htaccess
TMP=$(mktemp -d)
cp -r public/. "$TMP/"
rm -f "$TMP/admin.html" "$TMP/api/admin.php" "$TMP/api/config.php"
cp config.personal.sample.php "$TMP/api/config.sample.php"
cp schema.sql "$TMP/"
cp INSTALAR-PERSONAL.md "$TMP/INSTALAR.md"
rm -f tecniguia-personal.zip
( cd "$TMP" && zip -qr "$OLDPWD/tecniguia-personal.zip" . -x 'api/vendor/*/.git/*' 'api/vendor/*/*/.git/*' 'api/vendor/*/*/.github/*' 'api/vendor/*/*/tests/*' 'api/vendor/*/*/examples/*' 'api/vendor/*/*/fixtures/*' 'api/vendor/*/*/scripts/*' )
rm -rf "$TMP"
echo "Listo: tecniguia-personal.zip ($(du -h tecniguia-personal.zip | cut -f1))"
