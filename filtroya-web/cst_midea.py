# -*- coding: utf-8 -*-
"""Marca Midea (solo Chile). Equipos: refrigeradores (side by side y de congelador superior con dispensador), lavadoras de carga superior y cocinas a gas.
No se inventan líneas, códigos de error ni cifras: las descripciones son generales y las fallas, las habituales de cada tipo de equipo."""
M_MIDEA = dict(
    nombre="Midea", color="#0a6fb8", pais="China",
    origen=("Midea es una marca internacional de electrodomésticos de origen chino. En Chile se vende en las grandes tiendas y en el comercio especializado, sobre todo en refrigeradores, "
            "lavadoras y cocinas, y sus equipos ya están en muchos hogares del país."),
    lineas=["Refrigeradores side by side", "Refrigeradores con congelador superior", "Refrigeradores con dispensador de agua", "Lavadoras de carga superior", "Cocinas a gas"],
    equipos=["neveras", "lavadoras", "cocinas"],
    tech={
        "neveras": ("Los refrigeradores Midea se encuentran en formato side by side, con dos puertas verticales, y en formato de congelador superior, algunos con dispensador de agua. "
                    "Según el modelo, el frío es no frost: un ventilador reparte el aire y una resistencia deshiela de forma automática. En los modelos con dispensador, la línea de agua y el filtro "
                    "también influyen en el diagnóstico."),
        "lavadoras": ("Las lavadoras Midea de carga superior tienen panel digital con selector de programas, cajón de detergente y un motor que mueve el tambor. Controlan solas el llenado, el lavado, "
                      "el enjuague y el centrifugado. Las fallas más comunes se relacionan con el desagüe, el llenado de agua, el seguro de la tapa, el motor y los amortiguadores."),
        "cocinas": ("Las cocinas Midea a gas tienen cuatro quemadores, horno con perilla de temperatura y encendido por chispa. Los quemadores se ensucian con la grasa y los derrames, "
                    "y las bujías, el termostato del horno y la válvula de gas son las piezas que más se revisan. Toda reparación que toque el gas exige especial cuidado con la seguridad."),
    },
    fallas={
        "neveras": [
            ("No enfría bien", "Rejillas de aire tapadas, empaque de la puerta sin sellar, escarcha en el evaporador o falla del ventilador o del compresor.", "Revisamos el empaque, el ventilador y el sistema de deshielo, y medimos el arranque del compresor."),
            ("Hace ruido fuerte o intermitente", "Ventilador rozando hielo, compresor con desgaste o equipo mal nivelado o pegado a la pared.", "Ubicamos el origen del ruido, revisamos el ventilador y el compresor y verificamos la nivelación."),
            ("Se forma escarcha o hielo en el fondo", "Desagüe de deshielo tapado, resistencia o sensor de deshielo con falla, o puerta que no sella.", "Probamos la resistencia y el sensor de deshielo y limpiamos el desagüe."),
            ("Gotea agua en el piso o dentro del refrigerador", "Desagüe del deshielo tapado o congelado, o bandeja de evaporación fuera de lugar.", "Despejamos el desagüe, revisamos la bandeja y el nivel del equipo."),
            ("El dispensador de agua no funciona", "Filtro de agua saturado, electroválvula con falla o línea de agua doblada o congelada.", "Revisamos el filtro, la presión de agua y la electroválvula."),
            ("El compresor se enciende y se apaga cada pocos minutos", "Sensor de temperatura con falla, condensador con polvo o relé de arranque desgastado.", "Medimos el arranque, limpiamos el condensador y probamos el relé y los sensores."),
        ],
        "lavadoras": [
            ("No desagua", "Filtro o bomba de desagüe tapados, manguera doblada o desagüe de la pared obstruido.", "Revisamos el filtro, la bomba y la manguera, y probamos el desagüe."),
            ("No centrifuga", "Carga desbalanceada, bomba tapada con agua en el tambor o falla del motor o del control.", "Verificamos el nivel, el desagüe, el motor y el control de centrifugado."),
            ("Hace ruido fuerte al centrifugar", "Rodamientos desgastados, amortiguadores sin fuerza u objetos atrapados.", "Inspeccionamos rodamientos y amortiguadores y buscamos objetos entre las tinas."),
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
    },
    codigos={},
    mantenimiento=[
        "Limpiar el polvo del condensador del refrigerador y revisar que el empaque de las puertas selle bien.",
        "Cambiar el filtro de agua del refrigerador con dispensador según indique el manual del modelo.",
        "Limpiar el filtro de la bomba o las mallas de entrada de la lavadora cuando el agua tarde en salir o en entrar.",
        "Dejar la tapa de la lavadora abierta después de usarla para que se seque el tambor y evitar olores.",
        "Limpiar los quemadores de la cocina cuando se ensucien con derrames, siempre con el equipo frío y el gas cerrado.",
    ],
    etiqueta={
        "neveras": "Suele estar en el interior del refrigerador, en una pared lateral, o en la parte trasera del equipo.",
        "lavadoras": "Suele estar en la parte trasera o en el borde de la tapa.",
        "cocinas": "Suele estar en el borde del horno, bajo la tapa o en la parte trasera de la cocina.",
    },
    modelo_ej="El modelo y el número de serie están en la etiqueta del equipo; con una foto de esa etiqueta el diagnóstico es más preciso.",
    garantia=("La garantía de fábrica depende del modelo y de la tienda donde compraste el equipo; conserva la boleta o factura y revisa la tarjeta de garantía. "
              "En Chile, la Ley N° 19.496 contempla además una garantía legal para productos nuevos."),
    faq=[
        ("¿Reparan refrigeradores Midea side by side?", "Sí. Atendemos refrigeradores Midea side by side y de congelador superior, con o sin dispensador de agua. Cuéntanos el modelo y lo que hace y coordinamos la visita."),
        ("¿Reparan cocinas Midea a gas?", "Sí. Primero se revisa la seguridad del equipo y de la conexión. Recuerda que la instalación o modificación de gas debe hacerla un instalador autorizado por la SEC."),
    ],
)

CONSEJOS_MIDEA = {
    "midea|neveras|0": ("Revisa que las rejillas no estén tapadas por alimentos, que las puertas cierren bien y que la temperatura no esté en el mínimo. No metas comida caliente.", "vuelve"),
    "midea|neveras|1": ("Aleja el refrigerador unos centímetros de la pared y comprueba que esté nivelado y que nada roce la parte trasera.", "vuelve"),
    "midea|neveras|2": ("No retires la escarcha a la fuerza ni la rasques. Revisa que la puerta selle y que no haya alimentos contra la pared del fondo.", "vuelve"),
    "midea|neveras|3": ("Revisa que el equipo esté nivelado y que el desagüe de deshielo no esté tapado con restos. Seca el piso para evitar resbalones.", "vuelve"),
    "midea|neveras|4": ("Cambia el filtro de agua si ya pasó el tiempo que indica el manual, abre bien la llave de agua y revisa que la manguera de la parte trasera no esté doblada.", "vuelve"),
    "midea|neveras|5": ("Limpia el polvo del condensador y deja espacio de ventilación. Si empezó después de un corte de luz, no lo reinicies varias veces seguidas.", "tec"),
    "midea|lavadoras|0": ("Con la lavadora apagada y desconectada, limpia el filtro de la bomba si tu modelo lo tiene accesible y revisa que la manguera de desagüe no esté doblada.", "vuelve"),
    "midea|lavadoras|1": ("Detén el ciclo, reacomoda la ropa para que no quede toda de un lado y comprueba que la lavadora esté nivelada.", "vuelve"),
    "midea|lavadoras|2": ("Comprueba que la lavadora esté nivelada y firme, y que no haya objetos atrapados. Si el ruido es metálico, no la sigas usando.", "tec"),
    "midea|lavadoras|3": ("Cierra la llave de agua, revisa que las mangueras estén bien ajustadas y mira si hay agua en la base. Apaga y desconecta antes de tocar nada.", "vuelve"),
    "midea|lavadoras|4": ("Abre bien la llave de agua, revisa que la manguera de entrada no esté doblada y limpia las mallas de entrada con el equipo desconectado.", "vuelve"),
    "midea|lavadoras|5": ("Comprueba que nada impida cerrar la tapa y que el borde esté limpio. Apaga la lavadora 5 minutos y vuelve a encenderla.", "vuelve"),
    "midea|cocinas|0": ("Limpia el quemador con el equipo frío y seco, y verifica que los orificios no estén tapados. Si hueles a gas, cierra la llave y ventila.", "ya"),
    "midea|cocinas|1": ("Seca las bujías y limpia los quemadores. Si hueles a gas, cierra la llave del gas, ventila y no enciendas nada.", "ya"),
    "midea|cocinas|2": ("Comprueba que la perilla esté en la función correcta y que la puerta cierre bien. No uses el horno si ves chispas o humo.", "tec"),
    "midea|cocinas|3": ("Limpia los quemadores con el equipo frío. Si la llama sigue amarilla o irregular, deja de usar esa hornilla y llama al técnico.", "tec"),
}
