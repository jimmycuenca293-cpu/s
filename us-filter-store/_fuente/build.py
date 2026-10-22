#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tienda de filtros de agua para refrigeradores (EE. UU.), en inglés, estática y pensada para posicionamiento orgánico.
Uso: python3 build.py   → site/ y la-tienda-eeuu.zip
Lee config.json (dominio, WhatsApp, PayPal) y prices.csv (precios en USD). Mientras un filtro no tenga precio, la página manda al cliente a WhatsApp."""
import datetime, html, json, re, shutil, sys, zipfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from catalog import BRANDS, load, prices, slug  # noqa: E402
from guides import G  # noqa: E402

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
OUT = RAIZ / "site"
CFG = json.loads((RAIZ / "config.json").read_text(encoding="utf-8"))
DOM = CFG["domain"].rstrip("/")
NAME = CFG["store_name"]
WA = CFG["whatsapp"]
WA_DISP = CFG["whatsapp_display"]
HOY = datetime.date.today().isoformat()
e = lambda s: html.escape(str(s), quote=True)

P = load()
PR = prices()
PBY = {p["id"]: p for p in P}
PAGES = {}          # url -> (prioridad, imagen opcional)
SEARCH = []


def wa_link(text):
    from urllib.parse import quote
    return f"https://wa.me/{WA}?text={quote(text)}"


# ------------------------------------------------------------------ imágenes
def preparar_imagenes():
    d = OUT / "img" / "products"; d.mkdir(parents=True, exist_ok=True)
    for p in P:
        src = RAIZ / "fotos" / f"{p['photo']}.jpg"
        im = Image.open(src).convert("RGB")
        im.thumbnail((900, 900)); p["w"], p["h"] = im.size
        im.save(d / f"{p['id']}.jpg", quality=84, optimize=True)
        im.save(d / f"{p['id']}.webp", quality=82)
        s = im.copy(); s.thumbnail((400, 400)); p["w4"], p["h4"] = s.size
        s.save(d / f"{p['id']}-400.webp", quality=80)


def fuente(size, bold=True):
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)


def tarjeta_og(nombre, titulo, sub, fotos):
    im = Image.new("RGB", (1200, 630), (10, 59, 110))
    d = ImageDraw.Draw(im)
    for y in range(630):
        t = y / 630
        d.line([(0, y), (1200, y)], fill=(int(10 + 10 * t), int(59 + 70 * t), int(110 + 60 * t)))
    d.text((60, 70), NAME.upper(), font=fuente(26), fill=(160, 225, 245))
    y = 140
    for ln in titulo:
        d.text((60, y), ln, font=fuente(62), fill=(255, 255, 255)); y += 76
    d.text((60, y + 20), sub, font=fuente(28, False), fill=(214, 238, 248))
    x = 700
    for f in fotos[:3]:
        ph = Image.open(RAIZ / "fotos" / f"{f}.jpg").convert("RGB"); ph.thumbnail((300, 420))
        card = Image.new("RGB", (ph.width + 24, ph.height + 24), (255, 255, 255)); card.paste(ph, (12, 12))
        im.paste(card, (x, 120 + (420 - ph.height) // 2)); x += card.width + 14
        if x > 1100: break
    im.save(OUT / "img" / nombre, quality=86)


def preparar_og():
    tarjeta_og("og-home.jpg", ["Refrigerator", "Water Filters"], "Samsung · LG · Whirlpool · GE replacement filters", ["sam-cin-o", "lg-700-o", "wp-1-o"])
    for b, v in BRANDS.items():
        fo = [p["photo"] for p in P if p["brand"] == b][:3]
        tarjeta_og(f"og-{b}.jpg", [v["name"], "Water Filters"], "Replacement refrigerator filters", fo)


# ------------------------------------------------------------------ plantilla
CSS = """
:root{--ink:#0f2438;--mut:#53667a;--bg:#fff;--soft:#f2f7fb;--line:#d9e4ee;--pri:#0a5ea8;--pri2:#083f73;--acc:#12b3d3;--ok:#0f8a5f;--wa:#1fa855;--r:14px}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;font:16px/1.65 system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:var(--bg)}
img{max-width:100%;height:auto}a{color:var(--pri)}h1,h2,h3{line-height:1.2;letter-spacing:-.015em;margin:0 0 .5em;text-wrap:balance}h1{font-size:clamp(28px,4.6vw,44px);font-weight:800}h2{font-size:clamp(22px,3vw,30px);font-weight:800;margin-top:1.6em}h3{font-size:18px}
.w{max-width:1120px;margin:0 auto;padding-inline:max(16px,env(safe-area-inset-left,0px))}
.top{background:var(--pri2);color:#fff;font-size:13px}.top .w{display:flex;gap:18px;justify-content:center;flex-wrap:wrap;padding-block:7px}.top a{color:#fff}
header.h{position:sticky;top:0;z-index:40;background:#fff;border-bottom:1px solid var(--line)}header.h .w{display:flex;align-items:center;gap:18px;padding-block:10px}
.logo{display:flex;align-items:center;gap:9px;text-decoration:none;color:var(--ink);font-weight:800;font-size:19px;letter-spacing:-.02em}.logo svg{width:30px;height:30px}
.srch{flex:1;max-width:420px;display:flex}.srch input{flex:1;min-width:0;padding:10px 14px;border:1px solid var(--line);border-radius:999px 0 0 999px;font:inherit}.srch button{padding:0 16px;border:0;background:var(--pri);color:#fff;border-radius:0 999px 999px 0;font-weight:700;cursor:pointer}
nav.m{display:flex;gap:16px;flex-wrap:wrap}nav.m a{color:var(--ink);text-decoration:none;font-weight:600;font-size:14px}nav.m a:hover{color:var(--pri)}
@media(max-width:600px){.top span:not(:last-child){display:none}}
@media(max-width:900px){header.h .w{flex-wrap:wrap}.srch{order:3;max-width:none;flex-basis:100%}nav.m{gap:12px}}
.hero{background:linear-gradient(135deg,#06335f 0%,#0a5ea8 60%,#0e86b8 100%);color:#fff;padding-block:56px}.hero .w{display:grid;grid-template-columns:1.2fr .8fr;gap:32px;align-items:center}.hero h1{color:#fff}.hero p{font-size:18px;opacity:.95;max-width:58ch}
.hero.s{padding-block:34px}.hero.s .w{grid-template-columns:1fr}
.hero .photos{display:flex;gap:12px;justify-content:flex-end}.hero .photos span{background:#fff;border-radius:12px;padding:10px;height:230px;display:grid;place-items:center;width:30%}.hero .photos img{max-height:210px;width:auto}
@media(max-width:860px){.hero .w{grid-template-columns:1fr}.hero .photos{justify-content:flex-start}}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:12px 22px;border-radius:999px;border:2px solid var(--pri);background:var(--pri);color:#fff;font-weight:700;text-decoration:none;cursor:pointer;font:inherit;font-weight:700}.btn.wa{background:var(--wa);border-color:var(--wa)}.btn.sec{background:transparent;color:#fff;border-color:#fff}.btn.out{background:#fff;color:var(--pri)}
.big{padding:14px 28px;font-size:17px}
.sec{padding-block:44px}.sec.alt{background:var(--soft)}.cab{max-width:760px;margin-bottom:22px}.cab p{color:var(--mut)}
.grid{display:grid;gap:18px}.g4{grid-template-columns:repeat(4,1fr)}.g3{grid-template-columns:repeat(3,1fr)}.g2{grid-template-columns:repeat(2,1fr)}@media(max-width:960px){.g4{grid-template-columns:1fr 1fr}.g3{grid-template-columns:1fr 1fr}}@media(max-width:600px){.g4,.g3,.g2{grid-template-columns:1fr}}
.card{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:16px;display:flex;flex-direction:column;gap:8px;text-decoration:none;color:var(--ink)}a.card:hover{border-color:var(--pri);transform:translateY(-2px);transition:.15s}
.card .im{height:170px;display:grid;place-items:center;background:#fff}.card .im img{max-height:160px;width:auto}.card h3{margin:0;font-size:16px}.card .pr{font-weight:800;color:var(--pri)}.card p{margin:0;color:var(--mut);font-size:14px}
.tag{display:inline-block;font-size:12px;font-weight:700;background:var(--soft);color:var(--pri2);padding:3px 10px;border-radius:999px}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0}.chips a{padding:7px 13px;border:1px solid var(--line);border-radius:999px;background:#fff;text-decoration:none;color:var(--ink);font-size:14px;font-weight:600}.chips a:hover{border-color:var(--pri);color:var(--pri)}
.crumb{font-size:14px;color:var(--mut);padding-block:14px}.crumb a{color:var(--mut)}
.prod{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:36px;align-items:start}@media(max-width:860px){.prod{grid-template-columns:1fr}}
.foto{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:24px;display:grid;place-items:center}.foto img{max-height:480px;width:auto}
.buy{border:2px solid var(--line);border-radius:var(--r);padding:18px;margin:16px 0;background:#fff}.buy .price{font-size:30px;font-weight:800;color:var(--ink)}.buy .price small{font-size:14px;color:var(--mut);font-weight:600}
.buy label{font-size:14px;font-weight:700;display:block;margin:10px 0 4px}.buy select{padding:9px 12px;border:1px solid var(--line);border-radius:8px;font:inherit;min-width:150px}
.pp{margin-top:12px;min-height:44px}.note{font-size:13px;color:var(--mut)}
.ok{list-style:none;padding:0;margin:12px 0;display:grid;gap:6px}.ok li::before{content:"✓";color:var(--ok);font-weight:800;margin-right:8px}
table.t{border-collapse:collapse;width:100%;font-size:15px}table.t th,table.t td{padding:10px 12px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}table.t th{background:var(--soft);font-size:13px;text-transform:uppercase;letter-spacing:.05em}.tw{overflow-x:auto;border:1px solid var(--line);border-radius:12px}
.txt{max-width:820px}.txt p,.txt li{color:#233b52}.lead{font-size:18px;color:var(--mut)}
details{border:1px solid var(--line);border-radius:12px;padding:12px 16px;margin:10px 0;background:#fff}summary{font-weight:700;cursor:pointer}details p{margin:10px 0 0;color:#2f4558}
ol.steps{padding-left:22px}ol.steps li{margin:8px 0}
.trust{background:var(--soft);border-block:1px solid var(--line)}.trust .w{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;padding-block:16px}.trust b{display:block}.trust small{color:var(--mut)}@media(max-width:760px){.trust .w{grid-template-columns:1fr 1fr}}
footer.f{background:#06233f;color:#d7e6f3;padding-block:40px;margin-top:40px}footer.f a{color:#d7e6f3;text-decoration:none}footer.f a:hover{text-decoration:underline}.cols{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:28px}.cols b{display:block;color:#fff;margin-bottom:8px}.cols a{display:block;padding:3px 0;font-size:14px}@media(max-width:860px){.cols{grid-template-columns:1fr 1fr}}@media(max-width:520px){.cols{grid-template-columns:1fr}}
.legal{border-top:1px solid rgba(255,255,255,.15);margin-top:26px;padding-top:16px;font-size:12px;opacity:.85}
.wa-f{position:fixed;right:14px;bottom:calc(14px + env(safe-area-inset-bottom,0px));z-index:60;display:flex;align-items:center;gap:8px;background:#25d366;color:#fff!important;border-radius:999px;padding:12px 18px;font-weight:800;text-decoration:none;box-shadow:0 8px 22px rgba(0,0,0,.25)}.wa-f svg{width:26px;height:26px}@media(max-width:520px){.wa-f span{display:none}.wa-f{padding:14px}}
.resbox{display:grid;gap:10px}.resbox a{display:block;padding:12px 14px;border:1px solid var(--line);border-radius:10px;text-decoration:none;color:var(--ink);background:#fff}.resbox a small{display:block;color:var(--mut)}
"""

JS = r"""
(function(){
var S=window.STORE||{};window.dataLayer=window.dataLayer||[];
document.addEventListener('click',function(ev){var a=ev.target.closest('a[href*="wa.me/"]');if(a){dataLayer.push({event:'whatsapp',button:(a.textContent||'').trim().slice(0,60),page:location.pathname})}},true);
function money(n){return '$'+n.toFixed(2)}
/* precios: el HTML ya trae el precio; /assets/prices.json lo puede cambiar sin volver a generar el sitio */
function boot(prices){
 document.querySelectorAll('.buy').forEach(function(box){
  var sku=box.dataset.sku,pr=(prices&&prices[sku])||{},price=pr.price!=null?pr.price:parseFloat(box.dataset.price||'0')||0,pack=pr.pack!=null?pr.pack:parseFloat(box.dataset.pack||'0')||0,ship=parseFloat(S.shipping||0)||0;
  var name=box.dataset.name,sel=box.querySelector('select.q'),out=box.querySelector('.price'),pp=box.querySelector('.pp'),pay=box.querySelector('.paywrap');
  if(!price){if(pay)pay.hidden=true;return}
  function qtyInfo(){var v=sel?sel.value:'1',n=parseInt(v,10)||1,unit=price;if(v==='pack'){n=2;unit=pack/2}return {n:n,unit:unit,total:(v==='pack')?pack:price*n}}
  function paint(){var q=qtyInfo();if(out)out.innerHTML=money(q.total)+' <small>USD'+(ship?' + '+money(ship)+' shipping':'')+'</small>'}
  paint();if(sel)sel.addEventListener('change',function(){paint();render()});
  var rendered=false;function render(){
   if(!S.paypalClientId||!window.paypal){return}
   pp.innerHTML='';var q=qtyInfo();var items=(q.total).toFixed(2);
   paypal.Buttons({style:{layout:'vertical',shape:'pill',label:'paypal'},
    createOrder:function(d,a){var q=qtyInfo(),it=q.total.toFixed(2);return a.order.create({purchase_units:[{description:name+' x'+q.n,custom_id:sku+'|'+q.n,amount:{currency_code:'USD',value:(q.total+ship).toFixed(2),breakdown:{item_total:{currency_code:'USD',value:it},shipping:{currency_code:'USD',value:ship.toFixed(2)}}},items:[{name:name,sku:sku,unit_amount:{currency_code:'USD',value:q.unit.toFixed(2)},quantity:String(q.n)}]}],application_context:{shipping_preference:'GET_FROM_FILE'}})},
    onApprove:function(d,a){return a.order.capture().then(function(){dataLayer.push({event:'purchase_paypal',sku:sku});location.href='/thank-you/'})}}).render(pp)}
  if(S.paypalClientId){var s=document.createElement('script');s.src='https://www.paypal.com/sdk/js?client-id='+encodeURIComponent(S.paypalClientId)+'&currency=USD&components=buttons&enable-funding=card';s.onload=render;document.head.appendChild(s)}
  else if(!box.dataset.link){pp.innerHTML='<p class="note">Online checkout with PayPal is coming soon. To order now, message us on WhatsApp.</p>'}
 });
}
fetch('/assets/prices.json').then(function(r){return r.ok?r.json():{}}).catch(function(){return {}}).then(boot);
/* buscador de filtros */
var box=document.getElementById('finder-q'),res=document.getElementById('finder-res');
if(box&&res){fetch('/assets/search.json').then(function(r){return r.json()}).then(function(ix){
 function norm(s){return s.toLowerCase().replace(/[^a-z0-9]+/g,'')}
 function run(){var q=norm(box.value);res.innerHTML='';if(q.length<2)return;var n=0;
  ix.forEach(function(it){if(n>=40)return;if(norm(it[0]+' '+it[2]).indexOf(q)>-1){n++;res.insertAdjacentHTML('beforeend','<a href="'+it[1]+'">'+it[0]+'<small>'+it[3]+'</small></a>')}});
  if(!n)res.innerHTML='<p>No match yet. Send us your refrigerator model number or a photo of the old filter on <a href="'+S.waLink+'">WhatsApp</a>.</p>'}
 box.addEventListener('input',run);var u=new URLSearchParams(location.search).get('q');if(u){box.value=u;run()}})}
})();
"""

ICON = '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 3c4 6 8 10 8 15a8 8 0 0 1-16 0c0-5 4-9 8-15z" fill="#12b3d3"/><path d="M16 9c2.4 3.6 5 6.2 5 9.2a5 5 0 0 1-10 0c0-3 2.6-5.6 5-9.2z" fill="#0a5ea8"/></svg>'
WA_ICON = '<svg viewBox="0 0 32 32" aria-hidden="true"><path fill="#fff" d="M16 3a13 13 0 0 0-11 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 2.4a10.6 10.6 0 1 1-5.4 19.7l-.4-.2-3.9 1 1-3.8-.3-.4A10.6 10.6 0 0 1 16 5.4zm-4 5.2c-.3 0-.7.1-1 .5-.4.4-1.4 1.4-1.4 3.3s1.4 3.8 1.6 4.1c.2.3 2.8 4.3 6.8 5.9 3.3 1.3 4 1 4.7.9.7-.1 2.3-.9 2.6-1.8.3-.9.3-1.7.2-1.8-.1-.2-.4-.3-.8-.5s-2.3-1.1-2.6-1.3c-.4-.1-.6-.2-.9.2-.3.4-1 1.3-1.2 1.5-.2.3-.4.3-.8.1-.4-.2-1.6-.6-3-1.9-1.1-1-1.9-2.3-2.1-2.7-.2-.4 0-.6.2-.8l.6-.7c.2-.2.3-.4.4-.7.1-.3.1-.5 0-.7l-1.2-2.9c-.3-.7-.6-.7-.9-.7z"/></svg>'


def ld_script(items):
    return "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in items)


def org_ld():
    return {"@context": "https://schema.org", "@type": "Organization", "@id": DOM + "/#org", "name": NAME, "url": DOM + "/", "logo": DOM + "/img/logo.svg",
            "contactPoint": {"@type": "ContactPoint", "telephone": "+" + WA, "contactType": "customer service", "availableLanguage": ["English", "Spanish"]}}


def trim(t, n):
    t = " ".join(t.split())
    return t if len(t) <= n else t[:n - 1].rsplit(" ", 1)[0].rstrip(",;:.") + "…"


def page(path, title, desc, body, ld=None, og="og-home.jpg", noindex=False, prioridad="0.6", hero_cls=""):
    canon = DOM + path
    if len(title) > 62 and title.endswith(" | " + NAME): title = title[: -len(" | " + NAME)]
    if len(title) > 66: title = title[:66].rsplit(" ", 1)[0].rstrip(",;:.-|")
    desc = trim(desc, 158)
    head = (f'<!DOCTYPE html><html lang="en-US"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{e(title)}</title><meta name="description" content="{e(desc)}">'
            f'<meta name="robots" content="{"noindex,follow" if noindex else "index,follow,max-image-preview:large,max-snippet:-1"}">'
            f'<link rel="canonical" href="{canon}"><link rel="alternate" hreflang="en-us" href="{canon}"><link rel="alternate" hreflang="x-default" href="{canon}">'
            f'<meta property="og:type" content="website"><meta property="og:site_name" content="{e(NAME)}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">'
            f'<meta property="og:url" content="{canon}"><meta property="og:image" content="{DOM}/img/{og}" ><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:locale" content="en_US">'
            f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{DOM}/img/{og}">'
            f'<meta name="theme-color" content="#0a5ea8"><link rel="icon" href="/img/logo.svg" type="image/svg+xml">'
            + (f'<meta name="google-site-verification" content="{e(CFG["gsc_verification"])}">' if CFG.get("gsc_verification") else "")
            + '<link rel="stylesheet" href="/assets/site.css">' + ld_script(ld or []) + _analytics() + "</head><body>")
    nav = ('<nav class="m" aria-label="Main"><a href="/refrigerator-water-filters/">All filters</a><a href="/samsung-refrigerator-water-filters/">Samsung</a><a href="/lg-refrigerator-water-filters/">LG</a>'
           '<a href="/whirlpool-refrigerator-water-filters/">Whirlpool</a><a href="/ge-refrigerator-water-filters/">GE</a><a href="/guides/">Guides</a><a href="/part-numbers/">Part numbers</a></nav>')
    top = f'<div class="top"><div class="w"><span>Free delivery to your door</span><span>Ships from our U.S. warehouse</span><span>Secure checkout with PayPal</span><span>Questions? WhatsApp <a href="{wa_link("Hi! I have a question about a refrigerator water filter.")}">{WA_DISP}</a></span></div></div>'
    header = (f'<header class="h"><div class="w"><a class="logo" href="/">{ICON}<span>{e(NAME)}</span></a>'
              f'<form class="srch" action="/finder/" role="search"><input type="search" name="q" placeholder="Search model or part number" aria-label="Search by refrigerator model or filter part number"><button type="submit">Search</button></form>{nav}</div></header>')
    foot = (f'<footer class="f"><div class="w"><div class="cols"><div><b>{e(NAME)}</b><p>Replacement refrigerator water filters for Samsung, LG, Whirlpool and GE refrigerators. Orders ship from our U.S. warehouse.</p>'
            f'<p>WhatsApp: <a href="{wa_link("Hi! I have a question about a refrigerator water filter.")}">{WA_DISP}</a>' + (f'<br>Email: <a href="mailto:{e(CFG["email"])}">{e(CFG["email"])}</a>' if CFG.get("email") else "") + '</p></div>'
            '<div><b>Shop</b><a href="/refrigerator-water-filters/">All refrigerator water filters</a><a href="/samsung-refrigerator-water-filters/">Samsung filters</a><a href="/lg-refrigerator-water-filters/">LG filters</a><a href="/whirlpool-refrigerator-water-filters/">Whirlpool filters</a><a href="/ge-refrigerator-water-filters/">GE filters</a><a href="/external-inline-refrigerator-water-filters/">External inline filters</a></div>'
            '<div><b>Help</b><a href="/finder/">Find my filter</a><a href="/part-numbers/">Part number cross-reference</a><a href="/guides/">Guides</a><a href="/faq/">FAQ</a><a href="/contact/">Contact</a></div>'
            '<div><b>Company</b><a href="/about/">About</a><a href="/shipping-returns/">Shipping &amp; returns</a><a href="/privacy-policy/">Privacy policy</a><a href="/terms/">Terms</a><a href="/disclaimer/">Brand disclaimer</a></div></div>'
            f'<p class="legal">© {datetime.date.today().year} {e(NAME)}. Samsung, LG, Whirlpool, GE and all other brand names are trademarks of their respective owners and are used only to identify the refrigerator models and part numbers our filters fit. We are not affiliated with, endorsed by or sponsored by those brands.</p></div></footer>')
    wa_f = f'<a class="wa-f" href="{wa_link("Hi! I need help finding the right refrigerator water filter.")}" target="_blank" rel="noopener">{WA_ICON}<span>WhatsApp us</span></a>'
    cfgjs = "window.STORE=" + json.dumps({"paypalClientId": CFG.get("paypal_client_id", ""), "shipping": CFG.get("shipping_flat_usd", 0), "waLink": wa_link("Hi! I need help finding the right refrigerator water filter.")}) + ";"
    html_ = head + top + header + "<main>" + body + "</main>" + foot + wa_f + f"<script>{cfgjs}</script><script src=\"/assets/store.js\" defer></script></body></html>"
    f = OUT / path.strip("/") / "index.html" if path != "/" else OUT / "index.html"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(html_, encoding="utf-8")
    if not noindex:
        PAGES[path] = prioridad


def _analytics():
    g = CFG.get("ga4_id")
    return (f'<script async src="https://www.googletagmanager.com/gtag/js?id={e(g)}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","{e(g)}");</script>') if g else ""


def crumb(*items):
    out = '<nav class="crumb w" aria-label="Breadcrumb"><a href="/">Home</a>'
    for t, u in items:
        out += " › " + (f'<a href="{u}">{e(t)}</a>' if u else f"<span>{e(t)}</span>")
    return out + "</nav>"


def crumb_ld(*items):
    li = [{"@type": "ListItem", "position": 1, "name": "Home", "item": DOM + "/"}]
    for i, (t, u) in enumerate(items, 2):
        d = {"@type": "ListItem", "position": i, "name": t}
        if u: d["item"] = DOM + u
        li.append(d)
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": li}


def faq_ld(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}


def faq_html(faq):
    return "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faq)


def pic(p, alt, big=False, lazy=True):
    s = "" if big else "-400"
    w, h = (p["w"], p["h"]) if big else (p["w4"], p["h4"])
    return (f'<picture><source srcset="/img/products/{p["id"]}{s}.webp" type="image/webp"><img src="/img/products/{p["id"]}.jpg" alt="{e(alt)}" width="{w}" height="{h}" '
            f'{"loading=lazy" if lazy else "fetchpriority=high"} decoding="async"></picture>')


def alt_of(p):
    return f"{p['title']} (also {p['also'].split(',')[0].strip()})" if p["also"] else p["title"]


def price_of(p):
    return PR.get(p["id"], {}).get("price")


def price_line(p):
    pr = price_of(p)
    return f'<span class="pr">${pr:,.2f}</span>' if pr else '<span class="pr">Message us for price</span>'


def card(p):
    return (f'<a class="card" href="/filters/{p["slug"]}/"><span class="tag">{e(p["brand_name"])} · {"External" if p["kind"] == "external" else "Internal"}</span><span class="im">{pic(p, alt_of(p))}</span>'
            f'<h3>{e(p["title"])}</h3>{price_line(p)}<p>Part no. {e(p["ref"])}</p></a>')


def parts_of(p):
    return [a for a in p["aliases"] if slug(a) and slug(a) != slug(p["ref"])]


def part_url(a):
    return f"/part-numbers/{slug(a)}/"


def model_url(m, p):
    return f"/refrigerator-models/{slug(p['brand_name'] + ' ' + m)}/"


STEPS_INT = ["Find the old filter in your refrigerator (usually inside the fresh-food compartment or in the base grille) and open the cover if there is one.",
             "Turn the old filter counterclockwise, or press the release button, and pull it straight out.",
             "Remove the protective cap from the new filter and check that the O-rings are in place.",
             "Insert the new filter and turn it clockwise until it locks.",
             "Reset the filter indicator light and run water through the dispenser to flush the new filter (see your manual for the amount)."]
STEPS_EXT = ["Turn off the water supply to the refrigerator and relieve the pressure by running the dispenser for a moment.",
             "Mount the filter on the water line, following the arrow that shows the direction of water flow.",
             "Connect the tubing to the inlet and outlet fittings and make sure they are fully seated.",
             "Turn the water back on slowly and check every connection for leaks.",
             "Flush the filter by running water through the dispenser until it runs clear and steady."]


def buy_box(p):
    pr = PR.get(p["id"], {}); price = pr.get("price"); pack = pr.get("pack")
    msg = f"Hi! I'd like to order the {p['title']} (part {p['ref']}). My refrigerator model is: "
    wa = f'<a class="btn wa big" href="{wa_link(msg)}" target="_blank" rel="noopener">{WA_ICON.replace("<svg ", "<svg width=22 height=22 ")} Order or ask on WhatsApp</a>'
    em = (f'<a class="btn out" href="mailto:{e(CFG["email"])}?subject={e("Order: " + p["title"])}">Email us</a>' if CFG.get("email") else "")
    if price:
        opts = "".join(f'<option value="{n}">{n} filter{"s" if n > 1 else ""}</option>' for n in range(1, 7))
        if pack: opts += f'<option value="pack">2-pack (best value)</option>'
        paywrap = (f'<div class="paywrap"><label for="q-{p["id"]}">Quantity</label><select class="q" id="q-{p["id"]}">{opts}</select><div class="pp" aria-label="PayPal checkout"></div>'
                   + (('<p class="links" style="display:flex;gap:10px;flex-wrap:wrap;margin:10px 0 0">'
                       + (f'<a class="btn big" href="{e(pr["link"])}" target="_blank" rel="noopener">Pay with PayPal: 1 filter</a>' if pr.get("link") else "")
                       + (f'<a class="btn big out" href="{e(pr["link_pack"])}" target="_blank" rel="noopener">Pay with PayPal: 2-pack</a>' if pr.get("link_pack") else "") + "</p>") if (pr.get("link") or pr.get("link_pack")) else "")
                   + '<p class="note">Pay securely with PayPal or a credit/debit card. Your shipping address is collected at checkout.</p></div>')
        head = '<div class="price">$0.00</div>'
    else:
        paywrap = '<div class="paywrap" hidden></div>'
        head = '<div class="price">Message us for price</div><p class="note">We will reply with the price and delivery details for your address.</p>'
    return (f'<div class="buy" data-sku="{p["id"]}" data-name="{e(p["title"])}" data-price="{price or ""}" data-pack="{pack or ""}" data-link="{"1" if (pr.get("link") or pr.get("link_pack")) else ""}">{head}{paywrap}<p style="display:flex;gap:10px;flex-wrap:wrap;margin:12px 0 0">{wa}{em}</p></div>')


def product_pages():
    for p in P:
        url = f"/filters/{p['slug']}/"
        kind_txt = ("an internal refrigerator water filter cartridge that sits in your refrigerator's filter housing and filters the water for the dispenser and the ice maker" if p["kind"] == "internal"
                    else "an external inline water filter that connects to the water line outside the refrigerator and filters the water that feeds the dispenser and the ice maker")
        models = p["models"]
        mlinks = "".join(f'<a href="{model_url(m, p)}">{e(m)}</a>' for m in models)
        plinks = "".join(f'<a href="{part_url(a)}">{e(a)}</a>' for a in parts_of(p))
        steps = STEPS_INT if p["kind"] == "internal" else STEPS_EXT
        guides_ = [x for x in G if x["slug"] in ("how-often-to-change-a-refrigerator-water-filter", "how-to-find-your-refrigerator-model-number", "how-to-change-a-refrigerator-water-filter", "reset-refrigerator-water-filter-light", f"{p['brand']}-refrigerator-water-filter-guide")]
        faq = [(f"Does the {p['short']} ({p['ref']}) fit my refrigerator?", (f"It is listed for models such as {', '.join(models[:6])}. " if models else "") + "Always confirm with the model number on the label inside your refrigerator or the part number printed on your old filter. If you are not sure, send us a photo on WhatsApp and we will check before you order."),
               (f"What other part numbers is the {p['ref']} also known as?", f"It is also listed as {p['also']}. If your old filter or manual shows one of these numbers, this is the replacement."),
               ("How often should I replace it?", "Most manufacturers recommend replacing a refrigerator water filter about every six months, or sooner if the water flow slows or the taste changes."),
               ("How do I install it?", " ".join(f"{i}. {s}" for i, s in enumerate(steps, 1))),
               ("Do you ship from the United States?", "Yes. Orders ship from our U.S. warehouse and we send tracking information when your order ships.")]
        also_p = [q for q in P if q["brand"] == p["brand"] and q is not p][:4] + [q for q in P if q["kind"] == p["kind"] and q["brand"] != p["brand"]][:2]
        body = (crumb((p["brand_name"] + " filters", f"/{p['brand']}-refrigerator-water-filters/"), (p["short"], None))
                + f'<div class="w"><div class="prod"><div class="foto">{pic(p, alt_of(p), True, False)}</div><div><span class="tag">{e(p["brand_name"])} · {"External inline" if p["kind"] == "external" else "Internal cartridge"}</span>'
                f'<h1>{e(p["title"])}</h1><p class="lead">Replacement for the {e(p["short"])} ({e(p["ref"])}). Also listed as {e(p["also"])}.</p>{buy_box(p)}'
                '<ul class="ok"><li>Delivered to your door from our U.S. warehouse, with tracking</li><li>Secure checkout with PayPal (USD)</li><li>We help you confirm the fit before you order</li></ul></div></div>'
                f'<div class="txt"><h2>About the {e(p["short"])} ({e(p["ref"])})</h2><p>The {e(p["title"])} is {kind_txt}. It is a replacement for the {e(p["short"])}, part number {e(p["ref"])}.</p>'
                + (f'<p>{e(p["note"])}</p>' if p["note"] else "")
                + f'<p>Replace your refrigerator water filter about every six months, or sooner if the water flow slows down or the taste changes.</p>'
                + (f'<h2>Refrigerator models this filter fits</h2><p>Models in our compatibility list include:</p><div class="chips">{mlinks}</div><p class="note">Fit depends on your exact model. Check the label inside your refrigerator or message us.</p>' if models else
                   '<h2>Is this the right filter for your refrigerator?</h2><p>Send us your refrigerator model number or a photo of the old filter on WhatsApp and we will confirm it fits before you order.</p>')
                + (f'<h2>Also searched as</h2><p>People also search for this filter as:</p><div class="chips">{plinks}</div>' if plinks else "")
                + f'<h2>How to replace it</h2><ol class="steps">{"".join(f"<li>{e(s)}</li>" for s in steps)}</ol><p>After installing, reset the filter light: <a href="/guides/reset-refrigerator-water-filter-light/">how to reset the water filter light</a>.</p>'
                f'<h2>Frequently asked questions</h2>{faq_html(faq)}'
                f'<h2>Helpful guides</h2><div class="chips">{"".join(f"<a href=\"/guides/{x[chr(115)+chr(108)+chr(117)+chr(103)]}/\">{e(x[chr(104)+chr(49)])}</a>" for x in guides_)}</div></div>'
                f'<h2>More refrigerator water filters</h2><div class="grid g3">{"".join(card(q) for q in also_p)}</div></div>')
        offers = None
        pr = price_of(p)
        prod = {"@context": "https://schema.org", "@type": "Product", "name": p["title"], "description": f"Replacement for the {p['short']} ({p['ref']}) refrigerator water filter.",
                "image": [f"{DOM}/img/products/{p['id']}.jpg"], "sku": p["id"], "mpn": p["ref"], "category": "Refrigerator Water Filters",
                "isAccessoryOrSparePartFor": {"@type": "Product", "name": f"{p['brand_name']} refrigerators"}, "alternateName": [x.strip() for x in p["also"].split(",")]}
        if pr:
            prod["offers"] = {"@type": "Offer", "url": DOM + url, "priceCurrency": "USD", "price": f"{pr:.2f}", "availability": "https://schema.org/InStock" if PR[p["id"]].get("stock", True) else "https://schema.org/OutOfStock",
                              "itemCondition": "https://schema.org/NewCondition", "seller": {"@type": "Organization", "name": NAME}, "shippingDetails": {"@type": "OfferShippingDetails", "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "US"}}}
        page(url, f"{p['title']} | {NAME}", f"Buy the {p['short']} ({p['ref']}) refrigerator water filter replacement. Also listed as {p['also']}. Ships from our U.S. warehouse. Pay with PayPal.", body,
             [prod, crumb_ld((p["brand_name"] + " filters", f"/{p['brand']}-refrigerator-water-filters/"), (p["short"], None)), faq_ld(faq)], og=f"og-{p['brand']}.jpg", prioridad="0.9")
        SEARCH.append([p["title"], url, " ".join([p["ref"], p["also"], p["line"], p["short"]] + models), f"{p['brand_name']} filter · {p['ref']}"])


def part_pages():
    amap = {}
    for p in P:
        for a in parts_of(p):
            amap.setdefault(slug(a), (a, []))[1].append(p)
    for s, (a, ps) in amap.items():
        p = ps[0]; url = part_url(a)
        faq = [(f"Is {a} the same as {p['ref']}?", f"{a} is a part or cross-reference number listed for the {p['short']} (main part number {p['ref']}). Always confirm with the model number inside your refrigerator."),
               (f"What refrigerator water filter replaces {a}?", f"Our {p['title']} is the replacement we carry for {a}."),
               ("How often should I replace it?", "About every six months, or sooner if water flow slows or taste changes.")]
        body = (crumb(("Part numbers", "/part-numbers/"), (a, None))
                + f'<div class="w"><div class="prod"><div class="foto">{pic(p, alt_of(p), True, False)}</div><div><span class="tag">{e(p["brand_name"])}</span><h1>{e(a)} Refrigerator Water Filter Replacement</h1>'
                f'<p class="lead">Looking for a replacement for {e(a)}? The {e(p["short"])} ({e(p["ref"])}) is the filter we carry for this part number.</p>{buy_box(p)}</div></div>'
                f'<div class="txt"><h2>{e(a)} replacement: what you need to know</h2><p>{e(a)} is a number you may find on your old filter, in your refrigerator manual or in a parts listing. In our catalog it is associated with the {e(p["title"])}, whose main part number is {e(p["ref"])}.</p>'
                f'<p>This filter is also known as {e(p["also"])}.</p>'
                + (f'<h2>Refrigerator models</h2><div class="chips">{"".join(f"<a href=\"{model_url(m, p)}\">{e(m)}</a>" for m in p["models"])}</div>' if p["models"] else "")
                + f'<h2>Not sure it matches?</h2><p>Part numbers can be confusing because the same filter is sold under several numbers. Send us your refrigerator model number or a photo of the old filter on WhatsApp and we will confirm it before you order.</p>'
                f'<h2>Frequently asked questions</h2>{faq_html(faq)}<p><a href="/filters/{p["slug"]}/">View the full {e(p["short"])} page</a> · <a href="/part-numbers/">All part numbers</a></p></div></div>')
        page(url, f"{a} Refrigerator Water Filter Replacement | {NAME}", f"Replacement refrigerator water filter for {a}: the {p['short']} ({p['ref']}). Check fit by model number. Ships from our U.S. warehouse.", body,
             [crumb_ld(("Part numbers", "/part-numbers/"), (a, None)), faq_ld(faq)], og=f"og-{p['brand']}.jpg", prioridad="0.7")
        SEARCH.append([f"{a} water filter", url, f"{a} {p['ref']} {p['short']}", f"Part number · replaces {p['ref']}"])
    # índice de números de parte
    rows = ""
    for p in P:
        rows += f'<tr><td><a href="/filters/{p["slug"]}/">{e(p["ref"])}</a></td><td>{e(p["brand_name"])}</td><td><a href="/filters/{p["slug"]}/">{e(p["title"])}</a></td><td>{", ".join(f"<a href=\"{part_url(a)}\">{e(a)}</a>" for a in parts_of(p))}</td></tr>'
    body = (crumb(("Part numbers", None)) + f'<div class="w txt"><h1>Refrigerator Water Filter Part Number Cross-Reference</h1><p class="lead">Find the right replacement by part number. Many filters are sold under several numbers: look for yours in the last column.</p></div>'
            f'<div class="w"><div class="tw"><table class="t"><thead><tr><th>Main part no.</th><th>Brand</th><th>Filter</th><th>Also listed as</th></tr></thead><tbody>{rows}</tbody></table></div>'
            '<p class="note">Always confirm fit with the model number inside your refrigerator. Brand names are used only to identify compatibility.</p></div>')
    page("/part-numbers/", f"Refrigerator Water Filter Part Number Cross-Reference | {NAME}", "Cross-reference of Samsung, LG, Whirlpool and GE refrigerator water filter part numbers: find the replacement for your old filter.", body, [crumb_ld(("Part numbers", None))], prioridad="0.8")


def model_pages():
    seen = set()
    for p in P:
        for m in p["models"]:
            url = model_url(m, p)
            if url in seen: continue
            seen.add(url)
            b = BRANDS[p["brand"]]
            title = f"{p['brand_name']} {m} Water Filter Replacement ({p['ref']})"
            faq = [(f"What water filter does the {p['brand_name']} {m} use?", f"Our compatibility list shows the {p['short']} ({p['ref']}) for the {p['brand_name']} {m}. Confirm with the label inside your refrigerator or your manual."),
                   (f"How often should I change the {m} water filter?", "About every six months, or sooner if water flow slows or taste changes."),
                   (f"How do I reset the filter light on the {p['brand_name']} {m}?", b["reset"] + " Check your manual for the exact procedure for your model.")]
            body = (crumb((p["brand_name"] + " filters", f"/{p['brand']}-refrigerator-water-filters/"), (m, None))
                    + f'<div class="w"><div class="prod"><div class="foto">{pic(p, alt_of(p), True, False)}</div><div><span class="tag">{e(p["brand_name"])} {e(m)}</span><h1>{e(title)}</h1>'
                    f'<p class="lead">The {e(p["short"])} ({e(p["ref"])}) is the replacement water filter listed for the {e(p["brand_name"])} {e(m)} refrigerator.</p>{buy_box(p)}</div></div>'
                    f'<div class="txt"><h2>Which water filter fits the {e(p["brand_name"])} {e(m)}?</h2><p>According to our compatibility list, the {e(p["brand_name"])} {e(m)} uses the {e(p["title"])}. It is also known as {e(p["also"])}.</p>'
                    '<p class="note">Models can have revisions. Check the model number on the label inside your refrigerator, or message us a photo before you order.</p>'
                    f'<h2>How to change the {e(m)} water filter</h2><ol class="steps">{"".join(f"<li>{e(s)}</li>" for s in STEPS_INT)}</ol>'
                    f'<h2>Reset the filter light</h2><p>{e(b["reset"])} Your manual has the exact steps for your model.</p><h2>FAQ</h2>{faq_html(faq)}'
                    f'<p><a href="/filters/{p["slug"]}/">Full details for the {e(p["short"])}</a> · <a href="/{p["brand"]}-refrigerator-water-filters/">All {e(p["brand_name"])} filters</a></p></div></div>')
            page(url, f"{title} | {NAME}", f"Which water filter fits the {p['brand_name']} {m}? The {p['short']} ({p['ref']}). Replacement filter, fit check by model number. Ships from our U.S. warehouse.", body,
                 [crumb_ld((p["brand_name"] + " filters", f"/{p['brand']}-refrigerator-water-filters/"), (m, None)), faq_ld(faq)], og=f"og-{p['brand']}.jpg", prioridad="0.7")
            SEARCH.append([f"{p['brand_name']} {m} water filter", url, f"{m} {p['ref']} {p['short']}", f"Model · uses {p['ref']}"])


def collection_pages():
    for b, v in BRANDS.items():
        ps = [p for p in P if p["brand"] == b]
        models = [(m, p) for p in ps for m in p["models"]]
        guide = next(x for x in G if x["slug"] == f"{b}-refrigerator-water-filter-guide")
        faq = [(f"How do I know which {v['name']} water filter I need?", f"Use the model number on the label inside the refrigerator or the part number on your old filter, and compare it with the list on this page. If you are unsure, message us a photo."),
               (f"How often should I replace a {v['name']} refrigerator water filter?", "About every six months, or sooner if the water flow slows or the taste changes."),
               (f"How do I reset the {v['name']} filter light?", v["reset"])]
        body = (crumb((f"{v['name']} filters", None)) + f'<section class="hero s"><div class="w"><div><h1>{e(v["name"])} Refrigerator Water Filters</h1><p>Replacement water filters for {e(v["series"])}. Find your filter by part number or refrigerator model, and order with PayPal.</p>'
                f'<p><a class="btn wa big" href="{wa_link(f"Hi! I need a {v["name"]} refrigerator water filter. My model is: ")}" target="_blank" rel="noopener">Ask on WhatsApp</a></p></div></div></section>'
                f'<section class="sec"><div class="w"><h2 style="margin-top:0">{e(v["name"])} water filters</h2><div class="grid g3">{"".join(card(p) for p in ps)}</div>'
                f'<div class="txt"><h2>How to choose your {e(v["name"])} filter</h2><p>{e(guide["intro"])}</p><p><a href="/guides/{guide["slug"]}/">Read the {e(v["name"])} water filter guide</a> · <a href="/guides/reset-refrigerator-water-filter-light/">Reset the filter light</a></p>'
                f'<h2>{e(v["name"])} part numbers</h2><div class="chips">{"".join(f"<a href=\"{part_url(a)}\">{e(a)}</a>" for p in ps for a in parts_of(p))}</div>'
                + (f'<h2>{e(v["name"])} refrigerator models</h2><div class="chips">{"".join(f"<a href=\"{model_url(m, p)}\">{e(m)}</a>" for m, p in models)}</div>' if models else "")
                + f'<h2>{e(v["name"])} filter FAQ</h2>{faq_html(faq)}</div></div></section>')
        page(f"/{b}-refrigerator-water-filters/", f"{v['name']} Refrigerator Water Filters | Replacement Filters | {NAME}", f"Shop {v['name']} refrigerator water filter replacements. Find your filter by part number or model, ships from our U.S. warehouse, pay with PayPal.", body,
             [crumb_ld((f"{v['name']} filters", None)), faq_ld(faq), {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i, "url": f"{DOM}/filters/{p['slug']}/", "name": p["title"]} for i, p in enumerate(ps, 1)]}],
             og=f"og-{b}.jpg", prioridad="0.9")
    # todas / internos / externos
    def lista(path, h1, intro, ps, title, desc):
        body = (crumb((h1, None)) + f'<section class="hero s"><div class="w"><div><h1>{e(h1)}</h1><p>{e(intro)}</p></div></div></section><section class="sec"><div class="w"><div class="grid g3">{"".join(card(p) for p in ps)}</div></div></section>')
        page(path, title, desc, body, [crumb_ld((h1, None)), {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i, "url": f"{DOM}/filters/{p['slug']}/", "name": p["title"]} for i, p in enumerate(ps, 1)]}], prioridad="0.9")
    lista("/refrigerator-water-filters/", "Refrigerator Water Filters", "Replacement water filters for Samsung, LG, Whirlpool and GE refrigerators. Search by part number or refrigerator model.", P,
          f"All Refrigerator Water Filters by Brand and Part Number | {NAME}", "Shop refrigerator water filter replacements for Samsung, LG, Whirlpool and GE. Find your filter by model or part number. Ships from our U.S. warehouse.")
    lista("/internal-refrigerator-water-filters/", "Internal Refrigerator Water Filters", "Internal cartridge filters that sit inside the refrigerator's filter housing.", [p for p in P if p["kind"] == "internal"],
          f"Internal Refrigerator Water Filters | {NAME}", "Internal refrigerator water filter cartridges for Samsung, LG, Whirlpool and GE refrigerators.")
    lista("/external-inline-refrigerator-water-filters/", "External Inline Refrigerator Water Filters", "Inline filters that mount on the water line outside the refrigerator, for dispenser and ice maker supply.", [p for p in P if p["kind"] == "external"],
          f"External Inline Refrigerator Water Filters | {NAME}", "External inline water filters for refrigerators and ice makers. Samsung, LG and Whirlpool options.")


def guide_pages():
    cards = ""
    for x in G:
        url = f"/guides/{x['slug']}/"
        secs = ""
        for h, ps in x["sections"]:
            if len(ps) > 1 and all(len(t) < 140 for t in ps):
                secs += f"<h2>{e(h)}</h2><ul class=\"lista\">{''.join(f'<li>{e(t)}</li>' for t in ps)}</ul>"
            else:
                secs += f"<h2>{e(h)}</h2>" + "".join(f"<p>{e(t)}</p>" for t in ps)
        if x["steps"]:
            secs += '<h2>Quick steps</h2><ol class="steps">' + "".join(f"<li>{e(s)}</li>" for s in x["steps"]) + "</ol>"
        shop = ""
        if x["brand"]:
            shop = f'<h2>{e(BRANDS[x["brand"]]["name"])} water filters</h2><div class="grid g3">{"".join(card(p) for p in P if p["brand"] == x["brand"])}</div>'
        else:
            shop = f'<div class="buy" style="margin:26px 0"><b>Need a replacement filter?</b><p>Find your filter by refrigerator model or part number, or message us a photo of the old one.</p><p style="display:flex;gap:10px;flex-wrap:wrap"><a class="btn" href="/finder/">Find my filter</a><a class="btn wa" href="{wa_link("Hi! I need help finding my refrigerator water filter. My model is: ")}" target="_blank" rel="noopener">Ask on WhatsApp</a></p></div>'
        rel = "".join(f'<a href="/guides/{r}/">{e(next(y["h1"] for y in G if y["slug"] == r))}</a>' for r in x["related"] if any(y["slug"] == r for y in G))
        body = (crumb(("Guides", "/guides/"), (x["h1"], None)) + f'<div class="w txt"><h1>{e(x["h1"])}</h1><p class="lead">{e(x["intro"])}</p>{secs}{shop}'
                f'<h2>Frequently asked questions</h2>{faq_html(x["faq"])}' + (f'<h2>Related guides</h2><div class="chips">{rel}</div>' if rel else "") + '</div>')
        art = {"@context": "https://schema.org", "@type": "Article", "headline": x["h1"], "description": x["desc"], "datePublished": HOY, "dateModified": HOY, "inLanguage": "en-US",
               "author": {"@type": "Organization", "name": NAME}, "publisher": {"@type": "Organization", "name": NAME, "logo": {"@type": "ImageObject", "url": DOM + "/img/logo.svg"}},
               "mainEntityOfPage": DOM + url, "image": DOM + f"/img/{'og-' + x['brand'] if x['brand'] else 'og-home'}.jpg"}
        ld = [art, crumb_ld(("Guides", "/guides/"), (x["h1"], None)), faq_ld(x["faq"])]
        if x["steps"]:
            ld.append({"@context": "https://schema.org", "@type": "HowTo", "name": x["h1"], "step": [{"@type": "HowToStep", "position": i, "text": s} for i, s in enumerate(x["steps"], 1)]})
        page(url, f"{x['title']}", x["desc"], body, ld, og=f"og-{x['brand']}.jpg" if x["brand"] else "og-home.jpg", prioridad="0.8")
        SEARCH.append([x["h1"], url, x["title"] + " " + x["desc"], "Guide"])
        cards += f'<a class="card" href="{url}"><h3>{e(x["h1"])}</h3><p>{e(trim(x["desc"], 120))}</p></a>'
    body = (crumb(("Guides", None)) + f'<div class="w txt"><h1>Refrigerator Water Filter Guides</h1><p class="lead">Plain-English help for choosing, changing and troubleshooting refrigerator water filters.</p></div><div class="w"><div class="grid g3">{cards}</div></div>')
    page("/guides/", f"Refrigerator Water Filter Guides and How-Tos | {NAME}", "Guides for refrigerator water filters: how often to change, how to find your model number, reset the filter light, flush a new filter and fix leaks.", body, [crumb_ld(("Guides", None))], prioridad="0.8")


FAQ_HOME = [("How do I find the right water filter for my refrigerator?", "Use the model number on the label inside your refrigerator or the part number on your old filter. Search it in our finder, or message us a photo on WhatsApp and we will confirm it before you order."),
            ("How often should I replace a refrigerator water filter?", "Most manufacturers recommend about every six months, or sooner if the water flow slows down or the taste changes."),
            ("Do you ship from the United States?", "Yes. Orders ship from our U.S. warehouse and we send tracking information when your order ships."),
            ("How can I pay?", "Pay securely with PayPal or a credit or debit card at checkout. You can also message us on WhatsApp for help with your order."),
            ("Are the brand names on your site affiliated with the manufacturers?", "No. Samsung, LG, Whirlpool, GE and other names are trademarks of their owners and are used only to identify the refrigerator models and part numbers our filters fit."),
            ("What if I order the wrong filter?", "Send us your refrigerator model number or a photo of the old filter before you order and we will confirm the fit. See our shipping and returns page for the return policy.")]


def home_page():
    brands = "".join(f'<a class="card" href="/{b}-refrigerator-water-filters/"><h3>{e(v["name"])} refrigerator water filters</h3><p>{sum(1 for p in P if p["brand"] == b)} filters · {e(v["series"])}</p><span class="im">{pic(next(p for p in P if p["brand"] == b), BRANDS[b]["name"] + " refrigerator water filter")}</span></a>' for b, v in BRANDS.items())
    pop = [PBY[i] for i in ("sam-cin-o", "lg-700-o", "wp-1-o", "ge-mwf-o", "lg-1000-o", "wp-3-o", "sam-qin-o", "lg-800-o")]
    photos = "".join(f'<span>{pic(PBY[i], alt_of(PBY[i]), False, False)}</span>' for i in ("sam-cin-o", "lg-700-o", "wp-1-o"))
    body = (f'<section class="hero"><div class="w"><div><h1>Refrigerator Water Filters for Samsung, LG, Whirlpool and GE</h1><p>Find the replacement filter for your refrigerator by model number or part number. Ships from our U.S. warehouse. Pay securely with PayPal.</p>'
            '<form action="/finder/" class="srch" style="max-width:none;margin:18px 0"><input type="search" name="q" placeholder="Enter your refrigerator model or filter part number" aria-label="Refrigerator model or filter part number"><button type="submit">Find my filter</button></form>'
            f'<p><a class="btn wa big" href="{wa_link("Hi! I need help finding the right refrigerator water filter. My model is: ")}" target="_blank" rel="noopener">Not sure? Ask us on WhatsApp</a></p></div><div class="photos">{photos}</div></div></section>'
            '<section class="trust"><div class="w"><div><b>Delivered to your door</b><small>Ships from our U.S. warehouse, with tracking</small></div><div><b>Secure PayPal checkout</b><small>Pay in USD, card or PayPal</small></div><div><b>Fit check</b><small>We confirm your model before you order</small></div><div><b>WhatsApp support</b><small>Send a photo of your old filter</small></div></div></section>'
            f'<section class="sec"><div class="w"><div class="cab"><h2 style="margin-top:0">Shop by refrigerator brand</h2><p>Choose your brand to see the filters, part numbers and models.</p></div><div class="grid g4">{brands}</div></div></section>'
            f'<section class="sec alt"><div class="w"><div class="cab"><h2 style="margin-top:0">Popular refrigerator water filters</h2></div><div class="grid g4">{"".join(card(p) for p in pop)}</div><p style="margin-top:18px"><a class="btn" href="/refrigerator-water-filters/">See all refrigerator water filters</a></p></div></section>'
            '<section class="sec"><div class="w txt"><h2 style="margin-top:0">How to find the right refrigerator water filter</h2><ol class="steps"><li><b>Find your model number.</b> It is on a label inside the refrigerator, on a side wall or near the crisper drawers. <a href="/guides/how-to-find-your-refrigerator-model-number/">Where to look</a>.</li>'
            '<li><b>Match it to a filter.</b> Search your model or the part number printed on the old filter in our <a href="/finder/">filter finder</a> or the <a href="/part-numbers/">part number cross-reference</a>.</li>'
            '<li><b>Order and replace.</b> Pay with PayPal, and replace the filter about every six months. <a href="/guides/how-to-change-a-refrigerator-water-filter/">How to change it</a>.</li></ol></div></section>'
            f'<section class="sec alt"><div class="w txt"><h2 style="margin-top:0">Why replace your refrigerator water filter?</h2><p>A refrigerator water filter traps particles and reduces chlorine taste and odor, so the water and ice from your dispenser taste cleaner. The filter has a limited capacity: after about six months of normal use it is saturated and water can taste or flow differently. Most refrigerators remind you with a filter light.</p>'
            '<p>Replacing the filter on time is the simplest way to keep water and ice tasting fresh. <a href="/guides/how-often-to-change-a-refrigerator-water-filter/">Read how often to change it</a>.</p></div></section>'
            f'<section class="sec"><div class="w txt"><h2 style="margin-top:0">Frequently asked questions</h2>{faq_html(FAQ_HOME)}</div></section>'
            f'<section class="sec alt"><div class="w"><div class="cab"><h2 style="margin-top:0">Refrigerator water filter guides</h2></div><div class="chips">{"".join(f"<a href=\"/guides/{x[chr(115)+chr(108)+chr(117)+chr(103)]}/\">{e(x[chr(104)+chr(49)])}</a>" for x in G[:10])}</div><p><a href="/guides/">All guides</a></p></div></section>')
    ld = [org_ld(), {"@context": "https://schema.org", "@type": "WebSite", "@id": DOM + "/#site", "url": DOM + "/", "name": NAME, "inLanguage": "en-US", "publisher": {"@id": DOM + "/#org"},
                     "potentialAction": {"@type": "SearchAction", "target": DOM + "/finder/?q={search_term_string}", "query-input": "required name=search_term_string"}}, faq_ld(FAQ_HOME)]
    page("/", f"Refrigerator Water Filters: Samsung, LG, Whirlpool, GE | {NAME}", "Replacement refrigerator water filters for Samsung, LG, Whirlpool and GE. Find your filter by model or part number. Ships from our U.S. warehouse. Pay with PayPal.", body, ld, prioridad="1.0")


def static_pages():
    body = (crumb(("Find my filter", None)) + '<div class="w txt"><h1>Find Your Refrigerator Water Filter</h1><p class="lead">Type your refrigerator model number or the part number printed on your old filter.</p>'
            '<form class="srch" style="max-width:none" onsubmit="return false"><input id="finder-q" type="search" placeholder="Example: RF28HMEDBSR, LT700P, EDR1RXD1, DA29-00020B" aria-label="Refrigerator model or part number" autofocus><button>Search</button></form><div id="finder-res" class="resbox" style="margin-top:16px"></div>'
            f'<p>Cannot find it? Send us a photo of the old filter or the label inside your refrigerator on <a href="{wa_link("Hi! I could not find my refrigerator water filter. My model is: ")}">WhatsApp</a>.</p></div>')
    page("/finder/", f"Refrigerator Water Filter Finder by Model or Part Number | {NAME}", "Search by refrigerator model number or filter part number to find the replacement water filter for your Samsung, LG, Whirlpool or GE refrigerator.", body, [crumb_ld(("Find my filter", None))], prioridad="0.8")
    faq = FAQ_HOME + [(q, a) for x in G[:6] for q, a in x["faq"][:1]]
    page("/faq/", f"Refrigerator Water Filter FAQ | {NAME}", "Answers to common questions about refrigerator water filters: fit, replacement schedule, shipping and payment.", crumb(("FAQ", None)) + f'<div class="w txt"><h1>Refrigerator Water Filter FAQ</h1>{faq_html(faq)}</div>', [faq_ld(faq), crumb_ld(("FAQ", None))], prioridad="0.7")
    contact = (crumb(("Contact", None)) + f'<div class="w txt"><h1>Contact Us</h1><p class="lead">Not sure which filter you need? Send us your refrigerator model number or a photo of the old filter and we will help.</p>'
               f'<p><a class="btn wa big" href="{wa_link("Hi! I need help with a refrigerator water filter. My model is: ")}" target="_blank" rel="noopener">Message us on WhatsApp: {WA_DISP}</a></p>'
               + (f'<p>Email: <a href="mailto:{e(CFG["email"])}">{e(CFG["email"])}</a></p>' if CFG.get("email") else "") + '<p>Tell us your refrigerator brand, model number and the part number on your old filter if you can see it.</p></div>')
    page("/contact/", f"Contact | {NAME}", "Contact us on WhatsApp for help finding the right refrigerator water filter for your model.", contact, [crumb_ld(("Contact", None))], prioridad="0.5")
    about = (crumb(("About", None)) + f'<div class="w txt"><h1>About {e(NAME)}</h1><p>{e(NAME)} sells replacement water filters for Samsung, LG, Whirlpool and GE refrigerators. Orders ship from our U.S. warehouse.</p>'
             '<p>We built this store to make one thing easy: finding the right filter for your refrigerator. Search by model number or part number, and if you are not sure, send us a photo of your old filter. We will confirm the fit before you order.</p>'
             '<p>Our team also speaks Spanish: escríbenos por WhatsApp si prefieres español.</p></div>')
    page("/about/", f"About {NAME}", f"About {NAME}: replacement refrigerator water filters shipped from our U.S. warehouse.", about, [crumb_ld(("About", None))], prioridad="0.4")
    ship = (crumb(("Shipping & returns", None)) + f'<div class="w txt"><h1>Shipping and Returns</h1><h2>Shipping</h2><p>Orders ship from our U.S. warehouse. We send tracking information by email when your order ships. Delivery to your door is included in the price of the filters shown with a price; if shipping is charged, it is shown at checkout.</p>'
            '<h2>Returns</h2><p>If you ordered the wrong filter, contact us before you open the package. Unopened filters in original packaging can be returned; contact us on WhatsApp to start a return. Opened or used filters cannot be returned for hygiene reasons unless they are defective.</p>'
            '<h2>Damaged or defective items</h2><p>If your order arrives damaged or defective, send us a photo and your order number and we will make it right.</p>'
            '<p class="note">Policy details may be updated. Contact us with any questions before ordering.</p></div>')
    page("/shipping-returns/", f"Shipping and Returns | {NAME}", "Shipping and return information for refrigerator water filter orders.", ship, [crumb_ld(("Shipping & returns", None))], prioridad="0.4")
    priv = (crumb(("Privacy policy", None)) + f'<div class="w txt"><h1>Privacy Policy</h1><p>We collect the information you give us when you contact us or place an order (name, email, shipping address, phone number and order details) to process and ship your order and to answer your questions. Payments are processed by PayPal: we do not store your card number.</p>'
            '<p>We do not sell your personal information. We may use analytics tools to understand how the site is used. You can ask us to correct or delete your information by contacting us on WhatsApp or by email.</p></div>')
    page("/privacy-policy/", f"Privacy Policy | {NAME}", f"How {NAME} handles customer information.", priv, [crumb_ld(("Privacy policy", None))], prioridad="0.3")
    terms = (crumb(("Terms", None)) + '<div class="w txt"><h1>Terms of Use</h1><p>By using this site you agree to these terms. Product information, part numbers and compatibility lists are provided to help you choose a filter; always confirm fit with your refrigerator model number before ordering. Prices and availability may change.</p>'
             '<p>Orders are accepted after payment is confirmed. See our shipping and returns page for how we handle shipments and returns.</p></div>')
    page("/terms/", f"Terms of Use | {NAME}", "Terms of use for this store.", terms, [crumb_ld(("Terms", None))], prioridad="0.3")
    disc = (crumb(("Brand disclaimer", None)) + '<div class="w txt"><h1>Brand Disclaimer</h1><p>Samsung, LG, Whirlpool, Maytag, KitchenAid, Jenn-Air, Amana, GE and all other brand names mentioned on this site are trademarks of their respective owners. They are used only to identify the refrigerator models and part numbers that our filters fit.</p>'
            '<p>This store is not affiliated with, endorsed by or sponsored by any of those brands.</p></div>')
    page("/disclaimer/", f"Brand Disclaimer | {NAME}", "Brand and trademark disclaimer.", disc, [crumb_ld(("Brand disclaimer", None))], prioridad="0.3")
    page("/thank-you/", f"Thank you for your order | {NAME}", "Order confirmation.", '<div class="w txt"><h1>Thank you for your order!</h1><p class="lead">Your payment was received. We will email you tracking information when your order ships.</p><p>Questions? Message us on WhatsApp.</p></div>', noindex=True)
    f = OUT / "404.html"; f.write_text("<!doctype html><meta charset=utf-8><title>Page not found</title><meta name=robots content=noindex><body style='font-family:system-ui;padding:40px'><h1>Page not found</h1><p><a href=/>Go to the home page</a> or <a href=/finder/>find your refrigerator water filter</a>.</p>", encoding="utf-8")


def tecnico():
    a = OUT / "assets"; a.mkdir(parents=True, exist_ok=True)
    (a / "site.css").write_text(CSS, encoding="utf-8")
    (a / "store.js").write_text(JS, encoding="utf-8")
    (a / "search.json").write_text(json.dumps(SEARCH, ensure_ascii=False), encoding="utf-8")
    (a / "prices.json").write_text(json.dumps({k: {"price": v["price"], "pack": v["pack"]} for k, v in PR.items() if v["price"]}), encoding="utf-8")
    (OUT / "img" / "logo.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="8" fill="#fff"/><path d="M16 3c4 6 8 10 8 15a8 8 0 0 1-16 0c0-5 4-9 8-15z" fill="#12b3d3"/><path d="M16 9c2.4 3.6 5 6.2 5 9.2a5 5 0 0 1-10 0c0-3 2.6-5.6 5-9.2z" fill="#0a5ea8"/></svg>', encoding="utf-8")
    urls = "".join(f"<url><loc>{DOM}{u}</loc><lastmod>{HOY}</lastmod><priority>{pr}</priority></url>\n" for u, pr in sorted(PAGES.items(), key=lambda x: (-float(x[1]), x[0])))
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nUser-agent: GPTBot\nAllow: /\nUser-agent: ClaudeBot\nAllow: /\nUser-agent: PerplexityBot\nAllow: /\nUser-agent: Google-Extended\nAllow: /\n\nSitemap: {DOM}/sitemap.xml\n", encoding="utf-8")
    txt = f"# {NAME}\n\n> Replacement refrigerator water filters for Samsung, LG, Whirlpool and GE refrigerators. Ships from a U.S. warehouse. Pay with PayPal. WhatsApp +{WA}.\n\n## Filters\n"
    txt += "".join(f"- [{p['title']}]({DOM}/filters/{p['slug']}/): part {p['ref']}, also {p['also']}.\n" for p in P)
    txt += "\n## Guides\n" + "".join(f"- [{x['h1']}]({DOM}/guides/{x['slug']}/)\n" for x in G)
    txt += f"\n## Key pages\n- [All filters]({DOM}/refrigerator-water-filters/)\n- [Part number cross-reference]({DOM}/part-numbers/)\n- [Filter finder]({DOM}/finder/)\n\n## Questions and answers\n" + "".join(f"- **{q}** {a}\n" for q, a in FAQ_HOME)
    (OUT / "llms.txt").write_text(txt, encoding="utf-8")
    (OUT / ".htaccess").write_text("ErrorDocument 404 /404.html\nDirectoryIndex index.html\n<IfModule mod_deflate.c>\nAddOutputFilterByType DEFLATE text/html text/css application/javascript application/json image/svg+xml text/plain application/xml\n</IfModule>\n<IfModule mod_expires.c>\nExpiresActive On\nExpiresByType image/webp \"access plus 1 year\"\nExpiresByType image/jpeg \"access plus 1 year\"\nExpiresByType image/svg+xml \"access plus 1 year\"\nExpiresByType text/css \"access plus 1 month\"\nExpiresByType application/javascript \"access plus 1 month\"\nExpiresByType text/html \"access plus 10 minutes\"\n</IfModule>\n", encoding="utf-8")


def main():
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(parents=True); (OUT / "img").mkdir()
    preparar_imagenes(); preparar_og()
    home_page(); collection_pages(); product_pages(); part_pages(); model_pages(); guide_pages(); static_pages(); tecnico()
    z = RAIZ / "tienda-eeuu.zip"; z.unlink(missing_ok=True)
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in OUT.rglob("*"):
            if f.is_file(): zf.write(f, f.relative_to(OUT).as_posix())
    n = sum(1 for _ in OUT.rglob("index.html"))
    print(f"OK: {n} páginas, {len(PAGES)} en el sitemap → {z.name}")


if __name__ == "__main__":
    main()
