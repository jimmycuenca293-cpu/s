"""SEO de la tienda principal: páginas pensadas para lo que la gente escribe en Google.

- temas por marca (precio, luz del filtro, cada cuánto cambiar, dónde comprar, filtro externo, problemas, instalación, por modelo)
- una página por marca y ciudad (las ciudades más grandes)
- guías generales con términos de búsqueda (nevera, nevecón, refrigerador, con dispensador, precio, dónde comprar…)

Las usa paginas_seo.generar() (que ya sabe escribir páginas en la tienda) y build.py (portada de cada marca y portada).
Sin términos de marca prohibidos en Google Ads.
"""
import html

import instalacion
import marcas_exclusivas

esc = lambda s: html.escape(str(s), quote=True)
cop = lambda n: "$ " + f"{n:,}".replace(",", ".")
ANIO = 2026


FOTOS = {"alerta": ("tienda-alerta", "Pantalla del nevecón que dice «Cambie el filtro de agua»", "🔔 Así avisa el nevecón cuando toca cambiar el filtro"),
         "agua": ("tienda-agua", "Mujer sirviéndose agua con hielo del dispensador del nevecón", "💧 Con el filtro nuevo, el agua y el hielo salen limpios otra vez"),
         "familia": ("tienda-familia", "Familia sirviéndose agua con hielo del dispensador del nevecón", "👨‍👩‍👧 Agua y hielo limpios para toda la familia"),
         "asesoria": ("tienda-asesoria", "Asesora de la tienda mostrando en el celular cómo pedir el filtro de agua", "💬 Te ayudamos a escoger tu filtro y a pedirlo"),}


def figura(clave, pie=None):
    n, alt, leyenda = FOTOS[clave]
    return (f'<figure class="foto-sec"><picture><source srcset="/img/{n}-640.webp 640w, /img/{n}.webp 1024w" sizes="(max-width:700px) 100vw, 700px" type="image/webp">'
            f'<img src="/img/{n}.jpg" alt="{esc(alt)}" width="1024" height="576" loading="lazy"></picture><figcaption>{esc(pie or leyenda)}</figcaption></figure>')


def temas(marca, s, tiene_externo):
    """[(ruta, titulo corto)] de los temas de una marca. Se usa para escribirlas y para enlazarlas."""
    b = f"/marca/{s}/"
    t = [(f"{b}filtro-de-agua-para-nevera-{s}/", f"Filtro de agua para nevera {marca}"),
         (f"{b}precio-filtro-nevera-{s}/", f"Precio del filtro de nevera {marca}"),
         (f"{b}como-cambiar-filtro-nevera-{s}/", f"Cómo cambiar el filtro de la nevera {marca}"),
         (f"{b}luz-filtro-nevera-{s}/", f"Luz del filtro {marca}: cómo reiniciarla"),
         (f"{b}cada-cuanto-cambiar-filtro-nevera-{s}/", f"Cada cuánto cambiar el filtro {marca}"),
         (f"{b}donde-comprar-filtro-nevera-{s}/", f"Dónde comprar filtros {marca}"),
         (f"{b}filtro-nevera-{s}-por-modelo/", f"Filtro por modelo de nevera {marca}")]
    if tiene_externo:
        t.append((f"{b}filtro-externo-nevera-{s}/", f"Filtro externo para nevera {marca}"))
    t += [(f"{b}nevera-{s}-no-sale-agua-despues-de-cambiar-el-filtro/", f"{marca} no sale agua después de cambiar el filtro"),
          (f"{b}filtro-nevera-{s}-gotea/", f"El filtro {marca} gotea"),
          (f"{b}agua-con-mal-sabor-nevera-{s}/", f"Agua con mal sabor en nevera {marca}")]
    return t


def ciudades_chips(marca, s, slug, CIUDADES_CO):
    return (f'<section class="caja"><h2>Filtros para nevera {esc(marca)} por ciudad</h2><div class="chips">'
            + "".join(f'<a href="/marca/{s}/{slug(c[0])}/">{esc(c[0])}</a>' for c in CIUDADES_CO[:40]) + '</div></section>')


def generar(escribir, miga, faq_ld, faq_html, caja_producto, tarjeta, CATALOGO, MARCAS, slug, norm, ubic, CIUDADES_CO, rutas_ciudad, modelos_dir):
    """Escribe los temas y las páginas por ciudad de cada marca. Devuelve {marca: [(ruta, titulo)]}."""
    salida = {}
    top_ciudades = [c for c in CIUDADES_CO][:40]
    for marca in MARCAS:
        info = marcas_exclusivas.MARCAS_INFO[marca]
        ps = [p for p in CATALOGO if p["marca"] == marca]
        ext = [p for p in ps if ubic(p) == "externo"]
        s = slug(marca)
        b = f"/marca/{s}/"
        lista = temas(marca, s, bool(ext))
        salida[marca] = lista
        rango = f"{cop(min(p['precio'] for p in ps))} a {cop(max(p['precio'] for p in ps))}"
        mg0 = lambda nombre: miga(("Inicio", "/"), (f"Filtros {marca}", b), (nombre, None))
        grid = '<div class="grid">' + "".join(tarjeta(p) for p in ps) + "</div>"
        otros = '<section class="caja"><h2>Más sobre filtros ' + esc(marca) + '</h2><div class="chips">' + "".join(
            f'<a href="{r}">{esc(t)}</a>' for r, t in lista) + '</div></section>'
        refs_txt = ", ".join(p["ref"] for p in ps)
        tabla = ('<div class="caja" style="overflow-x:auto"><table class="t"><tr><th>Filtro</th><th>Referencia</th><th>Tipo</th><th>Precio</th><th>Pack de 2</th></tr>'
                 + "".join(f'<tr><td><a href="/filtro/{p["slug"]}/">{esc(p["nombre_largo"])}</a></td><td><span class="ref">{esc(p["ref"])}</span></td>'
                           f'<td>{"Externo" if ubic(p) == "externo" else "Interno"}</td><td><b>{cop(p["precio"])}</b></td><td>{cop(p["pack"])}</td></tr>' for p in ps) + "</table></div>")

        def pagina(ruta, titulo, desc, h1, intro, cuerpo, preguntas, nombre_miga, foto=None):
            mg, mg_ld = mg0(nombre_miga)
            art = {"@type": "Article", "headline": h1, "description": desc, "inLanguage": "es-CO", "datePublished": "2026-10-18", "dateModified": "2026-10-18",
                   "author": {"@id": "__BASE__/#tienda"}, "mainEntityOfPage": f"__BASE__{ruta}"}
            escribir(ruta, titulo, desc, [mg_ld, art, faq_ld(preguntas)],
                     f'{mg}\n<h1>{esc(h1)}</h1>\n<p>{intro}</p>\n{figura(foto) if foto else ""}\n{cuerpo}\n{grid}\n{faq_html(preguntas)}\n{otros}')

        # 1. filtro de agua para nevera {marca}
        pagina(f"{b}filtro-de-agua-para-nevera-{s}/", f"Filtro de agua para nevera {marca} | {len(ps)} referencias, envío gratis",
               f"Filtros de agua para nevera {marca} ({refs_txt}): precios entre {rango}, envío gratis a toda Colombia. Te decimos cuál le sirve a tu nevera o nevecón {marca}.",
               f"Filtro de agua para nevera {marca}",
               f"En Colombia le decimos <b>nevera</b>, <b>nevecón</b> o <b>refrigerador</b>, pero el filtro es el mismo: va en las neveras {esc(marca)} con dispensador de agua o máquina de hielo ({esc(info['lineas'])}). "
               f"Tenemos {len(ps)} referencias, con envío gratis a toda Colombia.",
               "<h2>Las referencias de filtro " + esc(marca) + "</h2>" + tabla
               + f'<section class="caja"><h2>¿Cuál filtro necesita mi nevera {esc(marca)}?</h2><ol><li>Saca el filtro viejo y busca la referencia impresa en la etiqueta (por ejemplo <span class="ref">{esc(ps[0]["ref"])}</span>).</li>'
                 f'<li>Si no se lee, busca el modelo de la nevera: {esc(info["etiqueta"])}</li>'
                 f'<li>Compara con el <a href="/referencias/">directorio de referencias</a> o con la lista de <a href="{b}filtro-nevera-{s}-por-modelo/">modelos de nevera {esc(marca)}</a>.</li></ol></section>',
               [(f"¿Qué filtro de agua usa una nevera {marca}?", f"Depende del modelo. Las referencias más comunes son {refs_txt}. Con el modelo o con la referencia del filtro viejo te confirmamos cuál es."),
                (f"¿El filtro de nevera y el de nevecón son diferentes?", "No. Nevera, nevecón y refrigerador son el mismo electrodoméstico; el filtro depende de la marca y del modelo, no del nombre."),
                ("¿Cuánto cuesta el envío?", "Nada: el envío es gratis a toda Colombia y el precio que ves es el precio final.")],
               "Filtro de agua para nevera", foto="agua")

        # 2. precio
        pagina(f"{b}precio-filtro-nevera-{s}/", f"Precio filtro nevera {marca} en Colombia {ANIO} | {rango}",
               f"Precios {ANIO} de los filtros de agua para nevera {marca} en Colombia: entre {rango} con envío gratis. Pack de 2 filtros con descuento. Paga con tarjeta, PSE o Nequi.",
               f"Precio del filtro de nevera {marca} en Colombia ({ANIO})",
               f"Estos son los precios del filtro de agua para nevera {esc(marca)}, con el envío a cualquier ciudad de Colombia ya incluido. Con el pack de 2 tienes el año completo (se cambia cada 6 meses) y ahorras.",
               "<h2>Lista de precios " + esc(marca) + "</h2>" + tabla
               + '<ul class="ok"><li><b>Envío gratis</b> a toda Colombia, sin costos escondidos.</li><li><b>Pago seguro</b> con tarjeta débito o crédito, PSE, Nequi o botón Bancolombia.</li>'
                 '<li><b>Pack anual de 2 filtros</b>: uno para ahora y otro para dentro de 6 meses, a menor precio por unidad.</li></ul>',
               [(f"¿Cuánto cuesta un filtro de nevera {marca}?", f"Entre {rango}, según la referencia. El envío está incluido."),
                ("¿Por qué cambia el precio entre referencias?", "Los filtros externos y los internos de mayor capacidad cuestan más. El precio de cada uno aparece en la tabla."),
                ("¿Hay descuento si compro dos?", "Sí: el pack anual de 2 filtros sale más barato que comprarlos por separado.")],
               "Precio del filtro")

        # 3. cómo cambiar
        pasos = "".join(
            f'<section class="caja"><h2><a href="/filtro/{p["slug"]}/#instalacion">Cómo cambiar el {esc(p["nombre_largo"])}</a></h2>'
            f'<p><b>Dónde va:</b> {esc(instalacion.datos(p)["donde"])} <b>Tiempo:</b> {esc(instalacion.datos(p)["tiempo"])}. <b>Herramientas:</b> {esc(instalacion.datos(p)["herramientas"])}</p>'
            f'<ol>{"".join(f"<li>{esc(x)}</li>" for x in instalacion.datos(p)["pasos"])}</ol><p><b>Último paso:</b> {esc(instalacion.datos(p)["reset"])}</p></section>' for p in ps)
        pagina(f"{b}como-cambiar-filtro-nevera-{s}/", f"Cómo cambiar el filtro de la nevera {marca} paso a paso",
               f"Paso a paso para cambiar el filtro de agua de la nevera {marca}, referencia por referencia: dónde va, cuánto tarda, qué necesitas y cómo reiniciar la luz.",
               f"Cómo cambiar el filtro de agua de la nevera {marca}",
               f"Cambiar el filtro de una nevera {esc(marca)} no requiere técnico ni herramientas. Busca tu referencia y sigue los pasos.", pasos,
               [("¿Necesito cerrar la llave del agua?", "En los filtros internos no hace falta; en los externos sí, antes de soltar la manguera."),
                ("¿Cuánto tarda el cambio?", "Los internos, un par de minutos; los externos, de 10 a 15 minutos."),
                ("¿Por qué sale aire o agua turbia al principio?", "Es normal: el filtro nuevo suelta aire y polvo de carbón. Saca unos 6 litros por el dispensador para limpiarlo.")],
               "Cómo cambiar el filtro", foto="agua")

        # 4. luz del filtro
        reset = "".join(f'<section class="caja"><h2><a href="/filtro/{p["slug"]}/">{esc(p["nombre_largo"])}</a></h2><p>{esc(instalacion.datos(p)["reset"])}</p></section>' for p in ps)
        pagina(f"{b}luz-filtro-nevera-{s}/", f"Luz del filtro de la nevera {marca}: qué significa y cómo reiniciarla",
               f"¿Se prendió la luz del filtro de tu nevera {marca}? Qué significa, cuándo cambiarlo y cómo reiniciar el aviso en cada modelo, paso a paso.",
               f"Luz del filtro de la nevera {marca}: qué significa y cómo reiniciarla",
               esc(info["aviso"]) + " La luz no mide qué tan sucio está el filtro: cuenta el tiempo de uso (unos 6 meses). Por eso, al cambiarlo, hay que reiniciar el aviso.",
               "<h2>Cómo reiniciar el aviso según tu filtro</h2>" + reset
               + '<p class="m">Si la luz no se apaga, deja presionado el botón un poco más (hasta 5 segundos) o revisa en el manual el botón que dice «Filter». Los filtros externos no prenden luz.</p>',
               [(f"¿Puedo apagar la luz del filtro {marca} sin cambiarlo?", "Se puede reiniciar, pero no conviene: un filtro saturado deja pasar cloro y sedimento y el agua y el hielo cogen mal sabor."),
                ("¿Cada cuánto se prende la luz?", "Más o menos cada 6 meses, que es lo que dura un filtro con uso normal."),
                ("¿La luz sigue prendida con el filtro nuevo?", "Falta reiniciar el aviso: se hace a mano, con el botón del panel, después de cambiar el filtro.")],
               "Luz del filtro", foto="alerta")

        # 5. cada cuánto
        pagina(f"{b}cada-cuanto-cambiar-filtro-nevera-{s}/", f"¿Cada cuánto cambiar el filtro de la nevera {marca}? | Señales y plazos",
               f"El filtro de agua de la nevera {marca} se cambia cada 6 meses. Señales de que ya está saturado, qué pasa si no lo cambias y cómo hacerlo tú mismo.",
               f"¿Cada cuánto se cambia el filtro de la nevera {marca}?",
               "La respuesta corta: <b>cada 6 meses</b>. Si en tu casa son muchas personas, usan mucho hielo o el agua de tu ciudad trae sedimento, puede tocar antes.",
               '<ul class="ok"><li><b>Pasaron 6 meses:</b> aunque todo se vea bien, el carbón del filtro ya está saturado.</li><li><b>Sabor u olor raro:</b> el agua o el hielo saben a cloro, a tierra o a encerrado.</li>'
               '<li><b>Menos presión:</b> el dispensador bota menos agua o tarda más en llenar el vaso.</li>'
               f'<li><b>Se prendió la luz:</b> {esc(info["aviso"])}</li></ul>',
               [("¿Qué pasa si no cambio el filtro a tiempo?", "Se tapa: baja la presión, el agua coge mal sabor y la suciedad puede llegar a la válvula y a la máquina de hielo."),
                ("¿Puedo lavar el filtro y volver a usarlo?", "No. Por dentro tiene carbón activado que se satura; lavarlo no lo recupera."),
                ("¿Puedo usar la nevera sin filtro?", "Algunos modelos traen un tapón para usarla sin filtro, pero el agua sale sin filtrar. Lo mejor es cambiarlo.")],
               "Cada cuánto cambiarlo", foto="alerta")

        # 6. dónde comprar
        pagina(f"{b}donde-comprar-filtro-nevera-{s}/", f"Dónde comprar filtros de nevera {marca} en Colombia | Envío gratis",
               f"Compra filtros de agua para nevera {marca} en Colombia: envío gratis a todo el país, pago seguro en línea y asesoría por WhatsApp para escoger el tuyo.",
               f"Dónde comprar filtros de agua para nevera {marca} en Colombia",
               f"Aquí mismo. Enviamos filtros para nevera {esc(marca)} a cualquier ciudad o municipio de Colombia, con envío gratis y el pago en línea.",
               '<ul class="ok"><li><b>Te ayudamos a escoger:</b> con el modelo o la referencia del filtro viejo te decimos cuál es.</li><li><b>Empaque sellado de fábrica</b> y referencia impresa en la caja.</li>'
               '<li><b>Envío gratis</b> con número de guía; llega en 2 a 3 días hábiles a las principales ciudades.</li><li><b>Pago seguro</b>: tarjeta, PSE, Nequi o botón Bancolombia.</li></ul>'
               '<p class="m">Ciudades con envío: ' + ", ".join(f'<a href="{rutas_ciudad[c[0]]}">{esc(c[0])}</a>' for c in top_ciudades[:12]) + ' y <a href="/envios/">toda Colombia</a>.</p>' + ciudades_chips(marca, s, slug, CIUDADES_CO),
               [(f"¿Venden filtros {marca} en mi ciudad?", "Enviamos a toda Colombia con envío gratis. A las principales ciudades llega en 2 a 3 días hábiles."),
                ("¿Cómo sé que el filtro es el correcto?", "Antes de pagar puedes escribirnos el modelo de tu nevera o la foto del filtro viejo y te confirmamos la referencia."),
                ("¿Puedo pagar contra entrega?", "El pago es en línea, en una página segura, con tarjeta, PSE o Nequi.")],
               "Dónde comprar")

        # 7. por modelo
        modelos = sorted({(m, ruta) for (mm, m, ruta, _) in modelos_dir if mm == marca})
        pagina(f"{b}filtro-nevera-{s}-por-modelo/", f"Filtro para nevera {marca} por modelo | Lista de modelos y referencias",
               f"Busca el modelo de tu nevera {marca} ({', '.join(m for m, _ in modelos[:4])}…) y mira qué filtro de agua usa. Envío gratis a toda Colombia.",
               f"Filtro para nevera {marca} por modelo",
               f"Busca el modelo de tu nevera {esc(marca)}. {esc(info['etiqueta'])}",
               '<section class="caja"><h2>Modelos de nevera ' + esc(marca) + '</h2><div class="chips">' + "".join(f'<a href="{r}">{esc(m)}</a>' for m, r in modelos) + "</div></section>",
               [(f"¿Dónde encuentro el modelo de mi nevera {marca}?", info["etiqueta"]),
                ("¿Y si mi modelo no está en la lista?", "Compara la referencia impresa en el filtro viejo con la tabla de referencias o escríbenos con el modelo y te confirmamos."),
                ("¿Una letra de más al final del modelo cambia el filtro?", "Casi nunca: suele indicar el color o el país. El filtro se define por la serie del modelo.")],
               "Por modelo")

        # 8. externo
        if ext:
            e = ext[0]
            pagina(f"{b}filtro-externo-nevera-{s}/", f"Filtro externo para nevera {marca} | {cop(e['precio'])} con envío gratis",
                   f"Filtro externo de manguera para nevera {marca}, referencia {e['ref']}: {cop(e['precio'])}, envío gratis. Cómo se instala y para qué neveras sirve.",
                   f"Filtro externo para nevera {marca}",
                   f"El filtro externo va en la manguera delgada que lleva el agua a la nevera, por detrás. Sirve para neveras {esc(marca)} que no traen filtro adentro, o como filtro adicional. Referencia: <b>{esc(e['ref'])}</b>.",
                   caja_producto(e, "Filtro externo " + marca) + '<h2>Cómo se instala</h2><ol>' + "".join(f"<li>{esc(x)}</li>" for x in instalacion.datos(e)["pasos"]) + "</ol>",
                   [("¿El filtro externo reemplaza al interno?", "No. Si tu nevera ya trae filtro adentro, el externo es un filtro adicional; si no lo trae, es el único."),
                    ("¿Cada cuánto se cambia?", "Cada 6 meses, igual que los internos."),
                    ("¿Necesito un técnico?", "No. Se conecta con racores rápidos, sin herramientas.")],
                   "Filtro externo")

        # 9-11. problemas
        pagina(f"{b}nevera-{s}-no-sale-agua-despues-de-cambiar-el-filtro/", f"Nevera {marca} no sale agua después de cambiar el filtro: causas y solución",
               f"¿Cambiaste el filtro de tu nevera {marca} y ya no sale agua o sale muy poca? Las causas más comunes y cómo solucionarlas paso a paso.",
               f"Nevera {marca} no sale agua después de cambiar el filtro",
               "Pasa más de lo que se cree y casi siempre tiene solución sencilla. Revisa en este orden:",
               '<ol><li><b>El filtro no quedó bien puesto:</b> sácalo y vuélvelo a meter hasta el fondo, girándolo hasta que quede firme. Revisa que le hayas quitado la tapa protectora.</li>'
               '<li><b>Hay aire en la línea:</b> presiona el dispensador por tandas de 30 segundos hasta que salga un chorro parejo (2 o 3 litros).</li>'
               '<li><b>La referencia no es la de tu nevera:</b> si el filtro no corresponde, no encaja bien y no deja pasar el agua. Compara la referencia con la del filtro anterior.</li>'
               '<li><b>La llave del agua está cerrada o con poca presión:</b> revisa la llave que alimenta la nevera.</li><li><b>Manguera congelada:</b> baja un poco el frío del congelador y espera unas horas.</li></ol>',
               [("¿Cuánto tarda en salir agua con un filtro nuevo?", "Entre 2 y 5 minutos de dispensado en tandas, hasta que el chorro salga parejo."),
                ("¿El filtro nuevo puede estar dañado?", "Es raro. Antes de cambiarlo, vuelve a instalarlo y purga el aire."),
                ("¿Cuándo llamo a un técnico?", "Si ya revisaste todo y sigue sin salir agua, puede ser la válvula de entrada o el interruptor del dispensador.")],
               "No sale agua", foto="agua")
        pagina(f"{b}filtro-nevera-{s}-gotea/", f"Filtro de nevera {marca} gotea o bota agua: causas y solución",
               f"¿El filtro de tu nevera {marca} gotea o hay agua alrededor? Causas más comunes (mal instalado, sello, manguera) y cómo arreglarlo.",
               f"El filtro de la nevera {marca} gotea: causas y solución",
               "Si ves agua alrededor del filtro o en el piso, apaga el dispensador y revisa estas causas:",
               '<ol><li><b>Filtro mal encajado:</b> sácalo, límpialo con un trapo y vuelve a ponerlo hasta el fondo, girándolo hasta que quede firme.</li>'
               '<li><b>Filtro con otra referencia:</b> si no es el de tu nevera, no sella bien y gotea. Verifica la referencia.</li>'
               '<li><b>Sello o empaque dañado:</b> mira que el aro de caucho del filtro nuevo no esté pellizcado o torcido.</li>'
               '<li><b>En filtros externos:</b> revisa que los racores estén bien metidos en la manguera y que la flecha apunte en el sentido del agua.</li></ol>',
               [("¿Un filtro que gotea daña el piso?", "Puede hacerlo si no se corrige. Cierra la llave del agua mientras lo revisas."),
                ("¿Es normal que salgan unas gotas al sacar el filtro?", "Sí, caen unas gotas de agua retenida. Ten un trapo a la mano."),
                ("¿Cómo evito que gotee en el próximo cambio?", "Compra la referencia exacta y verifica que quede firme antes de abrir el agua.")],
               "El filtro gotea")
        pagina(f"{b}agua-con-mal-sabor-nevera-{s}/", f"Agua con mal sabor o mal olor en la nevera {marca}: causas y solución",
               f"El agua o el hielo de tu nevera {marca} saben a cloro, a tierra o a encerrado. Las causas más comunes y cómo corregirlas.",
               f"Agua con mal sabor en la nevera {marca}",
               "El filtro vencido es la causa número uno, pero conviene descartar las demás en orden.",
               '<ol><li><b>Filtro vencido:</b> pasados unos 6 meses el carbón ya no retiene cloro ni olores. Cámbialo.</li><li><b>Filtro nuevo sin purgar:</b> bota los primeros 6 litros.</li>'
               '<li><b>Agua quieta en la manguera:</b> si el dispensador se usa poco, bota un par de vasos antes de servir.</li><li><b>Hielo viejo:</b> bota el hielo de la cubeta y deja que se haga hielo nuevo.</li>'
               '<li><b>Alimentos destapados:</b> el hielo absorbe olores; tapa la comida.</li></ol>',
               [("¿El mal sabor es peligroso?", "Un filtro vencido deja de retener el cloro y el sedimento; no conviene seguir tomando esa agua sin cambiarlo."),
                ("¿Cuánto dura el mal sabor con un filtro nuevo?", "Debe desaparecer después de botar los primeros litros."),
                ("¿Y si el agua de la llave ya sabe mal?", "El filtro se satura más rápido; cámbialo antes de los 6 meses o agrega un filtro externo.")],
               "Mal sabor", foto="agua")

        # páginas por ciudad
        for c in top_ciudades:
            ciudad, depto = c[0], c[1]
            ruta = f"{b}{slug(ciudad)}/"
            pagina(ruta, f"Filtro de agua para nevera {marca} en {ciudad} | Envío gratis",
                   f"Filtros de agua para nevera {marca} en {ciudad}, {depto}: {len(ps)} referencias, envío gratis y pago seguro en línea. Te decimos cuál le sirve a tu nevecón.",
                   f"Filtro de agua para nevera {marca} en {ciudad}",
                   f"Enviamos el filtro de tu nevera o nevecón <b>{esc(marca)}</b> a {esc(ciudad)} ({esc(depto)}), con <b>envío gratis</b>. Llega en 2 a 3 días hábiles a las principales ciudades.",
                   "<h2>Filtros " + esc(marca) + " disponibles en " + esc(ciudad) + "</h2>" + tabla
                   + f'<p class="m">Mira también el <a href="{rutas_ciudad[ciudad]}">envío a {esc(ciudad)}</a> con todas las marcas.</p>',
                   [(f"¿Envían filtros {marca} a {ciudad}?", f"Sí, con envío gratis. El pago es en línea y te llega el número de guía."),
                    (f"¿Cómo sé cuál filtro le sirve a mi nevera {marca} en {ciudad}?", "Con el modelo o la referencia del filtro viejo te confirmamos cuál es; lo puedes buscar en el directorio de referencias."),
                    ("¿Se instala fácil?", "Sí. Cada filtro trae su paso a paso y se cambia sin herramientas.")],
                   f"{ciudad}", foto="agua")
    return salida


def guias(CATALOGO, MARCAS, slug, ubic):
    """Guías generales con términos de búsqueda. Devuelve [(slug, titulo, descripcion, cuerpo_html)]."""
    marcas = list(MARCAS)
    links_marca = " · ".join(f'<a href="/marca/{slug(m)}/">Filtros {esc(m)}</a>' for m in marcas)
    precios = [p["precio"] for p in CATALOGO]
    rango = f"{cop(min(precios))} a {cop(max(precios))}"
    por_marca = {m: [p for p in CATALOGO if p["marca"] == m] for m in marcas}
    top = "".join(f'<a href="/marca/{slug(m)}/precio-filtro-nevera-{slug(m)}/">Precio filtro nevera {esc(m)}</a> · ' for m in marcas)[:-3]
    comun = f'<p class="m">Filtros por marca: {links_marca}. <a href="/tienda/">Ver toda la tienda</a> · <a href="/referencias/">Buscar por referencia</a> · <a href="/neveras/">Buscar por modelo</a>.</p>'
    G = []

    def g(sl, titulo, desc, cuerpo):
        G.append((sl, titulo, desc, cuerpo + comun))

    g("como-escoger-el-filtro-de-agua-para-la-nevera", "Cómo escoger el filtro de agua para la nevera o el nevecón",
      "Guía para escoger el filtro de agua de tu nevera: por marca, por modelo, interno o externo, y qué revisar antes de comprar.",
      "<p>Escoger el filtro correcto es más fácil de lo que parece si sigues este orden. Lo importante es que la referencia coincida con la de tu nevera: no sirve «parecido».</p>"
      "<h2>1. Identifica la marca y el modelo</h2><p>Abre el refrigerador y busca la etiqueta con el modelo (pared lateral, techo o detrás del cajón de las verduras). Con la marca y el modelo ya sabes por dónde empezar.</p>"
      "<h2>2. Mira la referencia del filtro viejo</h2><p>El filtro trae impresa su referencia, por ejemplo <span class=\"ref\">DA29-00020B</span>, <span class=\"ref\">LT1000P</span>, <span class=\"ref\">EDR1RXD1</span> o <span class=\"ref\">MWF</span>. Busca esa referencia en el <a href=\"/referencias/\">directorio</a>: muchas tienen equivalencias con otro nombre.</p>"
      "<h2>3. Decide si es interno o externo</h2><p>El interno va dentro del refrigerador; el externo, en la manguera de atrás. Si tu nevera ya trae uno, compra el mismo tipo. Más en <a href=\"/guia/filtro-interno-o-externo/\">interno o externo</a>.</p>"
      "<h2>4. Compra con envío y empaque sellado</h2><p>Revisa que la caja venga sellada, con la referencia y el código de barras, y que el envío esté incluido. Con el pack de 2 tienes el año completo.</p>")
    g("diferencia-entre-nevera-nevecon-y-refrigerador", "Nevera, nevecón o refrigerador: ¿cambia el filtro?",
      "Nevera, nevecón, refrigerador y frigorífico son el mismo electrodoméstico. Qué filtro de agua usa según la marca y el modelo.",
      "<p>En Colombia se le dice <b>nevera</b>, <b>nevecón</b> (la nevera grande, de dos puertas o French door), <b>refrigerador</b> o, en otros países, <b>frigorífico</b> o <b>heladera</b>. Para el filtro de agua no cambia nada: lo que decide cuál sirve es la <b>marca</b> y el <b>modelo</b>.</p>"
      "<h2>¿Qué neveras tienen filtro de agua?</h2><p>Las que traen dispensador de agua en la puerta o máquina de hielo: Samsung, LG, Whirlpool, GE, KitchenAid, Maytag y más marcas de dos puertas, side by side y French door. Una nevera sencilla sin dispensador normalmente no usa filtro.</p>"
      "<h2>Cómo saber cuál es el mío</h2><p>Busca la referencia en el filtro viejo o el modelo en la etiqueta interna. Mira la guía <a href=\"/guia/como-saber-que-filtro-usa-mi-nevecon/\">cómo saber qué filtro usa mi nevecón</a>.</p>")
    g("mejor-filtro-de-agua-para-nevera", "¿Cuál es el mejor filtro de agua para la nevera?",
      "El mejor filtro de agua para tu nevera es el que corresponde a su marca y modelo. Cómo escogerlo, cada cuánto cambiarlo y qué evitar.",
      "<p>No existe un «mejor filtro» para todas las neveras: el mejor es el que <b>encaja exacto</b> en tu modelo, está sellado de fábrica y se cambia a tiempo. Un filtro que no corresponde puede gotear o no abrir bien la válvula.</p>"
      "<h2>Qué mirar</h2><ul class=\"ok\"><li><b>Referencia exacta</b> de tu nevera o una equivalencia confirmada.</li><li><b>Caja sellada</b> con referencia y código de barras.</li><li><b>Cambio cada 6 meses</b> para mantener el filtrado.</li><li><b>Envío y pago seguro</b>, con quién te asesore si dudas.</li></ul>"
      "<h2>Qué evitar</h2><p>Precios demasiado bajos, cajas sin sellar o sin referencia, y filtros «universales» que no traen la conexión de tu modelo.</p>")
    g("precio-de-los-filtros-de-agua-para-nevera-en-colombia", f"Precio de los filtros de agua para nevera en Colombia ({ANIO})",
      f"Cuánto cuesta un filtro de agua para nevera en Colombia en {ANIO}: precios por marca (Samsung, LG, Whirlpool, GE), con envío incluido.",
      f"<p>Un filtro de agua para nevera cuesta entre <b>{rango}</b> según la marca y el tipo, con el envío incluido. Los externos de manguera y algunos internos de mayor capacidad están en la parte alta del rango.</p>"
      "<h2>Precios por marca</h2><ul class=\"ok\">"
      + "".join(f'<li><a href="/marca/{slug(m)}/precio-filtro-nevera-{slug(m)}/">Filtro nevera {esc(m)}</a>: de {cop(min(p["precio"] for p in ps))} a {cop(max(p["precio"] for p in ps))}.</li>' for m, ps in por_marca.items())
      + "</ul><h2>¿Se puede ahorrar?</h2><p>Sí: el pack anual de 2 filtros sale más barato por unidad y te cubre los 12 meses.</p>")
    g("donde-comprar-filtros-de-agua-para-nevera-en-colombia", "Dónde comprar filtros de agua para nevera en Colombia",
      "Dónde comprar filtros de agua para nevera Samsung, LG, Whirlpool, GE, KitchenAid, Maytag y más marcas en Colombia con envío gratis y pago seguro.",
      "<p>Puedes comprar el filtro de tu nevera en línea y recibirlo en tu casa en cualquier ciudad de Colombia. Aquí enviamos con <b>envío gratis</b> a las principales ciudades y municipios.</p>"
      "<h2>Qué ofrecemos</h2><ul class=\"ok\"><li>Filtros para neveras Samsung, LG, Whirlpool, GE, KitchenAid, Maytag y más marcas.</li><li>Asesoría para encontrar la referencia por modelo.</li><li>Pago con tarjeta, PSE, Nequi o botón Bancolombia.</li><li>Número de guía para seguir el paquete.</li></ul>"
      "<p>Mira las <a href=\"/envios/\">ciudades a las que enviamos</a> y escoge tu marca abajo.</p>")
    g("filtro-de-nevera-con-dispensador-de-agua-y-hielo", "Filtro para nevera con dispensador de agua y máquina de hielo",
      "Qué filtro usa una nevera con dispensador de agua y máquina de hielo, cómo se cambia y cada cuánto, según la marca.",
      "<p>Las neveras con dispensador de agua y máquina de hielo usan el mismo filtro para las dos cosas: el agua que sirves y el hielo que se hace pasan por él. Por eso un filtro vencido se nota en el sabor del agua y también del hielo.</p>"
      "<h2>Señales de que toca cambiarlo</h2><ul class=\"ok\"><li>Agua o hielo con sabor a cloro, tierra o encerrado.</li><li>Hielo turbio, pequeño o con mal olor.</li><li>El dispensador bota menos agua.</li><li>La luz del filtro en el panel.</li></ul>"
      "<p>Más detalles en <a href=\"/guia/cada-cuanto-cambiar-el-filtro-del-nevecon/\">cada cuánto se cambia</a> y <a href=\"/guia/como-cambiar-el-filtro-de-agua-del-nevecon/\">cómo cambiarlo</a>.</p>")
    g("cuantos-litros-filtra-un-filtro-de-nevera", "¿Cuántos litros filtra un filtro de nevera y cuánto dura?",
      "Cuánto dura un filtro de agua de nevera: la regla de los 6 meses, qué pasa si lo usas más tiempo y cómo saber si ya se saturó.",
      "<p>Los fabricantes calculan la vida del filtro por <b>tiempo</b> (unos 6 meses) y por <b>cantidad de agua</b>, y casi siempre se cumple primero el tiempo. Por eso la regla práctica es cambiarlo cada 6 meses, o antes si el agua cambia de sabor.</p>"
      "<h2>De qué depende</h2><ul class=\"ok\"><li>Cuánta gente vive en la casa y cuánto hielo se usa.</li><li>La calidad del agua de tu ciudad (con sedimento se satura antes).</li><li>La referencia del filtro.</li></ul>"
      "<p>Si pasaron los 6 meses, cámbialo aunque se vea bien: el carbón activado ya está saturado.</p>")
    g("se-puede-usar-la-nevera-sin-filtro-de-agua", "¿Se puede usar la nevera sin filtro de agua?",
      "Qué pasa si usas la nevera sin filtro de agua, cuándo sirve un tapón de derivación y por qué conviene cambiarlo.",
      "<p>Algunas neveras traen un <b>tapón de derivación</b> (bypass) para funcionar sin filtro, y la nevera funciona. Pero el agua y el hielo salen <b>sin filtrar</b>: con el cloro y el sedimento de la red, y la máquina de hielo trabaja con esa agua.</p>"
      "<h2>Por qué conviene tener filtro</h2><ul class=\"ok\"><li>Mejor sabor y olor del agua y del hielo.</li><li>Protege la válvula y la máquina de hielo del sedimento.</li><li>Evita que se prenda la luz de aviso.</li></ul>"
      "<p>Si se te venció, no esperes: busca tu referencia y cámbialo. Mira la <a href=\"/guia/cada-cuanto-cambiar-el-filtro-del-nevecon/\">guía de cambio</a>.</p>")
    g("como-saber-si-el-filtro-de-la-nevera-esta-vencido", "Cómo saber si el filtro de la nevera ya está vencido",
      "Señales claras de que el filtro de agua de tu nevera está vencido o saturado y qué hacer.",
      "<p>El filtro avisa de varias formas. Si notas una sola de estas señales, ya toca cambiarlo:</p>"
      "<ul class=\"ok\"><li><b>Sabor u olor:</b> el agua o el hielo saben a cloro, a tierra o a encerrado.</li><li><b>Menos caudal:</b> el vaso tarda más en llenarse.</li><li><b>Hielo diferente:</b> más pequeño, turbio o con mal olor.</li><li><b>La luz del panel:</b> «Replace Filter», «Order» o similar.</li><li><b>Más de 6 meses</b> desde el último cambio.</li></ul>"
      "<p>Cambiarlo toma unos minutos: <a href=\"/guia/como-cambiar-el-filtro-de-agua-del-nevecon/\">paso a paso</a>.</p>")
    g("agua-turbia-o-con-burbujas-en-la-nevera", "Agua turbia o con burbujas en la nevera: causas",
      "Por qué el agua de la nevera sale turbia, blanca o con burbujas y cuándo es normal.",
      "<p>Si el agua sale <b>lechosa o con burbujas</b> justo después de cambiar el filtro, es normal: es aire atrapado en la línea. Se corrige botando unos 6 litros en tandas.</p>"
      "<h2>Si sigue turbia</h2><ul class=\"ok\"><li>Filtro mal puesto que deja pasar aire: sácalo y vuelve a instalarlo hasta el fondo.</li><li>Filtro saturado: el sedimento ya pasa; cámbialo.</li><li>Agua de la red con sedimento: puede tocar cambiarlo antes de los 6 meses.</li></ul>")
    g("nevera-no-hace-hielo-revisar-el-filtro", "La nevera no hace hielo o hace poco: revisa el filtro",
      "Si tu nevera hace poco hielo o no hace, el filtro de agua tapado es una de las causas más comunes. Qué revisar.",
      "<p>La máquina de hielo recibe el agua que pasa por el filtro. Si el filtro está tapado, llega poca agua y salen cubos pequeños, huecos o ninguno.</p>"
      "<h2>Revisa en este orden</h2><ol><li>¿Pasaron más de 6 meses? Cambia el filtro.</li><li>¿El dispensador echa agua con buen chorro? Si no, es el filtro o la presión.</li><li>¿La máquina está encendida? Muchos paneles tienen la opción «Ice Off».</li><li>¿El congelador está lo bastante frío?</li></ol>"
      "<p>Si el agua no sale, mira <a href=\"/guia/el-dispensador-de-agua-del-nevecon-no-echa-agua/\">el dispensador no echa agua</a>.</p>")
    g("como-comprar-un-filtro-de-nevera-por-internet-sin-equivocarte", "Cómo comprar un filtro de nevera por internet sin equivocarte",
      "Checklist para comprar el filtro de tu nevera en línea: modelo, referencia, tipo, envío y empaque.",
      "<ol><li><b>Anota el modelo</b> de la nevera (etiqueta interna).</li><li><b>Fotografía el filtro viejo</b> y su referencia.</li><li><b>Busca la referencia</b> en el <a href=\"/referencias/\">directorio</a> o tu modelo en el de <a href=\"/neveras/\">neveras</a>.</li>"
      "<li><b>Escoge interno o externo</b> igual que el que ya tienes.</li><li><b>Confirma el envío incluido</b> y el tiempo de entrega a tu ciudad.</li><li><b>Paga en una página segura</b> y guarda el recibo.</li></ol>"
      "<p>Si tienes dudas, escríbenos con el modelo y te confirmamos antes de comprar.</p>")
    return G


CSS_HOME = """
.seo-home{max-width:1100px;margin:40px auto 0;padding:0 max(16px,env(safe-area-inset-left,0px));display:flex;flex-direction:column;gap:34px;color:var(--ink)}
.seo-home h2{font-size:clamp(22px,3vw,28px);margin:0 0 10px;letter-spacing:-.01em;text-wrap:balance}.seo-home h3{font-size:17px;margin:0 0 6px}
.seo-home p{color:var(--muted);line-height:1.65;margin:0 0 10px;max-width:75ch}.seo-home p a,.seo-home .sh-card h3 a{color:var(--brand,#0f7a6d);font-weight:700}
.seo-home .sh-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}
.seo-home .sh-card{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:18px;min-width:0}
.seo-home .sh-card a{color:var(--ink)}.seo-home .sh-chips{display:flex;flex-wrap:wrap;gap:8px}
.seo-home .sh-chips a{background:var(--panel);border:1px solid var(--line);border-radius:999px;padding:8px 14px;font-size:14px;font-weight:600;color:var(--ink);text-decoration:none}
.seo-home .sh-chips a:hover{border-color:var(--brand,#0f7a6d)}
.seo-home details{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:0 18px}.seo-home details+details{margin-top:8px}
.seo-home summary{cursor:pointer;padding:15px 0;font-weight:700}.seo-home details p{padding-bottom:6px}
"""


def home_bloque(CATALOGO, MARCAS, slug, ubic, CIUDADES_CO):
    """Texto de portada con términos de búsqueda + enlaces a los temas. Devuelve (html, [(pregunta, respuesta)])."""
    precios = [p["precio"] for p in CATALOGO]
    rango = f"{cop(min(precios))} a {cop(max(precios))}"
    tarjetas = ""
    for m in MARCAS:
        info = marcas_exclusivas.MARCAS_INFO[m]
        ps = [p for p in CATALOGO if p["marca"] == m]
        sl = slug(m)
        tarjetas += (f'<div class="sh-card"><h3><a href="/marca/{sl}/">Filtros de agua para nevera {esc(m)}</a></h3>'
                     f'<p>{esc(info["intro"])}</p><p><a href="/marca/{sl}/precio-filtro-nevera-{sl}/">Precio</a> · <a href="/marca/{sl}/luz-filtro-nevera-{sl}/">Luz del filtro</a> · '
                     f'<a href="/marca/{sl}/como-cambiar-filtro-nevera-{sl}/">Cómo cambiarlo</a> · <a href="/marca/{sl}/donde-comprar-filtro-nevera-{sl}/">Dónde comprar</a></p></div>')
    busquedas = [("/guia/cada-cuanto-cambiar-el-filtro-del-nevecon/", "Cada cuánto se cambia el filtro"), ("/guia/como-cambiar-el-filtro-de-agua-del-nevecon/", "Cómo cambiar el filtro de agua"),
                 ("/guia/como-reiniciar-la-luz-del-filtro-del-nevecon/", "Cómo apagar la luz del filtro"), ("/guia/como-saber-que-filtro-usa-mi-nevecon/", "Qué filtro usa mi nevecón"),
                 ("/guia/por-que-el-agua-del-nevecon-sabe-mal/", "Agua con mal sabor"), ("/guia/el-dispensador-de-agua-del-nevecon-no-echa-agua/", "El dispensador no echa agua"),
                 ("/guia/el-hielo-del-nevecon-sale-turbio-o-con-mal-sabor/", "Hielo turbio o con mal sabor"), ("/guia/filtro-interno-o-externo/", "Filtro interno o externo"),
                 ("/guia/precio-de-los-filtros-de-agua-para-nevera-en-colombia/", "Precio de los filtros"), ("/guia/mejor-filtro-de-agua-para-nevera/", "Mejor filtro de agua para nevera"),
                 ("/guia/diferencia-entre-nevera-nevecon-y-refrigerador/", "Nevera, nevecón o refrigerador"), ("/guia/se-puede-usar-la-nevera-sin-filtro-de-agua/", "Nevera sin filtro de agua"),
                 ("/guia/nevera-no-hace-hielo-revisar-el-filtro/", "La nevera no hace hielo"),
                 ("/otras-marcas/filtro-para-nevera-kitchenaid/", "Filtro para nevera KitchenAid"), ("/otras-marcas/filtro-para-nevera-maytag/", "Filtro para nevera Maytag (MyTag)"),
                 ("/otras-marcas/filtro-para-nevera-jenn-air/", "Filtro para nevera Jenn-Air"), ("/otras-marcas/filtro-para-nevera-amana/", "Filtro para nevera Amana"),
                 ("/otras-marcas/filtro-para-nevera-kenmore/", "Filtro para nevera Kenmore"), ("/otras-marcas/", "Filtros por marca de nevera"),
                 ("/otras-marcas/preguntas-frecuentes/", "Preguntas frecuentes"), ("/otras-marcas/blog/", "Blog de filtros de nevera"), ("/referencias/", "Buscar por referencia"), ("/neveras/", "Buscar por modelo"), ("/instalacion/", "Instalación por referencia")]
    ciudades = "".join(f'<a href="/envios/{slug(c[1])}/{slug(c[0])}/">Filtros de nevera en {esc(c[0])}</a>' for c in CIUDADES_CO[:16])
    faq = [("¿Qué filtro de agua usa mi nevera o nevecón?", "Depende de la marca y del modelo. Busca la referencia impresa en el filtro viejo (por ejemplo DA29-00020B, LT1000P, EDR1RXD1 o MWF) o el modelo en la etiqueta interna de la nevera, y búscalo en esta tienda."),
           ("¿Cada cuánto se cambia el filtro de agua de la nevera?", "Cada 6 meses, o antes si el agua o el hielo cambian de sabor, el dispensador bota menos agua o se prende la luz del filtro."),
           ("¿Cuánto cuesta un filtro de agua para nevera en Colombia?", f"Entre {rango}, con el envío incluido, según la marca y el tipo. El pack de 2 filtros sale más barato por unidad."),
           ("¿Hacen envíos a toda Colombia?", "Sí. El envío es gratis a toda Colombia y llega en 2 a 3 días hábiles a las principales ciudades, con número de guía."),
           ("¿Cómo instalo el filtro? ¿Necesito un técnico?", "No. Los internos se cambian en un par de minutos y los externos en 10 a 15, sin herramientas. Cada filtro trae su paso a paso."),
           ("¿Sirve el mismo filtro para nevera, nevecón y refrigerador?", "Sí: son el mismo electrodoméstico con distinto nombre. Lo que decide cuál filtro sirve es la marca y el modelo."),
           ("¿Cómo pago?", "En línea, en una página segura: tarjeta débito o crédito, PSE, Nequi o botón Bancolombia.")]
    h = f"""<section class="seo-home" id="info">
<div><h2>Filtros de agua para nevera y nevecón en Colombia</h2>
<p>Aquí encuentras el <b>filtro de agua de tu nevera, nevecón o refrigerador</b> Samsung, LG, Whirlpool, GE, KitchenAid, Maytag y más marcas, con <b>envío gratis</b> a toda Colombia y pago seguro en línea. Tenemos {len(CATALOGO)} referencias entre {rango}: filtros internos que van dentro del refrigerador y filtros externos de manguera.</p>
<p>Si no sabes cuál es el tuyo, búscalo por la <a href="/referencias/">referencia del filtro viejo</a> o por el <a href="/neveras/">modelo de tu nevera</a>. Te ayudamos a confirmarlo antes de comprar.</p></div>
<div><h2>Filtros por marca de nevera</h2><div class="sh-grid">{tarjetas}</div></div>
<div><h2>Cuándo cambiar el filtro y cómo queda el agua</h2><div class="foto-par">{figura("alerta")}{figura("agua")}</div><p>Cuando el nevecón muestra la alerta del filtro, ya pasaron unos 6 meses de uso: cámbialo y reinicia el aviso. Con el filtro nuevo, el agua y el hielo salen limpios otra vez.</p></div>
<div><h2>Lo que más buscan sobre filtros de nevera</h2><div class="sh-chips">{"".join(f'<a href="{r}">{esc(t)}</a>' for r, t in busquedas)}</div></div>
<div><h2>Preguntas frecuentes sobre filtros de agua para nevera</h2>{"".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faq)}</div>
<div><h2>Enviamos filtros para nevera a toda Colombia</h2><div class="sh-chips">{ciudades}<a href="/envios/">Ver todas las ciudades</a></div></div>
</section>"""
    return h, faq
