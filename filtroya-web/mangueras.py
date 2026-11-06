#!/usr/bin/env python3
"""Tienda de mangueras para lavadoras (todas las marcas): entrada de agua fría y caliente, entrada negra con rosca, desagüe y tina-bomba, con envío a toda Colombia.

Misma arquitectura que la tienda de filtros de pelusas (lavadoras.py), pero SIN marcas: una sola tienda para todas las lavadoras,
un solo asesor por WhatsApp, sin carrito ni pago en línea (pago contra entrega).
Genera sitios-mangueras/tienda/ y tienda-mangueras.zip.

Uso:  python3 mangueras.py [https://filtrosparalavadoras.click]   (por defecto ese dominio, en la carpeta /mangueras-para-lavadora/)

Fotos: imagenes-mangueras/todas/ (una por manguera, nombre en MARCAS[...]["productos"][...]["foto"]). Si falta una foto se genera una imagen
provisional con el texto «Foto próximamente» para que el sitio compile; reemplázala por la real y vuelve a generar.
Precios y referencias: llena "precio" (pesos) y "ref" en PRODUCTOS. Mientras no haya precio, la página manda al asesor por WhatsApp.
"""
import json, re, shutil, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

import lavadoras as L
from lavadoras import (esc, cop, slug, wa_link, faq_ld, faq_html, chips, foto_html, Sitio, php_val, ciudades,
                       LAV_PHP, CSS_EXTRA, SITEMAP_PHP, FUENTES, AQUI)

PREF = "/mangueras-para-lavadora"      # carpeta de esta tienda dentro del dominio: no pisa nada de la tienda de filtros
GTM = "GTM-5SCP73SQ"                                                  # el mismo de la tienda de filtros
VERIFICACION = "NsQML6RHpDIy79HzjoToyz_eOmWi97jh9G1I1ZwkUM4"          # Search Console de filtrosparalavadoras.click
SALIDA = AQUI / "sitios-mangueras"
FOTOS = AQUI / "imagenes-mangueras"
L.FOTOS = FOTOS

# ---------------------------------------------------------------- datos
WHATSAPP = "3054796329"        # CAMBIA AQUÍ el número del asesor (10 dígitos, sin 57)
TELEFONO = "305 479 6329"
MARCAS = {"todas": {
    "nombre": "Mangueras para lavadora", "clase": "samsung", "tema": "#0b3a75", "whatsapp": WHATSAPP, "telefono": TELEFONO,
    "tienda": "Mangueras para lavadora", "logo": "", "oficial": ("Superintendencia de Industria y Comercio", "https://www.sic.gov.co/"),
    "codigos": "5E, SE, OE o UE", "familias": [],
    "productos": [
        {"id": "man-1", "foto": "manguera-1.png", "slug": "manguera-entrada-agua-fria-azul-lavadora", "corto": "Manguera de entrada de agua fría (azul)", "ref": None, "precio": None, "cat": "entrada",
         "tipo": "Agua fría · tuerca azul", "carga": None, "forma": "manguera de entrada de agua blanca y flexible con una tuerca plástica azul de agarre fácil: la azul es para el agua fría"},
        {"id": "man-2", "foto": "manguera-2.png", "slug": "manguera-entrada-agua-caliente-naranja-lavadora", "corto": "Manguera de entrada de agua caliente (naranja)", "ref": None, "precio": None, "cat": "entrada",
         "tipo": "Agua caliente · tuerca naranja", "carga": None, "forma": "manguera de entrada de agua blanca y reforzada con tuercas plásticas de color naranja: la naranja es para el agua caliente"},
        {"id": "man-3", "foto": "manguera-3.png", "slug": "manguera-entrada-negra-con-rosca-lavadora-carga-frontal", "corto": "Manguera de entrada negra con rosca", "ref": None, "precio": None, "cat": "entrada",
         "tipo": "Negra con rosca · carga frontal", "carga": "carga-frontal", "forma": "manguera de entrada de agua negra de caucho, más fina, con tuercas metálicas con rosca en ambos extremos, la que usan las lavadoras de carga frontal"},
        {"id": "man-4", "foto": "manguera-4.png", "slug": "manguera-desague-corrugada-con-codo-lavadora", "corto": "Manguera de desagüe corrugada con codo", "ref": None, "precio": None, "cat": "desague",
         "tipo": "Corrugada con codo", "carga": None, "forma": "manguera de desagüe gris, corrugada y flexible, con un extremo en codo para colgarla del desagüe y un seguro para sujetarla"},
        {"id": "man-5", "foto": "manguera-5.png", "slug": "manguera-desague-larga-con-extension-lavadora", "corto": "Manguera de desagüe larga con extensión", "ref": None, "precio": None, "cat": "desague",
         "tipo": "Larga, con extensión · carga frontal", "carga": "carga-frontal", "forma": "manguera de desagüe gris corrugada y larga, con una extensión de plástico en la punta para alcanzar desagües lejanos"},
        {"id": "man-6", "foto": "manguera-6.png", "slug": "manguera-desague-con-funda-protectora-lavadora", "corto": "Manguera de desagüe con funda protectora", "ref": None, "precio": None, "cat": "desague",
         "tipo": "Corrugada con funda de espuma", "carga": None, "forma": "manguera de desagüe corrugada gris con codo y una funda de espuma que protege la zona del doblez para que no se aplaste ni se rompa"},
        {"id": "man-7", "foto": "manguera-7.png", "slug": "manguera-tina-bomba-lavadora", "corto": "Manguera tina-bomba", "ref": None, "precio": None, "cat": "tina",
         "tipo": "De la tina a la bomba de desagüe", "carga": None, "forma": "manguera negra corta y gruesa, tipo fuelle, que une la tina con la bomba de desagüe por dentro de la lavadora"},
    ],
}}
L.MARCAS = MARCAS
for _p in MARCAS["todas"]["productos"]:
    _p["nombre"] = _p["corto"] + " para lavadora"

INSTALACION_ENTRADA = [
    "Cierra la llave del agua y desconecta la lavadora de la corriente.",
    "Suelta con la mano (o con unas pinzas, si está apretada) la tuerca de la manguera vieja, en la llave y en la lavadora. Ten un trapo a mano: sale algo de agua.",
    "Revisa que la arandela de goma esté dentro de cada tuerca de la manguera nueva (es la que sella y evita goteos).",
    "Conecta cada extremo: si tu lavadora tiene dos entradas, la tuerca azul va en la de agua fría y la naranja en la de agua caliente. Aprieta a mano y un cuarto de vuelta más; no uses fuerza de más.",
    "Abre la llave despacio y mira las uniones: no debe gotear nada.",
    "Conecta la lavadora y haz un ciclo corto comprobando que llena bien.",
]
INSTALACION_DESAGUE = [
    "Desconecta la lavadora y cierra la llave del agua. Ten una cubeta y trapos: queda agua en la manguera.",
    "Suelta la manguera vieja del desagüe de la pared y de la lavadora (va con una abrazadera o un seguro).",
    "Compara la nueva con la vieja: debe tener el largo que necesitas para llegar al desagüe sin tensarse. Las más largas se usan en las lavadoras de carga frontal.",
    "Conéctala a la lavadora hasta el fondo y asegúrala con la abrazadera.",
    "Deja la punta en el desagüe de la pared formando una curva (un codo hacia arriba) para que no se devuelva el agua. No la metas hasta el fondo ni la dejes aplastada.",
    "Haz un ciclo de desagüe y mira que no haya fugas en las uniones.",
]
INSTALACION_TINA = [
    "Desconecta la lavadora y cierra el agua. Vacía la tina todo lo que puedas.",
    "Abre el panel de la lavadora (atrás o frontal inferior, según el modelo) para ver la manguera que une la tina con la bomba.",
    "Toma una foto de cómo está conectada y suelta las abrazaderas. Tendrás que tener cubeta y trapos: cae agua.",
    "Retira la manguera vieja y compárala con la nueva: deben coincidir en largo y diámetro.",
    "Pon la nueva con las abrazaderas bien apretadas, vuelve a cerrar el panel y haz un ciclo corto comprobando que no hay goteos.",
]
INSTALACION = INSTALACION_ENTRADA
NOTA_INSTALACION = ("Los pasos cambian según el modelo. Si tienes dudas con las mangueras internas o con la parte eléctrica, pídele ayuda a un técnico. "
                    "Y si no estás segura o seguro de cuál necesitas, escríbele al asesor por WhatsApp.")
SINTOMAS = [
    "Hay goteo o un charco de agua en la llave o detrás de la lavadora.",
    "La manguera de entrada está inflada, partida o con la tuerca oxidada.",
    "La lavadora no desagua, o desagua muy despacio, por una manguera doblada, rota o tapada.",
    "Sale olor a humedad o a agua sucia por la manguera de desagüe.",
    "La lavadora no llena de agua o llena muy lento.",
    "Aparecen códigos de error de nivel de agua o de desagüe.",
]


# ---------------------------------------------------------------- imágenes
def preparar_fotos(M, out):
    img = out / "img"
    img.mkdir(parents=True, exist_ok=True)
    for p in M["productos"]:
        f = FOTOS / "todas" / p["foto"]
        if f.exists():
            im = Image.open(f).convert("RGBA")
            fondo = Image.new("RGBA", im.size, (255, 255, 255, 255))
            im = Image.alpha_composite(fondo, im).convert("RGB")
            caja = Image.eval(im.convert("L"), lambda v: 255 if v < 245 else 0).getbbox()
            if caja:
                m = max(8, int(0.04 * max(im.size)))
                im = im.crop((max(0, caja[0] - m), max(0, caja[1] - m), min(im.width, caja[2] + m), min(im.height, caja[3] + m)))
            p["provisional"] = False
        else:  # imagen provisional: se reemplaza al poner la foto real
            im = Image.new("RGB", (900, 900), (240, 243, 250))
            d = ImageDraw.Draw(im)
            fb = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 54)
            fs = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 38)
            d.rounded_rectangle((60, 60, 840, 840), 40, outline=(170, 180, 205), width=6)
            d.text((450, 400), "Foto próximamente", font=fb, fill=(110, 120, 150), anchor="mm")
            d.text((450, 480), p["tipo"], font=fs, fill=(110, 120, 150), anchor="mm")
            p["provisional"] = True
        im.thumbnail((900, 900))
        p["w"], p["h"] = im.size
        im.save(img / f"{p['id']}.jpg", quality=84, optimize=True)
        im.save(img / f"{p['id']}.webp", quality=82)
        im4 = im.copy(); im4.thumbnail((400, 400)); im4.save(img / f"{p['id']}-400.webp", quality=80)


def preparar_entrega(out):
    """Foto de la entrega del paquete: se repinta la etiqueta de la caja para que hable de mangueras de lavadora."""
    im = Image.open(AQUI / "imagenes-tienda" / "entrega.jpg").convert("RGB")
    d = ImageDraw.Draw(im)
    caja = (684, 646, 1030, 800)
    base = (182, 142, 112)
    for y in range(caja[1], caja[3]):
        t = (y - caja[1]) / (caja[3] - caja[1])
        d.line([(caja[0], y), (caja[2], y)], fill=tuple(int(base[i] * (1 - 0.10 * t)) for i in range(3)))
    f1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34)
    f2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    d.text((694, 676), "Mangueras", font=f1, fill=(20, 45, 100))
    d.text((694, 722), "para su lavadora", font=f2, fill=(20, 45, 100))
    im.thumbnail((1100, 1100))
    img = out / "img"
    im.save(img / "entrega-manguera.jpg", quality=84, optimize=True)
    im.save(img / "entrega-manguera.webp", quality=82)
    im6 = im.copy(); im6.thumbnail((640, 640)); im6.save(img / "entrega-manguera-640.webp", quality=80)


def prefijar(h):
    """Todo enlace o imagen que empiece por «/» pasa a vivir dentro de /mangueras-para-lavadora/."""
    h = re.sub(r'(?<![\w.:/-])/img/', PREF + "/img/", h)
    return re.sub(r'(href|action)="/(?!/|mangueras-para-lavadora/)', lambda m: f'{m.group(1)}="{PREF}/', h)


def escribir(out, real, marca, titulo, desc, cuerpo, ld, extra_head=""):
    """Escribe una página PHP en out/<real>/index.php; la infraestructura (lav.php) vive en out/mangueras-para-lavadora/."""
    carpeta = out / real.strip("/")
    carpeta.mkdir(parents=True, exist_ok=True)
    ldj = json.dumps({"@context": "https://schema.org", "@graph": ld}, ensure_ascii=False) if ld else ""
    prof = len(real.strip("/").split("/")) - 1
    php = ("<?php $MARCA = '" + marca + "'; require __DIR__ . '/" + "../" * prof + "lav.php';\n"
           "lav_cabeza(" + json.dumps(titulo, ensure_ascii=False) + ", " + json.dumps(desc, ensure_ascii=False) + ", " + json.dumps(real) + ", "
           + json.dumps(prefijar(extra_head), ensure_ascii=False) + ", <<<'JSON'\n" + ldj + "\nJSON);\n?>\n" + prefijar(cuerpo) + "\n<?php lav_pie(); ?>\n")
    (carpeta / "index.php").write_text(php, encoding="utf-8")


L.escribir = escribir


class SitioM(Sitio):
    """Tienda sin marcas: todo vive directamente en /mangueras-para-lavadora/."""
    def __init__(self, dominio, out):
        self.M = MARCAS["todas"]; self.clave = "todas"
        self.out = out; self.paginas = {}; self.ciudades = ciudades()
        self.pref = PREF
        self.dominio = dominio + PREF
        self.raiz = dominio + PREF
        self.chips_ciudad = [(c[0], f"/mangueras-para-lavadora-en-{slug(c[0])}/") for c in self.ciudades]

    def pagina(self, ruta, titulo, desc, cuerpo, ld=None, prioridad="0.8", extra_head=""):
        if len(desc) > 165:
            c = desc[:160].rsplit(" ", 1)[0].rstrip(" ,;:.")
            desc = c + "."
        super().pagina(ruta, titulo, desc, cuerpo, ld, prioridad, extra_head)

    def barra(self, texto, chico="Pago contra entrega", boton="💬 Pedir por WhatsApp"):
        return f'<div class="m-barra"><span><small>{esc(chico)}</small><b>Asesor por WhatsApp</b></span>{self.boton_asesor(texto, "m-btn wa", boton)}</div>'


# ---------------------------------------------------------------- bloques comunes
def prod(pid): return next(p for p in MARCAS["todas"]["productos"] if p["id"] == pid)


def bloque_importancia():
    return f'''<section class="m-sec lav-importancia"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Lo importante</span><h2>Las mangueras de la lavadora: cuáles son y para qué sirven</h2>
<p>Una lavadora usa varias mangueras, cada una con su trabajo. Cuando una falla aparecen goteos, la máquina no llena, no desagua o muestra un error.</p></div>
<ul class="lav-puntos"><li><b>Manguera de entrada de agua fría (azul).</b> Lleva el agua fría de la llave a la lavadora. Sirve para todas las lavadoras y todas las marcas.</li>
<li><b>Manguera de entrada de agua caliente (naranja).</b> Lleva el agua caliente. Es del mismo tamaño que la azul; solo cambia el color para no confundirlas.</li>
<li><b>Manguera de entrada negra con rosca.</b> Es la más fina, de caucho, con tuercas metálicas. Es la que usan las lavadoras de carga frontal.</li>
<li><b>Manguera de desagüe.</b> Saca el agua sucia hacia el desagüe de la pared. Su medida cambia según la lavadora: las más largas son para carga frontal.</li>
<li><b>Manguera tina-bomba.</b> Va por dentro: une la tina con la bomba de desagüe. Si se agrieta, aparecen fugas debajo de la máquina.</li></ul>
<p><a class="m-btn sec" href="/como-saber-si-la-manguera-esta-danada/">Cómo saber si una manguera está dañada</a></p></div></section>'''


def bloque_entrega():
    foto = ('<picture><source srcset="/img/entrega-manguera-640.webp 640w, /img/entrega-manguera.webp 1100w" sizes="(max-width:860px) 100vw, 520px" type="image/webp">'
            '<img src="/img/entrega-manguera.jpg" alt="Repartidor entregando el paquete con las mangueras de la lavadora a una clienta en la puerta de su casa" width="1100" height="825" loading="lazy"></picture>')
    return f'''<section class="m-sec alt lav-entrega-sec"><div class="m-wrap lav-entrega"><div class="lav-entrega-foto">{foto}</div>
<div class="lav-entrega-tx"><span class="eyebrow">Pago contra entrega</span><h2>Recibes el paquete y pagas</h2>
<p>Pides tu manguera por WhatsApp, el asesor te confirma la correcta, el valor y el envío, y la recibes en tu casa. <b>Pagas cuando tienes el paquete en las manos.</b></p>
<ul class="m-ok"><li>Primero confirmas la manguera correcta con el asesor.</li><li>Te enviamos por transportadora, con número de guía.</li><li>Abres el paquete, la revisas y pagas al recibir.</li></ul>
<p class="m-mut">El asesor te confirma si el pago contra entrega está disponible en tu ciudad.</p></div></div></section>'''


def confianza():
    return '''<section class="m-confianza"><div class="m-wrap"><div><span class="ic">💵</span><span><b>Pago contra entrega</b><small>Pagas al recibir el paquete</small></span></div><div><span class="ic">🚚</span><span><b>Envío a toda Colombia</b><small>Con número de guía</small></span></div><div><span class="ic">💬</span><span><b>Asesor por WhatsApp</b><small>Te confirma la manguera</small></span></div><div><span class="ic">🔧</span><span><b>Cambio paso a paso</b><small>Guía de instalación</small></span></div></div></section>'''


def tres_pasos():
    return '''<section class="m-sec"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Así de fácil</span><h2>Compra en 3 pasos</h2></div><div class="m-cols m-num"><div class="m-bloque"><h3>Escríbele al asesor</h3><p>Dile qué manguera necesitas (entrada, desagüe, tina-bomba…) y, si es de desagüe, el modelo de tu lavadora. También puedes mandar una foto de la manguera vieja.</p></div><div class="m-bloque"><h3>Confirma manguera y envío</h3><p>El asesor te dice cuál es, el valor y el tiempo de entrega a tu ciudad.</p></div><div class="m-bloque"><h3>Recibe y paga</h3><p>Llega a tu casa con número de guía y pagas contra entrega.</p></div></div></div></section>'''


def faq_general():
    c = MARCAS["todas"]["codigos"]
    return [
        ("¿Estas mangueras sirven para todas las lavadoras?", "Las de entrada de agua (azul, naranja y negra con rosca) usan una conexión estándar y sirven para todas las lavadoras y todas las marcas; solo eliges el largo y si la tuya es de carga frontal. La de desagüe cambia de medida según la lavadora, así que el asesor te confirma la tuya."),
        ("¿Cuál es la diferencia entre la manguera azul y la naranja?", "Es solo el color para no confundirlas: la azul es para el agua fría y la naranja para el agua caliente. Son del mismo tamaño y la misma conexión. Si tu lavadora tiene una sola entrada, usa la azul (agua fría)."),
        ("¿Qué es la manguera negra con rosca?", "Es una manguera de entrada de agua de caucho negro, más fina, con tuercas metálicas con rosca. Es la que usan las lavadoras de carga frontal."),
        ("¿La manguera de desagüe es igual para todas las lavadoras?", "No. La medida del desagüe cambia según la lavadora y las más largas se usan en las de carga frontal. Dile al asesor el modelo de tu lavadora y te confirma cuál necesitas."),
        ("¿Qué es la manguera tina-bomba?", "Es una manguera interna que une la tina con la bomba de desagüe. Si se agrieta o se suelta, la lavadora pierde agua por debajo o no desagua."),
        ("¿Cómo sé si la manguera de mi lavadora está dañada?", "Los signos más comunes son goteos en la llave o detrás de la lavadora, manguera inflada, partida o con la tuerca oxidada, desagüe lento y olor a humedad. Antes de cambiarla revisa que no esté doblada ni tapada; el asesor te guía por WhatsApp."),
        (f"¿Qué código de error puede avisar un problema de manguera?", f"Depende del modelo; los de desagüe más comunes son {c}. Un código de desagüe o de nivel de agua puede venir de una manguera doblada, tapada o suelta. Mándale al asesor una foto del código."),
        ("¿Cuánto cuesta?", "El precio depende de la clase de manguera y del largo. Pregúntale al asesor por WhatsApp y te responde en el momento con el valor y el tiempo de entrega a tu ciudad."),
        ("¿Hacen envíos a toda Colombia?", "Sí. Enviamos por transportadora a todo el país y te mandamos el número de guía."),
        ("¿Puedo cambiarla yo mismo?", "Las mangueras de entrada y de desagüe, sí, con algo de práctica: se sueltan con la mano o con una abrazadera. Hay que desconectar la lavadora y cerrar el agua. Abajo está el paso a paso; la tina-bomba, si prefieres, que la cambie un técnico."),
        ("¿Cómo pago?", "Con pago contra entrega: pagas cuando recibes el paquete. El asesor te confirma si está disponible en tu ciudad."),
    ]


# ---------------------------------------------------------------- páginas
def tarjetas(S, cat=None):
    t = ""
    for p in MARCAS["todas"]["productos"]:
        if cat and p["cat"] != cat: continue
        pr = f'<span class="pr">{cop(p["precio"])}<small>Confirma envío con el asesor</small></span>' if p["precio"] else '<span class="pr consulta">Consulta el precio<small>Te responde el asesor</small></span>'
        t += (f'<article class="m-card"><span class="m-tipo">{esc(p["tipo"])}</span><span class="im">{foto_html(p)}</span><div class="tx">'
              f'<h3><a href="/{p["slug"]}/">{esc(p["nombre"])}</a></h3>{pr}'
              + S.boton_asesor(f"Hola, quiero consultar por la {p['nombre']}", "m-btn block wa", "💬 Preguntar al asesor")
              + f'<a class="m-link" href="/{p["slug"]}/">Ver detalles</a></div></article>')
    return t


def corta(t, n=66):
    if len(t) <= n: return t
    return t[:n].rsplit(" ", 1)[0].rstrip(" ,;:|-")


def pagina_inicio(S):
    faq = faq_general()
    P = MARCAS["todas"]["productos"]
    cuerpo = f'''<section class="m-hero"><div class="m-wrap">
  <div>
    <h1>Mangueras para lavadora: entrada de agua, desagüe y tina-bomba</h1>
    <p class="lead">Manguera de entrada de agua fría (azul) y caliente (naranja), manguera negra con rosca para carga frontal, manguera de desagüe y manguera tina-bomba. Las de entrada sirven para todas las lavadoras y todas las marcas. Pídela por WhatsApp y la recibes en toda Colombia con pago contra entrega.</p>
    <div class="acc">{S.boton_asesor("Hola, necesito una manguera para mi lavadora")}<a class="m-btn sec" href="#mangueras">Ver las mangueras</a></div>
    <ul><li>Pago contra entrega</li><li>Envío a toda Colombia</li><li>Asesor que te confirma la manguera</li></ul>
  </div>
  <div class="lav-fotos">{"".join(f'<span class="lf">{foto_html(p, lazy=i>0)}</span>' for i, p in enumerate([P[0], P[1], P[3]]))}</div>
</div></section>
{confianza()}
<section class="m-sec" id="mangueras"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Catálogo</span><h2>Mangueras para lavadora</h2><p>Escoge la clase de manguera que necesitas. El asesor confirma el largo y la medida antes de la compra.</p></div><div class="m-grid">{tarjetas(S)}</div></div></section>
<section class="m-sec alt"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Encuentra la tuya</span><h2>¿Qué manguera necesita mi lavadora?</h2></div>
<div class="m-cols"><div><h3>Entrada de agua</h3><p>Azul para agua fría, naranja para agua caliente y negra con rosca para carga frontal. Son estándar: sirven para todas las lavadoras y todas las marcas.</p><p><a class="m-link" href="/mangueras-de-entrada-de-agua-para-lavadora/">Mangueras de entrada →</a></p></div>
<div><h3>Desagüe</h3><p>Saca el agua sucia. Su medida cambia según la lavadora y las más largas son para carga frontal. El asesor te confirma la tuya.</p><p><a class="m-link" href="/mangueras-de-desague-para-lavadora/">Mangueras de desagüe →</a></p></div>
<div><h3>Tina-bomba</h3><p>Va por dentro de la lavadora, entre la tina y la bomba de desagüe. Si falla, hay fugas debajo de la máquina o no desagua.</p><p><a class="m-link" href="/manguera-tina-bomba-para-lavadora/">Manguera tina-bomba →</a></p></div></div>
<p style="margin-top:14px"><a class="m-btn" href="/cual-es-mi-manguera/">Guía: cuál es mi manguera</a></p></div></section>
{bloque_importancia()}
<section class="m-sec alt"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Señales</span><h2>Cuándo hay que cambiar una manguera de la lavadora</h2></div><ul class="lav-puntos">{"".join(f"<li>{esc(s)}</li>" for s in SINTOMAS)}</ul>
<p>Antes de comprar, descarta lo básico: que la manguera no esté doblada o aplastada contra la pared, que la tuerca esté bien apretada y que el filtro de entrada de la llave esté limpio. Si nada de eso es, la manguera es la sospechosa.</p>
<p><a class="m-btn sec" href="/lavadora-gotea-agua-por-la-manguera/">Mi lavadora gotea: qué revisar</a></p></div></section>
{bloque_entrega()}
{tres_pasos()}
<section class="m-sec"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Mantenimiento</span><h2>Cómo cambiar una manguera de tu lavadora</h2></div>
<div class="m-texto"><p>Cambiar una manguera de entrada o de desagüe es una tarea sencilla: se desconecta la lavadora, se cierra el agua, se suelta la manguera vieja y se pone la nueva. Tenemos el paso a paso con las precauciones.</p>
<p><a class="m-btn sec" href="/cambio-e-instalacion/">Paso a paso para cambiar la manguera</a></p></div></div></section>
<section class="m-sec alt" id="preguntas"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Resolvemos tus dudas</span><h2>Preguntas frecuentes sobre las mangueras de lavadora</h2></div>{faq_html(faq)}</div></section>
<section class="m-sec"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Envíos</span><h2>Enviamos mangueras para lavadora a toda Colombia</h2><p>Escoge tu ciudad para ver el tiempo de entrega y hablar con el asesor.</p></div>{chips(S.chips_ciudad[:24])}<p><a href="/mangueras-para-lavadora-por-ciudad/">Ver todas las ciudades →</a></p></div></section>
<section class="m-sec alt"><div class="m-wrap"><div class="m-cta"><div><h2>¿No sabes cuál manguera necesitas?</h2><p>Mándanos una foto de la manguera vieja o cuéntanos qué le pasa a tu lavadora por WhatsApp.</p></div>{S.boton_asesor("Hola, necesito una manguera para mi lavadora")}</div></div></section>
{S.barra("Hola, necesito una manguera para mi lavadora")}'''
    ld = [{"@type": "WebSite", "name": "Mangueras para lavadora", "url": S.dominio + "/", "inLanguage": "es-CO"},
          {"@type": "CollectionPage", "name": "Mangueras para lavadora", "url": S.dominio + "/", "description": "Mangueras de entrada de agua fría y caliente, negra con rosca, de desagüe y tina-bomba para lavadoras en Colombia."},
          {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i, "url": S.dominio + f"/{p['slug']}/", "name": p["nombre"]} for i, p in enumerate(P, 1)]},
          faq_ld(faq)]
    S.pagina("/", "Mangueras para lavadora | Entrada, desagüe y tina-bomba", "Mangueras de entrada de agua fría y caliente, negra con rosca, de desagüe y tina-bomba para todas las lavadoras. Pide por WhatsApp, paga contra entrega y recibe en toda Colombia.", cuerpo, ld, "1.0",
             f'<meta property="og:image" content="{S.raiz}/img/{P[0]["id"]}.jpg">')


def pasos_de(p):
    return {"entrada": INSTALACION_ENTRADA, "desague": INSTALACION_DESAGUE, "tina": INSTALACION_TINA}[p["cat"]]


def aviso(p):
    if p["id"] == "man-3":
        return "Para lavadoras de carga frontal", "Esta manguera negra con rosca es más fina y es la que usan las lavadoras de carga frontal. La conexión de entrada es estándar: sirve para todas las marcas. Solo te confirmamos el largo."
    if p["cat"] == "entrada":
        return "Sirve para todas las lavadoras", "La conexión de entrada de agua es estándar: sirve para todas las lavadoras y todas las marcas. Solo te confirmamos el largo que necesitas por WhatsApp."
    if p["cat"] == "desague":
        return "La medida del desagüe cambia", "Las mangueras de desagüe no son iguales en todas las lavadoras: las más largas son para las de carga frontal. Dile al asesor el modelo de tu lavadora y te confirma el largo."
    return "Confirma con el asesor", "La tina-bomba depende del modelo de la lavadora. Mándale la etiqueta con el modelo o una foto de la manguera vieja y te confirma la correcta."


def pagina_producto(S, p):
    otros = [(q["nombre"], f"/{q['slug']}/") for q in MARCAS["todas"]["productos"] if q is not p]
    t_av, x_av = aviso(p)
    pasos = pasos_de(p)
    if p["cat"] == "entrada":
        q0 = ("¿Esta manguera sirve para mi lavadora?", "Sí. La entrada de agua es estándar en todas las lavadoras y todas las marcas, así que sirve para la tuya. Lo único que se elige es el largo: escríbele al asesor y te lo confirma.")
    elif p["cat"] == "desague":
        q0 = ("¿Esta manguera sirve para mi lavadora?", "La medida del desagüe cambia según la lavadora. Escríbele al asesor con el modelo (o una foto de la manguera vieja) y te confirma el largo y el tipo antes de que compres.")
    else:
        q0 = ("¿Esta manguera sirve para mi lavadora?", "Depende del modelo. Escríbele al asesor con el modelo de tu lavadora (etiqueta) o una foto de la manguera vieja y te confirma antes de que compres.")
    faq = [q0, ("¿Cuánto cuesta?", "Pregunta al asesor por WhatsApp: te da el precio y el tiempo de entrega a tu ciudad."),
           ("¿Cómo la cambio?", "Desconectas la lavadora, cierras el agua, sueltas la manguera vieja y pones la nueva igual. Abajo está el paso a paso."),
           ("¿Cómo sé que la manguera es la que falla?", "Si hay goteo en la unión, la manguera está inflada o partida, o la lavadora no desagua ni llena y ya revisaste que no esté doblada ni tapada, lo más probable es la manguera. El asesor te ayuda a confirmarlo.")]
    precio = (f'<span class="precio">{cop(p["precio"])}<small>Confirma disponibilidad y envío con el asesor</small></span>' if p["precio"]
              else '<span class="precio consulta">Precio: pregúntale al asesor<small>Respuesta en el momento por WhatsApp</small></span>')
    extra_col = ""
    if p["id"] in ("man-1", "man-2"):
        extra_col = '<p>Recuerda: <b>azul = agua fría</b> y <b>naranja = agua caliente</b>. Si tu lavadora tiene dos entradas, pide una de cada color; si tiene una sola, usa la azul.</p>'
    cuerpo = f'''<div class="m-wrap">{S.miga((p["nombre"], None))}
<div class="m-prod">
  <div class="foto"><span class="m-badge">{esc(p["tipo"])}</span>{foto_html(p, True, False)}</div>
  <div class="info">
    <h1>{esc(p["nombre"])}</h1>
    <span class="sub">{esc(p["tipo"])} · Todas las marcas de lavadora</span>
    {precio}
    <div class="m-aviso"><span style="font-size:22px">💬</span><span><b>{t_av}</b>{x_av}</span></div>
    {S.boton_asesor(f"Hola, quiero consultar por la {p['nombre']}", "m-btn block wa", "💬 Pedir o preguntar al asesor por WhatsApp")}
    <ul class="m-ok"><li><b>Envío a toda Colombia</b> por transportadora, con número de guía.</li><li><b>Guía de cambio</b> paso a paso incluida en esta página.</li><li><b>Pago contra entrega</b>: pagas cuando recibes el paquete (el asesor confirma si aplica en tu ciudad).</li></ul>
  </div>
</div></div>
<section class="m-sec alt"><div class="m-wrap"><div class="m-texto"><div class="m-cab"><span class="eyebrow">Descripción</span><h2>{esc(p["nombre"])}</h2></div>
<p>Es una {esc(p["forma"])}.</p>{extra_col}
<p>Si tu lavadora gotea, no llena, no desagua o muestra un código de error de agua o de desagüe ({MARCAS["todas"]["codigos"]}), una manguera en mal estado es de las primeras cosas que se revisan.</p></div></div></section>
<section class="m-sec"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Datos</span><h2>Ficha del producto</h2></div><dl class="m-ficha"><dt>Clase de manguera</dt><dd>{esc(p["corto"])}</dd><dt>Tipo</dt><dd>{esc(p["tipo"])}</dd><dt>Sirve para</dt><dd>{"Todas las lavadoras y todas las marcas (conexión estándar)" if p["cat"] == "entrada" else "Lavadoras según la medida: el asesor te la confirma"}</dd><dt>Largo y medida</dt><dd>Te los confirma el asesor</dd><dt>Envío</dt><dd>Toda Colombia, por transportadora</dd></dl></div></section>
{bloque_importancia()}
{bloque_entrega()}
<section class="m-sec alt"><div class="m-wrap"><section class="caja tutorial" id="instalacion"><h2>Cómo cambiar esta manguera: paso a paso</h2><ol class="pasos">{"".join(f"<li>{esc(x)}</li>" for x in pasos)}</ol><p class="m-mut">{esc(NOTA_INSTALACION)}</p></section></div></section>
<section class="m-sec"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Preguntas</span><h2>Preguntas frecuentes</h2></div>{faq_html(faq)}</div></section>
<section class="m-sec alt"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Más mangueras</span><h2>Otras mangueras para lavadora</h2></div>{chips(otros)}</div></section>
{S.barra(f"Hola, quiero consultar por la {p['nombre']}")}'''
    prod = {"@type": "Product", "name": p["nombre"], "image": f"{S.raiz}/img/{p['id']}.jpg", "category": "Repuestos para lavadoras",
            "description": f"{p['corto']} para lavadora: {p['tipo'].lower()}. Envío a toda Colombia.", "areaServed": "CO"}
    if p["precio"]:
        prod["offers"] = {"@type": "Offer", "priceCurrency": "COP", "price": p["precio"], "availability": "https://schema.org/InStock", "url": f"{S.dominio}/{p['slug']}/"}
    how = {"@type": "HowTo", "name": f"Cómo cambiar la {p['corto'].lower()} de una lavadora", "step": [{"@type": "HowToStep", "position": i, "text": t} for i, t in enumerate(pasos, 1)]}
    S.pagina(f"/{p['slug']}/", corta(f"{p['corto']} para lavadora | Pago contra entrega"), corta(f"{p['corto']} para lavadora: {p['tipo'].lower()}. Pregunta al asesor por WhatsApp el precio y recibe en toda Colombia con pago contra entrega.", 160), cuerpo,
             [prod, faq_ld(faq), how, S.breadcrumb((p["nombre"], None))], "0.9", f'<link rel="preload" as="image" href="/img/{p["id"]}.webp"><meta property="og:image" content="{S.raiz}/img/{p["id"]}.jpg">')


def pagina_guia(S, ruta, titulo, desc, h1, cuerpo_html, faq=None):
    cuerpo = f'<div class="m-wrap">{S.miga((h1, None))}<div class="m-texto"><h1>{esc(h1)}</h1>{cuerpo_html}</div>' \
             f'<div class="m-cta" style="margin:24px 0"><div><h2>¿Quieres la manguera correcta?</h2><p>Escríbele al asesor por WhatsApp y te confirma cuál necesitas.</p></div>{S.boton_asesor("Hola, tengo una pregunta sobre las mangueras de mi lavadora")}</div>' \
             + (f'<h2>Preguntas frecuentes</h2>{faq_html(faq)}' if faq else "") + "</div>"
    ld = [S.breadcrumb((h1, None))] + ([faq_ld(faq)] if faq else [])
    S.pagina(ruta, corta(titulo, 68), corta(desc, 165), cuerpo, ld, "0.8")


def guias(S):
    F = faq_general()
    def chp(cat=None): return chips([(p["nombre"], f"/{p['slug']}/") for p in MARCAS["todas"]["productos"] if (not cat or p["cat"] in cat)])
    G = lambda *a, **k: pagina_guia(S, *a, **k)
    codigos = MARCAS["todas"]["codigos"]
    # --- categorías
    G("/mangueras-de-entrada-de-agua-para-lavadora/", "Mangueras de entrada de agua para lavadora: azul, naranja y negra", "Mangueras de entrada de agua para lavadora: azul (fría), naranja (caliente) y negra con rosca para carga frontal. Sirven para todas las marcas.",
      "Mangueras de entrada de agua para lavadora",
      "<p>La manguera de entrada lleva el agua de la llave a la lavadora. La conexión es estándar, así que <b>sirve para todas las lavadoras y todas las marcas</b>; solo eliges el color y el largo.</p><ul><li><b>Azul:</b> agua fría.</li><li><b>Naranja:</b> agua caliente.</li><li><b>Negra con rosca:</b> más fina, de caucho, la que usan las lavadoras de carga frontal.</li></ul>" + chp(["entrada"]), F[0:3])
    G("/mangueras-de-desague-para-lavadora/", "Mangueras de desagüe para lavadora: corrugadas, largas y con funda", "Mangueras de desagüe para lavadora: corrugada con codo, larga con extensión y con funda protectora. Las más largas son para carga frontal.",
      "Mangueras de desagüe para lavadora",
      "<p>La manguera de desagüe saca el agua sucia de la lavadora hacia el desagüe de la pared. Es corrugada y flexible. Su medida cambia según la lavadora: <b>las más largas son para las de carga frontal</b>.</p><p>Escríbele al asesor con el modelo de tu lavadora o una foto de la manguera vieja y te confirma el largo.</p>" + chp(["desague"]), [F[3]])
    G("/manguera-tina-bomba-para-lavadora/", "Manguera tina-bomba para lavadora: qué es y cuándo cambiarla", "Manguera tina-bomba para lavadora: la que une la tina con la bomba de desagüe. Señales de falla y cómo pedirla por WhatsApp.",
      "Manguera tina-bomba para lavadora",
      "<p>La manguera tina-bomba va por dentro de la lavadora y une la tina con la bomba de desagüe. Es corta, gruesa y de caucho. Si se agrieta o se suelta, hay fugas debajo de la máquina o la lavadora no desagua.</p><p>Como depende del modelo, el asesor te confirma la correcta con el modelo o una foto de la vieja.</p>" + chp(["tina"]), [F[4]])
    G("/manguera-agua-fria-y-caliente-lavadora-azul-y-naranja/", "Manguera azul y naranja de lavadora: agua fría y caliente", "Qué significan la manguera azul y la naranja de la lavadora: azul para agua fría y naranja para agua caliente. Cómo conectarlas.",
      "Manguera azul y naranja de la lavadora: agua fría y agua caliente",
      "<p>Las mangueras de entrada vienen en dos colores para que no las confundas: <b>la azul es para el agua fría</b> y <b>la naranja para el agua caliente</b>. Son del mismo tamaño y la misma conexión.</p><h2>Cómo conectarlas</h2><ol class='pasos'><li>Azul a la llave de agua fría y a la entrada de agua fría de la lavadora.</li><li>Naranja a la llave de agua caliente y a la entrada de agua caliente.</li><li>Si tu lavadora tiene una sola entrada, usa la azul (agua fría).</li></ol>" + chp(["entrada"]), F[1:2])
    G("/manguera-negra-con-rosca-lavadora-carga-frontal/", "Manguera negra con rosca para lavadora de carga frontal", "Manguera de entrada negra con rosca para lavadoras de carga frontal: más fina, de caucho y con tuercas metálicas. Pídela por WhatsApp.",
      "Manguera negra con rosca para lavadora de carga frontal",
      "<p>Es una manguera de entrada de agua de caucho negro, más fina que las de color, con tuercas metálicas con rosca en los dos extremos. Es la que usan las lavadoras de carga frontal.</p><p>La conexión es estándar: sirve para todas las marcas. Solo hay que elegir el largo.</p>" + chp(["entrada"]), F[2:3])
    G("/desague-largo-para-lavadora-de-carga-frontal/", "Desagüe largo para lavadora de carga frontal: cuál elegir", "Por qué las lavadoras de carga frontal usan una manguera de desagüe más larga y cómo elegir el largo correcto.",
      "Desagüe largo para lavadora de carga frontal",
      "<p>Las lavadoras de carga frontal suelen necesitar una manguera de desagüe más larga que las de carga superior. Si la tuya queda corta, tensa el desagüe y se puede soltar; si es muy larga, se dobla y no desagua bien.</p><h2>Cómo elegir el largo</h2><ol class='pasos'><li>Mide la distancia desde la parte de atrás de la lavadora hasta el desagüe de la pared.</li><li>Suma un poco para la curva que debe hacer la manguera (un codo hacia arriba).</li><li>Mándale la medida al asesor por WhatsApp y te dice cuál manguera es.</li></ol>" + chp(["desague"]), [F[3]])
    # --- guías
    G("/cual-es-mi-manguera/", "¿Cuál manguera necesita mi lavadora? Guía", "Cómo saber qué manguera necesita tu lavadora: entrada, desagüe o tina-bomba. Cuáles sirven para todas las marcas.",
      "¿Cuál manguera necesita mi lavadora?",
      "<p>Mira cuál manguera falla y qué tipo de lavadora tienes:</p><h2>1. Cuál manguera es</h2><ul><li><b>Entrada de agua:</b> de la llave a la lavadora. Es estándar y sirve para todas: azul (fría), naranja (caliente) o negra con rosca (carga frontal).</li><li><b>Desagüe:</b> de la lavadora al desagüe. Su medida cambia; las más largas son para carga frontal.</li><li><b>Tina-bomba:</b> manguera interna entre la tina y la bomba.</li></ul>" + chp() +
      "<h2>2. El modelo de la lavadora</h2><p>Está en una etiqueta atrás, en un costado o bajo la tapa. Para el desagüe y la tina-bomba, el asesor lo usa para confirmarte la manguera.</p><h2>3. La manguera vieja</h2><p>Compárala por el largo, el diámetro y la forma de las puntas. Una foto al asesor ayuda a confirmarla.</p>", [F[0], F[3]])
    G("/como-saber-si-la-manguera-esta-danada/", "Cómo saber si una manguera de la lavadora está dañada", "Señales de que una manguera de tu lavadora falla y qué revisar antes de comprar una nueva.",
      "Cómo saber si una manguera de la lavadora está dañada",
      "<p>Las mangueras se desgastan con el tiempo, el sol, la presión del agua y la cal. Estas son las señales más comunes:</p><ul>" + "".join(f"<li>{esc(s)}</li>" for s in SINTOMAS) + "</ul>"
      "<h2>Antes de cambiarla, revisa esto</h2><ol class='pasos'><li>Desconecta la lavadora y revisa que las mangueras no estén dobladas ni aplastadas contra la pared.</li><li>Mira las tuercas y las uniones: si hay humedad o sarro, hay fuga.</li><li>Pasa la mano por la manguera de entrada: si se siente inflada, blanda o con grietas, cámbiala.</li><li>Limpia el filtro de malla de la entrada (va en la punta de la manguera, junto a la llave).</li></ol>"
      "<p>Si después de esto sigue igual, escríbele al asesor.</p>", [F[5]])
    G("/cambio-e-instalacion/", "Cómo cambiar una manguera de la lavadora: paso a paso", "Paso a paso para cambiar la manguera de entrada, de desagüe o la tina-bomba de una lavadora, con precauciones.",
      "Cómo cambiar una manguera de la lavadora",
      "<h2>Manguera de entrada de agua</h2><ol class='pasos'>" + "".join(f"<li>{esc(x)}</li>" for x in INSTALACION_ENTRADA) + "</ol><h2>Manguera de desagüe</h2><ol class='pasos'>" + "".join(f"<li>{esc(x)}</li>" for x in INSTALACION_DESAGUE) + "</ol><h2>Manguera tina-bomba</h2><ol class='pasos'>" + "".join(f"<li>{esc(x)}</li>" for x in INSTALACION_TINA) + f"</ol><p class='m-mut'>{esc(NOTA_INSTALACION)}</p>", [F[9]])
    G("/lavadora-gotea-agua-por-la-manguera/", "Lavadora gotea agua: causas y qué manguera revisar", "Por qué una lavadora gotea o deja un charco, qué revisar (llave, tuercas, mangueras) y cuándo cambiar la manguera.",
      "Mi lavadora gotea agua",
      "<p>Cuando la lavadora gotea, casi siempre el culpable es una manguera o una unión. De la causa más fácil a la más seria:</p>"
      "<h2>Qué revisar, en orden</h2><ol class='pasos'><li><b>Tuerca floja en la llave o en la lavadora.</b> Apriétala con la mano y un cuarto de vuelta más.</li><li><b>Arandela de goma de la tuerca</b> gastada o ausente: cámbiala.</li><li><b>Manguera de entrada inflada, partida o resecada.</b> Hay que cambiarla.</li><li><b>Manguera de desagüe suelta del desagüe de la pared</b> o con un agujero.</li><li><b>Manguera interna agrietada</b> (tina-bomba). Se confirma al abrir el panel.</li></ol>"
      "<p>Seguridad: cierra la llave y desconecta la lavadora antes de meter la mano.</p>" + chp(), [F[5]])
    G("/lavadora-no-desagua/", "Lavadora no desagua: causas y mangueras a revisar", "Por qué una lavadora no desagua, qué revisar (manguera de desagüe, filtro, bomba) y cuándo cambiar la manguera.",
      "Mi lavadora no desagua",
      "<p>Cuando una lavadora no desagua, el agua se queda en la tina y el ciclo se detiene. De la causa más fácil a la más seria:</p>"
      "<h2>Qué revisar, en orden</h2><ol class='pasos'><li><b>Manguera de desagüe doblada o aplastada</b> contra la pared o el mueble.</li><li><b>Manguera de desagüe tapada</b> con pelusa o jabón: se desconecta y se enjuaga.</li><li><b>Desagüe de la pared obstruido</b> o con la manguera metida hasta el fondo.</li><li><b>Filtro de desagüe tapado</b> (en carga frontal, abajo).</li><li><b>Manguera tina-bomba agrietada o suelta</b> por dentro, o bomba atascada: lo confirma un técnico.</li></ol>"
      "<p>Seguridad: desconecta la lavadora antes de meter la mano y ten una cubeta para el agua que quede en la tina.</p>" + chp(["desague", "tina"]), [F[3], F[5]])
    G("/lavadora-no-llena-de-agua/", "Lavadora no llena de agua: mangueras a revisar", "Por qué una lavadora no llena de agua o llena muy lento y qué manguera de entrada revisar.",
      "Mi lavadora no llena de agua",
      "<p>Si la lavadora no llena o llena muy despacio, el problema suele estar antes de la máquina o en las mangueras de entrada.</p><h2>Revisa</h2><ol class='pasos'><li>Que la llave del agua esté bien abierta.</li><li>Que la manguera de entrada no esté doblada ni aplastada.</li><li>El filtro de malla de la punta de la manguera: si está tapado con sarro o arena, límpialo.</li><li>Que la manguera azul (fría) esté en la entrada correcta.</li><li>Si todo esto está bien, puede ser la válvula de entrada: la revisa un técnico.</li></ol>" + chp(["entrada"]))
    G("/codigo-error-desague-lavadora/", f"Código de error de desagüe en lavadora ({codigos})", f"Qué significan los códigos de desagüe de las lavadoras ({codigos}) y cuándo apuntan a una manguera doblada, tapada o suelta.",
      f"Código de error de desagüe en la lavadora ({codigos})",
      f"<p>Los códigos de error de desagüe más habituales son <b>{codigos}</b>. Indican que la máquina no logra sacar el agua en el tiempo esperado. El significado exacto depende de la marca y del modelo.</p><h2>Qué hacer</h2><ol class='pasos'><li>Desconecta la lavadora unos minutos y vuelve a encenderla.</li><li>Revisa que la manguera de desagüe no esté doblada, tapada ni metida hasta el fondo del desagüe.</li><li>Limpia el filtro de desagüe.</li><li>Si el código vuelve, la causa probable es una manguera interna (tina-bomba) o la bomba.</li></ol><p>Mándale al asesor una foto del código.</p>")
    G("/cuanto-cuesta-una-manguera-para-lavadora/", "Cuánto cuesta una manguera para lavadora", "De qué depende el precio de una manguera para lavadora y cómo consultarlo con el asesor.",
      "Cuánto cuesta una manguera para lavadora",
      "<p>El precio depende de la clase de manguera (entrada, desagüe o tina-bomba), del largo y de la ciudad de envío. Por eso no mostramos un valor único: el asesor te lo da en el momento por WhatsApp.</p><h2>Qué mandarle</h2><ul><li>Cuál manguera necesitas y, si es de desagüe, el modelo de tu lavadora.</li><li>Una foto de la manguera vieja, si ya la sacaste.</li><li>Tu ciudad.</li></ul>" + chp())
    G("/manguera-de-desague-o-de-entrada-de-la-lavadora/", "Manguera de desagüe o de entrada de lavadora: diferencias", "Cuál es la diferencia entre la manguera de desagüe y la de entrada de agua de una lavadora y cuál necesitas.",
      "Manguera de desagüe o de entrada de la lavadora: ¿cuál es cuál?",
      "<p>Son dos mangueras distintas y no se pueden cambiar entre sí.</p><ul><li><b>Manguera de entrada de agua:</b> trae agua a presión desde la llave. Es reforzada, lleva una tuerca en cada punta y es estándar para todas las lavadoras.</li><li><b>Manguera de desagüe:</b> saca el agua sucia por gravedad. Es corrugada, más ancha y flexible, y suele terminar en un codo. Su medida cambia según la lavadora.</li></ul><p>Si tu lavadora gotea en la llave o llena lento, mira la de entrada. Si no desagua o huele a humedad, mira la de desagüe.</p>" + chp())


def paginas_ciudad(S):
    for c in S.ciudades:
        ciudad, depto = c[0], c[1]
        ruta = f"/mangueras-para-lavadora-en-{slug(ciudad)}/"
        h1 = f"Mangueras para lavadora en {ciudad}"
        faq = [(f"¿Envían mangueras para lavadora a {ciudad}?", f"Sí. Enviamos por transportadora a {ciudad} ({depto}) y te mandamos el número de guía. Pregunta al asesor por el tiempo de entrega y si hay pago contra entrega en tu ciudad."),
               ("¿Cómo sé cuál manguera necesito?", "Las de entrada de agua sirven para todas las lavadoras; para la de desagüe o la tina-bomba, mándale al asesor el modelo de tu lavadora o una foto de la manguera vieja por WhatsApp.")]
        cuerpo = f'''<div class="m-wrap">{S.miga((f"Mangueras para lavadora en {ciudad}", None))}<div class="m-texto"><h1>{esc(h1)}</h1>
<p>Si tu lavadora en {esc(ciudad)}, {esc(depto)}, gotea, no desagua o no llena, aquí encuentras la manguera que necesita: entrada de agua fría (azul) o caliente (naranja), negra con rosca para carga frontal, desagüe y tina-bomba. La enviamos por transportadora y el asesor te confirma la correcta antes de comprar.</p>
{chips([(p["nombre"], f"/{p['slug']}/") for p in MARCAS["todas"]["productos"]])}
<p style="margin-top:16px">{S.boton_asesor(f"Hola, soy de {ciudad} y necesito una manguera para mi lavadora")}</p>
<h2>Preguntas frecuentes</h2>{faq_html(faq)}<p><a href="/mangueras-para-lavadora-por-ciudad/">Ver todas las ciudades →</a></p></div></div>
{bloque_entrega()}
{S.barra(f"Hola, soy de {ciudad} y necesito una manguera para mi lavadora")}'''
        S.pagina(ruta, corta(f"{h1} | Envío a todo el país") if len(f"{h1} | Envío a todo el país") <= 66 else corta(h1), f"Mangueras para lavadora en {ciudad}, {depto}: entrada de agua, desagüe y tina-bomba. Pregunta al asesor por WhatsApp y recibe en tu ciudad con pago contra entrega.", cuerpo,
                 [faq_ld(faq), S.breadcrumb((f"Mangueras para lavadora en {ciudad}", None))], "0.6")
    cuerpo = f'<div class="m-wrap">{S.miga(("Ciudades", None))}<div class="m-texto"><h1>Mangueras para lavadora en toda Colombia</h1><p>Elige tu ciudad.</p>{chips(S.chips_ciudad)}</div></div>'
    S.pagina("/mangueras-para-lavadora-por-ciudad/", "Mangueras para lavadora por ciudad", f"Envíos de mangueras para lavadora a {len(S.ciudades)} ciudades de Colombia: elige la tuya y pregunta al asesor por WhatsApp.", cuerpo, [S.breadcrumb(("Ciudades", None))], "0.7")


# ---------------------------------------------------------------- legales, textos y portada
REEMPLAZOS = [("distribuidor autorizado", "vendedor"), ("Distribuidor autorizado", "Vendedor"), (" con autorización", ""),
              ("del nevecón", "de la lavadora"), ("al nevecón", "a la lavadora"), ("el nevecón", "la lavadora"), ("un nevecón", "una lavadora"), ("los nevecones", "las lavadoras"),
              ("nevecones", "lavadoras"), ("Nevecones", "Lavadoras"), ("nevecón", "lavadora"), ("Nevecón", "Lavadora"), ("nevecon", "lavadora"),
              ("las neveras", "las lavadoras"), ("neveras", "lavadoras"), ("nevera", "lavadora"), ("filtros de agua", "mangueras para lavadora"), ("Filtros de agua", "Mangueras para lavadora"),
              ("filtro de agua", "manguera"), ("Filtro de agua", "Manguera")]
L.REEMPLAZOS = REEMPLAZOS
L.QUIENES = """<?php $MARCA = 'home'; require __DIR__ . '/lav.php';
$n = sitio()['negocio'];
lav_cabeza('Quiénes somos | ' . $n['nombre'], 'Somos un comercio colombiano de mangueras para lavadoras (entrada de agua, desagüe, tina-bomba), con asesoría por WhatsApp y envíos a todo el país.', '/quienes-somos.php', '', '')
?>
<div class="m-wrap"><div class="m-texto"><h1>Quiénes somos</h1>
<p><?= h($n['nombre']) ?> es un comercio colombiano de mangueras para lavadoras: de entrada de agua fría y caliente, negras con rosca, de desagüe y tina-bomba. Te ayudamos a encontrar la manguera que necesita tu lavadora y te la enviamos a donde estés.</p>
<p>Antes de que compres, un asesor revisa contigo cuál manguera necesitas por WhatsApp, para que pidas la correcta.</p>
<p>Atendemos <?= h($n['horario']) ?>. Escríbenos por WhatsApp: __TELEFONOS__ o al correo <?= h($n['correo']) ?>.</p>
<p><?= h($n['nombre']) ?> · <?= h($n['titular']) ?> · <?= h($n['documento']) ?></p></div></div>
<?php lav_pie(); ?>
"""
L.LEGALES = {
    "terminos": ("Términos y condiciones", """<p>Este sitio presenta mangueras para lavadoras (de entrada de agua, de desagüe y tina-bomba). No tiene carrito ni pago en línea: los pedidos se hacen por WhatsApp con un asesor y se pagan contra entrega.</p>
<h2>Cómo se hace un pedido</h2><p>Escribe al asesor por WhatsApp con la clase de manguera y, si hace falta, el modelo de tu lavadora o una foto de la manguera vieja. El asesor te confirma la manguera, el precio, el valor del envío y si hay pago contra entrega en tu ciudad antes de despachar.</p>
<h2>Confirma antes de comprar</h2><p>Las fotos son de referencia. Antes de pagar, compara la manguera con la que tienes o confirma el largo con el asesor. La instalación es responsabilidad del comprador; si no tienes experiencia con las partes internas de la lavadora, pídele ayuda a un técnico.</p>"""),
    "privacidad": ("Tratamiento de datos personales", """<p>Cuando nos escribes por WhatsApp usamos tu nombre, tu número y los datos que nos des (ciudad, dirección, modelo de la lavadora) solo para atender tu consulta, confirmar tu pedido y enviártelo.</p>
<p>No vendemos tus datos. Puedes pedirnos que los corrijamos o los eliminemos escribiéndonos por WhatsApp o al correo de contacto.</p>
<p>Este sitio puede usar herramientas de medición (como Google Analytics) para saber cuántas personas lo visitan.</p>"""),
    "garantia-y-retracto": ("Garantía y retracto", """<p>Si la manguera llega con algún defecto, escríbenos por WhatsApp con una foto y la revisamos.</p>
<p>Para compras a distancia puedes ejercer el derecho de retracto dentro de los 5 días hábiles siguientes a la entrega, según la ley colombiana, siempre que el producto no haya sido instalado ni usado y esté en buen estado. Coordina la devolución con el asesor.</p>
<p>Autoridad de protección al consumidor: <a href="https://www.sic.gov.co/" target="_blank" rel="noopener">Superintendencia de Industria y Comercio</a>.</p>"""),
}


def marca_json(S):
    M = S.M; b = PREF + "/"
    guias_ = [[b + "cual-es-mi-manguera/", "¿Cuál manguera necesita mi lavadora?"], [b + "como-saber-si-la-manguera-esta-danada/", "Cómo saber si una manguera está dañada"],
              [b + "cambio-e-instalacion/", "Cómo cambiar la manguera"], [b + "lavadora-gotea-agua-por-la-manguera/", "La lavadora gotea"],
              [b + "lavadora-no-desagua/", "La lavadora no desagua"], [b + "manguera-agua-fria-y-caliente-lavadora-azul-y-naranja/", "Manguera azul y naranja"],
              [b + "desague-largo-para-lavadora-de-carga-frontal/", "Desagüe largo para carga frontal"]]
    cats = [[b + "mangueras-de-entrada-de-agua-para-lavadora/", "Mangueras de entrada de agua"], [b + "mangueras-de-desague-para-lavadora/", "Mangueras de desagüe"], [b + "manguera-tina-bomba-para-lavadora/", "Manguera tina-bomba"]]
    return {"nombre": M["nombre"], "clase": M["clase"], "base": b, "tema": M["tema"], "fuentes": FUENTES, "tienda": M["tienda"], "logo": "", "logo_w": 0, "logo_h": 0, "icono": PREF + "/img/icono.svg",
            "whatsapp": M["whatsapp"], "telefono": M["telefono"], "productos": [[p["nombre"], p["slug"]] for p in M["productos"]], "guias": guias_,
            "ciudades": [[c, f"{b}mangueras-para-lavadora-en-{slug(c)}/"] for c in ["Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena", "Bucaramanga", "Pereira", "Manizales", "Armenia", "Ibagué", "Cúcuta", "Santa Marta"]],
            "hub": b + "mangueras-para-lavadora-por-ciudad/", "extra": cats, "externos": [["Superintendencia de Industria y Comercio", "https://www.sic.gov.co/"]]}


def llms_php(S):
    txt = ("# Mangueras para lavadora\n\n> Mangueras de entrada de agua fría (azul) y caliente (naranja), negra con rosca para carga frontal, de desagüe y tina-bomba para lavadoras de todas las marcas, con envío a toda Colombia y pago contra entrega. "
           "El largo y el precio se confirman con un asesor por WhatsApp.\n\n## Productos\n")
    for p in MARCAS["todas"]["productos"]:
        txt += f"- [{p['nombre']}](__BASE__{PREF}/{p['slug']}/): {p['tipo']}.\n"
    txt += f"\n## Guías\n- [Cuál manguera necesita mi lavadora](__BASE__{PREF}/cual-es-mi-manguera/)\n- [Cómo cambiar la manguera](__BASE__{PREF}/cambio-e-instalacion/)\n- [Manguera azul y naranja: agua fría y caliente](__BASE__{PREF}/manguera-agua-fria-y-caliente-lavadora-azul-y-naranja/)\n"
    txt += "\n## Preguntas y respuestas\n" + "".join(f"- **{q}** {a}\n" for q, a in faq_general()[:6])
    return "<?php\nrequire __DIR__ . '/api/sitio.php';\nheader('Content-Type: text/plain; charset=utf-8');\necho str_replace('__BASE__', sitio()['base'], <<<'TXT'\n" + txt + "TXT);\n"


# ---------------------------------------------------------------- construcción
def construir_todo(dominio):
    base = AQUI / "sitios" / "samsung"
    raiz = SALIDA / "tienda"                       # lo que se sube a public_html
    out = raiz / PREF.strip("/")                   # toda la tienda vive en /mangueras-para-lavadora/
    if raiz.exists():
        shutil.rmtree(raiz)
    out.mkdir(parents=True)
    for nombre in ["api", "data", "404.php", "estilo.css", "marcas.css", "marcas.php", "partes.php"]:   # sin .htaccess ni robots: son de la raíz
        o = base / nombre
        if o.is_dir():
            shutil.copytree(o, out / nombre, ignore=shutil.ignore_patterns("pedidos.sqlite*", "correos.log", "config.php"))
        else:
            shutil.copy(o, out / nombre)
    mp = (out / "marcas.php").read_text(encoding="utf-8")
    mp = mp.replace("✔ Distribuidor autorizado ' . h($M['nombre']) . ' en Colombia", "✔ Mangueras para lavadora ' . h($M['nombre']) . ' en Colombia").replace("<small>Distribuidor autorizado</small>", "<small>Mangueras para lavadora</small>")
    mp = mp.replace("Distribuidor autorizado de filtros de agua ' . h($M['nombre']) . ' en Colombia, con envío gratis a todo el país y pago seguro en línea.", "Mangueras para lavadora ' . h($M['nombre']) . ', con envío a todo el país y atención por WhatsApp.")
    mp = mp.replace("Distribuidor autorizado de filtros de agua ' . h($M['nombre']) . ' en Colombia. ' . h($M['nombre']) . ' y su logo son marcas registradas de su dueño y se usan con autorización.", "' . h($M['nombre']) . ' y su logo son marcas registradas de su dueño y se usan solo para indicar el tipo de lavadora.")
    mp = mp.replace('<script src="/carrito.js" defer></script>', '').replace("'</div><div class=\"m-wrap m-pie-medios\"><span>🔒 Pagos procesados en página segura</span>' . medios_pago_html() . '</div>'", "'</div>'")
    mp = re.sub(r"\$cart = '.*?';\n", "$cart = '';\n", mp, count=1, flags=re.S).replace("<a href=\"/carrito.php\">Mi carrito</a>", "").replace("🔒 Pago seguro en línea", "💵 Pago contra entrega")
    mp = mp.replace(" y pago seguro en línea", " y atención por WhatsApp")
    mp = mp.replace("Distribuidor autorizado", "Mangueras para lavadora").replace("Precios en pesos colombianos con envío incluido.", "Precios en pesos colombianos.")
    mp = mp.replace("Cuándo cambiarlo y cómo instalarlo", "Cómo cambiar la manguera")
    mp = mp.replace("return '<b>' . h($M['nombre']) . '</b>';", "return '<b class=\"m-logo-txt\">' . h($M['tienda'] ?? $M['nombre']) . '</b>';").replace("<small>Mangueras para lavadora</small>", "")
    mp = mp.replace("$tel = preg_replace('/\\D/', '', (string) (cfg()['whatsapp'] ?? ''));", "$tel = preg_replace('/\\D/', '', (string) ($M['whatsapp'] ?? (cfg()['whatsapp'] ?? '')));")
    mp = mp.replace("h($n['telefono']) . '</a>'", "h($M['telefono'] ?? $n['telefono']) . '</a>'")
    for a_, b_ in [("aria-label=\"Filtros '", "aria-label=\"Mangueras para lavadora '"), ("$dd('Filtros', $filtros)", "$dd('Mangueras', $filtros)"), ("'<b>Filtros</b>'", "'<b>Mangueras</b>'"),
                   ("cual-es-mi-filtro/", "cual-es-mi-manguera/"), ("'<nav><b>Filtros ' . h($M['nombre'])", "'<nav><b>Mangueras ' . h($M['nombre'])"),
                   (">Filtros ' . h($M['nombre']) . ' en '", ">Mangueras para lavadora ' . h($M['nombre']) . ' en '"), ("¿Cuál filtro es el mío?", "¿Cuál manguera es la mía?"),
                   ("content=\"Filtros '", "content=\"Mangueras para lavadora '"), ("(filtros, guías, ciudades)", "(mangueras, guías, ciudades)"),
                   ("Envío gratis a toda Colombia", "Envío a toda Colombia"),
                   # rutas de esta tienda: todo bajo /mangueras-para-lavadora/
                   ('href="/marcas.css"', f'href="{PREF}/marcas.css"'), ('href="/estilo.css"', f'href="{PREF}/estilo.css"'), ("'/img/icono.svg'", f"'{PREF}/img/icono.svg'"),
                   ('href="/terminos.php"', f'href="{PREF}/terminos.php"'), ('href="/privacidad.php"', f'href="{PREF}/privacidad.php"'),
                   ('href="/garantia-y-retracto.php"', f'href="{PREF}/garantia-y-retracto.php"'), ('href="/quienes-somos.php"', f'href="{PREF}/quienes-somos.php"')]:
        mp = mp.replace(a_, b_)
    mp = re.sub(r"Mangueras para lavadora '\s*\.\s*h\(\$M\['nombre'\]\)", "' . h($M['nombre'])", mp)
    mp = re.sub(r"Mangueras '\s*\.\s*h\(\$M\['nombre'\]\)", "' . h($M['nombre'])", mp)
    (out / "marcas.php").write_text(mp, encoding="utf-8")
    for f in ["partes.php", "404.php"]:
        t = (out / f).read_text(encoding="utf-8").replace("Filtros<b>Lavadoras</b>", "Mangueras<b>Lavadoras</b>")
        (out / f).write_text(t, encoding="utf-8")
    (out / "marcas.css").write_text((out / "marcas.css").read_text(encoding="utf-8") + CSS_EXTRA, encoding="utf-8")
    (out / "lav.php").write_text(LAV_PHP.replace("filtros para lavadoras (generado por lavadoras.py)", "mangueras para lavadoras (generado por mangueras.py)"), encoding="utf-8")
    L.limpiar_textos(out)
    lib = (out / "api" / "lib.php").read_text(encoding="utf-8")
    lib = lib.replace("$num = preg_replace('/\\D/', '', (string) (cfg()['whatsapp'] ?? ''));\n    if (strlen($num) === 10)", "$num = preg_replace('/\\D/', '', (string) (($GLOBALS['M']['whatsapp'] ?? null) ?? (cfg()['whatsapp'] ?? '')));\n    if (strlen($num) === 10)")
    (out / "api" / "lib.php").write_text(lib, encoding="utf-8")
    for f in ["pedido.php", "wompi.php", "estado.php", "reconciliar.php", "recordatorios.php"]:
        (out / "api" / f).unlink(missing_ok=True)
    L.legales(out)
    for nombre in list(L.LEGALES) + ["quienes-somos"]:   # la ruta canónica de las páginas legales incluye la carpeta
        p_ = out / (nombre + ".php")
        p_.write_text(p_.read_text(encoding="utf-8").replace(f"'/{nombre}.php'", f"'{PREF}/{nombre}.php'"), encoding="utf-8")
    tel = " · ".join(f"{m['nombre']} {m['telefono']}" for m in MARCAS.values())
    q = (out / "quienes-somos.php").read_text(encoding="utf-8").replace("__TELEFONOS__", tel)
    (out / "quienes-somos.php").write_text(q, encoding="utf-8")
    (out / "img").mkdir(exist_ok=True)
    shutil.copy(base / "img" / "icono.svg", out / "img" / "icono.svg")
    preparar_entrega(out)
    S = SitioM(dominio, raiz)
    preparar_fotos(MARCAS["todas"], out)
    mj = json.dumps(marca_json(S), ensure_ascii=False)
    for nombre in ("marca-todas.json", "marca-home.json", "marca.json"):
        (out / nombre).write_text(mj, encoding="utf-8")
    pagina_inicio(S)
    for p in MARCAS["todas"]["productos"]:
        pagina_producto(S, p)
    guias(S)
    paginas_ciudad(S)
    paginas = dict(S.paginas)
    cat = json.loads(subprocess.run(["php", "-r", "echo json_encode(include '" + str(base / 'api' / 'catalogo.php') + "', JSON_UNESCAPED_UNICODE);"], capture_output=True, text=True, check=True).stdout)
    cat["productos"] = {}
    cat["paginas"] = [k[len(PREF):] or "/" for k in paginas]
    cat["marcas"], cat["guias"], cat["compat"], cat["blog"], cat["rutas_ciudad"] = [], [], [], [], {}
    (out / "api" / "catalogo.php").write_text("<?php\n// Generado por mangueras.py: no lo edites a mano.\nreturn " + php_val(cat) + ";\n", encoding="utf-8")
    sm = SITEMAP_PHP.replace("$b = sitio()['base'];", "$b = sitio()['base'] . '" + PREF + "';").replace("'/quienes-somos.php'", "'/quienes-somos.php'")
    (out / "sitemap.php").write_text(sm, encoding="utf-8")
    (out / "llms.php").write_text(llms_php(S), encoding="utf-8")
    (out / ".htaccess").write_text("""DirectoryIndex index.php
Options -Indexes
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteCond %{HTTP:X-Forwarded-Proto} !https
RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
RewriteRule ^sitemap\\.xml$ sitemap.php [L]
RewriteRule ^llms\\.txt$ llms.php [L]
<FilesMatch "^(partes\\.php|marcas\\.php|marca.*\\.json|.*\\.md)$">
  Require all denied
</FilesMatch>
<FilesMatch "\\.(sqlite|sqlite-wal|sqlite-shm|log)$">
  Require all denied
</FilesMatch>
<IfModule mod_headers.c>
  Header always set X-Content-Type-Options "nosniff"
  Header always set Referrer-Policy "strict-origin-when-cross-origin"
</IfModule>
""", encoding="utf-8")
    cfg = (base / "api" / "config.sample.php").read_text(encoding="utf-8")
    sam = MARCAS["todas"]
    cfg = cfg.replace("https://filtrosaguanevecones.com", dominio).replace("Filtros Nevecones Colombia", "Filtros para lavadoras").replace("321 799 6144", sam["telefono"]).replace("3217996144", sam["whatsapp"])
    cfg = cfg.replace("pedidos@filtrosaguanevecones.com", "pedidos@" + dominio.split("//")[1])
    cfg = cfg.replace("GTM-5WSNHV66", GTM)                                                    # el mismo Tag Manager de filtrosparalavadoras.click
    cfg = re.sub(r"('google_verificacion'\s*=>\s*)'[^']*'", r"\1'" + VERIFICACION + "'", cfg)  # y la misma verificación de Search Console
    (out / "api" / "config.sample.php").write_text(cfg, encoding="utf-8")
    inst = out / "INSTALAR.md"
    inst.write_text(f"""# Mangueras para lavadora (todas las marcas), dentro de {dominio}

Todo vive en la carpeta `mangueras-para-lavadora/`, así que no pisa nada de las otras tiendas (`/samsung/`, `/lg/`, `/bombas-de-agua/`, `api/`, `.htaccess`, etc.).

- Tienda: {dominio}{PREF}/ (sin marcas: sirve para todas las lavadoras)
- Asesor WhatsApp: {TELEFONO} (para cambiarlo, edita WHATSAPP y TELEFONO al inicio de `mangueras.py` y vuelve a generar)

Sin carrito ni pago en línea: los pedidos se hacen por WhatsApp con el asesor (pago contra entrega).

1. En Hostinger abre el administrador de archivos del dominio {dominio.split('//')[1]}, entra a `public_html`, sube `tienda-mangueras-para-lavadora.zip` y descomprímelo ahí. Se crea solo la carpeta `mangueras-para-lavadora`.
2. Dentro de `mangueras-para-lavadora/api/` copia `config.sample.php` como `config.php` y completa el correo, el titular y el documento (iguales a los de la otra tienda). El Tag Manager ({GTM}) y la verificación de Search Console ya vienen puestos.
3. Cada clic en un botón de WhatsApp manda el mismo evento `whatsapp` a Tag Manager, igual que en las otras tiendas, así que cuenta como la misma conversión.
4. En Search Console agrega el sitemap {dominio}{PREF}/sitemap.xml (la propiedad es la misma).
5. Precios: mientras una manguera no tenga precio, su página dice «pregúntale al asesor».
""", encoding="utf-8")
    z = AQUI / "tienda-mangueras-para-lavadora.zip"
    z.unlink(missing_ok=True)
    (AQUI / "tienda-mangueras.zip").unlink(missing_ok=True)
    subprocess.run(["zip", "-qr", str(z), PREF.strip("/"), "-x", f"{PREF.strip('/')}/api/config.php", "-x", f"{PREF.strip('/')}/data/pedidos.sqlite*", "-x", f"{PREF.strip('/')}/data/correos.log"], cwd=raiz, check=True)
    sin_foto = [p["tipo"] for p in MARCAS["todas"]["productos"] if p.get("provisional")]
    print(f"Mangueras para lavadora: sitios-mangueras/tienda{PREF}/ con {len(paginas)} páginas → {z.name}")
    if sin_foto:
        print("Fotos provisionales (faltan las reales):", ", ".join(sin_foto))


if __name__ == "__main__":
    construir_todo(sys.argv[1] if len(sys.argv) > 1 else "https://filtrosparalavadoras.click")
