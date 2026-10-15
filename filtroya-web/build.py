#!/usr/bin/env python3
"""Genera la tienda FiltroYa para Hostinger (carpeta public_html/) a partir de la app de Claude.

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
ciudades = node_eval(f'[...{js_valor("CALI_METRO")}, ...{js_valor("PRINCIPALES")}, "Otro municipio"]')
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
for pid, url in imgs.items():
    (OUT / "img" / f"{pid}.jpg").write_bytes(base64.b64decode(url.split(",", 1)[1]))
app = app.replace(m.group(1), json.dumps({pid: f"/img/{pid}.jpg" for pid in imgs}))
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
app = cambiar(app, "<b>Paga fácil</b>Nequi, Bancolombia o llave Bre-B", "<b>Pago seguro</b>Tarjeta, PSE, Nequi o Bancolombia con Wompi", 3)
app = cambiar_re(app, r'<details class="faq"><summary>¿Cada cuánto se cambia el filtro\?</summary><p>.*?</p></details>',
                 '<details class="faq"><summary>¿Cada cuánto se cambia el filtro?</summary><p>Cada 6 meses, o antes si el agua cambia de sabor, de olor o sale con poca presión. Al comprar te podemos recordar por correo.</p></details>')
app = cambiar_re(app, r'<details class="faq"><summary>¿Cómo sé cuál es el mío\?</summary><p>.*?</p></details>',
                 '<details class="faq"><summary>¿Cómo sé cuál es el mío?</summary><p>Busca la referencia impresa en tu filtro viejo o el modelo en la etiqueta de adentro del nevecón y escríbela en el buscador. Si no aparece, escríbenos al correo con la foto.</p></details>')
app = cambiar_re(app, r'<details class="faq"><summary>¿Cómo se confirma mi pedido\?</summary><p>.*?</p></details>',
                 '<details class="faq"><summary>¿Cómo compro?</summary><p>Escoges tu filtro, pones tus datos de entrega y pagas en línea en la página segura de Wompi. Te llega el recibo a tu correo y despachamos tu pedido.</p></details>')
app = cambiar_re(app, r'<details class="faq"><summary>¿Cómo pago\?</summary><p>.*?</p></details>',
                 '<details class="faq"><summary>¿Cómo pago?</summary><p>En línea con Wompi (de Bancolombia): tarjeta débito o crédito, PSE, Nequi o botón Bancolombia. No guardamos los datos de tu tarjeta.</p></details>')
# Pago: solo Wompi
app = cambiar(app, 'contra: { t: "Contra entrega", sub: "", logo: "" },', 'wompi: { t: "Pago en línea con Wompi", sub: "", logo: "" },')
app = cambiar(app, 'pago: "nequi", entrega: null', 'pago: "wompi", entrega: null')
app = cambiar_re(app, r'\$\{\["nequi", "bancolombia", "llave"\]\.map\(k => `<label><input type="radio" name="pago".*?\.join\(""\)\}',
                 '<div class="paywompi">${ICON.shield}<span><b>Pago seguro en línea con Wompi</b><small>Tarjeta débito o crédito, PSE, Nequi o botón Bancolombia. Pagas al final, en la página segura de Wompi.</small></span></div>')
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
app = cambiar(app, '<a class="btn wa block" id="c-confirm" href="${waLink(orderMessage())}" target="_blank" rel="noopener">${ICON.wa}Enviar pedido a un asesor por WhatsApp</a>',
              '<button class="btn block" type="button" id="c-pagar">${ICON.shield}Pagar ${COP(t.total)} con Wompi</button><p class="err" id="c-perr" aria-live="polite"></p>')
app = cambiar_re(app, r'<p class="sub" style="font-size:12\.5px;margin:0">Se abre WhatsApp con tu pedido escrito.*?</p>`\);',
                 '<p class="sub" style="font-size:12.5px;margin:0">Te llevamos a la página segura de Wompi (de Bancolombia). Precio final: no hay cobros adicionales. Al pagar aceptas los <a href="/terminos.php" target="_blank">Términos y condiciones</a> y autorizas el tratamiento de tus datos según la <a href="/privacidad.php" target="_blank">Política de datos</a>.</p>`);')
# Recordatorio en calendario sin la capacidad de descargas de Claude
app = cambiar(app, 'if (!downloads) { msg.textContent = "Para guardar el recordatorio abre la app dentro de Claude."; return; }',
              'if (!downloads) { const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([ics], { type: "text/calendar" })); a.download = "recordatorio-filtro.ics"; document.body.append(a); a.click(); a.remove(); msg.textContent = "Listo: abre el archivo para agregarlo a tu calendario."; return; }', 2)

# Pago con Wompi, enlace directo a un producto (?p=) y marca (?marca=)
WEB_JS = r'''
/* ===================== TIENDA WEB: PAGO CON WOMPI ===================== */
document.addEventListener("click", async e => {
  const b = e.target.closest("#c-pagar"); if (!b || !cart) return;
  const t = totals(), k = cart.cli, old = b.innerHTML;
  b.disabled = true; b.textContent = "Conectando con Wompi…"; $("#c-perr").textContent = "";
  try {
    const r = await fetch(FY_WEB.api + "pedido.php", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({
      pid: cart.p.id, cantidad: t.unidades, pack: cart.pack, entrega: cart.entrega, total: t.total,
      cliente: { nombre: k.nombre, email: k.email, tel: k.wa, ciudad: k.ciudad, barrio: k.barrio, dir: k.dir, indicaciones: k.indicaciones, modelo: k.modelo, recordar: !!k.recordar } }) });
    const j = await r.json().catch(() => ({}));
    if (!r.ok || !j.url) throw new Error(j.mensaje || "No se pudo crear el pedido. Intenta de nuevo.");
    store.set("fy_cliente", { nombre: k.nombre, tel: k.tel, email: k.email, dir: k.dir, barrio: k.barrio, recordar: k.recordar });
    const cambio = new Date(); cambio.setMonth(cambio.getMonth() + NEGOCIO.mesesCambio);
    const orders = store.get("fy_orders", []).filter(o => o.id !== j.ref);
    orders.unshift({ id: j.ref, fecha: new Date().toISOString(), cambio: cambio.toISOString(), producto: cart.p.nombre, ref: cart.p.ref, pid: cart.p.id, qty: t.unidades, pack: cart.pack, ciudad: k.ciudad, entrega: cart.entrega, pago: "wompi", total: j.total, eta: delivery(k.ciudad, cart.p).corto, estado: "Pago pendiente", cliente: { recordar: !!k.recordar } });
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

# Enlaces fijos a todas las páginas de filtros (Google los sigue aunque no ejecute el JavaScript)
enlaces = ['<nav class="seo-links" aria-label="Todos los filtros"><h2 style="font-size:19px">Todos nuestros filtros</h2>']
for marca in MARCAS:
    ps = [p for p in CATALOGO if p["marca"] == marca]
    enlaces.append(f'<div><a class="mk" href="/marca/{slug(marca)}/">Filtros {esc(marca)}</a>' + "".join(f'<a href="/filtro/{p["slug"]}/">{esc(p["nombre_largo"])}</a>' for p in ps) + "</div>")
enlaces.append('</nav><footer class="web-foot"><a href="/terminos.php">Términos y condiciones</a><a href="/privacidad.php">Tratamiento de datos</a><a href="/terminos.php#garantia">Garantía y retracto</a><span id="pie-negocio"></span></footer>')
i = app.index('<details class="faq"><summary>¿Cómo pago?</summary>')
j = app.index("</div>", i) + len("</div>")
app = app[:j] + "\n  " + "".join(enlaces) + app[j:]

CSS_WEB = """
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
<script type="application/ld+json"><?php $ld = <<<'JSON'
{json.dumps({"@context": "https://schema.org", "@graph": [
    {"@type": "Store", "@id": "__BASE__/#tienda", "name": "__NOMBRE__", "url": "__BASE__/", "image": "__BASE__/img/lg-1000-o.jpg", "address": {"@type": "PostalAddress", "addressLocality": "Cali", "addressRegion": "Valle del Cauca", "addressCountry": "CO"}, "areaServed": "CO", "currenciesAccepted": "COP", "paymentAccepted": "Tarjeta de crédito, tarjeta débito, PSE, Nequi"},
    {"@type": "WebSite", "name": "__NOMBRE__", "url": "__BASE__/", "inLanguage": "es-CO"},
    {"@type": "ItemList", "name": "Filtros de agua para nevecón", "itemListElement": marca_ld}]}, ensure_ascii=False)}
JSON;
echo str_replace(['__BASE__', '__NOMBRE__'], [$S['base'], addslashes($n['nombre'])], $ld); ?></script>
<script>window.FY_WEB = <?= json_encode($S['web'], JSON_UNESCAPED_UNICODE | JSON_HEX_TAG) ?>;</script>
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
    return (f'<a class="card" href="/filtro/{p["slug"]}/"><span class="im"><img src="/img/{p["id"]}.jpg" alt="{esc(p["nombre_largo"])}" loading="lazy"></span>'
            f'<b>{esc(p["nombre_largo"])}</b><span class="p">{cop(p["precio"])}</span><span class="m">Envío gratis</span></a>')


def php_str(s):
    return "'" + str(s).replace("\\", "\\\\").replace("'", "\\'") + "'"


def cabeza_php(partes, titulo, desc, ruta, ld):
    """Inicio de una página PHP: datos estructurados para Google con el dominio real."""
    return (f"<?php require __DIR__ . '{partes}';\n$ld = <<<'JSON'\n{json.dumps(ld, ensure_ascii=False)}\nJSON;\n"
            f"cabeza({php_str(titulo)}, {php_str(desc)}, {php_str(ruta)}, '<script type=\"application/ld+json\">' . str_replace('__BASE__', sitio()['base'], $ld) . '</script>'); ?>")


for p in CATALOGO:
    alias = [r for r in p["refs"] if norm(r) != norm(p["ref"])]
    otros = [x for x in CATALOGO if x["marca"] == p["marca"] and x["id"] != p["id"]][:6]
    donde = "Va en la manguera de agua, por fuera del nevecón." if ubic(p) == "externo" else "Va por dentro del nevecón."
    ahorro = p["precio"] * 2 - p["pack"]
    titulo = f'{p["nombre_largo"]} | Envío gratis a toda Colombia'
    desc = (f'Compra el {p["nombre_largo"]} a {cop(p["precio"])} con envío gratis a toda Colombia en 2 días hábiles'
            + (f'. También aparece como {", ".join(alias[:3])}' if alias else "") + ". En Cali te lo instalamos gratis. Paga con tarjeta, PSE o Nequi.")
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Product", "name": p["nombre_largo"], "image": f"__BASE__/img/{p['id']}.jpg", "sku": p["ref"], "mpn": p["ref"],
         "brand": {"@type": "Brand", "name": p["marca"]}, "description": f'Filtro de agua para nevecón {p["marca"]}, referencia {p["ref"]}. {donde}',
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
            {"@type": "ListItem", "position": 3, "name": p["nombre_largo"], "item": f"__BASE__/filtro/{p['slug']}/"}]}]}
    pagina = cabeza_php("/../../partes.php", titulo, desc, f'/filtro/{p["slug"]}/', ld) + f"""
<nav class="miga"><a href="/">Inicio</a> › <a href="/marca/{slug(p["marca"])}/">Filtros {esc(p["marca"])}</a> › {esc(p["nombre_largo"])}</nav>
<div class="prod">
  <div class="foto"><img src="/img/{p["id"]}.jpg" alt="{esc(p["nombre_largo"])} para nevecón {esc(p["marca"])}" width="600" height="600"></div>
  <div class="caja">
    <h1>{esc(p["nombre_largo"])}</h1>
    <span class="m">Filtro de agua para nevecón {esc(p["marca"])} · {"Externo" if ubic(p) == "externo" else "Interno"} · Referencia <span class="ref">{esc(p["ref"])}</span></span>
    <span class="precio">{cop(p["precio"])}</span>
    <ul class="ok"><li><b>Envío gratis</b> a toda Colombia: llega en 2 días hábiles.</li><li>En Cali: <b>domicilio e instalación gratis</b>.</li><li>Pack anual de 2 filtros: {cop(p["pack"])} (ahorras {cop(ahorro)}).</li><li>Garantía de 30 días: si no encaja, te lo cambiamos.</li></ul>
    <a class="btn block" href="/?p={p["id"]}">Comprar</a>
    <span class="m">Pago seguro con Wompi: tarjeta débito o crédito, PSE, Nequi o botón Bancolombia.</span>
  </div>
</div>
<section class="caja">
  <h2>¿Es el filtro de tu nevecón?</h2>
  <p>Busca esta referencia impresa en tu filtro viejo: <span class="ref">{esc(p["ref"])}</span>. {esc(donde)}</p>
  {f'<p>También aparece como:</p><div class="chips">{"".join(f"<span>{esc(r)}</span>" for r in alias)}</div>' if alias else ""}
  {f'<p>Sirve para estos nevecones, entre otros: <b>{esc(", ".join(p["modelos"]))}</b>.</p>' if p["modelos"] else ""}
  {f'<p>{esc(p["nota"])}</p>' if p.get("nota") else ""}
  <p>Cámbialo cada 6 meses, o antes si el agua cambia de sabor, de olor o sale con poca presión.</p>
</section>
<section style="display:flex;flex-direction:column;gap:8px">
  <h2>Preguntas frecuentes</h2>
  <details><summary>¿Cuánto cuesta el envío?</summary><p>Nada. El envío es gratis a toda Colombia y llega en unos 2 días hábiles después del pago.</p></details>
  <details><summary>¿Lo instalan?</summary><p>En Cali te lo llevamos e instalamos gratis. En otras ciudades te lo enviamos con las instrucciones: se instala en minutos, sin herramientas.</p></details>
  <details><summary>¿Cómo pago?</summary><p>En línea con Wompi (de Bancolombia): tarjeta débito o crédito, PSE, Nequi o botón Bancolombia. Te llega el recibo a tu correo.</p></details>
  <details><summary>¿Y si no me sirve?</summary><p>Tienes 5 días hábiles para retractarte con el filtro sin instalar, y 30 días de garantía si no encaja o llega con un defecto. Mira los <a href="/terminos.php#garantia">términos</a>.</p></details>
</section>
{f'<section style="display:flex;flex-direction:column;gap:10px"><h2>Otros filtros {esc(p["marca"])}</h2><div class="grid">{"".join(tarjeta(x) for x in otros)}</div></section>' if otros else ""}
<?php pie(); ?>
"""
    d = OUT / "filtro" / p["slug"]
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.php").write_text(pagina, encoding="utf-8")

# ---------- páginas por marca ----------
INTRO = {
    "Samsung": "Filtros de agua para nevecones Samsung de dos puertas y French door: internos (HAF-CIN, HAF-QIN, Aqua-Pure) y el externo de manguera.",
    "LG": "Filtros de agua para nevecones LG: LT1000P, LT700P, LT800P, LT500P, LT600P y el externo de manguera.",
    "Whirlpool": "Filtros EveryDrop para nevecones Whirlpool, Maytag, KitchenAid, Jenn-Air y Amana: del 1 al 5.",
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
    "marcas": [{"nombre": m, "slug": slug(m)} for m in MARCAS],
    "productos": {p["id"]: {"nombre": p["nombre_largo"], "ref": p["ref"], "marca": p["marca"], "precio": p["precio"], "pack": p["pack"], "slug": p["slug"]} for p in CATALOGO},
}
(OUT / "api" / "catalogo.php").write_text("<?php\n// Generado por build.py: no lo edites a mano. Los precios se cambian en la app y se vuelve a generar.\nreturn " + php_val(cat_php) + ";\n", encoding="utf-8")

print(f"Listo: {OUT.relative_to(AQUI)}/ con {len(CATALOGO)} filtros, {len(MARCAS)} marcas y {len(imgs)} fotos")
