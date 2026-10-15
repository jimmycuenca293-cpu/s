"""Genera campana.html: la campaña de Google Ads para ver y copiar (vista previa de anuncios, palabras clave, negativas, recursos)."""
import html, json, runpy, pathlib
g = runpy.run_path("generar.py")
D, CAMP, GRUPOS, NEG = g["D"], g["CAMP"], g["GRUPOS"], g["NEGATIVAS"]
for f in ("anuncios.csv", "palabras-clave.csv", "grupos.json"):
    pathlib.Path(f).unlink(missing_ok=True)
e = lambda s: html.escape(str(s), quote=True)
SITELINKS = [("Cómo instalar tu filtro", "/purofiltro-instalacion/", "Paso a paso por referencia", "En minutos y sin herramientas"),
             ("¿Cuándo cambiar el filtro?", "/purofiltro-guia/cada-cuanto-cambiar-el-filtro-del-nevecon/", "Las señales de que ya toca", "Cada 6 meses o antes"),
             ("Busca por referencia", "/purofiltro-referencias/", "Todas las equivalencias", "Encuentra el tuyo fácil"),
             ("Envíos a toda Colombia", "/purofiltro-envios/", "Tiempo de entrega a tu ciudad", "Envío gratis"),
             ("Ver la tienda", "/purofiltro-tienda/", "Todos los filtros y precios", "Samsung, LG, Whirlpool, GE")]
CALLOUTS = ["Envío gratis", "Pago seguro en línea", "PSE, Nequi y tarjeta", "Asesoría por WhatsApp", "Llega en 2 a 3 días", "Pack anual con descuento", "Tutorial de instalación", "Técnicos de neveras"]
PRECIOS = [("Filtro Samsung HAF-CIN", "$115.900"), ("Filtro LG LT1000P", "$112.900"), ("Whirlpool EveryDrop 1", "$145.900"), ("Filtro GE MWF", "$158.900"), ("Filtros externos", "desde $81.900")]
CONFIG = [("Tipo", "Búsqueda (Search). Sin Red de Display ni socios de búsqueda."),
          ("Objetivo", "Ventas. Conversión principal: pago_wompi. Secundaria: whatsapp."),
          ("Ubicación", "Colombia · personas que están o suelen estar en la ubicación."),
          ("Idioma", "Español"),
          ("Presupuesto", "$25.000 a $35.000 al día (unos $750.000 a $1.050.000 al mes)."),
          ("Puja", "Semanas 1 a 4: Maximizar clics con CPC máximo de $1.500. Con 15+ conversiones: Maximizar conversiones y luego CPA objetivo de $25.000."),
          ("Horario", "Todos los días, de 6:00 a. m. a 11:00 p. m."),
          ("Concordancia", "Frase y exacta. Sin concordancia amplia al comienzo.")]
datos = [{"nombre": x["nombre"], "url": D + x["url"], "ruta": f"filtrosdeaguanevecon.com › {x['p1']} › {x['p2']}", "t": x["T"], "d": x["D"], "kw": x["kw"]} for x in GRUPOS]
total_kw = sum(len(x["kw"]) for x in GRUPOS)

tabs = "".join(f'<button type="button" role="tab" id="tab-{i}" aria-selected="{"true" if i == 0 else "false"}" data-g="{i}">{e(x["nombre"])}<span>{len(x["kw"])}</span></button>' for i, x in enumerate(datos))
cfg = "".join(f"<div><dt>{e(a)}</dt><dd>{e(b)}</dd></div>" for a, b in CONFIG)
sl = "".join(f'<li><b>{e(t)}</b><span>{e(l1)} · {e(l2)}</span><code>{e(D + u)}</code></li>' for t, u, l1, l2 in SITELINKS)
co = "".join(f"<span>{e(c)}</span>" for c in CALLOUTS)
pr = "".join(f"<li><span>{e(a)}</span><b>{e(b)}</b></li>" for a, b in PRECIOS)
neg = "\n".join(f'"{n}"' for n in NEG)

page = f"""<title>Campaña PuroFiltro</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Manrope:wght@400;500;600;700&family=JetBrains+Mono:wght@500&display=swap">
<style>
/* Layout: encabezado de la marca, resumen, pestañas por grupo con vista previa del anuncio a la izquierda y textos/palabras a la derecha */
:root{{--bg:#f3f6f5;--panel:#ffffff;--ink:#10292c;--muted:#5b7174;--line:#dbe5e3;--accent:#0f7f70;--accent-soft:#e1f2ee;--deep:#0a2a2e;--glow:#5fd6c3;--ok:#1f7a48;--warn:#9a5b00;
--g-title:#1a0dab;--g-url:#202124;--g-text:#4d5156;
--f-display:"Bricolage Grotesque",Manrope,system-ui,sans-serif;--f-body:Manrope,"Segoe UI",system-ui,sans-serif;--f-mono:"JetBrains Mono",ui-monospace,Menlo,Consolas,monospace}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0b1a1c;--panel:#122427;--ink:#e3eeec;--muted:#93acaa;--line:#24393c;--accent:#3fc1ae;--accent-soft:#143a35;--deep:#06191b;--ok:#6cc790;--warn:#f0a73a;--g-title:#8ab4f8;--g-url:#dadce0;--g-text:#bdc1c6;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#0b1a1c;--panel:#122427;--ink:#e3eeec;--muted:#93acaa;--line:#24393c;--accent:#3fc1ae;--accent-soft:#143a35;--deep:#06191b;--ok:#6cc790;--warn:#f0a73a;--g-title:#8ab4f8;--g-url:#dadce0;--g-text:#bdc1c6;color-scheme:dark}}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--ink);font:15px/1.55 var(--f-body);margin:0}}
.wrap{{max-width:1120px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}}
header{{background:var(--deep);color:#e6f2ef}}
header .wrap{{padding-block:28px 30px;display:flex;flex-direction:column;gap:10px}}
.marca{{font-family:var(--f-display);font-weight:800;font-size:18px;color:#fff}}.marca b{{color:var(--glow)}}
h1{{font-family:var(--f-display);font-size:clamp(26px,4vw,38px);line-height:1.1;margin:0;letter-spacing:-.02em;text-wrap:balance;color:#fff}}
header p{{margin:0;max-width:62ch;color:#b9d2cd}}
.resumen{{display:flex;flex-wrap:wrap;gap:8px;margin-top:6px}}
.resumen span{{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.14);border-radius:999px;padding:5px 12px;font-size:13px;font-weight:600;color:#e6f2ef;font-variant-numeric:tabular-nums}}
main{{display:flex;flex-direction:column;gap:28px;padding-block:28px 56px}}
h2{{font-family:var(--f-display);font-size:22px;margin:0;letter-spacing:-.01em}}
.sec{{display:flex;flex-direction:column;gap:14px}}
.sub{{color:var(--muted);margin:0;max-width:70ch}}
.panel{{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:18px}}
dl.cfg{{margin:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px}}
dl.cfg div{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:12px 14px}}
dt{{font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);font-weight:700}}dd{{margin:4px 0 0;font-weight:600}}
.tabs{{display:flex;gap:6px;overflow-x:auto;padding-bottom:2px}}
.tabs button{{flex:0 0 auto;font:600 14px var(--f-body);border:1.5px solid var(--line);background:var(--panel);color:var(--ink);border-radius:999px;padding:8px 14px;cursor:pointer;display:flex;gap:8px;align-items:center}}
.tabs button span{{font-size:12px;color:var(--muted);font-variant-numeric:tabular-nums}}
.tabs button[aria-selected="true"]{{background:var(--accent);border-color:var(--accent);color:#fff}}.tabs button[aria-selected="true"] span{{color:#e1f2ee}}
.tabs button:focus-visible,.copiar:focus-visible,.otro:focus-visible{{outline:3px solid var(--glow);outline-offset:2px}}
.grupo{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);gap:18px;align-items:start}}
@media (max-width:860px){{.grupo{{grid-template-columns:1fr}}}}
.col{{display:flex;flex-direction:column;gap:14px;min-width:0}}
.anuncio{{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:18px 20px;display:flex;flex-direction:column;gap:4px;font-family:Arial,Helvetica,sans-serif}}
.anuncio .pat{{font-size:12px;font-weight:700;color:var(--g-url)}}
.anuncio .url{{font-size:13px;color:var(--g-url)}}
.anuncio .tit{{font-size:20px;line-height:1.3;color:var(--g-title)}}
.anuncio .des{{font-size:14px;color:var(--g-text);line-height:1.5}}
.etq{{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;font-weight:700;display:flex;justify-content:space-between;align-items:center;gap:10px}}
.otro{{font:600 13px var(--f-body);background:var(--accent-soft);color:var(--accent);border:0;border-radius:10px;padding:7px 12px;cursor:pointer}}
ol.lista{{margin:0;padding-left:0;list-style:none;display:flex;flex-direction:column;gap:6px;counter-reset:n}}
ol.lista li{{display:flex;gap:10px;align-items:baseline;counter-increment:n;padding:6px 0;border-bottom:1px solid var(--line)}}
ol.lista li::before{{content:counter(n);font:500 12px var(--f-mono);color:var(--muted);min-width:20px}}
ol.lista li span{{flex:1;min-width:0}}
.cc{{font:500 12px var(--f-mono);font-variant-numeric:tabular-nums;color:var(--ok);background:var(--accent-soft);border-radius:6px;padding:1px 6px}}
.kwbox{{display:flex;flex-direction:column;gap:8px}}
.kwtabs{{display:flex;gap:6px;flex-wrap:wrap}}
.kwtabs button{{font:600 13px var(--f-body);border:1.5px solid var(--line);background:transparent;color:var(--ink);border-radius:10px;padding:6px 10px;cursor:pointer}}
.kwtabs button[aria-pressed="true"]{{border-color:var(--accent);color:var(--accent);background:var(--accent-soft)}}
pre{{margin:0;background:var(--bg);border:1px solid var(--line);border-radius:12px;padding:12px 14px;font:500 13px/1.7 var(--f-mono);overflow:auto;max-height:340px;white-space:pre}}
.copiar{{align-self:flex-start;font:700 14px var(--f-body);background:var(--accent);color:#fff;border:0;border-radius:12px;padding:10px 16px;cursor:pointer}}
.dest{{font-size:13px;color:var(--muted);word-break:break-all}}.dest a{{color:var(--accent)}}
.dos{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px}}
ul.sl{{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:10px}}
ul.sl li{{display:flex;flex-direction:column;gap:2px;padding-bottom:10px;border-bottom:1px solid var(--line)}}
ul.sl li span{{color:var(--muted);font-size:13.5px}}ul.sl code{{font:500 12px var(--f-mono);color:var(--accent);word-break:break-all}}
.chips{{display:flex;flex-wrap:wrap;gap:6px}}.chips span{{border:1px solid var(--line);border-radius:999px;padding:4px 10px;font-size:13px;font-weight:600;background:var(--panel)}}
ul.pr{{list-style:none;margin:0;padding:0}}ul.pr li{{display:flex;justify-content:space-between;gap:10px;padding:7px 0;border-bottom:1px solid var(--line);font-variant-numeric:tabular-nums}}
ol.pasos{{margin:0;padding-left:20px;display:flex;flex-direction:column;gap:8px}}
.nota{{border-left:4px solid var(--warn);background:var(--panel);border-radius:0 12px 12px 0;padding:12px 16px;color:var(--ink)}}
.toast{{position:fixed;left:50%;bottom:calc(20px + env(safe-area-inset-bottom,0px));transform:translateX(-50%);background:var(--deep);color:#fff;padding:10px 16px;border-radius:12px;font-weight:600;font-size:14px}}
@media (prefers-reduced-motion:no-preference){{.tabs button,.copiar,.otro{{transition:background .15s,border-color .15s}}}}
</style>
<header><div class="wrap">
  <div class="marca">Puro<b>Filtro</b> · Google Ads</div>
  <h1>Campaña de búsqueda para filtrosdeaguanevecon.com</h1>
  <p>Así se ven los anuncios, qué palabras clave van en cada grupo y qué configurar. Todo está listo para copiar y pegar en Google Ads.</p>
  <div class="resumen"><span>{len(datos)} grupos de anuncios</span><span>{len(datos)*15} títulos · {len(datos)*4} descripciones</span><span>{total_kw} palabras clave</span><span>{len(NEG)} negativas</span><span>Colombia · Español</span></div>
</div></header>
<main class="wrap">
  <section class="sec" aria-labelledby="h-cfg"><h2 id="h-cfg">Configuración</h2><dl class="cfg">{cfg}</dl></section>

  <section class="sec" aria-labelledby="h-gr"><h2 id="h-gr">Grupos de anuncios</h2>
    <p class="sub">Escoge un grupo. A la izquierda ves cómo puede salir el anuncio en Google (Google combina los títulos y descripciones solo); a la derecha están todos los textos y las palabras clave para copiar.</p>
    <div class="tabs" role="tablist" aria-label="Grupos de anuncios">{tabs}</div>
    <div class="grupo" id="grupo" role="tabpanel">
      <div class="col">
        <div class="etq">Vista previa del anuncio <button type="button" class="otro" id="otro">Ver otra combinación</button></div>
        <div class="anuncio" aria-live="polite"><span class="pat">Patrocinado</span><span class="url" id="a-url"></span><span class="tit" id="a-tit"></span><span class="des" id="a-des"></span></div>
        <p class="dest">Página de destino: <a id="a-dest" href="#" target="_blank" rel="noopener"></a></p>
        <div class="panel col"><div class="etq">Palabras clave del grupo</div>
          <div class="kwbox">
            <div class="kwtabs" role="group" aria-label="Tipo de concordancia"><button type="button" data-m="frase" aria-pressed="true">Frase "…"</button><button type="button" data-m="exacta" aria-pressed="false">Exacta […]</button><button type="button" data-m="simple" aria-pressed="false">Sin símbolos</button></div>
            <pre id="kw"></pre>
            <button type="button" class="copiar" id="copiar-kw">Copiar palabras clave</button>
          </div>
        </div>
      </div>
      <div class="col">
        <div class="panel col"><div class="etq">Títulos · máximo 30 caracteres <button type="button" class="otro" id="copiar-t">Copiar todos</button></div><ol class="lista" id="titulos"></ol></div>
        <div class="panel col"><div class="etq">Descripciones · máximo 90 caracteres <button type="button" class="otro" id="copiar-d">Copiar todas</button></div><ol class="lista" id="descs"></ol></div>
      </div>
    </div>
  </section>

  <section class="sec" aria-labelledby="h-neg"><h2 id="h-neg">Palabras negativas</h2>
    <p class="sub">Van en Palabras clave → Palabras clave negativas, a nivel de campaña. Así no pagas por búsquedas que no son de filtros de nevecón.</p>
    <div class="panel col"><pre id="neg">{e(neg)}</pre><button type="button" class="copiar" data-copiar="neg">Copiar negativas</button></div>
  </section>

  <section class="sec" aria-labelledby="h-rec"><h2 id="h-rec">Recursos del anuncio</h2>
    <div class="dos">
      <div class="panel col"><div class="etq">Enlaces a sitios</div><ul class="sl">{sl}</ul></div>
      <div class="col">
        <div class="panel col"><div class="etq">Textos destacados</div><div class="chips">{co}</div></div>
        <div class="panel col"><div class="etq">Fragmentos estructurados · Marcas</div><div class="chips"><span>Samsung</span><span>LG</span><span>Whirlpool</span><span>GE</span><span>Maytag</span><span>KitchenAid</span></div></div>
        <div class="panel col"><div class="etq">Llamada</div><b>321 799 6144</b><span class="sub">Solo en horario de atención.</span></div>
        <div class="panel col"><div class="etq">Precios</div><ul class="pr">{pr}</ul></div>
      </div>
    </div>
  </section>

  <section class="sec" aria-labelledby="h-sub"><h2 id="h-sub">Cómo subirla</h2>
    <div class="panel"><ol class="pasos">
      <li>Sube la tienda a Hostinger y deja publicadas en Tag Manager las conversiones <b>pago_wompi</b> y <b>whatsapp</b>.</li>
      <li>En Google Ads crea la campaña <b>{e(CAMP)}</b> con la configuración de arriba.</li>
      <li>Crea los 5 grupos. En cada uno pega sus palabras clave y arma un anuncio adaptable con sus 15 títulos y 4 descripciones.</li>
      <li>Pega las palabras negativas a nivel de campaña y agrega los recursos.</li>
      <li>Revisa y dale <b>Publicar</b>. La primera semana mira el informe de términos de búsqueda y agrega negativas nuevas.</li>
    </ol></div>
    <p class="nota">Samsung, LG, Whirlpool y GE son marcas registradas. Si Google limita o rechaza un anuncio por la marca, cambia ese título por la referencia (por ejemplo «Filtro LT1000P»). No uses «original» ni «genuino».</p>
  </section>
</main>
<div class="toast" id="toast" hidden></div>
<script>
const G = {json.dumps(datos, ensure_ascii=False)};
const $ = s => document.querySelector(s);
let gi = 0, modo = "frase", combo = 0;
const esc = s => String(s).replace(/[&<>"]/g, c => ({{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}}[c]));
function kwTexto() {{ const k = G[gi].kw; return modo === "frase" ? k.map(x => '"' + x + '"').join("\\n") : modo === "exacta" ? k.map(x => "[" + x + "]").join("\\n") : k.join("\\n"); }}
function anuncio() {{
  const g = G[gi], t = g.t, d = g.d, n = combo;
  $("#a-url").textContent = g.ruta;
  $("#a-tit").textContent = [t[n % t.length], t[(n + 9) % t.length], t[(n + 4) % t.length]].join(" | ");
  $("#a-des").textContent = d[n % d.length] + " " + d[(n + 2) % d.length];
}}
function pintar() {{
  const g = G[gi];
  document.querySelectorAll(".tabs button").forEach((b, i) => b.setAttribute("aria-selected", String(i === gi)));
  $("#grupo").setAttribute("aria-labelledby", "tab-" + gi);
  $("#titulos").innerHTML = g.t.map(x => `<li><span>${{esc(x)}}</span><em class="cc">${{x.length}}/30</em></li>`).join("");
  $("#descs").innerHTML = g.d.map(x => `<li><span>${{esc(x)}}</span><em class="cc">${{x.length}}/90</em></li>`).join("");
  $("#a-dest").href = g.url; $("#a-dest").textContent = g.url;
  $("#kw").textContent = kwTexto(); anuncio();
}}
function aviso(t) {{ const el = $("#toast"); el.textContent = t; el.hidden = false; clearTimeout(aviso.t); aviso.t = setTimeout(() => el.hidden = true, 1800); }}
async function copiar(texto, el) {{
  try {{ await navigator.clipboard.writeText(texto); aviso("Copiado"); }}
  catch {{ if (el) {{ const r = document.createRange(); r.selectNodeContents(el); const s = getSelection(); s.removeAllRanges(); s.addRange(r); }} aviso("Selecciónalo y cópialo con Ctrl+C"); }}
}}
document.querySelector(".tabs").addEventListener("click", e => {{ const b = e.target.closest("[data-g]"); if (!b) return; gi = +b.dataset.g; combo = 0; pintar(); try {{ localStorage.setItem("pf-grupo", gi); }} catch {{}} }});
document.querySelector(".kwtabs").addEventListener("click", e => {{ const b = e.target.closest("[data-m]"); if (!b) return; modo = b.dataset.m; document.querySelectorAll(".kwtabs button").forEach(x => x.setAttribute("aria-pressed", String(x === b))); $("#kw").textContent = kwTexto(); }});
$("#otro").addEventListener("click", () => {{ combo++; anuncio(); }});
$("#copiar-kw").addEventListener("click", () => copiar(kwTexto(), $("#kw")));
$("#copiar-t").addEventListener("click", () => copiar(G[gi].t.join("\\n"), $("#titulos")));
$("#copiar-d").addEventListener("click", () => copiar(G[gi].d.join("\\n"), $("#descs")));
document.querySelector('[data-copiar="neg"]').addEventListener("click", () => copiar($("#neg").textContent, $("#neg")));
try {{ const v = +localStorage.getItem("pf-grupo"); if (v >= 0 && v < G.length) gi = v; }} catch {{}}
pintar();
</script>
"""
(pathlib.Path(__file__).resolve().parent.parent / "campana.html").write_text(page, encoding="utf-8")
print("ok")
