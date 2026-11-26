# -*- coding: utf-8 -*-
"""Datos locales de Ciudad de Guatemala: 22 zonas y 13 municipios del área metropolitana.
Cada zona: (nombre, sectores representativos, rasgo)  /  (vivienda, acceso, sectores de la visita)  /  clima.
Solo se describen rasgos generales y sectores conocidos; donde no hay un dato seguro se nombra solo la zona o el centro del municipio."""

_G_URB = "la temporada de lluvias de mayo a octubre, con tormentas eléctricas y picos de voltaje al volver la luz, y la humedad del invierno"
_G_ALTA = "la temporada de lluvias de mayo a octubre, con tormentas eléctricas fuertes, y el uso diario intensivo de los equipos"
_G_ORI = "la temporada de lluvias de mayo a octubre, con tormentas eléctricas, y las variaciones de voltaje en las redes de las colonias"
_G_SUR = "la humedad y el calor del sur del valle, la ceniza ocasional del volcán de Pacaya y las tormentas eléctricas del invierno"
_G_RUR = "las variaciones de voltaje en redes más largas, el polvo de los caminos y las tormentas eléctricas del invierno"

# slug: (nombre, sectores, rasgo, vivienda, acceso, sectores_visita, clima)
_D = [
 ("zona-1", "Zona 1", "Centro Histórico, Plaza de la Constitución, Catedral Metropolitana", "Edificios antiguos y casas del centro histórico, junto a mucho comercio.",
  "edificios antiguos y comercio", "las calles angostas, el tráfico y el poco estacionamiento del centro", "el Centro Histórico y alrededores de la Plaza de la Constitución", _G_URB),
 ("zona-2", "Zona 2", "Zona 2", "Casas y colonias tradicionales del norte del centro.",
  "casas y colonias tradicionales", "el tráfico de las avenidas principales del centro", "la Zona 2", _G_URB),
 ("zona-3", "Zona 3", "Zona 3", "Casas y edificios de uso mixto cerca del centro.",
  "casas y edificios de uso mixto", "el tráfico y las calles angostas del sector", "la Zona 3", _G_URB),
 ("zona-4", "Zona 4", "Centro Cívico, Cuatro Grados Norte", "Edificios de oficinas, apartamentos nuevos y comercio en pleno centro.",
  "edificios de oficinas y apartamentos nuevos", "las porterías y los estacionamientos de visitas de los edificios", "el Centro Cívico y Cuatro Grados Norte", _G_URB),
 ("zona-5", "Zona 5", "Estadio Doroteo Guamuch Flores y colonias de la Zona 5", "Casas y colonias populosas, con equipos de uso familiar.",
  "casas y colonias populosas", "el tráfico y las calles angostas de algunas colonias", "la Zona 5 y el entorno del Estadio Doroteo Guamuch Flores", _G_URB),
 ("zona-6", "Zona 6", "Zona 6", "Casas y colonias populosas del noreste, con equipos de uso familiar.",
  "casas y colonias populosas", "las calles con pendiente y el tráfico hacia el norte", "la Zona 6", _G_URB),
 ("zona-7", "Zona 7", "Kaminal Juyú, Ciudad de Plata, Colonia Landívar, Quinta Samayoa", "Casas y colonias muy pobladas del poniente, con equipos de uso familiar.",
  "casas y colonias muy pobladas", "el tráfico de la Calzada Roosevelt y las calles con pendiente", "Kaminal Juyú, Ciudad de Plata, Landívar y Quinta Samayoa", _G_URB),
 ("zona-8", "Zona 8", "Zona 8", "Casas y comercio al poniente del centro.",
  "casas y comercio", "el tráfico y los accesos angostos del sector", "la Zona 8", _G_URB),
 ("zona-9", "Zona 9", "Avenida La Reforma, Plaza Obelisco", "Edificios de oficinas y apartamentos, con equipos de gama media y alta.",
  "edificios de oficinas y apartamentos", "las porterías de los edificios y los estacionamientos limitados", "la Avenida La Reforma y alrededores", _G_ALTA),
 ("zona-10", "Zona 10", "Zona Viva, Oakland, Avenida La Reforma", "Torres de apartamentos y edificios de gama alta, con equipos de última generación y mucho uso diario.",
  "torres de apartamentos y edificios de gama alta", "las porterías y los estacionamientos de visitas de las torres", "la Zona Viva, Oakland y la Avenida La Reforma", _G_ALTA),
 ("zona-11", "Zona 11", "Miraflores, Mariscal, Roosevelt", "Casas y colonias de clase media, con equipos de uso familiar.",
  "casas y colonias de clase media", "el tráfico de la Calzada Roosevelt y de Miraflores", "Miraflores, Mariscal y la Calzada Roosevelt", _G_URB),
 ("zona-12", "Zona 12", "Universidad de San Carlos, colonias de la Zona 12", "Casas y colonias populosas, con equipos de uso familiar.",
  "casas y colonias populosas", "el tráfico de la Avenida Petapa y las calles angostas", "el entorno de la Universidad de San Carlos y las colonias de la Zona 12", _G_URB),
 ("zona-13", "Zona 13", "Aeropuerto La Aurora, Colonia Aurora", "Casas y edificios cerca del aeropuerto, con equipos de uso mixto.",
  "casas y edificios cerca del aeropuerto", "el tráfico de la Avenida Hincapié y los accesos controlados", "el Aeropuerto La Aurora y la Colonia Aurora", _G_URB),
 ("zona-14", "Zona 14", "Avenida Las Américas, La Villa y sus torres", "Torres de apartamentos y casas amplias de gama alta, con equipos de línea premium.",
  "torres de apartamentos y casas de gama alta", "las porterías y los controles de acceso de las torres y residenciales", "la Avenida Las Américas y los alrededores de La Villa", _G_ALTA),
 ("zona-15", "Zona 15", "Vista Hermosa, Colinas de Minerva, El Maestro", "Casas y apartamentos de gama media y alta, con equipos de uso diario intensivo.",
  "casas y apartamentos de gama media y alta", "los controles de acceso de las colonias y el tráfico de Vista Hermosa", "Vista Hermosa, Colinas de Minerva y El Maestro", _G_ALTA),
 ("zona-16", "Zona 16", "Cayalá, Paseo Cayalá y residenciales de la Zona 16", "Residenciales cerrados y apartamentos nuevos de gama alta, con equipos de última generación.",
  "residenciales cerrados y apartamentos de gama alta", "los controles de acceso de los residenciales y las distancias hacia el oriente", "Cayalá, Paseo Cayalá y los residenciales de la Zona 16", _G_ALTA),
 ("zona-17", "Zona 17", "Zona 17", "Casas y residenciales del nororiente, con equipos de uso familiar.",
  "casas y residenciales del nororiente", "el tráfico de la Calzada San Juan y la Calzada Atlántico", "la Zona 17", _G_ORI),
 ("zona-18", "Zona 18", "Colonia Atlántida y colonias de la Zona 18", "Casas y colonias muy pobladas, con equipos de uso familiar.",
  "casas y colonias muy pobladas", "la distancia desde el centro y el tráfico de la Calzada Atlántico", "la Colonia Atlántida y las colonias de la Zona 18", _G_ORI),
 ("zona-19", "Zona 19", "Colonia La Florida y colonias de la Zona 19", "Casas y colonias populosas al norte, con equipos de uso familiar.",
  "casas y colonias populosas", "la distancia desde el centro y el tráfico hacia el norte", "la Colonia La Florida y las colonias de la Zona 19", _G_ORI),
 ("zona-21", "Zona 21", "Colonia Justo Rufino Barrios y colonias de la Zona 21", "Casas y colonias populosas al sur, con equipos de uso familiar.",
  "casas y colonias populosas del sur", "la distancia desde el centro y el tráfico de la Calzada Aguilar Batres", "la Colonia Justo Rufino Barrios y las colonias de la Zona 21", _G_SUR),
 ("zona-24", "Zona 24", "Zona 24", "Casas y colonias al nororiente de la ciudad.",
  "casas y colonias del nororiente", "la distancia desde el centro y el tráfico de la Calzada Atlántico", "la Zona 24", _G_ORI),
 ("zona-25", "Zona 25", "Zona 25", "Casas y colonias al norte de la ciudad, con distancias mayores desde el centro.",
  "casas y colonias del norte", "la distancia desde el centro y el tráfico de la Calzada Atlántico", "la Zona 25", _G_ORI),
 ("mixco", "Mixco", "Ciudad San Cristóbal, El Naranjo y el centro de Mixco", "Residenciales, condominios y casas en uno de los municipios más poblados del país, al poniente de la ciudad.",
  "residenciales y condominios muy poblados", "los controles de acceso de los residenciales y el tráfico de la Calzada Roosevelt y la CA-1", "Ciudad San Cristóbal, El Naranjo y el centro de Mixco", _G_URB),
 ("san-juan-sacatepequez", "San Juan Sacatepéquez", "Centro de San Juan Sacatepéquez", "Casas y comercios al norponiente, con distancias mayores desde el centro.",
  "casas y comercios", "la distancia desde la ciudad y las carreteras de montaña", "el centro de San Juan Sacatepéquez", _G_RUR),
 ("san-pedro-sacatepequez", "San Pedro Sacatepéquez", "Centro de San Pedro Sacatepéquez", "Casas y comercios al poniente, con distancias mayores desde el centro.",
  "casas y comercios", "la distancia desde la ciudad y las carreteras de montaña", "el centro de San Pedro Sacatepéquez", _G_RUR),
 ("villa-nueva", "Villa Nueva", "Bárcenas, Ciudad Real y el centro de Villa Nueva", "Residenciales, condominios y casas en uno de los municipios más poblados, al sur de la ciudad.",
  "residenciales y condominios muy poblados", "los controles de acceso de los residenciales y el tráfico de la CA-9 Sur", "Bárcenas, Ciudad Real y el centro de Villa Nueva", _G_SUR),
 ("san-miguel-petapa", "San Miguel Petapa", "Centro de San Miguel Petapa", "Residenciales y casas al sur de la ciudad, con equipos de uso familiar.",
  "residenciales y casas del sur", "el tráfico de la CA-9 Sur y de la Avenida Petapa", "el centro de San Miguel Petapa", _G_SUR),
 ("villa-canales", "Villa Canales", "Boca del Monte y el centro de Villa Canales", "Residenciales y casas al sur, con distancias mayores desde el centro.",
  "residenciales y casas del sur", "la distancia desde la ciudad y el tráfico de la carretera a Villa Canales", "Boca del Monte y el centro de Villa Canales", _G_SUR),
 ("amatitlan", "Amatitlán", "Lago de Amatitlán y el centro de Amatitlán", "Casas y casas de descanso junto al lago, con distancias mayores desde el centro.",
  "casas junto al lago", "la distancia desde la ciudad y el tráfico de la CA-9 Sur", "el Lago de Amatitlán y el centro de Amatitlán", _G_SUR),
 ("santa-catarina-pinula", "Santa Catarina Pinula", "Muxbal y el centro de Santa Catarina Pinula", "Residenciales cerrados y casas de gama media y alta, al oriente de la ciudad.",
  "residenciales cerrados de gama media y alta", "los controles de acceso de los residenciales y el tráfico de la Carretera a El Salvador", "Muxbal y el centro de Santa Catarina Pinula", _G_ALTA),
 ("san-jose-pinula", "San José Pinula", "Centro de San José Pinula", "Residenciales y casas al oriente de la ciudad, con distancias mayores.",
  "residenciales y casas del oriente", "los controles de acceso de los residenciales y la distancia por la Carretera a El Salvador", "el centro de San José Pinula", _G_ORI),
 ("fraijanes", "Fraijanes", "Fraijanes y la Carretera a El Salvador", "Residenciales y casas al oriente de la ciudad, con distancias mayores.",
  "residenciales y casas del oriente", "los controles de acceso de los residenciales y la distancia por la Carretera a El Salvador", "Fraijanes y la Carretera a El Salvador", _G_ORI),
 ("chinautla", "Chinautla", "Centro de Chinautla", "Casas y colonias populosas al norte de la ciudad, con equipos de uso familiar.",
  "casas y colonias populosas", "las calles con pendiente y el tráfico hacia el norte", "el centro de Chinautla", _G_ORI),
 ("san-pedro-ayampuc", "San Pedro Ayampuc", "Centro de San Pedro Ayampuc", "Casas y residenciales al norte, con distancias mayores desde el centro.",
  "casas y residenciales del norte", "la distancia desde la ciudad y las carreteras del norte", "el centro de San Pedro Ayampuc", _G_RUR),
 ("palencia", "Palencia", "Centro de Palencia", "Casas y residenciales al nororiente, con distancias mayores desde el centro.",
  "casas y residenciales del nororiente", "la distancia desde la ciudad y la Carretera al Atlántico", "el centro de Palencia", _G_RUR),
]

ZONAS_GT = {s: (n, b, r) for s, n, b, r, *_ in _D}
ZX_GT = {s: (v, a, t) for s, n, b, r, v, a, t, c in _D}
CLIMA_GT = {s: c for s, n, b, r, v, a, t, c in _D}
DESTACADAS = ["zona-10", "zona-14", "zona-15", "zona-16", "zona-9", "zona-1", "zona-4", "zona-11", "mixco", "villa-nueva", "santa-catarina-pinula", "zona-7"]
assert len(_D) == 35, len(_D)

# Sectores: página de resumen por marca y enlaces entre zonas cercanas.  slug: (nombre en frase, descripción, [zonas])
SECTORES_GT = {
 "centro-de-ciudad-de-guatemala": ("el centro de la Ciudad de Guatemala", "Zonas 1, 2, 3, 4, 5, 6 y 8: el Centro Histórico, el Centro Cívico y colonias populosas, con edificios antiguos y nuevos, comercio y poco estacionamiento.", ["zona-1", "zona-2", "zona-3", "zona-4", "zona-5", "zona-6", "zona-8"]),
 "zona-viva-y-oriente-de-guatemala": ("la Zona Viva y el oriente de la Ciudad de Guatemala", "Zonas 9, 10, 14, 15 y 16, junto a Santa Catarina Pinula, San José Pinula y Fraijanes: torres de apartamentos, residenciales cerrados y casas de gama media y alta, con equipos de uso diario intensivo.", ["zona-9", "zona-10", "zona-14", "zona-15", "zona-16", "santa-catarina-pinula", "san-jose-pinula", "fraijanes"]),
 "occidente-de-ciudad-de-guatemala": ("el occidente de la Ciudad de Guatemala", "Zonas 7 y 11, Mixco, San Juan Sacatepéquez y San Pedro Sacatepéquez: colonias muy pobladas, residenciales y condominios, con el tráfico de la Calzada Roosevelt y la CA-1.", ["zona-7", "zona-11", "mixco", "san-juan-sacatepequez", "san-pedro-sacatepequez"]),
 "sur-de-ciudad-de-guatemala": ("el sur de la Ciudad de Guatemala", "Zonas 12, 13 y 21, Villa Nueva, San Miguel Petapa, Villa Canales y Amatitlán: colonias populosas, residenciales y casas junto al lago, con el tráfico de la CA-9 Sur y la Avenida Petapa.", ["zona-12", "zona-13", "zona-21", "villa-nueva", "san-miguel-petapa", "villa-canales", "amatitlan"]),
 "norte-de-ciudad-de-guatemala": ("el norte de la Ciudad de Guatemala", "Zonas 17, 18, 19, 24 y 25, Chinautla, San Pedro Ayampuc y Palencia: colonias muy pobladas y residenciales, con distancias mayores hacia el norte y la Calzada Atlántico.", ["zona-17", "zona-18", "zona-19", "zona-24", "zona-25", "chinautla", "san-pedro-ayampuc", "palencia"]),
}
assert sorted(z for v in SECTORES_GT.values() for z in v[2]) == sorted(ZONAS_GT), set(ZONAS_GT) ^ {z for v in SECTORES_GT.values() for z in v[2]}
SECTOR_DE = {z: s for s, v in SECTORES_GT.items() for z in v[2]}
# zonas con página de reparación por equipo (las más buscadas)
COMUNAS_EQ = DESTACADAS + ["zona-12", "zona-13", "zona-17", "zona-18", "san-jose-pinula", "fraijanes", "chinautla", "villa-canales"]
