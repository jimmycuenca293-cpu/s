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

CSS2 = """
html{scroll-behavior:smooth}.sr{position:absolute;left:-9999px}
.trust{background:#fff;border-bottom:1px solid #e2e8f0}.trust .w{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;padding:14px 16px}.tr{display:flex;align-items:center;gap:10px;font-weight:600;font-size:.92rem}.tr svg{flex:none;width:30px;height:30px;color:var(--mh)}
.nav{position:sticky;top:51px;z-index:15;background:#fff;border-bottom:1px solid #e2e8f0;overflow-x:auto;white-space:nowrap}.nav .w{display:flex;gap:6px;padding:8px 16px}.nav a{flex:none;text-decoration:none;font-weight:600;font-size:.88rem;padding:7px 14px;border-radius:99px;background:var(--panel)}.nav a:hover{background:var(--mc);color:var(--on)}
.pedir{margin-top:18px}.pedir h2{margin-bottom:4px}.pedir .sub{margin:0 0 14px;color:var(--mu)}
.fld{display:grid;gap:12px;grid-template-columns:1fr}@media(min-width:760px){.fld{grid-template-columns:1fr 1fr}}.fld label{display:grid;gap:4px;font-weight:700;font-size:.9rem}.fld input{padding:13px 14px;font:inherit;border:2px solid #cbd5e1;border-radius:12px}.fld input:focus{outline:0;border-color:var(--mh)}
.pedir .res{margin:14px 0 10px}.big{width:100%;padding:16px 20px;font-size:1.1rem}
.sec h2{display:flex;align-items:center;gap:10px}.sec h2 svg{width:28px;height:28px;color:var(--mh);flex:none}
.mini{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(230px,1fr))}.mini div{background:var(--panel);border-radius:12px;padding:14px 16px}.mini b{display:block;margin-bottom:2px}
.cob{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(200px,1fr))}.cob button{border:2px solid #e2e8f0;background:#fff;border-radius:16px;padding:18px;font:inherit;cursor:pointer;text-align:left}.cob button:hover{border-color:var(--mh)}.cob b{display:block;font-size:1.15rem;color:var(--mh)}.cob span{color:var(--mu);font-size:.9rem}
.k{font-weight:700;color:var(--mh)}
.top b{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}@media(max-width:560px){.top .lg{display:none}.top .b{padding:10px 14px}.fr img{max-height:200px}.fr{padding:8px}.hero .w{padding:26px 16px 34px}.nav{top:49px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
"""

IC = {
 "ok": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M8 12.5l2.7 2.7L16 9.5"/></svg>',
 "casa": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11l9-8 9 8"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/></svg>',
 "gota": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/></svg>',
 "hielo": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20M4.5 6.5l15 11M19.5 6.5l-15 11"/></svg>',
 "lupa": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>',
 "llave": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18v3h3l6.3-6.3a4 4 0 0 0 5.4-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/></svg>',
 "duda": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.5 9a2.5 2.5 0 1 1 3.5 2.3c-.7.4-1 .9-1 1.7M12 17h.01"/></svg>',
}

# Textos propios de cada marca, tomados de las guías de tus otros proyectos (se pasan al español)
PREF = {
 "samsung": "Los modelos Samsung suelen empezar por RF o RS (por ejemplo RF28HMEDBSR).",
 "lg": "Los modelos LG suelen empezar por LF, LM, LR o LS (por ejemplo LFX28968ST).",
 "whirlpool": "Muchos modelos Whirlpool empiezan por W seguida de letras (por ejemplo WRF555SDFZ).",
}
RESET = {
 "samsung": "Mantén presionado el botón del filtro de agua (o el botón de alarma / reinicio de filtro, según el panel) unos 3 segundos, hasta que se apague la luz del filtro.",
 "lg": "Mantén presionado el botón del filtro de agua (o «Filter Reset») unos 3 segundos, hasta que se apague el indicador o la pantalla confirme el reinicio.",
 "whirlpool": "Mantén presionado el botón del filtro de agua («Reset Water Filter») unos 3 segundos, hasta que se apague el indicador. En algunos modelos el reinicio está en el menú de la pantalla táctil.",
}

PROBLEMAS = [
 ("El agua sabe mal después de cambiar el filtro", ["Puede faltar purgar el filtro nuevo: el polvo de carbón y el aire afectan los primeros vasos.", "Queda agua vieja en la línea del dispensador: toma varios litros en limpiarse.", "El hielo viejo guarda el sabor anterior: vacía el depósito y desecha las primeras dos tandas de hielo nuevo.", "El filtro no quedó bien asentado y parte del agua lo evita: sácalo y vuelve a instalarlo hasta que trabe.", "Confirma que la referencia del filtro sea la de tu modelo."]),
 ("El filtro no gira para soltarse", ["Verifica la dirección: la mayoría gira en sentido contrario a las manecillas; algunos se presionan y salen.", "Busca un botón o pestaña de liberación que haya que presionar.", "Usa un guante de caucho o un abridor de frascos de caucho para agarrar mejor.", "Cierra el agua un minuto para bajar la presión y prueba de nuevo.", "No uses pinzas ni llaves: pueden partir el plástico. Si no cede, escríbenos."]),
 ("Gotea agua alrededor del filtro", ["El filtro no está del todo insertado o no giró hasta trabar.", "Falta un anillo (O-ring) o está torcido o dañado: revísalo en el filtro nuevo antes de instalarlo.", "La referencia no corresponde a tu modelo.", "Si sigue goteando, cierra el agua, retira el filtro y escríbenos con una foto: el técnico lo revisa."]),
 ("La luz del filtro sigue encendida", ["Mantuviste presionado el reinicio el tiempo correcto (unos 3 segundos en muchos modelos).", "El filtro está completamente insertado y trabado, y la tapa del compartimento está cerrada.", "Algunos modelos no apagan la luz hasta detectar el filtro, y los de pantalla táctil lo reinician desde el menú.", "Si nada funciona, desconecta la nevera unos minutos y prueba de nuevo."]),
 ("El dispensador sale lento o con poco caudal", ["Casi siempre es el filtro tapado: si pasaron más de 6 meses, cámbialo.", "Revisa que la manguera detrás del nevecón no esté doblada y que la llave de paso esté totalmente abierta.", "Una línea parcialmente congelada también reduce el caudal.", "Tras cambiar el filtro, deja correr varios litros: el aire en el sistema hace que el chorro parezca débil un rato."]),
 ("El hielo sale turbio o con mal olor", ["El filtro está vencido.", "Hay hielo viejo en el depósito: vacíalo, lávalo y deja que se haga hielo nuevo.", "Hay comida de olor fuerte sin tapar en el congelador.", "El agua tiene minerales: el hielo turbio puede venir de aire y minerales disueltos."]),
]

JS = """var M="__M__",R="__R__",NUM="__NUM__",NEC=__NEC__,C=["Cali","Yumbo","Palmira"],ciudad="",barrio="",modelo="";
var q=new URLSearchParams(location.search);
(function(){var c=q.get("ciudad")||q.get("c");if(c){C.forEach(function(x){if(x.toLowerCase()===c.toLowerCase())ciudad=x;});}barrio=q.get("barrio")||"";modelo=q.get("modelo")||"";})();
function msg(x){var t="Hola, necesito instalación de nevecón "+M+(ciudad?" en "+ciudad:" en Cali, Yumbo o Palmira")+(barrio?", barrio "+barrio:"")+(modelo?". Modelo: "+modelo:"")+(x?". Servicio: "+x:"")+" ["+R+(ciudad?"-"+ciudad.toLowerCase():"")+"]";return "https://wa.me/"+NUM+"?text="+encodeURIComponent(t);}
function norm(t){return t.toLowerCase().replace(/[^a-z0-9]/g,"");}
function pintar(){
 document.querySelectorAll("[data-wa]").forEach(function(a){a.href=msg();});
 document.querySelectorAll("[data-wa-s]").forEach(function(a){a.href=msg(a.getAttribute("data-wa-s"));});
 document.getElementById("need").innerHTML=NEC.map(function(x){return '<a class="f" data-e="whatsapp" href="'+msg(x)+'">'+x+'</a>';}).join("");
 document.getElementById("h1c").textContent=ciudad?ciudad:"Cali, Yumbo y Palmira";
 document.getElementById("res").textContent=ciudad?("Instalación de nevecón "+M+" en "+ciudad+(barrio?" ("+barrio+")":"")+(modelo?", modelo "+modelo:"")+": toca el botón y te respondemos con horario y costo."):"Elige tu ciudad para pedir la instalación.";
 document.querySelectorAll("#ci button,.cob button").forEach(function(b){b.setAttribute("aria-pressed",b.dataset.c===ciudad);});
 var wq=document.querySelector("[data-wa-q]");if(wq)wq.href=msg("Mi modelo es "+(modelo||"___"));
}
document.querySelectorAll("#ci button,.cob button").forEach(function(b){b.addEventListener("click",function(){ciudad=b.dataset.c;pintar();if(b.closest(".cob"))document.getElementById("pedir").scrollIntoView({behavior:"smooth"});});});
var fb=document.getElementById("barrio"),fm=document.getElementById("modelo"),bus=document.getElementById("bus");
fb.value=barrio;fm.value=modelo;
fb.addEventListener("input",function(){barrio=fb.value.trim();pintar();});
function filtrar(v){var qq=norm(v),n=0;document.querySelectorAll("#tb tr").forEach(function(r){var ok=!qq||norm(r.textContent).indexOf(qq)>-1;r.hidden=!ok;if(ok)n++;});document.getElementById("nada").hidden=!(qq&&n===0);}
fm.addEventListener("input",function(){modelo=fm.value.trim();bus.value=modelo;filtrar(modelo);pintar();});
bus.addEventListener("input",function(){modelo=bus.value.trim();fm.value=modelo;filtrar(modelo);pintar();});
document.addEventListener("click",function(e){var a=e.target.closest("[data-e]");if(!a)return;window.dataLayer=window.dataLayer||[];window.dataLayer.push({event:a.dataset.e,marca:M,ciudad:ciudad,landing:R});});
if(modelo)filtrar(modelo);pintar();"""

def pagina_marca(m):
    n = N[m]; d = D[m]
    nev = b64(NEVERA[m], 600, 900, q=85); agua = b64(AGUA, 900, 600, q=70)
    ref = f"ads-nevecones-{m}"
    filas = tabla_modelos(m)
    filas_h = "".join("<tr>" + "".join(f"<td>{H.escape(c)}</td>" for c in f) + "</tr>" for f in filas)
    ejemplo = next((f[4].split(",")[0] for f in filas if f[4].startswith(("RF", "RS", "L", "W", "G"))), filas[0][1])
    necesidades = ["Instalar mi nevecón", "Instalar o cambiar el filtro de agua", "Instalar la fábrica de hielo", "Conectar el agua y el dispensador", "Se prendió la luz del filtro", "Reinstalar mi nevecón en una mudanza"]
    pasos_filtro = ["Ten a mano el filtro nuevo y una toalla. Quita la tapa protectora del filtro nuevo solo cuando lo vayas a instalar.", "Ubica el filtro: casi siempre en la esquina superior o la pared del fondo del compartimento, o en la rejilla de la base al frente; abre la tapa si la tiene.", "Gira el filtro usado en sentido contrario a las manecillas (o presiona el botón de liberación, según el modelo) y sácalo recto. Puede gotear un poco.", "Revisa que el filtro nuevo traiga los anillos (O-rings) en su lugar.", "Alinea el filtro, empújalo y gíralo en el sentido de las manecillas hasta que trabe.", "Cierra la tapa y reinicia la luz del filtro.", "Purga el filtro: deja correr agua por el dispensador varios litros, hasta que el chorro salga firme y claro. Desecha las primeras tandas de hielo."]
    pf = "".join(f"<li>{H.escape(x)}</li>" for x in pasos_filtro)
    pasos_hielo = [("Conexión de agua", "Manguera hasta la entrada de agua del nevecón, con llave de paso accesible y sin dobleces."), ("Encendido de la fábrica", "Se activa la fábrica de hielo según tu modelo y se confirma que quede funcionando."), ("Purga", "Se deja correr agua para eliminar el aire de la línea antes de la primera producción."), ("Primeras tandas", "Normalmente las primeras 24 horas el hielo sale poco; se desechan los primeros cubos. El manual de tu modelo confirma los tiempos.")]
    ph = "".join(f"<li><b>{H.escape(a)}</b>{H.escape(b)}</li>" for a, b in pasos_hielo)
    prob_h = "".join(f"<details><summary>{H.escape(t)}</summary><ul class='ben' style='margin-top:10px'>" + "".join(f"<li>{H.escape(x)}</li>" for x in L) + f"</ul><p><a class='b wa' data-e='whatsapp' data-wa-s='{H.escape(t)}' href='#'>Que me ayude el técnico</a></p></details>" for t, L in PROBLEMAS)
    faq = [(f"¿Cuánto cuesta la instalación de un nevecón {n}?", "Depende de si solo se ubica y conecta, o si también necesita conexión de agua, filtro y accesorios. El costo se informa en COP antes de empezar."),
           (f"¿Qué filtro necesita mi nevecón {n}?", d["filtro"] + " Cada modelo puede usar una referencia distinta: busca la tuya en la tabla de esta página o escríbenos con la etiqueta."),
           ("¿Dónde encuentro el modelo de mi nevecón?", "En una etiqueta dentro del compartimento (pared lateral superior o techo, o bajo los cajones), en el marco de la puerta, o en el manual. No lo confundas con el número de serie."),
           ("¿Instalan la fábrica de hielo y la conexión de agua?", "Sí: se conecta el agua con manguera y llave de paso, se purga la línea, se activa la fábrica de hielo y se comprueba que produzca."),
           ("¿Por qué no sale hielo después de instalar?", "Normalmente las primeras 24 horas la producción es baja y los primeros cubos se desechan. Si pasan 24 horas y no hay hielo, escríbenos."),
           ("¿Cada cuánto se cambia el filtro del nevecón?", "Normalmente cada 6 meses, o antes si cambia el sabor del agua o del hielo, el dispensador sale más lento, el hielo sale turbio o se enciende la luz del filtro. Con mucho uso o agua con sedimentos, puede ser antes."),
           ("¿Puedo cambiar el filtro yo mismo?", "Sí, es un cambio sencillo y no necesita herramientas. Si prefieres, lo hacemos en la visita de instalación o cuando lo necesites."),
           ("¿Hay que purgar el filtro nuevo?", "Sí: deja correr varios litros por el dispensador hasta que el agua salga clara y firme. Un poco de aire o agua grisácea al inicio es normal por el polvo del carbón. Desecha las primeras tandas de hielo."),
           ("¿Cuánto demora la instalación?", "Suele tomar entre 1 y 2 horas según el modelo y si hay que hacer la conexión de agua."),
           ("¿Pueden instalar mi nevecón en una mudanza?", "Sí. Indica la dirección de entrega, el modelo y si hay conexión de agua lista."),
           ("¿Puedo usar el nevecón sin filtro?", "Algunos modelos permiten usar un tapón de derivación, pero el agua y el hielo quedan sin filtrar. Pregúntanos por tu modelo."),
           ("¿Atienden en Cali, Yumbo y Palmira?", "Sí, atendemos las tres ciudades y sus barrios cercanos. Escribe tu barrio por WhatsApp para confirmar el horario.")]
    faq_h = "".join(f"<details><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>" for q, a in faq)
    ver = f'<meta name="google-site-verification" content="{CFG["verificacion_gsc"]}">' if CFG.get("verificacion_gsc") else ""
    css = CSS % PAL[m] + CSS2
    js = JS.replace("__M__", n).replace("__R__", ref).replace("__NUM__", TEL).replace("__NEC__", json.dumps(necesidades, ensure_ascii=False))
    cob = "".join(f'<button type="button" data-c="{c}" aria-pressed="false"><b>{c}</b><span>Instalación de nevecón {n} en {c}. Toca para pedirla.</span></button>' for c in CIUDADES)
    signos = ["El agua o el hielo cambian de sabor u olor.", "El dispensador llena un vaso más lento que antes.", "El hielo sale turbio o la fábrica de hielo hace cubos más pequeños.", "Se enciende o parpadea la luz del filtro.", "Ves sedimento o partículas en un vaso de agua."]
    sg = "".join(f"<li>{H.escape(x)}</li>" for x in signos)
    return f'''<!doctype html><html lang="es-CO"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Instalación de nevecones {n} en Cali, Yumbo y Palmira</title>
<meta name="description" content="Instalación de nevecones {n} en Cali, Yumbo y Palmira: encuentra tu modelo, instalación del filtro de agua, fábrica de hielo y conexión de agua. Costo antes de empezar.">
<meta name="robots" content="noindex,follow">{ver}<link rel="canonical" href="https://soporte-tecnico-autorizado.com/ads/{slug_marca(m)}/"><style>{css}</style></head><body>
<header class="top"><div class="w"><b><span class="lg">Instalación de nevecones </span>{n}</b><span class="sp"></span><a class="b ll" data-e="llamar" href="tel:+{TEL}">Llamar</a><a class="b wa" data-e="whatsapp" data-wa href="#">WhatsApp</a></div></header>
<section class="hero"><div class="w"><div class="t"><h1>Instalación de nevecones {n} en <span id="h1c">Cali, Yumbo y Palmira</span></h1><p>Instalamos tu nevecón {n} con conexión de agua, filtro y fábrica de hielo. Te damos el costo antes de empezar.</p>
<ul class="chips"><li>A domicilio</li><li>Filtro de agua</li><li>Fábrica de hielo</li><li>Costo antes de empezar</li></ul>
<div class="cta"><a class="b wa" data-e="whatsapp" data-wa href="#">Escribir por WhatsApp</a><a class="b ll" data-e="llamar" href="tel:+{TEL}">Llamar {TELV}</a></div></div><div class="fr"><img src="{nev}" alt="{ALT[m]}" width="300" height="540"></div></div></section>
<section class="trust"><div class="w"><div class="tr">{IC["ok"]}Costo antes de empezar</div><div class="tr">{IC["casa"]}A domicilio en Cali, Yumbo y Palmira</div><div class="tr">{IC["gota"]}Agua, filtro y dispensador</div><div class="tr">{IC["hielo"]}Prueba de hielo al final</div></div></section>
<nav class="nav" aria-label="Secciones"><div class="w"><a href="#pedir">Pedir instalación</a><a href="#modelo">Tu modelo</a><a href="#filtro">Filtro</a><a href="#hielo">Hielo</a><a href="#agua">Agua</a><a href="#problemas">Problemas</a><a href="#costo">Costo</a><a href="#faq">Preguntas</a></div></nav>
<main class="w">
<section class="card pedir" id="pedir"><h2>Pide tu instalación de nevecón {n}</h2><p class="sub">Elige tu ciudad y, si quieres, escribe tu barrio y tu modelo. Así el técnico llega preparado.</p>
<div class="ci" id="ci">{"".join(f'<button type="button" data-c="{c}" aria-pressed="false">{c}</button>' for c in CIUDADES)}</div>
<div class="fld"><label>Tu barrio (opcional)<input id="barrio" type="text" placeholder="Ej. barrio o sector" autocomplete="off"></label><label>Modelo de tu nevecón (opcional)<input id="modelo" type="text" placeholder="Ej. {ejemplo}" autocomplete="off"></label></div>
<div class="res" id="res">Elige tu ciudad para pedir la instalación.</div><a class="b wa big" data-e="whatsapp" data-wa href="#">Pedir instalación por WhatsApp</a></section>
<section class="card"><h2>¿Qué necesitas para tu nevecón {n}?</h2><div class="g" id="need"></div></section>
<section class="card sec" id="modelo"><h2>{IC["lupa"]}Encuentra la referencia de tu nevecón {n}</h2><p>{H.escape(PREF[m])} Escribe tu modelo o la referencia del filtro y te mostramos cuál le corresponde.</p>
<input class="bus" id="bus" type="search" placeholder="Ej. {ejemplo}" autocomplete="off" aria-label="Buscar modelo o referencia"><div class="tw"><table><thead><tr><th>Filtro</th><th>Referencia</th><th>También se conoce como</th><th>Ubicación</th><th>Modelos de nevecón (ejemplos)</th></tr></thead><tbody id="tb">{filas_h}</tbody></table></div>
<p id="nada" class="note" hidden>No aparece ese modelo en la lista. Escríbenos con la etiqueta de tu nevecón y te confirmamos el filtro y la instalación. <a href="#" data-wa-q="1" data-e="whatsapp" style="font-weight:700">Escribir mi modelo por WhatsApp</a></p>
<p style="font-size:.9rem;color:var(--mu)">Son ejemplos de modelos. Si el tuyo no está, escríbenos con la etiqueta y lo confirmamos.</p>
<h3>¿Dónde está el modelo de tu nevecón?</h3><ul class="ben"><li>Dentro del compartimento, en la pared lateral superior o en el techo.</li><li>En la pared lateral, debajo de los cajones o detrás de ellos (saca el cajón si no se ve).</li><li>En el marco de la puerta o el borde interior, sobre todo en los french door.</li><li>En la parte trasera del equipo o dentro de la puerta del congelador, en algunos modelos.</li><li>En el manual o en la factura.</li></ul>
<div class="note">Copia el modelo completo, con las letras del final. No lo confundas con el número de serie. Si no lo encuentras, mándanos una foto del filtro viejo y de cualquier etiqueta.</div>
<p><a class="b wa" data-e="whatsapp" data-wa-s="Envío foto de la etiqueta de mi nevecón" href="#">Enviar foto de la etiqueta por WhatsApp</a></p></section>
<section class="card sec" id="filtro"><h2>{IC["gota"]}Instalación del filtro de agua del nevecón {n}</h2><p>{H.escape(d["filtro"])}</p><div class="note">Son referencias frecuentes. Cada modelo puede usar una distinta: confirma con la etiqueta de tu nevecón o escríbenos con el modelo y te decimos cuál necesita.</div>
<div class="two"><div><h3>Cómo se instala</h3><ol class="st">{pf}</ol></div><div><h3>Detalle de tu marca</h3><p>{H.escape(d["paso"])}</p><h3>Luz del filtro: cómo reiniciarla</h3><p>{H.escape(RESET[m])}</p><h3>¿Cuándo cambiarlo?</h3><p>Normalmente cada 6 meses. Cámbialo antes si:</p><ul class="ben" style="margin-top:8px">{sg}</ul><p style="margin-top:12px"><a class="b wa" data-e="whatsapp" data-wa-s="Instalar o cambiar el filtro de agua" href="#">Consultar mi filtro por WhatsApp</a></p></div></div></section>
<section class="card sec" id="hielo"><h2>{IC["hielo"]}Instalación de la fábrica de hielo del nevecón {n}</h2><p>El técnico activa la fábrica de hielo según tu modelo y comprueba que entre agua y que produzca hielo.</p><ol class="st">{ph}</ol><div class="note">Después de cambiar el filtro, desecha las primeras tandas de hielo: el hielo hecho antes puede conservar el sabor anterior.</div></section>
<section class="card sec" id="agua"><h2>{IC["llave"]}Conexión de agua y dispensador</h2><div class="two"><img class="foto" src="{agua}" alt="Persona sirviéndose agua del dispensador de un nevecón" width="900" height="600"><ul class="ben"><li>Manguera de agua sin dobleces ni aplastamientos detrás del equipo.</li><li>Llave de paso accesible y totalmente abierta.</li><li>Presión de agua suficiente: si es muy baja, el dispensador sale lento.</li><li>Purga del sistema antes de tomar el primer vaso de agua.</li><li>Revisión de fugas en las uniones al terminar.</li><li>Prueba del dispensador de agua y de hielo con el equipo funcionando.</li></ul></div>
<h3>Después de instalar el filtro, lo que es normal</h3><div class="mini"><div><b>Chorro con aire</b>Un poco de aire o salpicaduras al inicio es aire atrapado en la línea.</div><div><b>Agua grisácea</b>Al principio puede salir agua turbia por el polvo fino del carbón; debe aclararse al purgar.</div><div><b>Si no se aclara</b>Si el agua sigue turbia o salen partículas, para y revisa que el filtro esté bien asentado.</div></div></section>
<section class="card sec" id="problemas"><h2>{IC["duda"]}Problemas comunes con el filtro y el agua</h2>{prob_h}</section>
<section class="card sec" id="costo"><h2>{IC["ok"]}Qué incluye la instalación y cómo se calcula el costo</h2><ul class="ben"><li>Revisión del lugar: espacio, piso firme y ventilación a los lados y atrás.</li><li>Nivelación del equipo con las patas ajustables.</li><li>Conexión a un tomacorriente con tierra, sin extensiones ni regletas.</li><li>Conexión de agua, filtro y fábrica de hielo.</li><li>Ajuste de la temperatura y verificación del enfriamiento.</li><li>Explicación del uso básico y del cambio de filtro.</li></ul>
<h3>De qué depende el costo</h3><div class="mini"><div><b>La conexión de agua</b>Si ya existe o hay que preparar manguera y llave de paso.</div><div><b>Los accesorios</b>Manguera, llave de paso y filtro, si no los tienes.</div><div><b>El modelo y el lugar</b>Dificultad de acceso y de ubicación del equipo.</div></div><p>El costo se te informa en COP <span class="k">antes de empezar</span>; no se hace nada sin tu aprobación.</p>
<h3>Antes de la visita</h3><ul class="ben"><li>Mide el espacio y la puerta de entrada para que el equipo pase.</li><li>Si el nevecón viajó acostado, déjalo reposar de pie varias horas antes de conectarlo; confirma el tiempo en el manual.</li><li>Ten un tomacorriente con tierra cerca y una llave de agua accesible.</li><li>Limpia el interior con un paño húmedo antes de usarlo.</li></ul></section>
<section class="card"><h2>Dónde instalamos</h2><div class="cob">{cob}</div></section>
<section class="card sec" id="faq"><h2>{IC["duda"]}Preguntas frecuentes sobre la instalación de nevecones {n}</h2>{faq_h}</section>
<section class="card end"><h2>¿Necesitas instalar tu nevecón {n}?</h2><p>Escríbenos y te respondemos con horario y costo antes de empezar.</p><div class="cta"><a class="b wa" data-e="whatsapp" data-wa href="#">WhatsApp {TELV}</a><a class="b ll" data-e="llamar" href="tel:+{TEL}">Llamar</a></div></section>
</main><footer>Servicio técnico independiente. {n} y su logotipo pertenecen a sus respectivos propietarios; este sitio no está afiliado ni patrocinado por {n}.</footer>
<div class="bar"><a class="b wa" data-e="whatsapp" data-wa href="#">WhatsApp</a><a class="b ll" data-e="llamar" href="tel:+{TEL}">Llamar</a></div>
<script>{js}</script></body></html>'''

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
            url = f"https://soporte-tecnico-autorizado.com/ads/{slug_marca(m)}/?ciudad={c}"
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
