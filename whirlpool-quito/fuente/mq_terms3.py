# -*- coding: utf-8 -*-
from mq_terms import T,t
from mq_eq2 import EQ
from mq_base import PHONE_TXT
def cap(s): return s[:1].upper()+s[1:]
def low1(s): return s[:1].lower()+s[1:]
SL={'refrigeradoras':'refrigeradora','neveras':'nevera','congeladores':'congelador','lavadoras':'lavadora','secadoras':'secadora','centros-de-lavado':'centro-de-lavado','cocinas':'cocina','hornos':'horno','parrillas':'parrilla','campanas-extractoras':'campana-extractora'}
for k,e in EQ.items():
    sing=e['sing']; art=e['art']; sl=SL[k]; fn=[low1(f[0]) for f in e['fallas'][:4]]
    causes=[f[1] for f in e['fallas'][:3]]
    # A) reparar
    t(f'reparar-{sl}-whirlpool-quito',f'Reparar {art} Whirlpool en Quito'.replace('Reparar la','Reparar la').replace('Reparar el','Reparar el'),f'Reparar {sing} Whirlpool en Quito',
      f'Reparar {art} Whirlpool en Quito: fallas comunes, qué revisar antes de llamar y cuándo pedir un técnico. Visita a domicilio y costo antes de reparar. WhatsApp {PHONE_TXT}.',[k],
      f'Si {art} Whirlpool dejó de funcionar bien, lo primero es saber qué tiene. Reparamos {e["corto"].lower()} Whirlpool a domicilio en Quito: diagnosticamos la falla, te explicamos y te damos el costo antes de reparar.',
      ['Diagnóstico de la falla en tu casa','Reparación de: '+'; '.join(fn),'Costo confirmado antes de reparar','Prueba de funcionamiento al terminar'],
      f'Conviene repararlo cuando la falla es de una pieza accesible y el equipo estaba funcionando bien. {e["seguridad"]}',
      [(f'¿Cuánto tarda reparar {art} Whirlpool?','Depende de la falla; si hace falta una pieza, te avisamos el plazo antes de empezar.'),(f'¿Qué fallas son más comunes en {low1(e["corto"])} Whirlpool?','Entre las más consultadas: '+', '.join(fn[:3])+'.')])
    # B) dónde reparar
    t(f'donde-reparar-{sl}-whirlpool-quito',f'Dónde reparar {art} Whirlpool en Quito',f'Dónde reparar {sing} Whirlpool en Quito',
      f'Dónde reparar {art} Whirlpool en Quito: servicio a domicilio o taller, y qué preguntar antes de elegir. WhatsApp {PHONE_TXT}.',[k],
      f'Al buscar dónde reparar {art} Whirlpool en Quito conviene comparar: llevarla a un taller o pedir un técnico a domicilio. Estas son las claves para elegir bien.',
      ['Si el equipo está en garantía de fábrica, consulta primero las condiciones con el fabricante','Fuera de garantía, un técnico a domicilio evita mover el equipo','Pide siempre diagnóstico y costo antes de aceptar la reparación','Pregunta qué garantía tiene la reparación y qué cubre'],
      f'{cap(e["quito"])}',
      [(f'¿Es mejor reparar {art} en casa o llevarla a un taller?','Depende del tamaño y de la instalación. Los equipos grandes o empotrados se revisan mejor en casa.'),('¿Qué hago si el equipo está en garantía?','Revisa las condiciones de la garantía de fábrica antes de pedir una reparación.')])
    # C) cuánto cuesta
    t(f'cuanto-cuesta-reparar-{sl}-whirlpool-quito',f'Cuánto cuesta reparar {art} Whirlpool en Quito',f'Cuánto cuesta reparar {sing} Whirlpool en Quito',
      f'Cuánto cuesta reparar {art} Whirlpool en Quito: de qué depende el costo, qué piezas suelen cambiarse y cómo pedir una cotización clara. WhatsApp {PHONE_TXT}.',[k],
      f'No hay un precio único para reparar {art} Whirlpool: depende de la falla, de la pieza y del trabajo necesario. Por eso primero diagnosticamos y te damos el costo antes de reparar.',
      ['La falla y la pieza que se cambie','La disponibilidad del repuesto según el modelo','El tiempo de trabajo y el acceso al equipo','El costo de la visita, que te confirmamos antes de ir'],
      'Causas frecuentes que influyen en el costo: '+' '.join(causes[:2]),
      [(f'¿Cuánto cuesta la visita de diagnóstico de {art}?','Escríbenos con el modelo y la falla; te confirmamos el costo de la visita antes de ir.'),('¿Cuándo conviene reemplazarlo en vez de repararlo?','Si la reparación se acerca al costo de un equipo nuevo y el equipo es muy antiguo, conviene evaluarlo. Te lo decimos con honestidad en el diagnóstico.')])
t('reparar-electrodomesticos-whirlpool-quito','Reparar electrodomésticos Whirlpool en Quito','Reparar electrodomésticos Whirlpool en Quito','Reparar electrodomésticos Whirlpool en Quito: refrigeradoras, neveras, lavadoras, secadoras, cocinas, hornos y parrillas a domicilio. Diagnóstico, costo antes de reparar. WhatsApp 099 350 8191.',['refrigeradoras','lavadoras','secadoras','cocinas'],
 'Si tu electrodoméstico Whirlpool falla, puedes repararlo sin moverlo: vamos a tu casa en Quito, diagnosticamos, te explicamos la falla y te damos el costo antes de reparar.',
 ['Refrigeradoras, neveras, lavadoras y secadoras','Casas, apartamentos y conjuntos de Quito','Visita a domicilio en norte, centro, sur y valles','Costo confirmado antes de reparar'],
 'Úsalo como punto de partida: elige tu equipo y revisa fallas comunes y cómo pedir la visita.',
 [('¿Puedo reparar mi electrodoméstico Whirlpool sin llevarlo a un taller?','Sí. Vamos a tu casa u oficina en Quito.'),('¿Qué necesito para pedir la visita?','Marca, modelo, falla y tu barrio. Una foto de la etiqueta ayuda.')])
t('donde-reparar-electrodomesticos-whirlpool-quito','Dónde reparar electrodomésticos Whirlpool en Quito','Dónde reparar electrodomésticos Whirlpool en Quito','Dónde reparar electrodomésticos Whirlpool en Quito: opciones, garantía de fábrica, técnicos a domicilio y qué preguntar antes de contratar. WhatsApp 099 350 8191.',['refrigeradoras','lavadoras'],
 'Hay varias formas de reparar un electrodoméstico Whirlpool en Quito. Te explicamos las opciones para que elijas con información y sin sorpresas.',
 ['Mientras haya garantía de fábrica, consulta primero sus condiciones','Técnico a domicilio: sin mover el equipo','Taller: útil para equipos pequeños y fáciles de transportar','Compara diagnóstico, costo, garantía de la reparación y tiempos'],
 'Si ya venció la garantía, un técnico a domicilio suele ser lo más ágil. Escríbenos y te orientamos.',
 [('¿Quién repara electrodomésticos Whirlpool en Quito?','Hay talleres y técnicos a domicilio. Nosotros vamos a tu casa en Quito.'),('¿Debo llevar el equipo?','No necesariamente: la mayoría se revisa en casa.')])
t('whirlpool-quito-servicio-tecnico-y-reparacion','Whirlpool Quito: servicio técnico y reparación de electrodomésticos','Whirlpool Quito: servicio técnico y reparación','Servicio técnico Whirlpool Quito: reparación de refrigeradoras, neveras, lavadoras, secadoras, cocinas, hornos y parrillas Whirlpool a domicilio. WhatsApp 099 350 8191.',['refrigeradoras','lavadoras','secadoras','cocinas'],
 'Si buscas Whirlpool en Quito para reparar un electrodoméstico, aquí encuentras servicio técnico Whirlpool Quito a domicilio para equipos Whirlpool, con diagnóstico claro y costo antes de reparar.',
 ['Equipos Whirlpool del hogar','Cobertura en norte, centro, sur y valles de Quito','Coordinación por WhatsApp','Costo confirmado antes de reparar'],
 'Esta página resume qué hacemos; cada equipo y cada zona tiene su propia información.',
 [('¿Qué es Servicio Técnico Whirlpool Quito?','Un servicio técnico a domicilio para electrodomésticos Whirlpool en Quito: diagnóstico, reparación y mantenimiento.'),('¿Qué marcas reparan?','Nos enfocamos en Whirlpool.')])
t('electrodomestico-whirlpool-no-funciona-que-hacer-en-quito','Electrodoméstico Whirlpool no funciona en Quito: qué hacer','Electrodoméstico Whirlpool no funciona: qué hacer','Mi electrodoméstico Whirlpool no funciona en Quito: primeras revisiones seguras, qué no hacer y cómo pedir un técnico a domicilio. WhatsApp 099 350 8191.',['refrigeradoras','lavadoras','cocinas'],
 'Cuando un electrodoméstico Whirlpool deja de funcionar, unos pasos simples ayudan a descartar causas sencillas y a evitar daños mayores antes de llamar al técnico.',
 ['Revisa tomacorriente, breaker y llaves de agua','Anota el código de error si la pantalla lo muestra','No fuerces piezas ni abras paneles eléctricos','Escríbenos con el modelo y un video corto de la falla'],
 'Si hay fuga de agua, chispas o humo, desconecta, cierra la llave y pide ayuda de inmediato.',
 [('¿Qué reviso primero?','Que haya energía, que el breaker no esté disparado y que las llaves estén abiertas.'),('¿Cuándo llamo al técnico?','Si ya revisaste lo básico y sigue la falla, o si hay riesgo.')])
