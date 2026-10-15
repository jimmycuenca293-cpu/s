"""Páginas extra para Google: una por cada referencia equivalente, una por cada modelo de nevecón,
guías, envíos por ciudad y los directorios. Las usa build.py.

Cada página trae información propia (equivalencias, cómo confirmar, cómo cambiarlo, modelos),
no solo el nombre cambiado: así Google la toma como útil y no como una copia.
"""
import html
import json

import instalacion

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
    <ul class="ok"><li><b>Envío gratis</b> a toda Colombia: llega en 2 a 3 días hábiles a las principales ciudades.</li><li><b>Fácil de instalar:</b> paso a paso en la página del filtro.</li><li>Asesoría por WhatsApp para confirmar que es el de tu nevecón.</li></ul>
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


def mas_info(p, ubic, r=None):
    """Bloque de descripción ampliada: qué hace, cuándo cambiarlo y qué pasa si no se cambia. Sirve en la ficha y en las referencias."""
    nombre = r or p["ref"]
    tipo = ("Es un filtro externo: se conecta en la manguera que lleva el agua al nevecón, así que sirve también para nevecones que no traen filtro de fábrica o que lo tienen dañado."
            if ubic(p) == "externo" else
            "Es un filtro interno: va dentro del nevecón, en su alojamiento original, y se cambia en menos de un minuto sin cerrar la llave del agua.")
    return f"""<section class="caja">
  <h2>Para qué sirve el filtro {esc(nombre)}</h2>
  <p>{esc(p.get("desc", ""))}</p>
  <p>{esc(tipo)}</p>
  <ul class="ok"><li><b>Mejor sabor y olor:</b> retiene el cloro y los compuestos que le dan sabor a tubería al agua y al hielo.</li>
  <li><b>Hielo más claro:</b> menos sedimento y partículas en los cubos.</li>
  <li><b>Protege el nevecón:</b> el sedimento tapa la válvula de entrada y la máquina de hielo; un filtro al día las cuida.</li>
  <li><b>Más barato que el botellón:</b> un filtro rinde unos 6 meses de agua fría filtrada para toda la familia.</li></ul>
  <h3 style="margin:6px 0 0;font-size:16px">Señales de que ya toca cambiarlo</h3>
  <ul><li>Se cumplieron 6 meses desde el último cambio, o se prendió la luz de «Filter» o «Replace».</li><li>El agua o el hielo saben u huelen raro.</li><li>El dispensador echa el agua con poca presión o a chorritos.</li><li>El hielo sale pequeño, turbio o la máquina hace menos.</li></ul>
</section>"""


def generar(OUT, CATALOGO, MARCAS, slug, norm, ubic, cabeza_php, tarjeta, CIUDADES_CO=()):
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
            desc = (f"¿Buscas el filtro {r}? Es la misma referencia que el {p['nombre_largo']}: {cop(p['precio'])} con envío gratis a toda Colombia. " + "Paga en línea con tarjeta, PSE o Nequi.")
            preguntas = [
                (f"¿El filtro {r} es igual al {p['ref']}?", f"Sí. {r} y {p['ref']} son nombres de la misma referencia de filtro para nevecón {p['marca']}: tienen la misma forma, la misma conexión y se cambian igual."),
                (f"¿Cada cuánto se cambia el filtro {r}?", "Cada 6 meses, o antes si el agua cambia de sabor, de olor o sale con poca presión."),
                (f"¿Cuánto cuesta el envío del {r}?", "Nada. El envío es gratis a toda Colombia y llega en unos 2 días hábiles después del pago. "),
            ]
            mg, mg_ld = miga(("Inicio", "/"), ("Referencias", "/referencias/"), (f"Filtro {r}", None))
            modelos = ", ".join(f'<a href="/nevecon/{slug(m)}/">{esc(m)}</a>' for m in p["modelos"])
            cuerpo = f"""{mg}
<h1>Filtro {esc(r)} para nevecón {esc(p["marca"])}</h1>
<p>El filtro <b>{esc(r)}</b> es la misma referencia que el <b>{esc(p["nombre_largo"])}</b>: {donde}. Lo tenemos a <b>{cop(p["precio"])}</b> con envío gratis a toda Colombia.</p>
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
{mas_info(p, ubic, r)}
{instalacion.tutorial_html(p, r)}
<p class="m">¿Otro tipo de filtro? Mira <a href="/instalacion/">todos los tutoriales de instalación</a>.</p>
{faq_html(preguntas)}"""
            escribir(ruta, titulo, desc, [mg_ld, faq_ld(preguntas), instalacion.tutorial_ld(p, f"__BASE__{ruta}", r)], cuerpo)

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
            desc = (f"El nevecón {p['marca']} {m} usa el filtro {p['nombre_largo']}. Cómprelo a {cop(p['precio'])} con envío gratis a toda Colombia " + ". Paga con tarjeta, PSE o Nequi.").replace("Cómprelo", "Cómpralo")
            preguntas = [
                (f"¿Qué filtro usa el nevecón {p['marca']} {m}?", f"El {p['nombre_largo']} (referencia {p['ref']}). También aparece como {', '.join([x for x in p['refs'] if norm(x) != norm(p['ref'])][:4]) or p['ref']}."),
                (f"¿Cada cuánto se cambia el filtro del {m}?", "Cada 6 meses, o antes si el agua cambia de sabor, de olor, o el hielo sale turbio o con mal sabor."),
                (f"¿Es difícil de instalar?", "No. Se instala en minutos y sin herramientas: el paso a paso está en esta página y te asesoramos por WhatsApp."),
            ]
            mg, mg_ld = miga(("Inicio", "/"), ("Neveras", "/neveras/"), (f"Nevecón {p['marca']} {m}", None))
            cuerpo = f"""{mg}
<h1>Filtro de agua para nevecón {esc(p["marca"])} {esc(m)}</h1>
<p>El nevecón <b>{esc(p["marca"])} {esc(m)}</b> usa el filtro <b>{esc(p["nombre_largo"])}</b>. Lo tenemos a {cop(p["precio"])} con envío gratis a toda Colombia.</p>
{caja_producto(p, f"Para el {m} te sirve")}
<section class="caja">
  <h2>Antes de comprar, confirma tu modelo</h2>
  <p>El modelo está en la etiqueta de adentro del refrigerador (en una pared lateral o en el techo). Tiene que decir <span class="ref">{esc(m)}</span>; a veces trae letras o números de más al final, y es el mismo nevecón.</p>
  <p>El filtro que trae puesto debe decir <span class="ref">{esc(p["ref"])}</span> o una de sus equivalencias: {", ".join(f'<a href="/referencia/{slug(x)}/">{esc(x)}</a>' if norm(x) not in principales else esc(x) for x in p["refs"] if norm(x) != norm(p["ref"])) or "—"}.</p>
</section>
{instalacion.tutorial_html(p)}
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
<p>¿Te quedó alguna duda? Escríbenos por WhatsApp y te guiamos paso a paso.</p>
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
                 'técnico de neveras · Actualizado el 15 de octubre de 2026</p>')
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
<p>{len(CATALOGO)} filtros para nevecones Samsung, LG, Whirlpool y GE. <b>Envío gratis</b> a toda Colombia y pago seguro en línea. Agrega varios al carrito y paga una sola vez.</p>
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

    # ---------- ciudades: una página por ciudad y por departamento ----------
    rutas_ciudad = {}
    deptos = {}
    for c in CIUDADES_CO:
        deptos.setdefault(c[1], []).append(c)
    precios = [p["precio"] for p in CATALOGO]
    oferta = {"@type": "AggregateOffer", "priceCurrency": "COP", "lowPrice": str(min(precios)), "highPrice": str(max(precios)), "offerCount": str(len(CATALOGO))}
    for c in CIUDADES_CO:
        rutas_ciudad[c[0]] = f"/envios/{slug(c[1])}/{slug(c[0])}/"
    for c in CIUDADES_CO:
        ciudad, depto = c[0], c[1]
        dias = c[2] if len(c) > 2 else 2
        lejos = dias >= 5
        ruta = rutas_ciudad[ciudad]
        vecinas = [x for x in deptos[depto] if x[0] != ciudad]
        mg, mg_ld = miga(("Inicio", "/"), ("Envíos", "/envios/"), (depto, f"/envios/{slug(depto)}/"), (ciudad, None))
        cuando = f"{dias} días hábiles" if dias > 2 else "2 días hábiles"
        preguntas = [
            (f"¿Envían filtros de agua para nevecón a {ciudad}?", f"Sí. Enviamos a {ciudad} ({depto}) los filtros para nevecones Samsung, LG, Whirlpool y GE, con envío gratis y número de guía."),
            (f"¿Cuánto se demora el envío a {ciudad}?", f"Llega en unos {cuando} después del pago. {'Por la distancia puede tardar un poco más en temporada alta.' if lejos else 'Despachamos el mismo día o el siguiente día hábil.'}"),
            (f"¿Cuánto cuesta el envío a {ciudad}?", "Nada: el envío es gratis y el precio que ves es el precio final."),
            (f"¿Es difícil de instalar?", "No. El filtro se cambia en menos de 5 minutos y sin herramientas: te dejamos los pasos en la página de cada filtro y te asesoramos por WhatsApp."),
            (f"¿Cómo pago desde {ciudad}?", "En línea, en página de pago segura: tarjeta débito o crédito, PSE, Nequi o botón Bancolombia. Te llega el recibo a tu correo."),
        ]
        ld = [mg_ld, faq_ld(preguntas), {
            "@type": "Service", "name": f"Venta y envío de filtros de agua para nevecón a {ciudad}", "serviceType": "Venta de filtros de agua para nevecón",
            "provider": {"@id": "__BASE__/#tienda"}, "url": f"__BASE__{ruta}",
            "areaServed": {"@type": "City", "name": ciudad, "containedInPlace": {"@type": "AdministrativeArea", "name": depto, "containedInPlace": {"@type": "Country", "name": "Colombia"}}},
            "offers": oferta}]
        cuerpo = f"""{mg}
<h1>Filtros de agua para nevecón en {esc(ciudad)}</h1>
<p>Te enviamos el filtro de agua de tu nevecón <b>Samsung, LG, Whirlpool o GE</b> a {esc(ciudad)}, {esc(depto)}, con <b>envío gratis</b>. Llega en unos <b>{cuando}</b> después del pago y te mandamos el número de guía a tu correo.</p>
<section class="caja">
  <h2>Envío a {esc(ciudad)}</h2>
  <dl class="dq"><dt>Ciudad</dt><dd>{esc(ciudad)}</dd><dt>Departamento</dt><dd>{esc(depto)}</dd><dt>Tiempo de entrega</dt><dd>Unos {cuando}</dd><dt>Costo del envío</dt><dd>Gratis</dd>
  <dt>Instalación</dt><dd>La haces tú en 5 minutos, sin herramientas</dd><dt>Pago</dt><dd>Tarjeta, PSE, Nequi o botón Bancolombia</dd></dl>
</section>
<h2>Filtros que enviamos a {esc(ciudad)}</h2>
<div class="grid">{"".join(tarjeta(p) for p in CATALOGO)}</div>
<section class="caja">
  <h2>Cómo pedir tu filtro desde {esc(ciudad)}</h2>
  <ol><li>Busca la referencia impresa en tu filtro viejo o el modelo de tu nevecón: mira el <a href="/referencias/">directorio de referencias</a> o el de <a href="/neveras/">modelos de nevecón</a>.</li>
  <li>Agrégalo al carrito (puedes llevar varios o el pack anual de 2) y escoge {esc(ciudad)} como ciudad de entrega.</li>
  <li>Paga en línea. Te llega el recibo al correo y despachamos tu pedido con número de guía.</li>
  <li>Cámbialo en 5 minutos con la guía <a href="/guia/como-cambiar-el-filtro-de-agua-del-nevecon/">cómo cambiar el filtro de agua del nevecón</a>.</li></ol>
</section>
{faq_html(preguntas)}
{f'<section class="caja"><h2>También enviamos en {esc(depto)}</h2><div class="chips">' + "".join(f'<a href="{rutas_ciudad[x[0]]}">{esc(x[0])}</a>' for x in vecinas)  + '</div></section>' if vecinas else ""}
<p class="m">Mira <a href="/envios/">todas las ciudades a las que enviamos</a>.</p>"""
        escribir(ruta, f"Filtros de agua para nevecón en {ciudad} | Envío gratis",
                 f"Filtros de agua para nevecón Samsung, LG, Whirlpool y GE con envío gratis a {ciudad}, {depto}. Llega en unos {cuando}. Paga en línea con tarjeta, PSE o Nequi.",
                 ld, cuerpo)
    for depto, cs in deptos.items():
        mg, mg_ld = miga(("Inicio", "/"), ("Envíos", "/envios/"), (depto, None))
        lista = sorted(cs, key=lambda x: slug(x[0]))
        escribir(f"/envios/{slug(depto)}/", f"Filtros de agua para nevecón en {depto} | Envío gratis",
                 f"Enviamos filtros de agua para nevecón Samsung, LG, Whirlpool y GE a {', '.join(x[0] for x in lista[:6])} y más ciudades de {depto}. Envío gratis.",
                 [mg_ld, {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"__BASE__{rutas_ciudad[x[0]]}", "name": x[0]} for i, x in enumerate(lista)]}],
                 f"""{mg}
<h1>Filtros de agua para nevecón en {esc(depto)}</h1>
<p>Enviamos gratis los filtros de agua para nevecones Samsung, LG, Whirlpool y GE a {len(lista)} {"ciudad" if len(lista) == 1 else "ciudades"} de {esc(depto)}. Escoge la tuya para ver el tiempo de entrega:</p>
<div class="caja" style="overflow-x:auto"><table class="t"><tr><th>Ciudad</th><th>Entrega</th><th>Envío</th></tr>{"".join(f'<tr><td><a href="{rutas_ciudad[x[0]]}">{esc(x[0])}</a></td><td>{"Unos " + str(x[2] if len(x) > 2 else 2) + " días hábiles"}</td><td>Gratis</td></tr>' for x in lista)}</table></div>
<h2>Filtros disponibles</h2>
<div class="grid">{"".join(tarjeta(p) for p in CATALOGO)}</div>""")
    mg, mg_ld = miga(("Inicio", "/"), ("Envíos", None))
    bloques = "".join(f'<section class="caja"><h2><a href="/envios/{slug(d)}/">{esc(d)}</a></h2><div class="chips">'
                      + "".join(f'<a href="{rutas_ciudad[x[0]]}">{esc(x[0])}</a>' for x in sorted(cs, key=lambda x: slug(x[0]))) + "</div></section>"
                      for d, cs in sorted(deptos.items(), key=lambda kv: slug(kv[0])))
    escribir("/envios/", "Envío gratis de filtros para nevecón a toda Colombia | Ciudades",
             f"Enviamos filtros de agua para nevecón a {len(CIUDADES_CO)} ciudades de los {len(deptos)} departamentos de Colombia y Bogotá. Envío gratis, pago en línea.",
             [mg_ld], f"""{mg}
<h1>Enviamos a toda Colombia</h1>
<p>Envío <b>gratis</b> de filtros de agua para nevecón a {len(CIUDADES_CO)} ciudades y municipios de {len(deptos)} departamentos. Si tu municipio no aparece, también te lo enviamos: escoge «Otro municipio» al pagar.</p>
{bloques}""")

    # ---------- tutoriales de instalación ----------
    mg, mg_ld = miga(("Inicio", "/"), ("Cómo instalar tu filtro", None))
    filas = "".join(f'''<section class="caja"><h2><a href="/filtro/{p["slug"]}/#instalacion">Cómo instalar el {esc(p["nombre_largo"])}</a></h2><p><b>Dónde va:</b> {esc(instalacion.datos(p)["donde"])}</p><p class="m">Tiempo: {esc(instalacion.datos(p)["tiempo"])} · <a href="/filtro/{p["slug"]}/#instalacion">Ver el paso a paso</a></p></section>''' for p in CATALOGO)
    escribir("/instalacion/", "Cómo instalar el filtro de agua del nevecón | Tutorial por referencia",
             "Paso a paso para instalar cada filtro de agua de nevecón Samsung, LG, Whirlpool y GE: dónde va, cómo se saca el viejo, cómo se pone el nuevo y cómo reiniciar la luz del filtro.",
             [mg_ld, {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"__BASE__/filtro/{p['slug']}/#instalacion", "name": f"Cómo instalar el {p['nombre_largo']}"} for i, p in enumerate(CATALOGO)]}],
             f"""{mg}
<h1>Cómo instalar el filtro de agua de tu nevecón</h1>
<p>Cada filtro se instala distinto: unos van arriba dentro del refrigerador y se giran, otros van en la rejilla de abajo y otros en la manguera de atrás. Busca el tuyo y sigue el paso a paso. Se hace en minutos y sin herramientas; y te asesoramos por WhatsApp.</p>
<section class="caja"><h2>Antes de empezar</h2><ul><li>Ten a la mano un trapo: al sacar el filtro caen unas gotas.</li><li>Confirma que el filtro nuevo tenga la misma referencia que el viejo o una de sus <a href="/referencias/">equivalencias</a>.</li><li>Después de instalarlo, purga el agua y reinicia la luz del filtro (está en cada tutorial).</li></ul></section>
{filas}
<p class="m">¿Cada cuánto se cambia? Mira la guía <a href="/guia/cada-cuanto-cambiar-el-filtro-del-nevecon/">cada cuánto cambiar el filtro del nevecón</a>.</p>""")

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

    return {"paginas": paginas, "rutas_ciudad": rutas_ciudad, "refs": refs_dir, "modelos": modelos_dir, "guias": [(f"/guia/{s}/", t) for s, t, _, _ in GUIAS]}
