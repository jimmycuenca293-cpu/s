#!/bin/sh
# Genera purofiltro-tienda.zip para subir a Hostinger (sin config.php ni pedidos).
set -e
cd "$(dirname "$0")"
python3 build.py
rm -f purofiltro-tienda.zip
cd public_html
zip -qr ../purofiltro-tienda.zip . -x 'purofiltro-api/config.php' -x 'purofiltro-data/pedidos.sqlite*' -x 'purofiltro-data/correos.log'
cd ..
zip -qj purofiltro-tienda.zip INSTALAR.md
echo "Listo: purofiltro-tienda.zip ($(du -h purofiltro-tienda.zip | cut -f1))"
# Un zip por marca, para subir cada uno a su propio dominio
for m in samsung lg whirlpool ge; do
  rm -f "purofiltro-$m.zip"
  (cd "sitios/$m" && zip -qr "../../purofiltro-$m.zip" . -x 'purofiltro-api/config.php' -x 'purofiltro-data/pedidos.sqlite*' -x 'purofiltro-data/correos.log')
  zip -qj "purofiltro-$m.zip" INSTALAR.md
  echo "Listo: purofiltro-$m.zip ($(du -h "purofiltro-$m.zip" | cut -f1))"
done
