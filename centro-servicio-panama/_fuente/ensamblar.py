# -*- coding: utf-8 -*-
"""Ensambla centrodeserviciopanama.com: Samsung en la raíz, LG en /lg/, Whirlpool en /whirlpool/, Mabe en /mabe/ Frigidaire en /frigidaire/ Electrolux en /electrolux/ y General Electric en /general-electric/ (una sola URL).
Uso: ejecutar generar.py en servicio-tecnico-samsung-panama/_fuente y servicio-tecnico-lg-panama/_fuente, luego:  python3 ensamblar.py"""
import shutil, zipfile, datetime
from pathlib import Path
AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
S = RAIZ.parent / "servicio-tecnico-samsung-panama"
L = RAIZ.parent / "servicio-tecnico-lg-panama"
W = RAIZ.parent / "servicio-tecnico-whirlpool-panama"
MB = RAIZ.parent / "servicio-tecnico-mabe-centro"
FR = RAIZ.parent / "servicio-tecnico-frigidaire-panama"
EL = RAIZ.parent / "servicio-tecnico-electrolux-panama"
GE = RAIZ.parent / "servicio-tecnico-general-electric-panama"
DOM = "https://centrodeserviciopanama.com"
HOY = datetime.date.today().isoformat()
SKIP = {"_fuente", "README.md", "__pycache__"}

def limpiar():
    for p in RAIZ.iterdir():
        if p.name in ("_fuente", "README.md"): continue
        shutil.rmtree(p) if p.is_dir() else p.unlink()

def copiar(origen, destino, excluir=()):
    for p in origen.rglob("*"):
        rel = p.relative_to(origen)
        if rel.parts[0] in SKIP or rel.as_posix() in excluir or not p.is_file(): continue
        d = destino / rel
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, d)

limpiar()
copiar(S, RAIZ, excluir=("sitemap.xml",))
copiar(L, RAIZ / "lg", excluir=("robots.txt", "sitemap.xml"))
copiar(W, RAIZ / "whirlpool", excluir=("robots.txt", "sitemap.xml"))
copiar(MB, RAIZ / "mabe", excluir=("robots.txt", "sitemap.xml"))
copiar(FR, RAIZ / "frigidaire", excluir=("robots.txt", "sitemap.xml"))
copiar(EL, RAIZ / "electrolux", excluir=("robots.txt", "sitemap.xml"))
copiar(GE, RAIZ / "general-electric", excluir=("robots.txt", "sitemap.xml"))
# sitemaps por marca + índice en la raíz
shutil.copy2(S / "sitemap.xml", RAIZ / "sitemap-samsung.xml")
shutil.copy2(L / "sitemap.xml", RAIZ / "lg" / "sitemap-lg.xml")
shutil.copy2(W / "sitemap.xml", RAIZ / "whirlpool" / "sitemap-whirlpool.xml")
shutil.copy2(MB / "sitemap.xml", RAIZ / "mabe" / "sitemap-mabe.xml")
shutil.copy2(FR / "sitemap.xml", RAIZ / "frigidaire" / "sitemap-frigidaire.xml")
shutil.copy2(EL / "sitemap.xml", RAIZ / "electrolux" / "sitemap-electrolux.xml")
shutil.copy2(GE / "sitemap.xml", RAIZ / "general-electric" / "sitemap-general-electric.xml")
(RAIZ / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    f'<sitemap><loc>{DOM}/sitemap-samsung.xml</loc><lastmod>{HOY}</lastmod></sitemap>\n<sitemap><loc>{DOM}/lg/sitemap-lg.xml</loc><lastmod>{HOY}</lastmod></sitemap>\n<sitemap><loc>{DOM}/whirlpool/sitemap-whirlpool.xml</loc><lastmod>{HOY}</lastmod></sitemap>\n<sitemap><loc>{DOM}/mabe/sitemap-mabe.xml</loc><lastmod>{HOY}</lastmod></sitemap>\n<sitemap><loc>{DOM}/frigidaire/sitemap-frigidaire.xml</loc><lastmod>{HOY}</lastmod></sitemap>\n<sitemap><loc>{DOM}/electrolux/sitemap-electrolux.xml</loc><lastmod>{HOY}</lastmod></sitemap>\n<sitemap><loc>{DOM}/general-electric/sitemap-general-electric.xml</loc><lastmod>{HOY}</lastmod></sitemap>\n</sitemapindex>\n', encoding="utf-8")
robots = (RAIZ / "robots.txt").read_text(encoding="utf-8")
import re
robots = re.sub(r"Sitemap:.*", f"Sitemap: {DOM}/sitemap.xml", robots)
(RAIZ / "robots.txt").write_text(robots, encoding="utf-8")
# llms.txt raíz: Samsung + referencia a LG
ll = (RAIZ / "llms.txt").read_text(encoding="utf-8")
ll = ll.replace("# Servicio Técnico Samsung Panamá", "# Centro de Servicio Panamá (Samsung y LG)", 1)
(RAIZ / "llms.txt").write_text(ll, encoding="utf-8")
# llms.txt raíz: presentación de la entidad y mapa de marcas para asistentes de IA
MARCAS = [("Samsung", ""), ("LG", "lg/"), ("Whirlpool", "whirlpool/"), ("Mabe", "mabe/"), ("Frigidaire", "frigidaire/"), ("Electrolux", "electrolux/"), ("General Electric", "general-electric/")]
cab = ("# Centro de Servicio Panamá\n\n> Servicio técnico a domicilio de neveras, refrigeradoras, lavadoras y secadoras en Ciudad de Panamá, San Miguelito y Panamá Oeste. "
       "Diagnóstico honesto, costo confirmado antes de reparar, garantía y visitas en 24 a 48 horas. WhatsApp +507 6933-7976. Lun a Sáb 7:00am–6:00pm.\n\n## Marcas que atendemos\n"
       + "".join(f"- [Servicio técnico {n} Panamá]({DOM}/{p}index.html): guía completa en {DOM}/{p}llms.txt\n" for n, p in MARCAS) + "\n")
(RAIZ / "llms.txt").write_text(cab + (RAIZ / "llms.txt").read_text(encoding="utf-8"), encoding="utf-8")
# 404 y reglas del servidor (Apache): compresión, caché, página de error
(RAIZ / "404.html").write_text('<!DOCTYPE html><html lang="es-PA"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Página no encontrada | Centro de Servicio Panamá</title>'
    '<meta name="robots" content="noindex, follow"><style>body{margin:0;font:16px/1.6 system-ui,sans-serif;display:grid;place-items:center;min-height:100vh;background:#f6f7f9;color:#17181b;text-align:center;padding:24px}a{color:#0b4ea2;font-weight:700}</style></head>'
    '<body><main><h1>No encontramos esa página</h1><p>Puede que el enlace haya cambiado. Vuelve al inicio o escríbenos por WhatsApp al <a href="https://wa.me/50769337976">+507 6933-7976</a>.</p><p><a href="/index.html">Ir al inicio</a></p></main></body></html>', encoding="utf-8")
(RAIZ / ".htaccess").write_text("""ErrorDocument 404 /404.html
<IfModule mod_deflate.c>
AddOutputFilterByType DEFLATE text/html text/css application/javascript application/json image/svg+xml text/plain application/xml
</IfModule>
<IfModule mod_expires.c>
ExpiresActive On
ExpiresByType image/webp "access plus 1 year"
ExpiresByType image/jpeg "access plus 1 year"
ExpiresByType image/png "access plus 1 year"
ExpiresByType image/svg+xml "access plus 1 year"
ExpiresByType text/css "access plus 1 month"
ExpiresByType application/javascript "access plus 1 month"
ExpiresByType text/html "access plus 10 minutes"
</IfModule>
<IfModule mod_headers.c>
Header set X-Content-Type-Options "nosniff"
Header set Referrer-Policy "strict-origin-when-cross-origin"
</IfModule>
""", encoding="utf-8")
# Organización y sitio web del dominio (solo portada principal)
import json as _j
_org = {"@context": "https://schema.org", "@graph": [
    {"@type": "Organization", "@id": DOM + "/#organizacion", "name": "Centro de Servicio Panamá", "url": DOM + "/", "telephone": "+507 6933-7976",
     "areaServed": {"@type": "AdministrativeArea", "name": "Panamá"}, "contactPoint": {"@type": "ContactPoint", "telephone": "+507 6933-7976", "contactType": "customer service", "areaServed": "PA", "availableLanguage": "es", "hoursAvailable": "Mo-Sa 07:00-18:00"}},
    {"@type": "WebSite", "@id": DOM + "/#sitio", "url": DOM + "/", "name": "Centro de Servicio Panamá", "inLanguage": "es-PA", "publisher": {"@id": DOM + "/#organizacion"}}]}
_ix = (RAIZ / "index.html").read_text(encoding="utf-8")
(RAIZ / "index.html").write_text(_ix.replace("</head>", '<script type="application/ld+json">' + _j.dumps(_org, ensure_ascii=False) + "</script></head>", 1), encoding="utf-8")
# zip
z = RAIZ.parent / "entrega" / "centrodeserviciopanama-com.zip"
z.parent.mkdir(exist_ok=True)
n = 0
with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
    for p in RAIZ.rglob("*"):
        if p.is_file() and "_fuente" not in p.parts and p.name != "README.md":
            zf.write(p, p.relative_to(RAIZ).as_posix()); n += 1
print(f"OK: {n} archivos → {z.name}")
