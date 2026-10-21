#!/usr/bin/env python3
"""Tienda de bombas de agua (bombas de desagüe) para lavadoras Samsung y LG, con envío a toda Colombia.

Misma arquitectura que la tienda de filtros de pelusas (lavadoras.py): un dominio, una tienda por marca (/samsung/ y /lg/),
asesor por WhatsApp propio de cada marca, sin carrito ni pago en línea (pago contra entrega).
Genera sitios-bombas/tienda/ y tienda-bombas.zip.

Uso:  python3 bombas.py [https://filtrosparalavadoras.click]   (por defecto ese dominio, en la carpeta /bombas-de-agua/)

Fotos: imagenes-bombas/<marca>/ (una por bomba, nombre en PRODUCTOS[...]["foto"]). Si falta una foto se genera una imagen
provisional con el texto «Foto próximamente» para que el sitio compile; reemplázala por la real y vuelve a generar.
Precios y referencias: llena "precio" (pesos) y "ref" en PRODUCTOS. Mientras no haya precio, la página manda al asesor por WhatsApp.
"""
import json, re, shutil, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

import lavadoras as L
from lavadoras import (esc, cop, slug, wa_link, faq_ld, faq_html, chips, foto_html, Sitio, php_val, ciudades,
                       LAV_PHP, CSS_EXTRA, SITEMAP_PHP, FUENTES, AQUI)

PREF = "/bombas-de-agua"      # carpeta de esta tienda dentro del dominio: no pisa nada de la tienda de filtros
GTM = "GTM-5SCP73SQ"                                                  # el mismo de la tienda de filtros
VERIFICACION = "NsQML6RHpDIy79HzjoToyz_eOmWi97jh9G1I1ZwkUM4"          # Search Console de filtrosparalavadoras.click
SALIDA = AQUI / "sitios-bombas"
FOTOS = AQUI / "imagenes-bombas"
L.FOTOS = FOTOS

# ---------------------------------------------------------------- datos por marca
MARCAS = {
    "samsung": {
        "nombre": "Samsung", "clase": "samsung", "tema": "#071338", "whatsapp": "3054796329", "telefono": "305 479 6329",
        "tienda": "Bombas de agua para lavadora Samsung", "logo": "",
        "oficial": ("Samsung Colombia", "https://www.samsung.com/co/"),
        "codigos": "5E, SE o 5C",
        "familias": [("WA", "Carga superior", "carga-superior"), ("WW", "Carga frontal", "carga-frontal"), ("WF", "Carga frontal", "carga-frontal")],
        "productos": [
            {"id": "bom-sam-1", "foto": "bomba-1.png", "slug": "bomba-desague-lavadora-samsung-carcasa-blanca-conector-azul", "corto": "Bomba de desagüe", "ref": None, "precio": None,
             "tipo": "Carcasa blanca con conector azul", "carga": None, "forma": "bomba de desagüe para lavadora Samsung con carcasa blanca, dos bocas de manguera, motor gris y conector eléctrico azul"},
            {"id": "bom-sam-2", "foto": "bomba-2.png", "slug": "bomba-desague-lavadora-samsung-carcasa-blanca-filtro-salida-roscada", "corto": "Bomba de desagüe", "ref": None, "precio": None,
             "tipo": "Carcasa blanca con filtro y salida roscada", "carga": None, "forma": "bomba de desagüe para lavadora Samsung con carcasa blanca, cámara de filtro con tapa negra, salida roscada hacia arriba y motor gris"},
            {"id": "bom-sam-3", "foto": "bomba-3.png", "slug": "bomba-desague-lavadora-samsung-motor-gris-rodete-celeste", "corto": "Bomba de desagüe", "ref": None, "precio": None,
             "tipo": "Motor gris con rodete celeste", "carga": None, "forma": "bomba de desagüe para lavadora Samsung de motor gris con rodete celeste y conector gris en la base"},
            {"id": "bom-sam-4", "foto": "bomba-4.png", "slug": "bomba-desague-lavadora-samsung-motor-gris-rodete-blanco", "corto": "Bomba de desagüe", "ref": None, "precio": None,
             "tipo": "Motor gris con rodete blanco", "carga": None, "forma": "bomba de desagüe para lavadora Samsung de motor gris con rodete blanco; la etiqueta del motor indica DRAIN PUMP y 60 Hz"},
            {"id": "bom-sam-5", "foto": "bomba-5.png", "slug": "bomba-desague-lavadora-samsung-carcasa-blanca-motor-gris-cables", "corto": "Bomba de desagüe", "ref": None, "precio": None,
             "tipo": "Carcasa blanca con motor gris y cables", "carga": None, "forma": "bomba de desagüe para lavadora Samsung con carcasa blanca, dos salidas de manguera y motor gris con cables de conexión"},
            {"id": "bom-sam-6", "foto": "bomba-6.png", "slug": "bomba-desague-lavadora-samsung-dc31-00181c", "corto": "Bomba de desagüe", "ref": "DC31-00181C", "precio": None,
             "tipo": "Carcasa blanca, motor Hanyu B15-3A (DC31-00181C)", "carga": None, "forma": "bomba de desagüe para lavadora Samsung con carcasa blanca y motor Hanyu B15-3A de 120 V y 60 Hz; en la etiqueta de la foto se lee la referencia DC31-00181C"},
        ],
    },
    "lg": {
        "nombre": "LG", "clase": "lg", "tema": "#a50034", "whatsapp": "3205102995", "telefono": "320 510 2995",
        "tienda": "Bombas de agua para lavadora LG", "logo": "",
        "oficial": ("LG Colombia", "https://www.lg.com/co/"),
        "codigos": "OE",
        "familias": [("WT", "Carga superior", "carga-superior"), ("WM", "Carga frontal", "carga-frontal"), ("WD", "Carga frontal", "carga-frontal")],
        "productos": [
            {"id": "bom-lg-1", "foto": "bomba-1.png", "slug": "bomba-desague-lavadora-lg-carcasa-filtro-gris", "corto": "Bomba de desagüe", "ref": None, "precio": None,
             "tipo": "Con carcasa y filtro integrado (gris)", "carga": None, "forma": "bomba de desagüe para lavadora LG con carcasa gris y cámara de filtro integrada, con el motor y el conector a un lado"},
            {"id": "bom-lg-2", "foto": "bomba-2.png", "slug": "bomba-desague-lavadora-lg-motor-negro-4681ea2001t", "corto": "Bomba de desagüe", "ref": "4681EA2001T", "precio": None,
             "tipo": "Motor negro con rodete blanco", "carga": None, "forma": "bomba de desagüe para lavadora LG de motor negro con rodete blanco; en la etiqueta de la foto se lee la referencia 4681EA2001T"},
            {"id": "bom-lg-3", "foto": "bomba-3.png", "slug": "bomba-desague-lavadora-lg-rodete-lila-marca-lc", "corto": "Bomba de desagüe", "ref": None, "precio": None,
             "tipo": "Rodete lila (con marca LC)", "carga": None, "forma": "bomba de desagüe para lavadora LG con carcasa gris, rodete lila y bornes de conexión en la base; esta versión trae la marca LC en el rodete"},
            {"id": "bom-lg-4", "foto": "bomba-4.png", "slug": "bomba-desague-lavadora-lg-rodete-lila", "corto": "Bomba de desagüe", "ref": None, "precio": None,
             "tipo": "Rodete lila", "carga": None, "forma": "bomba de desagüe para lavadora LG con carcasa gris, rodete lila y bornes de conexión en la base"},
            {"id": "bom-lg-5", "foto": "bomba-5.png", "slug": "bomba-desague-lavadora-lg-carcasa-filtro-blanca", "corto": "Bomba de desagüe", "ref": None, "precio": None,
             "tipo": "Con carcasa y filtro integrado (blanca)", "carga": None, "forma": "bomba de desagüe para lavadora LG con carcasa blanca y cámara de filtro integrada, con anillo negro del motor"},
            {"id": "bom-lg-6", "foto": "bomba-6.png", "slug": "bomba-desague-lavadora-lg-carcasa-filtro-negra-110-127v", "corto": "Bomba de desagüe", "ref": None, "precio": None,
             "tipo": "Carcasa de filtro negra (110-127 V)", "carga": None, "forma": "bomba de desagüe para lavadora LG con carcasa negra, tapa de filtro y bornes laterales; la etiqueta de la foto indica PSB-02, 110-127 V, 60 Hz y 35 W"},
            {"id": "bom-lg-7", "foto": "bomba-7.png", "slug": "bomba-desague-lavadora-lg-carcasa-gris-conector-blanco", "corto": "Bomba de desagüe", "ref": None, "precio": None,
             "tipo": "Carcasa gris con conector blanco", "carga": None, "forma": "bomba de desagüe para lavadora LG con carcasa gris, dos salidas de manguera y conector eléctrico blanco bajo la bomba"},
            {"id": "bom-lg-8", "foto": "bomba-8.png", "slug": "bomba-desague-lavadora-lg-carcasa-negra-manguera-purga", "corto": "Bomba de desagüe", "ref": None, "precio": None,
             "tipo": "Carcasa negra con manguera de purga", "carga": None, "forma": "bomba de desagüe para lavadora LG con carcasa negra, cámara de filtro de boca ancha y una manguera pequeña de purga"},
        ],
    },
}
L.MARCAS = MARCAS

# Palabras con las que la gente busca la misma pieza (se usan en textos, descripciones y llms.txt)
SINONIMOS = ("bomba de agua de la lavadora, bomba de desagüe, bomba de drenaje, motobomba de desagüe, bomba de vaciado, bomba de evacuación, "
             "bomba de la lavadora, bomba de agua para lavadora")

INSTALACION = [
    "Desconecta la lavadora de la corriente y cierra la llave del agua. No trabajes con la máquina enchufada.",
    "Vacía la tina todo lo que puedas. Ten a mano una cubeta, trapos y una linterna: siempre cae algo de agua al soltar la bomba.",
    "Accede a la bomba: en carga frontal suele estar abajo, detrás de la tapa o del panel frontal inferior; en carga superior, abajo o en la parte de atrás, según el modelo.",
    "Toma una foto de las mangueras y los conectores antes de soltarlos, para volver a ponerlos igual. Suelta las abrazaderas y los conectores eléctricos.",
    "Retira la bomba vieja (va con tornillos o con un seguro de media vuelta) y compárala con la nueva: deben coincidir en la forma de la carcasa, las entradas de manguera y el conector.",
    "Instala la bomba nueva, vuelve a poner mangueras, abrazaderas y conectores como en la foto, y revisa que no queden fugas.",
    "Abre el agua, conecta la lavadora y haz un ciclo corto de desagüe o centrifugado para comprobar que desagua bien y no gotea.",
]
NOTA_INSTALACION = ("Los pasos cambian según el modelo. Si no te sientes seguro con la parte eléctrica o con las mangueras, pídele ayuda a un técnico. "
                    "Y si tu modelo es distinto, escríbele al asesor por WhatsApp.")

SINTOMAS = [
    "La lavadora no desagua y el agua se queda en la tina.",
    "Hace ruido fuerte, zumbido o chillido cuando desagua.",
    "La ropa sale empapada porque no centrifuga.",
    "Aparece un código de error de desagüe en la pantalla.",
    "Hay fugas de agua debajo de la lavadora.",
    "La lavadora se detiene a mitad del ciclo.",
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
    """Foto de la entrega del paquete: se repinta la etiqueta de la caja para que hable de bombas de lavadora."""
    im = Image.open(AQUI / "imagenes-tienda" / "entrega.jpg").convert("RGB")
    d = ImageDraw.Draw(im)
    caja = (684, 646, 1030, 800)
    base = (182, 142, 112)
    for y in range(caja[1], caja[3]):
        t = (y - caja[1]) / (caja[3] - caja[1])
        d.line([(caja[0], y), (caja[2], y)], fill=tuple(int(base[i] * (1 - 0.10 * t)) for i in range(3)))
    f1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34)
    f2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    d.text((694, 676), "Bomba de desagüe", font=f1, fill=(20, 45, 100))
    d.text((694, 722), "para su lavadora", font=f2, fill=(20, 45, 100))
    im.thumbnail((1100, 1100))
    img = out / "img"
    im.save(img / "entrega-bomba.jpg", quality=84, optimize=True)
    im.save(img / "entrega-bomba.webp", quality=82)
    im6 = im.copy(); im6.thumbnail((640, 640)); im6.save(img / "entrega-bomba-640.webp", quality=80)


def prefijar(h):
    """Todo enlace o imagen que empiece por «/» pasa a vivir dentro de /bombas-de-agua/."""
    h = re.sub(r'(?<![\w.:/-])/img/', PREF + "/img/", h)
    return re.sub(r'(href|action)="/(?!/|bombas-de-agua/)', lambda m: f'{m.group(1)}="{PREF}/', h)


def escribir(out, real, marca, titulo, desc, cuerpo, ld, extra_head=""):
    """Escribe una página PHP en out/<real>/index.php; la infraestructura (lav.php) vive en out/bombas-de-agua/."""
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
    """Igual que Sitio, pero la marca vive en /bombas-de-agua/<marca>/."""
    def __init__(self, clave, dominio, out):
        super().__init__(clave, dominio, out)
        self.pref = PREF + "/" + clave
        self.dominio = dominio + self.pref
        self.raiz = dominio + PREF


# ---------------------------------------------------------------- bloques comunes
def bloque_importancia(n=""):
    return f'''<section class="m-sec lav-importancia"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Lo importante</span><h2>Para qué sirve la bomba de agua de tu lavadora {n}</h2>
<p>La bomba de desagüe (la gente también la llama bomba de agua, bomba de drenaje o motobomba) es la pieza que saca el agua sucia de la tina al terminar el lavado y antes de centrifugar.</p></div>
<ul class="lav-puntos"><li><b>Sin bomba, no hay desagüe.</b> Si falla, el agua se queda en la tina y la lavadora se detiene o muestra un error.</li>
<li><b>Sin desagüe, no hay centrifugado.</b> La ropa sale empapada y con mal olor.</li>
<li><b>Un ruido nuevo avisa.</b> Zumbidos, chillidos o golpeteo al desaguar suelen ser la bomba con el rodete atascado o desgastado.</li>
<li><b>A veces no es la bomba.</b> Una manguera doblada, el filtro tapado o un objeto atascado dan los mismos síntomas: por eso el asesor revisa contigo antes de que compres.</li>
<li><b>Se cambia sin cambiar de lavadora.</b> Reemplazar la bomba cuesta mucho menos que una lavadora nueva.</li></ul>
<p><a class="m-btn sec" href="/como-saber-si-la-bomba-esta-danada/">Cómo saber si tu bomba está dañada</a></p></div></section>'''


def bloque_entrega():
    foto = ('<picture><source srcset="/img/entrega-bomba-640.webp 640w, /img/entrega-bomba.webp 1100w" sizes="(max-width:860px) 100vw, 520px" type="image/webp">'
            '<img src="/img/entrega-bomba.jpg" alt="Repartidor entregando el paquete con la bomba de desagüe de la lavadora a una clienta en la puerta de su casa" width="1100" height="825" loading="lazy"></picture>')
    return f'''<section class="m-sec alt lav-entrega-sec"><div class="m-wrap lav-entrega"><div class="lav-entrega-foto">{foto}</div>
<div class="lav-entrega-tx"><span class="eyebrow">Pago contra entrega</span><h2>Recibes el paquete y pagas</h2>
<p>Pides tu bomba por WhatsApp, el asesor te confirma el modelo, el valor y el envío, y la recibes en tu casa. <b>Pagas cuando tienes el paquete en las manos.</b></p>
<ul class="m-ok"><li>Primero confirmas la bomba correcta con el asesor.</li><li>Te enviamos por transportadora, con número de guía.</li><li>Abres el paquete, la revisas y pagas al recibir.</li></ul>
<p class="m-mut">El asesor te confirma si el pago contra entrega está disponible en tu ciudad.</p></div></div></section>'''


def confianza():
    return '''<section class="m-confianza"><div class="m-wrap"><div><span class="ic">💵</span><span><b>Pago contra entrega</b><small>Pagas al recibir el paquete</small></span></div><div><span class="ic">🚚</span><span><b>Envío a toda Colombia</b><small>Con número de guía</small></span></div><div><span class="ic">💬</span><span><b>Asesor por WhatsApp</b><small>Te confirma el modelo</small></span></div><div><span class="ic">🔧</span><span><b>Cambio paso a paso</b><small>Guía de instalación</small></span></div></div></section>'''


def tres_pasos(n=""):
    return f'''<section class="m-sec"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Así de fácil</span><h2>Compra en 3 pasos</h2></div><div class="m-cols m-num"><div class="m-bloque"><h3>Escríbele al asesor</h3><p>Mándale el modelo de tu lavadora {n}o una foto de la bomba vieja o de la etiqueta de la máquina.</p></div><div class="m-bloque"><h3>Confirma bomba y envío</h3><p>El asesor te dice cuál bomba es, el valor y el tiempo de entrega a tu ciudad.</p></div><div class="m-bloque"><h3>Recibe y paga</h3><p>Llega a tu casa con número de guía y pagas contra entrega.</p></div></div></div></section>'''


def faq_general(S):
    n = S.M["nombre"]; c = S.M["codigos"]
    return [
        (f"¿Qué es la bomba de agua de la lavadora {n}?", f"Casi siempre se refiere a la bomba de desagüe (también llamada bomba de drenaje o motobomba): saca el agua de la tina al final del lavado. Si buscas la bomba de agua de tu lavadora {n} y la máquina no desagua, es esta pieza."),
        (f"¿Cómo sé si la bomba de mi lavadora {n} está dañada?", "Los signos más comunes son: el agua se queda en la tina, hace un zumbido o chillido al desaguar, la ropa sale empapada, hay fugas debajo o aparece un código de error de desagüe. Antes de cambiarla conviene revisar el filtro, la manguera y el desagüe; el asesor te guía por WhatsApp."),
        (f"¿Qué código de error de desagüe muestra la lavadora {n}?", f"Depende del modelo; en {n} los más comunes son {c}. Mándale al asesor una foto del código y el modelo de tu lavadora y te dice si apunta a la bomba."),
        (f"¿Cómo sé cuál bomba necesita mi lavadora {n}?", "Depende del modelo exacto y de si es de carga superior o frontal. Escríbele al asesor por WhatsApp con el modelo (está en una etiqueta atrás, en un costado o bajo la tapa) o con una foto de la bomba vieja, y te confirma la correcta antes de que compres."),
        ("¿Cuánto cuesta?", "El precio depende del modelo y de la referencia. Pregúntale al asesor por WhatsApp y te responde en el momento con el valor y el tiempo de entrega a tu ciudad."),
        ("¿Hacen envíos a toda Colombia?", "Sí. Enviamos por transportadora a todo el país y te mandamos el número de guía."),
        ("¿Puedo cambiarla yo mismo?", "Si tienes algo de práctica, sí: se suelta con unos pocos tornillos y abrazaderas. Hay que desconectar la lavadora, cerrar el agua y tomar fotos de las conexiones. Abajo está el paso a paso; si prefieres, pídele ayuda a un técnico."),
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
    fam = chips([(f"Lavadora {n} {f[0]} ({f[1].lower()})", f"/bomba-lavadora-{S.clave}-modelo-{f[0].lower()}/") for f in M["familias"]])
    cuerpo = f'''<section class="m-hero"><div class="m-wrap">
  <div>
    <h1>Bombas de agua para lavadora {n}</h1>
    <p class="lead">Bomba de desagüe (bomba de agua, bomba de drenaje) para lavadoras {n} de carga superior y de carga frontal. Cuéntale tu modelo al asesor por WhatsApp y te confirmamos la bomba correcta. Enviamos a toda Colombia con pago contra entrega.</p>
    <div class="acc">{S.boton_asesor(f"Hola, necesito la bomba de agua de mi lavadora {n}")}<a class="m-btn sec" href="#bombas">Ver las bombas</a></div>
    <ul><li>Pago contra entrega</li><li>Envío a toda Colombia</li><li>Asesor que te confirma el modelo</li></ul>
  </div>
  <div class="lav-fotos">{"".join(f'<span class="lf">{foto_html(p, lazy=i>0)}</span>' for i, p in enumerate(M["productos"][:3]))}</div>
</div></section>
{confianza()}
<section class="m-sec" id="bombas"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Catálogo {n}</span><h2>Bombas de desagüe para lavadora {n}</h2><p>Escoge según el tipo de carga de tu lavadora. El asesor confirma la referencia exacta con tu modelo antes de la compra.</p></div><div class="m-grid">{tarjetas(S)}</div></div></section>
<section class="m-sec alt"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Encuentra la tuya</span><h2>¿Qué bomba necesita mi lavadora {n}?</h2></div>
<div class="m-cols"><div><h3>Lavadora de carga superior</h3><p>Se abre por arriba. Los modelos suelen empezar con {M["familias"][0][0]}. La bomba va en la parte baja, y se cambia distinto a la de carga frontal.</p><p><a class="m-link" href="/bomba-lavadora-{S.clave}-carga-superior/">Bomba para carga superior →</a></p></div>
<div><h3>Lavadora de carga frontal</h3><p>Se abre por el frente con una puerta redonda. Los modelos suelen empezar con {" o ".join(f[0] for f in M["familias"][1:])}. La bomba está detrás del panel inferior.</p><p><a class="m-link" href="/bomba-lavadora-{S.clave}-carga-frontal/">Bomba para carga frontal →</a></p></div>
<div><h3>Si no estás segura o seguro</h3><p>Mándale al asesor una foto de la etiqueta con el modelo o de la bomba vieja. Te responde con la bomba que le corresponde.</p></div></div>
<h3 style="margin-top:18px">Busca por familia de modelo</h3>{fam}
<p style="margin-top:14px"><a class="m-btn" href="/cual-es-mi-bomba/">Guía: cuál es mi bomba</a></p></div></section>
{bloque_importancia(n)}
<section class="m-sec alt"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Señales</span><h2>Cuándo hay que cambiar la bomba de la lavadora {n}</h2></div><ul class="lav-puntos">{"".join(f"<li>{esc(s)}</li>" for s in SINTOMAS)}</ul>
<p>Antes de comprar, descarta lo básico: filtro de desagüe tapado, manguera doblada u obstruida y desagüe de la pared con tapón. Si nada de eso es, la bomba es la sospechosa.</p>
<p><a class="m-btn sec" href="/lavadora-{S.clave}-no-desagua/">Lavadora {n} no desagua: qué revisar</a></p></div></section>
{bloque_entrega()}
{tres_pasos(n + " ")}
<section class="m-sec"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Mantenimiento</span><h2>Cómo cambiar la bomba de agua de tu lavadora {n}</h2></div>
<div class="m-texto"><p>Cambiar la bomba es una reparación al alcance de quien tiene algo de práctica: se desconecta la lavadora, se cierra el agua, se suelta la bomba vieja y se pone la nueva. Tenemos el paso a paso con las precauciones.</p>
<p><a class="m-btn sec" href="/cambio-e-instalacion/">Paso a paso para cambiar la bomba</a></p></div></div></section>
<section class="m-sec alt" id="preguntas"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Resolvemos tus dudas</span><h2>Preguntas frecuentes sobre la bomba de la lavadora {n}</h2></div>{faq_html(faq)}</div></section>
<section class="m-sec"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Envíos</span><h2>Enviamos bombas para lavadora {n} a toda Colombia</h2><p>Escoge tu ciudad para ver el tiempo de entrega y hablar con el asesor.</p></div>{chips(S.chips_ciudad[:24])}<p><a href="/bombas-lavadora-{S.clave}-por-ciudad/">Ver todas las ciudades →</a></p></div></section>
<section class="m-sec alt"><div class="m-wrap"><div class="m-cta"><div><h2>¿No sabes cuál es tu bomba?</h2><p>Mándanos una foto de la etiqueta con el modelo de tu lavadora o de la bomba vieja por WhatsApp.</p></div>{S.boton_asesor(f"Hola, necesito la bomba de agua de mi lavadora {n}")}</div></div></section>
{S.barra(f"Hola, necesito la bomba de agua de mi lavadora {n}")}'''
    ld = [{"@type": "CollectionPage", "name": f"Bombas de agua para lavadora {n}", "url": S.dominio + "/", "description": f"Bombas de desagüe para lavadoras {n} en Colombia."},
          {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i, "url": S.dominio + f"/{p['slug']}/", "name": p["nombre"]} for i, p in enumerate(M["productos"], 1)]},
          faq_ld(faq)]
    S.pagina("/", f"Bombas de agua para lavadora {n} | Envío a toda Colombia", f"Bomba de desagüe (bomba de agua) para lavadoras {n} de carga superior y frontal. Pregunta al asesor por WhatsApp, paga contra entrega y recibe en toda Colombia.", cuerpo, ld, "1.0",
             f'<meta property="og:image" content="{S.raiz}/img/{M["productos"][0]["id"]}.jpg">')


def pagina_producto(S, p):
    M = S.M; n = M["nombre"]
    otros = [(f"{q['nombre']}", f"/{q['slug']}/") for q in M["productos"] if q is not p]
    faq = [(f"¿Esta bomba sirve para mi lavadora {n}?", f"Escríbele al asesor por WhatsApp con el modelo de tu lavadora (está en la etiqueta) o una foto de la bomba vieja y te confirmamos antes de que compres."),
           ("¿Cuánto cuesta?", "Pregunta al asesor por WhatsApp: te da el precio y el tiempo de entrega a tu ciudad."),
           ("¿Cómo la cambio?", "Desconectas la lavadora, cierras el agua, sueltas mangueras y conector de la bomba vieja y pones la nueva igual. Abajo está el paso a paso."),
           (f"¿Cómo sé que la bomba de mi lavadora {n} es la que falla?", "Si no desagua, hace un zumbido al desaguar o la ropa sale empapada, y ya revisaste filtro, manguera y desagüe, lo más probable es la bomba. El asesor te ayuda a confirmarlo.")]
    precio = (f'<span class="precio">{cop(p["precio"])}<small>Confirma disponibilidad y envío con el asesor</small></span>' if p["precio"]
              else '<span class="precio consulta">Precio: pregúntale al asesor<small>Respuesta en el momento por WhatsApp</small></span>')
    cuerpo = f'''<div class="m-wrap">{S.miga((p["nombre"], None))}
<div class="m-prod">
  <div class="foto"><span class="m-badge">{esc(p["tipo"])}</span>{foto_html(p, True, False)}</div>
  <div class="info">
    <h1>{esc(p["nombre"])}</h1>
    <span class="sub">Lavadora {n} · {esc(p["tipo"])}</span>
    {precio}
    <div class="m-aviso"><span style="font-size:22px">💬</span><span><b>¿Sirve para tu lavadora?</b>Antes de comprar, el asesor confirma contigo el modelo correcto. Mándale la etiqueta con el modelo o una foto de la bomba vieja.</span></div>
    {S.boton_asesor(f"Hola, quiero consultar por la {p['nombre']}", "m-btn block wa", "💬 Pedir o preguntar al asesor por WhatsApp")}
    <ul class="m-ok"><li><b>Envío a toda Colombia</b> por transportadora, con número de guía.</li><li><b>Guía de cambio</b> paso a paso incluida en esta página.</li><li><b>Pago contra entrega</b>: pagas cuando recibes el paquete (el asesor confirma si aplica en tu ciudad).</li></ul>
  </div>
</div></div>
<section class="m-sec alt"><div class="m-wrap"><div class="m-texto"><div class="m-cab"><span class="eyebrow">Descripción</span><h2>{esc(p["nombre"])}</h2></div>
<p>Es una {esc(p["forma"])}. También se conoce como bomba de agua, bomba de drenaje o motobomba de la lavadora: saca el agua de la tina cuando termina el lavado y antes del centrifugado.</p>
<p>Si tu lavadora {n} no desagua, hace ruido al vaciar o muestra un código de error de desagüe ({M["codigos"]}), esta pieza es una de las primeras que se revisan. Para estar seguros de que es la que necesita tu lavadora, el asesor revisa el modelo contigo por WhatsApp.</p></div></div></section>
<section class="m-sec"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Datos</span><h2>Ficha del producto</h2></div><dl class="m-ficha"><dt>Marca de la lavadora</dt><dd>{n}</dd><dt>Tipo de bomba</dt><dd>{esc(p["tipo"])}</dd><dt>Pieza</dt><dd>Bomba de desagüe (bomba de agua)</dd><dt>Referencia</dt><dd>{esc(p["ref"]) if p["ref"] else "Te la confirma el asesor según el modelo"}</dd><dt>Envío</dt><dd>Toda Colombia, por transportadora</dd></dl></div></section>
{bloque_importancia(n)}
{bloque_entrega()}
<section class="m-sec alt"><div class="m-wrap"><section class="caja tutorial" id="instalacion"><h2>Cómo cambiar la bomba de desagüe de tu lavadora {n}: paso a paso</h2><ol class="pasos">{"".join(f"<li>{esc(x)}</li>" for x in INSTALACION)}</ol><p class="m-mut">{esc(NOTA_INSTALACION)}</p></section></div></section>
<section class="m-sec"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Preguntas</span><h2>Preguntas frecuentes</h2></div>{faq_html(faq)}</div></section>
{('<section class="m-sec alt"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Más bombas</span><h2>Otras bombas para lavadora ' + n + '</h2></div>' + chips(otros) + '</div></section>') if otros else ""}
{S.barra(f"Hola, quiero consultar por la {p['nombre']}")}'''
    prod = {"@type": "Product", "name": p["nombre"], "image": f"{S.raiz}/img/{p['id']}.jpg", "brand": {"@type": "Brand", "name": n}, "category": "Repuestos para lavadoras",
            "description": f"Bomba de desagüe (bomba de agua) para lavadora {n}: {p['tipo'].lower()}. Envío a toda Colombia.", "areaServed": "CO"}
    if p["ref"]: prod["mpn"] = p["ref"]
    if p["precio"]:
        prod["offers"] = {"@type": "Offer", "priceCurrency": "COP", "price": p["precio"], "availability": "https://schema.org/InStock", "url": f"{S.dominio}/{p['slug']}/"}
    S.pagina(f"/{p['slug']}/", f"{p['nombre']} | Pago contra entrega", f"Bomba de desagüe para lavadora {n}: {p['tipo'].lower()}. Pregunta al asesor por WhatsApp el precio y recibe en toda Colombia.", cuerpo,
             [prod, faq_ld(faq), HowTo(S, p), S.breadcrumb((p["nombre"], None))], "0.9", f'<link rel="preload" as="image" href="/img/{p["id"]}.webp"><meta property="og:image" content="{S.raiz}/img/{p["id"]}.jpg">')


def HowTo(S, p):
    return {"@type": "HowTo", "name": f"Cómo cambiar la bomba de desagüe de una lavadora {S.M['nombre']}", "step": [{"@type": "HowToStep", "position": i, "text": t} for i, t in enumerate(INSTALACION, 1)]}


def pagina_guia(S, ruta, titulo, desc, h1, cuerpo_html, faq=None):
    n = S.M["nombre"]
    cuerpo = f'<div class="m-wrap">{S.miga((h1, None))}<div class="m-texto"><h1>{esc(h1)}</h1>{cuerpo_html}</div>' \
             f'<div class="m-cta" style="margin:24px 0"><div><h2>¿Quieres la bomba correcta?</h2><p>Escríbele al asesor por WhatsApp con el modelo de tu lavadora.</p></div>{S.boton_asesor(f"Hola, tengo una pregunta sobre la bomba de agua de mi lavadora {n}")}</div>' \
             + (f'<h2>Preguntas frecuentes</h2>{faq_html(faq)}' if faq else "") + "</div>"
    ld = [S.breadcrumb((h1, None))] + ([faq_ld(faq)] if faq else [])
    S.pagina(ruta, titulo, desc, cuerpo, ld, "0.8")


def guias(S):
    M = S.M; n = M["nombre"]; c = M["codigos"]
    cat = chips([(p["nombre"], f"/{p['slug']}/") for p in M["productos"]])
    G = lambda *a, **k: pagina_guia(S, *a, **k)
    G("/cual-es-mi-bomba/", f"¿Cuál bomba de agua necesita mi lavadora {n}? Guía", f"Cómo saber qué bomba de desagüe necesita tu lavadora {n}: carga superior o frontal, modelo y forma de la bomba.",
      f"¿Cuál bomba de agua necesita mi lavadora {n}?",
      f'<p>Para escoger bien mira tres cosas: el tipo de carga de tu lavadora, el modelo exacto y cómo es la bomba vieja.</p><h2>1. Tipo de carga</h2><p>Si la lavadora se abre por arriba es de carga superior; si tiene una puerta redonda al frente, es de carga frontal. La bomba y su ubicación cambian entre una y otra.</p>{cat}'
      f'<h2>2. El modelo de la lavadora</h2><p>Está en una etiqueta en la parte de atrás, en un costado o bajo la tapa. En {n} los modelos empiezan por {", ".join(f[0] for f in M["familias"])}. Con el modelo, el asesor te confirma la bomba por WhatsApp.</p>'
      f'<h2>3. La bomba vieja</h2><p>Si ya la sacaste, compárala por la forma de la carcasa, las entradas de manguera y el conector eléctrico. Una foto al asesor ayuda a confirmarla.</p>', faq_general(S)[3:5])
    G("/como-saber-si-la-bomba-esta-danada/", f"Cómo saber si la bomba de la lavadora {n} está dañada", f"Señales de que la bomba de desagüe de tu lavadora {n} falla y qué revisar antes de comprar una nueva.",
      f"Cómo saber si la bomba de la lavadora {n} está dañada",
      "<p>La bomba de desagüe falla de forma bastante reconocible. Estas son las señales más comunes:</p><ul>" + "".join(f"<li>{esc(s)}</li>" for s in SINTOMAS) + "</ul>"
      "<h2>Antes de cambiarla, revisa esto</h2><ol class='pasos'><li>Desconecta la lavadora y revisa el filtro de desagüe: si está tapado con monedas, hilos o pelusas, límpialo.</li><li>Mira que la manguera de desagüe no esté doblada ni aplastada.</li><li>Comprueba que el desagüe de la pared no esté tapado.</li><li>Haz un ciclo de centrifugado: si el agua no sale ni suena la bomba, o suena pero no mueve agua, la bomba es la sospechosa.</li></ol>"
      "<p>Si después de esto sigue igual, escríbele al asesor: con el modelo de tu lavadora te confirma la bomba que necesitas.</p>", faq_general(S)[1:3])
    G("/cambio-e-instalacion/", f"Cómo cambiar la bomba de desagüe de la lavadora {n}: paso a paso", f"Paso a paso para cambiar la bomba de agua (bomba de desagüe) de una lavadora {n} de carga superior o frontal, con precauciones.",
      f"Cómo cambiar la bomba de agua de la lavadora {n}",
      "<ol class='pasos'>" + "".join(f"<li>{esc(x)}</li>" for x in INSTALACION) + f"</ol><p class='m-mut'>{esc(NOTA_INSTALACION)}</p>", faq_general(S)[6:7])
    G(f"/lavadora-{S.clave}-no-desagua/", f"Lavadora {n} no desagua: causas y solución", f"Por qué una lavadora {n} no desagua, qué revisar (filtro, manguera, bomba) y cuándo hay que cambiar la bomba de agua.",
      f"Lavadora {n} no desagua",
      "<p>Cuando una lavadora no desagua, el agua se queda en la tina y el ciclo se detiene. Estas son las causas, de la más fácil a la más seria:</p>"
      "<h2>Qué revisar, en orden</h2><ol class='pasos'><li><b>Filtro de desagüe tapado.</b> Es el culpable más frecuente: sácalo y límpialo.</li><li><b>Manguera de desagüe doblada o tapada.</b></li><li><b>Desagüe de la pared obstruido.</b></li><li><b>Bomba de desagüe dañada o atascada.</b> Si hace zumbido pero no saca agua, o no suena nada, hay que revisarla o cambiarla.</li><li><b>Tarjeta o sensor de nivel.</b> Menos común; lo confirma un técnico.</li></ol>"
      "<p>Seguridad: desconecta la lavadora antes de meter la mano, y ten una cubeta para el agua que quede en la tina.</p>", faq_general(S)[0:2])
    G(f"/lavadora-{S.clave}-hace-ruido-al-desaguar/", f"Lavadora {n} hace ruido al desaguar: causas", f"Por qué la lavadora {n} hace zumbido, chillido o golpeteo al desaguar y si es la bomba de agua.",
      f"Lavadora {n} hace ruido al desaguar",
      "<p>Un ruido nuevo al desaguar casi siempre viene de la bomba de desagüe.</p><h2>Qué puede ser</h2><ul><li><b>Algo atascado en la bomba:</b> monedas, botones, clips, hilos.</li><li><b>Rodete desgastado</b> o rodamiento seco: chillido o zumbido fuerte.</li><li><b>Motor de la bomba forzado:</b> zumbido sin que salga agua.</li></ul>"
      "<h2>Qué hacer</h2><p>Revisa el filtro de desagüe. Si el ruido sigue, la bomba probablemente esté desgastada y conviene cambiarla antes de que se queme.</p>")
    G(f"/lavadora-{S.clave}-no-centrifuga-ropa-mojada/", f"Lavadora {n} no centrifuga y deja la ropa mojada", f"La lavadora {n} no centrifuga y la ropa sale empapada: cuándo es la bomba de desagüe y qué revisar.",
      f"Lavadora {n} no centrifuga y deja la ropa mojada",
      "<p>La lavadora no centrifuga mientras haya agua en la tina. Si el agua no se va, la máquina no gira para escurrir.</p><h2>Revisa</h2><ol class='pasos'><li>Que la lavadora esté nivelada y la carga bien repartida.</li><li>El filtro y la manguera de desagüe.</li><li>Si el agua no se va: la bomba de desagüe.</li></ol>")
    G(f"/codigo-error-desague-lavadora-{S.clave}/", f"Código de error de desagüe en lavadora {n} ({c})", f"Qué significan los códigos de desagüe de las lavadoras {n} ({c}) y cuándo apuntan a la bomba de agua.",
      f"Código de error de desagüe en lavadora {n} ({c})",
      f"<p>En las lavadoras {n} los códigos de error de desagüe más habituales son <b>{c}</b>. Indican que la máquina no logra sacar el agua en el tiempo esperado.</p><h2>Qué hacer</h2><ol class='pasos'><li>Desconecta la lavadora unos minutos y vuelve a encenderla.</li><li>Limpia el filtro de desagüe y revisa la manguera.</li><li>Si el código vuelve, la causa probable es la bomba de desagüe o su conexión.</li></ol><p>El significado exacto depende del modelo; mándale al asesor el código y el modelo.</p>")
    G(f"/cuanto-cuesta-bomba-agua-lavadora-{S.clave}/", f"Cuánto cuesta la bomba de agua de la lavadora {n}", f"De qué depende el precio de la bomba de desagüe de una lavadora {n} y cómo consultarlo con el asesor.",
      f"Cuánto cuesta la bomba de agua de la lavadora {n}",
      "<p>El precio depende del modelo, de la referencia de la bomba y de la ciudad de envío. Por eso no mostramos un valor único: el asesor te lo da en el momento por WhatsApp.</p><h2>Qué mandarle</h2><ul><li>El modelo de tu lavadora (etiqueta).</li><li>Una foto de la bomba vieja, si ya la sacaste.</li><li>Tu ciudad.</li></ul>" + cat)
    G(f"/bomba-de-agua-o-bomba-de-desague-lavadora-{S.clave}/", f"Bomba de agua, bomba de desagüe o bomba de drenaje: es lo mismo", f"Qué es la bomba de agua de la lavadora {n}: bomba de desagüe, bomba de drenaje, motobomba. Nombres de la misma pieza.",
      f"Bomba de agua o bomba de desagüe de la lavadora {n}: ¿es lo mismo?",
      f"<p>Sí. Cuando alguien busca la «bomba de agua de la lavadora» casi siempre se refiere a la <b>bomba de desagüe</b>, que saca el agua de la tina. Se le dice también <b>bomba de drenaje</b>, <b>bomba de vaciado</b>, <b>bomba de evacuación</b> o <b>motobomba</b>.</p><p>Si tu lavadora {n} no desagua o hace ruido al vaciar, es esta pieza.</p>{cat}")
    for tipo, slg, ptxt in [("carga superior", "carga-superior", "se abre por arriba"), ("carga frontal", "carga-frontal", "se abre por el frente con una puerta redonda")]:
        G(f"/bomba-lavadora-{S.clave}-{slg}/", f"Bomba de agua para lavadora {n} de {tipo}", f"Bombas de desagüe para lavadoras {n} de {tipo}. Pregunta al asesor por WhatsApp y recibe en toda Colombia.",
          f"Bomba de agua para lavadora {n} de {tipo}",
          f"<p>La lavadora de {tipo} {ptxt}. Su bomba de desagüe es distinta a la de la otra, por eso conviene confirmar el modelo antes de comprar.</p>" + chips([(p["nombre"], f"/{p['slug']}/") for p in (([q for q in M["productos"] if q["carga"] == slg]) or M["productos"])]))
    for pref, tipo, slg in M["familias"]:
        G(f"/bomba-lavadora-{S.clave}-modelo-{pref.lower()}/", f"Bomba de agua para lavadora {n} {pref} ({tipo.lower()})", f"Bomba de desagüe para lavadoras {n} de la familia {pref}: {tipo.lower()}. El asesor confirma la referencia con tu modelo exacto.",
          f"Bomba de agua para lavadora {n} modelo {pref}",
          f"<p>Los modelos de lavadora {n} que empiezan por <b>{pref}</b> suelen ser de {tipo.lower()}. Cada modelo puede usar una bomba distinta, así que la referencia exacta se confirma con el modelo completo (por ejemplo, {pref}… y los números y letras que siguen) que aparece en la etiqueta.</p>"
          f"<p>Mándale al asesor el modelo completo por WhatsApp y te confirma la bomba, el precio y el envío.</p>" + chips([(p["nombre"], f"/{p['slug']}/") for p in (([q for q in M["productos"] if q["carga"] == slg]) or M["productos"])]))


def paginas_ciudad(S):
    M = S.M; n = M["nombre"]
    for c in S.ciudades:
        ciudad, depto = c[0], c[1]
        ruta = f"/bomba-lavadora-{S.clave}-{slug(ciudad)}/"
        h1 = f"Bomba de agua para lavadora {n} en {ciudad}"
        faq = [(f"¿Envían bombas para lavadora {n} a {ciudad}?", f"Sí. Enviamos por transportadora a {ciudad} ({depto}) y te mandamos el número de guía. Pregunta al asesor por el tiempo de entrega y si hay pago contra entrega en tu ciudad."),
               ("¿Cómo sé cuál bomba necesito?", "Mándale al asesor el modelo de tu lavadora o una foto de la bomba vieja por WhatsApp.")]
        cuerpo = f'''<div class="m-wrap">{S.miga((f"Lavadoras {n} en {ciudad}", None))}<div class="m-texto"><h1>{esc(h1)}</h1>
<p>Si tu lavadora {n} en {esc(ciudad)}, {esc(depto)}, no desagua o hace ruido al vaciar, aquí encuentras la bomba de desagüe (bomba de agua). La enviamos por transportadora y el asesor te confirma el modelo correcto antes de comprar.</p>
{chips([(p["nombre"], f"/{p['slug']}/") for p in M["productos"]])}
<p style="margin-top:16px">{S.boton_asesor(f"Hola, soy de {ciudad} y necesito la bomba de agua de mi lavadora {n}")}</p>
<h2>Preguntas frecuentes</h2>{faq_html(faq)}<p><a href="/bombas-lavadora-{S.clave}-por-ciudad/">Ver todas las ciudades →</a></p></div></div>
{bloque_entrega()}
{S.barra(f"Hola, soy de {ciudad} y necesito la bomba de agua de mi lavadora {n}")}'''
        S.pagina(ruta, f"{h1} | Envío por transportadora", f"Bomba de desagüe para lavadora {n} en {ciudad}, {depto}. Pregunta al asesor por WhatsApp y recibe en tu ciudad.", cuerpo,
                 [faq_ld(faq), S.breadcrumb((f"Lavadoras {n} en {ciudad}", None))], "0.6")
    cuerpo = f'<div class="m-wrap">{S.miga(("Ciudades", None))}<div class="m-texto"><h1>Bombas de agua para lavadora {n} en toda Colombia</h1><p>Elige tu ciudad.</p>{chips(S.chips_ciudad)}</div></div>'
    S.pagina(f"/bombas-lavadora-{S.clave}-por-ciudad/", f"Bombas para lavadora {n} por ciudad", f"Envíos de bombas de agua para lavadora {n} a {len(S.ciudades)} ciudades de Colombia.", cuerpo, [S.breadcrumb(("Ciudades", None))], "0.7")


# ---------------------------------------------------------------- legales, textos y portada
REEMPLAZOS = [("distribuidor autorizado", "vendedor"), ("Distribuidor autorizado", "Vendedor"), (" con autorización", ""),
              ("del nevecón", "de la lavadora"), ("al nevecón", "a la lavadora"), ("el nevecón", "la lavadora"), ("un nevecón", "una lavadora"), ("los nevecones", "las lavadoras"),
              ("nevecones", "lavadoras"), ("Nevecones", "Lavadoras"), ("nevecón", "lavadora"), ("Nevecón", "Lavadora"), ("nevecon", "lavadora"),
              ("las neveras", "las lavadoras"), ("neveras", "lavadoras"), ("nevera", "lavadora"), ("filtros de agua", "bombas de agua para lavadora"), ("Filtros de agua", "Bombas de agua para lavadora"),
              ("filtro de agua", "bomba de agua"), ("Filtro de agua", "Bomba de agua")]
L.REEMPLAZOS = REEMPLAZOS
L.QUIENES = """<?php $MARCA = 'home'; require __DIR__ . '/lav.php';
$n = sitio()['negocio'];
lav_cabeza('Quiénes somos | ' . $n['nombre'], 'Somos un comercio colombiano de bombas de agua (bombas de desagüe) para lavadoras Samsung y LG, con asesoría por WhatsApp y envíos a todo el país.', '/quienes-somos.php', '', '')
?>
<div class="m-wrap"><div class="m-texto"><h1>Quiénes somos</h1>
<p><?= h($n['nombre']) ?> es un comercio colombiano de bombas de agua (bombas de desagüe) para lavadoras. Te ayudamos a encontrar la bomba que necesita tu lavadora y te la enviamos a donde estés.</p>
<p>Antes de que compres, un asesor revisa contigo el modelo de tu lavadora por WhatsApp, para que pidas la bomba correcta.</p>
<p>Atendemos <?= h($n['horario']) ?>. Escríbenos por WhatsApp: __TELEFONOS__ o al correo <?= h($n['correo']) ?>.</p>
<p><?= h($n['nombre']) ?> · <?= h($n['titular']) ?> · <?= h($n['documento']) ?></p></div></div>
<?php lav_pie(); ?>
"""
L.LEGALES = {
    "terminos": ("Términos y condiciones", """<p>Este sitio presenta bombas de agua (bombas de desagüe) para lavadoras. No tiene carrito ni pago en línea: los pedidos se hacen por WhatsApp con un asesor y se pagan contra entrega.</p>
<h2>Cómo se hace un pedido</h2><p>Escribe al asesor por WhatsApp con el modelo de tu lavadora o una foto de la bomba vieja. El asesor te confirma la bomba, el precio, el valor del envío y si hay pago contra entrega en tu ciudad antes de despachar.</p>
<h2>Confirma antes de comprar</h2><p>Las fotos son de referencia. Antes de pagar, compara la bomba con la que tienes o confirma el modelo de tu lavadora con el asesor. La instalación es responsabilidad del comprador; si no tienes experiencia con la parte eléctrica o hidráulica, pídele ayuda a un técnico.</p>
<h2>Marcas</h2><p>Los nombres de marca se usan solo para indicar el tipo de lavadora. Somos un comercio independiente.</p>"""),
    "privacidad": ("Tratamiento de datos personales", """<p>Cuando nos escribes por WhatsApp usamos tu nombre, tu número y los datos que nos des (ciudad, dirección, modelo de la lavadora) solo para atender tu consulta, confirmar tu pedido y enviártelo.</p>
<p>No vendemos tus datos. Puedes pedirnos que los corrijamos o los eliminemos escribiéndonos por WhatsApp o al correo de contacto.</p>
<p>Este sitio puede usar herramientas de medición (como Google Analytics) para saber cuántas personas lo visitan.</p>"""),
    "garantia-y-retracto": ("Garantía y retracto", """<p>Si la bomba llega con algún defecto, escríbenos por WhatsApp con una foto y la revisamos.</p>
<p>Para compras a distancia puedes ejercer el derecho de retracto dentro de los 5 días hábiles siguientes a la entrega, según la ley colombiana, siempre que el producto no haya sido instalado ni usado y esté en buen estado. Coordina la devolución con el asesor.</p>
<p>Autoridad de protección al consumidor: <a href="https://www.sic.gov.co/" target="_blank" rel="noopener">Superintendencia de Industria y Comercio</a>.</p>"""),
}

HOME_FAQ = [
    ("¿Venden bombas de agua para lavadoras Samsung y LG?", "Sí. Tenemos bombas de desagüe (bomba de agua, bomba de drenaje) para lavadoras Samsung y LG, de carga superior y de carga frontal. Cada marca tiene su tienda y su asesor por WhatsApp."),
    ("¿Es lo mismo la bomba de agua que la bomba de desagüe?", "En una lavadora, sí: cuando se habla de la «bomba de agua» casi siempre es la bomba de desagüe que saca el agua de la tina. También se le llama bomba de drenaje o motobomba."),
    ("¿Cómo sé cuál bomba necesita mi lavadora?", "Escríbele al asesor de tu marca por WhatsApp con el modelo de la lavadora (etiqueta) o una foto de la bomba vieja. Te confirma cuál es antes de que compres."),
    ("¿Cuánto cuesta?", "El precio depende del modelo y la referencia. El asesor te responde por WhatsApp con el valor y el tiempo de entrega a tu ciudad."),
    ("¿Hacen envíos a toda Colombia?", "Sí, enviamos por transportadora a todo el país y te mandamos el número de guía."),
    ("¿Cómo pago?", "Con pago contra entrega: pagas cuando recibes el paquete. El asesor te confirma si está disponible en tu ciudad."),
]


def pagina_home(out, dominio, Ss):
    cuerpo_marcas = ""; tarj = ""
    for S in Ss:
        M = S.M; n = M["nombre"]
        fotos = "".join(f'<span class="lf">{foto_html(p, lazy=True)}</span>' for p in M["productos"][:3])
        cuerpo_marcas += (f'<article class="m-card marca-card"><div class="tx"><h3><a href="/{S.clave}/">Bombas de agua para lavadora {n}</a></h3>'
                          f'<div class="lav-fotos">{fotos}</div><p>Carga superior y carga frontal. Asesor por WhatsApp: {esc(M["telefono"])}.</p>'
                          f'<a class="m-btn block" href="/{S.clave}/">Ver bombas {n}</a>'
                          f'<a class="m-btn block wa" href="{esc(wa_link(M["whatsapp"], "Hola, necesito la bomba de agua de mi lavadora " + n))}" target="_blank" rel="noopener">💬 Asesor {n} por WhatsApp</a></div></article>')
        for p in M["productos"]:
            pr = f'<span class="pr">{cop(p["precio"])}</span>' if p["precio"] else '<span class="pr consulta">Consulta el precio<small>Te responde el asesor</small></span>'
            tarj += (f'<article class="m-card"><span class="m-tipo">{n} · {esc(p["tipo"])}</span><span class="im">{foto_html(p)}</span><div class="tx">'
                     f'<h3><a href="/{S.clave}/{p["slug"]}/">{esc(p["nombre"])}</a></h3>{pr}'
                     f'<a class="m-btn block wa" href="{esc(wa_link(M["whatsapp"], "Hola, quiero consultar por la " + p["nombre"]))}" target="_blank" rel="noopener">💬 Preguntar al asesor</a>'
                     f'<a class="m-link" href="/{S.clave}/{p["slug"]}/">Ver detalles</a></div></article>')
    ciudades_links = " · ".join(f'<a href="/{S.clave}/bombas-lavadora-{S.clave}-por-ciudad/">Ciudades {esc(S.M["nombre"])}</a>' for S in Ss)
    cuerpo = f'''<section class="m-hero"><div class="m-wrap">
  <div>
    <h1>Bombas de agua para lavadoras Samsung y LG</h1>
    <p class="lead">Bomba de desagüe (bomba de agua, bomba de drenaje) para lavadoras Samsung y LG de carga superior y carga frontal. Elige tu marca, cuéntale tu modelo al asesor por WhatsApp y te confirmamos la bomba correcta. Enviamos a toda Colombia.</p>
    <div class="acc"><a class="m-btn" href="#marcas">Elegir mi marca</a></div>
    <ul><li>Pago contra entrega</li><li>Envío a toda Colombia</li><li>Asesor que te confirma el modelo</li></ul>
  </div>
</div></section>
{confianza()}
<section class="m-sec" id="marcas"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Escoge tu marca</span><h2>¿De qué marca es tu lavadora?</h2></div><div class="m-grid lav-marcas">{cuerpo_marcas}</div></div></section>
<section class="m-sec alt" id="bombas"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Catálogo</span><h2>Todas las bombas</h2><p>Pregunta por la tuya y el asesor te confirma el modelo correcto antes de comprar.</p></div><div class="m-grid">{tarj}</div></div></section>
{bloque_importancia()}
{bloque_entrega()}
{tres_pasos()}
<section class="m-sec alt" id="preguntas"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Resolvemos tus dudas</span><h2>Preguntas frecuentes</h2></div>{faq_html(HOME_FAQ)}</div></section>
<section class="m-sec"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Envíos</span><h2>Enviamos a toda Colombia</h2></div><p>{ciudades_links}</p></div></section>'''
    cuerpo = cuerpo.replace('href="/cambio-e-instalacion/"', 'href="/samsung/cambio-e-instalacion/"').replace('href="/como-saber-si-la-bomba-esta-danada/"', 'href="/samsung/como-saber-si-la-bomba-esta-danada/"')
    ld = [{"@type": "WebSite", "name": "Bombas de agua para lavadoras", "url": dominio + PREF + "/"}, faq_ld(HOME_FAQ),
          {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i, "url": f"{dominio}{PREF}/{S.clave}/{p['slug']}/", "name": p["nombre"]} for i, (S, p) in enumerate([(S, p) for S in Ss for p in S.M["productos"]], 1)]}]
    escribir(out, PREF + "/", "home", "Bombas de agua para lavadoras Samsung y LG | Envío a toda Colombia",
             "Bomba de desagüe (bomba de agua) para lavadoras Samsung y LG de carga superior y frontal. Pregunta al asesor por WhatsApp y recibe en toda Colombia.", cuerpo, ld,
             f'<meta property="og:image" content="{dominio}{PREF}/img/{Ss[0].M["productos"][0]["id"]}.jpg">')


def marca_json(S, Ss):
    M = S.M; clave = S.clave; b = S.pref + "/"
    otras = [[f"Bombas para lavadora {o.M['nombre']}", f"{PREF}/{o.clave}/"] for o in Ss if o is not S] + [["Inicio", PREF + "/"]]
    guias_ = [[f"{b}cual-es-mi-bomba/", "¿Cuál bomba necesita mi lavadora?"], [f"{b}como-saber-si-la-bomba-esta-danada/", "Cómo saber si la bomba está dañada"],
              [f"{b}cambio-e-instalacion/", "Cómo cambiar la bomba"], [f"{b}lavadora-{clave}-no-desagua/", "La lavadora no desagua"],
              [f"{b}bomba-lavadora-{clave}-carga-superior/", "Bomba de carga superior"], [f"{b}bomba-lavadora-{clave}-carga-frontal/", "Bomba de carga frontal"]]
    return {"nombre": M["nombre"], "clase": M["clase"], "base": b, "tema": M["tema"], "fuentes": FUENTES, "tienda": M["tienda"], "logo": "", "logo_w": 0, "logo_h": 0, "icono": PREF + "/img/icono.svg",
            "whatsapp": M["whatsapp"], "telefono": M["telefono"], "productos": [[p["nombre"], p["slug"]] for p in M["productos"]], "guias": guias_,
            "ciudades": [[c, f"{b}bomba-lavadora-{clave}-{slug(c)}/"] for c in ["Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena", "Bucaramanga", "Pereira", "Manizales", "Armenia", "Ibagué", "Cúcuta", "Santa Marta"]],
            "hub": f"{b}bombas-lavadora-{clave}-por-ciudad/", "extra": otras, "externos": [list(M["oficial"]), ["Superintendencia de Industria y Comercio", "https://www.sic.gov.co/"]]}


def llms_php(Ss):
    txt = ("# Bombas de agua para lavadoras Samsung y LG\n\n> Bomba de desagüe (bomba de agua, bomba de drenaje, motobomba) para lavadoras Samsung y LG de carga superior y carga frontal, con envío a toda Colombia y pago contra entrega. "
           "El modelo correcto y el precio se confirman con un asesor por WhatsApp.\n")
    for S in Ss:
        M = S.M
        txt += f"\n## {M['nombre']} (WhatsApp {M['telefono']})\n- [Bombas de agua para lavadora {M['nombre']}](__BASE__{PREF}/{S.clave}/)\n"
        for p in M["productos"]:
            txt += f"- [{p['nombre']}](__BASE__{PREF}/{S.clave}/{p['slug']}/): {p['tipo']}.\n"
        txt += (f"- [Cuál bomba necesita mi lavadora](__BASE__{PREF}/{S.clave}/cual-es-mi-bomba/)\n- [Cómo cambiar la bomba](__BASE__{PREF}/{S.clave}/cambio-e-instalacion/)\n"
                f"- [Lavadora {M['nombre']} no desagua](__BASE__{PREF}/{S.clave}/lavadora-{S.clave}-no-desagua/)\n")
    txt += "\n## Preguntas y respuestas\n" + "".join(f"- **{q}** {a}\n" for q, a in HOME_FAQ)
    return "<?php\nrequire __DIR__ . '/api/sitio.php';\nheader('Content-Type: text/plain; charset=utf-8');\necho str_replace('__BASE__', sitio()['base'], <<<'TXT'\n" + txt + "TXT);\n"


# ---------------------------------------------------------------- construcción
def construir_todo(dominio):
    base = AQUI / "sitios" / "samsung"
    raiz = SALIDA / "tienda"                       # lo que se sube a public_html
    out = raiz / PREF.strip("/")                   # toda la tienda vive en /bombas-de-agua/
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
    mp = mp.replace("✔ Distribuidor autorizado ' . h($M['nombre']) . ' en Colombia", "✔ Bombas de agua para lavadora ' . h($M['nombre']) . ' en Colombia").replace("<small>Distribuidor autorizado</small>", "<small>Bombas para lavadora</small>")
    mp = mp.replace("Distribuidor autorizado de filtros de agua ' . h($M['nombre']) . ' en Colombia, con envío gratis a todo el país y pago seguro en línea.", "Bombas de agua para lavadora ' . h($M['nombre']) . ', con envío a todo el país y atención por WhatsApp.")
    mp = mp.replace("Distribuidor autorizado de filtros de agua ' . h($M['nombre']) . ' en Colombia. ' . h($M['nombre']) . ' y su logo son marcas registradas de su dueño y se usan con autorización.", "' . h($M['nombre']) . ' y su logo son marcas registradas de su dueño y se usan solo para indicar el tipo de lavadora.")
    mp = mp.replace('<script src="/carrito.js" defer></script>', '').replace("'</div><div class=\"m-wrap m-pie-medios\"><span>🔒 Pagos procesados en página segura</span>' . medios_pago_html() . '</div>'", "'</div>'")
    mp = re.sub(r"\$cart = '.*?';\n", "$cart = '';\n", mp, count=1, flags=re.S).replace("<a href=\"/carrito.php\">Mi carrito</a>", "").replace("🔒 Pago seguro en línea", "💵 Pago contra entrega")
    mp = mp.replace(" y pago seguro en línea", " y atención por WhatsApp")
    mp = mp.replace("Distribuidor autorizado", "Bombas para lavadora").replace("Precios en pesos colombianos con envío incluido.", "Precios en pesos colombianos.")
    mp = mp.replace("Cuándo cambiarlo y cómo instalarlo", "Cómo cambiar la bomba")
    mp = mp.replace("return '<b>' . h($M['nombre']) . '</b>';", "return '<b class=\"m-logo-txt\">' . h($M['tienda'] ?? $M['nombre']) . '</b>';").replace("<small>Bombas para lavadora</small>", "")
    mp = mp.replace("$tel = preg_replace('/\\D/', '', (string) (cfg()['whatsapp'] ?? ''));", "$tel = preg_replace('/\\D/', '', (string) ($M['whatsapp'] ?? (cfg()['whatsapp'] ?? '')));")
    mp = mp.replace("h($n['telefono']) . '</a>'", "h($M['telefono'] ?? $n['telefono']) . '</a>'")
    for a_, b_ in [("aria-label=\"Filtros '", "aria-label=\"Bombas de agua '"), ("$dd('Filtros', $filtros)", "$dd('Bombas', $filtros)"), ("'<b>Filtros</b>'", "'<b>Bombas</b>'"),
                   ("cual-es-mi-filtro/", "cual-es-mi-bomba/"), ("'<nav><b>Filtros ' . h($M['nombre'])", "'<nav><b>Bombas ' . h($M['nombre'])"),
                   (">Filtros ' . h($M['nombre']) . ' en '", ">Bombas para lavadora ' . h($M['nombre']) . ' en '"), ("¿Cuál filtro es el mío?", "¿Cuál bomba es la mía?"),
                   ("content=\"Filtros '", "content=\"Bombas de agua '"), ("(filtros, guías, ciudades)", "(bombas, guías, ciudades)"),
                   ("Envío gratis a toda Colombia", "Envío a toda Colombia"),
                   # rutas de esta tienda: todo bajo /bombas-de-agua/
                   ('href="/marcas.css"', f'href="{PREF}/marcas.css"'), ('href="/estilo.css"', f'href="{PREF}/estilo.css"'), ("'/img/icono.svg'", f"'{PREF}/img/icono.svg'"),
                   ('href="/terminos.php"', f'href="{PREF}/terminos.php"'), ('href="/privacidad.php"', f'href="{PREF}/privacidad.php"'),
                   ('href="/garantia-y-retracto.php"', f'href="{PREF}/garantia-y-retracto.php"'), ('href="/quienes-somos.php"', f'href="{PREF}/quienes-somos.php"')]:
        mp = mp.replace(a_, b_)
    (out / "marcas.php").write_text(mp, encoding="utf-8")
    for f in ["partes.php", "404.php"]:
        t = (out / f).read_text(encoding="utf-8").replace("Filtros<b>Lavadoras</b>", "Bombas<b>Lavadoras</b>")
        (out / f).write_text(t, encoding="utf-8")
    (out / "marcas.css").write_text((out / "marcas.css").read_text(encoding="utf-8") + CSS_EXTRA, encoding="utf-8")
    (out / "lav.php").write_text(LAV_PHP.replace("filtros para lavadoras (generado por lavadoras.py)", "bombas para lavadoras (generado por bombas.py)"), encoding="utf-8")
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
        S.chips_ciudad = [(c[0], f"/bomba-lavadora-{S.clave}-{slug(c[0])}/") for c in S.ciudades]
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
    home = {"nombre": "Samsung y LG", "clase": "samsung", "base": PREF + "/", "tema": "#071338", "fuentes": FUENTES, "tienda": "Bombas de agua para lavadoras", "logo": "", "logo_w": 0, "logo_h": 0, "icono": PREF + "/img/icono.svg",
            "whatsapp": "", "telefono": "", "productos": [[p["nombre"], f"{S.clave}/{p['slug']}"] for S in Ss for p in S.M["productos"]], "guias": [], "ciudades": [], "hub": None,
            "extra": [[f"Bombas para lavadora {S.M['nombre']}", f"{PREF}/{S.clave}/"] for S in Ss], "externos": [["Superintendencia de Industria y Comercio", "https://www.sic.gov.co/"]]}
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
    (out / "api" / "catalogo.php").write_text("<?php\n// Generado por bombas.py: no lo edites a mano.\nreturn " + php_val(cat) + ";\n", encoding="utf-8")
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
    inst.write_text(f"""# Bombas de agua para lavadoras Samsung y LG, dentro de {dominio}

Todo vive en la carpeta `bombas-de-agua/`, así que no pisa nada de la tienda de filtros (`/samsung/`, `/lg/`, `api/`, `.htaccess`, etc.).

- Portada: {dominio}{PREF}/ (elige marca)
- Samsung: {dominio}{PREF}/samsung/ (asesor WhatsApp {MARCAS['samsung']['telefono']})
- LG: {dominio}{PREF}/lg/ (asesor WhatsApp {MARCAS['lg']['telefono']})

Sin carrito ni pago en línea: los pedidos se hacen por WhatsApp con el asesor (pago contra entrega).

1. En Hostinger abre el administrador de archivos del dominio {dominio.split('//')[1]}, entra a `public_html`, sube `tienda-bombas-de-agua.zip` y descomprímelo ahí. Se crea solo la carpeta `bombas-de-agua`.
2. Dentro de `bombas-de-agua/api/` copia `config.sample.php` como `config.php` y completa el correo, el titular y el documento (iguales a los de la otra tienda). El Tag Manager ({GTM}) y la verificación de Search Console ya vienen puestos.
3. Cada clic en un botón de WhatsApp manda el mismo evento `whatsapp` a Tag Manager (con la marca, la página y el texto del botón), igual que en la tienda de filtros, así que cuenta como la misma conversión.
4. En Search Console agrega el sitemap {dominio}{PREF}/sitemap.xml (la propiedad es la misma).
5. Precios: mientras una bomba no tenga precio, su página dice «pregúntale al asesor».
""", encoding="utf-8")
    z = AQUI / "tienda-bombas-de-agua.zip"
    z.unlink(missing_ok=True)
    (AQUI / "tienda-bombas.zip").unlink(missing_ok=True)
    subprocess.run(["zip", "-qr", str(z), PREF.strip("/"), "-x", f"{PREF.strip('/')}/api/config.php", "-x", f"{PREF.strip('/')}/data/pedidos.sqlite*", "-x", f"{PREF.strip('/')}/data/correos.log"], cwd=raiz, check=True)
    sin_foto = [f"{S.M['nombre']} {p['tipo']}" for S in Ss for p in S.M["productos"] if p.get("provisional")]
    print(f"Bombas Samsung y LG: sitios-bombas/tienda{PREF}/ con {len(paginas)} páginas → {z.name}")
    if sin_foto:
        print("Fotos provisionales (faltan las reales):", ", ".join(sin_foto))


if __name__ == "__main__":
    construir_todo(sys.argv[1] if len(sys.argv) > 1 else "https://filtrosparalavadoras.click")
