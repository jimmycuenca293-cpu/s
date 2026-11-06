# -*- coding: utf-8 -*-
from mq_terms import T,t
from mq_eq2 import EQ
from mq_base import PHONE_TXT
have={x['slug'] for x in T}
def add(slug,*a):
    if slug in have: return
    have.add(slug); t(slug,*a)
W=f'WhatsApp {PHONE_TXT}'
# ---- Centro de servicio por equipo
for k,pl,art in (('lavadoras','lavadoras','la lavadora'),('secadoras','secadoras','la secadora'),('refrigeradoras','refrigeradoras','la refrigeradora'),('neveras','neveras','la nevera'),('cocinas','cocinas','la cocina'),('hornos','hornos','el horno')):
    add(f'centro-de-servicio-de-{pl}-whirlpool-quito',f'Centro de servicio de {pl} Whirlpool en Quito',f'Centro de servicio de {pl} Whirlpool en Quito',
      f'Centro de servicio de {pl} Whirlpool en Quito: técnico a domicilio para reparar y dar mantenimiento sin que muevas el equipo. {W}.',[k],
      f'Si buscas un centro de servicio de {pl} Whirlpool en Quito, hay una forma más cómoda: el técnico va a tu casa, revisa {art} en su lugar y te explica la falla antes de reparar.',
      ['Diagnóstico a domicilio, sin trasladar el equipo','Reparación y mantenimiento en tu casa o apartamento','Costo confirmado antes de reparar','Atención en norte, centro, sur y valles de Quito'],
      'Mientras el equipo esté en garantía de fábrica, consulta primero sus condiciones con el fabricante. Fuera de garantía, la visita a domicilio suele ser lo más práctico.',
      [(f'¿Tengo que llevar {art} a un centro de servicio?','No necesariamente: la mayoría de las reparaciones se hacen en casa. Escríbenos y te orientamos.'),('¿Cómo pido la visita?',f'Por WhatsApp o llamada al {PHONE_TXT}, con el modelo, la falla y tu barrio.')])
# ---- Marca / generales
add('soporte-tecnico-whirlpool-quito','Soporte técnico Whirlpool en Quito','Soporte técnico Whirlpool en Quito','Soporte técnico Whirlpool en Quito para lavadoras, secadoras, neveras y refrigeradoras: orientación por WhatsApp y visita a domicilio. '+W+'.',['lavadoras','secadoras','refrigeradoras','neveras'],
 'Si necesitas soporte técnico Whirlpool en Quito, empezamos por WhatsApp: nos cuentas la falla, te orientamos y, si hace falta, coordinamos la visita a domicilio.',
 ['Orientación inicial por WhatsApp con foto y video','Visita técnica a domicilio en Quito','Diagnóstico claro y costo antes de reparar','Seguimiento hasta que el equipo quede funcionando'],
 'Escríbenos con el modelo y la falla; cuanto más información, más precisa es la orientación.',
 [('¿Qué necesito para recibir soporte?','Marca y modelo, descripción de la falla, tu barrio y, si puedes, una foto de la etiqueta y un video corto.'),('¿El soporte incluye visita?','La orientación inicial es por WhatsApp; el diagnóstico definitivo se hace en el equipo, a domicilio.')])
add('servicio-tecnico-whirlpool-ecuador-quito','Servicio técnico Whirlpool Ecuador: atención en Quito','Servicio técnico Whirlpool Ecuador: atención en Quito','Servicio técnico Whirlpool en Ecuador con atención a domicilio en Quito y sus valles: lavadoras, secadoras, neveras y refrigeradoras. '+W+'.',['lavadoras','secadoras','refrigeradoras','neveras'],
 'Si buscas servicio técnico Whirlpool en Ecuador y vives en Quito o sus valles, atendemos a domicilio: lavadoras, secadoras, neveras y refrigeradoras.',
 ['Cobertura en norte, centro, sur y valles de Quito','Visita a domicilio coordinada por WhatsApp','Diagnóstico y costo antes de reparar','Mantenimiento e instalación'],
 'Para otras ciudades de Ecuador, escríbenos y te decimos si podemos atender tu zona.',
 [('¿Atienden solo Quito?','Nuestra cobertura es Quito y sus valles; para otras zonas, consúltanos por WhatsApp.'),('¿Qué equipos Whirlpool reparan?','Lavadoras, secadoras, neveras y refrigeradoras.')])
add('whirlpool-quito-servicio-tecnico-y-reparacion','Whirlpool Quito: servicio técnico y reparación de electrodomésticos','Whirlpool Quito: servicio técnico y reparación','Whirlpool Quito: servicio técnico y reparación a domicilio de lavadoras, secadoras, neveras y refrigeradoras Whirlpool. '+W+'.',['lavadoras','secadoras','refrigeradoras','neveras'],
 'Si buscas Whirlpool en Quito para reparar un electrodoméstico, aquí encuentras servicio técnico Whirlpool Quito a domicilio, con diagnóstico claro y costo antes de reparar.',
 ['Lavadoras, secadoras, neveras y refrigeradoras Whirlpool','Cobertura en norte, centro, sur y valles','Coordinación por WhatsApp','Costo confirmado antes de reparar'],
 'Esta página resume qué hacemos; cada equipo y cada barrio tiene su propia información.',
 [('¿Qué es Servicio Técnico Whirlpool Quito?','Un servicio técnico a domicilio para electrodomésticos Whirlpool en Quito: diagnóstico, reparación y mantenimiento.'),('¿Qué marcas reparan?','Nos enfocamos en Whirlpool.')])
add('que-incluye-la-visita-de-servicio-tecnico-whirlpool-en-quito','Qué incluye la visita de servicio técnico Whirlpool en Quito','Qué incluye la visita de servicio técnico Whirlpool','Qué incluye la visita de servicio técnico Whirlpool en Quito: diagnóstico, explicación de la falla, costo antes de reparar y prueba final. '+W+'.',['lavadoras','refrigeradoras'],
 'Antes de pedir la visita conviene saber qué incluye: revisamos el equipo, te explicamos la falla y te damos el costo antes de reparar.',
 ['Revisión del equipo y pruebas de la falla','Explicación clara de la causa','Costo de la reparación antes de empezar','Prueba de funcionamiento al terminar'],
 'Si no conviene reparar, también te lo decimos.',
 [('¿Pagan la visita aunque no repare?','Escríbenos y te confirmamos el costo de la visita antes de ir.'),('¿Puedo decidir después del diagnóstico?','Sí, primero te explicamos y tú decides si continuamos.')])
# ---- Líneas de producto y búsquedas específicas Whirlpool
def linea(slug,h1,k,desc,intro,inc,cuando,faq): add(slug,h1,h1,desc,[k],intro,inc,cuando,faq)
linea('reparacion-de-lavadoras-whirlpool-xpert-system-quito','Reparación de lavadoras Whirlpool Xpert System en Quito','lavadoras','Reparación de lavadoras Whirlpool Xpert System en Quito: no centrifugan, no desaguan, ruidos y códigos de error. Visita a domicilio. '+W+'.',
 'Si tu lavadora Whirlpool Xpert System no centrifuga, no desagua, hace ruido o muestra un código de error en el panel, la revisamos en tu casa, te explicamos la falla y te damos el costo antes de reparar.',
 ['Revisión del desagüe, la bomba y el filtro','Revisión de amortiguadores, motor y nivelación','Lectura del código de error del panel','Prueba de ciclo completo'],'Anota el código exacto del panel y el modelo antes de escribirnos.',
 [('¿Reparan lavadoras Whirlpool Xpert System?','Sí, a domicilio en Quito. Envíanos el modelo y la falla por WhatsApp.'),('¿Qué hago si muestra un código de error?','Anótalo tal como aparece y escríbenos con el modelo; el significado depende del equipo.')])
linea('reparacion-de-lavadoras-whirlpool-con-agitador-quito','Reparación de lavadoras Whirlpool con agitador en Quito','lavadoras','Reparación de lavadoras Whirlpool de carga superior con agitador en Quito: no agitan, no centrifugan y ruidos. '+W+'.',
 'Las lavadoras de carga superior con agitador mueven la ropa con la pieza central de la tina. Si no agita, hace ruido o no centrifuga, revisamos transmisión, motor, correa y tapa.',
 ['Revisión del agitador y su acople','Revisión del motor, la correa y la transmisión','Revisión del seguro de tapa','Prueba de lavado y centrifugado'],'Si el agitador queda suelto o la lavadora no gira, pide una revisión.',
 [('¿Por qué no agita?','Acople del agitador, transmisión, motor o seguro de tapa; se confirma en la visita.'),('¿Se repara en casa?','Normalmente sí.')])
linea('reparacion-de-lavadoras-whirlpool-carga-frontal-quito','Reparación de lavadoras Whirlpool de carga frontal en Quito','lavadoras','Reparación de lavadoras Whirlpool de carga frontal en Quito: fugas por la puerta, olores, ruido y no desagua. '+W+'.',
 'En las lavadoras de carga frontal las fallas típicas son fugas por el empaque de la puerta, olor a humedad y ruido al centrifugar. Las revisamos a domicilio.',
 ['Revisión del empaque y del seguro de la puerta','Limpieza del filtro de desagüe','Revisión de amortiguadores y rodamientos','Prueba de ciclo completo'],'Deja la puerta entreabierta después de lavar para evitar olores.',
 [('¿Por qué gotea por la puerta?','Empaque desgastado o sucio, o exceso de detergente.'),('¿Se limpia el moho?','Sí, hacemos limpieza de tina y empaque en el mantenimiento.')])
linea('reparacion-de-refrigeradoras-whirlpool-side-by-side-quito','Reparación de refrigeradoras Whirlpool Side by Side en Quito','refrigeradoras','Reparación de refrigeradoras Whirlpool Side by Side en Quito: frío, hielo, dispensador y escarcha. Visita a domicilio. '+W+'.',
 'Las refrigeradoras Side by Side (dos puertas verticales) suelen tener dispensador de agua y fábrica de hielo. Las revisamos a domicilio en Quito: frío, descongelación, hielo y dispensador.',
 ['Revisión del frío en refrigerador y congelador','Revisión de descongelación y ventiladores','Revisión del dispensador y del hielo','Prueba de temperatura'],'Son equipos grandes y pesados: mejor que el técnico vaya a tu casa.',
 [('¿Reparan el dispensador de agua?','Sí: filtro, manguera y válvula.'),('¿Por qué hay escarcha?','Descongelación o empaque de puerta; se confirma en la visita.')])
linea('reparacion-de-refrigeradoras-whirlpool-french-door-quito','Reparación de refrigeradoras Whirlpool French Door en Quito','refrigeradoras','Reparación de refrigeradoras Whirlpool French Door en Quito: frío, hielo, dispensador y escarcha. Visita a domicilio. '+W+'.',
 'Las refrigeradoras French Door (dos puertas arriba y cajón de congelador abajo) tienen varios sistemas. Revisamos frío, descongelación, hielo y dispensador en tu cocina.',
 ['Revisión del frío en ambas zonas','Revisión de descongelación y ventiladores','Revisión de hielo y dispensador','Prueba de temperatura'],'Pide la revisión si no enfría parejo, hay escarcha o gotea agua.',
 [('¿Por qué el cajón del congelador se llena de escarcha?','Empaque, descongelación o ventilador; se confirma en la visita.'),('¿Reparan el dispensador?','Sí: filtro, manguera y válvula.')])
linea('reparacion-de-refrigeradoras-whirlpool-congelador-superior-quito','Reparación de refrigeradoras Whirlpool de congelador superior en Quito','refrigeradoras','Reparación de refrigeradoras Whirlpool de congelador superior (Top Mount) en Quito: no enfrían, escarcha y ruidos. '+W+'.',
 'Las refrigeradoras de congelador superior son las más comunes en los hogares. Si no enfría abajo, hay escarcha o hace ruido, la revisamos a domicilio.',
 ['Revisión de ventilador, sensores y descongelación','Revisión del empaque de las puertas','Revisión del compresor y su arranque','Prueba de temperatura'],'Si el congelador enfría pero abajo no, suele ser circulación de aire: pide revisión.',
 [('¿Por qué el congelador enfría y abajo no?','Escarcha que tapa el flujo de aire, ventilador o sensor.'),('¿Es urgente?','Si pierdes frío en la zona de alimentos, sí.')])
linea('reparacion-de-refrigeradoras-whirlpool-congelador-inferior-quito','Reparación de refrigeradoras Whirlpool de congelador inferior en Quito','refrigeradoras','Reparación de refrigeradoras Whirlpool de congelador inferior (Bottom Mount) en Quito. Visita a domicilio. '+W+'.',
 'En las refrigeradoras de congelador inferior el cajón se abre hacia afuera. Revisamos frío, descongelación, sellos y ruidos en tu casa.',
 ['Revisión del frío en ambas zonas','Revisión del sello y de los rieles del cajón','Revisión de descongelación y ventiladores','Prueba de temperatura'],'Si el cajón no cierra bien, entra aire húmedo y se forma escarcha.',
 [('¿Por qué se forma escarcha en el cajón?','Sello que no cierra, descongelación o mucha humedad.'),('¿Reparan en casa?','Normalmente sí.')])
linea('reparacion-de-neveras-whirlpool-side-by-side-quito','Reparación de neveras Whirlpool Side by Side en Quito','neveras','Reparación de neveras Whirlpool Side by Side en Quito: frío, hielo, dispensador y ruidos. Visita a domicilio. '+W+'.',
 'Las neveras Side by Side (dos puertas verticales) tienen dispensador y fábrica de hielo. Las revisamos a domicilio en Quito.',
 ['Revisión del frío en ambas puertas','Revisión del dispensador y del hielo','Revisión de descongelación','Prueba de temperatura'],'Son equipos grandes: mejor que el técnico vaya a tu casa.',
 [('¿Reparan el dispensador de agua?','Sí: filtro, manguera y válvula.'),('¿Por qué hay escarcha?','Descongelación o sello de puerta.')])
linea('reparacion-de-neveras-whirlpool-french-door-quito','Reparación de neveras Whirlpool French Door en Quito','neveras','Reparación de neveras Whirlpool French Door en Quito: frío, hielo y escarcha. Visita a domicilio. '+W+'.',
 'Las neveras French Door tienen congelador tipo cajón. Revisamos frío, descongelación, hielo y dispensador en tu cocina.',
 ['Revisión del frío','Revisión de descongelación y ventiladores','Revisión de hielo y dispensador','Prueba de temperatura'],'Pide la revisión si no enfría parejo o gotea agua.',
 [('¿Por qué gotea agua?','Desagüe de descongelación tapado o congelado.'),('¿Es urgente?','Si no enfría, sí.')])
linea('cambio-de-filtro-de-agua-de-nevera-whirlpool-quito','Cambio de filtro de agua de nevera Whirlpool en Quito','neveras','Cambio de filtro de agua de nevera y refrigeradora Whirlpool en Quito: cuándo cambiarlo, luz del filtro y dispensador lento. '+W+'.',
 'Si el agua de tu nevera Whirlpool sale lenta, con mal sabor o se enciende la luz del filtro, probablemente toca cambiar el filtro. Te orientamos con el modelo correcto y lo cambiamos en la visita.',
 ['Identificación del filtro según el modelo','Cambio del filtro y purga del sistema','Reinicio de la luz del filtro','Revisión del dispensador y de las mangueras'],'Como referencia general, el filtro se cambia cada 6 meses o cuando el agua salga lenta o con mal sabor.',
 [('¿Cada cuánto se cambia el filtro?','Cada 6 meses aproximadamente, o antes si el agua sale lenta o con mal sabor.'),('¿Cómo sé qué filtro necesita mi nevera?','Con el modelo de la nevera, que está en la etiqueta interior; envíanos una foto por WhatsApp.')])
linea('cambio-de-filtro-de-agua-de-refrigeradora-whirlpool-quito','Cambio de filtro de agua de refrigeradora Whirlpool en Quito','refrigeradoras','Cambio de filtro de agua de refrigeradora Whirlpool en Quito: modelo correcto, purga y reinicio de la luz. '+W+'.',
 'El filtro de agua de la refrigeradora Whirlpool mejora el sabor del agua y del hielo. Cuando se vence, el dispensador sale lento o la luz del filtro se enciende.',
 ['Identificación del filtro según el modelo','Cambio del filtro y purga','Reinicio de la luz del filtro','Revisión de mangueras y dispensador'],'Si ya cambiaste el filtro y sigue sin salir agua, puede ser la válvula o una manguera congelada.',
 [('¿Por qué no sale agua después de cambiar el filtro?','Filtro mal asentado, aire en la línea, manguera congelada o válvula; se revisa en la visita.'),('¿Cuánto dura un filtro?','Alrededor de 6 meses, según el uso.')])
linea('reparacion-de-secadoras-electricas-whirlpool-quito','Reparación de secadoras eléctricas Whirlpool en Quito','secadoras','Reparación de secadoras eléctricas Whirlpool en Quito: resistencia, termostato, ducto y 220 V. '+W+'.',
 'Muchas secadoras eléctricas usan 220 V y breaker propio. Revisamos resistencia, termostato, fusible térmico y la instalación eléctrica.',
 ['Revisión de resistencia y termostato','Revisión del voltaje y del breaker','Revisión del ducto','Prueba de ciclo'],'Si no calienta, verifica primero el breaker.',
 [('¿Necesita 220 V?','Muchas sí; la etiqueta del equipo lo indica.'),('¿Por qué no calienta?','Resistencia, termostato o fusible térmico.')])
linea('reparacion-de-secadoras-whirlpool-con-sensor-de-humedad-quito','Reparación de secadoras Whirlpool con sensor de humedad en Quito','secadoras','Reparación de secadoras Whirlpool con sensor de humedad en Quito: no secan, ciclos largos y ropa húmeda. '+W+'.',
 'Si tu secadora Whirlpool termina el ciclo con la ropa húmeda o los ciclos se alargan, el sensor de humedad, el filtro o el ducto pueden ser la causa.',
 ['Revisión y limpieza del sensor de humedad','Revisión del filtro y del ducto','Revisión de la resistencia','Prueba de ciclo'],'Si ya limpiaste el filtro y sigue igual, pide revisión.',
 [('¿Por qué no seca bien?','Filtro o ducto tapado, sensor sucio o resistencia.'),('¿Se limpia el sensor?','Sí, es parte de la revisión.')])
# ---- Nevera vs refrigeradora
add('nevera-o-refrigeradora-whirlpool-es-lo-mismo','¿Nevera o refrigeradora Whirlpool? Es lo mismo','¿Nevera o refrigeradora Whirlpool? Es lo mismo','¿Nevera o refrigeradora Whirlpool? Son el mismo electrodoméstico con distintos nombres. Cómo pedir servicio técnico en Quito. '+W+'.',['neveras','refrigeradoras'],
 'En Quito se dice refrigeradora; en otros países, nevera o refrigerador. Es el mismo equipo y lo reparamos igual: a domicilio.',
 ['Nevera, refrigeradora y refrigerador: mismo equipo','Reparamos modelos Whirlpool: congelador superior o inferior, Side by Side y French Door','Puedes pedir el servicio con cualquiera de los nombres','Diagnóstico y costo antes de reparar'],
 'Si tu equipo tiene congelador, dispensador o pantalla, también lo atendemos.',
 [('¿Qué diferencia hay entre nevera y refrigeradora?','Ninguna: son nombres regionales del mismo electrodoméstico.'),('¿Reparan ambas?','Sí, el mismo servicio aplica.')])
print(len(T))

# ---- Equipo x sector de Quito
from mq_zonas import ZD,ZSLUGS
SECT={'Norte':('el norte de Quito','norte'),'Centro':('el centro de Quito','centro'),'Sur':('el sur de Quito','sur'),'Valles':('los valles de Quito','valles')}
def _noms(sc,n=8): return [ZD[z]['nombre'] for z in ZSLUGS if ZD[z]['sector']==sc][:n]
for sc,(lab,short) in SECT.items():
    nm=', '.join(_noms(sc))
    for k,pl,art in (('lavadoras','lavadoras','la lavadora'),('secadoras','secadoras','la secadora'),('refrigeradoras','refrigeradoras','la refrigeradora'),('neveras','neveras','la nevera'),('cocinas','cocinas','la cocina'),('hornos','hornos','el horno')):
        add(f'reparacion-de-{pl}-whirlpool-en-{lab.replace("el ","").replace("los ","").replace(" de Quito","").lower()}-de-quito',
            f'Reparación de {pl} Whirlpool en {lab}',f'Reparación de {pl} Whirlpool en {lab}',
            f'Reparación de {pl} Whirlpool en {lab}: técnico a domicilio en {nm} y alrededores. '+W+'.',[k],
            f'Si vives en {lab} y {art} Whirlpool falla, el técnico va hasta tu casa o apartamento. Atendemos barrios como {nm}, entre otros.',
            [f'Visita a domicilio en {lab}',f'Revisión de {art} en su lugar de uso','Explicación de la falla y costo antes de reparar','Coordinación del día y la hora por WhatsApp'],
            f'Escríbenos tu barrio en {lab}, el modelo y la falla para confirmar la visita.',
            [(f'¿Atienden {lab}?',f'Sí, cubrimos {lab}. Escríbenos tu barrio por WhatsApp y confirmamos.'),(f'¿Reparan {pl} Whirlpool en {lab}?','Sí, a domicilio, con diagnóstico claro y costo antes de reparar.')])
# ---- Intenciones de contacto y urgencia
add('agendar-visita-de-servicio-tecnico-whirlpool-quito','Agendar visita de servicio técnico Whirlpool en Quito','Agendar visita de servicio técnico Whirlpool en Quito','Cómo agendar una visita de servicio técnico Whirlpool en Quito: qué enviar por WhatsApp y cómo se coordina. '+W+'.',['lavadoras','secadoras','refrigeradoras','neveras'],
 'Agendar la visita es simple: nos escribes por WhatsApp con el equipo, el modelo, la falla y tu barrio, y coordinamos el día y la hora.',
 ['Mensaje por WhatsApp con modelo, falla y barrio','Confirmación de cobertura en tu sector','Coordinación del día y la hora','Diagnóstico a domicilio con costo antes de reparar'],
 'Si puedes, envía una foto de la etiqueta del equipo y un video corto de la falla.',
 [('¿Cómo agendo la visita?','Escríbenos por WhatsApp o llámanos al 099 350 8191 con el modelo, la falla y tu barrio.'),('¿Puedo elegir la hora?','Coordinamos contigo la mejor hora según la disponibilidad que te confirmemos.')])
add('cotizacion-de-reparacion-de-electrodomesticos-whirlpool-quito','Cotización de reparación de electrodomésticos Whirlpool en Quito','Cotización de reparación de electrodomésticos Whirlpool','Pide la cotización de la reparación de tu electrodoméstico Whirlpool en Quito: te damos el costo antes de reparar. '+W+'.',['lavadoras','secadoras','refrigeradoras','neveras'],
 'Para cotizar la reparación primero hay que saber qué falla. Nos envías el modelo y los síntomas, y después del diagnóstico te damos el costo antes de empezar.',
 ['Orientación inicial por WhatsApp','Diagnóstico del equipo a domicilio','Costo de la reparación antes de empezar','Tú decides si continuamos'],
 'El costo exacto depende de la falla y de la pieza; por eso se confirma después del diagnóstico.',
 [('¿Cuánto cuesta reparar mi electrodoméstico?','Depende de la falla y de la pieza. Te lo confirmamos antes de reparar, después del diagnóstico.'),('¿La cotización compromete a reparar?','No: primero te explicamos y tú decides.')])
add('tecnico-whirlpool-urgente-quito','Técnico Whirlpool urgente en Quito','Técnico Whirlpool urgente en Quito','Técnico Whirlpool para urgencias en Quito: refrigeradora que no enfría, fuga de agua o falla eléctrica. Escribe por WhatsApp y confirmamos disponibilidad.',['refrigeradoras','neveras','lavadoras','secadoras'],
 'Algunas fallas no pueden esperar: una refrigeradora que deja de enfriar, una lavadora que inunda o una secadora que huele a quemado. Escríbenos y te decimos qué hacer y qué disponibilidad hay.',
 ['Orientación inmediata por WhatsApp sobre qué hacer','Confirmación de disponibilidad de visita','Revisión a domicilio','Costo confirmado antes de reparar'],
 'Si hay fuga de agua, cierra la llave y desconecta el equipo. Si huele a quemado, desconéctalo y no lo uses.',
 [('¿Atienden urgencias?','Escríbenos por WhatsApp y te confirmamos la disponibilidad para tu sector.'),('¿Qué hago mientras llega el técnico?','Desconecta el equipo si hay olor a quemado o fuga de agua y cierra la llave de agua.')])
for k,pl,art in (('lavadoras','lavadoras','la lavadora'),('secadoras','secadoras','la secadora'),('refrigeradoras','refrigeradoras','la refrigeradora'),('neveras','neveras','la nevera'),('cocinas','cocinas','la cocina'),('hornos','hornos','el horno')):
    add(f'tecnico-de-{pl}-whirlpool-urgente-quito',f'Técnico de {pl} Whirlpool urgente en Quito',f'Técnico de {pl} Whirlpool urgente en Quito',f'Técnico para urgencias de {pl} Whirlpool en Quito: escribe por WhatsApp, te orientamos y confirmamos disponibilidad. {W}.',[k],
     f'Si {art} Whirlpool dejó de funcionar de golpe, escríbenos: te indicamos qué hacer mientras tanto y confirmamos cuándo podemos ir.',
     ['Orientación inicial por WhatsApp','Confirmación de disponibilidad de visita','Diagnóstico a domicilio','Costo confirmado antes de reparar'],
     ('Si hueles a gas: cierra la llave, ventila, no uses llama ni interruptores y llama a un técnico.' if k in ('cocinas','hornos') else 'Ante olor a quemado o fuga de agua, desconecta el equipo y cierra la llave.'),
     [(f'¿Atienden urgencias de {pl}?','Escríbenos y te confirmamos la disponibilidad para tu sector.'),('¿Qué necesito enviar?','Modelo, falla y barrio; una foto o video ayuda.')])
    add(f'cotizar-reparacion-de-{pl}-whirlpool-quito',f'Cotizar la reparación de {pl} Whirlpool en Quito',f'Cotizar reparación de {pl} Whirlpool en Quito',f'Cotiza la reparación de {art} Whirlpool en Quito: diagnóstico a domicilio y costo antes de reparar. {W}.',[k],
     f'Para cotizar la reparación de {art} Whirlpool necesitamos saber qué falla. Envíanos el modelo y los síntomas y te orientamos; el costo final se confirma tras el diagnóstico.',
     ['Orientación por WhatsApp','Diagnóstico a domicilio','Costo antes de reparar','Reparación solo si tú aceptas'],
     'Cuanta más información envíes, más precisa será la orientación inicial.',
     [(f'¿Cuánto cuesta reparar {art}?','Depende de la falla y de la pieza; te lo confirmamos antes de reparar.'),('¿Cobran la visita?','Te confirmamos el costo de la visita por WhatsApp antes de ir.')])
