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
import importlib.util
def _cargar(m):
    d = {"mabe": "servicio-tecnico-mabe-centro"}.get(m, f"servicio-tecnico-{m}-panama")
    p = S / d / "_fuente" / "contenido.py"
    sp = importlib.util.spec_from_file_location("c_" + m.replace("-", "_"), p); mod = importlib.util.module_from_spec(sp)
    sys.path.insert(0, str(p.parent)); sp.loader.exec_module(mod); sys.path.pop(0)
    return {k: mod.EQUIPOS[k] for k in ("neveras", "lavadoras", "secadoras")}
EQB = {m: _cargar(m) for m in MA}   # contenido propio de cada marca: no se mezclan términos
EQ = EQB["samsung"]
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

from zonas import Z as ZONAS_X
CSSF = (RAIZ / "_fuente" / "estilo.css").read_text(encoding="utf-8")

# ---------- vocabulario por país ----------
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
def sing(cc, k):
    t = term(cc, k)
    return t if t.endswith("opas") else (t[:-2] if t.endswith("es") and t[:-2].endswith("r") else (t[:-1] if t.endswith("s") else t))
BASE_W = {"neveras": ("nevera", "neveras"), "lavadoras": ("lavadora", "lavadoras"), "secadoras": ("secadora", "secadoras")}

def txt(t, m, cc, k=None):
    """Adapta un texto de Samsung/Panamá a otra marca y país (marca, nombre del país, palabra local del equipo)."""
    mn = MA[m]["nombre"]; pn = PA[cc]["nombre"] if cc else "tu país"
    t = t.replace("Samsung", mn).replace("Ciudad de Panamá", pn).replace("Panamá", pn)
    t = re.sub(r"\b(refrigeradoras?|refrigeradores|heladeras?|neveras?) y refrigeradoras\b", r"\1", t)
    if cc and k:
        s, p = BASE_W[k]; ts, tp = sing(cc, k), term(cc, k)
        for a, b in ((p, tp), (s, ts)):
            t = re.sub(rf"\b{a}\b", b, t); t = re.sub(rf"\b{a.capitalize()}\b", b.capitalize(), t)
        if ts.endswith("or"):   # refrigerador: masculino
            t = re.sub(rf"\b([Ll])a {ts}", lambda x: x.group(1) + "a " + ts if False else ("E" if x.group(1) == "L" else "e") + f"l {ts}", t)
            t = re.sub(rf"\buna {ts}", f"un {ts}", t); t = re.sub(rf"\besta {ts}", f"este {ts}", t); t = re.sub(rf"\blas {tp}", f"los {tp}", t); t = re.sub(rf"\bLas {tp}", f"Los {tp}", t)
    t = re.sub(r"\b(refrigeradoras?|refrigeradores|heladeras?|neveras?) y refrigeradoras\b", r"\1", t)
    return t

def cap(s): return s[:1].upper() + s[1:]

def ciudad_pais(cc, ci): return f"{ci}, {PA[cc]['nombre']}" if ci else PA[cc]["nombre"]

# ---------- zonas ----------
def zonas_de(cc):
    if cc == "pa": return [(n, t, c if c in PA["pa"]["ciudades"] else "Ciudad de Panamá") for n, t, c in base.ZONAS]
    return [(n, t, c if c in PA[cc]["ciudades"] else list(PA[cc]["ciudades"])[0]) for n, t, c in ZONAS_X.get(cc, [])]

# ---------- códigos de error (solo los que conozco con certeza) ----------
CODIGOS = {
 "samsung": [("4C / 4E", "No entra agua", "Llave cerrada, manguera doblada, filtro de la entrada tapado o presión baja."), ("5C / 5E / SE", "No desagua", "Manguera de desagüe doblada o tapada, filtro de la bomba sucio o bomba de desagüe."), ("UE / UB", "Carga desbalanceada", "Ropa amontonada o muy pesada, equipo desnivelado."), ("LE / LC", "Fuga de agua", "Mangueras o sellos que gotean; apaga y cierra la llave."), ("dC / dE", "Puerta mal cerrada", "Seguro de la puerta o ropa que impide cerrar."), ("HE / HC", "Calentamiento", "Resistencia o sensor de temperatura."), ("3E", "Motor", "Motor o sensor de giro; requiere revisión técnica.")],
 "lg": [("OE", "No desagua", "Manguera doblada, filtro de la bomba tapado o bomba."), ("IE", "No entra agua", "Llave cerrada, manguera o filtro de entrada."), ("UE", "Carga desbalanceada", "Ropa mal repartida o equipo desnivelado."), ("dE / DE", "Puerta abierta", "Puerta mal cerrada o seguro con falla."), ("FE", "Exceso de agua", "Válvula de entrada o sensor de nivel."), ("LE", "Motor bloqueado", "Motor o sobrecarga; requiere revisión."), ("PE", "Sensor de presión", "Sensor de nivel de agua."), ("tE", "Sensor de temperatura", "Termistor o resistencia.")],
}

PAGES = []
def hreflangs(m, rel):
    return "".join(f'<link rel="alternate" hreflang="{PA[c]["locale"]}" href="{DOM}/{m}/{c}/{rel}">' for c in PA) + f'<link rel="alternate" hreflang="x-default" href="{DOM}/{m}/">'

def wa(num, texto=""): return f"https://wa.me/{num}" + (f"?text={quote(texto)}" if texto else "")

def orden_json(m, cc):
    mn = MA[m]["nombre"]; eq = {}
    for k, e in EQ.items():
        eq[k] = dict(t=term(cc, k) if cc else e["corto"].lower(), img=f"/img/{m}/{k}.jpg", alt=ALT(m, k, PA[cc]["nombre"] if cc else None),
                     fallas=[[txt(f[0], m, cc, k), txt(f[0], m, cc, k), f[2]] for f in e["fallas"]])
    return json.dumps({"equipos": eq}, ensure_ascii=False, separators=(",", ":"))

def page(ruta, title, desc, h1, sub, body, bc=None, m=None, cc=None, rel=None, jsonld=None, eq=None, falla=None, orden=True, fab=True):
    url = f"{DOM}/{ruta}"; PAGES.append(url)
    mc = MA[m]["color"] if m else "#0f766e"; mt = MA[m].get("texto", "#fff") if m else "#fff"
    bch = '<nav class="bc" aria-label="Migas de pan">' + " › ".join(f'<a href="{u}">{esc(t)}</a>' for t, u in bc) + "</nav>" if bc else ""
    ld = "".join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in (jsonld or []))
    hl = hreflangs(m, rel) if (m and cc and rel is not None) else ""
    gtm = f"<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s);j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i;f.parentNode.insertBefore(j,f)}})(window,document,'script','dataLayer','{CFG['gtm']}');</script>" if CFG["gtm"] else ""
    ver = f'<meta name="google-site-verification" content="{CFG["verificacion_gsc"]}">' if CFG["verificacion_gsc"] else ""
    man = f"/{m}/manifest.webmanifest" if m else "/manifest.webmanifest"
    ico = f"/img/{m}/logo.png" if m else "/icons/icon-192.png"
    img = f"{DOM}/img/{m}/tecnico.jpg" if m else f"{DOM}/icons/icon-512.png"
    logo = f'<a class="lg" href="/{m}/"><img src="/img/{m}/logo.png" alt="{esc(ALT(m,"logo"))}" height="30"></a>' if m else f'<span style="font-weight:800">{esc(NOM)}</span>'
    locale = PA[cc]["locale"] if cc else "es"
    wnum = PA[cc]["wa"] if cc else ""
    fb = f'<a class="btn wa fab" data-evt="whatsapp" id="fab" href="{wa(wnum, "Hola, necesito servicio técnico " + MA[m]["nombre"] + " en " + PA[cc]["nombre"])}" rel="noopener">WhatsApp</a>' if (fab and cc and m) else ""
    ordh = ""
    if orden and m:
        ordh = f'<section class="ord" id="orden" aria-label="Solicitud de servicio técnico {esc(MA[m]["nombre"])}"><h2>Pide tu servicio técnico {esc(MA[m]["nombre"])}</h2><p class="ay">Cuéntanos tu equipo y la falla; te conectamos por WhatsApp.</p>' + (f'<a class="btn wa" data-evt="whatsapp" href="{wa(wnum, "Hola, necesito servicio técnico " + MA[m]["nombre"])}">Escribir por WhatsApp</a>' if cc else "") + '</section>'
        ordh += f'<script>window.ORDEN={orden_json(m, cc)};</script>'
    h = f"""<!doctype html><html lang="{locale}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{url}">{hl}{ver}
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1"><meta name="geo.region" content="{cc.upper() if cc else ''}">
<link rel="manifest" href="{man}"><meta name="theme-color" content="{mc}"><link rel="icon" href="{ico}"><link rel="apple-touch-icon" href="{ico}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="{url}"><meta property="og:image" content="{img}"><meta property="og:locale" content="{locale.replace('-','_')}">
<link rel="stylesheet" href="/estilo.css">{ld}{gtm}</head><body data-marca="{m or ''}" data-nombre="{esc(MA[m]['nombre']) if m else ''}" data-pais="{cc or ''}" data-equipo="{eq or ''}" data-falla="{esc(falla or '')}" style="--mc:{mc};--mt:{mt}">
<header class="h"><div class="w"><div class="top">{logo}<a class="al" href="/">Todas las marcas</a></div>{bch}<h1>{esc(h1)}</h1><p class="sub">{esc(sub)}</p></div></header>
<main class="w">{ordh}{body}</main>{fb}
<footer>{esc(NOM)}{(' · Servicio técnico ' + esc(MA[m]['nombre'])) if m else ''}. Las marcas y logos pertenecen a sus respectivos propietarios.</footer>
<script src="/datos.js" defer></script><script src="/orden.js" defer></script><script src="/app.js" defer></script></body></html>"""
    p = OUT / ruta / "index.html" if ruta else OUT / "index.html"
    p.parent.mkdir(parents=True, exist_ok=True); p.write_text(h, encoding="utf-8")

def sec(t, inner): return f'<section class="sec"><h2>{t}</h2>{inner}</section>'
def faqh(fq): return "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in fq)
def faq_ld(pares): return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pares]}
def bc_ld(items): return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}
def how_ld(m, cc):
    mn = MA[m]["nombre"]
    return {"@context": "https://schema.org", "@type": "HowTo", "name": f"Cómo pedir un técnico {mn} en {PA[cc]['nombre']}", "step": [
        {"@type": "HowToStep", "name": "Activa tu ubicación", "text": "Permite la ubicación o elige tu país y ciudad."},
        {"@type": "HowToStep", "name": "Elige el equipo", "text": f"Nevera, lavadora o secadora {mn}."},
        {"@type": "HowToStep", "name": "Elige la falla", "text": "Selecciona el problema que más se parece al tuyo."},
        {"@type": "HowToStep", "name": "Envía la solicitud por WhatsApp", "text": "Recibes respuesta del técnico más cercano."}]}
def svc_ld(m, cc, ci=None, k=None):
    p = PA[cc]; mn = MA[m]["nombre"]; lugar = ci or p["nombre"]
    nom = f"Servicio técnico {mn}" + (f" de {term(cc,k)}" if k else "") + f" en {lugar}"
    return {"@context": "https://schema.org", "@type": "HomeAndConstructionBusiness", "name": nom, "url": f"{DOM}/{m}/{cc}/", "image": f"{DOM}/img/{m}/tecnico.jpg", "telephone": p["tel"] or None, "priceRange": "$$",
            "areaServed": ([{"@type": "City", "name": ci}] if ci else [{"@type": "City", "name": c} for c in p["ciudades"]]) + [{"@type": "Country", "name": p["nombre"]}],
            "makesOffer": {"@type": "Offer", "itemOffered": {"@type": "Service", "name": nom}}, "knowsAbout": [f"reparación de {term(cc,x)} {mn}" for x in EQ]}

def faq_gen(m, cc, ci=None, k=None):
    mn = MA[m]["nombre"]; p = PA[cc]; lugar = ci or p["nombre"]; eqn = f"{term(cc,k)} {mn}" if k else f"{term(cc,'neveras')}, {term(cc,'lavadoras')} y {term(cc,'secadoras')} {mn}"
    cs = ", ".join(p["ciudades"])
    return [
     (f"¿Hacen servicio técnico {mn} a domicilio en {lugar}?", f"Sí. Vamos a tu casa, apartamento u oficina en {lugar} para revisar y reparar {eqn}. Escríbenos por WhatsApp o usa la solicitud de esta página."),
     (f"¿Cómo pido el técnico {mn} más cercano a mi barrio?", f"Toca «Usar mi ubicación» en la solicitud, elige el equipo y la falla, y envía. La aplicación detecta tu barrio y manda tu solicitud al técnico {mn} más cercano por WhatsApp."),
     (f"¿Cuánto cuesta reparar {eqn} en {lugar}?", f"Depende de la falla, de la pieza y de la mano de obra. Te damos el costo en {p['moneda']} antes de empezar y no se repara nada sin tu aprobación."),
     (f"¿Cuánto tarda la reparación de {eqn}?", "Muchas fallas se resuelven en la misma visita. Si hay que conseguir una pieza, te avisamos el plazo antes de empezar."),
     (f"¿Qué garantía tiene la reparación de {eqn}?", "Cada reparación incluye garantía sobre la pieza instalada y la mano de obra; el plazo se confirma antes de reparar."),
     (f"¿Atienden urgencias y fines de semana en {lugar}?", "Coordinamos la visita según la urgencia. Si tu equipo no enfría o hay fuga de agua, indícalo en la solicitud para darle prioridad."),
     (f"¿En qué ciudades de {p['nombre']} atienden {mn}?", f"Atendemos {cs} y zonas cercanas."),
     (f"¿Vale la pena reparar mi equipo {mn} o comprar uno nuevo?", "Si la falla es de una pieza accesible, casi siempre conviene reparar. Si el costo se acerca al de un equipo nuevo, te lo decimos con honestidad."),
     (f"¿Qué necesito para pedir el servicio?", f"Marca, tipo de equipo, la falla y tu ubicación. El modelo ayuda mucho: está en la etiqueta del equipo.")]

def kw_list(m, cc, ci=None, k=None, falla=None, zona=None):
    mn = MA[m]["nombre"]; p = PA[cc]["nombre"]; lugar = zona or ci or p
    ks = [k] if k else list(EQ)
    out = [f"servicio técnico {mn} {lugar}", f"técnico {mn} a domicilio {lugar}", f"servicio técnico {mn} cerca de mí", f"teléfono servicio técnico {mn} {p}", f"whatsapp servicio técnico {mn} {p}", f"técnico {mn} más cercano"]
    for x in ks:
        t = term(cc, x); a = alt(cc, x); s = sing(cc, x)
        out += [f"reparación de {t} {mn} {lugar}", f"arreglar {s} {mn} {lugar}", f"{s} {mn} no funciona", f"cuánto cuesta reparar {s} {mn}", f"mantenimiento de {s} {mn}"]
        if a: out.append(f"reparación de {a} {mn} {lugar}")
        if falla: out.append(f"{txt(falla,m,cc,x).lower()} {mn}")
    return list(dict.fromkeys(out))
def kw_html(*a, **kw): return "<ul class='kw'>" + "".join(f"<li>{esc(x)}</li>" for x in kw_list(*a, **kw)) + "</ul>"
def pills(items): return "".join(f'<a class="pill" href="{u}">{esc(t)}</a>' for t, u in items)

def build():
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    copiar_imagenes()
    faltan = [c for c in PA if not PA[c]["wa"]]
    shutil.copy(RAIZ / "_fuente" / "estilo.css", OUT / "estilo.css"); shutil.copy(RAIZ / "_fuente" / "orden.js", OUT / "orden.js")
    # ---- raíz
    mc = "".join(f'<a href="/{m}/" style="--mc:{v["color"]}"><div class="bar"></div><img class="t" loading="lazy" src="/img/{m}/tecnico.jpg" alt="{esc(ALT(m,"tecnico"))}" width="400" height="300"><div class="in"><span class="lg"><img src="/img/{m}/logo.png" alt="{esc(ALT(m,"logo"))}" height="30"></span><h3>Servicio técnico {esc(v["nombre"])}</h3><span style="color:var(--mu);font-size:.9rem">Neveras, lavadoras y secadoras</span></div></a>' for m, v in MA.items())
    body = f'<section class="ord" id="marcas"><h2>Elige tu marca</h2><p class="ay">Cada marca tiene su propia solicitud de servicio.</p><div class="mk">{mc}</div></section>' + sec("Países donde trabajamos", "<p>" + ", ".join(esc(p["nombre"]) for p in PA.values()) + ".</p>")
    page("", f"Servicio técnico por marca en Latinoamérica: neveras, lavadoras y secadoras | {NOM}",
         "Pide tu técnico Samsung, LG, Whirlpool, Mabe, Frigidaire, Electrolux o GE. Detectamos tu barrio, eliges el equipo y la falla, y enviamos la solicitud por WhatsApp. Colombia, Panamá, Guatemala, El Salvador, Costa Rica, Ecuador, Paraguay y Chile.",
         "Servicio técnico por marca, en tu barrio", "Elige tu marca, cuéntanos la falla y te conectamos por WhatsApp con el técnico más cercano.", body, orden=False,
         jsonld=[{"@context": "https://schema.org", "@type": "WebSite", "name": NOM, "url": DOM + "/"}], fab=False)
    for m, v in MA.items():
        mn = v["nombre"]; tt = TEC.get(m, []); globals()["EQ"] = EQB[m]
        (OUT / m).mkdir(exist_ok=True)
        (OUT / m / "tecnicos.json").write_text(json.dumps(tt, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        (OUT / m / "manifest.webmanifest").write_text(json.dumps({"name": f"Servicio técnico {mn}", "short_name": mn, "start_url": f"/{m}/", "scope": f"/{m}/", "display": "standalone", "background_color": "#ffffff", "theme_color": v["color"], "lang": "es",
            "icons": [{"src": f"/img/{m}/logo.png", "sizes": "512x512", "type": "image/png", "purpose": "any"}]}, ensure_ascii=False), encoding="utf-8")
        # ---- home de marca
        fq = faq_gen(m, "pa")[:0]
        eqc = "".join(f'<div class="cd"><img src="/img/{m}/{k}.jpg" alt="{esc(ALT(m,k))}" loading="lazy" style="width:100%;aspect-ratio:16/10;object-fit:contain;background:#fff;border-radius:10px"><h3>{esc(e["corto"])} {esc(mn)}</h3><p style="color:var(--mu);margin:0">{esc(txt(e["intro"],m,None)[:140])}…</p></div>' for k, e in EQ.items())
        fqb = [(f"¿Qué equipos {mn} reparan?", f"Neveras (refrigeradoras, heladeras), lavadoras (lavarropas) y secadoras {mn}."),
               (f"¿En qué países hay servicio técnico {mn}?", "En " + ", ".join(p["nombre"] for p in PA.values()) + "."),
               (f"¿Cómo funciona la solicitud de servicio {mn}?", "Activas tu ubicación, eliges el equipo y la falla, y enviamos tu solicitud por WhatsApp al técnico más cercano."),
               (f"¿Cuánto cuesta el servicio técnico {mn}?", "Depende de la falla y la pieza. Te cotizamos antes de reparar, sin compromiso.")]
        body = sec("Elige tu país", pills([(p["nombre"], f"/{m}/{c}/") for c, p in PA.items()])) + sec(f"Equipos {mn} que reparamos", f'<div class="g">{eqc}</div>') \
            + sec("Preguntas frecuentes", faqh(fqb)) + sec(f"Búsquedas relacionadas con servicio técnico {mn}", "<ul class='kw'>" + "".join(f"<li>servicio técnico {esc(mn)} {esc(p['nombre'])}</li>" for p in PA.values()) + "</ul>")
        page(f"{m}/", f"Servicio técnico {mn}: pide tu técnico más cercano por WhatsApp | {NOM}",
             f"Servicio técnico {mn} a domicilio en 8 países. Activa tu ubicación, elige tu equipo y la falla, y envía tu solicitud por WhatsApp al técnico {mn} más cercano a tu barrio.",
             f"Servicio técnico {mn}", f"Pide tu técnico {mn} más cercano. Reparación a domicilio de neveras, lavadoras y secadoras.", body, bc=[("Inicio", "/")], m=m, rel=None,
             jsonld=[faq_ld(fqb), bc_ld([("Inicio", DOM + "/"), (mn, f"{DOM}/{m}/")])], fab=False)
        for cc, p in PA.items():
            pn = p["nombre"]; zs = zonas_de(cc)
            base_bc = [("Inicio", "/"), (mn, f"/{m}/")]
            # ---- país
            fq = faq_gen(m, cc)
            eqcards = "".join(f'<a class="cd" href="/{m}/{cc}/{k}/"><img src="/img/{m}/{k}.jpg" alt="{esc(ALT(m,k,pn))}" loading="lazy"><h3>{esc(cap(term(cc,k)))} {esc(mn)} en {esc(pn)}</h3></a>' for k in EQ)
            body = sec(f"Equipos {mn} que reparamos en {pn}", f'<div class="g">{eqcards}</div>') \
                + sec(f"Ciudades con técnico {mn} en {pn}", pills([(c, f"/{m}/{cc}/{slug(c)}/") for c in p["ciudades"]])) \
                + sec(f"Barrios y zonas donde atendemos {mn}", pills([(n, f"/{m}/{cc}/barrios/{slug(n)}/") for n, t, c in zs])) \
                + sec("Más ayuda", pills([("Preguntas frecuentes", f"/{m}/{cc}/preguntas-frecuentes/"), ("Técnico cerca de mí", f"/{m}/{cc}/cerca-de-mi/")])) \
                + sec(f"Preguntas frecuentes sobre servicio técnico {mn} en {pn}", faqh(fq)) + sec("Búsquedas relacionadas", kw_html(m, cc))
            page(f"{m}/{cc}/", f"Servicio técnico {mn} en {pn}: {term(cc,'neveras')}, {term(cc,'lavadoras')} y {term(cc,'secadoras')} | {NOM}",
                 f"Servicio técnico {mn} en {pn}: reparación a domicilio de {term(cc,'neveras')}, {term(cc,'lavadoras')} y {term(cc,'secadoras')} {mn}. Pide el técnico más cercano a tu barrio por WhatsApp.",
                 f"Servicio técnico {mn} en {pn}", f"Reparación a domicilio de {term(cc,'neveras')}, {term(cc,'lavadoras')} y {term(cc,'secadoras')} {mn} en {', '.join(list(p['ciudades'])[:3])} y más.", body,
                 bc=base_bc, m=m, cc=cc, rel="", jsonld=[svc_ld(m, cc), how_ld(m, cc), faq_ld(fq), bc_ld([("Inicio", DOM + "/"), (mn, f"{DOM}/{m}/"), (pn, f"{DOM}/{m}/{cc}/")])])
            bc_p = base_bc + [(pn, f"/{m}/{cc}/")]
            # ---- preguntas frecuentes (hub) y cerca de mí
            big = faq_gen(m, cc)
            for k, e in EQ.items(): big += [(txt(q, m, cc, k), txt(a, m, cc, k)) for q, a in e["faq"]]
            big = list(dict.fromkeys(big))
            page(f"{m}/{cc}/preguntas-frecuentes/", f"Preguntas frecuentes del servicio técnico {mn} en {pn} | {NOM}", f"Respuestas sobre precios, tiempos, garantía y cobertura del servicio técnico {mn} en {pn}: neveras, lavadoras y secadoras.",
                 f"Preguntas frecuentes: servicio técnico {mn} en {pn}", "Costos, tiempos, garantía y cobertura, explicados claro.", sec("Todas las preguntas", faqh(big)) + sec("Búsquedas relacionadas", kw_html(m, cc)),
                 bc=bc_p, m=m, cc=cc, rel="preguntas-frecuentes/", jsonld=[faq_ld(big), bc_ld([("Inicio", DOM + "/"), (mn, f"{DOM}/{m}/"), (pn, f"{DOM}/{m}/{cc}/"), ("Preguntas frecuentes", f"{DOM}/{m}/{cc}/preguntas-frecuentes/")])], orden=False)
            page(f"{m}/{cc}/cerca-de-mi/", f"Servicio técnico {mn} cerca de mí en {pn} | {NOM}", f"Encuentra el técnico {mn} más cercano a ti en {pn}: activa tu ubicación y envía tu solicitud por WhatsApp.",
                 f"Servicio técnico {mn} cerca de mí en {pn}", "Activa tu ubicación y te mostramos el técnico más cercano a tu barrio.", sec("Ciudades y barrios cercanos", pills([(c, f"/{m}/{cc}/{slug(c)}/") for c in p["ciudades"]]) + pills([(n, f"/{m}/{cc}/barrios/{slug(n)}/") for n, t, c in zs[:8]])) + sec("Búsquedas relacionadas", kw_html(m, cc)),
                 bc=bc_p, m=m, cc=cc, rel="cerca-de-mi/", jsonld=[svc_ld(m, cc), bc_ld([("Inicio", DOM + "/"), (mn, f"{DOM}/{m}/"), (pn, f"{DOM}/{m}/{cc}/"), ("Cerca de mí", f"{DOM}/{m}/{cc}/cerca-de-mi/")])])
            # ---- ciudades
            for ci in p["ciudades"]:
                cs = slug(ci); tecs = [t for t in tt if t["p"] == cc and t["c"] == ci]; fq = faq_gen(m, cc, ci)
                th = "".join(f'<div class="cd"><b>{esc(t["n"])}</b><br><span style="color:var(--mu)">{esc(t["z"])}, {esc(ci)}</span><p><a class="pill" data-evt="whatsapp" href="{wa(t["w"], f"Hola, necesito servicio técnico {mn} en {ci}")}" rel="noopener">WhatsApp</a></p></div>' for t in tecs)
                zc = [(n, f"/{m}/{cc}/barrios/{slug(n)}/") for n, t, c in zs if c == ci]
                eqh = "".join(f'<a class="cd" href="/{m}/{cc}/{cs}/{k}/"><img src="/img/{m}/{k}.jpg" alt="{esc(ALT(m,k,ci))}" loading="lazy"><h3>{esc(cap(term(cc,k)))} {esc(mn)} en {esc(ci)}</h3></a>' for k in EQ)
                body = sec(f"Técnicos {mn} en {ci}", f'<div class="g">{th}</div>') + sec(f"Equipos {mn} que reparamos en {ci}", f'<div class="g">{eqh}</div>') \
                    + (sec(f"Barrios de {ci} donde atendemos", pills(zc)) if zc else "") + sec(f"Preguntas frecuentes en {ci}", faqh(fq)) + sec("Búsquedas relacionadas", kw_html(m, cc, ci=ci))
                page(f"{m}/{cc}/{cs}/", f"Servicio técnico {mn} en {ci}, {pn}: {term(cc,'neveras')}, lavadoras y secadoras | {NOM}",
                     f"Servicio técnico {mn} cerca de ti en {ci}, {pn}: reparación a domicilio de {term(cc,'neveras')}, {term(cc,'lavadoras')} y {term(cc,'secadoras')} {mn}. WhatsApp del técnico más cercano a tu barrio.",
                     f"Servicio técnico {mn} en {ci}", f"Técnico {mn} a domicilio en {ci}, {pn}.", body, bc=bc_p, m=m, cc=cc, rel=None,
                     jsonld=[svc_ld(m, cc, ci), faq_ld(fq), bc_ld([("Inicio", DOM + "/"), (mn, f"{DOM}/{m}/"), (pn, f"{DOM}/{m}/{cc}/"), (ci, f"{DOM}/{m}/{cc}/{cs}/")])])
                for k, e in EQ.items():
                    fq = faq_gen(m, cc, ci, k) + [(txt(q, m, cc, k), txt(a, m, cc, k)) for q, a in e["faq"][:3]]
                    fl = pills([(txt(f[0], m, cc, k), f"/{m}/{cc}/{k}/{slug(f[0])}/") for f in e["fallas"][:6]])
                    body = sec(f"Fallas frecuentes en {term(cc,k)} {mn} en {ci}", fl) + sec(f"Preguntas frecuentes", faqh(fq)) + sec("Búsquedas relacionadas", kw_html(m, cc, ci=ci, k=k)) \
                        + sec("Más cerca de ti", pills([(f"{mn} en {ci}", f"/{m}/{cc}/{cs}/"), (f"{cap(term(cc,k))} {mn} en {pn}", f"/{m}/{cc}/{k}/")]))
                    t = f"Reparación de {term(cc,k)} {mn} en {ci}"
                    page(f"{m}/{cc}/{cs}/{k}/", f"{t}, {pn}: técnico a domicilio | {NOM}", f"{t}: técnico {mn} a domicilio en {ci}, {pn}. Diagnóstico, repuestos y garantía. Pide tu solicitud por WhatsApp.", t,
                         f"Técnico {mn} a domicilio en {ci}, {pn}.", body, bc=bc_p + [(ci, f"/{m}/{cc}/{cs}/")], m=m, cc=cc, rel=None, eq=k,
                         jsonld=[svc_ld(m, cc, ci, k), faq_ld(fq), bc_ld([("Inicio", DOM + "/"), (mn, f"{DOM}/{m}/"), (pn, f"{DOM}/{m}/{cc}/"), (ci, f"{DOM}/{m}/{cc}/{cs}/"), (cap(term(cc, k)), f"{DOM}/{m}/{cc}/{cs}/{k}/")])])
            # ---- barrios / zonas
            for n, tipo, ci in zs:
                a, b = base.TIPO_TXT[tipo]; fq = faq_gen(m, cc, ci)[:6]
                body = sec(f"Servicio técnico {mn} en {n}", f"<p>{esc(txt(a,m,cc))}</p><p>{esc(txt(b,m,cc))}</p>") + sec(f"Equipos {mn} que reparamos en {n}", pills([(f"{cap(term(cc,k))} {mn}", f"/{m}/{cc}/{k}/") for k in EQ])) \
                    + sec("Preguntas frecuentes", faqh(fq)) + sec("Búsquedas relacionadas", kw_html(m, cc, ci=ci, zona=n)) + sec("Cerca de aquí", pills([(f"{mn} en {ci}", f"/{m}/{cc}/{slug(ci)}/")]))
                page(f"{m}/{cc}/barrios/{slug(n)}/", f"Servicio técnico {mn} en {n}, {ci}: neveras, lavadoras y secadoras | {NOM}",
                     f"Técnico {mn} a domicilio en {n}, {ci} ({pn}): reparación de {term(cc,'neveras')}, {term(cc,'lavadoras')} y {term(cc,'secadoras')} {mn}. Pide tu solicitud por WhatsApp.",
                     f"Servicio técnico {mn} en {n}, {ci}", f"Técnico {mn} a domicilio en el barrio {n}.", body, bc=bc_p, m=m, cc=cc, rel=None,
                     jsonld=[svc_ld(m, cc, ci), faq_ld(fq), bc_ld([("Inicio", DOM + "/"), (mn, f"{DOM}/{m}/"), (pn, f"{DOM}/{m}/{cc}/"), (n, f"{DOM}/{m}/{cc}/barrios/{slug(n)}/")])])
            # ---- equipos, fallas, mantenimiento, costo, códigos
            for k, e in EQ.items():
                eqn = f"{term(cc,k)} {mn}"; t = f"Servicio técnico de {eqn} en {pn}"; a2 = alt(cc, k)
                fl = "".join(f'<a class="cd" href="/{m}/{cc}/{k}/{slug(f[0])}/"><span class="urg">{esc(f[2])}</span><h3>{esc(txt(f[0],m,cc,k))}</h3><p style="margin:0;color:var(--mu)">{esc(txt(f[1],m,cc,k)[:120])}…</p></a>' for f in e["fallas"])
                fq = [(txt(q, m, cc, k), txt(a, m, cc, k)) for q, a in e["faq"]] + faq_gen(m, cc, None, k)[:5]
                mod = "".join(f"<li>{esc(x)}</li>" for x in e["modelos"])
                extra = [("Mantenimiento", f"/{m}/{cc}/{k}/mantenimiento/"), ("¿Cuánto cuesta reparar?", f"/{m}/{cc}/{k}/cuanto-cuesta-reparar/")] + ([("Códigos de error", f"/{m}/{cc}/{k}/codigos-de-error/")] if (k == "lavadoras" and m in CODIGOS) else [])
                body = sec(f"Fallas comunes en {eqn}", f'<div class="g">{fl}</div>') + sec(f"Modelos de {eqn} que atendemos", f"<ul>{mod}</ul>") \
                    + sec("Guías", pills(extra)) + sec("Preguntas frecuentes", faqh(fq)) + sec("Búsquedas relacionadas", kw_html(m, cc, k=k)) \
                    + sec("Por ciudad", pills([(f"{c}", f"/{m}/{cc}/{slug(c)}/{k}/") for c in p["ciudades"]]))
                page(f"{m}/{cc}/{k}/", f"{t}: reparación a domicilio | {NOM}", f"{t}{' (' + a2 + ')' if a2 else ''}. Reparación a domicilio, diagnóstico y garantía. Solicita al técnico {mn} más cercano a tu barrio por WhatsApp.", t,
                     txt(e["intro"], m, cc, k)[:170], body, bc=bc_p, m=m, cc=cc, rel=f"{k}/", eq=k,
                     jsonld=[svc_ld(m, cc, None, k), faq_ld(fq), bc_ld([("Inicio", DOM + "/"), (mn, f"{DOM}/{m}/"), (pn, f"{DOM}/{m}/{cc}/"), (cap(term(cc, k)), f"{DOM}/{m}/{cc}/{k}/")])])
                bc_k = bc_p + [(cap(term(cc, k)), f"/{m}/{cc}/{k}/")]
                for f in e["fallas"]:
                    ft = txt(f[0], m, cc, k); fs = slug(f[0]); otras = pills([(txt(x[0], m, cc, k), f"/{m}/{cc}/{k}/{slug(x[0])}/") for x in e["fallas"] if x[0] != f[0]][:8])
                    fq = [(f"¿Por qué {ft[0].lower() + ft[1:]}?" if False else f"¿Por qué pasa: «{ft}»?", txt(f[1], m, cc, k)),
                          (f"¿Es peligroso seguir usando mi {sing(cc,k)} {mn} así?", f"Nivel de urgencia: {f[2].lower()}. " + txt(f[3], m, cc, k)),
                          (f"¿Cuánto cuesta arreglar esta falla en {pn}?", f"Depende de la pieza y la mano de obra. El técnico {mn} confirma el costo en {p['moneda']} antes de reparar."),
                          (f"¿Puedo arreglarlo yo mismo?", "Puedes revisar lo básico (energía, llaves de agua, limpieza). Para piezas internas conviene un técnico, para evitar daños mayores.")]
                    body = sec("¿Por qué pasa?", f"<p>{esc(txt(f[1],m,cc,k))}</p>") + sec("Qué hacer mientras llega el técnico", f"<p>{esc(txt(f[3],m,cc,k))}</p><p><span class='urg'>Urgencia: {esc(f[2])}</span></p>") \
                        + sec("Preguntas frecuentes", faqh(fq)) + sec("Otras fallas frecuentes", otras) + sec("Búsquedas relacionadas", kw_html(m, cc, k=k, falla=f[0])) \
                        + sec("Servicio por ciudad", pills([(c, f"/{m}/{cc}/{slug(c)}/{k}/") for c in p["ciudades"]]))
                    page(f"{m}/{cc}/{k}/{fs}/", f"{ft} – {mn} {pn}: causas, qué hacer y técnico | {NOM}", f"{ft} en tu {sing(cc,k)} {mn} ({pn}): causas, qué hacer y cuándo llamar al técnico. Solicita servicio a domicilio por WhatsApp.",
                         f"{ft}: {mn} en {pn}", f"Causas, qué hacer y técnico {mn} a domicilio.", body, bc=bc_k, m=m, cc=cc, rel=f"{k}/{fs}/", eq=k, falla=txt(f[0], m, cc, k),
                         jsonld=[faq_ld(fq), bc_ld([("Inicio", DOM + "/"), (mn, f"{DOM}/{m}/"), (pn, f"{DOM}/{m}/{cc}/"), (cap(term(cc, k)), f"{DOM}/{m}/{cc}/{k}/"), (ft, f"{DOM}/{m}/{cc}/{k}/{fs}/")])])
                # mantenimiento
                mant = "".join(f"<li>{esc(txt(x,m,cc,k))}</li>" for x in e["mant"])
                page(f"{m}/{cc}/{k}/mantenimiento/", f"Mantenimiento de {eqn} en {pn}: guía y servicio | {NOM}", f"Cómo cuidar tu {sing(cc,k)} {mn} y cuándo pedir mantenimiento a domicilio en {pn}.",
                     f"Mantenimiento de {eqn} en {pn}", "Hábitos simples que alargan la vida del equipo.", sec("Consejos de mantenimiento", f"<ul>{mant}</ul>") + sec("Búsquedas relacionadas", kw_html(m, cc, k=k)),
                     bc=bc_k, m=m, cc=cc, rel=f"{k}/mantenimiento/", eq=k, jsonld=[bc_ld([("Inicio", DOM + "/"), (mn, f"{DOM}/{m}/"), (pn, f"{DOM}/{m}/{cc}/"), ("Mantenimiento", f"{DOM}/{m}/{cc}/{k}/mantenimiento/")])])
                # costo
                fq = faq_gen(m, cc, None, k)[2:5]
                body = sec("Qué define el costo", "<ul><li>La falla: una pieza pequeña no cuesta como una tarjeta o un compresor.</li><li>La pieza: disponibilidad y tipo de repuesto.</li><li>La mano de obra y el tiempo de la visita.</li><li>La zona: distancia entre el técnico y tu barrio.</li></ul>") \
                    + sec("Cómo trabajamos el presupuesto", f"<p>El técnico {esc(mn)} revisa tu equipo, te explica la falla y te da el costo en {esc(p['moneda'])} antes de empezar. No se repara nada sin tu aprobación.</p>") + sec("Preguntas frecuentes", faqh(fq))
                page(f"{m}/{cc}/{k}/cuanto-cuesta-reparar/", f"¿Cuánto cuesta reparar {sing(cc,k)} {mn} en {pn}? | {NOM}", f"Qué define el precio de reparar {eqn} en {pn} y cómo pedir una cotización por WhatsApp.",
                     f"¿Cuánto cuesta reparar {sing(cc,k)} {mn} en {pn}?", "Lo que influye en el precio y cómo cotizar sin compromiso.", body, bc=bc_k, m=m, cc=cc, rel=f"{k}/cuanto-cuesta-reparar/", eq=k,
                     jsonld=[faq_ld(fq), bc_ld([("Inicio", DOM + "/"), (mn, f"{DOM}/{m}/"), (pn, f"{DOM}/{m}/{cc}/"), ("Costo", f"{DOM}/{m}/{cc}/{k}/cuanto-cuesta-reparar/")])])
                if k == "lavadoras" and m in CODIGOS:
                    rows = "".join(f"<tr><td><b>{esc(c)}</b></td><td>{esc(s)}</td><td>{esc(q)}</td></tr>" for c, s, q in CODIGOS[m])
                    body = sec(f"Códigos de error de lavadoras {mn}", f'<div style="overflow-x:auto"><table style="border-collapse:collapse;width:100%"><thead><tr><th align=left>Código</th><th align=left>Significado</th><th align=left>Causas frecuentes</th></tr></thead><tbody>{rows}</tbody></table></div><p style="color:var(--mu)">Los códigos pueden variar según el modelo; consulta el manual.</p>') + sec("Búsquedas relacionadas", kw_html(m, cc, k=k))
                    page(f"{m}/{cc}/{k}/codigos-de-error/", f"Códigos de error de lavadoras {mn} en {pn}: significado y solución | {NOM}", f"Significado de los códigos de error de las lavadoras {mn} y cuándo pedir un técnico en {pn}.",
                         f"Códigos de error de lavadoras {mn}", "Qué significa cada código y qué hacer.", body, bc=bc_k, m=m, cc=cc, rel=f"{k}/codigos-de-error/", eq=k,
                         jsonld=[bc_ld([("Inicio", DOM + "/"), (mn, f"{DOM}/{m}/"), (pn, f"{DOM}/{m}/{cc}/"), ("Códigos de error", f"{DOM}/{m}/{cc}/{k}/codigos-de-error/")])])
    # ---- estáticos
    (OUT / "datos.js").write_text("window.DATOS=" + json.dumps({c: {"n": p["nombre"], "wa": p["wa"], "dial": p["dial"], "ciudades": p["ciudades"], "voc": {k: term(c, k) for k in EQ}} for c, p in PA.items()}, ensure_ascii=False) + ";", encoding="utf-8")
    (OUT / "app.js").write_text("""if('serviceWorker' in navigator){addEventListener('load',function(){navigator.serviceWorker.register('/sw.js').catch(function(){});});}
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('[data-evt="whatsapp"]');if(a){window.dataLayer=window.dataLayer||[];window.dataLayer.push({event:'whatsapp',marca:document.body.dataset.marca||'',pais:document.body.dataset.pais||''});}});""", encoding="utf-8")
    (OUT / "sw.js").write_text("""var V='st-v3';
self.addEventListener('install',function(e){self.skipWaiting();});
self.addEventListener('activate',function(e){e.waitUntil(caches.keys().then(function(k){return Promise.all(k.filter(function(x){return x!==V;}).map(function(x){return caches.delete(x);}));}));self.clients.claim();});
self.addEventListener('fetch',function(e){if(e.request.method!=='GET'||new URL(e.request.url).origin!==location.origin)return;e.respondWith(fetch(e.request).then(function(r){var c=r.clone();caches.open(V).then(function(ch){ch.put(e.request,c);});return r;}).catch(function(){return caches.match(e.request).then(function(r){return r||caches.match('/');});}));});""", encoding="utf-8")
    (OUT / "manifest.webmanifest").write_text(json.dumps({"name": NOM, "short_name": "Soporte Técnico", "start_url": "/", "display": "standalone", "background_color": "#f3f4f6", "theme_color": "#0f766e", "lang": "es",
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
