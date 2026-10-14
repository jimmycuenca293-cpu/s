#!/usr/bin/env python3
"""Genera public/index.html (TecniGuía Pro) a partir de la app de Claude.

La app original vive en ../app-diagnostico/index.html y se sigue usando como
artifact. Este script la envuelve en un documento HTML completo, le agrega la
pantalla de cuenta (src/auth.html) y el puente con el servidor (src/shim.js),
y cambia los textos que hablan de Claude por textos del producto propio.

Uso:  python3 build.py
"""
import pathlib
import sys

AQUI = pathlib.Path(__file__).resolve().parent
ORIGEN = AQUI.parent / "app-diagnostico" / "index.html"
DESTINO = AQUI / "public" / "index.html"

app = ORIGEN.read_text(encoding="utf-8")
auth = (AQUI / "src" / "auth.html").read_text(encoding="utf-8")
shim = (AQUI / "src" / "shim.js").read_text(encoding="utf-8")


def cambiar(texto, viejo, nuevo, obligatorio=True):
    n = texto.count(viejo)
    if n == 0:
        if obligatorio:
            sys.exit(f"No encontré en la app: {viejo[:70]!r}")
        return texto
    return texto.replace(viejo, nuevo)


# Quitar la meta charset suelta de la app (va en el <head>)
app = cambiar(app, '<meta charset="utf-8">\n', "", obligatorio=False)

# Textos del producto propio
app = cambiar(app, "Guardado en tu cuenta de Claude: lo ves en el celular y en el computador.",
              "Guardado en tu cuenta: lo ves en el celular y en el computador.")
app = cambiar(app, "`Guardado en tu cuenta de Claude · ${VISITS.length} visita(s).`",
              "`Guardado en tu cuenta · ${VISITS.length} visita(s).`")
app = cambiar(app, "La visita guiada funciona cuando abres esta app dentro de Claude.",
              "La visita guiada necesita conexión a internet.")
app = cambiar(app, "la app tiene que estar abierta dentro de Claude", "necesitas conexión a internet")

# Barra del técnico (nombre, plan, salir) en el encabezado
app = cambiar(app, '<p>Diagnóstico de neveras, nevecones, lavadoras y secadoras</p>\n    </div>',
              '<p>Diagnóstico de neveras, nevecones, lavadoras y secadoras</p>\n'
              '      <div class="tg-bar" id="tg-userbar" hidden></div>\n    </div>')

# Términos en el pie
app = cambiar(app, "(secadoras eléctricas a 220 V).</footer>",
              '(secadoras eléctricas a 220 V). <a href="terminos.html">Términos de uso</a>.</footer>')

# Pantalla de cuenta antes del menú, y el puente antes del script de la app
app = cambiar(app, '<header class="top">', auth + '\n<header class="top">')
inicio_app = '<script>\n(() => {\n"use strict";'
app = cambiar(app, inicio_app, "<script>\n" + shim + "\n</script>\n" + inicio_app)

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
DESTINO.write_text(html, encoding="utf-8")
print(f"Listo: {DESTINO.relative_to(AQUI)} ({len(html) // 1024} KB)")
