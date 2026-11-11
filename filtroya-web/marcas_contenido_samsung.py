"""Contenido extra de SEO para la tienda propia de Samsung: preguntas frecuentes (para Google y asistentes de IA) y blog.
Misma idea que marcas_contenido.py (Whirlpool), con los 4 filtros Samsung."""
import html
import re


RESPUESTA = '<div class="m-respuesta"><b>Respuesta rápida</b><p>__T__</p></div>'


def esc(s):
    return html.escape(str(s), quote=True)


def cop(v):
    return "$ " + f"{int(v):,}".replace(",", ".")


def rutas(base, slug, hub=None):
    return {"familia": {}, "kenmore": [], "externas": {}, "hub": None, "faq": f"{base}preguntas-frecuentes/", "blog": f"{base}blog/"}


def _p(ps, ref_inicio):
    return next((p for p in ps if p["ref"].startswith(ref_inicio) or ref_inicio in " ".join(p["refs"])), None)


def articulos(ps, base="/", inst="/cambio-e-instalacion/"):
    """Blog: [(slug, titulo, descripcion, resumen, cuerpo_html, preguntas)]."""
    cin, qin, cu1, ex = (_p(ps, k) for k in ("DA29-00020B", "DA97-17376B", "DA29-00003G", "DA29-10105J"))
    L = lambda p: f'<a href="{base}{p["slug"]}/">{esc(p["nombre_largo"])}</a>'
    precios = sorted({p["precio"] for p in ps})
    rango = f"{cop(precios[0])} a {cop(precios[-1])}"
    mod = lambda p: ", ".join(p["modelos"][:5])
    A = []

    def a(slug_, titulo, desc, resumen, cuerpo, preguntas):
        A.append((slug_, titulo, desc, resumen, cuerpo.replace('/cambio-e-instalacion/', inst), preguntas))

    a("como-saber-que-filtro-necesita-tu-nevera-samsung", "Cómo saber qué filtro necesita tu nevera Samsung",
      "Tres pasos para saber si tu nevera Samsung usa el filtro HAF-CIN, HAF-QIN, Aqua-Pure Plus (HAFCU1) o el externo.",
      "Mira la referencia impresa en el filtro viejo (HAF-CIN, HAF-QIN, HAFCU1…) o el modelo de la nevera en la etiqueta interna.",
      "<p>Las neveras Samsung usan cuatro filtros distintos según el modelo. No se pueden cambiar entre sí. Estos son los tres caminos para encontrar el tuyo.</p>"
      "<h2>1. Mira el filtro viejo</h2><p>Sácalo y busca la referencia impresa: <span class=\"ref\">HAF-CIN</span> (DA29-00020B), <span class=\"ref\">HAF-QIN</span> (DA97-17376B) o <span class=\"ref\">HAFCU1</span> (DA29-00003G). Todos tienen equivalencias, por ejemplo DA29-00020A, DA97-08006C o DA29-00003B.</p>"
      "<h2>2. Mira el modelo de la nevera</h2><p>La etiqueta está dentro del refrigerador, en una pared lateral o detrás del cajón de las verduras. En Samsung suele empezar por <b>RF</b> (French door y de varias puertas) o <b>RS</b> (side by side).</p>"
      f"<ul class=\"m-ok\"><li>{L(cin)}: nevecones como {esc(mod(cin))}.</li><li>{L(qin)}: modelos como {esc(mod(qin))}.</li>{(f'<li>{L(cu1)}: side by side como {esc(mod(cu1))}.</li>' if cu1 else '')}</ul>"
      "<h2>3. Si tu nevera usa filtro externo</h2><p>Algunas se conectan a la manguera del agua y llevan el filtro por fuera. Ese es el " + L(ex) + ".</p>"
      "<p>Si dudas, mándanos la foto del filtro viejo o de la etiqueta por WhatsApp y te confirmamos antes de comprar.</p>",
      [("¿Un HAF-QIN sirve en una nevera que usa HAF-CIN?", "No. Cada referencia tiene forma y conexión propias; hay que usar la misma del filtro viejo."),
       ("¿Dónde está la referencia del filtro?", "Impresa en el cuerpo del filtro, junto con el código de Samsung que empieza por DA.")])
    a("diferencias-entre-haf-cin-haf-qin-aqua-pure-plus-y-filtro-externo-samsung", "Diferencias entre HAF-CIN, HAF-QIN, Aqua-Pure Plus y el filtro externo Samsung",
      "Qué cambia entre los cuatro filtros de agua Samsung: para qué nevecones sirve cada uno, equivalencias y precio.",
      "Los cuatro filtran el agua del dispensador y del hielo; lo que cambia es la forma, la conexión y los modelos de nevera que los usan.",
      f"<p>Son cuatro filtros distintos y cada uno va en neveras diferentes:</p><ul class=\"m-ok\"><li><b>{L(cin)}</b> ({cop(cin['precio'])}). Equivale a {esc(', '.join(cin['refs'][:4]))}.</li>"
      f"<li><b>{L(qin)}</b> ({cop(qin['precio'])}). Equivale a {esc(', '.join(qin['refs'][:3]))}.</li>"
      + (f"<li><b>{L(cu1)}</b> ({cop(cu1['precio'])}). Equivale a {esc(', '.join(cu1['refs'][:4]))}.</li>" if cu1 else '') +
      f"<li><b>{L(ex)}</b> ({cop(ex['precio'])}). Equivale a {esc(', '.join(ex['refs'][:3]))}.</li></ul>"
      "<p>El filtro correcto es el que usa tu modelo: comparar solo por precio lleva a comprar uno que no encaja. Todos se cambian cada 6 meses.</p>",
      [("¿El HAF-CIN y el HAF-QIN son lo mismo?", "No. Son referencias distintas con diferente conexión; no son intercambiables."),
       ("¿Cuál es el más económico?", f"El filtro externo ({cop(ex['precio'])}); los internos cuestan entre {cop(cin['precio'])} y {cop((cu1 or qin)['precio'])}.")])
    a("como-reiniciar-la-luz-del-filtro-de-la-nevera-samsung", "Cómo reiniciar la luz del filtro de la nevera Samsung",
      "Cómo apagar o reiniciar el indicador del filtro de agua en neveras Samsung después de cambiarlo.",
      "Después de cambiar el filtro, mantén presionado el botón del filtro (Filter Reset o Water Filter) unos 3 segundos hasta que el indicador se reinicie.",
      "<p>La luz del filtro (o el mensaje «Replace Filter») no se apaga sola: hay que reiniciarla después de cambiar el filtro.</p>"
      "<ol><li>Cambia el filtro y purga el aire sacando unos 6 litros por el dispensador.</li><li>Ubica el botón del filtro en el panel (suele decir <b>Filter Reset</b> o <b>Water Filter</b>).</li><li>Mantenlo presionado unos <b>3 segundos</b>.</li><li>Mira que el indicador cambie de color o se apague.</li></ol>"
      "<p>En algunos modelos con pantalla el reinicio está en el menú de ajustes. Si no se apaga, revisa el manual de tu modelo. Para el cambio completo mira la <a href=\"/cambio-e-instalacion/\">guía de instalación</a>.</p>",
      [("¿Por qué la luz no se apaga?", "Casi siempre porque no se mantuvo presionado el botón el tiempo suficiente o el modelo lo reinicia por el menú de la pantalla."),
       ("¿La luz funciona por tiempo o por litros?", "Por tiempo: se enciende cuando pasan unos 6 meses desde el último reinicio.")])
    a("nevera-samsung-no-saca-agua-del-dispensador-causas-y-soluciones", "Nevera Samsung que no saca agua del dispensador: causas y soluciones",
      "Qué revisar cuando el dispensador de tu nevera Samsung no saca agua o la saca muy despacio, de lo más fácil a lo que necesita técnico.",
      "Casi siempre es el filtro (tapado o mal puesto), la llave de paso cerrada o aire en la línea.",
      "<ol><li><b>El filtro.</b> Con más de 6 meses se tapa con sedimentos. Si es nuevo, mira que esté girado hasta el fondo y sin la tapa protectora.</li><li><b>La referencia.</b> Otra referencia no encaja y corta el paso del agua.</li>"
      "<li><b>El aire.</b> Después del cambio saca unos 6 litros por tandas.</li><li><b>La llave de paso</b> detrás de la nevera: abierta y la manguera sin dobleces.</li><li><b>Congelamiento</b> de la línea de agua: un técnico revisa la temperatura.</li></ol>"
        f"<p>Para reemplazar un filtro viejo mira el {L(cin)}{(', el ' + L(qin) + ' o el ' + L(cu1)) if cu1 else ' o el ' + L(qin)}, según el que use tu nevera.</p>",
      [("¿Por qué no sale agua después de cambiar el filtro?", "Casi siempre por mala instalación, aire en la línea o una referencia equivocada."),
       ("¿Cuánta agua debo sacar para purgar?", "Unos 6 litros, por tandas, hasta que salga pareja.")])
    a("nevera-samsung-hielo-pequeno-turbio-o-sin-hielo-que-revisar", "Nevera Samsung con hielo pequeño, turbio o sin hielo: qué revisar",
      "Por qué la máquina de hielo de tu nevera Samsung saca poco hielo, hielo chico o turbio, y cómo corregirlo.",
      "El hielo chico o poco casi siempre es falta de agua por un filtro tapado; el turbio, un filtro vencido o aire.",
      "<ul class=\"m-ok\"><li><b>Hielo pequeño o poco:</b> llega poca agua. Cambia el filtro si pasaron 6 meses.</li><li><b>Hielo turbio o con sabor:</b> filtro vencido o recién puesto sin purgar.</li><li><b>Hielo pegado:</b> revisa la temperatura del congelador y que la puerta cierre bien.</li><li><b>No hace hielo:</b> mira que la máquina esté encendida y la llave de paso abierta.</li></ul>"
      "<p>Tras cambiar el filtro, descarta las primeras tandas de hielo.</p>",
      [("¿Por qué el hielo sale más pequeño?", "Por falta de agua: un filtro tapado deja pasar menos caudal."),
       ("¿Cuándo tiro el primer hielo con filtro nuevo?", "Las primeras tandas, hasta que salga limpio.")])
    a("como-comprar-un-filtro-de-nevera-samsung-por-internet-sin-equivocarte", "Cómo comprar un filtro de nevera Samsung por internet sin equivocarte",
      "Cinco pasos para comprar el filtro correcto de tu nevera Samsung por internet: referencia, modelo, empaque, pago y envío.",
      "Confirma la referencia del filtro viejo o el modelo de la nevera, compra la misma referencia y revisa pago seguro, envío y retracto.",
      "<ol><li><b>Anota la referencia del filtro viejo</b> (HAF-CIN, HAF-QIN, HAFCU1…) o el modelo de la nevera.</li><li><b>Compra la misma referencia.</b></li><li><b>Verifica que sea nuevo</b> y venga en su empaque sellado.</li><li><b>Paga en un sitio seguro</b> (tarjeta, PSE o Nequi) o contra entrega.</li><li><b>Guarda la guía de envío y el recibo;</b> tienes 5 días hábiles de retracto, sin instalar.</li></ol>"
      f"<p>Precios de los filtros: de {rango}. {L(cin)}, {L(qin)}{(', ' + L(cu1)) if cu1 else ''} y {L(ex)}. Si dudas, usa el asistente de la página: escribes el modelo y te dice cuál es.</p>",
      [("¿Cómo sé si es el correcto?", "Compara la referencia con la del filtro viejo o con el modelo de la nevera."),
       ("¿Puedo devolverlo si me equivoco?", "Sí, dentro de 5 días hábiles, sin instalar y en su empaque.")])
    a("como-leer-el-modelo-de-tu-nevera-samsung", "Cómo leer el modelo de tu nevera Samsung",
      "Dónde está la etiqueta del modelo y qué significan sus letras en neveras Samsung (RF, RS).",
      "La etiqueta está dentro del refrigerador, en una pared lateral. En Samsung suele empezar por RF o RS.",
      "<p>Abre el refrigerador y busca una etiqueta con «Model». Las primeras letras indican el tipo: <b>RF</b> suele ser French door o de varias puertas y <b>RS</b> side by side. Con ese modelo y la referencia del filtro viejo se confirma cuál filtro es.</p>"
      f"<p>Algunos ejemplos de nuestra lista: {esc(mod(cin))} usan el {L(cin)}; {esc(mod(qin))} el {L(qin)}{(f'; y {esc(mod(cu1))} el {L(cu1)}' if cu1 else '')}.</p>",
      [("¿Qué hago si la etiqueta no se lee?", "Mándanos la foto del filtro viejo y te confirmamos.")])
    a("como-instalar-el-filtro-externo-samsung-da29-10105j", "Cómo instalar el filtro externo Samsung DA29-10105J",
      "Paso a paso para instalar el filtro externo Samsung en la manguera de agua de tu nevera, sin herramientas.",
      "Cierra la llave de agua, conecta el filtro con la flecha en el sentido del agua y purga antes de usarlo.",
      "<ol><li>Cierra la llave de paso del agua y desconecta la nevera.</li><li>Ubica la manguera de agua entre la llave y la nevera.</li><li>Conecta el filtro respetando la <b>flecha</b>: apunta en el sentido en que viaja el agua.</li><li>Ajusta los racores sin forzarlos.</li><li>Abre la llave, revisa que no gotee y conecta la nevera.</li><li>Saca unos 6 litros para purgar el aire.</li></ol>"
      f"<p>Producto y precio: {L(ex)}.</p>",
      [("¿Se usa junto con el filtro interno?", "Sí, el externo filtra antes y no reemplaza al interno.")])
    a("cada-cuanto-cambiar-el-filtro-de-agua-de-una-nevera-samsung", "Cada cuánto cambiar el filtro de agua de una nevera Samsung",
      "Cada cuánto se cambia el filtro de la nevera Samsung, señales de que ya toca y qué pasa si lo dejas más tiempo.",
      "Cada 6 meses, o antes si el agua cambia de sabor, sale menos o se prende la luz del filtro.",
      "<ul class=\"m-ok\"><li>Cada <b>6 meses</b> de uso normal.</li><li>Antes si el agua o el hielo saben o huelen raro.</li><li>Si el dispensador saca menos agua.</li><li>Si se prende la luz del filtro.</li></ul>"
      "<p>Si lo dejas más tiempo, el carbón activado se satura y el filtro se tapa; el agua puede volver a saber a cloro. Después del cambio, reinicia la luz del filtro (mira <a href=\"" + base + "blog/como-reiniciar-la-luz-del-filtro-de-la-nevera-samsung/\">cómo reiniciarla</a>).</p>",
      [("¿Se puede alargar el cambio a un año?", "No se recomienda: el filtro pierde efecto y puede tapar el flujo."),
       ("¿Si casi no uso la nevera, igual lo cambio?", "Sí, cada 6 meses: el filtro también envejece con el tiempo.")])
    return A


def preguntas_ia(ps, slug):
    cin, qin, cu1, ex = (_p(ps, k) for k in ("DA29-00020B", "DA97-17376B", "DA29-00003G", "DA29-10105J"))
    precios = sorted({p["precio"] for p in ps})
    rango = f"{cop(precios[0])} a {cop(precios[-1])}"
    G = [("Qué filtro usa cada modelo de nevera Samsung", [
        (f"¿Qué filtro de agua usa la nevera Samsung {m}?", f"La {m} usa el {p['nombre_largo']} (referencia {p['ref']}), por {cop(p['precio'])}, con envío a toda Colombia.")
        for p in ps for m in p["modelos"]])]
    G += [("Qué filtro le sirve a mi nevera Samsung", [
        ("¿Qué filtro de agua le sirve a una nevera Samsung?", f"Depende del modelo: HAF-CIN ({cin['ref']}), HAF-QIN ({qin['ref']}){(', Aqua-Pure Plus HAFCU1 (' + cu1['ref'] + ')') if cu1 else ''} o el externo ({ex['ref']}). Mira la referencia del filtro viejo o el modelo de la nevera."),
        ("¿Qué equivale al HAF-CIN?", f"{', '.join(cin['refs'])}."),
        ("¿Qué equivale al HAF-QIN?", f"{', '.join(qin['refs'])}."),
    ] + ([("¿Qué equivale al HAFCU1 y al HAFIN2?", f"{', '.join(cu1['refs'])}.")] if cu1 else []) + [
        ("¿Qué es el filtro externo Samsung?", f"El {ex['nombre_largo']}: se conecta a la manguera del agua y equivale a {', '.join(ex['refs'])}."),
        ("¿Cuánto cuesta un filtro para nevera Samsung?", f"Entre {rango}, según la referencia."),
    ]), ("Escoger y comprar", [
        ("¿Cómo sé qué filtro necesita mi nevera Samsung?", "Mira la referencia impresa en el filtro viejo o el modelo en la etiqueta interna. Si dudas, mándanos la foto y te confirmamos antes de comprar."),
        ("¿Son distribuidores de Samsung?", "Sí, somos distribuidores de Samsung a nivel nacional."),
        ("¿Hacen envíos a toda Colombia?", "Sí, enviamos a toda Colombia por transportadora, con número de guía."),
        ("¿Se puede pagar contra entrega?", "Sí. Puedes pagar en efectivo a la transportadora al recibir (recargo de $ 5.000 por producto) o en línea con tarjeta, PSE, Nequi o botón Bancolombia, en una página segura de Wompi."),
        ("¿Es seguro pagar en la tienda?", "Sí. El pago se hace en la página segura de Wompi; la tienda nunca ve los datos de tu tarjeta."),
        ("¿Qué pasa si me equivoco de filtro?", "Tienes 5 días hábiles para retractarte, con el filtro sin instalar y en su empaque."),
    ]), ("Instalación y uso", [
        ("¿Cada cuánto se cambia el filtro de la nevera Samsung?", "Cada 6 meses, o antes si el agua cambia de sabor, el dispensador saca menos agua o se prende la luz del filtro."),
        ("¿Necesito un técnico para cambiarlo?", "No. Los internos se cambian en un par de minutos y el externo en 10 a 15, sin herramientas."),
        ("¿Cómo apago la luz del filtro Samsung?", "Mantén presionado el botón del filtro (Filter Reset o Water Filter) unos 3 segundos después del cambio; en algunos modelos es desde el menú de la pantalla."),
        ("¿Por qué sale aire o agua turbia con el filtro nuevo?", "Es normal: el filtro nuevo suelta aire y polvo de carbón. Saca unos 6 litros por el dispensador."),
        ("¿Se puede lavar el filtro y volverlo a usar?", "No. El carbón activado se satura y lavarlo no lo recupera."),
    ]), ("Problemas frecuentes", [
        ("¿Por qué no sale agua después de cambiar el filtro Samsung?", "Casi siempre está mal puesto, no se purgó el aire o es otra referencia."),
        ("¿Por qué gotea el filtro?", "Por estar mal encajado, ser de otra referencia o tener el empaque pellizcado."),
        ("¿Por qué el agua sabe a cloro o a plástico?", "Por un filtro vencido o recién puesto sin purgar."),
        ("¿Por qué el hielo sale pequeño o turbio?", "Suele ser un filtro tapado que deja pasar poca agua; cámbialo."),
    ]), ("Más preguntas de compradores", [
        ("¿Cuál es el mejor filtro para una nevera Samsung?", "No hay uno mejor en general: el correcto es el que usa tu modelo. Escribe el modelo en el asistente de la página."),
        ("¿Dónde compro un filtro de nevera Samsung en Colombia?", "En esta tienda, con envío a toda Colombia y pago en línea o contra entrega."),
        ("¿Qué hago si no encuentro el modelo de mi nevera?", "Está en una etiqueta dentro del refrigerador, en una pared lateral. Si no se lee, manda la foto del filtro viejo."),
    ])]
    return G


def generar(pagina, ctx, h, R):
    """Páginas de preguntas frecuentes y blog de la tienda Samsung (usa la función `pagina` de marcas_seo)."""
    marca, ps, base, M = ctx["marca"], ctx["ps"], ctx["base"], ctx["M"]
    slug = ctx["slug"]
    X = R["extra"]
    inst = f"{base}cambio-e-instalacion/"
    grupos = preguntas_ia(ps, slug)
    if M.get("bogota"):
        grupos = [("Entregas en Bogotá", [("¿Entregan filtros Samsung en todo Bogotá?", "Sí, en las 19 localidades urbanas y en sus barrios, en 1 a 2 días hábiles."),
                                            ("¿Dónde están ubicados?", "Tenemos nuestra bodega en el barrio Cedritos, en Bogotá."),
                                            ("¿Hay pack de 2 filtros?", "Sí: el pack de 2 trae dos filtros de la misma referencia con ahorro; uno para ahora y otro para dentro de 6 meses."),
                                            ("¿Cómo pago?", "Solo en línea, en la pasarela segura de Wompi: tarjeta, PSE, Nequi o Bancolombia.")])] + grupos
    todas = [qa for _, l in grupos for qa in l]
    cuerpo = "".join(f'<h2 id="{slug(g)}" style="font-size:22px;margin:26px 0 12px">{esc(g)}</h2>' + "".join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in l) for g, l in grupos)
    pagina(X["faq"], f"Preguntas frecuentes sobre filtros de nevera Samsung ({len(todas)} respuestas)",
           f"{len(todas)} respuestas sobre filtros de agua para nevera Samsung: HAF-CIN, HAF-QIN, externo, equivalencias, precios y cómo cambiarlos.",
           "Preguntas frecuentes sobre filtros de nevera Samsung", "Respuestas rápidas",
           "Respuestas directas sobre qué filtro usa cada nevera Samsung, cuánto cuesta, cómo pagar y cómo cambiarlo.", cuerpo, todas, miga_nombre="Preguntas frecuentes")
    def respuesta(txt):
        return RESPUESTA.replace("__T__", txt)
    arts = articulos(ps, base, inst)
    if M.get("bogota"):
        import bogota_seo
        arts = bogota_seo.articulos(ps, base, inst) + arts
    for sl, titulo, desc, resumen, cuerpo_a, preguntas in arts:
        art = {"@type": "Article", "headline": titulo, "description": desc, "inLanguage": "es-CO", "datePublished": "2026-11-11", "dateModified": "2026-11-11",
               "author": {"@type": "Organization", "name": "__NOMBRE__"}, "publisher": {"@id": f"__BASE__{base}#tienda"}, "mainEntityOfPage": f"__BASE__{base}blog/{sl}/"}
        otros = [x for x in arts if x[0] != sl][:4]
        pagina(f"{base}blog/{sl}/", f"Blog: {titulo}", desc, titulo, "Blog", "",
               respuesta(esc(resumen)) + cuerpo_a
               + '<h2 style="font-size:20px;margin:26px 0 10px">Sigue leyendo</h2><div class="m-chips">' + "".join(f'<a href="{base}blog/{o[0]}/">{esc(o[1])}</a>' for o in otros) + "</div>",
               preguntas, miga_nombre=titulo, ld_extra=art)
    pagina(X["blog"], "Blog: guías sobre filtros de agua para nevera Samsung",
           "Guías prácticas sobre filtros de agua para nevera Samsung: cómo escoger el filtro, cada cuánto cambiarlo, reiniciar la luz y problemas comunes.",
           "Blog de filtros de agua para nevera Samsung", "Guías",
           "Artículos prácticos de un técnico de neveras para escoger, cambiar y cuidar el filtro de agua de tu Samsung.",
           '<div class="m-cols">' + "".join(f'<a class="m-bloque m-guia" href="{base}blog/{sl}/"><h3>{esc(t)}</h3><p>{esc(d)}</p></a>' for sl, t, d, _, _, _ in arts) + "</div>",
           [("¿Con qué frecuencia publican?", "Agregamos artículos nuevos sobre filtros y neveras con regularidad.")], miga_nombre="Blog")
