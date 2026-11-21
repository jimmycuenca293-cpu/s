# -*- coding: utf-8 -*-
"""Configuración por sitio. Se elige con la variable de entorno CST_SITIO = panama | cali.
Todo lo que depende del país o de la ciudad vive aquí; el generador (cst_build.py) no tiene datos fijos de un solo sitio."""
import os, re

SITIO = os.environ.get("CST_SITIO", "panama")

PANAMA = dict(
    sitio="panama", dom="https://centrodeserviciotecnicopanama.com", ciudad="Panamá", nombre="Centro de Servicio Técnico Panamá",
    tel="+507 6933-7976", telw="50769337976", locale="es-PA", cc="PA", region="Provincia de Panamá", pais="Panamá",
    gsc=["Ns9i5lJP6EAsC0ExK8vxW-GtkXKO8kdnf7S5kNFx54k", "ozHF9bZezdQ-xxlFh0xMkpJZRx0rwRKgNXAZQhrbmQg"],
    ext_lg=("Página del fabricante: LG Panamá", "https://www.lg.com/pa/"), ext_samsung=("Página del fabricante: Samsung (América Latina)", "https://www.samsung.com/latin/"),
    guia_humedad=("humedad-y-salitre-en-equipos", "Humedad y salitre en equipos {N} en Panamá", "Cómo la humedad y el salitre de Panamá afectan tus equipos {N}: qué fallas provocan y cómo prevenirlas."),
    costero=True, nev=("refrigeradoras", "refrigeradora", "refrigeradoras"),
    zlista="la ciudad de Panamá, San Miguelito, Arraiján, La Chorrera, Costa del Este, Tocumen, Panamá Oeste y Colón",
    sin_recorte=True, lbl_guias="Blog de consejos",
)

# ----------------------------------------------------------------------------- CALI
ZONAS_CALI = {
    "norte-de-cali": ("Norte de Cali", "Versalles, Vipasa, Chipichape, Menga, La Flora, Prados del Norte, Granada, Santa Mónica, Normandía", "Casas y edificios de estratos medios y altos, con mucho uso de aire acondicionado durante todo el año."),
    "sur-de-cali": ("Sur de Cali", "Ciudad Jardín, Valle del Lili, Pance, El Caney, Limonar, Cañasgordas, Mayapán", "Conjuntos residenciales y edificios modernos, con equipos de gama alta y varios años de uso intensivo."),
    "oeste-de-cali": ("Oeste de Cali", "Santa Teresita, El Peñón, San Fernando, Santa Rita, Juanambú, Arboledas", "Barrios tradicionales y edificios altos cerca de las laderas del oeste, con instalaciones eléctricas de distintas épocas."),
    "oriente-de-cali": ("Oriente de Cali", "Alfonso López, Manuela Beltrán, El Retiro, Mojica, Potrero Grande, Calipso", "Zona residencial muy poblada, con casas de varios pisos y muchos equipos de uso diario."),
    "centro-de-cali": ("Centro de Cali", "San Antonio, San Nicolás, Alameda, San Cayetano, El Centro", "Edificios antiguos y mezcla de vivienda y comercio, donde el cableado viejo exige cuidado con la corriente."),
    "jamundi": ("Jamundí", "Jamundí centro, Alfaguara, Potrerito", "Conjuntos campestres y casas con patio al sur del Valle, con distancias mayores desde Cali."),
    "yumbo": ("Yumbo", "Yumbo centro, Mulaló", "Zona industrial y residencial al norte de Cali."),
    "palmira": ("Palmira", "Palmira centro, Rozo", "Ciudad intermedia al oriente del Valle, con viviendas amplias y equipos de uso familiar."),
}
ZX_CALI = {
    "norte-de-cali": ("casas y edificios de estratos medios y altos", "el tráfico de la avenida Sexta y de la calle Quinta en horas pico", "Versalles, Vipasa, Chipichape y Menga"),
    "sur-de-cali": ("conjuntos residenciales y edificios modernos", "los controles de acceso de los conjuntos y los horarios de ascensor o mudanza", "Ciudad Jardín, Valle del Lili y Pance"),
    "oeste-de-cali": ("barrios tradicionales y edificios altos", "las calles con pendiente y los parqueaderos limitados de algunos edificios", "El Peñón, San Fernando y Santa Rita"),
    "oriente-de-cali": ("viviendas muy pobladas, con varios pisos", "la distancia desde el norte y el tráfico de hora pico", "Alfonso López, Manuela Beltrán y El Retiro"),
    "centro-de-cali": ("edificios antiguos que mezclan vivienda y comercio", "el tráfico y los pocos parqueaderos del centro", "San Antonio, San Nicolás y Alameda"),
    "jamundi": ("conjuntos campestres y casas con patio", "la distancia desde Cali al pedir la franja", "Jamundí centro, Alfaguara y Potrerito"),
    "yumbo": ("zona residencial e industrial", "el tráfico de la vía Cali–Yumbo", "Yumbo centro y Mulaló"),
    "palmira": ("viviendas amplias de uso familiar", "la distancia desde Cali y el tráfico de la vía a Palmira", "Palmira centro y Rozo"),
}
CLIMA_CALI = {
    "norte-de-cali": "el uso casi permanente del aire acondicionado y los picos de voltaje en tormentas eléctricas",
    "sur-de-cali": "el uso intensivo del aire acondicionado en edificios cerrados y los picos de voltaje en tormentas",
    "oeste-de-cali": "la humedad de las épocas de lluvia y las instalaciones eléctricas de distintas épocas",
    "oriente-de-cali": "el calor constante y la sobrecarga de circuitos cuando varios equipos funcionan a la vez",
    "centro-de-cali": "el cableado antiguo de algunos edificios y la humedad de las épocas de lluvia",
    "jamundi": "el calor, el polvo de las vías y las tormentas eléctricas del sur del Valle",
    "yumbo": "el polvo de la zona industrial y los picos de voltaje por tormentas",
    "palmira": "el calor del valle y las tormentas eléctricas en época de lluvia",
}
CALI = dict(
    sitio="cali", dom="https://centrodeserviciotecnicocali.com", ciudad="Cali", nombre="Centro de Servicio Técnico Cali",
    tel="+57 301 381 0242", telw="573013810242", locale="es-CO", cc="CO", region="Valle del Cauca", pais="Colombia",
    gsc=["IbsGW5jGisWODCoe6x1vv2zXSa8Gjj9hKC65vEEUm3c"],
    ext_lg=("Página del fabricante: LG Colombia", "https://www.lg.com/co/"), ext_samsung=("Página del fabricante: Samsung Colombia", "https://www.samsung.com/co/"),
    guia_humedad=("humedad-y-calor-en-equipos", "Humedad y calor en equipos {N} en Cali", "Cómo la humedad, el calor y las lluvias de Cali afectan tus equipos {N}: qué fallas provocan y cómo prevenirlas."),
    costero=False, nev=("neveras", "nevera", "neveras"),
    zonas=ZONAS_CALI, zx=ZX_CALI, clima=CLIMA_CALI,
    area=["Cali", "Jamundí", "Yumbo", "Palmira"], geo=(3.4516, -76.5320), geo_region="CO-VAC",
    zlista="el norte, el sur, el oeste, el oriente y el centro de Cali, y también en Jamundí, Yumbo y Palmira",
    sin_recorte=True, lbl_guias="Blog de consejos",
    zart={"norte-de-cali": "el norte de Cali", "sur-de-cali": "el sur de Cali", "oeste-de-cali": "el oeste de Cali", "oriente-de-cali": "el oriente de Cali", "centro-de-cali": "el centro de Cali"},
)

# ----------------------------------------------------------------------------- GUAYAQUIL
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent / "gye"))
try:
    from datos_sitio import ZONAS as _ZG
except Exception:
    _ZG = []
ZONAS_GYE = {z["slug"]: (z["nombre"], z["barrios"][0].upper() + z["barrios"][1:], z["vivienda"].split(". ")[0] + ".") for z in _ZG}
ZX_GYE = {
    "norte-de-guayaquil": ("edificios de departamentos, conjuntos y casas amplias con varios aires acondicionados", "el ingreso por portería y el horario del ascensor de carga cuando el equipo es grande", "Urdesa, Kennedy, Alborada, Samanes, Sauces y Garzota"),
    "ceibos-y-via-a-la-costa": ("casas grandes y urbanizaciones cerradas en zonas de lomas", "el registro previo en las urbanizaciones cerradas", "Los Ceibos, Colinas de los Ceibos y la Vía a la Costa"),
    "sur-de-guayaquil": ("casas de uno y varios pisos y edificios más antiguos", "las calles angostas y el acceso en algunos sectores", "Guasmo, La Floresta y Barrio Cuba"),
    "centro-de-guayaquil": ("edificios antiguos que mezclan vivienda, oficinas y comercio", "el tráfico y el poco estacionamiento del centro", "el Centro, la avenida 9 de Octubre, Boyacá y el Barrio Orellana"),
    "samborondon-y-la-puntilla": ("urbanizaciones cerradas y torres de departamentos modernas", "el registro de ingreso del conjunto y de la torre", "La Puntilla, Entre Ríos y Samborondón"),
    "daule-y-via-a-daule": ("urbanizaciones y casas familiares con patio y lavandería", "la distancia desde el centro y la franja horaria que se pida", "La Aurora, Pascuales y la Vía a Daule"),
    "duran": ("viviendas amplias de uso familiar y comercios", "el tráfico del puente y la franja horaria", "el centro de Durán y los sectores cercanos al puente"),
}
CLIMA_GYE = {
    "norte-de-guayaquil": "el uso casi permanente del aire acondicionado, el calor y la humedad altos y los picos de voltaje en tormentas",
    "ceibos-y-via-a-la-costa": "el viento y el polvo que ensucian los condensadores y las tormentas eléctricas de la temporada de lluvias",
    "sur-de-guayaquil": "la humedad alta y las instalaciones eléctricas de distintas épocas con muchos equipos en el mismo circuito",
    "centro-de-guayaquil": "el calor intenso, los edificios con poca ventilación y el cableado antiguo de algunos inmuebles",
    "samborondon-y-la-puntilla": "la cercanía al río, la humedad y la electrónica sensible de los equipos de gama alta",
    "daule-y-via-a-daule": "el calor fuerte, las tormentas eléctricas y los apagones de la época de lluvias",
    "duran": "el calor, la humedad y la corrosión de contactos y condensadores por la cercanía al río",
}
GUAYAQUIL = dict(
    sitio="guayaquil", dom="https://servicio-tecnico-guayaquil.com", ciudad="Guayaquil", nombre="Servicio Técnico Guayaquil",
    tel="+593 98 039 8179", telw="593980398179", locale="es-EC", cc="EC", region="Guayas", pais="Ecuador",
    gsc=["gEedz31KKCKIhiH6gAv3MPCE4K0x9uEcJW4FHG_Acwc"],
    ext_lg=("Página del fabricante: LG Ecuador", "https://www.lg.com/ec/"), ext_samsung=("Página del fabricante: Samsung Ecuador", "https://www.samsung.com/ec/"),
    guia_humedad=("humedad-y-calor-en-equipos", "Humedad, calor y lluvias en equipos {N} en Guayaquil", "Cómo la humedad, el calor y las lluvias de Guayaquil afectan tus equipos {N}: qué fallas provocan y cómo prevenirlas."),
    costero=False, nev=("refrigeradoras", "refrigeradora", "refrigeradoras"),
    zonas=ZONAS_GYE, zx=ZX_GYE, clima=CLIMA_GYE,
    area=["Guayaquil", "Samborondón", "Daule", "Durán"], geo_region="EC-G",
    zlista="el norte, el sur, el centro, Los Ceibos y la Vía a la Costa, Samborondón y La Puntilla, la Vía a Daule y Durán",
    zart={"norte-de-guayaquil": "el norte de Guayaquil", "ceibos-y-via-a-la-costa": "Los Ceibos y la Vía a la Costa", "sur-de-guayaquil": "el sur de Guayaquil", "centro-de-guayaquil": "el centro de Guayaquil",
          "samborondon-y-la-puntilla": "Samborondón y La Puntilla", "daule-y-via-a-daule": "Daule y la Vía a Daule", "duran": "Durán"},
    ley_datos="Ley Orgánica de Protección de Datos Personales del Ecuador", ley_consumo="Ley Orgánica de Defensa del Consumidor del Ecuador",
    sin_recorte=True, lbl_guias="Blog de consejos",
)
CFG = {"cali": CALI, "guayaquil": GUAYAQUIL}.get(SITIO, PANAMA)

# ----------------------------------------------------------------------------- localización de datos (solo Cali)
REEMP_CALI = [
    ("La falla más frecuente en Panamá no es el gas: es la placa de la unidad exterior afectada por picos de voltaje y por el salitre.", "Una falla frecuente es la placa de la unidad exterior, afectada por picos de voltaje y por la humedad."),
    ("El condensador y el filtro se tapan de pelusa, y eso pasa más rápido en Panamá, donde la ropa seca arrastra pelusa de toallas y sábanas nuevas.", "El condensador y el filtro se tapan de pelusa y conviene limpiarlos con frecuencia."),
    ("En zonas costeras de Panamá el condensador exterior se corroe antes que el compresor.", "El condensador exterior acumula polvo y humedad y conviene limpiarlo con regularidad."),
    ("Las cocinas Mabe a gas son de las más comunes en Panamá, con quemadores sellados y horno a gas con termostato de bulbo.", "Las cocinas Mabe a gas traen quemadores sellados y horno a gas con termostato de bulbo."),
    ("En Panamá, el condensador exterior se ensucia con facilidad.", "El condensador exterior se ensucia con facilidad."),
    ("En equipos importados a Panamá, la cobertura local puede cambiar.", "Si el equipo fue comprado en otro país, la cobertura puede cambiar."),
    ("Haceb es una marca colombiana de electrodomésticos, muy extendida en Panamá en refrigeradoras, lavadoras, estufas y hornos de gas. Muchos equipos llegan por importación y comparten repuestos con modelos vendidos en Colombia.", "Haceb es una marca colombiana de electrodomésticos: neveras, lavadoras, secadoras, estufas, hornos de gas y aires acondicionados."),
    ("disponibles en Panamá", "disponibles en " + CFG["pais"]),
]
def _vocab(t):
    t = re.sub(r"\b([Rr])efrigeradora(s?)\b", lambda m: ("N" if m.group(1) == "R" else "n") + "evera" + m.group(2), t)
    return t
def _sentencias_sin_ciudad(t):
    ps = re.split(r"(?<=[.])\s+", t.strip())
    return " ".join(p for p in ps if "Panamá" not in p)
def _loc_str(t, clave=None):
    for a, b in REEMP_CALI: t = t.replace(a, b)
    if clave == "origen": t = _sentencias_sin_ciudad(t)
    t = t.replace("humedad y salitre", "humedad y calor").replace("la humedad y el salitre", "la humedad y el calor")
    t = t.replace("en Panamá", "en " + CFG["pais"]).replace("Panamá", CFG["pais"])
    return _vocab(t) if CFG["nev"][1] != "refrigeradora" else t
def _deep(x, clave=None):
    if isinstance(x, str): return _loc_str(x, clave)
    if isinstance(x, dict): return {k: _deep(v, k) for k, v in x.items()}
    if isinstance(x, list): return [_deep(v, clave) for v in x]
    if isinstance(x, tuple): return tuple(_deep(v, clave) for v in x)
    return x
def localizar(obj):
    """Devuelve una copia de los datos adaptada al sitio activo (identidad en Panamá)."""
    return obj if CFG["sitio"] == "panama" else _deep(obj)

# ----------------------------------------------------------------------------- localización del HTML final (solo Cali)
def L(h):
    if CFG["sitio"] == "panama": return h
    _rutas = []
    def _g(m): _rutas.append(m.group(0)); return "\x00%d\x00" % (len(_rutas) - 1)
    h = re.sub(r"/img/[^\"'\s)<>]+", _g, h)
    ld = CFG.get("ley_datos", "Ley 1581 de 2012 de Colombia"); lc = CFG.get("ley_consumo", "Ley 1480 de 2011 (Estatuto del Consumidor) de Colombia")
    for a, b in [
        ("Ley 81 de 2019 de Panamá", ld), ("Ley 81 de 2019", ld),
        ("Ley 45 de 2007 de Panamá", lc), ("conseguirse en Panamá", "conseguirse en " + CFG["pais"]), ("Ciudad de Panamá", CFG["ciudad"]), ("Provincia de Panamá", CFG["region"]),
        ("es-PA", CFG["locale"]), ("es_PA", CFG["locale"].replace("-", "_")), ('"addressCountry": "PA"', '"addressCountry": "%s"' % CFG["cc"]),
        ("en Panamá", "en " + CFG["ciudad"]), ("de Panamá", "de " + CFG["ciudad"]), ("Panamá", CFG["ciudad"]), ("Panam%C3%A1", CFG["ciudad"]),
    ]: h = h.replace(a, b)
    if CFG["nev"][1] != "refrigeradora":
        h = re.sub(r"\b([Rr])efrigeradora(s?)\b", lambda m: ("N" if m.group(1) == "R" else "n") + "evera" + m.group(2), h)
    h = h.replace("humedad y salitre", "humedad y calor").replace("Humedad y salitre", "Humedad y calor")
    h = re.sub(r"(%s) \| %s\b" % (CFG["ciudad"], CFG["ciudad"]), r"\1", h)
    return re.sub(r"\x00(\d+)\x00", lambda m: _rutas[int(m.group(1))], h)
