# -*- coding: utf-8 -*-
"""Genera .htaccess con redirecciones 301 de las URLs viejas a las nuevas. Uso: python3 cst_redirects.py <sitio_nuevo>"""
import sys, os, re, pathlib
from cst_datos import M, EQ, BRANDS_ORDER
R = pathlib.Path(sys.argv[1])
def pb(m, s): return f"/samsung/{s}/" if m == "samsung" else f"/{m}/{s}/"
def hub(m): return "/" if m == "samsung" else f"/{m}/"
L = ["# Panamá: servidor Apache/LiteSpeed (Hostinger)", "RewriteEngine On",
     "RewriteCond %{HTTPS} off", "RewriteRule ^ https://centrodeserviciotecnicopanama.com%{REQUEST_URI} [L,R=301]",
     "RewriteCond %{HTTP_HOST} ^www\\. [NC]", "RewriteRule ^ https://centrodeserviciotecnicopanama.com%{REQUEST_URI} [L,R=301]", "",
     "# Páginas nuevas existentes: no redirigir", "RewriteCond %{REQUEST_FILENAME} -f [OR]", "RewriteCond %{REQUEST_FILENAME} -d", "RewriteRule ^ - [L]", "",
     "RewriteRule ^index\\.html$ / [R=301,L]", "RewriteRule ^samsung/?$ / [R=301,L]", "RewriteRule ^samsung/index\\.html$ / [R=301,L]", ""]
EQRX = [("neveras", r"nevera|refriger"), ("lavadoras", r"lavadora"), ("secadoras", r"secadora"), ("aires", r"aire"), ("cocinas", r"cocina|estufa|horno"), ("lavavajillas", r"lavavajillas"), ("centro-lavado", r"centro-?s?-de-lavado|torre"), ("batidoras", r"batidora"), ("microondas", r"microondas")]
n = 0
for m in BRANDS_ORDER:
    d = M[m]; L.append(f"# {d['nombre']}")
    for e, rx in EQRX:
        if e in d["equipos"]: tgt = pb(m, "reparacion-" + EQ[e][0])
        elif e == "centro-lavado" and "lavadoras" in d["equipos"]: tgt = pb(m, "reparacion-lavadoras")
        else: continue
        L.append(f"RewriteRule ^{m}/(?!blog)[^/]*(?:{rx})[^/]*\\.html$ {tgt} [R=301,L]"); n += 1
    L.append(f"RewriteRule ^{m}/(?:costo|garantia|repuestos|reparar|precio)[^/]*\\.html$ {pb(m, 'cuanto-cuesta-la-reparacion')} [R=301,L]")
    L.append(f"RewriteRule ^{m}/preguntas[^/]*\\.html$ {pb(m, 'preguntas-frecuentes')} [R=301,L]")
    if d["codigos"]: L.append(f"RewriteRule ^{m}/[^/]*(?:codigo|error)[^/]*\\.html$ {pb(m, 'codigos-de-error')} [R=301,L]")
    L.append(f"RewriteRule ^{m}/.*$ {hub(m)} [R=301,L]")
    L.append("")
# páginas sin marca (equipo x barrio, guías, etc.) -> portada Samsung (la principal)
L.append("# Páginas generales viejas")
L.append("RewriteRule ^[^/]+\\.html$ / [R=301,L]")
L += ["", "ErrorDocument 404 /404.html", "Options -Indexes", "<IfModule mod_expires.c>", "ExpiresActive On", "ExpiresByType image/webp \"access plus 1 year\"", "ExpiresByType text/css \"access plus 1 month\"", "</IfModule>"]
(R / ".htaccess").write_text("\n".join(L) + "\n"); os.chmod(R / ".htaccess", 0o644)
print(len(L), "líneas")
