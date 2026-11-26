# -*- coding: utf-8 -*-
"""Marca Midea para Guatemala (marca internacional). Equipos: refrigeradoras, lavadoras, estufas/hornos, aires acondicionados y microondas.
No se inventan líneas, códigos de error ni cifras: las descripciones son generales y las fallas, las habituales de cada tipo de equipo."""
_COMUN_REF = [
    ("No enfría bien", "Rejillas de aire tapadas, empaque de la puerta sin sellar, escarcha en el evaporador o falla del ventilador o del compresor.", "Revisamos el empaque, el ventilador y el sistema de deshielo, y medimos el arranque del compresor."),
    ("Hace ruido fuerte o intermitente", "Ventilador rozando hielo, compresor con desgaste o equipo mal nivelado o pegado a la pared.", "Ubicamos el origen del ruido, revisamos el ventilador y el compresor y verificamos la nivelación."),
    ("Se forma escarcha o hielo en el fondo", "Desagüe de deshielo tapado, resistencia o sensor de deshielo con falla, o puerta que no sella.", "Probamos la resistencia y el sensor de deshielo y limpiamos el desagüe."),
    ("Gotea agua en el piso o dentro de la refrigeradora", "Desagüe del deshielo tapado o congelado, o bandeja de evaporación fuera de lugar.", "Despejamos el desagüe, revisamos la bandeja y el nivel del equipo."),
    ("El dispensador de agua no funciona", "Filtro de agua saturado, electroválvula con falla o línea de agua doblada o congelada.", "Revisamos el filtro, la presión de agua y la electroválvula."),
    ("Se apagó o actúa raro después de una tormenta o un apagón", "Placa de control o sensor dañados por variaciones de voltaje al volver la luz.", "Medimos el voltaje, revisamos la placa y los sensores y probamos el arranque del compresor."),
]
M_MIDEA = dict(
    nombre="Midea", color="#0a6fb8", pais="China",
    origen=("Midea es una de las mayores fabricantes de electrodomésticos del mundo. Nació en China en 1968 y hoy su marca está presente en muchos países, con refrigeradoras, lavadoras, estufas, "
            "aires acondicionados y microondas. En Guatemala se encuentra en tiendas de electrodomésticos y comercios del país, y cada vez más hogares tienen un equipo Midea, por eso atendemos sus fallas a domicilio."),
    lineas=["Refrigeradoras side by side", "Refrigeradoras con congelador superior", "Refrigeradoras con dispensador de agua", "Lavadoras de carga superior", "Estufas a gas", "Aires acondicionados inverter", "Microondas"],
    equipos=["neveras", "lavadoras", "cocinas", "aires", "microondas"],
    tech={
        "neveras": ("Las refrigeradoras Midea se encuentran en formato side by side, con dos puertas verticales, y en formato de congelador superior, algunas con dispensador de agua. "
                    "Según el modelo, el frío es no frost: un ventilador reparte el aire y una resistencia deshiela de forma automática, y algunos modelos usan compresor inverter, controlado por una placa electrónica. "
                    "En los modelos con dispensador, la línea de agua y el filtro también influyen en el diagnóstico."),
        "lavadoras": ("Las lavadoras Midea de carga superior tienen panel digital con selector de programas, cajón de detergente y un motor que mueve el tambor. Controlan solas el llenado, el lavado, "
                      "el enjuague y el centrifugado. Las fallas más comunes se relacionan con el desagüe, el llenado de agua, el seguro de la tapa, el motor y los amortiguadores."),
        "cocinas": ("Las estufas Midea a gas tienen cuatro quemadores, horno con perilla de temperatura y encendido por chispa. Los quemadores se ensucian con la grasa y los derrames, "
                    "y las bujías, el termostato del horno y la válvula de gas son las piezas que más se revisan. Toda reparación que toque el gas exige especial cuidado con la seguridad."),
        "aires": ("Midea es especialmente conocida por sus aires acondicionados, entre ellos los modelos inverter, donde una placa ajusta la velocidad del compresor para mantener la temperatura. "
                  "Un aire se compone de una unidad interior, una unidad exterior y las tuberías que las unen. Las fallas más comunes se relacionan con filtros sucios, drenaje tapado, gas refrigerante, sensores y la placa de la unidad exterior."),
        "microondas": ("Los microondas Midea calientan con un magnetrón que genera las ondas, alimentado por un transformador o inversor, un diodo y un capacitor de alta tensión. "
                       "Cuando el plato gira y la luz funciona pero no calienta, la causa suele estar en esas piezas de alta tensión, que solo debe revisar un técnico."),
    },
    fallas={
        "neveras": _COMUN_REF,
        "lavadoras": [
            ("No desagua", "Filtro o bomba de desagüe tapados, manguera doblada o desagüe de la pared obstruido.", "Revisamos el filtro, la bomba y la manguera, y probamos el desagüe."),
            ("No centrifuga", "Carga desbalanceada, bomba tapada con agua en el tambor o falla del motor o del control.", "Verificamos el nivel, el desagüe, el motor y el control de centrifugado."),
            ("Hace ruido fuerte al centrifugar", "Rodamientos desgastados, amortiguadores sin fuerza u objetos atrapados.", "Inspeccionamos rodamientos y amortiguadores y buscamos objetos entre los tambores."),
            ("Fuga de agua por debajo", "Manguera suelta, empaque dañado o bomba con pérdida.", "Revisamos mangueras, empaques y bomba, y probamos con agua."),
            ("No llena de agua o llena lento", "Llave cerrada, mallas de entrada sucias o electroválvula con falla.", "Limpiamos las mallas, medimos la presión y probamos la electroválvula."),
            ("La tapa no cierra o no deja iniciar el ciclo", "Seguro de la tapa desalineado o con falla, o sensor de cierre sucio.", "Revisamos el seguro y el sensor de la tapa y sus conexiones."),
        ],
        "cocinas": [
            ("Un quemador no enciende", "Quemador sucio, bujía de encendido con falla o salida de gas tapada.", "Limpiamos el quemador, probamos la bujía y revisamos la salida de gas con las medidas de seguridad."),
            ("Los quemadores no encienden por chispa", "Bujías húmedas o sucias, módulo de encendido con falla o falta de alimentación.", "Secamos y limpiamos las bujías y probamos el módulo y la alimentación."),
            ("El horno no calienta o calienta mal", "Termostato descalibrado, válvula del horno con falla o encendido del horno que no actúa.", "Verificamos el termostato, la válvula y el encendido, y medimos la temperatura real."),
            ("La llama es amarilla o irregular", "Quemador sucio o con mezcla de aire mal ajustada, o tipo de gas que no corresponde al ajuste del equipo.", "Limpiamos y ajustamos la mezcla de aire y verificamos que el equipo corresponda al gas de la casa."),
        ],
        "aires": [
            ("Enciende pero no enfría", "Filtros y serpentín muy sucios, falta de gas refrigerante por fuga o falla del sensor de temperatura.", "Medimos presión y temperaturas de entrada y salida y revisamos el estado del serpentín antes de hablar de gas."),
            ("Gotea agua dentro de la casa", "Drenaje tapado o mala pendiente de la manguera.", "Destapamos el drenaje y revisamos la pendiente y el estado de la bandeja."),
            ("Hace ruido o vibra", "Ventilador desbalanceado, soporte flojo de la unidad exterior o piezas sueltas.", "Revisamos el ventilador, los soportes y los tornillos de ambas unidades."),
            ("Muestra un código de error o parpadea una luz", "Falla de comunicación entre unidades, sensor o placa con falla.", "Revisamos el cableado entre unidades, los sensores y la placa de la unidad exterior."),
            ("Se apaga sola o no responde al control", "Sensor de temperatura con falla, placa con falla o variación de voltaje.", "Probamos sensores, placa y alimentación y medimos el voltaje."),
            ("Dejó de funcionar después de una tormenta eléctrica", "Placa de la unidad exterior dañada por picos de voltaje al volver la luz.", "Medimos la placa y la alimentación y recomendamos protección de voltaje."),
        ],
        "microondas": [
            ("Gira el plato pero no calienta", "Magnetrón, diodo o fusible de alta tensión con falla.", "Verificamos el fusible, el diodo y el capacitor antes de cambiar el magnetrón."),
            ("Hace chispas dentro", "Placa guía de ondas quemada o interior dañado.", "Revisamos la placa guía y el interior del horno."),
            ("No enciende ni muestra nada", "Fusible, placa o puerta que no cierra el interruptor de seguridad.", "Revisamos el fusible, los interruptores de la puerta y la placa."),
            ("La puerta no cierra bien", "Bisagras o seguros desalineados o con desgaste.", "Revisamos seguros y bisagras y probamos el cierre con la puerta."),
        ],
    },
    codigos={},
    mantenimiento=[
        "Limpiar el polvo del condensador de la refrigeradora y revisar que el empaque de las puertas selle bien.",
        "Cambiar el filtro de agua de la refrigeradora con dispensador según indique el manual del modelo.",
        "Limpiar el filtro de la bomba o las mallas de entrada de la lavadora cuando el agua tarde en salir o en entrar.",
        "Dejar la tapa de la lavadora abierta después de usarla para que se seque el tambor y evitar olores.",
        "Limpiar los quemadores de la estufa cuando se ensucien con derrames, siempre con el equipo frío y el gas cerrado.",
        "Lavar los filtros del aire acondicionado con regularidad y pedir una limpieza completa antes de los meses más cálidos.",
        "Limpiar el interior del microondas y el borde de la puerta para que cierre bien.",
    ],
    etiqueta={
        "neveras": "Suele estar en el interior de la refrigeradora, en una pared lateral, o en la parte trasera del equipo.",
        "lavadoras": "Suele estar en la parte trasera o en el borde de la tapa.",
        "cocinas": "Suele estar en el borde del horno, bajo la tapa o en la parte trasera de la estufa.",
        "aires": "Suele estar en un costado de la unidad interior, bajo la tapa frontal, y en la unidad exterior.",
        "microondas": "Suele estar en la parte trasera o en el borde interior de la puerta.",
    },
    modelo_ej="El modelo y el número de serie están en la etiqueta del equipo; con una foto de esa etiqueta el diagnóstico es más preciso.",
    garantia=("La garantía de fábrica depende del modelo y de la tienda donde compraste el equipo; conserva la factura y revisa la tarjeta de garantía. "
              "En Guatemala, la Ley de Protección al Consumidor y Usuario protege además tus derechos como consumidor."),
    faq=[
        ("¿Reparan refrigeradoras Midea side by side?", "Sí. Atendemos refrigeradoras Midea side by side y de congelador superior, con o sin dispensador de agua. Cuéntanos el modelo y lo que hace y coordinamos la visita."),
        ("¿Reparan aires acondicionados Midea inverter?", "Sí. Revisamos aires Midea, incluidos los inverter: filtros, drenaje, gas, sensores y placa. Cuéntanos el modelo y lo que hace y coordinamos la visita."),
        ("¿Reparan estufas Midea a gas?", "Sí. Primero se revisa la seguridad del equipo y de la conexión del cilindro. Recuerda que la instalación o modificación de gas debe hacerla una persona calificada."),
        ("¿Atienden equipos Midea comprados en otro país?", "Sí, siempre que podamos identificar el modelo en la etiqueta. Algunas piezas pueden requerir pedido y eso alarga la reparación; te lo informamos antes de empezar."),
    ],
)

CONSEJOS_MIDEA = {
    "midea|neveras|0": ("Revisa que las rejillas no estén tapadas por alimentos, que las puertas cierren bien y que la temperatura no esté en el mínimo. No metas comida caliente.", "vuelve"),
    "midea|neveras|1": ("Aleja la refrigeradora unos centímetros de la pared y comprueba que esté nivelada y que nada roce la parte trasera.", "vuelve"),
    "midea|neveras|2": ("No retires la escarcha a la fuerza ni la rasques. Revisa que la puerta selle y que no haya alimentos contra la pared del fondo.", "vuelve"),
    "midea|neveras|3": ("Revisa que el equipo esté nivelado y que el desagüe de deshielo no esté tapado con restos. Seca el piso para evitar resbalones.", "vuelve"),
    "midea|neveras|4": ("Cambia el filtro de agua si ya pasó el tiempo que indica el manual, abre bien la llave de agua y revisa que la manguera de la parte trasera no esté doblada.", "vuelve"),
    "midea|neveras|5": ("Desconecta la refrigeradora 5 minutos y vuelve a conectarla. Si empezó después de una tormenta o un apagón, no la reinicies varias veces seguidas.", "tec"),
    "midea|lavadoras|0": ("Con la lavadora apagada y desconectada, limpia el filtro de la bomba si tu modelo lo tiene accesible y revisa que la manguera de desagüe no esté doblada.", "vuelve"),
    "midea|lavadoras|1": ("Detén el ciclo, reacomoda la ropa para que no quede toda de un lado y comprueba que la lavadora esté nivelada.", "vuelve"),
    "midea|lavadoras|2": ("Comprueba que la lavadora esté nivelada y firme, y que no haya objetos atrapados. Si el ruido es metálico, no la sigas usando.", "tec"),
    "midea|lavadoras|3": ("Cierra la llave de agua, revisa que las mangueras estén bien ajustadas y mira si hay agua en la base. Apaga y desconecta antes de tocar nada.", "vuelve"),
    "midea|lavadoras|4": ("Abre bien la llave de agua, revisa que la manguera de entrada no esté doblada y limpia las mallas de entrada con el equipo desconectado.", "vuelve"),
    "midea|lavadoras|5": ("Comprueba que nada impida cerrar la tapa y que el borde esté limpio. Apaga la lavadora 5 minutos y vuelve a encenderla.", "vuelve"),
    "midea|cocinas|0": ("Limpia el quemador con el equipo frío y seco, y verifica que los orificios no estén tapados. Si hueles a gas, cierra la llave del cilindro y ventila.", "ya"),
    "midea|cocinas|1": ("Seca las bujías y limpia los quemadores. Si hueles a gas, cierra la llave del cilindro, ventila y no enciendas nada.", "ya"),
    "midea|cocinas|2": ("Comprueba que la perilla esté en la función correcta y que la puerta cierre bien. No uses el horno si ves chispas o humo.", "tec"),
    "midea|cocinas|3": ("Limpia los quemadores con el equipo frío. Si la llama sigue amarilla o irregular, deja de usar ese quemador y pide al técnico que lo revise.", "tec"),
    "midea|aires|0": ("Limpia o lava los filtros de la unidad interior, revisa que la unidad exterior no esté tapada y que la temperatura y el modo estén bien configurados.", "vuelve"),
    "midea|aires|1": ("Apaga el aire y coloca un recipiente bajo la unidad interior. No metas objetos por el drenaje; deja que el técnico lo destape.", "tec"),
    "midea|aires|2": ("Revisa que no haya objetos sobre la unidad exterior y que esté firme. Si el ruido es metálico, apágalo.", "tec"),
    "midea|aires|3": ("Anota el código o el parpadeo de luces, apaga el aire 5 minutos y vuelve a encenderlo. Si el código vuelve, no insistas.", "tec"),
    "midea|aires|4": ("Cambia las pilas del control, revisa el modo y apaga el aire desde el automático unos minutos antes de volver a encenderlo.", "vuelve"),
    "midea|aires|5": ("Después de una tormenta, no lo enciendas varias veces seguidas. Revisa el automático y espera a que el técnico mida la placa.", "tec"),
    "midea|microondas|0": ("No uses el microondas vacío ni sigas probándolo. Si el plato gira y la luz funciona pero no calienta, desconéctalo: las piezas de alta tensión solo las revisa un técnico.", "tec"),
    "midea|microondas|1": ("Detén el microondas de inmediato, retira recipientes metálicos y limpia el interior con el equipo desconectado. Si las chispas siguen, no lo uses.", "tec"),
    "midea|microondas|2": ("Revisa que esté bien conectado y que el tomacorriente tenga corriente. Cierra bien la puerta y vuelve a probar.", "vuelve"),
    "midea|microondas|3": ("Limpia el borde de la puerta y los seguros, sin forzarlos. Si no cierra, no uses el microondas.", "tec"),
}
