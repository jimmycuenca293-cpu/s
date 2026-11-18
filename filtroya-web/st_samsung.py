#!/usr/bin/env python3
"""Soporte técnico Samsung (línea blanca, y televisores en Costa Rica) en varios países.
Páginas .html con «Respuesta rápida» en cada una, país → ciudad → servicio, guías de fallas, centro de respuestas para IA, sitemaps, llms.txt y formulario de solicitud de visita.

Uso:  python3 st_samsung.py <carpeta_de_salida> [dominio] [etiquetas_search_console_separadas_por_coma] [GTM-XXXX]
Variables de entorno opcionales: ST_WA (WhatsApp con indicativo, ej. 573205102995), ST_CONTACTOS (JSON país→WhatsApp), CORREO_AVISOS, SMTP_CLAVE.
"""
import datetime, hashlib, html, json, os, pathlib, random, re, shutil, sys, unicodedata

from st_datos import PAISES, SERVICIOS, ORDEN_SERV
from st_guias import GUIAS

AQUI = pathlib.Path(__file__).resolve().parent
# Modo sitio de una sola ciudad (ST_SOLO=ibague): solo Colombia y esa ciudad; las URLs quedan en la raíz (/lavadoras/, /el-salado/…)
SOLO = os.environ.get("ST_SOLO", "").strip()
BARRIOS_SOLO = {"ibague": ["Centro", "Jordán", "Picaleña", "El Salado", "Ambalá", "Interlaken", "Cádiz", "La Pola", "Belén", "Calambeo", "Piedra Pintada", "Mirolindo", "Arkacentro", "Gaitán", "El Vergel", "Topacio", "Alaska", "Boquerón", "Las Américas", "Libertador", "Santa Ana", "Restrepo", "Galán", "Granjas", "Combeima", "Ciudad Luz", "La Francia", "Ancón"]}
BARRIOS_SOLO["valledupar"] = ["Centro", "Los Mayales", "Los Campanos", "Alfonso López", "Villa Castro", "Novalito", "La Nevada", "Sicarare", "Garupal", "Cañaguate", "Altos del Rosario", "Villa Corelca", "Primero de Mayo", "12 de Octubre", "Los Fundadores", "Simón Bolívar", "Dangond", "Mareigua", "Divino Niño", "El Eneal", "Los Almendros", "Ciudad Salguero", "Altamira", "Los Cortijos", "Villa Alexandra", "7 de Agosto", "La Esperanza", "San Joaquín", "Sabanas del Rosario", "La Granja", "Los Músicos", "Villa Rosario", "Badillo", "Patillal", "Guacoche", "Mariangola", "Valencia de Jesús", "Atánquez", "Aguas Blancas", "Río Seco"]
SOLO_CFG = {"ibague": dict(nombre="Ibagué", dep="Tolima", lat=4.4389, lon=-75.2322, region="CO-TOL", tv=False, token="VnmP5YjaE7DzC-ztjsRFetEvNfbNaK9Mes-zaxXigoA"),
            "valledupar": dict(nombre="Valledupar", dep="Cesar", lat=10.4631, lon=-73.2532, region="CO-CES", tv=True, token="")}
if SOLO:
    _sl = lambda n: re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", n).encode("ascii", "ignore").decode().lower()).strip("-")
    PAISES = {"colombia": dict(PAISES["colombia"], ciudades=[(n, d, BARRIOS_SOLO.get(SOLO, z), t) for (n, d, z, t) in PAISES["colombia"]["ciudades"] if _sl(n) == SOLO], tv=(("televisor", "televisores") if SOLO_CFG[SOLO]["tv"] else None))}
OUT = pathlib.Path(sys.argv[1])
DOMINIO = (sys.argv[2] if len(sys.argv) > 2 else (f"https://serviciotecnicosamsung{SOLO}.click" if SOLO else "https://samsungsoportetecnico.com")).rstrip("/")
TOKENS = [t.strip() for t in (sys.argv[3] if len(sys.argv) > 3 else "").split(",") if t.strip()]
TOKENS = list(dict.fromkeys(TOKENS + ([SOLO_CFG[SOLO]["token"]] if SOLO and SOLO_CFG[SOLO]["token"] else ([] if SOLO else ["o38zbB3vp7xMgOaD4hdjS24tYMas1y4ozPiacc5Hiuc"]))))  # Search Console
GTM = (sys.argv[4] if len(sys.argv) > 4 else "").strip().upper()
# WhatsApp de cada país (los de los proyectos anteriores): Panamá cubre también Guatemala y El Salvador; Ecuador cubre también Paraguay.
WA_PAIS = {"colombia": "573013810242", "panama": "50769337976", "guatemala": "50769337976", "el-salvador": "50769337976", "costa-rica": "50670055753", "ecuador": "593993508191", "paraguay": "593993508191", "chile": "56983176106"}
CONTACTOS = {**WA_PAIS, **json.loads(os.environ.get("ST_CONTACTOS", "{}"))}
WA_DEF = os.environ.get("ST_WA", WA_PAIS["colombia"])
HOY = datetime.date.today().isoformat()
_M = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
_d = datetime.date.today()
FECHA_LARGA = f"{_d.day} de {_M[_d.month - 1]} de {_d.year}"
NOMBRE = f"Servicio Técnico Samsung {SOLO_CFG[SOLO]['nombre']}" if SOLO else "Soporte Técnico Samsung"
esc = lambda s: html.escape(str(s), quote=True)


def slug(n):
    n = unicodedata.normalize("NFKD", str(n)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", n).strip("-")


def wa_num(pk):
    return str(CONTACTOS.get(pk, WA_DEF))


def wa_vis(pk):
    n = wa_num(pk)
    for pref, g in (("507", (4, 4)), ("506", (4, 4)), ("502", (4, 4)), ("503", (4, 4)), ("595", (3, 3, 3)), ("593", (2, 3, 4)), ("57", (3, 3, 4)), ("56", (1, 4, 4))):
        if n.startswith(pref):
            r = n[len(pref):]; partes = []; i = 0
            for k in g:
                partes.append(r[i:i + k]); i += k
            return f"+{pref} " + " ".join(x for x in partes if x)
    return "+" + n


def wa_link(pk, msg):
    return f"https://wa.me/{wa_num(pk)}?text=" + re.sub(r"%20", "%20", __import__("urllib.parse").parse.quote(msg))


# ------------------------------------------------------------------ datos derivados
CIU = []
from st_datos2 import EXTRA, BUCKETS
if SOLO:
    EXTRA = {"colombia": [(n, d, BARRIOS_SOLO[SOLO], b, a) for (n, d, z, b, a) in EXTRA.get("colombia", []) if _sl(n) == SOLO]}
from st_clima import CLIMA
_usados = set()
for pk, P in PAISES.items():
    todos = [(n, dep, zonas, None, None, False) for (n, dep, zonas, tipo) in P["ciudades"]] + [(n, dep, zonas, b, alt, True) for (n, dep, zonas, b, alt) in EXTRA.get(pk, [])]
    for (n, dep, zonas, b, alt, amp) in todos:
        s_ = slug(n)
        if s_ in _usados:
            s_ = f"{s_}-{pk}"
        _usados.add(s_)
        zs = [(f"Centro de {n}" if z == "Centro" else z) for z in zonas]
        zp = len(zs) >= 3
        if not zs:
            zs = [f"Centro de {n}"]
        if amp:
            CLIMA[s_] = dict(BUCKETS[b], alt=alt)
        CIU.append(dict(n=n, d=slug(n), dep=dep, zonas=zs, pk=pk, s=s_, pais=P["nombre"], cap=(not amp and n == P["ciudades"][0][0]), amp=amp, zp=zp))
if SOLO:
    for _cc in CIU:
        _cc["amp"] = False; _cc["cap"] = True; _cc["zp"] = True
CIU_PAIS = {pk: [c for c in CIU if c["pk"] == pk] for pk in PAISES}
SERV_PAIS = {pk: [s for s in ORDEN_SERV] + (["tv"] if PAISES[pk]["tv"] else []) for pk in PAISES}
GEN = {"nevera": "neveras", "lava": "lavadoras", "seca": "secadoras", "lavaplatos": "lavavajillas", "cocina": "cocinas-y-hornos", "micro": "microondas", "tv": "televisores"}


def pal(pk, sv):  # (singular, plural) en el vocabulario del país
    P = PAISES[pk]
    key = {"nevera": "nevera", "lava": "lava", "seca": "seca", "lavaplatos": "lavaplatos", "cocina": "cocina", "micro": "micro", "tv": "tv"}[sv]
    return P[key]


# URLs internas: cada país es un directorio propio (/colombia/medellin/lavadoras/). Los hrefs se escriben desde la raíz y pagina() los vuelve relativos.
R_PAIS = lambda pk: f"{pk}/index.html"
R_CIU = lambda c: f"{c['pk']}/{c['d']}/index.html"
R_CS = lambda c, sv: f"{c['pk']}/{c['d']}/{slug(pal(c['pk'], sv)[1])}/index.html"
R_SERV = lambda pk, sv: f"{pk}/{slug(pal(pk, sv)[1])}/index.html"
R_G = lambda g, pk: f"{pk}/guias/{g['slug']}/index.html"
R_GUIAS = lambda pk: f"{pk}/guias/index.html"
R_INST = lambda pk, n: f"{pk}/{n}/index.html"
R_FAQ = lambda pk: R_INST(pk, "preguntas-frecuentes")
R_IA = lambda pk: R_INST(pk, "respuestas-rapidas")
R_SOL = lambda pk: R_INST(pk, "solicitar-visita")
R_WA = lambda c: f"{c['pk']}/{c['d']}/whatsapp/index.html"
R_TEL = lambda c: f"{c['pk']}/{c['d']}/telefono/index.html"
R_WAP = lambda pk: f"{pk}/whatsapp/index.html"
R_TELP = lambda pk: f"{pk}/telefono/index.html"
R_BARRIOS = lambda c: f"{c['pk']}/{c['d']}/barrios/index.html"
R_ZS = lambda c, z, sv: f"{c['pk']}/{c['d']}/{slug(z)}/{slug(pal(c['pk'], sv)[1])}/index.html"
R_MAPA = lambda pk: R_INST(pk, "mapa-del-sitio")
R_COD = lambda pk, cod: f"{pk}/guias/{slug(pal(pk, 'lava')[0])}-samsung-codigo-{slug(cod)}/index.html"
R_COD_LISTA = lambda pk: f"{pk}/guias/codigos-de-error-{slug(pal(pk, 'lava')[0])}-samsung/index.html"
R_MOD = lambda pk, sv: f"{pk}/guias/como-leer-el-modelo-de-tu-{slug(pal(pk, sv)[0])}-samsung/index.html"
for _pk in PAISES:
    _ds = [c["d"] for c in CIU_PAIS[_pk]]
    assert len(_ds) == len(set(_ds)), _pk


def solo_ruta(n):  # en el modo de una ciudad, colombia/ibague/x -> x
    if SOLO:
        for pre in (f"colombia/{SOLO}/", "colombia/"):
            if n.startswith(pre):
                return n[len(pre):] or "index.html"
    return n


def U(n):  # URL pública limpia de una página
    n = solo_ruta(n)
    n = "" if n == "index.html" else (n[:-10] if n.endswith("/index.html") else n)
    return f"{DOMINIO}/{n}"


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

# Fotos reales del equipo (las de los proyectos anteriores). Para lavavajillas, cocina, microondas y televisor no hay foto de producto: se usa una foto del técnico en visita.
IMG_ORIGEN = AQUI.parent / "samsung-el-salvador" / "fuente" / "img"
for f in ("nevera-family-hub", "nevera-superior-inox", "lavadora-superior", "secadora", "secadora-torre", "torre-lavado"):
    for suf in ("", "-m", "-s"):
        shutil.copy(IMG_ORIGEN / f"{f}{suf}.webp", OUT / "img" / f"{f}{suf}.webp")
for f in ("stp1", "stp2", "stp3", "stp4", "stp5", "stp6", "stp7", "c-revision", "c-compresor", "tecnico-lavadora", "tecnico-neveras", "portada-tecnico"):
    shutil.copy(IMG_ORIGEN / f"{f}.webp", OUT / "img" / f"{f}.webp")
NUEVAS = {1: "tecnico-samsung-saluda-en-la-puerta", 2: "atencion-al-cliente-servicio-samsung", 3: "tecnico-samsung-entrega-orden-de-servicio", 4: "tecnico-samsung-reparando-lavadora-a-domicilio", 5: "taller-reparacion-televisores-samsung"}
for _n in ("estufa-samsung-4-hornillas-horno", "horno-empotrado-samsung-acero", "lavavajillas-samsung-acero-inoxidable"):
    for _suf in ("", "-m", "-s"):
        shutil.copy(AQUI / "st_img" / "nuevas" / f"{_n}{_suf}.webp", OUT / "img" / f"{_n}{_suf}.webp")
for _i, _n in NUEVAS.items():
    shutil.copy(AQUI / "st_img" / "nuevas" / f"{_i}.webp", OUT / "img" / f"{_n}.webp")
from PIL import Image as _I
_mi = _I.open(AQUI / "st_img" / "microondas.png").convert("RGB")
for _suf, _lado in (("", 800), ("-m", 460), ("-s", 240)):
    _mi.resize((_lado, _lado), _I.LANCZOS).save(OUT / "img" / f"microondas{_suf}.webp", "WEBP", quality=85, method=6)
FOTO = {"nevera": ("nevera-family-hub-m.webp", "Nevera Samsung", False), "lava": ("lavadora-superior-m.webp", "Lavadora Samsung", False), "seca": ("secadora-m.webp", "Secadora Samsung", False),
        "lavaplatos": ("lavavajillas-samsung-acero-inoxidable-m.webp", "Lavavajillas Samsung", False), "cocina": ("estufa-samsung-4-hornillas-horno-m.webp", "Estufa y horno Samsung", False), "micro": ("microondas-m.webp", "Microondas Samsung", False),
        "tv": ("taller-reparacion-televisores-samsung.webp", "Técnico reparando la tarjeta de un televisor Samsung en el taller", True)}


def foto_serv(sv, alto=150, mini=False, ctx=None):
    f, alt, cover = FOTO[sv]
    if sv == "cocina" and int(hashlib.md5((ctx or "x").encode()).hexdigest()[:4], 16) % 2:
        f, alt = "horno-empotrado-samsung-acero-m.webp", "Horno empotrado Samsung"
    if ctx:
        alt = f"{alt}: servicio técnico a domicilio en {ctx}"
    if mini:
        f = f.replace("-m.webp", "-s.webp") if not cover else f
    return f'<img class="st-fimg{" cover" if cover else ""}" src="img/{f}" alt="{esc(alt)}" loading="lazy" decoding="async">'


ICO = {"lupa": '<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>', "wa": '<svg viewBox="0 0 16 16" width="20" height="20" fill="currentColor"><path d="M13.6 2.3A7.85 7.85 0 0 0 8 0C3.6 0 .07 3.56.06 7.93c0 1.4.37 2.76 1.06 3.97L0 16l4.2-1.1a7.93 7.93 0 0 0 3.8.97c4.37 0 7.93-3.56 7.93-7.93a7.9 7.9 0 0 0-2.33-5.64zM8 14.5a6.57 6.57 0 0 1-3.36-.92l-.24-.14-2.5.65.67-2.43-.16-.25A6.56 6.56 0 0 1 1.4 7.9c0-3.63 2.97-6.6 6.6-6.6 1.77 0 3.43.69 4.68 1.94a6.55 6.55 0 0 1 1.93 4.67c0 3.63-2.96 6.6-6.6 6.6zm3.62-4.94c-.2-.1-1.17-.58-1.35-.64-.18-.07-.31-.1-.44.1-.13.2-.5.64-.62.78-.11.13-.23.15-.43.05-.2-.1-.83-.3-1.58-.97-.58-.52-.98-1.16-1.1-1.35-.1-.2-.01-.3.09-.4.09-.09.2-.23.3-.35.1-.12.13-.2.2-.33.06-.13.03-.25-.02-.35-.05-.1-.44-1.06-.6-1.45-.16-.38-.32-.33-.44-.34h-.38c-.13 0-.35.05-.53.25-.18.2-.7.68-.7 1.67 0 .98.72 1.93.82 2.07.1.13 1.4 2.14 3.4 3 .47.2.84.33 1.13.42.48.15.91.13 1.25.08.38-.06 1.17-.48 1.34-.94.16-.46.16-.86.11-.94-.05-.08-.18-.13-.38-.23z"/></svg>'}
exec(open(AQUI / "st_base.py", encoding="utf-8").read())
exec(open(AQUI / "st_motor.py", encoding="utf-8").read())
exec(open(AQUI / "st_paginas.py", encoding="utf-8").read())
