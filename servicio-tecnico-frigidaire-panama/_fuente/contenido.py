# -*- coding: utf-8 -*-
"""Contenido del sitio «Servicio técnico Frigidaire en Panamá» (SEO orgánico).
Servicio técnico Frigidaire Panamá (SEO orgánico)."""

DOMINIO = "https://centroserviciopanama.com/frigidaire"
DOMINIO_RAIZ = "https://centroserviciopanama.com"
ORG = "Centro de Servicio Panamá"
MARCA = "Frigidaire"
ES_LG = False
NOMBRE = "Servicio Técnico Frigidaire Panamá"
TEL = "+507 6933-7976"
WA = "50769337976"
HORARIO = "Lun a Sáb 7:00am–6:00pm"
GTM_ID = ""           # p. ej. "GTM-XXXXXXX"
VERIFICACION = ""     # código de Search Console (content de la metaetiqueta)

EQUIPOS = {
 "neveras": dict(
  nombre="Neveras y Refrigeradoras", corto="Neveras", sing="nevera", art="la nevera", tipo="nevera", icono="fridge",
  titulo_h1="Servicio técnico de neveras Frigidaire en Panamá",
  intro="Reparamos neveras y refrigeradoras Frigidaire a domicilio en Ciudad de Panamá: de dos puertas (Side by Side), French Door, de congelador superior o inferior y modelos con dispensador de agua y hielo.",
  modelos=["Side by Side (dos puertas verticales)", "French Door (puertas dobles arriba y cajón de congelador abajo)", "Congelador superior (Top Mount)", "Congelador inferior (Bottom Mount)", "Modelos con dispensador de agua y fábrica de hielo", "Modelos con compresor inverter"],
  fallas=[
   ("La nevera no enfría", "Falla del ventilador del evaporador, escarcha que tapa la circulación de aire, sensor de temperatura, tarjeta de control o compresor.", "Urgente", "Si el congelador sigue frío pero la parte de abajo no, suele ser el aire que no circula. Si nada enfría, no esperes: los alimentos se dañan."),
   ("El congelador se llena de escarcha", "Falla del sistema de descongelación (resistencia, termostato de deshielo o tarjeta), o empaque de la puerta que no sella.", "Revisar pronto", "No raspes el hielo con objetos filosos: puedes dañar la tubería. Desconecta, deja descongelar y avísanos."),
   ("Gotea agua dentro de la nevera", "Desagüe de descongelación tapado o congelado, o bandeja de drenaje en mal estado.", "Revisar pronto", "El agua suele acumularse bajo los cajones o en el piso de la nevera."),
   ("Hace ruido o zumbido fuerte", "Ventilador con hielo o desgastado, compresor que arranca con dificultad, o la nevera mal nivelada.", "Revisar pronto", "Un ruido nuevo y constante merece revisión: puede avisar una falla antes de que deje de enfriar."),
   ("El dispensador no saca agua", "Filtro de agua vencido, manguera congelada o válvula de entrada de agua.", "Vigilar", "Cambiar el filtro cada 6 meses evita muchos problemas de agua."),
   ("No hace hielo o hace poco", "Fábrica de hielo congelada, válvula de agua, sensor o temperatura del congelador fuera de rango.", "Vigilar", "Revisa que la llave de agua esté abierta y que el filtro no esté tapado."),
   ("Se enciende la luz del filtro o suena una alarma", "Aviso de cambio de filtro o puerta que no cierra bien.", "Vigilar", "La alarma de puerta indica que quedó abierta o que el empaque no cierra."),
   ("Se apaga y prende sola, o salta el breaker", "Variaciones de voltaje, compresor con falla de arranque o tarjeta de control.", "Urgente", "Desconéctala y no la prendas repetidamente: puedes dañar el compresor."),
   ("Huele mal por dentro", "Alimentos derramados, drenaje sucio o filtro de olores saturado.", "Vigilar", "Limpia con agua tibia y bicarbonato; si persiste, revisa el desagüe."),
  ],
  mant=["Limpia las rejillas y el polvo de la parte trasera o inferior cada 6 meses.", "Revisa que el empaque (goma) de las puertas selle: prueba con una hoja de papel.", "Cambia el filtro de agua cada 6 meses o cuando se encienda el aviso.", "Deja unos centímetros de separación con la pared para que el calor salga.", "No sobrecargues la nevera: el aire debe circular entre los alimentos.", "Conecta la nevera a una toma firme y, si hay cortes de luz, usa un protector de voltaje."],
  faq=[("¿Cuánto tarda una reparación de nevera Frigidaire?", "Depende de la falla. Muchas reparaciones se hacen en la misma visita; si hay que conseguir una pieza, te avisamos el plazo antes de empezar."),
       ("¿Reparan neveras Side by Side y French Door?", "Sí. Atendemos neveras Frigidaire de dos puertas, French Door y de congelador superior o inferior."),
       ("¿Por qué mi nevera Frigidaire no enfría pero el congelador sí?", "Normalmente el aire frío no está llegando a la parte de abajo: ventilador, escarcha o sensor. Es una de las fallas más comunes."),
       ("¿Cada cuánto debo cambiar el filtro de agua?", "Cada 6 meses, o antes si el agua sale lenta o con mal sabor."),
       ("¿Vale la pena reparar una nevera vieja?", "Si la falla es de una pieza accesible, casi siempre sí. Si el compresor está dañado y el equipo es muy viejo, te explicamos las opciones con honestidad."),
       ("¿Trabajan con garantía?", "Sí, cada reparación incluye garantía sobre la pieza y la mano de obra; el plazo se confirma antes de empezar.")]),
 "lavadoras": dict(
  nombre="Lavadoras", corto="Lavadoras", sing="lavadora", art="la lavadora", tipo="lavadora", icono="washer",
  titulo_h1="Servicio técnico de lavadoras Frigidaire en Panamá",
  intro="Reparamos lavadoras Frigidaire de carga superior y de carga frontal a domicilio en Ciudad de Panamá: no centrifugan, no desaguan, hacen ruido, gotean o muestran códigos de error.",
  modelos=["Carga superior", "Carga frontal", "Lavadoras con inverter y motor de transmisión directa", "Lavadoras con pantalla digital y códigos de error", "Lavasecadoras (lavan y secan en un solo equipo)"],
  fallas=[
   ("No centrifuga o centrifuga con mucho ruido", "Carga desbalanceada, amortiguadores o rodamientos desgastados, o problema del motor.", "Revisar pronto", "Primero redistribuye la ropa. Si persiste con poca carga, hay que revisarla."),
   ("No desagua (queda agua en la tina)", "Filtro de desagüe tapado, bomba de desagüe o manguera obstruida.", "Revisar pronto", "Revisa el filtro de pelusas y la manguera. Si aparece un código de error, anótalo para el técnico."),
   ("No llena de agua o llena muy lento", "Llaves cerradas, malla de la manguera tapada, válvula de entrada o sensor de nivel.", "Revisar pronto", "Si aparece un código de error, anótalo para el técnico."),
   ("Gotea o se sale el agua", "Mangueras flojas, empaque de la puerta (en carga frontal), bomba o tina.", "Urgente", "Cierra la llave de agua y desconecta la lavadora mientras llega el técnico."),
   ("La puerta no abre o no cierra", "Seguro de la puerta (cerradura) o bisagra desgastada.", "Revisar pronto", "Si aparece un código de error, anótalo para el técnico."),
   ("Vibra mucho o se desbalancea", "Carga desbalanceada o patas sin nivelar.", "Vigilar", "Reparte la ropa, evita lavar una sola prenda pesada y verifica que las cuatro patas toquen el piso."),
   ("Huele mal o tiene moho", "Humedad, exceso de detergente, empaque sucio o filtro lleno de pelusas.", "Vigilar", "En clima húmedo como el de Panamá conviene dejar la puerta entreabierta y hacer una limpieza de tina."),
   ("No enciende o se apaga en medio del ciclo", "Tarjeta de control, tomacorriente, variaciones de voltaje o falla del seguro.", "Urgente", "Prueba otro tomacorriente. Si no responde, desconéctala y escríbenos."),
   ("Deja pelusas o la ropa sale con residuos", "Filtro de pelusas saturado o roto, exceso de detergente.", "Vigilar", "Limpia el filtro de pelusas cada 3 o 4 lavadas."),
  ],
  mant=["Limpia el filtro de pelusas cada 3 o 4 lavadas.", "Haz una limpieza de tina cada mes con el programa de autolimpieza o con agua caliente.", "Deja la puerta o la tapa abierta después de lavar para que se seque.", "Usa la cantidad de detergente recomendada, sobre todo en detergentes líquidos.", "Revisa las mangueras cada 6 meses: busca grietas o humedad.", "Verifica que la lavadora esté nivelada y que no haya objetos en los bolsillos."],
  faq=[("¿Qué significan los códigos de error de la lavadora Frigidaire?", "Cada modelo muestra códigos distintos; anota el código exacto de tu pantalla y escríbenos con el modelo."),
       ("¿Por qué mi lavadora Frigidaire no centrifuga?", "La causa más común es una carga desbalanceada. Si pasa también con poca ropa, pueden ser los amortiguadores, el rodamiento o el motor."),
       ("¿Reparan lavadoras de carga superior y frontal?", "Sí, atendemos las dos."),
       ("¿Puedo seguir usando la lavadora si gotea?", "No lo recomendamos: el agua puede dañar el piso o las conexiones eléctricas. Cierra la llave y desconecta."),
       ("¿Cuánto cuesta la visita de diagnóstico?", "Escríbenos por WhatsApp con el modelo y la falla; te confirmamos el costo de la visita antes de ir."),
       ("¿Atienden en apartamentos y torres?", "Sí. Coordinamos horario y acceso con la administración del edificio.")]),
 "secadoras": dict(
  nombre="Secadoras", corto="Secadoras", sing="secadora", art="la secadora", tipo="secadora", icono="dryer",
  titulo_h1="Servicio técnico de secadoras Frigidaire en Panamá",
  intro="Reparamos secadoras Frigidaire eléctricas y de gas a domicilio en Ciudad de Panamá: no secan, no calientan, hacen ruido, tardan mucho o se detienen a mitad del ciclo.",
  modelos=["Secadoras eléctricas", "Secadoras a gas", "Secadoras con sensor de humedad", "Secadoras con pantalla digital", "Secadoras con bomba de calor"],
  fallas=[
   ("No seca o la ropa sale húmeda", "Ducto de salida de aire obstruido, filtro de pelusas tapado o resistencia con falla.", "Revisar pronto", "Limpia el filtro después de cada uso. Un ducto sucio alarga el secado y aumenta el riesgo de sobrecalentamiento."),
   ("No calienta", "Resistencia (en eléctricas), termostato o fusible térmico (en eléctricas y a gas), o ignitor (a gas).", "Revisar pronto", "Si gira pero no calienta, no insistas con ciclos largos."),
   ("Tarda demasiado en secar", "Ducto largo o sucio, filtro lleno, sensor de humedad sucio o poca ventilación del cuarto.", "Vigilar", "Revisa que la manguera de salida no esté aplastada ni muy larga."),
   ("Hace ruido o golpea", "Rodillos, correa o rodamiento desgastados, o prendas atrapadas.", "Revisar pronto", "Un chirrido constante suele indicar desgaste de rodillos o rodamientos."),
   ("Se detiene a mitad del ciclo", "Sobrecalentamiento por ducto tapado, sensor de temperatura o puerta que no cierra bien.", "Revisar pronto", "Deja enfriar, limpia el filtro y el ducto y vuelve a intentar."),
   ("No enciende", "Tomacorriente, botón de inicio, fusible térmico o tarjeta de control.", "Urgente", "Verifica el breaker (las eléctricas usan un breaker de 220 V). Si no es eso, avísanos."),
   ("La ropa sale con olor o pelusa", "Filtro sucio, ducto con residuos o suavizante acumulado.", "Vigilar", "Limpia el filtro con agua y déjalo secar."),
   ("La puerta no cierra o se abre sola", "Bisagra, pestillo o interruptor de puerta.", "Revisar pronto", "Si la puerta no cierra, la secadora no arranca por seguridad."),
  ],
  mant=["Limpia el filtro de pelusas después de cada ciclo.", "Revisa y limpia el ducto de salida de aire al menos una vez al año.", "No sobrecargues el tambor: la ropa necesita espacio para voltear.", "Mantén el cuarto ventilado: la secadora necesita aire para trabajar.", "Evita secar prendas con restos de productos inflamables.", "Una vez al año, pide una revisión de resistencias, sensores y rodillos."],
  faq=[("¿Por qué mi secadora Frigidaire no seca bien?", "Casi siempre es filtro o ducto obstruidos. Si ya los limpiaste y sigue igual, puede ser la resistencia o el sensor."),
       ("¿Reparan secadoras a gas y eléctricas?", "Sí, atendemos las dos."),
       ("¿Es peligroso que la secadora se sobrecaliente?", "Sí, puede serlo. Si huele a quemado o se apaga por temperatura, desconéctala y llama a un técnico."),
       ("¿Cada cuánto se limpia el ducto?", "Al menos una vez al año; si secas mucha ropa, cada 6 meses."),
       ("¿Instalan la secadora y el ducto?", "Sí, hacemos la instalación y revisamos que el ducto quede bien."),
       ("¿Atienden en apartamentos?", "Sí. Coordinamos acceso y horario con la administración.")]),
}

SERVICIOS = {
 "reparacion-a-domicilio": ("Reparación a domicilio de electrodomésticos Frigidaire", "Reparación a domicilio",
   "Vamos a tu casa o apartamento, revisamos tu equipo Frigidaire, te explicamos la falla y te damos el costo antes de reparar.",
   ["Revisión del equipo en tu casa", "Explicación clara de la falla", "Costo confirmado antes de reparar", "Reparación en la misma visita cuando hay repuesto", "Garantía sobre pieza y mano de obra"]),
 "mantenimiento-preventivo": ("Mantenimiento preventivo para neveras, lavadoras y secadoras Frigidaire", "Mantenimiento preventivo",
   "Un mantenimiento a tiempo evita daños mayores y alarga la vida de tus electrodomésticos, sobre todo con el calor y la humedad de Panamá.",
   ["Limpieza de componentes y filtros", "Revisión eléctrica y de sensores", "Revisión de mangueras y desagües", "Recomendaciones de uso"]),
 "instalacion": ("Instalación de lavadoras y secadoras Frigidaire", "Instalación",
   "Instalamos y dejamos funcionando tu equipo nuevo: nivelación, conexiones, ducto de la secadora y puesta en marcha.",
   ["Nivelación y conexión de agua y desagüe", "Instalación del ducto de la secadora", "Prueba de funcionamiento", "Recomendaciones de primer uso"]),
 "diagnostico-a-domicilio": ("Diagnóstico a domicilio: ¿vale la pena reparar tu equipo Frigidaire?", "Diagnóstico a domicilio",
   "Si no sabes qué le pasa a tu equipo o si conviene repararlo, hacemos un diagnóstico honesto: qué falla, cuánto cuesta y si vale la pena.",
   ["Revisión completa del síntoma", "Causa probable explicada", "Costo estimado de la reparación", "Opinión honesta: reparar o reemplazar", "Sin compromiso de reparar"]),
}

# zona: (nombre, tipo, distrito/area)
ZONAS = [
 ("San Francisco", "torres", "Ciudad de Panamá"), ("Bella Vista", "torres", "Ciudad de Panamá"), ("El Cangrejo", "mixto", "Ciudad de Panamá"),
 ("Obarrio", "torres", "Ciudad de Panamá"), ("Marbella", "torres", "Ciudad de Panamá"), ("Costa del Este", "torres", "Ciudad de Panamá"),
 ("Punta Pacífica", "torres", "Ciudad de Panamá"), ("Paitilla", "torres", "Ciudad de Panamá"), ("Avenida Balboa", "torres", "Ciudad de Panamá"),
 ("Betania", "casas", "Ciudad de Panamá"), ("Villa de las Fuentes", "casas", "Ciudad de Panamá"), ("Altos del Golf", "casas", "Ciudad de Panamá"),
 ("Brisas del Golf", "casas", "Ciudad de Panamá"), ("Condado del Rey", "casas", "Ciudad de Panamá"), ("Villa Lucre", "casas", "San Miguelito"),
 ("San Miguelito", "popular", "San Miguelito"), ("Las Cumbres", "popular", "Ciudad de Panamá"), ("Chilibre", "popular", "Ciudad de Panamá"),
 ("Pueblo Nuevo", "mixto", "Ciudad de Panamá"), ("Parque Lefevre", "mixto", "Ciudad de Panamá"), ("Río Abajo", "mixto", "Ciudad de Panamá"),
 ("Juan Díaz", "mixto", "Ciudad de Panamá"), ("Pedregal", "mixto", "Ciudad de Panamá"), ("Tocumen", "mixto", "Ciudad de Panamá"),
 ("Albrook", "mixto", "Ciudad de Panamá"), ("Clayton", "torres", "Ciudad de Panamá"), ("Ancón", "casas", "Ciudad de Panamá"),
 ("Arraiján", "casas", "Panamá Oeste"), ("La Chorrera", "casas", "Panamá Oeste"), ("Panamá Pacífico", "casas", "Panamá Oeste"),
 ("Calidonia", "mixto", "Ciudad de Panamá"), ("Curundú", "popular", "Ciudad de Panamá"), ("Chanis", "mixto", "Ciudad de Panamá"),
 ("Cerro Viento", "casas", "Ciudad de Panamá"), ("Don Bosco", "casas", "Ciudad de Panamá"), ("Llano Bonito", "casas", "Ciudad de Panamá"),
 ("Las Mañanitas", "casas", "Ciudad de Panamá"), ("Pacora", "popular", "Ciudad de Panamá"), ("Altos de Panamá", "casas", "Ciudad de Panamá"),
 ("Ciudad Radial", "casas", "Ciudad de Panamá"), ("Vista Alegre", "casas", "Panamá Oeste"), ("Burunga", "casas", "Panamá Oeste"),
 ("Howard", "casas", "Panamá Oeste"), ("Veracruz", "casas", "Panamá Oeste"), ("Coronado", "casas", "Panamá Oeste"), ("Chame", "casas", "Panamá Oeste"),
]
TIPO_TXT = {
 "torres": ("En esta zona predominan los edificios y torres de apartamentos. Antes de ir coordinamos con la administración el horario, el ingreso de herramientas y el uso del ascensor de servicio, para que la visita no tenga contratiempos.",
            "En apartamentos las lavadoras y secadoras suelen estar en espacios pequeños: revisamos ventilación, desagües y ductos con cuidado para no mojar ni ensuciar."),
 "casas": ("Aquí hay muchas casas y residenciales con lavandería o terraza. Revisamos también las condiciones del lugar donde está el equipo: ventilación, humedad, tomacorrientes y desagües.",
           "En casas, las variaciones de voltaje y la humedad de las áreas externas son causas frecuentes de fallas; te recomendamos protegerlos y te explicamos cómo."),
 "popular": ("Atendemos viviendas y apartamentos de la zona con el mismo diagnóstico claro: te explicamos la falla, el costo y las opciones antes de reparar.",
             "Muchas veces el problema se resuelve con una pieza accesible; si el equipo ya no vale la pena reparar, te lo decimos con honestidad."),
 "mixto": ("Es una zona con casas, apartamentos y negocios pequeños. Adaptamos la visita al lugar: coordinamos acceso, estacionamiento y horario contigo.",
           "Revisamos el equipo en el sitio, explicamos la falla y confirmamos el costo antes de empezar cualquier reparación."),
}

BLOG = [
 ("lavadora-frigidaire-codigos-de-error-panama", "Códigos de error de la lavadora Frigidaire: qué significan y qué hacer", "lavadoras",
  "Qué hacer cuando tu lavadora Frigidaire muestra un código de error y qué revisar antes de llamar al técnico.",
  [("Por qué aparece un código", "Las lavadoras Frigidaire con pantalla muestran un código cuando un sensor detecta algo fuera de lo normal: agua que no entra, agua que no sale, puerta mal cerrada o carga desbalanceada. El código te ahorra tiempo porque señala por dónde empezar."),
   ("Cómo leer el código", "Cada modelo Frigidaire usa códigos distintos. Anota el código exacto y el modelo (etiqueta en la tapa o en el marco de la puerta): con eso el técnico identifica la falla más rápido."),
   ("Revisiones básicas según el síntoma", "<ul><li>Agua que no sale: filtro de desagüe y manguera.</li><li>Agua que no entra: llaves abiertas y mallas de las mangueras.</li><li>Puerta: que cierre bien y sin prendas atrapadas.</li><li>Vibración: carga repartida y patas niveladas.</li></ul>"),
   ("Qué revisar primero", "Apaga la lavadora, desconéctala unos minutos y vuelve a encenderla. Revisa llaves, mangueras, filtro de desagüe y que la puerta cierre. Si el código vuelve a aparecer, es momento de llamar."),
   ("Cuándo llamar al técnico", "Si el código persiste, hay agua en el piso, huele a quemado o la lavadora se apaga sola, no la sigas usando. Escríbenos por WhatsApp con el modelo y el código que muestra.")]),
 ("nevera-frigidaire-no-enfria-panama", "Nevera Frigidaire no enfría: causas y qué revisar", "neveras",
  "Si tu nevera Frigidaire no enfría o enfría poco, estas son las causas más comunes y qué puedes revisar antes de llamar.",
  [("Primero, ¿qué parte no enfría?", "Si el congelador está frío pero la nevera no, el aire frío no circula bien (ventilador, escarcha o sensor). Si nada enfría, puede ser el compresor, la tarjeta o el sistema de enfriamiento."),
   ("Qué puedes revisar", "<ul><li>Que la nevera esté conectada y el breaker encendido.</li><li>Que la temperatura esté en un valor normal (nevera alrededor de 3 °C, congelador alrededor de -18 °C).</li><li>Que las puertas cierren bien y el empaque selle.</li><li>Que no haya escarcha en el fondo del congelador.</li><li>Que haya espacio detrás y a los lados para ventilar.</li></ul>"),
   ("Causas frecuentes", "Ventilador del evaporador con hielo, sistema de descongelación con falla, sensor de temperatura, tarjeta de control y, en casos más serios, compresor o fuga de gas."),
   ("Qué hacer con los alimentos", "Si la nevera dejó de enfriar, mantén las puertas cerradas, pasa lo esencial a una hielera y escríbenos. Cuanto antes se revise, menos alimento se pierde.")]),
 ("nevera-frigidaire-escarcha-congelador-panama", "Escarcha en el congelador de la nevera Frigidaire: por qué pasa", "neveras",
  "Por qué se forma escarcha en el congelador, cuándo es normal y cuándo indica una falla de descongelación.",
  [("Un poco de escarcha es normal", "Cada vez que abres la puerta entra aire húmedo, y en un clima como el de Panamá esa humedad se convierte en escarcha. Una capa fina no es problema."),
   ("Cuando es una falla", "Si se forman capas gruesas, el hielo tapa las salidas de aire o hay agua debajo de los cajones, probablemente falla el sistema de descongelación: resistencia, termostato de deshielo o tarjeta."),
   ("Qué hacer", "Desconecta la nevera, deja descongelar con las puertas abiertas y seca bien. No uses objetos filosos para raspar. Si la escarcha vuelve en pocos días, hay que revisar la descongelación."),
   ("Cómo prevenirla", "Cierra bien las puertas, no guardes alimentos calientes y revisa que el empaque selle.")]),
 ("lavadora-frigidaire-no-centrifuga-panama", "La lavadora Frigidaire no centrifuga: causas comunes", "lavadoras",
  "Si tu lavadora Frigidaire se queda con la ropa mojada y no centrifuga, revisa estas causas antes de llamar.",
  [("Carga desbalanceada", "Es la causa más común. La lavadora detecta que la ropa está mal repartida y no centrifuga para no dañarse. Redistribuye las prendas y evita lavar una sola prenda pesada."),
   ("Otras causas", "Patas sin nivelar, desagüe tapado (la lavadora no centrifuga si no vacía el agua), amortiguadores o rodamientos desgastados, motor o tarjeta de control."),
   ("Qué revisar", "<ul><li>Reparte la ropa y vuelve a probar con una carga más pequeña.</li><li>Revisa el filtro de desagüe y la manguera.</li><li>Nivela la lavadora.</li><li>Mira si muestra un código de error.</li></ul>"),
   ("Cuándo llamar", "Si centrifuga mal con poca ropa, hace ruido fuerte o vibra mucho, escríbenos con el modelo.")]),
 ("secadora-frigidaire-no-seca-panama", "La secadora Frigidaire no seca: filtro, ducto y resistencia", "secadoras",
  "Cuando la secadora gira pero la ropa sale húmeda, normalmente es filtro, ducto o resistencia. Así se revisa.",
  [("Lo primero: filtro y ducto", "El filtro de pelusas lleno y el ducto de salida obstruido impiden que el aire caliente salga. La ropa tarda mucho o no se seca."),
   ("Cuando calienta poco o nada", "En secadoras eléctricas puede ser la resistencia o el fusible térmico; en secadoras a gas, el ignitor o la válvula de gas."),
   ("Qué hacer", "<ul><li>Limpia el filtro de pelusas.</li><li>Revisa que la manguera de salida no esté aplastada.</li><li>No sobrecargues el tambor.</li><li>Verifica el breaker (las eléctricas usan 220 V).</li></ul>"),
   ("Seguridad", "Si huele a quemado o la secadora se sobrecalienta, desconéctala y llama a un técnico.")]),
 ("cortes-de-luz-voltaje-panama-electrodomesticos-frigidaire", "Cortes de luz y variaciones de voltaje: cómo proteger tus electrodomésticos", "neveras",
  "Los picos de voltaje y los cortes de luz dañan tarjetas y compresores. Cómo protegerte.",
  [("Por qué dañan", "Cuando vuelve la luz después de un corte, puede llegar con picos de voltaje. Las tarjetas electrónicas y los compresores son los más afectados."),
   ("Cómo protegerlos", "<ul><li>Usa protectores de voltaje en neveras, lavadoras y secadoras.</li><li>Después de un corte, espera unos minutos antes de volver a encender.</li><li>Verifica que la instalación eléctrica tenga buena conexión a tierra.</li></ul>"),
   ("Neveras", "Los compresores no deben arrancar varias veces seguidas. Un protector con retardo evita ese daño."),
   ("Si ya pasó", "Si el equipo no enciende después de un corte, no lo prendas repetidamente. Desconéctalo y escríbenos.")]),
 ("lavadora-moho-humedad-panama-frigidaire", "Moho y mal olor en la lavadora por la humedad de Panamá", "lavadoras",
  "El clima húmedo favorece el moho en la tina y el empaque. Cómo evitarlo y cómo limpiarlo.",
  [("Por qué pasa", "La humedad, el detergente en exceso y la puerta cerrada dejan agua y residuos dentro. Así aparecen los malos olores y el moho."),
   ("Cómo prevenirlo", "<ul><li>Deja la puerta o la tapa abierta después de lavar.</li><li>Usa la cantidad correcta de detergente.</li><li>Limpia el empaque de la puerta con un paño.</li><li>Haz una limpieza de tina cada mes.</li></ul>"),
   ("Cómo limpiarla", "Usa el programa de limpieza de tina si tu modelo lo tiene, o un ciclo largo con agua caliente. Limpia el filtro de pelusas y el cajón del detergente."),
   ("Si el olor no se va", "Puede haber residuos en el desagüe o la tina. Escríbenos y la revisamos.")]),
 ("reparar-o-reemplazar-electrodomestico-frigidaire-panama", "¿Reparar o reemplazar tu electrodoméstico Frigidaire?", "neveras",
  "Cómo decidir si conviene reparar un equipo o comprar uno nuevo, según la falla, la edad y el costo.",
  [("Reparar suele convenir cuando", "La falla es de una pieza accesible (sensor, ventilador, bomba, empaque, filtro) y el equipo funcionaba bien hasta ahora."),
   ("Reemplazar puede convenir cuando", "El equipo es muy antiguo y la falla es el compresor, la tina o el motor, y el costo se acerca al de uno nuevo."),
   ("Una regla práctica", "Si la reparación cuesta más de la mitad de un equipo nuevo similar, conviene pensar en reemplazarlo."),
   ("Diagnóstico honesto", "Antes de repararlo te explicamos la falla y el costo, y si no vale la pena, te lo decimos.")]),
]

FAQ_GENERAL = [
 ("¿Hacen servicio técnico Frigidaire a domicilio en Panamá?", "Sí. Vamos a tu casa u oficina en Ciudad de Panamá, San Miguelito y Panamá Oeste para revisar y reparar tu equipo Frigidaire. Escríbenos por WhatsApp con el modelo y la falla."),
 ("¿Qué equipos Frigidaire reparan?", "Neveras, lavadoras y secadoras."),
 ("¿Dónde dan servicio?", "En Ciudad de Panamá y alrededores: zonas como San Francisco, Bella Vista, Obarrio, Costa del Este, Punta Pacífica, Betania, San Miguelito, Albrook, Arraiján y La Chorrera."),
 ("¿Cuánto tardan en llegar?", "Coordinamos visitas en 24 a 48 horas en la mayoría de las zonas; te confirmamos disponibilidad por WhatsApp."),
 ("¿Cuánto cuesta la visita?", "Escríbenos por WhatsApp con el equipo, el modelo y la falla; te confirmamos el costo de la visita antes de ir."),
 ("¿Dan garantía?", "Sí, cada reparación incluye garantía sobre la pieza reemplazada y sobre la mano de obra. El plazo se confirma antes de empezar."),
 ("¿Cuál es el horario?", "De lunes a sábado, de 7:00am a 6:00pm."),
]

from blog2 import BLOG2
BLOG = BLOG + BLOG2

