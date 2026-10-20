# -*- coding: utf-8 -*-
"""Genera el sitio estático «Refrigeradoras Samsung Panamá» (carpeta ..) y el zip."""
import html, json, re, shutil, unicodedata, zipfile
from pathlib import Path
from urllib.parse import quote
from base import *
from fallas import FALLAS
from repuestos_blog import REPUESTOS, BLOG
import ilustraciones as IL

AQUI = Path(__file__).resolve().parent
OUT = AQUI.parent
FOTOS = AQUI / "fotos"
esc = lambda s: html.escape(str(s), quote=True)
def slug(s):
    s = unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")
PAGINAS = {}
_uid = [0]

ICONOS = {
 "wrench": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.2L3 17.8V21h3.2l6.3-6.3a4 4 0 0 0 5.2-5.4l-2.5 2.5-2.4-.6-.6-2.4z"/></svg>',
 "wa": '<svg viewBox="0 0 32 32" aria-hidden="true"><path fill="currentColor" d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 23.6c-2 0-4-.6-5.7-1.6l-.4-.2-3.9 1 1-3.8-.3-.4A10.6 10.6 0 1 1 16 26.6zm5.8-7.9c-.3-.2-1.9-.9-2.2-1s-.5-.2-.7.2-.8 1-1 1.2-.4.2-.7.1a8.700 8.700 0 0 1-4.300-3.800c-.3-.6.3-.5.9-1.700.1-.2 0-.4 0-.5l-1-2.300c-.2-.6-.5-.5-.7-.5h-.6a1.200 1.200 0 0 0-.9.4 3.700 3.700 0 0 0-1.100 2.700c0 1.600 1.200 3.200 1.300 3.400s2.300 3.500 5.600 4.900c2 .9 2.800.9 3.800.8a3.200 3.200 0 0 0 2.100-1.500 2.600 2.600 0 0 0 .2-1.500c-.1-.1-.3-.2-.6-.4z"/></svg>',
 "ok": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5 9-10"/></svg>',
 "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
 "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l8 3v6c0 5-3.500 8-8 9-4.500-1-8-4-8-9V6z"/><path d="M8.500 12l2.500 2.500 4.500-5"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s7-6 7-11a7 7 0 0 0-14 0c0 5 7 11 7 11z"/><circle cx="12" cy="10" r="2.500"/></svg>',
 "tag": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.500" cy="8.500" r="1.500"/></svg>',
}
def wa(msg=""): return f"https://wa.me/{WA}" + (f"?text={quote(msg)}" if msg else "")
def R(d): return "../" * d

def foto(slot, alt, svg, clase="img", ancho=900):
    """Foto propia si existe en _fuente/fotos/<slot>.(jpg|jpeg|png|webp); si no, ilustración vectorial."""
    for ext in ("jpg", "jpeg", "png", "webp"):
        f = FOTOS / f"{slot}.{ext}"
        if f.exists():
            from PIL import Image
            (OUT / "images" / "fotos").mkdir(parents=True, exist_ok=True)
            im = Image.open(f).convert("RGB"); im.thumbnail((ancho, ancho))
            im.save(OUT / "images" / "fotos" / f"{slot}.jpg", quality=84, optimize=True); im.save(OUT / "images" / "fotos" / f"{slot}.webp", quality=82)
            return ("foto", f'<picture class="{clase}"><source srcset="@R@images/fotos/{slot}.webp" type="image/webp"><img src="@R@images/fotos/{slot}.jpg" alt="{esc(alt)}" width="{im.width}" height="{im.height}" loading="lazy"></picture>')
    return ("svg", f'<div class="{clase} svg" aria-label="{esc(alt)}">{svg}</div>')

def img(slot, alt, svg, clase="img"):
    k, h = foto(slot, alt, svg, clase)
    return h
def uid():
    _uid[0] += 1; return f"u{_uid[0]}"

def cabeza(ruta, titulo, desc, ld=None, og="images/og.jpg"):
    depth = ruta.count("/"); r = R(depth); canon = f"{DOMINIO}/{ruta}"
    lds = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (ld or []))
    gtm = (f"<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','{GTM_ID}');</script>" if GTM_ID else "")
    ver = f'<meta name="google-site-verification" content="{esc(VERIFICACION)}">' if VERIFICACION else ""
    return (f'<!DOCTYPE html><html lang="es-PA"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{esc(titulo)}</title><meta name="description" content="{esc(desc)}">'
            f'<meta name="robots" content="index, follow, max-image-preview:large">{ver}<meta name="geo.region" content="PA-8"><meta name="geo.placename" content="Ciudad de Panamá"><link rel="canonical" href="{canon}">'
            f'<link rel="alternate" hreflang="es-pa" href="{canon}"><link rel="alternate" hreflang="x-default" href="{canon}"><link rel="icon" href="{r}images/logo/favicon.svg" type="image/svg+xml">'
            f'<meta property="og:type" content="website"><meta property="og:title" content="{esc(titulo)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{DOMINIO}/{og}"><meta property="og:locale" content="es_PA">'
            f'<meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#1428a0"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap"><link rel="stylesheet" href="{r}css/estilos.css">{lds}{gtm}</head><body>')

def menu(depth):
    r = R(depth)
    tp = "".join(f'<a href="{r}tipos-de-refrigeradora/{t[0]}.html">{esc(t[1])}</a>' for t in TIPOS)
    sv = "".join(f'<a href="{r}servicios/{k}.html">{esc(v[1])}</a>' for k, v in SERVICIOS.items())
    fa = "".join(f'<a href="{r}fallas/refrigeradora-samsung-{f[0]}.html">{esc(f[1].capitalize())}</a>' for f in FALLAS[:8]) + f'<a class="todas" href="{r}fallas/index.html">Ver las {len(FALLAS)} fallas →</a>'
    return (f'<header class="top"><div class="barra"><div class="w"><span>Servicio técnico de refrigeradoras Samsung en Ciudad de Panamá · {HORARIO}</span><a href="{wa()}" target="_blank" rel="noopener" data-wa="barra">{ICONOS["wa"]} {TEL}</a></div></div>'
            f'<div class="w nav"><a class="logo" href="{r}index.html" aria-label="{NOMBRE}"><span class="lg-i">{ICONOS["wrench"]}</span><span class="lg-t">Refrigeradoras<b>Samsung</b><small>Panamá</small></span></a>'
            f'<nav aria-label="Principal"><div class="dd"><a href="{r}tipos-de-refrigeradora/index.html">Tipos ▾</a><div class="pn">{tp}</div></div><div class="dd"><a href="{r}fallas/index.html">Fallas ▾</a><div class="pn">{fa}</div></div>'
            f'<div class="dd"><a href="{r}servicios/index.html">Servicios ▾</a><div class="pn">{sv}</div></div><a href="{r}repuestos/index.html">Repuestos</a><a href="{r}zonas-de-cobertura.html">Zonas</a><a href="{r}blog/index.html">Blog</a>'
            f'<a class="btn wa" href="{wa("Hola, necesito servicio técnico para mi refrigeradora Samsung en Panamá")}" target="_blank" rel="noopener" data-wa="menu">{ICONOS["wa"]} WhatsApp</a></nav>'
            f'<button class="burger" type="button" aria-label="Abrir menú" aria-expanded="false"><span></span></button></div>'
            f'<div class="mov" hidden><b>Tipos de refrigeradora</b>{tp}<b>Servicios</b>{sv}<b>Más</b><a href="{r}fallas/index.html">Fallas comunes</a><a href="{r}repuestos/index.html">Repuestos</a><a href="{r}diagnostico.html">Diagnóstico rápido</a><a href="{r}zonas-de-cobertura.html">Zonas</a><a href="{r}blog/index.html">Blog</a><a href="{r}garantia.html">Garantía</a><a href="{r}nosotros.html">Nosotros</a></div></header><main>')

def pie(depth):
    r = R(depth)
    cols = lambda items: "".join(items)
    return (f'</main><footer class="pie"><div class="w cols"><div><b class="pl">{NOMBRE}</b><p>Servicio técnico independiente especializado en refrigeradoras Samsung: Side by Side, French Door, congelador superior e inferior, con y sin dispensador de agua y hielo, en Ciudad de Panamá.</p>'
            f'<a class="btn wa" href="{wa()}" target="_blank" rel="noopener" data-wa="pie">{ICONOS["wa"]} {TEL}</a><p class="hor">{HORARIO}</p></div>'
            f'<div><b>Tipos</b>{cols(f"<a href=\"{r}tipos-de-refrigeradora/{t[0]}.html\">{esc(t[1])}</a>" for t in TIPOS)}</div>'
            f'<div><b>Fallas</b>{cols(f"<a href=\"{r}fallas/refrigeradora-samsung-{f[0]}.html\">Refrigeradora {esc(f[1])}</a>" for f in FALLAS[:7])}<a href="{r}fallas/index.html"><u>Todas las fallas</u></a></div>'
            f'<div><b>Servicios y zonas</b>{cols(f"<a href=\"{r}servicios/{k}.html\">{esc(v[1])}</a>" for k, v in list(SERVICIOS.items())[:4])}{cols(f"<a href=\"{r}zonas/{slug(z[0])}.html\">{esc(z[0])}</a>" for z in ZONAS[:4])}<a href="{r}zonas-de-cobertura.html"><u>Todas las zonas</u></a></div></div>'
            f'<div class="w legal"><span>© 2026 {NOMBRE}. Servicio técnico independiente. Samsung y los nombres de sus productos son marcas de su dueño y se mencionan solo para indicar el tipo de equipo que reparamos; no somos Samsung ni servicio técnico autorizado por Samsung.</span>'
            f'<span><a href="{r}mapa-del-sitio.html">Mapa del sitio</a> · <a href="{r}garantia.html">Garantía</a> · <a href="{r}privacidad.html">Privacidad</a> · <a href="{r}aviso-legal.html">Aviso legal</a></span></div></footer>'
            f'<div class="m-barra"><a class="btn wa" href="{wa("Hola, necesito servicio técnico para mi refrigeradora Samsung en Panamá")}" target="_blank" rel="noopener" data-wa="barra-movil">{ICONOS["wa"]} Escribir por WhatsApp</a></div>'
            f'<a class="wa-flot" href="{wa("Hola, necesito servicio técnico para mi refrigeradora Samsung en Panamá")}" target="_blank" rel="noopener" data-wa="flotante" aria-label="Escribir por WhatsApp">{ICONOS["wa"]}<span>Escríbenos</span></a><script src="{r}js/main.js" defer></script></body></html>')

def escribir(ruta, titulo, desc, cuerpo, ld=None, prioridad="0.7", og="images/og.jpg"):
    depth = ruta.count("/"); p = OUT / ruta; p.parent.mkdir(parents=True, exist_ok=True)
    h = cabeza(ruta, titulo, desc, ld, og) + menu(depth) + cuerpo + pie(depth)
    p.write_text(h.replace("@R@", R(depth)), encoding="utf-8")
    PAGINAS[ruta] = (prioridad, titulo)

def miga(depth, *partes):
    r = R(depth); t = f'<nav class="miga w" aria-label="Migas de pan"><a href="{r}index.html">Inicio</a>'
    for n, u in partes: t += " › " + (f'<a href="{r}{u}">{esc(n)}</a>' if u else f'<span>{esc(n)}</span>')
    return t + "</nav>"
def bc(*partes):
    items = [{"@type": "ListItem", "position": 1, "name": "Inicio", "item": DOMINIO + "/index.html"}]
    for i, (n, u) in enumerate(partes, 2):
        it = {"@type": "ListItem", "position": i, "name": n}
        if u: it["item"] = f"{DOMINIO}/{u}"
        items.append(it)
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}
def faq_ld(faq): return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
def faq_html(faq): return "".join(f'<details class="faq"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in faq)
def cta(msg, titulo="¿Tu refrigeradora Samsung tiene una falla?", texto="Escríbenos por WhatsApp con el modelo y el síntoma. Te confirmamos disponibilidad para tu zona en minutos.", fuente="cta"):
    return (f'<section class="sec"><div class="w"><div class="cta"><div><h2>{esc(titulo)}</h2><p>{esc(texto)}</p></div><a class="btn wa lg" href="{wa(msg)}" target="_blank" rel="noopener" data-wa="{fuente}">{ICONOS["wa"]} Escribir por WhatsApp</a></div></div></section>')
def negocio_ld(area=None):
    return {"@context": "https://schema.org", "@type": "LocalBusiness", "@id": DOMINIO + "/#negocio", "name": NOMBRE, "url": DOMINIO + "/", "telephone": TEL,
            "description": "Servicio técnico independiente de refrigeradoras Samsung a domicilio en Ciudad de Panamá.",
            "areaServed": [{"@type": "City", "name": "Ciudad de Panamá"}, {"@type": "AdministrativeArea", "name": "Panamá"}] if not area else [{"@type": "Place", "name": area}],
            "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "07:00", "closes": "18:00"}], "priceRange": "$$",
            "knowsAbout": ["Reparación de refrigeradoras Samsung", "Refrigeradoras Side by Side", "Refrigeradoras French Door", "Fábrica de hielo", "Compresor inverter"]}
def servicio_ld(nombre, desc, area="Ciudad de Panamá"):
    return {"@context": "https://schema.org", "@type": "Service", "name": nombre, "description": desc, "provider": {"@id": DOMINIO + "/#negocio"}, "areaServed": area, "serviceType": "Reparación de refrigeradoras"}

def msg_falla(f): return f"Hola, mi refrigeradora Samsung {f[1]}. ¿Pueden revisarla en Panamá?"
RELACION = {"no-enfria": ["ventilador-evaporador", "sensor-de-temperatura", "tarjeta-de-control", "compresor-inverter"], "no-enfria-abajo-pero-congela-arriba": ["ventilador-evaporador", "sensor-de-temperatura", "resistencia-de-descongelacion"],
 "congelador-no-congela": ["ventilador-evaporador", "compresor-inverter", "tarjeta-de-control"], "escarcha-en-el-congelador": ["resistencia-de-descongelacion", "empaque-de-puerta"], "gotea-agua-dentro": ["resistencia-de-descongelacion", "empaque-de-puerta"],
 "agua-debajo-de-la-refrigeradora": ["valvula-de-agua", "filtro-de-agua"], "hace-ruido": ["ventilador-evaporador", "motor-del-condensador", "compresor-inverter"], "zumbido-y-compresor-no-arranca": ["compresor-inverter", "tarjeta-de-control"],
 "se-apaga-y-prende-sola": ["tarjeta-de-control", "motor-del-condensador", "compresor-inverter"], "salta-el-breaker": ["resistencia-de-descongelacion", "compresor-inverter"], "no-hace-hielo": ["fabrica-de-hielo", "valvula-de-agua", "filtro-de-agua"],
 "dispensador-no-saca-agua": ["filtro-de-agua", "valvula-de-agua"], "agua-con-mal-sabor": ["filtro-de-agua"], "huele-mal": ["filtro-de-agua", "empaque-de-puerta"], "la-puerta-no-cierra-bien": ["empaque-de-puerta", "bisagras-y-puertas"],
 "condensacion-sudor-afuera": ["empaque-de-puerta"], "alarma-de-puerta-abierta": ["bisagras-y-puertas", "tarjeta-del-display"], "codigo-de-error-en-pantalla": ["tarjeta-de-control", "sensor-de-temperatura", "tarjeta-del-display"],
 "luz-interior-no-enciende": ["tarjeta-del-display"], "congela-las-verduras": ["sensor-de-temperatura", "tarjeta-de-control"], "fuga-de-gas-refrigerante": ["compresor-inverter"], "cortes-de-luz-danan-la-refrigeradora": ["tarjeta-de-control", "compresor-inverter"],
 "luz-del-filtro-parpadea": ["filtro-de-agua"], "modo-demostracion-activo": ["tarjeta-del-display", "tarjeta-de-control"], "compresor-caliente": ["motor-del-condensador", "compresor-inverter"], "hielo-se-pega-o-se-forman-bloques": ["fabrica-de-hielo", "empaque-de-puerta"]}
REP = {r[0]: r for r in REPUESTOS}

# ------------------------------------------------------------ páginas
def pagina_inicio():
    msg = "Hola, necesito servicio técnico para mi refrigeradora Samsung en Panamá"
    hero_img = img("hero", "Refrigeradora Samsung French Door con servicio técnico a domicilio en Panamá", IL.hero("hh"), "hero-img")
    tipos = "".join(f'<a class="card tipo" href="tipos-de-refrigeradora/{t[0]}.html"><div class="ilu">{IL.fridge(t[0] if t[0] != "congelador-superior" else "top-mount", uid()) if t[0] not in ("congelador-inferior",) else IL.fridge("bottom-mount", uid())}</div><h3>{esc(t[1])}</h3><p>{esc(t[2].capitalize())}</p><span class="mas">Ver servicio →</span></a>' for t in TIPOS)
    top = "".join(f'<a class="card falla-c" href="fallas/refrigeradora-samsung-{f[0]}.html"><span class="u {slug(f[2])}">{esc(f[2])}</span><h3>Refrigeradora Samsung {esc(f[1])}</h3><p>{esc(f[3][:110].rsplit(" ",1)[0])}…</p><span class="mas">Causas y solución →</span></a>' for f in FALLAS[:9])
    rep = "".join(f'<a href="repuestos/{r[0]}.html">{esc(r[1])}</a>' for r in REPUESTOS)
    zonas = "".join(f'<a href="zonas/{slug(z[0])}.html">{esc(z[0])}</a>' for z in ZONAS[:18])
    blog = "".join(f'<a class="card" href="blog/{b[0]}.html"><span class="ey">{esc(b[2].capitalize())}</span><h3>{esc(b[1])}</h3><p>{esc(b[3][:100].rsplit(" ",1)[0])}…</p><span class="mas">Leer →</span></a>' for b in BLOG[:3])
    pasos = [("Escríbenos por WhatsApp", "Cuéntanos el modelo y el síntoma. Una foto de la etiqueta interior y de la falla nos ayuda."), ("Coordinamos la visita", "Confirmamos disponibilidad en tu zona, normalmente en 24 a 48 horas."), ("Diagnóstico y reparación", "Medimos temperaturas y voltaje, te explicamos la falla y el costo, y reparamos si estás de acuerdo.")]
    cuerpo = f'''<section class="hero"><div class="w hg"><div><span class="ey">Servicio técnico independiente · Panamá</span><h1>Servicio técnico de refrigeradoras Samsung en Panamá</h1>
<p class="lead">Reparamos neveras y refrigeradoras Samsung a domicilio en Ciudad de Panamá, San Miguelito y Panamá Oeste: no enfría, escarcha, gotea, hace ruido, no hace hielo o muestra códigos de error. Diagnóstico honesto, costo claro y garantía.</p>
<div class="acc"><a class="btn wa lg" href="{wa(msg)}" target="_blank" rel="noopener" data-wa="hero">{ICONOS["wa"]} Escribir por WhatsApp</a><a class="btn sec lg" href="diagnostico.html">Diagnóstico rápido</a></div>
<ul class="pts"><li>Visitas en 24 a 48 horas</li><li>Garantía en pieza y mano de obra</li><li>{HORARIO}</li></ul></div><div class="hero-media">{hero_img}</div></div></section>
<section class="conf"><div class="w"><div>{ICONOS["ok"]}<span><b>Especialistas en Samsung</b><small>Solo refrigeradoras</small></span></div><div>{ICONOS["tag"]}<span><b>Costo claro</b><small>Antes de reparar</small></span></div><div>{ICONOS["shield"]}<span><b>Garantía</b><small>Pieza y mano de obra</small></span></div><div>{ICONOS["clock"]}<span><b>{len(ZONAS)} zonas</b><small>Visita en 24-48 h</small></span></div></div></section>
<section class="sec"><div class="w"><div class="cab"><span class="ey">Tipos de refrigeradora</span><h2>Reparamos todos los tipos de refrigeradora Samsung</h2><p>Side by Side, French Door, congelador superior o inferior, con dispensador de agua y hielo y modelos con pantalla.</p></div><div class="grid g3">{tipos}</div></div></section>
<section class="sec alt"><div class="w"><div class="cab"><span class="ey">Fallas más buscadas</span><h2>¿Qué le pasa a tu refrigeradora Samsung?</h2><p>Explicamos {len(FALLAS)} fallas: causas, qué revisar y cuándo llamar al técnico.</p></div><div class="grid g3">{top}</div><p style="margin-top:18px"><a class="btn lg" href="fallas/index.html">Ver las {len(FALLAS)} fallas</a></p></div></section>
<section class="sec"><div class="w"><div class="cab"><span class="ey">Así trabajamos</span><h2>Cómo agendar el servicio técnico de tu refrigeradora Samsung</h2></div><ol class="pasos">{"".join(f"<li><b>{esc(a)}</b><p>{esc(b)}</p></li>" for a, b in pasos)}</ol></div></section>
<section class="sec alt"><div class="w split"><div><span class="ey">Por qué elegirnos</span><h2>Reparación de refrigeradoras con honestidad</h2><ul class="lista chk"><li><b>Diagnóstico honesto:</b> te explicamos la falla antes de reparar. Si no vale la pena, te lo decimos.</li><li><b>Mediciones, no suposiciones:</b> revisamos temperaturas, voltaje, ventiladores, descongelación y sellado.</li><li><b>Garantía real:</b> sobre la pieza reemplazada y la mano de obra; el plazo se confirma antes de empezar.</li><li><b>Costo claro:</b> la visita y la reparación se confirman antes de empezar.</li></ul>
<p class="aviso">Somos un servicio técnico independiente. No somos Samsung ni servicio técnico autorizado por Samsung; si tu refrigeradora está en garantía de fábrica, te lo decimos durante el diagnóstico.</p></div><div>{img("tecnico", "Técnico revisando una refrigeradora Samsung en una cocina de Panamá", IL.pieza("pp"), "foto-lado")}</div></div></section>
<section class="sec"><div class="w"><div class="cab"><span class="ey">Repuestos</span><h2>Piezas que reparamos y cambiamos</h2><p>Tarjetas, compresor, ventiladores, sensores, resistencias, válvulas, empaques y más.</p></div><div class="chips">{rep}</div></div></section>
<section class="sec alt"><div class="w split inv"><div>{img("zonas", "Zonas de cobertura del servicio técnico de refrigeradoras Samsung en Panamá", IL.mapa_zona("mm"), "foto-lado")}</div><div><span class="ey">Cobertura</span><h2>Servicio técnico de refrigeradoras Samsung en tu zona</h2><p>Llegamos a {len(ZONAS)} zonas de Ciudad de Panamá, San Miguelito y Panamá Oeste.</p><div class="chips">{zonas}</div><p><a href="zonas-de-cobertura.html">Ver todas las zonas →</a></p></div></div></section>
<section class="sec"><div class="w"><div class="cab"><span class="ey">Blog</span><h2>Guías sobre refrigeradoras Samsung</h2></div><div class="grid g3">{blog}</div><p style="margin-top:18px"><a href="blog/index.html">Ver todas las guías →</a></p></div></section>
<section class="sec alt"><div class="w"><div class="cab"><span class="ey">Dudas frecuentes</span><h2>Preguntas frecuentes sobre el servicio técnico de refrigeradoras Samsung</h2></div>{faq_html(FAQ_GENERAL)}</div></section>
{cta(msg)}'''
    ld = [negocio_ld(), faq_ld(FAQ_GENERAL), {"@context": "https://schema.org", "@type": "WebSite", "name": NOMBRE, "url": DOMINIO + "/", "inLanguage": "es-PA"}]
    escribir("index.html", f"Servicio Técnico de Refrigeradoras Samsung en Panamá | Reparación a domicilio | {TEL}",
             "Reparación de refrigeradoras y neveras Samsung en Panamá: no enfría, escarcha, gotea, hace ruido, dispensador y hielo. Side by Side y French Door. Visitas en 24-48 horas y garantía. WhatsApp +507 6933-7976.", cuerpo, ld, "1.0")

def paginas_tipos():
    cards = ""
    for t in TIPOS:
        s, nombre, desc, pref, intro, piezas, fallas = t
        kind = {"congelador-superior": "top-mount", "congelador-inferior": "bottom-mount"}.get(s, s)
        ilu = img("tipo-" + s, f"Refrigeradora Samsung {nombre}", IL.fridge(kind, uid()), "ilu-grande")
        msg = f"Hola, necesito servicio técnico para mi refrigeradora Samsung {nombre} en Panamá"
        rel = "".join(f'<a href="../fallas/refrigeradora-samsung-{f[0]}.html">Refrigeradora {esc(f[1])}</a>' for f in FALLAS[:12])
        faq = [(f"¿Reparan refrigeradoras Samsung {nombre}?", f"Sí, reparamos refrigeradoras Samsung {nombre} ({desc}) a domicilio en Ciudad de Panamá."), (f"¿Cuáles son las fallas más comunes en una {nombre}?", "; ".join(fallas) + "."), ("¿Cuánto tarda la visita?", "Coordinamos visitas en 24 a 48 horas en la mayoría de las zonas.")]
        prefijo = f' Los modelos suelen empezar por «{pref}».' if pref else ""
        cuerpo = f'''{miga(1, ("Tipos de refrigeradora", "tipos-de-refrigeradora/index.html"), (nombre, None))}<section class="hero chico"><div class="w hg"><div><span class="ey">Refrigeradoras Samsung</span><h1>Servicio técnico de refrigeradoras Samsung {esc(nombre)} en Panamá</h1><p class="lead">{esc(intro)}{prefijo}</p><div class="acc"><a class="btn wa lg" href="{wa(msg)}" target="_blank" rel="noopener" data-wa="hero">{ICONOS["wa"]} Escribir por WhatsApp</a></div></div><div class="hero-media">{ilu}</div></div></section>
<section class="sec"><div class="w split"><div><h2>Qué incluye una {esc(nombre)} Samsung</h2><ul class="lista chk">{"".join(f"<li>{esc(p)}</li>" for p in piezas)}</ul></div><div><h2>Fallas comunes en una {esc(nombre)}</h2><ul class="lista chk">{"".join(f"<li>{esc(p)}</li>" for p in fallas)}</ul></div></div></section>
<section class="sec alt"><div class="w"><div class="cab"><span class="ey">Fallas</span><h2>Fallas de refrigeradoras Samsung que explicamos</h2></div><div class="chips">{rel}</div></div></section>
<section class="sec"><div class="w"><h2>Preguntas frecuentes</h2>{faq_html(faq)}</div></section>{cta(msg, f"¿Tu refrigeradora {nombre} tiene una falla?")}'''
        escribir(f"tipos-de-refrigeradora/{s}.html", f"Reparación de refrigeradoras Samsung {nombre} en Panamá | Servicio técnico", f"Servicio técnico de refrigeradoras Samsung {nombre} en Panamá: fallas comunes, diagnóstico y reparación a domicilio. Garantía. WhatsApp {TEL}.", cuerpo,
                 [negocio_ld(), servicio_ld(f"Reparación de refrigeradoras Samsung {nombre}", intro), faq_ld(faq), bc(("Tipos de refrigeradora", "tipos-de-refrigeradora/index.html"), (nombre, None))], "0.8")
        cards += f'<a class="card tipo" href="{s}.html"><div class="ilu">{IL.fridge(kind, uid())}</div><h3>{esc(nombre)}</h3><p>{esc(desc.capitalize())}</p><span class="mas">Ver servicio →</span></a>'
    cuerpo = f'''{miga(1, ("Tipos de refrigeradora", None))}<section class="sec"><div class="w"><div class="cab"><h1>Tipos de refrigeradora Samsung que reparamos en Panamá</h1><p>Cada tipo de refrigeradora tiene fallas y piezas distintas. Elige el tuyo.</p></div><div class="grid g3">{cards}</div></div></section>{cta("Hola, necesito servicio técnico para mi refrigeradora Samsung en Panamá")}'''
    escribir("tipos-de-refrigeradora/index.html", "Tipos de refrigeradora Samsung: Side by Side, French Door, congelador superior e inferior | Panamá", f"Servicio técnico para todos los tipos de refrigeradora Samsung en Panamá: Side by Side, French Door, congelador superior e inferior, con dispensador y con pantalla. WhatsApp {TEL}.", cuerpo, [bc(("Tipos de refrigeradora", None))], "0.8")

def paginas_fallas():
    for i, f in enumerate(FALLAS):
        s, titulo, urg, sint, causas, revisar, llamar, tiempo, prev, faq = f
        ruta = f"fallas/refrigeradora-samsung-{s}.html"
        msg = msg_falla(f)
        rel_f = [FALLAS[(i + d) % len(FALLAS)] for d in (1, 2, 3, 4)]
        rel_r = [REP[x] for x in RELACION.get(s, []) if x in REP]
        blog_r = [b for b in BLOG if b[2] == "fallas"][:3]
        toc = '<nav class="toc" aria-label="Contenido"><b>En esta página</b><a href="#sintoma">Síntoma</a><a href="#causas">Causas</a><a href="#revisar">Qué revisar</a><a href="#cuando">Cuándo llamar</a><a href="#faq">Preguntas</a></nav>'
        prev_html = f'<h2 id="prev">Cómo prevenirlo</h2><p>{esc(prev)}</p>' if prev != "—" else ""
        cuerpo = f'''{miga(1, ("Fallas", "fallas/index.html"), (f"Refrigeradora {titulo}", None))}<section class="sec"><div class="w art"><article class="txt"><span class="u {slug(urg)}">{esc(urg)}</span><h1>Refrigeradora Samsung {esc(titulo)}: causas y solución en Panamá</h1>
<p class="lead">{esc(sint)} Estas son las causas más comunes, qué puedes revisar y cuándo conviene llamar al técnico.</p>{toc}
<h2 id="sintoma">Síntoma: refrigeradora Samsung {esc(titulo)}</h2><p>{esc(sint)} Es una consulta frecuente en refrigeradoras (neveras) Samsung de todos los tipos: Side by Side, French Door, congelador superior e inferior.</p>
<h2 id="causas">Causas más comunes</h2><ol class="causas">{"".join(f"<li><b>{esc(a)}.</b> {esc(b)}</li>" for a, b in causas)}</ol>
<h2 id="revisar">Qué puedes revisar antes de llamar</h2><ul class="lista chk">{"".join(f"<li>{esc(x)}</li>" for x in revisar)}</ul>
<h2 id="cuando">Cuándo llamar al técnico</h2><p>{esc(llamar)}</p><p><b>Tiempo típico:</b> {esc(tiempo)}</p>{prev_html}
<div class="cta mini"><div><b>¿Quieres que la revisemos?</b><p>Escríbenos con el modelo y una foto del problema.</p></div><a class="btn wa" href="{wa(msg)}" target="_blank" rel="noopener" data-wa="falla">{ICONOS["wa"]} Consultar por WhatsApp</a></div>
<h2 id="faq">Preguntas frecuentes</h2>{faq_html(faq)}</article>
<aside class="lado"><div class="caja"><b>Servicio a domicilio</b><p>Refrigeradoras Samsung en Ciudad de Panamá, San Miguelito y Panamá Oeste.</p><a class="btn wa" href="{wa(msg)}" target="_blank" rel="noopener" data-wa="lateral">{ICONOS["wa"]} {TEL}</a><small>{HORARIO}</small></div>
{f'<div class="caja"><b>Piezas relacionadas</b>{"".join(f"<a href=\"../repuestos/{r[0]}.html\">{esc(r[1])}</a>" for r in rel_r)}</div>' if rel_r else ""}
<div class="caja"><b>Otras fallas</b>{"".join(f"<a href=\"refrigeradora-samsung-{x[0]}.html\">Refrigeradora {esc(x[1])}</a>" for x in rel_f)}</div>
<div class="caja"><b>Tipos</b>{"".join(f"<a href=\"../tipos-de-refrigeradora/{t[0]}.html\">{esc(t[1])}</a>" for t in TIPOS[:4])}</div></aside></div></section>{cta(msg)}'''
        escribir(ruta, f"Refrigeradora Samsung {titulo}: causas y reparación en Panamá | {TEL}", f"¿Tu refrigeradora Samsung {titulo}? Causas más comunes, qué revisar y cuándo llamar al técnico. Servicio a domicilio en Panamá. WhatsApp {TEL}.", cuerpo,
                 [negocio_ld(), servicio_ld(f"Reparación de refrigeradora Samsung que {titulo}", sint), faq_ld(faq), bc(("Fallas", "fallas/index.html"), (f"Refrigeradora {titulo}", None))], "0.8")
    cards = "".join(f'<a class="card falla-c" href="refrigeradora-samsung-{f[0]}.html"><span class="u {slug(f[2])}">{esc(f[2])}</span><h3>Refrigeradora Samsung {esc(f[1])}</h3><p>{esc(f[3][:120].rsplit(" ",1)[0])}…</p><span class="mas">Causas y solución →</span></a>' for f in FALLAS)
    cuerpo = f'''{miga(1, ("Fallas", None))}<section class="sec"><div class="w"><div class="cab"><h1>Fallas comunes de refrigeradoras Samsung y cómo solucionarlas</h1><p>{len(FALLAS)} fallas explicadas con sus causas, qué revisar y cuándo llamar al técnico.</p></div><div class="grid g3">{cards}</div></div></section>{cta("Hola, mi refrigeradora Samsung tiene una falla y necesito ayuda en Panamá")}'''
    escribir("fallas/index.html", f"Fallas comunes de refrigeradoras Samsung: {len(FALLAS)} problemas y soluciones | Panamá", f"{len(FALLAS)} fallas de refrigeradoras y neveras Samsung explicadas: no enfría, escarcha, gotea, ruido, hielo, dispensador y códigos de error. WhatsApp {TEL}.", cuerpo, [bc(("Fallas", None))], "0.9")

def paginas_repuestos():
    cards = ""
    for r in REPUESTOS:
        s, nombre, fn, senales, cuando, nota = r
        msg = f"Hola, creo que mi refrigeradora Samsung necesita: {nombre}"
        usos = [f for f in FALLAS if s in RELACION.get(f[0], [])][:6]
        faq = [(f"¿Cuándo se cambia: {nombre.lower()}?", cuando), (f"¿Instalan {nombre.lower()} a domicilio?", "Sí, en la mayoría de los casos el cambio se hace en tu casa. Si la pieza hay que pedirla, te avisamos el plazo."), ("¿Tiene garantía?", "Sí, la pieza reemplazada y la mano de obra tienen garantía; el plazo se confirma antes de empezar.")]
        cuerpo = f'''{miga(1, ("Repuestos", "repuestos/index.html"), (nombre, None))}<section class="sec"><div class="w art"><article class="txt"><h1>{esc(nombre)} de refrigeradora Samsung en Panamá</h1><p class="lead">{esc(fn)}</p>
<h2>Señales de que falla</h2><ul class="lista chk">{"".join(f"<li>{esc(x)}</li>" for x in senales)}</ul><h2>Cuándo se cambia</h2><p>{esc(cuando)}</p><p>{esc(nota)}</p>
<h2>Fallas relacionadas</h2><div class="chips">{"".join(f"<a href=\"../fallas/refrigeradora-samsung-{f[0]}.html\">Refrigeradora {esc(f[1])}</a>" for f in usos)}</div><h2>Preguntas frecuentes</h2>{faq_html(faq)}</article>
<aside class="lado"><div class="caja">{img("repuesto-" + s, nombre, IL.pieza(uid()), "ilu-lado")}<b>Diagnóstico a domicilio</b><p>Revisamos la pieza en tu casa y te confirmamos el costo antes de cambiarla.</p><a class="btn wa" href="{wa(msg)}" target="_blank" rel="noopener" data-wa="lateral">{ICONOS["wa"]} {TEL}</a></div></aside></div></section>{cta(msg, f"¿Necesitas revisar: {nombre.lower()}?")}'''
        escribir(f"repuestos/{s}.html", f"{nombre} de refrigeradora Samsung en Panamá | Cambio a domicilio", f"{fn[:140]} Cambio y reparación a domicilio en Panamá. WhatsApp {TEL}.", cuerpo,
                 [negocio_ld(), servicio_ld(f"Cambio de {nombre.lower()} de refrigeradora Samsung", fn), faq_ld(faq), bc(("Repuestos", "repuestos/index.html"), (nombre, None))], "0.7")
        cards += f'<a class="card" href="{s}.html"><h3>{esc(nombre)}</h3><p>{esc(fn[:120].rsplit(" ",1)[0])}…</p><span class="mas">Ver más →</span></a>'
    cuerpo = f'''{miga(1, ("Repuestos", None))}<section class="sec"><div class="w"><div class="cab"><h1>Repuestos y piezas de refrigeradoras Samsung: cambio a domicilio en Panamá</h1><p>Estas son las piezas que reparamos y cambiamos con más frecuencia.</p></div><div class="grid g3">{cards}</div></div></section>{cta("Hola, necesito una pieza para mi refrigeradora Samsung en Panamá")}'''
    escribir("repuestos/index.html", "Repuestos y piezas de refrigeradoras Samsung en Panamá | Cambio a domicilio", f"Tarjeta de control, compresor inverter, ventiladores, sensores, resistencias, válvulas, empaques y filtros para refrigeradoras Samsung en Panamá. WhatsApp {TEL}.", cuerpo, [bc(("Repuestos", None))], "0.8")

def paginas_servicios():
    cards = ""
    for k, (titulo, corto, desc, puntos) in SERVICIOS.items():
        msg = f"Hola, quiero agendar: {corto.lower()} para mi refrigeradora Samsung en Panamá"
        faq = [("¿Qué refrigeradoras atienden?", "Side by Side, French Door, congelador superior e inferior, con y sin dispensador de agua y hielo."), ("¿Dónde lo hacen?", "En Ciudad de Panamá, San Miguelito y Panamá Oeste. Escríbenos por WhatsApp para confirmar tu zona."), ("¿Cuánto cuesta?", "Te confirmamos el costo por WhatsApp antes de ir, según el servicio y el modelo.")]
        cuerpo = f'''{miga(1, ("Servicios", "servicios/index.html"), (corto, None))}<section class="sec"><div class="w split"><div class="txt"><h1>{esc(titulo)}</h1><p class="lead">{esc(desc)}</p><h2>Qué incluye</h2><ul class="lista chk">{"".join(f"<li>{esc(p)}</li>" for p in puntos)}</ul></div><div>{img("servicio-" + k, corto, IL.pieza(uid()), "foto-lado")}</div></div>
<div class="w"><h2>Preguntas frecuentes</h2>{faq_html(faq)}</div></section>{cta(msg, f"Agenda: {corto.lower()}")}'''
        escribir(f"servicios/{k}.html", f"{titulo} | {TEL}", f"{desc[:150]} WhatsApp {TEL}.", cuerpo, [negocio_ld(), servicio_ld(titulo, desc), faq_ld(faq), bc(("Servicios", "servicios/index.html"), (corto, None))], "0.8")
        cards += f'<a class="card" href="{k}.html"><h3>{esc(corto)}</h3><p>{esc(desc[:130].rsplit(" ",1)[0])}…</p><span class="mas">Ver más →</span></a>'
    cuerpo = f'''{miga(1, ("Servicios", None))}<section class="sec"><div class="w"><div class="cab"><h1>Servicios de refrigeradoras Samsung a domicilio en Panamá</h1></div><div class="grid g3">{cards}</div></div></section>{cta("Hola, necesito servicio técnico para mi refrigeradora Samsung en Panamá")}'''
    escribir("servicios/index.html", "Servicios técnicos para refrigeradoras Samsung en Panamá | Reparación, mantenimiento, filtro, hielo", f"Reparación, mantenimiento, diagnóstico, cambio de filtro de agua, fábrica de hielo y fugas en refrigeradoras Samsung en Panamá. WhatsApp {TEL}.", cuerpo, [bc(("Servicios", None))], "0.8")

def paginas_zonas():
    for i, (z, tipo, area) in enumerate(ZONAS):
        s = slug(z); t1, t2 = TIPO_TXT[tipo]; vec = [ZONAS[(i + d) % len(ZONAS)] for d in (1, 2, 3, 4)]
        msg = f"Hola, necesito servicio técnico para mi refrigeradora Samsung en {z}"
        fl = [FALLAS[(i + d) % len(FALLAS)] for d in range(0, 6)]
        faq = [(f"¿Atienden refrigeradoras Samsung en {z}?", f"Sí, damos servicio técnico de refrigeradoras Samsung a domicilio en {z} ({area}). Escríbenos por WhatsApp y te confirmamos disponibilidad."), (f"¿Cuánto tardan en llegar a {z}?", "Coordinamos visitas en 24 a 48 horas en la mayoría de las zonas."), ("¿Qué tipos de refrigeradora reparan?", "Side by Side, French Door, congelador superior e inferior, con dispensador y con pantalla.")]
        cuerpo = f'''{miga(1, ("Zonas", "zonas-de-cobertura.html"), (z, None))}<section class="hero chico"><div class="w hg"><div><span class="ey">{esc(area)}</span><h1>Servicio técnico de refrigeradoras Samsung en {esc(z)}</h1><p class="lead">Reparamos neveras y refrigeradoras Samsung a domicilio en {esc(z)}: no enfría, escarcha, gotea, ruido, hielo y dispensador. Diagnóstico honesto, costo claro y garantía.</p><div class="acc"><a class="btn wa lg" href="{wa(msg)}" target="_blank" rel="noopener" data-wa="hero">{ICONOS["wa"]} Escribir por WhatsApp</a></div></div><div class="hero-media">{img("hero-zona", f"Servicio técnico de refrigeradoras en {z}", IL.mapa_zona(uid()), "hero-img")}</div></div></section>
<section class="sec"><div class="w txt"><h2>Técnico de refrigeradoras Samsung a domicilio en {esc(z)}</h2><p>{esc(t1)}</p><p>{esc(t2)}</p><h2>Fallas que atendemos en {esc(z)}</h2><div class="grid g3">{"".join(f'<a class="card falla-c" href="../fallas/refrigeradora-samsung-{f[0]}.html"><h3>Refrigeradora {esc(f[1])}</h3><span class="mas">Ver causas →</span></a>' for f in fl)}</div>
<h2>Tipos de refrigeradora Samsung en {esc(z)}</h2><div class="chips">{"".join(f"<a href=\"../tipos-de-refrigeradora/{t[0]}.html\">{esc(t[1])}</a>" for t in TIPOS)}</div><h2>Preguntas frecuentes en {esc(z)}</h2>{faq_html(faq)}<h2>Zonas cercanas</h2><div class="chips">{"".join(f"<a href=\"{slug(v[0])}.html\">{esc(v[0])}</a>" for v in vec)}</div></div></section>{cta(msg, f"¿Refrigeradora Samsung con falla en {z}?")}'''
        escribir(f"zonas/{s}.html", f"Servicio Técnico de Refrigeradoras Samsung en {z} | Reparación a domicilio | {TEL}", f"Reparación de refrigeradoras y neveras Samsung a domicilio en {z}, Panamá: no enfría, escarcha, gotea, ruido, hielo. Garantía y visitas en 24-48 horas. WhatsApp {TEL}.", cuerpo,
                 [negocio_ld(area=z), servicio_ld(f"Servicio técnico de refrigeradoras Samsung en {z}", f"Reparación a domicilio de refrigeradoras Samsung en {z}.", z), faq_ld(faq), bc(("Zonas", "zonas-de-cobertura.html"), (z, None))], "0.6")
    por = {}
    for z, t, a in ZONAS: por.setdefault(a, []).append(z)
    bl = "".join(f'<h2>{esc(a)}</h2><div class="chips">{"".join(f"<a href=\"zonas/{slug(z)}.html\">{esc(z)}</a>" for z in zs)}</div>' for a, zs in por.items())
    cuerpo = f'''{miga(0, ("Zonas de cobertura", None))}<section class="sec"><div class="w txt"><h1>Zonas de cobertura: servicio técnico de refrigeradoras Samsung en Panamá</h1><p class="lead">Atendemos a domicilio en {len(ZONAS)} zonas de Ciudad de Panamá, San Miguelito y Panamá Oeste. Si tu zona no aparece, escríbenos.</p>{bl}</div></section>{cta("Hola, quiero saber si dan servicio técnico de refrigeradoras Samsung en mi zona de Panamá")}'''
    escribir("zonas-de-cobertura.html", f"Zonas de cobertura: servicio técnico de refrigeradoras Samsung en Panamá | {TEL}", f"{len(ZONAS)} zonas donde reparamos refrigeradoras Samsung en Panamá: Ciudad de Panamá, San Miguelito, Arraiján, La Chorrera y más. WhatsApp {TEL}.", cuerpo, [bc(("Zonas de cobertura", None))], "0.8")

def paginas_blog():
    cards = ""
    for sl, titulo, cat, res, secs in BLOG:
        msg = f"Hola, leí '{titulo}' y necesito servicio técnico para mi refrigeradora Samsung"
        txt = "".join((f"<h2>{esc(h)}</h2>{t}" if "<ul>" in t else f"<h2>{esc(h)}</h2><p>{esc(t)}</p>") for h, t in secs)
        rel = "".join(f'<a href="{b[0]}.html">{esc(b[1])}</a>' for b in BLOG if b[2] == cat and b[0] != sl)
        fl = "".join(f'<a href="../fallas/refrigeradora-samsung-{f[0]}.html">Refrigeradora {esc(f[1])}</a>' for f in FALLAS[:6])
        cuerpo = f'''{miga(1, ("Blog", "blog/index.html"), (titulo, None))}<section class="sec"><div class="w txt"><span class="ey">{esc(cat.capitalize())}</span><h1>{esc(titulo)}</h1><p class="lead">{esc(res)}</p>{txt}<p><a href="../fallas/index.html">Ver todas las fallas de refrigeradoras Samsung →</a></p>{f'<h2>Te puede interesar</h2><div class="chips">{rel}</div>' if rel else ""}<h2>Fallas relacionadas</h2><div class="chips">{fl}</div></div></section>{cta(msg)}'''
        ld = [{"@context": "https://schema.org", "@type": "Article", "headline": titulo, "description": res, "inLanguage": "es-PA", "author": {"@type": "Organization", "name": NOMBRE}, "publisher": {"@type": "Organization", "name": NOMBRE}, "mainEntityOfPage": f"{DOMINIO}/blog/{sl}.html", "datePublished": "2026-10-20", "dateModified": "2026-10-20"}, bc(("Blog", "blog/index.html"), (titulo, None))]
        escribir(f"blog/{sl}.html", f"{titulo} | {NOMBRE}", res, cuerpo, ld, "0.6")
        cards += f'<a class="card" href="{sl}.html"><span class="ey">{esc(cat.capitalize())}</span><h3>{esc(titulo)}</h3><p>{esc(res)}</p><span class="mas">Leer →</span></a>'
    cuerpo = f'''{miga(1, ("Blog", None))}<section class="sec"><div class="w"><div class="cab"><h1>Blog: guías de refrigeradoras Samsung en Panamá</h1><p>Consejos para entender las fallas, el mantenimiento y el cuidado de tu refrigeradora Samsung.</p></div><div class="grid g3">{cards}</div></div></section>'''
    escribir("blog/index.html", f"Blog de refrigeradoras Samsung en Panamá | {NOMBRE}", "Guías sobre fallas, mantenimiento y ahorro de energía de refrigeradoras Samsung en Panamá.", cuerpo, [bc(("Blog", None))], "0.7")

def pagina_diagnostico():
    cards = "".join(f'<article class="falla dg"><span class="u {slug(f[2])}">{esc(f[2])}</span><h3>Refrigeradora {esc(f[1])}</h3><p><b>Causa probable:</b> {esc(f[4][0][0])}: {esc(f[4][0][1])}</p><p><b>Qué revisar:</b> {esc(f[5][0])}</p><p><a class="btn sm" href="fallas/refrigeradora-samsung-{f[0]}.html">Ver más</a> <a class="btn sm wa" href="{wa(msg_falla(f))}" target="_blank" rel="noopener" data-wa="diagnostico">{ICONOS["wa"]} Consultar</a></p></article>' for f in FALLAS)
    tabs = '<button class="tab on" data-f="todos">Todas</button><button class="tab" data-f="Urgente">Urgentes</button><button class="tab" data-f="Revisar pronto">Revisar pronto</button><button class="tab" data-f="Vigilar">Vigilar</button>'
    cards = cards.replace('<article class="falla dg">', '<article class="falla dg">')
    # etiqueta de urgencia para el filtro
    cards2 = ""
    for f in FALLAS:
        cards2 += cards.split("</article>")[FALLAS.index(f)].replace('<article class="falla dg">', f'<article class="falla dg" data-eq="{esc(f[2])}">') + "</article>"
    cuerpo = f'''{miga(0, ("Diagnóstico rápido", None))}<section class="sec"><div class="w"><div class="cab"><h1>Diagnóstico rápido: ¿qué le pasa a tu refrigeradora Samsung?</h1><p>{len(FALLAS)} fallas con la causa más probable, qué revisar y qué tan urgente es.</p></div><div class="tabs">{tabs}</div><div class="grid g2" id="dg">{cards2}</div></div></section>{cta("Hola, necesito un diagnóstico para mi refrigeradora Samsung en Panamá")}'''
    escribir("diagnostico.html", f"Diagnóstico rápido de refrigeradoras Samsung | {NOMBRE}", f"{len(FALLAS)} fallas de refrigeradoras Samsung con causa probable y urgencia. Consulta tu caso por WhatsApp.", cuerpo, [bc(("Diagnóstico rápido", None))], "0.8")

def paginas_info():
    msg = "Hola, necesito servicio técnico para mi refrigeradora Samsung en Panamá"
    c = f'''{miga(0, ("Garantía", None))}<section class="sec"><div class="w txt"><h1>Garantía del servicio técnico de refrigeradoras Samsung en Panamá</h1><p class="lead">Cada reparación incluye garantía sobre la pieza reemplazada y sobre la mano de obra. El plazo exacto se confirma antes de empezar el trabajo.</p><p>Es una garantía de nuestro servicio técnico independiente, no una garantía de fábrica de Samsung. Si tu refrigeradora está en garantía de fábrica, te lo decimos durante el diagnóstico.</p><h2>Qué cubre</h2><ul class="lista chk"><li><b>Pieza reemplazada:</b> si vuelve a fallar por defecto de la pieza dentro del plazo acordado, la revisamos sin costo adicional de mano de obra.</li><li><b>Mano de obra:</b> si el mismo síntoma reaparece por un error de instalación o ajuste, lo corregimos sin cargo.</li></ul><h2>Qué no cubre</h2><p>Daños nuevos por mal uso, variaciones de voltaje posteriores al servicio o intervención de terceros después de nuestra visita.</p>{faq_html([("¿Cuánto dura la garantía?", "Depende de la pieza y del tipo de reparación; te lo confirmamos por escrito al momento del servicio, antes de que pagues."), ("¿Qué hago si la falla vuelve?", "Escríbenos por WhatsApp con tu nombre y la fecha del servicio anterior; si está dentro del plazo, coordinamos la revisión.")])}</div></section>{cta(msg)}'''
    escribir("garantia.html", f"Garantía | {NOMBRE}", "Garantía sobre la pieza y la mano de obra en cada reparación de refrigeradoras Samsung en Panamá.", c, [bc(("Garantía", None))], "0.5")
    c = f'''{miga(0, ("Nosotros", None))}<section class="sec"><div class="w txt"><h1>Nosotros: especialistas en refrigeradoras Samsung en Panamá</h1><p class="lead">Somos un servicio técnico independiente enfocado en refrigeradoras Samsung.</p><p>Esa especialización nos permite conocer a fondo los modelos que circulan en Panamá, sus fallas más comunes y los repuestos que realmente necesitan. Trabajamos con coordinación directa por WhatsApp, sin intermediarios.</p><h2>Cómo trabajamos</h2><ul class="lista chk"><li><b>Diagnóstico honesto:</b> explicamos la falla antes de reparar.</li><li><b>Mediciones:</b> temperaturas, voltaje, ventiladores y descongelación.</li><li><b>Garantía:</b> en pieza y mano de obra.</li><li><b>Tiempos claros:</b> visitas en 24 a 48 horas en la mayoría de zonas.</li></ul><p class="aviso">No somos Samsung ni servicio técnico autorizado por Samsung. Samsung es una marca de su dueño y se menciona solo para indicar el tipo de equipo que reparamos.</p></div></section>{cta(msg)}'''
    escribir("nosotros.html", f"Nosotros | {NOMBRE}", "Servicio técnico independiente especializado en refrigeradoras Samsung en Ciudad de Panamá.", c, [negocio_ld(), bc(("Nosotros", None))], "0.5")
    c = f'''{miga(0, ("Preguntas frecuentes", None))}<section class="sec"><div class="w txt"><h1>Preguntas frecuentes sobre el servicio técnico de refrigeradoras Samsung en Panamá</h1>{faq_html(FAQ_GENERAL)}</div></section>{cta(msg)}'''
    escribir("preguntas-frecuentes.html", "Preguntas frecuentes | Servicio técnico de refrigeradoras Samsung en Panamá", "Respuestas sobre cobertura, costos, garantía y tiempos del servicio técnico de refrigeradoras Samsung en Panamá.", c, [faq_ld(FAQ_GENERAL), bc(("Preguntas frecuentes", None))], "0.6")
    c = f'''{miga(0, ("Privacidad", None))}<section class="sec"><div class="w txt"><h1>Política de privacidad</h1><p>Cuando nos escribes por WhatsApp o nos llamas usamos tu nombre, tu número y los datos que nos des (dirección, modelo y falla) solo para atender tu solicitud y coordinar la visita.</p><p>No vendemos tus datos. Puedes pedirnos que los corrijamos o los eliminemos escribiéndonos por WhatsApp al {TEL}.</p><p>Este sitio puede usar herramientas de medición (como Google Analytics o Tag Manager).</p></div></section>'''
    escribir("privacidad.html", f"Política de privacidad | {NOMBRE}", "Cómo usamos tus datos cuando nos contactas para un servicio técnico.", c, None, "0.2")
    c = f'''{miga(0, ("Aviso legal", None))}<section class="sec"><div class="w txt"><h1>Aviso legal</h1><p>{NOMBRE} es un servicio técnico independiente. No somos Samsung, ni una empresa afiliada, ni servicio técnico autorizado por Samsung.</p><p>Samsung y los nombres de sus productos son marcas de su dueño y se mencionan únicamente para indicar el tipo de equipos que reparamos.</p><p>La información de este sitio es orientativa. El diagnóstico definitivo y el costo se confirman en la visita.</p></div></section>'''
    escribir("aviso-legal.html", f"Aviso legal | {NOMBRE}", "Aviso legal del servicio técnico independiente de refrigeradoras Samsung en Panamá.", c, None, "0.2")

def mapa_html():
    grupos = [("Tipos de refrigeradora", [(f"tipos-de-refrigeradora/{t[0]}.html", t[1]) for t in TIPOS]), ("Fallas", [(f"fallas/refrigeradora-samsung-{f[0]}.html", f"Refrigeradora {f[1]}") for f in FALLAS]),
              ("Repuestos", [(f"repuestos/{r[0]}.html", r[1]) for r in REPUESTOS]), ("Servicios", [(f"servicios/{k}.html", v[1]) for k, v in SERVICIOS.items()]), ("Zonas", [(f"zonas/{slug(z[0])}.html", z[0]) for z in ZONAS]), ("Blog", [(f"blog/{b[0]}.html", b[1]) for b in BLOG])]
    h = "".join(f'<h2>{esc(g)}</h2><ul class="lista">{"".join(f"<li><a href=\"{u}\">{esc(t)}</a></li>" for u, t in items)}</ul>' for g, items in grupos)
    escribir("mapa-del-sitio.html", f"Mapa del sitio | {NOMBRE}", "Todas las páginas del sitio de servicio técnico de refrigeradoras Samsung en Panamá.", f'{miga(0, ("Mapa del sitio", None))}<section class="sec"><div class="w txt"><h1>Mapa del sitio</h1>{h}</div></section>', [bc(("Mapa del sitio", None))], "0.3")

CSS = open(AQUI / "estilos.css", encoding="utf-8").read() if (AQUI / "estilos.css").exists() else ""
JS = '''(function(){window.dataLayer=window.dataLayer||[];document.addEventListener("click",function(e){var a=e.target.closest('a[href*="wa.me/"],a[href^="tel:"]');if(a){dataLayer.push({event:"whatsapp",ubicacion:a.getAttribute("data-wa")||"enlace",boton:(a.textContent||"").trim().slice(0,60),pagina:location.pathname})}},true);
var b=document.querySelector(".burger"),m=document.querySelector(".mov");if(b&&m){b.addEventListener("click",function(){var o=m.hidden;m.hidden=!o;b.setAttribute("aria-expanded",String(o))})}
var tabs=document.querySelectorAll(".tab");tabs.forEach(function(t){t.addEventListener("click",function(){tabs.forEach(function(x){x.classList.remove("on")});t.classList.add("on");var f=t.getAttribute("data-f");document.querySelectorAll(".dg").forEach(function(c){c.hidden=(f!=="todos"&&c.getAttribute("data-eq")!==f)})})});})();'''

def estaticos():
    (OUT / "css").mkdir(exist_ok=True); (OUT / "js").mkdir(exist_ok=True); (OUT / "images" / "logo").mkdir(parents=True, exist_ok=True)
    (OUT / "css" / "estilos.css").write_text(CSS, encoding="utf-8"); (OUT / "js" / "main.js").write_text(JS, encoding="utf-8")
    (OUT / "images" / "logo" / "favicon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#1428a0"/><g transform="translate(14 14) scale(1.5)" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.2L3 17.8V21h3.2l6.3-6.3a4 4 0 0 0 5.2-5.4l-2.5 2.5-2.4-.6-.6-2.4z"/></g></svg>', encoding="utf-8")
    from PIL import Image, ImageDraw, ImageFont
    im = Image.new("RGB", (1200, 630)); d = ImageDraw.Draw(im)
    for y in range(630): d.line([(0, y), (1200, y)], fill=(int(10 + 10 * y / 630), int(20 + 20 * y / 630), int(96 + 64 * y / 630)))
    fb = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; fr = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    d.rounded_rectangle((820, 90, 1060, 540), 24, fill=(238, 241, 249)); d.rounded_rectangle((830, 100, 1050, 300), 16, fill=(214, 220, 234)); d.rounded_rectangle((830, 310, 1050, 530), 16, fill=(214, 220, 234))
    d.text((70, 140), "Servicio técnico de", font=ImageFont.truetype(fb, 52), fill="white"); d.text((70, 215), "refrigeradoras", font=ImageFont.truetype(fb, 84), fill="white"); d.text((70, 315), "Samsung en Panamá", font=ImageFont.truetype(fb, 62), fill="white")
    d.text((70, 430), "Side by Side · French Door · Dispensador y hielo", font=ImageFont.truetype(fr, 30), fill=(200, 214, 255)); d.text((70, 500), f"WhatsApp {TEL}", font=ImageFont.truetype(fb, 38), fill="white")
    im.save(OUT / "images" / "og.jpg", quality=88)

def indices():
    urls = "".join(f"<url><loc>{DOMINIO}/{r}</loc><lastmod>2026-10-20</lastmod><priority>{p[0]}</priority></url>\n" for r, p in sorted(PAGINAS.items(), key=lambda x: -float(x[1][0])))
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nUser-agent: GPTBot\nAllow: /\nUser-agent: ClaudeBot\nAllow: /\nUser-agent: PerplexityBot\nAllow: /\nUser-agent: Google-Extended\nAllow: /\n\nSitemap: {DOMINIO}/sitemap.xml\n", encoding="utf-8")
    t = f"# {NOMBRE}\n\n> Servicio técnico independiente de refrigeradoras (neveras) Samsung a domicilio en Ciudad de Panamá. WhatsApp {TEL}. {HORARIO}.\n\n## Fallas\n" + "".join(f"- [Refrigeradora Samsung {f[1]}]({DOMINIO}/fallas/refrigeradora-samsung-{f[0]}.html)\n" for f in FALLAS)
    t += "\n## Tipos\n" + "".join(f"- [{x[1]}]({DOMINIO}/tipos-de-refrigeradora/{x[0]}.html)\n" for x in TIPOS) + "\n## Zonas\n" + "".join(f"- [{z[0]}]({DOMINIO}/zonas/{slug(z[0])}.html)\n" for z in ZONAS)
    (OUT / "llms.txt").write_text(t, encoding="utf-8")

def main():
    for d in ["tipos-de-refrigeradora", "fallas", "repuestos", "servicios", "zonas", "blog", "images", "css", "js"]: shutil.rmtree(OUT / d, ignore_errors=True)
    estaticos(); pagina_inicio(); paginas_tipos(); paginas_fallas(); paginas_repuestos(); paginas_servicios(); paginas_zonas(); paginas_blog(); pagina_diagnostico(); paginas_info(); mapa_html(); indices()
    z = OUT.parent / "entrega" / "refrigeradoras-samsung-panama.zip"; z.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in OUT.rglob("*"):
            if p.is_file() and "_fuente" not in p.parts and "__pycache__" not in p.parts: zf.write(p, p.relative_to(OUT).as_posix())
    print(f"OK: {len(PAGINAS)} páginas → {z.name}")
main()
