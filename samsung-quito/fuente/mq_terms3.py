# -*- coding: utf-8 -*-
from mq_terms import T,t
from mq_eq2 import EQ
from mq_base import PHONE_TXT
def cap(s): return s[:1].upper()+s[1:]
def low1(s): return s[:1].lower()+s[1:]
SL={'refrigeradoras':'refrigeradora','congeladores':'congelador','lavadoras':'lavadora','secadoras':'secadora','centros-de-lavado':'centro-de-lavado','cocinas':'cocina','hornos':'horno','parrillas':'parrilla','campanas-extractoras':'campana-extractora'}
for k,e in EQ.items():
    sing=e['sing']; art=e['art']; sl=SL[k]; fn=[low1(f[0]) for f in e['fallas'][:4]]
    causes=[f[1] for f in e['fallas'][:3]]
    # A) reparar
    t(f'reparar-{sl}-samsung-quito',f'Reparar {art} Samsung en Quito'.replace('Reparar la','Reparar la').replace('Reparar el','Reparar el'),f'Reparar {sing} Samsung en Quito',
      f'Reparar {art} Samsung en Quito: fallas comunes, qué revisar antes de llamar y cuándo pedir un técnico. Visita a domicilio y costo antes de reparar. WhatsApp {PHONE_TXT}.',[k],
      f'Si {art} Samsung dejó de funcionar bien, lo primero es saber qué tiene. Reparamos {e["corto"].lower()} Samsung a domicilio en Quito: diagnosticamos la falla, te explicamos y te damos el costo antes de reparar.',
      ['Diagnóstico de la falla en tu casa','Reparación de: '+'; '.join(fn),'Costo confirmado antes de reparar','Prueba de funcionamiento al terminar'],
      f'Conviene repararlo cuando la falla es de una pieza accesible y el equipo estaba funcionando bien. {e["seguridad"]}',
      [(f'¿Cuánto tarda reparar {art} Samsung?','Depende de la falla; si hace falta una pieza, te avisamos el plazo antes de empezar.'),(f'¿Qué fallas son más comunes en {low1(e["corto"])} Samsung?','Entre las más consultadas: '+', '.join(fn[:3])+'.')])
    # B) dónde reparar
    t(f'donde-reparar-{sl}-samsung-quito',f'Dónde reparar {art} Samsung en Quito',f'Dónde reparar {sing} Samsung en Quito',
      f'Dónde reparar {art} Samsung en Quito: servicio a domicilio o taller, y qué preguntar antes de elegir. WhatsApp {PHONE_TXT}.',[k],
      f'Al buscar dónde reparar {art} Samsung en Quito conviene comparar: llevarla a un taller o pedir un técnico a domicilio. Estas son las claves para elegir bien.',
      ['Si el equipo está en garantía de fábrica, consulta primero las condiciones con el fabricante','Fuera de garantía, un técnico a domicilio evita mover el equipo','Pide siempre diagnóstico y costo antes de aceptar la reparación','Pregunta qué garantía tiene la reparación y qué cubre'],
      f'{cap(e["quito"])}',
      [(f'¿Es mejor reparar {art} en casa o llevarla a un taller?','Depende del tamaño y de la instalación. Los equipos grandes o empotrados se revisan mejor en casa.'),('¿Qué hago si el equipo está en garantía?','Revisa las condiciones de la garantía de fábrica antes de pedir una reparación.')])
    # C) cuánto cuesta
    t(f'cuanto-cuesta-reparar-{sl}-samsung-quito',f'Cuánto cuesta reparar {art} Samsung en Quito',f'Cuánto cuesta reparar {sing} Samsung en Quito',
      f'Cuánto cuesta reparar {art} Samsung en Quito: de qué depende el costo, qué piezas suelen cambiarse y cómo pedir una cotización clara. WhatsApp {PHONE_TXT}.',[k],
      f'No hay un precio único para reparar {art} Samsung: depende de la falla, de la pieza y del trabajo necesario. Por eso primero diagnosticamos y te damos el costo antes de reparar.',
      ['La falla y la pieza que se cambie','La disponibilidad del repuesto según el modelo','El tiempo de trabajo y el acceso al equipo','El costo de la visita, que te confirmamos antes de ir'],
      'Causas frecuentes que influyen en el costo: '+' '.join(causes[:2]),
      [(f'¿Cuánto cuesta la visita de diagnóstico de {art}?','Escríbenos con el modelo y la falla; te confirmamos el costo de la visita antes de ir.'),('¿Cuándo conviene reemplazarlo en vez de repararlo?','Si la reparación se acerca al costo de un equipo nuevo y el equipo es muy antiguo, conviene evaluarlo. Te lo decimos con honestidad en el diagnóstico.')])
t('reparar-electrodomesticos-samsung-quito','Reparar electrodomésticos Samsung en Quito','Reparar electrodomésticos Samsung en Quito','Reparar electrodomésticos Samsung en Quito: refrigeradoras, lavadoras, secadoras y centros de lavado a domicilio. Diagnóstico, costo antes de reparar. WhatsApp 099 350 8191.',['refrigeradoras','lavadoras','secadoras','cocinas'],
 'Si tu electrodoméstico Samsung falla, puedes repararlo sin moverlo: vamos a tu casa en Quito, diagnosticamos, te explicamos la falla y te damos el costo antes de reparar.',
 ['Refrigeradoras, lavadoras, secadoras y centros de lavado','Casas, apartamentos y conjuntos de Quito','Visita a domicilio en norte, centro, sur y valles','Costo confirmado antes de reparar'],
 'Úsalo como punto de partida: elige tu equipo y revisa fallas comunes y cómo pedir la visita.',
 [('¿Puedo reparar mi electrodoméstico Samsung sin llevarlo a un taller?','Sí. Vamos a tu casa u oficina en Quito.'),('¿Qué necesito para pedir la visita?','Marca, modelo, falla y tu barrio. Una foto de la etiqueta ayuda.')])
t('donde-reparar-electrodomesticos-samsung-quito','Dónde reparar electrodomésticos Samsung en Quito','Dónde reparar electrodomésticos Samsung en Quito','Dónde reparar electrodomésticos Samsung en Quito: opciones, garantía de fábrica, técnicos a domicilio y qué preguntar antes de contratar. WhatsApp 099 350 8191.',['refrigeradoras','lavadoras'],
 'Hay varias formas de reparar un electrodoméstico Samsung en Quito. Te explicamos las opciones para que elijas con información y sin sorpresas.',
 ['Mientras haya garantía de fábrica, consulta primero sus condiciones','Técnico a domicilio: sin mover el equipo','Taller: útil para equipos pequeños y fáciles de transportar','Compara diagnóstico, costo, garantía de la reparación y tiempos'],
 'Si ya venció la garantía, un técnico a domicilio suele ser lo más ágil. Escríbenos y te orientamos.',
 [('¿Quién repara electrodomésticos Samsung en Quito?','Hay talleres y técnicos a domicilio. Nosotros vamos a tu casa en Quito.'),('¿Debo llevar el equipo?','No necesariamente: la mayoría se revisa en casa.')])
t('samsung-quito-servicio-tecnico-y-reparacion','Samsung Quito: servicio técnico y reparación de electrodomésticos','Samsung Quito: servicio técnico y reparación','Servicio técnico Samsung Quito: reparación de refrigeradoras, lavadoras, secadoras y centros de lavado Samsung a domicilio. WhatsApp 099 350 8191.',['refrigeradoras','lavadoras','secadoras','cocinas'],
 'Si buscas Samsung en Quito para reparar un electrodoméstico, aquí encuentras servicio técnico Samsung Quito a domicilio para equipos Samsung, con diagnóstico claro y costo antes de reparar.',
 ['Equipos Samsung del hogar','Cobertura en norte, centro, sur y valles de Quito','Coordinación por WhatsApp','Costo confirmado antes de reparar'],
 'Esta página resume qué hacemos; cada equipo y cada zona tiene su propia información.',
 [('¿Qué es Servicio Técnico Samsung Quito?','Un servicio técnico a domicilio para electrodomésticos Samsung en Quito: diagnóstico, reparación y mantenimiento.'),('¿Qué marcas reparan?','Nos enfocamos en Samsung.')])
t('electrodomestico-samsung-no-funciona-que-hacer-en-quito','Electrodoméstico Samsung no funciona en Quito: qué hacer','Electrodoméstico Samsung no funciona: qué hacer','Mi electrodoméstico Samsung no funciona en Quito: primeras revisiones seguras, qué no hacer y cómo pedir un técnico a domicilio. WhatsApp 099 350 8191.',['refrigeradoras','lavadoras','cocinas'],
 'Cuando un electrodoméstico Samsung deja de funcionar, unos pasos simples ayudan a descartar causas sencillas y a evitar daños mayores antes de llamar al técnico.',
 ['Revisa tomacorriente, breaker y llaves de agua','Anota el código de error si la pantalla lo muestra','No fuerces piezas ni abras paneles eléctricos','Escríbenos con el modelo y un video corto de la falla'],
 'Si hay fuga de agua, chispas o humo, desconecta, cierra la llave y pide ayuda de inmediato.',
 [('¿Qué reviso primero?','Que haya energía, que el breaker no esté disparado y que las llaves estén abiertas.'),('¿Cuándo llamo al técnico?','Si ya revisaste lo básico y sigue la falla, o si hay riesgo.')])
