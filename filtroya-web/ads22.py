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

# ---------- 2b. SEO ampliado: más ciudades, páginas por referencia, por modelo y por departamento ----------
import ads22_seo as seo
ciudades = seo.leer_ciudades(OUT)
n_antes = len(ciudades)
nuevas_ciudad = seo.expandir_ciudades(OUT, ciudades)
nuevas_extra, refs_slug, depts = seo.paginas_nuevas(OUT, PRODUCTOS, ciudades)
seo.actualizar_hub(OUT, ciudades)
n_enl = seo.enlaces_internos(OUT, PRODUCTOS, refs_slug, depts)
import ads22_hubs
nuevas_hubs, HUBS = ads22_hubs.crear(OUT, seo, PRODUCTOS, ciudades, depts)
PAGINAS_NUEVAS = nuevas_ciudad + nuevas_extra + nuevas_hubs
print(f"ciudades: {n_antes} -> {len(ciudades)}; páginas nuevas: {len(PAGINAS_NUEVAS)} ({len(nuevas_ciudad)} de ciudad, {len(nuevas_extra)} de referencia/modelo/departamento); enlaces internos en {n_enl} páginas")

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

STRIP = ('<div class="pg-strip"><span>🔒 Pago seguro con Wompi</span><b>Tarjeta</b><b>PSE</b><b>Nequi</b><b>Bancolombia</b><b>Contra entrega</b></div>')
# fotos nítidas y del mismo tamaño: cada filtro con SU foto (recortada al producto y centrada en un cuadro blanco)
FOTO_HD = {"cin": "sam-cin-o.jpg", "qin": "sam-qin-o.jpg", "ext": "sam-ex-o.jpg"}
IMG_VIEJA = {}


def foto_cuadrada(origen, destino, lado=800, uso=0.92):
    """Recorta el producto, le quita el fondo blanco (solo el que toca el borde: el blanco del propio filtro se conserva) y lo centra en un cuadro transparente."""
    from PIL import ImageChops, ImageDraw
    im = Image.open(origen).convert("RGB")
    marco = Image.new("RGB", (im.width + 4, im.height + 4), (255, 255, 255))
    marco.paste(im, (2, 2))
    sello = (255, 0, 255)
    for xy in ((0, 0), (marco.width - 1, 0), (0, marco.height - 1), (marco.width - 1, marco.height - 1), (marco.width // 2, 0), (marco.width // 2, marco.height - 1)):
        if marco.getpixel(xy) != sello:
            ImageDraw.floodfill(marco, xy, sello, thresh=22)
    marco = marco.crop((2, 2, marco.width - 2, marco.height - 2))
    rgba = marco.convert("RGBA")
    px = rgba.load()
    for y in range(rgba.height):
        for x in range(rgba.width):
            if px[x, y][:3] == sello:
                px[x, y] = (255, 255, 255, 0)
    caja = rgba.getchannel("A").point(lambda v: 255 if v > 0 else 0).getbbox() or (0, 0) + rgba.size
    rgba = rgba.crop(caja)
    esc_ = lado * uso / max(rgba.size)
    rgba = rgba.resize((max(1, round(rgba.width * esc_)), max(1, round(rgba.height * esc_))), Image.LANCZOS)
    lienzo = Image.new("RGBA", (lado, lado), (255, 255, 255, 0))
    lienzo.paste(rgba, ((lado - rgba.width) // 2, (lado - rgba.height) // 2), rgba)
    lienzo.save(destino, "WEBP", quality=90, method=6)


for k_, f_ in FOTO_HD.items():
    foto_cuadrada(AQUI / "public_html" / "filtrosnevecones-img" / f_, OUT / "img" / f"p-{k_}.webp")
    IMG_VIEJA[PRODUCTOS[k_]["img"]] = f"img/p-{k_}.webp"
    PRODUCTOS[k_]["img"] = f"img/p-{k_}.webp"

# galería de imágenes de cada filtro: la foto principal + imágenes informativas propias + las fotos reales que se agreguen en fotos/<clave>-*.jpg
import galeria
galeria.generar()
GAL_FICHAS = {"filtro-haf-cin.html": "cin", "filtro-haf-qin.html": "qin", "filtro-externo.html": "ext"}
GALERIA = {}
for k_, p_ in PRODUCTOS.items():
    lista = [("principal", p_["img"], "Foto del filtro " + p_["corto"])]
    for extra in sorted((AQUI / "fotos").glob(f"{k_}-*.jpg")) if (AQUI / "fotos").is_dir() else []:
        foto_cuadrada(extra, OUT / "img" / ("real-" + extra.stem + ".webp"), uso=0.92)
        lista.append(("real", "img/real-" + extra.stem + ".webp", "Foto real del filtro " + p_["corto"]))
    for nom, tit in (("identificar", "Cómo identificar tu filtro"), ("instalacion", "Cómo se instala"), ("ficha", "Ficha técnica")):
        shutil.copy(AQUI / "galeria" / f"{k_}-{nom}.jpg", OUT / "img" / f"gal-{k_}-{nom}.jpg")
        lista.append((nom, f"img/gal-{k_}-{nom}.jpg", f"{tit} del filtro {p_['corto']}"))
    GALERIA[k_] = lista
GAL_CSS = """
.gal{display:grid;gap:12px;max-width:520px;margin:0 auto}
.gal-main{background:#fff;border:1px solid #DCE3F2;border-radius:16px;overflow:hidden;aspect-ratio:1/1;display:grid;place-items:center;cursor:zoom-in}
.gal-main img{width:100%;height:100%;object-fit:contain;transition:transform .25s;transform-origin:center}
.gal-main.zoom{cursor:zoom-out}.gal-main.zoom img{transform:scale(2)}
.gal-th{display:flex;gap:8px;overflow-x:auto;padding:2px}
.gal-th button{flex:0 0 72px;height:72px;border:2px solid #DCE3F2;border-radius:10px;background:#fff;padding:2px;cursor:pointer}
.gal-th button[aria-selected=true]{border-color:#1428A0}.gal-th img{width:100%;height:100%;object-fit:contain;border-radius:6px;display:block}
"""
TF_CSS = """
.tf-hero{background:#fff;border-bottom:1px solid #DCE3F2;padding:26px 0 18px}.tf-hero h1{font-size:clamp(26px,4.2vw,40px);line-height:1.15;margin:0 0 8px}
.tf-hero p{margin:0 0 14px;color:#4A5A72;font-size:16px;max-width:760px}
.tf-ok{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:8px}.tf-ok li{background:#F2F5FC;border:1px solid #DCE3F2;border-radius:999px;padding:7px 13px;font-size:13.5px;font-weight:600;color:#0A1628}
.tf{padding:26px 0 8px;background:#F2F5FC;scroll-margin-top:70px}
.tf-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.tf-card{background:#fff;border:1px solid #DCE3F2;border-radius:16px;overflow:hidden;display:flex;flex-direction:column}
.tf-img{display:block;background:#fff;aspect-ratio:4/3;position:relative}.tf-img img{position:absolute;inset:10px;width:calc(100% - 20px);height:calc(100% - 20px);object-fit:contain}
.tf-b{padding:4px 18px 18px;display:flex;flex-direction:column;gap:6px;flex:1}
.tf-b h3{margin:0;font-size:19px}.tf-b h3 a{color:#0A1628;text-decoration:none}.tf-code{font-family:var(--mono,monospace);font-size:12.5px;color:#1428A0;font-weight:700}
.tf-b p{margin:0;color:#4A5A72;font-size:14px}.tf-pr{font-size:28px;font-weight:800;color:#0A1628;margin:6px 0 4px}.tf-pr small{font-size:12px;font-weight:500;color:#4A5A72;margin-left:6px}
.tf-add{margin-top:auto;border:0;border-radius:12px;background:#1428A0;color:#fff;font:700 16px/1 inherit;font-family:inherit;padding:15px;cursor:pointer}.tf-add:hover{background:#0f1f80}
.tf-note{text-align:center;margin:16px 0 0;color:#4A5A72;font-size:14.5px}.tf-note a{color:#1428A0;font-weight:700}
@media(max-width:820px){.tf-hero{padding:18px 0 12px}.tf-ok{gap:6px}.tf-ok li{padding:5px 10px;font-size:12px}.tf-hero p{font-size:15px;margin-bottom:10px}.tf{padding-top:16px}.tf-grid{grid-template-columns:1fr;gap:14px}.tf-card{flex-direction:row}.tf-img{flex:0 0 40%;aspect-ratio:1/1;align-self:center}.tf-b{padding:14px 14px 14px 4px}.tf-pr{font-size:24px}}
"""
FORMA = {"cin": "Redondo · se instala girando", "qin": "Cuadrado · se instala empujando", "ext": "Externo · va en la línea de agua"}


def portada_tienda():
    cards = "".join(
        f'<article class="tf-card"><a class="tf-img" href="{p["url"]}" aria-label="Ver {p["corto"]}"><img src="{p["img"]}" alt="Filtro de agua Samsung {p["corto"]} original, código {p["ref"]}" width="400" height="400" loading="{"eager" if k == "cin" else "lazy"}"></a>'
        f'<div class="tf-b"><h3><a href="{p["url"]}">{p["corto"]}</a></h3><span class="tf-code">Código {p["ref"]}</span><p>{FORMA[k]}</p>'
        f'<div class="tf-pr">${p["precio"]:,}'.replace(",", ".") + '<small>COP</small></div>'
        f'<button type="button" class="tf-add" data-add="{k}">🛒 Agregar al carrito</button></div></article>' for k, p in PRODUCTOS.items())
    return ('<section class="tf-hero"><div class="wrap"><h1>Filtro de Agua Samsung Original para tu Nevecón</h1>'
            '<p>Escoge tu referencia, agrégala al carrito y paga en línea o contra entrega.</p>'
            '<ul class="tf-ok"><li>🔒 Pago seguro con Wompi</li><li>💵 Contra entrega disponible</li><li>✔ Producto nuevo y sellado</li><li>↩ 5 días de retracto</li></ul></div></section>'
            '<section class="tf" id="filtros"><div class="wrap"><div class="tf-grid">' + cards + '</div>'
            '<p class="tf-note">¿No sabes cuál es el tuyo? <a href="#identificar-modelo">Identifica tu filtro</a> por el código o el modelo de tu nevecón.</p></div></section>')


GAL_JS = """<script>document.querySelectorAll('[data-gal]').forEach(function(g){var m=g.querySelector('.gal-main'),i=m.querySelector('img');g.querySelectorAll('.gal-th button').forEach(function(b){b.addEventListener('click',function(){g.querySelectorAll('.gal-th button').forEach(function(x){x.setAttribute('aria-selected','false')});b.setAttribute('aria-selected','true');i.src=b.dataset.src;i.alt=b.dataset.alt;m.classList.remove('zoom')})});m.addEventListener('click',function(e){var r=m.getBoundingClientRect();i.style.transformOrigin=((e.clientX-r.left)/r.width*100)+'% '+((e.clientY-r.top)/r.height*100)+'%';m.classList.toggle('zoom')})});</script>"""

with open(OUT / "pasarela.css", "a", encoding="utf-8") as _f:
    _f.write(GAL_CSS + TF_CSS + """
/* carrito en la paleta del logo de Samsung: botón principal azul, secundarios blancos */
.btn{background:#1428A0!important;border-color:#1428A0!important;color:#fff!important;box-shadow:0 10px 24px -10px rgba(20,40,160,.7)!important}.btn:hover{background:#0f1f80!important}
.btn.ghost,.btn.sm.ghost{background:#fff!important;color:#1428A0!important}
""")


def galeria_html(k):
    L = GALERIA[k]
    return ('<div class="gal" data-gal><div class="gal-main"><img decoding="async" src="' + L[0][1] + '" alt="' + L[0][2] + '" width="520" height="520"></div><div class="gal-th" role="tablist" aria-label="Imágenes del producto">'
            + "".join(f'<button type="button" role="tab" aria-selected="{"true" if i == 0 else "false"}" data-src="{src}" data-alt="{alt}" aria-label="{alt}"><img src="{src}" alt="" loading="lazy"></button>' for i, (_, src, alt) in enumerate(L)) + "</div></div>")


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


import ads22_tema
TEMA = ads22_tema.Tema(OUT, PRODUCTOS, ciudades, hubs=HUBS)
TEMA.escribir_assets()
# el carrito, «gracias» y las páginas legales llevan el mismo encabezado y pie del sitio
_pt = (OUT / "partes.php").read_text(encoding="utf-8")
_i = _pt.index("'<header class=\"top\">")
_j = _pt.index("<main class=\"wrap\">';", _i) + len("<main class=\"wrap\">';")
_pt = _pt[:_i] + "$AQH . '<main class=\"wrap\">';" + _pt[_j:]
_pt = _pt.replace("    $S = sitio();\n    $canon", "    $AQH = <<<'AQH'\n" + TEMA.encabezado() + "\nAQH;\n    $S = sitio();\n    $canon", 1)
_pt = _pt.replace("family=Space+Grotesk:wght@500;700&family=Inter:wght@400;500;600;700", "family=Bricolage+Grotesque:wght@600;800&family=Inter:wght@400;500;600;700", 1)
_pt = _pt.replace('<link rel="stylesheet" href="/pasarela.css">', '<link rel="stylesheet" href="/pasarela.css"><link rel="stylesheet" href="/aqua-shell.css"><script src="/buscar.js" defer></script>', 1)
_k = _pt.index("    return '</main><footer class=\"pie\">")
_l = _pt.index("</footer></body></html>';", _k) + len("</footer></body></html>';")
_pt = _pt[:_k] + "    $AQF = <<<'AQF'\n" + TEMA.pie() + "\nAQF;\n    return '</main>' . $AQF . '</body></html>';" + _pt[_l:]
(OUT / "partes.php").write_text(_pt, encoding="utf-8")


def pagina(f):
    t = f.read_text(encoding="utf-8")
    o = t
    for viejo, nuevo in IMG_VIEJA.items():
        t = t.replace(viejo, nuevo)
    # a) el «Pagar en línea» de siempre ahora pasa por el carrito (un solo botón): agrega el filtro y abre el pago con sus datos, correo y confirmación
    def boton(m):
        k = LINK_A_ID.get(m.group(2))
        if not k:
            return m.group(0)
        attrs = m.group(1) + m.group(3)
        cls = re.search(r'class="([^"]*)"', attrs)
        clic = re.search(r'onclick="([^"]*)"', attrs)
        return (f'<button type="button" class="{cls.group(1) if cls else "btn-online"}"' + (f' onclick="{clic.group(1)}"' if clic else "") + f' data-add="{k}" data-ir="1">{m.group(4)}</button>')
    t = re.sub(r'<a ([^>]*?)href="https://checkout\.wompi\.co/l/(\w+)"([^>]*)>(.*?)</a>', boton, t, flags=re.S)
    # a2) la ventana emergente de la foto también pasa por el carrito (antes mandaba directo al link de Wompi, sin pedido ni correo)
    t = t.replace('<a href="#" id="lightboxWompi" target="_blank" rel="noopener noreferrer" class="btn-wompi">💳 Pagar en línea con Wompi</a>',
                  '<button type="button" id="lightboxWompi" class="btn-wompi" data-add="" data-ir="1">💳 Pagar en línea con Wompi</button>')
    t = t.replace("document.getElementById('lightboxWompi').href = WOMPI_LINKS[name] || '#';",
                  "document.getElementById('lightboxWompi').setAttribute('data-add', ({'HAF-CIN/EXP':'cin','HAF-QIN/EXP':'qin','Externo DA29-10105J':'ext'})[name] || 'cin');")
    # a3) tienda normal: «Agregar al carrito» + «Comprar ahora» (se quitan «Pedir por WhatsApp» y «Confirmar mi modelo» como botones de compra)
    def clave(txt):
        import urllib.parse
        u = urllib.parse.unquote(txt).upper()
        return "cin" if "HAF-CIN" in u else "qin" if "HAF-QIN" in u else "ext" if ("DA29-10105J" in u or "EXTERNO" in u) else None
    def agregar_wa(m):
        k = clave(m.group(2))
        cls, suf = m.group(3), m.group(4)
        if k:
            return f'<button type="button" class="{cls}" data-add="{k}">🛒 Agregar al carrito{suf}</button><button type="button" class="btn btn-line" data-add="{k}" data-ir="1">⚡ Comprar ahora</button>'
        return f'<a href="index.html#catalogo" class="{cls}">Ver filtros y comprar{suf}</a>'
    t = re.sub(r'<a (href="https://wa\.me/\d+\?text=([^"]*)") class="(btn btn-solid)">Pedir por WhatsApp([^<]*)</a>', agregar_wa, t)
    t = re.sub(r'<a href="https://wa\.me/\d+\?text=([^"]*)" class="(btn-order)">()Pedir</a>', lambda m: (f'<button type="button" class="btn-order" data-add="{clave(m.group(1))}">🛒 Agregar</button>' if clave(m.group(1)) else m.group(0)), t)
    t = re.sub(r'<a href="https://wa\.me/[^"]*" class="btn btn-line">Confirmar mi modelo antes de pagar</a>', "", t)
    t = t.replace('<a href="#" id="lightboxOrder" class="btn-order" style="text-align:center; padding:14px;">Pedir por WhatsApp</a>',
                  '<button type="button" id="lightboxOrder" class="btn-order" data-add="cin" style="text-align:center; padding:14px;">🛒 Agregar al carrito</button>')
    t = t.replace("document.getElementById('lightboxOrder').href = 'https://wa.me/573054796329?text=' + encodeURIComponent('Hola, quiero el filtro Samsung ' + name);",
                  "document.getElementById('lightboxOrder').setAttribute('data-add', ({'HAF-CIN/EXP':'cin','HAF-QIN/EXP':'qin','Externo DA29-10105J':'ext'})[name] || 'cin');")
    t = t.replace("💳 Pagar en línea con Wompi</button>", "⚡ Comprar ahora</button>")
    # medios de pago visibles junto a los botones de compra
    t = re.sub(r'(<div class="(?:spec-footer|hero-cta)">.*?</div>)', lambda mm: mm.group(1) + STRIP if "data-add" in mm.group(1) else mm.group(1), t, flags=re.S)
    if "data-add" in t and 'class="pg-strip"' not in t and "<footer>" in t:
        t = t.replace("<footer>", STRIP + "<footer>", 1)
    # b) carrito en el menú y botón flotante
    t = t.replace('<a class="hl" href="https://wa.me/573054796329">WhatsApp</a>', '<a class="carro" href="carrito.php">🛒 Carrito <span data-cart-n hidden></span></a><a class="hl" href="https://wa.me/573054796329">WhatsApp</a>', 1)
    if "</head>" in t and "pasarela.css" not in t:
        t = t.replace("</head>", '<link rel="stylesheet" href="pasarela.css"><link rel="preconnect" href="https://checkout.wompi.co"><style>.cart-fab{position:fixed;left:14px;bottom:14px;z-index:60;background:#0A1628;color:#fff;border-radius:999px;padding:12px 16px;font:700 14px system-ui,sans-serif;text-decoration:none;display:flex;gap:8px;align-items:center}.cart-fab span{background:#2F5FE0;border-radius:999px;min-width:20px;height:20px;display:inline-grid;place-items:center;font-size:12px;padding:0 5px}.pg-strip{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin:12px 0 0;font:600 12.5px system-ui,sans-serif;color:#4A5A72}.pg-strip span{margin-right:4px}.pg-strip b{border:1px solid #DCE3F2;background:#fff;color:#0A1628;border-radius:6px;padding:3px 8px}button.btn-online,button.btn-wompi,button.btn-order{cursor:pointer;font-family:inherit}[data-cart-n]{background:#2F5FE0;color:#fff;border-radius:999px;padding:0 6px;font-size:12px}</style></head>', 1)
    if "carrito.js" not in t and "</body>" in t:
        t = t.replace("</body>", '<a class="cart-fab" href="carrito.php" aria-label="Ver carrito">🛒 <span data-cart-n hidden></span></a><script src="carrito.js" defer></script></body>', 1)
    # c) panel de la pasarela en la portada y en las 3 fichas principales
    if f.name in ("index.html", "filtro-haf-cin.html", "filtro-haf-qin.html", "filtro-externo.html") and 'id="pasarela"' not in t:
        ic = t.find('id="catalogo"')
        sig = t.find("<section", ic + 20) if ic > 0 else -1
        if sig > 0:
            t = t[:sig] + PASARELA + "\n    " + t[sig:]
        elif '<section class="section" id="faq">' in t:
            t = t.replace('<section class="section" id="faq">', PASARELA + '\n    <section class="section" id="faq">', 1)
        elif "</main>" in t:
            t = t.replace("</main>", PASARELA + "</main>", 1)
        elif "<footer" in t:
            t = t.replace("<footer", PASARELA + "<footer", 1)
    # a4) como en cualquier tienda en línea: UN solo botón por producto («Agregar al carrito»); el pago se hace dentro del carrito
    t = re.sub(r'\s*<button type="button"[^>]*class="btn-wompi"[^>]*>.*?</button>', "", t, flags=re.S)
    t = re.sub(r'\s*<button type="button" class="btn btn-line" data-add="\w+" data-ir="1">⚡ Comprar ahora</button>', "", t)
    t = re.sub(r'\s*<a href="[^"]*" class="btn-detalle">Ver detalles[^<]*</a>', "", t)
    t = re.sub(r"\s*document\.getElementById\('lightboxWompi'\)\.setAttribute\([^\n]*?\|\| 'cin'\);", "", t)
    if f.name in GAL_FICHAS:
        t, nsub = re.subn(r'<img[^>]*class="hero-img"[^>]*>', lambda m: galeria_html(GAL_FICHAS[f.name]), t, count=1)
        assert nsub == 1, f.name
        t = t.replace("</body>", GAL_JS + "</body>", 1)
    # d) SEO: medidas y carga diferida de las imágenes (evita saltos de diseño), preconnect, ofertas completas en los datos estructurados
    primera = [True]

    def img(m):
        tag = m.group(0)
        src = re.search(r'\bsrc="([^"]+)"', tag)
        if not src:
            return tag
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
    t = TEMA.aplicar(t, f.name)
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
for nombre in PAGINAS_NUEVAS:
    if nombre not in s:
        prio = "0.7" if nombre.startswith(("filtro-agua-samsung-", "referencia-", "filtro-nevecon-", "filtros-samsung-")) else "0.6"
        s = s.replace("</urlset>", f"  <url><loc>{DOMINIO}/{nombre}</loc><lastmod>{HOY}</lastmod><changefreq>weekly</changefreq><priority>{prio}</priority></url>\n</urlset>")
for legal in ("terminos.php", "privacidad.php", "garantia-y-retracto.php"):
    if legal not in s:
        s = s.replace("</urlset>", f"  <url><loc>{DOMINIO}/{legal}</loc><lastmod>{HOY}</lastmod><changefreq>yearly</changefreq><priority>0.3</priority></url>\n</urlset>")
(OUT / "sitemap.xml").write_text(s, encoding="utf-8")
ll = (OUT / "llms.txt").read_text(encoding="utf-8")
if "Compra en línea" not in ll:
    ll += ("\n## Compra en línea\n- Tienda con carrito y pasarela de pagos segura (Wompi, de Bancolombia): tarjeta crédito o débito, PSE, Nequi, Bancolombia o contra entrega.\n"
           f"- Carrito: {DOMINIO}/carrito.php\n- Recibo y confirmación del pedido por correo. Retracto de 5 días hábiles: {DOMINIO}/garantia-y-retracto.php\n"
           f"- Precios: HAF-CIN/EXP DA29-00020B y HAF-QIN/EXP DA97-17376B $139.900; externo DA29-10105J $79.900 (envío gratis).\n")
    ll += (f"\n## Cobertura y referencias\n- Envíos a {len(ciudades)} ciudades y municipios de {len(depts)} departamentos: {DOMINIO}/filtro-agua-samsung-por-ciudad-colombia.html\n"
           f"- Una página por código/referencia (DA29-00020B, DA29-00020A, HAF-CIN, DA97-17376B, HAF-QIN, DA29-10105J, HAFEX, WSF-100…) y por modelo de nevecón (RF28HMEDBSR, RF28R7351SR…): {DOMINIO}/equivalencias-codigos-filtro-samsung.html\n"
           f"- Páginas por departamento: {DOMINIO}/filtros-samsung-antioquia.html, {DOMINIO}/filtros-samsung-valle-del-cauca.html y las demás.\n")
    (OUT / "llms.txt").write_text(ll, encoding="utf-8")
print("listo:", OUT)
