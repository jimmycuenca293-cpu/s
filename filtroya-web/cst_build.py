# -*- coding: utf-8 -*-
"""Genera centrodeserviciotecnicopanama.com: portada Samsung + una sección fuerte por marca.
Uso: python3 cst_build.py <salida> [carpeta_imagenes_origen=/tmp/cst_src]"""
import sys, os, re, json, html, shutil, pathlib, hashlib, glob
from cst_datos import M, EQ, BRANDS_ORDER, ZONAS

OUT = pathlib.Path(sys.argv[1]); SRC = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "/tmp/cst_src")
DOM = "https://centrodeserviciotecnicopanama.com"
NOMBRE = "Centro de Servicio Técnico Panamá"
TEL = "+507 6933-7976"; TELN = "50769337976"
GSC = ["Ns9i5lJP6EAsC0ExK8vxW-GtkXKO8kdnf7S5kNFx54k", "ozHF9bZezdQ-xxlFh0xMkpJZRx0rwRKgNXAZQhrbmQg"]
HOY = "2026-11-20"
esc = html.escape
ROOT = pathlib.Path(__file__).resolve().parent
paginas = []   # (url, prioridad, marca)

# ---------------------------------------------------------------- imágenes
EXCLUIR = {  # carteles de «autorizado»/«oficial», Costa Rica, sellos de garantía, fondos rotos o casi duplicadas (revisadas a mano)
 "banner-tecnico-kitchenaid-confiado", "secretaria-kitchenaid-escritorio", "tecnico-kitchenaid-reparando-batidora", "tecnico-kitchenaid-domicilio-furgon",
 "recepcion-whirlpool-1", "recepcion-whirlpool-2", "tecnico-whirlpool-diagnostico-lavadora-2",
 "tecnico-mabe-camino-centro-reparacion", "tecnico-mabe-saludo-cliente-puerta", "torre-lavado-secado-mabe-garantia", "banner-instalaciones-mabe",
 "agente-electrolux-mostrador-cliente", "banner-urgencias-tecnicas-electrolux", "refrigeradora-electrolux-side-by-side-negra",
 "banner-frigidaire-cocina", "recepcion-frigidaire-2", "tecnico-frigidaire-kitchen-2",
 "producto-lavadora-carga-superior-haceb", "producto-hornos-ge", "producto-lavadoras-ge", "producto-lavavajillas-ge", "producto-neveras-ge",
 "tecnico-lg-autorizado", "tecnico-lg-recepcion-2", "tecnico-lg-recepcion-4",
 "tecnico-autorizado-nevera", "tecnico-domicilio-furgon", "tecnico-reparando-secadora", "producto-aire-samsung-pared"}
def pool(m):
    d = SRC / m
    fs = [f for f in sorted(d.glob("*.webp")) if "logo" not in f.name and "autorizado" not in f.name and f.stem not in EXCLUIR] if d.exists() else []
    if m == "samsung":
        for p in sorted((ROOT / "st_img" / "panama").glob("*.webp")): fs.append(p)
        for p in sorted(glob.glob("/tmp/pan_img_work/img/*.webp")):
            n = os.path.basename(p)
            if re.search(r"-(s|m|400)\.webp$", n) or "logo" in n or "oval" in n: continue
            if re.match(r"(nevera|lavadora|secadora|lavavajillas|estufa|microondas|tecnico|horno|aire)", n): fs.append(pathlib.Path(p))
    # sin duplicados por contenido
    vis, out = set(), []
    for f in fs:
        h = hashlib.md5(f.read_bytes()).hexdigest()
        if h not in vis: vis.add(h); out.append(f)
    return out
POOLS = {m: pool(m) for m in BRANDS_ORDER}
KW = {"neveras": r"nevera|refriger|french|side-by-side|family", "lavadoras": r"lavadora", "secadoras": r"secadora", "aires": r"aire|windfree",
      "cocinas": r"estufa|horno|cocina", "lavavajillas": r"lavavajillas", "centro-lavado": r"centro-lavado|torre|washtower", "batidoras": r"batidora", "microondas": r"microondas", "_gente": r"tecnico|asesora|recepcion|equipo|saluda|agente|secretaria"}
import collections
USO = collections.Counter()
def copia(m, f):
    n = re.sub(r"[^a-z0-9.-]", "-", f.name.lower())
    d = OUT / "img" / m; d.mkdir(parents=True, exist_ok=True)
    if not (d / n).exists(): shutil.copyfile(f, d / n)
    return f"/img/{m}/{n}"
def alt_de(m, f, extra=""):
    t = re.sub(r"\.webp$", "", f.name); t = re.sub(r"[-_]+", " ", t)
    t = re.sub(r"\b(\d+|producto|banner|cutout|ge|1|2|3|4)\b", "", t).strip()
    return esc((t[:1].upper() + t[1:] + f" · {M[m]['nombre']} Panamá").strip())
def elegir(m, clave, cuantas=2, equipo=None):
    p = POOLS[m]
    if equipo is None: equipo = "_gente"
    if not p: return []
    cand = []
    if equipo and equipo in KW: cand = [f for f in p if re.search(KW[equipo], f.name)]
    rest = [f for f in p if f not in cand]
    h = lambda f: hashlib.md5((clave + f.name).encode()).hexdigest()
    orden = sorted(cand, key=lambda f: (USO[f], h(f))) + sorted(rest, key=lambda f: (USO[f], h(f)))
    res = orden[:cuantas]
    for f in res: USO[f] += 1
    return [(copia(m, f), alt_de(m, f)) for f in res]

PAL = {  # c principal, a botón, ab texto botón, bg fondo, soft tono claro, hd fin degradado héroe
 "samsung": ("#1428a0", "#0a84ff", "#fff", "#f1f5ff", "#e3ebff", "#0a1560"),
 "lg": ("#a50034", "#d4002f", "#fff", "#fbf3f5", "#f6e2e8", "#4a0017"),
 "whirlpool": ("#2d2d2d", "#ffc20e", "#1a1a1a", "#fbf9f1", "#fff1c2", "#111111"),
 "mabe": ("#0b5d8a", "#f28c1c", "#1a1a1a", "#eef6fa", "#d9ecf6", "#06344d"),
 "frigidaire": ("#c8102e", "#1f2a44", "#fff", "#fbf3f4", "#f8dde1", "#6e0719"),
 "electrolux": ("#011e41", "#0b66e4", "#fff", "#eff3f9", "#dbe5f3", "#000d1f"),
 "general-electric": ("#005eb8", "#00a3e0", "#fff", "#eef5fb", "#d7e8f6", "#003464"),
 "haceb": ("#00833e", "#f2b400", "#1a1a1a", "#eff8f2", "#d8eee0", "#004a22"),
 "kitchenaid": ("#9c1f2b", "#d4a24c", "#1a1a1a", "#fbf6f1", "#f3e5d6", "#4e0f16"),
}
DEF = ("#0b2a6f", "#16a34a", "#fff", "#f5f8fc", "#edf2fa", "#0a1b45")
# ---------------------------------------------------------------- CSS / JS
CSS = """
:root{--c:#0b2a6f;--a:#16a34a;--ab:#fff;--soft:#edf2fa;--hd:#0a1b45;--t:#10213f;--m:#5a6b85;--bg:#f5f8fc;--w:#fff;--r:16px;--sh:0 6px 24px rgba(11,42,111,.09)}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;font:16px/1.65 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:var(--t);background:var(--bg)}
img{max-width:100%;height:auto;display:block}a{color:var(--c)}h1,h2,h3{line-height:1.2;margin:0 0 .6rem;letter-spacing:-.01em}h1{font-size:clamp(1.7rem,4.5vw,2.7rem)}h2{font-size:clamp(1.3rem,3vw,1.8rem);margin-top:0}h3{font-size:1.1rem}
.w{max-width:1120px;margin:0 auto;padding:0 16px}.top{background:var(--hd);color:#fff;font-size:.85rem}.top .w{display:flex;gap:16px;justify-content:space-between;padding:7px 16px;flex-wrap:wrap}.top a{color:#fff;text-decoration:none}
header.h{background:var(--w);position:sticky;top:0;z-index:20;box-shadow:0 1px 0 #e3eaf4}.h .w{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:10px 16px}.logo{font-weight:800;color:var(--c);text-decoration:none;font-size:1.05rem;line-height:1.1}.logo small{display:block;font-weight:600;color:var(--m);font-size:.72rem}
.btn{display:inline-block;background:var(--a);color:var(--ab);text-decoration:none;font-weight:700;padding:12px 20px;border-radius:999px;border:0;cursor:pointer}.btn.o{background:transparent;color:var(--c);border:2px solid var(--c)}.hero .btn.o{color:#fff;border-color:#fff}.btn.s{padding:8px 14px;font-size:.9rem}
.chips{background:var(--w);border-bottom:1px solid #e3eaf4;overflow-x:auto;white-space:nowrap}.chips .w{display:flex;gap:8px;padding:8px 16px}.chips a{padding:7px 14px;border-radius:999px;background:var(--soft);text-decoration:none;font-weight:600;font-size:.9rem;color:var(--c)}.chips a.on{background:var(--c);color:#fff}
.hero{background:linear-gradient(135deg,var(--c),var(--hd));color:#fff;padding:36px 0}.hero .w{display:grid;gap:24px;align-items:center}.hero p{opacity:.94;font-size:1.08rem}.hero .bd{display:inline-block;background:rgba(255,255,255,.14);padding:5px 12px;border-radius:999px;font-size:.85rem;font-weight:600;margin-bottom:12px}.hero img{border-radius:var(--r);box-shadow:0 14px 40px rgba(0,0,0,.35);width:100%;aspect-ratio:4/3;object-fit:cover}
@media(min-width:860px){.hero .w{grid-template-columns:1.1fr .9fr}}
section.s{padding:30px 0}section.s.alt{background:var(--w)}.lead{color:var(--m);max-width:760px}
.rr{background:var(--soft);border-left:5px solid var(--a);padding:16px 18px;border-radius:12px;margin:0 0 18px}.rr b{display:block;margin-bottom:4px;color:var(--c)}
.g{display:grid;gap:16px}@media(min-width:700px){.g.c2{grid-template-columns:1fr 1fr}.g.c3{grid-template-columns:repeat(3,1fr)}}@media(min-width:1000px){.g.c4{grid-template-columns:repeat(4,1fr)}}
.card{background:var(--w);border-radius:var(--r);padding:18px;box-shadow:var(--sh)}.card.l{text-decoration:none;color:inherit;display:block;transition:.15s}.card.l:hover{transform:translateY(-3px)}.card .t{font-weight:800;color:var(--c)}.card small{color:var(--m)}
.tb{width:100%;border-collapse:collapse;background:var(--w);border-radius:var(--r);overflow:hidden;box-shadow:var(--sh)}.tb th,.tb td{padding:12px 14px;text-align:left;vertical-align:top;border-bottom:1px solid #e8eef7;font-size:.95rem}.tb th{background:var(--soft);color:var(--c)}
@media(max-width:699px){.tb thead{display:none}.tb tr{display:block;border-bottom:8px solid var(--bg)}.tb td{display:block;border:0;padding:6px 14px}.tb td:before{content:attr(data-l);display:block;font-size:.72rem;font-weight:700;text-transform:uppercase;color:var(--m)}}
.pasos{counter-reset:p;list-style:none;padding:0;margin:0;display:grid;gap:12px}@media(min-width:800px){.pasos{grid-template-columns:repeat(4,1fr)}}.pasos li{counter-increment:p;background:var(--w);padding:16px 16px 16px 58px;border-radius:var(--r);position:relative;box-shadow:var(--sh)}.pasos li:before{content:counter(p);position:absolute;left:14px;top:14px;width:32px;height:32px;border-radius:50%;background:var(--c);color:#fff;display:grid;place-items:center;font-weight:800}.pasos b{display:block}
details{background:var(--w);border-radius:12px;padding:14px 16px;margin-bottom:10px;box-shadow:var(--sh)}summary{cursor:pointer;font-weight:700}details[open] summary{margin-bottom:8px}
.pill{display:inline-block;padding:3px 10px;border-radius:999px;background:var(--soft);color:var(--c);font-weight:600;font-size:.85rem;margin:3px 4px 3px 0}.cb{font-weight:800;font-family:ui-monospace,monospace;color:#b42318}
.bc{font-size:.85rem;color:var(--m);padding:12px 0}.bc a{color:var(--m)}
.two{display:grid;gap:22px;align-items:center}@media(min-width:860px){.two{grid-template-columns:1fr 1fr}}.two img{border-radius:var(--r);box-shadow:var(--sh);width:100%;aspect-ratio:4/3;object-fit:cover}
footer{background:var(--hd);color:#cfd9ee;padding:34px 0 90px;font-size:.92rem}footer a{color:#fff}footer .g{gap:22px}footer h3{color:#fff}footer ul{list-style:none;padding:0;margin:0}footer li{margin:5px 0}
.fb{position:fixed;left:0;right:0;bottom:0;z-index:30;display:flex;gap:8px;padding:8px 10px;background:#fff;box-shadow:0 -4px 20px rgba(0,0,0,.12)}.fb a{flex:1;text-align:center;padding:12px;border-radius:12px;font-weight:700;text-decoration:none;color:#fff;background:var(--c)}.fb a.wa{background:var(--a);color:var(--ab)}@media(min-width:900px){.fb{display:none}footer{padding-bottom:34px}}
.wiz select{width:100%;padding:12px;border-radius:10px;border:1px solid #cfd9ee;font:inherit;margin:6px 0 12px}.res{display:none;background:#fff;border-left:5px solid var(--c);padding:16px;border-radius:12px;box-shadow:var(--sh)}
"""
JS_WIZ = """<script>(function(){var d=window.WIZ;if(!d)return;var e=document.getElementById('wq'),s=document.getElementById('ws'),r=document.getElementById('wr');
function eq(){s.innerHTML='<option value="">Elige el síntoma…</option>';(d[e.value]||[]).forEach(function(x,i){var o=document.createElement('option');o.value=i;o.textContent=x[0];s.appendChild(o)});r.style.display='none'}
e.addEventListener('change',eq);s.addEventListener('change',function(){var x=(d[e.value]||[])[s.value];if(!x){r.style.display='none';return}
r.innerHTML='<b>Causa más probable</b><p>'+x[1]+'</p><b>Qué revisamos en la visita</b><p>'+x[2]+'</p><a class="btn" target="_blank" rel="noopener" href="https://wa.me/"""+TELN+"""?text='+encodeURIComponent('Hola, mi '+e.options[e.selectedIndex].text+' '+window.WIZB+' presenta: '+x[0]+'. Necesito servicio técnico en Panamá.')+'">Pedir visita por WhatsApp</a>';r.style.display='block'});eq()})();</script>"""

# ---------------------------------------------------------------- plantilla
def wa(txt): return f"https://wa.me/{TELN}?text=" + re.sub(r"[ ]", "%20", txt).replace("¿", "%C2%BF").replace("á", "%C3%A1").replace("é", "%C3%A9").replace("í", "%C3%AD").replace("ó", "%C3%B3").replace("ú", "%C3%BA").replace("ñ", "%C3%B1").replace(",", "%2C")
def chips(actual):
    if actual:
        d = M[actual]; b = base(actual)
        it = [("Inicio", b)] + [(EQ[e][2].capitalize(), pathb(actual, "reparacion-" + EQ[e][0])) for e in d["equipos"]]
        if d["codigos"]: it.append(("Códigos de error", pathb(actual, "codigos-de-error")))
        it += [("Fallas", pathb(actual, "fallas")), ("Cobertura", pathb(actual, "cobertura")), ("Series y modelos", pathb(actual, "series-y-modelos")), ("Costos y garantía", pathb(actual, "cuanto-cuesta-la-reparacion")), ("Preguntas", pathb(actual, "preguntas-frecuentes")), ("Diagnóstico", pathb(actual, "diagnostico-por-sintoma"))]
    else:
        it = [("Inicio", "/"), ("Todas las marcas", "/marcas/"), ("Zonas", "/zonas/"), ("Blog", "/blog/"), ("Quiénes somos", "/nosotros/")]
    return '<nav class="chips" aria-label="Menú"><div class="w">' + "".join(f'<a href="{u}">{esc(t)}</a>' for t, u in it) + '</div></nav>'
def pie(marca=None):
    zon = '<div><h3>Zonas</h3><ul>' + "".join(f'<li><a href="/zonas/{z}/">{v[0]}</a></li>' for z, v in ZONAS.items()) + '</ul></div>'
    inf = ('<div><h3>Información</h3><ul><li><a href="/marcas/">Todas las marcas</a></li><li><a href="/nosotros/">Quiénes somos</a></li><li><a href="/blog/">Blog y guías</a></li><li><a href="/privacidad/">Política de privacidad</a></li><li><a href="/terminos/">Términos y condiciones</a></li><li><a href="/mapa-del-sitio/">Mapa del sitio</a></li></ul>'
           '<p><small>Servicio técnico independiente. Los nombres de marcas pertenecen a sus propietarios y se usan solo para indicar los equipos que reparamos.</small></p></div>')
    if marca:
        d = M[marca]; N = nom(marca)
        col = (f'<div><h3>Centro de Servicio Técnico {N} Panamá</h3><ul>' + "".join(f'<li><a href="{pathb(marca, "reparacion-" + EQ[e][0])}">{EQ[e][2].capitalize()} {N}</a></li>' for e in d["equipos"]) +
               (f'<li><a href="{pathb(marca, "codigos-de-error")}">Códigos de error</a></li>' if d["codigos"] else "") +
               f'<li><a href="{pathb(marca, "fallas")}">Fallas frecuentes</a></li><li><a href="{pathb(marca, "cobertura")}">Cobertura por zona</a></li><li><a href="{pathb(marca, "series-y-modelos")}">Series y modelos</a></li><li><a href="{pathb(marca, "cuanto-cuesta-la-reparacion")}">Costos y garantía</a></li><li><a href="{pathb(marca, "diagnostico-por-sintoma")}">Diagnóstico por síntoma</a></li></ul></div>')
        izq = f'<div><h3>{NOMBRE}</h3><p>Servicio técnico {N} a domicilio en Panamá.</p><p>{TEL}<br>Atención por WhatsApp.</p></div>'
    else:
        col = '<div><h3>Marcas</h3><ul>' + "".join(f'<li><a href="{"/" if m == "samsung" else "/" + m + "/"}">{M[m]["nombre"]} Panamá</a></li>' for m in BRANDS_ORDER) + '</ul></div>'
        izq = f'<div><h3>{NOMBRE}</h3><p>Servicio técnico de electrodomésticos a domicilio en Panamá. Cada marca tiene su propia sección.</p><p>{TEL}<br>Atención por WhatsApp.</p></div>'
    return ('<footer><div class="w"><div class="g c4">' + izq + col + zon + inf + '</div></div></footer>'
            f'<div class="fb"><a href="tel:+50769337976">Llamar</a><a class="wa" href="{wa("Hola, necesito servicio técnico en Panamá")}" target="_blank" rel="noopener">WhatsApp</a></div>')
LB = {"@type": "ProfessionalService", "@id": DOM + "/#negocio", "name": NOMBRE, "url": DOM + "/", "telephone": "+50769337976", "priceRange": "$$",
      "areaServed": [{"@type": "City", "name": "Ciudad de Panamá"}, {"@type": "AdministrativeArea", "name": "San Miguelito"}, {"@type": "City", "name": "Arraiján"}, {"@type": "City", "name": "La Chorrera"}, {"@type": "City", "name": "Colón"}],
      "address": {"@type": "PostalAddress", "addressLocality": "Panamá", "addressRegion": "Provincia de Panamá", "addressCountry": "PA"},
      "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "00:00", "closes": "23:59"}]}

def pagina(path, title, desc, h1, cuerpo, marca=None, hero=None, crumbs=None, ld=None, bd=None, prio="0.7", extra_js="", lead=None, noindex=False):
    """path: '/lg/reparacion-lavadoras/' ; cuerpo: html de secciones"""
    if len(title) > 62: title = title[:62].rsplit(" ", 1)[0].rstrip(" ,|-")
    if len(desc) > 158: desc = desc[:157].rsplit(" ", 1)[0].rstrip(" ,.;") + "…"
    color = M[marca]["color"] if marca else "#0b2a6f"
    url = DOM + path
    graf = [LB]
    if crumbs:
        graf.append({"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": DOM + u} for i, (n, u) in enumerate(crumbs)]})
    graf += ld or []
    bc = ""
    if crumbs and len(crumbs) > 1:
        bc = '<div class="w bc">' + " › ".join((f'<a href="{u}">{esc(n)}</a>' if i < len(crumbs) - 1 else esc(n)) for i, (n, u) in enumerate(crumbs)) + "</div>"
    himg = ""
    if hero: himg = f'<img src="{hero[0]}" alt="{hero[1]}" width="1024" height="768" fetchpriority="high" decoding="async">'
    heroh = (f'<section class="hero" style="--bc:{color}"><div class="w"><div><span class="bd">{esc(bd or NOMBRE)}</span><h1>{esc(h1)}</h1><p>{lead or esc(desc)}</p>'
             f'<p><a class="btn" href="{wa(f"Hola, necesito servicio técnico {M[marca]['nombre']} en Panamá" if marca else "Hola, necesito servicio técnico en Panamá")}" target="_blank" rel="noopener">Escribir por WhatsApp</a> <a class="btn o" href="tel:+50769337976">Llamar {TEL}</a></p></div>{himg}</div></section>')
    tags = "".join(f'<meta name="google-site-verification" content="{g}">' for g in GSC) if path == "/" else ""
    h = (f'<!doctype html><html lang="es-PA"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title>'
         f'<meta name="description" content="{esc(desc)}"><link rel="canonical" href="{url}"><link rel="alternate" hreflang="es-PA" href="{url}"><meta name="robots" content="{"noindex,follow" if noindex else "index,follow,max-image-preview:large,max-snippet:-1"}">{tags}'
         f'<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta property="og:locale" content="es_PA">'
         + (f'<meta property="og:image" content="{DOM}{hero[0]}">' if hero else '') +
         f'<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 64 64%27%3E%3Crect width=%2764%27 height=%2764%27 rx=%2714%27 fill=%27%230b2a6f%27/%3E%3Cpath d=%27M18 44l10-24 8 16 10-20%27 stroke=%27%23fff%27 stroke-width=%278%27 fill=%27none%27 stroke-linecap=%27round%27/%3E%3C/svg%3E">'
         f'<style>{CSS}</style><style>body{{--c:{PAL.get(marca, DEF)[0]};--a:{PAL.get(marca, DEF)[1]};--ab:{PAL.get(marca, DEF)[2]};--bg:{PAL.get(marca, DEF)[3]};--soft:{PAL.get(marca, DEF)[4]};--hd:{PAL.get(marca, DEF)[5]}}}</style><script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graf}, ensure_ascii=False)}</script></head><body>'
         f'<div class="top"><div class="w"><span>Atención a domicilio en Panamá · {TEL}</span><a href="{wa("Hola, necesito servicio técnico en Panamá")}" target="_blank" rel="noopener">WhatsApp</a></div></div>'
         f'<header class="h"><div class="w"><a class="logo" href="/">Centro de Servicio Técnico<small>Panamá</small></a><a class="btn s" href="{wa("Hola, necesito servicio técnico en Panamá")}" target="_blank" rel="noopener">Pedir visita</a></div></header>'
         + chips(marca) + heroh + bc + cuerpo + ('<!--cierre-->' + cierre(marca, path) + '<!--/cierre-->' if marca else '') + pie(marca) + extra_js + '</body></html>')
    f = OUT / path.lstrip("/") / "index.html" if path != "/" else OUT / "index.html"
    f.parent.mkdir(parents=True, exist_ok=True); f.write_text(h, encoding="utf-8")
    if not noindex: paginas.append((path, prio, marca))

EXT = {  # enlaces externos por marca: sitio oficial (solo informativo) y ACODECO para derechos del consumidor
 "samsung": ("Página del fabricante: Samsung (América Latina)", "https://www.samsung.com/latin/"),
 "lg": ("Página del fabricante: LG Panamá", "https://www.lg.com/pa/"),
 "whirlpool": ("Página del fabricante: Whirlpool", "https://www.whirlpool.com/"),
 "mabe": ("Página del fabricante: Mabe", "https://www.mabe.com.mx/"),
 "frigidaire": ("Página del fabricante: Frigidaire", "https://www.frigidaire.com/"),
 "electrolux": ("Página del fabricante: Electrolux", "https://www.electrolux.com/"),
 "general-electric": ("Página del fabricante: GE Appliances", "https://www.geappliances.com/"),
 "haceb": ("Página del fabricante: Haceb", "https://www.haceb.com/"),
 "kitchenaid": ("Página del fabricante: KitchenAid", "https://www.kitchenaid.com/"),
}
ACODECO = ("ACODECO: Autoridad de Protección al Consumidor de Panamá", "https://www.acodeco.gob.pa/")
ASEP = ("ASEP: Autoridad Nacional de los Servicios Públicos (electricidad y voltaje)", "https://www.asep.gob.pa/")
def cierre(m, path):
    d = M[m]; N = nom(m)
    pags = [(pathb(m, "reparacion-" + EQ[e][0]), f"Reparación de {EQ[e][2]} {N}") for e in d["equipos"]]
    if d["codigos"]: pags.append((pathb(m, "codigos-de-error"), f"Códigos de error {N}"))
    pags += [(pathb(m, "series-y-modelos"), f"Series y modelos {N}"), (pathb(m, "cuanto-cuesta-la-reparacion"), f"Cuánto cuesta y qué garantía tiene {N}"), (pathb(m, "preguntas-frecuentes"), f"Preguntas frecuentes {N}"), (pathb(m, "diagnostico-por-sintoma"), f"Diagnóstico por síntoma {N}")]
    pags = [(u, t) for u, t in pags if u != path]
    # los 6 más cercanos por posición, rotando según la página para repartir enlaces
    k = int(hashlib.md5(path.encode()).hexdigest(), 16) % max(1, len(pags))
    sel = (pags[k:] + pags[:k])[:6]
    inter = "".join(f'<a class="card l" href="{u}"><span class="t">{esc(t)}</span></a>' for u, t in sel)
    guias = ('<a class="card l" href="/blog/humedad-y-salitre-en-electrodomesticos-panama/"><span class="t">Humedad y salitre en tus electrodomésticos</span></a>'
             '<a class="card l" href="/blog/tormentas-electricas-y-voltaje-en-panama/"><span class="t">Tormentas y voltaje: protege las placas</span></a>'
             '<a class="card l" href="/zonas/"><span class="t">Zonas de cobertura en Panamá</span></a>')
    nm, url = EXT[m]
    externos = (f'<ul><li><a href="{url}" target="_blank" rel="noopener">{nm}</a> <small>(abre en otra pestaña; sitio del fabricante, no es nuestro)</small></li>'
                f'<li><a href="{ACODECO[1]}" target="_blank" rel="noopener">{ACODECO[0]}</a> <small>(derechos del consumidor en una reparación o compra)</small></li>'
                f'<li><a href="{ASEP[1]}" target="_blank" rel="noopener">{ASEP[0]}</a> <small>(los picos de voltaje dañan placas; infórmate sobre el servicio eléctrico)</small></li></ul>')
    busq = [(f"servicio técnico {N} Panamá", base(m)), (f"teléfono servicio técnico {N} Panamá", base(m)), (f"centro de servicio {N} cerca de mí", pathb(m, "cobertura")), (f"reparación {N} a domicilio", pathb(m, "fallas")), (f"repuestos {N} Panamá", pathb(m, "cuanto-cuesta-la-reparacion")), (f"códigos de error {N}", pathb(m, "codigos-de-error") if d["codigos"] else pathb(m, "fallas")), (f"mantenimiento {N}", base(m)), (f"garantía {N} Panamá", pathb(m, "cuanto-cuesta-la-reparacion"))]
    chips_b = "".join(f'<a class="pill" href="{u}">{esc(t)}</a>' for t, u in busq)
    return (sec(f"Búsquedas relacionadas con {N} en Panamá", chips_b)
            + sec(f"Más sobre {N} en Panamá", f'<div class="g c3">{inter}</div>', alt=True)
            + sec("Guías y zonas", f'<div class="g c3">{guias}</div>')
            + sec("Enlaces externos útiles", externos))
def sec(t, body, alt=False, lead=None):
    return f'<section class="s{" alt" if alt else ""}"><div class="w"><h2>{t}</h2>' + (f'<p class="lead">{lead}</p>' if lead else "") + body + '</div></section>'
def rr(txt): return f'<div class="rr"><b>Respuesta rápida</b>{txt}</div>'
def tabla(cab, filas):
    return '<table class="tb"><thead><tr>' + "".join(f"<th>{c}</th>" for c in cab) + '</tr></thead><tbody>' + "".join('<tr>' + "".join(f'<td data-l="{cab[i]}">{c}</td>' for i, c in enumerate(f)) + '</tr>' for f in filas) + '</tbody></table>'
def faq_html(faqs): return "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faqs)
def faq_ld(faqs): return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
PASOS = ('<ol class="pasos"><li><b>Escríbenos</b>Cuéntanos marca, modelo y qué hace el equipo.</li><li><b>Coordinamos</b>Acordamos día y franja en tu zona.</li>'
         '<li><b>Diagnóstico en casa</b>Revisamos el equipo y te explicamos la causa.</li><li><b>Reparación y prueba</b>Solo si tú apruebas el valor.</li></ol>')

def bajar(t):
    return t if (len(t) > 1 and t[1].isupper()) or t[:2] in ("OE", "IE", "UE") else t[0].lower() + t[1:]
def base(m): return "/" if m == "samsung" else f"/{m}/"
def pathb(m, s): return (f"/samsung/{s}/" if m == "samsung" else f"/{m}/{s}/")
def nom(m): return M[m]["nombre"]

# ---------------------------------------------------------------- páginas por marca
def eq_links(m):
    d = M[m]; out = []
    for e in d["equipos"]:
        s, sing, pl = EQ[e]
        out.append(f'<a class="card l" href="{pathb(m, "reparacion-" + s)}"><span class="t">Reparación de {pl} {nom(m)}</span><br><small>{esc(d["fallas"][e][0][0])}</small></a>')
    return '<div class="g c3">' + "".join(out) + '</div>'
def otras(m, actual):
    d = M[m]; items = [("fallas", f"Fallas frecuentes de {nom(m)}"), ("cobertura", f"Cobertura {nom(m)} por zona"), ("series-y-modelos", f"Series y modelos {nom(m)}"), ("cuanto-cuesta-la-reparacion", "Cuánto cuesta y garantía"), ("preguntas-frecuentes", "Preguntas frecuentes"), ("diagnostico-por-sintoma", "Diagnóstico por síntoma")]
    if d["codigos"]: items.insert(0, ("codigos-de-error", f"Códigos de error {nom(m)}"))
    return '<div class="g c3">' + "".join(f'<a class="card l" href="{pathb(m, s)}"><span class="t">{t}</span></a>' for s, t in items if s != actual) + "</div>"

def build_marca(m):
    d = M[m]; N = nom(m); crumbs0 = ([] if m == "samsung" else [("Marcas", "/marcas/")]) + [(f"Centro de Servicio Técnico {N} Panamá", base(m))]
    # --- hub
    hero = elegir(m, m + "hub", 1)
    teaser = "".join(f'<tr><td data-l="Equipo">{EQ[e][2].capitalize()}</td><td data-l="Falla frecuente">{esc(d["fallas"][e][0][0])}</td><td data-l="Causa probable">{esc(d["fallas"][e][0][1])}</td></tr>' for e in d["equipos"])
    mid = elegir(m, m + "hubmid", 1, d["equipos"][0])
    cuerpo = (sec(f"Centro de Servicio Técnico {N} Panamá: reparamos tus equipos {N} en casa",
                  rr(f"Reparamos {', '.join(EQ[e][2] for e in d['equipos'][:-1])} y {EQ[d['equipos'][-1]][2]} {N} a domicilio en Ciudad de Panamá, San Miguelito, Arraiján, La Chorrera y zonas cercanas. Escríbenos por WhatsApp con el modelo y la falla y coordinamos la visita.") + f"<p>{esc(d['origen'])}</p>")
              + sec(f"Equipos {N} que atendemos", eq_links(m), alt=True)
              + sec(f"Fallas más frecuentes en {N}", f'<table class="tb"><thead><tr><th>Equipo</th><th>Falla frecuente</th><th>Causa probable</th></tr></thead><tbody>{teaser}</tbody></table>')
              + sec(f"Lo que más buscan sobre {N} en Panamá", '<div class="g c2">' + "".join(f'<a class="card l" href="{pathb(m, "falla-" + slug(f[0]))}"><span class="t">{esc(EQ[e][1].capitalize())} {N} {esc(bajar(f[0]).rstrip("."))}</span></a>' for e in d["equipos"] for f in d["fallas"][e][:2]) + f'</div><p><a href="{pathb(m, "fallas")}">Ver todas las fallas de {N}</a> · <a href="{pathb(m, "cobertura")}">Cobertura por zona</a></p>', alt=True)
              + sec(f"Líneas y tecnologías {N} que conocemos", "".join(f'<span class="pill">{esc(x)}</span>' for x in d["lineas"]) + (f'<div class="two" style="margin-top:18px"><p>{esc(d["tech"][d["equipos"][0]])}</p><img loading="lazy" src="{mid[0][0]}" alt="{mid[0][1]}" width="1024" height="768"></div>' if mid else ""), alt=True)
              + sec(f"Mantenimiento recomendado para {N}", "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in d["mantenimiento"]) + "</ul>")
              + sec("Cómo trabajamos", PASOS, alt=True)
              + sec(f"Todo sobre el servicio {N}", otras(m, ""), alt=True)
              + sec(f"Preguntas frecuentes sobre {N} en Panamá", faq_html(d["faq"])))
    path = "/" if m == "samsung" else base(m)
    t = f"Centro de Servicio Técnico {N} Panamá | A domicilio" if m != "general-electric" else f"Centro de Servicio Técnico {N} Panamá"
    ld = [faq_ld(d["faq"]), {"@type": "Service", "name": f"Servicio técnico {N} en Panamá", "provider": {"@id": DOM + "/#negocio"}, "areaServed": "Panamá", "serviceType": f"Reparación de electrodomésticos {N}"}]
    pagina(path, t, f"Centro de servicio técnico {N} en Panamá: reparación a domicilio de {', '.join(EQ[e][2] for e in d['equipos'][:3])} y más. Diagnóstico en casa y atención por WhatsApp.",
           f"Centro de Servicio Técnico {N} Panamá", cuerpo, m, hero[0] if hero else None, ([] if m == "samsung" else [("Marcas", "/marcas/"), (f"{N} Panamá", base(m))]) or [("Centro de Servicio Técnico Samsung Panamá", "/")], ld,
           bd=f"{N} · Panamá", prio="1.0" if m == "samsung" else "0.9",
           lead=f"Reparación a domicilio de equipos {N} en Panamá. Diagnóstico en tu casa, explicación clara de la falla y atención por WhatsApp.")
    # --- por equipo
    for e in d["equipos"]:
        s, sing, pl = EQ[e]; fl = d["fallas"][e]
        imgs = elegir(m, m + e, 2, e)
        h = imgs[0] if imgs else None; h2 = imgs[1] if len(imgs) > 1 else None
        cod = d["codigos"].get("Lavadoras" if e in ("lavadoras", "centro-lavado") else "Refrigeradoras" if e == "neveras" else "_", [])
        sec_cod = sec(f"Códigos de error frecuentes en {pl} {N}", tabla(["Código", "Qué suele indicar"], [(f'<span class="cb">{c}</span>', esc(t)) for c, t in cod]) + f'<p><a href="{pathb(m, "codigos-de-error")}">Ver todos los códigos {N}</a></p>', alt=True) if cod else ""
        resp = rr(f"Si tu {sing} {N} " + bajar(fl[0][0]).rstrip(".") + f", lo más probable es: {bajar(fl[0][1])} Haremos la revisión en tu casa y te diremos el valor antes de reparar.")
        faq_e = [(q, r) for q, r in d["faq"]][:3]
        cuerpo = (sec(f"Reparación de {pl} {N} en Panamá", resp + f"<p>{esc(d['tech'][e])}</p>")
                  + sec(f"Fallas de {pl} {N} que más vemos", tabla(["Lo que notas", "Causa probable", "Qué revisamos"], [(f"<b>{esc(a)}</b>", esc(b), esc(c)) for a, b, c in fl]), alt=True)
                  + (sec(f"Antes de la visita: tu {sing} {N}", "" + (f'<div class="two" style="margin-top:20px"><div><h3>Antes de llamar</h3><p>{esc(d["etiqueta"].get(e, "Busca la etiqueta con el número de modelo y serie en el equipo."))}</p><p>Con una foto de esa etiqueta, el diagnóstico por WhatsApp es mucho más preciso.</p></div><img loading="lazy" src="{h2[0]}" alt="{h2[1]}" width="1024" height="768"></div>' if h2 else "")))
                  + sec_cod
                  + sec(f"Preguntas sobre {pl} {N}", faq_html(faq_e), alt=not bool(sec_cod))
                  )
        pagina(pathb(m, "reparacion-" + s), f"Reparación de {pl} {N} en Panamá | Centro de Servicio", f"Reparación de {pl} {N} en Panamá a domicilio: fallas frecuentes, causas probables y qué revisamos. Diagnóstico en casa y atención por WhatsApp.",
               f"Reparación de {pl} {N} en Panamá", cuerpo, m, h, crumbs0 + [(f"Reparación de {pl}", pathb(m, "reparacion-" + s))],
               [faq_ld(faq_e), {"@type": "Service", "name": f"Reparación de {pl} {N}", "provider": {"@id": DOM + "/#negocio"}, "areaServed": "Panamá"}], bd=f"{N} · {pl.capitalize()}", prio="0.8",
               lead=f"Qué le pasa a tu {sing} {N}, por qué ocurre y cómo lo revisamos en tu casa en Panamá.")
    # --- códigos
    if d["codigos"]:
        bloques = "".join(f'<h3>{g}</h3>' + tabla(["Código", "Qué suele indicar"], [(f'<span class="cb">{c}</span>', esc(t)) for c, t in L]) for g, L in d["codigos"].items())
        pagina(pathb(m, "codigos-de-error"), f"Códigos de error {N}: qué significan | Panamá", f"Lista de códigos de error {N} más comunes en lavadoras y refrigeradoras, con qué suele indicar cada uno y cuándo llamar al técnico.",
               f"Códigos de error {N}: qué significa cada uno", sec(f"Códigos de error {N}", rr(f"Los códigos de error {N} indican qué sistema del equipo detectó el problema. Muchos se resuelven limpiando filtros o revisando llaves; si el código vuelve tras apagar y encender, hace falta una revisión.") + bloques + "<p><small>Esta lista es orientativa. El significado exacto puede variar según el modelo y el año; confirma siempre con el manual de tu equipo.</small></p>") + sec("Equipos", eq_links(m), alt=True),
               m, elegir(m, m + "cod", 1)[0] if POOLS[m] else None, crumbs0 + [("Códigos de error", pathb(m, "codigos-de-error"))], bd=f"{N} · Códigos", prio="0.8",
               lead=f"Qué significan los códigos de error más frecuentes de {N} y qué hacer antes de llamar.")
    # --- series y modelos
    tb = "".join(f"<h3>{EQ[e][2].capitalize()} {N}</h3><p>{esc(d['tech'][e])}</p>" for e in d["equipos"])
    et = tabla(["Equipo", "Dónde está la etiqueta con el modelo"], [(EQ[e][2].capitalize(), esc(t)) for e, t in d["etiqueta"].items()])
    pagina(pathb(m, "series-y-modelos"), f"Series y modelos {N}: cómo identificar el tuyo", f"Líneas {N} más comunes en Panamá, cómo funciona cada tecnología y dónde encontrar el número de modelo de tu equipo.",
           f"Series, modelos y tecnologías {N}", sec(f"Líneas {N}", rr(f"{N} agrupa sus equipos en líneas como {', '.join(d['lineas'][:4])}. Conocer la tuya ayuda a pedir el repuesto correcto y a describir la falla con precisión.") + "".join(f'<span class="pill">{esc(x)}</span>' for x in d["lineas"]) + f"<p>{esc(d['modelo_ej'])}</p>") + sec("Cómo funciona cada equipo", tb, alt=True) + sec("Dónde encontrar el número de modelo", et + "<p>Con una foto de esa etiqueta puedes escribirnos por WhatsApp y adelantamos el diagnóstico.</p>"),
           m, elegir(m, m + "ser", 1)[0], crumbs0 + [("Series y modelos", pathb(m, "series-y-modelos"))], bd=f"{N} · Modelos", lead=f"Origen, líneas y tecnologías de {N}, y cómo leer la etiqueta del equipo.")
    comp = {"samsung": "el compresor Digital Inverter y la placa inverter", "lg": "el compresor inverter o lineal y la placa inverter", "whirlpool": "el compresor, el control y la transmisión de la lavadora", "mabe": "el compresor y la transmisión de la lavadora", "frigidaire": "la tarjeta de control y el compresor", "electrolux": "la placa inverter y el compresor", "general-electric": "la tarjeta de control y el sistema del dispensador", "haceb": "el compresor y la tarjeta", "kitchenaid": "el motor y la caja de engranes"}[m]
    # --- cuánto cuesta
    def nivel(txt):
        t = txt.lower()
        if re.search(r"placa|tarjeta|compresor|inverter|bobina|magnetr|transmisi|rodamiento|control", t): return "Alto"
        if re.search(r"filtro|limpi|ajuste|manguera|bujía|bujia|empaque|sello|llave|carga|grasa", t): return "Bajo"
        return "Medio"
    filas = []
    for e in d["equipos"]:
        for a_, b_, c_ in d["fallas"][e][:3]:
            filas.append((EQ[e][2].capitalize(), esc(a_), esc(b_), nivel(b_)))
    pagina(pathb(m, "cuanto-cuesta-la-reparacion"), f"Cuánto cuesta y qué garantía tiene {N} en Panamá", f"Qué fallas de equipos {N} suelen costar poco, cuáles más y por qué: tabla por equipo con el nivel de costo relativo y cómo se confirma el valor antes de reparar.",
           f"Cuánto cuesta la reparación de equipos {N} en Panamá",
           sec(f"Costo relativo de cada falla en {N}", rr(f"El costo de reparar un equipo {N} depende sobre todo de la pieza que falló. Un filtro o un ajuste cuesta mucho menos que una placa electrónica o un compresor. Confirmamos el valor por escrito después del diagnóstico y antes de reparar.")
               + tabla(["Equipo", "Falla", "Causa probable", "Costo relativo"], filas) + "<p><small>El nivel (Bajo, Medio o Alto) es una guía comparativa entre fallas, no un precio. El valor real se confirma tras el diagnóstico.</small></p>")
           + sec(f"Garantía de {N}: de fábrica y de la reparación", f"<p>{esc(d['garantia'])}</p><p>En {N} pesan más en una garantía {comp}. La garantía de fábrica no cubre golpes, líquidos ni picos de voltaje. Al reparar, te damos por escrito qué pieza se cambió y por cuánto tiempo respondemos por ella.</p><p>{N} es una marca de {d['pais']}: filtros, bombas, sensores y empaques suelen conseguirse en Panamá, y las placas o compresores de líneas como {', '.join(d['lineas'][:3])} pueden requerir pedido; te avisamos el plazo antes de empezar.</p>")
           + sec(f"Qué cambia el valor en equipos {N}", f"<ul><li>Si el repuesto de tu {N} está en Panamá o hay que pedirlo a {d['pais']} u otro país.</li><li>Antigüedad: en un equipo de muchos años se compara reparar con reemplazar.</li></ul>", alt=True)
           + sec("Equipos", eq_links(m)), m, elegir(m, m + "cost", 1)[0], crumbs0 + [("Cuánto cuesta", pathb(m, "cuanto-cuesta-la-reparacion"))], bd=f"{N} · Costos", lead=f"De qué depende el costo de reparar cada falla de tu equipo {N}.")
    # --- preguntas
    PF = list(d["faq"]) + [(f"¿Por qué mi {EQ[e][1]} {N} {bajar(f[0]).rstrip('.')}?", f"{f[1]} {f[2]}") for e in d["equipos"] for f in d["fallas"][e][:2]] + [(f"¿Cómo pido una visita para mi equipo {N}?", "Escribe por WhatsApp con el modelo, la falla y tu zona. Coordinamos día y franja horaria.")]
    pagina(pathb(m, "preguntas-frecuentes"), f"Preguntas frecuentes sobre {N} en Panamá", f"Respuestas a las preguntas más comunes sobre servicio técnico {N} en Panamá: cobertura, tiempos, garantía y cómo pedir una visita.",
           f"Preguntas frecuentes sobre servicio técnico {N}",
           sec("Preguntas frecuentes", faq_html(PF)),
           m, elegir(m, m + "faq", 1)[0], crumbs0 + [("Preguntas frecuentes", pathb(m, "preguntas-frecuentes"))], [faq_ld(PF)], bd=f"{N} · Preguntas", lead=f"Respuestas claras sobre el servicio técnico {N} en Panamá.", prio="0.6")
    # --- diagnóstico
    wiz = {e: [[a, b, c] for a, b, c in d["fallas"][e]] for e in d["equipos"]}
    opts = "".join(f'<option value="{e}">{EQ[e][1]}</option>' for e in d["equipos"])
    js = f'<script>window.WIZ={json.dumps(wiz, ensure_ascii=False)};window.WIZB={json.dumps(N)};</script>' + JS_WIZ
    pagina(pathb(m, "diagnostico-por-sintoma"), f"Diagnóstico por síntoma {N}: qué le pasa a tu equipo", f"Elige tu equipo {N} y el síntoma que notas para ver la causa más probable y qué revisaría un técnico. Herramienta gratuita.",
           f"Diagnóstico por síntoma de equipos {N}",
           sec("¿Qué le pasa a tu equipo?", rr("Elige el equipo y lo que notas. Te mostramos la causa más probable según las fallas que vemos en equipos de esta marca en Panamá.") + f'<div class="wiz card"><label>Equipo</label><select id="wq">{opts}</select><label>Síntoma</label><select id="ws"></select><div class="res" id="wr"></div></div><p><small>Es una guía orientativa. La causa se confirma con pruebas en el equipo.</small></p>'),
           m, elegir(m, m + "diag", 1)[0], crumbs0 + [("Diagnóstico por síntoma", pathb(m, "diagnostico-por-sintoma"))], bd=f"{N} · Diagnóstico", extra_js=js, lead=f"Herramienta gratuita para entender qué le pasa a tu equipo {N}.")


import unicodedata
def slug(t):
    t = unicodedata.normalize("NFKD", t.lower()).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:70]
def consejo(sint, causa):
    t = (sint + " " + causa).lower()
    if re.search(r"quemado|chispa|humo|gas\b|fuga de gas", t): return ("Apaga el equipo, desconéctalo y no lo vuelvas a usar hasta que lo revise un técnico. Si huele a gas, cierra la llave del gas y ventila el lugar.", "Esta falla puede ser peligrosa: no la pruebes de nuevo.")
    if re.search(r"gotea|fuga|agua en el piso|filtra", t): return ("Cierra la llave de paso del agua, seca el piso para evitar resbalones y revisa que las mangueras no estén dobladas ni flojas.", "Si el agua llega a enchufes o a la parte eléctrica, desconecta el equipo antes de tocar nada.")
    if re.search(r"drena|desag|se queda con agua|no desagua", t): return ("Revisa que la manguera de desagüe no esté doblada y que el desagüe de la pared no esté tapado. Si tu modelo tiene filtro de bomba accesible, límpialo con el equipo apagado y desconectado.", "Evita forzar ciclos de centrifugado con el tambor lleno de agua.")
    if re.search(r"ruido|zumbido|chasquido|rechin|golpe|vibra", t): return ("Comprueba que el equipo esté nivelado, que no toque la pared ni otros muebles y que no haya objetos sueltos dentro del tambor o detrás de la parte trasera.", "Si el ruido es metálico y fuerte, deja de usarlo: seguir puede dañar más piezas.")
    if re.search(r"no enfr|enfr|hielo|escarcha|congel", t): return ("Verifica que las rejillas de ventilación no estén tapadas, que la puerta cierre bien y que la temperatura no esté en el mínimo. Evita meter comida caliente.", "Si hay hielo acumulado, no lo raspes con objetos metálicos.")
    if re.search(r"calienta|no seca|seca lento|resisten", t): return ("Limpia el filtro de pelusa o el condensador, revisa que el ducto de salida no esté aplastado y no sobrecargues el tambor.", "No uses el equipo si se sobrecalienta o huele a quemado.")
    if re.search(r"no enciende|no responde|pantalla|c[oó]digo|error|se apaga|reinicia|botones", t): return ("Prueba el tomacorriente con otro aparato, revisa el breaker y desconecta el equipo cinco minutos antes de volver a encenderlo. Anota el código o el mensaje que aparece.", "Si el problema ocurre después de una tormenta o un apagón, puede ser la placa: no insistas con reinicios repetidos.")
    return ("Anota cuándo empezó, qué estabas haciendo y si aparece algún código o ruido. Con una foto de la etiqueta del modelo, el diagnóstico por WhatsApp es más preciso.", "Evita abrir el equipo si no eres técnico: hay partes con corriente y piezas que cortan.")
def oracion(t, k):
    ps = [x.strip() for x in re.split(r"(?<=[.])\s+", t) if x.strip()]
    return " ".join(ps[k % len(ps): k % len(ps) + 2]) if ps else t
def variantes(N, sing, sint):
    s_ = bajar(sint).rstrip(".")
    return [f"{sing} {N} {s_}", f"por qué mi {sing} {N} {s_}", f"reparar {sing} {N} {s_}", f"{N} {sing} {s_} Panamá", f"técnico {N} {sing} Panamá"]
SINT = {}   # marca -> lista (equipo, slug, sintoma, causa, revisamos)
def cierre_sint(m, e, sl):
    d = M[m]; N = nom(m)
    L = []
    for e2 in d["equipos"]:
        for i, (a, b, c) in enumerate(d["fallas"][e2]):
            L.append((e2, slug(a), a, b, c))
    SINT[m] = L
def build_sintomas(m):
    d = M[m]; N = nom(m); crumbs0 = ([] if m == "samsung" else [("Marcas", "/marcas/")]) + [(f"Centro de Servicio Técnico {N} Panamá", base(m))]
    cierre_sint(m, None, None)
    L = SINT[m]
    for k, (e, sl, a, b, c) in enumerate(L):
        sing = EQ[e][1]; pl = EQ[e][2]; N_ = N
        hint, aviso = consejo(a, b)
        # otras fallas del mismo equipo (enlaces internos)
        hermanas = [x for x in L if x[0] == e and x[1] != sl][:4] or [x for x in L if x[1] != sl][:4]
        hermanas_html = "".join(f'<a class="card l" href="{pathb(m, "falla-" + x[1])}"><span class="t">{esc(sing.capitalize())} {N_}: {esc(bajar(x[2]).rstrip("."))}</span></a>' for x in hermanas)
        cod = d["codigos"].get("Lavadoras" if e in ("lavadoras", "centro-lavado") else "Refrigeradoras" if e == "neveras" else "_", [])
        cod_html = (sec(f"Códigos {N_} relacionados", tabla(["Código", "Qué suele indicar"], [(f'<span class="cb">{x}</span>', esc(y)) for x, y in cod[:6]]) + f'<p><a href="{pathb(m, "codigos-de-error")}">Ver todos los códigos de error {N_}</a></p>', alt=True) if cod else "")
        im = elegir(m, m + sl, 2, e)
        h1 = f"Mi {sing} {N_} {bajar(a).rstrip('.')}: causas y qué hacer"
        titulo = f"{sing.capitalize()} {N_} {bajar(a).rstrip('.')} | Causa y solución"
        faq = [(f"¿Puedo seguir usando mi {sing} {N_} si {bajar(a).rstrip('.')}?", aviso),
               (f"¿Qué revisa el técnico cuando mi {sing} {N_} {bajar(a).rstrip('.')}?", c),
               (f"¿Cuánto cuesta arreglar esto en una {sing} {N_}?", f"Depende de la pieza. En este caso la causa más probable es: {bajar(b)} Después del diagnóstico te damos el valor por escrito antes de reparar.")]
        busc = "".join(f'<span class="pill">{esc(v)}</span>' for v in variantes(N_, sing, a))
        cuerpo = (sec(f"{sing.capitalize()} {N_} {bajar(a).rstrip('.')}", rr(f"{b} {hint}") + f"<h3>Causa más probable</h3><p>{esc(b)}</p><h3>Qué revisamos en tu casa</h3><p>{esc(c)}</p>")
                  + sec("Qué puedes hacer tú antes de llamar", f"<p>{esc(hint)}</p><p><b>Importante:</b> {esc(aviso)}</p>", alt=True)
                  + sec(f"Cómo funciona esta parte de tu {sing} {N_}", f"<p>{esc(oracion(d['tech'][e], k))}</p>" + (f'<img loading="lazy" src="{im[1][0]}" alt="{im[1][1]}" width="1024" height="768" style="border-radius:16px;margin-top:12px;max-width:min(560px,100%);height:auto">' if len(im) > 1 else ""))
                  + cod_html
                  + sec(f"Otras fallas de {pl} {N_}", f'<div class="g c2">{hermanas_html}</div><p><a href="{pathb(m, "reparacion-" + EQ[e][0])}">Ver toda la reparación de {pl} {N_}</a></p>', alt=not bool(cod_html))
                  + sec("Preguntas frecuentes", faq_html(faq))
                  + sec("Cómo lo buscan en Google", f"<p>Estas son algunas formas en que la gente describe este problema:</p>{busc}", alt=True))
        pagina(pathb(m, "falla-" + sl), titulo, f"{sing.capitalize()} {N_} {bajar(a).rstrip('.')}: causa más probable, qué revisa el técnico y qué puedes hacer antes de llamar. Servicio a domicilio en Panamá.",
               h1, cuerpo, m, im[0] if im else None, crumbs0 + [(f"Reparación de {pl}", pathb(m, "reparacion-" + EQ[e][0])), (a[:45], pathb(m, "falla-" + sl))],
               [faq_ld(faq), {"@type": "Service", "name": f"Reparación: {sing} {N_} {bajar(a).rstrip('.')}", "provider": {"@id": DOM + "/#negocio"}, "areaServed": "Panamá"}], bd=f"{N_} · {pl.capitalize()}", prio="0.7",
               lead=f"Causa probable, qué se revisa y qué puedes hacer antes de pedir la visita.")
    # índice de fallas
    grupos = ""
    for e in d["equipos"]:
        items = "".join(f'<a class="card l" href="{pathb(m, "falla-" + x[1])}"><span class="t">{esc(x[2])}</span><br><small>{esc(x[3][:90])}</small></a>' for x in L if x[0] == e)
        grupos += sec(f"Fallas de {EQ[e][2]} {N}", f'<div class="g c2">{items}</div>', alt=(d["equipos"].index(e) % 2 == 1))
    pagina(pathb(m, "fallas"), f"Fallas frecuentes de equipos {N} en Panamá", f"Todas las fallas frecuentes de equipos {N} en Panamá, con su causa probable: refrigeradoras, lavadoras y más. Elige tu síntoma.",
           f"Fallas frecuentes de equipos {N}", sec("Elige tu síntoma", rr(f"Aquí están las fallas que más vemos en equipos {N} en Panamá. Entra a la tuya para ver la causa más probable, qué puedes revisar y qué hace el técnico.")) + grupos, m,
           elegir(m, m + "fallas", 1)[0] if POOLS[m] else None, crumbs0 + [("Fallas frecuentes", pathb(m, "fallas"))], bd=f"{N} · Fallas", prio="0.8", lead=f"Todas las fallas frecuentes de {N} en un solo lugar.")

CLIMA = {"ciudad-de-panama": "la humedad constante y el salitre en edificios cercanos a la bahía", "san-miguelito": "los picos de voltaje en sectores de alta densidad y los apagones intermitentes", "arraijan": "los voltajes irregulares en urbanizaciones nuevas y el polvo de obra",
         "la-chorrera": "el calor y el polvo en urbanizaciones en crecimiento", "costa-del-este": "los edificios altos con aires de alta eficiencia y alta humedad frente al mar", "tocumen-y-24-de-diciembre": "el calor intenso y los cortes de energía por tormentas",
         "panama-oeste": "las urbanizaciones nuevas con equipos aún en garantía y el calor", "colon": "el salitre costero y la corrosión de condensadores y placas"}
def build_zonas_marca(m):
    d = M[m]; N = nom(m); crumbs0 = ([] if m == "samsung" else [("Marcas", "/marcas/")]) + [(f"Centro de Servicio Técnico {N} Panamá", base(m))]
    items = ""
    for z, (zn, barrios, rasgo) in ZONAS.items():
        e0 = d["equipos"][0]; e1 = d["equipos"][min(1, len(d["equipos"]) - 1)]
        f0 = d["fallas"][e0][0]; f1 = d["fallas"][e1][0]
        eqs = "".join(f'<a class="card l" href="{pathb(m, "reparacion-" + EQ[e][0])}"><span class="t">{EQ[e][2].capitalize()} {N}</span></a>' for e in d["equipos"][:4])
        tres = [d["fallas"][e][0] for e in d["equipos"][:3]]
        det = "".join(f"<li><b>{esc(EQ[e][2].capitalize())}:</b> {esc(bajar(f[0]).rstrip('.'))}. Causa probable: {esc(bajar(f[1]))}</li>" for e, f in zip(d["equipos"][:3], tres))
        linksf = "".join(f'<a class="card l" href="{pathb(m, "falla-" + slug(f[0]))}"><span class="t">{esc(EQ[e][1].capitalize())} {N} {esc(bajar(f[0]).rstrip("."))}</span></a>' for e, f in zip(d["equipos"][:4], [d["fallas"][e][0] for e in d["equipos"][:4]]))
        cuerpo = (sec(f"Servicio técnico {N} en {zn}", rr(f"Reparamos equipos {N} a domicilio en {zn}: {', '.join(EQ[e][2] for e in d['equipos'][:-1])} y {EQ[d['equipos'][-1]][2]}. Escribe por WhatsApp con tu barrio, el modelo y la falla.") + f"<p><b>Sectores:</b> {esc(', '.join(barrios.split(', ')[:6]))} y alrededores.</p>")
                  + sec(f"Qué vemos en {zn} con equipos {N}", f"<p>En {zn} pesan {CLIMA[z]}. Con {N} lo que más se reporta es:</p><ul>{det}</ul><p>{esc(oracion(d['tech'][e0], len(z)))}</p><p>Líneas {N} que atendemos: {', '.join(esc(x) for x in d['lineas'][:5])}.</p>", alt=True)
                  + sec(f"Fallas {N} frecuentes", f'<div class="g c2">{linksf}</div>')
                  + sec(f"Equipos {N} que reparamos en {zn}", f'<div class="g c2">{eqs}</div>', alt=True))
        pagina(pathb(m, "servicio-tecnico-" + z), f"Servicio técnico {N} en {zn} | Panamá", f"Servicio técnico {N} a domicilio en {zn}, Panamá: reparación de {', '.join(EQ[e][2] for e in d['equipos'][:3])} y más. Atención por WhatsApp.",
               f"Servicio técnico {N} en {zn}", cuerpo, m, elegir(m, m + z, 1)[0], crumbs0 + [("Cobertura", pathb(m, "cobertura")), (zn, pathb(m, "servicio-tecnico-" + z))],
               [{"@type": "Service", "name": f"Servicio técnico {N} en {zn}", "provider": {"@id": DOM + "/#negocio"}, "areaServed": {"@type": "Place", "name": zn}}], bd=f"{N} · {zn}", prio="0.7", lead=f"Visitas a domicilio para equipos {N} en {zn}.")
        items += f'<a class="card l" href="{pathb(m, "servicio-tecnico-" + z)}"><span class="t">Servicio técnico {N} en {zn}</span><br><small>Con {N}, aquí pesan {CLIMA[z]}: {esc(EQ[e0][2])} y {esc(EQ[e1][2])} son lo más reportado.</small></a>'
    pagina(pathb(m, "cobertura"), f"Cobertura del servicio técnico {N} en Panamá", f"Zonas de Panamá donde damos servicio técnico a domicilio para equipos {N}: Ciudad de Panamá, San Miguelito, Arraiján, La Chorrera, Colón y más.",
           f"Cobertura del servicio técnico {N} en Panamá", sec("Dónde atendemos equipos " + N, rr(f"Visitamos nueve zonas de Panamá para reparar equipos {N}: {', '.join(EQ[e][2] for e in d['equipos'])}. Cada zona tiene su página con lo que más vemos allí en {N}.") + f'<div class="g c2">{items}</div>') + sec(f"Líneas {N} que atendemos", "".join(f'<span class="pill">{esc(x)}</span>' for x in d["lineas"]) + f"<p>{esc(d['origen'])}</p>", alt=True), m, elegir(m, m + "cob", 1)[0], crumbs0 + [("Cobertura", pathb(m, "cobertura"))], bd=f"{N} · Cobertura", prio="0.7", lead=f"Zonas de Panamá con visita a domicilio para equipos {N}.", noindex=True)

# ---------------------------------------------------------------- zonas, institucionales, blog
def build_sitio():
    for z, (n, barrios, rasgo) in ZONAS.items():
        pagina(f"/zonas/{z}/", f"Servicio técnico de electrodomésticos en {n} | Panamá", f"Servicio técnico a domicilio en {n}, Panamá, para refrigeradoras, lavadoras, secadoras, aires acondicionados y cocinas de las principales marcas.",
               f"Servicio técnico de electrodomésticos en {n}", sec(f"Cobertura en {n}", rr(f"Visitamos {n} para reparar refrigeradoras, lavadoras, secadoras, aires y cocinas. Escríbenos por WhatsApp con tu barrio y coordinamos la visita.") + f"<p><b>Zonas que cubrimos:</b> {esc(barrios)}.</p><p>{esc(rasgo)}</p>")
               + sec("Elige tu marca", '<p><a class="btn" href="/marcas/">Ver todas las marcas</a></p>', alt=True), None, None, [("Inicio", "/"), ("Zonas", "/zonas/"), (f"{n}", f"/zonas/{z}/")], bd=f"{n} · Panamá", lead=f"Visitas a domicilio en {n} para tus electrodomésticos.", prio="0.7")
    pagina("/zonas/", "Zonas de cobertura | Servicio técnico en Panamá", "Zonas de Panamá donde damos servicio técnico a domicilio: Ciudad de Panamá, San Miguelito, Arraiján, La Chorrera, Colón y más.", "Zonas de cobertura en Panamá",
           sec("Dónde atendemos", '<div class="g c3">' + "".join(f'<a class="card l" href="/zonas/{z}/"><span class="t">{v[0]}</span><br><small>{esc(v[1][:90])}…</small></a>' for z, v in ZONAS.items()) + "</div>"), None, None, [("Inicio", "/"), ("Zonas", "/zonas/")], prio="0.6")
    pagina("/marcas/", "Todas las marcas | Centro de Servicio Técnico Panamá", "Marcas de electrodomésticos que reparamos en Panamá. Cada marca tiene su propia sección con fallas, códigos y tecnologías específicas.", "Marcas que atendemos en Panamá",
           sec("Elige tu marca", '<div class="g c3">' + "".join(f'<a class="card l" href="{base(m)}" style="border-top:5px solid {PAL[m][0] if PAL[m][0] != "#2d2d2d" else PAL[m][1]}"><span class="t">Centro de Servicio Técnico {nom(m)} Panamá</span><br><small>{", ".join(EQ[e][2] for e in M[m]["equipos"])}</small></a>' for m in BRANDS_ORDER) + "</div>"), None, None, [("Inicio", "/"), ("Marcas", "/marcas/")], bd="Marcas", lead="Cada marca tiene su propia sección. Elige la tuya.", prio="0.8")
    pagina("/nosotros/", f"Quiénes somos | {NOMBRE}", "Quiénes somos: un servicio técnico independiente de electrodomésticos en Panamá, con secciones separadas por marca.", "Quiénes somos",
           sec("Un servicio técnico independiente en Panamá", "<p>Somos un servicio técnico de electrodomésticos que atiende a domicilio en Panamá. Reparamos refrigeradoras, lavadoras, secadoras, aires acondicionados, cocinas y lavavajillas de Samsung, LG, Whirlpool, Mabe, Frigidaire, Electrolux, General Electric, Haceb y KitchenAid.</p><p>Somos un servicio técnico independiente: no somos el fabricante de ninguna de estas marcas, y sus nombres se usan solo para indicar qué equipos reparamos. Cuando un equipo está en garantía de fábrica, te recomendamos acudir primero al vendedor.</p>")
           + sec("Cómo trabajamos", PASOS, alt=True) + sec("Contacto", f"<p>WhatsApp y teléfono: <a href=\"tel:+50769337976\">{TEL}</a>.</p>"), None, None, [("Inicio", "/"), ("Quiénes somos", "/nosotros/")], prio="0.5")
    pagina("/privacidad/", f"Política de privacidad | {NOMBRE}", "Política de privacidad de centrodeserviciotecnicopanama.com: qué datos recibimos, para qué los usamos y tus derechos según la Ley 81 de 2019 de Panamá.", "Política de privacidad",
           sec("Datos personales", "<p>Cuando nos escribes por WhatsApp o por teléfono recibimos tu nombre, número, zona y los datos del equipo que quieres reparar. Los usamos solo para coordinar la visita y atender tu solicitud.</p><p>No vendemos tus datos. Puedes pedirnos que los corrijamos o eliminemos escribiéndonos al mismo número de contacto. Esta política se rige por la Ley 81 de 2019 sobre protección de datos personales de Panamá.</p><p>Este sitio puede usar herramientas de estadísticas para medir visitas, sin identificar personas.</p><p>Última actualización: noviembre de 2026.</p>"), None, None, [("Inicio", "/"), ("Privacidad", "/privacidad/")], prio="0.3")
    pagina("/terminos/", f"Términos y condiciones | {NOMBRE}", "Términos y condiciones del servicio técnico de electrodomésticos a domicilio en Panamá: diagnóstico, valores, garantía de la reparación y derechos del consumidor.", "Términos y condiciones",
           sec("Condiciones del servicio", "<p>El valor del diagnóstico y de la reparación se informa antes de empezar y solo se repara con tu aprobación. Cada reparación incluye una garantía sobre la pieza y la mano de obra, cuyo plazo se te indica por escrito.</p><p>Somos un servicio técnico independiente; no representamos al fabricante de ninguna marca. La garantía de fábrica es responsabilidad del fabricante o vendedor.</p><p>Tus derechos como consumidor están protegidos por la Ley 45 de 2007 de Panamá y la autoridad ACODECO.</p><p>Última actualización: noviembre de 2026.</p>"), None, None, [("Inicio", "/"), ("Términos", "/terminos/")], prio="0.3")
    arts = [
        ("humedad-y-salitre-en-electrodomesticos-panama", "Humedad y salitre: cómo afectan tus electrodomésticos en Panamá", "Con humedad casi todo el año, los contactos y placas se corroen más rápido. Qué cuidar en neveras, aires y lavadoras.", [("Qué causa la corrosión", "El vapor de agua y la sal del ambiente costero forman una capa conductora sobre las placas y contactos, y generan cortos y falsos contactos."), ("Qué equipos sufren más", "Las unidades exteriores de aire acondicionado, las placas de lavadoras y los conectores traseros de refrigeradoras."), ("Qué puedes hacer", "Limpiar condensadores, mantener ventilación detrás del equipo y no instalar lavadoras en zonas de salpicadura.")]),
        ("tormentas-electricas-y-voltaje-en-panama", "Tormentas eléctricas y voltaje: protege las placas de tu equipo", "Los picos de voltaje dañan las placas inverter. Cómo saber si necesitas un protector y qué equipos lo requieren.", [("Qué hace un pico de voltaje", "Quema componentes de la placa inverter, que es la parte más cara de refrigeradoras y aires modernos."), ("Qué protector elegir", "Uno con corte por sobrevoltaje y retardo de reconexión, no una regleta simple."), ("Qué equipos lo necesitan", "Refrigeradoras con compresor inverter, aires inverter y lavadoras de carga frontal.")]),
        ("garantia-de-fabrica-vs-garantia-de-reparacion", "Garantía de fábrica o garantía de reparación: cuál aplica", "No son lo mismo. Qué cubre cada una y cómo reclamar.", [("Garantía de fábrica", "La da el fabricante o vendedor y cubre defectos de fabricación por un plazo."), ("Garantía de reparación", "La da el técnico sobre la pieza cambiada y la mano de obra."), ("Cuál usar primero", "Si el equipo es nuevo y en garantía, comienza por el vendedor.")]),
        ("como-ahorrar-energia-con-tus-electrodomesticos-en-panama", "Cómo ahorrar energía con tus electrodomésticos en el calor de Panamá", "Hábitos simples para reducir el consumo de refrigeradora, aire y lavadora.", [("Refrigeradora", "Separarla de la pared, no meter comida caliente y limpiar el condensador."), ("Aire acondicionado", "Mantener filtros limpios y temperatura estable cerca de 24 grados."), ("Lavadora", "Lavar con carga completa y usar agua fría cuando se pueda.")]),
        ("como-instalar-bien-un-electrodomestico-nuevo", "Cómo instalar bien un electrodoméstico nuevo", "Nivelación, voltaje, desagüe y ventilación: lo que evita fallas en el primer año.", [("Nivelación", "Una lavadora desnivelada vibra y desgasta rodamientos."), ("Voltaje y tomacorriente", "Verifica que el equipo sea compatible con 110 o 220 voltios."), ("Ventilación", "Deja espacio detrás y a los lados según el manual.")]),
        ("apagon-y-refrigeradora-que-hacer-con-los-alimentos", "Apagón y refrigeradora: qué hacer con los alimentos", "Cuánto aguanta una refrigeradora sin luz y cómo evitar daños al volver la electricidad.", [("Cuánto tiempo aguanta", "Cerrada, mantiene el frío unas horas; el congelador lleno, más tiempo."), ("Qué evitar", "No abrir la puerta sin necesidad."), ("Al volver la luz", "Espera unos minutos antes de reconectar un equipo con compresor para evitar daño por picos.")]),
    ]
    for slug, t, d, bloques in arts:
        cuerpo = sec(t, rr(esc(d)) + "".join(f"<h3>{esc(a)}</h3><p>{esc(b)}</p>" for a, b in bloques) + '<p>¿Necesitas ayuda con tu equipo? <a href="/">Escríbenos por WhatsApp</a> o elige tu marca arriba.</p>')
        pagina(f"/blog/{slug}/", t[:62], d, t, cuerpo, None, None, [("Inicio", "/"), ("Blog", "/blog/"), (t[:50], f"/blog/{slug}/")],
               [{"@type": "Article", "headline": t, "description": d, "datePublished": HOY, "dateModified": HOY, "author": {"@type": "Organization", "name": NOMBRE}, "publisher": {"@type": "Organization", "name": NOMBRE}, "mainEntityOfPage": DOM + f"/blog/{slug}/"}], bd="Guía", prio="0.5")
    pagina("/blog/", "Blog y guías de electrodomésticos en Panamá", "Guías prácticas para cuidar tus electrodomésticos en el clima de Panamá: humedad, voltaje, garantías, ahorro de energía e instalación.", "Blog y guías de electrodomésticos en Panamá",
           sec("Guías", '<div class="g c3">' + "".join(f'<a class="card l" href="/blog/{s}/"><span class="t">{esc(t)}</span><br><small>{esc(d)}</small></a>' for s, t, d, _ in arts) + "</div>"), None, None, [("Inicio", "/"), ("Blog", "/blog/")], prio="0.6")
    todas = "".join(f'<h2><a href="{base(m)}">Centro de Servicio Técnico {nom(m)} Panamá</a></h2><ul>' + "".join(f'<li><a href="{p}">{esc(p)}</a></li>' for p, _, mm in paginas if mm == m) + "</ul>" for m in BRANDS_ORDER)
    pagina("/mapa-del-sitio/", "Mapa del sitio | Centro de Servicio Técnico Panamá", "Todas las secciones del sitio: nueve marcas, zonas de cobertura, blog e información legal.", "Mapa del sitio", sec("Todas las páginas", todas), None, None, [("Inicio", "/"), ("Mapa del sitio", "/mapa-del-sitio/")], prio="0.2")
    (OUT / "404.html").write_text(f'<!doctype html><html lang="es"><meta charset="utf-8"><title>Página no encontrada</title><meta name="robots" content="noindex"><body style="font-family:system-ui;padding:40px"><h1>Página no encontrada</h1><p><a href="/">Ir al inicio</a></p></body></html>', encoding="utf-8")

# ---------------------------------------------------------------- sitemaps, robots, llms
def tecnico():
    def sm(items):
        def im(p):
            f = (OUT / p.lstrip("/") / "index.html") if p != "/" else OUT / "index.html"
            t = f.read_text(encoding="utf-8") if f.exists() else ""
            return "".join(f"<image:image><image:loc>{DOM}{u}</image:loc></image:image>" for u in dict.fromkeys(re.findall(r'<img[^>]*src="(/img/[^"]+)"', t)))
        return '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">' + "".join(f"<url><loc>{DOM}{p}</loc><lastmod>{HOY}</lastmod><priority>{pr}</priority>{im(p)}</url>" for p, pr, _ in items) + "</urlset>"
    idx = []
    for m in BRANDS_ORDER:
        it = [x for x in paginas if x[2] == m]; (OUT / f"sitemap-{m}.xml").write_text(sm(it)); idx.append(f"sitemap-{m}.xml")
    it = [x for x in paginas if x[2] is None]; (OUT / "sitemap-principal.xml").write_text(sm(it)); idx.append("sitemap-principal.xml")
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<sitemap><loc>{DOM}/{i}</loc><lastmod>{HOY}</lastmod></sitemap>" for i in idx) + "</sitemapindex>")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {DOM}/sitemap.xml\n")
    L = [f"# {NOMBRE}", f"> Servicio técnico independiente de electrodomésticos a domicilio en Panamá. WhatsApp {TEL}.", "", "## Marcas"]
    for m in BRANDS_ORDER: L.append(f"- [Centro de Servicio Técnico {nom(m)} Panamá]({DOM}{base(m)}): {', '.join(EQ[e][2] for e in M[m]['equipos'])}.")
    L += ["", "## Zonas"] + [f"- [{v[0]}]({DOM}/zonas/{z}/)" for z, v in ZONAS.items()]
    (OUT / "llms.txt").write_text("\n".join(L) + "\n")

if __name__ == "__main__":
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    for m in BRANDS_ORDER: build_marca(m); build_sintomas(m); build_zonas_marca(m)
    build_sitio(); tecnico()
    for r, ds, fs in os.walk(OUT):
        os.chmod(r, 0o755)
        for f in fs: os.chmod(os.path.join(r, f), 0o644)
    print(len(paginas), "páginas")
