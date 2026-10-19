#!/usr/bin/env python3
"""Tienda de filtros para lavadoras por marca (Samsung, LG).

Genera sitios-lavadoras/<marca>/ listo para subir a su propio dominio y tienda-lavadoras-<marca>.zip.
Parte del sitio por marca ya construido (sitios/samsung: carrito, pago, legales, api) y le pone páginas propias de lavadoras.
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
            {"id": "lav-sam-1", "foto": "foto-1.png", "slug": "filtro-pelusas-lavadora-samsung-azul", "corto": "Filtro de pelusas azul", "ref": None, "precio": None, "tipo": "Carga superior",
             "forma": "azul, con una rejilla de ranuras largas y una lengüeta para sacarlo"},
            {"id": "lav-sam-2", "foto": "foto-2.png", "slug": "filtro-pelusas-lavadora-samsung-gris-panal", "corto": "Filtro de pelusas gris tipo panal", "ref": None, "precio": None, "tipo": "Carga superior",
             "forma": "gris, con celdas en forma de panal y una leyenda en relieve"},
            {"id": "lav-sam-3", "foto": "foto-3.png", "slug": "filtro-pelusas-lavadora-samsung-negro-triangulos", "corto": "Filtro de pelusas negro con malla de triángulos", "ref": None, "precio": None, "tipo": "Carga superior",
             "forma": "negro translúcido, con una malla en triángulos y una tapa con lengüeta"},
            {"id": "lav-sam-4", "foto": "foto-4.webp", "slug": "filtro-pelusas-lavadora-samsung-verde", "corto": "Filtro de pelusas verde", "ref": None, "precio": None, "tipo": "Carga superior",
             "forma": "verde, con dos columnas de ranuras con malla metálica y una leyenda en relieve"},
            {"id": "lav-sam-5", "foto": "foto-5.png", "slug": "bolsa-malla-pelusas-lavadora-samsung", "corto": "Bolsa de malla para pelusas", "ref": None, "precio": None, "tipo": "Bolsa de malla",
             "forma": "una bolsa de malla blanca con un marco plástico para engancharla"},
            {"id": "lav-sam-6", "foto": "foto-6.png", "slug": "filtro-pelusas-lavadora-samsung-carga-frontal", "corto": "Filtro para lavadora de carga frontal", "ref": None, "precio": None, "tipo": "Carga frontal",
             "forma": "blanco, con un asa ancha y una malla de tela para las pelusas"},
        ],
    },
}


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
        im.thumbnail((900, 900))
        w, h = im.size
        im.save(img / f"{p['id']}.jpg", quality=84, optimize=True)
        im.save(img / f"{p['id']}.webp", quality=82)
        im4 = im.copy(); im4.thumbnail((400, 400)); im4.save(img / f"{p['id']}-400.webp", quality=80)
        p["w"], p["h"] = w, h


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


class Sitio:
    def __init__(self, clave, dominio):
        self.M = MARCAS[clave]
        self.clave = clave
        self.dominio = dominio
        self.out = SALIDA / clave
        self.paginas = {}      # ruta -> (prioridad, archivo)
        self.ciudades = ciudades()
        m = self.M
        for p in m["productos"]:
            p["nombre"] = f"{p['corto']} para lavadora {m['nombre']}"
        self.chips_ciudad = [(c[0], f"/filtro-lavadora-{self.clave}-{slug(c[0])}/") for c in self.ciudades]

    # --- mensajes de WhatsApp
    def wa(self, texto):
        return wa_link(self.M["whatsapp"], texto)

    def boton_asesor(self, texto, clase="m-btn wa", etiqueta="💬 Preguntar al asesor por WhatsApp"):
        return f'<a class="{clase}" href="{esc(self.wa(texto))}" target="_blank" rel="noopener">{etiqueta}</a>'

    # --- escribe una página PHP
    def pagina(self, ruta, titulo, desc, cuerpo, ld=None, prioridad="0.8", extra_head=""):
        carpeta = self.out / ruta.strip("/")
        carpeta.mkdir(parents=True, exist_ok=True)
        ldj = json.dumps({"@context": "https://schema.org", "@graph": ld}, ensure_ascii=False) if ld else ""
        php = ("<?php require __DIR__ . '/" + "../" * (len(ruta.strip("/").split("/")) if ruta != "/" else 0) + "lav.php';\n"
               "lav_cabeza(" + json.dumps(titulo, ensure_ascii=False) + ", " + json.dumps(desc, ensure_ascii=False) + ", " + json.dumps(ruta) + ", "
               + json.dumps(extra_head, ensure_ascii=False) + ", <<<'JSON'\n" + ldj + "\nJSON);\n?>\n" + cuerpo + "\n<?php lav_pie(); ?>\n")
        (carpeta / "index.php").write_text(php, encoding="utf-8")
        self.paginas[ruta] = prioridad

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
    <ul><li>Envío a toda Colombia</li><li>Pago seguro en línea</li><li>Asesor por WhatsApp</li></ul>
  </div>
  <div class="lav-fotos">{"".join(f'<span class="lf">{foto_html(p, lazy=i>0)}</span>' for i, p in enumerate(M["productos"][:3]))}</div>
</div></section>
<section class="m-sec" id="filtros"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Catálogo {n}</span><h2>Filtros para lavadora {n}</h2><p>{len(M["productos"])} tipos de filtro. Pregunta por el tuyo y el asesor te confirma el modelo correcto antes de comprar.</p></div><div class="m-grid">{tarjetas}</div></div></section>
<section class="m-sec alt"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Encuentra el tuyo</span><h2>¿Cuál filtro necesita mi lavadora {n}?</h2></div>
<div class="m-cols"><div><h3>Lavadora de carga superior</h3><p>Se abre por arriba. El filtro de pelusas suele ir dentro de la tina, en una pared, o es una bolsa de malla que se engancha. Mira si el tuyo se parece a los de arriba.</p></div>
<div><h3>Lavadora de carga frontal</h3><p>Se abre por el frente, con una puerta redonda. El filtro es distinto al de carga superior. Mira el filtro para carga frontal del catálogo.</p></div>
<div><h3>Si no estás segura o seguro</h3><p>Mándale al asesor una foto del filtro viejo y el modelo de tu lavadora. Te responde con el filtro que le corresponde.</p></div></div>
<p style="margin-top:14px"><a class="m-btn" href="/cual-es-mi-filtro/">Guía: cuál es mi filtro</a></p></div></section>
<section class="m-sec"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Mantenimiento</span><h2>Cuándo limpiar o cambiar el filtro de tu lavadora {n}</h2></div>
<div class="m-texto"><p>Un filtro tapado hace que la ropa salga con pelusas, que la lavadora tarde más en desaguar y que huela mal. Sácalo y enjuágalo con agua después de cada 3 o 4 lavadas. Si la malla está rota, deformada o ya no se limpia bien, es hora de cambiarlo.</p></div>
<p><a class="m-btn sec" href="/cambio-e-instalacion/">Paso a paso para limpiar y cambiar el filtro</a></p></div></section>
<section class="m-sec alt" id="preguntas"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Resolvemos tus dudas</span><h2>Preguntas frecuentes sobre filtros de lavadora {n}</h2></div>{faq_html(faq)}</div></section>
<section class="m-sec"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Envíos</span><h2>Enviamos filtros para lavadora {n} a toda Colombia</h2><p>Escoge tu ciudad para ver el tiempo de entrega.</p></div>{chips(S.chips_ciudad[:24])}<p style="margin-top:12px"><a href="/filtros-lavadora-{S.clave}-por-ciudad/">Ver todas las ciudades →</a></p></div></section>
<section class="m-sec alt"><div class="m-wrap"><div class="m-cta"><div><h2>¿No sabes cuál es tu filtro?</h2><p>Mándanos una foto del filtro viejo o el modelo de tu lavadora por WhatsApp.</p></div>{S.boton_asesor(f"Hola, no sé cuál filtro necesita mi lavadora {n}")}</div></div></section>'''
    ld = [{"@type": "CollectionPage", "name": f"Filtros para lavadora {n}", "url": S.dominio + "/", "description": f"Filtros de pelusas y bolsas de malla para lavadoras {n} en Colombia."},
          {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i, "url": S.dominio + f"/{p['slug']}/", "name": p["nombre"]} for i, p in enumerate(M["productos"], 1)]},
          faq_ld(faq)]
    S.pagina("/", f"Filtros para lavadora {n} | Envío a toda Colombia", f"Filtros de pelusas y bolsas de malla para lavadoras {n} de carga superior y frontal. Pregunta al asesor por WhatsApp y recibe en toda Colombia.", cuerpo, ld, "1.0",
             f'<meta property="og:image" content="{S.dominio}/img/{M["productos"][0]["id"]}.jpg">')


def pasos_limpieza(n):
    return ["Desconecta la lavadora y espera a que la tina esté vacía.",
            "Ubica el filtro de pelusas: en carga superior va dentro de la tina o en una pared; en carga frontal, detrás de la tapa inferior o en el desagüe.",
            "Sácalo halando de la lengüeta o del asa. Ten un trapo a la mano por si cae agua.",
            "Retira las pelusas con la mano y enjuágalo con agua del grifo. Si tiene jabón pegado, usa un cepillo suave.",
            "Revisa la malla: si está rota, deformada o no se limpia, hay que cambiarlo por uno nuevo.",
            "Ponlo en su lugar hasta que quede firme y haz una lavada corta para comprobar que no gotea."]


def pagina_producto(S, p):
    M = S.M; n = M["nombre"]
    otros = [(q["corto"], f"/{q['slug']}/") for q in M["productos"] if q is not p]
    faq = [(f"¿Este filtro sirve para mi lavadora {n}?", f"Escríbele al asesor por WhatsApp con el modelo de tu lavadora o una foto del filtro viejo y te confirmamos antes de que compres."),
           ("¿Cuánto cuesta?", "Pregunta al asesor por WhatsApp: te da el precio y el tiempo de entrega a tu ciudad."),
           ("¿Cómo lo cambio?", "Sacas el filtro viejo a mano y pones el nuevo en el mismo lugar. No se necesitan herramientas.")]
    if p["precio"]:
        precio = f'<span class="precio">{cop(p["precio"])}<small>Envío gratis a toda Colombia</small></span>'
        compra = (f'<div class="compra"><button class="m-btn block" type="button" data-add="{p["id"]}">Agregar al carrito</button>'
                  f'<button class="m-btn sec block" type="button" data-add="{p["id"]}" data-ir="1">Comprar ahora</button></div>')
    else:
        precio = '<span class="precio consulta">Precio: pregúntale al asesor<small>Respuesta en el momento por WhatsApp</small></span>'
        compra = '<div class="compra"></div>'
    cuerpo = f'''<div class="m-wrap">{S.miga((p["corto"], None))}
<div class="m-prod">
  <div class="foto"><span class="m-badge">{esc(p["tipo"])}</span>{foto_html(p, True, False)}</div>
  <div class="info">
    <h1>{esc(p["nombre"])}</h1>
    <span class="sub">Lavadora {n} · {esc(p["tipo"])}</span>
    {precio}
    <div class="m-aviso"><span style="font-size:22px">💬</span><span><b>¿Sirve para tu lavadora?</b>Antes de comprar, el asesor confirma contigo el modelo correcto. Mándale una foto del filtro viejo o el modelo de tu lavadora.</span></div>
    {compra}
    {S.boton_asesor(f"Hola, quiero consultar por el {p['nombre']}", "m-btn block wa", "💬 Preguntar al asesor por WhatsApp")}
    <ul class="m-ok"><li><b>Envío a toda Colombia</b> por transportadora, con número de guía.</li><li><b>Fácil de cambiar</b>: sin técnico ni herramientas.</li><li><b>Pago seguro</b> en línea.</li></ul>
  </div>
</div></div>
<section class="m-sec alt"><div class="m-wrap"><div class="m-texto"><div class="m-cab"><span class="eyebrow">Descripción</span><h2>{esc(p["nombre"])}</h2></div>
<p>Es un {esc(p["corto"].lower())}: {p["forma"]}. Sirve para atrapar las pelusas y los residuos que sueltan las prendas durante el lavado, de modo que no vuelvan a la ropa ni tapen el desagüe de tu lavadora {n}.</p>
<p>Si el tuyo ya está roto, deformado o la malla no se limpia bien, es el momento de cambiarlo. Para estar seguros de que es el que necesita tu lavadora, el asesor revisa el modelo contigo por WhatsApp.</p></div></div></section>
<section class="m-sec"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Datos</span><h2>Ficha del producto</h2></div><dl class="m-ficha"><dt>Marca de la lavadora</dt><dd>{n}</dd><dt>Tipo</dt><dd>{esc(p["tipo"])}</dd><dt>Descripción</dt><dd>{p["forma"]}</dd><dt>Instalación</dt><dd>A mano, sin herramientas</dd><dt>Precio</dt><dd>{cop(p["precio"]) if p["precio"] else "Consúltalo con el asesor por WhatsApp"}</dd><dt>Envío</dt><dd>A toda Colombia por transportadora</dd></dl></div></section>
<section class="m-sec alt"><div class="m-wrap"><section class="caja tutorial" id="instalacion"><h2>Cómo limpiar y cambiar el filtro: paso a paso</h2><ol class="pasos">{"".join(f"<li>{esc(x)}</li>" for x in pasos_limpieza(n))}</ol></section></div></section>
<section class="m-sec"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Preguntas</span><h2>Preguntas frecuentes</h2></div>{faq_html(faq)}</div></section>
<section class="m-sec alt"><div class="m-wrap"><div class="m-cab"><span class="eyebrow">Más filtros</span><h2>Otros filtros para lavadora {n}</h2></div>{chips(otros)}</div></section>'''
    prod = {"@type": "Product", "name": p["nombre"], "image": f"{S.dominio}/img/{p['id']}.jpg", "brand": {"@type": "Brand", "name": n},
            "description": f"{p['corto']} para lavadora {n} ({p['tipo']}). Envío a toda Colombia."}
    if p["precio"]:
        prod["offers"] = {"@type": "Offer", "priceCurrency": "COP", "price": p["precio"], "availability": "https://schema.org/InStock", "url": f"{S.dominio}/{p['slug']}/"}
    S.pagina(f"/{p['slug']}/", f"{p['nombre']} | Envío a toda Colombia", f"{p['corto']} para lavadora {n} ({p['tipo']}). Pregunta al asesor por WhatsApp el precio y recibe en toda Colombia.", cuerpo,
             [prod, faq_ld(faq), S.breadcrumb((p["corto"], None))], "0.9", f'<link rel="preload" as="image" href="/img/{p["id"]}.webp"><meta property="og:image" content="{S.dominio}/img/{p["id"]}.jpg">')


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
        faq = [(f"¿Envían filtros para lavadora {n} a {ciudad}?", f"Sí. Enviamos por transportadora a {ciudad} ({depto}) y te mandamos el número de guía. Pregunta al asesor por el tiempo de entrega."),
               ("¿Cómo sé cuál filtro necesito?", "Mándale al asesor una foto del filtro viejo o el modelo de tu lavadora por WhatsApp.")]
        cuerpo = f'''<div class="m-wrap">{S.miga((f"Lavadoras {n} en {ciudad}", None))}<div class="m-texto"><h1>{esc(h1)}</h1>
<p>Si tienes una lavadora {n} en {esc(ciudad)}, {esc(depto)}, aquí encuentras filtros de pelusas y bolsas de malla. Los enviamos por transportadora y el asesor te confirma el modelo correcto antes de comprar.</p>
{chips([(p["corto"], f"/{p['slug']}/") for p in M["productos"]])}
<p style="margin-top:16px">{S.boton_asesor(f"Hola, soy de {ciudad} y necesito un filtro para mi lavadora {n}")}</p>
<h2>Preguntas frecuentes</h2>{faq_html(faq)}<p><a href="/filtros-lavadora-{S.clave}-por-ciudad/">Ver todas las ciudades →</a></p></div></div>'''
        S.pagina(ruta, f"{h1} | Envío por transportadora", f"Filtros de pelusas para lavadora {n} en {ciudad}, {depto}. Pregunta al asesor por WhatsApp y recibe en tu ciudad.", cuerpo,
                 [faq_ld(faq), S.breadcrumb((f"Lavadoras {n} en {ciudad}", None))], "0.6")
    cuerpo = f'<div class="m-wrap">{S.miga(("Ciudades", None))}<div class="m-texto"><h1>Filtros para lavadora {n} en toda Colombia</h1><p>Elige tu ciudad.</p>{chips(S.chips_ciudad)}</div></div>'
    S.pagina(f"/filtros-lavadora-{S.clave}-por-ciudad/", f"Filtros para lavadora {n} por ciudad", f"Envíos de filtros para lavadora {n} a {len(S.ciudades)} ciudades de Colombia.", cuerpo, [S.breadcrumb(("Ciudades", None))], "0.7")


# ---------------------------------------------------------------- infraestructura (copia del sitio por marca)
LAV_PHP = r'''<?php
// Piezas comunes de la tienda de filtros para lavadoras (generado por lavadoras.py)
require_once __DIR__ . '/marcas.php';
$M = json_decode(file_get_contents(__DIR__ . '/marca.json'), true);
function lav_cabeza(string $titulo, string $desc, string $ruta, string $extra, string $json): void
{
    global $M;
    $ld = $json !== '' ? '<script type="application/ld+json">' . str_replace('__BASE__', sitio()['base'], $json) . '</script>' : '';
    cabeza_marca($M, $titulo, $desc, $ruta, $extra . $ld);
}
function lav_pie(): void { global $M; pie_marca($M); }
'''

CSS_EXTRA = '''
/* Tienda de lavadoras */
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
QUIENES = """<?php require __DIR__ . '/lav.php';
$n = sitio()['negocio'];
lav_cabeza('Quiénes somos | ' . $n['nombre'], 'Somos un comercio colombiano de filtros de pelusas para lavadoras, con asesoría por WhatsApp y envíos a todo el país.', '/quienes-somos.php', '', '');
?>
<div class="m-wrap"><div class="m-texto"><h1>Quiénes somos</h1>
<p><?= h($n['nombre']) ?> es un comercio colombiano de filtros de pelusas y bolsas de malla para lavadoras. Te ayudamos a encontrar el filtro que necesita tu lavadora y te lo enviamos a donde estés.</p>
<p>Antes de que compres, un asesor revisa contigo el modelo de tu lavadora por WhatsApp, para que pidas el filtro correcto.</p>
<p>Atendemos <?= h($n['horario']) ?>. Escríbenos al WhatsApp <?= h($n['telefono']) ?> o al correo <?= h($n['correo']) ?>.</p>
<p><?= h($n['nombre']) ?> · <?= h($n['titular']) ?> · <?= h($n['documento']) ?></p></div></div>
<?php lav_pie(); ?>
"""


def limpiar_textos(out):
    for f in ["404.php", "carrito.php", "opinion.php", "privacidad.php", "garantia-y-retracto.php", "admin.php", "feed.php", "partes.php", "terminos.php", "marcas.php", "api/lib.php", "api/recordatorios.php", "api/reconciliar.php", "gracias.php"]:
        p = out / f
        t = p.read_text(encoding="utf-8")
        t = t.replace(", distribuidor autorizado\"", "\"")
        for a, b in REEMPLAZOS:
            t = t.replace(a, b)
        p.write_text(t, encoding="utf-8")
    (out / "quienes-somos.php").write_text(QUIENES, encoding="utf-8")


def construir(clave, dominio):
    S = Sitio(clave, dominio)
    M = S.M
    out = S.out
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    # 1) infraestructura común
    for nombre in ["api", "data", ".htaccess", "404.php", "admin.php", "carrito.js", "carrito.php", "diagnostico.php", "estilo.css", "garantia-y-retracto.php", "gracias.php", "marcas.css", "marcas.php",
                   "opinion.php", "partes.php", "privacidad.php", "quienes-somos.php", "terminos.php", "robots.php", "feed.php"]:
        o = BASE / nombre
        if o.is_dir():
            shutil.copytree(o, out / nombre, ignore=shutil.ignore_patterns("pedidos.sqlite*", "correos.log", "config.php"))
        else:
            shutil.copy(o, out / nombre)
    # 2) marca: sin frases de "distribuidor autorizado" (no lo somos para lavadoras)
    mp = (out / "marcas.php").read_text(encoding="utf-8")
    mp = mp.replace("✔ Distribuidor autorizado ' . h($M['nombre']) . ' en Colombia", "✔ Filtros para lavadora ' . h($M['nombre']) . ' en Colombia").replace("<small>Distribuidor autorizado</small>", "<small>Filtros para lavadora</small>")
    mp = mp.replace("Distribuidor autorizado de filtros de agua ' . h($M['nombre']) . ' en Colombia, con envío gratis a todo el país y pago seguro en línea.", "Filtros de pelusas para lavadora ' . h($M['nombre']) . ', con envío a todo Colombia y pago seguro en línea.")
    mp = mp.replace("Distribuidor autorizado de filtros de agua ' . h($M['nombre']) . ' en Colombia. ' . h($M['nombre']) . ' y su logo son marcas registradas de su dueño y se usan con autorización.", "' . h($M['nombre']) . ' y su logo son marcas de su dueño y se mencionan solo para indicar el tipo de lavadora. Somos un comercio independiente.")
    mp = mp.replace("Distribuidor autorizado", "Filtros para lavadora").replace("Precios en pesos colombianos con envío incluido.", "Precios en pesos colombianos.")
    mp = mp.replace("¿Cuál filtro es el mío?", "¿Cuál filtro es el mío?").replace("Cuándo cambiarlo y cómo instalarlo", "Cómo limpiarlo y cambiarlo")
    mp = mp.replace("return '<b>' . h($M['nombre']) . '</b>';", "return '<b class=\"m-logo-txt\">' . h($M['tienda'] ?? $M['nombre']) . '</b>';").replace("<small>Filtros para lavadora</small>", "")
    (out / "marcas.php").write_text(mp, encoding="utf-8")
    (out / "marcas.css").write_text((out / "marcas.css").read_text(encoding="utf-8") + CSS_EXTRA, encoding="utf-8")
    (out / "lav.php").write_text(LAV_PHP, encoding="utf-8")
    limpiar_textos(out)
    # 3) imágenes
    shutil.copytree(BASE / "img", out / "img", ignore=lambda d, f: [x for x in f if x.startswith("sam-") or x.startswith("logo-") and x != "logo-samsung.png" and False])
    for f in list((out / "img").glob("sam-*")) + list((out / "img").glob("logo-*")) + list((out / "img").glob("icono-*")):
        f.unlink()  # sin logos de marca
    preparar_fotos(M, out)
    # 4) catálogo (solo con precio entran al carrito)
    for p in M["productos"]:
        p["nombre"] = f"{p['corto']} para lavadora {M['nombre']}"
    # 5) marca.json
    prods = [[p["nombre"], p["slug"]] for p in M["productos"]]
    marca = {"nombre": M["nombre"], "clase": M["clase"], "base": "/", "tema": M["tema"], "fuentes": "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap",
             "tienda": M["tienda"], "logo": "", "logo_w": 0, "logo_h": 0, "icono": "/img/icono.svg", "productos": prods,
             "guias": [[f"/cual-es-mi-filtro/", "¿Cuál filtro necesita mi lavadora?"], ["/cambio-e-instalacion/", "Cómo limpiar y cambiar el filtro"],
                       [f"/cada-cuanto-limpiar-filtro-lavadora-{clave}/", "Cada cuánto limpiar el filtro"], [f"/lavadora-{clave}-deja-pelusas-en-la-ropa/", "La lavadora deja pelusas"],
                       [f"/filtro-lavadora-{clave}-carga-superior/", "Filtro de carga superior"], [f"/filtro-lavadora-{clave}-carga-frontal/", "Filtro de carga frontal"]],
             "ciudades": [[c, f"/filtro-lavadora-{clave}-{slug(c)}/"] for c in ["Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena", "Bucaramanga", "Pereira", "Manizales", "Armenia", "Ibagué", "Cúcuta", "Santa Marta", "Villavicencio", "Neiva"]],
             "hub": f"/filtros-lavadora-{clave}-por-ciudad/", "externos": [list(M["oficial"]), ["Superintendencia de Industria y Comercio", "https://www.sic.gov.co/"]]}
    (out / "marca.json").write_text(json.dumps(marca, ensure_ascii=False), encoding="utf-8")
    # 6) páginas
    pagina_inicio(S)
    for p in M["productos"]:
        pagina_producto(S, p)
    guias(S)
    paginas_ciudad(S)
    # 7) catálogo PHP para el carrito/pago + sitemap
    cat_src = subprocess.run(["php", "-r", "echo json_encode(include '" + str(BASE / 'api' / 'catalogo.php') + "', JSON_UNESCAPED_UNICODE);"], capture_output=True, text=True, check=True).stdout
    cat = json.loads(cat_src)
    cat["productos"] = {p["id"]: {"nombre": p["nombre"], "ref": p["ref"] or p["id"].upper(), "marca": M["nombre"], "precio": p["precio"], "pack": p["precio"], "slug": p["slug"], "alias": [], "modelos": [], "nota": "",
                                  "link_pago": "", "ubic": "interno", "rutas_ref": {}, "rutas_modelo": {}} for p in M["productos"] if p["precio"]}
    cat["paginas"] = list(S.paginas.keys())
    cat["marcas"], cat["guias"], cat["compat"], cat["blog"], cat["rutas_ciudad"] = [], [], [], [], {}
    (out / "api" / "catalogo.php").write_text("<?php\n// Generado por lavadoras.py: no lo edites a mano.\nreturn " + php_val(cat) + ";\n", encoding="utf-8")
    (out / "sitemap.php").write_text(SITEMAP_PHP, encoding="utf-8")
    (out / "llms.php").write_text(llms_php(S), encoding="utf-8")
    (out / "config.sample.php").write_text("", encoding="utf-8")
    cfg = (BASE / "api" / "config.sample.php").read_text(encoding="utf-8")
    cfg = cfg.replace("https://filtrosaguanevecones.com", dominio).replace("Filtros Nevecones Colombia", M["tienda"]).replace("321 799 6144", M["telefono"]).replace("3217996144", M["whatsapp"])
    cfg = cfg.replace("pedidos@filtrosaguanevecones.com", "pedidos@" + dominio.split("//")[1])
    (out / "api" / "config.sample.php").write_text(cfg, encoding="utf-8")
    (out / "config.sample.php").unlink()
    # 8) zip
    z = AQUI / f"tienda-lavadoras-{clave}.zip"
    z.unlink(missing_ok=True)
    subprocess.run(["zip", "-qr", str(z), ".", "-x", "api/config.php", "-x", "data/pedidos.sqlite*", "-x", "data/correos.log"], cwd=out, check=True)
    subprocess.run(["zip", "-qj", str(z), str(AQUI / "INSTALAR-lavadoras.md")], check=True)
    print(f"Lavadoras {M['nombre']}: {out.name}/ con {len(S.paginas)} páginas → {z.name}")


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


def llms_php(S):
    M = S.M
    txt = f"# {M['tienda']}\n\n> Filtros de pelusas y bolsas de malla para lavadoras {M['nombre']} de carga superior y frontal, con envío a toda Colombia. El precio y el modelo correcto se confirman con un asesor por WhatsApp ({M['telefono']}).\n\n## Productos\n"
    for p in M["productos"]:
        txt += f"- [{p['nombre']}](__BASE__/{p['slug']}/): {p['tipo']}.\n"
    txt += f"\n## Guías\n- [Cuál filtro necesita mi lavadora](__BASE__/cual-es-mi-filtro/)\n- [Cómo limpiar y cambiar el filtro](__BASE__/cambio-e-instalacion/)\n"
    return "<?php\nrequire __DIR__ . '/api/sitio.php';\nheader('Content-Type: text/plain; charset=utf-8');\necho str_replace('__BASE__', sitio()['base'], <<<'TXT'\n" + txt + "TXT);\n"


if __name__ == "__main__":
    dominio = sys.argv[1] if len(sys.argv) > 1 else "https://filtrosparalavadoras.com"
    construir("samsung", dominio)
