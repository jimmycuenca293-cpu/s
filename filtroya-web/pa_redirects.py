#!/usr/bin/env python3
"""Genera las redirecciones 301 de las páginas viejas de samsungpanamaserviciotecnico.com a las nuevas.
Uso: python3 pa_redirects.py <sitio_nuevo> <carpeta_con_las_paginas_viejas> <salida.txt>"""
import pathlib, re, sys
NEW, OLD, OUT = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3])
ex = lambda p: (NEW / p.strip("/") / "index.html").exists()
HOST = "https://www.samsungpanamaserviciotecnico.com"
def eq(n):
    for k, v in (("side-by-side", "refrigeradoras"), ("refrigerador", "refrigeradoras"), ("family-hub", "refrigeradoras"), ("lavadora", "lavadoras"), ("centro-lavado", "lavadoras"), ("secadora", "secadoras")):
        if k in n: return v
    return None
CAMBIOS = {"cambio-compresor-refrigeradora": "cambio-de-compresor-refrigeradora", "cambio-bomba-drenaje-lavadora": "cambio-de-bomba-de-desague-lavadora", "cambio-resistencia-secadora": "cambio-de-resistencia-secadora",
           "cambio-valvula-agua-refrigeradora": "refrigeradoras", "cambio-motor-lavadora": "lavadoras", "reparacion-tarjeta-electronica": "cambio-de-tarjeta-electronica-refrigeradora"}
EXTRA = {"bespoke-samsung-panama": "bespoke-samsung", "family-hub-samsung-panama": "family-hub-samsung", "ecobubble-samsung-panama": "ecobubble-samsung", "garantia-samsung-panama": "preguntas-frecuentes", "blog-cuidados-samsung-panama": "blog",
         "telefono-servicio-tecnico-samsung-panama": "telefono", "telefono-servicio-cliente-samsung-panama": "telefono", "servicio-urgente-samsung-panama": "falla-urgente-refrigeradoras", "tecnico-samsung-panama": "", "centro-autorizado-samsung-panama": "",
         "centro-de-servicio-samsung-panama": "", "samsung-service-center-panama": "", "reparaciones-samsung-panama": "", "reparacion-electrodomesticos-samsung-panama": "", "precio-servicio-tecnico-samsung-panama": "", "instalaciones-samsung-panama": "", "mantenimientos-samsung-panama": "",
         "servicio-tecnico-samsung-cerca-de-mi-panama": "cerca-de-mi-refrigeradoras", "servicio-tecnico-samsung-empresas-panama": "", "servicio-tecnico-samsung-airbnb-panama": "", "servicio-tecnico-samsung-panama-viejo-panama": ""}
main, sinpar = [], []
for f in sorted(OLD.glob("*.html")):
    n = f.stem
    if n == "index": continue
    dest = None
    if n in EXTRA: dest = EXTRA[n]
    else:
        base = re.sub(r"-samsung-panama$|-panama$", "", n)
        m = re.match(r"servicio-tecnico-samsung-(.+)-panama$", n)
        if m and ex(m.group(1)): dest = m.group(1)
        elif base in CAMBIOS: dest = CAMBIOS[base]
        elif "aire" in n: dest = None
        elif "windfree" in n: dest = None
        elif re.match(r"codigos-error-", n): dest = "guias"
        elif eq(n): dest = eq(n)
        elif re.search(r"no-centrifuga", n): dest = "lavadoras"
        elif re.search(r"no-drena", n): dest = "lavadoras"
        elif re.search(r"no-calienta", n): dest = "secadoras"
        elif re.search(r"no-enfria", n): dest = "refrigeradoras"
    if dest is None:
        sinpar.append(n); continue
    if dest and not ex(dest): dest = ""
    main.append((n, dest))
lineas = ["# Redirecciones 301: páginas viejas -> páginas nuevas (pega DESPUÉS de las líneas de HTACCESS-pegar-arriba.txt)", "RewriteEngine On"]
for n, d in main:
    lineas.append(f"RewriteRule ^{re.escape(n)}\\.html$ {HOST}/{d + '/' if d else ''} [R=301,L]")
lineas += ["", "# --- OPCIONAL: páginas sin equivalente en el sitio nuevo (aires acondicionados y WindFree). Si no las redireccionas, siguen funcionando con su texto actual. ---"]
for n in sinpar:
    lineas.append(f"# RewriteRule ^{re.escape(n)}\\.html$ {HOST}/ [R=301,L]")
OUT.write_text("\n".join(lineas) + "\n", encoding="utf-8")
print(len(main), "redirecciones;", len(sinpar), "páginas sin equivalente")
