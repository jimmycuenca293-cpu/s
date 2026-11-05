# -*- coding: utf-8 -*-
import os,re,json,shutil,html,datetime,sys
from content import *
import content2,content3,content4,content5,content6,content7
from content3 import EQUIPOS
from content4 import GUIAS_ALL as _G4
from content6 import ZONAS_TODAS as ZS, SERV_NUEVOS, MARCAS
GUIAS_ALL=_G4+content6.NG2
from brand import WA_SVG as WA_NEW,ICON_SVG,logo_pesa
OUT=sys.argv[1] if len(sys.argv)>1 else 'site'
PREVIEW=len(sys.argv)>2 and sys.argv[2]=='preview'   # enlaces relativos con index.html (para verlo sin servidor)
TODAY=datetime.date.today().isoformat()
shutil.rmtree(OUT,ignore_errors=True); os.makedirs(OUT)
E=html.escape
def depth(slug): 
    if slug=='': return 0
    return slug.count('/')+1
def url(frm,to):
    """enlace relativo desde la página frm a la página to ('' = inicio)"""
    up='../'*depth(frm)
    if to=='': t='index.html' if PREVIEW else ''
    else: t=to+('/index.html' if PREVIEW else '/')
    return (up+t) if (up+t) else './'
def asset(frm,name): return '../'*depth(frm)+name
ICON={
 'treadmill':'<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M6 36h30l4-6H10z"/><circle cx="12" cy="40" r="2"/><circle cx="34" cy="40" r="2"/><path d="M34 30l5-18"/><path d="M33 12h8"/><path d="M20 24l3-6 4 2"/><circle cx="22" cy="12" r="2.5"/></svg>',
 'bike':'<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><circle cx="24" cy="30" r="9"/><path d="M24 30l-8-14h8"/><path d="M24 30l8-6 4-12"/><path d="M33 12h6"/><path d="M12 14h8"/><path d="M14 42h20"/></svg>',
 'gym':'<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M8 40V8h24v32"/><path d="M8 8h28"/><path d="M13 16h14M13 22h14M13 28h14M13 34h14"/><path d="M36 14v14"/><circle cx="36" cy="32" r="3"/></svg>',
 'elliptical':'<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M8 40h30"/><path d="M14 40l8-10 8 0 4-16"/><path d="M30 30l-10-16"/><circle cx="34" cy="10" r="2.5"/><path d="M12 34h8"/></svg>',
 'shield':'<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M24 6l14 5v11c0 9-6 16-14 20-8-4-14-11-14-20V11z"/><path d="M17 24l5 5 9-10"/></svg>',
 'home':'<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M6 24L24 8l18 16"/><path d="M12 22v18h24V22"/><path d="M20 40V28h8v12"/></svg>',
 'pin':'<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M24 44s14-13 14-24a14 14 0 10-28 0c0 11 14 24 14 24z"/><circle cx="24" cy="20" r="5"/></svg>',
 'help':'<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><circle cx="24" cy="24" r="18"/><path d="M18 19a6 6 0 1112 0c0 4-6 4-6 9"/><path d="M24 34v.5"/></svg>',
 'chat':'<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M8 10h32v22H20l-8 8v-8H8z"/></svg>',
 'wrench':'<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M30 8a9 9 0 00-8 12L8 34l6 6 14-14a9 9 0 0012-8l-6 5-5-1-1-5z"/></svg>',
}
WA_SVG=WA_NEW
LOGO_MARK=ICON_SVG.replace('<svg xmlns="http://www.w3.org/2000/svg" ','<svg ')
GSC=open('gsc-meta.txt',encoding='utf-8').read().strip() if os.path.exists('gsc-meta.txt') else ''
PRE='<link rel="preload" as="image" href="img/portada-m.webp" imagesrcset="img/portada-m.webp 640w, img/portada.webp 1024w" imagesizes="100vw" fetchpriority="high">'
def head(slug,title,desc,extra_ld=None,og_type='website',noindex=False):
    canon=SITE+('/' if slug=='' else '/'+slug+'/')
    suf=' | Técnico Gym'
    if title.endswith(suf) and len(title)+5<=65: title=title+' Cali'
    ld=''.join(f'<script type="application/ld+json">{json.dumps(x,ensure_ascii=False)}</script>' for x in (extra_ld or []))
    return f'''<!doctype html><html lang="es-CO"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">
{'<meta name="robots" content="noindex">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">'}
<link rel="canonical" href="{canon}"><link rel="alternate" hreflang="es-CO" href="{canon}">
{GSC}<meta name="theme-color" content="#14161a"><meta name="geo.region" content="CO-VAC"><meta name="geo.placename" content="Cali">
<meta property="og:type" content="{og_type}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{canon}"><meta property="og:locale" content="es_CO"><meta property="og:site_name" content="{NAME}"><meta property="og:image" content="{SITE}/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{asset(slug,'favicon.svg')}" type="image/svg+xml"><link rel="apple-touch-icon" href="{asset(slug,'apple-touch-icon.png')}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Barlow:wght@400;500;600&display=swap">
<link rel="stylesheet" href="{asset(slug,'estilo.css')}">{PRE if slug=='' else ''}{ld}</head><body>'''
def header(slug):
    nav=[('servicios','Servicios'),('equipos-que-reparamos','Equipos'),('marcas','Marcas'),('como-trabajamos','Cómo trabajamos'),('guias','Guías'),('zonas-de-servicio-cali','Zonas')]
    links=''.join(f'<a href="{url(slug,"")+"#servicios" if s=="servicios" else url(slug,s)}"{" aria-current=page" if s==slug else ""}>{n}</a>' for s,n in nav)
    return f'''<a class="saltar" href="#contenido">Saltar al contenido</a>
<header class="top"><div class="wrap fila"><a class="logo" href="{url(slug,'')}" aria-label="Técnico Gym, inicio"><span class="mk">{LOGO_MARK}</span><span class="wm"><b>TÉCNICO GYM</b><small>Equipos de gimnasio · Cali</small></span></a>
<nav class="menu" aria-label="Principal">{links}</nav>
<a class="btn wa" href="{wa('Hola Técnico Gym, necesito una revisión de un equipo de gimnasio en Cali.')}" rel="noopener" target="_blank">{WA_SVG}<span>WhatsApp</span></a>
<details class="mov"><summary aria-label="Abrir menú"><span></span></summary><nav aria-label="Menú móvil">{links}</nav></details></div></header>
<main id="contenido">'''
def footer(slug):
    BR=''.join(f'<li><a href="{url(slug,s)}">{PAGES[s]["h1"].replace(" en Cali","")}</a></li>' for s in content5.NB)
    eq=''.join(f'<li><a href="{url(slug,s)}">{PAGES[s]["h1"].replace(" en Cali","")}</a></li>' for s in EQUIPOS[:9])
    gd=''.join(f'<li><a href="{url(slug,s)}">{PAGES[s]["h1"]}</a></li>' for s in GUIAS_ALL[:6])
    zn=''.join(f'<li><a href="{url(slug,s)}">{PAGES[s]["h1"].split(" en ")[-1]}</a></li>' for s in ZS[:6])
    return f'''</main><footer class="pie"><div class="wrap cols"><div><a class="logo" href="{url(slug,'')}"><span class="mk">{LOGO_MARK}</span><span class="wm"><b>TÉCNICO GYM</b><small>Equipos de gimnasio · Cali</small></span></a><p>Reparación y mantenimiento de caminadoras, bicicletas de spinning, elípticas y máquinas multifuncionales en Cali.</p><p><a class="tel" href="tel:{PHONE_TEL}">{PHONE_TXT}</a><br>WhatsApp y llamadas</p></div>
<div><h2>Equipos</h2><ul>{eq}<li><a href="{url(slug,'equipos-que-reparamos')}">Ver todos los equipos</a></li></ul></div><div><h2>Guías</h2><ul>{gd}<li><a href="{url(slug,'guias')}">Ver todas las guías</a></li></ul></div>
<div><h2>Zonas y más</h2><ul>{zn}<li><a href="{url(slug,'zonas-de-servicio-cali')}">Todas las zonas</a></li><li><a href="{url(slug,'servicios')}">Servicios</a></li><li><a href="{url(slug,'marcas')}">Marcas</a></li>{BR}<li><a href="{url(slug,'como-trabajamos')}">Cómo trabajamos</a></li><li><a href="{url(slug,'preguntas-frecuentes')}">Preguntas frecuentes</a></li><li><a href="{url(slug,'contacto')}">Contacto</a></li><li><a href="{url(slug,'privacidad')}">Tratamiento de datos</a></li></ul></div></div>
<div class="wrap base">© {datetime.date.today().year} Técnico Gym Cali · Colombia</div></footer>
<a class="flota" href="{wa('Hola Técnico Gym, necesito una revisión de un equipo de gimnasio en Cali.')}" target="_blank" rel="noopener" aria-label="Escribir por WhatsApp">{WA_SVG}</a></body></html>'''
def fix(html_,slug):
    m={'mantenimiento':'mantenimiento-equipos-gimnasio-cali','zonas':'zonas-de-servicio-cali','domicilio':'reparacion-equipos-gimnasio-a-domicilio-cali','proceso':'como-trabajamos','eq':'equipos-que-reparamos','c':'reparacion-de-caminadoras-cali','e':'reparacion-bicicletas-spinning-cali','m':'reparacion-maquinas-multifuncionales-cali','reparacion':'reparacion-de-caminadoras-cali','banda':'cambio-de-banda-de-caminadora-cali','motor':'reparacion-motor-de-caminadora-cali','tarjeta':'reparacion-tarjeta-controladora-de-caminadora-cali','consola':'reparacion-consola-de-caminadora-cali','calibracion':'calibracion-de-inclinacion-de-caminadora-cali','prev':'mantenimiento-preventivo-de-caminadoras-cali','guia_desgaste':'como-saber-si-la-banda-de-la-caminadora-esta-desgastada','guia_inc':'caminadora-no-sube-la-inclinacion','el':'reparacion-eliptica-cali','usados':'revision-de-equipos-de-gimnasio-usados-antes-de-comprar-cali','banco':'reparacion-banco-de-pesas-cali','costo':'cuanto-cuesta-reparar-una-caminadora','enc':'caminadora-no-enciende','apaga':'caminadora-se-apaga-sola','banda_g':'banda-de-caminadora-patina-o-se-corre','esc':'reparacion-escaladora-stepper-cali','serv':'servicios','vida':'cuanto-dura-una-caminadora'}
    for z in ZS: m['z_'+z]=z
    return re.sub(r'@([\w-]+)@',lambda x:url(slug,m[x.group(1)]),html_)
def crumbs(slug,p):
    items=[('Inicio','')]
    if p['kind']=='guia': items.append(('Guías','guias'))
    elif p['kind']=='zona': items.append(('Zonas','zonas-de-servicio-cali'))
    elif p['kind']=='marca': items.append(('Marcas','marcas'))
    elif slug in SERV_NUEVOS: items.append(('Servicios','servicios'))
    elif slug in EQUIPOS: items.append(('Equipos que reparamos','equipos-que-reparamos'))
    items.append((p['h1'],slug))
    return items
def bc_html(slug,items):
    return '<nav class="migas" aria-label="Ruta">'+' › '.join((f'<a href="{url(slug,s)}">{E(n)}</a>' if s!=slug else f'<span>{E(n)}</span>') for n,s in items)+'</nav>'
def bc_ld(items):
    return {'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':i+1,'name':n,'item':SITE+('/' if s=='' else '/'+s+'/')} for i,(n,s) in enumerate(items)]}
BIZ={'@context':'https://schema.org','@type':'LocalBusiness','@id':SITE+'/#negocio','name':NAME,'url':SITE+'/','telephone':'+57 321 799 6144','image':SITE+'/og.png','logo':SITE+'/logo-pesa.png','description':'Reparación y mantenimiento de caminadoras, bicicletas de spinning, elípticas y máquinas multifuncionales en Cali, Colombia.','address':{'@type':'PostalAddress','addressLocality':'Cali','addressRegion':'Valle del Cauca','addressCountry':'CO'},'geo':{'@type':'GeoCoordinates','latitude':3.4516,'longitude':-76.5320},'areaServed':{'@type':'City','name':'Cali','containedInPlace':{'@type':'AdministrativeArea','name':'Valle del Cauca'}},'knowsAbout':['Reparación de caminadoras','Reparación de bicicletas de spinning','Reparación de máquinas multifuncionales','Mantenimiento de equipos de gimnasio']}
def faq_html(faq):
    if not faq: return ''
    return '<section class="faq"><h2>Preguntas frecuentes</h2>'+''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q,a in faq)+'</section>'
def faq_ld(faq): return {'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in faq]}
def related_html(slug,p):
    if not p.get('related'): return ''
    return '<section class="rel"><h2>También te puede servir</h2><div class="cards">'+''.join(f'<a class="card{" has-th" if s in TH else ""}" href="{url(slug,s)}">{ico_html(slug,s,"sm") if s in TH else ""}<div><b>{E(PAGES[s]["h1"])}</b><span>{E(PAGES[s]["lead"][:110])}…</span></div></a>' for s in p['related'])+'</div></section>'
def cta_box(slug,p):
    return f'<aside class="caja"><h2>¿Necesitas ayuda con tu equipo?</h2><p>Escríbenos la marca, el modelo y qué falla presenta. Te orientamos por WhatsApp.</p><a class="btn wa grande" href="{wa(p["wamsg"])}" target="_blank" rel="noopener">{WA_SVG}<span>Escribir por WhatsApp</span></a><a class="btn linea" href="tel:{PHONE_TEL}">Llamar {PHONE_TXT}</a></aside>'
def write(slug,content):
    d=OUT if slug=='' else os.path.join(OUT,slug); os.makedirs(d,exist_ok=True)
    open(os.path.join(d,'index.html'),'w',encoding='utf-8').write(content)

PH={'caminadora-gimnasio-1':'Caminadora eléctrica de gimnasio con pantalla táctil','caminadora-gimnasio-2':'Caminadora comercial con consola y banda ancha','bicicleta-spinning-1':'Bicicleta de spinning para casa con monitor y volante de inercia','bicicleta-spinning-2':'Bicicleta de spinning de gimnasio con volante pesado','multifuncional-1':'Máquina multifuncional de casa con pila de pesas y polea alta','multifuncional-2':'Máquina multifuncional con estación de poleas, prensa de piernas y banco','eliptica-1':'Bicicleta elíptica con consola y pedales','escaladora-1':'Escaladora de escalones giratorios con consola y pasamanos'}
CAP={'caminadora-gimnasio-1':'Caminadora de gimnasio','caminadora-gimnasio-2':'Caminadora comercial','bicicleta-spinning-1':'Bicicleta de spinning para casa','bicicleta-spinning-2':'Bicicleta de spinning de gimnasio','multifuncional-1':'Multifuncional con pila de pesas','multifuncional-2':'Multifuncional con poleas','eliptica-1':'Elíptica','escaladora-1':'Escaladora de escalones'}
PHOTOS={'tecnico-de-equipos-de-gimnasio-cali':['caminadora-gimnasio-1','multifuncional-2','bicicleta-spinning-2'],'arreglo-de-caminadoras-cali':['caminadora-gimnasio-1'],'reparacion-de-trotadoras-cali':['caminadora-gimnasio-2'],'reparacion-de-maquinas-de-gimnasio-cali':['multifuncional-2','bicicleta-spinning-2'],'reparacion-de-equipos-fitness-cali':['bicicleta-spinning-2','multifuncional-2'],'reparacion-de-equipos-de-gimnasio-comercial-cali':['caminadora-gimnasio-2','escaladora-1'],'reparacion-de-escaladoras-stairmaster-cali':['escaladora-1'],'reparacion-escaladora-stepper-cali':['escaladora-1'],'reparacion-de-caminadoras-cali':['caminadora-gimnasio-1','caminadora-gimnasio-2'],'reparacion-bicicletas-spinning-cali':['bicicleta-spinning-2','bicicleta-spinning-1'],'reparacion-bicicleta-estatica-cali':['bicicleta-spinning-1'],'reparacion-maquinas-multifuncionales-cali':['multifuncional-1','multifuncional-2'],'reparacion-estacion-de-poleas-cali':['multifuncional-2'],'reparacion-eliptica-cali':['eliptica-1'],'mantenimiento-equipos-gimnasio-cali':['caminadora-gimnasio-2','bicicleta-spinning-2','multifuncional-2'],'reparacion-equipos-ultimate-fitness-cali':['caminadora-gimnasio-1','multifuncional-2','eliptica-1'],'reparacion-equipos-centurfit-cali':['caminadora-gimnasio-2'],'reparacion-equipos-evolution-fitness-cali':['bicicleta-spinning-1','bicicleta-spinning-2'],'reparacion-equipos-sportfitness-cali':['multifuncional-1'],'servicio-tecnico-de-caminadoras-cali':['caminadora-gimnasio-1','caminadora-gimnasio-2'],'mantenimiento-preventivo-de-caminadoras-cali':['caminadora-gimnasio-2'],'cambio-de-banda-de-caminadora-cali':['caminadora-gimnasio-1'],'reparacion-de-cables-y-poleas-de-maquinas-de-gimnasio-cali':['multifuncional-2','multifuncional-1'],'mantenimiento-de-gimnasios-en-conjuntos-residenciales-cali':['caminadora-gimnasio-2','bicicleta-spinning-2'],'mantenimiento-equipos-gimnasio-hoteles-y-empresas-cali':['caminadora-gimnasio-1','multifuncional-2']}
def fig(slug,n,eager=False):
    return f'<figure><img src="{asset(slug,"img/"+n+".webp")}" srcset="{asset(slug,"img/"+n+"-m.webp")} 460w, {asset(slug,"img/"+n+".webp")} 900w" sizes="(max-width:700px) 90vw, 330px" width="900" height="900" alt="{E(PH[n])}" loading="{"eager" if eager else "lazy"}" decoding="async"><figcaption>{E(CAP[n])}</figcaption></figure>'
TPH={'tecnico-caminadora':('Técnico revisando el motor de una caminadora en un gimnasio (imagen ilustrativa)','Revisión de una caminadora (imagen ilustrativa)'),'tecnico-spinning':('Técnico reparando una bicicleta de spinning (imagen ilustrativa)','Reparación de una bicicleta de spinning (imagen ilustrativa)'),'tecnico-domicilio':('Técnico con su caja de herramientas llegando a una casa para una reparación a domicilio (imagen ilustrativa)','Servicio a domicilio en Cali (imagen ilustrativa)')}
_cam=['reparacion-de-caminadoras-cali','servicio-tecnico-de-caminadoras-cali','arreglo-de-caminadoras-cali','reparacion-de-trotadoras-cali','tecnico-de-equipos-de-gimnasio-cali','mantenimiento-preventivo-de-caminadoras-cali','reparacion-motor-de-caminadora-cali','reparacion-tarjeta-controladora-de-caminadora-cali']
_spin=['reparacion-bicicletas-spinning-cali','reparacion-bicicleta-estatica-cali','mantenimiento-equipos-gimnasio-cali','reparacion-de-equipos-fitness-cali','mantenimiento-de-bicicleta-de-spinning-paso-a-paso']
_dom=['reparacion-equipos-gimnasio-a-domicilio-cali','como-trabajamos','tecnico-de-equipos-de-gimnasio-cerca-de-mi-cali','reparacion-de-maquinas-de-ejercicio-cali','contacto','zonas-de-servicio-cali']
TEC={}
for k in _cam: TEC[k]='tecnico-caminadora'
for k in _spin: TEC[k]='tecnico-spinning'
for k in _dom: TEC[k]='tecnico-domicilio'
def tec_fig(slug,n):
    alt,cap=TPH[n]
    return f'<figure class="tec"><img src="{asset(slug,"img/"+n+".webp")}" srcset="{asset(slug,"img/"+n+"-m.webp")} 560w, {asset(slug,"img/"+n+".webp")} 1000w" sizes="(max-width:700px) 92vw, 700px" width="1000" height="559" alt="{E(alt)}" loading="lazy" decoding="async"><figcaption>{E(cap)}</figcaption></figure>'

def galeria(slug):
    ph=PHOTOS.get(slug)
    t=tec_fig(slug,TEC[slug]) if slug in TEC else ''
    if not ph: return t
    return t+'<div class="gal">'+''.join(fig(slug,n,i==0) for i,n in enumerate(ph))+'</div><p class="refimg">Imágenes de referencia.</p>'

TH={'tecnico-de-equipos-de-gimnasio-cali':'caminadora-gimnasio-1','arreglo-de-caminadoras-cali':'caminadora-gimnasio-1','reparacion-de-trotadoras-cali':'caminadora-gimnasio-2','reparacion-de-maquinas-de-gimnasio-cali':'multifuncional-2','reparacion-de-equipos-fitness-cali':'bicicleta-spinning-2','reparacion-de-maquinas-de-ejercicio-cali':'bicicleta-spinning-1','reparacion-de-equipos-de-gimnasio-comercial-cali':'caminadora-gimnasio-2','reparacion-de-escaladoras-stairmaster-cali':'escaladora-1','reparacion-de-caminadoras-cali':'caminadora-gimnasio-1','reparacion-caminadora-plegable-cali':'caminadora-gimnasio-2','reparacion-caminadora-magnetica-cali':'caminadora-gimnasio-1','reparacion-caminadora-bajo-escritorio-cali':'caminadora-gimnasio-2','servicio-tecnico-de-caminadoras-cali':'caminadora-gimnasio-2','mantenimiento-preventivo-de-caminadoras-cali':'caminadora-gimnasio-1','cambio-de-banda-de-caminadora-cali':'caminadora-gimnasio-2','reparacion-motor-de-caminadora-cali':'caminadora-gimnasio-1','reparacion-tarjeta-controladora-de-caminadora-cali':'caminadora-gimnasio-2','reparacion-consola-de-caminadora-cali':'caminadora-gimnasio-1','calibracion-de-inclinacion-de-caminadora-cali':'caminadora-gimnasio-2','revision-de-equipos-de-gimnasio-usados-antes-de-comprar-cali':'caminadora-gimnasio-1','mantenimiento-equipos-gimnasio-cali':'caminadora-gimnasio-2','mantenimiento-de-gimnasios-en-conjuntos-residenciales-cali':'caminadora-gimnasio-2','mantenimiento-equipos-gimnasio-hoteles-y-empresas-cali':'caminadora-gimnasio-1','reparacion-equipos-gimnasio-a-domicilio-cali':'multifuncional-2',
'reparacion-bicicleta-estatica-cali':'bicicleta-spinning-1','reparacion-bicicleta-reclinada-cali':'bicicleta-spinning-1','reparacion-bicicletas-spinning-cali':'bicicleta-spinning-2','reparacion-air-bike-cali':'bicicleta-spinning-2','reparacion-eliptica-cali':'eliptica-1','reparacion-escaladora-stepper-cali':'escaladora-1',
'reparacion-maquinas-multifuncionales-cali':'multifuncional-1','reparacion-estacion-de-poleas-cali':'multifuncional-2','reparacion-maquina-smith-cali':'multifuncional-2','reparacion-prensa-de-piernas-cali':'multifuncional-1','reparacion-banco-de-pesas-cali':'multifuncional-1','reparacion-maquina-mariposa-pec-deck-cali':'multifuncional-2','reparacion-torre-de-potencia-cali':'multifuncional-1','reparacion-de-cables-y-poleas-de-maquinas-de-gimnasio-cali':'multifuncional-2','retapizado-de-bancos-y-asientos-de-gimnasio-cali':'multifuncional-1',
'reparacion-equipos-ultimate-fitness-cali':'caminadora-gimnasio-1','reparacion-equipos-centurfit-cali':'caminadora-gimnasio-2','reparacion-equipos-evolution-fitness-cali':'bicicleta-spinning-1','reparacion-equipos-sportfitness-cali':'multifuncional-1'}
def ico_html(frm,slug,cls=''):
    n=TH.get(slug)
    if n: return f'<span class="ico th {cls}"><img src="{asset(frm,"img/"+n+"-s.webp")}" alt="" width="240" height="240" loading="lazy" decoding="async"></span>'
    ic=PAGES.get(slug,{}).get('icon','')
    return f'<span class="ico {cls}">{ICON[ic]}</span>' if ic in ICON else ''

def page(slug):
    p=PAGES[slug]; items=crumbs(slug,p); ld=[BIZ,bc_ld(items)]
    if p['kind'] in ('service','zona','marca'):
        ld.append({'@context':'https://schema.org','@type':'Service','name':p['h1'],'serviceType':p['h1'],'provider':{'@id':SITE+'/#negocio'},'areaServed':{'@type':'City','name':'Cali'},'url':SITE+'/'+slug+'/','description':p['desc']})
    if p['kind']=='guia':
        ld.append({'@context':'https://schema.org','@type':'Article','headline':p['h1'],'description':p['desc'],'inLanguage':'es-CO','datePublished':TODAY,'dateModified':TODAY,'author':{'@type':'Organization','name':NAME},'publisher':{'@id':SITE+'/#negocio'},'mainEntityOfPage':SITE+'/'+slug+'/'})
    if p['faq']: ld.append(faq_ld(p['faq']))
    secs=''.join(f'<section><h2>{E(h)}</h2>{fix(b,slug)}</section>' for h,b in p['sections'])
    ic=ICON.get(p.get('icon',''),'')
    hero=f'<section class="phero"><div class="wrap">{bc_html(slug,items)}<div class="ph-fila">{ico_html(slug,slug,"big")}<div><h1>{E(p["h1"])}</h1><p class="lead">{E(p["lead"])}</p></div></div><div class="acc"><a class="btn wa grande" href="{wa(p["wamsg"])}" target="_blank" rel="noopener">{WA_SVG}<span>Cotizar por WhatsApp</span></a><a class="btn linea cl" href="tel:{PHONE_TEL}">Llamar {PHONE_TXT}</a></div></div></section>'
    body=f'<div class="wrap lay"><article class="art">{galeria(slug)}{secs}{faq_html(p["faq"])}</article>{cta_box(slug,p)}</div>{related_html(slug,p)}'
    write(slug,head(slug,p['title'],p['desc'],ld,'article' if p['kind']=='guia' else 'website')+header(slug)+hero+body+footer(slug))
import content3
for s in sorted(set(SERVICIOS+EQUIPOS+ZS+GUIAS_ALL+SERV_NUEVOS+MARCAS+['zonas-de-servicio-cali','contacto','como-trabajamos'])): page(s)
# FAQ page usa su propia lista
def faq_page():
    s='preguntas-frecuentes'; p=PAGES[s]; items=crumbs(s,p)
    ld=[BIZ,bc_ld(items),faq_ld(p['faq'])]
    hero=f'<section class="phero"><div class="wrap">{bc_html(s,items)}<div class="ph-fila"><span class="ico">{ICON["help"]}</span><div><h1>{E(p["h1"])}</h1><p class="lead">{E(p["lead"])}</p></div></div></div></section>'
    body=f'<div class="wrap lay"><article class="art">{faq_html(p["faq"]).replace("<h2>Preguntas frecuentes</h2>","")}</article>{cta_box(s,p)}</div>{related_html(s,p)}'
    write(s,head(s,p['title'],p['desc'],ld)+header(s)+hero+body+footer(s))
faq_page()
# hub de guías
def guias_hub():
    s='guias'; ttl='Guías de reparación de equipos de gimnasio | Técnico Gym'; dsc='Guías prácticas: caminadora que no enciende, banda que patina, ruidos, lubricación, spinning y costos de reparación. Consejos de técnicos en Cali.'
    items=[('Inicio',''),('Guías','guias')]
    cards=''.join(f'<a class="card" href="{url(s,g)}"><b>{E(PAGES[g]["h1"])}</b><span>{E(PAGES[g]["lead"])}</span></a>' for g in GUIAS_ALL)
    hero=f'<section class="phero"><div class="wrap">{bc_html(s,items)}<h1>Guías de reparación de equipos de gimnasio</h1><p class="lead">Qué revisar cuando tu caminadora o tu bicicleta falla, qué es normal y cuándo llamar a un técnico.</p></div></section>'
    p={'wamsg':'Hola Técnico Gym, tengo una duda sobre un equipo de gimnasio.'}
    write(s,head(s,ttl,dsc,[BIZ,bc_ld(items)])+header(s)+hero+f'<div class="wrap lay"><div class="art"><div class="cards g2">{cards}</div></div>{cta_box(s,p)}</div>'+footer(s))
guias_hub()
# privacidad
def privacidad():
    s='privacidad'; items=[('Inicio',''),('Tratamiento de datos','privacidad')]
    txt=f'<p>Técnico Gym recibe tus datos (nombre, teléfono, barrio y datos del equipo) cuando nos escribes por WhatsApp o nos llamas, y los usa solo para atender tu solicitud: orientarte, coordinar la visita y cotizar la reparación.</p><p>No vendemos ni compartimos tus datos con terceros para publicidad. Puedes pedirnos que los consultemos, actualicemos o eliminemos escribiendo al WhatsApp <b>{PHONE_TXT}</b>, conforme a la Ley 1581 de 2012 de protección de datos personales en Colombia.</p><p>Este sitio no tiene formularios ni cuentas de usuario. Los enlaces de WhatsApp abren tu aplicación con un mensaje prellenado.</p>'
    hero=f'<section class="phero"><div class="wrap">{bc_html(s,items)}<h1>Tratamiento de datos personales</h1></div></section>'
    write(s,head(s,'Tratamiento de datos personales | Técnico Gym','Cómo Técnico Gym trata tus datos personales cuando nos escribes por WhatsApp o nos llamas para pedir una revisión en Cali.',[bc_ld(items)])+header(s)+hero+f'<div class="wrap lay"><article class="art">{txt}</article></div>'+footer(s))
privacidad()
# 404
write('404',head('404','Página no encontrada | Técnico Gym','Esta página no existe.',None,noindex=True)+header('404')+'<section class="phero"><div class="wrap"><h1>Página no encontrada</h1><p class="lead">Puede que el enlace haya cambiado. Vuelve al inicio o escríbenos por WhatsApp.</p></div></section>'+footer('404'))
# ------- HOME -------

GRUPO={'reparacion-de-caminadoras-cali':'Cardio','reparacion-bicicletas-spinning-cali':'Cardio','reparacion-eliptica-cali':'Cardio','reparacion-maquinas-multifuncionales-cali':'Fuerza'}
for m_ in content3.M: GRUPO[m_['slug']]=m_['g']
def equipos_hub():
    s='equipos-que-reparamos'; items=[('Inicio',''),('Equipos que reparamos','equipos-que-reparamos')]
    ttl='Equipos de gimnasio que reparamos en Cali | Técnico Gym'; dsc='Reparamos caminadoras, bicicletas, elípticas, remos, escaladoras, multifuncionales, bancos y más equipos de gimnasio en casa en Cali. Mira la lista completa.'
    blocks=''
    for gname,sub in [('Cardio','Caminadoras, bicicletas, elípticas y más equipos para el entrenamiento cardiovascular.'),('Fuerza','Máquinas multifuncionales, poleas, Smith, prensa, bancos y torres.'),('Otros','Equipos de apoyo para el entrenamiento en casa.')]:
        cards=''.join(f'<a class="card has-th" href="{url(s,k)}">{ico_html(s,k,"sm")}<div><b>{E(PAGES[k]["h1"].replace(" en Cali",""))}</b><span>{E(PAGES[k]["lead"][:105])}…</span></div></a>' for k in EQUIPOS if GRUPO.get(k)==gname)
        blocks+=f'<section><h2>{gname}</h2><p>{sub}</p><div class="cards g2">{cards}</div></section>'
    hero=f'<section class="phero"><div class="wrap">{bc_html(s,items)}<h1>Equipos de gimnasio que reparamos en Cali</h1><p class="lead">Reparamos los equipos que más se usan para hacer ejercicio en casa y en gimnasios. Si no ves el tuyo, escríbenos: casi siempre podemos revisarlo.</p></div></section>'
    p={'wamsg':'Hola Técnico Gym, quiero saber si reparan mi equipo de gimnasio en Cali. Equipo: __ Marca: __'}
    ld=[BIZ,bc_ld(items),{'@context':'https://schema.org','@type':'ItemList','name':'Equipos de gimnasio que reparamos','itemListElement':[{'@type':'ListItem','position':i+1,'url':SITE+'/'+k+'/','name':PAGES[k]['h1']} for i,k in enumerate(EQUIPOS)]}]
    write(s,head(s,ttl,dsc,ld)+header(s)+hero+f'<div class="wrap lay"><div class="art">{blocks}</div>{cta_box(s,p)}</div>'+footer(s))
equipos_hub()

SERV_GRUPOS=[('Caminadoras','Servicio técnico y reparaciones específicas de caminadoras.',['servicio-tecnico-de-caminadoras-cali','mantenimiento-preventivo-de-caminadoras-cali','cambio-de-banda-de-caminadora-cali','reparacion-motor-de-caminadora-cali','reparacion-tarjeta-controladora-de-caminadora-cali','reparacion-consola-de-caminadora-cali','calibracion-de-inclinacion-de-caminadora-cali']),
 ('Gimnasios, conjuntos y empresas','Mantenimiento periódico para equipos de uso compartido.',['mantenimiento-equipos-gimnasio-cali','mantenimiento-de-gimnasios-en-conjuntos-residenciales-cali','mantenimiento-equipos-gimnasio-hoteles-y-empresas-cali']),
 ('Otros servicios','Máquinas de fuerza, tapicería, revisión de equipos usados y visitas a domicilio.',['reparacion-de-cables-y-poleas-de-maquinas-de-gimnasio-cali','retapizado-de-bancos-y-asientos-de-gimnasio-cali','revision-de-equipos-de-gimnasio-usados-antes-de-comprar-cali','reparacion-equipos-gimnasio-a-domicilio-cali'])]
SERV_GRUPOS.insert(0,('Lo que más se busca en Cali','Las formas en que la gente busca un técnico de equipos de gimnasio en Cali.',content7.N7S))
def servicios_hub():
    s='servicios'; items=[('Inicio',''),('Servicios','servicios')]
    ttl='Servicios de Reparación de Gimnasio en Cali | Técnico Gym'; dsc='Servicio técnico, mantenimiento y reparación de caminadoras, bicicletas, elípticas y multifuncionales en Cali: banda, motor, tarjeta, consola, tapicería y más.'
    blocks=''
    for t,sub,ks in SERV_GRUPOS:
        cards=''.join(f'<a class="card has-th" href="{url(s,k)}">{ico_html(s,k,"sm")}<div><b>{E(PAGES[k]["h1"].replace(" en Cali",""))}</b><span>{E(PAGES[k]["lead"][:105])}…</span></div></a>' for k in ks)
        blocks+=f'<section><h2>{t}</h2><p>{sub}</p><div class="cards g2">{cards}</div></section>'
    hero=f'<section class="phero"><div class="wrap">{bc_html(s,items)}<h1>{E(PAGES[s]["h1"])}</h1><p class="lead">{E(PAGES[s]["lead"])}</p></div></section>'
    ld=[BIZ,bc_ld(items)]
    write(s,head(s,ttl,dsc,ld)+header(s)+hero+f'<div class="wrap lay"><div class="art">{blocks}</div>{cta_box(s,PAGES[s])}</div>'+footer(s))
servicios_hub()
def marcas_hub():
    s='marcas'; items=[('Inicio',''),('Marcas','marcas')]
    ttl='Marcas de equipos de gimnasio que reparamos en Cali | Técnico Gym'; dsc='Reparamos equipos Ultimate Fitness, Centurfit, Evolution Fitness, Sportfitness y otras marcas en Cali. Servicio técnico independiente a domicilio.'
    cards=''.join(f'<a class="card has-th" href="{url(s,k)}">{ico_html(s,k,"sm")}<div><b>{E(PAGES[k]["h1"])}</b><span>{E(PAGES[k]["lead"][:110])}…</span></div></a>' for k in MARCAS)
    body=f'<section><h2>Marcas</h2><div class="cards g2">{cards}</div></section><section><h2>¿Tu marca no aparece?</h2><p>Revisamos equipos de distintas marcas. Escríbenos la marca y el modelo y te confirmamos si podemos atenderlo.</p><p><b>Aviso:</b> Técnico Gym es un servicio técnico independiente. No somos distribuidores ni centro de servicio autorizado de estas marcas; sus nombres se usan solo para indicar los equipos que atendemos.</p></section>'
    hero=f'<section class="phero"><div class="wrap">{bc_html(s,items)}<h1>{E(PAGES[s]["h1"])}</h1><p class="lead">{E(PAGES[s]["lead"])}</p></div></section>'
    write(s,head(s,ttl,dsc,[BIZ,bc_ld(items)])+header(s)+hero+f'<div class="wrap lay"><div class="art">{body}</div>{cta_box(s,PAGES[s])}</div>'+footer(s))
marcas_hub()

LOGOBIG=logo_pesa(True).replace('currentColor','#c5ccd5')
def chip_img(frm,k):
    n=TH.get(k)
    return f'<img src="{asset(frm,"img/"+n+"-s.webp")}" alt="" width="28" height="28" loading="lazy" decoding="async">' if n else ''
SVC_HOME=SERVICIOS+['servicio-tecnico-de-caminadoras-cali','cambio-de-banda-de-caminadora-cali','reparacion-motor-de-caminadora-cali','reparacion-tarjeta-controladora-de-caminadora-cali','reparacion-consola-de-caminadora-cali','calibracion-de-inclinacion-de-caminadora-cali','mantenimiento-preventivo-de-caminadoras-cali','reparacion-escaladora-stepper-cali','reparacion-banco-de-pesas-cali']
def home():
    TECS=''.join(f'<a class="gi" href="{url("",k)}">{tec_fig("",n)}</a>' for n,k in [('tecnico-caminadora','reparacion-de-caminadoras-cali'),('tecnico-spinning','reparacion-bicicletas-spinning-cali'),('tecnico-domicilio','reparacion-equipos-gimnasio-a-domicilio-cali')])
    s=''
    ld=[BIZ,{'@context':'https://schema.org','@type':'WebSite','url':SITE+'/','name':NAME,'inLanguage':'es-CO'}]
    faq=[('¿Reparan caminadoras a domicilio en Cali?','Sí. Atendemos en Cali. Escríbenos por WhatsApp con tu barrio, la marca y la falla y coordinamos la visita.'),('¿Qué equipos reparan?','Caminadoras, bicicletas de spinning y estáticas, elípticas y máquinas multifuncionales, de casa y de gimnasio.'),('¿Cuánto cuesta reparar una caminadora?','Depende de la falla y del equipo. Primero diagnosticamos y te informamos el costo antes de reparar.'),('¿Atienden gimnasios y condominios?','Sí. Podemos acordar visitas periódicas de mantenimiento preventivo.')]
    ld.append(faq_ld(faq))
    cards=''.join(f'<a class="svc" href="{url(s,k)}">{ico_html(s,k)}<b>{E(PAGES[k]["h1"])}</b><span>{E(PAGES[k]["lead"][:120])}…</span><i>Ver servicio →</i></a>' for k in SVC_HOME)
    fallas=[('Caminadora no enciende','caminadora-no-enciende'),('La banda patina o se corre','banda-de-caminadora-patina-o-se-corre'),('Ruido en la caminadora','ruido-en-la-caminadora'),('Se apaga sola','caminadora-se-apaga-sola'),('Spinning con ruido','bicicleta-spinning-hace-ruido'),('¿Cuánto cuesta reparar?','cuanto-cuesta-reparar-una-caminadora')]
    HG=''.join(f'<a class="gi" href="{url(s,k)}">{fig(s,n)}</a>' for n,k in [('caminadora-gimnasio-1','reparacion-de-caminadoras-cali'),('bicicleta-spinning-2','reparacion-bicicletas-spinning-cali'),('multifuncional-2','reparacion-maquinas-multifuncionales-cali'),('eliptica-1','reparacion-eliptica-cali'),('multifuncional-1','reparacion-maquinas-multifuncionales-cali'),('bicicleta-spinning-1','reparacion-bicicleta-estatica-cali')])
    cali_chips=''.join(f'<a href="{url(s,k)}">{E(PAGES[k]["h1"].replace(" en Cali",""))}</a>' for k in content7.N7S)
    svc2=''.join(f'<a href="{url(s,k)}">{E(PAGES[k]["h1"].replace(" en Cali",""))}</a>' for k in dict.fromkeys([k for k in SERVICIOS+SERV_NUEVOS if k not in content7.N7S and k not in SVC_HOME]+['calibracion-de-inclinacion-de-caminadora-cali','mantenimiento-equipos-gimnasio-hoteles-y-empresas-cali']))
    mchips=''.join(f'<a href="{url(s,k)}">{E(PAGES[k]["h1"].split("de ")[-1].replace(" en Cali","").replace("Reparación ",""))}</a>' for k in MARCAS)
    eqchips=''.join(f'<a href="{url(s,k)}">{chip_img(s,k)}{E(PAGES[k]["h1"].replace(" en Cali","").replace("Reparación de ","").capitalize())}</a>' for k in EQUIPOS)
    gcards=''.join(f'<a class="card" href="{url(s,k)}"><b>{E(PAGES[k]["h1"])}</b><span>{E(PAGES[k]["lead"][:100])}…</span></a>' for k in GUIAS_ALL[:6])
    fl=''.join(f'<a href="{url(s,g)}">{E(n)}</a>' for n,g in fallas)
    hero_svg='<svg viewBox="0 0 520 380" class="herosvg" role="img" aria-label="Ilustración de una persona corriendo en una caminadora"><ellipse cx="260" cy="356" rx="236" ry="9" fill="#0b0d10"/><g stroke="#FFC400" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" fill="none"><path d="M54 296h340a16 16 0 0 1 16 16v10H38v-10a16 16 0 0 1 16-16z" fill="#1d2025"/><path d="M72 322l-14 30M380 322l14 30"/><path d="M390 292L446 98"/><rect x="404" y="50" width="106" height="60" rx="10" fill="#1d2025"/><path d="M426 72h62M426 90h38" stroke-width="5"/><path d="M440 116C384 120 334 152 312 204" stroke-width="5"/><circle cx="76" cy="304" r="7" fill="#14161a"/><circle cx="384" cy="304" r="7" fill="#14161a"/></g><path d="M96 301h280" stroke="#4a525c" stroke-width="3" stroke-dasharray="12 12" fill="none"/><g stroke="#fff" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" fill="none"><circle cx="226" cy="124" r="16" fill="#fff"/><path d="M222 148L206 214"/><path d="M220 164L252 186L276 172"/><path d="M220 164L190 186L176 210"/><path d="M206 214L240 244L236 288"/><path d="M206 214L176 250L144 262"/></g></svg>'
    pasos=[('Escríbenos','Cuéntanos por WhatsApp la marca, el modelo y qué le pasa. Una foto o un video ayuda.'),('Diagnóstico','Revisamos el equipo y te explicamos la falla antes de reparar.'),('Cotización clara','Te informamos el costo y las piezas necesarias antes de empezar.'),('Reparación y prueba','Reparamos y probamos el equipo con carga antes de dejarlo listo.')]
    ps=''.join(f'<li><b>{i+1}</b><div><h3>{E(t)}</h3><p>{E(d)}</p></div></li>' for i,(t,d) in enumerate(pasos))
    quien=[('Equipos en casa','Caminadoras, bicicletas y elípticas de uso doméstico. Vamos hasta tu casa.'),('Gimnasios y estudios','Mantenimiento y reparación para que las máquinas no queden fuera de servicio.'),('Condominios y empresas','Zonas de ejercicio de conjuntos, hoteles y empresas en Cali.')]
    qs=''.join(f'<div class="q"><h3>{E(t)}</h3><p>{E(d)}</p></div>' for t,d in quien)
    zonas=['Ciudad Jardín','Pance','Valle del Lili','Granada','Versalles','San Fernando','Chipichape','Normandía','Cañasgordas','Ciudad 2000','Santa Mónica','Limonar']
    zh=''.join(f'<span>{z}</span>' for z in zonas)
    hero=f'''<section class="hero"><div class="hero-bg"><img src="img/portada.webp" srcset="img/portada-m.webp 640w, img/portada.webp 1024w" sizes="100vw" width="1024" height="572" alt="Atención al cliente en la recepción de Técnico Gym Cali" fetchpriority="high" decoding="async"></div><div class="wrap hgrid"><div><p class="kick">Técnicos en Cali</p><h1>Reparación de caminadoras y equipos de gimnasio en Cali</h1><p class="lead">Caminadoras, bicicletas de spinning, elípticas y máquinas multifuncionales. Cuéntanos qué falla por WhatsApp y te orientamos.</p><div class="acc"><a class="btn wa grande" href="{wa('Hola Técnico Gym, necesito reparar un equipo de gimnasio en Cali. Equipo: __ Marca: __ Falla: __')}" target="_blank" rel="noopener">{WA_SVG}<span>Escribir por WhatsApp</span></a><a class="btn linea cl" href="tel:{PHONE_TEL}">Llamar {PHONE_TXT}</a></div><ul class="pts"><li>Servicio a domicilio en Cali</li><li>Casa, gimnasios y condominios</li><li>Te explicamos la falla antes de reparar</li></ul></div></div></section>'''
    body=f'''<section class="sec"><div class="wrap"><h2>Servicios de reparación y mantenimiento</h2><p class="sub">Reparamos todo lo que tenga que ver con equipos de gimnasio en Cali.</p><div class="svcs">{cards}</div></div></section>
<section class="sec"><div class="wrap"><h2>Equipos que atendemos</h2><p class="sub">Caminadoras, bicicletas de spinning, multifuncionales y elípticas, de casa y de gimnasio.</p><div class="gal g3">{HG}</div><p class="refimg">Imágenes de referencia.</p></div></section>
<section class="sec osc"><div class="wrap"><h2>Lo que más se busca en Cali</h2><p class="sub">Técnicos de equipos de gimnasio en toda la ciudad, a domicilio.</p><div class="chips">{cali_chips}</div></div></section>
<section class="sec" id="servicios"><div class="wrap"><h2>Todos nuestros servicios</h2><p class="sub">Cada servicio tiene su página con qué incluye y cómo pedirlo.</p><div class="chips">{svc2}</div></div></section>
<section class="sec"><div class="wrap"><h2>Marcas que atendemos</h2><p class="sub">Servicio técnico independiente para estas y otras marcas.</p><div class="chips">{mchips}</div><p style="margin-top:22px"><a class="enlace" href="{url(s,'marcas')}">Ver las marcas →</a></p></div></section>
<section class="sec osc"><div class="wrap"><h2>Equipos que reparamos</h2><p class="sub">Casi cualquier equipo que uses para hacer ejercicio en casa o en el gimnasio.</p><div class="chips">{eqchips}</div><p style="margin-top:22px"><a class="enlace" href="{url(s,'equipos-que-reparamos')}">Ver todos los equipos →</a></p></div></section>
<section class="sec"><div class="wrap"><h2>¿Qué le pasa a tu equipo?</h2><p class="sub">Estas son las fallas por las que más nos escriben. Cada guía te dice qué revisar antes de llamar.</p><div class="chips">{fl}</div></div></section>
<section class="sec"><div class="wrap"><h2>Así te atendemos</h2><p class="sub">Vamos hasta donde está tu equipo, lo revisamos y lo reparamos.</p><div class="tecs">{TECS}</div><p class="refimg">Imágenes ilustrativas.</p></div></section>
<section class="sec osc"><div class="wrap"><h2>Cómo trabajamos</h2><ol class="pasos">{ps}</ol><p style="margin-top:22px"><a class="enlace" href="{url(s,'como-trabajamos')}">Ver el proceso completo paso a paso →</a></p></div></section>
<section class="sec"><div class="wrap"><h2>Guías para entender y revisar tu equipo</h2><p class="sub">Explicaciones paso a paso de las fallas más comunes.</p><div class="cards g2">{gcards}</div><p style="margin-top:22px"><a class="enlace" href="{url(s,'guias')}">Ver todas las guías →</a></p></div></section>
<section class="sec osc"><div class="wrap"><h2>Para quién es el servicio</h2><div class="qs">{qs}</div></div></section>
<section class="sec"><div class="wrap"><h2>Atendemos en toda Cali</h2><p class="sub">Sur, norte, oeste, centro y oriente. Algunas de las zonas desde donde nos escriben:</p><div class="zonas">{zh}</div><p><a class="enlace" href="{url(s,'zonas-de-servicio-cali')}">Ver todas las zonas →</a></p></div></section>
<section class="sec"><div class="wrap lay1">{faq_html(faq)}</div></section>
<section class="final"><div class="wrap"><div class="logobig">{LOGOBIG}</div><h2>¿Tu equipo está fallando?</h2><p>Escríbenos por WhatsApp con la marca, el modelo y la falla. Te orientamos y coordinamos la revisión en Cali.</p><a class="btn wa grande" href="{wa('Hola Técnico Gym, necesito una revisión de un equipo de gimnasio en Cali.')}" target="_blank" rel="noopener">{WA_SVG}<span>Escribir por WhatsApp</span></a></div></section>'''
    write('',head('','Técnico Gym Cali: Reparación de Caminadoras y Gimnasio','Reparación de caminadoras, bicicletas de spinning, elípticas y multifuncionales en Cali. Servicio a domicilio y mantenimiento para gimnasios. 321 799 6144.',ld)+header('')+hero+body+footer(''))
home()
# ---- archivos técnicos ----
urls=['']+[x for x in ['guias','servicios','marcas','equipos-que-reparamos','como-trabajamos','zonas-de-servicio-cali','preguntas-frecuentes','contacto','privacidad']+EQUIPOS+SERVICIOS+SERV_NUEVOS+MARCAS+ZS+GUIAS_ALL if x]
urls=list(dict.fromkeys(urls))
sm='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{SITE}/{u+"/" if u else ""}</loc><lastmod>{TODAY}</lastmod></url>' for u in urls)+'</urlset>'
open(os.path.join(OUT,'sitemap.xml'),'w').write(sm)
open(os.path.join(OUT,'robots.txt'),'w').write(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
RED=''
if os.path.exists('redirects.txt'):
    for l in open('redirects.txt',encoding='utf-8'):
        p_=l.split()
        if len(p_)==2 and p_[0].startswith('/'): RED+=f'Redirect 301 {p_[0]} {p_[1]}\n'
open(os.path.join(OUT,'.htaccess'),'w').write(RED+'''ErrorDocument 404 /404/
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
RewriteCond %{HTTP_HOST} ^www\\.(.+)$ [NC]
RewriteRule ^ https://%1%{REQUEST_URI} [L,R=301]
<IfModule mod_deflate.c>
AddOutputFilterByType DEFLATE text/html text/css application/javascript image/svg+xml application/xml
</IfModule>
<IfModule mod_expires.c>
ExpiresActive On
ExpiresByType text/css "access plus 30 days"
ExpiresByType image/png "access plus 30 days"
ExpiresByType image/svg+xml "access plus 30 days"
</IfModule>
''')
shutil.copy('estilo.css',os.path.join(OUT,'estilo.css'))
for f in os.listdir('assets'): shutil.copy(os.path.join('assets',f),os.path.join(OUT,f))
shutil.copytree('img',os.path.join(OUT,'img'))
if os.path.isdir('gsc-files'):
    for f in os.listdir('gsc-files'): shutil.copy(os.path.join('gsc-files',f),os.path.join(OUT,f))
print('páginas html:',sum(1 for r,d,f in os.walk(OUT) for x in f if x=='index.html'))
