# -*- coding: utf-8 -*-
from content import PAGES,add,SEG,GUIAS
import content2,content3
# ------------ GUÍAS NUEVAS ------------
NG=[]
def g(slug,**k):
    NG.append(slug); add(slug,kind='guia',faq=k.pop('faq',[]),**k)

g('caminadora-no-sube-la-inclinacion',
 title='Caminadora no sube la inclinación: causas | Técnico Gym',
 desc='La inclinación de tu caminadora no sube ni baja o se queda pegada. Causas comunes (motor de inclinación, calibración, cableado) y cuándo llamar al técnico en Cali.',
 h1='Caminadora no sube la inclinación: causas y qué hacer',
 lead='Si la inclinación no responde o se queda en una posición, casi siempre se trata de calibración, del motor de inclinación o de su cableado.',
 wamsg='Hola Técnico Gym, la inclinación de mi caminadora no sube. Marca: __ Estoy en Cali.',
 sections=[('Cómo funciona la inclinación','<p>En las caminadoras con inclinación eléctrica, un pequeño motor con un tornillo sinfín sube o baja la parte delantera de la plataforma. La tarjeta controladora recibe la posición y calcula el movimiento. Cuando algo falla, la consola puede mostrar un error o simplemente no responder.</p>'),
 ('Causas más comunes','<ul><li><b>Falta de calibración:</b> tras un apagón o un cambio de consola, la caminadora pierde la referencia de posición.</li><li><b>Motor de inclinación:</b> desgaste o falla del motor o del tornillo.</li><li><b>Cableado o conectores:</b> un cable suelto o dañado entre la tarjeta y el motor.</li><li><b>Tarjeta controladora:</b> una falla electrónica.</li></ul>'),
 ('Qué puedes revisar tú','<ol><li>Desconecta la caminadora, espera un minuto y vuelve a conectarla: algunas hacen una recalibración al encender.</li><li>Revisa el manual: muchos modelos tienen un procedimiento de calibración desde la consola.</li><li>Comprueba que nada bloquee la parte delantera de la plataforma.</li></ol>'+SEG),
 ('Cuándo llamar al técnico','<p>Si después de recalibrar la inclinación sigue sin responder, si se oye el motor pero no hay movimiento o si hay un error persistente en la consola, escríbenos con marca y modelo.</p>')],
 related=['error-en-la-consola-de-la-caminadora','reparacion-de-caminadoras-cali','caminadora-no-enciende'])

g('caminadora-no-marca-velocidad-ni-datos',
 title='Caminadora no marca velocidad ni datos: causas | Técnico Gym',
 desc='La consola de tu caminadora no muestra velocidad, tiempo o distancia. Causas comunes (sensor, imán, cableado, consola) y qué revisar antes de llamar al técnico.',
 h1='La caminadora no marca velocidad ni datos',
 lead='Si la banda se mueve pero la consola no muestra velocidad, tiempo o distancia, el problema suele ser el sensor de velocidad, su cableado o la consola.',
 wamsg='Hola Técnico Gym, mi caminadora no marca velocidad ni datos. Marca: __ Estoy en Cali.',
 sections=[('Cómo mide la velocidad una caminadora','<p>La mayoría de las caminadoras usan un pequeño sensor (a menudo magnético) junto al rodillo delantero que cuenta las vueltas. La tarjeta convierte esas vueltas en velocidad y distancia. Si el sensor falla o se desalinea, la consola puede mostrar cero, datos erráticos o un error.</p>'),
 ('Causas más comunes','<ul><li>El sensor o el imán del rodillo están desalineados o sueltos.</li><li>Cable del sensor flojo, pellizcado o roto.</li><li>La tarjeta controladora no lee la señal.</li><li>La consola tiene una falla en la pantalla o en el cableado.</li></ul>'),
 ('Qué puedes revisar tú','<ol><li>Con la caminadora desconectada, revisa que el cable del sensor no esté suelto ni aplastado.</li><li>Verifica si la banda se mueve a una velocidad normal aunque la pantalla no la muestre.</li><li>Anota si la pantalla muestra algún código.</li></ol>'+SEG),
 ('Cuándo llamar al técnico','<p>Si la velocidad sigue sin aparecer o la caminadora acelera sola, deja de usarla y escríbenos: un sensor que no informa bien puede hacer que el equipo funcione sin control.</p>')],
 related=['error-en-la-consola-de-la-caminadora','caminadora-no-enciende','reparacion-de-caminadoras-cali'])

g('error-en-la-consola-de-la-caminadora',
 title='Error en la consola de la caminadora: qué significa | Técnico Gym',
 desc='La consola de tu caminadora muestra un código de error. Qué significa en general, cómo anotarlo y qué hacer antes de llamar a un técnico en Cali.',
 h1='Error en la consola de la caminadora: qué significa',
 lead='Los códigos de error cambian de una marca a otra, pero casi siempre apuntan a una de pocas causas. Estos pasos te ayudan a reunir la información correcta.',
 wamsg='Hola Técnico Gym, mi caminadora muestra un error en la consola: __. Marca: __ Estoy en Cali.',
 sections=[('Por qué no hay una lista universal de códigos','<p>Cada fabricante usa sus propios códigos (E1, E2, E06, Er, entre otros) y el mismo código puede significar cosas distintas según la marca. Por eso lo más útil es anotar el código exacto, la marca y el modelo, y no buscar en una lista genérica.</p>'),
 ('Las causas más frecuentes detrás de un código','<ul><li><b>Sensor de velocidad:</b> no recibe señal.</li><li><b>Llave de seguridad:</b> no está puesta o se soltó.</li><li><b>Motor o tarjeta:</b> sobrecarga o sobrecalentamiento.</li><li><b>Inclinación:</b> pérdida de calibración.</li><li><b>Comunicación:</b> cable entre consola y tarjeta.</li></ul>'),
 ('Qué hacer','<ol><li>Anota el código tal como aparece y en qué momento salió (al encender, al subir velocidad, al inclinar).</li><li>Apaga, desconecta un minuto y vuelve a conectar.</li><li>Comprueba la llave de seguridad.</li><li>Si el código vuelve, tómale una foto y escríbenos.</li></ol>'+SEG),
 ('Qué información enviar','<p>El código, la marca, el modelo y una descripción de qué estabas haciendo cuando apareció.</p>')],
 related=['caminadora-no-sube-la-inclinacion','caminadora-no-marca-velocidad-ni-datos','reparacion-de-caminadoras-cali'])

g('caminadora-huele-a-quemado',
 title='Caminadora huele a quemado: qué hacer de inmediato | Técnico Gym',
 desc='Si tu caminadora huele a quemado, apágala y desconéctala. Causas posibles (banda, motor, correa, tarjeta) y por qué no debes seguir usándola.',
 h1='Caminadora que huele a quemado: qué hacer',
 lead='Un olor a quemado es una señal de alerta. Lo primero es apagar y desconectar el equipo.',
 wamsg='Hola Técnico Gym, mi caminadora huele a quemado. Marca: __ Estoy en Cali.',
 sections=[('Qué hacer en el momento','<ol><li>Apaga la caminadora y desconéctala de la pared.</li><li>No la vuelvas a encender para "probar".</li><li>Si hay humo o chispas, aleja a las personas y no la manipules.</li></ol>'),
 ('Causas posibles','<ul><li><b>Fricción de la banda:</b> banda seca o muy tensa que calienta la tabla y el motor.</li><li><b>Correa del motor patinando:</b> huele a caucho caliente.</li><li><b>Motor sobrecargado:</b> huele a barniz o aislante caliente.</li><li><b>Tarjeta o cableado:</b> huele a plástico o a componente electrónico quemado.</li></ul>'),
 ('Por qué no debes seguir usándola','<p>Seguir usando una caminadora que huele a quemado puede dañar el motor o la tarjeta, y en el peor caso provocar un incendio. Es mejor que un técnico revise la causa antes de volver a usarla.</p>'+SEG),
 ('Qué datos enviarnos','<p>Marca y modelo, cuándo apareció el olor (al encender, con la banda en movimiento, tras mucho rato), y si la banda patinaba o se oía forzada.</p>')],
 related=['caminadora-se-apaga-sola','banda-de-caminadora-patina-o-se-corre','reparacion-de-caminadoras-cali'])

g('como-centrar-la-banda-de-una-caminadora-paso-a-paso',
 title='Cómo centrar la banda de una caminadora paso a paso | Técnico Gym',
 desc='Guía paso a paso para centrar la banda de una caminadora que se corre a un lado: herramientas, ajuste de los tornillos traseros y errores que debes evitar.',
 h1='Cómo centrar la banda de una caminadora, paso a paso',
 lead='Si la banda se desplaza hacia un lado, puedes corregirla con ajustes pequeños en los tornillos traseros. Hazlo con cuidado y revisa el manual de tu modelo.',
 wamsg='Hola Técnico Gym, necesito ayuda con la banda de mi caminadora que se corre. Marca: __ Estoy en Cali.',
 sections=[('Antes de empezar','<ul><li>Necesitas la llave Allen (hexagonal) que suele venir con la caminadora.</li><li>Ubícate a un lado, no sobre la banda, mientras la ajustas.</li><li>Revisa el manual: el sentido de giro puede variar según el fabricante.</li></ul>'+SEG),
 ('Paso a paso','<ol><li><b>Enciende la caminadora a baja velocidad</b> (alrededor de 3 a 4 km/h), sin nadie encima.</li><li><b>Observa hacia dónde se desplaza la banda</b> en la parte trasera: izquierda o derecha.</li><li><b>Localiza los dos tornillos de ajuste</b> en los extremos de la parte trasera.</li><li><b>Haz un ajuste pequeño, de un cuarto de vuelta,</b> en el tornillo del lado hacia el que se desplaza. En la mayoría de los modelos, girar ese tornillo en sentido horario tensa ese lado y la banda se mueve hacia el centro; confirma el sentido en tu manual.</li><li><b>Espera uno o dos minutos</b> y observa si la banda se centró.</li><li><b>Repite con otro cuarto de vuelta</b> solo si hace falta.</li><li><b>Comprueba la tensión:</b> la banda no debe patinar al caminar sobre ella.</li></ol>'),
 ('Errores que debes evitar','<ul><li>Girar los tornillos más de un cuarto de vuelta de una sola vez.</li><li>Apretar demasiado: una banda muy tensa fuerza el motor y los rodamientos.</li><li>Ajustar con la caminadora apagada y esperar que se vea el resultado.</li></ul>'),
 ('Si no se centra','<p>Si después de varios ajustes la banda sigue corriéndose, puede haber desgaste de la banda, un rodillo desalineado o la estructura desnivelada. Escríbenos con marca y modelo.</p>')],
 related=['banda-de-caminadora-patina-o-se-corre','como-lubricar-una-caminadora-paso-a-paso','reparacion-de-caminadoras-cali'])

g('como-lubricar-una-caminadora-paso-a-paso',
 title='Cómo lubricar una caminadora paso a paso | Técnico Gym',
 desc='Cómo lubricar la banda de una caminadora paso a paso: cuándo hacerlo, qué lubricante usar, cuánto aplicar y errores que dañan la banda.',
 h1='Cómo lubricar una caminadora, paso a paso',
 lead='Lubricar la banda reduce la fricción con la tabla y alarga la vida del motor. Antes de hacerlo, confirma que tu modelo lo necesita.',
 wamsg='Hola Técnico Gym, quiero un mantenimiento y lubricación para mi caminadora en Cali. Marca: __',
 sections=[('Antes de empezar: ¿necesita lubricación?','<p>Algunas caminadoras vienen con la banda lubricada de fábrica y no necesitan lubricación periódica; otras sí. Mira el manual o busca una etiqueta de lubricación. Si tienes dudas, no apliques nada y escríbenos con marca y modelo.</p>'),
 ('Qué necesitas','<ul><li>Lubricante a base de silicona recomendado para caminadoras.</li><li>Paño limpio.</li></ul><p>No uses aceites ni aerosoles a base de petróleo: pueden dañar la banda.</p>'),
 ('Paso a paso','<ol><li>Apaga y desconecta la caminadora.</li><li>Levanta con cuidado un lado de la banda y limpia con un paño el polvo de la tabla.</li><li>Aplica el lubricante en forma de zigzag o en una línea a lo largo de la tabla, entre la banda y la tabla, siguiendo las indicaciones del producto.</li><li>Repite por el otro lado si el producto lo indica.</li><li>Baja la banda, conecta la caminadora y hazla funcionar a baja velocidad unos minutos para que se reparta el lubricante.</li><li>Limpia cualquier exceso.</li></ol>'+SEG),
 ('Cada cuánto','<p>Sigue el manual. Como referencia general, muchos fabricantes recomiendan revisarla cada tres meses o unas 150 horas de uso.</p>'),
 ('Cuándo pedir mantenimiento','<p>Si la banda se siente pesada, el motor suena forzado o la tabla está desgastada, es mejor que un técnico revise el conjunto.</p>')],
 related=['cada-cuanto-lubricar-una-caminadora','como-centrar-la-banda-de-una-caminadora-paso-a-paso','mantenimiento-equipos-gimnasio-cali'])

g('como-saber-si-la-banda-de-la-caminadora-esta-desgastada',
 title='¿La banda de la caminadora está desgastada? | Técnico Gym',
 desc='Señales de que la banda de tu caminadora está desgastada y hay que cambiarla: bordes deshilachados, brillo, grietas y patinaje. Cuándo llamar al técnico.',
 h1='Cómo saber si la banda de la caminadora está desgastada',
 lead='La banda es la pieza que más se desgasta. Estas son las señales de que ya toca cambiarla.',
 wamsg='Hola Técnico Gym, creo que la banda de mi caminadora está desgastada. Marca: __ Estoy en Cali.',
 sections=[('Señales de desgaste','<ul><li><b>Bordes deshilachados</b> o con hilos sueltos.</li><li><b>Superficie brillante o lisa</b> en la zona donde pisas.</li><li><b>Grietas o separación de capas.</b></li><li><b>Estiramiento:</b> la banda no se puede tensar sin que patine.</li><li><b>Bultos o zonas hundidas.</b></li></ul>'),
 ('Por qué se desgasta','<p>El uso constante, la falta de lubricación, el polvo bajo la banda, el calzado sucio y el peso o la velocidad por encima de lo recomendado aceleran el desgaste. También influye si la caminadora está desnivelada.</p>'),
 ('¿Se puede seguir usando?','<p>Con bordes deshilachados o grietas, no. La banda puede romperse o engancharse. Déjala de usar y pide la revisión.</p>'),
 ('Cómo prolongar la vida de la banda','<ul><li>Mantén la lubricación al día si tu modelo la necesita.</li><li>Limpia el polvo bajo la banda con el equipo desconectado.</li><li>Usa calzado limpio.</li><li>Centra la banda cuando se corra.</li></ul>')],
 related=['banda-de-caminadora-patina-o-se-corre','como-lubricar-una-caminadora-paso-a-paso','reparacion-de-caminadoras-cali'])

g('bicicleta-estatica-no-marca-o-sin-resistencia',
 title='Bicicleta estática no marca o sin resistencia | Técnico Gym',
 desc='Tu bicicleta estática no marca datos o la resistencia no funciona. Causas comunes (pilas, sensor, perilla, imán) y qué revisar antes de llamar al técnico.',
 h1='Bicicleta estática que no marca o no tiene resistencia',
 lead='Si el monitor no muestra datos o la resistencia no cambia, suele ser algo sencillo de revisar.',
 wamsg='Hola Técnico Gym, mi bicicleta estática no marca datos o no tiene resistencia. Marca: __ Estoy en Cali.',
 sections=[('El monitor no marca','<ol><li>Cambia las pilas por unas nuevas.</li><li>Revisa que el cable del monitor esté bien conectado en la base.</li><li>Comprueba que el imán del volante o de la manivela esté alineado con el sensor.</li></ol>'),
 ('La resistencia no cambia','<ul><li><b>Perilla o cable:</b> el cable puede estar suelto o estirado.</li><li><b>Imán:</b> desalineado o suelto.</li><li><b>Motor de resistencia (en modelos con consola):</b> no responde.</li><li><b>Pastilla de fricción (en spinning):</b> desgastada.</li></ul>'+SEG),
 ('Cuándo llamar al técnico','<p>Si cambiaste las pilas y revisaste los cables y el monitor o la resistencia siguen sin funcionar, escríbenos con marca y modelo.</p>')],
 related=['reparacion-bicicleta-estatica-cali','bicicleta-spinning-hace-ruido','reparacion-bicicletas-spinning-cali'])

g('eliptica-hace-ruido',
 title='Elíptica hace ruido: causas y qué revisar | Técnico Gym',
 desc='Tu elíptica hace ruido, cruje o golpetea. Causas (tornillería, pivotes, rodamientos, pedales) y qué revisar antes de llamar al técnico en Cali.',
 h1='La elíptica hace ruido: causas y qué revisar',
 lead='Una elíptica tiene muchas uniones móviles, así que un ruido casi siempre viene de una pieza floja o seca.',
 wamsg='Hola Técnico Gym, mi elíptica hace ruido. Marca: __ Estoy en Cali.',
 sections=[('Ubica el ruido','<ul><li><b>Crujido al pedalear:</b> tornillería o pivotes flojos.</li><li><b>Golpeteo en cada vuelta:</b> bujes o rodamientos con holgura.</li><li><b>Chirrido:</b> falta de lubricación en un pivote.</li><li><b>Ruido que viene de la base:</b> la elíptica está desnivelada.</li></ul>'),
 ('Qué revisar','<ol><li>Aprieta la tornillería de pedales, brazos y estructura.</li><li>Comprueba que la elíptica esté nivelada.</li><li>Revisa si hay holgura moviendo con la mano los brazos y pedales (con el equipo detenido).</li></ol>'+SEG),
 ('Cuándo llamar al técnico','<p>Si el ruido sigue después de apretar y nivelar, o si notas juego en un pedal o brazo, escríbenos.</p>')],
 related=['reparacion-eliptica-cali','bicicleta-spinning-hace-ruido','reparacion-escaladora-stepper-cali'])

g('como-ubicar-y-nivelar-una-caminadora-en-casa',
 title='Cómo ubicar y nivelar una caminadora en casa | Técnico Gym',
 desc='Dónde poner la caminadora en casa y cómo nivelarla: espacio libre, piso, toma de corriente y ventilación. Evita ruidos, vibración y desgaste.',
 h1='Cómo ubicar y nivelar una caminadora en casa',
 lead='Una buena ubicación y una caminadora bien nivelada evitan ruidos, vibración y desgaste temprano.',
 wamsg='Hola Técnico Gym, quiero una revisión de mi caminadora en casa en Cali. Marca: __',
 sections=[('Dónde ubicarla','<ul><li>Sobre un piso firme y plano, no sobre alfombras gruesas.</li><li>Con espacio libre detrás (como referencia, un par de metros) para poder bajarte con seguridad.</li><li>Cerca de una toma de corriente en buen estado, sin extensiones.</li><li>En un lugar ventilado y lejos de la humedad.</li></ul>'),
 ('Cómo nivelarla paso a paso','<ol><li>Coloca la caminadora en su lugar definitivo.</li><li>Pon un nivel de burbuja (o la aplicación de nivel del celular) sobre la plataforma.</li><li>Gira las patas niveladoras traseras hasta que quede pareja.</li><li>Comprueba que no se mueva al empujarla con la mano.</li><li>Haz una prueba corta a baja velocidad y revisa que la banda no se corra ni haga ruido.</li></ol>'),
 ('Qué evitar','<ul><li>Ponerla sobre una superficie blanda: se desnivela y vibra.</li><li>Taparla con ropa o dejar el polvo acumulado bajo el motor.</li><li>Moverla sin desconectarla ni levantar el cable.</li></ul>')],
 related=['como-centrar-la-banda-de-una-caminadora-paso-a-paso','ruido-en-la-caminadora','reparacion-de-caminadoras-cali'])

GUIAS_ALL=GUIAS+NG
# ------------ CÓMO TRABAJAMOS ------------
add('como-trabajamos',kind='info',icon='wrench',
 title='Cómo trabajamos: reparación paso a paso | Técnico Gym',
 desc='Así es el proceso de Técnico Gym en Cali: contacto por WhatsApp, diagnóstico, cotización antes de reparar, reparación y prueba final de tu equipo de gimnasio.',
 h1='Cómo trabajamos, paso a paso',
 lead='Queremos que sepas qué va a pasar desde que nos escribes hasta que tu equipo queda funcionando. Este es el proceso.',
 wamsg='Hola Técnico Gym, quiero coordinar la revisión de mi equipo de gimnasio en Cali.',
 sections=[
 ('Paso 1. Nos escribes por WhatsApp','<p>Escríbenos al <b>321 799 6144</b>. Cuéntanos qué equipo es, la marca, el modelo y qué falla presenta. No necesitas saber de técnica: con describir lo que pasa es suficiente.</p>'),
 ('Paso 2. Nos envías la información clave','<ul><li>Tipo de equipo (caminadora, bicicleta, elíptica, multifuncional…).</li><li>Marca y modelo (suele estar en una etiqueta o en la consola).</li><li>Qué falla presenta y desde cuándo.</li><li>Una foto o un video corto del problema o del ruido.</li><li>Tu barrio en Cali.</li></ul>'),
 ('Paso 3. Te orientamos','<p>Con esos datos te damos una primera orientación sobre la causa más probable y te decimos si es algo que puedes revisar tú o si conviene la visita. Si es peligroso seguir usando el equipo, también te lo avisamos.</p>'),
 ('Paso 4. Coordinamos la visita','<p>Acordamos el día y la hora en tu casa, gimnasio o conjunto. Si vives en un conjunto cerrado o un edificio, avísanos si hay que registrar el ingreso y si el equipo está en un piso alto.</p>'),
 ('Paso 5. Diagnóstico en el lugar','<p>El técnico revisa el equipo: seguridad, parte eléctrica, parte mecánica y pruebas de funcionamiento. Identifica la causa real de la falla y no solo el síntoma.</p>'),
 ('Paso 6. Cotización antes de reparar','<p>Te explicamos qué falla tiene el equipo, qué piezas hacen falta y cuánto cuesta, antes de empezar. Tú decides si apruebas la reparación.</p>'),
 ('Paso 7. Reparación','<p>Si apruebas, hacemos la reparación. Si se puede resolver en la visita, lo hacemos ahí; si requiere una pieza o llevar el equipo al taller, te lo explicamos y coordinamos.</p>'),
 ('Paso 8. Prueba final','<p>Probamos el equipo en funcionamiento, con carga y a distintas velocidades o niveles, para confirmar que quedó bien.</p>'),
 ('Paso 9. Recomendaciones de cuidado','<p>Te explicamos cómo mantener el equipo para que dure más: limpieza, lubricación según el manual, ubicación y uso.</p>'),
 ('Qué puedes hacer tú para agilizar el proceso','<ul><li>Tener a mano la marca y el modelo.</li><li>Dejar libre el espacio alrededor del equipo.</li><li>Tener una toma de corriente accesible.</li><li>Enviar un video corto del problema.</li></ul>'),
 ('Seguridad','<p>Mientras esperas la visita, no sigas usando un equipo con olor a quemado, chispas, cables dañados o ruidos fuertes.</p>'+SEG),
 ],
 faq=[('¿Cuánto demora una reparación?','Depende de la falla y de si hay que conseguir una pieza. Si se resuelve en la visita, el mismo día; si no, te informamos el tiempo estimado.'),('¿Cobran la visita?','Te informamos las condiciones al coordinar la visita, antes de ir.'),('¿Qué pasa si no apruebo la reparación?','Es tu decisión. Te explicamos la falla y el costo y puedes decidir con calma.')],
 related=['reparacion-equipos-gimnasio-a-domicilio-cali','equipos-que-reparamos','preguntas-frecuentes'])

# ------------ ZONAS (subpáginas locales) ------------
ZN=[
('ciudad-jardin','Ciudad Jardín','sur','Ciudad Jardín es una zona residencial del sur de Cali, con casas, conjuntos y edificios de apartamentos.','Ciudad Jardín, Limonar, Caney, El Ingenio y barrios cercanos','En conjuntos y edificios del sector es habitual que el gimnasio o la zona de ejercicio esté en un piso o en una zona común.'),
('pance','Pance','sur','Pance es una zona del sur de Cali con casas campestres, condominios y conjuntos, donde muchos hogares tienen un espacio de ejercicio propio.','Pance, Cuarto de Legua, Capri y alrededores','En zonas campestres y con clima más cálido y húmedo, conviene limpiar el sudor y secar los equipos para evitar la corrosión.'),
('valle-del-lili','Valle del Lili','sur','Valle del Lili es una zona del sur de Cali con conjuntos residenciales y edificios de apartamentos.','Valle del Lili, Ciudad 2000, Cañasgordas y barrios cercanos','En conjuntos cerrados de la zona suele pedirse registrar el ingreso del técnico con anticipación.'),
('canasgordas','Cañasgordas','sur','Cañasgordas es una zona residencial del sur de Cali con conjuntos cerrados y casas.','Cañasgordas, Pance, Gran Limonar y alrededores','Si tu equipo está en una casa de varios pisos, avísanos para llevar lo necesario.'),
('ciudad-2000','Ciudad 2000','sur','Ciudad 2000 es un sector residencial del sur de Cali.','Ciudad 2000, Caney, Valle del Lili y alrededores','Si vives en un conjunto cerrado, cuéntanos el nombre para coordinar el ingreso.'),
('granada','Granada','norte','Granada es una zona del norte de Cali con edificios de apartamentos, oficinas y restaurantes.','Granada, Juanambú, San Fernando y alrededores','En edificios de apartamentos conviene preguntar a la administración si hay un horario para el ingreso de técnicos y si hay ascensor de carga.'),
('versalles','Versalles','norte','Versalles es una zona residencial del norte de Cali, con casas y edificios.','Versalles, Santa Mónica, Prados del Norte y alrededores','Si tu equipo está en un segundo piso o en una terraza, avísanos al coordinar la visita.'),
('chipichape','Chipichape','norte','Chipichape es una zona del norte de Cali, con conjuntos y edificios de apartamentos cerca de zonas comerciales.','Chipichape, Vipasa, La Flora, Menga y alrededores','Muchas viviendas de la zona son apartamentos, donde el espacio libre para la caminadora es limitado.'),
('santa-monica','Santa Mónica','norte','Santa Mónica es una zona residencial del norte de Cali.','Santa Mónica, Versalles, La Flora y alrededores','Avísanos si el edificio o conjunto exige autorizar el ingreso del técnico.'),
('san-fernando','San Fernando','centro','San Fernando es un barrio tradicional del centro-sur de Cali, con casas y edificios.','San Fernando, Tequendama, Centenario y alrededores','En casas antiguas conviene revisar que la instalación eléctrica soporte el consumo del equipo.'),
('normandia','Normandía','oeste','Normandía es una zona residencial del oeste de Cali.','Normandía, Santa Teresita, San Antonio y alrededores','Si el equipo está en una casa con escaleras, avísanos para ir preparados.'),
]
ZS=[]
for slug,nom,pt,desc,cerca,tip in ZN:
    s='reparacion-de-caminadoras-'+slug+'-cali'; ZS.append(s)
    add(s,kind='zona',icon='pin',
     title=f'Reparación de Caminadoras en {nom}, Cali | Técnico Gym',
     desc=f'Técnico de caminadoras y equipos de gimnasio en {nom}, Cali. Reparación a domicilio de caminadoras, bicicletas y multifuncionales. WhatsApp.',
     h1=f'Reparación de caminadoras y equipos de gimnasio en {nom}, Cali',
     lead=f'Atendemos a domicilio en {nom} y alrededores. Escríbenos la marca, el modelo y la falla de tu equipo y coordinamos la visita.',
     wamsg=f'Hola Técnico Gym, necesito reparar un equipo de gimnasio en {nom}, Cali. Equipo: __ Falla: __',
     sections=[(f'Servicio a domicilio en {nom}',f'<p>{desc} Si tienes una caminadora, una bicicleta o cualquier equipo de gimnasio en casa que falle, vamos hasta tu domicilio, revisamos el equipo y te explicamos qué necesita.</p><p>{tip}</p>'),
      ('Equipos que reparamos en la zona','<ul><li><a href="@c@">Caminadoras</a> (no encienden, banda que patina, ruidos, se apagan solas).</li><li><a href="@e@">Bicicletas de spinning y estáticas</a>.</li><li><a href="@m@">Máquinas multifuncionales</a>, estaciones de poleas, banco de pesas y más.</li></ul><p>Mira todos los <a href="@eq@">equipos que reparamos</a>.</p>'),
      ('Barrios cercanos que atendemos',f'<p>{cerca}. Si no ves tu barrio, escríbenos y lo confirmamos.</p>'),
      ('Cómo coordinamos la visita','<p>Nos escribes por WhatsApp, te orientamos sobre la falla, acordamos el día y la hora, y el técnico revisa el equipo en tu casa. Te informamos la falla y el costo antes de reparar. Conoce el <a href="@proceso@">proceso paso a paso</a>.</p>')],
     faq=[(f'¿Atienden en {nom}?',f'Sí. Atendemos en {nom} y barrios cercanos. Escríbenos tu barrio por WhatsApp y coordinamos la visita.'),(f'¿Qué debo avisar si vivo en un conjunto o edificio de {nom}?','El nombre del conjunto o edificio, el piso y si hay que registrar el ingreso con anticipación.')],
     related=['zonas-de-servicio-cali','reparacion-equipos-gimnasio-a-domicilio-cali','como-trabajamos'])

# enlaces a las páginas de zona dentro de la página general de zonas
PAGES['zonas-de-servicio-cali']['sections'].insert(0,('Páginas por zona','<p>Elige tu zona para ver cómo coordinamos la visita:</p><ul>'+''.join(f'<li><a href="@z_{z}@">{PAGES[z]["h1"].split(" en ")[-1]}</a></li>' for z in ZS)+'</ul>'))

PAGES['equipos-que-reparamos']=dict(slug='equipos-que-reparamos',kind='hub',h1='Equipos de gimnasio que reparamos en Cali',lead='Caminadoras, bicicletas, elípticas, remos, escaladoras, multifuncionales, bancos y más equipos para hacer ejercicio en casa.',sections=[],faq=[],related=[],wamsg='Hola Técnico Gym, quiero saber si reparan mi equipo.')
