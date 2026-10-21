# -*- coding: utf-8 -*-
"""Genera el sitio estático «Servicio Técnico Frigidaire Panamá» (carpeta ..) y el zip."""
import html, json, re, shutil, sys, unicodedata, zipfile
from pathlib import Path
from urllib.parse import quote
from contenido import *
from seo import *
from seo_final import *

AQUI = Path(__file__).resolve().parent
OUT = AQUI.parent
esc = lambda s: html.escape(str(s), quote=True)
def slug(s):
    s = unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

PAGINAS = {}   # ruta -> (prioridad, titulo)
ICONOS = {
 "fridge": '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><rect x="12" y="4" width="24" height="40" rx="3"/><path d="M12 19h24M17 11v4M17 25v8"/></svg>',
 "washer": '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="4" width="30" height="40" rx="3"/><circle cx="24" cy="27" r="9"/><path d="M15 11h4M22 11h3"/><path d="M19 27c2-2 4 2 6 0"/></svg>',
 "dryer": '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="4" width="30" height="40" rx="3"/><circle cx="24" cy="27" r="9"/><path d="M15 11h4M22 11h3"/><path d="M20 24c1 4 3 4 4 0M24 30c1 3 3 3 4 0"/></svg>',
 "ac": '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="9" width="40" height="14" rx="3"/><path d="M10 28c0 4 2 5 2 9M20 28c0 4 2 5 2 9M30 28c0 4 2 5 2 9"/><path d="M10 16h28"/></svg>',
 "wrench": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.2L3 17.8V21h3.2l6.3-6.3a4 4 0 0 0 5.2-5.4l-2.5 2.5-2.4-.6-.6-2.4z"/></svg>',
 "wa": '<svg viewBox="0 0 32 32" aria-hidden="true"><path fill="currentColor" d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 23.6c-2 0-4-.6-5.7-1.6l-.4-.2-3.9 1 1-3.8-.3-.4A10.6 10.6 0 1 1 16 26.6zm5.8-7.9c-.3-.2-1.9-.9-2.2-1s-.5-.2-.7.2-.8 1-1 1.2-.4.2-.7.1a8.700 8.700 0 0 1-4.300-3.800c-.3-.6.3-.5.9-1.700.1-.2 0-.4 0-.5l-1-2.300c-.2-.6-.5-.5-.7-.5h-.6a1.200 1.200 0 0 0-.9.4 3.700 3.700 0 0 0-1.100 2.700c0 1.600 1.200 3.200 1.300 3.400s2.300 3.500 5.600 4.900c2 .9 2.800.9 3.800.8a3.200 3.200 0 0 0 2.100-1.500 2.600 2.600 0 0 0 .2-1.500c-.1-.1-.3-.2-.6-.4z"/></svg>',
}
def wa(msg=""):
    return f"https://wa.me/{WA}" + (f"?text={quote(msg)}" if msg else "")
def R(depth): return "../" * depth
def pic(nombre, alt, depth, w, h, clase="fto", lazy=True):
    r = R(depth)
    return f'<picture class="{clase}"><source srcset="{r}images/fotos/{nombre}.webp" type="image/webp"><img src="{r}images/fotos/{nombre}.jpg" alt="{esc(alt)}" width="{w}" height="{h}"{" loading=\"lazy\"" if lazy else ""}></picture>'
FOTO_EQ = {"neveras": ("sam-4", "Técnico reparando una refrigeradora Frigidaire en una cocina de Panamá"), "lavadoras": ("sam-3", "Técnico revisando una lavadora Frigidaire en una cocina de Panamá")}

WH = {"sam-4": (704, 378), "sam-4": (804, 450), "sam-3": (720, 500), "sam-1": (720, 500), "filtro-pelusa-1": (535, 485), "filtro-pelusa-2": (700, 700), "filtro-pelusa-3": (1000, 1000), "filtro-agua": (277, 641), "prod-nevera-sbs": (236, 497), "prod-nevera-sbs": (182, 328), "prod-lavadora-sup": (228, 382), "prod-torre": (345, 900), "sam-1": (1024, 765), "sam-2": (1024, 765), "sam-3": (1024, 765), "sam-4": (1024, 765), "sam-5": (1024, 765), "sam-6": (1024, 765), "sam-6": (1024, 765), "prod-lavadora-fr": (375, 494), "sam-5": (1024, 572), "sam-6": (1024, 434), "sam-1": (1024, 572)}
ALT = {"sam-1": "Asesora de servicio atendiendo en el mostrador", "sam-2": "Técnico y asesora de servicio conversando en la oficina", "sam-3": "Técnico saludando a la clienta en la puerta de su apartamento", "sam-4": "Técnico revisando una nevera con la clienta en la cocina", "sam-5": "Asesora atendiendo a un cliente en el mostrador", "sam-6": "Asesora de servicio atendiendo una llamada", "sam-6": "Técnico midiendo con multímetro una lavadora en la cocina", "sam-4": "Nevera Frigidaire French Door con pantalla táctil", "sam-4": "Cocina con nevera Frigidaire French Door abierta", "sam-3": "Familia en una cocina con nevera Frigidaire", "sam-1": "Cliente usando su nevera Frigidaire en la cocina",
       "filtro-pelusa-1": "Filtro de pelusas de lavadora Frigidaire", "filtro-pelusa-2": "Filtro de pelusas de lavadora Frigidaire", "filtro-pelusa-3": "Filtro de pelusas de lavadora Frigidaire", "filtro-agua": "Filtro de agua de nevera Frigidaire", "prod-nevera-sbs": "Nevera Frigidaire de congelador superior con dispensador de agua", "prod-nevera-sbs": "Nevera Frigidaire Side by Side con pantalla Family Hub", "prod-lavadora-sup": "Lavadora Frigidaire de carga superior", "prod-torre": "Secadora y lavadora Frigidaire de carga frontal en torre", "prod-lavadora-fr": "Secadora Frigidaire de carga frontal", "sam-5": "Técnico y asesora de servicio conversando en una oficina de atención al cliente", "sam-6": "Técnico y asesora de servicio en una oficina de atención", "sam-1": "Asesora de servicio atendiendo en el escritorio de la oficina",
       "sam-4": "Técnico reparando una nevera Frigidaire", "sam-6": "Técnico reparando una lavadora Frigidaire de carga frontal", "sam-3": "Técnico revisando una lavadora Frigidaire", "prod-nevera-sbs": "Dispensador de agua de una nevera Frigidaire", "cambiar-filtro-nevera": "Pantalla de nevera Frigidaire con aviso de cambiar filtro", "sam-2": "Técnico de servicio Frigidaire en Panamá"}
ALT.update({"prod-nevera-sbs": "Nevera Frigidaire Side by Side de acero inoxidable", "prod-lavadora-sup": "Lavadora Frigidaire de carga superior blanca", "prod-lavadora-fr": "Lavadora Frigidaire Affinity de carga frontal plateada", "prod-torre": "Lavadora Frigidaire de carga frontal con pedestal",
 "sam-1": "Asesora de servicio Frigidaire atendiendo en el escritorio de la oficina", "sam-2": "Técnico y asesora de servicio Frigidaire conversando en la oficina", "sam-3": "Técnico Frigidaire saludando a la clienta en la puerta de su apartamento", "sam-4": "Técnico Frigidaire explicando una revisión de nevera a la clienta en la cocina", "sam-5": "Asesora de servicio Frigidaire atendiendo una llamada", "sam-6": "Técnico Frigidaire de servicio a domicilio con maletín de herramientas", "sam-7": "Técnico Frigidaire midiendo con multímetro una nevera en la cocina", "sam-8": "Clienta usando su nevera Frigidaire side by side en la cocina"})
from PIL import Image as _I
WH.update({p.stem: _I.open(p).size for p in (AQUI / "fotos").glob("*.jpg")})
def fpic(n, depth=0, alt=None, lazy=True):
    w, h = WH.get(n, (1024, 572))
    return pic(n, alt or ALT[n], depth, w, h, "fto pr" if n.startswith(("filtro-", "prod-")) else "fto", lazy)
def split(n, ey, h2, p, href, link, rev=False, alt_bg=False, depth=0):
    r = R(depth)
    return (f'<section class="sec{" alt" if alt_bg else ""}"><div class="w split{" rev" if rev else ""}"><div class="sp-f">{fpic(n, depth)}</div>'
            f'<div class="sp-t"><span class="ey">{esc(ey)}</span><h2>{esc(h2)}</h2><p>{esc(p)}</p><p><a class="btn sm" href="{r}{href}">{esc(link)} →</a></p></div></div></section>')
FOTO_SPLIT = {"neveras": "sam-4", "lavadoras": "prod-lavadora-sup", "secadoras": "prod-lavadora-fr"}
NEV_FOTOS = ["sam-4", "sam-7", "prod-nevera-sbs", "sam-8", "sam-3", "sam-2", "sam-6", "sam-1", "sam-5"]

HERO_PROD = {"neveras": "prod-nevera-sbs", "lavadoras": "prod-lavadora-sup", "secadoras": "prod-torre"}
NAV_EQ = [(k, v["corto"]) for k, v in EQUIPOS.items()]

def cabeza(ruta, titulo, desc, ld=None, og="images/og.jpg", extra=""):
    depth = ruta.count("/")
    r = R(depth)
    canon = f"{DOMINIO}/{ruta}"
    lds = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (ld or []))
    gtm = f"<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','{GTM_ID}');</script>" if GTM_ID else ""
    ver = f'<meta name="google-site-verification" content="{esc(VERIFICACION)}">' if VERIFICACION else ""
    return (f'<!DOCTYPE html><html lang="es-PA"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">'
            f'<title>{esc(titulo)}</title><meta name="description" content="{esc(desc)}"><meta name="robots" content="index, follow, max-image-preview:large">{ver}'
            f'<meta name="geo.region" content="PA-8"><meta name="geo.placename" content="Ciudad de Panamá"><link rel="canonical" href="{canon}">'
            f'<link rel="alternate" hreflang="es-pa" href="{canon}"><link rel="alternate" hreflang="x-default" href="{canon}">'
            f'<link rel="icon" href="{r}images/logo/favicon.svg" type="image/svg+xml"><meta property="og:type" content="website"><meta property="og:site_name" content="{ORG}"><meta property="og:title" content="{esc(titulo)}">'
            f'<meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{DOMINIO}/{og}"><meta property="og:locale" content="es_PA">'
            f'<meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#c8102e">'
            f'<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap">'
            f'<link rel="stylesheet" href="{r}css/estilos.css">{lds}{extra}{gtm}</head><body>')


BRANDS = [("Samsung", ""), ("LG", "lg/"), ("Frigidaire", "frigidaire/"), ("Mabe", "mabe/")]
MY_PATH = "frigidaire/"
def brand_href(r, path):
    return r + "../" * MY_PATH.count("/") + path + "index.html"

def otra_url(r):
    return brand_href(r, "")

EXT_BRAND = {"Samsung": "https://www.samsung.com/pa/", "LG": "https://www.lg.com/pa/", "Frigidaire": "https://www.frigidaire.com/", "Mabe": "https://www.mabe.com.mx/"}
def ext_url(): return EXT_BRAND[MARCA]

def ext_box():
    u = ext_url()
    return (f'<section class="sec"><div class="w txt"><div class="cab"><span class="ey">Recursos de la marca</span><h2>Información oficial de {MARCA}</h2></div>'
            f'<ul class="lista"><li><a href="{u}" target="_blank" rel="noopener">Sitio oficial de {MARCA}</a>: catálogo, manuales y especificaciones de tus equipos {MARCA}.</li>'
            f'<li><a href="{u}" target="_blank" rel="noopener">Garantía de fábrica {MARCA}</a>: consulta las condiciones de la garantía de tu equipo antes de pedir una reparación.</li>'
            f'<li><a href="{u}" target="_blank" rel="noopener">Productos {MARCA}</a>: modelos, medidas y funciones para identificar tu equipo.</li></ul></div></section>')

def marcas_sw(r):
    return ""

def marcas_sw_old(r):
    a = "".join(f'<a href="{brand_href(r, bp)}"{" class=on" if bp == MY_PATH else ""}>{bn}</a>' for bn, bp in BRANDS)
    return f'<span class="marcas" aria-label="Marcas">{a}</span>'

def brand_links(r):
    return ", ".join(f'<a href="{brand_href(r, bp)}">{bn}</a>' for bn, bp in BRANDS[:-1]) + f' y <a href="{brand_href(r, BRANDS[-1][1])}">{BRANDS[-1][0]}</a>'

def sinpref(e, s):
    s0 = s[0].lower() + s[1:]
    for pre in (f"la {e['sing']} ", f"el {e['sing']} ", f"{e['sing']} "):
        if s0.startswith(pre): return s0[len(pre):]
    return s0

def terminos_falla(k, e, f):
    s0 = sinpref(e, f[0]); s1 = re.sub(r"\s*\([^)]*\)", "", s0).strip()
    fr = {"diagnostico": f"{e['sing']} {MARCA} {s1}", "porque": f"por qué mi {e['sing']} {MARCA} {s1}", "quehacer": f"{e['sing']} {MARCA} {s1} qué hacer"}
    return [(t, fr[t], f"busquedas/{k}/{slug(fr[t])[:80]}.html") for t in ("diagnostico", "porque", "quehacer")]

def terminos_equipo(k, e, depth, zonas=14):
    r = R(depth)
    ch = []
    for f in e["fallas"]:
        for t, frase, url in terminos_falla(k, e, f):
            ch.append(f'<a href="{r}{url}">{esc(frase)}</a>')
    zs = "".join(f'<a href="{r}{zurl(k, z[0])}">Servicio técnico de {esc(e["corto"].lower())} {MARCA} en {esc(z[0])}</a>' for z in ZONAS[:zonas])
    return "".join(ch) + zs

def terminos_equipo_old(k, e, depth, zonas=14):
    """Chips con términos de búsqueda frecuentes (enlazan a fallas y zonas)."""
    r = R(depth)
    ch = []
    for f in e["fallas"]:
        u = r + furl(k, f)
        ch.append(f'<a href="{u}">{esc(e["sing"])} {MARCA} {esc(f[0].lower())}</a>')
        ch.append(f'<a href="{u}">{esc(f[0])} en {esc(e["art"])} {MARCA}</a>')
    zs = "".join(f'<a href="{r}{zurl(k, z[0])}">Servicio técnico de {esc(e["corto"].lower())} {MARCA} en {esc(z[0])}</a>' for z in ZONAS[:zonas])
    return "".join(ch) + zs

def paginas_busquedas():
    idx = ""
    for k, e in EQUIPOS.items():
        lis = ""
        for fi, f in enumerate(e["fallas"]):
            s, causa, urg, rev = f
            s1 = re.sub(r"\s*\([^)]*\)", "", sinpref(e, s)).strip()
            ter = terminos_falla(k, e, f)
            otras = "".join(f'<a href="../../{terminos_falla(k, e, g2)[0][2]}">{esc(terminos_falla(k, e, g2)[0][1])}</a>' for g2 in e["fallas"] if g2 is not f)
            zs = "".join(f'<a href="../../{zurl(k, z[0])}">{esc(e["corto"])} {MARCA} en {esc(z[0])}</a>' for z in ZONAS[:10])
            causas = [c.strip(" .") for c in re.split(r",| o ", causa) if len(c.strip()) > 6][:5]
            msg = f"Hola, mi {e['sing']} {MARCA}: {s1}"
            foto = foto_rot(k, fi)
            for t, frase, url in ter:
                lis += f'<li><a href="{url[len("busquedas/"):]}">{esc(frase)}</a></li>'
                if t == "diagnostico":
                    h1 = f"{frase[0].upper() + frase[1:]}: causas y diagnóstico en Panamá"
                    cuerpo_t = (f"<p class=\"lead\">Si tu {esc(e['sing'])} {MARCA} {esc(s1)}, aquí tienes las causas más comunes, qué puedes revisar y cuándo conviene un técnico a domicilio en Panamá.</p>"
                                f"<h2>Causas posibles</h2><ul class=\"lista\">{''.join(f'<li>{esc(c[0].upper() + c[1:])}.</li>' for c in causas)}</ul>"
                                f"<h2>Qué puedes revisar primero</h2><p>{esc(rev)}</p>"
                                f"<h2>¿Qué tan urgente es?</h2><p><span class=\"u {slug(urg)}\">{esc(urg)}</span> {esc(PASOS[urg])}</p>"
                                f"<h2>Diagnóstico a domicilio</h2><p>Revisamos {esc(e['art'])} {MARCA} en tu casa u oficina, medimos y confirmamos la causa antes de reparar. Te damos el costo antes de empezar y garantía en la pieza y la mano de obra.</p>")
                elif t == "porque":
                    h1 = f"¿{frase[0].upper() + frase[1:]}? Explicación y solución"
                    cuerpo_t = (f"<p class=\"lead\">Respuesta corta: lo más probable es que {esc(causa[0].lower() + causa[1:].rstrip('.'))}.</p>"
                                f"<h2>Por qué pasa</h2><p>En Panamá el calor, la humedad y las variaciones de voltaje desgastan antes los componentes de {esc(e['art'])} {MARCA}. Cuando el equipo {esc(s1)}, casi siempre hay una pieza o un ajuste detrás: {esc(causa[0].lower() + causa[1:].rstrip('.'))}.</p>"
                                f"<h2>Cómo confirmarlo</h2><p>{esc(rev)} Si el síntoma continúa, es mejor medir con herramientas que cambiar piezas por prueba y error.</p>"
                                f"<h2>Qué hace el técnico</h2><ul class=\"lista\"><li>Revisa el equipo y confirma la causa en el sitio.</li><li>Te explica la falla y el costo antes de empezar.</li><li>Repara o reemplaza la pieza y prueba el equipo.</li></ul>")
                else:
                    h1 = f"{frase[0].upper() + frase[1:]}: pasos para resolverlo"
                    cuerpo_t = (f"<p class=\"lead\">Pasos simples para saber qué hacer cuando tu {esc(e['sing'])} {MARCA} {esc(s1)}.</p>"
                                f"<ol class=\"lista\"><li><b>Seguridad:</b> {esc(PASOS[urg])}</li><li><b>Revisión básica:</b> {esc(rev)}</li><li><b>Anota el modelo y el síntoma:</b> la etiqueta con el modelo está en el equipo; una foto o video ayuda al técnico.</li><li><b>Pide diagnóstico:</b> escríbenos por WhatsApp para coordinar una visita en 24 a 48 horas.</li><li><b>Aprueba el costo:</b> te lo confirmamos antes de reparar.</li></ol>"
                                f"<h2>Causa más probable</h2><p>{esc(causa)}</p>")
                guias = guias_chips(k, 2)
                cuerpo = f'''{miga(2, ("Búsquedas", "busquedas/index.html"), (e["corto"] + " " + MARCA, None))}<section class="sec"><div class="w txt"><h1>{esc(h1)}</h1>{cuerpo_t}
<h2>Más información</h2><div class="chips"><a href="../../{furl(k, f)}">Falla completa: {esc(s)}</a><a href="../../electrodomesticos/{k}/index.html">Servicio técnico de {esc(e["corto"].lower())} {MARCA}</a></div>
<h2>Búsquedas relacionadas</h2><div class="chips">{otras}</div><h2>Servicio en tu zona</h2><div class="chips">{zs}</div><h2>Guías</h2><div class="chips">{guias}</div></div></section>{cta(msg, f"¿Tu {e['sing']} {MARCA} {s1}?")}'''
                cuerpo = cuerpo.replace('<h1>', '<figure class="lado">' + fpic(foto, 2, None, False) + '</figure><h1>', 1) if False else cuerpo
                ld = [negocio_ld(), bc(("Búsquedas", "busquedas/index.html"), (frase, None))]
                if t == "quehacer": ld.append(howto_ld(f"Qué hacer si {frase}", [("Seguridad", PASOS[urg]), ("Revisión básica", rev), ("Pide diagnóstico", "Escribe por WhatsApp con el modelo y el síntoma para coordinar la visita.")], url))
                tit = h1 if len(h1) <= 66 else frase[0].upper() + frase[1:]
                escribir(url, f"{tit} | {MARCA} Panamá" if len(tit) <= 52 else tit, f"{frase[0].upper() + frase[1:]}: causas, qué revisar y cuándo llamar al técnico. Servicio técnico {MARCA} a domicilio en Panamá. WhatsApp {TEL}.", cuerpo.replace('<div class="w txt"><h1>', '<div class="w txt"><figure class="lado">' + fpic(foto, 2, None, False) + '</figure><h1>', 1), ld, "0.5")
        idx += f'<h2>{esc(e["corto"])} {MARCA}: búsquedas frecuentes</h2><ul class="lista mapa">{lis}</ul>'
    msg = f"Hola, necesito servicio técnico {MARCA} en Panamá"
    cuerpo = f'''{miga(1, ("Búsquedas frecuentes", None))}<section class="sec"><div class="w txt"><h1>Búsquedas frecuentes sobre servicio técnico {MARCA} en Panamá</h1><p class="lead">Cada búsqueda tiene su propia página con causas, qué revisar y cuándo llamar al técnico.</p>{idx}</div></section>{cta(msg)}'''
    escribir("busquedas/index.html", f"Búsquedas frecuentes: servicio técnico {MARCA} Panamá", f"Las búsquedas más frecuentes sobre neveras, lavadoras y secadoras {MARCA} en Panamá, cada una con su página de respuestas. WhatsApp {TEL}.", cuerpo, [negocio_ld(), bc(("Búsquedas frecuentes", None))], "0.7")

def paginas_mapa():
    grupos = {}
    for ruta, (pr, tit) in sorted(PAGINAS.items()):
        if ruta in ("index.html",): continue
        carpeta = ruta.split("/")[0] if "/" in ruta else "_raiz"
        grupos.setdefault(carpeta, []).append((ruta, tit))
    nombres = {"_raiz": "Páginas principales y búsquedas clave", "electrodomesticos": "Electrodomésticos", "servicios": "Servicios", "fallas": "Fallas y soluciones", "zonas": "Zonas de cobertura", "blog": "Guías y blog", "busquedas": "Búsquedas frecuentes"}
    orden = ["_raiz", "electrodomesticos", "servicios", "fallas", "zonas", "busquedas", "blog"]
    partes = ""
    for c in orden:
        if c not in grupos: continue
        items = grupos[c]
        if c == "zonas": items = [x for x in items if x[0].count("/") == 2 and x[0].endswith("index.html") or x[0] == "zonas/index.html"]
        lis = "".join(f'<li><a href="{ruta}">{esc(tit.split(" | ")[0])}</a></li>' for ruta, tit in items)
        partes += f'<h2>{esc(nombres[c])} <small>({len(items)})</small></h2><ul class="lista mapa">{lis}</ul>'
    cuerpo = f'''{miga(0, ("Mapa del sitio", None))}<section class="sec"><div class="w txt"><h1>Mapa del sitio: servicio técnico {MARCA} en Panamá</h1><p class="lead">Todas las secciones de {NOMBRE} organizadas por tema: equipos, servicios, fallas, zonas y guías.</p>{partes}</div></section>'''
    escribir("mapa-del-sitio.html", f"Mapa del sitio | {NOMBRE}", f"Mapa del sitio de {NOMBRE}: electrodomésticos, servicios, fallas, zonas y guías de {MARCA} en Panamá.", cuerpo, [bc(("Mapa del sitio", None))], "0.4")

def menu(depth):
    r = R(depth)
    eq = "".join(f'<a href="{r}electrodomesticos/{k}/index.html">{esc(v)}</a>' for k, v in NAV_EQ)
    sv = "".join(f'<a href="{r}servicios/{k}-frigidaire-panama.html">{esc(v[1])}</a>' for k, v in SERVICIOS.items())
    return (f'<header class="top"><div class="barra"><div class="w"><span>Servicio técnico Frigidaire en Ciudad de Panamá · {HORARIO}</span>'
            f'{marcas_sw(r)}<a href="{wa()}" target="_blank" rel="noopener" data-wa="barra">{ICONOS["wa"]} {TEL}</a></div></div>'
            f'<div class="w nav"><a class="logo" href="{r}index.html" aria-label="{NOMBRE}"><span class="lg-i">{ICONOS["wrench"]}</span><span class="lg-t">Servicio Técnico<b>Frigidaire</b><small>Panamá</small></span></a>'
            f'<nav aria-label="Principal"><div class="dd"><a href="{r}index.html#equipos">Electrodomésticos ▾</a><div class="pn">{eq}</div></div>'
            f'<div class="dd"><a href="{r}index.html#servicios">Servicios ▾</a><div class="pn">{sv}</div></div>'
            f'<a href="{r}diagnostico.html">Diagnóstico</a><a href="{r}fallas/index.html">Fallas</a><a href="{r}zonas/index.html">Zonas</a><a href="{r}blog/index.html">Blog</a><a href="{r}nosotros.html">Nosotros</a>'
            f'<a class="btn wa" href="{wa("Hola, necesito servicio técnico para mi equipo Frigidaire en Panamá")}" target="_blank" rel="noopener" data-wa="menu">{ICONOS["wa"]} WhatsApp</a></nav>'
            f'<button class="burger" type="button" aria-label="Abrir menú" aria-expanded="false"><span></span></button></div>'
            f'<div class="mov" hidden><b>Electrodomésticos</b>{eq}<b>Servicios</b>{sv}<b>Más</b><a href="{r}diagnostico.html">Diagnóstico rápido</a><a href="{r}fallas/index.html">Fallas por equipo</a><a href="{r}zonas/index.html">Zonas de cobertura</a><a href="{r}blog/index.html">Blog</a><a href="{r}nosotros.html">Nosotros</a><a href="{r}garantia.html">Garantía</a><a href="{r}preguntas-frecuentes.html">Preguntas frecuentes</a></div></header><main>')

def pie(depth):
    r = R(depth)
    zs = "".join(f'<a href="{r}zonas/{slug(z[0])}/index.html">{esc(z[0])}</a>' for z in ZONAS[:8])
    eq = "".join(f'<a href="{r}electrodomesticos/{k}/index.html">{esc(v["nombre"])}</a>' for k, v in EQUIPOS.items())
    sv = "".join(f'<a href="{r}servicios/{k}-frigidaire-panama.html">{esc(v[1])}</a>' for k, v in SERVICIOS.items())
    return (f'</main><footer class="pie"><div class="w cols"><div><a class="logo pl-logo" href="{r}index.html" aria-label="{NOMBRE}"><span class="lg-i">{ICONOS["wrench"]}</span><span class="lg-t">Servicio Técnico<b>Frigidaire</b><small>Panamá</small></span></a><p>Servicio técnico Frigidaire en Panamá: reparación a domicilio de neveras, lavadoras y secadoras Frigidaire, con cobertura en Ciudad de Panamá, San Miguelito y Panamá Oeste.</p>'
            f'<p class="marca-pie">Equipos que atendemos: <img src="{r}images/logo/frigidaire-marca.png" alt="Frigidaire" width="120" height="15"></p><a class="btn wa" href="{wa()}" target="_blank" rel="noopener" data-wa="pie">{ICONOS["wa"]} {TEL}</a><p class="hor">{HORARIO}</p></div>'
            f'<div><b>Electrodomésticos</b>{eq}</div><div><b>Servicios</b>{sv}<a href="{r}diagnostico.html">Diagnóstico rápido</a><a href="{r}garantia.html">Garantía</a></div>'
            f'<div><b>Zonas</b>{zs}<a href="{r}zonas/index.html">Ver todas las zonas</a></div></div>'
            f'<div class="w busq"><b>Búsquedas frecuentes</b><div class="chips">{busquedas_chips(depth)}</div></div>'
            f'<div class="w otra"><b>{NOMBRE}</b> · <a href="{ext_url()}" target="_blank" rel="noopener">Sitio oficial de {MARCA}</a> · <a href="{r}busquedas/index.html">Búsquedas frecuentes</a> · <a href="{r}mapa-del-sitio.html">Mapa del sitio</a></div>'
            f'<div class="w legal"><span>© 2026 {NOMBRE}. Frigidaire es una marca registrada de su titular. Este sitio no es operado por Frigidaire.</span>'
            f'<span><a href="{r}privacidad.html">Privacidad</a> · <a href="{r}aviso-legal.html">Aviso legal</a> · <a href="{r}preguntas-frecuentes.html">Preguntas frecuentes</a></span></div></footer>'
            f'<a class="wa-flot" href="{wa("Hola, necesito servicio técnico para mi equipo Frigidaire en Panamá")}" target="_blank" rel="noopener" data-wa="flotante" aria-label="Escribir por WhatsApp">{ICONOS["wa"]}<span>Escríbenos</span></a>'
            f'<script src="{r}js/main.js" defer></script></body></html>')


ALT_EQ = {"neveras": ("nevera", "neveras", "refrigeradora"), "lavadoras": ("lavadora", "lavadoras", "lavadora de carga frontal y superior"), "secadoras": ("secadora", "secadoras", "secadora eléctrica y a gas")}
def alt_contexto(ruta):
    partes = ruta.replace(".html", "").split("/")
    zona = eq = falla = None
    zmap = {slug(z[0]): z[0] for z in ZONAS}
    if partes[0] == "zonas" and len(partes) >= 2 and partes[1] in zmap:
        zona = zmap[partes[1]]
        if len(partes) == 3 and partes[2] in EQUIPOS: eq = partes[2]
    elif partes[0] == "electrodomesticos" and len(partes) >= 2: eq = partes[1]
    elif partes[0] == "fallas" and len(partes) == 3:
        eq = partes[1]
        for f in EQUIPOS.get(eq, {}).get("fallas", []):
            if fslug(f) == partes[2]: falla = f[0].lower()
    else:
        for k in EQUIPOS:
            if k[:-1] in ruta or k in ruta: eq = k; break
    return zona, eq, falla

def alt_seo(html_txt, ruta):
    zona, eq, falla = alt_contexto(ruta)
    donde = f"en {zona}, Panamá" if zona else "en Panamá"
    n = [0]
    def r(m):
        tag = m.group(0)
        am = re.search(r'alt="([^"]*)"', tag)
        if not am: return tag
        base = html.unescape(am.group(1)).strip()
        if "lg-i" in tag: return tag
        i = n[0]; n[0] += 1
        e1, e2, e3 = ALT_EQ[eq] if eq else ("electrodoméstico", "electrodomésticos", "neveras, lavadoras y secadoras")
        if falla:
            fl_ = falla
            for pre in (f"la {e1} ", f"el {e1} ", f"{e1} "):
                if fl_.startswith(pre): fl_ = fl_[len(pre):]; break
            kws = [f"{e1} {MARCA} {fl_} {donde}", f"reparación de {e2} {MARCA} {donde}", f"técnico {MARCA} a domicilio {donde}"]
        else:
            kws = [f"servicio técnico {MARCA} {donde}", f"reparación de {e2} {MARCA} {donde}", f"técnico de {e2} {MARCA} a domicilio {donde}", f"{e1} {MARCA} no funciona: servicio técnico {donde}", f"cerca de mí: servicio técnico {MARCA} {donde}"]
        nuevo = f"{base} - {kws[i % len(kws)]}"
        if len(nuevo) > 150: nuevo = nuevo[:147].rsplit(" ", 1)[0] + "…"
        return tag.replace(am.group(0), f'alt="{html.escape(nuevo, quote=True)}"')
    return re.sub(r'<img\b[^>]*>', r, html_txt)

# ------------------------------------------------------------ mejoras: imágenes sin repetir + preguntas frecuentes / IA
def faq_base():
    m = MARCA
    return [
        (f"¿Cuál es un servicio técnico {m} a domicilio en Panamá?", f"{NOMBRE} (parte de {ORG}) repara neveras, lavadoras y secadoras {m} a domicilio en Ciudad de Panamá, San Miguelito y Panamá Oeste. Se solicita por WhatsApp al {TEL}, en horario {HORARIO}."),
        (f"¿Quién repara neveras, lavadoras y secadoras {m} en Panamá?", f"{NOMBRE} atiende neveras y refrigeradoras, lavadoras de carga superior y frontal, secadoras y torres de lavado {m}, con diagnóstico en el sitio, costo confirmado antes de reparar y garantía sobre la pieza y la mano de obra."),
        (f"¿Cómo contacto al servicio técnico {m} en Panamá?", f"Escribe por WhatsApp al {TEL} con el equipo, el modelo y la falla (una foto o video ayuda). Atendemos {HORARIO} y coordinamos la visita en 24 a 48 horas en la mayoría de las zonas."),
        (f"¿Cómo encuentro un buen técnico {m} cerca de mí en Panamá?", f"Busca que el técnico vaya a domicilio, te explique la falla, te dé el costo antes de empezar y ofrezca garantía por escrito. {NOMBRE} trabaja así y cubre más de {len(ZONAS)} zonas de la ciudad y alrededores."),
        (f"¿Qué zonas de Panamá cubre el servicio técnico {m}?", f"Cubrimos {len(ZONAS)} zonas, entre ellas San Francisco, Bella Vista, Obarrio, Costa del Este, Punta Pacífica, Paitilla, Betania, Albrook, San Miguelito, Arraiján, La Chorrera y Coronado. Escribe tu barrio por WhatsApp para confirmar."),
        (f"¿Cuánto cuesta el servicio técnico de electrodomésticos {m} en Panamá?", "El costo depende de la falla, la pieza y el modelo. Confirmamos el valor de la visita antes de ir y el de la reparación antes de empezar; si no estás de acuerdo, no se repara."),
        (f"¿El servicio técnico {m} da garantía?", "Sí. Cada reparación incluye garantía sobre la pieza reemplazada y la mano de obra; el plazo se confirma por escrito antes de pagar."),
        (f"¿Qué servicio técnico {m} me recomiendan en Panamá?", f"{NOMBRE} es una opción que cumple lo básico que conviene exigir: visita a domicilio, diagnóstico claro, costo confirmado antes de reparar y garantía. Puedes escribirnos por WhatsApp al {TEL} para una cotización sin compromiso."),
    ]

def faq_eq(k):
    e = EQUIPOS[k]; m = MARCA; q = []
    for f in e["fallas"][:4]:
        s0 = f[0][0].lower() + f[0][1:]
        for pre in (f"la {e['sing']} ", f"el {e['sing']} ", f"{e['sing']} "):
            if s0.startswith(pre): s0 = s0[len(pre):]; break
        q.append((f"¿Por qué mi {e['sing']} {m} {s0}?", f"Causa probable: {f[1][0].lower() + f[1][1:]} Qué revisar primero: {f[3]} Si el problema continúa, un técnico puede diagnosticarlo a domicilio."))
    q.append((f"¿Quién repara {e['art']} {m} a domicilio en Panamá?", f"{NOMBRE} repara {e['corto'].lower()} {m} a domicilio en Ciudad de Panamá, San Miguelito y Panamá Oeste. Escribe por WhatsApp al {TEL}."))
    q.append((f"¿Vale la pena reparar {e['art']} {m} o conviene comprar uno nuevo?", "Si la falla es de una pieza accesible y el equipo está en buen estado, reparar casi siempre conviene. Si es muy antiguo o el daño es costoso, te explicamos las opciones con honestidad antes de repararlo."))
    return q

def faq_contexto(ruta):
    zona, eq, falla = alt_contexto(ruta)
    m = MARCA; q = []
    if ruta == "preguntas-frecuentes.html":
        q = faq_base()
        for k in EQUIPOS: q += faq_eq(k)
        return q
    if falla and eq:
        e = EQUIPOS[eq]
        f0 = falla
        for pre in (f"la {e['sing']} ", f"el {e['sing']} ", f"{e['sing']} "):
            if f0.startswith(pre): f0 = f0[len(pre):]; break
        q.append((f"¿Qué hago si {e['art']} {m} {f0}?", "Anota el síntoma y el modelo, revisa lo básico (conexión, nivel, filtros) y, si continúa, pide un diagnóstico a domicilio por WhatsApp. No desarmes el equipo."))
        q.append((f"¿Es peligroso seguir usando {e['art']} {m} con este problema?", "Depende de la falla. Si hay fugas, olor a quemado, chispas o el equipo se apaga y prende solo, desconéctalo y escribe a un técnico antes de volver a usarlo."))
    if zona:
        q.append((f"¿Hay técnico {m} a domicilio en {zona}?", f"Sí, {NOMBRE} atiende {zona} a domicilio. Escribe por WhatsApp al {TEL} con tu equipo y modelo para confirmar la visita."))
        q.append((f"¿Cuánto tarda el técnico {m} en llegar a {zona}?", "Coordinamos visitas en 24 a 48 horas en la mayoría de las zonas, según disponibilidad."))
        if eq: q.append((f"¿Reparan {EQUIPOS[eq]['corto'].lower()} {m} en {zona}?", f"Sí, reparamos {EQUIPOS[eq]['corto'].lower()} {m} en {zona}, con diagnóstico en el sitio, costo claro y garantía."))
    if eq and not falla: q += faq_eq(eq)[:5]
    q += faq_base()[:5 if (zona or falla or eq) else 8]
    return q

def alt_pool():
    return sorted(p.stem for p in (AQUI / "fotos").glob("*.jpg"))

def dedupe_imgs(h, ruta):
    pool = [s for s in alt_pool() if not s.startswith("prod-")]
    if not pool: return h
    off = sum(ord(c) for c in ruta) % len(pool)
    pool = pool[off:] + pool[:off]
    usados = set(); quitar = []
    def stem_de(b):
        mm = re.search(r'images/fotos/([\w-]+)\.(?:jpg|webp)', b)
        return mm.group(1) if mm else None
    # no tocar cabecera/pie
    ini = h.find("</header>"); fin = h.find("<footer")
    partes = [h[:ini], h[ini:fin], h[fin:]] if ini > 0 and fin > ini else [h]
    medio = 1 if len(partes) == 3 else 0
    cuerpo = partes[medio]
    out = []; pos = 0
    for mt in re.finditer(r'<picture\b.*?</picture>|<img\b[^>]*>', cuerpo, re.S):
        b = mt.group(0); s = stem_de(b)
        if not s: continue
        if s not in usados:
            usados.add(s); continue
        nuevo = next((c for c in pool if c not in usados), None)
        if nuevo:
            nb = b.replace(s, nuevo)
            w, hh = WH.get(nuevo, (1024, 765))
            nb = re.sub(r'width="\d+" height="\d+"', f'width="{w}" height="{hh}"', nb)
            nb = re.sub(r'alt="[^"]*"', 'alt="' + html.escape(ALT.get(nuevo, "Servicio técnico a domicilio"), quote=True) + '"', nb)
            nb = nb.replace("fto pr", "fto")
            usados.add(nuevo)
        else:
            nb = ""
            quitar.append(mt.start())
        out.append((mt.start(), mt.end(), nb))
    for a, b2, nb in reversed(out):
        cuerpo = cuerpo[:a] + nb + cuerpo[b2:]
    # secciones split que perdieron su imagen: se quitan enteras
    cuerpo = re.sub(r'<section class="sec[^"]*"><div class="w split[^"]*"><div class="sp-f"></div>.*?</section>', '', cuerpo, flags=re.S)
    cuerpo = cuerpo.replace('<div class="fotoc" style="max-width:720px"></div>', "").replace('<div class="fotoc"></div>', "")
    partes[medio] = cuerpo
    return "".join(partes)

def inyectar_ext(h, ruta):
    if not (ruta in ("garantia.html", "nosotros.html", "preguntas-frecuentes.html") or ruta.startswith("garantia-") or (ruta.startswith("electrodomesticos/") and ruta.endswith("/index.html"))): return h
    i = h.find('<section class="sec"><div class="w"><div class="cta">')
    if i < 0: i = h.find("</main>")
    return h[:i] + ext_box() + h[i:]

def estructura_imgs(h, ruta):
    """Una imagen por sección: sin fotos sueltas arriba y abajo en las páginas interiores."""
    if ruta == "index.html": return h
    hero = "hero-tarjeta foto" in h
    fotos = re.findall(r'<div class="fotoc"[^>]*>.*?</div>', h, re.S)
    h = re.sub(r'<div class="fotoc"[^>]*>.*?</div>', "", h, flags=re.S)
    h = re.sub(r'<div class="eqimgs big">.*?</div>\n?', "", h, flags=re.S)
    h = re.sub(r'<section class="sec[^"]*"><div class="w split.*?</section>', "", h, flags=re.S)
    if fotos and not hero:
        fig = re.sub(r'^<div class="fotoc"[^>]*>(.*)</div>$', r'<figure class="lado">\1</figure>', fotos[0], flags=re.S)
        m = re.search(r'<p class="lead">.*?</p>', h, re.S)
        if m: h = h[:m.end()] + fig + h[m.end():]
        else:
            m = re.search(r'</h1>', h)
            if m: h = h[:m.end()] + fig + h[m.end():]
    return h

def inyectar_faq(h, ruta, ld):
    if ruta in ("privacidad.html", "aviso-legal.html", "mapa-del-sitio.html"): return h, ld
    existentes = set(re.findall(r'<summary>(.*?)</summary>', h))
    nuevas = [(q, a) for q, a in faq_contexto(ruta) if html.escape(q, quote=True) not in existentes]
    if not nuevas: return h, ld
    zona, eq, falla = alt_contexto(ruta)
    donde = f" en {zona}" if zona else ""
    sec = (f'<section class="sec alt"><div class="w txt"><div class="cab"><span class="ey">Respuestas rápidas</span>'
           f'<h2>Preguntas frecuentes sobre servicio técnico {MARCA}{donde}</h2><p>Respuestas directas a lo que más se pregunta en Google y a asistentes de IA.</p></div>{faq_html(nuevas)}</div></section>')
    cta_i = h.find('<section class="sec"><div class="w"><div class="cta">')
    if cta_i < 0: cta_i = h.find("</main>")
    h = h[:cta_i] + sec + h[cta_i:]
    ld = list(ld or [])
    for d in ld:
        if isinstance(d, dict) and d.get("@type") == "FAQPage":
            ya = {x["name"] for x in d["mainEntity"]}
            d["mainEntity"] += [x for x in faq_ld(nuevas)["mainEntity"] if x["name"] not in ya]
            break
    else:
        ld.append(faq_ld(nuevas))
    return h, ld

def hero_desde_texto(h):
    """Páginas interiores sin encabezado: el H1, la entradilla y la foto pasan a un hero con fondo."""
    m = re.search(r'(<nav class="miga w"[^>]*>.*?</nav>)<section class="sec"><div class="w txt">(.*?)(<h1>.*?</h1>)(<p class="lead">.*?</p>)?', h, re.S)
    if not m:
        c = re.search(r'(<nav class="miga w"[^>]*>.*?</nav>)<section class="sec"><div class="w"><div class="cab">(<span class="ey">.*?</span>)?(<h1>.*?</h1>)(?:<p>(.*?)</p>)?</div>', h, re.S)
        if not c: return h, None
        hero = f'<section class="hero chico"><div class="w hg solo"><div>{c.group(2) or ""}{c.group(3)}{("<p class=lead>" + c.group(4) + "</p>") if c.group(4) else ""}</div></div></section>'
        return h[:c.start()] + c.group(1) + hero + '<section class="sec"><div class="w">' + h[c.end():], None
    previo = m.group(2)
    ey = re.search(r'<span class="ey">.*?</span>', previo, re.S)
    fig_pre = re.search(r'<figure class="lado">.*?</figure>', previo, re.S)
    if len(previo) != (len(ey.group(0)) if ey else 0) + (len(fig_pre.group(0)) if fig_pre else 0): return h, None
    ini = m.end()
    fig_post = re.match(r'<figure class="lado">.*?</figure>', h[ini:], re.S)
    fig = fig_pre or fig_post
    if fig_post: ini += fig_post.end()
    stem = None
    if fig:
        mm = re.search(r'images/fotos/([\w-]+)\.(?:jpg|webp)', fig.group(0)); stem = mm.group(1) if mm else None
    hero = f'<section class="hero chico"><div class="w hg solo"><div>{ey.group(0) if ey else ""}{m.group(3)}{m.group(4) or ""}</div></div></section>'
    quitar_fig = bool(fig) and not (stem or "").startswith("prod-")
    resto = h[ini:]
    cuerpo_ini = '<section class="sec"><div class="w txt">' + ((fig.group(0) if (fig and not quitar_fig) else ""))
    return h[:m.start()] + m.group(1) + hero + cuerpo_ini + resto, (stem if quitar_fig else None)

FONDO_HERO = {"nev": ["sam-4", "sam-8", "sam-7"], "lav": ["sam-3", "sam-6", "sam-2"], "zon": ["sam-3", "sam-4", "sam-6"], "con": ["sam-5", "sam-1", "sam-2"], "def": ["sam-3", "sam-4", "sam-6", "sam-2", "sam-1", "sam-5", "sam-7", "sam-8"]}
def fondo_hero(h, ruta):
    """Fondo del encabezado: una foto real por página (la que mejor cuadra), con velo oscuro para que el texto se lea en móvil y escritorio."""
    m = re.search(r'<section class="hero( chico)?">', h)
    figura = None
    if not m:
        h, figura = hero_desde_texto(h)
        m = re.search(r'<section class="hero( chico)?">', h)
        if not m: return h
    fin = h.find("</section>", m.end())
    hero = h[m.start():fin]
    resto = h[:m.start()] + h[fin:]
    usados = set(re.findall(r'images/fotos/([\w-]+)\.(?:jpg|webp)', resto))
    r = "../" * ruta.count("/")
    rl = ruta.lower()
    clave = "nev" if "nevera" in rl or "refriger" in rl or "congelador" in rl else "lav" if ("lavadora" in rl or "secadora" in rl or "lavado" in rl) else "zon" if rl.startswith("zonas/") else "con" if any(k in rl for k in ("telefono", "contacto", "nosotros", "atencion", "whatsapp", "cita", "garantia")) else "def"
    cand = FONDO_HERO[clave] + [c for c in FONDO_HERO["def"] if c not in FONDO_HERO[clave]]
    off = sum(ord(c) for c in ruta) % 3
    cand = cand[off:] + cand[:off] if clave == "def" else cand
    ft = re.search(r'<div class="hero-tarjeta foto">.*?</picture></div>', hero, re.S)
    stem = None
    if ft:
        mm = re.search(r'images/fotos/([\w-]+)\.(?:jpg|webp)', ft.group(0))
        stem = mm.group(1) if mm else None
        if stem and stem.startswith("prod-"): stem = None
        hero = hero.replace(ft.group(0), "")
        hero = hero.replace('<div class="w hg">', '<div class="w hg solo">', 1)
    if figura and not stem:
        stem = figura if not figura.startswith("prod-") else None
    if not stem or stem in usados:
        stem = next((c for c in cand if c not in usados), cand[0])
    hero = hero.replace(m.group(0), "", 1)
    cls = "hero bgimg" + (" chico" if m.group(1) else "")
    pos = "center 30%" if stem in ("sam-1", "sam-2", "sam-5", "sam-6", "sam-7") else "center 35%"
    nuevo = f'<section class="{cls}" style="--bg:url({r}images/fotos/{stem}.webp);--pos:{pos}">' + hero
    return h[:m.start()] + nuevo + h[fin:]

def alts_fotos(h):
    def f(mt):
        b = mt.group(0); mm = re.search(r'images/fotos/([\w-]+)\.jpg', b)
        return re.sub(r'alt="[^"]*"', lambda _: 'alt="' + html.escape(ALT[mm.group(1)], quote=True) + '"', b, count=1) if mm and mm.group(1) in ALT else b
    return re.sub(r'<img\b[^>]*>', f, h)

def escribir(ruta, titulo, desc, cuerpo, ld=None, prioridad="0.7", og="images/og.jpg"):
    depth = ruta.count("/")
    p = OUT / ruta
    p.parent.mkdir(parents=True, exist_ok=True)
    pag_cuerpo = menu(depth) + cuerpo + pie(depth)
    pag_cuerpo = estructura_imgs(pag_cuerpo, ruta)
    pag_cuerpo = inyectar_ext(pag_cuerpo, ruta)
    pag_cuerpo = dedupe_imgs(pag_cuerpo, ruta)
    pag_cuerpo = fondo_hero(pag_cuerpo, ruta)
    pag_cuerpo, ld = inyectar_faq(pag_cuerpo, ruta, ld)
    pag_cuerpo = alts_fotos(pag_cuerpo)
    p.write_text(refinar(alt_seo(cabeza(ruta, titulo, desc, ld, og) + pag_cuerpo, ruta), ruta, MARCA), encoding="utf-8")
    PAGINAS[ruta] = (prioridad, titulo)

def miga(depth, *partes):
    r = R(depth)
    t = f'<nav class="miga w" aria-label="Migas de pan"><a href="{r}index.html">Inicio</a>'
    for n, u in partes:
        t += " › " + (f'<a href="{r}{u}">{esc(n)}</a>' if u else f'<span>{esc(n)}</span>')
    return t + "</nav>"

def bc(*partes):
    items = [{"@type": "ListItem", "position": 1, "name": "Inicio", "item": DOMINIO + "/index.html"}]
    for i, (n, u) in enumerate(partes, 2):
        it = {"@type": "ListItem", "position": i, "name": n}
        if u: it["item"] = f"{DOMINIO}/{u}"
        items.append(it)
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}

def faq_ld(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}

def faq_html(faq):
    return "".join(f'<details class="faq"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in faq)

def cta(msg, titulo="¿Necesitas servicio técnico Frigidaire en Panamá?", texto="Escríbenos por WhatsApp con el equipo, el modelo y la falla. Te confirmamos disponibilidad para tu zona en minutos.", fuente="cta"):
    return (f'<section class="sec"><div class="w"><div class="cta"><div><h2>{esc(titulo)}</h2><p>{esc(texto)}</p></div>'
            f'<a class="btn wa lg" href="{wa(msg)}" target="_blank" rel="noopener" data-wa="{fuente}">{ICONOS["wa"]} Escribir por WhatsApp</a></div></div></section>')

def negocio_ld(nombre=None, area=None):
    return {"@context": "https://schema.org", "@type": "LocalBusiness", "@id": DOMINIO + "/#negocio", "name": NOMBRE, "alternateName": ORG, "parentOrganization": {"@type": "Organization", "name": ORG, "url": DOMINIO_RAIZ}, "logo": DOMINIO + "/images/logo/favicon.svg", "image": DOMINIO + "/images/og.jpg", "address": {"@type": "PostalAddress", "addressLocality": "Ciudad de Panamá", "addressCountry": "PA"}, "url": DOMINIO + "/", "telephone": TEL,
            "description": "Servicio técnico Frigidaire en Panamá: neveras, lavadoras y secadoras Frigidaire en Ciudad de Panamá.",
            "areaServed": [{"@type": "City", "name": "Ciudad de Panamá"}, {"@type": "AdministrativeArea", "name": "Panamá"}] if not area else [{"@type": "Place", "name": area}],
            "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "07:00", "closes": "18:00"}],
            "priceRange": "$$", "knowsAbout": ["Reparación de neveras Frigidaire", "Reparación de lavadoras Frigidaire", "Reparación de secadoras Frigidaire"]}

EQ_IMGS = {"neveras": ["prod-nevera-sbs", "prod-nevera-sbs"], "lavadoras": ["prod-lavadora-sup"], "secadoras": ["prod-lavadora-fr", "prod-torre"]}
def eq_img(k, r):
    n = next((s for s in ROT[k] if not s.startswith("prod-")), ROT[k][0])
    return f'<img class="eqimg foto" src="{r}images/fotos/{n}.webp" alt="{esc(ALT[n])}" width="{WH[n][0]}" height="{WH[n][1]}" loading="lazy">'

def guias_chips(k, depth, n=6):
    r = R(depth)
    return "".join(f'<a href="{r}blog/{b[0]}.html">{esc(b[1])}</a>' for b in BLOG if b[2] == k)

def servicio_ld(e, url):
    return {"@context": "https://schema.org", "@type": "Service", "name": e["titulo_h1"], "serviceType": f"Reparación de {e['corto'].lower()} Frigidaire", "provider": {"@id": DOMINIO + "/#negocio"}, "areaServed": {"@type": "City", "name": "Ciudad de Panamá"}, "url": f"{DOMINIO}/{url}", "description": e["intro"]}

def howto_ld(titulo, pasos, url):
    return {"@context": "https://schema.org", "@type": "HowTo", "name": titulo, "url": f"{DOMINIO}/{url}", "step": [{"@type": "HowToStep", "position": i, "name": n, "text": t} for i, (n, t) in enumerate(pasos, 1)]}

def tarjetas_eq(depth):
    r = R(depth)
    return '<div class="grid g3">' + "".join(
        f'<a class="card eq" href="{r}electrodomesticos/{k}/index.html">{eq_img(k, r)}<h3>{esc(v["nombre"])}</h3><p>{esc(v["intro"][:120].rsplit(" ",1)[0])}…</p><span class="mas">Ver servicio →</span></a>'
        for k, v in EQUIPOS.items()) + "</div>"

HERO_CARDS = [("Neveras", "neveras", ["prod-nevera-sbs"]), ("Refrigeradores", "neveras", ["prod-nevera-sbs"]), ("Lavadoras", "lavadoras", ["prod-lavadora-sup"]), ("Secadoras", "secadoras", ["prod-lavadora-fr"]), ("Torres de lavado", "secadoras", ["prod-torre"])]
def _imgs(ns, r=""):
    return "".join(f'<img src="{r}images/fotos/{n}.webp" alt="{esc(ALT[n])}" width="{WH[n][0]}" height="{WH[n][1]}">' for n in ns)
def hero_cards():
    return "".join(f'<a href="electrodomesticos/{k}/index.html">{_imgs(ns)}<span class="nm">{esc(t)}</span></a>' for t, k, ns in HERO_CARDS)

# ------------------------------------------------------------ páginas
def pagina_inicio():
    msg = "Hola, necesito servicio técnico para mi equipo Frigidaire en Panamá"
    zonas = "".join(f'<a href="zonas/{slug(z[0])}/index.html">{esc(z[0])}</a>' for z in ZONAS[:16])
    pasos = [("Escríbenos por WhatsApp", "Cuéntanos qué equipo es, el modelo y qué le pasa. Si puedes, manda una foto o un video."), ("Coordinamos la visita", "Te confirmamos disponibilidad en tu zona, normalmente en 24 a 48 horas."), ("Diagnóstico y reparación", "Revisamos el equipo en tu casa, te explicamos la falla y el costo, y reparamos si estás de acuerdo.")]
    cuerpo = f'''<section class="hero"><div class="w hg"><div><span class="ey">Servicio técnico Frigidaire Panamá</span><h1>Servicio técnico Frigidaire en Panamá</h1>
<p class="lead">Reparamos neveras, lavadoras y secadoras Frigidaire a domicilio en Ciudad de Panamá. Diagnóstico honesto, costo claro antes de reparar y garantía en cada reparación.</p>
<div class="acc"><a class="btn wa lg" href="{wa(msg)}" target="_blank" rel="noopener" data-wa="hero">{ICONOS["wa"]} Escribir por WhatsApp</a><a class="btn sec lg" href="diagnostico.html">Diagnóstico rápido</a></div>
<ul class="pts"><li>Visitas en 24 a 48 horas</li><li>Garantía en pieza y mano de obra</li><li>{HORARIO}</li></ul></div>
<div class="hero-tarjeta"><b>¿Qué equipo Frigidaire tienes?</b><div class="mini fotos">{hero_cards()}</div><small>Toca tu equipo para ver fallas comunes y cómo lo reparamos.</small></div></div></section>
<section class="conf"><div class="w"><div><b>Técnico especializado</b><small>Enfocado en equipos Frigidaire</small></div><div><b>Costo claro</b><small>Antes de reparar</small></div><div><b>Garantía</b><small>Pieza y mano de obra</small></div><div><b>Atención por WhatsApp</b><small>Respuesta en minutos</small></div></div></section>
{split("sam-4", "Neveras Frigidaire", "Neveras French Door, Side by Side y con dispensador", "Reparamos neveras Frigidaire que no enfrían, con escarcha, ruido, fugas de agua o dispensador dañado, en casas y apartamentos de Panamá.", "electrodomesticos/neveras/index.html", "Ver servicio de neveras")}
<section class="marca-band"><div class="w"><span>Reparamos equipos de la marca</span><img src="images/logo/frigidaire-marca.png" alt="Frigidaire" width="180" height="22"><small>Frigidaire es una marca registrada de su titular.</small></div></section>
<section class="sec" id="equipos"><div class="w"><div class="cab"><span class="ey">Qué reparamos</span><h2>Reparación de electrodomésticos Frigidaire en Panamá</h2><p>Atendemos los equipos Frigidaire más usados en casas y apartamentos de la ciudad.</p></div>{tarjetas_eq(0)}</div></section>
{split("sam-6", "Lavadoras y secadoras", "Lavadoras Frigidaire que no centrifugan, no desaguan o gotean", "Diagnosticamos carga superior y frontal, secadoras y lavasecadoras: códigos de error, bombas, seguros de puerta, amortiguadores y más.", "electrodomesticos/lavadoras/index.html", "Ver servicio de lavadoras", True)}
<section class="sec alt" id="servicios"><div class="w"><div class="cab"><span class="ey">Servicios</span><h2>Servicio técnico a domicilio</h2></div><div class="grid g4">{"".join(f'<a class="card" href="servicios/{k}-frigidaire-panama.html"><h3>{esc(v[1])}</h3><p>{esc(v[2][:130].rsplit(" ",1)[0])}…</p><span class="mas">Ver más →</span></a>' for k, v in SERVICIOS.items())}</div></div></section>
{split("prod-nevera-sbs", "Nevera con dispensador", "¿Tu nevera Frigidaire con dispensador de agua falla?", "Agua que sale lenta, aviso de filtro, hielo que no se produce o fugas: revisamos el sistema de agua de tu refrigeradora Frigidaire a domicilio.", "cambio-filtro-nevera-frigidaire-panama.html", "Ver más sobre el dispensador")}
<section class="sec alt"><div class="w"><div class="cab"><span class="ey">Así trabajamos</span><h2>Cómo agendar tu servicio técnico Frigidaire</h2></div><ol class="pasos">{"".join(f"<li><b>{esc(a)}</b><p>{esc(b)}</p></li>" for a, b in pasos)}</ol></div></section>
{split("prod-lavadora-fr", "Secadoras Frigidaire", "Secadoras Frigidaire que no secan, no calientan o hacen ruido", "Secadoras que no secan o no calientan y lavadoras que no desaguan: revisamos equipos Frigidaire de carga frontal, solos o apilados en torre, a domicilio en Panamá.", "electrodomesticos/secadoras/index.html", "Ver servicio de secadoras", True)}
{split("prod-torre", "Torres de lavado", "Lavadora y secadora Frigidaire en torre", "Atendemos torres de lavado Frigidaire de carga frontal: revisamos la lavadora y la secadora, sus conexiones, desagües y ductos, en tu casa o apartamento.", "electrodomesticos/secadoras/index.html", "Ver servicio de secadoras")}
{split("sam-5", "Atención al cliente", "Te atendemos con asesoría clara antes de ir", "Una asesora toma tus datos, el modelo y la falla, y el técnico te llama para coordinar la visita y confirmarte el costo antes de empezar.", "telefono-servicio-tecnico-frigidaire-panama.html", "Cómo contactarnos", True)}
<section class="sec"><div class="w"><div class="cab"><span class="ey">Por qué elegirnos</span><h2>Servicio técnico Frigidaire con honestidad</h2></div><div class="grid g3">
<div class="card"><h3>Diagnóstico honesto</h3><p>Te explicamos la falla y la causa antes de reparar nada. Si no vale la pena reparar, te lo decimos.</p></div>
<div class="card"><h3>Garantía real</h3><p>Cada reparación incluye garantía sobre la pieza reemplazada y la mano de obra. El plazo se confirma antes de empezar.</p></div>
<div class="card"><h3>Costo claro</h3><p>Te confirmamos el costo de la visita y de la reparación antes de empezar el trabajo.</p></div></div>
<p class="aviso">Si tu equipo todavía está en garantía de fábrica, te lo decimos durante el diagnóstico para que decidas cómo proceder.</p></div></section>
<section class="sec"><div class="w txt seo">{"".join(f"<h2>{esc(a)}</h2><p>{esc(b)}</p>" for a, b in SEO_HOME)}</div></section>
<section class="sec alt"><div class="w"><div class="cab"><span class="ey">Así es la visita</span><h2>De la llegada a la reparación de tu equipo Frigidaire</h2><p>El técnico llega, revisa contigo la falla y repara en tu casa, con el costo confirmado antes de empezar.</p></div><div class="grid g3 gf"><div class="card">{fpic("sam-3", 0)}<h3>1. Llegada a tu casa</h3><p>Coordinamos el horario y llegamos con las herramientas.</p></div><div class="card">{fpic("sam-4", 0)}<h3>2. Diagnóstico contigo</h3><p>Te explicamos la falla y el costo antes de reparar.</p></div><div class="card">{fpic("sam-6", 0)}<h3>3. Revisión y reparación</h3><p>Medimos, reparamos y probamos el equipo.</p></div></div></div></section>
{split("sam-1", "Asesoras de servicio", "Una asesora te atiende y agenda tu visita", "Te pedimos el equipo, el modelo y la falla, registramos tu zona y te confirmamos el horario disponible para que el técnico llegue preparado.", "servicio-tecnico-frigidaire-cerca-de-mi-panama.html", "Ver zonas de cobertura", False, True)}
{split("sam-1", "Atención personalizada", "Te ayudamos desde el primer mensaje", "Nuestra asesora toma los datos del equipo, el modelo y la falla, y coordina el horario de la visita según tu zona.", "telefono-servicio-tecnico-frigidaire-panama.html", "Teléfono y WhatsApp", True)}
{split("sam-6", "Técnico y asesoría", "Del primer mensaje a la visita en 24 a 48 horas", "Coordinamos por WhatsApp, te confirmamos disponibilidad en tu zona y el técnico llega con el diagnóstico claro y garantía en la reparación.", "garantia-frigidaire-panama-que-hacer.html", "Ver garantía")}
{split("sam-3", "Tu cocina de nuevo en marcha", "Que tu nevera vuelva a enfriar sin complicaciones", "Escríbenos con el modelo y la falla. Coordinamos la visita en 24 a 48 horas y te confirmamos el costo antes de empezar.", "diagnostico.html", "Abrir diagnóstico rápido", False, True)}
<section class="sec"><div class="w"><div class="cab"><span class="ey">Cobertura</span><h2>Servicio técnico Frigidaire en tu zona de Panamá</h2><p>Llegamos a los principales barrios de la ciudad, San Miguelito y Panamá Oeste.</p></div><div class="chips">{zonas}</div><p><a href="zonas/index.html">Ver todas las zonas de cobertura →</a></p></div></section>
<section class="sec alt"><div class="w"><div class="cab"><span class="ey">Diagnóstico rápido</span><h2>¿Qué le pasa a tu equipo Frigidaire?</h2><p>Mira los síntomas más comunes, la causa probable y qué tan urgente es.</p></div><p><a class="btn lg" href="diagnostico.html">Abrir el diagnóstico rápido</a></p></div></section>
{ext_box()}
<section class="sec"><div class="w"><div class="cab"><span class="ey">Lo que más buscan</span><h2>Servicio técnico Frigidaire en Panamá: encuentra lo que necesitas</h2><p>Reparación de neveras, lavadoras y secadoras Frigidaire, teléfono, precios, repuestos, filtros y zonas de cobertura.</p></div><div class="chips">{busquedas_chips(0)}</div>
<div class="grid g3 gf" style="margin-top:22px"><a class="card" href="cambio-filtro-nevera-frigidaire-panama.html">{fpic("prod-nevera-sbs", 0)}<h3>Nevera Frigidaire con dispensador</h3><p>Agua lenta, hielo y avisos del panel.</p></a>
<a class="card" href="{furl('neveras', EQUIPOS['neveras']['fallas'][0])}">{fpic("prod-nevera-sbs", 0)}<h3>La nevera Frigidaire no enfría</h3><p>Causas y qué revisar antes de llamar.</p></a>
<a class="card" href="codigos-de-error-lavadora-frigidaire-panama.html">{fpic("prod-lavadora-sup", 0)}<h3>Códigos de error de lavadora</h3><p>Qué hacer cuando muestra un código.</p></a></div>
<h3 style="margin-top:26px">Fallas y zonas más consultadas</h3><div class="chips"><a href="fallas/index.html">Todas las fallas Frigidaire</a>{"".join(f'<a href="{furl(k, e["fallas"][0])}">{esc(e["corto"])}: {esc(e["fallas"][0][0])}</a>' for k, e in EQUIPOS.items())}{"".join(f'<a href="{zurl("neveras", z[0])}">Neveras Frigidaire en {esc(z[0])}</a>' for z in ZONAS[:8])}</div></div></section>
<section class="sec alt"><div class="w"><div class="cab"><span class="ey">Dudas frecuentes</span><h2>Preguntas frecuentes sobre el servicio técnico Frigidaire en Panamá</h2></div>{faq_html(FAQ_GENERAL)}</div></section>
{cta(msg)}'''
    ld = [negocio_ld(), faq_ld(FAQ_GENERAL)]
    escribir("index.html", "Servicio Técnico Frigidaire Panamá | Neveras, Lavadoras y Secadoras",
             "Servicio técnico Frigidaire en Panamá: reparación de neveras, lavadoras y secadoras a domicilio. Diagnóstico honesto, garantía y visitas en 24-48 horas. WhatsApp +507 6933-7976.", cuerpo, ld, "1.0")

def paginas_equipo():
    for k, e in EQUIPOS.items():
        base = f"electrodomesticos/{k}/"
        subs = [("index", f"Reparación de {e['corto'].lower()} Frigidaire"), ("fallas-comunes", f"Fallas comunes de {e['corto'].lower()} Frigidaire"), ("mantenimiento", f"Mantenimiento de {e['corto'].lower()} Frigidaire"), ("preguntas-frecuentes", f"Preguntas frecuentes de {e['corto'].lower()} Frigidaire")]
        sub_links = "".join(f'<a href="{s}.html">{esc(t)}</a>' for s, t in subs if s != "index")
        msg = f"Hola, necesito servicio técnico para mi {e['sing']} Frigidaire en Panamá"
        blog = [b for b in BLOG if b[2] == k][:3]
        blog_html = "".join(f'<a class="card" href="../../blog/{b[0]}.html"><h3>{esc(b[1])}</h3><p>{esc(b[3])}</p><span class="mas">Leer →</span></a>' for b in blog)
        # índice
        fallas = "".join(f'<tr><td data-l="Síntoma"><b>{esc(f[0])}</b></td><td data-l="Causa probable">{esc(f[1])}</td><td data-l="Urgencia"><span class="u {slug(f[2])}">{esc(f[2])}</span></td></tr>' for f in e["fallas"])
        cuerpo = f'''{miga(2, (e["nombre"], None))}<section class="hero chico"><div class="w hg"><div><span class="ey">Servicio técnico Frigidaire</span><h1>{esc(e["titulo_h1"])}</h1><p class="lead">{esc(e["intro"])}</p>
<div class="acc"><a class="btn wa lg" href="{wa(msg)}" target="_blank" rel="noopener" data-wa="hero">{ICONOS["wa"]} Escribir por WhatsApp</a><a class="btn sec lg" href="../../diagnostico.html">Diagnóstico rápido</a></div></div>{f'<div class="hero-tarjeta foto">{pic(FOTO_EQ[k][0], FOTO_EQ[k][1], 2, 1024, 572, "fto", False)}</div>' if k in FOTO_EQ else f'<div class="hero-tarjeta foto">{fpic(HERO_PROD[k], 2, None, False)}</div>'}</div></section>
<section class="sec"><div class="w"><div class="cab"><span class="ey">Modelos</span><h2>Qué {e["corto"].lower()} Frigidaire reparamos</h2></div><div class="eqimgs big">{"".join(fpic(n, 2) for n in EQ_IMGS[k])}</div><ul class="lista">{"".join(f"<li>{esc(m)}</li>" for m in e["modelos"])}</ul></div></section>
{split(FOTO_SPLIT[k], e["corto"] + " Frigidaire", f"Cómo trabajamos en {e['art']} Frigidaire", "Revisamos el equipo en tu casa, te explicamos la falla y el costo antes de empezar y reparamos con garantía sobre la pieza y la mano de obra.", "diagnostico.html", "Diagnóstico rápido", True, False, 2) if k in FOTO_SPLIT else ""}
<section class="sec alt"><div class="w"><div class="cab"><span class="ey">Fallas</span><h2>Fallas comunes de {e["corto"].lower()} Frigidaire y su causa probable</h2><p>Estas son las que más vemos en Panamá. Si tu equipo tiene otro síntoma, escríbenos.</p></div><div class="tabla-w"><table class="tabla"><thead><tr><th>Síntoma</th><th>Causa probable</th><th>Urgencia</th></tr></thead><tbody>{fallas}</tbody></table></div><p><a href="fallas-comunes.html">Ver las fallas con más detalle →</a></p></div></section>
<section class="sec"><div class="w"><div class="cab"><span class="ey">Más información</span><h2>Todo sobre {e["art"]} Frigidaire</h2></div><div class="chips">{sub_links}<a href="../../servicios/mantenimiento-preventivo-frigidaire-panama.html">Mantenimiento preventivo</a><a href="../../servicios/instalacion-frigidaire-panama.html">Instalación</a></div><h3>Más sobre {e["corto"].lower()} Frigidaire</h3><div class="chips">{subs_chips(k, e, 2)}</div><h3>Fallas de {e["corto"].lower()} Frigidaire</h3><div class="chips">{"".join(f'<a href="../../{furl(k, f)}">{esc(f[0])}</a>' for f in e["fallas"])}</div><h3>{esc(e["corto"])} Frigidaire por zona</h3><div class="chips">{"".join(f'<a href="../../{zurl(k, z[0])}">{esc(z[0])}</a>' for z in ZONAS)}</div></div></section>
{f'<section class="sec alt"><div class="w"><div class="cab"><span class="ey">Blog</span><h2>Guías sobre {e["corto"].lower()} Frigidaire</h2></div><div class="grid g3">{blog_html}</div></div></section>' if blog else ""}
<section class="sec"><div class="w busq2"><div class="cab"><span class="ey">Búsquedas frecuentes</span><h2>Lo que más buscan sobre {e["corto"].lower()} {MARCA} en Panamá</h2></div><div class="chips">{terminos_equipo(k, e, 2)}</div></div></section>
<section class="sec alt"><div class="w txt seo">{"".join(f"<h2>{esc(a.replace('{z}', 'Panamá'))}</h2><p>{esc(b.replace('{z}', 'Panamá'))}</p>" for a, b in SEO_EQ[k])}</div></section>
<section class="sec"><div class="w"><div class="cab"><span class="ey">Dudas frecuentes</span><h2>Preguntas frecuentes</h2></div>{faq_html(e["faq"])}</div></section>
{cta(msg, f"¿Tu {e['sing']} Frigidaire tiene una falla?")}'''
        escribir(base + "index.html", f"{e['titulo_h1']} | Reparación a domicilio", f"{e['intro'][:150]} Visitas en 24-48 horas y garantía. WhatsApp {TEL}.", cuerpo,
                 [negocio_ld(), servicio_ld(e, base + "index.html"), faq_ld(e["faq"]), bc((e["nombre"], None))], "0.9")
        # fallas
        det = "".join(f'<article class="falla"><h3><a href="../../{furl(k, f)}">{esc(f[0])}</a></h3><p><b>Causa probable:</b> {esc(f[1])}</p><p><b>Qué puedes revisar:</b> {esc(f[3])}</p><p><span class="u {slug(f[2])}">{esc(f[2])}</span> <a class="btn sm wa" href="{wa(f"Hola, mi {e["sing"]} Frigidaire tiene este problema: {f[0]}")}" target="_blank" rel="noopener" data-wa="falla">{ICONOS["wa"]} Consultar esta falla</a></p></article>' for f in e["fallas"])
        cuerpo = f'''{miga(2, (e["nombre"], base + "index.html"), ("Fallas comunes", None))}<section class="sec"><div class="w txt"><h1>Fallas comunes de {esc(e["corto"].lower())} Frigidaire en Panamá</h1><p class="lead">Síntomas frecuentes, causa probable y qué puedes revisar antes de llamar al técnico.</p>{det}</div></section>{cta(msg)}'''
        escribir(base + "fallas-comunes.html", f"Fallas comunes de {e['corto'].lower()} Frigidaire en Panamá y cómo repararlas", f"Fallas más comunes de {e['corto'].lower()} Frigidaire en Panamá: síntomas, causa probable y qué revisar. Servicio técnico a domicilio. WhatsApp {TEL}.", cuerpo,
                 [bc((e["nombre"], base + "index.html"), ("Fallas comunes", None))], "0.8")
        # mantenimiento
        lis = "".join(f"<li>{esc(m)}</li>" for m in e["mant"])
        cuerpo = f'''{miga(2, (e["nombre"], base + "index.html"), ("Mantenimiento", None))}<section class="sec"><div class="w txt"><h1>Mantenimiento de {esc(e["corto"].lower())} Frigidaire en Panamá</h1><p class="lead">Con el calor, la humedad y las variaciones de voltaje de Panamá, un buen mantenimiento evita daños mayores.</p><ul class="lista">{lis}</ul>
<p>Si prefieres que lo haga un técnico, mira el <a href="../../servicios/mantenimiento-preventivo-frigidaire-panama.html">servicio de mantenimiento preventivo</a>.</p></div></section>{cta(msg, "¿Quieres agendar un mantenimiento?")}'''
        escribir(base + "mantenimiento.html", f"Mantenimiento de {e['corto'].lower()} Frigidaire en Panamá: consejos y servicio", f"Consejos de mantenimiento para {e['corto'].lower()} Frigidaire en Panamá y cuándo pedir un servicio técnico. WhatsApp {TEL}.", cuerpo,
                 [bc((e["nombre"], base + "index.html"), ("Mantenimiento", None))], "0.7")
        # faq
        cuerpo = f'''{miga(2, (e["nombre"], base + "index.html"), ("Preguntas frecuentes", None))}<section class="sec"><div class="w txt"><h1>Preguntas frecuentes sobre {esc(e["corto"].lower())} Frigidaire</h1>{faq_html(e["faq"])}</div></section>{cta(msg)}'''
        escribir(base + "preguntas-frecuentes.html", f"Preguntas frecuentes: {e['corto'].lower()} Frigidaire en Panamá", f"Respuestas a las dudas más comunes sobre reparación de {e['corto'].lower()} Frigidaire en Panamá. WhatsApp {TEL}.", cuerpo,
                 [faq_ld(e["faq"]), bc((e["nombre"], base + "index.html"), ("Preguntas frecuentes", None))], "0.6")

def paginas_servicio():
    for k, (titulo, corto, desc, puntos) in SERVICIOS.items():
        msg = f"Hola, quiero agendar: {corto.lower()} para mi equipo Frigidaire en Panamá"
        ruta = f"servicios/{k}-frigidaire-panama.html"
        faq = [(f"¿Qué equipos incluye el servicio de {corto.lower()}?", "Neveras, lavadoras y secadoras Frigidaire."), ("¿Dónde lo hacen?", "En Ciudad de Panamá, San Miguelito y Panamá Oeste. Escríbenos por WhatsApp para confirmar tu zona."), ("¿Cuánto cuesta?", "Te confirmamos el costo por WhatsApp antes de ir, según el equipo y el servicio.")]
        cuerpo = f'''{miga(1, (corto, None))}<section class="sec"><div class="w txt"><h1>{esc(titulo)}</h1><p class="lead">{esc(desc)}</p><h2>Qué incluye</h2><ul class="lista">{"".join(f"<li>{esc(p)}</li>" for p in puntos)}</ul>
<div class="fotoc" style="max-width:720px">{pic("sam-6", "Técnico y asesora de servicio en una oficina de atención", 1, 1024, 765)}</div><h2>Equipos que atendemos</h2>{tarjetas_eq(1)}<h2>{esc(corto)} por equipo</h2><div class="chips">{"".join(f'<a href="{k}-{k2}-frigidaire-panama.html">{esc(corto)} de {esc(e2["corto"].lower())} Frigidaire</a>' for k2, e2 in EQUIPOS.items())}</div><h2>Preguntas frecuentes</h2>{faq_html(faq)}</div></section>{cta(msg, f"Agenda: {corto.lower()}")}'''
        escribir(ruta, f"{titulo} | {TEL}", f"{desc[:150]} WhatsApp {TEL}.", cuerpo, [negocio_ld(), faq_ld(faq), bc((corto, None))], "0.8")

def paginas_zona():
    for i, (z, tipo, area) in enumerate(ZONAS):
        s = slug(z); ruta = f"zonas/{s}/index.html"
        t1, t2 = TIPO_TXT[tipo]
        vec = [ZONAS[(i + d) % len(ZONAS)] for d in (1, 2, 3, 4)]
        msg = f"Hola, necesito servicio técnico para mi equipo Frigidaire en {z}"
        faq = [(f"¿Atienden en {z}?", f"Sí, damos servicio técnico Frigidaire a domicilio en {z} ({area}). Escríbenos por WhatsApp y te confirmamos disponibilidad."),
               (f"¿Cuánto tardan en llegar a {z}?", "Coordinamos visitas en 24 a 48 horas en la mayoría de las zonas."),
               ("¿Qué equipos Frigidaire reparan?", "Neveras, lavadoras y secadoras.")]
        cuerpo = f'''{miga(2, ("Zonas", "zonas/index.html"), (z, None))}<section class="hero chico"><div class="w hg"><div><span class="ey">{esc(area)}</span><h1>Servicio técnico Frigidaire en {esc(z)}</h1><p class="lead">Reparación a domicilio de neveras, lavadoras y secadoras Frigidaire en {esc(z)}. Diagnóstico honesto, costo claro y garantía.</p>
<div class="acc"><a class="btn wa lg" href="{wa(msg)}" target="_blank" rel="noopener" data-wa="hero">{ICONOS["wa"]} Escribir por WhatsApp</a></div></div><div class="hero-tarjeta"><b>{esc(z)}</b><small>{HORARIO}</small></div></div></section>
<section class="sec"><div class="w txt"><h2>Técnico Frigidaire a domicilio en {esc(z)}</h2><p>{esc(t1)}</p><p>{esc(t2)}</p>
<h2>Equipos Frigidaire que reparamos en {esc(z)}</h2>{tarjetas_eq(2)}<h2>Preguntas frecuentes en {esc(z)}</h2>{faq_html(faq)}
<h2>Servicio por equipo en {esc(z)}</h2><div class="chips">{"".join(f'<a href="{k2}.html">Reparación de {esc(e2["corto"].lower())} Frigidaire en {esc(z)}</a>' for k2, e2 in EQUIPOS.items())}</div><h2>Zonas cercanas</h2><div class="chips">{"".join(f'<a href="../{slug(v[0])}/index.html">{esc(v[0])}</a>' for v in vec)}</div><h2>Búsquedas relacionadas en {esc(z)}</h2><div class="chips">{"".join(f'<a href="{k2}.html">{t}</a>' for k2, e2 in EQUIPOS.items() for t in (f'Técnico de {esc(e2["sing"])} {MARCA} en {esc(z)}', f'Reparación de {esc(e2["corto"].lower())} {MARCA} en {esc(z)}', f'Servicio técnico {MARCA} {esc(e2["corto"].lower())} {esc(z)}'))}</div></div></section>{cta(msg, f"¿Equipo Frigidaire con falla en {z}?")}'''
        escribir(ruta, f"Servicio Técnico Frigidaire en {z} | Neveras, Lavadoras y Secadoras", f"Servicio técnico Frigidaire a domicilio en {z}, Panamá: neveras, lavadoras y secadoras. Garantía y visitas en 24-48 horas. WhatsApp {TEL}.", cuerpo,
                 [negocio_ld(area=z), faq_ld(faq), bc(("Zonas", "zonas/index.html"), (z, None))], "0.6")
    por_area = {}
    for z, tipo, area in ZONAS: por_area.setdefault(area, []).append(z)
    bloques = "".join(f'<h2>{esc(a)}</h2><div class="chips">{"".join(f"<a href=\"{slug(z)}/index.html\">{esc(z)}</a>" for z in zs)}</div>' for a, zs in por_area.items())
    msg = "Hola, quiero saber si dan servicio técnico Frigidaire en mi zona de Panamá"
    cuerpo = f'''{miga(1, ("Zonas de cobertura", None))}<section class="sec"><div class="w txt"><h1>Zonas de cobertura del servicio técnico Frigidaire en Panamá</h1><p class="lead">Atendemos a domicilio en {len(ZONAS)} zonas de Ciudad de Panamá, San Miguelito y Panamá Oeste. Si tu zona no aparece, escríbenos: puede que también lleguemos.</p>{bloques}</div></section>{cta(msg)}'''
    escribir("zonas/index.html", f"Zonas de cobertura: servicio técnico Frigidaire en Panamá | {TEL}", f"Zonas donde damos servicio técnico Frigidaire en Panamá: Ciudad de Panamá, San Miguelito, Arraiján y La Chorrera. WhatsApp {TEL}.", cuerpo, [bc(("Zonas de cobertura", None))], "0.8")

def paginas_blog():
    tarj = ""
    for sl, titulo, cat, resumen, secs in BLOG:
        msg = f"Hola, leí '{titulo}' y necesito servicio técnico Frigidaire"
        cuerpo_txt = "".join(f"<h2>{esc(h)}</h2>" + (t if t.startswith("<") or "<ul>" in t else f"<p>{esc(t)}</p>") if False else (f"<h2>{esc(h)}</h2><p>{t}</p>" if "<ul>" not in t else f"<h2>{esc(h)}</h2>{t}") for h, t in secs)
        rel = "".join([f'<a href="{sl2}.html">{esc(t2)}</a>' for sl2, t2, c2, *_ in BLOG if c2 == cat and sl2 != sl][:8])
        cuerpo = f'''{miga(1, ("Blog", "blog/index.html"), (titulo, None))}<section class="sec"><div class="w txt"><span class="ey">{esc(EQUIPOS[cat]["corto"])} Frigidaire</span><h1>{esc(titulo)}</h1><p class="lead">{esc(resumen)}</p>{cuerpo_txt}
<p><a href="../electrodomesticos/{cat}/index.html">Ver el servicio técnico de {esc(EQUIPOS[cat]["corto"].lower())} Frigidaire →</a></p>{f'<h2>Te puede interesar</h2><div class="chips">{rel}</div>' if rel else ""}</div></section>{cta(msg)}'''
        ld = [{"@context": "https://schema.org", "@type": "Article", "headline": titulo, "description": resumen, "inLanguage": "es-PA", "author": {"@type": "Organization", "name": NOMBRE}, "publisher": {"@type": "Organization", "name": NOMBRE}, "mainEntityOfPage": f"{DOMINIO}/blog/{sl}.html", "datePublished": "2026-10-20", "dateModified": "2026-10-20"}, bc(("Blog", "blog/index.html"), (titulo, None))]
        escribir(f"blog/{sl}.html", f"{titulo} | {NOMBRE}", resumen, cuerpo, ld, "0.6")
        tarj += f'<a class="card" href="{sl}.html"><span class="ey">{esc(EQUIPOS[cat]["corto"])}</span><h3>{esc(titulo)}</h3><p>{esc(resumen)}</p><span class="mas">Leer →</span></a>'
    cuerpo = f'''{miga(1, ("Blog", None))}<section class="sec"><div class="w"><div class="cab"><h1>Blog: guías de electrodomésticos Frigidaire en Panamá</h1><p>Consejos para entender las fallas de tu nevera, lavadora o secadora Frigidaire.</p></div><div class="grid g3">{tarj}</div></div></section>'''
    escribir("blog/index.html", f"Blog de electrodomésticos Frigidaire en Panamá | {NOMBRE}", "Guías sobre fallas de neveras, lavadoras y secadoras Frigidaire en Panamá: causas y qué hacer.", cuerpo, [bc(("Blog", None))], "0.7")

def pagina_diagnostico():
    items = []
    for k, e in EQUIPOS.items():
        for f in e["fallas"]:
            items.append((k, e["corto"], e["sing"], f))
    tabs = '<button class="tab on" data-f="todos">Todos</button>' + "".join(f'<button class="tab" data-f="{k}">{esc(v["corto"])}</button>' for k, v in EQUIPOS.items())
    cards = "".join(f'<article class="falla dg" data-eq="{k}"><span class="ey">{esc(c)} Frigidaire</span><h3>{esc(f[0])}</h3><p><b>Causa probable:</b> {esc(f[1])}</p><p><b>Qué revisar:</b> {esc(f[3])}</p><p><span class="u {slug(f[2])}">{esc(f[2])}</span> <a class="btn sm wa" href="{wa(f"Hola, mi {s} Frigidaire tiene este problema: {f[0]}")}" target="_blank" rel="noopener" data-wa="diagnostico">{ICONOS["wa"]} Consultar</a></p></article>' for k, c, s, f in items)
    ld = {"@context": "https://schema.org", "@type": "ItemList", "name": "Diagnóstico rápido de electrodomésticos Frigidaire", "itemListElement": [{"@type": "ListItem", "position": i, "name": f"{x[2].capitalize()} Frigidaire: {x[3][0]}"} for i, x in enumerate(items, 1)]}
    cuerpo = f'''{miga(0, ("Diagnóstico rápido", None))}<section class="sec"><div class="w"><div class="cab"><h1>Diagnóstico rápido: ¿qué le pasa a tu equipo Frigidaire?</h1><p>{len(items)} fallas comunes de neveras, lavadoras y secadoras Frigidaire, con la causa probable y qué tan urgente es.</p></div><div class="tabs" role="tablist">{tabs}</div><div class="grid g2" id="dg">{cards}</div></div></section>{cta("Hola, necesito diagnóstico para mi equipo Frigidaire en Panamá")}'''
    escribir("diagnostico.html", f"Diagnóstico rápido de neveras, lavadoras y secadoras Frigidaire | {NOMBRE}", f"{len(items)} fallas comunes de electrodomésticos Frigidaire en Panamá con causa probable y urgencia. Consulta tu caso por WhatsApp.", cuerpo, [ld, bc(("Diagnóstico rápido", None))], "0.8")

FAQ_FULL = FAQ_GENERAL + [q for e in EQUIPOS.values() for q in e["faq"]]
def paginas_info():
    msg = "Hola, necesito servicio técnico para mi equipo Frigidaire en Panamá"
    c = f'''{miga(0, ("Garantía", None))}<section class="sec"><div class="w txt"><h1>Garantía de servicio técnico Frigidaire en Panamá</h1><p class="lead">Cada reparación incluye garantía sobre la pieza reemplazada y sobre la mano de obra. El plazo exacto se confirma antes de empezar el trabajo, no después.</p>
<p>Esta es la garantía de nuestro servicio técnico y es distinta de la garantía de fábrica. Si tu equipo todavía está en garantía de fábrica, te lo decimos durante el diagnóstico para que la hagas valer donde corresponda.</p>
<h2>Qué cubre</h2><ul class="lista"><li><b>Pieza reemplazada:</b> si vuelve a fallar por defecto de la pieza dentro del plazo acordado, la revisamos sin costo adicional de mano de obra.</li><li><b>Mano de obra:</b> si el mismo síntoma reaparece por un error de instalación o ajuste, lo corregimos sin cargo.</li></ul>
<h2>Qué no cubre</h2><p>Daños nuevos por mal uso, variaciones de voltaje posteriores al servicio o intervención de terceros después de nuestra visita.</p>{faq_html([("¿Cuánto dura la garantía?", "Depende de la pieza y del tipo de reparación; te lo confirmamos por escrito al momento del servicio, antes de que pagues."), ("¿Qué hago si la falla vuelve?", "Escríbenos por WhatsApp con tu nombre y la fecha del servicio anterior; si está dentro del plazo, coordinamos la revisión.")])}</div></section>{cta(msg)}'''
    escribir("garantia.html", f"Garantía de servicio técnico Frigidaire en Panamá | {NOMBRE}", "Garantía sobre la pieza reemplazada y la mano de obra en cada reparación de electrodomésticos Frigidaire en Panamá.", c, [bc(("Garantía", None))], "0.5")
    c = f'''{miga(0, ("Nosotros", None))}<section class="sec"><div class="w txt"><h1>Nosotros: especialistas en electrodomésticos Frigidaire en Panamá</h1><p class="lead">Somos un servicio técnico enfocado en electrodomésticos Frigidaire: neveras, lavadoras y secadoras.</p>
<p>Esa especialización nos permite conocer a fondo los modelos que circulan en Panamá, sus fallas más comunes y los repuestos que realmente necesitan. Trabajamos con coordinación directa por WhatsApp, sin intermediarios.</p>
<div class="fotoc" style="max-width:720px">{pic("sam-5", "Técnico y asesora de servicio conversando en una oficina de atención al cliente", 0, 1024, 765)}</div><div class="fotoc" style="max-width:720px">{pic("sam-1", "Asesora de servicio atendiendo en el escritorio de la oficina", 0, 1024, 765)}</div><div class="fotoc" style="max-width:720px">{pic("sam-2", "Técnico y asesora de servicio conversando en la oficina", 0, 1024, 765)}</div><div class="fotoc" style="max-width:720px">{pic("sam-5", "Asesora atendiendo a un cliente en el mostrador", 0, 1024, 765)}</div><h2>Cómo trabajamos</h2><ul class="lista"><li><b>Diagnóstico honesto:</b> explicamos la falla antes de reparar. Si no vale la pena, te lo decimos.</li><li><b>Garantía:</b> en la pieza y en la mano de obra.</li><li><b>Tiempos claros:</b> visitas en 24 a 48 horas en la mayoría de zonas.</li><li><b>Costo claro:</b> te lo confirmamos antes de empezar.</li></ul>
</div></section>{cta(msg)}'''
    escribir("nosotros.html", f"Nosotros | {NOMBRE}", "Servicio técnico especializado en electrodomésticos Frigidaire en Ciudad de Panamá.", c, [negocio_ld(), bc(("Nosotros", None))], "0.5")
    c = f'''{miga(0, ("Preguntas frecuentes", None))}<section class="sec"><div class="w txt"><h1>Preguntas frecuentes sobre el servicio técnico Frigidaire en Panamá</h1>{faq_html(FAQ_FULL)}</div></section>{cta(msg)}'''
    escribir("preguntas-frecuentes.html", f"Preguntas frecuentes | Servicio técnico Frigidaire en Panamá", "Respuestas sobre cobertura, costos, garantía y tiempos del servicio técnico Frigidaire en Panamá.", c, [faq_ld(FAQ_FULL), bc(("Preguntas frecuentes", None))], "0.6")
    c = f'''{miga(0, ("Privacidad", None))}<section class="sec"><div class="w txt"><h1>Política de privacidad</h1><p>Cuando nos escribes por WhatsApp o nos llamas usamos tu nombre, tu número y los datos que nos des (dirección, equipo, modelo y falla) solo para atender tu solicitud y coordinar la visita.</p><p>No vendemos tus datos. Puedes pedirnos que los corrijamos o los eliminemos escribiéndonos por WhatsApp al {TEL}.</p><p>Este sitio puede usar herramientas de medición (como Google Analytics o Tag Manager) para saber cuántas personas lo visitan y cuántas nos escriben por WhatsApp.</p></div></section>'''
    escribir("privacidad.html", f"Política de privacidad | {NOMBRE}", "Cómo usamos tus datos cuando nos contactas para un servicio técnico.", c, None, "0.2")
    c = f'''{miga(0, ("Aviso legal", None))}<section class="sec"><div class="w txt"><h1>Aviso legal</h1><p>{NOMBRE} presta servicio técnico a domicilio para electrodomésticos Frigidaire en Panamá.</p><p>Frigidaire es una marca registrada de su titular. Este sitio no es operado por Frigidaire.</p><p>La información de este sitio es orientativa. El diagnóstico definitivo y el costo se confirman en la visita.</p></div></section>'''
    escribir("aviso-legal.html", f"Aviso legal | {NOMBRE}", "Aviso legal del servicio técnico de electrodomésticos Frigidaire en Panamá.", c, None, "0.2")

CSS = r'''
:root{--pri:#c8102e;--pri2:#0c0a0a;--ink:#17181b;--mut:#5d5f66;--bg:#fff;--panel:#faf4f4;--line:#eadcdd;--soft:#f6e3e5;--wa:#1fa855;--r:18px}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;font:16px/1.6 "Plus Jakarta Sans",system-ui,sans-serif;color:var(--ink);background:var(--bg)}
img,svg{max-width:100%}a{color:var(--pri)}h1,h2,h3{line-height:1.2;letter-spacing:-.02em;margin:0 0 .5em;text-wrap:balance}h1{font-size:clamp(28px,5vw,46px);font-weight:800}h2{font-size:clamp(22px,3.4vw,32px);font-weight:800}h3{font-size:18px;font-weight:700}
.w{max-width:1120px;margin:0 auto;padding-inline:max(16px,env(safe-area-inset-left,0px))}
.top{position:sticky;top:0;z-index:50;background:#fff;border-bottom:1px solid var(--line)}.barra{background:var(--pri);color:#fff;font-size:13px}.barra .w{display:flex;justify-content:space-between;gap:12px;align-items:center;padding-block:6px}.barra a{color:#fff;text-decoration:none;font-weight:700;display:flex;gap:6px;align-items:center;white-space:nowrap}.barra svg{width:16px;height:16px}
.nav{display:flex;align-items:center;justify-content:space-between;gap:16px;padding-block:10px}.logo{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--ink)}.lg-i{display:grid;place-items:center;width:40px;height:40px;border-radius:12px;background:var(--pri);color:#fff}.lg-i svg{width:22px;height:22px}.lg-t{display:flex;flex-direction:column;line-height:1.05;font-weight:700;font-size:14px}.lg-t b{font-size:20px;color:var(--pri);letter-spacing:.04em}.lg-t small{font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--mut)}
nav{display:flex;align-items:center;gap:18px}nav>a,.dd>a{color:var(--ink);text-decoration:none;font-weight:600;font-size:15px}nav>a:hover,.dd>a:hover{color:var(--pri)}.dd{position:relative}.pn{display:none;position:absolute;top:100%;left:-10px;background:#fff;border:1px solid var(--line);border-radius:14px;box-shadow:0 16px 40px -16px rgba(0,0,0,.25);padding:8px;min-width:260px}.dd:hover .pn,.dd:focus-within .pn{display:block}.pn a{display:block;padding:9px 12px;border-radius:8px;color:var(--ink);text-decoration:none;font-weight:600;font-size:14px}.pn a:hover{background:var(--soft);color:var(--pri)}
.burger{display:none;width:44px;height:44px;border:1px solid var(--line);border-radius:12px;background:#fff;cursor:pointer;position:relative}.burger span,.burger span::before,.burger span::after{content:"";position:absolute;left:12px;right:12px;height:2px;background:var(--ink);border-radius:2px}.burger span{top:21px}.burger span::before{top:-7px;left:0;right:0}.burger span::after{top:7px;left:0;right:0}
.mov{padding:8px 16px 18px;border-top:1px solid var(--line);max-height:75vh;overflow:auto}.mov b{display:block;margin:12px 0 4px;color:var(--mut);font-size:12px;text-transform:uppercase;letter-spacing:.12em}.mov a{display:block;padding:10px 4px;color:var(--ink);text-decoration:none;font-weight:600;border-bottom:1px solid var(--line)}
@media(max-width:900px){nav{display:none}.burger{display:block}.barra span{display:none}.barra .w{justify-content:center}}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;background:var(--pri);color:#fff;border:2px solid var(--pri);border-radius:999px;padding:11px 20px;font-weight:700;text-decoration:none;cursor:pointer;font-size:15px}.btn svg{width:20px;height:20px}.btn.lg{padding:14px 26px;font-size:16px}.btn.sm{padding:6px 14px;font-size:13px}.btn.sec{background:transparent;color:#fff;border-color:#fff}.btn.wa{background:var(--wa);border-color:var(--wa);color:#fff}.btn:hover{filter:brightness(1.08)}
.hero{background:radial-gradient(1000px 420px at 85% -10%,#5a1119 0%,transparent 60%),linear-gradient(160deg,var(--pri2),var(--pri));color:#fff;padding-block:56px}.hero.chico{padding-block:40px}.hero h1{color:#fff}.hero .lead{font-size:18px;opacity:.95;max-width:60ch}.hg{display:grid;grid-template-columns:1.3fr 1fr;gap:32px;align-items:center}.ey{display:inline-block;font-size:12px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:#ff3b4e;margin-bottom:10px}.sec:not(.alt) .ey,.sec.alt .ey,.card .ey{color:var(--pri)}.acc{display:flex;gap:12px;flex-wrap:wrap;margin:22px 0}.pts{display:flex;gap:18px;flex-wrap:wrap;list-style:none;padding:0;margin:0;font-weight:600;font-size:14px}.pts li::before{content:"✓ ";color:#a9f5c9}
.hero.bgimg{background:linear-gradient(90deg,rgba(12,10,10,.94) 0%,rgba(12,10,10,.80) 48%,rgba(150,12,30,.50) 100%),var(--bg) var(--pos,center)/cover no-repeat;min-height:clamp(340px,46vw,520px);display:flex;align-items:center}.hero.bgimg>.w{width:100%}.hero.bgimg .hg.solo{grid-template-columns:minmax(0,760px)}.hero.bgimg .hero-tarjeta{backdrop-filter:blur(6px);background:rgba(12,10,10,.55)}.hero.bgimg h1{text-shadow:0 2px 18px rgba(0,0,0,.45)}@media(max-width:860px){.hero.bgimg{background:linear-gradient(180deg,rgba(12,10,10,.88) 0%,rgba(12,10,10,.80) 60%,rgba(120,10,25,.72) 100%),var(--bg) var(--pos,center)/cover no-repeat;min-height:0;padding-block:44px}}
.hero-tarjeta{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.25);border-radius:var(--r);padding:20px;display:flex;flex-direction:column;gap:12px}.eqimgs.big{gap:24px;margin:0 0 22px;justify-content:flex-start}.eqimgs.big .fto{width:auto}.eqimgs.big img{height:260px;width:auto;border:0;padding:0}.eqimgs{display:flex;justify-content:center;gap:10px}.eqimg.foto{height:auto;width:100%;aspect-ratio:16/10;object-fit:cover;border-radius:12px}.eqimg{height:150px;width:auto;max-width:100%;object-fit:contain;align-self:center;margin-bottom:6px}.mini.fotos a{flex-direction:column;justify-content:center;text-align:center;padding:12px 8px;gap:8px}.mini.fotos img{height:120px;width:auto;max-width:100%;object-fit:contain}.mini.fotos .nm{font-weight:700;line-height:1.2}.mini.fotos .ic svg{width:70px;height:70px}.mini{display:grid;grid-template-columns:1fr 1fr;gap:10px}.mini a{display:flex;align-items:center;gap:10px;background:#fff;color:var(--ink);border-radius:14px;padding:12px;text-decoration:none;font-weight:700;font-size:14px}.mini .ic svg,.ic.grande svg{width:34px;height:34px}.mini .ic{color:var(--pri)}.ic.grande{color:#fff}.ic.grande svg{width:56px;height:56px}
@media(max-width:860px){.hg{grid-template-columns:1fr}}
.conf{border-bottom:1px solid var(--line)}.conf .w{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;padding-block:20px}.conf b{display:block}.conf small{color:var(--mut)}@media(max-width:760px){.conf .w{grid-template-columns:1fr 1fr}}
.sec{padding-block:56px}.sec.alt{background:var(--panel)}.cab{max-width:720px;margin-bottom:28px}.cab p{color:var(--mut)}.grid{display:grid;gap:18px}.g4{grid-template-columns:repeat(4,1fr)}.g3{grid-template-columns:repeat(3,1fr)}.g2{grid-template-columns:repeat(2,1fr)}@media(max-width:960px){.g4{grid-template-columns:1fr 1fr}.g3{grid-template-columns:1fr 1fr}}@media(max-width:620px){.g4,.g3,.g2{grid-template-columns:1fr}}
.card{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:20px;text-decoration:none;color:var(--ink);display:flex;flex-direction:column;gap:6px}a.card:hover{border-color:var(--pri);transform:translateY(-2px);transition:.15s}.card p{color:var(--mut);margin:0;font-size:15px}.card .ic{color:var(--pri)}.card .ic svg{width:44px;height:44px}.mas{color:var(--pri);font-weight:700;margin-top:auto;font-size:14px}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0}.chips a{padding:8px 14px;border:1px solid var(--line);border-radius:999px;background:#fff;text-decoration:none;color:var(--ink);font-weight:600;font-size:14px}.chips a:hover{border-color:var(--pri);color:var(--pri)}
.pasos{list-style:none;counter-reset:n;display:grid;grid-template-columns:repeat(3,1fr);gap:18px;padding:0}.pasos li{counter-increment:n;background:var(--panel);border-radius:var(--r);padding:22px}.pasos li::before{content:counter(n);display:grid;place-items:center;width:38px;height:38px;border-radius:50%;background:var(--pri);color:#fff;font-weight:800;margin-bottom:10px}.pasos p{margin:4px 0 0;color:var(--mut)}@media(max-width:760px){.pasos{grid-template-columns:1fr}}
.aviso{background:var(--soft);border-radius:14px;padding:14px 18px;font-size:14px;margin-top:20px}
.cta{background:linear-gradient(120deg,var(--pri2),var(--pri));color:#fff;border-radius:var(--r);padding:28px;display:flex;gap:20px;align-items:center;justify-content:space-between;flex-wrap:wrap}.cta h2{color:#fff;margin:0 0 6px}.cta p{margin:0;opacity:.92;max-width:56ch}
.faq{border:1px solid var(--line);border-radius:14px;padding:12px 16px;margin:10px 0;background:#fff}.faq summary{font-weight:700;cursor:pointer}.faq p{margin:10px 0 0;color:var(--mut)}
.txt{max-width:820px}.txt h2{margin-top:1.4em}.lead{font-size:18px;color:var(--mut)}.hero .lead{color:#fff}.lista{padding-left:20px}.lista li{margin:6px 0}.miga{font-size:14px;padding-block:14px;color:var(--mut)}.miga a{color:var(--mut)}
.tabla-w{overflow-x:auto;border:1px solid var(--line);border-radius:14px;background:#fff}.tabla{border-collapse:collapse;width:100%;min-width:560px}.tabla th,.tabla td{padding:12px 14px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top;font-size:15px}.tabla th{background:var(--soft);font-size:13px;text-transform:uppercase;letter-spacing:.06em}
.u{display:inline-block;padding:3px 10px;border-radius:999px;font-size:12px;font-weight:800}.u.urgente{background:#fde2e2;color:#a31212}.u.revisar-pronto{background:#ffe3e6;color:#8a1020}.u.vigilar{background:#dff5e8;color:#0d6b3a}
.falla{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:18px;margin:14px 0}.falla p{margin:6px 0}.tabs{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:18px}.tab{padding:8px 16px;border:1px solid var(--line);border-radius:999px;background:#fff;font:600 14px inherit;cursor:pointer}.tab.on{background:var(--pri);color:#fff;border-color:var(--pri)}
.pie{background:var(--pri2);color:#f4ecec;padding-top:44px}.pie a{color:#f4ecec;text-decoration:none}.cols{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:28px}.cols b{display:block;color:#fff;margin-bottom:8px}.cols a{display:block;padding:3px 0;font-size:14px}.pl{font-size:18px}.hor{font-size:13px;opacity:.8}.legal{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;border-top:1px solid rgba(255,255,255,.15);margin-top:28px;padding-block:18px;font-size:12px;opacity:.85}@media(max-width:860px){.cols{grid-template-columns:1fr 1fr}}@media(max-width:560px){.cols{grid-template-columns:1fr}}
.wa-flot{position:fixed;right:16px;bottom:calc(16px + env(safe-area-inset-bottom,0px));z-index:60;display:flex;align-items:center;gap:8px;background:#25d366;color:#fff!important;border-radius:999px;padding:12px 18px 12px 14px;font-weight:800;text-decoration:none;box-shadow:0 8px 24px rgba(0,0,0,.25)}.wa-flot svg{width:28px;height:28px}@media(max-width:520px){.wa-flot span{display:none}.wa-flot{padding:14px}}

.pie .logo{color:#fff;display:flex!important;margin:0 0 12px}.pie .btn{display:inline-flex!important;width:auto}.pie .lg-t{font-size:14px}.pie .lg-t b{color:#fff}.pie .lg-t small{color:#e0c9cc}.pie .lg-i{background:#fff;color:var(--pri)}.busq{padding-top:22px}.busq b{display:block;color:#fff;margin-bottom:6px}.busq .chips a{background:transparent;border-color:rgba(255,255,255,.3);color:#f4ecec;font-size:13px;padding:6px 12px}.fto img{width:100%;height:auto;display:block;border-radius:var(--r)}.hero-tarjeta.foto{padding:0;overflow:hidden;background:none;border:0}.gf .fto img{aspect-ratio:16/10;object-fit:cover}.split{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:center}.split.rev .sp-f{order:2}.split .fto img{aspect-ratio:4/3;object-fit:cover}.fto.pr img{object-fit:contain!important;background:#fff;border:1px solid var(--line);padding:14px}.sp-t p{color:var(--mut)}.btn.sm{padding:8px 16px;font-size:14px}.split .fto.pr img{aspect-ratio:auto;width:auto;max-width:100%;max-height:440px;margin:0 auto}.sp-f{text-align:center}.mods{display:grid;grid-template-columns:repeat(5,1fr);gap:14px}.mods img{height:200px!important}.mods a{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:18px;text-align:center;text-decoration:none;color:var(--ink);display:flex;flex-direction:column;gap:10px;align-items:center}.mods img{height:230px;width:auto;max-width:100%;object-fit:contain}.mods b{font-size:15px}@media(max-width:900px){.mods{grid-template-columns:repeat(2,1fr)}}.marca-pie{display:flex;align-items:center;gap:10px;font-size:13px;color:#e0c9cc}.marca-pie img{background:#fff;border-radius:8px;padding:3px 8px;height:30px;width:auto}.marca-band{border-bottom:1px solid var(--line);background:#fff}.marca-band .w{display:flex;align-items:center;gap:18px;flex-wrap:wrap;padding-block:16px}.marca-band span{font-weight:700;color:var(--mut)}.marca-band img{height:44px;width:auto}.marca-band small{color:var(--mut);font-size:12px}.marcas{display:inline-flex;gap:4px;margin-left:12px}.marcas a{padding:2px 10px;border-radius:999px;border:1px solid rgba(255,255,255,.45);color:#fff;text-decoration:none;font-weight:700;font-size:12px}.marcas a.on{background:#fff;color:var(--pri)}.otra{padding:16px 0 4px;font-size:13px;color:var(--soft2,#ccd)}.otra a{text-decoration:underline}.mapa{columns:2;column-gap:32px}.mapa li{break-inside:avoid;font-size:14px}.busq2 .chips a{font-size:13px;padding:6px 12px}.ey{color:#c8102e!important}.hero .ey,.pie .ey{color:#ff3b4e!important}.mas{color:#c8102e!important}.lg-t b{color:#c8102e}.lg-i{background:#e3122b!important;color:#17181b!important}.u.urgente{background:#fde2e2}.lado{float:right;width:min(46%,420px);margin:4px 0 18px 26px}.lado img{width:100%;height:auto;border-radius:var(--r)}.txt::after{content:"";display:block;clear:both}@media(max-width:700px){.lado{float:none;width:100%;margin:0 0 16px}}.fotoc{max-width:520px;margin:18px 0}.fotoc img{width:100%;height:auto;border-radius:var(--r)}@media(max-width:820px){.split{grid-template-columns:1fr;gap:20px}.split.rev .sp-f{order:0}}
'''
JS = '''(function(){
  window.dataLayer=window.dataLayer||[];
  document.addEventListener("click",function(e){var a=e.target.closest('a[href*="wa.me/"],a[href^="tel:"]');if(a){dataLayer.push({event:"whatsapp",ubicacion:a.getAttribute("data-wa")||"enlace",boton:(a.textContent||"").trim().slice(0,60),pagina:location.pathname})}},true);
  var b=document.querySelector(".burger"),m=document.querySelector(".mov");
  if(b&&m){b.addEventListener("click",function(){var o=m.hidden;m.hidden=!o;b.setAttribute("aria-expanded",String(o))})}
  var tabs=document.querySelectorAll(".tab");
  tabs.forEach(function(t){t.addEventListener("click",function(){tabs.forEach(function(x){x.classList.remove("on")});t.classList.add("on");var f=t.getAttribute("data-f");document.querySelectorAll(".dg").forEach(function(c){c.hidden=(f!=="todos"&&c.getAttribute("data-eq")!==f)})})});
})();'''

def estaticos():
    (OUT / "css").mkdir(exist_ok=True); (OUT / "js").mkdir(exist_ok=True); (OUT / "images" / "logo").mkdir(parents=True, exist_ok=True)
    (OUT / "css" / "estilos.css").write_text(CSS, encoding="utf-8")
    (OUT / "js" / "main.js").write_text(JS, encoding="utf-8")
    (OUT / "images" / "logo" / "favicon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#c8102e"/><g transform="translate(14 14) scale(1.5)" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.2L3 17.8V21h3.2l6.3-6.3a4 4 0 0 0 5.2-5.4l-2.5 2.5-2.4-.6-.6-2.4z"/></g></svg>', encoding="utf-8")
    # imagen para compartir
    from PIL import Image, ImageDraw, ImageFont
    im = Image.new("RGB", (1200, 630), (38, 39, 43)); d = ImageDraw.Draw(im)
    for y in range(630):
        d.line([(0, y), (1200, y)], fill=(int(13 + 25 * y / 630), int(13 + 26 * y / 630), int(16 + 27 * y / 630)))
    fb = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; fr = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    d.text((70, 150), "Servicio técnico", font=ImageFont.truetype(fb, 64), fill="white")
    d.text((70, 235), "Frigidaire en Panamá", font=ImageFont.truetype(fb, 84), fill="white")
    d.text((70, 360), "Neveras · Lavadoras · Secadoras", font=ImageFont.truetype(fr, 34), fill=(255, 210, 63))
    d.text((70, 480), f"WhatsApp {TEL}  ·  {HORARIO}", font=ImageFont.truetype(fb, 36), fill="white")
    (OUT / "images").mkdir(exist_ok=True); im.save(OUT / "images" / "og.jpg", quality=88)

def indices():
    urls = "".join(f"<url><loc>{DOMINIO}/{r}</loc><lastmod>{LASTMOD}</lastmod><priority>{p[0]}</priority></url>\n" for r, p in sorted(((k, v) for k, v in PAGINAS.items() if k not in NOINDEX), key=lambda x: -float(x[1][0])))
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nUser-agent: GPTBot\nAllow: /\nUser-agent: ClaudeBot\nAllow: /\nUser-agent: PerplexityBot\nAllow: /\nUser-agent: Google-Extended\nAllow: /\n\nSitemap: {DOMINIO}/sitemap.xml\n", encoding="utf-8")
    txt = f"# {NOMBRE}\n\n> Servicio técnico Frigidaire en Panamá: neveras, lavadoras y secadoras Frigidaire a domicilio en Ciudad de Panamá. WhatsApp {TEL}. {HORARIO}.\n\n## Servicios\n"
    for k, e in EQUIPOS.items(): txt += f"- [{e['titulo_h1']}]({DOMINIO}/electrodomesticos/{k}/index.html)\n"
    txt += "\n## Páginas clave\n" + "".join(f"- [{h['h1']}]({DOMINIO}/{h['f']})\n" for h in HUBS)
    txt += "\n## Zonas\n" + "".join(f"- [Servicio técnico Frigidaire en {z[0]}]({DOMINIO}/zonas/{slug(z[0])}/index.html)\n" for z in ZONAS)
    txt += "\n## Guías\n" + "".join(f"- [{b[1]}]({DOMINIO}/blog/{b[0]}.html)\n" for b in BLOG)
    txt += f"\n## Datos clave\n- Negocio: {NOMBRE} (parte de {ORG})\n- Servicio: reparación a domicilio de neveras, lavadoras y secadoras {MARCA}\n- Teléfono y WhatsApp: {TEL}\n- Horario: {HORARIO}\n- Cobertura: Ciudad de Panamá, San Miguelito y Panamá Oeste ({len(ZONAS)} zonas)\n- Tiempo de visita: 24 a 48 horas en la mayoría de las zonas\n- Garantía: sobre la pieza reemplazada y la mano de obra\n"
    txt += "\n## Preguntas frecuentes\n" + "".join(f"\n### {q}\n{a}\n" for q, a in (faq_base() + [x for k in EQUIPOS for x in faq_eq(k)]))
    (OUT / "llms.txt").write_text(txt, encoding="utf-8")

# ------------------------------------------------------------ cobertura de búsquedas
def fslug(f): return slug(f[0])[:48].strip("-")
def furl(k, f): return f"fallas/{k}/{fslug(f)}.html"
def zurl(k, z): return f"zonas/{slug(z)}/{k}.html"
FOTO_FALLA = {"neveras": ("prod-nevera-sbs", "Persona usando el dispensador de agua de una nevera Frigidaire French Door"), "lavadoras": ("sam-6", "Técnico revisando una lavadora Frigidaire en Panamá"),
              "secadoras": ("sam-3", "Técnico revisando una secadora y lavadora Frigidaire")}
FOTO_ZEQ = {"neveras": ("sam-4", FOTO_EQ["neveras"][1]), "lavadoras": ("sam-3", FOTO_EQ["lavadoras"][1]), "secadoras": ("sam-6", "Técnico revisando una secadora Frigidaire")}
ROT = {"neveras": NEV_FOTOS, "lavadoras": ["sam-6", "prod-lavadora-sup", "sam-2", "sam-5", "sam-3", "sam-6"], "secadoras": ["prod-lavadora-fr", "prod-torre", "sam-3", "sam-6", "sam-1", "sam-2"]}
def foto_rot(k, i): return ROT[k][i % len(ROT[k])]
PASOS = {"Urgente": "Si el síntoma es este, lo mejor es apagar y desconectar el equipo y escribirnos cuanto antes: seguir usándolo puede agravar el daño o la pérdida de alimentos.",
         "Revisar pronto": "No es una emergencia, pero conviene revisarlo pronto: una falla pequeña que se deja pasar suele terminar en una reparación más costosa.",
         "Vigilar": "Normalmente no es grave. Prueba lo que te sugerimos; si el síntoma persiste o se repite, coordinamos una visita."}

def busquedas_chips(depth, n=None):
    r = R(depth)
    hs = HUBS if n is None else HUBS[:n]
    return "".join(f'<a href="{r}{h["f"]}">{esc(h["chip"])}</a>' for h in hs)

def paginas_fallas():
    todas = []
    for k, e in EQUIPOS.items():
        for f in e["fallas"]:
            todas.append((k, e, f))
    for idx, (k, e, f) in enumerate(todas):
        s, causa, urg, rev = f
        ruta = furl(k, f)
        msg = f"Hola, mi {e['sing']} Frigidaire tiene este problema: {s}"
        titulo = f"{s} en {e['sing']} Frigidaire: causas y reparación en Panamá"
        titulo = titulo if len(titulo) <= 68 else (f"{s}: {e['sing']} Frigidaire | Panamá" if len(s) < 38 else f"{s[:38].rsplit(' ', 1)[0]}…: {e['sing']} Frigidaire | Panamá")
        foto = foto_rot(k, idx)
        otras = "".join(f'<a href="{fslug(g)}.html">{esc(g[0])}</a>' for g in e["fallas"] if g is not f)
        zs = "".join(f'<a href="../../{zurl(k, z[0])}">{esc(e["corto"])} Frigidaire en {esc(z[0])}</a>' for z in ZONAS[:12])
        faq = [(f"¿Cuánto cuesta reparar: {s.lower()}?", "Depende de la causa y de la pieza. Escríbenos por WhatsApp con el modelo y el síntoma; te confirmamos el costo de la visita antes de ir y el de la reparación antes de empezar."),
               (f"¿Cuánto tarda la reparación?", "Muchas fallas se resuelven en la misma visita. Si hace falta una pieza, te avisamos el plazo antes de empezar. Coordinamos visitas en 24 a 48 horas."),
               (f"¿Atienden en mi zona de Panamá?", "Damos servicio a domicilio en Ciudad de Panamá, San Miguelito y Panamá Oeste. Escríbenos con tu barrio y te confirmamos.")]
        cuerpo = f'''{miga(2, ("Fallas", "fallas/index.html"), (f"{e['corto']}: {s}", None))}<section class="hero chico"><div class="w hg"><div><span class="ey">{esc(e["corto"])} Frigidaire · <span class="u {slug(urg)}">{esc(urg)}</span></span><h1>{esc(s)} en {esc(e["sing"])} Frigidaire</h1><p class="lead">Qué significa, cuál es la causa más probable y cuándo conviene llamar al técnico. Servicio técnico Frigidaire a domicilio en Panamá.</p>
<div class="acc"><a class="btn wa lg" href="{wa(msg)}" target="_blank" rel="noopener" data-wa="hero">{ICONOS["wa"]} Consultar esta falla</a></div></div><div class="hero-tarjeta foto">{fpic(foto, 2, None, False)}</div></div></section>
<section class="sec"><div class="w txt"><h2>¿Por qué mi {esc(e["sing"])} Frigidaire presenta este problema?</h2><p><b>Causa probable:</b> {esc(causa)}</p><p>En Panamá el calor, la humedad y las variaciones de voltaje aceleran el desgaste de componentes de {esc(e["art"])}, por eso esta falla es frecuente en equipos con algunos años de uso.</p>
<h2>Qué puedes revisar antes de llamar</h2><p>{esc(rev)}</p><p>Revisa también que el equipo esté bien conectado, nivelado y con el tomacorriente en buen estado. Si no estás seguro de algo, no desarmes el equipo: puedes empeorar la falla o hacerte daño.</p>
<h2>¿Es urgente?</h2><p><span class="u {slug(urg)}">{esc(urg)}</span> {esc(PASOS[urg])}</p>
<h2>Qué hacemos en la visita</h2><ul class="lista"><li>Revisamos el equipo en tu casa u oficina y confirmamos la causa de la falla.</li><li>Te explicamos el problema, las opciones y el costo antes de empezar.</li><li>Reparamos o reemplazamos la pieza necesaria y probamos el equipo.</li><li>La reparación incluye garantía sobre la pieza y la mano de obra.</li></ul>
<h2>Causas posibles en detalle</h2><p>{esc(s)} es un síntoma que puede tener más de una causa en {esc(e["art"])} Frigidaire. Por eso el técnico no cambia piezas a ciegas: mide, descarta y confirma la falla antes de reparar. En este caso la causa más probable es: {esc(causa[0].lower() + causa[1:])}</p>
<h2>¿Reparar o reemplazar {esc(e["art"])} Frigidaire?</h2><p>Si la falla es de una pieza accesible y el equipo está en buen estado general, reparar casi siempre conviene. Si el equipo es muy antiguo o el daño es costoso, te explicamos las opciones con honestidad para que decidas con la información completa.</p>
<h2>Cómo prevenir esta falla</h2><p>{esc(e["mant"][idx % len(e["mant"])])} Además, protege el equipo de bajones de voltaje y evita sobrecargarlo.</p>
<h2>Servicio técnico de {esc(e["corto"].lower())} Frigidaire en Ciudad de Panamá</h2><p>Atendemos este tipo de falla a domicilio en San Francisco, Bella Vista, Obarrio, Costa del Este, Punta Pacífica, Betania, San Miguelito, Albrook, Arraiján, La Chorrera y más zonas. Escríbenos por WhatsApp con el modelo y la falla.</p>
<h2>Guías relacionadas</h2><div class="chips">{guias_chips(k, 2)}</div>
<h2>Otras fallas de {esc(e["corto"].lower())} Frigidaire</h2><div class="chips">{otras}</div>
<h2>Preguntas frecuentes</h2>{faq_html(faq)}<h2>Servicio en tu zona</h2><div class="chips">{zs}</div><h2>Búsquedas relacionadas</h2><div class="chips">{"".join(f'<a href="../../{zurl(k, z[0])}">{esc(s)} {esc(e["sing"])} {MARCA} en {esc(z[0])}</a>' for z in ZONAS[12:24])}</div></div></section>{cta(msg, f"¿Tu {e['sing']} Frigidaire tiene esta falla?")}'''
        escribir(ruta, titulo, f"{s} en {e['sing']} Frigidaire: causa probable, qué revisar y cuándo llamar al técnico. Servicio técnico Frigidaire a domicilio en Panamá. WhatsApp {TEL}.", cuerpo,
                 [negocio_ld(), faq_ld(faq), howto_ld(f"Qué revisar si {s.lower()} en {e['art']} Frigidaire", [("Revisa lo básico", rev), ("Descarta la causa probable", causa), ("Pide diagnóstico técnico", "Si el síntoma continúa, escribe por WhatsApp con el modelo y la falla para coordinar una visita a domicilio en Panamá.")], ruta), bc(("Fallas", "fallas/index.html"), (f"{e['corto']}: {s}", None))], "0.7")
    bloques = ""
    for k, e in EQUIPOS.items():
        bloques += f'<h2>Fallas de {esc(e["corto"].lower())} Frigidaire</h2><div class="chips">' + "".join(f'<a href="{k}/{fslug(f)}.html">{esc(f[0])}</a>' for f in e["fallas"]) + "</div>"
    msg = "Hola, mi equipo Frigidaire tiene una falla y necesito un técnico en Panamá"
    cuerpo = f'''{miga(1, ("Fallas", None))}<section class="sec"><div class="w txt"><h1>Fallas de electrodomésticos Frigidaire en Panamá: causas y soluciones</h1><p class="lead">{len(todas)} síntomas frecuentes de neveras, lavadoras y secadoras Frigidaire, con la causa probable y qué revisar.</p>{bloques}</div></section>{cta(msg)}'''
    escribir("fallas/index.html", f"Fallas de neveras, lavadoras y secadoras Frigidaire en Panamá | {TEL}", f"{len(todas)} fallas comunes de electrodomésticos Frigidaire en Panamá con causa probable y solución. Servicio técnico a domicilio. WhatsApp {TEL}.", cuerpo, [bc(("Fallas", None))], "0.8")

def paginas_zona_equipo():
    n = 0
    for i, (z, tipo, area) in enumerate(ZONAS):
        t1, t2 = TIPO_TXT[tipo]
        for j, (k, e) in enumerate(EQUIPOS.items()):
            msg = f"Hola, necesito servicio técnico para mi {e['sing']} Frigidaire en {z}"
            foto = foto_rot(k, i + j)
            fl = "".join(f'<li><a href="../../{furl(k, f)}"><b>{esc(f[0])}</b></a>: {esc(f[1])}</li>' for f in e["fallas"][:5])
            mant = e["mant"][(i + j) % len(e["mant"])]
            otros = "".join(f'<a href="{k2}.html">{esc(e2["corto"])} Frigidaire en {esc(z)}</a>' for k2, e2 in EQUIPOS.items() if k2 != k)
            vec = "".join(f'<a href="../{slug(v[0])}/{k}.html">{esc(e["corto"])} Frigidaire en {esc(v[0])}</a>' for v in [ZONAS[(i + d) % len(ZONAS)] for d in (1, 2, 3, 4, 5)])
            faq = [(f"¿Reparan {e['corto'].lower()} Frigidaire en {z}?", f"Sí. Damos servicio técnico a domicilio de {e['corto'].lower()} Frigidaire en {z} ({area}). Escríbenos por WhatsApp con el modelo y la falla y te confirmamos la visita."),
                   (f"¿Cuánto tardan en llegar a {z}?", "Coordinamos visitas en 24 a 48 horas en la mayoría de las zonas, según disponibilidad."),
                   (f"¿Cuánto cuesta el servicio técnico de {e['art']} Frigidaire en {z}?", "Te confirmamos el costo de la visita antes de ir y el de la reparación antes de empezar, según la falla y el modelo.")]
            cuerpo = f'''{miga(2, ("Zonas", "zonas/index.html"), (z, f"zonas/{slug(z)}/index.html"), (e["corto"], None))}<section class="hero chico"><div class="w hg"><div><span class="ey">{esc(area)}</span><h1>Reparación de {esc(e["corto"].lower())} Frigidaire en {esc(z)}</h1><p class="lead">Servicio técnico Frigidaire a domicilio en {esc(z)} para {esc(e["corto"].lower())}: diagnóstico en el sitio, costo claro antes de reparar y garantía en la pieza y la mano de obra.</p>
<div class="acc"><a class="btn wa lg" href="{wa(msg)}" target="_blank" rel="noopener" data-wa="hero">{ICONOS["wa"]} Escribir por WhatsApp</a></div></div><div class="hero-tarjeta foto">{fpic(foto, 2, None, False)}</div></div></section>
<section class="sec"><div class="w txt"><h2>Técnico de {esc(e["corto"].lower())} Frigidaire en {esc(z)}</h2><p>{esc(t1)}</p><p>{esc(t2)}</p>
{"".join(f"<h2>{esc(a.replace('{z}', z))}</h2><p>{esc(b.replace('{z}', z))}</p>" for a, b in [SEO_EQ[k][(i + j) % 5], SEO_EQ[k][(i + j + 2) % 5]])}<h2>Fallas de {esc(e["corto"].lower())} Frigidaire que atendemos en {esc(z)}</h2><ul class="lista">{fl}</ul>
<h2>Consejo de mantenimiento</h2><p>{esc(mant)}</p>
<h2>Preguntas frecuentes en {esc(z)}</h2>{faq_html(faq)}
<h2>Guías de {esc(e["corto"].lower())} Frigidaire</h2><div class="chips">{guias_chips(k, 2)}</div><h2>Otros equipos Frigidaire en {esc(z)}</h2><div class="chips">{otros}</div><h2>{esc(e["corto"])} Frigidaire en zonas cercanas</h2><div class="chips">{vec}</div><h2>Búsquedas relacionadas en {esc(z)}</h2><div class="chips">{"".join(f'<a href="../../{furl(k, f)}">{esc(e["sing"])} {MARCA} {esc(f[0].lower())} en {esc(z)}</a>' for f in e["fallas"])}<a href="../../servicio-tecnico-{MARCA.lower()}-cerca-de-mi-panama.html">Servicio técnico {MARCA} cerca de {esc(z)}</a><a href="../../telefono-servicio-tecnico-{MARCA.lower()}-panama.html">Teléfono servicio técnico {MARCA} {esc(z)}</a></div></div></section>{cta(msg, f"¿Tu {e['sing']} Frigidaire falla en {z}?")}'''
            escribir(zurl(k, z), f"Reparación de {e['corto']} Frigidaire en {z} | Panamá", f"Servicio técnico de {e['corto'].lower()} Frigidaire a domicilio en {z}, Panamá. Diagnóstico claro, garantía y visitas en 24-48 horas. WhatsApp {TEL}.", cuerpo,
                     [negocio_ld(area=z), faq_ld(faq), bc(("Zonas", "zonas/index.html"), (z, f"zonas/{slug(z)}/index.html"), (e["corto"], None))], "0.5")
            n += 1

HUBS = [
 dict(f="servicio-tecnico-frigidaire-panama.html", chip="Servicio técnico Frigidaire Panamá", t="Servicio Técnico Frigidaire Panamá: Cómo Funciona, Zonas y Contacto", h1="Servicio técnico Frigidaire en Panamá", foto=("sam-4", ALT["sam-4"]), foto2="sam-3",
      lead="Reparación a domicilio de neveras, lavadoras y secadoras Frigidaire en Ciudad de Panamá, San Miguelito y Panamá Oeste.",
      secs=[("Qué es el servicio técnico Frigidaire que ofrecemos", "Atendemos en tu casa u oficina los electrodomésticos Frigidaire que presentan fallas: neveras que no enfrían, lavadoras que no centrifugan o no desaguan, secadoras que no secan o no calientan. Revisamos el equipo, te explicamos la causa y confirmamos el costo antes de reparar."),
            ("Cómo funciona", "1) Escríbenos por WhatsApp con el equipo, el modelo y la falla. 2) Coordinamos la visita, normalmente en 24 a 48 horas. 3) Diagnosticamos en el sitio y te damos el costo. 4) Reparamos y probamos el equipo, con garantía sobre la pieza y la mano de obra."),
            ("Por qué elegir un técnico especializado en Frigidaire", "Conocer las fallas típicas de cada línea (inverter, carga frontal, French Door, dispensador, tarjetas de control) acorta el diagnóstico y evita cambiar piezas por prueba y error.")],
      faq=[("¿Qué incluye el servicio técnico Frigidaire a domicilio?", "Visita, diagnóstico en el sitio, explicación de la falla, cotización y reparación del equipo, con garantía."), ("¿En qué zonas de Panamá atienden?", "En Ciudad de Panamá, San Miguelito, Arraiján y La Chorrera, entre otras. Mira la lista de zonas de cobertura.")]),
 dict(f="telefono-servicio-tecnico-frigidaire-panama.html", chip="Teléfono servicio técnico Frigidaire Panamá", t="Teléfono y WhatsApp del Servicio Técnico Frigidaire en Panamá", h1="Teléfono del servicio técnico Frigidaire en Panamá", foto=("sam-6", ALT["sam-6"]),
      lead=f"Llama o escribe por WhatsApp al {TEL}. Atendemos de lunes a sábado de 7:00am a 6:00pm.",
      secs=[("Contacto directo", f"WhatsApp y teléfono: {TEL}. Es la forma más rápida de pedir una visita: envíanos una foto del equipo, la etiqueta con el modelo (suele estar en el costado o en la parte trasera) y una descripción de la falla."),
            ("Qué información enviar", "Tipo de equipo (nevera, lavadora o secadora), modelo, tiempo de uso, qué síntoma presenta, si muestra códigos de error y tu barrio o edificio. Con eso te confirmamos disponibilidad y costo de la visita."),
            ("Horario", "Lunes a sábado de 7:00am a 6:00pm. Los mensajes enviados fuera de horario se responden el siguiente día hábil.")],
      faq=[("¿Cuál es el número de servicio técnico Frigidaire en Panamá?", f"Nuestro WhatsApp y teléfono es {TEL}."), ("¿Atienden por WhatsApp?", "Sí, es el canal principal: ahí coordinamos la visita y confirmamos el costo.")]),
 dict(f="tecnico-frigidaire-a-domicilio-panama.html", chip="Técnico Frigidaire a domicilio", t="Técnico Frigidaire a Domicilio en Panamá | Neveras, Lavadoras y Secadoras", h1="Técnico Frigidaire a domicilio en Panamá", foto=("sam-4", FOTO_EQ["neveras"][1]), foto2="sam-1",
      lead="Vamos a tu casa, apartamento u oficina para revisar y reparar tu electrodoméstico Frigidaire sin que tengas que moverlo.",
      secs=[("Ventajas de la reparación a domicilio", "No tienes que cargar ni transportar una nevera o una lavadora. El técnico revisa el equipo donde está instalado, con su conexión eléctrica, su desagüe y su ventilación reales, que muchas veces son parte del problema."),
            ("Apartamentos y torres", "Coordinamos con la administración el horario, el ascensor de servicio y el ingreso de herramientas para que la visita sea rápida y sin inconvenientes."),
            ("Qué llevamos a la visita", "Herramientas de diagnóstico, multímetro y las piezas más frecuentes según el equipo. Si hace falta una pieza que no llevamos, te avisamos el plazo antes de empezar.")],
      faq=[("¿Cuánto tarda en llegar el técnico?", "Coordinamos visitas en 24 a 48 horas en la mayoría de las zonas."), ("¿Hacen la reparación en el momento?", "Muchas fallas se resuelven en la misma visita; si hay que pedir una pieza te avisamos antes.")]),
 dict(f="reparacion-electrodomesticos-frigidaire-panama.html", chip="Reparación de electrodomésticos Frigidaire", t="Reparación de Electrodomésticos Frigidaire en Panamá | Neveras, Lavadoras y Secadoras", h1="Reparación de electrodomésticos Frigidaire en Panamá", foto=("sam-4", ALT["sam-4"]), foto2="prod-torre",
      lead="Neveras, lavadoras y secadoras Frigidaire: reparación, mantenimiento e instalación con diagnóstico claro y garantía.",
      secs=[("Equipos que reparamos", "Neveras (French Door, Side by Side, congelador superior e inferior, con dispensador), lavadoras de carga superior y frontal y secadoras split e inverter."),
            ("Tipos de servicio", "Reparación de fallas, diagnóstico, mantenimiento preventivo e instalación. Cada servicio incluye explicación de la falla y costo confirmado antes de empezar."),
            ("Fallas más comunes", "La nevera que no enfría, el congelador con escarcha, la lavadora que no desagua o no centrifuga, y la secadora que no seca son las consultas más frecuentes en Panamá.")],
      faq=[("¿Reparan todas las líneas de Frigidaire?", "Atendemos neveras, lavadoras y secadoras. Para otros equipos, escríbenos y te decimos si podemos ayudarte."), ("¿Vale la pena reparar un equipo viejo?", "Si la falla es de una pieza accesible, casi siempre sí. Si no vale la pena, te lo decimos con honestidad.")]),
 dict(f="servicio-tecnico-frigidaire-cerca-de-mi-panama.html", chip="Servicio técnico Frigidaire cerca de mí", t="Servicio Técnico Frigidaire Cerca de Mí en Panamá | Visita a Domicilio", h1="Servicio técnico Frigidaire cerca de mí en Panamá", foto=("sam-3", ALT["sam-3"]),
      lead="Si buscas un técnico Frigidaire cerca de tu casa en Panamá, atendemos a domicilio en más de 30 barrios y corregimientos.",
      secs=[("Cobertura por zonas", "Llegamos a San Francisco, Bella Vista, Obarrio, Marbella, Costa del Este, Punta Pacífica, Paitilla, Betania, San Miguelito, Albrook, Arraiján, La Chorrera y más. Elige tu zona abajo."),
            ("No tienes que ir a ningún lado", "Como el servicio es a domicilio, no necesitas buscar un taller cercano ni transportar tu equipo: nosotros vamos a donde está.")],
      faq=[("¿Mi zona tiene cobertura?", "Mira la lista de zonas o escríbenos con tu barrio. Si no aparece, es posible que igualmente lleguemos.")], zonas=True),
 dict(f="repuestos-frigidaire-panama.html", chip="Repuestos Frigidaire Panamá", t="Repuestos para Neveras, Lavadoras y Secadoras Frigidaire en Panamá", h1="Repuestos Frigidaire en Panamá", foto=("prod-torre", ALT["prod-torre"]), foto2="prod-nevera-sbs",
      lead="Cuando tu electrodoméstico Frigidaire necesita una pieza, la conseguimos e instalamos en la visita o en la siguiente, con garantía.",
      secs=[("Piezas más solicitadas", "Neveras: ventilador del evaporador, sensores, tarjeta de control, resistencia de descongelación, filtro de agua, empaques. Lavadoras: bomba de desagüe, válvula de entrada, seguro de puerta, amortiguadores, rodamientos. Secadoras: resistencia, termostatos, correa."),
            ("Cómo pedir una pieza", "Envíanos por WhatsApp el modelo del equipo (etiqueta) y una foto o descripción de la falla. Con eso identificamos la pieza que necesitas y te confirmamos plazo y costo."),
            ("Instalación incluida", "Si nos encargamos de la reparación, instalamos la pieza y la probamos. La pieza instalada y la mano de obra tienen garantía.")],
      faq=[("¿Venden repuestos sin instalación?", "Escríbenos con el modelo y la pieza que necesitas y te decimos qué podemos ofrecerte."), ("¿Cuánto tardan en conseguir una pieza?", "Depende de la pieza y del modelo; te confirmamos el plazo antes de empezar la reparación.")]),
 dict(f="cuanto-cuesta-reparar-electrodomesticos-frigidaire-panama.html", chip="¿Cuánto cuesta reparar un Frigidaire?", t="¿Cuánto Cuesta Reparar una Nevera, Lavadora o Secadora Frigidaire en Panamá?", h1="¿Cuánto cuesta reparar un electrodoméstico Frigidaire en Panamá?", foto=None,
      lead="El costo depende de la falla, la pieza y el modelo. Te lo confirmamos antes de la visita y antes de empezar la reparación.",
      secs=[("De qué depende el costo", "Del tipo de equipo, el modelo, la falla, la pieza que haya que reemplazar y la zona donde estás. Una limpieza de filtro o desagüe no cuesta lo mismo que cambiar una tarjeta de control o un compresor."),
            ("Cómo evitar sorpresas", "Pide siempre que el técnico te explique la falla y te dé el costo antes de empezar. Nosotros lo hacemos así: diagnóstico, explicación, costo y solo entonces reparación."),
            ("¿Reparar o reemplazar?", "Si la reparación cuesta una parte importante del valor de un equipo nuevo y el equipo es muy viejo, te explicamos las opciones con honestidad para que decidas.")],
      faq=[("¿Cuánto cuesta la visita de diagnóstico?", "Escríbenos por WhatsApp con el equipo, el modelo y la falla; te confirmamos el costo de la visita antes de ir."), ("¿El diagnóstico se descuenta de la reparación?", "Te explicamos las condiciones por WhatsApp antes de agendar la visita.")]),
 dict(f="reparacion-neveras-frigidaire-french-door-panama.html", chip="Neveras Frigidaire French Door", t="Reparación de Neveras Frigidaire French Door y Side by Side en Panamá", h1="Reparación de neveras Frigidaire French Door en Panamá", foto=("prod-nevera-sbs", ALT["prod-nevera-sbs"]), foto2="sam-4",
      lead="Atendemos neveras Frigidaire French Door, Side by Side y de congelador superior a domicilio en Ciudad de Panamá.",
      secs=[("Fallas frecuentes de las neveras Frigidaire", "La nevera que no enfría, la escarcha en el congelador, el dispensador de agua, la fábrica de hielo, las fugas de agua y los ruidos del ventilador o del compresor son las consultas más comunes."),
            ("Neveras Frigidaire con dispensador de agua y hielo", "Revisamos filtro, manguera, válvula de entrada, sensor y fábrica de hielo, y te explicamos qué pieza hay que cambiar antes de empezar."),
            ("Cómo pedir la visita", "Escríbenos por WhatsApp con el modelo de tu nevera Frigidaire y una foto o video del problema.")],
      faq=[("¿Reparan neveras Frigidaire French Door?", "Sí, atendemos French Door, Side by Side y de congelador superior o inferior."), ("¿Cuánto tarda la visita?", "Coordinamos visitas en 24 a 48 horas en la mayoría de las zonas.")]),
 dict(f="reparacion-lavadoras-frigidaire-carga-superior-frontal-panama.html", chip="Lavadoras Frigidaire carga superior y frontal", t="Reparación de Lavadoras Frigidaire de Carga Superior y Frontal en Panamá", h1="Reparación de lavadoras Frigidaire en Panamá: carga superior y frontal", foto=("prod-lavadora-sup", ALT["prod-lavadora-sup"]), foto2="sam-6",
      lead="Lavadoras Frigidaire de carga superior y frontal: vibración, desagüe, entrada de agua, fugas y códigos de error.",
      secs=[("Lavadoras Frigidaire que reparamos", "Carga superior con agitador, carga frontal, lavadoras con sensores y torres de lavado."),
            ("Fallas más consultadas", "No centrifuga, no desagua, no llena de agua, gotea, vibra de más o muestra un código de error. Mira nuestra guía de códigos de error."),
            ("Cómo pedir la visita", "Escríbenos por WhatsApp con el modelo, el síntoma y el código que muestra la pantalla.")],
      faq=[("¿Reparan lavadoras Frigidaire de carga superior?", "Sí, atendemos carga superior y frontal."), ("¿Qué hago si muestra un código?", "Anótalo, apaga y desconecta unos minutos y escríbenos con el modelo.")]),
 dict(f="garantia-frigidaire-panama-que-hacer.html", chip="Garantía Frigidaire en Panamá", t="Garantía Frigidaire en Panamá: Qué Hacer si tu Equipo Falla", h1="Garantía Frigidaire en Panamá: qué hacer si tu equipo falla", foto=("sam-5", ALT["sam-5"]),
      lead="Antes de reparar, verifica si tu equipo sigue en garantía de fábrica. Te explicamos cómo y qué opciones tienes.",
      secs=[("Cómo saber si tu equipo está en garantía", "Revisa la factura de compra, la fecha y el plazo indicado por el vendedor o el fabricante. Guarda siempre el comprobante: lo vas a necesitar para cualquier reclamo."),
            ("Si el equipo ya no está en garantía", "Podemos revisarlo a domicilio, explicarte la falla y repararlo. Nuestra reparación incluye garantía propia sobre la pieza reemplazada y la mano de obra."),
            ("Antes de pagar una reparación", "Si tu equipo es reciente, consulta primero las condiciones de garantía del vendedor. Durante nuestro diagnóstico también te lo recordamos para que tomes la mejor decisión.")],
      faq=[("¿Cuánto dura la garantía de la reparación?", "Se confirma por escrito al momento del servicio, antes de que pagues."), ("¿Qué hago si la falla vuelve?", "Escríbenos por WhatsApp con la fecha del servicio; si está dentro del plazo, coordinamos la revisión.")]),
 dict(f="cambio-filtro-nevera-frigidaire-panama.html", chip="Cambio de filtro de nevera Frigidaire", t="Cambio de Filtro de Agua de Nevera Frigidaire en Panamá | Cada Cuánto", h1="Cambio de filtro de agua de nevera Frigidaire en Panamá", foto=("prod-nevera-sbs", ALT["prod-nevera-sbs"]), foto2="sam-4",
      lead="Cuando la nevera muestra «cambiar filtro» o el agua sale lenta o con mal sabor, es momento de reemplazar el filtro. Lo hacemos a domicilio.",
      secs=[("Cada cuánto cambiar el filtro", "Por lo general cada 6 meses, o antes si el agua sale lenta, con sabor u olor extraño, o si la nevera muestra el aviso de filtro. En zonas con agua con más sedimentos puede necesitar cambio más seguido."),
            ("Señales de que el filtro está vencido", "Luz o aviso de cambio de filtro, flujo de agua lento en el dispensador, hielo con mal sabor, o fábrica de hielo que produce poco."),
            ("Qué hacemos en la visita", "Identificamos el modelo, instalamos el filtro correcto, purgamos el sistema y reiniciamos el aviso. Si el problema de agua continúa, revisamos manguera y válvula de entrada.")],
      faq=[("¿Cómo reinicio el aviso de filtro?", "En la mayoría de neveras con dispensador se mantiene presionado un botón del panel durante unos segundos después de cambiar el filtro; el método exacto depende del modelo."), ("¿Puedo cambiar el filtro yo mismo?", "En muchos modelos es sencillo, pero si tienes dudas, el agua sale lenta o hay fugas, podemos hacerlo nosotros.")]),
 dict(f="servicio-tecnico-frigidaire-24-horas-panama.html", chip="Servicio técnico Frigidaire urgente", t="Servicio Técnico Frigidaire Urgente en Panamá | Visitas en 24 a 48 Horas", h1="Servicio técnico Frigidaire urgente en Panamá", foto=("sam-6", ALT["sam-6"]),
      lead="Si tu nevera dejó de enfriar o tu lavadora gotea, escríbenos de inmediato: priorizamos las fallas urgentes y coordinamos visitas en 24 a 48 horas.",
      secs=[("Qué fallas son urgentes", "Nevera que no enfría o se apaga y prende sola, lavadora que gotea o inunda, equipos que saltan el breaker o huelen a quemado. En esos casos desconecta el equipo y escríbenos."),
            ("Mientras llega el técnico", "En la nevera, evita abrir la puerta para conservar el frío. En la lavadora, cierra la llave de agua y desconecta. En secadoras, apaga y desconecta si hay olor a quemado."),
            ("Cómo pedir una visita urgente", f"Escríbenos por WhatsApp al {TEL} con tu zona, el equipo y el síntoma. Te confirmamos la disponibilidad más cercana.")],
      faq=[("¿Atienden emergencias?", "Priorizamos las fallas urgentes; la disponibilidad se confirma por WhatsApp según tu zona."), ("¿Atienden fines de semana?", "Trabajamos de lunes a sábado de 7:00am a 6:00pm.")]),
 dict(f="codigos-de-error-lavadora-frigidaire-panama.html", chip="Códigos de error lavadora Frigidaire", t="Códigos de Error de Lavadora Frigidaire: Qué Hacer y Cuándo Llamar al Técnico", h1="Códigos de error de lavadoras Frigidaire: qué significan", foto=("sam-6", FOTO_FALLA["lavadoras"][1]),
      lead="Qué hacer cuando tu lavadora Frigidaire muestra un código de error y qué revisar antes de llamar al técnico.",
      secs=[("Cómo leer el código", "Cada modelo Frigidaire usa códigos distintos. Anota el código exacto que aparece en la pantalla y el modelo (etiqueta en la tapa o en el marco de la puerta)."),
            ("Si el problema es de desagüe", "Revisa el filtro de desagüe y que la manguera no esté doblada ni tapada. Si persiste, puede ser la bomba."),
            ("Si el problema es de entrada de agua", "Verifica que las llaves estén abiertas y limpia las mallas de las mangueras. Si sigue, puede ser la válvula de entrada."),
            ("Si el problema es la puerta", "Revisa que cierre bien y que no haya prendas atrapadas; si continúa, el seguro de la puerta puede necesitar reemplazo."),
            ("Si el problema es vibración o desbalance", "Reparte la ropa, evita lavar una sola prenda pesada y verifica que las patas toquen el piso."),
            ("Cuándo llamar", "Si el código reaparece, hay agua en el piso o la lavadora se apaga sola, no la sigas usando y escríbenos con el modelo y el código.")],
      faq=[("¿Cómo reinicio mi lavadora Frigidaire cuando muestra un código?", "Apágala, desconéctala unos minutos, vuelve a conectarla y prueba. Si el código regresa, escríbenos."), ("¿Un código de error significa que se dañó la tarjeta?", "No necesariamente: muchos códigos indican problemas simples como desagüe, agua o puerta.")]),
 dict(f="servicio-frigidaire-panama-donde-reparar.html", chip="Dónde reparar mi Frigidaire en Panamá", t="¿Dónde Reparar un Electrodoméstico Frigidaire en Panamá? | A Domicilio", h1="¿Dónde reparar un electrodoméstico Frigidaire en Panamá?", foto=None,
      lead="No tienes que ir a un taller: te visitamos en casa. Esta guía explica tus opciones y cómo pedir la visita.",
      secs=[("Opciones para reparar tu equipo", "Puedes consultar las condiciones de garantía del vendedor si el equipo es reciente, llevarlo a un taller o pedir un técnico a domicilio. Para equipos grandes como neveras y lavadoras, la visita a domicilio suele ser más cómoda."),
            ("Cómo pedir nuestra visita", f"Escríbenos por WhatsApp al {TEL} con el equipo, el modelo y la falla. Te confirmamos la disponibilidad en tu zona, normalmente en 24 a 48 horas."),
            ("Qué incluye", "Diagnóstico en el sitio, explicación de la falla, costo confirmado antes de reparar y garantía sobre la pieza y la mano de obra.")],
      faq=[("¿Tengo que llevar el equipo a un taller?", "No. Vamos a tu casa u oficina en Ciudad de Panamá, San Miguelito y Panamá Oeste."), ("¿Qué marca reparan?", "Nos especializamos en electrodomésticos Frigidaire: neveras, lavadoras y secadoras.")]),
]

def paginas_hubs():
    for h in HUBS:
        msg = f"Hola, vi su página '{h['h1']}' y necesito servicio técnico Frigidaire en Panamá"
        foto = f'<div class="hero-tarjeta foto">{fpic(h["foto"][0], 0, h["foto"][1], False)}</div>' if h["foto"] else f'<div class="hero-tarjeta"><b>{TEL}</b><small>{HORARIO}</small></div>'
        partes = [f"<h2>{esc(a)}</h2><p>{esc(b)}</p>" for a, b in h["secs"]]
        if h.get("foto2"): partes.insert(1, f'<div class="fotoc">{fpic(h["foto2"], 0)}</div>')
        partes += [f"<h2>{esc(a)}</h2><p>{esc(b)}</p>" for a, b in HUB_EXTRA]
        secs = "".join(partes)
        zs = '<h2>Zonas de cobertura</h2><div class="chips">' + "".join(f'<a href="zonas/{slug(z[0])}/index.html">{esc(z[0])}</a>' for z in ZONAS) + "</div>" if h.get("zonas") else ""
        rel = "".join(f'<a href="{o["f"]}">{esc(o["chip"])}</a>' for o in HUBS if o is not h)
        cuerpo = f'''{miga(0, (h["h1"], None))}<section class="hero chico"><div class="w hg"><div><span class="ey">Servicio técnico Frigidaire Panamá</span><h1>{esc(h["h1"])}</h1><p class="lead">{esc(h["lead"])}</p>
<div class="acc"><a class="btn wa lg" href="{wa(msg)}" target="_blank" rel="noopener" data-wa="hero">{ICONOS["wa"]} Escribir por WhatsApp</a></div></div>{foto}</div></section>
<section class="sec"><div class="w txt">{secs}<h2>Equipos Frigidaire que atendemos</h2>{tarjetas_eq(0)}{zs}<h2>Preguntas frecuentes</h2>{faq_html(h["faq"])}<h2>Búsquedas relacionadas</h2><div class="chips">{rel}</div></div></section>{cta(msg)}'''
        ld = [negocio_ld(), faq_ld(h["faq"]), bc((h["h1"], None))]
        escribir(h["f"], h["t"] if len(h["t"]) < 75 else h["h1"] + f" | {NOMBRE}", f"{h['lead']} WhatsApp {TEL}.", cuerpo, ld, "0.9")

# ------------------------------------------------------------ subpáginas por sección
EQ_REP = {
 "neveras": "ventilador del evaporador, sensores de temperatura, tarjeta de control, resistencia de descongelación, termostato de deshielo, empaques de puertas, válvula de agua, manguera y fábrica de hielo",
 "lavadoras": "bomba de desagüe, válvula de entrada de agua, seguro de la puerta, amortiguadores, rodamientos, tarjeta de control, sensor de nivel y mangueras",
 "secadoras": "resistencia de calor, termostatos y fusible térmico, sensor de humedad, motor, correa, rodillos, tarjeta de control y ducto de salida",
}
ATENC = [("sam-5", "Técnico y asesora de servicio conversando en una oficina de atención al cliente", 1024, 765), ("sam-6", "Técnico y asesora de servicio en una oficina de atención", 1024, 765)]
SUBS = [("modelos", "Modelos y líneas", "Modelos de {c} Frigidaire que reparamos en Panamá"),
        ("costo", "Costo de reparación", "¿Cuánto cuesta reparar {a} Frigidaire en Panamá?"),
        ("repuestos", "Repuestos", "Repuestos para {c} Frigidaire en Panamá"),
        ("urgente", "Servicio urgente", "Servicio técnico urgente de {c} Frigidaire en Panamá"),
        ("reparar-o-reemplazar", "¿Reparar o reemplazar?", "¿Reparar o reemplazar {a} Frigidaire?")]

def subs_chips(k, e, depth, actual=None):
    r = R(depth)
    return "".join(f'<a href="{r}electrodomesticos/{k}/{s}.html">{esc(t)} de {esc(e["corto"].lower())}</a>' for s, t, _ in SUBS if s != actual)

def paginas_subequipo():
    for ek, e in EQUIPOS.items():
        base = f"electrodomesticos/{ek}/"
        msg = f"Hola, necesito servicio técnico para mi {e['sing']} Frigidaire en Panamá"
        urg = [f for f in e["fallas"] if f[2] == "Urgente"]
        for j, (s, etiqueta, h1) in enumerate(SUBS):
            H1 = h1.format(c=e["corto"].lower(), a=e["art"])
            foto = ATENC[j % 2] if s in ("costo", "reparar-o-reemplazar") else None
            if s == "modelos":
                cuerpo_t = (f"<p class=\"lead\">Atendemos {esc(e['art'])} Frigidaire de las líneas más comunes en Panamá, en casas, apartamentos y oficinas.</p><h2>Líneas y tipos que atendemos</h2><ul class=\"lista\">{''.join(f'<li>{esc(m)}</li>' for m in e['modelos'])}</ul>"
                            f"<h2>¿Cómo encuentro el modelo de mi {esc(e['sing'])} Frigidaire?</h2><p>Casi siempre hay una etiqueta con el número de modelo y de serie en el costado, en la parte trasera o dentro de la puerta del equipo. Envíanos una foto de esa etiqueta por WhatsApp y te confirmamos si podemos atenderlo y cuánto tardaría la visita.</p>"
                            f"<h2>Fallas más frecuentes según el tipo</h2><ul class=\"lista\">{''.join(f'<li><a href=\"../../{furl(ek, f)}\">{esc(f[0])}</a></li>' for f in e['fallas'])}</ul>")
            elif s == "costo":
                cuerpo_t = (f"<p class=\"lead\">El costo de reparar {esc(e['art'])} Frigidaire depende de la falla, la pieza y el modelo. Esto es lo que influye y cómo evitar sorpresas.</p><h2>De qué depende el costo</h2><ul class=\"lista\"><li><b>La falla:</b> una limpieza o ajuste no cuesta lo mismo que cambiar una tarjeta electrónica o el compresor.</li><li><b>La pieza:</b> disponibilidad y precio según el modelo.</li><li><b>La visita:</b> zona de {esc('Panamá')} y horario.</li><li><b>Mano de obra:</b> tiempo que toma el diagnóstico y la reparación.</li></ul>"
                            f"<h2>Cómo trabajamos el costo</h2><p>Te confirmamos el valor de la visita antes de ir. En el sitio diagnosticamos, te explicamos la falla y te damos el costo de la reparación antes de empezar. Si no estás de acuerdo, no reparamos.</p>"
                            f"<h2>Fallas que suelen ser más económicas</h2><p>Casi siempre lo son las que se resuelven con limpieza, ajuste o piezas pequeñas: {esc(', '.join(f[0].lower() for f in e['fallas'] if f[2] == 'Vigilar')[:240])}.</p>")
            elif s == "repuestos":
                cuerpo_t = (f"<p class=\"lead\">Cuando {esc(e['art'])} Frigidaire necesita una pieza, la identificamos por el modelo y la instalamos en la visita o en la siguiente.</p><h2>Piezas que cambiamos con más frecuencia</h2><p>{esc(EQ_REP[ek].capitalize())}.</p>"
                            f"<h2>Cómo identificamos la pieza correcta</h2><p>Con la etiqueta del modelo y el síntoma. Así evitamos cambiar piezas por prueba y error. Envíanos la foto de la etiqueta por WhatsApp.</p><h2>Instalación y garantía</h2><p>La pieza instalada y la mano de obra tienen garantía. Si hay que pedir una pieza, te avisamos el plazo antes de empezar.</p>")
            elif s == "urgente":
                li = "".join(f"<li><a href=\"../../{furl(ek, f)}\"><b>{esc(f[0])}</b></a>: {esc(f[3])}</li>" for f in (urg or e['fallas'][:3]))
                cuerpo_t = (f"<p class=\"lead\">Si {esc(e['art'])} Frigidaire presenta una falla urgente, escríbenos de inmediato por WhatsApp. Priorizamos estos casos y coordinamos visitas en 24 a 48 horas.</p><h2>Fallas que consideramos urgentes</h2><ul class=\"lista\">{li}</ul>"
                            f"<h2>Qué hacer mientras llega el técnico</h2><ul class=\"lista\"><li>Si hay olor a quemado, chispas o humedad en la conexión eléctrica, desconecta el equipo.</li><li>No lo reinicies repetidamente: puedes dañar el compresor o la tarjeta.</li><li>Ten a la mano el modelo y una foto o video del problema.</li></ul>")
            else:
                cuerpo_t = (f"<p class=\"lead\">Decidir entre reparar o reemplazar {esc(e['art'])} Frigidaire depende de la edad, la falla y el costo. Te lo explicamos con claridad.</p><h2>Conviene reparar cuando…</h2><ul class=\"lista\"><li>El equipo tiene pocos años y está en buen estado general.</li><li>La falla es de una pieza accesible (sensor, ventilador, bomba, válvula, tarjeta).</li><li>El costo de la reparación es una fracción pequeña del valor de uno nuevo.</li></ul>"
                            f"<h2>Conviene reemplazar cuando…</h2><ul class=\"lista\"><li>El equipo es muy antiguo y tiene varias fallas seguidas.</li><li>El daño es en una pieza principal muy costosa.</li><li>El consumo de energía es muy alto frente a un equipo nuevo.</li></ul><h2>Nuestro criterio</h2><p>Primero diagnosticamos, luego te damos las opciones y el costo. Si no vale la pena reparar, te lo decimos con honestidad.</p>")
            fotoh = f'<div class="fotoc">{pic(foto[0], foto[1], 2, foto[2], foto[3])}</div>' if foto else ""
            faq = [(f"¿Atienden {e['corto'].lower()} Frigidaire en toda la ciudad de Panamá?", "Damos servicio a domicilio en Ciudad de Panamá, San Miguelito y Panamá Oeste. Escríbenos con tu barrio para confirmarlo."), ("¿Cuánto tarda la visita?", "Coordinamos visitas en 24 a 48 horas en la mayoría de las zonas."), ("¿La reparación tiene garantía?", "Sí, sobre la pieza reemplazada y la mano de obra. El plazo se confirma antes de empezar.")]
            cuerpo = f'''{miga(2, (e["nombre"], base + "index.html"), (etiqueta, None))}<section class="sec"><div class="w txt"><h1>{esc(H1)}</h1>{cuerpo_t}{fotoh}<h2>Guías de {esc(e["corto"].lower())} Frigidaire</h2><div class="chips">{guias_chips(ek, 2)}</div><h2>Más sobre {esc(e["corto"].lower())} Frigidaire</h2><div class="chips"><a href="index.html">Servicio técnico de {esc(e["corto"].lower())}</a><a href="fallas-comunes.html">Fallas comunes</a><a href="mantenimiento.html">Mantenimiento</a>{subs_chips(ek, e, 2, s)}</div><h2>Preguntas frecuentes</h2>{faq_html(faq)}</div></section>{cta(msg)}'''
            escribir(base + s + ".html", f"{H1} | Panamá" if len(H1) < 52 else H1, f"{H1} Servicio técnico Frigidaire a domicilio en Panamá. Diagnóstico claro, costo confirmado y garantía. WhatsApp {TEL}.", cuerpo,
                     [negocio_ld(), faq_ld(faq), bc((e["nombre"], base + "index.html"), (etiqueta, None))], "0.6")

def paginas_servicio_equipo():
    for sk, (titulo, corto, desc, puntos) in SERVICIOS.items():
        for j, (ek, e) in enumerate(EQUIPOS.items()):
            ruta = f"servicios/{sk}-{ek}-frigidaire-panama.html"
            H1 = f"{corto} de {e['corto'].lower()} Frigidaire en Panamá"
            msg = f"Hola, quiero agendar: {corto.lower()} de mi {e['sing']} Frigidaire en Panamá"
            fl = "".join(f'<li><a href="../{furl(ek, f)}">{esc(f[0])}</a></li>' for f in e["fallas"][:5])
            foto = ATENC[(j + len(sk)) % 2]
            faq = [(f"¿Qué incluye el servicio de {corto.lower()} de {e['art']} Frigidaire?", "; ".join(puntos[:3]) + "."), ("¿Dónde lo hacen?", "En tu casa, apartamento u oficina en Ciudad de Panamá, San Miguelito y Panamá Oeste."), ("¿Cuánto cuesta?", "Te confirmamos el costo por WhatsApp antes de agendar, según el equipo y el servicio.")]
            cuerpo = f'''{miga(1, ("Servicios", f"servicios/{sk}-frigidaire-panama.html"), (e["corto"], None))}<section class="sec"><div class="w txt"><h1>{esc(H1)}</h1><p class="lead">{esc(desc)}</p>
<h2>{esc(corto)} de {esc(e["corto"].lower())} Frigidaire: qué incluye</h2><ul class="lista">{"".join(f"<li>{esc(p)}</li>" for p in puntos)}</ul>
<div class="fotoc">{pic(foto[0], foto[1], 1, foto[2], foto[3])}</div>
<h2>Qué revisamos en {esc(e["art"])} Frigidaire</h2><p>{esc(EQ_REP[ek].capitalize())}.</p><h2>Fallas relacionadas</h2><ul class="lista">{fl}</ul>
<h2>Más información</h2><div class="chips"><a href="../electrodomesticos/{ek}/index.html">Servicio técnico de {esc(e["corto"].lower())} Frigidaire</a><a href="{sk}-frigidaire-panama.html">{esc(corto)}</a><a href="../electrodomesticos/{ek}/costo.html">Costo de reparación</a></div>
<h2>Preguntas frecuentes</h2>{faq_html(faq)}</div></section>{cta(msg)}'''
            escribir(ruta, f"{H1} | {NOMBRE}" if len(H1) < 40 else H1, f"{corto} de {e['corto'].lower()} Frigidaire a domicilio en Panamá. {desc[:90]} WhatsApp {TEL}.", cuerpo, [negocio_ld(), faq_ld(faq), bc(("Servicios", f"servicios/{sk}-frigidaire-panama.html"), (e["corto"], None))], "0.6")

def main():
    (OUT / "zonas-de-cobertura.html").unlink(missing_ok=True)
    for d in ["electrodomesticos", "servicios", "zonas", "blog", "fallas", "busquedas"]:
        shutil.rmtree(OUT / d, ignore_errors=True)
    estaticos(); pagina_inicio(); paginas_equipo(); paginas_servicio(); paginas_zona(); paginas_blog(); pagina_diagnostico(); paginas_info(); paginas_hubs(); paginas_subequipo(); paginas_servicio_equipo(); paginas_fallas(); paginas_zona_equipo(); paginas_busquedas(); paginas_mapa(); indices()
    z = AQUI.parent.parent / "entrega" / "servicio-tecnico-frigidaire-panama.zip"
    z.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in OUT.rglob("*"):
            if p.is_file() and "_fuente" not in p.parts and "__pycache__" not in p.parts:
                zf.write(p, p.relative_to(OUT).as_posix())
    print(f"OK: {len(PAGINAS)} páginas → {z.name}")
main()
