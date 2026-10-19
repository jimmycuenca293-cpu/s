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
  rm -f "tienda-$m.zip"
  (cd "sitios/$m" && zip -qr "../../tienda-$m.zip" . -x 'api/config.php' -x 'data/pedidos.sqlite*' -x 'data/correos.log')
  # en los sitios de marca las carpetas no llevan el prefijo purofiltro-
  sed -e 's/purofiltro-//g' -e 's/Filtros Nevecones Colombia/Tu tienda/g' INSTALAR.md > "sitios/INSTALAR.md" && zip -qj "tienda-$m.zip" "sitios/INSTALAR.md"
  echo "Listo: tienda-$m.zip ($(du -h "tienda-$m.zip" | cut -f1))"
done
