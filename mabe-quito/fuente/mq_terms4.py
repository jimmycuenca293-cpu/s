# -*- coding: utf-8 -*-
from mq_terms import T,t
from mq_eq2 import EQ
from mq_base import PHONE_TXT
SL={'refrigeradoras':'refrigeradoras','congeladores':'congeladores','lavadoras':'lavadoras','secadoras':'secadoras','centros-de-lavado':'centros-de-lavado','cocinas':'cocinas','hornos':'hornos','parrillas':'parrillas','campanas-extractoras':'campanas-extractoras'}
have={x['slug'] for x in T}
def low1(s): return s[:1].lower()+s[1:]
def add(slug,*a):
    if slug in have: return
    have.add(slug); t(slug,*a)
for k,e in EQ.items():
    pl=e['corto'].lower(); art=e['art']; sing=e['sing']; fn=[low1(f[0]) for f in e['fallas'][:4]]
    mods=e['modelos'][:3]
    # servicio técnico de X Mabe Quito (palabra clave principal por equipo)
    add(f'servicio-tecnico-de-{SL[k]}-mabe-quito',f'Servicio técnico de {pl} Mabe en Quito',f'Servicio técnico de {pl} Mabe en Quito',
      f'Servicio técnico de {pl} Mabe en Quito: diagnóstico, reparación y mantenimiento a domicilio, con costo antes de reparar. WhatsApp {PHONE_TXT}.',[k],
      f'Servicio técnico de {pl} Mabe en Quito, a domicilio: revisamos {art} en tu casa, identificamos la falla y te damos el costo antes de reparar.',
      ['Diagnóstico de la falla en el lugar','Reparación: '+'; '.join(fn),'Mantenimiento preventivo','Prueba de funcionamiento al terminar'],
      f'Pide el servicio técnico cuando {art} presente ruidos nuevos, fallas repetidas o deje de funcionar.',
      [(f'¿Cómo pido servicio técnico para {art}?',f'Por WhatsApp o llamada al {PHONE_TXT}, con la marca, el modelo y la falla.'),(f'¿Qué modelos de {pl} atienden?','Por ejemplo: '+', '.join(mods)+'.')])
    # repuestos
    add(f'repuestos-para-{SL[k]}-mabe-quito',f'Repuestos para {pl} Mabe en Quito',f'Repuestos para {pl} Mabe en Quito',
      f'Repuestos para {pl} Mabe en Quito: identificamos la pieza que necesita tu equipo y confirmamos disponibilidad y costo antes de reparar.',[k],
      f'Si {art} necesita una pieza, primero hay que confirmar cuál es. Revisamos el equipo, identificamos el repuesto según el modelo y te confirmamos disponibilidad y costo.',
      ['Identificación de la pieza según el modelo','Confirmación de disponibilidad y plazo','Costo informado antes de reparar','Instalación y prueba del repuesto'],
      f'Ten a mano {e["datos"]}: sin el modelo es difícil confirmar el repuesto correcto.',
      [(f'¿Consiguen repuestos para {pl} Mabe?','Depende del modelo y de la disponibilidad; te lo confirmamos antes de empezar.'),('¿Instalan el repuesto?','Sí, a domicilio, y probamos que el equipo quede funcionando.')])
    # mantenimiento
    add(f'mantenimiento-de-{SL[k]}-mabe-quito',f'Mantenimiento de {pl} Mabe en Quito',f'Mantenimiento de {pl} Mabe en Quito',
      f'Mantenimiento de {pl} Mabe en Quito a domicilio: limpieza, revisión y ajustes para evitar fallas y alargar la vida del equipo. WhatsApp {PHONE_TXT}.',[k],
      f'Un mantenimiento a tiempo evita fallas y alarga la vida de {art}. Lo hacemos a domicilio en Quito: limpieza, revisión de piezas y pruebas.',
      [e['mant'][0],e['mant'][1],e['mant'][2],'Prueba de funcionamiento y recomendaciones'],
      'Se recomienda hacerlo una vez al año, o antes si el equipo hace ruidos nuevos o rinde menos.',
      [(f'¿Cada cuánto se da mantenimiento a {art}?','Una vez al año en uso normal; más seguido si trabaja mucho.'),('¿El mantenimiento evita reparaciones?','Reduce el riesgo de fallas, pero no las elimina: las piezas se desgastan con el uso.')])
    # técnico a domicilio
    add(f'tecnico-de-{SL[k]}-mabe-a-domicilio-quito',f'Técnico de {pl} Mabe a domicilio en Quito',f'Técnico de {pl} Mabe a domicilio en Quito',
      f'Técnico de {pl} Mabe a domicilio en Quito: vamos a tu casa, revisamos el equipo y te damos el costo antes de reparar. WhatsApp {PHONE_TXT}.',[k],
      f'No tienes que mover {art}: el técnico va a tu casa en Quito, revisa el equipo en su lugar y te explica la falla antes de reparar.',
      ['Visita a domicilio en norte, centro, sur y valles','Revisión del equipo donde está instalado','Explicación de la falla y costo antes de reparar','Reparación y prueba'],
      e['seguridad'],
      [(f'¿El técnico de {pl} va a mi casa?','Sí, a domicilio en Quito. Coordinamos día y hora por WhatsApp.'),('¿Qué debo tener listo?','Marca, modelo y descripción de la falla; una foto de la etiqueta ayuda.')])
# instalación para equipos sin página de instalación
for k,e in EQ.items():
    if k in ('centros-de-lavado','parrillas','campanas-extractoras','refrigeradoras','congeladores'):
        pl=e['corto'].lower(); art=e['art']
        extra={'centros-de-lavado':'agua, desagüe, ducto y electricidad','parrillas':'gas o electricidad y nivelación','campanas-extractoras':'montaje, ducto y electricidad','refrigeradoras':'nivelación, ventilación y toma eléctrica','congeladores':'nivelación, ventilación y toma eléctrica'}[k]
        add(f'instalacion-de-{SL[k]}-mabe-quito',f'Instalación de {pl} Mabe en Quito',f'Instalación de {pl} Mabe en Quito',
          f'Instalación de {pl} Mabe en Quito: revisión del espacio y de las conexiones ({extra}) para que {art} funcione bien desde el primer día.',[k],
          f'Una buena instalación evita fallas y riesgos. Revisamos el espacio y las conexiones ({extra}) y dejamos {art} funcionando.',
          ['Revisión del espacio y de las conexiones','Nivelación y conexión','Prueba de funcionamiento','Indicaciones de uso y cuidado'],
          'Pídela antes de usar el equipo por primera vez o al mudarte.',
          [(f'¿Instalan {pl} Mabe?','Consulta por WhatsApp con el modelo y el lugar para confirmarte el servicio.'),('¿Qué necesito antes de la instalación?','Espacio despejado y las tomas o conexiones que el equipo requiere.')])
print(len(T))
