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

# ----------------------------------------------------------------------------- QUITO
ZONAS_QUITO = {
    "norte-de-quito": ("Norte de Quito", "La Carolina, Iñaquito, El Batán, Quito Tennis, Jipijapa, Cotocollao y Carcelén", "Edificios de departamentos, casas y conjuntos de estratos medios y altos."),
    "centro-norte-de-quito": ("Centro norte de Quito", "La Mariscal, González Suárez, La Floresta, Guápulo y Bellavista", "Edificios de departamentos y casas antiguas en barrios muy céntricos."),
    "centro-historico-de-quito": ("Centro Histórico de Quito", "el Centro Histórico, San Marcos, San Juan y La Loma", "Casas y edificios antiguos que mezclan vivienda y comercio."),
    "sur-de-quito": ("Sur de Quito", "Quitumbe, Chillogallo, La Magdalena, Solanda, Villaflora y Chimbacalle", "Barrios muy poblados con casas de varios pisos y mucho uso diario de electrodomésticos."),
    "valle-de-los-chillos": ("Valle de Los Chillos", "San Rafael, Sangolquí, Conocoto y Amaguaña", "Conjuntos residenciales y casas amplias al oriente de la ciudad."),
    "cumbaya-y-tumbaco": ("Cumbayá y Tumbaco", "Cumbayá, Lumbisí, Tumbaco, Puembo y Pifo", "Urbanizaciones y casas con jardín, con equipos de gama media y alta."),
    "calderon-y-pomasqui": ("Calderón y Pomasqui", "Calderón, Carapungo, Pomasqui y San Antonio de Pichincha", "Barrios y urbanizaciones del norte, con casas familiares de uso intensivo."),
}
ZX_QUITO = {
    "norte-de-quito": ("edificios de departamentos y casas de estratos medios y altos", "el ingreso por portería y el horario del ascensor de carga cuando el equipo es grande", "La Carolina, Iñaquito, El Batán y Cotocollao"),
    "centro-norte-de-quito": ("edificios de departamentos y casas antiguas en calles estrechas", "el tráfico y el poco estacionamiento de la zona", "La Mariscal, González Suárez, La Floresta y Guápulo"),
    "centro-historico-de-quito": ("casas y edificios antiguos de varios pisos, muchos sin ascensor", "las calles empinadas y de acceso restringido para vehículos", "el Centro Histórico, San Marcos y San Juan"),
    "sur-de-quito": ("casas de varios pisos y barrios muy poblados", "la distancia desde el norte y el tráfico de hora pico", "Quitumbe, Chillogallo, Solanda y Villaflora"),
    "valle-de-los-chillos": ("conjuntos residenciales y casas amplias", "el tráfico de la autopista y el registro de ingreso de cada conjunto", "San Rafael, Sangolquí y Conocoto"),
    "cumbaya-y-tumbaco": ("urbanizaciones y casas con jardín", "el registro de ingreso de cada urbanización y la distancia al coordinar la franja", "Cumbayá, Tumbaco y Puembo"),
    "calderon-y-pomasqui": ("barrios familiares y urbanizaciones del norte", "la distancia desde el centro y el tráfico de la vía Panamericana", "Calderón, Carapungo y Pomasqui"),
}
CLIMA_QUITO = {
    "norte-de-quito": "la altura, el clima fresco y las lluvias de la tarde, que traen tormentas eléctricas y picos de voltaje",
    "centro-norte-de-quito": "la altura, los cambios de temperatura entre el día y la noche y los cortes de energía en la temporada de lluvias",
    "centro-historico-de-quito": "el cableado antiguo de muchos inmuebles y la humedad de las casas de piedra y adobe",
    "sur-de-quito": "el uso intensivo de los electrodomésticos, el polvo de los meses secos y los picos de voltaje en tormentas",
    "valle-de-los-chillos": "el clima más templado que el centro, el polvo de los meses secos y las tormentas de la temporada de lluvias",
    "cumbaya-y-tumbaco": "el clima templado y seco, el polvo y las tormentas eléctricas de la temporada de lluvias",
    "calderon-y-pomasqui": "el viento y el polvo de los meses secos y las tormentas con granizo de la temporada de lluvias",
}
QUITO = dict(
    sitio="quito", dom="https://servicio-tecnico-quito.com", ciudad="Quito", nombre="Servicio Técnico Quito",
    tel="+593 98 039 8179", telw="593980398179", locale="es-EC", cc="EC", region="Pichincha", pais="Ecuador",
    gsc=["44WKxBkABsUarAnT8SfL6pqLT-POtaKN39b-lDkuhUI"],
    ext_lg=("Página del fabricante: LG Ecuador", "https://www.lg.com/ec/"), ext_samsung=("Página del fabricante: Samsung Ecuador", "https://www.samsung.com/ec/"),
    guia_humedad=("altura-frio-y-lluvias-en-equipos", "Altura, frío y lluvias en equipos {N} en Quito", "Cómo la altura, los cambios de temperatura y la temporada de lluvias de Quito afectan tus equipos {N}: qué fallas provocan y cómo prevenirlas."),
    intro_clima="Quito está a unos 2.850 metros de altura, con clima fresco y una temporada de lluvias con tormentas eléctricas y granizo. No hay calor húmedo, pero la humedad de las lluvias y la condensación por los cambios de temperatura entre el día y la noche también afectan a los equipos.",
    costero=False, frio=True, nev=("refrigeradoras", "refrigeradora", "refrigeradoras"),
    zonas=ZONAS_QUITO, zx=ZX_QUITO, clima=CLIMA_QUITO,
    area=["Quito", "Cumbayá", "Sangolquí", "Calderón"], geo_region="EC-P",
    zlista="el norte, el centro norte, el Centro Histórico, el sur, el Valle de Los Chillos, Cumbayá y Tumbaco, y Calderón y Pomasqui",
    zart={"norte-de-quito": "el norte de Quito", "centro-norte-de-quito": "el centro norte de Quito", "centro-historico-de-quito": "el Centro Histórico de Quito", "sur-de-quito": "el sur de Quito",
          "valle-de-los-chillos": "el Valle de Los Chillos", "cumbaya-y-tumbaco": "Cumbayá y Tumbaco", "calderon-y-pomasqui": "Calderón y Pomasqui"},
    ley_datos="Ley Orgánica de Protección de Datos Personales del Ecuador", ley_consumo="Ley Orgánica de Defensa del Consumidor del Ecuador",
    sin_recorte=True, lbl_guias="Blog de consejos",
)

# ----------------------------------------------------------------------------- COSTA RICA (pantallas)
ZONAS_CR = {
    "san-jose": ("San José", "San José centro, Barrio Escalante, Sabana, Pavas, Hatillo y Desamparados", "Ciudad capital con edificios, apartamentos y casas antiguas y modernas."),
    "escazu-y-santa-ana": ("Escazú y Santa Ana", "Escazú, San Rafael de Escazú, Santa Ana, Pozos y Lindora", "Condominios y casas de gama media y alta, con pantallas grandes y equipos de cine en casa."),
    "heredia": ("Heredia", "Heredia centro, San Pablo, Santo Domingo, Belén y San Rafael", "Casas, condominios y barrios universitarios al norte del Valle Central."),
    "alajuela": ("Alajuela", "Alajuela centro, San Antonio, La Guácima, Río Segundo y Atenas", "Viviendas familiares y condominios cerca del aeropuerto y del Valle Central."),
    "cartago": ("Cartago", "Cartago centro, Paraíso, Tres Ríos y Oreamuno", "Casas y condominios en una zona fresca y húmeda del Valle Central."),
    "curridabat-y-san-pedro": ("Curridabat y San Pedro", "Curridabat, San Pedro, Montes de Oca, Sabanilla y Zapote", "Barrios y condominios del este de San José, con mucha vivienda de estudiantes y familias."),
    "liberia-y-guanacaste": ("Liberia y Guanacaste", "Liberia, Nicoya, Santa Cruz, Playas del Coco y Tamarindo", "Casas, hoteles y alquileres vacacionales en una zona cálida, con estación seca marcada."),
}
ZX_CR = {
    "san-jose": ("edificios, apartamentos y casas de varias épocas", "el tráfico y el estacionamiento limitado del centro", "San José centro, Barrio Escalante, Sabana y Pavas"),
    "escazu-y-santa-ana": ("condominios y casas con pantallas grandes y equipos de cine en casa", "el registro de ingreso del condominio y la distancia al coordinar la franja", "Escazú, Santa Ana, Pozos y Lindora"),
    "heredia": ("casas, condominios y barrios universitarios", "el tráfico hacia el norte del Valle Central", "Heredia centro, San Pablo, Belén y Santo Domingo"),
    "alajuela": ("viviendas familiares y condominios", "el tráfico de la autopista y la distancia al coordinar la franja", "Alajuela centro, San Antonio, La Guácima y Río Segundo"),
    "cartago": ("casas y condominios en una zona fresca", "la distancia desde San José y el tráfico de la ruta a Cartago", "Cartago centro, Paraíso, Tres Ríos y Oreamuno"),
    "curridabat-y-san-pedro": ("barrios y condominios del este de San José", "el tráfico de hora pico y el poco estacionamiento", "Curridabat, San Pedro, Sabanilla y Zapote"),
    "liberia-y-guanacaste": ("casas, hoteles y alquileres vacacionales", "la distancia desde San José y la coordinación previa de la visita", "Liberia, Nicoya, Santa Cruz y las playas cercanas"),
}
CLIMA_CR = {
    "san-jose": "las tormentas eléctricas de la temporada de lluvias, que traen picos de voltaje, y los cortes de energía ocasionales",
    "escazu-y-santa-ana": "las tormentas eléctricas de la temporada de lluvias y la electrónica sensible de las pantallas grandes y los equipos de cine en casa",
    "heredia": "las lluvias de la tarde, la humedad y los picos de voltaje en tormentas",
    "alajuela": "el calor del Valle Central, las tormentas eléctricas y los picos de voltaje",
    "cartago": "el clima fresco y húmedo, que favorece la condensación en la electrónica, y las tormentas de la temporada de lluvias",
    "curridabat-y-san-pedro": "las tormentas eléctricas de la temporada de lluvias y el uso intensivo de las pantallas en viviendas de estudiantes y familias",
    "liberia-y-guanacaste": "el calor intenso, la estación seca con polvo y las tormentas eléctricas con picos de voltaje de la temporada de lluvias",
}
COSTARICA = dict(
    sitio="costarica", dom="https://servicio-tecnico-costa-rica.com", ciudad="Costa Rica", nombre="Servicio Técnico Costa Rica",
    tel="+506 7005-5853", telw="50670055853", locale="es-CR", cc="CR", region="San José", pais="Costa Rica",
    gsc=["XYsqhIDh94Jrxjg0dah9SUxAZTDy98U0yn3pNy_Sb7E"],
    ext_lg=("Página del fabricante: LG Costa Rica", "https://www.lg.com/cr/"), ext_samsung=("Página del fabricante: Samsung Costa Rica", "https://www.samsung.com/cr/"),
    guia_humedad=("humedad-calor-y-lluvias-en-equipos", "Humedad, calor y lluvias en tus equipos {N} en Costa Rica", "Cómo la humedad, el calor y la temporada de lluvias de Costa Rica afectan tus equipos {N}: qué fallas provocan y cómo prevenirlas."),
    intro_clima="En Costa Rica hay una estación seca y una temporada de lluvias con tormentas eléctricas casi diarias en muchas zonas, además de humedad alta en la costa y el Caribe.",
    costero=False, nev=("refrigeradoras", "refrigeradora", "refrigeradoras"),
    zonas=ZONAS_CR, zx=ZX_CR, clima=CLIMA_CR,
    area=["San José", "Escazú", "Heredia", "Alajuela", "Cartago", "Liberia"], geo_region="CR-SJ",
    zlista="San José, Escazú y Santa Ana, Heredia, Alajuela, Cartago, Curridabat y San Pedro, y Liberia y Guanacaste",
    zart={"san-jose": "San José", "escazu-y-santa-ana": "Escazú y Santa Ana", "heredia": "Heredia", "alajuela": "Alajuela", "cartago": "Cartago", "curridabat-y-san-pedro": "Curridabat y San Pedro", "liberia-y-guanacaste": "Liberia y Guanacaste"},
    ley_datos="Ley 8968 de Protección de la Persona frente al tratamiento de sus datos personales de Costa Rica", ley_consumo="Ley 7472 de Promoción de la Competencia y Defensa Efectiva del Consumidor de Costa Rica",
    sin_recorte=True, lbl_guias="Blog de consejos", mix=True, seo_plus=True,
)

# ----------------------------------------------------------------------------- BUCARAMANGA (electrodomésticos)
ZONAS_BGA = {
    "cabecera-y-sotomayor": ("Cabecera y Sotomayor", "Cabecera del Llano, Sotomayor, Alarcón, Mejoras Públicas", "Edificios altos y apartamentos modernos, con equipos de gama media y alta y mucho uso diario."),
    "centro-de-bucaramanga": ("Centro de Bucaramanga", "Centro, García Rovira, San Francisco, La Concordia", "Edificios antiguos que mezclan vivienda y comercio, con instalaciones eléctricas de distintas épocas."),
    "norte-de-bucaramanga": ("Norte de Bucaramanga", "Kennedy, La Joya, Mutis", "Barrios residenciales muy poblados, con casas de varios pisos y equipos de uso familiar."),
    "provenza-y-real-de-minas": ("Provenza y Real de Minas", "Provenza, Real de Minas", "Conjuntos y edificios residenciales en el sur de la ciudad, con acceso controlado."),
    "floridablanca": ("Floridablanca", "Floridablanca centro, Cañaveral, Zapamanga, Bellavista", "Conjuntos residenciales y casas en el área metropolitana, con distancias mayores desde el centro de Bucaramanga."),
    "giron": ("Girón", "Girón centro histórico, Ciudad Valencia, El Poblado", "Casas tradicionales del centro histórico y conjuntos nuevos hacia el occidente."),
    "piedecuesta": ("Piedecuesta", "Piedecuesta centro, Guatiguará", "Casas y conjuntos campestres al sur del área metropolitana, con distancias mayores."),
}
ZX_BGA = {
    "cabecera-y-sotomayor": ("edificios altos y apartamentos modernos", "los controles de acceso de los edificios y las calles con pendiente", "Cabecera del Llano, Sotomayor y Alarcón"),
    "centro-de-bucaramanga": ("edificios antiguos que mezclan vivienda y comercio", "el tráfico y los pocos parqueaderos del centro", "el Centro, García Rovira y San Francisco"),
    "norte-de-bucaramanga": ("viviendas muy pobladas, con varios pisos", "las calles con pendiente y el tráfico de hora pico", "Kennedy, La Joya y Mutis"),
    "provenza-y-real-de-minas": ("conjuntos y edificios residenciales", "los controles de acceso de los conjuntos", "Provenza y Real de Minas"),
    "floridablanca": ("conjuntos residenciales y casas", "la distancia desde Bucaramanga y el tráfico de la autopista", "Floridablanca centro, Cañaveral y Zapamanga"),
    "giron": ("casas tradicionales y conjuntos nuevos", "la distancia desde Bucaramanga al pedir la franja", "el centro histórico de Girón y Ciudad Valencia"),
    "piedecuesta": ("casas y conjuntos campestres", "la distancia desde Bucaramanga y el tráfico de la vía a Piedecuesta", "Piedecuesta centro y Guatiguará"),
}
_CL_BGA = "las dos temporadas de lluvias del año, con tormentas eléctricas y picos de voltaje, y las calles con pendiente que dificultan el acceso con equipos pesados"
CLIMA_BGA = {z: _CL_BGA for z in ZONAS_BGA}
CLIMA_BGA["floridablanca"] = "las tormentas eléctricas de las temporadas de lluvias y los picos de voltaje que traen"
BUCARAMANGA = dict(
    sitio="bucaramanga", dom="https://servicio-tecnico-bucaramanga.com", ciudad="Bucaramanga", nombre="Servicio Técnico Bucaramanga",
    tel="+57 301 381 0242", telw="573013810242", locale="es-CO", cc="CO", region="Santander", pais="Colombia",
    gsc=["Bn9udg0R2-tB4qWIHDJth3iYw_pKtm8zwVX9vb_cFB0"],
    ext_lg=("Página del fabricante: LG Colombia", "https://www.lg.com/co/"), ext_samsung=("Página del fabricante: Samsung Colombia", "https://www.samsung.com/co/"),
    guia_humedad=("humedad-y-lluvias-en-equipos", "Humedad y lluvias en equipos {N} en Bucaramanga", "Cómo la humedad, las lluvias y las tormentas eléctricas de Bucaramanga afectan tus equipos {N}: qué fallas provocan y cómo prevenirlas."),
    intro_clima="Bucaramanga tiene un clima templado, con dos temporadas de lluvias al año y tormentas eléctricas que traen picos de voltaje.",
    costero=False, nev=("neveras", "nevera", "neveras"),
    zonas=ZONAS_BGA, zx=ZX_BGA, clima=CLIMA_BGA,
    area=["Bucaramanga", "Floridablanca", "Girón", "Piedecuesta"], geo=(7.1254, -73.1198), geo_region="CO-SAN",
    zlista="Cabecera y Sotomayor, el centro, el norte, Provenza y Real de Minas, y también en Floridablanca, Girón y Piedecuesta",
    sin_recorte=True, lbl_guias="Blog de consejos", seo_plus=True, sin_tropico=True, esencial=True,
    zart={"cabecera-y-sotomayor": "Cabecera y Sotomayor", "centro-de-bucaramanga": "el centro de Bucaramanga", "norte-de-bucaramanga": "el norte de Bucaramanga", "provenza-y-real-de-minas": "Provenza y Real de Minas", "floridablanca": "Floridablanca", "giron": "Girón", "piedecuesta": "Piedecuesta"},
)

# ----------------------------------------------------------------------------- CHILE (Santiago, todas las comunas)
from cst_chile_datos import ZONAS_CL, ZX_CL, CLIMA_CL, DESTACADAS as DEST_CL, SECTORES_CL, SECTOR_DE, COMUNAS_EQ
_TEL_CL = os.environ.get("CST_TEL", "+56 9 8317 6106")
CHILE = dict(
    sitio="chile", dom="https://serviciotecnicoautorizadochile.cl", ciudad="Santiago", nombre="Servicio Técnico Santiago",
    tel=_TEL_CL, telw=re.sub(r"\D", "", _TEL_CL), locale="es-CL", cc="CL", region="Región Metropolitana", pais="Chile",
    gsc=[x for x in os.environ.get("CST_GSC", "").split(",") if x],
    ext_lg=("Página del fabricante: LG Chile", "https://www.lg.com/cl/"), ext_samsung=("Página del fabricante: Samsung Chile", "https://www.samsung.com/cl/"),
    guia_humedad=("polvo-calor-y-frio-en-equipos", "Polvo, calor y frío en equipos {N} en Santiago", "Cómo el polvo, los veranos calurosos y los inviernos fríos de Santiago afectan tus equipos {N}: qué fallas provocan y cómo prevenirlas."),
    clima_art=dict(h2="Qué hacen el polvo y los cambios de temperatura en tus equipos ", etq="el polvo y el calor",
                   texto="El polvo en suspensión tapa filtros, condensadores y rejillas; el calor del verano exige más a compresores y motores; y el frío del invierno endurece empaques y mangueras."),
    volt_art=dict(h2="Por qué importa el voltaje en equipos ", titulo="Cortes de luz y voltaje: protege tus equipos {N}", desc="Qué equipos {N} sufren más con los cortes de luz y las variaciones de voltaje en Santiago y cómo proteger sus placas y compresores.",
                  texto="Los temporales de invierno y los cortes de suministro pueden generar variaciones y picos de voltaje al volver la luz. En equipos {N}, los más sensibles son {eq}, porque dependen de placas y sensores electrónicos."),
    aire_art=dict(slug="aire-acondicionado-{m}-verano", titulo="Aire acondicionado {N} en verano: qué revisar", desc="Qué revisar en tu aire acondicionado {N} antes y durante el verano caluroso de Santiago."),
    intro_clima="Santiago tiene clima mediterráneo: veranos secos y calurosos, inviernos fríos con lluvias, polvo en suspensión y cortes de luz durante los temporales.",
    clima_extra="Los temporales de invierno pueden provocar cortes de luz y variaciones de voltaje al volver el suministro, que dañan placas electrónicas. Un protector de voltaje adecuado y desconectar los equipos más sensibles durante temporales fuertes reduce ese riesgo. El polvo en suspensión tapa filtros y condensadores, y los veranos secos y calurosos exigen más a refrigeradores y aires acondicionados.",
    clima_txt=("polvo y cambios de temperatura", "Polvo y cambios de temperatura"), guias_clima="el polvo, el calor del verano, el frío del invierno y los cortes de luz con sus picos de voltaje",
    ley_datos="Ley N° 19.628 sobre protección de la vida privada de Chile", ley_consumo="Ley N° 19.496 sobre protección de los derechos de los consumidores de Chile",
    costero=False, nev=("refrigeradores", "refrigerador", "refrigeradores"),
    zonas=ZONAS_CL, zx=ZX_CL, clima=CLIMA_CL, zonas_destacadas=DEST_CL, sectores=SECTORES_CL, sector_de=SECTOR_DE, comunas_eq=COMUNAS_EQ,
    area=[ZONAS_CL[z][0] for z in DEST_CL], geo=(-33.4489, -70.6693), geo_region="CL-RM",
    zlista="Las Condes, Providencia, Ñuñoa, Santiago Centro, Maipú, La Florida, Puente Alto, Vitacura y el resto de las comunas del Gran Santiago",
    sin_recorte=True, lbl_guias="Blog de consejos", seo_plus=True, sin_tropico=True, esencial=True, busquedas=True, marcas_extra=True, sin_toc=True, pro_layout=True,
)
CFG = {"chile": CHILE, "cali": CALI, "guayaquil": GUAYAQUIL, "quito": QUITO, "costarica": COSTARICA, "bucaramanga": BUCARAMANGA}.get(SITIO, PANAMA)

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
_ART_S = {"la": "el", "La": "El", "una": "un", "Una": "Un", "esta": "este", "Esta": "Este", "esa": "ese", "Esa": "Ese", "otra": "otro", "Otra": "Otro", "toda": "todo", "Toda": "Todo", "alguna": "algún", "Alguna": "Algún", "ninguna": "ningún", "Ninguna": "Ningún"}
_ART_P = {"las": "los", "Las": "Los", "unas": "unos", "Unas": "Unos", "estas": "estos", "Estas": "Estos", "esas": "esos", "Esas": "Esos", "otras": "otros", "Otras": "Otros", "todas": "todos", "Todas": "Todos"}
_ADJ = {"nueva": "nuevo", "vieja": "viejo", "antigua": "antiguo", "descompuesta": "descompuesto", "dañada": "dañado", "sucia": "sucio", "llena": "lleno", "vacía": "vacío", "apagada": "apagado", "tapada": "tapado", "congelada": "congelado", "misma": "mismo", "sola": "solo", "propia": "propio", "completa": "completo", "pequeña": "pequeño", "grande": "grande", "conectada": "conectado", "desconectada": "desconectado", "enchufada": "enchufado", "desenchufada": "desenchufado", "bloqueada": "bloqueado", "afectada": "afectado", "instalada": "instalado", "nivelada": "nivelado", "limpia": "limpio", "cerrada": "cerrado", "abierta": "abierto", "lista": "listo", "encendida": "encendido", "usada": "usado", "reparada": "reparado", "revisada": "revisado", "sellada": "sellado"}
def _refri(t):
    """Chile: «refrigerador» (masculino) en lugar de «refrigeradora» o «nevera»; ajusta artículos y adjetivos cercanos."""
    if t in ("neveras", "nevera"): return t   # claves internas de equipo
    t = re.sub(r"\b([Nn])evera(s?)\b", lambda m: ("R" if m.group(1) == "N" else "r") + "efrigeradora" + m.group(2), t)
    t = re.sub(r"\b(de|a)\s+la\s+refrigeradora", lambda m: ("del" if m.group(1) == "de" else "al") + " refrigerador", t)
    t = re.sub(r"\b(De|A)\s+la\s+refrigeradora", lambda m: ("Del" if m.group(1) == "De" else "Al") + " refrigerador", t)
    t = re.sub(r"\b(las|unas|esas|estas|otras|todas|Las|Unas|Esas|Estas|Otras|Todas)(\s+(?:mismas|demás|propias))?\s+refrigeradoras\b", lambda m: _ART_P[m.group(1)] + ((" " + {"mismas": "mismos", "demás": "demás", "propias": "propios"}[m.group(2).strip()]) if m.group(2) else "") + " refrigeradores", t)
    t = re.sub(r"\b(la|una|esta|esa|otra|toda|alguna|ninguna|La|Una|Esta|Esa|Otra|Toda|Alguna|Ninguna)(\s+(?:misma|nueva|vieja|antigua|propia|sola))?\s+refrigeradora\b", lambda m: _ART_S[m.group(1)] + ((" " + _ADJ[m.group(2).strip()]) if m.group(2) else "") + " refrigerador", t)
    t = re.sub(r"\b([Rr])efrigeradora(s?)\b", lambda m: m.group(1) + "efrigerador" + ("es" if m.group(2) else ""), t)
    def _adj(m):
        pl = m.group(1).endswith("es"); base = _ADJ[m.group(3)]; ps = m.group(4) == "s"
        if base == "grande": return m.group(0) if not (pl or ps) else m.group(1) + m.group(2) + "grandes"
        out = base if not (pl or ps) else (base + "s" if base[-1] in "oa" else base + "es")
        return m.group(1) + m.group(2) + out
    t = re.sub(r"\b([Rr]efrigerador(?:es)?)(\s+)(" + "|".join(sorted(_ADJ, key=len, reverse=True)) + r")(s?)\b", _adj, t)
    return t
def _vocab(t):
    if CFG["nev"][1] == "refrigerador": return _refri(t)
    t = re.sub(r"\b([Rr])efrigeradora(s?)\b", lambda m: ("N" if m.group(1) == "R" else "n") + "evera" + m.group(2), t)
    return t
def _sentencias_sin_ciudad(t):
    ps = re.split(r"(?<=[.])\s+", t.strip())
    return " ".join(p for p in ps if "Panamá" not in p)
def _loc_str(t, clave=None):
    for a, b in REEMP_CALI: t = t.replace(a, b)
    if clave == "origen": t = _sentencias_sin_ciudad(t)
    _cl = (CFG["clima_txt"][0] if CFG.get("clima_txt") else "humedad y lluvias") if (CFG.get("frio") or CFG.get("sin_tropico")) else "humedad y calor"
    t = t.replace("humedad y salitre", _cl).replace("la humedad y el salitre", "la " + _cl)
    if CFG.get("frio") or CFG.get("sin_tropico"): t = t.replace("en el trópico", "en la ciudad")
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
    _tvp = CFG.get("tv") or (CFG.get("mix") and re.search(r'rel="canonical" href="[^"]*/(sony/|[^"/]*pantalla[^"/]*/|pantallas-[^"/]*/|[^"/]*-de-pantallas/)', h))
    if CFG.get("tv") or CFG.get("mix"):
        h = re.sub(r"(?<=[ >«(])(led|qled|oled)\b", lambda m_: m_.group(1).upper(), h, flags=re.I)
        h = h.replace("mini LED", "Mini LED").replace("Mini led", "Mini LED")
    if _tvp:
        for x, y in [("filtros, bombas, sensores y empaques", "fuentes de poder, tiras de LED, puertos y cables"), ("Las placas y los compresores", "Los paneles y las placas"), ("las placas y los compresores", "los paneles y las placas"),
                     ("placas y compresores", "placas y paneles"), ("en los equipos con compresor o placa electrónica", "en las pantallas"), ("en equipos con compresor o placa electrónica", "en las pantallas"), ("compresores", "paneles")]:
            h = h.replace(x, y)
    if CFG["nev"][1] == "refrigerador": h = _refri(h)
    elif CFG["nev"][1] != "refrigeradora":
        h = re.sub(r"\b([Rr])efrigeradora(s?)\b", lambda m: ("N" if m.group(1) == "R" else "n") + "evera" + m.group(2), h)
    _cl = (CFG.get("clima_txt") or ("humedad y lluvias", "Humedad y lluvias")) if (CFG.get("frio") or CFG.get("sin_tropico")) else ("humedad y calor", "Humedad y calor")
    h = h.replace("humedad y salitre", _cl[0]).replace("Humedad y salitre", _cl[1])
    if CFG.get("pro_layout"):   # «Servicio técnico {marca} en Santiago» en lugar de «Centro de Servicio Técnico»
        h = re.sub(r"Centro de Servicio Técnico ([^<>|›\"]+?) %s" % CFG["ciudad"], r"Servicio Técnico \1 en %s" % CFG["ciudad"], h)
        h = re.sub(r"Centro de servicio técnico ([^<>|›\"]+?) en %s" % CFG["ciudad"], r"Servicio técnico \1 en %s" % CFG["ciudad"], h)
        h = h.replace("Centro de Servicio Técnico", "Servicio Técnico").replace(" | Centro de Servicio", " | Servicio técnico")
    h = re.sub(r"(%s) \| %s\b" % (CFG["ciudad"], CFG["ciudad"]), r"\1", h)
    return re.sub(r"\x00(\d+)\x00", lambda m: _rutas[int(m.group(1))], h)
