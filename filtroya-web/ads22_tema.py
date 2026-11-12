"""Tema «Aqua» de filtrodeaguasamsung.com: encabezado con buscador universal, portada nueva (productos arriba, selector «¿cómo es tu filtro viejo?»,
cobertura por departamentos), ficha de producto con galería y pie. Se aplica a todas las páginas del sitio sin tocar sus textos."""
import html
import json
import pathlib
import re
import unicodedata

AQUI = pathlib.Path(__file__).resolve().parent
esc = lambda s: html.escape(str(s), quote=True)
cop = lambda v: "$" + f"{int(v):,}".replace(",", ".")
WA = "573054796329"


def slug(n):
    n = unicodedata.normalize("NFKD", n).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", n).strip("-")


ICONOS = {
    "redondo": '<svg viewBox="0 0 64 64"><rect x="22" y="6" width="20" height="9" rx="3"/><rect x="16" y="15" width="32" height="43" rx="12"/><path d="M24 30h16M24 38h16"/></svg>',
    "cuadrado": '<svg viewBox="0 0 64 64"><rect x="20" y="5" width="24" height="8" rx="2"/><rect x="14" y="13" width="36" height="46" rx="5"/><path d="M22 30h20M22 38h20"/></svg>',
    "externo": '<svg viewBox="0 0 64 64"><path d="M32 3v8M32 53v8"/><rect x="22" y="11" width="20" height="42" rx="8"/><path d="M27 22h10M27 30h10"/></svg>',
    "lupa": '<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>',
    "caja": '<svg viewBox="0 0 24 24"><path d="M21 8 12 3 3 8v8l9 5 9-5z"/><path d="m3 8 9 5 9-5M12 13v8"/></svg>',
    "candado": '<svg viewBox="0 0 24 24"><rect x="4" y="10" width="16" height="11" rx="2.5"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>',
    "efectivo": '<svg viewBox="0 0 24 24"><rect x="2.5" y="6" width="19" height="12" rx="2"/><circle cx="12" cy="12" r="2.6"/></svg>',
    "retorno": '<svg viewBox="0 0 24 24"><path d="M9 14 4 9l5-5"/><path d="M4 9h10a6 6 0 0 1 0 12h-3"/></svg>',
}


class Tema:
    def __init__(self, OUT, PRODUCTOS, ciudades, galeria_html=None):
        self.OUT, self.P, self.ciudades = OUT, PRODUCTOS, ciudades
        self.galeria_html = galeria_html
        self.deptos = sorted({c["dept"] for c in ciudades.values()})
        self.por_dept = {}
        for s, c in ciudades.items():
            self.por_dept.setdefault(c["dept"], []).append((c["city"], s))
        for v in self.por_dept.values():
            v.sort()
        self.grandes = [("Bogotá D.C.", "bogota"), ("Medellín", "medellin"), ("Cali", "cali"), ("Barranquilla", "barranquilla"), ("Cartagena", "cartagena"), ("Bucaramanga", "bucaramanga"),
                        ("Cúcuta", "cucuta"), ("Pereira", "pereira"), ("Santa Marta", "santa-marta"), ("Ibagué", "ibague"), ("Manizales", "manizales"), ("Villavicencio", "villavicencio"),
                        ("Pasto", "pasto"), ("Montería", "monteria"), ("Neiva", "neiva"), ("Armenia", "armenia"), ("Soacha", "soacha"), ("Valledupar", "valledupar"), ("Popayán", "popayan"), ("Tunja", "tunja")]
        self.grandes = [(n, s) for n, s in self.grandes if s in ciudades]
        self.modelos = {"cin": ["RF28HMEDBSR", "RF263BEAESR", "RF28HFEDBSR", "RF4287HARS", "RF26J7500SR", "RF23J9011SR"], "qin": ["RF28R7351SR", "RF22R7351SG", "RF28R7201SR", "RF23M8070SR"]}

    # ---------- índice del buscador ----------
    def escribir_assets(self):
        OUT = self.OUT
        css = (AQUI / "ads22_tema.css").read_text(encoding="utf-8")
        (OUT / "tema.css").write_text(css, encoding="utf-8")
        # hoja solo con el encabezado y el pie: la usan el carrito y las páginas legales (que conservan su propio estilo)
        m = re.search(r":root\{([^}]*)\}", css)
        c1 = css[css.index("/* ---------- barra superior y encabezado ---------- */"):css.index("/* ---------- portada de página (hero) ---------- */")]
        c2 = css[css.index("/* ---------- pie ---------- */"):css.index("/* lightbox y pasarela heredados */")]
        (OUT / "aqua-shell.css").write_text(".aq-h,.aq-f,.aq-wa{" + m.group(1) + "}\n" + c1 + c2, encoding="utf-8")
        items = []
        for k, p in self.P.items():
            items.append([p["corto"] + " · " + p["ref"], p["url"], "Filtro", cop(p["precio"])])
        for s, c in self.ciudades.items():
            if (OUT / f"filtro-agua-samsung-{s}.html").exists():
                items.append([c["city"], f"filtro-agua-samsung-{s}.html", "Ciudad", c["dept"]])
        for d in self.deptos:
            if (OUT / f"filtros-samsung-{slug(d)}.html").exists():
                items.append([d, f"filtros-samsung-{slug(d)}.html", "Departamento", f"{len(self.por_dept[d])} ciudades"])
        for f in sorted(OUT.glob("filtro-nevecon-samsung-rf*.html")):
            items.append([f.stem.split("-")[-1].upper(), f.name, "Modelo de nevecón", "qué filtro usa"])
        for f in sorted(OUT.glob("referencia-filtro-samsung-*.html")):
            items.append([f.stem.replace("referencia-filtro-samsung-", "").upper(), f.name, "Código", "equivalencias"])
        prefijos = ("filtro-agua-samsung-", "filtro-haf-cin-", "filtro-haf-qin-", "filtro-externo-", "cambiar-filtro-nevecon-samsung-", "precio-filtro-nevecon-samsung-", "comprar-filtro-samsung-contra-entrega-",
                    "filtros-samsung-", "filtro-nevecon-samsung-", "referencia-filtro-samsung-")
        for f in sorted(OUT.glob("*.html")):
            if f.name in ("index.html", "404.html") or any(f.name.startswith(x) and f.name not in ("filtro-haf-cin.html", "filtro-haf-qin.html", "filtro-externo.html", "filtros-samsung-por-ciudad.html") for x in prefijos):
                continue
            if f.name in [p["url"] for p in self.P.values()]:
                continue
            m = re.search(r"<h1[^>]*>(.*?)</h1>", f.read_text(encoding="utf-8"), re.S)
            if m:
                items.append([re.sub(r"<[^>]+>", "", m.group(1)).strip(), f.name, "Guía", ""])
        js = ("(function(){var D=" + json.dumps(items, ensure_ascii=False, separators=(",", ":")) + ";"
              "function n(s){return s.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').replace(/[^a-z0-9 ]+/g,' ').trim()}"
              "var X=D.map(function(r){return n(r[0]+' '+r[2]+' '+r[3])});"
              "function buscar(q){q=n(q);if(!q)return[];var t=q.split(/ +/),o=[];for(var i=0;i<D.length;i++){var ok=true,sc=0;for(var j=0;j<t.length;j++){var p=X[i].indexOf(t[j]);if(p<0){ok=false;break}sc+=p===0?0:1}"
              "if(ok){var e=n(D[i][0]);o.push([sc+(e.indexOf(q)===0?-2:0)+(D[i][2]==='Ciudad'?0:.5),i])}}o.sort(function(a,b){return a[0]-b[0]});return o.slice(0,14).map(function(x){return D[x[1]]})}"
              "function pintar(caja,r,q){if(!q.trim()){caja.hidden=true;return}var g={},h='';r.forEach(function(x){(g[x[2]]=g[x[2]]||[]).push(x)});"
              "Object.keys(g).forEach(function(k){h+='<h6>'+k+'</h6>'+g[k].map(function(x){return '<a href=\"'+x[1]+'\"><span>'+x[0]+'</span><small>'+x[3]+'</small></a>'}).join('')});"
              "caja.innerHTML=h||'<p>No encontramos «'+q.replace(/</g,'')+'». Prueba con tu ciudad, el modelo de tu nevecón (RF28...) o el código del filtro.</p>';caja.hidden=false}"
              "document.querySelectorAll('[data-aq-q]').forEach(function(i){var c=i.parentNode.querySelector('.aq-res');i.addEventListener('input',function(){pintar(c,buscar(i.value),i.value)});"
              "i.addEventListener('focus',function(){if(i.value)pintar(c,buscar(i.value),i.value)});i.addEventListener('keydown',function(e){if(e.key==='Enter'){var a=c.querySelector('a');if(a)location.href=a.getAttribute('href')}if(e.key==='Escape')c.hidden=true})});"
              "document.addEventListener('click',function(e){document.querySelectorAll('.aq-res').forEach(function(c){if(!c.parentNode.contains(e.target))c.hidden=true});"
              "document.querySelectorAll('.aq-nav details[open]').forEach(function(d){if(!d.contains(e.target))d.removeAttribute('open')})});"
              "document.querySelectorAll('.aq-shape').forEach(function(b){b.addEventListener('click',function(){document.querySelectorAll('.aq-shape').forEach(function(x){x.setAttribute('aria-pressed','false')});b.setAttribute('aria-pressed','true');"
              "var t=document.getElementById('aq-t-'+b.dataset.k);document.querySelectorAll('.aq-r').forEach(function(x){x.hidden=true});if(t)t.hidden=false})});"
              "})();")
        (OUT / "buscar.js").write_text(js, encoding="utf-8")

    # ---------- encabezado y pie ----------
    def encabezado(self):
        P = self.P
        prod = "".join(f'<a href="{p["url"]}"><img src="{p["img"]}" alt="" width="62" height="62" loading="lazy"><span><b>{esc(p["corto"])}</b><small>{esc(p["ref"])} · {self.forma(k)}</small><em>{cop(p["precio"])}</em></span></a>' for k, p in P.items())
        deptos = "".join(f'<a href="filtros-samsung-{slug(d)}.html">{esc(d)}</a>' for d in self.deptos if (self.OUT / f"filtros-samsung-{slug(d)}.html").exists())
        grandes = "".join(f'<a href="filtro-agua-samsung-{s}.html">{esc(n)}</a>' for n, s in self.grandes[:14])
        return ('<div class="aq-h"><div class="aq-bar"><span>🚚 Envío gratis a toda Colombia</span><span>💳 Pago seguro con Wompi · 💵 Contra entrega</span><a href="tel:+' + WA + '">305 479 6329</a></div>'
                '<div class="aq-row aq-wrap"><a class="aq-brand" href="index.html"><img src="img/samsung-logo-oval.png" alt="Samsung" width="96" height="34"><span><b>Filtro de agua Samsung</b><small>Distribuidor autorizado · Colombia</small></span></a>'
                '<form class="aq-search" role="search" onsubmit="return false">' + ICONOS["lupa"].replace("<svg", '<svg aria-hidden="true"') + '<input type="search" data-aq-q placeholder="Tu ciudad, modelo de nevecón o código del filtro…" autocomplete="off" aria-label="Buscar ciudad, modelo o código"><div class="aq-res" hidden></div></form>'
                '<a class="aq-cart" href="carrito.php" aria-label="Ver carrito">🛒<span data-cart-n hidden></span></a><a class="aq-cta" href="index.html#filtros">Ver filtros</a></div>'
                '<nav class="aq-nav" aria-label="Principal"><div class="aq-wrap">'
                '<a href="index.html">Inicio</a>'
                f'<details class="aq-dd"><summary>Filtros</summary><div class="aq-pop prod"><div class="aq-wrap">{prod}</div></div></details>'
                f'<details class="aq-dd"><summary>Ciudades</summary><div class="aq-pop ciu"><div class="aq-wrap"><div><h5>Más buscadas</h5><div class="aq-chips">{grandes}</div></div><div><h5>Por departamento</h5><div class="aq-chips">{deptos}</div></div></div></div></details>'
                '<a href="guias-filtro-agua-nevecon-samsung.html">Guías</a><a href="como-identificar-filtro-samsung.html">¿Cuál es el mío?</a><a href="precio-filtro-agua-nevecon-samsung.html">Precios</a><a href="filtro-agua-samsung-por-ciudad-colombia.html">Todas las ciudades</a><a href="index.html#faq">Preguntas</a>'
                '</div></nav></div>')

    def forma(self, k):
        return {"cin": "redondo, se gira", "qin": "cuadrado, se empuja", "ext": "externo, va en la línea"}[k]

    def pie(self, wa_href=None):
        P = self.P
        refs = "".join(f'<li><a href="{p["url"]}">{esc(p["corto"])} · {cop(p["precio"])}</a></li>' for p in P.values())
        ciu = "".join(f'<li><a href="filtro-agua-samsung-{s}.html">{esc(n)}</a></li>' for n, s in self.grandes[:9])
        deptos = "".join(f'<li><a href="filtros-samsung-{slug(d)}.html">{esc(d)}</a></li>' for d in self.deptos[:9] if (self.OUT / f"filtros-samsung-{slug(d)}.html").exists())
        return ('<footer class="aq-f"><div class="aq-wrap"><div class="brandcol"><span class="logo-w"><img src="img/samsung-logo-oval.png" alt="Filtro de Agua Samsung Colombia" width="74" height="26" loading="lazy"></span>'
                '<p>Somos distribuidores autorizados para la venta de filtros de agua compatibles con equipos Samsung en Colombia. No somos Samsung Electronics ni su canal oficial de venta, ni tenemos afiliación comercial con la corporación. '
                'Los nombres y modelos se usan solo con fines descriptivos de compatibilidad.</p></div>'
                f'<div><h5>Filtros</h5><ul>{refs}<li><a href="como-identificar-filtro-samsung.html">Cómo identificar el mío</a></li><li><a href="diferencia-haf-cin-haf-qin.html">HAF-CIN vs HAF-QIN</a></li></ul></div>'
                f'<div><h5>Ciudades</h5><ul>{ciu}<li><a href="filtro-agua-samsung-por-ciudad-colombia.html"><b>Ver todas →</b></a></li></ul></div>'
                f'<div><h5>Departamentos</h5><ul>{deptos}</ul></div>'
                '<div><h5>Ayuda</h5><ul><li><a href="guias-filtro-agua-nevecon-samsung.html">Guías</a></li><li><a href="cambiar-filtro-agua-nevecon-samsung.html">Cómo cambiar el filtro</a></li><li><a href="precio-filtro-agua-nevecon-samsung.html">Precios</a></li>'
                '<li><a href="envio-filtros-samsung-colombia.html">Envíos</a></li><li><a href="garantia-cambio-y-devolucion-filtro-samsung.html">Garantía y devolución</a></li><li><a href="terminos.php">Términos</a></li><li><a href="privacidad.php">Datos personales</a></li></ul></div></div>'
                '<div class="aq-wrap aq-f-pay"><div><span class="m">Tarjeta</span><span class="m">PSE</span><span class="m">Nequi</span><span class="m">Bancolombia</span><span class="m">Contra entrega</span></div>'
                '<div>© 2026 Filtro de Agua Samsung Colombia — Distribuidor Autorizado</div></div></footer>'
                f'<a class="aq-wa" href="{wa_href or "https://wa.me/" + WA}" aria-label="WhatsApp"><svg width="22" height="22" fill="#fff" viewBox="0 0 16 16"><path d="M13.6 2.3A7.85 7.85 0 0 0 8 0C3.6 0 .07 3.56.06 7.93c0 1.4.37 2.76 1.06 3.97L0 16l4.2-1.1a7.93 7.93 0 0 0 3.8.97c4.37 0 7.93-3.56 7.93-7.93a7.9 7.9 0 0 0-2.33-5.64zM8 14.5a6.57 6.57 0 0 1-3.36-.92l-.24-.14-2.5.65.67-2.43-.16-.25A6.56 6.56 0 0 1 1.4 7.93C1.4 4.3 4.36 1.34 8 1.34a6.56 6.56 0 0 1 4.65 1.93 6.5 6.5 0 0 1 1.93 4.66c0 3.63-2.96 6.57-6.58 6.57z"/></svg><span>¿Dudas? Escríbenos</span></a>')

    # ---------- portada ----------
    def portada(self):
        P = self.P
        pr = list(P.items())
        stage = ('<div class="aq-stage" aria-hidden="false"><i></i><i></i><i></i><i></i>'
                 + "".join(f'<a class="s{i + 1}" href="{p["url"]}" aria-label="{esc(p["corto"])}"><img src="{p["img"]}" alt="Filtro de agua Samsung {esc(p["corto"])}, código {esc(p["ref"])}" width="300" height="300" {"loading=eager" if i == 1 else "loading=lazy"}></a>' for i, (k, p) in enumerate(pr[:3]))
                 + f'<span class="aq-price-tag">Desde {cop(min(p["precio"] for p in P.values()))}</span></div>')
        chips = "".join(f'<a href="filtro-nevecon-samsung-{m.lower()}.html">{m}</a>' for m in self.modelos["cin"][:2] + self.modelos["qin"][:2]) \
                + "".join(f'<a href="filtro-agua-samsung-{s}.html">{esc(n)}</a>' for n, s in self.grandes[:4])
        hero = ('<section class="aq-hero" id="inicio"><div class="wrap"><div><span class="kicker">Distribuidor autorizado · Toda Colombia</span>'
                '<h1>Filtro de Agua Samsung Original para tu Nevecón</h1>'
                '<p class="lead">Escoge tu referencia, agrégala al carrito y paga en línea o contra entrega. Te enviamos a tu ciudad y confirmamos que sea el filtro de tu nevecón antes de despachar.</p>'
                '<div class="aq-big"><form role="search" onsubmit="return false">' + ICONOS["lupa"].replace("<svg", '<svg aria-hidden="true"') + '<input type="search" data-aq-q placeholder="Escribe tu ciudad o el modelo de tu nevecón (RF28…)" autocomplete="off" aria-label="Buscar ciudad, modelo o código"><div class="aq-res" hidden></div></form></div>'
                f'<div class="aq-pop-chips"><span>Prueba:</span>{chips}</div>'
                '<div class="aq-trust"><span>Producto nuevo y sellado</span><span>Pago seguro Wompi</span><span>Contra entrega</span><span>5 días de retracto</span></div></div>'
                f'{stage}</div></section>')
        feats = {"cin": ["Cartucho redondo: se instala girando", "El más usado en French Door y Side by Side", "Cámbialo cada 6 meses"],
                 "qin": ["Cartucho cuadrado: se instala empujando", "Para nevecones Samsung más recientes", "Cámbialo cada 6 meses"],
                 "ext": ["Va fuera del nevecón, en la línea de agua", "Se conecta a la manguera del agua", "Cámbialo cada 6 meses"]}
        cards = "".join(
            f'<article class="tf-card"><a class="tf-img" href="{p["url"]}" aria-label="Ficha técnica del {esc(p["corto"])}"><img src="{p["img"]}" alt="Filtro de agua Samsung {esc(p["corto"])} original, código {esc(p["ref"])}" width="400" height="300" loading="lazy"></a>'
            f'<div class="tf-b"><h3><a href="{p["url"]}">{esc(p["corto"])}</a></h3><span class="tf-code">{esc(p["ref"])}</span>'
            f'<ul class="tf-feat">{"".join(f"<li>{esc(x)}</li>" for x in feats[k])}</ul>'
            f'<div class="tf-pr">{cop(p["precio"])}<small>COP · envío gratis</small></div>'
            f'<button type="button" class="tf-add" data-add="{k}">🛒 Agregar al carrito</button></div></article>' for k, p in P.items())
        estante = ('<section class="aq-sec" id="filtros"><div class="wrap"><h2>Elige tu filtro</h2><p class="sub2">Tres referencias reales para nevecones Samsung. Cada una con su ficha técnica completa: toca la foto o el nombre.</p>'
                   f'<div class="tf-grid">{cards}</div></div></section>')
        res = "".join(
            f'<div class="aq-result aq-r" id="aq-t-{k}" hidden><img src="{p["img"]}" alt="{esc(p["corto"])}" width="130" height="150"><div><b>{esc(p["corto"])}</b><p>{esc(p["ref"])} · {self.forma(k)}</p><div class="pr">{cop(p["precio"])}</div>'
            f'<button type="button" class="tf-add" style="margin:0" data-add="{k}">🛒 Agregar al carrito</button> <a href="{p["url"]}" style="margin-left:10px;font-weight:700">Ver ficha</a></div></div>' for k, p in P.items())
        selector = ('<section class="aq-sec alt" id="selector"><div class="wrap"><h2>¿Cuál es el tuyo? Mira tu filtro viejo</h2><p class="sub2">En 10 segundos: ¿cómo es el filtro que tienes hoy en tu nevecón?</p><div class="aq-find"><div>'
                    '<div class="aq-shapes">'
                    f'<button type="button" class="aq-shape" data-k="cin" aria-pressed="false">{ICONOS["redondo"]}Redondo<small>se gira para sacarlo</small></button>'
                    f'<button type="button" class="aq-shape" data-k="qin" aria-pressed="false">{ICONOS["cuadrado"]}Cuadrado<small>se empuja o se suelta</small></button>'
                    f'<button type="button" class="aq-shape" data-k="ext" aria-pressed="false">{ICONOS["externo"]}Externo<small>va en la manguera</small></button></div>'
                    '<p style="margin-top:16px;color:var(--ink2);font-size:14.5px">¿No lo tienes a la mano? Busca el modelo de tu nevecón arriba (por ejemplo RF28HMEDBSR) o lee <a href="como-identificar-filtro-samsung.html">cómo identificar tu filtro</a>.</p></div>'
                    f'<div><div class="aq-result aq-r" id="aq-t-ini"><div style="grid-column:1/-1;color:var(--ink2)"><b>Toca una de las tres formas</b><p>Te mostramos el filtro que corresponde, con su precio y su botón de compra.</p></div></div>{res}</div></div></div></section>')
        tiles = [("caja", "Nuevo y sellado", "Filtros nuevos, en su empaque, con la referencia impresa."), ("candado", "Pago seguro", "Wompi (Bancolombia): tarjeta, PSE, Nequi o botón Bancolombia."),
                 ("efectivo", "Contra entrega", "Paga en efectivo a la transportadora cuando recibas tu pedido."), ("retorno", "5 días de retracto", "Si pediste un filtro que no corresponde, lo cambiamos sin costo (sin usar).")]
        confianza = ('<section class="aq-sec"><div class="wrap"><h2>Compra tranquilo</h2><p class="sub2">Una tienda en línea como las grandes: carrito, pago seguro y confirmación por correo.</p><div class="aq-tiles">'
                     + "".join(f'<div class="aq-tile">{ICONOS[i]}<b>{esc(t)}</b><p>{esc(d)}</p></div>' for i, t, d in tiles) + '</div>'
                     '<div class="aq-pay"><span>Visa</span><span>Mastercard</span><span>PSE</span><span>Nequi</span><span>Bancolombia</span><span>Contra entrega</span></div></div></section>')
        dep_links = "".join(f'<a href="filtros-samsung-{slug(d)}.html">{esc(d)}</a>' for d in self.deptos if (self.OUT / f"filtros-samsung-{slug(d)}.html").exists())
        top = "".join(f'<a href="filtro-agua-samsung-{s}.html">{esc(n)}<small>{esc(self.ciudades[s]["dept"])}</small></a>' for n, s in self.grandes)
        cobertura = (f'<section class="aq-sec alt" id="cobertura"><div class="wrap"><h2>Llegamos a {len(self.ciudades)} ciudades y municipios de Colombia</h2>'
                     '<p class="sub2">Escribe tu ciudad en el buscador de arriba o entra por tu departamento.</p>'
                     f'<div class="aq-top-ciu">{top}</div><h3 style="margin-top:26px;font-size:1.1rem">Por departamento</h3><div class="aq-depts">{dep_links}</div>'
                     '<p><a class="btn-solid" href="filtro-agua-samsung-por-ciudad-colombia.html" style="display:inline-flex">Ver todas las ciudades</a></p></div></section>')
        tabla = ('<section class="aq-sec"><div class="wrap"><h2>Los tres filtros, lado a lado</h2><p class="sub2">Compara referencia, forma, instalación y precio.</p><div class="tbl-wrap aq-cmp"><table class="spec-table"><tr><th></th>'
                 + "".join(f'<th><a href="{p["url"]}" style="color:#fff">{esc(p["corto"])}</a></th>' for p in P.values()) + '</tr>'
                 + "<tr><td><b>Código Samsung</b></td>" + "".join(f'<td>{esc(p["ref"])}</td>' for p in P.values()) + "</tr>"
                 + "<tr><td><b>Forma</b></td><td>Redondo</td><td>Cuadrado</td><td>Cilíndrico, externo</td></tr>"
                 + "<tr><td><b>Instalación</b></td><td>Se gira</td><td>Se empuja</td><td>En la manguera del agua</td></tr>"
                 + "<tr><td><b>Cambio</b></td><td>Cada 6 meses</td><td>Cada 6 meses</td><td>Cada 6 meses</td></tr>"
                 + "<tr><td><b>Precio</b></td>" + "".join(f'<td><b>{cop(p["precio"])}</b></td>' for p in P.values()) + "</tr></table></div></div></section>")
        return hero + estante + selector + confianza + tabla + cobertura

    def rapida(self):
        return ('<section class="aq-quick"><div class="wrap"><div class="aq-qgrid">' + "".join(
            f'<div class="aq-q"><a href="{p["url"]}"><img src="{p["img"]}" alt="Filtro Samsung {esc(p["corto"])}" width="84" height="84" loading="lazy"></a><div><b>{esc(p["corto"])}</b><small>{esc(p["ref"])} · {self.forma(k)}</small><span>{cop(p["precio"])}</span></div>'
            f'<button type="button" data-add="{k}">🛒 Agregar</button></div>' for k, p in self.P.items()) + '</div></div></section>')

    # ---------- aplicar a una página ----------
    def aplicar(self, t, nombre, ld_home=None):
        if "tema.css" in t:
            return t
        # los municipios del listado extra solo tienen página de ciudad y de precio: lo demás apunta a la página general
        general = {"filtro-haf-cin-": "filtro-haf-cin.html", "filtro-haf-qin-": "filtro-haf-qin.html", "filtro-externo-": "filtro-externo.html",
                   "comprar-filtro-samsung-contra-entrega-": "filtro-samsung-contra-entrega.html", "cambiar-filtro-nevecon-samsung-": "cambiar-filtro-agua-nevecon-samsung.html"}

        def arreglar(m):
            u = m.group(1)
            if not (self.OUT / u).exists():
                for pre, g in general.items():
                    if u.startswith(pre):
                        return f'href="{g}"'
            return m.group(0)
        t = re.sub(r'href="((?:filtro-haf-cin-|filtro-haf-qin-|filtro-externo-|comprar-filtro-samsung-contra-entrega-|cambiar-filtro-nevecon-samsung-)[a-z0-9-]+\.html)"', arreglar, t)
        # estilos: el bloque inline pasa a una hoja compartida
        t = re.sub(r"<style>.*?</style>", '<link rel="stylesheet" href="tema.css?v=aqua1">', t, count=1, flags=re.S)
        t = t.replace("family=Space+Grotesk:wght@500;700&family=Inter:wght@400;500;600;700", "family=Bricolage+Grotesque:wght@600;800&family=Inter:wght@400;500;600;700")
        # encabezado: todo lo que hay entre la barra superior y el primer contenido
        t, n = re.subn(r'<div class="util-bar">.*?(?=<div class="breadcrumb|<section class="hero"|<section class="pick")', self.encabezado(), t, count=1, flags=re.S)
        assert n == 1, nombre
        # pie y botón de WhatsApp
        wa = re.search(r'<a href="(https://wa\.me/[^"]+)" style="position:fixed;bottom:20px;right:20px[^>]*>.*?</a>', t, re.S)
        wa_href = wa.group(1) if wa else None
        t = re.sub(r'<a href="https://wa\.me/[^"]+" style="position:fixed;bottom:20px;right:20px[^>]*>.*?</a>', "", t, flags=re.S)
        t = re.sub(r'<a class="cart-fab"[^>]*>.*?</a>', "", t, flags=re.S)
        t, n = re.subn(r"<footer>.*?</footer>", lambda m: self.pie(wa_href), t, count=1, flags=re.S)
        assert n == 1, nombre
        t = t.replace("</body>", '<script src="buscar.js" defer></script></body>', 1)
        if nombre == "index.html":
            t, n1 = re.subn(r'<section class="hero">.*?</section>', lambda m: self.portada(), t, count=1, flags=re.S)
            t, n2 = re.subn(r'<section class="pick" id="elige-tu-filtro">.*?</section>', "", t, count=1, flags=re.S)
            assert n1 == 1, nombre
        elif 'hero-grid' in t.split('<section id="respuesta-rapida', 1)[0]:
            t = t.replace('<section class="hero">', '<section class="hero hero-prod">', 1)
        elif re.match(r"(filtro-agua-samsung-|filtro-haf-cin-|filtro-haf-qin-|filtro-externo-|cambiar-filtro-nevecon-samsung-|precio-filtro-nevecon-samsung-|comprar-filtro-samsung-contra-entrega-|filtro-nevecon-samsung-rf|filtros-samsung-)", nombre) and "filtro-agua-samsung-por-ciudad" not in nombre:
            t = re.sub(r'(<section class="hero">.*?</section>)', lambda m: m.group(1) + self.rapida(), t, count=1, flags=re.S)
        return t
