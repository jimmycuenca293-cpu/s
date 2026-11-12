"""Tiendas locales «como la de Bogotá» para otras ciudades. Se cambian los datos (comunas, barrios, zonas) y, al final, se pasa por todo el sitio un traductor de textos
(Bogotá → Medellín, localidad → comuna, la sede). Así Medellín tiene exactamente la misma tienda, con sus propios barrios y direcciones."""
import pathlib
import re

import bogota_seo

ORIGINAL = dict(LOCALIDADES=bogota_seo.LOCALIDADES, ZONAS=bogota_seo.ZONAS, POPULARES=bogota_seo.POPULARES, CATS=bogota_seo.CATS_OVERRIDE, TEXTO_PORTADA=bogota_seo.TEXTO_PORTADA)

# ---------------------------------------------------------------- Medellín
MED_LOC = {
    "Popular": ("Nororiente", ["Santa Cruz", "Manrique"], "Comuna del nororiente de Medellín, de barrios de ladera con vivienda en casas y edificios bajos.",
                ["Popular", "Santo Domingo Savio", "Villa Guadalupe", "Carpinelo", "El Compromiso", "Granizal"]),
    "Santa Cruz": ("Nororiente", ["Popular", "Manrique", "Castilla"], "Comuna del nororiente de barrios residenciales y comercio de barrio, en las laderas.",
                   ["Santa Cruz", "La Rosa", "Villa del Socorro", "Moscú", "La Francia", "Andalucía", "Playón de los Comuneros"]),
    "Manrique": ("Nororiente", ["Popular", "Santa Cruz", "Aranjuez", "Villa Hermosa"], "Comuna tradicional del nororiente, de barrios residenciales y comercio.",
                 ["Manrique Central", "La Salle", "Las Granjas", "Palermo", "El Pomar", "Campo Valdés", "Versalles", "Santa Inés", "Bello Oriente"]),
    "Aranjuez": ("Nororiente", ["Manrique", "Castilla", "Villa Hermosa", "La Candelaria"], "Comuna del nororiente cercana al centro, de barrios residenciales, comercio y universidades.",
                 ["Aranjuez", "Berlín", "Moravia", "Sevilla", "San Isidro", "Miranda", "Brasilia", "Las Esmeraldas"]),
    "Castilla": ("Noroccidente", ["Aranjuez", "Doce de Octubre", "Santa Cruz"], "Comuna residencial y comercial del noroccidente, con barrios de casas y conjuntos de apartamentos.",
                 ["Castilla", "Tricentenario", "Florencia", "Toscana", "Héctor Abad Gómez", "Belalcázar", "Caribe", "Boyacá"]),
    "Doce de Octubre": ("Noroccidente", ["Castilla", "Robledo", "Santa Cruz"], "Comuna del noroccidente, de barrios de ladera y vivienda familiar.",
                        ["Doce de Octubre", "Pedregal", "Kennedy", "Picacho", "Progreso", "El Triunfo", "Mirador del Doce", "Santander"]),
    "Robledo": ("Noroccidente", ["Doce de Octubre", "Castilla", "La América", "San Javier", "Laureles-Estadio"], "Gran comuna del noroccidente, con barrios residenciales, comercio y varias universidades.",
                ["Robledo", "Pilarica", "Aures", "El Diamante", "Bello Horizonte", "Villa Flora", "San Germán", "Fuente Clara", "Córdoba", "Altamira", "Villa Sofía"]),
    "Villa Hermosa": ("Centro", ["Manrique", "Aranjuez", "La Candelaria", "Buenos Aires"], "Comuna del centro-oriente, de barrios de ladera y vivienda tradicional.",
                      ["Villa Hermosa", "La Mansión", "Enciso", "Sucre", "Llanaditas", "Villa Turbay", "Los Ángeles", "La Ladera", "Golondrinas", "Villatina"]),
    "Buenos Aires": ("Centro", ["Villa Hermosa", "La Candelaria", "El Poblado"], "Comuna del centro-oriente, de barrios tradicionales, comercio y vivienda en ladera.",
                     ["Buenos Aires", "Caicedo", "Miraflores", "Loreto", "Los Cerros", "Ocho de Marzo", "Cataluña", "La Milagrosa", "Alejandro Echavarría"]),
    "La Candelaria": ("Centro", ["Aranjuez", "Villa Hermosa", "Buenos Aires", "Laureles-Estadio", "El Poblado"], "El centro de Medellín: comercio, oficinas, edificios y vivienda alrededor del Parque Berrío y la Plaza Botero.",
                      ["Centro", "Prado", "Boston", "San Benito", "Guayaquil", "Jesús Nazareno", "El Chagualo", "Perpetuo Socorro", "Villanueva"]),
    "Laureles-Estadio": ("Occidente", ["La Candelaria", "La América", "Robledo", "Belén"], "Zona residencial y comercial del occidente, de casas, edificios y comercio alrededor del Estadio Atanasio Girardot.",
                         ["Laureles", "Estadio", "Conquistadores", "Florida Nueva", "Los Colores", "Lorena", "Carlos E. Restrepo", "Bolivariana", "Suramericana", "Naranjal", "San Joaquín", "Santa Teresita", "Velódromo", "Las Acacias", "La Castellana"]),
    "La América": ("Occidente", ["Laureles-Estadio", "San Javier", "Robledo", "Belén"], "Comuna residencial del occidente, de casas, edificios y comercio de barrio.",
                   ["La América", "Ferrini", "Calasanz", "Santa Mónica", "La Floresta", "Santa Lucía", "Los Pinos"]),
    "San Javier": ("Occidente", ["La América", "Robledo", "Belén"], "Comuna del occidente de barrios de ladera, con vivienda familiar y comercio.",
                   ["San Javier", "El Salado", "Belencito", "Las Independencias", "La Divisa", "Veinte de Julio", "Juan XXIII", "Santa Rosa de Lima", "Betania", "El Pesebre", "Blanquizal"]),
    "Guayabal": ("Occidente", ["El Poblado", "Belén", "Laureles-Estadio", "La Candelaria"], "Comuna del suroccidente con comercio, industria liviana y vivienda, cerca del aeropuerto Olaya Herrera.",
                 ["Guayabal", "Cristo Rey", "Santa Fe", "Trinidad", "Campo Amor", "Tenche", "Shellmar"]),
    "Belén": ("Occidente", ["Guayabal", "La América", "San Javier", "Laureles-Estadio"], "Comuna del suroccidente, de barrios residenciales y comerciales, cerca del Cerro Nutibara.",
              ["Belén", "Rosales", "Fátima", "Los Alpes", "La Mota", "Las Playas", "Granada", "Rodeo Alto", "El Rincón", "San Bernardo", "Las Violetas", "Zafra", "Altavista", "Loma de los Bernal", "Cerro Nutibara"]),
    "El Poblado": ("Sur", ["Buenos Aires", "La Candelaria", "Guayabal"], "Comuna del suroriente, con edificios, centros comerciales, zonas de oficinas y barrios residenciales.",
                   ["Manila", "Provenza", "Astorga", "Lleras", "El Tesoro", "Los Balsos", "Castropol", "Patio Bonito", "La Florida", "Santa María de los Ángeles", "Alejandría", "Las Lomas", "San Lucas", "Aguacatala", "El Castillo", "Los Naranjos", "Villa Carlota"]),
}
MED_ZONAS = {"Nororiente": "nororiente", "Noroccidente": "noroccidente", "Centro": "centro", "Occidente": "occidente", "Sur": "sur"}
MED_POPULARES = ["Laureles", "Estadio", "Conquistadores", "Provenza", "Manila", "Astorga", "El Tesoro", "Los Balsos", "Belén", "Rosales", "La América", "Robledo", "Pilarica", "Castilla", "Tricentenario",
                 "Aranjuez", "Moravia", "Manrique Central", "Villa Hermosa", "Buenos Aires", "La Candelaria Centro", "Prado", "Guayabal", "Doce de Octubre", "Pedregal", "Santa Cruz", "Popular", "San Javier", "El Salado", "Betania"]
MED_CATS = {
    "barrios-exclusivos": ("Filtros Samsung en los barrios más exclusivos de Medellín", "barrios exclusivos y residenciales de Medellín",
                           ["Provenza", "Manila", "Astorga", "Lleras", "El Tesoro", "Los Balsos", "Castropol", "Patio Bonito", "La Florida", "Alejandría", "Las Lomas", "San Lucas", "Aguacatala", "Los Naranjos", "Villa Carlota",
                            "Laureles", "Estadio", "Conquistadores", "Florida Nueva", "Los Colores", "Lorena", "Carlos E. Restrepo", "Bolivariana", "Suramericana", "Naranjal", "San Joaquín", "Rosales", "La Mota", "Los Alpes", "Rodeo Alto"],
                           "En estos barrios abundan los apartamentos y las casas con nevecones de gama alta; entregamos hasta la portería o la puerta."),
    "barrios-populares": ("Filtros Samsung en los barrios populares de Medellín", "barrios populares del nororiente, noroccidente y occidente de Medellín",
                          ["Popular", "Santo Domingo Savio", "Villa Guadalupe", "Carpinelo", "Granizal", "Santa Cruz", "La Rosa", "Moscú", "Manrique Central", "Las Granjas", "Aranjuez", "Moravia", "Castilla", "Doce de Octubre", "Pedregal",
                           "Picacho", "Robledo", "Villa Flora", "Villa Hermosa", "Enciso", "Llanaditas", "San Javier", "El Salado", "Belencito", "Betania", "Blanquizal"],
                          "Entregamos en todos los barrios de Medellín, también en las zonas de ladera."),
}
MED_TEXTO_PORTADA = ("Filtros de agua para nevera Samsung en Medellín: el filtro HAF-CIN (DA29-00020B) y el HAF-QIN (DA97-17376B) cuestan $ 130.900 y el filtro externo DA29-10105J $ 96.900, con pack de 2 para ahorrar. "
                     "Tenemos bodega en el barrio Laureles, con pago seguro en línea (tarjeta, PSE, Nequi y Bancolombia) y entrega en 1 a 2 días hábiles en Medellín, de Popular a El Poblado y de Robledo a Belén.")

CIUDADES = {
    "Bogotá": dict(nombre="Bogotá", slug="bogota"),
    "Medellín": dict(nombre="Medellín", slug="medellin", sede_barrio="Laureles", sede_comuna="Laureles-Estadio", sede_zona="el occidente", region="Antioquia", n_comunas=len(MED_LOC)),
}


def activar(ciudad):
    """Carga los datos de la ciudad en el generador local (comunas/localidades, barrios, zonas, listas)."""
    if ciudad == "Medellín":
        bogota_seo.LOCALIDADES, bogota_seo.ZONAS, bogota_seo.POPULARES, bogota_seo.CATS_OVERRIDE, bogota_seo.TEXTO_PORTADA = MED_LOC, MED_ZONAS, MED_POPULARES, MED_CATS, MED_TEXTO_PORTADA
    else:
        bogota_seo.LOCALIDADES, bogota_seo.ZONAS, bogota_seo.POPULARES, bogota_seo.CATS_OVERRIDE, bogota_seo.TEXTO_PORTADA = (ORIGINAL[k] for k in ("LOCALIDADES", "ZONAS", "POPULARES", "CATS", "TEXTO_PORTADA"))


def traducir(t, ciudad):
    """Pasa un texto de la tienda de Bogotá a la tienda de otra ciudad."""
    if ciudad == "Bogotá":
        return t
    c = CIUDADES[ciudad]
    barrio, comuna, zona, region, n = c["sede_barrio"], c["sede_comuna"], c["sede_zona"], c["region"], c["n_comunas"]
    reglas = [
        ('"addressRegion": "Bogotá D.C."', f'"addressRegion": "{region}"'),
        ("Cedritos, Usaquén, Bogotá D.C.", f"{barrio}, {c['nombre']}"),
        ("Cedritos, Usaquén, Bogotá", f"{barrio}, {c['nombre']}"),
        ("Cedritos, Usaquén", barrio),
        ("en la localidad de Usaquén, al norte de Bogotá", f"en la comuna {comuna}, en {zona} de {c['nombre']}"),
        ("en la localidad de Usaquén", f"en la comuna {comuna}"),
        ("en Usaquén", f"en la comuna {comuna}"),
        ("Usaquén", comuna),
        ("Cedritos", barrio),
        ("cedritos", slug_(barrio)),
        ("Bogotá D.C.", c["nombre"]),
        ("Bogot%C3%A1", "Medell%C3%ADn"),
        ("Bogotá", c["nombre"]),
        ("bogota", c["slug"]),
        ("norte, centro, occidente y sur, y en los municipios cercanos", "nororiente, noroccidente, centro, occidente y sur"),
        ("norte, centro, occidente y sur", "nororiente, noroccidente, centro, occidente y sur"),
        (" y a los municipios cercanos", ""),
        ("19 localidades urbanas", f"{n} comunas"),
        ("19 localidades", f"{n} comunas"),
        ("localidades", "comunas"), ("Localidades", "Comunas"), ("localidad", "comuna"), ("Localidad", "Comuna"),
    ]
    for a, b in reglas:
        t = t.replace(a, b)
    return t


def slug_(n):
    import unicodedata
    n = unicodedata.normalize("NFKD", n).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", n).strip("-")


def postproceso(dir_, ciudad):
    """Traduce el sitio ya generado: contenido de los archivos y nombres de carpetas/archivos."""
    if ciudad == "Bogotá":
        return 0
    n = 0
    for f in sorted(pathlib.Path(dir_).rglob("*")):
        if f.is_file() and f.suffix.lower() in (".php", ".js", ".json", ".txt", ".xml", ".html", ".htaccess", ".md", ".webmanifest", ".css") or f.name == ".htaccess":
            try:
                t = f.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            u = traducir(t, ciudad)
            if u != t:
                f.write_text(u, encoding="utf-8")
                n += 1
    # nombres: de las rutas más profundas hacia arriba
    for f in sorted(pathlib.Path(dir_).rglob("*"), key=lambda p: len(p.parts), reverse=True):
        nuevo = traducir(f.name, ciudad)
        if nuevo != f.name and f.exists():
            f.rename(f.with_name(nuevo))
    return n
