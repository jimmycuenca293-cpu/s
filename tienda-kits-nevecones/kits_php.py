#!/usr/bin/env python3
"""Tienda de kits de instalación para nevecones, con la MISMA estructura que la tienda de filtros (PHP, carrito, Wompi, pedidos, correos).

Genera una carpeta 'overlay' con los archivos que se suman a public_html:
  kits-instalacion-nevecones/            tienda (toda Colombia)
  kits-instalacion-nevecones-cali/       tienda + instalación en Cali
  filtrosnevecones-api/catalogo-kits.php productos con precio (el servidor cobra de aquí)
  filtrosnevecones-img/k-*.jpg           fotos
Uso: python3 kits_php.py <carpeta_salida>
Precio = (costo + envío + ganancia + comisión fija Wompi) / (1 - % Wompi), igual que la tienda de filtros (envío gratis).
"""
import html, json, math, re, shutil, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

AQUI = Path(__file__).parent
SALIDA = Path(sys.argv[1])
INDEX_TIENDA = Path(sys.argv[2]) if len(sys.argv) > 2 else None
ENVIO = 16000
GAN = {"solo": 15000, "combo": 30000}
WOMPI_PCT, WOMPI_FIJO = 0.0265 * 1.19, 700 * 1.19
esc = lambda s: html.escape(str(s), quote=True)
cop = lambda n: "$ " + f"{int(n):,}".replace(",", ".")
P_ = lambda s: s  # marcador: texto fijo


def precio(costo, tipo):
    raw = (costo + ENVIO + GAN[tipo] + WOMPI_FIJO) / (1 - WOMPI_PCT)
    return int(math.ceil(raw / 1000) * 1000 - 100)  # termina en 900 como la tienda de filtros


# costo de cada pieza (pesos). Filtros externos: $22.500 cada uno según el proveedor de Colombia.
COSTO = {"man14_m": 1500, "man516_m": 2000, "galapago": 15000, "plastica": 20000, "multi": 14000, "acople": 4000,
         "f-sam": 22500, "f-lg": 22500, "f-wp": 22500}

SLUG_BASE = "/kits-instalacion-nevecones"
SLUG_CALI = "/kits-instalacion-nevecones-cali"

# ------------------------------------------------------------------ productos
MET = [5, 10, 15, 20]
PROD = {}   # pid -> dict


def add(pid, **k):
    k["pid"] = pid
    PROD[pid] = k
    return k


for t, q, nom in (("14", "1/4", "man14_m"), ("516", "5/16", "man516_m")):
    for m in MET:
        c = COSTO[nom] * m
        add(f"k-man{t}-{m}", slug=f"manguera-{q.replace('/', '-')}-para-nevecon", grupo=f"man{t}", metros=m, tipo="solo",
            nombre=f'Manguera de {q}" x {m} metros', corto=f'Manguera {q}"', ref=f"MANG-{t}-{m}M", costo=c, precio=precio(c, "solo"),
            foto=f"manguera-{q.replace('/', '-')}-5m")

add("k-galapago", slug="llave-galapago-para-nevecon", tipo="solo", nombre="Llave galápago con racores, anillo y tuerca", corto="Llave galápago", ref="LLAVE-GALAPAGO",
    costo=COSTO["galapago"], precio=precio(COSTO["galapago"], "solo"), foto="llave-galapago")
add("k-plastica", slug="llave-plastica-acople-rapido-para-nevecon", tipo="solo", nombre="Llave plástica con acople rápido", corto="Llave plástica", ref="LLAVE-PLASTICA",
    costo=COSTO["plastica"], precio=precio(COSTO["plastica"], "solo"), foto="llave-plastica")
add("k-multi", slug="llave-multiproposito-para-nevecon", tipo="solo", nombre="Llave multipropósito", corto="Llave multipropósito", ref="LLAVE-MULTI",
    costo=COSTO["multi"], precio=precio(COSTO["multi"], "solo"), foto="llave-multiproposito")
add("k-acople14", slug="acople-rapido-manguera-1-4", tipo="solo", nombre='Acople rápido para manguera de 1/4"', corto='Acople rápido 1/4"', ref="ACOPLE-1-4",
    costo=COSTO["acople"], precio=precio(COSTO["acople"], "solo"), foto="acople-rapido-1-4")
add("k-acople516", slug="acople-rapido-manguera-5-16", tipo="solo", nombre='Acople rápido para manguera de 5/16"', corto='Acople rápido 5/16"', ref="ACOPLE-5-16",
    costo=COSTO["acople"], precio=precio(COSTO["acople"], "solo"), foto="acople-rapido-5-16")

BASE_M = COSTO["man14_m"] * 5
COMBOS = [
    ("k-kit-basico", "kit-basico-manguera-llave-galapago", "Kit básico: manguera 1/4\" 5 m + llave galápago", "Kit básico", "KIT-BASICO",
     [("k-man14-5", 1), ("k-galapago", 1)], BASE_M + COSTO["galapago"]),
    ("k-kit-plastica", "kit-manguera-llave-plastica", "Kit: manguera 1/4\" 5 m + llave plástica", "Kit con llave plástica", "KIT-PLASTICA",
     [("k-man14-5", 1), ("k-plastica", 1)], BASE_M + COSTO["plastica"]),
    ("k-kit-516", "kit-manguera-5-16-llave-galapago", "Kit: manguera 5/16\" 5 m + llave galápago", "Kit manguera 5/16\"", "KIT-5-16",
     [("k-man516-5", 1), ("k-galapago", 1)], COSTO["man516_m"] * 5 + COSTO["galapago"]),
    ("k-kit-multi", "kit-manguera-galapago-multiproposito", "Kit: manguera 1/4\" 5 m + llave galápago + llave multipropósito", "Kit con multipropósito", "KIT-MULTI",
     [("k-man14-5", 1), ("k-galapago", 1), ("k-multi", 1)], BASE_M + COSTO["galapago"] + COSTO["multi"]),
    ("k-kit-acoples", "kit-basico-con-acoples-rapidos", "Kit básico + 2 acoples rápidos de 1/4\"", "Kit con acoples", "KIT-ACOPLES",
     [("k-man14-5", 1), ("k-galapago", 1), ("k-acople14", 2)], BASE_M + COSTO["galapago"] + 2 * COSTO["acople"]),
]
for marca, k, fc, ref in (("Samsung", "sam", "f-sam", "DA29-10105J"), ("LG", "lg", "f-lg", "ADQ73693903"), ("Whirlpool", "wp", "f-wp", "4378411RB")):
    COMBOS.append((f"k-kit-{k}", f"kit-completo-nevecon-{marca.lower()}", f"Kit completo para nevecón {marca}: manguera 5 m + llave galápago + filtro externo {marca}",
                   f"Kit completo {marca}", f"KIT-{k.upper()}", [("k-man14-5", 1), ("k-galapago", 1), (f"f-{k}", 1)], BASE_M + COSTO["galapago"] + COSTO[fc]))

FILTRO_PRECIO = {"f-sam": 81900, "f-lg": 81900, "f-wp": 85900}   # precio de venta en la tienda de filtros (envío gratis)
FILTROS = {"f-sam": ("Samsung", "DA29-10105J", "sam-ex-o", "filtro-samsung-externo-da29-10105j", "Filtro Samsung externo DA29-10105J"),
           "f-lg": ("LG", "ADQ73693903", "lg-ex-o", "filtro-lg-externo-adq73693903", "Filtro LG externo ADQ73693903"),
           "f-wp": ("Whirlpool", "4378411RB", "wp-ex-o", "filtro-whirlpool-externo-4378411rb", "Filtro Whirlpool externo 4378411RB")}
for pid, slug, nom, corto, ref, comp, costo in COMBOS:
    add(pid, slug=slug, tipo="combo", nombre=nom, corto=corto, ref=ref, costo=costo, precio=precio(costo, "combo"), comp=comp, foto=None)

TEXTO = {
    "man14": dict(desc="Manguera blanca de 1/4 de pulgada para llevar el agua desde tu punto de agua, pasando por la llave y el filtro, hasta la entrada del nevecón.",
                  sirve=["Es la manguera con la que se conecta el dispensador de agua y la máquina de hielo del nevecón.",
                         "Se vende por largo: escoge 5, 10, 15 o 20 metros según la distancia entre el punto de agua y el nevecón.",
                         "No la recortes más de lo necesario: si queda corta, el nevecón no llega y toca empalmar con acoples."],
                  ficha=[("Medida", "1/4 de pulgada"), ("Color", "Blanca"), ("Largos disponibles", "5, 10, 15 o 20 metros")],
                  pasos=["Cierra la llave de paso del agua que alimenta el nevecón y desconecta el nevecón de la corriente.",
                         "Mide el recorrido real de la manguera desde el punto de agua hasta el nevecón y deja unos 50 cm extra para poder mover el nevecón sin tensionarla.",
                         "Corta la punta derecha, sin rebabas ni aplastar el tubo (un cortatubos o un bisturí filoso lo hace limpio).",
                         "Empuja la manguera hasta el fondo en el acople rápido o pásala por la tuerca y el anillo de la llave, según tu montaje.",
                         "Abre el agua despacio y revisa que no gotee en ninguna unión durante unos minutos.",
                         "Evita dobleces o aplastamientos: la manguera doblada baja la presión del agua del dispensador."]),
    "man516": dict(desc="Manguera transparente de 5/16 de pulgada, disponible en 5, 10, 15 y 20 metros.",
                   sirve=["Sirve para las conexiones de agua que usan manguera de 5/16 de pulgada.",
                          "Si no estás seguro de la medida de tu conexión, escríbenos por WhatsApp con una foto de la manguera del nevecón y te confirmamos.",
                          "Se vende por largo: escoge 5, 10, 15 o 20 metros."],
                   ficha=[("Medida", "5/16 de pulgada"), ("Color", "Transparente"), ("Largos disponibles", "5, 10, 15 o 20 metros")],
                   pasos=["Cierra el agua y desconecta el nevecón de la corriente.",
                          "Corta la punta derecha y limpia la rebaba.",
                          "Empuja la manguera hasta el fondo en el acople rápido (o pásala por la tuerca y el anillo de la llave) y hala suave para confirmar que quedó firme.",
                          "Abre el agua despacio y revisa que no gotee en ninguna unión."]),
    "galapago": dict(desc="Llave galápago metálica con abrazadera para tomar el agua directamente de un tubo, sin cortarlo. Incluye racores, anillo y tuerca para conectar la manguera.",
                     sirve=["Es la llave que más se usa para conectar un nevecón cuando en el punto de agua no hay una salida libre.",
                            "Se abraza al tubo con dos tornillos y, al ajustarla, su aguja perfora el tubo para sacar el agua sin tener que cortarlo ni soldar.",
                            "Trae los racores, el anillo y la tuerca para conectar la manguera de 1/4 de pulgada."],
                     ficha=[("Tipo", "Llave galápago con abrazadera"), ("Incluye", "Racores, anillo y tuerca"), ("Conexión de salida", "Manguera de 1/4 de pulgada")],
                     pasos=["Cierra el paso general del agua y abre un grifo para sacar el agua que queda en el tubo.",
                            "Limpia el tubo donde va la llave y verifica que sea un tubo derecho y sin soldaduras.",
                            "Pon la abrazadera con el sello de caucho contra el tubo y ajusta los dos tornillos parejo, alternando, hasta que quede firme.",
                            "Con la llave cerrada, gira el volante hasta perforar el tubo (sigue las instrucciones del empaque) y ábrela.",
                            "Pasa la tuerca y el anillo por la manguera, empújala en la salida y aprieta la tuerca sin pasarte.",
                            "Abre el paso general, revisa que no gotee y, si gotea, aprieta un poco más la tuerca o los tornillos."]),
    "plastica": dict(desc="Pieza plástica blanca con tuerca hexagonal y conexión rápida azul para la manguera.",
                     sirve=["Sirve para conectar la manguera de agua del nevecón sin herramientas especiales: la manguera se empuja en la conexión rápida azul y queda sujeta.",
                            "La tuerca hembra se enrosca en la salida del punto de agua. Si tienes duda de si tu salida es compatible, escríbenos por WhatsApp con una foto.",
                            "Es una alternativa más económica a la llave metálica cuando tu punto de agua ya tiene salida con rosca."],
                     ficha=[("Material", "Plástico blanco con conexión rápida azul"), ("Conexión a la manguera", "Rápida (se empuja)"), ("Conexión al punto de agua", "Tuerca hembra hexagonal")],
                     pasos=["Cierra el paso del agua y desconecta el nevecón de la corriente.",
                            "Enrosca la tuerca hembra en la salida del punto de agua con cinta de teflón y apriétala a mano, con un cuarto de vuelta extra.",
                            "Corta la punta de la manguera derecha y empújala hasta el fondo en la conexión rápida azul.",
                            "Hala suave para confirmar que quedó firme. Para soltarla, presiona el anillo azul y saca la manguera.",
                            "Abre el agua despacio y revisa que no gotee."]),
    "multi": dict(desc="Llave multipropósito para tomar y controlar el agua en el punto de conexión del nevecón.",
                  sirve=["Controla el paso del agua hacia la manguera del nevecón, para cerrar el agua cuando cambias el filtro o mueves el nevecón.",
                         "Si no sabes si es la que necesitas, escríbenos por WhatsApp con una foto de tu punto de agua y te decimos cuál usar."],
                  ficha=[("Tipo", "Llave multipropósito")],
                  pasos=["Cierra el paso general del agua.", "Instala la llave en tu punto de agua siguiendo el tipo de conexión de tu instalación (usa cinta de teflón en las roscas).",
                         "Conecta la manguera del nevecón.", "Abre el agua despacio y revisa que no gotee."]),
    "acople14": dict(desc="Acople rápido de unión recta para empalmar manguera de 1/4 de pulgada, sin herramientas.",
                     sirve=["Une dos tramos de manguera de 1/4 de pulgada, por ejemplo cuando necesitas alargar la manguera o cambiar un tramo dañado.",
                            "La manguera se empuja hasta el fondo y queda sujeta. Para soltarla se presiona el anillo azul y se hala."],
                     ficha=[("Medida", "Manguera de 1/4 de pulgada"), ("Tipo", "Unión recta, conexión rápida"), ("Colores", "Cuerpo negro y anillos azules")],
                     pasos=["Cierra el agua.", "Corta las puntas de las mangueras rectas y sin rebabas.", "Empuja cada manguera hasta el fondo en su lado del acople.",
                            "Hala suave para confirmar que quedó firme y abre el agua despacio."]),
    "acople516": dict(desc="Acople rápido de unión recta para empalmar manguera de 5/16 de pulgada, sin herramientas.",
                      sirve=["Une dos tramos de manguera de 5/16 de pulgada, por ejemplo cuando necesitas alargar la manguera o cambiar un tramo dañado.",
                             "La manguera se empuja hasta el fondo y queda sujeta. Para soltarla se presiona el anillo azul y se hala."],
                      ficha=[("Medida", "Manguera de 5/16 de pulgada"), ("Tipo", "Unión recta, conexión rápida"), ("Colores", "Cuerpo negro y anillos azules")],
                      pasos=["Cierra el agua.", "Corta las puntas de las mangueras rectas y sin rebabas.", "Empuja cada manguera hasta el fondo en su lado del acople.",
                             "Hala suave para confirmar que quedó firme y abre el agua despacio."]),
}
TEXTO_DE = {"k-galapago": "galapago", "k-plastica": "plastica", "k-multi": "multi", "k-acople14": "acople14", "k-acople516": "acople516"}

FAQ_COMUN = [
    ("¿Cuánto cuesta el envío?", "Nada. El envío es gratis a toda Colombia y ya está incluido en el precio que ves."),
    ("¿Cómo pago?", "En línea y de forma segura con tarjeta débito o crédito, PSE, Nequi o botón Bancolombia, con Wompi. Recibes el recibo en tu correo."),
    ("¿Cuánto demora en llegar?", "De 2 a 3 días hábiles a las principales ciudades. Te enviamos el número de guía."),
    ("¿No sé cuál necesito, me ayudan?", "Sí. Escríbenos por WhatsApp con una foto de tu punto de agua y de la manguera del nevecón y te decimos qué llevar. También puedes mirar la guía «Cómo conectar el agua de tu nevecón»."),
    ("¿Quién instala el kit?", "Cada producto trae su paso a paso en esta página y la guía «Cómo conectar el agua de tu nevecón». Si tienes dudas, escríbenos por WhatsApp y te guiamos."),
]


def foto_url(p):
    return f"/filtrosnevecones-img/{p['pid']}.jpg"


# ------------------------------------------------------------------ fotos
def mini(im, d, pid):
    t = im.copy(); t.thumbnail((400, 400)); t.save(d / f"{pid}-400.webp", quality=80)


def preparar_fotos(out):
    d = out / "filtrosnevecones-img"
    d.mkdir(parents=True, exist_ok=True)
    src = AQUI / "fotos"
    def cargar(n):
        f = src / f"{n}.jpg"
        return Image.open(f).convert("RGB") if f.exists() else None
    def placeholder(txt):
        im = Image.new("RGB", (640, 640), "#f1f4f8"); dr = ImageDraw.Draw(im)
        try: ft = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34)
        except Exception: ft = ImageFont.load_default()
        w = dr.textlength(txt, font=ft); dr.text(((640 - w) / 2, 300), txt, fill="#5b6679", font=ft); return im
    for p in PROD.values():
        pid = p["pid"]
        if p["tipo"] == "combo":
            ims = []
            for c, _n in p["comp"]:
                if c in FILTROS:
                    f = AQUI.parent / "filtrosnevecones-img-origen" / (FILTROS[c][2] + ".jpg")
                    f2 = AQUI / "fotos" / ("filtro-externo-" + {"f-sam": "samsung", "f-lg": "lg", "f-wp": "whirlpool"}[c] + ".jpg")
                    im = Image.open(f2).convert("RGB") if f2.exists() else None
                else:
                    im = cargar(PROD[c]["foto"]) if PROD[c].get("foto") else None
                if im is not None and not any(im is x for x in ims): ims.append(im)
            lienzo = Image.new("RGB", (900, 600), "white"); n = min(3, len(ims)) or 1; w = 900 // n
            for i, im in enumerate(ims[:3]):
                t = im.copy(); t.thumbnail((w - 20, 560)); lienzo.paste(t, (i * w + (w - t.width) // 2, (600 - t.height) // 2))
            lienzo.save(d / f"{pid}.jpg", quality=84, optimize=True); mini(lienzo, d, pid)
        else:
            im = cargar(p["foto"]) or placeholder("Foto próximamente")
            im.thumbnail((900, 900)); im.save(d / f"{pid}.jpg", quality=84, optimize=True); mini(im, d, pid)


# ------------------------------------------------------------------ PHP
def php_str(s): return "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"


def catalogo_php():
    filas = []
    for p in PROD.values():
        filas.append(f"  {php_str(p['pid'])} => ['nombre' => {php_str(p['nombre'])}, 'ref' => {php_str(p['ref'])}, 'marca' => 'Kits', 'precio' => {p['precio']}, 'pack' => 0, "
                     f"'slug' => {php_str(p['slug'])}, 'ubic' => 'kit', 'url' => {php_str(SLUG_BASE + '/' + p['slug'] + '/')}],")
    return "<?php\n// Generado por kits_php.py. Productos de la tienda de kits: el servidor cobra de aquí.\nreturn [\n" + "\n".join(filas) + "\n];\n"


def head(titulo, desc, ruta, ld):
    return f"<?php require __DIR__ . '/../partes.php';\ncabeza({php_str(titulo)}, {php_str(desc)}, {php_str(ruta)}, '<script type=\"application/ld+json\">' . {php_str(ld)} . '</script>'); ?>\n"


def tarjeta(p, base_cali=False):
    url = SLUG_BASE + "/" + p["slug"] + "/"
    return (f'<div class="card"><a href="{url}" style="text-decoration:none;color:inherit;display:flex;flex-direction:column;gap:6px">'
            f'<span class="im"><img src="{foto_url(p)}" alt="{esc(p["nombre"])}" loading="lazy"></span>'
            f'<span class="m">{"Combo" if p["tipo"] == "combo" else "Por separado"}</span><b>{esc(p["nombre"])}</b>'
            f'<span class="p">{cop(p["precio"])}</span><span class="m">Envío gratis</span></a>'
            f'<button class="btn sm" type="button" data-add="{p["pid"]}">Agregar al carrito</button></div>')


def tarjeta_grupo(grupo):
    vs = [p for p in PROD.values() if p.get("grupo") == grupo]; v0 = vs[0]
    ops = "".join(f'<option value="{v["pid"]}" data-p="{v["precio"]}">{v["metros"]} metros · {cop(v["precio"])}</option>' for v in vs)
    q = '1/4' if grupo == "man14" else '5/16'
    url = SLUG_BASE + "/" + v0["slug"] + "/"
    return (f'<div class="card"><a href="{url}" style="text-decoration:none;color:inherit;display:flex;flex-direction:column;gap:6px">'
            f'<span class="im"><img src="{foto_url(v0)}" alt="Manguera de {q} para nevecón" loading="lazy"></span><span class="m">Por separado · por metros</span>'
            f'<b>Manguera de {q}" para nevecón</b></a><select class="msel" aria-label="Metros de manguera de {q}">{ops}</select>'
            f'<span class="p">{cop(v0["precio"])}</span><span class="m">Envío gratis</span><button class="btn sm" type="button" data-add="{v0["pid"]}">Agregar al carrito</button></div>')


JS_SEL = """<script>
document.querySelectorAll('.card .msel').forEach(function(s){var c=s.closest('.card'),p=c.querySelector('.p'),b=c.querySelector('[data-add]');
function f(n){return '$ '+String(n).replace(/\\B(?=(\\d{3})+(?!\\d))/g,'.')}
s.addEventListener('change',function(){var o=s.options[s.selectedIndex];b.dataset.add=o.value;p.textContent=f(o.dataset.p)})});
</script>"""


def ld_prod(p, desc):
    d = {"@context": "https://schema.org", "@type": "Product", "name": p["nombre"], "sku": p["ref"], "description": desc,
         "image": "__BASE__" + foto_url(p), "brand": {"@type": "Brand", "name": "Kits de instalación para nevecón"},
         "offers": {"@type": "Offer", "priceCurrency": "COP", "price": p["precio"], "availability": "https://schema.org/InStock",
                    "url": "__BASE__" + SLUG_BASE + "/" + p["slug"] + "/"}}
    return json.dumps(d, ensure_ascii=False)


def faq_html(extra=()):
    return "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in list(extra) + FAQ_COMUN)


def pagina_producto(p):
    g = p.get("grupo")
    if p["tipo"] == "combo":
        return pagina_combo(p)
    clave = g or TEXTO_DE[p["pid"]]
    T = TEXTO[clave]
    opciones = ""
    if g:
        vs = [v for v in PROD.values() if v.get("grupo") == g]
        opciones = ('<label style="font-size:14px">Largo de manguera <select id="metros" class="msel" style="width:100%">' +
                    "".join(f'<option value="{v["pid"]}" data-p="{v["precio"]}">{v["metros"]} metros · {cop(v["precio"])}</option>' for v in vs) + "</select></label>")
    desc_meta = f'{p["nombre"]}: {T["desc"]} Envío gratis a toda Colombia. Paga en línea con tarjeta, PSE o Nequi.'
    # el JSON-LD lleva la base del sitio: se arma en PHP
    ld = ld_prod(p, T["desc"])
    cuerpo = (f"<?php require __DIR__ . '/../../partes.php';\n$ld = str_replace('__BASE__', sitio()['base'], {php_str(ld)});\n"
              f"cabeza({php_str(p['nombre'] + ' | Envío gratis a toda Colombia')}, {php_str(desc_meta[:300])}, {php_str(SLUG_BASE + '/' + p['slug'] + '/')}, '<script type=\"application/ld+json\">' . $ld . '</script>'); ?>\n")
    cuerpo += f'''<nav class="miga"><a href="/">Inicio</a> › <a href="{SLUG_BASE}/">Kits de instalación</a> › {esc(p["corto"])}</nav>
<div class="prod">
  <div class="foto"><img src="{foto_url(p)}" alt="{esc(p["nombre"])}" width="640" height="640" fetchpriority="high"></div>
  <div class="caja">
    <h1>{esc(p["nombre"])}</h1>
    <span class="m">Kits de instalación para nevecón · Referencia <span class="ref">{esc(p["ref"])}</span></span>
    <span class="precio" id="precio">{cop(p["precio"])}</span>
    {opciones}
    <ul class="ok"><li><b>Envío gratis</b> a toda Colombia: llega en 2 a 3 días hábiles a las principales ciudades.</li><li><b>Pago seguro en línea</b> con tarjeta, PSE, Nequi o botón Bancolombia.</li><li>Paso a paso de instalación en esta página y asesoría por WhatsApp.</li></ul>
    <div class="compra"><button class="btn block" type="button" id="b-add" data-add="{p["pid"]}">Agregar al carrito</button><button class="btn ghost block" type="button" id="b-ir" data-add="{p["pid"]}" data-ir="1">Comprar ahora</button></div>
    <span class="m">Pago seguro en línea: tarjeta débito o crédito, PSE, Nequi o botón Bancolombia.</span><?= medios_pago_html() ?>
  </div>
</div>
<section class="caja"><h2>Descripción</h2><p>{esc(T["desc"])}</p></section>
<section class="caja"><h2>Para qué sirve</h2>{"".join(f"<p>{esc(x)}</p>" for x in T["sirve"])}</section>
<section class="caja datos"><h2>Ficha técnica y datos rápidos</h2><dl class="dq">{"".join(f"<dt>{esc(a)}</dt><dd>{esc(b)}</dd>" for a, b in T["ficha"])}<dt>Envío</dt><dd>Gratis a toda Colombia, 2 a 3 días hábiles en las principales ciudades</dd><dt>Referencia</dt><dd>{esc(p["ref"])}</dd></dl></section>
<section class="caja tutorial" id="instalacion"><h2>Cómo instalarlo paso a paso</h2><ol class="pasos">{"".join(f"<li>{esc(x)}</li>" for x in T["pasos"])}</ol>
<p class="m">¿Tienes dudas? Escríbenos por WhatsApp y te guiamos. Mira también la guía <a href="{SLUG_BASE}/guia-conexion-agua-nevecon/">Cómo conectar el agua de tu nevecón</a>.</p></section>
<section style="display:flex;flex-direction:column;gap:8px"><h2>Preguntas frecuentes</h2>{faq_html()}</section>
<p class="m"><a href="{SLUG_BASE}/">← Ver todos los productos</a></p>
'''
    if g:
        cuerpo += """<script>
(function(){var s=document.getElementById('metros'),pr=document.getElementById('precio'),a=document.getElementById('b-add'),i=document.getElementById('b-ir');
function f(n){return '$ '+String(n).replace(/\\B(?=(\\d{3})+(?!\\d))/g,'.')}
s.addEventListener('change',function(){var o=s.options[s.selectedIndex];a.dataset.add=o.value;i.dataset.add=o.value;pr.textContent=f(o.dataset.p)})})();
</script>
"""
    cuerpo += "<?php pie(); ?>\n"
    return cuerpo


def pagina_combo(p):
    comps = []
    for c, n in p["comp"]:
        if c in FILTROS:
            marca, ref, _i, slug, nombre = FILTROS[c]
            comps.append((n, nombre, f"/filtrosnevecones-filtro/{slug}/"))
        else:
            q = PROD[c]
            comps.append((n, q["nombre"], SLUG_BASE + "/" + q["slug"] + "/"))
    sirve = "Un solo pedido con todo lo necesario para conectar el agua de tu nevecón, con un solo envío gratis y mejor precio que comprando las piezas por separado."
    desc_meta = f'{p["nombre"]}. {sirve} Envío gratis a toda Colombia.'
    ld = ld_prod(p, sirve)
    sep = sum((PROD[c]["precio"] if c in PROD else FILTRO_PRECIO[c]) * n for c, n in p["comp"])
    ahorro = max(0, sep - p["precio"])
    ahorro_li = (f'<li>Comprado por separado: <b>{cop(sep)}</b>. Con el combo <b>ahorras {cop(ahorro)}</b>.</li>' if ahorro > 0 else "")
    cuerpo = (f"<?php require __DIR__ . '/../../partes.php';\n$ld = str_replace('__BASE__', sitio()['base'], {php_str(ld)});\n"
              f"cabeza({php_str(p['nombre'] + ' | Envío gratis a toda Colombia')}, {php_str(desc_meta[:300])}, {php_str(SLUG_BASE + '/' + p['slug'] + '/')}, '<script type=\"application/ld+json\">' . $ld . '</script>'); ?>\n")
    lista = "".join(f'<li>{n} × <a href="{u}">{esc(nm)}</a></li>' for n, nm, u in comps)
    pasos = ["Cierra el paso general del agua y desconecta el nevecón de la corriente.",
             "Instala la llave en el tubo o en tu punto de agua (guía de la llave en su página).",
             "Conecta la manguera a la llave sin recortarla: si sobra, déjala enrollada detrás del nevecón.",
             "Si el kit trae filtro externo, instálalo en la manguera con la flecha apuntando hacia el nevecón.",
             "Abre el agua despacio, revisa que no gotee y purga unos 4 litros por el dispensador antes de usar el agua."]
    cuerpo += f'''<nav class="miga"><a href="/">Inicio</a> › <a href="{SLUG_BASE}/">Kits de instalación</a> › {esc(p["corto"])}</nav>
<div class="prod">
  <div class="foto"><img src="{foto_url(p)}" alt="{esc(p["nombre"])}" width="900" height="600" fetchpriority="high"></div>
  <div class="caja">
    <h1>{esc(p["nombre"])}</h1>
    <span class="m">Combo · Referencia <span class="ref">{esc(p["ref"])}</span></span>
    <span class="precio">{cop(p["precio"])}</span>
    <ul class="ok"><li><b>Envío gratis</b> a toda Colombia: llega en 2 a 3 días hábiles a las principales ciudades.</li><li>Un solo envío para todo el kit.</li>{ahorro_li}<li><b>Pago seguro en línea</b> con tarjeta, PSE, Nequi o botón Bancolombia.</li></ul>
    <div class="compra"><button class="btn block" type="button" data-add="{p["pid"]}">Agregar al carrito</button><button class="btn ghost block" type="button" data-add="{p["pid"]}" data-ir="1">Comprar ahora</button></div>
    <span class="m">Pago seguro en línea: tarjeta débito o crédito, PSE, Nequi o botón Bancolombia.</span><?= medios_pago_html() ?>
  </div>
</div>
<section class="caja"><h2>Qué incluye</h2><ul class="ok">{lista}</ul><p>{esc(sirve)}</p></section>
<section class="caja tutorial" id="instalacion"><h2>Cómo instalarlo paso a paso</h2><ol class="pasos">{"".join(f"<li>{esc(x)}</li>" for x in pasos)}</ol>
<p class="m">Mira la guía completa: <a href="{SLUG_BASE}/guia-conexion-agua-nevecon/">Cómo conectar el agua de tu nevecón</a>.</p></section>
<section style="display:flex;flex-direction:column;gap:8px"><h2>Preguntas frecuentes</h2>{faq_html()}</section>
<?php pie(); ?>
'''
    return cuerpo


def wa_php(texto):
    return f"<?= h('https://wa.me/57' . substr(preg_replace('/\\D/', '', (string) (cfg()['whatsapp'] ?? '')), -10) . '?text=' . rawurlencode({php_str(texto)})) ?>"


def listado(cali):
    ruta = SLUG_CALI if cali else SLUG_BASE
    ind = []
    vistos = set()
    for p in PROD.values():
        if p["tipo"] != "solo": continue
        if p.get("grupo"):
            if p["grupo"] in vistos: continue
            vistos.add(p["grupo"]); ind.append(tarjeta_grupo(p["grupo"]))
        else: ind.append(tarjeta(p))
    com = [tarjeta(p) for p in PROD.values() if p["tipo"] == "combo"]
    titulo = "Kits de instalación para nevecón en Cali, con instalación" if cali else "Kits de instalación para nevecón | Envío gratis a toda Colombia"
    desc = ("Compra kits de instalación para tu nevecón y pide la instalación en Cali: manguera, llaves, acoples y filtros externos. Envío gratis." if cali else
            "Manguera de 1/4, llaves galápago, acoples rápidos y filtros externos para conectar el agua de tu nevecón. Por separado o en combo, con envío gratis a toda Colombia y pago en línea.")
    ld = json.dumps({"@context": "https://schema.org", "@type": "ItemList", "name": "Kits de instalación para nevecón",
                     "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": p["nombre"], "url": "__BASE__" + SLUG_BASE + "/" + p["slug"] + "/"} for i, p in enumerate(PROD.values())]}, ensure_ascii=False)
    h = (f"<?php require __DIR__ . '/../partes.php';\n$ld = str_replace('__BASE__', sitio()['base'], {php_str(ld)});\n"
         f"cabeza({php_str(titulo)}, {php_str(desc)}, {php_str(ruta + '/')}, '<script type=\"application/ld+json\">' . $ld . '</script>'); ?>\n")
    h += f'<nav class="miga"><a href="/">Inicio</a> › Kits de instalación{" en Cali" if cali else ""}</nav>\n'
    if cali:
        h += f'''<h1>Kits de instalación para nevecón en Cali</h1>
<p>Compra el kit con envío gratis y, si estás en <b>Cali</b>, pide también que instalemos tu nevecón: bajamos y montamos las puertas, lo ubicamos y nivelamos, lo conectamos al punto de agua, cambiamos el filtro y purgamos el agua.</p>
<div class="caja"><b>Instalación de nevecones en Cali</b><span class="m">El servicio de instalación solo está disponible en Cali y se agenda por WhatsApp. Para el resto de Colombia, mira los <a href="{SLUG_BASE}/">kits con envío gratis</a>.</span>
<a class="btn" href="{wa_php("Hola, quiero la instalación de mi nevecón en Cali")}" target="_blank" rel="noopener">Agendar instalación por WhatsApp</a></div>
'''
    else:
        h += '''<h1>Kits de instalación para nevecón</h1>
<p>Todo para conectar el agua de tu nevecón: <b>manguera de 1/4"</b> (5, 10, 15 o 20 metros), <b>llaves</b>, <b>acoples rápidos</b> y <b>filtros externos</b>. Cada pieza por separado o en combo. <b>Envío gratis</b> a toda Colombia y pago seguro en línea.</p>
'''
    h += f'<p class="m">¿No sabes qué necesitas? Lee la guía <a href="{SLUG_BASE}/guia-conexion-agua-nevecon/">Cómo conectar el agua de tu nevecón</a>. ¿Vives en Cali? <a href="{SLUG_CALI}/">Mira la versión con instalación</a>.</p>\n' if not cali else ""
    h += f'<h2>Combos</h2><div class="grid">{"".join(com)}</div>\n<h2>Por separado</h2><div class="grid">{"".join(ind)}</div>\n'
    h += f'<section style="display:flex;flex-direction:column;gap:8px"><h2>Preguntas frecuentes</h2>{faq_html()}</section>\n{JS_SEL}\n<?php pie(); ?>\n'
    return h


def css_tienda():
    t = INDEX_TIENDA.read_text(encoding="utf-8")
    return "".join(f"<style>{b}</style>\n" for b in re.findall(r"<style>(.*?)</style>", t, re.S))


CATS = [("top", "Más pedidos", ""), ("combos", "Combos", "#1f4fd1"), ("mangueras", "Mangueras", "#c4004f"), ("llaves", "Llaves", "#7b3fa8"), ("acoples", "Acoples", "#1d5fae")]
CAT_DE = {"man14": "mangueras", "man516": "mangueras", "k-galapago": "llaves", "k-plastica": "llaves", "k-multi": "llaves", "k-acople14": "acoples", "k-acople516": "acoples"}
POPULARES = ["k-kit-basico", "k-kit-sam", "k-kit-lg", "k-galapago", "man14", "k-kit-wp", "k-acople14", "k-plastica"]


def datos_js():
    items, vistos = [], set()
    for p in PROD.values():
        if p.get("grupo"):
            if p["grupo"] in vistos: continue
            vistos.add(p["grupo"]); vs = [v for v in PROD.values() if v.get("grupo") == p["grupo"]]
            q = "1/4" if p["grupo"] == "man14" else "5/16"
            items.append({"id": p["grupo"], "cat": "mangueras", "nombre": f'Manguera de {q}" para nevecón', "marca": "Manguera · por metros", "ref": f"{q} de pulgada · 5, 10, 15 o 20 m",
                          "foto": foto_url(p), "url": SLUG_BASE + "/" + p["slug"] + "/", "vars": [{"pid": v["pid"], "m": v["metros"], "precio": v["precio"]} for v in vs],
                          "kw": f"manguera tubo agua {q} metros"})
        else:
            cat = "combos" if p["tipo"] == "combo" else CAT_DE[p["pid"]]
            items.append({"id": p["pid"], "cat": cat, "nombre": p["nombre"], "marca": "Combo" if p["tipo"] == "combo" else {"llaves": "Llave", "acoples": "Acople rápido"}[cat],
                          "ref": p["ref"], "foto": foto_url(p), "url": SLUG_BASE + "/" + p["slug"] + "/", "precio": p["precio"], "pid": p["pid"],
                          "kw": p["nombre"] + " " + p["corto"]})
    return items


def portada(cali):
    ruta = (SLUG_CALI if cali else SLUG_BASE) + "/"
    titulo = ("Kits de instalación para nevecón en Cali, con instalación | Envío gratis" if cali else "Kits de instalación para nevecón: manguera, llaves y filtros | Envío gratis a toda Colombia")
    desc = ("Compra kits de instalación para tu nevecón y agenda la instalación en Cali: manguera de 1/4, llaves, acoples y filtros externos Samsung, LG y Whirlpool. Envío gratis y pago en línea." if cali else
            "Manguera de 1/4 y 5/16 por metros, llaves galápago, acoples rápidos y filtros externos para conectar el agua de tu nevecón. Combos con envío gratis a toda Colombia. Paga con tarjeta, PSE o Nequi.")
    ld = json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "name": "Kits de instalación para nevecón", "url": "__BASE__" + ruta, "inLanguage": "es-CO"},
        {"@type": "ItemList", "name": "Kits de instalación para nevecón", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": p["nombre"], "url": "__BASE__" + SLUG_BASE + "/" + p["slug"] + "/"} for i, p in enumerate(PROD.values())]}]}, ensure_ascii=False)
    chips = "".join(f'<button type="button" data-q="{esc(q)}">{esc(q)}</button>' for q in ("galápago", "manguera 1/4", "kit Samsung", "kit LG", "acople"))
    banner = ""
    if cali:
        banner = (f'<div class="note info"><b>Instalación de nevecones en Cali.</b> Bajamos y montamos las puertas, ubicamos y nivelamos el nevecón, lo conectamos al punto de agua, cambiamos el filtro y purgamos. '
                  f'Se agenda por WhatsApp. <a class="btn wa" style="margin-top:8px" href="{wa_php("Hola, quiero la instalación de mi nevecón en Cali")}" target="_blank" rel="noopener">Agendar instalación por WhatsApp</a></div>')
    h1 = "Kits de instalación para tu nevecón en Cali" if cali else "Kits de instalación para nevecón, con envío gratis a toda Colombia"
    lead = ("Compra el kit con envío gratis y, si estás en Cali, pide que instalemos tu nevecón. Manguera de 1/4\", llaves, acoples y filtros externos Samsung, LG y Whirlpool." if cali else
            "Manguera de 1/4\" y 5/16\" por metros, llaves, acoples rápidos y filtros externos. Cada pieza por separado o en combo, pago seguro en línea y te llega en 2 a 3 días hábiles.")
    faq = faq_html()
    otra = ""
    return f"""<?php require __DIR__ . '/../partes.php'; $S = sitio(); $n = $S['negocio'];
$ld = str_replace('__BASE__', $S['base'], {php_str(ld)}); ?>
<!doctype html>
<html lang="es-CO">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(titulo)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="<?= h($S['base']) ?>{ruta}">
<meta property="og:type" content="website"><meta property="og:title" content="{esc(titulo)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="<?= h($S['base']) ?>{ruta}"><meta property="og:image" content="<?= h($S['base']) ?>/filtrosnevecones-img/compartir.jpg"><meta property="og:locale" content="es_CO"><meta property="og:site_name" content="<?= h($n['nombre']) ?>">
<link rel="manifest" href="/manifest.webmanifest"><link rel="apple-touch-icon" href="/filtrosnevecones-img/apple-touch-icon.png">
<meta name="theme-color" content="#0b1f6b"><link rel="icon" href="/filtrosnevecones-img/icono.svg" type="image/svg+xml">
<?= verificacion_html() . analytics_html() ?>
<script>window.FY_WA = <?= json_encode((strlen($w = preg_replace('/\\D/', '', (string) (cfg()['whatsapp'] ?? ''))) === 10 ? '57' : '') . $w) ?>;</script>
<script type="application/ld+json"><?= json_encode(json_decode($ld), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_HEX_TAG) ?></script>
<script src="/filtrosnevecones-carrito.js" defer></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Manrope:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500&display=swap">
{css_tienda()}</head>
<body>
<?= gtm_body_html() . anuncio_html() ?>
<header class="hero">
  <div class="wrap">
    <div class="top">
      <a class="logo" href="/" style="color:inherit;text-decoration:none"><svg viewBox="0 0 24 24" aria-hidden="true"><rect width="24" height="24" rx="6" fill="#1236a8"/><path d="M12 3.5C9.3 7.1 6.6 9.9 6.6 13.4a5.4 5.4 0 0 0 10.8 0c0-3.5-2.7-6.3-5.4-9.9z" fill="#38d6ff"/><path d="M12 11.2v4.8M9.9 12.4l4.2 2.4M14.1 12.4l-4.2 2.4" stroke="#0b1f6b" stroke-width="1.15" stroke-linecap="round" fill="none"/></svg><span class="lg-t">Filtros<b>Nevecones</b><small>Colombia</small></span></a>
      <nav class="hero-nav"><a href="/filtrosnevecones-tienda/">Filtros</a><a href="{SLUG_BASE}/">Kits</a><a href="{SLUG_BASE}/guia-conexion-agua-nevecon/">Guía</a></nav>
      <a class="cart-top" href="/carrito.php" aria-label="Ver carrito"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 4h2l2.2 10.5a1.5 1.5 0 0 0 1.5 1.2h8.6a1.5 1.5 0 0 0 1.5-1.1L21 8H6.2"/><circle cx="9.5" cy="19.5" r="1.4"/><circle cx="17" cy="19.5" r="1.4"/></svg><span data-cart-n hidden></span></a>
    </div>
    <h1>{esc(h1)}</h1>
    <p class="lead">{esc(lead)}</p>
    <form class="searchbox" id="search-form" role="search">
      <input id="q" type="search" placeholder="Busca: galápago, manguera, kit Samsung…" autocomplete="off" aria-label="Buscar un producto">
      <button type="submit">Buscar</button>
    </form>
    <div class="chips" id="chips" aria-label="Búsquedas frecuentes">{chips}</div>
  </div>
</header>
<main class="wrap">
<section id="v-buscar" style="display:flex;flex-direction:column;gap:20px">
  <div class="trust"><div><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 7h11v9H3zM14 10h4l3 3v3h-7"/><circle cx="7" cy="18" r="1.6"/><circle cx="17" cy="18" r="1.6"/></svg><b>Envío gratis</b>A toda Colombia, 2 a 3 días hábiles</div><div><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/></svg><b>Pago seguro</b>Tarjeta, PSE, Nequi o Bancolombia en línea</div><div><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20l1.2-4A8 8 0 1 1 8 18.8z"/></svg><b>Asesor por WhatsApp</b>Te ayudamos a escoger el tuyo</div></div>
  {banner}
  <span id="catalogo"></span><h2 id="list-title" class="cat-title">Más pedidos</h2>
  <div class="brandbar" id="brandbar"><div class="brands" id="brands" role="tablist" aria-label="Categorías"></div></div>
  <div class="cat-meta"><p class="sub" id="list-sub"></p></div>
  <div class="grid" id="grid"></div>
  <section class="explora" aria-label="Explora la tienda"><h2 style="font-size:19px">Explora la tienda</h2><div class="ex-grid">
<a href="{SLUG_BASE}/guia-conexion-agua-nevecon/"><b>🔧 Cómo conectar el agua</b><span>Qué necesitas y paso a paso</span></a>
<a href="/filtrosnevecones-tienda/"><b>💧 Filtros de agua</b><span>Todos los filtros con envío gratis</span></a>
{otra}
<a href="/filtrosnevecones-instalacion/"><b>🧰 Cómo instalar tu filtro</b><span>Paso a paso para cada referencia</span></a>
</div></section>
  <section class="pasos3" aria-label="Cómo comprar"><h2 style="font-size:19px">Compra en 3 pasos</h2><div class="p3-grid">
<div><span>1</span><b>Escoge tu kit</b><p>Combos listos o piezas por separado: manguera por metros, llave, acoples y filtro externo de tu marca.</p></div>
<div><span>2</span><b>Paga seguro en línea</b><p>Tarjeta débito o crédito, PSE, Nequi o botón Bancolombia, en página de pago segura.</p></div>
<div><span>3</span><b>Recíbelo en tu casa</b><p>Envío gratis a toda Colombia en 2 a 3 días hábiles. Lo instalas con nuestro paso a paso.</p></div>
</div></section>
  <section style="display:flex;flex-direction:column;gap:8px"><h2 style="font-size:19px">Preguntas frecuentes</h2><div class="faqs">{faq.replace("<details>", '<details class="faq">')}</div></section>
  <section class="explora" aria-label="Información"><h2 style="font-size:19px">Información</h2><div class="ex-grid">
<a href="/terminos.php"><b>📄 Términos y condiciones</b><span>Compras, precios y entregas</span></a>
<a href="/privacidad.php"><b>🔒 Tratamiento de datos</b><span>Cómo cuidamos tu información</span></a>
<a href="/garantia-y-retracto.php"><b>↩️ Garantía y retracto</b><span>Garantía legal y 5 días de retracto</span></a>
</div></section>
</section>
</main>
<nav class="tabs bnav" role="tablist" aria-label="Secciones" style="grid-template-columns:repeat(3,1fr)">
  <button role="tab" aria-selected="true" type="button" onclick="scrollTo({{top:0,behavior:'smooth'}})"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5"/></svg>Buscar</button>
  <button role="tab" aria-selected="false" type="button" onclick="location.href='/filtrosnevecones-tienda/'"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3.5C9.3 7.1 6.6 9.9 6.6 13.4a5.4 5.4 0 0 0 10.8 0c0-3.5-2.7-6.3-5.4-9.9z"/></svg>Filtros</button>
  <button role="tab" aria-selected="false" type="button" onclick="location.href='/carrito.php'"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 4h2l2.2 10.5a1.5 1.5 0 0 0 1.5 1.2h8.6a1.5 1.5 0 0 0 1.5-1.1L21 8H6.2"/><circle cx="9.5" cy="19.5" r="1.4"/><circle cx="17" cy="19.5" r="1.4"/></svg>Carrito</button>
</nav>
<a class="wa-flot" id="wa-flot" href="#" target="_blank" rel="noopener" aria-label="Escríbenos por WhatsApp"><svg viewBox="0 0 32 32" aria-hidden="true"><path fill="currentColor" d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 23.6c-2 0-4-.6-5.7-1.6l-.4-.2-3.9 1 1-3.8-.3-.4A10.6 10.6 0 1 1 16 26.6zm5.8-7.9c-.3-.2-1.9-.9-2.2-1-.3-.1-.5-.2-.7.2l-1 1.2c-.2.2-.4.2-.7.1a8.7 8.7 0 0 1-4.3-3.8c-.3-.6.3-.5 1-1.7.1-.2 0-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.1-1.2 2.8s1.2 3.2 1.4 3.5c.2.2 2.4 3.7 5.8 5.1 2.2.9 3 1 4.1.8.7-.1 1.9-.8 2.2-1.5.3-.8.3-1.4.2-1.5-.1-.2-.3-.3-.6-.4z"/></svg><span>Asesor</span></a>
<?= pie_html() ?>
<script>
const DATA = {json.dumps(datos_js(), ensure_ascii=False)};
const CATS = {json.dumps([[a, b, c] for a, b, c in CATS], ensure_ascii=False)};
const POP = {json.dumps(POPULARES)};
const CALI = {"true" if cali else "false"};
const $ = s => document.querySelector(s), esc = s => String(s).replace(/[&<>"]/g, c => ({{"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}}[c]));
const COP = n => "$ " + String(n).replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, ".");
const norm = s => String(s).normalize("NFD").replace(/[\\u0300-\\u036f]/g, "").toLowerCase();
const WA = (window.FY_WA || "573013810242");
$("#wa-flot").href = "https://wa.me/" + WA + "?text=" + encodeURIComponent("Hola, necesito ayuda con un kit de instalación para mi nevecón");
const ICON = {{truck: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 7h11v9H3zM14 10h4l3 3v3h-7"/><circle cx="7" cy="18" r="1.6"/><circle cx="17" cy="18" r="1.6"/></svg>',
  share: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="6" cy="12" r="2.4"/><circle cx="18" cy="6" r="2.4"/><circle cx="18" cy="18" r="2.4"/><path d="M8.2 10.9l7.6-3.8M8.2 13.1l7.6 3.8"/></svg>'}};
let cat = "top";
function precioDe(p) {{ return p.vars ? p.vars[0].precio : p.precio; }}
function card(p) {{
  const pid = p.vars ? p.vars[0].pid : p.pid;
  const sel = p.vars ? `<select class="msel" aria-label="Metros de manguera" style="width:100%;border:1px solid var(--line);border-radius:10px;padding:8px;background:var(--bg)">${{p.vars.map(v => `<option value="${{v.pid}}" data-p="${{v.precio}}">${{v.m}} metros · ${{COP(v.precio)}}</option>`).join("")}}</select>` : "";
  const txt = `${{p.nombre}} por ${{COP(precioDe(p))}} con envío gratis: ${{location.origin}}${{p.url}}`;
  return `<article class="card rise" data-id="${{p.id}}">
    <a class="pbig" href="${{p.url}}" aria-label="Ver ${{esc(p.nombre)}}" style="text-decoration:none"><img src="${{p.foto}}" alt="${{esc(p.nombre)}}" loading="lazy"></a>
    <div class="cinfo"><span class="brand">${{esc(p.marca)}}</span><h3><a href="${{p.url}}" style="color:inherit;text-decoration:none">${{esc(p.nombre)}}</a></h3><span class="ref">${{esc(p.ref)}}</span></div>
    ${{sel}}
    <div><div class="price">${{COP(precioDe(p))}}</div><div class="eta">${{ICON.truck}}<span>Envío gratis · 2 a 3 días hábiles</span></div></div>
    <div class="actions"><button class="btn" type="button" data-add="${{pid}}" data-ir="1" style="flex:1">Pedir</button><a class="icon-btn" href="https://wa.me/?text=${{encodeURIComponent(txt)}}" target="_blank" rel="noopener" aria-label="Compartir">${{ICON.share}}</a></div>
  </article>`;
}}
function brands() {{
  $("#brands").innerHTML = CATS.map(([k, t, c]) => {{
    const n = k === "top" ? 0 : DATA.filter(p => p.cat === k).length;
    return `<button type="button" role="tab" data-cat="${{k}}" aria-selected="${{k === cat}}"${{c ? ` style="--c:${{c}}"` : ""}}>${{c ? "<i></i>" : ""}}${{esc(t)}}${{n ? `<small>${{n}}</small>` : ""}}</button>`;
  }}).join("");
}}
function pintar(list, titulo, sub) {{
  brands();
  $("#list-title").textContent = titulo; $("#list-sub").textContent = sub || ""; $("#list-sub").hidden = !sub;
  $("#grid").innerHTML = list.length ? list.map(card).join("") : `<div class="check"><b>No encontramos ese producto.</b><span class="sub">Escríbenos por WhatsApp y te ayudamos a escoger.</span><a class="btn wa" href="https://wa.me/${{WA}}?text=${{encodeURIComponent("Hola, busco un producto para instalar mi nevecón")}}" target="_blank" rel="noopener">Escríbenos</a></div>`;
}}
function ver() {{
  if (cat === "top") return pintar(POP.map(id => DATA.find(p => p.id === id)).filter(Boolean), "Más pedidos", "Combos y piezas que más se compran. Envío gratis a toda Colombia.");
  const t = CATS.find(c => c[0] === cat)[1];
  pintar(DATA.filter(p => p.cat === cat), t, "");
}}
document.addEventListener("click", e => {{
  const b = e.target.closest("[data-cat]"); if (b) {{ cat = b.dataset.cat; $("#q").value = ""; ver(); b.scrollIntoView({{behavior: "smooth", block: "nearest", inline: "center"}}); return; }}
  const c = e.target.closest("#chips [data-q]"); if (c) {{ $("#q").value = c.dataset.q; buscar(c.dataset.q); }}
}});
document.addEventListener("change", e => {{
  const s = e.target.closest(".msel"); if (!s) return;
  const c = s.closest(".card"), o = s.options[s.selectedIndex];
  c.querySelector(".price").textContent = COP(o.dataset.p); c.querySelector("[data-add]").dataset.add = o.value;
}});
function buscar(q) {{
  q = norm(q).trim(); if (!q) return ver();
  const ws = q.split(/\\s+/);
  const hits = DATA.filter(p => {{ const t = norm(p.nombre + " " + p.kw + " " + p.ref + " " + p.marca); return ws.every(w => t.includes(w)); }});
  pintar(hits, hits.length ? `Resultados para “${{q}}”` : `Sin resultados para “${{q}}”`, hits.length ? "" : "Prueba con otra palabra, por ejemplo galápago, manguera o kit.");
}}
$("#search-form").addEventListener("submit", e => {{ e.preventDefault(); buscar($("#q").value); $("#list-title").scrollIntoView({{behavior: "smooth", block: "start"}}); }});
$("#q").addEventListener("input", e => {{ if (!e.target.value.trim()) ver(); }});
ver();
</script>
</body>
</html>
"""


def guia():
    desc = "Qué necesitas para conectar el agua de tu nevecón: manguera de 1/4, llave galápago o plástica, acoples, filtro externo y paso a paso con purga."
    ld = json.dumps({"@context": "https://schema.org", "@type": "HowTo", "name": "Cómo conectar el agua de tu nevecón",
                     "step": [{"@type": "HowToStep", "text": t} for t in [
                         "Cierra el agua y desconecta el nevecón.", "Instala la llave en el punto de agua.", "Conecta la manguera de 1/4 de pulgada sin recortarla.",
                         "Instala el filtro externo con la flecha hacia el nevecón.", "Abre el agua, revisa fugas y purga unos 4 litros."]]}, ensure_ascii=False)
    r = SLUG_BASE + "/guia-conexion-agua-nevecon/"
    h = (f"<?php require __DIR__ . '/../../partes.php';\n"
         f"cabeza('Cómo conectar el agua de tu nevecón: qué necesitas y paso a paso', {php_str(desc)}, {php_str(r)}, '<script type=\"application/ld+json\">' . {php_str(ld)} . '</script>'); ?>\n")
    h += f'''<nav class="miga"><a href="/">Inicio</a> › <a href="{SLUG_BASE}/">Kits de instalación</a> › Guía de conexión</nav>
<h1>Cómo conectar el agua de tu nevecón</h1>
<p>El dispensador de agua y la máquina de hielo de un nevecón se alimentan con una <b>manguera de 1/4 de pulgada</b> que va desde tu punto de agua hasta la parte de atrás del equipo. Aquí te explicamos qué necesitas y cómo se instala.</p>
<section class="caja"><h2>¿Qué necesito?</h2>
<ul class="ok"><li><b>Manguera de 1/4":</b> de 5, 10, 15 o 20 metros según la distancia. Mide el recorrido y no la recortes de más.</li>
<li><b>Una llave</b> para tomar el agua: la <a href="{SLUG_BASE}/llave-galapago-para-nevecon/">llave galápago</a> si tomas el agua de un tubo sin salida libre; la <a href="{SLUG_BASE}/llave-plastica-acople-rapido-para-nevecon/">llave plástica</a> si tu punto ya tiene salida con rosca.</li>
<li><b>Acoples rápidos</b> para empalmar mangueras o conectar el filtro.</li>
<li><b>Filtro externo</b> (opcional, recomendado): mejora el sabor del agua y del hielo y protege la válvula del nevecón.</li></ul></section>
<section class="caja"><h2>Qué llave necesito según mi punto de agua</h2>
<dl class="dq"><dt>Tubo sin salida libre</dt><dd>Llave galápago (se abraza al tubo y toma el agua sin cortarlo).</dd>
<dt>Salida con rosca disponible</dt><dd>Llave plástica con acople rápido, o llave multipropósito.</dd>
<dt>Necesito más largo</dt><dd>Manguera de 10, 15 o 20 metros, o un acople rápido para empalmar.</dd>
<dt>Quiero agua filtrada</dt><dd>Filtro externo de tu marca (Samsung, LG o Whirlpool), con la flecha hacia el nevecón.</dd></dl>
<p class="m">¿No estás seguro? Escríbenos por WhatsApp con una foto de tu punto de agua.</p></section>
<section class="caja tutorial"><h2>Paso a paso</h2><ol class="pasos">
<li>Cierra el paso general del agua y desconecta el nevecón de la corriente.</li>
<li>Instala la llave en el punto de agua (la guía de cada llave está en su página).</li>
<li>Mide el recorrido y deja unos 50 cm extra de manguera para poder mover el nevecón. Corta la punta derecha y sin rebabas.</li>
<li>Conecta la manguera a la llave y, por el otro extremo, a la entrada de agua del nevecón. Empuja hasta el fondo y hala suave para confirmar.</li>
<li>Si usas filtro externo, instálalo en la manguera con la flecha apuntando hacia el nevecón.</li>
<li>Abre el agua despacio y revisa que no gotee. Después conecta el nevecón y saca unos 4 litros de agua por el dispensador para purgar el aire.</li>
<li>Si el agua sale con poca presión, revisa que la manguera no esté doblada. Si la presión del punto de agua es muy baja, puede hacer falta una bomba propulsora.</li></ol></section>
<section style="display:flex;flex-direction:column;gap:8px"><h2>Preguntas frecuentes</h2>{faq_html()}</section>
<p><a class="btn" href="{SLUG_BASE}/">Ver kits y productos</a></p>
<?php pie(); ?>
'''
    return h


def main():
    out = SALIDA
    if out.exists(): shutil.rmtree(out)
    (out / "filtrosnevecones-api").mkdir(parents=True)
    preparar_fotos(out)
    (out / "filtrosnevecones-api" / "catalogo-kits.php").write_text(catalogo_php(), "utf-8")
    for carpeta, cali in (("kits-instalacion-nevecones", False),):
        d = out / carpeta; d.mkdir(parents=True)
        (d / "index.php").write_text(portada(cali) if INDEX_TIENDA else listado(cali), "utf-8")
    base = out / "kits-instalacion-nevecones"
    vistos = set()
    for p in PROD.values():
        if p["slug"] in vistos: continue
        vistos.add(p["slug"])
        d = base / p["slug"]; d.mkdir(); (d / "index.php").write_text(pagina_producto(p), "utf-8")
    d = base / "guia-conexion-agua-nevecon"; d.mkdir(); (d / "index.php").write_text(guia(), "utf-8")
    print(len(PROD), "productos;", sum(1 for _ in out.rglob("*.php")), "archivos php")
    for p in PROD.values():
        if p["tipo"] == "combo" or p.get("metros") in (None, 5): print(f"  {p['pid']:16s} {p['precio']:>7}  {p['nombre'][:60]}")


main()
