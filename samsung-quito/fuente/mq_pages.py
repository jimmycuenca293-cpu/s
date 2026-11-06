# -*- coding: utf-8 -*-
import re,html
from mq_base import *
from mq_eq2 import EQ
import mq_eq
from mq_zonas import Z,ZD,ZSLUGS,ZXA,AXZ,TIPO_TXT,SECTOR_TXT
import mq_terms2
import mq_terms3
import mq_terms4
import mq_terms5
from mq_terms import T
import mq_guias
E=html.escape
PAGES={}; ORDER=[]
REPF={'refrigeradoras':['rep-filtro-agua','rep-filtro-agua-2'],'lavadoras':['rep-bomba','rep-bomba-2','rep-filtro-pelusa'],'secadoras':['rep-filtro-secadora','rep-filtro-pelusa-2'],'centros-de-lavado':['rep-bomba-2','rep-filtro-pelusa']}
URG={'Urgente':'u','Revisar pronto':'r','Vigilar':'v'}
def cap(s): return s[:1].upper()+s[1:]
def low1(s): return s[:1].lower()+s[1:]
def clip(s,n):
    if len(s)<=n: return s
    c=s[:n].rsplit(' ',1)[0].rstrip(',;:. ')
    return c+'.' if not c.endswith('.') else c
def mktitle(core,suf=None):
    if len(core)>65: core=core[:62].rsplit(' ',1)[0]
    if 'servicio técnico samsung quito' in core.lower(): return core
    for s_ in ([suf] if suf else [' | Servicio Técnico Samsung Quito',' | Samsung Quito']):
        if len(core)+len(s_)<=65: return core+s_
    return core
KW=' Servicio técnico Samsung Quito.'
def addp(slug,**d):
    if 'desc' in d and 'servicio técnico samsung quito' not in d['desc'].lower():
        b=clip(d['desc'].rstrip(),160-len(KW)); d['desc']=(b if b.endswith('.') else b+'.')+KW
    d['slug']=slug; PAGES[slug]=d; ORDER.append(slug)
def ul(items): return '<ul>'+''.join(f'<li>{x}</li>' for x in items)+'</ul>'
def wam(txt): return txt
EQK=list(EQ.keys())
EQK_UI=[k for k in EQK if not EQ[k].get('alias')]
SUBJ={'refrigeradoras':('nevera','refrigeradora'),'hornos':('horno',),'centros-de-lavado':('torre',),'congeladores':('congelador',),'lavadoras':('lavadora',),'secadoras':('secadora',),'microondas':('microondas',),'lavavajillas':('lavavajillas',),'campanas-extractoras':('campana',)}
def fault_h1(k,name):
    e=EQ[k]; n=low1(name.strip())
    for s in SUBJ.get(k,()):
        m=re.match(r'^(el|la|un|una) '+s+r'\s+',n)
        if m: n=n[m.end():]
    h=f"{cap(e['sing'])} Samsung: {n}"
    if len(h)+9>58:
        n2=re.split(r',| o ',n)[0].strip()
        h=f"{cap(e['sing'])} Samsung: {n2}"
    return h
FAULTS={}   # slug -> (k,i)
for k in EQK:
    if EQ[k].get('alias'): continue
    for i,s in enumerate(EQ[k]['slugs']): FAULTS[s]=(k,i)
MERGE={'nevera-samsung-no-enfria-quito':'refrigeradora-samsung-no-enfria-quito','nevera-samsung-escarcha-congelador-quito':'refrigeradora-samsung-escarcha-en-el-congelador-quito','nevera-samsung-hace-ruido-quito':'refrigeradora-samsung-hace-ruido-quito','nevera-samsung-gotea-agua-quito':'refrigeradora-samsung-gotea-agua-por-dentro-quito','nevera-samsung-no-hace-hielo-quito':'refrigeradora-samsung-no-hace-hielo-quito','nevera-samsung-family-hub-pantalla-no-funciona-quito':'refrigeradora-samsung-family-hub-pantalla-no-funciona-quito','nevera-samsung-digital-inverter-ruido-quito':'refrigeradora-samsung-digital-inverter-ruido-quito','nevera-samsung-dispensador-agua-hielo-no-funciona-quito':'dispensador-de-agua-de-refrigeradora-samsung-no-funciona-quito','lavadora-samsung-no-centrifuga-quito':'lavadora-samsung-no-centrifuga-quito','lavadora-samsung-no-desagua-quito':'lavadora-samsung-no-desagua-quito','lavadora-samsung-gotea-agua-quito':'lavadora-samsung-gotea-o-bota-agua-quito','lavadora-samsung-codigo-5e-no-desagua-quito':'lavadora-samsung-codigo-5e-o-se-no-desagua-quito','lavadora-samsung-codigo-4e-no-entra-agua-quito':'lavadora-samsung-codigo-4e-no-entra-agua-quito','lavadora-samsung-addwash-ecobubble-fallas-quito':'lavadora-samsung-addwash-gotea-quito','lavadora-samsung-smartthings-no-conecta-quito':'lavadora-samsung-no-conecta-a-smartthings-quito','lavadora-samsung-codigo-ue-vibra-quito':'lavadora-samsung-codigo-ue-vibra-mucho-quito','lavadora-samsung-codigo-dc-de-puerta-quito':'lavadora-samsung-puerta-no-abre-o-no-cierra-quito','secadora-samsung-no-seca-quito':'secadora-samsung-no-seca-la-ropa-quito','secadora-samsung-no-calienta-quito':'secadora-samsung-no-calienta-quito','secadora-samsung-tarda-en-secar-quito':'secadora-samsung-tarda-demasiado-en-secar-quito','secadora-samsung-no-seca-ciclo-largo-quito':'secadora-samsung-ciclo-largo-ducto-o-filtro-saturado-quito'}
MERGED={}
for (s_,t_,eq_,d_,sec_) in mq_eq.BLOG_SRC:
    if s_ in MERGE: MERGED[MERGE[s_]]=(t_,sec_)
GUIDES=[(s,t,{'neveras':'refrigeradoras'}.get(eq,eq),d,sec) for (s,t,eq,d,sec) in mq_eq.BLOG_SRC if s not in MERGE]+[(s,t,eq,d,sec) for (s,t,eq,d,sec) in mq_guias.G]
GUIDES=[g for g in GUIDES if g[2] in EQ]
GEQ={}
for g in GUIDES: GEQ.setdefault(g[2],[]).append(g[0])
SECT_OUT=['servicio-tecnico-samsung-quito-norte','servicio-tecnico-samsung-quito-centro','servicio-tecnico-samsung-quito-sur']
T[:]=[t for t in T if t['slug'] not in SECT_OUT]
GEN=['tecnico-samsung-a-domicilio-quito','servicio-tecnico-samsung-cerca-de-mi-quito','reparacion-de-electrodomesticos-samsung-a-domicilio-quito','servicio-tecnico-de-electrodomesticos-quito','tecnico-de-electrodomesticos-a-domicilio-quito','mantenimiento-preventivo-de-electrodomesticos-samsung-quito','instalacion-de-electrodomesticos-samsung-quito','diagnostico-de-electrodomesticos-samsung-quito','reparacion-de-tarjetas-electronicas-de-electrodomesticos-samsung-quito','repuestos-para-electrodomesticos-samsung-quito','servicio-tecnico-samsung-edificios-y-conjuntos-quito','centro-de-servicio-samsung-quito','servicio-tecnico-samsung-telefono-y-whatsapp-quito','revision-de-electrodomesticos-samsung-usados-antes-de-comprar-quito','emergencias-de-electrodomesticos-samsung-fugas-de-agua-y-gas-quito','reparar-electrodomesticos-samsung-quito','donde-reparar-electrodomesticos-samsung-quito','samsung-quito-servicio-tecnico-y-reparacion','electrodomestico-samsung-no-funciona-que-hacer-en-quito']
VALLE_TERMS=['servicio-tecnico-samsung-valle-de-los-chillos','servicio-tecnico-samsung-cumbaya-y-tumbaco']
SECTOR_HUBS={'Norte':('servicio-tecnico-samsung-quito-norte','norte de Quito'),'Centro':('servicio-tecnico-samsung-quito-centro','centro de Quito'),'Sur':('servicio-tecnico-samsung-quito-sur','sur de Quito'),'Valles':('servicio-tecnico-samsung-valles-de-quito','valles de Quito')}
REM=('cocina','horno','parrilla','campana','congelador','microondas','lavavajillas','gas-quito','a-gas')
T[:]=[t for t in T if not any(r in t['slug'] for r in REM)]
for _t in T:
    _t['eq']=[k for k in _t['eq'] if k in EQ]
    if 'nevera' in _t['slug'] and 'neveras' in EQ: _t['eq']=['neveras']
T[:]=[t for t in T if t['eq']]
TERMS={t['slug']:t for t in T}
TEQ={}
for t in T:
    for k in t['eq']: TEQ.setdefault(k,[]).append(t['slug'])
# ---------- electrodomésticos ----------
def _ord(s):
    for n,pre in enumerate(('reparar-','donde-reparar-','cuanto-cuesta-','arreglo','tecnico','reparacion','mantenimiento','instalacion')):
        if s.startswith(pre): return n
    return 9
TPRIM={k:sorted([t['slug'] for t in T if t['slug'] not in GEN and t['slug'] not in VALLE_TERMS and t['eq'][0]==k],key=lambda s:(_ord(s),s)) for k in EQK}
for k in EQK:
    e=EQ[k]; nm=e["art"].split(" ",1)[1]
    fl='<ul class="fallas">'+''.join(f'<li><a href="@{e["slugs"][i]}@">{E(f[0])}</a> <span class="tag {URG[f[2]]}">{f[2]}</span><br><span class="cz">{E(f[1])}</span></li>' for i,f in enumerate(e['fallas']))+'</ul>'
    sv='<ul class="sublist">'+''.join(f'<li><a href="@{x}@">{E(TERMS[x]["h1"])}</a></li>' for x in TPRIM[k])+'</ul>' if TPRIM[k] else ''
    sec=[('Qué reparamos',f'<p>Modelos y tipos de {nm} Samsung que atendemos a domicilio en Quito:</p>'+ul([E(m) for m in e['modelos']])),
     (f'Fallas comunes de {nm} Samsung',f'<p>Cada falla tiene su propia página con causas, qué revisar y cuándo llamar.</p>{fl}')]
    if sv: sec.append((f'Servicios para {nm} Samsung en Quito',f'<p>Reparar, dónde reparar, cuánto cuesta y más:</p>{sv}'))
    sec+=[('Qué hacemos en la visita',f'<p>Vamos a tu casa, probamos {e["art"]} en su lugar de uso, identificamos la causa y te explicamos qué tiene antes de tocar nada.</p>'+ul(['Diagnóstico de la falla','Costo confirmado antes de reparar','Reparación y prueba de funcionamiento','Recomendaciones para que no se repita'])),
     (f'Mantenimiento para que {e["art"]} dure más',ul([E(m) for m in e['mant']])),
     ('Antes de llamar: seguridad y datos',f'<h3>Seguridad primero</h3><p>{E(e["seguridad"])}</p><h3>Qué enviarnos por WhatsApp</h3><p>Para orientarte más rápido, envíanos {E(e["datos"])}. Una foto de la etiqueta y un video corto de la falla ayudan mucho.</p>'),
     ('Particularidades de Quito',f'<p>{E(e["quito"])}</p>')]
    if k in AXZ:
        body='<p>Elige tu barrio para ver el servicio a domicilio de '+nm+' Samsung en tu zona:</p>'
        for sc,lab in (('Norte','Norte de Quito'),('Centro','Centro de Quito'),('Sur','Sur de Quito'),('Valles','Valles de Quito')):
            zs_=[z for z in ZXA if ZD[z]['sector']==sc]
            if zs_: body+=f'<h3>{lab}</h3><div class="chips">'+''.join(f'<a href="@reparacion-de-{k}-samsung-en-{z}@">{E(ZD[z]["nombre"])}</a>' for z in zs_)+'</div>'
        sec.append((f'Dónde atendemos: {nm} Samsung por zona',body))
    gl=GEQ.get('refrigeradoras' if e.get('alias') else k,[])
    if k=='refrigeradoras': gl=gl+GEQ.get('neveras',[])
    if gl: sec.append(('Guías relacionadas','<ul class="sublist">'+''.join(f'<li><a href="@{x}@">{E(next(g[1] for g in GUIDES if g[0]==x))}</a></li>' for x in gl[:8])+'</ul>'))
    rel=[EQ[x]['slug'] for x in EQK if x!=k][:6]
    addp(e['slug'],kind='service',h1=e['h1'],title=mktitle(e['h1']),desc=clip(f"{e['h1']}: {e['intro']} Visita a domicilio. WhatsApp {PHONE_TXT}.",160),lead=e['intro'],sections=sec,faq=e['faq'],related=rel,
         wamsg=f"Hola, necesito servicio técnico para {e['art']} Samsung en Quito.",icon=e['icon'],th=e['th'],photos=e['foto'],tec=None,eq=k)
# ---------- fallas ----------
GUIDEFOR={k:GEQ.get(k,[]) for k in EQK}
for k in EQK:
    if EQ[k].get('alias'): continue
    e=EQ[k]
    for i,f in enumerate(e['fallas']):
        name,causas,urg,tip=f[0],f[1],f[2],f[3]; slug=e['slugs'][i]
        h1=fault_h1(k,name); core=h1+' en Quito'
        if k=='refrigeradoras': core=core.replace('Refrigeradora Samsung:','Nevera o refrigeradora Samsung:',1)
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
             (f'Otras fallas de {e["art"].split(" ",1)[1]} Samsung',ul([f'<a href="@{x}@">{E(fault_h1(k,e["fallas"][j][0]))}</a>' for j,x in enumerate(e["slugs"]) if j!=i]))]
        resp=('No lo recomendamos hasta revisarlo.' if urg=='Urgente' else 'Puedes usarlo con precaución, pero conviene revisarlo pronto.' if urg=='Revisar pronto' else 'Normalmente sí, observando si empeora.')
        faq=[(f'¿Puedo seguir usando {e["art"]} Samsung mientras tanto?',resp),
             ('¿El técnico lo repara en mi casa en Quito?','Sí. Vamos a tu domicilio, diagnosticamos la falla y te damos el costo antes de reparar. Escríbenos por WhatsApp para coordinar.'),
             ('¿Qué debo enviarte para que me orientes?',f'Marca y modelo, una descripción de la falla, tu barrio y, si puedes, una foto de la etiqueta y un video corto del problema.')]
        rel=[e['slug']]+sib[:3]+GUIDEFOR[k][:2]
        addp(slug,kind='falla',h1=h1,title=mktitle(core),desc=clip(f"{core}: causas más comunes, qué revisar antes de llamar y cuándo pedir un técnico. Visita a domicilio. WhatsApp {PHONE_TXT}.",160),
             lead=f'Causas habituales: {low1(causas)}',sections=sec,faq=faq,related=rel,wamsg=f"Hola, mi {e['sing']} Samsung presenta esta falla: {low1(name)}. Estoy en Quito.",icon=e['icon'],th=e['th'],photos=[],tec=None,eq=k,fk=(k,i))
# ---------- zonas ----------
for z in Z:
    zs,zn,sec_,tipo,refs=z; sector=SECTOR_TXT[sec_]
    h1=f'Servicio técnico Samsung Quito: {zn}'
    eqchips=''.join(f'<a href="@{EQ[k]["slug"]}@">{E(EQ[k]["corto"])}</a>' for k in EQK)
    s=[('Cobertura en '+zn,f'<p>Atendemos {zn} y sus alrededores, en el {sector}. Algunas referencias de la zona:</p><div class="zonas">'+''.join(f'<span>{E(r)}</span>' for r in refs)+'</div>'),
       ('Cómo es la visita en esta zona',f'<p>{TIPO_TXT[tipo]}</p>'),
       ('Equipos Samsung que revisamos',f'<p>Visitamos {zn} para reparar y dar mantenimiento a estos electrodomésticos:</p><div class="chips">{eqchips}</div>')]
    if zs in ZXA:
        s.append((f'Reparación por electrodoméstico en {zn}','<ul class="sublist">'+''.join(f'<li><a href="@reparacion-de-{k}-samsung-en-{zs}@">Reparación de {E(low1(EQ[k]["corto"]))} Samsung en {E(zn)}</a></li>' for k in AXZ)+'</ul>'))
    near=[ZD[x] for x in ZSLUGS if ZD[x]['sector']==sec_ and x!=zs][:8]
    s.append(('Zonas cercanas',f'<div class="chips">'+''.join(f'<a href="@servicio-tecnico-samsung-en-{d["slug"]}@">{E(d["nombre"])}</a>' for d in near)+'</div>'))
    faq=[(f'¿Atienden en {zn}?',f'Sí. Escríbenos tu dirección y una referencia por WhatsApp y coordinamos la visita en {zn}.'),
         (f'¿Qué equipos Samsung reparan en {zn}?','Refrigeradoras, neveras, lavadoras y secadoras.'),
         ('¿Cuánto cuesta la visita?',f'Escríbenos con el equipo, el modelo y la falla; te confirmamos el costo de la visita antes de ir.')]
    addp(zs and 'servicio-tecnico-samsung-en-'+zs,kind='zona',h1=h1,title=mktitle(f'Servicio técnico Samsung Quito: {zn}'),desc=clip(f'Servicio técnico Samsung a domicilio en {zn}, {sector}: refrigeradoras, neveras, lavadoras y secadoras. Escríbenos por WhatsApp {PHONE_TXT}.',160),
         lead=f'Técnico a domicilio para electrodomésticos Samsung en {zn}, {sector}. Diagnóstico claro y costo antes de reparar.',sections=s,faq=faq,
         related=[EQ[k]['slug'] for k in ('refrigeradoras','neveras','lavadoras','secadoras')],wamsg=f'Hola, necesito servicio técnico Samsung en {zn}, Quito.',icon='pin',th='',photos=[],tec=None,zone=zs)
# ---------- zona x equipo ----------
for zi,zs in enumerate(ZXA):
    d=ZD[zs]; zn=d['nombre']
    for k in AXZ:
        e=EQ[k]; n=len(e['fallas']); idx=[(zi*2+j)%n for j in range(4)]
        fl='<ul class="fallas">'+''.join(f'<li><a href="@{e["slugs"][i]}@">{E(e["fallas"][i][0])}</a> <span class="tag {URG[e["fallas"][i][2]]}">{e["fallas"][i][2]}</span><br><span class="cz">{E(e["fallas"][i][1])}</span></li>' for i in idx)+'</ul>'
        h1=f'Reparación de {low1(e["corto"])} Samsung en {zn}'; slug=f'reparacion-de-{k}-samsung-en-{zs}'
        s=[(f'Servicio a domicilio en {zn}',f'<p>Reparamos {low1(e["corto"])} Samsung en {zn}, {SECTOR_TXT[d["sector"]]}. {TIPO_TXT[d["tipo"]]}</p>'),
           (f'Fallas que más nos consultan en {zn}',fl),
           ('Qué hacemos en la visita',ul(['Revisamos el equipo en su lugar de uso','Te explicamos la causa de la falla','Confirmamos el costo antes de reparar','Reparamos y probamos el funcionamiento'])),
           (f'Particularidades de Quito para {low1(e["corto"])}',f'<p>{E(e["quito"])}</p>'),
           ('Referencias de la zona','<div class="zonas">'+''.join(f'<span>{E(r)}</span>' for r in d['refs'])+'</div>'),
           ('Cómo pedir la visita',f'<p>Escríbenos por WhatsApp con la marca y el modelo, qué falla presenta, tu dirección en {zn} y una foto de la etiqueta. Te respondemos con el siguiente paso.</p>')]
        faq=[(f'¿Reparan {low1(e["corto"])} Samsung en {zn}?',f'Sí, atendemos {zn} y sus alrededores. Escríbenos tu dirección y coordinamos.'),
             (f'¿Qué falla es la más común en {low1(e["corto"])}?',f'Entre las que más nos consultan: {low1(e["fallas"][idx[0]][0])}, {low1(e["fallas"][idx[1]][0])} y {low1(e["fallas"][idx[2]][0])}.'),
             ('¿Dan el costo antes de reparar?','Sí. Primero diagnosticamos y te informamos el costo antes de continuar.')]
        others=[f'reparacion-de-{x}-samsung-en-{zs}' for x in AXZ if x!=k][:2]
        nz=ZXA[(zi+1)%len(ZXA)]
        addp(slug,kind='zxa',h1=h1,title=mktitle(f'{h1}, Quito') if len(f'{h1}, Quito')<=65 else (h1 if len(h1)<=65 else h1[:62].rsplit(' ',1)[0]),desc=clip(f'{h1}: fallas frecuentes, visita a domicilio y costo antes de reparar. WhatsApp {PHONE_TXT}.',160),
             lead=f'Servicio técnico a domicilio para {low1(e["corto"])} Samsung en {zn}: diagnóstico claro y costo confirmado antes de reparar.',sections=s,faq=faq,
             related=[e['slug'],'servicio-tecnico-samsung-en-'+zs]+others+[f'reparacion-de-{k}-samsung-en-{nz}'],wamsg=f'Hola, necesito reparar {e["art"]} Samsung en {zn}, Quito.',icon=e['icon'],th=e['th'],photos=[],tec=None,zone=zs,eq=k)
# ---------- sectores (cobertura) ----------
for sc,(sslug,label) in SECTOR_HUBS.items():
    zs_=[z for z in ZSLUGS if ZD[z]['sector']==sc]
    extra=[x for x in VALLE_TERMS] if sc=='Valles' else []
    s=[(f'Barrios y sectores del {label}',f'<p>Atendemos estos barrios y sectores. Elige el tuyo para ver cómo coordinamos la visita:</p><ul class="cols3">'+''.join(f'<li><a href="@servicio-tecnico-samsung-en-{z}@">{E(ZD[z]["nombre"])}</a></li>' for z in zs_)+'</ul>'+('<h3>Más información para los valles</h3><ul class="sublist">'+''.join(f'<li><a href="@{x}@">{E(TERMS[x]["h1"])}</a></li>' for x in extra)+'</ul>' if extra else '')),
       (f'Electrodomésticos Samsung que reparamos en el {label}','<ul class="sublist">'+''.join(f'<li><a href="@{EQ[k]["slug"]}@">{E(EQ[k]["h1"])}</a></li>' for k in EQK)+'</ul>'),
       ('Cómo coordinamos la visita',ul(['Escríbenos por WhatsApp con tu barrio y una referencia','Cuéntanos qué equipo es, la marca, el modelo y la falla','Confirmamos el día y la hora de la visita','Te damos el costo antes de reparar'])),]
    cap_label=label[0].upper()+label[1:]
    addp(sslug,kind='sector',h1=f'Servicio técnico Samsung Quito: {label}',title=mktitle(f'Servicio técnico Samsung Quito: {label}'),desc=clip(f'Servicio técnico Samsung a domicilio en el {label}: '+', '.join(ZD[z]["nombre"] for z in zs_[:6])+' y más barrios. WhatsApp '+PHONE_TXT+'.',160),
         lead=f'Técnico a domicilio para electrodomésticos Samsung en los barrios del {label}. Diagnóstico claro y costo antes de reparar.',sections=s,
         faq=[(f'¿Qué barrios del {label} atienden?','Los que ves en la lista de esta página; si el tuyo no aparece, escríbenos y confirmamos.'),('¿Cuánto cuesta la visita?','Escríbenos con el equipo, el modelo y la falla; te confirmamos el costo antes de ir.')],
         related=[EQ[k]['slug'] for k in ('refrigeradoras','neveras','lavadoras','secadoras')],wamsg=f'Hola, necesito servicio técnico Samsung en el {label}.',icon='pin',th='',photos=[],tec=None,sector=sc)
SECTOR_TERMS=[v[0] for v in SECTOR_HUBS.values()]+VALLE_TERMS
# ---------- términos ----------
for t in T:
    eqs=''.join(f'<a class="card" href="@{EQ[k]["slug"]}@"><div><b>{E(EQ[k]["h1"])}</b><span>{E(EQ[k]["intro"][:100])}…</span></div></a>' for k in t['eq'][:4])
    s=[('Qué incluye',ul([E(x) for x in t['inc']])),('Cuándo conviene',f'<p>{E(t["cuando"])}</p>'),
       ('Equipos relacionados',f'<div class="cards g2">{eqs}</div>'),
       ('Cómo pedir la visita',ul(['Escríbenos por WhatsApp o llámanos al '+PHONE_TXT,'Cuéntanos qué equipo es, la marca, el modelo y la falla','Envía tu barrio y, si puedes, una foto de la etiqueta y un video corto','Coordinamos el día y la hora de la visita'])),
       ('Dónde atendemos en Quito','<div class="chips">'+''.join(f'<a href="@{x}@">{E((PAGES[x]["h1"] if x in PAGES else TERMS[x]["h1"]).replace("Servicio técnico Samsung Quito: ","").replace("Servicio técnico Samsung en ","").replace("Servicio técnico Samsung ","").capitalize())}</a>' for x in SECTOR_TERMS if x!=t['slug'])+'<a href="@zonas-de-servicio-quito@">Ver todas las zonas</a></div>')]
    others=[x for x in TEQ.get(t['eq'][0],[]) if x!=t['slug']][:3]
    addp(t['slug'],kind='term',h1=t['h1'],title=mktitle(t['tit']),desc=clip(t['desc'],160),lead=t['intro'],sections=s,photos=(REPF.get(t['eq'][0],[]) if t['slug'].startswith('repuestos-para-') else []),faq=t['faq']+[('¿Cómo contacto al servicio técnico?',f'Por WhatsApp o llamada al {PHONE_TXT} (+593 99 350 8191).')],
         related=[EQ[k]['slug'] for k in t['eq'][:3]]+others,wamsg=f'Hola, vi la página "{t["h1"]}". Necesito ayuda con un equipo Samsung en Quito.',icon=EQ[t['eq'][0]]['icon'],th=EQ[t['eq'][0]]['th'],tec=None,eq=t['eq'][0])
# ---------- guías ----------
for (slug,tit,eq,desc,secs) in GUIDES:
    s=[(h,b) for h,b in secs]
    rel=[EQ[eq]['slug']]+[x for x in GEQ.get(eq,[]) if x!=slug][:3]
    addp(slug,kind='guia',h1=tit,title=mktitle(tit) if len(tit)<=50 else clip(tit,62),desc=clip(desc if len(desc)>=100 else desc+' Guía práctica para electrodomésticos Samsung en Quito, con pasos claros y cuándo pedir ayuda.',160),lead=desc,sections=s,faq=[('¿Puedo pedir ayuda por WhatsApp?',f'Sí. Escríbenos al {PHONE_TXT} con el modelo y la falla y te orientamos.')],related=rel,
         wamsg=f'Hola, leí la guía "{tit}" y necesito ayuda con mi equipo Samsung en Quito.',icon=EQ[eq]['icon'],th=EQ[eq]['th'],photos=[],tec=None,eq=eq)
GUIDE_SLUGS=[g[0] for g in GUIDES]
if __name__=='__main__':
    from collections import Counter
    print(len(PAGES),Counter(p['kind'] for p in PAGES.values()))
    bad=[(s,len(p['title'])) for s,p in PAGES.items() if len(p['title'])>65]; print('títulos largos',bad[:10],len(bad))
    sl=[s for s in PAGES if '/' in s]; print(sl)
