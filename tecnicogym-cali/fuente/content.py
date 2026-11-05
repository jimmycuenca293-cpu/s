# -*- coding: utf-8 -*-
SITE='https://tecnicogym.click'; NAME='Técnico Gym Cali'; PHONE_INTL='573217996144'; PHONE_TXT='321 799 6144'; PHONE_TEL='+573217996144'
def wa(msg): 
    import urllib.parse; return f'https://wa.me/{PHONE_INTL}?text='+urllib.parse.quote(msg)
SERVICIOS=['reparacion-de-caminadoras-cali','reparacion-bicicletas-spinning-cali','reparacion-maquinas-multifuncionales-cali','reparacion-eliptica-cali','mantenimiento-equipos-gimnasio-cali','reparacion-equipos-gimnasio-a-domicilio-cali']
GUIAS=['caminadora-no-enciende','banda-de-caminadora-patina-o-se-corre','ruido-en-la-caminadora','caminadora-se-apaga-sola','cada-cuanto-lubricar-una-caminadora','bicicleta-spinning-hace-ruido','cuanto-cuesta-reparar-una-caminadora','como-elegir-tecnico-de-equipos-de-gimnasio']
PAGES={}
def add(slug,**k): PAGES[slug]=dict(slug=slug,**k)

SEG='<p><b>Antes de revisar cualquier equipo, desconéctalo de la corriente.</b> No abras la tapa del motor ni toques la tarjeta electrónica si no tienes experiencia: aunque el equipo esté apagado, puede haber carga almacenada.</p>'

add('reparacion-de-caminadoras-cali',kind='service',icon='treadmill',
 title='Reparación de Caminadoras en Cali | Técnico Gym',
 desc='Reparamos caminadoras en Cali: no enciende, banda que patina, ruidos, se apaga sola, inclinación y consola. Escríbenos por WhatsApp con marca y falla.',
 h1='Reparación de caminadoras en Cali',
 lead='Si tu caminadora no enciende, la banda patina, hace ruido o se apaga sola, la revisamos y la dejamos funcionando. Atendemos equipos de casa y de gimnasios en Cali.',
 wamsg='Hola Técnico Gym, necesito reparar una caminadora en Cali. Marca: __ Falla: __',
 sections=[
 ('Fallas de caminadoras que reparamos','<ul><li><b>No enciende o la consola se queda sin pantalla:</b> revisamos cable, interruptor, fusible o breaker del equipo, fuente y tarjeta controladora.</li><li><b>La banda patina, se corre hacia un lado o salta:</b> ajuste de tensión y alineación, desgaste de la banda de correr y de la correa del motor.</li><li><b>Ruidos:</b> golpeteo, chillido o zumbido que suele venir de rodillos, rodamientos, falta de lubricación o motor.</li><li><b>Se apaga sola o pierde velocidad:</b> sobrecalentamiento del motor, tarjeta, sensor de velocidad o sobrecarga.</li><li><b>La inclinación no sube ni baja:</b> motor de inclinación, calibración y cableado.</li><li><b>Errores en la consola:</b> diagnóstico del código y de la causa real, no solo reinicio del equipo.</li><li><b>Mantenimiento general:</b> limpieza interna, lubricación de la banda y revisión de tornillería.</li></ul>'),
 ('Cómo trabajamos','<ol><li>Nos escribes por WhatsApp con la marca, el modelo y qué le pasa a la caminadora. Una foto o un video corto del problema ayuda mucho.</li><li>Te orientamos sobre la posible causa y coordinamos la revisión.</li><li>Diagnosticamos el equipo y te explicamos la falla y el costo antes de empezar la reparación.</li><li>Reparamos y probamos la caminadora con carga y a distintas velocidades.</li></ol>'),
 ('¿Cuándo llamar al técnico y no seguir usándola?','<p>Deja de usar la caminadora y escríbenos si huele a quemado, si ves chispas, si el motor suena forzado, si la banda está rota o desalineada o si se apaga con una persona encima. Seguir usándola puede dañar el motor o la tarjeta, y puede ser peligroso.</p>'+SEG),
 ('Caminadoras de casa y de gimnasio','<p>Reparamos caminadoras de uso doméstico y equipos de gimnasios, condominios y empresas en Cali. Si tienes varios equipos, también puedes pedir un <a href="@mantenimiento@">plan de mantenimiento</a> para reducir paradas.</p>'),
 ],
 faq=[('¿Reparan caminadoras a domicilio en Cali?','Sí. Atendemos en Cali. Escríbenos por WhatsApp con la ubicación, la marca y la falla y coordinamos la visita.'),('¿Qué información debo enviar?','La marca y el modelo (suelen estar en una etiqueta o en la consola), qué falla presenta y, si puedes, una foto o un video corto.'),('¿Cuánto cuesta reparar una caminadora?','Depende de la falla y del equipo. Por eso primero la diagnosticamos y te informamos el costo antes de reparar. En la guía de costos explicamos qué lo hace subir o bajar.'),('¿Reparan caminadoras de gimnasio?','Sí, también atendemos gimnasios, condominios y empresas.')],
 related=['caminadora-no-enciende','banda-de-caminadora-patina-o-se-corre','ruido-en-la-caminadora','cuanto-cuesta-reparar-una-caminadora'])

add('reparacion-bicicletas-spinning-cali',kind='service',icon='bike',
 title='Reparación de Bicicletas de Spinning en Cali | Técnico Gym',
 desc='Reparamos bicicletas de spinning y estáticas en Cali: ruidos, pedales, resistencia, transmisión y monitor. Para casa y gimnasios. Escríbenos por WhatsApp.',
 h1='Reparación de bicicletas de spinning y estáticas en Cali',
 lead='Pedales flojos, ruidos al pedalear, resistencia que no frena o un monitor que no marca: revisamos tu bicicleta de spinning o estática y la dejamos lista.',
 wamsg='Hola Técnico Gym, necesito reparar una bicicleta de spinning en Cali. Marca: __ Falla: __',
 sections=[
 ('Fallas que reparamos en bicicletas de spinning','<ul><li><b>Ruido o crujidos al pedalear:</b> pedales, pedalier, rodamientos, tornillería floja o transmisión sin lubricar.</li><li><b>Pedales sueltos o con juego:</b> rosca, manivelas y ejes.</li><li><b>La resistencia no frena o no cambia:</b> sistema de freno (por fricción o magnético), perilla y cable.</li><li><b>Transmisión:</b> revisión de cadena o correa y del volante de inercia.</li><li><b>Sillín y manillar que se aflojan o no sostienen la altura:</b> ajuste y reemplazo de pomos y tornillos.</li><li><b>Monitor o sensor sin datos:</b> pila, cableado y sensor de cadencia.</li></ul>'),
 ('Spinning de gimnasio y bicicleta estática de casa','<p>Una bicicleta de un estudio de spinning trabaja muchas horas al día y necesita revisiones periódicas. La de casa se usa menos, pero también se desajusta con el tiempo. Atendemos las dos y, para gimnasios, ofrecemos <a href="@mantenimiento@">mantenimiento periódico</a>.</p>'),
 ('Cómo pedir la revisión','<ol><li>Escríbenos por WhatsApp con la marca, el modelo y qué le pasa.</li><li>Si puedes, envía un video corto donde se escuche el ruido.</li><li>Coordinamos la visita en Cali, la revisamos y te informamos la falla y el costo antes de reparar.</li></ol>'),
 ],
 faq=[('¿Por qué mi bicicleta de spinning hace ruido?','Casi siempre es tornillería floja, pedales, falta de lubricación o un rodamiento desgastado. En la guía de ruidos explicamos cómo distinguirlo.'),('¿Reparan bicicletas de spinning de gimnasio?','Sí. Atendemos estudios de spinning y gimnasios en Cali.'),('¿Arreglan el monitor de la bicicleta?','Revisamos la pila, el cableado y el sensor. Según el modelo, el monitor se repara o se reemplaza.')],
 related=['bicicleta-spinning-hace-ruido','cuanto-cuesta-reparar-una-caminadora','como-elegir-tecnico-de-equipos-de-gimnasio'])

add('reparacion-maquinas-multifuncionales-cali',kind='service',icon='gym',
 title='Reparación de Máquinas Multifuncionales en Cali | Técnico Gym',
 desc='Reparamos máquinas multifuncionales y multigimnasios en Cali: cables, poleas, pila de pesas, bancos y tapicería. Para casa y gimnasios. Cotiza por WhatsApp.',
 h1='Reparación de máquinas multifuncionales y multigimnasios en Cali',
 lead='Cables desgastados, poleas que rechinan, pila de pesas que se traba o tapicería rota: reparamos tu máquina multifuncional para que vuelva a entrenar con seguridad.',
 wamsg='Hola Técnico Gym, necesito reparar una máquina multifuncional en Cali. Marca: __ Falla: __',
 sections=[
 ('Qué reparamos en una máquina multifuncional','<ul><li><b>Cables y poleas:</b> cambio de cables deshilachados o estirados y de poleas que rechinan o se salen.</li><li><b>Pila de pesas:</b> guías, pin selector, tope y amortiguadores.</li><li><b>Barras y guías:</b> limpieza, lubricación y revisión del recorrido.</li><li><b>Bancos y asientos:</b> ajuste, reemplazo de tornillería y tapicería rota o desgastada.</li><li><b>Agarres, manijas y accesorios:</b> reemplazo y ajuste.</li><li><b>Tornillería y estructura:</b> revisión de ajustes y desgaste para que la máquina sea estable.</li></ul>'),
 ('Por qué no conviene dejar un cable desgastado','<p>El cable es la pieza que soporta la carga cuando levantas peso. Si ves hilos sueltos, el cable se ha estirado o la polea lo roza, déjalo de usar y pide la revisión. Un cable que falla con carga puede lastimar a quien entrena.</p>'),
 ('Para casa, gimnasios y condominios','<p>Reparamos multifuncionales de casa y máquinas de gimnasios, condominios y empresas en Cali. Si manejas varios equipos, un <a href="@mantenimiento@">plan de mantenimiento</a> evita que una falla pequeña pare toda una zona.</p>'),
 ],
 faq=[('¿Cada cuánto se cambian los cables de una multifuncional?','Depende del uso. Lo importante es revisarlos con frecuencia: si ves hilos sueltos, deshilachado o deformación, hay que cambiarlos.'),('¿Retapizan bancos y asientos?','Sí, reparamos y reemplazamos tapicería. Escríbenos con una foto y las medidas aproximadas.'),('¿Atienden gimnasios?','Sí, atendemos gimnasios, condominios y empresas en Cali.')],
 related=['como-elegir-tecnico-de-equipos-de-gimnasio','cuanto-cuesta-reparar-una-caminadora'])

add('reparacion-eliptica-cali',kind='service',icon='elliptical',
 title='Reparación de Elípticas en Cali | Técnico Gym',
 desc='Reparamos bicicletas elípticas en Cali: crujidos, pedales flojos, resistencia y consola. Para casa y gimnasios. Escríbenos por WhatsApp.',
 h1='Reparación de elípticas en Cali',
 lead='Si tu elíptica cruje, se siente floja o la resistencia no responde, la revisamos y la ajustamos o reparamos.',
 wamsg='Hola Técnico Gym, necesito reparar una elíptica en Cali. Marca: __ Falla: __',
 sections=[
 ('Fallas de elípticas que atendemos','<ul><li><b>Crujidos o golpeteo:</b> pivotes, rodamientos, pedales y tornillería floja.</li><li><b>Pedales o brazos con juego:</b> ejes, bujes y piezas desgastadas.</li><li><b>La resistencia no cambia:</b> motor o imán de resistencia, cable y tarjeta.</li><li><b>Consola sin datos o que no enciende:</b> pila, adaptador, cableado y sensor.</li><li><b>Movimiento irregular o brusco:</b> volante de inercia y transmisión.</li></ul>'),
 ('Cómo saber si el ruido es grave','<p>Un crujido leve suele ser tornillería o falta de lubricación. Si el golpeteo aumenta, el equipo se mueve o los pedales tienen juego, deja de usarla y escríbenos. Un buje o rodamiento desgastado se arregla mejor cuando se detecta pronto.</p>'),
 ],
 faq=[('¿Reparan elípticas de gimnasio?','Sí, atendemos casas, gimnasios y condominios en Cali.'),('¿Qué debo enviar para cotizar?','Marca, modelo, qué falla presenta y, si puedes, un video donde se escuche el ruido.')],
 related=['bicicleta-spinning-hace-ruido','como-elegir-tecnico-de-equipos-de-gimnasio'])

add('mantenimiento-equipos-gimnasio-cali',kind='service',icon='shield',
 title='Mantenimiento de Equipos de Gimnasio en Cali | Técnico Gym',
 desc='Mantenimiento preventivo y correctivo de equipos de gimnasio en Cali: caminadoras, spinning, elípticas y multifuncionales. Para gimnasios, condominios y empresas.',
 h1='Mantenimiento de equipos de gimnasio en Cali',
 lead='Si tienes un gimnasio, un condominio o una empresa con zona de ejercicio, el mantenimiento a tiempo evita que una máquina quede fuera de servicio justo cuando más se usa.',
 wamsg='Hola Técnico Gym, quiero cotizar mantenimiento para los equipos de mi gimnasio en Cali.',
 sections=[
 ('Mantenimiento preventivo y correctivo','<p>El <b>preventivo</b> son las revisiones periódicas para encontrar el desgaste antes de que dañe una máquina. El <b>correctivo</b> es la reparación cuando algo ya falló. Hacemos los dos para caminadoras, bicicletas de spinning y estáticas, elípticas y máquinas multifuncionales.</p>'),
 ('Qué se revisa en una visita de mantenimiento','<ul><li>Caminadoras: lubricación y estado de la banda, tensión, alineación, rodillos y limpieza interna.</li><li>Bicicletas: tornillería, pedales, transmisión, freno de resistencia y sillín.</li><li>Elípticas: pivotes, rodamientos, pedales y consola.</li><li>Multifuncionales: cables, poleas, guías, pila de pesas, tapicería y estabilidad.</li><li>Seguridad: llaves de seguridad, paradas de emergencia y sujeciones.</li></ul>'),
 ('Para quién es','<ul><li>Gimnasios y estudios de spinning.</li><li>Conjuntos residenciales y condominios con gimnasio.</li><li>Empresas, hoteles y clínicas con zona de ejercicio.</li></ul><p>Podemos acordar visitas periódicas según el número de equipos y su uso. Escríbenos y te cotizamos.</p>'),
 ],
 faq=[('¿Cada cuánto debe hacerse el mantenimiento?','Depende de cuántas horas se usa cada equipo. Un gimnasio con uso diario necesita revisiones más seguidas que un equipo de casa. Te recomendamos una frecuencia después de ver tus equipos.'),('¿Hacen contratos de mantenimiento?','Podemos acordar visitas periódicas. Escríbenos con el número de equipos y te cotizamos.')],
 related=['cada-cuanto-lubricar-una-caminadora','como-elegir-tecnico-de-equipos-de-gimnasio'])

add('reparacion-equipos-gimnasio-a-domicilio-cali',kind='service',icon='home',
 title='Reparación de Gimnasio a Domicilio en Cali | Técnico Gym',
 desc='Técnico de equipos de gimnasio a domicilio en Cali: caminadoras, spinning, elípticas y multifuncionales. Cuéntanos la falla por WhatsApp y coordinamos la visita.',
 h1='Reparación de equipos de gimnasio a domicilio en Cali',
 lead='No tienes que desmontar ni mover tu equipo. Vamos a tu casa, oficina o gimnasio en Cali, revisamos la falla y te explicamos qué necesita.',
 wamsg='Hola Técnico Gym, necesito un técnico a domicilio en Cali para un equipo de gimnasio. Barrio: __ Equipo: __ Falla: __',
 sections=[
 ('Cómo funciona el servicio a domicilio','<ol><li>Escríbenos por WhatsApp con el barrio, el tipo de equipo, la marca y la falla.</li><li>Te orientamos y coordinamos el día y la hora de la visita.</li><li>El técnico revisa el equipo en el lugar donde está.</li><li>Te explica la falla y el costo antes de reparar. Si se puede resolver en la visita, lo hacemos.</li></ol>'),
 ('Qué tener listo antes de la visita','<ul><li>La marca y el modelo del equipo (etiqueta o consola).</li><li>Un tomacorriente accesible y espacio para trabajar alrededor del equipo.</li><li>Si puedes, un video corto del problema.</li></ul>'),
 ('Equipos que atendemos a domicilio','<p>Caminadoras, bicicletas de spinning y estáticas, elípticas y máquinas multifuncionales. Consulta el barrio y las <a href="@zonas@">zonas de Cali donde atendemos</a>.</p>'),
 ],
 faq=[('¿A qué zonas de Cali van?','Atendemos en Cali. Escríbenos el barrio y confirmamos la visita.'),('¿Pueden reparar el equipo en la visita?','Si la falla y los repuestos lo permiten, sí. Si hace falta una pieza o llevarlo al taller, te lo explicamos antes.')],
 related=['reparacion-de-caminadoras-cali','reparacion-bicicletas-spinning-cali'])

add('zonas-de-servicio-cali',kind='info',icon='pin',
 title='Zonas donde reparamos equipos de gimnasio en Cali | Técnico Gym',
 desc='Atendemos reparación y mantenimiento de equipos de gimnasio en Cali: sur, norte, oeste, centro y oriente. Consulta tu barrio por WhatsApp.',
 h1='Zonas de Cali donde reparamos equipos de gimnasio',
 lead='Atendemos en Cali. Estas son algunas de las zonas y barrios desde donde nos escriben. Si tu barrio no aparece, escríbenos y lo confirmamos.',
 wamsg='Hola Técnico Gym, quiero confirmar si atienden en mi barrio en Cali: __',
 sections=[
 ('Sur de Cali','<p>Ciudad Jardín, Pance, Valle del Lili, El Ingenio, Limonar, Caney, Ciudad 2000, Cañasgordas, Cuarto de Legua, Capri, Gran Limonar y alrededores.</p>'),
 ('Norte de Cali','<p>Granada, Versalles, Santa Mónica, Chipichape, Prados del Norte, Vipasa, La Flora, Menga, Floralia y alrededores.</p>'),
 ('Oeste de Cali','<p>Normandía, Santa Teresita, San Antonio, Aguacatal, Arboledas y alrededores.</p>'),
 ('Centro de Cali','<p>San Fernando, Tequendama, Centenario, San Bosco, Juanambú y alrededores.</p>'),
 ('Oriente de Cali','<p>Si tu equipo está en el oriente de la ciudad, escríbenos el barrio por WhatsApp y coordinamos.</p>'),
 ('¿Tu barrio no está en la lista?','<p>No importa. Escríbenos el barrio y el equipo que necesitas revisar y te confirmamos la visita. Consulta también el <a href="@domicilio@">servicio a domicilio</a>.</p>'),
 ],
 faq=[],related=['reparacion-equipos-gimnasio-a-domicilio-cali','reparacion-de-caminadoras-cali'])

# ----- GUÍAS -----
add('caminadora-no-enciende',kind='guia',
 title='Caminadora no enciende: causas y qué revisar | Técnico Gym',
 desc='¿Tu caminadora no enciende? Revisa la toma, el breaker, la llave de seguridad y el cable antes de llamar al técnico. Guía paso a paso y cuándo pedir ayuda.',
 h1='Caminadora no enciende: causas y qué revisar',
 lead='Antes de llamar al técnico hay cuatro revisiones simples que puedes hacer tú. Si ninguna resuelve el problema, la falla suele estar en la fuente, la tarjeta o la consola.',
 wamsg='Hola Técnico Gym, mi caminadora no enciende. Marca: __ Estoy en Cali.',
 sections=[
 ('Seguridad primero',SEG),
 ('Revisiones que puedes hacer tú','<ol><li><b>La toma de corriente.</b> Conecta otro aparato (una lámpara, un cargador) en el mismo tomacorriente. Si tampoco funciona, el problema es la toma o el breaker de la casa.</li><li><b>El breaker del equipo.</b> Muchas caminadoras tienen un pequeño interruptor o fusible reseteable cerca del cable de entrada. Si salta, ya habrá un indicio de sobrecarga.</li><li><b>La llave de seguridad.</b> Casi todas tienen una llave magnética que va en la consola. Si no está puesta o se salió, la caminadora no arranca.</li><li><b>El cable de alimentación.</b> Revisa que no esté doblado, quemado ni suelto en la entrada del equipo.</li></ol>'),
 ('Si sigue sin encender','<p>Si la consola no da señal de vida con la toma buena, la llave puesta y el cable en buen estado, la causa suele ser la fuente de poder, la tarjeta controladora o la propia consola. Son piezas que requieren medición con instrumentos y no se deben abrir sin experiencia.</p><p>Si además hay olor a quemado, ruido de chasquido o el breaker de la casa salta, no vuelvas a conectarla.</p>'),
 ('Qué datos enviarnos','<p>Marca, modelo, si hubo un apagón, una subida de tensión o un ruido antes de que se apagara, y qué luces o mensajes muestra la consola. Con eso orientamos la causa más probable.</p>'),
 ],
 faq=[('¿Una subida de tensión puede dañar la caminadora?','Sí. Una subida de voltaje o un apagón brusco puede dañar la fuente o la tarjeta. Si pasó justo antes de la falla, avísanos.'),('¿Es normal que se dispare el breaker?','No. Si se dispara una y otra vez, desconecta el equipo y pide una revisión.')],
 related=['caminadora-se-apaga-sola','reparacion-de-caminadoras-cali','cuanto-cuesta-reparar-una-caminadora'])

add('banda-de-caminadora-patina-o-se-corre',kind='guia',
 title='Banda de caminadora que patina o se corre: causas | Técnico Gym',
 desc='La banda de tu caminadora patina, se corre a un lado o salta. Conoce las causas (tensión, alineación, lubricación, desgaste) y cuándo llamar al técnico.',
 h1='La banda de la caminadora patina o se corre: causas',
 lead='Una banda que patina o se desplaza hacia un lado casi siempre tiene solución. Lo importante es identificar si el problema es de tensión, de alineación, de lubricación o de desgaste.',
 wamsg='Hola Técnico Gym, la banda de mi caminadora patina o se corre. Marca: __ Estoy en Cali.',
 sections=[
 ('Banda que patina o se siente resbalosa','<p>Si al pisar la banda se frena o salta mientras el motor sigue girando, suele ser <b>poca tensión</b> o una <b>correa del motor desgastada</b>. También puede pasar si la banda está seca y roza con la tabla de apoyo, o si hay desgaste en la superficie.</p>'),
 ('Banda que se corre hacia un lado','<p>Cuando la banda se va hacia la izquierda o hacia la derecha, suele ser un tema de <b>alineación de los rodillos</b>. Se corrige con los tornillos de ajuste de la parte trasera, y hay que hacerlo con la caminadora funcionando a baja velocidad y con ajustes pequeños (un cuarto de vuelta cada vez). Un ajuste excesivo puede dañar la banda.</p>'),
 ('Lubricación y desgaste','<p>La fricción entre la banda y la tabla de apoyo calienta el motor y desgasta ambas piezas. Revisa en el manual si tu caminadora requiere lubricación; algunas bandas vienen ya lubricadas y otras no. Si la banda está deshilachada en los bordes, brillante o con grietas, probablemente hay que cambiarla.</p>'),
 ('Cuándo llamar al técnico','<ul><li>Si ajustaste la banda y vuelve a correrse.</li><li>Si la banda tiene bordes rotos o está estirada.</li><li>Si el motor suena forzado o huele a quemado.</li></ul>'),
 ],
 faq=[('¿Puedo seguir usando la caminadora con la banda corrida?','No conviene. La banda puede rozar con el marco y romperse.'),('¿Cuándo hay que cambiar la banda?','Cuando está deshilachada, brillante, con grietas o ya no se puede tensar bien.')],
 related=['cada-cuanto-lubricar-una-caminadora','ruido-en-la-caminadora','reparacion-de-caminadoras-cali'])

add('ruido-en-la-caminadora',kind='guia',
 title='Ruido en la caminadora: tipos de ruido y causas | Técnico Gym',
 desc='¿Tu caminadora hace ruido? Golpeteo, chillido, zumbido o roce: qué significa cada uno y qué revisar antes de llamar al técnico en Cali.',
 h1='Ruido en la caminadora: qué significa cada uno',
 lead='El tipo de ruido ayuda a encontrar la causa. Estas son las más comunes.',
 wamsg='Hola Técnico Gym, mi caminadora hace ruido. Es un ruido de tipo __. Estoy en Cali.',
 sections=[
 ('Golpeteo rítmico','<p>Un golpe que se repite con cada vuelta de la banda suele indicar un empalme de la banda, un rodillo con un defecto o un objeto atrapado. Revisa debajo de la banda.</p>'),
 ('Chillido o rechinar','<p>Suele ser falta de lubricación entre banda y tabla, o un rodamiento seco en un rodillo.</p>'),
 ('Zumbido del motor','<p>Un zumbido más fuerte de lo normal puede indicar el motor trabajando forzado por exceso de fricción, una correa floja o polvo acumulado. Si huele a quemado, apágala.</p>'),
 ('Roce','<p>Un roce continuo en un lado suele indicar que la banda está desalineada y toca el marco.</p>'),
 ('Qué puedes hacer tú','<ul><li>Limpiar el polvo alrededor del motor con el equipo desconectado.</li><li>Revisar tornillos flojos en la estructura y la consola.</li><li>Confirmar si necesita lubricación según el manual.</li></ul>'+SEG),
 ],
 faq=[('¿Un ruido siempre es una falla?','No siempre, pero conviene revisarlo. Un ruido nuevo suele ser el primer síntoma de un desgaste que se puede corregir a tiempo.')],
 related=['cada-cuanto-lubricar-una-caminadora','banda-de-caminadora-patina-o-se-corre','reparacion-de-caminadoras-cali'])

add('caminadora-se-apaga-sola',kind='guia',
 title='Caminadora se apaga sola: causas y qué hacer | Técnico Gym',
 desc='Si tu caminadora se apaga sola mientras la usas, puede ser sobrecalentamiento, breaker, llave de seguridad o tarjeta. Qué revisar y cuándo llamar al técnico.',
 h1='La caminadora se apaga sola: causas y qué hacer',
 lead='Que se apague sola es una señal de que algo está forzando el equipo. Estas son las causas más frecuentes.',
 wamsg='Hola Técnico Gym, mi caminadora se apaga sola. Marca: __ Estoy en Cali.',
 sections=[
 ('Causas más comunes','<ul><li><b>Llave de seguridad:</b> si se mueve o se suelta, la caminadora se detiene.</li><li><b>Sobrecarga o sobrecalentamiento del motor:</b> por fricción excesiva, polvo o uso prolongado.</li><li><b>Breaker o fusible del equipo:</b> si salta, la caminadora corta la energía.</li><li><b>Tomacorriente o extensión:</b> una toma floja o una extensión inadecuada corta la energía.</li><li><b>Tarjeta o fuente:</b> una falla electrónica intermitente.</li></ul>'),
 ('Qué revisar','<ol><li>Conecta la caminadora directamente a la pared, sin extensiones.</li><li>Revisa la llave de seguridad.</li><li>Deja enfriar el motor y verifica si necesita lubricación.</li></ol>'),
 ('Cuándo pedir revisión','<p>Si se sigue apagando, si hay olor a quemado o si salta el breaker de la casa, no insistas: puedes dañar el motor o la tarjeta.</p>'),
 ],
 faq=[('¿Puedo usar una extensión?','No se recomienda. Las caminadoras consumen bastante y una extensión inadecuada se calienta.')],
 related=['caminadora-no-enciende','cada-cuanto-lubricar-una-caminadora','reparacion-de-caminadoras-cali'])

add('cada-cuanto-lubricar-una-caminadora',kind='guia',
 title='Cada cuánto lubricar una caminadora y cómo | Técnico Gym',
 desc='Cada cuánto lubricar la banda de una caminadora, cómo saber si lo necesita y por qué importa. Guía práctica y cuándo llamar a un técnico en Cali.',
 h1='Cada cuánto lubricar una caminadora',
 lead='Lubricar la banda alarga la vida del motor y de la banda. La frecuencia depende del modelo y del uso.',
 wamsg='Hola Técnico Gym, quiero un mantenimiento y lubricación para mi caminadora en Cali. Marca: __',
 sections=[
 ('Por qué importa','<p>Entre la banda y la tabla de apoyo hay fricción. Con la lubricación adecuada esa fricción baja, el motor trabaja con menos esfuerzo y la banda dura más.</p>'),
 ('Cada cuánto','<p>Lo correcto es seguir el manual de tu marca: algunas bandas vienen lubricadas de fábrica y otras requieren lubricante de silicona cada cierto tiempo. Como referencia general, muchos fabricantes recomiendan revisar la lubricación cada tres meses o unas 150 horas de uso, y más seguido si el uso es intensivo. Si no tienes el manual, escríbenos con marca y modelo.</p>'),
 ('Cómo saber si la necesita','<ul><li>La banda se siente "pesada" o rasposa al caminar.</li><li>El motor suena forzado o se calienta más.</li><li>Pasas la mano bajo la banda y la tabla se siente seca.</li></ul>'),
 ('Importante','<p>No todos los lubricantes sirven. Un producto equivocado puede dañar la banda. Si no estás seguro, pide mantenimiento.</p>'+SEG),
 ],
 faq=[('¿Todas las caminadoras se lubrican?','No. Depende del modelo. Algunas ya vienen con la banda lubricada y no necesitan lubricación periódica.')],
 related=['ruido-en-la-caminadora','banda-de-caminadora-patina-o-se-corre','mantenimiento-equipos-gimnasio-cali'])

add('bicicleta-spinning-hace-ruido',kind='guia',
 title='Bicicleta de spinning hace ruido: causas | Técnico Gym',
 desc='Bicicleta de spinning o estática que hace ruido al pedalear: pedales, tornillería, transmisión y freno. Qué revisar y cuándo llamar al técnico en Cali.',
 h1='Bicicleta de spinning que hace ruido: causas',
 lead='Un ruido al pedalear suele ser tornillería floja o desgaste en una pieza concreta. Así puedes ubicarlo.',
 wamsg='Hola Técnico Gym, mi bicicleta de spinning hace ruido. Estoy en Cali. Marca: __',
 sections=[
 ('Ubica el ruido','<ul><li><b>Cada vuelta del pedal:</b> pedales o manivelas flojas.</li><li><b>Un chirrido constante:</b> transmisión seca (cadena o correa).</li><li><b>Un roce al frenar o aumentar resistencia:</b> pastilla o freno desalineado.</li><li><b>Un golpeteo al ponerte de pie:</b> sillín, manillar o estructura floja.</li></ul>'),
 ('Qué revisar','<ol><li>Aprieta los pedales (recuerda que el pedal izquierdo tiene rosca inversa).</li><li>Revisa los tornillos del sillín y manillar.</li><li>Observa si algo roza con el volante de inercia.</li></ol>'),
 ('Cuándo llamar al técnico','<p>Si el ruido sigue después de apretar la tornillería, si hay juego en las manivelas o si el pedalear se siente irregular.</p>'),
 ],
 faq=[('¿Es peligroso un pedal flojo?','Sí. Puede dañar la rosca de la manivela y, en el peor caso, soltarse durante el uso.')],
 related=['reparacion-bicicletas-spinning-cali','reparacion-eliptica-cali'])

add('cuanto-cuesta-reparar-una-caminadora',kind='guia',
 title='¿Cuánto cuesta reparar una caminadora en Cali? | Técnico Gym',
 desc='Qué determina el costo de reparar una caminadora o un equipo de gimnasio: la falla, las piezas, la marca y la visita. Cómo cotizar en Cali.',
 h1='¿Cuánto cuesta reparar una caminadora?',
 lead='No existe un precio único. El costo depende de la falla, de las piezas y del equipo. Te explicamos qué influye y cómo conseguir una cotización clara.',
 wamsg='Hola Técnico Gym, quiero cotizar la reparación de mi equipo en Cali. Equipo: __ Falla: __',
 sections=[
 ('Qué hace que una reparación cueste más o menos','<ul><li><b>La falla:</b> ajustar una banda es muy distinto a cambiar una tarjeta o un motor.</li><li><b>Las piezas:</b> disponibilidad y precio según la marca y el modelo.</li><li><b>El tiempo de trabajo:</b> si se resuelve en una visita o requiere llevar el equipo.</li><li><b>El estado general:</b> un equipo con varias fallas cuesta más.</li></ul>'),
 ('Por qué conviene un diagnóstico antes','<p>Sin ver el equipo, cualquier precio es una suposición. Un diagnóstico permite decidir si conviene reparar, qué piezas hacen falta y cuánto cuesta.</p>'),
 ('Cómo conseguir una cotización','<ol><li>Envía marca, modelo y falla por WhatsApp.</li><li>Adjunta una foto o un video del problema.</li><li>Coordina la revisión y pide que te expliquen la falla y el costo antes de reparar.</li></ol>'),
 ],
 faq=[('¿Es mejor reparar o comprar una nueva?','Depende de la falla y del valor del equipo. Con el diagnóstico te damos una recomendación honesta.')],
 related=['como-elegir-tecnico-de-equipos-de-gimnasio','reparacion-de-caminadoras-cali'])

add('como-elegir-tecnico-de-equipos-de-gimnasio',kind='guia',
 title='Cómo elegir un técnico de equipos de gimnasio | Técnico Gym',
 desc='Qué preguntar antes de contratar un técnico de caminadoras y equipos de gimnasio en Cali: diagnóstico, costos claros, pruebas y comunicación.',
 h1='Cómo elegir un técnico de equipos de gimnasio',
 lead='Un buen técnico te explica la falla, te da un costo claro y prueba el equipo antes de irse. Estas preguntas te ayudan a elegir.',
 wamsg='Hola Técnico Gym, quiero una revisión de mi equipo en Cali. Equipo: __ Falla: __',
 sections=[
 ('Qué preguntar antes de contratar','<ul><li>¿Hacen diagnóstico antes de dar el precio?</li><li>¿Me explican la falla y qué piezas se cambian?</li><li>¿Pueden mostrarme la pieza dañada?</li><li>¿Prueban el equipo con carga antes de entregarlo?</li><li>¿Atienden en mi zona y a domicilio?</li></ul>'),
 ('Señales de alerta','<ul><li>Precios cerrados sin ver el equipo.</li><li>No explican qué se cambió.</li><li>Cambian piezas "por si acaso".</li></ul>'),
 ('Cómo trabajamos en Técnico Gym','<p>Diagnosticamos el equipo, te explicamos la falla y el costo antes de reparar, y probamos la máquina al terminar. Escríbenos por WhatsApp para coordinar la revisión.</p>'),
 ],
 faq=[],related=['cuanto-cuesta-reparar-una-caminadora','reparacion-equipos-gimnasio-a-domicilio-cali'])

add('preguntas-frecuentes',kind='info',icon='help',
 title='Preguntas frecuentes sobre reparación de gimnasio | Técnico Gym',
 desc='Respuestas sobre reparación de caminadoras, bicicletas y equipos de gimnasio en Cali: servicio a domicilio, costos, marcas, tiempos y cómo agendar.',
 h1='Preguntas frecuentes',
 lead='Las dudas más comunes sobre cómo trabajamos en Cali.',
 wamsg='Hola Técnico Gym, tengo una pregunta sobre la reparación de mi equipo.',
 sections=[],
 faq=[('¿Reparan equipos a domicilio en Cali?','Sí. Atendemos en Cali; escríbenos el barrio por WhatsApp y coordinamos la visita.'),
  ('¿Qué equipos reparan?','Caminadoras, bicicletas de spinning y estáticas, elípticas y máquinas multifuncionales, de casa y de gimnasio.'),
  ('¿Cuánto cuesta una reparación?','Depende de la falla y del equipo. Primero diagnosticamos y te informamos el costo antes de reparar.'),
  ('¿De qué marcas?','Revisamos equipos de distintas marcas. Escríbenos la marca y el modelo y te confirmamos.'),
  ('¿Cuánto demora una reparación?','Depende de la falla y de si hay que conseguir una pieza. Si se resuelve en la visita, el mismo día; si no, te informamos el tiempo estimado.'),
  ('¿Atienden gimnasios y condominios?','Sí. Podemos acordar visitas periódicas de mantenimiento.'),
  ('¿Qué debo enviar para cotizar?','Marca, modelo, la falla y, si puedes, una foto o un video corto.'),
  ('¿Cómo agendo?','Escríbenos por WhatsApp al '+PHONE_TXT+' o llámanos.')],
 related=['reparacion-de-caminadoras-cali','reparacion-equipos-gimnasio-a-domicilio-cali'])

add('contacto',kind='info',icon='chat',
 title='Contacto: Técnico Gym, reparación de equipos de gimnasio en Cali',
 desc='Escríbenos por WhatsApp al 321 799 6144 o llámanos. Reparación de caminadoras, spinning y multifuncionales en Cali.',
 h1='Contacto',
 lead='La forma más rápida de pedir una revisión es escribirnos por WhatsApp.',
 wamsg='Hola Técnico Gym, necesito una revisión de un equipo de gimnasio en Cali.',
 sections=[
 ('WhatsApp y llamadas','<p>WhatsApp y teléfono: <a href="tel:'+PHONE_TEL+'"><b>'+PHONE_TXT+'</b></a></p><p>Escríbenos con: tipo de equipo, marca y modelo, qué falla presenta, tu barrio en Cali y, si puedes, una foto o un video corto.</p>'),
 ('Cobertura','<p>Atendemos en Cali. Consulta las <a href="@zonas@">zonas</a> o escríbenos tu barrio.</p>'),
 ],faq=[],related=['reparacion-equipos-gimnasio-a-domicilio-cali','preguntas-frecuentes'])
