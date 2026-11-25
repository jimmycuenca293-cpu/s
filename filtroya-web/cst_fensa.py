# -*- coding: utf-8 -*-
"""Marca Fensa (solo Chile). Equipos: refrigeradores, lavadoras, secadoras y cocinas/hornos.
No se inventan líneas, códigos de error ni cifras: las descripciones son generales y las fallas, las habituales de cada tipo de equipo."""
M_FENSA = dict(
    nombre="Fensa", color="#406981", pais="Chile",
    origen=("Fensa es una marca chilena de electrodomésticos con más de cien años de historia: nació en Valparaíso a comienzos del siglo XX como fábrica de envases y enlozados "
            "y llegó a ser pionera en la fabricación de cocinas, refrigeradores y lavadoras en Chile. Hoy sus refrigeradores, lavadoras, secadoras y cocinas están en muchos hogares del país."),
    lineas=["Refrigeradores", "Lavadoras automáticas", "Lavadoras semiautomáticas", "Secadoras", "Cocinas a gas", "Hornos eléctricos"],
    equipos=["neveras", "lavadoras", "secadoras", "cocinas"],
    tech={
        "neveras": ("Los refrigeradores Fensa se encuentran en distintos formatos: de una puerta, con congelador arriba o con congelador abajo. Según el modelo, el frío es de tipo directo, "
                    "donde se forma escarcha que se retira de forma manual, o no frost, donde un ventilador reparte el aire y una resistencia deshiela de forma automática. "
                    "Saber cuál es el tuyo cambia el diagnóstico: una escarcha gruesa es normal en uno y una señal de falla en el otro."),
        "lavadoras": ("Fensa ofrece lavadoras automáticas y semiautomáticas en varias capacidades. Las automáticas controlan solas el llenado, el lavado, el enjuague y el centrifugado; "
                      "las semiautomáticas tienen dos tinas, una de lavado y otra de centrifugado, que se operan por separado. Las fallas más comunes se relacionan con el desagüe, el llenado de agua, "
                      "el motor y los amortiguadores."),
        "secadoras": ("Las secadoras Fensa secan con aire caliente y un tambor que gira. El filtro de pelusa, el ducto de salida y el termostato de seguridad son las piezas que más influyen en el rendimiento. "
                      "Cuando la ropa sale húmeda o tarda mucho en secar, casi siempre hay pelusa acumulada en el recorrido del aire."),
        "cocinas": ("Fensa fabrica cocinas a gas, hornos eléctricos y encimeras. En las cocinas a gas, el encendido por chispa y los quemadores se ensucian con la grasa y los derrames; "
                    "en los hornos eléctricos, la resistencia y el termostato son las piezas que más se desgastan. Toda reparación que toque el gas exige especial cuidado con la seguridad."),
    },
    fallas={
        "neveras": [
            ("No enfría bien", "Rejillas de aire tapadas, empaque de la puerta sin sellar, escarcha en el evaporador o falla del ventilador o del compresor.", "Revisamos el empaque, el ventilador y el sistema de deshielo, y medimos el arranque del compresor."),
            ("Hace ruido fuerte o intermitente", "Ventilador rozando hielo, compresor con desgaste o equipo mal nivelado o pegado a la pared.", "Ubicamos el origen del ruido, revisamos el ventilador y el compresor y verificamos la nivelación."),
            ("Se forma escarcha o hielo en el fondo", "Desagüe de deshielo tapado, resistencia o termostato de deshielo con falla, o puerta que no sella.", "Probamos la resistencia y el termostato de deshielo y limpiamos el desagüe."),
            ("Gotea agua en el piso o dentro del refrigerador", "Desagüe del deshielo tapado o congelado, o bandeja de evaporación fuera de lugar.", "Despejamos el desagüe, revisamos la bandeja y el nivel del equipo."),
            ("El compresor se enciende y se apaga cada pocos minutos", "Termostato o sensor con falla, condensador con polvo o relé de arranque desgastado.", "Medimos el arranque, limpiamos el condensador y probamos el relé y el termostato."),
        ],
        "lavadoras": [
            ("No desagua", "Filtro o bomba de desagüe tapados, manguera doblada o desagüe de la pared obstruido.", "Revisamos el filtro, la bomba y la manguera, y probamos el desagüe."),
            ("No centrifuga", "Carga desbalanceada, bomba tapada con agua en el tambor o falla del motor o del control.", "Verificamos el nivel, el desagüe, el motor y el control de centrifugado."),
            ("Hace ruido fuerte al centrifugar", "Rodamientos desgastados, amortiguadores sin fuerza o objetos atrapados.", "Inspeccionamos rodamientos y amortiguadores y buscamos objetos entre las tinas."),
            ("Fuga de agua por debajo", "Manguera suelta, empaque dañado o bomba con pérdida.", "Revisamos mangueras, empaques y bomba, y probamos con agua."),
            ("No llena de agua o llena lento", "Llave cerrada, mallas de entrada sucias o electroválvula con falla.", "Limpiamos las mallas, medimos la presión y probamos la electroválvula."),
        ],
        "secadoras": [
            ("No seca bien o tarda mucho", "Filtro o ducto de salida con pelusa, sensor sucio o sobrecarga del tambor.", "Limpiamos todo el recorrido del aire y revisamos el sensor y el termostato."),
            ("Gira pero no calienta", "Resistencia o termostato de seguridad con falla, o alimentación incompleta.", "Probamos la resistencia, el termostato de seguridad y la alimentación."),
            ("No enciende", "Falta de alimentación, puerta que no cierra bien o falla del control.", "Verificamos el enchufe, el interruptor de la puerta y el control."),
            ("El tambor no gira", "Correa cortada o motor con falla.", "Revisamos la correa, las poleas y el motor."),
        ],
        "cocinas": [
            ("Un quemador no enciende", "Quemador sucio, bujía de encendido con falla o salida de gas tapada.", "Limpiamos el quemador, probamos la bujía y revisamos la salida de gas con las medidas de seguridad."),
            ("Los quemadores no encienden por chispa", "Bujías húmedas o sucias, módulo de encendido con falla o falta de alimentación.", "Secamos y limpiamos las bujías y probamos el módulo y la alimentación."),
            ("El horno no calienta o calienta mal", "Resistencia quemada, termostato descalibrado o sensor con falla.", "Medimos la resistencia, probamos el termostato y verificamos la temperatura real."),
            ("El horno no enciende", "Falta de alimentación, selector o perilla con falla.", "Verificamos la alimentación y probamos el selector y las conexiones."),
        ],
    },
    codigos={},
    mantenimiento=[
        "Descongelar el refrigerador cada cierto tiempo si es de frío directo, y limpiar el polvo del condensador.",
        "Revisar el empaque de la puerta del refrigerador: si ya no sella, pierde frío y gasta más.",
        "Limpiar el filtro de la bomba o las mallas de entrada de la lavadora cuando el agua tarde en salir o en entrar.",
        "Limpiar el filtro de pelusa de la secadora después de cada uso y revisar que el ducto no esté aplastado.",
        "Limpiar los quemadores de la cocina cuando se ensucien con derrames, siempre con el equipo frío y el gas cerrado.",
    ],
    etiqueta={
        "neveras": "Suele estar en el interior del refrigerador, en una pared lateral, o en la parte trasera del equipo.",
        "lavadoras": "Suele estar en la parte trasera o en el borde de la tapa o de la puerta.",
        "secadoras": "Suele estar en el borde interior de la puerta o en la parte trasera.",
        "cocinas": "Suele estar en el borde del horno, bajo la tapa o en la parte trasera de la cocina.",
    },
    modelo_ej="El modelo y el número de serie están en la etiqueta del equipo; con una foto de esa etiqueta el diagnóstico es más preciso.",
    garantia=("La garantía de fábrica depende del modelo y de la tienda donde compraste el equipo; conserva la boleta o factura y revisa la tarjeta de garantía. "
              "En Chile, la Ley N° 19.496 contempla además una garantía legal para productos nuevos."),
    faq=[
        ("¿Reparan lavadoras semiautomáticas Fensa?", "Atendemos lavadoras Fensa automáticas y semiautomáticas. Cuéntanos el modelo y lo que hace, y coordinamos la visita para diagnosticarla en tu casa."),
        ("¿Reparan cocinas Fensa a gas?", "Sí. Primero se revisa la seguridad del equipo y de la conexión. Recuerda que la instalación o modificación de gas debe hacerla un instalador autorizado por la SEC."),
    ],
)

CONSEJOS_FENSA = {
    "fensa|neveras|0": ("Revisa que las rejillas no estén tapadas por alimentos, que la puerta cierre bien y que la perilla de temperatura no esté en el mínimo. No metas comida caliente.", "vuelve"),
    "fensa|neveras|1": ("Aleja el refrigerador unos centímetros de la pared y comprueba que esté nivelado y que nada roce la parte trasera.", "vuelve"),
    "fensa|neveras|2": ("Si es de frío directo, descongélalo por completo y limpia el interior. Si es no frost y la escarcha vuelve, no la retires a la fuerza.", "vuelve"),
    "fensa|neveras|3": ("Revisa que el equipo esté nivelado y que el desagüe de deshielo no esté tapado con restos. Seca el piso para evitar resbalones.", "vuelve"),
    "fensa|neveras|4": ("Limpia el polvo del condensador y deja espacio de ventilación. Si empezó después de un corte de luz, no lo reinicies varias veces seguidas.", "tec"),
    "fensa|lavadoras|0": ("Con la lavadora apagada y desconectada, limpia el filtro de la bomba si tu modelo lo tiene accesible y revisa que la manguera de desagüe no esté doblada.", "vuelve"),
    "fensa|lavadoras|1": ("Detén el ciclo, reacomoda la ropa para que no quede toda de un lado y comprueba que la lavadora esté nivelada.", "vuelve"),
    "fensa|lavadoras|2": ("Comprueba que la lavadora esté nivelada y firme, y que no haya objetos atrapados. Si el ruido es metálico, no la sigas usando.", "tec"),
    "fensa|lavadoras|3": ("Cierra la llave de agua, revisa que las mangueras estén bien ajustadas y mira si hay agua en la base. Apaga y desconecta antes de tocar nada.", "vuelve"),
    "fensa|lavadoras|4": ("Abre bien la llave de agua, revisa que la manguera de entrada no esté doblada y limpia las mallas de entrada con el equipo desconectado.", "vuelve"),
    "fensa|secadoras|0": ("Limpia el filtro de pelusa, revisa que el ducto de salida no esté aplastado y no sobrecargues el tambor.", "vuelve"),
    "fensa|secadoras|1": ("No sigas usándola si se sobrecalienta o huele a quemado. Limpia el filtro y revisa el ducto antes de volver a probar.", "tec"),
    "fensa|secadoras|2": ("Prueba el tomacorriente con otro aparato, revisa el breaker y comprueba que la puerta cierre bien.", "vuelve"),
    "fensa|secadoras|3": ("Apaga y desconecta la secadora. Un tambor que no gira suele indicar una correa o un motor con falla y requiere técnico.", "tec"),
    "fensa|cocinas|0": ("Limpia el quemador con el equipo frío y seco, y verifica que los orificios no estén tapados. Si hueles a gas, cierra la llave y ventila.", "ya"),
    "fensa|cocinas|1": ("Seca las bujías y limpia los quemadores. Si hueles a gas, cierra la llave del gas, ventila y no enciendas nada.", "ya"),
    "fensa|cocinas|2": ("Comprueba que el selector esté en la función correcta y que la puerta cierre bien. No uses el horno si ves chispas o humo.", "tec"),
    "fensa|cocinas|3": ("Prueba el tomacorriente con otro aparato y revisa el breaker. Si el horno sigue sin encender, desconéctalo y llama al técnico.", "tec"),
}
