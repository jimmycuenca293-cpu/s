# Páginas de la tienda de LG. Se ejecuta dentro de ads_lg.py (comparte sus funciones y datos).
FPAGO = "Pagas en línea con Wompi (tarjeta, PSE, Nequi o Bancolombia) o contra entrega, en efectivo, sin recargo."
MOD_TXT = "; ".join(f"{p['corto']} ({', '.join(p['modelos'])})" for p in PS if p["modelos"])
GAL_JS = ("<script>document.querySelectorAll('[data-gal]').forEach(function(g){var m=g.querySelector('.gal-main'),i=m.querySelector('img');g.querySelectorAll('.gal-th button').forEach(function(b){b.addEventListener('click',function(){"
          "g.querySelectorAll('.gal-th button').forEach(function(x){x.setAttribute('aria-selected','false')});b.setAttribute('aria-selected','true');i.src=b.dataset.src;i.alt=b.dataset.alt;m.classList.remove('zoom')})});"
          "m.addEventListener('click',function(e){var r=m.getBoundingClientRect();i.style.transformOrigin=((e.clientX-r.left)/r.width*100)+'% '+((e.clientY-r.top)/r.height*100)+'%';m.classList.toggle('zoom')})});</script>")


def galeria_html(p):
    L = [(p["img"], f"Foto del filtro {p['corto']}"), (f"img/gal-{p['id']}-identificar.jpg", f"Cómo identificar el filtro {p['corto']}"), (f"img/gal-{p['id']}-ficha.jpg", f"Ficha técnica del filtro {p['corto']}")]
    return ('<div class="gal" data-gal><div class="gal-main"><img decoding="async" src="' + L[0][0] + '" alt="' + esc(L[0][1]) + '" width="520" height="520"></div><div class="gal-th" role="tablist">'
            + "".join(f'<button type="button" role="tab" aria-selected="{"true" if i == 0 else "false"}" data-src="{s}" data-alt="{esc(a)}" aria-label="{esc(a)}"><img src="{s}" alt="" loading="lazy"></button>' for i, (s, a) in enumerate(L)) + "</div></div>")


# ---------------------------------------------------------------- buscador del encabezado
items = [[p["corto"] + " · " + p["ref"], p["url"], "Filtro", cop(p["precio"])] for p in PS]
items += [[CIUDAD[s][0], R_CIU(s), "Ciudad", CIUDAD[s][1]] for s in CIUDAD]
items += [[d, R_DEPTO(d), "Departamento", f"{len(POR_DEPTO[d])} ciudades"] for d in DEPTOS]
items += [[v[0], R_REG(k), "Región", "filtros LG"] for k, v in REG.items()] + [[v[0], R_AREA(k), "Área metropolitana", "filtros LG"] for k, v in AREAS.items()]
items += [[m, R_MOD(m), "Modelo de nevecón", p["corto"]] for m, p in MODELOS]
ref_vistos = set()
REFS = []
for p in PS:
    for r in p["refs"][1:]:
        if slug(r) not in ref_vistos and slug(r) != slug(p["ref"]):
            ref_vistos.add(slug(r))
            REFS.append((r, p))
items += [[r, R_REF(r), "Código", f"equivale al {p['corto']}"] for r, p in REFS]
ARTS = marcas_contenido_lg.articulos(PS, "/", "/cambio-e-instalacion/")
items += [[t, U(sl), "Guía", ""] for sl, t, d, _, _, _ in ARTS]
js = ("(function(){var D=" + json.dumps(items, ensure_ascii=False, separators=(",", ":")) + ";"
      "function n(s){return s.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').replace(/[^a-z0-9 ]+/g,' ').trim()}var X=D.map(function(r){return n(r[0]+' '+r[2]+' '+r[3])});"
      "function buscar(q){q=n(q);if(!q)return[];var t=q.split(/ +/),o=[];for(var i=0;i<D.length;i++){var ok=true,sc=0;for(var j=0;j<t.length;j++){var p=X[i].indexOf(t[j]);if(p<0){ok=false;break}sc+=p===0?0:1}"
      "if(ok){var e=n(D[i][0]);o.push([sc+(e.indexOf(q)===0?-2:0)+(D[i][2]==='Ciudad'?0:.5),i])}}o.sort(function(a,b){return a[0]-b[0]});return o.slice(0,14).map(function(x){return D[x[1]]})}"
      "function pintar(caja,r,q){if(!q.trim()){caja.hidden=true;return}var g={},h='';r.forEach(function(x){(g[x[2]]=g[x[2]]||[]).push(x)});Object.keys(g).forEach(function(k){h+='<h6>'+k+'</h6>'+g[k].map(function(x){return '<a href=\"'+x[1]+'\"><span>'+x[0]+'</span><small>'+x[3]+'</small></a>'}).join('')});"
      "caja.innerHTML=h||'<p>No encontramos «'+q.replace(/</g,'')+'». Prueba con tu ciudad, el modelo de tu nevecón o el código del filtro.</p>';caja.hidden=false}"
      "document.querySelectorAll('[data-aq-q]').forEach(function(i){var c=i.parentNode.querySelector('.aq-res');i.addEventListener('input',function(){pintar(c,buscar(i.value),i.value)});i.addEventListener('focus',function(){if(i.value)pintar(c,buscar(i.value),i.value)});"
      "i.addEventListener('keydown',function(e){if(e.key==='Enter'){var a=c.querySelector('a');if(a)location.href=a.getAttribute('href')}if(e.key==='Escape')c.hidden=true})});"
      "document.addEventListener('click',function(e){document.querySelectorAll('.aq-res').forEach(function(c){if(!c.parentNode.contains(e.target))c.hidden=true});document.querySelectorAll('.aq-nav details[open]').forEach(function(d){if(!d.contains(e.target))d.removeAttribute('open')})});})();")
(OUT / "buscar.js").write_text(js, encoding="utf-8")

# partes.php: el carrito y «gracias» llevan el mismo encabezado y pie
(OUT / "partes.php").write_text(r"""<?php
// Cabecera y pie de las páginas de compra (carrito, gracias, legales) con el mismo estilo del sitio.
require_once __DIR__ . '/api/sitio.php';
function marca_sitio(): ?array { return null; }
function seo_titulo(string $t): string { return $t; }
function seo_desc(string $d): string { return $d; }
function cabeza(string $titulo, string $desc, string $ruta, string $extra = '', bool $indexar = true): void
{
    $AQH = <<<'AQH'
__AQH__
AQH;
    $S = sitio();
    $canon = $S['base'] . $ruta;
    echo '<!doctype html><html lang="es-CO"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        . '<title>' . h($titulo) . '</title><meta name="description" content="' . h($desc) . '">'
        . ($indexar ? '<link rel="canonical" href="' . h($canon) . '">' : '<meta name="robots" content="noindex,nofollow">')
        . '<link rel="icon" href="/img/icono-lg.png"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        . '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600;800&family=Inter:wght@400;500;600;700&display=swap">'
        . '<link rel="stylesheet" href="/estilo.css"><link rel="stylesheet" href="/pasarela.css"><link rel="stylesheet" href="/aqua-shell.css"><script src="/buscar.js" defer></script><script src="/carrito.js" defer></script>'
        . verificacion_html() . analytics_html() . $extra . '</head><body class="tienda-samsung">' . gtm_body_html()
        . $AQH . '<main class="wrap">';
}
function pie_html(): string
{
    $AQF = <<<'AQF'
__AQF__
AQF;
    return '</main>' . $AQF . '</body></html>';
}
function pie(): void { echo pie_html(); }
""".replace("__AQH__", encoding_ := encabezado()).replace("__AQF__", pie()), encoding="utf-8")

# ---------------------------------------------------------------- portada
top3 = PS[:3]
stage = ('<div class="aq-stage"><i></i><i></i><i></i><i></i>' + "".join(f'<a class="s{i + 1}" href="{p["url"]}" aria-label="{esc(p["corto"])}"><img src="{p["img"]}" alt="Filtro de agua LG {esc(p["corto"])}, código {esc(p["ref"])}" width="300" height="300" {"loading=eager" if i == 1 else "loading=lazy"}></a>' for i, p in enumerate(top3))
         + f'<span class="aq-price-tag">Desde {cop(PREC[0])}</span></div>')
chips = "".join(f'<a href="{R_MOD(m)}">{m}</a>' for m, p in MODELOS[:2]) + "".join(f'<a href="{R_CIU(s)}">{esc(CIUDAD[s][0])}</a>' for s in TOP[:3])
hero = ('<section class="aq-hero" id="inicio"><div class="wrap"><div><span class="kicker">Distribuidor autorizado · Toda Colombia</span><h1>Filtro de Agua LG Original para tu Nevecón</h1>'
        '<p class="lead">Escoge tu referencia, agrégala al carrito y paga en línea o contra entrega. Te enviamos a tu ciudad y confirmamos que sea el filtro de tu nevecón LG antes de despachar.</p>'
        '<div class="aq-big"><form role="search" onsubmit="return false">' + ICONOS["lupa"].replace("<svg", '<svg aria-hidden="true"') + '<input type="search" data-aq-q placeholder="Escribe tu ciudad o el modelo de tu nevecón (LFX28968ST…)" autocomplete="off" aria-label="Buscar"><div class="aq-res" hidden></div></form></div>'
        f'<div class="aq-pop-chips"><span>Prueba:</span>{chips}</div><div class="aq-trust"><span>Producto nuevo y sellado</span><span>Pago seguro Wompi</span><span>Contra entrega</span><span>5 días de retracto</span></div></div>{stage}</div></section>')
qa_home = qa("¿Qué filtro de agua necesita mi nevecón LG?",
             f"Depende del modelo de tu nevecón: {esc(MOD_TXT)}. También vendemos el LT600P (5231JA2006) y el filtro externo ADQ73693903 para los equipos que lo usan. Los filtros LG cuestan entre {RANGO} con <b>envío gratis a toda Colombia</b>; "
             "pagas en línea con Wompi o contra entrega y recibes la confirmación por correo. Somos distribuidores autorizados.")
estante = seccion("Elige tu filtro LG", '<div class="tf-grid">' + "".join(tarjeta(p) for p in PS) + "</div>", sub=f"Seis referencias reales para nevecones LG, con su ficha técnica completa. Toca la foto o el nombre.").replace('<section class="aq-sec">', '<section class="aq-sec" id="filtros">', 1)
tabla_mod = ('<div class="tbl-wrap"><table class="spec-table"><tr><th>Modelo de nevecón LG</th><th>Filtro que usa</th><th>Precio</th></tr>'
             + "".join(f'<tr><td><a href="{R_MOD(m)}">{esc(m)}</a></td><td><a href="{p["url"]}">{esc(p["nombre"])}</a></td><td><b>{cop(p["precio"])}</b></td></tr>' for m, p in MODELOS) + "</table></div>"
             "<p class=\"note\" style=\"margin-top:14px\">¿Tu modelo no está en la lista? Escríbelo en el buscador o mira el código impreso en tu filtro viejo: <a href=\"cual-es-mi-filtro.html\">cómo identificar tu filtro</a>.</p>")
modelos_sec = seccion("Modelos de nevecón LG y su filtro", tabla_mod, sub="Cada modelo usa una referencia. Estos son los modelos que tenemos registrados.")
tiles = [("caja", "Nuevo y sellado", "Filtros nuevos, en su empaque, con la referencia impresa."), ("candado", "Pago seguro", "Wompi (Bancolombia): tarjeta, PSE, Nequi o botón Bancolombia."),
         ("efectivo", "Contra entrega", "Paga en efectivo a la transportadora cuando recibas tu pedido, sin recargo."), ("retorno", "5 días de retracto", "Si pediste un filtro que no corresponde, lo cambiamos sin costo (sin usar).")]
confianza = seccion("Compra tranquilo", '<div class="aq-tiles">' + "".join(f'<div class="aq-tile">{ICONOS[i]}<b>{esc(t)}</b><p>{esc(d)}</p></div>' for i, t, d in tiles) + '</div><div class="aq-pay"><span>Visa</span><span>Mastercard</span><span>PSE</span><span>Nequi</span><span>Bancolombia</span><span>Contra entrega</span></div>',
                    alt=True, sub="Una tienda en línea como las grandes: carrito, pago seguro y confirmación por correo.")
rapidas = [("¿Dónde comprar un filtro de nevecón LG en Colombia?", f"Aquí: somos distribuidores autorizados de filtros para neveras LG, con envío gratis a {len(CIU)} ciudades y municipios, pago seguro con Wompi o contra entrega y 5 días de retracto."),
           ("¿Cuánto cuesta el filtro de agua de una nevera LG?", f"Entre {RANGO}: " + ", ".join(f"{p['corto']} {cop(p['precio'])}" for p in PS) + ". Todos con envío gratis."),
           ("¿Cada cuánto se cambia el filtro de la nevera LG?", "Cada 6 meses de uso normal, o antes si el agua cambia de sabor, el hielo sale turbio o el dispensador entrega menos agua."),
           ("¿Cómo sé cuál filtro LG necesito?", f"Mira el código impreso en tu filtro viejo o el modelo de tu nevecón (etiqueta dentro del refrigerador, suele empezar por LF, LM, LR, LS o GR) y escríbelo en el buscador. Ejemplos: {MODELOS[0][0]} usa {MODELOS[0][1]['corto']}."),
           ("¿Cuánto tarda el envío?", "Entre 1 y 7 días hábiles según la ciudad; mira la página de tu ciudad para ver el tiempo exacto. El envío es gratis."),
           ("¿Puedo pagar contra entrega?", "Sí. " + FPAGO)]
rapidas_sec = seccion("Respuestas rápidas sobre filtros LG", "".join(f'<div class="qa" style="margin-bottom:14px"><p class="tag">⚡ Respuesta rápida</p><h3>{esc(q)}</h3><p>{esc(a)}</p></div>' for q, a in rapidas), sub="Las preguntas que más hacen, con la respuesta directa.")
fichas = "".join(
    f'<div class="spec-card" id="{p["slug"]}"><div class="spec-img"><img src="{p["img"]}" alt="Filtro de agua {esc(p["h"])} original" loading="lazy"></div><div class="spec-body"><h3>{esc(p["nombre"])}</h3><span class="spec-code">{esc(p["ref"])}</span>'
    f'<ul class="spec-list"><li>Equivale a: {esc(", ".join(p["refs"][1:6]) or p["ref"])}</li>' + (f'<li>Nevecones: {esc(", ".join(p["modelos"]))}</li>' if p["modelos"] else (f'<li>{esc(p["nota"])}</li>' if p["nota"] else "")) + '<li>Cámbialo cada 6 meses</li></ul>'
    f'<div class="price-row"><span class="price-tag">{cop(p["precio"])}</span><button type="button" class="btn-order" data-add="{p["id"]}">🛒 Agregar al carrito</button><a href="{p["url"]}">Ver ficha completa</a></div></div></div>' for p in PS)
fichas_sec = seccion("Ficha técnica de cada referencia", fichas, sub="Confirmamos el modelo antes de despachar: no vendemos «el que más se parece».")
comp = ('<div class="tbl-wrap"><table class="spec-table"><tr><th></th>' + "".join(f'<th><a href="{p["url"]}" style="color:#fff">{esc(p["corto"])}</a></th>' for p in PS) + "</tr>"
        "<tr><td><b>Código</b></td>" + "".join(f"<td>{esc(p['ref'])}</td>" for p in PS) + "</tr><tr><td><b>Tipo</b></td>" + "".join(f"<td>{'Externo' if p['ubic'] == 'externo' else 'Interno'}</td>" for p in PS) + "</tr>"
        "<tr><td><b>Cambio</b></td>" + "<td>6 meses</td>" * len(PS) + "</tr><tr><td><b>Precio</b></td>" + "".join(f"<td><b>{cop(p['precio'])}</b></td>" for p in PS) + "</tr></table></div>")
comp_sec = seccion("Los filtros LG, lado a lado", comp, alt=True, sub="Compara código, tipo y precio.")
cob = ('<div class="aq-top-ciu">' + "".join(f'<a href="{R_CIU(s)}">{esc(CIUDAD[s][0])}<small>{esc(CIUDAD[s][1])}</small></a>' for s in TOP) + '</div><h3 style="margin-top:26px;font-size:1.1rem">Por región y área metropolitana</h3><div class="aq-depts">'
       + "".join(f'<a href="{R_REG(k)}">{esc(v[0])}</a>' for k, v in REG.items()) + "".join(f'<a href="{R_AREA(k)}">{esc(v[0])}</a>' for k, v in AREAS.items()) + '</div><h3 style="margin-top:20px;font-size:1.1rem">Por departamento</h3><div class="aq-depts">'
       + "".join(f'<a href="{R_DEPTO(d)}">{esc(d)}</a>' for d in DEPTOS) + '</div><p style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn-solid" href="filtro-agua-lg-por-ciudad-colombia.html">Ver todas las ciudades</a><a class="btn-solid" href="ciudades-con-filtros-lg-a-z.html">Ciudades de la A a la Z</a></p>')
cob_sec = seccion(f"Llegamos a {len(CIU)} ciudades y municipios de Colombia", cob, sub="Escribe tu ciudad en el buscador de arriba o entra por tu departamento.")
FAQ_HOME = [("¿Qué filtro necesita mi nevecón LG?", "El de tu modelo: " + MOD_TXT + ". Confirma con el código de tu filtro viejo."), ("¿Cuánto cuestan los filtros LG?", f"Entre {RANGO}, con envío gratis."),
            ("¿Cómo pago?", FPAGO), ("¿Los filtros son nuevos?", "Sí, nuevos y en su empaque, con la referencia impresa."), ("¿Hay retracto?", "Sí, 5 días hábiles desde la entrega, con el filtro sin usar."),
            ("¿Son distribuidores autorizados?", "Sí, somos distribuidores autorizados de filtros para neveras LG; no somos LG Electronics ni su canal oficial de venta.")]
ld_home = [{"@type": "ItemList", "name": "Filtros de agua LG para nevecón", "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": ld_producto(p)} for i, p in enumerate(PS)]}]
pagina("index.html", "Filtro de Agua LG para Nevecón y Nevera | LT1000P, LT700P | Envío Gratis Colombia",
       f"Filtro de agua LG para nevecón y nevera: " + ", ".join(f"{p['corto']} {cop(p['precio'])}" for p in PS[:5]) + f" y externo {cop(PS[-1]['precio'])}. Distribuidores autorizados. Envío gratis y pago contra entrega en toda Colombia.",
       "filtro agua lg, filtro nevecon lg, filtro nevera lg, lt1000p, lt700p, lt800p, lt500p, lt600p, adq73693903, filtro agua refrigerador lg, precio filtro lg, filtro lg contra entrega, cambiar filtro nevecon lg",
       [("Inicio", None)], hero + qa_home + estante + modelos_sec + confianza + rapidas_sec + fichas_sec + comp_sec + cob_sec + faq_html(FAQ_HOME), FAQ_HOME, ld_home, prio="1.0")

# ---------------------------------------------------------------- fichas de producto
for p in PS:
    otros = [x for x in PS if x is not p][:3]
    equi = ", ".join(p["refs"][1:]) or p["ref"]
    qa_p = qa(f"¿Qué es el filtro {p['h']} y para qué nevecón sirve?",
              f"El <b>{esc(p['nombre'])}</b> (código {esc(p['ref'])}) es un filtro de agua {'externo, que se conecta a la manguera del agua' if p['ubic'] == 'externo' else 'interno'} para nevecones LG. Equivale a {esc(equi)}. "
              + (f"Lo usan nevecones como {esc(', '.join(p['modelos']))}. " if p["modelos"] else (esc(p["nota"]) + " " if p["nota"] else "")) + f"Cuesta <b>{cop2(p['precio'])}</b> con envío gratis a toda Colombia y se cambia cada 6 meses.")
    filas = [("Código", p["ref"]), ("También aparece como", equi), ("Tipo", "Externo (va en la manguera del agua)" if p["ubic"] == "externo" else "Interno (va dentro del nevecón)"),
             ("Nevecones LG", ", ".join(p["modelos"]) or "Confirma con el código de tu filtro viejo"), ("Precio", f"{cop2(p['precio'])} COP"), ("Envío", "Gratis a toda Colombia"), ("Cambio", "Cada 6 meses de uso normal"),
             ("Pago", "Wompi (tarjeta, PSE, Nequi, Bancolombia) o contra entrega")]
    ficha = '<div class="tbl-wrap"><table class="spec-table">' + "".join(f"<tr><th>{esc(a)}</th><td>{esc(b)}</td></tr>" for a, b in filas) + "</table></div>"
    compat = ("<h3 style=\"margin:22px 0 10px\">Nevecones que usan este filtro</h3><div class=\"city-tags\">" + "".join(f'<a href="{R_MOD(m)}">{esc(m)}</a>' for m in p["modelos"]) + "</div>") if p["modelos"] else ""
    eq_h = ("<h3 style=\"margin:22px 0 10px\">Códigos equivalentes</h3><div class=\"city-tags\">" + "".join(f'<a href="{R_REF(r)}">{esc(r)}</a>' for r in p["refs"][1:] if slug(r) in ref_vistos) + "</div>")
    pasos = (["Cierra la llave de paso del agua.", "Desconecta el filtro viejo de las mangueras.", "Conecta el filtro nuevo en el mismo sentido del flujo (mira la flecha).", "Abre la llave y revisa que no gotee.", "Saca unos 6 litros de agua para purgar el aire."]
             if p["ubic"] == "externo" else ["Abre el refrigerador y ubica el filtro.", "Retira el filtro viejo.", "Quita las tapas del filtro nuevo.", "Instálalo hasta que quede firme.", "Saca unos 6 litros de agua por el dispensador.", "Reinicia el aviso del filtro en el panel."])
    inst = '<h3 style="margin:22px 0 10px">Cómo cambiarlo</h3><ol class="vl">' + "".join(f"<li>{esc(x)}</li>" for x in pasos) + '</ol><p class="note" style="margin-top:12px">Guía completa: <a href="cambio-e-instalacion.html">cómo cambiar e instalar el filtro</a>.</p>'
    preg = [(f"¿Qué nevecones usan el {p['ref']}?", (", ".join(p["modelos"]) + ". Confirma con el código de tu filtro viejo.") if p["modelos"] else "Equipos LG que usan esta referencia; confirma con el código de tu filtro viejo o escríbenos."),
            (f"¿Qué equivale al {p['ref']}?", equi + "."), (f"¿Cuánto cuesta el filtro LG {p['ref']}?", f"{cop2(p['precio'])} con envío gratis."), ("¿Cada cuánto se cambia?", "Cada 6 meses."), ("¿Puedo pagar contra entrega?", FPAGO)]
    cuerpo = (f'<section class="hero hero-prod"><div class="wrap hero-grid"><div><span class="kicker">Repuesto original · código {esc(p["ref"])}</span><h1>Filtro de Agua LG {esc(p["corto"])} Original</h1>'
              f'<p class="sub" style="margin-top:16px;">{esc(p["nombre"])}: equivale a {esc(equi)}. {esc(", ".join(p["modelos"][:3]) + " y más." if p["modelos"] else p["nota"])}</p><div class="hero-price">{cop(p["precio"])} <small>COP · envío gratis</small></div>'
              f'<div class="hero-cta"><button type="button" class="btn btn-solid" data-add="{p["id"]}">🛒 Agregar al carrito</button></div></div>{galeria_html(p)}</div></section>'
              + qa_p + seccion("Ficha técnica", ficha + compat + eq_h + inst) + faq_html(preg)
              + seccion("Otros filtros LG", '<div class="tf-grid">' + "".join(tarjeta(x) for x in otros) + "</div>", alt=True) + GAL_JS)
    pagina(p["url"], f"Filtro de Agua LG {p['corto']} ({p['ref']}) | {cop(p['precio'])} | Envío Gratis"[:70], f"Compra el filtro de agua {p['nombre']} (código {p['ref']}) por {cop(p['precio'])}: equivale a {', '.join(p['refs'][1:4]) or p['ref']}. Envío gratis y pago contra entrega en toda Colombia.",
           f"filtro lg {p['corto'].lower()}, {p['ref'].lower()}, " + ", ".join(r.lower() for r in p["refs"][1:5]) + ", filtro nevecon lg, precio filtro lg", [("Inicio", "index.html"), ("Filtros LG", "index.html#filtros"), (p["nombre"], None)], cuerpo, preg, [ld_producto(p)], prio="0.9", og=p["img"])

# ---------------------------------------------------------------- códigos equivalentes y modelos de nevecón
for r, p in REFS:
    preg = [(f"¿Qué es el filtro LG {r}?", f"Es otro código del {p['nombre']} (referencia principal {p['ref']})."), (f"¿Cuánto cuesta el {r}?", f"{cop2(p['precio'])} con envío gratis."), ("¿Cómo lo compro?", FPAGO)]
    cuerpo = (hero_simple(f"Código {r}", f"Filtro LG {r}: es el {p['nombre']}", f"Si tu filtro viejo dice {r}, el que necesitas es el {p['nombre']} (código {p['ref']}). Es la misma pieza con otro código.")
              + qa(f"¿A qué filtro equivale el {r}?", f"El código <b>{esc(r)}</b> equivale al <b>{esc(p['nombre'])}</b> ({esc(p['ref'])}). {'Lo usan nevecones como ' + esc(', '.join(p['modelos'])) + '. ' if p['modelos'] else ''}Cuesta {cop2(p['precio'])} con envío gratis.")
              + seccion("Escoge tu filtro", '<div class="tf-grid">' + tarjeta(p) + "</div>") + faq_html(preg))
    pagina(R_REF(r), f"Filtro LG {r}: es el {p['corto']} | {cop(p['precio'])}"[:70], f"El filtro LG {r} equivale al {p['nombre']} (código {p['ref']}). {cop(p['precio'])} con envío gratis y pago contra entrega.", f"filtro lg {r.lower()}, {p['ref'].lower()}, equivalencia {r.lower()}",
           [("Inicio", "index.html"), ("Códigos", "cual-es-mi-filtro.html"), (r, None)], cuerpo, preg, [ld_producto(p)], prio="0.7")
for m, p in MODELOS:
    preg = [(f"¿Qué filtro de agua usa la nevera LG {m}?", f"El {p['nombre']} (código {p['ref']}), equivalente a {', '.join(p['refs'][1:3]) or p['ref']}."), (f"¿Cada cuánto se cambia el filtro de la {m}?", "Cada 6 meses, o antes si el agua cambia de sabor."),
            (f"¿Cuánto cuesta el filtro para la {m}?", f"{cop2(p['precio'])} con envío gratis."), (f"¿Puedo pagar contra entrega el filtro de la {m}?", FPAGO)]
    otros_m = [x for x in p["modelos"] if x != m]
    cuerpo = (hero_simple(f"Nevecón LG · {m}", f"Filtro de agua para el nevecón LG {m}", "Qué filtro usa, cómo cambiarlo y dónde comprarlo con envío a toda Colombia.")
              + qa(f"¿Qué filtro usa la nevera LG {m}?", f"La nevera LG <b>{esc(m)}</b> usa el filtro <b>{esc(p['nombre'])}</b> (código {esc(p['ref'])}). Cuesta {cop2(p['precio'])} con envío gratis y se cambia cada 6 meses.")
              + seccion("Datos del filtro", '<div class="tbl-wrap"><table class="spec-table">' + "".join(f"<tr><th>{esc(a)}</th><td>{esc(b)}</td></tr>" for a, b in [("Modelo", m), ("Filtro", p["nombre"]), ("Código", p["ref"]), ("También aparece como", ", ".join(p["refs"][1:5])), ("Precio", cop2(p["precio"])), ("Cambio", "Cada 6 meses")]) + "</table></div>"
                        + ('<h3 style="margin:22px 0 10px">Otros nevecones que usan el mismo filtro</h3><div class="city-tags">' + "".join(f'<a href="{R_MOD(x)}">{esc(x)}</a>' for x in otros_m) + "</div>" if otros_m else ""))
              + seccion("Compra el filtro de tu " + m, '<div class="tf-grid">' + tarjeta(p) + "</div>", alt=True) + faq_html(preg))
    pagina(R_MOD(m), f"Filtro de agua para nevera LG {m} | {p['corto']}"[:70], f"El filtro de agua de la nevera LG {m} es el {p['nombre']} ({cop(p['precio'])}). Cómo cambiarlo y comprarlo con envío gratis.", f"filtro nevecon lg {m.lower()}, filtro agua {m.lower()}, {p['ref'].lower()} {m.lower()}",
           [("Inicio", "index.html"), ("Modelos LG", "cual-es-mi-filtro.html"), (m, None)], cuerpo, preg, [ld_producto(p)], prio="0.8")

# ---------------------------------------------------------------- ciudades: una página con contenido propio en cada una (+ página de precio en las ciudades grandes)
RC = {"ciudades": {c[0]: ([c[0], c[1]], f"/{R_CIU(slug(c[0]))[:-5]}/") for c in CIU}, "hub": "/filtro-agua-lg-por-ciudad-colombia/"}
ciudad_unica.ads = True
for c in CIU:
    s = slug(c[0])
    vec = [(n, f"/{R_CIU(slug(n))[:-5]}/") for n, _ in [(x[0], None) for x in POR_DEPTO[c[1]]] if n != c[0]]
    u = ciudad_unica.contenido("LG", s, PS, "/", c, vec, RC)
    corto_c = c[0].split(" (")[0]
    d_ = ciudad_unica.dias_de(c)
    rng = random.Random(f"qa|{s}")
    area = next((v[0] for k, v in AREAS.items() if any(m_[0] == c[0] for m_ in v[2])), None)
    qa_t = [f"Sí. Enviamos filtros de agua LG a {corto_c} ({c[1]}) con envío gratis; llegan en {d_}. Hay {len(PS)} referencias ({', '.join(p['ref'] for p in PS[:4])}…) desde {cop(PREC[0])}. {FPAGO}",
            f"Vendemos y enviamos el filtro de tu nevecón LG a {corto_c}: entrega en {d_}, envío gratis y precios de {RANGO}. Escoge tu referencia por el código del filtro viejo o por el modelo de tu nevecón; pagas en línea o contra entrega.",
            f"En {corto_c}{' (' + area + ')' if area else ''} entregamos filtros LG en {d_}, con envío sin costo. Referencias: " + ", ".join(p["corto"] for p in PS) + f". Paga con Wompi o en efectivo al recibir."]
    cuerpo = (hero_simple(u["eyebrow"], u["h1"], html.unescape(re.sub(r"<[^>]+>", "", u["intro"]))) + qa(f"¿Envían filtros de agua LG a {corto_c}?", esc(rng.choice(qa_t))) + strip_rapida()
              + '<section class="aq-sec"><div class="wrap">' + u["cuerpo"] + "</div></section>" + faq_html(u["preguntas"], f"Preguntas de {corto_c}"))
    pagina(R_CIU(s), u["titulo"], u["desc"], f"filtro agua lg {corto_c.lower()}, filtro nevecon lg {corto_c.lower()}, comprar filtro lg {corto_c.lower()}, filtro nevera lg {c[1].lower()}", [("Inicio", "index.html"), ("Todas las ciudades", "filtro-agua-lg-por-ciudad-colombia.html"), (corto_c, None)],
           cuerpo, u["preguntas"], [{"@type": "Service", "name": f"Filtros de agua LG con envío a {c[0]}", "serviceType": "Venta de filtros de agua para nevera", "provider": {"@id": f"{DOMINIO}/#tienda"},
                                     "areaServed": {"@type": "City", "name": c[0], "containedInPlace": {"@type": "AdministrativeArea", "name": c[1]}}}], prio="0.7" if s in GRANDES_S else "0.5")
    if s in GRANDES_S:
        rng2 = random.Random(f"precio|{s}")
        orden = PS[:]
        rng2.shuffle(orden)
        filas = "".join(f'<tr><td><a href="{p["url"]}">{esc(p["nombre"])}</a></td><td>{esc(p["ref"])}</td><td><b>{cop(p["precio"])}</b></td><td>{cop(round(p["precio"] / 6))}</td></tr>' for p in orden)
        preg = [(f"¿Cuánto cuesta el filtro de una nevera LG en {corto_c}?", f"Entre {RANGO}, según la referencia, con envío gratis a {corto_c}."), (f"¿Cuál es el filtro LG más barato en {corto_c}?", f"El {min(PS, key=lambda x: x['precio'])['nombre']}, por {cop2(PREC[0])}."),
                (f"¿Puedo pagar contra entrega en {corto_c}?", FPAGO)]
        cuerpo = (hero_simple(f"Precios · {corto_c}", f"Precio del filtro de agua LG en {corto_c}", f"Cuánto cuesta cada filtro LG en {corto_c} ({c[1]}), con envío gratis y entrega en {d_}.")
                  + qa(f"¿Cuánto cuesta el filtro de agua LG en {corto_c}?", f"En {esc(corto_c)} los filtros de agua LG cuestan entre <b>{RANGO}</b> con envío gratis. El más económico es el {esc(min(PS, key=lambda x: x['precio'])['nombre'])} ({cop2(PREC[0])}). Llegan en {d_}.")
                  + seccion(f"Precios de los filtros LG en {esc(corto_c)}", '<div class="tbl-wrap"><table class="spec-table"><tr><th>Filtro</th><th>Código</th><th>Precio</th><th>Costo por mes*</th></tr>' + filas + '</table></div><p class="note" style="margin-top:12px">*Dividido en los 6 meses que dura el filtro.</p>'
                            f'<p style="margin-top:14px">Mira también el <a href="{R_CIU(s)}">envío a {esc(corto_c)}</a> y <a href="{R_DEPTO(c[1])}">los filtros LG en {esc(c[1])}</a>.</p>') + faq_html(preg))
        pagina(R_PRECIO(s), f"Precio del filtro LG en {c[0]}: desde {cop(PREC[0])}"[:70], f"Precio de los filtros de agua LG en {c[0]} ({c[1]}): {RANGO}. Envío gratis, entrega en {d_} y pago contra entrega.", f"precio filtro lg {corto_c.lower()}, cuanto cuesta filtro nevera lg {corto_c.lower()}",
               [("Inicio", "index.html"), ("Precios", "precio-filtro-agua-nevecon-lg.html"), (corto_c, None)], cuerpo, preg, [], prio="0.5")

# ---------------------------------------------------------------- departamentos, regiones, áreas, A–Z
tabla_filtros = ('<div class="tbl-wrap"><table class="spec-table"><tr><th>Filtro</th><th>Código</th><th>Precio</th></tr>' + "".join(f'<tr><td><a href="{p["url"]}">{esc(p["nombre"])}</a></td><td>{esc(p["ref"])}</td><td><b>{cop(p["precio"])}</b></td></tr>' for p in PS) + "</table></div>")
chips_c = lambda lista: '<div class="city-tags">' + "".join(f'<a href="{R_CIU(slug(c[0]))}">{esc(c[0])}</a>' for c in lista) + "</div>"
for d, lista in POR_DEPTO.items():
    preg = [(f"¿Envían filtros LG a {d}?", f"Sí, enviamos gratis a {len(lista)} {'ciudad' if len(lista) == 1 else 'ciudades'} de {d} y a otros municipios del departamento."), (f"¿Cuánto cuesta el filtro LG en {d}?", f"Entre {RANGO}, con envío gratis."), ("¿Puedo pagar contra entrega?", FPAGO)]
    cuerpo = (hero_simple(f"Cobertura · {d}", f"Filtros de agua LG en {d}", f"Envío gratis a {len(lista)} {'ciudad' if len(lista) == 1 else 'ciudades'} de {d}, con pago en línea o contra entrega.")
              + qa(f"¿Envían filtros de agua LG a {d}?", f"Sí. Vendemos los filtros LG {', '.join(p['corto'] for p in PS)} con envío gratis a {len(lista)} {'ciudad' if len(lista) == 1 else 'ciudades'} de {esc(d)}. Precios de {RANGO}; {esc(FPAGO)}")
              + seccion(f"Ciudades de {esc(d)} donde enviamos", chips_c(lista) + "<h3 style=\"margin:24px 0 10px\">Filtros disponibles</h3>" + tabla_filtros) + faq_html(preg))
    pagina(R_DEPTO(d), f"Filtros LG en {d}: envío y precios"[:70], f"Compra filtros de agua LG con envío gratis en {d}: {len(lista)} {'ciudad' if len(lista) == 1 else 'ciudades'}, precios de {RANGO} y pago en línea o contra entrega.", f"filtro agua lg {d.lower()}, filtro nevecon lg {d.lower()}",
           [("Inicio", "index.html"), ("Todas las ciudades", "filtro-agua-lg-por-ciudad-colombia.html"), (d, None)], cuerpo, preg, [], prio="0.6")
for k, (nombre_r, deptos, grandes) in REG.items():
    n_ciu = sum(len(POR_DEPTO[d]) for d in deptos)
    filas = "".join(f'<tr><td><a href="{R_DEPTO(d)}">{esc(d)}</a></td><td>{len(POR_DEPTO[d])}</td><td>{esc(", ".join(c[0].split(" (")[0] for c in POR_DEPTO[d][:4]))}…</td></tr>' for d in deptos)
    preg = [(f"¿Envían filtros LG a la {nombre_r}?", f"Sí, enviamos gratis a {n_ciu} ciudades de la {nombre_r}, entre ellas {grandes}."), (f"¿Cuánto cuesta el filtro LG en la {nombre_r}?", f"Entre {RANGO}, con envío gratis."), ("¿Puedo pagar contra entrega?", FPAGO)]
    cuerpo = (hero_simple(f"Cobertura · {nombre_r}", f"Filtros de agua LG en la {nombre_r}", f"Envío gratis a {n_ciu} ciudades de {len(deptos)} {'departamento' if len(deptos) == 1 else 'departamentos'}.")
              + qa(f"¿Envían filtros de agua LG a la {nombre_r}?", f"Sí: {esc(grandes)} y {n_ciu - 1} municipios más. Filtros LG de {RANGO} con envío gratis; {esc(FPAGO)}")
              + seccion("Departamentos donde entregamos", '<div class="tbl-wrap"><table class="spec-table"><tr><th>Departamento</th><th>Ciudades</th><th>Algunas</th></tr>' + filas + "</table></div><h3 style=\"margin:24px 0 10px\">Filtros disponibles</h3>" + tabla_filtros) + faq_html(preg))
    pagina(R_REG(k), f"Filtro de agua LG en la {nombre_r}"[:70], f"Filtros de agua LG con envío gratis a {n_ciu} ciudades de la {nombre_r}. Paga en línea o contra entrega.", f"filtro agua lg {k.lower()}, filtro nevecon lg región {k.lower()}",
           [("Inicio", "index.html"), ("Todas las ciudades", "filtro-agua-lg-por-ciudad-colombia.html"), (nombre_r, None)], cuerpo, preg, [], prio="0.6")
for k, (corto, largo, miembros) in AREAS.items():
    lista = ", ".join(c[0].split(" (")[0] for c in miembros)
    preg = [(f"¿Entregan filtros LG en {largo}?", f"Sí, enviamos gratis a {lista}."), (f"¿Cuánto cuesta el filtro LG en {corto}?", f"Entre {RANGO}, con envío gratis."), ("¿Puedo pagar contra entrega?", FPAGO)]
    cuerpo = (hero_simple(f"Cobertura · {corto}", f"Filtro de agua LG en {largo}", f"Envío gratis a {len(miembros)} municipios, con pago en línea o contra entrega.")
              + qa(f"¿Entregan filtros de agua LG en {largo}?", f"Sí: {esc(lista)}. Filtros LG de {RANGO} con envío gratis.") + seccion(f"Municipios de {esc(corto)} con envío", chips_c(miembros) + "<h3 style=\"margin:24px 0 10px\">Escoge tu filtro</h3><div class=\"tf-grid\">" + "".join(tarjeta(p) for p in PS[:3]) + "</div>") + faq_html(preg))
    pagina(R_AREA(k), f"Filtro de agua LG en {corto}: envío gratis"[:70], f"Filtros de agua LG en {largo}: {lista}. Envío gratis y pago en línea o contra entrega.", f"filtro agua lg {corto.lower()}, filtro nevecon lg {lista.lower()}",
           [("Inicio", "index.html"), ("Todas las ciudades", "filtro-agua-lg-por-ciudad-colombia.html"), (corto, None)], cuerpo, preg, [], prio="0.6")
por_letra = {}
for c in sorted(CIU, key=lambda c: slug(c[0])):
    por_letra.setdefault(slug(c[0])[0].upper(), []).append(c)
letras = "".join(f'<a href="#letra-{l}">{l}</a>' for l in sorted(por_letra))
az = "".join(f'<h3 id="letra-{l}" style="margin:22px 0 8px">{l}</h3><div class="city-tags">' + "".join(f'<a href="{R_CIU(slug(c[0]))}" title="{esc(c[1])}">{esc(c[0])}</a>' for c in v) + "</div>" for l, v in sorted(por_letra.items()))
pagina("ciudades-con-filtros-lg-a-z.html", f"Filtros LG por ciudad de la A a la Z", f"Lista alfabética de las {len(CIU)} ciudades y municipios donde enviamos filtros de agua LG con envío gratis.", "filtro agua lg por ciudad, ciudades filtro nevecon lg",
       [("Inicio", "index.html"), ("Todas las ciudades", "filtro-agua-lg-por-ciudad-colombia.html"), ("A–Z", None)], hero_simple("Cobertura · A–Z", f"Filtros LG en {len(CIU)} ciudades, de la A a la Z", "Busca tu ciudad por su inicial.")
       + qa("¿En qué ciudades venden filtros LG?", f"En {len(CIU)} ciudades y municipios de Colombia, con envío gratis. Busca la tuya por su inicial.") + seccion("Ciudades", '<div class="city-tags" style="margin-bottom:16px">' + letras + "</div>" + az), prio="0.6")
hub_c = "".join(f'<div class="dept"><h4><a href="{R_DEPTO(d)}">{esc(d)}</a></h4>' + chips_c(POR_DEPTO[d]) + "</div>" for d in DEPTOS)
pagina("filtro-agua-lg-por-ciudad-colombia.html", f"Filtros de agua LG en {len(CIU)} ciudades de Colombia", f"Enviamos filtros de agua LG con envío gratis a {len(CIU)} ciudades y municipios de Colombia: busca la tuya, mira el tiempo de entrega y compra en línea.",
       "filtro agua lg colombia, filtro nevecon lg ciudades", [("Inicio", "index.html"), ("Todas las ciudades", None)], hero_simple("Cobertura", "Filtros de agua LG en toda Colombia", f"Escoge tu ciudad: enviamos a {len(CIU)} ciudades y municipios.")
       + qa("¿A qué ciudades de Colombia envían filtros LG?", f"A {len(CIU)} ciudades y municipios de {len(DEPTOS)} departamentos, con envío gratis y pago en línea o contra entrega.") + seccion("Elige tu ciudad", hub_c), prio="0.8")

# ---------------------------------------------------------------- guías y páginas de ayuda
for sl, titulo, desc, resumen, cuerpo_a, preguntas in ARTS:
    otros = [x for x in ARTS if x[0] != sl][:4]
    cuerpo = (hero_simple("Guía · Filtros LG", titulo, desc) + qa(titulo, esc(resumen)) + seccion(esc(titulo), '<div class="prose">' + cuerpo_a + "</div>") + faq_html(preguntas)
              + seccion("Sigue leyendo", '<div class="link-grid">' + "".join(f'<a href="{U(o[0])}">{esc(o[1])}<small>{esc(o[2][:90])}</small></a>' for o in otros) + "</div>", alt=True))
    art = {"@type": "Article", "headline": titulo, "description": desc, "inLanguage": "es-CO", "datePublished": HOY, "dateModified": HOY, "author": {"@type": "Organization", "name": "Filtro de Agua LG Colombia"}, "publisher": {"@id": f"{DOMINIO}/#tienda"}}
    pagina(U(sl), titulo[:70], desc, "filtro lg, nevera lg, " + sl.replace("-", " "), [("Inicio", "index.html"), ("Guías", "guias-filtro-agua-nevecon-lg.html"), (titulo, None)], cuerpo, preguntas, [art], prio="0.7")
pagina("guias-filtro-agua-nevecon-lg.html", "Guías del filtro de agua LG: cambio, precio, modelos", "Guías prácticas sobre filtros de agua para nevecón LG: cómo escoger el filtro, cada cuánto cambiarlo, reiniciar el aviso, problemas comunes y precios.", "guias filtro lg",
       [("Inicio", "index.html"), ("Guías", None)], hero_simple("Guías", "Guías del filtro de agua para nevecón LG", "Respuestas claras para escoger, cambiar y cuidar tu filtro.") + qa("¿Dónde aprendo a cambiar el filtro de mi nevecón LG?", "En estas guías: cómo identificarlo, cada cuánto cambiarlo, cómo reiniciar el aviso y qué hacer si el dispensador no saca agua.")
       + seccion("Todas las guías", '<div class="link-grid">' + "".join(f'<a href="{U(sl)}">{esc(t)}<small>{esc(d[:100])}</small></a>' for sl, t, d, _, _, _ in ARTS) + "</div>"), prio="0.7")
pasos_i = [("Ubica el filtro", "En los nevecones LG el filtro interno suele estar dentro del refrigerador; el externo va en la manguera del agua, por fuera."), ("Retira el viejo", "Sácalo con cuidado; puede salir un poco de agua."),
           ("Instala el nuevo", "Quita las tapas protectoras e instálalo hasta que quede firme, siguiendo las marcas del filtro."), ("Purga el aire", "Saca unos 6 litros de agua por el dispensador."), ("Reinicia el aviso", "Mantén presionado el botón del filtro en el panel unos segundos.")]
preg_i = [("¿Necesito técnico para cambiar el filtro?", "No, toma unos minutos y no requiere herramientas."), ("¿Cuánta agua debo sacar?", "Unos 6 litros."), ("¿Cada cuánto lo cambio?", "Cada 6 meses.")]
pagina("cambio-e-instalacion.html", "Cómo cambiar el filtro de agua de la nevera LG: paso a paso", "Paso a paso para cambiar el filtro de agua de tu nevecón LG en minutos, purgar el aire y reiniciar el aviso del filtro.", "cambiar filtro nevecon lg, instalar filtro lg",
       [("Inicio", "index.html"), ("Guías", "guias-filtro-agua-nevecon-lg.html"), ("Cómo cambiar el filtro", None)], hero_simple("Guía", "Cómo cambiar el filtro de agua de tu nevecón LG", "Cinco pasos, unos minutos y sin herramientas.")
       + qa("¿Cómo se cambia el filtro de una nevera LG?", "Ubica el filtro, retira el viejo, instala el nuevo hasta que quede firme, saca unos 6 litros de agua y reinicia el aviso del filtro. Todo toma unos minutos.")
       + seccion("Paso a paso", '<div class="vline">' + "".join(f'<div class="vstep"><h4>{esc(t)}</h4><p>{esc(d)}</p></div>' for t, d in pasos_i) + "</div>") + faq_html(preg_i), preg_i, [], prio="0.8")
modelos_tab = '<div class="tbl-wrap"><table class="spec-table"><tr><th>Modelo de nevecón</th><th>Filtro</th><th>Código</th></tr>' + "".join(f'<tr><td><a href="{R_MOD(m)}">{esc(m)}</a></td><td><a href="{p["url"]}">{esc(p["nombre"])}</a></td><td>{esc(p["ref"])}</td></tr>' for m, p in MODELOS) + "</table></div>"
refs_tab = '<div class="tbl-wrap"><table class="spec-table"><tr><th>Código del filtro viejo</th><th>Es el filtro</th></tr>' + "".join(f'<tr><td>{esc(r)}</td><td><a href="{p["url"]}">{esc(p["nombre"])}</a></td></tr>' for p in PS for r in p["refs"]) + "</table></div>"
pagina("cual-es-mi-filtro.html", "¿Cuál es mi filtro LG? Por modelo o por código", "Encuentra el filtro de agua de tu nevecón LG por el modelo (LFX28968ST, LRMVS3006S…) o por el código impreso en el filtro viejo.", "cual es mi filtro lg, equivalencias filtro lg",
       [("Inicio", "index.html"), ("¿Cuál es mi filtro?", None)], hero_simple("Identifica tu filtro", "¿Cuál es el filtro de mi nevecón LG?", "Por el modelo de tu nevecón o por el código de tu filtro viejo.")
       + qa("¿Cómo sé qué filtro LG necesito?", f"Mira el código impreso en el filtro viejo o el modelo de tu nevecón (etiqueta dentro del refrigerador; en LG suele empezar por LF, LM, LR, LS o GR). Ejemplos: {esc(MODELOS[0][0])} usa {esc(MODELOS[0][1]['corto'])}; {esc(MODELOS[4][0])} usa {esc(MODELOS[4][1]['corto'])}.")
       + seccion("Por modelo de nevecón", modelos_tab) + seccion("Por código del filtro viejo", refs_tab, alt=True), prio="0.8")
pagina("precio-filtro-agua-nevecon-lg.html", f"Precio del filtro de agua LG en Colombia: {RANGO}", f"Precios de los filtros de agua para nevecón LG en Colombia: {', '.join(p['corto'] + ' ' + cop(p['precio']) for p in PS)}. Envío gratis.", "precio filtro lg, cuanto cuesta filtro nevera lg",
       [("Inicio", "index.html"), ("Precios", None)], hero_simple("Precios", "Precio del filtro de agua LG en Colombia", "Todos con envío gratis y pago en línea o contra entrega.")
       + qa("¿Cuánto cuesta un filtro de agua para nevera LG?", f"Entre {RANGO}: " + ", ".join(f"{esc(p['corto'])} {cop2(p['precio'])}" for p in PS) + ". Envío gratis.") + seccion("Lista de precios", tabla_filtros + '<div class="tf-grid" style="margin-top:22px">' + "".join(tarjeta(p) for p in PS) + "</div>"), prio="0.8")
pagina("envio-filtros-lg-colombia.html", "Envío de filtros LG a toda Colombia: gratis y con guía", f"Enviamos filtros de agua LG a {len(CIU)} ciudades de Colombia con envío gratis, guía de seguimiento y pago en línea o contra entrega.", "envio filtro lg colombia",
       [("Inicio", "index.html"), ("Envíos", None)], hero_simple("Envíos", "Envío de filtros LG a toda Colombia", "Gratis, con guía de seguimiento.") + qa("¿Cuánto tarda y cuánto cuesta el envío?", "El envío es gratis y tarda entre 1 y 7 días hábiles según tu ciudad; recibes guía de seguimiento. Mira la página de tu ciudad para el tiempo exacto.")
       + seccion("Elige tu ciudad", hub_c), prio="0.7")
pagina("garantia-cambio-y-devolucion-filtro-lg.html", "Garantía, cambio y devolución del filtro LG", "Tienes 5 días hábiles de retracto desde la entrega con el filtro sin usar. Así funciona el cambio y la devolución.", "garantia filtro lg",
       [("Inicio", "index.html"), ("Garantía y devolución", None)], hero_simple("Compra protegida", "Garantía, cambio y devolución", "Cinco días hábiles de retracto.") + qa("¿Puedo devolver el filtro?", "Sí, tienes 5 días hábiles desde la entrega con el filtro sin usar. Si pediste una referencia que no corresponde a tu nevecón, la cambiamos."), prio="0.5")
terminos_g = [(p["h"], f"Filtro LG de código {p['ref']}. Equivale a {', '.join(p['refs'][1:5]) or p['ref']}." + (f" Usado en nevecones como {', '.join(p['modelos'][:4])}." if p["modelos"] else "")) for p in PS]
terminos_g += [("Referencia o código", "Número impreso en el filtro que identifica la pieza exacta."), ("Equivalencia", "Una misma pieza puede aparecer con varios códigos; todos corresponden al mismo filtro."), ("Nevecón", "Forma colombiana de llamar a un refrigerador grande con dispensador de agua y hielo."),
               ("French door", "Nevecón con dos puertas de refrigerador arriba y cajón de congelador abajo."), ("Side by side", "Nevecón con refrigerador y congelador lado a lado."), ("Aviso del filtro", "Indicador del panel que se enciende cuando toca cambiar el filtro."),
               ("Purga", "Sacar unos 6 litros de agua tras el cambio para eliminar el aire."), ("Retracto", "Derecho a devolver el producto sin usar dentro de 5 días hábiles.")]
pagina("glosario-filtro-nevera-lg.html", "Glosario: códigos y términos del filtro LG", "Qué significa cada código y término del filtro de agua LG: " + ", ".join(p["ref"] for p in PS[:5]) + ", aviso del filtro, purga y retracto.", "glosario filtro lg, que significa lt1000p",
       [("Inicio", "index.html"), ("Guías", "guias-filtro-agua-nevecon-lg.html"), ("Glosario", None)], hero_simple("Glosario", "Glosario del filtro de agua para nevecón LG", "Qué significa cada código y cada término.") + qa("¿Qué significan LT1000P, LT700P y los demás códigos?", "Son las referencias de los filtros de agua LG: " + esc("; ".join(f"{p['corto']} = {p['nombre']}" for p in PS)) + ". Cada uno tiene códigos equivalentes.")
       + seccion("Términos", '<dl class="m-ficha">' + "".join(f"<dt>{esc(a)}</dt><dd>{esc(b)}</dd>" for a, b in terminos_g) + "</dl>"), terminos_g[:6], [], prio="0.6")
G = marcas_contenido_lg.preguntas_ia(PS, slug)
todas = [qa_ for _, l in G for qa_ in l]
faq_g = "".join(f'<h3 style="margin:24px 0 10px">{esc(g)}</h3><div class="faq-num">' + "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in l) + "</div>" for g, l in G)
pagina("preguntas-frecuentes-filtro-agua-lg.html", f"Preguntas frecuentes sobre filtros de nevera LG ({len(todas)} respuestas)", f"{len(todas)} respuestas sobre filtros de agua para nevera LG: " + ", ".join(p["ref"] for p in PS[:5]) + ", equivalencias, precios, pago contra entrega y cómo cambiarlos.", "preguntas frecuentes filtro lg",
       [("Inicio", "index.html"), ("Preguntas frecuentes", None)], hero_simple("Respuestas rápidas", "Preguntas frecuentes sobre filtros de nevera LG", "Respuestas directas, listas para ti y para los asistentes de IA.")
       + qa("¿Qué filtro usa mi nevera LG y cuánto cuesta?", f"Depende del modelo: {esc(MOD_TXT)}. Cuestan entre {RANGO} con envío gratis a toda Colombia.") + seccion("Todas las preguntas", faq_g), todas, [], prio="0.8")
mapa = lambda t, its: f'<h2 style="font-size:22px;margin:22px 0 10px">{esc(t)}</h2><ul class="spec-list">' + "".join(f'<li><a href="{u}">{esc(n)}</a></li>' for n, u in its) + "</ul>"
cuerpo = (mapa("Filtros", [(f"{p['nombre']} · {cop(p['precio'])}", p["url"]) for p in PS]) + mapa("Guías", [(t, U(sl)) for sl, t, d, _, _, _ in ARTS] + [("Cómo cambiar el filtro", "cambio-e-instalacion.html"), ("¿Cuál es mi filtro?", "cual-es-mi-filtro.html")])
          + mapa("Modelos de nevecón", [(m, R_MOD(m)) for m, p in MODELOS]) + mapa("Códigos", [(r, R_REF(r)) for r, p in REFS]) + mapa("Regiones", [(v[0], R_REG(k)) for k, v in REG.items()]) + mapa("Áreas metropolitanas", [(v[0], R_AREA(k)) for k, v in AREAS.items()])
          + mapa("Departamentos", [(f"Filtros LG en {d}", R_DEPTO(d)) for d in DEPTOS]) + mapa("Ayuda", [("Preguntas frecuentes", "preguntas-frecuentes-filtro-agua-lg.html"), ("Glosario", "glosario-filtro-nevera-lg.html"), ("Precios", "precio-filtro-agua-nevecon-lg.html"),
                                                                                                         ("Envíos", "envio-filtros-lg-colombia.html"), ("Ciudades A–Z", "ciudades-con-filtros-lg-a-z.html"), ("Todas las ciudades", "filtro-agua-lg-por-ciudad-colombia.html")]))
pagina("mapa-del-sitio.html", "Mapa del sitio | Filtros de agua LG", "Todas las páginas de la tienda de filtros de agua LG: filtros, guías, regiones, departamentos, ciudades, códigos y modelos.", "mapa del sitio filtro lg",
       [("Inicio", "index.html"), ("Mapa del sitio", None)], hero_simple("Mapa del sitio", "Mapa del sitio: filtros LG", "Todas las páginas en un solo lugar.") + qa("¿Qué hay en esta tienda?", f"Seis filtros de agua LG, {len(MODELOS)} modelos de nevecón, {len(REFS)} códigos equivalentes, {len(CIU)} ciudades, guías y preguntas frecuentes.") + seccion("Páginas", cuerpo), prio="0.4")
(OUT / "404.html").write_text("<!DOCTYPE html><html lang='es-CO'><head><meta charset='utf-8'><meta name='robots' content='noindex'><title>Página no encontrada</title></head><body style='font-family:sans-serif;padding:40px'><h1>Página no encontrada</h1><p><a href='index.html'>Ir al inicio</a></p></body></html>", encoding="utf-8")

# ---------------------------------------------------------------- robots, sitemap, llms y .htaccess
(OUT / "robots.txt").write_text("User-agent: *\nAllow: /\nDisallow: /carrito.php\nDisallow: /gracias.php\nDisallow: /admin.php\nDisallow: /diagnostico.php\nDisallow: /opinion.php\nDisallow: /api/\nDisallow: /data/\n\n"
                                + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in ("GPTBot", "ChatGPT-User", "OAI-SearchBot", "ClaudeBot", "Claude-Web", "Claude-SearchBot", "Claude-User", "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot-Extended", "Bingbot", "Googlebot"))
                                + f"Sitemap: {DOMINIO}/sitemap.xml\n", encoding="utf-8")
(OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>{DOMINIO}/{'' if n == 'index.html' else n}</loc><lastmod>{HOY}</lastmod><changefreq>weekly</changefreq><priority>{pr}</priority></url>\n" for n, pr, _, _ in PAGINAS) + "</urlset>\n", encoding="utf-8")
ll = [f"# Filtro de Agua LG Colombia", "", f"> Tienda en línea de filtros de agua para nevecones LG en Colombia. Distribuidores autorizados. Envío gratis a {len(CIU)} ciudades, pago con Wompi (tarjeta, PSE, Nequi, Bancolombia) o contra entrega, 5 días de retracto.", "",
      "## Filtros y precios (COP, envío gratis)"] + [f"- [{p['nombre']}]({DOMINIO}/{p['url']}): {cop(p['precio'])}. Equivale a {', '.join(p['refs'][1:5]) or p['ref']}." + (f" Nevecones: {', '.join(p['modelos'])}." if p["modelos"] else "") for p in PS]
ll += ["", "## Respuestas rápidas"] + [f"- **{q}** {a}" for q, a in rapidas] + ["", "## Páginas principales", f"- [Cuál es mi filtro]({DOMINIO}/cual-es-mi-filtro.html)", f"- [Precios]({DOMINIO}/precio-filtro-agua-nevecon-lg.html)", f"- [Cómo cambiar el filtro]({DOMINIO}/cambio-e-instalacion.html)",
                                                                                   f"- [Preguntas frecuentes]({DOMINIO}/preguntas-frecuentes-filtro-agua-lg.html)", f"- [Todas las ciudades]({DOMINIO}/filtro-agua-lg-por-ciudad-colombia.html)", f"- [Mapa del sitio]({DOMINIO}/mapa-del-sitio.html)", "", "## Guías"] + [f"- [{t}]({DOMINIO}/{U(sl)}): {d}" for sl, t, d, _, _, _ in ARTS]
(OUT / "llms.txt").write_text("\n".join(ll) + "\n", encoding="utf-8")
(OUT / ".htaccess").write_text("DirectoryIndex index.html index.php\nErrorDocument 404 /404.html\nOptions -Indexes\nRewriteEngine On\nRewriteCond %{HTTPS} off\nRewriteCond %{HTTP:X-Forwarded-Proto} !https\nRewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]\n"
                               "RewriteCond %{HTTP_HOST} ^www\\.(.+)$ [NC]\nRewriteRule ^ https://%1%{REQUEST_URI} [L,R=301]\n<FilesMatch \"\\.(sqlite|sqlite-wal|sqlite-shm|log)$\">\n  Require all denied\n</FilesMatch>\n", encoding="utf-8")
print(f"listo: {OUT} · {len(PAGINAS)} páginas · {len(CIU)} ciudades · {len(PS)} filtros")
