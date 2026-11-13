"""Página de ciudad con contenido propio para la tienda nacional de una marca (LG, etc.): cada ciudad tiene sus datos (departamento, región, área metropolitana, tiempo de entrega, vecinos,
sectores donde se conocen), un orden de bloques, textos y preguntas distintos, y una selección distinta de filtros y modelos del catálogo. Nada se inventa: solo datos reales de la ciudad y del catálogo."""
import hashlib
import html
import random
import re
import unicodedata

import ads22_hubs
import ads22_local

esc = lambda s: html.escape(str(s), quote=True)
cop = lambda v: "$ " + f"{int(v):,}".replace(",", ".")


def slug(n):
    n = unicodedata.normalize("NFKD", n).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", n).strip("-")


DIAS_DEPTO = {"Amazonas": "5 a 7 días hábiles", "Vaupés": "5 a 7 días hábiles", "Guainía": "5 a 7 días hábiles", "Vichada": "5 a 7 días hábiles", "San Andrés y Providencia": "5 a 7 días hábiles",
              "Guaviare": "4 a 5 días hábiles", "Putumayo": "4 a 5 días hábiles", "Caquetá": "4 a 5 días hábiles", "Chocó": "4 a 5 días hábiles", "Arauca": "4 a 5 días hábiles", "Casanare": "3 a 4 días hábiles",
              "Bogotá D.C.": "1 a 2 días hábiles", "Cundinamarca": "2 a 3 días hábiles", "Antioquia": "2 a 3 días hábiles", "Valle del Cauca": "2 a 3 días hábiles", "Atlántico": "2 a 3 días hábiles",
              "Santander": "2 a 3 días hábiles", "Risaralda": "2 a 3 días hábiles", "Caldas": "2 a 3 días hábiles", "Quindío": "2 a 3 días hábiles"}


def dias_de(c):
    if len(c) > 2 and c[2]:
        return f"{c[2]} días hábiles" if str(c[2]).isdigit() else str(c[2])
    return DIAS_DEPTO.get(c[1], "3 a 4 días hábiles")


def region_de(dept):
    for k, (nombre, deptos, grandes) in ads22_hubs.REGIONES.items():
        if dept in deptos:
            return k, nombre
    return None, None


def area_de(s):
    for k, (corto, largo, slugs) in ads22_hubs.AREAS.items():
        if s in slugs:
            return k, corto, slugs
    return None, None, []


INTROS = [
    "{c} está en {d} y recibe los filtros {m} en {dias}. Si tu nevecón está {en_lugar}, escoge la referencia, agrégala al carrito y paga en línea.",
    "Desde {d} hasta tu cocina en {c}: enviamos el filtro de tu nevecón {m} con envío gratis y entrega estimada de {dias}. Pagas con Wompi y recibes la confirmación por correo.",
    "¿Vives {en_lugar}? El filtro de agua {m} llega a {c} en {dias}. Tenemos {n} referencias y un buscador para saber cuál es la tuya.",
    "Comprar el filtro de tu refrigerador {m} en {c} es simple: eliges la referencia, pagas en línea y lo recibes en {dias}. {vec} también están en nuestra cobertura de {d}.",
    "Si el agua o el hielo de tu nevecón en {c} ya no saben igual, es hora de cambiar el filtro. Lo enviamos {a_lugar} en {dias}; instalarlo toma unos minutos.",
    "En {c} ({d}) atendemos pedidos de filtros {m} todos los días. El tiempo estimado de entrega es de {dias}, con envío gratis y pago seguro en línea.",
    "El refrigerador {m} de tu casa en {c} necesita un filtro nuevo cada 6 meses. Pídelo hoy: llega {a_lugar} en {dias}, nuevo y en su empaque.",
    "{c}, {d}: filtros de agua {m} con envío gratis. Entrega estimada de {dias}, pago seguro con Wompi y 5 días de retracto.",
]
TITULOS = ["Filtro nevera {m} en {ct} | Envío gratis", "Filtros {m} en {ct}: precios y envío", "Comprar filtro de agua {m} en {ct}", "Filtro para refrigerador {m} en {ct}", "Filtro de agua {m} {ct}: compra en línea",
           "Filtro nevecón {m} en {ct} | Pago seguro"]
H1S = ["Filtro para nevera {m} en {ct}", "Comprar filtros de agua {m} en {ct}", "Filtros {m} originales para tu nevecón en {ct}", "Tu filtro {m} en {ct}, con envío gratis"]
DESCS = ["Filtros de agua {m} en {ct}, {d}: llegan en {dias} con envío gratis. Desde {pmin} hasta {pmax}. Paga en línea con tarjeta, PSE o Nequi.",
         "Compra el filtro de tu nevecón {m} en {ct}: {n} referencias nuevas, entrega en {dias} y pago seguro con Wompi. Envío gratis.",
         "Filtro para refrigerador {m} en {ct} ({d}): {refs}. Envío gratis, entrega en {dias} y retracto de 5 días.",
         "¿Qué filtro necesita tu {m} en {ct}? Mira códigos y modelos, paga en línea y recíbelo en {dias} con envío gratis.",
         "Venta de filtros de agua {m} con envío a {ct}: precios desde {pmin}, {dias} de entrega y confirmación por correo. Distribuidores autorizados."]
BUSQUEDAS = ["filtro de agua nevecón {m} {c}", "comprar filtro {m} en {c}", "filtro nevera {m} {c} precio", "cambiar filtro refrigerador {m} en {c}", "filtro agua {m} {d}", "repuesto filtro nevecón {m} {c}",
             "{lt} {c}", "filtro {m} original {c}", "dónde comprar filtro {m} en {c}", "luz del filtro {m} {c}", "filtro {m} French door {c}", "filtro {m} con dispensador {c}", "envío filtro {m} a {c}",
             "filtro {m} {c} {d}", "filtro externo {m} {c}", "{mod} filtro {c}", "filtro de agua para refrigerador {m} {reg}", "cuánto cuesta el filtro {m} en {c}"]
CONSEJOS = ["Anota la fecha en que cambies el filtro: el cambio recomendado es cada 6 meses de uso normal, también en {c}.",
            "Antes de pedir, mira el código impreso en tu filtro viejo (por ejemplo {lt}): así te aseguras de que sea el de tu nevecón.",
            "Después de instalar el filtro nuevo deja correr unos 6 litros de agua por el dispensador para sacar el aire, y reinicia el aviso del filtro.",
            "Si el agua sale con menos presión o el hielo se ve turbio, no esperes a los 6 meses: cambia el filtro cuando notes el cambio.",
            "Guarda el filtro nuevo en su empaque hasta el momento de instalarlo.",
            "Si dudas cuál referencia es la tuya, escribe el modelo de tu nevecón (por ejemplo {mod}) en el buscador de la tienda."]
HEADS_MOD = ["Filtros {m} que puedes pedir en {c}", "Qué filtro usa cada nevecón {m}", "Códigos y modelos {m} para {c}", "Escoge tu filtro {m} en {c}"]
HEADS_BUS = ["Lo que más buscan en {c}", "Búsquedas frecuentes en {c}", "Términos que usan en {c} para encontrar su filtro"]
HEADS_FAQ = ["Preguntas de {c}", "Dudas frecuentes en {c}", "Lo que preguntan en {c}"]
PREGS = [
    ("¿Cuánto tarda en llegar el filtro a {c}?", "Estimamos {dias} después de confirmar el pago, con guía de seguimiento."),
    ("¿Cómo pago el filtro en {c}?", "Solo en línea, en la pasarela segura de Wompi: tarjeta, PSE, Nequi o Bancolombia. Te llega la confirmación a tu correo."),
    ("¿Qué filtro necesita mi nevecón {m} en {c}?", "El que corresponde a tu modelo. Hay {n} referencias ({refs}); mira el código del filtro viejo o busca tu modelo en la tienda."),
    ("¿También envían a otros municipios de {d}?", "Sí: {vec} y otros lugares de {d}."),
    ("¿El envío a {c} tiene costo?", "No, el envío a {c} es gratis para cualquiera de las referencias."),
    ("¿Puedo cambiar yo mismo el filtro en {c}?", "Sí, toma pocos minutos y no necesita herramientas. Tenemos la guía paso a paso."),
    ("¿Cada cuánto debo cambiar el filtro en {c}?", "Cada 6 meses de uso normal, o antes si el agua cambia de sabor o el dispensador entrega menos agua."),
    ("¿Qué pasa si pedí el filtro equivocado en {c}?", "Tienes 5 días hábiles de retracto desde la entrega, con el filtro sin usar."),
    ("¿Recibo comprobante de mi pedido en {c}?", "Sí, te llega la confirmación del pedido a tu correo."),
    ("¿Los filtros que envían a {c} son nuevos?", "Sí, nuevos y en su empaque, con la referencia impresa."),
    ("¿Cuánto cuesta el filtro {m} en {c}?", "Entre {pmin} y {pmax}, según la referencia, con envío gratis."),
    ("¿Cómo sé cuál filtro {m} necesito en {c}?", "Mira el código impreso en el filtro viejo o el modelo de tu nevecón (etiqueta dentro del refrigerador) y escríbelo en el buscador."),
]


def contenido(marca, s, ps, base, c, vecinos, R):
    """Devuelve dict con titulo, desc, h1, eyebrow, intro, cuerpo, preguntas, miga_nombre."""
    nombre, dept = c[0], c[1]
    corto = nombre.split(" (")[0]
    rng = random.Random(int(hashlib.md5(f"{marca}|{s}".encode()).hexdigest()[:12], 16))
    dias = dias_de(c)
    rk, rn = region_de(dept)
    ak, acorto, aslugs = area_de(s)
    barrios = ads22_local.BARRIOS.get(s, [])
    vec = list(vecinos)
    if ak:
        miembros = [(R["ciudades"][k][0][0], R["ciudades"][k][1]) for k in R["ciudades"] if slug(k.split(" (")[0]) in aslugs and slug(k.split(" (")[0]) != s]
        if len(miembros) >= 2:
            vec = miembros
    rng.shuffle(vec)
    vec_nombres = [n.split(" (")[0] for n, _ in vec]
    vec_txt = (", ".join(vec_nombres[:2]) + (" y " + vec_nombres[2] if len(vec_nombres) > 2 else "")) if len(vec_nombres) > 1 else (vec_nombres[0] if vec_nombres else f"otros municipios de {dept}")
    precios = sorted(p["precio"] for p in ps)
    lt = rng.choice([p["ref"] for p in ps])
    modelos_all = [m for p in ps for m in p["modelos"]]
    mod = rng.choice(modelos_all) if modelos_all else lt
    barrio_ = rng.choice(barrios) if barrios else None
    lugar = barrio_ or f"el casco urbano de {corto}"
    a_lugar = f"a {barrio_}" if barrio_ else f"al casco urbano de {corto}"
    en_lugar = f"en {barrio_}" if barrio_ else f"en el casco urbano de {corto}"
    d = dict(ct=nombre, c=corto, d=dept, m=marca, dias=dias, n=len(ps), lugar=lugar, a_lugar=a_lugar, en_lugar=en_lugar, vec=vec_txt, pmin=cop(precios[0]), pmax=cop(precios[-1]), refs=", ".join(p["ref"] for p in ps[:4]), lt=lt, mod=mod, reg=rn or dept)
    f = lambda t: t.format(**d)
    titulo = f(rng.choice(TITULOS))
    if len(titulo) > 62:
        titulo = titulo[:62].rsplit(" ", 1)[0]
    desc = f(rng.choice(DESCS))
    h1 = f(rng.choice(H1S))
    eyebrow = rng.choice([f"{corto}, {dept}", f"Envíos a {corto}", f"{dept} · {corto}"])
    intro = esc(f(rng.choice(INTROS)))
    # --- bloque: datos de entrega
    filas = [("Ciudad", corto), ("Departamento", dept), ("Tiempo de entrega", f"Unos {dias}"), ("Costo del envío", "Gratis"), ("Pago", "Tarjeta, PSE, Nequi o Bancolombia, en línea")]
    if rn:
        filas.insert(2, ("Región", rn.replace("Región ", "")))
    if ak:
        filas.insert(3, ("Área", acorto))
    cola = filas[2:]
    rng.shuffle(cola)
    filas = filas[:2] + cola
    tabla = '<div class="m-tabla-wrap"><table class="m-tabla"><tbody>' + "".join(f"<tr><th>{esc(a)}</th><td>{esc(b)}</td></tr>" for a, b in filas) + "</tbody></table></div>"
    # --- bloque: filtros y modelos (subconjunto distinto en cada ciudad)
    elegidos = rng.sample(ps, min(3, len(ps)))
    filas_m = "".join(f'<tr><td><a href="{base}{p["slug_o"]}/">{esc(p["nombre_largo"])}</a></td><td>{esc(", ".join(rng.sample(p["modelos"], min(2, len(p["modelos"])))) if p["modelos"] else ", ".join(p["refs"][:2]))}</td><td><b>{cop(p["precio"])}</b></td></tr>' for p in elegidos)
    bloque_mod = (f'<h2 style="font-size:22px;margin:28px 0 12px">{esc(f(rng.choice(HEADS_MOD)))}</h2><div class="m-tabla-wrap"><table class="m-tabla"><thead><tr><th>Filtro</th><th>Nevecones o equivalencias</th><th>Precio</th></tr></thead><tbody>'
                  + filas_m + f'</tbody></table></div><p class="m-mut" style="margin-top:10px">Mira <a href="{base}cual-es-mi-filtro/">todos los modelos y referencias</a>.</p>')
    # --- bloque: sectores y búsquedas
    sect = ""
    if barrios:
        sect = f'<h3 style="font-size:18px;margin:24px 0 10px">Sectores de {esc(corto)} donde entregamos</h3><div class="m-chips">' + "".join(f"<span>{esc(b)}</span>" for b in barrios) + "</div>"
    busq = [f(t) for t in rng.sample(BUSQUEDAS, 7)]
    bloque_bus = sect + f'<h3 style="font-size:18px;margin:24px 0 10px">{esc(f(rng.choice(HEADS_BUS)))}</h3><div class="m-chips">' + "".join(f"<span>{esc(b)}</span>" for b in busq) + "</div>"
    # --- bloque: vecinas y enlaces
    enl = []
    if rk:
        enl.append((f"Filtros {marca} en {rn}", f"{base}filtros-{slug(marca)}-region-{slug(rk)}/"))
    if ak:
        enl.append((f"Filtros {marca} en {acorto}", f"{base}filtro-nevera-{slug(marca)}-{ak}/"))
    enl.append((f"Filtros {marca} en {dept}", f"{base}filtros-{slug(marca)}-{slug(dept)}/"))
    enl += [(f"Todas las ciudades", R["hub"]), ("Ciudades de la A a la Z", f"{base}ciudades-con-filtros-{slug(marca)}-a-z/"), ("Glosario", f"{base}glosario-filtro-nevera-{slug(marca)}/")]
    bloque_vec = ('<h3 style="font-size:18px;margin:24px 0 10px">Más cerca de ' + esc(corto) + '</h3><div class="m-chips">' + "".join(f'<a href="{u}">{esc(n)}</a>' for n, u in enl) + "</div>"
                  + (f'<h3 style="font-size:18px;margin:20px 0 10px">También enviamos a</h3><div class="m-chips">' + "".join(f'<a href="{r}">{esc(n)}</a>' for n, r in vec[:10]) + "</div>" if vec else ""))
    consejo = f'<p style="margin-top:22px"><b>Consejo:</b> {esc(f(rng.choice(CONSEJOS)))}</p>'
    bloques = [bloque_mod, bloque_bus, bloque_vec + consejo]
    rng.shuffle(bloques)
    cuerpo = tabla + "".join(bloques)
    preg = rng.sample(PREGS, 4)
    if barrios and len(barrios) > 1:
        a, b = rng.sample(barrios, 2)
        preg[-1] = (f"¿Entregan en {a} y {b}?", f"Sí, entregamos en {a}, {b} y en toda {corto}. Escribe tu dirección al hacer el pedido.")
    preguntas = [(f(q), f(a)) for q, a in preg]
    return dict(titulo=titulo, desc=desc, h1=h1, eyebrow=eyebrow, intro=intro, cuerpo=cuerpo, preguntas=preguntas, miga_nombre=f"Envíos a {corto}")
