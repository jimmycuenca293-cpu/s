#!/usr/bin/env python3
"""Tienda de kits de instalación para nevecones.
Lee productos.csv (costo, envio, link_pago) y genera site/colombia (kits, envío gratis) y site/cali (kits + instalación).
Precio = (costo + envío + ganancia + comisión fija Wompi) / (1 - % Wompi). Combo: suma de costos de sus piezas + un solo envío (el mayor; 0 si incluye instalación).
Sin costo => "Consultar por WhatsApp". Sin link_pago => botón de WhatsApp con el pedido ya escrito.
Uso: python3 kits.py [dominio_colombia] [dominio_cali]
"""
import csv, html, json, re, shutil, sys, urllib.parse, zipfile
from pathlib import Path
AQUI = Path(__file__).parent
GANANCIA = {"individual": 15000, "servicio": 0, "combo": 25000}   # ganancia limpia por pedido, editable
WOMPI_FIJO, WOMPI_PCT = 700 * 1.19, 0.0265 * 1.19           # comisión Wompi + IVA (aproximada: confírmala en tu panel)
WA = "573013810242"; TEL = "+57 301 381 0242"
esc = lambda s: html.escape(str(s), quote=True)
cop = lambda n: "$ " + f"{int(n):,}".replace(",", ".")
DOMINIO = sys.argv[1] if len(sys.argv) > 1 else "https://filtrosaguanevecones.com"
# carpeta de cada tienda dentro del dominio (no pisa nada de la tienda de filtros)
CARPETA = {"colombia": "kits-instalacion-nevecones", "cali": "kits-instalacion-nevecones-cali"}
DOM = {k: f"{DOMINIO}/{v}" for k, v in CARPETA.items()}

def num(s):
    s = (s or "").strip().replace(".", "").replace("$", "").replace(" ", "")
    return int(s) if s else None

def cargar():
    P = {}
    for r in csv.DictReader(open(AQUI / "productos.csv", encoding="utf-8")):
        r["costo"], r["envio"] = num(r["costo"]), num(r["envio"]) or 0
        r["cali"] = r["solo_cali"].strip() == "1"; r["grupo"] = r.get("grupo") or ""; r["variante"] = r.get("variante") or ""
        r["inc"] = [x for x in r["incluye"].split(";") if x]
        P[r["id"]] = r
    for p in P.values():
        if p["tipo"] == "combo":
            cs = [P[i]["costo"] for i in p["inc"]]
            p["costo"] = None if None in cs else sum(cs)
            p["envio"] = 0 if any(P[i]["tipo"] == "servicio" for i in p["inc"]) else max([P[i]["envio"] for i in p["inc"]] or [0])
        p["precio"] = None if p["costo"] is None else int(round((p["costo"] + p["envio"] + GANANCIA[p["tipo"]] + WOMPI_FIJO) / (1 - WOMPI_PCT) / 500)) * 500
    return P

CSS = """:root{--bg:#f6f8fb;--c:#fff;--t:#14213d;--m:#5b6679;--a:#0b5fff;--a2:#0a3fa8;--ok:#16a34a;--b:#dfe5ee}
@media(prefers-color-scheme:dark){:root{--bg:#0e1420;--c:#172033;--t:#eef2f9;--m:#a3afc4;--a:#6ea0ff;--a2:#9bbcff;--b:#2a3650}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--t);font:16px/1.55 system-ui,sans-serif}
a{color:var(--a)}.w{max-width:1040px;margin:0 auto;padding:0 16px}
header{background:var(--c);border-bottom:1px solid var(--b)}header .w{display:flex;gap:16px;align-items:center;justify-content:space-between;padding:12px 16px;flex-wrap:wrap}
header b{font-size:18px}nav a{margin-right:14px;text-decoration:none;font-weight:600}
.hero{padding:34px 0 18px}h1{font-size:30px;line-height:1.2;margin:0 0 10px}h2{margin:30px 0 12px}
.gr{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px}
.card{background:var(--c);border:1px solid var(--b);border-radius:14px;padding:16px;display:flex;flex-direction:column;gap:8px}
.card h3{margin:0;font-size:17px}.card p{margin:0;color:var(--m);font-size:14px}
.ico.foto{height:130px;background:#fff;gap:6px;padding:6px}.ico.foto img{height:100%;min-width:0;flex:1 1 0;object-fit:contain;max-width:100%}
.ico{height:92px;border-radius:10px;background:linear-gradient(135deg,#dbe8ff,#eef4ff);display:grid;place-items:center;color:#0b5fff}.ico.foto{display:flex}
select{width:100%;padding:10px;border-radius:10px;border:1px solid var(--b);background:var(--c);color:var(--t);font:inherit}.pp{font-size:24px;font-weight:800}.pp small{font-size:13px;font-weight:600;color:var(--ok)}.pr{font-size:24px;font-weight:800}.pr small{font-size:13px;font-weight:600;color:var(--ok)}
.btn{display:inline-block;background:var(--a);color:#fff;padding:11px 16px;border-radius:10px;text-decoration:none;font-weight:700;text-align:center}
.btn.o{background:transparent;color:var(--a);border:2px solid var(--a)}.btn.g{background:#16a34a}
.badge{display:inline-block;background:#e8f7ee;color:#157a3a;border-radius:99px;padding:2px 10px;font-size:12.5px;font-weight:700}
.box{background:var(--c);border:1px solid var(--b);border-radius:14px;padding:18px}
table{width:100%;border-collapse:collapse;background:var(--c);border-radius:12px;overflow:hidden}td,th{padding:10px;border-bottom:1px solid var(--b);text-align:left;font-size:14.5px}
details{background:var(--c);border:1px solid var(--b);border-radius:10px;padding:12px 14px;margin:8px 0}summary{cursor:pointer;font-weight:700}
footer{margin-top:40px;padding:24px 0;border-top:1px solid var(--b);color:var(--m);font-size:14px}
.wa{position:fixed;right:14px;bottom:14px;z-index:9}@media(max-width:560px){h1{font-size:25px}}"""
ICON = '<svg width="54" height="54" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">%s</svg>'
ICONOS = {"manguera-1-4-5m": '<path d="M3 17c4 0 4-10 9-10s5 10 9 10"/>', "llave-galapago": '<circle cx="12" cy="12" r="3"/><path d="M12 3v6M12 15v6M3 12h6M15 12h6"/>',
          "manguera-5-16-5m": '<path d="M3 17c4 0 4-10 9-10s5 10 9 10"/>', "llave-multiproposito": '<path d="M4 12h16M12 12V6m-3 0h6"/>', "acople-rapido-1-4": '<path d="M3 9h6l2 2v2l-2 2H3M21 9h-4l-2 2v2l2 2h4"/>',
          "filtro-externo-samsung": '<rect x="8" y="3" width="8" height="18" rx="3"/><path d="M8 9h8M8 15h8"/>', "filtro-externo-lg": '<rect x="8" y="3" width="8" height="18" rx="3"/><path d="M8 9h8M8 15h8"/>', "filtro-externo-whirlpool": '<rect x="8" y="3" width="8" height="18" rx="3"/><path d="M8 9h8M8 15h8"/>',
          "filtro-externo": '<rect x="8" y="3" width="8" height="18" rx="3"/><path d="M8 9h8M8 15h8"/>', "servicio-instalacion": '<path d="M14 7l3-3 3 3-3 3zM3 21l10-10"/>'}
def ico(p, base="/"):
    ids = [p["id"]] if p["tipo"] != "combo" else list(dict.fromkeys(i for i in p["inc"] if P_[i]["tipo"] != "servicio"))
    fotos = [i for i in ids if (AQUI / "fotos" / f"{i}.jpg").exists()][:3]
    if fotos:
        return '<div class="ico foto">' + "".join(f'<img src="{base}img/{i}.jpg" alt="{esc(P_[i]["nombre"])}" loading="lazy">' for i in fotos) + "</div>"
    k = ICONOS.get(p["id"], '<rect x="4" y="5" width="16" height="14" rx="2"/><path d="M4 11h16"/>')
    return f'<div class="ico">{ICON % k}</div>'

def wa(msg): return f"https://wa.me/{WA}?text=" + urllib.parse.quote(msg)

def comprar(p, cali):
    if p["precio"] is None:
        return f'<a class="btn g" href="{wa("Hola, quiero cotizar: " + p["nombre"])}">Consultar precio por WhatsApp</a>'
    if p["link_pago"].strip():
        return f'<a class="btn" href="{esc(p["link_pago"].strip())}" rel="noopener">Pagar {cop(p["precio"])}</a>'
    ciudad = " Estoy en Cali." if cali else ""
    return f'<a class="btn g" href="{wa("Hola, quiero comprar: " + p["nombre"] + " (" + cop(p["precio"]) + ", envío gratis)." + ciudad)}">Pedir por WhatsApp</a>'

def precio(p, cali):
    if p["precio"] is None: return '<div class="pr">Precio por confirmar</div>'
    return f'<div class="pr">{cop(p["precio"])} <small>envío gratis</small></div>'

def visibles(P, cali):
    return [p for p in P.values() if cali or not p["cali"] and not any(P[i]["cali"] for i in p["inc"])]

def tarjeta(p, cali, base):
    inc = ""
    if p["inc"]:
        inc = "<p>Incluye: " + ", ".join(esc(P_[i]["corto"]) for i in p["inc"] if not P_[i]["cali"] or cali) + (" + instalación" if cali and any(P_[i]["cali"] for i in p["inc"]) else "") + "</p>"
    return f'''<div class="card">{ico(p, base)}<h3><a href="{base}p/{p["id"]}/" style="color:inherit;text-decoration:none">{esc(p["nombre"])}</a></h3>{inc}{precio(p, cali)}{comprar(p, cali)}</div>'''

def tarjeta_grupo(vs, cali, base):
    vs = [v for v in vs]
    datos = [{"m": v["variante"], "p": precio(v, cali), "b": comprar(v, cali), "h": f'{base}p/{v["id"]}/'} for v in vs]
    t = re.sub(r" x \d+ metros.*", "", vs[0]["nombre"]) + " para nevecón"
    ops = "".join(f'<option value="{i}">{esc(v["variante"])}' + (f' · {cop(v["precio"])}' if v["precio"] else "") + "</option>" for i, v in enumerate(vs))
    return f'''<div class="card grupo" data-v="{esc(json.dumps(datos))}">{ico(vs[0], base)}<h3>{esc(t)}</h3><p>Elige cuántos metros necesitas. Más metros, menos pagas por metro, porque el envío es uno solo.</p>
<select aria-label="Metros de manguera">{ops}</select><div class="pp">{datos[0]["p"]}</div><div class="bb">{datos[0]["b"]}</div></div>'''

JS_GRUPO = """<script>document.querySelectorAll('.grupo').forEach(function(c){var d=JSON.parse(c.dataset.v),s=c.querySelector('select');s.addEventListener('change',function(){var v=d[s.value];c.querySelector('.pp').innerHTML=v.p;c.querySelector('.bb').innerHTML=v.b})})</script>"""

def lista_individual(ind, cali, base):
    h, vistos = [], set()
    for p in ind:
        if p["grupo"]:
            if p["grupo"] in vistos: continue
            vistos.add(p["grupo"]); h.append(tarjeta_grupo([v for v in ind if v["grupo"] == p["grupo"]], cali, base))
        else: h.append(tarjeta(p, cali, base))
    return "".join(h)

def pagina(titulo, desc, cuerpo, cali, base, canon, ld=""):
    nav = f'<a href="{base}">Inicio</a><a href="{base}#combos">Combos</a><a href="{base}guia-llaves/">¿Qué llave necesito?</a>' + (f'<a href="{base}#instalacion">Instalación</a>' if cali else "")
    return f'''<!doctype html><html lang="es-CO"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(titulo)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{esc(canon)}">
<style>{CSS}</style>{ld}</head><body>
<header><div class="w"><b>Kits de instalación para nevecón{" · Cali" if cali else ""}</b><nav>{nav}</nav></div></header>
<main class="w">{cuerpo}</main>
<footer><div class="w">Tienda independiente de repuestos e instalación; no somos el fabricante ni servicio técnico oficial de ninguna marca. Envío gratis a toda Colombia. Atención por WhatsApp {TEL}.</div></footer>
<a class="btn g wa" href="{wa("Hola, necesito ayuda con un kit de instalación para mi nevecón")}">WhatsApp</a>{JS_GRUPO}</body></html>'''

FAQ = [("¿Por qué no recorto la manguera?", "Una manguera más corta de lo necesario pierde presión y el dispensador de agua puede fallar. Por eso el kit trae 5 metros: se deja la manguera completa."),
       ("¿Qué llave necesito?", "Depende de tu punto de agua. La llave galápago toma el agua del tubo sin cortarlo y trae racores, anillo y tuerca. Si ya tienes una llave, puedes usar la llave multipropósito y los acoples que haga falta. Mira la guía «¿Qué llave necesito?»."),
       ("¿El envío tiene costo?", "No. El envío es gratis a toda Colombia; ya está incluido en el precio."),
       ("¿Dónde en el filtro va la flecha?", "El filtro externo se instala con la flecha apuntando hacia el nevecón, y después se purga el agua (unos 4 litros) antes de usarla."),
       ("¿Pueden instalarme el nevecón?", "La instalación solo está disponible en Cali. En el resto de Colombia vendemos el kit con envío gratis y tú o tu técnico lo instalan.")]
def faq_html(cali):
    f = FAQ if cali else FAQ[:4] + [FAQ[4]]
    return "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in f)

def sitio(P, cali, out):
    base = "/" + CARPETA["cali" if cali else "colombia"] + "/" ; dom = DOM["cali" if cali else "colombia"].rstrip("/")
    vis = visibles(P, cali)
    ind = [p for p in vis if p["tipo"] == "individual"]; com = [p for p in vis if p["tipo"] == "combo"]
    h = f'''<section class="hero"><span class="badge">Envío gratis a toda Colombia</span><h1>Kit de instalación para nevecón{" en Cali" if cali else ""}</h1>
<p>Manguera de 1/4", llaves, acoples y filtro externo, cada pieza por separado o en combo. {"Si estás en Cali, también instalamos tu nevecón." if cali else "Pagas y te lo enviamos sin costo de envío."}</p></section>
<h2>Productos por separado</h2><div class="gr">{lista_individual(ind, cali, base)}</div>
<h2 id="combos">Combos</h2><div class="gr">{"".join(tarjeta(p, cali, base) for p in com)}</div>'''
    if cali:
        h += '''<h2 id="instalacion">Instalación de nevecones en Cali</h2><div class="box"><p>Bajamos y montamos las puertas, ubicamos y nivelamos el nevecón, lo conectamos al punto de agua (con la manguera sin recortar), cambiamos el filtro y purgamos. Servicio solo en Cali.</p></div>'''
    h += f"<h2>Preguntas frecuentes</h2>{faq_html(cali)}"
    out.mkdir(parents=True, exist_ok=True)
    (out / "img").mkdir(exist_ok=True)
    for f in (AQUI / "fotos").glob("*.jpg"): shutil.copy(f, out / "img" / f.name)
    (out / "index.html").write_text(pagina("Kits de instalación para nevecón" + (" en Cali" if cali else ""), "Manguera de 1/4, llaves galápago, acoples y filtro externo para nevecones, con envío gratis.", h, cali, base, dom + "/"), "utf-8")
    for p in vis:
        d = out / "p" / p["id"]; d.mkdir(parents=True, exist_ok=True)
        inc = ""
        if p["inc"]:
            inc = "<h2>Qué incluye</h2><ul>" + "".join(f'<li><a href="{base}p/{i}/">{esc(P[i]["nombre"])}</a></li>' for i in p["inc"] if cali or not P[i]["cali"]) + "</ul>"
        body = f'<section class="hero"><h1>{esc(p["nombre"])}</h1><p>{esc(p["descripcion"])}</p></section><div class="box">{ico(p, base)}{precio(p, cali)}<p>{comprar(p, cali)}</p></div>{inc}<h2>Preguntas frecuentes</h2>{faq_html(cali)}'
        (d / "index.html").write_text(pagina(p["nombre"], p["descripcion"][:155], body, cali, base, f"{dom}/p/{p['id']}/"), "utf-8")
    g = out / "guia-llaves"; g.mkdir(exist_ok=True)
    gb = '''<section class="hero"><h1>¿Qué llave necesito para el agua de mi nevecón?</h1><p>La manguera del nevecón es de 1/4 de pulgada. Lo que cambia es cómo tomas el agua en tu punto.</p></section>
<table><tr><th>Tu punto de agua</th><th>Qué usar</th></tr>
<tr><td>Tubo sin llave disponible</td><td>Llave galápago (trae racores, anillo y tuerca)</td></tr>
<tr><td>Ya tienes una llave de paso</td><td>Llave multipropósito, y acople o reducción si hace falta</td></tr>
<tr><td>Quieres agua filtrada</td><td>Filtro externo de tu marca (Samsung, LG o Whirlpool), con la flecha hacia el nevecón</td></tr></table>
<p>¿No estás seguro? Escríbenos por WhatsApp con una foto de tu punto de agua.</p>'''
    (g / "index.html").write_text(pagina("¿Qué llave necesito para mi nevecón?", "Guía para elegir llave galápago, llave de paso, acople o filtro para conectar el agua del nevecón.", gb, cali, base, dom + "/guia-llaves/"), "utf-8")

if __name__ == "__main__":
    P_ = P = cargar()
    salida = AQUI / "site"
    if salida.exists(): shutil.rmtree(salida)
    sitio(P, False, salida / "colombia"); sitio(P, True, salida / "cali")
    (salida / "LEEME.txt").write_text("colombia/ -> dominio principal (kits, envío gratis, sin instalación)\ncali/ -> URL aparte para Cali (kits + instalación)\n", "utf-8")
    print("ok", len(list(salida.rglob("*.html"))), "páginas")
