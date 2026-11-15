#!/usr/bin/env python3
"""Centro de servicio técnico Samsung (línea blanca, y televisores en Costa Rica) en varios países.
Páginas .html con «Respuesta rápida» en cada una, país → ciudad → servicio, guías de fallas, centro de respuestas para IA, sitemaps, llms.txt y formulario de solicitud de visita.

Uso:  python3 st_samsung.py <carpeta_de_salida> [dominio] [etiquetas_search_console_separadas_por_coma] [GTM-XXXX]
Variables de entorno opcionales: ST_WA (WhatsApp con indicativo, ej. 573205102995), ST_CONTACTOS (JSON país→WhatsApp), CORREO_AVISOS, SMTP_CLAVE.
"""
import datetime, hashlib, html, json, os, pathlib, random, re, shutil, sys, unicodedata

from st_datos import PAISES, SERVICIOS, ORDEN_SERV
from st_guias import GUIAS

AQUI = pathlib.Path(__file__).resolve().parent
OUT = pathlib.Path(sys.argv[1])
DOMINIO = (sys.argv[2] if len(sys.argv) > 2 else "https://centrodeserviciotecnicosamsung.com").rstrip("/")
TOKENS = [t.strip() for t in (sys.argv[3] if len(sys.argv) > 3 else "").split(",") if t.strip()]
GTM = (sys.argv[4] if len(sys.argv) > 4 else "").strip().upper()
WA_DEF = os.environ.get("ST_WA", "573205102995")
CONTACTOS = json.loads(os.environ.get("ST_CONTACTOS", "{}"))
HOY = datetime.date.today().isoformat()
_M = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
_d = datetime.date.today()
FECHA_LARGA = f"{_d.day} de {_M[_d.month - 1]} de {_d.year}"
NOMBRE = "Centro de Servicio Técnico Samsung"
esc = lambda s: html.escape(str(s), quote=True)


def slug(n):
    n = unicodedata.normalize("NFKD", str(n)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", n).strip("-")


def wa_num(pk):
    return str(CONTACTOS.get(pk, WA_DEF))


def wa_vis(pk):
    n = wa_num(pk)
    p = PAISES[pk]["wa_pref"]
    r = n[len(p):] if n.startswith(p) else n
    return f"+{p} {r[:3]} {r[3:6]} {r[6:]}".strip()


def wa_link(pk, msg):
    return f"https://wa.me/{wa_num(pk)}?text=" + re.sub(r"%20", "%20", __import__("urllib.parse").parse.quote(msg))


# ------------------------------------------------------------------ datos derivados
CIU = []
for pk, P in PAISES.items():
    for (n, dep, zonas, tipo) in P["ciudades"]:
        CIU.append(dict(n=n, dep=dep, zonas=zonas, pk=pk, s=slug(n), pais=P["nombre"], cap=(tipo == "1")))
CIU_PAIS = {pk: [c for c in CIU if c["pk"] == pk] for pk in PAISES}
SERV_PAIS = {pk: [s for s in ORDEN_SERV] + (["tv"] if PAISES[pk]["tv"] else []) for pk in PAISES}
GEN = {"nevera": "neveras", "lava": "lavadoras", "seca": "secadoras", "lavaplatos": "lavavajillas", "cocina": "cocinas-y-hornos", "micro": "microondas", "tv": "televisores"}


def pal(pk, sv):  # (singular, plural) en el vocabulario del país
    P = PAISES[pk]
    key = {"nevera": "nevera", "lava": "lava", "seca": "seca", "lavaplatos": "lavaplatos", "cocina": "cocina", "micro": "micro", "tv": "tv"}[sv]
    return P[key]


R_PAIS = lambda pk: f"{pk}.html"
R_CIU = lambda c: f"servicio-tecnico-samsung-{c['s']}.html"
R_CS = lambda c, sv: f"reparacion-{slug(pal(c['pk'], sv)[1])}-samsung-{c['s']}.html"
R_SERV = lambda sv: f"servicio-tecnico-{GEN[sv]}-samsung.html"
R_G = lambda g: f"{g['slug']}.html"
PAGINAS = []  # (nombre, prioridad, titulo, desc, tipo)
(OUT / "img").mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------------ imágenes y logos
LOGOS = AQUI / "logos"
IMG_SAM = AQUI / "public_html" / "filtrosnevecones-img"
shutil.copy(LOGOS / "samsung-web.png", OUT / "img" / "samsung-logo.png")
shutil.copy(LOGOS / "samsung-oval-web.png", OUT / "img" / "samsung-oval.png")
shutil.copy(LOGOS / "samsung-icono.png", OUT / "img" / "icono-samsung.png")
FILTROS_IMG = [("sam-cin-o", "Filtro de agua Samsung HAF-CIN"), ("sam-qin-o", "Filtro de agua Samsung HAF-QIN"), ("sam-cu1-o", "Filtro de agua Samsung Aqua Pure Plus"), ("sam-ex-o", "Filtro de agua externo Samsung")]
for k, _ in FILTROS_IMG:
    for ext in ("webp",):
        if (IMG_SAM / f"{k}.{ext}").exists():
            shutil.copy(IMG_SAM / f"{k}.{ext}", OUT / "img" / f"{k}.{ext}")
            if (IMG_SAM / f"{k}-400.{ext}").exists():
                shutil.copy(IMG_SAM / f"{k}-400.{ext}", OUT / "img" / f"{k}-400.{ext}")

AZUL, AZUL2, CIAN = "#1428a0", "#5b7cff", "#7fe0f7"


def ilus(sv, tam=96):
    """Ilustración vectorial de cada electrodoméstico (azul Samsung)."""
    c, a, f = AZUL, AZUL2, "#eaefff"
    s = {
        "nevera": f'<rect x="30" y="8" width="60" height="104" rx="8" fill="{f}" stroke="{c}" stroke-width="3"/><path d="M30 46h60" stroke="{c}" stroke-width="3"/><rect x="38" y="24" width="4" height="14" rx="2" fill="{a}"/><rect x="38" y="56" width="4" height="26" rx="2" fill="{a}"/><circle cx="76" cy="26" r="3" fill="{a}"/>',
        "lava": f'<rect x="22" y="8" width="76" height="104" rx="8" fill="{f}" stroke="{c}" stroke-width="3"/><path d="M22 30h76" stroke="{c}" stroke-width="3"/><circle cx="60" cy="72" r="27" fill="#fff" stroke="{c}" stroke-width="3"/><circle cx="60" cy="72" r="17" fill="{a}" opacity=".35" stroke="{a}" stroke-width="2"/><circle cx="34" cy="19" r="3.5" fill="{a}"/><rect x="50" y="15" width="34" height="8" rx="4" fill="{a}" opacity=".6"/>',
        "seca": f'<rect x="22" y="8" width="76" height="104" rx="8" fill="{f}" stroke="{c}" stroke-width="3"/><path d="M22 30h76" stroke="{c}" stroke-width="3"/><circle cx="60" cy="72" r="27" fill="#fff" stroke="{c}" stroke-width="3"/><path d="M48 76c4-6 8 6 12 0s8 6 12 0" fill="none" stroke="{a}" stroke-width="3" stroke-linecap="round"/><path d="M48 66c4-6 8 6 12 0s8 6 12 0" fill="none" stroke="{a}" stroke-width="3" stroke-linecap="round"/><circle cx="34" cy="19" r="3.5" fill="{a}"/>',
        "lavaplatos": f'<rect x="20" y="14" width="80" height="94" rx="8" fill="{f}" stroke="{c}" stroke-width="3"/><path d="M20 36h80" stroke="{c}" stroke-width="3"/><rect x="34" y="42" width="52" height="6" rx="3" fill="{a}"/><path d="M34 62h52M34 76h52M34 90h52" stroke="{a}" stroke-width="3" opacity=".55"/><circle cx="32" cy="25" r="3.5" fill="{a}"/><circle cx="44" cy="25" r="3.5" fill="{a}"/>',
        "cocina": f'<rect x="20" y="10" width="80" height="100" rx="8" fill="{f}" stroke="{c}" stroke-width="3"/><circle cx="42" cy="28" r="9" fill="#fff" stroke="{c}" stroke-width="2.5"/><circle cx="78" cy="28" r="9" fill="#fff" stroke="{c}" stroke-width="2.5"/><circle cx="42" cy="28" r="3.5" fill="{a}"/><circle cx="78" cy="28" r="3.5" fill="{a}"/><path d="M20 46h80" stroke="{c}" stroke-width="3"/><rect x="30" y="56" width="60" height="42" rx="5" fill="#fff" stroke="{c}" stroke-width="3"/><rect x="38" y="64" width="44" height="26" rx="3" fill="{a}" opacity=".3"/><rect x="36" y="50" width="48" height="3" rx="1.5" fill="{a}"/>',
        "micro": f'<rect x="10" y="28" width="100" height="64" rx="8" fill="{f}" stroke="{c}" stroke-width="3"/><rect x="18" y="36" width="58" height="48" rx="5" fill="#fff" stroke="{c}" stroke-width="3"/><rect x="24" y="42" width="46" height="36" rx="3" fill="{a}" opacity=".3"/><circle cx="92" cy="46" r="5" fill="{a}"/><circle cx="92" cy="62" r="5" fill="{a}" opacity=".6"/><rect x="85" y="74" width="14" height="6" rx="3" fill="{a}"/>',
        "tv": f'<rect x="8" y="22" width="104" height="62" rx="6" fill="{f}" stroke="{c}" stroke-width="3"/><rect x="14" y="28" width="92" height="50" rx="3" fill="{a}" opacity=".35"/><path d="M60 84v14M42 100h36" stroke="{c}" stroke-width="3.5" stroke-linecap="round"/>',
    }[sv]
    return f'<svg viewBox="0 0 120 120" width="{tam}" height="{tam}" role="img" aria-hidden="true" class="ilus">{s}</svg>'


ICO = {"lupa": '<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>', "wa": '<svg viewBox="0 0 16 16" width="20" height="20" fill="currentColor"><path d="M13.6 2.3A7.85 7.85 0 0 0 8 0C3.6 0 .07 3.56.06 7.93c0 1.4.37 2.76 1.06 3.97L0 16l4.2-1.1a7.93 7.93 0 0 0 3.8.97c4.37 0 7.93-3.56 7.93-7.93a7.9 7.9 0 0 0-2.33-5.64zM8 14.5a6.57 6.57 0 0 1-3.36-.92l-.24-.14-2.5.65.67-2.43-.16-.25A6.56 6.56 0 0 1 1.4 7.9c0-3.63 2.97-6.6 6.6-6.6 1.77 0 3.43.69 4.68 1.94a6.55 6.55 0 0 1 1.93 4.67c0 3.63-2.96 6.6-6.6 6.6zm3.62-4.94c-.2-.1-1.17-.58-1.35-.64-.18-.07-.31-.1-.44.1-.13.2-.5.64-.62.78-.11.13-.23.15-.43.05-.2-.1-.83-.3-1.58-.97-.58-.52-.98-1.16-1.1-1.35-.1-.2-.01-.3.09-.4.09-.09.2-.23.3-.35.1-.12.13-.2.2-.33.06-.13.03-.25-.02-.35-.05-.1-.44-1.06-.6-1.45-.16-.38-.32-.33-.44-.34h-.38c-.13 0-.35.05-.53.25-.18.2-.7.68-.7 1.67 0 .98.72 1.93.82 2.07.1.13 1.4 2.14 3.4 3 .47.2.84.33 1.13.42.48.15.91.13 1.25.08.38-.06 1.17-.48 1.34-.94.16-.46.16-.86.11-.94-.05-.08-.18-.13-.38-.23z"/></svg>'}
exec(open(AQUI / "st_base.py", encoding="utf-8").read())
exec(open(AQUI / "st_paginas.py", encoding="utf-8").read())
