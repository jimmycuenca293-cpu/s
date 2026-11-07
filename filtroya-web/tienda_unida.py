#!/usr/bin/env python3
"""Tienda unida de repuestos para lavadoras (filtrosparalavadoras.click).

Une en un solo sitio las tres tiendas que ya existen, sin cambiar ninguna dirección (para no perder posicionamiento ni anuncios):
  /                          portada nueva: repuestos para lavadoras (filtros, bombas, mangueras, presostatos)
  /samsung/  /lg/            filtros de pelusas
  /bombas-de-agua/           bombas de desagüe
  /mangueras-para-lavadora/  mangueras y presostatos
y le pone a todas una barra común arriba para saltar entre las secciones.

Uso:  python3 tienda_unida.py        → sitios-unida/public_html/ y tienda-repuestos-lavadoras.zip (se sube a public_html)
"""
import importlib, json, re, shutil, subprocess, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
SALIDA = AQUI / "sitios-unida" / "public_html"
DOM = "https://filtrosparalavadoras.click"
RAIZ = AQUI / "sitios-lavadoras" / "tienda"
BOMB = AQUI / "sitios-bombas" / "tienda" / "bombas-de-agua"
MANG = AQUI / "sitios-mangueras" / "tienda" / "mangueras-para-lavadora"

# 1) construir las tres tiendas
for s in ("lavadoras.py", "bombas.py", "mangueras.py"):
    subprocess.run([sys.executable, str(AQUI / s)], cwd=AQUI, check=True, stdout=subprocess.DEVNULL)

sys.path.insert(0, str(AQUI))
import lavadoras as L
_esc, _marcas = L.escribir, L.MARCAS
MF = {k: dict(v) for k, v in L.MARCAS.items()}
import bombas as B
MB = B.MARCAS
import mangueras as M
MM = M.MARCAS["todas"]
L.escribir, L.MARCAS = _esc, _marcas
esc, cop, wa_link = L.esc, L.cop, L.wa_link

WA_SAM, TEL_SAM = "3054796329", "305 479 6329"
WA_LG, TEL_LG = "3205102995", "320 510 2995"

# 2) productos de las cuatro secciones (nombre corto para tarjetas)
def filtros():
    out = []
    for k, m in MF.items():
        for p in m["productos"]:
            out.append(dict(id=p["id"], img=f"/img/{p['id']}", href=f"/{k}/{p['slug']}/", nombre=f"{p['corto']} · {m['nombre']}", tipo=p["tipo"], wa=m["whatsapp"], marca=m["nombre"]))
    return out

def bombas():
    out = []
    for k, m in MB.items():
        for p in m["productos"]:
            out.append(dict(id=p["id"], img=f"/bombas-de-agua/img/{p['id']}", href=f"/bombas-de-agua/{k}/{p['slug']}/", nombre=f"Bomba de desagüe · {m['nombre']}", tipo=p["tipo"], wa=m["whatsapp"], marca=m["nombre"]))
    return out

def mangueras():
    out = []
    for p in MM["productos"]:
        out.append(dict(id=p["id"], img=f"/mangueras-para-lavadora/img/{p['id']}", href=f"/mangueras-para-lavadora/{p['slug']}/", nombre=p["nombre"], tipo=p["tipo"],
                        wa=p.get("wa") or MM["whatsapp"], marca=p.get("marca", ""), cat=p["cat"]))
    return out

F, Bo, Ma = filtros(), bombas(), mangueras()
Man = [p for p in Ma if p["cat"] != "presostato"]
Pre = [p for p in Ma if p["cat"] == "presostato"]

# 3) barra común + estilos (se aplican a las tres tiendas)
CSS = """
/* ---- tienda unida ---- */
.m-hub{background:#0a1f44;color:#fff}.m-hub .m-wrap{display:flex;gap:2px;overflow-x:auto;scrollbar-width:none;padding-block:0}
.m-hub .m-wrap::-webkit-scrollbar{display:none}
.m-hub a{color:#cdd8ef;text-decoration:none;font-weight:700;font-size:14px;padding:11px 15px;white-space:nowrap;border-bottom:3px solid transparent}
.m-hub a:hover{color:#fff}.m-hub a.on{color:#fff;border-bottom-color:#ffc83d}
.h-hero{background:radial-gradient(1200px 520px at 85% -10%,#2a5fc8 0%,rgba(42,95,200,0) 60%),linear-gradient(160deg,#071a3d,#0b2f6b 70%);color:#fff;padding:64px 0 74px;position:relative;overflow:hidden}
.h-hero .m-wrap{display:grid;grid-template-columns:1.1fr .9fr;gap:44px;align-items:center}
.h-hero h1{font-size:clamp(34px,5vw,56px);line-height:1.05;margin:0 0 16px;letter-spacing:-.025em;color:#fff}
.h-hero .lead{font-size:19px;line-height:1.6;color:#d6e0f5;max-width:34em;margin:0 0 26px}
.h-kick{display:inline-block;background:rgba(255,200,61,.16);color:#ffd877;font-weight:800;font-size:12.5px;letter-spacing:1.6px;text-transform:uppercase;padding:7px 13px;border-radius:99px;margin-bottom:16px}
.h-acc{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:22px}
.h-acc .m-btn{font-size:17px;padding:15px 24px}
.h-btn2{background:transparent;border:2px solid rgba(255,255,255,.55);color:#fff!important}.h-btn2:hover{background:#fff;color:#0b2f6b!important}
.h-pts{display:flex;flex-wrap:wrap;gap:8px 20px;list-style:none;padding:0;margin:0;color:#cdd8ef;font-weight:600;font-size:15px}.h-pts li::before{content:"✓";color:#ffc83d;margin-right:7px;font-weight:800}
.h-collage{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.h-collage a{background:#fff;border-radius:22px;aspect-ratio:1/1;display:grid;place-items:center;padding:14px;box-shadow:0 18px 40px rgba(0,0,0,.28);transition:transform .2s;position:relative;text-decoration:none}
.h-collage a:hover{transform:translateY(-5px) rotate(-1deg)}.h-collage a:nth-child(2){transform:translateY(22px)}.h-collage a:nth-child(2):hover{transform:translateY(17px)}
.h-collage a:nth-child(4){transform:translateY(22px)}.h-collage a:nth-child(4):hover{transform:translateY(17px)}
.h-collage img{max-width:100%;max-height:100%;object-fit:contain}
.h-collage span{position:absolute;left:12px;bottom:12px;background:#0b2f6b;color:#fff;font-size:12.5px;font-weight:800;padding:5px 11px;border-radius:99px}
.h-sec{padding:64px 0}.h-sec.alt{background:#f2f6fd}
.h-cab{max-width:760px;margin:0 0 30px}.h-cab .eyebrow{display:block;color:#1f55c4;font-weight:800;letter-spacing:1.6px;text-transform:uppercase;font-size:12.5px;margin-bottom:8px}
.h-cab h2{font-size:clamp(26px,3.4vw,38px);margin:0 0 10px;letter-spacing:-.02em}.h-cab p{color:#5a6b86;font-size:17px;margin:0}
.h-cats{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}
.h-cat{background:#fff;border:1px solid #dbe4f3;border-radius:24px;overflow:hidden;display:flex;flex-direction:column;text-decoration:none;color:inherit;transition:transform .2s,box-shadow .2s;box-shadow:0 6px 18px rgba(10,31,68,.06)}
.h-cat:hover{transform:translateY(-6px);box-shadow:0 20px 40px rgba(10,31,68,.16)}
.h-cat .ph{background:linear-gradient(180deg,#f6f9ff,#e6eefb);aspect-ratio:4/3;display:grid;place-items:center;padding:16px;position:relative}
.h-cat .ph img{max-width:88%;max-height:100%;object-fit:contain}
.h-cat .n{position:absolute;top:12px;right:12px;background:#0b2f6b;color:#fff;font-size:12.5px;font-weight:800;padding:5px 11px;border-radius:99px}
.h-cat .tx{padding:20px 22px 24px;display:flex;flex-direction:column;gap:8px;flex:1}
.h-cat h3{font-size:21px;margin:0;color:#0a1f44}.h-cat p{margin:0;color:#5a6b86;font-size:15px;line-height:1.55;flex:1}
.h-cat b{color:#1f55c4;font-size:15px}
.h-marcas{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.h-marca{border-radius:22px;padding:26px;color:#fff;display:flex;flex-direction:column;gap:10px;text-decoration:none;min-height:190px}
.h-marca h3{margin:0;font-size:26px;color:#fff}.h-marca p{margin:0;opacity:.92;font-size:15.5px}.h-marca .links{display:flex;flex-wrap:wrap;gap:8px;margin-top:auto}
.h-marca .links a{background:rgba(255,255,255,.18);color:#fff;border-radius:99px;padding:7px 13px;font-weight:700;font-size:13.5px;text-decoration:none}.h-marca .links a:hover{background:#fff;color:#0a1f44}
.h-sam{background:linear-gradient(145deg,#0a2a8a,#1648c8)}.h-lg{background:linear-gradient(145deg,#8e0a2c,#c2123d)}.h-todas{background:linear-gradient(145deg,#12315f,#2a4f86)}
.h-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.h-prod{background:#fff;border:1px solid #dbe4f3;border-radius:20px;overflow:hidden;display:flex;flex-direction:column;box-shadow:0 4px 14px rgba(10,31,68,.05)}
.h-prod .im{display:grid;place-items:center;background:#fff;aspect-ratio:1/1;padding:14px;border-bottom:1px solid #eef2fa}.h-prod .im img{max-width:100%;max-height:100%;object-fit:contain}
.h-prod .tx{padding:14px 16px 18px;display:flex;flex-direction:column;gap:6px;flex:1}.h-prod h3{font-size:15.5px;line-height:1.3;margin:0}.h-prod h3 a{color:#0a1f44;text-decoration:none}
.h-prod small{color:#5a6b86}.h-prod .m-btn{margin-top:auto;font-size:14px;padding:11px 12px}
.h-ver{margin-top:22px}
.h-pasos{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;counter-reset:p}
.h-paso{background:#fff;border:1px solid #dbe4f3;border-radius:22px;padding:26px;position:relative}
.h-paso::before{counter-increment:p;content:counter(p);display:grid;place-items:center;width:46px;height:46px;border-radius:50%;background:#ffc83d;color:#0a1f44;font-weight:800;font-size:22px;margin-bottom:14px}
.h-paso h3{margin:0 0 6px;font-size:20px}.h-paso p{margin:0;color:#5a6b86}
.h-conf{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:-34px;position:relative;z-index:3}
.h-conf div{background:#fff;border:1px solid #dbe4f3;border-radius:18px;padding:18px 20px;display:flex;gap:12px;align-items:center;box-shadow:0 12px 30px rgba(10,31,68,.12)}
.h-conf .ic{font-size:26px}.h-conf b{display:block;color:#0a1f44}.h-conf small{color:#5a6b86}
.h-cta{background:linear-gradient(135deg,#071a3d,#0b2f6b);border-radius:28px;color:#fff;padding:42px;display:flex;gap:26px;justify-content:space-between;align-items:center;flex-wrap:wrap}
.h-cta h2{margin:0 0 8px;color:#fff;font-size:clamp(24px,3vw,34px)}.h-cta p{margin:0;color:#d6e0f5;max-width:32em}.h-cta .acc{display:flex;flex-wrap:wrap;gap:12px}
@media (max-width:1000px){.h-hero .m-wrap{grid-template-columns:1fr}.h-collage{max-width:520px}.h-cats,.h-grid{grid-template-columns:1fr 1fr}.h-marcas,.h-pasos{grid-template-columns:1fr}.h-conf{grid-template-columns:1fr 1fr}}
@media (max-width:560px){.h-hero{padding:40px 0 56px}.h-cats,.h-grid{grid-template-columns:1fr 1fr;gap:12px}.h-cat h3{font-size:17px}.h-cat .tx{padding:14px}.h-conf{grid-template-columns:1fr;margin-top:-26px}.h-sec{padding:44px 0}.h-cta{padding:28px}}
"""

HUB_PHP = r"""
    $u = $_SERVER['REQUEST_URI'] ?? '/';
    $on = fn(string $p, bool $exacto = false) => ($exacto ? $u === $p : str_starts_with($u, $p)) ? ' class="on"' : '';
    $pre = str_contains($u, 'presostato');
    echo '<nav class="m-hub" aria-label="Secciones de la tienda"><div class="m-wrap">'
        . '<a href="/"' . ($u === '/' || $u === '/index.php' ? ' class="on"' : '') . '>🏠 Inicio</a>'
        . '<a href="/#filtros"' . ((str_starts_with($u, '/samsung') || str_starts_with($u, '/lg')) ? ' class="on"' : '') . '>Filtros de pelusa</a>'
        . '<a href="/bombas-de-agua/"' . (str_starts_with($u, '/bombas-de-agua') ? ' class="on"' : '') . '>Bombas de desagüe</a>'
        . '<a href="/mangueras-para-lavadora/"' . (str_starts_with($u, '/mangueras-para-lavadora') && !$pre ? ' class="on"' : '') . '>Mangueras</a>'
        . '<a href="/mangueras-para-lavadora/presostato-para-lavadora-samsung-y-lg-inverter/"' . ($pre ? ' class="on"' : '') . '>Presostatos</a>'
        . '</div></nav>';
"""

def parchear(carpeta):
    mp = carpeta / "marcas.php"
    t = mp.read_text(encoding="utf-8")
    if "m-hub" not in t:
        # la barra va justo después del aviso azul de arriba
        t, n = re.subn(r"(\. '<div class=\"m-anuncio\">.*?</div>')", lambda m: m.group(1) + "\n        . (function () { ob_start(); " + HUB_PHP.replace("echo ", "echo ", 1) + " return ob_get_clean(); })()", t, count=1, flags=re.S)
        assert n == 1, carpeta
        mp.write_text(t, encoding="utf-8")
    css = carpeta / "marcas.css"
    c = css.read_text(encoding="utf-8")
    if "tienda unida" not in c: css.write_text(c + CSS, encoding="utf-8")

# 4) portada nueva
def tarjeta(p, i=0):
    msg = f"Hola, quiero consultar por: {p['nombre']}"
    return (f'<article class="h-prod"><a class="im" href="{p["href"]}"><picture><source srcset="{p["img"]}-400.webp" type="image/webp"><img src="{p["img"]}.jpg" alt="{esc(p["nombre"])}" width="400" height="400" loading="lazy"></picture></a>'
            f'<div class="tx"><h3><a href="{p["href"]}">{esc(p["nombre"])}</a></h3><small>{esc(p["tipo"])}</small>'
            f'<a class="m-btn wa" href="{esc(wa_link(p["wa"], msg))}" target="_blank" rel="noopener">💬 Preguntar</a></div></article>')

def portada():
    def foto(p, w=900): return f'<picture><source srcset="{p["img"]}.webp" type="image/webp"><img src="{p["img"]}.jpg" alt="{esc(p["nombre"])}" width="600" height="600"></picture>'
    destacados = [F[0], Bo[0], Man[0], Pre[0]]
    colash = (f'<a href="/#filtros">{foto(F[0])}<span>Filtros</span></a><a href="/bombas-de-agua/">{foto(Bo[1])}<span>Bombas</span></a>'
              f'<a href="/mangueras-para-lavadora/">{foto(Man[3])}<span>Mangueras</span></a><a href="/mangueras-para-lavadora/presostato-para-lavadora-samsung-y-lg-inverter/">{foto(Pre[0])}<span>Presostatos</span></a>')
    cats = [
        ("Filtros de pelusa", "Filtros y bolsas de malla para lavadoras Samsung y LG, de carga superior y frontal.", f"{len(F)} referencias", F[1], "/#filtros", "Ver filtros →"),
        ("Bombas de desagüe", "La bomba que saca el agua de la lavadora. Para Samsung y LG, con foto de cada una.", f"{len(Bo)} bombas", Bo[2], "/bombas-de-agua/", "Ver bombas →"),
        ("Mangueras", "Entrada de agua fría (azul) y caliente (naranja), negra con rosca, desagüe y tina-bomba. Sirven para todas las marcas.", f"{len(Man)} mangueras", Man[1], "/mangueras-para-lavadora/", "Ver mangueras →"),
        ("Presostatos", "El sensor de nivel de agua para lavadoras Samsung y LG inverter. Va por marca y modelo.", f"{len(Pre)} presostatos", Pre[2], "/mangueras-para-lavadora/presostato-para-lavadora-samsung-y-lg-inverter/", "Ver presostatos →"),
    ]
    ch = "".join(f'<a class="h-cat" href="{h}"><span class="ph"><span class="n">{n}</span>{foto(p)}</span><span class="tx"><h3>{t}</h3><p>{d}</p><b>{v}</b></span></a>' for t, d, n, p, h, v in cats)
    marcas = f'''<div class="h-marcas">
<div class="h-marca h-sam"><h3>Samsung</h3><p>Filtros, bombas y presostato para tu lavadora Samsung. Asesor propio por WhatsApp: {TEL_SAM}.</p><div class="links"><a href="/samsung/">Filtros</a><a href="/bombas-de-agua/samsung/">Bombas</a><a href="/mangueras-para-lavadora/presostato-lavadora-samsung-inverter-dc32-00025a/">Presostato</a></div></div>
<div class="h-marca h-lg"><h3>LG</h3><p>Filtros, bombas y presostato para tu lavadora LG. Asesor propio por WhatsApp: {TEL_LG}.</p><div class="links"><a href="/lg/">Filtros</a><a href="/bombas-de-agua/lg/">Bombas</a><a href="/mangueras-para-lavadora/presostato-lavadora-lg-inverter-con-manguerita/">Presostato</a></div></div>
<div class="h-marca h-todas"><h3>Todas las marcas</h3><p>Las mangueras de entrada, desagüe y tina-bomba sirven para lavadoras de cualquier marca.</p><div class="links"><a href="/mangueras-para-lavadora/mangueras-de-entrada-de-agua-para-lavadora/">Entrada</a><a href="/mangueras-para-lavadora/mangueras-de-desague-para-lavadora/">Desagüe</a><a href="/mangueras-para-lavadora/manguera-tina-bomba-para-lavadora/">Tina-bomba</a></div></div>
</div>'''
    def seccion(id_, eyebrow, titulo, sub, lista, ver, alt=False):
        return (f'<section class="h-sec{" alt" if alt else ""}" id="{id_}"><div class="m-wrap"><div class="h-cab"><span class="eyebrow">{eyebrow}</span><h2>{titulo}</h2><p>{sub}</p></div>'
                f'<div class="h-grid">{"".join(tarjeta(p) for p in lista)}</div><p class="h-ver"><a class="m-btn sec" href="{ver[0]}">{ver[1]}</a></p></div></section>')
    secs = (seccion("filtros", "Sección 1", "Filtros de pelusa para lavadora", "Filtros y bolsas de malla de Samsung y LG. El asesor te confirma el tuyo con el modelo.", F, ("/samsung/", "Ver todos los filtros Samsung"), False)
            + seccion("bombas", "Sección 2", "Bombas de desagüe", "Bomba de agua de la lavadora (bomba de desagüe) para Samsung y LG.", Bo[:8], ("/bombas-de-agua/", "Ver todas las bombas"), True)
            + seccion("mangueras", "Sección 3", "Mangueras para lavadora", "Entrada de agua (azul fría, naranja caliente, negra con rosca), desagüe y tina-bomba. Sirven para todas las marcas.", Man, ("/mangueras-para-lavadora/", "Ver todas las mangueras"), False)
            + seccion("presostatos", "Sección 4", "Presostatos Samsung y LG inverter", "El sensor de nivel de agua. No es genérico: va por marca y modelo, cada uno con su asesor.", Pre, ("/mangueras-para-lavadora/presostato-para-lavadora-samsung-y-lg-inverter/", "Ver presostatos"), True))
    faq = [
        ("¿Qué repuestos para lavadora venden?", "Filtros de pelusas y bolsas de malla, bombas de desagüe, mangueras de entrada, desagüe y tina-bomba, y presostatos (sensor de nivel de agua) para lavadoras Samsung y LG."),
        ("¿Cómo sé cuál repuesto necesita mi lavadora?", "Escríbele al asesor por WhatsApp con el modelo de tu lavadora (está en una etiqueta atrás, en un costado o bajo la tapa) o con una foto de la pieza vieja, y te confirma el correcto antes de que compres."),
        ("¿Las mangueras sirven para todas las lavadoras?", "Las de entrada de agua sí: la conexión es estándar. La de desagüe cambia de medida (las más largas son para carga frontal) y el presostato va por marca y modelo."),
        ("¿Cuánto cuesta?", "Depende del repuesto, del modelo y de la ciudad. Pregúntale al asesor por WhatsApp y te responde en el momento."),
        ("¿Hacen envíos a toda Colombia?", "Sí, enviamos por transportadora a todo el país y te mandamos el número de guía."),
        ("¿Cómo pago?", "Con pago contra entrega: pagas cuando recibes el paquete. El asesor te confirma si está disponible en tu ciudad."),
    ]
    mensaje = "Hola, necesito un repuesto para mi lavadora"
    cuerpo = f'''<section class="h-hero"><div class="m-wrap"><div>
<span class="h-kick">Repuestos para lavadoras</span>
<h1>Todo para reparar tu lavadora, en un solo lugar</h1>
<p class="lead">Filtros de pelusa, bombas de desagüe, mangueras y presostatos para lavadoras Samsung y LG. Cuéntale tu modelo al asesor por WhatsApp, te confirmamos la pieza correcta y te la enviamos a toda Colombia con pago contra entrega.</p>
<div class="h-acc"><a class="m-btn wa" href="{esc(wa_link(WA_SAM, mensaje))}" target="_blank" rel="noopener">💬 Asesor Samsung</a><a class="m-btn wa" href="{esc(wa_link(WA_LG, mensaje))}" target="_blank" rel="noopener">💬 Asesor LG</a><a class="m-btn h-btn2" href="#categorias">Ver repuestos</a></div>
<ul class="h-pts"><li>Pago contra entrega</li><li>Envío a toda Colombia</li><li>Te confirmamos la pieza correcta</li></ul>
</div><div class="h-collage">{colash}</div></div></section>
<div class="m-wrap"><div class="h-conf"><div><span class="ic">💵</span><span><b>Pago contra entrega</b><small>Pagas al recibir</small></span></div><div><span class="ic">🚚</span><span><b>Envío a toda Colombia</b><small>Con número de guía</small></span></div><div><span class="ic">💬</span><span><b>Asesor por WhatsApp</b><small>Te confirma el modelo</small></span></div><div><span class="ic">🔧</span><span><b>Guía para cambiarlo</b><small>Paso a paso incluido</small></span></div></div></div>
<section class="h-sec" id="categorias"><div class="m-wrap"><div class="h-cab"><span class="eyebrow">Compra por repuesto</span><h2>¿Qué le pasa a tu lavadora?</h2><p>Escoge el tipo de repuesto. Si no sabes cuál necesitas, escríbele al asesor y él te dice.</p></div><div class="h-cats">{ch}</div></div></section>
<section class="h-sec alt"><div class="m-wrap"><div class="h-cab"><span class="eyebrow">Compra por marca</span><h2>¿De qué marca es tu lavadora?</h2><p>Cada marca tiene su asesor por WhatsApp.</p></div>{marcas}</div></section>
{secs}
<section class="h-sec"><div class="m-wrap"><div class="h-cab"><span class="eyebrow">Así de fácil</span><h2>Compra en 3 pasos</h2></div><div class="h-pasos"><div class="h-paso"><h3>Escríbele al asesor</h3><p>Dile qué repuesto necesitas y el modelo de tu lavadora, o mándale una foto de la pieza vieja.</p></div><div class="h-paso"><h3>Confirma pieza y envío</h3><p>El asesor te dice cuál es, el valor y el tiempo de entrega a tu ciudad.</p></div><div class="h-paso"><h3>Recibe y paga</h3><p>Llega a tu casa con número de guía y pagas contra entrega.</p></div></div></div></section>
<section class="h-sec alt" id="preguntas"><div class="m-wrap"><div class="h-cab"><span class="eyebrow">Resolvemos tus dudas</span><h2>Preguntas frecuentes</h2></div>{L.faq_html(faq)}</div></section>
<section class="h-sec"><div class="m-wrap"><div class="h-cta"><div><h2>¿No sabes cuál repuesto necesitas?</h2><p>Mándanos el modelo de tu lavadora o una foto de la pieza por WhatsApp y te decimos cuál es.</p></div><div class="acc"><a class="m-btn wa" href="{esc(wa_link(WA_SAM, mensaje))}" target="_blank" rel="noopener">💬 Asesor Samsung</a><a class="m-btn wa" href="{esc(wa_link(WA_LG, mensaje))}" target="_blank" rel="noopener">💬 Asesor LG</a></div></div></div></section>'''
    ld = [{"@type": "WebSite", "name": "Repuestos para lavadoras", "url": DOM + "/", "inLanguage": "es-CO"}, L.faq_ld(faq),
          {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i, "url": DOM + p["href"], "name": p["nombre"]} for i, p in enumerate(F + Bo + Man + Pre, 1)]}]
    return cuerpo, ld

def escribir_portada():
    cuerpo, ld = portada()
    titulo = "Repuestos para lavadoras: filtros, bombas, mangueras y presostatos"
    desc = "Filtros de pelusa, bombas de desagüe, mangueras y presostatos para lavadoras Samsung y LG. Pregunta al asesor por WhatsApp, paga contra entrega y recibe en toda Colombia."
    ldj = json.dumps({"@context": "https://schema.org", "@graph": ld}, ensure_ascii=False)
    og = f'<meta property="og:image" content="{DOM}/img/lav-sam-1.jpg">'
    php = ("<?php $MARCA = 'home'; require __DIR__ . '/lav.php';\nlav_cabeza(" + json.dumps(titulo, ensure_ascii=False) + ", " + json.dumps(desc, ensure_ascii=False) + ", '/', "
           + json.dumps(og, ensure_ascii=False) + ", <<<'JSON'\n" + ldj + "\nJSON);\n?>\n" + cuerpo + "\n<?php lav_pie(); ?>\n")
    (SALIDA / "index.php").write_text(php, encoding="utf-8")

# 5) ensamblar public_html
if SALIDA.parent.exists(): shutil.rmtree(SALIDA.parent)
SALIDA.mkdir(parents=True)
shutil.copytree(RAIZ, SALIDA, dirs_exist_ok=True, ignore=shutil.ignore_patterns("pedidos.sqlite*", "correos.log", "config.php"))
shutil.copytree(BOMB, SALIDA / "bombas-de-agua", ignore=shutil.ignore_patterns("pedidos.sqlite*", "correos.log", "config.php"))
shutil.copytree(MANG, SALIDA / "mangueras-para-lavadora", ignore=shutil.ignore_patterns("pedidos.sqlite*", "correos.log", "config.php"))
for c in (SALIDA, SALIDA / "bombas-de-agua", SALIDA / "mangueras-para-lavadora"):
    parchear(c)
escribir_portada()
# menú de la portada: categorías en vez de solo filtros
mh = json.loads((SALIDA / "marca-home.json").read_text(encoding="utf-8"))
mh.update({"tienda": "Repuestos para lavadoras", "productos": [], "guias": [], "ciudades": [], "hub": None,
           "extra": [["Filtros de pelusa", "/#filtros"], ["Bombas de desagüe", "/bombas-de-agua/"], ["Mangueras", "/mangueras-para-lavadora/"], ["Presostatos", "/mangueras-para-lavadora/presostato-para-lavadora-samsung-y-lg-inverter/"], ["Filtros Samsung", "/samsung/"], ["Filtros LG", "/lg/"]]})
for nombre in ("marca-home.json", "marca.json"):
    (SALIDA / nombre).write_text(json.dumps(mh, ensure_ascii=False), encoding="utf-8")
mp = (SALIDA / "marcas.php").read_text(encoding="utf-8")
mp = mp.replace("<span>✔ Filtros para lavadora ' . h($M['nombre']) . ' en Colombia</span>", "<span>✔ ' . (($M['tienda'] ?? '') === 'Repuestos para lavadoras' ? 'Repuestos para lavadoras' : 'Filtros para lavadora ' . h($M['nombre'])) . ' en Colombia</span>")
(SALIDA / "marcas.php").write_text(mp, encoding="utf-8")
# robots: los tres sitemaps
rb = (SALIDA / "robots.php").read_text(encoding="utf-8")
if "bombas-de-agua/sitemap" not in rb:
    rb = rb.rstrip() + "\nSitemap: <?= sitio()['base'] ?>/bombas-de-agua/sitemap.xml\nSitemap: <?= sitio()['base'] ?>/mangueras-para-lavadora/sitemap.xml\n"
    (SALIDA / "robots.php").write_text(rb, encoding="utf-8")
(SALIDA / "INSTALAR-tienda-unida.md").write_text(f"""# Tienda unida de repuestos para lavadoras ({DOM})

Un solo zip con TODO el sitio (filtros + bombas + mangueras/presostatos + portada nueva). Las direcciones que ya tenías no cambian.

1. En Hostinger abre el administrador de archivos de {DOM.split('//')[1]}, entra a `public_html`.
2. **Antes de subir**, guarda una copia de `api/config.php` y de la carpeta `data/` (tienen tu correo y tus datos): este zip NO las sobrescribe, pero por si acaso.
3. Sube `tienda-repuestos-lavadoras.zip` y descomprímelo en `public_html` aceptando reemplazar.
4. Search Console: agrega los sitemaps {DOM}/sitemap.xml, {DOM}/bombas-de-agua/sitemap.xml y {DOM}/mangueras-para-lavadora/sitemap.xml.
5. WhatsApp: Samsung {TEL_SAM} · LG {TEL_LG} (mangueras: {TEL_SAM}). Para cambiarlos, edita `bombas.py`, `mangueras.py`, `lavadoras.py` y `tienda_unida.py` y vuelve a generar.
""", encoding="utf-8")
z = AQUI / "tienda-repuestos-lavadoras.zip"
z.unlink(missing_ok=True)
subprocess.run(["zip", "-qr", str(z), ".", "-x", "api/config.php", "-x", "data/pedidos.sqlite*", "-x", "data/correos.log"], cwd=SALIDA, check=True)
n = sum(1 for _ in SALIDA.rglob("index.php"))
print(f"Tienda unida: {SALIDA} ({n} páginas index.php) → {z.name}")
