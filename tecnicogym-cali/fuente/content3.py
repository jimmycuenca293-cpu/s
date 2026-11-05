# -*- coding: utf-8 -*-
from content import PAGES,add,SEG
# Cada máquina: (slug, nombre, plural-corto, icono, grupo, intro, fallas[(t,d)], mant[], senales[], faq[(q,a)], corto, rel[])
M=[]
def mq(**k): M.append(k)

mq(slug='reparacion-bicicleta-estatica-cali',n='bicicleta estática',g='Cardio',ic='bike',corto='ruidos al pedalear, resistencia que no cambia, asiento que se baja y monitor sin datos',
 intro='<p>La bicicleta estática vertical es una de las máquinas más comunes en casas y apartamentos. Tiene un volante de inercia, un sistema de resistencia (por perilla, imán o motor), pedales con manivelas, asiento regulable y un monitor. Como se usa muchas veces por semana y recibe sudor, sus fallas suelen aparecer por desgaste o por tornillería floja.</p>',
 fallas=[('Ruido o crujido al pedalear','pedales flojos, manivelas con juego, pedalier o rodamientos desgastados.'),('La resistencia no cambia','perilla o cable de resistencia, imán desalineado o motor de resistencia que no responde.'),('El asiento se baja o se mueve','pomo de ajuste desgastado, tubo con holgura o tornillos flojos.'),('Monitor sin datos o que se apaga','pilas, cableado, sensor de cadencia o conector suelto.'),('Transmisión','correa o cadena floja, desgastada o desalineada.'),('Inestabilidad','patas niveladoras desajustadas y estructura con tornillos flojos.')],
 mant=['Limpia el sudor del marco y del manillar después de entrenar: es corrosivo.','Aprieta pedales, asiento y manillar cada mes.','Si la transmisión es por cadena, mantenla limpia y lubricada.','Cambia las pilas del monitor antes de que se agoten del todo.','Guárdala en un lugar seco y nivelada.'],
 senales=['Ruido nuevo que se repite en cada vuelta del pedal.','Juego en las manivelas o los pedales.','La resistencia se siente irregular.','El asiento no sostiene la altura.'],
 faq=[('¿Cuál es la diferencia con una bicicleta de spinning?','La estática de casa suele tener un volante más liviano y más comodidades, como asiento y monitor. La de spinning es más robusta, con volante pesado y se usa en posición más inclinada.'),('¿Se puede reparar el monitor?','Depende del modelo. Revisamos pila, cableado y sensor; si el monitor está dañado, se evalúa cambiarlo.')],
 rel=['reparacion-bicicletas-spinning-cali','reparacion-bicicleta-reclinada-cali','bicicleta-estatica-no-marca-o-sin-resistencia'])

mq(slug='reparacion-bicicleta-reclinada-cali',n='bicicleta reclinada',g='Cardio',ic='bike',corto='asiento que se traba, ruido en el riel, resistencia y monitor',
 intro='<p>La bicicleta reclinada tiene un asiento con respaldo y los pedales al frente, lo que reduce la carga en la espalda y las articulaciones. Por eso es muy usada en casas con personas mayores o en procesos de recuperación. Su asiento se desliza sobre un riel, y ahí suelen aparecer los problemas.</p>',
 fallas=[('El asiento no desliza o se traba','riel sucio, rodillos desgastados o tornillería floja.'),('Ruido al pedalear','pedales, manivelas o pedalier con juego.'),('El respaldo se mueve o cruje','tornillos del respaldo y soportes flojos.'),('Resistencia que no cambia','perilla, cable o motor de resistencia.'),('Monitor sin datos','pila, cableado o sensor.')],
 mant=['Limpia el riel del asiento con un paño seco.','Revisa que el asiento quede bien trabado antes de pedalear.','Aprieta la tornillería del respaldo.','Lubrica solo lo que indique el manual.'],
 senales=['El asiento se desplaza solo mientras pedaleas.','Ruido que viene del riel.','Juego en el respaldo.'],
 faq=[('¿Es seguro usarla si el asiento se mueve?','No. Un asiento que se desliza mientras pedaleas puede causar caídas. Déjala de usar hasta revisarla.')],
 rel=['reparacion-bicicleta-estatica-cali','reparacion-bicicletas-spinning-cali','bicicleta-estatica-no-marca-o-sin-resistencia'])

mq(slug='reparacion-maquina-de-remo-cali',n='máquina de remo',g='Cardio',ic='gym',corto='ruido en el riel, correa o cadena, manija, resistencia y monitor',
 intro='<p>La máquina de remo trabaja casi todo el cuerpo y es cada vez más común en casas. Según el tipo de resistencia puede ser <b>de aire</b> (con un ventilador), <b>magnética</b>, <b>de agua</b> o <b>hidráulica</b> (con pistones). Todas tienen un riel por el que se desliza el asiento, una manija con cuerda, correa o cadena, y un monitor.</p>',
 fallas=[('Ruido o saltos del asiento','riel sucio, rodillos del carro desgastados o tornillería floja.'),('Cuerda, correa o cadena','estiramiento, deshilachado o desalineación.'),('Resistencia irregular','ventilador sucio o dañado (aire), imán (magnética) o pistones con fuga (hidráulica).'),('Monitor sin datos o con datos erróneos','sensor, cableado o pila.'),('Reposapiés flojos','tornillos y soportes.'),('Estructura','patas niveladoras y uniones con holgura.')],
 mant=['Limpia el riel del asiento con un paño después de entrenar.','Revisa la cuerda, correa o cadena y reemplázala si está deshilachada.','Aspira el polvo de la jaula del ventilador en las de aire.','Guárdala en vertical si el modelo lo permite.','Sigue las indicaciones de lubricación del fabricante.'],
 senales=['El asiento se traba o salta en el riel.','La cuerda o la correa muestran hilos sueltos.','Ruido nuevo en cada tirón.','Los datos del monitor no coinciden con tu esfuerzo.'],
 faq=[('¿Todas las máquinas de remo se lubrican?','No. Depende del modelo y del tipo de riel. Lo más seguro es seguir el manual o preguntarnos con la marca y el modelo.'),('¿Reparan remos hidráulicos?','Revisamos los pistones y su fijación; si un pistón perdió aceite, se evalúa su reemplazo.')],
 rel=['reparacion-escaladora-stepper-cali','reparacion-air-bike-cali','como-elegir-tecnico-de-equipos-de-gimnasio'])

mq(slug='reparacion-escaladora-stepper-cali',n='escaladora y stepper',g='Cardio',ic='elliptical',corto='pistones hidráulicos, pedales con juego, crujidos y monitor',
 intro='<p>La escaladora o stepper simula subir escaleras. Hay modelos pequeños con <b>pistones hidráulicos</b> que se usan en casa y modelos más grandes con escalones giratorios. Es un equipo compacto, pero los pedales y los pistones soportan todo el peso del cuerpo en cada paso.</p>',
 fallas=[('Escaladora de escalones giratorios (stair climber)','cadena o correa de los escalones, motor, rodamientos, tensión y consola.'),('Un pedal se siente más duro o más blando','uno de los pistones perdió aceite o presión.'),('Pedales con juego o que se hunden','bujes, rodamientos o pivotes desgastados.'),('Crujidos al pisar','tornillería floja o falta de lubricación en los pivotes.'),('Monitor sin datos','pila, sensor o conector.'),('Inestabilidad','base desnivelada o soportes sueltos.')],
 mant=['Revisa que el equipo esté sobre una superficie firme y nivelada.','Aprieta la tornillería periódicamente.','No excedas el peso máximo del equipo.','Limpia el sudor del manillar y los pedales.'],
 senales=['Un pedal baja más rápido que el otro.','Crujidos que antes no tenía.','Juego lateral en los pedales.'],
 faq=[('¿Se pueden cambiar los pistones?','En muchos modelos sí, cuando hay repuesto compatible. Se evalúa en la revisión.'),('¿Reparan escaladoras de gimnasio con escalones giratorios?','Sí, revisamos la transmisión de los escalones, el motor y la consola. Escríbenos con marca y modelo.')],
 rel=['reparacion-eliptica-cali','reparacion-maquina-de-remo-cali','como-elegir-tecnico-de-equipos-de-gimnasio'])

mq(slug='reparacion-maquina-smith-cali',n='máquina Smith',g='Fuerza',ic='gym',corto='barra que se atasca, rodamientos, guías y seguros',
 intro='<p>La máquina Smith guía la barra por dos rieles verticales y tiene ganchos de seguridad que permiten dejarla en cualquier punto. Es popular en gimnasios en casa porque permite entrenar con más control. Su funcionamiento depende de que la barra deslice libre y de que los seguros agarren bien.</p>',
 fallas=[('La barra se atasca o sube con tirones','guías sucias, rodamientos lineales desgastados o falta de lubricación.'),('Los ganchos de seguridad no agarran bien','mecanismo desgastado o mal ajustado.'),('Ruido al subir y bajar','roce, tornillos flojos o rodamientos.'),('Desnivel o balanceo','estructura con holgura y patas desniveladas.'),('Contrapeso o cables (en modelos que los tienen)','cables, poleas y sujeciones.')],
 mant=['Limpia las guías con un paño seco y aplica el lubricante recomendado, en poca cantidad.','Revisa que los seguros enganchen bien antes de cada serie.','Aprieta la tornillería con regularidad.','Usa los seguros de apoyo siempre que entrenes con carga.'],
 senales=['La barra no desliza libre.','Los seguros no enganchan o se sueltan.','Ruidos metálicos.'],
 faq=[('¿Es seguro entrenar si el seguro falla?','No. Si el mecanismo de seguridad no engancha bien, deja de usar la máquina hasta que la revisemos.')],
 rel=['reparacion-maquinas-multifuncionales-cali','reparacion-banco-de-pesas-cali','reparacion-estacion-de-poleas-cali'])

mq(slug='reparacion-prensa-de-piernas-cali',n='prensa de piernas',g='Fuerza',ic='gym',corto='carro que no desliza, rodillos, topes de seguridad y tapicería',
 intro='<p>La prensa de piernas permite empujar carga con las piernas desde una posición apoyada. Puede ser <b>inclinada a 45°</b>, <b>horizontal</b> o de pila de pesas. El carro o la plataforma desliza sobre rieles, y esa es la zona donde más desgaste hay.</p>',
 fallas=[('El carro no desliza suave','rieles sucios, rodillos desgastados o desalineados.'),('Ruidos al empujar','rodamientos, tornillería o roce.'),('Topes y seguros','topes de seguridad flojos o mal ajustados.'),('Tapicería rota o espuma hundida','respaldo y asiento desgastados.'),('Pin selector o pila de pesas (en modelos con pila)','guías, pin y amortiguadores.')],
 mant=['Limpia los rieles y quita el polvo.','Revisa los topes de seguridad antes de cargar peso.','Cambia o repara la tapicería rota para que no se agrave.','Verifica que los pines de carga estén bien puestos.'],
 senales=['El carro se frena o salta.','Los topes se mueven.','La tapicería deja ver la estructura.'],
 faq=[('¿Retapizan el asiento y el respaldo?','Sí. Escríbenos con una foto y las medidas aproximadas.')],
 rel=['reparacion-maquina-smith-cali','reparacion-maquinas-multifuncionales-cali','reparacion-banco-de-pesas-cali'])

mq(slug='reparacion-banco-de-pesas-cali',n='banco de pesas',g='Fuerza',ic='gym',corto='ajuste que no encaja, respaldo con juego, tapicería y soportes de barra',
 intro='<p>El banco de pesas (plano, inclinado o ajustable) es la base de un gimnasio en casa. Soporta el peso del cuerpo y de la barra, así que su estabilidad es una cuestión de seguridad. Los bancos ajustables tienen pasadores o mecanismos de cremallera que se desgastan con el tiempo.</p>',
 fallas=[('El ajuste no encaja o no sostiene','pasador o cremallera desgastados.'),('El respaldo o el asiento se mueven','tornillos y bujes flojos.'),('Tapicería rota o espuma hundida','desgaste por uso y sudor.'),('Soportes de barra flojos','soportes o ganchos que se mueven.'),('Inestabilidad','patas o niveladores desajustados.')],
 mant=['Revisa la tornillería cada mes.','Antes de entrenar, comprueba que el respaldo quede bien trabado.','Limpia la tapicería para evitar que se cuartee.','No uses un banco con estructura doblada o con fisuras.'],
 senales=['El respaldo baja solo al cargar peso.','El banco se balancea.','La estructura se nota doblada.'],
 faq=[('¿Reparan estructuras dobladas?','Una estructura doblada o con fisuras debe evaluarse con cuidado; en muchos casos es mejor reemplazarla por seguridad.')],
 rel=['reparacion-maquina-smith-cali','reparacion-torre-de-potencia-cali','reparacion-maquinas-multifuncionales-cali'])

mq(slug='reparacion-estacion-de-poleas-cali',n='estación de poleas',g='Fuerza',ic='gym',corto='cables desgastados, poleas, pila de pesas y agarres',
 intro='<p>La estación de poleas (jalón al pecho, polea alta y baja, remo sentado) usa cables que pasan por poleas y una pila de pesas con un pin selector. Es el mismo sistema de las máquinas multifuncionales, por eso las fallas suelen ser similares.</p>',
 fallas=[('Cables deshilachados o estirados','desgaste normal por uso, o roce con una polea.'),('Poleas que rechinan o se salen','rodamientos secos o soportes flojos.'),('La pila de pesas se traba','guías sucias, pin selector o amortiguadores.'),('Agarres, barras y mosquetones','desgaste o rotura.'),('Ruidos al jalar','roce, falta de lubricación o tornillería.')],
 mant=['Revisa los cables con regularidad: hilos sueltos significan que hay que cambiarlos.','Limpia las barras guía de la pila con un paño seco.','Verifica que el pin selector quede firme.','Aprieta la tornillería de la estructura.'],
 senales=['Hilos sueltos o cable aplastado.','Poleas con ruido.','La pila de pesas se mueve con tirones.'],
 faq=[('¿Cada cuánto se cambia un cable?','Depende del uso. Lo importante es revisarlo con frecuencia; si hay hilos sueltos o deformación, se cambia.')],
 rel=['reparacion-maquinas-multifuncionales-cali','reparacion-maquina-mariposa-pec-deck-cali','reparacion-maquina-smith-cali'])

mq(slug='reparacion-maquina-mariposa-pec-deck-cali',n='máquina mariposa (pec deck)',g='Fuerza',ic='gym',corto='brazos con juego, pivotes, cables y ajuste del asiento',
 intro='<p>La máquina mariposa o pec deck trabaja el pecho y los hombros con dos brazos que giran sobre pivotes y se conectan a una pila de pesas por cables. Suele tener un asiento regulable, a veces con un pistón de gas.</p>',
 fallas=[('Brazos con juego o ruido','pivotes, bujes o rodamientos desgastados.'),('Cables y poleas','desgaste, deshilachado o poleas que rechinan.'),('El asiento no sostiene la altura','pistón de gas o pasador desgastados.'),('Tapicería rota','desgaste por uso.'),('Pila de pesas','guías, pin selector y amortiguadores.')],
 mant=['Aprieta los tornillos de los brazos.','Limpia y revisa cables y poleas.','Comprueba que el asiento quede firme antes de usar.'],
 senales=['Los brazos se mueven con holgura.','El asiento baja solo.','Ruidos en el recorrido.'],
 faq=[('¿Reparan el asiento con pistón?','Revisamos el pistón de gas y el pasador; si hay repuesto compatible se cambia.')],
 rel=['reparacion-estacion-de-poleas-cali','reparacion-maquinas-multifuncionales-cali','reparacion-banco-de-pesas-cali'])

mq(slug='reparacion-torre-de-potencia-cali',n='torre de potencia',g='Fuerza',ic='gym',corto='almohadillas, tornillería, estabilidad y agarres',
 intro='<p>La torre de potencia (power tower) sirve para dominadas, fondos y elevaciones de piernas. Es una estructura vertical que soporta el peso del cuerpo, por lo que la estabilidad y la tornillería son lo más importante. Las almohadillas del respaldo y de los antebrazos se desgastan con el tiempo.</p>',
 fallas=[('Tornillos flojos y estructura que se mueve','vibración por uso.'),('Almohadillas o espuma desgastadas','respaldo, antebrazos y asideros.'),('Patas desniveladas','la torre se balancea.'),('Agarres de dominadas con desgaste','recubrimiento deteriorado.')],
 mant=['Revisa y aprieta la tornillería cada mes.','Verifica que las patas estén niveladas y apoyadas.','Cambia las almohadillas cuando se deterioren.'],
 senales=['La torre se balancea al hacer dominadas.','Tornillos que se aflojan seguido.','Espuma rota o deformada.'],
 faq=[('¿Es seguro si la torre se balancea?','No. Déjala de usar y revisa la tornillería y el apoyo de las patas.')],
 rel=['reparacion-banco-de-pesas-cali','reparacion-maquinas-multifuncionales-cali'])

mq(slug='reparacion-caminadora-bajo-escritorio-cali',n='caminadora bajo el escritorio',g='Cardio',ic='treadmill',corto='control remoto, banda que se corre, motor y ruidos',
 intro='<p>La caminadora bajo el escritorio (under desk) es una caminadora delgada y de baja velocidad pensada para caminar mientras trabajas. Casi siempre se maneja con un control remoto y no tiene barandas ni consola grande. Como se usa muchas horas al día a velocidad baja, el desgaste es distinto al de una caminadora de correr.</p>',
 fallas=[('No responde al control remoto','pilas, receptor o emparejamiento.'),('La banda se corre hacia un lado','alineación y tensión.'),('No enciende','cable, fuente o tarjeta.'),('Ruido o roce','falta de lubricación o rodillos.'),('Se detiene o pierde velocidad','sobrecalentamiento o tarjeta.')],
 mant=['Revisa en el manual si requiere lubricación; algunas vienen lubricadas de fábrica.','Cambia las pilas del control cuando falle.','Limpia el polvo debajo y alrededor del equipo.','No la uses por encima de la velocidad o el peso indicados.'],
 senales=['La banda roza el costado.','El equipo se calienta más de lo normal.','Se apaga durante la jornada.'],
 faq=[('¿Sirve para correr?','Las de bajo escritorio están pensadas para caminar a baja velocidad. Correr en ellas puede dañarlas.')],
 rel=['reparacion-de-caminadoras-cali','reparacion-caminadora-plegable-cali','como-lubricar-una-caminadora-paso-a-paso'])

mq(slug='reparacion-plataforma-vibratoria-cali',n='plataforma vibratoria',g='Otros',ic='gym',corto='motor, control remoto, ruidos y vibración débil',
 intro='<p>La plataforma vibratoria genera vibraciones con un motor interno y se usa para entrenamiento y calentamiento. Tiene un panel o control remoto con niveles de intensidad. Las fallas más comunes se relacionan con el motor, la alimentación y el control.</p>',
 fallas=[('No enciende','cable, fuente o interruptor.'),('El control o el panel no responde','pilas, receptor o botones.'),('La vibración es débil o irregular','motor o contrapesos.'),('Ruidos metálicos','tornillos internos flojos o piezas sueltas.'),('Olor a quemado','motor o tarjeta (apágala de inmediato).')],
 mant=['Usa la plataforma sobre una superficie firme y plana.','Respeta el peso máximo.','Evita la humedad y limpia con un paño ligeramente húmedo.'],
 senales=['La vibración cambió de repente.','Ruido que antes no tenía.','Olor a quemado o calentamiento excesivo.'],
 faq=[('¿Reparan plataformas vibratorias?','Revisamos alimentación, panel y motor; según el modelo se repara o se evalúa el reemplazo de la pieza.')],
 rel=['como-elegir-tecnico-de-equipos-de-gimnasio','cuanto-cuesta-reparar-una-caminadora'])

mq(slug='reparacion-air-bike-cali',n='bicicleta de aire (air bike)',g='Cardio',ic='bike',corto='correa o cadena, ventilador, pedales y brazos con juego',
 intro='<p>La bicicleta de aire (air bike) combina pedales y brazos móviles con un ventilador que genera la resistencia: cuanto más fuerte empujas, más resistencia hay. Es un equipo muy usado en entrenamientos intensos y soporta mucha carga en la transmisión.</p>',
 fallas=[('Cadena o correa floja o ruidosa','tensión, desgaste o falta de lubricación.'),('Ruido del ventilador','aspas sueltas, roce o polvo acumulado.'),('Pedales o brazos con juego','bujes, rodamientos y tornillería.'),('Monitor sin datos','sensor, pila o cableado.'),('Vibración','desbalance del ventilador o tornillos flojos.')],
 mant=['Limpia el polvo de la jaula del ventilador.','Lubrica la cadena si tu modelo la tiene, según el manual.','Aprieta pedales, brazos y asiento con regularidad.'],
 senales=['La cadena salta al pedalear fuerte.','Vibración o golpeteo del ventilador.','Juego en los brazos.'],
 faq=[('¿Cada cuánto se lubrica la cadena?','Depende del uso y del modelo. Un uso intensivo exige revisarla más seguido.')],
 rel=['reparacion-bicicletas-spinning-cali','reparacion-maquina-de-remo-cali','reparacion-bicicleta-estatica-cali'])

mq(slug='reparacion-caminadora-magnetica-cali',n='caminadora magnética (mecánica)',g='Cardio',ic='treadmill',corto='banda que patina, rodillos, resistencia magnética y monitor',
 intro='<p>La caminadora magnética o mecánica no tiene motor eléctrico: la banda se mueve con el impulso de tus pasos y una resistencia magnética regula el esfuerzo. Es una opción compacta y silenciosa, y casi no depende de la electricidad, solo del monitor.</p>',
 fallas=[('La banda patina o se traba','rodillos y rodamientos desgastados o banda floja.'),('La resistencia no cambia','imán o perilla desajustados.'),('Ruido al caminar','rodamientos, tornillos o roce.'),('Monitor sin datos','pila o sensor.'),('Banda desalineada','ajuste de rodillos.')],
 mant=['Limpia el polvo bajo la banda.','Revisa la alineación de la banda y la tornillería.','No la uses con más peso del indicado.'],
 senales=['La banda se siente pesada o a tirones.','Ruido de rodamientos.','Se corre hacia un lado.'],
 faq=[('¿Una caminadora magnética sirve para correr?','Depende del modelo. Muchas están pensadas para caminar; correr puede forzarlas.')],
 rel=['reparacion-de-caminadoras-cali','banda-de-caminadora-patina-o-se-corre','como-centrar-la-banda-de-una-caminadora-paso-a-paso'])

mq(slug='reparacion-caminadora-plegable-cali',n='caminadora plegable',g='Cardio',ic='treadmill',corto='sistema de plegado, pistón de gas, ruedas, motor y consola',
 intro='<p>La caminadora plegable permite guardar la plataforma en vertical para ganar espacio. Además de las fallas de cualquier caminadora, tiene un sistema de plegado con pistón de gas o amortiguador y un pestillo, que se desgastan con el uso y la edad.</p>',
 fallas=[('No sostiene la plataforma plegada o baja de golpe','pistón de gas o amortiguador débil.'),('El pestillo no traba','mecanismo desgastado.'),('Ruedas de transporte','desgaste y soportes.'),('Cableado en la zona de plegado','cables que se doblan y se rompen con el tiempo.'),('Fallas generales','banda, motor, consola e inclinación.')],
 mant=['Pliégala y despliégala despacio y con las dos manos.','No la guardes plegada si el pestillo no traba.','Revisa que el cable no se pellizque al plegar.'],
 senales=['La plataforma baja sola o muy rápido.','El pestillo no asegura.','El equipo se apaga al plegarlo o desplegarlo.'],
 faq=[('¿Es peligroso un pistón de gas débil?','Sí. Una plataforma que baja de golpe puede lastimar. No la uses hasta revisarla.')],
 rel=['reparacion-de-caminadoras-cali','reparacion-caminadora-bajo-escritorio-cali','caminadora-no-enciende'])

EQUIPOS=['reparacion-de-caminadoras-cali','reparacion-caminadora-plegable-cali','reparacion-caminadora-magnetica-cali','reparacion-caminadora-bajo-escritorio-cali','reparacion-bicicleta-estatica-cali','reparacion-bicicleta-reclinada-cali','reparacion-bicicletas-spinning-cali','reparacion-air-bike-cali','reparacion-eliptica-cali','reparacion-maquina-de-remo-cali','reparacion-escaladora-stepper-cali','reparacion-maquinas-multifuncionales-cali','reparacion-maquina-smith-cali','reparacion-estacion-de-poleas-cali','reparacion-maquina-mariposa-pec-deck-cali','reparacion-prensa-de-piernas-cali','reparacion-banco-de-pesas-cali','reparacion-torre-de-potencia-cali','reparacion-plataforma-vibratoria-cali']
def fit_desc(nm,corto):
    parts=[x.strip() for x in corto.replace(' y ',', ').split(',') if x.strip()]
    while True:
        d=f'Reparamos {nm} en Cali: '+', '.join(parts)+'. Servicio a domicilio. Escríbenos por WhatsApp.'
        if len(d)<=158 or len(parts)<=1: return d
        parts.pop()
NUEVOS=[m['slug'] for m in M]
for m in M:
    nm=m['n']
    secs=[('¿Cómo funciona '+('un ' if nm.startswith('banco') else 'una ')+nm+'?',m['intro']),
          ('Fallas de '+nm+' que reparamos','<ul>'+''.join(f'<li><b>{t}:</b> {d}</li>' for t,d in m['fallas'])+'</ul>'),
          ('Mantenimiento básico en casa','<ul>'+''.join(f'<li>{x}</li>' for x in m['mant'])+'</ul>'+SEG),
          ('Señales de que necesitas un técnico','<ul>'+''.join(f'<li>{x}</li>' for x in m['senales'])+'</ul><p>Si ves alguna de estas señales, es mejor revisarla pronto: una falla pequeña que se deja pasar suele terminar dañando otras piezas.</p>'),
          ('Cómo pedir la revisión','<ol><li>Escríbenos por WhatsApp con la marca, el modelo y qué falla presenta.</li><li>Si puedes, envía una foto o un video corto.</li><li>Coordinamos la visita en tu casa en Cali. Revisamos el equipo y te explicamos la falla y el costo antes de reparar.</li></ol><p>Conoce el detalle en <a href="@proceso@">cómo trabajamos paso a paso</a>.</p>')]
    add(m['slug'],kind='service',icon=m['ic'],
        title=f'Reparación de {nm.split(" (")[0]} en Cali | Técnico Gym',
        desc=fit_desc(nm,m['corto']),
        h1=f'Reparación de {nm} en Cali',
        lead=f'Si tu {nm} presenta fallas como {m["corto"]}, la revisamos en tu casa en Cali y te explicamos qué necesita.',
        wamsg=f'Hola Técnico Gym, necesito reparar mi {nm} en Cali. Marca: __ Falla: __',
        sections=secs,faq=m['faq'],related=m['rel'])
