# Perfil técnico de cada ciudad (clima, altitud, lluvias, electricidad). Son datos generales y verificables; sirven para escribir contenido distinto en cada página.
VOLT = {  # país → (voltaje, frecuencia, enchufes)
    "colombia": ("110-120 V", "60 Hz", "tipo A y B"), "panama": ("110-120 V", "60 Hz", "tipo A y B"), "costa-rica": ("120 V", "60 Hz", "tipo A y B"), "paraguay": ("220 V", "50 Hz", "tipo C"),
    "guatemala": ("120 V", "60 Hz", "tipo A y B"), "el-salvador": ("115-120 V", "60 Hz", "tipo A y B"), "ecuador": ("120 V", "60 Hz", "tipo A y B"), "chile": ("220-230 V", "50 Hz", "tipo C y L"),
}
# slug de ciudad → perfil
CLIMA = {
    "cali": dict(alt=1000, clima="cálido, con temperaturas medias de 24 a 30 °C", lluvia="de marzo a mayo y de octubre a noviembre", hum="media", rasgo="tardes calurosas y brisa del Pacífico", riesgo="calor sostenido"),
    "medellin": dict(alt=1500, clima="templado, con una media cercana a los 22 °C", lluvia="de abril a mayo y de octubre a noviembre", hum="media", rasgo="un valle con lluvias de tarde frecuentes", riesgo="lluvias de tarde y tormentas eléctricas"),
    "bogota": dict(alt=2600, clima="frío de montaña, con una media de unos 14 °C", lluvia="de marzo a mayo y de septiembre a noviembre", hum="media", rasgo="altura de unos 2.600 metros y noches frías", riesgo="altura (afecta a las estufas a gas) y cambios fuertes de temperatura"),
    "ibague": dict(alt=1250, clima="cálido, con temperaturas altas durante el día", lluvia="de marzo a mayo y de septiembre a noviembre", hum="media", rasgo="días calurosos al pie de la cordillera", riesgo="calor sostenido"),
    "cartagena": dict(alt=2, clima="tropical caribe, caluroso y húmedo todo el año", lluvia="de mayo a noviembre, con el pico en octubre", hum="alta", rasgo="brisa marina y salitre", riesgo="humedad y salitre (corrosión de placas y conectores)"),
    "barranquilla": dict(alt=18, clima="tropical caribe, caluroso y húmedo", lluvia="de septiembre a noviembre", hum="alta", rasgo="calor intenso y brisa del río y del mar", riesgo="humedad, calor y arroyos de lluvia que causan cortes de energía"),
    "bucaramanga": dict(alt=960, clima="cálido y seco-húmedo, entre 22 y 30 °C", lluvia="de marzo a mayo y de septiembre a noviembre", hum="media", rasgo="una ciudad de cañón con tardes calurosas", riesgo="calor sostenido"),
    "giron": dict(alt=780, clima="cálido, un poco más caluroso que Bucaramanga", lluvia="de marzo a mayo y de septiembre a noviembre", hum="media", rasgo="un casco histórico con barrios nuevos alrededor", riesgo="calor sostenido"),
    "piedecuesta": dict(alt=1000, clima="templado-cálido, con noches frescas", lluvia="de marzo a mayo y de septiembre a noviembre", hum="media", rasgo="zonas campestres y conjuntos residenciales", riesgo="polvo y variaciones de voltaje en zonas campestres"),
    "floridablanca": dict(alt=950, clima="cálido y seco-húmedo", lluvia="de marzo a mayo y de septiembre a noviembre", hum="media", rasgo="conjuntos cerrados y edificios en altura", riesgo="calor sostenido"),
    "pereira": dict(alt=1400, clima="templado, con lluvias frecuentes", lluvia="de marzo a mayo y de septiembre a noviembre", hum="alta", rasgo="un clima húmedo en el Eje Cafetero", riesgo="humedad (hongos en sellos y tambores)"),
    "armenia": dict(alt=1480, clima="templado y húmedo", lluvia="de marzo a mayo y de septiembre a noviembre", hum="alta", rasgo="humedad constante en el Eje Cafetero", riesgo="humedad (hongos en sellos y tambores)"),
    "manizales": dict(alt=2150, clima="fresco de montaña, con neblina frecuente", lluvia="casi todo el año, con picos de marzo a mayo y octubre a noviembre", hum="alta", rasgo="neblina, pendientes y humedad", riesgo="humedad alta y frío (condensación dentro de los equipos)"),
    "ciudad-de-panama": dict(alt=10, clima="tropical, caluroso y muy húmedo", lluvia="de mayo a diciembre", hum="alta", rasgo="aire acondicionado casi permanente y torres de apartamentos", riesgo="humedad y uso continuo del aire acondicionado (la red eléctrica trabaja al límite)"),
    "san-jose": dict(alt=1170, clima="templado, con una estación seca y una lluviosa bien marcadas", lluvia="de mayo a noviembre", hum="media", rasgo="valle central con tormentas eléctricas en la tarde", riesgo="tormentas eléctricas (picos de voltaje)"),
    "asuncion": dict(alt=60, clima="cálido y húmedo, con veranos muy calurosos", lluvia="durante todo el año, con más lluvia de octubre a abril", hum="alta", rasgo="veranos extremos y tormentas fuertes", riesgo="calor extremo, humedad y variaciones de voltaje en tormentas"),
    "ciudad-de-guatemala": dict(alt=1500, clima="templado, de eterna primavera", lluvia="de mayo a octubre", hum="media", rasgo="valle de altura con lluvias fuertes de tarde", riesgo="tormentas eléctricas y cortes de luz en época de lluvias"),
    "san-salvador": dict(alt=650, clima="cálido, con una estación seca y una lluviosa", lluvia="de mayo a octubre", hum="media", rasgo="un valle caluroso con tormentas tropicales", riesgo="tormentas y picos de voltaje"),
    "quito": dict(alt=2850, clima="fresco de altura, con una media de unos 15 °C", lluvia="de octubre a mayo", hum="media", rasgo="altura de unos 2.850 metros y cambios bruscos de temperatura en el día", riesgo="altura (afecta a las estufas a gas) y aire seco"),
    "guayaquil": dict(alt=4, clima="tropical, caluroso y húmedo", lluvia="de enero a abril", hum="alta", rasgo="calor intenso y humedad del estuario", riesgo="humedad y calor (corrosión y sobrecarga de compresores)"),
    "santiago-de-chile": dict(alt=520, clima="mediterráneo, con veranos secos y calurosos e inviernos fríos", lluvia="de mayo a agosto", hum="baja", rasgo="inviernos lluviosos en los que se usa mucho la secadora", riesgo="invierno (uso intensivo de secadoras) y aguas con alto contenido de minerales en algunos sectores"),
}

# Qué le pasa a cada tipo de equipo según el riesgo del clima
EFECTO = {
    "humedad": {"nevera": "la humedad forma condensación en los sellos de las puertas y favorece la escarcha en el congelador",
                "lava": "la humedad deja hongos y mal olor en el sello de la puerta y en el tambor, y corroe los conectores de la tarjeta",
                "seca": "la humedad ambiental hace que la secadora tarde más y que se acumule pelusa húmeda en el filtro y el ducto",
                "lavaplatos": "la humedad corroe contactos y favorece olores en el fondo del equipo",
                "cocina": "la humedad afecta a los encendedores (chispero) y al panel electrónico del horno",
                "micro": "la humedad y el salitre dañan el panel y los contactos internos",
                "tv": "la humedad provoca fallas en los puertos y en la tarjeta principal"},
    "calor": {"nevera": "con calor sostenido el compresor trabaja más tiempo y se desgasta antes si el condensador acumula polvo",
              "lava": "el calor y el uso continuo exigen más a la bomba de desagüe y al motor",
              "seca": "con calor ambiente la secadora necesita buena ventilación o se sobrecalienta",
              "lavaplatos": "el calor reseca los empaques y favorece los olores",
              "cocina": "el calor de la cocina estresa el panel y el ventilador del horno",
              "micro": "el calor de la cocina acorta la vida del magnetrón si no hay ventilación",
              "tv": "el calor acelera el desgaste de la retroiluminación"},
    "tormenta": {"nevera": "los picos de voltaje de las tormentas dañan la tarjeta electrónica y el compresor inverter",
                 "lava": "los picos de voltaje por tormentas dañan la tarjeta y el motor inverter",
                 "seca": "los picos de voltaje afectan a la tarjeta y a la resistencia",
                 "lavaplatos": "los picos de voltaje por tormentas dañan la tarjeta de control",
                 "cocina": "los picos de voltaje dañan el panel electrónico del horno",
                 "micro": "un pico de voltaje quema el fusible o la tarjeta del microondas",
                 "tv": "un pico de voltaje quema la fuente de poder"},
    "altura": {"nevera": "con aire más delgado el condensador disipa un poco peor, por eso conviene dejarlo bien ventilado",
               "lava": "el agua más fría de montaña alarga los ciclos y exige más al resistor de calentamiento",
               "seca": "con aire más delgado y frío el ciclo de secado es más lento",
               "lavaplatos": "el agua fría de montaña dificulta disolver el detergente",
               "cocina": "las estufas a gas pueden necesitar ajuste de la mezcla de aire por la altura",
               "micro": "el frío de montaña no suele afectarlo, pero la humedad de la cocina sí",
               "tv": "los cambios de temperatura generan condensación en los equipos recién encendidos"},
    "invierno": {"nevera": "en invierno trabaja menos, pero la puerta mal sellada deja entrar humedad",
                 "lava": "con el frío el agua de entrada llega más fría y los ciclos con agua caliente exigen más a la resistencia",
                 "seca": "en invierno la secadora trabaja casi todos los días y el filtro y el ducto se tapan más rápido",
                 "lavaplatos": "el agua con minerales deja sarro en las paredes y en la bomba",
                 "cocina": "el uso frecuente del horno en invierno desgasta resistencias y empaques",
                 "micro": "el uso diario exige revisar el plato giratorio y la puerta",
                 "tv": "más horas frente al televisor aceleran el desgaste de la retroiluminación"},
}


def tipo_riesgo(c):
    r = c["riesgo"]
    if "humedad" in r or "salitre" in r:
        return "humedad"
    if "altura" in r:
        return "altura"
    if "invierno" in r:
        return "invierno"
    if "tormenta" in r or "voltaje" in r:
        return "tormenta"
    return "calor"
