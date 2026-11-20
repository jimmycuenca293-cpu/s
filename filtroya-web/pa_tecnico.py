#!/usr/bin/env python3
"""Arreglos técnicos de SEO para una copia local de samsungpanamaserviciotecnico.com (no toca las frases de marca ni de «autorizado»).
Uso: python3 pa_tecnico.py <carpeta_con_el_sitio> <carpeta_de_salida> <etiqueta_search_console>
- Títulos de más de 70 caracteres -> se acortan sin perder «Panamá».
- Descripciones de más de 160 -> se recortan en un límite de frase o palabra.
- Agrega la etiqueta de Search Console a todas las páginas.
- sitemap.xml con fecha de hoy. Deja HTACCESS-pegar-arriba.txt para unificar www/https.
"""
import html, os, pathlib, re, sys, datetime
SRC, OUT, TOKEN = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3]
OUT.mkdir(parents=True, exist_ok=True)
HOY = datetime.date.today().isoformat()
ABREV = [(r"\s*\([^)]*\)", ""), ("Refrigeradoras Side by Side y Family Hub", "Side by Side y Family Hub"), ("Servicio Técnico de ", ""), ("Diagnóstico y Reparación", "Reparación"), ("Diagnóstico, Reparación y Repuestos", "Reparación y Repuestos")]
def titulo(t, lim=70):
    t = re.sub(r"\s+", " ", html.unescape(t)).strip()
    while len(t) > lim and " | " in t:
        t = t.rsplit(" | ", 1)[0]
    for a, b in ABREV:
        if len(t) <= lim: break
        t = re.sub(a, b, t).strip()
    if len(t) > lim:
        t = t[:lim].rsplit(" ", 1)[0].rstrip(" ,:;-|")
    return t
def descripcion(d, lim=158):
    d = re.sub(r"\s+", " ", html.unescape(d)).strip()
    if len(d) <= lim: return d
    c = d[:lim]; k = max(c.rfind(". "), c.rfind("; "))
    if k > 80: return c[:k + 1]
    return c[:c.rfind(" ")].rstrip(" ,;:.") + "."
MANUAL = {"blog-cuidados-samsung-panama.html": "Blog: Cuidados de Electrodomésticos Samsung en Panamá",
          "reparaciones-samsung-panama.html": "Reparaciones Samsung en Panamá | Todos los Equipos",
          "reparacion-electrodomesticos-samsung-panama.html": "Reparación de Electrodomésticos Samsung en Panamá"}
cambios = {"titulo": 0, "desc": 0, "token": 0}
for f in sorted(SRC.glob("*.html")):
    t = f.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"<title>(.*?)</title>", t, re.S)
    if m:
        n = MANUAL.get(f.name) or titulo(m.group(1))
        if n != html.unescape(m.group(1)).strip():
            t = t.replace(m.group(0), f"<title>{html.escape(n, quote=False)}</title>", 1); cambios["titulo"] += 1
            t = re.sub(r'(<meta property="og:title" content=")[^"]*(")', lambda x: x.group(1) + html.escape(n) + x.group(2), t, count=1)
    m = re.search(r'(<meta name="description" content=")(.*?)(")', t, re.S)
    if m and len(html.unescape(m.group(2))) > 160:
        n = descripcion(m.group(2)); t = t.replace(m.group(0), m.group(1) + html.escape(n) + m.group(3), 1); cambios["desc"] += 1
        t = re.sub(r'(<meta property="og:description" content=")[^"]*(")', lambda x: x.group(1) + html.escape(n) + x.group(2), t, count=1)
    if TOKEN not in t:
        tag = f'<meta name="google-site-verification" content="{TOKEN}">'
        t = t.replace("</head>", tag + "\n</head>", 1) if "</head>" in t else t; cambios["token"] += 1
    (OUT / f.name).write_text(t, encoding="utf-8")
sm = SRC / "sitemap.xml"
if sm.exists():
    s = sm.read_text(encoding="utf-8")
    s = re.sub(r"<lastmod>[^<]*</lastmod>", f"<lastmod>{HOY}</lastmod>", s)
    (OUT / "sitemap.xml").write_text(s, encoding="utf-8")
(OUT / "HTACCESS-pegar-arriba.txt").write_text("""# Pega ESTAS líneas al PRINCIPIO de tu .htaccess actual (no lo reemplaces entero).
# Unifica la dirección: todo va a https://www.samsungpanamaserviciotecnico.com/ (la que ya declaras como canonical).
RewriteEngine On
RewriteCond %{HTTPS} off [OR]
RewriteCond %{HTTP_HOST} !^www\\. [NC]
RewriteRule ^(.*)$ https://www.samsungpanamaserviciotecnico.com/$1 [L,R=301]
""", encoding="utf-8")
print(cambios)
