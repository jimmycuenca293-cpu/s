#!/usr/bin/env python3
"""Genera la tienda PuroFiltro para Hostinger (carpeta public_html/) a partir de la app de Claude.

- index.php: la misma tienda, pero el pago es automático con Wompi y no usa WhatsApp.
- filtro/<referencia>/ y marca/<marca>/: una página por filtro y por marca para Google.
- img/: las fotos como archivos (cargan más rápido que dentro del HTML).
- api/catalogo.php: precios que usa el servidor (el cliente no los puede cambiar).

Uso:  python3 build.py
"""
import base64
import datetime
import html
import json
import pathlib
import re
import shutil
import subprocess
import sys
import unicodedata

import paginas_seo
import instalacion

AQUI = pathlib.Path(__file__).resolve().parent
APP = AQUI.parent / "filtros-app" / "index.html"
SRC = AQUI / "src"
OUT = AQUI / "public_html"

app = APP.read_text(encoding="utf-8")


def cambiar(texto, viejo, nuevo, veces=1):
    n = texto.count(viejo)
    if n != veces:
        sys.exit(f"Esperaba {veces} vez(es) y encontré {n}: {viejo[:80]!r}")
    return texto.replace(viejo, nuevo)


def cambiar_re(texto, patron, nuevo):
    nuevo_txt, n = re.subn(patron, lambda m: nuevo, texto, count=1, flags=re.S)
    if n != 1:
        sys.exit(f"No encontré el patrón: {patron[:80]!r}")
    return nuevo_txt


def js_valor(nombre):
    """Lee una constante del JavaScript de la app (arreglo u objeto literal) con Node."""
    m = re.search(r"\nconst " + nombre + r" = (\[[^\n]*\]|\[.*?\n\]);", app, re.S)
    if not m:
        sys.exit(f"No encontré {nombre} en la app")
    return m.group(1)


def node_eval(expr):
    r = subprocess.run(["node", "-e", f"process.stdout.write(JSON.stringify({expr}))"], capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


def slug(s):
    s = unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def norm(s):
    return re.sub(r"[^A-Z0-9]", "", s.upper())


esc = lambda s: html.escape(str(s), quote=True)
cop = lambda n: "$ " + f"{n:,}".replace(",", ".")

# ---------- datos de la app ----------
CATALOGO = node_eval(js_valor("CATALOGO"))
POPULARES = node_eval(js_valor("POPULARES"))
CIUDADES_CO = node_eval(js_valor("CIUDADES_CO"))  # [ciudad, departamento, días?]
ciudades = node_eval(js_valor("CALI_METRO")) + [c[0] for c in CIUDADES_CO] + ["Otro municipio"]
MARCAS = [m[0] for m in node_eval(js_valor("MARCAS"))]
ubic = lambda p: "externo" if "-ex-" in p["id"] else "interno"
for p in CATALOGO:
    p["nombre_largo"] = p["nombre"] if norm(p["ref"]) in norm(p["nombre"]) else f'{p["nombre"]} {p["ref"]}'
    p["slug"] = slug(p["nombre_largo"])
    if not p.get("pack"):
        p["pack"] = round(p["precio"] * 2 * 0.9 / 100) * 100

# ---------- carpeta de salida ----------
if OUT.exists():
    # data/ tiene los pedidos: nunca se borra
    for hijo in OUT.iterdir():
        if hijo.name != "data":
            shutil.rmtree(hijo) if hijo.is_dir() else hijo.unlink()
OUT.mkdir(exist_ok=True)
shutil.copytree(SRC, OUT, dirs_exist_ok=True)
(OUT / "img").mkdir(exist_ok=True)

# ---------- fotos: de data URL a archivos ----------
m = re.search(r"\nconst PRODUCT_IMG = (\{.*?\});\n", app)
imgs = json.loads(m.group(1))
import io
from PIL import Image
TAM = {}
for pid, url in imgs.items():
    datos = base64.b64decode(url.split(",", 1)[1])
    (OUT / "img" / f"{pid}.jpg").write_bytes(datos)
    im = Image.open(io.BytesIO(datos)).convert("RGB")
    TAM[pid] = im.size
    im.save(OUT / "img" / f"{pid}.webp", "WEBP", quality=82, method=6)
    mini = im.copy(); mini.thumbnail((400, 400), Image.LANCZOS)
    mini.save(OUT / "img" / f"{pid}-400.webp", "WEBP", quality=80, method=6)
# La tienda usa WebP: pesa menos y carga más rápido en el celular
app = app.replace(m.group(1), json.dumps({pid: f"/img/{pid}.webp" for pid in imgs}))


def foto(p, alt, mini=False, lazy=True):
    """<picture> con WebP y JPG de respaldo, con medidas reales para que la página no salte al cargar."""
    w, h = TAM.get(p["id"], (600, 600))
    src = f"/img/{p['id']}-400.webp" if mini else f"/img/{p['id']}.webp"
    return (f'<picture><source srcset="{src}" type="image/webp"><img src="/img/{p["id"]}.jpg" alt="{esc(alt)}" width="{w}" height="{h}"'
            + (' loading="lazy"' if lazy else ' fetchpriority="high"') + "></picture>")
(OUT / "img" / "icono.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect width="24" height="24" rx="6" fill="#0a2a2e"/><path d="M12 3.5C9.3 7.1 6.6 9.9 6.6 13.4a5.4 5.4 0 0 0 10.8 0c0-3.5-2.7-6.3-5.4-9.9z" fill="#5fd6c3"/></svg>', encoding="utf-8")

# ---------- tienda en modo web ----------
app = app.replace('<meta charset="utf-8">\n', "", 1)
# El título y la descripción van en el <head> de index.php
app = cambiar_re(app, r"^<title>.*?</title>\n", "")
app = cambiar_re(app, r'<meta name="claude:viewport-fit-sides"[^>]*>\n', "")
app = cambiar_re(app, r'<meta name="description"[^>]*>\n', "")
app = cambiar(app, "const NEGOCIO = {", "const NEGOCIO = Object.assign({")
app = cambiar(app, "  mesesCambio: 6\n};", "  mesesCambio: 6\n}, (window.FY_WEB && FY_WEB.negocio) || {});")
# Ningún contacto va a WhatsApp: las consultas van al correo
app = cambiar(app, "const waLink = txt => waTo(NEGOCIO.whatsapp, txt);",
              'const waLink = txt => `mailto:${FY_WEB.correo}?subject=${encodeURIComponent("Consulta " + NEGOCIO.nombre)}&body=${encodeURIComponent(txt)}`;')
app = cambiar(app, "<h1>El filtro exacto de tu nevecón, con una foto</h1>", "<h1>Filtros de agua para nevecón, con envío gratis a toda Colombia</h1>")
app = cambiar(app, '<p class="lead">Tómale una foto al filtro que vas a cambiar y te decimos cuál es, cuánto cuesta y cuándo te llega.</p>',
              '<p class="lead">Samsung, LG, Whirlpool y GE. Escribe la referencia de tu filtro o el modelo de tu nevecón, paga en línea y te llega en 2 días hábiles. En Cali te lo instalamos gratis.</p>')
app = cambiar(app, '<h2 id="list-title" class="cat-title">', '<span id="catalogo"></span><h2 id="list-title" class="cat-title">')
# Textos de entrega y contacto
app = cambiar(app, "Te avisamos por WhatsApp.` : \"Agendamos contigo el día y la hora por WhatsApp.\"", "Te avisamos por correo.` : \"Te llamamos para acordar el día y la hora.\"")
app = cambiar(app, "Agendamos el día contigo por WhatsApp.", "Te llamamos para acordar el día.")
app = cambiar(app, "Escríbenos por WhatsApp con la foto del filtro", "Escríbenos al correo con la foto del filtro")
app = cambiar(app, "${ICON.wa}Preguntar por WhatsApp</a>", "Escríbenos</a>", 2)
app = cambiar(app, "Mándanos la foto de la etiqueta por WhatsApp", "Mándanos la foto de la etiqueta por correo")
app = cambiar(app, "${ICON.wa}Preguntar</a>", "Preguntar</a>")
app = cambiar(app, "<b>Te ayudamos</b>Con una foto sabemos cuál es el tuyo", "<b>Te ayudamos</b>Escribe tu referencia y te mostramos el tuyo")
app = cambiar_re(app, r'<details class="faq"><summary>¿Cada cuánto se cambia el filtro\?</summary><p>.*?</p></details>',
                 '<details class="faq"><summary>¿Cada cuánto se cambia el filtro?</summary><p>Cada 6 meses, o antes si el agua cambia de sabor, de olor o sale con poca presión. Al comprar te podemos recordar por correo.</p></details>')
app = cambiar_re(app, r'<details class="faq"><summary>¿Cómo sé cuál es el mío\?</summary><p>.*?</p></details>',
                 '<details class="faq"><summary>¿Cómo sé cuál es el mío?</summary><p>Busca la referencia impresa en tu filtro viejo o el modelo en la etiqueta de adentro del nevecón y escríbela en el buscador. Si no aparece, escríbenos al correo con la foto.</p></details>')
app = cambiar_re(app, r'<details class="faq"><summary>¿Cómo pago\?</summary><p>.*?</p></details>',
                 '<details class="faq"><summary>¿Cómo pago?</summary><p>En línea, en página de pago segura: tarjeta débito o crédito, PSE, Nequi o botón Bancolombia. No guardamos los datos de tu tarjeta.</p></details>')
# Pago: solo Wompi
# Datos: celular y correo
app = cambiar(app, '<span><b>WhatsApp</b> · para confirmar el pedido</span>', '<span><b>Celular</b> · para coordinar la entrega</span>')
i = app.index('<label class="f" id="f-tel">')
j = app.index("</label>", i) + len("</label>")
app = app[:j] + '\n        <label class="f" id="f-email"><span><b>Correo</b> · te llega el recibo</span><input id="c-email" type="email" inputmode="email" autocomplete="email" placeholder="tucorreo@gmail.com" maxlength="120" value="${esc(k.email || "")}"></label>' + app[j:]
app = cambiar(app, "<b>Recuérdame por WhatsApp cuando toque cambiar el filtro</b>", "<b>Recuérdame por correo cuando toque cambiar el filtro</b>")
app = cambiar(app, 'recordar: $("#c-rec").checked', 'recordar: $("#c-rec").checked, email: v("c-email")')
app = cambiar(app, "barrio: !k.barrio, dir: k.dir.length < 5 };", 'barrio: !k.barrio, dir: k.dir.length < 5, email: !/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(k.email || "") };')
app = cambiar(app, 'tel: "un WhatsApp válido (10 dígitos que empiezan por 3)"', 'tel: "un celular válido (10 dígitos que empiezan por 3)", email: "un correo válido"')
app = cambiar(app, 'tel: prev.tel || "",', 'tel: prev.tel || "", email: prev.email || "",')
app = cambiar(app, "<dt>WhatsApp</dt><dd>${esc(k.tel)}</dd>", "<dt>Celular</dt><dd>${esc(k.tel)}</dd><dt>Correo</dt><dd>${esc(k.email)}</dd>")
app = cambiar_re(app, r'\$\{conLink\(\) \? `<a class="btn block" id="c-confirm".*?Confirmar y recibir el link de pago</a>`\}',
              '<button class="btn block" type="button" id="c-pagar">${ICON.shield}Pagar ${COP(t.total)}</button><p class="err" id="c-perr" aria-live="polite"></p>')
app = cambiar_re(app, r'<p class="sub" style="font-size:12\.5px;margin:0">\$\{conLink\(\).*?</p>`\);',
                 '<p class="sub" style="font-size:12.5px;margin:0">Te llevamos a la página de pago segura. Precio final: no hay cobros adicionales. Al pagar aceptas los <a href="/terminos.php" target="_blank">Términos y condiciones</a> y autorizas el tratamiento de tus datos según la <a href="/privacidad.php" target="_blank">Política de datos</a>.</p>`);')
# Carrito: el paso 1 agrega al carrito; el pago se hace en /carrito.php con todos los productos
app = cambiar(app, '<button class="btn block" type="button" data-go="2">Continuar: tus datos</button>',
              '<button class="btn block" type="button" data-cart-add>Agregar al carrito</button><button class="btn ghost block" type="button" data-cart-now>Comprar ahora</button>')
app = cambiar(app, """        <select id="city" aria-label="Ciudad de entrega"></select>
      </label>""", """        <select id="city" aria-label="Ciudad de entrega"></select>
      </label>
      <a class="cart-top" href="/carrito.php" aria-label="Ver carrito"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 4h2l2.2 10.5a1.5 1.5 0 0 0 1.5 1.2h8.6a1.5 1.5 0 0 0 1.5-1.1L21 8H6.2"/><circle cx="9.5" cy="19.5" r="1.4"/><circle cx="17" cy="19.5" r="1.4"/></svg><span data-cart-n hidden></span></a>""")

# Pago con Wompi, enlace directo a un producto (?p=) y marca (?marca=)
WEB_JS = r'''
/* ===================== TIENDA WEB: CARRITO ===================== */
document.addEventListener("click", e => {
  const a = e.target.closest("[data-cart-add], [data-cart-now]"); if (!a || !cart || !window.FYCart) return;
  FYCart.agregar(cart.p.id, cart.pack, cart.pack ? 1 : cart.qty);
  if (a.hasAttribute("data-cart-now")) { location.href = "/carrito.php"; return; }
  closeSheet(); FYCart.aviso((cart.pack ? "Pack anual de " : "") + corto(cart.p) + " agregado al carrito");
});
/* ===================== TIENDA WEB: PAGO CON WOMPI ===================== */
document.addEventListener("click", async e => {
  const b = e.target.closest("#c-pagar"); if (!b || !cart) return;
  const t = totals(), k = cart.cli, old = b.innerHTML;
  b.disabled = true; b.textContent = "Abriendo el pago seguro…"; $("#c-perr").textContent = "";
  try {
    const r = await fetch(FY_WEB.api + "pedido.php", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({
      pid: cart.p.id, cantidad: t.unidades, pack: cart.pack, entrega: cart.entrega, total: t.total,
      cliente: { nombre: k.nombre, email: k.email, tel: k.wa, ciudad: k.ciudad, barrio: k.barrio, dir: k.dir, indicaciones: k.indicaciones, modelo: k.modelo, recordar: !!k.recordar } }) });
    const j = await r.json().catch(() => ({}));
    if (!r.ok || !j.url) throw new Error(j.mensaje || "No se pudo crear el pedido. Intenta de nuevo.");
    store.set("fy_cliente", { nombre: k.nombre, tel: k.tel, email: k.email, dir: k.dir, barrio: k.barrio, recordar: k.recordar });
    const cambio = new Date(); cambio.setMonth(cambio.getMonth() + NEGOCIO.mesesCambio);
    const orders = store.get("fy_orders", []).filter(o => o.id !== j.ref);
    orders.unshift({ id: j.ref, fecha: new Date().toISOString(), cambio: cambio.toISOString(), producto: cart.p.nombre, ref: cart.p.ref, pid: cart.p.id, qty: t.unidades, pack: cart.pack, ciudad: k.ciudad, entrega: cart.entrega, pago: "linea", total: j.total, eta: delivery(k.ciudad, cart.p).corto, estado: "Pago pendiente", cliente: { recordar: !!k.recordar } });
    store.set("fy_orders", orders.slice(0, 50));
    location.href = j.url;
  } catch (err) { $("#c-perr").textContent = err.message; b.disabled = false; b.innerHTML = old; }
});
(() => {
  const u = new URLSearchParams(location.search), pid = u.get("p"), marca = u.get("marca");
  if (marca && MARCAS.some(m => m[0] === marca)) { vista = { marca, ubic: "todos" }; renderCatalogo(); }
  if (pid && CATALOGO.some(x => x.id === pid)) setTimeout(() => startOrder(pid), 250);
})();
'''
k = app.rindex("\n})();\n</script>")
app = app[:k] + "\n" + WEB_JS + app[k:]

# Sección visible con las páginas de la tienda (guías, tutoriales, referencias, envíos)
EXPLORA = """<section class="explora" aria-label="Explora la tienda"><h2 style="font-size:19px">Explora la tienda</h2><div class="ex-grid">
<a href="/tienda/"><b>🛒 Tienda</b><span>Todos los filtros con precio y envío gratis</span></a>
<a href="/guia/cada-cuanto-cambiar-el-filtro-del-nevecon/"><b>⏱️ ¿Cuándo cambiar el filtro?</b><span>Las señales de que ya toca cambiarlo</span></a>
<a href="/instalacion/"><b>🔧 Cómo instalar tu filtro</b><span>Paso a paso para cada referencia</span></a>
<a href="/referencias/"><b>🔎 Buscar por referencia</b><span>Todas las referencias y equivalencias</span></a>
<a href="/neveras/"><b>🧊 Por modelo de nevecón</b><span>Qué filtro usa tu nevecón</span></a>
<a href="/guia/"><b>📘 Guías</b><span>Agua con mal sabor, dispensador, luz del filtro</span></a>
<a href="/envios/"><b>🚚 Envíos a toda Colombia</b><span>Tiempo de entrega a tu ciudad</span></a>
<a href="/cali/"><b>📍 Instalación gratis en Cali</b><span>Te lo llevamos e instalamos</span></a>
</div></section>
"""
k = app.index('<div class="check salud" id="salud">')
app = app[:k] + EXPLORA + "\n  " + app[k:]

# Enlaces fijos a todas las páginas de filtros (Google los sigue aunque no ejecute el JavaScript)
enlaces = ['<nav class="seo-links" aria-label="Todos los filtros"><h2 style="font-size:19px">Todos nuestros filtros</h2>']
for marca in MARCAS:
    ps = [p for p in CATALOGO if p["marca"] == marca]
    enlaces.append(f'<div><a class="mk" href="/marca/{slug(marca)}/">Filtros {esc(marca)}</a>' + "".join(f'<a href="/filtro/{p["slug"]}/">{esc(p["nombre_largo"])}</a>' for p in ps) + "</div>")
enlaces.append('<div><a class="mk" href="/guia/">Guías</a><a href="/guia/cada-cuanto-cambiar-el-filtro-del-nevecon/">Cada cuánto cambiar el filtro</a><a href="/guia/como-saber-que-filtro-usa-mi-nevecon/">Qué filtro usa mi nevecón</a><a href="/guia/como-cambiar-el-filtro-de-agua-del-nevecon/">Cómo cambiar el filtro</a><a href="/guia/filtro-interno-o-externo/">Interno o externo</a><a href="/guia/por-que-el-agua-del-nevecon-sabe-mal/">El agua sabe mal</a><a href="/guia/el-dispensador-de-agua-del-nevecon-no-echa-agua/">El dispensador no echa agua</a><a href="/guia/como-reiniciar-la-luz-del-filtro-del-nevecon/">Reiniciar la luz del filtro</a></div>'
               '<div><a class="mk" href="/tienda/">Tienda: todos los filtros</a><a href="/tienda/">Ver la tienda completa</a><a href="/carrito.php">Mi carrito</a></div>'
               '<div><a class="mk" href="/referencias/">Buscar por referencia o modelo</a><a href="/referencias/">Todas las referencias y equivalencias</a><a href="/neveras/">Filtro por modelo de nevecón</a><a href="/instalacion/">Cómo instalar tu filtro</a><a href="/envios/">Envíos a toda Colombia</a><a href="/cali/">Filtros con instalación gratis en Cali</a></div>')
enlaces.append('</nav><footer class="web-foot"><div class="medios" aria-label="Medios de pago" style="width:100%"><span>🔒 Pago seguro</span><span>Visa</span><span>Mastercard</span><span>American Express</span><span>PSE</span><span>Nequi</span><span>Bancolombia</span></div><a href="/terminos.php">Términos y condiciones</a><a href="/privacidad.php">Tratamiento de datos</a><a href="/terminos.php#garantia">Garantía y retracto</a><span id="pie-negocio"></span></footer>')
i = app.index('<details class="faq"><summary>¿Cómo pago?</summary>')
j = app.index("</div>", i) + len("</div>")
app = app[:j] + "\n  " + "".join(enlaces) + app[j:]

CSS_WEB = """
.top .cart-top{position:relative;display:grid;place-items:center;width:44px;height:44px;border-radius:12px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);margin-left:auto}
.top .city{order:3}.top .cart-top{order:2}
.cart-top svg{width:24px;height:24px;fill:none;stroke:#fff;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.cart-top span{position:absolute;top:-4px;right:-4px;min-width:20px;height:20px;border-radius:10px;background:var(--glow);color:#06221d;font-size:11.5px;font-weight:800;display:grid;place-items:center;padding:0 4px}
.fy-toast{position:fixed;left:50%;bottom:calc(84px + env(safe-area-inset-bottom,0px));transform:translate(-50%,200%);background:#0a2a2e;color:#fff;border-radius:14px;padding:12px 14px;display:flex;gap:14px;align-items:center;box-shadow:0 10px 30px rgba(0,0,0,.3);z-index:90;transition:transform .25s;max-width:calc(100% - 32px);font-size:14.5px}
.fy-toast.on{transform:translate(-50%,0)}.fy-toast a{color:#5fd6c3;font-weight:800;white-space:nowrap}
#cam,.hero .alt,#ai-off,nav.bnav button[data-tab="vendedor"]{display:none!important}
nav.bnav{grid-template-columns:repeat(2,1fr)!important}
#c-pagar svg{width:20px;height:20px;flex:0 0 auto;fill:none;stroke:currentColor;stroke-width:2}
.paywompi{display:flex;gap:10px;align-items:flex-start;border:1.5px solid var(--accent);background:var(--accent-soft);border-radius:14px;padding:12px}
.paywompi svg{width:24px;height:24px;flex:0 0 auto;fill:none;stroke:var(--accent);stroke-width:2}
.paywompi small{display:block;color:var(--muted);font-size:13px}
.seo-links{display:flex;flex-direction:column;gap:10px}
.seo-links div{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:14px}
.seo-links a{color:var(--accent)}.seo-links a.mk{font-weight:800;color:var(--ink);width:100%}
.web-foot{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:13px;color:var(--muted);border-top:1px solid var(--line);padding-top:12px}
.web-foot a{color:var(--accent)}
.explora{display:flex;flex-direction:column;gap:10px}.ex-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px}.ex-grid a{display:flex;flex-direction:column;gap:4px;padding:14px;border:1px solid var(--line);border-radius:14px;background:var(--panel);text-decoration:none;color:var(--ink)}.ex-grid a span{font-size:13px;color:var(--muted)}.ex-grid a:hover{border-color:var(--accent)}
.medios{display:flex;flex-wrap:wrap;gap:6px}.medios span{border:1px solid var(--line);border-radius:6px;padding:3px 8px;font-size:12px;font-weight:700;color:var(--ink);background:var(--panel)}
"""

marca_ld = [{"@type": "ListItem", "position": i + 1, "url": f"__BASE__/filtro/{p['slug']}/", "name": p["nombre_largo"]} for i, p in enumerate(CATALOGO)]
index_php = f"""<?php require __DIR__ . '/api/sitio.php'; $S = sitio(); $n = $S['negocio']; ?>
<!doctype html>
<html lang="es-CO">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Filtros de agua para nevecón Samsung, LG, Whirlpool y GE | Envío gratis | <?= h($n['nombre']) ?></title>
<meta name="description" content="Filtros de agua para nevecón Samsung, LG, Whirlpool EveryDrop y GE. Envío gratis a toda Colombia en 2 días hábiles e instalación gratis en Cali. Paga con tarjeta, PSE o Nequi.">
<link rel="canonical" href="<?= h($S['base']) ?>/">
<meta property="og:type" content="website"><meta property="og:title" content="Filtros de agua para nevecón | <?= h($n['nombre']) ?>"><meta property="og:description" content="Envío gratis a toda Colombia. Instalación gratis en Cali."><meta property="og:url" content="<?= h($S['base']) ?>/"><meta property="og:image" content="<?= h($S['base']) ?>/img/lg-1000-o.jpg"><meta property="og:locale" content="es_CO">
<meta name="theme-color" content="#0a2a2e"><link rel="icon" href="/img/icono.svg" type="image/svg+xml">
<?= verificacion_html() . analytics_html() ?>
<script type="application/ld+json"><?php $ld = <<<'JSON'
{json.dumps({"@context": "https://schema.org", "@graph": [
    {"@type": "Store", "@id": "__BASE__/#tienda", "name": "__NOMBRE__", "url": "__BASE__/", "image": "__BASE__/img/lg-1000-o.jpg", "address": {"@type": "PostalAddress", "addressLocality": "Cali", "addressRegion": "Valle del Cauca", "addressCountry": "CO"}, "areaServed": {"@type": "Country", "name": "Colombia"}, "currenciesAccepted": "COP", "paymentAccepted": "Tarjeta de crédito, tarjeta débito, PSE, Nequi", "sameAs": "__SAMEAS__"},
    {"@type": "WebSite", "name": "__NOMBRE__", "url": "__BASE__/", "inLanguage": "es-CO"},
    {"@type": "ItemList", "name": "Filtros de agua para nevecón", "itemListElement": marca_ld}]}, ensure_ascii=False)}
JSON;
echo str_replace(['__BASE__', '__NOMBRE__', '"__SAMEAS__"'], [$S['base'], addslashes($n['nombre']), json_encode(array_values(array_filter((array) (cfg()['redes'] ?? []))), JSON_UNESCAPED_SLASHES)], $ld); ?></script>
<link rel="alternate" type="text/plain" title="Resumen para asistentes de IA" href="/llms.txt">
<script>window.FY_WEB = <?= json_encode($S['web'], JSON_UNESCAPED_UNICODE | JSON_HEX_TAG) ?>;</script>
<script src="/carrito.js" defer></script>
<style>{CSS_WEB}</style>
</head>
<body>
{app}
<script>document.getElementById("pie-negocio").textContent = <?= json_encode($n['nombre'] . ' · ' . $n['titular'] . ' · ' . $n['documento'] . ' · ' . $n['correo'], JSON_UNESCAPED_UNICODE | JSON_HEX_TAG) ?>;</script>
</body>
</html>
"""
if "<?" in app:
    sys.exit("La app tiene '<?': no se puede meter en PHP sin escapar")
(OUT / "index.php").write_text(index_php, encoding="utf-8")


# ---------- páginas de cada filtro ----------
def tarjeta(p):
    return (f'<a class="card" href="/filtro/{p["slug"]}/"><span class="im">{foto(p, p["nombre_largo"], mini=True)}</span>'
            f'<b>{esc(p["nombre_largo"])}</b><span class="p">{cop(p["precio"])}</span><span class="m">Envío gratis</span></a>')


def php_str(s):
    return "'" + str(s).replace("\\", "\\\\").replace("'", "\\'") + "'"


def cabeza_producto(partes, titulo, desc, ruta, ld, img, pid):
    """Como cabeza_php, pero agrega las opiniones reales a los datos de Google (estrellas en los resultados)."""
    extra = f"<link rel=\"preload\" as=\"image\" href=\"{img}\"><meta property=\"og:image\" content=\"' . sitio()['base'] . '{img.replace('.webp', '.jpg')}\">"
    return (f"<?php require __DIR__ . '{partes}';\n$ld = json_decode(<<<'JSON'\n{json.dumps(ld, ensure_ascii=False)}\nJSON, true);\n"
            f"$R = resenas({php_str(pid)});\n"
            "if ($R['n']) {\n"
            "    $ld['@graph'][0]['aggregateRating'] = ['@type' => 'AggregateRating', 'ratingValue' => $R['prom'], 'reviewCount' => $R['n'], 'bestRating' => 5, 'worstRating' => 1];\n"
            "    $ld['@graph'][0]['review'] = array_map(fn($r) => ['@type' => 'Review', 'author' => ['@type' => 'Person', 'name' => $r['nombre']], 'datePublished' => substr($r['creado'], 0, 10),\n"
            "        'reviewRating' => ['@type' => 'Rating', 'ratingValue' => (int) $r['estrellas'], 'bestRating' => 5], 'reviewBody' => $r['texto']], array_slice($R['lista'], 0, 5));\n"
            "}\n"
            "$json = str_replace('__BASE__', sitio()['base'], json_encode($ld, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_HEX_TAG));\n"
            f"cabeza({php_str(titulo)}, {php_str(desc)}, {php_str(ruta)}, '{extra}<script type=\"application/ld+json\">' . $json . '</script>'); ?>")


def cabeza_php(partes, titulo, desc, ruta, ld, img=None):
    """Inicio de una página PHP: datos estructurados para Google con el dominio real."""
    extra = f"<link rel=\"preload\" as=\"image\" href=\"{img}\"><meta property=\"og:image\" content=\"' . sitio()['base'] . '{img}\">" if img else ""
    return (f"<?php require __DIR__ . '{partes}';\n$ld = <<<'JSON'\n{json.dumps(ld, ensure_ascii=False)}\nJSON;\n"
            f"cabeza({php_str(titulo)}, {php_str(desc)}, {php_str(ruta)}, '{extra}<script type=\"application/ld+json\">' . str_replace('__BASE__', sitio()['base'], $ld) . '</script>'); ?>")


RUTAS_CIUDAD = {"Cali": "/cali/", **{c[0]: f"/envios/{slug(c[1])}/{slug(c[0])}/" for c in CIUDADES_CO}}
CIUDADES_TOP = ["Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena", "Bucaramanga", "Pereira", "Manizales", "Armenia", "Ibagué", "Cúcuta", "Santa Marta",
                "Villavicencio", "Neiva", "Pasto", "Popayán", "Montería", "Valledupar", "Sincelejo", "Tunja", "Palmira", "Soacha", "Envigado", "Chía"]
PRINCIPALES = {norm(p["ref"]) for p in CATALOGO}
ruta_ref = {}
for p in CATALOGO:
    for r in p["refs"]:
        if norm(r) not in PRINCIPALES and norm(r) not in ruta_ref:
            ruta_ref[norm(r)] = f"/referencia/{slug(r)}/"
ruta_modelo = {norm(m): f"/nevecon/{slug(m)}/" for p in CATALOGO for m in p["modelos"]}

for p in CATALOGO:
    alias = [r for r in p["refs"] if norm(r) != norm(p["ref"])]
    otros = [x for x in CATALOGO if x["marca"] == p["marca"] and x["id"] != p["id"]][:6]
    donde = "Va en la manguera de agua, por fuera del nevecón." if ubic(p) == "externo" else "Va por dentro del nevecón."
    ahorro = p["precio"] * 2 - p["pack"]
    titulo = f'{p["nombre_largo"]} | Envío gratis a toda Colombia' if len(p['nombre_largo']) < 34 else f'{p["nombre_largo"]} | Envío gratis'
    desc = (f'Compra el {p["nombre_largo"]} a {cop(p["precio"])} con envío gratis a toda Colombia en 2 días hábiles'
            + (f'. También aparece como {", ".join(alias[:3])}' if alias else "") + ". En Cali te lo instalamos gratis. Paga con tarjeta, PSE o Nequi.")
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Product", "name": p["nombre_largo"], "image": f"__BASE__/img/{p['id']}.jpg", "sku": p["ref"], "mpn": p["ref"],
         "brand": {"@type": "Brand", "name": p["marca"]}, "description": f'Filtro de agua para nevecón {p["marca"]}, referencia {p["ref"]}. {p.get("desc") or donde}',
         "offers": {"@type": "Offer", "url": f"__BASE__/filtro/{p['slug']}/", "priceCurrency": "COP", "price": str(p["precio"]),
                    "availability": "https://schema.org/InStock" if p.get("stock") else "https://schema.org/BackOrder", "itemCondition": "https://schema.org/NewCondition",
                    "shippingDetails": {"@type": "OfferShippingDetails", "shippingRate": {"@type": "MonetaryAmount", "value": "0", "currency": "COP"},
                                        "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "CO"},
                                        "deliveryTime": {"@type": "ShippingDeliveryTime", "handlingTime": {"@type": "QuantitativeValue", "minValue": 0, "maxValue": 1, "unitCode": "DAY"},
                                                         "transitTime": {"@type": "QuantitativeValue", "minValue": 1, "maxValue": 3, "unitCode": "DAY"}}},
                    "hasMerchantReturnPolicy": {"@type": "MerchantReturnPolicy", "applicableCountry": "CO", "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
                                                "merchantReturnDays": 5, "returnMethod": "https://schema.org/ReturnByMail", "returnFees": "https://schema.org/ReturnFeesCustomerResponsibility"}}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": "__BASE__/"},
            {"@type": "ListItem", "position": 2, "name": f'Filtros {p["marca"]}', "item": f"__BASE__/marca/{slug(p['marca'])}/"},
            {"@type": "ListItem", "position": 3, "name": p["nombre_largo"], "item": f"__BASE__/filtro/{p['slug']}/"}]},
        instalacion.tutorial_ld(p, f"__BASE__/filtro/{p['slug']}/")]}
    pagina = cabeza_producto("/../../partes.php", titulo, desc, f'/filtro/{p["slug"]}/', ld, f'/img/{p["id"]}.webp', p["id"]) + f"""
<nav class="miga"><a href="/">Inicio</a> › <a href="/marca/{slug(p["marca"])}/">Filtros {esc(p["marca"])}</a> › {esc(p["nombre_largo"])}</nav>
<div class="prod">
  <div class="foto">{foto(p, p["nombre_largo"] + " para nevecón " + p["marca"], lazy=False)}</div>
  <div class="caja">
    <h1>{esc(p["nombre_largo"])}</h1>
    <span class="m">Filtro de agua para nevecón {esc(p["marca"])} · {"Externo" if ubic(p) == "externo" else "Interno"} · Referencia <span class="ref">{esc(p["ref"])}</span></span>
    <?php if ($R['n']) echo '<a href="#opiniones" style="text-decoration:none">' . estrellas_html($R['prom']) . ' <b>' . $R['prom'] . '</b> <span class="m">(' . $R['n'] . ($R['n'] === 1 ? ' opinión' : ' opiniones') . ')</span></a>'; ?>
    <span class="precio">{cop(p["precio"])}</span>
    <ul class="ok"><li><b>Envío gratis</b> a toda Colombia: llega en 2 a 3 días hábiles a las principales ciudades.</li><li>En Cali: <b>domicilio e instalación gratis</b>.</li><li>Pack anual de 2 filtros: {cop(p["pack"])} (ahorras {cop(ahorro)}).</li><li>Garantía de 30 días: si no encaja, te lo cambiamos.</li></ul>
    <div class="compra"><button class="btn block" type="button" data-add="{p["id"]}">Agregar al carrito</button><button class="btn ghost block" type="button" data-add="{p["id"]}" data-ir="1">Comprar ahora</button><button class="link" type="button" data-add="{p["id"]}" data-pack="1">+ Pack anual de 2 por {cop(p["pack"])} (ahorras {cop(ahorro)})</button></div>
    <span class="m">Pago seguro en línea: tarjeta débito o crédito, PSE, Nequi o botón Bancolombia.</span><?= medios_pago_html() ?>
  </div>
</div>
<section class="caja descripcion">
  <h2>Descripción</h2>
  <p>{esc(p.get("desc") or ("Filtro de agua para nevecones " + p["marca"] + ". " + donde))}</p>
  <p>Retiene el cloro, el sedimento y las partículas que le dan mal sabor y mal olor al agua y al hielo, y ayuda a proteger la válvula y la máquina de hielo del nevecón. Rinde unos 6 meses de uso normal; después se satura y conviene cambiarlo.</p>
  <p>{f"Si tu filtro viejo dice <b>{esc(p['ref'])}</b> o alguna de estas referencias: {esc(', '.join(alias))}, este es el tuyo." if alias else f"Si tu filtro viejo dice <b>{esc(p['ref'])}</b>, este es el tuyo."}</p>
  <h3 style="margin:6px 0 0;font-size:16px">Qué incluye</h3>
  <ul class="ok"><li>1 filtro de agua {esc(p["ref"])} nuevo, en su empaque (o 2 si escoges el pack anual).</li><li>Envío gratis a toda Colombia con número de guía.</li><li>En Cali: instalación gratis y revisión del dispensador.</li><li>Garantía de 30 días: si no encaja, te lo cambiamos.</li></ul>
</section>
<section class="caja datos">
  <h2>Ficha técnica y datos rápidos</h2>
  <p>El <b>{esc(p["nombre_largo"])}</b> es el filtro de agua {"externo (va en la manguera)" if ubic(p) == "externo" else "interno"} para nevecones {esc(p["marca"])}{(", también conocido como " + esc(", ".join(alias[:5]))) if alias else ""}. Cuesta {cop(p["precio"])} en <?= h(cfg()['negocio']['nombre']) ?> con envío gratis a toda Colombia (2 a 3 días hábiles en las principales ciudades) e instalación gratis en Cali. Se cambia cada 6 meses.</p>
  <dl class="dq"><dt>Referencia</dt><dd>{esc(p["ref"])}</dd><dt>Marca del nevecón</dt><dd>{esc(p["marca"])}</dd><dt>Tipo</dt><dd>{"Externo, en la manguera" if ubic(p) == "externo" else "Interno"}</dd>
  <dt>Precio</dt><dd>{cop(p["precio"])} (pack de 2: {cop(p["pack"])})</dd><dt>Envío</dt><dd>Gratis a toda Colombia, 2 a 3 días hábiles en las principales ciudades</dd><dt>Instalación</dt><dd>Gratis en Cali</dd><dt>Duración</dt><dd>6 meses</dd>
  {f'<dt>Equivalencias</dt><dd>{esc(", ".join(alias))}</dd>' if alias else ""}{f'<dt>Nevecones</dt><dd>{esc(", ".join(p["modelos"]))}</dd>' if p["modelos"] else ""}</dl>
</section>
<section class="caja">
  <h2>¿Es el filtro de tu nevecón?</h2>
  <p>Busca esta referencia impresa en tu filtro viejo: <span class="ref">{esc(p["ref"])}</span>. {esc(donde)}</p>
  {f'<p>También aparece como:</p><div class="chips">{"".join(f"<a href=\"{ruta_ref[norm(r)]}\">{esc(r)}</a>" if norm(r) in ruta_ref else f"<span>{esc(r)}</span>" for r in alias)}</div>' if alias else ""}
  {f'<p>Sirve para estos nevecones, entre otros:</p><div class="chips">{"".join(f"<a href=\"{ruta_modelo[norm(m)]}\">{esc(m)}</a>" for m in p["modelos"])}</div>' if p["modelos"] else ""}
  {f'<p>{esc(p["nota"])}</p>' if p.get("nota") else ""}
  <p>Cámbialo cada 6 meses, o antes si el agua cambia de sabor, de olor o sale con poca presión. <a href="/guia/cada-cuanto-cambiar-el-filtro-del-nevecon/">Más sobre cuándo cambiarlo</a>.</p>
</section>
{paginas_seo.mas_info(p, ubic)}
{instalacion.tutorial_html(p)}
<section class="caja" id="opiniones"><h2>Opiniones de compradores</h2>
<?php if ($R['n']): ?><span><?= estrellas_html($R['prom']) ?> <b><?= $R['prom'] ?> de 5</b> · <?= $R['n'] ?> <?= $R['n'] === 1 ? 'opinión' : 'opiniones' ?> de compradores reales</span>
<?php foreach ($R['lista'] as $r): ?><div class="resena"><?= estrellas_html((float) $r['estrellas']) ?> <b><?= h($r['nombre']) ?></b> <span class="m">· <?= h($r['ciudad']) ?> · <?= h(date('d/m/Y', strtotime($r['creado']))) ?></span><?= $r['texto'] !== '' ? '<p style="margin:4px 0 0">' . h($r['texto']) . '</p>' : '' ?></div><?php endforeach; ?>
<?php else: ?><p class="m">Todavía no hay opiniones de este filtro. Después de tu compra te pediremos la tuya por correo.</p><?php endif; ?>
</section>
<section style="display:flex;flex-direction:column;gap:8px">
  <h2>Preguntas frecuentes</h2>
  <details><summary>¿Cuánto cuesta el envío?</summary><p>Nada. El envío es gratis a toda Colombia y llega en unos 2 a 3 días hábiles a las principales ciudades. Mira el <a href="/envios/">tiempo de entrega a tu ciudad</a>.</p></details>
  <details><summary>¿Lo instalan?</summary><p>En Cali te lo llevamos e instalamos gratis. En otras ciudades te lo enviamos con las instrucciones: se instala en minutos, sin herramientas.</p></details>
  <details><summary>¿Cómo pago?</summary><p>En línea, en página de pago segura: tarjeta débito o crédito, PSE, Nequi o botón Bancolombia. Te llega el recibo a tu correo.</p></details>
  <details><summary>¿Y si no me sirve?</summary><p>Tienes 5 días hábiles para retractarte con el filtro sin instalar, y 30 días de garantía si no encaja o llega con un defecto. Mira los <a href="/terminos.php#garantia">términos</a>.</p></details>
</section>
<section class="caja"><h2>Enviamos el {esc(p["ref"])} a toda Colombia</h2><p>Envío gratis a {len(CIUDADES_CO) + 1} ciudades y municipios. Estas son algunas:</p><div class="chips">{"".join(f'<a href="{RUTAS_CIUDAD[c]}">{esc(c)}</a>' for c in CIUDADES_TOP)}</div><p class="m"><a href="/envios/">Ver todas las ciudades</a></p></section>
{f'<section style="display:flex;flex-direction:column;gap:10px"><h2>Otros filtros {esc(p["marca"])}</h2><div class="grid">{"".join(tarjeta(x) for x in otros)}</div></section>' if otros else ""}
<div class="barra-compra"><span><span class="m">{esc(p["nombre_largo"])}</span><b>{cop(p["precio"])}</b></span><button class="btn" type="button" data-add="{p["id"]}">Agregar al carrito</button></div>
<?php pie(); ?>
"""
    d = OUT / "filtro" / p["slug"]
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.php").write_text(pagina, encoding="utf-8")

# ---------- páginas por marca ----------
INTRO = {
    "Samsung": "Filtros de agua para nevecones Samsung de dos puertas y French door: internos (HAF-CIN, HAF-QIN, Aqua-Pure) y el externo de manguera.",
    "LG": "Filtros de agua para nevecones LG: LT1000P, LT700P, LT800P, LT500P, LT600P y el externo de manguera.",
    "Whirlpool": "Filtros EveryDrop para nevecones Whirlpool, Maytag, KitchenAid, Jenn-Air y Amana: del 1 al 5, y el filtro externo de manguera.",
    "GE": "Filtros de agua para nevecones GE General Electric: MWF y XWF.",
}
for marca in MARCAS:
    ps = [p for p in CATALOGO if p["marca"] == marca]
    s = slug(marca)
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Inicio", "item": "__BASE__/"},
        {"@type": "ListItem", "position": 2, "name": f"Filtros {marca}", "item": f"__BASE__/marca/{s}/"}]}
    titulo = f"Filtros de agua para nevecón {marca} | Envío gratis a toda Colombia"
    desc = f"{INTRO.get(marca, '')} Envío gratis a toda Colombia e instalación gratis en Cali. Paga con tarjeta, PSE o Nequi."
    pagina = cabeza_php("/../../partes.php", titulo, desc, f"/marca/{s}/", ld) + f"""
<nav class="miga"><a href="/">Inicio</a> › Filtros {esc(marca)}</nav>
<h1>Filtros de agua para nevecón {esc(marca)}</h1>
<p>{esc(INTRO.get(marca, ""))} Todos con <b>envío gratis</b> a toda Colombia y, en Cali, <b>instalación gratis</b>.</p>
<div class="grid">{"".join(tarjeta(p) for p in ps)}</div>
<section class="caja"><h2>¿Cuál es el mío?</h2><p>Saca el filtro viejo y busca la referencia impresa, o mira el modelo en la etiqueta de adentro del nevecón. Escríbelo en el <a href="/#catalogo">buscador de la tienda</a> y te mostramos el filtro que le sirve.</p></section>
<?php pie(); ?>
"""
    d = OUT / "marca" / s
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.php").write_text(pagina, encoding="utf-8")

# ---------- referencias, nevecones, guías, Cali y directorios ----------
extra = paginas_seo.generar(OUT, CATALOGO, MARCAS, slug, norm, ubic, cabeza_php, tarjeta, CIUDADES_CO)

# ---------- catálogo del servidor ----------
def php_val(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, str):
        return "'" + v.replace("\\", "\\\\").replace("'", "\\'") + "'"
    if isinstance(v, list):
        return "[" + ", ".join(php_val(x) for x in v) + "]"
    return "[" + ", ".join(f"{php_val(k)} => {php_val(x)}" for k, x in v.items()) + "]"


cat_php = {
    "fecha": datetime.date.today().isoformat(),
    "ciudades": ciudades,
    "dias": {c[0]: c[2] for c in CIUDADES_CO if len(c) > 2},
    "rutas_ciudad": extra["rutas_ciudad"],
    "marcas": [{"nombre": m, "slug": slug(m)} for m in MARCAS],
    "paginas": extra["paginas"],
    "guias": [{"ruta": r, "titulo": t} for r, t in extra["guias"]],
    "productos": {p["id"]: {"nombre": p["nombre_largo"], "ref": p["ref"], "marca": p["marca"], "precio": p["precio"], "pack": p["pack"], "slug": p["slug"], "alias": [r for r in p["refs"] if norm(r) != norm(p["ref"])],
                       "modelos": p["modelos"], "nota": p.get("nota", ""), "link_pago": p.get("linkPago", "") if p.get("linkMonto") == p["precio"] else "", "ubic": ubic(p), "rutas_ref": {r: ruta_ref[norm(r)] for r in p["refs"] if norm(r) in ruta_ref},
                       "rutas_modelo": {m: ruta_modelo[norm(m)] for m in p["modelos"]}} for p in CATALOGO},
}
(OUT / "api" / "catalogo.php").write_text("<?php\n// Generado por build.py: no lo edites a mano. Los precios se cambian en la app y se vuelve a generar.\nreturn " + php_val(cat_php) + ";\n", encoding="utf-8")

print(f"Listo: {OUT.relative_to(AQUI)}/ con {len(CATALOGO)} filtros, {len(MARCAS)} marcas, {len(extra['refs']) - len(CATALOGO)} referencias equivalentes, "
      f"{len(extra['modelos'])} nevecones, {len(extra['guias'])} guías y {len(imgs)} fotos")
