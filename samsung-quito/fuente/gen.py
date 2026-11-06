# -*- coding: utf-8 -*-
import os,re,json,shutil,html,datetime,sys,urllib.parse
from mq_base import *
from mq_ui import ICON,WA_SVG,LOGO_MARK
import mq_pages as mp
from mq_pages import PAGES,ORDER,EQ,EQK,TERMS,GUIDES,GUIDE_SLUGS,SECTOR_TERMS,SECTOR_HUBS,GEN,TPRIM,GEQ,VALLE_TERMS
from mq_zonas import Z,ZD,ZSLUGS,ZXA,AXZ,SECTOR_TXT
OUT=sys.argv[1] if len(sys.argv)>1 else 'site'
PREVIEW=len(sys.argv)>2 and sys.argv[2]=='preview'
TODAY=datetime.date.today().isoformat()
AUTH=os.environ.get('SAMSUNG_AUTH')=='1'   # fotos de técnicos con uniforme 'Servicio Autorizado': solo si el negocio es servicio autorizado
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
HERO='portada-tecnico'
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
{GSC}<meta name="theme-color" content="#0b2a45"><meta name="geo.region" content="EC-P"><meta name="geo.placename" content="Quito">
<meta property="og:type" content="{og}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{canon}"><meta property="og:locale" content="es_EC"><meta property="og:site_name" content="{NAME}"><meta property="og:image" content="{SITE}/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{asset(slug,'favicon.png')}" type="image/png"><link rel="apple-touch-icon" href="{asset(slug,'apple-touch-icon.png')}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="{asset(slug,'estilo.css')}">{PRE if slug=='' else ''}{lds}</head><body>'''
CORE=['reparacion-de-electrodomesticos-samsung-a-domicilio-quito','mantenimiento-preventivo-de-electrodomesticos-samsung-quito','instalacion-de-electrodomesticos-samsung-quito','diagnostico-de-electrodomesticos-samsung-quito','reparacion-de-tarjetas-electronicas-de-electrodomesticos-samsung-quito','repuestos-para-electrodomesticos-samsung-quito']
CORE_LAB={CORE[0]:'Reparación a domicilio',CORE[1]:'Mantenimiento preventivo',CORE[2]:'Instalación',CORE[3]:'Diagnóstico',CORE[4]:'Tarjetas electrónicas',CORE[5]:'Repuestos'}
WAHI='Hola, necesito servicio técnico para un electrodoméstico Samsung en Quito.'
SEC_LAB=[('Norte','Norte de Quito'),('Centro','Centro de Quito'),('Sur','Sur de Quito'),('Valles','Valles de Quito')]
def menu_groups(slug):
    u=lambda s:url(slug,s)
    return [
     ('Electrodomésticos','electrodomesticos',[(EQ[k]['corto'],EQ[k]['slug']) for k in EQK]+[('Ver todos','electrodomesticos')]),
     ('Servicios','servicios',[(CORE_LAB[c],c) for c in CORE]+[('Cómo trabajamos','como-trabajamos'),('Ver todos los servicios','servicios')]),
     ('Cobertura','zonas-de-servicio-quito',[(lab,SECTOR_HUBS[sc][0]) for sc,lab in SEC_LAB]+[('Todos los barrios','zonas-de-servicio-quito')]),
     ('Fallas','fallas-comunes',None),('Guías','guias',None),('Contacto','contacto',None)]
def header(slug):
    u=lambda s:url(slug,s)
    top='';mov=''
    for lab,s,sub in menu_groups(slug):
        cur=' aria-current=page' if s==slug else ''
        if sub:
            top+=f'<div class="dd"><a href="{u(s)}"{cur}>{lab}</a><div class="pn">'+''.join(f'<a href="{u(t)}">{E(n)}</a>' for n,t in sub)+'</div></div>'
            mov+=f'<b class="mh">{lab}</b>'+''.join(f'<a href="{u(t)}">{E(n)}</a>' for n,t in sub)
        else:
            top+=f'<a href="{u(s)}"{cur}>{lab}</a>'; mov+=f'<b class="mh">{lab}</b>'+f'<a href="{u(s)}">Ver {lab.lower()}</a>' if False else f'<a class="mh1" href="{u(s)}">{lab}</a>'
    LOGO=f'<a class="logo" href="{u("")}" aria-label="{NAME}, inicio"><img class="logoimg" src="{asset(slug,"img/samsung-logo.png")}" alt="Samsung, servicio técnico Samsung Quito" width="200" height="60"><span class="wm"><small>Servicio técnico</small><b>QUITO</b></span></a>'
    return f'''<a class="saltar" href="#contenido">Saltar al contenido</a>
<div class="topbar"><div class="wrap"><span>Servicio técnico Samsung Quito · reparación a domicilio</span><a href="{wa(WAHI)}" target="_blank" rel="noopener">WhatsApp {PHONE_TXT}</a></div></div>
<header class="top"><div class="wrap fila">{LOGO}
<nav class="menu" aria-label="Principal">{top}</nav>
<a class="btn wa" href="{wa(WAHI)}" rel="noopener" target="_blank">{WA_SVG}<span>WhatsApp</span></a>
<details class="mov"><summary aria-label="Abrir menú"><span></span></summary><nav aria-label="Menú móvil">{mov}</nav></details></div></header>
<main id="contenido">'''
def footer(slug):
    u=lambda s:url(slug,s)
    eq=''.join(f'<li><a href="{u(EQ[k]["slug"])}">{E(EQ[k]["corto"])}</a></li>' for k in EQK)
    sv=''.join(f'<li><a href="{u(c)}">{CORE_LAB[c]}</a></li>' for c in CORE)
    cv=''.join(f'<li><a href="{u(SECTOR_HUBS[sc][0])}">{lab}</a></li>' for sc,lab in SEC_LAB)
    return f'''</main><footer class="pie"><div class="wrap cols"><div><a class="logo" href="{u('')}"><img class="logoimg" src="{asset(slug,'img/samsung-logo.png')}" alt="Samsung, servicio técnico Samsung Quito" width="200" height="60"><span class="wm"><small>Servicio técnico</small><b>QUITO</b></span></a><p>Servicio técnico Samsung Quito: reparación y mantenimiento a domicilio de electrodomésticos Samsung en Quito.</p><p><a class="tel" href="tel:{PHONE_TEL}">{PHONE_TXT}</a><br>WhatsApp y llamadas · +593 99 350 8191</p></div>
<div><h2>Electrodomésticos</h2><ul>{eq}</ul></div>
<div><h2>Servicios</h2><ul>{sv}<li><a href="{u('servicios')}">Todos los servicios</a></li></ul><h2 class="h2b">Cobertura</h2><ul>{cv}<li><a href="{u('zonas-de-servicio-quito')}">Todos los barrios</a></li></ul></div>
<div><h2>Información</h2><ul><li><a href="{u('fallas-comunes')}">Fallas comunes</a></li><li><a href="{u('guias')}">Guías</a></li><li><a href="{u('como-trabajamos')}">Cómo trabajamos</a></li><li><a href="{u('preguntas-frecuentes')}">Preguntas frecuentes</a></li><li><a href="{u('contacto')}">Contacto</a></li><li><a href="{u('aviso-legal')}">Aviso legal</a></li><li><a href="{u('privacidad')}">Tratamiento de datos</a></li></ul></div></div>
<div class="wrap base">© {datetime.date.today().year} Servicio Técnico Samsung Quito · Quito, Ecuador</div></footer>
<a class="flota" href="{wa(WAHI)}" target="_blank" rel="noopener" aria-label="Escribir por WhatsApp">{WA_SVG}</a></body></html>'''
def write(slug,content):
    d=OUT if slug=='' else os.path.join(OUT,slug); os.makedirs(d,exist_ok=True)
    open(os.path.join(d,'index.html'),'w',encoding='utf-8').write(content)
BIZ={'@context':'https://schema.org','@type':'LocalBusiness','@id':SITE+'/#negocio','name':NAME,'url':SITE+'/','telephone':PHONE_FULL,'image':SITE+'/og.png','logo':SITE+'/img/samsung-marca.png','priceRange':'$$','description':'Servicio técnico Samsung Quito: reparación a domicilio de electrodomésticos Samsung en Quito, Ecuador: refrigeradoras, neveras, lavadoras y secadoras.','address':{'@type':'PostalAddress','addressLocality':'Quito','addressRegion':'Pichincha','addressCountry':'EC'},'geo':{'@type':'GeoCoordinates','latitude':-0.1807,'longitude':-78.4678},'areaServed':{'@type':'City','name':'Quito','containedInPlace':{'@type':'AdministrativeArea','name':'Pichincha'}},'knowsAbout':['Reparación de refrigeradoras Samsung','Reparación de lavadoras Samsung','Reparación de secadoras Samsung','Reparación de cocinas y hornos Samsung','Mantenimiento de electrodomésticos']}
def bc_html(slug,items): return '<nav class="migas" aria-label="Ruta">'+' › '.join((f'<a href="{url(slug,s)}">{E(n)}</a>' if s!=slug else f'<span>{E(n)}</span>') for n,s in items)+'</nav>'
def bc_ld(items): return {'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':i+1,'name':n,'item':SITE+('/' if s=='' else '/'+s+'/')} for i,(n,s) in enumerate(items)]}
def faq_html(faq): return '' if not faq else '<section class="faq"><h2>Preguntas frecuentes</h2>'+''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q,a in faq)+'</section>'
def faq_ld(faq): return {'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in faq]}
def thumb(frm,k,cls=''):
    th=EQ[k].get('th')
    if th: return f'<span class="ico th {cls}"><img src="{asset(frm,"img/"+th+"-s.webp")}" alt="{E(EQ[k]["sing"].capitalize())} Samsung" width="240" height="240" loading="eager" decoding="async"></span>'
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
    return f'<aside class="caja"><h2>Servicio técnico Samsung Quito</h2><p>Escríbenos la marca, el modelo y qué falla presenta. Te orientamos por WhatsApp.</p><a class="btn wa grande" href="{wa(p["wamsg"])}" target="_blank" rel="noopener">{WA_SVG}<span>Escribir por WhatsApp</span></a><a class="btn linea" href="tel:{PHONE_TEL}">Llamar {PHONE_TXT}</a></aside>'
PH={'nevera-family-hub':'Refrigeradora Samsung Side by Side con pantalla Family Hub','nevera-superior-inox':'Refrigeradora Samsung de congelador superior con dispensador','lavadora-superior':'Lavadora Samsung de carga superior','torre-lavado':'Torre de lavado y secado Samsung','secadora':'Secadora Samsung','secadora-torre':'Centro de lavado Samsung (lavadora y secadora)','rep-bomba':'Bomba de desagüe para lavadora (imagen de referencia)','rep-bomba-2':'Bomba de desagüe (imagen de referencia)','rep-filtro-pelusa':'Filtro de pelusas para lavadora (imagen de referencia)','rep-filtro-pelusa-2':'Filtro de pelusas (imagen de referencia)','rep-filtro-agua':'Filtro de agua para refrigeradora Samsung','rep-filtro-agua-2':'Filtro de agua para refrigeradora (imagen de referencia)','rep-filtro-secadora':'Filtro de pelusas para secadora (imagen de referencia)'}
REPF={'refrigeradoras':['rep-filtro-agua','rep-filtro-agua-2'],'lavadoras':['rep-bomba','rep-bomba-2','rep-filtro-pelusa'],'secadoras':['rep-filtro-secadora','rep-filtro-pelusa-2'],'centros-de-lavado':['rep-bomba-2','rep-filtro-pelusa']}
TECP={'tecnico-neveras':('Técnico de Samsung revisando el compresor de una refrigeradora en la cocina de una clienta (imagen ilustrativa)',900,503),'tecnico-lavadora':('Técnico revisando una lavadora en casa de una clienta (imagen ilustrativa)',900,298)}
def fig(slug,n,eager=False):
    return f'<figure><img src="{asset(slug,"img/"+n+".webp")}" srcset="{asset(slug,"img/"+n+"-m.webp")} 460w, {asset(slug,"img/"+n+".webp")} 900w" sizes="(max-width:700px) 44vw, 330px" width="900" height="900" alt="{E(PH[n])}" loading="eager" decoding="async"><figcaption>{E(PH[n])}</figcaption></figure>'
def cimg(frm,n,alt,cls=''):
    return f'<img class="{cls}" src="{asset(frm,"img/"+n+".webp")}" alt="{E(alt)}" width="640" height="426" loading="eager" decoding="async">'
PIMG=[('c-clienta','Clienta explicando la falla de su electrodoméstico'),('c-caja','Caja de herramientas del técnico'),('c-lavadora','Técnico revisando una lavadora'),('c-revision','Técnico revisando una refrigeradora'),('c-revision','Técnico diagnosticando la falla'),('c-compresor','Técnico reparando el compresor'),('c-caja','Herramientas del técnico')]
SIMG={'reparacion-de-electrodomesticos-samsung-a-domicilio-quito':('c-revision','Técnico revisando una refrigeradora'),'mantenimiento-preventivo-de-electrodomesticos-samsung-quito':('c-caja','Herramientas del técnico'),'instalacion-de-electrodomesticos-samsung-quito':('c-lavadora','Técnico revisando una lavadora'),'diagnostico-de-electrodomesticos-samsung-quito':('c-compresor','Técnico revisando el compresor'),'reparacion-de-tarjetas-electronicas-de-electrodomesticos-samsung-quito':('c-lavadora','Técnico probando una lavadora'),'repuestos-para-electrodomesticos-samsung-quito':('rep-bomba','Repuestos para lavadoras y refrigeradoras')}
def tec_fig(slug,n):
    alt,w,h=TECP[n]
    return f'<figure class="tec"><img src="{asset(slug,"img/"+n+".webp")}" srcset="{asset(slug,"img/"+n+"-m.webp")} 560w, {asset(slug,"img/"+n+".webp")} 900w" sizes="(max-width:700px) 92vw, 700px" width="{w}" height="{h}" alt="{E(alt)}" loading="eager" decoding="async"><figcaption>{E(alt.replace(" (imagen ilustrativa)",""))} · imagen ilustrativa</figcaption></figure>'
TECS=['tecnico-neveras','tecnico-lavadora']
CLEAN=['tecnico-neveras','tecnico-lavadora']
def tec_for(slug,p):
    k=p['kind']
    if not AUTH:
        if k=='service': return CLEAN[0] if p['eq'] in ('refrigeradoras','secadoras') else CLEAN[1]
        if k=='zona': return CLEAN[ZSLUGS.index(p['zone'])%2]
        if k=='sector': return CLEAN[list(SECTOR_HUBS).index(p['sector'])%2]
        if k=='term': return CLEAN[sum(map(ord,slug))%2]
        return None
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
    ph=ph[:3]
    g=('<div class="gal">'+''.join(fig(slug,n,i==0) for i,n in enumerate(ph))+'</div><p class="refimg">Imágenes de referencia de equipos Samsung.</p>') if ph else ''
    return t+g
def crumbs(slug,p):
    it=[('Inicio','')]; k=p['kind']
    if k=='service': it.append(('Electrodomésticos','electrodomesticos'))
    elif k=='falla': it.append(('Fallas comunes','fallas-comunes')); it.append((EQ[p['eq']]['h1'].replace(' en Quito',''),EQ[p['eq']]['slug']))
    elif k=='zona': it.append(('Cobertura','zonas-de-servicio-quito'))
    elif k=='sector': it.append(('Cobertura','zonas-de-servicio-quito'))
    elif k=='zxa': it.append(('Cobertura','zonas-de-servicio-quito')); it.append((ZD[p['zone']]['nombre'],'servicio-tecnico-samsung-en-'+p['zone']))
    elif k=='term': it.append(('Servicios','servicios'))
    elif k=='guia': it.append(('Guías','guias'))
    it.append((p['h1'],slug)); return it
def page(slug):
    p=PAGES[slug]; items=crumbs(slug,p); ld=[BIZ,bc_ld(items)]
    if p['kind'] in ('service','zona','zxa','term','sector'):
        ld.append({'@context':'https://schema.org','@type':'Service','name':p['h1'],'serviceType':p['h1'],'provider':{'@id':SITE+'/#negocio'},'areaServed':{'@type':'City','name':'Quito'},'url':SITE+'/'+slug+'/','description':p['desc']})
    if p['kind'] in ('guia','falla'):
        ld.append({'@context':'https://schema.org','@type':'Article','headline':p['h1'],'description':p['desc'],'inLanguage':'es-EC','datePublished':TODAY,'dateModified':TODAY,'author':{'@type':'Organization','name':NAME},'publisher':{'@id':SITE+'/#negocio'},'mainEntityOfPage':SITE+'/'+slug+'/'})
    if p['faq']: ld.append(faq_ld(p['faq']))
    secs=''.join(f'<section><h2>{E(h)}</h2>{fix(b,slug)}</section>' for h,b in p['sections'])
    hero=f'<section class="phero"><div class="wrap">{bc_html(slug,items)}<p class="kick">Servicio técnico Samsung Quito</p><div class="ph-fila">{pth(slug,p,"big")}<div><h1>{E(p["h1"])}</h1><p class="lead">{E(p["lead"])}</p></div></div><div class="acc"><a class="btn wa grande" href="{wa(p["wamsg"])}" target="_blank" rel="noopener">{WA_SVG}<span>Cotizar por WhatsApp</span></a><a class="btn linea cl" href="tel:{PHONE_TEL}">Llamar {PHONE_TXT}</a></div></div></section>'
    body=f'<div class="wrap lay"><article class="art">{galeria(slug,p)}{secs}{faq_html(p["faq"])}</article>{cta_box(slug,p)}</div>{related_html(slug,p)}'
    write(slug,head(slug,p['title'],p['desc'],ld,'article' if p['kind'] in ('guia','falla') else 'website')+header(slug)+hero+body+footer(slug))
INFO={'electrodomesticos','fallas-comunes','servicios','zonas-de-servicio-quito','guias','como-trabajamos','preguntas-frecuentes','contacto','aviso-legal','privacidad'}
def info_page(slug,h1,title,desc,lead,body_html,faq=None,icon='home',wamsg=WAHI,wide=False):
    items=[('Inicio',''),(h1,slug)]; ld=[BIZ,bc_ld(items)]+([faq_ld(faq)] if faq else [])
    hero=f'<section class="phero"><div class="wrap">{bc_html(slug,items)}<p class="kick">Servicio técnico Samsung Quito</p><div class="ph-fila"><div><h1>{E(h1)}</h1><p class="lead">{E(lead)}</p></div></div></div></section>'
    body=f'<div class="wrap lay1"><article class="art wide">{fix(body_html,slug)}{faq_html(faq)}</article></div>'
    write(slug,head(slug,title,desc,ld)+header(slug)+hero+body+footer(slug))
def cardlist(slug,slugs,cls='cards g2'):
    return f'<div class="{cls}">'+''.join(f'<a class="card has-th" href="{url(slug,s)}">{pth(slug,PAGES[s],"sm")}<div><b>{E(PAGES[s]["h1"])}</b><span>{E(PAGES[s]["lead"][:105])}…</span></div></a>' for s in slugs)+'</div>'
def chips(slug,slugs,label=None):
    return '<div class="chips">'+''.join(f'<a href="{url(slug,s)}">{E(label(s) if label else PAGES[s]["h1"])}</a>' for s in slugs)+'</div>'
# ---------------- páginas ----------------
for s in ORDER: page(s)
HOMEFAQ=[('¿Hacen servicio técnico Samsung a domicilio en Quito?','Sí. Vamos a tu casa, apartamento u oficina en Quito: norte, centro, sur y valles. Escríbenos por WhatsApp con el equipo, el modelo y la falla.'),
('¿Qué electrodomésticos Samsung reparan?','Refrigeradoras, neveras, lavadoras y secadoras.'),
('¿Qué hago si mi equipo está en garantía?','Revisa primero las condiciones de la garantía de fábrica. Si ya venció o necesitas un diagnóstico, escríbenos por WhatsApp.'),
('¿Cuánto cuesta la visita?','Escríbenos al WhatsApp con el equipo, el modelo y la falla; te confirmamos el costo de la visita antes de ir.'),
('¿Dan el costo antes de reparar?','Sí. Primero diagnosticamos, te explicamos la falla y te informamos el costo antes de continuar.'),
('¿Cómo pido el servicio?','Por WhatsApp o llamada al 099 350 8191 (+593 99 350 8191). Envía marca, modelo, falla, tu barrio y, si puedes, una foto de la etiqueta y un video corto.')]
# --- hubs
def tree_eq(sl):
    h=''
    for k in EQK:
        e=EQ[k]; nm=e["art"].split(" ",1)[1]
        fl='<ul class="sublist">'+''.join(f'<li><a href="@{s}@">{E(PAGES[s]["h1"])}</a></li>' for s in e['slugs'])+'</ul>'
        sv='<ul class="sublist">'+''.join(f'<li><a href="@{s}@">{E(TERMS[s]["h1"])}</a></li>' for s in TPRIM[k])+'</ul>' if TPRIM[k] else ''
        h+=f'<section class="eqhub"><h2><a href="@{e["slug"]}@">{E(e["h1"])}</a></h2><div class="tri"><div><h3>Fallas comunes</h3>{fl}</div>'+(f'<div><h3>Servicios</h3>{sv}</div>' if sv else '')+f'<div><h3>Más</h3><ul class="sublist"><li><a href="@{e["slug"]}@">Todo sobre {nm} Samsung</a></li><li><a href="@zonas-de-servicio-quito@">Dónde atendemos</a></li></ul></div></div></section>'
    return h
info_page('electrodomesticos','Electrodomésticos Samsung que reparamos en Quito','Electrodomésticos Samsung que reparamos en Quito | Samsung Quito','Reparamos refrigeradoras, neveras, lavadoras y secadoras Samsung en Quito. Fallas y servicios por equipo.','Elige tu electrodoméstico y entra a sus fallas, servicios y zonas, todo en orden.',tree_eq('electrodomesticos')+'<section><h2>¿No ves tu equipo?</h2><p>Escríbenos por WhatsApp con la marca y el modelo y te confirmamos si podemos atenderlo.</p></section>',icon='wrench')
fh=''
for k in EQK:
    e=EQ[k]; fh+=f'<section><h2><a href="@{e["slug"]}@">{E(e["corto"])}</a></h2><ul class="fallas">'+''.join(f'<li><a href="@{s}@">{E(PAGES[s]["h1"])}</a> <span class="tag {mp.URG[e["fallas"][i][2]]}">{e["fallas"][i][2]}</span></li>' for i,s in enumerate(e['slugs']))+'</ul></section>'
info_page('fallas-comunes','Fallas comunes de electrodomésticos Samsung en Quito','Fallas comunes de electrodomésticos Samsung en Quito','Todas las fallas comunes de refrigeradoras, lavadoras, secadoras y más equipos Samsung: causas, qué revisar y cuándo llamar a un técnico en Quito.','Encuentra tu falla por electrodoméstico, mira qué puedes revisar tú con seguridad y cuándo pedir un técnico.',fh,icon='help')
def cards_text(sl,slugs):
    return '<div class="svcs">'+''.join(f'<a class="svc" href="{url(sl,s)}"><b>{E(CORE_LAB.get(s,PAGES[s]["h1"]))}</b><span>{E(PAGES[s]["lead"][:110])}…</span><i>Ver servicio →</i></a>' for s in slugs)+'</div>'
OTRAS=[s for s in GEN if s not in CORE and s in TERMS]
sv='<section><h2>Nuestros servicios</h2>'+'@@CARDS@@'+'</section>'
for k in EQK:
    if TPRIM[k]:
        nm=EQ[k]["art"].split(" ",1)[1]
        sv+=f'<section><h2>Servicios para {nm} Samsung</h2><ul class="sublist">'+''.join(f'<li><a href="@{s}@">{E(TERMS[s]["h1"])}</a></li>' for s in TPRIM[k])+'</ul></section>'
sv+='<section><h2>Más búsquedas frecuentes</h2><ul class="sublist">'+''.join(f'<li><a href="@{s}@">{E(TERMS[s]["h1"])}</a></li>' for s in OTRAS)+'</ul></section><section><h2>Cobertura</h2><ul class="sublist">'+''.join(f'<li><a href="@{SECTOR_HUBS[sc][0]}@">{E(PAGES[SECTOR_HUBS[sc][0]]["h1"])}</a></li>' for sc,_ in SEC_LAB)+''.join(f'<li><a href="@{s}@">{E(TERMS[s]["h1"])}</a></li>' for s in VALLE_TERMS)+'</ul></section>'
sv=sv.replace('@@CARDS@@',cards_text('servicios',CORE))
info_page('servicios','Servicios de reparación y mantenimiento Samsung en Quito','Servicios de reparación y mantenimiento Samsung en Quito','Servicio técnico a domicilio, mantenimiento, instalación, diagnóstico y reparación de electrodomésticos Samsung en Quito, organizados por servicio, equipo y zona.','Todo lo que hacemos por tus electrodomésticos Samsung en Quito, ordenado por servicio, por equipo y por zona.',sv,icon='wrench')
gh=''
for k in EQK:
    gl=list(GEQ.get(k,[]))+(GEQ.get('neveras',[]) if k=='refrigeradoras' else [])
    if gl: gh+=f'<section><h2>{E(EQ[k]["corto"])}</h2><ul class="sublist">'+''.join(f'<li><a href="@{s}@">{E(PAGES[s]["h1"])}</a></li>' for s in gl)+'</ul></section>'
info_page('guias','Guías de electrodomésticos Samsung para Quito','Guías de electrodomésticos Samsung para Quito | Samsung Quito','Guías prácticas sobre refrigeradoras, neveras, lavadoras y secadoras Samsung: gas, voltaje, mantenimiento y cuándo reparar, pensadas para Quito.','Explicaciones claras para cuidar tus electrodomésticos y entender qué les pasa, ordenadas por equipo.',gh,icon='doc')
zh=''
for sc,lab in SEC_LAB:
    zs=[z for z in ZSLUGS if ZD[z]['sector']==sc]
    zh+=f'<section><h2><a href="@{SECTOR_HUBS[sc][0]}@">{lab}</a></h2><ul class="cols3">'+''.join(f'<li><a href="@servicio-tecnico-samsung-en-{z}@">{E(ZD[z]["nombre"])}</a></li>' for z in zs)+'</ul></section>'
zh+='<section><h2>¿Tu barrio no aparece?</h2><p>Escríbenos tu dirección por WhatsApp. Muchas veces podemos atender sectores cercanos.</p></section>'
info_page('zonas-de-servicio-quito','Cobertura: barrios de Quito donde atendemos','Cobertura servicio técnico Samsung en Quito: barrios y valles','Servicio técnico Samsung a domicilio en el norte, centro, sur y valles de Quito: La Carolina, Cumbayá, Villaflora, Calderón, Sangolquí y más de 60 barrios.','Elige tu sector y tu barrio para ver cómo coordinamos la visita en tu zona.',zh,icon='pin')
def pli(frm,i,a,b):
    n,alt=PIMG[i]
    return f'<li>{cimg(frm,n,alt,"pimg")}<div class="pt"><b>{i+1}</b><div><h3>{E(a)}</h3><p>{E(b)}</p></div></div></li>'
pasos=[('Escríbenos','Por WhatsApp o llamada al 099 350 8191. Cuéntanos qué equipo es, la marca, el modelo y la falla.'),('Envía datos y fotos','Una foto de la etiqueta del equipo y un video corto de la falla ayudan a orientarte mejor.'),('Coordinamos la visita','Acordamos día y hora en tu casa, apartamento u oficina de Quito.'),('Diagnóstico en tu casa','Probamos el equipo, identificamos la causa y te explicamos qué tiene.'),('Costo antes de reparar','Te informamos el costo y tú decides si continuamos.'),('Reparación y prueba','Reparamos y probamos que el equipo quede funcionando.'),('Recomendaciones','Te decimos cómo usarlo y cuidarlo para que la falla no se repita.')]
ch=f'<section><h2>Paso a paso</h2><ol class="pasos l">'+''.join(f'{pli("como-trabajamos",i,a,b)}' for i,(a,b) in enumerate(pasos))+'</ol></section><section><h2>Nuestro compromiso con la claridad</h2><p>No cambiamos piezas al azar: primero probamos y diagnosticamos. Si no conviene reparar, te lo decimos.</p></section>'
info_page('como-trabajamos','Cómo trabajamos: servicio técnico Samsung paso a paso','Cómo trabajamos el servicio técnico Samsung en Quito','Así es el servicio técnico Samsung a domicilio en Quito: contacto por WhatsApp, diagnóstico, costo antes de reparar, reparación y recomendaciones.','Del primer mensaje a la reparación: así trabajamos, sin sorpresas.',ch,icon='shield')
FAQ_ALL=HOMEFAQ+[('¿Reparan solo Samsung?','Nos enfocamos en electrodomésticos Samsung. Si tienes otra marca, escríbenos y te decimos si podemos ayudarte.'),('¿Qué hago si huele a gas?','Cierra la llave, ventila, no uses llama ni interruptores y llama a un técnico. Si hay riesgo, llama a emergencias (911).'),('¿Atienden apartamentos y conjuntos?','Sí. Coordinamos acceso y horario con la administración.'),('¿Qué datos debo enviar por WhatsApp?','Tipo de equipo, marca y modelo, la falla, tu barrio y una foto de la etiqueta si puedes.'),('¿Instalan electrodomésticos?','Consulta por WhatsApp con el modelo y el tipo de conexión (agua, gas o electricidad) para confirmarte el servicio.'),('¿Qué zonas de Quito atienden?','Norte, centro, sur y valles: La Carolina, Iñaquito, Cotocollao, Villaflora, Quitumbe, Cumbayá, Tumbaco, Calderón, Sangolquí y más. Consulta la lista completa en Zonas.')]
info_page('preguntas-frecuentes','Preguntas frecuentes sobre el servicio técnico Samsung en Quito','Preguntas frecuentes: servicio técnico Samsung en Quito','Respuestas sobre el servicio técnico Samsung a domicilio en Quito: equipos, zonas, costo de la visita, garantía de fábrica y cómo pedir el servicio.','Lo que más nos preguntan antes de pedir una visita.','',faq=FAQ_ALL,icon='help')
info_page('contacto','Contacto: servicio técnico Samsung en Quito','Contacto servicio técnico Samsung Quito | WhatsApp 099 350 8191','Contacta al servicio técnico Samsung en Quito por WhatsApp o llamada al 099 350 8191 (+593 99 350 8191). Cuéntanos tu equipo y la falla.','Escríbenos por WhatsApp o llámanos. Te respondemos con el siguiente paso.',
 f'<section><h2>Pide tu visita</h2><p><a class="btn wa grande" href="{wa(WAHI)}" target="_blank" rel="noopener">{WA_SVG}<span>Escribir por WhatsApp</span></a> <a class="btn linea" href="tel:{PHONE_TEL}">Llamar {PHONE_TXT}</a></p><p>Número: <b>{PHONE_TXT}</b> ({PHONE_FULL}).</p></section><section><h2>Qué contarnos</h2><ul><li>Qué equipo es y su marca y modelo</li><li>Qué falla presenta y desde cuándo</li><li>Tu barrio o sector de Quito</li><li>Si puedes, una foto de la etiqueta y un video corto del problema</li></ul></section><section><h2>Dónde atendemos</h2><p>Quito: norte, centro, sur y valles. Mira la lista en <a href="@zonas-de-servicio-quito@">Zonas</a>.</p></section>',icon='chat')
info_page('aviso-legal','Aviso legal','Aviso legal | Servicio Técnico Samsung Quito','Aviso legal de Servicio Técnico Samsung Quito: uso de marcas y alcance de la información del sitio.','Uso de marcas y alcance de la información de este sitio.',
 '<section><h2>Marcas</h2><p>Samsung es una marca de su respectivo titular. Este sitio no es operado por Samsung.</p></section><section><h2>Información orientativa</h2><p>El contenido de este sitio es orientativo. El diagnóstico definitivo y el costo se confirman en la visita. Las imágenes marcadas como ilustrativas o de referencia no corresponden necesariamente a equipos o personas concretas.</p></section><section><h2>Garantía de fábrica</h2><p>Si tu equipo está en garantía de fábrica, consulta las condiciones con el fabricante antes de solicitar una reparación independiente.</p></section>',icon='shield')
info_page('privacidad','Tratamiento de datos personales','Tratamiento de datos personales | Servicio Técnico Samsung Quito','Cómo trata Servicio Técnico Samsung Quito tus datos personales cuando nos escribes por WhatsApp o nos llamas para pedir una visita en Quito.','Qué datos recibimos y para qué los usamos.',
 f'<section><h2>Qué datos recibimos</h2><p>Cuando nos escribes por WhatsApp o nos llamas recibimos los datos que compartes: nombre, teléfono, barrio o dirección y datos del equipo.</p></section><section><h2>Para qué los usamos</h2><p>Solo para atender tu solicitud, coordinar la visita y dar seguimiento al servicio. No vendemos tus datos.</p></section><section><h2>Tus derechos</h2><p>Puedes pedirnos que corrijamos o eliminemos tus datos escribiendo al {PHONE_TXT}.</p></section>',icon='doc')
# --- portada
HERO_ALT='Técnico de Samsung revisando el compresor de una refrigeradora en casa de una clienta (imagen ilustrativa)'
def home():
    s=''
    sv=''.join(f'<a class="svc" href="{url(s,c)}">{cimg(s,SIMG[c][0],SIMG[c][1],"simg")}<b>{CORE_LAB[c]}</b><span>{E(PAGES[c]["lead"][:105])}…</span><i>Ver servicio →</i></a>' for c in CORE)
    def eqcard(k):
        e=EQ[k]; nm=e["art"].split(" ",1)[1]
        fl=''.join(f'<li><a href="{url(s,x)}">{E(PAGES[x]["h1"])}</a></li>' for x in e['slugs'][:3])
        return f'<div class="eqc">{thumb(s,k,"big")}<h3><a href="{url(s,e["slug"])}">{E(e["h1"])}</a></h3><p>{E(e["intro"][:105])}…</p><b class="sb">Fallas más consultadas</b><ul>{fl}</ul><a class="enlace" href="{url(s,e["slug"])}">Todo sobre {nm} Samsung →</a></div>'
    eqs=''.join(eqcard(k) for k in EQK)
    cs=''.join(f'<li><a href="{url(s,x)}">{E(TERMS[x]["h1"])}</a></li>' for x in ['centro-de-servicio-de-lavadoras-samsung-quito','centro-de-servicio-de-secadoras-samsung-quito','centro-de-servicio-de-refrigeradoras-samsung-quito','centro-de-servicio-de-neveras-samsung-quito','soporte-tecnico-samsung-quito','nevera-o-refrigeradora-samsung-es-lo-mismo'] if x in TERMS)
    cov=''
    for sc,lab in SEC_LAB:
        zs=[z for z in ZSLUGS if ZD[z]['sector']==sc]
        cov+=f'<div class="covc"><h3><a href="{url(s,SECTOR_HUBS[sc][0])}">{lab}</a></h3><ul>'+''.join(f'<li><a href="{url(s,"servicio-tecnico-samsung-en-"+z)}">{E(ZD[z]["nombre"])}</a></li>' for z in zs)+'</ul></div>'
    gcards=cardlist(s,GUIDE_SLUGS[:6])
    ps=''.join(pli(s,j,pasos[j][0],pasos[j][1]).replace(f'<b>{j+1}</b>',f'<b>{k+1}</b>') for k,j in enumerate([0,3,4,5]))
    tecs=''.join(f'<div>{tec_fig(s,n)}</div>' for n in CLEAN)
    if AUTH: ASI=f'<div class="tecs">{tecs}</div>'
    else: ASI='<div class="tecs dos">'+''.join(f'<div>{tec_fig(s,n)}</div>' for n in CLEAN)+'</div>'
    nz=len(ZSLUGS)
    hero=f'''<section class="hero"><div class="wrap hgrid"><div class="htxt"><p class="kick">Reparación de electrodomésticos a domicilio</p><h1>Servicio técnico Samsung Quito</h1><p class="lead">Reparación de electrodomésticos Samsung en Quito: neveras, refrigeradoras, lavadoras y secadoras, en tu casa. Servicio técnico y centro de servicio Samsung a domicilio, con costo antes de reparar.</p><div class="acc"><a class="btn wa grande" href="{wa(WAHI)}" target="_blank" rel="noopener">{WA_SVG}<span>Escribir por WhatsApp</span></a><a class="btn linea grande" href="tel:{PHONE_TEL}">Llamar {PHONE_TXT}</a></div><ul class="pts"><li>A domicilio en Quito</li><li>Norte, centro, sur y valles</li><li>Te explicamos la falla antes de reparar</li></ul></div><div class="hmedia"><img src="img/{HERO}.webp" srcset="img/{HERO}-m.webp 640w, img/{HERO}.webp 900w" sizes="(max-width:900px) 92vw, 560px" width="900" height="503" alt="{HERO_ALT}" fetchpriority="high" decoding="async"><div class="hbadge"><b>Costo antes de reparar</b><span>Diagnóstico claro, sin sorpresas</span></div></div></div></section>
<div class="trust"><div class="wrap"><div><b>{len(EQK)}</b><span>equipos Samsung: neveras, refrigeradoras, lavadoras y secadoras</span></div><div><b>{nz}</b><span>barrios y sectores de Quito</span></div><div><b>A domicilio</b><span>norte, centro, sur y valles</span></div><div><b>WhatsApp</b><span>respuesta directa al {PHONE_TXT}</span></div></div></div>'''
    body=f'''<section class="sec" id="servicios"><div class="wrap"><h2>Nuestros servicios</h2><p class="sub">Todo lo que hacemos por tus electrodomésticos Samsung en Quito.</p><div class="svcs">{sv}</div><p style="margin-top:22px"><a class="enlace" href="{url(s,'servicios')}">Ver todos los servicios, por equipo y por zona →</a></p></div></section>
<section class="sec osc" id="electrodomesticos"><div class="wrap"><h2>Electrodomésticos que reparamos</h2><p class="sub">Elige tu equipo: cada uno tiene sus fallas, servicios y zonas.</p><div class="eqgrid">{eqs}</div></div></section>
<section class="sec"><div class="wrap"><h2>¿Buscas un centro de servicio Samsung en Quito?</h2><p class="sub">Con nosotros no llevas el equipo: el técnico va a tu casa.</p><ul class="sublist cs">{cs}</ul></div></section>
<section class="sec" id="cobertura"><div class="wrap"><h2>Cobertura: barrios de Quito</h2><p class="sub">Atendemos el norte, el centro, el sur y los valles. Elige tu barrio.</p><figure class="banner"><img src="img/tecnico-lavadora.webp" alt="Técnico de Samsung revisando una lavadora en una casa de Quito" width="900" height="298" loading="eager" decoding="async"><figcaption>Vamos a tu casa en toda Quito</figcaption></figure><div class="covg">{cov}</div><p style="margin-top:22px"><a class="enlace" href="{url(s,'zonas-de-servicio-quito')}">Ver toda la cobertura →</a></p></div></section>
<section class="sec osc"><div class="wrap"><h2>Cómo trabajamos</h2><p class="sub">Vamos hasta donde está tu equipo, lo revisamos y te explicamos antes de reparar.</p>{ASI}<p class="refimg">Imágenes ilustrativas.</p><ol class="pasos">{ps}</ol><p style="margin-top:22px"><a class="enlace" href="{url(s,'como-trabajamos')}">Ver el proceso completo paso a paso →</a></p></div></section>
<section class="sec"><div class="wrap"><h2>Guías</h2><p class="sub">Voltaje, limpieza y fallas explicadas para Quito.</p>{gcards}<p style="margin-top:22px"><a class="enlace" href="{url(s,'guias')}">Ver todas las guías →</a></p></div></section>
<section class="sec osc"><div class="wrap lay1">{faq_html(HOMEFAQ)}</div></section>
<section class="final foto" style="--bg:url(img/tecnico-neveras.webp)"><div class="wrap"><h2>¿Tu electrodoméstico está fallando?</h2><p>Escríbenos por WhatsApp con la marca, el modelo y la falla. Te orientamos y coordinamos la visita.</p><a class="btn wa grande" href="{wa(WAHI)}" target="_blank" rel="noopener">{WA_SVG}<span>Escribir por WhatsApp</span></a> <a class="btn linea cl" href="tel:{PHONE_TEL}">Llamar {PHONE_TXT}</a></div></section>'''
    ld=[BIZ,{'@context':'https://schema.org','@type':'WebSite','url':SITE+'/','name':NAME,'inLanguage':'es-EC'},faq_ld(HOMEFAQ)]
    write('',head('','Servicio Técnico Samsung Quito: Reparación de Electrodomésticos','Servicio técnico Samsung Quito: reparación de electrodomésticos Samsung a domicilio, refrigeradoras, neveras, lavadoras y secadoras. WhatsApp 099 350 8191.',ld)+header('')+hero+body+footer(''))
home()
write('404',head('404','Página no encontrada | Samsung Quito','Esta página no existe.',None,noindex=True)+header('404')+'<section class="phero"><div class="wrap"><h1>Página no encontrada</h1><p class="lead">Puede que el enlace haya cambiado. Vuelve al inicio o escríbenos por WhatsApp.</p></div></section>'+footer('404'))
# ---------------- archivos técnicos ----------------
allp=['']+sorted(INFO)+ORDER
sm='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{SITE}/{s+"/" if s else ""}</loc><lastmod>{TODAY}</lastmod></url>' for s in allp)+'</urlset>'
open(os.path.join(OUT,'sitemap.xml'),'w',encoding='utf-8').write(sm)
open(os.path.join(OUT,'robots.txt'),'w').write(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
open(os.path.join(OUT,'llms.txt'),'w',encoding='utf-8').write(f'# {NAME}\n> Servicio técnico Samsung Quito: reparación a domicilio de electrodomésticos Samsung en Quito, Ecuador. WhatsApp {PHONE_FULL}.\n\n## Secciones\n- {SITE}/electrodomesticos/ : equipos que reparamos\n- {SITE}/fallas-comunes/ : fallas y qué revisar\n- {SITE}/zonas-de-servicio-quito/ : zonas de Quito\n- {SITE}/guias/ : guías\n- {SITE}/como-trabajamos/ : proceso\n')
open(os.path.join(OUT,'.htaccess'),'w').write('ErrorDocument 404 /404/\nRewriteEngine On\nRewriteCond %{HTTPS} off\nRewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]\nRewriteCond %{HTTP_HOST} ^www\\.(.+)$ [NC]\nRewriteRule ^ https://%1%{REQUEST_URI} [L,R=301]\n<IfModule mod_deflate.c>\nAddOutputFilterByType DEFLATE text/html text/css application/javascript image/svg+xml application/xml\n</IfModule>\n<IfModule mod_expires.c>\nExpiresActive On\nExpiresByType text/css "access plus 30 days"\nExpiresByType image/webp "access plus 180 days"\nExpiresByType image/png "access plus 30 days"\nExpiresByType image/svg+xml "access plus 30 days"\n</IfModule>\n')
shutil.copy('estilo.css',os.path.join(OUT,'estilo.css'))
shutil.copytree('img',os.path.join(OUT,'img'))
if os.path.isdir('assets'):
    for f in os.listdir('assets'): shutil.copy(os.path.join('assets',f),os.path.join(OUT,f))
print('páginas html:',sum(1 for r,_,fs in os.walk(OUT) for f in fs if f=='index.html'))
