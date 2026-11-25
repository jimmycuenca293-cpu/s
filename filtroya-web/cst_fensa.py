# -*- coding: utf-8 -*-
"""Marca Fensa (solo Chile). Equipos: refrigeradores, lavadoras, secadoras y cocinas/hornos.
No se inventan líneas, códigos de error ni cifras: las descripciones son generales y las fallas, las habituales de cada tipo de equipo."""
M_FENSA = dict(
    nombre="Fensa", color="#406981", pais="Chile",
    origen=("Fensa es una marca chilena de electrodomésticos con más de cien años de historia: nació en Valparaíso a comienzos del siglo XX como fábrica de envases y enlozados "
            "y llegó a ser pionera en la fabricación de cocinas, refrigeradores y lavadoras en Chile. Hoy sus refrigeradores y lavadoras están en muchos hogares del país."),
    lineas=["Refrigeradores side by side", "Lavadoras de carga superior", "Lavadoras que lavan y secan de carga frontal"],
    equipos=["neveras", "lavadoras"],
    tech={
        "neveras": ("Los refrigeradores Fensa que reparamos son de formato side by side, con dos puertas verticales, y algunos modelos traen tecnología inverter, donde una placa controla la velocidad del compresor. "
                    "El frío es no frost: un ventilador reparte el aire y una resistencia deshiela de forma automática. "
                    "Cuando falla la placa, el ventilador o el sistema de deshielo, el refrigerador deja de enfriar bien aunque el compresor se escuche funcionando."),
        "lavadoras": ("Fensa ofrece lavadoras de carga superior, con panel digital, selector de programas y dispensador de detergente, y lavadoras de carga frontal que lavan y también secan. "
                      "Controlan solas el llenado, el lavado, el enjuague y el centrifugado, y en los modelos que secan, además, el calentamiento y el secado. "
                      "Las fallas más comunes se relacionan con el desagüe, el llenado de agua, el motor, los amortiguadores y, en las que secan, la resistencia y el sensor del secado."),
    },
    fallas={
        "neveras": [
            ("No enfría bien", "Rejillas de aire tapadas, empaque de la puerta sin sellar, escarcha en el evaporador o falla del ventilador o del compresor.", "Revisamos el empaque, el ventilador y el sistema de deshielo, y medimos el arranque del compresor."),
            ("Hace ruido fuerte o intermitente", "Ventilador rozando hielo, compresor con desgaste o equipo mal nivelado o pegado a la pared.", "Ubicamos el origen del ruido, revisamos el ventilador y el compresor y verificamos la nivelación."),
            ("Se forma escarcha o hielo en el fondo", "Desagüe de deshielo tapado, resistencia o termostato de deshielo con falla, o puerta que no sella.", "Probamos la resistencia y el termostato de deshielo y limpiamos el desagüe."),
            ("Gotea agua en el piso o dentro del refrigerador", "Desagüe del deshielo tapado o congelado, o bandeja de evaporación fuera de lugar.", "Despejamos el desagüe, revisamos la bandeja y el nivel del equipo."),
            ("Muestra una temperatura rara o no responde el panel", "Sensor de temperatura con falla, placa de control con falla o variación de voltaje tras un corte de luz.", "Revisamos los sensores, la placa y la alimentación, y medimos el voltaje."),
            ("El compresor se enciende y se apaga cada pocos minutos", "Termostato o sensor con falla, condensador con polvo o relé de arranque desgastado.", "Medimos el arranque, limpiamos el condensador y probamos el relé y el termostato."),
        ],
        "lavadoras": [
            ("No desagua", "Filtro o bomba de desagüe tapados, manguera doblada o desagüe de la pared obstruido.", "Revisamos el filtro, la bomba y la manguera, y probamos el desagüe."),
            ("No centrifuga", "Carga desbalanceada, bomba tapada con agua en el tambor o falla del motor o del control.", "Verificamos el nivel, el desagüe, el motor y el control de centrifugado."),
            ("Hace ruido fuerte al centrifugar", "Rodamientos desgastados, amortiguadores sin fuerza o objetos atrapados.", "Inspeccionamos rodamientos y amortiguadores y buscamos objetos entre las tinas."),
            ("Fuga de agua por debajo", "Manguera suelta, empaque dañado o bomba con pérdida.", "Revisamos mangueras, empaques y bomba, y probamos con agua."),
            ("No llena de agua o llena lento", "Llave cerrada, mallas de entrada sucias o electroválvula con falla.", "Limpiamos las mallas, medimos la presión y probamos la electroválvula."),
            ("En el modelo que lava y seca, no seca o seca poco", "Filtro o conducto del secado con pelusa, sensor sucio o resistencia de secado con falla.", "Limpiamos el recorrido del aire y probamos el sensor y la resistencia de secado."),
        ],
    },
    codigos={},
    mantenimiento=[
        "Limpiar el polvo del condensador y revisar que el empaque de las puertas selle bien.",
        "Revisar el empaque de la puerta del refrigerador: si ya no sella, pierde frío y gasta más.",
        "Limpiar el filtro de la bomba o las mallas de entrada de la lavadora cuando el agua tarde en salir o en entrar.",
    ],
    etiqueta={
        "neveras": "Suele estar en el interior del refrigerador, en una pared lateral, o en la parte trasera del equipo.",
        "lavadoras": "Suele estar en la parte trasera, en el borde de la tapa o en el borde de la puerta.",
    },
    modelo_ej="El modelo y el número de serie están en la etiqueta del equipo; con una foto de esa etiqueta el diagnóstico es más preciso.",
    garantia=("La garantía de fábrica depende del modelo y de la tienda donde compraste el equipo; conserva la boleta o factura y revisa la tarjeta de garantía. "
              "En Chile, la Ley N° 19.496 contempla además una garantía legal para productos nuevos."),
    faq=[
        ("¿Reparan refrigeradores Fensa side by side?", "Sí. Atendemos refrigeradores Fensa side by side, también los de tecnología inverter. Cuéntanos el modelo y lo que hace y coordinamos la visita."),
        ("¿Reparan las lavadoras Fensa que lavan y secan?", "Sí. Atendemos lavadoras Fensa de carga superior y de carga frontal, incluidas las que también secan. Cuéntanos el modelo y lo que hace y coordinamos la visita."),
    ],
)

CONSEJOS_FENSA = {
    "fensa|neveras|0": ("Revisa que las rejillas no estén tapadas por alimentos, que la puerta cierre bien y que la perilla de temperatura no esté en el mínimo. No metas comida caliente.", "vuelve"),
    "fensa|neveras|1": ("Aleja el refrigerador unos centímetros de la pared y comprueba que esté nivelado y que nada roce la parte trasera.", "vuelve"),
    "fensa|neveras|2": ("Si es de frío directo, descongélalo por completo y limpia el interior. Si es no frost y la escarcha vuelve, no la retires a la fuerza.", "vuelve"),
    "fensa|neveras|3": ("Revisa que el equipo esté nivelado y que el desagüe de deshielo no esté tapado con restos. Seca el piso para evitar resbalones.", "vuelve"),
    "fensa|neveras|4": ("Anota lo que muestra el panel, desconecta el refrigerador 5 minutos y vuelve a conectarlo. Si empezó después de un corte de luz, no lo reinicies varias veces seguidas.", "tec"),
    "fensa|lavadoras|0": ("Con la lavadora apagada y desconectada, limpia el filtro de la bomba si tu modelo lo tiene accesible y revisa que la manguera de desagüe no esté doblada.", "vuelve"),
    "fensa|lavadoras|1": ("Detén el ciclo, reacomoda la ropa para que no quede toda de un lado y comprueba que la lavadora esté nivelada.", "vuelve"),
    "fensa|lavadoras|2": ("Comprueba que la lavadora esté nivelada y firme, y que no haya objetos atrapados. Si el ruido es metálico, no la sigas usando.", "tec"),
    "fensa|lavadoras|3": ("Cierra la llave de agua, revisa que las mangueras estén bien ajustadas y mira si hay agua en la base. Apaga y desconecta antes de tocar nada.", "vuelve"),
    "fensa|neveras|5": ("Limpia el polvo del condensador y deja espacio de ventilación. Si empezó después de un corte de luz, no lo reinicies varias veces seguidas.", "tec"),
    "fensa|lavadoras|4": ("Abre bien la llave de agua, revisa que la manguera de entrada no esté doblada y limpia las mallas de entrada con el equipo desconectado.", "vuelve"),
    "fensa|lavadoras|5": ("Limpia el filtro de pelusa si tu modelo lo tiene accesible, no sobrecargues el tambor y revisa que el conducto no esté aplastado. No uses el secado si huele a quemado.", "vuelve"),
}
