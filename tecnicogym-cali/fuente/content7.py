# -*- coding: utf-8 -*-
from content import PAGES,add,SEG
import content5,content6
from content5 import S,L,O,PRO
from content6 import G
N7S=[];N7G=[]
def S7(*a,**k):
    n=len(content5.NS); S(*a,**k); N7S.append(a[0])
def G7(*a,**k):
    G(*a,**k); N7G.append(a[0])
LISTA_EQ=L(['<a href="@c@">Caminadoras</a> (también llamadas trotadoras o cintas de correr).','<a href="@e@">Bicicletas de spinning</a> y estáticas.','<a href="@el@">Elípticas</a>.','<a href="@esc@">Escaladoras y steppers</a>.','<a href="@m@">Máquinas multifuncionales</a>, poleas, Smith, prensa y bancos.','Remos y bicicletas de aire.'])
S7('tecnico-de-equipos-de-gimnasio-cali','Técnico de equipos de gimnasio en Cali','Técnico de Equipos de Gimnasio en Cali | Técnico Gym',
 'Técnico de equipos de gimnasio en Cali: reparamos caminadoras, bicicletas, elípticas, escaladoras y multifuncionales a domicilio. WhatsApp 321 799 6144.',
 'Somos técnicos de equipos de gimnasio en Cali. Revisamos y reparamos tu equipo a domicilio, en casa o en el gimnasio.','wrench',
 [('Qué hace un técnico de equipos de gimnasio','<p>Un técnico de equipos de gimnasio diagnostica y repara máquinas de ejercicio: la parte mecánica (bandas, rodillos, cables, poleas, pedales), la eléctrica (motor, tarjeta, consola) y la estructural (tornillería, tapicería, estabilidad). También hace el mantenimiento que evita las fallas.</p>'),
  ('Equipos que atendemos en Cali',LISTA_EQ+'<p>Mira la lista completa en <a href="@eq@">equipos que reparamos</a>.</p>'),
  ('Dónde atendemos','<p>Atendemos en toda Cali: sur, norte, oeste, centro y oriente. Entra a la <a href="@zonas@">página de zonas</a> para ver los barrios, o escríbenos el tuyo por WhatsApp.</p>'),
  ('Para quién trabajamos',L(['Personas con equipos en casa o apartamento.','Gimnasios, estudios de spinning y boxes funcionales.','Conjuntos residenciales, hoteles, empresas y clínicas.'])),
  ('Cómo trabajamos','<p>Nos escribes por WhatsApp, te orientamos, coordinamos la visita, diagnosticamos y te informamos la falla y el costo antes de reparar. Conoce el <a href="@proceso@">proceso paso a paso</a> y todos los <a href="@serv@">servicios</a>.</p>')],
 [('¿Atienden en toda Cali?','Sí. Escríbenos tu barrio por WhatsApp y confirmamos la visita.'),('¿Reparan equipos de casa y de gimnasio?','Sí, de casa, de gimnasios, conjuntos, hoteles y empresas.')],
 ['servicios','equipos-que-reparamos','zonas-de-servicio-cali'],'Hola Técnico Gym, necesito un técnico de equipos de gimnasio en Cali. Equipo: __ Falla: __')
S7('arreglo-de-caminadoras-cali','Arreglo de caminadoras en Cali','Arreglo de Caminadoras en Cali | Técnico Gym',
 'Arreglo de caminadoras en Cali: no enciende, la banda patina, hace ruido o se apaga sola. Técnicos a domicilio. Escríbenos por WhatsApp y te orientamos.',
 'Si tu caminadora está dañada, te la arreglamos en tu casa o en tu gimnasio en Cali. Cuéntanos qué le pasa.','treadmill',
 [('Fallas que arreglamos',L(['No enciende o la consola no da señal.','Se apaga sola o pierde velocidad.','La banda patina, se corre o está desgastada.','Ruidos, vibración u olor a quemado.','La inclinación no funciona o la consola marca errores.'])+'<p>Cada falla tiene su guía: <a href="@enc@">no enciende</a>, <a href="@apaga@">se apaga sola</a>, <a href="@banda_g@">banda que patina</a>.</p>'),
  ('¿Se puede arreglar o conviene cambiarla?','<p>Depende de la falla, del costo de las piezas y del estado general. Muchas averías (banda, correa, lubricación, sensores, cables) se arreglan por una fracción de lo que cuesta una caminadora nueva. Un diagnóstico te da la respuesta. Mira <a href="@costo@">cuánto cuesta reparar una caminadora</a>.</p>'),
  ('Cómo pedir el arreglo',O(['Escríbenos por WhatsApp con la marca, el modelo y la falla.','Coordinamos la visita en Cali.','Te explicamos la falla y el costo antes de arreglar.','Probamos la caminadora al terminar.'])+PRO)],
 [('¿Arreglan caminadoras de cualquier marca?','Revisamos equipos de distintas marcas. Escríbenos la marca y el modelo y te confirmamos.')],
 ['reparacion-de-caminadoras-cali','servicio-tecnico-de-caminadoras-cali','cuanto-cuesta-reparar-una-caminadora'],'Hola Técnico Gym, necesito arreglar mi caminadora en Cali. Marca: __ Falla: __')
S7('reparacion-de-trotadoras-cali','Reparación de trotadoras en Cali','Reparación de Trotadoras en Cali | Técnico Gym',
 'Reparación de trotadoras (caminadoras o cintas de correr) en Cali: no enciende, banda, motor, consola e inclinación. Servicio a domicilio. Escríbenos por WhatsApp.',
 'Trotadora, caminadora, cinta de correr o máquina de correr: es el mismo equipo y lo reparamos en Cali, en tu casa o en tu gimnasio.','treadmill',
 [('Trotadora, caminadora o cinta de correr','<p>En Colombia se le dice de varias formas al mismo equipo: <b>caminadora</b>, <b>trotadora</b>, <b>cinta de correr</b>, <b>banda caminadora</b> o <b>máquina de correr</b>. Si tu trotadora falla, la reparación es la misma que la de una caminadora.</p>'),
  ('Fallas de trotadoras que reparamos',L(['No enciende o se apaga sola.','La banda se corre, patina o se siente pesada.','Ruidos del motor o de los rodillos.','Consola con errores o sin datos.','La inclinación no sube ni baja.','Olor a quemado (apágala y no la uses).'])),
  ('Qué debes saber al pedir la revisión','<p>Con la marca y el modelo, y una descripción de qué le pasa, te orientamos. Mira la lista de <a href="@reparacion@">reparaciones de caminadoras</a> y el <a href="@proceso@">proceso paso a paso</a>.</p>'+SEG)],
 [('¿Reparan trotadoras eléctricas y magnéticas?','Sí, atendemos las dos. Mira la diferencia entre una caminadora eléctrica y una magnética en nuestra guía.')],
 ['reparacion-de-caminadoras-cali','diferencia-entre-caminadora-electrica-y-magnetica','arreglo-de-caminadoras-cali'],'Hola Técnico Gym, necesito reparar mi trotadora en Cali. Marca: __ Falla: __')
S7('reparacion-de-maquinas-de-gimnasio-cali','Reparación de máquinas de gimnasio en Cali','Reparación de Máquinas de Gimnasio en Cali | Técnico Gym',
 'Reparación de máquinas de gimnasio en Cali: cardio y fuerza, de casa y de gimnasios. Cables, poleas, bandas, motores, consolas y tapicería. Cotiza por WhatsApp.',
 'Máquinas de cardio y de fuerza: las revisamos y las reparamos en Cali, con servicio a domicilio.','gym',
 [('Máquinas de cardio',L(['<a href="@c@">Caminadoras</a> y trotadoras.','<a href="@e@">Bicicletas de spinning</a> y estáticas.','<a href="@el@">Elípticas</a>.','<a href="@esc@">Escaladoras</a>.','Remos y bicicletas de aire.'])),
  ('Máquinas de fuerza',L(['<a href="@m@">Multifuncionales</a> y estaciones de poleas.','Máquinas Smith y prensas de piernas.','Mariposa (pec deck) y bancos de pesas.','Torres de potencia.'])+'<p>Las fallas más comunes son cables y poleas, tapicería, pila de pesas, bandas, motores, consolas y tornillería.</p>'),
  ('Cómo pedir la revisión','<p>Escríbenos por WhatsApp con el tipo de máquina, la marca y la falla. Coordinamos la visita en Cali. Mira todos los <a href="@serv@">servicios</a>.</p>')],
 [('¿Reparan máquinas de gimnasios comerciales?','Sí. Mira también el mantenimiento para gimnasios.')],
 ['tecnico-de-equipos-de-gimnasio-cali','equipos-que-reparamos','servicios'],'Hola Técnico Gym, necesito reparar una máquina de gimnasio en Cali. Máquina: __ Falla: __')
S7('reparacion-de-equipos-fitness-cali','Reparación de equipos fitness en Cali','Reparación de Equipos Fitness en Cali | Técnico Gym',
 'Reparación y mantenimiento de equipos fitness en Cali: caminadoras, bicicletas, elípticas, escaladoras y multifuncionales. Servicio técnico a domicilio.',
 'Servicio técnico para equipos fitness de casa, gimnasios y estudios en Cali.','shield',
 [('Equipos fitness que atendemos',LISTA_EQ),
  ('Servicios',L(['Diagnóstico y reparación de fallas.','<a href="@prev@">Mantenimiento preventivo</a>.','Cambio de piezas: bandas, cables, poleas, pedales, tapicería.','Revisión de equipos usados antes de comprar.'])),
  ('Para gimnasios, estudios y empresas','<p>Podemos acordar <a href="@mantenimiento@">visitas periódicas de mantenimiento</a>. Escríbenos con el número de equipos.</p>')],
 [('¿Atienden estudios de spinning, pilates o funcional?','Atendemos los equipos que reparamos en esas instalaciones. Escríbenos con el tipo de equipo.')],
 ['reparacion-de-maquinas-de-gimnasio-cali','mantenimiento-equipos-gimnasio-cali','tecnico-de-equipos-de-gimnasio-cali'],'Hola Técnico Gym, necesito servicio técnico para mis equipos fitness en Cali.')
S7('reparacion-de-maquinas-de-ejercicio-cali','Reparación de máquinas de ejercicio en Cali','Reparación de Máquinas de Ejercicio en Cali | Técnico Gym',
 'Reparación de máquinas de ejercicio para casa en Cali: caminadora, bicicleta estática, elíptica, remo y multifuncional. Técnico a domicilio. Cotiza por WhatsApp.',
 'Si tienes una máquina de ejercicio en casa y dejó de funcionar, la revisamos en tu domicilio en Cali.','gym',
 [('Máquinas de ejercicio para casa',L(['<a href="@c@">Caminadora</a> o trotadora.','Bicicleta estática o de spinning.','<a href="@el@">Elíptica</a>.','Máquina de remo.','<a href="@m@">Multifuncional</a> o multigimnasio.','Banco de pesas.'])),
  ('Qué pasa si la máquina lleva tiempo sin usarse','<p>Los equipos que se dejan guardados se llenan de polvo, se resecan y pueden fallar al volver a usarlos. Una revisión y un mantenimiento antes de retomar el ejercicio evita sorpresas.</p>'+SEG),
  ('Cómo coordinar la visita','<p>Escríbenos por WhatsApp con la máquina, la marca y la falla. Conoce el <a href="@proceso@">proceso</a>.</p>')],
 [('¿Revisan máquinas que llevan mucho tiempo guardadas?','Sí. Podemos revisarla y dejarla lista para usar.')],
 ['reparacion-equipos-gimnasio-a-domicilio-cali','equipos-que-reparamos','rutina-de-mantenimiento-mensual-de-equipos-en-casa'],'Hola Técnico Gym, necesito reparar una máquina de ejercicio en casa en Cali. Máquina: __ Falla: __')
S7('tecnico-de-equipos-de-gimnasio-cerca-de-mi-cali','Técnico de equipos de gimnasio cerca de ti en Cali','Técnico de Gimnasio Cerca de Mí en Cali | Técnico Gym',
 'Busca un técnico de equipos de gimnasio cerca de ti en Cali: vamos a tu casa o gimnasio. Escríbenos tu barrio por WhatsApp y confirmamos la visita.',
 'No tienes que llevar tu equipo a ningún lado: vamos hasta donde estás, en cualquier zona de Cali.','pin',
 [('Vamos a donde estás','<p>Atendemos a domicilio en Cali. Escríbenos tu barrio por WhatsApp y confirmamos la visita. Estas son algunas zonas desde donde nos escriben: <a href="@z_reparacion-de-caminadoras-ciudad-jardin-cali@">Ciudad Jardín</a>, <a href="@z_reparacion-de-caminadoras-pance-cali@">Pance</a>, <a href="@z_reparacion-de-caminadoras-valle-del-lili-cali@">Valle del Lili</a>, <a href="@z_reparacion-de-caminadoras-granada-cali@">Granada</a>, <a href="@z_reparacion-de-caminadoras-san-fernando-cali@">San Fernando</a> y <a href="@z_reparacion-de-caminadoras-versalles-cali@">Versalles</a>.</p>'),
  ('Cómo encontrarnos',L(['Escríbenos por WhatsApp al <b>321 799 6144</b>.','Dinos tu barrio, el equipo y la falla.','Coordinamos el día y la hora.'])+'<p>Mira todas las <a href="@zonas@">zonas de Cali</a>.</p>'),
  ('Equipos que revisamos','<p>Caminadoras, bicicletas, elípticas, escaladoras y multifuncionales. Mira la <a href="@eq@">lista completa</a>.</p>')],
 [('¿Cuánto tarda en llegar el técnico?','Depende de la zona y de la agenda. Te lo confirmamos al coordinar la visita.')],
 ['zonas-de-servicio-cali','tecnico-de-equipos-de-gimnasio-cali','reparacion-equipos-gimnasio-a-domicilio-cali'],'Hola Técnico Gym, busco un técnico de equipos de gimnasio cerca de mí en Cali. Barrio: __ Equipo: __')
S7('reparacion-de-escaladoras-stairmaster-cali','Reparación de escaladoras (stair climber) en Cali','Reparación de Escaladoras y Stairmaster en Cali | Técnico Gym',
 'Reparación de escaladoras de escalones (stair climber o stairmaster) en Cali: cadena, motor, escalones y consola. Servicio técnico a domicilio. Escríbenos.',
 'Las escaladoras de escalones giratorios trabajan con mucha carga. Las revisamos y las reparamos en gimnasios y casas de Cali.','elliptical',
 [('Cómo funciona una escaladora de escalones','<p>La escaladora de escalones (stair climber, a veces llamada stairmaster) tiene escalones que giran en un circuito, movidos por un motor y una transmisión, con pasamanos y una consola. Quien entrena sube sin avanzar, como si subiera una escalera sin fin.</p>'),
  ('Fallas que atendemos',L(['Escalones que se traban o se mueven con tirones.','Ruido de cadena, correa o rodamientos.','Motor que se calienta, se apaga o no arranca.','La velocidad no responde.','Consola sin datos o con errores.','Pasamanos o estructura con tornillería floja.'])),
  ('Mantenimiento recomendado',L(['Limpiar el polvo y el sudor de los escalones y la cubierta.','Revisar la tensión y el estado de la cadena o correa.','Comprobar la tornillería de los pasamanos.','Pedir una revisión periódica si es de gimnasio.'])+SEG),
  ('También reparamos steppers','<p>Si tu equipo es un stepper pequeño con pistones, mira la <a href="@esc@">página de escaladoras y steppers</a>.</p>')],
 [('¿Reparan escaladoras de gimnasios?','Sí, atendemos escaladoras de escalones de gimnasios y de casa en Cali.')],
 ['reparacion-escaladora-stepper-cali','mantenimiento-equipos-gimnasio-cali','reparacion-de-equipos-de-gimnasio-comercial-cali'],'Hola Técnico Gym, necesito reparar una escaladora en Cali. Marca: __ Falla: __')
S7('mantenimiento-de-equipos-crossfit-y-gimnasios-funcionales-cali','Mantenimiento de equipos para CrossFit y gimnasios funcionales en Cali','Mantenimiento de Equipos CrossFit en Cali | Técnico Gym',
 'Mantenimiento y reparación de equipos para boxes de CrossFit y gimnasios funcionales en Cali: remos, bicicletas de aire, escaladoras y más. Cotiza por WhatsApp.',
 'Los boxes y los gimnasios funcionales usan equipos de alta exigencia. Los mantenemos para que estén listos en cada clase.','gym',
 [('Equipos de box que atendemos',L(['Máquinas de remo.','Bicicletas de aire (air bike).','Escaladoras y steppers.','Caminadoras.','Bancos, torres y estructuras: revisión de tornillería y estabilidad.'])),
  ('Por qué el mantenimiento es clave en un box','<p>En clases con mucha gente y mucha carga, una cadena floja, un asiento de remo que se traba o un pedal con juego puede arruinar una clase y ser un riesgo. Un chequeo periódico reduce paradas y lesiones.</p>'),
  ('Cómo coordinarlo','<p>Escríbenos con el número de equipos y su estado. Podemos acordar <a href="@mantenimiento@">visitas periódicas</a> en el horario que menos afecte las clases.</p>')],
 [('¿Revisan estructuras y jaulas?','Revisamos tornillería, estabilidad y desgaste visible; las reparaciones estructurales se evalúan caso a caso.')],
 ['reparacion-maquina-de-remo-cali','reparacion-air-bike-cali','mantenimiento-equipos-gimnasio-cali'],'Hola Técnico Gym, quiero cotizar mantenimiento para los equipos de mi box en Cali.')
S7('reparacion-de-equipos-de-gimnasio-comercial-cali','Reparación de equipos de gimnasio comercial en Cali','Reparación de Equipos de Gimnasio Comercial en Cali | Técnico Gym',
 'Reparación y mantenimiento de equipos de gimnasio comercial en Cali: caminadoras, elípticas, spinning, escaladoras y multiestaciones de uso intensivo.',
 'Los equipos comerciales trabajan muchas horas al día. Los reparamos y los mantenemos para que el gimnasio no pierda clientes.','shield',
 [('Uso intensivo: qué cambia',L(['El desgaste es mayor: bandas, cables, poleas y rodamientos se gastan más rápido.','Una máquina dañada se nota enseguida: los usuarios se quejan.','El mantenimiento preventivo cuesta menos que las paradas.'])),
  ('Equipos comerciales que atendemos',LISTA_EQ),
  ('Servicio para gimnasios',L(['Revisión del estado de todos los equipos.','Reparación de fallas con diagnóstico previo.','<a href="@mantenimiento@">Visitas periódicas de mantenimiento</a>.'])+PRO)],
 [('¿Atienden gimnasios de todos los tamaños?','Atendemos gimnasios y estudios en Cali. Escríbenos con el número de equipos y te orientamos.')],
 ['mantenimiento-equipos-gimnasio-cali','reparacion-de-escaladoras-stairmaster-cali','mantenimiento-de-gimnasios-en-conjuntos-residenciales-cali'],'Hola Técnico Gym, quiero cotizar el mantenimiento de los equipos de mi gimnasio en Cali.')
# ---- guías locales
W=lambda t:f'Hola Técnico Gym, {t} Estoy en Cali.'
G7('clima-de-cali-y-equipos-de-gimnasio','Cómo afecta el clima de Cali a tus equipos de gimnasio','Clima de Cali y equipos de gimnasio: cuidados | Técnico Gym',
 'Calor, humedad y sudor: cómo afecta el clima de Cali a caminadoras, bicicletas y multifuncionales y qué hacer para evitar corrosión, ruidos y fallas.',
 'En una ciudad cálida como Cali, el sudor y la humedad desgastan los equipos más rápido. Estos cuidados ayudan.',
 [('Qué pasa con el calor y la humedad',L(['El sudor corrosivo ataca tornillos, marcos y tapicería.','La humedad puede afectar tarjetas y conexiones eléctricas.','El calor ambiente hace que los motores trabajen más calientes.','El polvo se pega a la grasa y a la banda.'])),
  ('Cuidados recomendados en Cali',L(['Limpia el sudor después de cada uso con un paño seco o apenas húmedo.','Ventila el lugar donde está el equipo y evita la humedad directa.','No dejes el equipo bajo goteras ni junto a ventanas con lluvia.','Revisa la tornillería con más frecuencia y busca óxido.','Haz mantenimiento preventivo periódico.'])),
  ('Cuándo pedir revisión','<p>Si ves óxido, tapicería que se deshace o la consola falla en días húmedos, pide una revisión. Mira el <a href="@prev@">mantenimiento preventivo</a>.</p>')],
 ['rutina-de-mantenimiento-mensual-de-equipos-en-casa','como-limpiar-equipos-de-gimnasio-correctamente','tecnico-de-equipos-de-gimnasio-cali'],W('quiero un mantenimiento para mis equipos.'))
G7('voltaje-y-proteccion-electrica-equipos-de-gimnasio','Voltaje y protección eléctrica para equipos de gimnasio','Voltaje y protección eléctrica de equipos de gimnasio | Técnico Gym'.replace('Voltaje y protección eléctrica de equipos de gimnasio','Protección eléctrica para equipos de gimnasio'),
 'Cómo proteger caminadoras y equipos de gimnasio de picos de tensión y apagones: regulador, polo a tierra, tomas y por qué evitar extensiones. Guía para Cali.',
 'Las variaciones de voltaje son una de las causas más comunes de tarjetas y fuentes dañadas.',
 [('El suministro eléctrico en Colombia','<p>En Colombia el suministro doméstico es de unos 110 a 120 voltios a 60 Hz. Las caminadoras y otros equipos eléctricos suelen estar diseñados para ese rango, pero los picos de tensión y los apagones pueden dañar la electrónica.</p>'),
  ('Cómo proteger tus equipos',L(['Conecta el equipo directo a un tomacorriente en buen estado, con conexión a tierra.','Evita extensiones y multitomas: se calientan con el consumo de una caminadora.','Si tu zona tiene variaciones o apagones, usa un regulador o protector adecuado a la potencia del equipo.','Desconecta el equipo si va a haber una tormenta fuerte o trabajos en la red.','Si una tormenta o un pico de tensión coincidió con la falla, avísanos.'])+SEG),
  ('Señales de problemas eléctricos',L(['El equipo se apaga al arrancar el motor.','El breaker de la casa salta.','La consola se reinicia sola.','Hay olor a quemado.'])+'<p>Mira la guía <a href="@enc@">caminadora no enciende</a> y el servicio de <a href="@tarjeta@">reparación de tarjetas</a>.</p>')],
 ['caminadora-no-enciende','reparacion-tarjeta-controladora-de-caminadora-cali','caminadora-da-corrientazos-o-descargas'],W('creo que mi equipo se dañó por un problema eléctrico.'))
G7('como-mover-o-trasladar-una-caminadora-o-multifuncional','Cómo mover o trasladar una caminadora o una multifuncional','Cómo mover una caminadora sin dañarla | Técnico Gym',
 'Guía para trasladar o mudar una caminadora, bicicleta o multifuncional sin dañarla: desconectar, asegurar, plegar y qué evitar. Consejos de técnicos en Cali.',
 'Una mudanza es una de las causas más comunes de golpes y desajustes en los equipos. Estos pasos ayudan a evitarlo.',
 [('Antes de mover el equipo',L(['Desconéctalo y recoge el cable.','Quita llaves, accesorios y objetos sueltos.','Si es plegable, plégala y asegura el pestillo.','Toma fotos de cómo está armado, sobre todo los cables.'])+SEG),
  ('Durante el traslado',L(['Muévelo entre dos o más personas, sin arrastrarlo.','Usa las ruedas de transporte de las caminadoras, si las tiene.','No lo apoyes en la consola ni en los pasamanos.','Protege tapicerías y pantallas.','En multifuncionales, asegura la pila de pesas y los cables.'])),
  ('Al llegar',O(['Ubícalo sobre una superficie firme y plana.','Nivela el equipo.','Revisa tornillería y cables.','Haz una prueba corta a baja velocidad o carga.'])+'<p>Si hay que desarmar y volver a armar un equipo grande, o notas ruidos tras el traslado, escríbenos para revisarlo.</p>')],
 ['como-ubicar-y-nivelar-una-caminadora-en-casa','reparacion-equipos-gimnasio-a-domicilio-cali','reparacion-maquinas-multifuncionales-cali'],W('movimos mi equipo y quiero una revisión.'))
G7('reparar-o-reemplazar-un-equipo-de-gimnasio','¿Reparar o reemplazar un equipo de gimnasio?','¿Reparar o reemplazar un equipo de gimnasio? | Técnico Gym',
 'Cómo decidir si conviene reparar o reemplazar una caminadora, bicicleta o multifuncional: costo de piezas, edad, estado y seguridad. Guía de técnicos en Cali.',
 'No siempre conviene reparar, ni siempre conviene comprar uno nuevo. Estos criterios te ayudan a decidir.',
 [('Conviene reparar cuando',L(['La falla es de una pieza sencilla: banda, correa, sensor, cable, pedal, tapicería.','El equipo es de buena calidad y está en buen estado general.','El costo de reparar es una parte pequeña del valor de uno nuevo equivalente.'])),
  ('Conviene reemplazar cuando',L(['La estructura está doblada o con fisuras.','Hay varias fallas graves a la vez.','Ya no hay piezas disponibles.','El costo de reparar se acerca al de uno nuevo.'])),
  ('Cómo decidir con información','<p>Un diagnóstico técnico te da el costo real y una recomendación honesta. Mira <a href="@costo@">cuánto cuesta reparar una caminadora</a> y la guía de <a href="@vida@">cuánto dura</a>.</p>')],
 ['cuanto-cuesta-reparar-una-caminadora','cuanto-dura-una-caminadora','usada-que-revisar-antes-de-comprar-una-caminadora'],W('quiero saber si vale la pena reparar mi equipo.'))
G7('que-debe-incluir-un-plan-de-mantenimiento-para-gimnasios','Qué debe incluir un plan de mantenimiento para gimnasios','Plan de mantenimiento para gimnasios: qué incluir | Técnico Gym',
 'Qué debe tener un plan de mantenimiento de equipos para un gimnasio: inventario, frecuencia, revisiones por tipo de equipo, registro y atención de fallas.',
 'Un buen plan convierte las fallas sorpresa en revisiones programadas. Esto es lo que debería tener.',
 [('Los elementos de un buen plan',L(['<b>Inventario</b> de equipos con marca, modelo y estado.','<b>Frecuencia</b> de revisión según el uso de cada equipo.','<b>Lista de revisión</b> por tipo: caminadoras, bicicletas, elípticas, multifuncionales.','<b>Registro</b> de lo que se revisó y se cambió.','<b>Atención de fallas</b> entre visitas.','<b>Reglas de uso</b> para los usuarios (peso máximo, limpieza).'])),
  ('Rutina del personal',L(['Revisión visual diaria y limpieza.','Retirar de servicio los equipos con ruido, cables dañados o fallas.','Avisar al técnico apenas aparezca un problema.'])),
  ('Cómo armarlo con un técnico','<p>Escríbenos con el número de equipos y su estado. Te orientamos sobre una frecuencia razonable. Mira el <a href="@mantenimiento@">mantenimiento para gimnasios</a>.</p>')],
 ['mantenimiento-equipos-gimnasio-cali','mantenimiento-de-gimnasios-en-conjuntos-residenciales-cali','reparacion-de-equipos-de-gimnasio-comercial-cali'],W('quiero armar un plan de mantenimiento para mi gimnasio.'))
