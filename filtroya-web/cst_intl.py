# -*- coding: utf-8 -*-
"""Capa internacional de serviciotecnicofrigidaire.com: portada, hubs de país, sitemap, robots, llms, hreflang, 404, clave IndexNow.
Se ejecuta DESPUÉS de construir cada ciudad (cada una vive en /país/ o /país/ciudad/ con sus propios assets e imágenes).
Uso:  python3 cst_intl.py <carpeta_de_salida> [token_search_console,...]"""
import html, json, os, pathlib, re, secrets, shutil, sys, datetime

OUT = pathlib.Path(sys.argv[1]); GSC = [x for x in (sys.argv[2] if len(sys.argv) > 2 else "").split(",") if x]
DOM = "https://serviciotecnicofrigidaire.com"
HOY = datetime.date.today().isoformat()
esc = html.escape
# país: (slug, nombre, locale, ciudades[(slug, nombre, resumen)], descripción corta). Una sola ciudad -> la portada del país es la ciudad.
PAISES = [   # (carpeta, nombre, locale, ciudades[(carpeta, nombre, resumen)], equipos, código de bandera). Panamá es la portada del dominio (raíz).
    ("panama", "Panamá", "es-PA", [("", "Panamá", "29 zonas y municipios de Ciudad de Panamá y su área metropolitana")], "refrigeradoras, lavadoras, secadoras, estufas y centros de lavado", "pa"),
    ("costa-rica", "Costa Rica", "es-CR", [("", "San José", "39 zonas y cantones de la Gran Área Metropolitana")], "refrigeradoras, lavadoras, secadoras, cocinas y centros de lavado", "cr"),
    ("guatemala", "Guatemala", "es-GT", [("", "Ciudad de Guatemala", "22 zonas y 13 municipios del área metropolitana")], "refrigeradoras, lavadoras, secadoras, estufas y centros de lavado", "gt"),
    ("el-salvador", "El Salvador", "es-SV", [("", "San Salvador", "32 colonias y municipios del Área Metropolitana")], "refrigeradoras, lavadoras, secadoras, cocinas y centros de lavado", "sv"),
    ("colombia", "Colombia", "es-CO", [("bogota", "Bogotá", "26 localidades y municipios de la Sabana"), ("cali", "Cali", "barrios de Cali y municipios vecinos como Jamundí y Yumbo")], "neveras, lavadoras, secadoras, estufas y centros de lavado", "co"),
    ("ecuador", "Ecuador", "es-EC", [("quito", "Quito", "sectores de Quito y sus valles"), ("guayaquil", "Guayaquil", "ciudadelas de Guayaquil, Samborondón y Daule")], "refrigeradoras, lavadoras, secadoras, cocinas y centros de lavado", "ec"),
    ("chile", "Chile", "es-CL", [("", "Santiago", "las 52 comunas de la Región Metropolitana")], "refrigeradores, lavadoras, secadoras, cocinas y centros de lavado", "cl"),
]
CR = "panama"          # vive en la raíz del dominio (portada del sitio)
def DIRP(p, c=""): return OUT if p[0] == CR else (OUT / p[0] / c[0] if c else OUT / p[0])
def RUTA(p): return "/" if p[0] == CR else f"/{p[0]}/"
PAISES = [p for p in PAISES if all((DIRP(p, c) / "index.html").exists() for c in p[3])]
URLP = {p[0]: RUTA(p) for p in PAISES}
_P0 = OUT
CSSV = re.search(r"site\.css\?v=([0-9a-f]+)", (_P0 / "index.html").read_text(encoding="utf-8")).group(1)
PAL = ("#c8102e", "#1f2a44", "#fff", "#fbf3f4", "#f8dde1", "#6e0719")
NOMBRE = "Servicio Técnico Frigidaire Latinoamérica"
sec = lambda t, b, alt=False, id=None: f'<section class="s{" alt" if alt else ""}"{f" id={chr(34)}{id}{chr(34)}" if id else ""}><div class="w"><h2>{t}</h2>{b}</div></section>'
flag = lambda cc, w=21, h=14: f'<img class="flag" src="/img/flags/{cc}.svg" alt="Bandera de {{}}" width="{w}" height="{h}">'
CC = {p[0]: p[5] for p in PAISES}
NOM = {p[0]: p[1] for p in PAISES}
fl = lambda slug, w=24, h=16: f'<img class="flag" src="/img/flags/{CC[slug]}.svg" alt="Bandera de {NOM[slug]}" width="{w}" height="{h}"> '
card = lambda u, t, s="": f'<a class="card l" href="{u}"><span class="t">{esc(t)}</span>' + (f"<br><small>{esc(s)}</small>" if s else "") + "</a>"
faq_html = lambda faqs: "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faqs)
faq_ld = lambda faqs: {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
URLS = []

def pagina(path, title, desc, h1, lead, cuerpo, crumbs=None, extra_ld=None, hreflangs=None, prio="0.8", noindex=False):
    url = DOM + path
    graf = [{"@type": "Organization", "@id": DOM + "/#org", "name": NOMBRE, "url": DOM + "/", "description": "Servicio técnico independiente a domicilio para equipos Frigidaire en varios países de Latinoamérica.",
             "areaServed": [{"@type": "Country", "name": p[1]} for p in PAISES], "knowsAbout": ["Reparación de refrigeradoras Frigidaire", "Reparación de lavadoras Frigidaire", "Reparación de secadoras Frigidaire", "Reparación de estufas Frigidaire", "Centros de lavado Frigidaire"]},
            {"@type": "WebSite", "@id": DOM + "/#sitio", "url": DOM + "/", "name": NOMBRE, "inLanguage": "es", "publisher": {"@id": DOM + "/#org"}},
            {"@type": "WebPage", "@id": url + "#pagina", "url": url, "name": title, "description": desc, "isPartOf": {"@id": DOM + "/#sitio"}, "inLanguage": "es", "dateModified": HOY}]
    if crumbs: graf.append({"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": DOM + u} for i, (n, u) in enumerate(crumbs)]})
    graf += extra_ld or []
    bc = ('<div class="w bc">' + " › ".join((f'<a href="{u}">{esc(n)}</a>' if i < len(crumbs) - 1 else esc(n)) for i, (n, u) in enumerate(crumbs)) + "</div>") if crumbs and len(crumbs) > 1 else ""
    alts = "".join(f'<link rel="alternate" hreflang="{l}" href="{DOM}{u}">' for l, u in (hreflangs or [])) + (f'<link rel="alternate" hreflang="x-default" href="{url}">' if hreflangs else "")
    tags = "".join(f'<meta name="google-site-verification" content="{g}">' for g in GSC) if path == "/" else ""
    h = (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(desc)}">'
         f'<link rel="canonical" href="{url}">{alts}<meta name="robots" content="{"noindex,follow" if noindex else "index,follow,max-image-preview:large,max-snippet:-1"}"><meta name="theme-color" content="{PAL[0]}">{tags}'
         f'<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta property="og:site_name" content="{esc(NOMBRE)}">'
         f'<link rel="icon" href="/img/logos/frigidaire.png"><link rel="stylesheet" href="/assets/site.css?v={CSSV}"><style>body{{--c:{PAL[0]};--a:{PAL[1]};--ab:{PAL[2]};--bg:{PAL[3]};--soft:{PAL[4]};--hd:{PAL[5]}}}</style>'
         f'<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graf}, ensure_ascii=False)}</script></head><body><a class="skip" href="#contenido">Saltar al contenido</a>'
         f'<header class="h"><div class="w"><a class="logo" href="/"><img class="lgo" src="/img/logos/frigidaire.png" alt="Logo Frigidaire" style="display:block;height:34px;width:auto;max-width:130px;aspect-ratio:auto;object-fit:contain;border-radius:0;box-shadow:none" width="600" height="71"><span>Servicio Técnico<small>Frigidaire · Latinoamérica</small></span></a></div></header>'
         f'<nav class="chips" aria-label="Menú"><div class="w"><a href="/paises/">Todos los países</a>' + "".join(f'<a href="{URLP[p[0]]}">{fl(p[0], 21, 14)}{esc(p[1])}</a>' for p in PAISES) + '</div></nav>'
         f'<main id="contenido"><section class="hero"><div class="w"><div><span class="bd">Frigidaire · Latinoamérica</span><h1>{esc(h1)}</h1><p>{lead}</p></div></div></section>{bc}{cuerpo}'
         f'<div class="w"><p class="upd">Actualizado el {datetime.date.today().strftime("%d/%m/%Y")} · Información orientativa; el diagnóstico final se confirma con pruebas en el equipo.</p></div></main>'
         f'<footer><div class="w"><div class="g c4"><div><h3>Países</h3><ul>' + "".join(f'<li><a href="{URLP[p[0]]}">{fl(p[0], 21, 14)}Servicio técnico Frigidaire en {esc(p[1])}</a></li>' for p in PAISES) + f'</ul></div><div><h3>{esc(NOMBRE)}</h3>'
         f'<p><small>Servicio técnico independiente. Frigidaire y su logo pertenecen a sus propietarios y se usan solo para indicar los equipos que reparamos.</small></p></div></div></div></footer></body></html>')
    f = OUT / path.lstrip("/") / "index.html" if path != "/" else OUT / "index.html"
    f.parent.mkdir(parents=True, exist_ok=True); f.write_text(h, encoding="utf-8")
    if not noindex: URLS.append((path, prio))

# ---------------------------------------------------------------- portada internacional
hreflangs = [(p[2], URLP[p[0]]) for p in PAISES]
faq = [("¿En qué países dan servicio técnico para Frigidaire?", f"Atendemos equipos Frigidaire a domicilio en {', '.join(p[1] for p in PAISES[:-1])} y {PAISES[-1][1]}. Elige tu país para ver las ciudades, las zonas y los equipos que reparamos."),
       ("¿Qué equipos Frigidaire reparan?", "Refrigeradoras, lavadoras, secadoras, estufas y hornos y centros de lavado Frigidaire, según el país. En cada país verás los equipos disponibles."),
       ("¿Son servicio técnico oficial de Frigidaire?", "No. Somos un servicio técnico independiente: no somos el fabricante ni un servicio oficial, y la garantía de fábrica la define el fabricante o el vendedor."),
       ("¿Cómo pido una visita?", "Entra a la página de tu país, elige tu ciudad y escríbenos por WhatsApp con el modelo, la falla y tu zona. Coordinamos el día y la franja."),
       ("¿Reparan equipos Frigidaire comprados en otro país?", "Sí, siempre que podamos identificar el modelo en la etiqueta. Algunas piezas pueden requerir pedido y eso alarga la reparación; te lo informamos antes de empezar.")]
cards = "".join(f'<a class="card l" href="{URLP[p[0]]}"><span class="t">{fl(p[0], 33, 22)}Servicio técnico Frigidaire en {esc(p[1])}</span><br><small>' + esc((f"{p[3][0][1]}: {p[3][0][2]}" if len(p[3]) == 1 else " y ".join(c[1] for c in p[3]))) + '</small></a>' for p in PAISES)
eqs = ["Refrigeradoras (incluidas las de panel Inverter)", "Lavadoras de carga frontal y superior", "Secadoras", "Estufas y hornos", "Centros de lavado"]
cuerpo = (sec("Elige tu país", f'<div class="g c3">{cards}</div>', id="paises")
          + sec("Servicio técnico independiente para equipos Frigidaire", "<p>Frigidaire es una marca de electrodomésticos de origen estadounidense, hoy parte del grupo Electrolux, con refrigeradoras, lavadoras, secadoras, estufas y centros de lavado. "
                "Reparamos esos equipos a domicilio en varios países de Latinoamérica: el técnico va a tu casa, revisa el equipo, te explica la causa y te da el valor antes de reparar.</p>"
                "<ul>" + "".join(f"<li>{x}</li>" for x in eqs) + "</ul>", alt=True)
          + sec("Cómo funciona la visita", "<ol><li><b>Elige tu país y tu ciudad</b> y escríbenos por WhatsApp con el modelo y lo que hace el equipo.</li><li><b>Coordinamos</b> el día y la franja en tu zona.</li><li><b>Diagnóstico en tu casa</b>: revisamos el equipo y te explicamos la causa.</li><li><b>Solo si tú lo apruebas</b> se repara, con el valor por escrito antes de empezar.</li></ol>")
          + sec("Preguntas frecuentes", faq_html(faq), alt=True))
pagina("/paises/", "Servicio técnico Frigidaire en Latinoamérica | Por país", f"Servicio técnico independiente a domicilio para equipos Frigidaire en {', '.join(p[1] for p in PAISES)}. Elige tu país y coordina la visita por WhatsApp.",
       "Servicio técnico Frigidaire en Latinoamérica", "Reparación a domicilio de refrigeradoras, lavadoras, secadoras, estufas y centros de lavado Frigidaire. Elige tu país.", cuerpo, [("Frigidaire Panamá", "/"), ("Países", "/paises/")],
       [faq_ld(faq), {"@type": "ItemList", "name": "Países donde atendemos equipos Frigidaire", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": p[1], "url": DOM + URLP[p[0]]} for i, p in enumerate(PAISES)]}],
       hreflangs=None, prio="0.9")

# ---------------------------------------------------------------- páginas de país con varias ciudades
for p in PAISES:
    if len(p[3]) < 2: continue
    nombres = [c[1] for c in p[3]]
    faq_p = [(f"¿En qué ciudades de {p[1]} dan servicio técnico para Frigidaire?", f"Atendemos equipos Frigidaire a domicilio en {' y '.join(nombres)}. Elige tu ciudad para ver las zonas y los equipos que reparamos."),
             ("¿Cómo pido una visita?", "Entra a la página de tu ciudad y escríbenos por WhatsApp con el modelo, la falla y tu zona. Coordinamos el día y la franja."),
             ("¿Son servicio técnico oficial de Frigidaire?", "No. Somos un servicio técnico independiente: no somos el fabricante ni un servicio oficial, y la garantía de fábrica la define el fabricante o el vendedor.")]
    cards_p = "".join(f'<a class="card l" href="/{p[0]}/{c[0]}/"><span class="t">{fl(p[0], 24, 16)}Servicio técnico Frigidaire en {esc(c[1])}</span><br><small>{esc(c[2])}</small></a>' for c in p[3])
    cuerpo_p = (sec(f"Ciudades de {p[1]} donde atendemos", f'<div class="g c3">{cards_p}</div>')
                + sec(f"Servicio técnico independiente para equipos Frigidaire en {p[1]}", f"<p>Reparamos {esc(p[4])} Frigidaire a domicilio en {esc(' y '.join(nombres))}. El técnico va a tu casa, revisa el equipo, te explica la causa y te da el valor antes de reparar.</p>", alt=True)
                + sec("Preguntas frecuentes", faq_html(faq_p)))
    pagina(f"/{p[0]}/", f"Servicio técnico Frigidaire en {p[1]} | {' y '.join(nombres)}", f"Servicio técnico independiente a domicilio para equipos Frigidaire en {' y '.join(nombres)}, {p[1]}. Elige tu ciudad y coordina la visita por WhatsApp.",
           f"Servicio técnico Frigidaire en {p[1]}", f"Reparación a domicilio de {esc(p[4])} Frigidaire en {esc(' y '.join(nombres))}.", cuerpo_p, [("Frigidaire Latinoamérica", "/paises/"), (p[1], f"/{p[0]}/")],
           [faq_ld(faq_p)], hreflangs=hreflangs, prio="0.9")

# ---------------------------------------------------------------- hreflang en la portada de cada país (alternativas entre países)
for p in PAISES:
    if len(p[3]) == 1:
        f = DIRP(p) / "index.html"; t = f.read_text(encoding="utf-8")
        alts = "".join(f'<link rel="alternate" hreflang="{l}" href="{DOM}{u}">' for l, u in hreflangs) + f'<link rel="alternate" hreflang="x-default" href="{DOM}/paises/">'
        t = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">', "", t)
        f.write_text(t.replace("</head>", alts + "</head>", 1), encoding="utf-8")
    else:      # varias ciudades con el mismo idioma-país: la alternativa entre países es la página del país, no cada ciudad
        for f in DIRP(p).rglob("index.html"):
            t = f.read_text(encoding="utf-8"); n = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">', "", t)
            if n != t: f.write_text(n, encoding="utf-8")

# ---------------------------------------------------------------- sitemaps, robots, llms, 404, clave IndexNow
sm_urls = "".join(f"<url><loc>{DOM}{u}</loc><lastmod>{HOY}</lastmod><priority>{pr}</priority></url>" for u, pr in URLS)
(OUT / "sitemap-principal.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm_urls}</urlset>')
subs = ["sitemap-principal.xml"] + [("" if p[0] == CR else f"{p[0]}/") + (c[0] + "/" if c[0] else "") + "sitemap-frigidaire.xml" for p in PAISES for c in p[3]]
(OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<sitemap><loc>{DOM}/{s}</loc><lastmod>{HOY}</lastmod></sitemap>" for s in subs) + "</sitemapindex>")
(OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {DOM}/sitemap.xml\n")
L = [f"# {NOMBRE}", "> Servicio técnico independiente a domicilio para equipos Frigidaire en varios países de Latinoamérica.", "", "## Países"]
for p in PAISES:
    L.append(f"- [Servicio técnico Frigidaire en {p[1]}]({DOM}{URLP[p[0]]}): {', '.join(c[1] for c in p[3])}; {p[4]}.")
    if len(p[3]) > 1: L += [f"  - [Servicio técnico Frigidaire en {c[1]}]({DOM}/{p[0]}/{c[0]}/): {c[2]}." for c in p[3]]
L += ["", f"- [Todos los países]({DOM}/paises/)"]
(OUT / "llms.txt").write_text("\n".join(L) + "\n")
(OUT / "404.html").write_text('<!doctype html><html lang="es"><meta charset="utf-8"><title>Página no encontrada</title><meta name="robots" content="noindex"><body style="font-family:system-ui;padding:40px"><h1>Página no encontrada</h1><p><a href="/">Ir al inicio</a></p></body></html>', encoding="utf-8")
key = secrets.token_hex(16); (OUT / f"{key}.txt").write_text(key)
(OUT / "version.txt").write_text(f"Servicio Tecnico Frigidaire Latinoamerica. Si ves este texto en {DOM}/version.txt, los archivos nuevos estan en la raiz.\n")
# limpieza de archivos de nivel ciudad que no deben quedar publicados
for p in PAISES:
    if p[0] == CR: continue
    for c in p[3]:
        for n in ("robots.txt", "llms.txt", "404.html"):
            q = DIRP(p, c) / n
            if q.exists() and q.is_file(): q.unlink()
open(OUT.parent / (OUT.name + "-indexnow-key.txt"), "w").write(key)
print(len(PAISES), "países;", len(URLS), "páginas internacionales; clave IndexNow", key)
