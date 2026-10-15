"""Tutorial de instalación de cada filtro: dónde va, cómo se saca el viejo, cómo se pone el nuevo,
cuánta agua purgar y cómo reiniciar el aviso. Lo usan la ficha del producto, las páginas de
referencia y de modelo de nevecón, y la página /instalacion/.

Donde el lugar cambia según el modelo, el texto lo dice: es mejor guiar al cliente a revisar
su nevecón que prometerle un sitio exacto que no sea el suyo.
"""
import html

esc = lambda s: html.escape(str(s), quote=True)

# Pasos comunes para los externos (van en la manguera)
_EXTERNO = {
    "donde": "En la manguera delgada que lleva el agua al nevecón, por detrás del aparato o debajo del lavaplatos, donde está la llave de paso.",
    "tiempo": "10 a 15 minutos",
    "herramientas": "Un trapo, un balde pequeño y, si la manguera es nueva, un bisturí o tijeras para cortarla derecha.",
    "pasos": [
        "Cierra la llave de paso del agua que alimenta el nevecón y desconecta el nevecón de la corriente.",
        "Separa un poco el nevecón de la pared para llegar a la manguera de atrás.",
        "Si vas a cambiar un filtro viejo, suéltalo de los dos extremos: presiona el anillo del racor y hala la manguera. Si es la primera vez, corta la manguera derecha en un tramo recto.",
        "Mira la flecha impresa en el filtro nuevo: debe apuntar hacia el nevecón, en la dirección en que corre el agua.",
        "Mete cada extremo de la manguera en el racor del filtro hasta el fondo (entra unos 1,5 cm) y hala suave para confirmar que quedó firme.",
        "Abre la llave de paso despacio y revisa durante un par de minutos que no gotee por ninguno de los dos lados.",
        "Conecta el nevecón y saca unos 4 litros de agua por el dispensador para purgar el aire y el polvo de carbón. Los primeros chorros salen con aire: es normal.",
    ],
    "reset": "El filtro externo no prende ninguna luz en el nevecón. Anota la fecha en el filtro con un marcador y cámbialo a los 6 meses.",
}

_INTERNO_GIRO = [
    "Pon un trapo o una toalla debajo del filtro: al sacarlo caen unas gotas de agua.",
    "Gira el filtro viejo un cuarto de vuelta hacia la izquierda (contra las manecillas del reloj) y sácalo halando derecho.",
    "Quítale la tapa protectora al filtro nuevo.",
    "Mételo en el mismo sitio, alineando la marca o la flecha del filtro con la del nevecón, y gíralo un cuarto de vuelta hacia la derecha hasta que quede firme. No lo fuerces.",
]

INSTALACION = {
    "sam-cin-o": {
        "donde": "Dentro del refrigerador, en la esquina de arriba (a la derecha en la mayoría de nevecones Samsung de dos puertas y French door). En algunos modelos está detrás de una tapa.",
        "tiempo": "2 minutos", "herramientas": "Ninguna, solo un trapo.",
        "pasos": ["Si tu modelo tiene tapa, ábrela halando desde el borde."] + _INTERNO_GIRO + [
            "Saca unos 6 litros de agua por el dispensador (unos 5 minutos en total, con pausas) para sacar el aire y el polvo de carbón."],
        "reset": "Reinicia el aviso del filtro: según el modelo, deja presionado 3 segundos el botón «Filter Reset» o la combinación «Ice Type» + «Child Lock» del panel.",
    },
    "sam-qin-o": {
        "donde": "Dentro del refrigerador, arriba, en una caja con tapa (al centro o a la derecha según el modelo, incluidos los Bespoke y Family Hub).",
        "tiempo": "2 minutos", "herramientas": "Ninguna, solo un trapo.",
        "pasos": ["Abre la tapa de la caja del filtro."] + _INTERNO_GIRO + [
            "Cierra la tapa.",
            "Saca unos 6 litros de agua por el dispensador (unos 5 minutos, con pausas) para sacar el aire y el polvo de carbón."],
        "reset": "Reinicia el aviso: en el panel o en la pantalla del nevecón busca «Filtro» o «Filter» y deja presionado «Reset» 3 segundos; en los Family Hub se hace desde la pantalla, en Ajustes.",
    },
    "sam-cu1-o": {
        "donde": "Dentro del refrigerador, en la esquina de arriba a la derecha, en los nevecones Samsung de dos puertas lado a lado (side by side) que traen este filtro de cuerpo corto.",
        "tiempo": "2 minutos", "herramientas": "Ninguna, solo un trapo.",
        "pasos": _INTERNO_GIRO + ["Saca unos 6 litros de agua por el dispensador para sacar el aire y el polvo de carbón."],
        "reset": "Reinicia el aviso: deja presionado 3 segundos el botón «Filter Reset» (en algunos modelos es «Ice Type» o «Alarm»; mira el texto pequeño debajo del botón).",
    },
    "sam-ex-o": dict(_EXTERNO),
    "lg-1000-o": {
        "donde": "Dentro del refrigerador, en el techo, detrás de una tapa (a la izquierda o atrás según el modelo).",
        "tiempo": "2 minutos", "herramientas": "Ninguna, solo un trapo.",
        "pasos": ["Abre la tapa del filtro empujándola o halándola hacia abajo.",
                  "Gira el filtro viejo un cuarto de vuelta hacia la izquierda y bájalo halando derecho; ten un trapo debajo.",
                  "Quítale la tapa protectora al filtro nuevo.",
                  "Mételo hacia arriba alineando la flecha con la del nevecón y gíralo un cuarto de vuelta hacia la derecha hasta que quede firme.",
                  "Cierra la tapa.",
                  "Saca unos 4 litros de agua por el dispensador para sacar el aire y el polvo de carbón."],
        "reset": "Reinicia el aviso: deja presionado 3 segundos el botón «Filter» o «Water Filter» del panel hasta que se apague la luz.",
    },
    "lg-700-o": {
        "donde": "Dentro del refrigerador, en la esquina de arriba a la izquierda, detrás de una tapa (nevecones LG French door y de dos puertas).",
        "tiempo": "2 minutos", "herramientas": "Ninguna, solo un trapo.",
        "pasos": ["Abre la tapa del filtro presionando la pestaña de abajo."] + _INTERNO_GIRO + [
            "Cierra la tapa.", "Saca unos 4 litros de agua por el dispensador para sacar el aire y el polvo de carbón."],
        "reset": "Reinicia el aviso: deja presionado 3 segundos el botón «Filter» o «Water Filter» del panel.",
    },
    "lg-800-o": {
        "donde": "Dentro del refrigerador, arriba, detrás de una tapa (a la derecha en la mayoría de nevecones LG French door que usan este filtro).",
        "tiempo": "2 minutos", "herramientas": "Ninguna, solo un trapo.",
        "pasos": ["Abre la tapa del filtro."] + _INTERNO_GIRO + [
            "Cierra la tapa.", "Saca unos 4 litros de agua por el dispensador para sacar el aire y el polvo de carbón."],
        "reset": "Reinicia el aviso: deja presionado 3 segundos el botón «Filter» o «Water Filter» del panel.",
    },
    "lg-500-o": {
        "donde": "Dentro del refrigerador, en la parte de arriba, en una caja con tapa (a la izquierda o a la derecha según el modelo) en nevecones LG de dos puertas lado a lado.",
        "tiempo": "2 minutos", "herramientas": "Ninguna, solo un trapo.",
        "pasos": ["Abre la tapa de la caja del filtro."] + _INTERNO_GIRO + [
            "Cierra la tapa.", "Saca unos 4 litros de agua por el dispensador para sacar el aire y el polvo de carbón."],
        "reset": "Reinicia el aviso: deja presionado 3 segundos el botón «Filter» o «Water Filter» del panel.",
    },
    "lg-600-o": {
        "donde": "Dentro del refrigerador, en la parte de arriba, en una caja con tapa, en nevecones LG de dos puertas lado a lado (según el modelo, a la izquierda o a la derecha).",
        "tiempo": "2 minutos", "herramientas": "Ninguna, solo un trapo.",
        "pasos": ["Abre la tapa de la caja del filtro."] + _INTERNO_GIRO + [
            "Cierra la tapa.", "Saca unos 4 litros de agua por el dispensador para sacar el aire y el polvo de carbón."],
        "reset": "Reinicia el aviso: deja presionado 3 segundos el botón «Filter» o «Water Filter» del panel.",
    },
    "lg-ex-o": dict(_EXTERNO),
    "wp-1-o": {
        "donde": "Dentro del refrigerador, en la esquina de arriba a la derecha (nevecones Whirlpool, Maytag, KitchenAid y Jenn-Air de puertas francesas).",
        "tiempo": "2 minutos", "herramientas": "Ninguna, solo un trapo.",
        "pasos": ["Si tiene tapa, ábrela."] + _INTERNO_GIRO + [
            "Saca unos 12 litros de agua por el dispensador (unos 5 minutos, con pausas): los filtros EveryDrop piden una purga larga para que el agua salga clara."],
        "reset": "Reinicia el aviso: deja presionado 3 segundos el botón «Filter Reset» o «Water Filter» del panel.",
    },
    "wp-2-o": {
        "donde": "En la rejilla de abajo, al frente del nevecón (zócalo), en nevecones Whirlpool, Maytag, KitchenAid y Amana de dos puertas lado a lado.",
        "tiempo": "3 minutos", "herramientas": "Ninguna, solo un trapo.",
        "pasos": ["Ubica la tapa del filtro en la rejilla de abajo, al frente.",
                  "Gira la tapa un cuarto de vuelta hacia la izquierda y saca el filtro viejo halándolo hacia afuera.",
                  "Quita la tapa del filtro viejo: se pasa al filtro nuevo, no la botes.",
                  "Pon la tapa en el filtro nuevo, mételo en el hueco y gira la tapa un cuarto de vuelta hacia la derecha hasta que quede alineada con la rejilla.",
                  "Saca unos 12 litros de agua por el dispensador para sacar el aire y el polvo de carbón."],
        "reset": "Reinicia el aviso: deja presionado 3 segundos el botón «Filter Reset» o «Water Filter» del panel.",
    },
    "wp-3-o": {
        "donde": "Dentro del refrigerador, arriba (a la derecha en la mayoría de modelos), en una caja con tapa: es el filtro de botón que se suelta empujando.",
        "tiempo": "2 minutos", "herramientas": "Ninguna, solo un trapo.",
        "pasos": ["Abre la tapa de la caja del filtro.",
                  "Empuja el filtro viejo hacia adentro y suéltalo: sale solo unos centímetros. Hálalo derecho; ten un trapo debajo.",
                  "Quítale la tapa protectora al filtro nuevo.",
                  "Mételo derecho y empújalo hasta que haga clic y quede firme.",
                  "Cierra la tapa y saca unos 12 litros de agua por el dispensador para sacar el aire y el polvo de carbón."],
        "reset": "Reinicia el aviso: deja presionado 3 segundos el botón «Filter Reset» o «Water Filter» del panel.",
    },
    "wp-4-o": {
        "donde": "Dentro del refrigerador, en la esquina de arriba a la derecha (o en el techo) en la mayoría de nevecones Whirlpool, Maytag, KitchenAid y Amana que usan el UKF8001.",
        "tiempo": "2 minutos", "herramientas": "Ninguna, solo un trapo.",
        "pasos": ["Si tiene tapa, ábrela."] + _INTERNO_GIRO + [
            "Saca unos 12 litros de agua por el dispensador para sacar el aire y el polvo de carbón."],
        "reset": "Reinicia el aviso: deja presionado 3 segundos el botón «Filter Reset» o «Water Filter» del panel.",
    },
    "wp-5-o": {
        "donde": "En la rejilla de abajo, al frente del nevecón (zócalo): es el filtro de botón de los Whirlpool, Maytag y KitchenAid lado a lado.",
        "tiempo": "3 minutos", "herramientas": "Ninguna, solo un trapo.",
        "pasos": ["Presiona el botón que está al lado del filtro en la rejilla de abajo: el filtro sale unos centímetros.",
                  "Hala el filtro viejo hacia afuera; ten un trapo debajo.",
                  "Quita la tapa del filtro viejo y pásala al nuevo (en algunos modelos la tapa ya viene puesta).",
                  "Mete el filtro nuevo derecho y empújalo hasta que haga clic y el botón vuelva a salir.",
                  "Saca unos 12 litros de agua por el dispensador para sacar el aire y el polvo de carbón."],
        "reset": "Reinicia el aviso: deja presionado 3 segundos el botón «Filter Reset» o «Water Filter» del panel.",
    },
    "wp-ex-o": dict(_EXTERNO),
    "ge-mwf-o": {
        "donde": "Dentro del refrigerador, arriba (atrás a la derecha en la mayoría de nevecones GE de dos puertas y French door), en una caja con tapa.",
        "tiempo": "2 minutos", "herramientas": "Ninguna, solo un trapo.",
        "pasos": ["Abre la tapa de la caja del filtro si tu modelo la tiene."] + _INTERNO_GIRO + [
            "Saca unos 12 litros de agua por el dispensador (unos 5 minutos, con pausas) para sacar el aire y el polvo de carbón."],
        "reset": "Reinicia el aviso: deja presionado 3 segundos el botón «Reset Water Filter» o «Filter» del panel.",
    },
    "ge-xwf-o": {
        "donde": "Dentro del refrigerador, en la esquina de arriba a la izquierda, detrás de una tapa (nevecones GE French door más nuevos).",
        "tiempo": "2 minutos", "herramientas": "Ninguna, solo un trapo.",
        "pasos": ["Abre la tapa del filtro."] + _INTERNO_GIRO + [
            "Cierra la tapa y saca unos 12 litros de agua por el dispensador para sacar el aire y el polvo de carbón."],
        "reset": "Reinicia el aviso: deja presionado 3 segundos el botón «Reset Water Filter» o «Filter» del panel.",
    },
}


def datos(p):
    return INSTALACION.get(p["id"]) or (dict(_EXTERNO) if "-ex-" in p["id"] else {
        "donde": "Dentro del refrigerador, arriba o en la rejilla de abajo según el modelo.", "tiempo": "2 minutos",
        "herramientas": "Ninguna, solo un trapo.", "pasos": _INTERNO_GIRO + ["Saca unos 4 litros de agua por el dispensador."],
        "reset": "Reinicia el aviso dejando presionado 3 segundos el botón «Filter» del panel."})


def tutorial_html(p, nombre=None):
    """Sección «Cómo instalar» con los pasos propios del filtro. id="instalacion" para enlazarla."""
    d = datos(p)
    nombre = nombre or p["ref"]
    return f"""<section class="caja tutorial" id="instalacion">
  <h2>Cómo instalar el filtro {esc(nombre)}: paso a paso</h2>
  <dl class="dq"><dt>Dónde va</dt><dd>{esc(d["donde"])}</dd><dt>Tiempo</dt><dd>{esc(d["tiempo"])}</dd><dt>Herramientas</dt><dd>{esc(d["herramientas"])}</dd></dl>
  <ol class="pasos">{"".join(f"<li>{esc(x)}</li>" for x in d["pasos"])}</ol>
  <p><b>Último paso:</b> {esc(d["reset"])}</p>
  <p class="m">Consejos: el agua de los primeros vasos puede salir turbia o con burbujas, es normal y se aclara en unos minutos. Bota el primer hielo que salga después del cambio. Si gotea, saca el filtro y vuelve a meterlo derecho hasta que quede firme. En Cali te lo instalamos gratis.</p>
</section>"""


def tutorial_ld(p, url, nombre=None):
    """Datos estructurados HowTo para Google y los asistentes de IA."""
    d = datos(p)
    nombre = nombre or p["ref"]
    pasos = d["pasos"] + [d["reset"]]
    return {"@type": "HowTo", "name": f"Cómo instalar el filtro de agua {nombre}", "totalTime": "PT15M" if "15" in d["tiempo"] else "PT3M",
            "supply": [{"@type": "HowToSupply", "name": f"Filtro {nombre}"}], "tool": [{"@type": "HowToTool", "name": "Trapo"}],
            "step": [{"@type": "HowToStep", "position": i + 1, "text": x, "url": f"{url}#instalacion"} for i, x in enumerate(pasos)]}
