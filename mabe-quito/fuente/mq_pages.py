# -*- coding: utf-8 -*-
import re,html
from mq_base import *
from mq_eq2 import EQ
import mq_eq
from mq_zonas import Z,ZD,ZSLUGS,ZXA,AXZ,TIPO_TXT,SECTOR_TXT
import mq_terms2
import mq_terms3
from mq_terms import T
import mq_guias
E=html.escape
PAGES={}; ORDER=[]
URG={'Urgente':'u','Revisar pronto':'r','Vigilar':'v'}
def cap(s): return s[:1].upper()+s[1:]
def low1(s): return s[:1].lower()+s[1:]
def clip(s,n):
    if len(s)<=n: return s
    c=s[:n].rsplit(' ',1)[0].rstrip(',;:. ')
    return c+'.' if not c.endswith('.') else c
def mktitle(core,suf=None):
    if 'servicio técnico mabe quito' in core.lower(): return core
    for s_ in ([suf] if suf else [' | Servicio Técnico Mabe Quito',' | Mabe Quito']):
        if len(core)+len(s_)<=65: return core+s_
    return core
KW=' Servicio técnico Mabe Quito.'
def addp(slug,**d):
    if 'desc' in d and 'servicio técnico mabe quito' not in d['desc'].lower():
        b=clip(d['desc'].rstrip(),160-len(KW)); d['desc']=(b if b.endswith('.') else b+'.')+KW
    d['slug']=slug; PAGES[slug]=d; ORDER.append(slug)
def ul(items): return '<ul>'+''.join(f'<li>{x}</li>' for x in items)+'</ul>'
def wam(txt): return txt
EQK=list(EQ.keys())
SUBJ={'refrigeradoras':('nevera','refrigeradora'),'hornos':('horno',),'centros-de-lavado':('torre',),'congeladores':('congelador',),'lavadoras':('lavadora',),'secadoras':('secadora',),'microondas':('microondas',),'lavavajillas':('lavavajillas',),'campanas-extractoras':('campana',)}
def fault_h1(k,name):
    e=EQ[k]; n=low1(name.strip())
    for s in SUBJ.get(k,()):
        m=re.match(r'^(el|la|un|una) '+s+r'\s+',n)
        if m: n=n[m.end():]
    h=f"{cap(e['sing'])} Mabe: {n}"
    if len(h)+9>58:
        n2=re.split(r',| o ',n)[0].strip()
        h=f"{cap(e['sing'])} Mabe: {n2}"
    return h
FAULTS={}   # slug -> (k,i)
for k in EQK:
    for i,s in enumerate(EQ[k]['slugs']): FAULTS[s]=(k,i)
MERGE={'nevera-mabe-no-enfria-quito':'refrigeradora-mabe-no-enfria-quito','nevera-mabe-escarcha-congelador-quito':'refrigeradora-mabe-escarcha-en-el-congelador-quito','nevera-mabe-hace-ruido-quito':'refrigeradora-mabe-hace-ruido-quito','nevera-mabe-gotea-agua-quito':'refrigeradora-mabe-gotea-agua-por-dentro-quito','nevera-mabe-no-hace-hielo-quito':'refrigeradora-mabe-no-hace-hielo-quito','lavadora-mabe-no-centrifuga-quito':'lavadora-mabe-no-centrifuga-quito','lavadora-mabe-no-desagua-quito':'lavadora-mabe-no-desagua-quito','lavadora-mabe-gotea-agua-quito':'lavadora-mabe-gotea-o-bota-agua-quito','secadora-mabe-no-seca-quito':'secadora-mabe-no-seca-la-ropa-quito','secadora-mabe-no-calienta-quito':'secadora-mabe-no-calienta-quito','secadora-mabe-tarda-en-secar-quito':'secadora-mabe-tarda-demasiado-en-secar-quito'}
MERGED={}
for (s_,t_,eq_,d_,sec_) in mq_eq.BLOG_SRC:
    if s_ in MERGE: MERGED[MERGE[s_]]=(t_,sec_)
GUIDES=[(s,t,{'neveras':'refrigeradoras'}.get(eq,eq),d,sec) for (s,t,eq,d,sec) in mq_eq.BLOG_SRC if s not in MERGE]+[(s,t,eq,d,sec) for (s,t,eq,d,sec) in mq_guias.G]
GEQ={}
for g in GUIDES: GEQ.setdefault(g[2],[]).append(g[0])
TERMS={t['slug']:t for t in T}
TEQ={}
for t in T:
    for k in t['eq']: TEQ.setdefault(k,[]).append(t['slug'])
# ---------- electrodomésticos ----------
for k in EQK:
    e=EQ[k]; faultlinks=[]
    fl='<ul class="fallas">'+''.join(f'<li><a href="@{e["slugs"][i]}@">{E(f[0])}</a> <span class="tag {URG[f[2]]}">{f[2]}</span><br><span class="cz">{E(f[1])}</span></li>' for i,f in enumerate(e['fallas']))+'</ul>'
    sec=[('Modelos y tipos que atendemos',ul([E(m) for m in e['modelos']])),
     (f'Fallas más comunes en {e["art"].split(" ",1)[1]} Mabe',fl),
     ('Qué hacemos en la visita',f'<p>Vamos a tu casa, probamos {e["art"]} en su lugar de uso, identificamos la causa y te explicamos qué tiene antes de tocar nada.</p>'+ul(['Diagnóstico de la falla','Costo confirmado antes de reparar','Reparación y prueba de funcionamiento','Recomendaciones para que no se repita'])),
     (f'Mantenimiento para que {e["art"]} dure más',ul([E(m) for m in e['mant']])),
     ('Seguridad primero',f'<p>{E(e["seguridad"])}</p>'),
     ('Qué enviarnos por WhatsApp',f'<p>Para orientarte más rápido, envíanos {E(e["datos"])}. Una foto de la etiqueta y un video corto de la falla ayudan mucho.</p>'),
     ('Particularidades de Quito',f'<p>{E(e["quito"])}</p>')]
    if k in AXZ:
        chips=''.join(f'<a href="@{"reparacion-de-"+k+"-mabe-en-"+z}@">{E(ZD[z]["nombre"])}</a>' for z in ZXA)
        sec.append((f'{cap(e["corto"])} Mabe en tu zona de Quito',f'<p>Elige tu sector para ver la información de servicio a domicilio:</p><div class="chips">{chips}</div>'))
    tl=TEQ.get(k,[])
    if tl: sec.append(('Búsquedas relacionadas',f'<div class="chips">'+''.join(f'<a href="@{x}@">{E(TERMS[x]["h1"])}</a>' for x in tl)+'</div>'))
    rel=[EQ[x]['slug'] for x in EQK if x!=k][:6]
    addp(e['slug'],kind='service',h1=e['h1'],title=mktitle(e['h1']),desc=clip(f"{e['h1']}: {e['intro']} Visita a domicilio. WhatsApp {PHONE_TXT}.",160),lead=e['intro'],sections=sec,faq=e['faq'],related=rel,
         wamsg=f"Hola, necesito servicio técnico para {e['art']} Mabe en Quito.",icon=e['icon'],th=e['th'],photos=e['foto'],tec=None,eq=k)
# ---------- fallas ----------
GUIDEFOR={k:GEQ.get(k,[]) for k in EQK}
for k in EQK:
    e=EQ[k]
    for i,f in enumerate(e['fallas']):
        name,causas,urg,tip=f[0],f[1],f[2],f[3]; slug=e['slugs'][i]
        h1=fault_h1(k,name); core=h1+' en Quito'
        if urg=='Urgente': cuando='No lo dejes pasar: este tipo de falla puede dañar el equipo, causar una fuga o representar un riesgo. Deja de usarlo, sigue las indicaciones de seguridad y escríbenos para coordinar la revisión.'
        elif urg=='Revisar pronto': cuando='Conviene que lo revise un técnico en los próximos días. Si sigues usándolo con la falla, el problema puede crecer y la reparación salir más cara.'
        else: cuando='Puedes observarlo unos días mientras haces las revisiones de arriba. Si empeora, reaparece o se suma otro síntoma, pide una revisión.'
        sib=[x for j,x in enumerate(e['slugs']) if j!=i]
        sec=[('Qué suele estar pasando',f'<p>{E(causas)}</p><p>Nivel de atención: <span class="tag {URG[urg]}">{urg}</span></p>'),
             ('Qué puedes revisar tú',f'<p>{E(tip)}</p><p>{E(e["seguridad"])}</p>'),
             ('Cuándo llamar al técnico',f'<p>{cuando}</p>'),
             ('Qué hacemos en la visita',ul(['Probamos el equipo y reproducimos la falla','Identificamos la pieza o el sistema que la causa','Te explicamos el diagnóstico y el costo antes de reparar','Reparamos y probamos que quede funcionando'])),
             ('Datos que nos ayudan por WhatsApp',f'<p>Envíanos {E(e["datos"])}. Si la falla hace ruido, huele o muestra un código, grábala en un video corto.</p>'),
             *([('Guía detallada',''.join(f'<h3>{E(h_)}</h3>{b_}' for h_,b_ in MERGED[slug][1]))] if slug in MERGED else []),
             ('Particularidades de Quito',f'<p>{E(e["quito"])}</p>'),
             (f'Otras fallas de {e["art"].split(" ",1)[1]} Mabe',ul([f'<a href="@{x}@">{E(fault_h1(k,e["fallas"][j][0]))}</a>' for j,x in enumerate(e["slugs"]) if j!=i]))]
        resp=('No lo recomendamos hasta revisarlo.' if urg=='Urgente' else 'Puedes usarlo con precaución, pero conviene revisarlo pronto.' if urg=='Revisar pronto' else 'Normalmente sí, observando si empeora.')
        faq=[(f'¿Puedo seguir usando {e["art"]} Mabe mientras tanto?',resp),
             ('¿El técnico lo repara en mi casa en Quito?','Sí. Vamos a tu domicilio, diagnosticamos la falla y te damos el costo antes de reparar. Escríbenos por WhatsApp para coordinar.'),
             ('¿Qué debo enviarte para que me orientes?',f'Marca y modelo, una descripción de la falla, tu barrio y, si puedes, una foto de la etiqueta y un video corto del problema.')]
        rel=[e['slug']]+sib[:3]+GUIDEFOR[k][:2]
        addp(slug,kind='falla',h1=h1,title=mktitle(core),desc=clip(f"{core}: causas más comunes, qué revisar antes de llamar y cuándo pedir un técnico. Visita a domicilio. WhatsApp {PHONE_TXT}.",160),
             lead=f'Causas habituales: {low1(causas)}',sections=sec,faq=faq,related=rel,wamsg=f"Hola, mi {e['sing']} Mabe presenta esta falla: {low1(name)}. Estoy en Quito.",icon=e['icon'],th=e['th'],photos=[],tec=None,eq=k,fk=(k,i))
# ---------- zonas ----------
for z in Z:
    zs,zn,sec_,tipo,refs=z; sector=SECTOR_TXT[sec_]
    h1=f'Servicio técnico Mabe Quito: {zn}'
    eqchips=''.join(f'<a href="@{EQ[k]["slug"]}@">{E(EQ[k]["corto"])}</a>' for k in EQK)
    s=[('Cobertura en '+zn,f'<p>Atendemos {zn} y sus alrededores, en el {sector}. Algunas referencias de la zona:</p><div class="zonas">'+''.join(f'<span>{E(r)}</span>' for r in refs)+'</div>'),
       ('Cómo es la visita en esta zona',f'<p>{TIPO_TXT[tipo]}</p>'),
       ('Equipos Mabe que revisamos',f'<p>Visitamos {zn} para reparar y dar mantenimiento a estos electrodomésticos:</p><div class="chips">{eqchips}</div>')]
    if zs in ZXA:
        s.append((f'Reparación por equipo en {zn}','<div class="chips">'+''.join(f'<a href="@reparacion-de-{k}-mabe-en-{zs}@">{E(EQ[k]["corto"])} en {E(zn)}</a>' for k in AXZ)+'</div>'))
    near=[ZD[x] for x in ZSLUGS if ZD[x]['sector']==sec_ and x!=zs][:8]
    s.append(('Zonas cercanas',f'<div class="chips">'+''.join(f'<a href="@servicio-tecnico-mabe-en-{d["slug"]}@">{E(d["nombre"])}</a>' for d in near)+'</div>'))
    faq=[(f'¿Atienden en {zn}?',f'Sí. Escríbenos tu dirección y una referencia por WhatsApp y coordinamos la visita en {zn}.'),
         (f'¿Qué equipos Mabe reparan en {zn}?','Refrigeradoras, congeladores, lavadoras, secadoras, centros de lavado, cocinas, hornos, parrillas, campanas, microondas y lavavajillas.'),
         ('¿Cuánto cuesta la visita?',f'Escríbenos con el equipo, el modelo y la falla; te confirmamos el costo de la visita antes de ir.')]
    addp(zs and 'servicio-tecnico-mabe-en-'+zs,kind='zona',h1=h1,title=mktitle(f'Servicio técnico Mabe Quito: {zn}'),desc=clip(f'Servicio técnico Mabe a domicilio en {zn}, {sector}: refrigeradoras, lavadoras, secadoras, cocinas y hornos. Escríbenos por WhatsApp {PHONE_TXT}.',160),
         lead=f'Técnico a domicilio para electrodomésticos Mabe en {zn}, {sector}. Diagnóstico claro y costo antes de reparar.',sections=s,faq=faq,
         related=[EQ[k]['slug'] for k in ('refrigeradoras','lavadoras','secadoras','cocinas')],wamsg=f'Hola, necesito servicio técnico Mabe en {zn}, Quito.',icon='pin',th='',photos=[],tec=None,zone=zs)
# ---------- zona x equipo ----------
for zi,zs in enumerate(ZXA):
    d=ZD[zs]; zn=d['nombre']
    for k in AXZ:
        e=EQ[k]; n=len(e['fallas']); idx=[(zi*2+j)%n for j in range(4)]
        fl='<ul class="fallas">'+''.join(f'<li><a href="@{e["slugs"][i]}@">{E(e["fallas"][i][0])}</a> <span class="tag {URG[e["fallas"][i][2]]}">{e["fallas"][i][2]}</span><br><span class="cz">{E(e["fallas"][i][1])}</span></li>' for i in idx)+'</ul>'
        h1=f'Reparación de {low1(e["corto"])} Mabe en {zn}'; slug=f'reparacion-de-{k}-mabe-en-{zs}'
        s=[(f'Servicio a domicilio en {zn}',f'<p>Reparamos {low1(e["corto"])} Mabe en {zn}, {SECTOR_TXT[d["sector"]]}. {TIPO_TXT[d["tipo"]]}</p>'),
           (f'Fallas que más nos consultan en {zn}',fl),
           ('Qué hacemos en la visita',ul(['Revisamos el equipo en su lugar de uso','Te explicamos la causa de la falla','Confirmamos el costo antes de reparar','Reparamos y probamos el funcionamiento'])),
           (f'Particularidades de Quito para {low1(e["corto"])}',f'<p>{E(e["quito"])}</p>'),
           ('Referencias de la zona','<div class="zonas">'+''.join(f'<span>{E(r)}</span>' for r in d['refs'])+'</div>'),
           ('Cómo pedir la visita',f'<p>Escríbenos por WhatsApp con la marca y el modelo, qué falla presenta, tu dirección en {zn} y una foto de la etiqueta. Te respondemos con el siguiente paso.</p>')]
        faq=[(f'¿Reparan {low1(e["corto"])} Mabe en {zn}?',f'Sí, atendemos {zn} y sus alrededores. Escríbenos tu dirección y coordinamos.'),
             (f'¿Qué falla es la más común en {low1(e["corto"])}?',f'Entre las que más nos consultan: {low1(e["fallas"][idx[0]][0])}, {low1(e["fallas"][idx[1]][0])} y {low1(e["fallas"][idx[2]][0])}.'),
             ('¿Dan el costo antes de reparar?','Sí. Primero diagnosticamos y te informamos el costo antes de continuar.')]
        others=[f'reparacion-de-{x}-mabe-en-{zs}' for x in AXZ if x!=k][:2]
        nz=ZXA[(zi+1)%len(ZXA)]
        addp(slug,kind='zxa',h1=h1,title=mktitle(f'{h1}, Quito'),desc=clip(f'{h1}: fallas frecuentes, visita a domicilio y costo antes de reparar. WhatsApp {PHONE_TXT}.',160),
             lead=f'Servicio técnico a domicilio para {low1(e["corto"])} Mabe en {zn}: diagnóstico claro y costo confirmado antes de reparar.',sections=s,faq=faq,
             related=[e['slug'],'servicio-tecnico-mabe-en-'+zs]+others+[f'reparacion-de-{k}-mabe-en-{nz}'],wamsg=f'Hola, necesito reparar {e["art"]} Mabe en {zn}, Quito.',icon=e['icon'],th=e['th'],photos=[],tec=None,zone=zs,eq=k)
# ---------- términos ----------
SECTOR_TERMS=['servicio-tecnico-mabe-quito-norte','servicio-tecnico-mabe-quito-centro','servicio-tecnico-mabe-quito-sur','servicio-tecnico-mabe-valle-de-los-chillos','servicio-tecnico-mabe-cumbaya-y-tumbaco']
for t in T:
    eqs=''.join(f'<a class="card" href="@{EQ[k]["slug"]}@"><div><b>{E(EQ[k]["h1"])}</b><span>{E(EQ[k]["intro"][:100])}…</span></div></a>' for k in t['eq'][:4])
    s=[('Qué incluye',ul([E(x) for x in t['inc']])),('Cuándo conviene',f'<p>{E(t["cuando"])}</p>'),
       ('Equipos relacionados',f'<div class="cards g2">{eqs}</div>'),
       ('Cómo pedir la visita',ul(['Escríbenos por WhatsApp o llámanos al '+PHONE_TXT,'Cuéntanos qué equipo es, la marca, el modelo y la falla','Envía tu barrio y, si puedes, una foto de la etiqueta y un video corto','Coordinamos el día y la hora de la visita'])),
       ('Dónde atendemos en Quito','<div class="chips">'+''.join(f'<a href="@{x}@">{E(TERMS[x]["h1"].replace("Servicio técnico Mabe en ","").replace("Servicio técnico Mabe ",""))}</a>' for x in SECTOR_TERMS if x!=t['slug'])+'<a href="@zonas-de-servicio-quito@">Ver todas las zonas</a></div>')]
    others=[x for x in TEQ.get(t['eq'][0],[]) if x!=t['slug']][:3]
    addp(t['slug'],kind='term',h1=t['h1'],title=mktitle(t['tit']),desc=clip(t['desc'],160),lead=t['intro'],sections=s,faq=t['faq']+[('¿Cómo contacto al servicio técnico?',f'Por WhatsApp o llamada al {PHONE_TXT} (+593 99 350 8191).')],
         related=[EQ[k]['slug'] for k in t['eq'][:3]]+others,wamsg=f'Hola, vi la página "{t["h1"]}". Necesito ayuda con un equipo Mabe en Quito.',icon=EQ[t['eq'][0]]['icon'],th=EQ[t['eq'][0]]['th'],photos=[],tec=None,eq=t['eq'][0])
# ---------- guías ----------
for (slug,tit,eq,desc,secs) in GUIDES:
    s=[(h,b) for h,b in secs]
    rel=[EQ[eq]['slug']]+[x for x in GEQ.get(eq,[]) if x!=slug][:3]
    addp(slug,kind='guia',h1=tit,title=mktitle(tit) if len(tit)<=50 else clip(tit,62),desc=clip(desc if len(desc)>=100 else desc+' Guía práctica para electrodomésticos Mabe en Quito, con pasos claros y cuándo pedir ayuda.',160),lead=desc,sections=s,faq=[('¿Puedo pedir ayuda por WhatsApp?',f'Sí. Escríbenos al {PHONE_TXT} con el modelo y la falla y te orientamos.')],related=rel,
         wamsg=f'Hola, leí la guía "{tit}" y necesito ayuda con mi equipo Mabe en Quito.',icon=EQ[eq]['icon'],th=EQ[eq]['th'],photos=[],tec=None,eq=eq)
GUIDE_SLUGS=[g[0] for g in GUIDES]
if __name__=='__main__':
    from collections import Counter
    print(len(PAGES),Counter(p['kind'] for p in PAGES.values()))
    bad=[(s,len(p['title'])) for s,p in PAGES.items() if len(p['title'])>65]; print('títulos largos',bad[:10],len(bad))
    sl=[s for s in PAGES if '/' in s]; print(sl)
