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
HERO='portada' if AUTH else 'portada-saludo'
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
<meta property="og:image:alt" content="Servicio técnico Mabe Quito: reparación de electrodomésticos a domicilio"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(desc)}"><meta name="twitter:image" content="{SITE}/og.png">
<link rel="icon" href="{asset(slug,'favicon.png')}" type="image/png"><link rel="apple-touch-icon" href="{asset(slug,'apple-touch-icon.png')}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="{asset(slug,'estilo.css')}">{PRE if slug=='' else ''}{lds}</head><body>'''
CORE=['reparacion-de-electrodomesticos-mabe-a-domicilio-quito','mantenimiento-preventivo-de-electrodomesticos-mabe-quito','instalacion-de-electrodomesticos-mabe-quito','diagnostico-de-electrodomesticos-mabe-quito','reparacion-de-tarjetas-electronicas-de-electrodomesticos-mabe-quito','repuestos-para-electrodomesticos-mabe-quito']
CORE_LAB={CORE[0]:'Reparación a domicilio',CORE[1]:'Mantenimiento preventivo',CORE[2]:'Instalación',CORE[3]:'Diagnóstico',CORE[4]:'Tarjetas electrónicas',CORE[5]:'Repuestos'}
WAHI='Hola, necesito servicio técnico para un electrodoméstico Mabe en Quito.'
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
    LOGO=f'<a class="logo" href="{u("")}" aria-label="{NAME}, inicio"><img class="logoimg" src="{asset(slug,"img/mabe-logo.png")}" alt="Mabe, servicio técnico Mabe Quito" width="200" height="60"><span class="wm"><small>Servicio técnico</small><b>QUITO</b></span></a>'
    return f'''<a class="saltar" href="#contenido">Saltar al contenido</a>
<div class="topbar"><div class="wrap"><span>Servicio técnico Mabe Quito · reparación a domicilio</span><a href="{wa(WAHI)}" target="_blank" rel="noopener">WhatsApp {PHONE_TXT}</a></div></div>
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
    return f'''</main><footer class="pie"><div class="wrap cols"><div><a class="logo" href="{u('')}"><img class="logoimg" src="{asset(slug,'img/mabe-logo.png')}" alt="Mabe, servicio técnico Mabe Quito" width="200" height="60"><span class="wm"><small>Servicio técnico</small><b>QUITO</b></span></a><p>Servicio técnico Mabe Quito: reparación y mantenimiento a domicilio de electrodomésticos Mabe en Quito.</p><p><a class="tel" href="tel:{PHONE_TEL}">{PHONE_TXT}</a><br>WhatsApp y llamadas · +593 99 350 8191</p></div>
<div><h2>Electrodomésticos</h2><ul>{eq}</ul></div>
<div><h2>Servicios</h2><ul>{sv}<li><a href="{u('servicios')}">Todos los servicios</a></li></ul><h2 class="h2b">Cobertura</h2><ul>{cv}<li><a href="{u('zonas-de-servicio-quito')}">Todos los barrios</a></li></ul></div>
<div><h2>Información</h2><ul><li><a href="{u('fallas-comunes')}">Fallas comunes</a></li><li><a href="{u('guias')}">Guías</a></li><li><a href="{u('como-trabajamos')}">Cómo trabajamos</a></li><li><a href="{u('preguntas-frecuentes')}">Preguntas frecuentes</a></li><li><a href="{u('mapa-del-sitio')}">Mapa del sitio</a></li><li><a href="{u('contacto')}">Contacto</a></li><li><a href="{u('aviso-legal')}">Aviso legal</a></li><li><a href="{u('privacidad')}">Tratamiento de datos</a></li></ul></div></div>
<div class="wrap base">© {datetime.date.today().year} Servicio Técnico Mabe Quito · Quito, Ecuador</div></footer>
<a class="flota" href="{wa(WAHI)}" target="_blank" rel="noopener" aria-label="Escribir por WhatsApp">{WA_SVG}</a></body></html>'''
def write(slug,content):
    d=OUT if slug=='' else os.path.join(OUT,slug); os.makedirs(d,exist_ok=True)
    open(os.path.join(d,'index.html'),'w',encoding='utf-8').write(content)
BIZ={'@context':'https://schema.org','@type':'LocalBusiness','@id':SITE+'/#negocio','name':NAME,'url':SITE+'/','telephone':PHONE_FULL,'image':SITE+'/og.png','logo':SITE+'/img/mabe-marca.png','priceRange':'$$','description':'Servicio técnico Mabe Quito: reparación a domicilio de electrodomésticos Mabe en Quito, Ecuador: refrigeradoras, lavadoras, secadoras, cocinas y hornos.','address':{'@type':'PostalAddress','addressLocality':'Quito','addressRegion':'Pichincha','addressCountry':'EC'},'geo':{'@type':'GeoCoordinates','latitude':-0.1807,'longitude':-78.4678},'areaServed':{'@type':'City','name':'Quito','containedInPlace':{'@type':'AdministrativeArea','name':'Pichincha'}},'contactPoint':{'@type':'ContactPoint','telephone':PHONE_FULL,'contactType':'customer service','areaServed':'EC','availableLanguage':'es'},'knowsAbout':['Reparación de refrigeradoras Mabe','Reparación de lavadoras Mabe','Reparación de secadoras Mabe','Reparación de cocinas y hornos Mabe','Mantenimiento de electrodomésticos']}
def bc_html(slug,items): return '<nav class="migas" aria-label="Ruta">'+' › '.join((f'<a href="{url(slug,s)}">{E(n)}</a>' if s!=slug else f'<span>{E(n)}</span>') for n,s in items)+'</nav>'
def bc_ld(items): return {'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':i+1,'name':n,'item':SITE+('/' if s=='' else '/'+s+'/')} for i,(n,s) in enumerate(items)]}
def faq_html(faq): return '' if not faq else '<section class="faq"><h2>Preguntas frecuentes</h2>'+''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q,a in faq)+'</section>'
def faq_ld(faq): return {'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in faq]}
def thumb(frm,k,cls=''):
    th=EQ[k].get('th')
    if th: return f'<span class="ico th {cls}"><img src="{asset(frm,"img/"+th+"-s.webp")}" alt="{E(EQ[k]["sing"].capitalize())} Mabe" width="240" height="240" loading="eager" decoding="async"></span>'
    return ''
def pth(frm,p,cls=''):
    if p.get('eq') and p['kind'] in ('service','falla','zxa','term','guia'): return thumb(frm,p['eq'],cls)
    return ''
def ell(s,n):
    if len(s)<=n: return s
    c=s[:n]
    k=max(c.rfind(','),c.rfind(';'),c.rfind(':'),c.rfind('.'))
    c=c[:k] if k>=int(n*0.55) else c.rsplit(' ',1)[0]
    c=c.rstrip(' ,;:.')
    while True:
        w=c.rsplit(' ',1)
        if len(w)==2 and w[1].lower() in ('a','la','el','los','las','del','de','y','o','con','en','un','una','que','por','para','se','al','e','u'): c=w[0].rstrip(' ,;:.')
        else: break
    return c+'…'
def related_html(slug,p):
    if not p.get('related'): return ''
    cs=''
    for s in p['related']:
        q=PAGES[s]; cs+=f'<a class="card has-th" href="{url(slug,s)}">{pth(slug,q,"sm")}<div><b>{E(q["h1"])}</b><span>{E(ell(q["lead"],105))}</span></div></a>'
    return f'<section class="rel"><div class="wrap"><h2>También te puede servir</h2><div class="cards">{cs}</div></div></section>'
def cta_box(slug,p):
    return f'<aside class="caja"><h2>Servicio técnico Mabe Quito</h2><p>Escríbenos la marca, el modelo y qué falla presenta. Te orientamos por WhatsApp.</p><a class="btn wa grande" href="{wa(p["wamsg"])}" target="_blank" rel="noopener">{WA_SVG}<span>Escribir por WhatsApp</span></a><a class="btn linea grande" href="tel:{PHONE_TEL}">Llamar {PHONE_TXT}</a></aside>'
PH={'nevera-superior-negra':'Refrigeradora Mabe de congelador superior','nevera-superior-inox':'Refrigeradora Mabe de congelador superior en acero','nevera-side-by-side':'Refrigeradora Mabe Side by Side con dispensador','nevera-side-by-side-inox':'Refrigeradora Mabe Side by Side en acero','lavadora-superior':'Lavadora Mabe de carga superior','secadora':'Secadora Mabe','secadora-oscura':'Secadora Mabe de color oscuro','torre-lavado':'Centro de lavado Mabe (torre)','cocina-gas':'Cocina a gas Mabe de seis hornillas','horno-empotrable':'Horno empotrable Mabe','parrilla-gas':'Parrilla a gas Mabe de cuatro hornillas','campana-extractora':'Campana extractora Mabe','congelador-horizontal':'Congelador horizontal Mabe'}
TECP={'tecnico-saludo':('Técnico de Mabe saludando al cliente en la puerta de su casa (imagen ilustrativa)',900,503),'tecnico-cocina-gas':('Técnico revisando una cocina a gas en casa de una clienta (imagen ilustrativa)',900,503),'tecnico-cliente':('Técnico explicando una falla a una clienta frente a la refrigeradora (imagen ilustrativa)',900,672),'tecnico-cocina':('Técnico con su caja de herramientas en una cocina con refrigeradora y lavadora (imagen ilustrativa)',900,672),'tecnico-puerta':('Técnico llegando a un domicilio (imagen ilustrativa)',900,672),'tecnico-manos':('Revisión de un electrodoméstico (imagen ilustrativa)',900,507)}
def fig(slug,n,eager=False):
    return f'<figure><img src="{asset(slug,"img/"+n+".webp")}" srcset="{asset(slug,"img/"+n+"-m.webp")} 460w, {asset(slug,"img/"+n+".webp")} 900w" sizes="(max-width:700px) 44vw, 330px" width="900" height="900" alt="{E(PH[n])}" loading="eager" decoding="async"></figure>'
def cimg(frm,n,alt,cls=''):
    return f'<img class="{cls}" src="{asset(frm,"img/"+n+".webp")}" alt="{E(alt)}" width="900" height="600" loading="eager" decoding="async">'
PIMG=[('stp1','Cliente conversando con el técnico en su cocina'),('stp2','Técnico revisando los controles de un electrodoméstico'),('stp3','Técnico llegando a la casa del cliente con su caja de herramientas'),('stp4','Técnico diagnosticando un electrodoméstico en la cocina'),('stp5','Técnico atendiendo a la clienta en su cocina'),('stp6','Técnico reparando un electrodoméstico en casa del cliente'),('stp7','Técnico despidiéndose del cliente en la puerta de su casa')]
SIMG={'reparacion-de-electrodomesticos-mabe-a-domicilio-quito': ('stp4', 'Técnico saludando en la puerta'), 'mantenimiento-preventivo-de-electrodomesticos-mabe-quito': ('stp6', 'Maletín y herramientas'), 'instalacion-de-electrodomesticos-mabe-quito': ('stp1', 'Técnico llegando al domicilio'), 'diagnostico-de-electrodomesticos-mabe-quito': ('stp5', 'Técnico revisando una cocina'), 'reparacion-de-tarjetas-electronicas-de-electrodomesticos-mabe-quito': ('stp2', 'Técnico probando los controles'), 'repuestos-para-electrodomesticos-mabe-quito': ('c-caja', 'Caja de herramientas y repuestos')}
def tec_fig(slug,n):
    alt,w,h=TECP[n]
    return f'<figure class="tec"><img src="{asset(slug,"img/"+n+".webp")}" srcset="{asset(slug,"img/"+n+"-m.webp")} 560w, {asset(slug,"img/"+n+".webp")} 900w" sizes="(max-width:700px) 92vw, 700px" width="{w}" height="{h}" alt="{E(alt)}" loading="eager" decoding="async"></figure>'
TECS=['tecnico-cliente','tecnico-cocina','tecnico-puerta','tecnico-manos']
CLEAN=['tecnico-saludo','tecnico-cocina-gas']
def tec_for(slug,p):
    k=p['kind']
    if not AUTH:
        if k=='service': return 'tecnico-cocina-gas' if p['eq'] in ('cocinas','hornos','parrillas','campanas-extractoras') else 'tecnico-saludo'
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
    g=('<div class="gal">'+''.join(fig(slug,n,i==0) for i,n in enumerate(ph))+'</div>') if ph else ''
    return t+g
def crumbs(slug,p):
    it=[('Inicio','')]; k=p['kind']
    if k=='service': it.append(('Electrodomésticos','electrodomesticos'))
    elif k=='falla': it.append(('Fallas comunes','fallas-comunes')); it.append((EQ[p['eq']]['h1'].replace(' en Quito',''),EQ[p['eq']]['slug']))
    elif k=='zona': it.append(('Cobertura','zonas-de-servicio-quito'))
    elif k=='sector': it.append(('Cobertura','zonas-de-servicio-quito'))
    elif k=='zxa': it.append(('Cobertura','zonas-de-servicio-quito')); it.append((ZD[p['zone']]['nombre'],'servicio-tecnico-mabe-en-'+p['zone']))
    elif k=='term': it.append(('Servicios','servicios'))
    elif k=='guia': it.append(('Guías','guias'))
    it.append((p['h1'],slug)); return it

PASOS_MINI=[('Escríbenos','Por WhatsApp o llamada al '+PHONE_TXT+'. Cuéntanos el equipo, el modelo y la falla.'),('Coordinamos la visita','Acordamos día y hora en tu casa, apartamento u oficina de Quito.'),('Diagnóstico en tu casa','Probamos el equipo, identificamos la causa y te explicamos qué tiene.'),('Reparación y prueba','Te damos el costo antes de reparar; si aceptas, reparamos y probamos.')]
def why_band(slug):
    cards=[('stp5','Diagnóstico claro','Probamos el equipo, identificamos la causa y te la explicamos con palabras simples, sin cambiar piezas al azar.'),('stp4','Costo antes de reparar','Te informamos el costo después del diagnóstico y tú decides si continuamos. Sin sorpresas.'),('stp3','A domicilio en Quito','Vamos a tu casa, apartamento u oficina en el norte, centro, sur y valles. Coordinamos por WhatsApp.')]
    h=''.join(f'<div class="wcard">{cimg(slug,n,t)}<h3>{E(t)}</h3><p>{E(d)}</p></div>' for n,t,d in cards)
    return f'<section class="sec why"><div class="wrap"><h2>Por qué pedir tu visita con nosotros</h2><p class="sub">Un servicio ordenado: te explicamos, te cotizamos y recién entonces reparamos.</p><div class="wgrid">{h}</div></div></section>'
def pasos_band(slug):
    ps=''.join(f'<li>{cimg(slug,PIMG[i][0],PIMG[i][1],"pimg")}<div class="pt"><b>{k+1}</b><div><h3>{E(t)}</h3><p>{E(d)}</p></div></div></li>' for k,(i,(t,d)) in enumerate(zip((0,2,3,5),PASOS_MINI)))
    return f'<section class="sec osc"><div class="wrap"><h2>Cómo es la visita</h2><p class="sub">Del primer mensaje a la reparación, así trabajamos.</p><ol class="pasos">{ps}</ol></div></section>'
def cta_band(slug,eq=None):
    t=f'¿Tu {EQ[eq]["sing"]} está fallando?' if eq in EQ else '¿Tu electrodoméstico está fallando?'
    return f'<section class="final foto" style="--bg:url({asset(slug,"img/stp4.webp")})"><div class="wrap"><h2>{E(t)}</h2><p>Escríbenos por WhatsApp con la marca, el modelo y la falla. Te orientamos y coordinamos la visita.</p><a class="btn wa grande" href="{wa(WAHI)}" target="_blank" rel="noopener">{WA_SVG}<span>Escribir por WhatsApp</span></a> <a class="btn linea cl" href="tel:{PHONE_TEL}">Llamar {PHONE_TXT}</a></div></section>'
GFAQ=[('¿Cuándo conviene llamar a un técnico?','Cuando la falla se repite, el equipo hace ruidos nuevos, hay fugas o olor a quemado, o ya probaste lo básico sin resultado.'),('¿La visita incluye diagnóstico?','Sí: probamos el equipo, te explicamos la causa y te damos el costo antes de reparar. Tú decides si continuamos.')]
def page(slug):
    p=PAGES[slug]; items=crumbs(slug,p); ld=[BIZ,bc_ld(items)]
    if p['kind'] in ('service','zona','zxa','term','sector'):
        ld.append({'@context':'https://schema.org','@type':'Service','name':p['h1'],'serviceType':p['h1'],'provider':{'@id':SITE+'/#negocio'},'areaServed':{'@type':'City','name':'Quito'},'url':SITE+'/'+slug+'/','description':p['desc']})
    if p['kind'] in ('guia','falla'):
        ld.append({'@context':'https://schema.org','@type':'Article','headline':p['h1'],'description':p['desc'],'inLanguage':'es-EC','datePublished':TODAY,'dateModified':TODAY,'author':{'@type':'Organization','name':NAME},'publisher':{'@id':SITE+'/#negocio'},'mainEntityOfPage':SITE+'/'+slug+'/'})
    if p['kind']=='guia': p=dict(p); p['faq']=list(p['faq'])+GFAQ
    if p['faq']: ld.append(faq_ld(p['faq']))
    secs=''.join(f'<section><h2>{E(h)}</h2>{fix(b,slug)}</section>' for h,b in p['sections'])
    hero=f'<section class="phero"><div class="wrap">{bc_html(slug,items)}<p class="kick">Servicio técnico Mabe Quito</p><div class="ph-fila">{pth(slug,p,"big")}<div><h1>{E(p["h1"])}</h1><p class="lead">{E(p["lead"])}</p></div></div><div class="acc"><a class="btn wa grande" href="{wa(p["wamsg"])}" target="_blank" rel="noopener">{WA_SVG}<span>Cotizar por WhatsApp</span></a><a class="btn linea cl" href="tel:{PHONE_TEL}">Llamar {PHONE_TXT}</a></div></div></section>'
    body=f'<div class="wrap lay"><article class="art">{galeria(slug,p)}{secs}{faq_html(p["faq"])}</article>{cta_box(slug,p)}</div>{related_html(slug,p)}{why_band(slug)}{pasos_band(slug)}{cta_band(slug,p.get('eq'))}'
    write(slug,head(slug,p['title'],p['desc'],ld,'article' if p['kind'] in ('guia','falla') else 'website')+header(slug)+hero+body+footer(slug))
INFO={'electrodomesticos','fallas-comunes','servicios','zonas-de-servicio-quito','guias','como-trabajamos','preguntas-frecuentes','contacto','aviso-legal','privacidad','mapa-del-sitio'}
def info_page(slug,h1,title,desc,lead,body_html,faq=None,icon='home',wamsg=WAHI,wide=False,raw=False):
    items=[('Inicio',''),(h1,slug)]; ld=[BIZ,bc_ld(items)]+([faq_ld(faq)] if faq else [])
    hero=f'<section class="phero"><div class="wrap">{bc_html(slug,items)}<p class="kick">Servicio técnico Mabe Quito</p><div class="ph-fila"><div><h1>{E(h1)}</h1><p class="lead">{E(lead)}</p></div></div></div></section>'
    body=(fix(body_html,slug) if raw else f'<div class="wrap lay1"><article class="art wide">{fix(body_html,slug)}{faq_html(faq)}</article></div>')
    extra='' if slug in ('privacidad','aviso-legal','mapa-del-sitio','como-trabajamos','contacto') else why_band(slug)+pasos_band(slug)+cta_band(slug)
    write(slug,head(slug,title,desc,ld)+header(slug)+hero+body+extra+footer(slug))
def cardlist(slug,slugs,cls='cards g2'):
    return f'<div class="{cls}">'+''.join(f'<a class="card has-th" href="{url(slug,s)}">{pth(slug,PAGES[s],"sm")}<div><b>{E(PAGES[s]["h1"])}</b><span>{E(ell(PAGES[s]["lead"],105))}</span></div></a>' for s in slugs)+'</div>'
def chips(slug,slugs,label=None):
    return '<div class="chips">'+''.join(f'<a href="{url(slug,s)}">{E(label(s) if label else PAGES[s]["h1"])}</a>' for s in slugs)+'</div>'
# ---------------- páginas ----------------
for s in ORDER: page(s)
HOMEFAQ_X=[('¿Nevera o refrigeradora Mabe: cuál es la diferencia?','Ninguna: son nombres del mismo electrodoméstico. En Quito se usa más refrigeradora, pero reparamos ambas igual y a domicilio.'),('¿Son un centro de servicio Mabe en Quito?','Somos un servicio técnico a domicilio para electrodomésticos Mabe en Quito: en vez de llevar el equipo a un centro, el técnico va a tu casa. Para condiciones de garantía de fábrica, consulta directamente con el fabricante.'),('¿Cuánto cuesta la reparación?','Depende de la falla y de la pieza. Después del diagnóstico te damos el costo antes de reparar y tú decides.'),('¿Qué necesito para pedir el servicio?','Marca y modelo del equipo, la falla que presenta, tu barrio y, si puedes, una foto de la etiqueta y un video corto.'),('¿Atienden los valles de Quito?','Sí: Cumbayá, Tumbaco, Valle de los Chillos y otros sectores de los valles. Escríbenos tu barrio y confirmamos.')]
HOMEFAQ=[('¿Hacen servicio técnico Mabe a domicilio en Quito?','Sí. Vamos a tu casa, apartamento u oficina en Quito: norte, centro, sur y valles. Escríbenos por WhatsApp con el equipo, el modelo y la falla.'),
('¿Qué electrodomésticos Mabe reparan?','Refrigeradoras, congeladores, lavadoras, secadoras, centros de lavado, cocinas, hornos, parrillas y campanas extractoras.'),
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
        h+=f'<section class="eqhub"><h2><a href="@{e["slug"]}@">{E(e["h1"])}</a></h2><div class="tri"><div><h3>Fallas comunes</h3>{fl}</div>'+(f'<div><h3>Servicios</h3>{sv}</div>' if sv else '')+f'<div><h3>Más</h3><ul class="sublist"><li><a href="@{e["slug"]}@">Todo sobre {nm} Mabe</a></li><li><a href="@zonas-de-servicio-quito@">Dónde atendemos</a></li></ul></div></div></section>'
    return h
info_page('electrodomesticos','Electrodomésticos Mabe que reparamos en Quito','Electrodomésticos Mabe que reparamos en Quito | Mabe Quito','Reparamos refrigeradoras, congeladores, lavadoras, secadoras, centros de lavado, cocinas, hornos, parrillas y campanas Mabe en Quito. Fallas y servicios por equipo.','Elige tu electrodoméstico y entra a sus fallas, servicios y zonas, todo en orden.',tree_eq('electrodomesticos')+'<section><h2>¿No ves tu equipo?</h2><p>Escríbenos por WhatsApp con la marca y el modelo y te confirmamos si podemos atenderlo.</p></section>',icon='wrench')
fh=''
for k in EQK:
    e=EQ[k]; fh+=f'<section><h2><a href="@{e["slug"]}@">{E(e["corto"])}</a></h2><ul class="fallas">'+''.join(f'<li><a href="@{s}@">{E(PAGES[s]["h1"])}</a> <span class="tag {mp.URG[e["fallas"][i][2]]}">{e["fallas"][i][2]}</span></li>' for i,s in enumerate(e['slugs']))+'</ul></section>'
info_page('fallas-comunes','Fallas comunes de electrodomésticos Mabe en Quito','Fallas comunes de electrodomésticos Mabe en Quito','Todas las fallas comunes de refrigeradoras, lavadoras, secadoras, cocinas, hornos y más equipos Mabe: causas, qué revisar y cuándo llamar a un técnico en Quito.','Encuentra tu falla por electrodoméstico, mira qué puedes revisar tú con seguridad y cuándo pedir un técnico.',fh,icon='help')
def cards_text(sl,slugs):
    return '<div class="svcs">'+''.join(f'<a class="svc" href="{url(sl,s)}"><b>{E(CORE_LAB.get(s,PAGES[s]["h1"]))}</b><span>{E(ell(PAGES[s]["lead"],110))}</span><i>Ver servicio →</i></a>' for s in slugs)+'</div>'
OTRAS=[s for s in GEN if s not in CORE]
sv='<section><h2>Nuestros servicios</h2>'+'@@CARDS@@'+'</section>'
for k in EQK:
    if TPRIM[k]:
        nm=EQ[k]["art"].split(" ",1)[1]
        sv+=f'<section><h2>Servicios para {nm} Mabe</h2><ul class="sublist">'+''.join(f'<li><a href="@{s}@">{E(TERMS[s]["h1"])}</a></li>' for s in TPRIM[k])+'</ul></section>'
sv+='<section><h2>Más búsquedas frecuentes</h2><ul class="sublist">'+''.join(f'<li><a href="@{s}@">{E(TERMS[s]["h1"])}</a></li>' for s in OTRAS)+'</ul></section><section><h2>Cobertura</h2><ul class="sublist">'+''.join(f'<li><a href="@{SECTOR_HUBS[sc][0]}@">{E(PAGES[SECTOR_HUBS[sc][0]]["h1"])}</a></li>' for sc,_ in SEC_LAB)+''.join(f'<li><a href="@{s}@">{E(TERMS[s]["h1"])}</a></li>' for s in VALLE_TERMS)+'</ul></section>'
sv=sv.replace('@@CARDS@@',cards_text('servicios',CORE))
info_page('servicios','Servicios de reparación y mantenimiento Mabe en Quito','Servicios de reparación y mantenimiento Mabe en Quito','Servicio técnico a domicilio, mantenimiento, instalación, diagnóstico y reparación de electrodomésticos Mabe en Quito, organizados por servicio, equipo y zona.','Todo lo que hacemos por tus electrodomésticos Mabe en Quito, ordenado por servicio, por equipo y por zona.',sv,icon='wrench')
gh=''
for k in EQK:
    gl=list(GEQ.get(k,[]))+(GEQ.get('neveras',[]) if k=='refrigeradoras' else [])
    if gl: gh+=f'<section><h2>{E(EQ[k]["corto"])}</h2><ul class="sublist">'+''.join(f'<li><a href="@{s}@">{E(PAGES[s]["h1"])}</a></li>' for s in gl)+'</ul></section>'
info_page('guias','Guías de electrodomésticos Mabe para Quito','Guías de electrodomésticos Mabe para Quito | Mabe Quito','Guías prácticas sobre refrigeradoras, lavadoras, secadoras, cocinas y hornos Mabe: gas, voltaje, mantenimiento y cuándo reparar, pensadas para Quito.','Explicaciones claras para cuidar tus electrodomésticos y entender qué les pasa, ordenadas por equipo.',gh,icon='doc')
zh=''
for sc,lab in SEC_LAB:
    zs=[z for z in ZSLUGS if ZD[z]['sector']==sc]
    zh+=f'<section><h2><a href="@{SECTOR_HUBS[sc][0]}@">{lab}</a></h2><ul class="cols3">'+''.join(f'<li><a href="@servicio-tecnico-mabe-en-{z}@">{E(ZD[z]["nombre"])}</a></li>' for z in zs)+'</ul></section>'
zh+='<section><h2>¿Tu barrio no aparece?</h2><p>Escríbenos tu dirección por WhatsApp. Muchas veces podemos atender sectores cercanos.</p></section>'
info_page('zonas-de-servicio-quito','Cobertura: barrios de Quito donde atendemos','Cobertura servicio técnico Mabe en Quito: barrios y valles','Servicio técnico Mabe a domicilio en el norte, centro, sur y valles de Quito: La Carolina, Cumbayá, Villaflora, Calderón, Sangolquí y más de 60 barrios.','Elige tu sector y tu barrio para ver cómo coordinamos la visita en tu zona.',zh,icon='pin')
def pli(frm,i,a,b):
    n,alt=PIMG[i]
    return f'<li>{cimg(frm,n,alt,"pimg")}<div class="pt"><b>{i+1}</b><div><h3>{E(a)}</h3><p>{E(b)}</p></div></div></li>'
def step_sec(frm,i,a,b):
    n,alt=PIMG[i]
    return f'<section class="stepsec{" inv" if i%2 else ""}"><div class="wrap"><div class="sfoto">{cimg(frm,n,alt,"sim")}</div><div class="stxt"><span class="snum">{i+1}</span><h2>{E(a)}</h2><p>{E(b)}</p></div></div></section>'
pasos=[('Escríbenos','Por WhatsApp o llamada al 099 350 8191. Cuéntanos qué equipo es, la marca, el modelo y la falla.'),('Envía datos y fotos','Una foto de la etiqueta del equipo y un video corto de la falla ayudan a orientarte mejor.'),('Coordinamos la visita','Acordamos día y hora en tu casa, apartamento u oficina de Quito.'),('Diagnóstico en tu casa','Probamos el equipo, identificamos la causa y te explicamos qué tiene.'),('Costo antes de reparar','Te informamos el costo y tú decides si continuamos.'),('Reparación y prueba','Reparamos y probamos que el equipo quede funcionando.'),('Recomendaciones','Te decimos cómo usarlo y cuidarlo para que la falla no se repita.')]
ch='@@STEPS@@<section class="cierre"><div class="wrap"><h2>Nuestro compromiso con la claridad</h2><p>No cambiamos piezas al azar: primero probamos y diagnosticamos. Si no conviene reparar, te lo decimos.</p></div></section>'
ch=ch.replace('@@STEPS@@',''.join(step_sec('como-trabajamos',i,a,b) for i,(a,b) in enumerate(pasos)))
info_page('como-trabajamos','Cómo trabajamos: servicio técnico Mabe paso a paso','Cómo trabajamos el servicio técnico Mabe en Quito','Así es el servicio técnico Mabe a domicilio en Quito: contacto por WhatsApp, diagnóstico, costo antes de reparar, reparación y recomendaciones.','Del primer mensaje a la reparación: así trabajamos, sin sorpresas.',ch,icon='shield',raw=True)
FAQ_ALL=HOMEFAQ+[('¿Reparan solo Mabe?','Nos enfocamos en electrodomésticos Mabe. Si tienes otra marca, escríbenos y te decimos si podemos ayudarte.'),('¿Qué hago si huele a gas?','Cierra la llave, ventila, no uses llama ni interruptores y llama a un técnico. Si hay riesgo, llama a emergencias (911).'),('¿Atienden apartamentos y conjuntos?','Sí. Coordinamos acceso y horario con la administración.'),('¿Qué datos debo enviar por WhatsApp?','Tipo de equipo, marca y modelo, la falla, tu barrio y una foto de la etiqueta si puedes.'),('¿Instalan electrodomésticos?','Consulta por WhatsApp con el modelo y el tipo de conexión (agua, gas o electricidad) para confirmarte el servicio.'),('¿Qué zonas de Quito atienden?','Norte, centro, sur y valles: La Carolina, Iñaquito, Cotocollao, Villaflora, Quitumbe, Cumbayá, Tumbaco, Calderón, Sangolquí y más. Consulta la lista completa en Zonas.')]
info_page('preguntas-frecuentes','Preguntas frecuentes sobre el servicio técnico Mabe en Quito','Preguntas frecuentes: servicio técnico Mabe en Quito','Respuestas sobre el servicio técnico Mabe a domicilio en Quito: equipos, zonas, costo de la visita, garantía de fábrica y cómo pedir el servicio.','Lo que más nos preguntan antes de pedir una visita.','',faq=FAQ_ALL,icon='help')
info_page('contacto','Contacto: servicio técnico Mabe en Quito','Contacto servicio técnico Mabe Quito | WhatsApp 099 350 8191','Contacta al servicio técnico Mabe en Quito por WhatsApp o llamada al 099 350 8191 (+593 99 350 8191). Cuéntanos tu equipo y la falla.','Escríbenos por WhatsApp o llámanos. Te respondemos con el siguiente paso.',
 f'''<section class="sec"><div class="wrap"><div class="ccards"><div class="ccard"><h2>WhatsApp</h2><p>La forma más rápida: envía el equipo, el modelo, la falla y tu barrio, con una foto de la etiqueta si puedes.</p><a class="btn wa grande" href="{wa(WAHI)}" target="_blank" rel="noopener">{WA_SVG}<span>Escribir por WhatsApp</span></a></div><div class="ccard"><h2>Llamada</h2><p>Si prefieres hablar, llámanos y coordinamos la visita.</p><a class="btn linea grande" href="tel:{PHONE_TEL}">Llamar {PHONE_TXT}</a><p class="mini">{PHONE_FULL}</p></div><div class="ccard"><h2>Cobertura</h2><p>Atendemos el norte, el centro, el sur y los valles de Quito.</p><a class="btn linea grande" href="@zonas-de-servicio-quito@">Ver barrios</a></div></div></div></section>
<section class="stepsec"><div class="wrap"><div class="sfoto">{cimg('contacto','stp1','Cliente conversando con el técnico en su cocina','sim')}</div><div class="stxt"><h2>Qué contarnos</h2><ul class="clist"><li>Qué equipo es, su marca y modelo</li><li>Qué falla presenta y desde cuándo</li><li>Tu barrio o sector de Quito</li><li>Si puedes, una foto de la etiqueta y un video corto del problema</li></ul></div></div></section>
'''+why_band('contacto')+pasos_band('contacto')+f'<div class="wrap lay1"><article class="art wide">{faq_html(FAQ_ALL[:8])}</article></div>'+cta_band('contacto'),icon='chat',raw=True)
info_page('aviso-legal','Aviso legal','Aviso legal | Servicio Técnico Mabe Quito','Aviso legal de Servicio Técnico Mabe Quito: uso de marcas y alcance de la información del sitio.','Uso de marcas y alcance de la información de este sitio.',
 '<section><h2>Marcas</h2><p>Mabe es una marca de su respectivo titular. Este sitio no es operado por Mabe.</p></section><section><h2>Información orientativa</h2><p>El contenido de este sitio es orientativo. El diagnóstico definitivo y el costo se confirman en la visita. Las imágenes del sitio son ilustrativas y no corresponden necesariamente a equipos o personas concretas.</p></section><section><h2>Garantía de fábrica</h2><p>Si tu equipo está en garantía de fábrica, consulta las condiciones con el fabricante antes de solicitar una reparación independiente.</p></section>',icon='shield')
info_page('privacidad','Tratamiento de datos personales','Tratamiento de datos personales | Servicio Técnico Mabe Quito','Cómo trata Servicio Técnico Mabe Quito tus datos personales cuando nos escribes por WhatsApp o nos llamas para pedir una visita en Quito.','Qué datos recibimos y para qué los usamos.',
 f'<section><h2>Qué datos recibimos</h2><p>Cuando nos escribes por WhatsApp o nos llamas recibimos los datos que compartes: nombre, teléfono, barrio o dirección y datos del equipo.</p></section><section><h2>Para qué los usamos</h2><p>Solo para atender tu solicitud, coordinar la visita y dar seguimiento al servicio. No vendemos tus datos.</p></section><section><h2>Tus derechos</h2><p>Puedes pedirnos que corrijamos o eliminemos tus datos escribiendo al {PHONE_TXT}.</p></section>',icon='doc')
# --- portada
HERO_ALT='Técnico explicando una falla a una clienta frente a la refrigeradora (imagen ilustrativa)' if AUTH else 'Técnico de Mabe saludando al cliente en la puerta de su casa (imagen ilustrativa)'
def L(sl,tx,frm=''):
    return f'<a href="{url(frm,sl)}">{tx}</a>' if sl in PAGES else tx
def home():
    s=''
    sv=''.join(f'<a class="svc" href="{url(s,c)}">{cimg(s,SIMG[c][0],SIMG[c][1],"simg")}<b>{CORE_LAB[c]}</b><span>{E(ell(PAGES[c]["lead"],105))}</span><i>Ver servicio →</i></a>' for c in CORE)
    def eqcard(k):
        e=EQ[k]; nm=e["art"].split(" ",1)[1]
        fl=''.join(f'<li><a href="{url(s,x)}">{E(PAGES[x]["h1"])}</a></li>' for x in e['slugs'][:3])
        return f'<div class="eqc">{thumb(s,k,"big")}<h3><a href="{url(s,e["slug"])}">{E(e["h1"])}</a></h3><p>{E(ell(e["intro"],105))}</p><b class="sb">Fallas más consultadas</b><ul>{fl}</ul><a class="enlace" href="{url(s,e["slug"])}">Todo sobre {nm} Mabe →</a></div>'
    eqs=''.join(eqcard(k) for k in EQK)
    cov=''
    for sc,lab in SEC_LAB:
        zs=[z for z in ZSLUGS if ZD[z]['sector']==sc]
        cov+=f'<div class="covc"><h3><a href="{url(s,SECTOR_HUBS[sc][0])}">{lab}</a></h3><ul>'+''.join(f'<li><a href="{url(s,"servicio-tecnico-mabe-en-"+z)}">{E(ZD[z]["nombre"])}</a></li>' for z in zs)+'</ul></div>'
    gcards=cardlist(s,GUIDE_SLUGS[:6])
    ps=''.join(pli(s,j,pasos[j][0],pasos[j][1]).replace(f'<b>{j+1}</b>',f'<b>{k+1}</b>') for k,j in enumerate([0,2,3,5]))
    tecs=''.join(f'<div>{tec_fig(s,n)}</div>' for n in ('tecnico-cocina','tecnico-puerta','tecnico-manos'))
    if AUTH: ASI=f'<div class="tecs">{tecs}</div>'
    else: ASI='<div class="tecs dos">'+''.join(f'<div>{tec_fig(s,n)}</div>' for n in CLEAN)+'</div>'
    nz=len(ZSLUGS)
    eqlinks=', '.join(f'<a href="{url(s,EQ[k]["slug"])}">{EQ[k]["nombre"].lower()}</a>' for k in EQK)
    hero=f'''<section class="hero"><div class="wrap hgrid"><div class="htxt"><p class="kick">Reparación de electrodomésticos a domicilio</p><h1>Servicio técnico Mabe Quito</h1><p class="lead">Reparación de electrodomésticos Mabe en Quito: refrigeradoras, lavadoras, secadoras, cocinas, hornos y más, en tu casa. Diagnóstico claro y costo antes de reparar.</p><div class="acc"><a class="btn wa grande" href="{wa(WAHI)}" target="_blank" rel="noopener">{WA_SVG}<span>Escribir por WhatsApp</span></a><a class="btn linea grande" href="tel:{PHONE_TEL}">Llamar {PHONE_TXT}</a></div><ul class="pts"><li>A domicilio en Quito</li><li>Norte, centro, sur y valles</li><li>Te explicamos la falla antes de reparar</li></ul></div><div class="hmedia"><img src="img/{HERO}.webp" srcset="img/{HERO}-m.webp 640w, img/{HERO}.webp 900w" sizes="(max-width:900px) 92vw, 560px" width="900" height="503" alt="{HERO_ALT}" fetchpriority="high" decoding="async"><div class="hbadge"><b>Costo antes de reparar</b><span>Diagnóstico claro, sin sorpresas</span></div></div></div></section>
<div class="trust"><div class="wrap"><div><b>{len(EQK)}</b><span>tipos de electrodomésticos Mabe</span></div><div><b>{nz}</b><span>barrios y sectores de Quito</span></div><div><b>A domicilio</b><span>norte, centro, sur y valles</span></div><div><b>WhatsApp</b><span>respuesta directa al {PHONE_TXT}</span></div></div></div>'''
    body=f'''<section class="sec" id="servicios"><div class="wrap"><h2>Nuestros servicios</h2><p class="sub">Todo lo que hacemos por tus electrodomésticos Mabe en Quito.</p><div class="svcs">{sv}</div><p style="margin-top:22px"><a class="enlace" href="{url(s,'servicios')}">Ver todos los servicios, por equipo y por zona →</a></p></div></section>
<section class="sec osc" id="electrodomesticos"><div class="wrap"><h2>Electrodomésticos que reparamos</h2><p class="sub">Elige tu equipo: cada uno tiene sus fallas, servicios y zonas.</p><div class="eqgrid">{eqs}</div></div></section>
<section class="sec" id="cobertura"><div class="wrap"><h2>Cobertura: barrios de Quito</h2><p class="sub">Atendemos el norte, el centro, el sur y los valles. Elige tu barrio.</p><figure class="banner">{cimg(s,"c-furgon","Técnico de Mabe llegando a un domicilio en Quito")}<figcaption>Vamos a tu casa en toda Quito</figcaption></figure><div class="covg">{cov}</div><p style="margin-top:22px"><a class="enlace" href="{url(s,'zonas-de-servicio-quito')}">Ver toda la cobertura →</a></p></div></section>
<section class="sec osc"><div class="wrap"><h2>Cómo trabajamos</h2><p class="sub">Vamos hasta donde está tu equipo, lo revisamos y te explicamos antes de reparar.</p><ol class="pasos">{ps}</ol><p style="margin-top:22px"><a class="enlace" href="{url(s,'como-trabajamos')}">Ver el proceso completo paso a paso →</a></p></div></section>
<section class="sec"><div class="wrap"><h2>Guías</h2><p class="sub">Gas, voltaje, limpieza y fallas explicadas para Quito.</p>{gcards}<p style="margin-top:22px"><a class="enlace" href="{url(s,'guias')}">Ver todas las guías →</a></p></div></section>
<section class="sec"><div class="wrap lay1 seo"><h2>Servicio técnico Mabe en Quito: reparación a domicilio</h2><p>Servicio Técnico Mabe Quito reúne la reparación, el mantenimiento y la instalación de electrodomésticos Mabe en Quito: {eqlinks}. Si buscas un {L('centro-de-servicio-mabe-quito','centro de servicio Mabe en Quito')}, aquí es distinto: el técnico va a tu casa, revisa el equipo en su lugar, te explica la falla y te da el costo antes de reparar.</p><p>Cada falla tiene su propia página con causas probables, qué revisar antes de llamar y cuándo conviene pedir al técnico: {L('refrigeradora-mabe-no-enfria-quito','refrigeradora que no enfría')}, {L('lavadora-mabe-no-desagua-quito','lavadora que no desagua')}, {L('lavadora-mabe-no-centrifuga-quito','lavadora que no centrifuga')} o {L('secadora-mabe-no-seca-la-ropa-quito','secadora que no seca')}, entre muchas otras.</p><p>Atendemos {nz} barrios y sectores del norte, el centro, el sur y los valles de Quito, como {L('servicio-tecnico-mabe-en-la-carolina','La Carolina')}, {L('servicio-tecnico-mabe-en-cumbaya','Cumbayá')}, {L('servicio-tecnico-mabe-en-quitumbe','Quitumbe')} o {L('servicio-tecnico-mabe-en-solanda','Solanda')}. Para pedir el servicio, escribe por WhatsApp o llama al {PHONE_TXT} con el modelo del equipo, la falla y tu barrio; también puedes ver {L('agendar-visita-de-servicio-tecnico-mabe-quito','cómo agendar la visita')} o {L('cotizacion-de-reparacion-de-electrodomesticos-mabe-quito','cómo cotizar una reparación')}.</p></div></section>
<section class="sec osc"><div class="wrap lay1">{faq_html(HOMEFAQ+HOMEFAQ_X)}</div></section>
<section class="final foto" style="--bg:url(img/tecnico-cocina-gas.webp)"><div class="wrap"><h2>¿Tu electrodoméstico está fallando?</h2><p>Escríbenos por WhatsApp con la marca, el modelo y la falla. Te orientamos y coordinamos la visita.</p><a class="btn wa grande" href="{wa(WAHI)}" target="_blank" rel="noopener">{WA_SVG}<span>Escribir por WhatsApp</span></a> <a class="btn linea cl" href="tel:{PHONE_TEL}">Llamar {PHONE_TXT}</a></div></section>'''
    ld=[BIZ,{'@context':'https://schema.org','@type':'WebSite','url':SITE+'/','name':NAME,'inLanguage':'es-EC'},faq_ld(HOMEFAQ+HOMEFAQ_X)]
    write('',head('','Servicio Técnico Mabe Quito: Reparación de Electrodomésticos','Servicio técnico Mabe Quito: reparación de electrodomésticos Mabe a domicilio, refrigeradoras, lavadoras, secadoras, cocinas y hornos. WhatsApp 099 350 8191.',ld)+header('')+hero+body+footer(''))
home()
write('404',head('404','Página no encontrada | Mabe Quito','Esta página no existe.',None,noindex=True)+header('404')+'<section class="phero"><div class="wrap"><h1>Página no encontrada</h1><p class="lead">Puede que el enlace haya cambiado. Vuelve al inicio o escríbenos por WhatsApp.</p></div></section>'+footer('404'))

# ---------- mapa del sitio (HTML) ----------
def _li(sl,txt): return f'<li><a href="@{sl}@">{E(txt)}</a></li>'
ms='<section><h2>Servicios</h2><ul class="sublist">'+''.join(_li(c,CORE_LAB[c]) for c in CORE)+'</ul></section>'
for k in EQK:
    e=EQ[k]
    ms+=f'<section><h2><a href="@{e["slug"]}@">{E(e["h1"])}</a></h2><ul class="sublist">'+''.join(_li(s_,PAGES[s_]["h1"]) for s_ in e['slugs'])+'</ul></section>'
ms+='<section><h2>Búsquedas frecuentes</h2><ul class="sublist">'+''.join(_li(s_,TERMS[s_]["h1"]) for s_ in TERMS if s_ not in SECTOR_TERMS)+'</ul></section>'
ms+='<section><h2>Cobertura por sector</h2><ul class="sublist">'+''.join(_li(SECTOR_HUBS[sc][0],PAGES[SECTOR_HUBS[sc][0]]["h1"]) for sc,_ in SEC_LAB)+''.join(_li(s_,TERMS[s_]["h1"]) for s_ in VALLE_TERMS)+'</ul></section>'
ms+='<section><h2>Barrios de Quito</h2><ul class="sublist">'+''.join(_li('servicio-tecnico-mabe-en-'+z,ZD[z]['nombre']) for z in ZSLUGS)+'</ul></section>'
ms+='<section><h2>Guías</h2><ul class="sublist">'+''.join(_li(g_[0],g_[1]) for g_ in GUIDES)+'</ul></section>'
ms+='<section><h2>Más páginas</h2><ul class="sublist">'+''.join(_li(s_,t_) for s_,t_ in (('electrodomesticos','Electrodomésticos'),('fallas-comunes','Fallas comunes'),('servicios','Servicios'),('zonas-de-servicio-quito','Zonas de servicio'),('guias','Guías'),('como-trabajamos','Cómo trabajamos'),('preguntas-frecuentes','Preguntas frecuentes'),('contacto','Contacto')))+'</ul></section>'
info_page('mapa-del-sitio','Mapa del sitio: servicio técnico Mabe Quito','Mapa del sitio | Servicio Técnico Mabe Quito','Todas las páginas de Servicio Técnico Mabe Quito: equipos, fallas, servicios, barrios y guías en un solo lugar.','Encuentra rápido lo que buscas: equipos, fallas, servicios, barrios de Quito y guías.',ms,icon='wrench')
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
