# -*- coding: utf-8 -*-
"""Genera servicio-tecnico-guayaquil.com. Uso: python3 gye/gye_build.py /ruta/salida"""
import sys, os, re, json, html, shutil, pathlib, hashlib, collections, urllib.parse
AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI)); sys.path.insert(0, str(AQUI.parent))
from datos_equipos1 import REFRIGERADORAS, LAVADORAS, SECADORAS, COCINAS
from datos_equipos2 import AIRES, LAVAVAJILLAS, MICROONDAS
from datos_sitio import SITE, MARCAS, ZONAS, GUIAS
from datos_extra import EXTRA
from cst_datos import M as MARCA_DATOS

OUT = pathlib.Path(sys.argv[1]); INV = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "/tmp/gye/inv.json")
EQS = [REFRIGERADORAS, LAVADORAS, SECADORAS, COCINAS, AIRES, LAVAVAJILLAS, MICROONDAS]
EQ = {e["slug"]: e for e in EQS}
DOM = SITE["dom"]; NOMBRE = SITE["nombre"]; TEL = SITE["tel"]; TELW = SITE["telw"]; HOY = SITE["hoy"]
esc = lambda t: html.escape(str(t), quote=True)
def wa(txt): return f"https://wa.me/{TELW}?text=" + urllib.parse.quote(txt)
def cap(t): return t[:1].upper() + t[1:]
def bajar(t): return t[:1].lower() + t[1:]
def slugify(t): return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")

# ------------------------------------------------------------------ imágenes (siempre completas, nunca recortadas)
INVENT = json.load(open(INV))
POOL = collections.defaultdict(list)
for it in INVENT:
    POOL[it["cat"]].append(it)
CATS = {"refrigeradoras": ["refrigeradoras"], "lavadoras": ["lavadoras", "centro-lavado"], "secadoras": ["secadoras", "centro-lavado"], "cocinas": ["cocinas"],
        "aires": ["aires"], "lavavajillas": ["lavavajillas"], "microondas": ["microondas"], "personas": ["personas"]}
MARCA_NOM = {"samsung": "Samsung", "lg": "LG", "whirlpool": "Whirlpool", "mabe": "Mabe", "frigidaire": "Frigidaire", "electrolux": "Electrolux", "general-electric": "General Electric", "haceb": "Haceb", "kitchenaid": "KitchenAid"}
COPIADAS = {}
USO = collections.Counter()
def _alt(it, cat):
    b = MARCA_NOM.get(it["brand"], "")
    n = it["name"].lower()
    if cat == "personas":
        if re.search(r"asesora|recep|mostrador|agente", n): return "Asesora de atención al cliente coordinando una visita de servicio técnico"
        if re.search(r"taller|equipo-de", n): return "Equipo de técnicos en el taller de servicio"
        if re.search(r"puerta|llegada|saluda|domicilio", n): return "Técnico llegando a un domicilio para una visita de servicio técnico"
        return "Técnico de electrodomésticos atendiendo a un cliente en su casa"
    nombre = {"refrigeradoras": "Refrigeradora", "lavadoras": "Lavadora", "secadoras": "Secadora", "cocinas": "Cocina u horno", "aires": "Aire acondicionado", "lavavajillas": "Lavavajillas", "microondas": "Microondas"}[cat]
    if "centro-lavado" in n or "torre" in n or "washtower" in n: nombre = "Centro de lavado"
    return f"{nombre} {b} que reparamos en Guayaquil".strip()
def foto(cat, clave, usadas, tipo=None):
    """Elige una foto de la categoría, sin repetir dentro de la página. Devuelve dict con ruta y medidas."""
    cands = []
    for c in CATS[cat]: cands += POOL[c]
    if not cands: return None
    orden = sorted(cands, key=lambda it: (USO[it["f"]], hashlib.md5((clave + it["f"]).encode()).hexdigest()))
    for it in orden:
        if it["f"] in usadas: continue
        usadas.add(it["f"]); USO[it["f"]] += 1
        if it["f"] not in COPIADAS:
            rel = f"/img/{cat if cat != 'personas' else 'tecnicos'}/{it['brand']}-{slugify(it['name'][:-5])[:60]}.webp"
            dest = OUT / rel.lstrip("/"); dest.parent.mkdir(parents=True, exist_ok=True); shutil.copy(it["f"], dest)
            COPIADAS[it["f"]] = rel
        rel = COPIADAS[it["f"]]
        return dict(src=rel, alt=_alt(it, cat), w=it["w"], h=it["h"], persona=(cat == "personas"))
    return None
def figura(f, eager=False, cls=""):
    if not f: return ""
    k = "fig persona" if f["persona"] else "fig prod"
    return (f'<figure class="{k} {cls}"><img src="{f["src"]}" alt="{esc(f["alt"])}" width="{f["w"]}" height="{f["h"]}"'
            + (' fetchpriority="high" decoding="async"' if eager else ' loading="lazy" decoding="async"') + '></figure>')

# ------------------------------------------------------------------ CSS
CSS = """
:root{--c:#0a4d7c;--c2:#073556;--a:#f26b1d;--ab:#fff;--soft:#e7f0f7;--bg:#f4f8fb;--w:#fff;--t:#10243a;--m:#546a80;--r:16px;--sh:0 6px 24px rgba(10,77,124,.10)}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;font:16px/1.7 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:var(--t);background:var(--bg)}
img{max-width:100%;height:auto;display:block}a{color:var(--c)}h1,h2,h3{line-height:1.22;margin:0 0 .6rem;letter-spacing:-.01em}h1{font-size:clamp(1.7rem,4.4vw,2.7rem)}h2{font-size:clamp(1.3rem,3vw,1.85rem)}h3{font-size:1.1rem}p{margin:0 0 1rem}ul,ol{padding-left:1.2rem}li{margin:.25rem 0}
.w{max-width:1120px;margin:0 auto;padding:0 16px}.skip{position:absolute;left:-999px;top:0;background:#fff;color:#000;padding:10px 14px;z-index:99}.skip:focus{left:8px;top:8px}
.top{background:var(--c2);color:#fff;font-size:.85rem}.top .w{display:flex;gap:16px;justify-content:space-between;padding:7px 16px;flex-wrap:wrap}.top a{color:#fff;text-decoration:none;font-weight:700}
header.h{background:var(--w);position:sticky;top:0;z-index:20;box-shadow:0 1px 0 #dce7f0}.h .w{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:10px 16px}
.logo{display:flex;flex-direction:column;text-decoration:none;color:var(--c);font-weight:800;line-height:1.15}.logo small{font-weight:600;color:var(--m);font-size:.75rem}
.btn{display:inline-block;background:var(--a);color:var(--ab);text-decoration:none;font-weight:700;padding:12px 20px;border-radius:999px;border:0;cursor:pointer}.btn.o{background:transparent;color:#fff;border:2px solid #fff}.btn.s{padding:8px 16px;font-size:.9rem}.btn.c{background:var(--c)}
.chips{background:var(--w);border-bottom:1px solid #dce7f0;overflow-x:auto;white-space:nowrap}.chips .w{display:flex;gap:8px;padding:8px 16px}.chips a{padding:7px 14px;border-radius:999px;background:var(--soft);text-decoration:none;font-weight:600;font-size:.9rem;color:var(--c)}
.hero{background:linear-gradient(135deg,var(--c),var(--c2));color:#fff;padding:34px 0}.hero .w{display:grid;gap:24px;align-items:center}@media(min-width:860px){.hero .w{grid-template-columns:1.05fr .95fr}}
.hero p{opacity:.95}.bd{display:inline-block;background:rgba(255,255,255,.16);padding:4px 12px;border-radius:999px;font-size:.85rem;margin-bottom:10px;font-weight:600}.hero .btns{display:flex;gap:10px;flex-wrap:wrap;margin-top:6px}
.fig{margin:0}.fig img{display:block;width:100%;height:auto;border-radius:14px}
.fig.prod{background:#fff;border-radius:var(--r);padding:16px;box-shadow:var(--sh)}.fig.prod img{width:auto;max-width:100%;max-height:420px;margin:0 auto;object-fit:contain;border-radius:0}
.fig.persona img{width:auto;max-width:100%;max-height:520px;margin:0 auto;object-fit:contain;box-shadow:var(--sh)}
section.s{padding:34px 0}section.s.alt{background:var(--w)}.lead{color:var(--m);max-width:780px}
.bc{font-size:.85rem;color:var(--m);padding:12px 0}.bc a{color:var(--m)}
.g{display:grid;gap:16px}@media(min-width:700px){.g.c2{grid-template-columns:1fr 1fr}.g.c3{grid-template-columns:repeat(3,1fr)}}@media(min-width:1000px){.g.c4{grid-template-columns:repeat(4,1fr)}.g.c7{grid-template-columns:repeat(4,1fr)}}
.card{background:var(--w);border-radius:var(--r);padding:18px;box-shadow:var(--sh)}.card.l{text-decoration:none;color:inherit;display:block;transition:.15s}.card.l:hover{transform:translateY(-3px)}.card .t{font-weight:800;color:var(--c);display:block;margin-bottom:4px}
.tile{display:flex;flex-direction:column;background:var(--w);border-radius:var(--r);overflow:hidden;box-shadow:var(--sh);text-decoration:none;color:var(--t);border:2px solid transparent;transition:.15s}.tile:hover{transform:translateY(-3px);border-color:var(--a)}
.tile .ti{height:190px;background:#fff;display:grid;place-items:center;padding:12px}.tile .ti img{max-height:165px;max-width:100%;width:auto;height:auto;object-fit:contain}.tile b{padding:12px 16px 0;color:var(--c);font-size:1.05rem}.tile small{padding:2px 16px 14px;color:var(--m)}
.stp{display:flex;gap:8px;flex-wrap:wrap;list-style:none;padding:0;margin:0 0 16px}.stp li{display:flex;align-items:center;gap:8px;background:var(--w);border-radius:999px;padding:6px 14px 6px 8px;font-size:.88rem;font-weight:600;color:var(--m);margin:0}.stp li b{display:inline-grid;place-items:center;width:24px;height:24px;border-radius:50%;background:var(--soft);color:var(--c)}.stp li.on{color:var(--c);box-shadow:0 0 0 2px var(--c)}.stp li.on b{background:var(--c);color:#fff}
.svc{display:grid;gap:14px}@media(min-width:800px){.svc{grid-template-columns:repeat(3,1fr)}}.svc .card h3{color:var(--c)}
.rr{background:var(--soft);border-left:5px solid var(--a);padding:16px 18px;border-radius:12px;margin:0 0 18px}.rr b{display:block;margin-bottom:4px;color:var(--c)}
.call{background:#fff4ec;border-left:5px solid var(--a);padding:16px 18px;border-radius:12px;margin:0 0 16px}
.tb{width:100%;border-collapse:collapse;background:var(--w);border-radius:var(--r);overflow:hidden;box-shadow:var(--sh)}.tb th,.tb td{padding:12px 14px;text-align:left;vertical-align:top;border-bottom:1px solid #e3ecf3;font-size:.95rem}.tb th{background:var(--soft);color:var(--c)}
@media(max-width:699px){.tb thead{display:none}.tb tr{display:block;border-bottom:8px solid var(--bg)}.tb td{display:block;border:0;padding:6px 14px}.tb td:before{content:attr(data-l);display:block;font-size:.72rem;font-weight:800;color:var(--c);text-transform:uppercase}}
.two{display:grid;gap:22px;align-items:start}@media(min-width:860px){.two{grid-template-columns:1.1fr .9fr}}
details{background:var(--w);border-radius:12px;padding:14px 16px;margin-bottom:10px;box-shadow:var(--sh)}summary{cursor:pointer;font-weight:700}details[open] summary{margin-bottom:8px}
.pill{display:inline-block;padding:3px 10px;border-radius:999px;background:var(--soft);color:var(--c);font-weight:600;font-size:.85rem;margin:3px 4px 3px 0}
.anc{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 18px}.anc a{padding:8px 14px;background:var(--w);border-radius:999px;box-shadow:var(--sh);text-decoration:none;font-weight:600;font-size:.9rem}
.marcas{display:grid;gap:14px;grid-template-columns:repeat(auto-fill,minmax(150px,1fr))}.marcas .mk{background:#fff;border-radius:var(--r);box-shadow:var(--sh);padding:18px 12px;display:grid;place-items:center;height:92px}.marcas img{max-height:42px;max-width:130px;width:auto;height:auto;object-fit:contain}
.upd{font-size:.85rem;color:var(--m);margin:6px 0 28px}
.band{background:linear-gradient(135deg,var(--c),var(--c2));color:#fff;padding:40px 0;text-align:center}.band p{max-width:620px;margin:0 auto 16px}
footer{background:var(--c2);color:#cfdeea;padding:34px 0 90px;font-size:.92rem}footer a{color:#fff}footer h3{color:#fff}footer ul{list-style:none;padding:0;margin:0}footer li{margin:5px 0}
.fb{position:fixed;left:0;right:0;bottom:0;z-index:30;display:flex;gap:8px;padding:8px 10px;background:#fff;box-shadow:0 -4px 20px rgba(0,0,0,.12)}.fb a{flex:1;text-align:center;padding:12px;border-radius:12px;font-weight:800;text-decoration:none;color:#fff;background:var(--c)}.fb a.wa{background:#1fa855}
@media(min-width:900px){.fb{display:none}}
dl.pz dt{font-weight:800;color:var(--c)}dl.pz dd{margin:0 0 10px;padding-bottom:10px;border-bottom:1px solid #e3ecf3}
"""
CSSV = hashlib.md5(CSS.encode()).hexdigest()[:10]

# ------------------------------------------------------------------ piezas de página
paginas = []   # (path, prio, imgs)
def sec(t, body, alt=False, lead=None, id=None):
    return f'<section class="s{" alt" if alt else ""}"{f" id={chr(34)}{id}{chr(34)}" if id else ""}><div class="w"><h2>{t}</h2>' + (f'<p class="lead">{lead}</p>' if lead else "") + body + '</div></section>'
def tabla(cab, filas):
    return '<table class="tb"><thead><tr>' + "".join(f"<th>{esc(c)}</th>" for c in cab) + "</tr></thead><tbody>" + "".join("<tr>" + "".join(f'<td data-l="{esc(cab[i])}">{c}</td>' for i, c in enumerate(f)) + "</tr>" for f in filas) + "</tbody></table>"
def faq_html(fs): return "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in fs)
def faq_ld(fs): return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in fs]}
def stepper(n): return '<ol class="stp">' + "".join(f'<li class="{"on" if i == n else ""}"><b>{i}</b>{t}</li>' for i, t in ((1, "Elige tu equipo"), (2, "Elige lo que necesitas"), (3, "Pide la visita"))) + "</ol>"
def cta_band(texto, msg):
    return f'<section class="band"><div class="w"><h2>{texto}</h2><p>Escríbenos con el equipo, la marca, el modelo y lo que notas, y coordinamos la visita en Guayaquil.</p><a class="btn" href="{wa(msg)}" target="_blank" rel="noopener">Escribir por WhatsApp</a> <a class="btn o" href="tel:+{TELW}">Llamar {TEL}</a></div></section>'
def fit(t, n=62):
    if len(t) <= n: return t
    p = t.split(" | ")
    while len(" | ".join(p)) > n and len(p) > 1: p.pop()
    t = " | ".join(p)
    if len(t) > n: t = re.sub(r"[\s,:;\-]+(?:de|en|y|a|la|el|los|las|con|para|del|que|o|u|al)?$", "", t[:n].rsplit(" ", 1)[0])
    return t
def fitdesc(d, extra=" Atención a domicilio en Guayaquil y por WhatsApp."):
    if len(d) < 118 and len(d) + len(extra) <= 158: d += extra
    if len(d) > 158: d = d[:157].rsplit(" ", 1)[0].rstrip(" ,.;") + "…"
    return d

NAV = [("Inicio", "/")] + [(e["corto"], f"/{e['slug']}/") for e in EQS] + [("Zonas", "/servicio-tecnico-cerca-de-mi/"), ("Marcas", "/marcas-que-reparamos/"), ("Guías", "/guias/"), ("Contacto", "/contacto/")]
def chips(): return '<nav class="chips" aria-label="Menú"><div class="w">' + "".join(f'<a href="{u}">{esc(t)}</a>' for t, u in NAV) + "</div></nav>"
def pie():
    c1 = '<div><h3>Servicios</h3><ul>' + "".join(f'<li><a href="/{e["slug"]}/">{esc(e["corto"])}</a></li>' for e in EQS) + "</ul></div>"
    c2 = '<div><h3>Zonas</h3><ul>' + "".join(f'<li><a href="/{z["slug"]}/">{esc(z["nombre"])}</a></li>' for z in ZONAS) + "</ul></div>"
    c3 = ('<div><h3>Información</h3><ul><li><a href="/telefono-servicio-tecnico-guayaquil/">Teléfono de servicio técnico</a></li><li><a href="/servicio-tecnico-a-domicilio/">Servicio técnico a domicilio</a></li><li><a href="/cuanto-cuesta-reparar-electrodomesticos/">Cuánto cuesta reparar</a></li>'
          '<li><a href="/garantia-de-la-reparacion/">Garantía de la reparación</a></li><li><a href="/repuestos-para-electrodomesticos/">Repuestos</a></li><li><a href="/preguntas-frecuentes/">Preguntas frecuentes</a></li><li><a href="/guias/">Guías</a></li></ul></div>')
    c4 = (f'<div><h3>{NOMBRE}</h3><p>{TEL}</p><ul><li><a href="/quienes-somos/">Quiénes somos</a></li><li><a href="/contacto/">Contacto</a></li><li><a href="/politica-de-privacidad/">Política de privacidad</a></li><li><a href="/terminos-y-condiciones/">Términos y condiciones</a></li></ul>'
          '<p><small>Servicio técnico independiente. Los nombres de marcas pertenecen a sus propietarios y se usan solo para indicar los equipos que reparamos.</small></p></div>')
    return (f'<footer><div class="w"><div class="g c4">{c1}{c2}{c3}{c4}</div></div></footer>'
            f'<div class="fb"><a href="tel:+{TELW}">Llamar</a><a class="wa" href="{wa("Hola, necesito servicio técnico en Guayaquil")}" target="_blank" rel="noopener">WhatsApp</a></div>')

LB = {"@type": "ProfessionalService", "@id": DOM + "/#negocio", "name": NOMBRE, "url": DOM + "/", "telephone": "+" + TELW, "inLanguage": SITE["locale"],
      "description": "Servicio técnico a domicilio en Guayaquil: reparación, mantenimiento e instalación de refrigeradoras, lavadoras, secadoras, cocinas y hornos, aires acondicionados, lavavajillas y microondas.",
      "knowsAbout": [f"Reparación de {e['p']}" for e in EQS] + [f"Mantenimiento de {e['p']}" for e in EQS[:3]] + ["Instalación de electrodomésticos"],
      "areaServed": [{"@type": "City", "name": c} for c in SITE["areas"]],
      "address": {"@type": "PostalAddress", "addressLocality": SITE["ciudad"], "addressRegion": SITE["provincia"], "addressCountry": SITE["cc"]},
      "contactPoint": [{"@type": "ContactPoint", "telephone": "+" + TELW, "contactType": "customer service", "availableLanguage": ["es"], "areaServed": SITE["cc"]}]}

def pagina(path, title, desc, h1, cuerpo, crumbs=None, hero=None, ld=None, bd=None, lead=None, noindex=False, prio="0.7", btns=None, extra_head="", imgs=None):
    title = fit(title); desc = fitdesc(desc)
    url = DOM + path
    graf = [LB, {"@type": "WebSite", "@id": DOM + "/#sitio", "url": DOM + "/", "name": NOMBRE, "inLanguage": SITE["locale"], "publisher": {"@id": DOM + "/#negocio"}}]
    wp = {"@type": "CollectionPage" if re.search(r"/(guias|marcas-que-reparamos|servicio-tecnico-cerca-de-mi)/$", path) or path.count("/") == 2 and any(path == f"/{e['slug']}/" for e in EQS) else "WebPage",
          "@id": url + "#pagina", "url": url, "name": title, "description": desc, "isPartOf": {"@id": DOM + "/#sitio"}, "about": {"@id": DOM + "/#negocio"}, "inLanguage": SITE["locale"], "dateModified": HOY, "datePublished": HOY}
    if hero: wp["primaryImageOfPage"] = {"@type": "ImageObject", "url": DOM + hero["src"], "caption": hero["alt"], "width": hero["w"], "height": hero["h"]}
    graf.append(wp)
    if crumbs: graf.append({"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": DOM + u} for i, (n, u) in enumerate(crumbs)]})
    for x in (ld or []):
        if x.get("@type") == "Article":
            x["mainEntityOfPage"] = {"@id": url + "#pagina"}
            if hero: x["image"] = [DOM + hero["src"]]
        graf.append(x)
    bc = ('<div class="w bc">' + " › ".join((f'<a href="{u}">{esc(n)}</a>' if i < len(crumbs) - 1 else esc(n)) for i, (n, u) in enumerate(crumbs)) + "</div>") if crumbs and len(crumbs) > 1 else ""
    btn1 = btns or (f"Hola, necesito servicio técnico en Guayaquil", "Escribir por WhatsApp")
    heroh = (f'<section class="hero"><div class="w"><div><span class="bd">{esc(bd or NOMBRE)}</span><h1>{esc(h1)}</h1><p>{lead or esc(desc)}</p>'
             f'<div class="btns"><a class="btn" href="{wa(btn1[0])}" target="_blank" rel="noopener">{btn1[1]}</a><a class="btn o" href="tel:+{TELW}">Llamar {TEL}</a></div></div>{figura(hero, True)}</div></section>')
    gsc = f'<meta name="google-site-verification" content="{SITE["gsc"]}">' if path == "/" else ""
    robots = "noindex,follow" if noindex else "index,follow,max-image-preview:large,max-snippet:-1"
    ogimg = (f'<meta property="og:image" content="{DOM}{hero["src"]}"><meta property="og:image:alt" content="{esc(hero["alt"])}"><meta name="twitter:image" content="{DOM}{hero["src"]}"><link rel="preload" as="image" href="{hero["src"]}" fetchpriority="high">' if hero else "")
    h = (f'<!doctype html><html lang="{SITE["locale"]}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title>'
         f'<meta name="description" content="{esc(desc)}"><link rel="canonical" href="{url}"><link rel="alternate" hreflang="{SITE["locale"]}" href="{url}"><link rel="alternate" hreflang="x-default" href="{url}">'
         f'<meta name="geo.region" content="EC-G"><meta name="geo.placename" content="Guayaquil"><meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#0a4d7c"><meta name="robots" content="{robots}">{gsc}'
         f'<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta property="og:locale" content="es_EC"><meta property="og:site_name" content="{NOMBRE}">'
         f'<meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(desc)}">{ogimg}{extra_head}'
         f'<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/site.css?v={CSSV}">'
         f'<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graf}, ensure_ascii=False)}</script></head><body><a class="skip" href="#contenido">Saltar al contenido</a>'
         f'<div class="top"><div class="w"><span>Atención a domicilio en Guayaquil · {TEL}</span><a href="{wa("Hola, necesito servicio técnico en Guayaquil")}" target="_blank" rel="noopener">WhatsApp</a></div></div>'
         f'<header class="h"><div class="w"><a class="logo" href="/">Servicio Técnico<small>Guayaquil · Electrodomésticos</small></a><a class="btn s" href="{wa("Hola, necesito servicio técnico en Guayaquil")}" target="_blank" rel="noopener">Pedir visita</a></div></header>'
         + chips() + '<main id="contenido">' + heroh + bc + cuerpo
         + ('<div class="w"><p class="upd">Actualizado el ' + SITE["hoy_txt"] + ' · Información orientativa; el diagnóstico final se confirma con pruebas en el equipo.</p></div>' if not noindex else "")
         + "</main>" + pie() + "</body></html>")
    h = re.sub(r"\b([Aa]) el\b", lambda m: m.group(1) + "l", h)
    h = re.sub(r"\b([Dd]e) el\b", lambda m: m.group(1) + "l", h)
    f = OUT / path.lstrip("/") / "index.html" if path != "/" else OUT / "index.html"
    f.parent.mkdir(parents=True, exist_ok=True); f.write_text(h, encoding="utf-8")
    if not noindex: paginas.append((path, prio, ([hero["src"]] if hero else []) + (imgs or [])))

# ------------------------------------------------------------------ páginas de electrodoméstico
def pls(e): return e["p"]
def build_equipo(e):
    s, p, sl = e["s"], e["p"], e["slug"]
    U = set()
    hero = foto(e["foto"], sl + "hero", U)
    crumb0 = ("Inicio", "/"); cr = [crumb0, (f"Servicio técnico de {p}", f"/{sl}/")]
    # --- hub
    tarj = "".join(f'<a class="card l" href="/{sl}/{k}/"><span class="t">{t}</span>{d}</a>' for k, t, d in (
        ("reparacion", f"Reparación de {p}", f"Diagnóstico y reparación a domicilio: {bajar(e['fallas'][0]['termino'])}, {bajar(e['fallas'][1]['termino'])} y más."),
        ("mantenimiento", f"Mantenimiento de {p}", "Limpieza, revisión y cuidados que evitan averías y bajan el consumo de energía."),
        ("instalacion", f"Instalación de {p}", "Instalación segura y probada, paso a paso.")))
    fallas = "".join(f'<a class="card l" href="/{sl}/{f["slug"]}/"><span class="t">{esc(cap(f["termino"]))}</span>{esc(f["sintoma"])}</a>' for f in e["fallas"])
    urg = "".join(f"<li><b>{esc(cap(f['termino']))}:</b> {esc(f['llamar'])}</li>" for f in e["fallas"])
    img2 = figura(foto(e["foto"], sl + "h2", U))
    img3 = figura(foto("personas", sl + "h3", U))
    marcas_tag = "".join(f'<span class="pill">{m}</span>' for m in MARCAS)
    zonas_l = "".join(f'<a class="card l" href="/{z["slug"]}/"><span class="t">{esc(z["nombre"])}</span>{esc(z["barrios"])}</a>' for z in ZONAS[:4])
    cuerpo = (sec(f"¿Qué necesitas para tu {s}?", stepper(2) + f'<div class="svc">{tarj}</div>', id="servicios", lead=f"Elige reparación, mantenimiento o instalación de {p}. Cada servicio tiene su propia guía con pasos, tiempos y consejos para Guayaquil.")
              + sec(f"¿Qué le pasa a tu {s}?", f'<div class="g c2">{fallas}</div>', alt=True, id="fallas", lead=f"Toca lo que notas en tu {s}. Te explicamos las causas más probables, qué puedes probar tú y cuándo conviene llamar.")
              + sec(f"Cómo funciona {e['la']} {s} y por qué falla", f'<div class="two"><div><p>{esc(e["intro"][0])}</p><p>{esc(e["funciona"])}</p><p><b>Tipos que atendemos:</b> {esc(e["tipos"])}.</p></div>{img2}</div>')
              + sec(f"¿Reparar o cambiar {e['la']} {s}?", f'<p>{cap(e["la"])} {s} dura en promedio <b>{EXTRA[sl]["vida"]}</b> con buen mantenimiento. Antes de decidir, revisamos el equipo y te damos el valor por escrito.</p><div class="two"><div><h3>Casi siempre conviene reparar si…</h3><ul>' + "".join(f"<li>{esc(x)}</li>" for x in EXTRA[sl]["cuando_reparar"]) + '</ul></div><div><h3>Conviene evaluar el cambio si…</h3><ul>' + "".join(f"<li>{esc(x)}</li>" for x in EXTRA[sl]["cuando_cambiar"]) + '</ul></div></div>')
              + sec(f"Cuándo llamar de inmediato por tu {s}", f"<ul>{urg}</ul>", alt=True)
              + sec(f"Servicio técnico de {p} en Guayaquil", f'<div class="two"><div><p>{esc(e["intro"][1])}</p><p><b>Marcas que reparamos:</b></p><p>{marcas_tag}</p><p>Si tu modelo es poco común, mándanos una foto de la etiqueta por WhatsApp y te confirmamos.</p></div>{img3}</div>')
              + sec(f"Preguntas frecuentes sobre {p}", faq_html(e["faq"]), alt=True)
              + sec(f"Guías útiles para tu {s}", '<div class="g c2">' + "".join(f'<a class="card l" href="/guias/{g["slug"]}/"><span class="t">{esc(g["titulo"])}</span>{esc(g["desc"])}</a>' for g in GUIAS) + "</div>", alt=True)
              + sec(f"Atendemos {p} en toda la ciudad", f'<div class="g c2">{zonas_l}</div><p style="margin-top:14px"><a href="/servicio-tecnico-cerca-de-mi/">Ver todas las zonas de Guayaquil</a></p>')
              + cta_band(f"¿Tu {s} necesita revisión?", f"Hola, necesito servicio técnico para mi {s} en Guayaquil"))
    pagina(f"/{sl}/", f"Servicio técnico de {p} en Guayaquil", f"Servicio técnico de {p} en Guayaquil: reparación, mantenimiento e instalación a domicilio para {e['tipos']}. Diagnóstico claro y atención por WhatsApp.",
           f"Servicio técnico de {p} en Guayaquil", cuerpo, cr, hero, [faq_ld(e["faq"]), {"@type": "Service", "name": f"Servicio técnico de {p}", "serviceType": f"Reparación, mantenimiento e instalación de {p}", "provider": {"@id": DOM + "/#negocio"}, "areaServed": {"@type": "City", "name": "Guayaquil"}}],
           bd=f"{e['corto']} · Guayaquil", lead=f"Reparamos, damos mantenimiento e instalamos {p} en tu casa. Elige lo que necesitas y te guiamos paso a paso.", btns=(f"Hola, necesito servicio técnico para mi {s} en Guayaquil", "Escribir por WhatsApp"), prio="0.9")
    # --- reparación
    U = set(); hero = foto(e["foto"], sl + "rep", U)
    lista = "".join(f'<a class="card l" href="/{sl}/{f["slug"]}/"><span class="t">{esc(cap(f["termino"]))}</span>{esc(f["sintoma"])}</a>' for f in e["fallas"])
    pasos = ["Nos escribes con la marca, el modelo y lo que notas.", f"Coordinamos el día y la franja de la visita en tu zona de Guayaquil.", f"Revisamos tu {s} en casa: " + "; ".join(bajar(r.rstrip('.')) for r in e["fallas"][0]["revisa"][:2]) + ".", "Te explicamos la causa y el valor por escrito antes de reparar.", "Solo reparamos si tú lo apruebas, y probamos el equipo contigo."]
    comunes = []
    for f in e["fallas"]:
        for c, ex in f["causas"][:2]: comunes.append((c, ex))
    vistos = set(); causas_tb = []
    for c, ex in comunes:
        if c not in vistos: vistos.add(c); causas_tb.append((f"<b>{esc(c)}</b>", esc(ex)))
    cuerpo = (sec(f"Qué reparamos en {p}", f'<div class="g c2">{lista}</div>', lead=f"Estas son las fallas que más vemos en {p} en Guayaquil. Entra a la tuya para ver causas, pruebas y cuándo llamar.")
              + sec("Cómo es una visita de reparación", "<ol>" + "".join(f"<li>{esc(x)}</li>" for x in pasos) + "</ol>", alt=True)
              + sec(f"Las piezas y causas más comunes en {p}", tabla(["Pieza o causa", "Qué provoca"], causas_tb[:8]), lead=f"Según el tipo de falla, estas son las piezas que revisamos primero en {p}.")
              + sec(f"Reparar o cambiar {e['la']} {s}", f"<p>No siempre conviene reparar. Antes de decidir, revisamos tu {s}, te damos el valor por escrito y te decimos con honestidad si el equipo vale la pena arreglarlo. Si la reparación se acerca a la mitad del precio de uno nuevo y el equipo ya tiene muchos años, conviene evaluar el cambio. Lo explicamos con más detalle en la <a href=\"/guias/reparar-o-cambiar-tu-electrodomestico/\">guía para decidir entre reparar o cambiar</a>.</p>", alt=True)
              + sec(f"Otros servicios para {e['la']} {s}", f'<div class="g c2"><a class="card l" href="/{sl}/mantenimiento/"><span class="t">Mantenimiento de {p}</span>Evita la próxima avería con un plan de limpieza y revisión.</a><a class="card l" href="/{sl}/instalacion/"><span class="t">Instalación de {p}</span>Instalación segura, nivelada y probada.</a></div>')
              + sec(f"Preguntas sobre la reparación de {p}", faq_html(e["faq"][:3]), alt=True)
              + cta_band(f"Pide la revisión de tu {s}", f"Hola, necesito reparar mi {s} en Guayaquil"))
    pagina(f"/{sl}/reparacion/", f"Reparación de {p} en Guayaquil | A domicilio", f"Reparación de {p} a domicilio en Guayaquil: fallas frecuentes, causas, piezas y cómo es la visita. Valor por escrito antes de reparar.",
           f"Reparación de {p} en Guayaquil", cuerpo, cr + [("Reparación", f"/{sl}/reparacion/")], hero, [faq_ld(e["faq"][:3]), {"@type": "Service", "name": f"Reparación de {p}", "provider": {"@id": DOM + "/#negocio"}, "areaServed": {"@type": "City", "name": "Guayaquil"}}],
           bd=f"Reparación · {e['corto']}", lead=f"Diagnóstico y reparación de {p} a domicilio, con el valor por escrito antes de empezar.", btns=(f"Hola, necesito reparar mi {s} en Guayaquil", "Pedir reparación"), prio="0.8")
    # --- mantenimiento
    m = e["mant"]; U = set(); hero = foto(e["foto"], sl + "man", U); img = figura(foto("personas", sl + "manp", U))
    incl = "".join(f"<li>{esc(t[0])} ({esc(bajar(t[1]))}).</li>" for t in m["tabla"])
    cuerpo = (sec(f"Por qué dar mantenimiento a {e['la']} {s}", f'<div class="two"><div><p>{esc(m["intro"])}</p><p>{esc(m["gye"])}</p></div>{img}</div>')
              + sec("Plan de mantenimiento recomendado", tabla(["Tarea", "Cada cuánto", "Por qué importa"], [(f"<b>{esc(a)}</b>", esc(b), esc(c)) for a, b, c in m["tabla"]]), alt=True)
              + sec("Señales de que toca mantenimiento", "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in m["senales"]) + "</ul>")
              + sec(f"Cómo hacer el mantenimiento básico de {e['la']} {s} paso a paso", "<ol>" + "".join(f"<li>{esc(x)}</li>" for x in EXTRA[sl]["diy"]) + "</ol><p>Estos pasos cubren lo básico. Para una revisión completa (presiones, voltaje, componentes internos) conviene la visita de un técnico.</p>")
              + sec(f"Qué no debes hacer con {e['la']} {s}", "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in EXTRA[sl]["nohacer"]) + "</ul>", alt=True)
              + sec(f"Qué incluye nuestro mantenimiento de {p}", f"<p>En la visita revisamos {e['la']} {s} completo y nos enfocamos en estas tareas:</p><ul>{incl}</ul><p>Al terminar te explicamos el estado del equipo y qué conviene vigilar.</p>")
              + sec(f"Si algo ya falla en {e['la']} {s}", f'<p>El mantenimiento previene, pero si ya notas un problema revisa estas guías: <a href="/{sl}/reparacion/">reparación de {p}</a> y <a href="/{sl}/instalacion/">instalación de {p}</a>.</p>')
              + sec(f"Preguntas sobre el mantenimiento de {p}", faq_html(e["faq"][1:3] + e["faq"][3:]), alt=True)
              + cta_band(f"Agenda el mantenimiento de tu {s}", f"Hola, quiero mantenimiento para mi {s} en Guayaquil"))
    pagina(f"/{sl}/mantenimiento/", f"Mantenimiento de {p} en Guayaquil | Preventivo", f"Mantenimiento preventivo de {p} en Guayaquil: plan, frecuencia, señales de alerta y qué incluye la visita. Evita averías con el calor y la humedad.",
           f"Mantenimiento de {p} en Guayaquil", cuerpo, cr + [("Mantenimiento", f"/{sl}/mantenimiento/")], hero, [faq_ld(e["faq"][1:3]), {"@type": "Service", "name": f"Mantenimiento de {p}", "provider": {"@id": DOM + "/#negocio"}, "areaServed": {"@type": "City", "name": "Guayaquil"}}],
           bd=f"Mantenimiento · {e['corto']}", lead=f"Mantén {e['la']} {s} en buen estado con un plan sencillo, pensado para el clima de Guayaquil.", btns=(f"Hola, quiero mantenimiento para mi {s} en Guayaquil", "Pedir mantenimiento"), prio="0.8")
    # --- instalación
    i = e["inst"]; U = set(); hero = foto(e["foto"], sl + "ins", U); img = figura(foto("personas", sl + "insp", U))
    cuerpo = (sec(f"Cómo instalamos {e['la']} {s}", f'<div class="two"><div><p>{esc(i["intro"])}</p><p>{esc(i["gye"])}</p></div>{img}</div>')
              + sec("Qué debes tener listo antes de la instalación", "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in i["antes"]) + "</ul>", alt=True)
              + sec("Paso a paso de la instalación", "<ol>" + "".join(f"<li>{esc(x)}</li>" for x in i["pasos"]) + "</ol>")
              + sec("Errores comunes que evitamos", "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in i["errores"]) + "</ul>", alt=True)
              + sec(f"Señales de que {e['la']} {s} quedó mal instalado", "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in EXTRA[sl]["mala_inst"]) + "</ul>")
              + sec(f"Por qué conviene que lo instale un técnico", f"<p>Una instalación hecha sin cuidado se paga después con averías, más consumo de energía o riesgos de seguridad. En el caso de {p}, los errores más frecuentes son: {esc('; '.join(bajar(x.rstrip('.')) for x in i['errores'][:3]))}. Un técnico verifica cada conexión, prueba el equipo y te deja explicado cómo usarlo y cuidarlo.</p>", alt=True)
              + sec(f"Después de instalar {e['la']} {s}", f'<p>Una instalación correcta se complementa con un buen mantenimiento. Mira el <a href="/{sl}/mantenimiento/">plan de mantenimiento de {p}</a> y, si algo falla, la <a href="/{sl}/reparacion/">reparación de {p}</a>.</p>')
              + sec(f"Preguntas sobre la instalación de {p}", faq_html([q for q in e["faq"] if re.search(r"instal", q[0] + q[1], re.I)] or e["faq"][:2]), alt=True)
              + cta_band(f"Pide la instalación de tu {s}", f"Hola, necesito instalar {e['art']} {s} en Guayaquil"))
    pagina(f"/{sl}/instalacion/", f"Instalación de {p} en Guayaquil | A domicilio", f"Instalación de {p} en Guayaquil: requisitos previos, paso a paso, errores comunes y qué incluye. Instalación segura y probada.",
           f"Instalación de {p} en Guayaquil", cuerpo, cr + [("Instalación", f"/{sl}/instalacion/")], hero, [{"@type": "Service", "name": f"Instalación de {p}", "provider": {"@id": DOM + "/#negocio"}, "areaServed": {"@type": "City", "name": "Guayaquil"}}],
           bd=f"Instalación · {e['corto']}", lead=f"Instalamos {p} de forma segura y la probamos antes de dejarla funcionando. " + i["intro"].split(". ")[0] + ".", btns=(f"Hola, necesito instalar {e['art']} {s} en Guayaquil", "Pedir instalación"), prio="0.8")
    # --- fallas
    for k, f in enumerate(e["fallas"]):
        U = set(); hero = foto(e["foto"], f["slug"], U); img = figura(foto("personas", f["slug"] + "p", U))
        otras = "".join(f'<a class="card l" href="/{sl}/{x["slug"]}/"><span class="t">{esc(cap(x["termino"]))}</span>{esc(x["sintoma"])}</a>' for x in e["fallas"] if x["slug"] != f["slug"])
        causas = "".join(f"<h3>{esc(c)}</h3><p>{esc(t)}</p>" for c, t in f["causas"])
        var = [f["termino"] + " en Guayaquil", "reparación de " + e["p"] + " en Guayaquil", "técnico de " + e["p"] + " a domicilio", f["termino"] + " qué hacer"]
        faq = [(f"¿Cuánto cuesta arreglar {f['termino'].replace('mi ', '')} en Guayaquil?", f"Depende de la pieza que falle: {bajar(f['causas'][0][0])}, {bajar(f['causas'][1][0])} u otra. Después del diagnóstico te damos el valor por escrito, antes de reparar."),
               (f"¿Qué datos necesito para pedir la visita por «{f['termino']}»?", f"La marca, el modelo y una descripción o un video corto de lo que notas. En el equipo hay una etiqueta con el modelo y la serie; una foto de esa etiqueta acelera el diagnóstico."),
               (f"¿Puedo seguir usando {e['la']} {s} si presenta este problema?", "Depende de la causa. Si hay olor a quemado, chispas, olor a gas o agua cerca de enchufes, deja de usar el equipo y llama. En los demás casos, prueba lo indicado en esta página y, si el problema vuelve, solicita la revisión.")]
        cuerpo = (sec(f"{cap(f['termino'])}: qué significa", f'<div class="two"><div><div class="rr"><b>Resumen</b>{esc(f["sintoma"])}</div><p>{esc(f["causas"][0][1])}</p></div>{img}</div>')
                  + sec("Causas más probables", causas, alt=True, lead=f"Estas son las causas que revisamos, de la más a la menos frecuente, cuando {bajar(f['sintoma'].rstrip('.'))}.")
                  + sec("Qué puedes probar tú antes de llamar", "<ol>" + "".join(f"<li>{esc(x)}</li>" for x in f["probar"]) + "</ol>" + f'<div class="call"><b>¿Cuándo llamar?</b> {esc(f["llamar"])}</div>')
                  + sec("Qué revisa el técnico en tu casa", "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in f["revisa"]) + "</ul>" + f"<p><b>Cómo prevenirlo:</b> {esc(f['prevenir'])}</p>", alt=True)
                  + sec("Qué no hacer", "<ul>" + "".join(f"<li>{esc(EXTRA[sl]['nohacer'][(k + j) % len(EXTRA[sl]['nohacer'])])}</li>" for j in range(2)) + "</ul>")
                  + sec(f"Cómo distinguirla de otras fallas de {p}", "<ul>" + "".join(f"<li>Si en cambio {esc(bajar(x['sintoma'].rstrip('.')))}, la causa más frecuente es {esc(bajar(x['causas'][0][0]))}. <a href=\"/{sl}/{x['slug']}/\">Ver {esc(x['termino'])}</a>.</li>" for x in e["fallas"] if x["slug"] != f["slug"]) + "</ul>", alt=True)
                  + sec("Otras formas de buscar este problema", "".join(f'<span class="pill">{esc(v)}</span>' for v in var))
                  + sec(f"Otras fallas de {p}", f'<div class="g c2">{otras}</div><p style="margin-top:14px"><a href="/{sl}/reparacion/">Ver toda la reparación de {p}</a> · <a href="/{sl}/mantenimiento/">Mantenimiento de {p}</a> · <a href="/{sl}/instalacion/">Instalación de {p}</a> · <a href="/{sl}/">Servicio técnico de {p}</a></p>', alt=True)
                  + sec("Preguntas frecuentes", faq_html(faq))
                  + cta_band(f"Pide la visita por «{f['termino']}»", f"Hola, mi {s} presenta: {f['termino']}. Estoy en Guayaquil."))
        pagina(f"/{sl}/{f['slug']}/", f["titulo"], f"{cap(f['termino'])} en Guayaquil: causas más probables, qué puedes probar, cuándo llamar y qué revisa el técnico a domicilio.",
               cap(f["termino"]) + " en Guayaquil", cuerpo, cr + [(cap(f["termino"]), f"/{sl}/{f['slug']}/")], hero, [faq_ld(faq), {"@type": "Service", "name": f"Reparación: {f['termino']}", "provider": {"@id": DOM + "/#negocio"}, "areaServed": {"@type": "City", "name": "Guayaquil"}}],
               bd=f"{e['corto']} · Falla", lead="Qué puede ser, qué puedes probar tú y cuándo llamar al técnico.", btns=(f"Hola, mi {s} presenta: {f['termino']}. Estoy en Guayaquil.", "Pedir visita"), prio="0.7")

# ------------------------------------------------------------------ zonas
def build_zonas():
    for z in ZONAS:
        U = set(); hero = foto("personas", z["slug"], U)
        tarj = "".join(f'<a class="card l" href="/{k}/"><span class="t">{esc(EQ[k]["corto"])} en {esc(z["nombre"])}</span>{esc(bajar(EQ[k]["fallas"][0]["termino"]))}, {esc(bajar(EQ[k]["fallas"][1]["termino"]))} y más</a>' for k in z["pedidos"])
        ejem = "".join(f"<li><b>{esc(EQ[k]['corto'])}:</b> {esc(EQ[k]['fallas'][0]['sintoma'])}</li>" for k in z["pedidos"])
        otras = "".join(f'<a class="card l" href="/{x["slug"]}/"><span class="t">{esc(x["nombre"])}</span>{esc(x["barrios"])}</a>' for x in ZONAS if x["slug"] != z["slug"])
        faq = [(f"¿Atienden en {z['nombre']}?", f"Sí. Atendemos {z['art']}, incluyendo {z['barrios']}. Escríbenos con tu dirección o sector para coordinar la visita."),
               (f"¿Qué electrodomésticos reparan más en {z['nombre']}?", f"En {z['art']} lo que más vemos es {z['frecuente']}. También atendemos el resto de equipos del hogar."),
               (f"¿Cómo coordino la visita en {z['nombre']}?", z["acceso"])]
        cuerpo = (sec(f"Servicio técnico de electrodomésticos en {z['nombre']}", f'<div class="two"><div><p>{esc(z["vivienda"])}</p><p><b>Sectores que atendemos:</b> {esc(z["barrios"])}.</p><p><b>Clima y condiciones:</b> {esc(z["clima"])}</p></div>{figura(foto("personas", "cuerpo" + str(len(paginas)), U))}</div>')
                  + sec(f"Lo que más reparamos en {z['nombre']}", f'<div class="g c3">{tarj}</div><ul style="margin-top:14px">{ejem}</ul>', alt=True)
                  + sec(f"Un consejo para quienes viven en {z['nombre']}", (lambda k, fi, ti: f"<p>{esc(z['clima'])} Por eso, si tu {EQ[k]['s']} presenta «{esc(EQ[k]['fallas'][fi]['termino'])}», empieza por esto: {esc(bajar(EQ[k]['fallas'][fi]['probar'][0]))} Si el problema continúa, <a href=\"/{k}/{EQ[k]['fallas'][fi]['slug']}/\">revisa las causas y cuándo llamar</a>.</p><p><b>Mantenimiento recomendado para {esc(EQ[k]['p'])}:</b> {esc(EQ[k]['mant']['tabla'][ti][0])} ({esc(bajar(EQ[k]['mant']['tabla'][ti][1]))}). {esc(EQ[k]['mant']['tabla'][ti][2])}</p>")(z['pedidos'][ZONAS.index(z) % 3], ZONAS.index(z) % 3, ZONAS.index(z) % 6))
                  + sec("Cómo coordinamos la visita", f"<p>{esc(z['acceso'])}</p><p>Para que la visita sea más rápida, ten a mano la marca, el modelo y una descripción de lo que notas. Puedes enviar fotos o un video corto por WhatsApp.</p>")
                  + sec(f"Preguntas sobre el servicio en {z['nombre']}", faq_html(faq), alt=True)
                  + sec("Otras zonas de Guayaquil", f'<div class="g c3">{otras}</div>')
                  + cta_band(f"Servicio técnico en {z['nombre']}", f"Hola, necesito servicio técnico en {z['nombre']}, Guayaquil"))
        pagina(f"/{z['slug']}/", f"Servicio técnico en {z['nombre']} | Electrodomésticos", f"Servicio técnico de electrodomésticos en {z['nombre']}: reparación, mantenimiento e instalación a domicilio en {z['barrios']}.",
               f"Servicio técnico en {z['nombre']}", cuerpo, [("Inicio", "/"), ("Zonas", "/servicio-tecnico-cerca-de-mi/"), (z["nombre"], f"/{z['slug']}/")], hero, [faq_ld(faq), {"@type": "Service", "name": f"Servicio técnico en {z['nombre']}", "provider": {"@id": DOM + "/#negocio"}, "areaServed": {"@type": "Place", "name": z["nombre"]}}],
               bd=f"Zona · {z['nombre']}", lead=f"Atendemos {z['art']}: {z['barrios']}.", btns=(f"Hola, necesito servicio técnico en {z['nombre']}, Guayaquil", "Pedir visita"), prio="0.7")

# ------------------------------------------------------------------ páginas de búsqueda
def build_terminos():
    def eq_rapido(f_slug_idx=0):
        return "".join(f'<div class="card"><h3><a href="/{e["slug"]}/">{esc(e["corto"])}</a></h3><p>{esc(cap(e["fallas"][0]["termino"]))}: {esc(e["fallas"][0]["sintoma"])}</p><p><a href="/{e["slug"]}/{e["fallas"][0]["slug"]}/">Ver causas y qué probar</a></p></div>' for e in EQS)
    # teléfono
    U = set(); hero = foto("personas", "tel", U)
    c = (sec("Cómo pedir un técnico en Guayaquil", f'<div class="two"><div><p>Para pedir servicio técnico de electrodomésticos en Guayaquil puedes llamar al <b>{TEL}</b> o escribir por WhatsApp al mismo número. Lo más rápido es WhatsApp, porque puedes enviar una foto de la etiqueta del equipo y un video corto de lo que notas.</p><p>Con esos datos te orientamos sobre la causa más probable, coordinamos el día y la franja de la visita y te explicamos cómo es el proceso.</p><p><a class="btn" href="{wa("Hola, necesito servicio técnico en Guayaquil")}" target="_blank" rel="noopener">Escribir por WhatsApp</a></p></div>{figura(foto("personas", "cuerpo" + str(len(paginas)), U))}</div>', lead="Un solo número para pedir diagnóstico, reparación, mantenimiento o instalación.")
         + sec("Qué datos tener a mano", "<ul><li><b>Equipo y marca:</b> por ejemplo, refrigeradora Samsung o lavadora Mabe.</li><li><b>Modelo y serie:</b> están en una etiqueta en el equipo; una foto es suficiente.</li><li><b>Qué notas:</b> el síntoma o el código que aparece en la pantalla.</li><li><b>Dónde estás:</b> sector de Guayaquil, y si es edificio o urbanización, el nombre.</li><li><b>Cuándo empezó:</b> y si ocurrió algo antes, como una tormenta o un corte de luz.</li></ul><p><a href='/guias/como-preparar-la-visita-del-tecnico/'>Cómo preparar la visita del técnico</a></p>", alt=True)
         + sec("Qué decir según tu equipo", f'<div class="g c2">{eq_rapido()}</div>')
         + sec("Preguntas sobre el teléfono y la atención", faq_html([("¿El teléfono sirve también para WhatsApp?", "Sí, es el mismo número: " + TEL + "."), ("¿Atienden fines de semana?", "Escríbenos por WhatsApp y confirmamos la disponibilidad para el día que necesitas."), ("¿Puedo mandar fotos y videos?", "Sí, ayudan mucho a orientar el diagnóstico antes de la visita.")]), alt=True)
         + cta_band("Llama o escribe ahora", "Hola, necesito servicio técnico en Guayaquil"))
    pagina("/telefono-servicio-tecnico-guayaquil/", "Teléfono de servicio técnico de electrodomésticos Guayaquil", f"Teléfono y WhatsApp de servicio técnico de electrodomésticos en Guayaquil: {TEL}. Qué datos tener a mano y qué decir según tu equipo.", "Teléfono de servicio técnico de electrodomésticos en Guayaquil", c,
           [("Inicio", "/"), ("Teléfono", "/telefono-servicio-tecnico-guayaquil/")], hero, [], bd="Contacto", lead=f"Llama o escribe al {TEL} para pedir diagnóstico, reparación, mantenimiento o instalación.", prio="0.8")
    # a domicilio
    U = set(); hero = foto("personas", "dom", U); img2 = figura(foto("personas", "dom2", U))
    rev = "".join(f"<li><b>{esc(e['corto'])}:</b> {esc(e['fallas'][0]['revisa'][0])}</li>" for e in EQS)
    c = (sec("Cómo funciona la visita a domicilio", f'<div class="two"><div><p>El servicio técnico a domicilio evita que tengas que mover tu refrigeradora, tu lavadora o tu cocina. El técnico llega a tu casa o apartamento en Guayaquil, revisa el equipo en su lugar y te explica qué pasa antes de tocar nada.</p><ol><li>Nos escribes con el equipo, la marca y el síntoma.</li><li>Coordinamos el día y la franja de la visita.</li><li>El técnico revisa el equipo y mide lo necesario.</li><li>Te explica la causa y el valor por escrito.</li><li>Si apruebas, repara y prueba el equipo contigo.</li></ol></div>{hero and figura(foto("personas", "cuerpo" + str(len(paginas)), U))}</div>')
         + sec("Qué revisa el técnico según el equipo", f"<ul>{rev}</ul>", alt=True)
         + sec("Qué dejar listo antes de la visita", f'<div class="two"><div><ul><li>Acceso libre al equipo y a la toma de corriente.</li><li>La etiqueta con el modelo a la vista, o una foto de ella.</li><li>Un adulto presente que pueda aprobar la reparación.</li><li>En edificios y urbanizaciones, aviso en portería y ascensor de carga si el equipo es grande.</li><li>Para refrigeradoras, los alimentos delicados en una nevera portátil.</li></ul><p><a href="/guias/como-preparar-la-visita-del-tecnico/">Guía completa para preparar la visita</a></p></div>{img2}</div>')
         + sec("¿Y si hace falta un repuesto?", "<p>Si el repuesto no está en la visita, te lo informamos, coordinamos su conseguido y una segunda visita para instalarlo, siempre con el valor por escrito antes de seguir. Si la reparación no conviene, te lo decimos con honestidad.</p>", alt=True)
         + cta_band("Pide tu visita a domicilio", "Hola, quiero una visita a domicilio en Guayaquil"))
    pagina("/servicio-tecnico-a-domicilio/", "Servicio técnico a domicilio en Guayaquil | Electrodomésticos", "Servicio técnico a domicilio de electrodomésticos en Guayaquil: cómo es la visita, qué revisa el técnico según el equipo y qué dejar listo.", "Servicio técnico a domicilio en Guayaquil", c,
           [("Inicio", "/"), ("A domicilio", "/servicio-tecnico-a-domicilio/")], hero, [], bd="A domicilio", lead="Revisamos y reparamos tus electrodomésticos en tu casa, sin que muevas el equipo.", prio="0.8")
    # cerca de mí
    U = set(); hero = foto("personas", "cerca", U)
    zl = "".join(f'<a class="card l" href="/{z["slug"]}/"><span class="t">{esc(z["nombre"])}</span><b>Sectores:</b> {esc(z["barrios"])}.<br>{esc(z["frecuente"].capitalize())}.</a>' for z in ZONAS)
    c = (sec("Servicio técnico cerca de ti en Guayaquil", f'<div class="two"><div><p>Buscar un servicio técnico cerca de ti es buscar rapidez y confianza. Atendemos a domicilio en las principales zonas de Guayaquil y alrededores: norte, sur, centro, Los Ceibos y la Vía a la Costa, Samborondón, la Vía a Daule y Durán.</p><p>Elige tu zona para ver qué electrodomésticos reparamos más allí, cómo coordinamos el ingreso y qué consejos aplican al clima y a las viviendas del sector.</p></div>{figura(foto("personas", "cuerpo" + str(len(paginas)), U))}</div>')
         + sec("Zonas que atendemos", f'<div class="g c2">{zl}</div>', alt=True)
         + sec("¿No ves tu sector?", "<p>Escríbenos con tu dirección o sector. Atendemos buena parte de Guayaquil y sus alrededores, y te confirmamos la cobertura y la franja disponible por WhatsApp.</p>")
         + cta_band("Pide tu visita en tu zona", "Hola, necesito servicio técnico cerca de mí en Guayaquil"))
    pagina("/servicio-tecnico-cerca-de-mi/", "Servicio técnico cerca de mí en Guayaquil | Zonas", "Servicio técnico de electrodomésticos cerca de ti en Guayaquil: zonas que atendemos, sectores y cómo coordinamos la visita a domicilio.", "Servicio técnico cerca de mí en Guayaquil", c,
           [("Inicio", "/"), ("Zonas", "/servicio-tecnico-cerca-de-mi/")], hero, [{"@type": "ItemList", "name": "Zonas de servicio en Guayaquil", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": DOM + f"/{z['slug']}/", "name": z["nombre"]} for i, z in enumerate(ZONAS)]}], bd="Cobertura", lead="Atendemos a domicilio en las principales zonas de Guayaquil y sus alrededores.", prio="0.8")
    # cuánto cuesta
    U = set(); hero = foto("personas", "costo", U)
    var = "".join(f"<tr><td data-l=\"Equipo\"><a href=\"/{e['slug']}/reparacion/\">{esc(e['corto'])}</a></td><td data-l=\"Qué hace variar el valor\">{esc(e['fallas'][0]['causas'][0][0])}, {esc(bajar(e['fallas'][1]['causas'][0][0]))} y la disponibilidad del repuesto.</td></tr>" for e in EQS)
    c = (sec("Cuánto cuesta reparar un electrodoméstico en Guayaquil", f'<div class="two"><div><p>El valor de una reparación depende de la falla, de la pieza que haya que cambiar, de la marca y el modelo del equipo y de si el repuesto está disponible. Por eso no damos un precio sin ver el equipo: preferimos diagnosticar y darte un valor claro por escrito.</p><p>Esto evita sorpresas: sabes cuánto cuesta, qué incluye y decides tú si apruebas la reparación.</p></div>{figura(foto("personas", "cuerpo" + str(len(paginas)), U))}</div>')
         + sec("Qué hace variar el valor, por equipo", f'<table class="tb"><thead><tr><th>Equipo</th><th>Qué hace variar el valor</th></tr></thead><tbody>{var}</tbody></table>', alt=True)
         + sec("Cómo te cotizamos", "<ol><li>Revisamos el equipo y confirmamos la causa.</li><li>Te explicamos qué pieza falla y si hay alternativas.</li><li>Te damos el valor por escrito antes de reparar.</li><li>Solo reparamos si tú apruebas el valor.</li></ol>")
         + sec("¿Conviene reparar o cambiar?", "<p>Una regla útil: si la reparación se acerca a la mitad del precio de un equipo nuevo equivalente y el aparato tiene muchos años, conviene evaluar el cambio. Si cuesta mucho menos, casi siempre conviene reparar. Te lo explicamos con más detalle en la <a href=\"/guias/reparar-o-cambiar-tu-electrodomestico/\">guía de reparar o cambiar</a>.</p>", alt=True)
         + cta_band("Pide tu diagnóstico y valor por escrito", "Hola, quiero cotizar la reparación de un electrodoméstico en Guayaquil"))
    pagina("/cuanto-cuesta-reparar-electrodomesticos/", "Cuánto cuesta reparar un electrodoméstico en Guayaquil", "Cuánto cuesta reparar un electrodoméstico en Guayaquil: qué hace variar el valor por equipo, cómo cotizamos y cuándo conviene reparar o cambiar.", "Cuánto cuesta reparar un electrodoméstico en Guayaquil", c,
           [("Inicio", "/"), ("Cuánto cuesta", "/cuanto-cuesta-reparar-electrodomesticos/")], hero, [], bd="Valores", lead="Te damos el valor por escrito antes de reparar. Esto es lo que lo hace variar.", prio="0.8")
    # garantía
    U = set(); hero = foto("personas", "gar", U)
    c = (sec("Garantía de la reparación de electrodomésticos", f'<div class="two"><div><p>Cuando reparas un electrodoméstico, lo importante es que quede por escrito qué se hizo y qué cubre la reparación. En Guayaquil, como en cualquier ciudad, conviene saber qué preguntar antes de aprobar un trabajo.</p><p>Esta página te explica qué debe constar en una orden de servicio, la diferencia entre la garantía de fábrica y la garantía de una reparación, y cómo reclamar si algo no queda bien.</p></div>{figura(foto("personas", "cuerpo" + str(len(paginas)), U))}</div>')
         + sec("Qué debe constar por escrito", "<ul><li>El equipo, la marca, el modelo y la falla que se reportó.</li><li>El trabajo realizado y las piezas cambiadas.</li><li>El valor de la mano de obra y de los repuestos, por separado.</li><li>La garantía que cubre el trabajo y las piezas instaladas, con su plazo.</li><li>Los datos de contacto para reclamos.</li></ul>", alt=True)
         + sec("Garantía de fábrica y garantía de reparación", "<p>La garantía de fábrica la da el fabricante o la tienda donde compraste el equipo y suele cubrir defectos de fabricación durante un tiempo. La garantía de una reparación cubre el trabajo y las piezas que se instalaron en esa reparación. Si tu equipo aún tiene garantía de fábrica, conviene revisar sus condiciones antes de que un tercero intervenga.</p>")
         + sec("Tus derechos como consumidor", "<p>En Ecuador, la Ley Orgánica de Defensa del Consumidor protege tus derechos en la compra de bienes y la prestación de servicios. Pide siempre un comprobante del servicio y guarda la orden de trabajo.</p>", alt=True)
         + sec("Cómo trabajamos", "<p>Te explicamos la causa, te damos el valor por escrito antes de reparar y probamos el equipo contigo al terminar. Si algo no queda bien, escríbenos por WhatsApp con la orden de servicio y lo revisamos.</p>")
         + cta_band("¿Tienes dudas sobre una reparación?", "Hola, tengo una duda sobre la garantía de una reparación en Guayaquil"))
    pagina("/garantia-de-la-reparacion/", "Garantía de la reparación de electrodomésticos | Guayaquil", "Garantía de reparación de electrodomésticos en Guayaquil: qué debe constar por escrito, garantía de fábrica frente a la de reparación y tus derechos.", "Garantía de la reparación de electrodomésticos en Guayaquil", c,
           [("Inicio", "/"), ("Garantía", "/garantia-de-la-reparacion/")], hero, [], bd="Garantía", lead="Qué pedir por escrito y qué cubre una reparación.", prio="0.7")
    # repuestos
    txt = open(AQUI.parent / "cst_build.py", encoding="utf-8").read()
    def lit(nombre):
        i = txt.index(nombre + " = {"); j = txt.index("\n}\n", i) + 2
        return eval(txt[i + len(nombre) + 3:j])
    PARTES = lit("PARTES"); DESC = lit("PARTE_DESC")
    mapa = {"refrigeradoras": "neveras", "lavadoras": "lavadoras", "secadoras": "secadoras", "cocinas-y-hornos": "cocinas", "aires-acondicionados": "aires", "lavavajillas": "lavavajillas", "microondas": None}
    blq = ""
    for e in EQS:
        k = mapa[e["slug"]]
        if not k or k not in PARTES: continue
        lst = [(pn, DESC[pn]) for pn, _ in PARTES[k] if pn in DESC][:6]
        blq += sec(f"Repuestos para {e['p']}", "<dl class=\"pz\">" + "".join(f"<dt>{esc(a)}</dt><dd>{esc(b)}</dd>" for a, b in lst) + f'</dl><p><a href="/{e["slug"]}/reparacion/">Reparación de {e["p"]}</a></p>', alt=(EQS.index(e) % 2 == 1))
    U = set(); hero = foto("personas", "rep", U)
    c = (sec("Repuestos para electrodomésticos en Guayaquil", f'<div class="two"><div><p>Cada electrodoméstico tiene piezas que se desgastan con el uso, el calor y la humedad. Conocerlas ayuda a entender qué se cambia en una reparación y por qué el valor varía.</p><p>Estas son las piezas que más se cambian en cada equipo. Si necesitas un repuesto específico, escríbenos con la marca, el modelo y una foto de la pieza.</p></div>{figura(foto("personas", "cuerpo" + str(len(paginas)), U))}</div>') + blq
         + cta_band("¿Buscas un repuesto?", "Hola, busco un repuesto para un electrodoméstico en Guayaquil"))
    pagina("/repuestos-para-electrodomesticos/", "Repuestos para electrodomésticos en Guayaquil", "Repuestos para electrodomésticos en Guayaquil: las piezas que más se cambian en refrigeradoras, lavadoras, secadoras, aires, cocinas y lavavajillas.", "Repuestos para electrodomésticos en Guayaquil", c,
           [("Inicio", "/"), ("Repuestos", "/repuestos-para-electrodomesticos/")], hero, [], bd="Repuestos", lead="Las piezas que más se cambian en cada equipo y qué hacen.", prio="0.7")
    # marcas
    logos = "".join(f'<div class="mk"><img src="/img/logos/{k}.png" alt="Logo {MARCA_NOM[k]}" width="130" height="42" loading="lazy"></div>' for k in MARCA_NOM)
    tarj = "".join(f'<div class="card"><h3>{MARCA_NOM[k]}</h3><p>Reparamos {esc(", ".join(MARCA_DATOS[k]["equipos"][:5]).replace("neveras", "refrigeradoras").replace("-", " "))}.</p></div>' for k in MARCA_NOM if k in MARCA_DATOS)
    U = set(); hero = foto("personas", "marcas", U)
    c = (sec("Marcas de electrodomésticos que reparamos en Guayaquil", f'<div class="two"><div><p>Reparamos electrodomésticos de las marcas más comunes en los hogares de Guayaquil. Los técnicos trabajan con todas las líneas: refrigeradoras, lavadoras, secadoras, cocinas y hornos, aires acondicionados, lavavajillas y microondas.</p><p>Si tu marca no aparece, escríbenos: muchas veces podemos atenderla igualmente.</p></div>{figura(foto("personas", "cuerpo" + str(len(paginas)), U))}</div>')
         + sec("Marcas", f'<div class="marcas">{logos}</div>', alt=True)
         + sec("Qué equipos de cada marca atendemos", f'<div class="g c3">{tarj}</div>')
         + sec("Importante", "<p>Somos un servicio técnico independiente. Las marcas y logos pertenecen a sus propietarios y se muestran únicamente para indicar los equipos que reparamos.</p>", alt=True)
         + cta_band("Cuéntanos tu marca y modelo", "Hola, quiero revisar mi electrodoméstico (marca y modelo) en Guayaquil"))
    pagina("/marcas-que-reparamos/", "Marcas de electrodomésticos que reparamos en Guayaquil", "Marcas de electrodomésticos que reparamos en Guayaquil: Samsung, LG, Whirlpool, Mabe, Electrolux, Frigidaire, General Electric, Haceb y KitchenAid.", "Marcas que reparamos en Guayaquil", c,
           [("Inicio", "/"), ("Marcas", "/marcas-que-reparamos/")], hero, [], bd="Marcas", lead="Samsung, LG, Whirlpool, Mabe, Electrolux, Frigidaire, General Electric, Haceb y KitchenAid.", prio="0.7")
    # FAQ general
    grupos = "".join(sec(f"Preguntas sobre {e['p']}", faq_html(e["faq"]), alt=(i % 2 == 1)) for i, e in enumerate(EQS))
    todas = [q for e in EQS for q in e["faq"]]
    c = grupos + cta_band("¿No encuentras tu pregunta?", "Hola, tengo una pregunta sobre un electrodoméstico en Guayaquil")
    pagina("/preguntas-frecuentes/", "Preguntas frecuentes de servicio técnico en Guayaquil", "Preguntas frecuentes sobre reparación, mantenimiento e instalación de electrodomésticos en Guayaquil: refrigeradoras, lavadoras, secadoras, aires y más.", "Preguntas frecuentes sobre servicio técnico en Guayaquil", c,
           [("Inicio", "/"), ("Preguntas frecuentes", "/preguntas-frecuentes/")], foto("personas", "faq", set()), [faq_ld(todas)], bd="Preguntas", lead="Respuestas claras sobre cada electrodoméstico.", prio="0.6")
    # quiénes somos / contacto
    c = (sec("Quiénes somos", "<p>Somos un servicio técnico independiente de electrodomésticos en Guayaquil. Atendemos a domicilio refrigeradoras, lavadoras, secadoras, cocinas y hornos, aires acondicionados, lavavajillas y microondas, de las marcas más comunes en los hogares de la ciudad.</p><p>Nos enfocamos en explicar con claridad qué falla, dar el valor por escrito antes de reparar y probar el equipo contigo al terminar.</p>")
         + sec("Cómo trabajamos", "<ul><li>Diagnóstico en tu casa, sin que muevas el equipo.</li><li>Explicación de la causa en lenguaje claro.</li><li>Valor por escrito antes de reparar.</li><li>Reparación solo si tú la apruebas.</li><li>Prueba del equipo contigo al terminar.</li></ul>", alt=True)
         + sec("Información de esta página", "<p>Los contenidos de este sitio son orientativos y explican causas frecuentes de fallas. El diagnóstico definitivo se confirma siempre con pruebas en el equipo.</p>")
         + cta_band("Hablemos de tu equipo", "Hola, quiero información sobre el servicio técnico en Guayaquil"))
    pagina("/quienes-somos/", "Quiénes somos | Servicio Técnico Guayaquil", "Servicio técnico independiente de electrodomésticos a domicilio en Guayaquil: cómo trabajamos, qué atendemos y qué puedes esperar de la visita.", "Quiénes somos", c,
           [("Inicio", "/"), ("Quiénes somos", "/quienes-somos/")], foto("personas", "qs", set()), [], bd="Nosotros", lead="Servicio técnico independiente de electrodomésticos en Guayaquil.", prio="0.5")
    c = (sec("Cómo contactarnos", f"<p><b>Teléfono y WhatsApp:</b> <a href=\"tel:+{TELW}\">{TEL}</a></p><p>Escríbenos con el equipo, la marca, el modelo y lo que notas, y coordinamos la visita a domicilio en Guayaquil.</p><p><a class=\"btn\" href=\"{wa('Hola, necesito servicio técnico en Guayaquil')}\" target=\"_blank\" rel=\"noopener\">Escribir por WhatsApp</a></p>")
         + sec("Qué incluir en tu mensaje", "<ul><li>El equipo y la marca.</li><li>El modelo (foto de la etiqueta).</li><li>Lo que notas o el código que aparece.</li><li>Tu sector de Guayaquil.</li></ul>", alt=True)
         + sec("Servicios que puedes pedir", '<div class="g c3">' + "".join(f'<a class="card l" href="/{e["slug"]}/"><span class="t">{esc(e["corto"])}</span>Reparación, mantenimiento e instalación</a>' for e in EQS) + "</div>")
         + sec("Zonas que atendemos", '<div class="g c2">' + "".join(f'<a class="card l" href="/{z["slug"]}/"><span class="t">{esc(z["nombre"])}</span>{esc(z["barrios"])}</a>' for z in ZONAS) + "</div>", alt=True))
    pagina("/contacto/", "Contacto | Servicio Técnico Guayaquil", f"Contacto de servicio técnico de electrodomésticos en Guayaquil: teléfono y WhatsApp {TEL}. Escríbenos con el equipo, la marca y el síntoma.", "Contacto", c,
           [("Inicio", "/"), ("Contacto", "/contacto/")], foto("personas", "contacto", set()), [], bd="Contacto", lead=f"Teléfono y WhatsApp: {TEL}.", prio="0.6")
    # legales
    c = sec("Política de privacidad", "<p>Tratamos los datos que nos envías (nombre, sector y descripción del problema) únicamente para coordinar y realizar el servicio técnico. No los compartimos con terceros ajenos al servicio. Puedes pedirnos que corrijamos o eliminemos tus datos escribiéndonos por WhatsApp. Aplicamos las disposiciones de la Ley Orgánica de Protección de Datos Personales del Ecuador.</p>")
    pagina("/politica-de-privacidad/", "Política de privacidad | Servicio Técnico Guayaquil", "Política de privacidad de Servicio Técnico Guayaquil: qué datos recibimos, para qué los usamos y cómo ejercer tus derechos.", "Política de privacidad", c, [("Inicio", "/"), ("Privacidad", "/politica-de-privacidad/")], None, [], noindex=True)
    c = sec("Términos y condiciones", "<p>La información de este sitio es orientativa y no reemplaza el diagnóstico en el equipo. Los valores y la garantía de cada reparación se confirman por escrito antes y después del servicio. Somos un servicio técnico independiente; las marcas mencionadas pertenecen a sus propietarios y se usan solo para indicar los equipos que reparamos.</p>")
    pagina("/terminos-y-condiciones/", "Términos y condiciones | Servicio Técnico Guayaquil", "Términos y condiciones de uso del sitio y de los servicios de Servicio Técnico Guayaquil.", "Términos y condiciones", c, [("Inicio", "/"), ("Términos", "/terminos-y-condiciones/")], None, [], noindex=True)

# ------------------------------------------------------------------ guías
def build_guias():
    U = set(); tarj = "".join(f'<a class="card l" href="/guias/{g["slug"]}/"><span class="t">{esc(g["titulo"])}</span>{esc(g["desc"])}</a>' for g in GUIAS)
    pagina("/guias/", "Guías para cuidar tus electrodomésticos en Guayaquil", "Guías prácticas para cuidar tus electrodomésticos en Guayaquil: humedad y calor, picos de voltaje, cuándo reparar o cambiar y cómo preparar la visita.", "Guías para cuidar tus electrodomésticos",
           sec("Guías", f'<div class="g c2">{tarj}</div>') + cta_band("¿Tienes un problema con tu equipo?", "Hola, necesito servicio técnico en Guayaquil"), [("Inicio", "/"), ("Guías", "/guias/")], foto("personas", "guias", set()),
           [{"@type": "ItemList", "name": "Guías", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": DOM + f"/guias/{g['slug']}/", "name": g["titulo"]} for i, g in enumerate(GUIAS)]}], bd="Guías", lead="Consejos prácticos pensados para el clima y las condiciones de Guayaquil.", prio="0.6")
    for g in GUIAS:
        U = set(); hero = foto("personas", g["slug"], U)
        secs = "".join(sec(t, f"<p>{esc(b)}</p>", alt=(i % 2 == 0)) for i, (t, b) in enumerate(g["secciones"]))
        eq = "".join(f'<a class="card l" href="/{e["slug"]}/"><span class="t">{esc(e["corto"])}</span>Reparación, mantenimiento e instalación</a>' for e in EQS)
        extra = ""
        if g["slug"].startswith("humedad"):
            extra = sec("Qué hacer según tu electrodoméstico", "".join(f'<h3><a href="/{e["slug"]}/mantenimiento/">{esc(e["corto"])}</a></h3><p>{esc(e["mant"]["gye"])}</p>' for e in EQS))
        elif g["slug"].startswith("picos"):
            filas = []
            for e in EQS:
                for f in e["fallas"]:
                    cs = [c for c in f["causas"] if re.search(r"placa|inverter|voltaje|control|electr", c[0] + c[1], re.I)]
                    if cs: filas.append((f'<a href="/{e["slug"]}/">{esc(e["corto"])}</a>', esc(cs[0][0]), esc(cs[0][1]))); break
            extra = sec("Qué daña un pico de voltaje en cada equipo", tabla(["Equipo", "Qué se afecta", "Cómo se nota"], filas))
        elif g["slug"].startswith("reparar"):
            filas = [(f'<a href="/{e["slug"]}/reparacion/">{esc(e["corto"])}</a>', EXTRA[e["slug"]]["vida"], esc("; ".join(EXTRA[e["slug"]]["cuando_reparar"])), esc("; ".join(EXTRA[e["slug"]]["cuando_cambiar"]))) for e in EQS]
            extra = sec("Reparar o cambiar según el equipo", tabla(["Equipo", "Vida útil", "Casi siempre se repara si…", "Conviene evaluar el cambio si…"], filas))
        elif g["slug"].startswith("como-preparar"):
            extra = sec("Qué preparar según tu equipo", "".join(f'<h3><a href="/{e["slug"]}/reparacion/">{esc(e["corto"])}</a></h3><p>{esc(e["fallas"][0]["probar"][0])} {esc(e["inst"]["antes"][0])}</p>' for e in EQS))
        c = sec("Introducción", f"<p>{esc(g['intro'])}</p>") + secs + extra + sec("Servicios por electrodoméstico", f'<div class="g c3">{eq}</div>', alt=True) + cta_band("¿Necesitas una revisión?", "Hola, necesito servicio técnico en Guayaquil")
        pagina(f"/guias/{g['slug']}/", fit(g["titulo"]), g["desc"], g["titulo"], c, [("Inicio", "/"), ("Guías", "/guias/"), (g["titulo"][:48], f"/guias/{g['slug']}/")], hero,
               [{"@type": "Article", "headline": g["titulo"], "description": g["desc"], "datePublished": HOY, "dateModified": HOY, "author": {"@id": DOM + "/#negocio"}, "publisher": {"@id": DOM + "/#negocio"}, "inLanguage": SITE["locale"]}],
               bd="Guía", lead=g["desc"], prio="0.6")

# ------------------------------------------------------------------ inicio
def build_home():
    U = set(); hero = foto("personas", "home", U)
    tiles = "".join(f'<a class="tile" href="/{e["slug"]}/"><div class="ti">{(lambda f: f"<img src={chr(34)}{f['src']}{chr(34)} alt={chr(34)}{esc(f['alt'])}{chr(34)} width={chr(34)}{f['w']}{chr(34)} height={chr(34)}{f['h']}{chr(34)} loading={chr(34)}lazy{chr(34)}>" if f else e["corto"][:1])(foto(e["foto"], "tile" + e["slug"], set()))}</div><b>{esc(e["corto"])}</b><small>Reparación · Mantenimiento · Instalación</small></a>' for e in EQS)
    svc = (f'<div class="svc"><div class="card"><h3>Reparación</h3><p>Diagnóstico a domicilio y reparación de refrigeradoras, lavadoras, secadoras, cocinas y hornos, aires, lavavajillas y microondas. Te damos el valor por escrito antes de reparar.</p><a href="/servicio-tecnico-a-domicilio/">Cómo es la visita</a></div>'
           '<div class="card"><h3>Mantenimiento</h3><p>Limpieza y revisión preventiva que evita averías, baja el consumo y alarga la vida de tus equipos, sobre todo con el calor y la humedad de Guayaquil.</p><a href="/aires-acondicionados/mantenimiento/">Ver mantenimiento de aires</a></div>'
           '<div class="card"><h3>Instalación</h3><p>Instalación segura de equipos nuevos: nivelación, conexión eléctrica, de agua o de gas, y ciclo de prueba antes de dejarlos funcionando.</p><a href="/lavadoras/instalacion/">Ver instalación de lavadoras</a></div></div>')
    logos = "".join(f'<div class="mk"><img src="/img/logos/{k}.png" alt="Logo {MARCA_NOM[k]}" width="130" height="42" loading="lazy"></div>' for k in MARCA_NOM)
    top = "".join(f'<a class="card l" href="/{e["slug"]}/{e["fallas"][0]["slug"]}/"><span class="t">{esc(cap(e["fallas"][0]["termino"]))}</span>{esc(e["fallas"][0]["sintoma"])}</a>' for e in EQS)
    zl = "".join(f'<a class="card l" href="/{z["slug"]}/"><span class="t">{esc(z["nombre"])}</span>{esc(z["barrios"])}</a>' for z in ZONAS)
    gl = "".join(f'<a class="card l" href="/guias/{g["slug"]}/"><span class="t">{esc(g["titulo"])}</span>{esc(g["desc"])}</a>' for g in GUIAS[:3])
    faq = [("¿Hacen servicio técnico a domicilio en Guayaquil?", "Sí. Vamos a tu casa o apartamento en Guayaquil, Samborondón, Daule y Durán para diagnosticar, reparar, dar mantenimiento o instalar tu electrodoméstico."),
           ("¿Qué electrodomésticos atienden?", "Refrigeradoras, lavadoras y centros de lavado, secadoras, cocinas y hornos, aires acondicionados, lavavajillas y microondas, de las marcas más comunes."),
           ("¿Cómo pido una visita?", f"Llama o escribe por WhatsApp al {TEL} con el equipo, la marca, el modelo y lo que notas. Coordinamos el día y la franja."),
           ("¿Dan el valor antes de reparar?", "Sí. Revisamos el equipo, te explicamos la causa y te damos el valor por escrito antes de empezar. Solo reparamos si tú lo apruebas.")]
    cuerpo = (sec("¿Qué electrodoméstico necesitas atender?", stepper(1) + f'<div class="g c4">{tiles}</div>', id="equipos", lead="Toca tu electrodoméstico. Te llevamos a su reparación, su mantenimiento y su instalación, y a las fallas más comunes con texto claro.")
              + sec("Reparación, mantenimiento e instalación", svc, alt=True)
              + sec("Las fallas más buscadas", f'<div class="g c3">{top}</div>', lead="Entra a la tuya para ver causas, qué puedes probar tú y cuándo llamar.")
              + sec("Marcas que reparamos", f'<div class="marcas">{logos}</div><p style="margin-top:14px"><a href="/marcas-que-reparamos/">Ver marcas y equipos que atendemos</a></p>', alt=True)
              + sec("Zonas de Guayaquil que atendemos", f'<div class="g c2">{zl}</div><p style="margin-top:14px"><a href="/servicio-tecnico-cerca-de-mi/">Servicio técnico cerca de mí</a> · <a href="/telefono-servicio-tecnico-guayaquil/">Teléfono de servicio técnico</a> · <a href="/cuanto-cuesta-reparar-electrodomesticos/">Cuánto cuesta reparar</a></p>')
              + sec("Guías útiles", f'<div class="g c3">{gl}</div>', alt=True)
              + sec("Preguntas frecuentes", faq_html(faq))
              + cta_band("Pide tu visita en Guayaquil", "Hola, necesito servicio técnico en Guayaquil"))
    pagina("/", "Servicio técnico de electrodomésticos en Guayaquil | A domicilio", "Servicio técnico de electrodomésticos en Guayaquil: reparación, mantenimiento e instalación a domicilio de refrigeradoras, lavadoras, secadoras, cocinas, aires, lavavajillas y microondas.",
           "Servicio técnico de electrodomésticos en Guayaquil", cuerpo, None, hero, [faq_ld(faq)], bd="Guayaquil · A domicilio", lead="Reparación, mantenimiento e instalación de tus electrodomésticos en tu casa. Elige tu equipo y te guiamos paso a paso.", prio="1.0")

# ------------------------------------------------------------------ archivos del sitio
def archivos():
    (OUT / "assets").mkdir(parents=True, exist_ok=True); (OUT / "assets" / "site.css").write_text(CSS.replace("\n", " "), encoding="utf-8")
    (OUT / "favicon.svg").write_text("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'><rect width='64' height='64' rx='14' fill='#0a4d7c'/><path d='M20 22h24v6H20zM20 32h24v6H20zM26 42h12v4H26z' fill='#fff'/><circle cx='46' cy='18' r='5' fill='#f26b1d'/></svg>", encoding="utf-8")
    (OUT / "img" / "logos").mkdir(parents=True, exist_ok=True)
    for k in MARCA_NOM: shutil.copy(AQUI.parent / "cst_logos" / f"{k}.png", OUT / "img" / "logos" / f"{k}.png")
    # sitemap con imágenes
    L = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for p, pr, im in paginas:
        L.append(f"<url><loc>{DOM}{p}</loc><lastmod>{HOY}</lastmod><priority>{pr}</priority>" + "".join(f"<image:image><image:loc>{DOM}{i}</image:loc></image:image>" for i in dict.fromkeys(im)) + "</url>")
    L.append("</urlset>"); (OUT / "sitemap.xml").write_text("\n".join(L), encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {DOM}/sitemap.xml\n", encoding="utf-8")
    ll = [f"# {NOMBRE}", "", f"> Servicio técnico de electrodomésticos a domicilio en Guayaquil, Ecuador. Reparación, mantenimiento e instalación de refrigeradoras, lavadoras, secadoras, cocinas y hornos, aires acondicionados, lavavajillas y microondas. Teléfono y WhatsApp: {TEL}.", "", "## Servicios"]
    for e in EQS: ll.append(f"- [{e['corto']}]({DOM}/{e['slug']}/): reparación, mantenimiento e instalación")
    ll += ["", "## Zonas"] + [f"- [{z['nombre']}]({DOM}/{z['slug']}/)" for z in ZONAS] + ["", "## Guías"] + [f"- [{g['titulo']}]({DOM}/guias/{g['slug']}/)" for g in GUIAS]
    (OUT / "llms.txt").write_text("\n".join(ll) + "\n", encoding="utf-8")
    (OUT / "404.html").write_text(f'<!doctype html><html lang="es-EC"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Página no encontrada | {NOMBRE}</title><meta name="robots" content="noindex"><link rel="stylesheet" href="/assets/site.css?v={CSSV}"></head><body><main class="w" style="padding:60px 16px"><h1>No encontramos esa página</h1><p>Prueba con el servicio que necesitas:</p><p>' + " · ".join(f'<a href="/{e["slug"]}/">{esc(e["corto"])}</a>' for e in EQS) + f'</p><p><a class="btn" href="/">Ir al inicio</a></p></main></body></html>', encoding="utf-8")
    H = ["# Generado por gye_build.py", "RewriteEngine On", "RewriteCond %{HTTPS} off", "RewriteRule ^(.*)$ https://servicio-tecnico-guayaquil.com/$1 [R=301,L]", "RewriteCond %{HTTP_HOST} ^www\\. [NC]", "RewriteRule ^(.*)$ https://servicio-tecnico-guayaquil.com/$1 [R=301,L]",
         "ErrorDocument 404 /404.html", "Options -Indexes", "<IfModule mod_deflate.c>", "AddOutputFilterByType DEFLATE text/html text/css application/javascript application/json application/xml text/xml text/plain image/svg+xml", "</IfModule>",
         "<IfModule mod_expires.c>", "ExpiresActive On", 'ExpiresByType image/webp "access plus 1 month"', 'ExpiresByType image/png "access plus 1 month"', 'ExpiresByType text/css "access plus 1 year"', 'ExpiresByType text/html "access plus 0 seconds"', "</IfModule>",
         "<IfModule mod_headers.c>", '<FilesMatch "\\.html$">', 'Header set Cache-Control "public, max-age=0, must-revalidate"', "</FilesMatch>", '<FilesMatch "\\.css$">', 'Header set Cache-Control "public, max-age=31536000, immutable"', "</FilesMatch>",
         'Header always set X-Content-Type-Options "nosniff"', 'Header always set Referrer-Policy "strict-origin-when-cross-origin"', 'Header always set X-Frame-Options "SAMEORIGIN"', "</IfModule>"]
    (OUT / ".htaccess").write_text("\n".join(H) + "\n", encoding="utf-8")

if __name__ == "__main__":
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    build_home()
    for e in EQS: build_equipo(e)
    build_zonas(); build_terminos(); build_guias(); archivos()
    for r, ds, fs in os.walk(OUT):
        os.chmod(r, 0o755)
        for f in fs: os.chmod(os.path.join(r, f), 0o644)
    print(len(paginas), "páginas indexables")
