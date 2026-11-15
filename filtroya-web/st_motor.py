# Motor de contenido: bancos de frases y consejos para que cada ciudad, zona y servicio tenga texto propio (se ejecuta dentro de st_samsung.py).
import itertools
from st_guias import _ul, _ol, _h
from st_clima import CLIMA, VOLT, EFECTO, tipo_riesgo


def mix(clave, lista, k=1):
    """k elementos distintos de la lista, elegidos de forma determinista por la clave."""
    r = random.Random(int(hashlib.md5(clave.encode()).hexdigest()[:10], 16))
    l = list(lista)
    r.shuffle(l)
    return l[:k]


def uno(clave, lista):
    return mix(clave, lista, 1)[0]


INTRO_Z = [
    "Si vives en {z} ({c}) no tienes que mover tu electrodoméstico Samsung: el técnico llega a tu casa o apartamento y lo revisa ahí mismo.",
    "Cubrimos {z} dentro de nuestra atención en {c}: coordinas por WhatsApp, te confirmamos el día y el técnico hace el diagnóstico en el lugar.",
    "En {z}, {c}, damos servicio a domicilio para línea blanca Samsung: neveras, lavadoras, secadoras y más.",
    "{z} forma parte de las zonas de {c} que visitamos. Escríbenos con el equipo, el modelo y la falla, y agendamos la visita.",
    "¿Tu Samsung falló en {z}? Cuéntanos qué le pasa y un técnico va a revisar el equipo en tu hogar en {c}.",
    "Atender un electrodoméstico en {z} es sencillo: nos escribes, coordinamos la visita y te confirmamos el valor antes de reparar.",
    "Llegamos a {z} y a los sectores cercanos de {c} con visita técnica a domicilio para equipos Samsung.",
    "Para quienes viven o trabajan en {z} ({c}), revisamos y reparamos línea blanca Samsung sin que tengas que llevar el equipo a un taller.",
]
CLIMA_Z = [
    "Conviene tener presente que en {c}, con un clima {clima}, {efecto}.",
    "Las lluvias {ll} y el clima {clima} de {c} hacen que {efecto}.",
    "{rasgo}: ese es el contexto de {c}, y por eso {efecto}.",
    "Piensa en el entorno de {z}: {rasgo}. En ese contexto, {efecto}.",
    "A unos {alt} metros sobre el nivel del mar, {c} tiene un clima {clima}; por eso {efecto}.",
    "En {c} el clima es {clima}, con lluvias {ll}. Para tu equipo eso significa que {efecto}.",
]
TIPS = {
    "nevera": ["Separa la nevera de la pared unos centímetros y limpia el polvo del condensador cada seis meses: un condensador sucio obliga al compresor a trabajar de más.",
               "Si el congelador acumula escarcha o la nevera gotea por dentro, revisa primero los sellos de las puertas antes de sospechar del compresor.",
               "No llenes la nevera hasta tapar las rejillas de aire: el flujo de aire frío es lo que mantiene la temperatura pareja.",
               "Un ruido nuevo y repetitivo suele avisar de un ventilador con problemas; pide revisión antes de perder alimentos.",
               "Si la fábrica de hielo deja de producir, revisa el filtro de agua y la llave antes de llamar al técnico.",
               "Evita abrir la puerta por largos periodos y no guardes comida caliente: aumentan la escarcha y el consumo."],
    "lava": ["Deja la puerta entreabierta después de cada lavado para que el sello se seque y no aparezcan hongos ni mal olor.",
             "Si el panel muestra un código de error (4E, 5E, UE, dE, LE), anótalo antes de escribirnos: ayuda a acortar el diagnóstico.",
             "No sobrecargues el tambor: las cargas pesadas desgastan amortiguadores y rodamientos.",
             "Limpia de vez en cuando el filtro de la bomba de desagüe; monedas, botones y pelusa son la causa más común de que no desagüe.",
             "Usa la cantidad correcta de detergente: el exceso deja residuos, espuma de más y malos olores.",
             "Mantén la lavadora nivelada: una patas desniveladas hacen vibrar el equipo y fuerzan el tambor."],
    "seca": ["Limpia el filtro de pelusa en cada carga: un filtro tapado alarga el secado y sobrecalienta la resistencia.",
             "Revisa que el ducto de salida no esté doblado ni obstruido; la pelusa acumulada es un riesgo de recalentamiento.",
             "No mezcles prendas muy mojadas: centrifuga bien en la lavadora antes de pasar la ropa a la secadora.",
             "Deja ventilado el lugar de la secadora; sin aire fresco el ciclo se alarga y el equipo se calienta de más.",
             "Si la secadora tarda cada vez más, no sigas alargando ciclos: puede ser un sensor o la resistencia."],
    "lavaplatos": ["Limpia el filtro del fondo con frecuencia: los restos de comida son la causa más común de mal olor y de que no desagüe.",
                   "No sobrecargues los canastos; los brazos rociadores deben girar libres para lavar bien.",
                   "Raspa los platos pero no los enjuagues del todo: el detergente trabaja mejor con algo de suciedad.",
                   "Si ves sarro blanco en los vasos, puede haber minerales en el agua: pregunta por el uso de sal regeneradora o abrillantador según el modelo.",
                   "Ejecuta de vez en cuando un ciclo en vacío con limpiador para eliminar grasa y olores."],
    "cocina": ["Limpia los quemadores y el chispero: la grasa y los derrames son la causa más frecuente de que una hornilla no encienda bien.",
               "Si la llama sale amarilla o irregular, apaga y pide revisión; puede faltar ajuste de aire.",
               "No cubras el piso del horno con papel de aluminio sin revisar el manual; puede dañar el esmalte o la resistencia.",
               "Si el horno calienta de más o de menos, el sensor de temperatura puede estar fallando.",
               "Revisa el empaque de la puerta del horno: si está roto se pierde calor y se gasta más energía."],
    "micro": ["No lo uses vacío: sin alimento el magnetrón se sobrecalienta y se daña.",
              "Nunca metas metal ni recipientes con filo metálico; las chispas dañan la cavidad.",
              "Limpia la guía y el plato giratorio: la suciedad hace que gire mal o haga ruido.",
              "Si la puerta no cierra bien, deja de usarlo y pide revisión; los seguros son parte de la seguridad del equipo.",
              "Si gira pero no calienta, no lo abras: hay componentes con alto voltaje incluso desconectado."],
    "tv": ["Deja espacio alrededor del televisor para que ventile; el calor acumulado acorta la vida de la retroiluminación.",
           "Usa un protector de voltaje: los picos son la causa más común de fuentes de poder quemadas.",
           "Limpia la pantalla con un paño de microfibra seco o apenas húmedo; evita limpiadores con alcohol o amoníaco.",
           "Si la imagen se ve oscura o parpadea, no esperes a que se apague del todo: la retroiluminación puede estar fallando.",
           "Si no enciende, prueba otro tomacorriente y desconéctalo un minuto antes de pensar en una falla mayor."],
}
VISITA = [
    ["Escríbenos por WhatsApp con el equipo, el modelo (está en una etiqueta) y la falla.", "Te confirmamos el día y la franja de la visita en {z}.", "El técnico revisa el equipo en tu casa y te dice qué tiene.", "Te confirmamos el valor antes de reparar; si aceptas, se repara."],
    ["Cuéntanos qué le pasa a tu Samsung y envía una foto de la etiqueta del modelo.", "Coordinamos la visita para tu dirección en {z}, {c}.", "El diagnóstico se hace en el lugar, con tu equipo funcionando o no.", "Con el valor claro, decides si repararlo en la misma visita."],
    ["Pide tu visita por WhatsApp o con el formulario de la página.", "Agendamos día y hora para {z}.", "El técnico llega, revisa y te explica la falla en palabras simples.", "Repara con tu aprobación y deja el equipo funcionando."],
]
FAQ_Z = [
    ("¿Atienden en {z}?", "Sí, atendemos {z} y los sectores cercanos de {c} con visita a domicilio."),
    ("¿Cuánto tarda en llegar el técnico a {z}?", "Depende de la agenda del día; al escribirnos te confirmamos la fecha y la franja disponible para {z}."),
    ("¿Reparan en edificios y conjuntos cerrados de {z}?", "Sí. Solo necesitamos que la administración o la portería autorice el ingreso del técnico."),
    ("¿Qué equipos Samsung puedo pedir que revisen en {z}?", "{equipos}."),
    ("¿Cobran por la visita en {z}?", "Las condiciones de la visita y del diagnóstico se confirman al agendar; el valor de la reparación se te informa antes de realizarla."),
    ("¿Puedo mandar fotos antes de que vayan a {z}?", "Sí, por WhatsApp puedes enviar fotos o un video corto de la falla y de la etiqueta del modelo."),
    ("¿Atienden equipos con código de error?", "Sí. Anota el código que muestra el panel y escríbenoslo; ayuda a preparar la visita."),
    ("¿Dan servicio a casas y apartamentos en {z}?", "Atendemos viviendas y apartamentos; para locales y negocios coordinamos según el equipo."),
    ("¿Puedo pedir la visita para otro día?", "Sí; al escribirnos acordamos el día y la franja que mejor te sirva."),
]
FAQ_CS = [
    ("¿Qué {s1} Samsung atienden en {c}?", "{lineas}."),
    ("¿Qué revisa el técnico primero en una {s1} que falla en {c}?", "{revisa1}, y después {revisa2}."),
    ("¿Puedo pedir la revisión de mi {s1} Samsung por la tarde en {c}?", "Al escribirnos acordamos el día y la franja disponible en {c}."),
    ("¿Qué datos debo enviar para agilizar la visita en {c}?", "El modelo (etiqueta del equipo), la falla y, si el panel muestra un código, el código."),
    ("¿Arreglan una {s1} Samsung que ya está fuera de garantía en {c}?", "Sí, atendemos equipos dentro y fuera de garantía; el valor se confirma tras el diagnóstico."),
    ("¿Vale la pena reparar mi {s1} Samsung en {c}?", "Depende de la falla y de la edad del equipo; el técnico te orienta en el diagnóstico antes de que decidas."),
]


def ctx_ciudad(c):
    cl = CLIMA[c["s"]]
    r = tipo_riesgo(cl)
    return cl, r


def efecto_de(c, sv):
    cl, r = ctx_ciudad(c)
    return EFECTO[r][sv]


def parrafo_clima(c, z, sv, clave):
    cl, _ = ctx_ciudad(c)
    return uno(clave, CLIMA_Z).format(c=c["n"], z=z, clima=cl["clima"], ll=cl["lluvia"], alt=f"{cl['alt']:,}".replace(",", "."), rasgo=cl["rasgo"][:1].upper() + cl["rasgo"][1:], efecto=efecto_de(c, sv))


def bloque_local(c, sv, clave):
    """Sección «Clima y equipo» + consejo del técnico, distinta en cada ciudad y equipo."""
    s1, s2 = pal(c["pk"], sv)
    tip = uno(clave + "|tip", TIPS[sv])
    return seccion(f"{esc(cap(s2))} Samsung y el clima de {esc(c['n'])}", f"<p>{esc(parrafo_clima(c, c['zonas'][0], sv, clave + '|cl'))}</p><p><b>Consejo del técnico:</b> {esc(tip)}</p>", alt=True)


def faq_cs(c, sv):
    S = SERVICIOS[sv]; s1, s2 = pal(c["pk"], sv)
    f = {"s1": s1, "s2": s2, "c": c["n"], "lineas": S["lineas"].capitalize(), "revisa1": S["revisa"][0], "revisa2": S["revisa"][1]}
    return [(q.format(**f), a.format(**f)) for q, a in mix(f"fq|{c['s']}|{sv}", FAQ_CS, 3)]


R_Z = lambda c, z: f"servicio-tecnico-samsung-{slug(z)}-{c['s']}.html"
R_MANT = lambda c: f"mantenimiento-electrodomesticos-samsung-{c['s']}.html"
R_VOLT = lambda pk: f"voltaje-electrodomesticos-samsung-{pk}.html"
