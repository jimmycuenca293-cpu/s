# -*- coding: utf-8 -*-
"""Datos propios de cada marca para centrodeserviciotecnicopanama.com.
Cada marca tiene su origen, líneas, tecnologías y fallas por equipo. Nada se comparte entre marcas."""

# equipo -> (slug, nombre singular, plural, artículo)
EQ = {
 "neveras": ("refrigeradoras", "refrigeradora", "refrigeradoras"),
 "lavadoras": ("lavadoras", "lavadora", "lavadoras"),
 "secadoras": ("secadoras", "secadora", "secadoras"),
 "aires": ("aires-acondicionados", "aire acondicionado", "aires acondicionados"),
 "cocinas": ("cocinas-y-hornos", "cocina u horno", "cocinas y hornos"),
 "lavavajillas": ("lavavajillas", "lavavajillas", "lavavajillas"),
 "centro-lavado": ("centros-de-lavado", "centro de lavado", "centros de lavado"),
 "batidoras": ("batidoras", "batidora de pedestal", "batidoras de pedestal"),
 "microondas": ("microondas", "microondas", "microondas"),
}

M = {}

M["samsung"] = dict(
 nombre="Samsung", color="#1428a0", pais="Corea del Sur",
 origen="Samsung Electronics es una empresa surcoreana. En Panamá es la marca de línea blanca con más equipos instalados en apartamentos nuevos, y por eso es la que más visitas técnicas recibe en nuestro centro.",
 lineas=["Family Hub", "Bespoke", "Side by Side", "French Door con Twin Cooling Plus", "EcoBubble", "AddWash", "QuickDrive", "WindFree", "Digital Inverter"],
 equipos=["neveras", "lavadoras", "secadoras", "aires", "cocinas", "lavavajillas", "microondas"],
 tech={
  "neveras": "Casi todos los modelos actuales usan compresor Digital Inverter y, en French Door y Family Hub, el sistema Twin Cooling Plus con dos evaporadores separados, uno para refrigerador y otro para congelador. Esa separación evita mezclar olores, pero duplica los ventiladores y los sensores de deshielo que pueden fallar.",
  "lavadoras": "Los modelos EcoBubble, AddWash y QuickDrive trabajan con motor Digital Inverter de acople directo, sin correa. Eso las hace silenciosas, pero cuando el rodamiento del tambor se desgasta el ruido aparece rápido y el cambio exige abrir el cuba completo.",
  "secadoras": "Las secadoras Samsung más recientes usan sensor de humedad por contacto en el tambor y, en las de bomba de calor, un circuito cerrado con condensador que se tapa con pelusa si no se limpia cada pocos ciclos.",
  "aires": "La serie WindFree reparte el aire por miles de microorificios en lugar de un chorro directo, y los Digital Inverter ajustan la velocidad del compresor. La falla más frecuente en Panamá no es el gas: es la placa de la unidad exterior afectada por picos de voltaje y por el salitre.",
  "cocinas": "Samsung vende cocinas de gas y eléctricas con Flex Duo (un horno que se divide en dos cavidades) y estufas de inducción. Las fallas se concentran en el sensor del horno, el relé de la placa y los quemadores de encendido electrónico.",
  "lavavajillas": "Los lavavajillas Samsung con brazo de rociado WaterWall y secado automático dependen de la bomba de circulación y del sensor de turbidez. Un filtro sucio es la causa de la mayoría de las visitas.",
  "microondas": "Los microondas Samsung con interior cerámico (Ceramic Inside) y modo Slim Fry dependen del magnetrón y del fusible de alta tensión, que se quema cuando el equipo trabaja vacío o por una subida de voltaje.",
 },
 fallas={
  "neveras": [
   ("La refrigeradora enfría el congelador pero no el refrigerador", "El ventilador del evaporador del compartimiento fresco se detuvo, o el conducto de aire se cubrió de hielo por una falla del deshielo.", "Probamos el ventilador del evaporador, la resistencia de deshielo, el sensor de deshielo y el bimetal antes de proponer cambios."),
   ("Hace un zumbido o chasquido fuerte y rítmico", "Casi siempre es el ventilador del congelador rozando hielo acumulado. Si el ruido viene de atrás, puede ser el ventilador del compresor.", "Ubicamos de qué ventilador viene el sonido y revisamos si hay hielo o una aspa golpeando."),
   ("Marca un código en la pantalla y se apaga el enfriamiento", "Un sensor de temperatura dejó de leer bien y la placa corta el ciclo por seguridad.", "Medimos la resistencia de cada sensor contra su tabla y descartamos placa antes de cambiar nada."),
   ("No sale agua ni hielo del dispensador", "Filtro de agua saturado, electroválvula obstruida o línea de agua congelada en la puerta.", "Revisamos filtro, presión de entrada, electroválvula y la resistencia que protege la manguera de la puerta."),
   ("El compresor arranca y se detiene a cada rato", "Placa inverter con problemas por voltaje irregular, o relé de arranque en modelos más viejos.", "Medimos voltaje real del tomacorriente y la señal que la placa envía al compresor."),
  ],
  "lavadoras": [
   ("Hace un ruido metálico fuerte al centrifugar", "Rodamientos del tambor desgastados o amortiguadores sin fuerza.", "Giramos el tambor a mano para sentir juego, revisamos amortiguadores y confirmamos si el cuba permite cambio de rodamiento."),
   ("Se queda con agua en el tambor", "Filtro de la bomba tapado con monedas o pelusa, o bomba de drenaje trabada.", "Abrimos el filtro de drenaje, medimos la bomba y revisamos la manguera de salida."),
   ("Muestra un código de nivel de agua o de fuga", "Sensor de nivel (presostato) o manguera de aire del sensor obstruida; en el código de fuga, agua acumulada en la base.", "Revisamos manguera de presión, presostato y fondo de la base."),
   ("La puerta no abre o no cierra", "Cerradura de puerta o su sensor dañados.", "Probamos el bloqueo eléctrico de la puerta y su conector."),
   ("El tambor no gira o gira con fuerza insuficiente", "Placa del motor inverter, sensor Hall del motor o sobrecarga.", "Medimos el sensor Hall y revisamos la alimentación al motor."),
  ],
  "secadoras": [
   ("Seca muy lento o deja la ropa húmeda", "Condensador o ducto tapado de pelusa, o sensor de humedad sucio.", "Limpiamos el circuito de aire completo y probamos el sensor de humedad."),
   ("Calienta demasiado o se apaga sola", "Termostato de seguridad o resistencia.", "Medimos termostatos y resistencia por separado."),
   ("Hace ruido al girar", "Rodillos de apoyo o correa del tambor.", "Revisamos rodillos, polea tensora y correa."),
   ("Muestra error de drenaje de condensado", "Depósito lleno o bomba de condensado obstruida (modelos con bomba de calor).", "Revisamos depósito, bomba y manguera de condensado."),
  ],
  "aires": [
   ("Enciende pero no enfría", "Falta de gas por fuga o filtro y serpentín muy sucios; en inverter también una falla del sensor de temperatura.", "Medimos presión, temperatura de entrada y salida y estado del serpentín antes de hablar de gas."),
   ("Gotea agua dentro de la casa", "Drenaje tapado o mala pendiente en la instalación.", "Destapamos el drenaje y revisamos la pendiente de la manguera."),
   ("Código de error en la pantalla de la unidad interior", "Falla de comunicación entre unidad interior y exterior, o sensor.", "Revisamos cableado entre unidades y la placa exterior."),
   ("Se apaga con tormentas o apagones", "La placa inverter exterior se dañó por picos de voltaje.", "Medimos la placa y recomendamos protección de voltaje."),
  ],
  "cocinas": [
   ("El horno no calienta o calienta mal", "Resistencia, sensor de temperatura o relé de la placa.", "Probamos resistencia y sensor con multímetro y revisamos el relé."),
   ("La estufa no enciende los quemadores", "Bujías sucias o módulo de encendido.", "Limpiamos y probamos bujías y módulo."),
   ("La inducción marca error o apaga zonas", "Bobina o ventilador de la placa por calor excesivo.", "Revisamos ventilación y bobina de la zona afectada."),
  ],
  "lavavajillas": [
   ("No drena y deja agua en el fondo", "Filtro tapado o bomba de drenaje.", "Limpiamos filtro y medimos la bomba."),
   ("No lava bien o deja residuos blancos", "Brazos rociadores obstruidos, sensor o dureza del agua.", "Revisamos brazos, bomba de circulación y sensor."),
  ],
  "microondas": [
   ("Gira pero no calienta", "Magnetrón, diodo o fusible de alta tensión.", "Verificamos el fusible, diodo y capacitor antes de cambiar el magnetrón."),
   ("Hace chispas dentro", "Placa guía de ondas quemada o interior dañado.", "Revisamos la placa guía y el interior."),
  ],
 },
 codigos={
  "Lavadoras": [("4E / 4C", "No entra agua: llave cerrada, filtro de la entrada o electroválvula."), ("5E / 5C", "No drena: filtro de la bomba tapado o bomba."), ("UE / Ud", "Carga desbalanceada: la lavadora no puede centrifugar."), ("dE / dC", "Puerta mal cerrada o falla del sensor de puerta."), ("LE / LC", "Detectó agua de más o una fuga."), ("HE / HC", "Problema en el calentador o su sensor."), ("3E / 3C", "Motor o su sensor Hall."), ("SUD / SUDS", "Exceso de espuma: se usó demasiado detergente.")],
  "Refrigeradoras": [("22E / 21E", "Ventilador del congelador (evaporador), frecuentemente por hielo."), ("5E / 1E", "Sensor de temperatura del evaporador o del congelador."), ("84C / 85C", "Fallas de la placa de control o comunicación; se revisa con técnico."), ("Luz de filtro de agua", "No es falla: es el aviso de cambio de filtro cada seis meses.")],
 },
 mantenimiento=["Limpiar el filtro de la bomba de la lavadora cada dos o tres meses.", "Desmontar y limpiar el condensador de la secadora de bomba de calor cada 10 ciclos.", "Cambiar el filtro de agua de la refrigeradora cada seis meses; con agua dura, cada cuatro.", "Limpiar filtros del aire WindFree cada mes en uso diario.", "Usar protector de voltaje en aires y neveras con placa inverter."],
 etiqueta={"neveras": "En el lado interior izquierdo del refrigerador, cerca de las repisas; en Family Hub, también en el menú de la pantalla.", "lavadoras": "En el borde interior de la puerta, o en la parte posterior del equipo.", "secadoras": "En el borde interior de la puerta.", "aires": "Sobre la unidad exterior, junto a las conexiones, y en la unidad interior bajo el panel frontal."},
 modelo_ej="Los modelos Samsung de refrigeradora empiezan por RF, RS, RT o RB; las lavadoras por WA, WW o WF; los aires por AR.",
 garantia="Los equipos Samsung nuevos suelen traer garantía de fábrica de un año en la mayoría del equipo y más años para el compresor Digital Inverter, según el modelo y el país de compra. Confirma el tiempo exacto en la factura o el certificado de tu equipo.",
 faq=[("¿Cómo sé si el error de mi lavadora Samsung es grave?", "Los códigos 4E, 5E y UE son los más comunes y casi siempre se resuelven limpiando filtros, revisando llaves o reacomodando la carga. Si el código vuelve tras apagar y encender el equipo, hace falta una revisión."), ("¿Reparan neveras Samsung Family Hub?", "Sí. Revisamos la parte de enfriamiento y la pantalla. Si la falla es de software de la pantalla, se orienta al usuario sobre actualización o restablecimiento de fábrica."), ("¿Atienden aires WindFree?", "Sí, incluyendo la limpieza de los microorificios del panel frontal, que se tapan con polvo y grasa de cocina.")],
)

M["lg"] = dict(
 nombre="LG", color="#a50034", pais="Corea del Sur",
 origen="LG Electronics, de Corea del Sur, es la marca más reconocida por sus lavadoras de carga frontal y sus neveras con compresor lineal. En Panamá se ve mucho en apartamentos y en casas con lavandería interna.",
 lineas=["InstaView", "Door-in-Door", "Smart Inverter", "Linear Compressor", "TurboWash", "TwinWash", "WashTower", "Dual Inverter", "Direct Drive"],
 equipos=["neveras", "lavadoras", "secadoras", "centro-lavado", "aires", "lavavajillas"],
 tech={
  "neveras": "LG usa compresor inverter (Smart Inverter) y, en varias series, compresor lineal, que se mueve con un pistón en lugar de un cigüeñal. Es muy silencioso y eficiente, pero cuando la placa inverter falla el equipo deja de enfriar de golpe en vez de hacer ruido.",
  "lavadoras": "LG fabrica las lavadoras con motor Direct Drive acoplado al tambor, sin correa. Sus códigos de error son más cortos y fáciles de interpretar que en otras marcas, y la más conocida es OE por drenaje. Los modelos TurboWash y TwinWash suman válvulas y bombas adicionales.",
  "secadoras": "Las secadoras LG de bomba de calor (Dual Inverter HeatPump) secan a menor temperatura. El condensador y el filtro se tapan de pelusa, y eso pasa más rápido en Panamá, donde la ropa seca arrastra pelusa de toallas y sábanas nuevas.",
  "centro-lavado": "El WashTower une lavadora y secadora en una sola columna con panel central compartido. Una falla de comunicación entre las dos unidades puede apagar las dos aunque solo una esté dañada.",
  "aires": "Los aires LG Dual Inverter regulan el compresor y el ventilador con dos inverters. Las fallas típicas en el trópico son sensor de temperatura, drenaje y placa exterior afectada por la humedad.",
  "lavavajillas": "Los lavavajillas LG QuadWash usan cuatro brazos giratorios y un motor inverter silencioso. El filtro y la bomba de drenaje son la causa de la mayoría de las llamadas.",
 },
 fallas={
  "neveras": [
   ("Dejó de enfriar por completo y no hace ruido", "Placa inverter del compresor o compresor lineal sin arranque.", "Medimos la salida de la placa al compresor y la resistencia del bobinado."),
   ("Hace un zumbido que sube y baja", "Ventilador del evaporador o hielo acumulado en el ducto.", "Revisamos ventilador y la resistencia de deshielo."),
   ("La pantalla muestra Er FF o Er dF", "FF apunta al ventilador del congelador; dF a una falla del ciclo de deshielo.", "Probamos ventilador y sensor de deshielo; si se repite, revisamos la placa."),
   ("Gotea agua adentro del refrigerador", "Drenaje del evaporador congelado o tapado.", "Descongelamos el drenaje y revisamos la resistencia."),
   ("El dispensador de agua no funciona", "Filtro, electroválvula o línea congelada.", "Revisamos filtro, presión y electroválvula."),
  ],
  "lavadoras": [
   ("Muestra OE y se queda con agua", "OE significa que no puede drenar: filtro de la bomba tapado o bomba bloqueada.", "Abrimos el filtro, limpiamos y medimos la bomba."),
   ("Muestra IE", "IE es agua que no entra bien: llave cerrada, filtros de la entrada sucios o válvula.", "Revisamos las mallas de entrada y las válvulas."),
   ("Muestra UE y no centrifuga", "Carga desbalanceada.", "Se acomoda la carga; si se repite, se revisa el nivel y los amortiguadores."),
   ("Muestra dE", "Puerta no detectada como cerrada, o cerradura dañada.", "Probamos el interruptor de puerta y la cerradura."),
   ("Muestra LE o PE", "LE es motor bloqueado o sobrecarga; PE es el sensor de nivel de agua.", "Medimos el motor, el sensor Hall y la manguera del presostato."),
   ("Ruido fuerte al centrifugar", "Rodamientos o amortiguadores.", "Revisamos el juego del tambor."),
  ],
  "secadoras": [
   ("No seca bien", "Filtro, condensador o ducto obstruidos.", "Limpiamos todo el recorrido del aire."),
   ("No enciende", "Placa o fusible térmico.", "Probamos el fusible térmico y la alimentación."),
   ("Muestra error de condensado", "Depósito lleno o bomba.", "Revisamos el depósito y la bomba."),
  ],
  "centro-lavado": [
   ("Una unidad funciona y la otra no", "Falla de comunicación entre unidades.", "Probamos el cableado y la placa principal."),
   ("El panel central no responde", "Panel o conexión.", "Reiniciamos el equipo y revisamos conectores."),
  ],
  "aires": [
   ("Muestra código en la unidad interior", "Comunicación o sensor.", "Revisamos el cable entre unidades y sensores."),
   ("No enfría bien", "Gas, filtro o serpentín sucio.", "Medimos presión y temperatura de salida."),
   ("Gotea agua", "Drenaje tapado.", "Destapamos el drenaje."),
  ],
  "lavavajillas": [
   ("No drena", "Filtro o bomba.", "Limpiamos filtro y medimos bomba."),
   ("No limpia bien", "Brazos rociadores tapados.", "Revisamos brazos y el sensor."),
  ],
 },
 codigos={
  "Lavadoras": [("OE", "No drena: filtro o bomba de drenaje."), ("IE", "No entra suficiente agua: llave, filtros o válvula."), ("UE", "Carga desbalanceada."), ("dE / dE1 / dE2", "Puerta abierta o cerradura con falla."), ("LE", "Motor bloqueado o con sobrecarga."), ("PE", "Falla del sensor de nivel de agua (presostato)."), ("FE", "Exceso de agua dentro de la tina."), ("tE", "Sensor de temperatura del calentador."), ("CL", "Bloqueo de niños activo; no es falla.")],
  "Refrigeradoras": [("Er FF", "Ventilador del congelador."), ("Er dF", "Ciclo de deshielo."), ("Er IF", "Ventilador del hielo."), ("Er rt", "Sensor de temperatura del refrigerador.")],
 },
 mantenimiento=["Limpiar el filtro de drenaje de la lavadora una vez al mes si se lava ropa con mucha pelusa.", "Dejar la puerta de la lavadora entreabierta después de usarla para evitar moho en el empaque.", "Limpiar el filtro y el condensador de la secadora de bomba de calor.", "Usar protector de voltaje para los equipos con compresor inverter."],
 etiqueta={"neveras": "En el lado interior del refrigerador, en la pared izquierda o derecha, o detrás de la repisa inferior.", "lavadoras": "En la parte trasera o en el borde interior de la puerta.", "secadoras": "Borde interior de la puerta.", "aires": "En la unidad interior, bajo el panel frontal."},
 modelo_ej="Los números de modelo LG suelen empezar por GM, GR o LT en refrigeradoras, WM o WT en lavadoras y DLE o RH en secadoras.",
 garantia="LG ofrece garantía de fábrica estándar y, en algunos modelos, garantía extendida para el compresor inverter. El plazo depende del modelo y de la tienda donde lo compraste; conserva la factura.",
 faq=[("¿Qué significa OE en mi lavadora LG?", "Significa que la lavadora no logra sacar el agua. Casi siempre es el filtro de la bomba tapado; se limpia sin herramientas especiales."), ("¿Reparan WashTower?", "Sí. Diagnosticamos lavadora y secadora por separado y revisamos la comunicación entre ambas."), ("¿Las neveras con compresor lineal se reparan en casa?", "El diagnóstico sí. El cambio del compresor se coordina según el modelo y el estado del equipo.")],
)

M["whirlpool"] = dict(
 nombre="Whirlpool", color="#f2a900", pais="Estados Unidos",
 origen="Whirlpool es una compañía estadounidense. En Panamá se ve mucho en lavadoras de carga superior con agitador, que son resistentes y de mecánica sencilla, y en refrigeradoras de dos puertas con dispensador.",
 lineas=["Xpert System", "Cabrio", "Duet", "6th Sense", "Side by Side"],
 equipos=["neveras", "lavadoras", "secadoras", "cocinas", "lavavajillas"],
 tech={
  "neveras": "Las refrigeradoras Whirlpool son, en su mayoría, de ciclo mecánico-electrónico: un termostato o control electrónico decide el deshielo con un temporizador. Ese temporizador, el termostato de deshielo y el ventilador son los tres repuestos que más se cambian.",
  "lavadoras": "Whirlpool tiene dos mundos: la carga superior con agitador y transmisión mecánica (embrague, buje y tapa), y la carga frontal Duet con motor y correa. Las fallas del primero son mecánicas y se ven; las del segundo son electrónicas.",
  "secadoras": "Las secadoras Whirlpool eléctricas y a gas dependen del termostato de corte, el fusible térmico y la correa del tambor. La mayoría de los fallos de calentamiento son una resistencia o un fusible térmico cortado.",
  "cocinas": "Whirlpool fabrica estufas y hornos con control analógico y también con pantalla táctil. Los sensores del horno, el interruptor de selección y los quemadores son los repuestos habituales.",
  "lavavajillas": "Los lavavajillas Whirlpool empotrables usan bomba de dos funciones (circulación y drenaje). Una pieza pequeña, el sello de la puerta, también causa goteo.",
 },
 fallas={
  "neveras": [
   ("Se forma hielo en el congelador y el refrigerador no enfría", "El deshielo no está funcionando: temporizador, resistencia o termostato de deshielo.", "Probamos el ciclo de deshielo completo con multímetro."),
   ("Zumbido en la parte de atrás", "Ventilador del condensador con polvo.", "Limpiamos el condensador y revisamos el ventilador."),
   ("El dispensador gotea o no despacha", "Electroválvula o filtro.", "Revisamos la entrada de agua y filtro."),
   ("Se enciende y apaga el compresor cada pocos minutos", "Relé de arranque o protector térmico.", "Probamos el relé y el capacitor."),
  ],
  "lavadoras": [
   ("Llena de agua pero el agitador no se mueve", "Embrague, buje de transmisión o bandas.", "Retiramos el agitador y revisamos el conjunto del buje y del embrague."),
   ("No centrifuga con la tapa cerrada", "Interruptor de tapa.", "Probamos el interruptor y el actuador de tapa."),
   ("Se detiene a mitad del ciclo con un código F", "F5E1 y F8E1 aparecen con problemas de drenaje o de llenado de agua.", "Revisamos manguera, válvulas y bomba."),
   ("Hace ruido de golpe en carga frontal Duet", "Amortiguadores o rodamientos.", "Revisamos suspensión y rodamientos."),
  ],
  "secadoras": [
   ("Gira pero no calienta", "Fusible térmico o resistencia.", "Medimos continuidad en el fusible, termostato y resistencia."),
   ("El tambor no gira", "Correa rota.", "Abrimos y cambiamos la correa y el rodillo tensor."),
   ("Se apaga a los pocos minutos", "Ducto tapado por pelusa y termostato de seguridad.", "Limpiamos el ducto y probamos el termostato."),
  ],
  "cocinas": [
   ("El horno no calienta", "Resistencia o sensor.", "Probamos ambos con multímetro."),
   ("Un quemador eléctrico no calienta", "Elemento o interruptor selector.", "Probamos el elemento y el interruptor."),
  ],
  "lavavajillas": [
   ("Gotea por la puerta", "Sello de la puerta.", "Revisamos el sello y el nivel."),
   ("No drena", "Filtro o bomba.", "Limpiamos y medimos la bomba."),
  ],
 },
 codigos={
  "Lavadoras": [("F5E1", "Tiempo de drenaje prolongado: manguera doblada, filtro o bomba."), ("F8E1", "Tiempo de llenado prolongado: llave cerrada, mallas de entrada o válvula."), ("F7E1", "Problema con el motor o su control."), ("LD", "Tapa abierta o interruptor de tapa."), ("Sd / SUD", "Exceso de espuma.")],
  "Refrigeradoras": [("Luz de filtro de agua", "Aviso de cambio de filtro; no es falla."), ("Alarma de puerta", "Puerta mal cerrada o empaque dañado.")],
 },
 mantenimiento=["Limpiar la parte trasera de la refrigeradora cada seis meses.", "Revisar el empaque de la puerta con una hoja de papel: si sale sin resistencia, el empaque ya no sella.", "Limpiar el ducto de la secadora cada año.", "Cambiar las mangueras de entrada de la lavadora cada cinco años."],
 etiqueta={"neveras": "Dentro del refrigerador, en el costado o en el techo interior.", "lavadoras": "En la parte trasera o bajo la tapa en carga superior.", "secadoras": "En el borde interior de la puerta."},
 modelo_ej="Los modelos de Whirlpool suelen empezar por WRS, WRT o WRX en refrigeradoras y WTW o WFW en lavadoras.",
 garantia="Whirlpool entrega garantía de fábrica por tiempo limitado en el equipo y garantías más largas para piezas específicas según el modelo. El plazo cambia por país, así que lo exacto está en tu factura.",
 faq=[("¿La lavadora Whirlpool no centrifuga, es el motor?", "Con tapa cerrada, lo más común es el interruptor de tapa. El motor falla mucho menos."), ("¿Qué es F5E1?", "Es un código de drenaje lento: se revisa manguera, filtro y bomba."), ("¿Arreglan refrigeradoras Whirlpool de dos puertas?", "Sí, y los temas más comunes son el deshielo y el ventilador del evaporador.")],
)

M["mabe"] = dict(
 nombre="Mabe", color="#0b5d8a", pais="México",
 origen="Mabe es una empresa mexicana que fabrica electrodomésticos para Latinoamérica. Sus equipos están muy extendidos en Panamá en hogares de clase media.",
 lineas=["Refrigeradoras No Frost", "Lavadoras de carga superior", "Torres de lavado y secado", "Aires Tecinverter", "Cocinas a gas", "Centros de lavado"],
 equipos=["neveras", "lavadoras", "centro-lavado", "aires", "cocinas"],
 tech={
  "neveras": "Las refrigeradoras Mabe no frost circulan aire frío con un ventilador y descongelan el evaporador con una resistencia. Para el usuario, la falla clásica es que se acumula hielo en el fondo del congelador y el refrigerador se calienta.",
  "lavadoras": "Mabe fabrica lavadoras de carga superior con agitador de ciclos largos y gran capacidad, hasta 22 kg. Sus piezas mecánicas son resistentes, y los fallos más comunes se concentran en la transmisión, la bomba y el interruptor de tapa.",
  "centro-lavado": "Las torres de lavado y secado Mabe tienen un solo mueble con lavadora abajo y secadora arriba. Las dos unidades comparten la conexión eléctrica, así que un problema de alimentación afecta a ambas.",
  "aires": "Los aires Mabe Tecinverter usan compresor inverter. En zonas costeras de Panamá el condensador exterior se corroe antes que el compresor.",
  "cocinas": "Las cocinas Mabe a gas son de las más comunes en Panamá, con quemadores sellados y horno a gas con termostato de bulbo.",
 },
 fallas={
  "neveras": [
   ("Hielo en el fondo del congelador y refrigerador tibio", "Resistencia de deshielo o terminador de deshielo.", "Probamos la resistencia y el terminador; verificamos el drenaje."),
   ("El compresor se calienta y se apaga", "Relé o protector térmico.", "Medimos la corriente de arranque del compresor."),
   ("La puerta no sella", "Empaque deformado o bisagras flojas.", "Revisamos empaque y alineación."),
  ],
  "lavadoras": [
   ("No agita aunque llena", "Transmisión, correa o motor.", "Revisamos la correa y el embrague."),
   ("No desagua", "Bomba o manguera.", "Limpiamos y medimos la bomba."),
   ("Se detiene a medio ciclo", "Tarjeta o interruptor de tapa.", "Probamos el interruptor y la tarjeta."),
   ("Fuga de agua por debajo", "Manguera interna o tina.", "Seguimos el recorrido del agua."),
  ],
  "centro-lavado": [
   ("Ninguna de las dos unidades enciende", "Alimentación eléctrica compartida.", "Medimos voltaje y breaker."),
   ("La secadora no calienta", "Resistencia.", "Probamos resistencia y termostato."),
  ],
  "aires": [
   ("No enfría", "Gas o sensor.", "Medimos presiones y temperaturas."),
   ("Placa exterior dañada por tormentas", "Picos de voltaje.", "Medimos la placa."),
  ],
  "cocinas": [
   ("El horno no enciende", "Termostato o válvula.", "Probamos el termostato de bulbo y la válvula."),
   ("Un quemador no enciende", "Bujía o inyector tapado.", "Limpiamos el inyector."),
  ],
 },
 codigos={},
 mantenimiento=["Descongelar manualmente cada seis meses si el equipo no es no frost.", "Limpiar el condensador exterior del aire con agua a baja presión.", "Revisar el empaque del refrigerador cada año.", "Limpiar el filtro de pelusa de la torre de lavado en cada ciclo."],
 etiqueta={"neveras": "En el interior, en un costado del refrigerador.", "lavadoras": "En la parte trasera o en el panel superior.", "aires": "En la unidad interior, bajo el panel."},
 modelo_ej="En Mabe, el número de modelo suele incluir letras del tipo de equipo y capacidad, y se encuentra junto al número de serie.",
 garantia="Mabe ofrece garantía de fábrica por tiempo limitado, que varía según el producto y el país. Conserva la factura y el certificado.",
 faq=[("¿Reparan lavadoras Mabe de 22 kg?", "Sí. Las de gran capacidad tienen transmisión robusta y las fallas se diagnostican en casa."), ("¿Los aires Tecinverter se reparan en casa?", "El diagnóstico y la mayoría de las reparaciones se hacen en el sitio.")],
)

M["frigidaire"] = dict(
 nombre="Frigidaire", color="#c8102e", pais="Estados Unidos",
 origen="Frigidaire es una marca estadounidense. En Panamá se ve en lavadoras de carga frontal, estufas y refrigeradoras de gran tamaño, muchas veces compradas por importación.",
 lineas=["Gallery", "Professional", "Centros de lavado", "Refrigeradoras con panel Inverter", "JetClean"],
 equipos=["neveras", "lavadoras", "secadoras", "cocinas", "centro-lavado"],
 tech={
  "neveras": "Las refrigeradoras Frigidaire grandes usan tarjetas de control y paneles táctiles que son sensibles a los picos de voltaje. Algunos modelos usan compresor inverter.",
  "lavadoras": "Las lavadoras Frigidaire de carga frontal y con panel JetClean limpian con agua a presión. Dependen de válvulas de entrada y de bomba de drenaje.",
  "secadoras": "Las secadoras Frigidaire eléctricas y a gas usan sensor de humedad y termostato de seguridad. El ducto largo de ventilación es la causa más habitual del sobrecalentamiento.",
  "cocinas": "Las estufas Frigidaire con horno de convección tienen ventilador y resistencia adicionales, que son los que fallan primero.",
  "centro-lavado": "Los centros de lavado Frigidaire tienen lavadora y secadora apiladas con un solo panel de control.",
 },
 fallas={
  "neveras": [
   ("Pantalla en blanco o botones sin respuesta", "Tarjeta de control afectada por voltaje.", "Medimos alimentación y revisamos la tarjeta."),
   ("No enfría en el refrigerador", "Ventilador o deshielo.", "Probamos el ventilador y el ciclo de deshielo."),
   ("Ruido fuerte intermitente", "Ventilador con hielo.", "Revisamos y descongelamos."),
  ],
  "lavadoras": [
   ("Código E20 o de drenaje", "Bomba o filtro.", "Limpiamos el filtro y medimos la bomba."),
   ("Código E10 o de llenado", "Llave o válvula.", "Revisamos la entrada de agua."),
   ("Código E40 de puerta", "Cerradura de puerta.", "Probamos cerradura y traba."),
   ("Ruido fuerte en el centrifugado", "Rodamiento.", "Revisamos juego y suspensión."),
  ],
  "secadoras": [
   ("No calienta", "Resistencia o termostato.", "Medimos continuidad."),
   ("Tarda más de un ciclo en secar", "Ducto tapado.", "Limpiamos el ducto."),
  ],
  "cocinas": [
   ("El horno no calienta", "Resistencia o sensor.", "Probamos resistencia y sensor."),
   ("La resistencia de convección no funciona", "Ventilador o resistencia.", "Revisamos ventilador y resistencia."),
  ],
  "centro-lavado": [
   ("Una unidad no responde", "Tarjeta.", "Revisamos la tarjeta y los conectores."),
   ("La secadora no calienta", "Resistencia.", "Probamos la resistencia."),
  ],
 },
 codigos={"Lavadoras": [("E10", "Problema de llenado de agua."), ("E20", "Problema de drenaje."), ("E40", "Puerta abierta o cerradura."), ("E50 / E51", "Problema de motor o control del motor."), ("E66", "Problema del nivel de agua.")]},
 mantenimiento=["Limpiar el ducto de la secadora cada año.", "Limpiar el filtro de drenaje de la lavadora cada dos meses.", "Proteger el panel táctil de la refrigeradora con regulador de voltaje.", "Limpiar el condensador cada seis meses."],
 etiqueta={"neveras": "Dentro del refrigerador, en el costado superior.", "lavadoras": "En la parte trasera o en el borde de la puerta.", "cocinas": "Bajo el cajón del horno o en el marco frontal."},
 modelo_ej="Los modelos Frigidaire usan prefijos como FFHT, FGHB o FFFC.",
 garantia="Frigidaire ofrece garantía limitada de fábrica, que cambia con el país de compra. Los equipos importados pueden no tener cobertura local.",
 faq=[("¿Reparan equipos Frigidaire importados?", "Sí. Revisamos el equipo y te explicamos con claridad si hay repuestos disponibles en Panamá."), ("¿Qué significa E20 en mi lavadora Frigidaire?", "Es un código de drenaje: se limpia el filtro y se prueba la bomba."), ("¿Dónde encuentro el modelo de mi equipo Frigidaire?", "En una etiqueta dentro del refrigerador o en el marco de la puerta de la lavadora; con una foto adelantamos el diagnóstico.")],
)

M["electrolux"] = dict(
 nombre="Electrolux", color="#001e50", pais="Suecia",
 origen="Electrolux es una compañía sueca de electrodomésticos. En Panamá se encuentra en refrigeradoras inverter, lavadoras de carga superior y frontal, y hornos o placas de inducción.",
 lineas=["Perfect Care", "Inverter", "Frost Free", "Placas de inducción", "Hornos empotrados"],
 equipos=["neveras", "lavadoras", "cocinas", "secadoras"],
 tech={
  "neveras": "Las refrigeradoras Electrolux inverter y Frost Free dependen de sensores de temperatura y de una placa electrónica que controla el compresor. Cuando falla un sensor, la placa puede dejar de enfriar aunque el compresor esté bien.",
  "lavadoras": "Las lavadoras Electrolux de carga frontal con sistema Perfect Care usan sensores de carga y de suciedad. Sus códigos de error empiezan con la letra E.",
  "cocinas": "Los hornos empotrados y las placas de inducción Electrolux tienen sensores de temperatura y ventiladores de enfriamiento de la electrónica. Cuando el ventilador se obstruye, la placa apaga zonas para protegerse.",
  "secadoras": "Las secadoras Electrolux de condensación y de bomba de calor necesitan limpiar filtros y el intercambiador con regularidad.",
 },
 fallas={
  "neveras": [
   ("No enfría y el compresor no arranca", "Placa inverter o sensor.", "Probamos placa, sensor y compresor."),
   ("Ruido de ventilador", "Ventilador con hielo.", "Revisamos el ventilador y el deshielo."),
   ("Alarma de puerta constante", "Interruptor o empaque.", "Revisamos el interruptor y el sello."),
  ],
  "lavadoras": [
   ("Código E10", "Problema de entrada de agua.", "Revisamos llave, mallas y válvula."),
   ("Código E20", "Problema de drenaje.", "Limpiamos filtro y bomba."),
   ("Código E40", "Puerta mal cerrada.", "Revisamos cerradura."),
   ("Ruido en el centrifugado", "Rodamientos.", "Medimos el juego del tambor."),
  ],
  "cocinas": [
   ("La placa de inducción apaga zonas", "Ventilador o sensor.", "Revisamos ventilación y sensores."),
   ("El horno no calienta", "Resistencia o sensor.", "Probamos ambos."),
  ],
  "secadoras": [
   ("Seca lento", "Filtro o condensador.", "Limpiamos y probamos."),
   ("Se apaga sola", "Termostato.", "Medimos el termostato."),
  ],
 },
 codigos={"Lavadoras": [("E10", "La lavadora Electrolux no recibe agua suficiente: llave cerrada, mallas de entrada sucias o electroválvula."), ("E20", "El agua no sale: se revisa la manguera de desagüe, el filtro y la bomba de la lavadora."), ("E40", "El equipo no detecta la puerta cerrada: empaque, traba o interruptor de puerta."), ("E50", "Problema en el motor o en su sensor de giro."), ("E90", "Falla de comunicación entre la placa y el panel de control.")]},
 mantenimiento=["Limpiar el filtro de la bomba cada dos o tres meses.", "Limpiar los filtros de la secadora en cada uso.", "No obstruir las rejillas de ventilación de las placas.", "Usar regulador de voltaje en las refrigeradoras inverter."],
 etiqueta={"neveras": "Dentro del refrigerador, en el costado.", "lavadoras": "En el marco de la puerta o atrás.", "cocinas": "En el borde del horno, al abrir la puerta."},
 modelo_ej="Electrolux usa códigos como IT, IM o ERT en neveras y EWF en lavadoras.",
 garantia="Electrolux ofrece garantía de fábrica limitada y varía por país y modelo.",
 faq=[("¿Reparan placas de inducción Electrolux?", "Sí, revisando ventilador, bobina y sensores."), ("¿Qué es E20 en una lavadora Electrolux?", "Es un código de drenaje."), ("¿La refrigeradora inverter Electrolux se reinicia sola?", "Puede ser por picos de voltaje o por una falla del sensor; se revisa en casa.")],
)

M["general-electric"] = dict(
 nombre="General Electric", color="#005eb8", pais="Estados Unidos",
 origen="General Electric (GE Appliances) es una marca estadounidense. En Panamá se encuentran con frecuencia sus refrigeradoras, lavavajillas y hornos empotrados.",
 lineas=["GE Profile", "Café", "Monogram", "Unitized Spacemaker", "Lavavajillas con tecnología Piranha"],
 equipos=["neveras", "lavadoras", "lavavajillas", "cocinas", "centro-lavado"],
 tech={
  "neveras": "Las refrigeradoras GE, especialmente French Door y Side by Side, tienen dispensador de agua y hielo, tarjeta electrónica y a veces ventilador doble. Los problemas del dispensador son los más reportados.",
  "lavadoras": "GE produce lavadoras de carga superior con agitador y de carga frontal. Son resistentes, y los repuestos de la transmisión son comunes.",
  "lavavajillas": "Los lavavajillas GE suelen traer un triturador de residuos (Piranha) y filtro autolimpiante. El triturador puede atascarse con huesos pequeños o vidrio.",
  "cocinas": "Los hornos y estufas GE tienen sensores y relés que se desgastan; los modelos Profile y Café sumen convección.",
  "centro-lavado": "El Unitized Spacemaker GE junta lavadora y secadora en un solo mueble, común en apartamentos.",
 },
 fallas={
  "neveras": [
   ("El dispensador no entrega hielo", "Fábrica de hielo o electroválvula.", "Revisamos molde, motor y válvula."),
   ("El refrigerador no enfría", "Ventilador del evaporador.", "Probamos el ventilador y el ciclo de deshielo."),
   ("Gotea agua en el piso", "Drenaje o línea de agua.", "Revisamos el drenaje y las conexiones."),
  ],
  "lavadoras": [
   ("No agita", "Transmisión o acoplamiento.", "Revisamos el acople del motor."),
   ("No desagua", "Bomba.", "Limpiamos y medimos la bomba."),
  ],
  "lavavajillas": [
   ("No drena", "Filtro o triturador atascado.", "Limpiamos el triturador y el filtro."),
   ("Deja residuos", "Brazos rociadores o bomba.", "Revisamos brazos y bomba."),
  ],
  "cocinas": [
   ("El horno no calienta", "Resistencia o sensor.", "Probamos ambos."),
   ("La estufa no enciende", "Bujía o módulo.", "Limpiamos y probamos."),
  ],
  "centro-lavado": [
   ("La secadora no calienta", "Resistencia.", "Probamos."),
   ("La lavadora no centrifuga", "Interruptor de tapa o motor.", "Probamos ambos."),
  ],
 },
 codigos={},
 mantenimiento=["Cambiar el filtro de agua cada seis meses.", "Limpiar el filtro del lavavajillas cada mes.", "Limpiar el condensador de la refrigeradora cada seis meses.", "Revisar el ducto de la secadora cada año."],
 etiqueta={"neveras": "Dentro del refrigerador, en el costado superior.", "lavavajillas": "En el borde interior de la puerta."},
 modelo_ej="Los modelos GE comienzan con letras como GSS o GNE en refrigeradoras y GDT en lavavajillas.",
 garantia="GE ofrece garantía limitada de fábrica que varía por producto y país.",
 faq=[("¿Reparan lavavajillas GE con triturador?", "Sí, incluyendo la limpieza del triturador."), ("¿Qué marcas de piezas usan para GE?", "Usamos repuestos originales cuando están disponibles en Panamá y compatibles de calidad cuando no, y te lo decimos antes de reparar."), ("¿El dispensador de hielo GE se puede arreglar?", "Sí, la mayoría de las veces es la electroválvula o el molde.")],
)

M["haceb"] = dict(
 nombre="Haceb", color="#00833e", pais="Colombia",
 origen="Haceb es una marca colombiana de electrodomésticos, muy extendida en Panamá en refrigeradoras, lavadoras, estufas y hornos de gas. Muchos equipos llegan por importación y comparten repuestos con modelos vendidos en Colombia.",
 lineas=["Neveras no frost", "Lavadoras carga superior", "Estufas a gas", "Hornos empotrables", "Aires acondicionados"],
 equipos=["neveras", "lavadoras", "secadoras", "cocinas", "aires"],
 tech={
  "neveras": "Las neveras Haceb no frost usan un ciclo de deshielo electrónico. La falla más frecuente es el termostato o sensor de deshielo.",
  "lavadoras": "Las lavadoras Haceb de carga superior con agitador son de mecánica sencilla y fáciles de reparar. Las fallas son de correa, bomba y tarjeta.",
  "secadoras": "Las secadoras Haceb de carga frontal secan con aire caliente y un tambor giratorio. El filtro de pelusa y el ducto de salida son lo que más condiciona el rendimiento, y en equipos de gran capacidad como los de 12 kg la pelusa se acumula rápido.",
  "cocinas": "Las estufas y hornos Haceb funcionan a gas con encendido eléctrico. Las bujías y las válvulas son lo que más se cambia.",
  "aires": "Los aires Haceb tienen compresor on/off o inverter según el modelo. En Panamá, el condensador exterior se ensucia con facilidad.",
 },
 fallas={
  "neveras": [
   ("No enfría y hace ruido", "Ventilador del evaporador.", "Probamos el ventilador y el deshielo."),
   ("Escarcha en el fondo", "Resistencia de deshielo.", "Medimos la resistencia y el termostato."),
  ],
  "lavadoras": [
   ("No centrifuga", "Correa o interruptor de tapa.", "Revisamos correa e interruptor."),
   ("No desagua", "Bomba.", "Limpiamos y medimos la bomba."),
  ],
  "secadoras": [
   ("No seca bien o tarda mucho", "Filtro de pelusa saturado o ducto de salida tapado.", "Limpiamos el filtro y todo el recorrido del aire de salida."),
   ("Gira pero no calienta", "Resistencia o termostato.", "Medimos resistencia y termostatos por separado."),
   ("Se apaga sola a mitad del ciclo", "Termostato de seguridad por sobrecalentamiento.", "Revisamos el ducto y probamos el termostato de seguridad."),
   ("Hace ruido al girar", "Rodillos de apoyo o correa del tambor.", "Revisamos rodillos, polea tensora y correa."),
  ],
  "cocinas": [
   ("Los quemadores no encienden", "Bujías o módulo.", "Limpiamos bujías y revisamos el módulo."),
   ("El horno no calienta", "Termostato o válvula.", "Probamos el termostato y la válvula."),
  ],
  "aires": [
   ("No enfría", "Gas o filtro.", "Medimos presión y limpiamos."),
   ("Gotea agua", "Drenaje.", "Destapamos el drenaje."),
  ],
 },
 codigos={},
 mantenimiento=["Limpiar los filtros del aire cada mes.", "Limpiar las bujías de la estufa cada tres meses.", "Descongelar y limpiar el compartimento de la nevera cada seis meses.", "Revisar la manguera del gas cada año.", "Limpiar el filtro de pelusa de la secadora en cada uso y revisar el ducto de salida cada año."],
 etiqueta={"neveras": "Dentro del refrigerador, en el costado.", "lavadoras": "En la parte trasera.", "secadoras": "En el borde interior de la puerta o en la parte trasera."},
 modelo_ej="Los modelos Haceb combinan letras y números según la línea del equipo.",
 garantia="Haceb ofrece garantía de fábrica limitada, variable por producto. En equipos importados a Panamá, la cobertura local puede cambiar.",
 faq=[("¿Reparan equipos Haceb comprados en Colombia?", "Sí, y te explicamos con claridad si hay repuestos disponibles."), ("¿Reparan hornos Haceb a gas?", "Sí, con revisión segura de las conexiones."), ("¿Los aires Haceb son inverter?", "Depende del modelo; algunos son on/off y otros inverter.")],
)

M["kitchenaid"] = dict(
 nombre="KitchenAid", color="#9c1f2b", pais="Estados Unidos",
 origen="KitchenAid es mundialmente conocida por la batidora de pedestal. En Panamá también se encuentran sus refrigeradoras French Door y estufas.",
 lineas=["Artisan", "Classic", "Pro Line", "French Door", "Batidoras de cabeza inclinable", "Batidoras de tazón elevable"],
 equipos=["batidoras", "neveras"],
 tech={
  "batidoras": "La batidora KitchenAid tiene un motor universal y una caja de engranes con grasa. Con los años, la grasa se seca, y la batidora hace ruido o pierde fuerza. El cambio de grasa y de engranes de plástico o metal es la reparación más frecuente.",
  "neveras": "Las refrigeradoras KitchenAid French Door tienen compresores inverter, tarjetas de control y dispensador. Las revisamos como a cualquier equipo de alta gama: sensores, ventiladores y tarjeta.",
 },
 fallas={
  "batidoras": [
   ("Huele a quemado o suelta grasa por la cabeza", "Grasa vieja de la caja de engranes.", "Abrimos la caja, retiramos grasa vieja y colocamos grasa apta para alimentos."),
   ("Gira lento o se detiene con masa pesada", "Engrane desgastado, escobillas o control de velocidad.", "Revisamos el engrane, las escobillas y el control."),
   ("Hace ruido de rechinado", "Falta de lubricación o engrane dañado.", "Abrimos y revisamos."),
   ("El batidor toca el fondo del tazón", "Ajuste de altura.", "Ajustamos el tornillo de altura."),
  ],
  "neveras": [
   ("No enfría bien", "Ventilador o sensor.", "Probamos ventilador y sensores."),
   ("El dispensador no funciona", "Filtro o válvula.", "Revisamos el filtro y la válvula."),
  ],
 },
 codigos={},
 mantenimiento=["Cambiar la grasa de la batidora cada dos o tres años con uso frecuente.", "No pasar de la velocidad recomendada con masa pesada.", "Limpiar el filtro de agua de la refrigeradora cada seis meses."],
 etiqueta={"batidoras": "En la parte inferior de la base de la batidora.", "neveras": "Dentro del refrigerador, en el costado."},
 modelo_ej="Las batidoras KitchenAid tienen un número de modelo en la base, como KSM150 o KSM75.",
 garantia="KitchenAid ofrece garantía limitada de fábrica, que depende del producto y del país.",
 faq=[("¿Reparan batidoras KitchenAid?", "Sí. Cambiamos la grasa y los engranes, y revisamos motor y escobillas."), ("¿Por qué mi batidora KitchenAid suelta grasa?", "Normalmente es grasa vieja que se separó. Se limpia y se repone."), ("¿Atienden refrigeradoras KitchenAid?", "Sí, incluyendo los modelos French Door.")],
)

BRANDS_ORDER = ["samsung", "lg", "whirlpool", "mabe", "frigidaire", "electrolux", "general-electric", "haceb", "kitchenaid"]

ZONAS = {
 "ciudad-de-panama": ("Ciudad de Panamá", "Casco Antiguo, San Francisco, Bella Vista, El Cangrejo, Obarrio, Marbella, Paitilla, Punta Pacífica, Costa del Este, Albrook, Clayton, Betania, Pueblo Nuevo, Río Abajo", "Mezcla de edificios altos con aire central y casas antiguas con instalaciones eléctricas viejas. En el Casco Antiguo, la humedad y el salitre afectan a los equipos."),
 "san-miguelito": ("San Miguelito", "Belisario Frías, Mateo Iturralde, Amelia Denis de Icaza, Omar Torrijos, Victoriano Lorenzo", "Zona densa de viviendas y apartamentos; las visitas suelen coordinarse por franjas horarias por el tráfico."),
 "arraijan": ("Arraiján", "Vista Alegre, Burunga, Veracruz, Howard, Nuevo Arraiján", "Cuenta con muchos proyectos residenciales nuevos, y muchos equipos están en garantía de fábrica."),
 "la-chorrera": ("La Chorrera", "Barrio Balboa, Barrio Colón, El Coco, Playa Leona", "Mezcla de casas y urbanizaciones; las visitas incluyen equipos de lavandería y neveras de mayor tamaño."),
 "costa-del-este": ("Costa del Este", "Costa del Este, Santa María, Panamá Pacífico", "Apartamentos modernos con aires de alta eficiencia, centros de lavado y neveras de gran tamaño."),
 "tocumen-y-24-de-diciembre": ("Tocumen y 24 de Diciembre", "Tocumen, 24 de Diciembre, Pacora, Las Mañanitas", "Zona del este con crecimiento de viviendas; las neveras y lavadoras son los equipos más atendidos."),
 "panama-oeste": ("Panamá Oeste", "Panamá Pacífico, Howard, Veracruz, Vista Alegre, Arraiján", "Zona con mucho crecimiento reciente; muchos equipos todavía están en período de garantía."),
 "colon": ("Colón", "Colón ciudad, Cristóbal, Sabanitas, Margarita", "Clima costero con humedad y salitre; la corrosión es la causa más común de fallas en el condensador del aire acondicionado."),
}
