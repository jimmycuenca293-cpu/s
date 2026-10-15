#!/bin/sh
# Genera filtroya-web.zip para subir a Hostinger (sin config.php ni pedidos).
set -e
cd "$(dirname "$0")"
python3 build.py
rm -f filtroya-web.zip
cd public_html
zip -qr ../filtroya-web.zip . -x 'api/config.php' -x 'data/pedidos.sqlite*' -x 'data/correos.log'
cd ..
zip -qj filtroya-web.zip INSTALAR.md
echo "Listo: filtroya-web.zip ($(du -h filtroya-web.zip | cut -f1))"
