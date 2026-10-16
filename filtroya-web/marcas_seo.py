"""Subpáginas de búsqueda de cada sitio por marca: una página por cada forma en que la gente busca en Google.

Cada página responde una búsqueda concreta con información propia (no es la misma página con otro título):
  /filtro-nevera-<marca>/            «filtro nevera samsung», «filtro refrigerador samsung»
  /precio-filtro-<marca>/            «precio filtro nevera samsung»
  /luz-filtro-<marca>/               «luz filtro nevera samsung», «cómo reiniciar el filtro»
  /cada-cuanto-cambiar-filtro-<marca>/
  /donde-comprar-filtro-<marca>/     «dónde comprar filtro samsung original»
  /filtro-<marca>-original-o-generico/
  /filtro-externo-nevera-<marca>/    (si la marca tiene filtro externo)
  /filtro-<referencia>/              una por cada referencia equivalente (DA29-00020A, HAF-CIN/EXP…)
  /filtro-nevera-<modelo>/           una por cada modelo de nevera (RF28HMEDBSR…)
  /filtro-nevera-<marca>-<ciudad>/   una por cada ciudad principal
Las usa marcas_exclusivas.generar_marca.
"""
import datetime
import html

esc = lambda s: html.escape(str(s), quote=True)
cop = lambda n: "$ " + f"{n:,}".replace(",", ".")
CIUDADES_SEO = 20
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
hoy = datetime.date.today()  # ciudades con página propia por marca (las más grandes)


def rutas(marca, ps, base, slug, norm, ubic, CIUDADES_CO):
    """Calcula todas las rutas antes de escribir, para que las páginas se enlacen entre sí."""
    s = slug(marca)
    temas = [(f"{base}filtro-nevera-{s}/", f"Filtro para nevera {marca}"),
             (f"{base}precio-filtro-{s}/", f"Precio del filtro {marca}"),
             (f"{base}luz-filtro-{s}/", f"Luz del filtro {marca}: cómo reiniciarla"),
             (f"{base}cada-cuanto-cambiar-filtro-{s}/", "Cada cuánto cambiar el filtro"),
             (f"{base}donde-comprar-filtro-{s}/", f"Dónde comprar filtros {marca} originales"),
             (f"{base}filtro-{s}-original-o-generico/", "Original o genérico: diferencias")]
    temas += [(f"{base}nevera-{s}-no-sale-agua-despues-de-cambiar-el-filtro/", "No sale agua después de cambiar el filtro"),
              (f"{base}filtro-nevera-{s}-gotea/", "El filtro gotea: causas y solución"),
              (f"{base}agua-o-hielo-con-mal-sabor-nevera-{s}/", "Agua o hielo con mal sabor")]
    if any(ubic(p) == "externo" for p in ps):
        temas.append((f"{base}filtro-externo-nevera-{s}/", f"Filtro externo para nevera {marca}"))
    principales = {norm(p["ref"]) for p in ps}
    refs, modelos = {}, {}
    for p in ps:
        for r in p["refs"]:
            if norm(r) not in principales and norm(r) not in refs:
                refs[norm(r)] = (r, p, f"{base}filtro-{slug(r)}/")
        for m in p["modelos"]:
            modelos.setdefault(norm(m), (m, p, f"{base}filtro-nevera-{slug(m)}/"))
    ciudades = {c[0]: (c, f"{base}filtro-nevera-{s}-{slug(c[0])}/") for c in CIUDADES_CO[:CIUDADES_SEO]}
    return {"temas": temas, "refs": refs, "modelos": modelos, "ciudades": ciudades}


def generar(R, escribir, dir_, ctx, h):
    """Escribe las subpáginas. h trae las piezas comunes de marcas_exclusivas. Devuelve las rutas."""
    marca, info, ps, base, M, ubic, php_str = (ctx[k] for k in ("marca", "info", "ps", "base", "M", "ubic", "php_str"))
    hechas = []

    def pagina(ruta, titulo, desc, h1, eyebrow, intro, cuerpo, preguntas=(), miga_nombre=None, ld_extra=None):
        miga_h, miga_ld = h.miga([(f"Filtros {marca} originales", base), (miga_nombre or h1, None)])
        graf = [{"@type": "WebPage", "name": h1, "url": f"__BASE__{ruta}", "inLanguage": "es-CO", "description": desc, "dateModified": hoy.isoformat()}, miga_ld]
        faq_h = ""
        if preguntas:
            faq_h, faq_ld = h.faq(list(preguntas))
            graf.append(faq_ld)
        if ld_extra:
            graf.append(ld_extra)
        texto = (h.inicio(M, php_str, titulo, desc, ruta, {"@context": "https://schema.org", "@graph": graf})
                 + f'<div class="m-wrap">{miga_h}</div>'
                 + h.sec(h.cab(eyebrow, h1, intro, h="h1") + cuerpo + f'<p class="m-mut m-fecha">Actualizado: {MESES[hoy.month - 1]} de {hoy.year}</p>')
                 + h.sec(h.cab("Catálogo " + marca, f"Filtros {marca} originales con envío gratis") + '<div class="m-grid">' + "".join(h.tarjeta(p, base, ctx["foto"], ubic) for p in ps) + "</div>", alt=True)
                 + (h.sec(h.cab("Preguntas", "Preguntas frecuentes") + faq_h) if faq_h else "")
                 + h.sec(relacionadas(R, ruta, marca), alt=not faq_h)
                 + h.sec(h.cta_wa(marca))
                 + "</main>\n<?php pie_marca($M); ?>\n")
        escribir(dir_ / ruta.strip("/") / "index.php", texto)
        hechas.append(ruta)

    tabla = ('<div class="m-tabla-wrap"><table class="m-tabla"><thead><tr><th>Filtro original</th><th>Referencia</th><th>Tipo</th><th>Precio</th><th>Pack de 2</th></tr></thead><tbody>'
             + "".join(f'<tr><td><a href="{base}{p["slug_o"]}/">{esc(p["nombre_largo"])}</a></td><td>{esc(p["ref"])}</td><td>{"Externo" if ubic(p) == "externo" else "Interno"}</td><td><b>{cop(p["precio"])}</b></td><td>{cop(p["pack"])}</td></tr>' for p in ps)
             + "</tbody></table></div>")
    minimo, maximo = min(p["precio"] for p in ps), max(p["precio"] for p in ps)
    rango = cop(minimo) if minimo == maximo else f"{cop(minimo)} y {cop(maximo)}"
    internos = [p for p in ps if ubic(p) != "externo"]
    externos = [p for p in ps if ubic(p) == "externo"]
    T = dict(R["temas"])
    s = M["clase"]
    anio = datetime.date.today().year

    # 1. filtro para nevera <marca>
    pagina(f"{base}filtro-nevera-{s}/", f"Filtro para nevera {marca} original | Precios y envío gratis",
           f"Filtro de agua para nevera {marca}: {len(ps)} referencias originales entre {rango}, envío gratis a toda Colombia. Te ayudamos a encontrar el de tu nevera.",
           f"Filtro para nevera {marca}", "Nevera, nevecón o refrigerador",
           f"En Colombia le decimos nevera, nevecón o refrigerador, pero el filtro es el mismo: va en las neveras {esc(marca)} con dispensador de agua o máquina de hielo. Somos distribuidor autorizado {esc(marca)} y tenemos {len(ps)} referencias originales.",
           f'<div class="m-cols">'
           + f'<div class="m-bloque"><div class="ic">🧊</div><h3>Filtro interno</h3><p>Va dentro de la nevera, arriba o en la rejilla de abajo. {"Referencias: " + esc(", ".join(p["ref"] for p in internos)) + "." if internos else ""}</p></div>'
           + (f'<div class="m-bloque"><div class="ic">🚰</div><h3>Filtro externo</h3><p>Va en la manguera del agua, por detrás de la nevera. Sirve para las neveras que no traen filtro adentro. Referencia: {esc(", ".join(p["ref"] for p in externos))}.</p></div>' if externos else "")
           + f'<div class="m-bloque"><div class="ic">🔎</div><h3>¿Cuál es el tuyo?</h3><p>{esc(info["etiqueta"])} <a href="{base}cual-es-mi-filtro/">Búscalo en la tabla</a>.</p></div></div>'
           + f'<div style="margin-top:22px">{tabla}</div>',
           [(f"¿Qué filtro lleva mi nevera {marca}?", f"Depende del modelo. {info['etiqueta']} Con el modelo o con la referencia del filtro viejo lo encuentras en nuestra tabla, o escríbenos por WhatsApp."),
            (f"¿Es lo mismo filtro para nevera y para nevecón {marca}?", "Sí. Nevera, nevecón y refrigerador son la misma cosa; lo que cambia es el modelo, y cada modelo usa una referencia de filtro."),
            (f"¿Cuánto cuesta el filtro de la nevera {marca}?", f"Entre {rango} según la referencia, con envío gratis a toda Colombia.")])

    # 2. precio
    pagina(f"{base}precio-filtro-{s}/", f"Precio filtro nevera {marca} en Colombia {anio} | Originales",
           f"Precios {anio} de los filtros de agua {marca} originales en Colombia: entre {rango} con envío gratis. Pack de 2 con descuento. Paga con tarjeta, PSE o Nequi.",
           f"Precio del filtro de agua {marca} en Colombia ({anio})", "Precios actualizados",
           f"Estos son los precios de los filtros {esc(marca)} originales, con el envío a cualquier ciudad de Colombia ya incluido. Con el pack de 2 tienes el año completo (se cambia cada 6 meses) y ahorras.",
           tabla + '<ul class="m-ok" style="margin-top:22px"><li><b>Envío gratis</b> a toda Colombia, sin costos escondidos.</li><li><b>Pago seguro</b> con tarjeta débito o crédito, PSE, Nequi o botón Bancolombia.</li><li><b>Originales</b>: somos distribuidor autorizado ' + esc(marca) + ".</li></ul>"
           + '<p class="m-mut" style="margin-top:14px">¿Viste un filtro mucho más barato? Desconfía: los filtros de imitación usan la misma referencia, pero no filtran igual y pueden gotear.</p>',
           [(f"¿Por qué varía el precio del filtro {marca}?", "Cada referencia tiene un precio distinto según su tamaño y tecnología. Los externos de manguera son más económicos que los internos."),
            ("¿El precio incluye el envío?", "Sí. El envío es gratis a toda Colombia y llega en 2 a 3 días hábiles a las principales ciudades."),
            ("¿Hay descuento por comprar dos?", "Sí. El pack de 2 filtros cuesta menos que dos sueltos y te alcanza para un año.")])

    # 3. luz del filtro
    pasos_reset = "".join(f'<div class="m-bloque"><h3><a href="{base}{p["slug_o"]}/">{esc(p["nombre_largo"])}</a></h3><p>{esc(ctx["datos"](p)["reset"])}</p></div>' for p in ps)
    pagina(f"{base}luz-filtro-{s}/", f"Luz del filtro de la nevera {marca}: cómo reiniciarla",
           f"¿Se prendió la luz del filtro de tu nevera {marca}? Qué significa, cuándo cambiar el filtro y cómo reiniciar el aviso en cada modelo, paso a paso.",
           f"Luz del filtro de la nevera {marca}: qué significa y cómo reiniciarla", "Aviso del filtro",
           esc(info["aviso"]) + " La luz no mide qué tan sucio está el filtro: cuenta el tiempo (unos 6 meses). Por eso, después de cambiarlo, hay que reiniciar el aviso.",
           '<h2 style="font-size:22px;margin-bottom:14px">Cómo reiniciar el aviso según tu filtro</h2><div class="m-cols">' + pasos_reset + "</div>"
           + '<p class="m-mut" style="margin-top:16px">Si la luz no se apaga, deja presionado el botón un poco más (hasta 5 segundos) o revisa en el manual el botón que dice «Filter». Los filtros externos no prenden ninguna luz.</p>',
           [(f"¿Puedo apagar la luz del filtro {marca} sin cambiarlo?", "Sí se puede reiniciar, pero no conviene: el filtro saturado deja pasar cloro y sedimento, y el agua y el hielo cogen mal sabor."),
            ("¿Cada cuánto se prende la luz?", "Más o menos cada 6 meses, que es lo que dura un filtro con uso normal."),
            ("¿Qué pasa si no cambio el filtro?", "El agua sale con menos presión y mal sabor, y la suciedad puede afectar la válvula y la máquina de hielo.")],
           miga_nombre="Luz del filtro")

    # 4. cada cuánto cambiar
    pagina(f"{base}cada-cuanto-cambiar-filtro-{s}/", f"¿Cada cuánto cambiar el filtro de la nevera {marca}?",
           f"El filtro de agua de la nevera {marca} se cambia cada 6 meses. Señales de que ya está saturado, qué pasa si no lo cambias y cómo hacerlo tú mismo.",
           f"¿Cada cuánto se cambia el filtro de la nevera {marca}?", "Cada 6 meses",
           f"La respuesta corta: <b>cada 6 meses</b>. Si en tu casa son muchas personas, usan mucho hielo o el agua de tu ciudad trae mucho sedimento, puede tocar antes.",
           '<div class="m-cols">' + "".join(f'<div class="m-bloque"><div class="ic">{i}</div><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for i, t, d in [
               ("📅", "Pasaron 6 meses", "Aunque todo se vea bien, el carbón del filtro ya está saturado."),
               ("👅", "Sabor u olor raro", "El agua o el hielo saben a cloro, a tierra o a encerrado."),
               ("💧", "Menos presión", "El dispensador bota menos agua o tarda más en llenar el vaso."),
               ("💡", "Se prendió la luz", info["aviso"])]) + "</div>"
           + f'<p style="margin-top:18px">Cambiarlo es fácil y no necesitas técnico: mira <a href="{base}cambio-e-instalacion/">el paso a paso de cada filtro {esc(marca)}</a>. Con el pack de 2 tienes el año completo.</p>',
           [("¿Qué pasa si no cambio el filtro a tiempo?", "El filtro se tapa: baja la presión, el agua coge mal sabor y la suciedad puede llegar a la válvula y a la máquina de hielo."),
            ("¿Puedo lavar el filtro y volverlo a usar?", "No. Por dentro tiene carbón activado que se satura; lavarlo no lo recupera."),
            ("¿Puedo usar la nevera sin filtro?", "Algunos modelos traen un tapón para usarla sin filtro, pero el agua sale sin filtrar. Lo mejor es cambiarlo.")])

    # 5. dónde comprar
    pagina(f"{base}donde-comprar-filtro-{s}/", f"Dónde comprar filtros {marca} originales en Colombia",
           f"Compra filtros de agua {marca} originales a un distribuidor autorizado en Colombia: envío gratis a todo el país, pago seguro y asesoría por WhatsApp.",
           f"Dónde comprar filtros de agua {marca} originales en Colombia", "Distribuidor autorizado",
           f"Aquí mismo. Somos <b>distribuidor autorizado {esc(marca)}</b> y enviamos filtros originales a cualquier ciudad o municipio de Colombia, con envío gratis.",
           '<div class="m-cols">' + "".join(f'<div class="m-bloque"><div class="ic">{i}</div><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for i, t, d in h.verificar(marca)) + "</div>"
           + f'<h2 style="font-size:22px;margin:28px 0 12px">Cómo reconocer un filtro {esc(marca)} de imitación</h2><ul class="m-ok"><li>El precio es mucho más bajo que el normal.</li><li>La caja viene sin sellar, con letras borrosas o errores de ortografía.</li><li>El filtro no encaja firme o gotea al ponerlo.</li><li>El vendedor no da factura ni datos de contacto.</li></ul>',
           [(f"¿Venden filtros {marca} en mi ciudad?", "Enviamos a toda Colombia con envío gratis. A las principales ciudades llega en 2 a 3 días hábiles."),
            ("¿Cómo sé que es original?", "Llega en su caja de fábrica sellada, con la referencia y el código de barras. Si quieres, antes de pagar te mandamos fotos reales por WhatsApp."),
            ("¿Puedo pagar contra entrega?", "No. El pago es en línea, en una página de pago segura, con tarjeta, PSE o Nequi.")])

    # 6. original o genérico
    pagina(f"{base}filtro-{s}-original-o-generico/", f"Filtro {marca} original o genérico: diferencias",
           f"¿Vale la pena el filtro {marca} original o sirve uno genérico? Diferencias en filtrado, ajuste, fugas y duración, para que decidas bien.",
           f"Filtro {marca} original o genérico: ¿cuál conviene?", "Compara antes de comprar",
           f"Los filtros genéricos usan la misma referencia del {esc(marca)} original, pero no son iguales por dentro. Estas son las diferencias que más importan.",
           '<div class="m-tabla-wrap"><table class="m-tabla"><thead><tr><th></th><th>Original ' + esc(marca) + '</th><th>Genérico</th></tr></thead><tbody>'
           + "".join(f"<tr><td><b>{esc(a)}</b></td><td>{esc(b)}</td><td>{esc(c)}</td></tr>" for a, b, c in [
               ("Ajuste", "Encaja exacto en la nevera", "Puede quedar flojo o gotear"),
               ("Filtrado", "Hecho para la nevera " + marca, "Varía según el fabricante"),
               ("Aviso del filtro", "La nevera lo reconoce sin problema", "Algunos modelos no lo reconocen"),
               ("Empaque", "Caja de fábrica sellada", "Empaque genérico"),
               ("Precio", "Mayor", "Menor")]) + "</tbody></table></div>"
           + '<p style="margin-top:16px">Un filtro que gotea puede dañar el piso o la nevera, y uno que no filtra bien deja pasar el cloro y el sedimento. Por eso recomendamos el original.</p>',
           [("¿Un filtro genérico daña la nevera?", "No siempre, pero si no encaja bien puede gotear, y si no filtra bien la suciedad llega a la válvula y a la máquina de hielo."),
            ("¿El original dura más?", "Ambos se cambian cada 6 meses, pero el original mantiene el filtrado y la presión durante todo ese tiempo.")],
           miga_nombre="Original o genérico")

    # 7. filtro externo
    if externos:
        e = externos[0]
        pagina(f"{base}filtro-externo-nevera-{s}/", f"Filtro externo para nevera {marca} original | {cop(e['precio'])}",
               f"Filtro externo de manguera para nevera {marca}, referencia {e['ref']}: para neveras sin filtro interno. {cop(e['precio'])} con envío gratis a toda Colombia.",
               f"Filtro externo para nevera {marca}", "Filtro de manguera",
               f"El filtro externo va en la manguera delgada que lleva el agua a la nevera. Sirve para neveras {esc(marca)} que no traen filtro adentro, o como filtro adicional. Referencia original: <b>{esc(e['ref'])}</b>.",
               h.caja(e, base, ctx["foto"]) + f'<p style="margin-top:16px"><a href="{base}{e["slug_o"]}/#instalacion">Cómo se instala, paso a paso</a> (10 a 15 minutos, sin herramientas especiales).</p>',
               [("¿Mi nevera necesita filtro externo?", "Si tu nevera tiene dispensador o máquina de hielo y no trae filtro adentro, sí. Si ya trae filtro interno, el externo es opcional."),
                ("¿El filtro externo prende la luz del filtro?", "No. Anota la fecha de instalación en el filtro y cámbialo a los 6 meses.")])

    # 7b. problemas comunes (la gente los busca justo antes de comprar o al cambiar el filtro)
    def lista(items):
        return '<ol class="m-pasos">' + "".join(f"<li><b>{esc(a)}</b> {esc(b)}</li>" for a, b in items) + "</ol>"
    pagina(f"{base}nevera-{s}-no-sale-agua-despues-de-cambiar-el-filtro/", f"Nevera {marca} no sale agua después de cambiar el filtro: solución",
           f"¿Cambiaste el filtro de tu nevera {marca} y no sale agua? Las 6 causas más comunes y cómo solucionarlo tú mismo en minutos.",
           f"Mi nevera {marca} no saca agua después de cambiar el filtro", "Solución paso a paso",
           f"Es lo más común después de un cambio de filtro y casi siempre se arregla en minutos, sin técnico. Revisa en este orden:",
           lista([("El filtro no quedó encajado.", "Sácalo y vuelve a meterlo derecho, hasta el fondo, y gíralo hasta que haga clic o quede firme."),
                  ("Quedó la tapa protectora puesta.", "Algunos filtros traen un capuchón en la punta: quítalo antes de instalar."),
                  ("Hay aire en la línea.", "Presiona el dispensador 5 segundos y suelta, varias veces, hasta sacar unos 4 litros. Al principio sale con burbujas o a chorros."),
                  ("La llave de paso está cerrada.", "Revisa la llave del agua que alimenta la nevera, por detrás o debajo del lavaplatos."),
                  ("La manguera está doblada o congelada.", "Al mover la nevera la manguera se puede doblar. Si hace mucho frío en la puerta, la línea se congela: sube un poco la temperatura."),
                  ("El filtro es de imitación.", f"Algunos genéricos no abren bien la válvula de la nevera {marca}. Con el original no pasa.")])
           + f'<p style="margin-top:16px">Mira el <a href="{base}cambio-e-instalacion/">paso a paso de instalación de cada filtro {esc(marca)}</a>. ¿Sigue sin salir agua? Escríbenos por WhatsApp y te ayudamos.</p>',
           [("¿Cuánta agua hay que sacar después de cambiar el filtro?", "Unos 4 litros, para sacar el aire y el carbón suelto. Bota también el primer hielo."),
            ("¿Es normal que el agua salga turbia o blanca?", "Sí, los primeros vasos salen con aire o carbón suelto. Se aclara en unos minutos.")],
           miga_nombre="No sale agua")
    pagina(f"{base}filtro-nevera-{s}-gotea/", f"El filtro de la nevera {marca} gotea: causas y solución",
           f"¿Gotea el filtro de tu nevera {marca}? Por qué pasa (mal encajado, empaque dañado, filtro genérico) y cómo solucionarlo antes de que dañe el piso.",
           f"El filtro de mi nevera {marca} gotea: ¿qué hago?", "Solución paso a paso",
           "Una gota al cambiar el filtro es normal. Si sigue goteando, revisa esto:",
           lista([("Encájalo de nuevo.", "Sácalo y vuelve a meterlo derecho hasta el fondo: un filtro torcido es la causa número uno."),
                  ("Revisa los empaques (o-rings).", "Los anillos de caucho de la punta deben estar completos y sin cortes."),
                  ("Revisa la tapa o el soporte.", "Si la carcasa del filtro o la tapa tienen una grieta, el agua sale por ahí."),
                  ("Filtro externo: revisa los racores.", "La manguera debe entrar hasta el fondo del racor rápido y estar cortada derecha."),
                  ("Filtros genéricos.", f"Muchas fugas vienen de filtros de imitación que no encajan exacto. El {marca} original sella bien.")])
           + '<p style="margin-top:16px">Mientras lo revisas, cierra la llave de paso del agua para no mojar el piso.</p>',
           [("¿Puedo usar la nevera si el filtro gotea?", "Mejor no. Cierra la llave del agua hasta encajarlo bien o cambiarlo: el agua puede dañar el piso o la nevera."),
            ("¿Por qué gotea un filtro nuevo?", "Casi siempre porque quedó torcido o le falta un empaque. Si es genérico, puede que no encaje exacto.")],
           miga_nombre="El filtro gotea")
    pagina(f"{base}agua-o-hielo-con-mal-sabor-nevera-{s}/", f"Agua o hielo con mal sabor en la nevera {marca}: solución",
           f"¿El agua o el hielo de tu nevera {marca} saben raro? Las causas más comunes (filtro saturado, hielo viejo, dispensador sucio) y cómo solucionarlo.",
           f"El agua o el hielo de mi nevera {marca} saben mal", "Solución paso a paso",
           "Si el agua o el hielo saben a cloro, a tierra, a plástico o a encerrado, revisa esto:",
           lista([("El filtro está saturado.", "Si tiene más de 6 meses, ya no retiene el cloro ni el sedimento. Es la causa más común."),
                  ("El hielo es viejo.", "El hielo guardado coge el olor de los alimentos. Bota el hielo del depósito y deja que se haga nuevo."),
                  ("Acabas de cambiar el filtro.", "Saca 4 litros de agua y bota el primer hielo: al principio puede salir con carbón suelto."),
                  ("El dispensador está sucio.", "Limpia la boquilla y la bandeja con agua tibia y bicarbonato."),
                  ("Alimentos destapados.", "Los olores fuertes pasan al hielo: tapa los alimentos y usa un poco de bicarbonato en la nevera.")]),
           [("¿El filtro quita el mal sabor del agua?", "Sí: el carbón activado retiene el cloro y los olores mientras no esté saturado."),
            ("¿Cada cuánto debo cambiar el filtro para que no sepa mal?", "Cada 6 meses, o antes si notas el sabor raro.")],
           miga_nombre="Mal sabor")

    # 8. referencias equivalentes
    for r, p, ruta in R["refs"].values():
        otros = [x for x in p["refs"] if x != r]
        pagina(ruta, f"Filtro {r} original {marca} | Envío gratis Colombia",
               f"Filtro {r}: es el {p['nombre_largo']} original. {cop(p['precio'])} con envío gratis a toda Colombia. Te lo confirmamos por WhatsApp.",
               f"Filtro {r}", f"Referencia equivalente {marca}",
               f"Si tu filtro viejo dice <b>{esc(r)}</b>, el que necesitas es el <b>{esc(p['nombre_largo'])}</b> original. Es la misma pieza con otra referencia de fábrica.",
               h.caja(p, base, ctx["foto"]) + f'<p style="margin-top:16px">También aparece como: {esc(", ".join(otros))}.</p>',
               [(f"¿El {r} y el {p['ref']} son el mismo filtro?", f"Sí. {r} es otra referencia del mismo filtro {marca}; sirve en las mismas neveras."),
                (f"¿Cuánto cuesta el filtro {r}?", f"{cop(p['precio'])} con envío gratis a toda Colombia, o {cop(p['pack'])} el pack de 2.")],
               ld_extra=h.producto_ld(p, ruta, f"Filtro {r} ({p['nombre_largo']} original)", marca))

    # 9. modelos de nevera
    for m, p, ruta in R["modelos"].values():
        pagina(ruta, f"Filtro para nevera {marca} {m} | Original, envío gratis",
               f"El filtro de agua de la nevera {marca} {m} es el {p['nombre_largo']} original: {cop(p['precio'])} con envío gratis a toda Colombia. Paso a paso para cambiarlo.",
               f"Filtro para nevera {marca} {m}", "Por modelo de nevera",
               f"La nevera <b>{esc(marca)} {esc(m)}</b> usa el filtro <b>{esc(p['nombre_largo'])}</b>. {esc(ctx['datos'](p)['donde'])}",
               h.caja(p, base, ctx["foto"]) + f'<p style="margin-top:16px">Para reiniciar el aviso: {esc(ctx["datos"](p)["reset"])}</p>',
               [(f"¿Qué filtro usa la nevera {m}?", f"El {p['nombre_largo']} original (referencia {p['ref']})."),
                (f"¿Dónde va el filtro de la {m}?", ctx["datos"](p)["donde"])],
               miga_nombre=f"Nevera {m}", ld_extra=h.producto_ld(p, ruta, f"Filtro para nevera {marca} {m}", marca))

    # 10. ciudades
    for nombre, (c, ruta) in R["ciudades"].items():
        dias = f"{c[2]} días hábiles" if len(c) > 2 and c[2] else "2 a 3 días hábiles"
        pagina(ruta, f"Filtro nevera {marca} en {nombre} | Original, envío gratis",
               f"Filtros de agua {marca} originales en {nombre}, {c[1]}: llegan en {dias} con envío gratis. Distribuidor autorizado. Paga con tarjeta, PSE o Nequi.",
               f"Filtro para nevera {marca} en {nombre}", f"{nombre}, {c[1]}",
               f"Te enviamos el filtro {esc(marca)} original a tu casa u oficina en <b>{esc(nombre)}</b>. Llega en <b>{esc(dias)}</b> con envío gratis y número de guía para que sigas el paquete.",
               '<div class="m-cols m-num">' + "".join(f'<div class="m-bloque"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t, d in [
                   ("Escoge tu filtro", f"Por la referencia del filtro viejo o el modelo de tu nevera {marca}."),
                   ("Paga en línea", "Con tarjeta, PSE o Nequi en página segura."),
                   (f"Recíbelo en {nombre}", f"En {dias}, con envío gratis.")]) + "</div>",
               [(f"¿Cuánto tarda el envío a {nombre}?", f"Unos {dias} después de confirmar el pago."),
                (f"¿Cuánto cuesta el envío a {nombre}?", "Nada, el envío es gratis."),
                (f"¿Tienen tienda física en {nombre}?", "Vendemos en línea y enviamos a toda Colombia; te asesoramos por WhatsApp.")],
               miga_nombre=f"Envíos a {nombre}")
    return hechas


def relacionadas(R, actual, marca):
    """Enlaces a las demás subpáginas: ayudan a Google a encontrarlas todas y al cliente a seguir buscando."""
    temas = "".join(f'<a href="{r}">{esc(t)}</a>' for r, t in R["temas"] if r != actual)
    ciudades = "".join(f'<a href="{r}">{esc(n)}</a>' for n, (_, r) in R["ciudades"].items() if r != actual)
    return (f'<div class="m-cab"><span class="eyebrow">Te puede servir</span><h2>Más sobre filtros {esc(marca)}</h2></div>'
            f'<div class="m-chips">{temas}</div><h3 style="margin:22px 0 10px">Envíos por ciudad</h3><div class="m-chips">{ciudades}</div>')
