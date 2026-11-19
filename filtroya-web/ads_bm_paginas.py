# Páginas de la tienda de protectores Breakermatic. Se ejecuta dentro de ads_bm.py (comparte sus funciones y datos).
GAL_JS = ""


def galeria_html(p):
    return ('<div class="gal" data-gal><div class="gal-main"><img decoding="async" src="' + p["img"] + '" alt="' + esc(p["nombre"]) + '" width="520" height="520"></div></div>')


# ---------------------------------------------------------------- buscador del encabezado
ARTS_BASE = [("Cómo elegir el protector", "como-elegir-protector-de-voltaje.html"), ("Para qué sirve un protector de voltaje", "para-que-sirve-un-protector-de-voltaje.html"),
             ("Preguntas frecuentes", "preguntas-frecuentes-protector-de-voltaje.html"), ("Envíos y contra entrega", "envios-y-contra-entrega.html"), ("Garantía, cambio y devolución", "garantia-cambio-y-devolucion.html")]
items = [[p["nombre"], p["url"], "Protector", cop(p["precio"])] for p in PS]
items += [[f"Protector de voltaje para {p['equipos']}", p["url"], "Equipo", p["corto"]] for p in PS]
items += [[t, u, "Guía", ""] for t, u in ARTS_BASE]
js = ("(function(){var D=" + json.dumps(items, ensure_ascii=False, separators=(",", ":")) + ";"
      "function n(s){return s.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').replace(/[^a-z0-9 ]+/g,' ').trim()}var X=D.map(function(r){return n(r[0]+' '+r[2]+' '+r[3])});"
      "function buscar(q){q=n(q);if(!q)return[];var t=q.split(/ +/),o=[];for(var i=0;i<D.length;i++){var ok=true,sc=0;for(var j=0;j<t.length;j++){var p=X[i].indexOf(t[j]);if(p<0){ok=false;break}sc+=p===0?0:1}"
      "if(ok){var e=n(D[i][0]);o.push([sc+(e.indexOf(q)===0?-2:0),i])}}o.sort(function(a,b){return a[0]-b[0]});return o.slice(0,10).map(function(x){return D[x[1]]})}"
      "function pintar(caja,r,q){if(!q.trim()){caja.hidden=true;return}var g={},h='';r.forEach(function(x){(g[x[2]]=g[x[2]]||[]).push(x)});Object.keys(g).forEach(function(k){h+='<h6>'+k+'</h6>'+g[k].map(function(x){return '<a href=\"'+x[1]+'\"><span>'+x[0]+'</span><small>'+x[3]+'</small></a>'}).join('')});"
      "caja.innerHTML=h||'<p>No encontramos «'+q.replace(/</g,'')+'». Prueba con nevera, lavadora o televisor.</p>';caja.hidden=false}"
      "document.querySelectorAll('[data-aq-q]').forEach(function(i){var c=i.parentNode.querySelector('.aq-res');i.addEventListener('input',function(){pintar(c,buscar(i.value),i.value)});i.addEventListener('focus',function(){if(i.value)pintar(c,buscar(i.value),i.value)});"
      "i.addEventListener('keydown',function(e){if(e.key==='Enter'){var a=c.querySelector('a');if(a)location.href=a.getAttribute('href')}if(e.key==='Escape')c.hidden=true})});"
      "document.addEventListener('click',function(e){document.querySelectorAll('.aq-res').forEach(function(c){if(!c.parentNode.contains(e.target))c.hidden=true});document.querySelectorAll('.aq-nav details[open]').forEach(function(d){if(!d.contains(e.target))d.removeAttribute('open')})});})();")
(OUT / "buscar.js").write_text(js, encoding="utf-8")

# partes.php: el carrito y «gracias» llevan el mismo encabezado y pie
_src_lg = open(AQUI / "ads_lg_paginas.py", encoding="utf-8").read()
_partes = _src_lg.split('(OUT / "partes.php").write_text(r"""')[1].split('""".replace("__AQH__"')[0]
_partes = _partes.replace("/img/icono-lg.png", "/img/icono-bm.png").replace('<body class="tienda-samsung">', '<body class="tienda-samsung">')
(OUT / "partes.php").write_text(_partes.replace("__AQH__", encabezado()).replace("__AQF__", pie()), encoding="utf-8")

# páginas PHP de compra: se quitan las menciones a filtros y se escriben términos y garantía de esta tienda
_c = (OUT / "carrito.php").read_text(encoding="utf-8")
_c = re.sub(r'Busca el filtro de tu nevecón por la referencia o por[^<]*', 'Elige el protector de voltaje de tu nevera, lavadora o televisor.', _c)
_c = re.sub(r'(<label)([^>]*>(?:(?!</label>).)*Recuérdame por correo cuando toque cambiar el filtro)', r'\1 hidden\2', _c, flags=re.S)
_c = _c.replace('Modelo del nevecón <i>(opcional)</i>', 'Equipo que quieres proteger <i>(opcional)</i>').replace('Nos ayuda a confirmar que le sirve', 'Ej.: nevera, lavadora o televisor')
_c = _c.replace('Ver todos los filtros', 'Ver los protectores').replace('href="/tienda/"', 'href="/index.html#protectores"')
_c = _c.replace('${n === 1 ? "filtro" : "filtros"}', '${n === 1 ? "protector" : "protectores"}')
(OUT / "carrito.php").write_text(_c, encoding="utf-8")
_pv = (OUT / "privacidad.php").read_text(encoding="utf-8")
_pv = re.sub(r'<li>[^<]*enviarte un correo cuando toque cambiar el filtro[^<]*</li>', '', _pv)
(OUT / "privacidad.php").write_text(_pv, encoding="utf-8")
_legal = lambda titulo, desc, ruta, cuerpo: ("<?php require __DIR__ . '/partes.php'; $n = cfg()['negocio']; cabeza('" + titulo + " | ' . $n['nombre'], '" + desc + "', '/" + ruta + "'); ?>\n<article class=\"legal\">\n" + cuerpo + "\n</article>\n<?php pie(); ?>\n")
(OUT / "terminos.php").write_text(_legal("Términos y condiciones", "Términos y condiciones de compra, envíos, garantía y derecho de retracto.", "terminos.php",
    "<h1>Términos y condiciones</h1><p class=\"m\">Ley 1480 de 2011 (Estatuto del Consumidor).</p>"
    "<h2>1. Quiénes somos</h2><p><?= identificacion() ?> WhatsApp y teléfono: <?= h($n['telefono']) ?>. Correo: <?= h($n['correo']) ?>.</p>"
    "<h2>2. Cómo se compra</h2><p>Escoges el protector, escribes tus datos de entrega y pagas en línea con Wompi (tarjeta, PSE, Nequi o Bancolombia) o contra entrega, en efectivo, sin recargo.</p>"
    "<h2>3. Precios</h2><p>Están en pesos colombianos y son el valor total a pagar, con el envío incluido. No hay cobros adicionales.</p>"
    "<h2>4. Antes de comprar</h2><p>Los protectores son de 110 VAC. Las fotos son de referencia. Si tienes dudas sobre cuál es el de tu equipo, escríbenos antes de comprar.</p>"
    "<h2>5. Entregas</h2><p>Envío sin costo a toda Colombia por transportadora. Los tiempos son estimados y se informan al confirmar el pedido.</p>"
    "<h2 id=\"garantia\">6. Garantía</h2><p>Todos los productos tienen la garantía legal de la Ley 1480 de 2011. Más detalle en <a href=\"/garantia-y-retracto.php\">Garantía y retracto</a>.</p>"
    "<h2>7. Derecho de retracto</h2><p>Como es una compra a distancia, tienes <b>5 días hábiles desde que recibes el producto</b> para retractarte, sin dar explicaciones. El producto debe estar sin usar y en su empaque.</p>"
    "<h2>8. Marcas</h2><p>Breakermatic es una marca de su propietario. <?= h($n['nombre']) ?> es un comercio independiente que vende sus productos; no tiene afiliación con el fabricante.</p>"
    "<h2>9. Peticiones, quejas y reclamos</h2><p>Escríbenos a <?= h($n['correo']) ?>. Respondemos en máximo 15 días hábiles. También puedes acudir a la <a href=\"https://www.sic.gov.co\" rel=\"noopener\">Superintendencia de Industria y Comercio</a>.</p>"), encoding="utf-8")
(OUT / "garantia-y-retracto.php").write_text(_legal("Garantía y retracto", "Garantía legal, cambio y derecho de retracto de 5 días hábiles.", "garantia-y-retracto.php",
    "<h1>Garantía y retracto</h1><h2>Derecho de retracto</h2><p>Tienes 5 días hábiles desde la entrega para retractarte si el protector está sin usar y en su empaque. Escríbenos a <?= h($n['correo']) ?> o al WhatsApp <?= h($n['telefono']) ?>.</p>"
    "<h2>Garantía</h2><p>Los productos tienen la garantía legal de la Ley 1480 de 2011. Si llega defectuoso o no es el que pediste, lo cambiamos.</p>"
    "<h2>Cómo pedir un cambio</h2><p>Escríbenos con tu número de pedido y una foto del producto. Te indicamos cómo devolverlo.</p>"), encoding="utf-8")
(OUT / "opinion.php").unlink(missing_ok=True)
(OUT / "admin.php").unlink(missing_ok=True) if not os.environ.get("ADMIN_CLAVE") else None

# ---------------------------------------------------------------- portada
MAS = PS[0]
stage = ('<div class="aq-stage"><i></i><i></i><i></i><i></i>' + "".join(f'<a class="s{i + 1}" href="{p["url"]}" aria-label="{esc(p["corto"])}"><img src="{p["img"]}" alt="{esc(p["nombre"])}" width="300" height="300" {"loading=eager" if i == 0 else "loading=lazy"}></a>' for i, p in enumerate([PS[1], PS[0], PS[2]]))
         + f'<span class="aq-price-tag">★ Los 3 modelos a {cop(PRECIO)} · envío gratis</span></div>')
hero = ('<section class="aq-hero" id="inicio"><div class="wrap"><div><span class="kicker">Breakermatic · 110 V · Toda Colombia</span><h1>Protector de voltaje para tu nevera, lavadora o televisor</h1>'
        '<p class="lead">Elige el protector de tu equipo, agrégalo al carrito y paga en línea o contra entrega. Desconecta tu electrodoméstico cuando el voltaje sube o baja y lo reconecta al volver a la normalidad. Envío gratis.</p>'
        '<div class="aq-trust"><span>Envío gratis a toda Colombia</span><span>Pago seguro Wompi</span><span>Contra entrega</span><span>5 días de retracto</span></div></div>' + stage + '</div></section>')
qa_home = qa("¿Qué protector de voltaje necesito para mi nevera, lavadora o televisor?",
             f"Breakermatic tiene un protector para cada equipo: <b>neveras digitales</b> (110 VAC, 10 A, espera de 4 minutos), <b>lavadoras</b> (110 VAC, 15 A, 2 tomas) y <b>televisores</b> (110 VAC, 10 A, 2 tomas). Cada uno cuesta <b>{cop2(PRECIO)}</b> con <b>envío gratis a toda Colombia</b>; "
             "pagas en línea con Wompi o contra entrega.", [("Voltaje", "110 VAC"), ("Precio", cop(PRECIO)), ("Envío", "Gratis"), ("Pago", "Wompi o contra entrega")])
estante = seccion(f"Elige tu protector Breakermatic · {cop(PRECIO)} con envío gratis", '<div class="tf-grid">' + "".join(tarjeta(p, i) for i, p in enumerate(PS)) + "</div>").replace('<section class="aq-sec">', '<section class="aq-sec estante-top" id="protectores">', 1)
porque = [("rayo", "Vigila el voltaje", "Mide el voltaje de la toma y muestra el estado con luces indicadoras."), ("candado", "Desconecta a tiempo", "Si el voltaje es alto o bajo, corta la corriente al equipo conectado."),
          ("retorno", "Reconecta con espera", "Al normalizarse el voltaje espera unos segundos (4 minutos en neveras) antes de volver a dar corriente."), ("caja", "Se instala solo", "Conéctalo a la toma de pared y enchufa tu equipo. Sin obras ni técnico.")]
ICONOS["rayo"] = '<svg viewBox="0 0 24 24"><path d="M13 2 4 14h7l-1 8 9-12h-7z"/></svg>'
sec_porque = seccion("Para qué sirve un protector de voltaje", '<div class="aq-tiles">' + "".join(f'<div class="aq-tile">{ICONOS[i]}<b>{esc(t)}</b><p>{esc(d)}</p></div>' for i, t, d in porque) + "</div>", alt=True,
                     sub="El voltaje de la red puede subir o bajar sin que lo notes. Los equipos con tarjeta electrónica son los más sensibles.")
luces = ('<div class="aq-tiles"><div class="aq-tile"><b>🟢 Voltaje normal</b><p>El equipo está conectado y recibe corriente.</p></div><div class="aq-tile"><b>🟡 Ciclo de espera</b><p>El protector espera antes de reconectar el equipo.</p></div>'
         '<div class="aq-tile"><b>🔴 Voltaje alto</b><p>El voltaje superó el rango normal: el equipo se desconecta.</p></div><div class="aq-tile"><b>🔴 Voltaje bajo</b><p>El voltaje cayó por debajo del rango normal: el equipo se desconecta.</p></div></div>')
sec_luces = seccion("Qué significan las luces del protector", luces, sub="Los tres modelos traen cuatro indicadores.")
comp = ('<div class="tbl-wrap"><table class="spec-table"><tr><th></th>' + "".join(f'<th><a href="{p["url"]}" style="color:#fff">{esc(p["corto"])}</a></th>' for p in PS) + "</tr>"
        "<tr><td><b>Voltaje</b></td>" + "<td>110 VAC · 50/60 Hz</td>" * 3 + "</tr><tr><td><b>Corriente máxima</b></td>" + "".join(f"<td>{p['amp']} A (aprox. {p['wf']} W)</td>" for p in PS) + "</tr>"
        "<tr><td><b>Tomas</b></td>" + "".join(f"<td>{p['tomas']}</td>" for p in PS) + "</tr><tr><td><b>Ciclo de espera</b></td>" + "".join(f"<td>{p['espera']}</td>" for p in PS) + "</tr>"
        "<tr><td><b>Precio</b></td>" + "".join(f"<td><b>{cop(p['precio'])}</b></td>" for p in PS) + "</tr></table></div>")
sec_comp = seccion("Los tres protectores, lado a lado", comp, alt=True, sub="Compara corriente, tomas, tiempo de espera y precio.")
tiles = [("caja", "Envío gratis", "A toda Colombia, sin costo adicional."), ("candado", "Pago seguro", "Wompi (Bancolombia): tarjeta, PSE, Nequi o botón Bancolombia."),
         ("efectivo", "Contra entrega", "Paga en efectivo cuando recibas tu pedido, sin recargo."), ("retorno", "5 días de retracto", "Si no es lo que necesitas, lo cambiamos (sin usar y en su empaque).")]
confianza = seccion("Compra tranquilo", '<div class="aq-tiles">' + "".join(f'<div class="aq-tile">{ICONOS[i]}<b>{esc(t)}</b><p>{esc(d)}</p></div>' for i, t, d in tiles) + '</div><div class="aq-pay"><span>Visa</span><span>Mastercard</span><span>PSE</span><span>Nequi</span><span>Bancolombia</span><span>Contra entrega</span></div>',
                    sub="Una tienda en línea como las grandes: carrito, pago seguro y confirmación por correo.")
pasos = '<ol class="vl"><li><b>Elige tu protector</b> según el equipo: nevera, lavadora o televisor.</li><li><b>Agrégalo al carrito</b> y escribe tus datos de entrega.</li><li><b>Paga</b> en línea con Wompi o elige contra entrega.</li><li><b>Recibe</b> en tu casa con envío gratis y conéctalo a la toma de pared.</li></ol>'
sec_pasos = seccion("Cómo comprar en 4 pasos", pasos, alt=True)
FAQ_HOME = [("¿Qué protector necesita mi equipo?", "El de su tipo: neveras digitales, lavadoras o televisores. Los tres son de 110 VAC; revisa la etiqueta de tu equipo para confirmar su voltaje y su consumo."),
            ("¿Cuánto cuestan?", f"Cada protector cuesta {cop2(PRECIO)} con envío gratis a toda Colombia."), ("¿Cómo pago?", FPAGO), ("¿Los productos son nuevos?", "Sí, nuevos y en su empaque."),
            ("¿Hay retracto?", "Sí, 5 días hábiles desde la entrega, con el producto sin usar y en su empaque."), ("¿Sirve para equipos de 220 V?", "No. Estos protectores son de 110 VAC.")]
ld_home = [{"@type": "ItemList", "name": "Protectores de voltaje Breakermatic", "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": ld_producto(p)} for i, p in enumerate(PS)]}]
pagina("index.html", f"Protector de Voltaje Breakermatic | Neveras, Lavadoras, TV | {cop(PRECIO)}",
       f"Protectores de voltaje Breakermatic 110V para neveras digitales, lavadoras y televisores: {cop(PRECIO)} con envío gratis y pago contra entrega en toda Colombia. Compra en línea con Wompi.",
       "protector de voltaje, protector de voltaje nevera, protector voltaje lavadora, protector voltaje televisor, breakermatic, regulador de voltaje, protector electronico, protector contra picos de voltaje, protector 110v, contra entrega",
       [("Inicio", None)], hero + estante + qa_home + sec_porque + sec_luces + sec_comp + confianza + sec_pasos + faq_html(FAQ_HOME), FAQ_HOME, ld_home, prio="1.0", og=PS[0]["img"])

# ---------------------------------------------------------------- fichas de producto
for p in PS:
    otros = [x for x in PS if x is not p]
    qa_p = qa(f"¿Para qué sirve el {p['nombre']}?",
              f"El <b>{esc(p['nombre'])}</b> es un protector electrónico de voltaje de 110 VAC (hasta {p['amp']} A, aprox. {p['wf']} W) con {p['tomas']} toma{'s' if p['tomas'] > 1 else ''}. {esc(p['porque'])} "
              f"Cuesta <b>{cop2(p['precio'])}</b> con envío gratis a toda Colombia.", [("Voltaje", "110 VAC"), ("Corriente máx.", f"{p['amp']} A"), ("Tomas", str(p["tomas"])), ("Espera", p["espera"])])
    filas = [("Marca", "Breakermatic"), ("Tipo", "Protector electrónico de voltaje"), ("Para", p["equipo"].capitalize()), ("Voltaje", "110 VAC · 50/60 Hz"), ("Corriente máxima", f"{p['amp']} A (aprox. {p['wf']} W a 110 V)"),
             ("Tomas", str(p["tomas"])), ("Ciclo de espera", p["espera"]), ("Indicadores", p["lista"]), ("Instalación", "Se conecta a la toma de pared; el equipo se conecta al protector"), ("Envío", "Gratis a toda Colombia"),
             ("Pago", "Wompi (tarjeta, PSE, Nequi, Bancolombia) o contra entrega")]
    ficha = '<div class="tbl-wrap"><table class="spec-table">' + "".join(f"<tr><th>{esc(a)}</th><td>{esc(b)}</td></tr>" for a, b in filas) + "</table></div>"
    inst = '<h3 style="margin:22px 0 10px">Cómo usarlo</h3><ol class="vl"><li>Conecta el protector a la toma de pared.</li><li>Espera a que la luz verde indique voltaje normal.</li><li>Enchufa tu ' + p["equipo"] + ' al protector.</li><li>Si el voltaje sale del rango, el protector desconecta el equipo y lo reconecta al normalizarse.</li></ol>'
    preg = [(f"¿Cuánto espera el protector antes de reconectar mi {p['equipo']}?", f"Tiene un ciclo de espera de {p['espera']} después de que el voltaje vuelve a la normalidad."),
            (f"¿Cuánto cuesta el protector de voltaje para {p['equipos']}?", f"{cop2(p['precio'])} con envío gratis a toda Colombia."), ("¿Puedo pagar contra entrega?", FPAGO),
            ("¿Sirve para equipos de 220 V?", "No. Este protector es de 110 VAC."), (f"¿Cuántos equipos puedo conectar?", f"Tiene {p['tomas']} toma{'s' if p['tomas'] > 1 else ''}. La suma del consumo no debe superar {p['amp']} A (aprox. {p['wf']} W).")]
    cuerpo = (f'<section class="hero hero-prod"><div class="wrap hero-grid"><div><span class="kicker">Breakermatic · 110 VAC · {p["amp"]} A</span><h1>{esc(p["nombre"])}</h1>'
              f'<p class="sub" style="margin-top:16px;">{esc(p["resumen"])}</p><div class="hero-price">{cop(p["precio"])} <small>COP · envío gratis</small></div>'
              f'<div class="hero-cta"><button type="button" class="btn btn-solid" data-add="{p["id"]}">🛒 Agregar al carrito</button><button type="button" class="btn" data-add="{p["id"]}" data-ir="1">Comprar ahora</button></div></div>{galeria_html(p)}</div></section>'
              + qa_p + seccion("Especificaciones técnicas", ficha + inst) + faq_html(preg)
              + seccion("Otros protectores Breakermatic", '<div class="tf-grid">' + "".join(tarjeta(x) for x in otros) + "</div>", alt=True))
    pagina(p["url"], f"Protector de Voltaje para {p['equipos'].capitalize()} Breakermatic | {cop(p['precio'])}", f"Compra el {p['nombre']} por {cop(p['precio'])}: 110 VAC, {p['amp']} A, {p['tomas']} toma(s), espera de {p['espera']}. Envío gratis y pago contra entrega en toda Colombia.",
           f"protector de voltaje {p['equipo']}, protector voltaje {p['equipos']}, breakermatic {p['equipos']}, protector {p['equipo']} 110v, regulador voltaje {p['equipo']}, protector contra picos {p['equipo']}",
           [("Inicio", "index.html"), ("Protectores", "index.html#protectores"), (p["corto"], None)], cuerpo, preg, [ld_producto(p)], prio="0.9", og=p["img"])

# ---------------------------------------------------------------- guías y páginas de ayuda
def pag_info(nombre, titulo, desc, kw, h1, cuerpo, preg=(), prio="0.6"):
    c = hero_simple("Protectores de voltaje Breakermatic", h1, desc) + cuerpo + (faq_html(list(preg)) if preg else "") + seccion("Elige tu protector", '<div class="tf-grid">' + "".join(tarjeta(x) for x in PS) + "</div>", alt=True)
    pagina(nombre, titulo, desc, kw, [("Inicio", "index.html"), (h1, None)], c, preg, prio=prio)


FAQ_G = [("¿Qué hace un protector de voltaje?", "Vigila el voltaje que llega a tu equipo. Si sube o baja fuera del rango normal, lo desconecta, y lo vuelve a conectar cuando el voltaje se normaliza, después del tiempo de espera."),
         ("¿Sirve para equipos de 220 V?", "No. Estos protectores son de 110 VAC."), ("¿Cómo pago?", FPAGO), ("¿Cuánto cuesta el envío?", "Es gratis a toda Colombia."),
         ("¿Un protector evita todos los daños?", "Reduce el riesgo de daños por voltaje alto o bajo, pero ningún protector cubre todos los casos. Para equipos costosos usa también una buena instalación eléctrica.")]
pag_info("como-elegir-protector-de-voltaje.html", "Cómo elegir un protector de voltaje para nevera, lavadora o TV", "Guía para elegir el protector de voltaje correcto: voltaje de tu equipo, corriente máxima, tomas y tiempo de espera.",
         "como elegir protector de voltaje, que protector necesito, protector voltaje nevera lavadora tv", "Cómo elegir un protector de voltaje",
         seccion("Cuatro datos para acertar", '<ol class="vl"><li><b>Voltaje.</b> Debe coincidir con la etiqueta de tu equipo. Estos protectores son de 110 VAC.</li><li><b>Corriente.</b> El consumo del equipo no debe superar los 10 A o 15 A del modelo.</li>'
                 '<li><b>Tomas.</b> Lavadoras y televisores traen 2 tomas; el de neveras, 1.</li><li><b>Espera.</b> El de neveras espera 4 minutos antes de reconectar; los otros, 5 segundos.</li></ol>'
                 '<div class="tbl-wrap"><table class="spec-table"><tr><th>Equipo</th><th>Protector</th><th>Corriente</th><th>Tomas</th><th>Espera</th><th>Precio</th></tr>' + "".join(f'<tr><td>{p["equipo"].capitalize()}</td><td><a href="{p["url"]}">{esc(p["nombre"])}</a></td><td>{p["amp"]} A</td><td>{p["tomas"]}</td><td>{p["espera"]}</td><td><b>{cop(p["precio"])}</b></td></tr>' for p in PS) + "</table></div>"), FAQ_G)
pag_info("para-que-sirve-un-protector-de-voltaje.html", "Para qué sirve un protector de voltaje y cómo funciona", "Qué es un protector de voltaje, cómo funciona, qué significan sus luces y por qué una nevera, una lavadora y un televisor lo necesitan.",
         "para que sirve un protector de voltaje, como funciona un protector de voltaje, luces protector voltaje", "Para qué sirve un protector de voltaje",
         seccion("Cómo funciona", "<p>El protector se conecta a la toma de pared y el equipo se conecta a él. Mide el voltaje continuamente: si es normal, deja pasar la corriente; si es alto o bajo, desconecta el equipo; cuando vuelve a la normalidad, espera un tiempo y lo reconecta.</p>" + luces) +
         seccion("Por qué cada equipo tiene el suyo", "<ul class=\"spec-list\">" + "".join(f"<li><b>{p['equipos'].capitalize()}:</b> {esc(p['porque'])}</li>" for p in PS) + "</ul>", alt=True), FAQ_G)
pag_info("preguntas-frecuentes-protector-de-voltaje.html", "Preguntas frecuentes sobre protectores de voltaje Breakermatic", "Respuestas sobre protectores de voltaje Breakermatic: precios, envío gratis, pago contra entrega, garantía, retracto y compatibilidad.",
         "preguntas frecuentes protector de voltaje", "Preguntas frecuentes", "", FAQ_HOME + FAQ_G[:2])
pag_info("envios-y-contra-entrega.html", "Envío gratis y pago contra entrega | Protectores Breakermatic", "Enviamos protectores de voltaje Breakermatic a toda Colombia con envío gratis, pago con Wompi o contra entrega sin recargo.",
         "envio gratis protector voltaje, contra entrega protector voltaje", "Envíos y formas de pago",
         seccion("Envío gratis a toda Colombia", "<p>Enviamos por transportadora sin costo adicional. Te confirmamos el despacho por correo y WhatsApp. Los tiempos de entrega son estimados y dependen de la ciudad.</p>") +
         seccion("Formas de pago", "<ul class=\"spec-list\"><li><b>En línea con Wompi:</b> tarjeta de crédito o débito, PSE, Nequi o botón Bancolombia.</li><li><b>Contra entrega:</b> pagas en efectivo cuando recibes el producto, sin recargo.</li></ul>", alt=True),
         [("¿Cuánto cuesta el envío?", "Nada: el envío es gratis a toda Colombia."), ("¿Cómo funciona el pago contra entrega?", "Haces el pedido, lo confirmamos y pagas cuando lo recibes."), ("¿Puedo pagar con tarjeta?", "Sí, con Wompi: tarjeta, PSE, Nequi o Bancolombia.")])
pag_info("garantia-cambio-y-devolucion.html", "Garantía, cambio y devolución | Protectores Breakermatic", "Tienes 5 días hábiles de retracto desde la entrega con el producto sin usar y en su empaque, y la garantía legal de la Ley 1480.",
         "garantia protector voltaje, devolucion protector voltaje", "Garantía, cambio y devolución",
         seccion("Retracto de 5 días hábiles", "<p>Si el protector no es lo que necesitas, tienes 5 días hábiles desde que lo recibes para devolverlo, siempre que esté sin usar y en su empaque. Escríbenos por WhatsApp o correo y coordinamos la devolución.</p>") +
         seccion("Garantía", "<p>Todos los productos tienen la garantía legal de la Ley 1480 de 2011. Si llega defectuoso, lo cambiamos.</p>", alt=True))
pag_info("quienes-somos.html", "Quiénes somos | Protectores de Voltaje Breakermatic", "Tienda en línea independiente de protectores de voltaje Breakermatic para neveras, lavadoras y televisores, con envío gratis a toda Colombia.",
         "quienes somos protectores breakermatic", "Quiénes somos",
         seccion("Una tienda dedicada a proteger tus electrodomésticos", f"<p>{esc(NOMBRE)} es una tienda en línea independiente que vende protectores electrónicos de voltaje Breakermatic en Colombia. Te ayudamos a escoger el modelo de tu equipo y te lo enviamos gratis. Breakermatic es una marca de su propietario; no somos el fabricante.</p><p>WhatsApp y teléfono: <a href=\"tel:+{WA}\">{TEL}</a>.</p>"))
pag_info("contacto.html", "Contacto | Protectores de Voltaje Breakermatic", f"WhatsApp y teléfono {TEL}. Escríbenos con el equipo que quieres proteger y te recomendamos el protector.",
         "contacto protectores breakermatic", "Contacto",
         seccion("Escríbenos", f'<div class="aq-tiles"><div class="aq-tile"><b>WhatsApp</b><p><a href="https://wa.me/{WA}?text=Hola%2C%20quiero%20un%20protector%20de%20voltaje%20Breakermatic" rel="noopener">{TEL}</a></p></div><div class="aq-tile"><b>Teléfono</b><p><a href="tel:+{WA}">{TEL}</a></p></div></div>'))
pag_info("mapa-del-sitio.html", "Mapa del sitio | Protectores Breakermatic", "Todas las páginas de la tienda de protectores de voltaje Breakermatic.", "mapa del sitio", "Mapa del sitio",
         seccion("Páginas", "<ul class=\"spec-list\">" + "".join(f'<li><a href="{n}">{esc(t)}</a></li>' for n, pr, t, d in PAGINAS if n != "mapa-del-sitio.html") + "</ul>"))
(OUT / "404.html").write_text(head_404 := ("<!doctype html><html lang=\"es-CO\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>Página no encontrada</title><link rel=\"stylesheet\" href=\"/tema.css\"></head><body>" + encabezado().replace('href="', 'href="/').replace('src="', 'src="/').replace('href="//', 'href="/') + '<section class="hero"><div class="wrap"><h1>Página no encontrada</h1><p class="sub"><a href="/">Volver al inicio</a></p></div></section></body></html>'), encoding="utf-8")

# ---------------------------------------------------------------- robots, sitemap, llms y .htaccess
IMG_MAP = {p["url"]: f"{DOMINIO}/{p['img']}" for p in PS}
(OUT / "robots.txt").write_text("User-agent: *\nAllow: /\nDisallow: /carrito.php\nDisallow: /gracias.php\nDisallow: /api/\n\n" + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in ("GPTBot", "ChatGPT-User", "OAI-SearchBot", "ClaudeBot", "Claude-SearchBot", "PerplexityBot", "Google-Extended")) + f"Sitemap: {DOMINIO}/sitemap.xml\n", encoding="utf-8")
(OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n' + "".join(
    f"  <url><loc>{DOMINIO}/{'' if n == 'index.html' else n}</loc><lastmod>{HOY}</lastmod><changefreq>weekly</changefreq><priority>{pr}</priority>" + (f"<image:image><image:loc>{IMG_MAP[n]}</image:loc></image:image>" if n in IMG_MAP else "") + "</url>\n" for n, pr, t, d in PAGINAS) + "</urlset>\n", encoding="utf-8")
ll = [f"# {NOMBRE}", "", f"> Tienda en línea de protectores de voltaje Breakermatic 110V para neveras, lavadoras y televisores en Colombia. Envío gratis a toda Colombia, pago con Wompi o contra entrega. WhatsApp {TEL}.", "", "## Protectores y precios (COP, envío gratis)"]
ll += [f"- [{p['nombre']}]({DOMINIO}/{p['url']}): {cop(p['precio'])}. 110 VAC, {p['amp']} A, {p['tomas']} toma(s), espera de {p['espera']}." for p in PS]
ll += ["", "## Ayuda"] + [f"- [{t}]({DOMINIO}/{u})" for t, u in ARTS_BASE]
(OUT / "llms.txt").write_text("\n".join(ll) + "\n", encoding="utf-8")
(OUT / ".htaccess").write_text("DirectoryIndex index.html index.php\nErrorDocument 404 /404.html\nOptions -Indexes\nRewriteEngine On\nRewriteCond %{HTTPS} off\nRewriteCond %{HTTP:X-Forwarded-Proto} !https\nRewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]\n"
                               "RewriteCond %{HTTP_HOST} ^www\\.(.+)$ [NC]\nRewriteRule ^ https://%1%{REQUEST_URI} [L,R=301]\n<FilesMatch \"\\.(sqlite|sqlite-wal|sqlite-shm|log)$\">\n  Require all denied\n</FilesMatch>\n"
                               "<IfModule mod_expires.c>\nExpiresActive On\nExpiresByType image/webp \"access plus 1 month\"\nExpiresByType text/css \"access plus 1 week\"\n</IfModule>\n", encoding="utf-8")
print(f"listo: {OUT} · {len(PAGINAS)} páginas · {len(PS)} protectores")

# ---- versión por contenido en CSS y JS
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
