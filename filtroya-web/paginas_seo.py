"""Páginas extra para Google: una por cada referencia equivalente, una por cada modelo de nevecón,
guías, la página de Cali y los directorios. Las usa build.py.

Cada página trae información propia (equivalencias, cómo confirmar, cómo cambiarlo, modelos),
no solo el nombre cambiado: así Google la toma como útil y no como una copia.
"""
import html
import json

esc = lambda s: html.escape(str(s), quote=True)
cop = lambda n: "$ " + f"{n:,}".replace(",", ".")


def miga(*items):
    """Ruta de navegación visible + datos para Google. items: (nombre, ruta) o (nombre, None) para la actual."""
    html_ = '<nav class="miga">' + " › ".join(f'<a href="{r}">{esc(n)}</a>' if r else esc(n) for n, r in items) + "</nav>"
    ld = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, **({"item": f"__BASE__{r}"} if r else {})} for i, (n, r) in enumerate(items)]}
    return html_, ld


def faq_ld(preguntas):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in preguntas]}


def faq_html(preguntas):
    return ('<section style="display:flex;flex-direction:column;gap:8px"><h2>Preguntas frecuentes</h2>'
            + "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in preguntas) + "</section>")


def caja_producto(p, titulo=None):
    return f"""<div class="prod">
  <a class="foto" href="/filtro/{p["slug"]}/"><picture><source srcset="/img/{p["id"]}.webp" type="image/webp"><img src="/img/{p["id"]}.jpg" alt="{esc(p["nombre_largo"])} para nevecón {esc(p["marca"])}" width="600" height="600" fetchpriority="high"></picture></a>
  <div class="caja">
    <span class="m">{esc(titulo or "El filtro que necesitas")}</span>
    <h2 style="margin:0">{esc(p["nombre_largo"])}</h2>
    <span class="precio">{cop(p["precio"])}</span>
    <ul class="ok"><li><b>Envío gratis</b> a toda Colombia: llega en 2 días hábiles.</li><li>En Cali: <b>domicilio e instalación gratis</b>.</li><li>Garantía de 30 días: si no encaja, te lo cambiamos.</li></ul>
    <div class="compra"><button class="btn block" type="button" data-add="{p["id"]}">Agregar al carrito</button><button class="btn ghost block" type="button" data-add="{p["id"]}" data-ir="1">Comprar ahora</button><a class="link" href="/filtro/{p["slug"]}/">Ver todos los detalles del filtro</a></div>
  </div>
</div>"""


def pasos_cambio(p, ubic):
    if ubic(p) == "externo":
        pasos = ["Cierra la llave de paso del agua que alimenta el nevecón.",
                 "Suelta la manguera de los dos extremos del filtro viejo: presiona el anillo del racor rápido y hala.",
                 "Conecta el filtro nuevo respetando la flecha que indica la dirección del agua.",
                 "Abre la llave y revisa que no gotee por ningún lado.",
                 "Saca 2 o 3 litros de agua por el dispensador para sacar el aire y el carbón suelto."]
    else:
        pasos = ["Ubica la tapa del filtro dentro del nevecón (arriba, a un lado o en la rejilla de abajo, según el modelo).",
                 "Saca el filtro viejo: según el modelo se gira un cuarto de vuelta a la izquierda o se suelta con el botón. Ten un trapo a la mano, puede salir un poco de agua.",
                 "Quítale la tapa protectora al filtro nuevo y mételo hasta que quede firme (girando a la derecha si es de rosca).",
                 "Saca 2 o 3 litros de agua por el dispensador para sacar el aire y el carbón suelto.",
                 "Reinicia el aviso del filtro: en la mayoría de modelos se deja presionado el botón «Filter» o «Reset» unos 3 segundos."]
    return "<ol>" + "".join(f"<li>{esc(x)}</li>" for x in pasos) + "</ol>"


def generar(OUT, CATALOGO, MARCAS, slug, norm, ubic, cabeza_php, tarjeta):
    paginas = []

    def escribir(ruta, titulo, desc, ld_items, cuerpo):
        ld = {"@context": "https://schema.org", "@graph": ld_items}
        d = OUT / ruta.strip("/")
        d.mkdir(parents=True, exist_ok=True)
        partes = "/" + "../" * len(ruta.strip("/").split("/")) + "partes.php"
        (d / "index.php").write_text(cabeza_php(partes, titulo, desc, ruta, ld) + "\n" + cuerpo + "\n<?php pie(); ?>\n", encoding="utf-8")
        paginas.append(ruta)

    # ---------- referencias equivalentes ----------
    principales = {norm(p["ref"]) for p in CATALOGO}
    vistas = set()
    refs_dir = []  # (referencia, ruta, producto)
    for p in CATALOGO:
        refs_dir.append((p["ref"], f'/filtro/{p["slug"]}/', p))
        donde = "va en la manguera de agua, por fuera del nevecón" if ubic(p) == "externo" else "va por dentro del nevecón"
        for r in p["refs"]:
            n = norm(r)
            if n == norm(p["ref"]) or n in principales or n in vistas:
                continue
            vistas.add(n)
            ruta = f"/referencia/{slug(r)}/"
            refs_dir.append((r, ruta, p))
            otras = [x for x in p["refs"] if norm(x) != n]
            titulo = f"Filtro {r} para nevecón {p['marca']} | Equivale a {p['ref']}"
            desc = (f"¿Buscas el filtro {r}? Es la misma referencia que el {p['nombre_largo']}: {cop(p['precio'])} con envío gratis a toda Colombia. "
                    f"En Cali te lo instalamos gratis.")
            preguntas = [
                (f"¿El filtro {r} es igual al {p['ref']}?", f"Sí. {r} y {p['ref']} son nombres de la misma referencia de filtro para nevecón {p['marca']}: tienen la misma forma, la misma conexión y se cambian igual."),
                (f"¿Cada cuánto se cambia el filtro {r}?", "Cada 6 meses, o antes si el agua cambia de sabor, de olor o sale con poca presión."),
                (f"¿Cuánto cuesta el envío del {r}?", "Nada. El envío es gratis a toda Colombia y llega en unos 2 días hábiles después del pago. En Cali también lo instalamos gratis."),
            ]
            mg, mg_ld = miga(("Inicio", "/"), ("Referencias", "/referencias/"), (f"Filtro {r}", None))
            modelos = "".join(f'<a href="/nevecon/{slug(m)}/">{esc(m)}</a>' for m in p["modelos"])
            cuerpo = f"""{mg}
<h1>Filtro {esc(r)} para nevecón {esc(p["marca"])}</h1>
<p>El filtro <b>{esc(r)}</b> es la misma referencia que el <b>{esc(p["nombre_largo"])}</b>: {donde}. Lo tenemos a <b>{cop(p["precio"])}</b> con envío gratis a toda Colombia, y en Cali te lo instalamos gratis.</p>
{caja_producto(p, f"Para el {r} te sirve")}
<section class="caja">
  <h2>Equivalencias del filtro {esc(r)}</h2>
  <p>Estas referencias son el mismo filtro. Si tu filtro viejo trae cualquiera de ellas impresa, este es el tuyo:</p>
  <table class="t"><tr><th>Referencia</th><th>Marca</th><th>Tipo</th></tr>
  {"".join(f'<tr><td><span class="ref">{esc(x)}</span></td><td>{esc(p["marca"])}</td><td>{"Externo" if ubic(p) == "externo" else "Interno"}</td></tr>' for x in [p["ref"]] + otras)}
  </table>
</section>
<section class="caja">
  <h2>Cómo confirmar que es tu filtro</h2>
  <ol><li>Saca el filtro viejo y busca la referencia impresa en la etiqueta: tiene que decir <span class="ref">{esc(r)}</span> o alguna de las equivalencias de arriba.</li>
  <li>Si no se lee, mira el modelo del nevecón en la etiqueta de adentro (en una pared lateral o en el techo del refrigerador).</li>
  <li>{f"Compara el modelo con estos nevecones que usan este filtro: {modelos}." if modelos else "Si tienes dudas, escríbenos al correo con la foto del filtro viejo o de la etiqueta y te confirmamos antes de comprar."}</li></ol>
</section>
<section class="caja"><h2>Cómo se cambia</h2>{pasos_cambio(p, ubic)}<p class="m">Más detalles en la guía <a href="/guia/como-cambiar-el-filtro-de-agua-del-nevecon/">cómo cambiar el filtro de agua del nevecón</a>.</p></section>
{faq_html(preguntas)}"""
            escribir(ruta, titulo, desc, [mg_ld, faq_ld(preguntas)], cuerpo)

    # ---------- modelos de nevecón ----------
    modelos_dir = []  # (marca, modelo, ruta, producto)
    hechos = set()
    for p in CATALOGO:
        for m in p["modelos"]:
            if norm(m) in hechos:
                continue
            hechos.add(norm(m))
            ruta = f"/nevecon/{slug(m)}/"
            modelos_dir.append((p["marca"], m, ruta, p))
            hermanos = [x for x in p["modelos"] if x != m]
            titulo = f"Filtro de agua para nevecón {p['marca']} {m} | {p['ref']}"
            desc = (f"El nevecón {p['marca']} {m} usa el filtro {p['nombre_largo']}. Cómprelo a {cop(p['precio'])} con envío gratis a toda Colombia "
                    f"e instalación gratis en Cali.").replace("Cómprelo", "Cómpralo")
            preguntas = [
                (f"¿Qué filtro usa el nevecón {p['marca']} {m}?", f"El {p['nombre_largo']} (referencia {p['ref']}). También aparece como {', '.join([x for x in p['refs'] if norm(x) != norm(p['ref'])][:4]) or p['ref']}."),
                (f"¿Cada cuánto se cambia el filtro del {m}?", "Cada 6 meses, o antes si el agua cambia de sabor, de olor, o el hielo sale turbio o con mal sabor."),
                (f"¿Me lo instalan?", "En Cali sí, gratis. En el resto del país te lo enviamos gratis y se instala en minutos, sin herramientas."),
            ]
            mg, mg_ld = miga(("Inicio", "/"), ("Neveras", "/neveras/"), (f"Nevecón {p['marca']} {m}", None))
            cuerpo = f"""{mg}
<h1>Filtro de agua para nevecón {esc(p["marca"])} {esc(m)}</h1>
<p>El nevecón <b>{esc(p["marca"])} {esc(m)}</b> usa el filtro <b>{esc(p["nombre_largo"])}</b>. Lo tenemos a {cop(p["precio"])} con envío gratis a toda Colombia y, en Cali, instalación gratis.</p>
{caja_producto(p, f"Para el {m} te sirve")}
<section class="caja">
  <h2>Antes de comprar, confirma tu modelo</h2>
  <p>El modelo está en la etiqueta de adentro del refrigerador (en una pared lateral o en el techo). Tiene que decir <span class="ref">{esc(m)}</span>; a veces trae letras o números de más al final, y es el mismo nevecón.</p>
  <p>El filtro que trae puesto debe decir <span class="ref">{esc(p["ref"])}</span> o una de sus equivalencias: {", ".join(f'<a href="/referencia/{slug(x)}/">{esc(x)}</a>' if norm(x) not in principales else esc(x) for x in p["refs"] if norm(x) != norm(p["ref"])) or "—"}.</p>
</section>
<section class="caja"><h2>Cómo cambiar el filtro del {esc(m)}</h2>{pasos_cambio(p, ubic)}</section>
{f'<section class="caja"><h2>Otros nevecones que usan el mismo filtro</h2><div class="chips">{"".join(f"<a href=\"/nevecon/{slug(x)}/\">{esc(x)}</a>" for x in hermanos)}</div></section>' if hermanos else ""}
{faq_html(preguntas)}"""
            escribir(ruta, titulo, desc, [mg_ld, faq_ld(preguntas)], cuerpo)

    # ---------- guías ----------
    def por_marca(m):
        return [p for p in CATALOGO if p["marca"] == m]

    grid_top = "".join(tarjeta(p) for p in CATALOGO if p["id"] in ("sam-cin-o", "lg-1000-o", "wp-1-o", "ge-mwf-o"))
    GUIAS = [
        ("cada-cuanto-cambiar-el-filtro-del-nevecon", "¿Cada cuánto se cambia el filtro de agua del nevecón?",
         "Cada cuánto cambiar el filtro de agua del nevecón, las señales de que ya está vencido y qué pasa si no lo cambias.",
         f"""<p>La recomendación de los fabricantes de nevecones es cambiar el filtro de agua <b>cada 6 meses</b>. Ese es el tiempo en que el carbón activado del filtro se va llenando con el cloro, el sedimento y las partículas que le saca al agua.</p>
<h2>Señales de que ya toca cambiarlo</h2>
<ul class="ok"><li>El agua o el hielo saben u huelen raro (a cloro, a tierra o a encerrado).</li><li>El dispensador echa el agua más despacio que antes.</li><li>El hielo sale turbio, pequeño o con mal sabor.</li><li>Se prendió la luz o el aviso de «Filter» en el panel.</li></ul>
<h2>¿Qué pasa si no lo cambio?</h2>
<p>Un filtro vencido deja de filtrar y se tapa poco a poco: el agua sale con mal sabor, baja la presión del dispensador y la máquina de hielo trabaja forzada. En casas con mucho consumo o agua con sedimento, puede tocar cambiarlo antes de los 6 meses.</p>
<h2>Un truco para no olvidarlo</h2>
<p>Cuando compras en nuestra tienda puedes pedir que te recordemos por correo cuando se cumplan los 6 meses. También sirve comprar el <b>pack anual de 2 filtros</b>: uno para ahora y otro para dentro de 6 meses, con descuento.</p>
<div class="grid">{grid_top}</div>"""),
        ("como-saber-que-filtro-usa-mi-nevecon", "¿Cómo saber qué filtro usa mi nevecón?",
         "Tres formas fáciles de saber qué filtro de agua usa tu nevecón Samsung, LG, Whirlpool o GE: por la referencia, por el modelo o por la forma.",
         """<p>Hay tres formas de encontrar el filtro exacto de tu nevecón. Con cualquiera de las dos primeras no hay pierde.</p>
<h2>1. Por la referencia del filtro viejo</h2>
<p>Saca el filtro que tiene puesto y busca la etiqueta: trae una referencia como <span class="ref">DA29-00020B</span>, <span class="ref">LT1000P</span>, <span class="ref">EDR1RXD1</span> o <span class="ref">MWF</span>. Escríbela en el <a href="/#catalogo">buscador de la tienda</a> o búscala en el <a href="/referencias/">directorio de referencias</a>. Muchos filtros tienen varios nombres que son el mismo filtro; en cada página te mostramos todas las equivalencias.</p>
<h2>2. Por el modelo del nevecón</h2>
<p>Abre el refrigerador y busca la etiqueta con el modelo: suele estar en una pared lateral o en el techo, cerca del bombillo. Es un código como <span class="ref">RF28HMEDBSR</span> (Samsung) o <span class="ref">LFXS26973S</span> (LG). Búscalo en el <a href="/neveras/">directorio de neveras</a>.</p>
<h2>3. Por la forma y el lugar donde va</h2>
<ul class="ok"><li><b>Interno arriba a la derecha</b>, que se gira: típico de Samsung (HAF-CIN, HAF-QIN), LG (LT1000P, LT700P, LT800P) y GE (MWF, XWF).</li><li><b>Interno en la rejilla de abajo</b>: algunos Whirlpool y LG antiguos (LT500P, LT600P).</li><li><b>Externo, en la manguera</b>: para nevecones con dispensador que no traen filtro adentro.</li></ul>
<p>Si después de esto tienes dudas, escríbenos al correo con la foto del filtro viejo o de la etiqueta y te confirmamos antes de que compres.</p>"""),
        ("como-cambiar-el-filtro-de-agua-del-nevecon", "Cómo cambiar el filtro de agua del nevecón, paso a paso",
         "Paso a paso para cambiar el filtro de agua interno o externo de un nevecón Samsung, LG, Whirlpool o GE, sin herramientas.",
         f"""<p>Cambiar el filtro toma unos 5 minutos y no necesitas herramientas. Ten a la mano un trapo, porque puede salir un poco de agua.</p>
<h2>Filtro interno (dentro del nevecón)</h2>{pasos_cambio(CATALOGO[0], lambda p: "interno")}
<h2>Filtro externo (en la manguera)</h2>{pasos_cambio(CATALOGO[0], lambda p: "externo")}
<h2>Después de cambiarlo</h2>
<p>Las primeras gotas pueden salir con un poco de carbón: es normal, por eso se botan los primeros 2 o 3 litros. Si el dispensador gotea o el agua no sale, revisa que el filtro haya quedado hasta el fondo y bien girado.</p>
<p>En <b>Cali</b> no tienes que hacer nada de esto: al comprar escoges «Domicilio + instalación» y te lo instalamos gratis.</p>
<div class="grid">{grid_top}</div>"""),
        ("filtro-interno-o-externo", "Filtro de nevecón interno o externo: ¿cuál necesito?",
         "Diferencias entre el filtro de agua interno y el externo del nevecón, y cómo saber cuál lleva el tuyo.",
         f"""<p>Los nevecones con dispensador de agua y hielo usan un filtro <b>interno</b> (va dentro del refrigerador) o uno <b>externo</b> (va en la manguera que trae el agua, por detrás del nevecón).</p>
<h2>Filtro interno</h2>
<p>Es el más común en Samsung, LG, Whirlpool y GE. Cada marca y modelo usa una referencia propia, así que hay que comprar exactamente la que corresponde. Ejemplos: <a href="/filtro/{next(p["slug"] for p in CATALOGO if p["id"] == "sam-cin-o")}/">Samsung HAF-CIN</a>, <a href="/filtro/{next(p["slug"] for p in CATALOGO if p["id"] == "lg-1000-o")}/">LG LT1000P</a>, <a href="/filtro/{next(p["slug"] for p in CATALOGO if p["id"] == "ge-mwf-o")}/">GE MWF</a>.</p>
<h2>Filtro externo</h2>
<p>Se usa en nevecones con dispensador que no traen filtro adentro, o para filtrar el agua antes de que entre. Va conectado a la manguera con racores rápidos. Ejemplos: <a href="/filtro/{next(p["slug"] for p in CATALOGO if p["id"] == "sam-ex-o")}/">Samsung externo</a> y <a href="/filtro/{next(p["slug"] for p in CATALOGO if p["id"] == "lg-ex-o")}/">LG externo</a>.</p>
<h2>¿Cuál tiene el mío?</h2>
<p>Abre el refrigerador y busca una tapa o compartimento con la palabra «Filter». Si lo encuentras, es interno. Si no hay ninguno y tu nevecón tiene dispensador, mira la manguera de atrás: si hay un cilindro conectado en la mitad, es externo.</p>"""),
    ]
    def link(pid, texto):
        q = next(p for p in CATALOGO if p["id"] == pid)
        return f'<a href="/filtro/{q["slug"]}/">{esc(texto)}</a>'

    GUIAS += [
        ("por-que-el-agua-del-nevecon-sabe-mal", "¿Por qué el agua del nevecón sabe mal o huele raro?",
         "Las causas más comunes del mal sabor y mal olor del agua del nevecón, explicadas por un técnico, y cómo solucionarlas.",
         f"""<p>Es una de las consultas que más vemos en el taller. En la gran mayoría de casos la solución es sencilla, pero conviene descartar las causas en orden.</p>
<h2>1. El filtro está vencido</h2>
<p>Es la causa número uno. Después de unos 6 meses el carbón activado ya no retiene el cloro ni los olores, y el agua empieza a saber a cloro, a tierra o a encerrado. Si no recuerdas cuándo lo cambiaste, lo más probable es que ya toque. Mira <a href="/guia/cada-cuanto-cambiar-el-filtro-del-nevecon/">cada cuánto cambiarlo</a>.</p>
<h2>2. El filtro es nuevo pero no se purgó</h2>
<p>Un filtro recién puesto suelta aire y polvillo de carbón. Si no se botan los primeros 2 o 3 litros, el agua puede salir turbia o con sabor raro los primeros días.</p>
<h2>3. Agua quieta en la manguera o el tanque</h2>
<p>Si el dispensador se usa poco, el agua se queda quieta en la manguera y el tanque interno y coge sabor. Bota un par de vasos antes de servir y úsalo a diario.</p>
<h2>4. Alimentos destapados</h2>
<p>El hielo y el agua absorben olores de la comida. Tapa los alimentos con olor fuerte (cebolla, pescado, quesos) y limpia el nevecón por dentro.</p>
<h2>5. El agua que llega a la casa</h2>
<p>Si el agua de la llave ya sabe mal, el filtro se satura más rápido. En ese caso conviene cambiarlo antes de los 6 meses o poner también un <a href="/guia/filtro-interno-o-externo/">filtro externo</a> en la manguera.</p>
<p><b>En resumen:</b> si el agua sabe mal, empieza por cambiar el filtro y botar los primeros litros. Busca el tuyo por <a href="/referencias/">referencia</a> o por <a href="/neveras/">modelo de nevecón</a>.</p>"""),
        ("el-dispensador-de-agua-del-nevecon-no-echa-agua", "El dispensador de agua del nevecón no echa agua o sale muy poca",
         "Por qué el dispensador del nevecón no echa agua o sale con poca presión: filtro tapado, mal instalado, manguera congelada y otras causas.",
         """<p>Cuando el dispensador deja de echar agua, o sale un chorrito muy delgado, estas son las causas en el orden en que las revisamos los técnicos:</p>
<h2>1. Filtro tapado o vencido</h2>
<p>Con el tiempo el filtro se llena de sedimento y deja pasar cada vez menos agua. Si el chorro fue bajando poco a poco durante semanas, casi siempre es el filtro.</p>
<h2>2. Filtro mal instalado</h2>
<p>Si el problema empezó justo después de cambiar el filtro, sácalo y vuelve a ponerlo hasta el fondo, girándolo hasta que quede firme. Revisa también que le hayas quitado la tapa protectora.</p>
<h2>3. Aire en la línea</h2>
<p>Después de un cambio de filtro queda aire en la manguera. Presiona el dispensador por tandas de 30 segundos hasta que salga un chorro parejo (2 o 3 litros).</p>
<h2>4. Llave de paso cerrada o con poca presión</h2>
<p>Revisa la llave que alimenta el nevecón (detrás o debajo del lavaplatos) y que la casa tenga buena presión de agua.</p>
<h2>5. Manguera congelada en la puerta</h2>
<p>Si el congelador está muy frío, el agua se puede congelar en la manguera que pasa por la puerta. Sube un poco la temperatura del congelador y espera unas horas.</p>
<p>Si después de revisar todo esto sigue sin echar agua, puede ser la válvula de entrada o el interruptor del dispensador: ahí sí toca un técnico.</p>"""),
        ("el-hielo-del-nevecon-sale-turbio-o-con-mal-sabor", "El hielo del nevecón sale turbio, pequeño o con mal sabor",
         "Causas del hielo turbio, pequeño o con mal sabor en el nevecón y cómo solucionarlo, según un técnico.",
         """<p>La máquina de hielo usa la misma agua del filtro, así que muchos problemas del hielo empiezan ahí.</p>
<h2>Hielo con mal sabor u olor</h2>
<p>Suele ser el filtro vencido o hielo viejo que absorbió olores del congelador. Cambia el filtro, bota todo el hielo de la cubeta y deja que la máquina haga hielo nuevo.</p>
<h2>Hielo pequeño o en cubos huecos</h2>
<p>La máquina no recibe suficiente agua en cada ciclo. La causa más común es un filtro tapado; también puede ser poca presión de agua en la casa o aire en la línea después de cambiar el filtro.</p>
<h2>Hielo turbio o blancuzco</h2>
<p>Un poco de turbidez es normal (es aire atrapado al congelarse rápido). Si además trae partículas o sabor, el filtro ya no está reteniendo el sedimento.</p>
<h2>No hace hielo</h2>
<p>Revisa que la máquina esté encendida (en muchos modelos hay un interruptor o la opción «Ice Off» en el panel) y que el dispensador sí eche agua. Si no echa agua, mira la guía <a href="/guia/el-dispensador-de-agua-del-nevecon-no-echa-agua/">el dispensador no echa agua</a>.</p>"""),
        ("como-reiniciar-la-luz-del-filtro-del-nevecon", "Cómo apagar o reiniciar la luz del filtro del nevecón",
         "Cómo reiniciar el aviso o la luz del filtro de agua en nevecones Samsung, LG, Whirlpool y GE después de cambiar el filtro.",
         """<p>El aviso del filtro no mide el agua: es un contador de tiempo (casi siempre 6 meses). Por eso, después de cambiar el filtro hay que reiniciarlo a mano; si no, la luz sigue prendida aunque el filtro sea nuevo.</p>
<h2>La forma general</h2>
<p>En casi todos los modelos se deja presionado el botón del filtro durante unos <b>3 segundos</b>, hasta que la luz cambie o se apague. El botón puede llamarse «Filter», «Filter Reset», «Reset» o «Water Filter».</p>
<h2>Según la marca</h2>
<ul class="ok"><li><b>Samsung:</b> en muchos modelos se mantiene presionado «Filter Reset» o el botón «Alarm / Hold 3 sec for Filter Reset».</li>
<li><b>LG:</b> en muchos modelos se mantiene presionado «Water Filter» o «Filter Condition Reset».</li>
<li><b>Whirlpool:</b> en muchos modelos se mantiene presionado «Filter» o «Filter Reset».</li>
<li><b>GE:</b> en muchos modelos se mantiene presionado «Reset Water Filter».</li></ul>
<p>Si tu panel tiene bloqueo («Lock» o «Control Lock»), desbloquéalo primero. Los nombres cambian según el modelo; si no lo encuentras, busca en el manual la palabra «filter».</p>
<h2>¿Y si el agua sigue saliendo mal?</h2>
<p>Reiniciar la luz no cambia el filtro. Si el agua sabe mal o sale despacio, mira <a href="/guia/por-que-el-agua-del-nevecon-sabe-mal/">por qué el agua del nevecón sabe mal</a>.</p>"""),
    ]
    for s, titulo, desc, cuerpo_g in GUIAS:
        ruta = f"/guia/{s}/"
        mg, mg_ld = miga(("Inicio", "/"), ("Guías", "/guia/"), (titulo, None))
        art = {"@type": "Article", "headline": titulo, "description": desc, "inLanguage": "es-CO", "datePublished": "2026-10-15", "dateModified": "2026-10-15",
               "author": {"@type": "Organization", "name": "PuroFiltro"}, "mainEntityOfPage": f"__BASE__{ruta}"}
        firma = ('<p class="m">Escrito por <a href="/quienes-somos.php"><?= h(trim((string) (cfg()["tecnico"]["nombre"] ?? "")) ?: cfg()["negocio"]["nombre"]) ?></a>, '
                 'técnico de neveras en Cali · Actualizado el 15 de octubre de 2026</p>')
        escribir(ruta, titulo, desc, [mg_ld, art], f'{mg}\n<article class="legal"><h1>{esc(titulo)}</h1>\n{firma}\n{cuerpo_g}</article>')
    mg, mg_ld = miga(("Inicio", "/"), ("Guías", None))
    escribir("/guia/", "Guías sobre filtros de agua para nevecón", "Guías para escoger, cambiar y cuidar el filtro de agua de tu nevecón.", [mg_ld],
             f'{mg}<h1>Guías sobre filtros de agua para nevecón</h1><div style="display:flex;flex-direction:column;gap:10px">'
             + "".join(f'<a class="caja" href="/guia/{s}/" style="text-decoration:none;color:inherit"><b>{esc(t)}</b><span class="m">{esc(d)}</span></a>' for s, t, d, _ in GUIAS) + "</div>")

    # ---------- tienda: todos los filtros con filtros por marca y tipo ----------
    mg, mg_ld = miga(("Inicio", "/"), ("Tienda", None))
    lista = {"@type": "ItemList", "name": "Filtros de agua para nevecón", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": f"__BASE__/filtro/{p['slug']}/", "name": p["nombre_largo"]} for i, p in enumerate(CATALOGO)]}
    tarjetas = "".join(
        f'<div class="card" data-marca="{esc(p["marca"])}" data-tipo="{ubic(p)}" data-precio="{p["precio"]}">'
        f'<a href="/filtro/{p["slug"]}/" style="text-decoration:none;color:inherit;display:flex;flex-direction:column;gap:6px"><span class="im"><picture><source srcset="/img/{p["id"]}-400.webp" type="image/webp"><img src="/img/{p["id"]}.jpg" alt="{esc(p["nombre_largo"])}" loading="lazy"></picture></span>'
        f'<span class="m">{esc(p["marca"])} · {"Externo" if ubic(p) == "externo" else "Interno"}</span><b>{esc(p["nombre_largo"])}</b><span class="p">{cop(p["precio"])}</span><span class="m">Envío gratis</span></a>'
        f'<button class="btn sm" type="button" data-add="{p["id"]}">Agregar al carrito</button></div>' for p in CATALOGO)
    chips = '<button type="button" data-f="todas" aria-pressed="true">Todas</button>' + "".join(f'<button type="button" data-f="{esc(m)}" aria-pressed="false">{esc(m)}</button>' for m in MARCAS)
    escribir("/tienda/", "Tienda de filtros de agua para nevecón | Envío gratis a toda Colombia",
             "Todos los filtros de agua para nevecón Samsung, LG, Whirlpool y GE en un solo lugar. Agrega al carrito, paga en línea y recibe con envío gratis.",
             [mg_ld, lista],
             f"""{mg}
<h1>Tienda de filtros de agua para nevecón</h1>
<p>{len(CATALOGO)} filtros para nevecones Samsung, LG, Whirlpool y GE. <b>Envío gratis</b> a toda Colombia y, en Cali, <b>instalación gratis</b>. Agrega varios al carrito y paga una sola vez.</p>
<div class="tienda-filtros" id="f-marca">{chips}</div>
<div class="tienda-filtros" id="f-tipo"><button type="button" data-t="todos" aria-pressed="true">Internos y externos</button><button type="button" data-t="interno" aria-pressed="false">Internos</button><button type="button" data-t="externo" aria-pressed="false">Externos</button>
<label style="margin-left:auto;font-size:14px">Ordenar <select id="orden"><option value="pop">Más pedidos</option><option value="asc">Menor precio</option><option value="desc">Mayor precio</option></select></label></div>
<div class="grid" id="tienda">{tarjetas}</div>
<p class="m">¿No sabes cuál es el tuyo? Búscalo por <a href="/referencias/">referencia</a> o por <a href="/neveras/">modelo de nevecón</a>.</p>
<script>
(() => {{
  let marca = "todas", tipo = "todos";
  const g = document.getElementById("tienda"), orig = [...g.children];
  function pintar() {{
    const o = document.getElementById("orden").value;
    const l = orig.filter(c => (marca === "todas" || c.dataset.marca === marca) && (tipo === "todos" || c.dataset.tipo === tipo));
    if (o !== "pop") l.sort((a, b) => (o === "asc" ? 1 : -1) * (a.dataset.precio - b.dataset.precio));
    g.replaceChildren(...l);
  }}
  document.getElementById("f-marca").addEventListener("click", e => {{ const b = e.target.closest("[data-f]"); if (!b) return; marca = b.dataset.f; e.currentTarget.querySelectorAll("button").forEach(x => x.setAttribute("aria-pressed", String(x === b))); pintar(); }});
  document.getElementById("f-tipo").addEventListener("click", e => {{ const b = e.target.closest("[data-t]"); if (!b) return; tipo = b.dataset.t; e.currentTarget.querySelectorAll("button[data-t]").forEach(x => x.setAttribute("aria-pressed", String(x === b))); pintar(); }});
  document.getElementById("orden").addEventListener("change", pintar);
}})();
</script>""")

    # ---------- Cali ----------
    mg, mg_ld = miga(("Inicio", "/"), ("Filtros en Cali", None))
    cali_ld = {"@type": "Store", "@id": "__BASE__/#tienda", "name": "PuroFiltro", "url": "__BASE__/cali/", "image": "__BASE__/img/lg-1000-o.jpg",
               "address": {"@type": "PostalAddress", "addressLocality": "Cali", "addressRegion": "Valle del Cauca", "addressCountry": "CO"},
               "areaServed": {"@type": "City", "name": "Cali"}, "priceRange": "$$"}
    escribir("/cali/", "Filtros de agua para nevecón en Cali | Domicilio e instalación gratis",
             "Filtros de agua para nevecón Samsung, LG, Whirlpool y GE en Cali, con domicilio e instalación gratis. Paga en línea con tarjeta, PSE o Nequi.",
             [mg_ld, cali_ld],
             f"""{mg}
<h1>Filtros de agua para nevecón en Cali, con instalación gratis</h1>
<p>En Cali te llevamos el filtro de tu nevecón y te lo instalamos <b>sin costo</b>. De paso revisamos que el dispensador y la máquina de hielo queden funcionando bien.</p>
<section class="caja"><h2>Cómo funciona</h2><ol><li>Busca tu filtro por la referencia o por el modelo del nevecón.</li><li>Escoge «Domicilio + instalación» y paga en línea con tarjeta, PSE, Nequi o botón Bancolombia.</li><li>Te llamamos para acordar el día y la hora, y llegamos con el filtro.</li></ol></section>
<h2>Filtros que instalamos</h2>
<div class="grid">{"".join(tarjeta(p) for p in CATALOGO)}</div>
<p class="m">¿No estás en Cali? Te lo enviamos gratis a toda Colombia y llega en unos 2 días hábiles.</p>""")

    # ---------- directorios ----------
    mg, mg_ld = miga(("Inicio", "/"), ("Referencias", None))
    filas = "".join(f'<tr><td><a href="{ruta}"><span class="ref">{esc(r)}</span></a></td><td>{esc(p["marca"])}</td><td><a href="/filtro/{p["slug"]}/">{esc(p["nombre_largo"])}</a></td></tr>'
                    for r, ruta, p in sorted(refs_dir, key=lambda x: norm(x[0])))
    escribir("/referencias/", "Referencias de filtros de agua para nevecón y sus equivalencias",
             "Directorio de referencias de filtros de agua para nevecón Samsung, LG, Whirlpool y GE, con sus equivalencias. Envío gratis a toda Colombia.",
             [mg_ld], f'{mg}<h1>Referencias de filtros y sus equivalencias</h1><p>Busca la referencia impresa en tu filtro viejo. Cada una te lleva al filtro que le sirve.</p>'
             f'<div class="caja" style="overflow-x:auto"><table class="t"><tr><th>Referencia</th><th>Marca</th><th>Filtro</th></tr>{filas}</table></div>')
    mg, mg_ld = miga(("Inicio", "/"), ("Neveras", None))
    bloques = ""
    for marca in MARCAS:
        ms = [x for x in modelos_dir if x[0] == marca]
        if ms:
            bloques += f'<section class="caja"><h2>Nevecones {esc(marca)}</h2><div class="chips">' + "".join(f'<a href="{ruta}">{esc(m)}</a>' for _, m, ruta, _ in sorted(ms, key=lambda x: x[1])) + "</div></section>"
    escribir("/neveras/", "¿Qué filtro usa mi nevecón? Busca por modelo",
             "Busca el modelo de tu nevecón Samsung, LG, Whirlpool o GE y mira qué filtro de agua usa. Envío gratis a toda Colombia.",
             [mg_ld], f'{mg}<h1>¿Qué filtro usa mi nevecón?</h1><p>Busca el modelo que aparece en la etiqueta de adentro de tu nevecón.</p>{bloques}'
             '<p class="m">¿No está tu modelo? Mira la guía <a href="/guia/como-saber-que-filtro-usa-mi-nevecon/">cómo saber qué filtro usa mi nevecón</a>.</p>')

    return {"paginas": paginas, "refs": refs_dir, "modelos": modelos_dir, "guias": [(f"/guia/{s}/", t) for s, t, _, _ in GUIAS]}
