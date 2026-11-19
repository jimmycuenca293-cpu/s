#!/usr/bin/env python3
"""Tienda de repuestos de línea blanca (lavadoras, neveras y protectores de voltaje) generada desde repuestos/catalogo.csv, con la base de las tiendas de filtros:
carrito, pago seguro con Wompi (link de pago por producto), pago contra entrega, SEO, datos estructurados y llms.txt.

Uso:  python3 ads_bm.py <carpeta_de_salida> [dominio] [etiqueta_search_console] [GTM-XXXX]
Precio de cada protector: 105.000 (90.000 + 15.000 de domicilio incluido). Envío gratis. Links de Wompi: LINKS_WOMPI abajo.
"""
import os, csv, datetime, html, json, pathlib, re, shutil, subprocess, sys, unicodedata, hashlib
from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
OUT = pathlib.Path(sys.argv[1])
DOMINIO = (sys.argv[2] if len(sys.argv) > 2 else "https://repuestoslineablanca.com").rstrip("/")
TOKEN = sys.argv[3] if len(sys.argv) > 3 else ""
TOKENS = [t_.strip() for t_ in TOKEN.split(",") if t_.strip()]
TOKEN = TOKENS[0] if TOKENS else ""
GTM = (sys.argv[4] if len(sys.argv) > 4 else "").strip().upper()
HOY = datetime.date.today().isoformat()
_M = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
FECHA_LARGA = f"{datetime.date.today().day} de {_M[datetime.date.today().month - 1]} de {datetime.date.today().year}"
WA, TEL = os.environ.get("TIENDA_WA", "573013810242"), os.environ.get("TIENDA_TEL", "301 381 0242")
NOMBRE = "Repuestos de Línea Blanca"
SRC = AQUI / "src"
BM = AQUI / "breakermatic"
RP = AQUI / "repuestos"
esc = lambda s: html.escape(str(s), quote=True)
cop = lambda v: "$" + f"{int(v):,}".replace(",", ".")
cop2 = lambda v: "$ " + f"{int(v):,}".replace(",", ".")
PRECIO = int(os.environ.get("TIENDA_PRECIO", "105000"))     # 90.000 del protector + 15.000 de domicilio; el envío se anuncia gratis
LINKS_WOMPI = {"bm-nev": os.environ.get("WOMPI_NEVERAS", ""), "bm-lav": os.environ.get("WOMPI_LAVADORAS", ""), "bm-tv": os.environ.get("WOMPI_TELEVISORES", "")}


def slug(n):
    n = unicodedata.normalize("NFKD", n).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", n).strip("-")



# ---------------------------------------------------------------- datos (todo sale de repuestos/catalogo.csv)
cat_php = json.loads(subprocess.run(["php", "-r", f'echo json_encode(require "{AQUI}/sitios/lg/api/catalogo.php");'], capture_output=True, text=True, check=True).stdout)
ESPEC_PV = {"PV-BM-NEV": (10, 1, "4 minutos"), "PV-BM-LAV": (15, 2, "5 segundos"), "PV-BM-TV": (10, 2, "5 segundos")}
FOTO_PV = {"PV-BM-NEV": "neveras", "PV-BM-LAV": "lavadoras", "PV-BM-TV": "televisores"}
PLURAL = {"Lavadoras": "lavadoras", "Neveras": "neveras", "Televisores": "televisores"}
PS = []
(OUT / "img").mkdir(parents=True)
for r in csv.DictReader(open(RP / "catalogo.csv", encoding="utf-8-sig")):
    sku = r["sku"]
    if sku in FOTO_PV:
        origen = BM / "img" / f"{FOTO_PV[sku]}.webp"
    else:
        origen = RP / "img" / (pathlib.Path(r["foto"]).stem + ".webp")
    if not origen.exists():
        continue      # sin foto real no se publica
    pid = sku.lower()
    im = Image.open(origen).convert("RGBA")
    im.save(OUT / "img" / f"p-{pid}.webp", "WEBP", quality=90, method=6)
    im.resize((480, 480), Image.LANCZOS).save(OUT / "img" / f"p-{pid}-480.webp", "WEBP", quality=82, method=6)
    precio = int(r["precio_venta"]) if r["precio_venta"].strip().isdigit() else None
    marca_eq = r["marca_equipo"].strip()
    p = dict(id=pid, sku=sku, ref=r["referencia"].strip() or sku, nombre=r["nombre"].strip(), equipo=r["equipo"].strip(), equipo_s=slug(r["equipo"]), categoria=r["categoria"].strip(), cat_s=slug(r["categoria"]),
             marca_eq=marca_eq, marca_s=slug(marca_eq), marca_prod=r["marca_producto"].strip(), modelos=[m.strip() for m in r["modelos_compatibles"].split(",") if m.strip()], precio=precio, link=os.environ.get("WOMPI_" + sku.replace("-", "_"), ""),
             desc=r["descripcion"].strip(), img=f"img/p-{pid}.webp", slug=slug(r["nombre"]), espec=ESPEC_PV.get(sku))
    p["url"] = p["slug"] + ".html"
    p["corto"] = p["nombre"]
    p["resumen"] = p["desc"] if p["desc"] and not p["desc"].startswith("Precio vigente") else f"{p['nombre']}."
    PS.append(p)
PRECIO_MIN = min((p["precio"] for p in PS if p["precio"]), default=0)
EQUIPOS = {}
for p in PS:
    EQUIPOS.setdefault(p["equipo"], {}).setdefault(p["categoria"], []).append(p)
MARCAS_EQ = sorted({p["marca_eq"] for p in PS if p["marca_eq"] and p["marca_eq"] != "Todas las marcas"})
PAGINAS = []  # (nombre, prioridad, titulo, descripcion)
shutil.copy(RP / "logo-512.png", OUT / "img" / "logo-bm.png")
shutil.copy(RP / "logo-512.png", OUT / "img" / "icono-bm.png")
shutil.copy(RP / "og.jpg", OUT / "img" / "og.jpg")
shutil.copy(RP / "logo.svg", OUT / "img" / "logo-bm.svg")


# ---------------------------------------------------------------- estilos (Breakermatic: azul y amarillo)
PAL = []
def pintar(t):
    for a, b in PAL:
        t = t.replace(a, b)
    return t


css = pintar((AQUI / "ads22_tema.css").read_text(encoding="utf-8"))
css += "\n.aq-hero .kicker,.hero .kicker{background:rgba(255,255,255,.16)}.aq-brand img{height:38px}.aq-qa-sec{padding:0 0 12px}.aq-ticker{display:flex;align-items:center;height:42px;background:#fff;border-bottom:1px solid #eadde2;overflow:hidden}.aq-tk-view{flex:1;overflow:hidden;min-width:0}.aq-tk-track{display:inline-flex;white-space:nowrap;animation:aqtk var(--d,300s) linear infinite}.aq-tk-track:hover{animation-play-state:paused}.aq-tk-track a{display:inline-flex;align-items:center;padding:0 16px;font:700 14px Inter,sans-serif;color:#3a2a32;text-decoration:none;line-height:42px}.aq-tk-track a:hover{color:#1428a0}.aq-tk-track a::after{content:'';width:5px;height:5px;border-radius:50%;background:#1428a0;margin-left:32px}@keyframes aqtk{to{transform:translateX(-50%)}}@media(prefers-reduced-motion:reduce){.aq-tk-track{animation:none}.aq-tk-view{overflow-x:auto}}.tf-card{position:relative}.tf-card.top{border-color:#1428a0!important;box-shadow:0 14px 34px rgba(20,40,160,.22)!important}.tf-badge{position:absolute;z-index:3;top:12px;left:12px;background:#1428a0;color:#fff;font:800 12px Inter,sans-serif;letter-spacing:.03em;padding:6px 12px;border-radius:999px;box-shadow:0 6px 14px rgba(20,40,160,.35)}.aq-nav a.nav-top{color:#1428a0;font-weight:800}.aq-hero.compacto{padding:12px 0 40px}.aq-hero.compacto .lead,.aq-hero.compacto .aq-trust{display:none}.aq-hero.compacto .aq-stage{max-width:230px}.aq-sec.estante-top h2{font-size:1.45rem;margin:0 0 12px}.aq-hero.compacto .aq-hero-in{gap:20px}.aq-hero.compacto h1{font-size:clamp(1.65rem,3vw,2.3rem);margin:2px 0 8px}.aq-hero.compacto p.lead{font-size:.98rem}.aq-hero.compacto .aq-big{margin-top:12px}.aq-hero.compacto .aq-trust{margin-top:10px}@media(max-width:640px){.aq-hero.compacto p.lead{display:none}.aq-hero.compacto{padding:12px 0 36px}.aq-hero.compacto .aq-big{display:none}}.aq-sec.estante-top{padding-top:8px}.aq-up{position:fixed;left:max(14px,env(safe-area-inset-left,0px));bottom:calc(16px + env(safe-area-inset-bottom,0px));z-index:50;background:#1428a0;color:#fff;border:2px solid #fff;border-radius:999px;padding:12px 18px;font:700 14px Inter,sans-serif;text-decoration:none;box-shadow:0 10px 26px rgba(0,0,0,.3);opacity:0;pointer-events:none;transform:translateY(12px);transition:.25s}.aq-up.on{opacity:1;pointer-events:auto;transform:none}.qa-datos{list-style:none;margin:14px 0 0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:8px}.qa-datos li{background:rgba(255,255,255,.7);border:1px solid rgba(20,40,160,.14);border-radius:10px;padding:8px 12px;font-size:.88rem}.qa-datos b{display:block;font-size:.72rem;letter-spacing:.04em;text-transform:uppercase;color:#1428a0}.eqt a.aq-tile,.eqt a.aq-tile b,.eqt a.aq-tile p{text-decoration:none!important}.eqt a.aq-tile b{color:#1428a0}.qa-meta{margin:12px 0 0;font-size:.78rem;opacity:.7}.tf-badge{background:#ffc21a;color:#0b1f4d}.hero .kicker,.aq-hero .kicker{background:#ffc21a!important;color:#0b1f4d!important}.aq-brand img{height:42px;width:auto}\n"
(OUT / "tema.css").write_text(css, encoding="utf-8")
m_v = re.search(r":root\{([^}]*)\}", css)
c1 = css[css.index("/* ---------- barra superior y encabezado ---------- */"):css.index("/* ---------- portada de página (hero) ---------- */")]
c2 = css[css.index("/* ---------- pie ---------- */"):css.index("/* lightbox y pasarela heredados */")]
c3 = "\n".join(l for l in css[css.index("/* ===== Paleta del logo"):].splitlines() if ".aq-" in l)
(OUT / "aqua-shell.css").write_text(".aq-h,.aq-f,.aq-wa{" + m_v.group(1) + "}\n" + c1 + c2 + c3, encoding="utf-8")

# ---------------------------------------------------------------- servidor: carrito, pedidos, correo, hoja (el mismo de las demás tiendas)
api = OUT / "api"
api.mkdir()
for f in ("lib.php", "pedido.php", "estado.php", "wompi.php", "sitio.php", "reconciliar.php"):
    shutil.copy(SRC / "api" / f, api / f)
lib = (api / "lib.php").read_text(encoding="utf-8")
if TOKEN:
    lib = lib.replace("w-s2eiVewLzOHFjK7HAR9UUeqFoNMS14k_Gfrqt_ND4", TOKEN)
(api / "lib.php").write_text(lib, encoding="utf-8")
(OUT / "data").mkdir()
(OUT / "data" / ".htaccess").write_text("Require all denied\n")
(api / ".htaccess").write_text('<FilesMatch "^(config|config\\.sample|lib|catalogo|sitio)\\.php$">\nRequire all denied\n</FilesMatch>\n')
prods = {p["id"]: {"nombre": p["nombre"], "ref": p["ref"], "marca": p["marca_prod"] or "Repuestos", "precio": p["precio"], "pack": p["precio"] * 2, "slug": p["slug"], "alias": [p["ref"]], "modelos": p["modelos"], "nota": p["resumen"], "link_pago": p["link"],
                   "ubic": "", "url": p["url"], "img": p["img"]} for p in PS if p["precio"]}
cat = {"fecha": HOY, "ciudades": cat_php["ciudades"], "dias": cat_php.get("dias", {}), "rutas_ciudad": {}, "marcas": [], "paginas": [], "guias": [], "compat": [], "blog": [], "productos": prods}


def php_val(v):
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


(api / "catalogo.php").write_text("<?php\n// Generado por ads_lg.py: no lo edites a mano.\nreturn " + php_val(cat) + ";\n", encoding="utf-8")
cfg = (SRC / "api" / "config.sample.php").read_text(encoding="utf-8")
cfg = (cfg.replace("'dominio' => 'https://filtrosnevecones.com'", f"'dominio' => '{DOMINIO}'").replace("w-s2eiVewLzOHFjK7HAR9UUeqFoNMS14k_Gfrqt_ND4", TOKEN)
       .replace("'nombre'    => 'Filtros Nevecones Colombia'", f"'nombre'    => '{NOMBRE}'").replace("'whatsapp' => '3107147299'", f"'whatsapp' => '{WA[2:]}'")
       .replace("'telefono'  => '310 714 7299'", f"'telefono'  => '{TEL}'").replace("'gtm' => 'GTM-5WSNHV66'", f"'gtm' => '{GTM}'").replace("'contraentrega' => ['activo' => true, 'recargo' => 5000]", "'contraentrega' => ['activo' => true, 'recargo' => 0]"))
# Hoja de cálculo, correo y panel: se leen de variables de entorno para no guardar claves en el repositorio
for _k, _v in (("'hoja' => ['url' => '', 'clave' => '']", f"'hoja' => ['url' => '{os.environ.get('HOJA_URL', '')}', 'clave' => '{os.environ.get('HOJA_CLAVE', '')}']"), ("'admin_clave' => ''", f"'admin_clave' => '{os.environ.get('ADMIN_CLAVE', '')}'")):
    cfg = cfg.replace(_k, _v, 1)
if os.environ.get("CORREO_AVISOS"):
    cfg = cfg.replace("'correo_avisos'    => 'serviciotecnicoyrepuestoscali@gmail.com'", f"'correo_avisos'    => '{os.environ['CORREO_AVISOS']}'", 1)
if os.environ.get("SMTP_CLAVE"):
    cfg = cfg.replace("'clave'   => '',", f"'clave'   => '{os.environ['SMTP_CLAVE']}',", 1)
(api / "config.sample.php").write_text(cfg, encoding="utf-8")
if os.environ.get("HOJA_CLAVE"):
    (api / "config.php").write_text(cfg, encoding="utf-8")
shutil.copy(SRC / "estilo.css", OUT / "estilo.css")
shutil.copy(SRC / "carrito.js", OUT / "carrito.js")
for f in ("carrito.php", "gracias.php", "admin.php", "diagnostico.php", "terminos.php", "privacidad.php", "garantia-y-retracto.php", "opinion.php"):
    shutil.copy(SRC / f, OUT / f)
c = (OUT / "carrito.php").read_text(encoding="utf-8")
c = c.replace("'ref' => $p['ref'], 'marca' => $p['marca']", "'ref' => $p['ref'], 'url' => $p['url'] ?? '', 'img' => $p['img'] ?? '', 'marca' => $p['marca']", 1)
c = re.sub(r'<a class="lim" href=.*?</picture></a>', '<a class="lim" href="/${p.url}"><img src="/${p.img}" alt="${esc(p.nombre)}" width="96" height="96" style="object-fit:contain"></a>', c, flags=re.S)
c = re.sub(r'<a href="/\$\{p\.marca\.toLowerCase\(\).*?/\$\{p\.slug\}/">', '<a href="/${p.url}">', c)
assert "'url' => $p['url']" in c and "${p.url}" in c and "p.marca.toLowerCase" not in c
(OUT / "carrito.php").write_text(c, encoding="utf-8")
for f in ("carrito.php", "gracias.php", "terminos.php", "privacidad.php", "garantia-y-retracto.php", "opinion.php", "admin.php"):
    t = (OUT / f).read_text(encoding="utf-8")
    t = t.replace('href="/tienda/"', 'href="/index.html#protectores"').replace('href="/envios/"', 'href="/envios-y-contra-entrega.html"')
    (OUT / f).write_text(t, encoding="utf-8")
(OUT / "pasarela.css").write_text(pintar(open(AQUI / "ads22.py", encoding="utf-8").read().split('(OUT / "pasarela.css").write_text("""')[1].split('""", encoding="utf-8")')[0])
                                  + "\n.btn{background:#1428a0!important;border-color:#1428a0!important;color:#fff!important}.btn:hover{background:#0f1f80!important}.btn.ghost{background:#fff!important;color:#1428a0!important}\n", encoding="utf-8")

ICONOS = {"lupa": '<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>', "caja": '<svg viewBox="0 0 24 24"><path d="M21 8 12 3 3 8v8l9 5 9-5z"/><path d="m3 8 9 5 9-5M12 13v8"/></svg>',
          "candado": '<svg viewBox="0 0 24 24"><rect x="4" y="10" width="16" height="11" rx="2.5"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>', "efectivo": '<svg viewBox="0 0 24 24"><rect x="2.5" y="6" width="19" height="12" rx="2"/><circle cx="12" cy="12" r="2.6"/></svg>',
          "retorno": '<svg viewBox="0 0 24 24"><path d="M9 14 4 9l5-5"/><path d="M4 9h10a6 6 0 0 1 0 12h-3"/></svg>'}





# ---------------------------------------------------------------- piezas comunes de las páginas
ICONOS_PLACEHOLDER = None
FPAGO = "Pagas en línea con Wompi (tarjeta, PSE, Nequi o Bancolombia) o contra entrega, en efectivo, sin recargo."
ENVIO_TXT = "Envío gratis a toda Colombia"
U = lambda n: n


def fix(t):
    return t


def encabezado():
    prod = "".join(f'<a href="{p["url"]}"><img src="{p["img"]}" alt="" width="62" height="62" loading="lazy"><span><b>{esc(p["corto"])}</b><small>110 VAC · {p["amp"]} A</small><em>{cop(p["precio"])}</em></span></a>' for p in PS)
    return ('<div class="aq-h"><div class="aq-bar"><span>✔ Envío gratis a toda Colombia</span><span>🔒 Pago seguro con Wompi · Contra entrega</span><a href="tel:+' + WA + '">' + TEL + '</a></div>'
            '<div class="aq-row aq-wrap"><a class="aq-brand" href="index.html"><img src="img/logo-bm.png" alt="Breakermatic" width="42" height="42"><span><b>Protectores de voltaje</b><small>Breakermatic · neveras, lavadoras y TV</small></span></a>'
            '<form class="aq-search" role="search" onsubmit="return false">' + ICONOS["lupa"].replace("<svg", '<svg aria-hidden="true"') + '<input type="search" data-aq-q placeholder="Busca tu protector: nevera, lavadora, televisor…" autocomplete="off" aria-label="Buscar protector"><div class="aq-res" hidden></div></form>'
            '<a class="aq-cart" href="carrito.php" aria-label="Ver carrito">🛒<span data-cart-n hidden></span></a><a class="aq-cta" href="index.html#protectores">Ver protectores</a></div>'
            '<nav class="aq-nav" aria-label="Principal"><div class="aq-wrap"><a href="index.html">Inicio</a>'
            f'<details class="aq-dd"><summary>Protectores</summary><div class="aq-pop prod"><div class="aq-wrap">{prod}</div></div></details>'
            '<a href="como-elegir-protector-de-voltaje.html">¿Cuál necesito?</a><a href="para-que-sirve-un-protector-de-voltaje.html">Guía</a><a href="preguntas-frecuentes-protector-de-voltaje.html">Preguntas</a><a href="envios-y-contra-entrega.html">Envíos y pagos</a><a href="contacto.html">Contacto</a>'
            '</div></nav></div>')


def pie():
    refs = "".join(f'<li><a href="{p["url"]}">{esc(p["corto"])} · {cop(p["precio"])}</a></li>' for p in PS)
    return ('<footer class="aq-f"><div class="aq-wrap"><div class="brandcol"><span class="logo-w"><img src="img/logo-bm.png" alt="Protectores Breakermatic" width="48" height="48" loading="lazy"></span>'
            '<p>Tienda en línea de protectores electrónicos de voltaje Breakermatic para neveras, lavadoras y televisores, con envío gratis a toda Colombia. Breakermatic es una marca de su propietario; '
            'esta tienda comercializa sus productos de forma independiente.</p></div>'
            f'<div><h5>Protectores</h5><ul>{refs}<li><a href="como-elegir-protector-de-voltaje.html">Cuál necesito</a></li></ul></div>'
            '<div><h5>Ayuda</h5><ul><li><a href="como-elegir-protector-de-voltaje.html">Cómo elegir</a></li><li><a href="para-que-sirve-un-protector-de-voltaje.html">Para qué sirve</a></li><li><a href="preguntas-frecuentes-protector-de-voltaje.html">Preguntas frecuentes</a></li>'
            '<li><a href="envios-y-contra-entrega.html">Envíos y pagos</a></li><li><a href="garantia-cambio-y-devolucion.html">Garantía y cambios</a></li><li><a href="mapa-del-sitio.html">Mapa del sitio</a></li></ul></div>'
            '<div><h5>Tienda</h5><ul><li><a href="quienes-somos.html">Quiénes somos</a></li><li><a href="contacto.html">Contacto</a></li><li><a href="terminos.php">Términos</a></li><li><a href="privacidad.php">Datos personales</a></li></ul></div></div>'
            '<div class="aq-wrap aq-f-pay"><div><span class="m">Tarjeta</span><span class="m">PSE</span><span class="m">Nequi</span><span class="m">Bancolombia</span><span class="m">Contra entrega</span></div>'
            f'<div>© 2026 {esc(NOMBRE)}</div></div></footer>'
            f'<a class="aq-wa" href="https://wa.me/{WA}?text=' + "Hola%2C%20necesito%20un%20repuesto" + '" aria-label="WhatsApp"><svg width="22" height="22" fill="#fff" viewBox="0 0 16 16"><path d="M13.6 2.3A7.85 7.85 0 0 0 8 0C3.6 0 .07 3.56.06 7.93c0 1.4.37 2.76 1.06 3.97L0 16l4.2-1.1a7.93 7.93 0 0 0 3.8.97c4.37 0 7.93-3.56 7.93-7.93a7.9 7.9 0 0 0-2.33-5.61zM8 14.5c-1.2 0-2.37-.32-3.4-.93l-.24-.15-2.5.65.67-2.43-.16-.25A6.5 6.5 0 1 1 8 14.5z"/></svg><span>WhatsApp</span></a>')


def tarjeta(p, k=None):
    feat = [f"110 VAC · hasta {p['amp']} A", f"{p['tomas']} toma{'s' if p['tomas'] > 1 else ''} · espera de {p['espera']}", "4 luces indicadoras de voltaje"]
    top = p["id"] == "bm-nev"
    return (f'<article class="tf-card{" top" if top else ""}">' + ('<span class="tf-badge">★ Más pedido</span>' if top else "") + f'<a class="tf-img" href="{p["url"]}" aria-label="Ficha técnica: {esc(p["nombre"])}"><img src="{p["img"][:-5]}-480.webp" alt="{esc(p["nombre"])}" width="480" height="480" loading="lazy"></a>'
            f'<div class="tf-b"><h3><a href="{p["url"]}">{esc(p["nombre"])}</a></h3><span class="tf-code">Breakermatic · {esc(p["corto"])}</span><ul class="tf-feat">{"".join(f"<li>{esc(x)}</li>" for x in feat)}</ul>'
            f'<div class="tf-pr">{cop(p["precio"])}<small>COP · envío gratis</small></div><button type="button" class="tf-add" data-add="{p["id"]}">🛒 Agregar al carrito</button></div></article>')


def qa(titulo, respuesta, datos=None):
    d = ""
    if datos:
        d = '<ul class="qa-datos">' + "".join(f"<li><b>{esc(k)}</b>{esc(v)}</li>" for k, v in datos) + "</ul>"
    return (f'<section class="aq-qa-sec"><div class="wrap"><div class="qa" data-ia="respuesta"><p class="tag">⚡ Respuesta rápida</p><h2>{esc(titulo)}</h2><p>{respuesta}</p>{d}'
            f'<p class="qa-meta">Información verificada · actualizada el {FECHA_LARGA} · Protectores Breakermatic con envío gratis a toda Colombia</p></div></div></section>')


def seccion(h2, cuerpo, alt=False, sub=""):
    return f'<section class="aq-sec{" alt" if alt else ""}"><div class="wrap"><h2>{h2}</h2>' + (f'<p class="sub2">{sub}</p>' if sub else "") + cuerpo + "</div></section>"


def faq_html(preg, h2="Preguntas frecuentes"):
    return ('<section class="aq-sec alt"><div class="wrap"><h2>' + esc(h2) + '</h2><div class="faq-num">'
            + "".join(f'<details{" open" if i == 0 else ""}><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for i, (q, a) in enumerate(preg)) + "</div></div></section>")


def ld_base(nombre, titulo, desc, miga):
    url = f"{DOMINIO}/{nombre}" if nombre != "index.html" else f"{DOMINIO}/"
    return [{"@type": "WebPage", "@id": url, "name": titulo, "url": url, "inLanguage": "es-CO", "description": desc, "dateModified": HOY, "isPartOf": {"@id": f"{DOMINIO}/#tienda"}, "about": {"@type": "Brand", "name": "Breakermatic"}},
            {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, **({"item": f"{DOMINIO}/{u}"} if u else {})} for i, (n, u) in enumerate(miga)]}]


def ld_faq(preg):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in preg]}


def ld_producto(p):
    return {"@type": "Product", "name": p["nombre"], "sku": p["ref"], "mpn": p["ref"], "image": f"{DOMINIO}/{p['img']}", "brand": {"@type": "Brand", "name": "Breakermatic"}, "category": "Protectores de voltaje",
            "description": p["resumen"],
            "additionalProperty": [{"@type": "PropertyValue", "name": "Voltaje", "value": "110 VAC"}, {"@type": "PropertyValue", "name": "Corriente máxima", "value": f"{p['amp']} A"}, {"@type": "PropertyValue", "name": "Tomas", "value": str(p["tomas"])},
                                   {"@type": "PropertyValue", "name": "Ciclo de espera", "value": p["espera"]}],
            "offers": {"@type": "Offer", "url": f"{DOMINIO}/{p['url']}", "priceCurrency": "COP", "price": str(p["precio"]), "availability": "https://schema.org/InStock", "itemCondition": "https://schema.org/NewCondition",
                       "priceValidUntil": "2027-12-31", "seller": {"@id": f"{DOMINIO}/#tienda"},
                       "hasMerchantReturnPolicy": {"@type": "MerchantReturnPolicy", "applicableCountry": "CO", "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow", "merchantReturnDays": 5},
                       "shippingDetails": {"@type": "OfferShippingDetails", "shippingRate": {"@type": "MonetaryAmount", "value": "0", "currency": "COP"}, "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "CO"}}}}


TIENDA_LD = {"@type": "OnlineStore", "@id": f"{DOMINIO}/#tienda", "name": NOMBRE, "url": f"{DOMINIO}/", "logo": f"{DOMINIO}/img/logo-bm.png", "image": f"{DOMINIO}/img/og.jpg", "areaServed": {"@type": "Country", "name": "Colombia"},
             "currenciesAccepted": "COP", "paymentAccepted": "Tarjeta de crédito, tarjeta débito, PSE, Nequi, Bancolombia, contra entrega",
             "contactPoint": {"@type": "ContactPoint", "telephone": "+" + WA, "contactType": "customer service", "areaServed": "CO", "availableLanguage": "es"}}


def estante_min():
    return ""


def pagina(nombre, titulo, desc, kw, miga, cuerpo, preguntas=(), ld_extra=(), prio="0.6", og=None, hero=None):
    titulo = titulo.strip()
    if len(titulo) > 66:
        titulo = titulo[:66].rsplit(" ", 1)[0].rstrip(" ,:;·|-")
    if len(desc) > 160:
        c = desc[:160]
        k = max(c.rfind(". "), c.rfind(": "), c.rfind("; "), c.rfind(", "))
        desc = (c[:k] if k > 90 else c[:c.rfind(" ")]).rstrip(" ,;:.") + "."
    url = f"{DOMINIO}/{nombre}" if nombre != "index.html" else f"{DOMINIO}/"
    graf = ld_base(nombre, titulo, desc, miga) + ([ld_faq(list(preguntas))] if preguntas else []) + list(ld_extra)
    if nombre == "index.html":
        graf.append(TIENDA_LD)
    bc = '<div class="breadcrumb wrap" style="font:500 13px Inter,sans-serif;padding:16px 22px 0;">' + " / ".join(f'<a href="{u}">{esc(n)}</a>' if u else esc(n) for n, u in miga) + "</div>" if len(miga) > 1 else ""
    gtm_js = (("<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','" + GTM + "');</script>") if GTM else "")
    head = ('<!DOCTYPE html><html lang="es-CO"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">'
            f'<title>{esc(titulo)}</title><meta name="description" content="{esc(desc)}"><meta name="keywords" content="{esc(kw)}"><link rel="canonical" href="{url}">'
            f'<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1"><meta name="theme-color" content="#1428a0"><meta name="author" content="{esc(NOMBRE)}"><meta name="geo.region" content="CO"><meta name="geo.placename" content="Colombia">'
            f'<link rel="alternate" hreflang="es-CO" href="{url}"><link rel="alternate" hreflang="x-default" href="{url}"><link rel="alternate" type="text/plain" href="{DOMINIO}/llms.txt" title="llms.txt">'
            + "".join(f'<meta name="google-site-verification" content="{t_}">' for t_ in TOKENS) + gtm_js
            + f'<meta property="og:type" content="website"><meta property="og:locale" content="es_CO"><meta property="og:site_name" content="{esc(NOMBRE)}"><meta property="og:title" content="{esc(titulo)}">'
            f'<meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{DOMINIO}/{og or "img/og.jpg"}"><meta property="og:image:alt" content="{esc(titulo)}">'
            f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(titulo)}"><meta name="twitter:description" content="{esc(desc)}">'
            '<link rel="icon" type="image/svg+xml" href="img/logo-bm.svg"><link rel="apple-touch-icon" href="img/icono-bm.png"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">'
            '<link rel="stylesheet" href="tema.css?v=bm1"><link rel="stylesheet" href="pasarela.css">'
            f'<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graf}, ensure_ascii=False)}</script></head><body>' + (f'<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM}" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>' if GTM else ""))
    t = head + encabezado() + bc + cuerpo + pie() + '<a class="aq-up" href="' + ("#repuestos" if nombre == "index.html" else "index.html#repuestos") + '">↑ Ver repuestos</a><script>(function(){var a=document.querySelector(".aq-up");if(!a)return;function f(){a.classList.toggle("on",window.scrollY>700)}f();addEventListener("scroll",f,{passive:true})})();</script><script src="buscar.js" defer></script><script src="carrito.js" defer></script></body></html>'
    (OUT / nombre).write_text(t, encoding="utf-8")
    PAGINAS.append((nombre, prio, titulo, desc))
    return t


def hero_simple(kicker, h1, sub):
    return f'<section class="hero"><div class="wrap"><span class="kicker">{esc(kicker)}</span><h1>{esc(h1)}</h1><p class="sub" style="margin-top:16px;">{esc(sub)}</p></div></section>'



def encabezado():
    eqs = "".join(f'<a href="{R_EQ(eq)}"><span><b>Repuestos para {esc(eq.lower())}</b><small>{esc(", ".join(c.lower() for c in cs))}</small></span></a>' for eq, cs in EQUIPOS.items())
    marcas = "".join(f'<a href="marca-{slug(m)}.html"><span><b>{esc(m)}</b></span></a>' for m in MARCAS_EQ)
    return ('<div class="aq-h"><div class="aq-bar"><span>✔ Envío a toda Colombia</span><span>🔒 Pago seguro con Wompi · Contra entrega</span><a href="tel:+' + WA + '">' + TEL + '</a></div>'
            '<div class="aq-row aq-wrap"><a class="aq-brand" href="index.html"><img src="img/logo-bm.png" alt="Repuestos de línea blanca" width="42" height="42"><span><b>Repuestos de línea blanca</b><small>Lavadoras · neveras · protectores</small></span></a>'
            '<form class="aq-search" role="search" onsubmit="return false">' + ICONOS["lupa"].replace("<svg", '<svg aria-hidden="true"') + '<input type="search" data-aq-q placeholder="Busca tu repuesto: manguera, presostato, protector…" autocomplete="off" aria-label="Buscar repuesto"><div class="aq-res" hidden></div></form>'
            '<a class="aq-cart" href="carrito.php" aria-label="Ver carrito">🛒<span data-cart-n hidden></span></a><a class="aq-cta" href="index.html#repuestos">Ver repuestos</a></div>'
            '<nav class="aq-nav" aria-label="Principal"><div class="aq-wrap"><a href="index.html">Inicio</a>'
            f'<details class="aq-dd"><summary>Equipos</summary><div class="aq-pop prod"><div class="aq-wrap">{eqs}</div></div></details>'
            f'<details class="aq-dd"><summary>Marcas</summary><div class="aq-pop prod"><div class="aq-wrap">{marcas}</div></div></details>'
            '<a href="como-elegir-repuesto-para-lavadora.html">¿Cuál necesito?</a><a href="como-encontrar-el-modelo-de-tu-electrodomestico.html">Tu modelo</a><a href="preguntas-frecuentes-repuestos.html">Preguntas</a><a href="envios-y-pagos.html">Envíos y pagos</a><a href="contacto.html">Contacto</a>'
            '</div></nav></div>')


def pie():
    eqs = "".join(f'<li><a href="{R_EQ(eq)}">Repuestos para {esc(eq.lower())}</a></li>' for eq in EQUIPOS)
    marcas = "".join(f'<li><a href="marca-{slug(m)}.html">{esc(m)}</a></li>' for m in MARCAS_EQ)
    return ('<footer class="aq-f"><div class="aq-wrap"><div class="brandcol"><span class="logo-w"><img src="img/logo-bm.png" alt="Repuestos de línea blanca" width="48" height="48" loading="lazy"></span>'
            '<p>Tienda en línea de repuestos para lavadoras y neveras, con envío a toda Colombia. Los nombres de marcas se usan solo para indicar compatibilidad; esta tienda es independiente y no tiene afiliación con los fabricantes.</p></div>'
            f'<div><h5>Equipos</h5><ul>{eqs}</ul></div><div><h5>Marcas</h5><ul>{marcas}</ul></div>'
            '<div><h5>Ayuda</h5><ul><li><a href="como-elegir-repuesto-para-lavadora.html">Cómo elegir</a></li><li><a href="como-encontrar-el-modelo-de-tu-electrodomestico.html">Tu modelo</a></li><li><a href="preguntas-frecuentes-repuestos.html">Preguntas frecuentes</a></li>'
            '<li><a href="envios-y-pagos.html">Envíos y pagos</a></li><li><a href="garantia-cambio-y-devolucion.html">Garantía y cambios</a></li><li><a href="quienes-somos.html">Quiénes somos</a></li><li><a href="contacto.html">Contacto</a></li><li><a href="terminos.php">Términos</a></li><li><a href="privacidad.php">Datos personales</a></li><li><a href="mapa-del-sitio.html">Mapa del sitio</a></li></ul></div></div>'
            '<div class="aq-wrap aq-f-pay"><div><span class="m">Tarjeta</span><span class="m">PSE</span><span class="m">Nequi</span><span class="m">Bancolombia</span><span class="m">Contra entrega</span></div>'
            f'<div>© 2026 {esc(NOMBRE)}</div></div></footer>'
            f'<a class="aq-wa" href="https://wa.me/{WA}?text=Hola%2C%20necesito%20un%20repuesto" aria-label="WhatsApp"><svg width="22" height="22" fill="#fff" viewBox="0 0 16 16"><path d="M13.6 2.3A7.85 7.85 0 0 0 8 0C3.6 0 .07 3.56.06 7.93c0 1.4.37 2.76 1.06 3.97L0 16l4.2-1.1a7.93 7.93 0 0 0 3.8.97c4.37 0 7.93-3.56 7.93-7.93a7.9 7.9 0 0 0-2.33-5.61zM8 14.5c-1.2 0-2.37-.32-3.4-.93l-.24-.15-2.5.65.67-2.43-.16-.25A6.5 6.5 0 1 1 8 14.5z"/></svg><span>WhatsApp</span></a>')


def tarjeta(p, k=None):
    feat = [p["categoria"] + " · " + p["equipo"], ("Para " + p["marca_eq"]) if p["marca_eq"] not in ("", "Todas las marcas") else "Sirve para varias marcas"]
    if p["espec"]:
        feat.append(f"110 VAC · hasta {p['espec'][0]} A · {p['espec'][1]} toma(s)")
    elif p["ref"] != p["sku"]:
        feat.append("Ref. " + p["ref"])
    if p["precio"]:
        pie_t = f'<div class="tf-pr">{cop(p["precio"])}<small>COP · envío gratis</small></div><button type="button" class="tf-add" data-add="{p["id"]}">🛒 Agregar al carrito</button>'
    else:
        pie_t = f'<div class="tf-pr" style="font-size:1.1rem">Consulta el precio</div><a class="tf-add" style="text-align:center;text-decoration:none;display:block" href="{wa_pieza(p)}" rel="noopener">Consultar por WhatsApp</a>'
    return (f'<article class="tf-card"><a class="tf-img" href="{p["url"]}" aria-label="{esc(p["nombre"])}"><img src="{p["img"][:-5]}-480.webp" alt="{esc(p["nombre"])}" width="480" height="480" loading="lazy"></a>'
            f'<div class="tf-b"><h3><a href="{p["url"]}">{esc(p["nombre"])}</a></h3><span class="tf-code">{esc(p["marca_prod"] if p["marca_prod"] and not p["marca_prod"].startswith("PENDIENTE") else p["categoria"])}</span><ul class="tf-feat">{"".join(f"<li>{esc(x)}</li>" for x in feat)}</ul>{pie_t}</div></article>')


def ld_producto(p):
    d = {"@type": "Product", "name": p["nombre"], "sku": p["sku"], "image": f"{DOMINIO}/{p['img']}", "category": p["categoria"], "description": p["resumen"]}
    if p["marca_prod"] and not p["marca_prod"].startswith("PENDIENTE"):
        d["brand"] = {"@type": "Brand", "name": p["marca_prod"]}
    if p["ref"] != p["sku"]:
        d["mpn"] = p["ref"]
    if p["precio"]:
        d["offers"] = {"@type": "Offer", "url": f"{DOMINIO}/{p['url']}", "priceCurrency": "COP", "price": str(p["precio"]), "availability": "https://schema.org/InStock", "itemCondition": "https://schema.org/NewCondition", "priceValidUntil": "2027-12-31", "seller": {"@id": f"{DOMINIO}/#tienda"},
                       "hasMerchantReturnPolicy": {"@type": "MerchantReturnPolicy", "applicableCountry": "CO", "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow", "merchantReturnDays": 5},
                       "shippingDetails": {"@type": "OfferShippingDetails", "shippingRate": {"@type": "MonetaryAmount", "value": "0", "currency": "COP"}, "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "CO"}}}
    return d


TIENDA_LD["name"] = NOMBRE

exec(open(AQUI / "ads_rp_paginas.py", encoding="utf-8").read())
