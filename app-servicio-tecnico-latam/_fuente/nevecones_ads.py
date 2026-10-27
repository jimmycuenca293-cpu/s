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
N = {"samsung": "Samsung", "lg": "LG", "whirlpool": "Whirlpool", "mabe": "Mabe", "frigidaire": "Frigidaire", "electrolux": "Electrolux", "general-electric": "General Electric"}

# Datos por marca. Las referencias de filtro son las que figuran en fuentes de venta y fabricantes; siempre se confirma con la etiqueta del modelo.
D = {
 "samsung": dict(
   lineas=["Family Hub: pantalla táctil y conexión Wi-Fi (SmartThings).", "Twin Cooling Plus: dos sistemas de frío independientes.", "Digital Inverter: compresor de velocidad variable.", "Bespoke: acabados y módulos personalizables."],
   filtro="Referencia frecuente: DA29-00020B (HAF-CIN/EXP). Se cambia cada 6 meses o cuando se enciende el indicador de cambio de filtro.",
   paso="Se retira el filtro en posición vertical, sin inclinarlo, para no dañar la carcasa; algunos modelos piden quitar primero los estantes que quedan encima.",
   hielo="En muchos modelos Samsung la fábrica de hielo tiene un interruptor o ícono de encendido en el panel; el técnico lo activa y verifica la producción."),
 "lg": dict(
   lineas=["InstaView Door-in-Door: ventana que se ilumina al tocarla.", "Linear Inverter: compresor de velocidad variable.", "ThinQ: control y diagnóstico desde el celular.", "Craft Ice: hielo en esferas, en modelos que lo incluyen."],
   filtro="Referencias frecuentes: LT1000P (ADQ74793501) y LT700P (ADQ36006101). Se cambia cada 6 meses o antes si baja el caudal de agua.",
   paso="Según el modelo, el filtro gira un cuarto de vuelta para soltarse (LT1000P) o se tira hacia abajo y se empuja hacia arriba para fijarlo (LT700P); el técnico lo hace con el filtro correcto de tu equipo.",
   hielo="Los modelos con fábrica de hielo LG suelen traer un interruptor de encendido; el técnico lo activa y confirma que entre agua y baje el hielo."),
 "whirlpool": dict(
   lineas=["Side by Side con dispensador de agua y hielo.", "French Door con cajón de congelador inferior.", "6th Sense: sensores que ajustan la temperatura, en modelos que lo incluyen.", "Modelos con compresor inverter."],
   filtro="Referencia frecuente: EDR1RXD1 / W10295370A (llamado «Filter 1» en varios modelos). Se cambia cada 6 meses o 200 galones, lo que ocurra primero.",
   paso="Cada modelo trae el filtro en un lugar distinto (base, pared del compartimento o dispensador); el técnico lo ubica, lo cambia y deja el sistema purgado.",
   hielo="La fábrica de hielo se enciende con un brazo o un interruptor según el modelo; el técnico lo deja activo y comprueba la producción."),
 "mabe": dict(
   lineas=["Side by Side con dispensador de agua.", "French Door.", "Modelos con compresor inverter.", "Congelador superior e inferior."],
   filtro="Te confirmamos la referencia exacta con el modelo de tu nevecón: escríbenos con la etiqueta y te decimos cuál filtro necesita. Se cambia normalmente cada 6 meses.",
   paso="El técnico ubica el filtro de tu modelo, lo cambia y deja el sistema purgado.",
   hielo="El técnico activa la fábrica de hielo y comprueba que entre agua y baje el hielo."),
 "frigidaire": dict(
   lineas=["Gallery: línea de gama media con dispensador.", "Professional: línea de gama alta.", "Side by Side con agua y hielo en la puerta.", "French Door."],
   filtro="Varios modelos usan filtros de la familia PureSource; confirmamos la referencia exacta con la etiqueta de tu modelo. Se cambia cada 6 meses o cuando se enciende la luz del filtro.",
   paso="El técnico ubica el filtro de tu modelo (dentro del compartimento o en la base), lo cambia y purga el sistema.",
   hielo="El técnico activa la fábrica de hielo y confirma la producción."),
 "electrolux": dict(
   lineas=["Side by Side con dispensador de agua y hielo.", "French Door.", "Frost Free: sin escarcha.", "Modelos con compresor inverter."],
   filtro="Referencia frecuente en varios modelos: EPTWFU01. Se cambia cada 6 meses o cuando se enciende la luz del filtro.",
   paso="El técnico ubica el filtro de tu modelo, lo cambia y deja el sistema purgado.",
   hielo="El técnico activa la fábrica de hielo y comprueba que produzca."),
 "general-electric": dict(
   lineas=["GE Profile: línea de gama alta con dispensador.", "GE Café: acabados premium.", "Side by Side GE con agua y hielo.", "French Door GE."],
   filtro="Referencia frecuente: MWF (filtro interno). Se cambia cada 6 meses o cuando se enciende la luz del filtro.",
   paso="El filtro MWF va dentro del compartimento; el técnico lo cambia y purga el sistema.",
   hielo="El técnico activa la fábrica de hielo y comprueba que produzca."),
}

CSS = """:root{--mc:%(c)s;--ink:#0f172a;--mu:#475569;--panel:#f1f5f9}*{box-sizing:border-box}body{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;color:var(--ink);background:var(--panel);padding-bottom:84px;line-height:1.5}
a{color:inherit}.w{max-width:1080px;margin:0 auto;padding:0 16px}
.top{position:sticky;top:0;z-index:20;background:#fff;box-shadow:0 1px 10px rgba(0,0,0,.08)}.top .w{display:flex;align-items:center;gap:10px;padding:8px 16px}.top img{height:30px}.top .sp{flex:1}
.b{display:inline-flex;align-items:center;justify-content:center;border-radius:14px;padding:13px 20px;font-weight:700;text-decoration:none;border:0;cursor:pointer;font-size:1rem}.wa{background:#25d366;color:#0b2e17}.ll{background:#fff;color:var(--mc);border:2px solid var(--mc)}
.hero{color:#fff;background:linear-gradient(110deg,color-mix(in srgb,var(--mc) 92%%,#000),color-mix(in srgb,var(--mc) 70%%,transparent)),url(%(hero)s) center/cover}.hero .w{padding:36px 16px 52px;display:grid;gap:16px}.hero h1{margin:0;font-size:clamp(1.8rem,5vw,2.9rem);line-height:1.1;max-width:20ch}.hero p{margin:0;font-size:1.1rem;max-width:48ch}
.chips{display:flex;gap:8px;flex-wrap:wrap;list-style:none;margin:0;padding:0}.chips li{background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.35);padding:6px 12px;border-radius:99px;font-size:.88rem;font-weight:600}.cta{display:flex;gap:12px;flex-wrap:wrap}
.card{background:#fff;border-radius:18px;padding:22px;margin:18px 0;box-shadow:0 6px 24px rgba(0,0,0,.06)}.card h2{margin:0 0 12px;font-size:1.35rem;color:var(--mc)}.card h3{margin:14px 0 6px}.sel{margin-top:-30px;position:relative}
.ci{display:flex;gap:10px;flex-wrap:wrap;margin:6px 0 12px}.ci button{border:2px solid #e2e8f0;background:#fff;border-radius:99px;padding:10px 18px;font:inherit;font-weight:700;cursor:pointer}.ci button[aria-pressed=true]{background:var(--mc);border-color:var(--mc);color:#fff}
.res{padding:12px 14px;border-radius:12px;background:#ecfdf3;font-weight:600;margin-bottom:12px}
.g{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px}.ben{list-style:none;margin:0;padding:0;display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(250px,1fr))}.ben li{padding-left:28px;position:relative}.ben li::before{content:"✓";position:absolute;left:0;color:#128c4a;font-weight:800}
.f{display:flex;justify-content:space-between;gap:10px;background:var(--panel);border-radius:12px;padding:14px 16px;text-decoration:none;font-weight:600;border:1px solid rgba(0,0,0,.06)}.f::after{content:"→ WhatsApp";font-size:.8rem;color:#128c4a;white-space:nowrap}
.mod{background:var(--panel);border-radius:12px;padding:14px 16px;border:1px solid rgba(0,0,0,.06)}.mod b{display:block}
.st{counter-reset:s;list-style:none;margin:0;padding:0;display:grid;gap:10px}.st li{counter-increment:s;background:var(--panel);border-radius:12px;padding:14px 14px 14px 56px;position:relative}.st li::before{content:counter(s);position:absolute;left:14px;top:12px;width:30px;height:30px;border-radius:50%%;background:var(--mc);color:#fff;display:grid;place-items:center;font-weight:700}.st b{display:block}
.note{background:#fff7ed;border-left:4px solid #f59e0b;padding:10px 14px;border-radius:8px;margin:12px 0;font-size:.95rem}
.two{display:grid;gap:18px;grid-template-columns:1fr}@media(min-width:800px){.two{grid-template-columns:1fr 1fr}}
details{border-bottom:1px solid #e2e8f0;padding:12px 0}summary{cursor:pointer;font-weight:700}details p{margin:8px 0 0;color:var(--mu)}
.end{background:linear-gradient(110deg,var(--mc),color-mix(in srgb,var(--mc) 60%%,#000));color:#fff;text-align:center}.end h2{color:#fff}.end .cta{justify-content:center;margin-top:14px}
footer{max-width:1080px;margin:0 auto;padding:18px 16px;font-size:.8rem;color:#64748b}
.bar{position:fixed;left:0;right:0;bottom:0;z-index:30;background:#fff;box-shadow:0 -4px 18px rgba(0,0,0,.14);padding:10px 12px;display:flex;gap:10px}.bar .b{flex:1;padding:12px}@media(min-width:900px){.bar{display:none}body{padding-bottom:0}}
"""

def b64(path, w, h, fmt="JPEG", q=62):
    im = Image.open(path)
    im = im.convert("RGBA") if fmt == "PNG" else im.convert("RGB")
    im.thumbnail((w, h)); b = io.BytesIO(); im.save(b, fmt, **({"optimize": True} if fmt == "PNG" else {"quality": q}))
    return f"data:image/{fmt.lower()};base64," + base64.b64encode(b.getvalue()).decode()

def slug_marca(m): return f"soporte-tecnico-autorizado-{m}-instalacion-nevecones-cali-yumbo-palmira-colombia"

def pagina_marca(m):
    n = N[m]; d = D[m]; color = CFG["marcas"][m]["color"]
    hero = b64(SITE / "img" / m / "tecnico-3.jpg" if (SITE / "img" / m / "tecnico-3.jpg").exists() else SITE / "img" / m / "tecnico-0.jpg", 1200, 700)
    logo = b64(SITE / "img" / m / "logo.png", 220, 70, "PNG")
    ref = f"ads-nevecones-{m}"
    lineas = "".join(f"<li>{H.escape(x)}</li>" for x in d["lineas"])
    tipos = [("Side by Side", "Dos puertas verticales: nevera a un lado y congelador al otro."), ("French Door", "Puertas dobles arriba y cajón de congelador abajo."), ("Con dispensador de agua y hielo", "Agua fría y hielo en la puerta; requiere conexión de agua y filtro."), ("Congelador superior o inferior", "Modelos de menor tamaño que también se instalan y conectan."), ("Compresor inverter", "Menor ruido y consumo; se nivela y se conecta igual que los demás.")]
    tipos_h = "".join(f'<div class="mod"><b>{H.escape(a)}</b>{H.escape(b)}</div>' for a, b in tipos)
    pasos_filtro = ["Se cierra la llave de agua y se ubica el filtro de tu modelo.", "Se retira el filtro usado (puede salir un poco de agua).", "Se coloca el filtro nuevo hasta que encaje y se cierra la tapa.", "Se purga el sistema dejando correr agua varios minutos para sacar el aire y el polvo del carbón.", "Se reinicia el indicador de cambio de filtro si tu modelo lo tiene.", "Se revisa que no haya fugas y se anota la fecha del próximo cambio."]
    pf = "".join(f"<li>{H.escape(x)}</li>" for x in pasos_filtro)
    pasos_hielo = [("Conexión de agua", "Manguera hasta la entrada de agua del nevecón, con llave de paso accesible y sin dobleces."), ("Encendido de la fábrica", "Se activa la fábrica de hielo y se confirma que el brazo o el sensor estén en posición de trabajo."), ("Purga", "Se deja correr agua para eliminar el aire de la línea antes de la primera producción."), ("Primeras tandas", "Normalmente las primeras 24 horas el hielo sale poco; se desechan los primeros cubos. El manual de tu modelo confirma los tiempos.")]
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
    css = CSS % dict(c=color, hero=hero)
    h1 = f"Instalación de nevecones {n} en Cali, Yumbo y Palmira"
    return f'''<!doctype html><html lang="es-CO"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Instalación de nevecones {n} en Cali, Yumbo y Palmira</title>
<meta name="description" content="Instalación de nevecones {n} en Cali, Yumbo y Palmira: modelos, instalación del filtro de agua, fábrica de hielo y conexión de agua. Costo antes de empezar.">
<meta name="robots" content="noindex,follow">{ver}<link rel="canonical" href="https://soporte-tecnico-autorizado.com/ads/{slug_marca(m)}/"><style>{css}</style></head><body>
<header class="top"><div class="w"><img src="{logo}" alt="Logo {n}"><span class="sp"></span><a class="b ll" data-e="llamar" href="tel:+{TEL}">Llamar</a><a class="b wa" data-e="whatsapp" data-wa href="#">WhatsApp</a></div></header>
<section class="hero"><div class="w"><h1>{h1}</h1><p>Instalamos tu nevecón {n} con conexión de agua, filtro y fábrica de hielo. Te damos el costo antes de empezar.</p>
<ul class="chips"><li>A domicilio</li><li>Filtro de agua</li><li>Fábrica de hielo</li><li>Costo antes de empezar</li></ul>
<div class="cta"><a class="b wa" data-e="whatsapp" data-wa href="#">Escribir por WhatsApp</a><a class="b ll" data-e="llamar" href="tel:+{TEL}">Llamar {TELV}</a></div></div></section>
<main class="w">
<section class="card sel"><h2>Elige tu ciudad</h2><div class="ci" id="ci">{"".join(f'<button type="button" data-c="{c}" aria-pressed="false">{c}</button>' for c in CIUDADES)}</div><div class="res" id="res">Selecciona tu ciudad para pedir la instalación.</div><a class="b wa" data-e="whatsapp" data-wa href="#">Pedir instalación por WhatsApp</a></section>
<section class="card"><h2>¿Qué necesitas para tu nevecón {n}?</h2><div class="g" id="need"></div></section>
<section class="card"><h2>Modelos de nevecones {n} que instalamos</h2><div class="g">{tipos_h}</div><h3>Líneas y tecnologías {n} frecuentes</h3><ul class="ben">{lineas}</ul></section>
<section class="card"><h2>Instalación del filtro de agua del nevecón {n}</h2><p>{H.escape(d["filtro"])}</p><div class="note">Son referencias frecuentes. Cada modelo puede usar una distinta: confirma con la etiqueta de tu nevecón o escríbenos con el modelo y te decimos cuál necesita.</div>
<div class="two"><div><h3>Cómo se instala</h3><ol class="st">{pf}</ol></div><div><h3>Detalle de tu marca</h3><p>{H.escape(d["paso"])}</p><h3>¿Cuándo cambiarlo?</h3><p>Normalmente cada 6 meses, o antes si se enciende la luz del filtro, si baja el caudal de agua o si el agua y el hielo cambian de sabor.</p><p><a class="b wa" data-e="whatsapp" data-wa-s="Instalar o cambiar el filtro de agua" href="#">Consultar mi filtro por WhatsApp</a></p></div></div></section>
<section class="card"><h2>Instalación de la fábrica de hielo del nevecón {n}</h2><p>{H.escape(d["hielo"])}</p><ol class="st">{ph}</ol></section>
<section class="card"><h2>Conexión de agua y dispensador</h2><ul class="ben"><li>Manguera de agua sin dobleces ni aplastamientos detrás del equipo.</li><li>Llave de paso accesible para cerrar el agua cuando haga falta.</li><li>Presión de agua suficiente: si es muy baja, el dispensador sale lento y el hielo sale pequeño.</li><li>Purga del sistema antes de tomar el primer vaso de agua.</li><li>Revisión de fugas en las uniones al terminar.</li><li>Prueba del dispensador de agua y de hielo con el equipo funcionando.</li></ul></section>
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
document.getElementById("ci").addEventListener("click",function(e){{var b=e.target.closest("button");if(b){{ciudad=b.dataset.c;pintar();}}}});
document.addEventListener("click",function(e){{var a=e.target.closest("[data-e]");if(!a)return;window.dataLayer=window.dataLayer||[];window.dataLayer.push({{event:a.dataset.e,marca:M,ciudad:ciudad,landing:R}});}});pintar();</script></body></html>'''

def pagina_entrada(enlace):
    """enlace(m) -> dirección de la página de cada marca."""
    ver = f'<meta name="google-site-verification" content="{CFG["verificacion_gsc"]}">' if CFG.get("verificacion_gsc") else ""
    hero = b64(SITE / "img" / "samsung" / "tecnico-3.jpg", 1200, 700)
    css = CSS % dict(c="#0f4c81", hero=hero)
    tarj = "".join(f'<a class="mk" href="{enlace(m)}" style="--c:{CFG["marcas"][m]["color"]}"><img src="{b64(SITE / "img" / m / "logo.png", 220, 70, "PNG")}" alt="{N[m]}"><b>Nevecones {N[m]}</b><span>Modelos, filtro, hielo y agua</span></a>' for m in N)
    extra = ".mk{display:grid;place-items:center;gap:6px;text-align:center;background:#fff;border:2px solid #e2e8f0;border-radius:16px;padding:18px 10px;text-decoration:none;min-height:150px}.mk:hover{border-color:var(--c)}.mk img{max-height:34px;max-width:80%}.mk span{font-size:.85rem;color:var(--mu)}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}"
    return f'''<!doctype html><html lang="es-CO"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Instalación de nevecones por marca en Cali, Yumbo y Palmira</title><meta name="description" content="Instalación de nevecones por marca en Cali, Yumbo y Palmira: filtro de agua, fábrica de hielo y conexión de agua. Elige tu marca.">
<meta name="robots" content="noindex,follow">{ver}<style>{css}{extra}</style></head><body>
<header class="top"><div class="w"><b style="flex:1">Instalación de nevecones · Cali, Yumbo y Palmira</b><a class="b ll" href="tel:+{TEL}">Llamar</a><a class="b wa" href="https://wa.me/{TEL}?text=Hola%2C%20necesito%20instalaci%C3%B3n%20de%20nevec%C3%B3n">WhatsApp</a></div></header>
<section class="hero"><div class="w"><h1>Instalación de nevecones por marca en Cali, Yumbo y Palmira</h1><p>Elige la marca de tu nevecón y ve los modelos, la instalación del filtro, la fábrica de hielo y la conexión de agua.</p></div></section>
<main class="w"><section class="card sel"><h2>Elige la marca de tu nevecón</h2><div class="grid">{tarj}</div></section></main>
<footer>Servicio técnico independiente. Las marcas y sus logotipos pertenecen a sus respectivos propietarios; este sitio no está afiliado ni patrocinado por ellas.</footer></body></html>'''

if __name__ == "__main__":
    prev = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    base = prev if prev else SITE / "ads"
    for m in N:
        d = base / slug_marca(m); d.mkdir(parents=True, exist_ok=True); (d / "index.html").write_text(pagina_marca(m), encoding="utf-8")
    entrada = pagina_entrada((lambda m: f"{slug_marca(m)}/index.html") if prev else (lambda m: f"/ads/{slug_marca(m)}/"))
    if prev: (prev / "index.html").write_text(entrada, encoding="utf-8")
    else:
        d = base / "instalacion-nevecones-por-marca-cali-yumbo-palmira"; d.mkdir(parents=True, exist_ok=True); (d / "index.html").write_text(entrada, encoding="utf-8")
    print("páginas de nevecones por marca:", len(N), "+ entrada")
