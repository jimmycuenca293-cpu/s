# -*- coding: utf-8 -*-
"""Datos locales de San Salvador: 13 municipios del Área Metropolitana (más Santo Tomás y Panchimalco) y colonias conocidas de la capital.
Solo se describen rasgos generales y sectores conocidos; donde no hay un dato seguro se nombra solo el centro del municipio o la colonia."""

_S_URB = "el calor y la humedad durante casi todo el año, la temporada de lluvias de mayo a octubre y los picos de voltaje de las tormentas eléctricas"
_S_ALTA = "el uso intensivo del aire acondicionado, las tormentas eléctricas de la temporada de lluvias y los picos de voltaje al volver la luz"
_S_NORTE = "el calor y el polvo de la zona norte, las tormentas eléctricas de la temporada de lluvias y las variaciones de voltaje en redes más largas"
_S_ORI = "el calor, la humedad y las tormentas eléctricas de la temporada de lluvias, con muchas viviendas pequeñas y equipos de uso diario intenso"
_S_RUR = "las variaciones de voltaje en redes más largas, el polvo de los caminos y las tormentas eléctricas de la temporada de lluvias"

# slug: (nombre, sectores, rasgo, vivienda, acceso, sectores_visita, clima)
_D = [
 ("centro-historico", "Centro Histórico", "Plaza Barrios, Catedral Metropolitana, Palacio Nacional", "Edificios antiguos, casas y mucho comercio en el centro de la capital.",
  "edificios antiguos y comercio", "el tráfico, las calles angostas y el poco parqueo del centro", "el Centro Histórico y los alrededores de la Plaza Barrios", _S_URB),
 ("san-jacinto", "San Jacinto", "San Jacinto y sus colonias", "Casas y colonias populosas al sur del centro, con equipos de uso familiar.",
  "casas y colonias populosas", "el tráfico y las calles con pendiente", "San Jacinto y las colonias del sur del centro", _S_URB),
 ("colonia-centroamerica", "Colonia Centroamérica", "Colonia Centroamérica y alrededores", "Casas y edificios de clase media cerca del centro.",
  "casas y edificios de clase media", "el tráfico de las avenidas principales", "la Colonia Centroamérica y sus alrededores", _S_URB),
 ("layco", "Colonia Layco", "Colonia Layco", "Casas y apartamentos de clase media al norte del centro.",
  "casas y apartamentos de clase media", "las calles con pendiente y el tráfico del sector", "la Colonia Layco", _S_URB),
 ("miralvalle", "Miralvalle", "Colonia Miralvalle", "Casas y apartamentos al poniente del centro.",
  "casas y apartamentos", "el tráfico y las calles con pendiente", "la Colonia Miralvalle", _S_URB),
 ("flor-blanca", "Flor Blanca", "Colonia Flor Blanca", "Casas y edificios de clase media y media alta, cerca del Estadio Cuscatlán.",
  "casas y edificios de clase media y media alta", "el tráfico de la Alameda Roosevelt y el parqueo limitado", "la Colonia Flor Blanca", _S_ALTA),
 ("escalon", "Colonia Escalón", "Paseo General Escalón, Zona Rosa, Colonia Escalón", "Edificios altos, torres de apartamentos y casas de gama media y alta, con equipos de última generación.",
  "edificios altos, torres de apartamentos y casas de gama alta", "las garitas y los parqueos de visitas de los edificios", "el Paseo General Escalón, la Zona Rosa y la Colonia Escalón", _S_ALTA),
 ("san-benito", "San Benito", "Colonia San Benito, Zona Rosa", "Edificios de apartamentos, hoteles y casas de gama alta cerca de la Zona Rosa.",
  "edificios de apartamentos y casas de gama alta", "las garitas y los controles de acceso de los edificios", "la Colonia San Benito y la Zona Rosa", _S_ALTA),
 ("colonia-medica", "Colonia Médica", "Colonia Médica y hospitales cercanos", "Casas y consultorios en una zona residencial y médica de clase media alta.",
  "casas y apartamentos de clase media alta", "el tráfico del Paseo General Escalón y los parqueos limitados", "la Colonia Médica", _S_ALTA),
 ("miramonte", "Miramonte", "Colonia Miramonte", "Casas y apartamentos de clase media alta al poniente de la capital.",
  "casas y apartamentos de clase media alta", "el tráfico y las calles con pendiente", "la Colonia Miramonte", _S_ALTA),
 ("maquilishuat", "Maquilishuat", "Colonia Maquilishuat", "Casas amplias y residenciales de gama alta al poniente de la capital.",
  "casas amplias y residenciales de gama alta", "los controles de acceso y las calles con pendiente", "la Colonia Maquilishuat", _S_ALTA),
 ("la-mascota", "La Mascota", "Colonia La Mascota", "Casas y apartamentos de clase media alta cerca de la Zona Rosa.",
  "casas y apartamentos de clase media alta", "el tráfico y los accesos controlados de algunas calles", "la Colonia La Mascota", _S_ALTA),
 ("colonia-roma", "Colonia Roma", "Colonia Roma", "Casas y edificios de clase media y media alta en el centro-poniente de la capital.",
  "casas y edificios de clase media y media alta", "el tráfico y el parqueo limitado", "la Colonia Roma", _S_ALTA),
 ("antiguo-cuscatlan", "Antiguo Cuscatlán", "Antiguo Cuscatlán centro, Santa Elena", "Residenciales, apartamentos y zonas empresariales de gama media y alta.",
  "residenciales, apartamentos y zonas empresariales", "los controles de acceso de los residenciales y el tráfico de la Calle El Pedregal", "Antiguo Cuscatlán centro y Santa Elena", _S_ALTA),
 ("santa-elena", "Santa Elena", "Urbanización Santa Elena", "Oficinas, apartamentos y residenciales de gama media y alta.",
  "oficinas, apartamentos y residenciales", "los controles de acceso y el tráfico de la zona empresarial", "la Urbanización Santa Elena", _S_ALTA),
 ("jardines-de-la-hacienda", "Jardines de la Hacienda", "Jardines de la Hacienda", "Residenciales y casas de gama media y alta en Antiguo Cuscatlán.",
  "residenciales y casas de gama media y alta", "los controles de acceso de los residenciales", "Jardines de la Hacienda", _S_ALTA),
 ("santa-tecla", "Santa Tecla", "Santa Tecla centro, Colonia Escalón de Santa Tecla", "Casas y residenciales de clase media y media alta, con un centro histórico propio.",
  "casas y residenciales de clase media y media alta", "el tráfico de la Carretera Panamericana y el parqueo del centro", "Santa Tecla centro y sus colonias", _S_ALTA),
 ("ciudad-merliot", "Ciudad Merliot", "Ciudad Merliot", "Residenciales, apartamentos y comercio entre Santa Tecla y Antiguo Cuscatlán.",
  "residenciales y apartamentos", "los controles de acceso de los residenciales y el tráfico de la zona", "Ciudad Merliot y sus residenciales", _S_ALTA),
 ("san-marcos", "San Marcos", "San Marcos centro", "Casas y colonias populosas al sur de la capital, con equipos de uso familiar.",
  "casas y colonias populosas", "el tráfico de la Carretera al Puerto de La Libertad", "San Marcos centro y sus colonias", _S_URB),
 ("mejicanos", "Mejicanos", "Mejicanos centro, Zacamil", "Colonias populosas y edificios de apartamentos al norte de la capital.",
  "colonias populosas y edificios de apartamentos", "las calles con pendiente y el tráfico hacia el norte", "Mejicanos centro y la Zacamil", _S_NORTE),
 ("zacamil", "Zacamil", "Colonia Zacamil", "Conjuntos de apartamentos y colonias populosas al norte de la capital.",
  "conjuntos de apartamentos y colonias populosas", "las escaleras de los edificios y el tráfico hacia el norte", "la Colonia Zacamil", _S_NORTE),
 ("cuscatancingo", "Cuscatancingo", "Cuscatancingo centro", "Colonias populosas al norte de la capital, con equipos de uso familiar.",
  "colonias populosas", "las calles angostas y el tráfico hacia el norte", "Cuscatancingo centro y sus colonias", _S_NORTE),
 ("ayutuxtepeque", "Ayutuxtepeque", "Ayutuxtepeque centro", "Colonias y residenciales al norte de la capital.",
  "colonias y residenciales", "el tráfico hacia el norte y las calles con pendiente", "Ayutuxtepeque centro y sus colonias", _S_NORTE),
 ("apopa", "Apopa", "Apopa centro", "Colonias y residenciales en uno de los municipios más poblados, al norte de la capital.",
  "colonias y residenciales muy poblados", "la distancia desde el centro y el tráfico de la Troncal del Norte", "Apopa centro y sus colonias", _S_NORTE),
 ("nejapa", "Nejapa", "Nejapa centro", "Casas y residenciales al norponiente, con distancias mayores desde el centro.",
  "casas y residenciales", "la distancia desde el centro y el tráfico de la carretera a Quezaltepeque", "Nejapa centro", _S_RUR),
 ("tonacatepeque", "Tonacatepeque", "Tonacatepeque centro", "Casas y residenciales al nororiente, con distancias mayores desde el centro.",
  "casas y residenciales", "la distancia desde el centro y las carreteras del nororiente", "Tonacatepeque centro", _S_RUR),
 ("soyapango", "Soyapango", "Soyapango centro", "Colonias y residenciales en uno de los municipios más poblados del país, al oriente de la capital.",
  "colonias y residenciales muy poblados", "el tráfico del Bulevar del Ejército y las calles angostas", "Soyapango centro y sus colonias", _S_ORI),
 ("ilopango", "Ilopango", "Ilopango centro", "Colonias y residenciales junto al lago, al oriente de la capital.",
  "colonias y residenciales", "el tráfico del Bulevar del Ejército y la Autopista Oriente", "Ilopango centro y sus colonias", _S_ORI),
 ("san-martin", "San Martín", "San Martín centro", "Colonias y residenciales al oriente, con distancias mayores desde el centro.",
  "colonias y residenciales del oriente", "la distancia desde el centro y la Autopista Oriente", "San Martín centro", _S_ORI),
 ("delgado", "Ciudad Delgado", "Ciudad Delgado centro", "Colonias populosas al nororiente de la capital, con equipos de uso familiar.",
  "colonias populosas", "las calles angostas y el tráfico del sector", "Ciudad Delgado centro y sus colonias", _S_ORI),
 ("santo-tomas", "Santo Tomás", "Santo Tomás centro", "Colonias y residenciales al sur de la capital, con distancias mayores.",
  "colonias y residenciales del sur", "la distancia desde el centro y el tráfico hacia el sur", "Santo Tomás centro", _S_RUR),
 ("panchimalco", "Panchimalco", "Panchimalco centro", "Pueblo y colonias al sur de la capital, con calles con pendiente.",
  "pueblo y colonias del sur", "las calles con pendiente y la distancia desde el centro", "Panchimalco centro", _S_RUR),
]

ZONAS_SV = {s: (n, b, r) for s, n, b, r, *_ in _D}
ZX_SV = {s: (v, a, t) for s, n, b, r, v, a, t, c in _D}
CLIMA_SV = {s: c for s, n, b, r, v, a, t, c in _D}
DESTACADAS = ["escalon", "san-benito", "santa-tecla", "antiguo-cuscatlan", "soyapango", "mejicanos", "colonia-medica", "centro-historico", "apopa", "ilopango", "miramonte", "la-mascota"]
assert len(_D) == 32, len(_D)

SECTORES_SV = {
 "centro-de-san-salvador": ("el centro de San Salvador", "El Centro Histórico, San Jacinto y las colonias Centroamérica, Layco, Miralvalle y Flor Blanca: edificios antiguos y nuevos, casas y comercio, con poco parqueo y mucho tráfico.", ["centro-historico", "san-jacinto", "colonia-centroamerica", "layco", "miralvalle", "flor-blanca"]),
 "escalon-y-zona-rosa-de-san-salvador": ("el Escalón y la Zona Rosa de San Salvador", "La Colonia Escalón, San Benito, la Colonia Médica, Miramonte, Maquilishuat, La Mascota y la Colonia Roma: torres de apartamentos, edificios y casas de gama media y alta, con equipos de uso diario intensivo.", ["escalon", "san-benito", "colonia-medica", "miramonte", "maquilishuat", "la-mascota", "colonia-roma"]),
 "poniente-de-san-salvador": ("el poniente de San Salvador", "Antiguo Cuscatlán, Santa Elena, Jardines de la Hacienda, Santa Tecla, Ciudad Merliot y San Marcos: residenciales, apartamentos y zonas empresariales, con controles de acceso y el tráfico de la Panamericana.", ["antiguo-cuscatlan", "santa-elena", "jardines-de-la-hacienda", "santa-tecla", "ciudad-merliot", "san-marcos"]),
 "norte-de-san-salvador": ("el norte de San Salvador", "Mejicanos, la Zacamil, Cuscatancingo, Ayutuxtepeque, Apopa, Nejapa y Tonacatepeque: colonias populosas, conjuntos de apartamentos y residenciales, con distancias mayores hacia Apopa y Tonacatepeque.", ["mejicanos", "zacamil", "cuscatancingo", "ayutuxtepeque", "apopa", "nejapa", "tonacatepeque"]),
 "oriente-y-sur-de-san-salvador": ("el oriente y el sur de San Salvador", "Soyapango, Ilopango, San Martín, Ciudad Delgado, Santo Tomás y Panchimalco: colonias populosas y residenciales, con el tráfico del Bulevar del Ejército y la Autopista Oriente.", ["soyapango", "ilopango", "san-martin", "delgado", "santo-tomas", "panchimalco"]),
}
assert sorted(z for v in SECTORES_SV.values() for z in v[2]) == sorted(ZONAS_SV), set(ZONAS_SV) ^ {z for v in SECTORES_SV.values() for z in v[2]}
SECTOR_DE = {z: s for s, v in SECTORES_SV.items() for z in v[2]}
COMUNAS_EQ = DESTACADAS + ["flor-blanca", "colonia-centroamerica", "san-marcos", "ciudad-merliot", "cuscatancingo", "delgado", "san-martin", "zacamil"]
