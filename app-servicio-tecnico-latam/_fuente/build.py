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


POOL = {
 "samsung": dict(tecnico=[F("samsung", n) for n in ("sam-3", "sam-4", "sam-7", "sam-2", "sam-5", "sam-1", "sam-6")], neveras=[F("samsung", "prod-nevera-sbs"), F("samsung", "prod-nevera-top")], lavadoras=[F("samsung", "prod-lavadora-sup"), F("samsung", "prod-torre")], secadoras=[F("samsung", "prod-secadora"), F("samsung", "prod-torre")]),
 "lg": dict(tecnico=[F("lg", n) for n in ("tecnico-nevera", "tecnico-lavadora-1", "tecnico-lavadora-2", "tecnico-banner", "atencion-1", "atencion-2", "atencion-3")], neveras=[F("lg", "prod-nevera-top")], lavadoras=[F("lg", "prod-lavadora-fr"), F("lg", "prod-lavadora-sup"), F("lg", "prod-torre")], secadoras=[F("lg", "prod-secadora"), F("lg", "prod-torre")]),
 "whirlpool": dict(tecnico=[F("whirlpool", n) for n in ("sam-1", "sam-2", "sam-3")], neveras=[F("whirlpool", "prod-nevera-sbs"), F("whirlpool", "prod-nevera-top")], lavadoras=[F("whirlpool", "prod-lavadora-sup"), F("whirlpool", "prod-torre")], secadoras=[F("whirlpool", "prod-secadora"), F("whirlpool", "prod-torre")]),
 "frigidaire": dict(tecnico=[F("frigidaire", n) for n in ("sam-3", "sam-4", "sam-6", "sam-7", "sam-8", "sam-1", "sam-2", "sam-5")], neveras=[F("frigidaire", "prod-nevera-sbs")], lavadoras=[F("frigidaire", "prod-lavadora-fr"), F("frigidaire", "prod-lavadora-sup")], secadoras=[F("frigidaire", "prod-torre")]),
 "electrolux": dict(tecnico=[F("electrolux", n) for n in ("sam-3", "sam-4", "sam-6", "sam-1", "sam-2", "sam-5")], neveras=[F("electrolux", "prod-nevera-sbs"), F("electrolux", "prod-nevera-top")], lavadoras=[F("electrolux", "prod-lavadora-fr"), F("electrolux", "prod-lavadora-sup")], secadoras=[F("electrolux", "prod-torre")]),
 "general-electric": dict(tecnico=[F("general-electric", n) for n in ("sam-2", "sam-3", "sam-4", "sam-5", "sam-1")], neveras=[F("general-electric", "prod-nevera-sbs"), F("general-electric", "prod-nevera-top")], lavadoras=[F("general-electric", "prod-lavadora-fr"), F("general-electric", "prod-lavadora-sup")], secadoras=[F("general-electric", "prod-secadora")]),
 "mabe": dict(tecnico=[MB / "nosotros" / n for n in ("tecnico-saludo-cliente-panama.jpg", "tecnico-trabajando-servicio-mabe.jpg", "tecnico-confianza-mabe-cocina.jpg", "torre-garantia-mabe.jpg")],
              neveras=[MB / "neveras" / n for n in ("producto-neveras-panama.jpg", "sideby-side-neveras-panama.jpg", "topfreezer-inox-neveras-panama.jpg", "hero-neveras-panama.jpg")],
              lavadoras=[MB / "lavadoras" / n for n in ("hero-lavadoras-panama.jpg", "equipo-lavadoras-panama.jpg")] + [MB / "centros-de-lavado" / "hero-centros-de-lavado-panama.jpg"],
              secadoras=[MB / "secadoras" / n for n in ("hero-secadoras-panama.jpg", "equipo-secadoras-panama.jpg")]),
}
CCS = ["co", "pa", "gt", "sv", "cr", "ec", "py", "cl"]
def imgk(m, cc, k, off=0):
    """foto del equipo/técnico distinta según país (k = neveras|lavadoras|secadoras|tecnico)"""
    n = len(POOL[m][k]); return f"/img/{m}/{k}-{(CCS.index(cc) + off) % n}.jpg"
def copiar_pool():
    for m, d in POOL.items():
        for k, lst in d.items():
            for i, src in enumerate(lst):
                if not src.exists(): print("⚠ falta", src); continue
                im = Image.open(src).convert("RGB"); im.thumbnail((900, 900)); im.save(OUT / "img" / m / f"{k}-{i}.jpg", quality=80, optimize=True)

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


PS = {"co": "colombia", "pa": "panama", "gt": "guatemala", "sv": "el-salvador", "cr": "costa-rica", "ec": "ecuador", "py": "paraguay", "cl": "chile"}
def slugloc(ci, cc):
    t = slug(ci); return t if PS[cc] in t else f"{t}-{PS[cc]}"
def Um(m): return f"/soporte-tecnico-autorizado-{m}/"
def _u(m, *partes): return "/soporte-tecnico-autorizado-" + "-".join([m] + [p for p in partes if p]) + "/"
def Uc(m, cc): return _u(m, PS[cc])
def Ue(m, cc, k): return _u(m, slug(term(cc, k)), PS[cc])
def Uci(m, cc, ci): return _u(m, slugloc(ci, cc))
def Ucek(m, cc, ci, k): return _u(m, slug(term(cc, k)), slugloc(ci, cc))
def Uz(m, cc, n):
    ci = next((c for z, t, c in zonas_de(cc) if z == n), list(PA[cc]["ciudades"])[0])
    return _u(m, slug(n), slugloc(ci, cc))
def Uf(m, cc, k, f0): return _u(m, slug(txt(f0, m, cc, k)), PS[cc])
def Ufaq(m, cc): return _u(m, "preguntas-frecuentes", PS[cc])
def Ucerca(m, cc): return _u(m, "cerca-de-mi", PS[cc])
def Umant(m, cc, k): return _u(m, "mantenimiento", slug(term(cc, k)), PS[cc])
def Ucosto(m, cc, k): return _u(m, "cuanto-cuesta-reparar", slug(term(cc, k)), PS[cc])
def Ucod(m, cc, k): return _u(m, "codigos-de-error", slug(term(cc, k)), PS[cc])

PAGES = []
def hreflangs(m, rel):
    return "".join(f'<link rel="alternate" hreflang="{PA[c]["locale"]}" href="{DOM}{rel(c)}">' for c in PA) + f'<link rel="alternate" hreflang="x-default" href="{DOM}{Um(m)}">'

def wa(num, texto=""): return f"https://wa.me/{num}" + (f"?text={quote(texto)}" if texto else "")

def orden_json(m, cc):
    mn = MA[m]["nombre"]; eq = {}
    for k, e in EQ.items():
        eq[k] = dict(t=term(cc, k) if cc else e["corto"].lower(), img=(imgk(m, cc, k) if cc else f"/img/{m}/{k}.jpg"), alt=ALT(m, k, PA[cc]["nombre"] if cc else None),
                     fallas=[[txt(f[0], m, cc, k), txt(f[0], m, cc, k), f[2]] for f in e["fallas"]])
    return json.dumps({"equipos": eq}, ensure_ascii=False, separators=(",", ":"))


TITULOS = set()
def acortar(t, must=(), n=68):
    """Títulos cortos cuando se puede, pero siempre únicos y con marca + lugar."""
    cands = [t]; u = t
    for sep in (": ", " – ", "? "):
        if sep in u:
            u = u.rsplit(sep, 1)[0] + ("?" if sep == "? " else ""); cands.append(u)
    out = t
    for c in reversed(cands):          # del más corto al más largo
        if len(c) <= n and all(x in c for x in must) and c not in TITULOS: out = c; break
    TITULOS.add(out); return out

def page(ruta, title, desc, h1, sub, body, bc=None, m=None, cc=None, rel=None, jsonld=None, eq=None, falla=None, orden=True, fab=True, ci=None):
    title = acortar(title, ([MA[m]['nombre']] + ([ci] if ci else ([PA[cc]['nombre']] if cc else []))) if m else ())
    url = f"{DOM}/{ruta}"; PAGES.append(url)
    mc = MA[m]["color"] if m else "#0f766e"; mt = MA[m].get("texto", "#fff") if m else "#fff"
    V = MA[m] if m else {}
    pal = f"--mc:{mc};--mt:{mt};--mc2:{V.get('pri2', '#0b3d38')};--acc:{V.get('acc', '#25d366')};--soft:{V.get('soft', '#e6f4f1')};--panel:{V.get('panel', '#f3f4f6')};--ink:{V.get('ink', '#0f172a')}"
    bch = '<nav class="bc" aria-label="Migas de pan">' + " › ".join(f'<a href="{u}">{esc(t)}</a>' for t, u in bc) + "</nav>" if bc else ""
    ld = "".join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in (jsonld or []))
    hl = hreflangs(m, rel) if (m and cc and rel is not None) else ""
    gtm = f"<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s);j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i;f.parentNode.insertBefore(j,f)}})(window,document,'script','dataLayer','{CFG['gtm']}');</script>" if CFG["gtm"] else ""
    ver = f'<meta name="google-site-verification" content="{CFG["verificacion_gsc"]}">' if CFG["verificacion_gsc"] else ""
    man = Um(m) + "manifest.webmanifest" if m else "/manifest.webmanifest"
    ico = f"/img/{m}/logo.png" if m else "/icons/icon-192.png"
    img = f"{DOM}/img/{m}/tecnico.jpg" if m else f"{DOM}/icons/icon-512.png"
    logo = f'<a class="lg" href="{Um(m)}"><img src="/img/{m}/logo.png" alt="{esc(ALT(m,"logo"))}" height="30"></a>' if m else f'<span style="font-weight:800">{esc(NOM)}</span>'
    locale = PA[cc]["locale"] if cc else "es"
    wnum = PA[cc]["wa"] if cc else ""
    fb = f'<a class="btn wa fab" data-evt="whatsapp" id="fab" href="{wa(wnum, "Hola, necesito servicio técnico " + MA[m]["nombre"] + " en " + PA[cc]["nombre"])}" rel="noopener">WhatsApp</a>' if (fab and cc and m) else ""
    if m and cc: body = body + extras(m, cc, ci, eq, ruta)
    body, toc = anclar(body)
    ordh = ""
    if orden and m:
        ordh = f'<section class="ord" id="orden" aria-label="Solicitud de servicio técnico {esc(MA[m]["nombre"])}"><h2>Pide tu servicio técnico {esc(MA[m]["nombre"])}</h2><p class="ay">Cuéntanos tu equipo y la falla; te conectamos por WhatsApp.</p>' + (f'<a class="btn wa" data-evt="whatsapp" href="{wa(wnum, "Hola, necesito servicio técnico " + MA[m]["nombre"])}">Escribir por WhatsApp</a>' if cc else "") + '</section>'
        ordh += f'<script>window.ORDEN={orden_json(m, cc)};</script>'
    ordh += toc
    h = f"""<!doctype html><html lang="{locale}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{url}">{hl}{ver}
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1"><meta name="geo.region" content="{cc.upper() if cc else ''}">
<link rel="manifest" href="{man}"><meta name="theme-color" content="{mc}"><link rel="icon" href="{ico}"><link rel="apple-touch-icon" href="{ico}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="{url}"><meta property="og:image" content="{img}"><meta property="og:locale" content="{locale.replace('-','_')}">
<link rel="stylesheet" href="/estilo.css">{ld}{gtm}</head><body data-marca="{m or ''}" data-nombre="{esc(MA[m]['nombre']) if m else ''}" data-pais="{cc or ''}" data-bu="{Um(m) if m else ''}" data-equipo="{eq or ''}" data-falla="{esc(falla or '')}" style="{pal}">
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
    return {"@context": "https://schema.org", "@type": "HomeAndConstructionBusiness", "name": nom, "url": DOM + Uc(m, cc), "image": f"{DOM}/img/{m}/tecnico.jpg", "telephone": p["tel"] or None, "priceRange": "$$",
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
    out = [x.format(m=mn, c=(ci or list(PA[cc]['ciudades'])[0])) for x in INFO[cc]['busq']] + out
    return list(dict.fromkeys(out))
def kw_html(*a, **kw): return "<ul class='kw'>" + "".join(f"<li>{esc(x)}</li>" for x in kw_list(*a, **kw)) + "</ul>"
def pills(items): return "".join(f'<a class="pill" href="{u}">{esc(t)}</a>' for t, u in items)


from paises_info import INFO, CIUDAD
import zlib
OFICIAL = {"samsung": "https://www.samsung.com/", "lg": "https://www.lg.com/", "whirlpool": "https://www.whirlpool.com/", "mabe": "https://www.mabe.com.mx/",
           "frigidaire": "https://www.frigidaire.com/", "electrolux": "https://www.electrolux.com/", "general-electric": "https://www.geappliances.com/"}
WIKI_PAIS = {"co": "Colombia", "pa": "Panamá", "gt": "Guatemala", "sv": "El_Salvador", "cr": "Costa_Rica", "ec": "Ecuador", "py": "Paraguay", "cl": "Chile"}

def anclar(body):
    """Pone id a cada sección y arma el índice «En esta página»."""
    ids = []
    def sub(mm):
        t = re.sub(r"<[^>]+>", "", mm.group(1)); i = slug(t)[:50] or "seccion"
        ids.append((t, i)); return f'<section class="sec" id="{i}"><h2>{mm.group(1)}</h2>'
    body = re.sub(r'<section class="sec"><h2>(.*?)</h2>', sub, body)
    toc = ""
    if len(ids) >= 3:
        toc = '<nav class="sec" aria-label="En esta página"><h3 style="margin:.8em 0 .5em">En esta página</h3>' + "".join(f'<a class="pill" href="#{i}">{esc(t)}</a>' for t, i in ids) + "</nav>"
    return body, toc

def faq_pais(m, cc):
    mn = MA[m]["nombre"]; p = PA[cc]; pn = p["nombre"]; I = INFO[cc]
    return [
     (f"¿Mi equipo {mn} funciona con el voltaje de {pn}?", f"En {pn} la red eléctrica es de {I['volt']}. Los equipos {mn} vendidos en el país vienen preparados para ese voltaje; si tu equipo llegó de otro país, el técnico revisa la compatibilidad antes de conectarlo."),
     (f"¿Qué hago con los bajones de luz y las tormentas en {pn}?", f"{I['rayos']} Desconecta el equipo durante tormentas fuertes y usa un protector de voltaje para neveras, lavadoras y secadoras {mn}."),
     (f"¿El clima de {pn} afecta mi {mn}?", f"{I['clima']} Con ese ambiente conviene limpiar rejillas y filtros con más frecuencia y revisar las gomas de las puertas."),
     (f"¿El agua de {pn} daña mi lavadora {mn}?", f"{I['agua']} Un mantenimiento periódico alarga la vida de válvulas, resistencias y mangueras."),
     (f"¿Cómo se llama en {pn} la nevera, la lavadora y la secadora?", f"En {pn} la nevera suele llamarse «{term(cc,'neveras')}» (también «{alt(cc,'neveras') or term(cc,'neveras')}»), la lavadora «{term(cc,'lavadoras')}» y la secadora «{term(cc,'secadoras')}». Atendemos todas, sin importar cómo las llames."),
     (f"¿En qué ciudades de {pn} tienen técnico {mn}?", "Tenemos cobertura en " + ", ".join(p["ciudades"]) + " y sus alrededores."),
     (f"¿En qué barrios de {pn} atienden equipos {mn}?", "Atendemos, entre otros, " + ", ".join(n for n, t, c in zonas_de(cc)[:8]) + ".")]

def extras(m, cc, ci, k, ruta):
    mn = MA[m]["nombre"]; p = PA[cc]; pn = p["nombre"]; I = INFO[cc]; lugar = ci or pn
    off = zlib.crc32(ruta.encode()) % 7
    out = []
    # 1 · lo local
    loc = f"<p>{esc(I['clima'])}</p>"
    if ci and ci in CIUDAD: loc += f"<p><b>{esc(ci)}:</b> {esc(CIUDAD[ci])}</p>"
    loc += f"<p>{esc(I['rayos'])} {esc(I['agua'])}</p><p>La red eléctrica de {esc(pn)} es de {esc(I['volt'])}.</p>"
    if k: loc += f"<p><b>Consejo para {esc(term(cc,k))} {esc(mn)} en {esc(pn)}:</b> {esc(I['tip'][k])}</p>"
    loc += f'<img class="ph" loading="lazy" src="{imgk(m, cc, "tecnico", off)}" alt="{esc(ALT(m, "tecnico", lugar))}" width="900" height="560">'
    out.append(sec(f"Lo que debes saber en {lugar} sobre tu {mn}", loc))
    # 2 · la visita
    pasos = [("Recibimos tu solicitud", f"Llega por WhatsApp con la marca ({mn}), el equipo, la falla y tu ubicación en {lugar}."),
             ("Te contactamos", f"El técnico {mn} más cercano a tu barrio te escribe para confirmar horario y datos del equipo."),
             ("Diagnóstico en tu casa", "Revisa el equipo en el sitio y te explica la falla con palabras simples, sin tecnicismos."),
             ("Presupuesto claro", f"Te da el costo en {p['moneda']} antes de empezar. No se repara nada sin tu aprobación."),
             ("Reparación y garantía", "Repara, prueba el equipo contigo y te explica la garantía de la pieza y la mano de obra.")]
    out.append(sec(f"Cómo es la visita del técnico {mn} en {lugar}", "<ol>" + "".join(f"<li><b>{esc(a)}.</b> {esc(b)}</li>" for a, b in pasos) + "</ol>"))
    # 3 · señales (enlaces a fallas)
    ks = [k] if k else list(EQ)
    sen = ""
    for x in ks:
        sen += f"<h3>{esc(cap(term(cc, x)))} {esc(mn)}</h3>" + pills([(txt(f[0], m, cc, x), Uf(m, cc, x, f[0])) for f in EQ[x]["fallas"][:6]])
    out.append(sec(f"Señales de que tu equipo {mn} necesita un técnico", sen))
    # 4 · explora (enlaces internos)
    ex = [(f"Soporte técnico autorizado {mn}", Um(m)), (f"{mn} en {pn}", Uc(m, cc)), ("Preguntas frecuentes", Ufaq(m, cc)), ("Técnico cerca de mí", Ucerca(m, cc))]
    ex += [(f"{cap(term(cc, x))} {mn} en {pn}", Ue(m, cc, x)) for x in EQ]
    ex += [(f"¿Cuánto cuesta reparar {sing(cc, x)} {mn}?", Ucosto(m, cc, x)) for x in EQ] + [(f"Mantenimiento de {term(cc, x)} {mn}", Umant(m, cc, x)) for x in EQ]
    ex += [(c, Uci(m, cc, c)) for c in p["ciudades"]] + [(n, Uz(m, cc, n)) for n, t, c in zonas_de(cc)[:8]]
    out.append(sec(f"Explora más sobre {mn} en {pn}", pills(ex)))
    # 5 · enlaces externos
    q = quote(f"servicio técnico {mn} {lugar}")
    ext = [f'<li><a href="https://www.google.com/maps/search/{q}" target="_blank" rel="noopener">Ver servicios técnicos {esc(mn)} en {esc(lugar)} en Google Maps</a></li>',
           f'<li><a href="{OFICIAL[m]}" target="_blank" rel="noopener">Sitio oficial de {esc(mn)}</a> (manuales, garantía y registro de producto)</li>',
           f'<li><a href="https://es.wikipedia.org/w/index.php?search={quote(mn)}" target="_blank" rel="noopener">{esc(mn)} en Wikipedia</a></li>',
           f'<li><a href="https://es.wikipedia.org/wiki/{WIKI_PAIS[cc]}" target="_blank" rel="noopener">Acerca de {esc(pn)} en Wikipedia</a></li>']
    out.append(sec("Enlaces útiles", "<ul>" + "".join(ext) + "</ul><p style='color:var(--mu);font-size:.85rem'>Los enlaces externos llevan a sitios de terceros.</p>"))
    return "".join(out)

def build():
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    copiar_imagenes(); copiar_pool()
    faltan = [c for c in PA if not PA[c]["wa"]]
    shutil.copy(RAIZ / "_fuente" / "estilo.css", OUT / "estilo.css"); shutil.copy(RAIZ / "_fuente" / "orden.js", OUT / "orden.js")
    # ---- raíz
    mc = "".join(f'<a href="{Um(m)}" style="--mc:{v["color"]}"><div class="bar"></div><img class="t" loading="lazy" src="/img/{m}/tecnico.jpg" alt="{esc(ALT(m,"tecnico"))}" width="400" height="300"><div class="in"><span class="lg"><img src="/img/{m}/logo.png" alt="{esc(ALT(m,"logo"))}" height="30"></span><h3>Servicio técnico {esc(v["nombre"])}</h3><span style="color:var(--mu);font-size:.9rem">Neveras, lavadoras y secadoras</span></div></a>' for m, v in MA.items())
    body = f'<section class="ord" id="marcas"><h2>Elige tu marca</h2><p class="ay">Cada marca tiene su propia solicitud de servicio.</p><div class="mk">{mc}</div></section>' + sec("Países donde trabajamos", "<p>" + ", ".join(esc(p["nombre"]) for p in PA.values()) + ".</p>")
    page("", "Soporte técnico autorizado por marca: neveras, lavadoras y secadoras en Latinoamérica",
         "Pide tu técnico Samsung, LG, Whirlpool, Mabe, Frigidaire, Electrolux o GE. Detectamos tu barrio, eliges el equipo y la falla, y enviamos la solicitud por WhatsApp. Colombia, Panamá, Guatemala, El Salvador, Costa Rica, Ecuador, Paraguay y Chile.",
         "Soporte técnico autorizado por marca, en tu barrio", "Elige tu marca, cuéntanos la falla y te conectamos por WhatsApp con el técnico más cercano.", body, orden=False,
         jsonld=[{"@context": "https://schema.org", "@type": "WebSite", "name": NOM, "url": DOM + "/"}], fab=False)
    for m, v in MA.items():
        mn = v["nombre"]; tt = TEC.get(m, []); globals()["EQ"] = EQB[m]
        (OUT / Um(m)[1:]).mkdir(parents=True, exist_ok=True)
        (OUT / Um(m)[1:] / "tecnicos.json").write_text(json.dumps(tt, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        (OUT / Um(m)[1:] / "manifest.webmanifest").write_text(json.dumps({"name": f"Servicio técnico {mn}", "short_name": mn, "start_url": Um(m), "scope": Um(m), "display": "standalone", "background_color": "#ffffff", "theme_color": v["color"], "lang": "es",
            "icons": [{"src": f"/img/{m}/logo.png", "sizes": "512x512", "type": "image/png", "purpose": "any"}]}, ensure_ascii=False), encoding="utf-8")
        # ---- home de marca
        fq = faq_gen(m, "pa")[:0]
        eqc = "".join(f'<div class="cd"><img src="/img/{m}/{k}.jpg" alt="{esc(ALT(m,k))}" loading="lazy" style="width:100%;aspect-ratio:16/10;object-fit:contain;background:#fff;border-radius:10px"><h3>{esc(e["corto"])} {esc(mn)}</h3><p style="color:var(--mu);margin:0">{esc(txt(e["intro"],m,None)[:140])}…</p></div>' for k, e in EQ.items())
        fqb = [(f"¿Qué equipos {mn} reparan?", f"Neveras (refrigeradoras, heladeras), lavadoras (lavarropas) y secadoras {mn}."),
               (f"¿En qué países hay servicio técnico {mn}?", "En " + ", ".join(p["nombre"] for p in PA.values()) + "."),
               (f"¿Cómo funciona la solicitud de servicio {mn}?", "Activas tu ubicación, eliges el equipo y la falla, y enviamos tu solicitud por WhatsApp al técnico más cercano."),
               (f"¿Cuánto cuesta el servicio técnico {mn}?", "Depende de la falla y la pieza. Te cotizamos antes de reparar, sin compromiso.")]
        body = sec("Elige tu país", pills([(p["nombre"], Uc(m, c)) for c, p in PA.items()])) + sec(f"Equipos {mn} que reparamos", f'<div class="g">{eqc}</div>') \
            + sec("Preguntas frecuentes", faqh(fqb)) + sec(f"Búsquedas relacionadas con servicio técnico {mn}", "<ul class='kw'>" + "".join(f"<li>servicio técnico {esc(mn)} {esc(p['nombre'])}</li>" for p in PA.values()) + "</ul>")
        page(Um(m)[1:], f"Soporte técnico autorizado {mn}: técnico más cercano por WhatsApp",
             f"Servicio técnico {mn} a domicilio en 8 países. Activa tu ubicación, elige tu equipo y la falla, y envía tu solicitud por WhatsApp al técnico {mn} más cercano a tu barrio.",
             f"Soporte técnico autorizado {mn}", f"Pide tu técnico {mn} más cercano. Reparación a domicilio de neveras, lavadoras y secadoras.", body, bc=[("Inicio", "/")], m=m, rel=None,
             jsonld=[faq_ld(fqb), bc_ld([("Inicio", DOM + "/"), (mn, DOM + Um(m))])], fab=False)
        for cc, p in PA.items():
            pn = p["nombre"]; zs = zonas_de(cc)
            base_bc = [("Inicio", "/"), (mn, Um(m))]
            # ---- país
            fq = faq_pais(m, cc) + faq_gen(m, cc)
            eqcards = "".join(f'<a class="cd" href="{Ue(m,cc,k)}"><img src="{imgk(m,cc,k)}" alt="{esc(ALT(m,k,pn))}" loading="lazy"><h3>{esc(cap(term(cc,k)))} {esc(mn)} en {esc(pn)}</h3></a>' for k in EQ)
            body = sec(f"Equipos {mn} que reparamos en {pn}", f'<div class="g">{eqcards}</div>') \
                + sec(f"Ciudades con técnico {mn} en {pn}", pills([(c, Uci(m, cc, c)) for c in p["ciudades"]])) \
                + sec(f"Barrios y zonas donde atendemos {mn}", pills([(n, Uz(m, cc, n)) for n, t, c in zs])) \
                + sec("Más ayuda", pills([("Preguntas frecuentes", Ufaq(m, cc)), ("Técnico cerca de mí", Ucerca(m, cc))])) \
                + sec(f"Preguntas frecuentes sobre servicio técnico {mn} en {pn}", faqh(fq)) + sec("Búsquedas relacionadas", kw_html(m, cc))
            page(Uc(m, cc)[1:], f"Soporte técnico autorizado {mn} {pn}: {term(cc,'neveras')}, {term(cc,'lavadoras')} y {term(cc,'secadoras')}",
                 f"Servicio técnico {mn} en {pn}: reparación a domicilio de {term(cc,'neveras')}, {term(cc,'lavadoras')} y {term(cc,'secadoras')} {mn}. Pide el técnico más cercano a tu barrio por WhatsApp.",
                 f"Soporte técnico autorizado {mn} en {pn}", f"Reparación a domicilio de {term(cc,'neveras')}, {term(cc,'lavadoras')} y {term(cc,'secadoras')} {mn} en {', '.join(list(p['ciudades'])[:3])} y más.", body,
                 bc=base_bc, m=m, cc=cc, rel=(lambda c2: Uc(m, c2)), jsonld=[svc_ld(m, cc), how_ld(m, cc), faq_ld(fq), bc_ld([("Inicio", DOM + "/"), (mn, DOM + Um(m)), (pn, DOM + Uc(m, cc))])])
            bc_p = base_bc + [(pn, Uc(m, cc))]
            # ---- preguntas frecuentes (hub) y cerca de mí
            big = faq_pais(m, cc) + faq_gen(m, cc)
            for k, e in EQ.items(): big += [(txt(q, m, cc, k), txt(a, m, cc, k)) for q, a in e["faq"]]
            big = list(dict.fromkeys(big))
            page(Ufaq(m, cc)[1:], f"Soporte técnico autorizado {mn} {pn}: preguntas frecuentes", f"Respuestas sobre precios, tiempos, garantía y cobertura del servicio técnico {mn} en {pn}: neveras, lavadoras y secadoras.",
                 f"Preguntas frecuentes del soporte técnico autorizado {mn} en {pn}", "Costos, tiempos, garantía y cobertura, explicados claro.", sec("Todas las preguntas", faqh(big)) + sec("Búsquedas relacionadas", kw_html(m, cc)),
                 bc=bc_p, m=m, cc=cc, rel=(lambda c2: Ufaq(m, c2)), jsonld=[faq_ld(big), bc_ld([("Inicio", DOM + "/"), (mn, DOM + Um(m)), (pn, DOM + Uc(m, cc)), ("Preguntas frecuentes", DOM + Ufaq(m, cc))])], orden=False)
            page(Ucerca(m, cc)[1:], f"Soporte técnico autorizado {mn} cerca de mí en {pn}", f"Encuentra el técnico {mn} más cercano a ti en {pn}: activa tu ubicación y envía tu solicitud por WhatsApp.",
                 f"Soporte técnico autorizado {mn} cerca de mí en {pn}", "Activa tu ubicación y te mostramos el técnico más cercano a tu barrio.", sec("Ciudades y barrios cercanos", pills([(c, Uci(m, cc, c)) for c in p["ciudades"]]) + pills([(n, Uz(m, cc, n)) for n, t, c in zs[:8]])) + sec("Búsquedas relacionadas", kw_html(m, cc)),
                 bc=bc_p, m=m, cc=cc, rel=(lambda c2: Ucerca(m, c2)), jsonld=[svc_ld(m, cc), bc_ld([("Inicio", DOM + "/"), (mn, DOM + Um(m)), (pn, DOM + Uc(m, cc)), ("Cerca de mí", DOM + Ucerca(m, cc))])])
            # ---- ciudades
            for ci in p["ciudades"]:
                cs = slug(ci); tecs = [t for t in tt if t["p"] == cc and t["c"] == ci]; fq = faq_gen(m, cc, ci)
                th = "".join(f'<div class="cd"><b>{esc(t["n"])}</b><br><span style="color:var(--mu)">{esc(t["z"])}, {esc(ci)}</span><p><a class="pill" data-evt="whatsapp" href="{wa(t["w"], f"Hola, necesito servicio técnico {mn} en {ci}")}" rel="noopener">WhatsApp</a></p></div>' for t in tecs)
                zc = [(n, Uz(m, cc, n)) for n, t, c in zs if c == ci]
                eqh = "".join(f'<a class="cd" href="{Ucek(m,cc,ci,k)}"><img src="{imgk(m,cc,k,1)}" alt="{esc(ALT(m,k,ci))}" loading="lazy"><h3>{esc(cap(term(cc,k)))} {esc(mn)} en {esc(ci)}</h3></a>' for k in EQ)
                body = sec(f"Técnicos {mn} en {ci}", f'<div class="g">{th}</div>') + sec(f"Equipos {mn} que reparamos en {ci}", f'<div class="g">{eqh}</div>') \
                    + (sec(f"Barrios de {ci} donde atendemos", pills(zc)) if zc else "") + sec(f"Preguntas frecuentes en {ci}", faqh(fq)) + sec("Búsquedas relacionadas", kw_html(m, cc, ci=ci))
                page(Uci(m, cc, ci)[1:], f"Soporte técnico autorizado {mn} {ci}, {pn}: {term(cc,'neveras')}, lavadoras y secadoras",
                     f"Servicio técnico {mn} cerca de ti en {ci}, {pn}: reparación a domicilio de {term(cc,'neveras')}, {term(cc,'lavadoras')} y {term(cc,'secadoras')} {mn}. WhatsApp del técnico más cercano a tu barrio.",
                     f"Soporte técnico autorizado {mn} en {ci}", f"Técnico {mn} a domicilio en {ci}, {pn}.", body, bc=bc_p, m=m, cc=cc, ci=ci, rel=None,
                     jsonld=[svc_ld(m, cc, ci), faq_ld(fq), bc_ld([("Inicio", DOM + "/"), (mn, DOM + Um(m)), (pn, DOM + Uc(m, cc)), (ci, DOM + Uci(m, cc, ci))])])
                for k, e in EQ.items():
                    fq = faq_gen(m, cc, ci, k) + [(txt(q, m, cc, k), txt(a, m, cc, k)) for q, a in e["faq"][:3]]
                    fl = pills([(txt(f[0], m, cc, k), Uf(m, cc, k, f[0])) for f in e["fallas"][:6]])
                    body = sec(f"Fallas frecuentes en {term(cc,k)} {mn} en {ci}", fl) + sec(f"Preguntas frecuentes", faqh(fq)) + sec("Búsquedas relacionadas", kw_html(m, cc, ci=ci, k=k)) \
                        + sec("Más cerca de ti", pills([(f"{mn} en {ci}", Uci(m, cc, ci)), (f"{cap(term(cc,k))} {mn} en {pn}", Ue(m, cc, k))]))
                    t = f"Soporte técnico autorizado {mn}: {term(cc,k)} en {ci}"
                    page(Ucek(m, cc, ci, k)[1:], f"{t}, {pn}: técnico a domicilio", f"{t}: técnico {mn} a domicilio en {ci}, {pn}. Diagnóstico, repuestos y garantía. Pide tu solicitud por WhatsApp.", t,
                         f"Técnico {mn} a domicilio en {ci}, {pn}.", body, bc=bc_p + [(ci, Uci(m, cc, ci))], m=m, cc=cc, ci=ci, rel=None, eq=k,
                         jsonld=[svc_ld(m, cc, ci, k), faq_ld(fq), bc_ld([("Inicio", DOM + "/"), (mn, DOM + Um(m)), (pn, DOM + Uc(m, cc)), (ci, DOM + Uci(m, cc, ci)), (cap(term(cc, k)), DOM + Ucek(m, cc, ci, k))])])
            # ---- barrios / zonas
            for n, tipo, ci in zs:
                a, b = base.TIPO_TXT[tipo]; fq = faq_gen(m, cc, ci)[:6]
                body = sec(f"Servicio técnico {mn} en {n}", f"<p>{esc(txt(a,m,cc))}</p><p>{esc(txt(b,m,cc))}</p>") + sec(f"Equipos {mn} que reparamos en {n}", pills([(f"{cap(term(cc,k))} {mn}", Ue(m, cc, k)) for k in EQ])) \
                    + sec("Preguntas frecuentes", faqh(fq)) + sec("Búsquedas relacionadas", kw_html(m, cc, ci=ci, zona=n)) + sec("Cerca de aquí", pills([(f"{mn} en {ci}", Uci(m, cc, ci))]))
                page(Uz(m, cc, n)[1:], f"Soporte técnico autorizado {mn} {n}, {ci}: neveras, lavadoras y secadoras",
                     f"Técnico {mn} a domicilio en {n}, {ci} ({pn}): reparación de {term(cc,'neveras')}, {term(cc,'lavadoras')} y {term(cc,'secadoras')} {mn}. Pide tu solicitud por WhatsApp.",
                     f"Soporte técnico autorizado {mn} en {n}, {ci}", f"Técnico {mn} a domicilio en el barrio {n}.", body, bc=bc_p, m=m, cc=cc, ci=ci, rel=None,
                     jsonld=[svc_ld(m, cc, ci), faq_ld(fq), bc_ld([("Inicio", DOM + "/"), (mn, DOM + Um(m)), (pn, DOM + Uc(m, cc)), (n, DOM + Uz(m, cc, n))])])
            # ---- equipos, fallas, mantenimiento, costo, códigos
            for k, e in EQ.items():
                eqn = f"{term(cc,k)} {mn}"; t = f"Soporte técnico autorizado {mn}: {term(cc,k)} en {pn}"; a2 = alt(cc, k)
                fl = "".join(f'<a class="cd" href="{Uf(m,cc,k,f[0])}"><span class="urg">{esc(f[2])}</span><h3>{esc(txt(f[0],m,cc,k))}</h3><p style="margin:0;color:var(--mu)">{esc(txt(f[1],m,cc,k)[:120])}…</p></a>' for f in e["fallas"])
                fq = [(txt(q, m, cc, k), txt(a, m, cc, k)) for q, a in e["faq"]] + faq_gen(m, cc, None, k)[:5]
                mod = "".join(f"<li>{esc(x)}</li>" for x in e["modelos"])
                extra = [("Mantenimiento", Umant(m, cc, k)), ("¿Cuánto cuesta reparar?", Ucosto(m, cc, k))] + ([("Códigos de error", Ucod(m, cc, k))] if (k == "lavadoras" and m in CODIGOS) else [])
                body = sec(f"Fallas comunes en {eqn}", f'<div class="g">{fl}</div>') + sec(f"Modelos de {eqn} que atendemos", f"<ul>{mod}</ul>") \
                    + sec("Guías", pills(extra)) + sec("Preguntas frecuentes", faqh(fq)) + sec("Búsquedas relacionadas", kw_html(m, cc, k=k)) \
                    + sec("Por ciudad", pills([(f"{c}", Ucek(m, cc, c, k)) for c in p["ciudades"]]))
                page(Ue(m, cc, k)[1:], f"{t}: reparación a domicilio", f"{t}{' (' + a2 + ')' if a2 else ''}. Reparación a domicilio, diagnóstico y garantía. Solicita al técnico {mn} más cercano a tu barrio por WhatsApp.", t,
                     txt(e["intro"], m, cc, k)[:170], body, bc=bc_p, m=m, cc=cc, rel=(lambda c2: Ue(m, c2, k)), eq=k,
                     jsonld=[svc_ld(m, cc, None, k), faq_ld(fq), bc_ld([("Inicio", DOM + "/"), (mn, DOM + Um(m)), (pn, DOM + Uc(m, cc)), (cap(term(cc, k)), DOM + Ue(m, cc, k))])])
                bc_k = bc_p + [(cap(term(cc, k)), Ue(m, cc, k))]
                for f in e["fallas"]:
                    ft = txt(f[0], m, cc, k); fs = slug(f[0]); otras = pills([(txt(x[0], m, cc, k), Uf(m, cc, k, x[0])) for x in e["fallas"] if x[0] != f[0]][:8])
                    fq = [(f"¿Por qué {ft[0].lower() + ft[1:]}?" if False else f"¿Por qué pasa: «{ft}»?", txt(f[1], m, cc, k)),
                          (f"¿Es peligroso seguir usando mi {sing(cc,k)} {mn} así?", f"Nivel de urgencia: {f[2].lower()}. " + txt(f[3], m, cc, k)),
                          (f"¿Cuánto cuesta arreglar esta falla en {pn}?", f"Depende de la pieza y la mano de obra. El técnico {mn} confirma el costo en {p['moneda']} antes de reparar."),
                          (f"¿Puedo arreglarlo yo mismo?", "Puedes revisar lo básico (energía, llaves de agua, limpieza). Para piezas internas conviene un técnico, para evitar daños mayores.")]
                    body = sec("¿Por qué pasa?", f"<p>{esc(txt(f[1],m,cc,k))}</p>") + sec("Qué hacer mientras llega el técnico", f"<p>{esc(txt(f[3],m,cc,k))}</p><p><span class='urg'>Urgencia: {esc(f[2])}</span></p>") \
                        + sec("Preguntas frecuentes", faqh(fq)) + sec("Otras fallas frecuentes", otras) + sec("Búsquedas relacionadas", kw_html(m, cc, k=k, falla=f[0])) \
                        + sec("Servicio por ciudad", pills([(c, Ucek(m, cc, c, k)) for c in p["ciudades"]]))
                    page(Uf(m, cc, k, f[0])[1:], f"{ft} – soporte técnico autorizado {mn} {pn}", f"{ft} en tu {sing(cc,k)} {mn} ({pn}): causas, qué hacer y cuándo llamar al técnico. Solicita servicio a domicilio por WhatsApp.",
                         f"{ft}: soporte técnico autorizado {mn} en {pn}", f"Causas, qué hacer y técnico {mn} a domicilio.", body, bc=bc_k, m=m, cc=cc, rel=(lambda c2: Uf(m, c2, k, f[0])), eq=k, falla=txt(f[0], m, cc, k),
                         jsonld=[faq_ld(fq), bc_ld([("Inicio", DOM + "/"), (mn, DOM + Um(m)), (pn, DOM + Uc(m, cc)), (cap(term(cc, k)), DOM + Ue(m, cc, k)), (ft, DOM + Uf(m, cc, k, f[0]))])])
                # mantenimiento
                mant = "".join(f"<li>{esc(txt(x,m,cc,k))}</li>" for x in e["mant"])
                page(Umant(m, cc, k)[1:], f"Soporte técnico autorizado {mn} {pn}: mantenimiento de {term(cc,k)}", f"Cómo cuidar tu {sing(cc,k)} {mn} y cuándo pedir mantenimiento a domicilio en {pn}.",
                     f"Mantenimiento de {eqn} en {pn}: soporte técnico autorizado", "Hábitos simples que alargan la vida del equipo.", sec("Consejos de mantenimiento", f"<ul>{mant}</ul>") + sec("Búsquedas relacionadas", kw_html(m, cc, k=k)),
                     bc=bc_k, m=m, cc=cc, rel=(lambda c2: Umant(m, c2, k)), eq=k, jsonld=[bc_ld([("Inicio", DOM + "/"), (mn, DOM + Um(m)), (pn, DOM + Uc(m, cc)), ("Mantenimiento", DOM + Umant(m, cc, k))])])
                # costo
                fq = faq_gen(m, cc, None, k)[2:5]
                body = sec("Qué define el costo", "<ul><li>La falla: una pieza pequeña no cuesta como una tarjeta o un compresor.</li><li>La pieza: disponibilidad y tipo de repuesto.</li><li>La mano de obra y el tiempo de la visita.</li><li>La zona: distancia entre el técnico y tu barrio.</li></ul>") \
                    + sec("Cómo trabajamos el presupuesto", f"<p>El técnico {esc(mn)} revisa tu equipo, te explica la falla y te da el costo en {esc(p['moneda'])} antes de empezar. No se repara nada sin tu aprobación.</p>") + sec("Preguntas frecuentes", faqh(fq))
                page(Ucosto(m, cc, k)[1:], f"¿Cuánto cuesta reparar {sing(cc,k)} {mn} en {pn}? Soporte técnico autorizado", f"Qué define el precio de reparar {eqn} en {pn} y cómo pedir una cotización por WhatsApp.",
                     f"¿Cuánto cuesta reparar {sing(cc,k)} {mn} en {pn}?", "Lo que influye en el precio y cómo cotizar sin compromiso.", body, bc=bc_k, m=m, cc=cc, rel=(lambda c2: Ucosto(m, c2, k)), eq=k,
                     jsonld=[faq_ld(fq), bc_ld([("Inicio", DOM + "/"), (mn, DOM + Um(m)), (pn, DOM + Uc(m, cc)), ("Costo", DOM + Ucosto(m, cc, k))])])
                if k == "lavadoras" and m in CODIGOS:
                    rows = "".join(f"<tr><td><b>{esc(c)}</b></td><td>{esc(s)}</td><td>{esc(q)}</td></tr>" for c, s, q in CODIGOS[m])
                    body = sec(f"Códigos de error de lavadoras {mn}", f'<div style="overflow-x:auto"><table style="border-collapse:collapse;width:100%"><thead><tr><th align=left>Código</th><th align=left>Significado</th><th align=left>Causas frecuentes</th></tr></thead><tbody>{rows}</tbody></table></div><p style="color:var(--mu)">Los códigos pueden variar según el modelo; consulta el manual.</p>') + sec("Búsquedas relacionadas", kw_html(m, cc, k=k))
                    page(Ucod(m, cc, k)[1:], f"Códigos de error de lavadoras {mn} en {pn}: soporte técnico autorizado", f"Significado de los códigos de error de las lavadoras {mn} y cuándo pedir un técnico en {pn}.",
                         f"Códigos de error de lavadoras {mn}", "Qué significa cada código y qué hacer.", body, bc=bc_k, m=m, cc=cc, rel=(lambda c2: Ucod(m, c2, k)), eq=k,
                         jsonld=[bc_ld([("Inicio", DOM + "/"), (mn, DOM + Um(m)), (pn, DOM + Uc(m, cc)), ("Códigos de error", DOM + Ucod(m, cc, k))])])
    # ---- estáticos
    (OUT / "datos.js").write_text("window.DATOS=" + json.dumps({c: {"n": p["nombre"], "wa": p["wa"], "dial": p["dial"], "ps": PS[c], "ciudades": p["ciudades"], "voc": {k: term(c, k) for k in EQ}} for c, p in PA.items()}, ensure_ascii=False) + ";", encoding="utf-8")
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
    for nombre, filtro in [("inicio", lambda u: u.rstrip("/") == DOM)] + [(m, (lambda mm: (lambda u: u.startswith(f"{DOM}/soporte-tecnico-autorizado-{mm}")))(m)) for m in MA]:
        us = sorted(u for u in set(PAGES) if filtro(u))
        (OUT / f"sitemap-{nombre}.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{u}</loc><changefreq>monthly</changefreq></url>" for u in us) + "</urlset>", encoding="utf-8")
        idx.append(f"<sitemap><loc>{DOM}/sitemap-{nombre}.xml</loc></sitemap>")
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(idx) + "</sitemapindex>", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {DOM}/sitemap.xml\n", encoding="utf-8")
    (OUT / "llms.txt").write_text(f"# {NOM}\n> Servicio técnico a domicilio por marca (neveras, lavadoras, secadoras) en " + ", ".join(p["nombre"] for p in PA.values()) + ".\n" + "".join(f"- {v['nombre']}: {DOM}{Um(m)}\n" for m, v in MA.items()), encoding="utf-8")
    (OUT / ".htaccess").write_text("DirectoryIndex index.html\nAddType application/manifest+json .webmanifest\nHeader set Permissions-Policy \"geolocation=(self)\"\n", encoding="utf-8")
    print(f"{len(set(PAGES))} páginas")
    if faltan:
        print("⚠ FALTAN WhatsApp para: " + ", ".join(PA[c]["nombre"] for c in faltan))
        if ESTRICTO: sys.exit(1)

build()
