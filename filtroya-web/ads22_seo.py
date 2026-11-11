"""SEO ampliado para filtrodeaguasamsung.com: más ciudades, páginas por referencia, por modelo de nevecón y por departamento.
Copia el diseño y la estructura de las páginas que ya tiene el sitio (no cambia ninguna de ellas, solo agrega páginas nuevas y enlaces)."""
import html
import json
import re
import unicodedata

DOMINIO = "https://filtrodeaguasamsung.com"
HOY = "2026-11-11"
WA = "573054796329"

# ciudades que se suman (municipios con más de 30.000 habitantes y cabeceras importantes que todavía no tenían página)
NUEVAS = {
    "Antioquia": ["Marinilla", "La Ceja", "Guarne", "Girardota", "Barbosa", "Carepa", "Chigorodó", "Yarumal", "Puerto Berrío", "Santa Fe de Antioquia", "Andes", "Segovia"],
    "Atlántico": ["Galapa", "Sabanagrande", "Santo Tomás", "Palmar de Varela"],
    "Bolívar": ["Mompós", "María la Baja", "San Jacinto", "Turbana"],
    "Boyacá": ["Puerto Boyacá", "Villa de Leyva", "Moniquirá", "Samacá", "Nobsa"],
    "Caldas": ["Anserma", "Riosucio", "Aguadas", "Salamina"],
    "Caquetá": ["San Vicente del Caguán"],
    "Casanare": ["Villanueva", "Paz de Ariporo", "Monterrey"],
    "Cauca": ["Piendamó", "Guapi", "Timbío", "Miranda", "Corinto"],
    "Cesar": ["Bosconia", "Agustín Codazzi", "La Jagua de Ibirico", "Curumaní", "El Copey"],
    "Chocó": ["Tadó", "Condoto", "Bahía Solano"],
    "Córdoba": ["Planeta Rica", "Tierralta", "Ciénaga de Oro", "San Pelayo", "Ayapel", "Puerto Libertador"],
    "Cundinamarca": ["Sibaté", "Tocancipá", "Cota", "Sopó", "Tenjo", "Villeta", "La Mesa", "Guaduas", "Ubaté"],
    "Huila": ["Campoalegre", "Rivera", "Gigante", "Algeciras"],
    "La Guajira": ["Fonseca", "San Juan del Cesar", "Villanueva", "Dibulla", "Manaure"],
    "Magdalena": ["Plato", "El Banco", "Aracataca", "Pivijay"],
    "Meta": ["Puerto López", "Puerto Gaitán", "Cumaral", "Restrepo"],
    "Nariño": ["Túquerres", "La Unión", "Sandoná", "Samaniego"],
    "Norte de Santander": ["Tibú", "Ábrego", "El Zulia", "Chinácota"],
    "Putumayo": ["Orito", "Sibundoy"],
    "Quindío": ["Quimbaya", "Circasia", "Filandia", "Salento"],
    "Risaralda": ["Belén de Umbría", "Marsella", "Quinchía"],
    "Santander": ["Socorro", "Lebrija", "Málaga", "Vélez", "Puerto Wilches", "Sabana de Torres"],
    "Sucre": ["Tolú", "Sampués", "San Marcos", "Coveñas", "San Onofre"],
    "Tolima": ["Flandes", "Mariquita", "Guamo", "Purificación", "Natagaima", "Ortega", "Armero"],
    "Valle del Cauca": ["El Cerrito", "Florida", "Pradera", "Dagua", "Roldanillo", "Zarzal", "Caicedonia", "Ginebra", "Guacarí"],
}

PREF = {"agua": "filtro-agua-samsung-", "cin": "filtro-haf-cin-", "qin": "filtro-haf-qin-", "ext": "filtro-externo-",
        "cambiar": "cambiar-filtro-nevecon-samsung-", "precio": "precio-filtro-nevecon-samsung-", "comprar": "comprar-filtro-samsung-contra-entrega-"}
GRANDES = [("Bogotá D.C.", "bogota"), ("Medellín", "medellin"), ("Cali", "cali"), ("Barranquilla", "barranquilla"), ("Cartagena", "cartagena")]

# modelos de nevecón y su filtro (los mismos de las tiendas de Samsung)
MODELOS = {"cin": ["RF28HMEDBSR", "RF263BEAESR", "RF28HFEDBSR", "RF4287HARS", "RF26J7500SR", "RF23J9011SR"],
           "qin": ["RF28R7351SR", "RF22R7351SG", "RF28R7201SR", "RF23M8070SR"]}


def slug(n):
    n = unicodedata.normalize("NFKD", n).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", n).strip("-")


def esc(s):
    return html.escape(str(s), quote=True)


def cop(v):
    return "$" + f"{int(v):,}".replace(",", ".")


# ---------- ciudades ----------
def leer_ciudades(OUT):
    d = {}
    for f in sorted(OUT.glob("filtro-haf-cin-*.html")):
        s = f.name[len("filtro-haf-cin-"):-5]
        t = f.read_text(encoding="utf-8")
        m = re.search(r"<th>Ciudad de entrega</th><td>([^<]+?), ([^<]+)</td></tr><tr><th>Tiempo estimado</th><td>([^<]+)</td>", t)
        if m:
            d[s] = {"city": m.group(1), "dept": m.group(2), "days": m.group(3)}
    return d


def etiquetas(prefijo, vecinos, ciudades, propia):
    """Bloque «También enviamos a…»: primero los de su departamento y luego las ciudades grandes."""
    n, usados = [], set()
    for s in vecinos:
        if s != propia and s in ciudades and s not in usados:
            usados.add(s); n.append((ciudades[s]["city"], s))
    for c, s in GRANDES:
        if len(n) >= 8:
            break
        if s != propia and s not in usados:
            usados.add(s); n.append((c, s))
    return "".join(f'<a href="{prefijo}{s}.html"><span>{esc(c)}</span></a>' for c, s in n[:8])


def clonar(plantilla, tp, nuevo, tags_html, tsd):
    """Copia una página de ciudad cambiando solo los datos de la ciudad."""
    t = plantilla
    tc, ts, td = tp["city"], tp["slug"], tp["dept"]
    nc, ns, nd = nuevo["city"], nuevo["slug"], nuevo["dept"]
    if td != tc:
        t = t.replace(td, nd)
    from urllib.parse import quote
    t = t.replace("%20" + quote(tc), "%20" + quote(nc)).replace("%20" + tc, "%20" + quote(nc))
    t = re.sub(r"(?<![\wÀ-ÿ])" + re.escape(tc) + r"(?![\wÀ-ÿ])", nc, t)
    t = t.replace(f"-{ts}.html", f"-{ns}.html")
    kw_old, kw_new = ts.replace("-", " "), ns.replace("-", " ")
    t = re.sub(r'(<meta name="keywords" content=")([^"]*)(")', lambda m: m.group(1) + re.sub(r"(?<![\w])" + re.escape(kw_old) + r"(?![\w])", kw_new, m.group(2)) + m.group(3), t)
    t = re.sub(r'<div class="city-tags">.*?</div>', '<div class="city-tags">' + tags_html + "</div>", t, count=1, flags=re.S)
    if tp["days"] != nuevo["days"]:
        t = t.replace(tp["days"], nuevo["days"])
    sin_tags = re.sub(r'<div class="city-tags">.*?</div>', "", t, flags=re.S)
    assert not re.search(re.escape(tc), sin_tags) or tc == nc, f"quedó {tc} en la página de {nc}"
    return t


def expandir_ciudades(OUT, ciudades):
    """Devuelve la lista de páginas nuevas escritas."""
    nuevas = []
    # nuevas ciudades
    for dept, nombres in NUEVAS.items():
        for n in nombres:
            s = slug(n)
            if s in ciudades or any(x["city"] == n for x in ciudades.values()):  # mismo nombre en otro departamento
                s = slug(f"{n} {dept}")
                n = f"{n} ({dept})"
            assert s not in ciudades, f"ciudad repetida: {s}"
            ciudades[s] = {"city": n, "dept": dept, "days": "2 a 4 días hábiles", "nueva": True}
    por_dept = {}
    for s, c in ciudades.items():
        por_dept.setdefault(c["dept"], []).append(s)

    def plant(fam, dias):
        # una ciudad de la plantilla (capital ya existente) que tenga ese tiempo de entrega y esa familia
        for cand in ("armenia", "cali", "leticia", "mocoa", "yopal", "quibdo", "florencia", "inirida", "mitu", "puerto-carreno", "san-andres"):
            c = ciudades.get(cand)
            f = OUT / f"{PREF[fam]}{cand}.html"
            if c and c["days"] == dias and f.exists():
                return {"city": c["city"], "slug": cand, "dept": c["dept"], "days": c["days"]}, f.read_text(encoding="utf-8")
        return None, None

    for s, c in sorted(ciudades.items()):
        for fam in PREF:
            destino = OUT / f"{PREF[fam]}{s}.html"
            if destino.exists():
                continue
            tp, tt = plant(fam, c["days"])
            if tp is None:
                tp, tt = plant(fam, "2 a 4 días hábiles")
            assert tp is not None, f"sin plantilla para {fam} / {c['days']}"
            vecinos = [x for x in por_dept[c["dept"]] if x != s]
            pref_tag = PREF[fam] if fam in ("agua", "cin", "qin", "ext") else PREF["agua"]
            tags = etiquetas(pref_tag, vecinos, ciudades, s)
            destino.write_text(clonar(tt, tp, {"city": c["city"], "slug": s, "dept": c["dept"], "days": c["days"]}, tags, None), encoding="utf-8")
            nuevas.append(destino.name)
    return nuevas


# ---------- cascarón del sitio ----------
class Cascaron:
    def __init__(self, OUT):
        t = (OUT / "equivalencias-codigos-filtro-samsung.html").read_text(encoding="utf-8")
        i = t.index('<div class="breadcrumb')
        j = t.index("<footer>")
        self.pre, self.post = t[:i], t[j:]
        self.pre = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', "", self.pre, flags=re.S)

    def pagina(self, nombre, titulo, desc, kw, miga, contenido, ld):
        canon = f"{DOMINIO}/{nombre}"
        pre = self.pre
        pre = re.sub(r"<title>.*?</title>", f"<title>{esc(titulo)}</title>", pre, flags=re.S)
        pre = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1) + esc(desc) + m.group(2), pre)
        pre = re.sub(r'(<meta name="keywords" content=")[^"]*(")', lambda m: m.group(1) + esc(kw) + m.group(2), pre)
        pre = re.sub(r'(<link rel="canonical" href=")[^"]*(")', lambda m: m.group(1) + canon + m.group(2), pre)
        for prop in ("og:title", "twitter:title"):
            pre = re.sub(r'(<meta (?:property|name)="' + prop + r'" content=")[^"]*(")', lambda m: m.group(1) + esc(titulo) + m.group(2), pre)
        for prop in ("og:description", "twitter:description"):
            pre = re.sub(r'(<meta (?:property|name)="' + prop + r'" content=")[^"]*(")', lambda m: m.group(1) + esc(desc) + m.group(2), pre)
        pre = re.sub(r'(<meta property="og:url" content=")[^"]*(")', lambda m: m.group(1) + canon + m.group(2), pre)
        ldh = "".join('<script type="application/ld+json">\n' + json.dumps(x, ensure_ascii=False, indent=2) + "\n</script>\n" for x in ld)
        pre = pre.replace("</head>", ldh + "</head>", 1)
        bc = ('<div class="breadcrumb wrap" style="font-family:var(--mono);font-size:12.5px;color:var(--ink-dim);padding:16px 24px 0;">'
              + " / ".join(f'<a href="{u}" style="color:var(--accent);">{esc(n)}</a>' if u else esc(n) for n, u in miga) + "</div>")
        return pre + bc + contenido + self.post


def ld_miga(miga):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, **({"item": f"{DOMINIO}/{u}"} if u else {})} for i, (n, u) in enumerate(miga)]}


def ld_faq(preg):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in preg]}


def ld_web(nombre, titulo, desc):
    return {"@context": "https://schema.org", "@type": "WebPage", "name": titulo, "url": f"{DOMINIO}/{nombre}", "inLanguage": "es-CO", "description": desc, "dateModified": HOY,
            "isPartOf": {"@id": f"{DOMINIO}/#store"}}


def hero(kicker, h1, sub):
    return f'<section class="hero"><div class="wrap"><span class="kicker">{esc(kicker)}</span><h1>{esc(h1)}</h1><p class="sub" style="margin-top:16px;">{esc(sub)}</p></div></section>'


def rapida(txt):
    return f'<section id="respuesta-rapida-guia" style="padding:0 0 12px;"><div class="wrap"><div class="qa"><p class="tag">⚡ Respuesta rápida</p><h2>Respuesta rápida</h2><p>{txt}</p></div></div></section>'


def faq_html(preg):
    return ('<section class="section" style="background:#fff;"><div class="wrap"><div class="section-head"><h2>Preguntas frecuentes</h2></div><div class="faq-num">'
            + "".join(f'<details{" open" if i == 0 else ""}><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for i, (q, a) in enumerate(preg)) + "</div></div></section>")


def tarjeta_producto(p):
    return (f'<div class="product-card" id="{p["id"]}"><div class="product-img"><img loading="lazy" src="{p["img"]}" alt="{esc(p["nombre"])}, código {esc(p["ref"])}"></div>'
            f'<h3><a href="{p["url"]}" style="color:inherit;">{esc(p["corto"])}</a></h3><span class="product-code">{esc(p["ref"])}</span><p>{esc(p["desc"])}</p>'
            f'<div class="product-footer"><span class="price-tag">{cop(p["precio"])}</span><a href="https://wa.me/{WA}?text=Hola%2C%20quiero%20el%20filtro%20Samsung%20{p["corto"].replace(" ", "%20")}" class="btn-order">Pedir</a></div>'
            f'<a href="https://checkout.wompi.co/l/{p["link"]}" target="_blank" rel="noopener noreferrer" class="btn-wompi">💳 Pagar en línea con Wompi</a>'
            f'<a href="{p["url"]}" class="btn-detalle">Ver detalles →</a></div>')


def ld_producto(p, url):
    return {"@context": "https://schema.org", "@type": "Product", "name": p["nombre"], "sku": p["ref"], "mpn": p["ref"], "image": f"{DOMINIO}/{p['img']}", "brand": {"@type": "Brand", "name": "Samsung"},
            "description": p["desc"], "category": "Filtros de agua para nevecón",
            "offers": {"@type": "Offer", "priceCurrency": "COP", "price": str(p["precio"]), "availability": "https://schema.org/InStock", "itemCondition": "https://schema.org/NewCondition", "url": url,
                       "priceValidUntil": "2027-12-31", "seller": {"@id": f"{DOMINIO}/#store"}}}


TIPO = {"cin": "cartucho redondo que se instala girando", "qin": "cartucho cuadrado que se instala empujando", "ext": "filtro externo que va en la línea de agua, fuera del nevecón"}
DESC = {"cin": "Cartucho redondo de instalación por giro, usado en muchos nevecones Samsung French Door y Side by Side (series RF y RS).",
        "qin": "Cartucho cuadrado de instalación por empuje, usado en nevecones Samsung más recientes.",
        "ext": "Filtro externo que se instala fuera del nevecón, en la línea de agua. Para equipos Samsung con sistema de filtrado externo."}
PASOS = {"cin": ["Abre la puerta del refrigerador y ubica el filtro en la parte superior derecha del compartimento.", "Gira el filtro usado un cuarto de vuelta hacia la izquierda y retíralo.",
                 "Quita la tapa protectora del filtro nuevo e insértalo girándolo hacia la derecha hasta que quede firme.", "Saca unos 6 litros de agua por el dispensador para purgar el aire y el polvo de carbón.", "Reinicia la luz del filtro."],
         "qin": ["Abre la puerta y ubica el filtro cuadrado en el compartimento.", "Presiona y suelta el filtro usado para retirarlo.", "Quita la tapa protectora del filtro nuevo e insértalo empujándolo hasta el fondo.",
                 "Saca unos 6 litros de agua por el dispensador para purgar el aire.", "Reinicia la luz del filtro."],
         "ext": ["Cierra la llave de paso del agua.", "Desconecta la manguera del filtro usado.", "Conecta el filtro nuevo respetando el sentido de la flecha del agua.", "Abre la llave y revisa que no gotee.", "Purga unos 6 litros y reinicia la luz del filtro."]}


def paginas_nuevas(OUT, productos, ciudades):
    cas = Cascaron(OUT)
    out = []
    por_ref = {}
    for k, p in productos.items():
        p.update({"id": {"cin": "haf-cin", "qin": "haf-qin", "ext": "externo"}[k], "desc": DESC[k], "tipo": TIPO[k], "k": k})

    # ---- una página por referencia / código ----
    refs = []
    for k, p in productos.items():
        for c in [p["ref"]] + [a for a in p["alias"] if a != p["ref"]]:
            refs.append((c, k))
    refs_slug = {c: "referencia-filtro-samsung-" + slug(c) + ".html" for c, _ in refs}
    for c, k in refs:
        p = productos[k]
        nombre = refs_slug[c]
        igual = [a for a in [p["ref"]] + p["alias"] if a != c]
        es_oficial = c == p["ref"]
        titulo = f"Filtro Samsung {c}: equivalencia, nevecones y precio"
        titulo = titulo if len(titulo) <= 62 else f"Filtro Samsung {c}: equivalencia y precio"
        desc = (f"El {c} {'es el código Samsung del' if es_oficial else 'equivale al'} {p['corto']} ({p['ref']}). {p['tipo'].capitalize()}. "
                f"Precio {cop(p['precio'])}, envío gratis a toda Colombia y pago en línea o contra entrega.")
        rel = (f"El <b>{esc(c)}</b> " + ("es el código con el que Samsung identifica este filtro." if es_oficial else f"es otro nombre con el que se conoce el filtro <b>{esc(p['corto'])}</b> (código Samsung {esc(p['ref'])}).")
               + f" Es un {esc(p['tipo'])}. Cuesta <b>{cop(p['precio'])}</b> con envío gratis a toda Colombia.")
        modelos = MODELOS.get(k, [])
        tabla = "".join(f"<tr><td>{esc(x)}</td><td>{'Código Samsung' if x == p['ref'] else 'Equivalente'}</td><td><a href=\"{p['url']}\">{esc(p['corto'])}</a></td></tr>" for x in [p["ref"]] + p["alias"])
        mod_h = ""
        if modelos:
            mod_h = ("<h2>Nevecones Samsung que usan este filtro</h2><p>Estos son algunos modelos que usan el filtro " + esc(p["corto"]) + ". Si el tuyo no aparece, compara el código impreso en tu filtro viejo con la tabla de arriba.</p>"
                     '<div class="pill-row">' + "".join(f'<a href="filtro-nevecon-samsung-{slug(m)}.html">{esc(m)}</a>' for m in modelos) + "</div>")
        pasos = "<h2>Cómo se instala</h2><ol>" + "".join(f"<li>{esc(x)}</li>" for x in PASOS[k]) + "</ol>"
        otros = [x for x, kk in refs if kk == k and x != c][:8]
        otros_h = ('<h2>Otros nombres de este mismo filtro</h2><div class="pill-row">' + "".join(f'<a href="{refs_slug[x]}">{esc(x)}</a>' for x in otros) + "</div>") if otros else ""
        preg = [(f"¿El {c} es lo mismo que el {p['ref']}?", (f"Sí, el {c} es el mismo filtro que el {p['ref']} ({p['corto']})." if not es_oficial else f"El {c} es el código Samsung del {p['corto']}; también se conoce como {', '.join(igual[:3])}.")),
                (f"¿Qué nevecones Samsung usan el {c}?", ("Por ejemplo " + ", ".join(modelos) + ". Si dudas, mándanos el modelo y te confirmamos.") if modelos else "Los equipos Samsung con sistema de filtrado externo en la línea de agua. Mándanos el modelo y te confirmamos."),
                (f"¿Cuánto cuesta el filtro {c}?", f"{cop(p['precio'])} COP con envío gratis a toda Colombia."),
                (f"¿Cada cuánto se cambia el filtro {c}?", "Cada 6 meses o entre 300 y 500 galones de uso, lo que ocurra primero."),
                (f"¿Puedo pagar contra entrega el {c}?", "Sí, en efectivo a la transportadora sin anticipos, o en línea con tarjeta, PSE, Nequi o Bancolombia a través de Wompi.")]
        miga = [("Inicio", "index.html"), ("Códigos y equivalencias", "equivalencias-codigos-filtro-samsung.html"), (f"Filtro Samsung {c}", None)]
        cont = (hero("Referencia · Filtro Samsung", f"Filtro Samsung {c}: equivalencia, nevecones compatibles y precio", f"Todo sobre el código {c}: a qué filtro equivale y dónde comprarlo.")
                + rapida(rel)
                + '<section class="section" style="background:#fff;"><div class="wrap"><div class="prose"><h2>Códigos equivalentes</h2><div class="tbl-wrap"><table class="spec-table cols"><tr><th>Código</th><th>Qué es</th><th>Filtro</th></tr>' + tabla + "</table></div>"
                + otros_h + mod_h + pasos + "</div></div></section>"
                + '<section class="section"><div class="wrap"><div class="section-head"><h2>Compra el filtro ' + esc(p["corto"]) + '</h2></div><div class="product-grid">' + tarjeta_producto(p) + "</div>"
                + '<p style="margin-top:18px;font-size:14.5px;">Compara con las otras referencias en la <a href="diferencia-haf-cin-haf-qin.html">guía HAF-CIN vs HAF-QIN</a>, mira las <a href="equivalencias-codigos-filtro-samsung.html">equivalencias de todos los códigos</a> '
                  'o escoge tu ciudad en <a href="filtro-agua-samsung-por-ciudad-colombia.html">envíos a toda Colombia</a>.</p></div></section>'
                + faq_html(preg))
        ld = [ld_web(nombre, titulo, desc), ld_miga(miga), ld_faq(preg), ld_producto(p, f"{DOMINIO}/{p['url']}")]
        (OUT / nombre).write_text(cas.pagina(nombre, titulo, desc, f"filtro samsung {c.lower()}, {c.lower()} equivalencia, {p['corto'].lower()}, filtro agua nevecon samsung", miga, cont, ld), encoding="utf-8")
        out.append(nombre)

    # ---- una página por modelo de nevecón ----
    for k, ms in MODELOS.items():
        p = productos[k]
        for m in ms:
            nombre = f"filtro-nevecon-samsung-{slug(m)}.html"
            titulo = f"Filtro para nevecón Samsung {m}: cuál es y precio"
            desc = f"El nevecón Samsung {m} usa el filtro {p['corto']} ({p['ref']}): {p['tipo']}. Precio {cop(p['precio'])}, envío gratis a toda Colombia y pago en línea o contra entrega."
            rapida_t = (f"El nevecón Samsung <b>{esc(m)}</b> usa el filtro de agua <b>{esc(p['corto'])}</b> (código {esc(p['ref'])}), un {esc(p['tipo'])}. "
                        f"Cuesta <b>{cop(p['precio'])}</b> con envío gratis y se cambia cada 6 meses.")
            otros_m = [x for x in ms if x != m]
            preg = [(f"¿Qué filtro de agua usa la nevera Samsung {m}?", f"Usa el {p['corto']} (código {p['ref']}), equivalente a {', '.join(p['alias'][:3])}."),
                    (f"¿Cada cuánto se cambia el filtro de la {m}?", "Cada 6 meses, o antes si el agua sale con sabor extraño o el dispensador entrega menos agua."),
                    (f"¿Dónde está el filtro en la {m}?", "En el compartimento del refrigerador, " + ("en la parte superior derecha; se gira un cuarto de vuelta para sacarlo." if k == "cin" else "se retira presionándolo y se instala empujando hasta el fondo.")),
                    (f"¿Cuánto cuesta el filtro para la {m}?", f"{cop(p['precio'])} COP con envío gratis a toda Colombia."),
                    (f"¿Puedo pagar contra entrega el filtro de la {m}?", "Sí, en efectivo a la transportadora sin anticipos, o en línea con Wompi.")]
            miga = [("Inicio", "index.html"), ("Filtros Samsung", "index.html#catalogo"), (f"Nevecón Samsung {m}", None)]
            cont = (hero("Nevecón Samsung · " + m, f"Filtro de agua para el nevecón Samsung {m}", f"Qué filtro usa, cómo cambiarlo y dónde comprarlo con envío a toda Colombia.")
                    + rapida(rapida_t)
                    + '<section class="section" style="background:#fff;"><div class="wrap"><div class="prose"><h2>Datos del filtro para la ' + esc(m) + '</h2><div class="tbl-wrap"><table class="spec-table"><tr><th>Filtro</th><td><a href="' + p["url"] + '">' + esc(p["nombre"]) + '</a></td></tr>'
                    f'<tr><th>Código Samsung</th><td>{esc(p["ref"])}</td></tr><tr><th>También aparece como</th><td>{esc(", ".join(p["alias"]))}</td></tr><tr><th>Tipo</th><td>{esc(p["tipo"].capitalize())}</td></tr>'
                    f'<tr><th>Precio</th><td>{cop(p["precio"])} COP con envío gratis</td></tr><tr><th>Cambio</th><td>Cada 6 meses</td></tr></table></div>'
                    f'<h2>Cómo cambiar el filtro de tu {esc(m)}</h2><ol>' + "".join(f"<li>{esc(x)}</li>" for x in PASOS[k]) + "</ol>"
                    '<p>Guías útiles: <a href="cambiar-filtro-agua-nevecon-samsung.html">cómo cambiar el filtro</a> · <a href="reiniciar-luz-filtro-nevecon-samsung.html">reiniciar la luz del filtro</a> · <a href="cada-cuanto-cambiar-filtro-agua-samsung.html">cada cuánto cambiarlo</a>.</p>'
                    + ("<h2>Otros nevecones que usan el mismo filtro</h2><div class=\"pill-row\">" + "".join(f'<a href="filtro-nevecon-samsung-{slug(x)}.html">{esc(x)}</a>' for x in otros_m) + "</div>") + "</div></div></section>"
                    + '<section class="section"><div class="wrap"><div class="section-head"><h2>Compra el filtro de tu ' + esc(m) + '</h2></div><div class="product-grid">' + tarjeta_producto(p) + "</div>"
                    '<p style="margin-top:18px;font-size:14.5px;">¿Tu nevecón no es este modelo? Mira <a href="como-identificar-filtro-samsung.html">cómo identificar tu filtro</a> o escoge tu ciudad en <a href="filtro-agua-samsung-por-ciudad-colombia.html">envíos a toda Colombia</a>.</p></div></section>'
                    + faq_html(preg))
            ld = [ld_web(nombre, titulo, desc), ld_miga(miga), ld_faq(preg), ld_producto(p, f"{DOMINIO}/{p['url']}")]
            (OUT / nombre).write_text(cas.pagina(nombre, titulo, desc, f"filtro nevecon samsung {m.lower()}, filtro agua {m.lower()}, {p['ref'].lower()} {m.lower()}, filtro nevera samsung {m.lower()}", miga, cont, ld), encoding="utf-8")
            out.append(nombre)

    # ---- una página por departamento ----
    depts = {}
    for s, c in ciudades.items():
        depts.setdefault(c["dept"], []).append((c["city"], s, c["days"]))
    for d, cs in sorted(depts.items()):
        nombre = f"filtros-samsung-{slug(d)}.html"
        cs.sort()
        dias = sorted({x[2].split(" (")[0] for x in cs})
        titulo = f"Filtro de agua Samsung en {d}: envío y precios"
        titulo = titulo if len(titulo) <= 62 else f"Filtro de agua Samsung en {d}: envío"
        desc = f"Compra filtros de agua Samsung HAF-CIN, HAF-QIN y externo con envío gratis en {d}: {len(cs)} {'ciudad' if len(cs) == 1 else 'ciudades'} con tiempos de entrega, precios y pago contra entrega o en línea."
        preg = [(f"¿Envían filtros de agua Samsung a {d}?", f"Sí, enviamos gratis a {len(cs)} {'ciudad' if len(cs) == 1 else 'ciudades'} de {d} y a otros municipios del departamento."),
                (f"¿Cuánto tarda el envío a {d}?", "Entre " + " y ".join(dias[:1] + dias[-1:]) if len(dias) > 1 else f"Estimamos {dias[0]}."),
                (f"¿Cuánto cuesta el filtro Samsung en {d}?", "$139.900 COP el HAF-CIN/EXP y el HAF-QIN/EXP, y $79.900 COP el filtro externo DA29-10105J, con envío gratis."),
                (f"¿Puedo pagar contra entrega en {d}?", "Sí, en efectivo a la transportadora sin anticipos, o en línea con tarjeta, PSE, Nequi o Bancolombia.")]
        if len(dias) > 1:
            preg[1] = (preg[1][0], f"Entre {dias[0]} y {dias[-1]}, según la ciudad, con guía de rastreo.")
        miga = [("Inicio", "index.html"), ("Todas las ciudades", "filtro-agua-samsung-por-ciudad-colombia.html"), (f"Filtros Samsung en {d}", None)]
        filas = "".join(f'<tr><td><a href="filtro-agua-samsung-{s}.html">{esc(c)}</a></td><td>{esc(dd)}</td><td><a href="cambiar-filtro-nevecon-samsung-{s}.html">Cambiar el filtro</a> · <a href="precio-filtro-nevecon-samsung-{s}.html">Precio</a></td></tr>' for c, s, dd in cs)
        cont = (hero(f"Cobertura · {d}", f"Filtros de agua Samsung en {d}", f"Envío gratis a {len(cs)} {'ciudad' if len(cs) == 1 else 'ciudades'} de {d}, con pago en línea o contra entrega.")
                + rapida(f"Vendemos los filtros de agua Samsung <b>HAF-CIN/EXP</b> y <b>HAF-QIN/EXP</b> ($139.900) y el <b>filtro externo DA29-10105J</b> ($79.900) con envío gratis en {esc(d)}. Escoge tu ciudad para ver el tiempo de entrega.")
                + '<section class="section" style="background:#fff;"><div class="wrap"><div class="prose"><h2>Ciudades de ' + esc(d) + ' con envío</h2><div class="tbl-wrap"><table class="spec-table cols"><tr><th>Ciudad</th><th>Entrega estimada</th><th>Más</th></tr>' + filas + "</table></div>"
                + '<h2>Precios de los filtros Samsung</h2><div class="tbl-wrap"><table class="spec-table cols"><tr><th>Filtro</th><th>Código</th><th>Precio</th></tr>'
                + "".join(f'<tr><td><a href="{p["url"]}">{esc(p["corto"])}</a></td><td>{esc(p["ref"])}</td><td>{cop(p["precio"])}</td></tr>' for p in productos.values()) + "</table></div>"
                + '<p>¿Tu municipio no está en la lista? También enviamos a otros lugares de ' + esc(d) + '; escríbenos tu ciudad y confirmamos el tiempo de entrega. Mira <a href="filtro-agua-samsung-por-ciudad-colombia.html">todas las ciudades de Colombia</a>.</p></div></div></section>'
                + faq_html(preg))
        ld = [ld_web(nombre, titulo, desc), ld_miga(miga), ld_faq(preg)]
        (OUT / nombre).write_text(cas.pagina(nombre, titulo, desc, f"filtro agua samsung {d.lower()}, filtro nevecon samsung {d.lower()}, comprar filtro samsung {d.lower()}", miga, cont, ld), encoding="utf-8")
        out.append(nombre)
    return out, refs_slug, depts


def actualizar_hub(OUT, ciudades):
    f = OUT / "filtro-agua-samsung-por-ciudad-colombia.html"
    t = f.read_text(encoding="utf-8")
    i = t.index("<h2>Elige tu ciudad</h2>")
    j = t.index("</section>", i)
    cierre = "</div></div>"
    por = {}
    for s, c in ciudades.items():
        por.setdefault(c["dept"], []).append((c["city"], s, c["days"].split(" (")[0]))
    cuerpo = (f"<h2>Elige tu ciudad</h2><p>Enviamos a todo el país. Estas son las {len(ciudades)} ciudades con página propia, agrupadas por departamento, con los tiempos estimados de entrega:</p>")
    for d in sorted(por):
        cuerpo += f'<h2><a href="filtros-samsung-{slug(d)}.html" style="color:inherit;">{esc(d)}</a></h2><div class="link-grid">' + "".join(
            f'<a href="filtro-agua-samsung-{s}.html">{esc(c)}<small>Entrega estimada: {esc(dd)}</small></a>' for c, s, dd in sorted(por[d])) + "</div>"
    t = t[:i] + cuerpo + cierre + t[j:]
    t = t.replace("más de 100 ciudades", f"más de {len(ciudades)} ciudades")
    f.write_text(t, encoding="utf-8")


def enlaces_internos(OUT, productos, refs_slug, depts):
    """Bloque de enlaces (referencias, modelos y departamentos) en la portada, las fichas y las guías: reparte la fuerza entre las páginas nuevas."""
    refs = "".join(f'<a href="{u}">{esc(c)}</a>' for c, u in refs_slug.items())
    mods = "".join(f'<a href="filtro-nevecon-samsung-{slug(m)}.html">{esc(m)}</a>' for ms in MODELOS.values() for m in ms)
    deps = "".join(f'<a href="filtros-samsung-{slug(d)}.html">{esc(d)}</a>' for d in sorted(depts))
    bloque = ('<section class="section" id="mas-filtros" style="background:#fff;"><div class="wrap"><div class="section-head"><h2>Busca tu filtro por código, modelo o departamento</h2></div>'
              '<h3 style="margin:10px 0 6px;font-size:16px;">Códigos y referencias</h3><div class="pill-row">' + refs + '</div>'
              '<h3 style="margin:18px 0 6px;font-size:16px;">Modelos de nevecón Samsung</h3><div class="pill-row">' + mods + '</div>'
              '<h3 style="margin:18px 0 6px;font-size:16px;">Envíos por departamento</h3><div class="pill-row">' + deps + '</div></div></section>')
    n = 0
    for nombre in ("index.html", "filtro-haf-cin.html", "filtro-haf-qin.html", "filtro-externo.html", "equivalencias-codigos-filtro-samsung.html", "guias-filtro-agua-nevecon-samsung.html",
                   "filtro-agua-samsung-por-ciudad-colombia.html", "como-identificar-filtro-samsung.html"):
        f = OUT / nombre
        t = f.read_text(encoding="utf-8")
        if 'id="mas-filtros"' in t or "<footer>" not in t:
            continue
        f.write_text(t.replace("<footer>", bloque + "<footer>", 1), encoding="utf-8")
        n += 1
    return n
