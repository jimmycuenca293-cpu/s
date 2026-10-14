#!/usr/bin/env bash
# Genera tecniguia-pro.zip listo para subir a Hostinger.
set -euo pipefail
cd "$(dirname "$0")"
python3 build.py
( cd public/api && composer install --no-dev --optimize-autoloader --no-interaction --quiet )
rm -f tecniguia-pro.zip
cp schema.sql INSTALAR.md public/
( cd public && zip -qr ../tecniguia-pro.zip . -x 'api/config.php' 'api/vendor/*/.git/*' 'api/vendor/*/*/.git/*' 'api/vendor/*/*/.github/*' 'api/vendor/*/*/tests/*' 'api/vendor/*/*/examples/*' 'api/vendor/*/*/fixtures/*' 'api/vendor/*/*/scripts/*' )
rm public/schema.sql public/INSTALAR.md
echo "Listo: tecniguia-pro.zip ($(du -h tecniguia-pro.zip | cut -f1))"
