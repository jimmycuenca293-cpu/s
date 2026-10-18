"""Contenido extra para la tienda Whirlpool: marcas a las que le sirven los filtros, preguntas frecuentes y blog.

- Una página por cada marca de nevera a la que le sirven los filtros Whirlpool EveryDrop (Maytag, KitchenAid, Jenn-Air,
  Amana, Kenmore, Estate) y por cada marca a la que le sirve el filtro externo.
- Preguntas frecuentes completas y blog, pensados para Google y para las respuestas de asistentes de IA.

Sin términos de marca prohibidos en Google Ads.
No usar este texto en anuncios de Google Ads. Las marcas citadas son de sus dueños y se nombran solo para indicar para qué neveras sirven.
"""
import html
import re

esc = lambda s: html.escape(str(s), quote=True)
cop = lambda n: "$ " + f"{n:,}".replace(",", ".")

# Marcas de la familia Whirlpool: les sirven los EveryDrop (según la ficha de cada filtro) y el externo
FAMILIA = {
    "Maytag": dict(alias=["MyTag", "Maitag", "Mei Tag", "Maytag"], prefijo="empieza por M (por ejemplo MFI2570FEZ)"),
    "KitchenAid": dict(alias=["Kitchen Aid", "Kitchen Eye", "Kichen Aid", "KitchenAid"], prefijo="empieza por K (por ejemplo KRFF305ESS o KRFF507ESS)"),
    "Jenn-Air": dict(alias=["Jenn Air", "Jennair", "Yen Air", "Jenn-Air"], prefijo="empieza por J"),
    "Amana": dict(alias=["Amana", "Amana nevecón", "Amana refrigerador"], prefijo="empieza por A"),
}
# Marcas a las que les sirve el filtro externo en línea (va en la manguera del agua)
EXTERNAS = ["Samsung", "LG", "GE", "Mabe", "Haceb", "Challenger", "Electrolux", "Frigidaire", "Bosch", "Hisense", "Midea", "Panasonic", "Daewoo", "Estate"]


def _marcas_de(p):
    """Marcas de la familia que nombra la ficha del filtro."""
    t = (p.get("desc") or "") + " " + (p.get("nota") or "")
    return [m for m in ("Whirlpool", "Maytag", "KitchenAid", "Jenn-Air", "Amana") if m.lower() in t.lower()]


def _modelos_de(ps, marca):
    pref = {"Whirlpool": "W", "Maytag": "M", "KitchenAid": "K", "Jenn-Air": "J", "Amana": "A"}[marca]
    return [(m, p) for p in ps for m in p["modelos"] if m.upper().startswith(pref)]


def rutas(base, slug, hub=None):
    """Rutas de todo el contenido extra (para menús, mapa del sitio y enlaces)."""
    r = {"familia": {}, "kenmore": [], "externas": {}, "hub": hub or f"{base}filtros-para-nevera-por-marca/", "faq": f"{base}preguntas-frecuentes/", "blog": f"{base}blog/"}
    for m in FAMILIA:
        s = slug(m)
        r["familia"][m] = [(f"{base}filtro-para-nevera-{s}/", f"Filtro para nevera {m}"), (f"{base}precio-filtro-nevera-{s}/", f"Precio del filtro {m}"),
                           (f"{base}como-cambiar-filtro-nevera-{s}/", f"Cómo cambiar el filtro {m}"), (f"{base}cada-cuanto-cambiar-filtro-nevera-{s}/", f"Cada cuánto cambiar el filtro {m}")]
    r["kenmore"] = [(f"{base}filtro-para-nevera-kenmore/", "Filtro para nevera Kenmore"), (f"{base}filtros-kenmore-46-9930-46-9081-46-9030-46-9006-46-9010/", "Referencias Kenmore 46-9xxx")]
    for m in EXTERNAS:
        r["externas"][m] = f"{base}filtro-externo-para-nevera-{slug(m)}/"
    return r


def articulos(ps, base="/", inst="/cambio-e-instalacion/"):
    """Blog: [(slug, titulo, descripcion, resumen, cuerpo_html, preguntas)]."""
    por = {p["ref"]: p for p in ps}
    e1, e2, e3, e4, e5, ex = (por[k] for k in ("EDR1RXD1", "EDR2RXD1", "EDR3RXD1", "EDR4RXD1", "EDR5RXD1", "4378411RB"))
    precios = sorted({p["precio"] for p in ps})
    rango = f"{cop(precios[0])} a {cop(precios[-1])}"
    A = []

    def a(slug_, titulo, desc, resumen, cuerpo, preguntas):
        cuerpo = cuerpo.replace('href="/filtro-para-nevera-', f'href="{base}filtro-para-nevera-').replace('/cambio-e-instalacion/', inst)
        A.append((slug_, titulo, desc, resumen, cuerpo, preguntas))

    a("como-saber-que-filtro-everydrop-necesita-tu-nevera-whirlpool", "Cómo saber qué filtro EveryDrop necesita tu nevera Whirlpool",
      "Tres pasos para saber si tu nevera Whirlpool, Maytag, KitchenAid, Jenn-Air o Amana usa el filtro EveryDrop 1, 2, 3, 4 o 5.",
      "Mira el número grande de la caja del filtro viejo (1 a 5) o la referencia que empieza por EDR; si no la tienes, el modelo de la nevera te dice cuál es.",
      "<p>Los filtros <b>EveryDrop</b> se numeran del 1 al 5. Cada número tiene forma y lugar distintos, así que no se pueden cambiar entre sí. Estos son los tres caminos para encontrar el tuyo.</p>"
      "<h2>1. Mira el filtro viejo</h2><p>Sácalo y busca la referencia impresa: <span class=\"ref\">EDR1RXD1</span> es el EveryDrop 1, <span class=\"ref\">EDR2RXD1</span> el 2, y así hasta el <span class=\"ref\">EDR5RXD1</span>. También puede traer el código de la marca, como W10295370A, UKF8001 o 4396841: todos son equivalentes de alguno de los cinco.</p>"
      "<h2>2. Mira el modelo de la nevera</h2><p>La etiqueta está dentro del refrigerador, en una pared lateral de arriba. En Whirlpool suele empezar por WRF, WRS o WRX; en KitchenAid por K; en Maytag por M. Con el modelo y la forma del filtro se confirma la referencia.</p>"
      "<h2>3. Fíjate dónde va y cómo se saca</h2><ul class=\"m-ok\"><li>Se cambia girándolo, adentro del refrigerador: es el caso del EveryDrop 4 y de otros según el modelo.</li><li>Está en la rejilla de abajo, al frente, y se suelta con un botón: EveryDrop 3.</li></ul>"
      "<p>Si dudas, mándanos la foto del filtro viejo o de la etiqueta y te confirmamos antes de que compres.</p>",
      [("¿Un EveryDrop 2 sirve en una nevera que usa el 1?", "No. Cada número tiene forma y conexión propias; hay que usar el mismo número del filtro que tiene la nevera."),
       ("¿Dónde está el número del EveryDrop?", "Viene grande en la caja y la referencia EDR va impresa en el filtro.")])
    a("diferencias-entre-filtros-everydrop-1-2-3-4-y-5", "Diferencias entre los filtros EveryDrop 1, 2, 3, 4 y 5",
      "Qué cambia entre EveryDrop 1, 2, 3, 4 y 5: forma, lugar de instalación, equivalentes y para qué neveras se usan.",
      "Los cinco filtran el agua igual de bien; lo que cambia es la forma, el lugar donde van y la nevera que los usa. Por eso no son intercambiables.",
      "<p>Todos los EveryDrop reducen el cloro, el sabor y el olor del agua. La diferencia está en el <b>encaje</b>: cada número es para una familia de neveras.</p>"
      f"<ul class=\"m-ok\"><li><b>EveryDrop 1 ({esc(e1['ref'])})</b>: {esc(e1['desc'])}</li><li><b>EveryDrop 2 ({esc(e2['ref'])})</b>: {esc(e2['desc'])}</li><li><b>EveryDrop 3 ({esc(e3['ref'])})</b>: {esc(e3['desc'])}</li>"
      f"<li><b>EveryDrop 4 ({esc(e4['ref'])})</b>: {esc(e4['desc'])}</li><li><b>EveryDrop 5 ({esc(e5['ref'])})</b>: {esc(e5['desc'])}</li></ul>"
      f"<p>Precios: entre {rango} con envío gratis. Mira el <a href=\"/\">catálogo completo</a>.</p>",
      [("¿Cuál EveryDrop es el más común?", "Depende de tu modelo: cada número es para una familia de neveras. El EveryDrop 4 (EDR4RXD1) es el mismo UKF8001."),
       ("¿Se pueden usar en cualquier nevera?", "No. Solo en las que usan ese número; para neveras sin filtro de fábrica existe el filtro externo.")])
    a("filtro-para-nevera-kitchenaid-guia-de-compra", "Filtro para nevera KitchenAid: guía para comprar el correcto",
      "Qué filtros EveryDrop sirven en neveras KitchenAid, cómo saber cuál usa tu modelo y cuánto cuestan.",
      "Las neveras KitchenAid usan filtros EveryDrop: el 1, 2, 3, 4 o 5 según el modelo. Los KRFF305ESS y KRFF507ESS son ejemplos conocidos.",
      "<p>KitchenAid y Whirlpool son de la misma familia de electrodomésticos, y por eso comparten filtros. Si tu nevera es KitchenAid, lo más probable es que use un <b>EveryDrop</b>.</p>"
      f"<h2>Ejemplos de modelos</h2><ul class=\"m-ok\"><li>KRFF305ESS usa el {esc(e1['nombre_largo'])}.</li><li>KRFF507ESS usa el {esc(e4['nombre_largo'])}.</li></ul>"
      "<h2>Cómo confirmar el tuyo</h2><p>Mira el modelo en la etiqueta interna (empieza por K) y la referencia del filtro viejo. Si no coinciden con estos ejemplos, escríbenos con una foto.</p>"
      "<p>Compra directo en la página <a href=\"/filtro-para-nevera-kitchenaid/\">Filtro para nevera KitchenAid</a>.</p>",
      [("¿Cada cuánto se cambia el filtro de una KitchenAid?", "Cada 6 meses, o antes si el agua cambia de sabor."),
       ("¿Qué pasa si escribo mal el nombre, como Kitchen Aid?", "No importa: es la misma marca. Aquí está con las formas más comunes de escribirla.")])
    a("filtro-para-nevera-maytag-cual-es-y-como-cambiarlo", "Filtro para nevera Maytag: cuál es y cómo cambiarlo",
      "El filtro de agua de las neveras Maytag (también escrito MyTag o Maitag): referencias EveryDrop y cambio paso a paso.",
      "Las neveras Maytag usan filtros EveryDrop. El MFI2570FEZ, por ejemplo, usa el EveryDrop 4 (UKF8001).",
      "<p>Si buscas el filtro de una nevera <b>Maytag</b> (a veces escrita «MyTag» o «Maitag»), casi siempre es un EveryDrop de Whirlpool.</p>"
      f"<ul class=\"m-ok\"><li>MFI2570FEZ: {esc(e4['nombre_largo'])}.</li></ul><h2>Cómo cambiarlo</h2><ol>"
      + "".join(f"<li>{esc(x)}</li>" for x in __import__('instalacion').datos(e4)["pasos"]) + "</ol>"
      "<p>Más en <a href=\"/filtro-para-nevera-maytag/\">Filtro para nevera Maytag</a>.</p>",
      [("¿MyTag es lo mismo que Maytag?", "Sí, es la misma marca; mucha gente la escribe así."),
       ("¿Sirve el mismo filtro para todas las Maytag?", "No: depende del modelo. Confirma con la referencia del filtro viejo.")])
    a("filtros-kenmore-46-9930-46-9081-46-9030-46-9006-46-9010-equivalencias", "Filtros Kenmore 46-9930, 46-9081, 46-9030, 46-9006 y 46-9010: equivalencias",
      "Qué filtro EveryDrop equivale a cada referencia Kenmore 46-9xxx para neveras.",
      "46-9930 = EDR1RXD1, 46-9081 = EDR2RXD1, 46-9030 = EDR3RXD1, 46-9006 = EDR4RXD1 y 46-9010 = EDR5RXD1.",
      "<table class=\"m-tabla\"><tr><th>Kenmore</th><th>EveryDrop</th></tr><tr><td>46-9930</td><td>EDR1RXD1</td></tr><tr><td>46-9081</td><td>EDR2RXD1</td></tr><tr><td>46-9030</td><td>EDR3RXD1</td></tr><tr><td>46-9006</td><td>EDR4RXD1</td></tr><tr><td>46-9010</td><td>EDR5RXD1</td></tr></table>"
      "<p>Si el filtro de tu nevera Kenmore trae uno de estos números, el EveryDrop de la derecha es su equivalente. Mira <a href=\"/filtro-para-nevera-kenmore/\">Filtro para nevera Kenmore</a>.</p>",
      [("¿Qué filtro es el Kenmore 46-9930?", "Equivale al EveryDrop 1 (EDR1RXD1)."), ("¿Qué filtro es el Kenmore 46-9006?", "Equivale al EveryDrop 4 (EDR4RXD1), igual al UKF8001.")])
    a("por-que-el-agua-de-la-nevera-sabe-a-plastico-o-a-cloro", "Por qué el agua de la nevera sabe a plástico o a cloro",
      "Causas del sabor a plástico o a cloro en el agua de la nevera y cómo corregirlo en minutos.",
      "La causa más común es un filtro vencido o recién instalado sin purgar. Cámbialo y bota unos 6 litros de agua.",
      "<ul class=\"m-ok\"><li><b>Filtro vencido:</b> después de unos 6 meses ya no retiene el cloro.</li><li><b>Filtro nuevo sin purgar:</b> deja salir 6 litros por el dispensador.</li><li><b>Agua quieta:</b> si casi no usas el dispensador, bota unos vasos.</li>"
      "<li><b>Hielo viejo:</b> bótalo y deja que se haga hielo nuevo.</li></ul><p>Tienes el paso a paso en <a href=\"/cambio-e-instalacion/\">cómo cambiar el filtro</a>.</p>",
      [("¿El sabor a plástico es peligroso?", "Un filtro vencido no filtra bien; lo mejor es cambiarlo y purgar el agua."), ("¿Cuánto tarda en irse el sabor?", "Debe desaparecer al botar los primeros litros con el filtro nuevo.")])
    a("cada-cuanto-cambiar-el-filtro-de-la-nevera-whirlpool-y-por-que", "Cada cuánto cambiar el filtro de la nevera Whirlpool y por qué",
      "El filtro de agua de la nevera Whirlpool se cambia cada 6 meses. Qué pasa si esperas más y cómo no olvidarlo.",
      "Cada 6 meses. Después de ese tiempo el carbón activado está saturado y deja pasar cloro y sedimento.",
      "<p>El filtro tiene carbón activado que se va llenando. A los 6 meses, aunque se vea bien, ya no filtra igual. Con mucho uso o agua con sedimento, cámbialo antes.</p>"
      "<ul class=\"m-ok\"><li>Anota la fecha en el filtro con un marcador.</li><li>Pon una alarma en el celular para dentro de 6 meses.</li><li>Compra el pack de 2 y tendrás el siguiente listo.</li></ul>",
      [("¿Puedo estirar el cambio a 8 meses?", "No conviene: el agua sale con peor sabor y el filtro se tapa."), ("¿Se puede lavar el filtro?", "No, el carbón activado no se recupera lavándolo.")])
    a("como-reiniciar-la-luz-del-filtro-whirlpool-order-y-replace", "Cómo reiniciar la luz del filtro Whirlpool: Order y Replace",
      "Qué significan las luces «Order» y «Replace» de tu nevera Whirlpool y cómo reiniciar el aviso después de cambiar el filtro.",
      "«Order» pide que compres el filtro y «Replace» que lo cambies ya. Después de cambiarlo, deja presionado el botón del filtro unos 3 segundos.",
      "<p>En muchas neveras Whirlpool la luz pasa de «Order» (pide el filtro) a «Replace» (cámbialo ya). La luz cuenta tiempo, no mide la suciedad.</p>"
      "<ol><li>Cambia el filtro.</li><li>Deja presionado el botón del filtro (o «Filter Reset») unos 3 segundos.</li><li>Verifica que la luz se apague. Si no, mantén el botón unos segundos más.</li></ol>"
      "<p>Según el modelo cambia el nombre del botón. Si tu panel tiene bloqueo, desbloquéalo primero.</p>",
      [("¿Por qué sigue la luz prendida con el filtro nuevo?", "Falta reiniciar el aviso a mano."), ("¿Puedo apagar la luz sin cambiar el filtro?", "Se puede, pero no conviene: el filtro vencido deja pasar cloro y sedimento.")])
    a("filtro-externo-o-interno-cual-conviene-para-tu-nevera", "Filtro externo o interno: cuál conviene para tu nevera",
      "Diferencias entre el filtro interno EveryDrop y el filtro externo de manguera, y cuándo usar cada uno.",
      "El interno va dentro del refrigerador y es específico de cada modelo; el externo va en la manguera del agua y sirve cuando la nevera no trae filtro.",
      f"<p>El filtro <b>interno</b> (EveryDrop) es el de fábrica. El <b>externo</b> ({esc(ex['ref'])}) se conecta a la manguera, por detrás: sirve si tu nevera no trae filtro adentro o como filtro adicional. Cuesta {cop(ex['precio'])}.</p>"
      "<ul class=\"m-ok\"><li>Si tu nevera tiene tapa de filtro, usa el interno.</li><li>Si no la tiene y hay dispensador, el externo es la solución.</li></ul>",
      [("¿El externo reemplaza al interno?", "No: si ya tienes interno, el externo es adicional."), ("¿Se instala sin técnico?", "Sí, con racores rápidos, en 10 a 15 minutos.")])
    a("como-cuidar-la-maquina-de-hielo-de-tu-nevera", "Cómo cuidar la máquina de hielo de tu nevera",
      "Hábitos simples para que el hielo salga claro y sin mal sabor: filtro al día, limpieza y buen uso.",
      "Filtro cada 6 meses, hielo viejo fuera y comida tapada. Con eso la máquina rinde más y el hielo sale claro.",
      "<ul class=\"m-ok\"><li>Cambia el filtro cada 6 meses.</li><li>Bota el hielo viejo y deja que se haga nuevo.</li><li>Tapa los alimentos con olor fuerte.</li><li>Revisa que la máquina no esté apagada («Ice Off»).</li></ul>",
      [("¿Por qué el hielo sale pequeño?", "Casi siempre llega poca agua por un filtro tapado."), ("¿Por qué sale turbio?", "Un poco es normal; si trae partículas, cambia el filtro.")])
    a("cuanto-cuesta-mantener-agua-filtrada-en-casa-filtro-vs-botellon", "Cuánto cuesta tener agua filtrada en casa: filtro de nevera vs botellón",
      "Compara el costo anual de un filtro de nevera frente a comprar botellones.",
      f"Un filtro de nevera ({rango}) dura 6 meses y filtra el agua y el hielo de toda la familia.",
      "<p>El filtro de la nevera filtra el agua del dispensador y el hielo sin que cargues botellones. Dos filtros al año cubren los 12 meses; con el <b>pack de 2</b> pagas menos por unidad.</p>"
      "<p>El costo depende del consumo de tu casa; haz la cuenta con lo que gastas hoy en agua embotellada.</p>",
      [("¿El filtro de nevera reemplaza el botellón?", "Filtra el agua del grifo que llega a la nevera; el sabor mejora, pero depende del agua de tu ciudad.")])
    a("errores-al-cambiar-el-filtro-de-la-nevera-y-como-evitarlos", "Errores al cambiar el filtro de la nevera y cómo evitarlos",
      "Los errores más comunes al cambiar el filtro de agua de la nevera: tapa protectora, referencia equivocada, aire en la línea.",
      "Los más comunes: dejar la tapa protectora, comprar otro número de filtro y no purgar el aire.",
      "<ol><li><b>Dejar la tapa protectora</b> del filtro nuevo: no pasa agua.</li><li><b>Comprar otra referencia</b>: no encaja y gotea.</li><li><b>No purgar</b>: saca 6 litros para limpiar el aire.</li><li><b>No reiniciar la luz</b>.</li><li><b>No girar hasta el tope</b>.</li></ol>",
      [("¿Qué hago si goteó?", "Cierra el agua, sácalo y vuelve a instalarlo hasta el fondo.")])
    a("como-leer-el-modelo-de-tu-nevera-whirlpool", "Cómo leer el modelo de tu nevera Whirlpool",
      "Dónde está la etiqueta del modelo y qué significan sus letras en neveras Whirlpool, KitchenAid y Maytag.",
      "La etiqueta está dentro del refrigerador, en una pared lateral de arriba. Whirlpool suele empezar por WRF, WRS o WRX.",
      "<p>Abre el refrigerador y busca una etiqueta con «Model». Las primeras letras indican la marca y la línea: <b>WRF</b>, <b>WRS</b> y <b>WRX</b> en Whirlpool; <b>K</b> en KitchenAid; <b>M</b> en Maytag. Con ese modelo y la referencia del filtro viejo escoges el filtro.</p>",
      [("¿Qué hago si la etiqueta no se lee?", "Mándanos la foto del filtro viejo y te confirmamos.")])
    a("que-hacer-si-el-filtro-de-la-nevera-gotea", "Qué hacer si el filtro de la nevera gotea",
      "Causas del goteo del filtro de la nevera y soluciones paso a paso.",
      "Casi siempre es un filtro mal encajado, de otra referencia o con el empaque pellizcado.",
      "<ol><li>Cierra el agua y saca el filtro.</li><li>Revisa que sea la referencia correcta.</li><li>Mira que el aro de caucho esté bien.</li><li>Vuelve a ponerlo hasta el fondo y gíralo hasta que quede firme.</li><li>En el externo, revisa los racores y la flecha.</li></ol>",
      [("¿Un filtro que gotea daña el piso?", "Puede hacerlo; cierra el agua mientras lo revisas.")])
    return A


def preguntas_ia(ps, slug):
    """Preguntas y respuestas directas para Google y asistentes de IA. [(grupo, [(pregunta, respuesta)])]"""
    por = {p["ref"]: p for p in ps}
    r = lambda k: por[k]["ref"]
    precios = sorted({p["precio"] for p in ps})
    rango = f"{cop(precios[0])} a {cop(precios[-1])}"
    G = []
    G.append(("Marcas de nevera", [
        ("¿Qué filtro de agua le sirve a una nevera Whirlpool?", f"Los EveryDrop 1 a 5 ({', '.join(por[k]['ref'] for k in ('EDR1RXD1','EDR2RXD1','EDR3RXD1','EDR4RXD1','EDR5RXD1'))}). Cuál usa tu nevera depende del modelo y de la referencia del filtro viejo."),
        ("¿El filtro Whirlpool EveryDrop sirve para neveras KitchenAid?", "Sí. Las neveras KitchenAid usan filtros EveryDrop; por ejemplo, la KRFF305ESS usa el EveryDrop 1 y la KRFF507ESS el EveryDrop 4."),
        ("¿Qué filtro usa una nevera Maytag (MyTag)?", "También un EveryDrop. La Maytag MFI2570FEZ, por ejemplo, usa el EveryDrop 4 (UKF8001)."),
        ("¿Sirve para neveras Jenn-Air y Amana?", "Para Jenn-Air sirven los EveryDrop 1, 3, 4 y 5; para Amana, del 1 al 5. El EveryDrop 2 es para Whirlpool, Maytag, KitchenAid y Amana."),
        ("¿Qué equivale a los filtros Kenmore 46-9930, 46-9081, 46-9030, 46-9006 y 46-9010?", "46-9930 = EDR1RXD1, 46-9081 = EDR2RXD1, 46-9030 = EDR3RXD1, 46-9006 = EDR4RXD1 y 46-9010 = EDR5RXD1."),
        ("¿Hay filtro para neveras de otras marcas como Samsung, LG o Mabe?", "El filtro externo 4378411RB se conecta a la manguera del agua y sirve en neveras con dispensador de varias marcas. Para el filtro interno de esas marcas hay que usar el suyo."),
        ("¿Qué es el UKF8001?", "Es la referencia de marca del EveryDrop 4 (EDR4RXD1)."),
    ]))
    G.append(("Escoger y comprar", [
        ("¿Cómo sé qué filtro necesita mi nevera?", "Mira la referencia impresa en el filtro viejo o el modelo en la etiqueta interna. Si dudas, mándanos la foto y te confirmamos antes de comprar."),
        ("¿Cuánto cuesta un filtro para nevera Whirlpool?", f"Entre {rango}, con envío gratis a toda Colombia."),
        ("¿Hacen envíos a toda Colombia?", "Sí, el envío es gratis a toda Colombia y llega en 2 a 3 días hábiles a las principales ciudades."),
        ("¿Se puede pagar contra entrega?", "No. El pago es solo en línea: tarjeta débito o crédito, PSE, Nequi o botón Bancolombia, en una página segura de Wompi."),
        ("¿Es seguro pagar en la tienda?", "Sí. El pago se hace en la página segura de Wompi; la tienda nunca ve los datos de tu tarjeta."),
        ("¿Qué pasa si me equivoco de filtro?", "Tienes 5 días hábiles para retractarte, con el filtro sin instalar y en su empaque."),
        ("¿Venden el pack de 2 filtros?", "Sí, el pack anual de 2 filtros sale más barato por unidad y cubre 12 meses."),
        ("¿Me dan factura o recibo?", "Te llega el recibo del pago a tu correo apenas Wompi confirma la compra."),
    ]))
    G.append(("Instalación y uso", [
        ("¿Cada cuánto se cambia el filtro de la nevera?", "Cada 6 meses, o antes si el agua cambia de sabor, el dispensador bota menos agua o se prende la luz del filtro."),
        ("¿Necesito un técnico para cambiarlo?", "No. Los internos se cambian en un par de minutos y los externos en 10 a 15, sin herramientas."),
        ("¿Cómo apago la luz del filtro?", "Deja presionado el botón del filtro (o «Filter Reset») unos 3 segundos después de cambiarlo."),
        ("¿Qué significan «Order» y «Replace»?", "«Order» pide que consigas el filtro y «Replace» que lo cambies ya."),
        ("¿Por qué sale aire o agua turbia con el filtro nuevo?", "Es normal: el filtro nuevo suelta aire y polvo de carbón. Saca unos 6 litros por el dispensador."),
        ("¿Se puede lavar el filtro y volverlo a usar?", "No. El carbón activado se satura y lavarlo no lo recupera."),
        ("¿Puedo usar la nevera sin filtro?", "Algunos modelos traen un tapón para eso, pero el agua sale sin filtrar."),
    ]))
    G.append(("Problemas frecuentes", [
        ("¿Por qué no sale agua después de cambiar el filtro?", "Casi siempre está mal puesto, no se purgó el aire o es otra referencia. Reinstálalo hasta el fondo y saca agua por tandas."),
        ("¿Por qué gotea el filtro?", "Por estar mal encajado, ser de otra referencia o tener el empaque pellizcado."),
        ("¿Por qué el agua sabe a cloro o a plástico?", "Por un filtro vencido o recién puesto sin purgar."),
        ("¿Por qué el hielo sale pequeño o turbio?", "Suele ser un filtro tapado que deja pasar poca agua; cámbialo."),
    ]))
    G.append(("Sobre la tienda", [
        ("¿Son distribuidores autorizados de Whirlpool?", "Sí. Somos distribuidor autorizado de Whirlpool en Colombia."),
        ("¿Cómo los contacto?", "Por WhatsApp y por el correo de la tienda; atendemos en el horario que aparece al final de cada página."),
        ("¿Entregan en mi ciudad?", "Enviamos a 126 ciudades y municipios y a otros lugares de Colombia; en cada página de ciudad ves el tiempo de entrega."),
    ]))
    return G


def generar(pagina, ctx, h, R):
    """Escribe las páginas de más marcas, preguntas frecuentes y blog. Devuelve las rutas."""
    marca, ps, base, M, ubic = ctx["marca"], ctx["ps"], ctx["base"], ctx["M"], ctx["ubic"]
    slug = ctx["slug"]
    X = R["extra"]
    datos = ctx["datos"]
    rp = ctx.get("rp") or (lambda p: f'{base}{p["slug_o"]}/')
    inst = ctx.get("inst", "/cambio-e-instalacion/")
    internos = [p for p in ps if ubic(p) == "interno"]
    externo = next(p for p in ps if ubic(p) == "externo")
    n_pag = []

    def tabla(lista, marca_filtro=None):
        filas = ""
        for p in lista:
            sirve = _marcas_de(p)
            aplica = (marca_filtro is None) or (marca_filtro in sirve) or ubic(p) == "externo"
            equiv = ", ".join(x for x in p["refs"] if x != p["ref"])
            filas += (f'<tr><td><a href="{rp(p)}">{esc(p["nombre_largo"])}</a></td><td><span class="ref">{esc(p["ref"])}</span><br><small>{esc(equiv)}</small></td>'
                      f'<td>{"Externo" if ubic(p) == "externo" else "Interno"}</td><td><b>{cop(p["precio"])}</b></td><td>{"Sirve" if aplica else "No aplica"}</td></tr>')
        return ('<div class="m-tabla-wrap"><table class="m-tabla"><thead><tr><th>Filtro</th><th>Referencia y equivalentes</th><th>Tipo</th><th>Precio</th>'
                f'<th>{esc(marca_filtro) if marca_filtro else "Neveras"}</th></tr></thead><tbody>{filas}</tbody></table></div>')

    def respuesta(txt):
        return f'<div class="m-respuesta"><b>Respuesta rápida</b><p>{txt}</p></div>'

    def ok(p, w):
        return w in _marcas_de(p)

    # ---------- marcas de la familia ----------
    for m, f in FAMILIA.items():
        s = slug(m)
        lista = [p for p in ps if ok(p, m) or ubic(p) == "externo"]
        modelos = _modelos_de(ps, m)
        refs = ", ".join(p["ref"] for p in lista if ubic(p) == "interno")
        alias = ", ".join(f["alias"])
        modelos_txt = (", ".join(f"{mo} (usa el {p['ref']})" for mo, p in modelos)) if modelos else "Aún no tenemos un modelo publicado: escríbenos el tuyo y te confirmamos"
        faq = [(f"¿Qué filtro de agua le sirve a una nevera {m}?", f"Los filtros EveryDrop {refs}. Cuál usa tu nevera {m} depende del modelo; con la referencia del filtro viejo o el modelo te confirmamos."),
               (f"¿{m} también se escribe {f['alias'][0]}?", f"Sí. Muchas personas buscan {alias}. Es la misma marca."),
               (f"¿El filtro EveryDrop de Whirlpool sirve en {m}?", f"Sí: {m} es de la familia Whirlpool y usa filtros EveryDrop según el modelo."),
               (f"¿Cada cuánto cambio el filtro de mi nevera {m}?", "Cada 6 meses, o antes si el agua cambia de sabor o el dispensador bota menos agua."),
               (f"¿Cómo ubico el modelo de mi nevera {m}?", f"Busca la etiqueta dentro del refrigerador, en una pared lateral de arriba; el modelo {f['prefijo']}."),
               ("¿Puedo pagar contra entrega?", "No. El pago es solo en línea, con tarjeta, PSE, Nequi o botón Bancolombia.")]
        nota = f'<p class="m-mut" style="margin-top:18px">{esc(m)} es una marca registrada de su dueño; se nombra aquí solo para indicar para qué neveras sirven estos filtros.</p>'
        pagina(f"{base}filtro-para-nevera-{s}/", f"Filtro para nevera {m} | Filtros EveryDrop, envío gratis",
               f"Filtros de agua para neveras {m} ({alias}): EveryDrop {refs}. Equivalencias, precios y cómo cambiarlo. Envío gratis a toda Colombia.",
               f"Filtro de agua para nevera {m}", f"Para neveras {m}",
               f"Los filtros EveryDrop de Whirlpool sirven en neveras {esc(m)}. Aquí ves cuál le sirve a tu modelo, sus equivalencias y el precio, con envío gratis.",
               respuesta(f"Una nevera {esc(m)} usa un filtro <b>EveryDrop</b>. Los que sirven son: {esc(refs)}. Se cambia cada 6 meses.")
               + "<h2 style=\"font-size:22px;margin:22px 0 12px\">Filtros que le sirven a " + esc(m) + "</h2>" + tabla(lista, m)
               + f'<h2 style="font-size:22px;margin:26px 0 12px">Modelos {esc(m)} y su filtro</h2><p>{esc(modelos_txt)}.</p>'
               + f'<h2 style="font-size:22px;margin:26px 0 12px">Otras formas de buscarlo</h2><p>Mucha gente lo busca como: {esc(alias)}. También puedes buscar por la referencia del filtro: {esc(", ".join(x for p in lista for x in p["refs"][:3]))}.</p>' + nota,
               faq, miga_nombre=f"Filtro para nevera {m}")
        precios = ", ".join(f"{p['ref']}: {cop(p['precio'])}" for p in lista)
        pagina(f"{base}precio-filtro-nevera-{s}/", f"Precio del filtro de nevera {m} en Colombia 2026 | EveryDrop",
               f"Cuánto cuesta el filtro de agua para nevera {m} en Colombia: {precios}. Envío gratis y pago seguro en línea.",
               f"Precio del filtro de nevera {m} en Colombia", "Precios 2026",
               f"Precios de los filtros para neveras {esc(m)}, con el envío incluido a toda Colombia. El pack de 2 filtros sale más barato por unidad.",
               respuesta(f"El filtro para nevera {esc(m)} cuesta entre {cop(min(p['precio'] for p in lista))} y {cop(max(p['precio'] for p in lista))} con envío gratis.") + tabla(lista, m) + nota,
               [(f"¿Cuánto cuesta el filtro de una nevera {m}?", f"Entre {cop(min(p['precio'] for p in lista))} y {cop(max(p['precio'] for p in lista))}, según la referencia."),
                ("¿El envío tiene costo?", "No, es gratis a toda Colombia.")], miga_nombre=f"Precio filtro {m}")
        pasos = "".join(f'<div class="m-bloque"><h3><a href="{rp(p)}#instalacion">{esc(p["nombre_largo"])}</a></h3><p><b>Dónde va:</b> {esc(datos(p)["donde"])}</p><ol>'
                        + "".join(f"<li>{esc(x)}</li>" for x in datos(p)["pasos"]) + f'</ol><p><b>Último paso:</b> {esc(datos(p)["reset"])}</p></div>' for p in lista if ubic(p) == "interno")
        pagina(f"{base}como-cambiar-filtro-nevera-{s}/", f"Cómo cambiar el filtro de la nevera {m} paso a paso",
               f"Paso a paso para cambiar el filtro de agua de una nevera {m}, referencia por referencia (EveryDrop {refs}).",
               f"Cómo cambiar el filtro de la nevera {m}", "Paso a paso",
               f"Cambiar el filtro de tu nevera {esc(m)} toma unos minutos y no necesitas técnico. Busca tu referencia y sigue los pasos.",
               respuesta("Saca el filtro viejo, instala el nuevo hasta el fondo, bota unos 6 litros de agua y reinicia la luz del filtro.") + '<div class="m-cols">' + pasos + "</div>" + nota,
               [("¿Necesito herramientas?", "No. Los filtros internos se cambian sin herramientas."), ("¿Cuánto tarda?", "Un par de minutos.")], miga_nombre=f"Cómo cambiar el filtro {m}")
        pagina(f"{base}cada-cuanto-cambiar-filtro-nevera-{s}/", f"¿Cada cuánto cambiar el filtro de la nevera {m}? | Señales",
               f"El filtro de agua de la nevera {m} se cambia cada 6 meses. Señales de que ya toca y qué filtro EveryDrop usar.",
               f"¿Cada cuánto se cambia el filtro de la nevera {m}?", "Cada 6 meses",
               f"La respuesta corta: <b>cada 6 meses</b>. Si usan mucho hielo o el agua trae sedimento, antes.",
               respuesta(f"El filtro de una nevera {esc(m)} se cambia cada 6 meses.")
               + '<ul class="m-ok"><li>Pasaron 6 meses.</li><li>El agua o el hielo saben a cloro, a tierra o a plástico.</li><li>El dispensador bota menos agua.</li><li>Se prendió la luz del filtro.</li></ul>'
               + f'<p>Filtros que sirven: <a href="{base}filtro-para-nevera-{s}/">ver la lista para {esc(m)}</a>.</p>' + nota,
               faq[3:5], miga_nombre=f"Cada cuánto cambiar {m}")
    # ---------- Kenmore ----------
    ken = [(p, [x for x in p["refs"] if x.startswith("46-")]) for p in internos]
    ken = [(p, k[0]) for p, k in ken if k]
    filas_k = "".join(f'<tr><td><span class="ref">{esc(k)}</span></td><td><a href="{rp(p)}">{esc(p["nombre_largo"])}</a></td><td>{cop(p["precio"])}</td></tr>' for p, k in ken)
    tk = f'<div class="m-tabla-wrap"><table class="m-tabla"><thead><tr><th>Referencia Kenmore</th><th>Filtro equivalente</th><th>Precio</th></tr></thead><tbody>{filas_k}</tbody></table></div>'
    faqk = [("¿Qué filtro equivale al Kenmore 46-9930?", "El EveryDrop 1 (EDR1RXD1)."), ("¿Qué filtro equivale al Kenmore 46-9006?", "El EveryDrop 4 (EDR4RXD1), igual al UKF8001."),
            ("¿Qué filtro equivale al Kenmore 46-9081?", "El EveryDrop 2 (EDR2RXD1)."), ("¿Y al 46-9030?", "El EveryDrop 3 (EDR3RXD1)."), ("¿Y al 46-9010?", "El EveryDrop 5 (EDR5RXD1).")]
    nota_k = '<p class="m-mut" style="margin-top:18px">Kenmore es una marca registrada de su dueño; se nombra aquí solo para indicar equivalencias de referencias.</p>'
    pagina(f"{base}filtro-para-nevera-kenmore/", "Filtro para nevera Kenmore | Equivalencias 46-9930, 46-9081, 46-9030, 46-9006, 46-9010",
           "Filtros de agua para nevera Kenmore: qué EveryDrop equivale a cada referencia Kenmore 46-9xxx. Envío gratis a toda Colombia.",
           "Filtro de agua para nevera Kenmore", "Para neveras Kenmore",
           "Si el filtro de tu nevera Kenmore dice 46-9930, 46-9081, 46-9030, 46-9006 o 46-9010, este es el filtro equivalente.",
           respuesta("Cada referencia Kenmore 46-9xxx tiene un EveryDrop equivalente: mira la tabla.") + tk + nota_k, faqk, miga_nombre="Filtro para nevera Kenmore")
    pagina(f"{base}filtros-kenmore-46-9930-46-9081-46-9030-46-9006-46-9010/", "Filtros Kenmore 46-9930, 46-9081, 46-9030, 46-9006 y 46-9010: equivalencias",
           "Tabla de equivalencias de los filtros Kenmore 46-9930, 46-9081, 46-9030, 46-9006 y 46-9010 con los EveryDrop de Whirlpool.",
           "Filtros Kenmore 46-9xxx y su equivalente", "Equivalencias",
           "Busca tu referencia Kenmore y mira el filtro equivalente con su precio.", tk + nota_k, faqk, miga_nombre="Referencias Kenmore")
    # ---------- filtro externo por marca ----------
    for m in EXTERNAS:
        faq = [(f"¿El filtro externo sirve para una nevera {m}?", f"Sí, si tu nevera {m} tiene dispensador o máquina de hielo con conexión de agua: el filtro se conecta a la manguera, por detrás."),
               (f"¿Reemplaza el filtro interno de mi nevera {m}?", "No. Si tu nevera ya trae filtro adentro, el externo es adicional."),
               ("¿Se instala sin técnico?", "Sí, con racores rápidos y sin herramientas especiales, en 10 a 15 minutos."),
               ("¿Cada cuánto se cambia?", "Cada 6 meses.")]
        pagina(X["externas"][m], f"Filtro externo para nevera {m} | Envío gratis",
               f"Filtro externo de manguera para neveras {m}, referencia {externo['ref']}: {cop(externo['precio'])} con envío gratis. Cómo se instala.",
               f"Filtro externo para nevera {m}", f"Para neveras {m}",
               f"El filtro externo {esc(externo['ref'])} se conecta a la manguera del agua y sirve en neveras con dispensador o máquina de hielo, incluidas las {esc(m)}.",
               respuesta(f"El filtro externo {esc(externo['ref'])} va en la manguera del agua por detrás de la nevera {esc(m)}. Cuesta {cop(externo['precio'])} con envío gratis.") + h.caja(externo, base, ctx["foto"])
               + "<h2 style=\"font-size:22px;margin:24px 0 12px\">Cómo se instala</h2><ol>" + "".join(f"<li>{esc(x)}</li>" for x in datos(externo)["pasos"]) + "</ol>"
               + f'<p class="m-mut" style="margin-top:18px">{esc(m)} es una marca registrada de su dueño; se nombra solo para indicar para qué neveras sirven. Si tienes dudas, mándanos una foto de la manguera o del modelo.</p>',
               faq, miga_nombre=f"Filtro externo {m}", ld_extra=h.producto_ld(externo, X["externas"][m], f"Filtro externo para nevera {m}", marca))
    # ---------- hub de marcas ----------
    fam = "".join(f'<div class="m-bloque"><h3><a href="{lista[0][0]}">{esc(m)}</a></h3><p>{esc(", ".join(FAMILIA[m]["alias"][:3]))}</p><p>' + " · ".join(f'<a href="{r}">{esc(t)}</a>' for r, t in lista[1:]) + "</p></div>" for m, lista in X["familia"].items())
    kk = "".join(f'<a href="{r}">{esc(t)}</a>' for r, t in X["kenmore"])
    ee = "".join(f'<a href="{r}">{esc(m)}</a>' for m, r in X["externas"].items())
    pagina(X["hub"], "Filtros de agua para nevera por marca: Whirlpool, Maytag, KitchenAid, Jenn-Air, Amana, Kenmore y más",
           "Encuentra el filtro de agua de tu nevera por marca: Whirlpool, Maytag (MyTag), KitchenAid, Jenn-Air, Amana, Kenmore, Samsung, LG, GE, Mabe, Haceb y más.",
           "Filtros de agua para nevera por marca", "Todas las marcas",
           "Escoge la marca de tu nevera y mira qué filtro le sirve, cuánto cuesta y cómo cambiarlo.",
           f'<h2 style="font-size:22px;margin:10px 0 14px">Marcas de la familia Whirlpool</h2><div class="m-cols"><div class="m-bloque"><h3><a href="{base}">Whirlpool</a></h3><p>EveryDrop 1 al 5 y filtro externo.</p></div>{fam}</div>'
           f'<h2 style="font-size:22px;margin:26px 0 12px">Kenmore</h2><div class="m-chips">{kk}</div>'
           f'<h2 style="font-size:22px;margin:26px 0 12px">Filtro externo para neveras de otras marcas</h2><div class="m-chips">{ee}</div>',
           [("¿Qué marcas de nevera usan los filtros Whirlpool?", "Whirlpool, Maytag, KitchenAid, Jenn-Air y Amana usan los EveryDrop; Kenmore tiene referencias equivalentes; el filtro externo sirve en neveras de varias marcas."),
            ("¿Cómo busco por marca?", "Entra a la página de tu marca y compara la referencia del filtro viejo con la tabla.")], miga_nombre="Filtros por marca")
    # ---------- preguntas frecuentes (para Google y asistentes de IA) ----------
    grupos = preguntas_ia(ps, slug) + list(ctx.get("faq_extra", []))
    todas = [qa for _, l in grupos for qa in l]
    cuerpo = "".join(f'<h2 id="{slug(g)}" style="font-size:22px;margin:26px 0 12px">{esc(g)}</h2>' + "".join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in l) for g, l in grupos)
    pagina(X["faq"], f"Preguntas frecuentes sobre filtros de nevera Whirlpool y más marcas ({len(todas)} respuestas)",
           f"{len(todas)} respuestas sobre filtros de agua para nevera: equivalencias con KitchenAid, Maytag, Jenn-Air, Amana y Kenmore, precios, envíos, pagos y cómo cambiarlos.",
           "Preguntas frecuentes sobre filtros de nevera", "Respuestas rápidas",
           "Respuestas directas sobre qué filtro usar, para qué marcas sirve, cuánto cuesta, cómo pagar y cómo cambiarlo.", cuerpo, todas, miga_nombre="Preguntas frecuentes")
    # ---------- blog ----------
    arts = articulos(ps, base, inst)
    for sl, titulo, desc, resumen, cuerpo_a, preguntas in arts:
        art = {"@type": "Article", "headline": titulo, "description": desc, "inLanguage": "es-CO", "datePublished": "2026-10-18", "dateModified": "2026-10-18",
               "author": {"@type": "Organization", "name": "__NOMBRE__"}, "publisher": {"@id": f"__BASE__{base}#tienda"}, "mainEntityOfPage": f"__BASE__{base}blog/{sl}/"}
        otros = [x for x in arts if x[0] != sl][:4]
        pagina(f"{base}blog/{sl}/", f"{titulo} | Blog de filtros Whirlpool", desc, titulo, "Blog",
               "", respuesta(esc(resumen)) + cuerpo_a + '<h2 style="font-size:20px;margin:26px 0 10px">Sigue leyendo</h2><div class="m-chips">'
               + "".join(f'<a href="{base}blog/{o[0]}/">{esc(o[1])}</a>' for o in otros) + "</div>", preguntas, miga_nombre=titulo, ld_extra=art)
    pagina(X["blog"], "Blog: guías sobre filtros de agua para nevera Whirlpool, KitchenAid y Maytag",
           "Guías prácticas sobre filtros de agua para nevera: cómo escoger el EveryDrop, cada cuánto cambiarlo, luces del filtro y problemas comunes.",
           "Blog de filtros de agua para nevera", "Guías",
           "Artículos prácticos de un técnico de neveras para escoger, cambiar y cuidar el filtro de agua.",
           '<div class="m-cols">' + "".join(f'<a class="m-bloque m-guia" href="{base}blog/{sl}/"><h3>{esc(t)}</h3><p>{esc(d)}</p></a>' for sl, t, d, _, _, _ in arts) + "</div>",
           [("¿Con qué frecuencia publican?", "Agregamos artículos nuevos sobre filtros y neveras con regularidad.")], miga_nombre="Blog")
    rutas_nuevas = [r for l in X["familia"].values() for r, _ in l] + [r for r, _ in X["kenmore"]] + list(X["externas"].values()) + [X["hub"], X["faq"], X["blog"]] + [f"{base}blog/{a[0]}/" for a in arts]
    return rutas_nuevas
