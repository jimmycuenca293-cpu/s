# -*- coding: utf-8 -*-
"""Genera el sitio estático «Servicio Técnico Samsung Panamá» (carpeta ..) y el zip."""
import html, json, re, shutil, sys, unicodedata, zipfile
from pathlib import Path
from urllib.parse import quote
from contenido import *

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
FOTO_EQ = {"neveras": ("tecnico-nevera", "Técnico reparando una refrigeradora Samsung en una cocina de Panamá"), "lavadoras": ("tecnico-lavadora-2", "Técnico revisando una lavadora Samsung en una cocina de Panamá")}

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
            f'<link rel="icon" href="{r}images/logo/favicon.svg" type="image/svg+xml"><meta property="og:type" content="website"><meta property="og:title" content="{esc(titulo)}">'
            f'<meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{DOMINIO}/{og}"><meta property="og:locale" content="es_PA">'
            f'<meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#1428a0">'
            f'<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap">'
            f'<link rel="stylesheet" href="{r}css/estilos.css">{lds}{extra}{gtm}</head><body>')

def menu(depth):
    r = R(depth)
    eq = "".join(f'<a href="{r}electrodomesticos/{k}/index.html">{esc(v)}</a>' for k, v in NAV_EQ)
    sv = "".join(f'<a href="{r}servicios/{k}-samsung-panama.html">{esc(v[1])}</a>' for k, v in SERVICIOS.items())
    return (f'<header class="top"><div class="barra"><div class="w"><span>Servicio técnico Samsung en Ciudad de Panamá · {HORARIO}</span>'
            f'<a href="{wa()}" target="_blank" rel="noopener" data-wa="barra">{ICONOS["wa"]} {TEL}</a></div></div>'
            f'<div class="w nav"><a class="logo" href="{r}index.html" aria-label="{NOMBRE}"><span class="lg-i">{ICONOS["wrench"]}</span><span class="lg-t">Servicio Técnico<b>Samsung</b><small>Panamá</small></span></a>'
            f'<nav aria-label="Principal"><div class="dd"><a href="{r}index.html#equipos">Electrodomésticos ▾</a><div class="pn">{eq}</div></div>'
            f'<div class="dd"><a href="{r}index.html#servicios">Servicios ▾</a><div class="pn">{sv}</div></div>'
            f'<a href="{r}diagnostico.html">Diagnóstico</a><a href="{r}fallas/index.html">Fallas</a><a href="{r}zonas-de-cobertura.html">Zonas</a><a href="{r}blog/index.html">Blog</a><a href="{r}nosotros.html">Nosotros</a>'
            f'<a class="btn wa" href="{wa("Hola, necesito servicio técnico para mi equipo Samsung en Panamá")}" target="_blank" rel="noopener" data-wa="menu">{ICONOS["wa"]} WhatsApp</a></nav>'
            f'<button class="burger" type="button" aria-label="Abrir menú" aria-expanded="false"><span></span></button></div>'
            f'<div class="mov" hidden><b>Electrodomésticos</b>{eq}<b>Servicios</b>{sv}<b>Más</b><a href="{r}diagnostico.html">Diagnóstico rápido</a><a href="{r}fallas/index.html">Fallas por equipo</a><a href="{r}zonas-de-cobertura.html">Zonas de cobertura</a><a href="{r}blog/index.html">Blog</a><a href="{r}nosotros.html">Nosotros</a><a href="{r}garantia.html">Garantía</a><a href="{r}preguntas-frecuentes.html">Preguntas frecuentes</a></div></header><main>')

def pie(depth):
    r = R(depth)
    zs = "".join(f'<a href="{r}zonas/{slug(z[0])}.html">{esc(z[0])}</a>' for z in ZONAS[:8])
    eq = "".join(f'<a href="{r}electrodomesticos/{k}/index.html">{esc(v["nombre"])}</a>' for k, v in EQUIPOS.items())
    sv = "".join(f'<a href="{r}servicios/{k}-samsung-panama.html">{esc(v[1])}</a>' for k, v in SERVICIOS.items())
    return (f'</main><footer class="pie"><div class="w cols"><div><a class="logo pl-logo" href="{r}index.html" aria-label="{NOMBRE}"><span class="lg-i">{ICONOS["wrench"]}</span><span class="lg-t">Servicio Técnico<b>Samsung</b><small>Panamá</small></span></a><p>Servicio técnico Samsung en Panamá: reparación a domicilio de neveras, lavadoras, secadoras y aires acondicionados Samsung, con cobertura en Ciudad de Panamá, San Miguelito y Panamá Oeste.</p>'
            f'<a class="btn wa" href="{wa()}" target="_blank" rel="noopener" data-wa="pie">{ICONOS["wa"]} {TEL}</a><p class="hor">{HORARIO}</p></div>'
            f'<div><b>Electrodomésticos</b>{eq}</div><div><b>Servicios</b>{sv}<a href="{r}diagnostico.html">Diagnóstico rápido</a><a href="{r}garantia.html">Garantía</a></div>'
            f'<div><b>Zonas</b>{zs}<a href="{r}zonas-de-cobertura.html">Ver todas las zonas</a></div></div>'
            f'<div class="w busq"><b>Búsquedas frecuentes</b><div class="chips">{busquedas_chips(depth)}</div></div>'
            f'<div class="w legal"><span>© 2026 {NOMBRE}. Samsung es una marca registrada de Samsung Electronics Co., Ltd. Este sitio no es operado por Samsung.</span>'
            f'<span><a href="{r}privacidad.html">Privacidad</a> · <a href="{r}aviso-legal.html">Aviso legal</a> · <a href="{r}preguntas-frecuentes.html">Preguntas frecuentes</a></span></div></footer>'
            f'<a class="wa-flot" href="{wa("Hola, necesito servicio técnico para mi equipo Samsung en Panamá")}" target="_blank" rel="noopener" data-wa="flotante" aria-label="Escribir por WhatsApp">{ICONOS["wa"]}<span>Escríbenos</span></a>'
            f'<script src="{r}js/main.js" defer></script></body></html>')

def escribir(ruta, titulo, desc, cuerpo, ld=None, prioridad="0.7", og="images/og.jpg"):
    depth = ruta.count("/")
    p = OUT / ruta
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(cabeza(ruta, titulo, desc, ld, og) + menu(depth) + cuerpo + pie(depth), encoding="utf-8")
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

def cta(msg, titulo="¿Necesitas servicio técnico Samsung en Panamá?", texto="Escríbenos por WhatsApp con el equipo, el modelo y la falla. Te confirmamos disponibilidad para tu zona en minutos.", fuente="cta"):
    return (f'<section class="sec"><div class="w"><div class="cta"><div><h2>{esc(titulo)}</h2><p>{esc(texto)}</p></div>'
            f'<a class="btn wa lg" href="{wa(msg)}" target="_blank" rel="noopener" data-wa="{fuente}">{ICONOS["wa"]} Escribir por WhatsApp</a></div></div></section>')

def negocio_ld(nombre=None, area=None):
    return {"@context": "https://schema.org", "@type": "LocalBusiness", "@id": DOMINIO + "/#negocio", "name": NOMBRE, "url": DOMINIO + "/", "telephone": TEL,
            "description": "Servicio técnico Samsung en Panamá: neveras, lavadoras, secadoras y aires acondicionados Samsung en Ciudad de Panamá.",
            "areaServed": [{"@type": "City", "name": "Ciudad de Panamá"}, {"@type": "AdministrativeArea", "name": "Panamá"}] if not area else [{"@type": "Place", "name": area}],
            "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "07:00", "closes": "18:00"}],
            "priceRange": "$$", "knowsAbout": ["Reparación de neveras Samsung", "Reparación de lavadoras Samsung", "Reparación de secadoras Samsung", "Aire acondicionado Samsung"]}

def tarjetas_eq(depth):
    r = R(depth)
    return '<div class="grid g4">' + "".join(
        f'<a class="card eq" href="{r}electrodomesticos/{k}/index.html"><span class="ic">{ICONOS[v["icono"]]}</span><h3>{esc(v["nombre"])}</h3><p>{esc(v["intro"][:120].rsplit(" ",1)[0])}…</p><span class="mas">Ver servicio →</span></a>'
        for k, v in EQUIPOS.items()) + "</div>"

# ------------------------------------------------------------ páginas
def pagina_inicio():
    msg = "Hola, necesito servicio técnico para mi equipo Samsung en Panamá"
    zonas = "".join(f'<a href="zonas/{slug(z[0])}.html">{esc(z[0])}</a>' for z in ZONAS[:16])
    pasos = [("Escríbenos por WhatsApp", "Cuéntanos qué equipo es, el modelo y qué le pasa. Si puedes, manda una foto o un video."), ("Coordinamos la visita", "Te confirmamos disponibilidad en tu zona, normalmente en 24 a 48 horas."), ("Diagnóstico y reparación", "Revisamos el equipo en tu casa, te explicamos la falla y el costo, y reparamos si estás de acuerdo.")]
    cuerpo = f'''<section class="hero"><div class="w hg"><div><span class="ey">Servicio técnico Samsung Panamá</span><h1>Servicio técnico Samsung en Panamá</h1>
<p class="lead">Reparamos neveras, lavadoras, secadoras y aires acondicionados Samsung a domicilio en Ciudad de Panamá. Diagnóstico honesto, costo claro antes de reparar y garantía en cada reparación.</p>
<div class="acc"><a class="btn wa lg" href="{wa(msg)}" target="_blank" rel="noopener" data-wa="hero">{ICONOS["wa"]} Escribir por WhatsApp</a><a class="btn sec lg" href="diagnostico.html">Diagnóstico rápido</a></div>
<ul class="pts"><li>Visitas en 24 a 48 horas</li><li>Garantía en pieza y mano de obra</li><li>{HORARIO}</li></ul></div>
<div class="hero-tarjeta"><b>¿Qué equipo tienes?</b><div class="mini">{"".join(f'<a href="electrodomesticos/{k}/index.html"><span class="ic">{ICONOS[v["icono"]]}</span>{esc(v["corto"])}</a>' for k, v in EQUIPOS.items())}</div><small>Toca tu equipo para ver fallas comunes y cómo lo reparamos.</small></div></div></section>
<section class="conf"><div class="w"><div><b>Técnico especializado</b><small>Enfocado en equipos Samsung</small></div><div><b>Costo claro</b><small>Antes de reparar</small></div><div><b>Garantía</b><small>Pieza y mano de obra</small></div><div><b>Atención por WhatsApp</b><small>Respuesta en minutos</small></div></div></section>
<section class="sec fotos-s"><div class="w"><div class="cab"><span class="ey">En tu casa</span><h2>Técnicos revisando tus equipos Samsung</h2><p>Medimos, diagnosticamos y te explicamos la falla antes de reparar.</p></div><div class="grid g3 gf">{pic("tecnico-nevera", "Técnico reparando una nevera Samsung", 0, 1024, 572)}{pic("tecnico-lavadora-2", "Técnico revisando una lavadora Samsung", 0, 1024, 572)}{pic("tecnico-lavadora-1", "Técnico reparando una lavadora Samsung de carga frontal", 0, 1024, 572)}</div></div></section>
<section class="sec" id="equipos"><div class="w"><div class="cab"><span class="ey">Qué reparamos</span><h2>Reparación de electrodomésticos Samsung en Panamá</h2><p>Atendemos los equipos Samsung más usados en casas y apartamentos de la ciudad.</p></div>{tarjetas_eq(0)}</div></section>
<section class="sec alt" id="servicios"><div class="w"><div class="cab"><span class="ey">Servicios</span><h2>Servicio técnico a domicilio</h2></div><div class="grid g4">{"".join(f'<a class="card" href="servicios/{k}-samsung-panama.html"><h3>{esc(v[1])}</h3><p>{esc(v[2][:130].rsplit(" ",1)[0])}…</p><span class="mas">Ver más →</span></a>' for k, v in SERVICIOS.items())}</div></div></section>
<section class="sec"><div class="w"><div class="cab"><span class="ey">Así trabajamos</span><h2>Cómo agendar tu servicio técnico Samsung</h2></div><ol class="pasos">{"".join(f"<li><b>{esc(a)}</b><p>{esc(b)}</p></li>" for a, b in pasos)}</ol></div></section>
<section class="sec alt"><div class="w"><div class="cab"><span class="ey">Por qué elegirnos</span><h2>Servicio técnico Samsung con honestidad</h2></div><div class="grid g3">
<div class="card"><h3>Diagnóstico honesto</h3><p>Te explicamos la falla y la causa antes de reparar nada. Si no vale la pena reparar, te lo decimos.</p></div>
<div class="card"><h3>Garantía real</h3><p>Cada reparación incluye garantía sobre la pieza reemplazada y la mano de obra. El plazo se confirma antes de empezar.</p></div>
<div class="card"><h3>Costo claro</h3><p>Te confirmamos el costo de la visita y de la reparación antes de empezar el trabajo.</p></div></div>
<p class="aviso">Si tu equipo todavía está en garantía de fábrica, te lo decimos durante el diagnóstico para que decidas cómo proceder.</p></div></section>
<section class="sec"><div class="w"><div class="cab"><span class="ey">Cobertura</span><h2>Servicio técnico Samsung en tu zona de Panamá</h2><p>Llegamos a los principales barrios de la ciudad, San Miguelito y Panamá Oeste.</p></div><div class="chips">{zonas}</div><p><a href="zonas-de-cobertura.html">Ver todas las zonas de cobertura →</a></p></div></section>
<section class="sec alt"><div class="w"><div class="cab"><span class="ey">Diagnóstico rápido</span><h2>¿Qué le pasa a tu equipo Samsung?</h2><p>Mira los síntomas más comunes, la causa probable y qué tan urgente es.</p></div><p><a class="btn lg" href="diagnostico.html">Abrir el diagnóstico rápido</a></p></div></section>
<section class="sec"><div class="w"><div class="cab"><span class="ey">Lo que más buscan</span><h2>Servicio técnico Samsung en Panamá: encuentra lo que necesitas</h2><p>Reparación de neveras, lavadoras, secadoras y aires acondicionados Samsung, teléfono, precios, repuestos, filtros y zonas de cobertura.</p></div><div class="chips">{busquedas_chips(0)}</div>
<div class="grid g3 gf" style="margin-top:22px"><a class="card" href="cambio-filtro-nevera-samsung-panama.html">{pic("cambiar-filtro-nevera", "Pantalla de nevera Samsung con aviso de cambiar filtro", 0, 1024, 572)}<h3>Cambio de filtro de nevera</h3><p>Cuándo cambiarlo y qué hacer si aparece el aviso.</p></a>
<a class="card" href="fallas/neveras-samsung-{fslug(EQUIPOS['neveras']['fallas'][0])}.html">{pic("dispensador-nevera", "Persona usando el dispensador de una nevera Samsung", 0, 1024, 572)}<h3>La nevera Samsung no enfría</h3><p>Causas y qué revisar antes de llamar.</p></a>
<a class="card" href="codigos-de-error-lavadora-samsung-panama.html">{pic("tecnico-lavadora-1", "Técnico revisando una lavadora Samsung", 0, 1024, 572)}<h3>Códigos de error de lavadora</h3><p>UE, 5E, 4E, dE, LE: qué significan.</p></a></div>
<h3 style="margin-top:26px">Fallas y zonas más consultadas</h3><div class="chips"><a href="fallas/index.html">Todas las fallas Samsung</a>{"".join(f'<a href="{furl(k, e["fallas"][0])}">{esc(e["corto"])}: {esc(e["fallas"][0][0])}</a>' for k, e in EQUIPOS.items())}{"".join(f'<a href="{zurl("neveras", z[0])}">Neveras Samsung en {esc(z[0])}</a>' for z in ZONAS[:8])}</div></div></section>
<section class="sec alt"><div class="w"><div class="cab"><span class="ey">Dudas frecuentes</span><h2>Preguntas frecuentes sobre el servicio técnico Samsung en Panamá</h2></div>{faq_html(FAQ_GENERAL)}</div></section>
{cta(msg)}'''
    ld = [negocio_ld(), faq_ld(FAQ_GENERAL)]
    escribir("index.html", "Servicio Técnico Samsung en Panamá | Neveras, Lavadoras, Secadoras y Aires | +507 6933-7976",
             "Servicio técnico Samsung en Panamá: reparación de neveras, lavadoras, secadoras y aires acondicionados a domicilio. Diagnóstico honesto, garantía y visitas en 24-48 horas. WhatsApp +507 6933-7976.", cuerpo, ld, "1.0")

def paginas_equipo():
    for k, e in EQUIPOS.items():
        base = f"electrodomesticos/{k}/"
        subs = [("index", f"Reparación de {e['corto'].lower()} Samsung"), ("fallas-comunes", f"Fallas comunes de {e['corto'].lower()} Samsung"), ("mantenimiento", f"Mantenimiento de {e['corto'].lower()} Samsung"), ("preguntas-frecuentes", f"Preguntas frecuentes de {e['corto'].lower()} Samsung")]
        sub_links = "".join(f'<a href="{s}.html">{esc(t)}</a>' for s, t in subs if s != "index")
        msg = f"Hola, necesito servicio técnico para mi {e['sing']} Samsung en Panamá"
        blog = [b for b in BLOG if b[2] == k][:3]
        blog_html = "".join(f'<a class="card" href="../../blog/{b[0]}.html"><h3>{esc(b[1])}</h3><p>{esc(b[3])}</p><span class="mas">Leer →</span></a>' for b in blog)
        # índice
        fallas = "".join(f'<tr><td data-l="Síntoma"><b>{esc(f[0])}</b></td><td data-l="Causa probable">{esc(f[1])}</td><td data-l="Urgencia"><span class="u {slug(f[2])}">{esc(f[2])}</span></td></tr>' for f in e["fallas"])
        cuerpo = f'''{miga(2, (e["nombre"], None))}<section class="hero chico"><div class="w hg"><div><span class="ey">Servicio técnico Samsung</span><h1>{esc(e["titulo_h1"])}</h1><p class="lead">{esc(e["intro"])}</p>
<div class="acc"><a class="btn wa lg" href="{wa(msg)}" target="_blank" rel="noopener" data-wa="hero">{ICONOS["wa"]} Escribir por WhatsApp</a><a class="btn sec lg" href="../../diagnostico.html">Diagnóstico rápido</a></div></div>{f'<div class="hero-tarjeta foto">{pic(FOTO_EQ[k][0], FOTO_EQ[k][1], 2, 1024, 572, "fto", False)}</div>' if k in FOTO_EQ else f'<div class="hero-tarjeta"><span class="ic grande">{ICONOS[e["icono"]]}</span><b>{esc(e["nombre"])} Samsung</b><small>{HORARIO}</small></div>'}</div></section>
<section class="sec"><div class="w"><div class="cab"><span class="ey">Modelos</span><h2>Qué {e["corto"].lower()} Samsung reparamos</h2></div><ul class="lista">{"".join(f"<li>{esc(m)}</li>" for m in e["modelos"])}</ul></div></section>
<section class="sec alt"><div class="w"><div class="cab"><span class="ey">Fallas</span><h2>Fallas comunes de {e["corto"].lower()} Samsung y su causa probable</h2><p>Estas son las que más vemos en Panamá. Si tu equipo tiene otro síntoma, escríbenos.</p></div><div class="tabla-w"><table class="tabla"><thead><tr><th>Síntoma</th><th>Causa probable</th><th>Urgencia</th></tr></thead><tbody>{fallas}</tbody></table></div><p><a href="fallas-comunes.html">Ver las fallas con más detalle →</a></p></div></section>
<section class="sec"><div class="w"><div class="cab"><span class="ey">Más información</span><h2>Todo sobre {e["art"]} Samsung</h2></div><div class="chips">{sub_links}<a href="../../servicios/mantenimiento-preventivo-samsung-panama.html">Mantenimiento preventivo</a><a href="../../servicios/instalacion-samsung-panama.html">Instalación</a></div><h3>Fallas de {e["corto"].lower()} Samsung</h3><div class="chips">{"".join(f'<a href="../../{furl(k, f)}">{esc(f[0])}</a>' for f in e["fallas"])}</div><h3>{esc(e["corto"])} Samsung por zona</h3><div class="chips">{"".join(f'<a href="../../{zurl(k, z[0])}">{esc(z[0])}</a>' for z in ZONAS)}</div></div></section>
{f'<section class="sec alt"><div class="w"><div class="cab"><span class="ey">Blog</span><h2>Guías sobre {e["corto"].lower()} Samsung</h2></div><div class="grid g3">{blog_html}</div></div></section>' if blog else ""}
<section class="sec"><div class="w"><div class="cab"><span class="ey">Dudas frecuentes</span><h2>Preguntas frecuentes</h2></div>{faq_html(e["faq"])}</div></section>
{cta(msg, f"¿Tu {e['sing']} Samsung tiene una falla?")}'''
        escribir(base + "index.html", f"{e['titulo_h1']} | {TEL}", f"{e['intro'][:150]} Visitas en 24-48 horas y garantía. WhatsApp {TEL}.", cuerpo,
                 [negocio_ld(), faq_ld(e["faq"]), bc((e["nombre"], None))], "0.9")
        # fallas
        det = "".join(f'<article class="falla"><h3><a href="../../{furl(k, f)}">{esc(f[0])}</a></h3><p><b>Causa probable:</b> {esc(f[1])}</p><p><b>Qué puedes revisar:</b> {esc(f[3])}</p><p><span class="u {slug(f[2])}">{esc(f[2])}</span> <a class="btn sm wa" href="{wa(f"Hola, mi {e["sing"]} Samsung tiene este problema: {f[0]}")}" target="_blank" rel="noopener" data-wa="falla">{ICONOS["wa"]} Consultar esta falla</a></p></article>' for f in e["fallas"])
        cuerpo = f'''{miga(2, (e["nombre"], base + "index.html"), ("Fallas comunes", None))}<section class="sec"><div class="w txt"><h1>Fallas comunes de {esc(e["corto"].lower())} Samsung en Panamá</h1><p class="lead">Síntomas frecuentes, causa probable y qué puedes revisar antes de llamar al técnico.</p>{det}</div></section>{cta(msg)}'''
        escribir(base + "fallas-comunes.html", f"Fallas comunes de {e['corto'].lower()} Samsung en Panamá y cómo repararlas", f"Fallas más comunes de {e['corto'].lower()} Samsung en Panamá: síntomas, causa probable y qué revisar. Servicio técnico a domicilio. WhatsApp {TEL}.", cuerpo,
                 [bc((e["nombre"], base + "index.html"), ("Fallas comunes", None))], "0.8")
        # mantenimiento
        lis = "".join(f"<li>{esc(m)}</li>" for m in e["mant"])
        cuerpo = f'''{miga(2, (e["nombre"], base + "index.html"), ("Mantenimiento", None))}<section class="sec"><div class="w txt"><h1>Mantenimiento de {esc(e["corto"].lower())} Samsung en Panamá</h1><p class="lead">Con el calor, la humedad y las variaciones de voltaje de Panamá, un buen mantenimiento evita daños mayores.</p><ul class="lista">{lis}</ul>
<p>Si prefieres que lo haga un técnico, mira el <a href="../../servicios/mantenimiento-preventivo-samsung-panama.html">servicio de mantenimiento preventivo</a>.</p></div></section>{cta(msg, "¿Quieres agendar un mantenimiento?")}'''
        escribir(base + "mantenimiento.html", f"Mantenimiento de {e['corto'].lower()} Samsung en Panamá: consejos y servicio", f"Consejos de mantenimiento para {e['corto'].lower()} Samsung en Panamá y cuándo pedir un servicio técnico. WhatsApp {TEL}.", cuerpo,
                 [bc((e["nombre"], base + "index.html"), ("Mantenimiento", None))], "0.7")
        # faq
        cuerpo = f'''{miga(2, (e["nombre"], base + "index.html"), ("Preguntas frecuentes", None))}<section class="sec"><div class="w txt"><h1>Preguntas frecuentes sobre {esc(e["corto"].lower())} Samsung</h1>{faq_html(e["faq"])}</div></section>{cta(msg)}'''
        escribir(base + "preguntas-frecuentes.html", f"Preguntas frecuentes: {e['corto'].lower()} Samsung en Panamá", f"Respuestas a las dudas más comunes sobre reparación de {e['corto'].lower()} Samsung en Panamá. WhatsApp {TEL}.", cuerpo,
                 [faq_ld(e["faq"]), bc((e["nombre"], base + "index.html"), ("Preguntas frecuentes", None))], "0.6")

def paginas_servicio():
    for k, (titulo, corto, desc, puntos) in SERVICIOS.items():
        msg = f"Hola, quiero agendar: {corto.lower()} para mi equipo Samsung en Panamá"
        ruta = f"servicios/{k}-samsung-panama.html"
        faq = [(f"¿Qué equipos incluye el servicio de {corto.lower()}?", "Neveras, lavadoras, secadoras y aires acondicionados Samsung."), ("¿Dónde lo hacen?", "En Ciudad de Panamá, San Miguelito y Panamá Oeste. Escríbenos por WhatsApp para confirmar tu zona."), ("¿Cuánto cuesta?", "Te confirmamos el costo por WhatsApp antes de ir, según el equipo y el servicio.")]
        cuerpo = f'''{miga(1, (corto, None))}<section class="sec"><div class="w txt"><h1>{esc(titulo)}</h1><p class="lead">{esc(desc)}</p><h2>Qué incluye</h2><ul class="lista">{"".join(f"<li>{esc(p)}</li>" for p in puntos)}</ul>
<h2>Equipos que atendemos</h2>{tarjetas_eq(1)}<h2>Preguntas frecuentes</h2>{faq_html(faq)}</div></section>{cta(msg, f"Agenda: {corto.lower()}")}'''
        escribir(ruta, f"{titulo} | {TEL}", f"{desc[:150]} WhatsApp {TEL}.", cuerpo, [negocio_ld(), faq_ld(faq), bc((corto, None))], "0.8")

def paginas_zona():
    for i, (z, tipo, area) in enumerate(ZONAS):
        s = slug(z); ruta = f"zonas/{s}.html"
        t1, t2 = TIPO_TXT[tipo]
        vec = [ZONAS[(i + d) % len(ZONAS)] for d in (1, 2, 3, 4)]
        msg = f"Hola, necesito servicio técnico para mi equipo Samsung en {z}"
        faq = [(f"¿Atienden en {z}?", f"Sí, damos servicio técnico Samsung a domicilio en {z} ({area}). Escríbenos por WhatsApp y te confirmamos disponibilidad."),
               (f"¿Cuánto tardan en llegar a {z}?", "Coordinamos visitas en 24 a 48 horas en la mayoría de las zonas."),
               ("¿Qué equipos Samsung reparan?", "Neveras, lavadoras, secadoras y aires acondicionados.")]
        cuerpo = f'''{miga(1, ("Zonas", "zonas-de-cobertura.html"), (z, None))}<section class="hero chico"><div class="w hg"><div><span class="ey">{esc(area)}</span><h1>Servicio técnico Samsung en {esc(z)}</h1><p class="lead">Reparación a domicilio de neveras, lavadoras, secadoras y aires acondicionados Samsung en {esc(z)}. Diagnóstico honesto, costo claro y garantía.</p>
<div class="acc"><a class="btn wa lg" href="{wa(msg)}" target="_blank" rel="noopener" data-wa="hero">{ICONOS["wa"]} Escribir por WhatsApp</a></div></div><div class="hero-tarjeta"><b>{esc(z)}</b><small>{HORARIO}</small></div></div></section>
<section class="sec"><div class="w txt"><h2>Técnico Samsung a domicilio en {esc(z)}</h2><p>{esc(t1)}</p><p>{esc(t2)}</p>
<h2>Equipos Samsung que reparamos en {esc(z)}</h2>{tarjetas_eq(1)}<h2>Preguntas frecuentes en {esc(z)}</h2>{faq_html(faq)}
<h2>Servicio por equipo en {esc(z)}</h2><div class="chips">{"".join(f'<a href="{k2}-samsung-{s}.html">Reparación de {esc(e2["corto"].lower())} Samsung en {esc(z)}</a>' for k2, e2 in EQUIPOS.items())}</div><h2>Zonas cercanas</h2><div class="chips">{"".join(f'<a href="{slug(v[0])}.html">{esc(v[0])}</a>' for v in vec)}</div></div></section>{cta(msg, f"¿Equipo Samsung con falla en {z}?")}'''
        escribir(ruta, f"Servicio Técnico Samsung en {z} | Neveras, Lavadoras y Aires | {TEL}", f"Servicio técnico Samsung a domicilio en {z}, Panamá: neveras, lavadoras, secadoras y aires acondicionados. Garantía y visitas en 24-48 horas. WhatsApp {TEL}.", cuerpo,
                 [negocio_ld(area=z), faq_ld(faq), bc(("Zonas", "zonas-de-cobertura.html"), (z, None))], "0.6")
    por_area = {}
    for z, tipo, area in ZONAS: por_area.setdefault(area, []).append(z)
    bloques = "".join(f'<h2>{esc(a)}</h2><div class="chips">{"".join(f"<a href=\"zonas/{slug(z)}.html\">{esc(z)}</a>" for z in zs)}</div>' for a, zs in por_area.items())
    msg = "Hola, quiero saber si dan servicio técnico Samsung en mi zona de Panamá"
    cuerpo = f'''{miga(0, ("Zonas de cobertura", None))}<section class="sec"><div class="w txt"><h1>Zonas de cobertura del servicio técnico Samsung en Panamá</h1><p class="lead">Atendemos a domicilio en {len(ZONAS)} zonas de Ciudad de Panamá, San Miguelito y Panamá Oeste. Si tu zona no aparece, escríbenos: puede que también lleguemos.</p>{bloques}</div></section>{cta(msg)}'''
    escribir("zonas-de-cobertura.html", f"Zonas de cobertura: servicio técnico Samsung en Panamá | {TEL}", f"Zonas donde damos servicio técnico Samsung en Panamá: Ciudad de Panamá, San Miguelito, Arraiján y La Chorrera. WhatsApp {TEL}.", cuerpo, [bc(("Zonas de cobertura", None))], "0.8")

def paginas_blog():
    tarj = ""
    for sl, titulo, cat, resumen, secs in BLOG:
        msg = f"Hola, leí '{titulo}' y necesito servicio técnico Samsung"
        cuerpo_txt = "".join(f"<h2>{esc(h)}</h2>" + (t if t.startswith("<") or "<ul>" in t else f"<p>{esc(t)}</p>") if False else (f"<h2>{esc(h)}</h2><p>{t}</p>" if "<ul>" not in t else f"<h2>{esc(h)}</h2>{t}") for h, t in secs)
        rel = "".join(f'<a href="{sl2}.html">{esc(t2)}</a>' for sl2, t2, c2, *_ in BLOG if c2 == cat and sl2 != sl)[:600]
        cuerpo = f'''{miga(1, ("Blog", "blog/index.html"), (titulo, None))}<section class="sec"><div class="w txt"><span class="ey">{esc(EQUIPOS[cat]["corto"])} Samsung</span><h1>{esc(titulo)}</h1><p class="lead">{esc(resumen)}</p>{cuerpo_txt}
<p><a href="../electrodomesticos/{cat}/index.html">Ver el servicio técnico de {esc(EQUIPOS[cat]["corto"].lower())} Samsung →</a></p>{f'<h2>Te puede interesar</h2><div class="chips">{rel}</div>' if rel else ""}</div></section>{cta(msg)}'''
        ld = [{"@context": "https://schema.org", "@type": "Article", "headline": titulo, "description": resumen, "inLanguage": "es-PA", "author": {"@type": "Organization", "name": NOMBRE}, "publisher": {"@type": "Organization", "name": NOMBRE}, "mainEntityOfPage": f"{DOMINIO}/blog/{sl}.html", "datePublished": "2026-10-20", "dateModified": "2026-10-20"}, bc(("Blog", "blog/index.html"), (titulo, None))]
        escribir(f"blog/{sl}.html", f"{titulo} | {NOMBRE}", resumen, cuerpo, ld, "0.6")
        tarj += f'<a class="card" href="{sl}.html"><span class="ey">{esc(EQUIPOS[cat]["corto"])}</span><h3>{esc(titulo)}</h3><p>{esc(resumen)}</p><span class="mas">Leer →</span></a>'
    cuerpo = f'''{miga(1, ("Blog", None))}<section class="sec"><div class="w"><div class="cab"><h1>Blog: guías de electrodomésticos Samsung en Panamá</h1><p>Consejos para entender las fallas de tu nevera, lavadora, secadora o aire acondicionado Samsung.</p></div><div class="grid g3">{tarj}</div></div></section>'''
    escribir("blog/index.html", f"Blog de electrodomésticos Samsung en Panamá | {NOMBRE}", "Guías sobre fallas de neveras, lavadoras, secadoras y aires acondicionados Samsung en Panamá: causas y qué hacer.", cuerpo, [bc(("Blog", None))], "0.7")

def pagina_diagnostico():
    items = []
    for k, e in EQUIPOS.items():
        for f in e["fallas"]:
            items.append((k, e["corto"], e["sing"], f))
    tabs = '<button class="tab on" data-f="todos">Todos</button>' + "".join(f'<button class="tab" data-f="{k}">{esc(v["corto"])}</button>' for k, v in EQUIPOS.items())
    cards = "".join(f'<article class="falla dg" data-eq="{k}"><span class="ey">{esc(c)} Samsung</span><h3>{esc(f[0])}</h3><p><b>Causa probable:</b> {esc(f[1])}</p><p><b>Qué revisar:</b> {esc(f[3])}</p><p><span class="u {slug(f[2])}">{esc(f[2])}</span> <a class="btn sm wa" href="{wa(f"Hola, mi {s} Samsung tiene este problema: {f[0]}")}" target="_blank" rel="noopener" data-wa="diagnostico">{ICONOS["wa"]} Consultar</a></p></article>' for k, c, s, f in items)
    ld = {"@context": "https://schema.org", "@type": "ItemList", "name": "Diagnóstico rápido de electrodomésticos Samsung", "itemListElement": [{"@type": "ListItem", "position": i, "name": f"{x[2].capitalize()} Samsung: {x[3][0]}"} for i, x in enumerate(items, 1)]}
    cuerpo = f'''{miga(0, ("Diagnóstico rápido", None))}<section class="sec"><div class="w"><div class="cab"><h1>Diagnóstico rápido: ¿qué le pasa a tu equipo Samsung?</h1><p>{len(items)} fallas comunes de neveras, lavadoras, secadoras y aires acondicionados Samsung, con la causa probable y qué tan urgente es.</p></div><div class="tabs" role="tablist">{tabs}</div><div class="grid g2" id="dg">{cards}</div></div></section>{cta("Hola, necesito diagnóstico para mi equipo Samsung en Panamá")}'''
    escribir("diagnostico.html", f"Diagnóstico rápido de neveras, lavadoras, secadoras y aires Samsung | {NOMBRE}", f"{len(items)} fallas comunes de electrodomésticos Samsung en Panamá con causa probable y urgencia. Consulta tu caso por WhatsApp.", cuerpo, [ld, bc(("Diagnóstico rápido", None))], "0.8")

def paginas_info():
    msg = "Hola, necesito servicio técnico para mi equipo Samsung en Panamá"
    c = f'''{miga(0, ("Garantía", None))}<section class="sec"><div class="w txt"><h1>Garantía de servicio técnico Samsung en Panamá</h1><p class="lead">Cada reparación incluye garantía sobre la pieza reemplazada y sobre la mano de obra. El plazo exacto se confirma antes de empezar el trabajo, no después.</p>
<p>Esta es la garantía de nuestro servicio técnico y es distinta de la garantía de fábrica. Si tu equipo todavía está en garantía de fábrica, te lo decimos durante el diagnóstico para que la hagas valer donde corresponda.</p>
<h2>Qué cubre</h2><ul class="lista"><li><b>Pieza reemplazada:</b> si vuelve a fallar por defecto de la pieza dentro del plazo acordado, la revisamos sin costo adicional de mano de obra.</li><li><b>Mano de obra:</b> si el mismo síntoma reaparece por un error de instalación o ajuste, lo corregimos sin cargo.</li></ul>
<h2>Qué no cubre</h2><p>Daños nuevos por mal uso, variaciones de voltaje posteriores al servicio o intervención de terceros después de nuestra visita.</p>{faq_html([("¿Cuánto dura la garantía?", "Depende de la pieza y del tipo de reparación; te lo confirmamos por escrito al momento del servicio, antes de que pagues."), ("¿Qué hago si la falla vuelve?", "Escríbenos por WhatsApp con tu nombre y la fecha del servicio anterior; si está dentro del plazo, coordinamos la revisión.")])}</div></section>{cta(msg)}'''
    escribir("garantia.html", f"Garantía de servicio técnico Samsung en Panamá | {NOMBRE}", "Garantía sobre la pieza reemplazada y la mano de obra en cada reparación de electrodomésticos Samsung en Panamá.", c, [bc(("Garantía", None))], "0.5")
    c = f'''{miga(0, ("Nosotros", None))}<section class="sec"><div class="w txt"><h1>Nosotros: especialistas en electrodomésticos Samsung en Panamá</h1><p class="lead">Somos un servicio técnico enfocado en electrodomésticos Samsung: neveras, lavadoras, secadoras y aires acondicionados.</p>
<p>Esa especialización nos permite conocer a fondo los modelos que circulan en Panamá, sus fallas más comunes y los repuestos que realmente necesitan. Trabajamos con coordinación directa por WhatsApp, sin intermediarios.</p>
<h2>Cómo trabajamos</h2><ul class="lista"><li><b>Diagnóstico honesto:</b> explicamos la falla antes de reparar. Si no vale la pena, te lo decimos.</li><li><b>Garantía:</b> en la pieza y en la mano de obra.</li><li><b>Tiempos claros:</b> visitas en 24 a 48 horas en la mayoría de zonas.</li><li><b>Costo claro:</b> te lo confirmamos antes de empezar.</li></ul>
</div></section>{cta(msg)}'''
    escribir("nosotros.html", f"Nosotros | {NOMBRE}", "Servicio técnico especializado en electrodomésticos Samsung en Ciudad de Panamá.", c, [negocio_ld(), bc(("Nosotros", None))], "0.5")
    c = f'''{miga(0, ("Preguntas frecuentes", None))}<section class="sec"><div class="w txt"><h1>Preguntas frecuentes sobre el servicio técnico Samsung en Panamá</h1>{faq_html(FAQ_GENERAL)}</div></section>{cta(msg)}'''
    escribir("preguntas-frecuentes.html", f"Preguntas frecuentes | Servicio técnico Samsung en Panamá", "Respuestas sobre cobertura, costos, garantía y tiempos del servicio técnico Samsung en Panamá.", c, [faq_ld(FAQ_GENERAL), bc(("Preguntas frecuentes", None))], "0.6")
    c = f'''{miga(0, ("Privacidad", None))}<section class="sec"><div class="w txt"><h1>Política de privacidad</h1><p>Cuando nos escribes por WhatsApp o nos llamas usamos tu nombre, tu número y los datos que nos des (dirección, equipo, modelo y falla) solo para atender tu solicitud y coordinar la visita.</p><p>No vendemos tus datos. Puedes pedirnos que los corrijamos o los eliminemos escribiéndonos por WhatsApp al {TEL}.</p><p>Este sitio puede usar herramientas de medición (como Google Analytics o Tag Manager) para saber cuántas personas lo visitan y cuántas nos escriben por WhatsApp.</p></div></section>'''
    escribir("privacidad.html", f"Política de privacidad | {NOMBRE}", "Cómo usamos tus datos cuando nos contactas para un servicio técnico.", c, None, "0.2")
    c = f'''{miga(0, ("Aviso legal", None))}<section class="sec"><div class="w txt"><h1>Aviso legal</h1><p>{NOMBRE} presta servicio técnico a domicilio para electrodomésticos Samsung en Panamá.</p><p>Samsung es una marca registrada de Samsung Electronics Co., Ltd. Este sitio no es operado por Samsung.</p><p>La información de este sitio es orientativa. El diagnóstico definitivo y el costo se confirman en la visita.</p></div></section>'''
    escribir("aviso-legal.html", f"Aviso legal | {NOMBRE}", "Aviso legal del servicio técnico de electrodomésticos Samsung en Panamá.", c, None, "0.2")

CSS = r'''
:root{--pri:#1428a0;--pri2:#0a1460;--ink:#0b1440;--mut:#545c78;--bg:#fff;--panel:#f2f4fb;--line:#dde2f1;--soft:#e6eaf8;--wa:#1fa855;--r:18px}
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
.hero{background:radial-gradient(1000px 420px at 85% -10%,#2f4fd0 0%,transparent 60%),linear-gradient(160deg,var(--pri2),var(--pri));color:#fff;padding-block:56px}.hero.chico{padding-block:40px}.hero h1{color:#fff}.hero .lead{font-size:18px;opacity:.95;max-width:60ch}.hg{display:grid;grid-template-columns:1.3fr 1fr;gap:32px;align-items:center}.ey{display:inline-block;font-size:12px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:#a9b8ff;margin-bottom:10px}.sec:not(.alt) .ey,.sec.alt .ey,.card .ey{color:var(--pri)}.acc{display:flex;gap:12px;flex-wrap:wrap;margin:22px 0}.pts{display:flex;gap:18px;flex-wrap:wrap;list-style:none;padding:0;margin:0;font-weight:600;font-size:14px}.pts li::before{content:"✓ ";color:#a9f5c9}
.hero-tarjeta{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.25);border-radius:var(--r);padding:20px;display:flex;flex-direction:column;gap:12px}.mini{display:grid;grid-template-columns:1fr 1fr;gap:10px}.mini a{display:flex;align-items:center;gap:10px;background:#fff;color:var(--ink);border-radius:14px;padding:12px;text-decoration:none;font-weight:700;font-size:14px}.mini .ic svg,.ic.grande svg{width:34px;height:34px}.mini .ic{color:var(--pri)}.ic.grande{color:#fff}.ic.grande svg{width:56px;height:56px}
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
.u{display:inline-block;padding:3px 10px;border-radius:999px;font-size:12px;font-weight:800}.u.urgente{background:#fde2e2;color:#a31212}.u.revisar-pronto{background:#fff0d0;color:#8a5600}.u.vigilar{background:#dff5e8;color:#0d6b3a}
.falla{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:18px;margin:14px 0}.falla p{margin:6px 0}.tabs{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:18px}.tab{padding:8px 16px;border:1px solid var(--line);border-radius:999px;background:#fff;font:600 14px inherit;cursor:pointer}.tab.on{background:var(--pri);color:#fff;border-color:var(--pri)}
.pie{background:var(--pri2);color:#dfe5ff;padding-top:44px}.pie a{color:#dfe5ff;text-decoration:none}.cols{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:28px}.cols b{display:block;color:#fff;margin-bottom:8px}.cols a{display:block;padding:3px 0;font-size:14px}.pl{font-size:18px}.hor{font-size:13px;opacity:.8}.legal{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;border-top:1px solid rgba(255,255,255,.15);margin-top:28px;padding-block:18px;font-size:12px;opacity:.85}@media(max-width:860px){.cols{grid-template-columns:1fr 1fr}}@media(max-width:560px){.cols{grid-template-columns:1fr}}
.wa-flot{position:fixed;right:16px;bottom:calc(16px + env(safe-area-inset-bottom,0px));z-index:60;display:flex;align-items:center;gap:8px;background:#25d366;color:#fff!important;border-radius:999px;padding:12px 18px 12px 14px;font-weight:800;text-decoration:none;box-shadow:0 8px 24px rgba(0,0,0,.25)}.wa-flot svg{width:28px;height:28px}@media(max-width:520px){.wa-flot span{display:none}.wa-flot{padding:14px}}

.pie .logo{color:#fff;display:flex!important;margin:0 0 12px}.pie .btn{display:inline-flex!important;width:auto}.pie .lg-t{font-size:14px}.pie .lg-t b{color:#fff}.pie .lg-t small{color:#b9c4f5}.pie .lg-i{background:#fff;color:var(--pri)}.busq{padding-top:22px}.busq b{display:block;color:#fff;margin-bottom:6px}.busq .chips a{background:transparent;border-color:rgba(255,255,255,.3);color:#dfe5ff;font-size:13px;padding:6px 12px}.fto img{width:100%;height:auto;display:block;border-radius:var(--r)}.hero-tarjeta.foto{padding:0;overflow:hidden;background:none;border:0}.gf .fto img{aspect-ratio:16/10;object-fit:cover}
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
    (OUT / "images" / "logo" / "favicon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#1428a0"/><g transform="translate(14 14) scale(1.5)" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.2L3 17.8V21h3.2l6.3-6.3a4 4 0 0 0 5.2-5.4l-2.5 2.5-2.4-.6-.6-2.4z"/></g></svg>', encoding="utf-8")
    # imagen para compartir
    from PIL import Image, ImageDraw, ImageFont
    im = Image.new("RGB", (1200, 630), (20, 40, 160)); d = ImageDraw.Draw(im)
    for y in range(630):
        d.line([(0, y), (1200, y)], fill=(int(10 + 10 * y / 630), int(20 + 20 * y / 630), int(96 + 64 * y / 630)))
    fb = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; fr = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    d.text((70, 150), "Servicio técnico", font=ImageFont.truetype(fb, 64), fill="white")
    d.text((70, 235), "Samsung en Panamá", font=ImageFont.truetype(fb, 84), fill="white")
    d.text((70, 360), "Neveras · Lavadoras · Secadoras · Aires acondicionados", font=ImageFont.truetype(fr, 34), fill=(200, 214, 255))
    d.text((70, 480), f"WhatsApp {TEL}  ·  {HORARIO}", font=ImageFont.truetype(fb, 36), fill="white")
    (OUT / "images").mkdir(exist_ok=True); im.save(OUT / "images" / "og.jpg", quality=88)

def indices():
    urls = "".join(f"<url><loc>{DOMINIO}/{r}</loc><lastmod>2026-10-20</lastmod><priority>{p[0]}</priority></url>\n" for r, p in sorted(PAGINAS.items(), key=lambda x: -float(x[1][0])))
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nUser-agent: GPTBot\nAllow: /\nUser-agent: ClaudeBot\nAllow: /\nUser-agent: PerplexityBot\nAllow: /\nUser-agent: Google-Extended\nAllow: /\n\nSitemap: {DOMINIO}/sitemap.xml\n", encoding="utf-8")
    txt = f"# {NOMBRE}\n\n> Servicio técnico Samsung en Panamá: neveras, lavadoras, secadoras y aires acondicionados Samsung a domicilio en Ciudad de Panamá. WhatsApp {TEL}. {HORARIO}.\n\n## Servicios\n"
    for k, e in EQUIPOS.items(): txt += f"- [{e['titulo_h1']}]({DOMINIO}/electrodomesticos/{k}/index.html)\n"
    txt += "\n## Páginas clave\n" + "".join(f"- [{h['h1']}]({DOMINIO}/{h['f']})\n" for h in HUBS)
    txt += "\n## Zonas\n" + "".join(f"- [Servicio técnico Samsung en {z[0]}]({DOMINIO}/zonas/{slug(z[0])}.html)\n" for z in ZONAS)
    txt += "\n## Guías\n" + "".join(f"- [{b[1]}]({DOMINIO}/blog/{b[0]}.html)\n" for b in BLOG)
    (OUT / "llms.txt").write_text(txt, encoding="utf-8")

# ------------------------------------------------------------ cobertura de búsquedas
def fslug(f): return slug(f[0])[:48].strip("-")
def furl(k, f): return f"fallas/{k}-samsung-{fslug(f)}.html"
def zurl(k, z): return f"zonas/{k}-samsung-{slug(z)}.html"
FOTO_FALLA = {"neveras": ("dispensador-nevera", "Persona usando el dispensador de agua de una nevera Samsung French Door"), "lavadoras": ("tecnico-lavadora-1", "Técnico revisando una lavadora Samsung en Panamá"),
              "secadoras": ("tecnico-lavadora-2", "Técnico revisando una secadora y lavadora Samsung"), "aires-acondicionados": ("tecnico-banner", "Técnico de servicio Samsung en Panamá")}
FOTO_ZEQ = {"neveras": ("tecnico-nevera", FOTO_EQ["neveras"][1]), "lavadoras": ("tecnico-lavadora-2", FOTO_EQ["lavadoras"][1]), "secadoras": ("tecnico-lavadora-1", "Técnico revisando una secadora Samsung"), "aires-acondicionados": ("tecnico-banner", "Técnico de servicio Samsung en Panamá")}
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
    for k, e, f in todas:
        s, causa, urg, rev = f
        ruta = furl(k, f)
        msg = f"Hola, mi {e['sing']} Samsung tiene este problema: {s}"
        titulo = f"{s} en {e['sing']} Samsung: causas y reparación en Panamá"
        foto = FOTO_FALLA[k]
        otras = "".join(f'<a href="{k}-samsung-{fslug(g)}.html">{esc(g[0])}</a>' for g in e["fallas"] if g is not f)
        zs = "".join(f'<a href="../{zurl(k, z[0])}">{esc(e["corto"])} Samsung en {esc(z[0])}</a>' for z in ZONAS[:12])
        faq = [(f"¿Cuánto cuesta reparar: {s.lower()}?", "Depende de la causa y de la pieza. Escríbenos por WhatsApp con el modelo y el síntoma; te confirmamos el costo de la visita antes de ir y el de la reparación antes de empezar."),
               (f"¿Cuánto tarda la reparación?", "Muchas fallas se resuelven en la misma visita. Si hace falta una pieza, te avisamos el plazo antes de empezar. Coordinamos visitas en 24 a 48 horas."),
               (f"¿Atienden en mi zona de Panamá?", "Damos servicio a domicilio en Ciudad de Panamá, San Miguelito y Panamá Oeste. Escríbenos con tu barrio y te confirmamos.")]
        cuerpo = f'''{miga(1, ("Fallas", "fallas/index.html"), (f"{e['corto']}: {s}", None))}<section class="hero chico"><div class="w hg"><div><span class="ey">{esc(e["corto"])} Samsung · <span class="u {slug(urg)}">{esc(urg)}</span></span><h1>{esc(s)} en {esc(e["sing"])} Samsung</h1><p class="lead">Qué significa, cuál es la causa más probable y cuándo conviene llamar al técnico. Servicio técnico Samsung a domicilio en Panamá.</p>
<div class="acc"><a class="btn wa lg" href="{wa(msg)}" target="_blank" rel="noopener" data-wa="hero">{ICONOS["wa"]} Consultar esta falla</a></div></div><div class="hero-tarjeta foto">{pic(foto[0], foto[1], 1, 1024, 572, "fto", False)}</div></div></section>
<section class="sec"><div class="w txt"><h2>¿Por qué mi {esc(e["sing"])} Samsung presenta este problema?</h2><p><b>Causa probable:</b> {esc(causa)}</p><p>En Panamá el calor, la humedad y las variaciones de voltaje aceleran el desgaste de componentes de {esc(e["art"])}, por eso esta falla es frecuente en equipos con algunos años de uso.</p>
<h2>Qué puedes revisar antes de llamar</h2><p>{esc(rev)}</p><p>Revisa también que el equipo esté bien conectado, nivelado y con el tomacorriente en buen estado. Si no estás seguro de algo, no desarmes el equipo: puedes empeorar la falla o hacerte daño.</p>
<h2>¿Es urgente?</h2><p><span class="u {slug(urg)}">{esc(urg)}</span> {esc(PASOS[urg])}</p>
<h2>Qué hacemos en la visita</h2><ul class="lista"><li>Revisamos el equipo en tu casa u oficina y confirmamos la causa de la falla.</li><li>Te explicamos el problema, las opciones y el costo antes de empezar.</li><li>Reparamos o reemplazamos la pieza necesaria y probamos el equipo.</li><li>La reparación incluye garantía sobre la pieza y la mano de obra.</li></ul>
<h2>Otras fallas de {esc(e["corto"].lower())} Samsung</h2><div class="chips">{otras}</div>
<h2>Preguntas frecuentes</h2>{faq_html(faq)}<h2>Servicio en tu zona</h2><div class="chips">{zs}</div></div></section>{cta(msg, f"¿Tu {e['sing']} Samsung tiene esta falla?")}'''
        escribir(ruta, f"{titulo} | {TEL}", f"{s} en {e['sing']} Samsung: causa probable, qué revisar y cuándo llamar al técnico. Servicio técnico Samsung a domicilio en Panamá. WhatsApp {TEL}.", cuerpo,
                 [negocio_ld(), faq_ld(faq), bc(("Fallas", "fallas/index.html"), (f"{e['corto']}: {s}", None))], "0.7")
    bloques = ""
    for k, e in EQUIPOS.items():
        bloques += f'<h2>Fallas de {esc(e["corto"].lower())} Samsung</h2><div class="chips">' + "".join(f'<a href="{k}-samsung-{fslug(f)}.html">{esc(f[0])}</a>' for f in e["fallas"]) + "</div>"
    msg = "Hola, mi equipo Samsung tiene una falla y necesito un técnico en Panamá"
    cuerpo = f'''{miga(1, ("Fallas", None))}<section class="sec"><div class="w txt"><h1>Fallas de electrodomésticos Samsung en Panamá: causas y soluciones</h1><p class="lead">{len(todas)} síntomas frecuentes de neveras, lavadoras, secadoras y aires acondicionados Samsung, con la causa probable y qué revisar.</p>{bloques}</div></section>{cta(msg)}'''
    escribir("fallas/index.html", f"Fallas de neveras, lavadoras, secadoras y aires Samsung en Panamá | {TEL}", f"{len(todas)} fallas comunes de electrodomésticos Samsung en Panamá con causa probable y solución. Servicio técnico a domicilio. WhatsApp {TEL}.", cuerpo, [bc(("Fallas", None))], "0.8")

def paginas_zona_equipo():
    n = 0
    for i, (z, tipo, area) in enumerate(ZONAS):
        t1, t2 = TIPO_TXT[tipo]
        for j, (k, e) in enumerate(EQUIPOS.items()):
            msg = f"Hola, necesito servicio técnico para mi {e['sing']} Samsung en {z}"
            foto = FOTO_ZEQ[k]
            fl = "".join(f'<li><a href="../{furl(k, f)}"><b>{esc(f[0])}</b></a>: {esc(f[1])}</li>' for f in e["fallas"][:5])
            mant = e["mant"][(i + j) % len(e["mant"])]
            otros = "".join(f'<a href="../{zurl(k2, z)}">{esc(e2["corto"])} Samsung en {esc(z)}</a>' for k2, e2 in EQUIPOS.items() if k2 != k)
            vec = "".join(f'<a href="{k}-samsung-{slug(v[0])}.html">{esc(e["corto"])} Samsung en {esc(v[0])}</a>' for v in [ZONAS[(i + d) % len(ZONAS)] for d in (1, 2, 3, 4, 5)])
            faq = [(f"¿Reparan {e['corto'].lower()} Samsung en {z}?", f"Sí. Damos servicio técnico a domicilio de {e['corto'].lower()} Samsung en {z} ({area}). Escríbenos por WhatsApp con el modelo y la falla y te confirmamos la visita."),
                   (f"¿Cuánto tardan en llegar a {z}?", "Coordinamos visitas en 24 a 48 horas en la mayoría de las zonas, según disponibilidad."),
                   (f"¿Cuánto cuesta el servicio técnico de {e['art']} Samsung en {z}?", "Te confirmamos el costo de la visita antes de ir y el de la reparación antes de empezar, según la falla y el modelo.")]
            cuerpo = f'''{miga(1, ("Zonas", "zonas-de-cobertura.html"), (z, f"zonas/{slug(z)}.html"), (e["corto"], None))}<section class="hero chico"><div class="w hg"><div><span class="ey">{esc(area)}</span><h1>Reparación de {esc(e["corto"].lower())} Samsung en {esc(z)}</h1><p class="lead">Servicio técnico Samsung a domicilio en {esc(z)} para {esc(e["corto"].lower())}: diagnóstico en el sitio, costo claro antes de reparar y garantía en la pieza y la mano de obra.</p>
<div class="acc"><a class="btn wa lg" href="{wa(msg)}" target="_blank" rel="noopener" data-wa="hero">{ICONOS["wa"]} Escribir por WhatsApp</a></div></div><div class="hero-tarjeta foto">{pic(foto[0], foto[1], 1, 1024, 572, "fto", False)}</div></div></section>
<section class="sec"><div class="w txt"><h2>Técnico de {esc(e["corto"].lower())} Samsung en {esc(z)}</h2><p>{esc(t1)}</p><p>{esc(t2)}</p>
<h2>Fallas de {esc(e["corto"].lower())} Samsung que atendemos en {esc(z)}</h2><ul class="lista">{fl}</ul>
<h2>Consejo de mantenimiento</h2><p>{esc(mant)}</p>
<h2>Preguntas frecuentes en {esc(z)}</h2>{faq_html(faq)}
<h2>Otros equipos Samsung en {esc(z)}</h2><div class="chips">{otros}</div><h2>{esc(e["corto"])} Samsung en zonas cercanas</h2><div class="chips">{vec}</div></div></section>{cta(msg, f"¿Tu {e['sing']} Samsung falla en {z}?")}'''
            escribir(zurl(k, z), f"Reparación de {e['corto'].lower()} Samsung en {z} | Servicio técnico | {TEL}", f"Servicio técnico de {e['corto'].lower()} Samsung a domicilio en {z}, Panamá. Diagnóstico claro, garantía y visitas en 24-48 horas. WhatsApp {TEL}.", cuerpo,
                     [negocio_ld(area=z), faq_ld(faq), bc(("Zonas", "zonas-de-cobertura.html"), (z, f"zonas/{slug(z)}.html"), (e["corto"], None))], "0.5")
            n += 1

HUBS = [
 dict(f="servicio-tecnico-samsung-panama.html", chip="Servicio técnico Samsung Panamá", t="Servicio Técnico Samsung Panamá | Neveras, Lavadoras, Secadoras y Aires", h1="Servicio técnico Samsung en Panamá", foto=("tecnico-banner", "Técnico de servicio Samsung en Panamá"),
      lead="Reparación a domicilio de neveras, lavadoras, secadoras y aires acondicionados Samsung en Ciudad de Panamá, San Miguelito y Panamá Oeste.",
      secs=[("Qué es el servicio técnico Samsung que ofrecemos", "Atendemos en tu casa u oficina los electrodomésticos Samsung que presentan fallas: neveras que no enfrían, lavadoras que no centrifugan o no desaguan, secadoras que no secan y aires acondicionados que no enfrían o gotean. Revisamos el equipo, te explicamos la causa y confirmamos el costo antes de reparar."),
            ("Cómo funciona", "1) Escríbenos por WhatsApp con el equipo, el modelo y la falla. 2) Coordinamos la visita, normalmente en 24 a 48 horas. 3) Diagnosticamos en el sitio y te damos el costo. 4) Reparamos y probamos el equipo, con garantía sobre la pieza y la mano de obra."),
            ("Por qué elegir un técnico especializado en Samsung", "Conocer las fallas típicas de cada línea (inverter, carga frontal, French Door, dispensador, tarjetas de control) acorta el diagnóstico y evita cambiar piezas por prueba y error.")],
      faq=[("¿Qué incluye el servicio técnico Samsung a domicilio?", "Visita, diagnóstico en el sitio, explicación de la falla, cotización y reparación del equipo, con garantía."), ("¿En qué zonas de Panamá atienden?", "En Ciudad de Panamá, San Miguelito, Arraiján y La Chorrera, entre otras. Mira la lista de zonas de cobertura.")]),
 dict(f="telefono-servicio-tecnico-samsung-panama.html", chip="Teléfono servicio técnico Samsung Panamá", t="Teléfono y WhatsApp del Servicio Técnico Samsung en Panamá", h1="Teléfono del servicio técnico Samsung en Panamá", foto=None,
      lead=f"Llama o escribe por WhatsApp al {TEL}. Atendemos de lunes a sábado de 7:00am a 6:00pm.",
      secs=[("Contacto directo", f"WhatsApp y teléfono: {TEL}. Es la forma más rápida de pedir una visita: envíanos una foto del equipo, la etiqueta con el modelo (suele estar en el costado o en la parte trasera) y una descripción de la falla."),
            ("Qué información enviar", "Tipo de equipo (nevera, lavadora, secadora o aire acondicionado), modelo, tiempo de uso, qué síntoma presenta, si muestra códigos de error y tu barrio o edificio. Con eso te confirmamos disponibilidad y costo de la visita."),
            ("Horario", "Lunes a sábado de 7:00am a 6:00pm. Los mensajes enviados fuera de horario se responden el siguiente día hábil.")],
      faq=[("¿Cuál es el número de servicio técnico Samsung en Panamá?", f"Nuestro WhatsApp y teléfono es {TEL}."), ("¿Atienden por WhatsApp?", "Sí, es el canal principal: ahí coordinamos la visita y confirmamos el costo.")]),
 dict(f="tecnico-samsung-a-domicilio-panama.html", chip="Técnico Samsung a domicilio", t="Técnico Samsung a Domicilio en Panamá | Neveras, Lavadoras y Aires", h1="Técnico Samsung a domicilio en Panamá", foto=("tecnico-nevera", FOTO_EQ["neveras"][1]),
      lead="Vamos a tu casa, apartamento u oficina para revisar y reparar tu electrodoméstico Samsung sin que tengas que moverlo.",
      secs=[("Ventajas de la reparación a domicilio", "No tienes que cargar ni transportar una nevera o una lavadora. El técnico revisa el equipo donde está instalado, con su conexión eléctrica, su desagüe y su ventilación reales, que muchas veces son parte del problema."),
            ("Apartamentos y torres", "Coordinamos con la administración el horario, el ascensor de servicio y el ingreso de herramientas para que la visita sea rápida y sin inconvenientes."),
            ("Qué llevamos a la visita", "Herramientas de diagnóstico, multímetro y las piezas más frecuentes según el equipo. Si hace falta una pieza que no llevamos, te avisamos el plazo antes de empezar.")],
      faq=[("¿Cuánto tarda en llegar el técnico?", "Coordinamos visitas en 24 a 48 horas en la mayoría de las zonas."), ("¿Hacen la reparación en el momento?", "Muchas fallas se resuelven en la misma visita; si hay que pedir una pieza te avisamos antes.")]),
 dict(f="reparacion-electrodomesticos-samsung-panama.html", chip="Reparación de electrodomésticos Samsung", t="Reparación de Electrodomésticos Samsung en Panamá | Neveras, Lavadoras, Secadoras, Aires", h1="Reparación de electrodomésticos Samsung en Panamá", foto=("tecnico-lavadora-1", FOTO_FALLA["lavadoras"][1]),
      lead="Neveras, lavadoras, secadoras y aires acondicionados Samsung: reparación, mantenimiento e instalación con diagnóstico claro y garantía.",
      secs=[("Equipos que reparamos", "Neveras (French Door, Side by Side, congelador superior e inferior, con dispensador), lavadoras de carga superior y frontal, secadoras y aires acondicionados split e inverter."),
            ("Tipos de servicio", "Reparación de fallas, diagnóstico, mantenimiento preventivo e instalación. Cada servicio incluye explicación de la falla y costo confirmado antes de empezar."),
            ("Fallas más comunes", "La nevera que no enfría, el congelador con escarcha, la lavadora que no desagua o no centrifuga, la secadora que no seca y el aire que no enfría o gotea son las consultas más frecuentes en Panamá.")],
      faq=[("¿Reparan todas las líneas de Samsung?", "Atendemos neveras, lavadoras, secadoras y aires acondicionados. Para otros equipos, escríbenos y te decimos si podemos ayudarte."), ("¿Vale la pena reparar un equipo viejo?", "Si la falla es de una pieza accesible, casi siempre sí. Si no vale la pena, te lo decimos con honestidad.")]),
 dict(f="servicio-tecnico-samsung-cerca-de-mi-panama.html", chip="Servicio técnico Samsung cerca de mí", t="Servicio Técnico Samsung Cerca de Mí en Panamá | Visita a Domicilio", h1="Servicio técnico Samsung cerca de mí en Panamá", foto=None,
      lead="Si buscas un técnico Samsung cerca de tu casa en Panamá, atendemos a domicilio en más de 30 barrios y corregimientos.",
      secs=[("Cobertura por zonas", "Llegamos a San Francisco, Bella Vista, Obarrio, Marbella, Costa del Este, Punta Pacífica, Paitilla, Betania, San Miguelito, Albrook, Arraiján, La Chorrera y más. Elige tu zona abajo."),
            ("No tienes que ir a ningún lado", "Como el servicio es a domicilio, no necesitas buscar un taller cercano ni transportar tu equipo: nosotros vamos a donde está.")],
      faq=[("¿Mi zona tiene cobertura?", "Mira la lista de zonas o escríbenos con tu barrio. Si no aparece, es posible que igualmente lleguemos.")], zonas=True),
 dict(f="repuestos-samsung-panama.html", chip="Repuestos Samsung Panamá", t="Repuestos para Neveras, Lavadoras, Secadoras y Aires Samsung en Panamá", h1="Repuestos Samsung en Panamá", foto=("cambiar-filtro-nevera", "Pantalla de nevera Samsung con aviso de cambiar filtro"),
      lead="Cuando tu electrodoméstico Samsung necesita una pieza, la conseguimos e instalamos en la visita o en la siguiente, con garantía.",
      secs=[("Piezas más solicitadas", "Neveras: ventilador del evaporador, sensores, tarjeta de control, resistencia de descongelación, filtro de agua, empaques. Lavadoras: bomba de desagüe, válvula de entrada, seguro de puerta, amortiguadores, rodamientos. Secadoras: resistencia, termostatos, correa. Aires: tarjetas, sensores, capacitores, motores de ventilador."),
            ("Cómo pedir una pieza", "Envíanos por WhatsApp el modelo del equipo (etiqueta) y una foto o descripción de la falla. Con eso identificamos la pieza que necesitas y te confirmamos plazo y costo."),
            ("Instalación incluida", "Si nos encargamos de la reparación, instalamos la pieza y la probamos. La pieza instalada y la mano de obra tienen garantía.")],
      faq=[("¿Venden repuestos sin instalación?", "Escríbenos con el modelo y la pieza que necesitas y te decimos qué podemos ofrecerte."), ("¿Cuánto tardan en conseguir una pieza?", "Depende de la pieza y del modelo; te confirmamos el plazo antes de empezar la reparación.")]),
 dict(f="cuanto-cuesta-reparar-electrodomesticos-samsung-panama.html", chip="¿Cuánto cuesta reparar un Samsung?", t="¿Cuánto Cuesta Reparar una Nevera, Lavadora o Aire Samsung en Panamá?", h1="¿Cuánto cuesta reparar un electrodoméstico Samsung en Panamá?", foto=None,
      lead="El costo depende de la falla, la pieza y el modelo. Te lo confirmamos antes de la visita y antes de empezar la reparación.",
      secs=[("De qué depende el costo", "Del tipo de equipo, el modelo, la falla, la pieza que haya que reemplazar y la zona donde estás. Una limpieza de filtro o desagüe no cuesta lo mismo que cambiar una tarjeta de control o un compresor."),
            ("Cómo evitar sorpresas", "Pide siempre que el técnico te explique la falla y te dé el costo antes de empezar. Nosotros lo hacemos así: diagnóstico, explicación, costo y solo entonces reparación."),
            ("¿Reparar o reemplazar?", "Si la reparación cuesta una parte importante del valor de un equipo nuevo y el equipo es muy viejo, te explicamos las opciones con honestidad para que decidas.")],
      faq=[("¿Cuánto cuesta la visita de diagnóstico?", "Escríbenos por WhatsApp con el equipo, el modelo y la falla; te confirmamos el costo de la visita antes de ir."), ("¿El diagnóstico se descuenta de la reparación?", "Te explicamos las condiciones por WhatsApp antes de agendar la visita.")]),
 dict(f="garantia-samsung-panama-que-hacer.html", chip="Garantía Samsung en Panamá", t="Garantía Samsung en Panamá: Qué Hacer si tu Equipo Falla", h1="Garantía Samsung en Panamá: qué hacer si tu equipo falla", foto=None,
      lead="Antes de reparar, verifica si tu equipo sigue en garantía de fábrica. Te explicamos cómo y qué opciones tienes.",
      secs=[("Cómo saber si tu equipo está en garantía", "Revisa la factura de compra, la fecha y el plazo indicado por el vendedor o el fabricante. Guarda siempre el comprobante: lo vas a necesitar para cualquier reclamo."),
            ("Si el equipo ya no está en garantía", "Podemos revisarlo a domicilio, explicarte la falla y repararlo. Nuestra reparación incluye garantía propia sobre la pieza reemplazada y la mano de obra."),
            ("Antes de pagar una reparación", "Si tu equipo es reciente, consulta primero las condiciones de garantía del vendedor. Durante nuestro diagnóstico también te lo recordamos para que tomes la mejor decisión.")],
      faq=[("¿Cuánto dura la garantía de la reparación?", "Se confirma por escrito al momento del servicio, antes de que pagues."), ("¿Qué hago si la falla vuelve?", "Escríbenos por WhatsApp con la fecha del servicio; si está dentro del plazo, coordinamos la revisión.")]),
 dict(f="cambio-filtro-nevera-samsung-panama.html", chip="Cambio de filtro de nevera Samsung", t="Cambio de Filtro de Agua de Nevera Samsung en Panamá | Cada Cuánto", h1="Cambio de filtro de agua de nevera Samsung en Panamá", foto=("cambiar-filtro-nevera", "Pantalla de nevera Samsung con aviso de cambiar filtro"),
      lead="Cuando la nevera muestra «cambiar filtro» o el agua sale lenta o con mal sabor, es momento de reemplazar el filtro. Lo hacemos a domicilio.",
      secs=[("Cada cuánto cambiar el filtro", "Por lo general cada 6 meses, o antes si el agua sale lenta, con sabor u olor extraño, o si la nevera muestra el aviso de filtro. En zonas con agua con más sedimentos puede necesitar cambio más seguido."),
            ("Señales de que el filtro está vencido", "Luz o aviso de cambio de filtro, flujo de agua lento en el dispensador, hielo con mal sabor, o fábrica de hielo que produce poco."),
            ("Qué hacemos en la visita", "Identificamos el modelo, instalamos el filtro correcto, purgamos el sistema y reiniciamos el aviso. Si el problema de agua continúa, revisamos manguera y válvula de entrada.")],
      faq=[("¿Cómo reinicio el aviso de filtro?", "En la mayoría de neveras con dispensador se mantiene presionado un botón del panel durante unos segundos después de cambiar el filtro; el método exacto depende del modelo."), ("¿Puedo cambiar el filtro yo mismo?", "En muchos modelos es sencillo, pero si tienes dudas, el agua sale lenta o hay fugas, podemos hacerlo nosotros.")]),
 dict(f="servicio-tecnico-samsung-24-horas-panama.html", chip="Servicio técnico Samsung urgente", t="Servicio Técnico Samsung Urgente en Panamá | Visitas en 24 a 48 Horas", h1="Servicio técnico Samsung urgente en Panamá", foto=None,
      lead="Si tu nevera dejó de enfriar o tu lavadora gotea, escríbenos de inmediato: priorizamos las fallas urgentes y coordinamos visitas en 24 a 48 horas.",
      secs=[("Qué fallas son urgentes", "Nevera que no enfría o se apaga y prende sola, lavadora que gotea o inunda, equipos que saltan el breaker o huelen a quemado. En esos casos desconecta el equipo y escríbenos."),
            ("Mientras llega el técnico", "En la nevera, evita abrir la puerta para conservar el frío. En la lavadora, cierra la llave de agua y desconecta. En aires y secadoras, apaga y desconecta si hay olor a quemado."),
            ("Cómo pedir una visita urgente", f"Escríbenos por WhatsApp al {TEL} con tu zona, el equipo y el síntoma. Te confirmamos la disponibilidad más cercana.")],
      faq=[("¿Atienden emergencias?", "Priorizamos las fallas urgentes; la disponibilidad se confirma por WhatsApp según tu zona."), ("¿Atienden fines de semana?", "Trabajamos de lunes a sábado de 7:00am a 6:00pm.")]),
 dict(f="codigos-de-error-lavadora-samsung-panama.html", chip="Códigos de error lavadora Samsung", t="Códigos de Error de Lavadora Samsung: UE, 5E, 4E, dE, LE y Qué Hacer", h1="Códigos de error de lavadoras Samsung: qué significan", foto=("tecnico-lavadora-1", FOTO_FALLA["lavadoras"][1]),
      lead="Los códigos más comunes de las lavadoras Samsung y qué revisar antes de llamar al técnico.",
      secs=[("UE: carga desbalanceada", "La ropa se acumuló de un lado de la tina. Pausa, redistribuye la carga y evita lavar una sola prenda pesada. Verifica que las cuatro patas toquen el piso."),
            ("5E / SE: problema de desagüe", "La lavadora no logra sacar el agua. Revisa el filtro de desagüe y que la manguera no esté doblada ni tapada. Si persiste, puede ser la bomba."),
            ("4E: entrada de agua", "Poca o ninguna agua entra. Verifica que las llaves estén abiertas y limpia las mallas de las mangueras. Si sigue, puede ser la válvula de entrada."),
            ("dE / DC: puerta", "La puerta no cierra bien o el seguro no detecta el cierre. Revisa que nada la bloquee; si continúa, el seguro de la puerta puede necesitar reemplazo."),
            ("LE: fuga de agua", "Se detectó agua donde no debe. Cierra la llave, desconecta la lavadora y escríbenos para revisarla."),
            ("3E: motor", "Falla en el control del motor. Apaga, espera unos minutos y reinicia; si reaparece, requiere diagnóstico técnico.")],
      faq=[("¿Cómo reinicio mi lavadora Samsung cuando muestra un código?", "Apágala, desconéctala unos minutos, vuelve a conectarla y prueba. Si el código regresa, escríbenos."), ("¿El código de error significa que se dañó la tarjeta?", "No necesariamente: muchos códigos indican problemas simples como desagüe, agua o puerta.")]),
 dict(f="servicio-samsung-panama-donde-reparar.html", chip="Dónde reparar mi Samsung en Panamá", t="¿Dónde Reparar un Electrodoméstico Samsung en Panamá? | A Domicilio", h1="¿Dónde reparar un electrodoméstico Samsung en Panamá?", foto=None,
      lead="No tienes que ir a un taller: te visitamos en casa. Esta guía explica tus opciones y cómo pedir la visita.",
      secs=[("Opciones para reparar tu equipo", "Puedes consultar las condiciones de garantía del vendedor si el equipo es reciente, llevarlo a un taller o pedir un técnico a domicilio. Para equipos grandes como neveras y lavadoras, la visita a domicilio suele ser más cómoda."),
            ("Cómo pedir nuestra visita", f"Escríbenos por WhatsApp al {TEL} con el equipo, el modelo y la falla. Te confirmamos la disponibilidad en tu zona, normalmente en 24 a 48 horas."),
            ("Qué incluye", "Diagnóstico en el sitio, explicación de la falla, costo confirmado antes de reparar y garantía sobre la pieza y la mano de obra.")],
      faq=[("¿Tengo que llevar el equipo a un taller?", "No. Vamos a tu casa u oficina en Ciudad de Panamá, San Miguelito y Panamá Oeste."), ("¿Qué marca reparan?", "Nos especializamos en electrodomésticos Samsung: neveras, lavadoras, secadoras y aires acondicionados.")]),
]

def paginas_hubs():
    for h in HUBS:
        msg = f"Hola, vi su página '{h['h1']}' y necesito servicio técnico Samsung en Panamá"
        foto = f'<div class="hero-tarjeta foto">{pic(h["foto"][0], h["foto"][1], 0, 1024, 572, "fto", False)}</div>' if h["foto"] else f'<div class="hero-tarjeta"><b>{TEL}</b><small>{HORARIO}</small></div>'
        secs = "".join(f"<h2>{esc(a)}</h2><p>{esc(b)}</p>" for a, b in h["secs"])
        zs = '<h2>Zonas de cobertura</h2><div class="chips">' + "".join(f'<a href="zonas/{slug(z[0])}.html">{esc(z[0])}</a>' for z in ZONAS) + "</div>" if h.get("zonas") else ""
        rel = "".join(f'<a href="{o["f"]}">{esc(o["chip"])}</a>' for o in HUBS if o is not h)
        cuerpo = f'''{miga(0, (h["h1"], None))}<section class="hero chico"><div class="w hg"><div><span class="ey">Servicio técnico Samsung Panamá</span><h1>{esc(h["h1"])}</h1><p class="lead">{esc(h["lead"])}</p>
<div class="acc"><a class="btn wa lg" href="{wa(msg)}" target="_blank" rel="noopener" data-wa="hero">{ICONOS["wa"]} Escribir por WhatsApp</a></div></div>{foto}</div></section>
<section class="sec"><div class="w txt">{secs}<h2>Equipos Samsung que atendemos</h2>{tarjetas_eq(0)}{zs}<h2>Preguntas frecuentes</h2>{faq_html(h["faq"])}<h2>Búsquedas relacionadas</h2><div class="chips">{rel}</div></div></section>{cta(msg)}'''
        ld = [negocio_ld(), faq_ld(h["faq"]), bc((h["h1"], None))]
        escribir(h["f"], h["t"] if len(h["t"]) < 75 else h["h1"] + f" | {NOMBRE}", f"{h['lead']} WhatsApp {TEL}.", cuerpo, ld, "0.9")

def main():
    for d in ["electrodomesticos", "servicios", "zonas", "blog", "fallas"]:
        shutil.rmtree(OUT / d, ignore_errors=True)
    estaticos(); pagina_inicio(); paginas_equipo(); paginas_servicio(); paginas_zona(); paginas_blog(); pagina_diagnostico(); paginas_info(); paginas_hubs(); paginas_fallas(); paginas_zona_equipo(); indices()
    z = AQUI.parent.parent / "entrega" / "servicio-tecnico-samsung-panama.zip"
    z.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in OUT.rglob("*"):
            if p.is_file() and "_fuente" not in p.parts and "__pycache__" not in p.parts:
                zf.write(p, p.relative_to(OUT).as_posix())
    print(f"OK: {len(PAGINAS)} páginas → {z.name}")
main()
