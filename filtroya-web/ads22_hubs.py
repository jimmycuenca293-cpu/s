"""Páginas de búsqueda nuevas de filtrodeaguasamsung.com: regiones, áreas metropolitanas, índice de ciudades A–Z, glosario, preguntas frecuentes y mapa del sitio.
Cada una responde a una búsqueda real («filtro de agua Samsung Región Caribe», «filtro Samsung Valle de Aburrá»…) y enlaza a las páginas de ciudad y departamento."""
import re
import unicodedata

REGIONES = {
    "Caribe": ("Región Caribe", ["Atlántico", "Bolívar", "Cesar", "Córdoba", "La Guajira", "Magdalena", "Sucre"], "Barranquilla, Cartagena, Santa Marta, Valledupar, Montería, Sincelejo y Riohacha"),
    "Andina": ("Región Andina", ["Antioquia", "Boyacá", "Caldas", "Cundinamarca", "Huila", "Norte de Santander", "Quindío", "Risaralda", "Santander", "Tolima", "Bogotá D.C."], "Bogotá, Medellín, Bucaramanga, Cúcuta, Pereira, Manizales, Ibagué y Neiva"),
    "Pacífica": ("Región Pacífica", ["Chocó", "Cauca", "Nariño", "Valle del Cauca"], "Cali, Pasto, Popayán, Quibdó, Buenaventura y Tumaco"),
    "Orinoquía": ("Orinoquía", ["Arauca", "Casanare", "Meta", "Vichada"], "Villavicencio, Yopal, Arauca y Puerto Carreño"),
    "Amazonía": ("Amazonía", ["Amazonas", "Caquetá", "Guainía", "Guaviare", "Putumayo", "Vaupés"], "Leticia, Florencia, Mocoa, San José del Guaviare, Inírida y Mitú"),
    "Insular": ("Región Insular", ["San Andrés y Providencia"], "San Andrés"),
}
AREAS = {
    "valle-de-aburra": ("Valle de Aburrá", "Medellín y el Valle de Aburrá", ["medellin", "bello", "envigado", "itagui", "sabaneta", "la-estrella", "caldas", "copacabana", "girardota", "barbosa"]),
    "sabana-de-bogota": ("Bogotá y la Sabana", "Bogotá y la Sabana de Bogotá", ["bogota", "soacha", "chia", "cajica", "zipaquira", "cota", "funza", "mosquera", "madrid", "facatativa", "tocancipa", "sopo", "la-calera"]),
    "area-metropolitana-de-bucaramanga": ("Área Metropolitana de Bucaramanga", "el Área Metropolitana de Bucaramanga", ["bucaramanga", "floridablanca", "giron", "piedecuesta"]),
    "area-metropolitana-de-barranquilla": ("Área Metropolitana de Barranquilla", "el Área Metropolitana de Barranquilla", ["barranquilla", "soledad", "malambo", "puerto-colombia", "galapa", "baranoa"]),
    "cali-y-area-de-influencia": ("Cali y su área", "Cali, Yumbo, Jamundí y Palmira", ["cali", "yumbo", "jamundi", "palmira", "candelaria", "florida", "pradera", "cerrito", "el-cerrito"]),
    "eje-cafetero": ("Eje Cafetero", "el Eje Cafetero", ["pereira", "dosquebradas", "la-virginia", "manizales", "armenia", "santa-rosa-de-cabal", "calarca", "la-tebaida", "montenegro", "chinchina", "villamaria", "quimbaya", "circasia"]),
    "area-metropolitana-de-cucuta": ("Área Metropolitana de Cúcuta", "Cúcuta y su área metropolitana", ["cucuta", "villa-del-rosario", "los-patios", "el-zulia", "pamplona"]),
    "cartagena-y-alrededores": ("Cartagena y alrededores", "Cartagena y sus alrededores", ["cartagena", "turbaco", "arjona", "turbana", "santa-catalina", "clemencia"]),
}


def slug(n):
    n = unicodedata.normalize("NFKD", n).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", n).strip("-")


def crear(OUT, seo, productos, ciudades, depts):
    esc, cop, hero, rapida, faq_html, ld_web, ld_miga, ld_faq = seo.esc, seo.cop, seo.hero, seo.rapida, seo.faq_html, seo.ld_web, seo.ld_miga, seo.ld_faq
    cas = seo.Cascaron(OUT)
    out, info = [], {"region_de": {}, "area_de": {}, "regiones": {}, "areas": {}}
    precios = f"{cop(productos['cin']['precio'])} el HAF-CIN/EXP y el HAF-QIN/EXP, y {cop(productos['ext']['precio'])} el filtro externo DA29-10105J"
    tabla_filtros = ('<h2>Precios de los filtros Samsung</h2><div class="tbl-wrap"><table class="spec-table cols"><tr><th>Filtro</th><th>Código</th><th>Precio</th></tr>'
                     + "".join(f'<tr><td><a href="{p["url"]}">{esc(p["corto"])}</a></td><td>{esc(p["ref"])}</td><td>{cop(p["precio"])}</td></tr>' for p in productos.values()) + "</table></div>")
    tarjetas = '<div class="product-grid">' + "".join(seo.tarjeta_producto(p) for p in productos.values()) + "</div>"
    pre_comp = [("¿Puedo pagar contra entrega?", "Sí, en efectivo a la transportadora sin recargo, o en línea con Wompi: tarjeta, PSE, Nequi o Bancolombia."),
                ("¿El envío tiene costo?", "No: el envío es gratis a toda Colombia.")]

    def escribir(nombre, titulo, desc, kw, miga, contenido, preg):
        ld = [ld_web(nombre, titulo, desc), ld_miga(miga)] + ([ld_faq(preg)] if preg else [])
        (OUT / nombre).write_text(cas.pagina(nombre, titulo, desc, kw, miga, contenido, ld), encoding="utf-8")
        out.append(nombre)

    # ---------- regiones ----------
    for clave, (nombre_r, deptos, grandes) in REGIONES.items():
        presentes = [d for d in deptos if d in depts]
        if not presentes:
            continue
        n_ciu = sum(len(depts[d]) for d in presentes)
        nombre = f"filtros-samsung-region-{slug(clave)}.html"
        info["regiones"][nombre] = nombre_r
        for d in presentes:
            info["region_de"][d] = (nombre, nombre_r)
        filas = "".join(f'<tr><td><a href="filtros-samsung-{slug(d)}.html">{esc(d)}</a></td><td>{len(depts[d])}</td><td>{esc(", ".join(c for c, s, _ in sorted(depts[d])[:4]))}…</td></tr>' for d in presentes)
        titulo = f"Filtro de agua Samsung en la {nombre_r}"[:62] if len(f"Filtro de agua Samsung en la {nombre_r}") > 62 else f"Filtro de agua Samsung en la {nombre_r}"
        desc = f"Filtros de agua Samsung HAF-CIN, HAF-QIN y externo con envío gratis a {n_ciu} ciudades de la {nombre_r} ({len(presentes)} {'departamento' if len(presentes) == 1 else 'departamentos'}). Paga en línea o contra entrega."
        preg = [(f"¿Envían filtros de agua Samsung a la {nombre_r}?", f"Sí, enviamos gratis a {n_ciu} ciudades y municipios de la {nombre_r}, entre ellas {grandes}."),
                (f"¿Cuánto cuesta el filtro Samsung en la {nombre_r}?", f"{precios[0].upper() + precios[1:]}, con envío gratis."),
                ] + pre_comp
        miga = [("Inicio", "index.html"), ("Todas las ciudades", "filtro-agua-samsung-por-ciudad-colombia.html"), (nombre_r, None)]
        cont = (hero(f"Cobertura · {nombre_r}", f"Filtros de agua Samsung en la {nombre_r}", f"Envío gratis a {n_ciu} ciudades de {len(presentes)} {'departamento' if len(presentes) == 1 else 'departamentos'}, con pago en línea o contra entrega.")
                + rapida(f"Vendemos filtros de agua Samsung HAF-CIN/EXP, HAF-QIN/EXP y externo DA29-10105J con envío gratis a la {esc(nombre_r)}: {esc(grandes)} y {n_ciu - 1} municipios más.")
                + '<section class="section" style="background:#fff;"><div class="wrap"><div class="prose"><h2>Departamentos de la ' + esc(nombre_r) + ' donde entregamos</h2><div class="tbl-wrap"><table class="spec-table cols"><tr><th>Departamento</th><th>Ciudades</th><th>Algunas</th></tr>'
                + filas + "</table></div>" + tabla_filtros
                + '<p style="margin-top:16px">¿No sabes cuál es tu filtro? Mira <a href="como-identificar-filtro-samsung.html">cómo identificarlo</a>, la <a href="diferencia-haf-cin-haf-qin.html">diferencia entre HAF-CIN y HAF-QIN</a> o <a href="glosario-filtro-agua-nevecon-samsung.html">el glosario</a>.</p></div></div></section>'
                + '<section class="section"><div class="wrap"><div class="section-head"><h2>Compra tu filtro con envío a la ' + esc(nombre_r) + '</h2></div>' + tarjetas + '</div></section>' + faq_html(preg))
        escribir(nombre, titulo, desc, f"filtro agua samsung {clave.lower()}, filtro nevecon samsung región {clave.lower()}, comprar filtro samsung {clave.lower()}", miga, cont, preg)

    # ---------- áreas metropolitanas ----------
    for clave, (corto, largo, slugs) in AREAS.items():
        cs = [(ciudades[s]["city"], s) for s in slugs if s in ciudades]
        if len(cs) < 3:
            continue
        nombre = f"filtro-agua-samsung-{clave}.html"
        info["areas"][nombre] = corto
        for _, s in cs:
            info["area_de"].setdefault(s, (nombre, corto))
        lista = ", ".join(c for c, _ in cs)
        titulo = f"Filtro de agua Samsung en {corto}: envío gratis"
        titulo = titulo if len(titulo) <= 62 else f"Filtro de agua Samsung en {corto}"
        desc = f"Filtros de agua Samsung HAF-CIN, HAF-QIN y externo en {largo}: {lista}. Envío gratis, pago en línea o contra entrega."
        preg = [(f"¿Entregan filtros de agua Samsung en {largo}?", f"Sí, enviamos gratis a {lista}."),
                (f"¿Cuánto cuesta el filtro Samsung en {corto}?", f"{precios[0].upper() + precios[1:]}.")] + pre_comp
        miga = [("Inicio", "index.html"), ("Todas las ciudades", "filtro-agua-samsung-por-ciudad-colombia.html"), (corto, None)]
        cont = (hero(f"Cobertura · {corto}", f"Filtro de agua Samsung en {largo}", f"Envío gratis a {len(cs)} municipios, con pago en línea o contra entrega.")
                + rapida(f"Si vives en {esc(lista)}, te enviamos el filtro de agua de tu nevecón Samsung sin costo de envío. Escoge tu ciudad para ver el tiempo de entrega.")
                + '<section class="section" style="background:#fff;"><div class="wrap"><div class="prose"><h2>Municipios de ' + esc(corto) + ' con envío</h2><div class="city-tags">'
                + "".join(f'<a href="filtro-agua-samsung-{s}.html">{esc(c)}</a>' for c, s in cs) + "</div>" + tabla_filtros + "</div></div></section>"
                + '<section class="section"><div class="wrap"><div class="section-head"><h2>Compra tu filtro en ' + esc(corto) + '</h2></div>' + tarjetas + '</div></section>' + faq_html(preg))
        escribir(nombre, titulo, desc, f"filtro agua samsung {corto.lower()}, filtro nevecon samsung {corto.lower()}, comprar filtro samsung {lista.lower()}", miga, cont, preg)

    # ---------- índice A–Z ----------
    por_letra = {}
    for s, c in sorted(ciudades.items(), key=lambda x: slug(x[1]["city"])):
        por_letra.setdefault(slug(c["city"])[0].upper(), []).append((c["city"], s, c["dept"]))
    nombre = "ciudades-con-filtros-samsung-a-z.html"
    letras = "".join(f'<a href="#letra-{l}">{l}</a>' for l in sorted(por_letra))
    cuerpo = "".join(f'<div class="dept" id="letra-{l}"><h4>{l}</h4><div class="city-tags">' + "".join(f'<a href="filtro-agua-samsung-{s}.html" title="{esc(d)}">{esc(c)}</a>' for c, s, d in v) + "</div></div>" for l, v in sorted(por_letra.items()))
    miga = [("Inicio", "index.html"), ("Todas las ciudades", "filtro-agua-samsung-por-ciudad-colombia.html"), ("Ciudades de la A a la Z", None)]
    cont = (hero("Cobertura · A–Z", f"Filtros de agua Samsung en {len(ciudades)} ciudades de Colombia, de la A a la Z", "Busca tu ciudad por su inicial y entra a su página con tiempo de entrega y precios.")
            + '<section class="section" style="background:#fff;"><div class="wrap"><div class="city-tags" style="margin-bottom:18px;position:sticky;top:112px">' + letras + "</div>" + cuerpo + "</div></section>")
    escribir(nombre, f"Filtros de agua Samsung por ciudad de la A a la Z", f"Lista alfabética de las {len(ciudades)} ciudades y municipios de Colombia donde enviamos filtros de agua Samsung para nevecón, con envío gratis y pago contra entrega.",
             "filtro agua samsung por ciudad, ciudades filtro nevecon samsung, filtro samsung colombia lista de ciudades", miga, cont, None)

    # ---------- glosario ----------
    terminos = [("HAF-CIN/EXP (DA29-00020B)", "Filtro de agua Samsung de cartucho redondo que se instala girando. Es el más usado en nevecones French Door y Side by Side."),
                ("HAF-QIN/EXP (DA97-17376B)", "Filtro de agua Samsung de cartucho cuadrado que se instala empujando, usado en nevecones Samsung más recientes."),
                ("DA29-10105J (HAFEX/EXP)", "Filtro externo de Samsung: se instala fuera del nevecón, en la línea de agua."),
                ("Referencia o código", "Número impreso en el filtro (por ejemplo DA29-00020B) que identifica la pieza exacta. Es la forma más segura de pedir el filtro correcto."),
                ("Equivalencia", "Un mismo filtro puede aparecer con varios códigos (DA29-00020A, HAF-CIN, 46-9101…). Todos corresponden a la misma pieza."),
                ("Nevecón", "Forma de llamar en Colombia a un refrigerador Samsung grande de puertas dobles con dispensador de agua y hielo."),
                ("French Door", "Nevecón con dos puertas de refrigerador arriba y cajón de congelador abajo."),
                ("Side by Side", "Nevecón con refrigerador y congelador lado a lado, cada uno con su puerta vertical."),
                ("Luz del filtro", "Aviso en el panel que se enciende cuando toca cambiar el filtro. Se apaga con el botón de reinicio después de instalar el nuevo."),
                ("Purga", "Dejar correr unos 6 litros de agua por el dispensador después del cambio para sacar el aire del filtro nuevo."),
                ("NSF/ANSI 42 y 53", "Normas de certificación para filtros de agua: la 42 se refiere a sabor y olor (cloro) y la 53 a efectos sobre la salud."),
                ("Contra entrega", "Pagas en efectivo a la transportadora cuando recibes tu pedido, sin anticipos."),
                ("Retracto", "Derecho a devolver el producto sin usar dentro de 5 días hábiles desde la entrega.")]
    nombre = "glosario-filtro-agua-nevecon-samsung.html"
    cont = (hero("Glosario", "Glosario del filtro de agua para nevecón Samsung", "Qué significa cada código y cada término que verás al comprar o cambiar el filtro.")
            + '<section class="section" style="background:#fff;"><div class="wrap"><div class="prose">' + "".join(f"<h2>{esc(t)}</h2><p>{esc(d)}</p>" for t, d in terminos)
            + '<p>Más ayuda: <a href="como-identificar-filtro-samsung.html">cómo identificar tu filtro</a> · <a href="equivalencias-codigos-filtro-samsung.html">equivalencias de códigos</a> · <a href="preguntas-frecuentes-filtro-agua-samsung.html">preguntas frecuentes</a>.</p></div></div></section>')
    miga = [("Inicio", "index.html"), ("Guías", "guias-filtro-agua-nevecon-samsung.html"), ("Glosario", None)]
    escribir(nombre, "Glosario: HAF-CIN, HAF-QIN, DA29-00020B y más", "Qué significan HAF-CIN, HAF-QIN, DA29-00020B, DA97-17376B, DA29-10105J, luz del filtro, purga y NSF/ANSI 42 y 53 en un filtro de agua para nevecón Samsung.",
             "glosario filtro samsung, que es haf-cin, que es haf-qin, da29-00020b significado, nsf ansi 42 53", miga, cont, [(t, d) for t, d in terminos[:6]])

    # ---------- preguntas frecuentes (todas) ----------
    p = productos
    preg = [("¿Qué filtro de agua usa mi nevecón Samsung?", f"Depende del modelo: el {p['cin']['corto']} ({p['cin']['ref']}), el {p['qin']['corto']} ({p['qin']['ref']}) o el externo {p['ext']['ref']}. Compara el código del filtro viejo o busca tu modelo en la tienda."),
            ("¿Cómo sé si mi filtro es redondo o cuadrado?", "Sácalo y míralo: el HAF-CIN es redondo y el HAF-QIN es cuadrado. Si va fuera del nevecón, en la manguera, es el externo."),
            ("¿Cada cuánto se cambia el filtro de agua del nevecón Samsung?", "Cada 6 meses de uso normal, o antes si el agua cambia de sabor o el dispensador entrega menos agua."),
            ("¿Cuánto cuesta el filtro de agua Samsung?", f"{precios[0].upper() + precios[1:]}, con envío gratis."),
            ("¿Puedo pagar contra entrega?", "Sí, en efectivo a la transportadora sin recargo. También puedes pagar en línea con tarjeta, PSE, Nequi o Bancolombia."),
            ("¿El envío tiene costo?", "No, el envío es gratis a toda Colombia."),
            ("¿A qué ciudades envían?", f"A {len(ciudades)} ciudades y municipios de Colombia y a otros lugares que nos escriban."),
            ("¿Los filtros son nuevos?", "Sí, nuevos y en su empaque, con la referencia impresa."),
            ("¿Puedo cambiar el filtro yo mismo?", "Sí, toma unos minutos y no necesita herramientas: mira la guía paso a paso."),
            ("¿Qué hago si pedí un filtro que no corresponde?", "Tienes 5 días hábiles de retracto desde la entrega, con el filtro sin usar."),
            ("¿Cómo reinicio la luz del filtro?", "Después de instalar el filtro nuevo, mantén presionado el botón de reinicio del panel unos segundos."),
            ("¿Cuánta agua debo sacar después del cambio?", "Unos 6 litros, para purgar el aire del filtro nuevo."),
            ("¿Recibo comprobante de mi pedido?", "Sí, te llega la confirmación del pedido a tu correo.")]
    nombre = "preguntas-frecuentes-filtro-agua-samsung.html"
    cont = (hero("Preguntas frecuentes", "Preguntas frecuentes sobre el filtro de agua del nevecón Samsung", "Las dudas más comunes sobre referencias, precios, pagos, envíos y cambio del filtro.")
            + faq_html(preg) + '<section class="section"><div class="wrap"><div class="section-head"><h2>Escoge tu filtro</h2></div>' + tarjetas + "</div></section>")
    escribir(nombre, "Preguntas frecuentes del filtro de agua Samsung", "Respuestas sobre qué filtro usa tu nevecón Samsung, precios, pago contra entrega, envío gratis, cada cuánto cambiarlo y cómo reiniciar la luz del filtro.",
             "preguntas frecuentes filtro samsung, cada cuanto cambiar filtro nevecon samsung, filtro samsung contra entrega", [("Inicio", "index.html"), ("Preguntas frecuentes", None)], cont, preg)

    # ---------- mapa del sitio (se genera al final, cuando ya existen todas las páginas) ----------
    guias = []
    for f in sorted(OUT.glob("*.html")):
        if f.name.startswith(("filtro-agua-samsung-", "filtro-haf-cin-", "filtro-haf-qin-", "filtro-externo-", "cambiar-filtro-nevecon-samsung-", "precio-filtro-nevecon-samsung-", "comprar-filtro-samsung-contra-entrega-", "filtros-samsung-",
                              "filtro-nevecon-samsung-", "referencia-filtro-samsung-", "ciudades-con-", "glosario-", "preguntas-frecuentes-")) or f.name in ("index.html", "404.html", "mapa-del-sitio.html"):
            continue
        m = re.search(r"<h1[^>]*>(.*?)</h1>", f.read_text(encoding="utf-8"), re.S)
        if m:
            guias.append((re.sub(r"<[^>]+>", "", m.group(1)).strip(), f.name))
    bloque = lambda t, items: f'<h2>{esc(t)}</h2><ul>' + "".join(f'<li><a href="{u}">{esc(n)}</a></li>' for n, u in items) + "</ul>"
    refs = [(f.stem.replace("referencia-filtro-samsung-", "").upper(), f.name) for f in sorted(OUT.glob("referencia-filtro-samsung-*.html"))]
    mods = [(f.stem.split("-")[-1].upper(), f.name) for f in sorted(OUT.glob("filtro-nevecon-samsung-rf*.html"))]
    cuerpo = (bloque("Filtros", [(p_["corto"] + " · " + cop(p_["precio"]), p_["url"]) for p_ in productos.values()]) + bloque("Regiones", [(n, u) for u, n in info["regiones"].items()])
              + bloque("Áreas metropolitanas", [(n, u) for u, n in info["areas"].items()]) + bloque("Departamentos", [(f"Filtros Samsung en {d}", f"filtros-samsung-{slug(d)}.html") for d in sorted(depts)])
              + bloque("Guías y consejos", guias) + bloque("Por código de filtro", refs) + bloque("Por modelo de nevecón", mods)
              + bloque("Ciudades", [("Todas las ciudades por departamento", "filtro-agua-samsung-por-ciudad-colombia.html"), ("Ciudades de la A a la Z", "ciudades-con-filtros-samsung-a-z.html")])
              + bloque("Ayuda", [("Glosario", "glosario-filtro-agua-nevecon-samsung.html"), ("Preguntas frecuentes", "preguntas-frecuentes-filtro-agua-samsung.html"), ("Garantía y devolución", "garantia-cambio-y-devolucion-filtro-samsung.html"), ("Envíos", "envio-filtros-samsung-colombia.html")]))
    nombre = "mapa-del-sitio.html"
    cont = (hero("Mapa del sitio", "Mapa del sitio: filtros de agua Samsung", "Todas las páginas de la tienda en un solo lugar.") + '<section class="section" style="background:#fff;"><div class="wrap"><div class="prose">' + cuerpo + "</div></div></section>")
    escribir(nombre, "Mapa del sitio | Filtros de agua Samsung", "Todas las páginas de la tienda de filtros de agua Samsung: filtros, guías, regiones, departamentos, ciudades, códigos y modelos de nevecón.",
             "mapa del sitio filtro agua samsung", [("Inicio", "index.html"), ("Mapa del sitio", None)], cont, None)
    return out, info
