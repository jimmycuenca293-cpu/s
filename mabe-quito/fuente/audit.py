import re,os,json,urllib.request,html
from urllib.parse import urljoin
B='http://127.0.0.1:8751'
urls=re.findall(r'<loc>https://serviciotecnicomabequito.click(/[^<]*)</loc>',open('site/sitemap.xml').read())
bad=[];tit={};desc={};words={};seen=set()
for u in urls:
    h=urllib.request.urlopen(B+u).read().decode()
    t=html.unescape(re.search(r'<title>([^<]*)',h).group(1)); d=html.unescape(re.search(r'<meta name="description" content="([^"]*)"',h).group(1))
    if len(t)>65: bad.append((u,'título largo',len(t)))
    if len(d)>165 or len(d)<80: bad.append((u,'descripción fuera de rango',len(d)))
    if t in tit: bad.append((u,'título repetido',tit[t]))
    if d in desc: bad.append((u,'descripción repetida',desc[d]))
    tit[t]=u;desc[d]=u
    n=len(re.findall(r'<h1[ >]',h))
    if n!=1: bad.append((u,'h1',n))
    if f'<link rel="canonical" href="https://serviciotecnicomabequito.click{u}">' not in h: bad.append((u,'canonical'))
    for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>',h,re.S):
        try: json.loads(j)
        except Exception: bad.append((u,'JSON-LD inválido'))
    txt=re.sub(r'<[^>]+>',' ',re.sub(r'<script[\s\S]*?</script>|<style[\s\S]*?</style>','',h)); words[u]=len(txt.split())
    for l in re.findall(r'(?:href|src)="([^"#]+)"',h):
        if l.startswith(('http','tel:','mailto:')): continue
        full=urljoin(B+u,l)
        if full in seen: continue
        seen.add(full)
        try: urllib.request.urlopen(full)
        except Exception: bad.append((u,'enlace/recurso roto',l))
print('páginas:',len(urls),'| problemas:',len(bad)); [print(' ',b) for b in bad[:20]]
for u,w in sorted(words.items(),key=lambda x:x[1]): print(f'  {w:5d} {u}')
