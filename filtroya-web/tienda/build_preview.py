# Genera la vista previa de una sola página (hash routing) a partir de la tienda ya construida. Uso: build_preview.py /tmp/tienda /ruta/salida
import re,glob,posixpath,os,sys,shutil
SRC,DST=sys.argv[1],sys.argv[2]
os.chdir(SRC)
pages={os.path.dirname(f):open(f,encoding='utf-8').read() for f in glob.glob('**/index.html',recursive=True)}
key=lambda d:'inicio' if d=='' else re.sub(r'[^a-z0-9]+','-',d.lower()).strip('-')
def conv(t,d):
    def r(m):
        u=m.group(1)
        if re.match(r'(https?:|mailto:|tel:|data:|#)',u): return m.group(0)
        p=u.partition('#')[0]
        dest=posixpath.normpath(posixpath.join(d,p)) if p else d
        if dest=='.': dest=''
        return f'href="#{key(dest.rstrip("/"))}"'
    t=re.sub(r'href="([^"]*)"',r,t)
    return re.sub(r'src="(?:\.\./)*img/',r'src="img/',t)
t0=pages['']
hdr=conv(re.search(r'<div class="top">.*?</header>',t0,re.S).group(0),'').replace('action="tienda/" method="get"','id="bf"')
ftr=conv(re.search(r'<footer class="f">.*?</footer>.*?<div class="toast" id="toast"></div>',t0,re.S).group(0),'')
views=[f'<div class="vw" id="v-{key(d)}" hidden>{conv(re.search(r"</header>(.*?)<footer class=\"f\">",t,re.S).group(1),d)}</div>' for d,t in sorted(pages.items())]
css=open('tienda.css',encoding='utf-8').read();js=open('tienda.js',encoding='utf-8').read()
out=f'''<title>Tienda Repuestos Samsung</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link href="https://fonts.googleapis.com/css2?family=Kameron:wght@500;700&family=Open+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<style>{css}
body{{margin:0}}.vw[hidden]{{display:none!important}}
.top .wrap,.hr,.wrap{{padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}}
</style>
{hdr}{"".join(views)}{ftr}
<script>{js}
(function(){{function show(){{var k=(location.hash||'#inicio').slice(1)||'inicio',v=document.getElementById('v-'+k)||document.getElementById('v-inicio');[].forEach.call(document.querySelectorAll('.vw'),function(x){{x.hidden=true}});v.hidden=false;window.scrollTo(0,0);var n=document.getElementById('nav');if(n)n.classList.remove('o')}}
window.addEventListener('hashchange',show);show();
var bf=document.getElementById('bf');if(bf)bf.addEventListener('submit',function(e){{e.preventDefault();var q=document.getElementById('q');if(q){{q.value=bf.q.value;q.dispatchEvent(new Event('input'))}};location.hash='#tienda'}})}})();
</script>'''
shutil.rmtree(DST,ignore_errors=True);os.makedirs(DST+'/img')
for f in glob.glob('img/*'): shutil.copy(f,DST+'/img/')
open(DST+'/index.html','w',encoding='utf-8').write(out);print(len(out)//1024,'KB')
