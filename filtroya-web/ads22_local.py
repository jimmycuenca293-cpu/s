"""Contenido propio de cada ciudad para filtrodeaguasamsung.com: sectores y barrios (solo donde se conocen de verdad), búsquedas locales, preguntas con datos de la ciudad
(tiempo de entrega, municipios vecinos, región, área metropolitana) y un texto distinto por ciudad y por tipo de página. Todo es verificable: no se inventan barrios."""
import hashlib
import html
import json
import random

esc = lambda s: html.escape(str(s), quote=True)

# Sectores y barrios reales de las ciudades más grandes (solo los que se conocen con certeza)
BARRIOS = {
    "bogota": ["Usaquén", "Cedritos", "Chicó", "Chapinero", "Rosales", "Suba", "Niza", "Colina Campestre", "Engativá", "Normandía", "Fontibón", "Kennedy", "Castilla", "Teusaquillo", "Galerías", "Bosa", "Ciudad Bolívar", "Puente Aranda", "San Cristóbal"],
    "medellin": ["El Poblado", "Laureles", "Belén", "Robledo", "Buenos Aires", "Castilla", "Aranjuez", "Manrique", "La América", "Guayabal", "Villa Hermosa", "San Javier", "Estadio"],
    "cali": ["Granada", "San Fernando", "Ciudad Jardín", "Pance", "Versalles", "El Peñón", "Alameda", "Tequendama", "Meléndez", "Siloé", "Santa Mónica"],
    "barranquilla": ["El Prado", "Alto Prado", "Riomar", "Ciudad Jardín", "Villa Country", "Miramar", "Buenavista", "Las Delicias", "Boston", "Villa Santos", "San Francisco"],
    "cartagena": ["Bocagrande", "Manga", "Castillogrande", "El Laguito", "Centro Histórico", "Crespo", "Getsemaní", "Pie de la Popa", "Ternera", "El Bosque"],
    "bucaramanga": ["Cabecera", "Sotomayor", "Cañaveral", "García Rovira", "Mutis", "La Concordia", "San Francisco", "Provenza", "Real de Minas", "La Aurora"],
    "cucuta": ["Caobos", "Quinta Oriental", "Atalaya", "La Riviera", "Colsag", "Prados del Este", "El Rosal"],
    "pereira": ["Cerritos", "Pinares", "Circunvalar", "Álamos", "Cuba", "Centro"],
    "santa-marta": ["El Rodadero", "Bello Horizonte", "Taganga", "Mamatoco", "Gaira", "Los Almendros", "Centro Histórico"],
    "ibague": ["Cádiz", "El Salado", "Ambalá", "Picaleña", "Jordán", "La Pola", "Centro"],
    "manizales": ["Chipre", "El Cable", "Palogrande", "La Enea", "Milán", "Versalles"],
    "villavicencio": ["Barzal", "Kirpas", "La Grama", "Centro"],
    "pasto": ["Centro", "Torobajo", "Pandiaco", "Anganoy", "Los Rosales"],
    "monteria": ["La Castellana", "Mocarí", "Cantaclaro", "El Recreo", "Centro"],
    "neiva": ["Altico", "Cándido", "Las Granjas", "Los Parques", "Centro"],
    "armenia": ["Centenario", "La Castellana", "Granada", "El Bosque", "Zuldemaida"],
    "popayan": ["Centro Histórico", "Pubenza", "Campobello"],
    "soacha": ["San Mateo", "Compartir", "Ciudad Verde", "Terreros", "San Humberto"],
    "bello": ["Niquía", "Zamora", "Cabañas", "París", "Quitasol"],
    "envigado": ["Zúñiga", "El Dorado", "La Magnolia", "Alcalá"],
    "itagui": ["Ditaires", "Santa María", "San Pío X", "Calatrava", "La Finca"],
    "sabaneta": ["Aves María", "Playa Rica", "Prados de Sabaneta", "Mayorca"],
    "rionegro": ["Llanogrande", "San Antonio de Pereira", "El Porvenir", "Centro"],
    "floridablanca": ["Cañaveral", "Zapamanga"],
    "jamundi": ["Alfaguara", "Potrerito", "Ciudad Country"],
    "yumbo": ["Arroyohondo", "Centro"],
    "buenaventura": ["Bellavista", "Pueblo Nuevo", "Centro"],
    "chia": ["Fonquetá", "Fagua", "Centro"],
    "cajica": ["Calahorra", "Chuntame", "Centro"],
}

INTROS = [
    "{c} está en {d} y recibe los filtros de agua Samsung en {dias}. Si tu nevecón está en {lugar}, escoge la referencia, agrégala al carrito y paga en línea o contra entrega.",
    "Desde {d} hasta tu cocina en {c}: enviamos el filtro de tu nevecón Samsung con envío gratis y entrega estimada de {dias}. Pides, pagas como prefieras y recibes la confirmación por correo.",
    "¿Vives en {lugar}? El filtro de agua Samsung llega a {c} en {dias}. Tenemos tres referencias (HAF-CIN/EXP, HAF-QIN/EXP y externo) y un buscador para saber cuál es la tuya.",
    "Comprar el filtro de tu nevecón Samsung en {c} es simple: eliges la referencia, pagas con Wompi o contra entrega y lo recibes en {dias}. {vec} también están dentro de nuestra cobertura en {d}.",
    "Si el agua de tu nevecón en {c} ya no sabe igual, es hora de cambiar el filtro. Lo enviamos a {lugar} en {dias} y lo puedes instalar tú mismo en pocos minutos.",
    "En {c} ({d}) atendemos pedidos de filtros Samsung todos los días. El tiempo estimado de entrega es de {dias} y el envío es gratis, con pago en línea o en efectivo al recibir.",
    "Tu nevecón Samsung en {c} necesita un filtro nuevo cada 6 meses. Pídelo hoy: llega a {lugar} en {dias}, con la referencia impresa y en su empaque sellado.",
    "{c}, {d}: filtros de agua Samsung originales con envío gratis. Entrega estimada de {dias}, pago seguro con Wompi o contra entrega y 5 días de retracto.",
]
TITULOS = ["Filtro de agua Samsung en {c}: lo que debes saber", "Tu filtro Samsung en {c}, paso a paso", "Comprar el filtro de tu nevecón en {c}", "Búsquedas y respuestas para {c}"]
BUSQUEDAS = ["filtro de agua nevecón Samsung {c}", "comprar filtro HAF-CIN en {c}", "filtro nevera Samsung {c} contra entrega", "cambiar filtro refrigerador Samsung en {c}", "filtro agua Samsung {d}",
             "precio filtro Samsung en {c}", "DA29-00020B {c}", "DA97-17376B {c}", "filtro externo Samsung DA29-10105J {c}", "luz del filtro nevecón Samsung {c}", "filtro Samsung original {c} {d}",
             "dónde comprar filtro Samsung en {c}", "filtro agua nevera Samsung {reg}", "repuesto filtro nevecón Samsung {c}", "filtro Samsung French Door {c}", "filtro Samsung Side by Side {c}", "HAF-QIN {c}", "envío filtro Samsung a {c}"]
CONSEJOS = ["Anota la fecha en que cambies el filtro: en {c} y en cualquier lugar, el cambio recomendado es cada 6 meses de uso normal.",
            "Antes de pedir, mira el código impreso en tu filtro viejo (DA29-00020B, DA97-17376B o DA29-10105J): así te aseguras de que sea el de tu nevecón.",
            "Después de instalar el filtro nuevo deja correr unos 6 litros de agua por el dispensador para sacar el aire, y reinicia la luz del filtro.",
            "Si el agua sale con menos presión o el hielo se ve turbio, no esperes a los 6 meses: cambia el filtro cuando notes el cambio.",
            "Guarda el filtro nuevo en su empaque sellado hasta el momento de instalarlo.",
            "Si tienes dudas de cuál referencia es la tuya, escribe el modelo de tu nevecón (por ejemplo RF28HMEDBSR) en el buscador de arriba."]
PREGUNTAS = [
    ("¿Cuánto tarda en llegar el filtro a {c}?", "Estimamos {dias} después de confirmar el pedido, con guía de seguimiento."),
    ("¿Puedo pagar contra entrega en {c}?", "Sí. En {c} puedes pagar en efectivo a la transportadora al recibir, sin recargo, o en línea con tarjeta, PSE, Nequi o Bancolombia."),
    ("¿Qué filtro necesita mi nevecón Samsung en {c}?", "El que corresponde a tu modelo: HAF-CIN/EXP ({p1}), HAF-QIN/EXP ({p1}) o el externo DA29-10105J ({p3}). Mira el código de tu filtro viejo o busca tu modelo en la tienda."),
    ("¿También envían a otros municipios de {d}?", "Sí: {vec} y otros lugares de {d}."),
    ("¿El envío a {c} tiene costo?", "No, el envío a {c} es gratis para cualquiera de las tres referencias."),
    ("¿Puedo cambiar yo mismo el filtro en {c}?", "Sí, toma pocos minutos y no necesita herramientas. Tenemos la guía paso a paso para cada referencia."),
    ("¿Cada cuánto debo cambiar el filtro en {c}?", "Cada 6 meses de uso normal, o antes si el agua cambia de sabor o el dispensador entrega menos agua."),
    ("¿Qué pasa si pedí el filtro equivocado en {c}?", "Tienes 5 días hábiles de retracto desde la entrega, con el filtro sin usar."),
    ("¿Recibo comprobante de mi pedido en {c}?", "Sí, te llega la confirmación del pedido a tu correo."),
    ("¿Los filtros que envían a {c} son nuevos?", "Sí, nuevos y en su empaque sellado, con la referencia impresa."),
]


def corto(c):
    return c.split(" (")[0]


def bloque(slug, ciudad, dept, dias, vecinos, region, area, fam, productos, cerca=False):
    """Devuelve (html, json-ld) con el contenido propio de esa ciudad y esa página."""
    c = corto(ciudad)
    rng = random.Random(int(hashlib.md5(f"{slug}|{fam}".encode()).hexdigest()[:12], 16))
    barrios = BARRIOS.get(slug, [])
    vec = [corto(n) for n, _ in vecinos]
    rng.shuffle(vec)
    vec_txt = ", ".join(vec[:3]) if vec else f"otros municipios de {dept}"
    vec_corto = (", ".join(vec[:2]) + (" y " + vec[2] if len(vec) > 2 else "")) if len(vec) > 1 else (vec[0] if vec else f"otros municipios de {dept}")
    lugar = f"{rng.choice(barrios)}" if barrios else f"el casco urbano de {c}"
    reg = region or dept
    p1 = f"${productos['cin']['precio']:,}".replace(",", ".")
    p3 = f"${productos['ext']['precio']:,}".replace(",", ".")
    datos = dict(c=c, d=dept, dias=dias.split(" (")[0], reg=reg, lugar=lugar, vec=vec_corto, p1=p1, p3=p3)
    f = lambda s: s.format(**datos)
    prod = {"cin": ("HAF-CIN/EXP", "DA29-00020B"), "qin": ("HAF-QIN/EXP", "DA97-17376B"), "ext": ("filtro externo", "DA29-10105J")}
    clave = {"filtro-haf-cin": "cin", "filtro-haf-qin": "qin", "filtro-externo": "ext"}.get(fam)
    intro = f(rng.choice(INTROS))
    titulo = f(rng.choice(TITULOS))
    if clave:
        n, r = prod[clave]
        intro += f" Esta página es para el {n} (código {r}) en {c}."
    busq = [f(x) for x in rng.sample(BUSQUEDAS, 7)]
    if clave:
        busq[0] = f"{prod[clave][0].lower()} {prod[clave][1]} {c}"
    preg = rng.sample(PREGUNTAS, 4)
    if barrios:
        a, b = rng.sample(barrios, min(2, len(barrios))) if len(barrios) > 1 else (barrios[0], barrios[0])
        preg[-1] = (f"¿Entregan en {a} y {b}?", f"Sí, entregamos en {a}, {b} y en toda {c}. Escríbenos tu dirección al hacer el pedido.")
    preg = [(f(q).replace(f"otros municipios de {dept}?", f"municipios cercanos a {c}?") if cerca else f(q), f(a)) for q, a in preg]
    if clave:
        n, r = prod[clave]
        preg[0] = (f"¿Dónde comprar el {n} ({r}) en {c}?", f"Aquí mismo: agrégalo al carrito y paga en línea o contra entrega. Llega a {c} en {datos['dias']} con envío gratis.")
    consejo = f(rng.choice(CONSEJOS))
    zona = ""
    if barrios:
        zona = f'<p style="margin:12px 0 6px"><b>Sectores de {esc(c)} donde entregamos:</b></p><div class="aq-depts">' + "".join(f"<span style=\"background:#fff;border:1px solid var(--line);border-radius:99px;padding:7px 14px;font-size:13.5px;font-weight:600\">{esc(b)}</span>" for b in barrios) + "</div>"
    if area:
        zona += f'<p style="margin:10px 0;color:var(--ink2)">{esc(c)} hace parte de <a href="{esc(area[0])}">{esc(area[1])}</a>.</p>'
    chips = "".join(f'<span style="background:#eaefff;border-radius:99px;padding:6px 13px;font-size:13px;font-weight:600;color:var(--navy)">{esc(b)}</span>' for b in busq)
    faqh = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in preg)
    orden = rng.random() < 0.5
    cuerpo_a = f'<p style="max-width:780px">{esc(intro)}</p>{zona}<h3 style="font-size:1.05rem;margin:18px 0 8px">Lo que más buscan en {esc(c)}</h3><div class="aq-depts">{chips}</div>'
    cuerpo_b = f'<h3 style="font-size:1.05rem;margin:22px 0 10px">Preguntas de {esc(c)}</h3><div class="faq-num">{faqh}</div><p style="margin-top:14px;color:var(--ink2)"><b>Consejo:</b> {esc(consejo)}</p>'
    h = (f'<section class="aq-sec"><div class="wrap"><h2 style="font-size:1.55rem">{esc(titulo)}</h2>' + (cuerpo_a + cuerpo_b if orden else cuerpo_b + cuerpo_a) + "</div></section>")
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in preg]}
    return h, json.dumps(ld, ensure_ascii=False)
