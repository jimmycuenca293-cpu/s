#!/usr/bin/env python3
"""Tienda de filtros para lavadoras por marca (Samsung, LG).

Genera sitios-lavadoras/<marca>/ listo para subir a su propio dominio y tienda-lavadoras-<marca>.zip.
Parte del sitio por marca ya construido (sitios/samsung: legales, api) y le pone páginas propias de lavadoras.
Los precios y las referencias se llenan en PRODUCTOS: mientras un filtro no tenga precio, la página manda al asesor por WhatsApp.
"""
import html, json, re, shutil, subprocess, sys, unicodedata
from pathlib import Path
from PIL import Image

AQUI = Path(__file__).parent
BASE = AQUI / "sitios" / "samsung"          # sitio por marca ya generado (infraestructura común)
SALIDA = AQUI / "sitios-lavadoras"
FOTOS = AQUI / "imagenes-lavadoras"

esc = lambda s: html.escape(str(s), quote=True)
cop = lambda n: "$ " + f"{n:,}".replace(",", ".")


def slug(s):
    s = unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def ciudades():
    app = (AQUI.parent / "filtros-app" / "index.html").read_text(encoding="utf-8")
    m = re.search(r"\nconst CIUDADES_CO = (\[[^\n]*\]|\[.*?\n\]);", app, re.S)
    r = subprocess.run(["node", "-e", f"process.stdout.write(JSON.stringify({m.group(1)}))"], capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


# ---------------------------------------------------------------- datos por marca
MARCAS = {
    "samsung": {
        "nombre": "Samsung", "clase": "samsung", "tema": "#071338", "whatsapp": "3054796329", "telefono": "305 479 6329",
        "tienda": "Filtros para lavadora Samsung", "logo": "",
        "oficial": ("Samsung Colombia", "https://www.samsung.com/co/"),
        # precio: None = el cliente pregunta al asesor por WhatsApp. Cuando lo tengas, escribe el valor en pesos (ej. 45900).
        "productos": [
            {"id": "lav-sam-1", "inst": "rect", "foto": "foto-1.png", "slug": "filtro-pelusas-lavadora-samsung-azul", "corto": "Filtro de pelusas azul", "ref": None, "precio": None, "tipo": "Carga superior",
             "forma": "azul, con una rejilla de ranuras largas y una lengüeta para sacarlo"},
            {"id": "lav-sam-2", "inst": "rect", "foto": "foto-2.png", "slug": "filtro-pelusas-lavadora-samsung-gris-panal", "corto": "Filtro de pelusas gris tipo panal", "ref": None, "precio": None, "tipo": "Carga superior",
             "forma": "gris, con celdas en forma de panal y una leyenda en relieve"},
            {"id": "lav-sam-3", "inst": "rect", "foto": "foto-3.png", "slug": "filtro-pelusas-lavadora-samsung-negro-triangulos", "corto": "Filtro de pelusas negro con malla de triángulos", "ref": None, "precio": None, "tipo": "Carga superior",
             "forma": "negro translúcido, con una malla en triángulos y una tapa con lengüeta"},
            {"id": "lav-sam-4", "inst": "rect", "foto": "foto-4.webp", "slug": "filtro-pelusas-lavadora-samsung-verde", "corto": "Filtro de pelusas verde", "ref": None, "precio": None, "tipo": "Carga superior",
             "forma": "verde, con dos columnas de ranuras con malla metálica y una leyenda en relieve"},
            {"id": "lav-sam-5", "inst": "bolsa", "foto": "foto-5.png", "slug": "bolsa-malla-pelusas-lavadora-samsung", "corto": "Bolsa de malla para pelusas", "ref": None, "precio": None, "tipo": "Bolsa de malla",
             "forma": "una bolsa de malla blanca con un marco plástico para engancharla"},
            {"id": "lav-sam-6", "inst": "asa", "foto": "foto-6.png", "slug": "filtro-pelusas-lavadora-samsung-carga-frontal", "corto": "Filtro para lavadora de carga frontal", "ref": None, "precio": None, "tipo": "Carga frontal",
             "forma": "blanco, con un asa ancha y una malla de tela para las pelusas"},
        ],
    },
    "lg": {
        "nombre": "LG", "clase": "lg", "tema": "#a50034", "whatsapp": "3205102995", "telefono": "320 510 2995",
        "tienda": "Filtros para lavadora LG", "logo": "",
        "oficial": ("LG Colombia", "https://www.lg.com/co/"),
        "productos": [
            {"id": "lav-lg-1", "inst": "bolsa", "foto": "foto-1.png", "slug": "bolsa-malla-pelusas-lavadora-lg", "corto": "Bolsa de malla para pelusas", "ref": None, "precio": None, "tipo": "Bolsa de malla",
             "forma": "una bolsa de malla blanca con un marco plástico gris que la sostiene"},
            {"id": "lav-lg-2", "inst": "redondo", "foto": "foto-2.png", "slug": "filtro-pelusas-redondo-lavadora-lg", "corto": "Filtro de pelusas redondo azul", "ref": None, "precio": None, "tipo": "Filtro redondo",
             "forma": "redondo, azul translúcido, con orificios y dos lengüetas laterales para sacarlo"},
            {"id": "lav-lg-3", "inst": "rect", "foto": "foto-3.png", "slug": "filtro-pelusas-gris-circulos-lavadora-lg", "corto": "Filtro de pelusas gris con círculos y rejillas", "ref": None, "precio": None, "tipo": "Filtro rectangular",
             "forma": "gris, rectangular, con 12 círculos de malla arriba y cinco rejillas de malla debajo"},
            {"id": "lav-lg-4", "inst": "rect", "foto": "foto-5.png", "slug": "filtro-pelusas-gris-tapa-flechas-lavadora-lg", "corto": "Filtro de pelusas gris con tapa de flechas", "ref": None, "precio": None, "tipo": "Filtro rectangular",
             "forma": "gris, rectangular, con una tapa con relieve de flechas y marcas para abrir y cerrar"},
            {"id": "lav-lg-5", "foto": "foto-6.png", "slug": "filtro-pelusas-secadora-lg", "corto": "Filtro de pelusas", "dest": "secadora", "inst": "secadora", "ref": None, "precio": None, "tipo": "Secadora",
             "forma": "blanco, de marco plástico con una malla fina de tela, que se coloca en la abertura de la puerta de la secadora"},
        ],
    },
}


INSTALACION = {
    "rect": ["Apaga y desconecta la lavadora, y espera a que la tina esté vacía.",
             "Ubica el filtro de pelusas usado: va dentro de la tina, en una de sus paredes, y se sostiene con una lengüeta.",
             "Halando de la lengüeta, sácalo hacia ti. Si está sujeto con clips, presiónalos a la vez.",
             "Compara el filtro nuevo con el viejo: debe tener el mismo tamaño y la misma forma de lengüeta.",
             "Alinea el filtro nuevo con la ranura y empújalo hasta que haga clic o quede firme.",
             "Revisa que no queden espacios por donde pasen las pelusas y haz una lavada corta para comprobar que no se mueve."],
    "redondo": ["Apaga y desconecta la lavadora, y vacía la tina.",
                "Ubica el filtro redondo: va en el fondo o en una pared de la tina, sujeto con dos lengüetas laterales.",
                "Presiona las dos lengüetas al mismo tiempo y gíralo o sácalo hacia ti, según tu modelo.",
                "Limpia el alojamiento con un trapo húmedo antes de poner el nuevo.",
                "Coloca el filtro nuevo alineando las lengüetas con las ranuras y presiona hasta que quede firme.",
                "Haz una lavada corta y revisa que el filtro no se haya movido."],
    "bolsa": ["Apaga y desconecta la lavadora, y espera a que la tina esté vacía.",
              "Ubica el marco plástico de la bolsa: va enganchado en una pared de la tina, con la malla hacia abajo.",
              "Desengancha el marco y saca la bolsa vieja. Sacúdela fuera de la tina.",
              "Revisa que el marco nuevo tenga la misma forma y tamaño que el viejo.",
              "Engancha el marco nuevo en el mismo lugar hasta que quede firme y deja la malla colgando dentro de la tina.",
              "Haz una lavada corta para comprobar que la bolsa queda bien sujeta."],
    "asa": ["Apaga y desconecta la lavadora, y espera a que la tina esté vacía.",
            "Ubica el filtro usado: tiene un asa ancha para sacarlo y una malla de tela para las pelusas.",
            "Sácalo halando del asa. Si está fijo con un seguro, suéltalo primero.",
            "Compara el filtro nuevo con el viejo: debe tener el mismo largo y la misma forma de asa.",
            "Pon el filtro nuevo en su lugar y empújalo hasta que quede firme.",
            "Haz una lavada corta y revisa que no se mueve ni deja pasar pelusas."],
    "secadora": ["Apaga y desconecta la secadora, y espera a que se enfríe.",
                 "Abre la puerta y ubica el filtro de pelusas: en muchas secadoras de carga frontal está en la parte baja de la abertura de la puerta.",
                 "Sácalo halándolo hacia arriba. Si no lo ves, revisa el manual o pregúntale al asesor por WhatsApp.",
                 "Quita las pelusas de la malla con la mano. Si tiene residuos de suavizante, enjuágalo con agua tibia y déjalo secar por completo.",
                 "Revisa que la malla no esté rota. Si tiene huecos, usa el filtro nuevo.",
                 "Inserta el filtro en su ranura hasta que quede firme y cierra la puerta."],
}
NOTA_INSTALACION = "Los pasos pueden variar un poco según el modelo. Si el tuyo es distinto, escríbele al asesor por WhatsApp y te explica cómo ponerlo."


def wa_link(numero, texto):
    from urllib.parse import quote
    return f"https://wa.me/57{numero}?text={quote(texto)}"


# ---------------------------------------------------------------- imágenes
def preparar_fotos(M, out):
    img = out / "img"
    img.mkdir(parents=True, exist_ok=True)
    for p in M["productos"]:
        im = Image.open(FOTOS / M["clase"] / p["foto"]).convert("RGBA")
        fondo = Image.new("RGBA", im.size, (255, 255, 255, 255))
        im = Image.alpha_composite(fondo, im).convert("RGB")  # las fotos con fondo transparente se ven sobre blanco
        caja = Image.eval(im.convert("L"), lambda v: 255 if v < 245 else 0).getbbox()  # recorta el margen blanco
        if caja:
            m = max(8, int(0.04 * max(im.size)))
            im = im.crop((max(0, caja[0] - m), max(0, caja[1] - m), min(im.width, caja[2] + m), min(im.height, caja[3] + m)))
        im.thumbnail((900, 900))
        w, h = im.size
        im.save(img / f"{p['id']}.jpg", quality=84, optimize=True)
        im.save(img / f"{p['id']}.webp", quality=82)
        im4 = im.copy(); im4.thumbnail((400, 400)); im4.save(img / f"{p['id']}-400.webp", quality=80)
        p["w"], p["h"] = w, h


def preparar_entrega(out):
    """Foto de la entrega del paquete: se repinta la etiqueta de la caja para que hable de lavadoras (la original decía otro producto)."""
    from PIL import ImageDraw, ImageFont
    im = Image.open(AQUI / "imagenes-tienda" / "entrega.jpg").convert("RGB")
    d = ImageDraw.Draw(im)
    caja = (684, 646, 1030, 800)
    base = (182, 142, 112)
    for y in range(caja[1], caja[3]):
        t = (y - caja[1]) / (caja[3] - caja[1])
        d.line([(caja[0], y), (caja[2], y)], fill=tuple(int(base[i] * (1 - 0.10 * t)) for i in range(3)))
    f1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34)
    f2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    d.text((694, 676), "Filtro de pelusas", font=f1, fill=(20, 45, 100))
    d.text((694, 722), "para su lavadora", font=f2, fill=(20, 45, 100))
    im.thumbnail((1100, 1100))
    img = out / "img"
    im.save(img / "entrega-lavadora.jpg", quality=84, optimize=True)
    im.save(img / "entrega-lavadora.webp", quality=82)
    im6 = im.copy(); im6.thumbnail((640, 640)); im6.save(img / "entrega-lavadora-640.webp", quality=80)


def preparar_importancia(out):
    im = Image.open(FOTOS / "importancia.webp").convert("RGB")
    im.thumbnail((1100, 1100))
    img = out / "img"
    im.save(img / "filtro-importancia.jpg", quality=84, optimize=True)
    im.save(img / "filtro-importancia.webp", quality=82)
    im6 = im.copy(); im6.thumbnail((640, 640)); im6.save(img / "filtro-importancia-640.webp", quality=80)


def bloque_importancia(n=""):
    """Sección: por qué es importante el filtro de pelusas de la lavadora."""
    return f'''<section class="m-sec lav-importancia"><div class="m-wrap lav-entrega lav-inv"><div class="lav-entrega-foto"><picture><source srcset="/img/filtro-importancia-640.webp 640w, /img/filtro-importancia.webp 1100w" sizes="(max-width:860px) 100vw, 520px" type="image/webp"><img src="/img/filtro-importancia.jpg" alt="Mujer colocando un filtro de pelusas en la tina de una lavadora de carga superior" width="1100" height="1100" loading="lazy"></picture></div>
<div class="lav-entrega-tx"><span class="eyebrow">Lo importante</span><h2>Por qué es importante el filtro de tu lavadora {n}</h2>
<p>El filtro de pelusas parece pequeño, pero hace un trabajo que se nota en cada lavada. Atrapa los hilos y las pelusas que sueltan las prendas, y así no se quedan en tu ropa ni en la máquina.</p>
<ul class="lav-puntos"><li><b>Cuida tu ropa.</b> Sin filtro, las pelusas se pegan a las prendas oscuras, a las toallas y a la ropa de los niños.</li>
<li><b>Protege el desagüe.</b> Las pelusas acumuladas pueden tapar la salida del agua y hacer que la lavadora desagüe lento.</li>
<li><b>Evita malos olores.</b> La pelusa mojada que se queda en la tina o en el filtro se descompone y huele mal.</li>
<li><b>Ayuda a que la lavadora rinda más años.</b> Una máquina limpia trabaja con menos esfuerzo.</li>
<li><b>Se cambia fácil.</b> Cuando la malla se rompe o se deforma, se reemplaza a mano en minutos.</li></ul>
<p><a class="m-btn sec" href="/cambio-e-instalacion/">Cómo limpiar y cambiar el filtro</a></p></div></div></section>'''


ENTREGA_FOTO = ('<picture><source srcset="/img/entrega-lavadora-640.webp 640w, /img/entrega-lavadora.webp 1100w" sizes="(max-width:860px) 100vw, 520px" type="image/webp">'
                '<img src="/img/entrega-lavadora.jpg" alt="Repartidor entregando el paquete con el filtro a una clienta que lo recibe en la puerta de su casa" width="1100" height="825" loading="lazy"></picture>')


def bloque_entrega(corto=False):
    """Sección «Pago contra entrega» con la foto de la entrega."""
    return f'''<section class="m-sec alt lav-entrega-sec"><div class="m-wrap lav-entrega"><div class="lav-entrega-foto">{ENTREGA_FOTO}</div>
<div class="lav-entrega-tx"><span class="eyebrow">Pago contra entrega</span><h2>Recibes el paquete y pagas</h2>
<p>Pides tu filtro por WhatsApp, el asesor te confirma el modelo, el valor y el envío, y lo recibes en tu casa. <b>Pagas cuando tienes el paquete en las manos.</b></p>
<ul class="m-ok"><li>Primero confirmas el filtro correcto con el asesor.</li><li>Te enviamos por transportadora, con número de guía.</li><li>Abres el paquete, lo revisas y pagas al recibir.</li></ul>
<p class="m-mut">El asesor te confirma si el pago contra entrega está disponible en tu ciudad.</p></div></div></section>'''


def confianza():
    return '''<section class="m-confianza"><div class="m-wrap"><div><span class="ic">💵</span><span><b>Pago contra entrega</b><small>Pagas al recibir el paquete</small></span></div><div><span class="ic">🚚</span><span><b>Envío a toda Colombia</b><small>Con número de guía</small></span></div><div><span class="ic">💬</span><span><b>Asesor por WhatsApp</b><small>Te confirma el modelo</small></span></div><div><span class="ic">🔧</span><span><b>Cambio fácil</b><small>Paso a paso, sin técnico</small></span></div></div></section>'''


def tres_pasos(n=""):
    return f'''<section class="m-sec"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Así de fácil</span><h2>Compra en 3 pasos</h2></div><div class="m-cols m-num"><div class="m-bloque"><h3>Escríbele al asesor</h3><p>Mándale el modelo de tu lavadora {n}o una foto del filtro viejo por WhatsApp.</p></div><div class="m-bloque"><h3>Confirma filtro y envío</h3><p>El asesor te dice cuál filtro es, el valor y el tiempo de entrega a tu ciudad.</p></div><div class="m-bloque"><h3>Recibe y paga</h3><p>Llega a tu casa con número de guía y pagas contra entrega.</p></div></div></div></section>'''


# ---------------------------------------------------------------- piezas de HTML
def foto_html(p, grande=False, lazy=True):
    sufijo = "" if grande else "-400"
    return (f'<picture><source srcset="/img/{p["id"]}{sufijo}.webp" type="image/webp"><img src="/img/{p["id"]}.jpg" alt="{esc(p["nombre"])}" '
            f'width="{p["w"]}" height="{p["h"]}" {"loading=\"lazy\"" if lazy else "fetchpriority=\"high\""}></picture>')


def faq_ld(faq):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in faq]}


def faq_html(faq):
    return "".join(f'<details class="m-faq"><summary>{esc(q)}</summary><p>{a}</p></details>' for q, a in faq)


def chips(items):
    return '<div class="m-chips">' + "".join(f'<a href="{esc(u)}">{esc(t)}</a>' for t, u in items) + "</div>"


def escribir(out, real, marca, titulo, desc, cuerpo, ld, extra_head=""):
    """Escribe una página PHP en out/<real>/index.php (real = ruta completa con el prefijo de la marca)."""
    carpeta = out / real.strip("/")
    carpeta.mkdir(parents=True, exist_ok=True)
    ldj = json.dumps({"@context": "https://schema.org", "@graph": ld}, ensure_ascii=False) if ld else ""
    prof = len(real.strip("/").split("/")) if real != "/" else 0
    php = ("<?php $MARCA = '" + marca + "'; require __DIR__ . '/" + "../" * prof + "lav.php';\n"
           "lav_cabeza(" + json.dumps(titulo, ensure_ascii=False) + ", " + json.dumps(desc, ensure_ascii=False) + ", " + json.dumps(real) + ", "
           + json.dumps(extra_head, ensure_ascii=False) + ", <<<'JSON'\n" + ldj + "\nJSON);\n?>\n" + cuerpo + "\n<?php lav_pie(); ?>\n")
    (carpeta / "index.php").write_text(php, encoding="utf-8")


class Sitio:
    def __init__(self, clave, dominio, out):
        self.M = MARCAS[clave]
        self.clave = clave
        self.raiz = dominio                 # https://dominio (para imágenes comunes)
        self.pref = "/" + clave             # cada marca vive en /samsung/ o /lg/
        self.dominio = dominio + self.pref
        self.out = out
        self.paginas = {}
        self.ciudades = ciudades()
        m = self.M
        for p in m["productos"]:
            p["nombre"] = f"{p['corto']} para {p.get('dest', 'lavadora')} {m['nombre']}"
        self.chips_ciudad = [(c[0], f"/filtro-lavadora-{self.clave}-{slug(c[0])}/") for c in self.ciudades]

    def enlaces(self, html_):
        """Los enlaces internos de la marca (carpetas, sin punto) llevan el prefijo /samsung/ o /lg/."""
        return re.sub(r'href="/(?!/)([^"#.]*)"', lambda m: f'href="{self.pref}/{m.group(1)}"', html_)

    # --- mensajes de WhatsApp
    def wa(self, texto):
        return wa_link(self.M["whatsapp"], texto)

    def boton_asesor(self, texto, clase="m-btn wa", etiqueta="💬 Preguntar al asesor por WhatsApp"):
        return f'<a class="{clase}" href="{esc(self.wa(texto))}" target="_blank" rel="noopener">{etiqueta}</a>'

    # --- escribe una página PHP
    def pagina(self, ruta, titulo, desc, cuerpo, ld=None, prioridad="0.8", extra_head=""):
        real = self.pref + ruta
        escribir(self.out, real, self.clave, titulo, desc, self.enlaces(cuerpo), ld, extra_head)
        self.paginas[real] = prioridad

    def barra(self, texto, chico="Pago contra entrega", boton="💬 Pedir por WhatsApp"):
        return f'<div class="m-barra"><span><small>{esc(chico)}</small><b>Asesor {esc(self.M["nombre"])}</b></span>{self.boton_asesor(texto, "m-btn wa", boton)}</div>'

    def miga(self, *partes):
        t = '<nav class="m-miga"><a href="/">' + esc(self.M["tienda"]) + "</a>"
        for nombre, url in partes:
            t += " › " + (f'<a href="{esc(url)}">{esc(nombre)}</a>' if url else esc(nombre))
        return t + "</nav>"

    def breadcrumb(self, *partes):
        items = [{"@type": "ListItem", "position": 1, "name": self.M["tienda"], "item": self.dominio + "/"}]
        for i, (n, u) in enumerate(partes, 2):
            items.append({"@type": "ListItem", "position": i, "name": n, **({"item": self.dominio + u} if u else {})})
        return {"@type": "BreadcrumbList", "itemListElement": items}


# ---------------------------------------------------------------- contenido
def faq_general(S):
    n = S.M["nombre"]
    return [
        (f"¿Para qué sirve el filtro de pelusas de la lavadora {n}?", "Atrapa las pelusas, los hilos y los residuos que se sueltan de la ropa durante el lavado. Así no se pegan en la ropa limpia ni tapan el desagüe de la lavadora."),
        ("¿Cada cuánto se limpia?", "Lo ideal es sacarlo y enjuagarlo después de cada 3 o 4 lavadas. Si lavas mucha ropa con pelusa, como toallas o cobijas, límpialo con más frecuencia. Cuando la malla se rompe o se deforma, hay que cambiarlo."),
        (f"¿Cómo sé cuál filtro necesita mi lavadora {n}?", f"Depende del modelo y de si tu lavadora es de carga superior o frontal. Escríbele al asesor por WhatsApp con una foto del filtro viejo o con el modelo de la lavadora (está en una etiqueta en la parte de atrás o dentro de la tapa) y te confirmamos cuál es."),
        ("¿Cuánto cuesta?", "El precio depende del tipo de filtro. Pregúntale al asesor por WhatsApp y te responde en el momento con el valor y el tiempo de entrega a tu ciudad."),
        ("¿Hacen envíos a toda Colombia?", "Sí. Enviamos por transportadora a todo el país y te mandamos el número de guía."),
        ("¿Puedo cambiarlo yo mismo?", "Sí. No necesitas técnico ni herramientas: se saca y se pone a mano en pocos minutos. Abajo está el paso a paso."),
        ("¿Cómo pago?", "Con pago contra entrega: pagas cuando recibes el paquete. El asesor te confirma si está disponible en tu ciudad."),
    ]


def pagina_inicio(S):
    M = S.M; n = M["nombre"]
    tarjetas = ""
    for p in M["productos"]:
        pr = f'<span class="pr">{cop(p["precio"])}<small>Envío gratis</small></span>' if p["precio"] else '<span class="pr consulta">Consulta el precio<small>Te responde el asesor</small></span>'
        tarjetas += (f'<article class="m-card"><span class="m-tipo">{esc(p["tipo"])}</span><span class="im">{foto_html(p)}</span><div class="tx">'
                     f'<h3><a href="/{p["slug"]}/">{esc(p["nombre"])}</a></h3>{pr}'
                     + S.boton_asesor(f"Hola, quiero consultar por el {p['nombre']}", "m-btn block wa", "💬 Preguntar al asesor")
                     + f'<a class="m-link" href="/{p["slug"]}/">Ver detalles</a></div></article>')
    faq = faq_general(S)
    cuerpo = f'''<section class="m-hero"><div class="m-wrap">
  <div>
    <h1>Filtros para lavadora {n}</h1>
    <p class="lead">Filtros de pelusas y bolsas de malla para lavadoras {n} de carga superior y de carga frontal. Cuéntale tu modelo al asesor por WhatsApp y te decimos cuál necesitas. Enviamos a toda Colombia.</p>
    <div class="acc">{S.boton_asesor(f"Hola, necesito un filtro para mi lavadora {n}")}<a class="m-btn sec" href="#filtros">Ver los filtros</a></div>
    <ul><li>Pago contra entrega</li><li>Envío a toda Colombia</li><li>Asesor que te confirma el modelo</li></ul>
  </div>
  <div class="lav-fotos">{"".join(f'<span class="lf">{foto_html(p, lazy=i>0)}</span>' for i, p in enumerate(M["productos"][:3]))}</div>
</div></section>
{confianza()}
<section class="m-sec" id="filtros"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Catálogo {n}</span><h2>Filtros para lavadora {n}</h2><p>{len(M["productos"])} tipos de filtro. Pregunta por el tuyo y el asesor te confirma el modelo correcto antes de comprar.</p></div><div class="m-grid">{tarjetas}</div></div></section>
<section class="m-sec alt"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Encuentra el tuyo</span><h2>¿Cuál filtro necesita mi lavadora {n}?</h2></div>
<div class="m-cols"><div><h3>Lavadora de carga superior</h3><p>Se abre por arriba. El filtro de pelusas suele ir dentro de la tina, en una pared, o es una bolsa de malla que se engancha. Mira si el tuyo se parece a los de arriba.</p></div>
<div><h3>Lavadora de carga frontal</h3><p>Se abre por el frente, con una puerta redonda. El filtro es distinto al de carga superior. Mira el filtro para carga frontal del catálogo.</p></div>
<div><h3>Si no estás segura o seguro</h3><p>Mándale al asesor una foto del filtro viejo y el modelo de tu lavadora. Te responde con el filtro que le corresponde.</p></div></div>
<p style="margin-top:14px"><a class="m-btn" href="/cual-es-mi-filtro/">Guía: cuál es mi filtro</a></p></div></section>
{bloque_importancia(n)}
{bloque_entrega()}
{tres_pasos(n + " ")}
<section class="m-sec"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Mantenimiento</span><h2>Cuándo limpiar o cambiar el filtro de tu lavadora {n}</h2></div>
<div class="m-texto"><p>Un filtro tapado hace que la ropa salga con pelusas, que la lavadora tarde más en desaguar y que huela mal. Sácalo y enjuágalo con agua después de cada 3 o 4 lavadas. Si la malla está rota, deformada o ya no se limpia bien, es hora de cambiarlo.</p></div>
<p><a class="m-btn sec" href="/cambio-e-instalacion/">Paso a paso para limpiar y cambiar el filtro</a></p></div></section>
<section class="m-sec alt" id="preguntas"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Resolvemos tus dudas</span><h2>Preguntas frecuentes sobre filtros de lavadora {n}</h2></div>{faq_html(faq)}</div></section>
<section class="m-sec"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Envíos</span><h2>Enviamos filtros para lavadora {n} a toda Colombia</h2><p>Escoge tu ciudad para ver el tiempo de entrega.</p></div>{chips(S.chips_ciudad[:24])}<p style="margin-top:12px"><a href="/filtros-lavadora-{S.clave}-por-ciudad/">Ver todas las ciudades →</a></p></div></section>
<section class="m-sec alt"><div class="m-wrap"><div class="m-cta"><div><h2>¿No sabes cuál es tu filtro?</h2><p>Mándanos una foto del filtro viejo o el modelo de tu lavadora por WhatsApp.</p></div>{S.boton_asesor(f"Hola, no sé cuál filtro necesita mi lavadora {n}")}</div></div></section>
{S.barra(f"Hola, necesito un filtro para mi lavadora {n}")}'''
    ld = [{"@type": "CollectionPage", "name": f"Filtros para lavadora {n}", "url": S.dominio + "/", "description": f"Filtros de pelusas y bolsas de malla para lavadoras {n} en Colombia."},
          {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i, "url": S.dominio + f"/{p['slug']}/", "name": p["nombre"]} for i, p in enumerate(M["productos"], 1)]},
          faq_ld(faq)]
    S.pagina("/", f"Filtros para lavadora {n} | Envío a toda Colombia", f"Filtros de pelusas y bolsas de malla para lavadoras {n} de carga superior y frontal. Pregunta al asesor por WhatsApp y recibe en toda Colombia.", cuerpo, ld, "1.0",
             f'<meta property="og:image" content="{S.raiz}/img/{M["productos"][0]["id"]}.jpg">')


def pasos_limpieza(n):
    return ["Desconecta la lavadora y espera a que la tina esté vacía.",
            "Ubica el filtro de pelusas: en carga superior va dentro de la tina o en una pared; en carga frontal, detrás de la tapa inferior o en el desagüe.",
            "Sácalo halando de la lengüeta o del asa. Ten un trapo a la mano por si cae agua.",
            "Retira las pelusas con la mano y enjuágalo con agua del grifo. Si tiene jabón pegado, usa un cepillo suave.",
            "Revisa la malla: si está rota, deformada o no se limpia, hay que cambiarlo por uno nuevo.",
            "Ponlo en su lugar hasta que quede firme y haz una lavada corta para comprobar que no gotea."]


def pagina_producto(S, p):
    M = S.M; n = M["nombre"]; d = p.get("dest", "lavadora")
    ciclo = "secado" if d == "secadora" else "lavado"
    efecto = f"se acumulen dentro de tu secadora" if d == "secadora" else f"tapen el desagüe de tu lavadora"
    otros = [(q["corto"], f"/{q['slug']}/") for q in M["productos"] if q is not p]
    faq = [(f"¿Este filtro sirve para mi {d} {n}?", f"Escríbele al asesor por WhatsApp con el modelo de tu {d} o una foto del filtro viejo y te confirmamos antes de que compres."),
           ("¿Cuánto cuesta?", "Pregunta al asesor por WhatsApp: te da el precio y el tiempo de entrega a tu ciudad."),
           ("¿Cómo lo cambio?", "Sacas el filtro viejo a mano y pones el nuevo en el mismo lugar. No se necesitan herramientas.")]
    if p["precio"]:
        precio = f'<span class="precio">{cop(p["precio"])}<small>Confirma disponibilidad y envío con el asesor</small></span>'
    else:
        precio = '<span class="precio consulta">Precio: pregúntale al asesor<small>Respuesta en el momento por WhatsApp</small></span>'
    compra = ""
    cuerpo = f'''<div class="m-wrap">{S.miga((p["corto"], None))}
<div class="m-prod">
  <div class="foto"><span class="m-badge">{esc(p["tipo"])}</span>{foto_html(p, True, False)}</div>
  <div class="info">
    <h1>{esc(p["nombre"])}</h1>
    <span class="sub">{d.capitalize()} {n} · {esc(p["tipo"])}</span>
    {precio}
    <div class="m-aviso"><span style="font-size:22px">💬</span><span><b>¿Sirve para tu {d}?</b>Antes de comprar, el asesor confirma contigo el modelo correcto. Mándale una foto del filtro viejo o el modelo de tu {d}.</span></div>
    {compra}
    {S.boton_asesor(f"Hola, quiero consultar por el {p['nombre']}", "m-btn block wa", "💬 Pedir o preguntar al asesor por WhatsApp")}
    <ul class="m-ok"><li><b>Envío a toda Colombia</b> por transportadora, con número de guía.</li><li><b>Fácil de cambiar</b>: sin técnico ni herramientas.</li><li><b>Pago contra entrega</b>: pagas cuando recibes el paquete (el asesor confirma si aplica en tu ciudad).</li></ul>
  </div>
</div></div>
<section class="m-sec alt"><div class="m-wrap"><div class="m-texto"><div class="m-cab"><span class="eyebrow">Descripción</span><h2>{esc(p["nombre"])}</h2></div>
<p>Es un {esc(p["corto"].lower())}: {p["forma"]}. Sirve para atrapar las pelusas y los residuos que sueltan las prendas durante el {ciclo}, de modo que no vuelvan a la ropa ni {efecto} {n}.</p>
<p>Si el tuyo ya está roto, deformado o la malla no se limpia bien, es el momento de cambiarlo. Para estar seguros de que es el que necesita tu {d}, el asesor revisa el modelo contigo por WhatsApp.</p></div></div></section>
<section class="m-sec"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Datos</span><h2>Ficha del producto</h2></div><dl class="m-ficha"><dt>Marca de la {d}</dt><dd>{n}</dd><dt>Tipo</dt><dd>{esc(p["tipo"])}</dd><dt>Descripción</dt><dd>{p["forma"]}</dd><dt>Instalación</dt><dd>A mano, sin herramientas</dd><dt>Precio</dt><dd>{cop(p["precio"]) if p["precio"] else "Consúltalo con el asesor por WhatsApp"}</dd><dt>Envío</dt><dd>A toda Colombia por transportadora</dd></dl></div></section>
{bloque_importancia(n)}
{bloque_entrega()}
<section class="m-sec alt"><div class="m-wrap"><section class="caja tutorial" id="instalacion"><h2>Cómo instalar el {esc(p["corto"].lower())}: paso a paso</h2><ol class="pasos">{"".join(f"<li>{esc(x)}</li>" for x in INSTALACION.get(p.get("inst"), pasos_limpieza(n)))}</ol><p class="m-mut">{NOTA_INSTALACION}</p></section></div></section>
<section class="m-sec"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Preguntas</span><h2>Preguntas frecuentes</h2></div>{faq_html(faq)}</div></section>
<section class="m-sec alt"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Más filtros</span><h2>Otros filtros {n}</h2></div>{chips(otros)}</div></section>
{S.barra(f"Hola, quiero consultar por el {p['nombre']}")}'''
    prod = {"@type": "Product", "name": p["nombre"], "image": f"{S.raiz}/img/{p['id']}.jpg", "brand": {"@type": "Brand", "name": n},
            "description": f"{p['corto']} para {d} {n} ({p['tipo']}). Envío a toda Colombia."}
    if p["precio"]:
        prod["offers"] = {"@type": "Offer", "priceCurrency": "COP", "price": p["precio"], "availability": "https://schema.org/InStock", "url": f"{S.dominio}/{p['slug']}/"}
    S.pagina(f"/{p['slug']}/", f"{p['nombre']} | Pago contra entrega", f"{p['corto']} para {d} {n} ({p['tipo']}). Pregunta al asesor por WhatsApp el precio y recibe en toda Colombia.", cuerpo,
             [prod, faq_ld(faq), S.breadcrumb((p["corto"], None))], "0.9", f'<link rel="preload" as="image" href="/img/{p["id"]}.webp"><meta property="og:image" content="{S.raiz}/img/{p["id"]}.jpg">')


def pagina_guia(S, ruta, titulo, desc, h1, cuerpo_html, faq=None):
    cuerpo = f'<div class="m-wrap">{S.miga((h1, None))}<div class="m-texto"><h1>{esc(h1)}</h1>{cuerpo_html}</div>' \
             f'<div class="m-cta" style="margin:24px 0"><div><h2>¿Quieres el filtro correcto?</h2><p>Escríbele al asesor por WhatsApp.</p></div>{S.boton_asesor(f"Hola, tengo una pregunta sobre el filtro de mi lavadora {S.M['nombre']}")}</div>' \
             + (f'<h2>Preguntas frecuentes</h2>{faq_html(faq)}' if faq else "") + "</div>"
    ld = [S.breadcrumb((h1, None))] + ([faq_ld(faq)] if faq else [])
    S.pagina(ruta, titulo, desc, cuerpo, ld, "0.8")


def guias(S):
    M = S.M; n = M["nombre"]
    cat = chips([(p["corto"], f"/{p['slug']}/") for p in M["productos"]])
    pagina_guia(S, "/cual-es-mi-filtro/", f"¿Cuál filtro necesita mi lavadora {n}? Guía", f"Cómo saber qué filtro de pelusas necesita tu lavadora {n}: carga superior o frontal, forma del filtro y modelo.",
                f"¿Cuál filtro necesita mi lavadora {n}?",
                f'<p>Para escoger bien tienes que mirar tres cosas: el tipo de carga de tu lavadora, cómo es el filtro viejo y el modelo de la lavadora.</p><h2>1. Tipo de carga</h2><p>Si la lavadora se abre por arriba es de carga superior. Si tiene una puerta redonda al frente, es de carga frontal. Los filtros son distintos.</p>'
                f'<h2>2. Cómo es tu filtro viejo</h2><p>Compáralo con los del catálogo: color, forma de las ranuras y si es de plástico con malla o una bolsa de tela.</p>{cat}'
                f'<h2>3. El modelo de la lavadora</h2><p>Está en una etiqueta en la parte de atrás, en un costado o dentro de la tapa. Con él, el asesor te confirma el filtro por WhatsApp.</p>', faq_general(S)[2:4])
    pagina_guia(S, "/cambio-e-instalacion/", f"Cómo limpiar y cambiar el filtro de pelusas de la lavadora {n}", f"Paso a paso para sacar, limpiar y cambiar el filtro de pelusas de una lavadora {n}, sin técnico y sin herramientas.",
                f"Cómo limpiar y cambiar el filtro de pelusas de la lavadora {n}",
                "<ol class='pasos'>" + "".join(f"<li>{esc(x)}</li>" for x in pasos_limpieza(n)) + "</ol><h2>Cada cuánto</h2><p>Enjuágalo cada 3 o 4 lavadas. Cámbialo cuando la malla se rompa o se deforme.</p>", faq_general(S)[:2])
    pagina_guia(S, f"/cada-cuanto-limpiar-filtro-lavadora-{S.clave}/", f"Cada cuánto limpiar el filtro de la lavadora {n}", f"Cada cuánto se limpia y cuándo se cambia el filtro de pelusas de una lavadora {n}.",
                f"Cada cuánto limpiar el filtro de la lavadora {n}",
                "<p>Lo recomendable es sacarlo y enjuagarlo cada 3 o 4 lavadas. Si lavas toallas, cobijas o ropa que suelta mucha pelusa, hazlo más seguido.</p><h2>Señales de que está tapado</h2><ul><li>La ropa sale con pelusas pegadas.</li><li>La lavadora tarda más en desaguar.</li><li>Hay mal olor en la tina.</li></ul><h2>Señales de que hay que cambiarlo</h2><ul><li>La malla está rota o abierta.</li><li>El plástico se deformó y ya no ajusta.</li><li>Aunque lo limpies, sigue dejando pasar pelusa.</li></ul>", faq_general(S)[1:2])
    pagina_guia(S, f"/lavadora-{S.clave}-deja-pelusas-en-la-ropa/", f"Lavadora {n} deja pelusas en la ropa: causas y solución", f"Por qué tu lavadora {n} deja pelusas en la ropa y cómo solucionarlo con el filtro de pelusas.",
                f"Lavadora {n} deja pelusas en la ropa",
                "<p>Cuando la ropa sale con pelusas, lo más común es que el filtro esté tapado, roto o mal puesto.</p><h2>Qué revisar</h2><ol class='pasos'><li>Saca el filtro de pelusas y límpialo.</li><li>Revisa que la malla no tenga huecos.</li><li>Comprueba que quedó bien ajustado en su lugar.</li><li>No sobrecargues la lavadora y separa la ropa que suelta mucha pelusa.</li></ol><p>Si la malla está dañada, cámbialo por uno nuevo.</p>")
    for tipo, slg, ptxt in [("carga superior", "carga-superior", "se abre por arriba"), ("carga frontal", "carga-frontal", "se abre por el frente con una puerta redonda")]:
        pagina_guia(S, f"/filtro-lavadora-{S.clave}-{slg}/", f"Filtro para lavadora {n} de {tipo}", f"Filtros de pelusas para lavadoras {n} de {tipo}. Pregunta al asesor por WhatsApp y recibe en toda Colombia.",
                    f"Filtro para lavadora {n} de {tipo}",
                    f"<p>La lavadora de {tipo} {ptxt}. Su filtro de pelusas es distinto al de la otra, por eso conviene confirmar el modelo antes de comprar.</p>{cat}")


def paginas_ciudad(S):
    M = S.M; n = M["nombre"]
    for c in S.ciudades:
        ciudad, depto = c[0], c[1]
        ruta = f"/filtro-lavadora-{S.clave}-{slug(ciudad)}/"
        h1 = f"Filtro para lavadora {n} en {ciudad}"
        faq = [(f"¿Envían filtros para lavadora {n} a {ciudad}?", f"Sí. Enviamos por transportadora a {ciudad} ({depto}) y te mandamos el número de guía. Pregunta al asesor por el tiempo de entrega y si hay pago contra entrega en tu ciudad."),
               ("¿Cómo sé cuál filtro necesito?", "Mándale al asesor una foto del filtro viejo o el modelo de tu lavadora por WhatsApp.")]
        cuerpo = f'''<div class="m-wrap">{S.miga((f"Lavadoras {n} en {ciudad}", None))}<div class="m-texto"><h1>{esc(h1)}</h1>
<p>Si tienes una lavadora {n} en {esc(ciudad)}, {esc(depto)}, aquí encuentras filtros de pelusas y bolsas de malla. Los enviamos por transportadora y el asesor te confirma el modelo correcto antes de comprar.</p>
{chips([(p["corto"], f"/{p['slug']}/") for p in M["productos"]])}
<p style="margin-top:16px">{S.boton_asesor(f"Hola, soy de {ciudad} y necesito un filtro para mi lavadora {n}")}</p>
<h2>Preguntas frecuentes</h2>{faq_html(faq)}<p><a href="/filtros-lavadora-{S.clave}-por-ciudad/">Ver todas las ciudades →</a></p></div></div>
{bloque_entrega()}
{S.barra(f"Hola, soy de {ciudad} y necesito un filtro para mi lavadora {n}")}'''
        S.pagina(ruta, f"{h1} | Envío por transportadora", f"Filtros de pelusas para lavadora {n} en {ciudad}, {depto}. Pregunta al asesor por WhatsApp y recibe en tu ciudad.", cuerpo,
                 [faq_ld(faq), S.breadcrumb((f"Lavadoras {n} en {ciudad}", None))], "0.6")
    cuerpo = f'<div class="m-wrap">{S.miga(("Ciudades", None))}<div class="m-texto"><h1>Filtros para lavadora {n} en toda Colombia</h1><p>Elige tu ciudad.</p>{chips(S.chips_ciudad)}</div></div>'
    S.pagina(f"/filtros-lavadora-{S.clave}-por-ciudad/", f"Filtros para lavadora {n} por ciudad", f"Envíos de filtros para lavadora {n} a {len(S.ciudades)} ciudades de Colombia.", cuerpo, [S.breadcrumb(("Ciudades", None))], "0.7")


# ---------------------------------------------------------------- infraestructura (copia del sitio por marca)
LAV_PHP = r'''<?php
// Piezas comunes de la tienda de filtros para lavadoras (generado por lavadoras.py)
require_once __DIR__ . '/marcas.php';
$MARCA = preg_replace('/[^a-z]/', '', (string) ($MARCA ?? 'home'));
$M = json_decode(file_get_contents(__DIR__ . "/marca-$MARCA.json"), true);
function lav_cabeza(string $titulo, string $desc, string $ruta, string $extra, string $json): void
{
    global $M;
    $ld = $json !== '' ? '<script type="application/ld+json">' . str_replace('__BASE__', sitio()['base'], $json) . '</script>' : '';
    cabeza_marca($M, $titulo, $desc, $ruta, $extra . $ld . lav_evento_whatsapp());
}
function lav_pie(): void { global $M; pie_marca($M); }
// Evento para Google Tag Manager: «whatsapp» al tocar cualquier enlace de WhatsApp
function lav_evento_whatsapp(): string
{
    global $M;
    return '<script>window.dataLayer=window.dataLayer||[];document.addEventListener("click",function(e){var a=e.target.closest(\'a[href*="wa.me/"]\');if(a){dataLayer.push({event:"whatsapp",ubicacion:a.classList.contains("wa-flot")?"boton_flotante":"enlace",boton:(a.textContent||"").trim().slice(0,60),pagina:location.pathname,marca:' . json_encode($M['nombre']) . '})}},true);</script>';
}
'''

CSS_EXTRA = '''
/* Tienda de lavadoras */
.lav-entrega{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:40px;align-items:center}
.lav-entrega-foto{border-radius:var(--r-foto,24px);overflow:hidden;box-shadow:0 18px 40px -20px rgba(0,0,0,.35)}.lav-entrega-foto img{width:100%;height:auto;display:block}
.lav-entrega-tx h2{margin:6px 0 10px}.lav-entrega-tx .m-mut{margin-top:10px;font-size:14px}
@media(max-width:860px){.lav-entrega{grid-template-columns:1fr;gap:20px}}
.m-barra .m-btn.wa{min-height:46px}
.lav-inv .lav-entrega-foto{order:2}.lav-inv .lav-entrega-tx{order:1}
@media(max-width:860px){.lav-inv .lav-entrega-foto{order:0}.lav-inv .lav-entrega-tx{order:0}}
.lav-puntos{list-style:none;margin:12px 0;padding:0;display:grid;gap:10px}.lav-puntos li{padding:10px 14px;border-radius:12px;background:var(--panel,#f4f6fb);border:1px solid var(--line,#dde2f1)}
/* LG: misma estructura que Samsung (cabecera y pie oscuros) con el rojo y el blanco de la marca */
body.m-lg{--f-titulo:"Plus Jakarta Sans",system-ui,sans-serif;--f-texto:"Plus Jakarta Sans",system-ui,sans-serif;--ls-marca:.22em;
  --pri:#a50034;--ink:#2a0a14;--muted:#6b5058;--fondo:#ffffff;--panel:#fbf0f3;--card:#ffffff;--suave:#f8e0e7;--line:#f0d3dc;--ok:#0f8a5f;
  --anuncio:#a50034;--pie:#5c001c;--hero-bg:radial-gradient(1100px 480px at 85% -10%,#d4144f 0%,transparent 60%),linear-gradient(160deg,#5c001c 0%,#a50034 100%);--hero-ink:#fff;--hero-acento:#ffb3c8;
  --r-btn:999px;--r-card:18px;--r-foto:24px;--r-ic:12px;--card-borde:1px solid var(--line);--card-sombra:none}
body.m-lg .m-sello b{color:#a50034}
body.m-lg .m-hero .m-btn:not(.sec){background:#fff;color:#a50034}
body.m-lg .m-cta{background:linear-gradient(120deg,#a50034,#7a0026);color:#fff}body.m-lg .m-cta h2{color:#fff}

.m-logo-txt{font-size:20px;font-weight:800;letter-spacing:-.01em;color:inherit}.m-sello{gap:0}
.m-btn.wa{background:#1fa855;border-color:#1fa855;color:#fff}.m-btn.wa:hover{filter:brightness(1.07)}
.lav-fotos{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;align-self:center}.lav-fotos .lf{background:#fff;border-radius:14px;padding:8px;height:200px;display:grid;place-items:center;overflow:hidden}.lav-fotos picture{display:grid;place-items:center;width:100%;height:100%}.lav-fotos img{width:100%;height:100%;object-fit:contain}
.pr.consulta,.precio.consulta{font-size:16px;font-weight:700}
.m-faq{border:1px solid rgba(128,128,128,.3);border-radius:10px;padding:10px 14px;margin:8px 0}.m-faq summary{font-weight:700;cursor:pointer}
.m-texto h1{margin-bottom:12px}.m-miga{margin:14px 0;font-size:14px}
'''



REEMPLAZOS = [
    ("distribuidor autorizado", "vendedor"), ("Distribuidor autorizado", "Vendedor"), (" con autorización", ""), ("es vendedor de filtros de agua", "vende filtros de pelusas para lavadoras"),
    ("del nevecón", "de la lavadora"), ("al nevecón", "a la lavadora"), ("el nevecón", "la lavadora"), ("un nevecón", "una lavadora"), ("los nevecones", "las lavadoras"), ("de nevecones", "de lavadoras"),
    ("nevecones", "lavadoras"), ("Nevecones", "Lavadoras"), ("nevecón", "lavadora"), ("Nevecón", "Lavadora"), ("nevecon", "lavadora"),
    ("las neveras", "las lavadoras"), ("neveras", "lavadoras"), ("nevera", "lavadora"), ("Filtros de agua", "Filtros de pelusas"), ("filtros de agua", "filtros de pelusas"),
    ("Filtro de agua", "Filtro de pelusas"), ("filtro de agua", "filtro de pelusas"),
]
QUIENES = """<?php $MARCA = 'home'; require __DIR__ . '/lav.php';
$n = sitio()['negocio'];
lav_cabeza('Quiénes somos | ' . $n['nombre'], 'Somos un comercio colombiano de filtros de pelusas para lavadoras, con asesoría por WhatsApp y envíos a todo el país.', '/quienes-somos.php', '', '');
?>
<div class="m-wrap"><div class="m-texto"><h1>Quiénes somos</h1>
<p><?= h($n['nombre']) ?> es un comercio colombiano de filtros de pelusas y bolsas de malla para lavadoras. Te ayudamos a encontrar el filtro que necesita tu lavadora y te lo enviamos a donde estés.</p>
<p>Antes de que compres, un asesor revisa contigo el modelo de tu lavadora por WhatsApp, para que pidas el filtro correcto.</p>
<p>Atendemos <?= h($n['horario']) ?>. Escríbenos por WhatsApp: __TELEFONOS__ o al correo <?= h($n['correo']) ?>.</p>
<p><?= h($n['nombre']) ?> · <?= h($n['titular']) ?> · <?= h($n['documento']) ?></p></div></div>
<?php lav_pie(); ?>
"""


def limpiar_textos(out):
    for f in ["404.php", "partes.php", "marcas.php", "api/lib.php"]:
        p = out / f
        t = p.read_text(encoding="utf-8")
        t = t.replace(", distribuidor autorizado\"", "\"")
        for a, b in REEMPLAZOS:
            t = t.replace(a, b)
        p.write_text(t, encoding="utf-8")
    (out / "quienes-somos.php").write_text(QUIENES, encoding="utf-8")


LEGALES = {
    "terminos": ("Términos y condiciones", """<p>Este sitio presenta filtros de pelusas y bolsas de malla para lavadoras. No tiene carrito ni pago en línea: los pedidos se hacen por WhatsApp con un asesor y se pagan contra entrega.</p>
<h2>Cómo se hace un pedido</h2><p>Escribe al asesor por WhatsApp con el modelo de tu lavadora o una foto del filtro viejo. El asesor te confirma el filtro, el precio, el valor del envío y si hay pago contra entrega en tu ciudad antes de que compres.</p><h2>Pago contra entrega</h2><p>Pagas cuando recibes el paquete. Revisa el producto al recibirlo. Si el envío no tiene pago contra entrega en tu ciudad, el asesor te lo dice antes de despachar y acuerdas con él otra forma de pago.</p>
<h2>Confirma antes de comprar</h2><p>Las fotos son de referencia. Antes de pagar, compara el filtro con el que tienes o confirma el modelo de tu lavadora con el asesor.</p>
<h2>Marcas</h2><p>Los nombres de marca se usan solo para indicar el tipo de lavadora. Somos un comercio independiente.</p>"""),
    "privacidad": ("Tratamiento de datos personales", """<p>Cuando nos escribes por WhatsApp usamos tu nombre, tu número y los datos que nos des (ciudad, dirección, modelo de la lavadora) solo para atender tu consulta, confirmar tu pedido y coordinar el envío.</p>
<p>No vendemos tus datos. Puedes pedirnos que los corrijamos o los eliminemos escribiéndonos por WhatsApp o al correo de contacto.</p>
<p>Este sitio puede usar herramientas de medición (como Google Analytics) para saber cuántas personas lo visitan.</p>"""),
    "garantia-y-retracto": ("Garantía y retracto", """<p>Si el filtro llega con algún defecto, escríbenos por WhatsApp con una foto y lo revisamos.</p>
<p>Para compras a distancia puedes ejercer el derecho de retracto dentro de los 5 días hábiles siguientes a la entrega, según la ley colombiana, siempre que el producto no haya sido usado y esté en buen estado. Coordina la devolución con el asesor.</p>
<p>Autoridad de protección al consumidor: <a href="https://www.sic.gov.co/" target="_blank" rel="noopener">Superintendencia de Industria y Comercio</a>.</p>"""),
}


def legales(out):
    for nombre, (titulo, cuerpo) in LEGALES.items():
        php = ("<?php $MARCA = 'home'; require __DIR__ . '/lav.php';\n$n = sitio()['negocio'];\nlav_cabeza(" + json.dumps(titulo + " | ", ensure_ascii=False) + " . $n['nombre'], " + json.dumps(titulo, ensure_ascii=False)
               + ", '/" + nombre + ".php', '', '');\n?>\n<div class=\"m-wrap\"><div class=\"m-texto\"><h1>" + titulo + "</h1>" + cuerpo
               + "<p><?= h($n['nombre']) ?> · <?= h($n['titular']) ?> · <?= h($n['documento']) ?> · <?= h($n['correo']) ?></p></div></div>\n<?php lav_pie(); ?>\n")
        (out / (nombre + ".php")).write_text(php, encoding="utf-8")


HOME_FAQ = [
    ("¿Hacen filtros para lavadoras Samsung y LG?", "Tenemos filtros de pelusas y bolsas de malla para lavadoras Samsung y para lavadoras y secadoras LG. Cada marca tiene su página y su asesor por WhatsApp."),
    ("¿Cómo sé cuál filtro necesita mi lavadora?", "Escríbele al asesor de tu marca por WhatsApp con una foto del filtro viejo o con el modelo de la lavadora. Te confirma cuál es antes de que compres."),
    ("¿Cuánto cuesta?", "El precio depende del filtro. El asesor te responde por WhatsApp con el valor y el tiempo de entrega a tu ciudad."),
    ("¿Hacen envíos a toda Colombia?", "Sí, enviamos por transportadora a todo el país y te mandamos el número de guía."),
    ("¿Cómo pago?", "Con pago contra entrega: pagas cuando recibes el paquete. El asesor te confirma si está disponible en tu ciudad."),
]


def pagina_home(out, dominio, Ss):
    tarj = ""
    cuerpo_marcas = ""
    for S in Ss:
        M = S.M; n = M["nombre"]
        fotos = "".join(f'<span class="lf">{foto_html(p, lazy=True)}</span>' for p in M["productos"][:3])
        cuerpo_marcas += (f'<article class="m-card marca-card"><div class="tx"><h3><a href="/{S.clave}/">Filtros para lavadora {n}</a></h3>'
                          f'<div class="lav-fotos">{fotos}</div><p>{len(M["productos"])} filtros y bolsas de malla. Asesor por WhatsApp: {esc(M["telefono"])}.</p>'
                          f'<a class="m-btn block" href="/{S.clave}/">Ver filtros {n}</a>'
                          + f'<a class="m-btn block wa" href="{esc(wa_link(M["whatsapp"], "Hola, necesito un filtro para mi lavadora " + n))}" target="_blank" rel="noopener">💬 Asesor {n} por WhatsApp</a></div></article>')
        for p in M["productos"]:
            pr = f'<span class="pr">{cop(p["precio"])}</span>' if p["precio"] else '<span class="pr consulta">Consulta el precio<small>Te responde el asesor</small></span>'
            tarj += (f'<article class="m-card"><span class="m-tipo">{n} · {esc(p["tipo"])}</span><span class="im">{foto_html(p)}</span><div class="tx">'
                     f'<h3><a href="/{S.clave}/{p["slug"]}/">{esc(p["nombre"])}</a></h3>{pr}'
                     + f'<a class="m-btn block wa" href="{esc(wa_link(M["whatsapp"], "Hola, quiero consultar por el " + p["nombre"]))}" target="_blank" rel="noopener">💬 Preguntar al asesor</a>'
                     + f'<a class="m-link" href="/{S.clave}/{p["slug"]}/">Ver detalles</a></div></article>')
    cuerpo = f'''<section class="m-hero"><div class="m-wrap">
  <div>
    <h1>Filtros para lavadoras Samsung y LG</h1>
    <p class="lead">Filtros de pelusas y bolsas de malla para lavadoras Samsung y LG, y filtro para secadora LG. Elige tu marca, cuéntale tu modelo al asesor por WhatsApp y te decimos cuál necesitas. Enviamos a toda Colombia.</p>
    <div class="acc"><a class="m-btn" href="#marcas">Elegir mi marca</a></div>
    <ul><li>Pago contra entrega</li><li>Envío a toda Colombia</li><li>Asesor que te confirma el modelo</li></ul>
  </div>
</div></section>
{confianza()}
<section class="m-sec" id="marcas"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Escoge tu marca</span><h2>¿De qué marca es tu lavadora?</h2></div><div class="m-grid lav-marcas">{cuerpo_marcas}</div></div></section>
<section class="m-sec alt" id="filtros"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Catálogo</span><h2>Todos los filtros</h2><p>Pregunta por el tuyo y el asesor te confirma el modelo correcto antes de comprar.</p></div><div class="m-grid">{tarj}</div></div></section>
{bloque_importancia()}
{bloque_entrega()}
{tres_pasos()}
<section class="m-sec alt" id="preguntas"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Resolvemos tus dudas</span><h2>Preguntas frecuentes</h2></div>{faq_html(HOME_FAQ)}</div></section>
<section class="m-sec"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Envíos</span><h2>Enviamos a toda Colombia</h2></div><p>{" · ".join(f'<a href="/{S.clave}/filtros-lavadora-{S.clave}-por-ciudad/">Ciudades {esc(S.M["nombre"])}</a>' for S in Ss)}</p></div></section>'''
    ld = [{"@type": "WebSite", "name": "Filtros para lavadoras", "url": dominio + "/"}, faq_ld(HOME_FAQ),
          {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i, "url": f"{dominio}/{S.clave}/{p['slug']}/", "name": p["nombre"]} for i, (S, p) in enumerate([(S, p) for S in Ss for p in S.M["productos"]], 1)]}]
    cuerpo = cuerpo.replace('href="/cambio-e-instalacion/"', 'href="/samsung/cambio-e-instalacion/"')
    escribir(out, "/", "home", "Filtros para lavadoras Samsung y LG | Envío a toda Colombia", "Filtros de pelusas y bolsas de malla para lavadoras Samsung y LG. Pregunta al asesor por WhatsApp y recibe en toda Colombia.", cuerpo, ld,
             f'<meta property="og:image" content="{dominio}/img/{Ss[0].M["productos"][0]["id"]}.jpg">')


def marca_json(S, Ss):
    M = S.M; clave = S.clave; b = S.pref + "/"
    otras = [[f"Filtros para lavadora {o.M['nombre']}", f"/{o.clave}/"] for o in Ss if o is not S] + [["Inicio", "/"]]
    return {"nombre": M["nombre"], "clase": M["clase"], "base": b, "tema": M["tema"], "fuentes": FUENTES, "tienda": M["tienda"], "logo": "", "logo_w": 0, "logo_h": 0, "icono": "/img/icono.svg",
            "whatsapp": M["whatsapp"], "telefono": M["telefono"],
            "productos": [[p["nombre"], p["slug"]] for p in M["productos"]],
            "guias": [[f"{b}cual-es-mi-filtro/", "¿Cuál filtro necesita mi lavadora?"], [f"{b}cambio-e-instalacion/", "Cómo limpiar y cambiar el filtro"],
                      [f"{b}cada-cuanto-limpiar-filtro-lavadora-{clave}/", "Cada cuánto limpiar el filtro"], [f"{b}lavadora-{clave}-deja-pelusas-en-la-ropa/", "La lavadora deja pelusas"],
                      [f"{b}filtro-lavadora-{clave}-carga-superior/", "Filtro de carga superior"], [f"{b}filtro-lavadora-{clave}-carga-frontal/", "Filtro de carga frontal"]],
            "ciudades": [[c, f"{b}filtro-lavadora-{clave}-{slug(c)}/"] for c in ["Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena", "Bucaramanga", "Pereira", "Manizales", "Armenia", "Ibagué", "Cúcuta", "Santa Marta", "Villavicencio", "Neiva"]],
            "hub": f"{b}filtros-lavadora-{clave}-por-ciudad/", "extra": otras, "externos": [list(M["oficial"]), ["Superintendencia de Industria y Comercio", "https://www.sic.gov.co/"]]}


FUENTES = "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap"


def construir_todo(dominio):
    global BASE
    BASE = AQUI / "sitios" / "samsung"
    out = SALIDA / "tienda"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    # 1) infraestructura común
    for nombre in ["api", "data", ".htaccess", "404.php", "estilo.css", "marcas.css", "marcas.php", "partes.php", "robots.php"]:
        o = BASE / nombre
        if o.is_dir():
            shutil.copytree(o, out / nombre, ignore=shutil.ignore_patterns("pedidos.sqlite*", "correos.log", "config.php"))
        else:
            shutil.copy(o, out / nombre)
    # 2) textos: sin "distribuidor autorizado", sin carrito ni pagos
    mp = (out / "marcas.php").read_text(encoding="utf-8")
    mp = mp.replace("✔ Distribuidor autorizado ' . h($M['nombre']) . ' en Colombia", "✔ Filtros para lavadora ' . h($M['nombre']) . ' en Colombia").replace("<small>Distribuidor autorizado</small>", "<small>Filtros para lavadora</small>")
    mp = mp.replace("Distribuidor autorizado de filtros de agua ' . h($M['nombre']) . ' en Colombia, con envío gratis a todo el país y pago seguro en línea.", "Filtros de pelusas para lavadora ' . h($M['nombre']) . ', con envío a todo Colombia y pago seguro en línea.")
    mp = mp.replace("Distribuidor autorizado de filtros de agua ' . h($M['nombre']) . ' en Colombia. ' . h($M['nombre']) . ' y su logo son marcas registradas de su dueño y se usan con autorización.", "' . h($M['nombre']) . ' y su logo son marcas de su dueño y se mencionan solo para indicar el tipo de lavadora. Somos un comercio independiente.")
    mp = mp.replace('<script src="/carrito.js" defer></script>', '').replace("'</div><div class=\"m-wrap m-pie-medios\"><span>🔒 Pagos procesados en página segura</span>' . medios_pago_html() . '</div>'", "'</div>'")
    mp = re.sub(r"\$cart = '.*?';\n", "$cart = '';\n", mp, count=1, flags=re.S).replace("<a href=\"/carrito.php\">Mi carrito</a>", "").replace("🔒 Pago seguro en línea", "💵 Pago contra entrega")
    mp = mp.replace(" y pago seguro en línea", " y atención por WhatsApp")
    mp = mp.replace("Distribuidor autorizado", "Filtros para lavadora").replace("Precios en pesos colombianos con envío incluido.", "Precios en pesos colombianos.")
    mp = mp.replace("Cuándo cambiarlo y cómo instalarlo", "Cómo limpiarlo y cambiarlo")
    mp = mp.replace("return '<b>' . h($M['nombre']) . '</b>';", "return '<b class=\"m-logo-txt\">' . h($M['tienda'] ?? $M['nombre']) . '</b>';").replace("<small>Filtros para lavadora</small>", "")
    # cada marca (y la portada) usa su propio WhatsApp en el pie
    mp = mp.replace("$tel = preg_replace('/\\D/', '', (string) (cfg()['whatsapp'] ?? ''));", "$tel = preg_replace('/\\D/', '', (string) ($M['whatsapp'] ?? (cfg()['whatsapp'] ?? '')));")
    mp = mp.replace("h($n['telefono']) . '</a>'", "h($M['telefono'] ?? $n['telefono']) . '</a>'")
    (out / "marcas.php").write_text(mp, encoding="utf-8")
    (out / "marcas.css").write_text((out / "marcas.css").read_text(encoding="utf-8") + CSS_EXTRA, encoding="utf-8")
    (out / "lav.php").write_text(LAV_PHP, encoding="utf-8")
    limpiar_textos(out)
    lib = (out / "api" / "lib.php").read_text(encoding="utf-8")
    lib = lib.replace("$num = preg_replace('/\\D/', '', (string) (cfg()['whatsapp'] ?? ''));\n    if (strlen($num) === 10)", "$num = preg_replace('/\\D/', '', (string) (($GLOBALS['M']['whatsapp'] ?? null) ?? (cfg()['whatsapp'] ?? '')));\n    if (strlen($num) === 10)")
    (out / "api" / "lib.php").write_text(lib, encoding="utf-8")
    for f in ["pedido.php", "wompi.php", "estado.php", "reconciliar.php", "recordatorios.php"]:
        (out / "api" / f).unlink(missing_ok=True)  # sin pasarela de pagos: se vende por WhatsApp
    legales(out)
    tel = " · ".join(f"{m['nombre']} {m['telefono']}" for m in MARCAS.values())
    q = (out / "quienes-somos.php").read_text(encoding="utf-8").replace("__TELEFONOS__", tel)
    (out / "quienes-somos.php").write_text(q, encoding="utf-8")
    # 3) marcas
    (out / "img").mkdir(exist_ok=True)
    shutil.copy(BASE / "img" / "icono.svg", out / "img" / "icono.svg")
    preparar_entrega(out)
    preparar_importancia(out)
    Ss = [Sitio(c, dominio, out) for c in MARCAS]
    for S in Ss:
        preparar_fotos(S.M, out)
    for S in Ss:
        (out / f"marca-{S.clave}.json").write_text(json.dumps(marca_json(S, Ss), ensure_ascii=False), encoding="utf-8")
        pagina_inicio(S)
        for p in S.M["productos"]:
            pagina_producto(S, p)
        guias(S)
        paginas_ciudad(S)
    home = {"nombre": "Samsung y LG", "clase": "samsung", "base": "/", "tema": "#071338", "fuentes": FUENTES, "tienda": "Filtros para lavadoras", "logo": "", "logo_w": 0, "logo_h": 0, "icono": "/img/icono.svg",
            "whatsapp": "", "telefono": "", "productos": [[p["nombre"], f"{S.clave}/{p['slug']}"] for S in Ss for p in S.M["productos"]], "guias": [], "ciudades": [], "hub": None,
            "extra": [[f"Filtros para lavadora {S.M['nombre']}", f"/{S.clave}/"] for S in Ss], "externos": [["Superintendencia de Industria y Comercio", "https://www.sic.gov.co/"]]}
    (out / "marca-home.json").write_text(json.dumps(home, ensure_ascii=False), encoding="utf-8")
    (out / "marca.json").write_text(json.dumps(home, ensure_ascii=False), encoding="utf-8")
    pagina_home(out, dominio, Ss)
    paginas = {"/": "1.0"}
    for S in Ss:
        paginas.update(S.paginas)
    # 4) catálogo vacío (sin carrito), sitemap, llms, configuración
    cat = json.loads(subprocess.run(["php", "-r", "echo json_encode(include '" + str(BASE / 'api' / 'catalogo.php') + "', JSON_UNESCAPED_UNICODE);"], capture_output=True, text=True, check=True).stdout)
    cat["productos"] = {}
    cat["paginas"] = list(paginas.keys())
    cat["marcas"], cat["guias"], cat["compat"], cat["blog"], cat["rutas_ciudad"] = [], [], [], [], {}
    (out / "api" / "catalogo.php").write_text("<?php\n// Generado por lavadoras.py: no lo edites a mano.\nreturn " + php_val(cat) + ";\n", encoding="utf-8")
    (out / "sitemap.php").write_text(SITEMAP_PHP, encoding="utf-8")
    (out / "llms.php").write_text(llms_php(Ss), encoding="utf-8")
    cfg = (BASE / "api" / "config.sample.php").read_text(encoding="utf-8")
    sam = MARCAS["samsung"]
    cfg = cfg.replace("https://filtrosaguanevecones.com", dominio).replace("Filtros Nevecones Colombia", "Filtros para lavadoras").replace("321 799 6144", sam["telefono"]).replace("3217996144", sam["whatsapp"])
    cfg = cfg.replace("pedidos@filtrosaguanevecones.com", "pedidos@" + dominio.split("//")[1])
    cfg = cfg.replace("GTM-5WSNHV66", "GTM-5SCP73SQ")
    cfg = re.sub(r"('google_verificacion'\s*=>\s*)'[^']*'", r"\1'NsQML6RHpDIy79HzjoToyz_eOmWi97jh9G1I1ZwkUM4'", cfg)  # Search Console de filtrosparalavadoras.click
    (out / "api" / "config.sample.php").write_text(cfg, encoding="utf-8")
    # 5) zip único
    z = AQUI / "tienda-lavadoras.zip"
    z.unlink(missing_ok=True)
    subprocess.run(["zip", "-qr", str(z), ".", "-x", "api/config.php", "-x", "data/pedidos.sqlite*", "-x", "data/correos.log"], cwd=out, check=True)
    subprocess.run(["zip", "-qj", str(z), str(AQUI / "INSTALAR-lavadoras.md")], check=True)
    print(f"Lavadoras Samsung y LG: sitios-lavadoras/tienda/ con {len(paginas)} páginas → {z.name}")


def php_val(v, ind=0):
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, str):
        return "'" + v.replace("\\", "\\\\").replace("'", "\\'") + "'"
    if isinstance(v, list):
        return "[" + ", ".join(php_val(x) for x in v) + "]"
    return "[" + ", ".join(php_val(str(k) if not isinstance(k, int) else k) + " => " + php_val(x) for k, x in v.items()) + "]"


SITEMAP_PHP = '''<?php
require __DIR__ . '/api/sitio.php';
header('Content-Type: application/xml; charset=utf-8');
$b = sitio()['base'];
$cat = catalogo();
$urls = array_fill_keys($cat['paginas'], '0.8') + ['/quienes-somos.php' => '0.4', '/terminos.php' => '0.2', '/privacidad.php' => '0.2', '/garantia-y-retracto.php' => '0.3'];
$urls['/'] = '1.0';
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\\n" . '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\\n";
foreach ($urls as $u => $pr) echo '  <url><loc>' . htmlspecialchars($b . $u) . '</loc><lastmod>' . $cat['fecha'] . '</lastmod><priority>' . $pr . '</priority></url>' . "\\n";
echo '</urlset>';
'''


def llms_php(Ss):
    txt = "# Filtros para lavadoras Samsung y LG\n\n> Filtros de pelusas y bolsas de malla para lavadoras Samsung y LG, y filtro para secadora LG, con envío a toda Colombia. El precio y el modelo correcto se confirman con un asesor por WhatsApp.\n"
    for S in Ss:
        M = S.M
        txt += f"\n## {M['nombre']} (WhatsApp {M['telefono']})\n- [Filtros para lavadora {M['nombre']}](__BASE__/{S.clave}/)\n"
        for p in M["productos"]:
            txt += f"- [{p['nombre']}](__BASE__/{S.clave}/{p['slug']}/): {p['tipo']}.\n"
        txt += f"- [Cuál filtro necesita mi lavadora](__BASE__/{S.clave}/cual-es-mi-filtro/)\n- [Cómo limpiar y cambiar el filtro](__BASE__/{S.clave}/cambio-e-instalacion/)\n"
    return "<?php\nrequire __DIR__ . '/api/sitio.php';\nheader('Content-Type: text/plain; charset=utf-8');\necho str_replace('__BASE__', sitio()['base'], <<<'TXT'\n" + txt + "TXT);\n"


if __name__ == "__main__":
    dominio = sys.argv[1] if len(sys.argv) > 1 else "https://filtrosparalavadoras.click"
    construir_todo(dominio)
