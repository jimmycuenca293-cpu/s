#!/usr/bin/env python3
"""filtrodeaguasamsung.com (sitio HTML estático que ya está en Google Ads): le agrega carrito, pasarela de pagos (Wompi),
pedidos por correo y hoja de cálculo, confirmación al cliente y mejoras de SEO, SIN cambiar sus textos, diseño, direcciones ni etiquetas.

Uso:  python3 ads22.py <public_html_22.zip> <carpeta_de_salida>
La carpeta de salida queda lista para subir a public_html (sin config.php y sin pedidos).
"""
import datetime
import html
import json
import pathlib
import re
import shutil
import sys
import zipfile

from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
SRC_ZIP, OUT = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
HOY = datetime.date.today().isoformat()
DOMINIO = "https://filtrodeaguasamsung.com"
TOKEN_GSC = "82OYND3le6w8UJopCSGa_ge39KLuH_feDaw1AUrFIZU"

# Los 3 filtros del sitio, con sus links de pago de Wompi (los que ya usa) y sus páginas
PRODUCTOS = {
    "cin": dict(nombre="Filtro de agua Samsung HAF-CIN/EXP", corto="HAF-CIN/EXP", ref="DA29-00020B", precio=139900, link="MEGm9S",
                img="img/filtro-haf-cin-exp.png", url="filtro-haf-cin.html", ubic="interno", alias=["DA29-00020A", "HAF-CIN", "HAF-CIN/EXP", "46-9101"]),
    "qin": dict(nombre="Filtro de agua Samsung HAF-QIN/EXP", corto="HAF-QIN/EXP", ref="DA97-17376B", precio=139900, link="oogWOK",
                img="img/filtro-haf-qin-exp.png", url="filtro-haf-qin.html", ubic="interno", alias=["DA97-08006C", "HAF-QIN", "HAF-QIN/EXP"]),
    "ext": dict(nombre="Filtro externo Samsung DA29-10105J", corto="Externo DA29-10105J", ref="DA29-10105J", precio=79900, link="bjU3bv",
                img="img/filtro-externo-da29-10105j.png", url="filtro-externo.html", ubic="externo", alias=["HAFEX", "HAFEX/EXP", "WSF-100"]),
}
LINK_A_ID = {p["link"]: k for k, p in PRODUCTOS.items()}

# ---------- 1. el sitio de partida ----------
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True)
with zipfile.ZipFile(SRC_ZIP) as z:
    z.extractall(OUT.parent / (OUT.name + "_tmp"))
raiz = OUT.parent / (OUT.name + "_tmp") / "public_html"
shutil.rmtree(OUT)
shutil.move(str(raiz), str(OUT))
shutil.rmtree(OUT.parent / (OUT.name + "_tmp"), ignore_errors=True)

# los precios del sitio y los del carrito tienen que ser los mismos
for k, p in PRODUCTOS.items():
    t = (OUT / p["url"]).read_text(encoding="utf-8")
    assert f'"price": "{p["precio"]}"' in t, f"el precio de {p['url']} no coincide con {p['precio']}"
    assert f"checkout.wompi.co/l/{p['link']}" in t, f"falta el link de Wompi de {p['url']}"

# ---------- 2. servidor: pedidos, correo, hoja y pasarela (usa el código de las otras tiendas) ----------
SRC = AQUI / "src"
api = OUT / "api"
api.mkdir()
for f in ("lib.php", "pedido.php", "estado.php", "wompi.php", "sitio.php", "reconciliar.php"):
    shutil.copy(SRC / "api" / f, api / f)
lib = (api / "lib.php").read_text(encoding="utf-8")
lib = lib.replace("w-s2eiVewLzOHFjK7HAR9UUeqFoNMS14k_Gfrqt_ND4", TOKEN_GSC)  # etiqueta de Search Console de ESTE dominio
(api / "lib.php").write_text(lib, encoding="utf-8")
(OUT / "data").mkdir()
(OUT / "data" / ".htaccess").write_text("Require all denied\n")
(api / ".htaccess").write_text('<FilesMatch "^(config|config\\.sample|lib|catalogo|sitio)\\.php$">\nRequire all denied\n</FilesMatch>\n')

# catálogo: solo los 3 filtros, con sus links de pago (la ciudad y los días de entrega vienen de las otras tiendas)
import subprocess
base = json.loads(subprocess.run(["php", "-r", f'echo json_encode(require "{AQUI}/sitios/samsung/api/catalogo.php");'], capture_output=True, text=True, check=True).stdout)
prods = {}
for k, p in PRODUCTOS.items():
    prods[k] = {"nombre": p["nombre"], "ref": p["ref"], "marca": "Samsung", "precio": p["precio"], "pack": p["precio"] * 2, "slug": p["url"].replace(".html", ""), "alias": p["alias"],
                "modelos": [], "nota": "", "link_pago": f"https://checkout.wompi.co/l/{p['link']}", "ubic": p["ubic"], "url": p["url"], "img": p["img"]}
cat = {"fecha": HOY, "ciudades": base["ciudades"], "dias": base.get("dias", {}), "rutas_ciudad": {}, "marcas": [], "paginas": [], "guias": [], "compat": [], "blog": [], "productos": prods}


def php_val(v, n=0):
    if isinstance(v, dict):
        return "[" + ", ".join(f"{php_val(k)} => {php_val(x)}" for k, x in v.items()) + "]"
    if isinstance(v, list):
        return "[" + ", ".join(php_val(x) for x in v) + "]"
    if isinstance(v, bool):
        return "true" if v else "false"
    if v is None:
        return "null"
    if isinstance(v, (int, float)):
        return str(v)
    return "'" + str(v).replace("\\", "\\\\").replace("'", "\\'") + "'"


(api / "catalogo.php").write_text("<?php\n// Generado por ads22.py: no lo edites a mano.\nreturn " + php_val(cat) + ";\n", encoding="utf-8")

cfg = (SRC / "api" / "config.sample.php").read_text(encoding="utf-8")
cfg = (cfg.replace("'dominio' => 'https://filtrosnevecones.com'", f"'dominio' => '{DOMINIO}'")
          .replace("w-s2eiVewLzOHFjK7HAR9UUeqFoNMS14k_Gfrqt_ND4", TOKEN_GSC)
          .replace("'nombre'    => 'Filtros Nevecones Colombia'", "'nombre'    => 'Filtro de Agua Samsung Colombia'")
          .replace("'whatsapp' => '3107147299'", "'whatsapp' => '3054796329'")
          .replace("'telefono'  => '310 714 7299'", "'telefono'  => '305 479 6329'")
          .replace("'contraentrega' => ['activo' => true, 'recargo' => 5000]", "'contraentrega' => ['activo' => true, 'recargo' => 0]"))
(api / "config.sample.php").write_text(cfg, encoding="utf-8")

# páginas del servidor
shutil.copy(SRC / "estilo.css", OUT / "estilo.css")
shutil.copy(SRC / "carrito.js", OUT / "carrito.js")
for f in ("carrito.php", "gracias.php", "admin.php", "diagnostico.php", "terminos.php", "privacidad.php", "garantia-y-retracto.php", "opinion.php"):
    shutil.copy(SRC / f, OUT / f)

c = (OUT / "carrito.php").read_text(encoding="utf-8")
# el carrito apunta a las páginas y fotos de ESTE sitio
c = c.replace("'ref' => $p['ref'], 'marca' => $p['marca']", "'ref' => $p['ref'], 'url' => $p['url'] ?? '', 'img' => $p['img'] ?? '', 'marca' => $p['marca']", 1)
c = re.sub(r'<a class="lim" href=.*?</picture></a>', '<a class="lim" href="/${p.url}"><img src="/${p.img}" alt="${esc(p.nombre)}" width="96" height="96" style="object-fit:contain"></a>', c, flags=re.S)
c = re.sub(r'<a href="/\$\{p\.marca\.toLowerCase\(\).*?/\$\{p\.slug\}/">', '<a href="/${p.url}">', c)
c = c.replace('href="/tienda/"', 'href="/index.html#catalogo"')
assert "'url' => $p['url']" in c and "${p.url}" in c and "p.marca.toLowerCase" not in c, "no se pudieron cambiar los enlaces del carrito"
(OUT / "carrito.php").write_text(c, encoding="utf-8")
for f in ("carrito.php", "gracias.php", "terminos.php", "privacidad.php", "garantia-y-retracto.php", "opinion.php", "admin.php"):
    t = (OUT / f).read_text(encoding="utf-8")
    t = t.replace('href="/tienda/"', 'href="/index.html#catalogo"').replace('href="/envios/"', 'href="/envio-filtros-samsung-colombia.html"')
    (OUT / f).write_text(t, encoding="utf-8")

(OUT / "partes.php").write_text(r"""<?php
// Cabecera y pie de las páginas de compra (carrito, gracias, legales) con el mismo estilo del sitio.
require_once __DIR__ . '/api/sitio.php';
function marca_sitio(): ?array { return null; }
function seo_titulo(string $t): string { return $t; }
function seo_desc(string $d): string { return $d; }
function cabeza(string $titulo, string $desc, string $ruta, string $extra = '', bool $indexar = true): void
{
    $S = sitio();
    $canon = $S['base'] . $ruta;
    echo '<!doctype html><html lang="es-CO"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        . '<title>' . h($titulo) . '</title><meta name="description" content="' . h($desc) . '">'
        . ($indexar ? '<link rel="canonical" href="' . h($canon) . '">' : '<meta name="robots" content="noindex,nofollow">')
        . '<link rel="icon" href="/img/samsung-logo-oval.png"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        . '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;500;600;700&display=swap">'
        . '<link rel="stylesheet" href="/estilo.css"><link rel="stylesheet" href="/pasarela.css"><script src="/carrito.js" defer></script>'
        . verificacion_html() . analytics_html() . $extra . '</head><body class="tienda-samsung">' . gtm_body_html()
        . '<header class="top"><div class="wrap"><a class="logo" href="/index.html" aria-label="Filtro de agua Samsung"><img src="/img/samsung-logo-oval.png" alt="Samsung" width="104" height="35" style="height:34px;width:auto"><small>Filtro de Agua Original</small></a>'
        . '<nav class="nv"><a href="/index.html#catalogo">Ver filtros</a><a class="carro" href="/carrito.php" aria-label="Ver carrito">🛒 <span data-cart-n hidden></span></a></nav></div></header><main class="wrap">';
}
function pie_html(): string
{
    $n = sitio()['negocio'];
    return '</main><footer class="pie"><div class="wrap"><nav><a href="/index.html">Inicio</a><a href="/envio-filtros-samsung-colombia.html">Envíos</a><a href="/garantia-y-retracto.php">Garantía y retracto</a><a href="/terminos.php">Términos</a><a href="/privacidad.php">Datos personales</a></nav>'
        . '<p>© ' . date('Y') . ' ' . h($n['nombre']) . '. Precios en pesos colombianos con envío incluido. Samsung es una marca registrada de su dueño; se menciona solo para indicar en qué nevecones sirve cada filtro.</p></div></footer></body></html>';
}
function pie(): void { echo pie_html(); }
""", encoding="utf-8")

# estilos de la pasarela y del carrito en las páginas estáticas
(OUT / "pasarela.css").write_text("""/* Carrito y pasarela de pagos (se suma al estilo que ya tiene el sitio) */
:root{--accent:#1428A0;--accent-bright:#2F5FE0;--accent-soft:#E7ECFB;--deep:#0A1628;--glow:#8fb0ff}
body.tienda-samsung{--bg:#F2F5FC;--ink:#0A1628;--muted:#4A5A72;--line:#DCE3F2;--panel:#fff;--f:'Inter',-apple-system,sans-serif;--mono:'Space Grotesk',monospace}
header.top{background:#fff;border-bottom:1px solid #DCE3F2}header.top .logo{color:#0A1628;font-size:15px;font-weight:600}header.top .logo small{color:#4A5A72}
header.top .nv{display:flex;gap:14px;align-items:center}header.top .nv a{color:#1428A0;font-weight:700;text-decoration:none}
.pie{background:#0A1628;color:#c9d3ea;padding:22px 0;margin-top:20px}.pie a{color:#fff;margin-right:14px}.pie p{font-size:13px;opacity:.85}
.btn-cart{display:inline-flex;align-items:center;gap:6px;background:#1428A0;color:#fff;border:0;border-radius:8px;padding:11px 18px;font:700 13px var(--mono,monospace);cursor:pointer;white-space:nowrap}
.btn-cart:hover{background:#2F5FE0}
.cart-fab{position:fixed;left:14px;bottom:14px;z-index:60;background:#0A1628;color:#fff;border-radius:999px;padding:12px 16px;font:700 14px system-ui,sans-serif;text-decoration:none;display:flex;gap:8px;align-items:center;box-shadow:0 8px 24px rgba(0,0,0,.28)}
.cart-fab span{background:#2F5FE0;border-radius:999px;min-width:20px;height:20px;display:inline-grid;place-items:center;font-size:12px;padding:0 5px}
.site-nav a.carro{font-weight:700}
.fy-toast{position:fixed;left:50%;bottom:78px;transform:translate(-50%,20px);background:#0A1628;color:#fff;border-radius:12px;padding:12px 16px;display:none;gap:14px;align-items:center;z-index:80;font:600 14px system-ui,sans-serif;box-shadow:0 12px 30px rgba(0,0,0,.3)}
.fy-toast.on{display:flex;transform:translate(-50%,0)}.fy-toast a{color:#8fb0ff}
/* pasarela de pagos */
.pg{border:1px solid #DCE3F2;background:#fff;border-radius:16px;padding:22px;display:flex;flex-direction:column;gap:16px;color:#0A1628;font-family:'Inter',system-ui,sans-serif}
.pg svg{width:22px;height:22px;fill:none;stroke:currentColor;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round;flex:none}
.pg-h{display:flex;align-items:center;gap:12px}.pg-h b{display:block;font-size:18px}.pg-h small{color:#4A5A72;font-size:13.5px}
.pg-l{width:44px;height:44px;border-radius:12px;background:#1428A0;color:#fff;display:grid;place-items:center;flex:none}.pg-l svg{stroke:#fff}
.pg-m{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:10px}
.pg-m li{display:flex;align-items:center;gap:10px;border:1px solid #DCE3F2;border-radius:12px;padding:11px 12px;background:#F2F5FC;min-width:0}
.pg-i{width:38px;height:38px;border-radius:10px;background:#E7ECFB;color:#1428A0;display:grid;place-items:center;flex:none}
.pg-m b{display:block;font-size:14.5px;line-height:1.2}.pg-m small{display:block;color:#4A5A72;font-size:12.5px;line-height:1.3}
.pg-s{list-style:none;margin:0;padding:12px 14px;display:flex;flex-direction:column;gap:7px;background:#F2F5FC;border-radius:12px;font-size:13.5px}
.pg-s li{display:flex;gap:9px;align-items:center}.pg-s svg{width:17px;height:17px;color:#1e7a46}
.pg-p{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:12px;counter-reset:q}
.pg-p li{counter-increment:q;position:relative;padding:14px 14px 14px 52px;border:1px dashed #DCE3F2;border-radius:12px}
.pg-p li::before{content:counter(q);position:absolute;left:14px;top:14px;width:26px;height:26px;border-radius:50%;background:#1428A0;color:#fff;font-weight:800;display:grid;place-items:center;font-size:14px}
.pg-p b{display:block}.pg-p span{color:#4A5A72;font-size:13.5px}
.pg-sec{padding:40px 0}.pg-sec .wrap{max-width:1080px;margin:0 auto;padding:0 24px}
@media (max-width:760px){.pg-p{grid-template-columns:1fr}.pg-m{grid-template-columns:1fr 1fr}.pg{padding:16px}}
@media (max-width:420px){.pg-m{grid-template-columns:1fr}}
""", encoding="utf-8")

# ---------- 3. páginas estáticas: carrito, pasarela y SEO ----------
IC = {
    "tarjeta": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="2.5" y="5" width="19" height="14" rx="2.5"/><path d="M2.5 9.5h19M6 15h4"/></svg>',
    "pse": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 10 12 4l9 6M5 10v8M9.5 10v8M14.5 10v8M19 10v8M3 20h18"/></svg>',
    "nequi": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="6.5" y="2.5" width="11" height="19" rx="2.5"/><path d="M10.5 18.5h3"/></svg>',
    "banco": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 8h16M6 8v10M10 8v10M14 8v10M18 8v10M3 20h18M12 3 3 8h18z"/></svg>',
    "efectivo": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="2.5" y="6" width="19" height="12" rx="2"/><circle cx="12" cy="12" r="2.6"/></svg>',
    "candado": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="10.5" width="14" height="10" rx="2.2"/><path d="M8 10.5V8a4 4 0 0 1 8 0v2.5M12 14.5v2.5"/></svg>',
}
MEDIOS = [("tarjeta", "Tarjeta crédito o débito", "Visa y Mastercard"), ("pse", "PSE", "Débito desde tu banco"), ("nequi", "Nequi", "Pagas desde la app"),
          ("banco", "Bancolombia", "Botón con tu cuenta"), ("efectivo", "Contra entrega", "Efectivo a la transportadora")]
PASARELA = ('<section class="pg-sec" id="pasarela" aria-labelledby="pg-t"><div class="wrap"><div class="pg"><div class="pg-h"><span class="pg-l">' + IC["candado"] + '</span><span><b id="pg-t">Pasarela de pagos segura</b>'
            '<small>Pagos en línea procesados por Wompi, de Bancolombia</small></span></div><ul class="pg-m">'
            + "".join(f'<li><span class="pg-i">{IC[i]}</span><span><b>{t}</b><small>{d}</small></span></li>' for i, t, d in MEDIOS) + '</ul>'
            '<ol class="pg-p"><li><b>Agrega tu filtro</b><span>Escoge la referencia y tócala en «Agregar al carrito».</span></li><li><b>Paga como prefieras</b><span>En línea con tarjeta, PSE, Nequi o Bancolombia, o contra entrega.</span></li>'
            '<li><b>Recibe la confirmación</b><span>Te llega el recibo por correo y tu pedido sale con número de guía.</span></li></ol>'
            '<ul class="pg-s"><li>' + IC["candado"] + 'Pago en la pasarela segura de Wompi (Bancolombia)</li><li>' + IC["candado"] + 'Conexión cifrada: no vemos ni guardamos los datos de tu tarjeta</li>'
            '<li>' + IC["candado"] + 'Confirmación de tu pedido por correo</li></ul></div></div></section>')

DIMS = {}
for f in (OUT / "img").iterdir():
    try:
        DIMS["img/" + f.name] = Image.open(f).size
    except Exception:
        pass

LD = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)
RETORNO = {"@type": "MerchantReturnPolicy", "applicableCountry": "CO", "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow", "merchantReturnDays": 5,
           "returnMethod": "https://schema.org/ReturnByMail", "returnFees": "https://schema.org/ReturnFeesCustomerResponsibility"}
ENTREGA = {"@type": "ShippingDeliveryTime", "handlingTime": {"@type": "QuantitativeValue", "minValue": 0, "maxValue": 1, "unitCode": "DAY"},
           "transitTime": {"@type": "QuantitativeValue", "minValue": 1, "maxValue": 3, "unitCode": "DAY"}}


def mejorar_oferta(o, url):
    if not isinstance(o, dict):
        return
    o["url"] = url
    o["priceValidUntil"] = "2027-12-31"
    o.setdefault("hasMerchantReturnPolicy", RETORNO)
    sd = o.get("shippingDetails")
    if isinstance(sd, dict):
        sd.setdefault("deliveryTime", ENTREGA)


def ld_producto(p, url):
    return {"@context": "https://schema.org", "@type": "Product", "name": p["nombre"], "sku": p["ref"], "mpn": p["ref"], "image": f"{DOMINIO}/{p['img']}", "brand": {"@type": "Brand", "name": "Samsung"},
            "category": "Filtros de agua para nevecón", "offers": {"@type": "Offer", "priceCurrency": "COP", "price": str(p["precio"]), "availability": "https://schema.org/InStock", "itemCondition": "https://schema.org/NewCondition",
                                                                  "url": url, "priceValidUntil": "2027-12-31", "seller": {"@id": f"{DOMINIO}/#store"}, "hasMerchantReturnPolicy": RETORNO,
                                                                  "shippingDetails": {"@type": "OfferShippingDetails", "shippingRate": {"@type": "MonetaryAmount", "value": "0", "currency": "COP"},
                                                                                      "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "CO"}, "deliveryTime": ENTREGA}}}


def pagina(f):
    t = f.read_text(encoding="utf-8")
    o = t
    # a) «Agregar al carrito» al lado de cada «Pagar en línea» (mismo link de Wompi que ya tenía)
    def boton(m):
        a = m.group(0)
        k = LINK_A_ID.get(m.group(1))
        if not k or "data-add" in t[m.end():m.end() + 140]:
            return a
        return a + f'<button type="button" class="btn-cart" data-add="{k}">🛒 Agregar al carrito</button>'
    t = re.sub(r'<a [^>]*href="https://checkout\.wompi\.co/l/(\w+)"[^>]*>.*?</a>', boton, t, flags=re.S)
    # b) carrito en el menú y botón flotante
    t = t.replace('<a class="hl" href="https://wa.me/573054796329">WhatsApp</a>', '<a class="carro" href="carrito.php">🛒 Carrito <span data-cart-n hidden></span></a><a class="hl" href="https://wa.me/573054796329">WhatsApp</a>', 1)
    if "</head>" in t and "pasarela.css" not in t:
        t = t.replace("</head>", '<link rel="stylesheet" href="pasarela.css"><link rel="preconnect" href="https://checkout.wompi.co"></head>', 1)
    if "carrito.js" not in t and "</body>" in t:
        t = t.replace("</body>", '<a class="cart-fab" href="carrito.php" aria-label="Ver carrito">🛒 <span data-cart-n hidden></span></a><script src="carrito.js" defer></script></body>', 1)
    # c) panel de la pasarela en la portada y en las 3 fichas principales
    if f.name in ("index.html", "filtro-haf-cin.html", "filtro-haf-qin.html", "filtro-externo.html") and 'id="pasarela"' not in t:
        if '<section class="section" id="faq">' in t:
            t = t.replace('<section class="section" id="faq">', PASARELA + '\n    <section class="section" id="faq">', 1)
        elif "</main>" in t:
            t = t.replace("</main>", PASARELA + "</main>", 1)
        elif "<footer" in t:
            t = t.replace("<footer", PASARELA + "<footer", 1)
    # d) SEO: medidas y carga diferida de las imágenes (evita saltos de diseño), preconnect, ofertas completas en los datos estructurados
    primera = [True]

    def img(m):
        tag = m.group(0)
        src = re.search(r'\bsrc="([^"]+)"', tag)
        if not src:
            return tag
        if "width=" not in tag and src.group(1) in DIMS:
            w, h = DIMS[src.group(1)]
            tag = tag.replace("<img", f'<img width="{w}" height="{h}"', 1)
        if "loading=" not in tag and "fetchpriority" not in tag:
            tag = tag.replace("<img", '<img loading="lazy"', 1)
        if "decoding=" not in tag:
            tag = tag.replace("<img", '<img decoding="async"', 1)
        return tag
    t = re.sub(r"<img\b[^>]*>", img, t)
    if "fonts.gstatic.com" not in t:
        t = t.replace("<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">", '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>', 1)

    canon = re.search(r'<link rel="canonical" href="([^"]+)"', t)
    url = canon.group(1) if canon else DOMINIO + "/" + f.name

    def ld(m):
        try:
            j = json.loads(m.group(2))
        except Exception:
            return m.group(0)
        graf = j.get("@graph", [j]) if isinstance(j, dict) else j
        cambio = False
        for n in (graf if isinstance(graf, list) else [graf]):
            if isinstance(n, dict) and n.get("@type") == "Product":
                mejorar_oferta(n.get("offers"), url)
                cambio = True
        return m.group(1) + "\n    " + json.dumps(j, ensure_ascii=False, indent=2).replace("\n", "\n    ") + "\n    " + m.group(3) if cambio else m.group(0)
    t = LD.sub(ld, t)
    if f.name == "index.html" and '"@type": "ItemList"' not in t.replace('"@type":"ItemList"', '"@type": "ItemList"'):
        lista = {"@context": "https://schema.org", "@type": "ItemList", "name": "Filtros de agua Samsung para nevecón", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "item": ld_producto(p, f"{DOMINIO}/{p['url']}")} for i, p in enumerate(PRODUCTOS.values())]}
        t = t.replace("</head>", '<script type="application/ld+json">\n' + json.dumps(lista, ensure_ascii=False, indent=2) + "\n</script>\n</head>", 1)
    if t != o:
        f.write_text(t, encoding="utf-8")
        return 1
    return 0


n = sum(pagina(f) for f in sorted(OUT.glob("*.html")))
print("páginas HTML modificadas:", n)

# ---------- 4. robots, sitemap y llms ----------
r = (OUT / "robots.txt").read_text(encoding="utf-8")
if "Disallow: /carrito.php" not in r:
    r = r.replace("User-agent: *\nAllow: /", "User-agent: *\nAllow: /\nDisallow: /carrito.php\nDisallow: /gracias.php\nDisallow: /admin.php\nDisallow: /diagnostico.php\nDisallow: /opinion.php\nDisallow: /api/\nDisallow: /data/", 1)
    (OUT / "robots.txt").write_text(r, encoding="utf-8")
s = (OUT / "sitemap.xml").read_text(encoding="utf-8")
s = re.sub(r"<lastmod>[^<]*</lastmod>", f"<lastmod>{HOY}</lastmod>", s)
for legal in ("terminos.php", "privacidad.php", "garantia-y-retracto.php"):
    if legal not in s:
        s = s.replace("</urlset>", f"  <url><loc>{DOMINIO}/{legal}</loc><lastmod>{HOY}</lastmod><changefreq>yearly</changefreq><priority>0.3</priority></url>\n</urlset>")
(OUT / "sitemap.xml").write_text(s, encoding="utf-8")
ll = (OUT / "llms.txt").read_text(encoding="utf-8")
if "Compra en línea" not in ll:
    ll += ("\n## Compra en línea\n- Tienda con carrito y pasarela de pagos segura (Wompi, de Bancolombia): tarjeta crédito o débito, PSE, Nequi, Bancolombia o contra entrega.\n"
           f"- Carrito: {DOMINIO}/carrito.php\n- Recibo y confirmación del pedido por correo. Retracto de 5 días hábiles: {DOMINIO}/garantia-y-retracto.php\n"
           f"- Precios: HAF-CIN/EXP DA29-00020B y HAF-QIN/EXP DA97-17376B $139.900; externo DA29-10105J $79.900 (envío gratis).\n")
    (OUT / "llms.txt").write_text(ll, encoding="utf-8")
print("listo:", OUT)
