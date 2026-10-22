# -*- coding: utf-8 -*-
"""Generador: app/PWA de servicio técnico multipaís con geolocalización. Uso: python3 _fuente/build.py [--estricto]"""
import json, sys, shutil, html, unicodedata, re, math
from pathlib import Path
from urllib.parse import quote
sys.path.insert(0, str(Path("/home/user/s/servicio-tecnico-samsung-panama/_fuente")))
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

def wa(cc, texto=""):
    n = PA[cc]["wa"] or (PA[cc]["dial"] + "00000000")
    return f"https://wa.me/{n}?text={quote(texto)}" if texto else f"https://wa.me/{n}"

def adapt(t, marca, pais):
    return t.replace("Samsung", marca).replace("Ciudad de Panamá", pais["nombre"]).replace("Panamá", pais["nombre"])

CSS = """:root{--c:#0f766e;--bg:#f6f8fa;--tx:#14202b;--card:#fff;--ln:#dde3ea}
*{box-sizing:border-box}body{margin:0;font:16px/1.55 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:var(--tx);background:var(--bg)}
a{color:var(--c)}header.h{background:linear-gradient(135deg,#0b1f33,#0f766e);color:#fff;padding:28px 16px}
.w{max-width:1000px;margin:0 auto;padding:0 16px}header .w{padding:0}h1{margin:.2em 0;font-size:clamp(1.5rem,5vw,2.3rem);line-height:1.2}
nav.bc{font-size:.85rem;opacity:.9}nav.bc a{color:#cfeee9}main{padding:20px 0 40px}
.g{display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(210px,1fr))}.card{background:var(--card);border:1px solid var(--ln);border-radius:12px;padding:14px}
.card h3{margin:.1em 0 .3em}.b{display:inline-block;padding:11px 18px;border-radius:10px;background:#25d366;color:#052e16;font-weight:700;text-decoration:none;border:0;cursor:pointer;font-size:1rem}
.b.alt{background:#fff;color:var(--c);border:2px solid var(--c)}.m{display:block;color:#fff;text-decoration:none;border-radius:12px;padding:16px;font-weight:700}
#geo{background:#fff;border:1px solid var(--ln);border-radius:14px;padding:16px;margin:16px 0}#msg{margin:.6em 0;font-weight:600}
.urg{color:#b45309;font-weight:700;font-size:.85rem}details{background:#fff;border:1px solid var(--ln);border-radius:10px;padding:10px 14px;margin:8px 0}
.fab{position:fixed;right:14px;bottom:14px;z-index:9}footer{padding:24px 16px;font-size:.85rem;color:#556;text-align:center}
.flag{display:flex;flex-wrap:wrap;gap:8px}.pill{padding:8px 14px;border:1px solid var(--ln);border-radius:99px;background:#fff;text-decoration:none}"""

HEAD_PWA = '<link rel="manifest" href="/manifest.webmanifest"><meta name="theme-color" content="#0f766e"><link rel="icon" href="/icons/icon-192.png"><link rel="apple-touch-icon" href="/icons/icon-192.png">'

def alt_hreflang(path_rel):
    """path_rel: ruta tras el prefijo de país ('' o 'samsung/neveras/')"""
    l = [f'<link rel="alternate" hreflang="{PA[c]["locale"]}" href="{DOM}/{c}/{path_rel}">' for c in PA]
    l.append(f'<link rel="alternate" hreflang="x-default" href="{DOM}/">')
    return "".join(l)

PAGES = []   # urls para sitemap

def page(ruta, title, desc, h1, body, bc=None, cc=None, rel=None, jsonld=None, geo=True, noscript=""):
    url = f"{DOM}/{ruta}"; PAGES.append(url)
    bch = ""
    if bc:
        bch = '<nav class="bc">' + " › ".join(f'<a href="{u}">{esc(t)}</a>' for t, u in bc) + "</nav>"
    ld = ""
    if jsonld:
        ld = "".join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in jsonld)
    hl = alt_hreflang(rel) if (cc and rel is not None) else ""
    gtm = f"<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s);j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i;f.parentNode.insertBefore(j,f)}})(window,document,'script','dataLayer','{CFG['gtm']}');</script>" if CFG["gtm"] else ""
    ver = f'<meta name="google-site-verification" content="{CFG["verificacion_gsc"]}">' if CFG["verificacion_gsc"] else ""
    locale = PA[cc]["locale"] if cc else "es"
    fab = f'<a class="b fab" id="fab" data-evt="whatsapp" href="{wa(cc, "Hola, necesito servicio técnico")}" rel="noopener">WhatsApp</a>' if cc else ""
    h = f"""<!doctype html><html lang="{locale}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{url}">{hl}{ver}{HEAD_PWA}
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="{url}">
<style>{CSS}</style>{ld}{gtm}</head><body{(' data-pais="'+cc+'"') if cc else ''}>
<header class="h"><div class="w">{bch}<h1>{esc(h1)}</h1></div></header>
<main class="w">{body}</main>{fab}
<footer>{esc(NOM)} · <a href="/">Cambiar país</a></footer>
{'<script src="/geo.js" defer></script>' if geo else ''}<script src="/app.js" defer></script></body></html>"""
    p = OUT / ruta / "index.html" if ruta else OUT / "index.html"
    p.parent.mkdir(parents=True, exist_ok=True); p.write_text(h, encoding="utf-8")

def faq_ld(pares):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pares]}

def bc_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}

def local_ld(cc, marca=None):
    p = PA[cc]
    return {"@context": "https://schema.org", "@type": "HomeAndConstructionBusiness", "name": f"{NOM} {p['nombre']}" + (f" – {marca}" if marca else ""),
            "url": f"{DOM}/{cc}/", "areaServed": [{"@type": "City", "name": c} for c in p["ciudades"]] + [{"@type": "Country", "name": p["nombre"]}],
            "telephone": p["tel"] or None, "priceRange": "$$", "knowsAbout": ["reparación de neveras", "reparación de lavadoras", "reparación de secadoras"]}

def build():
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    faltan = [c for c in PA if not PA[c]["wa"]]
    # ---- raíz
    datos = {c: {"n": p["nombre"], "wa": p["wa"], "dial": p["dial"], "ciudades": p["ciudades"]} for c, p in PA.items()}
    paises_html = "".join(f'<a class="pill" href="/{c}/">{esc(p["nombre"])}</a>' for c, p in PA.items())
    marcas_html = "".join(f'<a class="m" data-marca="{m}" data-nombre="{esc(v["nombre"])}" style="background:{v["color"]};color:{v.get("texto","#fff")}" href="#">{esc(v["nombre"])}<small style="display:block;font-weight:400">Servicio técnico</small></a>' for m, v in MA.items())
    body = f"""<section id="geo"><p><b>Encuentra tu servicio técnico más cercano.</b> Activa tu ubicación y te conectamos por WhatsApp con el técnico de tu país.</p>
<button class="b" id="geo-btn" type="button">📍 Usar mi ubicación</button> <span id="msg" role="status"></span>
<p style="font-size:.85rem;color:#556">Tu ubicación se usa solo en tu dispositivo para saber el país; no se guarda en ningún servidor.</p></section>
<h2>Elige tu marca</h2><div class="g" id="marcas">{marcas_html}</div>
<h2>O elige tu país</h2><div class="flag">{paises_html}</div>
<script type="application/json" id="datos">{json.dumps(datos, ensure_ascii=False)}</script>
<script type="application/json" id="marcasjs">{json.dumps({m: v["nombre"] for m, v in MA.items()}, ensure_ascii=False)}</script>"""
    page("", f"Servicio técnico de neveras, lavadoras y secadoras en Latinoamérica | {NOM}",
         "Servicio técnico a domicilio de Samsung, LG, Whirlpool, Mabe, Frigidaire, Electrolux y GE en Colombia, Panamá, Guatemala, El Salvador, Costa Rica, Ecuador, Paraguay y Chile. Activa tu ubicación y escribe por WhatsApp.",
         "Servicio técnico de electrodomésticos: detecta tu país y escribe por WhatsApp", body, jsonld=[{"@context":"https://schema.org","@type":"WebSite","name":NOM,"url":DOM+"/"}])
    # ---- países
    for cc, p in PA.items():
        pn = p["nombre"]
        marcas_g = "".join(f'<a class="m" style="background:{v["color"]};color:{v.get("texto","#fff")}" href="/{cc}/{m}/">Servicio técnico {esc(v["nombre"])} {esc(pn)}</a>' for m, v in MA.items())
        ciud = "".join(f'<a class="pill" href="/{cc}/{slug(c)}/">{esc(c)}</a>' for c in p["ciudades"])
        body = f"""<p>Reparamos neveras, lavadoras y secadoras a domicilio en {esc(pn)}. Escríbenos por WhatsApp con tu marca y la falla.</p>
<p><a class="b" data-evt="whatsapp" href="{wa(cc,'Hola, necesito servicio técnico en '+pn)}" rel="noopener">Escribir por WhatsApp</a></p>
<h2>Marcas que atendemos en {esc(pn)}</h2><div class="g">{marcas_g}</div>
<h2>Ciudades</h2><div class="flag">{ciud}</div>
<h2>Preguntas frecuentes en {esc(pn)}</h2>"""
        fq = [(f"¿Hacen servicio técnico a domicilio en {pn}?", f"Sí. Atendemos neveras, lavadoras y secadoras a domicilio en {', '.join(p['ciudades'])} y alrededores."),
              ("¿Cómo pido una visita?", "Escríbenos por WhatsApp con la marca, el modelo y la falla; te respondemos con el plazo de visita."),
              ("¿Qué marcas reparan?", "Samsung, LG, Whirlpool, Mabe, Frigidaire, Electrolux y General Electric.")]
        body += "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in fq)
        page(f"{cc}/", f"Servicio técnico de electrodomésticos en {pn} – neveras, lavadoras, secadoras | {NOM}",
             f"Reparación a domicilio de neveras, lavadoras y secadoras Samsung, LG, Whirlpool, Mabe, Frigidaire, Electrolux y GE en {pn}. Cotiza por WhatsApp.",
             f"Servicio técnico de electrodomésticos en {pn}", body, bc=[("Inicio", "/")], cc=cc, rel="",
             jsonld=[local_ld(cc), faq_ld(fq), bc_ld([("Inicio", DOM + "/"), (pn, f"{DOM}/{cc}/")])])
        # ciudades
        for c in p["ciudades"]:
            cs = slug(c)
            ml = "".join(f'<a class="m" style="background:{v["color"]};color:{v.get("texto","#fff")}" href="/{cc}/{cs}/{m}/">{esc(v["nombre"])} en {esc(c)}</a>' for m, v in MA.items())
            body = f"""<p>Servicio técnico a domicilio en {esc(c)}, {esc(pn)}: neveras, lavadoras y secadoras de todas las marcas.</p>
<p><a class="b" data-evt="whatsapp" href="{wa(cc,'Hola, necesito servicio técnico en '+c)}" rel="noopener">WhatsApp en {esc(c)}</a></p><div class="g">{ml}</div>"""
            page(f"{cc}/{cs}/", f"Servicio técnico de neveras, lavadoras y secadoras en {c}, {pn} | {NOM}",
                 f"Técnicos a domicilio en {c}, {pn}. Samsung, LG, Whirlpool, Mabe, Frigidaire, Electrolux y GE. Escríbenos por WhatsApp.",
                 f"Servicio técnico de electrodomésticos en {c}", body, bc=[("Inicio", "/"), (pn, f"/{cc}/")], cc=cc, rel=None,
                 jsonld=[local_ld(cc), bc_ld([("Inicio", DOM + "/"), (pn, f"{DOM}/{cc}/"), (c, f"{DOM}/{cc}/{cs}/")])])
            for m, v in MA.items():
                mn = v["nombre"]
                el = "".join(f'<a class="card" style="text-decoration:none;color:inherit" href="/{cc}/{m}/{k}/"><h3>{esc(e["corto"])} {esc(mn)} en {esc(c)}</h3><span>{esc(e["fallas"][0][0])}, {esc(e["fallas"][1][0].lower())}…</span></a>' for k, e in EQ.items())
                fq = [(f"¿Hacen servicio técnico {mn} a domicilio en {c}?", f"Sí. Visitamos hogares y negocios en {c}, {pn}, para neveras, lavadoras y secadoras {mn}."),
                      (f"¿Cómo contacto al técnico {mn} en {c}?", f"Toca el botón de WhatsApp, indica el modelo y la falla de tu equipo {mn} y te confirmamos la visita en {c}.")]
                body = f"""<p>Técnico {esc(mn)} en {esc(c)}, {esc(pn)}: diagnóstico y reparación a domicilio de neveras, lavadoras y secadoras {esc(mn)}.</p>
<p><a class="b" data-evt="whatsapp" href="{wa(cc,f'Hola, necesito servicio técnico {mn} en {c}, {pn}')}" rel="noopener">WhatsApp {esc(mn)} {esc(c)}</a></p><div class="g">{el}</div>
<h2>Preguntas frecuentes</h2>""" + "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in fq)
                page(f"{cc}/{cs}/{m}/", f"Servicio técnico {mn} en {c}, {pn} – neveras, lavadoras, secadoras | {NOM}",
                     f"Técnico {mn} a domicilio en {c}, {pn}: reparación de neveras, lavadoras y secadoras {mn}. Cotiza por WhatsApp.",
                     f"Servicio técnico {mn} en {c}, {pn}", body, bc=[("Inicio", "/"), (pn, f"/{cc}/"), (c, f"/{cc}/{cs}/")], cc=cc, rel=None,
                     jsonld=[local_ld(cc, mn), faq_ld(fq), bc_ld([("Inicio", DOM + "/"), (pn, f"{DOM}/{cc}/"), (c, f"{DOM}/{cc}/{cs}/"), (mn, f"{DOM}/{cc}/{cs}/{m}/")])])
        # marcas y equipos
        for m, v in MA.items():
            mn = v["nombre"]
            eqs = "".join(f'<a class="card" style="text-decoration:none;color:inherit" href="/{cc}/{m}/{k}/"><h3>{esc(e["corto"])} {esc(mn)}</h3><span>{esc(adapt(e["intro"],mn,p)[:110])}…</span></a>' for k, e in EQ.items())
            body = f"""<p>Servicio técnico oficial independiente de {esc(mn)} en {esc(pn)}. Diagnóstico y reparación a domicilio en {esc(', '.join(list(p['ciudades'])[:4]))} y más.</p>
<p><a class="b" data-evt="whatsapp" href="{wa(cc,'Hola, necesito servicio técnico '+mn+' en '+pn)}" rel="noopener">WhatsApp {esc(mn)} {esc(pn)}</a></p><div class="g">{eqs}</div>"""
            page(f"{cc}/{m}/", f"Servicio técnico {mn} {pn} – neveras, lavadoras, secadoras | {NOM}",
                 f"Servicio técnico {mn} en {pn}: reparación a domicilio de neveras, lavadoras y secadoras {mn}. Cotiza por WhatsApp.",
                 f"Servicio técnico {mn} en {pn}", body, bc=[("Inicio", "/"), (pn, f"/{cc}/")], cc=cc, rel=f"{m}/",
                 jsonld=[local_ld(cc, mn), bc_ld([("Inicio", DOM + "/"), (pn, f"{DOM}/{cc}/"), (mn, f"{DOM}/{cc}/{m}/")])])
            for k, e in EQ.items():
                fl = "".join(f'<div class="card"><h3>{esc(adapt(f[0],mn,p))}</h3><span class="urg">{esc(f[2])}</span><p>{esc(adapt(f[1],mn,p))}</p><p><i>{esc(adapt(f[3],mn,p))}</i></p></div>' for f in e["fallas"])
                fq = [(adapt(q, mn, p), adapt(a, mn, p)) for q, a in e["faq"]]
                mod = "".join(f"<li>{esc(x)}</li>" for x in e["modelos"])
                body = f"""<p>{esc(adapt(e['intro'],mn,p))}</p>
<p><a class="b" data-evt="whatsapp" href="{wa(cc,f'Hola, mi {e["sing"]} {mn} tiene una falla (en {pn})')}" rel="noopener">Cotizar por WhatsApp</a></p>
<h2>Fallas comunes en {esc(e['corto'].lower())} {esc(mn)}</h2><div class="g">{fl}</div>
<h2>Modelos que atendemos</h2><ul>{mod}</ul>
<h2>Preguntas frecuentes</h2>""" + "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in fq)
                t = adapt(e["titulo_h1"], mn, p)
                page(f"{cc}/{m}/{k}/", f"{t} | {NOM}", f"{t}. Reparación a domicilio, diagnóstico y garantía. Escríbenos por WhatsApp en {pn}.", t, body,
                     bc=[("Inicio", "/"), (pn, f"/{cc}/"), (mn, f"/{cc}/{m}/")], cc=cc, rel=f"{m}/{k}/",
                     jsonld=[local_ld(cc, mn), faq_ld(fq), bc_ld([("Inicio", DOM + "/"), (pn, f"{DOM}/{cc}/"), (mn, f"{DOM}/{cc}/{m}/"), (e["corto"], f"{DOM}/{cc}/{m}/{k}/")])])
    # ---- estáticos: geo.js, app.js, PWA, SEO
    ciudades = {c: [[n, la, lo] for n, (la, lo) in p["ciudades"].items()] for c, p in PA.items()}
    (OUT / "geo.js").write_text("""(function(){
var D=JSON.parse((document.getElementById('datos')||{textContent:'null'}).textContent)||%s;
function dist(a,b,c,d){var R=6371,r=Math.PI/180,x=(c-a)*r,y=(d-b)*r,h=Math.sin(x/2)*Math.sin(x/2)+Math.cos(a*r)*Math.cos(c*r)*Math.sin(y/2)*Math.sin(y/2);return 2*R*Math.asin(Math.sqrt(h));}
function nearest(lat,lon){var best=null;for(var cc in D){var cs=D[cc].ciudades;for(var n in cs){var d=dist(lat,lon,cs[n][0],cs[n][1]);if(!best||d<best.d)best={cc:cc,city:n,d:d};}}return best;}
var TZ={'America/Guatemala':'gt','America/Panama':'pa','America/Costa_Rica':'cr','America/Guayaquil':'ec','America/El_Salvador':'sv','America/Asuncion':'py','America/Bogota':'co','America/Santiago':'cl'};
function guardar(cc,city){try{localStorage.setItem('pais',cc);if(city)localStorage.setItem('ciudad',city);}catch(e){}}
function leer(){try{return localStorage.getItem('pais');}catch(e){return null;}}
function waLink(cc,marca){var n=D[cc].wa||(D[cc].dial+'00000000');return 'https://wa.me/'+n+'?text='+encodeURIComponent('Hola, necesito servicio técnico '+marca+' en '+D[cc].n);}
function aplicarRaiz(cc,city){
  document.querySelectorAll('#marcas a').forEach(function(a){a.href=waLink(cc,a.dataset.nombre);a.target='_blank';a.rel='noopener';a.setAttribute('data-evt','whatsapp');a.querySelector('small').textContent='WhatsApp '+D[cc].n+' →';});
  var m=document.getElementById('msg');if(m)m.innerHTML='Estás en <b>'+(city?city+', ':'')+D[cc].n+'</b>. Toca tu marca para escribir al técnico, o <a href="/'+cc+'/">ver página de '+D[cc].n+'</a>.';
}
function onPos(p){var n=nearest(p.coords.latitude,p.coords.longitude),m=document.getElementById('msg');
  if(!n||n.d>900){if(m)m.textContent='Aún no atendemos tu zona. Elige tu país abajo.';return;}
  guardar(n.cc,n.city);
  if(document.body.dataset.pais){ if(document.body.dataset.pais!==n.cc){banner(n);} return; }
  aplicarRaiz(n.cc,n.city);}
function onErr(e){var m=document.getElementById('msg');if(m)m.textContent=e&&e.code===1?'No diste permiso de ubicación. Elige tu país abajo.':'No pudimos obtener tu ubicación. Elige tu país abajo.';}
function banner(n){var b=document.createElement('div');b.style.cssText='background:#fff3cd;padding:10px 16px;text-align:center';b.innerHTML='Parece que estás en <b>'+D[n.cc].n+'</b>. <a href="/'+n.cc+'/">Ir al servicio técnico de '+D[n.cc].n+'</a>';document.body.prepend(b);}
var btn=document.getElementById('geo-btn');
if(btn)btn.addEventListener('click',function(){var m=document.getElementById('msg');if(!navigator.geolocation){m.textContent='Tu navegador no permite ubicación. Elige tu país abajo.';return;}m.textContent='Buscando tu ubicación…';navigator.geolocation.getCurrentPosition(onPos,onErr,{enableHighAccuracy:false,timeout:12000,maximumAge:600000});});
// sin permiso: país recordado o zona horaria (solo sugerencia)
if(!document.body.dataset.pais&&document.getElementById('marcas')){var cc=leer();if(!cc){try{cc=TZ[Intl.DateTimeFormat().resolvedOptions().timeZone];}catch(e){}}
  if(cc&&D[cc]){aplicarRaiz(cc,localStorage.getItem('ciudad'));}}
})();""" % json.dumps({c: {"n": p["nombre"], "wa": p["wa"], "dial": p["dial"], "ciudades": p["ciudades"]} for c, p in PA.items()}, ensure_ascii=False), encoding="utf-8")
    (OUT / "app.js").write_text("""if('serviceWorker' in navigator){addEventListener('load',function(){navigator.serviceWorker.register('/sw.js').catch(function(){});});}
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('[data-evt="whatsapp"]');if(a){window.dataLayer=window.dataLayer||[];window.dataLayer.push({event:'whatsapp',pais:document.body.dataset.pais||''});}});""", encoding="utf-8")
    (OUT / "sw.js").write_text("""var V='st-v1',SHELL=['/','/geo.js','/app.js','/manifest.webmanifest'];
self.addEventListener('install',function(e){e.waitUntil(caches.open(V).then(function(c){return c.addAll(SHELL);}));self.skipWaiting();});
self.addEventListener('activate',function(e){e.waitUntil(caches.keys().then(function(k){return Promise.all(k.filter(function(x){return x!==V;}).map(function(x){return caches.delete(x);}));}));self.clients.claim();});
self.addEventListener('fetch',function(e){if(e.request.method!=='GET')return;e.respondWith(fetch(e.request).then(function(r){var c=r.clone();caches.open(V).then(function(ch){ch.put(e.request,c);});return r;}).catch(function(){return caches.match(e.request).then(function(r){return r||caches.match('/');});}));});""", encoding="utf-8")
    (OUT / "manifest.webmanifest").write_text(json.dumps({"name": NOM, "short_name": "Servicio Técnico", "start_url": "/", "display": "standalone", "background_color": "#f6f8fa", "theme_color": "#0f766e", "lang": "es",
        "icons": [{"src": "/icons/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}]}, ensure_ascii=False), encoding="utf-8")
    (OUT / "icons").mkdir()
    from PIL import Image, ImageDraw
    for s in (192, 512):
        im = Image.new("RGB", (s, s), "#0f766e"); d = ImageDraw.Draw(im)
        d.ellipse([s*.3, s*.18, s*.7, s*.58], fill="white"); d.polygon([(s*.5, s*.84), (s*.34, s*.5), (s*.66, s*.5)], fill="white"); d.ellipse([s*.42, s*.3, s*.58, s*.46], fill="#0f766e")
        im.save(OUT / "icons" / f"icon-{s}.png")
    urls = "".join(f"<url><loc>{u}</loc></url>" for u in sorted(set(PAGES)))
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>', encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {DOM}/sitemap.xml\n", encoding="utf-8")
    (OUT / "llms.txt").write_text(f"# {NOM}\n> Servicio técnico a domicilio de neveras, lavadoras y secadoras Samsung, LG, Whirlpool, Mabe, Frigidaire, Electrolux y GE en " + ", ".join(p["nombre"] for p in PA.values()) + ".\n" + "".join(f"- {p['nombre']}: {DOM}/{c}/\n" for c, p in PA.items()), encoding="utf-8")
    (OUT / ".htaccess").write_text("DirectoryIndex index.html\nAddType application/manifest+json .webmanifest\nHeader set Permissions-Policy \"geolocation=(self)\"\n", encoding="utf-8")
    print(f"{len(set(PAGES))} páginas")
    if faltan:
        msg = "FALTAN números de WhatsApp en config.json para: " + ", ".join(PA[c]["nombre"] for c in faltan)
        print("⚠ " + msg)
        if ESTRICTO: sys.exit(1)

build()
