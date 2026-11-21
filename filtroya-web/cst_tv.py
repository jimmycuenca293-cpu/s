# -*- coding: utf-8 -*-
"""Datos de pantallas (televisores) para servicio-tecnico-costa-rica.com.
Mismo formato que cst_datos (M, EQ, BRANDS_ORDER) para reutilizar el generador de marcas."""

BRANDS_ORDER = ["samsung", "lg", "sony"]
EQ = {
    "tv-led": ("pantallas-led", "pantalla LED", "pantallas LED"),
    "tv-qled": ("pantallas-qled", "pantalla QLED", "pantallas QLED y Mini LED"),
    "tv-oled": ("pantallas-oled", "pantalla OLED", "pantallas OLED"),
}

# Fallas tipo: (síntoma, causa, qué revisamos, qué probar, cuándo llamar [ya|tec|vuelve])
ARQ = {
 "tv-led": [
  ("No enciende y la luz de espera parpadea o no se ve", "Fuente de poder dañada o placa principal en protección; los picos de voltaje suelen provocarlo.", "Medimos la salida de la fuente de poder y revisamos fusibles, condensadores y la placa principal.",
   "Desconecta la pantalla 10 minutos, mantén presionado 30 segundos el botón de encendido del propio equipo (no del control) y prueba otro tomacorriente sin regleta.", "vuelve"),
  ("Enciende y hay sonido, pero la imagen es muy oscura o no se ve", "Retroiluminación LED dañada o driver de LED con falla.", "Con una linterna sobre la pantalla vemos si hay imagen tenue y medimos las tiras de LED y su driver.",
   "Acerca una linterna a la pantalla: si ves la imagen muy tenue, el problema es la retroiluminación y requiere técnico. Antes, desactiva el modo de ahorro de energía y sube el brillo.", "tec"),
  ("Aparecen líneas verticales u horizontales", "Cinta flex o placa T-CON del panel, o daño del propio panel.", "Revisamos las cintas flex, la placa T-CON y descartamos daño en el panel.",
   "Mira si las líneas aparecen también en el menú de la pantalla. Si es así, no es el cable ni la fuente: es la pantalla. No la presiones ni la golpees.", "tec"),
  ("Hay imagen pero no hay sonido", "Parlantes, placa de audio o ajustes de salida de audio (altavoz, ARC).", "Probamos los parlantes, la salida de audio y los ajustes de HDMI ARC.",
   "Revisa que no esté en silencio, que la salida de audio sea el altavoz de la pantalla y desconecta barras de sonido o auriculares Bluetooth.", "vuelve"),
  ("El HDMI no detecta el dispositivo", "Puerto HDMI dañado, cable defectuoso o fallo de comunicación (HDCP o CEC).", "Probamos los puertos HDMI, el cable y la comunicación con cada dispositivo.",
   "Prueba otro cable HDMI y otro puerto de la pantalla, y apaga y enciende ambos equipos. Si el dispositivo se reinicia solo, desactiva HDMI-CEC.", "vuelve"),
  ("No se conecta al Wi-Fi o las aplicaciones fallan", "Módulo Wi-Fi, firmware desactualizado o problema de la red.", "Revisamos el módulo Wi-Fi, actualizamos el firmware y probamos la conexión por cable.",
   "Reinicia el router y la pantalla, olvida y vuelve a conectar la red y revisa la fecha y la hora del equipo. Prueba con la red de tu celular.", "vuelve"),
  ("Se reinicia sola o se queda en el logo", "Firmware dañado, memoria de la placa principal o fuente de poder inestable.", "Probamos el arranque, medimos la fuente de poder y reinstalamos o actualizamos el firmware.",
   "Desconéctala 10 minutos y actualiza el firmware por USB desde la página del fabricante si tienes el modelo exacto. Evita regletas compartidas.", "vuelve"),
  ("La pantalla se rompió o quedó con una mancha tras un golpe", "Panel dañado: el cristal y las capas internas no se pueden reparar, solo reemplazar.", "Evaluamos si el panel tiene reemplazo disponible y si conviene económicamente frente a una pantalla nueva.",
   "No la uses si hay vidrio suelto, líquido o líneas que crecen. Desconéctala y no limpies la zona dañada.", "ya"),
 ],
 "tv-qled": [
  ("Hay sombras, halos o zonas oscuras en la imagen", "Atenuación local (local dimming) o LED de la retroiluminación por zonas con falla.", "Revisamos los LED por zonas, su driver y la configuración de atenuación local.",
   "Prueba con otro contenido y desactiva la atenuación local o el brillo adaptable en la configuración. Si la zona oscura siempre está en el mismo lugar, es retroiluminación.", "tec"),
  ("Aparecen manchas o «nubes» de luz", "Retroiluminación irregular o presión sobre el panel.", "Revisamos la retroiluminación, los difusores y si hubo presión o golpe sobre el panel.",
   "Reproduce una imagen negra a oscuras para ver bien las manchas. No presiones la pantalla para «acomodarla»: puede empeorar el daño.", "tec"),
  ("La pantalla se queda negra pero hay sonido", "Retroiluminación por zonas o placa de control de LED con falla.", "Medimos el driver de LED y probamos las tiras de retroiluminación.",
   "Con una linterna acerca la luz a la pantalla: si ves imagen tenue, es retroiluminación y necesita técnico.", "tec"),
  ("Se apaga sola y vuelve a encender", "Protección térmica, fuente de poder o firmware; en modelos con caja de conexiones externa, la caja o su cable.", "Medimos la fuente de poder, revisamos la ventilación y la comunicación con la caja externa si la tiene.",
   "Verifica que tenga ventilación libre atrás y a los lados, y desconecta y vuelve a conectar el cable de la caja externa si tu modelo la trae.", "vuelve"),
  ("El brillo cambia solo o parpadea", "Sensor de luz ambiente, modo HDR o driver de LED inestable.", "Probamos el sensor de luz, los modos de imagen y el driver de LED.",
   "Desactiva el brillo automático y el sensor de luz ambiente y prueba con otro contenido. Si parpadea en todo el contenido, es hardware.", "vuelve"),
  ("Aparecen líneas o una franja de colores", "Placa T-CON, cinta flex o panel dañado.", "Revisamos las cintas flex y la placa T-CON y descartamos daño en el panel.",
   "Mira si la franja aparece también en el menú. Si es así, no es el cable ni la fuente: es la pantalla.", "tec"),
 ],
 "tv-oled": [
  ("Queda una imagen fantasma o un logo marcado", "Retención de imagen por desgaste desigual de los píxeles orgánicos al mostrar imágenes fijas por mucho tiempo.", "Ejecutamos el ciclo de compensación de píxeles y evaluamos si la marca es permanente.",
   "Cambia a un contenido en movimiento y deja que la pantalla ejecute su ciclo de compensación con el equipo en espera. Reduce el brillo con imágenes fijas.", "vuelve"),
  ("Aparece una banda o línea vertical de color", "Cinta del panel o fallo del controlador de píxeles.", "Revisamos las cintas del panel, su controlador y la señal desde la placa principal.",
   "Mira si la banda aparece en el menú del equipo y en distintas entradas. No presiones la pantalla.", "tec"),
  ("No enciende y solo se oye un clic o nada", "Fuente de poder o placa principal con falla; los picos de voltaje suelen dañarlas.", "Medimos la fuente de poder, la placa principal y las protecciones.",
   "Desconecta la pantalla 10 minutos y prueba otro tomacorriente sin regleta. Si no hay ninguna reacción, necesita técnico.", "vuelve"),
  ("Hay puntos negros o zonas sin imagen", "Píxeles dañados o daño físico en el panel.", "Evaluamos la extensión del daño y si el panel tiene reemplazo disponible.",
   "Reproduce una imagen blanca y otra negra para ver la zona afectada. No intentes «arreglarla» presionando la pantalla.", "tec"),
  ("La imagen tiene un tono verdoso o rosado en los negros", "Calibración del panel o firmware que necesita actualización.", "Revisamos los ajustes de imagen, actualizamos el firmware y calibramos el panel.",
   "Restablece el modo de imagen a valores de fábrica y actualiza el firmware antes de pedir la visita.", "vuelve"),
  ("Marca un error de temperatura o se apaga", "Ventilación bloqueada, protección térmica o ventilador interno.", "Revisamos la ventilación, la temperatura de trabajo y los ventiladores internos.",
   "Aléjala de la pared, retira objetos encima y verifica que no esté junto a una fuente de calor.", "vuelve"),
 ],
}

# Particularidades por marca: sistema, procesador, líneas, origen, modelos y garantía.
MARCAS = {
 "samsung": dict(nombre="Samsung", color="#1428a0", pais="Corea del Sur", sistema="Tizen",
  origen="Samsung Electronics es una empresa surcoreana. Sus pantallas usan el sistema Tizen y las líneas Crystal UHD, QLED y Neo QLED.",
  lineas=["Crystal UHD", "QLED", "Neo QLED", "Neo QLED 8K", "OLED (QD-OLED)", "The Frame"], equipos=["tv-led", "tv-qled", "tv-oled"],
  tech={"tv-led": "Las pantallas Samsung Crystal UHD usan retroiluminación LED, el sistema Tizen y el procesador Crystal. Las fallas más comunes son la fuente de poder, la retroiluminación y la placa principal.",
        "tv-qled": "Las QLED y Neo QLED de Samsung añaden puntos cuánticos y, en los modelos altos, una caja One Connect externa que concentra las conexiones. Una falla en esa caja o en su cable puede dejar la pantalla sin señal.",
        "tv-oled": "Las pantallas OLED de Samsung (QD-OLED) combinan píxeles que emiten luz propia con puntos cuánticos. No tienen retroiluminación, así que las fallas típicas son retención de imagen, bandas de color, fuente de poder y placa principal."},
  etiqueta={"tv-led": "En la etiqueta de la parte trasera y en el menú Configuración > Soporte > Acerca de este TV.", "tv-qled": "En la etiqueta trasera y en el menú Configuración > Soporte > Acerca de este TV.", "tv-oled": "En la etiqueta trasera y en el menú Configuración > Soporte > Acerca de este TV."},
  modelo_ej="Los modelos Samsung empiezan por UN (Crystal UHD) o QN (QLED), por ejemplo UN55CU7000 o QN65Q60C. Están en la etiqueta trasera y en el menú Soporte de la pantalla.",
  garantia="Samsung ofrece garantía de fábrica en sus pantallas; su duración y condiciones dependen del modelo y del país de compra",
  mant=["Actualizar el software Tizen cuando la pantalla lo indique.", "Usar un protector de voltaje, sobre todo en la temporada de lluvias.", "No presionar la pantalla ni apoyar objetos sobre ella.", "En modelos con caja One Connect, mantener la caja ventilada y los cables firmes."],
  faq=[("¿Qué significa la luz roja que parpadea en mi pantalla Samsung?", "Indica que la pantalla está en espera o en protección. Si parpadea repetidamente al intentar encender, suele relacionarse con la fuente de poder o la placa principal."),
       ("¿Reparan Neo QLED y The Frame?", "Sí, incluyendo la caja One Connect y la retroiluminación por zonas."),
       ("¿La retroiluminación de una pantalla Samsung se puede reparar?", "Sí. Se reemplazan o reparan las tiras de LED y su driver; en pantallas grandes es una reparación frecuente.")]),
 "lg": dict(nombre="LG", color="#a50034", pais="Corea del Sur", sistema="webOS",
  origen="LG Electronics es una empresa surcoreana y una de las pioneras en pantallas OLED. Sus televisores usan el sistema webOS.",
  lineas=["OLED evo", "OLED", "QNED", "NanoCell", "UHD", "StanbyME"], equipos=["tv-led", "tv-qled", "tv-oled"],
  tech={"tv-led": "Las pantallas LG UHD y NanoCell usan retroiluminación LED y el sistema webOS. Las fallas más comunes son la fuente de poder, la retroiluminación y la conexión Wi-Fi.",
        "tv-qled": "Las QNED de LG combinan retroiluminación Mini LED con puntos cuánticos y NanoCell. Las fallas típicas son zonas oscuras por la atenuación local, manchas de luz y fuente de poder.",
        "tv-oled": "Las OLED de LG emiten luz propia en cada píxel y no tienen retroiluminación. Por eso las fallas típicas son retención de imagen, bandas de color, fuente de poder y placa principal."},
  etiqueta={"tv-led": "En la etiqueta de la parte trasera y en el menú Todos los ajustes > Soporte > Información del TV.", "tv-qled": "En la etiqueta trasera y en el menú Todos los ajustes > Soporte > Información del TV.", "tv-oled": "En la etiqueta trasera y en el menú Todos los ajustes > Soporte > Información del TV."},
  modelo_ej="Los modelos LG empiezan por OLED, por el tamaño y una referencia, por ejemplo OLED55C3PSA o 50UR8750PSA. Están en la etiqueta trasera y en el menú Soporte.",
  garantia="LG ofrece garantía de fábrica en sus pantallas; su duración y condiciones dependen del modelo y del país de compra",
  mant=["Actualizar webOS cuando la pantalla lo indique.", "En OLED, evitar imágenes fijas con brillo alto durante muchas horas y dejar que la pantalla haga su ciclo de compensación en espera.", "Usar un protector de voltaje, sobre todo en la temporada de lluvias.", "Limpiar la pantalla con un paño de microfibra seco, sin productos con alcohol."],
  faq=[("¿Qué es la retención de imagen en una OLED LG?", "Es una marca tenue que queda por mostrar una imagen fija mucho tiempo. A veces mejora con el ciclo de compensación de píxeles; si es permanente, se evalúa el panel."),
       ("¿Reparan OLED evo y QNED?", "Sí. Revisamos fuente de poder, placa principal, cintas del panel y, en QNED, la retroiluminación."),
       ("¿Mi pantalla LG no conecta al Wi-Fi, qué reviso?", "Reinicia el router, revisa la fecha y hora de la pantalla y actualiza webOS. Si sigue, puede ser el módulo Wi-Fi.")]),
 "sony": dict(nombre="Sony", color="#16161a", pais="Japón", sistema="Google TV",
  origen="Sony es una empresa japonesa de electrónica. Sus pantallas Bravia usan Google TV y los procesadores Cognitive Processor XR en los modelos altos.",
  lineas=["Bravia XR OLED", "Bravia XR Mini LED", "Bravia XR LED", "Bravia 4K LED", "Serie X80", "Serie X90"], equipos=["tv-led", "tv-qled", "tv-oled"],
  tech={"tv-led": "Las pantallas Sony Bravia LED usan Google TV y el procesador de imagen de la marca. Las fallas más comunes son la fuente de poder, la retroiluminación y los puertos HDMI.",
        "tv-qled": "Las Bravia XR Mini LED de Sony usan retroiluminación Mini LED con atenuación local y el procesador Cognitive Processor XR. Las fallas típicas son zonas oscuras, halos y fuente de poder.",
        "tv-oled": "Las Bravia XR OLED de Sony emiten luz propia en cada píxel. Las fallas típicas son retención de imagen, bandas de color, fuente de poder y protección térmica."},
  etiqueta={"tv-led": "En la etiqueta de la parte trasera y en el menú Configuración > Acerca de.", "tv-qled": "En la etiqueta trasera y en el menú Configuración > Acerca de.", "tv-oled": "En la etiqueta trasera y en el menú Configuración > Acerca de."},
  modelo_ej="Los modelos Sony empiezan por KD, XR o K, por ejemplo KD-55X80K o XR-65A80J. Están en la etiqueta trasera y en el menú Configuración > Acerca de.",
  garantia="Sony ofrece garantía de fábrica en sus pantallas; su duración y condiciones dependen del modelo y del país de compra",
  mant=["Actualizar el software de Google TV cuando la pantalla lo indique.", "Dejar espacio de ventilación detrás y a los lados de la pantalla.", "Usar un protector de voltaje, sobre todo en la temporada de lluvias.", "No usar productos de limpieza con alcohol ni amoníaco sobre la pantalla."],
  faq=[("¿Reparan las Bravia XR OLED?", "Sí. Revisamos fuente de poder, placa principal, cintas del panel y protección térmica."),
       ("¿Por qué mi pantalla Sony se reinicia sola?", "Suele ser firmware, memoria de la placa principal o una fuente de poder inestable. Actualizar el software y descartar la fuente resuelve la mayoría de los casos."),
       ("¿Qué hago si el HDMI de mi Sony no detecta la consola?", "Prueba otro cable y otro puerto, y apaga y enciende ambos equipos. Si sigue, puede ser el puerto HDMI.")]),
}

def _armar():
    M, C = {}, {}
    for bi, (m, b) in enumerate(MARCAS.items()):
        fallas = {}
        for e in b["equipos"]:
            arq = ARQ[e]; n = len(arq)
            orden = arq[bi % len(arq):] + arq[:bi % len(arq)]
            sel = orden[:n]
            fallas[e] = [[s, c, r] for s, c, r, _p, _cod in sel]
            for i, (_s, _c, _r, probar, cod) in enumerate(sel): C[f"{m}|{e}|{i}"] = (probar, cod)
        M[m] = dict(nombre=b["nombre"], color=b["color"], pais=b["pais"], origen=b["origen"], lineas=b["lineas"], equipos=b["equipos"], tech=b["tech"], fallas=fallas, codigos={},
                    mantenimiento=b["mant"], etiqueta=b["etiqueta"], modelo_ej=b["modelo_ej"], garantia=b["garantia"], faq=[list(x) for x in b["faq"]])
    return M, C
M, CONSEJOS = _armar()

# Repuestos (piezas) y diagnóstico para pantallas
PARTES = {k: [("Fuente de poder", r"fuente|voltaje|protecci"), ("Placa principal", r"placa principal|firmware|memoria|logo"), ("Retroiluminación LED", r"retroiluminaci|LED|sombra|mancha|oscur"),
              ("Placa T-CON y cintas flex", r"T-CON|cinta|l[ií]nea|banda|franja"), ("Panel (pantalla)", r"panel|rot|golpe|p[ií]xel"), ("Parlantes y audio", r"parlante|audio|sonido"),
              ("Puertos HDMI", r"HDMI"), ("Módulo Wi-Fi", r"Wi-Fi|red|aplicaci"), ("Ventilación y protección térmica", r"t[eé]rmic|temperatura|ventila")] for k in ("tv-led", "tv-qled", "tv-oled")}
PARTE_DESC = {
 "Fuente de poder": "Convierte la corriente de la pared en los voltajes que usa la pantalla. Si falla, la pantalla no enciende, se reinicia o solo parpadea la luz de espera.",
 "Placa principal": "Es el cerebro de la pantalla: procesa la imagen, el sonido y el sistema inteligente. Dañada o con firmware corrupto, la pantalla se queda en el logo o no responde.",
 "Retroiluminación LED": "Son las tiras de LED que iluminan el panel. Si fallan, hay sonido pero la imagen es oscura, con sombras o manchas.",
 "Placa T-CON y cintas flex": "Reciben la imagen de la placa principal y la reparten a los píxeles. Si fallan, aparecen líneas, bandas o franjas de color.",
 "Panel (pantalla)": "Es la pantalla en sí. Un golpe o puntos negros extensos suelen significar panel dañado, cuya reparación depende de si hay reemplazo disponible.",
 "Parlantes y audio": "Producen el sonido. Si fallan, hay imagen pero poco o ningún sonido, o el sonido distorsiona.",
 "Puertos HDMI": "Conectan consolas, decodificadores y barras de sonido. Un puerto dañado deja de detectar dispositivos.",
 "Módulo Wi-Fi": "Conecta la pantalla a internet. Si falla, la pantalla no ve redes o las aplicaciones no cargan.",
 "Ventilación y protección térmica": "Evita que la pantalla se sobrecaliente. Si se bloquea o falla, la pantalla se apaga sola o muestra un aviso de temperatura.",
}
PARTE_DIAG = {
 "Fuente de poder": "Medimos las salidas de voltaje, revisamos fusibles y buscamos condensadores hinchados.",
 "Placa principal": "Probamos el arranque, buscamos pistas dañadas y reinstalamos o actualizamos el firmware.",
 "Retroiluminación LED": "Con linterna confirmamos si hay imagen tenue y medimos cada tira de LED y su driver.",
 "Placa T-CON y cintas flex": "Revisamos las cintas, los conectores y la placa T-CON, y probamos con una señal de prueba.",
 "Panel (pantalla)": "Evaluamos la extensión del daño con imágenes de prueba y confirmamos si el panel tiene reemplazo.",
 "Parlantes y audio": "Medimos la impedancia de cada parlante y probamos la salida de audio y ARC.",
 "Puertos HDMI": "Probamos cada puerto con distintos cables y dispositivos y revisamos soldaduras del conector.",
 "Módulo Wi-Fi": "Actualizamos el firmware, probamos la conexión por cable y verificamos el módulo.",
 "Ventilación y protección térmica": "Revisamos ventiladores, pasta térmica y la temperatura de trabajo.",
}
EQ_VIDA = {
 "tv-led": ("7 a 10 años", ["el panel está roto o tiene líneas permanentes en un equipo con muchos años", "la placa principal y la retroiluminación fallan a la vez", "la reparación se acerca a la mitad del precio de una pantalla nueva"],
            ["falla la fuente de poder, la retroiluminación, un puerto HDMI o el módulo Wi-Fi", "la placa falla por un pico de voltaje y la pantalla es relativamente nueva"]),
 "tv-qled": ("7 a 10 años", ["el panel está dañado o la retroiluminación por zonas falla en muchas zonas", "la caja de conexiones y la placa principal fallan a la vez", "la reparación se acerca a la mitad del precio de una pantalla nueva"],
             ["falla la fuente de poder, el driver de LED o una tira de retroiluminación", "la caja o el cable de conexiones tienen un mal contacto"]),
 "tv-oled": ("8 a 10 años", ["el panel tiene bandas, puntos negros extensos o retención de imagen permanente", "la reparación del panel supera la mitad del precio de una pantalla nueva", "la pantalla recibió un golpe o líquido"],
             ["falla la fuente de poder, la placa principal o hay un error de temperatura", "hay retención de imagen leve que mejora con la compensación de píxeles"]),
}
GL_EQ = {k: ["Retroiluminación", "Fuente de poder", "Placa principal", "T-CON", "Panel", "HDMI ARC", "Firmware", "Retención de imagen", "Atenuación local"] for k in ("tv-led", "tv-qled", "tv-oled")}
GLOSARIO_TV = [("Retroiluminación", "Luz de fondo (tiras de LED) que ilumina el panel en pantallas LED y QLED."), ("Fuente de poder", "Placa que convierte la corriente de la pared en los voltajes que usa la pantalla."),
               ("Placa principal", "Placa que procesa la imagen, el sonido y el sistema inteligente de la pantalla."), ("T-CON", "Placa que reparte la imagen a los píxeles del panel."), ("Panel", "La pantalla en sí, donde se forma la imagen."),
               ("HDMI ARC", "Entrada HDMI que también envía el sonido de la pantalla a una barra de sonido."), ("Firmware", "Programa interno de la pantalla; si se daña o está desactualizado, aparecen reinicios y fallas de red."),
               ("Retención de imagen", "Marca tenue que queda en una OLED por mostrar una imagen fija durante mucho tiempo."), ("Atenuación local", "Función que apaga zonas de la retroiluminación para lograr negros más profundos.")]

# Mantenimiento e instalación por tipo de pantalla (mismo formato que los datos de electrodomésticos)
_MANT_COMUN = [("Limpiar la pantalla con microfibra seca", "Cada semana", "El polvo y las huellas opacan la imagen; evita alcohol y amoníaco."), ("Revisar la ventilación detrás y a los lados", "Cada mes", "El calor acumulado acorta la vida de la fuente y la placa."),
               ("Actualizar el firmware", "Cuando la pantalla lo indique", "Corrige fallas de red, reinicios y errores de las aplicaciones."), ("Revisar cables y puertos HDMI", "Cada 6 meses", "Un cable flojo o dañado causa pérdidas de imagen y sonido."),
               ("Usar protector de voltaje", "Siempre, y más en lluvias", "Los picos de voltaje dañan la fuente de poder y la placa principal."), ("No presionar ni apoyar objetos sobre la pantalla", "Siempre", "Una presión puntual daña el panel de forma permanente.")]
_INST_COMUN = dict(
 antes=["Mide el espacio y elige una altura de visión cómoda: el centro de la pantalla a la altura de los ojos sentado.", "Confirma que el tomacorriente tenga conexión a tierra y usa un protector de voltaje; evita extensiones compartidas.", "Si es de pared, verifica que esté soportada por un muro firme y que el soporte sea compatible (VESA) con el peso y el tamaño.", "Prepara la señal: cable de antena o decodificador, internet por cable o Wi-Fi y los dispositivos que conectarás por HDMI."],
 pasos=["Retiramos el empaque con cuidado, sin apoyar la pantalla sobre el panel.", "Armamos las patas o el soporte de pared y fijamos la pantalla.", "Conectamos la corriente, la antena o decodificador y los dispositivos por HDMI.", "Encendemos, configuramos idioma, región, red y la sintonización de canales.", "Ajustamos el modo de imagen y el sonido, y actualizamos el firmware.", "Te explicamos el uso del control remoto y los cuidados básicos."],
 errores=["Instalar el soporte de pared sin comprobar que el muro aguante el peso.", "Dejar la pantalla pegada a la pared o a un mueble sin ventilación.", "Cargar la pantalla por el panel en lugar de sostenerla por el marco.", "Conectarla a una regleta compartida con equipos de alto consumo."])
MANT_INST = {
 "tv-led": dict(mant=dict(intro="Una pantalla LED necesita poco mantenimiento, pero constante: limpieza correcta, buena ventilación y protección contra picos de voltaje evitan la mayoría de las averías de fuente de poder y retroiluminación.", tabla=_MANT_COMUN, senales=["Imagen que tarda en aparecer o parpadea al encender.", "Luz de espera que parpadea.", "Zonas más oscuras o manchas en la imagen.", "Reinicios o cierre inesperado de aplicaciones."], gye="En Costa Rica la temporada de lluvias trae tormentas eléctricas y picos de voltaje que dañan la fuente de poder y la placa principal. Desconecta la pantalla durante las tormentas fuertes y usa un protector con retardo de reconexión."),
                inst=dict(intro="Instalar bien una pantalla evita daños en el panel, mala imagen y problemas con la señal. Incluye montaje, conexiones, sintonización de canales y configuración de imagen y sonido.", gye="En Costa Rica la televisión digital usa el estándar ISDB-Tb, así que las pantallas compatibles sintonizan canales abiertos con una antena adecuada; en la sintonización conviene elegir la región correcta.", **_INST_COMUN)),
 "tv-qled": dict(mant=dict(intro="Las pantallas QLED y Mini LED tienen retroiluminación por zonas y, en algunos modelos, una caja de conexiones externa. Cuidar la ventilación y las conexiones evita sombras, parpadeos y apagados.", tabla=_MANT_COMUN, senales=["Zonas oscuras o halos alrededor de objetos brillantes.", "Brillo que cambia solo.", "Pérdida de señal al mover la caja o su cable.", "Apagados repentinos."], gye="Con el clima cálido y húmedo de muchas zonas de Costa Rica, deja siempre ventilación libre y evita ubicar la pantalla cerca de ventanas con lluvia o de fuentes de calor."),
                 inst=dict(intro="Las QLED y Mini LED suelen ser pantallas grandes y delgadas: el montaje y el transporte requieren cuidado, y la caja de conexiones externa debe quedar ventilada y bien conectada.", gye="En viviendas de Costa Rica con muros de gypsum o prefabricados, confirma que el soporte de pared se ancle a una estructura firme y no solo al panel de yeso.", **_INST_COMUN)),
 "tv-oled": dict(mant=dict(intro="Las pantallas OLED no tienen retroiluminación: cada píxel emite su luz. Cuidar el brillo con imágenes fijas y dejar que la pantalla ejecute su ciclo de compensación protege el panel.", tabla=_MANT_COMUN + [("Dejar que la pantalla haga el ciclo de compensación", "Cuando lo pida, con la pantalla en espera", "Compensa el desgaste de los píxeles y reduce la retención de imagen.")], senales=["Logos o menús que quedan marcados.", "Bandas o líneas de color.", "Puntos negros o zonas sin imagen.", "Avisos de temperatura."], gye="En Costa Rica el calor y la humedad aceleran el desgaste de la electrónica. Evita dejar la OLED encendida con una imagen fija durante horas y usa un protector de voltaje."),
                inst=dict(intro="Las OLED son muy delgadas y delicadas: se instalan sosteniéndolas por el marco, sin presionar el panel, y con una ubicación que evite el sol directo y el exceso de brillo en imágenes fijas.", gye="Al instalar una OLED en Costa Rica, elige una pared sin sol directo y deja ventilación libre atrás; el calor acumulado acorta la vida del panel.", **_INST_COMUN)),
}


# Descripción de cada línea de pantallas (una página por línea): tipo de pantalla, qué es y qué suele fallar
LINEAS_DET = {
 "samsung": {
  "Crystal UHD": ("tv-led", "Es la gama LED 4K de Samsung: retroiluminación LED, el procesador Crystal 4K y el sistema Tizen. Es la línea que más se ve en los hogares, por eso concentra muchas reparaciones de fuente de poder, retroiluminación y conexión Wi-Fi.", "En las Crystal UHD con retroiluminación en el borde, una tira de LED dañada oscurece la imagen por zonas y suele pedir cambio de la tira completa."),
  "QLED": ("tv-qled", "Añade una capa de puntos cuánticos sobre una base LED para lograr más brillo y color. Sigue necesitando retroiluminación, así que sus fallas se parecen a las de una LED.", "Una zona oscura fija en una QLED casi siempre es retroiluminación o su driver, no el panel."),
  "Neo QLED": ("tv-qled", "Usa retroiluminación Mini LED con atenuación local muy fina y, en la mayoría de los modelos, una caja One Connect externa que concentra las conexiones.", "Si una Neo QLED no recibe señal o se apaga sola, además de la pantalla se revisan la caja One Connect y el cable que la une."),
  "Neo QLED 8K": ("tv-qled", "Es la versión de resolución 8K de la Neo QLED: más zonas de atenuación y más procesamiento. Suele ser una pantalla grande y de gama alta.", "En pantallas grandes la retroiluminación tiene muchas zonas; una falla parcial se ve como halos o manchas y puede resolverse por módulos."),
  "OLED (QD-OLED)": ("tv-oled", "Combina píxeles que emiten luz propia con puntos cuánticos. No tiene retroiluminación, por lo que no sufre sombras de LED, pero sí retención de imagen si se abusa de imágenes fijas.", "Una marca tenue de un logo o de un menú puede mejorar con el ciclo de compensación de píxeles; si es permanente se evalúa el panel."),
  "The Frame": ("tv-qled", "Es una pantalla diseñada como un cuadro, con marco y modo arte. Suele colgarse pegada a la pared y usar una caja de conexiones externa con cable fino.", "En una The Frame el acceso al cableado es delicado: una falla de señal puede ser el cable, la caja o el soporte, y se diagnostica con la pantalla montada."),
 },
 "lg": {
  "OLED evo": ("tv-oled", "Es la gama OLED de LG con panel más brillante y el procesador α. Cada píxel emite su luz, por eso los negros son profundos y no hay retroiluminación.", "La falla típica de una OLED evo es la retención de imagen o una banda de color; el golpe al panel no tiene reparación sencilla."),
  "OLED": ("tv-oled", "Es la gama OLED de acceso de LG: mismo principio de píxeles que emiten luz propia y el sistema webOS.", "Una OLED que no enciende suele ser fuente de poder o placa principal, no el panel."),
  "QNED": ("tv-qled", "Combina retroiluminación Mini LED con puntos cuánticos y la tecnología NanoCell de LG, para más brillo y color que una LED común.", "Las zonas oscuras o los halos en una QNED apuntan a la atenuación local o a una zona de Mini LED."),
  "NanoCell": ("tv-led", "Es una LED con una capa NanoCell que filtra los colores para mejorar la pureza. Usa retroiluminación LED y webOS.", "Como en toda LED, la falla más común es la fuente de poder o la retroiluminación."),
  "UHD": ("tv-led", "Es la gama LED 4K de acceso de LG con webOS y el procesador de la marca. Es muy popular por su precio.", "En una UHD de LG, una pantalla que enciende con sonido pero sin imagen suele ser retroiluminación."),
  "StanbyME": ("tv-led", "Es una pantalla táctil portátil de LG montada sobre ruedas, pensada para moverla por la casa.", "Por moverse con frecuencia, en una StanbyME conviene revisar el cable de corriente, la batería interna y los puertos."),
 },
 "sony": {
  "Bravia XR OLED": ("tv-oled", "Es la gama OLED de Sony con el procesador Cognitive Processor XR y Google TV. Cada píxel emite su luz propia.", "En una Bravia XR OLED, un aviso de temperatura o un apagado repentino apunta a la ventilación o a la protección térmica."),
  "Bravia XR Mini LED": ("tv-qled", "Usa retroiluminación Mini LED con atenuación local y el procesador XR de Sony, para mucho brillo y contraste.", "Las zonas oscuras o los halos en una Mini LED de Sony indican una zona de retroiluminación o su driver."),
  "Bravia XR LED": ("tv-led", "Es la gama LED con retroiluminación de matriz completa y procesador XR de Sony, con Google TV.", "En una XR LED, si hay sonido pero imagen oscura, se revisan primero las tiras de LED y su driver."),
  "Bravia 4K LED": ("tv-led", "Es la gama LED 4K de acceso de Sony con Google TV.", "En una Bravia 4K, un reinicio en bucle suele ser firmware, memoria de la placa principal o una fuente inestable."),
  "Serie X80": ("tv-led", "Es una serie LED 4K de Sony muy extendida, con modelos de varios tamaños y Google TV.", "Una X80 que no enciende y tiene la luz de espera parpadeando casi siempre pide revisar la fuente de poder."),
  "Serie X90": ("tv-led", "Es una serie LED de gama alta de Sony con mejor atenuación y procesamiento que la X80.", "En una X90, las zonas oscuras fijas apuntan a la retroiluminación; las intermitentes, al driver o al firmware."),
 },
}

# Contenido de instalación y mantenimiento propio de cada marca (páginas dedicadas)
SERV_MARCA = {
 "samsung": dict(
  inst=["Si tu pantalla trae caja One Connect, la instalamos en un lugar ventilado y dejamos el cable fino ordenado y sin dobleces.", "Para The Frame, el soporte de pared pegado al muro y la ruta oculta del cable son parte de la instalación.", "Configuramos el sistema Tizen, la cuenta de Samsung y las aplicaciones que uses."],
  mant=[("Revisar la caja One Connect y su cable", "Cada 6 meses", "Un cable flojo o la caja sin ventilación puede dejar la pantalla sin señal."), ("Actualizar Tizen", "Cuando la pantalla lo indique", "Corrige fallas de Wi-Fi, aplicaciones y reinicios.")]),
 "lg": dict(
  inst=["Las OLED son muy delgadas: las sostenemos por el marco, nunca por el panel, y usamos un soporte de pared compatible con su peso.", "Configuramos webOS, la cuenta de LG y los ajustes de imagen para que el brillo no desgaste el panel OLED.", "Si pides un montaje a ras de pared, verificamos que los cables y los puertos queden accesibles."],
  mant=[("Dejar que la OLED haga su ciclo de compensación", "Cuando lo pida, con la pantalla en espera", "Compensa el desgaste de los píxeles y reduce la retención de imagen."), ("Actualizar webOS", "Cuando la pantalla lo indique", "Corrige fallas de Wi-Fi, aplicaciones y reinicios.")]),
 "sony": dict(
  inst=["Las Bravia con patas tipo caballete necesitan un mueble del ancho correcto: lo medimos antes de colocarla.", "Configuramos Google TV, la cuenta de Google y los ajustes de imagen del procesador XR.", "En modelos con matriz completa de retroiluminación, dejamos ventilación libre detrás para evitar sobrecalentamiento."],
  mant=[("Revisar los puertos HDMI y la salida de audio digital", "Cada 6 meses", "Los puertos flojos causan pérdida de imagen y sonido con consolas y barras."), ("Actualizar el software de Google TV", "Cuando la pantalla lo indique", "Corrige fallas de Wi-Fi, aplicaciones y reinicios.")]),
}
SOPORTES = [("Soporte fijo", "Deja la pantalla pegada a la pared. Es el más delgado y el más estable, pero no permite ajustar el ángulo ni acceder fácil a los puertos."),
            ("Soporte inclinable", "Permite inclinar la pantalla hacia abajo o hacia arriba. Sirve cuando se coloca alta o para evitar reflejos."),
            ("Soporte articulado", "Permite girar y separar la pantalla de la pared. Es útil en esquinas, salas grandes y para llegar a los puertos."),
            ("Mueble o patas", "Se apoya sobre un mueble. Hay que verificar el ancho del mueble, que aguante el peso y que deje ventilación libre.")]
LIMPIEZA = ["Apaga la pantalla y desconéctala de la corriente.", "Espera unos minutos a que se enfríe.", "Pasa un paño de microfibra seco con movimientos suaves, de arriba hacia abajo y sin presionar.", "Si hay una mancha, humedece apenas el paño con agua; nunca rocíes líquido sobre la pantalla.", "No uses alcohol, amoníaco ni limpiavidrios, porque dañan las capas de la pantalla.", "Seca con otro paño y espera a que no quede humedad antes de volver a conectar."]
NO_HACER = ["No presiones la pantalla con los dedos ni apoyes objetos sobre ella.", "No cubras las rejillas de ventilación ni la pegues a la pared sin espacio.", "No uses extensiones ni regletas compartidas con equipos de alto consumo.", "No abras la pantalla: tiene partes con voltaje alto aunque esté desconectada."]
