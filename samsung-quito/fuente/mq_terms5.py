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
for k,pl,art in (('lavadoras','lavadoras','la lavadora'),('secadoras','secadoras','la secadora'),('refrigeradoras','refrigeradoras','la refrigeradora'),('neveras','neveras','la nevera')):
    add(f'centro-de-servicio-de-{pl}-samsung-quito',f'Centro de servicio de {pl} Samsung en Quito',f'Centro de servicio de {pl} Samsung en Quito',
      f'Centro de servicio de {pl} Samsung en Quito: técnico a domicilio para reparar y dar mantenimiento sin que muevas el equipo. {W}.',[k],
      f'Si buscas un centro de servicio de {pl} Samsung en Quito, hay una forma más cómoda: el técnico va a tu casa, revisa {art} en su lugar y te explica la falla antes de reparar.',
      ['Diagnóstico a domicilio, sin trasladar el equipo','Reparación y mantenimiento en tu casa o apartamento','Costo confirmado antes de reparar','Atención en norte, centro, sur y valles de Quito'],
      'Mientras el equipo esté en garantía de fábrica, consulta primero sus condiciones con el fabricante. Fuera de garantía, la visita a domicilio suele ser lo más práctico.',
      [(f'¿Tengo que llevar {art} a un centro de servicio?','No necesariamente: la mayoría de las reparaciones se hacen en casa. Escríbenos y te orientamos.'),('¿Cómo pido la visita?',f'Por WhatsApp o llamada al {PHONE_TXT}, con el modelo, la falla y tu barrio.')])
# ---- Marca / generales
add('soporte-tecnico-samsung-quito','Soporte técnico Samsung en Quito','Soporte técnico Samsung en Quito','Soporte técnico Samsung en Quito para lavadoras, secadoras, neveras y refrigeradoras: orientación por WhatsApp y visita a domicilio. '+W+'.',['lavadoras','secadoras','refrigeradoras','neveras'],
 'Si necesitas soporte técnico Samsung en Quito, empezamos por WhatsApp: nos cuentas la falla, te orientamos y, si hace falta, coordinamos la visita a domicilio.',
 ['Orientación inicial por WhatsApp con foto y video','Visita técnica a domicilio en Quito','Diagnóstico claro y costo antes de reparar','Seguimiento hasta que el equipo quede funcionando'],
 'Escríbenos con el modelo y la falla; cuanto más información, más precisa es la orientación.',
 [('¿Qué necesito para recibir soporte?','Marca y modelo, descripción de la falla, tu barrio y, si puedes, una foto de la etiqueta y un video corto.'),('¿El soporte incluye visita?','La orientación inicial es por WhatsApp; el diagnóstico definitivo se hace en el equipo, a domicilio.')])
add('servicio-tecnico-samsung-ecuador-quito','Servicio técnico Samsung Ecuador: atención en Quito','Servicio técnico Samsung Ecuador: atención en Quito','Servicio técnico Samsung en Ecuador con atención a domicilio en Quito y sus valles: lavadoras, secadoras, neveras y refrigeradoras. '+W+'.',['lavadoras','secadoras','refrigeradoras','neveras'],
 'Si buscas servicio técnico Samsung en Ecuador y vives en Quito o sus valles, atendemos a domicilio: lavadoras, secadoras, neveras y refrigeradoras.',
 ['Cobertura en norte, centro, sur y valles de Quito','Visita a domicilio coordinada por WhatsApp','Diagnóstico y costo antes de reparar','Mantenimiento e instalación'],
 'Para otras ciudades de Ecuador, escríbenos y te decimos si podemos atender tu zona.',
 [('¿Atienden solo Quito?','Nuestra cobertura es Quito y sus valles; para otras zonas, consúltanos por WhatsApp.'),('¿Qué equipos Samsung reparan?','Lavadoras, secadoras, neveras y refrigeradoras.')])
add('samsung-quito-servicio-tecnico-y-reparacion','Samsung Quito: servicio técnico y reparación de electrodomésticos','Samsung Quito: servicio técnico y reparación','Samsung Quito: servicio técnico y reparación a domicilio de lavadoras, secadoras, neveras y refrigeradoras Samsung. '+W+'.',['lavadoras','secadoras','refrigeradoras','neveras'],
 'Si buscas Samsung en Quito para reparar un electrodoméstico, aquí encuentras servicio técnico Samsung Quito a domicilio, con diagnóstico claro y costo antes de reparar.',
 ['Lavadoras, secadoras, neveras y refrigeradoras Samsung','Cobertura en norte, centro, sur y valles','Coordinación por WhatsApp','Costo confirmado antes de reparar'],
 'Esta página resume qué hacemos; cada equipo y cada barrio tiene su propia información.',
 [('¿Qué es Servicio Técnico Samsung Quito?','Un servicio técnico a domicilio para electrodomésticos Samsung en Quito: diagnóstico, reparación y mantenimiento.'),('¿Qué marcas reparan?','Nos enfocamos en Samsung.')])
add('que-incluye-la-visita-de-servicio-tecnico-samsung-en-quito','Qué incluye la visita de servicio técnico Samsung en Quito','Qué incluye la visita de servicio técnico Samsung','Qué incluye la visita de servicio técnico Samsung en Quito: diagnóstico, explicación de la falla, costo antes de reparar y prueba final. '+W+'.',['lavadoras','refrigeradoras'],
 'Antes de pedir la visita conviene saber qué incluye: revisamos el equipo, te explicamos la falla y te damos el costo antes de reparar.',
 ['Revisión del equipo y pruebas de la falla','Explicación clara de la causa','Costo de la reparación antes de empezar','Prueba de funcionamiento al terminar'],
 'Si no conviene reparar, también te lo decimos.',
 [('¿Pagan la visita aunque no repare?','Escríbenos y te confirmamos el costo de la visita antes de ir.'),('¿Puedo decidir después del diagnóstico?','Sí, primero te explicamos y tú decides si continuamos.')])
# ---- Líneas de producto
LAV=('lavadoras','la lavadora'); REF=('refrigeradoras','la refrigeradora')
def linea(slug,h1,k,desc,intro,inc,cuando,faq): add(slug,h1,h1,desc,[k],intro,inc,cuando,faq)
linea('reparacion-de-lavadoras-samsung-ecobubble-quito','Reparación de lavadoras Samsung EcoBubble en Quito','lavadoras','Reparación de lavadoras Samsung EcoBubble en Quito: espuma, desagüe, ruidos y códigos de error. Visita a domicilio. '+W+'.',
 'Las lavadoras Samsung con EcoBubble mezclan aire, agua y detergente para generar burbujas. Si la tuya hace espuma de más, no desagua o muestra un código de error, la revisamos en tu casa.',
 ['Revisión del desagüe y del sistema de llenado','Revisión de espuma y dosificación de detergente','Lectura del código de error','Prueba de ciclo'],'Si notas exceso de espuma, olor o ciclos que no terminan, pide una revisión.',
 [('¿Por qué mi lavadora hace tanta espuma?','Detergente en exceso o no apto para lavadoras; también puede haber un problema de desagüe.'),('¿Qué hago si muestra un código?','Anótalo y escríbenos con el modelo.')])
linea('reparacion-de-lavadoras-samsung-addwash-quito','Reparación de lavadoras Samsung AddWash en Quito','lavadoras','Reparación de lavadoras Samsung AddWash en Quito: puerta pequeña que gotea, no abre o no cierra. Visita a domicilio. '+W+'.',
 'AddWash es la puertita de las lavadoras Samsung que permite agregar ropa durante el ciclo. Si gotea, no abre o no cierra bien, la revisamos a domicilio.',
 ['Revisión del sello y del seguro de AddWash','Revisión de la puerta principal','Prueba de fuga con ciclo de agua','Ajuste o cambio de piezas si hace falta'],'No abras AddWash en pleno desagüe si ves agua; escríbenos si gotea.',
 [('¿AddWash puede gotear?','Sí, por sello desgastado, suciedad o cierre mal ajustado.'),('¿Se repara en casa?','Normalmente sí, a domicilio.')])
linea('reparacion-de-lavadoras-samsung-digital-inverter-quito','Reparación de lavadoras Samsung Digital Inverter en Quito','lavadoras','Reparación de lavadoras Samsung con motor Digital Inverter en Quito: ruidos, vibración y fallas al centrifugar. '+W+'.',
 'Muchas lavadoras Samsung usan motor Digital Inverter. Si la tuya hace ruidos nuevos, vibra o no centrifuga, revisamos motor, amortiguadores y tarjeta.',
 ['Revisión del motor y de las conexiones','Revisión de amortiguadores y nivelación','Prueba de centrifugado','Lectura del código de error'],'Un ruido nuevo al centrifugar merece revisión antes de que se dañe algo más.',
 [('¿Por qué hace ruido al centrifugar?','Carga desbalanceada, amortiguadores o rodamientos; se confirma en la revisión.'),('¿Se puede reparar el motor?','Depende del caso; lo confirmamos en el diagnóstico.')])
linea('reparacion-de-refrigeradoras-samsung-family-hub-quito','Reparación de refrigeradoras Samsung Family Hub en Quito','refrigeradoras','Reparación de refrigeradoras Samsung Family Hub en Quito: pantalla, conexión, cámaras interiores y falla de frío. '+W+'.',
 'Las refrigeradoras Family Hub tienen pantalla táctil y funciones conectadas. Si la pantalla se congela, no conecta o la refrigeradora no enfría bien, la revisamos a domicilio.',
 ['Revisión de la pantalla y de la conexión','Revisión del sistema de frío','Prueba de dispensador y hielo','Recomendaciones de uso'],'Si la pantalla falla pero la refrigeradora enfría, no hay urgencia; si deja de enfriar, escríbenos pronto.',
 [('¿La pantalla Family Hub se puede reparar?','Depende de la causa; se confirma en el diagnóstico.'),('¿Por qué no conecta a la app?','Router, señal o configuración; revisa que el router esté en 2.4 GHz y reinicia ambos.')])
linea('reparacion-de-refrigeradoras-samsung-french-door-quito','Reparación de refrigeradoras Samsung French Door en Quito','refrigeradoras','Reparación de refrigeradoras Samsung French Door en Quito: frío, hielo, dispensador y escarcha. Visita a domicilio. '+W+'.',
 'Las refrigeradoras French Door (dos puertas arriba y cajón de congelador abajo) tienen varios sistemas. Revisamos frío, descongelación, hielo y dispensador en tu cocina.',
 ['Revisión del frío en ambas zonas','Revisión de descongelación y ventiladores','Revisión de hielo y dispensador','Prueba de temperatura'],'Pide la revisión si no enfría parejo, hay escarcha o gotea agua.',
 [('¿Por qué el cajón del congelador se llena de escarcha?','Sello, descongelación o ventilador; se confirma en la visita.'),('¿Reparan el dispensador?','Sí: filtro, manguera y válvula.')])
linea('reparacion-de-refrigeradoras-samsung-twin-cooling-plus-quito','Reparación de refrigeradoras Samsung Twin Cooling Plus en Quito','refrigeradoras','Reparación de refrigeradoras Samsung Twin Cooling Plus en Quito: frío desparejo, escarcha y ruidos. '+W+'.',
 'Twin Cooling Plus es el sistema de enfriamiento independiente de refrigerador y congelador en muchas Samsung. Si una zona enfría mal, hay escarcha o ruidos, la revisamos.',
 ['Revisión de evaporadores y ventiladores','Revisión de sensores y tarjeta','Prueba de temperatura por zona','Recomendaciones de uso'],'Si una zona no enfría pero la otra sí, pide revisión.',
 [('¿Por qué enfría una zona y la otra no?','Ventilador, escarcha o sensor; se confirma en la visita.'),('¿Es urgente?','Si pierdes frío en la zona de alimentos, sí: escríbenos pronto.')])
linea('reparacion-de-refrigeradoras-samsung-digital-inverter-quito','Reparación de refrigeradoras Samsung Digital Inverter en Quito','refrigeradoras','Reparación de refrigeradoras Samsung con compresor Digital Inverter en Quito: ruidos, vibración y falla de frío. '+W+'.',
 'El compresor Digital Inverter ajusta su velocidad según la necesidad de frío. Si la refrigeradora hace zumbidos, vibra o no enfría, revisamos compresor, ventilador y tarjeta.',
 ['Revisión del compresor y de su arranque','Revisión de ventiladores y nivelación','Revisión de la tarjeta de control','Prueba de funcionamiento'],'Un zumbido nuevo y constante puede avisar una falla.',
 [('¿Es normal que cambie de ruido?','El inverter varía la velocidad; un ruido fuerte o nuevo sí merece revisión.'),('¿Se repara en casa?','Normalmente sí.')])
linea('reparacion-de-neveras-samsung-side-by-side-quito','Reparación de neveras Samsung Side by Side en Quito','neveras','Reparación de neveras Samsung Side by Side en Quito: frío, hielo, dispensador y ruidos. Visita a domicilio. '+W+'.',
 'Las neveras Side by Side (dos puertas verticales) tienen dispensador y fábrica de hielo. Las revisamos a domicilio en Quito.',
 ['Revisión del frío en ambas puertas','Revisión del dispensador y del hielo','Revisión de descongelación','Prueba de temperatura'],'Son equipos grandes: mejor que el técnico vaya a tu casa.',
 [('¿Reparan el dispensador de agua?','Sí: filtro, manguera y válvula.'),('¿Por qué hay escarcha?','Descongelación o sello de puerta.')])
linea('reparacion-de-neveras-samsung-family-hub-quito','Reparación de neveras Samsung Family Hub en Quito','neveras','Reparación de neveras Samsung Family Hub en Quito: pantalla, conexión y falla de frío. Visita a domicilio. '+W+'.',
 'Si tu nevera Samsung Family Hub tiene la pantalla congelada, no conecta o no enfría, la revisamos a domicilio en Quito.',
 ['Revisión de pantalla y conexión','Revisión del sistema de frío','Prueba del dispensador','Recomendaciones de uso'],'Si deja de enfriar, escríbenos pronto.',
 [('¿Reparan la pantalla?','Depende de la causa; lo confirmamos en el diagnóstico.'),('¿Y la conexión a SmartThings?','Te orientamos con la configuración y revisamos el equipo.')])
linea('reparacion-de-neveras-samsung-french-door-quito','Reparación de neveras Samsung French Door en Quito','neveras','Reparación de neveras Samsung French Door en Quito: frío, hielo y escarcha. Visita a domicilio. '+W+'.',
 'Las neveras French Door tienen congelador tipo cajón. Revisamos frío, descongelación, hielo y dispensador en tu cocina.',
 ['Revisión del frío','Revisión de descongelación y ventiladores','Revisión de hielo y dispensador','Prueba de temperatura'],'Pide la revisión si no enfría parejo o gotea agua.',
 [('¿Por qué gotea agua?','Desagüe de descongelación tapado o congelado.'),('¿Es urgente?','Si no enfría, sí.')])
linea('reparacion-de-secadoras-samsung-con-sensor-de-humedad-quito','Reparación de secadoras Samsung con sensor de humedad en Quito','secadoras','Reparación de secadoras Samsung con sensor de humedad en Quito: no secan, ciclos largos y ropa húmeda. '+W+'.',
 'Si tu secadora Samsung termina el ciclo con la ropa húmeda o los ciclos se alargan, el sensor de humedad, el filtro o el ducto pueden ser la causa.',
 ['Revisión y limpieza del sensor de humedad','Revisión del filtro y del ducto','Revisión de la resistencia','Prueba de ciclo'],'Si ya limpiaste el filtro y sigue igual, pide revisión.',
 [('¿Por qué no seca bien?','Filtro o ducto tapado, sensor sucio o resistencia.'),('¿Se limpia el sensor?','Sí, es parte de la revisión.')])
linea('reparacion-de-secadoras-electricas-samsung-quito','Reparación de secadoras eléctricas Samsung en Quito','secadoras','Reparación de secadoras eléctricas Samsung en Quito: resistencia, termostato, ducto y 220 V. '+W+'.',
 'Muchas secadoras eléctricas usan 220 V y breaker propio. Revisamos resistencia, termostato, fusible térmico y la instalación eléctrica.',
 ['Revisión de resistencia y termostato','Revisión del voltaje y del breaker','Revisión del ducto','Prueba de ciclo'],'Si no calienta, verifica primero el breaker.',
 [('¿Necesita 220 V?','Muchas sí; la etiqueta del equipo lo indica.'),('¿Por qué no calienta?','Resistencia, termostato o fusible térmico.')])
# ---- Códigos de error (lavadoras)
def cod(slug,h1,k,desc,intro,inc,cuando,faq): add(slug,h1,h1,desc,[k],intro,inc,cuando,faq)
cod('lavadora-samsung-codigo-le-lc-fuga-de-agua-quito','Lavadora Samsung código LE o LC: fuga de agua','lavadoras','Lavadora Samsung con código LE o LC en Quito: qué indica, qué revisar y cuándo llamar al técnico. '+W+'.',
 'En muchas lavadoras Samsung, LE o LC indica una posible fuga o agua donde no debería haber. El significado exacto puede variar por modelo.',
 ['Cierra la llave de agua y desconecta la lavadora','Revisa mangueras, filtro de desagüe y piso','Anota el código exacto y el modelo','Pide diagnóstico si el código vuelve'],'No sigas usándola si hay fuga: puedes dañar el piso o la instalación eléctrica.',
 [('¿Qué significa LE o LC?','Suele relacionarse con una fuga o detección de agua; varía por modelo.'),('¿Puedo reiniciarla?','Puedes intentar, pero si reaparece, requiere revisión.')])
cod('lavadora-samsung-codigo-he-hc-calentador-quito','Lavadora Samsung código HE o HC: problema del calentador','lavadoras','Lavadora Samsung con código HE o HC en Quito: posible falla de calentamiento. Qué revisar. '+W+'.',
 'HE o HC suele asociarse con la función de calentar el agua. El significado exacto depende del modelo; por eso conviene anotar el código y el modelo.',
 ['Prueba un ciclo con agua fría','Anota el código y el modelo','No fuerces el equipo','Pide diagnóstico a domicilio'],'Si el código persiste, escríbenos con el modelo.',
 [('¿Puedo seguir lavando?','Con agua fría quizá sí; consulta antes de forzar el equipo.'),('¿Qué se revisa?','Resistencia, sensor y tarjeta, según el modelo.')])
cod('lavadora-samsung-sud-exceso-de-espuma-quito','Lavadora Samsung muestra SUD: exceso de espuma','lavadoras','Lavadora Samsung con SUD o SUDS en Quito: exceso de espuma, detergente y qué hacer. '+W+'.',
 'SUD (o SUDS) suele indicar exceso de espuma. Casi siempre es detergente en exceso o no apto para lavadoras.',
 ['Usa menos detergente y de baja espuma','Haz un enjuague extra sin ropa','Revisa que el desagüe no esté tapado','Pide revisión si se repite'],'Si repite aun con poca cantidad de detergente, revisa el desagüe.',
 [('¿Por qué hace tanta espuma?','Detergente en exceso o de lavado a mano.'),('¿Daña la lavadora?','La espuma excesiva puede afectar desagüe y sensores.')])
cod('secadora-samsung-codigo-hc-he-calefaccion-quito','Secadora Samsung código HC o HE: problema de calefacción','secadoras','Secadora Samsung con código HC o HE en Quito: posible falla de calefacción. Qué revisar. '+W+'.',
 'En algunas secadoras Samsung, HC o HE se asocia con la calefacción. El significado exacto varía por modelo.',
 ['Limpia el filtro y revisa el ducto','Verifica el breaker (220 V en muchos modelos)','Anota el código y el modelo','Pide diagnóstico'],'Si hay olor a quemado, desconéctala y no la uses.',
 [('¿Por qué no calienta?','Resistencia, termostato o ducto tapado.'),('¿Es peligroso?','Un ducto tapado y sobrecalentamiento sí; apágala y revisa.')])
# ---- Nevera vs refrigeradora
add('nevera-o-refrigeradora-samsung-es-lo-mismo','¿Nevera o refrigeradora Samsung? Es lo mismo','¿Nevera o refrigeradora Samsung? Es lo mismo','¿Nevera o refrigeradora Samsung? Son el mismo electrodoméstico con distintos nombres. Cómo pedir servicio técnico en Quito. '+W+'.',['neveras','refrigeradoras'],
 'En Quito se dice refrigeradora; en otros países, nevera o refrigerador. Es el mismo equipo y lo reparamos igual: a domicilio.',
 ['Nevera, refrigeradora y refrigerador: mismo equipo','Reparamos modelos Samsung: Top Mount, Side by Side, French Door y Family Hub','Puedes pedir el servicio con cualquiera de los nombres','Diagnóstico y costo antes de reparar'],
 'Si tu equipo tiene congelador, dispensador o pantalla, también lo atendemos.',
 [('¿Qué diferencia hay entre nevera y refrigeradora?','Ninguna: son nombres regionales del mismo electrodoméstico.'),('¿Reparan ambas?','Sí, el mismo servicio aplica.')])
print(len(T))
