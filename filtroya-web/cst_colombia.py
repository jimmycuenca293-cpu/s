# -*- coding: utf-8 -*-
"""Ciudades principales de Colombia para el sitio internacional de Frigidaire (además de Bogotá y Cali):
Bucaramanga, Cartagena, Barranquilla, Valledupar, Ibagué, Manizales, Medellín y Santa Marta.
Solo se nombran zonas, barrios y municipios reconocidos; las frases de sector empiezan con «el» (se usan en títulos como «Zonas del …»)."""

BUCARAMANGA = dict(
    zonas=[("cabecera-del-llano", "Cabecera del Llano", "Cabecera del Llano y la Carrera 33", "alta"), ("sotomayor", "Sotomayor", "Sotomayor", "alta"), ("la-concordia", "La Concordia", "La Concordia", "media"),
           ("provenza", "Provenza", "Provenza", "media"), ("san-francisco", "San Francisco", "San Francisco", "media"), ("real-de-minas", "Real de Minas", "Real de Minas", "media"), ("mutis", "Mutis", "Mutis", "media"),
           ("centro-de-bucaramanga", "Centro de Bucaramanga", "Centro y la Plaza Guarín", "hist"), ("la-victoria", "La Victoria", "La Victoria", "pop"), ("kennedy", "Kennedy", "Kennedy", "pop"), ("colorados", "Colorados", "Colorados", "media"),
           ("floridablanca", "Floridablanca", "Floridablanca centro", "media"), ("canaveral", "Cañaveral", "Cañaveral", "alta"), ("lagos-del-cacique", "Lagos del Cacique", "Lagos del Cacique", "res"), ("zapamanga", "Zapamanga", "Zapamanga", "res"),
           ("giron", "Girón", "Centro histórico de Girón", "hist"), ("ciudad-valencia", "Ciudad Valencia", "Ciudad Valencia", "res"), ("rincon-de-giron", "Rincón de Girón", "Rincón de Girón", "res"),
           ("piedecuesta", "Piedecuesta", "Piedecuesta centro", "ext"), ("ruitoque", "Ruitoque", "Ruitoque", "res"), ("menzuly", "Menzuly", "Menzuly", "res"), ("guatiguara", "Guatiguará", "Guatiguará", "ext")],
    sectores={"oriente-de-bucaramanga": ("el oriente de Bucaramanga", "Cabecera del Llano, Sotomayor, La Concordia, Provenza, San Francisco, Real de Minas y Mutis: apartamentos, edificios y casas de clase media y alta, con portería y parqueaderos de visitantes.", ["cabecera-del-llano", "sotomayor", "la-concordia", "provenza", "san-francisco", "real-de-minas", "mutis"]),
              "centro-y-norte-de-bucaramanga": ("el centro y el norte de Bucaramanga", "El centro, La Victoria, Kennedy y Colorados: comercio, barrios tradicionales y barrios populosos, con poco parqueo.", ["centro-de-bucaramanga", "la-victoria", "kennedy", "colorados"]),
              "municipio-de-floridablanca": ("el municipio de Floridablanca", "Floridablanca centro, Cañaveral, Lagos del Cacique y Zapamanga: conjuntos cerrados y casas de gama media y alta.", ["floridablanca", "canaveral", "lagos-del-cacique", "zapamanga"]),
              "municipio-de-giron": ("el municipio de Girón", "El centro histórico, Ciudad Valencia y Rincón de Girón: casas coloniales y conjuntos residenciales.", ["giron", "ciudad-valencia", "rincon-de-giron"]),
              "municipio-de-piedecuesta": ("el municipio de Piedecuesta", "Piedecuesta centro, Ruitoque, Menzuly y Guatiguará: conjuntos y casas campestres, con distancias mayores desde Bucaramanga.", ["piedecuesta", "ruitoque", "menzuly", "guatiguara"])},
)
CARTAGENA = dict(
    zonas=[("bocagrande", "Bocagrande", "Bocagrande y la Avenida San Martín", "alta"), ("el-laguito", "El Laguito", "El Laguito", "alta"), ("castillogrande", "Castillogrande", "Castillogrande", "alta"), ("manga", "Manga", "Manga", "media"),
           ("el-cabrero", "El Cabrero", "El Cabrero", "media"), ("centro-historico", "Centro Histórico", "Centro Histórico y la Ciudad Amurallada", "hist"), ("getsemani", "Getsemaní", "Getsemaní", "hist"), ("san-diego", "San Diego", "San Diego", "hist"),
           ("pie-de-la-popa", "Pie de la Popa", "Pie de la Popa", "media"), ("marbella", "Marbella", "Marbella", "media"), ("crespo", "Crespo", "Crespo y la zona del aeropuerto", "media"), ("zona-norte", "Zona Norte", "Zona Norte y Cielo Mar", "res"),
           ("la-boquilla", "La Boquilla", "La Boquilla", "res"), ("serena-del-mar", "Serena del Mar", "Serena del Mar", "res"), ("torices", "Torices", "Torices", "pop"), ("olaya-herrera", "Olaya Herrera", "Olaya Herrera", "pop"),
           ("ternera", "Ternera", "Ternera", "pop"), ("los-alpes", "Los Alpes", "Los Alpes", "pop"), ("turbaco", "Turbaco", "Turbaco centro", "ext")],
    sectores={"bocagrande-y-el-laguito": ("el sector de Bocagrande y El Laguito", "Bocagrande, El Laguito, Castillogrande, Manga y El Cabrero: torres de apartamentos frente al mar y barrios residenciales, con portería y parqueo limitado.", ["bocagrande", "el-laguito", "castillogrande", "manga", "el-cabrero"]),
              "centro-historico-de-cartagena": ("el centro histórico de Cartagena", "El Centro Histórico, Getsemaní, San Diego y Pie de la Popa: casas coloniales, hoteles y edificios antiguos, con calles angostas.", ["centro-historico", "getsemani", "san-diego", "pie-de-la-popa"]),
              "norte-de-cartagena": ("el norte de Cartagena", "Marbella, Crespo, la Zona Norte, La Boquilla y Serena del Mar: conjuntos y urbanizaciones cerca del mar, con controles de acceso.", ["marbella", "crespo", "zona-norte", "la-boquilla", "serena-del-mar"]),
              "sur-y-oriente-de-cartagena": ("el sur y el oriente de Cartagena", "Torices, Olaya Herrera, Ternera, Los Alpes y Turbaco: barrios populosos y municipios vecinos, con distancias mayores desde el centro.", ["torices", "olaya-herrera", "ternera", "los-alpes", "turbaco"])},
)
BARRANQUILLA = dict(
    zonas=[("el-prado", "El Prado", "El Prado", "alta"), ("alto-prado", "Alto Prado", "Alto Prado", "alta"), ("riomar", "Riomar", "Riomar", "alta"), ("ciudad-jardin", "Ciudad Jardín", "Ciudad Jardín", "alta"),
           ("villa-country", "Villa Country", "Villa Country", "alta"), ("granadillo", "Granadillo", "Granadillo", "alta"), ("buenavista", "Buenavista", "Buenavista", "alta"), ("villa-carolina", "Villa Carolina", "Villa Carolina", "media"),
           ("boston", "Boston", "Boston", "media"), ("miramar", "Miramar", "Miramar", "media"), ("centro-de-barranquilla", "Centro de Barranquilla", "Centro y la Calle 72", "hist"), ("barrio-abajo", "Barrio Abajo", "Barrio Abajo", "hist"),
           ("rebolo", "Rebolo", "Rebolo", "pop"), ("la-chinita", "La Chinita", "La Chinita", "pop"), ("soledad", "Soledad", "Soledad centro", "pop"), ("puerto-colombia", "Puerto Colombia", "Puerto Colombia", "res"),
           ("malambo", "Malambo", "Malambo", "ext"), ("galapa", "Galapa", "Galapa", "ext")],
    sectores={"norte-de-barranquilla": ("el norte de Barranquilla", "El Prado, Alto Prado, Riomar, Ciudad Jardín, Villa Country, Granadillo, Buenavista y Villa Carolina: apartamentos, edificios y conjuntos de gama media y alta, con aire acondicionado de uso casi permanente.", ["el-prado", "alto-prado", "riomar", "ciudad-jardin", "villa-country", "granadillo", "buenavista", "villa-carolina"]),
              "centro-y-sur-de-barranquilla": ("el centro y el sur de Barranquilla", "Boston, Miramar, el centro, Barrio Abajo, Rebolo y La Chinita: barrios tradicionales y populosos, con calles angostas.", ["boston", "miramar", "centro-de-barranquilla", "barrio-abajo", "rebolo", "la-chinita"]),
              "area-metropolitana-de-barranquilla": ("el área metropolitana de Barranquilla", "Soledad, Puerto Colombia, Malambo y Galapa: municipios vecinos con distancias mayores desde el centro.", ["soledad", "puerto-colombia", "malambo", "galapa"])},
)
VALLEDUPAR = dict(
    zonas=[("los-mayales", "Los Mayales", "Los Mayales", "alta"), ("los-campanos", "Los Campanos", "Los Campanos", "alta"), ("canaguate", "Cañaguate", "Cañaguate", "res"), ("altos-del-rosario", "Altos del Rosario", "Altos del Rosario", "res"),
           ("novalito", "Novalito", "Novalito", "res"), ("altamira", "Altamira", "Altamira", "res"), ("los-almendros", "Los Almendros", "Los Almendros", "res"), ("centro-de-valledupar", "Centro de Valledupar", "Centro y la Plaza Alfonso López", "hist"),
           ("alfonso-lopez", "Alfonso López", "Alfonso López", "media"), ("villa-castro", "Villa Castro", "Villa Castro", "media"), ("la-nevada", "La Nevada", "La Nevada", "media"), ("los-fundadores", "Los Fundadores", "Los Fundadores", "media"),
           ("dangond", "Dangond", "Dangond", "media"), ("mareigua", "Mareigua", "Mareigua", "media"), ("sicarare", "Sicarare", "Sicarare", "pop"), ("garupal", "Garupal", "Garupal", "pop"), ("villa-corelca", "Villa Corelca", "Villa Corelca", "pop"),
           ("primero-de-mayo", "Primero de Mayo", "Primero de Mayo", "pop"), ("doce-de-octubre", "12 de Octubre", "12 de Octubre", "pop"), ("simon-bolivar", "Simón Bolívar", "Simón Bolívar", "pop"), ("divino-nino", "Divino Niño", "Divino Niño", "pop"),
           ("badillo", "Badillo", "Badillo", "ext"), ("patillal", "Patillal", "Patillal", "ext"), ("valencia-de-jesus", "Valencia de Jesús", "Valencia de Jesús", "ext")],
    sectores={"norte-de-valledupar": ("el norte de Valledupar", "Los Mayales, Los Campanos, Cañaguate, Altos del Rosario, Novalito, Altamira y Los Almendros: conjuntos cerrados y casas de gama media y alta, con aire acondicionado de uso casi permanente.", ["los-mayales", "los-campanos", "canaguate", "altos-del-rosario", "novalito", "altamira", "los-almendros"]),
              "centro-de-valledupar": ("el centro de Valledupar", "El centro, Alfonso López, Villa Castro, La Nevada, Los Fundadores, Dangond y Mareigua: barrios tradicionales y comercio, con poco parqueo.", ["centro-de-valledupar", "alfonso-lopez", "villa-castro", "la-nevada", "los-fundadores", "dangond", "mareigua"]),
              "sur-y-oriente-de-valledupar": ("el sur y el oriente de Valledupar", "Sicarare, Garupal, Villa Corelca, Primero de Mayo, 12 de Octubre, Simón Bolívar y Divino Niño: barrios populosos, con calles angostas.", ["sicarare", "garupal", "villa-corelca", "primero-de-mayo", "doce-de-octubre", "simon-bolivar", "divino-nino"]),
              "corregimientos-de-valledupar": ("los corregimientos de Valledupar", "Badillo, Patillal y Valencia de Jesús: poblaciones cercanas con distancias mayores desde la ciudad.", ["badillo", "patillal", "valencia-de-jesus"])},
)
IBAGUE = dict(
    zonas=[("centro-de-ibague", "Centro de Ibagué", "Centro y la Plaza de Bolívar", "hist"), ("la-pola", "La Pola", "La Pola", "media"), ("cadiz", "Cádiz", "Cádiz", "media"), ("interlaken", "Interlaken", "Interlaken", "res"),
           ("arkacentro", "Arkacentro", "Arkacentro", "alta"), ("mirolindo", "Mirolindo", "Mirolindo", "media"), ("piedra-pintada", "Piedra Pintada", "Piedra Pintada", "res"), ("belen", "Belén", "Belén", "pop"), ("gaitan", "Gaitán", "Gaitán", "pop"),
           ("el-vergel", "El Vergel", "El Vergel", "pop"), ("las-americas", "Las Américas", "Las Américas", "pop"), ("libertador", "Libertador", "Libertador", "pop"), ("santa-ana", "Santa Ana", "Santa Ana", "pop"), ("restrepo", "Restrepo", "Restrepo", "pop"),
           ("ambala", "Ambalá", "Ambalá", "pop"), ("jordan", "Jordán", "Jordán", "res"), ("picalena", "Picaleña", "Picaleña", "res"), ("el-salado", "El Salado", "El Salado", "media"), ("calambeo", "Calambeo", "Calambeo", "ext"),
           ("ciudad-luz", "Ciudad Luz", "Ciudad Luz", "res"), ("la-francia", "La Francia", "La Francia", "res"), ("combeima", "Combeima", "Combeima", "ext")],
    sectores={"centro-y-zona-residencial-de-ibague": ("el centro y la zona residencial de Ibagué", "El centro, La Pola, Cádiz, Interlaken, Arkacentro, Mirolindo y Piedra Pintada: edificios, conjuntos y casas de clase media y alta, con portería y parqueo limitado.", ["centro-de-ibague", "la-pola", "cadiz", "interlaken", "arkacentro", "mirolindo", "piedra-pintada"]),
              "sector-popular-de-ibague": ("el sector de barrios populares de Ibagué", "Belén, Gaitán, El Vergel, Las Américas, Libertador, Santa Ana, Restrepo y Ambalá: barrios populosos, con calles angostas y equipos de uso familiar.", ["belen", "gaitan", "el-vergel", "las-americas", "libertador", "santa-ana", "restrepo", "ambala"]),
              "periferia-de-ibague": ("el sector periférico de Ibagué", "Jordán, Picaleña, El Salado, Calambeo, Ciudad Luz, La Francia y Combeima: conjuntos y casas con distancias mayores desde el centro.", ["jordan", "picalena", "el-salado", "calambeo", "ciudad-luz", "la-francia", "combeima"])},
)
MANIZALES = dict(
    zonas=[("centro-de-manizales", "Centro de Manizales", "Centro, Catedral y Plaza de Bolívar", "hist"), ("cable", "El Cable", "El Cable", "alta"), ("milan", "Milán", "Milán", "media"), ("chipre", "Chipre", "Chipre", "media"),
           ("palermo", "Palermo", "Palermo", "media"), ("versalles", "Versalles", "Versalles", "media"), ("campohermoso", "Campohermoso", "Campohermoso", "media"), ("la-enea", "La Enea", "La Enea", "res"), ("alta-suiza", "Alta Suiza", "Alta Suiza", "res"),
           ("malteria", "Maltería", "Maltería", "res"), ("avenida-santander", "Avenida Santander", "Avenida Santander", "media"), ("villamaria", "Villamaría", "Villamaría", "ext"), ("chinchina", "Chinchiná", "Chinchiná", "ext")],
    sectores={"centro-de-manizales": ("el centro de Manizales", "El centro, El Cable, Chipre, Palermo, Versalles y Campohermoso: edificios y casas en calles con pendiente, con poco parqueo.", ["centro-de-manizales", "cable", "chipre", "palermo", "versalles", "campohermoso"]),
              "zona-residencial-de-manizales": ("el sector residencial de Manizales", "Milán, La Enea, Alta Suiza, Maltería y la Avenida Santander: conjuntos y casas de clase media y alta.", ["milan", "la-enea", "alta-suiza", "malteria", "avenida-santander"]),
              "municipios-vecinos-de-manizales": ("los municipios vecinos de Manizales", "Villamaría y Chinchiná: municipios cercanos con distancias mayores desde la ciudad.", ["villamaria", "chinchina"])},
)
MEDELLIN = dict(
    zonas=[("el-poblado", "El Poblado", "El Poblado, Provenza y Parque Lleras", "alta"), ("laureles", "Laureles", "Laureles y la Avenida Nutibara", "alta"), ("estadio", "Estadio", "Estadio y Conquistadores", "media"), ("belen", "Belén", "Belén", "media"),
           ("la-america", "La América", "La América", "media"), ("guayabal", "Guayabal", "Guayabal", "media"), ("robledo", "Robledo", "Robledo", "pop"), ("san-javier", "San Javier", "San Javier", "pop"), ("candelaria", "La Candelaria", "Centro y La Candelaria", "hist"),
           ("villa-hermosa", "Villa Hermosa", "Villa Hermosa", "pop"), ("buenos-aires", "Buenos Aires", "Buenos Aires", "media"), ("aranjuez", "Aranjuez", "Aranjuez", "pop"), ("manrique", "Manrique", "Manrique", "pop"), ("castilla", "Castilla", "Castilla", "pop"),
           ("envigado", "Envigado", "Envigado centro", "alta"), ("sabaneta", "Sabaneta", "Sabaneta centro", "media"), ("itagui", "Itagüí", "Itagüí centro", "media"), ("la-estrella", "La Estrella", "La Estrella", "ext"), ("caldas", "Caldas", "Caldas", "ext"),
           ("bello", "Bello", "Bello centro", "pop"), ("copacabana", "Copacabana", "Copacabana", "ext"), ("rionegro", "Rionegro", "Rionegro centro", "res")],
    sectores={"sur-de-medellin": ("el sur del Valle de Aburrá", "El Poblado, Envigado, Sabaneta, Itagüí, La Estrella y Caldas: apartamentos y casas de gama media y alta, con portería y parqueaderos de visitantes.", ["el-poblado", "envigado", "sabaneta", "itagui", "la-estrella", "caldas"]),
              "occidente-de-medellin": ("el occidente de Medellín", "Laureles, Estadio, Belén, La América, Guayabal, Robledo y San Javier: barrios de clase media y populosos, con el tráfico de la Avenida 80 y la 33.", ["laureles", "estadio", "belen", "la-america", "guayabal", "robledo", "san-javier"]),
              "centro-y-norte-de-medellin": ("el centro y el norte de Medellín", "La Candelaria, Villa Hermosa, Buenos Aires, Aranjuez, Manrique, Castilla, Bello y Copacabana: barrios tradicionales y populosos, con calles con pendiente.", ["candelaria", "villa-hermosa", "buenos-aires", "aranjuez", "manrique", "castilla", "bello", "copacabana"]),
              "oriente-antioqueno": ("el municipio de Rionegro", "Rionegro centro: urbanizaciones y casas en el Oriente antioqueño, con distancias mayores desde Medellín.", ["rionegro"])},
)
SANTA_MARTA = dict(
    zonas=[("el-rodadero", "El Rodadero", "El Rodadero", "res"), ("bello-horizonte", "Bello Horizonte", "Bello Horizonte", "alta"), ("pozos-colorados", "Pozos Colorados", "Pozos Colorados", "res"), ("taganga", "Taganga", "Taganga", "ext"),
           ("gaira", "Gaira", "Gaira", "ext"), ("centro-historico-de-santa-marta", "Centro Histórico de Santa Marta", "Centro Histórico y la Bahía", "hist"), ("bastidas", "Bastidas", "Bastidas", "media"), ("los-almendros", "Los Almendros", "Los Almendros", "media"),
           ("pescaito", "Pescaíto", "Pescaíto", "pop"), ("mamatoco", "Mamatoco", "Mamatoco", "pop"), ("bonda", "Bonda", "Bonda", "ext"), ("cienaga", "Ciénaga", "Ciénaga centro", "ext")],
    sectores={"centro-de-santa-marta": ("el centro de Santa Marta", "El Centro Histórico, Bastidas, Los Almendros, Pescaíto y Mamatoco: barrios tradicionales y populosos, con calles angostas.", ["centro-historico-de-santa-marta", "bastidas", "los-almendros", "pescaito", "mamatoco"]),
              "sector-turistico-de-santa-marta": ("el sector turístico de Santa Marta", "El Rodadero, Bello Horizonte, Pozos Colorados, Taganga y Gaira: apartamentos, hoteles y casas cerca del mar, con calor y salitre.", ["el-rodadero", "bello-horizonte", "pozos-colorados", "taganga", "gaira"]),
              "alrededores-de-santa-marta": ("los alrededores de Santa Marta", "Bonda y Ciénaga: poblaciones cercanas con distancias mayores desde la ciudad.", ["bonda", "cienaga"])},
)

def _base(extra):
    return extra

DATOS_COL = {
    "bucaramanga": (BUCARAMANGA, dict(ciudad="Bucaramanga", slug="colombia/bucaramanga", region="Santander", geo=(7.1254, -73.1198), geo_region="CO-SAN",
        marcas_sector="Cabecera del Llano, Sotomayor, Provenza, Floridablanca, Girón y Piedecuesta",
        intro_clima="Bucaramanga tiene un clima cálido y agradable, con dos temporadas de lluvias al año (de abril a mayo y de septiembre a noviembre) y tormentas eléctricas con picos de voltaje.",
        verano="Las temporadas secas de diciembre a marzo y de junio a agosto traen más calor y polvo, y los equipos de frío trabajan más.", calor="el calor y la humedad de la meseta", lluvia="las temporadas de lluvias", bomberos="Bomberos (119)")),
    "cartagena": (CARTAGENA, dict(ciudad="Cartagena", slug="colombia/cartagena", region="Bolívar", geo=(10.3910, -75.4794), geo_region="CO-BOL", costero=True, clima_txt=("calor, humedad y salitre", "Calor, humedad y salitre"),
        marcas_sector="Bocagrande, El Laguito, Manga, Crespo, Zona Norte y Turbaco",
        intro_clima="Cartagena tiene un clima caribeño, muy caluroso y húmedo, con brisa marina y salitre, una temporada seca de diciembre a abril y lluvias sobre todo de septiembre a noviembre, con tormentas eléctricas y picos de voltaje.",
        verano="El verano, la temporada seca de diciembre a abril, trae calor y brisa con salitre, y los equipos de frío y los aires acondicionados trabajan más.", calor="el calor intenso, la humedad y el salitre del mar", lluvia="las lluvias de septiembre a noviembre", bomberos="Bomberos (119)")),
    "barranquilla": (BARRANQUILLA, dict(ciudad="Barranquilla", slug="colombia/barranquilla", region="Atlántico", geo=(10.9685, -74.7813), geo_region="CO-ATL", costero=True, clima_txt=("calor, humedad y salitre", "Calor, humedad y salitre"),
        marcas_sector="El Prado, Alto Prado, Riomar, Ciudad Jardín, Villa Country y Soledad",
        intro_clima="Barranquilla tiene un clima caribeño, muy caluroso y húmedo, con una temporada seca de diciembre a abril y lluvias de septiembre a noviembre, cuando los arroyos y las tormentas eléctricas traen picos de voltaje.",
        verano="El verano, la temporada seca de diciembre a abril, trae el calor más fuerte, y los equipos de frío y los aires acondicionados trabajan sin descanso.", calor="el calor intenso y la humedad", lluvia="las lluvias de septiembre a noviembre", bomberos="Bomberos (119)")),
    "valledupar": (VALLEDUPAR, dict(ciudad="Valledupar", slug="colombia/valledupar", region="Cesar", geo=(10.4631, -73.2532), geo_region="CO-CES",
        marcas_sector="Los Mayales, Los Campanos, Cañaguate, Alfonso López y Villa Castro",
        intro_clima="Valledupar tiene un clima muy caluroso y seco, con dos temporadas de lluvias al año (de abril a junio y de septiembre a noviembre), mucho polvo y tormentas eléctricas con picos de voltaje.",
        verano="El verano, la temporada seca de diciembre a marzo, trae el calor más intenso y mucho polvo, y los aires acondicionados y los equipos de frío trabajan al límite.", calor="el calor muy intenso y el polvo", lluvia="las temporadas de lluvias", bomberos="Bomberos (119)")),
    "ibague": (IBAGUE, dict(ciudad="Ibagué", slug="colombia/ibague", region="Tolima", geo=(4.4389, -75.2322), geo_region="CO-TOL",
        marcas_sector="Interlaken, Arkacentro, Jordán, Picaleña, El Salado y el centro",
        intro_clima="Ibagué tiene un clima cálido y templado, con dos temporadas de lluvias al año (de marzo a mayo y de octubre a noviembre) y tormentas eléctricas con picos de voltaje.",
        verano="Las temporadas secas de diciembre a febrero y de junio a agosto traen más calor y polvo, y los equipos de frío trabajan más.", calor="el calor y la humedad", lluvia="las temporadas de lluvias", bomberos="Bomberos (119)")),
    "manizales": (MANIZALES, dict(ciudad="Manizales", slug="colombia/manizales", region="Caldas", geo=(5.0703, -75.5138), geo_region="CO-CAL",
        marcas_sector="El Cable, Chipre, Palermo, Milán, La Enea y Villamaría",
        intro_clima="Manizales tiene un clima frío y húmedo de montaña, con lluvias frecuentes casi todo el año, neblina y tormentas eléctricas con picos de voltaje.",
        verano="Las temporadas menos lluviosas de diciembre a febrero y de julio a agosto traen más días soleados, pero la humedad sigue siendo alta.", calor="el frío, la neblina y la humedad de las lluvias frecuentes", lluvia="las lluvias frecuentes", bomberos="Bomberos (119)")),
    "medellin": (MEDELLIN, dict(ciudad="Medellín", slug="colombia/medellin", region="Antioquia", geo=(6.2442, -75.5812), geo_region="CO-ANT",
        marcas_sector="El Poblado, Laureles, Envigado, Sabaneta, Belén y Rionegro",
        intro_clima="Medellín tiene un clima templado de valle, con dos temporadas de lluvias al año (de abril a mayo y de octubre a noviembre) y tormentas eléctricas con picos de voltaje.",
        verano="Las temporadas secas de diciembre a febrero y de junio a agosto traen más sol y polvo, y los equipos acumulan polvo en filtros y condensadores.", calor="el clima templado, la humedad y las lluvias", lluvia="las temporadas de lluvias", bomberos="Bomberos (119)")),
    "santamarta": (SANTA_MARTA, dict(ciudad="Santa Marta", slug="colombia/santa-marta", region="Magdalena", geo=(11.2408, -74.1990), geo_region="CO-MAG", costero=True, clima_txt=("calor, humedad y salitre", "Calor, humedad y salitre"),
        marcas_sector="El Rodadero, Bello Horizonte, Pozos Colorados, Taganga, Gaira y el centro",
        intro_clima="Santa Marta tiene un clima caribeño, caluroso y húmedo, con brisa marina y salitre, una temporada seca de diciembre a abril y lluvias sobre todo de septiembre a noviembre, con tormentas eléctricas y picos de voltaje.",
        verano="El verano, la temporada seca de diciembre a abril, trae calor intenso y brisa con salitre, y los equipos de frío trabajan más.", calor="el calor intenso, la humedad y el salitre del mar", lluvia="las lluvias de septiembre a noviembre", bomberos="Bomberos (119)")),
}
