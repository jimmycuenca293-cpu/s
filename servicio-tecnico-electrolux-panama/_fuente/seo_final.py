# -*- coding: utf-8 -*-
"""Refinamiento SEO final de cada página: títulos y descripciones en longitud ideal, redes sociales, precarga del encabezado, noindex en legales."""
import re, html as _h, datetime
LASTMOD = datetime.date.today().isoformat()
NOINDEX = {"aviso-legal.html", "privacidad.html"}
_PREP = {"de", "la", "el", "en", "y", "que", "qué", "con", "del", "para", "a", "los", "las", "un", "una", "o", "por", "al"}

def _corta(t, n):
    if len(t) <= n: return t
    c = t[:n + 1].rsplit(" ", 1)[0].rstrip(" ,;:.-–|")
    w = c.split(" ")
    while len(w) > 3 and w[-1].lower() in _PREP: w.pop()
    return " ".join(w)

def ajustar_titulo(t, marca, n=60):
    t = _h.unescape(t)
    if len(t) <= n: return t
    partes = [p.strip() for p in t.split(" | ")]
    for k in range(len(partes) - 1, 1, -1):
        c = " | ".join(partes[:k])
        if len(c) <= n: return c
    primero = partes[0]
    if marca.lower() not in primero.lower():
        c = f"{primero} | {marca} Panamá"
        if len(c) <= n: return c
        c = f"{primero} | {marca}"
        if len(c) <= n: return c
        return _corta(primero, n - len(marca) - 3) + f" | {marca}"
    if len(partes) > 1 and len(primero) <= n: return primero
    return _corta(primero, n)

_USADOS = {}
def titulo_unico(t, marca, ruta):
    for n in ((72,) if ruta == "index.html" else (60, 72)):
        c = ajustar_titulo(t, marca, n)
        if _USADOS.get(c, ruta) == ruta: _USADOS[c] = ruta; return c
    c = _h.unescape(t)
    _USADOS[c] = ruta
    return c

def ajustar_desc(d, n=155):
    d = _h.unescape(d)
    d = re.sub(r"\s*WhatsApp \+507 6933-7976\.?$", "", d).strip() if len(d) > n else d
    if len(d) < 100: d = d.rstrip(".") + (". Visita a domicilio, diagnóstico claro y garantía. WhatsApp +507 6933-7976." if "Panamá" in d else ". Servicio técnico a domicilio en Panamá con garantía. WhatsApp +507 6933-7976.")
    if len(d) <= n: return d
    c = d[:n + 1]
    i = max(c.rfind(". "), c.rfind("; "))
    if i >= 90: return c[:i + 1]
    return _corta(d, n - 1).rstrip(",") + "."

def refinar(h, ruta, marca):
    esc = lambda s: _h.escape(s, quote=True)
    m = re.search(r"<title>(.*?)</title>", h, re.S)
    if m:
        t = titulo_unico(m.group(1), marca, ruta)
        h = h.replace(m.group(0), f"<title>{esc(t)}</title>", 1)
        h = re.sub(r'(<meta property="og:title" content=")[^"]*"', lambda x: x.group(1) + esc(t) + '"', h, 1)
    m = re.search(r'<meta name="description" content="(.*?)">', h)
    d = None
    if m:
        d = ajustar_desc(m.group(1))
        h = h.replace(m.group(0), f'<meta name="description" content="{esc(d)}">', 1)
        h = re.sub(r'(<meta property="og:description" content=")[^"]*"', lambda x: x.group(1) + esc(d) + '"', h, 1)
    extra = ""
    mi = re.search(r'<meta property="og:image" content="([^"]*)">', h)
    if mi:
        extra += '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
        extra += f'<meta property="og:image:alt" content="{esc(marca)}: servicio técnico a domicilio en Panamá"><meta name="twitter:image" content="{mi.group(1)}">'
    if m and 'twitter:title' not in h:
        mt = re.search(r"<title>(.*?)</title>", h, re.S).group(1)
        extra += f'<meta name="twitter:title" content="{mt}"><meta name="twitter:description" content="{esc(d)}">'
    mb = re.search(r'--bg:url\(([^)]+)\)', h)
    if mb: extra += f'<link rel="preload" as="image" href="{mb.group(1)}" fetchpriority="high">'
    if ruta in NOINDEX:
        h = h.replace('content="index, follow, max-image-preview:large"', 'content="noindex, follow"', 1)
    h = h.replace("</head>", extra + "</head>", 1)
    h = re.sub(r'<img (?![^>]*decoding=)', '<img decoding="async" ', h)
    return h
