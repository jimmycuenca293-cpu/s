# Motor de contenido: bancos de frases y consejos para que cada ciudad, zona y servicio tenga texto propio (se ejecuta dentro de st_samsung.py).
import itertools
from st_guias import _ul, _ol, _h, AVISO
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


def alt_txt(cl):
    return f"{cl['alt']:,}".replace(",", ".") if cl.get("alt") else ""


def parrafo_clima(c, z, sv, clave):
    cl, _ = ctx_ciudad(c)
    pool = CLIMA_Z if cl.get("alt") else [x for x in CLIMA_Z if "{alt}" not in x]
    return uno(clave, pool).format(c=c["n"], z=z, clima=cl["clima"], ll=cl["lluvia"], alt=alt_txt(cl), rasgo=cl["rasgo"][:1].upper() + cl["rasgo"][1:], efecto=efecto_de(c, sv))


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


def zlink(c, z, texto=None):
    t = esc(texto or z)
    return f'<a href="{R_Z(c, z)}">{t}</a>' if c.get("zp", True) else f"<span>{esc(z)}</span>"


def nota_amp(c):
    return (f" En {c['n']} la cobertura es ampliada: coordinamos la visita según la disponibilidad del técnico, así que escríbenos con anticipación." if c.get("amp") else "")


MITOS = {
    "nevera": [("Poner la nevera al máximo frío la enfría más rápido.", "Solo gasta más energía y puede congelar los alimentos del refrigerador; usa el nivel recomendado."), ("Si la nevera hace ruido, siempre es el compresor.", "Muchas veces es el ventilador del evaporador con hielo o un tubo que roza; un técnico lo distingue en minutos."),
               ("La escarcha es normal y no importa.", "Una capa fina sí; mucha escarcha suele indicar sellos dañados o falla en el deshielo.")],
    "lava": [("Más detergente lava mejor.", "El exceso deja residuos, espuma de más y malos olores."), ("Un código de error siempre significa que hay que cambiar la tarjeta.", "La mayoría de códigos (4E, 5E, UE, dE, LE) apuntan a algo sencillo: agua, desagüe, carga o puerta."),
             ("Cerrar la puerta tras lavar protege la lavadora.", "Al contrario: cerrada atrapa humedad y favorece el moho; déjala entreabierta.")],
    "seca": [("Un ciclo más largo seca mejor.", "Si el filtro o el ducto están tapados, alargar el ciclo solo gasta energía."), ("Si no calienta, hay que cambiarla.", "A menudo es un sensor, un filtro tapado o la resistencia; se repara sin cambiar el equipo.")],
    "lavaplatos": [("Hay que enjuagar todo a mano antes de cargar.", "Raspar los restos basta; enjuagar del todo reduce la eficacia del detergente."), ("Si queda agua en el fondo, el equipo está dañado.", "Casi siempre es el filtro o la manguera de desagüe; se resuelve con limpieza o una revisión rápida.")],
    "cocina": [("Una llama amarilla es normal.", "Puede indicar mala mezcla de aire; conviene una revisión."), ("Si el horno no calienta, hay que cambiarlo.", "Muchas veces es la resistencia o el sensor de temperatura; se repara.")],
    "micro": [("Se puede calentar vacío un rato sin problema.", "Sin alimento el magnetrón se sobrecalienta y se daña."), ("Si gira pero no calienta, basta cambiar el plato.", "El problema suele estar en el magnetrón, el diodo o el condensador, no en el plato.")],
    "tv": [("Dejar el televisor en espera siempre es inofensivo.", "Los picos de voltaje pueden dañar la fuente aunque esté apagado; usa protector."), ("Si hay sonido pero no imagen, el panel está perdido.", "Muy a menudo es la retroiluminación, que se repara.")],
}
ANTES = ["Anota el modelo y el número de serie de la etiqueta del equipo.", "Toma una foto o un video corto de la falla.", "Anota el código de error si el panel lo muestra.", "Desconecta el equipo si hay agua, chispas u olor a quemado.", "Ten a mano la dirección exacta y un teléfono de contacto.",
         "Cuéntanos desde cuándo falla y si pasó algo antes (tormenta, mudanza, corte de luz).", "Mueve lo que haya alrededor para que el técnico pueda acceder al equipo.", "Revisa que el equipo esté conectado a un tomacorriente que funcione.", "Si es una lavadora o lavavajillas, ten a la mano las llaves de agua.",
         "Si vives en conjunto o edificio, avisa a la portería de la visita.", "Despeja el espacio frente al equipo para trabajar con comodidad.", "Ten a la mano la factura o la fecha de compra si la tienes.", "Si la falla es intermitente, anota cuándo ocurre.", "Mantén a las mascotas y a los niños alejados del área de trabajo."]
AIQ = [("¿Dónde reparar una {nev} Samsung en {c}?", "Con visita a domicilio: escribe por WhatsApp al {wa}, hacemos el diagnóstico y te confirmamos el valor antes de reparar."),
       ("¿Quién arregla {lavs} Samsung a domicilio en {c}?", "Nuestros técnicos van a tu casa en {c}. Coordinas por WhatsApp ({wa}) y se revisa el equipo en tu hogar."),
       ("¿Cuánto cuesta un técnico para una Samsung en {c}?", "Depende de la falla y del repuesto. Se hace el diagnóstico y el valor se confirma antes de reparar."),
       ("¿Cómo pido un técnico Samsung en {c} por WhatsApp?", "Escribe al {wa} con el equipo, el modelo y la falla; coordinamos el día y el técnico va a tu dirección."),
       ("¿Qué electrodomésticos Samsung reparan en {c}?", "{equipos}."),
       ("¿Un técnico Samsung independiente puede reparar equipos con garantía?", "Esto depende de las condiciones de tu garantía; consúltalas en el manual del equipo. Para equipos sin garantía, reparamos con diagnóstico previo."),
       ("¿Tienen servicio técnico Samsung en {c} los fines de semana?", "La disponibilidad se confirma al escribirnos; acordamos el día que mejor te sirva."),
       ("¿Qué debo tener listo para la visita en {c}?", "El modelo del equipo, una descripción de la falla y la dirección exacta.")]


def bloque_mitos(clave, svs, n=2):
    pares = [(sv, m) for sv in svs for m in MITOS.get(sv, [])]
    sel = mix(clave + "|mt", pares, n)
    items = "".join(f"<li><b>Mito:</b> {esc(m[0])}<br><b>Verdad:</b> {esc(m[1])}</li>" for sv, m in sel)
    ant = "".join(f"<li>{esc(x)}</li>" for x in mix(clave + "|an", ANTES, 3))
    return seccion("Mitos y verdades", f'<ul class="spec-list">{items}</ul><h3 style="margin:18px 0 8px">Antes de llamar, ten listo</h3><ul class="spec-list">{ant}</ul>')


def preguntas_ia(c, clave, k=4):
    pk = c["pk"]; svs = SERV_PAIS[pk]
    f = dict(c=c["n"], nev=pal(pk, "nevera")[1], lavs=pal(pk, "lava")[1], wa=wa_vis(pk), equipos=cap(", ".join(pal(pk, s)[1] for s in svs)))
    return [(q.format(**f), a.format(**f)) for q, a in mix(clave + "|ai", AIQ, k)]


# fondos de encabezado (fotos reales) por tipo de página
HERO_FOTOS = ["portada-tecnico", "tecnico-neveras", "stp1", "stp3", "stp5", "stp7", "c-revision", "c-compresor", "stp2", "stp4"]
HERO_SV = {"nevera": ["tecnico-neveras", "stp1", "stp4"], "lava": ["tecnico-lavadora", "stp6"], "seca": ["stp2", "c-revision"]}
PLURAL_SV = {slug(pal(k, sv)[1]): sv for k in PAISES for sv in SERV_PAIS[k]}


def hero_img(nombre):
    m = re.match(r"reparacion-(.+?)-samsung-", nombre)
    if m and PLURAL_SV.get(m.group(1)) in HERO_SV:
        return uno(nombre + "|h", HERO_SV[PLURAL_SV[m.group(1)]])
    return uno(nombre + "|h", HERO_FOTOS)


def mezclar_secciones(cuerpo, clave):
    """Reordena las secciones intermedias de forma distinta en cada página (misma información, estructura diferente)."""
    partes = [x for x in re.split(r"(?=<section class=)", cuerpo) if x]
    hero = [x for x in partes if x.startswith('<section class="hero')]
    qa_ = [x for x in partes if 'aq-qa-sec' in x[:40]]
    faq = [x for x in partes if 'class="faq-num"' in x]
    cola = [x for x in partes if re.search(r"<h2>(Zonas cercanas|Más información|Otros equipos)", x[:300])]
    usados = hero + qa_ + faq + cola
    mid = [x for x in partes if x not in usados]
    random.Random(int(hashlib.md5(clave.encode()).hexdigest()[:8], 16)).shuffle(mid)
    mid = [x.replace('class="aq-sec alt"', 'class="aq-sec"', 1) for x in mid]
    mid = [x.replace('class="aq-sec"', 'class="aq-sec alt"', 1) if i % 2 else x for i, x in enumerate(mid)]
    return "".join(hero + qa_ + mid + faq + cola)


# ------------------------------------------------------------------ fragmentos destacados: respuestas de 40 a 55 palabras + pasos + tabla
SNIP_Q = [("¿Cuánto cuesta un técnico Samsung en {c}?", "El costo depende de la falla y del repuesto. En {c} primero se hace el diagnóstico en tu casa y el valor de la reparación se te confirma antes de empezar, de modo que sepas cuánto vas a pagar antes de aceptar. Escríbenos por WhatsApp al {wa} con el modelo y la falla."),
          ("¿Cómo pedir un técnico Samsung a domicilio en {c}?", "Escribe por WhatsApp al {wa} con el equipo, el modelo (está en la etiqueta) y la falla. Coordinamos el día y la franja, el técnico llega a tu dirección en {c}, revisa el equipo y te confirma el valor antes de repararlo."),
          ("¿Cuánto demora la visita de un técnico Samsung en {c}?", "El tiempo depende de la agenda del día y de la zona de {c}. Al escribirnos por WhatsApp ({wa}) te confirmamos la fecha y la franja disponibles, y puedes adelantar el diagnóstico enviando fotos o un video corto de la falla."),
          ("¿Qué electrodomésticos Samsung reparan en {c}?", "En {c} reparamos {equipos} Samsung, con visita a domicilio. Atendemos equipos dentro y fuera de garantía; el diagnóstico es primero y el valor se confirma antes de reparar."),
          ("¿Vale la pena reparar una Samsung en {c} o es mejor cambiarla?", "Depende de la falla y de la edad del equipo. Muchas fallas (sellos, ventiladores, sensores, bombas, filtros) se reparan a un costo razonable. El técnico te orienta en el diagnóstico y tú decides si repararla o no."),
          ("¿Un técnico independiente puede reparar mi Samsung?", "Sí, para equipos fuera de garantía. Si tu equipo aún tiene garantía, revisa sus condiciones en el manual antes de intervenir. En {c} reparamos con diagnóstico previo y valor confirmado antes de la reparación.")]
PASOS4 = [["Escríbenos por WhatsApp con el equipo, el modelo y la falla.", "Confirma el día y la franja de la visita.", "El técnico revisa el equipo en tu casa y te explica qué tiene.", "Aprueba el valor y se repara; el equipo se prueba contigo."],
          ["Cuéntanos qué le pasa a tu Samsung y envía una foto de la etiqueta.", "Elige el día que mejor te sirva.", "Recibe al técnico y mira el diagnóstico.", "Decide si reparar con el valor ya confirmado."],
          ["Pide la visita por WhatsApp o con el formulario.", "Acordamos hora y dirección.", "El técnico diagnostica en el lugar.", "Reparamos con tu aprobación y probamos el equipo."]]


def bloque_snippets(c, clave, n=3, tabla=True):
    pk = c["pk"]; f = dict(c=c["n"], wa=wa_vis(pk), equipos=", ".join(pal(pk, s)[1] for s in SERV_PAIS[pk]))
    qs = "".join(f"<h3>{esc(q.format(**f))}</h3><p>{esc(a.format(**f))}</p>" for q, a in mix(clave + "|sq", SNIP_Q, n))
    pasos = '<h3>Cómo pedir la visita en 4 pasos</h3><ol class="vl">' + "".join(f"<li>{esc(x)}</li>" for x in uno(clave + "|p4", PASOS4)) + "</ol>"
    tb = ""
    if tabla:
        filas = "".join(f'<tr><td>{esc(cap(pal(pk, sv)[1]))}</td><td>{esc(SERVICIOS[sv]["sintomas"][i % len(SERVICIOS[sv]["sintomas"])])}</td><td>{esc(SERVICIOS[sv]["revisa"][i % len(SERVICIOS[sv]["revisa"])])}</td></tr>' for i, sv in enumerate(SERV_PAIS[pk]))
        tb = f'<h3>Equipos, fallas frecuentes y qué se revisa en {esc(c["n"])}</h3><div class="tbl-wrap"><table class="spec-table"><tr><th>Equipo Samsung</th><th>Falla frecuente</th><th>Qué revisa el técnico</th></tr>{filas}</table></div>'
    return seccion(f"Preguntas rápidas sobre el servicio técnico Samsung en {esc(c['n'])}", qs + pasos + tb)
