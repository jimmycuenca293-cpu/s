# -*- coding: utf-8 -*-
from content import PAGES,add,SEG
import content4
from content4 import GUIAS_ALL,ZS,ZN
NS=[];NB=[];NG2=[];NZ=[]
L=lambda items:'<ul>'+''.join(f'<li>{x}</li>' for x in items)+'</ul>'
O=lambda items:'<ol>'+''.join(f'<li>{x}</li>' for x in items)+'</ol>'
PRO='<p>Conoce el <a href="@proceso@">proceso paso a paso</a> o escríbenos por WhatsApp.</p>'
def S(slug,h1,title,desc,lead,icon,secs,faq,rel,wamsg):
    NS.append(slug); add(slug,kind='service',icon=icon,title=title,desc=desc,h1=h1,lead=lead,wamsg=wamsg,sections=secs,faq=faq,related=rel)
# ---------- SERVICIOS (por términos de búsqueda) ----------
S('servicio-tecnico-de-caminadoras-cali','Servicio técnico de caminadoras en Cali','Servicio Técnico de Caminadoras en Cali | Técnico Gym',
 'Servicio técnico de caminadoras en Cali: diagnóstico, reparación y mantenimiento a domicilio para casas y gimnasios. Escríbenos por WhatsApp.',
 'Un servicio técnico completo para tu caminadora: desde el diagnóstico hasta la prueba final, en tu casa o en tu gimnasio.','treadmill',
 [('Qué incluye el servicio técnico','<p>El servicio técnico de una caminadora cubre tres frentes: la revisión (diagnóstico), la reparación (correctivo) y el cuidado periódico (preventivo). Según lo que necesite tu equipo, hacemos uno o varios.</p>'),
  ('Servicios que hacemos en caminadoras',L(['<a href="@reparacion@">Reparación de caminadoras</a>: no enciende, se apaga sola, banda que patina, ruidos.','<a href="@banda@">Cambio de banda</a> y revisión de la tabla y los rodillos.','<a href="@motor@">Reparación del motor</a> y de la correa.','<a href="@tarjeta@">Reparación de tarjeta controladora</a> y de la <a href="@consola@">consola</a>.','<a href="@calibracion@">Calibración de la inclinación</a>.','<a href="@prev@">Mantenimiento preventivo</a>: limpieza, lubricación y ajustes.'])),
  ('Cuándo pedir el servicio técnico',L(['La caminadora no enciende o se apaga sola.','Hay olor a quemado, ruidos fuertes o vibración nueva.','La banda se corre, patina o se siente pesada.','La consola muestra errores o no marca datos.','Llevas meses sin hacerle mantenimiento.'])+SEG),
  ('Cómo coordinamos el servicio',O(['Nos escribes por WhatsApp con la marca, el modelo y la falla.','Te orientamos y coordinamos la visita en Cali.','Diagnosticamos y te informamos la falla y el costo antes de reparar.','Reparamos y probamos la caminadora.'])+PRO)],
 [('¿Atienden caminadoras de gimnasio?','Sí, atendemos caminadoras de casa y de gimnasios, condominios y empresas en Cali.'),('¿Qué necesito enviar?','Marca, modelo, la falla y, si puedes, una foto o un video corto.')],
 ['reparacion-de-caminadoras-cali','mantenimiento-preventivo-de-caminadoras-cali','cuanto-cuesta-reparar-una-caminadora'],'Hola Técnico Gym, necesito servicio técnico para mi caminadora en Cali. Marca: __ Falla: __')

S('mantenimiento-preventivo-de-caminadoras-cali','Mantenimiento preventivo de caminadoras en Cali','Mantenimiento Preventivo de Caminadoras en Cali | Técnico Gym',
 'Mantenimiento preventivo de caminadoras en Cali: limpieza interna, lubricación, tensión y alineación de la banda, revisión eléctrica. Para casa y gimnasios.',
 'Un mantenimiento a tiempo evita la mayoría de las fallas y alarga la vida del motor y de la banda.','shield',
 [('Qué revisamos en un mantenimiento preventivo',L(['Limpieza interna: polvo bajo la cubierta del motor y debajo de la banda.','Lubricación de la banda y la tabla, cuando el modelo lo necesita.','Tensión y alineación de la banda.','Estado de rodillos, rodamientos y correa del motor.','Revisión de la tornillería y de la estructura.','Revisión eléctrica: cable, interruptor y conexiones.','Prueba de funcionamiento a distintas velocidades y de la inclinación.'])),
  ('Cada cuánto conviene hacerlo','<p>Depende del uso. Una caminadora de casa que se usa algunas veces por semana necesita una revisión menos frecuente que una de gimnasio que trabaja varias horas al día. Como referencia, muchos fabricantes recomiendan revisar la lubricación cada tres meses o unas 150 horas de uso. Te recomendamos una frecuencia después de ver tu equipo.</p>'),
  ('Beneficios del mantenimiento preventivo',L(['Menos fallas inesperadas.','Menor desgaste de la banda y del motor.','Reparaciones más económicas, porque se detectan a tiempo.','Un equipo más silencioso y seguro.'])),
  ('Para casas y gimnasios','<p>Hacemos mantenimiento en casas y apartamentos, y podemos acordar visitas periódicas para <a href="@mantenimiento@">gimnasios, condominios y empresas</a>.</p>'+PRO)],
 [('¿Cuánto demora un mantenimiento?','Depende del equipo y de su estado. Te lo informamos al coordinar la visita.')],
 ['cada-cuanto-lubricar-una-caminadora','como-lubricar-una-caminadora-paso-a-paso','mantenimiento-equipos-gimnasio-cali'],'Hola Técnico Gym, quiero un mantenimiento preventivo para mi caminadora en Cali. Marca: __')

S('cambio-de-banda-de-caminadora-cali','Cambio de banda de caminadora en Cali','Cambio de Banda de Caminadora en Cali | Técnico Gym',
 'Cambio de banda de caminadora en Cali: cuándo hay que cambiarla, qué se revisa en la tabla y los rodillos y cómo pedir la cotización por WhatsApp.',
 'Si la banda de tu caminadora está desgastada, deshilachada o patina, la cambiamos y revisamos las piezas que la rodean.','treadmill',
 [('Cuándo hay que cambiar la banda',L(['Bordes deshilachados o con hilos sueltos.','Superficie brillante o lisa donde pisas.','Grietas, bultos o capas que se separan.','La banda está estirada y patina aunque la tensemos.'])),
  ('Qué se revisa al cambiarla','<p>Cambiar solo la banda no basta si la tabla de apoyo o los rodillos están desgastados: una banda nueva sobre una tabla gastada se daña rápido. Por eso revisamos la tabla, los rodillos, los rodamientos y la correa del motor, y te explicamos qué conviene cambiar.</p>'),
  ('Cómo se hace el cambio',O(['Revisamos el estado de la banda, la tabla y los rodillos.','Te informamos el costo y las piezas antes de empezar.','Retiramos la banda vieja y colocamos la nueva.','Alineamos, tensamos y lubricamos si el modelo lo requiere.','Probamos la caminadora a distintas velocidades.'])),
  ('Para que la banda nueva dure más',L(['Mantén la lubricación al día si tu modelo la necesita.','Limpia el polvo bajo la banda.','Usa calzado limpio.','Centra la banda cuando se corra.'])+'<p>Mira la guía <a href="@guia_desgaste@">cómo saber si la banda está desgastada</a>.</p>')],
 [('¿Cómo sé qué banda necesito?','Depende de la marca, el modelo y el ancho. Con una foto de la etiqueta del equipo podemos orientarte.'),('¿Se puede reparar la banda en vez de cambiarla?','Si la banda está deshilachada, agrietada o estirada, lo recomendable es cambiarla; reparar bordes rotos suele ser una solución temporal.')],
 ['banda-de-caminadora-patina-o-se-corre','como-saber-si-la-banda-de-la-caminadora-esta-desgastada','como-centrar-la-banda-de-una-caminadora-paso-a-paso'],'Hola Técnico Gym, necesito cambiar la banda de mi caminadora en Cali. Marca: __')

S('reparacion-motor-de-caminadora-cali','Reparación de motor de caminadora en Cali','Reparación de Motor de Caminadora en Cali | Técnico Gym',
 'Reparación de motor de caminadora en Cali: el motor no gira, huele a quemado, se calienta o suena forzado. Diagnóstico a domicilio. Escríbenos por WhatsApp.',
 'Si el motor de tu caminadora no gira, suena forzado o se calienta, lo diagnosticamos y te decimos si se repara o se reemplaza.','treadmill',
 [('Síntomas de un motor con problemas',L(['La banda no se mueve aunque la consola enciende.','Olor a quemado o a barniz caliente.','El motor se calienta mucho o la caminadora se apaga.','Ruido de roce, zumbido fuerte o vibración.','La velocidad es irregular o se traba al subir.'])),
  ('Causas frecuentes',L(['Fricción excesiva entre banda y tabla por falta de lubricación.','Correa del motor floja, desgastada o desalineada.','Desgaste de piezas internas del motor, como las escobillas en motores que las tienen.','Sobrecarga por uso intensivo.','Una falla en la tarjeta que alimenta el motor.'])),
  ('Cómo diagnosticamos','<p>Antes de hablar de cambiar el motor, descartamos las causas que lo hacen trabajar forzado: banda, tabla, rodillos y correa. Muchas veces el motor está bien y el problema es la fricción. Si el motor sí falló, te explicamos si conviene repararlo o reemplazarlo.</p>'+SEG),
  ('Qué hacer mientras tanto','<p>Si huele a quemado o el motor se calienta, apaga y desconecta la caminadora y no sigas usándola. Escríbenos con marca y modelo.</p>'+PRO)],
 [('¿Se puede reparar un motor de caminadora?','Depende del tipo de falla y de los repuestos disponibles. Se evalúa en el diagnóstico.')],
 ['caminadora-huele-a-quemado','caminadora-se-apaga-sola','como-lubricar-una-caminadora-paso-a-paso'],'Hola Técnico Gym, el motor de mi caminadora falla. Marca: __ Estoy en Cali.')

S('reparacion-tarjeta-controladora-de-caminadora-cali','Reparación de tarjeta controladora de caminadora en Cali','Reparación de Tarjeta de Caminadora en Cali | Técnico Gym',
 'Reparación de tarjeta controladora de caminadora en Cali: no enciende, no acelera, errores en consola. Diagnóstico electrónico a domicilio. Cotiza por WhatsApp.',
 'La tarjeta controladora es el cerebro de la caminadora. Si falla, el equipo puede no encender, no acelerar o mostrar errores.','treadmill',
 [('Síntomas de una tarjeta controladora dañada',L(['La caminadora no enciende o la consola no da señal.','Enciende pero la banda no arranca.','La velocidad sube sola o no responde.','La inclinación no funciona.','Se apaga de forma intermitente.','Códigos de error repetidos en la consola.'])),
  ('Por qué se dañan las tarjetas',L(['Picos o subidas de tensión y apagones.','Humedad o polvo acumulado.','Sobrecarga del motor por fricción.','Calor excesivo o desgaste de componentes.'])),
  ('Reparar o reemplazar','<p>Según el daño, una tarjeta se puede reparar o hay que reemplazarla. Te explicamos las dos opciones y el costo antes de empezar. Antes de culpar a la tarjeta, descartamos fuente, cableado, sensor y motor, que dan síntomas parecidos.</p>'+SEG),
  ('Cómo prevenir daños en la tarjeta',L(['Conecta la caminadora directo a la pared, sin extensiones.','Usa un protector o regulador de voltaje adecuado si tu zona tiene variaciones.','Mantén limpio el motor y el área de la tarjeta.','Lubrica la banda si tu modelo lo necesita.']))],
 [('¿Una subida de tensión daña la tarjeta?','Sí, es una de las causas más comunes. Si ocurrió justo antes de la falla, avísanos.')],
 ['caminadora-no-enciende','error-en-la-consola-de-la-caminadora','reparacion-consola-de-caminadora-cali'],'Hola Técnico Gym, creo que la tarjeta de mi caminadora está dañada. Marca: __ Estoy en Cali.')

S('reparacion-consola-de-caminadora-cali','Reparación de consola de caminadora en Cali','Reparación de Consola de Caminadora en Cali | Técnico Gym',
 'Reparación de consola de caminadora en Cali: pantalla sin datos, botones que no responden, errores y cableado. Diagnóstico a domicilio por WhatsApp.',
 'Pantalla apagada, botones que no responden o datos que no aparecen: revisamos la consola y su cableado.','treadmill',
 [('Fallas de consola que atendemos',L(['La pantalla no enciende o se ve a medias.','Los botones no responden o se activan solos.','No muestra velocidad, tiempo o distancia.','Muestra un código de error.','Se apaga durante el entrenamiento.'])),
  ('Qué puede estar pasando','<p>No siempre es la consola. Puede ser el cable que la conecta con la tarjeta, el sensor de velocidad, la llave de seguridad o la propia tarjeta. Por eso medimos y probamos antes de proponer un cambio de consola, que suele ser lo más costoso.</p>'),
  ('Cómo pedir la revisión',O(['Escríbenos con marca, modelo y qué muestra la consola.','Envía una foto o un video de la pantalla.','Coordinamos la visita y te explicamos la causa y el costo antes de reparar.'])+PRO)],
 [('¿Cuándo hay que cambiar la consola?','Cuando la pantalla o los botones están dañados y no hay reparación viable. Primero descartamos otras causas.')],
 ['caminadora-no-marca-velocidad-ni-datos','error-en-la-consola-de-la-caminadora','reparacion-tarjeta-controladora-de-caminadora-cali'],'Hola Técnico Gym, la consola de mi caminadora falla. Marca: __ Estoy en Cali.')

S('calibracion-de-inclinacion-de-caminadora-cali','Calibración de inclinación de caminadora en Cali','Calibración de Inclinación de Caminadora en Cali | Técnico Gym',
 'Calibración de la inclinación de caminadoras en Cali: la inclinación no sube, no baja o se queda pegada. Revisión del motor de inclinación y su cableado.',
 'Cuando la inclinación pierde la referencia o no responde, hay que calibrarla o revisar el motor que la mueve.','treadmill',
 [('Cuándo hace falta calibrar la inclinación',L(['La inclinación no sube ni baja.','Se queda en una posición.','Después de un apagón o de cambiar la consola.','Muestra un error de inclinación.','Sube más de lo que indica la pantalla.'])),
  ('Qué se revisa','<p>Revisamos el motor de inclinación y su tornillo, el cableado, el sensor de posición y la tarjeta. Si el problema es de referencia, se recalibra desde el menú de servicio del equipo; si es de motor o cableado, se repara o se reemplaza la pieza.</p>'),
  ('Qué puedes hacer tú antes','<p>Desconecta la caminadora un minuto y vuélvela a conectar. Mira la guía <a href="@guia_inc@">caminadora no sube la inclinación</a>.</p>'+SEG)],
 [('¿La calibración se puede hacer en casa?','En muchos modelos hay un procedimiento de calibración desde la consola. Si no funciona, escríbenos.')],
 ['caminadora-no-sube-la-inclinacion','error-en-la-consola-de-la-caminadora','reparacion-de-caminadoras-cali'],'Hola Técnico Gym, la inclinación de mi caminadora no funciona. Marca: __ Estoy en Cali.')

S('revision-de-equipos-de-gimnasio-usados-antes-de-comprar-cali','Revisión de equipos de gimnasio usados antes de comprar','Revisión de Equipos de Gimnasio Usados en Cali | Técnico Gym',
 'Antes de comprar una caminadora o un equipo de gimnasio usado en Cali, pide una revisión técnica. Qué se revisa y qué señales indican problemas.',
 'Comprar un equipo usado puede ser buen negocio o un dolor de cabeza. Una revisión técnica antes de pagar te dice en qué estado está.','shield',
 [('Qué se revisa en una caminadora usada',L(['Que encienda y que la banda arranque suave a todas las velocidades.','Estado de la banda: bordes, brillo, grietas.','Ruidos de motor y de rodillos.','Funcionamiento de la inclinación.','Consola: pantalla, botones y datos.','Olor a quemado y calentamiento del motor.','Estructura, tornillería y estabilidad.'])),
  ('Qué se revisa en bicicletas, elípticas y multifuncionales',L(['Pedales y manivelas sin juego.','Resistencia que cambie de forma pareja.','Monitor funcionando.','Cables y poleas en buen estado.','Tapicería y soldaduras sin fisuras.'])),
  ('Señales de alerta al comprar usado',L(['El vendedor no deja encender el equipo o probarlo.','Olor a quemado o ruidos fuertes.','Banda deshilachada o muy brillante.','Piezas faltantes o cables improvisados.'])),
  ('Cómo coordinarlo','<p>Si vas a comprar un equipo usado en Cali, escríbenos con el tipo de equipo, la marca y el lugar. Coordinamos una revisión para que decidas con información. Conoce el <a href="@proceso@">proceso</a>.</p>')],
 [('¿Puedo pedir la revisión antes de pagar?','Sí. Lo ideal es revisar el equipo antes de pagar, cuando todavía puedes negociar o decidir no comprar.')],
 ['cuanto-cuesta-reparar-una-caminadora','como-elegir-tecnico-de-equipos-de-gimnasio','usada-que-revisar-antes-de-comprar-una-caminadora'],'Hola Técnico Gym, quiero revisar un equipo usado antes de comprarlo en Cali. Equipo: __')

S('mantenimiento-de-gimnasios-en-conjuntos-residenciales-cali','Mantenimiento de gimnasios en conjuntos residenciales de Cali','Mantenimiento de Gimnasio en Conjuntos de Cali | Técnico Gym',
 'Mantenimiento y reparación de equipos del gimnasio de tu conjunto residencial en Cali: caminadoras, bicicletas, elípticas y multifuncionales. Cotiza por WhatsApp.',
 'El gimnasio del conjunto lo usan muchas personas todos los días. Un mantenimiento periódico evita que los equipos queden fuera de servicio.','shield',
 [('Para administradores y consejos de administración',L(['Revisión del estado de cada equipo y un reporte de lo que necesita.','Mantenimiento preventivo y reparación de fallas.','Visitas periódicas según el uso y el número de equipos.'])),
  ('Equipos que atendemos en gimnasios de conjuntos',L(['<a href="@c@">Caminadoras</a>.','Bicicletas de spinning y estáticas.','Elípticas.','<a href="@m@">Máquinas multifuncionales</a>, poleas y bancos.'])),
  ('Qué conviene definir con la administración',L(['Horario en que el gimnasio puede cerrarse para la visita.','Registro de ingreso del técnico en portería.','Quién autoriza las reparaciones y el presupuesto.'])),
  ('Cómo empezar','<p>Escríbenos con el nombre del conjunto, cuántos equipos hay y cuáles tienen fallas. Te orientamos y coordinamos la revisión. Mira también el <a href="@mantenimiento@">mantenimiento para gimnasios</a>.</p>')],
 [('¿Atienden conjuntos en todo Cali?','Atendemos en Cali. Escríbenos el conjunto y el barrio y confirmamos.')],
 ['mantenimiento-equipos-gimnasio-cali','mantenimiento-equipos-gimnasio-hoteles-y-empresas-cali','zonas-de-servicio-cali'],'Hola Técnico Gym, quiero cotizar el mantenimiento del gimnasio de mi conjunto en Cali. Conjunto: __ Barrio: __')

S('mantenimiento-equipos-gimnasio-hoteles-y-empresas-cali','Mantenimiento de equipos de gimnasio para hoteles y empresas en Cali','Mantenimiento de Gimnasio para Hoteles y Empresas | Técnico Gym',
 'Mantenimiento y reparación de equipos de gimnasio para hoteles, empresas y clínicas en Cali. Visitas periódicas y atención de fallas. Cotiza por WhatsApp.',
 'Para hoteles, empresas y clínicas, un equipo dañado se nota enseguida. Cuidamos tus máquinas para que estén listas cuando se usan.','shield',
 [('Qué ofrecemos',L(['Revisión de todos los equipos y reporte de su estado.','Mantenimiento preventivo periódico.','Reparación de fallas de caminadoras, bicicletas, elípticas y multifuncionales.','Atención coordinada para no interrumpir el servicio a los usuarios.'])),
  ('Por qué importa el mantenimiento en uso intensivo','<p>Los equipos de uso compartido trabajan muchas horas y reciben distintos pesos y estilos de uso. El desgaste se acumula más rápido y una falla de seguridad, como un cable deshilachado o un pedal flojo, puede causar lesiones. Un plan de revisión periódica reduce paradas y riesgos.</p>'),
  ('Cómo coordinamos',O(['Nos escribes con el tipo de establecimiento y el número de equipos.','Coordinamos una visita de revisión.','Te entregamos el estado de cada equipo y la cotización.','Acordamos la frecuencia de las visitas.'])+PRO)],
 [('¿Pueden atender fuera del horario de uso?','Podemos coordinar la visita en el horario que menos afecte a los usuarios. Lo acordamos al agendar.')],
 ['mantenimiento-equipos-gimnasio-cali','mantenimiento-de-gimnasios-en-conjuntos-residenciales-cali','como-elegir-tecnico-de-equipos-de-gimnasio'],'Hola Técnico Gym, quiero cotizar el mantenimiento de los equipos de mi empresa u hotel en Cali.')

S('retapizado-de-bancos-y-asientos-de-gimnasio-cali','Retapizado de bancos y asientos de gimnasio en Cali','Retapizado de Bancos y Asientos de Gimnasio en Cali | Técnico Gym',
 'Retapizado de bancos de pesas, asientos y respaldos de máquinas de gimnasio en Cali. Tapicería rota o espuma hundida. Cotiza por WhatsApp con una foto.',
 'Si la tapicería de tu banco o máquina está rota o la espuma hundida, la renovamos para que vuelva a ser cómoda y segura.','gym',
 [('Qué retapizamos',L(['Bancos de pesas planos, inclinados y ajustables.','Asientos y respaldos de máquinas multifuncionales.','Almohadillas de prensas, pec deck y estaciones de poleas.','Asientos de bicicletas y elípticas, según el modelo.'])),
  ('Cuándo conviene retapizar',L(['La tapicería está rota y se ve la espuma.','La espuma está hundida y no sostiene bien.','Hay costuras abiertas.','El material se cuartea o se despega.'])+'<p>Una tapicería rota deja entrar sudor y humedad a la espuma y a la estructura, y se daña cada vez más rápido.</p>'),
  ('Cómo pedir la cotización',O(['Envíanos por WhatsApp una foto del banco o de la máquina.','Indícanos las medidas aproximadas del asiento o respaldo.','Te informamos el costo y el tiempo antes de empezar.'])+PRO)],
 [('¿Puedo elegir el color?','Escríbenos y revisamos las opciones de material y color disponibles.')],
 ['reparacion-banco-de-pesas-cali','reparacion-maquinas-multifuncionales-cali','reparacion-prensa-de-piernas-cali'],'Hola Técnico Gym, quiero retapizar un banco o asiento de gimnasio en Cali. Equipo: __')

S('reparacion-de-cables-y-poleas-de-maquinas-de-gimnasio-cali','Reparación de cables y poleas de máquinas de gimnasio en Cali','Reparación de Cables y Poleas de Gimnasio en Cali | Técnico Gym',
 'Cambio y reparación de cables, poleas y pila de pesas de máquinas de gimnasio y multifuncionales en Cali. Servicio a domicilio. Cotiza por WhatsApp.',
 'Cables deshilachados, poleas que rechinan o una pila de pesas que se traba: lo revisamos y lo reparamos antes de que falle con carga.','gym',
 [('Fallas en cables y poleas',L(['Cable deshilachado, estirado o aplastado.','Poleas que rechinan, se salen del cable o tienen juego.','Pila de pesas que se traba o sube con tirones.','Pin selector flojo o desgastado.','Agarres, barras y mosquetones con desgaste.'])),
  ('Por qué no esperar','<p>El cable soporta la carga cada vez que levantas peso. Si ves hilos sueltos, déjalo de usar y pide la revisión: un cable que falla con carga puede lastimar a quien entrena.</p>'+SEG),
  ('Qué hacemos',O(['Revisamos cables, poleas y recorrido de toda la máquina.','Te explicamos qué piezas se cambian y el costo.','Cambiamos cables y poleas, lubricamos las guías y ajustamos.','Probamos la máquina con carga.'])),
  ('Máquinas donde aplica',L(['<a href="@m@">Multifuncionales</a>.','Estaciones de poleas, jalón y polea baja.','Máquina mariposa o pec deck.','Máquinas de pila de pesas de gimnasios.']))],
 [('¿Cada cuánto se cambia un cable?','Depende del uso. Lo importante es revisarlo con frecuencia y cambiarlo si tiene hilos sueltos o deformación.')],
 ['reparacion-estacion-de-poleas-cali','reparacion-maquinas-multifuncionales-cali','reparacion-maquina-mariposa-pec-deck-cali'],'Hola Técnico Gym, necesito cambiar un cable o una polea de mi máquina en Cali. Equipo: __')

# ---------- MARCAS (las de las fotos) ----------
AV='<p><b>Aviso:</b> Técnico Gym es un servicio técnico independiente. No somos distribuidores ni centro de servicio autorizado de esta marca; su nombre se usa solo para indicar los equipos que atendemos.</p>'
def B(slug,marca,h1,title,desc,lead,equipos,fallas,rel,gal=None):
    NB.append(slug); add(slug,kind='marca',icon='wrench',title=title,desc=desc,h1=h1,lead=lead,wamsg=f'Hola Técnico Gym, necesito reparar un equipo {marca} en Cali. Modelo: __ Falla: __',
      sections=[(f'Equipos {marca} que atendemos',equipos),('Fallas frecuentes',L(fallas)),('Cómo pedir la revisión',O([f'Escríbenos por WhatsApp con el modelo de tu equipo {marca} y qué falla presenta.','Si puedes, envía una foto de la etiqueta con el modelo y un video del problema.','Coordinamos la visita en Cali y te informamos la falla y el costo antes de reparar.'])+PRO),('Importante',AV)],
      faq=[(f'¿Son servicio autorizado de {marca}?','No. Somos un servicio técnico independiente en Cali. Reparamos y damos mantenimiento a equipos de distintas marcas.'),(f'¿Qué necesito enviar para equipos {marca}?','El modelo del equipo (suele estar en una etiqueta), la falla y, si puedes, una foto o un video corto.')],related=rel)
B('reparacion-equipos-ultimate-fitness-cali','Ultimate Fitness','Reparación de equipos Ultimate Fitness en Cali','Reparación de Equipos Ultimate Fitness en Cali | Técnico Gym',
 'Reparación de caminadoras, elípticas y multifuncionales Ultimate Fitness en Cali. Servicio técnico independiente a domicilio. Escríbenos por WhatsApp con el modelo.',
 'Atendemos caminadoras, elípticas y máquinas multifuncionales Ultimate Fitness en Cali: no encienden, ruidos, consola, banda y más.',
 L(['<a href="@c@">Caminadoras</a> con pantalla táctil y consola.','<a href="@el@">Elípticas</a> con consola y resistencia.','<a href="@m@">Máquinas multifuncionales</a> con pila de pesas y poleas.']),
 ['Caminadora que no enciende o se apaga sola.','Banda que patina, se corre o hace ruido.','Pantalla táctil o consola con fallas.','Elíptica con crujidos, juego en los pedales o resistencia que no cambia.','Multifuncional con cables deshilachados, poleas que rechinan o pila de pesas trabada.'],
 ['reparacion-de-caminadoras-cali','reparacion-eliptica-cali','reparacion-maquinas-multifuncionales-cali'])
B('reparacion-equipos-centurfit-cali','Centurfit','Reparación de caminadoras Centurfit en Cali','Reparación de Caminadoras Centurfit en Cali | Técnico Gym',
 'Reparación de caminadoras Centurfit en Cali, incluidas las comerciales tipo Titan: consola, banda, motor y amortiguación. Servicio independiente a domicilio.',
 'Atendemos caminadoras Centurfit, incluidas las comerciales como la Titan: banda, motor, consola y amortiguación.',
 L(['<a href="@c@">Caminadoras</a> comerciales y de gimnasio con consola grande y banda ancha.','Caminadoras de uso intensivo en gimnasios y condominios.']),
 ['Consola con fallas o que no marca datos.','Banda que patina, se corre o hace ruido.','Motor que se calienta o se apaga bajo carga.','Desgaste de la amortiguación bajo la banda.','Mantenimiento de equipos de uso intensivo en gimnasios.'],
 ['reparacion-de-caminadoras-cali','servicio-tecnico-de-caminadoras-cali','mantenimiento-preventivo-de-caminadoras-cali'])
B('reparacion-equipos-evolution-fitness-cali','Evolution Fitness','Reparación de bicicletas de spinning Evolution Fitness en Cali','Reparación de Bicicletas Evolution Fitness en Cali | Técnico Gym',
 'Reparación de bicicletas de spinning y estáticas Evolution Fitness en Cali: pedales, transmisión, resistencia y monitor. Servicio independiente a domicilio.',
 'Atendemos bicicletas de spinning y estáticas Evolution Fitness, de casa y de gimnasio: pedales, resistencia, transmisión y monitor.',
 L(['<a href="@e@">Bicicletas de spinning</a> de gimnasio con volante pesado.','Bicicletas de spinning y estáticas para casa con monitor.']),
 ['Ruido o crujido al pedalear.','Pedales o manivelas con juego.','Resistencia que no frena o no cambia.','Asiento o manillar que se aflojan.','Monitor sin datos.'],
 ['reparacion-bicicletas-spinning-cali','reparacion-bicicleta-estatica-cali','bicicleta-spinning-hace-ruido'])
B('reparacion-equipos-sportfitness-cali','Sportfitness','Reparación de multifuncionales Sportfitness en Cali','Reparación de Multifuncionales Sportfitness en Cali | Técnico Gym',
 'Reparación de máquinas multifuncionales Sportfitness en Cali: cables, poleas, pila de pesas, tapicería. Servicio técnico independiente a domicilio.',
 'Atendemos máquinas multifuncionales Sportfitness con pila de pesas: cables, poleas, guías, agarres y tapicería.',
 L(['<a href="@m@">Multifuncionales</a> de casa con pila de pesas, jalón y polea.','Bancos y accesorios de la máquina.']),
 ['Cables deshilachados o estirados.','Poleas que rechinan o se salen.','Pila de pesas trabada o con tirones.','Tapicería rota o espuma hundida.','Tornillería floja y estructura con juego.'],
 ['reparacion-maquinas-multifuncionales-cali','reparacion-de-cables-y-poleas-de-maquinas-de-gimnasio-cali','retapizado-de-bancos-y-asientos-de-gimnasio-cali'])
