# Páginas de la tienda de repuestos de línea blanca. Se ejecuta dentro de ads_rp.py (comparte sus funciones y datos).
FPAGO = "Pagas en línea con Wompi (tarjeta, PSE, Nequi o Bancolombia) o contra entrega, en efectivo, sin recargo."
R_EQ = lambda eq: f"repuestos-para-{slug(eq)}.html"
R_CAT = lambda eq, cat: f"{slug(cat)}-para-{slug(eq)}.html"
R_EQM = lambda eq, m: f"repuestos-para-{slug(eq)}-{slug(m)}.html"
EQ_LISTA = list(EQUIPOS)
PREG_PV = {}


def galeria_html(p):
    return '<div class="gal" data-gal><div class="gal-main"><img decoding="async" src="' + p["img"] + '" alt="' + esc(p["nombre"]) + '" width="520" height="520"></div></div>'


def wa_pieza(p):
    return f"https://wa.me/{WA}?text=" + __import__("urllib.parse").parse.quote(f"Hola, quiero información de: {p['nombre']}" + (f" (ref. {p['ref']})" if p["ref"] != p["sku"] else "") + ". Mi modelo de equipo es: ")


# ---------------------------------------------------------------- buscador del encabezado
ARTS_BASE = [("Cómo elegir el repuesto de tu lavadora", "como-elegir-repuesto-para-lavadora.html"), ("Cómo encontrar el modelo de tu electrodoméstico", "como-encontrar-el-modelo-de-tu-electrodomestico.html"),
             ("Preguntas frecuentes", "preguntas-frecuentes-repuestos.html"), ("Envíos y pagos", "envios-y-pagos.html"), ("Garantía, cambio y devolución", "garantia-cambio-y-devolucion.html")]
items = [[p["nombre"], p["url"], "Repuesto", cop(p["precio"]) if p["precio"] else "consultar precio"] for p in PS]
items += [[f"Repuestos para {eq.lower()}", R_EQ(eq), "Equipo", ""] for eq in EQ_LISTA]
items += [[f"{cat} para {eq.lower()}", R_CAT(eq, cat), "Tipo de pieza", ""] for eq, cs in EQUIPOS.items() for cat in cs]
items += [[f"Repuestos {m}", f"marca-{slug(m)}.html", "Marca", ""] for m in MARCAS_EQ]
items += [[t, u, "Guía", ""] for t, u in ARTS_BASE]
js = ("(function(){var D=" + json.dumps(items, ensure_ascii=False, separators=(",", ":")) + ";"
      "function n(s){return s.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').replace(/[^a-z0-9 ]+/g,' ').trim()}var X=D.map(function(r){return n(r[0]+' '+r[2]+' '+r[3])});"
      "function buscar(q){q=n(q);if(!q)return[];var t=q.split(/ +/),o=[];for(var i=0;i<D.length;i++){var ok=true,sc=0;for(var j=0;j<t.length;j++){var p=X[i].indexOf(t[j]);if(p<0){ok=false;break}sc+=p===0?0:1}"
      "if(ok){var e=n(D[i][0]);o.push([sc+(e.indexOf(q)===0?-2:0),i])}}o.sort(function(a,b){return a[0]-b[0]});return o.slice(0,12).map(function(x){return D[x[1]]})}"
      "function pintar(caja,r,q){if(!q.trim()){caja.hidden=true;return}var g={},h='';r.forEach(function(x){(g[x[2]]=g[x[2]]||[]).push(x)});Object.keys(g).forEach(function(k){h+='<h6>'+k+'</h6>'+g[k].map(function(x){return '<a href=\"'+x[1]+'\"><span>'+x[0]+'</span><small>'+x[3]+'</small></a>'}).join('')});"
      "caja.innerHTML=h||'<p>No encontramos «'+q.replace(/</g,'')+'». Prueba con manguera, presostato o protector.</p>';caja.hidden=false}"
      "document.querySelectorAll('[data-aq-q]').forEach(function(i){var c=i.parentNode.querySelector('.aq-res');i.addEventListener('input',function(){pintar(c,buscar(i.value),i.value)});i.addEventListener('focus',function(){if(i.value)pintar(c,buscar(i.value),i.value)});"
      "i.addEventListener('keydown',function(e){if(e.key==='Enter'){var a=c.querySelector('a');if(a)location.href=a.getAttribute('href')}if(e.key==='Escape')c.hidden=true})});"
      "document.addEventListener('click',function(e){document.querySelectorAll('.aq-res').forEach(function(c){if(!c.parentNode.contains(e.target))c.hidden=true});document.querySelectorAll('.aq-nav details[open]').forEach(function(d){if(!d.contains(e.target))d.removeAttribute('open')})});})();")
(OUT / "buscar.js").write_text(js, encoding="utf-8")

# partes.php y páginas PHP de compra
_src_lg = open(AQUI / "ads_lg_paginas.py", encoding="utf-8").read()
_partes = _src_lg.split('(OUT / "partes.php").write_text(r"""')[1].split('""".replace("__AQH__"')[0].replace("/img/icono-lg.png", "/img/icono-bm.png")
(OUT / "partes.php").write_text(_partes.replace("__AQH__", encabezado()).replace("__AQF__", pie()), encoding="utf-8")
_c = (OUT / "carrito.php").read_text(encoding="utf-8")
_c = re.sub(r'Busca el filtro de tu nevecón por la referencia o por[^<]*', 'Elige los repuestos que necesitas para tu lavadora o tu nevera.', _c)
_c = re.sub(r'(<label)([^>]*>(?:(?!</label>).)*Recuérdame por correo cuando toque cambiar el filtro)', r'\1 hidden\2', _c, flags=re.S)
_c = _c.replace('${n === 1 ? "filtro" : "filtros"}', '${n === 1 ? "repuesto" : "repuestos"}').replace('Modelo del nevecón <i>(opcional)</i>', 'Modelo de tu equipo <i>(opcional)</i>').replace('Nos ayuda a confirmar que le sirve', 'Ej.: WA13J5710SG o RT38K5930S8')
_c = _c.replace('Ver todos los filtros', 'Ver los repuestos').replace('href="/tienda/"', 'href="/index.html#repuestos"')
(OUT / "carrito.php").write_text(_c, encoding="utf-8")
_pv = (OUT / "privacidad.php").read_text(encoding="utf-8")
(OUT / "privacidad.php").write_text(re.sub(r'<li>[^<]*enviarte un correo cuando toque cambiar el filtro[^<]*</li>', '', _pv), encoding="utf-8")
_legal = lambda titulo, desc, ruta, cuerpo: ("<?php require __DIR__ . '/partes.php'; $n = cfg()['negocio']; cabeza('" + titulo + " | ' . $n['nombre'], '" + desc + "', '/" + ruta + "'); ?>\n<article class=\"legal\">\n" + cuerpo + "\n</article>\n<?php pie(); ?>\n")
(OUT / "terminos.php").write_text(_legal("Términos y condiciones", "Términos y condiciones de compra, envíos, garantía y derecho de retracto.", "terminos.php",
    "<h1>Términos y condiciones</h1><p class=\"m\">Ley 1480 de 2011 (Estatuto del Consumidor).</p>"
    "<h2>1. Quiénes somos</h2><p><?= identificacion() ?> WhatsApp y teléfono: <?= h($n['telefono']) ?>. Correo: <?= h($n['correo']) ?>.</p>"
    "<h2>2. Cómo se compra</h2><p>Escoges el repuesto, escribes tus datos de entrega y pagas en línea con Wompi (tarjeta, PSE, Nequi o Bancolombia) o contra entrega, en efectivo, sin recargo.</p>"
    "<h2>3. Precios</h2><p>Están en pesos colombianos y son el valor total a pagar, con el envío incluido en los productos que lo indican. No hay cobros adicionales.</p>"
    "<h2>4. Antes de comprar, confirma la compatibilidad</h2><p>Compara el modelo o la referencia de tu equipo con los de la ficha. Las fotos son de referencia. Si tienes dudas, escríbenos con el modelo de tu equipo antes de comprar.</p>"
    "<h2>5. Entregas</h2><p>Enviamos a toda Colombia por transportadora. Los tiempos son estimados y se informan al confirmar el pedido.</p>"
    "<h2 id=\"garantia\">6. Garantía</h2><p>Todos los productos tienen la garantía legal de la Ley 1480 de 2011. Más detalle en <a href=\"/garantia-y-retracto.php\">Garantía y retracto</a>.</p>"
    "<h2>7. Derecho de retracto</h2><p>Como es una compra a distancia, tienes <b>5 días hábiles desde que recibes el producto</b> para retractarte, sin dar explicaciones. El producto debe estar sin usar ni instalar y en su empaque.</p>"
    "<h2>8. Marcas</h2><p>Los nombres de marcas de electrodomésticos se usan solo para indicar compatibilidad. <?= h($n['nombre']) ?> es un comercio independiente; no tiene afiliación con los fabricantes.</p>"
    "<h2>9. Peticiones, quejas y reclamos</h2><p>Escríbenos a <?= h($n['correo']) ?>. Respondemos en máximo 15 días hábiles. También puedes acudir a la <a href=\"https://www.sic.gov.co\" rel=\"noopener\">Superintendencia de Industria y Comercio</a>.</p>"), encoding="utf-8")
(OUT / "garantia-y-retracto.php").write_text(_legal("Garantía y retracto", "Garantía legal, cambio y derecho de retracto de 5 días hábiles.", "garantia-y-retracto.php",
    "<h1>Garantía y retracto</h1><h2>Derecho de retracto</h2><p>Tienes 5 días hábiles desde la entrega para retractarte si el producto está sin usar ni instalar y en su empaque. Escríbenos a <?= h($n['correo']) ?> o al WhatsApp <?= h($n['telefono']) ?>.</p>"
    "<h2>Garantía</h2><p>Los productos tienen la garantía legal de la Ley 1480 de 2011. Si llega defectuoso o no es el que pediste, lo cambiamos.</p><h2>Cómo pedir un cambio</h2><p>Escríbenos con tu número de pedido y una foto del producto.</p>"), encoding="utf-8")
(OUT / "opinion.php").unlink(missing_ok=True)

# ---------------------------------------------------------------- portada
def conteo(eq): return sum(len(v) for v in EQUIPOS[eq].values())
_c1 = next((p for p in PS if p["equipo"] == "Lavadoras" and p["categoria"].startswith("Mangueras de entrada")), None)
_c2 = next((p for p in PS if p["categoria"] == "Presostatos"), None)
_c3 = next((p for p in PS if p["sku"] == "PV-BM-NEV"), None)
dest = [x for x in (_c1, _c2, _c3) if x] or PS[:3]
dest = (dest + [x for x in PS if x not in dest])[:3]
stage = ('<div class="aq-stage"><i></i><i></i><i></i><i></i>' + "".join(f'<a class="s{i + 1}" href="{p["url"]}" aria-label="{esc(p["nombre"])}"><img src="{p["img"]}" alt="{esc(p["nombre"])}" width="300" height="300" {"loading=eager" if i == 0 else "loading=lazy"}></a>' for i, p in enumerate(dest))
         + '<span class="aq-price-tag">Repuestos para lavadoras y neveras · envío a toda Colombia</span></div>')
hero = ('<section class="aq-hero" id="inicio"><div class="wrap"><div><span class="kicker">Lavadoras · Neveras · Toda Colombia</span><h1>Repuestos de línea blanca para tu lavadora y tu nevera</h1>'
        '<p class="lead">Elige tu equipo, la marca y la pieza. Cada repuesto trae foto, precio y compatibilidad, y pagas en línea o contra entrega. Si no sabes cuál necesitas, escríbenos con el modelo de tu equipo.</p>'
        '<div class="aq-trust"><span>Envío a toda Colombia</span><span>Pago seguro Wompi</span><span>Contra entrega</span><span>5 días de retracto</span></div></div>' + stage + '</div></section>')
tiles_eq = "".join(f'<a class="aq-tile" href="{R_EQ(eq)}"><b>Repuestos para {esc(eq.lower())}</b><p>{conteo(eq)} repuesto{"s" if conteo(eq) > 1 else ""}: {esc(", ".join(c.lower() for c in EQUIPOS[eq]))}.</p></a>' for eq in EQ_LISTA)
sec_eq = seccion("Compra por equipo", f'<div class="aq-tiles">{tiles_eq}</div>', sub="Elige tu electrodoméstico y mira solo lo que le sirve.")
estante = seccion("Repuestos disponibles", '<div class="tf-grid">' + "".join(tarjeta(p) for p in PS[:6]) + "</div>").replace('<section class="aq-sec">', '<section class="aq-sec estante-top" id="repuestos">', 1)
cats = [(eq, c, len(v)) for eq, cs in EQUIPOS.items() for c, v in cs.items()]
sec_cat = seccion("Busca por tipo de pieza", '<div class="city-tags">' + "".join(f'<a href="{R_CAT(eq, c)}">{esc(c)} para {esc(eq.lower())} ({n})</a>' for eq, c, n in cats) + "</div>", alt=True)
sec_marca = seccion("Repuestos por marca de electrodoméstico", '<div class="city-tags">' + "".join(f'<a href="marca-{slug(m)}.html">Repuestos {esc(m)}</a>' for m in MARCAS_EQ) + "</div><p class=\"note\" style=\"margin-top:14px\">¿No ves tu marca? Escríbenos con el modelo y te decimos si tenemos la pieza.</p>")
qa_home = qa("¿Dónde comprar repuestos para lavadoras y neveras en Colombia?",
             f"Aquí encuentras mangueras de entrada y de desagüe, presostatos y protectores de voltaje para lavadoras y neveras, con foto, precio y compatibilidad. Pagas en línea con Wompi o contra entrega y enviamos a toda Colombia. "
             "Si no estás seguro de cuál es tu pieza, escríbenos por WhatsApp con el modelo de tu equipo.", [("Equipos", "Lavadoras y neveras"), ("Pago", "Wompi o contra entrega"), ("Envío", "Toda Colombia"), ("Retracto", "5 días hábiles")])
tiles = [("caja", "Envío a toda Colombia", "Por transportadora, con confirmación por correo y WhatsApp."), ("candado", "Pago seguro", "Wompi (Bancolombia): tarjeta, PSE, Nequi o botón Bancolombia."),
         ("efectivo", "Contra entrega", "Paga en efectivo cuando recibas tu pedido, sin recargo."), ("retorno", "5 días de retracto", "Si no es lo que necesitas, lo cambiamos (sin usar y en su empaque).")]
confianza = seccion("Compra tranquilo", '<div class="aq-tiles">' + "".join(f'<div class="aq-tile">{ICONOS[i]}<b>{esc(t)}</b><p>{esc(d)}</p></div>' for i, t, d in tiles) + "</div>", sub="Una tienda en línea como las grandes: carrito, pago seguro y confirmación por correo.")
pasos = '<ol class="vl"><li><b>Elige tu equipo</b> (lavadora o nevera) y la pieza que necesitas.</li><li><b>Confirma la compatibilidad</b> con el modelo de tu equipo; si dudas, escríbenos.</li><li><b>Agrégala al carrito</b> y paga en línea o contra entrega.</li><li><b>Recíbela</b> en tu casa y cámbiala o instálala.</li></ol>'
FAQ_HOME = [("¿Cómo sé qué repuesto necesita mi lavadora?", "Mira el modelo en la etiqueta de tu equipo y la descripción de la pieza. Si dudas, escríbenos con el modelo y una foto de la pieza."),
            ("¿Cómo pago?", FPAGO), ("¿Hacen envíos a toda Colombia?", "Sí, por transportadora. El tiempo de entrega se confirma al hacer el pedido."), ("¿Los productos son nuevos?", "Sí, nuevos y en su empaque."),
            ("¿Hay retracto?", "Sí, 5 días hábiles desde la entrega, con el producto sin usar ni instalar y en su empaque.")]
ld_home = [{"@type": "ItemList", "name": "Repuestos de línea blanca", "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": ld_producto(p)} for i, p in enumerate(PS)]}]
pagina("index.html", "Repuestos de Línea Blanca | Lavadoras y Neveras | Envío a Colombia", "Repuestos para lavadoras y neveras: mangueras, presostatos y protectores de voltaje con foto, precio y compatibilidad. Paga con Wompi o contra entrega. Envío a toda Colombia.",
       "repuestos linea blanca, repuestos lavadoras, repuestos neveras, mangueras lavadora, presostato lavadora, protector de voltaje, repuestos contra entrega, comprar repuestos lavadora",
       [("Inicio", None)], hero + sec_eq.replace('<div class="aq-tiles">','<div class="aq-tiles eqt">') + estante + sec_cat + sec_marca + qa_home + confianza + seccion("Cómo comprar en 4 pasos", pasos, alt=True) + faq_html(FAQ_HOME), FAQ_HOME, ld_home, prio="1.0", og=dest[0]["img"])

# ---------------------------------------------------------------- páginas por equipo, tipo de pieza y marca
def filtros_html(eq):
    cs = EQUIPOS[eq]
    marcas = sorted({p["marca_eq"] for c in cs.values() for p in c if p["marca_eq"] != "Todas las marcas"})
    return ('<div class="city-tags"><b>Tipo de pieza:</b> ' + "".join(f'<a href="{R_CAT(eq, c)}">{esc(c)} ({len(v)})</a>' for c, v in cs.items()) + "</div>"
            + ('<div class="city-tags" style="margin-top:10px"><b>Marca:</b> ' + "".join(f'<a href="{R_EQM(eq, m)}">{esc(m)}</a>' for m in marcas) + "</div>" if marcas else ""))


def pag_lista(nombre, titulo, desc, kw, h1, lista, extra="", miga=None, faq=()):
    cuerpo = (hero_simple("Repuestos de línea blanca", h1, desc) + seccion(h1, extra + '<div class="tf-grid">' + "".join(tarjeta(p) for p in lista) + "</div>")
              + (faq_html(list(faq)) if faq else ""))
    ld = [{"@type": "ItemList", "name": h1, "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{DOMINIO}/{p['url']}", "name": p["nombre"]} for i, p in enumerate(lista)]}]
    pagina(nombre, titulo, desc, kw, miga or [("Inicio", "index.html"), (h1, None)], cuerpo, faq, ld, prio="0.8", og=lista[0]["img"])


for eq, cs in EQUIPOS.items():
    todos = [p for v in cs.values() for p in v]
    pag_lista(R_EQ(eq), f"Repuestos para {eq} | Mangueras, Presostatos y más", f"Repuestos para {eq.lower()}: " + ", ".join(c.lower() for c in cs) + f". {len(todos)} producto(s) con foto, compatibilidad y pago contra entrega.",
              f"repuestos para {eq.lower()}, repuestos {eq.lower()} colombia, comprar repuestos {eq.lower()}", f"Repuestos para {eq.lower()}", todos, filtros_html(eq))
    for c, v in cs.items():
        pag_lista(R_CAT(eq, c), f"{c} para {eq} | Precio y compatibilidad", f"{c} para {eq.lower()}: " + ", ".join(p["nombre"] for p in v[:3]) + ". Con foto, precio y pago contra entrega.",
                  f"{c.lower()} para {eq.lower()}, comprar {c.lower()}, {c.lower()} {eq.lower()} precio", f"{c} para {eq.lower()}", v, "", [("Inicio", "index.html"), (f"Repuestos para {eq.lower()}", R_EQ(eq)), (c, None)])
    marcas = sorted({p["marca_eq"] for p in todos if p["marca_eq"] != "Todas las marcas"})
    for m in marcas:
        v = [p for p in todos if p["marca_eq"] == m]
        pag_lista(R_EQM(eq, m), f"Repuestos para {eq} {m} | Compatibles", f"Repuestos para {eq.lower()} {m}: " + ", ".join(p["nombre"] for p in v[:3]) + ".", f"repuestos {eq.lower()} {m.lower()}, {m.lower()} {eq.lower()} repuestos", f"Repuestos para {eq.lower()} {m}", v, "",
                  [("Inicio", "index.html"), (f"Repuestos para {eq.lower()}", R_EQ(eq)), (m, None)])
for m in MARCAS_EQ:
    v = [p for p in PS if p["marca_eq"] == m]
    pag_lista(f"marca-{slug(m)}.html", f"Repuestos {m} | Lavadoras y Neveras", f"Repuestos compatibles con electrodomésticos {m}: " + ", ".join(p["nombre"] for p in v[:3]) + ". Foto, precio y compatibilidad.", f"repuestos {m.lower()}, repuestos para {m.lower()}", f"Repuestos {m}", v,
              "", [("Inicio", "index.html"), (f"Repuestos {m}", None)])

# ---------------------------------------------------------------- fichas de producto
for p in PS:
    otros = [x for x in PS if x is not p and x["equipo"] == p["equipo"]][:3]
    pv = p["espec"]
    if p["precio"]:
        precio_t = f"Cuesta <b>{cop2(p['precio'])}</b>" + (" con envío gratis a toda Colombia." if True else ".")
    else:
        precio_t = "Escríbenos por WhatsApp para confirmar el precio y la disponibilidad."
    compat = (f"Sirve para {', '.join(p['modelos'])}." if p["modelos"] else (f"Es compatible con lavadoras {p['marca_eq']}; confirma tu modelo por WhatsApp antes de comprar." if p["marca_eq"] not in ("", "Todas las marcas") else "Sirve para lavadoras de varias marcas; confirma con la descripción o escríbenos con el modelo."))
    qa_p = qa(f"{p['nombre']}: ¿qué es y para qué sirve?", f"{esc(p['resumen'])} {esc(compat)} {precio_t}",
              [("Tipo", p["categoria"]), ("Equipo", p["equipo"]), ("Marca", p["marca_eq"] if p["marca_eq"] != "Todas las marcas" else "Varias"), ("Precio", cop(p["precio"]) if p["precio"] else "Consultar")])
    filas = [("Tipo de pieza", p["categoria"]), ("Para", p["equipo"]), ("Marca del equipo", p["marca_eq"] or "Varias marcas")]
    if p["marca_prod"] and not p["marca_prod"].startswith("PENDIENTE"):
        filas.append(("Marca del producto", p["marca_prod"]))
    if p["ref"] != p["sku"]:
        filas.append(("Referencia", p["ref"]))
    if pv:
        filas += [("Voltaje", "110 VAC · 50/60 Hz"), ("Corriente máxima", f"{pv[0]} A (aprox. {pv[0] * 110:,} W)".replace(",", ".")), ("Tomas", str(pv[1])), ("Ciclo de espera", pv[2])]
    filas += [("Modelos compatibles", ", ".join(p["modelos"]) or "Confirma tu modelo por WhatsApp"), ("Precio", cop2(p["precio"]) + " COP" if p["precio"] else "Consultar por WhatsApp"), ("Pago", "Wompi (tarjeta, PSE, Nequi, Bancolombia) o contra entrega")]
    ficha = '<div class="tbl-wrap"><table class="spec-table">' + "".join(f"<tr><th>{esc(a)}</th><td>{esc(b)}</td></tr>" for a, b in filas) + "</table></div>"
    preg = [("¿Cómo sé si esta pieza sirve para mi equipo?", "Compara el modelo de tu equipo y la descripción de la pieza. Si no estás seguro, escríbenos por WhatsApp con el modelo y una foto de la pieza vieja."),
            ("¿Puedo pagar contra entrega?", FPAGO), ("¿Hacen envíos a toda Colombia?", "Sí, por transportadora; el tiempo se confirma al hacer el pedido."), ("¿Hay retracto?", "Sí, 5 días hábiles desde la entrega, con el producto sin usar ni instalar.")]
    if pv:
        preg.append(("¿Sirve para equipos de 220 V?", "No. Este protector es de 110 VAC."))
    botones = ('<button type="button" class="btn btn-solid" data-add="' + p["id"] + '">🛒 Agregar al carrito</button><button type="button" class="btn" data-add="' + p["id"] + '" data-ir="1">Comprar ahora</button>') if p["precio"] else f'<a class="btn btn-solid" href="{wa_pieza(p)}" rel="noopener">Consultar precio por WhatsApp</a>'
    cuerpo = (f'<section class="hero hero-prod"><div class="wrap hero-grid"><div><span class="kicker">{esc(p["categoria"])} · {esc(p["equipo"])}</span><h1>{esc(p["nombre"])}</h1>'
              f'<p class="sub" style="margin-top:16px;">{esc(p["resumen"])}</p>' + (f'<div class="hero-price">{cop(p["precio"])} <small>COP · envío gratis</small></div>' if p["precio"] else '<div class="hero-price" style="font-size:1.6rem">Consulta el precio</div>')
              + f'<div class="hero-cta">{botones}</div><p class="sub" style="margin-top:14px"><a href="{wa_pieza(p)}" rel="noopener">¿Dudas con tu modelo? Escríbenos →</a></p></div>{galeria_html(p)}</div></section>'
              + qa_p + seccion("Especificaciones", ficha) + faq_html(preg) + (seccion("Otros repuestos para " + p["equipo"].lower(), '<div class="tf-grid">' + "".join(tarjeta(x) for x in otros) + "</div>", alt=True) if otros else ""))
    pagina(p["url"], f"{p['nombre']}" + (f" | {cop(p['precio'])}" if p["precio"] else " | Consulta el precio"), f"{p['nombre']}: {p['resumen'][:90].rstrip('. ')}. " + (f"{cop(p['precio'])}, envío gratis y pago contra entrega." if p["precio"] else "Consulta el precio por WhatsApp."),
           f"{p['nombre'].lower()}, {p['categoria'].lower()} {p['equipo'].lower()}, comprar {p['categoria'].lower()}", [("Inicio", "index.html"), (f"Repuestos para {p['equipo'].lower()}", R_EQ(p["equipo"])), (p["nombre"], None)], cuerpo, preg, [ld_producto(p)], prio="0.9", og=p["img"])

# ---------------------------------------------------------------- guías y páginas de ayuda
def pag_info(nombre, titulo, desc, kw, h1, cuerpo, preg=(), prio="0.6"):
    c = hero_simple("Repuestos de línea blanca", h1, desc) + cuerpo + (faq_html(list(preg)) if preg else "") + seccion("Repuestos disponibles", '<div class="tf-grid">' + "".join(tarjeta(x) for x in PS[:3]) + "</div>", alt=True)
    pagina(nombre, titulo, desc, kw, [("Inicio", "index.html"), (h1, None)], c, preg, prio=prio)


pag_info("como-elegir-repuesto-para-lavadora.html", "Cómo elegir el repuesto de tu lavadora: mangueras y presostato", "Qué diferencia hay entre la manguera de entrada y la de desagüe, para qué sirve el presostato y cómo escoger la pieza correcta para tu lavadora.",
         "como elegir manguera lavadora, manguera entrada o desague lavadora, presostato lavadora", "Cómo elegir el repuesto de tu lavadora",
         seccion("Las piezas más cambiadas", "<ul class=\"spec-list\"><li><b>Manguera de entrada:</b> lleva el agua de la llave a la lavadora. Cada una trae un color de tuerca: azul para el agua fría y naranja para la caliente.</li><li><b>Manguera de desagüe:</b> saca el agua sucia al desagüe; las hay corrugadas, largas con extensión y con funda protectora.</li><li><b>Manguera tina-bomba:</b> va dentro de la lavadora y une la tina con la bomba de desagüe.</li><li><b>Presostato:</b> sensor que mide el nivel de agua dentro de la lavadora; se vende por marca y tipo (por ejemplo, inverter).</li></ul>") +
         seccion("Cómo elegir", '<ol class="vl"><li>Identifica la pieza: entrada, desagüe, tina-bomba o presostato.</li><li>Compara la forma, el largo y las tuercas con tu pieza vieja.</li><li>En el presostato, confirma la marca y el modelo de tu lavadora.</li><li>Si dudas, escríbenos con una foto y el modelo.</li></ol>', alt=True), FAQ_HOME)
pag_info("como-encontrar-el-modelo-de-tu-electrodomestico.html", "Cómo encontrar el modelo de tu lavadora o nevera", "Dónde está la etiqueta del modelo en lavadoras y neveras y qué enviar por WhatsApp para confirmar que un repuesto le sirve.", "donde esta el modelo de mi lavadora, modelo de mi nevera, etiqueta modelo electrodomestico",
         "Cómo encontrar el modelo de tu electrodoméstico", seccion("Dónde mirar", "<ul class=\"spec-list\"><li><b>Lavadora:</b> en el marco de la puerta, en la parte trasera o en un costado.</li><li><b>Nevera:</b> dentro del refrigerador, en la pared lateral o cerca del cajón de verduras, y a veces atrás.</li></ul><p>Fotografía la etiqueta y la pieza dañada, y envíalas por WhatsApp para confirmar la compatibilidad.</p>"), FAQ_HOME)
pag_info("preguntas-frecuentes-repuestos.html", "Preguntas frecuentes sobre repuestos de línea blanca", "Respuestas sobre compatibilidad, precios, envíos, pago contra entrega, garantía y retracto de los repuestos.", "preguntas frecuentes repuestos", "Preguntas frecuentes", "", FAQ_HOME)
pag_info("envios-y-pagos.html", "Envíos y formas de pago | Repuestos de línea blanca", "Enviamos a toda Colombia por transportadora. Pagas con Wompi (tarjeta, PSE, Nequi, Bancolombia) o contra entrega sin recargo.", "envios repuestos colombia, contra entrega repuestos", "Envíos y formas de pago",
         seccion("Envíos", "<p>Enviamos a toda Colombia por transportadora. Te confirmamos el despacho por correo y WhatsApp; el tiempo de entrega depende de la ciudad.</p>") + seccion("Formas de pago", "<ul class=\"spec-list\"><li><b>En línea con Wompi:</b> tarjeta de crédito o débito, PSE, Nequi o botón Bancolombia.</li><li><b>Contra entrega:</b> pagas en efectivo al recibir, sin recargo.</li></ul>", alt=True),
         [("¿Cómo funciona el pago contra entrega?", "Haces el pedido, lo confirmamos y pagas cuando lo recibes."), ("¿Puedo pagar con tarjeta?", "Sí, con Wompi.")])
pag_info("garantia-cambio-y-devolucion.html", "Garantía, cambio y devolución | Repuestos de línea blanca", "Tienes 5 días hábiles de retracto desde la entrega con el producto sin usar ni instalar, y la garantía legal de la Ley 1480.", "garantia repuestos, devolucion repuestos", "Garantía, cambio y devolución",
         seccion("Retracto de 5 días hábiles", "<p>Si la pieza no es lo que necesitas, tienes 5 días hábiles desde que la recibes para devolverla, siempre que esté sin usar ni instalar y en su empaque.</p>") + seccion("Garantía", "<p>Todos los productos tienen la garantía legal de la Ley 1480 de 2011. Si llega defectuoso, lo cambiamos.</p>", alt=True))
pag_info("quienes-somos.html", "Quiénes somos | Repuestos de línea blanca", "Tienda en línea independiente de repuestos para lavadoras y neveras, con envío a toda Colombia.", "quienes somos repuestos linea blanca", "Quiénes somos",
         seccion("Repuestos que sí le sirven a tu equipo", f"<p>{esc(NOMBRE)} es una tienda en línea independiente de repuestos para lavadoras y neveras en Colombia. Te ayudamos a confirmar la compatibilidad con el modelo de tu equipo antes de comprar. Los nombres de marcas se usan solo para indicar compatibilidad; no tenemos afiliación con los fabricantes.</p><p>WhatsApp y teléfono: <a href=\"tel:+{WA}\">{TEL}</a>.</p>"))
pag_info("contacto.html", "Contacto | Repuestos de línea blanca", f"WhatsApp y teléfono {TEL}. Escríbenos con el modelo de tu equipo y la pieza que necesitas.", "contacto repuestos linea blanca", "Contacto",
         seccion("Escríbenos", f'<div class="aq-tiles"><div class="aq-tile"><b>WhatsApp</b><p><a href="https://wa.me/{WA}?text=Hola%2C%20necesito%20un%20repuesto" rel="noopener">{TEL}</a></p></div><div class="aq-tile"><b>Teléfono</b><p><a href="tel:+{WA}">{TEL}</a></p></div></div>'))
pag_info("mapa-del-sitio.html", "Mapa del sitio | Repuestos de línea blanca", "Todas las páginas de la tienda de repuestos de línea blanca.", "mapa del sitio", "Mapa del sitio",
         seccion("Páginas", "<ul class=\"spec-list\">" + "".join(f'<li><a href="{n}">{esc(t)}</a></li>' for n, pr, t, d in PAGINAS if n != "mapa-del-sitio.html") + "</ul>"))
(OUT / "404.html").write_text("<!doctype html><html lang=\"es-CO\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>Página no encontrada</title><link rel=\"stylesheet\" href=\"/tema.css\"></head><body>" + encabezado().replace('href="', 'href="/').replace('src="', 'src="/').replace('href="//', 'href="/') + '<section class="hero"><div class="wrap"><h1>Página no encontrada</h1><p class="sub"><a href="/">Volver al inicio</a></p></div></section></body></html>', encoding="utf-8")

# ---------------------------------------------------------------- robots, sitemap, llms y .htaccess
IMG_MAP = {p["url"]: f"{DOMINIO}/{p['img']}" for p in PS}
(OUT / "robots.txt").write_text("User-agent: *\nAllow: /\nDisallow: /carrito.php\nDisallow: /gracias.php\nDisallow: /api/\n\n" + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in ("GPTBot", "ChatGPT-User", "OAI-SearchBot", "ClaudeBot", "Claude-SearchBot", "PerplexityBot", "Google-Extended")) + f"Sitemap: {DOMINIO}/sitemap.xml\n", encoding="utf-8")
(OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n' + "".join(
    f"  <url><loc>{DOMINIO}/{'' if n == 'index.html' else n}</loc><lastmod>{HOY}</lastmod><changefreq>weekly</changefreq><priority>{pr}</priority>" + (f"<image:image><image:loc>{IMG_MAP[n]}</image:loc></image:image>" if n in IMG_MAP else "") + "</url>\n" for n, pr, t, d in PAGINAS) + "</urlset>\n", encoding="utf-8")
ll = [f"# {NOMBRE}", "", f"> Tienda en línea de repuestos para lavadoras y neveras en Colombia: mangueras, presostatos y protectores de voltaje. Pago con Wompi o contra entrega. WhatsApp {TEL}.", "", "## Repuestos"]
ll += [f"- [{p['nombre']}]({DOMINIO}/{p['url']})" + (f": {cop(p['precio'])}." if p["precio"] else ": consultar precio.") for p in PS]
ll += ["", "## Ayuda"] + [f"- [{t}]({DOMINIO}/{u})" for t, u in ARTS_BASE]
(OUT / "llms.txt").write_text("\n".join(ll) + "\n", encoding="utf-8")
(OUT / ".htaccess").write_text("DirectoryIndex index.html index.php\nErrorDocument 404 /404.html\nOptions -Indexes\nRewriteEngine On\nRewriteCond %{HTTPS} off\nRewriteCond %{HTTP:X-Forwarded-Proto} !https\nRewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]\n"
                               "RewriteCond %{HTTP_HOST} ^www\\.(.+)$ [NC]\nRewriteRule ^ https://%1%{REQUEST_URI} [L,R=301]\n<FilesMatch \"\\.(sqlite|sqlite-wal|sqlite-shm|log)$\">\n  Require all denied\n</FilesMatch>\n"
                               "<IfModule mod_expires.c>\nExpiresActive On\nExpiresByType image/webp \"access plus 1 month\"\nExpiresByType text/css \"access plus 1 week\"\n</IfModule>\n", encoding="utf-8")
print(f"listo: {OUT} · {len(PAGINAS)} páginas · {len(PS)} repuestos")
_V = {}
for _f in ("tema.css", "buscar.js", "carrito.js", "pasarela.css", "estilo.css"):
    if (OUT / _f).exists():
        _V[_f] = hashlib.md5((OUT / _f).read_bytes()).hexdigest()[:8]
_pat = re.compile(r"""(["'])(/?)(tema\.css|buscar\.js|carrito\.js|pasarela\.css|estilo\.css)(\?v=[\w]+)?(?=["'])""")
for _h in list(OUT.glob("*.html")) + list(OUT.glob("*.php")):
    _t = _h.read_text(encoding="utf-8")
    _t2 = _pat.sub(lambda m: f"{m.group(1)}{m.group(2)}{m.group(3)}?v={_V[m.group(3)]}" if m.group(3) in _V else m.group(0), _t)
    if _t2 != _t:
        _h.write_text(_t2, encoding="utf-8")
