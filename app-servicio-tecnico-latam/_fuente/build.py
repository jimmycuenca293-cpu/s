# -*- coding: utf-8 -*-
"""App/PWA de servicio técnico POR MARCA y por país, con geolocalización (barrio + técnico más cercano).
Uso: python3 _fuente/build.py [--estricto]"""
import json, sys, shutil, html, unicodedata, re, csv
from pathlib import Path
from urllib.parse import quote
from PIL import Image
S = Path("/home/user/s")
sys.path.insert(0, str(S / "servicio-tecnico-samsung-panama/_fuente"))
import contenido as base

RAIZ = Path(__file__).resolve().parent.parent
OUT = RAIZ / "site"
CFG = json.loads((RAIZ / "config.json").read_text(encoding="utf-8"))
DOM = CFG["dominio"].rstrip("/"); NOM = CFG["nombre"]; PA = CFG["paises"]; MA = CFG["marcas"]
EQ = {k: base.EQUIPOS[k] for k in ("neveras", "lavadoras", "secadoras")}
ESTRICTO = "--estricto" in sys.argv
esc = html.escape

def slug(s):
    s = unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

# ---------- imágenes por marca (de los sitios de Panamá; sin tocar logos ni fotos) ----------
def F(b, n): return S / f"servicio-tecnico-{b}-panama/images/fotos/{n}.jpg"
MB = S / "servicio-tecnico-mabe-panama/images"
IMG = {
 "samsung": dict(logo=S/"servicio-tecnico-samsung-panama/images/logo/samsung-marca.png", neveras=F("samsung","prod-nevera-sbs"), lavadoras=F("samsung","prod-lavadora-sup"), secadoras=F("samsung","prod-secadora"), tecnico=F("samsung","sam-3"), taller=F("samsung","sam-2")),
 "lg": dict(logo=S/"servicio-tecnico-lg-panama/images/logo/lg-marca.png", neveras=F("lg","prod-nevera-top"), lavadoras=F("lg","prod-lavadora-fr"), secadoras=F("lg","prod-secadora"), tecnico=F("lg","tecnico-nevera"), taller=F("lg","tecnico-banner")),
 "whirlpool": dict(logo=S/"servicio-tecnico-whirlpool-panama/images/logo/whirlpool-marca.png", neveras=F("whirlpool","prod-nevera-sbs"), lavadoras=F("whirlpool","prod-lavadora-sup"), secadoras=F("whirlpool","prod-secadora"), tecnico=F("whirlpool","sam-1"), taller=F("whirlpool","sam-2")),
 "mabe": dict(logo=MB/"logo/logo.png", neveras=MB/"neveras/producto-neveras-panama.jpg", lavadoras=MB/"lavadoras/hero-lavadoras-panama.jpg", secadoras=MB/"secadoras/hero-secadoras-panama.jpg", tecnico=MB/"nosotros/tecnico-saludo-cliente-panama.jpg", taller=MB/"nosotros/tecnico-trabajando-servicio-mabe.jpg"),
 "frigidaire": dict(logo=S/"servicio-tecnico-frigidaire-panama/images/logo/frigidaire-marca.png", neveras=F("frigidaire","prod-nevera-sbs"), lavadoras=F("frigidaire","prod-lavadora-fr"), secadoras=F("frigidaire","prod-torre"), tecnico=F("frigidaire","sam-4"), taller=F("frigidaire","sam-1")),
 "electrolux": dict(logo=S/"servicio-tecnico-electrolux-panama/images/logo/electrolux-marca.png", neveras=F("electrolux","prod-nevera-sbs"), lavadoras=F("electrolux","prod-lavadora-fr"), secadoras=F("electrolux","prod-torre"), tecnico=F("electrolux","sam-6"), taller=F("electrolux","sam-2")),
 "general-electric": dict(logo=S/"servicio-tecnico-general-electric-panama/images/logo/general-electric-marca.png", neveras=F("general-electric","prod-nevera-sbs"), lavadoras=F("general-electric","prod-lavadora-fr"), secadoras=F("general-electric","prod-secadora"), tecnico=F("general-electric","sam-4"), taller=F("general-electric","sam-2")),
}
def copiar_imagenes():
    for m, d in IMG.items():
        (OUT / "img" / m).mkdir(parents=True, exist_ok=True)
        for k, src in d.items():
            if not src.exists(): print("⚠ falta", src); continue
            im = Image.open(src)
            if k == "logo":
                im.save(OUT / "img" / m / "logo.png")
            else:
                im = im.convert("RGB"); im.thumbnail((900, 900)); im.save(OUT / "img" / m / f"{k}.jpg", quality=80, optimize=True)
        im = Image.open(OUT / "img" / m / "logo.png").convert("RGBA"); im.thumbnail((512, 512)); im.save(OUT / "img" / m / "logo.png")

def ALT(m, k, pais=None):
    mn = MA[m]["nombre"]; z = f" en {pais}" if pais else ""
    return {"logo": f"Logo {mn}", "neveras": f"Servicio técnico de neveras {mn}{z}", "lavadoras": f"Reparación de lavadoras {mn}{z}",
            "secadoras": f"Reparación de secadoras {mn}{z}", "tecnico": f"Técnico {mn} a domicilio{z}", "taller": f"Centro de servicio técnico {mn}{z}"}[k]

# ---------- técnicos (editable en tecnicos.csv) ----------
TEC = {}
for r in csv.DictReader(open(RAIZ / "tecnicos.csv", encoding="utf-8")):
    TEC.setdefault(r["marca"], []).append(dict(n=r["nombre"], p=r["pais"], c=r["ciudad"], z=r["zona"], la=float(r["lat"]), lo=float(r["lon"]), w=r["whatsapp"]))

def wa(num, texto=""):
    return f"https://wa.me/{num}" + (f"?text={quote(texto)}" if texto else "")

def adapt(t, marca, pais):
    return t.replace("Samsung", marca).replace("Ciudad de Panamá", pais).replace("Panamá", pais)

CSS = """:root{--c:#0f766e;--bg:#f6f8fa;--tx:#14202b;--card:#fff;--ln:#dde3ea;--mu:#5b6b76}
@media (prefers-color-scheme:dark){:root{--bg:#0f1a22;--tx:#e8eef2;--card:#17252f;--ln:#27394a;--mu:#9bb0bf}}
*{box-sizing:border-box}body{margin:0;font:16px/1.55 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:var(--tx);background:var(--bg)}
a{color:var(--c)}img{max-width:100%;height:auto}.w{max-width:1000px;margin:0 auto;padding:0 16px}
header.h{background:var(--mc,#0f766e);color:var(--mt,#fff);padding:22px 0}header .w{display:grid;gap:14px;grid-template-columns:1fr;align-items:center}
@media(min-width:760px){header .w.hero{grid-template-columns:1.1fr .9fr}}
h1{margin:.2em 0;font-size:clamp(1.5rem,5vw,2.3rem);line-height:1.2;text-wrap:balance}h2{text-wrap:balance}
nav.bc{font-size:.85rem;opacity:.9}nav.bc a{color:inherit}.lg{display:inline-block;background:#fff;border-radius:10px;padding:6px 12px}.lg img{height:34px;width:auto;display:block}
.ph{border-radius:14px;width:100%;aspect-ratio:16/10;object-fit:cover;display:block}main{padding:20px 0 70px}
.g{display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(210px,1fr))}.card{background:var(--card);border:1px solid var(--ln);border-radius:12px;padding:14px;color:var(--tx)}
.card.l{text-decoration:none;display:block}.card .ph{margin-bottom:10px;aspect-ratio:4/3;object-fit:contain;background:#fff}
.b{display:inline-block;padding:12px 18px;border-radius:10px;background:#25d366;color:#052e16;font-weight:700;text-decoration:none;border:0;cursor:pointer;font-size:1rem}
.b.alt{background:#fff;color:#0b1f33}.urg{color:#b45309;font-weight:700;font-size:.85rem}
#geo{background:var(--card);border:1px solid var(--ln);border-radius:14px;padding:16px;margin:0 0 18px}#msg{margin:.6em 0;font-weight:600}
#tec{display:none;margin-top:10px;border:2px solid #25d366;border-radius:12px;padding:12px}.mu{color:var(--mu);font-size:.85rem}
details{background:var(--card);border:1px solid var(--ln);border-radius:10px;padding:10px 14px;margin:8px 0}
.fab{position:fixed;right:14px;bottom:14px;z-index:9;box-shadow:0 4px 14px rgba(0,0,0,.3)}footer{padding:24px 16px;font-size:.85rem;color:var(--mu);text-align:center}
.pill{display:inline-block;padding:8px 14px;border:1px solid var(--ln);border-radius:99px;background:var(--card);text-decoration:none;margin:0 6px 8px 0}
.mb{display:block;border-radius:14px;overflow:hidden;text-decoration:none;color:#fff;font-weight:800}.mb .lg{margin:14px}.mb span{display:block;padding:0 14px 14px}"""

PAGES = []
# Cómo busca la gente en cada país (para títulos, H1 y descripciones)
VOC = {
 "co": {"neveras": "neveras", "lavadoras": "lavadoras", "secadoras": "secadoras", "alt": {"neveras": "refrigeradores"}},
 "pa": {"neveras": "neveras", "lavadoras": "lavadoras", "secadoras": "secadoras", "alt": {"neveras": "refrigeradoras"}},
 "gt": {"neveras": "refrigeradoras", "lavadoras": "lavadoras", "secadoras": "secadoras", "alt": {"neveras": "neveras"}},
 "sv": {"neveras": "refrigeradoras", "lavadoras": "lavadoras", "secadoras": "secadoras", "alt": {"neveras": "neveras"}},
 "cr": {"neveras": "refrigeradoras", "lavadoras": "lavadoras", "secadoras": "secadoras", "alt": {"neveras": "neveras"}},
 "ec": {"neveras": "refrigeradoras", "lavadoras": "lavadoras", "secadoras": "secadoras", "alt": {"neveras": "neveras"}},
 "py": {"neveras": "heladeras", "lavadoras": "lavarropas", "secadoras": "secarropas", "alt": {"neveras": "refrigeradores", "lavadoras": "lavadoras"}},
 "cl": {"neveras": "refrigeradores", "lavadoras": "lavadoras", "secadoras": "secadoras", "alt": {"neveras": "neveras"}},
}
def term(cc, k): return VOC[cc][k]
def alt(cc, k): return VOC[cc]["alt"].get(k, "")

def hreflangs(m, rel):
    l = [f'<link rel="alternate" hreflang="{PA[c]["locale"]}" href="{DOM}/{m}/{c}/{rel}">' for c in PA]
    return "".join(l) + f'<link rel="alternate" hreflang="x-default" href="{DOM}/{m}/">'

def page(ruta, title, desc, h1, body, bc=None, m=None, cc=None, rel=None, jsonld=None, hero=None, fab=True):
    url = f"{DOM}/{ruta}"; PAGES.append(url)
    mc = MA[m]["color"] if m else "#0f766e"; mt = MA[m].get("texto", "#fff") if m else "#fff"
    bch = '<nav class="bc">' + " › ".join(f'<a href="{u}">{esc(t)}</a>' for t, u in bc) + "</nav>" if bc else ""
    ld = "".join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in (jsonld or []))
    hl = hreflangs(m, rel) if (m and cc and rel is not None) else ""
    gtm = f"<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s);j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i;f.parentNode.insertBefore(j,f)}})(window,document,'script','dataLayer','{CFG['gtm']}');</script>" if CFG["gtm"] else ""
    ver = f'<meta name="google-site-verification" content="{CFG["verificacion_gsc"]}">' if CFG["verificacion_gsc"] else ""
    man = f"/{m}/manifest.webmanifest" if m else "/manifest.webmanifest"
    ico = f"/img/{m}/logo.png" if m else "/icons/icon-192.png"
    img = f"{DOM}{hero[0]}" if hero else f"{DOM}{ico}"
    hr = f'<img class="ph" src="{hero[0]}" alt="{esc(hero[1])}" width="900" height="560" fetchpriority="high">' if hero else ""
    logo = f'<a class="lg" href="/{m}/"><img src="/img/{m}/logo.png" alt="{esc(ALT(m,"logo"))}"></a>' if m else ""
    locale = PA[cc]["locale"] if cc else "es"
    fabh = ""
    if fab and cc and m:
        fabh = f'<a class="b fab" data-evt="whatsapp" id="fab" href="{wa(PA[cc]["wa"], "Hola, necesito servicio técnico " + MA[m]["nombre"] + " en " + PA[cc]["nombre"])}" rel="noopener">WhatsApp {esc(MA[m]["nombre"])}</a>'
    h = f"""<!doctype html><html lang="{locale}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{url}">{hl}{ver}
<link rel="manifest" href="{man}"><meta name="theme-color" content="{mc}"><link rel="icon" href="{ico}"><link rel="apple-touch-icon" href="{ico}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="{url}"><meta property="og:image" content="{img}">
<style>{CSS}</style>{ld}{gtm}</head><body data-marca="{m or ''}" data-nombre="{esc(MA[m]['nombre']) if m else ''}" data-pais="{cc or ''}" style="--mc:{mc};--mt:{mt}">
<header class="h"><div class="w{' hero' if hero else ''}"><div>{logo}{bch}<h1>{esc(h1)}</h1></div>{hr}</div></header>
<main class="w">{body}</main>{fabh}
<footer>{esc(NOM)}{(' · ' + esc(MA[m]['nombre'])) if m else ''} · <a href="/">Todas las marcas</a></footer>
<script src="/datos.js" defer></script><script src="/geo.js" defer></script><script src="/app.js" defer></script></body></html>"""
    p = OUT / ruta / "index.html" if ruta else OUT / "index.html"
    p.parent.mkdir(parents=True, exist_ok=True); p.write_text(h, encoding="utf-8")

def faq_ld(pares):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pares]}
def bc_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}
def local_ld(m, cc, ciudad=None):
    p = PA[cc]; mn = MA[m]["nombre"]
    return {"@context": "https://schema.org", "@type": "HomeAndConstructionBusiness", "name": f"Servicio técnico {mn} {ciudad or p['nombre']}",
            "url": f"{DOM}/{m}/{cc}/", "image": f"{DOM}/img/{m}/tecnico.jpg", "telephone": p["tel"] or None, "priceRange": "$$",
            "areaServed": ([{"@type": "City", "name": ciudad}] if ciudad else [{"@type": "City", "name": c} for c in p["ciudades"]]) + [{"@type": "Country", "name": p["nombre"]}],
            "knowsAbout": [f"reparación de neveras {mn}", f"reparación de lavadoras {mn}", f"reparación de secadoras {mn}"]}

def btn(m, cc, texto, etiqueta):
    return f'<a class="b" data-evt="whatsapp" href="{wa(PA[cc]["wa"], texto)}" rel="noopener">{esc(etiqueta)}</a>'

def bloque_geo(m):
    mn = MA[m]["nombre"]
    return f"""<section id="geo"><p><b>¿Dónde estás?</b> Activa tu ubicación y te mostramos el técnico {esc(mn)} más cercano a tu barrio, con su WhatsApp.</p>
<button class="b" id="geo-btn" type="button">📍 Usar mi ubicación</button><div id="msg" role="status"></div>
<div id="tec"></div><p class="mu">Tu ubicación se procesa en tu dispositivo. Para decirte el barrio se consulta OpenStreetMap con tus coordenadas aproximadas; no guardamos nada en nuestros servidores.</p></section>"""

def build():
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    copiar_imagenes()
    faltan = [c for c in PA if not PA[c]["wa"]]
    # ---- raíz: elegir marca
    mc = "".join(f'<a class="card l mb" href="/{m}/" style="background:{v["color"]};color:{v.get("texto","#fff")}"><span class="lg"><img src="/img/{m}/logo.png" alt="{esc(ALT(m,"logo"))}"></span><img class="ph" style="aspect-ratio:4/3;object-fit:cover" loading="lazy" src="/img/{m}/tecnico.jpg" alt="{esc(ALT(m,"tecnico"))}"><span>Servicio técnico {esc(v["nombre"])}</span></a>' for m, v in MA.items())
    body = f"""<section id="geo"><p><b>Elige tu marca.</b> Cada marca tiene su propia aplicación: al entrar y activar tu ubicación verás el técnico de esa marca más cercano a tu barrio.</p></section>
<div class="g">{mc}</div><h2>Países donde trabajamos</h2><p>{', '.join(esc(p['nombre']) for p in PA.values())}.</p>"""
    page("", f"Servicio técnico de neveras, lavadoras y secadoras por marca en Latinoamérica | {NOM}",
         "Elige tu marca (Samsung, LG, Whirlpool, Mabe, Frigidaire, Electrolux o GE) y encuentra el técnico más cercano a tu barrio con su WhatsApp en Colombia, Panamá, Guatemala, El Salvador, Costa Rica, Ecuador, Paraguay y Chile.",
         "Servicio técnico por marca: encuentra el técnico más cercano a tu barrio", body, jsonld=[{"@context": "https://schema.org", "@type": "WebSite", "name": NOM, "url": DOM + "/"}], fab=False)
    for m, v in MA.items():
        mn = v["nombre"]; tt = TEC.get(m, [])
        # datos de técnicos de ESTA marca únicamente
        (OUT / m).mkdir(exist_ok=True)
        (OUT / m / "tecnicos.json").write_text(json.dumps(tt, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        (OUT / m / "manifest.webmanifest").write_text(json.dumps({"name": f"Servicio técnico {mn}", "short_name": mn, "start_url": f"/{m}/", "scope": f"/{m}/", "display": "standalone", "background_color": "#ffffff", "theme_color": v["color"], "lang": "es",
            "icons": [{"src": f"/img/{m}/logo.png", "sizes": "512x512", "type": "image/png", "purpose": "any"}]}, ensure_ascii=False), encoding="utf-8")
        # ---- home de la marca
        pais_l = "".join(f'<a class="pill" href="/{m}/{c}/">{esc(p["nombre"])}</a>' for c, p in PA.items())
        eqs = "".join(f'<a class="card l" href="/{m}/{k}/"><img class="ph" loading="lazy" src="/img/{m}/{k}.jpg" alt="{esc(ALT(m,k))}"><h3>{esc(e["corto"])} {esc(mn)}</h3></a>' for k, e in EQ.items()) if False else ""
        body = bloque_geo(mn and m) + f"""<h2>Elige tu país</h2><p>{pais_l}</p>
<h2>Equipos {esc(mn)} que reparamos</h2><div class="g">""" + "".join(f'<div class="card"><img class="ph" loading="lazy" src="/img/{m}/{k}.jpg" alt="{esc(ALT(m,k))}"><h3>{esc(e["corto"])} {esc(mn)}</h3><p class="mu">{esc(adapt(e["intro"],mn,"tu país")[:120])}…</p></div>' for k, e in EQ.items()) + "</div>"
        page(f"{m}/", f"Servicio técnico {mn} – técnico más cercano a tu barrio con WhatsApp | {NOM}",
             f"Servicio técnico {mn} a domicilio: activa tu ubicación y escribe por WhatsApp al técnico {mn} más cercano. Neveras, lavadoras y secadoras {mn} en 8 países.",
             f"Servicio técnico {mn}: el técnico más cercano a tu barrio", body, bc=[("Inicio", "/")], m=m, rel=None,
             hero=(f"/img/{m}/tecnico.jpg", ALT(m, "tecnico")), jsonld=[bc_ld([("Inicio", DOM + "/"), (mn, f"{DOM}/{m}/")])], fab=False)
        for cc, p in PA.items():
            pn = p["nombre"]
            ciud = "".join(f'<a class="pill" href="/{m}/{cc}/{slug(c)}/">{esc(c)}</a>' for c in p["ciudades"])
            eqc = "".join(f'<a class="card l" href="/{m}/{cc}/{k}/"><img class="ph" loading="lazy" src="/img/{m}/{k}.jpg" alt="{esc(ALT(m,k,pn))}"><h3>{esc(e["corto"])} {esc(mn)} en {esc(pn)}</h3></a>' for k, e in EQ.items())
            fq = [(f"¿Hacen servicio técnico {mn} a domicilio en {pn}?", f"Sí. Atendemos neveras, lavadoras y secadoras {mn} a domicilio en {', '.join(p['ciudades'])} y alrededores."),
                  (f"¿Cómo contacto al técnico {mn} en {pn}?", f"Escríbenos por WhatsApp con el modelo y la falla de tu equipo {mn}; o activa tu ubicación para ver el técnico más cercano a tu barrio.")]
            body = bloque_geo(m) + f"""<p>Reparación a domicilio de neveras, lavadoras y secadoras {esc(mn)} en {esc(pn)}.</p><p>{btn(m,cc,f'Hola, necesito servicio técnico {mn} en {pn}',f'WhatsApp {mn} {pn}')}</p>
<h2>Equipos {esc(mn)} en {esc(pn)}</h2><div class="g">{eqc}</div><h2>Ciudades con servicio {esc(mn)}</h2><p>{ciud}</p><h2>Preguntas frecuentes</h2>""" + "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in fq)
            page(f"{m}/{cc}/", f"Servicio técnico {mn} en {pn}: {term(cc,'neveras')}, {term(cc,'lavadoras')} y {term(cc,'secadoras')} | {NOM}",
                 f"Servicio técnico {mn} en {pn}: reparación a domicilio de {term(cc,'neveras')}, {term(cc,'lavadoras')} y {term(cc,'secadoras')} {mn}. Encuentra el técnico {mn} más cercano a tu barrio y escríbele por WhatsApp.",
                 f"Servicio técnico {mn} en {pn}", body, bc=[("Inicio", "/"), (mn, f"/{m}/")], m=m, cc=cc, rel="",
                 hero=(f"/img/{m}/taller.jpg", ALT(m, "taller", pn)), jsonld=[local_ld(m, cc), faq_ld(fq), bc_ld([("Inicio", DOM + "/"), (mn, f"{DOM}/{m}/"), (pn, f"{DOM}/{m}/{cc}/")])])
            for ci in p["ciudades"]:
                cs = slug(ci); tecs = [t for t in tt if t["p"] == cc and t["c"] == ci]
                th = "".join(f'<div class="card"><b>{esc(t["n"])}</b><br><span class="mu">Zona: {esc(t["z"])}, {esc(ci)}</span><p>{btn(m,cc,f"Hola, necesito servicio técnico {mn} en {ci}","WhatsApp").replace(PA[cc]["wa"], t["w"] or PA[cc]["wa"])}</p></div>' for t in tecs)
                eqh = "".join(f'<a class="card l" href="/{m}/{cc}/{k}/"><img class="ph" loading="lazy" src="/img/{m}/{k}.jpg" alt="{esc(ALT(m,k,ci))}"><h3>{esc(e["corto"])} {esc(mn)} en {esc(ci)}</h3><span class="mu">{esc(e["fallas"][0][0])}; {esc(e["fallas"][1][0].lower())}</span></a>' for k, e in EQ.items())
                fq = [(f"¿Hacen servicio técnico {mn} a domicilio en {ci}?", f"Sí. Visitamos hogares y negocios en {ci}, {pn}, para neveras, lavadoras y secadoras {mn}."),
                      (f"¿Cuál es el técnico {mn} más cercano en {ci}?", f"Activa tu ubicación en esta página y te mostramos el técnico {mn} más cercano a tu barrio con su WhatsApp.")]
                body = bloque_geo(m) + f"""<p>Técnico {esc(mn)} en {esc(ci)}, {esc(pn)}: diagnóstico y reparación a domicilio.</p><h2>Técnicos {esc(mn)} en {esc(ci)}</h2><div class="g">{th}</div>
<h2>Equipos {esc(mn)} que reparamos en {esc(ci)}</h2><div class="g">{eqh}</div><h2>Preguntas frecuentes</h2>""" + "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in fq)
                page(f"{m}/{cc}/{cs}/", f"Servicio técnico {mn} en {ci}, {pn}: {term(cc,'neveras')}, lavadoras y secadoras | {NOM}",
                     f"Servicio técnico {mn} cerca de ti en {ci}, {pn}: reparación a domicilio de {term(cc,'neveras')}, {term(cc,'lavadoras')} y {term(cc,'secadoras')} {mn}. WhatsApp del técnico más cercano a tu barrio.",
                     f"Servicio técnico {mn} en {ci}, {pn}", body, bc=[("Inicio", "/"), (mn, f"/{m}/"), (pn, f"/{m}/{cc}/")], m=m, cc=cc, rel=None,
                     hero=(f"/img/{m}/tecnico.jpg", ALT(m, "tecnico", ci)), jsonld=[local_ld(m, cc, ci), faq_ld(fq), bc_ld([("Inicio", DOM + "/"), (mn, f"{DOM}/{m}/"), (pn, f"{DOM}/{m}/{cc}/"), (ci, f"{DOM}/{m}/{cc}/{cs}/")])])
            for k, e in EQ.items():
                fl = "".join(f'<div class="card"><h3>{esc(adapt(f[0],mn,pn))}</h3><span class="urg">{esc(f[2])}</span><p>{esc(adapt(f[1],mn,pn))}</p><p><i>{esc(adapt(f[3],mn,pn))}</i></p></div>' for f in e["fallas"])
                fq = [(adapt(q, mn, pn), adapt(a, mn, pn)) for q, a in e["faq"]]
                mod = "".join(f"<li>{esc(x)}</li>" for x in e["modelos"])
                body = bloque_geo(m) + f"""<p>{esc(adapt(e['intro'],mn,pn))}</p><p>{btn(m,cc,f'Hola, mi {e["sing"]} {mn} tiene una falla (en {pn})','Cotizar por WhatsApp')}</p>
<h2>Fallas comunes en {esc(e['corto'].lower())} {esc(mn)}</h2><div class="g">{fl}</div><h2>Modelos que atendemos</h2><ul>{mod}</ul>
<img class="ph" loading="lazy" src="/img/{m}/tecnico.jpg" alt="{esc(ALT(m,'tecnico',pn))}"><h2>Preguntas frecuentes</h2>""" + "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in fq)
                t = f"Servicio técnico de {term(cc,k)} {mn} en {pn}"
                a2 = f" ({alt(cc,k)})" if alt(cc,k) else ""
                page(f"{m}/{cc}/{k}/", f"{t} – reparación a domicilio | {NOM}", f"{t}{a2}. Reparación a domicilio, diagnóstico y garantía. WhatsApp del técnico {mn} más cercano a tu barrio en {pn}.", t, body,
                     bc=[("Inicio", "/"), (mn, f"/{m}/"), (pn, f"/{m}/{cc}/")], m=m, cc=cc, rel=f"{k}/", hero=(f"/img/{m}/{k}.jpg", ALT(m, k, pn)),
                     jsonld=[local_ld(m, cc), faq_ld(fq), bc_ld([("Inicio", DOM + "/"), (mn, f"{DOM}/{m}/"), (pn, f"{DOM}/{m}/{cc}/"), (e["corto"], f"{DOM}/{m}/{cc}/{k}/")])])
    # ---- estáticos
    (OUT / "datos.js").write_text("window.DATOS=" + json.dumps({c: {"n": p["nombre"], "wa": p["wa"], "dial": p["dial"], "ciudades": p["ciudades"]} for c, p in PA.items()}, ensure_ascii=False) + ";", encoding="utf-8")
    (OUT / "geo.js").write_text(r"""(function(){
var D=window.DATOS,B=document.body,M=B.dataset.marca,btn=document.getElementById('geo-btn'),msg=document.getElementById('msg'),tec=document.getElementById('tec');
function dist(a,b,c,d){var R=6371,r=Math.PI/180,x=(c-a)*r,y=(d-b)*r,h=Math.sin(x/2)*Math.sin(x/2)+Math.cos(a*r)*Math.cos(c*r)*Math.sin(y/2)*Math.sin(y/2);return 2*R*Math.asin(Math.sqrt(h));}
function ciudadCerca(la,lo){var b=null;for(var cc in D){var cs=D[cc].ciudades;for(var n in cs){var d=dist(la,lo,cs[n][0],cs[n][1]);if(!b||d<b.d)b={cc:cc,city:n,d:d};}}return b;}
function slug(s){return s.normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');}
function barrio(la,lo,cb){var done=false,t=setTimeout(function(){if(!done){done=true;cb(null);}},4500);
  fetch('https://nominatim.openstreetmap.org/reverse?format=jsonv2&zoom=16&accept-language=es&lat='+la+'&lon='+lo).then(function(r){return r.json();}).then(function(j){if(done)return;done=true;clearTimeout(t);var a=j.address||{};cb(a.neighbourhood||a.suburb||a.quarter||a.city_district||a.village||a.town||null);}).catch(function(){if(!done){done=true;cb(null);}});}
function mostrar(la,lo,nb){
  var c=ciudadCerca(la,lo);if(!c||c.d>600){msg.textContent='Todavía no tenemos técnicos en tu zona. Elige tu país abajo.';return;}
  try{localStorage.setItem('pos',JSON.stringify([la,lo]));}catch(e){}
  msg.innerHTML='Estás en <b>'+(nb?nb+', ':'')+c.city+', '+D[c.cc].n+'</b>';
  if(!M){var h='';return;}
  fetch('/'+M+'/tecnicos.json').then(function(r){return r.json();}).then(function(T){
    var best=null;T.forEach(function(t){if(t.p!==c.cc)return;var d=dist(la,lo,t.la,t.lo);if(!best||d<best.d)best={t:t,d:d};});
    var num=best&&best.t.w||D[c.cc].wa,nombre=best?best.t.n:'Servicio técnico',zona=best?best.t.z+', '+best.t.c:D[c.cc].n;
    var txt='Hola, necesito servicio técnico '+B.dataset.nombre+(nb?' en '+nb+', ':' en ')+c.city;
    tec.style.display='block';
    tec.innerHTML='<b>Técnico más cercano</b><br>'+nombre+'<br><span class="mu">'+zona+(best?' · a '+Math.round(best.d)+' km':'')+'</span><p><a class="b" data-evt="whatsapp" target="_blank" rel="noopener" href="https://wa.me/'+num+'?text='+encodeURIComponent(txt)+'">💬 Escribir por WhatsApp</a></p><p><a href="/'+M+'/'+c.cc+'/'+slug(c.city)+'/">Ver servicio en '+c.city+'</a></p>';
    var f=document.getElementById('fab');if(f)f.href='https://wa.me/'+num+'?text='+encodeURIComponent(txt);
  });}
function pedir(){if(!navigator.geolocation){msg.textContent='Tu navegador no permite ubicación. Elige tu país abajo.';return;}
  msg.textContent='Buscando tu ubicación…';
  navigator.geolocation.getCurrentPosition(function(p){var la=p.coords.latitude,lo=p.coords.longitude;msg.textContent='Buscando tu barrio…';barrio(la,lo,function(nb){mostrar(la,lo,nb);});},
    function(e){msg.textContent=e&&e.code===1?'No diste permiso de ubicación. Elige tu país abajo.':'No pudimos obtener tu ubicación. Elige tu país abajo.';},{timeout:12000,maximumAge:600000});}
if(btn){btn.addEventListener('click',pedir);
  if(navigator.permissions&&navigator.permissions.query){navigator.permissions.query({name:'geolocation'}).then(function(s){if(s.state==='granted')pedir();}).catch(function(){});}}
})();""", encoding="utf-8")
    (OUT / "app.js").write_text("""if('serviceWorker' in navigator){addEventListener('load',function(){navigator.serviceWorker.register('/sw.js').catch(function(){});});}
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('[data-evt="whatsapp"]');if(a){window.dataLayer=window.dataLayer||[];window.dataLayer.push({event:'whatsapp',marca:document.body.dataset.marca||'',pais:document.body.dataset.pais||''});}});""", encoding="utf-8")
    (OUT / "sw.js").write_text("""var V='st-v2';
self.addEventListener('install',function(e){self.skipWaiting();});
self.addEventListener('activate',function(e){e.waitUntil(caches.keys().then(function(k){return Promise.all(k.filter(function(x){return x!==V;}).map(function(x){return caches.delete(x);}));}));self.clients.claim();});
self.addEventListener('fetch',function(e){if(e.request.method!=='GET'||new URL(e.request.url).origin!==location.origin)return;e.respondWith(fetch(e.request).then(function(r){var c=r.clone();caches.open(V).then(function(ch){ch.put(e.request,c);});return r;}).catch(function(){return caches.match(e.request).then(function(r){return r||caches.match('/');});}));});""", encoding="utf-8")
    (OUT / "manifest.webmanifest").write_text(json.dumps({"name": NOM, "short_name": "Soporte Técnico", "start_url": "/", "display": "standalone", "background_color": "#f6f8fa", "theme_color": "#0f766e", "lang": "es",
        "icons": [{"src": "/icons/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, ensure_ascii=False), encoding="utf-8")
    (OUT / "icons").mkdir()
    from PIL import ImageDraw
    for s in (192, 512):
        im = Image.new("RGB", (s, s), "#0f766e"); d = ImageDraw.Draw(im)
        d.ellipse([s*.3, s*.18, s*.7, s*.58], fill="white"); d.polygon([(s*.5, s*.84), (s*.34, s*.5), (s*.66, s*.5)], fill="white"); d.ellipse([s*.42, s*.3, s*.58, s*.46], fill="#0f766e")
        im.save(OUT / "icons" / f"icon-{s}.png")
    idx = []
    for nombre, filtro in [("inicio", lambda u: u.rstrip("/") == DOM)] + [(m, (lambda mm: (lambda u: u.startswith(f"{DOM}/{mm}/")))(m)) for m in MA]:
        us = sorted(u for u in set(PAGES) if filtro(u))
        (OUT / f"sitemap-{nombre}.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{u}</loc><changefreq>monthly</changefreq></url>" for u in us) + "</urlset>", encoding="utf-8")
        idx.append(f"<sitemap><loc>{DOM}/sitemap-{nombre}.xml</loc></sitemap>")
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(idx) + "</sitemapindex>", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {DOM}/sitemap.xml\n", encoding="utf-8")
    (OUT / "llms.txt").write_text(f"# {NOM}\n> Servicio técnico a domicilio por marca (neveras, lavadoras, secadoras) en " + ", ".join(p["nombre"] for p in PA.values()) + ".\n" + "".join(f"- {v['nombre']}: {DOM}/{m}/\n" for m, v in MA.items()), encoding="utf-8")
    (OUT / ".htaccess").write_text("DirectoryIndex index.html\nAddType application/manifest+json .webmanifest\nHeader set Permissions-Policy \"geolocation=(self)\"\n", encoding="utf-8")
    print(f"{len(set(PAGES))} páginas")
    if faltan:
        print("⚠ FALTAN WhatsApp para: " + ", ".join(PA[c]["nombre"] for c in faltan))
        if ESTRICTO: sys.exit(1)

build()
