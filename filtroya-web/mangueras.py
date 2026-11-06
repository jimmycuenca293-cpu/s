#!/usr/bin/env python3
"""Tienda de mangueras para lavadoras Samsung y LG (desagüe, entrada de agua, tina-bomba, presostato, dispensador), con envío a toda Colombia.

Misma arquitectura que la tienda de filtros de pelusas (lavadoras.py): un dominio, una tienda por marca (/samsung/ y /lg/),
asesor por WhatsApp propio de cada marca, sin carrito ni pago en línea (pago contra entrega).
Genera sitios-mangueras/tienda/ y tienda-mangueras.zip.

Uso:  python3 mangueras.py [https://filtrosparalavadoras.click]   (por defecto ese dominio, en la carpeta /mangueras-para-lavadora/)

Fotos: imagenes-mangueras/<marca>/ (una por manguera, nombre en MARCAS[...]["productos"][...]["foto"]). Si falta una foto se genera una imagen
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

# ---------------------------------------------------------------- datos por marca
MARCAS = {
    "samsung": {
        "nombre": "Samsung", "clase": "samsung", "tema": "#071338", "whatsapp": "3054796329", "telefono": "305 479 6329",
        "tienda": "Mangueras para lavadora Samsung", "logo": "",
        "oficial": ("Samsung Colombia", "https://www.samsung.com/co/"),
        "codigos": "5E, SE o 5C",
        "familias": [("WA", "Carga superior", "carga-superior"), ("WW", "Carga frontal", "carga-frontal"), ("WF", "Carga frontal", "carga-frontal")],
        "productos": [
            {"id": "man-sam-1", "foto": "manguera-1.png", "slug": "manguera-de-desague-lavadora-samsung-desague-corrugada", "corto": "Manguera de desagüe", "ref": None, "precio": None,
             "tipo": "Corrugada con codo en la punta", "carga": None, "forma": "manguera de desagüe corrugada y flexible, con un codo en la punta para colgarla del desagüe de la pared"},
            {"id": "man-sam-2", "foto": "manguera-2.png", "slug": "manguera-de-desague-lavadora-samsung-desague-extension", "corto": "Manguera de desagüe", "ref": None, "precio": None,
             "tipo": "Extensión para alargar el desagüe", "carga": None, "forma": "manguera de desagüe corrugada para alargar la salida de la lavadora cuando el desagüe queda lejos"},
            {"id": "man-sam-3", "foto": "manguera-3.png", "slug": "manguera-de-entrada-de-agua-lavadora-samsung-entrada-tuercas", "corto": "Manguera de entrada de agua", "ref": None, "precio": None,
             "tipo": "Con tuercas en ambos extremos", "carga": None, "forma": "manguera de entrada de agua reforzada, con una tuerca en cada extremo: una para la llave y otra para la lavadora"},
            {"id": "man-sam-4", "foto": "manguera-4.png", "slug": "manguera-de-entrada-de-agua-lavadora-samsung-entrada-blanca-naranja", "corto": "Manguera de entrada de agua", "ref": None, "precio": None,
             "tipo": "Blanca con tuercas plásticas naranja", "carga": None, "forma": "manguera de entrada de agua blanca, reforzada, con tuercas plásticas de color naranja fáciles de apretar con la mano"},
            {"id": "man-sam-5", "foto": "manguera-5.png", "slug": "manguera-tina-bomba-lavadora-samsung-tina-bomba", "corto": "Manguera tina-bomba", "ref": None, "precio": None,
             "tipo": "De la tina a la bomba de desagüe", "carga": None, "forma": "manguera corta y gruesa que une la tina con la bomba de desagüe por dentro de la lavadora"},
            {"id": "man-sam-6", "foto": "manguera-6.png", "slug": "manguera-del-presostato-lavadora-samsung-presostato", "corto": "Manguera del presostato", "ref": None, "precio": None,
             "tipo": "Sensor de nivel de agua", "carga": None, "forma": "manguera delgada que lleva la presión de la tina al presostato, el sensor que le indica a la lavadora cuánta agua hay"},
            {"id": "man-sam-7", "foto": "manguera-7.png", "slug": "manguera-del-dispensador-lavadora-samsung-dispensador", "corto": "Manguera del dispensador", "ref": None, "precio": None,
             "tipo": "Caja de detergente y suavizante", "carga": None, "forma": "manguera que lleva el agua desde la válvula de entrada hasta la caja del detergente y el suavizante"},
            {"id": "man-sam-8", "foto": "manguera-8.png", "slug": "accesorios-manguera-lavadora-samsung-abrazaderas", "corto": "Abrazaderas y codo para manguera", "ref": None, "precio": None,
             "tipo": "Para sujetar mangueras y desagüe", "carga": None, "forma": "juego de abrazaderas y codo de desagüe para sujetar bien las mangueras de la lavadora y evitar goteos"},
            {"id": "man-sam-9", "foto": "manguera-9.png", "slug": "manguera-de-entrada-de-agua-lavadora-samsung-entrada-blanca-azul", "corto": "Manguera de entrada de agua", "ref": None, "precio": None,
             "tipo": "Blanca con tuerca plástica azul", "carga": None, "forma": "manguera de entrada de agua blanca, flexible, con una tuerca plástica azul de agarre fácil y un extremo recto"},
            {"id": "man-sam-10", "foto": "manguera-10.png", "slug": "manguera-de-desague-lavadora-samsung-desague-con-funda", "corto": "Manguera de desagüe", "ref": None, "precio": None,
             "tipo": "Corrugada gris con codo y funda protectora", "carga": None, "forma": "manguera de desagüe corrugada gris con codo en un extremo y una funda de espuma que protege la zona del doblez"},
        ],
    },
    "lg": {
        "nombre": "LG", "clase": "lg", "tema": "#a50034", "whatsapp": "3205102995", "telefono": "320 510 2995",
        "tienda": "Mangueras para lavadora LG", "logo": "",
        "oficial": ("LG Colombia", "https://www.lg.com/co/"),
        "codigos": "OE",
        "familias": [("WT", "Carga superior", "carga-superior"), ("WM", "Carga frontal", "carga-frontal"), ("WD", "Carga frontal", "carga-frontal")],
        "productos": [
            {"id": "man-lg-1", "foto": "manguera-1.png", "slug": "manguera-de-desague-lavadora-lg-desague-corrugada", "corto": "Manguera de desagüe", "ref": None, "precio": None,
             "tipo": "Corrugada con codo en la punta", "carga": None, "forma": "manguera de desagüe corrugada y flexible, con un codo en la punta para colgarla del desagüe de la pared"},
            {"id": "man-lg-2", "foto": "manguera-2.png", "slug": "manguera-de-desague-lavadora-lg-desague-extension", "corto": "Manguera de desagüe", "ref": None, "precio": None,
             "tipo": "Extensión para alargar el desagüe", "carga": None, "forma": "manguera de desagüe corrugada para alargar la salida de la lavadora cuando el desagüe queda lejos"},
            {"id": "man-lg-3", "foto": "manguera-3.png", "slug": "manguera-de-entrada-de-agua-lavadora-lg-entrada-tuercas", "corto": "Manguera de entrada de agua", "ref": None, "precio": None,
             "tipo": "Con tuercas en ambos extremos", "carga": None, "forma": "manguera de entrada de agua reforzada, con una tuerca en cada extremo: una para la llave y otra para la lavadora"},
            {"id": "man-lg-4", "foto": "manguera-4.png", "slug": "manguera-de-entrada-de-agua-lavadora-lg-entrada-blanca-naranja", "corto": "Manguera de entrada de agua", "ref": None, "precio": None,
             "tipo": "Blanca con tuercas plásticas naranja", "carga": None, "forma": "manguera de entrada de agua blanca, reforzada, con tuercas plásticas de color naranja fáciles de apretar con la mano"},
            {"id": "man-lg-5", "foto": "manguera-5.png", "slug": "manguera-tina-bomba-lavadora-lg-tina-bomba", "corto": "Manguera tina-bomba", "ref": None, "precio": None,
             "tipo": "De la tina a la bomba de desagüe", "carga": None, "forma": "manguera corta y gruesa que une la tina con la bomba de desagüe por dentro de la lavadora"},
            {"id": "man-lg-6", "foto": "manguera-6.png", "slug": "manguera-del-presostato-lavadora-lg-presostato", "corto": "Manguera del presostato", "ref": None, "precio": None,
             "tipo": "Sensor de nivel de agua", "carga": None, "forma": "manguera delgada que lleva la presión de la tina al presostato, el sensor que le indica a la lavadora cuánta agua hay"},
            {"id": "man-lg-7", "foto": "manguera-7.png", "slug": "manguera-del-dispensador-lavadora-lg-dispensador", "corto": "Manguera del dispensador", "ref": None, "precio": None,
             "tipo": "Caja de detergente y suavizante", "carga": None, "forma": "manguera que lleva el agua desde la válvula de entrada hasta la caja del detergente y el suavizante"},
            {"id": "man-lg-8", "foto": "manguera-8.png", "slug": "accesorios-manguera-lavadora-lg-abrazaderas", "corto": "Abrazaderas y codo para manguera", "ref": None, "precio": None,
             "tipo": "Para sujetar mangueras y desagüe", "carga": None, "forma": "juego de abrazaderas y codo de desagüe para sujetar bien las mangueras de la lavadora y evitar goteos"},
            {"id": "man-lg-9", "foto": "manguera-9.png", "slug": "manguera-de-entrada-de-agua-lavadora-lg-entrada-blanca-azul", "corto": "Manguera de entrada de agua", "ref": None, "precio": None,
             "tipo": "Blanca con tuerca plástica azul", "carga": None, "forma": "manguera de entrada de agua blanca, flexible, con una tuerca plástica azul de agarre fácil y un extremo recto"},
            {"id": "man-lg-10", "foto": "manguera-10.png", "slug": "manguera-de-desague-lavadora-lg-desague-con-funda", "corto": "Manguera de desagüe", "ref": None, "precio": None,
             "tipo": "Corrugada gris con codo y funda protectora", "carga": None, "forma": "manguera de desagüe corrugada gris con codo en un extremo y una funda de espuma que protege la zona del doblez"},
        ],
    },
}
L.MARCAS = MARCAS

# Palabras con las que la gente busca estas piezas (se usan en textos, descripciones y llms.txt)
SINONIMOS = ("manguera de la lavadora, manguera de desagüe, manguera de drenaje, manguera de entrada de agua, manguera de alimentación, manguera tina bomba, "
             "manguera del presostato, manguera del dispensador, manguera para lavadora")

INSTALACION = [
    "Desconecta la lavadora de la corriente y cierra la llave del agua. No trabajes con la máquina enchufada.",
    "Ten a mano una cubeta, trapos y una linterna: siempre sale algo de agua al soltar una manguera.",
    "Ubica la manguera: la de entrada va de la llave a la parte de atrás de la lavadora; la de desagüe sale por atrás hacia el desagüe de la pared; las internas (tina-bomba, presostato, dispensador) se ven al abrir el panel de atrás, el de arriba o el frontal inferior, según el modelo.",
    "Toma una foto de cómo está conectada antes de soltarla, para volver a ponerla igual.",
    "Suelta la abrazadera o la tuerca y retira la manguera vieja. Compárala con la nueva: deben coincidir en el largo, el diámetro y la forma de las puntas.",
    "Instala la manguera nueva. Las tuercas se aprietan con la mano y un cuarto de vuelta más; las abrazaderas, lo justo para que sellen. No fuerces.",
    "Abre el agua, conecta la lavadora y haz un ciclo corto mirando que no haya goteos en las uniones.",
]
NOTA_INSTALACION = ("Los pasos cambian según el modelo. Si tienes dudas con las mangueras internas o con la parte eléctrica, pídele ayuda a un técnico. "
                    "Y si tu modelo es distinto, escríbele al asesor por WhatsApp.")

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
        f = FOTOS / M["clase"] / p["foto"]
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


class SitioB(Sitio):
    """Igual que Sitio, pero la marca vive en /mangueras-para-lavadora/<marca>/."""
    def __init__(self, clave, dominio, out):
        super().__init__(clave, dominio, out)
        self.pref = PREF + "/" + clave
        self.dominio = dominio + self.pref
        self.raiz = dominio + PREF


# ---------------------------------------------------------------- bloques comunes
def bloque_importancia(n=""):
    return f'''<section class="m-sec lav-importancia"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Lo importante</span><h2>Las mangueras de tu lavadora {n}: cuáles son y para qué sirven</h2>
<p>Una lavadora usa varias mangueras, cada una con su trabajo. Cuando una falla, aparecen goteos, la máquina no llena, no desagua o muestra un error.</p></div>
<ul class="lav-puntos"><li><b>Manguera de entrada de agua.</b> Lleva el agua de la llave a la lavadora. Si se infla, se parte o se oxida, gotea o la máquina no llena. Es igual en todas las lavadoras.</li>
<li><b>Manguera de desagüe.</b> Saca el agua sucia hacia el desagüe de la pared. Si se dobla, se rompe o se tapa, la lavadora no desagua. Su medida cambia según el modelo.</li>
<li><b>Manguera tina-bomba.</b> Va por dentro: une la tina con la bomba de desagüe. Si se agrieta, aparecen fugas debajo de la máquina.</li>
<li><b>Manguera del presostato.</b> Lleva la presión de la tina al sensor de nivel. Si se suelta o se tapa, la lavadora llena de más o de menos.</li>
<li><b>Manguera del dispensador.</b> Lleva el agua a la caja del detergente y el suavizante. Si falla, la caja se desborda o no enjuaga.</li></ul>
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
    return '''<section class="m-confianza"><div class="m-wrap"><div><span class="ic">💵</span><span><b>Pago contra entrega</b><small>Pagas al recibir el paquete</small></span></div><div><span class="ic">🚚</span><span><b>Envío a toda Colombia</b><small>Con número de guía</small></span></div><div><span class="ic">💬</span><span><b>Asesor por WhatsApp</b><small>Te confirma el modelo</small></span></div><div><span class="ic">🔧</span><span><b>Cambio paso a paso</b><small>Guía de instalación</small></span></div></div></section>'''


def tres_pasos(n=""):
    return f'''<section class="m-sec"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Así de fácil</span><h2>Compra en 3 pasos</h2></div><div class="m-cols m-num"><div class="m-bloque"><h3>Escríbele al asesor</h3><p>Dile qué manguera necesitas (desagüe, entrada, tina-bomba…) y el modelo de tu lavadora {n}o mándale una foto de la manguera vieja.</p></div><div class="m-bloque"><h3>Confirma manguera y envío</h3><p>El asesor te dice cuál es, el valor y el tiempo de entrega a tu ciudad.</p></div><div class="m-bloque"><h3>Recibe y paga</h3><p>Llega a tu casa con número de guía y pagas contra entrega.</p></div></div></div></section>'''


def faq_general(S):
    n = S.M["nombre"]; c = S.M["codigos"]
    return [
        (f"¿Qué mangueras tiene una lavadora {n}?", f"Tiene la manguera de entrada de agua (de la llave a la máquina), la de desagüe (de la máquina al desagüe) y varias internas: tina-bomba, presostato y dispensador. En esta tienda las encuentras todas."),
        (f"¿Cómo sé si la manguera de mi lavadora {n} está dañada?", "Los signos más comunes son goteos en la llave o detrás de la lavadora, manguera inflada, partida o con la tuerca oxidada, desagüe lento y olor a humedad. Antes de cambiarla conviene revisar que no esté doblada ni tapada; el asesor te guía por WhatsApp."),
        (f"¿Cuál manguera necesita mi lavadora {n}?", "La de entrada de agua sirve para todas las lavadoras: solo eliges el largo. La de desagüe cambia de medida según la lavadora (las más largas son para carga frontal) y las internas dependen del modelo. Escríbele al asesor por WhatsApp con el modelo (está en una etiqueta atrás, en un costado o bajo la tapa) o con una foto de la manguera vieja y te confirma la correcta."),
        ("¿La manguera de entrada sirve para cualquier lavadora?", "Sí. La conexión de entrada de agua es la misma en todas las lavadoras, de cualquier marca y de carga superior o frontal. Lo que cambia es el largo que necesitas según dónde esté la llave."),
        ("¿La manguera de desagüe es igual para todas?", "No. La medida del desagüe cambia según la lavadora y las más largas se usan en las de carga frontal. El asesor te confirma cuál necesitas con el modelo."),
        (f"¿Qué código de error puede avisar un problema de manguera en {n}?", f"Depende del modelo; en {n} los de desagüe más comunes son {c}. Un código de desagüe o de nivel de agua puede venir de una manguera doblada, tapada o suelta. Mándale al asesor una foto del código y el modelo."),
        ("¿Cuánto cuesta?", "El precio depende de la clase de manguera y del modelo. Pregúntale al asesor por WhatsApp y te responde en el momento con el valor y el tiempo de entrega a tu ciudad."),
        ("¿Hacen envíos a toda Colombia?", "Sí. Enviamos por transportadora a todo el país y te mandamos el número de guía."),
        ("¿Puedo cambiarla yo mismo?", "Las mangueras de entrada y de desagüe, sí, con algo de práctica: se sueltan con la mano o con una abrazadera. Hay que desconectar la lavadora y cerrar el agua. Abajo está el paso a paso; las mangueras internas, si prefieres, que las cambie un técnico."),
        ("¿Cómo pago?", "Con pago contra entrega: pagas cuando recibes el paquete. El asesor te confirma si está disponible en tu ciudad."),
    ]


# ---------------------------------------------------------------- páginas
def tarjetas(S, solo=None):
    M = S.M; t = ""
    for p in M["productos"]:
        pr = f'<span class="pr">{cop(p["precio"])}<small>Confirma envío con el asesor</small></span>' if p["precio"] else '<span class="pr consulta">Consulta el precio<small>Te responde el asesor</small></span>'
        t += (f'<article class="m-card"><span class="m-tipo">{esc(p["tipo"])}</span><span class="im">{foto_html(p)}</span><div class="tx">'
              f'<h3><a href="/{p["slug"]}/">{esc(p["nombre"])}</a></h3>{pr}'
              + S.boton_asesor(f"Hola, quiero consultar por la {p['nombre']}", "m-btn block wa", "💬 Preguntar al asesor")
              + f'<a class="m-link" href="/{p["slug"]}/">Ver detalles</a></div></article>')
    return t


def pagina_inicio(S):
    M = S.M; n = M["nombre"]
    faq = faq_general(S)
    fam = chips([(f"Lavadora {n} {f[0]} ({f[1].lower()})", f"/manguera-lavadora-{S.clave}-modelo-{f[0].lower()}/") for f in M["familias"]])
    cuerpo = f'''<section class="m-hero"><div class="m-wrap">
  <div>
    <h1>Mangueras para lavadora {n}</h1>
    <p class="lead">Manguera de desagüe, de entrada de agua, tina-bomba, del presostato y del dispensador para lavadoras {n} de carga superior y de carga frontal. La de entrada sirve para todas las lavadoras; para la de desagüe dile tu modelo al asesor por WhatsApp y te confirmamos el largo. Enviamos a toda Colombia con pago contra entrega.</p>
    <div class="acc">{S.boton_asesor(f"Hola, necesito una manguera para mi lavadora {n}")}<a class="m-btn sec" href="#mangueras">Ver las mangueras</a></div>
    <ul><li>Pago contra entrega</li><li>Envío a toda Colombia</li><li>Asesor que te confirma la manguera</li></ul>
  </div>
  <div class="lav-fotos">{"".join(f'<span class="lf">{foto_html(p, lazy=i>0)}</span>' for i, p in enumerate(M["productos"][:3]))}</div>
</div></section>
{confianza()}
<section class="m-sec" id="mangueras"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Catálogo {n}</span><h2>Mangueras para lavadora {n}</h2><p>Escoge la clase de manguera que necesitas. El asesor confirma la medida y la referencia con tu modelo antes de la compra.</p></div><div class="m-grid">{tarjetas(S)}</div></div></section>
<section class="m-sec alt"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Encuentra la tuya</span><h2>¿Qué manguera necesita mi lavadora {n}?</h2></div>
<div class="m-cols"><div><h3>Manguera de desagüe</h3><p>Es la que saca el agua sucia hacia el desagüe. Si la lavadora no desagua o hay olor a humedad, empieza por ahí.</p><p><a class="m-link" href="/manguera-de-desague-lavadora-{S.clave}/">Mangueras de desagüe →</a></p></div>
<div><h3>Manguera de entrada de agua</h3><p>Va de la llave a la lavadora. Si gotea en la llave o la máquina llena lento, revisa esta.</p><p><a class="m-link" href="/manguera-de-entrada-lavadora-{S.clave}/">Mangueras de entrada →</a></p></div>
<div><h3>Mangueras internas</h3><p>La tina-bomba, la del presostato y la del dispensador van por dentro de la lavadora. Se cambian al abrir el panel.</p><p><a class="m-link" href="/manguera-tina-bomba-lavadora-{S.clave}/">Manguera tina-bomba →</a></p></div></div>
<h3 style="margin-top:18px">Busca por familia de modelo</h3>{fam}
<p style="margin-top:14px"><a class="m-btn" href="/cual-es-mi-manguera/">Guía: cuál es mi manguera</a></p></div></section>
{bloque_importancia(n)}
<section class="m-sec alt"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Señales</span><h2>Cuándo hay que cambiar una manguera de la lavadora {n}</h2></div><ul class="lav-puntos">{"".join(f"<li>{esc(s)}</li>" for s in SINTOMAS)}</ul>
<p>Antes de comprar, descarta lo básico: que la manguera no esté doblada o aplastada contra la pared, que la tuerca esté bien apretada y que el filtro de entrada de la llave esté limpio. Si nada de eso es, la manguera es la sospechosa.</p>
<p><a class="m-btn sec" href="/lavadora-{S.clave}-gotea-agua-por-la-manguera/">Lavadora {n} gotea: qué revisar</a></p></div></section>
{bloque_entrega()}
{tres_pasos(n + " ")}
<section class="m-sec"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Mantenimiento</span><h2>Cómo cambiar una manguera de tu lavadora {n}</h2></div>
<div class="m-texto"><p>Cambiar una manguera de entrada o de desagüe es una tarea sencilla: se desconecta la lavadora, se cierra el agua, se suelta la manguera vieja y se pone la nueva. Tenemos el paso a paso con las precauciones.</p>
<p><a class="m-btn sec" href="/cambio-e-instalacion/">Paso a paso para cambiar la manguera</a></p></div></div></section>
<section class="m-sec alt" id="preguntas"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Resolvemos tus dudas</span><h2>Preguntas frecuentes sobre las mangueras de la lavadora {n}</h2></div>{faq_html(faq)}</div></section>
<section class="m-sec"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Envíos</span><h2>Enviamos mangueras para lavadora {n} a toda Colombia</h2><p>Escoge tu ciudad para ver el tiempo de entrega y hablar con el asesor.</p></div>{chips(S.chips_ciudad[:24])}<p><a href="/mangueras-lavadora-{S.clave}-por-ciudad/">Ver todas las ciudades →</a></p></div></section>
<section class="m-sec alt"><div class="m-wrap"><div class="m-cta"><div><h2>¿No sabes cuál manguera necesitas?</h2><p>Mándanos una foto de la manguera vieja o de la etiqueta con el modelo de tu lavadora por WhatsApp.</p></div>{S.boton_asesor(f"Hola, necesito una manguera para mi lavadora {n}")}</div></div></section>
{S.barra(f"Hola, necesito una manguera para mi lavadora {n}")}'''
    ld = [{"@type": "CollectionPage", "name": f"Mangueras para lavadora {n}", "url": S.dominio + "/", "description": f"Mangueras de desagüe, entrada de agua, tina-bomba, presostato y dispensador para lavadoras {n} en Colombia."},
          {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i, "url": S.dominio + f"/{p['slug']}/", "name": p["nombre"]} for i, p in enumerate(M["productos"], 1)]},
          faq_ld(faq)]
    S.pagina("/", f"Mangueras para lavadora {n} | Envío a toda Colombia", f"Mangueras de desagüe, de entrada de agua y tina-bomba para lavadoras {n}. Pregunta al asesor por WhatsApp, paga contra entrega y recibe en toda Colombia.", cuerpo, ld, "1.0",
             f'<meta property="og:image" content="{S.raiz}/img/{M["productos"][0]["id"]}.jpg">')


def corta(t, n=66):
    if len(t) <= n: return t
    return t[:n].rsplit(" ", 1)[0].rstrip(" ,;:|-")


def pagina_producto(S, p):
    M = S.M; n = M["nombre"]
    otros = [(f"{q['nombre']}", f"/{q['slug']}/") for q in M["productos"] if q is not p]
    faq = [(f"¿Esta manguera sirve para mi lavadora {n}?", f"Escríbele al asesor por WhatsApp con el modelo de tu lavadora (está en la etiqueta) o una foto de la manguera vieja y te confirmamos el largo y el tipo antes de que compres."),
           ("¿Cuánto cuesta?", "Pregunta al asesor por WhatsApp: te da el precio y el tiempo de entrega a tu ciudad."),
           ("¿Cómo la cambio?", "Desconectas la lavadora, cierras el agua, sueltas la tuerca o la abrazadera de la manguera vieja y pones la nueva igual. Abajo está el paso a paso."),
           (f"¿Cómo sé que la manguera de mi lavadora {n} es la que falla?", "Si hay goteo en la unión, la manguera está inflada o partida, o la lavadora no desagua ni llena y ya revisaste que no esté doblada ni tapada, lo más probable es la manguera. El asesor te ayuda a confirmarlo.")]
    entrada = "entrada" in p["slug"]; desague = "desague" in p["slug"]
    if entrada:
        aviso_t, aviso_x = "Sirve para todas las lavadoras", f"La conexión de entrada de agua es la misma en todas las lavadoras {n} y de otras marcas. Solo te confirmamos el largo que necesitas por WhatsApp."
        faq[0] = (f"¿Esta manguera sirve para mi lavadora {n}?", "Sí. La entrada de agua es del mismo tamaño en todas las lavadoras, de carga superior o frontal, así que esta manguera sirve para la tuya. Lo único que se elige es el largo: escríbele al asesor y te lo confirma.")
    elif desague:
        aviso_t, aviso_x = "La medida del desagüe cambia", f"Las mangueras de desagüe no son iguales en todas las lavadoras: las más largas son para las de carga frontal. Dile al asesor el modelo de tu lavadora y te confirma el largo."
    else:
        aviso_t, aviso_x = "¿Sirve para tu lavadora?", "Antes de comprar, el asesor confirma contigo el largo y el tipo. Mándale la etiqueta con el modelo o una foto de la manguera vieja."
    precio = (f'<span class="precio">{cop(p["precio"])}<small>Confirma disponibilidad y envío con el asesor</small></span>' if p["precio"]
              else '<span class="precio consulta">Precio: pregúntale al asesor<small>Respuesta en el momento por WhatsApp</small></span>')
    cuerpo = f'''<div class="m-wrap">{S.miga((p["nombre"], None))}
<div class="m-prod">
  <div class="foto"><span class="m-badge">{esc(p["tipo"])}</span>{foto_html(p, True, False)}</div>
  <div class="info">
    <h1>{esc(p["nombre"])}</h1>
    <span class="sub">Lavadora {n} · {esc(p["tipo"])}</span>
    {precio}
    <div class="m-aviso"><span style="font-size:22px">💬</span><span><b>{aviso_t}</b>{aviso_x}</span></div>
    {S.boton_asesor(f"Hola, quiero consultar por la {p['nombre']}", "m-btn block wa", "💬 Pedir o preguntar al asesor por WhatsApp")}
    <ul class="m-ok"><li><b>Envío a toda Colombia</b> por transportadora, con número de guía.</li><li><b>Guía de cambio</b> paso a paso incluida en esta página.</li><li><b>Pago contra entrega</b>: pagas cuando recibes el paquete (el asesor confirma si aplica en tu ciudad).</li></ul>
  </div>
</div></div>
<section class="m-sec alt"><div class="m-wrap"><div class="m-texto"><div class="m-cab"><span class="eyebrow">Descripción</span><h2>{esc(p["nombre"])}</h2></div>
<p>Es una {esc(p["forma"])}. En la lavadora se conoce como «{esc(p["corto"].lower())}» y cumple una función concreta dentro del circuito del agua.</p>
<p>Si tu lavadora {n} gotea, no llena, no desagua o muestra un código de error de agua o de desagüe ({M["codigos"]}), una manguera en mal estado es de las primeras cosas que se revisan. Para estar seguros de que es la que necesita tu lavadora, el asesor revisa el modelo contigo por WhatsApp.</p></div></div></section>
<section class="m-sec"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Datos</span><h2>Ficha del producto</h2></div><dl class="m-ficha"><dt>Marca de la lavadora</dt><dd>{n}</dd><dt>Clase de manguera</dt><dd>{esc(p["corto"])}</dd><dt>Tipo</dt><dd>{esc(p["tipo"])}</dd><dt>Referencia y medida</dt><dd>{esc(p["ref"]) if p["ref"] else "Te las confirma el asesor según el modelo"}</dd><dt>Envío</dt><dd>Toda Colombia, por transportadora</dd></dl></div></section>
{bloque_importancia(n)}
{bloque_entrega()}
<section class="m-sec alt"><div class="m-wrap"><section class="caja tutorial" id="instalacion"><h2>Cómo cambiar una manguera de tu lavadora {n}: paso a paso</h2><ol class="pasos">{"".join(f"<li>{esc(x)}</li>" for x in INSTALACION)}</ol><p class="m-mut">{esc(NOTA_INSTALACION)}</p></section></div></section>
<section class="m-sec"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Preguntas</span><h2>Preguntas frecuentes</h2></div>{faq_html(faq)}</div></section>
{('<section class="m-sec alt"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Más mangueras</span><h2>Otras mangueras para lavadora ' + n + '</h2></div>' + chips(otros) + '</div></section>') if otros else ""}
{S.barra(f"Hola, quiero consultar por la {p['nombre']}")}'''
    prod = {"@type": "Product", "name": p["nombre"], "image": f"{S.raiz}/img/{p['id']}.jpg", "brand": {"@type": "Brand", "name": n}, "category": "Repuestos para lavadoras",
            "description": f"{p['corto']} para lavadora {n}: {p['tipo'].lower()}. Envío a toda Colombia.", "areaServed": "CO"}
    if p["ref"]: prod["mpn"] = p["ref"]
    if p["precio"]:
        prod["offers"] = {"@type": "Offer", "priceCurrency": "COP", "price": p["precio"], "availability": "https://schema.org/InStock", "url": f"{S.dominio}/{p['slug']}/"}
    S.pagina(f"/{p['slug']}/", corta(f"{p['corto']} lavadora {n}: {p['tipo'].lower()}") if len(f"{p['corto']} lavadora {n}: {p['tipo'].lower()}") <= 66 else corta(f"{p['corto']} para lavadora {n} | Pago contra entrega"), f"{p['corto']} para lavadora {n}: {p['tipo'].lower()}. Pregunta al asesor por WhatsApp el precio y recibe en toda Colombia.", cuerpo,
             [prod, faq_ld(faq), HowTo(S, p), S.breadcrumb((p["nombre"], None))], "0.9", f'<link rel="preload" as="image" href="/img/{p["id"]}.webp"><meta property="og:image" content="{S.raiz}/img/{p["id"]}.jpg">')


def HowTo(S, p):
    return {"@type": "HowTo", "name": f"Cómo cambiar una manguera de una lavadora {S.M['nombre']}", "step": [{"@type": "HowToStep", "position": i, "text": t} for i, t in enumerate(INSTALACION, 1)]}


def pagina_guia(S, ruta, titulo, desc, h1, cuerpo_html, faq=None):
    n = S.M["nombre"]
    cuerpo = f'<div class="m-wrap">{S.miga((h1, None))}<div class="m-texto"><h1>{esc(h1)}</h1>{cuerpo_html}</div>' \
             f'<div class="m-cta" style="margin:24px 0"><div><h2>¿Quieres la manguera correcta?</h2><p>Escríbele al asesor por WhatsApp con el modelo de tu lavadora.</p></div>{S.boton_asesor(f"Hola, tengo una pregunta sobre las mangueras de mi lavadora {n}")}</div>' \
             + (f'<h2>Preguntas frecuentes</h2>{faq_html(faq)}' if faq else "") + "</div>"
    ld = [S.breadcrumb((h1, None))] + ([faq_ld(faq)] if faq else [])
    S.pagina(ruta, titulo, desc, cuerpo, ld, "0.8")


def guias(S):
    M = S.M; n = M["nombre"]; c = M["codigos"]
    cat = chips([(p["nombre"], f"/{p['slug']}/") for p in M["productos"]])
    def clase(*claves): return chips([(p["nombre"], f"/{p['slug']}/") for p in M["productos"] if any(k in p["id"] or k in p["slug"] for k in claves)] or [(p["nombre"], f"/{p['slug']}/") for p in M["productos"]])
    G = lambda *a, **k: pagina_guia(S, *a, **k)
    G("/cual-es-mi-manguera/", f"¿Cuál manguera necesita mi lavadora {n}? Guía", f"Cómo saber qué manguera necesita tu lavadora {n}: entrada, desagüe, tina-bomba, presostato o dispensador, y cómo medirla.",
      f"¿Cuál manguera necesita mi lavadora {n}?",
      f'<p>Para escoger bien mira tres cosas: cuál manguera falla, el modelo exacto de la lavadora y cómo es la manguera vieja.</p><h2>1. Cuál manguera es</h2><ul><li><b>Entrada de agua:</b> la que va de la llave a la parte de atrás de la lavadora. Sirve para todas las lavadoras: solo eliges el largo.</li><li><b>Desagüe:</b> la que sale por atrás hacia el desagüe de la pared. Su medida cambia según la lavadora; las más largas son para carga frontal.</li><li><b>Tina-bomba, presostato y dispensador:</b> mangueras internas que se ven al abrir la lavadora.</li></ul>{cat}'
      f'<h2>2. El modelo de la lavadora</h2><p>Está en una etiqueta en la parte de atrás, en un costado o bajo la tapa. En {n} los modelos empiezan por {", ".join(f[0] for f in M["familias"])}. Con el modelo, el asesor te confirma la manguera por WhatsApp.</p>'
      f'<h2>3. La manguera vieja</h2><p>Compárala por el largo, el diámetro y la forma de las puntas (tuerca, codo o abrazadera). Una foto al asesor ayuda a confirmarla.</p>', faq_general(S)[2:4])
    G("/como-saber-si-la-manguera-esta-danada/", f"Cómo saber si una manguera de la lavadora {n} está dañada", f"Señales de que una manguera de tu lavadora {n} falla y qué revisar antes de comprar una nueva.",
      f"Cómo saber si una manguera de la lavadora {n} está dañada",
      "<p>Las mangueras se desgastan con el tiempo, el sol, la presión del agua y la cal. Estas son las señales más comunes:</p><ul>" + "".join(f"<li>{esc(s)}</li>" for s in SINTOMAS) + "</ul>"
      "<h2>Antes de cambiarla, revisa esto</h2><ol class='pasos'><li>Desconecta la lavadora y revisa que las mangueras no estén dobladas ni aplastadas contra la pared.</li><li>Mira las tuercas y las uniones: si hay humedad o sarro, hay fuga.</li><li>Pasa la mano por la manguera de entrada: si se siente inflada, blanda o con grietas, cámbiala.</li><li>Limpia el filtro de malla de la entrada (va en la punta de la manguera, junto a la llave).</li></ol>"
      "<p>Si después de esto sigue igual, escríbele al asesor: con el modelo de tu lavadora te confirma la manguera que necesitas.</p>", faq_general(S)[1:2])
    G("/cambio-e-instalacion/", f"Cómo cambiar una manguera de la lavadora {n}: paso a paso", f"Paso a paso para cambiar la manguera de entrada, de desagüe o una interna de una lavadora {n}, con precauciones.",
      f"Cómo cambiar una manguera de la lavadora {n}",
      "<ol class='pasos'>" + "".join(f"<li>{esc(x)}</li>" for x in INSTALACION) + f"</ol><p class='m-mut'>{esc(NOTA_INSTALACION)}</p>", faq_general(S)[6:7])
    G(f"/lavadora-{S.clave}-gotea-agua-por-la-manguera/", f"Lavadora {n} gotea agua: causas y qué manguera revisar", f"Por qué una lavadora {n} gotea o deja un charco, qué revisar (llave, tuercas, mangueras) y cuándo cambiar la manguera.",
      f"Lavadora {n} gotea agua",
      "<p>Cuando la lavadora gotea, casi siempre el culpable es una manguera o una unión. Estas son las causas, de la más fácil a la más seria:</p>"
      "<h2>Qué revisar, en orden</h2><ol class='pasos'><li><b>Tuerca floja en la llave o en la lavadora.</b> Apriétala con la mano y un cuarto de vuelta más.</li><li><b>Empaque de goma de la tuerca</b> (la arandela) gastado o ausente: cámbialo.</li><li><b>Manguera de entrada inflada, partida o resecada.</b> Hay que cambiarla.</li><li><b>Manguera de desagüe suelta del desagüe de la pared</b> o con un agujero.</li><li><b>Manguera interna agrietada</b> (tina-bomba, dispensador). Lo confirma al abrir el panel.</li></ol>"
      "<p>Seguridad: cierra la llave y desconecta la lavadora antes de meter la mano.</p>" + cat, faq_general(S)[0:2])
    G(f"/lavadora-{S.clave}-no-desagua/", f"Lavadora {n} no desagua: causas y mangueras a revisar", f"Por qué una lavadora {n} no desagua, qué revisar (manguera de desagüe, filtro, bomba) y cuándo cambiar la manguera.",
      f"Lavadora {n} no desagua",
      "<p>Cuando una lavadora no desagua, el agua se queda en la tina y el ciclo se detiene. Estas son las causas, de la más fácil a la más seria:</p>"
      "<h2>Qué revisar, en orden</h2><ol class='pasos'><li><b>Manguera de desagüe doblada o aplastada</b> contra la pared o el mueble.</li><li><b>Manguera de desagüe tapada</b> con pelusa o jabón: se desconecta y se enjuaga.</li><li><b>Desagüe de la pared obstruido</b> o con la manguera metida hasta el fondo.</li><li><b>Filtro de desagüe tapado</b> (en carga frontal, abajo).</li><li><b>Manguera tina-bomba agrietada o suelta</b> por dentro, o bomba atascada: lo confirma un técnico.</li></ol>"
      "<p>Seguridad: desconecta la lavadora antes de meter la mano, y ten una cubeta para el agua que quede en la tina.</p>" + clase("desague","tina"), faq_general(S)[0:2])
    G(f"/lavadora-{S.clave}-no-llena-de-agua/", f"Lavadora {n} no llena de agua: mangueras a revisar", f"Por qué una lavadora {n} no llena de agua o llena muy lento y qué manguera de entrada revisar.",
      f"Lavadora {n} no llena de agua",
      "<p>Si la lavadora no llena o llena muy despacio, el problema suele estar antes de la máquina o en las mangueras de entrada.</p><h2>Revisa</h2><ol class='pasos'><li>Que la llave del agua esté bien abierta.</li><li>Que la manguera de entrada no esté doblada ni aplastada.</li><li>El filtro de malla de la punta de la manguera: si está tapado con sarro o arena, límpialo.</li><li>La manguera del presostato (sensor de nivel): si está suelta o tapada, la lavadora llena de más o de menos.</li><li>Si todo esto está bien, puede ser la válvula de entrada: la revisa un técnico.</li></ol>" + clase("entrada","presostato"))
    G(f"/codigo-error-desague-lavadora-{S.clave}/", f"Código de error de desagüe en lavadora {n} ({c})", f"Qué significan los códigos de desagüe de las lavadoras {n} ({c}) y cuándo apuntan a una manguera doblada, tapada o suelta.",
      f"Código de error de desagüe en lavadora {n} ({c})",
      f"<p>En las lavadoras {n} los códigos de error de desagüe más habituales son <b>{c}</b>. Indican que la máquina no logra sacar el agua en el tiempo esperado.</p><h2>Qué hacer</h2><ol class='pasos'><li>Desconecta la lavadora unos minutos y vuelve a encenderla.</li><li>Revisa que la manguera de desagüe no esté doblada, tapada ni metida hasta el fondo del desagüe.</li><li>Limpia el filtro de desagüe.</li><li>Si el código vuelve, la causa probable es una manguera interna (tina-bomba) o la bomba.</li></ol><p>El significado exacto depende del modelo; mándale al asesor el código y el modelo.</p>")
    G(f"/cuanto-cuesta-manguera-lavadora-{S.clave}/", f"Cuánto cuesta una manguera para lavadora {n}", f"De qué depende el precio de una manguera para lavadora {n} y cómo consultarlo con el asesor.",
      f"Cuánto cuesta una manguera para lavadora {n}",
      "<p>El precio depende de la clase de manguera (entrada, desagüe o interna), del largo y de la ciudad de envío. Por eso no mostramos un valor único: el asesor te lo da en el momento por WhatsApp.</p><h2>Qué mandarle</h2><ul><li>Cuál manguera necesitas y el modelo de tu lavadora (etiqueta).</li><li>Una foto de la manguera vieja, si ya la sacaste.</li><li>Tu ciudad.</li></ul>" + cat)
    G(f"/manguera-de-desague-o-de-entrada-lavadora-{S.clave}/", f"Manguera de desagüe o de entrada de lavadora {n}", f"Cuál es la diferencia entre la manguera de desagüe y la de entrada de agua de una lavadora {n} y cuál necesitas.",
      f"Manguera de desagüe o de entrada de la lavadora {n}: ¿cuál es cuál?",
      f"<p>Son dos mangueras distintas y no se pueden cambiar entre sí.</p><ul><li><b>Manguera de entrada de agua:</b> trae agua a presión desde la llave. Es reforzada y lleva una tuerca en cada punta.</li><li><b>Manguera de desagüe:</b> saca el agua sucia por gravedad. Es corrugada, más ancha y flexible, y suele terminar en un codo.</li></ul><p>Si tu lavadora {n} gotea en la llave o llena lento, mira la de entrada. Si no desagua o huele a humedad, mira la de desagüe.</p>{cat}")
    for slg, titulo, tipo, intro, claves in [("manguera-de-desague-lavadora", "Manguera de desagüe", "desagüe", "La manguera de desagüe saca el agua sucia de la lavadora hacia el desagüe de la pared. Es corrugada y flexible; si se dobla, se rompe o se tapa, la lavadora no desagua.", ("desague",)),
                                            ("manguera-de-entrada-lavadora", "Manguera de entrada de agua", "entrada de agua", "La manguera de entrada trae el agua de la llave a la lavadora. Es reforzada y lleva tuercas en los extremos; con el tiempo se infla, se reseca o se oxida y empieza a gotear.", ("entrada",)),
                                            ("manguera-tina-bomba-lavadora", "Manguera tina-bomba", "tina-bomba", "La manguera tina-bomba va por dentro de la lavadora y une la tina con la bomba de desagüe. Si se agrieta o se suelta, hay fugas debajo de la máquina o no desagua.", ("tina",))]:
        G(f"/{slg}-{S.clave}/", f"{titulo} para lavadora {n}", f"{titulo} para lavadoras {n}: qué hace, cómo saber si falla y cómo pedirla por WhatsApp con envío a toda Colombia.",
          f"{titulo} para lavadora {n}",
          f"<p>{intro}</p><p>Cada modelo {n} usa medidas distintas, así que conviene confirmar la referencia con el modelo de tu lavadora antes de comprar.</p>" + clase(*claves))
    for pref, tipo, slg in M["familias"]:
        G(f"/manguera-lavadora-{S.clave}-modelo-{pref.lower()}/", f"Mangueras para lavadora {n} {pref} ({tipo.lower()})", f"Mangueras de desagüe, entrada y tina-bomba para lavadoras {n} de la familia {pref}: {tipo.lower()}. El asesor confirma la referencia con tu modelo exacto.",
          f"Mangueras para lavadora {n} modelo {pref}",
          f"<p>Los modelos de lavadora {n} que empiezan por <b>{pref}</b> suelen ser de {tipo.lower()}. Cada modelo puede usar mangueras de distinto largo y forma, así que la referencia exacta se confirma con el modelo completo (por ejemplo, {pref}… y los números y letras que siguen) que aparece en la etiqueta.</p>"
          f"<p>Mándale al asesor el modelo completo por WhatsApp y te confirma la manguera, el precio y el envío.</p>" + cat)


def paginas_ciudad(S):
    M = S.M; n = M["nombre"]
    for c in S.ciudades:
        ciudad, depto = c[0], c[1]
        ruta = f"/manguera-lavadora-{S.clave}-{slug(ciudad)}/"
        h1 = f"Mangueras para lavadora {n} en {ciudad}"
        faq = [(f"¿Envían mangueras para lavadora {n} a {ciudad}?", f"Sí. Enviamos por transportadora a {ciudad} ({depto}) y te mandamos el número de guía. Pregunta al asesor por el tiempo de entrega y si hay pago contra entrega en tu ciudad."),
               ("¿Cómo sé cuál manguera necesito?", "Mándale al asesor el modelo de tu lavadora o una foto de la manguera vieja por WhatsApp.")]
        cuerpo = f'''<div class="m-wrap">{S.miga((f"Lavadoras {n} en {ciudad}", None))}<div class="m-texto"><h1>{esc(h1)}</h1>
<p>Si tu lavadora {n} en {esc(ciudad)}, {esc(depto)}, gotea, no desagua o no llena, aquí encuentras la manguera que necesita: desagüe, entrada de agua, tina-bomba, presostato o dispensador. La enviamos por transportadora y el asesor te confirma la correcta antes de comprar.</p>
{chips([(p["nombre"], f"/{p['slug']}/") for p in M["productos"]])}
<p style="margin-top:16px">{S.boton_asesor(f"Hola, soy de {ciudad} y necesito una manguera para mi lavadora {n}")}</p>
<h2>Preguntas frecuentes</h2>{faq_html(faq)}<p><a href="/mangueras-lavadora-{S.clave}-por-ciudad/">Ver todas las ciudades →</a></p></div></div>
{bloque_entrega()}
{S.barra(f"Hola, soy de {ciudad} y necesito una manguera para mi lavadora {n}")}'''
        S.pagina(ruta, corta(f"{h1} | Envío por transportadora") if len(f"{h1} | Envío por transportadora") <= 66 else corta(h1), f"Mangueras para lavadora {n} en {ciudad}, {depto}: desagüe, entrada y tina-bomba. Pregunta al asesor por WhatsApp y recibe en tu ciudad.", cuerpo,
                 [faq_ld(faq), S.breadcrumb((f"Lavadoras {n} en {ciudad}", None))], "0.6")
    cuerpo = f'<div class="m-wrap">{S.miga(("Ciudades", None))}<div class="m-texto"><h1>Mangueras para lavadora {n} en toda Colombia</h1><p>Elige tu ciudad.</p>{chips(S.chips_ciudad)}</div></div>'
    S.pagina(f"/mangueras-lavadora-{S.clave}-por-ciudad/", f"Mangueras para lavadora {n} por ciudad", f"Envíos de mangueras para lavadora {n} a {len(S.ciudades)} ciudades de Colombia: elige la tuya y pregunta al asesor por WhatsApp.", cuerpo, [S.breadcrumb(("Ciudades", None))], "0.7")


# ---------------------------------------------------------------- legales, textos y portada
REEMPLAZOS = [("distribuidor autorizado", "vendedor"), ("Distribuidor autorizado", "Vendedor"), (" con autorización", ""),
              ("del nevecón", "de la lavadora"), ("al nevecón", "a la lavadora"), ("el nevecón", "la lavadora"), ("un nevecón", "una lavadora"), ("los nevecones", "las lavadoras"),
              ("nevecones", "lavadoras"), ("Nevecones", "Lavadoras"), ("nevecón", "lavadora"), ("Nevecón", "Lavadora"), ("nevecon", "lavadora"),
              ("las neveras", "las lavadoras"), ("neveras", "lavadoras"), ("nevera", "lavadora"), ("filtros de agua", "mangueras para lavadora"), ("Filtros de agua", "Mangueras para lavadora"),
              ("filtro de agua", "manguera"), ("Filtro de agua", "Manguera")]
L.REEMPLAZOS = REEMPLAZOS
L.QUIENES = """<?php $MARCA = 'home'; require __DIR__ . '/lav.php';
$n = sitio()['negocio'];
lav_cabeza('Quiénes somos | ' . $n['nombre'], 'Somos un comercio colombiano de mangueras para lavadoras Samsung y LG (desagüe, entrada de agua, tina-bomba), con asesoría por WhatsApp y envíos a todo el país.', '/quienes-somos.php', '', '')
?>
<div class="m-wrap"><div class="m-texto"><h1>Quiénes somos</h1>
<p><?= h($n['nombre']) ?> es un comercio colombiano de mangueras para lavadoras: de desagüe, de entrada de agua, tina-bomba, del presostato y del dispensador. Te ayudamos a encontrar la manguera que necesita tu lavadora y te la enviamos a donde estés.</p>
<p>Antes de que compres, un asesor revisa contigo cuál manguera necesitas y el modelo de tu lavadora por WhatsApp, para que pidas la correcta.</p>
<p>Atendemos <?= h($n['horario']) ?>. Escríbenos por WhatsApp: __TELEFONOS__ o al correo <?= h($n['correo']) ?>.</p>
<p><?= h($n['nombre']) ?> · <?= h($n['titular']) ?> · <?= h($n['documento']) ?></p></div></div>
<?php lav_pie(); ?>
"""
L.LEGALES = {
    "terminos": ("Términos y condiciones", """<p>Este sitio presenta mangueras para lavadoras (de desagüe, de entrada de agua, tina-bomba, presostato y dispensador). No tiene carrito ni pago en línea: los pedidos se hacen por WhatsApp con un asesor y se pagan contra entrega.</p>
<h2>Cómo se hace un pedido</h2><p>Escribe al asesor por WhatsApp con la clase de manguera y el modelo de tu lavadora, o una foto de la manguera vieja. El asesor te confirma la manguera, el precio, el valor del envío y si hay pago contra entrega en tu ciudad antes de despachar.</p>
<h2>Confirma antes de comprar</h2><p>Las fotos son de referencia. Antes de pagar, compara la manguera con la que tienes o confirma el modelo de tu lavadora con el asesor. La instalación es responsabilidad del comprador; si no tienes experiencia con las partes internas de la lavadora, pídele ayuda a un técnico.</p>
<h2>Marcas</h2><p>Los nombres de marca se usan solo para indicar el tipo de lavadora. Somos un comercio independiente.</p>"""),
    "privacidad": ("Tratamiento de datos personales", """<p>Cuando nos escribes por WhatsApp usamos tu nombre, tu número y los datos que nos des (ciudad, dirección, modelo de la lavadora) solo para atender tu consulta, confirmar tu pedido y enviártelo.</p>
<p>No vendemos tus datos. Puedes pedirnos que los corrijamos o los eliminemos escribiéndonos por WhatsApp o al correo de contacto.</p>
<p>Este sitio puede usar herramientas de medición (como Google Analytics) para saber cuántas personas lo visitan.</p>"""),
    "garantia-y-retracto": ("Garantía y retracto", """<p>Si la manguera llega con algún defecto, escríbenos por WhatsApp con una foto y la revisamos.</p>
<p>Para compras a distancia puedes ejercer el derecho de retracto dentro de los 5 días hábiles siguientes a la entrega, según la ley colombiana, siempre que el producto no haya sido instalado ni usado y esté en buen estado. Coordina la devolución con el asesor.</p>
<p>Autoridad de protección al consumidor: <a href="https://www.sic.gov.co/" target="_blank" rel="noopener">Superintendencia de Industria y Comercio</a>.</p>"""),
}

HOME_FAQ = [
    ("¿Venden mangueras para lavadoras Samsung y LG?", "Sí. Tenemos mangueras de desagüe, de entrada de agua, tina-bomba, del presostato y del dispensador para lavadoras Samsung y LG, de carga superior y de carga frontal. Cada marca tiene su tienda y su asesor por WhatsApp."),
    ("¿Cuál es la diferencia entre la manguera de desagüe y la de entrada?", "La de entrada trae el agua a presión de la llave a la lavadora y lleva tuerca en cada punta; la de desagüe saca el agua sucia por gravedad, es corrugada y termina en un codo. No se pueden cambiar entre sí."),
    ("¿La manguera de entrada sirve para todas las lavadoras?", "Sí. La conexión de entrada de agua es la misma en todas las lavadoras, sin importar la marca ni si es de carga superior o frontal. Solo cambia el largo."),
    ("¿La manguera de desagüe sirve para todas?", "No siempre: la medida del desagüe cambia según la lavadora, y las más largas son para las de carga frontal. El asesor te confirma la medida."),
    ("¿Qué es la manguera tina-bomba?", "Es una manguera interna que une la tina con la bomba de desagüe. Si se agrieta o se suelta, la lavadora pierde agua por debajo o no desagua."),
    ("¿Cómo sé cuál manguera necesita mi lavadora?", "Escríbele al asesor de tu marca por WhatsApp con el modelo de la lavadora (etiqueta) o una foto de la manguera vieja. Te confirma cuál es antes de que compres."),
    ("¿Cuánto cuesta?", "El precio depende de la clase de manguera y del largo. El asesor te responde por WhatsApp con el valor y el tiempo de entrega a tu ciudad."),
    ("¿Hacen envíos a toda Colombia?", "Sí, enviamos por transportadora a todo el país y te mandamos el número de guía."),
    ("¿Cómo pago?", "Con pago contra entrega: pagas cuando recibes el paquete. El asesor te confirma si está disponible en tu ciudad."),
]


def pagina_home(out, dominio, Ss):
    cuerpo_marcas = ""; tarj = ""
    for S in Ss:
        M = S.M; n = M["nombre"]
        fotos = "".join(f'<span class="lf">{foto_html(p, lazy=True)}</span>' for p in M["productos"][:3])
        cuerpo_marcas += (f'<article class="m-card marca-card"><div class="tx"><h3><a href="/{S.clave}/">Mangueras para lavadora {n}</a></h3>'
                          f'<div class="lav-fotos">{fotos}</div><p>Desagüe, entrada de agua, tina-bomba y más. Asesor por WhatsApp: {esc(M["telefono"])}.</p>'
                          f'<a class="m-btn block" href="/{S.clave}/">Ver mangueras {n}</a>'
                          f'<a class="m-btn block wa" href="{esc(wa_link(M["whatsapp"], "Hola, necesito una manguera para mi lavadora " + n))}" target="_blank" rel="noopener">💬 Asesor {n} por WhatsApp</a></div></article>')
        for p in M["productos"]:
            pr = f'<span class="pr">{cop(p["precio"])}</span>' if p["precio"] else '<span class="pr consulta">Consulta el precio<small>Te responde el asesor</small></span>'
            tarj += (f'<article class="m-card"><span class="m-tipo">{n} · {esc(p["tipo"])}</span><span class="im">{foto_html(p)}</span><div class="tx">'
                     f'<h3><a href="/{S.clave}/{p["slug"]}/">{esc(p["nombre"])}</a></h3>{pr}'
                     f'<a class="m-btn block wa" href="{esc(wa_link(M["whatsapp"], "Hola, quiero consultar por la " + p["nombre"]))}" target="_blank" rel="noopener">💬 Preguntar al asesor</a>'
                     f'<a class="m-link" href="/{S.clave}/{p["slug"]}/">Ver detalles</a></div></article>')
    ciudades_links = " · ".join(f'<a href="/{S.clave}/mangueras-lavadora-{S.clave}-por-ciudad/">Ciudades {esc(S.M["nombre"])}</a>' for S in Ss)
    cuerpo = f'''<section class="m-hero"><div class="m-wrap">
  <div>
    <h1>Mangueras para lavadoras Samsung y LG</h1>
    <p class="lead">Manguera de desagüe, de entrada de agua, tina-bomba, del presostato y del dispensador para lavadoras Samsung y LG de carga superior y carga frontal. La de entrada sirve para todas las lavadoras; para las demás, cuéntale tu modelo al asesor por WhatsApp y te confirmamos la correcta. Enviamos a toda Colombia.</p>
    <div class="acc"><a class="m-btn" href="#marcas">Elegir mi marca</a></div>
    <ul><li>Pago contra entrega</li><li>Envío a toda Colombia</li><li>Asesor que te confirma la manguera</li></ul>
  </div>
</div></section>
{confianza()}
<section class="m-sec" id="marcas"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Escoge tu marca</span><h2>¿De qué marca es tu lavadora?</h2></div><div class="m-grid lav-marcas">{cuerpo_marcas}</div></div></section>
<section class="m-sec alt" id="mangueras"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Catálogo</span><h2>Todas las mangueras</h2><p>Pregunta por la tuya y el asesor te confirma la correcta antes de comprar.</p></div><div class="m-grid">{tarj}</div></div></section>
{bloque_importancia()}
{bloque_entrega()}
{tres_pasos()}
<section class="m-sec alt" id="preguntas"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Resolvemos tus dudas</span><h2>Preguntas frecuentes</h2></div>{faq_html(HOME_FAQ)}</div></section>
<section class="m-sec"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Envíos</span><h2>Enviamos a toda Colombia</h2></div><p>{ciudades_links}</p></div></section>'''
    cuerpo = cuerpo.replace('href="/cambio-e-instalacion/"', 'href="/samsung/cambio-e-instalacion/"').replace('href="/como-saber-si-la-manguera-esta-danada/"', 'href="/samsung/como-saber-si-la-manguera-esta-danada/"')
    ld = [{"@type": "WebSite", "name": "Mangueras para lavadoras", "url": dominio + PREF + "/"}, faq_ld(HOME_FAQ),
          {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i, "url": f"{dominio}{PREF}/{S.clave}/{p['slug']}/", "name": p["nombre"]} for i, (S, p) in enumerate([(S, p) for S in Ss for p in S.M["productos"]], 1)]}]
    escribir(out, PREF + "/", "home", "Mangueras para lavadoras Samsung y LG | Envío a toda Colombia",
             "Mangueras de desagüe, entrada de agua y tina-bomba para lavadoras Samsung y LG. Pregunta al asesor por WhatsApp y recibe en toda Colombia con pago contra entrega.", cuerpo, ld,
             f'<meta property="og:image" content="{dominio}{PREF}/img/{Ss[0].M["productos"][0]["id"]}.jpg">')


def marca_json(S, Ss):
    M = S.M; clave = S.clave; b = S.pref + "/"
    otras = [[f"Mangueras para lavadora {o.M['nombre']}", f"{PREF}/{o.clave}/"] for o in Ss if o is not S] + [["Inicio", PREF + "/"]]
    guias_ = [[f"{b}cual-es-mi-manguera/", "¿Cuál manguera necesita mi lavadora?"], [f"{b}como-saber-si-la-manguera-esta-danada/", "Cómo saber si una manguera está dañada"],
              [f"{b}cambio-e-instalacion/", "Cómo cambiar la manguera"], [f"{b}lavadora-{clave}-gotea-agua-por-la-manguera/", "La lavadora gotea"],
              [f"{b}manguera-de-desague-lavadora-{clave}/", "Manguera de desagüe"], [f"{b}manguera-de-entrada-lavadora-{clave}/", "Manguera de entrada de agua"]]
    return {"nombre": M["nombre"], "clase": M["clase"], "base": b, "tema": M["tema"], "fuentes": FUENTES, "tienda": M["tienda"], "logo": "", "logo_w": 0, "logo_h": 0, "icono": PREF + "/img/icono.svg",
            "whatsapp": M["whatsapp"], "telefono": M["telefono"], "productos": [[p["nombre"], p["slug"]] for p in M["productos"]], "guias": guias_,
            "ciudades": [[c, f"{b}manguera-lavadora-{clave}-{slug(c)}/"] for c in ["Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena", "Bucaramanga", "Pereira", "Manizales", "Armenia", "Ibagué", "Cúcuta", "Santa Marta"]],
            "hub": f"{b}mangueras-lavadora-{clave}-por-ciudad/", "extra": otras, "externos": [list(M["oficial"]), ["Superintendencia de Industria y Comercio", "https://www.sic.gov.co/"]]}


def llms_php(Ss):
    txt = ("# Mangueras para lavadoras Samsung y LG\n\n> Manguera de desagüe, de entrada de agua, tina-bomba, del presostato y del dispensador para lavadoras Samsung y LG de carga superior y carga frontal, con envío a toda Colombia y pago contra entrega. "
           "La manguera correcta y el precio se confirman con un asesor por WhatsApp.\n")
    for S in Ss:
        M = S.M
        txt += f"\n## {M['nombre']} (WhatsApp {M['telefono']})\n- [Mangueras para lavadora {M['nombre']}](__BASE__{PREF}/{S.clave}/)\n"
        for p in M["productos"]:
            txt += f"- [{p['nombre']}](__BASE__{PREF}/{S.clave}/{p['slug']}/): {p['tipo']}.\n"
        txt += (f"- [Cuál manguera necesita mi lavadora](__BASE__{PREF}/{S.clave}/cual-es-mi-manguera/)\n- [Cómo cambiar la manguera](__BASE__{PREF}/{S.clave}/cambio-e-instalacion/)\n"
                f"- [Lavadora {M['nombre']} gotea agua](__BASE__{PREF}/{S.clave}/lavadora-{S.clave}-gotea-agua-por-la-manguera/)\n")
    txt += "\n## Preguntas y respuestas\n" + "".join(f"- **{q}** {a}\n" for q, a in HOME_FAQ)
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
    Ss = [SitioB(c, dominio, raiz) for c in MARCAS]
    for S in Ss:
        S.chips_ciudad = [(c[0], f"/manguera-lavadora-{S.clave}-{slug(c[0])}/") for c in S.ciudades]
        for p in S.M["productos"]:
            p["nombre"] = f"{p['corto']} para lavadora {S.M['nombre']}: {p['tipo'][0].lower() + p['tipo'][1:]}"
        preparar_fotos(S.M, out)
    for S in Ss:
        (out / f"marca-{S.clave}.json").write_text(json.dumps(marca_json(S, Ss), ensure_ascii=False), encoding="utf-8")
        pagina_inicio(S)
        for p in S.M["productos"]:
            pagina_producto(S, p)
        guias(S)
        paginas_ciudad(S)
    home = {"nombre": "Samsung y LG", "clase": "samsung", "base": PREF + "/", "tema": "#071338", "fuentes": FUENTES, "tienda": "Mangueras para lavadoras", "logo": "", "logo_w": 0, "logo_h": 0, "icono": PREF + "/img/icono.svg",
            "whatsapp": "", "telefono": "", "productos": [[p["nombre"], f"{S.clave}/{p['slug']}"] for S in Ss for p in S.M["productos"]], "guias": [], "ciudades": [], "hub": None,
            "extra": [[f"Mangueras para lavadora {S.M['nombre']}", f"{PREF}/{S.clave}/"] for S in Ss], "externos": [["Superintendencia de Industria y Comercio", "https://www.sic.gov.co/"]]}
    (out / "marca-home.json").write_text(json.dumps(home, ensure_ascii=False), encoding="utf-8")
    (out / "marca.json").write_text(json.dumps(home, ensure_ascii=False), encoding="utf-8")
    pagina_home(raiz, dominio, Ss)
    paginas = {PREF + "/": "1.0"}
    for S in Ss:
        paginas.update(S.paginas)
    cat = json.loads(subprocess.run(["php", "-r", "echo json_encode(include '" + str(base / 'api' / 'catalogo.php') + "', JSON_UNESCAPED_UNICODE);"], capture_output=True, text=True, check=True).stdout)
    cat["productos"] = {}
    cat["paginas"] = [k[len(PREF):] or "/" for k in paginas]
    cat["marcas"], cat["guias"], cat["compat"], cat["blog"], cat["rutas_ciudad"] = [], [], [], [], {}
    (out / "api" / "catalogo.php").write_text("<?php\n// Generado por mangueras.py: no lo edites a mano.\nreturn " + php_val(cat) + ";\n", encoding="utf-8")
    sm = SITEMAP_PHP.replace("$b = sitio()['base'];", "$b = sitio()['base'] . '" + PREF + "';").replace("'/quienes-somos.php'", "'/quienes-somos.php'")
    (out / "sitemap.php").write_text(sm, encoding="utf-8")
    (out / "llms.php").write_text(llms_php(Ss), encoding="utf-8")
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
    sam = MARCAS["samsung"]
    cfg = cfg.replace("https://filtrosaguanevecones.com", dominio).replace("Filtros Nevecones Colombia", "Filtros para lavadoras").replace("321 799 6144", sam["telefono"]).replace("3217996144", sam["whatsapp"])
    cfg = cfg.replace("pedidos@filtrosaguanevecones.com", "pedidos@" + dominio.split("//")[1])
    cfg = cfg.replace("GTM-5WSNHV66", GTM)                                                    # el mismo Tag Manager de filtrosparalavadoras.click
    cfg = re.sub(r"('google_verificacion'\s*=>\s*)'[^']*'", r"\1'" + VERIFICACION + "'", cfg)  # y la misma verificación de Search Console
    (out / "api" / "config.sample.php").write_text(cfg, encoding="utf-8")
    inst = out / "INSTALAR.md"
    inst.write_text(f"""# Mangueras para lavadoras Samsung y LG, dentro de {dominio}

Todo vive en la carpeta `mangueras-para-lavadora/`, así que no pisa nada de la tienda de filtros (`/samsung/`, `/lg/`, `api/`, `.htaccess`, etc.).

- Portada: {dominio}{PREF}/ (elige marca)
- Samsung: {dominio}{PREF}/samsung/ (asesor WhatsApp {MARCAS['samsung']['telefono']})
- LG: {dominio}{PREF}/lg/ (asesor WhatsApp {MARCAS['lg']['telefono']})

Sin carrito ni pago en línea: los pedidos se hacen por WhatsApp con el asesor (pago contra entrega).

1. En Hostinger abre el administrador de archivos del dominio {dominio.split('//')[1]}, entra a `public_html`, sube `tienda-mangueras-para-lavadora.zip` y descomprímelo ahí. Se crea solo la carpeta `mangueras-para-lavadora`.
2. Dentro de `mangueras-para-lavadora/api/` copia `config.sample.php` como `config.php` y completa el correo, el titular y el documento (iguales a los de la otra tienda). El Tag Manager ({GTM}) y la verificación de Search Console ya vienen puestos.
3. Cada clic en un botón de WhatsApp manda el mismo evento `whatsapp` a Tag Manager (con la marca, la página y el texto del botón), igual que en la tienda de filtros, así que cuenta como la misma conversión.
4. En Search Console agrega el sitemap {dominio}{PREF}/sitemap.xml (la propiedad es la misma).
5. Precios: mientras una manguera no tenga precio, su página dice «pregúntale al asesor».
""", encoding="utf-8")
    z = AQUI / "tienda-mangueras-para-lavadora.zip"
    z.unlink(missing_ok=True)
    (AQUI / "tienda-mangueras.zip").unlink(missing_ok=True)
    subprocess.run(["zip", "-qr", str(z), PREF.strip("/"), "-x", f"{PREF.strip('/')}/api/config.php", "-x", f"{PREF.strip('/')}/data/pedidos.sqlite*", "-x", f"{PREF.strip('/')}/data/correos.log"], cwd=raiz, check=True)
    sin_foto = [f"{S.M['nombre']} {p['tipo']}" for S in Ss for p in S.M["productos"] if p.get("provisional")]
    print(f"Mangueras Samsung y LG: sitios-mangueras/tienda{PREF}/ con {len(paginas)} páginas → {z.name}")
    if sin_foto:
        print("Fotos provisionales (faltan las reales):", ", ".join(sin_foto))


if __name__ == "__main__":
    construir_todo(sys.argv[1] if len(sys.argv) > 1 else "https://filtrosparalavadoras.click")
