import json,html,sys
d=json.load(open('datos.json',encoding='utf-8'))
e=lambda s:html.escape(s,quote=True)
row=lambda t,l:f'<li><span class="t">{e(t)}</span><span class="n">{len(t)}/{l}</span><button class="cp" data-t="{e(t)}">Copiar</button></li>'
lista=lambda it,l:'<ul class="rows">'+''.join(row(t,l) for t in it)+'</ul>'
bl=lambda it,et:f'<button class="cp all" data-t="{e(chr(10).join(it))}">{et}</button>'
nav=''.join(f'<a href="#g{i}">{e(g["nombre"])}</a>' for i,g in enumerate(d['grupos']))
sec=''
for i,g in enumerate(d['grupos']):
    K=g['claves']; info=g['nombre'].startswith('Cambio')
    fr=['"'+k+'"' for k in K]; ex=[] if info else ['['+k+']' for k in K]
    sec+=f'''<section class="grupo" id="g{i}"><h2>{e(g["nombre"])}</h2>
<p class="meta">URL final <span class="u">{e(g["url"])}</span> <button class="cp" data-t="{e(g["url"])}">Copiar</button> · Ruta visible <b>{e(g["path1"])}/{e(g["path2"])}</b> <button class="cp" data-t="{e(g["path1"])}">Ruta 1</button> <button class="cp" data-t="{e(g["path2"])}">Ruta 2</button></p>
<div class="cols"><div><h3>Títulos ({len(g["titulos"])}) {bl(g["titulos"],"Copiar todos")}</h3>{lista(g["titulos"],30)}</div>
<div><h3>Descripciones ({len(g["descripciones"])}) {bl(g["descripciones"],"Copiar todas")}</h3>{lista(g["descripciones"],90)}</div></div>
<h3>Palabras clave ({len(K)}) {bl(fr,"En frase")} {bl(ex,"En exacta") if ex else ""} {bl(K,"Sin formato")}</h3>
<p class="kw">{" ".join(f'<span class="k">{e(k)}</span>' for k in K)}</p>{('<p class="nota">'+e(g["nota"])+'</p>') if g["nota"] else ''}</section>'''
neg=d['negativas']
sl=''.join(f'<li><span class="t"><b>{e(s[0])}</b> · {e(s[1])} · {e(s[2])}<br><span class="u">{e(s[3])}</span></span><span class="btns"><button class="cp" data-t="{e(s[0])}">Título</button><button class="cp" data-t="{e(s[1])}">Desc 1</button><button class="cp" data-t="{e(s[2])}">Desc 2</button><button class="cp" data-t="{e(s[3])}">URL</button></span></li>' for s in d['sitelinks'])
f=d['fragmento']
page=f'''<title>Campaña Filtros Lavadoras</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600;800&family=Public+Sans:wght@400;600&family=JetBrains+Mono:wght@400&display=swap">
<style>
/* Layout: barra de grupos fija arriba, cada grupo en dos columnas (títulos | descripciones), filas con botón de copiar */
:root{{--bg:#f6f8fb;--card:#fff;--fg:#10223a;--mut:#5b6b80;--line:#dbe3ee;--acc:#0a6cff;--accf:#fff;--ok:#0f8a4f;--soft:#eaf2ff;--disp:'Bricolage Grotesque',system-ui,sans-serif;--body:'Public Sans',system-ui,sans-serif;--mono:'JetBrains Mono',ui-monospace,monospace}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0d1520;--card:#142132;--fg:#e6edf6;--mut:#93a4b8;--line:#25364b;--acc:#5aa2ff;--accf:#07121f;--ok:#4fd18b;--soft:#182a42;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#0d1520;--card:#142132;--fg:#e6edf6;--mut:#93a4b8;--line:#25364b;--acc:#5aa2ff;--accf:#07121f;--ok:#4fd18b;--soft:#182a42;color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);font:15px/1.5 var(--body);padding-block:0 48px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}}
.w{{max-width:1100px;margin:0 auto}}h1{{font:800 clamp(26px,5vw,40px)/1.1 var(--disp);margin:28px 0 6px;text-wrap:balance}}h2{{font:800 26px var(--disp);margin:0 0 6px}}h3{{font:600 15px var(--body);margin:18px 0 8px;display:flex;flex-wrap:wrap;gap:8px;align-items:center}}
.sub{{color:var(--mut);margin:0 0 14px;max-width:70ch}}
nav{{position:sticky;top:env(safe-area-inset-top,0px);background:var(--bg);padding:10px 0;display:flex;gap:6px;flex-wrap:wrap;border-bottom:1px solid var(--line);z-index:5}}
nav a{{padding:5px 10px;border:1px solid var(--line);border-radius:6px;color:var(--fg);text-decoration:none;font-size:13px;background:var(--card)}}nav a:hover{{border-color:var(--acc);color:var(--acc)}}
.grupo,.gen{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:20px;margin-top:20px}}
.meta{{color:var(--mut);font-size:13px;margin:0 0 4px;overflow-wrap:anywhere}}.u{{font-family:var(--mono);font-size:12px}}
.cols{{display:grid;grid-template-columns:1fr 1fr;gap:20px}}.cols>div{{min-width:0}}
.rows{{list-style:none;margin:0;padding:0;border:1px solid var(--line);border-radius:8px}}.rows li{{display:flex;gap:10px;align-items:center;padding:8px 10px;border-bottom:1px solid var(--line)}}.rows li:last-child{{border:0}}
.t{{flex:1;min-width:0;overflow-wrap:anywhere}}.n{{font:12px var(--mono);color:var(--mut);white-space:nowrap}}.btns{{display:flex;gap:4px;flex-wrap:wrap}}
.cp{{font:600 12px var(--body);border:1px solid var(--acc);color:var(--acc);background:transparent;border-radius:6px;padding:4px 9px;cursor:pointer;white-space:nowrap}}.cp:hover{{background:var(--soft)}}.cp:focus-visible{{outline:2px solid var(--acc);outline-offset:2px}}.cp.ok{{background:var(--ok);border-color:var(--ok);color:var(--accf)}}.cp.all{{background:var(--acc);color:var(--accf)}}
.kw{{display:flex;flex-wrap:wrap;gap:5px;margin:0}}.k{{font:12px var(--mono);background:var(--soft);padding:2px 7px;border-radius:5px}}.nota{{color:var(--mut);font-style:italic}}
@media(max-width:760px){{.cols{{grid-template-columns:1fr}}.rows li{{flex-wrap:wrap}}}}
</style>
<div class="w"><h1>{e(d["campana"])}</h1>
<p class="sub">Toca «Copiar» en cada título, descripción o palabra clave y pégalo en Google Ads. Los números muestran el largo permitido (títulos 30, descripciones 90). Conversión: evento <b>whatsapp</b> de Tag Manager (GTM-5SCP73SQ).</p>
<nav><a href="#gen">Campaña</a>{nav}<a href="#neg">Negativas</a></nav>
<section class="gen" id="gen"><h2>Recursos de la campaña</h2><h3>Enlaces de sitio</h3><ul class="rows">{sl}</ul>
<h3>Textos destacados {bl(d["destacados"],"Copiar todos")}</h3>{lista(d["destacados"],25)}
<h3>Fragmento estructurado ({e(f[0])}) {bl(f[1],"Copiar valores")}</h3><p class="kw">{" ".join(f'<span class="k">{e(k)}</span>' for k in f[1])}</p>
<h3>Llamadas</h3><ul class="rows"><li><span class="t">Samsung 305 479 6329</span><button class="cp" data-t="3054796329">Copiar</button></li><li><span class="t">LG 320 510 2995</span><button class="cp" data-t="3205102995">Copiar</button></li></ul></section>
{sec}
<section class="gen" id="neg"><h2>Palabras negativas ({len(neg)})</h2><p class="sub">Agrégalas a nivel de campaña, en concordancia de frase. {bl(neg,"Copiar todas")} {bl(['"'+n+'"' for n in neg],"En frase")}</p><p class="kw">{" ".join(f'<span class="k">{e(k)}</span>' for k in neg)}</p></section></div>
<script>
document.addEventListener('click',function(ev){{var b=ev.target.closest('.cp');if(!b)return;var t=b.getAttribute('data-t');
function ok(){{var o=b.textContent;b.classList.add('ok');b.textContent='Copiado';setTimeout(function(){{b.classList.remove('ok');b.textContent=o}},1200)}}
function fb(){{var a=document.createElement('textarea');a.value=t;a.style.position='fixed';a.style.opacity='0';document.body.appendChild(a);a.select();try{{document.execCommand('copy');ok()}}catch(e){{}}a.remove()}}
if(navigator.clipboard&&navigator.clipboard.writeText){{navigator.clipboard.writeText(t).then(ok,fb)}}else fb()}});
</script>'''
open(sys.argv[1],'w',encoding='utf-8').write(page)
