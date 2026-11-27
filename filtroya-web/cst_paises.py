# -*- coding: utf-8 -*-
"""Ciudades del sitio internacional de Frigidaire: Panamá, Costa Rica, Bogotá, Cali, Quito y Guayaquil.
Cada ciudad se describe con una lista de zonas (nombre, sectores conocidos, tipo de vivienda), sectores y clima; el resto del texto sale de plantillas.
Solo se nombran zonas y sectores reconocidos; no se inventan precios, plazos ni horarios."""
import re

# tipo de zona: (vivienda como frase, vivienda corta, acceso a tener en cuenta)
TIPOS = {
    "alta": ("Torres de apartamentos, edificios y casas de gama media y alta, con equipos de última generación y mucho uso diario.", "torres de apartamentos y casas de gama alta", "las porterías y los parqueos de visitas de los edificios"),
    "media": ("Casas y edificios de clase media, con una mezcla de equipos nuevos y de muchos años.", "casas y edificios de clase media", "el tráfico de las avenidas principales y el parqueo limitado"),
    "pop": ("Casas y barrios populosos, con equipos de uso familiar intenso.", "casas y barrios populosos", "las calles angostas y el tráfico del sector"),
    "res": ("Urbanizaciones y conjuntos cerrados de casas y apartamentos, con controles de acceso.", "urbanizaciones y conjuntos cerrados", "los controles de acceso de las urbanizaciones y conjuntos"),
    "ext": ("Casas y urbanizaciones en las afueras, con distancias mayores desde el centro.", "casas y urbanizaciones en las afueras", "la distancia desde el centro y el tráfico de las vías de acceso"),
    "hist": ("Edificios antiguos, casas y mucho comercio en el centro.", "edificios antiguos y comercio", "las calles angostas, el tráfico y el poco parqueo del centro"),
}

# ----------------------------------------------------------------------------------------------------------------------------- datos
# zonas: (slug, nombre, sectores representativos, tipo)   ·   sectores: slug -> (frase, descripción, [zonas])
PANAMA = dict(
    zonas=[("costa-del-este", "Costa del Este", "Costa del Este, Panamá Pacífico Business Park, Santa María", "alta"), ("punta-pacifica", "Punta Pacífica", "Punta Pacífica y sus torres frente a la bahía", "alta"),
           ("punta-paitilla", "Punta Paitilla", "Punta Paitilla y la Avenida Balboa", "alta"), ("san-francisco", "San Francisco", "San Francisco, Calle 50 y Coco del Mar", "alta"),
           ("bella-vista", "Bella Vista", "Bella Vista y la Avenida Balboa", "alta"), ("obarrio", "Obarrio", "Obarrio y la Calle 50", "alta"),
           ("el-cangrejo", "El Cangrejo", "El Cangrejo y la Vía Argentina", "media"), ("marbella", "Marbella", "Marbella y la Calle 50", "alta"),
           ("casco-antiguo", "Casco Antiguo", "Casco Antiguo, San Felipe y la Plaza de la Independencia", "hist"), ("calidonia", "Calidonia", "Calidonia y la Avenida Central", "hist"),
           ("albrook", "Albrook", "Albrook y la zona del aeropuerto", "media"), ("clayton", "Clayton", "Clayton y Ciudad del Saber", "res"), ("ancon", "Ancón", "Ancón y Balboa", "res"),
           ("betania", "Betania", "Betania y Los Ángeles", "media"), ("el-dorado", "El Dorado", "El Dorado y Villa Lucre", "media"), ("condado-del-rey", "Condado del Rey", "Condado del Rey", "media"),
           ("parque-lefevre", "Parque Lefevre", "Parque Lefevre", "media"), ("rio-abajo", "Río Abajo", "Río Abajo", "pop"), ("juan-diaz", "Juan Díaz", "Juan Díaz y Altos de Cerro Viento", "pop"),
           ("pedregal", "Pedregal", "Pedregal", "pop"), ("tocumen", "Tocumen", "Tocumen y el aeropuerto internacional", "pop"), ("pueblo-nuevo", "Pueblo Nuevo", "Pueblo Nuevo", "pop"),
           ("san-miguelito", "San Miguelito", "San Miguelito y Los Andes", "pop"), ("las-cumbres", "Las Cumbres", "Las Cumbres y Chivo Chivo", "ext"), ("chilibre", "Chilibre", "Chilibre", "ext"),
           ("pacora", "Pacora", "Pacora", "ext"), ("arraijan", "Arraiján", "Arraiján y Vista Alegre", "ext"), ("la-chorrera", "La Chorrera", "La Chorrera", "ext"), ("panama-pacifico", "Panamá Pacífico", "Panamá Pacífico y Howard", "res")],
    sectores={"centro-de-ciudad-de-panama": ("el centro de Ciudad de Panamá", "San Francisco, Bella Vista, Obarrio, El Cangrejo, Marbella, el Casco Antiguo y Calidonia: torres de apartamentos, oficinas y edificios antiguos, con porterías y poco parqueo.", ["san-francisco", "bella-vista", "obarrio", "el-cangrejo", "marbella", "casco-antiguo", "calidonia"]),
              "este-de-ciudad-de-panama": ("el este de Ciudad de Panamá", "Costa del Este, Punta Pacífica, Punta Paitilla, Parque Lefevre, Río Abajo, Juan Díaz, Pedregal, Tocumen y Pueblo Nuevo: torres frente a la bahía y barrios populosos hacia el aeropuerto.", ["costa-del-este", "punta-pacifica", "punta-paitilla", "parque-lefevre", "rio-abajo", "juan-diaz", "pedregal", "tocumen", "pueblo-nuevo"]),
              "oeste-de-ciudad-de-panama": ("el oeste de Ciudad de Panamá", "Albrook, Clayton, Ancón, Betania, El Dorado y Condado del Rey: residenciales, edificios y zonas verdes hacia el Canal.", ["albrook", "clayton", "ancon", "betania", "el-dorado", "condado-del-rey"]),
              "norte-de-ciudad-de-panama": ("el norte de Ciudad de Panamá", "San Miguelito, Las Cumbres, Chilibre y Pacora: barrios populosos y urbanizaciones, con distancias mayores hacia el norte.", ["san-miguelito", "las-cumbres", "chilibre", "pacora"]),
              "panama-oeste": ("Panamá Oeste", "Arraiján, La Chorrera y Panamá Pacífico: urbanizaciones y comunidades al otro lado del Puente de las Américas.", ["arraijan", "la-chorrera", "panama-pacifico"])},
)
COSTA_RICA = dict(
    zonas=[("escazu", "Escazú", "Escazú centro, San Rafael y Guachipelín", "alta"), ("santa-ana", "Santa Ana", "Santa Ana centro, Lindora y Pozos", "alta"), ("curridabat", "Curridabat", "Curridabat y Granadilla", "alta"),
           ("sabana", "Sabana", "La Sabana, Sabana Norte y Nunciatura", "alta"), ("rohrmoser", "Rohrmoser", "Rohrmoser", "alta"), ("barrio-escalante", "Barrio Escalante", "Barrio Escalante y Barrio Amón", "alta"),
           ("san-pedro", "San Pedro", "San Pedro y Montes de Oca", "media"), ("moravia", "Moravia", "Moravia y San Vicente", "media"), ("tibas", "Tibás", "Tibás y Llorente", "media"),
           ("goicoechea", "Goicoechea", "Guadalupe y Ciudad Hacienda", "media"), ("coronado", "Coronado", "Coronado y San Antonio", "res"), ("pavas", "Pavas", "Pavas y Rohrmoser Oeste", "pop"),
           ("desamparados", "Desamparados", "Desamparados centro y San Antonio", "pop"), ("alajuelita", "Alajuelita", "Alajuelita centro", "pop"), ("hatillo", "Hatillo", "Hatillo", "pop"),
           ("la-uruca", "La Uruca", "La Uruca", "pop"), ("san-jose-centro", "San José Centro", "Centro de San José, Barrio Otoya y Plaza de la Cultura", "hist"), ("zapote", "Zapote", "Zapote", "media"),
           ("heredia", "Heredia", "Heredia centro, Ulloa y Lagunilla", "media"), ("belen", "Belén", "San Antonio de Belén y La Ribera", "res"), ("alajuela", "Alajuela", "Alajuela centro", "ext"),
           ("cartago", "Cartago", "Cartago centro", "ext"), ("san-rafael-de-heredia", "San Rafael de Heredia", "San Rafael de Heredia", "res"), ("santo-domingo", "Santo Domingo", "Santo Domingo de Heredia", "res"),
           ("los-yoses", "Los Yoses", "Los Yoses y la Rotonda de la Hispanidad", "alta"), ("paseo-colon", "Paseo Colón", "Paseo Colón y Sabana Sur", "alta"), ("tres-rios", "Tres Ríos", "Tres Ríos de Cartago", "res"),
           ("la-union", "La Unión", "La Unión y Concepción", "res"), ("barva", "Barva", "Barva de Heredia", "ext"), ("san-pablo-de-heredia", "San Pablo de Heredia", "San Pablo de Heredia", "res"),
           ("san-antonio-de-escazu", "San Antonio de Escazú", "San Antonio de Escazú", "res"), ("guachipelin", "Guachipelín", "Guachipelín de Escazú", "alta"), ("lindora", "Lindora", "Lindora y Pozos de Santa Ana", "alta"),
           ("piedades-de-santa-ana", "Piedades de Santa Ana", "Piedades de Santa Ana", "res"), ("la-guacima", "La Guácima", "La Guácima de Alajuela", "res"), ("ciudad-colon", "Ciudad Colón", "Ciudad Colón de Mora", "ext"),
           ("san-francisco-de-dos-rios", "San Francisco de Dos Ríos", "San Francisco de Dos Ríos", "media"), ("rio-segundo", "Río Segundo", "Río Segundo de Alajuela", "ext"), ("paraiso", "Paraíso", "Paraíso de Cartago", "ext")],
    sectores={"centro-de-san-jose": ("el centro de San José", "San José Centro, Barrio Escalante, Paseo Colón, Sabana, Rohrmoser, La Uruca, Hatillo y Pavas: oficinas, edificios y barrios tradicionales, con poco parqueo.", ["san-jose-centro", "barrio-escalante", "paseo-colon", "sabana", "rohrmoser", "la-uruca", "hatillo", "pavas"]),
              "oeste-de-san-jose": ("el oeste de San José", "Escazú, Santa Ana, Belén y Ciudad Colón: residenciales de gama alta, condominios y zonas empresariales, con controles de acceso.", ["escazu", "san-antonio-de-escazu", "guachipelin", "santa-ana", "lindora", "piedades-de-santa-ana", "belen", "ciudad-colon"]),
              "este-de-san-jose": ("el este de San José", "Curridabat, San Pedro, Los Yoses, Moravia, Zapote, Goicoechea, Coronado, Tibás, Tres Ríos y La Unión: barrios de clase media, universidades y residenciales.", ["curridabat", "san-pedro", "los-yoses", "moravia", "zapote", "san-francisco-de-dos-rios", "goicoechea", "coronado", "tibas", "tres-rios", "la-union"]),
              "sur-de-san-jose": ("el sur de San José", "Desamparados y Alajuelita: barrios populosos con calles con pendiente.", ["desamparados", "alajuelita"]),
              "gran-area-metropolitana": ("la Gran Área Metropolitana", "Heredia, Barva, San Pablo, Santo Domingo, San Rafael de Heredia, Alajuela, La Guácima, Río Segundo, Cartago y Paraíso: ciudades vecinas con distancias mayores desde San José.", ["heredia", "barva", "san-pablo-de-heredia", "santo-domingo", "san-rafael-de-heredia", "alajuela", "la-guacima", "rio-segundo", "cartago", "paraiso"])},
)
BOGOTA = dict(
    zonas=[("chico", "El Chicó", "El Chicó, Zona T y Parque 93", "alta"), ("usaquen", "Usaquén", "Usaquén centro, Santa Bárbara y Cedritos", "alta"), ("chapinero", "Chapinero", "Chapinero Alto, Rosales y Zona G", "alta"),
           ("cedritos", "Cedritos", "Cedritos y Toberín", "media"), ("suba", "Suba", "Suba centro, Niza y La Colina", "media"), ("teusaquillo", "Teusaquillo", "Teusaquillo, La Soledad y Galerías", "media"),
           ("barrios-unidos", "Barrios Unidos", "Barrios Unidos, 7 de Agosto y Los Alcázares", "media"), ("engativa", "Engativá", "Engativá, Normandía y Bolivia", "pop"), ("fontibon", "Fontibón", "Fontibón y Modelia", "media"),
           ("kennedy", "Kennedy", "Kennedy, Patio Bonito y Castilla", "pop"), ("bosa", "Bosa", "Bosa y Bosa Centro", "pop"), ("puente-aranda", "Puente Aranda", "Puente Aranda y Zona Industrial", "pop"),
           ("santa-fe", "Santa Fe", "Santa Fe, Las Nieves y el Centro Internacional", "hist"), ("la-candelaria", "La Candelaria", "La Candelaria y Plaza de Bolívar", "hist"), ("los-martires", "Los Mártires", "Los Mártires y Paloquemao", "hist"),
           ("antonio-narino", "Antonio Nariño", "Antonio Nariño y Restrepo", "pop"), ("tunjuelito", "Tunjuelito", "Tunjuelito", "pop"), ("ciudad-bolivar", "Ciudad Bolívar", "Ciudad Bolívar", "pop"),
           ("san-cristobal", "San Cristóbal", "San Cristóbal y 20 de Julio", "pop"), ("rafael-uribe-uribe", "Rafael Uribe Uribe", "Rafael Uribe Uribe", "pop"), ("usme", "Usme", "Usme", "ext"),
           ("soacha", "Soacha", "Soacha centro y Ciudad Verde", "ext"), ("chia", "Chía", "Chía y Fonquetá", "res"), ("cajica", "Cajicá", "Cajicá", "res"), ("mosquera", "Mosquera", "Mosquera y Funza", "ext"), ("la-calera", "La Calera", "La Calera", "res")],
    sectores={"norte-de-bogota": ("el norte de Bogotá", "El Chicó, Usaquén, Cedritos y Suba: apartamentos, conjuntos cerrados y casas de gama media y alta, con portería y parqueaderos de visitantes.", ["chico", "usaquen", "cedritos", "suba"]),
              "centro-y-chapinero": ("el centro y Chapinero de Bogotá", "Chapinero, Teusaquillo, Barrios Unidos, Santa Fe, La Candelaria y Los Mártires: edificios antiguos y nuevos, oficinas y comercio, con poco parqueo.", ["chapinero", "teusaquillo", "barrios-unidos", "santa-fe", "la-candelaria", "los-martires"]),
              "occidente-de-bogota": ("el occidente de Bogotá", "Engativá, Fontibón, Kennedy, Bosa y Puente Aranda: barrios populosos, conjuntos residenciales y zona industrial, con el tráfico de la Avenida Boyacá y la calle 80.", ["engativa", "fontibon", "kennedy", "bosa", "puente-aranda"]),
              "sur-de-bogota": ("el sur de Bogotá", "Antonio Nariño, Tunjuelito, Ciudad Bolívar, San Cristóbal, Rafael Uribe Uribe y Usme: barrios populosos con calles con pendiente y distancias mayores.", ["antonio-narino", "tunjuelito", "ciudad-bolivar", "san-cristobal", "rafael-uribe-uribe", "usme"]),
              "sabana-de-bogota": ("la Sabana de Bogotá", "Soacha, Chía, Cajicá, Mosquera y La Calera: municipios vecinos con conjuntos cerrados y distancias mayores desde la ciudad.", ["soacha", "chia", "cajica", "mosquera", "la-calera"])},
)
CALI = dict(
    zonas=[("ciudad-jardin", "Ciudad Jardín", "Ciudad Jardín y Pance", "alta"), ("pance", "Pance", "Pance y la vía a Jamundí", "res"), ("granada", "Granada", "Granada, Avenida Sexta y Juanambú", "alta"),
           ("versalles", "Versalles", "Versalles y Santa Mónica", "alta"), ("santa-monica", "Santa Mónica", "Santa Mónica y Normandía", "alta"), ("san-fernando", "San Fernando", "San Fernando y Tequendama", "media"),
           ("tequendama", "Tequendama", "Tequendama y Limonar", "media"), ("el-ingenio", "El Ingenio", "El Ingenio y Ciudad Jardín Sur", "res"), ("valle-del-lili", "Valle del Lili", "Valle del Lili y Cañasgordas", "res"),
           ("cañasgordas", "Cañasgordas", "Cañasgordas", "res"), ("limonar", "Limonar", "Limonar", "media"), ("centro-de-cali", "Centro de Cali", "Centro, San Antonio y la Plaza de Caycedo", "hist"),
           ("san-antonio", "San Antonio", "San Antonio", "hist"), ("chipichape", "Chipichape", "Chipichape y Normandía", "media"), ("menga", "Menga", "Menga y La Flora", "media"),
           ("la-flora", "La Flora", "La Flora", "media"), ("alfonso-lopez", "Alfonso López", "Alfonso López", "pop"), ("aguablanca", "Distrito de Aguablanca", "El Retiro, Mojica y Potrero Grande", "pop"),
           ("siloe", "Siloé", "Siloé", "pop"), ("melendez", "Meléndez", "Meléndez y Caney", "media"), ("caney", "Caney", "Caney", "media"), ("ciudad-2000", "Ciudad 2000", "Ciudad 2000", "res"),
           ("jamundi", "Jamundí", "Jamundí centro y Alfaguara", "ext"), ("yumbo", "Yumbo", "Yumbo y zona industrial", "ext"), ("palmira", "Palmira", "Palmira centro", "ext")],
    sectores={"sur-de-cali": ("el sur de Cali", "Ciudad Jardín, Pance, El Ingenio, Valle del Lili, Cañasgordas y Ciudad 2000: conjuntos cerrados, condominios y casas de gama media y alta, con portería y controles de acceso.", ["ciudad-jardin", "pance", "el-ingenio", "valle-del-lili", "cañasgordas", "ciudad-2000"]),
              "oeste-de-cali": ("el oeste de Cali", "Granada, Versalles, Santa Mónica, San Fernando, Tequendama y Limonar: apartamentos y casas de clase media y alta con equipos de uso diario intenso.", ["granada", "versalles", "santa-monica", "san-fernando", "tequendama", "limonar"]),
              "centro-y-norte-de-cali": ("el centro y el norte de Cali", "Centro, San Antonio, Chipichape, Menga y La Flora: comercio, oficinas y barrios tradicionales, con poco parqueo.", ["centro-de-cali", "san-antonio", "chipichape", "menga", "la-flora"]),
              "oriente-y-ladera-de-cali": ("el oriente y la ladera de Cali", "Alfonso López, Distrito de Aguablanca, Siloé, Meléndez y Caney: barrios populosos y laderas con calles con pendiente.", ["alfonso-lopez", "aguablanca", "siloe", "melendez", "caney"]),
              "area-metropolitana-de-cali": ("el área metropolitana de Cali", "Jamundí, Yumbo y Palmira: municipios vecinos con conjuntos cerrados y zonas industriales, con distancias mayores desde la ciudad.", ["jamundi", "yumbo", "palmira"])},
)
QUITO = dict(
    zonas=[("la-carolina", "La Carolina", "La Carolina, Avenida de los Shyris y el Parque La Carolina", "alta"), ("inaquito", "Iñaquito", "Iñaquito y la Avenida Amazonas", "alta"), ("gonzalez-suarez", "González Suárez", "González Suárez y Bellavista", "alta"),
           ("la-floresta", "La Floresta", "La Floresta y Guápulo", "alta"), ("quito-tenis", "Quito Tenis", "Quito Tenis y El Batán", "alta"), ("el-condado", "El Condado", "El Condado y Ponceano", "media"),
           ("cumbaya", "Cumbayá", "Cumbayá y Lumbisí", "res"), ("tumbaco", "Tumbaco", "Tumbaco y Puembo", "res"), ("la-mariscal", "La Mariscal", "La Mariscal y Plaza Foch", "media"),
           ("centro-historico", "Centro Histórico", "Centro Histórico, La Ronda y la Plaza Grande", "hist"), ("la-magdalena", "La Magdalena", "La Magdalena y Chimbacalle", "pop"), ("chillogallo", "Chillogallo", "Chillogallo y La Ecuatoriana", "pop"),
           ("quitumbe", "Quitumbe", "Quitumbe y Solanda", "pop"), ("guamani", "Guamaní", "Guamaní", "pop"), ("calderon", "Calderón", "Calderón y Carapungo", "pop"), ("cotocollao", "Cotocollao", "Cotocollao y Ponciano", "media"),
           ("el-batan", "El Batán", "El Batán", "media"), ("la-armenia", "La Armenia", "La Armenia y San Rafael", "res"), ("conocoto", "Conocoto", "Conocoto", "res"), ("sangolqui", "Sangolquí", "Sangolquí y el Valle de los Chillos", "res"),
           ("pomasqui", "Pomasqui", "Pomasqui y San Antonio de Pichincha", "ext"), ("nayon", "Nayón", "Nayón y Zámbiza", "res"), ("tababela", "Tababela", "Tababela y Yaruquí", "ext"), ("la-gasca", "La Gasca", "La Gasca y La Vicentina", "media")],
    sectores={"norte-de-quito": ("el norte de Quito", "La Carolina, Iñaquito, González Suárez, Quito Tenis, El Condado, Cotocollao, El Batán y La Floresta: edificios, conjuntos y casas de gama media y alta, con portería y parqueaderos de visita.", ["la-carolina", "inaquito", "gonzalez-suarez", "la-floresta", "quito-tenis", "el-condado", "cotocollao", "el-batan", "la-gasca"]),
              "centro-de-quito": ("el centro de Quito", "El Centro Histórico, La Mariscal y La Magdalena: edificios antiguos, casas y comercio, con calles angostas y poco parqueo.", ["centro-historico", "la-mariscal", "la-magdalena"]),
              "sur-de-quito": ("el sur de Quito", "Chillogallo, Quitumbe y Guamaní: barrios populosos al sur, con distancias mayores y calles con pendiente.", ["chillogallo", "quitumbe", "guamani"]),
              "valles-de-quito": ("los valles de Quito", "Cumbayá, Tumbaco, Nayón, Conocoto, Sangolquí y La Armenia: conjuntos cerrados y casas en los valles, con controles de acceso.", ["cumbaya", "tumbaco", "nayon", "conocoto", "sangolqui", "la-armenia", "tababela"]),
              "norte-lejano-de-quito": ("el extremo norte de Quito", "Calderón y Pomasqui: barrios populosos y conjuntos con distancias mayores hacia el norte.", ["calderon", "pomasqui"])},
)
GUAYAQUIL = dict(
    zonas=[("urdesa", "Urdesa", "Urdesa Central, Urdesa Norte y la Víctor Emilio Estrada", "alta"), ("kennedy", "Kennedy", "Kennedy Norte y la Avenida Francisco de Orellana", "alta"), ("ceibos", "Los Ceibos", "Los Ceibos y Colinas de los Ceibos", "res"),
           ("la-garzota", "La Garzota", "La Garzota", "media"), ("alborada", "Alborada", "Alborada y Guayacanes", "media"), ("sauces", "Sauces", "Sauces y la Avenida Rodolfo Baquerizo", "media"),
           ("samborondon", "Samborondón", "La Puntilla, Entre Ríos y Ciudad Celeste", "res"), ("la-puntilla", "La Puntilla", "La Puntilla", "res"), ("via-a-la-costa", "Vía a la Costa", "Vía a la Costa y Puerto Azul", "res"),
           ("centenario", "Centenario", "Centenario y El Centro", "hist"), ("centro-de-guayaquil", "Centro de Guayaquil", "Centro, Malecón 2000 y Las Peñas", "hist"), ("ciudadela-atarazana", "Atarazana", "Ciudadela Atarazana", "media"),
           ("miraflores", "Miraflores", "Miraflores", "media"), ("mapasingue", "Mapasingue", "Mapasingue", "pop"), ("bastion-popular", "Bastión Popular", "Bastión Popular", "pop"), ("pascuales", "Pascuales", "Pascuales", "pop"),
           ("guasmo", "Guasmo", "Guasmo Norte y Guasmo Sur", "pop"), ("isla-trinitaria", "Isla Trinitaria", "Isla Trinitaria", "pop"), ("el-fortin", "El Fortín", "El Fortín", "pop"),
           ("duran", "Durán", "Durán centro", "ext"), ("daule", "Daule", "Daule y La Aurora", "res"), ("milagro", "Milagro", "Milagro", "ext"), ("la-aurora", "La Aurora", "La Aurora", "res"), ("urbanor", "Urbanor", "Urbanor y Mucho Lote", "pop")],
    sectores={"norte-de-guayaquil": ("el norte de Guayaquil", "Urdesa, Kennedy, La Garzota, Alborada, Sauces, Urbanor y Mapasingue: ciudadelas, edificios y casas de clase media y alta, con aire acondicionado de uso casi permanente.", ["urdesa", "kennedy", "la-garzota", "alborada", "sauces", "urbanor", "mapasingue"]),
              "via-a-la-costa-y-ceibos": ("la Vía a la Costa y Los Ceibos", "Los Ceibos y la Vía a la Costa: urbanizaciones cerradas y casas de gama alta, con controles de acceso y distancias mayores.", ["ceibos", "via-a-la-costa"]),
              "samborondon-y-daule": ("Samborondón y Daule", "La Puntilla, Samborondón, Daule y La Aurora: urbanizaciones cerradas al otro lado del puente, con controles de acceso.", ["samborondon", "la-puntilla", "daule", "la-aurora"]),
              "centro-y-sur-de-guayaquil": ("el centro y el sur de Guayaquil", "Centro, Centenario, Atarazana, Miraflores, Guasmo, Isla Trinitaria y El Fortín: comercio, edificios antiguos y barrios populosos.", ["centro-de-guayaquil", "centenario", "ciudadela-atarazana", "miraflores", "guasmo", "isla-trinitaria", "el-fortin"]),
              "oeste-y-periferia-de-guayaquil": ("la periferia de Guayaquil", "Bastión Popular, Pascuales, Durán y Milagro: barrios populosos y ciudades vecinas con distancias mayores desde el centro.", ["bastion-popular", "pascuales", "duran", "milagro"])},
)
# --------------------------------------------------------------------------------------------------------------------------- ciudades
# clima: (calor/humedad texto largo, urb, alta, ext)
C = {
 "panama": dict(DATOS=PANAMA, ciudad="Panamá", ciudad_corta="Panamá", slug="panama", cc="PA", locale="es-PA", region="Panamá", pais="Panamá", geo=(8.9824, -79.5199), geo_region="PA-8",
                nev="refrigeradora", gas="gas propano en cilindro", cond="PH y edificios", marcas_sector="Costa del Este, San Francisco, Bella Vista, Obarrio, Albrook, San Miguelito, Arraiján y La Chorrera",
                intro_clima="Ciudad de Panamá tiene un clima tropical, caluroso y húmedo todo el año, con una temporada seca de enero a abril (el verano) y una temporada de lluvias de mayo a diciembre (el invierno), con tormentas eléctricas y picos de voltaje.",
                verano="El verano, la temporada seca de enero a abril, trae el calor más fuerte, y los equipos de frío y los aires acondicionados trabajan más.", invierno="En invierno, la temporada de lluvias de mayo a diciembre, hay tormentas eléctricas, apagones y variaciones de voltaje al volver la luz, y se usa más la secadora.",
                calor="el calor y la humedad durante todo el año", lluvia="la temporada de lluvias de mayo a diciembre", volt="120 V", volt2="240 V", ley_datos="Ley 81 de 2019 sobre protección de datos personales", ley_consumo="Ley 45 de 2007 sobre protección al consumidor", bomberos="Bomberos (103)",
                ext=[("Autoridad de Protección al Consumidor y Defensa de la Competencia (ACODECO)", "https://www.acodeco.gob.pa/", "Tus derechos como consumidor y cómo presentar un reclamo."), ("Autoridad Nacional de los Servicios Públicos (ASEP)", "https://www.asep.gob.pa/", "Información sobre el servicio eléctrico, voltaje y calidad de la energía.")],
                ext_lg="https://www.lg.com/pa/", vocab=[(r"\bcomunas\b", "zonas"), (r"\bcomuna\b", "zona"), (r"\bboleta\b", "factura"), (r"\bconserjería\b", "portería"), (r"\bporterías\b", "porterías"), (r"\bdepartamentos\b", "apartamentos"), (r"\bdepartamento\b", "apartamento"), (r"\bparqueos\b", "estacionamientos"), (r"\bparqueo\b", "estacionamiento")]),
 "costarica": dict(DATOS=COSTA_RICA, ciudad="San José", ciudad_corta="San José", slug="costa-rica", cc="CR", locale="es-CR", region="San José", pais="Costa Rica", geo=(9.9281, -84.0907), geo_region="CR-SJ",
                nev="refrigeradora", gas="gas LP en cilindro", cond="condominios", marcas_sector="Escazú, Santa Ana, Curridabat, Sabana, Heredia y Alajuela",
                intro_clima="San José tiene un clima templado de altura, con una temporada seca de diciembre a abril (el verano) y una temporada de lluvias de mayo a noviembre (el invierno), con tormentas eléctricas y picos de voltaje.",
                verano="El verano, la temporada seca de diciembre a abril, trae más polvo y calor en algunos meses, y los equipos de frío trabajan más.", invierno="En invierno, la temporada de lluvias de mayo a noviembre, hay tormentas eléctricas, apagones y variaciones de voltaje al volver la luz, y se usa más la secadora.",
                calor="la humedad y las lluvias casi diarias de mayo a noviembre", lluvia="la temporada de lluvias de mayo a noviembre", volt="120 V", volt2="240 V", ley_datos="Ley 8968 de protección de la persona frente al tratamiento de sus datos personales", ley_consumo="Ley 7472 de promoción de la competencia y defensa efectiva del consumidor", bomberos="Bomberos (118)",
                ext=[("Ministerio de Economía, Industria y Comercio (MEIC): defensa del consumidor", "https://www.meic.go.cr/", "Tus derechos como consumidor y cómo presentar un reclamo."), ("Autoridad Reguladora de los Servicios Públicos (ARESEP)", "https://aresep.go.cr/", "Información sobre el servicio eléctrico y la calidad de la energía."), ("Instituto Costarricense de Electricidad (ICE)", "https://www.grupoice.com/", "Información del servicio eléctrico y recomendaciones ante apagones.")],
                ext_lg="https://www.lg.com/cr/", vocab=[(r"\bcomunas\b", "zonas"), (r"\bcomuna\b", "zona"), (r"\bboleta\b", "factura"), (r"\bconserjería\b", "garita"), (r"\bporterías\b", "garitas"), (r"\bportería\b", "garita"), (r"\bdepartamentos\b", "apartamentos"), (r"\bdepartamento\b", "apartamento"), (r"\bestacionamientos\b", "parqueos"), (r"\bestacionamiento\b", "parqueo"), (r"\bpropano\b", "LP")]),
 "bogota": dict(DATOS=BOGOTA, ciudad="Bogotá", ciudad_corta="Bogotá", slug="colombia/bogota", cc="CO", locale="es-CO", region="Bogotá D.C.", pais="Colombia", geo=(4.7110, -74.0721), geo_region="CO-DC",
                nev="nevera", gas="gas natural domiciliario o gas propano en cilindro (pipeta)", cond="conjuntos residenciales", marcas_sector="El Chicó, Usaquén, Chapinero, Suba, Cedritos, Kennedy y Chía",
                intro_clima="Bogotá tiene un clima frío de altura, con dos temporadas de lluvias al año (de marzo a mayo y de octubre a noviembre), y tormentas eléctricas con picos de voltaje.",
                verano="Las temporadas secas de diciembre a febrero y de julio a agosto traen más polvo y días soleados, y los equipos de frío trabajan algo más.", invierno="En las temporadas de lluvias hay aguaceros, tormentas eléctricas y variaciones de voltaje al volver la luz, y se usa más la secadora.",
                calor="el frío y la humedad de las lluvias", lluvia="las temporadas de lluvias", volt="110 V", volt2="220 V", ley_datos="Ley 1581 de 2012 sobre protección de datos personales", ley_consumo="Ley 1480 de 2011 (Estatuto del Consumidor)", bomberos="Bomberos (119)",
                ext=[("Superintendencia de Industria y Comercio (SIC): protección al consumidor", "https://www.sic.gov.co/", "Tus derechos como consumidor y cómo presentar una queja."), ("Superintendencia de Servicios Públicos Domiciliarios", "https://www.superservicios.gov.co/", "Información sobre el servicio de energía y gas domiciliario.")],
                ext_lg="https://www.lg.com/co/", vocab=[(r"\bcomunas\b", "zonas"), (r"\bcomuna\b", "zona"), (r"\bboleta\b", "factura"), (r"\bconserjería\b", "portería"), (r"\bporterías\b", "porterías"), (r"\bestacionamientos\b", "parqueaderos"), (r"\bestacionamiento\b", "parqueadero"), (r"\bparqueos\b", "parqueaderos"), (r"\bparqueo\b", "parqueadero"), (r"\bdepartamentos\b", "apartamentos"), (r"\bdepartamento\b", "apartamento"), (r"\bcondominios\b", "conjuntos residenciales"), (r"\bcondominio\b", "conjunto residencial")]),
 "cali": dict(DATOS=CALI, ciudad="Cali", ciudad_corta="Cali", slug="colombia/cali", cc="CO", locale="es-CO", region="Valle del Cauca", pais="Colombia", geo=(3.4516, -76.5320), geo_region="CO-VAC",
                nev="nevera", gas="gas natural domiciliario o gas propano en cilindro (pipeta)", cond="conjuntos residenciales", marcas_sector="Ciudad Jardín, Pance, Granada, San Fernando, Valle del Lili, Jamundí y Yumbo",
                intro_clima="Cali tiene un clima cálido, con dos temporadas de lluvias al año (de abril a junio y de octubre a noviembre), calor casi todo el año y tormentas eléctricas con picos de voltaje.",
                verano="Las temporadas secas de diciembre a marzo y de julio a septiembre traen el calor más fuerte, y los equipos de frío y los aires acondicionados trabajan más.", invierno="En las temporadas de lluvias hay aguaceros, tormentas eléctricas y variaciones de voltaje al volver la luz, y se usa más la secadora.",
                calor="el calor y la humedad durante casi todo el año", lluvia="las temporadas de lluvias", volt="110 V", volt2="220 V", ley_datos="Ley 1581 de 2012 sobre protección de datos personales", ley_consumo="Ley 1480 de 2011 (Estatuto del Consumidor)", bomberos="Bomberos (119)",
                ext=[("Superintendencia de Industria y Comercio (SIC): protección al consumidor", "https://www.sic.gov.co/", "Tus derechos como consumidor y cómo presentar una queja."), ("Superintendencia de Servicios Públicos Domiciliarios", "https://www.superservicios.gov.co/", "Información sobre el servicio de energía y gas domiciliario.")],
                ext_lg="https://www.lg.com/co/", vocab=None),
 "quito": dict(DATOS=QUITO, ciudad="Quito", ciudad_corta="Quito", slug="ecuador/quito", cc="EC", locale="es-EC", region="Pichincha", pais="Ecuador", geo=(-0.1807, -78.4678), geo_region="EC-P",
                nev="refrigeradora", gas="gas licuado en cilindro", cond="conjuntos y urbanizaciones", marcas_sector="La Carolina, Iñaquito, Cumbayá, Tumbaco, El Condado y el Valle de los Chillos",
                intro_clima="Quito tiene un clima de altura, templado de día y frío por las noches, con una temporada de lluvias de octubre a mayo y una temporada seca de junio a septiembre (el verano), con tormentas eléctricas y picos de voltaje.",
                verano="El verano, la temporada seca de junio a septiembre, trae más polvo y viento, y los equipos acumulan polvo en filtros y condensadores.", invierno="En invierno, la temporada de lluvias de octubre a mayo, hay aguaceros, tormentas eléctricas y variaciones de voltaje al volver la luz, y se usa más la secadora.",
                calor="la altura, el frío y la humedad de las lluvias", lluvia="la temporada de lluvias de octubre a mayo", volt="120 V", volt2="240 V", ley_datos="Ley Orgánica de Protección de Datos Personales de Ecuador", ley_consumo="Ley Orgánica de Defensa del Consumidor de Ecuador", bomberos="Bomberos (911)",
                ext=[("Defensoría del Pueblo de Ecuador", "https://www.dpe.gob.ec/", "Tus derechos como consumidor y cómo presentar un reclamo.")],
                ext_lg="https://www.lg.com/ec/", vocab=[(r"\bcomunas\b", "zonas"), (r"\bcomuna\b", "zona"), (r"\bboleta\b", "factura"), (r"\bconserjería\b", "portería"), (r"\bporterías\b", "porterías"), (r"\bestacionamientos\b", "parqueaderos"), (r"\bestacionamiento\b", "parqueadero"), (r"\bparqueos\b", "parqueaderos"), (r"\bparqueo\b", "parqueadero"), (r"\bapartamentos\b", "departamentos"), (r"\bapartamento\b", "departamento"), (r"\bcondominios\b", "conjuntos"), (r"\bcondominio\b", "conjunto"), (r"\bgas propano\b", "gas licuado")]),
 "guayaquil": dict(DATOS=GUAYAQUIL, ciudad="Guayaquil", ciudad_corta="Guayaquil", slug="ecuador/guayaquil", cc="EC", locale="es-EC", region="Guayas", pais="Ecuador", geo=(-2.1700, -79.9224), geo_region="EC-G",
                nev="refrigeradora", gas="gas licuado en cilindro", cond="ciudadelas y urbanizaciones", marcas_sector="Urdesa, Kennedy, Alborada, Sauces, Samborondón y Vía a la Costa",
                intro_clima="Guayaquil tiene un clima tropical, muy caluroso y húmedo, con una temporada de lluvias de diciembre a mayo (el invierno), tormentas eléctricas con picos de voltaje y una temporada seca de junio a noviembre.",
                verano="El verano, la temporada seca de junio a noviembre, trae calor intenso, y los refrigeradores y los aires acondicionados trabajan sin descanso.", invierno="En invierno, la temporada de lluvias de diciembre a mayo, hay aguaceros, tormentas eléctricas y variaciones de voltaje al volver la luz, y la humedad es muy alta.",
                calor="el calor intenso y la humedad durante casi todo el año", lluvia="la temporada de lluvias de diciembre a mayo", volt="120 V", volt2="240 V", ley_datos="Ley Orgánica de Protección de Datos Personales de Ecuador", ley_consumo="Ley Orgánica de Defensa del Consumidor de Ecuador", bomberos="Bomberos (911)",
                ext=[("Defensoría del Pueblo de Ecuador", "https://www.dpe.gob.ec/", "Tus derechos como consumidor y cómo presentar un reclamo.")],
                ext_lg="https://www.lg.com/ec/", vocab=None),
}
C["cali"]["vocab"] = C["bogota"]["vocab"]; C["guayaquil"]["vocab"] = C["quito"]["vocab"]
for _k, _v in C.items():     # variantes con mayúscula inicial
    if _v["vocab"] is not None: _v["vocab"] = list(_v["vocab"]) + [(r"\bComunas\b", "Zonas"), (r"\bComuna\b", "Zona"), (r"\bEstacionamientos\b", "Parqueos" if _k in ("costarica",) else "Estacionamientos")]
    else: _v["vocab"] = []



def build_cfg(key, tel, solo_wa=True):
    """Arma la configuración de una ciudad a partir de su descripción (zonas, sectores, clima, vocabulario y leyes)."""
    c = C[key]; D = c["DATOS"]; ciudad = c["ciudad"]; pais = c["pais"]
    zonas, zx, clima, destacadas = {}, {}, {}, []
    for slug, nombre, sect, tipo in D["zonas"]:
        viv, corta, acc = TIPOS[tipo]
        zonas[slug] = (nombre, sect, viv); zx[slug] = (corta, acc, sect)
        clima[slug] = (f"{c['calor']}, sumados a los picos de voltaje de las tormentas eléctricas al volver la luz," if tipo != "ext" else f"las variaciones de voltaje en redes más largas, el polvo de los caminos y las tormentas eléctricas de {c['lluvia']}")
    orden = [z[0] for z in D["zonas"]]
    sectores = D["sectores"]
    assert sorted(z for v in sectores.values() for z in v[2]) == sorted(orden), set(orden) ^ {z for v in sectores.values() for z in v[2]}
    sector_de = {z: s for s, v in sectores.items() for z in v[2]}
    n = len(orden)
    reemp = [("Ver las 52 comunas donde atendemos", f"Ver las {n} zonas y municipios donde atendemos"), ("Atendemos las 52 comunas de la Región Metropolitana", f"Atendemos las {n} zonas y municipios de {ciudad} y su área metropolitana"),
             ("en Santiago de Chile y toda la Región Metropolitana", f"en {ciudad} y todo su área metropolitana"),
             ("En Chile las viviendas usan 220 V.", f"En {pais} los tomacorrientes comunes son de {c['volt']} y algunos equipos grandes usan {c['volt2']}."),
             ("¿Qué voltaje se usa en Chile?", f"¿Qué voltaje se usa en {pais}?"),
             ("En Chile, la Ley N° 19.496 sobre protección de los derechos de los consumidores contempla una garantía legal para productos nuevos; consulta en el SERNAC los plazos y condiciones vigentes.", f"En {pais}, la {c['ley_consumo']} protege tus derechos como consumidor; consulta en la entidad de protección al consumidor los plazos y condiciones vigentes."),
             ("En Chile, la Ley N° 19.496 contempla además una garantía legal para productos nuevos.", f"En {pais}, la {c['ley_consumo']} protege además tus derechos como consumidor."),
             ("su representante en Chile", f"su representante en {pais}"), ("Bomberos (132)", c["bomberos"]),
             ("Los veranos de Santiago son secos y calurosos, y los equipos de frío trabajan más.", c["verano"]),
             ("En invierno hay temporales, cortes de luz y variaciones de voltaje al volver el suministro, y se usa más la secadora.", c["invierno"]),
             ("el verano de Santiago", f"el verano de {ciudad}"), ("el invierno de Santiago", f"el invierno de {ciudad}"),
             ("Santiago de Chile", ciudad), ("la Región Metropolitana", "el área metropolitana"), ("Región Metropolitana", "área metropolitana"), ("de Santiago", f"de {ciudad}"), ("para Santiago", f"para {ciudad}"), ("en Santiago", f"en {ciudad}")]
    cfg = dict(
        sitio="i_" + key, dom="", ciudad=ciudad, ciudad_larga=("Ciudad de Panamá" if key == "panama" else ciudad), ciudad_corta=c["ciudad_corta"], nombre=f"Servicio Técnico {ciudad}",
        tel=tel, telw=re.sub(r"\D", "", tel), solo_wa=solo_wa, locale=c["locale"], cc=c["cc"], region=c["region"], pais=pais, gsc=[],
        ext_lg=(f"Página del fabricante: LG {pais}", c["ext_lg"]), ext_samsung=("Página del fabricante: Samsung Latinoamérica", "https://www.samsung.com/latin/"), ext_oficiales=c["ext"],
        trust_zonas=(f"{n} zonas y municipios", f"Toda el área de {ciudad}"), lead_cob=f"las zonas y municipios del área metropolitana de {ciudad}",
        guia_humedad=("humedad-y-tormentas-en-equipos", f"Humedad y tormentas en equipos {{N}} en {ciudad}", f"Cómo la humedad, el clima y las tormentas eléctricas de {ciudad} afectan tus equipos {{N}}: qué fallas provocan y cómo prevenirlas."),
        clima_art=dict(h2="Qué hacen el clima y las tormentas en tus equipos ", etq="el clima y las tormentas",
                       texto=f"{c['calor'].capitalize()} y {c['lluvia']} exigen más a los equipos; las tormentas eléctricas provocan apagones y picos de voltaje que dañan placas; y el polvo tapa filtros, condensadores y rejillas."),
        volt_art=dict(h2="Por qué importa el voltaje en equipos ", titulo="Apagones y voltaje: protege tus equipos {N}", desc=f"Qué equipos {{N}} sufren más con los apagones y las variaciones de voltaje en {ciudad} y cómo proteger sus placas y compresores.",
                      texto="Las tormentas eléctricas y los apagones pueden generar variaciones y picos de voltaje al volver la luz. En equipos {N}, los más sensibles son {eq}, porque dependen de placas y sensores electrónicos."),
        aire_art=dict(slug="aire-acondicionado-{m}-calor", titulo="Aire acondicionado {N}: qué revisar", desc=f"Qué revisar en tu aire acondicionado {{N}} antes y durante los meses más calurosos en {ciudad}."),
        intro_clima=c["intro_clima"],
        clima_extra=f"Las tormentas eléctricas pueden provocar apagones y variaciones de voltaje al volver el suministro, que dañan placas electrónicas. Un protector de voltaje adecuado y desconectar los equipos más sensibles durante tormentas fuertes reduce ese riesgo. {c['calor'].capitalize()} exigen más a refrigeradores y aires acondicionados, y la humedad favorece el moho en lavadoras y sellos.",
        clima_txt=c.get("clima_txt", ("clima y tormentas", "Clima y tormentas")), guias_clima=f"{c['calor']} y los apagones con sus picos de voltaje",
        ley_datos=c["ley_datos"], ley_consumo=c["ley_consumo"], costero=c.get("costero", False),
        nev=("refrigeradoras", "refrigeradora", "refrigeradoras") if c["nev"] == "refrigeradora" else ("neveras", "nevera", "neveras"),
        zonas=zonas, zx=zx, clima=clima, zonas_destacadas=orden[:12], sectores=sectores, sector_de=sector_de, comunas_eq=orden[:28],
        area=[zonas[z][0] for z in orden[:12]], geo=c["geo"], geo_region=c["geo_region"], zlista=", ".join(zonas[z][0] for z in orden[:8]) + " y el resto de zonas y municipios",
        reemp=reemp, vocab=c["vocab"], sin_recorte=True, lbl_guias="Blog de consejos", seo_plus=True, sin_tropico=True, esencial=True, busquedas=True, sin_toc=True, pro_layout=True,
        mi=mi_para(c))
    return cfg


def mi_para(c):
    """Textos de mantenimiento e instalación adaptados a la ciudad (a partir de los de San Salvador)."""
    from cst_salvador_mi import SV_MI
    ciudad, pais = c["ciudad"], c["pais"]
    out = {}
    for e, d in SV_MI.items():
        out[e] = {k: v.replace("San Salvador", ciudad).replace("El Salvador", pais) for k, v in d.items()}
    out["neveras"]["mant_gye"] = f"En {ciudad}, {c['calor']} hacen trabajar más al compresor y ensucian el condensador: conviene limpiarlo antes de {c['lluvia']}. Si hay un apagón por una tormenta, no abras la puerta más de lo necesario y espera unos minutos antes de volver a conectar cuando regrese la luz."
    out["neveras"]["mant_intro"] = f"El mantenimiento preventivo de una refrigeradora es sencillo y evita la mayoría de averías caras. En {ciudad}, donde {c['calor']} obligan al compresor a trabajar más y las tormentas eléctricas dañan las placas, conviene limpiar el condensador con regularidad y proteger el equipo."
    out["cocinas"]["inst_gye"] = f"En {pais} muchas cocinas funcionan con {c['gas']}: la ruta de la manguera, la ventilación y la instalación hecha por una persona calificada son parte de la instalación segura. Si la cocina va empotrada en un mueble de madera, hay que verificar la distancia a las paredes."
    out["aires"]["mant_gye"] = f"En {ciudad} el aire acondicionado trabaja más en los meses de más calor. Programa el mantenimiento antes de esa época y limpia los filtros con frecuencia, porque el polvo y la humedad los ensucian rápido."
    out["aires"]["mant_intro"] = f"El mantenimiento de un aire acondicionado incluye limpiar filtros, evaporador, condensador y drenaje, además de medir presiones. Es lo que más alarga la vida del equipo, sobre todo en {ciudad}, con {c['calor']}."
    out["lavadoras"]["mant_gye"] = out["lavadoras"]["mant_gye"].replace("con el calor y la humedad", f"con {c['calor']}")
    out["centro-lavado"] = out["lavadoras"]
    return out


# ciudades principales de Colombia (además de Bogotá y Cali): se arman a partir de la configuración de Cali
from cst_colombia import DATOS_COL
for _k, (_D, _e) in DATOS_COL.items():
    C[_k] = dict(C["cali"], DATOS=_D, ciudad_corta=_e["ciudad"], **_e)
