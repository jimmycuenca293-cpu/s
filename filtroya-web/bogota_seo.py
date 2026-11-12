"""SEO local de Bogotá: una página por localidad, por barrio, por zona, por municipio cercano y artículos del blog.
Se usa solo en la tienda propia «Filtros Samsung Bogotá» (filtroneverasamsungenbogota.click)."""
import html
import re
import unicodedata

ENTREGA = "1 a 2 días hábiles"


def slug(n):
    n = unicodedata.normalize("NFKD", n).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", n).strip("-")


def esc(s):
    return html.escape(str(s), quote=True)


# nombre: (zona, localidades vecinas, perfil, barrios)
LOCALIDADES = {
    "Usaquén": ("Norte", ["Chapinero", "Suba"], "Localidad del norte de Bogotá, con barrios residenciales, comercio y el casco antiguo de Usaquén. Muchas casas y apartamentos de varios pisos.",
                ["Usaquén", "Santa Bárbara", "Santa Ana", "Cedritos", "Toberín", "Verbenal", "San Cristóbal Norte", "Britalia", "Servitá", "Babilonia", "La Uribe", "Los Cedros", "Mirandela", "Pontevedra", "El Codito", "Buenavista", "Country Club"]),
    "Chapinero": ("Norte", ["Usaquén", "Barrios Unidos", "Teusaquillo", "Santa Fe"], "Zona de oficinas, comercio y vivienda en edificios, de la calle 39 a la 100 entre la carrera séptima y la Caracas.",
                  ["Chapinero Central", "Chapinero Alto", "El Chicó", "Chicó Norte", "El Retiro", "Rosales", "El Nogal", "Quinta Camacho", "Bellavista", "Pardo Rubio", "Antiguo Country", "Lago Gaitán"]),
    "Suba": ("Norte", ["Usaquén", "Engativá", "Barrios Unidos"], "La localidad más poblada del noroccidente de Bogotá, con barrios consolidados, conjuntos residenciales y mucho comercio de barrio.",
             ["Suba Centro", "Niza", "Colina Campestre", "Prado Veraniego", "La Gaitana", "Tibabuyes", "El Rincón", "Casablanca Suba", "Bilbao", "Lisboa", "Compartir", "Aures", "Villa del Prado", "San José de Bavaria", "Mazurén"]),
    "Barrios Unidos": ("Norte", ["Chapinero", "Teusaquillo", "Engativá", "Suba"], "Localidad central-norte de comercio, talleres y vivienda, con barrios tradicionales de casas y apartamentos.",
                       ["7 de Agosto", "Alcázares", "Polo Club", "La Castellana", "Los Andes", "Doce de Octubre", "Rionegro", "Entre Ríos", "San Fernando", "Colombia", "Concepción Norte"]),
    "Teusaquillo": ("Centro", ["Chapinero", "Barrios Unidos", "Los Mártires", "Puente Aranda", "Engativá"], "Localidad céntrica y residencial, de casas antiguas, edificios y universidades.",
                    ["Teusaquillo", "La Soledad", "Palermo", "Park Way", "Galerías", "La Magdalena", "Quinta Paredes", "Ciudad Universitaria", "Armenia", "Santa Teresita"]),
    "Santa Fe": ("Centro", ["Chapinero", "La Candelaria", "Los Mártires", "San Cristóbal"], "Localidad del centro-oriente de Bogotá, de barrios tradicionales cerca de los cerros.",
                 ["La Macarena", "Las Nieves", "La Perseverancia", "Sagrado Corazón", "Bosque Izquierdo", "Las Aguas", "Germania", "Lourdes", "Egipto", "San Martín"]),
    "La Candelaria": ("Centro", ["Santa Fe", "Los Mártires"], "El centro histórico de Bogotá: casas coloniales, universidades, oficinas y vivienda.",
                      ["La Candelaria", "Belén", "Las Aguas Candelaria", "Santa Bárbara Centro"]),
    "Los Mártires": ("Centro", ["Teusaquillo", "Santa Fe", "Antonio Nariño", "Puente Aranda", "La Candelaria"], "Localidad céntrica de comercio, bodegas y vivienda.",
                     ["Paloquemao", "La Favorita", "Ricaurte", "Samper Mendoza", "Eduardo Santos", "La Sabana", "Santa Fe Mártires"]),
    "Antonio Nariño": ("Centro", ["Los Mártires", "Puente Aranda", "San Cristóbal", "Rafael Uribe Uribe"], "Localidad pequeña del centro-sur, de comercio y barrios residenciales tradicionales.",
                       ["Restrepo", "Ciudad Jardín", "San Antonio", "La Fraguita", "Santander", "Policarpa", "Ciudad Berna"]),
    "Puente Aranda": ("Centro", ["Teusaquillo", "Los Mártires", "Antonio Nariño", "Kennedy", "Fontibón"], "Zona industrial y comercial del centro-occidente, con barrios residenciales alrededor.",
                      ["Puente Aranda", "Zona Industrial", "Ciudad Montes", "Muzú", "San Rafael", "Galán", "Batallón Caldas", "Salazar Gómez", "Pensilvania", "Veraguas"]),
    "Engativá": ("Occidente", ["Suba", "Barrios Unidos", "Teusaquillo", "Fontibón"], "Gran localidad del occidente, de barrios residenciales y comercio, cerca del aeropuerto.",
                 ["Engativá", "Minuto de Dios", "Boyacá Real", "Garcés Navas", "Álamos Norte", "Bolivia", "Las Ferias", "La Granja", "Normandía", "Quirigua", "Santa Helenita", "Ciudadela Colsubsidio", "Villas de Granada", "Bosque Popular", "Gran Granada"]),
    "Fontibón": ("Occidente", ["Engativá", "Kennedy", "Puente Aranda"], "Localidad del occidente junto al aeropuerto El Dorado, con barrios residenciales y zona empresarial.",
                 ["Fontibón", "Modelia", "Hayuelos", "Capellanía", "Puente Grande", "Villemar", "Ferrocarril", "Zona Franca"]),
    "Kennedy": ("Occidente", ["Bosa", "Fontibón", "Puente Aranda", "Tunjuelito"], "Una de las localidades más grandes y pobladas, de barrios consolidados y comercio.",
                ["Kennedy Central", "Castilla", "Patio Bonito", "Américas", "Timiza", "Techo", "Bavaria", "Carvajal", "Corabastos", "Roma", "Mandalay", "Tintal", "Bellavista Occidental", "Villa Alsacia"]),
    "Bosa": ("Occidente", ["Kennedy", "Ciudad Bolívar"], "Localidad del suroccidente en crecimiento, de barrios y conjuntos nuevos junto a Soacha.",
             ["Bosa Centro", "Bosa Nova", "Antonia Santos", "El Recreo", "Porvenir", "Argelia", "San Bernardino", "Holanda", "Bosa Piamonte", "Apogeo"]),
    "Tunjuelito": ("Sur", ["Kennedy", "Ciudad Bolívar", "Rafael Uribe Uribe", "Usme"], "Localidad del sur de Bogotá de barrios tradicionales, comercio y pequeña industria.",
                   ["Venecia", "Tunjuelito", "San Benito", "Isla del Sol", "El Carmen", "Fátima"]),
    "San Cristóbal": ("Sur", ["Santa Fe", "Antonio Nariño", "Rafael Uribe Uribe", "Usme"], "Localidad del suroriente, de barrios populares en las laderas de los cerros.",
                      ["20 de Julio", "San Blas", "La Gloria", "Los Libertadores", "Villa Javier", "Altamira", "Moralba", "Montebello", "Sosiego"]),
    "Rafael Uribe Uribe": ("Sur", ["San Cristóbal", "Antonio Nariño", "Tunjuelito", "Usme"], "Localidad del sur de Bogotá, de barrios residenciales y mucho comercio de barrio.",
                           ["Quiroga", "Marruecos", "San José", "Diana Turbay", "Olaya", "Molinos", "Santa Lucía", "Bochica", "Quiroga Central", "Granjas de San Pablo"]),
    "Ciudad Bolívar": ("Sur", ["Bosa", "Tunjuelito", "Usme", "Kennedy"], "La localidad más extensa del sur, de barrios de ladera y conjuntos nuevos.",
                       ["Lucero", "Perdomo", "Candelaria La Nueva", "Arborizadora Alta", "Arborizadora Baja", "El Tesoro", "Sierra Morena", "San Francisco", "Jerusalén", "Paraíso", "Meissen", "Potosí", "Quiba"]),
    "Usme": ("Sur", ["San Cristóbal", "Rafael Uribe Uribe", "Tunjuelito", "Ciudad Bolívar"], "Localidad del extremo sur, con barrios urbanos y zonas que crecen rápido.",
             ["Usme Centro", "Ciudad Usme", "Santa Librada", "Danubio Azul", "Comuneros", "Alfonso López", "La Fiscala", "Yomasa", "Gran Yomasa", "Marichuela"]),
}
MUNICIPIOS = []  # la tienda es solo de Bogotá
CATS_OVERRIDE = None  # otra ciudad puede traer sus propias listas de barrios por tipo
ZONAS = {"Norte": "norte", "Centro": "centro", "Occidente": "occidente", "Sur": "sur"}


def datos():
    """Barrios con rutas únicas (si un nombre se repite en dos localidades, se agrega la localidad)."""
    vistos, barrios = {}, []
    for loc, (zona, vec, perfil, bs) in LOCALIDADES.items():
        for b in bs:
            if slug(b) == slug(loc):  # el barrio que se llama igual que su localidad: se distingue como «Centro»
                b = f"{b} Centro"
            s = slug(b)
            if s in vistos:
                s = slug(f"{b} {loc}")
            vistos[s] = 1
            barrios.append(dict(nombre=b, slug=s, loc=loc, zona=zona))
    return barrios


def generar(pagina, ctx, h, R, hechas):
    ps, base, M, marca = ctx["ps"], ctx["base"], ctx["M"], ctx["marca"]
    cop = lambda v: "$ " + f"{int(v):,}".replace(",", ".")
    refs = ", ".join(p["ref"] for p in ps)
    precios = sorted({p["precio"] for p in ps})
    rango = f"{cop(precios[0])} a {cop(precios[-1])}"
    barrios = datos()
    por_loc = {}
    for b in barrios:
        por_loc.setdefault(b["loc"], []).append(b)
    ruta_loc = {l: f"{base}filtro-nevera-samsung-{slug(l)}-bogota/" for l in LOCALIDADES}
    ruta_bar = {(b["loc"], b["nombre"]): f"{base}filtro-nevera-samsung-{b['slug']}-bogota/" for b in barrios}
    ruta_mun = {m: f"{base}filtro-nevera-samsung-{slug(m)}/" for m in MUNICIPIOS}
    ruta_zona = {z: f"{base}filtros-samsung-{s}-de-bogota/" for z, s in ZONAS.items()}
    hub = f"{base}filtros-samsung-bogota-por-localidad/"
    tabla = lambda filas: '<div class="m-tabla-wrap"><table class="m-tabla"><tbody>' + "".join(f"<tr><th>{esc(a)}</th><td>{b}</td></tr>" for a, b in filas) + "</tbody></table></div>"
    pasos = lambda lugar: ('<div class="m-cols m-num" style="margin-top:20px">' + "".join(f'<div class="m-bloque"><h3>{esc(t)}</h3><p>{d}</p></div>' for t, d in [
        ("Escoge tu filtro", f"Por la referencia del filtro viejo o el modelo de tu nevecón: usa el <a href=\"{base}cual-es-mi-filtro/\">buscador</a>."),
        ("Paga en línea", "Con tarjeta, PSE, Nequi o Bancolombia en la pasarela segura de Wompi; te llega la confirmación por correo."),
        (f"Recíbelo en {esc(lugar)}", f"Entrega en {ENTREGA}. Luego cámbialo con la guía de <a href=\"{base}cambio-e-instalacion/\">instalación</a>.")]) + "</div>")
    chips = lambda items: '<div class="m-chips">' + "".join(f'<a href="{r}">{esc(n)}</a>' for n, r in items) + "</div>"

    # ---------- localidades ----------
    for loc, (zona, vec, perfil, bs) in LOCALIDADES.items():
        ruta = ruta_loc[loc]
        servicio = {"@type": "Service", "name": f"Filtros de agua Samsung con envío a {loc}, Bogotá", "serviceType": "Venta de filtros de agua para nevera", "provider": {"@id": f"__BASE__{base}#tienda"},
                    "areaServed": {"@type": "AdministrativeArea", "name": f"{loc}, Bogotá D.C.", "containedInPlace": {"@type": "City", "name": "Bogotá"}}}
        pagina(ruta, f"Filtro nevera Samsung en {loc}, Bogotá | Compra segura",
               f"Filtros de agua Samsung HAF-CIN, HAF-QIN y externo en {loc}, Bogotá: entrega en {ENTREGA}. Compra en línea con tarjeta, PSE, Nequi o Bancolombia.",
               f"Filtro para nevera Samsung en {loc}, Bogotá", f"{loc} · zona {zona.lower()} de Bogotá",
               f"{esc(perfil)} Entregamos el filtro de agua de tu nevecón Samsung en tu casa, apartamento u oficina en <b>{esc(loc)}</b> en <b>{ENTREGA}</b>.",
               ('<div class="m-aviso"><span style="font-size:22px">📍</span><span><b>Nuestra bodega está en Cedritos, Usaquén</b>Tenemos nuestra bodega en el barrio Cedritos, en esta localidad.</span></div>' if loc == "Usaquén" else "")
               + tabla([("Localidad", esc(loc)), ("Ciudad", "Bogotá D.C."), ("Zona", esc(zona)), ("Entrega", f"{ENTREGA}"), ("Filtros disponibles", esc(refs)), ("Pago", "Tarjeta, PSE, Nequi o Bancolombia, en línea")])
               + f'<h2 style="font-size:22px;margin:26px 0 12px">Barrios de {esc(loc)} donde entregamos</h2>' + chips([(b["nombre"], ruta_bar[(loc, b["nombre"])]) for b in por_loc[loc]])
               + pasos(loc)
               + f'<h2 style="font-size:22px;margin:26px 0 12px">Localidades cercanas a {esc(loc)}</h2>' + chips([(v, ruta_loc[v]) for v in vec])
               + f'<p class="m-mut" style="margin-top:14px">Mira también <a href="{ruta_zona[zona]}">todas las localidades de la zona {esc(zona.lower())}</a> y el <a href="{hub}">listado de todas las localidades de Bogotá</a>.</p>',
               [(f"¿Hacen entregas en {loc}, Bogotá?", f"Sí, entregamos filtros de agua Samsung en {loc} y en todos sus barrios, en {ENTREGA}."),
                (f"¿Cuánto cuesta el filtro de nevera Samsung en {loc}?", f"Entre {rango}, según la referencia."),
                (f"¿Cómo pago el filtro en {loc}?", "En línea, en la pasarela segura de Wompi, con tarjeta, PSE, Nequi o Bancolombia. Recibes la confirmación de tu pedido por correo."),
                (f"¿Qué filtro necesita mi nevecón Samsung en {loc}?", f"Depende del modelo: las referencias son {refs}. Escribe el modelo en el buscador y te decimos cuál es.")],
               miga_nombre=f"{loc}, Bogotá", ld_extra=servicio)

    # ---------- barrios ----------
    for b in barrios:
        loc, nom = b["loc"], b["nombre"]
        zona, vec, perfil, _ = LOCALIDADES[loc]
        ruta = ruta_bar[(loc, nom)]
        cerca = [x for x in por_loc[loc] if x["nombre"] != nom]
        ini = (barrios.index(b) % max(1, len(cerca))) if cerca else 0
        cerca = (cerca[ini:] + cerca[:ini])[:7]
        servicio = {"@type": "Service", "name": f"Filtros de agua Samsung con envío a {nom}, {loc}, Bogotá", "serviceType": "Venta de filtros de agua para nevera", "provider": {"@id": f"__BASE__{base}#tienda"},
                    "areaServed": {"@type": "Place", "name": f"Barrio {nom}, {loc}, Bogotá D.C."}}
        pagina(ruta, f"Filtro nevera Samsung en {nom}, Bogotá | Compra segura",
               f"Filtro de agua para nevera Samsung en {nom} ({loc}, Bogotá): HAF-CIN, HAF-QIN y externo con entrega en {ENTREGA}. Paga en línea con tarjeta, PSE, Nequi o Bancolombia.",
               f"Filtro para nevera Samsung en {nom}, Bogotá", f"{nom} · {loc}",
               f"¿Vives o trabajas en <b>{esc(nom)}</b>, en la localidad de {esc(loc)}? Te llevamos el filtro de agua de tu nevecón Samsung en <b>{ENTREGA}</b>, con pago seguro en línea.",
               ('<div class="m-aviso"><span style="font-size:22px">📍</span><span><b>Nuestra bodega está en Cedritos</b>Estamos en este barrio, en la localidad de Usaquén, al norte de Bogotá.</span></div>' if nom == "Cedritos" else "")
               + tabla([("Barrio", esc(nom)), ("Localidad", f'<a href="{ruta_loc[loc]}">{esc(loc)}</a>'), ("Ciudad", "Bogotá D.C."), ("Entrega", f"{ENTREGA}"), ("Filtros", esc(refs))])
               + pasos(nom)
               + (f'<h2 style="font-size:22px;margin:26px 0 12px">Otros barrios de {esc(loc)}</h2>' + chips([(x["nombre"], ruta_bar[(loc, x["nombre"])]) for x in cerca]) if cerca else "")
               + f'<p class="m-mut" style="margin-top:14px">Más sobre <a href="{ruta_loc[loc]}">filtros Samsung en {esc(loc)}</a> y en <a href="{ruta_zona[zona]}">la zona {esc(zona.lower())} de Bogotá</a>.</p>',
               [(f"¿Entregan el filtro Samsung en {nom}?", f"Sí, entregamos en {nom} ({loc}, Bogotá) en {ENTREGA}."),
                (f"¿Cuánto tarda el filtro en llegar a {nom}?", f"{ENTREGA}, después de confirmar el pago."),
                (f"¿Qué filtro necesito para mi nevera Samsung en {nom}?", f"Depende del modelo: {refs}. Mira la referencia impresa en tu filtro viejo o escribe el modelo en el buscador.")],
               miga_nombre=f"{nom}, Bogotá", ld_extra=servicio)

    # ---------- zonas ----------
    for zona, s in ZONAS.items():
        locs = [l for l, d in LOCALIDADES.items() if d[0] == zona]
        pagina(ruta_zona[zona], f"Filtro nevera Samsung en el {s} de Bogotá | Compra segura",
               f"Filtros de agua Samsung en el {s} de Bogotá: {', '.join(locs[:5])}{' y más' if len(locs) > 5 else ''}. Entrega en {ENTREGA}, pago en línea.",
               f"Filtros Samsung en el {s} de Bogotá", f"Zona {zona.lower()}",
               f"Entregamos filtros de agua Samsung en todas las localidades del {esc(s)} de Bogotá y en sus barrios, en {ENTREGA}.",
               f'<h2 style="font-size:22px;margin:6px 0 12px">Localidades del {esc(s)}</h2>' + chips([(l, ruta_loc[l]) for l in locs])
               + "".join(f'<h3 style="margin:20px 0 8px">{esc(l)}</h3>' + chips([(b["nombre"], ruta_bar[(l, b["nombre"])]) for b in por_loc[l]]) for l in locs)
               + f'<p class="m-mut" style="margin-top:16px">Mira <a href="{hub}">todas las localidades de Bogotá</a>.</p>',
               [(f"¿Entregan filtros Samsung en el {s} de Bogotá?", f"Sí, en todas sus localidades ({', '.join(locs)}) y en sus barrios, en {ENTREGA}."),
                ("¿Cómo pago?", "En línea, en la pasarela segura de Wompi, con tarjeta, PSE, Nequi o Bancolombia.")],
               miga_nombre=f"Zona {zona.lower()}")

    # ---------- barrios por tipo: zonas de edificios y barrios residenciales selectos / barrios populares ----------
    CATS = CATS_OVERRIDE or {
        "barrios-exclusivos": ("Filtros Samsung en los barrios más exclusivos de Bogotá", "barrios exclusivos y residenciales de Bogotá",
                               ["El Chicó", "Chicó Norte", "Rosales", "El Nogal", "Santa Bárbara", "Country Club", "Antiguo Country", "Quinta Camacho", "El Retiro", "Los Cedros", "Cedritos", "Colina Campestre", "Niza", "Pontevedra", "Lago Gaitán", "Modelia", "Park Way", "Polo Club", "La Castellana", "Santa Ana"],
                               "En estos barrios abundan los apartamentos y las casas con nevecones de gama alta; entregamos hasta la portería o la puerta."),
        "barrios-populares": ("Filtros Samsung en los barrios populares de Bogotá", "barrios populares del sur, occidente y centro de Bogotá",
                              ["Kennedy Central", "Patio Bonito", "Bosa Centro", "Lucero", "Perdomo", "Arborizadora Alta", "Usme Centro", "Santa Librada", "Quiroga", "Diana Turbay", "20 de Julio", "Tunjuelito Centro", "Timiza", "Techo", "Porvenir", "Villa Javier", "Tibabuyes", "Garcés Navas", "Marruecos", "Olaya", "San Blas", "Yomasa", "El Tesoro", "Candelaria La Nueva"],
                              "Entregamos en todos los barrios de Bogotá, también en las zonas de ladera."),
    }
    ruta_cat = {}
    for k, (tit, nombre_c, lista, intro_c) in CATS.items():
        ruta_cat[k] = f"{base}filtros-samsung-{k}-de-bogota/"
        presentes = [b for b in barrios if b["nombre"] in lista]
        pagina(ruta_cat[k], tit + " | Compra segura", f"Filtros de agua Samsung HAF-CIN, HAF-QIN y externo en {len(presentes)} {nombre_c}: entrega en {ENTREGA} y pago seguro en línea.",
               tit, "Bogotá por barrios", f"{intro_c} Entrega en <b>{ENTREGA}</b>.",
               '<h2 style="font-size:22px;margin:6px 0 12px">Barrios donde entregamos</h2>' + chips([(b["nombre"], ruta_bar[(b["loc"], b["nombre"])]) for b in presentes])
               + f'<p class="m-mut" style="margin-top:16px">Mira <a href="{hub}">todas las localidades y barrios de Bogotá</a>.</p>',
               [("¿Entregan en cualquier barrio de Bogotá?", f"Sí, en todos, en {ENTREGA}.")], miga_nombre=nombre_c.capitalize())

    # ---------- municipios cercanos ----------
    for m in MUNICIPIOS:
        pagina(ruta_mun[m], f"Filtro nevera Samsung en {m} | Envío gratis desde Bogotá",
               f"Filtros de agua Samsung HAF-CIN, HAF-QIN y externo en {m}, Cundinamarca: envío gratis desde Bogotá y pago en línea con tarjeta, PSE o Nequi.",
               f"Filtro para nevera Samsung en {m}, Cundinamarca", f"{m} · cerca de Bogotá",
               f"Enviamos el filtro de agua de tu nevecón Samsung a <b>{esc(m)}</b> desde Bogotá, con envío gratis y pago seguro en línea. Llega de 2 a 3 días hábiles.",
               tabla([("Municipio", esc(m)), ("Departamento", "Cundinamarca"), ("Entrega", "De 2 a 3 días hábiles"), ("Envío", "Gratis"), ("Filtros", esc(refs))]) + pasos(m)
               + f'<p class="m-mut" style="margin-top:14px">Mira las <a href="{hub}">localidades de Bogotá</a> donde entregamos.</p>',
               [(f"¿Envían filtros Samsung a {m}?", f"Sí, enviamos a {m} desde Bogotá con envío gratis."),
                (f"¿Cuánto tarda a {m}?", "De 2 a 3 días hábiles, con número de guía.")],
               miga_nombre=m)

    # ---------- listado de todas las localidades ----------
    cuerpo = ""
    for zona in ZONAS:
        cuerpo += f'<h2 style="font-size:24px;margin:26px 0 10px"><a href="{ruta_zona[zona]}" style="color:inherit">Zona {esc(zona.lower())}</a></h2>'
        for l, d in LOCALIDADES.items():
            if d[0] != zona:
                continue
            cuerpo += f'<h3 style="margin:16px 0 8px"><a href="{ruta_loc[l]}">{esc(l)}</a></h3>' + chips([(b["nombre"], ruta_bar[(l, b["nombre"])]) for b in por_loc[l]])
    cuerpo += ('<h2 style="font-size:24px;margin:30px 0 10px">Por tipo de barrio</h2>' + chips([("Barrios exclusivos y residenciales", ruta_cat["barrios-exclusivos"]), ("Barrios populares", ruta_cat["barrios-populares"])]))
    pagina(hub, f"Filtros Samsung en Bogotá: todas las localidades y barrios",
           f"Entregamos filtros de agua Samsung en las {len(LOCALIDADES)} localidades de Bogotá y en {len(barrios)} barrios, con entrega en {ENTREGA} y pago seguro en línea.",
           "Filtros de agua Samsung en todas las localidades de Bogotá", "Cobertura en Bogotá",
           f"Escoge tu localidad o tu barrio: entregamos en <b>{len(LOCALIDADES)} localidades</b> y <b>{len(barrios)} barrios</b> de Bogotá.", cuerpo,
           [("¿En qué zonas de Bogotá entregan?", "En las 19 localidades urbanas: norte, centro, occidente y sur, y en los municipios cercanos."),
            ("¿Cuánto tarda la entrega en Bogotá?", f"{ENTREGA}.")], miga_nombre="Todas las localidades")
    return ruta_loc, ruta_bar, ruta_zona, ruta_mun, hub


# ---------- artículos del blog sobre Bogotá ----------
def articulos(ps, base="/", inst="/cambio-e-instalacion/"):
    cin = next(p for p in ps if "HAF-CIN" in " ".join(p["refs"]).upper() or p["ref"] == "DA29-00020B")
    qin = next(p for p in ps if p["ref"] == "DA97-17376B")
    ex = next(p for p in ps if p["ref"] == "DA29-10105J")
    L = lambda p: f'<a href="{base}{p["slug"]}/">{esc(p["nombre_largo"])}</a>'
    A = []
    A.append(("donde-comprar-un-filtro-de-nevera-samsung-en-bogota", "Dónde comprar un filtro de nevera Samsung en Bogotá",
              "Guía para comprar el filtro de agua de tu nevecón Samsung en Bogotá: qué referencia pedir, cuánto cuesta, cuánto tarda y cómo pagar en línea.",
              "Pide la referencia exacta de tu filtro, compra en una tienda que te dé recibo y envío con guía, y paga en una pasarela segura.",
              "<p>En Bogotá hay muchas formas de conseguir un filtro para tu nevecón Samsung. Esto debes mirar antes de comprar:</p>"
              "<ol><li><b>La referencia.</b> Saca el filtro viejo y busca el código (DA29-00020B, DA97-17376B o DA29-10105J).</li><li><b>Que sea nuevo y sellado.</b></li><li><b>El pago.</b> Una pasarela segura (tarjeta, PSE, Nequi o Bancolombia) y recibo por correo.</li><li><b>La entrega.</b> En Bogotá debe llegar en 1 a 2 días hábiles.</li></ol>"
              f"<p>Los filtros que tenemos: {L(cin)}, {L(qin)} y {L(ex)}. Mira <a href=\"{base}filtros-samsung-bogota-por-localidad/\">las localidades de Bogotá</a> donde entregamos.</p>",
              [("¿Cuánto tarda en llegar un filtro en Bogotá?", "Entre 1 y 2 días hábiles después de confirmar el pago."), ("¿Cómo sé cuál filtro necesito?", "Mira la referencia del filtro viejo o escribe el modelo de tu nevecón en el buscador de la página.")]))
    A.append(("filtro-samsung-para-apartamento-en-bogota-como-cambiarlo", "Filtro Samsung en un apartamento en Bogotá: cómo cambiarlo",
              "Paso a paso para cambiar el filtro de agua de tu nevecón Samsung en un apartamento en Bogotá, en minutos y sin técnico.",
              "En un apartamento el cambio se hace igual que en una casa: cierra el agua si es externo, cambia el filtro, purga unos 6 litros y reinicia la luz.",
              "<p>La mayoría de los apartamentos de Bogotá tienen el nevecón junto a una conexión de agua con llave de paso. Eso facilita el cambio:</p>"
              "<ol><li>Identifica tu filtro: interno (dentro del refrigerador) o externo (en la manguera).</li><li>Si es externo, cierra la llave de paso del agua.</li><li>Retira el filtro viejo y pon el nuevo hasta el fondo.</li><li>Saca unos 6 litros por el dispensador para purgar el aire.</li><li>Reinicia la luz del filtro.</li></ol>"
              f"<p>Guía completa en <a href=\"{inst}\">cómo cambiar e instalar tu filtro</a>.</p>",
              [("¿Necesito técnico en mi apartamento?", "No, el cambio toma unos minutos y no requiere herramientas."), ("¿Cada cuánto lo cambio?", "Cada 6 meses.")]))
    A.append(("por-que-cambiar-el-filtro-de-agua-de-tu-nevecon-samsung-cada-6-meses-en-bogota", "Por qué cambiar el filtro de agua del nevecón cada 6 meses en Bogotá",
              "El filtro del nevecón Samsung se satura con el uso: qué retiene, cada cuánto cambiarlo y señales de que ya toca, para casas y apartamentos de Bogotá.",
              "El filtro retiene cloro y sedimentos; con los meses se satura y el agua y el hielo pierden calidad, por eso se cambia cada 6 meses.",
              "<p>El agua llega a tu casa tratada, pero puede traer cloro y partículas de las tuberías. El filtro de carbón activado los retiene y mejora el sabor y el olor del agua y del hielo.</p>"
              "<ul class=\"m-ok\"><li>Con el tiempo el carbón se satura y el filtro deja de retener.</li><li>Un filtro tapado reduce el caudal del dispensador.</li><li>Cámbialo cada 6 meses, o antes si el agua sabe distinto.</li></ul>"
              f"<p>Reemplázalo con el {L(cin)}, el {L(qin)} o el {L(ex)}, según tu nevecón.</p>",
              [("¿Qué pasa si no cambio el filtro?", "El agua puede volver a saber a cloro y el dispensador sacar menos agua."), ("¿Sirve para casas y apartamentos?", "Sí, el filtro funciona igual en casas y apartamentos.")]))
    A.append(("nevecones-samsung-comunes-en-bogota-y-su-filtro", "Nevecones Samsung comunes en Bogotá y su filtro",
              "Qué filtro usa cada nevecón Samsung: modelos RF28HMEDBSR, RF263BEAESR, RF28R7351SR y más, con su referencia y precio.",
              "Cada modelo usa una referencia: los RF28HMEDBSR y similares usan HAF-CIN; los RF28R7351SR y similares, HAF-QIN.",
              "<p>Estos son algunos modelos de nevecón Samsung y su filtro:</p><ul class=\"m-ok\">"
              + "".join(f"<li><b>{esc(m)}</b> → {L(p)}</li>" for p in (cin, qin) for m in p["modelos"][:6]) + "</ul>"
              f"<p>Si tu modelo no está, mira la <a href=\"{base}cual-es-mi-filtro/\">tabla de modelos y referencias</a>.</p>",
              [("¿Dónde veo el modelo de mi nevecón?", "En una etiqueta dentro del refrigerador, en la pared lateral."), ("¿Y si mi modelo no aparece?", "Compara la referencia del filtro viejo con nuestra tabla.")]))
    A.append(("cuanto-tarda-en-llegar-un-filtro-a-tu-barrio-en-bogota", "Cuánto tarda en llegar un filtro a tu barrio en Bogotá",
              "Tiempos de entrega de filtros de agua Samsung en las localidades y barrios de Bogotá: norte, centro, occidente y sur.",
              "En Bogotá llega en 1 a 2 días hábiles a cualquier localidad.",
              f"<p>Entregamos en las {len(LOCALIDADES)} localidades urbanas de Bogotá. El tiempo estimado es de <b>1 a 2 días hábiles</b> desde que se confirma el pago.</p>"
              '<ul class="m-ok">' + "".join(f'<li><a href="{base}filtros-samsung-{zs}-de-bogota/">{esc(z)}</a>: {esc(", ".join(l for l, d in LOCALIDADES.items() if d[0] == z))}.</li>' for z, zs in ZONAS.items()) + "</ul>",
              [("¿Entregan en mi barrio?", "Sí, en todas las localidades y barrios de Bogotá, en 1 a 2 días hábiles.")]))
    return A


POPULARES = ["Usaquén Centro", "Cedritos", "Santa Bárbara", "El Chicó", "Chapinero Central", "Rosales", "Suba Centro", "Niza", "Colina Campestre", "La Gaitana", "Modelia", "Castilla", "Kennedy Central", "Américas",
             "Engativá Centro", "Minuto de Dios", "Boyacá Real", "Teusaquillo Centro", "Galerías", "Ciudad Montes", "Bosa Centro", "Timiza", "Patio Bonito", "Hayuelos", "Restrepo", "20 de Julio", "Ciudad Bolívar", "Lucero", "Usme Centro", "Quiroga"]


GUIAS = [("filtro-de-agua-nevecon-samsung-bogota/", "Guía del filtro Samsung en Bogotá"), ("precio-filtro-nevera-samsung-bogota/", "Precios 2026"), ("comprar-filtro-nevera-samsung-bogota/", "Cómo comprar"),
         ("cambio-de-filtro-nevera-samsung-bogota/", "Cómo cambiarlo"), ("repuesto-filtro-nevera-samsung-bogota/", "Códigos y equivalencias"), ("mejor-filtro-nevera-samsung-bogota-haf-cin-o-haf-qin/", "HAF-CIN o HAF-QIN"),
         ("pack-2-filtros-samsung-bogota/", "Pack de 2 filtros"), ("bodega-cedritos-bogota/", "Nuestra bodega en Cedritos"), ("nevera-samsung-no-saca-agua-bogota/", "Nevera que no saca agua"), ("preguntas-frecuentes/", "Preguntas frecuentes")]
TEXTO_PORTADA = ("Filtros de agua para nevera Samsung en Bogotá: el filtro HAF-CIN (DA29-00020B) y el HAF-QIN (DA97-17376B) cuestan $ 130.900 y el filtro externo DA29-10105J $ 96.900, con pack de 2 para ahorrar. "
                 "Somos una tienda de Cedritos, Usaquén, con pago seguro en línea (tarjeta, PSE, Nequi y Bancolombia) y entrega en 1 a 2 días hábiles en Bogotá, de Usaquén a Ciudad Bolívar y de Suba a Kennedy.")


def bloque_portada(base, sec, cab):
    """Sección de la portada: las 4 zonas con sus localidades y los barrios más buscados (enlaces internos hacia todas las páginas locales)."""
    barrios = {b["nombre"]: b for b in datos()}
    ruta = lambda b: f"{base}filtro-nevera-samsung-{b['slug']}-bogota/"
    zonas = ""
    for z, sl in ZONAS.items():
        locs = [l for l, d in LOCALIDADES.items() if d[0] == z]
        zonas += (f'<div class="m-bloque"><h3><a href="{base}filtros-samsung-{sl}-de-bogota/">Zona {z.lower()}</a></h3><p>'
                  + " · ".join(f'<a href="{base}filtro-nevera-samsung-{slug(l)}-bogota/">{esc(l)}</a>' for l in locs) + "</p></div>")
    pop = "".join(f'<a href="{ruta(barrios[n])}">{esc(n)}</a>' for n in POPULARES if n in barrios)
    return sec(cab("Entregas en Bogotá", "Entregamos en todas las localidades y barrios de Bogotá",
                   f"Escoge tu zona: llegamos en {ENTREGA} a las 19 localidades urbanas y a los municipios cercanos, con pago seguro en línea.")
               + '<div class="m-cols">' + zonas + "</div>"
               + '<h3 style="margin:22px 0 10px">Barrios más buscados</h3><div class="m-chips">' + pop + f'<a href="{base}filtros-samsung-barrios-exclusivos-de-bogota/">Barrios exclusivos</a><a href="{base}filtros-samsung-barrios-populares-de-bogota/">Barrios populares</a><a href="{base}filtros-samsung-bogota-por-localidad/"><b>Ver todas las localidades y barrios →</b></a></div>'
               + '<h3 style="margin:22px 0 10px">Guías para comprar y cambiar tu filtro en Bogotá</h3><div class="m-chips">'
               + "".join(f'<a href="{base}{r}">{esc(t)}</a>' for r, t in GUIAS) + "</div>"
               + '<p class="m-mut" style="margin-top:18px">' + TEXTO_PORTADA + "</p>", alt=True)
