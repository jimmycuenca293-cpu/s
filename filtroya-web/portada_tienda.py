"""Portada de FiltrosNevecones con estructura de gran almacén (como las tiendas por departamentos de Colombia):
franja de promoción, cabecera de una fila con menú de marcas, carrusel de banners por marca, círculos de categorías,
estantes de productos con flechas, promociones en mosaico, tiendas por marca y pie grande.
No lleva buscador: la otra tienda ya lo tiene. Es HTML completo en el servidor, así Google ve marcas, productos y textos."""
import html

esc = lambda s: html.escape(str(s), quote=True)
cop = lambda n: "$ " + f"{n:,}".replace(",", ".")

FAQ = [
    ("¿Cómo sé cuál filtro le sirve a mi nevera?",
     "Mira la referencia impresa en el filtro viejo (por ejemplo DA29-00020B, LT1000P o EDR1RXD1) o el modelo en la etiqueta de la nevera. Entra a la página de tu marca y la referencia te lleva al filtro correcto. Si dudas, escríbenos por WhatsApp y te ayudamos."),
    ("¿Cada cuánto se cambia el filtro de agua de la nevera?",
     "Cada 6 meses o cuando se enciende la luz del filtro, lo que pase primero. Si el agua sale con mal sabor, olor o sale poca agua, también toca cambiarlo."),
    ("¿El envío tiene costo?",
     "No. El envío es gratis a toda Colombia y llega entre 2 y 3 días hábiles a las principales ciudades. Te damos número de guía para seguir el paquete."),
    ("¿Cómo pago?",
     "En línea, en una página de pago segura, con tarjeta débito o crédito, PSE, Nequi o botón Bancolombia. Puedes agregar varios filtros al carrito y pagar una sola vez."),
    ("¿Es difícil instalar el filtro?",
     "No. Los filtros internos se cambian en 2 minutos y sin herramientas; los externos van en la manguera del agua y toman de 10 a 15 minutos. En cada página del filtro está el paso a paso."),
    ("¿Los filtros son originales?",
     "Vendemos filtros nuevos, en su empaque, de las referencias de cada marca y sus equivalentes compatibles. Cada página indica la referencia exacta."),
]

BANNER = {
    "Samsung": ("Filtros Samsung", "HAF-CIN, HAF-QIN, Aqua-Pure Plus y el externo de manguera para neveras de dos puertas, French door y Family Hub.", "sam-cin-o"),
    "LG": ("Filtros LG", "LT1000P, LT700P, LT800P, LT500P, LT600P y el externo para neveras French door y de dos puertas.", "lg-1000-o"),
    "Whirlpool": ("Filtros Whirlpool", "EveryDrop del 1 al 5 para Whirlpool, Maytag, KitchenAid, Jenn-Air y Amana, y el externo de manguera.", "wp-1-o"),
    "GE": ("Filtros GE", "MWF y XWF para neveras GE y GE Profile. Agua y hielo limpios todo el año.", "ge-mwf-o"),
}

ICONOS = {
    "interno": '<svg viewBox="0 0 24 24"><rect x="6" y="3" width="12" height="18" rx="3"/><path d="M6 10h12M15 6v2M15 13v3"/></svg>',
    "externo": '<svg viewBox="0 0 24 24"><path d="M3 12h4m10 0h4"/><rect x="7" y="8" width="10" height="8" rx="2"/></svg>',
    "pack": '<svg viewBox="0 0 24 24"><rect x="4" y="9" width="7" height="11" rx="2"/><rect x="13" y="9" width="7" height="11" rx="2"/><path d="M8 5h8"/></svg>',
    "instalacion": '<svg viewBox="0 0 24 24"><path d="M14.5 6.5a4 4 0 0 0-5 5L4 17l3 3 5.5-5.5a4 4 0 0 0 5-5l-2.5 2.5-2-2z"/></svg>',
    "guias": '<svg viewBox="0 0 24 24"><path d="M5 4h10a3 3 0 0 1 3 3v13H8a3 3 0 0 1-3-3z"/><path d="M8 8h7M8 12h7"/></svg>',
    "envios": '<svg viewBox="0 0 24 24"><path d="M3 6h11v10H3zM14 9h4l3 3v4h-7"/><circle cx="7" cy="18" r="1.6"/><circle cx="17" cy="18" r="1.6"/></svg>',
}

JS_PORTADA = r"""(function () {
  var car = document.getElementById('fx-car'); if (!car) return;
  var pts = document.querySelectorAll('.fx-pts button'), n = pts.length, i = 0, t;
  function ir(k) { i = (k + n) % n; car.scrollTo({left: car.clientWidth * i, behavior: 'smooth'}); marcar(); }
  function marcar() { pts.forEach(function (b, j) { b.setAttribute('aria-current', j === i ? 'true' : 'false'); }); }
  pts.forEach(function (b, j) { b.addEventListener('click', function () { ir(j); auto(); }); });
  car.addEventListener('scroll', function () { var k = Math.round(car.scrollLeft / car.clientWidth); if (k !== i) { i = k; marcar(); } });
  function auto() { clearInterval(t); if (!matchMedia('(prefers-reduced-motion: reduce)').matches) t = setInterval(function () { ir(i + 1); }, 6000); }
  car.addEventListener('pointerdown', function () { clearInterval(t); }); auto(); marcar();
  document.querySelectorAll('[data-fila]').forEach(function (btn) {
    btn.addEventListener('click', function () { var f = document.getElementById(btn.getAttribute('data-fila')); f.scrollBy({left: (btn.dataset.dir === 'a' ? -1 : 1) * f.clientWidth * .85, behavior: 'smooth'}); });
  });
})();
"""

CSS = """
/* ===== FiltrosNevecones: tienda por departamentos (cabecera, portada y pie) ===== */
:root{--fx-deep:#0b3b3c;--fx-deep2:#0f5e57;--fx-teal:#0e8f78;--fx-mint:#5eead4;--fx-amb:#f5b301;--fx-amb2:#ffc21a;--fx-bg:#f4f6f6;--fx-ink:#0b2a2b;--fx-mut:#52696a;--fx-line:#dfe7e6;--fx-f:Sora,"Segoe UI",system-ui,sans-serif}
.fx-wrap{max-width:1280px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.fx-util{background:var(--fx-amb2);color:#2a1d00;font:600 13px var(--fx-f)}.fx-util .fx-wrap{display:flex;justify-content:space-between;gap:12px;padding-block:7px;flex-wrap:wrap}.fx-util a{color:#2a1d00;text-decoration:none;font-weight:700}.fx-util nav{display:flex;gap:18px}
.fx-head{background:#fff;border-bottom:1px solid var(--fx-line);position:sticky;top:0;z-index:40}
.fx-head-in{display:flex;align-items:center;gap:6px;padding-block:10px}
.fx-logo{display:flex;align-items:center;gap:9px;text-decoration:none;color:var(--fx-ink);font:800 23px/1 var(--fx-f);letter-spacing:-.03em;margin-right:12px}.fx-logo img{border-radius:10px}.fx-logo b{color:var(--fx-teal)}.fx-logo small{font-size:13px;font-weight:600;color:var(--fx-mut);letter-spacing:0;margin-left:1px}
.fx-todas summary{list-style:none;cursor:pointer;background:var(--fx-deep);color:#fff;font:700 14px var(--fx-f);padding:11px 18px;border-radius:99px;white-space:nowrap}.fx-todas summary::-webkit-details-marker{display:none}.fx-todas summary::before{content:"☰  "}
.fx-mega{position:absolute;left:0;right:0;top:100%;background:#fff;border-bottom:1px solid var(--fx-line);box-shadow:0 24px 40px rgba(11,42,43,.15);display:grid;grid-template-columns:repeat(4,1fr);gap:8px 24px;padding:22px max(16px,calc((100% - 1280px)/2 + 16px));z-index:45}
.fx-mega div{display:flex;flex-direction:column}.fx-mega a{padding:6px 0;font-weight:500;font-size:14px;color:var(--fx-ink);text-decoration:none;display:flex;justify-content:space-between;gap:10px}.fx-mega a:hover{color:var(--fx-teal)}.fx-mega small{color:var(--fx-mut)}.fx-mega .fx-mh{font-weight:800;color:var(--fx-teal);font-size:15px}
.fx-menu{display:flex;align-items:center;gap:2px;margin-left:8px;overflow-x:auto;scrollbar-width:none;flex:1}.fx-menu::-webkit-scrollbar{display:none}.fx-menu a{white-space:nowrap;text-decoration:none;color:var(--fx-ink);font:600 14px var(--fx-f);padding:10px 12px;border-radius:99px}.fx-menu a:hover{background:var(--fx-bg);color:var(--fx-teal)}
.fx-wa{display:flex;align-items:center;gap:7px;background:#1fa855;color:#fff;text-decoration:none;font:700 13px var(--fx-f);padding:9px 14px;border-radius:99px;white-space:nowrap}.fx-wa svg{width:18px;height:18px;fill:#fff}
.fx-carro{position:relative;display:flex;align-items:center;gap:8px;text-decoration:none;color:var(--fx-ink);font:700 14px var(--fx-f);padding:8px 10px;border-radius:12px}.fx-carro:hover{background:var(--fx-bg)}.fx-carro svg{width:26px;height:26px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.fx-carro span{position:absolute;top:0;left:24px;min-width:19px;height:19px;border-radius:10px;background:var(--fx-amb);color:#2a1d00;font-size:11px;display:grid;place-items:center;padding:0 4px}
@media (max-width:900px){.fx-head-in{flex-wrap:wrap}.fx-menu{order:5;flex:1 0 100%;margin:0}.fx-wa span{display:none}.fx-wa{padding:9px}.fx-carro b{display:none}.fx-logo{margin-right:auto}.fx-mega{grid-template-columns:1fr 1fr;position:fixed;top:auto;max-height:70vh;overflow:auto}.fx-util nav{display:none}}
.fx-btn{display:inline-block;background:var(--fx-amb2);color:#2a1d00;font:800 15px/1.2 var(--fx-f);padding:13px 22px;border-radius:99px;text-decoration:none;border:2px solid var(--fx-amb2)}.fx-btn:hover{background:var(--fx-amb)}.fx-btn.fx-sec{background:transparent;color:inherit;border-color:currentColor}
.fx-home{background:var(--fx-bg);color:var(--fx-ink);font-family:var(--f,system-ui,sans-serif)}.fx-home h1,.fx-home h2,.fx-home h3{font-family:var(--fx-f);letter-spacing:-.02em;text-wrap:balance}
.fx-car{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none}.fx-car::-webkit-scrollbar{display:none}
.fx-sl{flex:0 0 100%;scroll-snap-align:start;background:var(--c);color:#fff;position:relative;overflow:hidden}.fx-sl-in{display:grid;grid-template-columns:1.1fr .9fr;gap:24px;align-items:center;min-height:380px;padding-block:34px}
.fx-sl::after{content:"";position:absolute;right:-8%;top:-30%;width:55%;aspect-ratio:1;border-radius:50%;background:rgba(255,255,255,.08)}
.fx-eye{display:inline-block;color:var(--fx-amb2);font:700 12px var(--fx-f);letter-spacing:.14em;text-transform:uppercase}.fx-sl h1,.fx-sl h2{font-size:clamp(30px,4.6vw,54px);line-height:1.05;margin:10px 0 12px}.fx-sl p{color:rgba(255,255,255,.88);font-size:17px;line-height:1.55;max-width:50ch}
.fx-desde{display:inline-flex;flex-direction:column;margin:6px 0 18px}.fx-desde small{font-size:12px;opacity:.8}.fx-desde b{font:800 32px var(--fx-f)}
.fx-sl-img{position:relative;z-index:1;display:grid;place-items:center}.fx-sl-img span{display:block;background:#fff;border-radius:28px;width:min(100%,330px);aspect-ratio:1;padding:16px;box-shadow:0 30px 60px rgba(0,0,0,.3);transform:rotate(3deg)}.fx-sl-img picture,.fx-sl-img img{display:block;width:100%;height:100%;object-fit:contain}
.fx-pts{display:flex;justify-content:center;gap:8px;padding:10px;background:#fff}.fx-pts button{width:10px;height:10px;border-radius:50%;border:0;background:#c5d3d1;cursor:pointer;padding:0}.fx-pts button[aria-current=true]{background:var(--fx-teal);width:28px;border-radius:6px}
@media (max-width:820px){.fx-sl-in{grid-template-columns:1fr;min-height:0;padding-block:28px}.fx-sl-img span{width:200px}.fx-sl-img{order:-1}}
.fx-bur{background:#fff;border-bottom:1px solid var(--fx-line)}.fx-bur ul{list-style:none;margin:0;padding:18px 0;display:flex;gap:18px;overflow-x:auto;scrollbar-width:none;justify-content:space-between}.fx-bur li{flex:0 0 auto}
.fx-bur a{display:flex;flex-direction:column;align-items:center;gap:8px;text-decoration:none;color:var(--fx-ink);font:700 12.5px var(--fx-f);width:88px;text-align:center}.fx-bur .fx-c{width:72px;height:72px;border-radius:50%;background:var(--fx-bg);display:grid;place-items:center;border:2px solid var(--fx-line);overflow:hidden;transition:border-color .15s}.fx-bur a:hover .fx-c{border-color:var(--fx-teal)}
.fx-c img{width:78%;height:78%;object-fit:contain}.fx-c svg{width:32px;height:32px;fill:none;stroke:var(--fx-deep2);stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}
.fx-sec{padding-block:30px}.fx-sec h2{font-size:clamp(21px,2.6vw,28px);margin:0}.fx-sub{color:var(--fx-mut);margin:6px 0 0}
.fx-est-h{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:14px}.fx-est-h a.fx-ver{color:var(--fx-teal);font-weight:700;text-decoration:none;font-size:14px}
.fx-tienda{background:#fff;border:1px solid var(--fx-line);border-radius:20px;overflow:hidden}.fx-tienda-h{display:flex;align-items:center;gap:14px;background:var(--c);color:#fff;padding:14px 20px;flex-wrap:wrap}.fx-tienda-h .fx-lg{background:#fff;border-radius:10px;padding:6px 12px;display:flex;align-items:center;height:44px}.fx-tienda-h .fx-lg img{max-height:30px;width:auto;display:block}
.fx-tienda-h h2{color:#fff;font-size:20px}.fx-tienda-h a{margin-left:auto;color:#fff;font-weight:700;text-decoration:none;font-size:14px;border:2px solid rgba(255,255,255,.7);border-radius:99px;padding:7px 16px}.fx-tienda-h a:hover{background:#fff;color:var(--c)}
.fx-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(185px,1fr));gap:14px;padding:16px}
.fx-fila-w{position:relative}.fx-fila{display:grid;grid-auto-flow:column;grid-auto-columns:minmax(215px,230px);gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;padding-bottom:6px}.fx-fila::-webkit-scrollbar{display:none}.fx-fila .fx-card{scroll-snap-align:start}
.fx-fl{position:absolute;top:38%;width:42px;height:42px;border-radius:50%;border:1px solid var(--fx-line);background:#fff;box-shadow:0 8px 20px rgba(11,42,43,.2);cursor:pointer;font-size:18px;z-index:3;color:var(--fx-ink)}.fx-fl[data-dir=a]{left:-6px}.fx-fl[data-dir=s]{right:-6px}
@media (max-width:700px){.fx-fl{display:none}}
.fx-card{background:#fff;border:1px solid var(--fx-line);border-radius:16px;display:flex;flex-direction:column;overflow:hidden;min-width:0;position:relative}.fx-card:hover{box-shadow:0 14px 30px rgba(11,42,43,.12)}
.fx-ph{display:block;background:#fff;aspect-ratio:1/1;position:relative}.fx-ph picture{position:absolute;inset:10px;display:block}.fx-ph img{width:100%;height:100%;object-fit:contain;display:block}.fx-b{display:flex;flex-direction:column;gap:5px;padding:12px 14px 16px;flex:1}
.fx-m{font-size:11px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:var(--fx-mut)}.fx-b h3{font-size:15px;line-height:1.3;margin:0}.fx-b h3 a{color:inherit;text-decoration:none}.fx-ref{font-family:ui-monospace,Menlo,monospace;font-size:12px;color:var(--fx-teal)}
.fx-pr{display:flex;flex-direction:column;margin-top:6px}.fx-pr b{font:800 22px var(--fx-f)}.fx-pr small{color:var(--fx-teal);font-weight:700;font-size:12px}.fx-pack{font-size:12px;color:var(--fx-mut);margin-top:2px}.fx-pack b{color:var(--fx-ink)}
.fx-add{margin-top:auto;border:0;border-radius:99px;background:var(--fx-amb2);color:#2a1d00;font:800 14px var(--fx-f);padding:12px;cursor:pointer}.fx-add:hover{background:var(--fx-amb)}
.fx-sello{position:absolute;top:10px;left:10px;background:var(--fx-deep);color:#fff;font:700 11px var(--fx-f);padding:4px 9px;border-radius:99px;z-index:2}
.fx-mos{display:grid;grid-template-columns:1.3fr 1fr 1fr;gap:14px}.fx-mo{display:flex;flex-direction:column;justify-content:flex-end;gap:6px;border-radius:20px;padding:24px;min-height:230px;color:#fff;text-decoration:none;background:var(--c);position:relative;overflow:hidden}.fx-mo b{font:800 22px/1.15 var(--fx-f);position:relative}.fx-mo span{font-size:14px;position:relative;opacity:.92}.fx-mo i{font-style:normal;font-weight:800;color:var(--fx-amb2);position:relative}.fx-mo:hover{filter:brightness(1.08)}
.fx-mo svg{position:absolute;right:14px;top:14px;width:84px;height:84px;fill:none;stroke:rgba(255,255,255,.28);stroke-width:1.2}
@media (max-width:820px){.fx-mos{grid-template-columns:1fr}.fx-mo{min-height:150px}}
.fx-conf{background:#fff;border-block:1px solid var(--fx-line)}.fx-conf ul{list-style:none;margin:0;padding:22px 0;display:grid;grid-template-columns:repeat(4,1fr);gap:18px}.fx-conf li{display:flex;gap:12px;align-items:flex-start}.fx-conf svg{width:34px;height:34px;flex:0 0 auto;fill:none;stroke:var(--fx-teal);stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}.fx-conf b{display:block;font:700 15px var(--fx-f)}.fx-conf span{color:var(--fx-mut);font-size:13px}
@media (max-width:820px){.fx-conf ul{grid-template-columns:1fr 1fr}}
.fx-refs{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}.fx-refs a{background:#fff;border:1px solid var(--fx-line);border-radius:99px;padding:6px 13px;font:600 13px ui-monospace,Menlo,monospace;text-decoration:none;color:var(--fx-ink)}.fx-refs a:hover{border-color:var(--fx-teal);color:var(--fx-teal)}
.fx-ciu{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}.fx-ciu a{background:#fff;border:1px solid var(--fx-line);border-radius:99px;padding:8px 16px;text-decoration:none;color:var(--fx-ink);font-weight:600;font-size:14px}.fx-ciu a:hover{border-color:var(--fx-teal);color:var(--fx-teal)}.fx-ciu .fx-mas{background:var(--fx-teal);color:#fff;border-color:var(--fx-teal)}
.fx-guias{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}.fx-guia{display:flex;flex-direction:column;gap:8px;background:#fff;border:1px solid var(--fx-line);border-radius:14px;padding:16px;text-decoration:none;color:var(--fx-ink)}.fx-guia b{font:700 15px/1.35 var(--fx-f)}.fx-guia span{color:var(--fx-teal);font-weight:700;font-size:13px;margin-top:auto}.fx-guia:hover{border-color:var(--fx-teal)}
.fx-faq-in{max-width:860px}.fx-faq{margin-top:14px}.fx-faq details{background:#fff;border:1px solid var(--fx-line);border-radius:12px;margin-bottom:8px;padding:0 16px}.fx-faq summary{cursor:pointer;padding:15px 0;font:700 15px var(--fx-f);list-style:none;display:flex;justify-content:space-between}.fx-faq summary::after{content:"+";color:var(--fx-teal);font-size:20px}.fx-faq details[open] summary::after{content:"–"}.fx-faq p{margin:0 0 15px;color:var(--fx-mut);line-height:1.6}
.fx-seo{background:#fff}.fx-seo p{color:var(--fx-mut);line-height:1.7;max-width:80ch}.fx-seo a{color:var(--fx-teal);font-weight:600}
.fx-pie{background:var(--fx-deep);color:#cfe9e4}.fx-pie a{color:#cfe9e4;text-decoration:none}.fx-pie a:hover{color:#fff}.fx-pie-top{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:28px;padding-block:38px}.fx-pie nav{display:flex;flex-direction:column;gap:8px;font-size:14px}.fx-pie nav b{color:#fff;font:700 14px var(--fx-f);margin-bottom:4px}
.fx-pie .fx-logo{color:#fff}.fx-pie .fx-logo b{color:var(--fx-mint)}.fx-pie .fx-logo small{color:#cfe9e4}.fx-pie-m p{font-size:14px;line-height:1.6;margin:12px 0}.fx-pie-wa{display:inline-block;background:var(--fx-amb2);color:#2a1d00!important;font-weight:800;border-radius:99px;padding:9px 16px}.fx-pie-h{display:block;font-size:13px;margin-top:8px}
.fx-pie-pago{display:flex;align-items:center;gap:14px;flex-wrap:wrap;padding-block:16px;border-top:1px solid rgba(255,255,255,.14);font-size:13px}.fx-pie-base{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;padding-block:16px;border-top:1px solid rgba(255,255,255,.14);font-size:12px}
@media (max-width:820px){.fx-pie-top{grid-template-columns:1fr 1fr}.fx-pie-m{grid-column:1/-1}}
main.wrap:empty{display:none}
.fx-todas{background:none!important;border:0!important;box-shadow:none!important;padding:0!important;margin:0!important;border-radius:0!important}.fx-todas summary::after{content:none!important}.fx-menu a{padding:10px 10px}
"""


def generar(OUT, CATALOGO, MARCAS, slug, foto, ubic, refs, modelos, guias, ciudades_top, rutas_ciudad, cabeza_php, MARCAS_INFO, info_marca):
    url = lambda p: f"/{slug(p['marca'])}/{p['slug']}/"
    desde = {m: min(p["precio"] for p in CATALOGO if p["marca"] == m) for m in MARCAS}
    por_id = {p["id"]: p for p in CATALOGO}

    def card(p, pack=False, sello=None):
        ahorro = p["precio"] * 2 - p["pack"]
        return (f'<article class="fx-card">{f"<span class=fx-sello>{esc(sello)}</span>" if sello else ""}'
                f'<a class="fx-ph" href="{url(p)}" tabindex="-1" aria-hidden="true">{foto(p, p["nombre_largo"] + " para nevecón " + p["marca"], mini=True)}</a>'
                f'<div class="fx-b"><span class="fx-m">{esc(p["marca"])} · {"Externo" if ubic(p) == "externo" else "Interno"}</span>'
                f'<h3><a href="{url(p)}">{esc(p["nombre_largo"])}</a></h3><span class="fx-ref">Ref. {esc(p["ref"])}</span>'
                + (f'<div class="fx-pr"><b>{cop(p["pack"])}</b><small>Pack de 2 · ahorras {cop(ahorro)}</small></div>' if pack else
                   f'<div class="fx-pr"><b>{cop(p["precio"])}</b><small>Envío gratis</small></div><span class="fx-pack">Pack de 2: <b>{cop(p["pack"])}</b></span>')
                + (f'<button class="fx-add" type="button" data-add="{p["id"]}" data-pack="1">Agregar el pack</button>' if pack else
                   f'<button class="fx-add" type="button" data-add="{p["id"]}">Agregar al carrito</button>')
                + '</div></article>')

    def fila(idf, cards):
        return (f'<div class="fx-fila-w"><button class="fx-fl" type="button" data-fila="{idf}" data-dir="a" aria-label="Anterior">‹</button>'
                f'<div class="fx-fila" id="{idf}">{cards}</div><button class="fx-fl" type="button" data-fila="{idf}" data-dir="s" aria-label="Siguiente">›</button></div>')

    slides = ""
    for i, m in enumerate(MARCAS):
        tit, txt, pid = BANNER[m]
        p = por_id[pid]
        h = "h1" if i == 0 else "h2"
        slides += (f'<section class="fx-sl" style="--c:{MARCAS_INFO[m]["tema"]}" aria-roledescription="diapositiva" aria-label="{esc(tit)}"><div class="fx-wrap fx-sl-in"><div>'
                   f'<span class="fx-eye">{"Filtros de agua para nevera" if i == 0 else "Tienda " + esc(m)}</span><{h}>{"Filtros para tu nevera " + esc(m) if i == 0 else esc(tit)}</{h}><p>{esc(txt)}</p>'
                   f'<span class="fx-desde"><small>Desde</small><b>{cop(desde[m])}</b></span><div><a class="fx-btn" href="/{slug(m)}/">Ver filtros {esc(m)}</a></div></div>'
                   f'<div class="fx-sl-img"><span>{foto(p, p["nombre_largo"] + " para nevecón " + p["marca"], lazy=(i > 0))}</span></div></div></section>')
    puntos = "".join(f'<button type="button" aria-label="Ir al banner de {esc(m)}"></button>' for m in MARCAS)

    circ = "".join(f'<li><a href="/{slug(m)}/"><span class="fx-c"><img src="/img/logo-{slug(m)}.png" alt="Logo {esc(m)}" width="{info_marca[m][0]}" height="{info_marca[m][1]}" loading="lazy"></span>{esc(m)}</a></li>' for m in MARCAS)
    circ += "".join(f'<li><a href="{r}"><span class="fx-c">{ICONOS[k]}</span>{t}</a></li>' for k, r, t in (
        ("interno", "/tienda/", "Filtros internos"), ("externo", "/tienda/", "Filtros externos"), ("pack", "#packs", "Packs de 2"),
        ("instalacion", "/instalacion/", "Instalación"), ("guias", "/guia/", "Guías"), ("envios", "/envios/", "Envíos")))

    populares = [por_id[i] for i in ("sam-cin-o", "lg-1000-o", "wp-1-o", "sam-qin-o", "lg-700-o", "wp-4-o", "ge-mwf-o", "sam-ex-o") if i in por_id]
    packs = [p for p in CATALOGO if ubic(p) == "interno"][:8]
    tiendas = ""
    for m in MARCAS:
        ps = [p for p in CATALOGO if p["marca"] == m]
        tiendas += (f'<section class="fx-sec" aria-labelledby="e-{slug(m)}"><div class="fx-wrap"><div class="fx-tienda" style="--c:{MARCAS_INFO[m]["tema"]}"><div class="fx-tienda-h">'
                    f'<span class="fx-lg"><img src="/img/logo-{slug(m)}.png" alt="Logo {esc(m)}" width="{info_marca[m][0]}" height="{info_marca[m][1]}" loading="lazy"></span>'
                    f'<h2 id="e-{slug(m)}">Tienda de filtros {esc(m)}</h2><a href="/{slug(m)}/">Entrar a la tienda {esc(m)}</a></div>'
                    f'<div class="fx-grid">{"".join(card(p) for p in ps)}</div></div></div></section>')
    mosaico = (f'<a class="fx-mo" style="--c:#0f5e57" href="#packs"><b>Pack anual de 2 filtros</b><span>Cambia el filtro dos veces al año y ahorra en cada pack.</span><i>Ver packs →</i>{ICONOS["pack"]}</a>'
               f'<a class="fx-mo" style="--c:#0b3b3c" href="/instalacion/"><b>Instálalo tú mismo</b><span>Internos en 2 minutos y externos en 10 a 15, con paso a paso.</span><i>Ver cómo →</i>{ICONOS["instalacion"]}</a>'
               f'<a class="fx-mo" style="--c:#7a5200" href="/envios/"><b>Envío gratis a toda Colombia</b><span>Entrega en 2 a 3 días hábiles a las principales ciudades.</span><i>Ver ciudades →</i>{ICONOS["envios"]}</a>')
    conf = "".join(f'<li>{ICONOS[k]}<div><b>{t}</b><span>{d}</span></div></li>' for k, t, d in (
        ("envios", "Envío gratis", "a toda Colombia, con número de guía"), ("pack", "Pago seguro", "tarjeta, PSE, Nequi o Bancolombia"),
        ("instalacion", "Fácil de instalar", "paso a paso en cada filtro"), ("guias", "Te asesoramos", "por WhatsApp, de lunes a sábado")))
    chips_ref = "".join(f'<a href="{r}">{esc(t)}</a>' for t, r in refs[:20])
    ciudades = "".join(f'<a href="{rutas_ciudad[c]}">{esc(c)}</a>' for c in ciudades_top if c in rutas_ciudad)
    guias_html = "".join(f'<a class="fx-guia" href="{r}"><b>{esc(t)}</b><span>Leer la guía →</span></a>' for r, t in guias[:6])
    faq_html = "".join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in FAQ)

    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Store", "@id": "__BASE__/#tienda", "name": "__NOMBRE__", "url": "__BASE__/", "image": "__BASE__/img/compartir.jpg", "logo": "__BASE__/img/icono-512.png",
         "telephone": "__TEL__", "areaServed": {"@type": "Country", "name": "Colombia"}, "priceRange": "$$"},
        {"@type": "WebSite", "@id": "__BASE__/#web", "url": "__BASE__/", "name": "__NOMBRE__", "inLanguage": "es-CO", "publisher": {"@id": "__BASE__/#tienda"}},
        {"@type": "ItemList", "name": "Filtros de agua para nevera", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"__BASE__{url(p)}", "name": p["nombre_largo"]} for i, p in enumerate(CATALOGO)]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]}
    titulo = "FiltrosNevecones | Filtros de agua para nevera, envío gratis"
    desc = "Filtros de agua para nevera Samsung, LG, Whirlpool y GE: precios, referencias y cómo instalarlos. Envío gratis a toda Colombia y pago seguro."
    cuerpo = f"""
</main><div class="fx-home">
<div id="fx-car" class="fx-car" role="region" aria-roledescription="carrusel" aria-label="Marcas destacadas">{slides}</div>
<div class="fx-pts">{puntos}</div>
<section class="fx-bur" aria-label="Categorías"><div class="fx-wrap"><ul>{circ}</ul></div></section>
<section class="fx-sec" aria-labelledby="t-vend"><div class="fx-wrap"><header class="fx-est-h"><h2 id="t-vend">Los más pedidos</h2><a class="fx-ver" href="/tienda/">Ver todos los filtros →</a></header>{fila("f-vend", "".join(card(p, sello="Más pedido") for p in populares))}</div></section>
<section class="fx-sec" aria-label="Promociones"><div class="fx-wrap fx-mos">{mosaico}</div></section>
<section class="fx-sec" id="packs" aria-labelledby="t-packs"><div class="fx-wrap"><header class="fx-est-h"><div><h2 id="t-packs">Packs anuales de 2 filtros</h2><p class="fx-sub">Un filtro cada 6 meses: llévate los dos del año con descuento.</p></div></header>{fila("f-packs", "".join(card(p, pack=True) for p in packs))}</div></section>
{tiendas}
<section class="fx-conf" aria-label="Beneficios"><div class="fx-wrap"><ul>{conf}</ul></div></section>
<section class="fx-sec" aria-labelledby="t-ref"><div class="fx-wrap"><h2 id="t-ref">Busca tu filtro por referencia</h2><p class="fx-sub">La referencia está impresa en el filtro viejo. Entra a la tuya:</p><div class="fx-refs">{chips_ref}<a href="/referencias/">Todas las referencias →</a><a href="/neveras/">Por modelo de nevera →</a></div></div></section>
<section class="fx-sec" aria-labelledby="t-env"><div class="fx-wrap"><h2 id="t-env">Enviamos a toda Colombia</h2><p class="fx-sub">Envío gratis a cualquier ciudad. Mira el tiempo de entrega a la tuya:</p><div class="fx-ciu">{ciudades}<a class="fx-mas" href="/envios/">Ver todas las ciudades →</a></div></div></section>
<section class="fx-sec" aria-labelledby="t-gu"><div class="fx-wrap"><header class="fx-est-h"><h2 id="t-gu">Guías para cuidar el agua de tu nevera</h2><a class="fx-ver" href="/guia/">Todas las guías →</a></header><div class="fx-guias">{guias_html}</div></div></section>
<section class="fx-sec" aria-labelledby="t-faq"><div class="fx-wrap fx-faq-in"><h2 id="t-faq">Preguntas frecuentes</h2><div class="fx-faq">{faq_html}</div></div></section>
<section class="fx-sec fx-seo"><div class="fx-wrap"><h2>Filtros de agua para nevera y nevecón en Colombia</h2>
<p>En FiltrosNevecones vendemos filtros de agua para neveras con dispensador de agua y hielo de las marcas Samsung, LG, Whirlpool, GE, KitchenAid, Maytag, Jenn-Air, Amana y Kenmore. Tenemos {len(CATALOGO)} referencias entre {cop(min(p["precio"] for p in CATALOGO))} y {cop(max(p["precio"] for p in CATALOGO))}, filtros internos que van dentro de la nevera y filtros externos que se conectan a la manguera del agua.</p>
<p>Cada marca tiene su propia tienda con precios, referencias equivalentes, guía de instalación y envíos a más de 120 ciudades: <a href="/samsung/">filtros Samsung</a>, <a href="/lg/">filtros LG</a>, <a href="/whirlpool/">filtros Whirlpool</a> y <a href="/ge/">filtros GE</a>. El filtro se cambia cada 6 meses para tener agua y hielo limpios.</p></div></section>
</div><script>{JS_PORTADA}</script><main>
"""
    pagina = cabeza_php("/partes.php", titulo, desc, "/", ld) + cuerpo + "<?php pie(); ?>\n"
    pagina = pagina.replace("'<script type=\"application/ld+json\">' . str_replace('__BASE__', sitio()['base'], $ld) . '</script>'",
                            "'<script type=\"application/ld+json\">' . str_replace(['__BASE__', '__NOMBRE__', '__TEL__'], [sitio()['base'], addslashes(cfg()['negocio']['nombre']), '+57' . substr(preg_replace('/\\D/', '', (string) (cfg()['whatsapp'] ?? '')), -10)], $ld) . '</script>'")
    (OUT / "index.php").write_text(pagina, encoding="utf-8")
    css = OUT / "estilo.css"
    css.write_text(css.read_text(encoding="utf-8") + CSS, encoding="utf-8")
