"""Contenido extra de SEO para la tienda nacional de LG: preguntas frecuentes (para Google y asistentes de IA) y blog. Todo sale del catálogo (códigos, equivalencias, modelos y precios)."""
import html

RESPUESTA = '<div class="m-respuesta"><b>Respuesta rápida</b><p>__T__</p></div>'
esc = lambda s: html.escape(str(s), quote=True)
cop = lambda v: "$ " + f"{int(v):,}".replace(",", ".")


def rutas(base, slug, hub=None):
    return {"familia": {}, "kenmore": [], "externas": {}, "hub": None, "faq": f"{base}preguntas-frecuentes/", "blog": f"{base}blog/"}


def _p(ps, ref):
    return next((p for p in ps if p["ref"].startswith(ref) or ref in " ".join(p["refs"]) or ref in p["nombre_largo"]), None)


def articulos(ps, base="/", inst="/cambio-e-instalacion/"):
    L = lambda p: f'<a href="{base}{p["slug"]}/">{esc(p["nombre_largo"])}</a>'
    internos = [p for p in ps if "-ex-" not in p["id"]]
    ext = next((p for p in ps if "-ex-" in p["id"]), None)
    precios = sorted({p["precio"] for p in ps})
    rango = f"{cop(precios[0])} a {cop(precios[-1])}"
    A = []

    def a(slug_, titulo, desc, resumen, cuerpo, preguntas):
        A.append((slug_, titulo, desc, resumen, cuerpo.replace("/cambio-e-instalacion/", inst), preguntas))

    lista_p = "<ul class=\"m-ok\">" + "".join(f"<li>{L(p)} — equivale a {esc(', '.join(p['refs'][:4]))}" + (f"; nevecones como {esc(', '.join(p['modelos'][:3]))}" if p["modelos"] else "") + f". <b>{cop(p['precio'])}</b></li>" for p in ps) + "</ul>"
    a("como-saber-que-filtro-necesita-tu-nevera-lg", "Cómo saber qué filtro necesita tu nevera LG", "Tres pasos para saber qué filtro de agua usa tu nevera o nevecón LG: por el filtro viejo, por el modelo o por la conexión externa.",
      "Mira el código impreso en el filtro viejo, el modelo de la nevera (etiqueta interna) o si el filtro va en la manguera del agua.",
      "<p>Las neveras LG usan filtros distintos según el modelo y no se pueden cambiar entre sí. Estos son los tres caminos para encontrar el tuyo.</p>"
      "<h2>1. Mira el filtro viejo</h2><p>Sácalo y busca el código impreso en el cuerpo del filtro. Estos son los que vendemos:</p>" + lista_p
      + "<h2>2. Mira el modelo de la nevera</h2><p>La etiqueta está dentro del refrigerador, en una pared lateral o detrás del cajón de las verduras. En LG suele empezar por <b>LF</b>, <b>LM</b>, <b>LR</b>, <b>LS</b> o <b>GR</b>. Escríbelo en el <a href=\"" + base + "cual-es-mi-filtro/\">buscador por modelo</a>.</p>"
      + "<h2>3. Si el filtro va por fuera</h2><p>" + (f"Algunos nevecones llevan el filtro en la manguera del agua, fuera del refrigerador. Ese es el {L(ext)}." if ext else "Algunos nevecones llevan el filtro por fuera.") + "</p>",
      [("¿Un LT700P sirve en una nevera que usa LT1000P?", "No. Cada referencia tiene su forma y conexión; hay que usar la misma del filtro viejo."), ("¿Dónde está el código del filtro?", "Impreso en el cuerpo del filtro, junto al código de LG.")])
    a("diferencias-entre-los-filtros-de-agua-lg", "Diferencias entre los filtros de agua LG: " + ", ".join(p["ref"] for p in internos[:5]), "Qué cambia entre los filtros de agua LG: para qué nevecones sirve cada uno, equivalencias y precio.",
      "Todos filtran el agua del dispensador y del hielo; cambia la forma, la conexión y los modelos de nevecón que los usan.", "<p>Estos son los filtros LG que tenemos y lo que cambia entre ellos:</p>" + lista_p
      + "<p>El filtro correcto es el que usa tu modelo: comparar solo por precio lleva a comprar uno que no encaja. Todos se cambian cada 6 meses.</p>",
      [("¿Cuál es el más económico?", f"El filtro externo ({cop(ext['precio'])}) si tu nevecón lo usa; entre los internos, el {internos[0]['ref']} ({cop(internos[0]['precio'])})." if ext else f"Desde {cop(precios[0])}."), ("¿Son intercambiables?", "No, usa la referencia exacta de tu nevecón.")])
    a("cuanto-cuesta-el-filtro-de-agua-de-una-nevera-lg", "Cuánto cuesta el filtro de agua de una nevera LG en Colombia", f"Precios de los filtros de agua para nevecón LG en Colombia: de {rango}, con envío gratis y pago en línea.",
      f"Los filtros LG cuestan entre {rango} según la referencia, con envío gratis a toda Colombia.", "<p>Estos son los precios de los filtros de agua LG que vendemos, con envío gratis y pago seguro en línea:</p>" + lista_p
      + "<p>Pagas con tarjeta, PSE, Nequi o Bancolombia en la pasarela de Wompi y recibes la confirmación por correo.</p>", [("¿El envío tiene costo?", "No, el envío es gratis a toda Colombia."), ("¿Cómo pago?", "En línea, en la pasarela segura de Wompi.")])
    a("cada-cuanto-cambiar-el-filtro-de-agua-de-la-nevera-lg", "Cada cuánto cambiar el filtro de agua de la nevera LG", "El filtro de agua del nevecón LG se cambia cada 6 meses: señales de que ya toca y qué pasa si no se cambia.",
      "Cámbialo cada 6 meses, o antes si el agua cambia de sabor, el hielo sale turbio o el dispensador entrega menos agua.",
      "<p>El filtro retiene cloro y sedimentos; con el uso se satura. La recomendación es cambiarlo cada <b>6 meses</b>.</p><ul class=\"m-ok\"><li>Pasaron 6 meses desde el último cambio.</li><li>El agua o el hielo saben u huelen distinto.</li><li>El dispensador saca menos agua.</li>"
      "<li>Se enciende el aviso de cambio de filtro en el panel.</li></ul><p>Mira <a href=\"/cambio-e-instalacion/\">cómo cambiarlo paso a paso</a>.</p>",
      [("¿Qué pasa si no lo cambio?", "El agua puede volver a saber a cloro, el hielo salir turbio y el dispensador entregar menos agua."), ("¿Cuánto tarda el cambio?", "Unos minutos y sin herramientas especiales.")])
    a("como-reiniciar-el-aviso-del-filtro-de-la-nevera-lg", "Cómo reiniciar el aviso del filtro de la nevera LG", "Cómo apagar o reiniciar el aviso de cambio de filtro en neveras LG después de instalar el filtro nuevo.",
      "Después de cambiar el filtro, mantén presionado el botón del filtro en el panel unos segundos; el procedimiento exacto depende del modelo.",
      "<p>En los nevecones LG el panel muestra un aviso (por ejemplo «Replace Filter») cuando toca cambiar el filtro.</p><ol><li>Instala el filtro nuevo hasta que quede firme.</li><li>Saca unos 6 litros de agua por el dispensador para purgar el aire.</li>"
      "<li>Mantén presionado el botón del filtro (o «Water Filter») en el panel unos 3 segundos hasta que el aviso se apague.</li></ol><p>Si tu modelo tiene otro procedimiento, revisa el manual del equipo.</p>",
      [("¿Por qué sigue el aviso encendido?", "Suele faltar mantener presionado el botón del filtro unos segundos o reiniciar tras purgar el agua."), ("¿Necesito técnico?", "No, se hace desde el panel.")])
    a("nevera-lg-no-sale-agua-del-dispensador", "Nevera LG que no saca agua del dispensador: causas", "Por qué el dispensador de tu nevera LG no saca agua o sale con poca presión: filtro saturado, aire en la línea o llave cerrada.",
      "Casi siempre es el filtro saturado o mal puesto, aire en la línea o la llave de agua cerrada.", "<ol><li>Si el filtro tiene más de 6 meses, cámbialo.</li><li>Confirma que la referencia sea la de tu nevecón.</li><li>Después del cambio, saca unos 6 litros por tandas.</li>"
      "<li>Revisa que la llave de paso esté abierta y la manguera sin dobleces.</li><li>Si sigue igual, llama a un técnico: puede ser la válvula o un congelamiento de la línea.</li></ol>",
      [("¿Cuánta agua debo sacar tras el cambio?", "Unos 6 litros."), ("¿Puede ser el filtro?", "Sí, un filtro saturado es la causa más común.")])
    a("agua-de-la-nevera-lg-sabe-mal-despues-de-cambiar-el-filtro", "Agua de la nevera LG con mal sabor después de cambiar el filtro", "Si el agua o el hielo de tu nevera LG saben raro después de cambiar el filtro, casi siempre falta purgar el filtro nuevo.",
      "Deja correr unos 6 litros de agua por el dispensador para sacar el aire y el polvo de carbón del filtro nuevo.", "<p>Un filtro nuevo trae aire y partículas finas de carbón. Para eliminarlos:</p><ol><li>Saca unos 6 litros de agua por el dispensador.</li><li>Bota los primeros cubos de hielo.</li><li>Espera unas horas a que el agua se normalice.</li></ol>",
      [("¿Es normal que salga agua turbia al inicio?", "Sí, por el aire del filtro; se aclara al purgar."), ("¿Cuándo debo preocuparme?", "Si pasados unos días el sabor sigue, confirma que el filtro sea la referencia de tu modelo.")])
    a("como-comprar-un-filtro-lg-con-pago-seguro-y-envio-a-toda-colombia", "Cómo comprar un filtro LG con pago seguro y envío a toda Colombia", "Pasos para comprar el filtro de tu nevecón LG en línea: escoger la referencia, pagar con Wompi y recibirlo en tu ciudad.",
      "Escoge la referencia, agrégala al carrito, paga en Wompi y recibe la confirmación por correo; el envío es gratis.", "<ol><li><b>Escoge tu filtro</b> por el código del filtro viejo o el modelo de tu nevecón.</li><li><b>Agrégalo al carrito</b> y escribe tu ciudad y dirección.</li>"
      "<li><b>Paga en línea</b> con tarjeta, PSE, Nequi o Bancolombia en la pasarela segura de Wompi.</li><li><b>Recibe la confirmación</b> por correo y espera tu pedido.</li></ol><p>Somos distribuidores autorizados de filtros para neveras LG. Retracto de 5 días hábiles.</p>",
      [("¿Es seguro pagar en línea?", "Sí, el pago se hace en la pasarela de Wompi (Bancolombia) y no guardamos los datos de tu tarjeta."), ("¿Hay retracto?", "Sí, 5 días hábiles con el filtro sin usar.")])
    a("modelos-de-nevecon-lg-y-su-filtro", "Modelos de nevecón LG y su filtro de agua", "Qué filtro usa cada nevecón LG: modelos como " + ", ".join(m for p in ps for m in p["modelos"][:1]) + " y su referencia.",
      "Cada modelo usa una referencia; busca el tuyo en la lista o escríbelo en el buscador.", "<p>Estos son algunos modelos de nevecón LG y su filtro:</p><ul class=\"m-ok\">" + "".join(f"<li><b>{esc(m)}</b> → {L(p)}</li>" for p in ps for m in p["modelos"]) + "</ul>"
      f"<p>Si tu modelo no está, mira la <a href=\"{base}cual-es-mi-filtro/\">tabla de modelos y referencias</a>.</p>", [("¿Dónde veo el modelo?", "En una etiqueta dentro del refrigerador, en la pared lateral."), ("¿Y si no aparece?", "Compara el código del filtro viejo con la tabla.")])
    return A


def preguntas_ia(ps, slug):
    """Grupos de preguntas y respuestas: [(grupo, [(pregunta, respuesta)])], todo derivado del catálogo."""
    precios = sorted({p["precio"] for p in ps})
    rango = f"{cop(precios[0])} a {cop(precios[-1])}"
    por_ref = []
    for p in ps:
        por_ref += [(f"¿Qué es el filtro LG {p['ref']}?", f"Es el {p['nombre_largo']}, un filtro de agua {'externo, que va en la manguera del agua' if '-ex-' in p['id'] else 'interno para nevecones LG'}. Cuesta {cop(p['precio'])} con envío gratis."),
                    (f"¿Qué equivale al {p['ref']}?", ", ".join(p["refs"]) + ".")]
        if p["modelos"]:
            por_ref.append((f"¿Qué nevecones LG usan el {p['ref']}?", "Por ejemplo " + ", ".join(p["modelos"]) + ". Confirma el código de tu filtro viejo."))
        if p.get("nota"):
            por_ref.append((f"¿Cómo confirmo que el {p['ref']} es el mío?", p["nota"]))
    G = [("Referencias y equivalencias", por_ref),
         ("Comprar y pagar", [("¿Dónde comprar un filtro de nevera LG en Colombia?", "Aquí, con envío gratis a toda Colombia y pago seguro en línea."), ("¿Cuánto cuesta un filtro de agua para nevera LG?", f"Entre {rango}, según la referencia."),
                              ("¿Cómo pago?", "En línea, en la pasarela segura de Wompi: tarjeta, PSE, Nequi o Bancolombia."), ("¿Son distribuidores autorizados?", "Sí, somos distribuidores autorizados de filtros para neveras LG; no somos LG Electronics ni su canal oficial de venta."),
                              ("¿Recibo comprobante?", "Sí, la confirmación del pedido llega a tu correo."), ("¿Los filtros son nuevos?", "Sí, nuevos y en su empaque.")]),
         ("Envío y cobertura", [("¿Envían a toda Colombia?", "Sí, a cientos de ciudades y municipios, con envío gratis."), ("¿Cuánto tarda el envío?", "Entre 1 y 7 días hábiles según la ciudad; lo ves en la página de tu ciudad."), ("¿El envío tiene costo?", "No, es gratis.")]),
         ("Cambio y mantenimiento", [("¿Cada cuánto se cambia el filtro de la nevera LG?", "Cada 6 meses de uso normal."), ("¿Cuánta agua debo sacar tras el cambio?", "Unos 6 litros, para purgar el aire."),
                                     ("¿Puedo cambiar el filtro yo mismo?", "Sí, toma unos minutos y no requiere herramientas."), ("¿Cómo reinicio el aviso del filtro?", "Mantén presionado el botón del filtro en el panel unos segundos, tras instalar el nuevo."),
                                     ("¿Qué pasa si no lo cambio?", "El agua puede saber a cloro y el dispensador entregar menos agua.")]),
         ("Devoluciones", [("¿Puedo devolver el filtro?", "Sí, tienes 5 días hábiles de retracto desde la entrega, con el filtro sin usar."), ("¿Qué hago si pedí el filtro equivocado?", "Escríbenos dentro de los 5 días hábiles y lo cambiamos, sin usar.")])]
    return G


def generar(pagina, ctx, h, R):
    marca, ps, base, M = ctx["marca"], ctx["ps"], ctx["base"], ctx["M"]
    slug = ctx["slug"]
    X = R["extra"]
    inst = f"{base}cambio-e-instalacion/"
    grupos = preguntas_ia(ps, slug)
    todas = [qa for _, l in grupos for qa in l]
    cuerpo = "".join(f'<h2 id="{slug(g)}" style="font-size:22px;margin:26px 0 12px">{esc(g)}</h2>' + "".join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in l) for g, l in grupos)
    pagina(X["faq"], f"Preguntas frecuentes sobre filtros de nevera LG ({len(todas)} respuestas)", f"{len(todas)} respuestas sobre filtros de agua para nevera LG: " + ", ".join(p["ref"] for p in ps[:5]) + ", equivalencias, precios y cómo cambiarlos.",
           "Preguntas frecuentes sobre filtros de nevera LG", "Respuestas rápidas", "Respuestas directas sobre qué filtro usa cada nevera LG, cuánto cuesta, cómo pagar y cómo cambiarlo.", cuerpo, todas, miga_nombre="Preguntas frecuentes")
    arts = articulos(ps, base, inst)
    for sl, titulo, desc, resumen, cuerpo_a, preguntas in arts:
        art = {"@type": "Article", "headline": titulo, "description": desc, "inLanguage": "es-CO", "datePublished": "2026-11-13", "dateModified": "2026-11-13",
               "author": {"@type": "Organization", "name": "__NOMBRE__"}, "publisher": {"@id": f"__BASE__{base}#tienda"}, "mainEntityOfPage": f"__BASE__{base}blog/{sl}/"}
        otros = [x for x in arts if x[0] != sl][:4]
        pagina(f"{base}blog/{sl}/", f"Blog: {titulo}"[:70], desc, titulo, "Blog", "", RESPUESTA.replace("__T__", esc(resumen)) + cuerpo_a + '<h2 style="font-size:20px;margin:26px 0 10px">Sigue leyendo</h2><div class="m-chips">'
               + "".join(f'<a href="{base}blog/{o[0]}/">{esc(o[1])}</a>' for o in otros) + "</div>", preguntas, miga_nombre=titulo, ld_extra=art)
    pagina(X["blog"], "Blog: guías sobre filtros de agua para nevera LG", "Guías prácticas sobre filtros de agua para nevera LG: cómo escoger el filtro, cada cuánto cambiarlo, reiniciar el aviso y problemas comunes.",
           "Blog de filtros de agua para nevera LG", "Guías", "Artículos prácticos para escoger, cambiar y cuidar el filtro de agua de tu nevecón LG.",
           '<div class="m-cols">' + "".join(f'<a class="m-bloque m-guia" href="{base}blog/{sl}/"><h3>{esc(t)}</h3><p>{esc(d)}</p></a>' for sl, t, d, _, _, _ in arts) + "</div>",
           [("¿Con qué frecuencia publican?", "Agregamos artículos nuevos sobre filtros y neveras con regularidad.")], miga_nombre="Blog")
