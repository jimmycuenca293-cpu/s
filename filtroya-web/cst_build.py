# -*- coding: utf-8 -*-
"""Genera centrodeserviciotecnicopanama.com: portada Samsung + una sección fuerte por marca.
Uso: python3 cst_build.py <salida> [carpeta_imagenes_origen=/tmp/cst_src]"""
import sys, os, re, json, html, shutil, pathlib, hashlib, glob
from cst_datos import M, EQ, BRANDS_ORDER, ZONAS
from cst_consejos import C as CONSEJOS, LLAMAR, USAR
from cst_sitio import CFG, localizar, L as LOC
if CFG.get("tv"):
    import cst_tv as _TV
    M, EQ, BRANDS_ORDER, CONSEJOS = _TV.M, _TV.EQ, _TV.BRANDS_ORDER, _TV.CONSEJOS
M = localizar(M); CONSEJOS = localizar(CONSEJOS)
if "neveras" in EQ: EQ["neveras"] = CFG["nev"]
if CFG.get("zonas"): ZONAS = CFG["zonas"]

OUT = pathlib.Path(sys.argv[1]); SRC = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "/tmp/cst_src")
DOM = CFG["dom"]; NOMBRE = CFG["nombre"]; TEL = CFG["tel"]; TELN = CFG["telw"]; GSC = CFG["gsc"]
import datetime as _dt
_MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
_hoy = _dt.date.today()
HOY = _hoy.isoformat()
HOY_TXT = f"{_hoy.day} de {_MESES[_hoy.month - 1]} de {_hoy.year}"
esc = html.escape
ROOT = pathlib.Path(__file__).resolve().parent
paginas = []   # (url, prioridad, marca)
TITULOS = {}

# ---------------------------------------------------------------- imágenes
EXCLUIR = {  # carteles de «autorizado»/«oficial», Costa Rica, sellos de garantía, fondos rotos o casi duplicadas (revisadas a mano)
 "banner-tecnico-kitchenaid-confiado", "secretaria-kitchenaid-escritorio", "tecnico-kitchenaid-reparando-batidora", "tecnico-kitchenaid-domicilio-furgon",
 "recepcion-whirlpool-1", "recepcion-whirlpool-2", "tecnico-whirlpool-diagnostico-lavadora-2",
 "tecnico-mabe-camino-centro-reparacion", "tecnico-mabe-saludo-cliente-puerta", "torre-lavado-secado-mabe-garantia", "banner-instalaciones-mabe",
 "agente-electrolux-mostrador-cliente", "banner-urgencias-tecnicas-electrolux", "refrigeradora-electrolux-side-by-side-negra",
 "banner-frigidaire-cocina", "recepcion-frigidaire-2", "tecnico-frigidaire-kitchen-2",
 "producto-lavadora-carga-superior-haceb", "producto-hornos-ge", "producto-lavadoras-ge", "producto-lavavajillas-ge", "producto-neveras-ge",
 "tecnico-lg-autorizado", "tecnico-lg-recepcion-2", "tecnico-lg-recepcion-4",
 "tecnico-mabe-diagnostico-lavadora-cliente", "tecnico-mabe-llegada-domicilio-cliente", "tecnico-whirlpool-diagnostico-lavadora-1", "tecnico-whirlpool-perfil", "tecnico-reparando-lavadora-samsung", "tecnico-reparando-refrigeradora-samsung-en-cocina", "tecnico-samsung-visita-a-domicilio-7", "tecnico-autorizado-nevera", "tecnico-domicilio-furgon", "tecnico-reparando-secadora", "producto-aire-samsung-pared"}
def pool(m):
    d = SRC / m
    if CFG.get("sin_recorte"):   # Guayaquil: se usan TODAS las fotos de la marca (menos logos y miniaturas duplicadas)
        fs = [f for f in sorted(d.glob("*.webp")) if "logo" not in f.name and not re.search(r"-(s|m|400)\.webp$", f.name)] if d.exists() else []
    else:
        fs = [f for f in sorted(d.glob("*.webp")) if "logo" not in f.name and "autorizado" not in f.name and f.stem not in EXCLUIR] if d.exists() else []
    extra = ROOT / "st_img" / "cst" / m
    if extra.exists() and not CFG.get("tv"): fs += sorted(extra.glob("*.webp"))
    if m == "samsung" and not CFG.get("tv"):
        for p in sorted((ROOT / "st_img" / "panama").glob("*.webp")): fs.append(p)
        for p in sorted(glob.glob("/tmp/pan_img_work/img/*.webp")):
            n = os.path.basename(p)
            if re.search(r"-(s|m|400)\.webp$", n) or "logo" in n or "oval" in n: continue
            if re.match(r"(nevera|lavadora|secadora|lavavajillas|estufa|microondas|tecnico|horno|aire|asesora|equipo|servicio)" if CFG.get("sin_recorte") else r"(nevera|lavadora|secadora|lavavajillas|estufa|microondas|tecnico|horno|aire)", n): fs.append(pathlib.Path(p))
    # sin duplicados por contenido
    vis, out = set(), []
    for f in fs:
        h = hashlib.md5(f.read_bytes()).hexdigest()
        if h not in vis: vis.add(h); out.append(f)
    return out
POOLS = {m: pool(m) for m in BRANDS_ORDER}
KW = {"neveras": r"nevera|refriger|french|side-by-side|family", "lavadoras": r"lavadora", "secadoras": r"secadora", "aires": r"aire|windfree",
      "cocinas": r"estufa|horno|cocina", "lavavajillas": r"lavavajillas", "centro-lavado": r"centro-lavado|torre|washtower", "batidoras": r"batidora", "microondas": r"microondas", "tv-led": r"televisor|\btv\b|pantalla", "tv-qled": r"televisor|\btv\b|pantalla", "tv-oled": r"televisor|\btv\b|pantalla", "_gente": r"tecnico|asesora|recepcion|equipo|saluda|agente|secretaria"}
import collections
USO = collections.Counter()
def copia(m, f):
    n = re.sub(r"[^a-z0-9.-]", "-", f.name.lower().replace("autorizado", "servicio").replace("oficial", "servicio"))
    d = OUT / "img" / m; d.mkdir(parents=True, exist_ok=True)
    if not (d / n).exists(): shutil.copyfile(f, d / n)
    return f"/img/{m}/{n}"
def alt_de(m, f, extra=""):
    """Texto alternativo descriptivo (SEO y accesibilidad): qué muestra la foto, de qué marca y en qué ciudad."""
    n = f.name.lower(); N = M[m]["nombre"]; ciu = CFG["ciudad"]
    eq = None
    for rx, nombre in ((r"centro-lavado|torre|washtower", "Centro de lavado"), (r"lavavajillas", "Lavavajillas"), (r"microondas", "Microondas"), (r"secadora", "Secadora"), (r"lavadora", "Lavadora"),
                       (r"aire|windfree", "Aire acondicionado"), (r"horno", "Horno empotrado"), (r"estufa|cocina|hornillas", "Cocina"), (r"nevera|refriger|family|french|side-by-side|top-freezer", "Refrigeradora"), (r"batidora", "Batidora de pedestal")):
        if re.search(rx, n): eq = nombre; break
    rasgos = [t for rx, t in ((r"side-by-side", "side by side"), (r"french", "french door"), (r"top-freezer|congelador-superior", "con congelador arriba"), (r"frontal", "de carga frontal"), (r"carga-superior", "de carga superior"),
                              (r"inverter", "inverter"), (r"dispensador", "con dispensador"), (r"family|familyhub", "Family Hub"), (r"empotr", "empotrado"), (r"windfree", "WindFree"), (r"interior|abierta", "abierta por dentro")) if re.search(rx, n)]
    _ok = {"Refrigeradora": {"side by side", "french door", "con congelador arriba", "inverter", "con dispensador", "Family Hub", "abierta por dentro"}, "Lavadora": {"de carga frontal", "de carga superior"}, "Secadora": {"de carga frontal", "de carga superior"},
           "Centro de lavado": set(), "Aire acondicionado": {"inverter", "WindFree"}, "Cocina": set(), "Horno empotrado": {"empotrado"}, "Lavavajillas": set(), "Microondas": set(), "Batidora de pedestal": set()}
    rasgos = [r_ for r_ in rasgos if r_ in _ok.get(eq, set())]
    gente = re.search(r"tecnico|asesora|recep|agente|equipo-de|taller|secretaria|mostrador|cliente|servicio-centro|banner", n)
    if gente:
        if re.search(r"banner", n): t = f"Servicio técnico {N} a domicilio en {ciu}"
        elif re.search(r"asesora|recep|mostrador|agente|secretaria|telefono|oficina", n): t = f"Asesora de atención al cliente de {N} coordinando una visita en {ciu}"
        elif re.search(r"taller|equipo-de", n): t = f"Equipo de técnicos en el taller de servicio {N}"
        elif re.search(r"saluda|llegada|llegando|puerta|furgon|domicilio-cliente|portada", n): t = f"Técnico {N} llegando a un domicilio en {ciu} para una visita de servicio"
        elif re.search(r"tablet|explicando|entrega|orden", n): t = f"Técnico {N} explicando el diagnóstico a un cliente en {ciu}"
        elif eq: t = f"Técnico {N} reparando {('una ' if eq in ('Refrigeradora','Lavadora','Secadora','Cocina') else 'un ')}{eq.lower()} en {ciu}"
        else: t = f"Técnico {N} atendiendo a un cliente en {ciu}"
    elif eq: t = f"{eq} {N} {' '.join(rasgos)} que reparamos en {ciu}".replace("  ", " ")
    else: t = f"Equipos {N} en {ciu}"
    return esc(re.sub(r"\s+", " ", t).strip())
def elegir(m, clave, cuantas=2, equipo=None):
    p = POOLS[m]
    if equipo is None: equipo = "_gente"
    if not p: return []
    cand = []
    if equipo and equipo in KW: cand = [f for f in p if re.search(KW[equipo], f.name)]
    h = lambda f: hashlib.md5((clave + f.name).encode()).hexdigest()
    if equipo in KW and equipo != "_gente":
        # una página de un equipo solo muestra fotos de ESE equipo o de personas; nunca de otro electrodoméstico
        gente = re.compile(KW["_gente"])
        rest = [f for f in p if f not in cand and gente.search(f.name)]
        orden = sorted(cand, key=lambda f: (USO[f], h(f))) + sorted(rest, key=lambda f: (USO[f], h(f)))
        if not orden: orden = sorted(p, key=lambda f: (USO[f], h(f)))
    else:
        rest = [f for f in p if f not in cand]
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
 "sony": ("#16161a", "#3b82f6", "#fff", "#f3f4f6", "#e5e7eb", "#0a0a0c"),
 "tcl": ("#d71920", "#1a1a1a", "#fff", "#fbf3f3", "#f6dede", "#6b0a0e"),
 "hisense": ("#00857f", "#00a19b", "#fff", "#eef8f8", "#d8eeed", "#00504d"),
 "philips": ("#0b5ed7", "#0b5ed7", "#fff", "#eef4fd", "#dbe8fb", "#082f6b"),
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
.hero{position:relative;background:var(--hd) var(--bgi,none) center/cover;color:#fff;padding:36px 0}.hero:before{content:"";position:absolute;inset:0;background:linear-gradient(135deg,var(--c),var(--hd));opacity:.9}.hero .w{position:relative;display:grid;gap:24px;align-items:center}.hero p{opacity:.94;font-size:1.08rem}.hero .bd{display:inline-block;background:rgba(255,255,255,.14);padding:5px 12px;border-radius:999px;font-size:.85rem;font-weight:600;margin-bottom:12px}.hero img{border-radius:var(--r);box-shadow:0 14px 40px rgba(0,0,0,.35);width:100%;aspect-ratio:4/3;object-fit:cover}
@media(min-width:860px){.hero .w{grid-template-columns:1.1fr .9fr}}
section.s{padding:30px 0}section.s.alt{background:var(--w)}.lead{color:var(--m);max-width:760px}
.band{position:relative;padding:56px 0;color:#fff;background:var(--hd) var(--bgi,none) center/cover;text-align:center}.band:before{content:"";position:absolute;inset:0;background:linear-gradient(135deg,var(--c),var(--hd));opacity:.82}.band .w{position:relative}.band h2{color:#fff}.band p{max-width:640px;margin:0 auto 18px}
.ph{background:linear-gradient(rgba(255,255,255,.93),rgba(255,255,255,.93)),var(--bgi) center/cover!important}
.gal{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}.gal img{aspect-ratio:4/3;object-fit:cover;width:100%;border-radius:16px;box-shadow:var(--sh)}
.stp{display:flex;gap:8px;flex-wrap:wrap;list-style:none;padding:0;margin:0 0 16px;counter-reset:s}.stp li{counter-increment:s;display:flex;align-items:center;gap:8px;background:var(--w);border-radius:999px;padding:6px 14px 6px 6px;font-weight:700;font-size:.9rem;box-shadow:var(--sh);opacity:.55}.stp li:before{content:counter(s);width:26px;height:26px;border-radius:50%;background:var(--soft);color:var(--c);display:grid;place-items:center}.stp li.on{opacity:1;outline:2px solid var(--c)}.stp li.on:before{background:var(--c);color:#fff}
.tiles{display:grid;gap:14px;grid-template-columns:repeat(auto-fill,minmax(150px,1fr))}@media(min-width:700px){.tiles{grid-template-columns:repeat(auto-fill,minmax(210px,1fr))}}
.tile{display:flex;flex-direction:column;background:var(--w);border-radius:var(--r);overflow:hidden;box-shadow:var(--sh);text-decoration:none;color:var(--t);border:2px solid transparent;transition:.15s}.tile:hover{transform:translateY(-3px);border-color:var(--a)}
.ti-img{aspect-ratio:4/3;background:var(--soft);display:grid;place-items:center;font-size:2.4rem;font-weight:800;color:var(--c)}.ti-img img{width:100%;height:100%;object-fit:contain;padding:10px}
.tile b{padding:12px 14px 0;font-size:1.05rem;color:var(--c)}.tile small{padding:2px 14px;color:var(--m)}.tile .go{margin:auto 14px 14px;padding-top:8px;font-weight:700;color:var(--c)}
.symb{display:grid;gap:10px}@media(min-width:700px){.symb{grid-template-columns:1fr 1fr}}.sy{display:flex;gap:12px;align-items:center;background:var(--w);padding:14px 16px;border-radius:14px;box-shadow:var(--sh);text-decoration:none;color:var(--t);border:2px solid transparent}.sy:hover{border-color:var(--a)}.sy b{display:block;line-height:1.3}.sy small{color:var(--m)}.sy i{font-style:normal;font-weight:800;color:var(--c);font-size:1.4rem}
.anc{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 18px}.anc a{padding:8px 14px;background:var(--w);border-radius:999px;box-shadow:var(--sh);text-decoration:none;font-weight:600;font-size:.9rem}
.cta-box{display:grid;gap:12px}@media(min-width:700px){.cta-box{grid-template-columns:1fr 1fr}}.cta-box .card{display:flex;flex-direction:column;gap:8px;align-items:flex-start}
.sec-h{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}.sec-h small{color:var(--m)}
.upd{font-size:.85rem;color:var(--m);margin:6px 0 28px}
.pz{display:grid;gap:10px;margin:0}.pz dt{font-weight:800;color:var(--c)}.pz dd{margin:0 0 8px;padding-bottom:8px;border-bottom:1px solid #e3eaf4}.lgo{display:block;height:34px;width:auto;max-width:130px;object-fit:contain}.hl{display:inline-block;margin:0 0 14px}.hero .hl img{display:block;height:56px;width:auto;max-width:260px;aspect-ratio:auto;object-fit:contain;border-radius:0;box-shadow:none}@media(max-width:520px){.lgo{height:28px;max-width:96px}.logo span{font-size:.85rem}}.fl{display:inline-block;margin:0 0 20px}.fl img{display:block;height:44px;width:auto;max-width:190px;object-fit:contain}.logo{display:flex;align-items:center;gap:10px}.logo span{display:block;line-height:1.15}.skip{position:absolute;left:-999px;top:0;background:#fff;color:#000;padding:10px 14px;z-index:99}.skip:focus{left:8px;top:8px}.rr{background:var(--soft);border-left:5px solid var(--a);padding:16px 18px;border-radius:12px;margin:0 0 18px}.rr b{display:block;margin-bottom:4px;color:var(--c)}
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
if CFG.get("sin_recorte"):
    CSS += """
.hero img{aspect-ratio:auto!important;object-fit:contain!important;width:auto!important;max-width:100%;max-height:480px;height:auto!important;margin:0 auto;background:#fff}
.two img{aspect-ratio:auto!important;object-fit:contain!important;height:auto!important;max-height:520px;width:auto;max-width:100%;margin:0 auto}
.gal{align-items:start}.gal img{aspect-ratio:auto!important;object-fit:contain!important;height:auto!important;background:#fff}
.fgrid{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));align-items:start}
.fgrid figure,.gf{margin:0;background:#fff;border-radius:16px;padding:10px;box-shadow:var(--sh)}
.fgrid img,.gf img{display:block;width:100%;height:auto;max-height:440px;object-fit:contain;border-radius:10px}
.gf figcaption,.fgrid figcaption{font-size:.8rem;color:var(--m);margin-top:6px}
.why{display:grid;gap:14px}@media(min-width:800px){.why{grid-template-columns:repeat(3,1fr)}}.why .card h3{color:var(--c)}
.wab{display:flex;gap:10px;flex-wrap:wrap}.wab a{background:#1fa855;color:#fff;text-decoration:none;font-weight:700;padding:12px 18px;border-radius:999px}
"""
CSSV = hashlib.md5(CSS.encode()).hexdigest()[:10]
JS_WIZ = """<script>(function(){var d=window.WIZ;if(!d)return;var e=document.getElementById('wq'),s=document.getElementById('ws'),r=document.getElementById('wr');
function eq(){s.innerHTML='<option value="">Elige el síntoma…</option>';(d[e.value]||[]).forEach(function(x,i){var o=document.createElement('option');o.value=i;o.textContent=x[0];s.appendChild(o)});r.style.display='none'}
e.addEventListener('change',eq);s.addEventListener('change',function(){var x=(d[e.value]||[])[s.value];if(!x){r.style.display='none';return}
r.innerHTML='<b>Causa más probable</b><p>'+x[1]+'</p><b>Qué revisamos en la visita</b><p>'+x[2]+'</p><a class="btn" target="_blank" rel="noopener" href="https://wa.me/"""+TELN+"""?text='+encodeURIComponent('Hola, mi '+e.options[e.selectedIndex].text+' '+window.WIZB+' presenta: '+x[0]+'. Necesito servicio técnico en Panamá.')+'">Pedir visita por WhatsApp</a>';r.style.display='block'});eq()})();</script>"""

# ---------------------------------------------------------------- plantilla
def wa(txt): return f"https://wa.me/{TELN}?text=" + re.sub(r"[ ]", "%20", txt).replace("¿", "%C2%BF").replace("á", "%C3%A1").replace("é", "%C3%A9").replace("í", "%C3%AD").replace("ó", "%C3%B3").replace("ú", "%C3%BA").replace("ñ", "%C3%B1").replace(",", "%2C")
def chips(actual):
    if actual:
        d = M[actual]; b = base(actual)
        it = [("Inicio", b), ("Reparar mi equipo", b + "#equipos"), ("Fallas", pathb(actual, "fallas"))]
        if d["codigos"]: it.append(("Códigos de error", pathb(actual, "codigos-de-error")))
        it += [("Repuestos", pathb(actual, "repuestos")), ("Garantía", pathb(actual, "garantia")), ("Diagnóstico", pathb(actual, "diagnostico-por-sintoma")), *([("Instalación", pathb(actual, "instalacion-de-pantallas")), ("Mantenimiento", pathb(actual, "mantenimiento-de-pantallas"))] if CFG.get("tv") else []), (CFG.get("lbl_guias", "Guías"), pathb(actual, "guias")), ("Zonas", pathb(actual, "cobertura")), ("Teléfono", pathb(actual, "telefono-servicio-tecnico"))]
    else:
        it = [("Todas las marcas", "/marcas/")]
    return '<nav class="chips" aria-label="Menú"><div class="w">' + "".join(f'<a href="{u}">{esc(t)}</a>' for t, u in it) + '</div></nav>'
def pie(marca=None, lista_marcas=False):
    aviso = '<p><small>Servicio técnico independiente. Los nombres de marcas pertenecen a sus propietarios y se usan solo para indicar los equipos que reparamos.</small></p>'
    if marca:
        d = M[marca]; N = nom(marca)
        col1 = (f'<div><h3>Equipos {N}</h3><ul>' + "".join(f'<li><a href="{pathb(marca, "reparacion-" + EQ[e][0])}">{EQ[e][2].capitalize()} {N}</a></li>' for e in d["equipos"]) + '</ul></div>')
        col2 = (f'<div><h3>Servicio {N}</h3><ul>' + (f'<li><a href="{pathb(marca, "codigos-de-error")}">Códigos de error</a></li>' if d["codigos"] else "") +
                f'<li><a href="{pathb(marca, "fallas")}">Fallas frecuentes</a></li><li><a href="{pathb(marca, "repuestos")}">Repuestos</a></li><li><a href="{pathb(marca, "garantia")}">Garantía</a></li>{(f'<li><a href="{pathb(marca, "instalacion-de-pantallas")}">Instalación</a></li><li><a href="{pathb(marca, "mantenimiento-de-pantallas")}">Mantenimiento</a></li>' if CFG.get("tv") else "")}<li><a href="{pathb(marca, "cuanto-cuesta-la-reparacion")}">Costos</a></li><li><a href="{pathb(marca, "diagnostico-por-sintoma")}">Diagnóstico por síntoma</a></li><li><a href="{pathb(marca, "series-y-modelos")}">Series y modelos</a></li><li><a href="{pathb(marca, "guias")}">{CFG.get("lbl_guias", "Guías")}</a></li><li><a href="{pathb(marca, "glosario")}">Glosario</a></li></ul></div>')
        col3 = (f'<div><h3>Zonas</h3><ul><li><a href="{pathb(marca, "centro-de-servicio-cerca-de-mi")}">Cerca de mí</a></li><li><a href="{pathb(marca, "reparacion-a-domicilio")}">A domicilio</a></li>' + "".join(f'<li><a href="{pathb(marca, "servicio-tecnico-" + z)}">{v[0]}</a></li>' for z, v in list(ZONAS.items())[:5]) + '</ul></div>')
        col4 = (f'<div><h3>{N} Panamá</h3><ul><li><a href="{pathb(marca, "telefono-servicio-tecnico")}">Teléfono y WhatsApp</a></li><li><a href="{pathb(marca, "quienes-somos")}">Quiénes somos</a></li><li><a href="{pathb(marca, "politica-de-privacidad")}">Política de privacidad</a></li><li><a href="{pathb(marca, "terminos-y-condiciones")}">Términos y condiciones</a></li></ul>{aviso}<p>{TEL}</p></div>')
        cols = col1 + col2 + col3 + col4
    elif lista_marcas:
        cols = ('<div><h3>Marcas</h3><ul>' + "".join(f'<li><a href="{"/" if m == "samsung" else "/" + m + "/"}">{M[m]["nombre"]} Panamá</a></li>' for m in BRANDS_ORDER) + f'</ul></div><div><h3>{NOMBRE}</h3><p>{TEL}</p>{aviso}</div>')
    else:
        cols = f'<div><h3>{NOMBRE}</h3><p>{TEL}</p>{aviso}</div>'
    flogo = f'<span class="fl"><img src="/img/logos/{marca}-blanco.png" alt="Logo {nom(marca)}" width="190" height="48" style="display:block;height:44px;width:auto;max-width:200px;aspect-ratio:auto;object-fit:contain;border-radius:0;box-shadow:none"></span>' if marca else ""
    return ('<footer><div class="w">' + flogo + '<div class="g c4">' + cols + '</div></div></footer>'
            f'<div class="fb"><a href="tel:+{TELN}">Llamar</a><a class="wa" href="{wa("Hola, necesito servicio técnico en Panamá")}" target="_blank" rel="noopener">WhatsApp</a></div>')
LB = {"@type": "ProfessionalService", "knowsAbout": (["Reparación de pantallas LED", "Reparación de pantallas QLED y Mini LED", "Reparación de pantallas OLED", "Instalación de pantallas"] if CFG.get("tv") else ["Reparación de refrigeradoras", "Reparación de lavadoras", "Reparación de secadoras", "Aires acondicionados", "Cocinas y hornos"]) + [f"Servicio técnico {M[x]['nombre']}" for x in BRANDS_ORDER], "inLanguage": CFG["locale"], "@id": DOM + "/#negocio", "name": NOMBRE, "url": DOM + "/", "telephone": "+" + TELN, 
      "areaServed": [{"@type": "City", "name": c} for c in (CFG.get("area") or ["Ciudad de Panamá", "San Miguelito", "Arraiján", "La Chorrera", "Colón"])],
      "address": {"@type": "PostalAddress", "addressLocality": CFG["ciudad"], "addressRegion": CFG["region"], "addressCountry": CFG["cc"]}}
LB["contactPoint"] = [{"@type": "ContactPoint", "telephone": "+" + TELN, "contactType": "customer service", "availableLanguage": ["es"], "areaServed": CFG["cc"]}]
LB["knowsLanguage"] = "es"


def decorar(marca, cuerpo, hero, path):
    """Añade fondos y fotos de la marca: héroe con foto de fondo, banda de contacto, fondos suaves y galería. Sin repetir imagen dentro de la página."""
    p = POOLS.get(marca) or []
    vistas = set(re.findall(r'/img/[^"\')\s]+', cuerpo)) | ({hero[0]} if hero else set())
    es_eq = ("/falla-" in path) or ("/reparacion-" in path)
    def libre(clave, n=1, gente=True):
        h = lambda f: hashlib.md5((clave + f.name).encode()).hexdigest()
        cand = [f for f in p if not any(copia_ruta(marca, f) == v for v in vistas)]
        rx = re.compile(KW["_gente"])
        if es_eq: cand = [f for f in cand if rx.search(f.name)]   # en páginas de un equipo, solo fotos de personas/servicio (nunca de otro electrodoméstico)
        cand = sorted(cand, key=lambda f: ((not rx.search(f.name)) if gente else bool(rx.search(f.name)), USO[f], h(f)))[:n]
        out = []
        for f in cand:
            USO[f] += 1; r = copia(marca, f); vistas.add(r); out.append((r, alt_de(marca, f)))
        return out
    bg = libre(path + "hero")
    bgi = f"url({bg[0][0]})" if bg else "none"
    # banda de contacto tras la primera sección
    b = libre(path + "banda")
    banda = ""
    if b:
        banda = (f'<section class="band" style="--bgi:url({b[0][0]})"><div class="w"><h2>Pide tu visita {nom(marca)} hoy</h2><p>Cuéntanos el modelo y la falla por WhatsApp y coordinamos el día y la franja en tu zona.</p>'
                 f'<a class="btn" href="{wa("Hola, necesito servicio técnico " + nom(marca) + " en Panamá")}" target="_blank" rel="noopener">Escribir por WhatsApp</a></div></section>')
    i = cuerpo.find("</section>")
    if banda and i >= 0 and cuerpo.count("</section>") >= 3: cuerpo = cuerpo[:i + 10] + banda + cuerpo[i + 10:]
    # fondos suaves en secciones alternas (hasta 2)
    for k in range(2):
        f2 = libre(path + f"ph{k}")
        if not f2: break
        cuerpo = cuerpo.replace('<section class="s alt">', f'<section class="s alt ph" style="--bgi:url({f2[0][0]})">', 1)
    # galería final
    es_equipo = ("/falla-" in path) or ("/reparacion-" in path)
    g = libre(path + "gal", 4, gente=es_equipo)
    if len(g) >= 2 and not CFG.get("sin_recorte"):   # Guayaquil/Cali/Panamá nuevos: las fotos del contenido van completas en franjas, no en galería recortada
        cuerpo += sec((f"Nuestro servicio {nom(marca)} en Panamá" if es_equipo else f"Equipos y servicio {nom(marca)} en Panamá"), '<div class="gal">' + "".join(f'<img loading="lazy" src="{u}" alt="{a}" width="1024" height="768">' for u, a in g) + '</div>')
    return cuerpo, bgi
def copia_ruta(m, f):
    return f"/img/{m}/" + re.sub(r"[^a-z0-9.-]", "-", f.name.lower())

def FAV(marca):
    c = PAL.get(marca, DEF)[0] if marca else DEF[0]
    ini = {"samsung": "S", "lg": "LG", "whirlpool": "W", "mabe": "m", "frigidaire": "F", "electrolux": "E", "general-electric": "GE", "haceb": "H", "kitchenaid": "K"}.get(marca, "CS")
    fs = 34 if len(ini) == 1 else 26
    svg = f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'><rect width='64' height='64' rx='14' fill='{c}'/><text x='32' y='{32 + fs * 0.36:.0f}' font-family='Arial,sans-serif' font-weight='700' font-size='{fs}' fill='white' text-anchor='middle'>{ini}</text></svg>"
    return "data:image/svg+xml," + svg.replace("<", "%3C").replace(">", "%3E").replace("#", "%23").replace(" ", "%20").replace("'", "%27")
def pagina(path, title, desc, h1, cuerpo, marca=None, hero=None, crumbs=None, ld=None, bd=None, prio="0.7", extra_js="", lead=None, noindex=False, marcas_ok=False, cta2=None):
    """path: '/lg/reparacion-lavadoras/' ; cuerpo: html de secciones"""
    title = LOC(title); desc = LOC(desc)
    if len(title) > 62:
        partes = title.split(" | ")
        while len(" | ".join(partes)) > 62 and len(partes) > 1: partes.pop()
        title = " | ".join(partes)
        if len(title) > 62: title = re.sub(r"(\s+(?:de|en|y|a|la|el|los|las|con|para|del|que|o|u|al))+$", "", title[:62].rsplit(" ", 1)[0].rstrip(" ,|-:"))
    if marca and len(title) < 38 and len(title) + 20 <= 62 and "Servicio técnico" not in title: title += " | Servicio técnico"
    if len(desc) < 125 and len(desc) + 38 <= 158 and not noindex: desc = desc.rstrip(" ") + " Atención a domicilio y por WhatsApp."
    if len(desc) > 158:
        oraciones = re.split(r"(?<=\.)\s+", desc); acum = ""
        for o in oraciones:
            if len((acum + " " + o).strip()) <= 158: acum = (acum + " " + o).strip()
            else: break
        desc = acum if len(acum) >= 70 else desc[:157].rsplit(" ", 1)[0].rstrip(" ,.;:") + "."
    if len(desc) < 100 and len(desc) + 38 <= 158 and not noindex: desc = desc.rstrip(" ") + " Atención a domicilio y por WhatsApp."
    color = M[marca]["color"] if marca else "#0b2a6f"
    url = DOM + path
    graf = [LB]
    graf.append({"@type": "WebSite", "@id": DOM + "/#sitio", "url": DOM + "/", "name": NOMBRE, "inLanguage": CFG["locale"], "publisher": {"@id": DOM + "/#negocio"}})
    wp = {"@type": "CollectionPage" if re.search(r"/(fallas|guias|codigos-de-error|series-y-modelos)/$", path) else "WebPage", "@id": url + "#pagina", "url": url, "name": title, "description": desc,
          "isPartOf": {"@id": DOM + "/#sitio"}, "about": {"@id": DOM + "/#negocio"}, "inLanguage": CFG["locale"], "dateModified": HOY, "datePublished": HOY}
    if hero: wp["primaryImageOfPage"] = {"@type": "ImageObject", "url": DOM + hero[0], "caption": hero[1], "width": 1024, "height": 768}
    graf.append(wp)
    if crumbs:
        graf.append({"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": DOM + u} for i, (n, u) in enumerate(crumbs)]})
    graf += ld or []
    for x in graf:
        if x.get("@type") == "Article":
            x["mainEntityOfPage"] = {"@id": url + "#pagina"}
            if hero: x["image"] = [DOM + hero[0]]
    bc = ""
    if crumbs and len(crumbs) > 1:
        bc = '<div class="w bc">' + " › ".join((f'<a href="{u}">{esc(n)}</a>' if i < len(crumbs) - 1 else esc(n)) for i, (n, u) in enumerate(crumbs)) + "</div>"
    bgi = "none"
    if marca and not noindex: cuerpo, bgi = decorar(marca, cuerpo, hero, path)
    himg = ""
    if hero: himg = f'<img src="{hero[0]}" alt="{hero[1]}" width="1024" height="768" fetchpriority="high" decoding="async">'
    heroh = (f'<section class="hero" style="--bgi:{bgi}"><div class="w"><div><span class="bd">{esc(bd or NOMBRE)}</span><h1>{esc(h1)}</h1><p>{lead or esc(desc)}</p>'
             f'<p><a class="btn" href="{wa(f"Hola, necesito servicio técnico {M[marca]['nombre']} en Panamá" if marca else "Hola, necesito servicio técnico en Panamá")}" target="_blank" rel="noopener">Escribir por WhatsApp</a> <a class="btn o" href="{cta2[1] if cta2 else "tel:+" + TELN}">{cta2[0] if cta2 else "Llamar " + TEL}</a></p></div>{himg}</div></section>')
    tags = "".join(f'<meta name="google-site-verification" content="{g}">' for g in GSC) if path == "/" else ""
    h = (f'<!doctype html><html lang="es-PA"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title>'
         f'<meta name="description" content="{esc(desc)}"><link rel="canonical" href="{url}"><link rel="alternate" hreflang="es-PA" href="{url}"><link rel="alternate" hreflang="x-default" href="{url}">{GEO_META}<meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="{PAL.get(marca, DEF)[0]}"><meta name="robots" content="{"noindex,follow" if noindex else "index,follow,max-image-preview:large,max-snippet:-1"}">{tags}'
         f'<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta property="og:locale" content="es_PA"><meta property="og:site_name" content="{esc(NOMBRE)}"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(desc)}"><meta property="article:modified_time" content="{HOY}">'
         + (f'<meta property="og:image" content="{DOM}{hero[0]}"><meta property="og:image:alt" content="{esc(hero[1])}"><meta name="twitter:image" content="{DOM}{hero[0]}"><link rel="preload" as="image" href="{hero[0]}" fetchpriority="high">' if hero else '') +
         f'<link rel="icon" href="{FAV(marca)}">'
         f'<link rel="stylesheet" href="/assets/site.css?v={CSSV}"><style>body{{--c:{PAL.get(marca, DEF)[0]};--a:{PAL.get(marca, DEF)[1]};--ab:{PAL.get(marca, DEF)[2]};--bg:{PAL.get(marca, DEF)[3]};--soft:{PAL.get(marca, DEF)[4]};--hd:{PAL.get(marca, DEF)[5]}}}</style><script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graf}, ensure_ascii=False)}</script></head><body><a class="skip" href="#contenido">Saltar al contenido</a>'
         f'<div class="top"><div class="w"><span>Atención a domicilio en Panamá · {TEL}</span><a href="{wa("Hola, necesito servicio técnico en Panamá")}" target="_blank" rel="noopener">WhatsApp</a></div></div>'
         f'<header class="h"><div class="w"><a class="logo" href="{base(marca) if marca else "/"}">{f'<img class="lgo" src="/img/logos/{marca}.png" alt="Logo {nom(marca)}" width="130" height="40" style="display:block;height:34px;width:auto;max-width:130px;aspect-ratio:auto;object-fit:contain;border-radius:0;box-shadow:none">' if marca else ""}<span>Centro de Servicio Técnico<small>{nom(marca) + " Panamá" if marca else "Panamá"}</small></span></a><a class="btn s" href="{wa("Hola, necesito servicio técnico en Panamá")}" target="_blank" rel="noopener">Pedir visita</a></div></header>'
         + chips(marca) + '<main id="contenido">' + heroh + bc + cuerpo + ('<div class="w"><p class="upd">Actualizado el ' + HOY_TXT + ' · Información orientativa; el diagnóstico final se confirma con pruebas en el equipo.</p></div>' if not re.search(r'/(politica-de-privacidad|terminos-y-condiciones)/', path) else '') + ('<!--cierre-->' + cierre(marca, path) + '<!--/cierre-->' if marca else '') + '</main>' + pie(marca, marcas_ok) + extra_js + '</body></html>')
    h = LOC(h)
    f = OUT / path.lstrip("/") / "index.html" if path != "/" else OUT / "index.html"
    f.parent.mkdir(parents=True, exist_ok=True); f.write_text(h, encoding="utf-8")
    TITULOS[path] = title
    if not noindex: paginas.append((path, prio, marca))

EXT = {  # enlaces externos por marca: sitio oficial (solo informativo) y ACODECO para derechos del consumidor
 "samsung": CFG["ext_samsung"],
 "lg": CFG["ext_lg"],
 "whirlpool": ("Página del fabricante: Whirlpool", "https://www.whirlpool.com/"),
 "mabe": ("Página del fabricante: Mabe", "https://www.mabe.com.mx/"),
 "frigidaire": ("Página del fabricante: Frigidaire", "https://www.frigidaire.com/"),
 "electrolux": ("Página del fabricante: Electrolux", "https://www.electrolux.com/"),
 "general-electric": ("Página del fabricante: GE Appliances", "https://www.geappliances.com/"),
 "haceb": ("Página del fabricante: Haceb", "https://www.haceb.com/"),
 "kitchenaid": ("Página del fabricante: KitchenAid", "https://www.kitchenaid.com/"),
 "sony": ("Página del fabricante: Sony", "https://www.sony.com/"),
 "tcl": ("Página del fabricante: TCL", "https://www.tcl.com/"),
 "hisense": ("Página del fabricante: Hisense", "https://global.hisense.com/"),
 "philips": ("Página del fabricante: Philips", "https://www.philips.com/"),
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
    guias = "".join(f'<a class="card l" href="{pathb(m, "guia-" + sl)}"><span class="t">{esc(t_)}</span></a>' for sl, t_ in ART.get(m, [])[:3]) + f'<a class="card l" href="{pathb(m, "guias")}"><span class="t">Todas las guías {N}</span></a><a class="card l" href="{pathb(m, "glosario")}"><span class="t">Glosario {N}</span></a><a class="card l" href="{pathb(m, "cobertura")}"><span class="t">Zonas donde atendemos {N}</span></a>'
    busq = [(f"servicio técnico {N} Panamá", base(m)), (f"teléfono servicio técnico {N} Panamá", pathb(m, "telefono-servicio-tecnico")), (f"centro de servicio {N} cerca de mí", pathb(m, "centro-de-servicio-cerca-de-mi")), (f"reparación {N} a domicilio", pathb(m, "reparacion-a-domicilio")), (f"repuestos {N} Panamá", pathb(m, "repuestos")), (f"códigos de error {N}", pathb(m, "codigos-de-error") if d["codigos"] else pathb(m, "fallas")), (f"mantenimiento {N}", pathb(m, "guia-de-cuidado")), (f"garantía {N} Panamá", pathb(m, "garantia"))]
    chips_b = "".join(f'<a class="pill" href="{u}">{esc(t)}</a>' for t, u in busq)
    nm, url = EXT[m]
    externos = f'<ul><li><a href="{url}" target="_blank" rel="noopener">{nm}</a> <small>(abre en otra pestaña; sitio del fabricante, no es nuestro)</small></li></ul>'
    return (sec(f"Búsquedas relacionadas con {N} en Panamá", chips_b)
            + sec(f"Más sobre {N} en Panamá", f'<div class="g c3">{inter}</div>', alt=True)
            + sec(f"Guías de {N}", f'<div class="g c3">{guias}</div>')
            + sec(f"Enlace externo: {N}", externos))
GEO_META = (f'<meta name="geo.region" content="{CFG["geo_region"]}"><meta name="geo.placename" content="{CFG["ciudad"]}">' if CFG.get("geo_region") else "")
def sec(t, body, alt=False, lead=None, id=None):
    return f'<section class="s{" alt" if alt else ""}"{f" id={chr(34)}{id}{chr(34)}" if id else ""}><div class="w"><h2>{t}</h2>' + (f'<p class="lead">{lead}</p>' if lead else "") + body + '</div></section>'
def rr(txt): return f'<div class="rr"><b>Respuesta rápida</b>{txt}</div>'
def tabla(cab, filas):
    return '<table class="tb"><thead><tr>' + "".join(f"<th>{c}</th>" for c in cab) + '</tr></thead><tbody>' + "".join('<tr>' + "".join(f'<td data-l="{cab[i]}">{c}</td>' for i, c in enumerate(f)) + '</tr>' for f in filas) + '</tbody></table>'
def faq_html(faqs): return "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faqs)
def faq_ld(faqs): return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
PASOS = ('<ol class="pasos"><li><b>Escríbenos</b>Cuéntanos marca, modelo y qué hace el equipo.</li><li><b>Coordinamos</b>Acordamos día y franja en tu zona.</li>'
         '<li><b>Diagnóstico en casa</b>' + ("Revisamos la pantalla en tu casa y, si hace falta taller, coordinamos el retiro con cuidado." if CFG.get("tv") else "Revisamos el equipo y te explicamos la causa.") + '</li><li><b>Reparación y prueba</b>Solo si tú apruebas el valor.</li></ol>')

def cap(t):
    return t[:1].upper() + t[1:]
def etq(t):
    t = bajar(t).rstrip(".")
    return t if re.match(r"(en|dentro|detrás|sobre|bajo|junto|al|arriba|abajo)\b", t) else "en " + t
def uni(sing, N, a):
    a2 = bajar(a).rstrip(".")
    return f"{sing} {N}: {a2}" if re.match(r"(el|la|los|las|un|una|unos|unas|ninguna|ningún|todas)\b", a2) else f"{sing} {N} {a2}"
def bajar(t):
    # no bajar a minúscula si empieza con un código/sigla (OE, F5E1, UE, Er FF...)
    return t if (len(t) > 1 and t[1].isupper()) or t[:2] in ("OE", "IE", "UE") or re.match(r"[A-Z]\d", t) or re.match(r"[A-Z]{1,3}[a-z]?\d", t) else t[0].lower() + t[1:]
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
    d = M[m]; items = [("guia-de-cuidado", f"Guía de cuidado {nom(m)}"), ("fallas", f"Fallas frecuentes de {nom(m)}"), ("cobertura", f"Cobertura {nom(m)} por zona"), ("series-y-modelos", f"Series y modelos {nom(m)}"), ("cuanto-cuesta-la-reparacion", "Cuánto cuesta y garantía"), ("preguntas-frecuentes", "Preguntas frecuentes"), ("diagnostico-por-sintoma", "Diagnóstico por síntoma")]
    if d["codigos"]: items.insert(0, ("codigos-de-error", f"Códigos de error {nom(m)}"))
    return '<div class="g c3">' + "".join(f'<a class="card l" href="{pathb(m, s)}"><span class="t">{t}</span></a>' for s, t in items if s != actual) + "</div>"


def stepper(n):
    t = ["Elige tu equipo", "Elige lo que le pasa", "Pide la visita"]
    return '<ol class="stp">' + "".join(f'<li{" class=on" if i + 1 == n else ""}>{x}</li>' for i, x in enumerate(t)) + '</ol>'
def foto_equipo(m, e):
    rx = re.compile(KW.get(e, "zzz")); g = re.compile(KW["_gente"])
    c = [f for f in POOLS[m] if rx.search(f.name) and not g.search(f.name)]
    if not c: return None
    c.sort(key=lambda f: (USO[f], f.name)); f = c[0]; USO[f] += 1
    return (copia(m, f), alt_de(m, f))
EJ = {"tv-led": "No enciende, sin imagen, líneas", "tv-qled": "Sombras, manchas, se apaga", "tv-oled": "Imagen marcada, bandas, no enciende", "neveras": "No enfría, hace ruido, gotea", "lavadoras": "No drena, no centrifuga, error", "secadoras": "No seca, no calienta", "aires": "No enfría, gotea, código", "cocinas": "No calienta, no enciende", "lavavajillas": "No drena, no lava bien", "centro-lavado": "Una unidad no responde", "batidoras": "Ruido, grasa, pierde fuerza", "microondas": "No calienta, hace chispas"}
def tiles(m):
    d = M[m]; N = nom(m); out = ""
    for e in d["equipos"]:
        f = None if CFG.get("tv") else foto_equipo(m, e)
        _ico = '<svg viewBox="0 0 120 90" width="140" height="105" role="img" aria-label="Pantalla"><rect x="6" y="6" width="108" height="64" rx="6" fill="none" stroke="var(--c)" stroke-width="5"/><rect x="14" y="14" width="92" height="48" rx="2" fill="var(--soft)"/><path d="M40 82h40M60 70v12" stroke="var(--c)" stroke-width="5" stroke-linecap="round"/></svg>'
        im = f'<img loading="lazy" src="{f[0]}" alt="{f[1]}" width="400" height="300">' if f else (_ico if CFG.get("tv") else EQ[e][2][:1].upper())
        out += f'<a class="tile" href="{pathb(m, "reparacion-" + EQ[e][0])}"><span class="ti-img">{im}</span><b>{EQ[e][2].capitalize()} {N}</b><small>{EJ[e]}</small><span class="go">Elegir →</span></a>'
    return f'<div class="tiles">{out}</div>'
def sintomas_btn(m, e, lista):
    return '<div class="symb">' + "".join(f'<a class="sy" href="{pathb(m, "falla-" + slug(EQ[e][1] + " " + a))}"><i>›</i><span><b>{esc(a)}</b><small>{esc(b[:88])}{"…" if len(b) > 88 else ""}</small></span></a>' for a, b, c in lista) + '</div>'
def caja_ayuda(m):
    N = nom(m)
    return ('<div class="cta-box"><div class="card"><b class="t">Diagnóstico por síntoma</b><p>Usa el diagnóstico por síntoma: eliges tu equipo y lo que notas, y te mostramos la causa más probable.</p>'
            f'<a class="btn s" href="{pathb(m, "diagnostico-por-sintoma")}">Abrir el diagnóstico</a></div>'
            f'<div class="card"><b class="t">Hablar con una persona</b><p>Escríbenos por WhatsApp con la marca, el modelo y la falla. Respondemos y coordinamos la visita.</p><a class="btn s" href="{wa("Hola, necesito servicio técnico " + N + " en Panamá")}" target="_blank" rel="noopener">Escribir por WhatsApp</a></div></div>')

# ---------------------------------------------------------------- Guayaquil: contenido adicional por marca
def faq10(m):
    """Exactamente 10 preguntas frecuentes por marca, con respuestas propias de la marca."""
    d = M[m]; N = nom(m); E = d["equipos"]; e0 = E[0]; e1 = E[1] if len(E) > 1 else E[0]; ciu = CFG["ciudad"]
    cand = list(d["faq"]) + [
        (f"¿Hacen servicio técnico {N} a domicilio en {ciu}?", f"Sí. Vamos a tu casa o apartamento en {CFG.get('zlista', ciu)} para diagnosticar y reparar tu equipo {N} sin que lo muevas."),
        (f"¿Qué necesito para pedir la visita de un técnico {N}?", f"Ten a mano el modelo del equipo, lo que notas o el código que aparece, y tu barrio. {d['modelo_ej']}"),
        (f"¿Reparan equipos {N} que ya no tienen garantía?", f"Sí. {d['garantia'].split('. ')[0]}. Si ya venció, revisamos el equipo, te explicamos la causa y el valor se confirma por escrito antes de empezar."),
        (f"¿Qué equipos {N} atienden?", f"Atendemos {pls_(d)}. Entre las fallas que más atendemos están «{bajar(d['fallas'][e0][0][0]).rstrip('.')}» en {EQ[e0][2]} y «{bajar(d['fallas'][E[-1]][0][0]).rstrip('.')}» en {EQ[E[-1]][2]}."),
        (f"¿Dónde encuentro el modelo de mi {EQ[e0][1]} {N}?", cap(d["etiqueta"].get(e0, "En una etiqueta pegada al equipo")).rstrip(".") + ". Con una foto de esa etiqueta, el diagnóstico por WhatsApp es mucho más preciso."),
        (f"¿Qué líneas de {N} atienden?", f"Atendemos líneas como {', '.join(d['lineas'][:5])}. Si tu modelo no aparece, escríbenos con la foto de la etiqueta y te confirmamos."),
        (f"¿Qué mantenimiento recomiendan para equipos {N}?", " ".join(x.rstrip(".") + "." for x in d["mantenimiento"][:2]) + " Un mantenimiento preventivo anual evita la mayoría de averías."),
        (f"¿Cuánto cuesta la reparación de un equipo {N}?", "Depende de la falla y de la pieza. Primero diagnosticamos y te damos el valor por escrito antes de reparar; solo reparamos si tú lo apruebas."),
        (f"¿Qué hago si mi {EQ[e1][1]} {N} presenta «{bajar(d['fallas'][e1][0][0]).rstrip('.')}»?", f"{d['fallas'][e1][0][1]} {d['fallas'][e1][0][2]} Escríbenos por WhatsApp y te orientamos."),
        (f"¿Cómo pido una visita para mi equipo {N} por WhatsApp?", f"Escribe al {TEL} con el equipo, el modelo y lo que notas. Coordinamos el día y la franja en tu zona."),
        (f"¿Puedo seguir usando mi {EQ[e0][1]} {N} si presenta una falla?", "Depende de la causa. Si hay olor a quemado, chispas, olor a gas o agua cerca de enchufes, deja de usarlo y llama. En los demás casos, prueba lo indicado en nuestras páginas de fallas y, si el problema vuelve, pide la revisión."),
    ]
    if d["codigos"]: cand.insert(5, (f"¿Qué significa un código de error en mi equipo {N}?", "Los códigos indican qué parte detectó la falla (sensor, drenaje, comunicación, etc.). Mira la página de códigos de error de tu marca y, si persiste, pide la visita para medir el componente."))
    vis, out = set(), []
    for q, a in cand:
        k = re.sub(r"\W+", "", q.lower())[:40]
        if k in vis: continue
        vis.add(k); out.append((q, a))
    return out[:10]

def por_que_elegirnos(m):
    d = M[m]; N = nom(m); E = d["equipos"]; e0 = E[0]; e1 = E[1] if len(E) > 1 else E[0]; bi = BRANDS_ORDER.index(m)
    items = [(f"Conocemos las líneas {N}", f"Trabajamos con {', '.join(d['lineas'][:3])} y otras líneas {N}, y sabemos qué piezas fallan más en cada una."),
             (f"Sabemos qué falla más en {N}", f"En {EQ[e0][2]} {N} lo más frecuente es {bajar(d['fallas'][e0][0][0]).rstrip('.')}; en {EQ[e1][2]}, {bajar(d['fallas'][e1][0][0]).rstrip('.')}."),
             (f"Identificamos tu modelo {N}", d["modelo_ej"].split(". ")[0].rstrip(".") + ". Con esa etiqueta confirmamos repuestos y procedimientos."),
             ("Valor por escrito antes de reparar", "Te explicamos la causa y el valor antes de empezar. Solo reparamos si tú lo apruebas."),
             ("Visita a domicilio", f"Vamos a tu casa en {CFG.get('zlista', CFG['ciudad'])}. No tienes que mover tu equipo."),
             ("Atención por WhatsApp", f"Escríbenos al {TEL} con el modelo y lo que notas, y coordinamos la visita.")]
    items = items[bi % 6:] + items[:bi % 6]
    return '<div class="why">' + "".join(f'<div class="card"><h3>{esc(t)}</h3><p>{esc(x)}</p></div>' for t, x in items) + "</div>"

def quienes_breve(m):
    N = nom(m)
    return (f'<p>Somos un servicio técnico independiente en {CFG["ciudad"]}, especializado en reparar y dar mantenimiento a equipos {N}: {pls_(M[m])}. '
            f'Nos enfocamos en explicar con claridad qué falla, dar el valor por escrito antes de reparar y probar el equipo contigo al terminar.</p>'
            f'<p><a href="{pathb(m, "quienes-somos")}">Conoce más sobre nosotros</a></p>')

def wa_por_equipo(m):
    d = M[m]; N = nom(m)
    return ('<div class="wab">' + "".join(f'<a href="{wa("Hola, necesito servicio técnico para mi " + EQ[e][1] + " " + N + " en Panamá")}" target="_blank" rel="noopener">WhatsApp: {esc(EQ[e][1])} {esc(N)}</a>' for e in d["equipos"])
            + f'<a href="{wa("Hola, necesito servicio técnico " + N + " en Panamá")}" target="_blank" rel="noopener">WhatsApp: otro equipo {esc(N)}</a></div>')

_GYE = None
def _gye():
    global _GYE
    if _GYE is None:
        from datos_equipos1 import REFRIGERADORAS, LAVADORAS, SECADORAS, COCINAS
        from datos_equipos2 import AIRES, LAVAVAJILLAS, MICROONDAS
        _GYE = {"neveras": REFRIGERADORAS, "lavadoras": LAVADORAS, "centro-lavado": LAVADORAS, "secadoras": SECADORAS, "cocinas": COCINAS, "aires": AIRES, "lavavajillas": LAVAVAJILLAS, "microondas": MICROONDAS}
    return _GYE
BATIDORA = dict(
    mant=dict(intro="Una batidora de pedestal bien cuidada dura muchos años. El mantenimiento se centra en la limpieza, la grasa de la caja de engranes y el estado de las escobillas del motor.",
              tabla=[("Limpiar el tazón, el batidor y los accesorios", "Después de cada uso", "Evita residuos y óxido."), ("Limpiar la cabeza y las rejillas sin mojarlas", "Cada semana", "La humedad en el motor causa fallas."),
                     ("Revisar la altura del batidor", "Cada 6 meses", "Si toca el fondo, desgasta el tazón y el batidor."), ("Revisar la grasa de la caja de engranes", "1 vez al año", "La grasa vieja o escasa produce ruido y pérdida de fuerza."),
                     ("Revisar escobillas del motor", "Cada 1 o 2 años según uso", "Escobillas gastadas hacen que la batidora pierda potencia.")],
              gye="En Guayaquil la humedad puede afectar el motor y las partes metálicas. Guarda la batidora seca y limpia, y evita lavar la cabeza con agua."),
    inst=None)
QUITO_MI = {
 "neveras": dict(mant_intro="El mantenimiento preventivo de una refrigeradora es sencillo y evita la mayoría de averías caras. En Quito el clima fresco ayuda al equipo, pero el polvo de los meses secos y los picos de voltaje de la temporada de lluvias afectan el condensador y la placa.",
                 mant_gye="En Quito conviene limpiar el condensador al terminar los meses secos, cuando más polvo se acumula, y revisar la protección de voltaje antes de la temporada de lluvias. El aire seco de altura reseca los empaques de las puertas, así que revísalos con regularidad.",
                 inst_gye="En edificios de Quito con ascensor pequeño o escaleras angostas, conviene medir antes. En casas antiguas del Centro Histórico, revisa que los tomacorrientes tengan conexión a tierra antes de conectar la refrigeradora, porque el equipo no debe trabajar sin ella."),
 "lavadoras": dict(mant_intro="El mantenimiento preventivo de la lavadora evita bombas tapadas, malos olores y averías. En Quito, donde se lava mucha ropa gruesa y se seca dentro de casa, conviene cuidar el filtro, el sello y el desagüe.",
                    mant_gye="En Quito la ropa de abrigo, las cobijas y la pelusa tapan el filtro de la bomba más rápido. Si el agua de tu zona deja sedimentos, limpia las mallas de las mangueras de entrada con más frecuencia.",
                    inst_gye="En departamentos de Quito es común que el desagüe de la lavadora comparta tubería con el lavamanos o el piso. Hay que revisar que la tubería tenga capacidad y ventilación, o la lavadora se quedará con agua o hará ruido de gorgoteo."),
 "secadoras": dict(mant_intro="Una secadora bien mantenida seca más rápido, gasta menos energía y evita riesgos de incendio por pelusa acumulada, que es la causa más seria de accidentes con secadoras. En Quito, con días frescos y lluviosos, es el equipo que más ayuda a secar la ropa, por eso se usa tanto.",
                    mant_gye="En Quito la ropa gruesa y las cobijas generan mucha pelusa: limpia el filtro después de cada ciclo y el ducto una vez al año. Si tu cuarto de lavado no tiene salida directa al exterior, revisa con más frecuencia el escape.",
                    inst_gye="En edificios de Quito es común que no exista salida de ducto: en ese caso conviene una secadora de condensación o de bomba de calor, o definir una salida segura al exterior antes de comprar."),
 "cocinas": dict(mant_intro="El mantenimiento de una cocina y un horno es sobre todo limpieza y seguridad: quemadores limpios, conexión de gas en buen estado y componentes eléctricos secos.",
                  mant_gye="En Quito, por la altura, la llama de los quemadores a gas necesita una mezcla de aire bien ajustada: si ves llama amarilla o con puntas rojas, pide revisar el quemador. Las cocinas de inducción, muy comunes en la ciudad, agradecen un protector de voltaje durante la temporada de lluvias.",
                  inst_gye="En edificios de Quito con gas centralizado o con cilindro en el balcón, la ruta de la manguera y la ventilación del cilindro son parte de la instalación segura. Para cocinas de inducción, verifica la capacidad del circuito: muchas requieren 220 V."),
 "aires": dict(mant_intro="El mantenimiento de un aire acondicionado incluye limpiar filtros, evaporador, condensador y drenaje, además de medir presiones. En Quito el clima fresco hace que el aire se use menos que en la costa, pero el mantenimiento anual igual evita olores, goteos y fallas por picos de voltaje.",
                mant_gye="En Quito el aire acondicionado se usa menos horas que en la costa, pero el polvo de los meses secos y las tormentas de la temporada de lluvias afectan filtros, unidad exterior y placa. Programa el mantenimiento antes de la temporada de uso más intenso y revisa la protección de voltaje.",
                inst_gye="En Quito conviene instalar con protección contra picos de voltaje y revisar que la estructura de la unidad exterior soporte el viento y la radiación solar. En fachadas de edificios, hay que respetar las normas de la administración y usar soportes resistentes a la corrosión."),
 "lavavajillas": dict(mant_gye="El agua de la ciudad puede dejar sarro con el tiempo. Si notas manchas blancas en vasos y platos, ajusta la sal regeneradora y el abrillantador y haz limpieza periódica.",
                       inst_gye="En departamentos de Quito, el espacio bajo el fregadero suele ser pequeño. Conviene planificar la salida del desagüe y la llave de paso antes de comprar."),
 "microondas": dict(mant_gye="Los picos de voltaje de la temporada de lluvias afectan la electrónica de los microondas, por eso es importante dejar espacio de ventilación y evitar enchufarlos junto a otros equipos de alto consumo."),
 "batidoras": dict(mant_gye="En Quito el aire seco de altura ayuda a conservar las partes metálicas, pero guarda la batidora limpia y seca y evita lavar la cabeza con agua."),
}
QUITO_MI["centro-lavado"] = QUITO_MI["lavadoras"]
def _gye_loc(t):
    """Adapta los textos de mantenimiento e instalación (escritos para Guayaquil) a la ciudad del sitio."""
    if CFG["sitio"] == "guayaquil" or CFG.get("tv"): return t
    mar = CFG.get("costero")
    for x, y in [("Si vives cerca del río o el estero, el aire con sal acelera la corrosión de los contactos", "Si vives cerca del mar, el aire con sal (salitre) acelera la corrosión de los contactos" if mar else "Si vives en una zona muy húmeda, la corrosión de los contactos avanza más rápido"),
                 ("si vives cerca del río o el estero, donde la sal del aire corroe más rápido", "si vives cerca del mar, donde la sal del aire corroe más rápido" if mar else "si vives en una zona muy húmeda, donde la corrosión avanza más rápido")]:
        t = t.replace(x, y)
    return t.replace("Guayaquil", CFG["ciudad"])
def bloque_mant_inst(m, e):
    """Secciones de mantenimiento e instalación de un equipo de una marca (solo Guayaquil)."""
    if not CFG.get("sin_recorte"): return ""
    d = M[m]; N = nom(m); sing = EQ[e][1]; pl = EQ[e][2]; bi = BRANDS_ORDER.index(m)
    if e.startswith("tv-"): g = _TV.MANT_INST[e]
    else: g = BATIDORA if e == "batidoras" else {"mant": _gye()[e]["mant"], "inst": _gye()[e]["inst"]}
    mt, ins = g["mant"], g["inst"]
    ov = QUITO_MI.get(e, {}) if CFG["sitio"] == "quito" else {}
    if CFG.get("tv"):
        mt = {**mt}; ins = {**ins} if ins else ins
    mt = {**mt, "intro": ov.get("mant_intro") or _gye_loc(mt["intro"]), "gye": ov.get("mant_gye") or _gye_loc(mt["gye"])}
    if ins: ins = {**ins, "intro": ov.get("inst_intro") or _gye_loc(ins["intro"]), "gye": ov.get("inst_gye") or _gye_loc(ins["gye"])}
    filas = _rot(mt["tabla"], bi, 5) if len(mt["tabla"]) > 4 else mt["tabla"]
    raiz = sing.split()[0][:5].lower()
    propios = [x for x in d["mantenimiento"] if raiz in x.lower()]
    tech = d["tech"][e].split(". ")[0].rstrip(".") + "."
    mant = (sec(f"Mantenimiento de {pl} {N} en {CFG['ciudad']}", f"<p>{esc(mt['intro'])}</p><p>{esc(tech)} {esc(mt['gye'])}</p>"
                + tabla(["Tarea", "Cada cuánto", "Por qué importa"], [(f"<b>{esc(a)}</b>", esc(b_), esc(c_)) for a, b_, c_ in filas])
                + ("<h3 style='margin-top:18px'>Recomendado por el fabricante para tu línea</h3><ul>" + "".join(f"<li>{esc(x)}</li>" for x in propios[:2]) + "</ul>" if propios else ""), id="mantenimiento"))
    inst = ""
    if ins:
        antes = _rot(ins["antes"], bi, 3)
        inst = sec(f"Instalación de {pl} {N} en {CFG['ciudad']}", f"<p>{esc(ins['intro'])}</p><p>{esc(ins['gye'])}</p><h3>Antes de instalar tu {esc(sing)} {esc(N)}</h3><ul>" + "".join(f"<li>{esc(x)}</li>" for x in antes)
                   + f"<li>Ten a mano el modelo: {esc(d['etiqueta'].get(e, 'está en una etiqueta pegada al equipo').rstrip('.'))}.</li></ul><h3>Paso a paso</h3><ol>" + "".join(f"<li>{esc(x)}</li>" for x in ins["pasos"]) + "</ol>", alt=True, id="instalacion")
    return mant + inst

def fotos_eq(m, e, usadas):
    """Fotos completas (sin recortar) del tipo de equipo, de esa marca, que aún no se usaron en la página."""
    rx = re.compile(KW.get(e, "zzzz")); out = []
    for f in POOLS[m]:
        if rx.search(f.name) and copia(m, f) not in usadas: out.append(f)
    out = sorted(out, key=lambda f: USO[f])[:3]
    if len(out) < 2: return ""
    figs = ""
    for f in out:
        USO[f] += 1; r = copia(m, f); usadas.add(r)
        w, h = _dim(f)
        figs += f'<figure><img loading="lazy" src="{r}" alt="{alt_de(m, f)}" width="{w}" height="{h}"></figure>'
    return f'<section class="s alt"><div class="w"><div class="fgrid">{figs}</div></div></section>'
_DIM = {}
def _dim(f):
    if f not in _DIM:
        from PIL import Image
        with Image.open(f) as im: _DIM[f] = im.size
    return _DIM[f]

def build_galeria(m):
    if not CFG.get("sin_recorte"): return
    N = nom(m); crumbs0 = [(f"Centro de Servicio Técnico {N} Panamá", base(m))]
    rg = re.compile(KW["_gente"])
    prod = [f for f in POOLS[m] if not rg.search(f.name)]; gente = [f for f in POOLS[m] if rg.search(f.name)]
    def figs(lst):
        o = ""
        for f in lst:
            USO[f] += 1; r = copia(m, f); w, h = _dim(f)
            o += f'<figure class="gf"><img loading="lazy" src="{r}" alt="{alt_de(m, f)}" width="{w}" height="{h}"></figure>'
        return '<div class="fgrid">' + o + "</div>"
    cuerpo = (sec(f"Equipos {N} que reparamos en Panamá", figs(prod))
              + sec(f"Servicio técnico {N} a domicilio", figs(gente), alt=True)
              + sec(f"¿Tienes un equipo {N} con falla?", f'<p><a class="btn" href="{wa("Hola, necesito servicio técnico " + N + " en Panamá")}" target="_blank" rel="noopener">Escribir por WhatsApp</a></p>'))
    pagina(pathb(m, "galeria"), f"Galería de fotos {N} en Panamá | Equipos y servicio", f"Galería de fotos de equipos {N} y del servicio técnico a domicilio en Panamá: refrigeradoras, lavadoras, secadoras, cocinas, aires y más, mostrados completos.",
           f"Galería de fotos {N}", cuerpo, m, None, crumbs0 + [("Galería", pathb(m, "galeria"))], bd=f"{N} · Galería", prio="0.5", lead=f"Equipos {N} y servicio técnico a domicilio.")

def build_tv_extra(m):
    """Páginas propias de pantallas: una por cada línea de la marca, más instalación y mantenimiento de pantallas {marca}."""
    d = M[m]; N = nom(m); crumbs0 = [(f"Centro de Servicio Técnico {N} Panamá", base(m))]; ciu = CFG["ciudad"]
    lineas_url = {}
    for ln, (tipo, desc, nota) in _TV.LINEAS_DET[m].items():
        sl = "pantallas-" + slug(N + " " + ln); lineas_url[ln] = pathb(m, sl)
        fl = d["fallas"][tipo][:4]
        lista = "".join(f'<li><a href="{pathb(m, "falla-" + slug(EQ[tipo][1] + " " + f[0]))}"><b>{esc(cap(f[0].strip().rstrip(".")))}</b></a>: {esc(bajar(f[1]))} <i>Qué revisamos:</i> {esc(bajar(f[2]))}</li>' for f in fl)
        faq = [(f"¿Reparan pantallas {N} {ln} en {ciu}?", f"Sí. Revisamos fuente de poder, placa principal, retroiluminación o panel según el tipo de pantalla, y te damos el valor por escrito antes de reparar."),
               (f"¿Qué suele fallar en una {N} {ln}?", f"{nota} Las demás fallas frecuentes de este tipo de pantalla están en la lista de arriba."),
               (f"¿Cómo sé qué modelo de {N} {ln} tengo?", f"{cap(d['etiqueta'].get(tipo, 'En la etiqueta trasera.').rstrip('.'))}. {d['modelo_ej']}")]
        cuerpo = (sec(f"Qué es una pantalla {N} {ln}", f"<p>{esc(desc)}</p><p><b>Tipo de pantalla:</b> {esc(EQ[tipo][2])}. {esc(d['tech'][tipo])}</p><p>{esc(nota)}</p>")
                  + sec(f"Fallas frecuentes en pantallas {N} {ln}", f"<ul>{lista}</ul><p><a href=\"{pathb(m, 'reparacion-' + EQ[tipo][0])}\">Ver toda la reparación de {EQ[tipo][2]} {N}</a></p>", alt=True)
                  + sec(f"Cómo identificar tu modelo {ln}", f"<p>{esc(d['modelo_ej'])}</p><p><b>Dónde está la etiqueta:</b> {esc(d['etiqueta'].get(tipo, 'En la etiqueta trasera.'))}</p><p>Con una foto de esa etiqueta y de lo que notas, el diagnóstico por WhatsApp es mucho más preciso.</p>")
                  + sec(f"Servicios para tu pantalla {N} {ln}", f'<div class="g c3"><a class="card l" href="{pathb(m, "reparacion-" + EQ[tipo][0])}"><span class="t">Reparación</span>Fallas, causas y qué revisamos.</a><a class="card l" href="{pathb(m, "instalacion-de-pantallas")}"><span class="t">Instalación</span>Montaje en pared o mueble y configuración.</a><a class="card l" href="{pathb(m, "mantenimiento-de-pantallas")}"><span class="t">Mantenimiento</span>Cuidados que alargan la vida de tu pantalla.</a></div>', alt=True)
                  + sec(f"Preguntas sobre las pantallas {N} {ln}", faq_html(faq))
                  + sec(f"Otras líneas {N}", "".join(f'<a class="pill" href="{pathb(m, "pantallas-" + slug(N + " " + x))}">{esc(x)}</a>' for x in _TV.LINEAS_DET[m] if x != ln) + f'<p><a href="{pathb(m, "series-y-modelos")}">Ver series y modelos {N}</a> · <a href="{pathb(m, "fallas")}">Fallas frecuentes</a></p>', alt=True))
        pagina(pathb(m, sl), f"Reparación de pantallas {N} {ln} en {ciu}", f"Reparación de pantallas {N} {ln} en {ciu}: fallas frecuentes, qué revisamos, cómo identificar tu modelo y cómo pedir la visita a domicilio.",
               f"Reparación de pantallas {N} {ln}", cuerpo, m, (elegir(m, m + sl, 1) or [None])[0], crumbs0 + [(f"{N} {ln}", pathb(m, sl))],
               [faq_ld(faq), {"@type": "Service", "name": f"Reparación de pantallas {N} {ln}", "provider": {"@id": DOM + "/#negocio"}, "areaServed": {"@type": "Country", "name": ciu}, "brand": {"@type": "Brand", "name": N}}],
               bd=f"{N} · {ln}", prio="0.8", lead=f"Fallas, modelos y servicio a domicilio para tu pantalla {N} {ln}.")
    _LINEAS_URL[m] = lineas_url
    ex = _TV.SERV_MARCA[m]; E = d["equipos"]
    # ---- instalación
    antes = _TV._INST_COMUN["antes"]
    cuerpo = (sec(f"Instalación de pantallas {N} en {ciu}", f"<p>Instalamos pantallas {N} ({', '.join(d['lineas'][:4])} y más) en tu casa u oficina en {ciu}: montaje en pared o sobre mueble, conexión de cables, sintonización de canales y configuración de imagen y sonido.</p><p>{esc(_TV.MANT_INST[E[0]]['inst']['gye'])}</p>")
              + sec("Tipos de soporte", "<dl class=\"pz\">" + "".join(f"<dt>{esc(a_)}</dt><dd>{esc(b_)}</dd>" for a_, b_ in _TV.SOPORTES) + "</dl><p>El soporte correcto depende del tamaño y del peso de la pantalla y del patrón de agujeros de la parte trasera (VESA), que cambia según el modelo; por ejemplo 200×200, 300×300, 400×400 o 600×400 mm.</p>", alt=True)
              + sec(f"Qué necesitamos saber de tu {N}", "<ul><li>El modelo exacto y el tamaño en pulgadas.</li><li>Si va en pared (de concreto, de bloque o de gypsum) o sobre un mueble.</li><li>A qué altura quieres el centro de la pantalla.</li><li>Qué dispositivos conectarás: decodificador, consola, barra de sonido o computadora.</li></ul>")
              + sec(f"Qué debes tener listo antes de instalar tu {N}", "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in antes) + "</ul>", alt=True)
              + sec(f"Particularidades de las pantallas {N}", "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in ex["inst"]) + "</ul>")
              + sec("Paso a paso de la instalación", "<ol>" + "".join(f"<li>{esc(x)}</li>" for x in _TV._INST_COMUN["pasos"]) + "</ol>", alt=True)
              + sec("Errores comunes que evitamos", "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in _TV._INST_COMUN["errores"]) + "</ul>")
              + sec("Preguntas sobre la instalación", faq_html([(f"¿Instalan pantallas {N} en pared de gypsum?", "Sí, pero el soporte debe anclarse a la estructura firme y no solo al panel de yeso. Lo verificamos antes de colgar la pantalla."),
                                                                (f"¿Qué soporte necesita mi pantalla {N}?", "Depende del tamaño, el peso y el patrón VESA de tu modelo. Mándanos el modelo por WhatsApp y te indicamos cuál usar."),
                                                                (f"¿Pueden dejar los cables de mi {N} ocultos?", "Sí, cuando la pared y la obra lo permiten. Se define antes de instalar, porque cambia la ruta del cable."),
                                                                (f"¿Sintonizan los canales de mi pantalla {N}?", "Sí. En Costa Rica la televisión digital usa ISDB-Tb; configuramos la región y buscamos los canales con la antena o el decodificador que uses.")]), alt=True))
    pagina(pathb(m, "instalacion-de-pantallas"), f"Instalación de pantallas {N} en {ciu} | Soporte de pared", f"Instalación de pantallas {N} en {ciu}: soporte de pared o mueble, cableado, sintonización de canales y configuración de imagen y sonido a domicilio.",
           f"Instalación de pantallas {N} en {ciu}", cuerpo, m, (elegir(m, m + "inst", 1) or [None])[0], crumbs0 + [("Instalación de pantallas", pathb(m, "instalacion-de-pantallas"))],
           [{"@type": "Service", "name": f"Instalación de pantallas {N}", "provider": {"@id": DOM + "/#negocio"}, "areaServed": {"@type": "Country", "name": ciu}, "brand": {"@type": "Brand", "name": N}}],
           bd=f"{N} · Instalación", prio="0.8", lead=f"Montaje, cableado y configuración de tu pantalla {N} en {ciu}.")
    # ---- mantenimiento
    _prop = ex["mant"]; _ext = [r for r in _TV._MANT_COMUN if not (r[0].startswith("Actualizar") and any(x[0].startswith("Actualizar") for x in _prop)) and not (("HDMI" in r[0] or "cables" in r[0]) and any(("HDMI" in x[0] or "cables" in x[0]) for x in _prop))]
    filas = [(f"<b>{esc(a_)}</b>", esc(b_), esc(c_)) for a_, b_, c_ in (_prop + _ext)]
    cuerpo = (sec(f"Mantenimiento de pantallas {N} en {ciu}", f"<p>Una pantalla {N} bien cuidada dura muchos años. El mantenimiento se reduce a limpiarla bien, dejarla respirar, protegerla de los picos de voltaje y mantener actualizado su sistema.</p><p>{esc(_TV.MANT_INST[E[0]]['mant']['gye'])}</p>")
              + sec("Plan de mantenimiento recomendado", tabla(["Tarea", "Cada cuánto", "Por qué importa"], filas), alt=True)
              + sec("Cómo limpiar la pantalla paso a paso", "<ol>" + "".join(f"<li>{esc(x)}</li>" for x in _TV.LIMPIEZA) + "</ol>")
              + sec(f"Qué no hacer con tu pantalla {N}", "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in _TV.NO_HACER) + "</ul>", alt=True)
              + sec("Señales de que necesita revisión", "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in _TV.MANT_INST[E[0]]["mant"]["senales"] + _TV.MANT_INST[E[-1]]["mant"]["senales"][:2]) + "</ul><p>Si notas alguna, no esperes a que falle del todo: pide la revisión.</p>")
              + sec("Preguntas sobre el mantenimiento", faq_html([(f"¿Cada cuánto debo limpiar mi pantalla {N}?", "La superficie, cada semana con microfibra seca. La ventilación y los cables, cada seis meses."),
                                                                  (f"¿Es necesario actualizar el sistema de mi {N}?", "Sí. Las actualizaciones corrigen fallas de Wi-Fi, aplicaciones y reinicios, y conviene instalarlas cuando la pantalla las indique."),
                                                                  (f"¿Sirve un protector de voltaje para mi pantalla {N}?", "Sí. Los picos de voltaje de las tormentas dañan la fuente de poder y la placa principal; un protector con retardo de reconexión es la medida más económica."),
                                                                  (f"¿Hacen mantenimiento aunque mi {N} funcione bien?", "Sí. Revisamos ventilación, cables, puertos y software, y te decimos si algo empieza a fallar antes de que deje de funcionar.")]), alt=True))
    pagina(pathb(m, "mantenimiento-de-pantallas"), f"Mantenimiento de pantallas {N} en {ciu} | Cuidados", f"Mantenimiento de pantallas {N} en {ciu}: plan, limpieza correcta, qué no hacer y señales de que tu pantalla necesita revisión.",
           f"Mantenimiento de pantallas {N} en {ciu}", cuerpo, m, (elegir(m, m + "mant", 1) or [None])[0], crumbs0 + [("Mantenimiento de pantallas", pathb(m, "mantenimiento-de-pantallas"))],
           [{"@type": "Service", "name": f"Mantenimiento de pantallas {N}", "provider": {"@id": DOM + "/#negocio"}, "areaServed": {"@type": "Country", "name": ciu}, "brand": {"@type": "Brand", "name": N}}],
           bd=f"{N} · Mantenimiento", prio="0.8", lead=f"Cuida tu pantalla {N}: limpieza correcta, ventilación y protección contra picos de voltaje.")
_LINEAS_URL = {}

def build_marca(m):
    d = M[m]; N = nom(m); crumbs0 = [(f"Centro de Servicio Técnico {N} Panamá", base(m))]
    # --- hub
    hero = elegir(m, m + "hub", 1)
    teaser = "".join(f'<tr><td data-l="Equipo">{EQ[e][2].capitalize()}</td><td data-l="Falla frecuente">{esc(d["fallas"][e][0][0])}</td><td data-l="Causa probable">{esc(d["fallas"][e][0][1])}</td></tr>' for e in d["equipos"])
    mid = elegir(m, m + "hubmid", 1, d["equipos"][0])
    top8 = [(e, f) for e in d["equipos"] for f in d["fallas"][e][:2]][:8]
    FAQ_H = list(d["faq"]) + [
        (f"¿Qué necesito para pedir la visita de un técnico {N}?", f"Ten a mano el modelo del equipo, lo que notas o el código que aparece, y tu barrio. {d['modelo_ej']}"),
        (f"¿Reparan equipos {N} que ya no tienen garantía?", f"Sí. {d['garantia'].split('. ')[0]}. Si ya venció, revisamos el equipo, te explicamos la causa y el valor se confirma por escrito antes de empezar."),
        (f"¿Qué equipos {N} atienden?", f"Atendemos {pls_(d)}. Lo que más vemos: {bajar(d['fallas'][d['equipos'][0]][0][0]).rstrip('.')} en {EQ[d['equipos'][0]][2]} y {bajar(d['fallas'][d['equipos'][-1]][0][0]).rstrip('.')} en {EQ[d['equipos'][-1]][2]}.")]
    if CFG.get("sin_recorte"): FAQ_H = faq10(m)
    sbtn = '<div class="symb">' + "".join(f'<a class="sy" href="{pathb(m, "falla-" + slug(EQ[e][1] + " " + f[0]))}"><i>›</i><span><b>{esc(EQ[e][1].capitalize())} {N}: {esc(bajar(f[0]).rstrip("."))}</b><small>{esc(f[1][:80])}{"…" if len(f[1]) > 80 else ""}</small></span></a>' for e, f in top8) + '</div>'
    cuerpo = (sec(f"¿Qué equipo {N} quieres reparar?", stepper(1) + tiles(m), id="equipos", lead="Toca el equipo que tienes con falla. Te llevamos a sus fallas y a cómo pedir la visita.")
              + sec("¿Necesitas ayuda para elegir?", caja_ayuda(m), alt=True)
              + sec(f"Las fallas más buscadas de {N}", sbtn + f'<p style="margin-top:14px"><a href="{pathb(m, "fallas")}">Ver todas las fallas de {N}</a></p>')
              + sec("Así funciona la visita", PASOS, alt=True)
              + (sec(f"¿Por qué elegirnos para tu equipo {N}?", por_que_elegirnos(m)) if CFG.get("sin_recorte") else "")
              + (sec(f"WhatsApp de servicio técnico {N}", "<p>Elige tu equipo y te abrimos WhatsApp con el mensaje listo para enviar.</p>" + wa_por_equipo(m), alt=True) if CFG.get("sin_recorte") else "")
              + sec(f"Preguntas frecuentes sobre {N}", faq_html(FAQ_H))
              + sec(f"Zonas de {CFG['ciudad']} donde atendemos equipos {N}", '<div class="g c3">' + "".join(f'<a class="card l" href="{pathb(m, "servicio-tecnico-" + z)}"><span class="t">Servicio técnico {N} en {esc(CFG.get("zart", {}).get(z, v[0]))}</span></a>' for z, v in ZONAS.items()) + '</div>', alt=True)
              + (sec(f"Quiénes somos", quienes_breve(m), alt=True) if CFG.get("sin_recorte") else "")
              + sec(f"Más información sobre {N}", otras(m, ""))
              + sec(f"Sobre los equipos {N}", f"<p>{esc(d['origen'])}</p><p><b>Líneas que atendemos:</b></p>" + "".join((f'<a class="pill" href="{pathb(m, "pantallas-" + slug(N + " " + x))}">{esc(x)}</a>' if CFG.get("tv") else f'<span class="pill">{esc(x)}</span>') for x in d["lineas"]) + "<h3 style='margin-top:18px'>Mantenimiento recomendado</h3><ul>" + "".join(f"<li>{esc(x)}</li>" for x in d["mantenimiento"]) + "</ul>"))
    path = "/" if m == "samsung" else base(m)
    t = f"Centro de Servicio Técnico {N} Panamá | A domicilio" if m != "general-electric" else f"Centro de Servicio Técnico {N} Panamá"
    ld = [faq_ld(FAQ_H), {"@type": "Service", "name": f"Servicio técnico {N} en Panamá", "provider": {"@id": DOM + "/#negocio"}, "areaServed": "Panamá", "serviceType": (f"Reparación de pantallas {N}" if CFG.get("tv") else f"Reparación de electrodomésticos {N}"), "brand": {"@type": "Brand", "name": N, "sameAs": EXT[m][1]},
          "hasOfferCatalog": {"@type": "OfferCatalog", "name": f"Servicios para equipos {N}", "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": f"Reparación de {EQ[e][2]} {N}", "url": DOM + pathb(m, "reparacion-" + EQ[e][0])}} for e in d["equipos"]]
              + ([{"@type": "Offer", "itemOffered": {"@type": "Service", "name": f"Mantenimiento de {EQ[e][2]} {N}", "url": DOM + pathb(m, "reparacion-" + EQ[e][0]) + "#mantenimiento"}} for e in d["equipos"]]
                 + [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": f"Instalación de {EQ[e][2]} {N}", "url": DOM + pathb(m, "reparacion-" + EQ[e][0]) + "#instalacion"}} for e in d["equipos"] if e != "batidoras"] if CFG.get("sin_recorte") else [])}}]
    pagina(path, t, f"Centro de servicio técnico {N} en Panamá: reparación a domicilio de {', '.join(EQ[e][2] for e in d['equipos'][:3])} y más. Diagnóstico en casa y atención por WhatsApp.",
           f"Centro de Servicio Técnico {N} Panamá", cuerpo, m, hero[0] if hero else None, [(f"Centro de Servicio Técnico {N} Panamá", base(m))], ld,
           bd=f"{N} · Panamá", prio="1.0" if m == "samsung" else "0.9",
           lead=f"Reparamos tus equipos {N} en tu casa. Elige tu equipo abajo y te guiamos paso a paso.", cta2=("Elegir mi equipo ↓", "#equipos"))
    # --- por equipo
    for e in d["equipos"]:
        s, sing, pl = EQ[e]; fl = d["fallas"][e]
        imgs = elegir(m, m + e, 1, e)
        h = imgs[0] if imgs else None
        gente = elegir(m, m + e + "gente", 1)
        h2 = gente[0] if gente else None
        cod = d["codigos"].get("Lavadoras" if e in ("lavadoras", "centro-lavado") else "Refrigeradoras" if e == "neveras" else "_", [])
        sec_cod = sec(f"Códigos de error frecuentes en {pl} {N}", tabla(["Código", "Qué suele indicar"], [(f'<span class="cb">{c}</span>', esc(t)) for c, t in cod]) + f'<p><a href="{pathb(m, "codigos-de-error")}">Ver todos los códigos {N}</a></p>', id="codigos", alt=True, lead=f"Si la pantalla de tu {sing} {N} muestra un código, aquí está lo que suele indicar.") if cod else ""
        raiz = sing.split()[0][:5].lower()
        cuid = [x for x in d["mantenimiento"] if raiz in x.lower()]
        cuid_html = ("<h3>Cuidados que alargan su vida</h3><ul>" + "".join(f"<li>{esc(x)}</li>" for x in cuid[:3]) + "</ul>") if cuid else ""
        anc = f'<div class="anc"><a href="#fallas">Elegir mi falla</a>' + ('<a href="#codigos">Códigos de error</a>' if cod else "") + f'<a href="#funciona">Cómo funciona</a><a href="#reparar-o-cambiar">¿Reparar o cambiar?</a><a href="#visita">Antes de la visita</a><a href="#preguntas">Preguntas</a><a href="{wa("Hola, necesito reparar mi " + sing + " " + N)}" target="_blank" rel="noopener">Pedir visita</a></div>'
        modelo_txt = d["etiqueta"].get(e, "Busca la etiqueta con el número de modelo y serie en el equipo.")
        faq_e = [(f"¿Dónde encuentro el modelo de mi {sing} {N}?", modelo_txt + " Con una foto de esa etiqueta el diagnóstico por WhatsApp es mucho más preciso."),
                 (f"¿Cuál es la falla más común en {pl} {N}?", f"{cap(bajar(fl[0][0]).rstrip('.'))}. Lo más probable: {bajar(fl[0][1])}"),
                 (f"¿Qué hago si mi {sing} {N} presenta «{bajar(fl[-1][0]).rstrip('.')}»?", f"{fl[-1][1]} {fl[-1][2]}")] + [(q, r) for q, r in d["faq"] if re.search(sing.split()[0][:6], q + r, re.I)][:1]
        visita = (f'<div class="two"><div><h3>Ten a mano el modelo</h3><p>{esc(modelo_txt)}</p><p>Con una foto de esa etiqueta y de lo que muestra el equipo, el diagnóstico por WhatsApp es mucho más preciso.</p>'
                  f'<h3 style="margin-top:14px">Qué pasa en la visita</h3><ol><li>Revisamos tu {sing} {N} en casa.</li><li>Te explicamos la causa y el valor por escrito.</li><li>Solo reparamos si tú lo apruebas.</li></ol>'
                  f'<p><a class="btn" href="{wa("Hola, necesito reparar mi " + sing + " " + N)}" target="_blank" rel="noopener">Pedir la visita</a></p></div>'
                  + (f'<img loading="lazy" src="{h2[0]}" alt="{h2[1]}" width="1024" height="768">' if h2 else "") + '</div>')
        vd = EQ_VIDA.get(e)
        rc = sec(f"¿Reparar o cambiar tu {sing} {N}?", f"<p>Una {sing} dura en promedio <b>{vd[0]}</b> si se cuida bien. Antes de decidir, revisamos el equipo y te damos el valor por escrito; tú eliges.</p><div class=\"two\" style=\"align-items:start\"><div><h3>Casi siempre conviene reparar si…</h3><ul>" + "".join(f"<li>{esc(x)}</li>" for x in vd[2]) + "</ul></div><div><h3>Conviene evaluar el cambio si…</h3><ul>" + "".join(f"<li>{esc(x)}</li>" for x in vd[1]) + "</ul></div></div>", id="reparar-o-cambiar", alt=True) if vd else ""
        cuerpo = (sec(f"¿Qué le pasa a tu {sing} {N}?", anc + stepper(2) + sintomas_btn(m, e, fl), id="fallas", lead="Toca lo que notas en tu equipo. Te mostramos la causa más probable y qué puedes hacer antes de llamar.")
                  + sec_cod
                  + sec(f"Cómo funciona tu {sing} {N}", f"<p>{esc(d['tech'][e])}</p>" + cuid_html, id="funciona", alt=not bool(sec_cod))
                  + rc
                  + sec(f"Antes de la visita: tu {sing} {N}", visita, id="visita", alt=not bool(rc))
                  + bloque_mant_inst(m, e)
                  + (fotos_eq(m, e, {x[0] for x in (h, h2) if x}) if CFG.get("sin_recorte") else "")
                  + sec(f"Preguntas sobre {pl} {N}", faq_html(faq_e), alt=not bool(sec_cod), id="preguntas")
                  + f"<!--REL:{e}-->")
        pagina(pathb(m, "reparacion-" + s), f"Reparación de {pl} {N} en Panamá | Centro de Servicio", f"Reparación de {pl} {N} en Panamá a domicilio: fallas frecuentes, causas probables y qué revisamos. Diagnóstico en casa y atención por WhatsApp.",
               f"Reparación de {pl} {N} en Panamá", cuerpo, m, h, crumbs0 + [(f"Reparación de {pl}", pathb(m, "reparacion-" + s))],
               [faq_ld(faq_e), {"@type": "Service", "name": f"Reparación de {pl} {N}", "provider": {"@id": DOM + "/#negocio"}, "areaServed": "Panamá"}], bd=f"{N} · {pl.capitalize()}", prio="0.8",
               lead=f"Qué le pasa a tu {sing} {N}, por qué ocurre y cómo lo revisamos en tu casa en Panamá.")
    # --- códigos
    if d["codigos"]:
        bloques = "".join(f'<h3>{g}</h3>' + tabla(["Código", "Qué significa", "Qué hacer"], [(f'<span class="cb">{c}</span>', esc(t), esc(accion_cod(t))) for c, t in L]) for g, L in d["codigos"].items())
        pagina(pathb(m, "codigos-de-error"), f"Códigos de error {N}: qué significan | Panamá", f"Lista de códigos de error {N} más comunes en lavadoras y refrigeradoras, con qué suele indicar cada uno y cuándo llamar al técnico.",
               f"Códigos de error {N}: qué significa cada uno", sec(f"Códigos de error {N}", rr(f"Los códigos de error {N} indican qué sistema del equipo detectó el problema. Muchos se resuelven limpiando filtros o revisando llaves; si el código vuelve tras apagar y encender, hace falta una revisión.") + bloques + "<p><small>Esta lista es orientativa. El significado exacto puede variar según el modelo y el año; confirma siempre con el manual de tu equipo.</small></p>") + sec("Equipos", eq_links(m), alt=True),
               m, (elegir(m, m + "cod", 1) or [None])[0] if POOLS[m] else None, crumbs0 + [("Códigos de error", pathb(m, "codigos-de-error"))], bd=f"{N} · Códigos", prio="0.8",
               lead=f"Qué significan los códigos de error más frecuentes de {N} y qué hacer antes de llamar.")
    # --- series y modelos
    tb = "".join(f"<h3>{EQ[e][2].capitalize()} {N}</h3><p>{esc(d['tech'][e])}</p>" for e in d["equipos"])
    et = tabla(["Equipo", "Dónde está la etiqueta con el modelo"], [(EQ[e][2].capitalize(), esc(t)) for e, t in d["etiqueta"].items()])
    pagina(pathb(m, "series-y-modelos"), f"Series y modelos {N}: cómo identificar el tuyo", f"Líneas {N} más comunes en Panamá, cómo funciona cada tecnología y dónde encontrar el número de modelo de tu equipo.",
           f"Series, modelos y tecnologías {N}", sec(f"Líneas {N}", rr(f"{N} agrupa sus equipos en líneas como {', '.join(d['lineas'][:4])}. Conocer la tuya ayuda a pedir el repuesto correcto y a describir la falla con precisión.") + "".join(f'<span class="pill">{esc(x)}</span>' for x in d["lineas"]) + f"<p>{esc(d['modelo_ej'])}</p>") + sec("Cómo funciona cada equipo", tb, alt=True) + sec("Dónde encontrar el número de modelo", et + "<p>Con una foto de esa etiqueta puedes escribirnos por WhatsApp y adelantamos el diagnóstico.</p>"),
           m, (elegir(m, m + "ser", 1) or [None])[0], crumbs0 + [("Series y modelos", pathb(m, "series-y-modelos"))], bd=f"{N} · Modelos", lead=f"Origen, líneas y tecnologías de {N}, y cómo leer la etiqueta del equipo.")
    comp = {"samsung": "el compresor Digital Inverter y la placa inverter", "lg": "el compresor inverter o lineal y la placa inverter", "whirlpool": "el compresor, el control y la transmisión de la lavadora", "mabe": "el compresor y la transmisión de la lavadora", "frigidaire": "la tarjeta de control y el compresor", "electrolux": "la placa inverter y el compresor", "general-electric": "la tarjeta de control y el sistema del dispensador", "haceb": "el compresor y la tarjeta", "kitchenaid": "el motor y la caja de engranes"}.get(m, "la fuente de poder, la placa principal y la retroiluminación")
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
    grp = ""
    for e in d["equipos"]:
        niv = {"Bajo": [], "Medio": [], "Alto": []}
        for a_, b_, c_ in d["fallas"][e]: niv[nivel(b_)].append(cap(bajar(a_).rstrip(".")))
        li = ""
        if niv["Bajo"]: li += "<li><b>Más económicas:</b> " + "; ".join(esc(x) for x in niv["Bajo"]) + ".</li>"
        if niv["Medio"]: li += "<li><b>Costo intermedio:</b> " + "; ".join(esc(x) for x in niv["Medio"]) + ".</li>"
        if niv["Alto"]: li += "<li><b>Las que más pesan:</b> " + "; ".join(esc(x) for x in niv["Alto"]) + ".</li>"
        grp += f"<h3>{EQ[e][2].capitalize()} {N}</h3><ul>{li}</ul>"
    pagina(pathb(m, "cuanto-cuesta-la-reparacion"), f"Cuánto cuesta reparar equipos {N} en Panamá", f"Qué fallas de cada equipo {N} suelen costar poco y cuáles más, y cómo se confirma el valor antes de reparar en Panamá.",
           f"Cuánto cuesta reparar equipos {N} en Panamá",
           sec(f"Qué fallas de {N} cuestan más o menos, equipo por equipo", f"<p>El valor depende de la pieza que falló. Esta es la guía comparativa para equipos {N}; no son precios, el valor real se confirma después del diagnóstico y antes de reparar.</p>" + grp)
           + sec(f"Qué decide el precio de reparar {ART_EQ[d['equipos'][0]]} {EQ[d['equipos'][0]][1]} {N}", f"<p>{esc(d['tech'][d['equipos'][0]])}</p><p>Si el repuesto está disponible en {CFG['pais']} o hay que pedirlo a {d['pais']}, el plazo y el valor cambian. En equipos con muchos años se compara reparar con reemplazar.</p>", alt=True),
           m, (elegir(m, m + "cost", 1) or [None])[0], crumbs0 + [("Cuánto cuesta", pathb(m, "cuanto-cuesta-la-reparacion"))], bd=f"{N} · Costos", lead=f"De qué depende el costo de reparar cada equipo {N}.")
    # --- preguntas
    PF = (faq10(m) if CFG.get("sin_recorte") else list(d["faq"])) + [(f"¿Qué pasa si {ART_EQ[e]} {EQ[e][1]} {N} presenta «{f[0].rstrip('.')}»?", f"{f[1]} {f[2]}") for e in d["equipos"] for f in d["fallas"][e][:2]] + [(f"¿Cómo pido una visita para mi equipo {N}?", "Escribe por WhatsApp con el modelo, la falla y tu zona. Coordinamos día y franja horaria.")]
    pagina(pathb(m, "preguntas-frecuentes"), f"Preguntas frecuentes sobre {N} en Panamá", f"Respuestas a las preguntas más comunes sobre servicio técnico {N} en Panamá: cobertura, tiempos, garantía y cómo pedir una visita.",
           f"Preguntas frecuentes sobre servicio técnico {N}",
           sec("Preguntas frecuentes", faq_html(PF)),
           m, (elegir(m, m + "faq", 1) or [None])[0], crumbs0 + [("Preguntas frecuentes", pathb(m, "preguntas-frecuentes"))], [faq_ld(PF)], bd=f"{N} · Preguntas", lead=f"Respuestas claras sobre el servicio técnico {N} en Panamá.", prio="0.6")
    # --- diagnóstico
    wiz = {e: [[a, b, c] for a, b, c in d["fallas"][e]] for e in d["equipos"]}
    opts = "".join(f'<option value="{e}">{EQ[e][1]}</option>' for e in d["equipos"])
    js = f'<script>window.WIZ={json.dumps(wiz, ensure_ascii=False)};window.WIZB={json.dumps(N)};</script>' + JS_WIZ
    pagina(pathb(m, "diagnostico-por-sintoma"), f"Diagnóstico por síntoma {N}: qué le pasa a tu equipo", f"Elige tu equipo {N} y el síntoma que notas para ver la causa más probable y qué revisaría un técnico. Herramienta gratuita.",
           f"Diagnóstico por síntoma de equipos {N}",
           sec("¿Qué le pasa a tu equipo?", rr("Elige el equipo y lo que notas. Te mostramos la causa más probable según las fallas que vemos en equipos de esta marca en Panamá.") + f'<div class="wiz card"><label>Equipo</label><select id="wq">{opts}</select><label>Síntoma</label><select id="ws"></select><div class="res" id="wr"></div></div><p><small>Es una guía orientativa. La causa se confirma con pruebas en el equipo.</small></p>'),
           m, (elegir(m, m + "diag", 1) or [None])[0], crumbs0 + [("Diagnóstico por síntoma", pathb(m, "diagnostico-por-sintoma"))], bd=f"{N} · Diagnóstico", extra_js=js, noindex=True, lead=f"Herramienta gratuita para entender qué le pasa a tu equipo {N}.")


import unicodedata
def slug(t):
    t = unicodedata.normalize("NFKD", t.lower()).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    if len(s) > 70 and CFG.get("tv"): s = s[:70].rsplit("-", 1)[0]
    return s[:70]
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
    ps = [x.strip() for x in re.split(r"(?<=[.])\s+", t.strip()) if x.strip()]
    return " ".join(ps[:2]) if ps else t
def variantes(N, sing, sint):
    base_ = uni(sing, N, sint).replace(": ", " ")
    pal = bajar(sint).rstrip(".").split()
    return [base_, f"{base_} solución", f"reparar {sing} {N} en Panamá", f"técnico {N} {sing} a domicilio Panamá", f"{sing} {N} problema {' '.join(pal[:3])}"]
SINT = {}   # marca -> lista (equipo, slug, sintoma, causa, revisamos)
def cierre_sint(m, e, sl):
    d = M[m]; N = nom(m)
    L = []
    for e2 in d["equipos"]:
        for i, (a, b, c) in enumerate(d["fallas"][e2]):
            L.append((e2, slug(EQ[e2][1] + " " + a), a, b, c))
    SINT[m] = L
ART_EQ = {"tv-led": "una", "tv-qled": "una", "tv-oled": "una", "neveras": "una", "lavadoras": "una", "secadoras": "una", "aires": "un", "cocinas": "una", "lavavajillas": "un", "centro-lavado": "un", "batidoras": "una", "microondas": "un"}
def build_sintomas(m):
    d = M[m]; N = nom(m); crumbs0 = [(f"Centro de Servicio Técnico {N} Panamá", base(m))]
    cierre_sint(m, None, None)
    L = SINT[m]
    for k, (e, sl, a, b, c) in enumerate(L):
        sing = EQ[e][1]; pl = EQ[e][2]; N_ = N; art = ART_EQ[e]
        idx = [x[1] for x in L if x[0] == e].index(sl)
        probar, cod_ = CONSEJOS[f"{m}|{e}|{idx}"]
        hermanas = [x for x in L if x[0] == e and x[1] != sl][:4] or [x for x in L if x[1] != sl][:4]
        hermanas_html = "".join(f'<a class="card l" href="{pathb(m, "falla-" + x[1])}"><span class="t">{esc(cap(bajar(x[2]).rstrip(".")))}</span></a>' for x in hermanas)
        # códigos solo si la falla trata de un código o error
        cod = d["codigos"].get("Lavadoras" if e in ("lavadoras", "centro-lavado") else "Refrigeradoras" if e == "neveras" else "_", [])
        cod_html = ""
        if cod and re.search(r"c[oó]digo|error|pantalla|muestra|\bE\d|Er ", a, re.I):
            cod_html = sec(f"Códigos de {pl} {N_}", tabla(["Código", "Qué suele indicar"], [(f'<span class="cb">{x}</span>', esc(y)) for x, y in cod[:6]]) + f'<p><a href="{pathb(m, "codigos-de-error")}">Ver todos los códigos de error {N_}</a></p>', alt=True)
        im = elegir(m, m + sl, 1, e) + elegir(m, m + sl + "g", 1)
        nombre = (f"{cap(sing)} {N_}: {bajar(a).rstrip('.')}" if CFG.get("tv") else cap(uni(sing, N_, a)))
        titulo = nombre
        while len(titulo) > 62 and re.search(r"\s(o|y|,)\s", titulo): titulo = re.sub(r"\s+(?:o|y)\s+[^ ]*(?:\s+[^ ]+)*$", "", titulo, count=1) if re.search(r"\s(o|y)\s", titulo) else titulo
        if len(titulo) > 62: titulo = re.sub(r"(\s+(?:de|en|y|a|la|el|los|las|con|para|del|que|o|u|al|no|se))+$", "", titulo[:62].rsplit(" ", 1)[0].rstrip(" ,:;"))
        if len(titulo) <= 42: titulo += " | Causa y solución"
        q = f"«{a.rstrip('.')}»"
        faq = [(f"¿Cuánto cuesta arreglar {q} en {art} {sing} {N_}?", f"Depende de la pieza. La causa más probable es: {bajar(b)} Después del diagnóstico te damos el valor por escrito antes de reparar."),
               (f"¿Qué datos necesito para pedir la visita por {q}?", f"El modelo del equipo y una foto o descripción de lo que notas. {d['etiqueta'].get(e, 'Busca la etiqueta con el modelo y la serie en el equipo.')}")]
        navtop = f'<div class="anc"><a href="{pathb(m, "reparacion-" + EQ[e][0])}">← Otras fallas de {pl}</a><a href="{pathb(m, "fallas")}">Índice de fallas {N_}</a><a href="{wa("Hola, mi " + sing + " " + N_ + " presenta: " + a)}" target="_blank" rel="noopener">Pedir visita</a></div>'
        paso = f"<p><b>Qué puedes hacer tú:</b> {esc(probar)}</p><p><b>¿Llamar al técnico?</b> {esc(LLAMAR[cod_])}</p>"
        tec = f"<p>{esc(c)}</p>"
        tec_html = f'<div class="two" style="align-items:start"><div>{tec}<p><a class="btn" href="{wa("Hola, mi " + sing + " " + N_ + " presenta: " + a)}" target="_blank" rel="noopener">Pedir la visita</a></p></div>' + (f'<img loading="lazy" src="{im[1][0]}" alt="{im[1][1]}" width="1024" height="768">' if len(im) > 1 else "") + '</div>'
        piezas = []
        for parte, rx in PARTES.get(e, []):
            if re.search(rx, b + " " + c, re.I) and parte in PARTE_DESC: piezas.append((parte, PARTE_DESC[parte]))
        piezas_html = sec(f"Las piezas que pueden estar fallando", "<p>Según lo que notas, estas son las piezas que revisamos primero y qué hace cada una:</p><dl class=\"pz\">" + "".join(f"<dt>{esc(p)}</dt><dd>{esc(t)}<br><b>Cómo lo comprobamos:</b> {esc(PARTE_DIAG.get(p, ''))}</dd>" for p, t in piezas[:4]) + "</dl>") if piezas else ""
        cuerpo = (sec(f"¿Qué le pasa a tu {sing} {N_}?", navtop + stepper(3) + rr(f"<b>{esc(cap(bajar(a).rstrip('.')))}.</b> Lo más probable: {esc(bajar(b))}"))
                  + sec("Qué hacer, paso a paso", paso, alt=True)
                  + sec(f"¿Puedo seguir usando mi {sing}?", f"<p>{esc(USAR[cod_])}</p>")
                  + sec("Qué revisa el técnico", tec_html, alt=True)
                  + piezas_html.replace('<section class="s">', '<section class="s">', 1)
                  + cod_html
                  + sec(f"Cómo distinguirla de otras fallas de {pl} {N_}", "<ul>" + "".join(f"<li>Si lo que notas es «{esc(bajar(x[2]).rstrip('.'))}», la causa suele ser distinta: {esc(bajar(x[3]))}</li>" for x in hermanas[:3]) + "</ul>", alt=not bool(cod_html))
                  + sec(f"Otras fallas de {pl} {N_}", f'<div class="g c2">{hermanas_html}</div><p><a href="{pathb(m, "reparacion-" + EQ[e][0])}">Ver toda la reparación de {pl} {N_}</a></p>', alt=bool(cod_html))
                  + sec("Preguntas frecuentes", faq_html(faq), alt=not bool(cod_html))
                  + f"<!--RELF:{e}-->")
        pagina(pathb(m, "falla-" + sl), titulo, f"{nombre}: causa más probable, qué puedes hacer tú, cuándo llamar al técnico y qué revisa en tu casa. Servicio a domicilio en Panamá.",
               nombre, cuerpo, m, im[0] if im else None, crumbs0 + [(f"Reparación de {pl}", pathb(m, "reparacion-" + EQ[e][0])), (a[:45], pathb(m, "falla-" + sl))],
               [faq_ld(faq), {"@type": "Service", "name": f"Reparación: {nombre}", "provider": {"@id": DOM + "/#negocio"}, "areaServed": "Panamá"}], bd=f"{N_} · {pl.capitalize()}", prio="0.7", noindex=(len(b) + len(c) < 40),
               lead="Qué puede ser, qué puedes probar tú y cuándo llamar al técnico.")
    # índice de fallas
    grupos = ""
    for e in d["equipos"]:
        items = "".join(f'<a class="card l" href="{pathb(m, "falla-" + x[1])}"><span class="t">{esc(x[2])}</span><br><small>{esc(x[3][:90])}</small></a>' for x in L if x[0] == e)
        grupos += sec(f"Fallas de {EQ[e][2]} {N}", f'<div class="g c2">{items}</div>', alt=(d["equipos"].index(e) % 2 == 1))
    il = {"@type": "ItemList", "name": f"Fallas frecuentes de {N}", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": DOM + pathb(m, "falla-" + x[1]), "name": f"{EQ[x[0]][1].capitalize()} {N} {bajar(x[2]).rstrip('.')}"} for i, x in enumerate(L)]}
    pagina(pathb(m, "fallas"), f"Fallas frecuentes de equipos {N} en Panamá", f"Todas las fallas frecuentes de equipos {N} en Panamá, con su causa probable: {junta(EQ[e][2] for e in d["equipos"])}. Elige tu síntoma.",
           f"Fallas frecuentes de equipos {N}", sec("Elige tu síntoma", rr(f"Aquí están las fallas que más vemos en equipos {N} en Panamá. Entra a la tuya para ver la causa más probable, qué puedes revisar y qué hace el técnico.")) + grupos, m,
           (elegir(m, m + "fallas", 1) or [None])[0] if POOLS[m] else None, crumbs0 + [("Fallas frecuentes", pathb(m, "fallas"))], [il], bd=f"{N} · Fallas", prio="0.8", lead=f"Todas las fallas frecuentes de {N} en un solo lugar.")

def eq_de_consejo(t):
    x = t.lower()
    if CFG.get("tv"):
        if re.search(r"oled", x): return "tv-oled"
        if re.search(r"qled|mini led|one connect|caja", x): return "tv-qled"
        if re.search(r"pantalla|televisor|webos|tizen|google tv|vidaa|software|sistema|ventilaci|limpiar", x): return "tv-led"
        return None
    for e, rx in (("lavavajillas", r"lavavajillas"), ("microondas", r"microondas"), ("batidoras", r"batidora"), ("centro-lavado", r"torre|centro de lavado"), ("secadoras", r"secadora"), ("lavadoras", r"lavadora"), ("neveras", r"refrigeradora|nevera|filtro de agua"), ("aires", r"\baire|windfree"), ("cocinas", r"estufa|horno|cocina|bujía|bujia")):
        if re.search(rx, x): return e
    return None
def build_guia(m):
    d = M[m]; N = nom(m); crumbs0 = [(f"Centro de Servicio Técnico {N} Panamá", base(m))]
    blq = ""; generales = [x for x in d["mantenimiento"] if eq_de_consejo(x) is None]
    for k, e in enumerate(d["equipos"]):
        sing = EQ[e][1]; pl = EQ[e][2]
        tips = [x for x in d["mantenimiento"] if eq_de_consejo(x) == e]
        if e in ("neveras", "aires", "lavadoras", "centro-lavado") : tips += [x for x in generales if re.search(r"voltaje|inverter", x, re.I)]
        if not tips: continue
        alert = [x for x in d["fallas"][e]][:2]
        blq += sec(f"Cuidado de tu {sing} {N}", "<h3>Hazlo tú</h3><ul>" + "".join(f"<li>{esc(x)}</li>" for x in tips) + "</ul><h3>Señales de que conviene llamar</h3><ul>" + "".join(f"<li>{esc(a_)}: {esc(bajar(b_))}</li>" for a_, b_, c_ in alert) + f'</ul><p><a href="{pathb(m, "reparacion-" + EQ[e][0])}">Fallas de {pl} {N}</a></p>', alt=(k % 2 == 1))
    pagina(pathb(m, "guia-de-cuidado"), f"Guía de cuidado de equipos {N} en Panamá", f"Cómo cuidar tus equipos {N} en el clima de Panamá: tareas de mantenimiento por equipo y señales de que conviene llamar al técnico.",
           f"Guía de cuidado de equipos {N}", blq,
           m, (elegir(m, m + "guia", 1) or [None])[0], crumbs0 + [("Guía de cuidado", pathb(m, "guia-de-cuidado"))], [{"@type": "Article", "headline": f"Guía de cuidado de equipos {N}", "datePublished": HOY, "dateModified": HOY, "author": {"@id": DOM + "/#negocio"}, "publisher": {"@id": DOM + "/#negocio"}, "inLanguage": CFG["locale"]}],
           bd=f"{N} · Guía", prio="0.6", lead=f"Mantenimiento y señales de alerta para tus equipos {N}.")

EQ_VIDA = {
 "neveras": ("12 a 15 años", ["el compresor falla en un equipo con más de 12 años", "hay fugas de gas en el evaporador o el serpentín", "la reparación y el repuesto se acercan a la mitad del precio de una nueva"], ["falla un ventilador, un sensor, la resistencia de deshielo o el empaque", "la placa falla por un pico de voltaje y el equipo es relativamente nuevo"]),
 "lavadoras": ("8 a 12 años", ["el tambor o la tina están rotos o con óxido pasado", "los rodamientos fallan junto con el sello en un equipo con muchos años", "la reparación supera la mitad del precio de una nueva"], ["falla la bomba, el filtro, la cerradura, el interruptor de tapa o la electroválvula", "la placa o el motor fallan en un equipo con pocos años"]),
 "secadoras": ("10 a 13 años", ["el tambor está deformado o oxidado", "la placa y el motor fallan a la vez", "la reparación supera la mitad del precio de una nueva"], ["falla la resistencia, la correa, el termostato o el sensor de humedad", "el ducto de pelusa está tapado y el equipo se recalienta"]),
 "aires": ("10 a 15 años", ["el compresor falla en un equipo con muchos años y gas antiguo", "el serpentín tiene varias fugas", "la placa exterior se daña seguido por mala instalación eléctrica"], ["falla la placa, un sensor o el ventilador", "hay una fuga localizable o falta limpieza y gas"]),
 "cocinas": ("15 a 20 años", ["el horno tiene la cavidad oxidada o la puerta deformada", "la placa o la mesa de inducción está agrietada", "faltan repuestos del modelo"], ["falla un quemador, una bujía, el módulo de encendido o la resistencia", "el termostato o la válvula del horno no regula bien"]),
 "lavavajillas": ("9 a 12 años", ["la tina tiene fugas o está oxidada", "la bomba y la placa fallan a la vez", "la reparación supera la mitad del precio de una nueva"], ["falla la bomba, el filtro, un brazo rociador o el sello de la puerta", "hay sarro o residuos que bloquean el paso del agua"]),
 "centro-lavado": ("8 a 12 años", ["la placa principal y un motor fallan a la vez", "una de las dos unidades tiene daño estructural", "la reparación supera la mitad del precio de uno nuevo"], ["falla un conector, una resistencia o el interruptor de tapa", "una unidad funciona y la otra solo necesita un ajuste"]),
 "microondas": ("7 a 10 años", ["el magnetrón falla y el equipo ya es antiguo", "la cavidad está oxidada o con chispas por daño en la pared interior", "el costo de la pieza se acerca al de uno nuevo"], ["falla el plato giratorio, el fusible o la cerradura de la puerta", "el panel o el fusible de alta tensión necesitan cambio"]),
 "batidoras": ("más de 10 años con buen mantenimiento", ["el motor está quemado y el repuesto es difícil de conseguir", "la carcasa de engranes está rota", "hay daños por golpes o líquidos dentro del motor"], ["la grasa de la caja de engranes se secó o se escapó", "faltan escobillas o hay ruido de rechinado por desgaste normal"]),
}
PARTE_DIAG = {
 "Ventilador del evaporador": "Abrimos el panel del congelador, giramos el aspa con la mano para ver si está trabada por hielo y medimos si el motor recibe corriente.",
 "Resistencia de deshielo": "Medimos su continuidad con multímetro; una resistencia abierta no calienta y deja la escarcha pegada.",
 "Sensor de temperatura": "Medimos su resistencia a temperatura ambiente y la comparamos con la tabla del fabricante.",
 "Placa electrónica o inverter": "Medimos la tensión de entrada y la señal que envía al compresor y a los ventiladores; buscamos pistas quemadas o condensadores hinchados.",
 "Compresor": "Medimos el bobinado y el consumo al arrancar; escuchamos si arranca, se calienta y se apaga por protección.",
 "Relé de arranque": "Lo sacamos y lo agitamos para oír si hay piezas sueltas; probamos su continuidad y su respuesta al arrancar.",
 "Filtro de agua": "Lo revisamos por fecha de cambio y medimos el caudal con y sin el filtro puesto.",
 "Electroválvula de agua": "Medimos la tensión en la bobina cuando el equipo pide agua y comprobamos que la malla de entrada no esté tapada.",
 "Empaque de la puerta": "Pasamos un papel entre la puerta y el empaque para ver dónde no sella y revisamos si está rígido o roto.",
 "Termostato": "Lo medimos con el equipo frío y caliente para ver si corta y conecta a la temperatura correcta.",
 "Bomba de drenaje": "Desmontamos la bomba, giramos el impulsor a mano y medimos el motor; buscamos objetos atascados.",
 "Filtro de la bomba": "Lo desenroscamos con una bandeja debajo y buscamos monedas, pelusa o hebras que bloqueen el paso.",
 "Rodamientos del tambor": "Giramos el tambor con la mano y sentimos juego o rugosidad; confirmamos con el ruido al centrifugar.",
 "Amortiguadores": "Empujamos el tambor hacia abajo y lo soltamos; si rebota más de una vez, el amortiguador está vencido.",
 "Electroválvula de entrada": "Medimos la tensión de la bobina al pedir agua y revisamos que la malla y la presión de la llave sean correctas.",
 "Presostato (sensor de nivel)": "Soplamos suavemente por la manguera del presostato para oír el clic y medimos la continuidad según el nivel.",
 "Cerradura de puerta": "Probamos el cierre y el enclavamiento de forma manual y medimos la bobina que bloquea la puerta.",
 "Interruptor de tapa": "Medimos su continuidad con la tapa cerrada y abierta; también revisamos el actuador plástico de la tapa.",
 "Transmisión, embrague o correa": "Quitamos la tapa inferior, giramos el eje a mano y revisamos desgaste de la correa, el acople o las zapatas del embrague.",
 "Placa o tarjeta de control": "Revisamos pistas quemadas, humedad y conectores; medimos las salidas a motor, bomba y válvulas.",
 "Motor y sensor del motor": "Medimos el bobinado y la señal del sensor de velocidad; verificamos que las escobillas, si las hay, no estén gastadas.",
 "Resistencia": "Medimos su continuidad; una resistencia abierta o con tierra explica que el equipo no caliente.",
 "Termostato y fusible térmico": "Medimos continuidad de ambos; un fusible abierto casi siempre indica sobrecalentamiento previo por ducto tapado.",
 "Correa y rodillos": "Abrimos la secadora, giramos el tambor a mano y revisamos tensión y desgaste de correa y rodillos.",
 "Sensor de humedad": "Limpiamos las barras del sensor y medimos su respuesta con la ropa húmeda.",
 "Bomba de condensado": "Medimos el motor de la bomba y revisamos mangueras y depósito por obstrucciones.",
 "Filtro y ducto de pelusa": "Limpiamos filtro y ducto y medimos el flujo de aire en la salida; un ducto tapado es una causa frecuente de apagado por temperatura.",
 "Gas refrigerante": "Medimos presiones con manómetros y buscamos fugas en uniones y serpentines antes de recargar nada.",
 "Placa de la unidad exterior": "Medimos la alimentación y las señales hacia compresor y ventilador; revisamos humedad y daños por picos de voltaje.",
 "Drenaje y manguera": "Verificamos la pendiente de la manguera y soplamos el drenaje para ver si el agua fluye libre.",
 "Filtros y serpentín": "Limpiamos filtros y revisamos el serpentín por suciedad o hielo; medimos la diferencia de temperatura del aire.",
 "Resistencia del horno": "Medimos su continuidad y buscamos zonas quemadas o con mal contacto en los terminales.",
 "Bujías de encendido": "Las limpiamos y comprobamos que la chispa salte de forma continua y cerca del quemador.",
 "Módulo de encendido": "Medimos la alimentación al módulo y la salida hacia las bujías.",
 "Relé de la placa": "Escuchamos si el relé hace clic y medimos la salida cuando debería dar corriente.",
 "Termostato y válvula": "Probamos la temperatura real del horno con un termómetro y comprobamos que la válvula abra y cierre el gas.",
 "Ventilador de convección": "Giramos el aspa a mano y medimos el motor; revisamos que nada roce dentro de la cavidad.",
 "Interruptor selector": "Medimos continuidad en cada posición del selector.",
 "Bobina de inducción": "Medimos la bobina y revisamos el ventilador que la enfría; verificamos que la olla sea apta.",
 "Brazos rociadores": "Los retiramos, los lavamos y revisamos que cada orificio esté libre y que giren sin trabarse.",
 "Filtro del fondo": "Lo sacamos y revisamos restos y sarro; también miramos la manguera de drenaje.",
 "Sensor de turbidez": "Medimos su respuesta con agua limpia y sucia, y limpiamos la lente del sensor.",
 "Sello de la puerta": "Revisamos deformaciones o suciedad en el sello y que la puerta cierre pareja.",
 "Triturador": "Giramos la cuchilla a mano buscando huesos o restos duros que la bloqueen.",
 "Placa principal": "Revisamos alimentación, pistas y conectores; medimos las salidas hacia cada unidad del centro de lavado.",
 "Cableado y conectores": "Seguimos los cables entre placa, motor y sensores y buscamos conectores flojos, quemados o corroídos.",
 "Resistencia de la secadora": "Medimos continuidad y comprobamos que el termostato y el fusible no estén abiertos.",
 "Motor": "Medimos bobinado y consumo; revisamos que gire libre y que el condensador de arranque, si lo tiene, esté en buen estado.",
}
PARTE_DESC = {
 "Ventilador del evaporador": "Mueve el aire frío del congelador hacia el refrigerador. Si se traba o se escarcha, el congelador enfría pero el refrigerador queda tibio y se oye un zumbido.",
 "Resistencia de deshielo": "Derrite la escarcha del evaporador cada cierto tiempo. Si falla, se forma hielo en el fondo y el aire deja de circular.",
 "Sensor de temperatura": "Le dice a la placa qué tan frío o caliente está el equipo. Un sensor descalibrado hace que el equipo enfríe de más, de menos o muestre un código.",
 "Placa electrónica o inverter": "Es el cerebro que controla compresor, ventiladores y deshielo. Los picos de voltaje suelen dañarla; el equipo deja de enfriar o muestra error sin hacer ruido.",
 "Compresor": "Es el motor que hace circular el refrigerante. Si arranca y se apaga a cada rato, o no arranca, el equipo pierde frío poco a poco.",
 "Relé de arranque": "Pieza pequeña que ayuda a arrancar el compresor. Cuando falla se oye un clic repetido y el compresor no arranca.",
 "Filtro de agua": "Limpia el agua del dispensador y del hielo. Saturado, reduce el caudal o hace que el agua salga lenta o con mal sabor.",
 "Electroválvula de agua": "Abre y cierra el paso del agua. Si falla o se tapa, el dispensador no sale agua o la lavadora no llena.",
 "Empaque de la puerta": "Sella la puerta contra el cuerpo. Si está rígido o roto, entra aire caliente, se forma hielo y el compresor trabaja de más.",
 "Termostato": "Corta y da corriente según la temperatura. Un termostato defectuoso hace que el equipo no enfríe o no pare nunca.",
 "Bomba de drenaje": "Saca el agua del tambor o de la cuba. Si se tapa o se quema, el equipo se queda con agua o no avanza el ciclo.",
 "Filtro de la bomba": "Atrapa monedas, pelusa y residuos antes de la bomba. Si se tapa, el agua no sale y aparece un error de drenaje.",
 "Rodamientos del tambor": "Permiten que el tambor gire parejo. Desgastados, hacen un ruido metálico fuerte al centrifugar.",
 "Amortiguadores": "Sujetan el tambor y absorben la vibración. Vencidos, la lavadora salta o golpea al centrifugar.",
 "Electroválvula de entrada": "Deja entrar el agua a la lavadora. Si falla, la lavadora llena poco, no llena o sigue entrando agua.",
 "Presostato (sensor de nivel)": "Mide el nivel de agua dentro de la tina. Con falla, la lavadora llena de más, de menos o marca error de nivel.",
 "Cerradura de puerta": "Bloquea la puerta durante el ciclo. Si no cierra o no se libera, la lavadora no arranca o no abre al terminar.",
 "Interruptor de tapa": "Detecta que la tapa está cerrada. Si falla, la lavadora no centrifuga o se detiene con la tapa cerrada.",
 "Transmisión, embrague o correa": "Transmite el giro del motor al tambor o agitador. Desgastada, el agitador no se mueve aunque el motor suene.",
 "Placa o tarjeta de control": "Ordena todo el ciclo de lavado. Dañada por humedad o voltaje, la lavadora se detiene, marca códigos o no responde.",
 "Motor y sensor del motor": "Hace girar el tambor. El sensor controla su velocidad; si falla, el tambor gira lento, se detiene o marca error.",
 "Resistencia": "Genera el calor de la secadora u horno. Quemada, el equipo gira o enciende pero no calienta.",
 "Termostato y fusible térmico": "Protegen contra sobrecalentamiento. Si se disparan, la secadora se apaga sola o deja de calentar.",
 "Correa y rodillos": "Hacen girar el tambor de la secadora. Gastados, el tambor no gira o suena al girar.",
 "Sensor de humedad": "Detecta si la ropa ya está seca. Sucio o dañado, la secadora corta el ciclo antes de tiempo o seca de más.",
 "Bomba de condensado": "Saca el agua que genera la secadora. Si falla, aparece un error de drenaje o de depósito lleno.",
 "Filtro y ducto de pelusa": "Retienen la pelusa de la ropa. Tapados, la secadora tarda más, se calienta de más y se apaga sola.",
 "Gas refrigerante": "Es lo que transporta el calor en el aire acondicionado. Si hay fuga, el equipo enciende pero enfría poco o nada.",
 "Placa de la unidad exterior": "Controla el compresor y el ventilador exterior. Los picos de voltaje y las tormentas la dañan con frecuencia.",
 "Drenaje y manguera": "Sacan el agua de condensación. Tapados, el agua gotea dentro de la casa.",
 "Filtros y serpentín": "Limpian y enfrían el aire. Sucios, reducen el flujo, congelan el serpentín y el equipo enfría poco.",
 "Resistencia del horno": "Calienta el horno. Quemada o con mal contacto, el horno no calienta o calienta de forma desigual.",
 "Bujías de encendido": "Producen la chispa de los quemadores. Sucias o desgastadas, el quemador no enciende o tarda en encender.",
 "Módulo de encendido": "Envía la chispa a las bujías. Con falla, ningún quemador enciende aunque salga gas.",
 "Relé de la placa": "Interruptor que da corriente a una función. Con falla, una función no responde aunque el resto funcione.",
 "Termostato y válvula": "Regulan el gas y la temperatura del horno. Con falla, el horno no mantiene la temperatura o no enciende.",
 "Ventilador de convección": "Reparte el aire caliente dentro del horno. Con falla, el horno calienta mal o hace ruido.",
 "Interruptor selector": "Elige la función del horno. Con desgaste, la función elegida no responde.",
 "Bobina de inducción": "Calienta la olla por campo magnético. Con falla, la zona marca error o no calienta.",
 "Brazos rociadores": "Reparten el agua sobre la vajilla. Tapados con sarro o residuos, lavan mal y dejan restos.",
 "Filtro del fondo": "Retiene residuos de comida. Saturado, el lavavajillas no drena bien y huele.",
 "Sensor de turbidez": "Mide qué tan sucia está el agua. Con falla, el programa se alarga o lava mal.",
 "Sello de la puerta": "Evita que el agua salga. Deformado o sucio, gotea por la puerta.",
 "Triturador": "Muele restos de comida pequeños. Atascado, el lavavajillas no drena.",
 "Placa principal": "Controla ambos equipos del centro de lavado. Con falla, una o las dos unidades dejan de responder.",
 "Cableado y conectores": "Comunican la placa con el motor y los sensores. Un conector flojo o corroído causa fallas intermitentes.",
 "Resistencia de la secadora": "Calienta el aire de la secadora. Quemada, la secadora gira pero no calienta.",
 "Motor": "Hace girar el tambor o el eje. Con falla, no gira, gira lento o se calienta de más.",
}
PARTES = {
 "neveras": [("Ventilador del evaporador", r"ventilador"), ("Resistencia de deshielo", r"deshielo|resistencia"), ("Sensor de temperatura", r"sensor"), ("Placa electrónica o inverter", r"placa|inverter|tarjeta|control"), ("Compresor", r"compresor"), ("Relé de arranque", r"relé|rele|protector"), ("Filtro de agua", r"filtro"), ("Electroválvula de agua", r"electrov"), ("Empaque de la puerta", r"empaque|sell"), ("Termostato", r"termostato")],
 "lavadoras": [("Bomba de drenaje", r"bomba"), ("Filtro de la bomba", r"filtro"), ("Rodamientos del tambor", r"rodamiento"), ("Amortiguadores", r"amortiguador|suspensi"), ("Electroválvula de entrada", r"electrov|válvula|valvula"), ("Presostato (sensor de nivel)", r"presostato|nivel"), ("Cerradura de puerta", r"cerradura"), ("Interruptor de tapa", r"interruptor|\btapa\b"), ("Transmisión, embrague o correa", r"transmisi|embrague|correa|acople"), ("Placa o tarjeta de control", r"placa|tarjeta|control"), ("Motor y sensor del motor", r"motor|hall")],
 "secadoras": [("Resistencia", r"resistencia"), ("Termostato y fusible térmico", r"termostato|fusible"), ("Correa y rodillos", r"correa|rodillo"), ("Sensor de humedad", r"humedad"), ("Bomba de condensado", r"bomba|condensad"), ("Filtro y ducto de pelusa", r"filtro|ducto|pelusa")],
 "aires": [("Gas refrigerante", r"gas"), ("Sensor de temperatura", r"sensor"), ("Placa de la unidad exterior", r"placa|voltaje"), ("Drenaje y manguera", r"drenaje|manguera"), ("Filtros y serpentín", r"filtro|serpent"), ("Compresor", r"compresor")],
 "cocinas": [("Resistencia del horno", r"resistencia"), ("Sensor de temperatura", r"sensor"), ("Bujías de encendido", r"buj"), ("Módulo de encendido", r"módulo|modulo"), ("Relé de la placa", r"relé|rele"), ("Termostato y válvula", r"termostato|válvula|valvula"), ("Ventilador de convección", r"ventilador|convecci"), ("Interruptor selector", r"selector|interruptor"), ("Bobina de inducción", r"bobina|inducci")],
 "lavavajillas": [("Bomba de drenaje", r"bomba"), ("Filtro del fondo", r"filtro"), ("Brazos rociadores", r"brazo|rociador"), ("Sensor de turbidez", r"sensor"), ("Sello de la puerta", r"sello"), ("Triturador", r"triturador")],
 "centro-lavado": [("Placa principal", r"placa|tarjeta"), ("Cableado y conectores", r"cableado|conector|comunicaci"), ("Resistencia de la secadora", r"resistencia"), ("Interruptor de tapa", r"interruptor|\btapa\b"), ("Motor", r"motor")],
 "batidoras": [("Grasa y caja de engranes", r"grasa|engrane"), ("Escobillas del motor", r"escobilla"), ("Control de velocidad", r"control|velocidad"), ("Tornillo de altura", r"altura|tazón|tazon")],
 "microondas": [("Magnetrón", r"magnetr"), ("Diodo y capacitor", r"diodo|capacitor"), ("Fusible de alta tensión", r"fusible"), ("Placa guía de ondas", r"gu[ií]a")],
}

def accion_cod(t):
    x = t.lower()
    if re.search(r"no es falla|aviso|bloqueo de niños", x): return "No necesitas técnico: no es una falla."
    if re.search(r"puerta|cerradura", x): return "Cierra bien la puerta y revisa el empaque; si el código sigue, llama."
    if re.search(r"desbalance|\bcarga\b|espuma", x): return "Reacomoda la carga y prueba otra vez; si sigue, llama."
    if re.search(r"motor|sensor|placa|control|comunic|calentador|ventilador|deshielo|compresor|presostato|exceso", x): return "Apaga y desconecta 5 minutos; si el código vuelve, llama: requiere técnico."
    if re.search(r"filtro|llave|drena|agua|manguera|bomba|entrada|válvula", x): return "Revisa la llave de agua y los filtros; si el código vuelve, llama."
    return "Apaga y desconecta 5 minutos; si el código vuelve, llama."
def build_terminos(m):
    d = M[m]; N = nom(m); crumbs0 = [(f"Centro de Servicio Técnico {N} Panamá", base(m))]; E = d["equipos"]; bi = BRANDS_ORDER.index(m)
    wam = wa(f"Hola, necesito servicio técnico {N} en Panamá")
    nv = lambda t: "Alto" if re.search(r"placa|tarjeta|compresor|inverter|bobina|magnetr|transmisi|rodamiento|control", t.lower()) else ("Bajo" if re.search(r"filtro|limpi|ajuste|manguera|buj|empaque|sello|llave|carga|grasa", t.lower()) else "Medio")
    # ---- 1 TELÉFONO: por equipo -> qué notas / causa probable / qué puedes probar / ¿llamar?
    bloques = ""
    for e in E:
        filas = []
        for k_, (a_, b_, c_) in enumerate(d["fallas"][e]):
            pr, cd_ = CONSEJOS[f"{m}|{e}|{k_}"]
            filas.append((f"<b>{esc(a_)}</b>", esc(b_), esc(pr), esc(LLAMAR[cd_])))
        tb = tabla(["Lo que notas", "Causa probable", "Qué puedes probar tú", "¿Llamar al técnico?"], filas)
        cd = ""
        for g, L in d["codigos"].items():
            if (g == "Lavadoras" and e in ("lavadoras", "centro-lavado")) or (g == "Refrigeradoras" and e == "neveras"):
                cd = f"<h3>Si en la pantalla aparece un código</h3>" + tabla(["Código", "Qué significa", "Qué hacer"], [(f'<span class="cb">{c}</span>', esc(t_), esc(accion_cod(t_))) for c, t_ in L])
        bloques += f"<details><summary><b>{EQ[e][2].capitalize()} {N}</b>: qué hacer según lo que notas</summary><p>{esc(_prim(d['tech'][e]))}</p>{tb}{cd}</details>"
    modelos = tabla(["Equipo", "Dónde está el número de modelo"], [(EQ[e][2].capitalize(), esc(cap(etq(d["etiqueta"].get(e, "en una etiqueta pegada al equipo"))) + ".")) for e in E])
    pagina(pathb(m, "telefono-servicio-tecnico"), f"Teléfono servicio técnico {N} Panamá: {TEL}", f"Teléfono y WhatsApp del servicio técnico {N} en Panamá: {TEL}. Qué probar tú según la falla de tu equipo {N} y cuándo llamar al técnico.", f"Teléfono del servicio técnico {N} en Panamá",
           sec(f"{TEL}: llama o escribe por WhatsApp", f"<p>Este es el teléfono y WhatsApp del servicio técnico {N} en Panamá. Atendemos con visita a domicilio para {pls_(d)}.</p>" + f'<p><a class="btn" href="{wam}" target="_blank" rel="noopener">Escribir por WhatsApp</a> <a class="btn o" href="tel:+{TELN}">Llamar {TEL}</a></p>')
           + sec(f"Antes de llamar: elige tu equipo {N}", "<p>Abre tu equipo y mira qué le pasa. Si la falla se puede resolver sin técnico, te lo decimos; si no, llámanos.</p>" + bloques, alt=True)
           + sec("Ten a mano el modelo", f"<p>{esc(d['modelo_ej'])}</p>" + modelos),
           m, (elegir(m, m + "tel", 1) or [None])[0], crumbs0 + [("Teléfono", pathb(m, "telefono-servicio-tecnico"))], bd=f"{N} · Contacto", prio="0.7", lead=f"Qué probar según la falla de tu equipo {N} y cuándo llamar.")
    # ---- 2 CERCA DE MÍ: una línea por zona con la falla local y el equipo
    todas = [(e, f) for e in E for f in d["fallas"][e]]
    zl = ""
    for zi, (z, (zn, barrios, rasgo)) in enumerate(ZONAS.items()):
        (e, f), (e2, f2) = distintos(todas, bi * 2 + zi * 3 + 1, 2)
        v = (bi + 2 * zi) % 4
        if v == 0: t = f"para equipos {N} se atienden {EQ[e][2]} («{esc(bajar(f[0]).rstrip('.'))}») y {EQ[e2][2]} («{esc(bajar(f2[0]).rstrip('.'))}»). Sectores: {ZX[z][2]}."
        elif v == 1: t = f"con {ZX[z][1]}. Caso típico en {N}: {EQ[e][1]} con «{esc(bajar(f[0]).rstrip('.'))}», causa probable {esc(bajar(f[1]).rstrip('.'))}."
        elif v == 2: t = f"{ZX[z][0]}. En equipos {N} se ve «{esc(bajar(f2[0]).rstrip('.'))}» en {EQ[e2][2]}; en la visita: {esc(bajar(f2[2]).rstrip('.'))}."
        else: t = f"sectores como {ZX[z][2]}. Para {N}, lo habitual es {EQ[e][1]} con «{esc(bajar(f[0]).rstrip('.'))}» o {EQ[e2][1]} con «{esc(bajar(f2[0]).rstrip('.'))}»."
        zl += f'<li><a href="{pathb(m, "servicio-tecnico-" + z)}">{zn}</a> · {t}</li>'
    pagina(pathb(m, "centro-de-servicio-cerca-de-mi"), f"Centro de servicio {N} cerca de mí en Panamá", f"Centro de servicio {N} cerca de ti en Panamá: el técnico llega a tu casa. Zonas, sectores y qué equipos {N} atendemos en cada una.", f"Centro de servicio {N} cerca de mí en Panamá",
           sec(f"Dónde llega el técnico {N}", f"<p>Elige tu zona:</p><ul>{zl}</ul>"),
           m, (elegir(m, m + "cerca", 1) or [None])[0], crumbs0 + [("Cerca de mí", pathb(m, "centro-de-servicio-cerca-de-mi"))], bd=f"{N} · Cerca de mí", prio="0.7", lead=f"Zonas donde el técnico {N} llega a tu casa.")
    # ---- 3 A DOMICILIO: qué revisa el técnico en tu casa por equipo + qué dejar listo
    pas = "".join(f"<li><b>{EQ[e][2].capitalize()} {N}:</b> {esc(d['fallas'][e][0][2])} {esc(d['fallas'][e][1][2] if len(d['fallas'][e]) > 1 else '')} <i>Ten a mano el modelo, que está {esc(etq(d['etiqueta'].get(e, 'en la etiqueta del equipo')))}.</i></li>" for e in E)
    pagina(pathb(m, "reparacion-a-domicilio"), f"Reparación {N} a domicilio en Panamá", f"Cómo es la reparación a domicilio de equipos {N} en Panamá: qué revisa el técnico en tu casa en cada equipo y qué debes dejar listo.", f"Reparación {N} a domicilio en Panamá",
           sec(f"Qué pasa cuando el técnico {N} llega a tu casa", f"<p>En la visita se hace primero el diagnóstico del equipo {N} y recién entonces se da el valor. Esto es lo que se revisa según el equipo:</p><ul>{pas}</ul>")
           + sec("Antes de la visita", f"<p>Despeja el espacio alrededor del equipo, ten a mano el modelo ({esc(d['modelo_ej'])}) y la factura si el equipo aún puede tener garantía.</p>", alt=True),
           m, (elegir(m, m + "dom", 1) or [None])[0], crumbs0 + [("A domicilio", pathb(m, "reparacion-a-domicilio"))], bd=f"{N} · Domicilio", prio="0.7", lead=f"La visita técnica {N}, equipo por equipo.")
    # ---- 4 REPUESTOS: piezas reales que aparecen en las fallas de esta marca, por equipo
    pz = ""
    for e in E:
        txt = [(x[0], x[1] + " " + x[2]) for x in d["fallas"][e]]
        filas = []
        for parte, rx in PARTES.get(e, []):
            cuando = [bajar(a_).rstrip(".") for a_, tx_ in txt if re.search(rx, tx_, re.I)]
            if cuando: filas.append((f"<b>{parte}</b>", esc("; ".join(cuando[:2]))))
        if filas: pz += f"<h3>{EQ[e][2].capitalize()} {N}</h3>" + tabla(["Pieza", "Se cambia cuando"], filas)
    pagina(pathb(m, "repuestos"), f"Repuestos {N} en Panamá", f"Repuestos para equipos {N} en Panamá: qué piezas se cambian en cada equipo, en qué falla y cuáles pueden pedirse por encargo.", f"Repuestos {N} en Panamá",
           sec(f"Piezas de equipos {N} que más se cambian", f"<p>{N} es una marca de {d['pais']}. Estas son las piezas que más vemos en sus equipos, y en qué falla se cambian:</p>" + pz)
           + sec("Originales o compatibles", f"<p>Usamos repuestos originales {N} cuando están disponibles; si no, compatibles de calidad, y te decimos cuál es cuál antes de que apruebes. Las placas y los compresores pueden requerir pedido; los filtros, bombas, sensores y empaques suelen conseguirse en Panamá.</p>", alt=True),
           m, (elegir(m, m + "rep", 1) or [None])[0], crumbs0 + [("Repuestos", pathb(m, "repuestos"))], bd=f"{N} · Repuestos", prio="0.7", lead=f"Piezas de equipos {N} y en qué falla se cambian.")
    # ---- 5 GARANTÍA: qué suele cubrir y qué no, según las fallas de la marca
    cub = [(EQ[e][1], x[0]) for e in E for x in d["fallas"][e] if nv(x[1]) == "Alto"][:5]
    nocub = [(EQ[e][1], x[0]) for e in E for x in d["fallas"][e] if nv(x[1]) == "Bajo"][:5]
    pagina(pathb(m, "garantia"), f"Garantía {N} en Panamá: qué cubre y qué no", f"Garantía de equipos {N} en Panamá: qué fallas suelen ser de componentes cubiertos, cuáles son de mantenimiento y qué garantía damos por la reparación.", f"Garantía {N} en Panamá: qué cubre y qué no",
           sec(f"La garantía de fábrica de {N}", f"<p>{esc(d['garantia'])}</p><p>{esc(d['origen'])}</p>")
           + sec("Fallas de componentes: suelen ser tema de garantía si el equipo es nuevo", "<ul>" + "".join(f"<li>{esc(a.capitalize())} {N}: {esc(bajar(b))}</li>" for a, b in cub) + "</ul>", alt=True)
           + sec("Fallas de mantenimiento: normalmente no las cubre", "<ul>" + "".join(f"<li>{esc(a.capitalize())} {N}: {esc(bajar(b))}</li>" for a, b in nocub) + "</ul>")
           + sec(f"Dónde encontrar los datos de garantía de tu {EQ[E[0]][1]} {N}", f"<p>{esc(d['modelo_ej'])} {esc(d['etiqueta'].get(E[0], ''))}</p><p>Líneas {N}: {', '.join(esc(x) for x in d['lineas'][:5])}.</p>", alt=True),
           m, (elegir(m, m + "gar2", 1) or [None])[0], crumbs0 + [("Garantía", pathb(m, "garantia"))], bd=f"{N} · Garantía", prio="0.7", lead=f"Qué cubre la garantía {N} y qué no.")

CLIMA = {"ciudad-de-panama": "la humedad constante y el salitre en edificios cercanos a la bahía", "san-miguelito": "los picos de voltaje en sectores de alta densidad y los apagones intermitentes", "arraijan": "los voltajes irregulares en urbanizaciones nuevas y el polvo de obra",
         "la-chorrera": "el calor y el polvo en urbanizaciones en crecimiento", "costa-del-este": "los edificios altos con aires de alta eficiencia y alta humedad frente al mar", "tocumen-y-24-de-diciembre": "el calor intenso y los cortes de energía por tormentas",
         "panama-oeste": "las urbanizaciones nuevas con equipos aún en garantía y el calor", "colon": "el salitre costero y la corrosión de condensadores y placas"}
def build_zonas_marca(m):
    d = M[m]; N = nom(m); crumbs0 = [(f"Centro de Servicio Técnico {N} Panamá", base(m))]; E = d["equipos"]
    bi = BRANDS_ORDER.index(m)
    todas = [(e, f) for e in E for f in d["fallas"][e]]
    items = ""
    for zi, (z, (zn, barrios, rasgo)) in enumerate(ZONAS.items()):
        viv, acc, sect = ZX[z]
        za = CFG.get("zart", {}).get(z, zn)
        var = (bi + zi) % 3
        fl = distintos(todas, bi * 3 + zi * 2, 3)
        det = "".join(f"<li><b>{esc(EQ[e][1].capitalize())} {N}:</b> {esc(f[0])}. {esc(f[1])} {esc(f[2])}</li>" for e, f in fl)
        e0 = fl[0][0]; e1 = fl[1][0] if fl[1][0] != fl[0][0] else fl[-1][0]
        if var == 0: intro = f"En {za} predominan {viv}. Para quienes tienen equipos {N} aquí, lo que más condiciona la visita es {acc}. Atendemos sectores como {sect}."
        elif var == 1: intro = f"{cap(za)} se caracteriza por {viv}; al coordinar el servicio técnico {N} hay que contar con {acc}. Entre los sectores que visitamos están {sect}."
        else: intro = f"Cuando un equipo {N} falla en {za} ({sect}), la visita tiene en cuenta {acc}. La zona combina {viv}."
        cuerpo = (sec(f"Servicio técnico {N} en {za}", f"<p>{esc(intro)}</p><p>{esc(CLIMA[z].capitalize())} influyen en cómo envejecen los equipos de esta zona.</p>")
                  + sec(f"Fallas de {N} que más se reportan en {za}", f"<ul>{det}</ul>", alt=True)
                  + sec(f"Cómo funcionan {EQ[e0][2]}" + (f" y {EQ[e1][2]}" if e1 != e0 else "") + f" {N}", f"<p>{esc(oracion(d['tech'][e0], zi))}</p>" + (f"<p>{esc(oracion(d['tech'][e1], zi + 1))}</p>" if e1 != e0 else ""))
                  + sec(f"Modelos {N} en {za}", f"<p>{esc(d['modelo_ej'])}</p><p><b>Líneas frecuentes:</b> {', '.join(esc(x) for x in _rot(d['lineas'], zi, 4))}.</p>", alt=True))
        pagina(pathb(m, "servicio-tecnico-" + z), f"Servicio técnico {N} en {za} | Panamá", f"Servicio técnico {N} a domicilio en {za}, Panamá: qué fallas de equipos {N} se reportan allí, sectores que visitamos y cómo coordinar la visita.",
               f"Servicio técnico {N} en {za}", cuerpo, m, (elegir(m, m + z, 1) or [None])[0], crumbs0 + [("Cobertura", pathb(m, "cobertura")), (zn, pathb(m, "servicio-tecnico-" + z))],
               [{"@type": "Service", "name": f"Servicio técnico {N} en {za}", "provider": {"@id": DOM + "/#negocio"}, "areaServed": {"@type": "Place", "name": zn}}], bd=f"{N} · {za}", prio="0.7", lead=f"Equipos {N} en {za}: fallas frecuentes y visita a domicilio.")
        items += f'<a class="card l" href="{pathb(m, "servicio-tecnico-" + z)}"><span class="t">Servicio técnico {N} en {za}</span><br><small>{esc(sect)}</small></a>'
    pagina(pathb(m, "cobertura"), f"Cobertura del servicio técnico {N} en Panamá", f"Zonas de Panamá donde damos servicio técnico a domicilio para equipos {N}.",
           f"Cobertura del servicio técnico {N} en Panamá", sec("Dónde atendemos equipos " + N, f'<div class="g c2">{items}</div>'), m, (elegir(m, m + "cob", 1) or [None])[0], crumbs0 + [("Cobertura", pathb(m, "cobertura"))], bd=f"{N} · Cobertura", prio="0.7", lead=f"Zonas de Panamá con visita a domicilio para equipos {N}.", noindex=True)



ZX = {  # datos locales por zona: vivienda, acceso y sectores representativos
 "ciudad-de-panama": ("edificios altos de apartamentos junto a casas antiguas en barrios tradicionales", "el tráfico y los estacionamientos de los edificios, por lo que la visita se coordina por franjas horarias", "El Cangrejo, Obarrio, San Francisco, Bella Vista y el Casco Antiguo"),
 "san-miguelito": ("viviendas muy densas, con muchos apartamentos y casas pareadas", "las calles estrechas de algunos sectores y la hora pico", "Belisario Frías, Mateo Iturralde y Amelia Denis de Icaza"),
 "arraijan": ("urbanizaciones nuevas al oeste del Canal", "el tráfico de salida de la ciudad en horas pico", "Vista Alegre, Burunga y Veracruz"),
 "la-chorrera": ("casas con patio y urbanizaciones en crecimiento", "la distancia desde la capital, que conviene considerar al pedir la franja", "Barrio Balboa, Barrio Colón y El Coco"),
 "costa-del-este": ("torres de apartamentos modernos frente al mar", "las porterías y los horarios de ascensor o mudanza de cada edificio", "Costa del Este, Santa María y Panamá Pacífico"),
 "tocumen-y-24-de-diciembre": ("viviendas del este, cerca del aeropuerto", "el tráfico de hora pico hacia el este de la ciudad", "Tocumen, 24 de Diciembre y Pacora"),
 "panama-oeste": ("urbanizaciones recientes con equipos aún nuevos", "la distancia entre urbanizaciones y el tráfico de la vía principal", "Howard, Veracruz y Vista Alegre"),
 "colon": ("edificios y casas de clima costero", "la distancia desde la capital", "Colón ciudad, Cristóbal y Sabanitas"),
}
def distintos(todas, k, n):
    rot = [todas[(k + i) % len(todas)] for i in range(len(todas))]
    out, vistos = [], set()
    for e, f in rot:
        if e not in vistos: out.append((e, f)); vistos.add(e)
        if len(out) == n: break
    for e, f in rot:
        if len(out) >= n: break
        if (e, f) not in out: out.append((e, f))
    return out
def _rot(lista, k, n):
    return [lista[(k + i) % len(lista)] for i in range(min(n, len(lista)))]



ARTS2 = [
 ("reparar-o-cambiar-un-electrodomestico-regla-del-50", "¿Reparar o cambiar tu electrodoméstico? La regla del 50%", "Cómo decidir si conviene reparar o reemplazar un electrodoméstico según el costo, la edad y el tipo de falla.", [
   ("La regla práctica", "Si la reparación cuesta más de la mitad de lo que vale un equipo nuevo parecido, suele convenir cambiarlo. Es una guía, no una ley: depende de la edad, del consumo y de si el repuesto se consigue."),
   ("La edad importa", "Una refrigeradora o lavadora con más de diez años acumula desgaste en varias piezas. Arreglar una falla puede traer otra pronto. En equipos de tres a siete años casi siempre conviene reparar."),
   ("Qué fallas suelen valer la pena", "Filtros, bombas, sensores, empaques, ventiladores y resistencias son reparaciones habituales y razonables. Una placa electrónica o un compresor cuestan más y piden comparar."),
   ("Pregunta antes de aprobar", "Pide el diagnóstico por escrito, el valor de la pieza, la mano de obra y la garantía de la reparación. Con esos datos haces la cuenta tú mismo.")]),
 ("que-es-un-compresor-inverter-y-por-que-importa", "Qué es un compresor inverter y por qué importa en Panamá", "Cómo funciona un compresor inverter, qué ventajas da en refrigeradoras y aires y por qué necesita protección de voltaje.", [
   ("Cómo trabaja", "Un compresor tradicional se enciende y se apaga. Uno inverter ajusta su velocidad según la necesidad: va más despacio cuando la temperatura ya es la correcta y acelera cuando hace falta."),
   ("Ventajas", "Menos ruido, temperatura más estable y menos consumo eléctrico, algo útil con el calor y la humedad de Panamá."),
   ("El punto débil", "Un inverter usa una placa electrónica. Los picos de voltaje por tormentas o apagones dañan esa placa antes que el compresor mismo."),
   ("Cómo cuidarlo", "Usa un protector de voltaje con retardo de reconexión, deja ventilación detrás del equipo y limpia el condensador cada seis meses.")]),
 ("voltaje-en-panama-110-220-y-tus-electrodomesticos", "Voltaje en Panamá: 110, 220 y tus electrodomésticos", "Qué voltaje usan los electrodomésticos en Panamá, cómo leer la etiqueta y por qué no conviene usar adaptadores con equipos de compresor.", [
   ("Qué voltaje hay en casa", "En Panamá la mayoría de las casas usan 120 voltios a 60 hertz en tomacorrientes comunes, y 240 voltios para equipos grandes como estufas eléctricas, secadoras y algunos aires."),
   ("Cómo leer la etiqueta", "La etiqueta del equipo indica voltaje, frecuencia y consumo. Si dice 220 o 240 V y lo conectas a 120 V, no funcionará bien; al revés, puedes dañarlo."),
   ("Equipos comprados fuera", "Un equipo traído de otro país puede usar otro voltaje o frecuencia. Confirma la etiqueta antes de conectarlo."),
   ("Por qué no usar adaptadores", "Neveras, aires y lavadoras tienen compresor o motor sensibles. Un adaptador mal escogido sobrecalienta el cable y acorta la vida del equipo.")]),
 ("mantenimiento-del-aire-acondicionado-en-epoca-lluviosa", "Mantenimiento del aire acondicionado en época lluviosa", "Qué revisar en tu aire acondicionado antes y durante las lluvias en Panamá: filtros, drenaje, unidad exterior y voltaje.", [
   ("Filtros cada mes", "Con uso diario, lava los filtros cada mes. Un filtro sucio reduce el aire frío y hace trabajar más al compresor."),
   ("Drenaje despejado", "La humedad alta genera más agua. Si el drenaje se tapa, el aire gotea dentro de la casa. Una limpieza anual evita ese problema."),
   ("Unidad exterior", "Retira hojas y polvo, deja espacio alrededor y evita que el agua de lluvia caiga directo sobre la placa."),
   ("Tormentas eléctricas", "Si hay tormenta fuerte, apaga y desconecta el aire cuando sea posible, o usa un protector de voltaje adecuado.")]),
 ("electrodomesticos-mojados-por-inundacion-que-hacer", "Electrodomésticos mojados por una inundación: qué hacer", "Pasos seguros si tus electrodomésticos se mojaron: no enchufar, secar, revisar y cuándo llamar a un técnico.", [
   ("Primero la seguridad", "Desconecta desde el breaker. No toques equipos conectados si el piso está mojado."),
   ("No lo enciendas", "Aunque parezca seco, la humedad dentro de placas y motores puede causar un corto al encender."),
   ("Qué puedes hacer", "Retira el agua visible, deja ventilar y evita usar secadores de calor intenso sobre las placas."),
   ("Cuándo llamar", "Pide una revisión antes de volver a usar el equipo. Un técnico mide aislamiento y estado de placas y motores.")]),
 ("como-elegir-un-servicio-tecnico-de-confianza", "Cómo elegir un servicio técnico de confianza", "Señales de un buen servicio técnico y alertas que debes evitar: diagnóstico, precio por escrito, garantía y repuestos.", [
   ("Diagnóstico antes del precio", "Un buen técnico revisa el equipo y explica la causa antes de dar un valor."),
   ("Precio por escrito", "Pide el valor de repuesto y mano de obra por escrito. Desconfía de cobros que cambian sin explicación."),
   ("Garantía de la reparación", "La pieza y la mano de obra deben tener garantía por escrito y con plazo claro."),
   ("Señales de alerta", "Pagos completos por adelantado, ninguna factura, piezas sin explicar o presión para aprobar rápido. Tus derechos como consumidor están protegidos en Panamá.")]),
 ("calendario-de-mantenimiento-de-electrodomesticos", "Calendario de mantenimiento de electrodomésticos del hogar", "Qué revisar cada mes, cada seis meses y cada año en refrigeradora, lavadora, secadora, aire y cocina.", [
   ("Cada mes", "Lava los filtros del aire acondicionado, limpia el filtro de pelusa de la secadora y revisa el empaque de la refrigeradora."),
   ("Cada seis meses", "Limpia el condensador detrás o debajo de la refrigeradora, el filtro de la bomba de la lavadora y cambia el filtro de agua si tu refrigeradora lo tiene."),
   ("Cada año", "Limpia el ducto de la secadora, revisa mangueras de la lavadora y lava el drenaje del aire acondicionado."),
   ("Cada cinco años", "Cambia las mangueras de entrada de la lavadora y revisa las conexiones de gas de la cocina.")]),
 ("como-proteger-tus-electrodomesticos-de-picos-de-voltaje", "Cómo proteger tus electrodomésticos de los picos de voltaje", "Diferencia entre regleta, supresor y protector de voltaje, y qué equipos necesitan protección en Panamá.", [
   ("Regleta no es protector", "Una regleta común solo multiplica tomas. Un supresor de picos absorbe sobretensiones breves. Un protector de voltaje corta si el voltaje sube o baja demasiado."),
   ("Qué equipos lo necesitan", "Refrigeradoras con compresor inverter, aires acondicionados, lavadoras de carga frontal y televisores."),
   ("Retardo de reconexión", "Para equipos con compresor, elige uno con retardo de unos minutos al volver la luz."),
   ("Tierra y breakers", "Un buen sistema de tierra y breakers adecuados completan la protección. Pide a un electricista revisar la instalación.")]),
 ("olores-en-electrodomesticos-causas-y-soluciones", "Olores en electrodomésticos: causas y soluciones", "Por qué huele mal tu lavadora, refrigeradora o lavavajillas y cómo corregirlo con limpieza y ventilación.", [
   ("Lavadora con olor a humedad", "Detergente acumulado y empaque húmedo favorecen el moho. Deja la puerta entreabierta tras cada uso y limpia el empaque."),
   ("Refrigeradora con mal olor", "Alimentos olvidados o el drenaje del descongelado tapado. Limpia el interior y el desagüe."),
   ("Lavavajillas con olor", "El filtro con restos de comida. Límpialo con regularidad y corre un ciclo caliente vacío."),
   ("Si el olor es a quemado", "Apaga y desconecta el equipo. Puede ser una falla eléctrica o una pieza sobrecalentada.")]),
 ("mudanza-de-electrodomesticos-como-moverlos-sin-danarlos", "Mudanza de electrodomésticos: cómo moverlos sin dañarlos", "Cómo preparar refrigeradora, lavadora y aire acondicionado para una mudanza y cuánto esperar antes de volver a conectarlos.", [
   ("Refrigeradora", "Vacíala, descongélala y transpórtala en posición vertical. Al llegar, espera varias horas antes de enchufarla para que el aceite del compresor se asiente."),
   ("Lavadora", "Retira mangueras, drena el agua y coloca los seguros de transporte si el equipo los trae."),
   ("Aire acondicionado", "La desinstalación y recuperación del gas debe hacerla un técnico; no desconectes las tuberías por tu cuenta."),
   ("Al instalar", "Nivela el equipo, revisa el voltaje y prueba un ciclo antes de cargar ropa o alimentos.")]),
 ("humedad-en-casa-y-electrodomesticos-lo-que-debes-saber", "Humedad en casa y electrodomésticos: lo que debes saber", "Cómo la humedad de Panamá afecta placas, contactos y empaques, y qué hábitos reducen las fallas.", [
   ("Qué hace la humedad", "Corroe contactos, favorece moho en empaques y puede causar falsos contactos en placas."),
   ("Zonas más afectadas", "Cerca del mar, en sótanos o cuartos sin ventilación, y en áreas de lavado."),
   ("Hábitos que ayudan", "Ventilar, mantener los equipos separados de la pared y limpiar condensadores y filtros con regularidad."),
   ("Señales de alerta", "Códigos de error intermitentes, olores y manchas de óxido cerca de conexiones.")]),
]
GLOSARIO = [("Compresor", "Pieza que mueve el gas refrigerante en neveras y aires."), ("Inverter", "Tecnología que ajusta la velocidad del compresor o del motor para ahorrar energía."), ("Evaporador", "Serpentín donde el refrigerante absorbe calor y enfría el aire."), ("Condensador", "Serpentín donde el refrigerante libera calor; suele estar atrás o abajo de la refrigeradora."), ("No frost", "Sistema que evita la escarcha mediante ciclos de deshielo automático."), ("Resistencia de deshielo", "Elemento que derrite el hielo del evaporador."), ("Termostato", "Sensor que controla la temperatura."), ("Presostato", "Sensor de nivel de agua de la lavadora."), ("Bomba de drenaje", "Saca el agua de la lavadora o el lavavajillas."), ("Rodamiento", "Pieza que permite girar al tambor de la lavadora."), ("Amortiguador", "Reduce la vibración de la lavadora al centrifugar."), ("Electroválvula", "Válvula eléctrica que deja entrar el agua."), ("Magnetrón", "Pieza que genera las microondas en un microondas."), ("Placa de control", "Tarjeta electrónica que gobierna el equipo."), ("Relé", "Interruptor eléctrico que activa piezas como la resistencia."), ("Bujía", "Pieza que genera la chispa de encendido en estufas a gas."), ("Gas refrigerante", "Fluido que circula en el sistema de frío."), ("Protector de voltaje", "Dispositivo que corta la energía si el voltaje es peligroso."), ("Breaker", "Interruptor automático del tablero eléctrico."), ("Código de error", "Mensaje que muestra el equipo para indicar qué sistema detectó la falla.")]


# ---------------------------------------------------------------- blog, glosario y legales POR MARCA
def _prim(t): 
    return re.split(r"(?<=[.])\s+", t.strip())[0]
def _rx_elec(d, e):
    return re.compile(r"placa|inverter|tarjeta|control|electr|sensor|pantalla", re.I)
def arts_marca(m):
    d = M[m]; N = nom(m); E = d["equipos"]; pls = lambda es: junta(EQ[e][2] for e in es)
    A = []   # (slug, titulo, descripcion, [(h, html)])
    def lk(e): return f'<p><a href="{pathb(m, "reparacion-" + EQ[e][0])}">Ver reparación de {EQ[e][2]} {N}</a></p>'
    # 1 humedad y salitre
    rxh = re.compile(r"placa|tarjeta|inverter|contacto|empaque|corros|comunicaci|moho|pantalla|conector|cableado", re.I)
    eh = [(e, [x for x in d["fallas"][e] if rxh.search(x[1] + " " + x[0])]) for e in E]
    eh = [(e, fs) for e, fs in eh if fs]
    intro_h = CFG.get("intro_clima") or ("En Panamá la humedad es alta casi todo el año y cerca del mar se suma el salitre." if CFG["costero"] else f"En {CFG['ciudad']} el calor es constante y la humedad sube en las épocas de lluvia.")
    sec_h = [(("Qué hacen la altura y la humedad en tus equipos " if CFG.get("frio") else "Qué hace la humedad en tus equipos ") + N, f"<p>{intro_h} La humedad corroe contactos y placas, favorece el moho en empaques y causa falsos contactos. En equipos {N} esto se nota sobre todo en {pls([e for e, _ in eh[:3]]) if eh else pls(E[:3])}.</p>")]
    for e, fs in eh[:5]:
        f = fs[0]
        sec_h.append((f"{EQ[e][2].capitalize()} {N} y la humedad", f"<p><b>Falla que puede aparecer:</b> {esc(f[0].rstrip('.'))}. <b>Causa probable:</b> {esc(bajar(f[1]))}</p><p><b>Qué hace el técnico:</b> {esc(f[2])}</p>" + lk(e)))
    sec_h.append(("Qué puedes hacer", "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in d["mantenimiento"][:4]) + "</ul>"))
    A.append((f"{CFG['guia_humedad'][0]}-{m}", CFG["guia_humedad"][1].format(N=N), CFG["guia_humedad"][2].format(N=N), sec_h))
    # 2 voltaje y tormentas
    rx = re.compile(r"placa|inverter|tarjeta|control|electr|sensor|pantalla", re.I)
    ev = [e for e in E if rx.search(d["tech"][e] + " ".join(x[1] for x in d["fallas"][e]))]
    if ev:
        sv = [("Por qué importa el voltaje en equipos " + N, f"<p>Las tormentas eléctricas y los apagones generan picos de voltaje. En equipos {N}, los más sensibles son {pls(ev[:4])}, porque dependen de placas y sensores electrónicos.</p>")]
        for e in ev[:4]:
            f = next((x for x in d["fallas"][e] if rx.search(x[1] + x[0])), d["fallas"][e][0])
            sv.append((f"{EQ[e][2].capitalize()} {N}", f"<p><b>Falla que vemos:</b> {esc(f[0].rstrip('.'))}. <b>Causa probable:</b> {esc(bajar(f[1]))}</p><p><b>Qué hace el técnico:</b> {esc(f[2])}</p>" + lk(e)))
        sv.append(("Cómo protegerlos", "<p>Usa un protector de voltaje con retardo de reconexión en los equipos con compresor o placa electrónica, y pide revisar la instalación eléctrica si los picos son frecuentes.</p>"))
        A.append((f"voltaje-y-tormentas-equipos-{m}", f"Voltaje y tormentas: protege tus equipos {N}", f"Qué equipos {N} sufren más los picos de voltaje en Panamá y cómo proteger sus placas y compresores.", sv))
    # 3 reparar o cambiar
    nv = lambda t: "Alto" if re.search(r"placa|tarjeta|compresor|inverter|bobina|magnetr|transmisi|rodamiento|control", t.lower()) else ("Bajo" if re.search(r"filtro|limpi|ajuste|manguera|buj|empaque|sello|llave|carga|grasa", t.lower()) else "Medio")
    bajos = [(EQ[e][1], x[0]) for e in E for x in d["fallas"][e] if nv(x[1]) == "Bajo"][:5]
    altos = [(EQ[e][1], x[0]) for e in E for x in d["fallas"][e] if nv(x[1]) == "Alto"][:5]
    sr = [("Fallas de equipos " + N + " que suelen convenir reparar", "<ul>" + "".join(f"<li>{esc(a.capitalize())} {N}: {esc(bajar(b))}</li>" for a, b in bajos) + "</ul>"),
          ("Fallas que conviene evaluar con calma", "<ul>" + "".join(f"<li>{esc(a.capitalize())} {N}: {esc(bajar(b))}</li>" for a, b in altos) + "</ul>"),
          (f"Garantía y repuestos de {N}", f"<p>{esc(d['garantia'])}</p><p>{N} es una marca de {d['pais']}: filtros, bombas, sensores y empaques suelen conseguirse en Panamá; placas y compresores pueden requerir pedido, y eso alarga la reparación.</p>")]
    A.append((f"reparar-o-cambiar-equipos-{m}", f"¿Reparar o cambiar tu equipo {N}?", f"Cómo decidir si reparar o reemplazar un equipo {N}: fallas que valen la pena, costos relativos, garantía y repuestos.", sr))
    # 4 elegir servicio técnico
    st = [("Qué preguntar antes de contratar", f"<p>Para un equipo {N}, pregunta si el técnico conoce las líneas {', '.join(d['lineas'][:4])}, si trabaja con repuestos originales o compatibles y si entrega el valor por escrito después del diagnóstico.</p>"),
          ("Señales de un buen servicio", "<ul><li>Diagnóstico antes de dar precio.</li><li>Valor de repuesto y mano de obra por escrito.</li><li>Garantía escrita de la reparación.</li><li>Te explica la causa en palabras simples.</li></ul>"),
          ("Señales de alerta", "<p>Pagos completos por adelantado, ninguna factura, piezas sin explicar o presión para aprobar rápido.</p>"),
          ("Lo que haces tú", f"<p>Ten a mano el modelo del equipo {N}: {esc(d['modelo_ej'])}</p>")]
    A.append((f"como-elegir-servicio-tecnico-{m}", f"Cómo elegir un servicio técnico {N} de confianza", f"Qué preguntar y qué evitar al contratar un servicio técnico para equipos {N} en Panamá.", st))
    # 5 olores
    eo = [e for e in E if e in ("lavadoras", "neveras", "lavavajillas", "cocinas", "microondas", "batidoras", "secadoras")]
    if eo:
        so = [("Olores en equipos " + N, f"<p>Un olor raro en un equipo {N} casi siempre tiene una causa simple: humedad, restos de comida o suciedad en filtros y drenajes. Si huele a quemado, apaga y desconecta de inmediato.</p>")]
        tx = {"lavadoras": "Moho en el empaque y detergente acumulado. Deja la puerta entreabierta tras cada uso y limpia el empaque.", "neveras": "Alimentos olvidados o el drenaje del descongelado tapado. Limpia el interior y el desagüe.", "lavavajillas": "Restos de comida en el filtro. Límpialo con regularidad y corre un ciclo caliente vacío.", "cocinas": "Grasa acumulada o restos en quemadores. Si huele a gas, cierra la llave y ventila: es una emergencia.", "microondas": "Restos de comida en el interior. Límpialo con un paño húmedo y vinagre diluido.", "batidoras": "Grasa vieja de la caja de engranes. Se limpia y se repone.", "secadoras": "Pelusa acumulada o ducto con humedad. Limpia filtro y ducto."}
        for e in eo[:4]: so.append((f"{EQ[e][2].capitalize()} {N} con mal olor", f"<p>{esc(tx.get(e, ""))}</p>" + lk(e)))
        A.append((f"olores-en-equipos-{m}", f"Olores en equipos {N}: causas y soluciones", f"Por qué huele mal tu {EQ[eo[0]][1]} {N} u otros equipos de la marca y cómo corregirlo.", so))
    # 6 mudanza
    sm = [("Mudar equipos " + N, f"<p>Antes de mover equipos {N} prepara cada uno según su tipo y evita conectarlo de inmediato al llegar.</p>")]
    mu = {"neveras": "Vacíala, descongélala y transpórtala en vertical. Espera varias horas antes de enchufarla.", "lavadoras": "Retira mangueras, drena el agua y coloca los seguros de transporte si los trae.", "secadoras": "Desconecta el ducto, limpia el filtro y asegura la puerta.", "aires": "La desinstalación y la recuperación del gas las hace un técnico; no desconectes las tuberías por tu cuenta.", "cocinas": "Cierra el gas, desconecta la manguera y retira parrillas sueltas.", "lavavajillas": "Drena el agua, retira mangueras y asegura los racks.", "centro-lavado": "Desarma la unión de la torre con ayuda de dos personas y asegura el tambor.", "batidoras": "Guarda el tazón y los batidores aparte y transporta la base en su caja.", "microondas": "Retira el plato giratorio y asegura la puerta."}
    for k, e in enumerate(E[:6]): sm.append((f"{EQ[e][2].capitalize()} {N}", f"<p>{esc(oracion(d['tech'][e], k))}</p><p>{esc(mu.get(e, ""))}</p><p><b>Etiqueta del modelo:</b> {esc(d['etiqueta'].get(e, 'en el cuerpo del equipo'))}</p><p><b>Lo primero que revisamos al instalarla:</b> {esc(bajar(d['fallas'][e][-1][0]).rstrip('.'))}: {esc(bajar(d['fallas'][e][-1][2]))}</p>"))
    A.append((f"mudanza-de-equipos-{m}", f"Mudanza de equipos {N}: cómo moverlos sin dañarlos", f"Cómo preparar y mover tus equipos {N} en una mudanza y cuándo volver a conectarlos.", sm))
    # 7 aire lluvioso
    if "aires" in E:
        A.append((f"aire-acondicionado-{m}-epoca-lluviosa", f"Aire acondicionado {N} en época lluviosa", f"Qué revisar en tu aire acondicionado {N} antes y durante las lluvias en Panamá.", [("Qué cuidar", f"<p>{esc(d['tech']['aires'])}</p>"), ("Cada mes", "<p>Lava los filtros. Un filtro sucio reduce el aire frío y hace trabajar más al compresor.</p>"), ("Drenaje y unidad exterior", "<p>Mantén el drenaje despejado y la unidad exterior sin hojas ni polvo, protegida de la lluvia directa.</p>"), ("Fallas que vemos", "<ul>" + "".join(f"<li>{esc(x[0])}: {esc(bajar(x[1]).rstrip('.'))}. Se revisa: {esc(bajar(x[2]))}</li>" for x in d['fallas']['aires'][:4]) + "</ul>" + lk("aires")), (f"Dónde está el modelo de tu aire {N}", f"<p>{esc(d['etiqueta'].get('aires', 'La etiqueta está en el cuerpo del equipo.'))}</p>")]))
    # 8 inverter / compresor
    if any("inverter" in d["tech"][e].lower() for e in E):
        ei = [e for e in E if "inverter" in d["tech"][e].lower()]
        rxi = re.compile(r"inverter|compresor|placa", re.I)
        bl = [("Qué es", "<p>Un compresor o motor inverter ajusta su velocidad según la necesidad, en lugar de encenderse y apagarse. Ahorra energía y hace menos ruido.</p>")]
        for e in ei[:3]:
            f = next((x for x in d["fallas"][e] if rxi.search(x[0] + " " + x[1])), None)
            bl.append((f"{EQ[e][2].capitalize()} {N} con tecnología inverter", f"<p>{esc(d['tech'][e])}</p>" + (f"<p><b>Falla ligada:</b> {esc(f[0].rstrip('.'))}. {esc(f[1])}</p>" if f else "") + lk(e)))
        bl.append(("Cómo cuidarla", "<p>Usa un protector de voltaje con retardo de reconexión, deja ventilación libre y limpia el condensador.</p>"))
        A.append((f"tecnologia-inverter-{m}", f"Tecnología inverter en equipos {N}: qué es y cómo cuidarla", f"Qué significa inverter en tus equipos {N}, qué ventajas da y por qué necesita protección de voltaje.", bl))
    # 9 apagón y nevera
    if "neveras" in E:
        rxa = re.compile(r"placa|inverter|compresor|pantalla|c[oó]digo|se apaga|arranca|reinicia|sensor|control", re.I)
        fa = [x for x in d["fallas"]["neveras"] if rxa.search(x[0] + " " + x[1])]
        A.append((f"apagon-y-refrigeradora-{m}", f"Apagón y tu refrigeradora {N}: qué hacer", f"Qué hacer con los alimentos y con tu refrigeradora {N} durante y después de un apagón.", [("Durante el apagón", "<p>No abras la puerta sin necesidad: cerrada mantiene el frío unas horas, y el congelador lleno, más tiempo.</p>"), ("Al volver la luz", "<p>Espera unos minutos antes de reconectar. Un compresor que arranca de golpe junto con un pico de voltaje puede dañar la placa electrónica.</p>"), ("Si algo falla después del apagón", "<ul>" + "".join(f"<li><b>{esc(x[0].rstrip('.'))}:</b> {esc(bajar(x[1]))}</li>" for x in fa[:3]) + "</ul>" + lk("neveras") if fa else "<p>Si la refrigeradora no enfría o muestra un código tras el apagón, desconéctala unos minutos y llama si persiste.</p>" + lk("neveras"))]))
    # 10 instalación
    si = [("Instalar equipos " + N + " nuevos", f"<p>Una buena instalación evita fallas en el primer año. Confirma el voltaje, nivela y deja ventilación.</p>")]
    for e in E[:5]: si.append((f"{EQ[e][2].capitalize()} {N}", f"<p><b>Dónde está el modelo:</b> {esc(d['etiqueta'].get(e, 'en el cuerpo del equipo'))}</p><p>{esc(_prim(d['tech'][e]))}</p>"))
    A.append((f"instalar-equipos-{m}-nuevos", f"Cómo instalar bien un equipo {N} nuevo", f"Nivelación, voltaje y ventilación: lo que debes revisar al instalar un equipo {N} nuevo en Panamá.", si))
    return A
def build_blog(m):
    d = M[m]; N = nom(m); crumbs0 = [(f"Centro de Servicio Técnico {N} Panamá", base(m))]
    A = [a for a in arts_marca(m) if not a[0].startswith(("olores", "como-elegir", "mudanza", "instalar", "apagon")) and not (a[0].startswith("tecnologia-inverter") and m in ("haceb", "frigidaire", "kitchenaid"))]; ART[m] = [(s, t) for s, t, _, _ in A]
    for slg, t, desc, bl in A:
        cuerpo = sec(t, "".join(f"<h3>{esc(h)}</h3>{b if b.startswith('<') else '<p>' + esc(b) + '</p>'}" for h, b in bl)) 
        pagina(pathb(m, "guia-" + slg), t[:62], desc, t, cuerpo, m, (elegir(m, m + slg, 1) or [None])[0], crumbs0 + [("Guías", pathb(m, "guias")), (t[:45], pathb(m, "guia-" + slg))],
               [{"@type": "Article", "headline": t, "description": desc, "datePublished": HOY, "dateModified": HOY, "author": {"@id": DOM + "/#negocio"}, "publisher": {"@id": DOM + "/#negocio"}, "inLanguage": CFG["locale"]}], bd=f"{N} · Guía", prio="0.6", lead=desc)
    pagina(pathb(m, "guias"), (f"Blog de consejos para equipos {N} en Panamá" if CFG.get("lbl_guias") else f"Guías y consejos para equipos {N} en Panamá"), f"Blog de consejos y guías prácticas para equipos {N} en Panamá: humedad, voltaje, mantenimiento, reparar o cambiar y cuidado diario.", (f"Blog de consejos {N}" if CFG.get("lbl_guias") else f"Guías y consejos para equipos {N}"),
           sec(f"Guías {N}", '<div class="g c2">' + "".join(f'<a class="card l" href="{pathb(m, "guia-" + s_)}"><span class="t">{esc(t_)}</span></a>' for s_, t_ in ART[m]) + '</div>') , m, (elegir(m, m + "guias", 1) or [None])[0], crumbs0 + [("Guías", pathb(m, "guias"))], bd=f"{N} · Guías", prio="0.6", lead=f"Consejos concretos para cuidar tus equipos {N}.", noindex=not CFG.get("lbl_guias"))
ART = {}
GL_EQ = {"neveras": ["Compresor", "Inverter", "Evaporador", "Condensador", "No frost", "Resistencia de deshielo", "Termostato", "Gas refrigerante"], "lavadoras": ["Presostato", "Bomba de drenaje", "Rodamiento", "Amortiguador", "Electroválvula"], "secadoras": ["Termostato", "Condensador", "Relé"], "aires": ["Compresor", "Inverter", "Gas refrigerante", "Evaporador", "Condensador"], "cocinas": ["Bujía", "Termostato", "Relé"], "lavavajillas": ["Bomba de drenaje", "Electroválvula"], "microondas": ["Magnetrón"], "centro-lavado": ["Presostato", "Bomba de drenaje", "Relé"], "batidoras": ["Relé"]}
def build_glosario(m):
    d = M[m]; N = nom(m); crumbs0 = [(f"Centro de Servicio Técnico {N} Panamá", base(m))]
    gd = dict(GLOSARIO); alltxt = " ".join(d["tech"].values())
    sents = [x for x in re.split(r"(?<=[.])\s+", alltxt) if not re.match(r"(Esa|Eso|Esto|Esta|Estas|Esos|Ese)\b", x)]
    cand = []
    for e in d["equipos"]:
        for t in GL_EQ.get(e, []):
            if t not in cand: cand.append(t)
    items = []; usados = []; yaus = set()
    for t in cand + ["Placa de control", "Código de error", "Protector de voltaje"]:
        key = {"No frost": "no frost", "Resistencia de deshielo": "deshielo", "Gas refrigerante": "gas", "Bomba de drenaje": "bomba", "Código de error": "código", "Protector de voltaje": "voltaje", "Placa de control": "placa"}.get(t, t.lower())
        ctx = sorted([x for x in sents if re.search(r"\b" + re.escape(key), x.lower()) and x not in yaus], key=len)
        ctx = [x for x in ctx if len(x) < 230][:1]
        if not ctx and t not in ("Código de error", "Protector de voltaje"): continue
        for x in ctx: yaus.add(x)
        usados.append(t)
        items.append(f"<details><summary>{esc(t)}</summary><p>{esc(gd.get(t, ''))}" + (f" <b>En {N}:</b> {esc(ctx[0])}" if ctx else "") + "</p></details>")
    cod = ""
    if d["codigos"]:
        cod = "".join(f"<h3>Códigos de error {N}: {g}</h3>" + tabla(["Código", "Qué suele indicar"], [(f'<span class="cb">{c}</span>', esc(t)) for c, t in L]) for g, L in d["codigos"].items())
    pagina(pathb(m, "glosario"), f"Glosario de equipos {N}: términos explicados", f"Glosario con los términos que escuchas al reparar equipos {N}: {', '.join(usados[:5])} y más, con ejemplos de la marca.", f"Glosario de equipos {N}",
           sec(f"Términos de reparación de equipos {N}", "".join(items) + "<h3 style='margin-top:18px'>Líneas " + N + "</h3>" + "".join(f'<span class="pill">{esc(x)}</span>' for x in d["lineas"]) + cod),
           m, (elegir(m, m + "glos", 1) or [None])[0], crumbs0 + [("Glosario", pathb(m, "glosario"))], [{"@type": "DefinedTermSet", "name": f"Glosario {N}", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": gd.get(t, "")} for t in usados]}], bd=f"{N} · Glosario", prio="0.5", lead=f"Los términos técnicos de tus equipos {N}, con ejemplos de la marca.")
def junta(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " y " + xs[-1]
def pls_(d): return junta(EQ[e][2] for e in d["equipos"])
def build_legal(m):
    d = M[m]; N = nom(m); crumbs0 = [(f"Centro de Servicio Técnico {N} Panamá", base(m))]
    pagina(pathb(m, "quienes-somos"), f"Quiénes somos | Servicio técnico {N} Panamá", f"Quiénes somos: servicio técnico independiente de equipos {N} a domicilio en Panamá.", f"Quiénes somos: servicio técnico {N} en Panamá",
           sec(f"Un servicio técnico independiente para equipos {N}", f"<p>Reparamos a domicilio en Panamá equipos {N}: {pls_(d)}. Somos un servicio técnico independiente: no somos el fabricante de {N}, y el nombre de la marca se usa solo para indicar qué equipos reparamos.</p><p>{esc(d['origen'])}</p>") + sec("Cómo trabajamos", PASOS, alt=True) + sec("Contacto", f"<p>WhatsApp y teléfono: <a href=\"tel:+{TELN}\">{TEL}</a>.</p>"),
           m, (elegir(m, m + "qs", 1) or [None])[0], crumbs0 + [("Quiénes somos", pathb(m, "quienes-somos"))], bd=f"{N} · Nosotros", prio="0.5", noindex=True, lead=f"Quiénes somos y cómo reparamos tus equipos {N}.")
    pagina(pathb(m, "politica-de-privacidad"), f"Política de privacidad | {N} Panamá", f"Política de privacidad del servicio técnico {N} en Panamá: datos que recibimos, uso y tus derechos (Ley 81 de 2019).", f"Política de privacidad del servicio técnico {N}",
           sec("Datos personales", f"<p>Cuando nos escribes por WhatsApp o teléfono para reparar un equipo {N} recibimos tu nombre, número, zona y datos del equipo. Los usamos solo para coordinar la visita.</p><p>No vendemos tus datos. Puedes pedirnos que los corrijamos o eliminemos por el mismo número de contacto. Esta política se rige por la Ley 81 de 2019 de Panamá. Última actualización: noviembre de 2026.</p>"),
           m, None, crumbs0 + [("Privacidad", pathb(m, "politica-de-privacidad"))], bd=f"{N} · Legal", prio="0.3", noindex=True)
    pagina(pathb(m, "terminos-y-condiciones"), f"Términos y condiciones | {N} Panamá", f"Términos y condiciones del servicio técnico {N} en Panamá: diagnóstico, valores, garantía de la reparación y derechos del consumidor.", f"Términos y condiciones del servicio {N}",
           sec("Condiciones del servicio", f"<p>El valor del diagnóstico y de la reparación de tu equipo {N} se informa antes de empezar y solo se repara con tu aprobación. Cada reparación incluye garantía sobre la pieza y la mano de obra, con plazo por escrito.</p><p>Somos un servicio técnico independiente y no representamos a {N}; la garantía de fábrica es del fabricante o vendedor. Tus derechos como consumidor están protegidos por la Ley 45 de 2007 de Panamá. Última actualización: noviembre de 2026.</p>"),
           m, None, crumbs0 + [("Términos", pathb(m, "terminos-y-condiciones"))], bd=f"{N} · Legal", prio="0.3", noindex=True)

# ---------------------------------------------------------------- zonas, institucionales, blog
def build_sitio():
    (OUT / "404.html").write_text(f'<!doctype html><html lang="es"><meta charset="utf-8"><title>Página no encontrada</title><meta name="robots" content="noindex"><body style="font-family:system-ui;padding:40px"><h1>Página no encontrada</h1><p><a href="/">Ir al inicio</a></p></body></html>', encoding="utf-8")

# ---------------------------------------------------------------- sitemaps, robots, llms
def tecnico():
    def sm(items):
        def im(p):
            f = (OUT / p.lstrip("/") / "index.html") if p != "/" else OUT / "index.html"
            t = f.read_text(encoding="utf-8") if f.exists() else ""
            salida = {}
            for m_ in re.finditer(r'<img[^>]*?src="(/img/(?!logos/)[^"]+)"[^>]*?alt="([^"]*)"', t): salida.setdefault(m_.group(1), m_.group(2))
            for u in re.findall(r'url\((/img/[^)]+)\)', t): salida.setdefault(u, "")
            return "".join(f"<image:image><image:loc>{DOM}{u}</image:loc>" + (f"<image:caption>{a_}</image:caption>" if a_ else "") + "</image:image>" for u, a_ in salida.items())
        return '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">' + "".join(f"<url><loc>{DOM}{p}</loc><lastmod>{HOY}</lastmod><priority>{pr}</priority>{im(p)}</url>" for p, pr, _ in items) + "</urlset>"
    idx = []
    for m in BRANDS_ORDER:
        it = [x for x in paginas if x[2] == m]; (OUT / f"sitemap-{m}.xml").write_text(sm(it)); idx.append(f"sitemap-{m}.xml")
    it = [x for x in paginas if x[2] is None]
    if it: (OUT / "sitemap-principal.xml").write_text(sm(it)); idx.append("sitemap-principal.xml")
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<sitemap><loc>{DOM}/{i}</loc><lastmod>{HOY}</lastmod></sitemap>" for i in idx) + "</sitemapindex>")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {DOM}/sitemap.xml\n")
    L = [f"# {NOMBRE}", f"> Servicio técnico independiente de {"pantallas" if CFG.get("tv") else "electrodomésticos"} a domicilio en {CFG['ciudad']}. WhatsApp {TEL}.", "", "## Marcas"]
    for m in BRANDS_ORDER: L.append(f"- [Centro de Servicio Técnico {nom(m)} {CFG['ciudad']}]({DOM}{base(m)}): {', '.join(EQ[e][2] for e in M[m]['equipos'])}.")
    L += ["", "## Contenido por marca", "Cada marca tiene su propio blog, glosario, zonas, repuestos y garantía dentro de su carpeta."]
    (OUT / "llms.txt").write_text("\n".join(L) + "\n")

REL_GUIAS = {"neveras": ["voltaje-y-tormentas", "tecnologia-inverter", "humedad", "reparar-o-cambiar"], "lavadoras": ["humedad", "voltaje-y-tormentas", "tecnologia-inverter", "reparar-o-cambiar"],
             "secadoras": ["voltaje-y-tormentas", "reparar-o-cambiar", "humedad"], "aires": ["aire-acondicionado", "tecnologia-inverter", "voltaje-y-tormentas", "humedad"],
             "cocinas": ["voltaje-y-tormentas", "reparar-o-cambiar", "humedad"], "lavavajillas": ["reparar-o-cambiar", "voltaje-y-tormentas", "humedad"],
             "centro-lavado": ["reparar-o-cambiar", "voltaje-y-tormentas", "humedad"], "microondas": ["reparar-o-cambiar", "voltaje-y-tormentas"], "batidoras": ["reparar-o-cambiar", "humedad"]}
def repartir_fotos():
    """Segunda pasada (Guayaquil): cada foto de la marca que aún no aparece en ninguna página se coloca, completa, en una franja de la página que le corresponde."""
    if not CFG.get("sin_recorte"): return
    for m in BRANDS_ORDER:
        carp = OUT / ("samsung" if m == "samsung" else m)
        paginas_m = [OUT / "index.html"] if m == "samsung" else [carp / "index.html"]
        paginas_m += sorted(carp.glob("*/index.html"))
        usadas = set()
        for p in paginas_m: usadas |= set(re.findall(r"/img/%s/[^\"')\s]+" % m, p.read_text(encoding="utf-8")))
        sobran = [f for f in POOLS[m] if copia(m, f) not in usadas]
        if not sobran: continue
        rg = re.compile(KW["_gente"]); por_eq = collections.defaultdict(list); resto = []
        for f in sobran:
            for e in M[m]["equipos"]:
                if re.search(KW[e], f.name) and not rg.search(f.name): por_eq[e].append(f); break
            else: resto.append(f)
        def franja(fs):
            figs = ""
            for f in fs:
                w, h = _dim(f); figs += f'<figure><img loading="lazy" src="{copia(m, f)}" alt="{alt_de(m, f)}" width="{w}" height="{h}"></figure>'
            return f'<section class="s alt"><div class="w"><div class="fgrid">{figs}</div></div></section>'
        def poner(p, fs):
            t = p.read_text(encoding="utf-8")
            ancla = '<div class="w"><p class="upd">' if '<div class="w"><p class="upd">' in t else "<!--cierre-->"
            if ancla not in t: return False
            p.write_text(t.replace(ancla, franja(fs) + ancla, 1), encoding="utf-8"); return True
        def lotes(lst):
            out = [lst[i:i + 3] for i in range(0, len(lst), 3)]
            if len(out) > 1 and len(out[-1]) == 1: out[-2] += out.pop()
            return out
        for e, fs in por_eq.items():
            destinos = [carp / ("reparacion-" + EQ[e][0]) / "index.html"] + [x for x in sorted(carp.glob("falla-*/index.html")) if x.parent.name.startswith("falla-" + slug(EQ[e][1]))]
            ls = lotes(fs) if len(fs) > 1 else []
            if len(fs) == 1: resto += fs
            for lote, dpath in zip(ls, destinos):
                if not poner(dpath, lote): resto += lote
            resto += [f for l in ls[len(destinos):] for f in l]
        orden = [paginas_m[0]] + [carp / s / "index.html" for s in ("quienes-somos", "telefono-servicio-tecnico", "reparacion-a-domicilio", "garantia", "cuanto-cuesta-la-reparacion", "series-y-modelos", "repuestos", "centro-de-servicio-cerca-de-mi", "preguntas-frecuentes", "diagnostico-por-sintoma", "glosario")]
        orden += sorted(carp.glob("guia-*/index.html")) + sorted(carp.glob("servicio-tecnico-*/index.html")) + sorted(carp.glob("falla-*/index.html"))
        pend = lotes(resto) if len(resto) > 1 else ([resto] if resto else [])
        k = 0
        for dpath in orden:
            if k >= len(pend): break
            if dpath.exists() and poner(dpath, pend[k]): k += 1

def relacionadas():
    """Segunda pasada: enlaza cada página de equipo con las guías de su marca que existen y le sirven."""
    for m in BRANDS_ORDER:
        carp = OUT / ("samsung" if m == "samsung" else m)
        guias = {p.name: p for p in carp.glob("guia-*") if (p / "index.html").exists()}
        for e in M[m]["equipos"]:
            f = carp / ("reparacion-" + EQ[e][0]) / "index.html"
            if not f.exists(): continue
            t = f.read_text(encoding="utf-8")
            items = []
            for clave in REL_GUIAS.get(e, []):
                for nombre in guias:
                    if clave in nombre and nombre != "guia-de-cuidado":
                        h1 = re.search(r"<h1>(.*?)</h1>", (guias[nombre] / "index.html").read_text(encoding="utf-8"))
                        if h1: items.append((pathb(m, nombre), h1.group(1))); break
            if (carp / "guia-de-cuidado" / "index.html").exists(): items.append((pathb(m, "guia-de-cuidado"), f"Guía de cuidado {nom(m)}"))
            items = items[:5]
            bloque = (sec(f"Guías relacionadas con tu {EQ[e][1]} {nom(m)}", '<div class="g c2">' + "".join(f'<a class="card l" href="{u}"><span class="t">{n}</span></a>' for u, n in items) + "</div>", alt=True) if items else "")
            f.write_text(t.replace(f"<!--REL:{e}-->", bloque), encoding="utf-8")
            enl = items[:3]
            blq = (sec(f"Guías útiles para tu {EQ[e][1]} {nom(m)}", '<div class="g c3">' + "".join(f'<a class="card l" href="{u}"><span class="t">{n}</span></a>' for u, n in enl) + "</div>", alt=True) if enl else "")
            for ff in carp.glob("falla-*/index.html"):
                tt = ff.read_text(encoding="utf-8")
                if f"<!--RELF:{e}-->" in tt: ff.write_text(tt.replace(f"<!--RELF:{e}-->", blq), encoding="utf-8")

if CFG.get("tv"):
    PARTES.update(_TV.PARTES); PARTE_DESC.update(_TV.PARTE_DESC); PARTE_DIAG.update(_TV.PARTE_DIAG); EQ_VIDA.update(_TV.EQ_VIDA); GL_EQ.update(_TV.GL_EQ)
    _gl = dict(GLOSARIO); _gl.update(dict(_TV.GLOSARIO_TV)); GLOSARIO = list(_gl.items()) if isinstance(GLOSARIO, list) else _gl
if CFG.get("zx"): ZX = CFG["zx"]
if CFG.get("clima"): CLIMA = CFG["clima"]

if __name__ == "__main__":
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(parents=True); (OUT / "assets").mkdir(); (OUT / "assets" / "site.css").write_text(CSS.replace("\n", " "), encoding="utf-8")
    (OUT / "img" / "logos").mkdir(parents=True, exist_ok=True)
    for m in BRANDS_ORDER:
        for suf in ("", "-blanco"): shutil.copy(pathlib.Path(__file__).parent / "cst_logos" / f"{m}{suf}.png", OUT / "img" / "logos" / f"{m}{suf}.png")
    for m in BRANDS_ORDER: build_marca(m); build_sintomas(m); build_zonas_marca(m); build_guia(m); build_blog(m); build_glosario(m); build_legal(m); build_terminos(m)
    if CFG.get('tv'):
        for m in BRANDS_ORDER: build_tv_extra(m)
    build_sitio(); relacionadas(); repartir_fotos()
    for ff in OUT.rglob("index.html"):
        tt = ff.read_text(encoding="utf-8")
        if "<!--REL" in tt: ff.write_text(re.sub(r"<!--RELF?:[a-z-]+-->", "", tt), encoding="utf-8")
    tecnico()
    for r, ds, fs in os.walk(OUT):
        os.chmod(r, 0o755)
        for f in fs: os.chmod(os.path.join(r, f), 0o644)
    print(len(paginas), "páginas")
