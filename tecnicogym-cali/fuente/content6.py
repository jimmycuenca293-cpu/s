# -*- coding: utf-8 -*-
from content import PAGES,add,SEG
import content4,content5
from content4 import GUIAS_ALL,ZS
from content5 import L,O,PRO
NG2=[]
def G(slug,h1,title,desc,lead,secs,rel,wamsg,faq=None):
    NG2.append(slug); add(slug,kind='guia',title=title,desc=desc,h1=h1,lead=lead,wamsg=wamsg,sections=secs,faq=faq or [],related=rel)
W=lambda t:f'Hola Técnico Gym, {t} Estoy en Cali. Marca: __'
G('caminadora-da-corrientazos-o-descargas','La caminadora da corrientazos o descargas: causas','Caminadora que da corrientazos: causas y qué hacer | Técnico Gym',
 'Tu caminadora da pequeños choques o descargas al tocarla. Causas (estática, tierra, humedad, fallas eléctricas) y por qué debes dejar de usarla hasta revisarla.',
 'Sentir una descarga al tocar la caminadora puede ser electricidad estática o una falla eléctrica. No lo dejes pasar.',
 [('Primero, seguridad','<p>Si sientes descargas, deja de usar la caminadora y desconéctala. Una falla eléctrica real puede ser peligrosa.</p>'+SEG),
  ('Causas posibles',L(['<b>Electricidad estática:</b> es común en climas secos o con ciertos pisos y calzado; suele ser un chispazo leve al tocar la consola o la barra.','<b>Falta de conexión a tierra:</b> una toma sin tierra o un enchufe adaptado.','<b>Humedad o sudor</b> en la consola o el cable.','<b>Aislamiento dañado</b> en un cable interno.','<b>Falla de la fuente o la tarjeta.</b>'])),
  ('Qué puedes revisar',O(['Comprueba que el tomacorriente tenga conexión a tierra y que el enchufe no esté adaptado.','Evita usar extensiones o multitomas en mal estado.','Seca el sudor de la consola y los pasamanos.','Si el choque se repite, no sigas usándola.'])),
  ('Cuándo llamar al técnico','<p>Siempre que la descarga no sea un simple chispazo estático o que se repita. Una revisión eléctrica permite descartar fallas de aislamiento.</p>')],
 ['caminadora-huele-a-quemado','caminadora-no-enciende','reparacion-de-caminadoras-cali'],W('mi caminadora da corrientazos.'))
G('como-cambiar-la-banda-de-una-caminadora','Cómo cambiar la banda de una caminadora: guía general','Cómo cambiar la banda de una caminadora | Técnico Gym',
 'Guía general de cómo se cambia la banda de una caminadora: señales, herramientas, pasos y cuándo conviene que lo haga un técnico en Cali.',
 'Cambiar la banda es un trabajo que se puede hacer en casa si tienes herramientas y paciencia, pero un error puede dañar rodillos y tabla.',
 [('Antes de empezar',L(['Confirma que la banda es el problema: bordes deshilachados, grietas o estiramiento.','Consigue una banda del mismo largo, ancho y tipo que la original.','Ten a mano llaves Allen, un paño y lubricante de silicona si tu modelo lo usa.'])+SEG),
  ('Pasos generales',O(['Desconecta la caminadora.','Afloja los tornillos de tensión traseros para destensar la banda.','Retira las tapas laterales y, si el modelo lo exige, suelta el rodillo trasero.','Retira la banda vieja y limpia la tabla y los rodillos.','Revisa si la tabla está desgastada o los rodamientos suenan.','Coloca la banda nueva centrada.','Vuelve a montar, tensa y centra la banda con ajustes pequeños.','Pruébala a baja velocidad y ajusta.'])),
  ('Por qué conviene un técnico','<p>Si el rodillo queda desalineado, la tabla está gastada o la tensión es incorrecta, la banda nueva se daña rápido o se corre. Además hay que revisar la correa y el motor. Mira el servicio de <a href="@banda@">cambio de banda en Cali</a>.</p>')],
 ['cambio-de-banda-de-caminadora-cali','como-centrar-la-banda-de-una-caminadora-paso-a-paso','como-saber-si-la-banda-de-la-caminadora-esta-desgastada'],W('necesito cambiar la banda de mi caminadora.'))
G('caminadora-vibra-o-se-mueve-al-correr','La caminadora vibra o se mueve al correr','Caminadora que vibra o se mueve al correr: causas | Técnico Gym',
 'Tu caminadora vibra, se mueve o se balancea mientras corres. Causas: desnivel, patas, tornillería, rodillos y banda. Qué revisar y cuándo llamar al técnico.',
 'Una caminadora debe sentirse firme. Si vibra o se balancea, casi siempre es cuestión de apoyo, tornillería o desgaste.',
 [('Causas frecuentes',L(['La caminadora está desnivelada o sobre una superficie blanda.','Patas niveladoras desajustadas.','Tornillos de la estructura flojos.','Rodillo con rodamiento desgastado.','Banda con un bulto o desgaste.','Motor o correa en mal estado.'])),
  ('Qué revisar tú',O(['Comprueba el nivel de la caminadora y ajusta las patas.','Apoya la caminadora en un piso firme, no sobre alfombras gruesas.','Revisa y aprieta la tornillería de la estructura y de la consola.','Observa si la vibración aparece solo a cierta velocidad.'])+SEG),
  ('Cuándo llamar al técnico','<p>Si después de nivelar y apretar sigue vibrando, si hay golpes en cada vuelta de la banda o ruidos del motor, escríbenos con marca y modelo.</p>')],
 ['como-ubicar-y-nivelar-una-caminadora-en-casa','ruido-en-la-caminadora','reparacion-de-caminadoras-cali'],W('mi caminadora vibra al correr.'))
G('caminadora-se-traba-al-subir-la-velocidad','La caminadora se traba al subir la velocidad','Caminadora que se traba al subir la velocidad | Técnico Gym',
 'La caminadora se traba, da tirones o se detiene al subir la velocidad. Causas: banda, correa, motor, tarjeta o sensor. Qué revisar antes de llamar al técnico.',
 'Si la banda se traba o da tirones al acelerar, suele ser fricción, la correa del motor o la tarjeta.',
 [('Causas frecuentes',L(['Banda seca o muy tensa que roza con la tabla.','Correa del motor floja o desgastada.','Motor sobrecargado o con desgaste.','Sensor de velocidad que no lee bien.','Tarjeta controladora que no entrega la potencia.'])),
  ('Qué revisar',O(['Revisa si tu modelo necesita lubricación y si la banda se siente pesada.','Comprueba que la banda no esté muy tensa ni desalineada.','Anota a qué velocidad se traba y si la consola muestra algún error.'])+SEG),
  ('Cuándo pedir revisión','<p>Si se traba siempre a la misma velocidad o con peso, es mejor revisar motor y tarjeta antes de que se dañen.</p>')],
 ['reparacion-motor-de-caminadora-cali','caminadora-se-apaga-sola','como-lubricar-una-caminadora-paso-a-paso'],W('mi caminadora se traba al subir la velocidad.'))
G('la-banda-de-la-caminadora-se-siente-dura-o-pesada','La banda de la caminadora se siente dura o pesada','Banda de caminadora dura o pesada: causas | Técnico Gym',
 'Si la banda de tu caminadora se siente dura, pesada o cuesta caminar sobre ella, puede faltar lubricación o estar muy tensa. Qué revisar y cuándo llamar al técnico.',
 'Una banda que se siente pesada obliga al motor a trabajar más. Corregirlo a tiempo evita daños mayores.',
 [('Causas',L(['Falta de lubricación entre banda y tabla.','Banda demasiado tensa.','Tabla de apoyo desgastada o con residuos.','Rodamientos de los rodillos con desgaste.','Polvo acumulado bajo la banda.'])),
  ('Qué hacer',O(['Desconecta y limpia el polvo bajo la banda.','Revisa en el manual si tu modelo requiere lubricación.','Verifica que la tensión no sea excesiva (la banda no debe estar rígida).','Si no mejora, pide una revisión.'])+SEG),
  ('Por qué importa','<p>La fricción extra calienta el motor y desgasta banda y tabla. Muchas veces es la causa detrás de motores quemados.</p>')],
 ['como-lubricar-una-caminadora-paso-a-paso','cada-cuanto-lubricar-una-caminadora','mantenimiento-preventivo-de-caminadoras-cali'],W('la banda de mi caminadora se siente pesada.'))
G('usada-que-revisar-antes-de-comprar-una-caminadora','Qué revisar antes de comprar una caminadora usada','Qué revisar antes de comprar una caminadora usada | Técnico Gym',
 'Lista práctica para revisar una caminadora usada antes de comprarla: banda, motor, ruidos, consola, inclinación y estructura. Evita malas compras en Cali.',
 'Una caminadora usada puede ser buena compra. Esta lista te ayuda a detectar problemas antes de pagar.',
 [('Antes de ir',L(['Pide marca, modelo y año aproximado.','Pregunta por qué la venden y cuánto se usó.','Pide que esté conectada para probarla.'])),
  ('Revisión paso a paso',O(['Enciéndela y revisa que la consola funcione.','Súbela de a poco hasta una velocidad alta y escucha el motor: debe ser parejo.','Pisa la banda mientras se mueve: no debe patinar ni saltar.','Mira los bordes de la banda: no deben estar deshilachados ni brillantes.','Prueba la inclinación en todo el rango.','Comprueba que no huela a quemado.','Verifica estructura, tornillos y estabilidad.'])),
  ('Señales para no comprar',L(['No te dejan encenderla.','Ruidos fuertes o vibración.','Piezas faltantes o cables improvisados.','Olor a quemado o motor muy caliente.'])),
  ('Revisión técnica','<p>Si quieres estar seguro, coordina una <a href="@usados@">revisión técnica antes de comprar</a>.</p>')],
 ['revision-de-equipos-de-gimnasio-usados-antes-de-comprar-cali','cuanto-cuesta-reparar-una-caminadora','diferencia-entre-caminadora-electrica-y-magnetica'],W('quiero revisar una caminadora usada antes de comprarla.'))
G('diferencia-entre-caminadora-electrica-y-magnetica','Diferencia entre caminadora eléctrica y magnética','Caminadora eléctrica vs magnética: diferencias | Técnico Gym',
 'Diferencias entre una caminadora eléctrica y una magnética (mecánica): cómo funcionan, ventajas, desventajas y fallas más comunes de cada una.',
 'Saber qué tipo de caminadora tienes ayuda a entender sus fallas y su mantenimiento.',
 [('Caminadora eléctrica','<p>Tiene un motor que mueve la banda, una consola con velocidad programable y, en muchos modelos, inclinación eléctrica. Se usa para caminar y correr. Fallas típicas: motor, tarjeta, correa, banda, consola e inclinación.</p>'),
  ('Caminadora magnética o mecánica','<p>No tiene motor eléctrico: la banda se mueve con tu paso y una resistencia magnética regula el esfuerzo. Es más compacta y silenciosa. Fallas típicas: rodamientos de los rodillos, resistencia, banda y monitor. Suele servir para caminar, no para correr.</p>'),
  ('¿Cuál conviene?',L(['<b>Eléctrica:</b> si quieres correr, controlar la velocidad y entrenar con inclinación.','<b>Magnética:</b> si buscas algo compacto, silencioso y para caminar.'])),
  ('Mantenimiento de cada una','<p>Las dos necesitan limpieza, revisión de la banda y de la tornillería. La eléctrica, además, lubricación (si el modelo la pide) y revisión del motor. Mira las páginas de <a href="@reparacion@">reparación de caminadoras</a>.</p>')],
 ['reparacion-caminadora-magnetica-cali','reparacion-de-caminadoras-cali','usada-que-revisar-antes-de-comprar-una-caminadora'],W('quiero saber qué tipo de caminadora tengo.'))
G('que-hacer-si-se-moja-una-caminadora','Qué hacer si se moja una caminadora','Qué hacer si se moja una caminadora | Técnico Gym',
 'Si se derramó agua o líquido sobre tu caminadora o hay humedad en el equipo, qué hacer primero, qué no hacer y cuándo llamar a un técnico en Cali.',
 'El agua y la electricidad no se llevan bien. Actúa rápido y con cuidado.',
 [('Qué hacer de inmediato',O(['No la toques si está conectada y mojada: desconecta primero desde el tomacorriente, con las manos secas.','No la enciendas.','Seca por fuera con un paño.','Déjala secar en un lugar ventilado, sin forzarla.'])+SEG),
  ('Qué no hacer',L(['No uses secador de pelo cerca de la tarjeta o la consola.','No la enciendas "para probar".','No ignores un derrame aunque parezca poco.'])),
  ('Cuándo llamar al técnico','<p>Siempre que el líquido haya entrado a la consola, al motor o a la tarjeta. La humedad puede dañar la electrónica incluso días después. Escríbenos con marca y modelo.</p>')],
 ['caminadora-no-enciende','reparacion-tarjeta-controladora-de-caminadora-cali','caminadora-da-corrientazos-o-descargas'],W('se mojó mi caminadora.'))
G('mantenimiento-de-bicicleta-de-spinning-paso-a-paso','Mantenimiento de bicicleta de spinning paso a paso','Mantenimiento de bicicleta de spinning paso a paso | Técnico Gym',
 'Guía de mantenimiento de una bicicleta de spinning: limpieza, tornillería, pedales, transmisión y resistencia. Qué hacer cada semana y cada mes.',
 'Unos minutos de cuidado a tiempo mantienen tu bicicleta de spinning silenciosa y segura.',
 [('Después de cada uso',L(['Limpia el sudor del marco, manillar y asiento con un paño.','Revisa que el asiento y el manillar sigan firmes.'])),
  ('Cada semana',O(['Aprieta los pedales (el izquierdo tiene rosca inversa).','Revisa la tornillería visible.','Observa si hay ruidos o juego en las manivelas.'])),
  ('Cada mes',O(['Revisa y limpia la transmisión (cadena o correa).','Lubrica la cadena, si la tiene, con el lubricante indicado.','Revisa la pastilla de resistencia en modelos de fricción.','Comprueba el nivelado de la bicicleta.'])+SEG),
  ('Cuándo llamar al técnico','<p>Si hay ruido que no desaparece, juego en las manivelas o resistencia irregular, pide una revisión. En estudios y gimnasios conviene un <a href="@mantenimiento@">mantenimiento periódico</a>.</p>')],
 ['bicicleta-spinning-hace-ruido','reparacion-bicicletas-spinning-cali','como-cambiar-los-pedales-de-una-bicicleta-de-spinning'],W('quiero mantenimiento para mi bicicleta de spinning.'))
G('como-cambiar-los-pedales-de-una-bicicleta-de-spinning','Cómo cambiar los pedales de una bicicleta de spinning','Cómo cambiar los pedales de una bici de spinning | Técnico Gym',
 'Cómo cambiar los pedales de una bicicleta de spinning o estática: herramienta, rosca inversa del pedal izquierdo y errores que dañan la manivela.',
 'Cambiar los pedales es sencillo si recuerdas un detalle: el pedal izquierdo se aprieta al revés.',
 [('Lo que necesitas',L(['Llave de pedal o llave fija del tamaño del pedal (a menudo 15 mm) o llave Allen en algunos modelos.','Un poco de grasa para la rosca.'])),
  ('Paso a paso',O(['Identifica cuál es el pedal derecho (R) y cuál el izquierdo (L).','Para aflojar el derecho, gira la llave en sentido contrario a las agujas del reloj.','El izquierdo tiene rosca inversa: se afloja en sentido horario.','Limpia la rosca y aplica un poco de grasa.','Coloca el pedal nuevo a mano para no cruzar la rosca.','Aprieta con la llave en el sentido contrario al de aflojar.'])+SEG),
  ('Errores comunes',L(['Cruzar la rosca por forzar el pedal.','Apretar el pedal izquierdo en el sentido equivocado.','No limpiar la rosca antes de colocar el pedal.'])+'<p>Si la rosca de la manivela ya está dañada, escríbenos para revisarla.</p>')],
 ['mantenimiento-de-bicicleta-de-spinning-paso-a-paso','bicicleta-spinning-hace-ruido','reparacion-bicicletas-spinning-cali'],W('necesito cambiar los pedales de mi bicicleta de spinning.'))
G('bicicleta-de-spinning-resistencia-no-funciona','La resistencia de la bicicleta de spinning no funciona','Resistencia de bicicleta de spinning no funciona | Técnico Gym',
 'La resistencia de tu bicicleta de spinning no frena o no cambia. Causas en bicicletas de fricción y magnéticas y qué revisar antes de llamar al técnico.',
 'Si al girar la perilla no cambia el esfuerzo, la causa depende del tipo de resistencia de tu bicicleta.',
 [('Bicicleta de fricción',L(['La pastilla de fieltro o caucho está desgastada.','La perilla o el cable de resistencia está flojo o estirado.','La pastilla no toca el volante por una mala posición.'])),
  ('Bicicleta magnética',L(['Imanes desalineados o sueltos.','Cable o perilla de resistencia desajustados.','En modelos con consola, el motor de resistencia no responde.'])),
  ('Qué revisar',O(['Verifica que la perilla gire y que el cable se mueva.','Observa si el cable está suelto o enredado.','En modelos con consola, cambia las pilas o revisa el adaptador.'])+SEG)],
 ['bicicleta-estatica-no-marca-o-sin-resistencia','reparacion-bicicletas-spinning-cali','reparacion-bicicleta-estatica-cali'],W('la resistencia de mi bicicleta de spinning no funciona.'))
G('eliptica-se-siente-floja-o-con-juego','La elíptica se siente floja o con juego','Elíptica floja o con juego: causas y solución | Técnico Gym',
 'Tu elíptica se siente floja, con juego en pedales o brazos o se mueve al usarla. Causas (tornillería, bujes, rodamientos) y cuándo llamar al técnico.',
 'Una elíptica con juego se desgasta más rápido y puede ser insegura.',
 [('Causas',L(['Tornillos de brazos, pedales o estructura flojos.','Bujes o rodamientos desgastados.','Pivotes con holgura.','Patas niveladoras desajustadas.'])),
  ('Qué hacer',O(['Con el equipo detenido, mueve brazos y pedales con la mano para ubicar dónde hay juego.','Aprieta la tornillería que encuentres floja.','Nivela la elíptica.'])+SEG),
  ('Cuándo llamar al técnico','<p>Si el juego persiste después de apretar, hay piezas desgastadas que conviene cambiar antes de que dañen otras. Mira <a href="@el@">reparación de elípticas</a>.</p>')],
 ['eliptica-hace-ruido','reparacion-eliptica-cali','reparacion-escaladora-stepper-cali'],W('mi elíptica se siente floja.'))
G('banco-de-pesas-se-tambalea','El banco de pesas se tambalea','Banco de pesas que se tambalea: causas y solución | Técnico Gym',
 'Tu banco de pesas se tambalea o el respaldo se mueve. Causas, cómo ajustarlo y cuándo es peligroso seguir usándolo. Reparación de bancos en Cali.',
 'Un banco inestable es un riesgo cuando cargas peso. Revisa estos puntos antes de volver a entrenar.',
 [('Causas',L(['Patas desniveladas o piso irregular.','Tornillos flojos en estructura, respaldo o asiento.','Pasador de ajuste desgastado.','Estructura doblada o con fisuras.'])),
  ('Qué hacer',O(['Revisa que el banco esté sobre un piso plano y firme.','Aprieta la tornillería.','Verifica que el respaldo quede trabado antes de cargar peso.'])+SEG),
  ('Cuándo dejar de usarlo','<p>Si el banco está doblado, tiene fisuras o el ajuste no sostiene, no lo uses con carga. Escríbenos: mira la <a href="@banco@">reparación de bancos de pesas</a>.</p>')],
 ['reparacion-banco-de-pesas-cali','retapizado-de-bancos-y-asientos-de-gimnasio-cali','reparacion-torre-de-potencia-cali'],W('mi banco de pesas se tambalea.'))
G('como-limpiar-equipos-de-gimnasio-correctamente','Cómo limpiar equipos de gimnasio correctamente','Cómo limpiar equipos de gimnasio correctamente | Técnico Gym',
 'Cómo limpiar caminadoras, bicicletas, elípticas y multifuncionales sin dañarlas: qué productos usar, qué evitar y cada cuánto limpiar.',
 'Limpiar bien alarga la vida de los equipos. Limpiar mal los daña.',
 [('Reglas generales',L(['Desconecta el equipo antes de limpiar.','Usa un paño ligeramente húmedo, no mojado.','No rocíes líquidos directamente sobre consolas o tarjetas.','Seca después de limpiar.'])),
  ('Por tipo de equipo',L(['<b>Caminadora:</b> limpia la consola, los pasamanos y los costados de la banda; aspira el polvo alrededor del motor.','<b>Bicicletas y elípticas:</b> limpia el sudor del marco, manillar y pedales.','<b>Multifuncionales y bancos:</b> limpia la tapicería y las barras guía con un paño seco.'])),
  ('Qué evitar',L(['Productos agresivos o con mucho alcohol en tapicería y plásticos.','Aceites o aerosoles de petróleo sobre la banda.','Mojar la tarjeta o la consola.'])+SEG)],
 ['rutina-de-mantenimiento-mensual-de-equipos-en-casa','mantenimiento-preventivo-de-caminadoras-cali','mantenimiento-equipos-gimnasio-cali'],W('quiero un mantenimiento completo para mis equipos.'))
G('rutina-de-mantenimiento-mensual-de-equipos-en-casa','Rutina de mantenimiento mensual de equipos de gimnasio en casa','Rutina de mantenimiento mensual de equipos en casa | Técnico Gym',
 'Rutina sencilla de mantenimiento para tus equipos de gimnasio en casa: qué revisar cada semana y cada mes en caminadoras, bicicletas y multifuncionales.',
 'Diez minutos al mes bastan para detectar problemas pequeños antes de que se vuelvan caros.',
 [('Cada semana',L(['Limpia el sudor y el polvo de cada equipo.','Revisa que no haya ruidos nuevos.','Comprueba que los cables no estén pellizcados.'])),
  ('Cada mes',O(['Aprieta la tornillería de caminadoras, bicicletas y bancos.','Revisa la alineación de la banda de la caminadora.','Mira los cables de las multifuncionales: sin hilos sueltos.','Limpia el riel o las guías.','Revisa las pilas de los monitores.'])+SEG),
  ('Cada tres meses',L(['Revisa la lubricación de la caminadora según el manual.','Revisa la transmisión de bicicletas y el desgaste de pastillas.','Considera un <a href="@prev@">mantenimiento preventivo</a> con un técnico.']))],
 ['como-limpiar-equipos-de-gimnasio-correctamente','mantenimiento-preventivo-de-caminadoras-cali','mantenimiento-de-bicicleta-de-spinning-paso-a-paso'],W('quiero un mantenimiento para mis equipos de gimnasio en casa.'))
G('cuanto-dura-una-caminadora','¿Cuánto dura una caminadora?','¿Cuánto dura una caminadora? Vida útil y cuidados | Técnico Gym',
 'Cuánto dura una caminadora según su uso, calidad y mantenimiento. Factores que acortan su vida útil y cómo alargarla. Consejos de técnicos en Cali.',
 'No hay una cifra única: la vida de una caminadora depende de su calidad, su uso y su mantenimiento.',
 [('Qué influye en la duración',L(['La calidad y el tipo de motor.','Las horas de uso al día y el peso de quienes la usan.','La lubricación y la limpieza.','El voltaje de la instalación eléctrica.','La ubicación: humedad, polvo y piso.'])),
  ('Cómo alargar su vida',L(['Hacer mantenimiento preventivo.','Mantener la banda lubricada si el modelo lo requiere.','Conectarla directo a la pared.','Reparar a tiempo ruidos y fallas pequeñas.'])),
  ('¿Reparar o reemplazar?','<p>Depende de la falla, del costo de las piezas y del estado general. Con un diagnóstico podemos darte una recomendación honesta. Mira <a href="@costo@">cuánto cuesta reparar una caminadora</a>.</p>')],
 ['cuanto-cuesta-reparar-una-caminadora','mantenimiento-preventivo-de-caminadoras-cali','usada-que-revisar-antes-de-comprar-una-caminadora'],W('quiero saber si vale la pena reparar mi caminadora.'))

# ---------- ZONAS ADICIONALES ----------
ZN2=[('limonar','Limonar','sur','Limonar es una zona residencial del sur de Cali, con casas y edificios de apartamentos.','Limonar, Gran Limonar, Caney y alrededores','En edificios de la zona avisa si hay ascensor de carga o escaleras para el equipo.'),
('caney','El Caney','sur','El Caney es un sector residencial del sur de Cali, con casas y conjuntos.','El Caney, Limonar, Ciudad 2000 y alrededores','Si vives en un conjunto cerrado, cuéntanos el nombre para coordinar el ingreso.'),
('el-ingenio','El Ingenio','sur','El Ingenio es una zona residencial del sur de Cali.','El Ingenio, Ciudad Jardín, Caney y alrededores','Avísanos el piso y si hay ascensor para ir preparados con el equipo de trabajo.'),
('cuarto-de-legua','Cuarto de Legua','sur','Cuarto de Legua es una zona residencial del sur de Cali, con casas y conjuntos.','Cuarto de Legua, Pance, Capri y alrededores','En casas con equipos en segundo piso, avísanos al coordinar.'),
('capri','Capri','sur','Capri es un barrio del sur de Cali, con casas y edificios.','Capri, Cuarto de Legua, Ciudad Jardín y alrededores','Cuéntanos si el equipo está en una casa o en un apartamento.'),
('gran-limonar','Gran Limonar','sur','Gran Limonar es una zona residencial del sur de Cali, con conjuntos y edificios.','Gran Limonar, Limonar, Cañasgordas y alrededores','En conjuntos cerrados puede requerirse registrar el ingreso del técnico.'),
('tequendama','Tequendama','centro','Tequendama es un barrio del centro-sur de Cali, con casas y edificios.','Tequendama, San Fernando, Centenario y alrededores','En casas antiguas conviene revisar que la instalación eléctrica soporte el equipo.'),
('centenario','Centenario','centro','Centenario es un barrio del centro de Cali, con casas y edificios.','Centenario, San Fernando, Juanambú y alrededores','Avísanos si hay que coordinar el ingreso con la administración.'),
('juanambu','Juanambú','norte','Juanambú es una zona del centro-norte de Cali, con edificios de apartamentos y oficinas.','Juanambú, Granada, Centenario y alrededores','En edificios de apartamentos pregunta a la administración por el horario de ingreso de técnicos.'),
('menga','Menga','norte','Menga es una zona del norte de Cali, con vivienda y zonas comerciales.','Menga, Chipichape, La Flora y alrededores','Cuéntanos si el equipo está en casa, apartamento o en un local.'),
('prados-del-norte','Prados del Norte','norte','Prados del Norte es una zona residencial del norte de Cali.','Prados del Norte, Versalles, Vipasa y alrededores','Avísanos si el equipo está en un piso alto o en un conjunto cerrado.'),
('vipasa','Vipasa','norte','Vipasa es una zona del norte de Cali, con vivienda y comercio.','Vipasa, Chipichape, Prados del Norte y alrededores','Cuéntanos el tipo de equipo y el piso para coordinar la visita.'),
('la-flora','La Flora','norte','La Flora es una zona residencial del norte de Cali.','La Flora, Menga, Vipasa y alrededores','Avísanos si hay que registrar el ingreso en portería.'),
('santa-teresita','Santa Teresita','oeste','Santa Teresita es un barrio residencial del oeste de Cali.','Santa Teresita, Normandía, San Antonio y alrededores','Si el equipo está en una casa con escaleras, avísanos.'),
('arboledas','Arboledas','oeste','Arboledas es una zona residencial del oeste de Cali, con casas y conjuntos.','Arboledas, Santa Teresita, San Antonio y alrededores','Cuéntanos el nombre del conjunto para coordinar el ingreso.')]
ZS2=[]
for slug,nom,pt,desc,cerca,tip in ZN2:
    s='reparacion-de-caminadoras-'+slug+'-cali'; ZS2.append(s)
    add(s,kind='zona',icon='pin',title=f'Reparación de Caminadoras en {nom}, Cali | Técnico Gym',
     desc=f'Técnico de caminadoras y equipos de gimnasio en {nom}, Cali. Reparación a domicilio de caminadoras, bicicletas y multifuncionales. WhatsApp.',
     h1=f'Reparación de caminadoras y equipos de gimnasio en {nom}, Cali',
     lead=f'Atendemos a domicilio en {nom} y alrededores. Escríbenos la marca, el modelo y la falla de tu equipo y coordinamos la visita.',
     wamsg=f'Hola Técnico Gym, necesito reparar un equipo de gimnasio en {nom}, Cali. Equipo: __ Falla: __',
     sections=[(f'Servicio a domicilio en {nom}',f'<p>{desc} Si tienes una caminadora, una bicicleta o cualquier equipo de gimnasio en casa que falle, vamos hasta tu domicilio, revisamos el equipo y te explicamos qué necesita.</p><p>{tip}</p>'),
      ('Equipos que reparamos en la zona','<ul><li><a href="@c@">Caminadoras</a> (no encienden, banda que patina, ruidos, se apagan solas).</li><li><a href="@e@">Bicicletas de spinning y estáticas</a>.</li><li><a href="@m@">Máquinas multifuncionales</a>, estación de poleas, banco de pesas y más.</li></ul><p>Mira todos los <a href="@eq@">equipos que reparamos</a>.</p>'),
      ('Barrios cercanos que atendemos',f'<p>{cerca}. Si no ves tu barrio, escríbenos y lo confirmamos.</p>'),
      ('Cómo coordinamos la visita','<p>Nos escribes por WhatsApp, te orientamos sobre la falla, acordamos el día y la hora, y el técnico revisa el equipo en tu casa. Te informamos la falla y el costo antes de reparar. Conoce el <a href="@proceso@">proceso paso a paso</a>.</p>')],
     faq=[(f'¿Atienden en {nom}?',f'Sí. Atendemos en {nom} y barrios cercanos. Escríbenos tu barrio por WhatsApp y coordinamos la visita.'),(f'¿Qué debo avisar si vivo en un conjunto o edificio de {nom}?','El nombre del conjunto o edificio, el piso y si hay que registrar el ingreso con anticipación.')],
     related=['zonas-de-servicio-cali','reparacion-equipos-gimnasio-a-domicilio-cali','como-trabajamos'])
GUIAS_TODAS=GUIAS_ALL+NG2
ZONAS_TODAS=ZS+ZS2
SERV_NUEVOS=content5.NS; MARCAS=content5.NB
# hubs
PAGES['servicios']=dict(slug='servicios',kind='hub',h1='Servicios de reparación y mantenimiento de equipos de gimnasio en Cali',lead='Servicio técnico, reparación y mantenimiento de caminadoras, bicicletas, elípticas y máquinas multifuncionales.',sections=[],faq=[],related=[],wamsg='Hola Técnico Gym, necesito un servicio para mi equipo de gimnasio en Cali.')
PAGES['marcas']=dict(slug='marcas',kind='hub',h1='Marcas de equipos de gimnasio que reparamos en Cali',lead='Servicio técnico independiente para distintas marcas de caminadoras, bicicletas y multifuncionales.',sections=[],faq=[],related=[],wamsg='Hola Técnico Gym, quiero saber si reparan mi marca de equipo en Cali.')
# zonas: la página general enlaza todas
PAGES['zonas-de-servicio-cali']['sections']=[s for s in PAGES['zonas-de-servicio-cali']['sections'] if s[0]!='Páginas por zona']
PAGES['zonas-de-servicio-cali']['sections'].insert(0,('Páginas por zona','<p>Elige tu zona para ver cómo coordinamos la visita:</p><ul>'+''.join(f'<li><a href="@z_{z}@">{PAGES[z]["h1"].split(" en ")[-1]}</a></li>' for z in ZONAS_TODAS)+'</ul>'))
