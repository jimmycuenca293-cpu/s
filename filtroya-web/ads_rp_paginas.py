# Páginas de la tienda de repuestos de línea blanca. Se ejecuta dentro de ads_rp.py (comparte sus funciones y datos).
FPAGO = "Pagas en línea con Wompi (tarjeta, PSE, Nequi o Bancolombia) o contra entrega, en efectivo, sin recargo."
N_CIU = int(os.environ.get("TIENDA_CIUDADES", "20"))
R_EQ = lambda eq: f"repuestos-para-{slug(eq)}.html"
R_CAT = lambda eq, cat: f"{slug(cat)}-para-{slug(eq)}.html"
R_EQM = lambda eq, m: f"repuestos-para-{slug(eq)}-{slug(m)}.html"
MT = {}
for _p in PS:
    if _p["marca_eq"] and _p["marca_eq"] != "Todas las marcas":
        MT.setdefault((_p["equipos_l"][0], _p["categoria"], _p["marca_eq"]), []).append(_p)
mt_url = lambda eq, c, m: f"{slug(c)}-para-{slug(eq)}-{slug(m)}.html"
EQ_LISTA = list(EQUIPOS)
CATS_TXT = ", ".join(dict.fromkeys(c.lower() for p_ in PS for c in [p_["categoria"]]))
HAY_PRESO = any(p_["categoria"] == "Presostatos" for p_ in PS)
PREG_PV = {}


GAL_CSS = """
.tf-img{background:#fff!important;border-bottom:1px solid #e6ebf6}.tf-card{border:1px solid #e3e8f4!important}.g2-main{background:#fff!important;border:1px solid #e3e8f4}.hx-i{background:#fff!important}
.g2{display:grid;gap:12px}.g2-main{position:relative;overflow:hidden;border-radius:20px;background:linear-gradient(160deg,#eef3ff,#dfe8fb);aspect-ratio:1;cursor:zoom-in;touch-action:manipulation}
.g2-main img{width:100%;height:100%;object-fit:contain;display:block;transition:transform .18s ease-out;will-change:transform}.g2-main.z{cursor:zoom-out}.g2-main.z img{transform:scale(2.2)}
.g2-lupa{position:absolute;right:12px;bottom:12px;background:#fff;border-radius:999px;padding:6px 12px;font:700 12px Inter,sans-serif;color:#1428a0;box-shadow:0 4px 12px rgba(0,0,0,.15);pointer-events:none}
.g2-th{display:flex;gap:10px;flex-wrap:wrap}.g2-th button{width:84px;height:84px;border-radius:12px;border:2px solid #dbe3f5;background:#fff;padding:4px;cursor:pointer}.g2-th button[aria-selected=true]{border-color:#1428a0;box-shadow:0 0 0 3px rgba(20,40,160,.15)}.g2-th img{width:100%;height:100%;object-fit:contain;display:block}
.g2-tip{margin:0;font-size:13px;color:#5b6478}
.pay2{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:6px}.pay2 .btn{width:100%;justify-content:center;align-items:center;flex-direction:column;gap:2px;min-height:58px;font-size:1rem;text-align:center}.pay2 .btn small{display:block;font-weight:500;font-size:.72rem;opacity:.85}
.btn.cod{background:#fff;color:#0f1f80;border:2px solid #1428a0}.btn.cod:hover{background:#eef2ff}.pay2-sec{margin:10px 0 0}.pay2-sec button{background:none;border:0;color:#1428a0;font:600 .95rem Inter,sans-serif;cursor:pointer;text-decoration:underline;padding:0}
.tf-cod{width:auto;margin:8px 20px 0;padding:13px;border-radius:99px;border:2px solid #1428a0;background:#fff;color:#0f1f80;font:700 .95rem Inter,sans-serif;cursor:pointer}.tf-cod:hover{background:#eef2ff}
@media(max-width:560px){.pay2{grid-template-columns:1fr}.g2-th button{width:68px;height:68px}}
"""
(OUT / "tema.css").write_text((OUT / "tema.css").read_text(encoding="utf-8") + GAL_CSS, encoding="utf-8")

HX_CSS = """
.hx{background:#f4f7fc;border-bottom:1px solid #e1e7f3;padding:46px 0}.hx-g{display:grid;grid-template-columns:1.05fr 1fr;gap:44px;align-items:center}
.hx-k{display:inline-block;color:#1428a0;font:700 13px Inter,sans-serif;letter-spacing:.07em;text-transform:uppercase;margin-bottom:14px}
.hx h1{font-size:clamp(2rem,3.6vw,3.05rem);line-height:1.08;color:#0b1f4d;margin:0 0 16px}.hx p{color:#4a5876;font-size:1.1rem;line-height:1.6;max-width:52ch;margin:0 0 24px}
.hx-b{display:flex;gap:12px;flex-wrap:wrap}.hx-b a{display:inline-flex;align-items:center;justify-content:center;min-height:52px;padding:0 26px;border-radius:12px;font:700 1rem Inter,sans-serif;text-decoration:none}
.hx-p{background:#1428a0;color:#fff}.hx-p:hover{background:#0f1f80}.hx-w{background:#fff;color:#0f1f80;border:2px solid #1faa59}.hx-w:hover{background:#f0fbf4}
.hx-u{list-style:none;padding:0;margin:24px 0 0;display:grid;grid-template-columns:1fr 1fr;gap:10px 20px;color:#2a3a5c;font-weight:600;font-size:.95rem}.hx-u li:before{content:"✓";color:#1faa59;margin-right:8px;font-weight:800}
.hx-r{display:grid;grid-template-columns:1fr 1fr;gap:14px}.hx-t{background:#fff;border:1px solid #e1e7f3;border-radius:16px;padding:14px;display:flex;flex-direction:column;gap:6px;text-decoration:none;color:#0f1b33;box-shadow:0 8px 24px rgba(11,31,77,.06);transition:.2s}
.hx-a{display:flex;flex-direction:column;gap:6px;text-decoration:none;color:inherit}.hx-bt{display:grid;gap:6px;margin-top:8px}.hx-bt button{min-height:40px;border-radius:10px;font:700 .85rem Inter,sans-serif;cursor:pointer}.hx-bt .tf-add{background:#1428a0!important;color:#fff!important;border:0!important;border-radius:10px!important;box-shadow:none!important;width:auto!important;margin:0!important}.hx-bt .tf-cod{border-radius:10px!important}.hero-prod .pay2 .btn-solid{background:#1428a0!important;color:#fff!important}.hero-prod .pay2 .btn-solid small{color:#dbe3ff}.hx-bt .tf-cod{background:#fff;color:#1428a0;border:1.5px solid #1428a0;margin:0!important;width:auto!important}.hx-t:hover{transform:translateY(-3px);box-shadow:0 14px 32px rgba(11,31,77,.12)}.hx-i{aspect-ratio:4/3;display:grid;place-items:center;background:#f4f7fc;border-radius:10px;overflow:hidden}.hx-i img{width:90%;height:90%;object-fit:contain}
.hx-t b{font-size:.92rem;line-height:1.25;font-weight:700}.hx-t span{font-weight:800;color:#1428a0;font-size:1.05rem}
@media(max-width:900px){.hx{padding:30px 0}.hx-g{grid-template-columns:1fr;gap:26px}.hx-u{grid-template-columns:1fr}.hx-b a{flex:1}}
"""
(OUT / "tema.css").write_text((OUT / "tema.css").read_text(encoding="utf-8") + HX_CSS, encoding="utf-8")
GAL_JS = ("<script>(function(){document.querySelectorAll('[data-g2]').forEach(function(g){var m=g.querySelector('.g2-main'),i=m.querySelector('img');"
          "g.querySelectorAll('.g2-th button').forEach(function(b){b.addEventListener('click',function(){g.querySelectorAll('.g2-th button').forEach(function(x){x.setAttribute('aria-selected','false')});b.setAttribute('aria-selected','true');i.src=b.dataset.src;i.alt=b.dataset.alt;m.classList.remove('z');i.style.transformOrigin='50% 50%'})});"
          "function o(e){var r=m.getBoundingClientRect(),t=e.touches?e.touches[0]:e;i.style.transformOrigin=((t.clientX-r.left)/r.width*100)+'% '+((t.clientY-r.top)/r.height*100)+'%'}"
          "m.addEventListener('mouseenter',function(){if(matchMedia('(hover:hover)').matches)m.classList.add('z')});m.addEventListener('mouseleave',function(){m.classList.remove('z')});m.addEventListener('mousemove',o);"
          "m.addEventListener('click',function(e){if(!matchMedia('(hover:hover)').matches){o(e);m.classList.toggle('z')}});})})();</script>")


def ficha_img(p, filas):
    from PIL import Image as _I, ImageDraw as _D, ImageFont as _F
    B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"; R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
    W = 1200; im = _I.new("RGB", (W, W), "#f2f6ff"); d = _D.Draw(im)
    d.rectangle((0, 0, W, 210), fill="#1428a0"); fb = _F.truetype(B, 46); fr = _F.truetype(R, 34); fk = _F.truetype(B, 30)
    t = p["nombre"]; lineas = []; actual = ""
    for w in t.split():
        if d.textlength(actual + " " + w, font=fb) > W - 120 and actual:
            lineas.append(actual); actual = w
        else:
            actual = (actual + " " + w).strip()
    lineas.append(actual)
    y = 36
    for l in lineas[:3]:
        d.text((60, y), l, fill="white", font=fb); y += 56
    d.text((60, 172), "Ficha técnica", fill="#ffc21a", font=fk)
    y = 250
    for a, b in filas[:9]:
        d.rounded_rectangle((50, y, W - 50, y + 84), radius=16, fill="white" if (y // 90) % 2 else "#e8eeff")
        d.text((80, y + 24), a, fill="#1428a0", font=fk)
        v = b if d.textlength(b, font=fr) < 560 else b[:36] + "…"
        d.text((560, y + 22), v, fill="#14213d", font=fr); y += 92
    if y < 860:
        _f = _I.open(OUT / "img" / f"p-{p['id']}.webp").convert("RGBA"); _f.thumbnail((300, 300)); im.paste(_f, (W - 360, y + 10), _f)
    d.text((60, W - 70), "Envío a toda Colombia · Pago con Wompi o contra entrega", fill="#5b6478", font=_F.truetype(R, 30))
    im.save(OUT / "img" / f"p-{p['id']}-ficha.webp", "WEBP", quality=88, method=6)


def galeria_html(p, filas=None):
    fotos = [(p["img"], p["nombre"])] + [(x, f"{p['nombre']}, otra vista") for x in p["extras"]]
    if filas:
        ficha_img(p, filas); fotos.append((f"img/p-{p['id']}-ficha.webp", f"Ficha técnica de {p['nombre']}"))
    th = "".join(f'<button type="button" aria-selected="{"true" if i == 0 else "false"}" data-src="{s}" data-alt="{esc(a)}" aria-label="{esc(a)}"><img src="{s}" alt="" loading="lazy"></button>' for i, (s, a) in enumerate(fotos))
    return (f'<div class="g2" data-g2><div class="g2-main"><img decoding="async" src="{fotos[0][0]}" alt="{esc(fotos[0][1])}" width="1200" height="1200"><span class="g2-lupa">🔍 Pasa el mouse para ampliar</span></div>'
            f'<div class="g2-th">{th}</div><p class="g2-tip">Toca la foto para acercarla. Cambia de imagen con las miniaturas.</p></div>')


def wa_cod(p):
    q = __import__("urllib.parse").parse.quote
    return f"https://wa.me/{WA}?text=" + q(f"Hola, quiero pedir contra entrega:\n• {p['nombre']}" + (f" (ref. {p['ref']})" if p["ref"] != p["sku"] else "") + f"\nPrecio: {cop(p['precio'])} (envío gratis)\n\nMi nombre:\nCiudad:\nBarrio y dirección:\nCelular:")


def wa_pieza(p):
    return f"https://wa.me/{WA}?text=" + __import__("urllib.parse").parse.quote(f"Hola, quiero información de: {p['nombre']}" + (f" (ref. {p['ref']})" if p["ref"] != p["sku"] else "") + ". Mi modelo de equipo es: ")


# ---------------------------------------------------------------- buscador del encabezado
ARTS_BASE = [("Guías de repuestos", "guias-de-repuestos.html"), ("Cómo elegir el repuesto de tu lavadora", "como-elegir-repuesto-para-lavadora.html"), ("Cómo encontrar el modelo de tu electrodoméstico", "como-encontrar-el-modelo-de-tu-electrodomestico.html"),
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
      "caja.innerHTML=h||'<p>No encontramos «'+q.replace(/</g,'')+'». Prueba con manguera o protector.</p>';caja.hidden=false}"
      "document.querySelectorAll('[data-aq-q]').forEach(function(i){var c=i.parentNode.querySelector('.aq-res');i.addEventListener('input',function(){pintar(c,buscar(i.value),i.value)});i.addEventListener('focus',function(){if(i.value)pintar(c,buscar(i.value),i.value)});"
      "i.addEventListener('keydown',function(e){if(e.key==='Enter'){var a=c.querySelector('a');if(a)location.href=a.getAttribute('href')}if(e.key==='Escape')c.hidden=true})});"
      "document.addEventListener('click',function(e){document.querySelectorAll('.aq-res').forEach(function(c){if(!c.parentNode.contains(e.target))c.hidden=true});document.querySelectorAll('.aq-nav details[open]').forEach(function(d){if(!d.contains(e.target))d.removeAttribute('open')})});})();")
(OUT / "buscar.js").write_text(js, encoding="utf-8")

# partes.php y páginas PHP de compra
_src_lg = open(AQUI / "ads_lg_paginas.py", encoding="utf-8").read()
_partes = _src_lg.split('(OUT / "partes.php").write_text(r"""')[1].split('""".replace("__AQH__"')[0].replace("/img/icono-lg.png", "/img/icono-bm.png")
(OUT / "partes.php").write_text(_partes.replace("__AQH__", encabezado()).replace("__AQF__", pie()).replace('<script src="/buscar.js', '<link rel="stylesheet" href="/nav.css"><script src="/nav.js" defer></script><script src="/buscar.js', 1), encoding="utf-8")
_g = (OUT / "gracias.php").read_text(encoding="utf-8")
_wa_btn = ('    try { const d0 = JSON.parse(sessionStorage.getItem("fy_cod_" + cod) || "null"); const c0 = (d0 && d0.cli) || {}; const it = ((d0 && d0.items) || []).map(x => "• " + x.item_name + " x" + (x.quantity || 1) + " — " + cop(x.price) + " c/u").join("\\n"); '
           'const msg = "Hola, quiero pedir *contra entrega* (pedido " + cod + "):\\n" + it + "\\nTotal a pagar al recibir: " + cop(d0 ? d0.total : 0) + " (envío gratis)\\nForma de pago: contra entrega (efectivo al recibir)\\n\\nNombre: " + (c0.nombre || "") + "\\nCelular: " + (c0.tel || "") + "\\nCiudad: " + (c0.ciudad || "") + "\\nBarrio: " + (c0.barrio || "") + "\\nDirección: " + (c0.dir || "") + (c0.indicaciones ? "\\nIndicaciones: " + c0.indicaciones : ""); '
           'out.insertAdjacentHTML("beforeend", `<p style="margin-top:14px"><a class="btn" target="_blank" rel="noopener" href="https://wa.me/' + WA + '?text=${encodeURIComponent(msg)}">Enviar mi pedido por WhatsApp</a></p>`); } catch {}\n')
_g = _g.replace('    try { localStorage.removeItem("fy_carrito"); } catch {}\n', '    try { localStorage.removeItem("fy_carrito"); } catch {}\n' + _wa_btn, 1)
assert "Enviar mi pedido por WhatsApp" in _g
(OUT / "gracias.php").write_text(_g, encoding="utf-8")
_c = (OUT / "carrito.php").read_text(encoding="utf-8")
_c = re.sub(r'Busca el filtro de tu nevecón por la referencia o por[^<]*', 'Elige los repuestos que necesitas para tu lavadora o tu nevera.', _c)
_c = re.sub(r'(<label)([^>]*>(?:(?!</label>).)*Recuérdame por correo cuando toque cambiar el filtro)', r'\1 hidden\2', _c, flags=re.S)
_c = _c.replace('JSON.stringify({ total: j.total, items: L.map', 'JSON.stringify({ cli: cli, total: j.total, items: L.map')
_c = _c.replace('let entrega = null, pago = "linea";', 'let entrega = null, pago = new URLSearchParams(location.search).get("pago") === "cod" ? "cod" : "linea";')
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
_dest4 = [x for x in (next((p for p in PS if p["sku"] == "PV-MIST-15A"), None), next((p for p in PS if p["sku"] == "PV-BM-NEV"), None), next((p for p in PS if p["categoria"] == "Presostatos"), None), next((p for p in PS if p["categoria"].startswith("Mangueras")), None)) if x]
_dest4 = (_dest4 + [x for x in PS if x not in _dest4])[:4]
_btn = lambda x: (f'<div class="hx-bt"><button type="button" class="tf-add" data-add="{x["id"]}">🛒 Agregar</button><button type="button" class="tf-cod" data-cod="{x["id"]}">🚚 Contra entrega</button></div>' if x["precio"] else "")
_tiles = "".join(f'<div class="hx-t"><a class="hx-a" href="{x["url"]}"><div class="hx-i"><img src="{x["img"][:-5]}-480.webp" alt="{esc(x["nombre"])}" width="480" height="480" {"loading=eager" if i < 2 else "loading=lazy"}></div><b>{esc(x["nombre"])}</b><span>{cop(x["precio"]) if x["precio"] else "Consultar precio"}</span></a>{_btn(x)}</div>' for i, x in enumerate(_dest4))
hero = ('<section class="hx" id="inicio"><div class="wrap hx-g"><div class="hx-l"><span class="hx-k">Repuestos para lavadoras y neveras</span><h1>Repuestos para lavadoras y neveras, con todos los medios de pago</h1>'
        '<p>Filtros de agua, mangueras, presostatos y protectores de voltaje con foto, precio y especificaciones. Paga como prefieras: tarjeta débito o crédito, PSE, Nequi, Bancolombia o efectivo contra entrega. Envío gratis a toda Colombia.</p>'
        f'<div class="hx-b"><a class="hx-p" href="#repuestos">Ver repuestos</a><a class="hx-w" href="https://wa.me/{WA}?text=Hola%2C%20necesito%20un%20repuesto" rel="noopener">Escribir por WhatsApp</a></div>'
        '<ul class="hx-u"><li>Envío gratis a toda Colombia</li><li>Tarjeta, PSE, Nequi y Bancolombia</li><li>Contra entrega en efectivo</li><li>5 días de retracto</li></ul></div>'
        f'<div class="hx-r">{_tiles}</div></div></section>')
tiles_eq = "".join(f'<a class="aq-tile" href="{R_EQ(eq)}"><b>Repuestos para {esc(eq.lower())}</b><p>{conteo(eq)} repuesto{"s" if conteo(eq) > 1 else ""}: {esc(", ".join(c.lower() for c in EQUIPOS[eq]))}.</p></a>' for eq in EQ_LISTA)
sec_eq = seccion("Compra por equipo", f'<div class="aq-tiles">{tiles_eq}</div>', sub="Elige tu electrodoméstico y mira solo lo que le sirve.")
_grupos = [("Filtros de agua para nevera", lambda x: x["categoria"] == "Filtros de agua"), ("Mangueras para lavadora", lambda x: x["categoria"].startswith("Mangueras")), ("Presostatos para lavadora", lambda x: x["categoria"] == "Presostatos"), ("Motores de ventilador para nevera", lambda x: x["categoria"] == "Motores de ventilador"), ("Mangueras de agua para nevera", lambda x: x["categoria"] == "Mangueras de agua para nevera"), ("Kits de arranque para nevera", lambda x: x["categoria"] == "Kits de arranque de compresor"), ("Varillas de suspensión para lavadora", lambda x: x["categoria"] == "Varillas de suspensión"), ("Sensores de temperatura para nevera", lambda x: x["categoria"] == "Sensores de temperatura"), ("Filtros de motas para lavadora", lambda x: x["categoria"] == "Filtros de motas"), ("Protectores de voltaje", lambda x: x["categoria"] == "Protectores de voltaje")]
_ids_cat = {}
for _x in PS:
    _ids_cat.setdefault(_x["categoria"], (_x["equipo"], _x["categoria"]))
def _enlace_grupo(nombre, lista):
    _eq, _ct = (lista[0]["equipo"], lista[0]["categoria"])
    _href = R_CAT(_eq, _ct) if len({x["categoria"] for x in lista}) == 1 else R_EQ(_eq)
    return f'<p style="margin-top:14px"><a class="btn" href="{_href}">Ver todos ({len(lista)}) →</a></p>'
estante = ""
for _i, (_n, _f) in enumerate(_grupos):
    _l = [x for x in PS if _f(x)]
    if _l:
        estante += seccion(_n, '<div class="tf-grid">' + "".join(tarjeta(x) for x in _l[:6]) + "</div>" + (_enlace_grupo(_n, _l) if len(_l) > 6 else ""), alt=bool(_i % 2)).replace('<section class="aq-sec">', '<section class="aq-sec estante-top" id="repuestos">' if _i == 0 else '<section class="aq-sec">', 1)
cats = [(eq, c, len(v)) for eq, cs in EQUIPOS.items() for c, v in cs.items()]
_pz = {}
for _x in PS:
    _pz.setdefault((_x["equipos_l"][0], _x["categoria"]), []).append(_x)
sec_pz = seccion("Compra por tipo de pieza", '<p style="margin:0 0 16px"><a class="btn btn-solid" href="repuestos.html">🔎 Filtrar por nevera, lavadora o tipo de repuesto</a></p><div class="pz">' + "".join(
    f'<a class="pz-t" href="{R_CAT(_e, _c)}"><span class="pz-i"><img src="{_v[0]["img"][:-5]}-480.webp" alt="{esc(_c)} para {esc(_e.lower())}" width="480" height="480" loading="lazy"></span><b>{esc(_c)}</b><small>para {esc(_e.lower())} · {len(_v)} producto{"s" if len(_v) > 1 else ""}</small>'
    + (f'<em>desde {cop(min(x["precio"] for x in _v if x["precio"]))}</em>' if any(x["precio"] for x in _v) else "") + '</a>' for (_e, _c), _v in _pz.items()) + "</div>", sub="Elige la pieza que necesitas y entra directo a esa sección.")
sec_cat = seccion("Busca por tipo de pieza", '<div class="city-tags">' + "".join(f'<a href="{R_CAT(eq, c)}">{esc(c)} para {esc(eq.lower())} ({n})</a>' for eq, c, n in cats) + "</div>", alt=True)
sec_mt = seccion("Busca por marca y tipo de repuesto", '<div class="city-tags">' + "".join(f'<a href="{mt_url(e3, c3, m3)}">{esc(c3)} {esc(m3)}</a>' for (e3, c3, m3) in MT) + "</div>", alt=True)
sec_marca = seccion("Repuestos por marca de electrodoméstico", '<div class="city-tags">' + "".join(f'<a href="marca-{slug(m)}.html">Repuestos {esc(m)}</a>' for m in MARCAS_EQ) + "</div><p class=\"note\" style=\"margin-top:14px\">¿No ves tu marca? Escríbenos con el modelo y te decimos si tenemos la pieza.</p>")
qa_home = qa("¿Dónde comprar repuestos para lavadoras y neveras en Colombia?",
             f"Aquí encuentras {CATS_TXT} para lavadoras y neveras, con foto, precio y compatibilidad. Pagas en línea con Wompi o contra entrega y enviamos a toda Colombia. "
             "Si no estás seguro de cuál es tu pieza, escríbenos por WhatsApp con el modelo de tu equipo.", [("Equipos", "Lavadoras y neveras"), ("Pago", "Wompi o contra entrega"), ("Envío", "Toda Colombia"), ("Retracto", "5 días hábiles")])
tiles = [("caja", "Envío a toda Colombia", "Por transportadora, con confirmación por correo y WhatsApp."), ("candado", "Pago seguro", "Wompi (Bancolombia): tarjeta, PSE, Nequi o botón Bancolombia."),
         ("efectivo", "Contra entrega", "Paga en efectivo cuando recibas tu pedido, sin recargo."), ("retorno", "5 días de retracto", "Si no es lo que necesitas, lo cambiamos (sin usar y en su empaque).")]
confianza = seccion("Compra tranquilo", '<div class="aq-tiles">' + "".join(f'<div class="aq-tile">{ICONOS[i]}<b>{esc(t)}</b><p>{esc(d)}</p></div>' for i, t, d in tiles) + "</div>", sub="Una tienda en línea como las grandes: carrito, pago seguro y confirmación por correo.")
pasos = '<ol class="vl"><li><b>Elige tu equipo</b> (lavadora o nevera) y la pieza que necesitas.</li><li><b>Confirma la compatibilidad</b> con el modelo de tu equipo; si dudas, escríbenos.</li><li><b>Agrégala al carrito</b> y paga en línea o contra entrega.</li><li><b>Recíbela</b> en tu casa y cámbiala o instálala.</li></ol>'
FAQ_HOME = [("¿Cómo sé qué repuesto necesita mi lavadora?", "Mira el modelo en la etiqueta de tu equipo y la descripción de la pieza. Si dudas, escríbenos con el modelo y una foto de la pieza."),
            ("¿Cómo pago?", FPAGO), ("¿Hacen envíos a toda Colombia?", "Sí, por transportadora. El tiempo de entrega se confirma al hacer el pedido."), ("¿Los productos son nuevos?", "Sí, nuevos y en su empaque."),
            ("¿Hay retracto?", "Sí, 5 días hábiles desde la entrega, con el producto sin usar ni instalar y en su empaque.")]
ld_home = [{"@type": "ItemList", "name": "Repuestos de línea blanca", "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": ld_producto(p)} for i, p in enumerate(PS)]}]
pagina("index.html", "Repuestos de Línea Blanca | Lavadoras y Neveras | Envío a Colombia", f"Repuestos para lavadoras y neveras: {CATS_TXT} con foto, precio y compatibilidad. Paga con Wompi o contra entrega. Envío a toda Colombia.",
       "repuestos linea blanca, repuestos lavadoras, repuestos neveras, mangueras lavadora, protector de voltaje, repuestos contra entrega, comprar repuestos lavadora",
       [("Inicio", None)], hero + sec_pz + estante + confianza + seccion("Repuestos con envío a tu ciudad", '<div class="city-tags">' + "".join(f'<a href="repuestos-en-{slug(c_)}.html">Repuestos en {esc(c_)}</a>' for c_ in cat_php["ciudades"][:N_CIU]) + '</div><p style="margin-top:12px"><a href="envios-a-toda-colombia.html">Ver todas las ciudades con envío →</a></p>', alt=True) + sec_mt + sec_eq.replace('<div class="aq-tiles">','<div class="aq-tiles eqt">') + faq_html(FAQ_HOME), FAQ_HOME, ld_home, prio="1.0", og=dest[0]["img"])

CONT = {
    "Filtros de agua": dict(
        que="El filtro de agua de la nevera limpia el agua y el hielo que salen del dispensador. Con el uso se satura, y por eso se cambia periódicamente: normalmente cada 6 meses de uso normal.",
        senales=["Pasaron unos 6 meses desde el último cambio.", "El agua o el hielo tienen mal sabor, mal olor o se ven turbios.", "El dispensador entrega menos agua o sale lento.", "El aviso o la luz de cambio de filtro de tu nevera está encendido."],
        elegir=["Mira la referencia impresa en tu filtro viejo (por ejemplo, DA29-00020B).", "O busca el modelo de tu nevera en la etiqueta dentro del refrigerador y compáralo con los modelos de la ficha.", "Interno (va dentro de la nevera) o externo (va en la manguera del agua).", "Si dudas, escríbenos el modelo de tu nevera o la foto del filtro viejo antes de comprar."],
        faq=[("¿Cada cuánto se cambia el filtro de agua de la nevera?", "Cada 6 meses de uso normal, o antes si el agua cambia de sabor o el dispensador entrega menos agua."), ("¿Cómo sé cuál filtro necesita mi nevera?", "Por la referencia impresa en el filtro viejo o por el modelo de tu nevera. Si dudas, envíanos la foto del filtro o el modelo por WhatsApp.")]),
    "Mangueras de entrada": dict(
        que="La manguera de entrada lleva el agua desde la llave de paso hasta tu lavadora. Si está vieja, agrietada o mal sellada, la lavadora puede llenar despacio, gotear o dejar agua en el piso, y por eso conviene cambiarla a tiempo.",
        senales=["Gotea o suelta agua en las uniones.", "La cubierta está abultada, agrietada o rota.", "La lavadora llena muy despacio o no entra agua.", "La tuerca o la rosca está dañada y no sella bien.", "Tiene muchos años de uso: conviene revisarla de vez en cuando."],
        elegir=["Agua fría o caliente: la tuerca azul indica agua fría y la naranja, agua caliente.", "Que el largo alcance de la llave a la lavadora sin quedar tensa.", "Que la tuerca y la rosca coincidan con tu llave y con la entrada de tu lavadora.", "Si tienes dudas, envíanos una foto de la manguera vieja por WhatsApp."],
        faq=[("¿Cada cuánto se cambia la manguera de entrada de la lavadora?", "No hay un plazo fijo: se cambia cuando se ve abultada, agrietada, gotea o la lavadora llena despacio. Revisarla de vez en cuando evita fugas e inundaciones.")]),
    "Mangueras de desagüe": dict(
        que="La manguera de desagüe saca el agua usada de la lavadora hacia el desagüe. Si está aplastada, rota o mal sujeta, la lavadora puede desaguar lento o dejar agua en el piso.",
        senales=["Hay agua en el piso mientras la lavadora desagua.", "La manguera está doblada, aplastada, rota o con huecos.", "La lavadora tarda mucho en desaguar. Revisa que la manguera no esté tapada; si sigue igual, puede ser otra pieza.", "El codo o el extremo está roto y no se sujeta al desagüe."],
        elegir=["Largo suficiente para llegar al desagüe sin doblarse.", "Que el extremo (codo o recto) se ajuste a tu desagüe.", "Las mangueras corrugadas se doblan sin aplastarse; la funda protectora cuida la zona del doblez.", "Si dudas, envíanos una foto de tu manguera vieja."],
        faq=[("¿Qué manguera de desagüe necesito para mi lavadora?", "Mide el largo que necesitas de la lavadora al desagüe y fíjate en el extremo: con codo o recto. Si dudas, envíanos una foto de tu manguera.")]),
    "Mangueras tina-bomba": dict(
        que="La manguera tina-bomba va por dentro de la lavadora y une la tina con la bomba de desagüe. Si se rompe o se afloja, la lavadora puede soltar agua por debajo.",
        senales=["Sale agua por debajo de la lavadora.", "La manguera interna está agrietada, aplastada o suelta.", "La lavadora no desagua bien después de revisar la manguera externa."],
        elegir=["Que tenga la forma y el largo de la que vas a cambiar.", "Es una pieza interna: te recomendamos que la cambie un técnico.", "Envíanos una foto de la pieza vieja para confirmar."],
        faq=[("¿La manguera tina-bomba se instala sola?", "Va dentro de la lavadora y exige abrirla. Recomendamos que la cambie un técnico y que desconecte la lavadora de la corriente antes.")]),
    "Filtros de motas": dict(
        que="El filtro de motas de la lavadora atrapa pelusas e hilos que se sueltan de la ropa durante el lavado, para que no vuelvan a quedar en las prendas ni tapen el desagüe. Con el tiempo se llena, se rompe o se deforma y hay que cambiarlo.",
        senales=["Salen motas o pelusas pegadas en la ropa después del lavado.", "El filtro está roto, deformado o la malla tiene huecos.", "Se perdió el filtro o ya no encaja bien en su lugar.", "El agua desagua más lento porque la pelusa se acumula."],
        elegir=["La marca de tu lavadora (este es para LG).", "El tamaño y la forma: compáralos con tu filtro viejo (con bolsa de malla, redondo o de marco).", "Compara con el filtro viejo o escríbenos con el modelo de tu lavadora y una foto para confirmar que encaja."],
        faq=[("¿Cada cuánto se limpia el filtro de motas?", "Conviene limpiarlo con frecuencia, según el uso, y cambiarlo cuando esté roto, deformado o ya no retenga las motas."), ("¿Cómo sé si el filtro grande sirve para mi lavadora LG?", "Compáralo con el que tienes o envíanos por WhatsApp el modelo de tu lavadora y una foto del filtro viejo.")]),
    "Sensores de temperatura": dict(
        que="El sensor de temperatura de la nevera (termistor) le informa a la tarjeta qué tan frío está el compartimiento, para que encienda y apague el compresor y los ventiladores. Si falla, la nevera puede enfriar de más, no enfriar o mostrar un código de error.",
        senales=["La nevera enfría de más o no enfría lo suficiente.", "El display muestra un código de error de sensor.", "El compresor trabaja sin parar o se apaga muy seguido.", "Estos síntomas también pueden venir de otras piezas: si dudas, escríbenos o consulta a un técnico."],
        elegir=["La marca de tu nevera (este es para Samsung).", "La referencia impresa en el sensor viejo (por ejemplo, DA32-00006B).", "El conector y el color del cable: compáralos con tu sensor antes de pedir.", "Si no estás seguro, envíanos el modelo de tu nevera y una foto del sensor viejo."],
        faq=[("¿Cómo sé si el sensor de temperatura de mi nevera está dañado?", "Los síntomas típicos son que enfríe de más, no enfríe o muestre un error de sensor, pero también pueden venir de otras piezas. Un técnico puede medirlo con un multímetro."), ("¿Cómo sé cuál sensor necesita mi nevera Samsung?", "Mira la referencia impresa en el sensor viejo o el modelo de tu nevera, y compáralos con la ficha del producto. Si dudas, escríbenos por WhatsApp.")]),
    "Varillas de suspensión": dict(
        que="Las varillas de suspensión sostienen la tina de la lavadora y absorben la vibración del lavado y del centrifugado. Con el uso se desgastan o pierden fuerza, y la lavadora empieza a vibrar, golpear o moverse de lugar.",
        senales=["La lavadora vibra mucho o golpea durante el centrifugado.", "Se mueve o \"camina\" mientras exprime.", "Hace ruidos fuertes al girar la tina.", "La tina se ve inclinada o roza el gabinete.", "Estos síntomas también pueden venir de la ropa mal repartida o de las patas desniveladas: revísalo antes de cambiar piezas."],
        elegir=["La marca de tu lavadora (esta referencia es para Samsung).", "El largo: esta varilla mide 63,5 cm. Mide la tuya antes de pedir.", "Se recomienda cambiarlas en juego para que la tina quede pareja.", "Si dudas, envíanos el modelo de tu lavadora y una foto de la varilla vieja."],
        faq=[("¿Cómo sé si las varillas de mi lavadora Samsung están dañadas?", "Los síntomas típicos son vibración fuerte, golpes y movimiento de la lavadora al exprimir. También pueden venir de otras causas, así que conviene revisar la carga y el nivelado."), ("¿Se cambian todas las varillas juntas?", "Se recomienda cambiarlas en juego para que la tina quede equilibrada.")]),
    "Kits de arranque de compresor": dict(
        que="El relé PTC y el protector térmico arrancan y protegen el compresor de la nevera. Si fallan, el compresor puede no arrancar, hacer «clic» y apagarse, o la nevera deja de enfriar.",
        senales=["La nevera no enfría y se oye un clic repetido.", "El compresor no arranca o se apaga a los pocos segundos.", "El compresor está caliente y el térmico se dispara seguido.", "Otras fallas del compresor dan síntomas parecidos: un técnico debe revisarlo."],
        elegir=["La potencia de tu compresor: este kit es para compresores de 1/12 hp a 1/2 hp.", "La forma y los terminales: compáralos con el kit que tienes.", "Es una pieza eléctrica: debe instalarla un técnico con la nevera desconectada.", "Envíanos la etiqueta del compresor y una foto del kit viejo para confirmar."],
        faq=[("¿Cómo sé si el relé y el térmico de mi nevera están dañados?", "Los síntomas típicos son que no arranque, haga clic o se apague rápido, pero también pueden venir del compresor. Un técnico puede medirlos."), ("¿Este kit sirve para mi nevera?", "Sirve para compresores de 1/12 hp a 1/2 hp. Confirma la potencia en la etiqueta del compresor o escríbenos por WhatsApp.")]),
    "Mangueras de agua para nevera": dict(
        que="La manguera de 1/4 de pulgada lleva el agua hasta el filtro, el dispensador y la fábrica de hielo del nevecón. Si se aplasta, se rompe o se llena de sarro, el agua sale poco, con mal sabor o gotea.",
        senales=["Hay agua o humedad debajo o detrás de la nevera.", "El dispensador entrega poca agua o nada.", "La manguera está doblada, aplastada, agrietada o amarillenta.", "El agua o el hielo tienen mal sabor y ya cambiaste el filtro."],
        elegir=["El diámetro: esta manguera es de 1/4 de pulgada.", "El largo: se vende por tramos de 5 metros y cada unidad que agregues son 5 metros más.", "Los conectores: confirma el tipo de conector de tu nevecón; escríbenos si dudas.", "Corta la manguera recta y sin rebabas para que sellen bien los conectores."],
        faq=[("¿Cuántos metros de manguera necesito para mi nevecón?", "Mide desde la toma de agua hasta la nevera y suma un poco de holgura. Se vende por tramos de 5 metros."), ("¿La manguera de 1/4 sirve para cualquier nevecón?", "El diámetro de 1/4 es el más usado en neveras con dispensador, pero confirma el de tu equipo o escríbenos con el modelo.")]),
    "Motores de ventilador": dict(
        que="El motor del ventilador mueve el aire dentro de la nevera para repartir el frío por el refrigerador y el congelador. Si falla, la nevera puede enfriar mal, hacer ruido o formar escarcha.",
        senales=["La nevera enfría poco o de forma despareja.", "Se oye ruido, vibración o el ventilador no gira.", "Se forma escarcha o el congelador enfría y el refrigerador no.", "Estos síntomas también pueden venir de otras piezas: un técnico puede confirmar que sea el motor."],
        elegir=["La marca y el modelo de tu nevera (este es para LG).", "La referencia impresa en el motor viejo o en su etiqueta.", "El voltaje y el conector: compáralos con tu motor antes de pedir (la etiqueta de este indica DC 13 V).", "Desconecta la nevera antes de cambiarlo; si no tienes experiencia, usa un técnico."],
        faq=[("¿Cómo sé si el motor del ventilador de mi nevera está dañado?", "Si el ventilador no gira, hace ruido o la nevera enfría mal puede ser el motor, pero también pueden ser el sensor, la tarjeta u otra pieza. Un técnico puede medirlo."), ("¿Este motor sirve para mi nevera LG?", "Compara la referencia 4681JB1027A con la de tu motor viejo o escríbenos con el modelo de tu nevera.")]),
    "Presostatos": dict(
        que="El presostato es el sensor de nivel de agua de la lavadora: mide cuánta agua hay en la tina y le avisa a la tarjeta cuándo parar de llenar o empezar a lavar. Se vende por marca y tipo de lavadora.",
        senales=["La lavadora llena de más o no llena el agua que debe.", "No detecta el nivel de agua o muestra un error de nivel.", "El ciclo se detiene o repite el llenado sin avanzar.", "Estos síntomas pueden tener otras causas; un técnico confirma el diagnóstico."],
        elegir=["Marca de tu lavadora (Samsung, LG, etc.).", "Tipo: carga superior o carga frontal, e inverter o no.", "Referencia o modelo de tu lavadora: está en la etiqueta del equipo.", "Si no estás seguro, envíanos el modelo y una foto de tu presostato por WhatsApp antes de comprar."],
        faq=[("¿Cómo sé si el presostato de mi lavadora está dañado?", "Los síntomas típicos son que llene de más, no llene o muestre un error de nivel de agua, pero también pueden venir de otras piezas. Un técnico lo confirma con una prueba.")]),
    "Protectores de voltaje": dict(
        que="El protector de voltaje vigila el voltaje que llega a tu equipo. Si el voltaje sube o baja fuera del rango normal, desconecta el equipo, y lo vuelve a conectar cuando se normaliza, después del tiempo de espera.",
        senales=["Hay cortes de luz o variaciones de voltaje en tu zona.", "Quieres cuidar un equipo con tarjeta electrónica (nevera, lavadora, televisor).", "Tu equipo se reinicia o se apaga solo cuando vuelve la luz."],
        elegir=["Voltaje: estos protectores son de 110 VAC.", "Corriente: el consumo del equipo no debe superar los amperios del protector.", "Número de tomas: cuántos equipos vas a conectar.", "Tiempo de espera: el que indica la ficha del producto."],
        faq=[("¿Un protector de voltaje evita todos los daños?", "Reduce el riesgo de daños por voltaje alto o bajo, pero ningún protector cubre todos los casos.")]),
}


# ---------------------------------------------------------------- páginas por equipo, tipo de pieza y marca
def cat_pie(c, eq, v):
    k = CONT.get(c)
    if not k:
        return ""
    otros = "".join(f'<a href="{R_CAT(e2, c2)}">{esc(c2)} para {esc(e2.lower())}</a>' for e2, cs2 in EQUIPOS.items() for c2 in cs2 if (e2, c2) != (eq, c))
    otros += "".join(f'<a href="{mt_url(e3, c3, m3)}">{esc(c3)} para {esc(e3.lower())} {esc(m3)}</a>' for (e3, c3, m3) in MT if (e3, c3) == (eq, c))
    return (seccion(f"Qué debes saber de {c.lower()} para {eq.lower()}", f"<p style=\"max-width:75ch\">{esc(k['que'])}</p>", alt=True)
            + seccion("Cuándo cambiarla", "<ul class=\"spec-list\">" + "".join(f"<li>{esc(x)}</li>" for x in k["senales"]) + "</ul>")
            + seccion("Cómo elegir la correcta", "<ul class=\"spec-list\">" + "".join(f"<li>{esc(x)}</li>" for x in k["elegir"]) + "</ul>", alt=True)
            + seccion("También te puede interesar", f'<div class="city-tags">{otros}<a href="{R_EQ(eq)}">Todos los repuestos para {esc(eq.lower())}</a><a href="envios-a-toda-colombia.html">Envíos a toda Colombia</a></div>'))


def filtros_html(eq):
    cs = EQUIPOS[eq]
    marcas = sorted({p["marca_eq"] for c in cs.values() for p in c if p["marca_eq"] != "Todas las marcas"})
    return ('<div class="city-tags ct-row"><b>Tipo de pieza:</b> ' + "".join(f'<a href="{R_CAT(eq, c)}">{esc(c)} ({len(v)})</a>' for c, v in cs.items()) + "</div>"
            + ('<div class="city-tags ct-row" style="margin-top:10px"><b>Marca:</b> ' + "".join(f'<a href="{R_EQM(eq, m)}">{esc(m)}</a>' for m in marcas) + "</div>" if marcas else ""))


def pag_lista(nombre, titulo, desc, kw, h1, lista, extra="", miga=None, faq=(), pie=""):
    cuerpo = (hero_simple("Repuestos de línea blanca", h1, desc) + seccion(h1, extra + '<div class="tf-grid">' + "".join(tarjeta(p) for p in lista) + "</div>") + pie
              + (faq_html(list(faq)) if faq else ""))
    ld = [{"@type": "ItemList", "name": h1, "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{DOMINIO}/{p['url']}", "name": p["nombre"]} for i, p in enumerate(lista)]}]
    pagina(nombre, titulo, desc, kw, miga or [("Inicio", "index.html"), (h1, None)], cuerpo, faq, ld, prio="0.8", og=lista[0]["img"])


for eq, cs in EQUIPOS.items():
    todos = [p for v in cs.values() for p in v]
    pag_lista(R_EQ(eq), f"Repuestos para {eq} | Mangueras, Presostatos y más", f"Repuestos para {eq.lower()}: " + ", ".join(c.lower() for c in cs) + f". {len(todos)} producto(s) con foto, compatibilidad y pago contra entrega.",
              f"repuestos para {eq.lower()}, repuestos {eq.lower()} colombia, comprar repuestos {eq.lower()}", f"Repuestos para {eq.lower()}", todos, filtros_html(eq))
    for c, v in cs.items():
        pag_lista(R_CAT(eq, c), f"{c} para {eq} | Precio y compatibilidad", f"{c} para {eq.lower()}: " + ", ".join(p["nombre"] for p in v[:3]) + ". Con foto, precio y pago contra entrega.",
                  f"{c.lower()} para {eq.lower()}, comprar {c.lower()}, {c.lower()} {eq.lower()} precio", f"{c} para {eq.lower()}", v, "", [("Inicio", "index.html"), (f"Repuestos para {eq.lower()}", R_EQ(eq)), (c, None)], faq=CONT.get(c, {}).get("faq", []), pie=cat_pie(c, eq, v))
    marcas = sorted({p["marca_eq"] for p in todos if p["marca_eq"] != "Todas las marcas"})
    for m in marcas:
        v = [p for p in todos if p["marca_eq"] == m]
        pag_lista(R_EQM(eq, m), f"Repuestos para {eq} {m} | Compatibles", f"Repuestos para {eq.lower()} {m}: " + ", ".join(p["nombre"] for p in v[:3]) + ".", f"repuestos {eq.lower()} {m.lower()}, {m.lower()} {eq.lower()} repuestos", f"Repuestos para {eq.lower()} {m}", v, "",
                  [("Inicio", "index.html"), (f"Repuestos para {eq.lower()}", R_EQ(eq)), (m, None)], pie=seccion(f"{m}: por tipo de repuesto", '<div class="city-tags">' + "".join(f'<a href="{mt_url(e3, c3, m3)}">{esc(c3)} para {esc(e3.lower())} {esc(m3)}</a>' for (e3, c3, m3) in MT if m3 == m and e3 == eq) + "</div>", alt=True))
for m in MARCAS_EQ:
    v = [p for p in PS if p["marca_eq"] == m]
    pag_lista(f"marca-{slug(m)}.html", f"Repuestos {m} | Lavadoras y Neveras", f"Repuestos compatibles con electrodomésticos {m}: " + ", ".join(p["nombre"] for p in v[:3]) + ". Foto, precio y compatibilidad.", f"repuestos {m.lower()}, repuestos para {m.lower()}", f"Repuestos {m}", v,
              "", [("Inicio", "index.html"), (f"Repuestos {m}", None)], pie=seccion(f"Repuestos {m} por tipo", '<div class="city-tags">' + "".join(f'<a href="{mt_url(e3, c3, m3)}">{esc(c3)} para {esc(e3.lower())} {esc(m3)}</a>' for (e3, c3, m3) in MT if m3 == m) + "</div>", alt=True))


# ---------------------------------------------------------------- SEO de cada producto para toda Colombia
CIUDADES = sorted(cat_php["ciudades"], key=lambda c: slug(c))
TOP_CIU = cat_php["ciudades"][:20]
def cont_seo(p):
    c = CONT.get(p["categoria"])
    if not c:
        return "", []
    ciud = "".join(f"<span>{esc(x)}</span>" for x in TOP_CIU)
    html_ = (seccion(f"Qué es: {esc(p['nombre'])}", f"<p style=\"max-width:75ch\">{esc(c['que'])}</p><p style=\"max-width:75ch\">{esc(p['resumen'])}</p>")
             + seccion("Cuándo cambiarla o cuándo la necesitas" if p["categoria"] != "Protectores de voltaje" else "Cuándo te sirve", "<ul class=\"spec-list\">" + "".join(f"<li>{esc(x)}</li>" for x in c["senales"]) + "</ul>", alt=True)
             + seccion("Cómo elegir la correcta", "<ul class=\"spec-list\">" + "".join(f"<li>{esc(x)}</li>" for x in c["elegir"]) + "</ul>")
             + seccion("Enviamos a toda Colombia", f'<p style="max-width:75ch">Este repuesto llega a {len(CIUDADES)} ciudades y municipios de Colombia con envío gratis por transportadora. Paga en línea con Wompi o contra entrega.</p><div class="city-tags">{ciud}<a href="envios-a-toda-colombia.html"><b>Ver todas las ciudades →</b></a></div>', alt=True))
    faq = c["faq"] + [(f"¿Hacen envíos de {p['nombre'].lower()} a mi ciudad?", f"Sí, enviamos a toda Colombia, incluidas {', '.join(TOP_CIU[:6])} y más de {len(CIUDADES) - 6} ciudades y municipios. El envío es gratis y el tiempo depende de la ciudad."),
                      ("¿Puedo pagar contra entrega en cualquier ciudad?", "Sí. Pides por WhatsApp o por el carrito y pagas al recibir, sin recargo.")]
    return html_, faq



# ---------------------------------------------------------------- formulario de pago contra entrega (llena los datos y arma el WhatsApp)
_prods = {x["id"]: {"n": x["nombre"], "p": x["precio"], "u": x["url"], "r": (x["ref"] if x["ref"] != x["sku"] else "")} for x in PS if x["precio"]}
_ciu = TOP_CIU + [c for c in CIUDADES if c not in TOP_CIU]
PEDIDO_JS = """(function(){var P=%s,C=%s,WA='%s',K='rp_cliente',B='rp_borrador',m,cur,ok=false,F=['nom','tel','ciu','bar','dir','ind'];
function bor(){try{return JSON.parse(localStorage.getItem(B)||'null')}catch(e){return null}}
function guardar(){if(!m||m.hidden||ok)return;var d={id:cur,c:document.getElementById('pc-c').value};F.forEach(function(k){d[k]=document.getElementById('pc-'+k).value});try{localStorage.setItem(B,JSON.stringify(d))}catch(e){}}
function sucio(){return F.some(function(k){var e=document.getElementById('pc-'+k);return e&&e.value.trim()})}
function cop(n){return '$'+String(n).replace(/\\B(?=(\\d{3})+(?!\\d))/g,'.')}
function g(){try{return JSON.parse(localStorage.getItem(K)||'{}')}catch(e){return{}}}
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function build(){m=document.createElement('div');m.className='pc-m';m.hidden=true;m.setAttribute('role','dialog');m.setAttribute('aria-modal','true');m.setAttribute('aria-label','Pedido contra entrega');
m.innerHTML='<div class="pc-b"><button type="button" class="pc-x" aria-label="Cerrar">×</button><h2>Pedido contra entrega</h2><div class="pc-prod"><b id="pc-n"></b><span id="pc-p"></span></div>'
+'<form id="pc-f" novalidate><div class="pc-q"><span>Cantidad</span><div><button type="button" data-q="-1">−</button><input id="pc-c" value="1" inputmode="numeric" aria-label="Cantidad"><button type="button" data-q="1">+</button></div></div>'
+'<label>Nombre completo<input id="pc-nom" autocomplete="name" required></label><label>Celular (WhatsApp)<input id="pc-tel" type="tel" inputmode="tel" autocomplete="tel" placeholder="300 123 4567" required></label>'
+'<label>Ciudad<input id="pc-ciu" list="pc-ciud" autocomplete="address-level2" required></label><datalist id="pc-ciud">'+C.map(function(c){return '<option value="'+esc(c)+'">'}).join('')+'</datalist>'
+'<label>Barrio<input id="pc-bar" autocomplete="address-level3" required></label><label>Dirección<input id="pc-dir" autocomplete="street-address" placeholder="Calle 5 # 66-20, apto 301" required></label>'
+'<label>Indicaciones (opcional)<input id="pc-ind" placeholder="Torre, portería, llamar antes…"></label>'
+'<div class="pc-t"><span>Total a pagar al recibir</span><b id="pc-tot"></b></div><p class="pc-e" id="pc-err" hidden></p>'
+'<button class="pc-s" type="submit">Enviar pedido por WhatsApp</button><p class="pc-n">Pagas en efectivo cuando recibes. Envío gratis. Guardamos tus datos solo en este celular para tu próximo pedido.</p></form></div>';
document.body.appendChild(m);
m.addEventListener('click',function(e){if(e.target.closest('.pc-x')||(e.target===m&&!sucio()))cerrar();var q=e.target.closest('[data-q]');if(q){var c=document.getElementById('pc-c');c.value=Math.min(10,Math.max(1,(parseInt(c.value)||1)+parseInt(q.dataset.q)));tot()}});
document.getElementById('pc-c').addEventListener('input',tot);document.getElementById('pc-f').addEventListener('submit',enviar);m.addEventListener('input',guardar);m.addEventListener('click',function(e){if(e.target.closest('[data-q]'))guardar()});document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!m.hidden)cerrar()})}
function qty(){return Math.min(10,Math.max(1,parseInt(document.getElementById('pc-c').value)||1))}
function tot(){document.getElementById('pc-tot').textContent=cop(P[cur].p*qty())}
function abrir(id){if(!P[id])return;cur=id;if(!m)build();m.querySelector('.pc-b').scrollTop=0;var c=g();document.getElementById('pc-n').textContent=P[id].n;document.getElementById('pc-p').textContent=cop(P[id].p)+' c/u · envío gratis';document.getElementById('pc-c').value=1;
['nom','tel','ciu','bar','dir','ind'].forEach(function(k){var e=document.getElementById('pc-'+k);e.value=c[k]||''});var d=bor();if(d&&d.id===id){F.forEach(function(k){if(d[k])document.getElementById('pc-'+k).value=d[k]});document.getElementById('pc-c').value=d.c||1}document.getElementById('pc-err').hidden=true;tot();m.hidden=false;document.body.style.overflow='hidden';setTimeout(function(){document.getElementById(c.nom?'pc-c':'pc-nom').focus()},50)}
function cerrar(){m.hidden=true;document.body.style.overflow='';if(ok){try{localStorage.removeItem(B)}catch(e){}m.remove();m=null;ok=false;var r=document.querySelector('.pc-rt');if(r)r.remove()}else pill()}
function enviar(e){e.preventDefault();var v=function(k){return document.getElementById('pc-'+k).value.trim()},tel=v('tel').replace(/\\D/g,''),er=document.getElementById('pc-err');if(tel.length===12&&tel.indexOf('57')===0)tel=tel.slice(2);
var msg=v('nom').length<3?'Escribe tu nombre completo.':!/^3\\d{9}$/.test(tel)?'Escribe un celular válido (10 dígitos que empiezan por 3).':v('ciu').length<3?'Escribe tu ciudad.':v('bar').length<2?'Escribe tu barrio.':v('dir').length<5?'Escribe tu dirección.':'';
if(msg){er.textContent=msg;er.hidden=false;return}
var n=qty(),pr=P[cur],tx='Hola, quiero pedir *contra entrega*:\\n• '+pr.n+(pr.r?' (ref. '+pr.r+')':'')+' x'+n+'\\nPrecio: '+cop(pr.p)+' c/u (envío gratis)\\nTotal a pagar al recibir: '+cop(pr.p*n)+'\\nForma de pago: contra entrega (efectivo al recibir)\\n\\nNombre: '+v('nom')+'\\nCelular: '+tel+'\\nCiudad: '+v('ciu')+'\\nBarrio: '+v('bar')+'\\nDirección: '+v('dir')+(v('ind')?'\\nIndicaciones: '+v('ind'):'');
try{localStorage.setItem(K,JSON.stringify({nom:v('nom'),tel:tel,ciu:v('ciu'),bar:v('bar'),dir:v('dir'),ind:v('ind')}))}catch(x){}
try{window.dataLayer=window.dataLayer||[];dataLayer.push({event:'pedido_contraentrega_whatsapp',producto:cur,value:pr.p*n,currency:'COP'})}catch(x){}
var u='https://wa.me/'+WA+'?text='+encodeURIComponent(tx);ok=true;var b=m.querySelector('.pc-b');b.innerHTML='<button type="button" class="pc-x" aria-label="Cerrar">×</button><div class="pc-ok"><div class="pc-ic">✔</div><h2>Tu pedido está listo</h2><p>Se abrió WhatsApp con todos tus datos. Solo toca <b>Enviar</b> en el chat para que lo recibamos.</p><a class="pc-s pc-a" href="'+u+'" target="_blank" rel="noopener">Abrir WhatsApp otra vez</a><button type="button" class="pc-c2" id="pc-cp">Copiar mi pedido</button><p class="pc-n">Si WhatsApp no se abrió, usa el botón verde o copia tu pedido y pégalo en el chat. Tus datos no se pierden hasta que cierres esta ventana.</p></div>';
b.querySelector('#pc-cp').addEventListener('click',function(){var t=this;(navigator.clipboard?navigator.clipboard.writeText(tx):Promise.reject()).then(function(){t.textContent='✔ Copiado'},function(){t.textContent='Selecciona y copia desde WhatsApp'})});var w=window.open(u,'_blank');if(!w){/* el botón verde abre WhatsApp */}}
function pill(){var d=bor();if(!d||!P[d.id]||document.querySelector('.pc-rt')||!(d.nom||d.tel||d.dir))return;var r=document.createElement('div');r.className='pc-rt';r.innerHTML='<button type="button" data-cod="'+d.id+'">Tienes un pedido sin terminar · <b>Retomar</b></button><button type="button" class="pc-rx" aria-label="Descartar">×</button>';r.querySelector('.pc-rx').addEventListener('click',function(){try{localStorage.removeItem(B)}catch(e){}r.remove()});document.body.appendChild(r)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',pill);else pill();
document.addEventListener('click',function(e){var b=e.target.closest('[data-cod]');if(b){e.preventDefault();var r=document.querySelector('.pc-rt');if(r)r.remove();abrir(b.getAttribute('data-cod'))}})})();""" % (json.dumps(_prods, ensure_ascii=False), json.dumps(_ciu, ensure_ascii=False), WA)
(OUT / "pedido.js").write_text(PEDIDO_JS, encoding="utf-8")
PC_CSS = """
.pz{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:16px}.pz-t{display:flex;flex-direction:column;gap:4px;background:#fff;border:1px solid #e1e7f3;border-radius:16px;padding:14px;text-decoration:none;color:#14213d;transition:.2s}.pz-t:hover{box-shadow:0 12px 28px rgba(20,40,160,.15);transform:translateY(-3px)}
.pz-i{display:grid;place-items:center;aspect-ratio:1;background:#f4f7fc;border-radius:12px;margin-bottom:8px;overflow:hidden}.pz-i img{width:88%;height:88%;object-fit:contain}.pz-t b{font-size:1rem}.pz-t small{color:#5b6478}.pz-t em{font-style:normal;font-weight:800;color:#1428a0}
@media(max-width:560px){.pz{grid-template-columns:1fr 1fr;gap:12px}}
.pc-ok{text-align:center;padding:8px 0}.pc-ic{width:64px;height:64px;border-radius:50%;background:#e3f6ea;color:#1faa59;font-size:34px;display:grid;place-items:center;margin:0 auto 12px}.pc-ok h2{margin:0 0 8px}.pc-ok p{color:#3d4b6b;margin:0 0 14px}.pc-a{display:flex!important;align-items:center;justify-content:center;text-decoration:none}.pc-c2{width:100%;min-height:48px;border:1.5px solid #cfd8ee;background:#fff;border-radius:12px;font:700 1rem Inter,sans-serif;cursor:pointer;margin-top:10px;color:#14213d}
.pc-rt{position:fixed;left:12px;right:12px;bottom:76px;z-index:4000;max-width:460px;margin:0 auto;display:flex;background:#0b1f4d;border-radius:14px;box-shadow:0 10px 30px rgba(0,0,0,.3);overflow:hidden}.pc-rt button{border:0;background:none;color:#fff;font:600 .92rem Inter,sans-serif;padding:14px 16px;cursor:pointer;text-align:left;flex:1}.pc-rt b{color:#ffc21a}.pc-rt .pc-rx{flex:0 0 48px;font-size:22px;text-align:center;padding:0}
.pc-s{position:sticky;bottom:0}.pc-b form{padding-bottom:4px}
.pc-m{position:fixed;inset:0;z-index:5000;background:rgba(11,31,77,.55);display:flex;align-items:flex-end;justify-content:center;padding:0;overflow-y:auto}.pc-m[hidden]{display:none}
.pc-b{position:relative;background:#fff;width:100%;max-width:520px;border-radius:20px 20px 0 0;padding:24px 20px 28px;box-shadow:0 -10px 40px rgba(0,0,0,.25);max-height:95vh;overflow-y:auto}
@media(min-width:640px){.pc-m{align-items:center;padding:24px}.pc-b{border-radius:20px}}
.pc-b h2{font-size:1.35rem;margin:0 0 12px;color:#0b1f4d}.pc-x{position:absolute;right:14px;top:10px;border:0;background:none;font-size:30px;line-height:1;cursor:pointer;color:#5b6478}
.pc-prod{display:flex;justify-content:space-between;gap:12px;background:#f4f7fc;border:1px solid #e1e7f3;border-radius:12px;padding:12px 14px;margin-bottom:14px;font-size:.95rem}.pc-prod span{font-weight:800;color:#1428a0;white-space:nowrap}
.pc-b label{display:block;font:600 14px Inter,sans-serif;color:#2a3a5c;margin:0 0 12px}.pc-b input{display:block;width:100%;margin-top:5px;padding:13px 14px;border:1.5px solid #cfd8ee;border-radius:12px;font:400 16px Inter,sans-serif;background:#fff;box-sizing:border-box}.pc-b input:focus{outline:3px solid rgba(20,40,160,.22);border-color:#1428a0}
.pc-q{display:flex;align-items:center;justify-content:space-between;margin:0 0 12px;font:600 14px Inter,sans-serif;color:#2a3a5c}.pc-q div{display:flex;align-items:center;border:1.5px solid #cfd8ee;border-radius:12px;overflow:hidden}.pc-q button{border:0;background:#f4f7fc;width:42px;height:44px;font-size:20px;cursor:pointer}.pc-q input{width:50px!important;margin:0!important;text-align:center;border:0!important;border-radius:0!important;padding:0!important;height:44px}
.pc-t{display:flex;justify-content:space-between;align-items:center;font:700 1rem Inter,sans-serif;margin:6px 0 10px;padding-top:12px;border-top:1px dashed #cfd8ee}.pc-t b{font-size:1.4rem;color:#0b1f4d}
.pc-e{background:#fdecec;color:#a02525;border-radius:10px;padding:10px 12px;font-size:.9rem;margin:0 0 10px}.pc-s{width:100%;min-height:54px;border:0;border-radius:12px;background:#1faa59;color:#fff;font:800 1.05rem Inter,sans-serif;cursor:pointer}.pc-s:hover{background:#178a47}.pc-n{font-size:.8rem;color:#5b6478;margin:10px 0 0;text-align:center}
"""
(OUT / "tema.css").write_text((OUT / "tema.css").read_text(encoding="utf-8") + PC_CSS, encoding="utf-8")


# ---------------------------------------------------------------- tecnología: asistente, verificador, barra de compra, vistos
_tech = {x["id"]: {"n": x["nombre"], "u": x["url"], "p": x["precio"], "i": x["img"][:-5] + "-480.webp", "c": x["categoria"], "e": x["equipos_l"], "m": x["modelos"]} for x in PS}
TECH_JS = """(function(){var T=%s,C=%s,WA='%s';
function cop(n){return '$'+String(n).replace(/\\B(?=(\\d{3})+(?!\\d))/g,'.')}
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function nm(s){return String(s).toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').replace(/[^a-z0-9]+/g,'')}
function ev(n,d){try{window.dataLayer=window.dataLayer||[];d=d||{};d.event=n;dataLayer.push(d)}catch(x){}}
function wa(t){return 'https://wa.me/'+WA+'?text='+encodeURIComponent(t)}
function card(id){var p=T[id];return '<div class="tk-c"><a href="'+p.u+'"><img src="'+p.i+'" alt="'+esc(p.n)+'" loading="lazy" width="240" height="240"><b>'+esc(p.n)+'</b><span>'+(p.p?cop(p.p):'Consultar precio')+'</span></a>'+(p.p?'<div class="hx-bt"><button type="button" class="tf-add" data-add="'+id+'">🛒 Agregar</button><button type="button" class="tf-cod" data-cod="'+id+'">🚚 Contra entrega</button></div>':'')+'</div>'}
var ids=Object.keys(T);
/* 1. Asistente: encuentra tu repuesto en 3 toques (solo inicio) */
var host=document.getElementById('repuestos');
if(host&&document.querySelector('.hx')){var eqs=[];ids.forEach(function(i){T[i].e.forEach(function(e){if(eqs.indexOf(e)<0)eqs.push(e)})});
var sec=document.createElement('section');sec.className='aq-sec tk-f';sec.innerHTML='<div class="wrap"><h2>Encuentra tu repuesto en 3 toques</h2><p class="tk-s">Elige tu equipo y el tipo de pieza. Te mostramos solo lo que le sirve.</p><div class="tk-st" id="tk-st"></div><div class="tk-g" id="tk-g"></div></div>';host.parentNode.insertBefore(sec,host);
var st={e:'',c:''};function pills(a,k,on){return a.map(function(x){return '<button type="button" class="tk-p'+(on===x?' on':'')+'" data-k="'+k+'" data-v="'+esc(x)+'">'+esc(x)+'</button>'}).join('')}
function draw(){var h='<div><span>1. Mi equipo</span>'+pills(eqs,'e',st.e)+'</div>';if(st.e){var cs=[];ids.forEach(function(i){if(T[i].e.indexOf(st.e)>=0&&cs.indexOf(T[i].c)<0)cs.push(T[i].c)});h+='<div><span>2. Tipo de pieza</span>'+pills(cs,'c',st.c)+'</div>'}
document.getElementById('tk-st').innerHTML=h;var g=document.getElementById('tk-g');if(st.e&&st.c){var r=ids.filter(function(i){return T[i].e.indexOf(st.e)>=0&&T[i].c===st.c});g.innerHTML='<p class="tk-n">'+r.length+' repuesto'+(r.length>1?'s':'')+' para '+esc(st.e.toLowerCase())+'</p><div class="tk-row">'+r.map(card).join('')+'</div><p class="tk-s"><a href="'+wa('Hola, busco '+st.c.toLowerCase()+' para '+st.e.toLowerCase()+'. Mi modelo es: ')+'" rel="noopener">¿No ves tu modelo? Escríbenos →</a></p>'}else g.innerHTML=''}
sec.addEventListener('click',function(e){var b=e.target.closest('[data-k]');if(!b)return;st[b.dataset.k]=b.dataset.v;if(b.dataset.k==='e')st.c='';draw();ev('asistente_repuesto',{paso:b.dataset.k,valor:b.dataset.v})});draw()}
/* 2. Producto: verificador de ciudad y de modelo, barra de compra */
var ctas=document.querySelectorAll('.hero-cta'),pid,P;
ctas.forEach(function(cta){var add=cta.querySelector('[data-add]');pid=add&&add.getAttribute('data-add');P=pid&&T[pid];if(!P)return;var bx=document.createElement('div');bx.className='tk-b';
bx.innerHTML='<div class="tk-t"><label>¿Llega a tu ciudad?<input class="tk-ciu" list="tk-cl-'+pid+'" placeholder="Escribe tu ciudad"></label><datalist id="tk-cl-'+pid+'">'+C.map(function(c){return '<option value="'+esc(c)+'">'}).join('')+'</datalist><p class="tk-cr" hidden></p></div>'
+'<div class="tk-t"><label>¿Sirve para mi modelo?<input class="tk-mod" placeholder="Ej: WA17T6260BW"></label><p class="tk-mr" hidden></p></div>';cta.parentNode.insertBefore(bx,cta.nextSibling);
bx.querySelector('.tk-ciu').addEventListener('change',function(){var v=this.value.trim(),r=bx.querySelector('.tk-cr'),ok=C.some(function(c){return nm(c)===nm(v)});r.hidden=!v;r.className=ok?'ok':'';r.innerHTML=ok?'✔ Sí enviamos a <b>'+esc(v)+'</b> con envío gratis. Puedes pagar con Wompi o contra entrega. El tiempo exacto te lo confirmamos al pedir.':'Escríbenos para confirmar el envío a «'+esc(v)+'»: <a href="'+wa('Hola, ¿envían a '+v+'? Me interesa: '+P.n)+'" rel="noopener">WhatsApp</a>';ev('verifica_ciudad',{ciudad:v,ok:ok})});
bx.querySelector('.tk-mod').addEventListener('change',function(){var v=this.value.trim(),r=bx.querySelector('.tk-mr');if(!v){r.hidden=true;return}var q=nm(v),hit=P.m.some(function(m){var k=nm(m);return k&&(k.indexOf(q)>=0||q.indexOf(k)>=0)});r.hidden=false;r.className=hit?'ok':'';
r.innerHTML=hit?'✔ <b>'+esc(v)+'</b> aparece en la lista de modelos compatibles de este repuesto.':'No aparece en nuestra lista. No lo descartes: <a href="'+wa('Hola, ¿este repuesto sirve para mi modelo '+v+'? '+P.n)+'" rel="noopener">confírmalo por WhatsApp</a> con una foto de tu pieza.';ev('verifica_modelo',{modelo:v,ok:hit})});
if(ctas.length===1&&P.p){var sb=document.createElement('div');sb.className='tk-sb';sb.innerHTML='<div><b>'+esc(P.n)+'</b><span>'+cop(P.p)+' · envío gratis</span></div><button type="button" class="btn btn-solid" data-add="'+pid+'" data-ir="1">Comprar</button><button type="button" class="btn cod" data-cod="'+pid+'">Contra entrega</button>';document.body.appendChild(sb);
var io=new IntersectionObserver(function(en){sb.classList.toggle('on',!en[0].isIntersecting&&en[0].boundingClientRect.top<0)});io.observe(cta)}
if(ctas.length===1)try{var v=JSON.parse(localStorage.getItem('rp_vistos')||'[]').filter(function(x){return x!==pid});v.unshift(pid);localStorage.setItem('rp_vistos',JSON.stringify(v.slice(0,8)))}catch(x){}});
/* 3. Vistos recientemente */
try{var vs=JSON.parse(localStorage.getItem('rp_vistos')||'[]').filter(function(x){return T[x]&&x!==pid}).slice(0,4);var ft=document.querySelector('footer.aq-f');
if(vs.length&&ft&&(P||document.querySelector('.hx'))){var s=document.createElement('section');s.className='aq-sec tk-f';s.innerHTML='<div class="wrap"><h2>Vistos recientemente</h2><div class="tk-row">'+vs.map(card).join('')+'</div></div>';ft.parentNode.insertBefore(s,ft)}}catch(x){}
/* 4. Aparición suave de tarjetas y atajo "/" para buscar */
if('IntersectionObserver' in window&&!matchMedia('(prefers-reduced-motion:reduce)').matches){var o=new IntersectionObserver(function(en){en.forEach(function(x){if(x.isIntersecting){x.target.classList.add('tk-in');o.unobserve(x.target)}})},{rootMargin:'0px 0px -40px 0px'});document.querySelectorAll('.tf-card,.aq-tile,.tk-c').forEach(function(c){c.classList.add('tk-r');o.observe(c)})}
document.addEventListener('keydown',function(e){if(e.key==='/'&&!/INPUT|TEXTAREA/.test((document.activeElement||{}).tagName||'')){var i=document.querySelector('[data-aq-q]');if(i){e.preventDefault();i.focus()}}})})();""" % (json.dumps(_tech, ensure_ascii=False, separators=(",", ":")), json.dumps(_ciu, ensure_ascii=False, separators=(",", ":")), WA)
(OUT / "tech.js").write_text(TECH_JS, encoding="utf-8")
TECH_CSS = """
.tk-f{padding:44px 0}.tk-f h2{margin:0 0 6px}.tk-s{color:#5b6478;margin:0 0 16px}.tk-st>div{margin-bottom:14px}.tk-st>div>span{display:block;font:700 .8rem Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#1428a0;margin-bottom:8px}
.tk-p{border:1.5px solid #cfd8ee;background:#fff;border-radius:999px;padding:10px 16px;margin:0 8px 8px 0;font:600 .95rem Inter,sans-serif;cursor:pointer;color:#14213d;transition:.15s}.tk-p:hover{border-color:#1428a0}.tk-p.on{background:#1428a0;border-color:#1428a0;color:#fff}
.tk-n{font-weight:700;margin:8px 0 12px}.tk-row{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:14px}
.tk-c a{display:flex;flex-direction:column;gap:6px;text-decoration:none;color:inherit}.tk-c{display:flex;flex-direction:column;gap:6px;background:#fff;border:1px solid #e1e7f3;border-radius:16px;padding:12px;text-decoration:none;color:#14213d;transition:.2s}.tk-c:hover{box-shadow:0 10px 26px rgba(20,40,160,.14);transform:translateY(-3px)}.tk-c img{width:100%%;height:auto;aspect-ratio:1;object-fit:contain;border-radius:10px;background:#f4f7fc}.tk-c b{font-size:.88rem;line-height:1.3}.tk-c span{font-weight:800;color:#1428a0}
.tk-b{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px}.tk-t{background:#f4f7fc;border:1px solid #e1e7f3;border-radius:14px;padding:12px 14px}.tk-t label{display:block;font:700 .85rem Inter,sans-serif;color:#2a3a5c}.tk-t input{display:block;width:100%%;margin-top:6px;padding:11px 12px;border:1.5px solid #cfd8ee;border-radius:10px;font:400 15px Inter,sans-serif;box-sizing:border-box;background:#fff}.tk-t p{margin:8px 0 0;font-size:.85rem;color:#5b6478}.tk-t p.ok{color:#14733d}
@media(max-width:640px){.tk-b{grid-template-columns:1fr}}
.tk-sb{position:fixed;left:0;right:0;bottom:0;z-index:900;background:#fff;border-top:1px solid #e1e7f3;box-shadow:0 -6px 24px rgba(11,31,77,.14);display:flex;align-items:center;gap:10px;padding:10px 16px;transform:translateY(110%%);transition:transform .25s}.tk-sb.on{transform:none}.tk-sb div{flex:1;min-width:0}.tk-sb b{display:block;font-size:.9rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.tk-sb span{font-size:.8rem;color:#5b6478}.tk-sb .btn{min-height:44px;padding:0 16px;width:auto;white-space:nowrap}
@media(max-width:560px){.tk-sb .cod{display:none}.aq-wa{bottom:76px}}
.tk-r{opacity:0;transform:translateY(14px);transition:opacity .5s,transform .5s}.tk-r.tk-in{opacity:1;transform:none}
"""
(OUT / "tema.css").write_text((OUT / "tema.css").read_text(encoding="utf-8") + TECH_CSS.replace("%%", "%"), encoding="utf-8")


# ---------------------------------------------------------------- navegación móvil, ordenar, aviso al agregar
_menu = {"q": [[eq, R_EQ(eq), [[c, R_CAT(eq, c)] for c in cs]] for eq, cs in EQUIPOS.items()], "m": [[m, f"marca-{slug(m)}.html"] for m in MARCAS_EQ],
         "a": [[t, u] for t, u in ARTS_BASE] + [["Envíos a toda Colombia", "envios-a-toda-colombia.html"], ["Contacto y WhatsApp", f"https://wa.me/{WA}?text=Hola%2C%20necesito%20un%20repuesto"]]}
NAV_JS = """(function(){var M=__MENU__,WA='__WA__';
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function ev(n,d){try{window.dataLayer=window.dataLayer||[];d=d||{};d.event=n;dataLayer.push(d)}catch(x){}}
var home=!!document.querySelector('.hx');
/* menú lateral con equipos, tipos y marcas */
var dr=document.createElement('div');dr.className='nv-d';dr.hidden=true;dr.setAttribute('role','dialog');dr.setAttribute('aria-modal','true');dr.setAttribute('aria-label','Menú');
dr.innerHTML='<div class="nv-p"><div class="nv-h"><b>Menú</b><button type="button" class="nv-x" aria-label="Cerrar menú">×</button></div><div class="nv-s"><input type="search" placeholder="Busca tu repuesto o modelo" aria-label="Buscar"></div>'
+'<div class="nv-l"><a class="nv-top" href="index.html">🏠 Inicio</a><a class="nv-top" href="repuestos.html">🔎 Filtrar todos los repuestos</a>'
+'<h6>Compra por equipo</h6>'+M.q.map(function(e){return '<details><summary>'+esc(e[0])+'</summary><a href="'+e[1]+'">Todos los repuestos para '+esc(e[0].toLowerCase())+'</a>'+e[2].map(function(c){return '<a href="'+c[1]+'">'+esc(c[0])+'</a>'}).join('')+'</details>'}).join('')
+'<h6>Marcas</h6><div class="nv-m">'+M.m.map(function(m){return '<a href="'+m[1]+'">'+esc(m[0])+'</a>'}).join('')+'</div>'
+'<h6>Ayuda</h6>'+M.a.map(function(a){return '<a href="'+a[1]+'">'+esc(a[0])+'</a>'}).join('')+'<a class="nv-wa" href="https://wa.me/'+WA+'?text=Hola%2C%20necesito%20un%20repuesto" rel="noopener">💬 Escribir por WhatsApp</a></div></div>';
document.body.appendChild(dr);
function abrir(){dr.hidden=false;document.body.style.overflow='hidden';ev('menu_movil')}function cerrar(){dr.hidden=true;document.body.style.overflow=''}
dr.addEventListener('click',function(e){if(e.target===dr||e.target.closest('.nv-x')||(e.target.closest('a')&&!e.target.closest('summary')))cerrar()});
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!dr.hidden)cerrar()});
/* el buscador del menú reutiliza el del encabezado */
var si=dr.querySelector('.nv-s input');si.addEventListener('keydown',function(e){if(e.key==='Enter'&&si.value.trim()){var h=document.querySelector('[data-aq-q]');if(h){cerrar();h.value=si.value;h.dispatchEvent(new Event('input'));h.focus();scrollTo(0,0)}}});
/* barra inferior solo en celular */
var tb=document.createElement('nav');tb.className='nv-b';tb.setAttribute('aria-label','Atajos');
tb.innerHTML='<a href="index.html"><i>🏠</i>Inicio</a><button type="button" data-nv="menu"><i>☰</i>Menú</button><button type="button" data-nv="buscar"><i>🔍</i>Buscar</button><a href="carrito.php" class="nv-c"><i>🛒</i>Carrito<em hidden></em></a><a href="https://wa.me/'+WA+'?text=Hola%2C%20necesito%20un%20repuesto" rel="noopener" class="nv-w"><i>💬</i>WhatsApp</a>';
document.body.appendChild(tb);document.body.classList.add('nv-on');
tb.addEventListener('click',function(e){var b=e.target.closest('[data-nv]');if(!b)return;if(b.dataset.nv==='menu')abrir();else{scrollTo({top:0,behavior:'smooth'});setTimeout(function(){var h=document.querySelector('[data-aq-q]');if(h)h.focus()},350)}});
var cn=document.querySelector('[data-cart-n]'),em=tb.querySelector('em');function sync(){if(cn&&em){em.textContent=cn.textContent;em.hidden=!cn.textContent.trim()||cn.hidden}}if(cn){sync();new MutationObserver(sync).observe(cn,{childList:true,characterData:true,subtree:true,attributes:true})}
/* aviso al agregar al carrito */
var tt;document.addEventListener('click',function(e){var b=e.target.closest('[data-add]');if(!b||b.dataset.ir)return;clearTimeout(tt);var t=document.querySelector('.nv-t');if(!t){t=document.createElement('div');t.className='nv-t';t.setAttribute('role','status');document.body.appendChild(t)}
t.innerHTML='<span>✔ Agregado al carrito</span><a href="carrito.php">Ver carrito y pagar</a>';t.classList.add('on');tt=setTimeout(function(){t.classList.remove('on')},4500);ev('agregado_aviso')});
/* ordenar listados */
if(!home){var g=document.querySelector('.tf-grid');if(g&&g.querySelectorAll('.tf-card').length>3){var cs=[].slice.call(g.querySelectorAll('.tf-card')),bar=document.createElement('div');bar.className='nv-o';bar.innerHTML='<span>'+cs.length+' repuestos</span><label>Ordenar <select><option value="0">Recomendado</option><option value="1">Precio: menor a mayor</option><option value="2">Precio: mayor a menor</option></select></label>';g.parentNode.insertBefore(bar,g);
function pr(c){var t=c.querySelector('.tf-pr');return t?parseInt((t.textContent.match(/\\$([\\d.]+)/)||[0,'0'])[1].replace(/\\./g,''),10):0}
cs.forEach(function(c,i){c.dataset.o=i});bar.querySelector('select').addEventListener('change',function(){var v=this.value,a=cs.slice().sort(function(x,y){return v==='1'?pr(x)-pr(y):v==='2'?pr(y)-pr(x):x.dataset.o-y.dataset.o});a.forEach(function(c){g.appendChild(c)});ev('ordenar',{orden:v})})}}
})();"""
NAV_JS = NAV_JS.replace("__MENU__", json.dumps(_menu, ensure_ascii=False, separators=(",", ":"))).replace("__WA__", WA)
(OUT / "nav.js").write_text(NAV_JS, encoding="utf-8")
NAV_CSS = """
@media(max-width:820px){.hx h1{font-size:1.75rem!important;line-height:1.12!important}.hx-l p{font-size:.95rem!important;line-height:1.45}.hx-b{flex-direction:column;gap:10px}.hx-b a{text-align:center;width:100%;box-sizing:border-box}.hx-u{display:none}.hx{padding-top:24px!important}.breadcrumb{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.aq-bar{flex-wrap:nowrap;justify-content:center;gap:14px}}
@media(max-width:820px){.hero:not(.hero-prod) .sub{display:none}.hero:not(.hero-prod){padding:14px 0 64px!important}.hero:not(.hero-prod) h1{font-size:1.5rem!important;margin:0!important}.hero:not(.hero-prod) .kicker{display:none}.aq-sec{padding-top:22px!important;padding-bottom:22px!important}}
@media(hover:none){.g2-lupa{font-size:0!important}.g2-lupa::after{content:'🔍 Toca para ampliar';font-size:.8rem}}
@media(max-width:899px){.hero-prod .g2{display:contents}.hero-prod .g2-main{order:-2}.hero-prod .hero-grid>div:first-child{order:-1}.hero-prod .g2-th{order:1}.hero-prod .g2-tip{order:2}.hero-prod .hero-grid{gap:16px}.hero-prod{padding-top:18px}}
@media(max-width:820px){.ct-row{flex-wrap:nowrap!important;overflow-x:auto;scrollbar-width:none;padding-bottom:6px}.ct-row::-webkit-scrollbar{display:none}.ct-row a,.ct-row b{white-space:nowrap;flex:0 0 auto}.ct-row b{align-self:center}}
.nv-b,.nv-d{display:none}
@media(max-width:820px){
.aq-nav{display:none!important}.aq-wa{display:none!important}.aq-bar span:nth-child(2){display:none}
body.nv-on{padding-bottom:68px}
.nv-b{display:grid;grid-template-columns:repeat(5,1fr);position:fixed;left:0;right:0;bottom:0;z-index:3000;background:#fff;border-top:1px solid #dfe6f4;box-shadow:0 -4px 20px rgba(11,31,77,.1);padding:6px 4px calc(6px + env(safe-area-inset-bottom))}
.nv-b a,.nv-b button{position:relative;display:flex;flex-direction:column;align-items:center;gap:2px;border:0;background:none;font:600 .68rem Inter,sans-serif;color:#2a3a5c;text-decoration:none;padding:4px 0;cursor:pointer;min-height:48px}.nv-b i{font-style:normal;font-size:20px;line-height:1.2}.nv-w{color:#14733d!important}
.nv-b em{position:absolute;top:0;left:55%;background:#1428a0;color:#fff;border-radius:999px;font:700 .62rem Inter,sans-serif;min-width:17px;height:17px;display:grid;place-items:center;font-style:normal;padding:0 4px}
.nv-d{display:block;position:fixed;inset:0;z-index:4500;background:rgba(11,31,77,.55)}.nv-d[hidden]{display:none}
.nv-p{position:absolute;left:0;top:0;bottom:0;width:min(88vw,380px);background:#fff;display:flex;flex-direction:column;box-shadow:8px 0 30px rgba(0,0,0,.25);animation:nvs .22s}@keyframes nvs{from{transform:translateX(-100%)}to{transform:none}}
.nv-h{display:flex;justify-content:space-between;align-items:center;padding:14px 16px;border-bottom:1px solid #e6ebf6}.nv-h b{font:800 1.1rem Inter,sans-serif;color:#0b1f4d}.nv-x{border:0;background:none;font-size:30px;line-height:1;cursor:pointer;color:#5b6478}
.nv-s{padding:12px 16px}.nv-s input{width:100%;box-sizing:border-box;padding:13px 14px;border:1.5px solid #cfd8ee;border-radius:12px;font:400 16px Inter,sans-serif}
.nv-l{overflow-y:auto;padding:0 8px 24px}.nv-l h6{margin:18px 10px 6px;font:700 .75rem Inter,sans-serif;letter-spacing:.07em;text-transform:uppercase;color:#1428a0}
.nv-l a,.nv-l summary{display:block;padding:14px 12px;font:600 1rem Inter,sans-serif;color:#14213d;text-decoration:none;border-radius:10px;cursor:pointer}.nv-l a:active,.nv-l summary:active{background:#eef2ff}
.nv-l details a{padding-left:28px;font-weight:500;color:#3d4b6b}.nv-l summary{list-style:none;display:flex;justify-content:space-between}.nv-l summary::after{content:'›';font-size:1.3rem;transition:.2s}.nv-l details[open] summary::after{transform:rotate(90deg)}.nv-l summary::-webkit-details-marker{display:none}
.nv-m{display:flex;flex-wrap:wrap;gap:8px;padding:0 10px}.nv-m a{border:1.5px solid #cfd8ee;border-radius:999px;padding:8px 14px;font-size:.9rem}.nv-top{background:#f4f7fc}.nv-wa{margin:14px 10px 0;background:#1faa59;color:#fff!important;text-align:center}
.tk-sb{bottom:68px}.pc-rt{bottom:80px}.nv-t{bottom:140px!important}
}
.nv-t{position:fixed;left:12px;right:12px;bottom:24px;z-index:4200;max-width:420px;margin:0 auto;background:#0b1f4d;color:#fff;border-radius:14px;padding:14px 16px;display:flex;justify-content:space-between;gap:12px;align-items:center;font:600 .92rem Inter,sans-serif;box-shadow:0 10px 30px rgba(0,0,0,.3);transform:translateY(160%);transition:transform .25s}.nv-t.on{transform:none}.nv-t a{color:#ffc21a;white-space:nowrap}
.nv-o{display:flex;justify-content:space-between;align-items:center;margin:0 0 14px;font:600 .92rem Inter,sans-serif;color:#2a3a5c}.nv-o label{display:flex;align-items:center;white-space:nowrap}.nv-o span{white-space:nowrap}.nv-o select{margin-left:8px;padding:9px 12px;border:1.5px solid #cfd8ee;border-radius:10px;font:500 .92rem Inter,sans-serif;background:#fff}
"""
(OUT / "tema.css").write_text((OUT / "tema.css").read_text(encoding="utf-8") + NAV_CSS, encoding="utf-8")
(OUT / "nav.css").write_text(NAV_CSS, encoding="utf-8")

# ---------------------------------------------------------------- SEO extra: WebSite+buscador, manifest, feed de Google Merchant
(OUT / "manifest.webmanifest").write_text(json.dumps({"name": NOMBRE, "short_name": "Repuestos", "start_url": "/", "display": "standalone", "background_color": "#ffffff", "theme_color": "#1428a0", "lang": "es-CO",
    "icons": [{"src": "img/icono-bm.png", "sizes": "192x192", "type": "image/png"}]}, ensure_ascii=False), encoding="utf-8")
_item = lambda p: ('<item><g:id>' + esc(p["sku"]) + '</g:id><g:title>' + esc(p["nombre"][:150]) + '</g:title><g:description>' + esc(p["resumen"][:4900]) + '</g:description><g:link>' + f'{DOMINIO}/{p["url"]}' + '</g:link><g:image_link>' + f'{DOMINIO}/{p["img"]}' + '</g:image_link>'
    + '<g:availability>in_stock</g:availability><g:condition>new</g:condition><g:price>' + f'{p["precio"]}.00 COP' + '</g:price>'
    + ('<g:brand>' + esc(p["marca_prod"]) + '</g:brand>' if p["marca_prod"] and not p["marca_prod"].startswith("PENDIENTE") else '<g:identifier_exists>no</g:identifier_exists>')
    + ('<g:mpn>' + esc(p["ref"]) + '</g:mpn>' if p["ref"] != p["sku"] else '') + '<g:google_product_category>Home &amp; Garden &gt; Household Appliance Accessories</g:google_product_category><g:product_type>' + esc(p["categoria"] + " > " + p["equipo"]) + '</g:product_type>'
    + '<g:shipping><g:country>CO</g:country><g:service>Estándar</g:service><g:price>0.00 COP</g:price></g:shipping></item>')
(OUT / "feed-google-merchant.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0"><channel><title>' + esc(NOMBRE) + '</title><link>' + DOMINIO + '/</link><description>Repuestos de línea blanca con envío a toda Colombia</description>\n'
    + "\n".join(_item(p) for p in PS if p["precio"]) + '\n</channel></rss>', encoding="utf-8")

# ---------------------------------------------------------------- fichas de producto
for p in PS:
    otros = [x for x in PS if x is not p and x["equipo"] == p["equipo"]][:3]
    pv = p["espec"]
    if p["precio"]:
        precio_t = f"Cuesta <b>{cop2(p['precio'])}</b>" + (" con envío gratis a toda Colombia." if True else ".")
    else:
        precio_t = "Escríbenos por WhatsApp para confirmar el precio y la disponibilidad."
    compat = (f"Sirve para {', '.join(p['modelos'])}." if p["modelos"] else (f"Es compatible con lavadoras {p['marca_eq']}; confirma tu modelo por WhatsApp antes de comprar." if p["marca_eq"] not in ("", "Todas las marcas") else (f"Sirve para {p['equipo_txt']} de varias marcas." if p["espec"] else "Sirve para lavadoras de varias marcas; confirma con la descripción o escríbenos con el modelo.")))
    qa_p = qa(f"{p['nombre']}: ¿qué es y para qué sirve?", f"{esc(p['resumen'])} {esc(compat)} {precio_t}",
              [("Tipo", p["categoria"]), ("Equipo", p["equipo_txt"].capitalize()), ("Marca", p["marca_prod"] if p["marca_prod"] and not p["marca_prod"].startswith("PENDIENTE") else p["marca_eq"] if p["marca_eq"] != "Todas las marcas" else "Varias"), ("Precio", cop(p["precio"]) if p["precio"] else "Consultar")])
    filas = [("Tipo de pieza", p["categoria"]), ("Para", p["equipo_txt"].capitalize()), ("Marca del equipo", p["marca_eq"] or "Varias marcas")]
    if p["marca_prod"] and not p["marca_prod"].startswith("PENDIENTE"):
        filas.append(("Marca del producto", p["marca_prod"]))
    if p["ref"] != p["sku"]:
        filas.append(("Referencia", p["ref"]))
    if pv:
        filas += [("Voltaje", "110 VAC · 50/60 Hz"), ("Corriente máxima", f"{pv[0]} A (aprox. {pv[0] * 110:,} W)".replace(",", ".")), ("Tomas", str(pv[1])), ("Ciclo de espera", pv[2])] + p["extra"]
    filas += [("Modelos compatibles", ", ".join(p["modelos"]) or "Confirma tu modelo por WhatsApp"), ("Precio", cop2(p["precio"]) + " COP" if p["precio"] else "Consultar por WhatsApp"), ("Pago", "Wompi (tarjeta, PSE, Nequi, Bancolombia) o contra entrega")]
    ficha = '<div class="tbl-wrap"><table class="spec-table">' + "".join(f"<tr><th>{esc(a)}</th><td>{esc(b)}</td></tr>" for a, b in filas) + "</table></div>"
    preg = [("¿Cómo sé si esta pieza sirve para mi equipo?", "Compara el modelo de tu equipo y la descripción de la pieza. Si no estás seguro, escríbenos por WhatsApp con el modelo y una foto de la pieza vieja."),
            ("¿Puedo pagar contra entrega?", FPAGO), ("¿Hacen envíos a toda Colombia?", "Sí, por transportadora; el tiempo se confirma al hacer el pedido."), ("¿Hay retracto?", "Sí, 5 días hábiles desde la entrega, con el producto sin usar ni instalar.")]
    if pv:
        preg.append(("¿Sirve para equipos de 220 V?", "No. Este protector es de 110 VAC."))
    _cont, _faq2 = cont_seo(p)
    _hub = seccion("Más información y repuestos relacionados", '<div class="city-tags">' + f'<a href="{R_CAT(p["equipos_l"][0], p["categoria"])}">Más {esc(p["categoria"].lower())} para {esc(p["equipos_l"][0].lower())}</a><a href="{R_EQ(p["equipos_l"][0])}">Todos los repuestos para {esc(p["equipos_l"][0].lower())}</a>'
                   + (f'<a href="marca-{p["marca_s"]}.html">Repuestos {esc(p["marca_eq"])}</a><a href="{mt_url(p["equipos_l"][0], p["categoria"], p["marca_eq"])}">{esc(p["categoria"])} para {esc(p["equipos_l"][0].lower())} {esc(p["marca_eq"])}</a>' if p["marca_eq"] not in ("", "Todas las marcas") else "")
                   + '<a href="envios-a-toda-colombia.html">Envíos a toda Colombia</a><a href="envios-y-pagos.html">Medios de pago</a><a href="garantia-cambio-y-devolucion.html">Garantía y devolución</a><a href="como-encontrar-el-modelo-de-tu-electrodomestico.html">Cómo encontrar el modelo de tu equipo</a></div>', alt=True) + seccion(f"{p['corto']} en tu ciudad", '<div class="city-tags">' + "".join(f'<a href="{p["slug"]}-en-{slug(c_)}.html">{esc(c_)}</a>' for c_ in cat_php["ciudades"][:N_CIU]) + "</div>")
    _faq3 = [(f"¿Cuánto cuesta {p['nombre'].lower()}?", (f"Cuesta {cop(p['precio'])} con envío gratis a toda Colombia." if p["precio"] else "Escríbenos por WhatsApp y te confirmamos el precio.")),
             ("¿Es un producto nuevo?", "Sí, nuevo y en su empaque."), ("¿Qué medios de pago aceptan?", "Tarjeta débito o crédito, PSE, Nequi, botón Bancolombia y efectivo contra entrega, sin recargo.")]
    preg = _faq2 + preg + _faq3
    botones = (f'<div class="pay2"><button type="button" class="btn btn-solid" data-add="{p["id"]}" data-ir="1">💳 Comprar ahora<small>Pago en línea · Wompi</small></button><button type="button" class="btn cod" data-cod="{p["id"]}">🚚 Pago contra entrega<small>Llenas tus datos · pedido por WhatsApp</small></button></div>'
               f'<p class="pay2-sec"><button type="button" data-add="{p["id"]}">🛒 Agregar al carrito y seguir comprando</button></p>') if p["precio"] else f'<a class="btn btn-solid" href="{wa_pieza(p)}" rel="noopener">Consultar precio por WhatsApp</a>'
    cuerpo = (f'<section class="hero hero-prod"><div class="wrap hero-grid"><div><span class="kicker">{esc(p["categoria"])} · {esc(p["equipo_txt"])}</span><h1>{esc(p["nombre"])}</h1>'
              f'<p class="sub" style="margin-top:16px;">{esc(p["resumen"])}</p>' + (f'<div class="hero-price">{cop(p["precio"])} <small>COP · envío gratis</small></div>' if p["precio"] else '<div class="hero-price" style="font-size:1.6rem">Consulta el precio</div>')
              + f'<div class="hero-cta">{botones}</div><p class="sub" style="margin-top:14px"><a href="{wa_pieza(p)}" rel="noopener">¿Dudas con tu modelo? Escríbenos →</a></p></div>{galeria_html(p, filas)}</div></section>'
              + qa_p + seccion("Especificaciones", ficha) + _cont + _hub + faq_html(preg) + (seccion("Otros repuestos para " + p["equipo"].lower(), '<div class="tf-grid">' + "".join(tarjeta(x) for x in otros) + "</div>", alt=True) if otros else "") + GAL_JS)
    _t = f"{p['nombre']} | Envío a toda Colombia"
    if len(_t) > 66:
        _t = f"{p['nombre']} | Colombia"
    if len(_t) > 66:
        _t = p["nombre"]
    pagina(p["url"], _t, f"{p['nombre']}: {p['resumen'][:70].rstrip('. ')}. " + (f"{cop(p['precio'])} con envío gratis a toda Colombia y pago contra entrega." if p["precio"] else "Consulta el precio por WhatsApp. Envío a toda Colombia."),
           f"{p['nombre'].lower()}, {p['categoria'].lower()} {p['equipo'].lower()}, comprar {p['categoria'].lower()} colombia, {p['nombre'].lower()} precio, repuestos {p['equipo'].lower()} envio colombia", [("Inicio", "index.html"), (f"Repuestos para {p['equipo'].lower()}", R_EQ(p["equipo"])), (p["nombre"], None)], cuerpo, preg, [ld_producto(p)], prio="0.9", og=p["img"])

# ---------------------------------------------------------------- páginas por ciudad: cada repuesto en cada ciudad principal + una por ciudad
N_CIU = int(os.environ.get("TIENDA_CIUDADES", "20"))
CIU_PAG = cat_php["ciudades"][:N_CIU]
cp_url = lambda p, c: f"{p['slug']}-en-{slug(c)}.html"
ch_url = lambda c: f"repuestos-en-{slug(c)}.html"
PAGO_TXT = "tarjeta débito o crédito, PSE, Nequi o botón Bancolombia, o en efectivo contra entrega"
for c in CIU_PAG:
    for p in PS:
        otras = "".join(f'<a href="{cp_url(p, o)}">{esc(p["corto"])} en {esc(o)}</a>' for o in CIU_PAG if o != c)
        compat = ("Es compatible con: " + ", ".join(p["modelos"][:12]) + ".") if p["modelos"] else "Confirma que sirve para tu modelo escribiéndonos por WhatsApp con el modelo de tu equipo y una foto de la pieza."
        precio = cop(p["precio"]) if p["precio"] else None
        botones_c = (f'<div class="pay2"><button type="button" class="btn btn-solid" data-add="{p["id"]}" data-ir="1">💳 Comprar ahora<small>Pago en línea · Wompi</small></button><button type="button" class="btn cod" data-cod="{p["id"]}">🚚 Pago contra entrega<small>Llenas tus datos · pedido por WhatsApp</small></button></div>'
                     if p["precio"] else f'<a class="btn btn-solid" href="{wa_pieza(p)}" rel="noopener">Consultar precio por WhatsApp</a>')
        preg = [(f"¿Envían {p['nombre'].lower()} a {c}?", f"Sí. Enviamos a {c} por transportadora" + (", con envío gratis." if p["precio"] else ".") + " Al hacer el pedido te confirmamos el tiempo de entrega."),
                (f"¿Puedo pagar contra entrega en {c}?", f"Sí. Si estás en {c} puedes pedir contra entrega: llenas tus datos, nos llega el pedido por WhatsApp con el precio de esta página y pagas en efectivo al recibir, sin recargo."),
                (f"¿Cuánto cuesta {p['nombre'].lower()} en {c}?", (f"{precio} con envío gratis a {c}. Es el mismo precio en toda Colombia." if p["precio"] else "Escríbenos por WhatsApp y te confirmamos el precio.")),
                ("¿Cómo sé si sirve para mi equipo?", compat)]
        cuerpo = (f'<section class="hero hero-prod"><div class="wrap hero-grid"><div><span class="kicker">{esc(p["categoria"])} · Envío a {esc(c)}</span><h1>{esc(p["nombre"])} en {esc(c)}</h1>'
                  f'<p class="sub" style="margin-top:16px;">Compra en línea {esc(p["nombre"].lower())} y recíbelo en {esc(c)}. {esc(p["resumen"])}</p>'
                  + (f'<div class="hero-price">{precio} <small>COP · envío gratis a {esc(c)}</small></div>' if p["precio"] else "") + f'<div class="hero-cta">{botones_c}</div>'
                  f'<p class="sub" style="margin-top:14px"><a href="{p["url"]}">Ver ficha técnica completa →</a></p></div>{galeria_html(p)}</div></section>'
                  + seccion(f"Cómo comprar {p['corto'].lower()} en {c}", f'<ol class="vl"><li><b>Elige</b> «Comprar ahora» para pagar en línea con {PAGO_TXT.split(", o")[0]}, o «Pago contra entrega».</li><li><b>Llena tus datos</b> de entrega en {esc(c)}: nombre, celular, barrio y dirección.</li><li><b>Recíbelo</b> en {esc(c)}. Con contra entrega pagas en efectivo cuando llega, al precio fijo de esta página.</li></ol>')
                  + seccion(f"Datos del repuesto para {c}", f'<p style="max-width:75ch">{esc(p["nombre"])} · {esc(p["categoria"])} para {esc(p["equipo_txt"])}. {esc(compat)} Medios de pago: {PAGO_TXT}. Envío a {esc(c)} por transportadora, con confirmación por correo y WhatsApp. Compra nueva, en su empaque, con 5 días hábiles de retracto.</p>', alt=True)
                  + faq_html(preg) + seccion(f"{p['corto']} en otras ciudades", f'<div class="city-tags"><a href="{p["url"]}">Todo el país</a>{otras}</div>', alt=True)
                  + seccion(f"Más repuestos en {c}", f'<div class="city-tags"><a href="{ch_url(c)}">Todos los repuestos en {esc(c)}</a><a href="{R_CAT(p["equipos_l"][0], p["categoria"])}">{esc(p["categoria"])} para {esc(p["equipos_l"][0].lower())}</a><a href="repuestos.html">Filtrar todos los repuestos</a></div>') + GAL_JS)
        ld = [dict(ld_producto(p), **{"areaServed": {"@type": "City", "name": c}})]
        pagina(cp_url(p, c), (f"{p['nombre']} en {c} | Envío gratis" if len(f"{p['nombre']} en {c} | Envío gratis") <= 66 else (f"{p['nombre']} en {c}" if len(f"{p['nombre']} en {c}") <= 66 else p["nombre"][:66 - len(f" en {c}")].rsplit(" ", 1)[0] + f" en {c}")),
               f"Compra {p['nombre'].lower()} en {c}: " + (f"{precio} con envío gratis, " if p["precio"] else "") + "pago con Wompi o contra entrega en efectivo. Foto, compatibilidad y envío a " + c + ".",
               f"{p['nombre'].lower()} {c.lower()}, comprar {p['categoria'].lower()} {c.lower()}, repuestos {p['equipo'].lower()} {c.lower()}, {p['categoria'].lower()} {p['equipo'].lower()} en {c.lower()} contra entrega",
               [("Inicio", "index.html"), (f"Repuestos en {c}", ch_url(c)), (p["corto"], None)], cuerpo, preg, ld, prio="0.5", og=p["img"])
    # portada de la ciudad
    pag_lista(ch_url(c), f"Repuestos de línea blanca en {c} | Envío gratis", f"Repuestos para lavadoras y neveras en {c}: {CATS_TXT}. Envío gratis, pago con Wompi o contra entrega en {c}.",
              f"repuestos lavadoras {c.lower()}, repuestos neveras {c.lower()}, repuestos linea blanca {c.lower()}, filtros de agua nevera {c.lower()}", f"Repuestos de línea blanca en {c}", PS,
              f'<p style="max-width:75ch;margin-bottom:18px">Compra repuestos para tu lavadora o nevera y recíbelos en {esc(c)} con envío gratis. Pagas en línea con {PAGO_TXT.split(", o")[0]}, o contra entrega en efectivo al recibir. Cada pedido llega con foto, compatibilidad y precio fijo.</p>',
              [("Inicio", "index.html"), (f"Repuestos en {c}", None)],
              [(f"¿Hacen envíos a {c}?", f"Sí, enviamos a {c} por transportadora con envío gratis."), (f"¿Hay pago contra entrega en {c}?", "Sí, pagas en efectivo al recibir, sin recargo.")],
              pie=seccion(f"Repuestos por categoría en {c}", '<div class="city-tags">' + "".join(f'<a href="{cp_url(p, c)}">{esc(p["corto"])} en {esc(c)}</a>' for p in PS) + "</div>", alt=True))

# ---------------------------------------------------------------- catálogo con filtros por equipo, tipo, marca y precio
_fa = []
for p in PS:
    _t = tarjeta(p).replace('<article class="tf-card"', f'<article class="tf-card" data-eq="{esc("|".join(p["equipos_l"]))}" data-c="{esc(p["categoria"])}" data-m="{esc(p["marca_eq"])}" data-p="{p["precio"] or 0}" data-n="{esc(p["nombre"].lower())}"', 1)
    _fa.append(_t)
_eqs_f = list(EQUIPOS)
_cats_f = sorted({p["categoria"] for p in PS})
_mar_f = sorted({p["marca_eq"] for p in PS if p["marca_eq"] and p["marca_eq"] != "Todas las marcas"})
_chip = lambda k, v: f'<button type="button" class="fl-c" data-k="{k}" data-v="{esc(v)}">{esc(v)}</button>'
FL = ('<div class="fl"><div class="fl-b"><input type="search" id="fl-q" placeholder="Buscar por nombre, referencia o modelo" aria-label="Buscar en el catálogo"></div>'
      '<div class="fl-g"><span>Equipo</span><div>' + "".join(_chip("eq", e) for e in _eqs_f) + '</div></div>'
      '<div class="fl-g"><span>Tipo de repuesto</span><div>' + "".join(_chip("c", c) for c in _cats_f) + '</div></div>'
      '<div class="fl-g"><span>Marca del equipo</span><div>' + "".join(_chip("m", m) for m in _mar_f) + '</div></div>'
      '<div class="fl-o"><b id="fl-n"></b><button type="button" id="fl-x" hidden>Quitar filtros</button><label>Ordenar <select id="fl-s"><option value="0">Recomendado</option><option value="1">Precio: menor a mayor</option><option value="2">Precio: mayor a menor</option></select></label></div>'
      '<div class="tf-grid" id="fl-g">' + "".join(_fa) + '</div><p id="fl-0" hidden>No hay repuestos con esos filtros. <a href="https://wa.me/' + WA + '?text=Hola%2C%20busco%20un%20repuesto">Escríbenos por WhatsApp</a> y lo conseguimos.</p></div>')
FL_JS = """<script>(function(){var g=document.getElementById('fl-g'),cs=[].slice.call(g.children),st={eq:'',c:'',m:'',q:'',s:'0'};
function n(s){return String(s).toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'')}
var u=new URLSearchParams(location.search);['eq','c','m'].forEach(function(k){if(u.get(k))st[k]=u.get(k)});if(u.get('q')){st.q=u.get('q');document.getElementById('fl-q').value=st.q}cs.forEach(function(c,i){c.dataset.o=i});
function draw(){var v=0,q=n(st.q);cs.forEach(function(c){var ok=(!st.eq||c.dataset.eq.split('|').indexOf(st.eq)>=0)&&(!st.c||c.dataset.c===st.c)&&(!st.m||c.dataset.m===st.m)&&(!q||n(c.dataset.n+' '+c.textContent).indexOf(q)>=0);c.hidden=!ok;if(ok)v++});
document.querySelectorAll('.fl-c').forEach(function(b){var k=b.dataset.k,t=Object.assign({},st);t[k]=b.dataset.v;var any=cs.some(function(c){return (!t.eq||c.dataset.eq.split('|').indexOf(t.eq)>=0)&&(!t.c||c.dataset.c===t.c)&&(!t.m||c.dataset.m===t.m)});b.classList.toggle('on',st[k]===b.dataset.v);b.classList.toggle('off',!any)});document.getElementById('fl-n').textContent=v+' repuesto'+(v===1?'':'s');document.getElementById('fl-0').hidden=v>0;document.getElementById('fl-x').hidden=!(st.eq||st.c||st.m||st.q);
var a=cs.slice().sort(function(x,y){return st.s==='1'?x.dataset.p-y.dataset.p:st.s==='2'?y.dataset.p-x.dataset.p:x.dataset.o-y.dataset.o});a.forEach(function(c){g.appendChild(c)});
try{var p=new URLSearchParams();['eq','c','m'].forEach(function(k){if(st[k])p.set(k,st[k])});history.replaceState(null,'',p.toString()?'?'+p:location.pathname)}catch(e){}}
document.querySelector('.fl').addEventListener('click',function(e){var b=e.target.closest('.fl-c');if(b){st[b.dataset.k]=st[b.dataset.k]===b.dataset.v?'':b.dataset.v;draw()}if(e.target.id==='fl-x'){st.eq=st.c=st.m=st.q='';document.getElementById('fl-q').value='';draw()}});
document.getElementById('fl-q').addEventListener('input',function(){st.q=this.value;draw()});document.getElementById('fl-s').addEventListener('change',function(){st.s=this.value;draw()});draw()})();</script>"""
pagina("repuestos.html", "Todos los repuestos | Filtra por equipo y tipo", f"Filtra los repuestos por nevera, lavadora o televisor, por tipo de pieza y por marca. {len(PS)} repuestos con foto, precio fijo, envío gratis y pago contra entrega.",
       "repuestos nevera, repuestos lavadora, filtrar repuestos linea blanca, catalogo repuestos", [("Inicio", "index.html"), ("Todos los repuestos", None)],
       hero_simple("Catálogo", "Todos los repuestos de línea blanca", "Elige tu equipo, el tipo de repuesto y la marca. Verás solo lo que le sirve a tu electrodoméstico.") + seccion("Filtrar repuestos", FL) + FL_JS, prio="0.9", og=PS[0]["img"])
CSS_FL = """
.fl-b input{width:100%;box-sizing:border-box;padding:14px 16px;border:1.5px solid #cfd8ee;border-radius:12px;font:400 16px Inter,sans-serif;margin-bottom:14px}
.fl-g{margin-bottom:12px}.fl-g>span{display:block;font:700 .78rem Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#1428a0;margin-bottom:8px}.fl-g>div{display:flex;flex-wrap:wrap;gap:8px}
.fl-c{border:1.5px solid #cfd8ee;background:#fff;border-radius:999px;padding:9px 15px;font:600 .92rem Inter,sans-serif;cursor:pointer;color:#14213d}.fl-c.on{background:#1428a0;border-color:#1428a0;color:#fff}
.fl-o{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;margin:18px 0 14px;font:600 .95rem Inter,sans-serif}.fl-o select{margin-left:6px;padding:9px 12px;border:1.5px solid #cfd8ee;border-radius:10px;font:500 .92rem Inter,sans-serif;background:#fff}#fl-x{border:0;background:none;color:#1428a0;text-decoration:underline;font:600 .92rem Inter,sans-serif;cursor:pointer}
.tf-card[hidden]{display:none}.fl-c.off{opacity:.35}
"""
(OUT / "tema.css").write_text((OUT / "tema.css").read_text(encoding="utf-8") + CSS_FL, encoding="utf-8")

# ---------------------------------------------------------------- páginas por marca y tipo de repuesto (ej. «Filtros de agua para nevera Samsung»)
for (eq, c, m), v in MT.items():
    k = CONT.get(c, {})
    refs = ", ".join(x["ref"] for x in v if x["ref"] != x["sku"])[:140]
    intro = (f'<p style="max-width:75ch;margin-bottom:18px">{esc(c)} para {esc(eq.lower())} {esc(m)}: {len(v)} opción{"es" if len(v) > 1 else ""} con foto, precio fijo y envío gratis a toda Colombia'
             + (f' (referencias {esc(refs)})' if refs else "") + f'. Pagas en línea o contra entrega en efectivo. Compáralas con tu pieza actual y, si dudas, escríbenos con el modelo de tu {esc(eq.lower().rstrip("s"))} {esc(m)}.</p>')
    pie_mt = (seccion(f"Cómo elegir {c.lower()} para {eq.lower()} {m}", "<ul class=\"spec-list\">" + "".join(f"<li>{esc(x)}</li>" for x in k.get("elegir", [])) + "</ul>", alt=True) if k else "") \
        + seccion("Más repuestos relacionados", f'<div class="city-tags"><a href="{R_CAT(eq, c)}">Todos: {esc(c.lower())} para {esc(eq.lower())}</a><a href="{R_EQM(eq, m)}">Repuestos para {esc(eq.lower())} {esc(m)}</a><a href="marca-{slug(m)}.html">Repuestos {esc(m)}</a><a href="repuestos.html">Filtrar todo el catálogo</a></div>')
    pag_lista(mt_url(eq, c, m), f"{c} para {eq} {m} | Precio y envío", f"{c} para {eq.lower()} {m}: " + ", ".join(x["nombre"] for x in v[:2]) + ". Precio, foto y compatibilidad. Envío gratis a toda Colombia.",
              f"{c.lower()} {m.lower()}, {c.lower()} para {eq.lower()} {m.lower()}, comprar {c.lower()} {m.lower()}, {c.lower()} {m.lower()} colombia, {c.lower()} {m.lower()} precio", f"{c} para {eq.lower()} {m}", v, intro,
              [("Inicio", "index.html"), (f"Repuestos para {eq.lower()}", R_EQ(eq)), (f"{c} para {eq.lower()}", R_CAT(eq, c)), (m, None)],
              [(f"¿Dónde comprar {c.lower()} para {eq.lower()} {m} en Colombia?", f"Aquí: enviamos a toda Colombia con envío gratis y pago con Wompi o contra entrega."),
               (f"¿Cómo sé cuál {c.lower().rstrip('s')} sirve para mi {eq.lower().rstrip('s')} {m}?", "Compara la referencia de tu pieza vieja o el modelo de tu equipo con la ficha del producto. Si dudas, escríbenos por WhatsApp.")] + list(k.get("faq", [])[:1]), pie=pie_mt)

# ---------------------------------------------------------------- guías de repuestos (contenido útil para buscar en Google)
def lk(sku, txt=None):
    q = next((x for x in PS if x["sku"] == sku), None)
    return f'<a href="{q["url"]}">{esc(txt or q["nombre"])}</a>' if q else esc(txt or sku)
def lista(items): return "<ul class=\"spec-list\">" + "".join(f"<li>{x}</li>" for x in items) + "</ul>"
def parr(t): return f'<p style="max-width:75ch">{t}</p>'
GUIAS = []
def guia(nombre, titulo, h1, desc, kw, secciones, preg, rel):
    GUIAS.append((nombre, h1, desc))
    cuerpo = hero_simple("Guía de repuestos", h1, desc) + "".join(seccion(t, c, alt=bool(i % 2)) for i, (t, c) in enumerate(secciones)) + faq_html(preg) \
        + seccion("Repuestos relacionados", '<div class="tf-grid">' + "".join(tarjeta(x) for x in rel if x) + "</div>", alt=True)
    art = {"@type": "Article", "headline": h1, "description": desc, "inLanguage": "es-CO", "datePublished": HOY, "dateModified": HOY, "author": {"@id": f"{DOMINIO}/#tienda"}, "publisher": {"@id": f"{DOMINIO}/#tienda"}, "mainEntityOfPage": f"{DOMINIO}/{nombre}"}
    pagina(nombre, titulo, desc, kw, [("Inicio", "index.html"), ("Guías de repuestos", "guias-de-repuestos.html"), (h1, None)], cuerpo, preg, [art], prio="0.7")
_S = lambda *sk: [next((x for x in PS if x["sku"] == s_), None) for s_ in sk]
guia("presostato-lavadora-sintomas-y-como-elegirlo.html", "Presostato de lavadora: síntomas de falla y cómo elegirlo", "Presostato de lavadora: síntomas de falla y cómo elegirlo",
     "Qué hace el presostato, síntomas de que falla (llena de más, no llena, error de nivel), qué revisar antes de cambiarlo y cómo elegir el correcto para tu lavadora.", "presostato lavadora, sensor de nivel de agua lavadora, presostato dañado síntomas, presostato lavadora samsung, presostato lavadora lg",
     [("¿Qué hace el presostato de la lavadora?", parr("El presostato es el sensor de nivel de agua: mide cuánta agua hay en la tina y le avisa a la tarjeta cuándo parar de llenar o empezar a lavar.")),
      ("Síntomas de un presostato dañado", lista(["La lavadora llena de más o no llena el agua que debe.", "Muestra un error de nivel de agua.", "El ciclo se detiene o repite el llenado sin avanzar.", "Estos síntomas también pueden venir de otras piezas: no cambies el presostato sin revisar lo demás."])),
      ("Qué revisar antes de cambiarlo", lista(["Que la manguerita de aire del presostato no esté suelta, aplastada ni tapada.", "Que llegue agua con buena presión y que el filtro de la manguera de entrada no esté tapado.", "Desconecta siempre la lavadora de la corriente antes de abrirla."])),
      ("Cómo elegir el presostato correcto", lista(["La marca de tu lavadora (Samsung, LG, etc.).", "El tipo: carga superior o frontal, con o sin tecnología inverter.", "El modelo de tu lavadora, que está en la etiqueta del equipo.", "Si no estás seguro, escríbenos con el modelo y una foto de tu presostato."]))],
     [("¿Cómo sé si el presostato de mi lavadora está dañado?", "Si llena de más, no llena o muestra error de nivel puede ser el presostato, pero conviene revisar primero la manguerita de aire y el suministro de agua."), ("¿El presostato sirve para cualquier lavadora?", "No. Se elige por marca, tipo de carga y modelo.")], _S("PR-SAM-CS-INV", "PR-LG-CS-INV"))
guia("varillas-de-suspension-lavadora-cuando-cambiarlas.html", "Varillas de suspensión de lavadora: síntomas y cuándo cambiarlas", "Varillas de suspensión de lavadora: síntomas y cuándo cambiarlas",
     "Para qué sirven las varillas de suspensión, síntomas de que están gastadas (vibra, golpea, camina), qué revisar antes y por qué se cambian en juego.", "varillas de suspension lavadora, varillas lavadora samsung, lavadora vibra mucho, lavadora golpea al exprimir, amortiguadores lavadora",
     [("¿Para qué sirven las varillas de suspensión?", parr("Sostienen la tina de la lavadora y absorben la vibración del lavado y del centrifugado. Con el uso se desgastan o pierden fuerza.")),
      ("Síntomas de varillas gastadas", lista(["La lavadora vibra mucho o golpea al exprimir.", "Se mueve o «camina» mientras centrifuga.", "Hace ruidos fuertes cuando gira la tina.", "La tina se ve inclinada o roza el gabinete."])),
      ("Qué revisar primero", lista(["Que la ropa esté bien repartida y la carga no sea excesiva.", "Que la lavadora esté nivelada y las patas firmes.", "Si sigue igual, revisa las varillas."])),
      ("Cómo elegir las correctas", lista(["Marca y modelo de tu lavadora.", "El largo: mide tu varilla vieja (nuestro juego de Samsung mide 63,5 cm).", "Cámbialas en juego para que la tina quede pareja."]))],
     [("¿Cuántas varillas lleva una lavadora?", "Muchas lavadoras de carga superior usan 4. Revisa el manual o abre la tapa inferior para confirmar las de tu modelo."), ("¿Puedo cambiar las varillas yo mismo?", "Exige abrir la lavadora y levantar la tina. Si no tienes experiencia, es mejor un técnico.")], _S("VS-SAM-635"))
guia("rele-y-termico-nevera-sintomas-de-falla.html", "Relé y térmico de nevera: síntomas de falla y cómo elegir el kit", "Relé y térmico de nevera: síntomas de falla y cómo elegir el kit",
     "Qué hacen el relé PTC y el protector térmico del compresor, síntomas de falla (clic repetido, no arranca) y cómo elegir el kit según la potencia en hp.", "rele nevera, termico nevera, rele ptc nevera, kit termico y rele nevera, nevera no arranca hace clic, rele klixon",
     [("¿Qué hacen el relé PTC y el térmico?", parr("El relé PTC ayuda a arrancar el compresor y el protector térmico lo apaga si se calienta o consume de más. Juntos protegen el compresor de la nevera.")),
      ("Síntomas de falla", lista(["La nevera no enfría y se oye un clic repetido.", "El compresor no arranca o se apaga a los pocos segundos.", "El térmico se dispara seguido.", "Otras fallas del compresor dan síntomas parecidos: pide revisión técnica."])),
      ("Cómo elegir el kit", lista(["La potencia del compresor en hp (nuestro kit Klixon es para 1/12 hp a 1/2 hp).", "La forma y los terminales: compáralos con el kit que tienes.", "Es una pieza eléctrica: instálala con la nevera desconectada y, si no sabes, con un técnico."]))],
     [("¿El relé y el térmico se cambian juntos?", "Suelen cambiarse en kit porque trabajan juntos, pero un técnico puede confirmarlo midiendo el compresor."), ("¿Cómo sé la potencia de mi compresor?", "Está en la etiqueta del compresor, en la parte trasera de la nevera.")], _S("KT-NEV-KLX"))
guia("cuando-cambiar-el-filtro-de-agua-de-la-nevera.html", "Cuándo cambiar el filtro de agua de la nevera y cómo elegirlo", "Cuándo cambiar el filtro de agua de la nevera y cómo elegirlo",
     "Cada cuánto se cambia el filtro de agua de la nevera, señales de que ya está saturado, filtro interno o externo y cómo encontrar la referencia para Samsung, LG, GE y Whirlpool.", "filtro de agua nevera, cada cuanto cambiar filtro nevera, filtro nevecon samsung, filtro nevecon lg, filtro agua whirlpool, filtro ge nevera",
     [("¿Cada cuánto se cambia el filtro de agua?", parr("Normalmente cada 6 meses de uso normal, o antes si el agua cambia de sabor o el dispensador entrega menos.")),
      ("Señales de que ya hay que cambiarlo", lista(["Pasaron unos 6 meses desde el último cambio.", "El agua o el hielo tienen mal sabor, mal olor o se ven turbios.", "El dispensador sale lento.", "El aviso de cambio de filtro de la nevera está encendido."])),
      ("Filtro interno o externo", parr("El filtro interno va dentro de la nevera y el externo se instala por fuera, en la línea de agua. Mira cuál tienes antes de pedir.")),
      ("Cómo encontrar la referencia", lista(["Está impresa en el filtro viejo (por ejemplo DA29-00020B en Samsung).", "O busca el modelo de tu nevera en la etiqueta interior y compáralo con la ficha.", "Por marca: " + " · ".join(f'<a href="{mt_url("Neveras", "Filtros de agua", m_)}">{m_}</a>' for m_ in ("Samsung", "LG", "GE", "Whirlpool") if ("Neveras", "Filtros de agua", m_) in MT)]))],
     [("¿Puedo usar la nevera sin filtro?", "Muchas neveras permiten usar un tapón en vez del filtro, pero el agua no se filtra. Revisa el manual de tu modelo."), ("¿El filtro de una marca sirve en otra?", "No. Cada filtro es para ciertos modelos: compara la referencia.")],
     [x for x in PS if x["categoria"] == "Filtros de agua"][:4])
guia("filtro-de-motas-lavadora-como-limpiarlo-y-cambiarlo.html", "Filtro de motas de la lavadora: cómo limpiarlo y cuándo cambiarlo", "Filtro de motas de la lavadora: cómo limpiarlo y cuándo cambiarlo",
     "Para qué sirve el filtro de motas, cada cuánto limpiarlo, señales de que está roto y los tipos que hay (con bolsa, redondo, de marco) para lavadoras LG y Samsung.", "filtro de motas lavadora, atrapa pelusas lavadora, atrapamotas samsung, filtro motas lg, pelusas en la ropa lavadora",
     [("¿Para qué sirve el filtro de motas?", parr("Atrapa las pelusas y los hilos que se sueltan de la ropa durante el lavado, para que no vuelvan a quedar en las prendas ni tapen el desagüe.")),
      ("Cada cuánto limpiarlo", parr("Conviene limpiarlo con frecuencia, según el uso: sácalo, enjuágalo con agua y vuelve a ponerlo.")),
      ("Señales de que hay que cambiarlo", lista(["Salen pelusas pegadas en la ropa.", "El filtro está roto, deformado o con huecos en la malla.", "Se perdió o ya no encaja bien."])),
      ("Tipos de filtro", lista(["Con bolsa de malla y marco (LG).", "Redondo de plástico con malla (LG).", "De marco rectangular con rejillas (Samsung).", "Compara con el tuyo o envíanos una foto con el modelo."]))],
     [("¿El filtro de motas sirve para cualquier lavadora?", "No: cambian la forma y el tamaño según la marca y el modelo. Compara con el filtro viejo."), ("¿Cuántos filtros vienen por pedido?", "Cada ficha indica cuántas unidades trae; algunos vienen en par.")], _S("FM-LG-X2", "FM-LG-BOL", "FM-LG-RED", "FM-SAM-MOD"))
pagina("guias-de-repuestos.html", "Guías de repuestos para lavadoras y neveras", "Guías para entender, elegir y cambiar repuestos de lavadoras y neveras: presostato, varillas, relé y térmico, filtros de agua y filtros de motas.",
       "guias repuestos lavadora, guias repuestos nevera, como elegir repuestos linea blanca", [("Inicio", "index.html"), ("Guías de repuestos", None)],
       hero_simple("Guías", "Guías de repuestos para lavadoras y neveras", "Síntomas, cómo elegir la pieza correcta y cuándo llamar a un técnico.") + seccion("Todas las guías", '<div class="aq-tiles">' + "".join(f'<a class="aq-tile" href="{n_}"><b>{esc(h_)}</b><p>{esc(d_)}</p></a>' for n_, h_, d_ in GUIAS) + "</div>"), [], [], prio="0.8")
# WebSite con buscador para Google
TIENDA_LD["potentialAction"] = {"@type": "SearchAction", "target": f"{DOMINIO}/repuestos.html?q={{search_term_string}}", "query-input": "required name=search_term_string"}

# ---------------------------------------------------------------- guías y páginas de ayuda
def pag_info(nombre, titulo, desc, kw, h1, cuerpo, preg=(), prio="0.6"):
    c = hero_simple("Repuestos de línea blanca", h1, desc) + cuerpo + (faq_html(list(preg)) if preg else "") + seccion("Repuestos disponibles", '<div class="tf-grid">' + "".join(tarjeta(x) for x in PS[:3]) + "</div>", alt=True)
    pagina(nombre, titulo, desc, kw, [("Inicio", "index.html"), (h1, None)], c, preg, prio=prio)


pag_info("como-elegir-repuesto-para-lavadora.html", "Cómo elegir la manguera de tu lavadora: entrada, desagüe y tina-bomba", "Qué diferencia hay entre la manguera de entrada y la de desagüe y cómo escoger la pieza correcta para tu lavadora.",
         "como elegir manguera lavadora, manguera entrada o desague lavadora", "Cómo elegir el repuesto de tu lavadora",
         seccion("Las piezas más cambiadas", "<ul class=\"spec-list\"><li><b>Manguera de entrada:</b> lleva el agua de la llave a la lavadora. Cada una trae un color de tuerca: azul para el agua fría y naranja para la caliente.</li><li><b>Manguera de desagüe:</b> saca el agua sucia al desagüe; las hay corrugadas, largas con extensión y con funda protectora.</li><li><b>Manguera tina-bomba:</b> va dentro de la lavadora y une la tina con la bomba de desagüe.</li>"+("<li><b>Presostato:</b> sensor que mide el nivel de agua dentro de la lavadora; se vende por marca y tipo (por ejemplo, inverter).</li>" if HAY_PRESO else "")+"</ul>") +
         seccion("Cómo elegir", '<ol class="vl"><li>Identifica la pieza: entrada, desagüe o tina-bomba.</li><li>Compara la forma, el largo y las tuercas con tu pieza vieja.</li><li>Si dudas, escríbenos con una foto y el modelo.</li></ol>', alt=True), FAQ_HOME)
pag_info("como-encontrar-el-modelo-de-tu-electrodomestico.html", "Cómo encontrar el modelo de tu lavadora o nevera", "Dónde está la etiqueta del modelo en lavadoras y neveras y qué enviar por WhatsApp para confirmar que un repuesto le sirve.", "donde esta el modelo de mi lavadora, modelo de mi nevera, etiqueta modelo electrodomestico",
         "Cómo encontrar el modelo de tu electrodoméstico", seccion("Dónde mirar", "<ul class=\"spec-list\"><li><b>Lavadora:</b> en el marco de la puerta, en la parte trasera o en un costado.</li><li><b>Nevera:</b> dentro del refrigerador, en la pared lateral o cerca del cajón de verduras, y a veces atrás.</li></ul><p>Fotografía la etiqueta y la pieza dañada, y envíalas por WhatsApp para confirmar la compatibilidad.</p>"), FAQ_HOME)
pag_info("preguntas-frecuentes-repuestos.html", "Preguntas frecuentes sobre repuestos de línea blanca", "Respuestas sobre compatibilidad, precios, envíos, pago contra entrega, garantía y retracto de los repuestos.", "preguntas frecuentes repuestos", "Preguntas frecuentes", "", FAQ_HOME)
pag_info("envios-y-pagos.html", "Envíos y formas de pago | Repuestos de línea blanca", "Enviamos a toda Colombia por transportadora. Pagas con Wompi (tarjeta, PSE, Nequi, Bancolombia) o contra entrega sin recargo.", "envios repuestos colombia, contra entrega repuestos", "Envíos y formas de pago",
         seccion("Envíos", "<p>Enviamos a toda Colombia por transportadora. Te confirmamos el despacho por correo y WhatsApp; el tiempo de entrega depende de la ciudad.</p>") + seccion("Formas de pago", "<ul class=\"spec-list\"><li><b>En línea con Wompi:</b> tarjeta de crédito o débito, PSE, Nequi o botón Bancolombia.</li><li><b>Contra entrega:</b> pagas en efectivo al recibir, sin recargo.</li></ul>", alt=True),
         [("¿Cómo funciona el pago contra entrega?", "Haces el pedido, lo confirmamos y pagas cuando lo recibes."), ("¿Puedo pagar con tarjeta?", "Sí, con Wompi.")])
pag_info("envios-a-toda-colombia.html", f"Envíos a toda Colombia: {len(CIUDADES)} ciudades | Repuestos de línea blanca", f"Enviamos repuestos para lavadoras y neveras a {len(CIUDADES)} ciudades y municipios de Colombia, con envío gratis, pago con Wompi o contra entrega.",
         "envios repuestos colombia, repuestos lavadora envio todo colombia, repuestos nevera envio colombia", "Envíos a toda Colombia",
         seccion(f"Llegamos a {len(CIUDADES)} ciudades y municipios", f'<p style="max-width:75ch">Enviamos por transportadora a todo el país, con envío gratis. Si tu ciudad no está en la lista, escríbenos por WhatsApp y confirmamos la entrega.</p><div class="city-tags">' + "".join(f"<span>{esc(x)}</span>" for x in CIUDADES) + "</div>") +
         seccion("Qué repuestos puedes pedir", "<div class=\"city-tags\">" + "".join(f'<a href="{x["url"]}">{esc(x["nombre"])}</a>' for x in PS) + "</div>", alt=True),
         [("¿Hacen envíos a mi ciudad?", f"Sí, enviamos a {len(CIUDADES)} ciudades y municipios de Colombia, entre ellas " + ", ".join(TOP_CIU[:8]) + "."), ("¿Cuánto cuesta el envío?", "Es gratis."), ("¿Puedo pagar contra entrega?", "Sí, en toda Colombia, sin recargo.")], prio="0.8")
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
for _f in list(OUT.glob("*.html")) + list(OUT.glob("*.php")) + list(OUT.glob("*.css")):
    _t = _f.read_text(encoding="utf-8")
    _t2 = _t.replace("family=Bricolage+Grotesque:wght@600;800&family=Inter:wght@400;500;600;700", "family=Inter:wght@400;500;600;700;800").replace("Bricolage Grotesque", "Inter").replace("ui-monospace,Menlo,Consolas,monospace", "'Inter',system-ui,sans-serif")
    if _f.suffix == ".html":
        _t2 = _t2.replace('<div class="g2-main"><img decoding="async"', '<div class="g2-main"><img fetchpriority="high" decoding="async"', 1)
    if _f.name == "tema.css":
        _t2 += "h1,h2,h3,h4{letter-spacing:-.025em;font-weight:800}.tf-b h3{font-weight:700;letter-spacing:-.01em}"
    if _t2 != _t:
        _f.write_text(_t2, encoding="utf-8")
print(f"listo: {OUT} · {len(PAGINAS)} páginas · {len(PS)} repuestos")
_V = {}
for _f in ("tema.css", "buscar.js", "carrito.js", "pedido.js", "tech.js", "nav.js", "pasarela.css", "estilo.css"):
    if (OUT / _f).exists():
        _V[_f] = hashlib.md5((OUT / _f).read_bytes()).hexdigest()[:8]
_pat = re.compile(r"""(["'])(/?)(tema\.css|buscar\.js|carrito\.js|pedido\.js|tech\.js|nav\.js|pasarela\.css|estilo\.css)(\?v=[\w]+)?(?=["'])""")
for _h in list(OUT.glob("*.html")) + list(OUT.glob("*.php")):
    _t = _h.read_text(encoding="utf-8")
    _t2 = _pat.sub(lambda m: f"{m.group(1)}{m.group(2)}{m.group(3)}?v={_V[m.group(3)]}" if m.group(3) in _V else m.group(0), _t)
    if _t2 != _t:
        _h.write_text(_t2, encoding="utf-8")
