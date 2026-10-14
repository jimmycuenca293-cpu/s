#!/usr/bin/env python3
"""Genera simple/index.html: la TecniGuía personal sin cuenta ni base de datos.

Toma la app de Claude (../app-diagnostico/index.html), la envuelve en un
documento HTML completo y le pone el puente src/shim-simple.js, que usa
api/ia.php con la clave del técnico. Sin clave, la app abre igual sin IA.

Uso:  python3 build_simple.py
"""
import pathlib
import sys

AQUI = pathlib.Path(__file__).resolve().parent
app = (AQUI.parent / "app-diagnostico" / "index.html").read_text(encoding="utf-8")
shim = (AQUI / "src" / "shim-simple.js").read_text(encoding="utf-8")


def cambiar(texto, viejo, nuevo):
    if viejo not in texto:
        sys.exit(f"No encontré en la app: {viejo[:70]!r}")
    return texto.replace(viejo, nuevo)


app = app.replace('<meta charset="utf-8">\n', "", 1)
app = cambiar(app, "La visita guiada funciona cuando abres esta app dentro de Claude.",
              "Para activar el diagnóstico con IA, pega tu clave de Claude en el archivo <b>api/clave.php</b> de tu Hostinger.")
app = cambiar(app, "la app tiene que estar abierta dentro de Claude", "falta tu clave de la IA en api/clave.php")
app = cambiar(app, '<script>\n(() => {\n"use strict";', "<script>\n" + shim + '\n</script>\n<script>\n(() => {\n"use strict";')

html = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#0b6e8a">
<style>
:root{{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}
body{{margin:0;font:14px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}}
img{{max-width:100%}}
[hidden]{{display:none!important}}
</style>
</head>
<body>
{app}
</body>
</html>
"""
destino = AQUI / "simple" / "index.html"
destino.write_text(html, encoding="utf-8")
print(f"Listo: {destino.relative_to(AQUI)} ({len(html) // 1024} KB)")
