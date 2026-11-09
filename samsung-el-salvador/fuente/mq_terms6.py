# -*- coding: utf-8 -*-
from mq_terms import T,t
from mq_eq2 import EQ
from mq_base import PHONE_TXT
from mq_zonas import ZD,ZSLUGS
import unicodedata,re
B="Samsung"; b=B.lower()
have={x['slug'] for x in T}
def add(slug,*a):
    if slug in have: return
    have.add(slug); t(slug,*a)
def sl(s): return re.sub(r'[^a-z0-9]+','-',unicodedata.normalize('NFD',s.lower()).encode('ascii','ignore').decode()).strip('-')
W=f'WhatsApp {PHONE_TXT}'
GAS=('cocinas','hornos','parrillas')
SECT={'Norte':'el Gran San Salvador','Centro':'La Libertad','Sur':'el occidente de El Salvador','Valles':'el oriente y la zona paracentral'}
def noms(sc,n=8): return ', '.join([ZD[z]['nombre'] for z in ZSLUGS if ZD[z]['sector']==sc][:n])
for k,e in EQ.items():
    pl=e['nombre'].lower(); plsl=sl(e['nombre']); art=e['art']
    for sc,lab in SECT.items():
        nm=noms(sc)
        add(f'reparacion-de-{plsl}-{b}-en-{sl(lab.replace("el ","").replace("los ",""))}',
            f'Reparación de {pl} {B} en {lab}',f'Reparación de {pl} {B} en {lab}',
            f'Reparación de {pl} {B} en {lab}: técnico a domicilio en {nm} y alrededores. '+W+'.',[k],
            f'Si vives en {lab} y {art} {B} falla, el técnico va hasta tu casa o apartamento. Atendemos municipios como {nm}, entre otros.',
            [f'Visita a domicilio en {lab}',f'Revisión de {art} en su lugar de uso','Explicación de la falla y costo antes de reparar','Coordinación del día y la hora por WhatsApp'],
            f'Escríbenos tu municipio o colonia en {lab}, el modelo y la falla para confirmar la visita.',
            [(f'¿Atienden {lab}?',f'Sí, cubrimos {lab}. Escríbenos tu municipio o colonia por WhatsApp y confirmamos.'),(f'¿Reparan {pl} {B} en {lab}?','Sí, a domicilio, con diagnóstico claro y costo antes de reparar.')])
    seg=('Si hueles a gas: cierra la llave, ventila, no uses llama ni interruptores y pide un técnico.' if k in GAS else 'Ante olor a quemado o fuga de agua, desconecta el equipo y cierra la llave.')
    add(f'tecnico-de-{plsl}-{b}-urgente-el-salvador',f'Técnico de {pl} {B} urgente en El Salvador',f'Técnico de {pl} {B} urgente en El Salvador',f'Técnico para urgencias de {pl} {B} en El Salvador: escribe por WhatsApp, te orientamos y confirmamos disponibilidad. {W}.',[k],
        f'Si {art} {B} dejó de funcionar de golpe, escríbenos: te indicamos qué hacer mientras tanto y confirmamos cuándo podemos ir.',
        ['Orientación inicial por WhatsApp','Confirmación de disponibilidad de visita','Diagnóstico a domicilio','Costo confirmado antes de reparar'],seg,
        [(f'¿Atienden urgencias de {pl}?','Escríbenos y te confirmamos la disponibilidad para tu sector.'),('¿Qué necesito enviar?','Modelo, falla y colonia; una foto o video ayuda.')])
    add(f'cotizar-reparacion-de-{plsl}-{b}-el-salvador',f'Cotizar la reparación de {pl} {B} en El Salvador',f'Cotizar reparación de {pl} {B} en El Salvador',f'Cotiza la reparación de {art} {B} en El Salvador: diagnóstico a domicilio y costo antes de reparar. {W}.',[k],
        f'Para cotizar la reparación de {art} {B} necesitamos saber qué falla. Envíanos el modelo y los síntomas y te orientamos; el costo final se confirma tras el diagnóstico.',
        ['Orientación por WhatsApp','Diagnóstico a domicilio','Costo antes de reparar','Reparación solo si tú aceptas'],
        'Cuanta más información envíes, más precisa será la orientación inicial.',
        [(f'¿Cuánto cuesta reparar {art}?','Depende de la falla y de la pieza; te lo confirmamos antes de reparar.'),('¿Cobran la visita?','Te confirmamos el costo de la visita por WhatsApp antes de ir.')])
EQK=list(EQ.keys())
add(f'agendar-visita-de-servicio-tecnico-{b}-el-salvador',f'Agendar visita de servicio técnico {B} en El Salvador',f'Agendar visita de servicio técnico {B} en El Salvador',f'Cómo agendar una visita de servicio técnico {B} en El Salvador: qué enviar por WhatsApp y cómo se coordina. '+W+'.',EQK[:4],
 'Agendar la visita es simple: nos escribes por WhatsApp con el equipo, el modelo, la falla y tu municipio o colonia, y coordinamos el día y la hora.',
 ['Mensaje por WhatsApp con modelo, falla y colonia','Confirmación de cobertura en tu sector','Coordinación del día y la hora','Diagnóstico a domicilio con costo antes de reparar'],
 'Si puedes, envía una foto de la etiqueta del equipo y un video corto de la falla.',
 [('¿Cómo agendo la visita?',f'Escríbenos por WhatsApp  al {PHONE_TXT} con el modelo, la falla y tu municipio o colonia.'),('¿Puedo elegir la hora?','Coordinamos contigo la mejor hora según la disponibilidad que te confirmemos.')])
add(f'cotizacion-de-reparacion-de-electrodomesticos-{b}-el-salvador',f'Cotización de reparación de electrodomésticos {B} en El Salvador',f'Cotización de reparación de electrodomésticos {B}',f'Pide la cotización de la reparación de tu electrodoméstico {B} en El Salvador: te damos el costo antes de reparar. '+W+'.',EQK[:4],
 'Para cotizar la reparación primero hay que saber qué falla. Nos envías el modelo y los síntomas, y después del diagnóstico te damos el costo antes de empezar.',
 ['Orientación inicial por WhatsApp','Diagnóstico del equipo a domicilio','Costo de la reparación antes de empezar','Tú decides si continuamos'],
 'El costo exacto depende de la falla y de la pieza; por eso se confirma después del diagnóstico.',
 [('¿Cuánto cuesta reparar mi electrodoméstico?','Depende de la falla y de la pieza. Te lo confirmamos antes de reparar, después del diagnóstico.'),('¿La cotización compromete a reparar?','No: primero te explicamos y tú decides.')])
add(f'tecnico-{b}-urgente-el-salvador',f'Técnico {B} urgente en El Salvador',f'Técnico {B} urgente en El Salvador',f'Técnico {B} para urgencias en El Salvador: equipo que no funciona, fuga de agua o falla eléctrica. Escribe por WhatsApp y confirmamos disponibilidad.',EQK[:4],
 'Algunas fallas no pueden esperar: una refrigeradora que deja de enfriar, una lavadora que inunda o un equipo que huele a quemado. Escríbenos y te decimos qué hacer y qué disponibilidad hay.',
 ['Orientación inmediata por WhatsApp sobre qué hacer','Confirmación de disponibilidad de visita','Revisión a domicilio','Costo confirmado antes de reparar'],
 'Si hay fuga de agua, cierra la llave y desconecta el equipo. Si huele a quemado, desconéctalo y no lo uses.',
 [('¿Atienden urgencias?','Escríbenos por WhatsApp y te confirmamos la disponibilidad para tu sector.'),('¿Qué hago mientras llega el técnico?','Desconecta el equipo si hay olor a quemado o fuga de agua y cierra la llave de agua.')])
