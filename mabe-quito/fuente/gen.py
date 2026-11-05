# -*- coding: utf-8 -*-
import os,re,json,shutil,html,datetime,sys,urllib.parse
from mq_base import *
from mq_ui import ICON,WA_SVG,LOGO_MARK
import mq_pages as mp
from mq_pages import PAGES,ORDER,EQ,EQK,TERMS,GUIDES,GUIDE_SLUGS,SECTOR_TERMS
from mq_zonas import Z,ZD,ZSLUGS,ZXA,AXZ,SECTOR_TXT
OUT=sys.argv[1] if len(sys.argv)>1 else 'site'
PREVIEW=len(sys.argv)>2 and sys.argv[2]=='preview'
TODAY=datetime.date.today().isoformat()
AUTH=os.environ.get('MABE_AUTH')=='1'   # fotos de técnicos con uniforme 'Servicio Autorizado': solo si el negocio es servicio autorizado
shutil.rmtree(OUT,ignore_errors=True); os.makedirs(OUT)
E=html.escape
def depth(slug): return 0 if slug=='' else slug.count('/')+1
def url(frm,to):
    up='../'*depth(frm)
    if to=='': t='index.html' if PREVIEW else ''
    else: t=to+('/index.html' if PREVIEW else '/')
    return (up+t) if (up+t) else './'
def asset(frm,name): return '../'*depth(frm)+name
def wa(msg): return f'https://wa.me/{PHONE_INTL}?text='+urllib.parse.quote(msg)
GSC=open('gsc-meta.txt',encoding='utf-8').read().strip() if os.path.exists('gsc-meta.txt') else ''
HERO='portada' if AUTH else 'portada-cocina'
PRE=f'<link rel="preload" as="image" href="img/{HERO}-m.webp" imagesrcset="img/{HERO}-m.webp 640w, img/{HERO}.webp 900w" imagesizes="100vw" fetchpriority="high">'
def fix(h,slug):
    def r(m):
        t=m.group(1)
        if t not in PAGES and t not in INFO: raise KeyError(t)
        return url(slug,t)
    return re.sub(r'@([\w-]+)@',r,h)
def head(slug,title,desc,ld=None,og='website',noindex=False):
    canon=SITE+('/' if slug=='' else '/'+slug+'/')
    lds=''.join(f'<script type="application/ld+json">{json.dumps(x,ensure_ascii=False)}</script>' for x in (ld or []))
    return f'''<!doctype html><html lang="es-EC"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">
{'<meta name="robots" content="noindex">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">'}
<link rel="canonical" href="{canon}"><link rel="alternate" hreflang="es-EC" href="{canon}">
{GSC}<meta name="theme-color" content="#0c2740"><meta name="geo.region" content="EC-P"><meta name="geo.placename" content="Quito">
<meta property="og:type" content="{og}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{canon}"><meta property="og:locale" content="es_EC"><meta property="og:site_name" content="{NAME}"><meta property="og:image" content="{SITE}/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{asset(slug,'favicon.png')}" type="image/png"><link rel="apple-touch-icon" href="{asset(slug,'apple-touch-icon.png')}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Barlow:wght@400;500;600&display=swap">
<link rel="stylesheet" href="{asset(slug,'estilo.css')}">{PRE if slug=='' else ''}{lds}</head><body>'''
NAV=[('electrodomesticos','Electrodomésticos'),('fallas-comunes','Fallas'),('servicios','Servicios'),('zonas-de-servicio-quito','Zonas'),('guias','Guías'),('como-trabajamos','Cómo trabajamos')]
WAHI='Hola, necesito servicio técnico para un electrodoméstico Mabe en Quito.'
def header(slug):
    links=''.join(f'<a href="{url(slug,s)}"{" aria-current=page" if s==slug else ""}>{n}</a>' for s,n in NAV)
    return f'''<a class="saltar" href="#contenido">Saltar al contenido</a>
<header class="top"><div class="wrap fila"><a class="logo" href="{url(slug,'')}" aria-label="{NAME}, inicio"><span class="mkimg"><img src="{asset(slug,'img/mabe-marca.png')}" alt="Mabe" width="360" height="107"></span><span class="wm"><small>Servicio técnico</small><b>MABE QUITO</b></span></a>
<nav class="menu" aria-label="Principal">{links}</nav>
<a class="btn wa" href="{wa(WAHI)}" rel="noopener" target="_blank">{WA_SVG}<span>WhatsApp</span></a>
<details class="mov"><summary aria-label="Abrir menú"><span></span></summary><nav aria-label="Menú móvil">{links}</nav></details></div></header>
<main id="contenido">'''
def footer(slug):
    eq=''.join(f'<li><a href="{url(slug,EQ[k]["slug"])}">{E(EQ[k]["corto"])}</a></li>' for k in EQK)
    zn=''.join(f'<li><a href="{url(slug,"servicio-tecnico-mabe-en-"+z)}">{E(ZD[z]["nombre"])}</a></li>' for z in ('la-carolina','cumbaya','la-villaflora','calderon','sangolqui','centro-historico'))
    return f'''</main><footer class="pie"><div class="wrap cols"><div><a class="logo" href="{url(slug,'')}"><span class="mkimg"><img src="{asset(slug,'img/mabe-marca.png')}" alt="Mabe" width="360" height="107"></span><span class="wm"><small>Servicio técnico</small><b>MABE QUITO</b></span></a><p>Reparación y mantenimiento a domicilio de refrigeradoras, lavadoras, secadoras, cocinas, hornos y más electrodomésticos Mabe en Quito.</p><p><a class="tel" href="tel:{PHONE_TEL}">{PHONE_TXT}</a><br>WhatsApp y llamadas · +593 99 350 8191</p></div>
<div><h2>Electrodomésticos</h2><ul>{eq}</ul></div>
<div><h2>Zonas</h2><ul>{zn}<li><a href="{url(slug,'zonas-de-servicio-quito')}">Todas las zonas</a></li></ul></div>
<div><h2>Más</h2><ul><li><a href="{url(slug,'servicios')}">Servicios</a></li><li><a href="{url(slug,'fallas-comunes')}">Fallas comunes</a></li><li><a href="{url(slug,'guias')}">Guías</a></li><li><a href="{url(slug,'como-trabajamos')}">Cómo trabajamos</a></li><li><a href="{url(slug,'preguntas-frecuentes')}">Preguntas frecuentes</a></li><li><a href="{url(slug,'contacto')}">Contacto</a></li><li><a href="{url(slug,'aviso-legal')}">Aviso legal</a></li><li><a href="{url(slug,'privacidad')}">Tratamiento de datos</a></li></ul></div></div>
<div class="wrap base">© {datetime.date.today().year} Servicio Técnico Mabe Quito · Quito, Ecuador</div></footer>
<a class="flota" href="{wa(WAHI)}" target="_blank" rel="noopener" aria-label="Escribir por WhatsApp">{WA_SVG}</a></body></html>'''
def write(slug,content):
    d=OUT if slug=='' else os.path.join(OUT,slug); os.makedirs(d,exist_ok=True)
    open(os.path.join(d,'index.html'),'w',encoding='utf-8').write(content)
BIZ={'@context':'https://schema.org','@type':'LocalBusiness','@id':SITE+'/#negocio','name':NAME,'url':SITE+'/','telephone':PHONE_FULL,'image':SITE+'/og.png','logo':SITE+'/img/mabe-marca.png','priceRange':'$$','description':'Servicio técnico Mabe Quito: reparación a domicilio de electrodomésticos Mabe en Quito, Ecuador: refrigeradoras, lavadoras, secadoras, cocinas y hornos.','address':{'@type':'PostalAddress','addressLocality':'Quito','addressRegion':'Pichincha','addressCountry':'EC'},'geo':{'@type':'GeoCoordinates','latitude':-0.1807,'longitude':-78.4678},'areaServed':{'@type':'City','name':'Quito','containedInPlace':{'@type':'AdministrativeArea','name':'Pichincha'}},'knowsAbout':['Reparación de refrigeradoras Mabe','Reparación de lavadoras Mabe','Reparación de secadoras Mabe','Reparación de cocinas y hornos Mabe','Mantenimiento de electrodomésticos']}
def bc_html(slug,items): return '<nav class="migas" aria-label="Ruta">'+' › '.join((f'<a href="{url(slug,s)}">{E(n)}</a>' if s!=slug else f'<span>{E(n)}</span>') for n,s in items)+'</nav>'
def bc_ld(items): return {'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':i+1,'name':n,'item':SITE+('/' if s=='' else '/'+s+'/')} for i,(n,s) in enumerate(items)]}
def faq_html(faq): return '' if not faq else '<section class="faq"><h2>Preguntas frecuentes</h2>'+''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q,a in faq)+'</section>'
def faq_ld(faq): return {'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in faq]}
def thumb(frm,k,cls=''):
    th=EQ[k].get('th')
    if th: return f'<span class="ico th {cls}"><img src="{asset(frm,"img/"+th+"-s.webp")}" alt="" width="240" height="240" loading="lazy" decoding="async"></span>'
    return ''
def pth(frm,p,cls=''):
    if p.get('eq') and p['kind'] in ('service','falla','zxa','term','guia'): return thumb(frm,p['eq'],cls)
    return ''
def related_html(slug,p):
    if not p.get('related'): return ''
    cs=''
    for s in p['related']:
        q=PAGES[s]; cs+=f'<a class="card has-th" href="{url(slug,s)}">{pth(slug,q,"sm")}<div><b>{E(q["h1"])}</b><span>{E(q["lead"][:105])}…</span></div></a>'
    return f'<section class="rel"><div class="wrap"><h2>También te puede servir</h2><div class="cards">{cs}</div></div></section>'
def cta_box(slug,p):
    return f'<aside class="caja"><h2>Servicio técnico Mabe Quito</h2><p>Escríbenos la marca, el modelo y qué falla presenta. Te orientamos por WhatsApp.</p><a class="btn wa grande" href="{wa(p["wamsg"])}" target="_blank" rel="noopener">{WA_SVG}<span>Escribir por WhatsApp</span></a><a class="btn linea" href="tel:{PHONE_TEL}">Llamar {PHONE_TXT}</a></aside>'
PH={'nevera-superior-negra':'Refrigeradora Mabe de congelador superior','nevera-superior-inox':'Refrigeradora Mabe de congelador superior en acero','nevera-side-by-side':'Refrigeradora Mabe Side by Side con dispensador','nevera-side-by-side-inox':'Refrigeradora Mabe Side by Side en acero','lavadora-superior':'Lavadora Mabe de carga superior','secadora':'Secadora Mabe','secadora-oscura':'Secadora Mabe de color oscuro','torre-lavado':'Centro de lavado Mabe (torre)','cocina-gas':'Cocina a gas Mabe de seis hornillas','horno-empotrable':'Horno empotrable Mabe'}
TECP={'tecnico-cliente':('Técnico explicando una falla a una clienta frente a la refrigeradora (imagen ilustrativa)',900,672),'tecnico-cocina':('Técnico con su caja de herramientas en una cocina con refrigeradora y lavadora (imagen ilustrativa)',900,672),'tecnico-puerta':('Técnico llegando a un domicilio (imagen ilustrativa)',900,672),'tecnico-manos':('Revisión de un electrodoméstico (imagen ilustrativa)',900,507)}
def fig(slug,n,eager=False):
    return f'<figure><img src="{asset(slug,"img/"+n+".webp")}" srcset="{asset(slug,"img/"+n+"-m.webp")} 460w, {asset(slug,"img/"+n+".webp")} 900w" sizes="(max-width:700px) 44vw, 330px" width="900" height="900" alt="{E(PH[n])}" loading="{"eager" if eager else "lazy"}" decoding="async"><figcaption>{E(PH[n])}</figcaption></figure>'
def tec_fig(slug,n):
    alt,w,h=TECP[n]
    return f'<figure class="tec"><img src="{asset(slug,"img/"+n+".webp")}" srcset="{asset(slug,"img/"+n+"-m.webp")} 560w, {asset(slug,"img/"+n+".webp")} 900w" sizes="(max-width:700px) 92vw, 700px" width="{w}" height="{h}" alt="{E(alt)}" loading="lazy" decoding="async"><figcaption>{E(alt.replace(" (imagen ilustrativa)",""))} · imagen ilustrativa</figcaption></figure>'
TECS=['tecnico-cliente','tecnico-cocina','tecnico-puerta','tecnico-manos']
def tec_for(slug,p):
    if not AUTH: return None
    k=p['kind']
    if k=='service': return {'refrigeradoras':'tecnico-cliente','lavadoras':'tecnico-cocina','secadoras':'tecnico-puerta','cocinas':'tecnico-manos','hornos':'tecnico-manos'}.get(p['eq'])
    if k=='zona': return TECS[ZSLUGS.index(p['zone'])%4]
    if k=='term': return TECS[sum(map(ord,slug))%4]
    return None
def galeria(slug,p):
    t=tec_for(slug,p); t=tec_fig(slug,t) if t else ''
    ph=list(p.get('photos') or [])
    if not ph:
        k=p['kind']
        if k in ('falla','zxa','term','guia') and p.get('eq') and EQ[p['eq']]['foto']:
            pool=EQ[p['eq']]['foto']; o=sum(map(ord,slug))%len(pool); ph=(pool[o:]+pool[:o])[:2]
        elif k=='zona':
            allp=list(PH.keys()); o=ZSLUGS.index(p['zone'])%len(allp); ph=(allp[o:]+allp[:o])[:3]
    g=('<div class="gal">'+''.join(fig(slug,n,i==0) for i,n in enumerate(ph))+'</div><p class="refimg">Imágenes de referencia de equipos Mabe.</p>') if ph else ''
    return t+g
def crumbs(slug,p):
    it=[('Inicio','')]; k=p['kind']
    if k=='service': it.append(('Electrodomésticos','electrodomesticos'))
    elif k=='falla': it.append(('Fallas comunes','fallas-comunes')); it.append((EQ[p['eq']]['h1'].replace(' en Quito',''),EQ[p['eq']]['slug']))
    elif k=='zona': it.append(('Zonas','zonas-de-servicio-quito'))
    elif k=='zxa': it.append(('Zonas','zonas-de-servicio-quito')); it.append((ZD[p['zone']]['nombre'],'servicio-tecnico-mabe-en-'+p['zone']))
    elif k=='term': it.append(('Servicios','servicios'))
    elif k=='guia': it.append(('Guías','guias'))
    it.append((p['h1'],slug)); return it
def page(slug):
    p=PAGES[slug]; items=crumbs(slug,p); ld=[BIZ,bc_ld(items)]
    if p['kind'] in ('service','zona','zxa','term'):
        ld.append({'@context':'https://schema.org','@type':'Service','name':p['h1'],'serviceType':p['h1'],'provider':{'@id':SITE+'/#negocio'},'areaServed':{'@type':'City','name':'Quito'},'url':SITE+'/'+slug+'/','description':p['desc']})
    if p['kind'] in ('guia','falla'):
        ld.append({'@context':'https://schema.org','@type':'Article','headline':p['h1'],'description':p['desc'],'inLanguage':'es-EC','datePublished':TODAY,'dateModified':TODAY,'author':{'@type':'Organization','name':NAME},'publisher':{'@id':SITE+'/#negocio'},'mainEntityOfPage':SITE+'/'+slug+'/'})
    if p['faq']: ld.append(faq_ld(p['faq']))
    secs=''.join(f'<section><h2>{E(h)}</h2>{fix(b,slug)}</section>' for h,b in p['sections'])
    hero=f'<section class="phero"><div class="wrap">{bc_html(slug,items)}<p class="kick">Servicio técnico Mabe Quito</p><div class="ph-fila">{pth(slug,p,"big")}<div><h1>{E(p["h1"])}</h1><p class="lead">{E(p["lead"])}</p></div></div><div class="acc"><a class="btn wa grande" href="{wa(p["wamsg"])}" target="_blank" rel="noopener">{WA_SVG}<span>Cotizar por WhatsApp</span></a><a class="btn linea cl" href="tel:{PHONE_TEL}">Llamar {PHONE_TXT}</a></div></div></section>'
    body=f'<div class="wrap lay"><article class="art">{galeria(slug,p)}{secs}{faq_html(p["faq"])}</article>{cta_box(slug,p)}</div>{related_html(slug,p)}'
    write(slug,head(slug,p['title'],p['desc'],ld,'article' if p['kind'] in ('guia','falla') else 'website')+header(slug)+hero+body+footer(slug))
INFO={'electrodomesticos','fallas-comunes','servicios','zonas-de-servicio-quito','guias','como-trabajamos','preguntas-frecuentes','contacto','aviso-legal','privacidad'}
def info_page(slug,h1,title,desc,lead,body_html,faq=None,icon='home',wamsg=WAHI,wide=False):
    items=[('Inicio',''),(h1,slug)]; ld=[BIZ,bc_ld(items)]+([faq_ld(faq)] if faq else [])
    hero=f'<section class="phero"><div class="wrap">{bc_html(slug,items)}<p class="kick">Servicio técnico Mabe Quito</p><div class="ph-fila"><div><h1>{E(h1)}</h1><p class="lead">{E(lead)}</p></div></div></div></section>'
    body=f'<div class="wrap lay1"><article class="art wide">{fix(body_html,slug)}{faq_html(faq)}</article></div>'
    write(slug,head(slug,title,desc,ld)+header(slug)+hero+body+footer(slug))
def cardlist(slug,slugs,cls='cards g2'):
    return f'<div class="{cls}">'+''.join(f'<a class="card has-th" href="{url(slug,s)}">{pth(slug,PAGES[s],"sm")}<div><b>{E(PAGES[s]["h1"])}</b><span>{E(PAGES[s]["lead"][:105])}…</span></div></a>' for s in slugs)+'</div>'
def chips(slug,slugs,label=None):
    return '<div class="chips">'+''.join(f'<a href="{url(slug,s)}">{E(label(s) if label else PAGES[s]["h1"])}</a>' for s in slugs)+'</div>'
# ---------------- páginas ----------------
for s in ORDER: page(s)
HOMEFAQ=[('¿Hacen servicio técnico Mabe a domicilio en Quito?','Sí. Vamos a tu casa, apartamento u oficina en Quito: norte, centro, sur y valles. Escríbenos por WhatsApp con el equipo, el modelo y la falla.'),
('¿Qué electrodomésticos Mabe reparan?','Refrigeradoras, congeladores, lavadoras, secadoras, centros de lavado, cocinas, hornos, parrillas, campanas, microondas y lavavajillas.'),
('¿Qué hago si mi equipo está en garantía?','Revisa primero las condiciones de la garantía de fábrica. Si ya venció o necesitas un diagnóstico, escríbenos por WhatsApp.'),
('¿Cuánto cuesta la visita?','Escríbenos al WhatsApp con el equipo, el modelo y la falla; te confirmamos el costo de la visita antes de ir.'),
('¿Dan el costo antes de reparar?','Sí. Primero diagnosticamos, te explicamos la falla y te informamos el costo antes de continuar.'),
('¿Cómo pido el servicio?','Por WhatsApp o llamada al 099 350 8191 (+593 99 350 8191). Envía marca, modelo, falla, tu barrio y, si puedes, una foto de la etiqueta y un video corto.')]
# --- hubs
info_page('electrodomesticos','Electrodomésticos Mabe que reparamos en Quito','Electrodomésticos Mabe que reparamos en Quito | Mabe Quito','Reparamos refrigeradoras, congeladores, lavadoras, secadoras, centros de lavado, cocinas, hornos, parrillas, campanas, microondas y lavavajillas Mabe en Quito.','Elige tu electrodoméstico para ver fallas comunes, mantenimiento y cómo pedir la visita a domicilio.',
 '<section>'+cardlist('electrodomesticos',[EQ[k]['slug'] for k in EQK])+'</section><section><h2>¿No ves tu equipo?</h2><p>Escríbenos por WhatsApp con la marca y el modelo y te confirmamos si podemos atenderlo.</p></section>',icon='wrench')
fh=''
for k in EQK:
    e=EQ[k]; fh+=f'<section><h2><a href="@{e["slug"]}@">{E(e["corto"])}</a></h2><ul class="fallas">'+''.join(f'<li><a href="@{s}@">{E(PAGES[s]["h1"])}</a> <span class="tag {mp.URG[e["fallas"][i][2]]}">{e["fallas"][i][2]}</span></li>' for i,s in enumerate(e['slugs']))+'</ul></section>'
info_page('fallas-comunes','Fallas comunes de electrodomésticos Mabe en Quito','Fallas comunes de electrodomésticos Mabe en Quito','Todas las fallas comunes de refrigeradoras, lavadoras, secadoras, cocinas, hornos y más equipos Mabe: causas, qué revisar y cuándo llamar a un técnico en Quito.','Encuentra tu falla, mira qué puedes revisar tú con seguridad y cuándo conviene pedir un técnico.',fh,icon='help')
GEN=['tecnico-mabe-a-domicilio-quito','servicio-tecnico-mabe-cerca-de-mi-quito','reparacion-de-electrodomesticos-mabe-a-domicilio-quito','servicio-tecnico-de-electrodomesticos-quito','tecnico-de-electrodomesticos-a-domicilio-quito','mantenimiento-preventivo-de-electrodomesticos-mabe-quito','instalacion-de-electrodomesticos-mabe-quito','diagnostico-de-electrodomesticos-mabe-quito','reparacion-de-tarjetas-electronicas-de-electrodomesticos-mabe-quito','repuestos-para-electrodomesticos-mabe-quito','servicio-tecnico-mabe-edificios-y-conjuntos-quito','centro-de-servicio-mabe-quito','servicio-tecnico-mabe-telefono-y-whatsapp-quito','revision-de-electrodomesticos-mabe-usados-antes-de-comprar-quito','emergencias-de-electrodomesticos-mabe-fugas-de-agua-y-gas-quito','reparar-electrodomesticos-mabe-quito','donde-reparar-electrodomesticos-mabe-quito','mabe-quito-servicio-tecnico-y-reparacion','electrodomestico-mabe-no-funciona-que-hacer-en-quito']
EQT=[s for s in TERMS if s not in GEN and s not in SECTOR_TERMS]
sv=f'<section><h2>Servicios</h2>{cardlist("servicios",GEN)}</section><section><h2>Por tipo de equipo</h2>{cardlist("servicios",EQT)}</section><section><h2>Por zona de Quito</h2>{cardlist("servicios",SECTOR_TERMS)}</section>'
info_page('servicios','Servicios de reparación y mantenimiento Mabe en Quito','Servicios de reparación y mantenimiento Mabe en Quito','Servicio técnico a domicilio, mantenimiento, instalación, diagnóstico y reparación de electrodomésticos Mabe en Quito, por equipo y por zona.','Todo lo que hacemos por tus electrodomésticos Mabe en Quito, organizado por servicio, equipo y zona.',sv,icon='wrench')
gh=f'<section>{cardlist("guias",GUIDE_SLUGS)}</section>'
info_page('guias','Guías de electrodomésticos Mabe para Quito','Guías de electrodomésticos Mabe para Quito | Mabe Quito','Guías prácticas sobre refrigeradoras, lavadoras, secadoras, cocinas y hornos Mabe: gas, voltaje, mantenimiento y cuándo reparar, pensadas para Quito.','Explicaciones claras para cuidar tus electrodomésticos y entender qué les pasa.',gh,icon='doc')
zh=''
for sec,lab in (('Norte','Norte de Quito'),('Centro','Centro de Quito'),('Sur','Sur de Quito'),('Valles','Valles')):
    zs=[z for z in ZSLUGS if ZD[z]['sector']==sec]
    zh+=f'<section><h2>{lab}</h2>'+chips('zonas-de-servicio-quito',['servicio-tecnico-mabe-en-'+z for z in zs],lambda s:ZD[s.replace("servicio-tecnico-mabe-en-","")]['nombre'])+'</section>'
zh+='<section><h2>Por sector</h2>'+chips('zonas-de-servicio-quito',SECTOR_TERMS)+'</section><section><h2>Reparación por equipo en tu zona</h2><p>Estos sectores tienen páginas por electrodoméstico:</p>'+chips('zonas-de-servicio-quito',['servicio-tecnico-mabe-en-'+z for z in ZXA],lambda s:ZD[s.replace("servicio-tecnico-mabe-en-","")]['nombre'])+'</section><section><h2>¿Tu barrio no aparece?</h2><p>Escríbenos tu dirección por WhatsApp. Muchas veces podemos atender sectores cercanos.</p></section>'
info_page('zonas-de-servicio-quito','Zonas de servicio Mabe en Quito','Zonas de servicio técnico Mabe en Quito | Mabe Quito','Servicio técnico Mabe a domicilio en el norte, centro, sur y valles de Quito: La Carolina, Cumbayá, Villaflora, Calderón, Sangolquí y más.','Elige tu barrio para ver cómo coordinamos la visita en tu zona.',zh,icon='pin')
pasos=[('Escríbenos','Por WhatsApp o llamada al 099 350 8191. Cuéntanos qué equipo es, la marca, el modelo y la falla.'),('Envía datos y fotos','Una foto de la etiqueta del equipo y un video corto de la falla ayudan a orientarte mejor.'),('Coordinamos la visita','Acordamos día y hora en tu casa, apartamento u oficina de Quito.'),('Diagnóstico en tu casa','Probamos el equipo, identificamos la causa y te explicamos qué tiene.'),('Costo antes de reparar','Te informamos el costo y tú decides si continuamos.'),('Reparación y prueba','Reparamos y probamos que el equipo quede funcionando.'),('Recomendaciones','Te decimos cómo usarlo y cuidarlo para que la falla no se repita.')]
ch=f'<section><h2>Paso a paso</h2><ol class="pasos l">'+''.join(f'<li><b>{i+1}</b><div><h3>{E(a)}</h3><p>{E(b)}</p></div></li>' for i,(a,b) in enumerate(pasos))+'</ol></section><section><h2>Nuestro compromiso con la claridad</h2><p>No cambiamos piezas al azar: primero probamos y diagnosticamos. Si no conviene reparar, te lo decimos.</p></section>'
info_page('como-trabajamos','Cómo trabajamos: servicio técnico Mabe paso a paso','Cómo trabajamos el servicio técnico Mabe en Quito','Así es el servicio técnico Mabe a domicilio en Quito: contacto por WhatsApp, diagnóstico, costo antes de reparar, reparación y recomendaciones.','Del primer mensaje a la reparación: así trabajamos, sin sorpresas.',ch,icon='shield')
FAQ_ALL=HOMEFAQ+[('¿Reparan solo Mabe?','Nos enfocamos en electrodomésticos Mabe. Si tienes otra marca, escríbenos y te decimos si podemos ayudarte.'),('¿Qué hago si huele a gas?','Cierra la llave, ventila, no uses llama ni interruptores y llama a un técnico. Si hay riesgo, llama a emergencias (911).'),('¿Atienden apartamentos y conjuntos?','Sí. Coordinamos acceso y horario con la administración.'),('¿Qué datos debo enviar por WhatsApp?','Tipo de equipo, marca y modelo, la falla, tu barrio y una foto de la etiqueta si puedes.'),('¿Instalan electrodomésticos?','Consulta por WhatsApp con el modelo y el tipo de conexión (agua, gas o electricidad) para confirmarte el servicio.'),('¿Qué zonas de Quito atienden?','Norte, centro, sur y valles: La Carolina, Iñaquito, Cotocollao, Villaflora, Quitumbe, Cumbayá, Tumbaco, Calderón, Sangolquí y más. Consulta la lista completa en Zonas.')]
info_page('preguntas-frecuentes','Preguntas frecuentes sobre el servicio técnico Mabe en Quito','Preguntas frecuentes: servicio técnico Mabe en Quito','Respuestas sobre el servicio técnico Mabe a domicilio en Quito: equipos, zonas, costo de la visita, garantía de fábrica y cómo pedir el servicio.','Lo que más nos preguntan antes de pedir una visita.','',faq=FAQ_ALL,icon='help')
info_page('contacto','Contacto: servicio técnico Mabe en Quito','Contacto servicio técnico Mabe Quito | WhatsApp 099 350 8191','Contacta al servicio técnico Mabe en Quito por WhatsApp o llamada al 099 350 8191 (+593 99 350 8191). Cuéntanos tu equipo y la falla.','Escríbenos por WhatsApp o llámanos. Te respondemos con el siguiente paso.',
 f'<section><h2>Pide tu visita</h2><p><a class="btn wa grande" href="{wa(WAHI)}" target="_blank" rel="noopener">{WA_SVG}<span>Escribir por WhatsApp</span></a> <a class="btn linea" href="tel:{PHONE_TEL}">Llamar {PHONE_TXT}</a></p><p>Número: <b>{PHONE_TXT}</b> ({PHONE_FULL}).</p></section><section><h2>Qué contarnos</h2><ul><li>Qué equipo es y su marca y modelo</li><li>Qué falla presenta y desde cuándo</li><li>Tu barrio o sector de Quito</li><li>Si puedes, una foto de la etiqueta y un video corto del problema</li></ul></section><section><h2>Dónde atendemos</h2><p>Quito: norte, centro, sur y valles. Mira la lista en <a href="@zonas-de-servicio-quito@">Zonas</a>.</p></section>',icon='chat')
info_page('aviso-legal','Aviso legal','Aviso legal | Servicio Técnico Mabe Quito','Aviso legal de Servicio Técnico Mabe Quito: uso de marcas y alcance de la información del sitio.','Uso de marcas y alcance de la información de este sitio.',
 '<section><h2>Marcas</h2><p>Mabe es una marca de su respectivo titular. Este sitio no es operado por Mabe.</p></section><section><h2>Información orientativa</h2><p>El contenido de este sitio es orientativo. El diagnóstico definitivo y el costo se confirman en la visita. Las imágenes marcadas como ilustrativas o de referencia no corresponden necesariamente a equipos o personas concretas.</p></section><section><h2>Garantía de fábrica</h2><p>Si tu equipo está en garantía de fábrica, consulta las condiciones con el fabricante antes de solicitar una reparación independiente.</p></section>',icon='shield')
info_page('privacidad','Tratamiento de datos personales','Tratamiento de datos personales | Servicio Técnico Mabe Quito','Cómo trata Servicio Técnico Mabe Quito tus datos personales cuando nos escribes por WhatsApp o nos llamas para pedir una visita en Quito.','Qué datos recibimos y para qué los usamos.',
 f'<section><h2>Qué datos recibimos</h2><p>Cuando nos escribes por WhatsApp o nos llamas recibimos los datos que compartes: nombre, teléfono, barrio o dirección y datos del equipo.</p></section><section><h2>Para qué los usamos</h2><p>Solo para atender tu solicitud, coordinar la visita y dar seguimiento al servicio. No vendemos tus datos.</p></section><section><h2>Tus derechos</h2><p>Puedes pedirnos que corrijamos o eliminemos tus datos escribiendo al {PHONE_TXT}.</p></section>',icon='doc')
# --- portada
HERO_ALT='Técnico explicando una falla a una clienta frente a la refrigeradora (imagen ilustrativa)' if AUTH else 'Cocina con refrigeradora Mabe de dos puertas (imagen de referencia)'
def home():
    s=''
    eqcards=''.join(f'<a class="svc" href="{url(s,EQ[k]["slug"])}">{thumb(s,k)}<b>{E(EQ[k]["h1"])}</b><span>{E(EQ[k]["intro"][:115])}…</span><i>Ver servicio →</i></a>' for k in EQK)
    termchips=chips(s,list(TERMS.keys()),lambda x:TERMS[x]['h1'].replace(' en Quito',''))
    topf=[sl for k in EQK for sl in EQ[k]['slugs'][:3]]
    fchips=chips(s,topf,lambda x:PAGES[x]['h1'])
    zchips=''
    for sec,lab in (('Norte','Norte'),('Centro','Centro'),('Sur','Sur'),('Valles','Valles')):
        zchips+=f'<h3 class="zt">{lab}</h3>'+chips(s,['servicio-tecnico-mabe-en-'+z for z in ZSLUGS if ZD[z]['sector']==sec],lambda x:ZD[x.replace("servicio-tecnico-mabe-en-","")]['nombre'])
    gcards=cardlist(s,GUIDE_SLUGS[:6])
    ps=''.join(f'<li><b>{i+1}</b><div><h3>{E(a)}</h3><p>{E(b)}</p></div></li>' for i,(a,b) in enumerate([pasos[0],pasos[3],pasos[4],pasos[5]]))
    tecs=''.join(f'<div>{tec_fig(s,n)}</div>' for n in ('tecnico-cocina','tecnico-puerta','tecnico-manos'))
    if AUTH: ASI=f'<section class="sec osc"><div class="wrap"><h2>Así te atendemos</h2><p class="sub">Vamos hasta donde está tu equipo, lo revisamos y te explicamos antes de reparar.</p><div class="tecs">{tecs}</div><p class="refimg">Imágenes ilustrativas.</p></div></section>'
    else: ASI='<section class="sec osc"><div class="wrap"><h2>Equipos Mabe que atendemos</h2><p class="sub">Algunos de los modelos de la marca que revisamos a domicilio en Quito.</p><div class="gal g3">'+''.join(fig(s,n) for n in ('nevera-side-by-side','lavadora-superior','secadora','torre-lavado','cocina-gas','horno-empotrable'))+'</div><p class="refimg">Imágenes de referencia de equipos Mabe.</p></div></section>'
    qs=[('Para tu casa','Refrigeradoras, lavadoras, secadoras, cocinas y hornos Mabe en tu hogar.'),('Para apartamentos y conjuntos','Coordinamos acceso y horario con la administración.'),('Para pequeños negocios','Equipos Mabe en oficinas, locales y cafeterías pequeñas.')]
    qh=''.join(f'<div class="q"><h3>{a}</h3><p>{b}</p></div>' for a,b in qs)
    hero=f'''<section class="hero"><div class="hero-bg"><img src="img/{HERO}.webp" srcset="img/{HERO}-m.webp 640w, img/{HERO}.webp 900w" sizes="100vw" width="900" height="{672 if AUTH else 900}" alt="{HERO_ALT}" fetchpriority="high" decoding="async"></div><div class="wrap hgrid"><div><p class="kick">Reparación de electrodomésticos a domicilio</p><h1>Servicio técnico Mabe Quito</h1><p class="lead">Reparación de electrodomésticos Mabe en Quito: refrigeradoras, lavadoras, secadoras, cocinas, hornos y más, en tu casa. Diagnóstico claro y costo antes de reparar.</p><div class="acc"><a class="btn wa grande" href="{wa(WAHI)}" target="_blank" rel="noopener">{WA_SVG}<span>Escribir por WhatsApp</span></a><a class="btn linea cl" href="tel:{PHONE_TEL}">Llamar {PHONE_TXT}</a></div><ul class="pts"><li>A domicilio en Quito</li><li>Norte, centro, sur y valles</li><li>Te explicamos la falla antes de reparar</li></ul></div></div></section>'''
    body=f'''<section class="sec" id="electrodomesticos"><div class="wrap"><h2>Electrodomésticos Mabe que reparamos en Quito</h2><p class="sub">Elige tu equipo para ver fallas comunes, mantenimiento y cómo pedir la visita.</p><div class="svcs">{eqcards}</div></div></section>
<section class="sec osc" id="servicios"><div class="wrap"><h2>Lo que más se busca en Quito</h2><p class="sub">Servicios, equipos y zonas: cada búsqueda tiene su página con respuestas claras.</p>{termchips}</div></section>
<section class="sec"><div class="wrap"><h2>¿Qué le pasa a tu equipo?</h2><p class="sub">Estas son las fallas por las que más nos escriben. Cada una explica qué revisar antes de llamar.</p>{fchips}<p style="margin-top:22px"><a class="enlace" href="{url(s,'fallas-comunes')}">Ver todas las fallas →</a></p></div></section>
{ASI}
<section class="sec"><div class="wrap"><h2>Cómo trabajamos</h2><ol class="pasos">{ps}</ol><p style="margin-top:22px"><a class="enlace" href="{url(s,'como-trabajamos')}">Ver el proceso completo paso a paso →</a></p></div></section>
<section class="sec osc" id="zonas"><div class="wrap"><h2>Zonas de Quito donde atendemos</h2><p class="sub">Norte, centro, sur y valles. Si tu barrio no aparece, escríbenos.</p>{zchips}<p style="margin-top:22px"><a class="enlace" href="{url(s,'zonas-de-servicio-quito')}">Ver todas las zonas →</a></p></div></section>
<section class="sec"><div class="wrap"><h2>Guías para entender y cuidar tus electrodomésticos</h2><p class="sub">Gas, voltaje, limpieza y fallas explicadas para Quito.</p>{gcards}<p style="margin-top:22px"><a class="enlace" href="{url(s,'guias')}">Ver todas las guías →</a></p></div></section>
<section class="sec osc"><div class="wrap"><h2>Para quién es el servicio</h2><div class="qs">{qh}</div></div></section>
<section class="sec"><div class="wrap lay1">{faq_html(HOMEFAQ)}</div></section>
<section class="final"><div class="wrap"><h2>¿Tu electrodoméstico está fallando?</h2><p>Escríbenos por WhatsApp con la marca, el modelo y la falla. Te orientamos y coordinamos la visita.</p><a class="btn wa grande" href="{wa(WAHI)}" target="_blank" rel="noopener">{WA_SVG}<span>Escribir por WhatsApp</span></a> <a class="btn linea cl" href="tel:{PHONE_TEL}">Llamar {PHONE_TXT}</a></div></section>'''
    ld=[BIZ,{'@context':'https://schema.org','@type':'WebSite','url':SITE+'/','name':NAME,'inLanguage':'es-EC'},faq_ld(HOMEFAQ)]
    write('',head('','Servicio Técnico Mabe Quito: Reparación de Electrodomésticos','Servicio técnico Mabe Quito: reparación de electrodomésticos Mabe a domicilio, refrigeradoras, lavadoras, secadoras, cocinas y hornos. WhatsApp 099 350 8191.',ld)+header('')+hero+body+footer(''))
home()
write('404',head('404','Página no encontrada | Mabe Quito','Esta página no existe.',None,noindex=True)+header('404')+'<section class="phero"><div class="wrap"><h1>Página no encontrada</h1><p class="lead">Puede que el enlace haya cambiado. Vuelve al inicio o escríbenos por WhatsApp.</p></div></section>'+footer('404'))
# ---------------- archivos técnicos ----------------
allp=['']+sorted(INFO)+ORDER
sm='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{SITE}/{s+"/" if s else ""}</loc><lastmod>{TODAY}</lastmod></url>' for s in allp)+'</urlset>'
open(os.path.join(OUT,'sitemap.xml'),'w',encoding='utf-8').write(sm)
open(os.path.join(OUT,'robots.txt'),'w').write(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
open(os.path.join(OUT,'llms.txt'),'w',encoding='utf-8').write(f'# {NAME}\n> Servicio técnico Mabe Quito: reparación a domicilio de electrodomésticos Mabe en Quito, Ecuador. WhatsApp {PHONE_FULL}.\n\n## Secciones\n- {SITE}/electrodomesticos/ : equipos que reparamos\n- {SITE}/fallas-comunes/ : fallas y qué revisar\n- {SITE}/zonas-de-servicio-quito/ : zonas de Quito\n- {SITE}/guias/ : guías\n- {SITE}/como-trabajamos/ : proceso\n')
open(os.path.join(OUT,'.htaccess'),'w').write('ErrorDocument 404 /404/\nRewriteEngine On\nRewriteCond %{HTTPS} off\nRewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]\nRewriteCond %{HTTP_HOST} ^www\\.(.+)$ [NC]\nRewriteRule ^ https://%1%{REQUEST_URI} [L,R=301]\n<IfModule mod_deflate.c>\nAddOutputFilterByType DEFLATE text/html text/css application/javascript image/svg+xml application/xml\n</IfModule>\n<IfModule mod_expires.c>\nExpiresActive On\nExpiresByType text/css "access plus 30 days"\nExpiresByType image/webp "access plus 180 days"\nExpiresByType image/png "access plus 30 days"\nExpiresByType image/svg+xml "access plus 30 days"\n</IfModule>\n')
shutil.copy('estilo.css',os.path.join(OUT,'estilo.css'))
shutil.copytree('img',os.path.join(OUT,'img'))
if os.path.isdir('assets'):
    for f in os.listdir('assets'): shutil.copy(os.path.join('assets',f),os.path.join(OUT,f))
print('páginas html:',sum(1 for r,_,fs in os.walk(OUT) for f in fs if f=='index.html'))
