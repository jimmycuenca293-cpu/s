# Vista previa en una sola página de una tienda PHP ya generada (ads_bm.py): las páginas .html salen del disco y las .php se piden al servidor local.
# Uso: python3 build_preview_php.py <carpeta_del_sitio> <url_servidor_php> <carpeta_de_salida> [titulo]
import re, sys, os, shutil, glob, urllib.request
SITE, BASE, DST = sys.argv[1], sys.argv[2].rstrip("/"), sys.argv[3]
TITULO = sys.argv[4] if len(sys.argv) > 4 else "Tienda Breakermatic"
key = lambda n: re.sub(r"[^a-z0-9]+", "-", re.sub(r"\.(html|php)$", "", n).lower()).strip("-") or "inicio"
pages = {}
for f in sorted(glob.glob(SITE + "/*.html")):
    n = os.path.basename(f)
    if n == "404.html": continue
    pages[key("inicio" if n == "index.html" else n)] = open(f, encoding="utf-8").read()
for n in ("carrito.php", "terminos.php", "privacidad.php", "garantia-y-retracto.php"):
    pages[key(n)] = urllib.request.urlopen(f"{BASE}/{n}").read().decode("utf-8")
def partir(t):
    h0 = t.index('<div class="aq-h">'); fo = t.index('<footer class="aq-f">')
    h1 = t.index("</nav></div>", h0) + len("</nav></div>")
    f1 = t.index("</a>", t.index('<a class="aq-wa"', fo)) + 4
    return t[h0:h1], t[h1:fo], t[fo:f1]
def enlaces(t):
    def r(m):
        u = m.group(1)
        if re.match(r"(https?:|mailto:|tel:|#|/api)", u): return m.group(0)
        p = u.split("#")[0].lstrip("/")
        return f'href="#{key(p) if p else "inicio"}"'
    return re.sub(r'href="([^"]*)"', r, t)
hdr, _, ftr = partir(pages["inicio"])
views = []
for k, t in pages.items():
    _, cuerpo, _ = partir(t)
    cuerpo = re.sub(r"<script src=[^>]*></script>", "", cuerpo)
    views.append(f'<div class="vw" id="v-{k}" hidden>{enlaces(cuerpo)}</div>')
css = "".join(open(f"{SITE}/{n}", encoding="utf-8").read() for n in ("tema.css", "pasarela.css", "aqua-shell.css", "estilo.css") if os.path.exists(f"{SITE}/{n}"))
js = open(f"{SITE}/buscar.js", encoding="utf-8").read() + "\n" + (open(f"{SITE}/pedido.js", encoding="utf-8").read() + "\n" if os.path.exists(f"{SITE}/pedido.js") else "") + (open(f"{SITE}/tech.js", encoding="utf-8").read() + "\n" if os.path.exists(f"{SITE}/tech.js") else "") + open(f"{SITE}/carrito.js", encoding="utf-8").read().replace('"/carrito.php"', '"#carrito"').replace('/carrito.php', '#carrito')
out = f'''<title>{TITULO}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{css}
body{{margin:0}}.vw[hidden]{{display:none!important}}</style>
{enlaces(hdr)}{"".join(views)}{enlaces(ftr)}
<script>{js}</script>
<script>(function(){{function show(){{var k=(location.hash||'#inicio').slice(1)||'inicio',v=document.getElementById('v-'+k)||document.getElementById('v-inicio');[].forEach.call(document.querySelectorAll('.vw'),function(x){{x.hidden=true}});v.hidden=false;window.scrollTo(0,0)}}window.addEventListener('hashchange',function(){{if((location.hash||'')==='#carrito'){{location.reload();return}}show()}});show()}})();</script>'''
shutil.rmtree(DST, ignore_errors=True); os.makedirs(DST + "/img")
for f in glob.glob(SITE + "/img/*"): shutil.copy(f, DST + "/img/")
open(DST + "/index.html", "w", encoding="utf-8").write(out); print(len(out) // 1024, "KB", len(views), "vistas")
