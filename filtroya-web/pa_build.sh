#!/bin/bash
# Construye el sitio de Panamá completo. Uso: bash pa_build.sh <salida> [carpeta_img_mejoradas]
set -e
OUT=$1; IMGS=$2
cd "$(dirname "$0")"
set -a; [ -f /tmp/tienda.env ] && . /tmp/tienda.env; set +a
rm -rf "$OUT"
ST_SOLO=panama python3 st_samsung.py "$OUT" https://samsungpanamaserviciotecnico.com "JO5tODRL0axh4F-CgMYNcGb5z2ub2dK3tXSHP8p-1zg"
python3 st_cali_mejoras.py "$OUT"
if [ -n "$IMGS" ] && [ -d "$IMGS" ]; then cp -f "$IMGS"/*.webp "$OUT/img/"; fi
python3 pa_diseno.py "$OUT"
