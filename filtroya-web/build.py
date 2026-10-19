#!/usr/bin/env python3
"""Genera la tienda Filtros Nevecones para Hostinger (carpeta public_html/) a partir de la app de Claude.

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

import marcas_exclusivas
import paginas_seo
import seo_busquedas
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


PREFIJO = "purofiltro-"  # nombre del proyecto en cada carpeta
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
        if hijo.name not in ("data", PREFIJO + "data"):
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
# imagen para compartir en redes, íconos y manifiesto de la app
for src_, dst_ in (("compartir.jpg", "compartir.jpg"), ("icono-512.png", "icono-512.png"), ("apple-touch-icon.png", "apple-touch-icon.png")):
    shutil.copy(AQUI / "imagenes-tienda" / src_, OUT / "img" / dst_)
(OUT / "manifest.webmanifest").write_text(json.dumps({"name": "Filtros Nevecones Colombia", "short_name": "Filtros Nevecones", "start_url": "/", "display": "standalone",
    "background_color": "#f1f5ff", "theme_color": "#0b1f6b", "lang": "es-CO",
    "icons": [{"src": "/img/icono-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"}, {"src": "/img/apple-touch-icon.png", "sizes": "180x180", "type": "image/png"}]}, ensure_ascii=False), encoding="utf-8")
# fotos de las secciones (las que envió el dueño): se recortan a 16:9 y salen en JPG y WebP livianos
for nombre, (y0, caja) in {"alerta": (None, (0, 200, 1145, 845)), "agua": (60, None), "familia": (20, None), "asesoria": (20, None)}.items():
    im = Image.open(AQUI / "imagenes-tienda" / f"{nombre}.jpg").convert("RGB")
    if caja is None:
        h = round(im.width * 9 / 16)
        caja = (0, min(y0, im.height - h), im.width, min(y0, im.height - h) + h)
    im = im.crop(caja).resize((1024, 576), Image.LANCZOS)
    im.save(OUT / "img" / f"tienda-{nombre}.jpg", quality=84, optimize=True, progressive=True)
    im.save(OUT / "img" / f"tienda-{nombre}.webp", "WEBP", quality=80, method=6)
    im.resize((640, 360), Image.LANCZOS).save(OUT / "img" / f"tienda-{nombre}-640.webp", "WEBP", quality=80, method=6)
# La tienda usa WebP: pesa menos y carga más rápido en el celular
app = app.replace(m.group(1), json.dumps({pid: f"/img/{pid}.webp" for pid in imgs}))


def foto(p, alt, mini=False, lazy=True):
    """<picture> con WebP y JPG de respaldo, con medidas reales para que la página no salte al cargar."""
    w, h = TAM.get(p["id"], (600, 600))
    src = f"/img/{p['id']}-400.webp" if mini else f"/img/{p['id']}.webp"
    return (f'<picture><source srcset="{src}" type="image/webp"><img src="/img/{p["id"]}.jpg" alt="{esc(alt)}" width="{w}" height="{h}"'
            + (' loading="lazy"' if lazy else ' fetchpriority="high"') + "></picture>")
(OUT / "img" / "icono.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect width="24" height="24" rx="6" fill="#0b1f6b"/><path d="M12 3.5C9.3 7.1 6.6 9.9 6.6 13.4a5.4 5.4 0 0 0 10.8 0c0-3.5-2.7-6.3-5.4-9.9z" fill="#38d6ff"/><path d="M12 11.2v4.8M9.9 12.4l4.2 2.4M14.1 12.4l-4.2 2.4" stroke="#0b1f6b" stroke-width="1.15" stroke-linecap="round" fill="none"/></svg>', encoding="utf-8")

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
              '<p class="lead">Samsung, LG, Whirlpool, GE, KitchenAid, Maytag, Jenn-Air, Amana, Kenmore y más marcas. Escribe la referencia de tu filtro o el modelo de tu nevecón, paga en línea de forma segura y te llega en 2 a 3 días hábiles.</p>')
app = cambiar(app, '<h2 id="list-title" class="cat-title">', '<span id="catalogo"></span><h2 id="list-title" class="cat-title">')
# Textos de entrega y contacto
app = cambiar(app, "Te avisamos por WhatsApp.` : \"Agendamos contigo el día y la hora por WhatsApp.\"", "Te avisamos por correo.` : \"Te llamamos para acordar el día y la hora.\"")
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
      <nav class="hero-nav"><a href="/tienda/">Tienda</a><a href="/marca/samsung/">Samsung</a><a href="/marca/lg/">LG</a><a href="/marca/whirlpool/">Whirlpool</a><a href="/marca/ge/">GE</a><a href="/instalacion/">Instalación</a><a href="/guia/">Guías</a></nav>
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
    window.FYPago ? FYPago(j.url, j.total, j.ref) : (location.href = j.url);
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

app = cambiar(app, 'whatsapp: "573217996144",', 'whatsapp: window.FY_WA || "573217996144",')
# Sección visible con las páginas de la tienda (guías, tutoriales, referencias, envíos)
EXPLORA = """<section class="explora" aria-label="Explora la tienda"><h2 style="font-size:19px">Explora la tienda</h2><div class="ex-grid">
<a href="/tienda/"><b>🛒 Tienda</b><span>Todos los filtros con precio y envío gratis</span></a>
<a href="/guia/cada-cuanto-cambiar-el-filtro-del-nevecon/"><b>⏱️ ¿Cuándo cambiar el filtro?</b><span>Las señales de que ya toca cambiarlo</span></a>
<a href="/instalacion/"><b>🔧 Cómo instalar tu filtro</b><span>Paso a paso para cada referencia</span></a>
<a href="/referencias/"><b>🔎 Buscar por referencia</b><span>Todas las referencias y equivalencias</span></a>
<a href="/neveras/"><b>🧊 Por modelo de nevecón</b><span>Qué filtro usa tu nevecón</span></a>
<a href="/guia/"><b>📘 Guías</b><span>Agua con mal sabor, dispensador, luz del filtro</span></a>
<a href="/envios/"><b>🚚 Envíos a toda Colombia</b><span>Tiempo de entrega a tu ciudad</span></a>
<a href="#" data-wa-asesor><b>💬 Asesor por WhatsApp</b><span>Te ayudamos a escoger el tuyo</span></a>
<a href="/quienes-somos.php"><b>👨‍🔧 Quiénes somos</b><span>Técnicos de neveras y nevecones</span></a>
</div></section>
"""
ABAJO = """<section class="explora" aria-label="Información"><h2 style="font-size:19px">Información</h2><div class="ex-grid">
<a href="/terminos.php"><b>📄 Términos y condiciones</b><span>Compras, precios y entregas</span></a>
<a href="/privacidad.php"><b>🔒 Tratamiento de datos</b><span>Cómo cuidamos tu información</span></a>
<a href="/garantia-y-retracto.php"><b>↩️ Garantía y retracto</b><span>Garantía legal y 5 días de retracto</span></a>
</div></section>
<section class="pasos3" aria-label="Cómo comprar"><h2 style="font-size:19px">Compra en 3 pasos</h2><div class="p3-grid">
<div><span>1</span><b>Encuentra tu filtro</b><p>Escribe la referencia de tu filtro viejo o el modelo de tu nevecón y te mostramos el que le sirve.</p></div>
<div><span>2</span><b>Paga seguro en línea</b><p>Tarjeta débito o crédito, PSE, Nequi o botón Bancolombia, en página de pago segura.</p></div>
<div><span>3</span><b>Recíbelo en tu casa</b><p>Envío gratis a toda Colombia en 2 a 3 días hábiles. Lo instalas en minutos con nuestro paso a paso.</p></div>
</div></section>
<section class="marcas-sec" aria-label="Filtros por marca de nevera">
<figure class="ms-foto"><picture><source srcset="/img/tienda-familia-640.webp 640w, /img/tienda-familia.webp 1024w" sizes="(max-width:700px) 100vw, 520px" type="image/webp"><img src="/img/tienda-familia.jpg" alt="Familia sirviéndose agua con hielo del dispensador del nevecón" width="1024" height="576" loading="lazy"></picture><figcaption>Agua y hielo limpios para toda la familia</figcaption></figure>
<div class="ms-txt"><span class="ms-eye">Para tu marca de nevera</span><h2>Filtros para Samsung, LG, Whirlpool, GE, KitchenAid, Maytag y más</h2>
<p>Escoge la marca de tu nevera o nevecón y mira qué filtro le sirve, cuánto cuesta y cómo cambiarlo. Envío gratis a toda Colombia.</p>
<div class="ms-grid">
<a href="/marca/samsung/"><b>Samsung</b><span>HAF-CIN, HAF-QIN, Aqua-Pure</span></a>
<a href="/marca/lg/"><b>LG</b><span>LT1000P, LT700P, LT800P</span></a>
<a href="/marca/whirlpool/"><b>Whirlpool</b><span>EveryDrop 1 al 5</span></a>
<a href="/marca/ge/"><b>GE</b><span>MWF y XWF</span></a>
<a href="/otras-marcas/filtro-para-nevera-kitchenaid/"><b>KitchenAid</b><span>Filtros EveryDrop</span></a>
<a href="/otras-marcas/filtro-para-nevera-maytag/"><b>Maytag</b><span>También MyTag</span></a>
<a href="/otras-marcas/filtro-para-nevera-jenn-air/"><b>Jenn-Air</b><span>Filtros EveryDrop</span></a>
<a href="/otras-marcas/filtro-para-nevera-amana/"><b>Amana</b><span>Filtros EveryDrop</span></a>
<a href="/otras-marcas/filtro-para-nevera-kenmore/"><b>Kenmore</b><span>Equivalencias 46-9xxx</span></a>
<a class="ms-mas" href="/otras-marcas/"><b>Y más marcas →</b><span>Filtro externo para Mabe, Haceb y otras</span></a>
</div></div></section>
"""
# En la web, las guías rápidas de la app se cambian por enlaces a las páginas completas
app = cambiar_re(app, r'<div class="guias-rapidas" id="guias-rapidas">.*?</div></div>\n', EXPLORA)
app = cambiar(app, '<div class="check salud" id="salud">', ABAJO + '<div class="check salud" id="salud">')

# Enlaces fijos a todas las páginas de filtros (Google los sigue aunque no ejecute el JavaScript)
enlaces = ['<nav class="seo-links" aria-label="Todos los filtros"><h2 style="font-size:19px">Todos nuestros filtros</h2>']
for marca in MARCAS:
    ps = [p for p in CATALOGO if p["marca"] == marca]
    enlaces.append(f'<div><a class="mk" href="/marca/{slug(marca)}/">Filtros {esc(marca)}</a>' + "".join(f'<a href="/filtro/{p["slug"]}/">{esc(p["nombre_largo"])}</a>' for p in ps) + "</div>")
enlaces.append('<div><a class="mk" href="/guia/">Guías</a><a href="/guia/cada-cuanto-cambiar-el-filtro-del-nevecon/">Cada cuánto cambiar el filtro</a><a href="/guia/como-saber-que-filtro-usa-mi-nevecon/">Qué filtro usa mi nevecón</a><a href="/guia/como-cambiar-el-filtro-de-agua-del-nevecon/">Cómo cambiar el filtro</a><a href="/guia/filtro-interno-o-externo/">Interno o externo</a><a href="/guia/por-que-el-agua-del-nevecon-sabe-mal/">El agua sabe mal</a><a href="/guia/el-dispensador-de-agua-del-nevecon-no-echa-agua/">El dispensador no echa agua</a><a href="/guia/como-reiniciar-la-luz-del-filtro-del-nevecon/">Reiniciar la luz del filtro</a></div>'
               '<div><a class="mk" href="/tienda/">Tienda: todos los filtros</a><a href="/tienda/">Ver la tienda completa</a><a href="/carrito.php">Mi carrito</a></div>'
               '<div><a class="mk" href="/referencias/">Buscar por referencia o modelo</a><a href="/referencias/">Todas las referencias y equivalencias</a><a href="/neveras/">Filtro por modelo de nevecón</a><a href="/instalacion/">Cómo instalar tu filtro</a><a href="/envios/">Envíos a toda Colombia</a></div>')
enlaces.append('</nav>')
i = app.index('<details class="faq"><summary>¿Cómo pago?</summary>')
j = app.index("</div>", i) + len("</div>")
app = app[:j] + "\n  " + "".join(enlaces) + app[j:]

_EST = (SRC / "estilo.css").read_text(encoding="utf-8")
CSS_COMUN = _EST[_EST.index("/* barra de anuncio */"):_EST.index("/* encabezado */")] + _EST[_EST.index("/* pie de página */"):]
CSS_WEB = """
.top .cart-top{position:relative;display:grid;place-items:center;width:44px;height:44px;border-radius:12px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);margin-left:auto}
.top .city{order:3}.top .cart-top{order:2}
.hero-nav{display:none}@media (min-width:980px){.hero-nav{display:flex;gap:2px;order:1;margin-left:auto}.hero-nav a{color:#dfeeea;text-decoration:none;font-weight:600;font-size:15px;padding:8px 11px;border-radius:10px}.hero-nav a:hover{background:rgba(255,255,255,.1);color:#fff}}
.cart-top svg{width:24px;height:24px;fill:none;stroke:#fff;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.cart-top span{position:absolute;top:-4px;right:-4px;min-width:20px;height:20px;border-radius:10px;background:var(--glow);color:#06221d;font-size:11.5px;font-weight:800;display:grid;place-items:center;padding:0 4px}
.fy-toast{position:fixed;left:50%;bottom:calc(84px + env(safe-area-inset-bottom,0px));transform:translate(-50%,200%);background:#0b1f6b;color:#fff;border-radius:14px;padding:12px 14px;display:flex;gap:14px;align-items:center;box-shadow:0 10px 30px rgba(0,0,0,.3);z-index:90;transition:transform .25s;max-width:calc(100% - 32px);font-size:14.5px}
.fy-toast.on{transform:translate(-50%,0)}.fy-toast a{color:#38d6ff;font-weight:800;white-space:nowrap}
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
.wrap{max-width:1140px!important}
.pasos3{display:flex;flex-direction:column;gap:12px}.p3-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}
.p3-grid div{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:16px;display:flex;flex-direction:column;gap:6px}
.p3-grid span{width:34px;height:34px;border-radius:50%;display:grid;place-items:center;background:var(--accent);color:var(--accent-ink);font-weight:800;font-family:var(--f-display)}
.p3-grid p{margin:0;color:var(--muted);font-size:14px;line-height:1.5}
.marcas-sec{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:22px;align-items:center;margin-top:10px}
.ms-foto{margin:0;position:relative;border-radius:20px;overflow:hidden;box-shadow:var(--shadow)}.ms-foto img{width:100%;height:auto;aspect-ratio:16/10;object-fit:cover;display:block}
.ms-foto figcaption{position:absolute;left:12px;bottom:12px;background:rgba(11,31,107,.88);color:#fff;font-weight:700;font-size:13px;padding:7px 12px;border-radius:999px}
.ms-eye{font-size:12px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--accent)}
.ms-txt h2{margin:6px 0 8px;font-size:clamp(21px,3vw,28px);line-height:1.12}.ms-txt p{color:var(--muted);margin:0 0 14px}
.ms-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px}
.ms-grid a{display:flex;flex-direction:column;gap:2px;padding:11px 13px;border-radius:14px;background:var(--panel);border:1px solid var(--line);text-decoration:none;color:var(--ink);transition:transform .15s,border-color .15s,box-shadow .15s}
.ms-grid a:hover{transform:translateY(-2px);border-color:var(--accent);box-shadow:0 10px 24px -14px rgba(26,92,255,.5)}
.ms-grid b{font-family:var(--f-display);font-size:17px}.ms-grid span{font-size:12.5px;color:var(--muted)}
.ms-grid .ms-mas{background:linear-gradient(135deg,#ff8a1f,#ff4d2e);border-color:transparent;color:#fff}.ms-grid .ms-mas span{color:rgba(255,255,255,.9)}
@media (max-width:760px){.marcas-sec{grid-template-columns:1fr}}
.ex-grid a{transition:transform .18s,box-shadow .18s,border-color .18s}.ex-grid a:hover{transform:translateY(-3px);box-shadow:0 14px 30px -18px rgba(11,26,69,.45)}
#wa-flot{left:auto!important;right:max(16px,env(safe-area-inset-right,0px))!important}@media (max-width:520px){#wa-flot span{display:none}#wa-flot{padding:14px!important}}
.explora{display:flex;flex-direction:column;gap:10px}.ex-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px}.ex-grid a{display:flex;flex-direction:column;gap:4px;padding:14px;border:1px solid var(--line);border-radius:14px;background:var(--panel);text-decoration:none;color:var(--ink)}.ex-grid a span{font-size:13px;color:var(--muted)}.ex-grid a:hover{border-color:var(--accent)}
.medios{display:flex;flex-wrap:wrap;gap:6px}.medios span{border:1px solid var(--line);border-radius:6px;padding:3px 8px;font-size:12px;font-weight:700;color:var(--ink);background:var(--panel)}
"""

home_seo, home_faq = seo_busquedas.home_bloque(CATALOGO, MARCAS, slug, ubic, CIUDADES_CO)
marca_ld = [{"@type": "ListItem", "position": i + 1, "url": f"__BASE__/filtro/{p['slug']}/", "name": p["nombre_largo"]} for i, p in enumerate(CATALOGO)]
index_php = f"""<?php require __DIR__ . '/partes.php'; $S = sitio(); $n = $S['negocio']; ?>
<!doctype html>
<html lang="es-CO">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Filtros de agua para nevera y nevecón: Samsung, LG, Whirlpool, GE, KitchenAid, Maytag y más marcas | Envío gratis</title>
<meta name="description" content="Compra el filtro de agua de tu nevera o nevecón Samsung, LG, Whirlpool, GE, KitchenAid, Maytag, Jenn-Air, Amana, Kenmore y más marcas. Precios, referencias, cómo instalarlo y cada cuánto cambiarlo. Envío gratis a toda Colombia. Paga con tarjeta, PSE o Nequi.">
<meta name="keywords" content="filtro de agua para nevera, filtro de nevecón, filtro nevera Samsung, filtro nevera LG, filtro Whirlpool EveryDrop, filtro GE MWF, precio filtro de nevera, cada cuánto cambiar el filtro de la nevera, luz del filtro, filtro de refrigerador Colombia">
<link rel="canonical" href="<?= h($S['base']) ?>/">
<meta property="og:type" content="website"><meta property="og:title" content="Filtros de agua para nevera y nevecón | Envío gratis a toda Colombia"><meta property="og:description" content="Envío gratis a toda Colombia. Pago seguro en línea."><meta property="og:url" content="<?= h($S['base']) ?>/"><meta property="og:image" content="<?= h($S['base']) ?>/img/compartir.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:locale" content="es_CO"><meta property="og:site_name" content="<?= h($n['nombre']) ?>"><meta name="twitter:card" content="summary_large_image"><link rel="manifest" href="/manifest.webmanifest"><link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<meta name="theme-color" content="#0b1f6b"><link rel="icon" href="/img/icono.svg" type="image/svg+xml">
<?= verificacion_html() . analytics_html() ?>
<script>window.FY_WA = <?= json_encode((strlen($w = preg_replace('/\\D/', '', (string) (cfg()['whatsapp'] ?? ''))) === 10 ? '57' : '') . $w) ?>;</script>
<script type="application/ld+json"><?php $ld = <<<'JSON'
{json.dumps({"@context": "https://schema.org", "@graph": [
    {"@type": "Store", "@id": "__BASE__/#tienda", "name": "__NOMBRE__", "url": "__BASE__/", "image": "__BASE__/img/compartir.jpg", "logo": "__BASE__/img/icono-512.png", "slogan": "Filtros de agua para nevera con envío gratis a toda Colombia", "priceRange": "$$", "areaServed": {"@type": "Country", "name": "Colombia"}, "currenciesAccepted": "COP", "paymentAccepted": "Tarjeta de crédito, tarjeta débito, PSE, Nequi", "sameAs": "__SAMEAS__"},
    {"@type": "WebSite", "name": "__NOMBRE__", "url": "__BASE__/", "inLanguage": "es-CO"},
    {"@type": "ItemList", "name": "Filtros de agua para nevecón", "itemListElement": marca_ld},
    paginas_seo.faq_ld(home_faq)]}, ensure_ascii=False)}
JSON;
echo str_replace(['__BASE__', '__NOMBRE__', '"__SAMEAS__"'], [$S['base'], addslashes($n['nombre']), json_encode(array_values(array_filter((array) (cfg()['redes'] ?? []))), JSON_UNESCAPED_SLASHES)], $ld); ?></script>
<link rel="alternate" type="text/plain" title="Resumen para asistentes de IA" href="/llms.txt">
<script>window.FY_WEB = <?= json_encode($S['web'], JSON_UNESCAPED_UNICODE | JSON_HEX_TAG) ?>;</script>
<script src="/carrito.js" defer></script>
<style>{CSS_WEB}
{CSS_COMUN}
{seo_busquedas.CSS_HOME}
footer.pie{{margin:24px 0 0;padding-bottom:84px}}footer.pie .medios{{display:flex;flex-wrap:wrap;gap:6px}}footer.pie .medios span{{border:1px solid rgba(255,255,255,.14);border-radius:6px;padding:3px 8px;font-size:12px;font-weight:700}}</style>
</head>
<body>
<?= gtm_body_html() . anuncio_html() ?>
{app}
{home_seo}
<?= pie_html() ?>
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


RUTAS_CIUDAD = {**{c[0]: f"/envios/{slug(c[1])}/{slug(c[0])}/" for c in CIUDADES_CO}}
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
    titulo = f'{p["nombre_largo"]} para nevera | Precio y envío gratis' if len(p['nombre_largo']) < 38 else f'{p["nombre_largo"]} | Precio y envío gratis'
    desc = (f'Compra el {p["nombre_largo"]} a {cop(p["precio"])} con envío gratis a toda Colombia en 2 días hábiles'
            + (f'. También aparece como {", ".join(alias[:3])}' if alias else "") + ". Paga con tarjeta, PSE o Nequi.")
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
    <ul class="ok"><li><b>Envío gratis</b> a toda Colombia: llega en 2 a 3 días hábiles a las principales ciudades.</li><li><b>Fácil de instalar:</b> paso a paso en esta página.</li><li>Pack anual de 2 filtros: {cop(p["pack"])} (ahorras {cop(ahorro)}).</li><li>Asesoría por WhatsApp para confirmar que es el de tu nevecón.</li></ul>
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
  <ul class="ok"><li>1 filtro de agua {esc(p["ref"])} nuevo, en su empaque (o 2 si escoges el pack anual).</li><li>Envío gratis a toda Colombia con número de guía.</li><li>Paso a paso de instalación y asesoría por WhatsApp.</li><li>Asesoría por WhatsApp para confirmar que es el de tu nevecón.</li></ul>
</section>
<section class="caja datos">
  <h2>Ficha técnica y datos rápidos</h2>
  <p>El <b>{esc(p["nombre_largo"])}</b> es el filtro de agua {"externo (va en la manguera)" if ubic(p) == "externo" else "interno"} para nevecones {esc(p["marca"])}{(", también conocido como " + esc(", ".join(alias[:5]))) if alias else ""}. Cuesta {cop(p["precio"])} en <?= h(cfg()['negocio']['nombre']) ?> con envío gratis a toda Colombia (2 a 3 días hábiles en las principales ciudades). Se cambia cada 6 meses.</p>
  <dl class="dq"><dt>Referencia</dt><dd>{esc(p["ref"])}</dd><dt>Marca del nevecón</dt><dd>{esc(p["marca"])}</dd><dt>Tipo</dt><dd>{"Externo, en la manguera" if ubic(p) == "externo" else "Interno"}</dd>
  <dt>Precio</dt><dd>{cop(p["precio"])} (pack de 2: {cop(p["pack"])})</dd><dt>Envío</dt><dd>Gratis a toda Colombia, 2 a 3 días hábiles en las principales ciudades</dd><dt>Instalación</dt><dd>{"En la manguera del agua, 10 a 15 minutos" if ubic(p) == "externo" else "Dentro del nevecón, 2 minutos sin herramientas"}</dd><dt>Duración</dt><dd>6 meses</dd>
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
{seo_busquedas.figura('agua')}
<section class="caja" id="opiniones"><h2>Opiniones de compradores</h2>
<?php if ($R['n']): ?><span><?= estrellas_html($R['prom']) ?> <b><?= $R['prom'] ?> de 5</b> · <?= $R['n'] ?> <?= $R['n'] === 1 ? 'opinión' : 'opiniones' ?> de compradores reales</span>
<?php foreach ($R['lista'] as $r): ?><div class="resena"><?= estrellas_html((float) $r['estrellas']) ?> <b><?= h($r['nombre']) ?></b> <span class="m">· <?= h($r['ciudad']) ?> · <?= h(date('d/m/Y', strtotime($r['creado']))) ?></span><?= $r['texto'] !== '' ? '<p style="margin:4px 0 0">' . h($r['texto']) . '</p>' : '' ?></div><?php endforeach; ?>
<?php else: ?><p class="m">Todavía no hay opiniones de este filtro. Después de tu compra te pediremos la tuya por correo.</p><?php endif; ?>
</section>
<section style="display:flex;flex-direction:column;gap:8px">
  <h2>Preguntas frecuentes</h2>
  <details><summary>¿Cuánto cuesta el envío?</summary><p>Nada. El envío es gratis a toda Colombia y llega en unos 2 a 3 días hábiles a las principales ciudades. Mira el <a href="/envios/">tiempo de entrega a tu ciudad</a>.</p></details>
  <details><summary>¿Es difícil de instalarlo?</summary><p>No. {"Se conecta en la manguera del agua en 10 a 15 minutos." if ubic(p) == "externo" else "Se cambia en 2 minutos y sin herramientas."} Sigue el paso a paso de esta página y, si tienes dudas, te asesoramos por WhatsApp.</p></details>
  <details><summary>¿Cómo pago?</summary><p>En línea, en página de pago segura: tarjeta débito o crédito, PSE, Nequi o botón Bancolombia. Te llega el recibo a tu correo.</p></details>
  <details><summary>¿Y si no me sirve?</summary><p>Tienes 5 días hábiles para retractarte con el filtro sin instalar, y la garantía legal si llega con un defecto de fábrica. Mira los <a href="/terminos.php#garantia">términos</a>.</p></details>
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
    desc = f"{INTRO.get(marca, '')} Envío gratis a toda Colombia. Paga con tarjeta, PSE o Nequi."
    pagina = cabeza_php("/../../partes.php", titulo, desc, f"/marca/{s}/", ld) + f"""
<nav class="miga"><a href="/">Inicio</a> › Filtros {esc(marca)}</nav>
<h1>Filtros de agua para nevecón {esc(marca)}</h1>
<p>{esc(INTRO.get(marca, ""))} Todos con <b>envío gratis</b> a toda Colombia y pago seguro en línea.</p>
<div class="grid">{"".join(tarjeta(p) for p in ps)}</div>
<section class="caja"><h2>Filtro de agua para nevera {esc(marca)}: lo que debes saber</h2>
<p>Las neveras y nevecones {esc(marca)} con dispensador de agua o máquina de hielo usan un filtro que se cambia <b>cada 6 meses</b>. Cada modelo usa una referencia propia ({esc(", ".join(p["ref"] for p in ps))}), así que lo importante es comprar la que corresponde a tu nevera: la encuentras impresa en el filtro viejo o por el modelo del refrigerador.</p>
<p>Aquí tienes los precios, cómo cambiarlo paso a paso, cómo apagar la luz del filtro y las causas de los problemas más comunes.</p>
<div class="chips">{"".join(f'<a href="{r}">{esc(t)}</a>' for r, t in seo_busquedas.temas(marca, s, any(ubic(p) == "externo" for p in ps)))}</div></section>
{seo_busquedas.ciudades_chips(marca, s, slug, CIUDADES_CO)}
<section class="caja"><h2>¿Cuál es el mío?</h2><p>Saca el filtro viejo y busca la referencia impresa, o mira el modelo en la etiqueta de adentro del nevecón. Escríbelo en el <a href="/#catalogo">buscador de la tienda</a> y te mostramos el filtro que le sirve.</p></section>
<?php pie(); ?>
"""
    d = OUT / "marca" / s
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.php").write_text(pagina, encoding="utf-8")

# ---------- referencias, nevecones, guías, envíos y directorios ----------
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
    "compat": [{"ruta": r, "titulo": t} for r, t in extra["compat"]],
    "blog": [{"ruta": r, "titulo": t} for r, t in extra["blog"]],
    "productos": {p["id"]: {"nombre": p["nombre_largo"], "ref": p["ref"], "marca": p["marca"], "precio": p["precio"], "pack": p["pack"], "slug": p["slug"], "alias": [r for r in p["refs"] if norm(r) != norm(p["ref"])],
                       "modelos": p["modelos"], "nota": p.get("nota", ""), "link_pago": p.get("linkPago", "") if p.get("linkMonto") == p["precio"] else "", "ubic": ubic(p), "rutas_ref": {r: ruta_ref[norm(r)] for r in p["refs"] if norm(r) in ruta_ref},
                       "rutas_modelo": {m: ruta_modelo[norm(m)] for m in p["modelos"]}} for p in CATALOGO},
}
(OUT / "api" / "catalogo.php").write_text("<?php\n// Generado por build.py: no lo edites a mano. Los precios se cambian en la app y se vuelve a generar.\nreturn " + php_val(cat_php) + ";\n", encoding="utf-8")

# ---------- carpetas con el nombre del proyecto ----------
# Todas las carpetas (y la hoja de estilos y el carrito) llevan "purofiltro-" adelante para no chocar
# con archivos que ya existan en el hosting. Se renombran al final y se corrigen todas las rutas.
CARPETAS = ["img", "api", "data", "filtro", "referencia", "referencias", "nevecon", "neveras", "marca", "guia", "envios", "tienda", "instalacion", "otras-marcas"]
for c in CARPETAS:
    viejo, nuevo = OUT / c, OUT / (PREFIJO + c)
    if not viejo.exists():
        continue
    if nuevo.exists():  # data/ de una generación anterior: se conservan los pedidos
        for f in viejo.iterdir():
            if not (nuevo / f.name).exists():
                shutil.move(str(f), nuevo / f.name)
        shutil.rmtree(viejo)
    else:
        viejo.rename(nuevo)
for f in ("estilo.css", "carrito.js"):
    (OUT / f).rename(OUT / (PREFIJO + f))
patron = re.compile(r"/(" + "|".join(CARPETAS) + r")/")
for f in OUT.rglob("*"):
    if not f.is_file() or f.suffix not in (".php", ".js", ".css", ".html", ".txt", ".xml", ".json", ".webmanifest", "") or PREFIJO + "data" in f.parts:
        continue
    t = f.read_text(encoding="utf-8")
    t2 = patron.sub(lambda m: "/" + PREFIJO + m.group(1) + "/", t)
    t2 = t2.replace("/estilo.css", "/" + PREFIJO + "estilo.css").replace("/carrito.js", "/" + PREFIJO + "carrito.js").replace("carrito.js']", PREFIJO + "carrito.js']")
    t2 = t2.replace("'/../data'", "'/../" + PREFIJO + "data'").replace("'filtro/'", "'" + PREFIJO + "filtro/'")
    t2 = re.sub(r"(?<![/\w-])api/config\.php", PREFIJO + "api/config.php", t2)
    if t2 != t:
        f.write_text(t2, encoding="utf-8")

print(f"Listo: {OUT.relative_to(AQUI)}/ con {len(CATALOGO)} filtros, {len(MARCAS)} marcas, {len(extra['refs']) - len(CATALOGO)} referencias equivalentes, "
      f"{len(extra['modelos'])} nevecones, {len(extra['guias'])} guías y {len(imgs)} fotos")


# ---------- un sitio por marca (cada uno va en su propio dominio) ----------
# sitios/<marca>/ es una tienda completa (carrito, pago, pedidos, legales) que solo vende esa marca.
# Lleva todo lo de la tienda principal menos sus páginas, y la portada y las fichas de la marca en la raíz.
SITIOS = AQUI / "sitios"
QUITAR = {"index.php", "llms.php", "sitemap.php", "manifest.webmanifest", "contacto.php", "politica-de-envios.php"} | {PREFIJO + c for c in CARPETAS if c not in ("img", "api", "data")}  # llms.php y sitemap.php se escriben aparte para cada marca
SITEMAP_MARCA = """<?php
require __DIR__ . '/%sapi/sitio.php';
header('Content-Type: application/xml; charset=utf-8');
$b = sitio()['base'];
$cat = catalogo();
$fotos = [];
foreach ($cat['productos'] as $id => $p) $fotos['/' . $p['slug'] . '/'] = "/%simg/$id.jpg";
$urls = array_fill_keys($cat['paginas'], '0.9') + ['/quienes-somos.php' => '0.4', '/terminos.php' => '0.2', '/privacidad.php' => '0.2', '/garantia-y-retracto.php' => '0.3'];
$urls['/'] = '1.0';
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n" . '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">' . "\n";
foreach ($urls as $u => $pr) echo '  <url><loc>' . htmlspecialchars($b . $u) . '</loc><lastmod>' . $cat['fecha'] . '</lastmod><priority>' . $pr . '</priority>'
    . (isset($fotos[$u]) ? '<image:image><image:loc>' . htmlspecialchars($b . $fotos[$u]) . '</image:loc></image:image>' : '') . "</url>\n";
echo '</urlset>';
""" % (PREFIJO, PREFIJO)
CAMBIOS_MARCA = {  # rutas de la tienda principal que en el sitio de la marca son otras
    "carrito.php": [("/purofiltro-filtro/${p.slug}/", "/${p.slug}/"), ('href="/purofiltro-tienda/"', 'href="/#filtros"')],
    "404.php": [('href="/#catalogo"', 'href="/#filtros"'), ('href="/purofiltro-referencias/"', 'href="/cual-es-mi-filtro/"'), ('href="/purofiltro-neveras/">Buscar por modelo', 'href="/cambio-e-instalacion/">Cómo instalarlo')],
    "quienes-somos.php": [('href="/purofiltro-guia/">Lee nuestras guías', 'href="/cambio-e-instalacion/">Cómo cambiar tu filtro'), ('href="/#catalogo"', 'href="/#filtros"')],
    "feed.php": [("$b/purofiltro-filtro/{$p['slug']}/", "$b/{$p['slug']}/")],
    PREFIJO + "api/recordatorios.php": [("'" + PREFIJO + "filtro/' . $cat[$p['pid']]['slug'] . '/'", "$cat[$p['pid']]['slug'] . '/'")],
}
for marca in marcas_exclusivas.MARCAS_INFO:
    s = slug(marca)
    d = SITIOS / s
    ids = {p["id"] for p in CATALOGO if p["marca"] == marca}
    if d.exists():  # los pedidos de purofiltro-data/ nunca se borran
        for hijo in d.iterdir():
            if hijo.name not in ("data", PREFIJO + "data"):
                shutil.rmtree(hijo) if hijo.is_dir() else hijo.unlink()
    d.mkdir(parents=True, exist_ok=True)
    for f in OUT.iterdir():
        if f.name in QUITAR or f.name == PREFIJO + "data" and ((d / "data").exists() or (d / f.name).exists()):
            continue
        if f.is_dir():
            shutil.copytree(f, d / f.name, dirs_exist_ok=True, ignore=shutil.ignore_patterns("pedidos.sqlite*", "correos.log", "config.php") if f.name in (PREFIJO + "data", PREFIJO + "api") else None)
        else:
            shutil.copy2(f, d / f.name)
    for f in (d / (PREFIJO + "img")).iterdir():  # solo las fotos de la marca
        if f.name != "icono.svg" and f.name.split(".")[0].removesuffix("-400") not in ids:
            f.unlink()
    logo = None
    if (AQUI / "logos" / f"{s}-web.png").exists():  # somos distribuidor autorizado: cada sitio lleva el logo de su marca
        shutil.copy(AQUI / "logos" / f"{s}-web.png", d / (PREFIJO + "img") / f"logo-{s}.png")
        lw, lh = Image.open(AQUI / "logos" / f"{s}-web.png").size
        logo = {"logo": f"/{PREFIJO}img/logo-{s}.png", "logo_w": lw, "logo_h": lh}
        if (AQUI / "logos" / f"{s}-icono.png").exists():
            shutil.copy(AQUI / "logos" / f"{s}-icono.png", d / (PREFIJO + "img") / f"icono-{s}.png")
            logo["icono"] = f"/{PREFIJO}img/icono-{s}.png"
    rutas, M = marcas_exclusivas.generar_marca(marca, d, "/", CATALOGO, slug, norm, ubic, foto, php_str, CIUDADES_CO, logo)
    (d / "purofiltro-marca.json").write_text(json.dumps(M, ensure_ascii=False), encoding="utf-8")
    (d / "sitemap.php").write_text(SITEMAP_MARCA, encoding="utf-8")
    # resumen en texto para asistentes de IA (ChatGPT, Gemini, Claude, Perplexity): tudominio.com/llms.txt
    ps_m = [p for p in CATALOGO if p["marca"] == marca]
    llms = (f"# Filtros {marca} en Colombia\n\n"
            f"> Distribuidor autorizado de filtros de agua {marca} para nevera/nevecón. Envío gratis a toda Colombia "
            "(2 a 3 días hábiles en las principales ciudades), pago en línea con tarjeta, PSE o Nequi, asesoría por WhatsApp.\n\n"
            "## Filtros y precios (COP, envío incluido)\n"
            + "".join(f"- [{p['nombre_largo']}](__BASE__/{p['slug']}/): {cop(p['precio'])}; pack de 2 {cop(p['pack'])}. "
                      f"Referencias equivalentes: {', '.join(p['refs'])}." + (f" Neveras: {', '.join(p['modelos'])}." if p["modelos"] else "") + "\n" for p in ps_m)
            + "\n## Guías\n" + "".join(f"- [{n}](__BASE__{r})\n" for r, n in M["guias"])
            + "- [¿Cuál filtro es el mío? (por modelo o referencia)](__BASE__/cual-es-mi-filtro/)\n- [Cómo cambiar e instalar cada filtro](__BASE__/cambio-e-instalacion/)\n"
            + "\n## Compra\n- Envío gratis a toda Colombia con número de guía.\n- Pago en línea seguro; no hay pago contra entrega.\n- 5 días hábiles de retracto con el filtro sin instalar.\n"
              "- Términos: __BASE__/terminos.php\n")
    if marca == "Whirlpool":
        import marcas_contenido
        X = marcas_contenido.rutas("/", slug)
        llms += ("\n## Marcas de nevera a las que les sirven estos filtros (para qué neveras sirven)\n"
                 "- Filtros EveryDrop 1 a 5: neveras Whirlpool, Maytag (también escrito MyTag), KitchenAid (Kitchen Aid), Jenn-Air y Amana, según el modelo; Kenmore tiene referencias equivalentes (46-9930, 46-9081, 46-9030, 46-9006, 46-9010).\n"
                 "- Filtro externo 4378411RB: se conecta a la manguera del agua y sirve en neveras con dispensador de varias marcas (Samsung, LG, GE, Mabe, Haceb, Challenger, Electrolux, Frigidaire, Bosch, Hisense, Midea, Panasonic, Daewoo, Estate).\n"
                 + "".join(f"- [{t}](__BASE__{r})\n" for m_, l in X["familia"].items() for r, t in l[:1]) + f"- [Todas las marcas](__BASE__{X['hub']})\n"
                 "\n## Preguntas y respuestas\n" + "".join(f"- **{q}** {a_}\n" for _, l in marcas_contenido.preguntas_ia(ps_m, slug) for q, a_ in l)
                 + f"\n## Blog\n- [Blog de filtros Whirlpool](__BASE__{X['blog']})\n" + "".join(f"- [{t}](__BASE__/blog/{sl}/): {d_}\n" for sl, t, d_, _, _, _ in marcas_contenido.articulos(ps_m))
                 + f"- [Preguntas frecuentes](__BASE__{X['faq']})\n")
    (d / "llms.php").write_text("<?php\nrequire __DIR__ . '/" + PREFIJO + "api/sitio.php';\nheader('Content-Type: text/plain; charset=utf-8');\necho str_replace('__BASE__', sitio()['base'], <<<'TXT'\n" + llms + "TXT);\n", encoding="utf-8")
    cat_m = dict(cat_php, paginas=rutas, guias=[], compat=[], blog=[], rutas_ciudad={}, marcas=[{"nombre": marca, "slug": s}],
                 productos={k: v for k, v in cat_php["productos"].items() if k in ids})
    (d / (PREFIJO + "api") / "catalogo.php").write_text("<?php\n// Generado por build.py para el sitio de " + marca + ": no lo edites a mano.\nreturn " + php_val(cat_m) + ";\n", encoding="utf-8")
    for nombre, cambios in CAMBIOS_MARCA.items():
        f = d / nombre
        txt = f.read_text(encoding="utf-8")
        for a, b_ in cambios:
            if a not in txt:
                sys.exit(f"{nombre}: no encontré {a!r}")
            txt = txt.replace(a, b_)
        f.write_text(txt, encoding="utf-8")
    # rutas sin prefijo de las páginas nuevas (img, carrito.js) igual que en la tienda principal
    for f in d.rglob("*.php"):
        if PREFIJO + "data" in f.parts:
            continue
        txt = f.read_text(encoding="utf-8")
        t2 = re.sub(r"/(img|api)/", lambda m: "/" + PREFIJO + m.group(1) + "/", txt).replace('"/carrito.js"', '"/' + PREFIJO + 'carrito.js"').replace("'/estilo.css'", "'/" + PREFIJO + "estilo.css'").replace('href="/estilo.css"', 'href="/' + PREFIJO + 'estilo.css"')
        if t2 != txt:
            f.write_text(t2, encoding="utf-8")
    # la hoja de estilo solo lleva los colores de esta marca
    css = (d / "purofiltro-marcas.css").read_text(encoding="utf-8")
    bloques = re.split(r"(?=/\* ===== )|(?=/\* Páginas comunes)", css)
    css = "".join(x for x in bloques if not x.startswith("/* ===== ") or x.startswith(f"/* ===== {marca}:"))
    (d / "purofiltro-marcas.css").write_text(css, encoding="utf-8")
    sobran = [x.name for x in d.iterdir() if x.name in QUITAR and x.name not in ("index.php", "llms.php", "sitemap.php")]
    if sobran:  # el sitio de una marca nunca debe llevar páginas de la tienda principal (tienen las otras marcas)
        sys.exit(f"Sitio {marca}: sobran {sobran}")
    # En su propio dominio no hace falta el prefijo: img/, api/, data/, carrito.js... (el negocio ya no se llama PuroFiltro)
    for x in list(d.iterdir()):
        if x.name.startswith(PREFIJO):
            destino = d / x.name[len(PREFIJO):]
            if x.name == PREFIJO + "data" and destino.exists():
                shutil.rmtree(x)
            else:
                x.rename(destino)
    for f in d.rglob("*"):
        if f.is_file() and "data" not in f.relative_to(d).parts[:1] and f.suffix in (".php", ".js", ".css", ".json", ".txt", ".xml", ".html", "") :
            txt = f.read_text(encoding="utf-8")
            if PREFIJO in txt or "Filtros Nevecones Colombia" in txt:
                f.write_text(txt.replace(PREFIJO, "").replace("Filtros Nevecones Colombia", M["tienda"]), encoding="utf-8")
    print(f"Sitio {marca}: sitios/{s}/ con {len(rutas)} páginas")
