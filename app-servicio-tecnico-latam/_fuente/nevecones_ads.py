"""Páginas de Google Ads: instalación de nevecones por marca en Cali, Yumbo y Palmira.
Una página completa por marca (modelos, filtro, fábrica de hielo, agua, preguntas) y una página de entrada con las 7 marcas.
Uso: python3 _fuente/nevecones_ads.py [carpeta_vista_previa]   (sin argumento escribe en site/ads/)"""
import json, base64, io, sys, html as H
from pathlib import Path
from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
SITE = RAIZ / "site"
CFG = json.load(open(RAIZ / "config.json", encoding="utf-8"))
TEL = "573013810242"; TELV = "+57 301 381 0242"
CIUDADES = ["Cali", "Yumbo", "Palmira"]
N = {"samsung": "Samsung", "lg": "LG", "whirlpool": "Whirlpool"}

# Datos por marca. Las referencias de filtro son las que figuran en fuentes de venta y fabricantes; siempre se confirma con la etiqueta del modelo.
D = {
 "samsung": dict(
   filtro="Referencia frecuente: DA29-00020B (HAF-CIN/EXP). Se cambia cada 6 meses o cuando se enciende el indicador de cambio de filtro.",
   paso="Se retira el filtro en posición vertical, sin inclinarlo, para no dañar la carcasa."),
 "lg": dict(
   filtro="Referencias frecuentes: LT1000P (ADQ74793501) y LT700P (ADQ36006101). Se cambia cada 6 meses o antes si baja el caudal de agua.",
   paso="Según el modelo, el filtro gira un cuarto de vuelta para soltarse (LT1000P) o se tira hacia abajo y se empuja hacia arriba para fijarlo (LT700P)."),
 "whirlpool": dict(
   filtro="Referencia frecuente: EDR1RXD1 / W10295370A (llamado «Filter 1» en varios modelos). Se cambia cada 6 meses o 200 galones, lo que ocurra primero.",
   paso="El técnico ubica el filtro de tu modelo, lo cambia y deja el sistema purgado."),
}

CSS = """:root{--mc:%(c)s;--mh:%(mh)s;--h1:%(h1)s;--h2:%(h2)s;--ht:%(ht)s;--on:%(on)s;--chb:%(chb)s;--chd:%(chd)s;--ink:#0f172a;--mu:#475569;--panel:#f1f5f9}*{box-sizing:border-box}body{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;color:var(--ink);background:var(--panel);padding-bottom:84px;line-height:1.5}
a{color:inherit}.w{max-width:1080px;margin:0 auto;padding:0 16px}
.top{position:sticky;top:0;z-index:20;background:#fff;box-shadow:0 1px 10px rgba(0,0,0,.08)}.top .w{display:flex;align-items:center;gap:10px;padding:8px 16px}.top img{height:30px}.top .sp{flex:1}
.b{display:inline-flex;align-items:center;justify-content:center;border-radius:14px;padding:13px 20px;font-weight:700;text-decoration:none;border:0;cursor:pointer;font-size:1rem}.wa{background:#25d366;color:#0b2e17}.ll{background:#fff;color:var(--mh);border:2px solid var(--mh)}
.hero{color:var(--ht);background:linear-gradient(120deg,var(--h1),var(--h2))}.hero .w{padding:36px 16px 52px;display:grid;gap:16px;grid-template-columns:1fr}.hero .t{display:grid;gap:16px;align-content:center}.fr{background:#fff;border-radius:18px;padding:14px;display:grid;place-items:center;box-shadow:0 10px 30px rgba(0,0,0,.25)}.fr img{max-height:340px;width:auto;max-width:100%%}@media(min-width:800px){.hero .w{grid-template-columns:1.5fr 1fr;align-items:center}}.foto{width:100%%;height:auto;border-radius:16px;display:block}.hero h1{margin:0;font-size:clamp(1.8rem,5vw,2.9rem);line-height:1.1;max-width:20ch}.hero p{margin:0;font-size:1.1rem;max-width:48ch}
.chips{display:flex;gap:8px;flex-wrap:wrap;list-style:none;margin:0;padding:0}.chips li{background:var(--chb);border:1px solid var(--chd);padding:6px 12px;border-radius:99px;font-size:.88rem;font-weight:600}.cta{display:flex;gap:12px;flex-wrap:wrap}
.card{background:#fff;border-radius:18px;padding:22px;margin:18px 0;box-shadow:0 6px 24px rgba(0,0,0,.06)}.card h2{margin:0 0 12px;font-size:1.35rem;color:var(--mh)}.card h3{margin:14px 0 6px}.sel{margin-top:-30px;position:relative}
.ci{display:flex;gap:10px;flex-wrap:wrap;margin:6px 0 12px}.ci button{border:2px solid #e2e8f0;background:#fff;border-radius:99px;padding:10px 18px;font:inherit;font-weight:700;cursor:pointer}.ci button[aria-pressed=true]{background:var(--mc);border-color:var(--mc);color:var(--on)}
.res{padding:12px 14px;border-radius:12px;background:#ecfdf3;font-weight:600;margin-bottom:12px}
.g{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px}.ben{list-style:none;margin:0;padding:0;display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(250px,1fr))}.ben li{padding-left:28px;position:relative}.ben li::before{content:"✓";position:absolute;left:0;color:#128c4a;font-weight:800}
.f{display:flex;justify-content:space-between;gap:10px;background:var(--panel);border-radius:12px;padding:14px 16px;text-decoration:none;font-weight:600;border:1px solid rgba(0,0,0,.06)}.f::after{content:"→ WhatsApp";font-size:.8rem;color:#128c4a;white-space:nowrap}
.mod{background:var(--panel);border-radius:12px;padding:14px 16px;border:1px solid rgba(0,0,0,.06)}.mod b{display:block}
.st{counter-reset:s;list-style:none;margin:0;padding:0;display:grid;gap:10px}.st li{counter-increment:s;background:var(--panel);border-radius:12px;padding:14px 14px 14px 56px;position:relative}.st li::before{content:counter(s);position:absolute;left:14px;top:12px;width:30px;height:30px;border-radius:50%%;background:var(--mc);color:var(--on);display:grid;place-items:center;font-weight:700}.st b{display:block}
.tw{overflow-x:auto;margin-top:10px}.tw table{width:100%%;border-collapse:collapse;font-size:.92rem}.tw th,.tw td{text-align:left;padding:10px 12px;border-bottom:1px solid #e2e8f0;vertical-align:top}.tw th{background:var(--panel)}.tw tr[hidden]{display:none}
.bus{width:100%%;padding:13px 16px;font:inherit;border:2px solid #cbd5e1;border-radius:12px;margin-top:6px}.bus:focus{outline:0;border-color:var(--mh)}
.note{background:#fff7ed;border-left:4px solid #f59e0b;padding:10px 14px;border-radius:8px;margin:12px 0;font-size:.95rem}
.two{display:grid;gap:18px;grid-template-columns:1fr}@media(min-width:800px){.two{grid-template-columns:1fr 1fr}}
details{border-bottom:1px solid #e2e8f0;padding:12px 0}summary{cursor:pointer;font-weight:700}details p{margin:8px 0 0;color:var(--mu)}
.end{background:linear-gradient(110deg,var(--h1),var(--h2));color:var(--ht);text-align:center}.end h2{color:var(--ht)}.end .cta{justify-content:center;margin-top:14px}
footer{max-width:1080px;margin:0 auto;padding:18px 16px;font-size:.8rem;color:#64748b}
.bar{position:fixed;left:0;right:0;bottom:0;z-index:30;background:#fff;box-shadow:0 -4px 18px rgba(0,0,0,.14);padding:10px 12px;display:flex;gap:10px}.bar .b{flex:1;padding:12px}@media(min-width:900px){.bar{display:none}body{padding-bottom:0}}
"""

CAT = json.load(open(RAIZ.parent / "us-filter-store/_fuente/catalogo_colombia.json", encoding="utf-8"))
PAL = {
 "samsung": dict(c="#1428a0", mh="#1428a0", h1="#0a1a6b", h2="#1428a0", ht="#ffffff", on="#ffffff", chb="rgba(255,255,255,.16)", chd="rgba(255,255,255,.35)"),
 "lg": dict(c="#c8102e", mh="#a50034", h1="#7d0026", h2="#c8102e", ht="#ffffff", on="#ffffff", chb="rgba(255,255,255,.16)", chd="rgba(255,255,255,.4)"),
 "whirlpool": dict(c="#f5b800", mh="#8a6100", h1="#ffd84a", h2="#f5b800", ht="#1f2937", on="#1f2937", chb="rgba(0,0,0,.08)", chd="rgba(0,0,0,.25)"),
 "neutro": dict(c="#0f4c81", mh="#0f4c81", h1="#0b2d54", h2="#0f4c81", ht="#ffffff", on="#ffffff", chb="rgba(255,255,255,.16)", chd="rgba(255,255,255,.35)"),
}
MARCA_CAT = {"samsung": "Samsung", "lg": "LG", "whirlpool": "Whirlpool"}

def tabla_modelos(m):
    """Filas del catálogo propio (referencias de filtro y modelos de nevecón) de la marca."""
    filas = []
    for k, v in CAT.items():
        if v["marca"] != MARCA_CAT[m]: continue
        ext = v.get("ubic") == "externo"
        mod = ", ".join(v.get("modelos") or []) or ("Sirve a nevecones con dispensador de agua; confirma con tu modelo." if ext else "Confirma con la foto del filtro o la etiqueta de tu modelo.")
        filas.append((v["nombre"].replace("Filtro ", "", 1), v["ref"], ", ".join(v.get("alias") or []) or "-", "Externo (va en la manguera del agua)" if ext else "Interno (cartucho dentro del nevecón)", mod))
    return filas

FOTOS = RAIZ.parent
FDIR = RAIZ / "_fuente" / "fotos-nevecones"   # fotos de neveras de otros proyectos, con la marca impresa en el equipo ya borrada
NEVERA = {m: FDIR / f"{m}.jpg" for m in ("samsung", "lg", "whirlpool")}
ALT = {"samsung": "Nevecón Samsung side by side con dispensador de agua", "lg": "Nevecón LG french door con dispensador de agua y hielo", "whirlpool": "Nevecón Whirlpool side by side con dispensador de agua"}
AGUA = FDIR / "agua.jpg"

def b64(path, w, h, fmt="JPEG", q=62):
    im = Image.open(path)
    im = im.convert("RGBA") if fmt == "PNG" else im.convert("RGB")
    im.thumbnail((w, h)); b = io.BytesIO(); im.save(b, fmt, **({"optimize": True} if fmt == "PNG" else {"quality": q}))
    return f"data:image/{fmt.lower()};base64," + base64.b64encode(b.getvalue()).decode()

def slug_marca(m): return f"soporte-tecnico-autorizado-{m}-instalacion-nevecones-cali-yumbo-palmira-colombia"

def pagina_marca(m):
    n = N[m]; d = D[m]
    nev = b64(NEVERA[m], 600, 900, q=85); agua = b64(AGUA, 900, 600, q=70)
    ref = f"ads-nevecones-{m}"
    tipos = [("Side by Side con agua y hielo", "Dos puertas verticales, con dispensador de agua y fábrica de hielo."), ("French Door con agua y hielo", "Puertas dobles arriba y cajón de congelador abajo, con dispensador de agua y fábrica de hielo.")]
    tipos_h = "".join(f'<div class="mod"><b>{H.escape(a)}</b>{H.escape(b)}</div>' for a, b in tipos)
    pasos_filtro = ["Se cierra la llave de agua y se ubica el filtro de tu modelo.", "Se retira el filtro usado (puede salir un poco de agua).", "Se coloca el filtro nuevo hasta que encaje y se cierra la tapa.", "Se purga el sistema dejando correr agua varios minutos para sacar el aire del circuito.", "Se reinicia el indicador de cambio de filtro si tu modelo lo tiene.", "Se revisa que no haya fugas y se anota la fecha del próximo cambio."]
    filas = tabla_modelos(m)
    filas_h = "".join("<tr>" + "".join(f"<td>{H.escape(c)}</td>" for c in f) + "</tr>" for f in filas)
    ejemplo = next((f[4].split(",")[0] for f in filas if f[4].startswith(("RF", "RS", "L", "W", "G"))), filas[0][1])
    pf = "".join(f"<li>{H.escape(x)}</li>" for x in pasos_filtro)
    pasos_hielo = [("Conexión de agua", "Manguera hasta la entrada de agua del nevecón, con llave de paso accesible y sin dobleces."), ("Encendido de la fábrica", "Se activa la fábrica de hielo según tu modelo y se confirma que quede funcionando."), ("Purga", "Se deja correr agua para eliminar el aire de la línea antes de la primera producción."), ("Primeras tandas", "Normalmente las primeras 24 horas el hielo sale poco; se desechan los primeros cubos. El manual de tu modelo confirma los tiempos.")]
    ph = "".join(f"<li><b>{H.escape(a)}</b>{H.escape(b)}</li>" for a, b in pasos_hielo)
    necesidades = ["Instalar mi nevecón", "Instalar o cambiar el filtro de agua", "Instalar la fábrica de hielo", "Conectar el agua y el dispensador", "Se prendió la luz del filtro", "Reinstalar mi nevecón en una mudanza"]
    faq = [(f"¿Cuánto cuesta la instalación de un nevecón {n}?", "Depende de si solo se ubica y conecta o si también necesita conexión de agua, filtro y accesorios. El costo se informa en COP antes de empezar."),
           (f"¿Qué filtro necesita mi nevecón {n}?", d["filtro"] + " Las referencias dependen del modelo: confirma con la etiqueta antes de comprar."),
           ("¿Instalan la fábrica de hielo y la conexión de agua?", "Sí: se conecta el agua con manguera y llave de paso, se purga la línea, se activa la fábrica de hielo y se comprueba que produzca."),
           ("¿Por qué no sale hielo después de instalar?", "Normalmente las primeras 24 horas la producción es baja y los primeros cubos se desechan. Si pasan 24 horas y no hay hielo, escríbenos."),
           ("¿Cada cuánto se cambia el filtro del nevecón?", "Normalmente cada 6 meses, o antes si se enciende la luz del filtro o baja el caudal de agua."),
           ("¿Cuánto demora la instalación?", "Suele tomar entre 1 y 2 horas según el modelo y si hay que hacer la conexión de agua."),
           ("¿Pueden instalar mi nevecón en una mudanza?", "Sí. Indica la dirección de entrega, el modelo y si hay conexión de agua lista."),
           ("¿Atienden en Cali, Yumbo y Palmira?", "Sí, atendemos las tres ciudades y sus barrios cercanos. Escribe tu barrio por WhatsApp para confirmar el horario.")]
    faq_h = "".join(f"<details><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>" for q, a in faq)
    ver = f'<meta name="google-site-verification" content="{CFG["verificacion_gsc"]}">' if CFG.get("verificacion_gsc") else ""
    css = CSS % PAL[m]
    h1 = f"Instalación de nevecones {n} en Cali, Yumbo y Palmira"
    return f'''<!doctype html><html lang="es-CO"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Instalación de nevecones {n} en Cali, Yumbo y Palmira</title>
<meta name="description" content="Instalación de nevecones {n} en Cali, Yumbo y Palmira: modelos, instalación del filtro de agua, fábrica de hielo y conexión de agua. Costo antes de empezar.">
<meta name="robots" content="noindex,follow">{ver}<link rel="canonical" href="https://soporte-tecnico-autorizado.com/ads/{slug_marca(m)}/"><style>{css}</style></head><body>
<header class="top"><div class="w"><b>Instalación de nevecones {n}</b><span class="sp"></span><a class="b ll" data-e="llamar" href="tel:+{TEL}">Llamar</a><a class="b wa" data-e="whatsapp" data-wa href="#">WhatsApp</a></div></header>
<section class="hero"><div class="w"><div class="t"><h1>{h1}</h1><p>Instalamos tu nevecón {n} con conexión de agua, filtro y fábrica de hielo. Te damos el costo antes de empezar.</p>
<ul class="chips"><li>A domicilio</li><li>Filtro de agua</li><li>Fábrica de hielo</li><li>Costo antes de empezar</li></ul>
<div class="cta"><a class="b wa" data-e="whatsapp" data-wa href="#">Escribir por WhatsApp</a><a class="b ll" data-e="llamar" href="tel:+{TEL}">Llamar {TELV}</a></div></div><div class="fr"><img src="{nev}" alt="{ALT[m]}" width="300" height="540"></div></div></section>
<main class="w">
<section class="card sel"><h2>Elige tu ciudad</h2><div class="ci" id="ci">{"".join(f'<button type="button" data-c="{c}" aria-pressed="false">{c}</button>' for c in CIUDADES)}</div><div class="res" id="res">Selecciona tu ciudad para pedir la instalación.</div><a class="b wa" data-e="whatsapp" data-wa href="#">Pedir instalación por WhatsApp</a></section>
<section class="card"><h2>¿Qué necesitas para tu nevecón {n}?</h2><div class="g" id="need"></div></section>
<section class="card"><h2>Modelos de nevecones {n} que instalamos</h2><div class="two"><div><p>Instalamos nevecones {n} con dispensador de agua y fábrica de hielo, como los side by side y los french door. Abajo puedes buscar la referencia de tu modelo.</p></div><div class="fr"><img src="{nev}" alt="{ALT[m]}" width="300" height="540" style="max-height:300px"></div></div><p style="margin-top:12px">Escríbenos con el modelo de tu nevecón {n} (etiqueta dentro del compartimento) y te confirmamos la instalación y el filtro que necesita.</p></section>
<section class="card"><h2>Encuentra la referencia de tu nevecón {n}</h2><p>Escribe el modelo de tu nevecón (etiqueta dentro del compartimento) o la referencia del filtro, y te mostramos cuál le corresponde.</p>
<input class="bus" id="bus" type="search" placeholder="Ej. {ejemplo}" autocomplete="off" aria-label="Buscar modelo o referencia"><div class="tw"><table><thead><tr><th>Filtro</th><th>Referencia</th><th>También se conoce como</th><th>Ubicación</th><th>Modelos de nevecón (ejemplos)</th></tr></thead><tbody id="tb">{filas_h}</tbody></table></div>
<p id="nada" class="note" hidden>No aparece ese modelo en la lista. Escríbenos con la etiqueta de tu nevecón y te confirmamos el filtro y la instalación. <a href="#" data-wa-q="1" data-e="whatsapp" style="font-weight:700">Escribir mi modelo por WhatsApp</a></p>
<p style="font-size:.9rem;color:var(--mu)">Son ejemplos de modelos. Si el tuyo no está, escríbenos con la etiqueta y lo confirmamos.</p></section>
<section class="card"><h2>Instalación del filtro de agua del nevecón {n}</h2><p>{H.escape(d["filtro"])}</p><div class="note">Son referencias frecuentes. Cada modelo puede usar una distinta: confirma con la etiqueta de tu nevecón o escríbenos con el modelo y te decimos cuál necesita.</div>
<div class="two"><div><h3>Cómo se instala</h3><ol class="st">{pf}</ol></div><div><h3>Detalle de tu marca</h3><p>{H.escape(d["paso"])}</p><h3>¿Cuándo cambiarlo?</h3><p>Normalmente cada 6 meses, o antes si se enciende la luz del filtro, si baja el caudal de agua o si el agua y el hielo cambian de sabor.</p><p><a class="b wa" data-e="whatsapp" data-wa-s="Instalar o cambiar el filtro de agua" href="#">Consultar mi filtro por WhatsApp</a></p></div></div></section>
<section class="card"><h2>Instalación de la fábrica de hielo del nevecón {n}</h2><p>El técnico activa la fábrica de hielo según tu modelo y comprueba que entre agua y que produzca hielo.</p><ol class="st">{ph}</ol></section>
<section class="card"><h2>Conexión de agua y dispensador</h2><div class="two"><img class="foto" src="{agua}" alt="Persona sirviéndose agua del dispensador de un nevecón" width="900" height="600"><ul class="ben"><li>Manguera de agua sin dobleces ni aplastamientos detrás del equipo.</li><li>Llave de paso accesible para cerrar el agua cuando haga falta.</li><li>Presión de agua suficiente: si es muy baja, el dispensador sale lento y el hielo sale pequeño.</li><li>Purga del sistema antes de tomar el primer vaso de agua.</li><li>Revisión de fugas en las uniones al terminar.</li><li>Prueba del dispensador de agua y de hielo con el equipo funcionando.</li></ul></div></section>
<section class="card"><h2>Qué incluye la instalación de tu nevecón {n}</h2><ul class="ben"><li>Revisión del lugar: espacio, piso firme y ventilación a los lados y atrás.</li><li>Nivelación del equipo con las patas ajustables.</li><li>Conexión a un tomacorriente con tierra, sin extensiones ni regletas.</li><li>Conexión de agua, filtro y fábrica de hielo.</li><li>Ajuste de la temperatura y verificación del enfriamiento.</li><li>Explicación del uso básico y del cambio de filtro.</li></ul>
<h3>Antes de la visita</h3><ul class="ben"><li>Mide el espacio y la puerta de entrada para que el equipo pase.</li><li>Si el nevecón viajó acostado, déjalo reposar de pie varias horas antes de conectarlo; confirma el tiempo en el manual.</li><li>Ten un tomacorriente con tierra cerca y una llave de agua accesible.</li><li>Limpia el interior con un paño húmedo antes de usarlo.</li></ul></section>
<section class="card"><h2>Preguntas frecuentes sobre la instalación de nevecones {n}</h2>{faq_h}</section>
<section class="card end"><h2>¿Necesitas instalar tu nevecón {n}?</h2><p>Escríbenos y te respondemos con horario y costo antes de empezar.</p><div class="cta"><a class="b wa" data-e="whatsapp" data-wa href="#">WhatsApp {TELV}</a><a class="b ll" data-e="llamar" href="tel:+{TEL}">Llamar</a></div></section>
</main><footer>Servicio técnico independiente. {n} y su logotipo pertenecen a sus respectivos propietarios; este sitio no está afiliado ni patrocinado por {n}.</footer>
<div class="bar"><a class="b wa" data-e="whatsapp" data-wa href="#">WhatsApp</a><a class="b ll" data-e="llamar" href="tel:+{TEL}">Llamar</a></div>
<script>var M="{n}",R="{ref}",NUM="{TEL}",ciudad="",NEC={json.dumps(necesidades, ensure_ascii=False)};
function msg(x){{var t="Hola, necesito instalación de nevecón "+M+(ciudad?" en "+ciudad:" en Cali, Yumbo o Palmira")+(x?". Servicio: "+x:"")+" ["+R+(ciudad?"-"+ciudad.toLowerCase():"")+"]";return "https://wa.me/"+NUM+"?text="+encodeURIComponent(t);}}
function pintar(){{document.querySelectorAll("[data-wa]").forEach(function(a){{a.href=msg();}});document.querySelectorAll("[data-wa-s]").forEach(function(a){{a.href=msg(a.getAttribute("data-wa-s"));}});
document.getElementById("need").innerHTML=NEC.map(function(x){{return '<a class="f" data-e="whatsapp" href="'+msg(x)+'">'+x+'</a>';}}).join("");
document.getElementById("res").textContent=ciudad?"Instalación de nevecón "+M+" en "+ciudad+": toca el botón y te respondemos con horario y costo.":"Selecciona tu ciudad para pedir la instalación.";
document.querySelectorAll("#ci button").forEach(function(b){{b.setAttribute("aria-pressed",b.dataset.c===ciudad);}});}}
var bus=document.getElementById("bus");function norm(t){{return t.toLowerCase().replace(/[^a-z0-9]/g,"");}}
bus.addEventListener("input",function(){{var q=norm(bus.value),rows=document.querySelectorAll("#tb tr"),n=0;rows.forEach(function(r){{var ok=!q||norm(r.textContent).indexOf(q)>-1;r.hidden=!ok;if(ok)n++;}});document.getElementById("nada").hidden=!(q&&n===0);var a=document.querySelector("[data-wa-q]");if(a)a.href=msg("Mi modelo es "+bus.value);}});
document.getElementById("ci").addEventListener("click",function(e){{var b=e.target.closest("button");if(b){{ciudad=b.dataset.c;pintar();}}}});
document.addEventListener("click",function(e){{var a=e.target.closest("[data-e]");if(!a)return;window.dataLayer=window.dataLayer||[];window.dataLayer.push({{event:a.dataset.e,marca:M,ciudad:ciudad,landing:R}});}});pintar();</script></body></html>'''

def pagina_entrada(enlace):
    """enlace(m) -> dirección de la página de cada marca."""
    ver = f'<meta name="google-site-verification" content="{CFG["verificacion_gsc"]}">' if CFG.get("verificacion_gsc") else ""
    css = CSS % PAL["neutro"]
    tarj = "".join(f'<a class="mk" href="{enlace(m)}" style="border-top:6px solid {PAL[m]['c']}"><img src="{b64(NEVERA[m], 300, 450, q=80)}" alt="{ALT[m]}"><b>Nevecones {N[m]}</b><span>Filtro, hielo y agua</span></a>' for m in N)
    extra = ".mk{display:grid;place-items:center;gap:6px;text-align:center;background:#fff;border:2px solid #e2e8f0;border-radius:16px;padding:18px 10px;text-decoration:none;min-height:260px}.mk:hover{border-color:var(--mc)}.mk img{max-height:170px;width:auto;max-width:90%}.mk span{font-size:.85rem;color:var(--mu)}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}"
    return f'''<!doctype html><html lang="es-CO"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Instalación de nevecones por marca en Cali, Yumbo y Palmira</title><meta name="description" content="Instalación de nevecones por marca en Cali, Yumbo y Palmira: filtro de agua, fábrica de hielo y conexión de agua. Elige tu marca.">
<meta name="robots" content="noindex,follow">{ver}<style>{css}{extra}</style></head><body>
<header class="top"><div class="w"><b style="flex:1">Instalación de nevecones · Cali, Yumbo y Palmira</b><a class="b ll" href="tel:+{TEL}">Llamar</a><a class="b wa" href="https://wa.me/{TEL}?text=Hola%2C%20necesito%20instalaci%C3%B3n%20de%20nevec%C3%B3n">WhatsApp</a></div></header>
<section class="hero"><div class="w"><div class="t"><h1>Instalación de nevecones por marca en Cali, Yumbo y Palmira</h1><p>Elige la marca de tu nevecón y ve la instalación del filtro, la fábrica de hielo y la conexión de agua.</p></div></div></section>
<main class="w"><section class="card sel"><h2>Elige la marca de tu nevecón</h2><div class="grid">{tarj}</div></section></main>
<footer>Servicio técnico independiente. Las marcas y sus logotipos pertenecen a sus respectivos propietarios; este sitio no está afiliado ni patrocinado por ellas.</footer></body></html>'''

def csv_anuncios():
    import csv
    filas = []
    for m, n in N.items():
        for c in CIUDADES:
            url = f"https://soporte-tecnico-autorizado.com/ads/{slug_marca(m)}/"
            kws = [f"instalación de nevecón {n} {c}", f"instalar filtro nevecón {n} {c}", f"instalación fábrica de hielo {n} {c}", f"instalación de nevecones por marca {c}"]
            filas.append([n, "Colombia", c, "nevecones", url, f"Instalación Nevecón {n}"[:30], "Filtro, Hielo y Agua", c, f"Instalación de nevecón {n} en {c} con agua y filtro. Costo antes de empezar."[:90], "Escríbenos por WhatsApp y recibe horario y costo antes de empezar."[:90], " | ".join(kws)])
    dest = RAIZ / "entrega"; dest.mkdir(exist_ok=True)
    with open(dest / "anuncios-nevecones-google-ads.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["Marca", "País", "Ciudad", "Equipo", "URL final", "Título 1", "Título 2", "Título 3", "Descripción 1", "Descripción 2", "Palabras clave sugeridas (concordancia de frase)"]); w.writerows(filas)

if __name__ == "__main__":
    prev = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    base = prev if prev else SITE / "ads"
    for m in N:
        d = base / slug_marca(m); d.mkdir(parents=True, exist_ok=True); (d / "index.html").write_text(pagina_marca(m), encoding="utf-8")
    entrada = pagina_entrada((lambda m: f"{slug_marca(m)}/index.html") if prev else (lambda m: f"/ads/{slug_marca(m)}/"))
    if prev: (prev / "index.html").write_text(entrada, encoding="utf-8")
    else:
        d = base / "instalacion-nevecones-por-marca-cali-yumbo-palmira"; d.mkdir(parents=True, exist_ok=True); (d / "index.html").write_text(entrada, encoding="utf-8")
    if not prev: csv_anuncios()
    print("páginas de nevecones por marca:", len(N), "+ entrada")
