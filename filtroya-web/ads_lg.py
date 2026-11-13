#!/usr/bin/env python3
"""Tienda de filtros de agua LG con el mismo proyecto de filtrodeaguasamsung.com: páginas .html con «Respuesta rápida» al inicio de cada una (para Google y para que las IA nos recomienden),
home con todos los filtros y sus fichas técnicas, una página por ciudad con contenido propio, regiones, áreas, departamentos, A–Z, glosario, preguntas frecuentes, guías, pasarela de pagos (Wompi y contra entrega),
carrito, pedidos por correo y hoja, llms.txt, sitemap y robots.

Uso:  python3 ads_lg.py <carpeta_de_salida> [dominio] [etiqueta_search_console]
"""
import datetime
import html
import json
import pathlib
import random
import re
import shutil
import subprocess
import sys
import unicodedata

from PIL import Image, ImageChops, ImageDraw

import ads22_hubs
import ads22_local
import ciudad_unica
import galeria
import marcas_contenido_lg

AQUI = pathlib.Path(__file__).resolve().parent
OUT = pathlib.Path(sys.argv[1])
DOMINIO = (sys.argv[2] if len(sys.argv) > 2 else "https://tu-dominio-lg.com").rstrip("/")
TOKEN = sys.argv[3] if len(sys.argv) > 3 else ""
HOY = datetime.date.today().isoformat()
WA, TEL = "573054796329", "305 479 6329"
SRC = AQUI / "src"
esc = lambda s: html.escape(str(s), quote=True)
cop = lambda v: "$" + f"{int(v):,}".replace(",", ".")
cop2 = lambda v: "$ " + f"{int(v):,}".replace(",", ".")


def slug(n):
    n = unicodedata.normalize("NFKD", n).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", n).strip("-")


# ---------------------------------------------------------------- datos
cat_php = json.loads(subprocess.run(["php", "-r", f'echo json_encode(require "{AQUI}/sitios/lg/api/catalogo.php");'], capture_output=True, text=True, check=True).stdout)
PS = []
for pid, p in cat_php["productos"].items():
    refs = [p["ref"]] + [a for a in p["alias"] if a != p["ref"]]
    PS.append(dict(id=pid, nombre_largo=p["nombre"], nombre=p["nombre"], ref=p["ref"], refs=refs, modelos=p["modelos"], precio=p["precio"], link=p["link_pago"], nota=p.get("nota", ""), ubic=p["ubic"],
                   slug=p["slug"], slug_o=p["slug"], corto=p["nombre"].replace("Filtro LG ", "").replace("Filtro ", ""), url=p["slug"] + ".html", img=f"img/p-{pid}.webp"))
for p in PS:
    p["corto"] = {"lg-600-o": "LT600P", "lg-ex-o": "Externo ADQ73693903"}.get(p["id"], p["corto"].split(" ")[0])
    p["h"] = p["nombre"] + (f" ({p['ref']})" if p["ref"] not in p["nombre"] else "")
PREC = sorted(p["precio"] for p in PS)
RANGO = f"{cop(PREC[0])} a {cop(PREC[-1])}"
MODELOS = [(m, p) for p in PS for m in p["modelos"]]

# ciudades: las de la app + los municipios extra (mismas listas de las demás tiendas), con departamento
app = open(AQUI.parent / "filtros-app" / "index.html", encoding="utf-8").read()
m_ = re.search(r"\nconst CIUDADES_CO = (\[[^\n]*\]|\[.*?\n\]);", app, re.S)
CIUDADES_CO = json.loads(subprocess.run(["node", "-e", f"process.stdout.write(JSON.stringify({m_.group(1)}))"], capture_output=True, text=True, check=True).stdout)
import ciudades_extra
import ciudades_mas
CIU = [list(c) for c in CIUDADES_CO]
vistos = {slug(c[0]) for c in CIU}
nombres = {c[0] for c in CIU}
for depto_, noms in list(ciudades_extra.NUEVAS.items()) + list(ciudades_extra.ANTERIORES.items()) + list(ciudades_mas.MAS.items()):
    for n_ in noms:
        if (n_, depto_) in {(c[0], c[1]) for c in CIU}:
            continue
        nom = n_ if (slug(n_) not in vistos and n_ not in nombres) else f"{n_} ({depto_})"
        if slug(nom) in vistos:
            continue
        vistos.add(slug(nom))
        nombres.add(nom)
        CIU.append([nom, depto_])
GRANDES_S = {slug(c[0]) for c in CIUDADES_CO}
CIUDAD = {slug(c[0]): c for c in CIU}
POR_DEPTO = {}
for c in CIU:
    POR_DEPTO.setdefault(c[1], []).append(c)
for v in POR_DEPTO.values():
    v.sort(key=lambda c: c[0])
DEPTOS = sorted(POR_DEPTO)
TOP = [slug(x) for x in ("Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena", "Bucaramanga", "Cúcuta", "Pereira", "Santa Marta", "Ibagué", "Manizales", "Villavicencio", "Pasto", "Montería", "Neiva", "Armenia", "Soacha", "Valledupar", "Popayán", "Tunja")]
TOP = [s for s in TOP if s in CIUDAD]

# ---------------------------------------------------------------- salida
if OUT.exists():
    shutil.rmtree(OUT)
(OUT / "img").mkdir(parents=True)
PAGINAS = []  # (nombre, prioridad)


def foto_cuadrada(origen, destino, lado=800, uso=0.92):
    im = Image.open(origen)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        b_ = Image.new("RGB", im.size, (255, 255, 255))
        b_.paste(im, mask=im.getchannel("A"))
        im = b_
    im = im.convert("RGB")
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
    e = lado * uso / max(rgba.size)
    rgba = rgba.resize((max(1, round(rgba.width * e)), max(1, round(rgba.height * e))), Image.LANCZOS)
    lienzo = Image.new("RGBA", (lado, lado), (255, 255, 255, 0))
    lienzo.paste(rgba, ((lado - rgba.width) // 2, (lado - rgba.height) // 2), rgba)
    lienzo.save(destino, "WEBP", quality=90, method=6)


for p in PS:
    foto_cuadrada(AQUI / "public_html" / "filtrosnevecones-img" / f"{p['id']}.jpg", OUT / "img" / f"p-{p['id']}.webp")
shutil.copy(AQUI / "logos" / "lg-web.png", OUT / "img" / "logo-lg.png")
shutil.copy(AQUI / "logos" / "lg-icono.png", OUT / "img" / "icono-lg.png")

# galería de cada ficha: la foto + dos imágenes informativas con los datos del catálogo (en la paleta de LG)
galeria.AZUL, galeria.FONDO, galeria.LINEA = (165, 0, 52), (252, 247, 248), (234, 221, 225)
for p in PS:
    d = dict(corto=p["corto"], ref=p["ref"], forma="Externo" if p["ubic"] == "externo" else "Interno", como="Va en la manguera del agua" if p["ubic"] == "externo" else "Va dentro del nevecón",
             tipo="Externo (en la línea de agua)" if p["ubic"] == "externo" else "Interno (dentro del nevecón)", alias=p["refs"][:5], modelos=p["modelos"],
             pasos=(["Cierra la llave de paso del agua.", "Desconecta el filtro viejo de las mangueras.", "Conecta el filtro nuevo en el mismo sentido del flujo.", "Abre la llave y revisa que no gotee.", "Saca unos 6 litros de agua para purgar."]
                    if p["ubic"] == "externo" else ["Abre el refrigerador y ubica el filtro.", "Retira el filtro viejo.", "Quita las tapas del filtro nuevo.", "Instálalo hasta que quede firme.", "Saca unos 6 litros y reinicia el aviso."]))
    galeria.identificar("", d).save(OUT / "img" / f"gal-{p['id']}-identificar.jpg", quality=88, optimize=True)
    galeria.ficha("", d).save(OUT / "img" / f"gal-{p['id']}-ficha.jpg", quality=88, optimize=True)

# ---------------------------------------------------------------- estilos (paleta del logo de LG: magenta y blanco)
PAL = [("#071a6b", "#2a0a16"), ("#1428a0", "#a50034"), ("#2a46c8", "#c4204f"), ("#0f1f80", "#7d0027"), ("#5b7cff", "#e0577a"), ("#b9c8ff", "#f2b8c6"), ("#eaefff", "#fdeef2"), ("#c7d3ff", "#f2c4d0"),
       ("#d5deff", "#f7d3dc"), ("#dbe3ff", "#fbe1e8"), ("#aab8ff", "#ee9db3"), ("#0a1440", "#1d0f14"), ("#26305e", "#3a2830"), ("#3f4a78", "#5b4850"), ("#6b7699", "#8a757d"), ("#dde3f6", "#eadde1"),
       ("#f4f6fd", "#faf6f7"), ("#f6f8ff", "#fcf8f9"), ("#e1e6ff", "#f9e3e9"), ("#d5dcff", "#f0d6de"), ("#cdd5f5", "#e6cbd3"), ("#9aa6d6", "#c9a9b4"), ("#16257a", "#4a1a2a"), ("#26338a", "#5e2538"),
       ("#b9c4f5", "#f2c9d4"), ("#eef1ff", "#fdeef2"), ("rgba(91,124,255,", "rgba(224,87,122,"), ("rgba(10,20,64,", "rgba(29,15,20,"), ("rgba(20,40,160,", "rgba(165,0,52,"), ("rgba(120,150,255,", "rgba(230,110,140,"),
       ("#DCE3F2", "#eadde1"), ("#1428A0", "#a50034"), ("#2F5FE0", "#c4204f"), ("#0A1628", "#1d0f14"), ("#4A5A72", "#5b4850"), ("#E7ECFB", "#fdeef2"), ("#F2F5FC", "#faf6f7"), ("#8fb0ff", "#f2b8c6")]


def pintar(t):
    for a, b in PAL:
        t = t.replace(a, b)
    return t


css = pintar((AQUI / "ads22_tema.css").read_text(encoding="utf-8"))
css += "\n.aq-hero .kicker,.hero .kicker{background:rgba(255,255,255,.16)}.aq-brand img{height:38px}.aq-qa-sec{padding:0 0 12px}\n"
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
prods = {p["id"]: {"nombre": p["nombre"], "ref": p["ref"], "marca": "LG", "precio": p["precio"], "pack": p["precio"] * 2, "slug": p["slug"], "alias": p["refs"], "modelos": p["modelos"], "nota": p["nota"], "link_pago": p["link"],
                   "ubic": p["ubic"], "url": p["url"], "img": p["img"]} for p in PS}
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
       .replace("'nombre'    => 'Filtros Nevecones Colombia'", "'nombre'    => 'Filtro de Agua LG Colombia'").replace("'whatsapp' => '3107147299'", "'whatsapp' => '3054796329'")
       .replace("'telefono'  => '310 714 7299'", "'telefono'  => '305 479 6329'").replace("'contraentrega' => ['activo' => true, 'recargo' => 5000]", "'contraentrega' => ['activo' => true, 'recargo' => 0]"))
(api / "config.sample.php").write_text(cfg, encoding="utf-8")
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
    t = t.replace('href="/tienda/"', 'href="/index.html#filtros"').replace('href="/envios/"', '/envio-filtros-lg-colombia.html'.join(['href="', '"']))
    (OUT / f).write_text(t, encoding="utf-8")
(OUT / "pasarela.css").write_text(pintar(open(AQUI / "ads22.py", encoding="utf-8").read().split('(OUT / "pasarela.css").write_text("""')[1].split('""", encoding="utf-8")')[0])
                                  + "\n.btn{background:#a50034!important;border-color:#a50034!important;color:#fff!important}.btn:hover{background:#7d0027!important}.btn.ghost{background:#fff!important;color:#a50034!important}\n", encoding="utf-8")

# ---------------------------------------------------------------- piezas comunes de las páginas
ICONOS = {"lupa": '<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>', "caja": '<svg viewBox="0 0 24 24"><path d="M21 8 12 3 3 8v8l9 5 9-5z"/><path d="m3 8 9 5 9-5M12 13v8"/></svg>',
          "candado": '<svg viewBox="0 0 24 24"><rect x="4" y="10" width="16" height="11" rx="2.5"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>', "efectivo": '<svg viewBox="0 0 24 24"><rect x="2.5" y="6" width="19" height="12" rx="2"/><circle cx="12" cy="12" r="2.6"/></svg>',
          "retorno": '<svg viewBox="0 0 24 24"><path d="M9 14 4 9l5-5"/><path d="M4 9h10a6 6 0 0 1 0 12h-3"/></svg>'}
REG = {k: (v[0], [d for d in v[1] if d in POR_DEPTO], v[2]) for k, v in ads22_hubs.REGIONES.items()}
REG = {k: v for k, v in REG.items() if v[1]}
AREAS = {}
for k, (corto, largo, ss) in ads22_hubs.AREAS.items():
    miembros = [CIUDAD[s] for s in ss if s in CIUDAD]
    if len(miembros) >= 3:
        AREAS[k] = (corto, largo, miembros)
U = lambda n: f"{n}.html"
R_REG = lambda k: f"filtros-lg-region-{slug(k)}.html"
R_AREA = lambda k: f"filtro-nevera-lg-{k}.html"
R_DEPTO = lambda d: f"filtros-lg-{slug(d)}.html"
R_CIU = lambda s: f"filtro-agua-lg-{s}.html"
R_PRECIO = lambda s: f"precio-filtro-lg-{s}.html"
R_MOD = lambda m: f"filtro-nevecon-lg-{slug(m)}.html"
R_REF = lambda r: f"referencia-filtro-lg-{slug(r)}.html"


def fix(t):
    """Enlaces de directorio (/x/) a páginas .html, y clases de las tiendas nacionales a las de este sitio."""
    t = re.sub(r'href="/blog/([a-z0-9-]+)/"', r'href="\1.html"', t)
    t = re.sub(r'href="/(filtro-[a-z0-9-]+|filtros-[a-z0-9-]+|ciudades-con-[a-z0-9-]+|glosario-[a-z0-9-]+|cual-es-mi-filtro|cambio-e-instalacion|preguntas-frecuentes|mapa-del-sitio|blog)/"', r'href="\1.html"', t)
    t = re.sub(r'href="/([a-z0-9-]+)/"', r'href="\1.html"', t)
    for a, b in (("m-tabla-wrap", "tbl-wrap"), ("m-tabla", "spec-table"), ("m-chips", "city-tags"), ("m-mut", "note"), ("m-ok", "spec-list")):
        t = t.replace(a, b)
    return t


def encabezado():
    prod = "".join(f'<a href="{p["url"]}"><img src="{p["img"]}" alt="" width="62" height="62" loading="lazy"><span><b>{esc(p["corto"])}</b><small>{esc(p["ref"])}</small><em>{cop(p["precio"])}</em></span></a>' for p in PS)
    deptos = "".join(f'<a href="{R_DEPTO(d)}">{esc(d)}</a>' for d in DEPTOS)
    grandes = "".join(f'<a href="{R_CIU(s)}">{esc(CIUDAD[s][0])}</a>' for s in TOP[:14])
    regs = "".join(f'<a href="{R_REG(k)}">{esc(v[0])}</a>' for k, v in REG.items())
    areas = "".join(f'<a href="{R_AREA(k)}">{esc(v[0])}</a>' for k, v in AREAS.items())
    return ('<div class="aq-h"><div class="aq-bar"><span>🚚 Envío gratis a toda Colombia</span><span>💳 Pago seguro con Wompi · 💵 Contra entrega</span><a href="tel:+' + WA + '">' + TEL + '</a></div>'
            '<div class="aq-row aq-wrap"><a class="aq-brand" href="index.html"><img src="img/logo-lg.png" alt="LG" width="86" height="38"><span><b>Filtro de agua LG</b><small>Distribuidor autorizado · Colombia</small></span></a>'
            '<form class="aq-search" role="search" onsubmit="return false">' + ICONOS["lupa"].replace("<svg", '<svg aria-hidden="true"') + '<input type="search" data-aq-q placeholder="Tu ciudad, modelo de nevecón o código del filtro…" autocomplete="off" aria-label="Buscar ciudad, modelo o código"><div class="aq-res" hidden></div></form>'
            '<a class="aq-cart" href="carrito.php" aria-label="Ver carrito">🛒<span data-cart-n hidden></span></a><a class="aq-cta" href="index.html#filtros">Ver filtros</a></div>'
            '<nav class="aq-nav" aria-label="Principal"><div class="aq-wrap"><a href="index.html">Inicio</a>'
            f'<details class="aq-dd"><summary>Filtros</summary><div class="aq-pop prod"><div class="aq-wrap">{prod}</div></div></details>'
            f'<details class="aq-dd"><summary>Ciudades</summary><div class="aq-pop ciu"><div class="aq-wrap"><div><h5>Más buscadas</h5><div class="aq-chips">{grandes}</div></div><div><h5>Por región</h5><div class="aq-chips">{regs}</div><h5 style="margin-top:14px">Áreas metropolitanas</h5><div class="aq-chips">{areas}</div><h5 style="margin-top:14px">Por departamento</h5><div class="aq-chips">{deptos}</div></div></div></div></details>'
            '<a href="guias-filtro-agua-nevecon-lg.html">Guías</a><a href="cual-es-mi-filtro.html">¿Cuál es el mío?</a><a href="precio-filtro-agua-nevecon-lg.html">Precios</a><a href="filtro-agua-lg-por-ciudad-colombia.html">Todas las ciudades</a><a href="preguntas-frecuentes-filtro-agua-lg.html">Preguntas</a>'
            '</div></nav></div>')


def pie():
    refs = "".join(f'<li><a href="{p["url"]}">{esc(p["corto"])} · {cop(p["precio"])}</a></li>' for p in PS)
    ciu = "".join(f'<li><a href="{R_CIU(s)}">{esc(CIUDAD[s][0])}</a></li>' for s in TOP[:9])
    deptos = "".join(f'<li><a href="{R_DEPTO(d)}">{esc(d)}</a></li>' for d in DEPTOS[:9])
    return ('<footer class="aq-f"><div class="aq-wrap"><div class="brandcol"><span class="logo-w"><img src="img/logo-lg.png" alt="Filtro de Agua LG Colombia" width="60" height="26" loading="lazy"></span>'
            '<p>Somos distribuidores autorizados para la venta de filtros de agua compatibles con neveras LG en Colombia. No somos LG Electronics ni su canal oficial de venta, ni tenemos afiliación comercial con la corporación. '
            'Los nombres y modelos se usan solo con fines descriptivos de compatibilidad.</p></div>'
            f'<div><h5>Filtros</h5><ul>{refs}<li><a href="cual-es-mi-filtro.html">Cómo identificar el mío</a></li></ul></div>'
            f'<div><h5>Ciudades</h5><ul>{ciu}<li><a href="filtro-agua-lg-por-ciudad-colombia.html"><b>Ver todas →</b></a></li></ul></div><div><h5>Departamentos</h5><ul>{deptos}</ul></div>'
            '<div><h5>Ayuda</h5><ul><li><a href="guias-filtro-agua-nevecon-lg.html">Guías</a></li><li><a href="cambio-e-instalacion.html">Cómo cambiar el filtro</a></li><li><a href="precio-filtro-agua-nevecon-lg.html">Precios</a></li>'
            '<li><a href="preguntas-frecuentes-filtro-agua-lg.html">Preguntas frecuentes</a></li><li><a href="glosario-filtro-nevera-lg.html">Glosario</a></li><li><a href="mapa-del-sitio.html">Mapa del sitio</a></li>'
            '<li><a href="envio-filtros-lg-colombia.html">Envíos</a></li><li><a href="terminos.php">Términos</a></li><li><a href="privacidad.php">Datos personales</a></li></ul></div></div>'
            '<div class="aq-wrap aq-f-pay"><div><span class="m">Tarjeta</span><span class="m">PSE</span><span class="m">Nequi</span><span class="m">Bancolombia</span><span class="m">Contra entrega</span></div>'
            '<div>© 2026 Filtro de Agua LG Colombia — Distribuidor Autorizado</div></div></footer>'
            f'<a class="aq-wa" href="https://wa.me/{WA}" aria-label="WhatsApp"><svg width="22" height="22" fill="#fff" viewBox="0 0 16 16"><path d="M13.6 2.3A7.85 7.85 0 0 0 8 0C3.6 0 .07 3.56.06 7.93c0 1.4.37 2.76 1.06 3.97L0 16l4.2-1.1a7.93 7.93 0 0 0 3.8.97c4.37 0 7.93-3.56 7.93-7.93a7.9 7.9 0 0 0-2.33-5.64zM8 14.5a6.57 6.57 0 0 1-3.36-.92l-.24-.14-2.5.65.67-2.43-.16-.25A6.56 6.56 0 0 1 1.4 7.93C1.4 4.3 4.36 1.34 8 1.34a6.56 6.56 0 0 1 4.65 1.93 6.5 6.5 0 0 1 1.93 4.66c0 3.63-2.96 6.57-6.58 6.57z"/></svg><span>¿Dudas? Escríbenos</span></a>')


def tarjeta(p, k=None):
    feat = (["Va fuera del nevecón, en la línea de agua", "Se conecta a la manguera del agua"] if p["ubic"] == "externo" else ["Filtro interno para nevecones LG", f"Equivale a {', '.join(p['refs'][1:3])}" if len(p["refs"]) > 1 else "Referencia original"]) + ["Cámbialo cada 6 meses"]
    return (f'<article class="tf-card"><a class="tf-img" href="{p["url"]}" aria-label="Ficha técnica del {esc(p["corto"])}"><img src="{p["img"]}" alt="Filtro de agua {esc(p["h"])} original" width="400" height="300" loading="lazy"></a>'
            f'<div class="tf-b"><h3><a href="{p["url"]}">{esc(p["nombre"])}</a></h3><span class="tf-code">{esc(p["ref"])}</span><ul class="tf-feat">{"".join(f"<li>{esc(x)}</li>" for x in feat)}</ul>'
            f'<div class="tf-pr">{cop(p["precio"])}<small>COP · envío gratis</small></div><button type="button" class="tf-add" data-add="{p["id"]}">🛒 Agregar al carrito</button></div></article>')


def qa(titulo, respuesta):
    return f'<section class="aq-qa-sec"><div class="wrap"><div class="qa"><p class="tag">⚡ Respuesta rápida</p><h2>{esc(titulo)}</h2><p>{respuesta}</p></div></div></section>'


def seccion(h2, cuerpo, alt=False, sub=""):
    return f'<section class="aq-sec{" alt" if alt else ""}"><div class="wrap"><h2>{h2}</h2>' + (f'<p class="sub2">{sub}</p>' if sub else "") + cuerpo + "</div></section>"


def faq_html(preg, h2="Preguntas frecuentes"):
    return ('<section class="aq-sec alt"><div class="wrap"><h2>' + esc(h2) + '</h2><div class="faq-num">'
            + "".join(f'<details{" open" if i == 0 else ""}><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for i, (q, a) in enumerate(preg)) + "</div></div></section>")


def strip_rapida():
    return ('<section class="aq-quick"><div class="wrap"><div class="aq-qgrid">' + "".join(
        f'<div class="aq-q"><a href="{p["url"]}"><img src="{p["img"]}" alt="Filtro {esc(p["corto"])}" width="84" height="84" loading="lazy"></a><div><b>{esc(p["corto"])}</b><small>{esc(p["ref"])}</small><span>{cop(p["precio"])}</span></div>'
        f'<button type="button" data-add="{p["id"]}">🛒 Agregar</button></div>' for p in PS[:3]) + '</div></div></section>')


def ld_base(nombre, titulo, desc, miga):
    url = f"{DOMINIO}/{nombre}" if nombre != "index.html" else f"{DOMINIO}/"
    g = [{"@type": "WebPage", "@id": url, "name": titulo, "url": url, "inLanguage": "es-CO", "description": desc, "dateModified": HOY, "isPartOf": {"@id": f"{DOMINIO}/#tienda"}},
         {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, **({"item": f"{DOMINIO}/{u}"} if u else {})} for i, (n, u) in enumerate(miga)]}]
    return g


def ld_faq(preg):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in preg]}


def ld_producto(p):
    return {"@type": "Product", "name": p["nombre"], "sku": p["ref"], "mpn": p["ref"], "image": f"{DOMINIO}/{p['img']}", "brand": {"@type": "Brand", "name": "LG"}, "category": "Filtros de agua para nevecón",
            "description": f"Filtro de agua {p['nombre']} (código {p['ref']}), equivalente a {', '.join(p['refs'][1:4]) or p['ref']}. Para nevecones LG.",
            "offers": {"@type": "Offer", "url": f"{DOMINIO}/{p['url']}", "priceCurrency": "COP", "price": str(p["precio"]), "availability": "https://schema.org/InStock", "itemCondition": "https://schema.org/NewCondition",
                       "priceValidUntil": "2027-12-31", "seller": {"@id": f"{DOMINIO}/#tienda"}, "hasMerchantReturnPolicy": {"@type": "MerchantReturnPolicy", "applicableCountry": "CO", "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow", "merchantReturnDays": 5},
                       "shippingDetails": {"@type": "OfferShippingDetails", "shippingRate": {"@type": "MonetaryAmount", "value": "0", "currency": "COP"}, "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "CO"}}}}


TIENDA_LD = {"@type": "OnlineStore", "@id": f"{DOMINIO}/#tienda", "name": "Filtro de Agua LG Colombia", "url": f"{DOMINIO}/", "logo": f"{DOMINIO}/img/logo-lg.png", "areaServed": {"@type": "Country", "name": "Colombia"},
             "currenciesAccepted": "COP", "paymentAccepted": "Tarjeta de crédito, tarjeta débito, PSE, Nequi, Bancolombia, contra entrega", "contactPoint": {"@type": "ContactPoint", "telephone": "+57" + WA[2:], "contactType": "customer service", "areaServed": "CO", "availableLanguage": "es"}}


def pagina(nombre, titulo, desc, kw, miga, cuerpo, preguntas=(), ld_extra=(), prio="0.6", og=None, hero=None):
    titulo = titulo.strip()
    url = f"{DOMINIO}/{nombre}" if nombre != "index.html" else f"{DOMINIO}/"
    graf = ld_base(nombre, titulo, desc, miga) + ([ld_faq(list(preguntas))] if preguntas else []) + list(ld_extra)
    if nombre == "index.html":
        graf.append(TIENDA_LD)
    bc = '<div class="breadcrumb wrap" style="font:500 13px Inter,sans-serif;padding:16px 22px 0;">' + " / ".join(f'<a href="{u}">{esc(n)}</a>' if u else esc(n) for n, u in miga) + "</div>" if len(miga) > 1 else ""
    head = ('<!DOCTYPE html><html lang="es-CO"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">'
            f'<title>{esc(titulo)}</title><meta name="description" content="{esc(desc)}"><meta name="keywords" content="{esc(kw)}"><link rel="canonical" href="{url}">'
            '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1"><meta name="theme-color" content="#a50034">'
            + (f'<meta name="google-site-verification" content="{TOKEN}">' if TOKEN else "")
            + f'<meta property="og:type" content="website"><meta property="og:locale" content="es_CO"><meta property="og:site_name" content="Filtro de Agua LG Colombia"><meta property="og:title" content="{esc(titulo)}">'
            f'<meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{DOMINIO}/{og or PS[0]["img"]}">'
            f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(titulo)}"><meta name="twitter:description" content="{esc(desc)}">'
            '<link rel="icon" href="img/icono-lg.png"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">'
            '<link rel="stylesheet" href="tema.css?v=lg1"><link rel="stylesheet" href="pasarela.css">'
            f'<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graf}, ensure_ascii=False)}</script></head><body>')
    t = head + encabezado() + bc + fix(cuerpo) + pie() + '<script src="carrito.js" defer></script><script src="buscar.js" defer></script></body></html>'
    (OUT / nombre).write_text(t, encoding="utf-8")
    PAGINAS.append((nombre, prio, titulo, desc))
    return t


def hero_simple(kicker, h1, sub):
    return f'<section class="hero"><div class="wrap"><span class="kicker">{esc(kicker)}</span><h1>{esc(h1)}</h1><p class="sub" style="margin-top:16px;">{esc(sub)}</p></div></section>'


exec(open(AQUI / "ads_lg_paginas.py", encoding="utf-8").read())
