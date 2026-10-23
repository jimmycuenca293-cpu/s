# Guías de solución por falla. Texto neutro de marca y de país: el generador agrega marca, ciudad y moneda.
# Campos: resumen, causas [(causa, cómo reconocerla, qué hacer, quién)], pasos, nohacer, llamar, visita, tiempo, costo, prevencion, faq [(p, r)]
import re, unicodedata

def _n(t): return "".join(c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn")

T, X = "Tú", "Técnico"

G = {}

# ───────────────────────── NEVERAS ─────────────────────────
G["nev_nofria"] = dict(
 resumen="Cuando el congelador enfría y la parte de abajo no (o ninguna de las dos), casi siempre el aire frío no está circulando o el sistema de frío no está trabajando. Algunas causas se revisan en 15 minutos sin herramientas; otras necesitan técnico.",
 pasos=["Confirma que llega corriente: prueba el tomacorriente con otro aparato y revisa que el enchufe esté firme. Evita regletas compartidas con otros equipos grandes.",
        "Mira el panel: que no esté en modo demostración, vacaciones o apagado (por ejemplo «OF OF»), y que la temperatura sea aproximadamente 3 a 4 °C en la nevera y -18 °C en el congelador.",
        "Revisa la puerta: cierra bien, el empaque (goma) no está roto ni sucio y no hay recipientes que impidan cerrarla. Prueba con un papel: si sale sin resistencia, el empaque no sella.",
        "Despeja las rejillas de aire dentro de la nevera y del congelador. Si hay bolsas o recipientes tapando las salidas, el aire frío no llega.",
        "Observa el fondo del congelador: una capa de escarcha o hielo en la pared trasera indica que el sistema de descongelación falló y el hielo está bloqueando el aire.",
        "Si hay escarcha, desconecta el equipo, deja las puertas abiertas unas horas con toallas en el piso y vuelve a conectar. Si el problema vuelve en pocos días, la causa es una pieza y necesita técnico.",
        "Espera 24 horas después de cualquier ajuste antes de decidir: la nevera tarda en estabilizar su temperatura."],
 causas=[("Escarcha que bloquea el evaporador", "Hielo en la pared trasera del congelador; el congelador enfría pero la nevera no", "Descongelar y revisar; si vuelve, cambiar resistencia, termostato de deshielo o tarjeta", X),
         ("Ventilador del evaporador dañado", "No se escucha el ventilador al abrir la puerta del congelador; ruido de rozamiento o silencio total", "Cambio del motor del ventilador", X),
         ("Sensor de temperatura o tarjeta de control", "El equipo trabaja a ratos o la temperatura no corresponde a la configurada", "Diagnóstico y cambio del sensor o la tarjeta", X),
         ("Compresor o relé de arranque", "Se oye un «clic» y el compresor no arranca, o se calienta de más y se apaga", "Cambio del relé o diagnóstico del compresor", X),
         ("Empaque de la puerta o mal uso", "Goma floja, puerta que no cierra, rejillas tapadas, demasiada carga", "Limpiar, reacomodar o cambiar el empaque", T)],
 nohacer=["No piques el hielo con cuchillos ni objetos metálicos: puedes perforar el evaporador y la reparación se vuelve mucho más cara.", "No desconectes y conectes la nevera repetidamente: el compresor necesita al menos 5 minutos para volver a arrancar.", "No agregues gas refrigerante por tu cuenta ni pidas «recargar gas» sin que se encuentre antes la fuga.", "No bajes el termostato al mínimo esperando que enfríe más rápido."],
 llamar=["Pasaron 24 horas con las revisiones y sigue sin enfriar.", "El congelador tampoco congela, o los alimentos empiezan a descongelarse.", "Oyes un clic repetido, el compresor no arranca o está muy caliente.", "Hay olor a quemado, chispas o el breaker se dispara."],
 visita="El técnico mide temperaturas, revisa el ventilador del evaporador, el sistema de descongelación, los sensores y la tarjeta, y comprueba el compresor y su relé. Te explica la causa en el sitio y te da el costo antes de cambiar cualquier pieza.",
 tiempo="Diagnóstico de 30 a 60 minutos. Cambios como ventilador, sensor o resistencia suelen hacerse en la misma visita si la pieza está disponible.",
 costo="Depende de la pieza (un sensor no cuesta lo mismo que una tarjeta o un compresor), de si la pieza está disponible y de la mano de obra. El valor se te informa antes de empezar.",
 prevencion=["No tapes las rejillas internas ni sobrecargues la nevera.", "Limpia el empaque de la puerta cada mes con agua tibia.", "Deja unos 5 cm de espacio atrás y a los lados para que el equipo ventile."],
 faq=[("¿Por qué el congelador sí enfría y la nevera no?", "Lo más común es que el aire frío no pasa al compartimento de abajo: escarcha en el evaporador, ventilador que no gira o una compuerta de aire trabada."), ("¿Se pierde la comida si no enfría?", "Los alimentos refrigerados aguantan unas 4 horas sin frío si no abres la puerta; el congelador lleno, hasta 24 a 48 horas. Pasa lo importante a una hielera mientras llega el técnico."), ("¿Necesita recarga de gas?", "Solo si hay una fuga, y primero hay que repararla. Una nevera no «gasta» el gas como un carro gasta gasolina.")])

G["nev_escarcha"] = dict(
 resumen="La escarcha que se acumula en el congelador no es normal en una nevera moderna: indica que el sistema de descongelación automático falló o que entra aire húmedo por un empaque dañado.",
 pasos=["Revisa que la puerta del congelador cierre bien y que ningún empaque o paquete la deje entreabierta.", "Evita abrir la puerta por periodos largos y no guardes comida caliente sin dejarla enfriar.", "Desconecta la nevera, saca los alimentos a una hielera y deja descongelar con las puertas abiertas (varias horas), con toallas para el agua.", "Limpia y seca el interior, y revisa que el orificio de desagüe del fondo no esté tapado.", "Vuelve a conectar y observa durante una semana. Si la escarcha regresa, hay una pieza dañada."],
 causas=[("Resistencia de descongelación quemada", "Escarcha que crece en la pared trasera y poco a poco bloquea el aire", "Cambio de la resistencia", X), ("Termostato o fusible de deshielo", "La resistencia está bien pero no recibe corriente", "Cambio del termostato o fusible", X), ("Tarjeta o temporizador de descongelación", "El ciclo de deshielo nunca se activa", "Diagnóstico y cambio de la tarjeta", X), ("Empaque dañado o puerta mal cerrada", "Escarcha concentrada cerca de la puerta", "Limpiar o cambiar el empaque", T)],
 nohacer=["No raspes ni piques el hielo con objetos filosos.", "No uses secador de pelo cerca del plástico por mucho tiempo ni agua hirviendo dentro del congelador.", "No ignores la escarcha: termina bloqueando el aire y dañando el ventilador."],
 llamar=["La escarcha regresa en días o semanas después de descongelar.", "La nevera deja de enfriar mientras hay hielo en el fondo.", "Hay agua en el piso que no viene del desagüe."],
 visita="El técnico revisa la resistencia, el termostato de deshielo, el temporizador o la tarjeta y el desagüe, y cambia la pieza que falló.", tiempo="Entre 1 y 2 horas, según el modelo y la disponibilidad de la pieza.", costo="Depende de qué pieza del sistema de descongelación falló y de la mano de obra; se te confirma antes de empezar.",
 prevencion=["Cierra bien las puertas y no las dejes abiertas.", "Deja enfriar los alimentos antes de guardarlos.", "Revisa el empaque cada mes."],
 faq=[("¿Puedo seguir usando la nevera con escarcha?", "Por unos días sí, pero la escarcha crece y termina bloqueando el aire: la nevera deja de enfriar y puede dañarse el ventilador."), ("¿Descongelar la nevera la arregla?", "Solo temporalmente. Si la causa es una pieza del sistema de descongelación, la escarcha vuelve.")])

G["nev_gotea"] = dict(
 resumen="El agua dentro de la nevera casi siempre sale de un desagüe de descongelación tapado o congelado: el agua del deshielo no puede salir y se derrama hacia el compartimento.",
 pasos=["Revisa que la nevera esté nivelada y ligeramente inclinada hacia atrás (que las patas estén ajustadas).", "Busca el orificio de desagüe en el fondo de la pared trasera del compartimento y límpialo con un hisopo y agua tibia.", "Si hay hielo en el fondo del congelador, descongela el equipo como se explica en «Escarcha».", "Revisa la bandeja de goteo detrás o debajo de la nevera: que esté en su lugar y no rebose.", "Si tiene dispensador o fábrica de hielo, revisa las mangueras de agua por fugas o hielo.", "Seca el interior y observa 24 horas."],
 causas=[("Desagüe de deshielo tapado o congelado", "Charco de agua en el fondo, bajo los cajones", "Destapar con agua tibia; si se congela de nuevo, revisar descongelación", T), ("Bandeja de goteo mal puesta o llena", "Agua debajo del equipo", "Reubicar o vaciar la bandeja", T), ("Manguera de agua o válvula con fuga (modelos con dispensador)", "Agua que aparece cerca del dispensador o la fábrica de hielo", "Cambio de manguera o válvula", X), ("Empaque o puerta que no sella", "Condensación y gotas por humedad", "Limpiar o cambiar el empaque", T)],
 nohacer=["No uses alambres duros ni objetos punzantes para destapar el desagüe: puedes perforar la tubería.", "No dejes que el agua llegue a los enchufes ni a la parte eléctrica trasera.", "No inclines la nevera hacia adelante para «sacar el agua»."],
 llamar=["El desagüe vuelve a taparse o congelarse.", "El agua sale del dispensador o de las mangueras.", "Hay agua cerca de componentes eléctricos o la nevera huele a quemado."],
 visita="El técnico destapa y prueba el desagüe, revisa la resistencia de descongelación, las mangueras y las válvulas de agua, y verifica el nivel del equipo.", tiempo="Alrededor de 1 hora; con cambio de pieza, hasta 2 horas.", costo="Un desagüe tapado es una intervención sencilla; una válvula o resistencia cuesta más. Se te informa antes de empezar.",
 prevencion=["Limpia el orificio de desagüe cada 3 a 4 meses.", "Mantén la nevera nivelada.", "No guardes recipientes que toquen la pared trasera."],
 faq=[("¿Por qué gotea agua dentro de mi nevera?", "Porque el agua del deshielo no sale por el desagüe (tapado o congelado) y rebosa hacia adentro."), ("¿Es grave?", "Si es solo el desagüe, no. Si viene con escarcha o falta de frío, hay una pieza del sistema de descongelación fallando.")])

G["nev_ruido"] = dict(
 resumen="Es normal oír un zumbido suave del compresor y algún chasquido al enfriar. Un ruido nuevo, fuerte o constante merece revisión: suele ser el ventilador, el compresor o el equipo mal apoyado.",
 pasos=["Revisa que la nevera esté nivelada y apoyada sin balancearse; ajusta las patas.", "Aleja la nevera unos centímetros de la pared y de muebles que vibren.", "Identifica el ruido: zumbido o vibración (compresor), rozamiento o aleteo (ventilador), golpeteo (hielo o piezas sueltas), burbujeo (gas, normal).", "Abre el congelador y escucha: si el ruido cambia con la puerta abierta, es el ventilador del evaporador (a veces por hielo).", "Retira objetos que rocen las aspas o las paredes y revisa que no haya hielo atrás.", "Limpia la parte trasera o inferior (con el equipo desconectado) si hay polvo acumulado en el condensador."],
 causas=[("Ventilador del evaporador con hielo o desgastado", "Aleteo o chillido al abrir el congelador", "Descongelar y, si persiste, cambiar el motor", X), ("Ventilador del condensador sucio o duro", "Ruido atrás o abajo, cerca del compresor", "Limpiar o cambiar el motor", X), ("Compresor con desgaste", "Zumbido fuerte, vibración, calentamiento", "Diagnóstico del compresor", X), ("Equipo desnivelado o contacto con la pared", "Vibración que cambia al mover la nevera", "Nivelar y separar", T)],
 nohacer=["No ignores un ruido fuerte nuevo: puede ser el compresor y se agrava.", "No aprietes ni dobles las tuberías de la parte trasera.", "No metas la mano cerca de ventiladores con el equipo conectado."],
 llamar=["El ruido es fuerte, constante o empeora.", "Hay golpeteo metálico, chillido o el equipo vibra mucho.", "Además del ruido, falla el frío."],
 visita="El técnico ubica el origen del ruido (ventiladores, compresor, tuberías), limpia el condensador y cambia el ventilador o la pieza que corresponda.", tiempo="Entre 1 y 2 horas.", costo="Depende de si es un ventilador (menor) o el compresor (mayor). Se te explica antes de decidir.",
 prevencion=["Nivela el equipo al instalarlo.", "Limpia el condensador cada 6 meses.", "No dejes que se forme hielo en el congelador."],
 faq=[("¿Es normal que la nevera haga ruido?", "Un zumbido suave y algún chasquido sí. Un ruido nuevo, fuerte o que se repite sin parar no."), ("¿Por qué hace ruido al abrir el congelador?", "Casi siempre es el ventilador del evaporador con hielo o desgastado.")])

G["nev_dispensador"] = dict(
 resumen="Si el dispensador no saca agua, el problema suele ser el filtro vencido, una manguera congelada o la válvula de entrada de agua.",
 pasos=["Verifica que la llave de agua de la pared esté abierta y que la manguera no esté doblada ni aplastada detrás de la nevera.", "Revisa el filtro de agua: si pasaron más de 6 meses, cámbialo; un filtro tapado reduce o corta el caudal.", "Confirma que el dispensador no esté bloqueado por el seguro de panel (bloqueo infantil).", "Mira la temperatura del congelador: si está muy fría, la manguera interna puede congelarse.", "Después de cambiar el filtro, deja correr agua unos minutos para purgar el aire."],
 causas=[("Filtro de agua vencido", "Chorro débil o ausente; la luz del filtro encendida", "Cambiar el filtro", T), ("Manguera congelada", "No sale agua pero el filtro es nuevo", "Descongelar y revisar la temperatura", X), ("Válvula de entrada de agua", "Se oye un zumbido pero no pasa agua", "Cambio de la válvula", X), ("Presión de agua baja o llave cerrada", "Otros grifos también tienen poca presión", "Abrir llave / revisar suministro", T)],
 nohacer=["No fuerces la palanca del dispensador.", "No uses agua caliente ni objetos para descongelar la manguera interna.", "No dejes la nevera conectada si hay fugas de agua."],
 llamar=["Cambiaste el filtro y sigue sin salir agua.", "Hay fuga de agua en el piso.", "El dispensador hace ruido pero no entrega agua."],
 visita="El técnico revisa la presión y la manguera, prueba la válvula de entrada y el solenoide, y reemplaza lo que esté dañado.", tiempo="Alrededor de 1 hora.", costo="Depende de si es filtro, manguera o válvula. Se te confirma antes de empezar.",
 prevencion=["Cambia el filtro cada 6 meses.", "Instala una llave de paso accesible.", "Revisa la manguera al mover la nevera."],
 faq=[("¿Cada cuánto se cambia el filtro de agua?", "Normalmente cada 6 meses o cuando la luz del filtro se enciende; con agua muy dura, antes."), ("¿Sin filtro funciona?", "En muchos modelos se puede usar un tapón de derivación, pero el agua no queda filtrada.")])

G["nev_hielo"] = dict(
 resumen="Si la nevera no hace hielo o hace muy poco, lo más común es una fábrica de hielo congelada, poca agua por filtro o válvula, o una temperatura del congelador que no es la adecuada.",
 pasos=["Confirma que la fábrica de hielo esté encendida (palanca abajo o interruptor en ON).", "Revisa que el congelador esté entre -15 y -18 °C; si está más caliente, no congela bien el hielo.", "Cambia el filtro de agua si tiene más de 6 meses.", "Mira si hay un bloque de hielo pegado en la bandeja o en el conducto; si lo hay, descongela.", "Verifica la llave de agua y la manguera detrás de la nevera.", "Espera 24 horas: una fábrica nueva o reiniciada tarda en producir."],
 causas=[("Fábrica de hielo congelada o bloqueada", "Bloque de hielo, cubos pegados", "Descongelar y limpiar", T), ("Válvula de agua o manguera", "No entra agua a la fábrica", "Diagnóstico y cambio", X), ("Sensor o motor de la fábrica", "Brazo que no gira o no detecta", "Cambio del módulo", X), ("Congelador muy caliente", "Alimentos blandos, cubos pequeños", "Ajustar temperatura o revisar frío", T)],
 nohacer=["No uses objetos filosos para despegar el hielo de la bandeja.", "No añadas agua manualmente en la fábrica.", "No dejes la puerta abierta para «ayudar»."],
 llamar=["Pasaron 24 horas y no produce hielo.", "El agua se ve pero no baja a la bandeja.", "Hay fuga cerca de la fábrica de hielo."],
 visita="El técnico revisa la entrada de agua, la válvula, el sensor y el módulo de la fábrica de hielo y lo cambia si hace falta.", tiempo="Entre 1 y 2 horas.", costo="Depende de si es la válvula, el sensor o el módulo; se te informa antes de reparar.",
 prevencion=["Cambia el filtro a tiempo.", "Vacía y limpia la bandeja cada pocos meses.", "Mantén el congelador a -18 °C."],
 faq=[("¿Por qué mi nevera hace cubos pequeños?", "Normalmente por poca presión de agua, filtro tapado o congelador demasiado frío en la zona del molde."), ("¿Cuánto hielo debe producir?", "Depende del modelo; la mayoría llena una bandeja de cubos en unas pocas horas.")])

G["nev_filtro_alarma"] = dict(
 resumen="La luz del filtro de agua y la alarma de puerta o temperatura son avisos del equipo: no siempre indican una avería, pero conviene entender cuál es.",
 pasos=["Identifica el aviso: filtro de agua (cambio), filtro de aire, puerta abierta o temperatura alta.", "Si es alarma de puerta, revisa que cierre bien y que ningún recipiente la obstruya.", "Si es el filtro de agua, cámbialo y reinicia el aviso con el botón indicado en el manual (suele ser mantener presionado «Filter» unos segundos).", "Si es temperatura alta, mira si hubo apagón o puerta abierta; espera unas horas a que se estabilice.", "Si el aviso sigue, anota el código o ícono y toma una foto del panel."],
 causas=[("Filtro de agua o aire vencido", "Luz encendida del filtro", "Cambiar y reiniciar el aviso", T), ("Puerta mal cerrada", "Pitido continuo", "Cerrar bien o limpiar empaque", T), ("Temperatura alta por apagón", "Alarma de temperatura", "Esperar a que enfríe", T), ("Sensor o tarjeta", "El aviso no se quita aunque todo esté bien", "Diagnóstico", X)],
 nohacer=["No tapes la luz con cinta sin cambiar el filtro.", "No desconectes la nevera repetidamente para «quitar» la alarma.", "No ignores una alarma de temperatura con alimentos dentro."],
 llamar=["El aviso persiste tras cambiar el filtro y reiniciar.", "La alarma de temperatura sigue y los alimentos se calientan.", "El panel muestra un código de error."],
 visita="El técnico lee el código del panel, revisa sensores y tarjeta y confirma que el aviso corresponda a un filtro o a una avería real.", tiempo="30 a 60 minutos.", costo="Cambiar un filtro es sencillo; una tarjeta o sensor cuesta más. Se te informa antes.",
 prevencion=["Anota la fecha de cambio del filtro.", "Cierra bien las puertas.", "Usa filtros compatibles con tu modelo."],
 faq=[("¿Cómo reinicio la luz del filtro?", "Con el filtro nuevo instalado, mantén presionado el botón del filtro unos 3 a 5 segundos; el procedimiento exacto está en el manual de tu modelo."), ("¿Puedo usar un filtro genérico?", "Puedes, pero uno no compatible puede dar fugas o poco caudal. Conviene el original o uno certificado.")])

G["nev_breaker"] = dict(
 resumen="Si la nevera se apaga y prende sola, o salta el breaker, hay un problema eléctrico o de arranque. Es una falla que conviene atender pronto: puede dañar el compresor.",
 pasos=["Conecta la nevera directo a un tomacorriente con tierra, sin extensiones ni regletas.", "Revisa el cable y el enchufe: que no estén quemados, flojos ni calientes.", "Comprueba que el breaker de la línea no esté compartido con aire acondicionado, horno u otros equipos grandes.", "Escucha: si se oye un «clic» y el compresor no arranca, o si arranca y se apaga a los pocos minutos, anótalo.", "Si el breaker salta apenas la conectas, déjala desconectada y llama al técnico."],
 causas=[("Relé de arranque o protector térmico", "Clic repetido; el compresor no arranca o se apaga", "Cambio del relé o protector", X), ("Compresor con corto o desgaste", "El breaker salta al arrancar", "Diagnóstico del compresor", X), ("Tarjeta de control o sensor", "Se apaga y prende a intervalos irregulares", "Diagnóstico y cambio", X), ("Instalación eléctrica o voltaje inestable", "También fallan otros equipos", "Regulador de voltaje / revisión eléctrica", X)],
 nohacer=["No subas el amperaje del breaker.", "No uses extensiones delgadas.", "No sigas conectándola si salta el breaker o huele a quemado.", "No abras tapas eléctricas con el equipo conectado."],
 llamar=["El breaker salta una o más veces.", "Se apaga sola con frecuencia.", "Hay olor a quemado, chispas o cable caliente."],
 visita="El técnico mide corriente y voltaje, revisa el relé, el protector, el compresor y la tarjeta, y comprueba la instalación del tomacorriente.", tiempo="1 a 2 horas.", costo="Un relé es una reparación menor; un compresor o una tarjeta cuesta más. Se te informa antes de empezar.",
 prevencion=["Usa un regulador de voltaje.", "No compartas el circuito con equipos de alto consumo.", "Revisa el enchufe cada tanto."],
 faq=[("¿Por qué salta el breaker cuando conecto la nevera?", "Por un corto o sobrecarga: compresor, relé, cable dañado o un circuito compartido. Desconéctala y que la revise un técnico."), ("¿Es peligroso?", "Puede serlo si hay cable quemado o chispas. No la uses hasta revisarla.")])

G["nev_huele"] = dict(
 resumen="El mal olor dentro de la nevera viene casi siempre de comida derramada, un desagüe sucio o un filtro de olores saturado, no de una avería.",
 pasos=["Saca todos los alimentos y revisa vencimientos; retira lo dañado.", "Lava estantes y cajones con agua tibia y jabón neutro; seca bien.", "Limpia las paredes y el empaque con agua y bicarbonato (1 cucharada por litro).", "Destapa y limpia el orificio de desagüe del fondo.", "Cambia el filtro de olores o de aire si tu modelo lo tiene.", "Deja un recipiente con bicarbonato o carbón activado unas horas."],
 causas=[("Alimentos derramados o vencidos", "Olor localizado", "Limpieza profunda", T), ("Desagüe sucio", "Olor persistente y agua en el fondo", "Limpiar desagüe", T), ("Filtro de olores saturado", "Olor general", "Cambiar el filtro", T), ("Moho en el empaque", "Manchas negras en la goma", "Limpiar o cambiar el empaque", T)],
 nohacer=["No uses cloro ni productos fuertes dentro: dejan olor y dañan el plástico.", "No dejes la nevera desconectada y cerrada: se llena de moho.", "No uses ambientadores dentro."],
 llamar=["El olor persiste tras limpiar todo.", "Huele a quemado o a químico.", "Hay agua o moho que reaparecen."],
 visita="El técnico revisa desagüe, empaques y sistema de descongelación, y descarta que el olor venga de una fuga o un componente.", tiempo="Menos de 1 hora.", costo="Suele ser una revisión sencilla; se te informa antes de cualquier cambio.",
 prevencion=["Limpia la nevera cada mes.", "Guarda los alimentos tapados.", "Cambia el filtro de olores a tiempo."],
 faq=[("¿Cómo quito el olor a podrido de la nevera?", "Vacíala, límpiala con agua y bicarbonato, destapa el desagüe y deja bicarbonato o carbón activado adentro unas horas."), ("¿El olor a quemado es normal?", "No. Desconecta la nevera y llama a un técnico.")])

G["nev_pantalla"] = dict(
 resumen="Si la pantalla táctil de la nevera no enciende, se congela o no responde, normalmente se corrige con un reinicio o una actualización; si no, puede ser la pantalla o la tarjeta.",
 pasos=["Desconecta la nevera, espera 5 minutos y vuelve a conectar para reiniciar la pantalla.", "Revisa que la nevera tenga conexión Wi-Fi estable si usa funciones en línea.", "Busca actualizaciones de software en el menú de ajustes.", "Limpia la pantalla con un paño suave seco: la humedad o la grasa afectan el tacto.", "Revisa el cable y el enchufe, y que no se haya activado el modo ahorro o bloqueo de pantalla."],
 causas=[("Software bloqueado", "Pantalla congelada o lenta", "Reinicio y actualización", T), ("Conexión Wi-Fi inestable", "No abre apps ni widgets", "Revisar la red", T), ("Pantalla o tarjeta de control dañada", "Pantalla negra, líneas, táctil que no responde", "Cambio de la pantalla o tarjeta", X)],
 nohacer=["No uses productos de limpieza con alcohol fuerte o amoníaco sobre la pantalla.", "No presiones con objetos duros.", "No abras el panel con el equipo conectado."],
 llamar=["El reinicio no soluciona la pantalla.", "La pantalla está negra o con líneas.", "La nevera deja de enfriar además de fallar la pantalla."],
 visita="El técnico prueba la pantalla, el cableado y la tarjeta, actualiza el software y cambia lo que corresponda. La pantalla no afecta el enfriamiento, que se verifica aparte.", tiempo="1 a 2 horas.", costo="Una pantalla o tarjeta de este tipo es una pieza costosa; se te informa antes de cambiarla.",
 prevencion=["Mantén el software actualizado.", "Limpia la pantalla con paño suave.", "Evita salpicaduras de líquidos."],
 faq=[("¿La nevera enfría si la pantalla no funciona?", "Normalmente sí: la pantalla es independiente del sistema de frío, pero conviene confirmarlo con el técnico."), ("¿Se puede actualizar el software en casa?", "Muchos modelos lo hacen desde el menú si tienen Wi-Fi.")])

G["nev_instaview"] = dict(
 resumen="Si la ventana de la puerta no se ilumina, lo habitual es un ajuste, un sensor o la iluminación de la ventana; la nevera sigue enfriando.",
 pasos=["Golpea suavemente dos veces la ventana con los nudillos: debería encenderse la luz interior.", "Revisa en el panel que la función no esté desactivada o en modo ahorro.", "Comprueba que la puerta cierre bien: algunas luces se apagan si detectan la puerta abierta.", "Desconecta la nevera 5 minutos y reconecta.", "Si sigue apagada, anota el modelo y toma un video del problema."],
 causas=[("Función desactivada o modo ahorro", "El golpe no enciende la ventana", "Activar en el panel", T), ("Sensor o interruptor de puerta", "Se enciende a veces", "Diagnóstico y cambio", X), ("Iluminación LED o cable de la ventana", "Nunca se enciende", "Cambio del módulo", X)],
 nohacer=["No golpees fuerte el cristal.", "No limpies con químicos fuertes la ventana.", "No desarmes la puerta."],
 llamar=["La ventana no se enciende tras reiniciar.", "Hay humedad entre cristales.", "También hay problemas de frío."],
 visita="El técnico revisa el sensor, el cableado y el módulo LED de la ventana, y cambia lo que haga falta.", tiempo="1 hora aprox.", costo="Depende del módulo; se informa antes de cambiar.",
 prevencion=["Limpia con paño suave.", "No cargues peso en la puerta.", "Cierra la puerta con suavidad."],
 faq=[("¿La nevera enfría igual si la ventana no se ilumina?", "Sí. Es una función de comodidad e iluminación; el frío es independiente."), ("¿Se puede arreglar sin cambiar la puerta?", "Normalmente se cambia el módulo de luz, no la puerta completa.")])

G["nev_codigo_panel"] = dict(
 resumen="Un código de error en el panel de la nevera indica qué sistema falló (sensor, ventilador, descongelación, comunicación). Anotarlo y fotografiarlo acelera el diagnóstico.",
 pasos=["Toma una foto del código tal como aparece en el panel.", "Desconecta la nevera 5 minutos y reconecta: algunos códigos son temporales.", "Revisa que la puerta cierre y que no haya hielo bloqueando el ventilador.", "Mira si aparece de nuevo el mismo código; si desaparece, estuvo relacionado con una variación eléctrica.", "Envía el código, el modelo y la foto por WhatsApp para orientarte."],
 causas=[("Sensor de temperatura", "Códigos de sensor del congelador o la nevera", "Cambio del sensor", X), ("Ventilador o descongelación", "Código con falta de frío o escarcha", "Diagnóstico y pieza", X), ("Comunicación de tarjetas", "Código intermitente", "Revisión de cableado o tarjeta", X), ("Variación eléctrica puntual", "El código desaparece tras reiniciar", "Regulador de voltaje", T)],
 nohacer=["No ignores un código que reaparece.", "No abras paneles internos con el equipo conectado.", "No cambies piezas «a prueba y error»."],
 llamar=["El código reaparece tras reiniciar.", "Además del código, falla el frío.", "Hay olor a quemado."],
 visita="El técnico lee el código con el manual de servicio del modelo, prueba el componente indicado y lo repara o cambia.", tiempo="1 a 2 horas.", costo="Depende del componente al que apunte el código; se informa antes de empezar.",
 prevencion=["Usa regulador de voltaje.", "No dejes la puerta abierta.", "Revisa que el equipo esté nivelado."],
 faq=[("¿Dónde encuentro el significado del código?", "En el manual de tu modelo o con el técnico; los códigos cambian entre modelos."), ("¿Sirve reiniciar la nevera?", "A veces limpia un código temporal. Si regresa, hay que revisar el componente.")])

G["nev_compresor"] = dict(
 resumen="Un ruido de arranque o una vibración fuerte del compresor puede ser normal en un arranque, pero si es nuevo o constante conviene revisarlo: el compresor es la pieza más cara de la nevera.",
 pasos=["Revisa que la nevera esté nivelada y no toque la pared.", "Escucha si el ruido ocurre solo al arrancar y luego se normaliza, o si es continuo.", "Limpia el condensador (con el equipo desconectado) para evitar sobrecalentamiento.", "Usa regulador de voltaje si hay variaciones eléctricas.", "Anota cuánto dura el ruido y toma un video corto."],
 causas=[("Arranque normal del compresor", "Zumbido breve al encender", "Normal", T), ("Condensador sucio", "Compresor muy caliente, ruido constante", "Limpieza", T), ("Relé de arranque débil", "Clic y arranque difícil", "Cambio del relé", X), ("Desgaste interno del compresor", "Vibración fuerte, golpeteo", "Diagnóstico del compresor", X)],
 nohacer=["No ignores un golpeteo metálico.", "No sigas desconectando y reconectando.", "No muevas la nevera con el compresor funcionando."],
 llamar=["El ruido es fuerte o constante.", "El compresor se calienta o se apaga.", "La nevera enfría menos."],
 visita="El técnico mide corriente de arranque y presiones, revisa relé y protector, limpia el condensador y diagnostica el estado del compresor.", tiempo="1 a 2 horas.", costo="Un relé es menor; un compresor es la reparación más costosa. Te dicen cuál es antes de decidir.",
 prevencion=["Limpia el condensador cada 6 meses.", "Deja espacio de ventilación.", "Evita variaciones de voltaje."],
 faq=[("¿Cuánto dura un compresor?", "Bien cuidado puede durar 10 años o más."), ("¿Vale la pena cambiar el compresor?", "Depende de la edad de la nevera y del costo frente a una nueva; el técnico te lo dice con honestidad.")])

# ───────────────────────── LAVADORAS ─────────────────────────
G["lav_nocentrifuga"] = dict(
 resumen="Si la lavadora no centrifuga o centrifuga con ruido fuerte, normalmente la carga está desbalanceada, no desagua bien o hay un problema de amortiguadores, rodamientos o motor.",
 pasos=["Pausa el ciclo, abre y reacomoda la ropa: una carga muy grande o una sola prenda pesada (cobija, jeans) desbalancea el tambor.", "Revisa que la lavadora esté nivelada y que sus cuatro patas apoyen sin balancearse.", "Comprueba que desagüe: si queda agua en la tina, la centrifugación no arranca (ver «No desagua»).", "Limpia el filtro de la bomba (normalmente abajo al frente) y revisa que la manguera no esté doblada.", "Retira los tornillos de transporte si la lavadora es nueva.", "Prueba un ciclo de centrifugado solo, con carga pequeña y repartida."],
 causas=[("Carga desbalanceada o demasiado grande", "Se detiene o vibra y no sube de velocidad", "Reacomodar y reducir carga", T), ("Mal desagüe (filtro o manguera)", "Agua en la tina al terminar", "Limpiar filtro y manguera", T), ("Amortiguadores o rodamientos gastados", "Ruido fuerte, golpes, el tambor se mueve flojo", "Cambio de amortiguadores o rodamientos", X), ("Motor, carbones o tarjeta", "No gira o se detiene con error", "Diagnóstico y cambio", X)],
 nohacer=["No metas la mano mientras el tambor gira.", "No dejes que centrifugue una carga muy desbalanceada: daña los rodamientos.", "No fuerces la puerta para abrir en pleno centrifugado."],
 llamar=["Ruido metálico fuerte o golpes del tambor.", "No centrifuga aunque la carga esté bien repartida y desagüe.", "Muestra código de error que no se quita."],
 visita="El técnico revisa desagüe, amortiguadores, rodamientos, correa o motor, y la tarjeta; indica la pieza exacta y su costo antes de reparar.", tiempo="1 a 3 horas según la pieza.", costo="Un rodamiento o un motor cuestan bastante más que un filtro o una manguera; se te informa antes de empezar.",
 prevencion=["No sobrecargues la lavadora.", "Nivélala al instalarla.", "Lava prendas pesadas aparte."],
 faq=[("¿Por qué la lavadora no centrifuga y deja la ropa mojada?", "Casi siempre por carga desbalanceada o porque no desagua. Si no, puede ser motor o tarjeta."), ("¿Se puede seguir usando?", "Si hace ruido metálico fuerte, no: los rodamientos se dañan más.")])

G["lav_nodesagua"] = dict(
 resumen="Una lavadora que deja agua en la tina casi siempre tiene un filtro de la bomba tapado, una manguera doblada o una bomba de desagüe con falla. Muchas veces se resuelve en casa.",
 pasos=["Apaga y desconecta la lavadora.", "Revisa la manguera de desagüe: que no esté doblada, aplastada ni demasiado alta (máximo unos 1,0 a 1,2 m).", "Ubica el filtro de la bomba (abajo al frente, tras una tapa pequeña), pon toallas y un recipiente, ábrelo despacio y saca monedas, botones, pelusa.", "Limpia el filtro y vuelve a cerrarlo bien.", "Revisa el tubo de desagüe de la pared o el lavadero: que no esté obstruido.", "Haz un ciclo corto de desagüe para probar."],
 causas=[("Filtro de la bomba tapado", "Agua en la tina; ruido de la bomba atascada", "Limpiar el filtro", T), ("Manguera doblada o tapada", "El agua baja muy lento", "Enderezar o destapar", T), ("Bomba de desagüe dañada", "Zumbido sin sacar agua o silencio total", "Cambio de la bomba", X), ("Presostato o tarjeta", "No detecta nivel y no inicia el desagüe", "Diagnóstico y cambio", X)],
 nohacer=["No abras el filtro sin toallas y recipiente: sale mucha agua.", "No fuerces la puerta con la tina llena.", "No metas la mano en el tambor ni en la bomba con el equipo conectado."],
 llamar=["Limpiaste filtro y manguera y sigue sin desaguar.", "La bomba zumba pero no saca agua.", "Se muestra un código de error de desagüe que persiste."],
 visita="El técnico comprueba filtro, manguera, bomba, presostato y tarjeta, y cambia la pieza que falló.", tiempo="Entre 1 y 2 horas.", costo="Una bomba es una pieza económica a media; se te informa antes de cambiarla.",
 prevencion=["Limpia el filtro de la bomba cada mes.", "Revisa bolsillos antes de lavar.", "Usa bolsas para prendas pequeñas."],
 faq=[("¿Dónde está el filtro de la lavadora?", "En la mayoría de lavadoras de carga frontal, abajo al frente tras una tapa; en las de carga superior suele estar dentro del tambor o en la parte inferior."), ("¿Qué significa que no desagüe?", "Puede ser un filtro tapado, una manguera doblada o una bomba con falla.")])

G["lav_nollena"] = dict(
 resumen="Si la lavadora no llena de agua o llena muy lento, suele ser una llave cerrada, la malla de la manguera tapada o la válvula de entrada con falla.",
 pasos=["Verifica que las llaves de agua estén totalmente abiertas y que haya agua en otros grifos de la casa.", "Revisa que las mangueras de entrada no estén dobladas ni aplastadas.", "Cierra las llaves, desconecta cada manguera de la lavadora y limpia la pequeña malla (filtro) de la entrada.", "Vuelve a conectar bien las mangueras y abre las llaves.", "Haz un ciclo corto para comprobar.", "Revisa que la puerta o tapa cierren completamente: si no, la lavadora no llena."],
 causas=[("Llave cerrada o poca presión", "Llena muy lento; otros grifos también", "Abrir llave / revisar suministro", T), ("Malla de la manguera tapada", "Entra poco agua", "Limpiar la malla", T), ("Válvula de entrada", "Zumbido sin pasar agua, o no llena", "Cambio de la válvula", X), ("Sensor de nivel o seguro de puerta", "No llena o se detiene", "Diagnóstico y cambio", X)],
 nohacer=["No desconectes mangueras con las llaves abiertas.", "No uses alambre o herramientas filosas en la malla.", "No dejes la lavadora llenando sin vigilar si ya hubo fugas."],
 llamar=["Limpiaste mallas y sigue sin llenar.", "Se oye la válvula pero no entra agua.", "Muestra un código de error de entrada de agua que persiste."],
 visita="El técnico revisa presión, mallas, válvula de entrada, sensor de nivel y seguro de puerta.", tiempo="Alrededor de 1 hora.", costo="Una válvula es una pieza de costo medio; se te informa antes.",
 prevencion=["Limpia las mallas cada 6 meses.", "Cierra las llaves si te ausentas por días.", "Cambia las mangueras cada 5 años."],
 faq=[("¿Por qué mi lavadora tarda tanto en llenar?", "Poca presión de agua, malla tapada o válvula de entrada debilitada."), ("¿Debo cerrar las llaves?", "Es buena práctica si vas a estar fuera varios días.")])

G["lav_gotea"] = dict(
 resumen="El agua que sale de la lavadora puede venir de las mangueras, la puerta, el dispensador o la bomba. Identificar de dónde viene evita daños en el piso.",
 pasos=["Detén la lavadora y cierra las llaves de agua.", "Seca la zona y observa dónde reaparece el agua: conexión de manguera en la pared, en la lavadora, bajo la puerta o debajo del equipo.", "Aprieta a mano las conexiones de las mangueras y revisa las arandelas de goma.", "Revisa la goma de la puerta: busca grietas, objetos atrapados o suciedad.", "Revisa que el cajón del detergente no se desborde: usa menos jabón y de tipo HE si es de alta eficiencia.", "Mira la bomba y el filtro: que la tapa del filtro esté bien cerrada."],
 causas=[("Conexión de manguera floja o arandela gastada", "Gotea en la llave o en la entrada de la lavadora", "Apretar o cambiar la arandela/manguera", T), ("Goma de la puerta dañada o sucia", "Agua sale por la puerta", "Limpiar o cambiar la goma", X), ("Exceso de jabón o cajón obstruido", "Espuma y agua por el cajón", "Reducir jabón; limpiar el cajón", T), ("Bomba, tina o mangueras internas", "Agua debajo de la lavadora", "Cambio de pieza", X)],
 nohacer=["No uses la lavadora con fuga activa.", "No dejes agua cerca de enchufes.", "No uses silicona sobre la goma de la puerta."],
 llamar=["No encuentras el origen o la fuga continúa.", "Hay agua debajo de la lavadora.", "La goma está rota."],
 visita="El técnico localiza la fuga con prueba de agua, revisa mangueras, goma, bomba y tina, y repara o cambia lo que corresponda.", tiempo="1 a 2 horas.", costo="Una manguera o arandela es económica; una goma o una bomba cuestan más. Se informa antes.",
 prevencion=["Cambia mangueras cada 5 años.", "Usa jabón en la cantidad indicada.", "Limpia la goma de la puerta cada mes."],
 faq=[("¿De dónde puede gotear mi lavadora?", "Lo más común: conexiones de manguera, goma de la puerta, cajón de detergente o bomba."), ("¿Es peligroso?", "El agua cerca de la electricidad sí; cierra llaves y desconecta hasta revisarla.")])

G["lav_puerta"] = dict(
 resumen="Si la puerta no abre, normalmente hay agua dentro o el seguro sigue activo; si no cierra, puede estar mal puesta la ropa o dañado el seguro.",
 pasos=["Espera 2 a 3 minutos tras terminar el ciclo: el seguro tarda en liberarse.", "Revisa si queda agua en la tina; si sí, haz un ciclo de desagüe.", "Si sigue trabada, desconecta la lavadora 5 minutos y reconecta.", "Para cerrar, verifica que ninguna prenda quede atrapada en el borde.", "Revisa la goma y la cerradura buscando suciedad o piezas rotas."],
 causas=[("Seguro de puerta aún activo", "No abre justo tras el ciclo", "Esperar y reiniciar", T), ("Agua en la tina", "No libera la puerta", "Desagüe forzado", T), ("Cerradura dañada", "No traba o no libera", "Cambio de la cerradura", X), ("Manija o bisagra rotas", "No cierra bien", "Cambio de la pieza", X)],
 nohacer=["No fuerces la puerta con la tina llena.", "No abras el seguro con herramientas sin desconectar.", "No uses la lavadora con la puerta mal trabada."],
 llamar=["La puerta sigue trabada tras reiniciar y vaciar.", "No cierra aunque no haya obstáculo.", "Hay piezas rotas."],
 visita="El técnico revisa cerradura, interruptor de puerta, manija y bisagras.", tiempo="Alrededor de 1 hora.", costo="Depende de la cerradura o la manija; se informa antes.",
 prevencion=["No cierres la puerta de golpe.", "Revisa la goma al sacar la ropa.", "No fuerces el cierre."],
 faq=[("¿Cómo abro la lavadora si está trabada?", "Desconéctala, espera unos minutos, asegúrate de que no haya agua; muchas tienen una palanca de emergencia (consulta el manual)."), ("¿Por qué no cierra?", "Una prenda atrapada, la cerradura dañada o la goma deformada.")])

G["lav_vibra"] = dict(
 resumen="Vibración fuerte o códigos de desbalance (como UE) indican que el tambor gira descompensado: carga mal repartida, lavadora desnivelada o amortiguadores gastados.",
 pasos=["Pausa y reacomoda la ropa; no laves una sola prenda pesada.", "Revisa que no haya tornillos de transporte (en lavadoras nuevas).", "Nivela la lavadora con un nivel de burbuja ajustando las patas; apriétalas con la tuerca de seguridad.", "Apoya la lavadora sobre piso firme, no sobre madera floja.", "Reduce la carga a lo recomendado y mezcla prendas grandes con pequeñas.", "Haz una centrifugación de prueba."],
 causas=[("Carga desbalanceada", "El tambor se mueve en un lado; el código aparece", "Reacomodar", T), ("Lavadora desnivelada o con tornillos de transporte", "Se mueve y golpea", "Nivelar o retirar tornillos", T), ("Amortiguadores o resortes gastados", "Vibra aun con carga ligera", "Cambio de amortiguadores", X), ("Rodamientos", "Ruido grave metálico", "Cambio de rodamientos", X)],
 nohacer=["No ignores un código que reaparece.", "No sujetes la lavadora con la mano mientras centrifuga.", "No lavar cobijas pesadas en ciclos normales."],
 llamar=["Vibra mucho con carga bien repartida.", "Se oyen golpes del tambor.", "El código vuelve repetidamente."],
 visita="El técnico revisa nivelación, amortiguadores, resortes, rodamientos y sensor de balance.", tiempo="1 a 2 horas.", costo="Amortiguadores cuestan menos que rodamientos; se informa antes.",
 prevencion=["Nivela al instalar.", "No sobrecargues.", "Mezcla prendas."],
 faq=[("¿Qué significa el código UE?", "Desbalance de carga: la lavadora detecta que el tambor gira descompensado y se detiene."), ("¿Por qué vibra mi lavadora?", "Normalmente carga desbalanceada, equipo desnivelado o amortiguadores gastados.")])

G["lav_huele"] = dict(
 resumen="El olor a humedad o moho en la lavadora viene de residuos de jabón y humedad que se acumulan en la goma, el cajón y el tambor.",
 pasos=["Limpia la goma de la puerta con un paño y agua con vinagre o cloro diluido; presta atención a los pliegues.", "Saca y lava el cajón del detergente.", "Limpia el filtro de la bomba.", "Haz un ciclo de limpieza de tina en caliente (programa «Limpieza de tambor» o 60–90 °C vacía) con un limpiador específico o vinagre.", "Deja la puerta y el cajón abiertos al terminar para que seque.", "Usa menos jabón y suavizante."],
 causas=[("Moho en la goma de la puerta", "Manchas negras y olor", "Limpiar o cambiar la goma", T), ("Residuos de jabón en cajón y tambor", "Olor a humedad", "Limpieza de tina", T), ("Agua estancada en filtro o manguera", "Olor a drenaje", "Limpiar filtro y manguera", T)],
 nohacer=["No mezcles cloro con vinagre.", "No cierres la puerta con la lavadora húmeda.", "No uses exceso de suavizante."],
 llamar=["El olor persiste tras limpiar.", "Hay agua estancada o fugas.", "La goma está rota."],
 visita="El técnico revisa desagüe, mangueras y goma, y descarta agua estancada o piezas dañadas.", tiempo="Menos de 1 hora.", costo="Suele ser una limpieza o cambio de goma; se informa antes.",
 prevencion=["Deja la puerta abierta tras lavar.", "Limpia el tambor cada 1 a 2 meses.", "Usa la dosis correcta."],
 faq=[("¿Cómo quito el moho de la lavadora?", "Limpia la goma y el cajón, y haz un ciclo de limpieza en caliente con limpiador o vinagre."), ("¿Por qué huele a humedad?", "Por residuos de jabón y agua que se quedan sin ventilar.")])

G["lav_noenciende"] = dict(
 resumen="Si la lavadora no enciende o se apaga en medio del ciclo, revisa primero lo básico: corriente, puerta bien cerrada y que no se haya activado una protección.",
 pasos=["Confirma que llega corriente: prueba el tomacorriente con otro aparato y revisa el breaker.", "Cierra bien la puerta o tapa; si no traba, no arranca.", "Revisa que las llaves de agua estén abiertas y que no haya agua de más.", "Desconecta la lavadora 5 minutos y reconecta para reiniciar la tarjeta.", "Prueba sin carga y con un ciclo corto.", "Anota si muestra código o se apaga siempre en el mismo punto del ciclo."],
 causas=[("Corriente o enchufe", "No enciende ningún indicador", "Revisar tomacorriente/breaker", T), ("Seguro de puerta", "No inicia el ciclo", "Revisar puerta/cerradura", X), ("Tarjeta de control", "Se apaga en el mismo punto", "Diagnóstico y cambio", X), ("Sobrecalentamiento o protector", "Se apaga con carga pesada", "Esperar y reducir carga", T)],
 nohacer=["No abras paneles con la lavadora conectada.", "No uses extensiones delgadas.", "No ignores olor a quemado."],
 llamar=["No enciende tras revisar corriente.", "Se apaga siempre igual.", "Hay olor a quemado o chispas."],
 visita="El técnico mide voltaje, revisa puerta, filtros de ruido eléctrico y la tarjeta.", tiempo="1 a 2 horas.", costo="Una tarjeta es de las piezas más costosas; se informa antes.",
 prevencion=["Usa regulador de voltaje.", "No sobrecargues.", "No compartas circuito con equipos de alto consumo."],
 faq=[("¿Por qué se apaga a mitad del ciclo?", "Seguro de puerta, tarjeta, sobrecalentamiento o variación eléctrica."), ("¿Cuándo es la tarjeta?", "Cuando se descartan corriente, puerta y carga, y la falla se repite igual.")])

G["lav_pelusas"] = dict(
 resumen="La ropa que sale con pelusas o residuos suele deberse a filtros sucios, exceso de jabón o mezclar telas que sueltan pelusa.",
 pasos=["Limpia el filtro de pelusas (si tiene) y el filtro de la bomba.", "Usa menos detergente y asegúrate de que sea el adecuado.", "Separa prendas que sueltan pelusa (toallas, felpa) de las oscuras.", "Haz un ciclo de limpieza de tina.", "Aumenta el enjuague o agrega un ciclo extra."],
 causas=[("Filtro sucio", "Pelusa en la ropa oscura", "Limpiar filtro", T), ("Exceso de detergente", "Residuos blancos", "Reducir dosis; enjuague extra", T), ("Tambor sucio", "Manchas o residuos", "Limpieza de tina", T)],
 nohacer=["No uses más detergente del recomendado.", "No mezcles telas que sueltan pelusa.", "No olvides limpiar el filtro."],
 llamar=["Persisten residuos tras limpiar todo.", "La lavadora enjuaga mal.", "Hay agua que no se renueva."],
 visita="El técnico revisa filtros, enjuague, bomba y nivel de agua.", tiempo="Menos de 1 hora.", costo="Normalmente es una limpieza o ajuste; se informa antes.",
 prevencion=["Dosis correcta.", "Separa por colores y telas.", "Limpia filtros cada mes."],
 faq=[("¿Por qué mi ropa sale con residuos blancos?", "Casi siempre exceso de detergente o enjuague insuficiente."), ("¿Ayuda el vinagre?", "Un ciclo de limpieza con vinagre ayuda a quitar residuos del tambor.")])

G["lav_cod_motor"] = dict(
 resumen="Un código de error del motor indica que el motor no gira o está bloqueado: puede ser carga excesiva, una obstrucción o una falla del motor o de la tarjeta.",
 pasos=["Apaga y desconecta la lavadora.", "Retira parte de la ropa y reacomoda: una carga excesiva bloquea el tambor.", "Gira el tambor con la mano para comprobar que no esté trabado por una moneda o prenda.", "Reconecta y prueba un ciclo con carga pequeña.", "Anota el código exacto y envíalo con el modelo."],
 causas=[("Carga excesiva o tambor trabado", "El tambor no gira libre", "Reducir carga o desatascar", T), ("Motor o escobillas gastadas", "Zumbido sin giro", "Cambio del motor o escobillas", X), ("Tarjeta o sensor del motor", "El motor está bien pero no recibe señal", "Diagnóstico y cambio", X)],
 nohacer=["No fuerces el tambor con herramientas.", "No uses la lavadora con el código encendido.", "No abras paneles conectada."],
 llamar=["El código regresa con carga ligera.", "El tambor no gira libre.", "Hay olor a quemado."],
 visita="El técnico prueba el motor, las escobillas, la tarjeta y el sensor de giro.", tiempo="1 a 3 horas.", costo="Un motor es una de las piezas más costosas; se informa antes.",
 prevencion=["No sobrecargues.", "Revisa bolsillos.", "Nivela la lavadora."],
 faq=[("¿Qué hago si el tambor no gira?", "Desconecta, revisa si hay algo atascado y reduce la carga; si sigue, llama al técnico."), ("¿Se repara el motor?", "A veces se cambian escobillas; otras, el motor completo.")])

G["lav_app"] = dict(
 resumen="Si la lavadora no se conecta a la aplicación, casi siempre es la red Wi-Fi, el modo de emparejamiento o una actualización pendiente.",
 pasos=["Verifica que el teléfono y la lavadora estén en una red de 2,4 GHz (muchas no usan 5 GHz).", "Acerca el router a la lavadora o usa un repetidor.", "Reinicia la lavadora (desconectar 5 minutos) y el router.", "Activa el modo de emparejamiento Wi-Fi de la lavadora según su manual.", "Actualiza la aplicación y el firmware.", "Elimina el equipo de la app y vuelve a agregarlo."],
 causas=[("Red Wi-Fi 5 GHz o señal débil", "No encuentra la red", "Usar 2,4 GHz / acercar router", T), ("App o firmware desactualizados", "Conecta y se desconecta", "Actualizar", T), ("Módulo Wi-Fi de la lavadora", "Nunca se conecta", "Diagnóstico del módulo", X)],
 nohacer=["No uses redes con portal cautivo.", "No restablezcas de fábrica sin leer el manual.", "No ignores avisos de actualización."],
 llamar=["No conecta tras los pasos anteriores.", "El módulo no enciende.", "La app muestra error persistente."],
 visita="El técnico prueba el módulo Wi-Fi y la tarjeta, y actualiza el firmware.", tiempo="Alrededor de 1 hora.", costo="Depende de si es configuración o el módulo; se informa antes.",
 prevencion=["Mantén el router cerca.", "Actualiza la app.", "Usa red de 2,4 GHz."],
 faq=[("¿La lavadora funciona sin la app?", "Sí, la app es un complemento: la lavadora funciona con los botones."), ("¿Por qué no encuentra mi Wi-Fi?", "Muchas solo usan 2,4 GHz o la señal es débil.")])

# ───────────────────────── SECADORAS ─────────────────────────
G["sec_noseca"] = dict(
 resumen="Una secadora que no seca bien suele tener el filtro de pelusas o el ducto de salida tapados; si no, la resistencia o el sensor pueden estar fallando.",
 pasos=["Limpia el filtro de pelusas: debe quedar limpio en cada carga; lávalo si está tapado por residuos de suavizante.", "Revisa el ducto de salida: que no esté aplastado, doblado ni lleno de pelusa; el aire debe salir libremente hacia afuera.", "Revisa la salida exterior del ducto: la tapa debe abrir y no estar bloqueada.", "No sobrecargues: la ropa necesita espacio para girar.", "Usa el ciclo adecuado según la tela y evita mezclar prendas muy mojadas.", "Limpia el sensor de humedad (barras metálicas dentro del tambor) con un paño y alcohol."],
 causas=[("Filtro de pelusas tapado", "Tiempos de secado largos; ropa húmeda", "Limpiar el filtro", T), ("Ducto obstruido o muy largo", "Mucho calor y ropa húmeda; el aire sale poco", "Limpiar o acortar el ducto", T), ("Sensor de humedad sucio", "Se detiene antes de secar", "Limpiar el sensor", T), ("Resistencia, termostato o gas/ignitor", "Sale tibia o fría", "Diagnóstico y cambio", X)],
 nohacer=["No uses la secadora con el filtro sucio: es riesgo de incendio.", "No uses ductos de plástico flexible: acumulan pelusa y son más peligrosos que los metálicos.", "No sobrecargues el tambor."],
 llamar=["Limpiaste filtro y ducto y sigue húmeda.", "Sale fría o tibia.", "Huele a quemado."],
 visita="El técnico mide temperatura de salida, revisa ducto, resistencia o quemador, termostatos, fusible térmico y sensor.", tiempo="1 a 2 horas.", costo="Una resistencia o ignitor tiene costo medio; se informa antes de empezar.",
 prevencion=["Limpia el filtro en cada carga.", "Limpia el ducto cada 6 a 12 meses.", "Revisa la salida exterior."],
 faq=[("¿Por qué mi secadora no seca la ropa?", "Lo más común es el filtro o el ducto tapados; si no, falla la resistencia o el sensor."), ("¿Es peligroso un ducto tapado?", "Sí: el calor atrapado y la pelusa son riesgo de incendio. Límpialo.")])

G["sec_nocalienta"] = dict(
 resumen="Si la secadora gira pero no calienta, la causa es una pieza de calor: resistencia o fusible térmico en las eléctricas, o ignitor y válvulas en las de gas.",
 pasos=["Revisa el breaker: las secadoras eléctricas usan dos fases; si una cae, gira pero no calienta.", "Verifica el ciclo: que no esté en «sin calor» o «aire».", "Limpia el filtro y el ducto: un ducto tapado activa el fusible térmico.", "En las de gas, confirma que la llave de gas esté abierta.", "Haz un ciclo de 10 minutos y siente la temperatura de salida."],
 causas=[("Breaker de una fase caído", "Gira y no calienta", "Rearmar el breaker", T), ("Fusible térmico fundido", "Se funde por ducto obstruido", "Cambiar y destapar el ducto", X), ("Resistencia quemada (eléctrica)", "Sin calor", "Cambio de la resistencia", X), ("Ignitor o válvula de gas (a gas)", "No enciende la llama", "Cambio del ignitor o la válvula", X)],
 nohacer=["No manipules gas ni cables con el equipo conectado.", "No «puentees» el fusible térmico.", "No uses la secadora con olor a gas."],
 llamar=["Rearmaste el breaker y limpiaste el ducto, y sigue fría.", "Hay olor a gas: cierra la llave y ventila.", "Huele a quemado."],
 visita="El técnico mide continuidad de resistencia, fusible y termostatos, y en las de gas revisa ignitor y válvulas.", tiempo="1 a 2 horas.", costo="Depende de la pieza (fusible, resistencia, ignitor); se informa antes.",
 prevencion=["Limpia ducto y filtro.", "No sobrecargues.", "Revisa el breaker."],
 faq=[("¿Por qué gira y no calienta?", "Falla una pieza de calor o cayó una fase del breaker."), ("¿Puedo cambiar el fusible yo?", "Es mejor que lo haga un técnico, y destapar primero el ducto.")])

G["sec_tarda"] = dict(
 resumen="Un ciclo muy largo casi siempre significa que el aire no sale bien: ducto largo o sucio, filtro lleno o poca ventilación del cuarto.",
 pasos=["Limpia el filtro de pelusas.", "Revisa que el ducto sea lo más corto y recto posible, y limpio.", "Verifica la ventilación del cuarto: la secadora necesita aire de entrada.", "Evita cargas enormes y prendas muy mojadas (centrifuga bien antes).", "Limpia el sensor de humedad.", "Revisa que el aviso de ventilación del panel (si lo hay) no esté activo."],
 causas=[("Ducto largo, sucio o con curvas", "Ciclos de 2 a 3 horas", "Limpiar o acortar", T), ("Filtro tapado", "Tiempo de secado aumenta", "Limpiar", T), ("Poca ventilación del cuarto", "Cuarto caliente y húmedo", "Ventilar", T), ("Sensor o resistencia débiles", "Calienta poco", "Diagnóstico", X)],
 nohacer=["No uses ductos plásticos flexibles.", "No sobrecargues.", "No ignores el aviso de ventilación."],
 llamar=["Con ducto y filtro limpios sigue tardando.", "El aviso de ventilación no se quita.", "Calienta muy poco."],
 visita="El técnico mide el flujo de aire y la temperatura, revisa ducto, sensor y resistencia.", tiempo="1 a 2 horas.", costo="Una limpieza de ducto es sencilla; una pieza de calor cuesta más. Se informa antes.",
 prevencion=["Limpia el ducto cada 6 a 12 meses.", "Filtro en cada carga.", "Ducto corto y metálico."],
 faq=[("¿Cuánto debe durar un ciclo?", "Entre 40 y 70 minutos para una carga normal; mucho más indica problema de aire."), ("¿Ayuda dividir la carga?", "Sí, una carga más pequeña seca más rápido.")])

G["sec_ruido"] = dict(
 resumen="Golpes, chirridos o ruidos fuertes en la secadora suelen venir de objetos en el tambor, rodillos o correa desgastados.",
 pasos=["Revisa bolsillos y el tambor: monedas, botones y cremalleras golpean.", "Revisa que la secadora esté nivelada.", "Escucha si el ruido es rítmico (rodillos o cojinete) o continuo (motor).", "Retira el filtro y revisa que no haya piezas sueltas.", "Anota el ruido y toma un video."],
 causas=[("Objetos en el tambor", "Golpes intermitentes", "Retirar objetos", T), ("Rodillos del tambor gastados", "Chirrido rítmico", "Cambio de rodillos", X), ("Correa o polea tensora", "Chillido al arrancar", "Cambio de correa/polea", X), ("Cojinete o motor", "Ruido grave constante", "Diagnóstico", X)],
 nohacer=["No uses la secadora con ruido metálico fuerte.", "No pongas tenis duros sin bolsa.", "No fuerces el tambor."],
 llamar=["Chirridos o golpes continuos.", "Olor a quemado o goma.", "El tambor se detiene."],
 visita="El técnico revisa rodillos, correa, tensor, cojinete y motor.", tiempo="1 a 2 horas.", costo="Rodillos y correa son piezas de costo medio; se informa antes.",
 prevencion=["Revisa bolsillos.", "No sobrecargues.", "Nivela la secadora."],
 faq=[("¿Por qué chirría mi secadora?", "Lo más común son rodillos o la correa gastados."), ("¿Se puede seguir usando?", "Con chirrido fuerte conviene no usarla hasta revisarla.")])

G["sec_detiene"] = dict(
 resumen="Si la secadora se detiene a mitad del ciclo, suele ser protección térmica por ducto o filtro tapados, una puerta mal cerrada o un problema de la tarjeta.",
 pasos=["Limpia el filtro y revisa el ducto.", "Cierra bien la puerta y revisa el seguro.", "Deja enfriar la secadora 30 minutos y vuelve a probar: si la protección térmica la detuvo, arrancará.", "Reduce la carga.", "Anota en qué momento se detiene y si muestra algún código."],
 causas=[("Protección térmica por sobrecalentamiento", "Se detiene caliente y reinicia al enfriar", "Limpiar filtro y ducto", T), ("Interruptor de puerta", "Se detiene al moverla", "Cambio del interruptor", X), ("Tarjeta o sensor", "Se detiene sin patrón", "Diagnóstico", X), ("Breaker o corriente", "Se apaga junto con la luz", "Revisar el breaker", T)],
 nohacer=["No uses la secadora con el ducto tapado.", "No puentees el termostato.", "No abras la puerta durante un ciclo caliente."],
 llamar=["Se detiene siempre con ducto y filtro limpios.", "Huele a quemado.", "Muestra código que no se quita."],
 visita="El técnico revisa termostatos, interruptor de puerta, tarjeta y ducto.", tiempo="1 a 2 horas.", costo="Depende de la pieza; se informa antes.",
 prevencion=["Limpia filtro y ducto.", "No sobrecargues.", "Revisa el cierre de la puerta."],
 faq=[("¿Por qué se detiene a mitad del ciclo?", "Normalmente por sobrecalentamiento (ducto o filtro) o interruptor de puerta."), ("¿Es seguro reiniciarla?", "Sí, tras dejarla enfriar y limpiar filtro y ducto.")])

G["sec_noenciende"] = dict(
 resumen="Si la secadora no enciende, revisa primero la corriente y la puerta: es lo más común y se comprueba en minutos.",
 pasos=["Confirma que llega corriente: revisa el breaker (en las eléctricas son dos fases) y el enchufe.", "Cierra bien la puerta hasta oír el clic.", "Presiona «Inicio» sostenido unos segundos.", "Desconecta 5 minutos y reconecta.", "Revisa que no esté activo el bloqueo del panel."],
 causas=[("Breaker o enchufe", "No se enciende ninguna luz", "Rearmar el breaker / revisar enchufe", T), ("Interruptor de puerta", "El panel enciende pero no arranca", "Cambio del interruptor", X), ("Fusible térmico o tarjeta", "Sin respuesta", "Diagnóstico y cambio", X), ("Motor o botón de inicio", "Zumbido sin giro", "Diagnóstico", X)],
 nohacer=["No abras paneles conectada.", "No uses extensiones.", "No ignores olor a quemado."],
 llamar=["Sin corriente en el panel tras revisar el breaker.", "Zumbido sin giro.", "Olor a quemado."],
 visita="El técnico mide voltaje y continuidad, revisa puerta, fusible térmico, tarjeta y motor.", tiempo="1 a 2 horas.", costo="Depende de la pieza; se informa antes.",
 prevencion=["Usa su propio circuito.", "Revisa el enchufe.", "No cierres de golpe la puerta."],
 faq=[("¿Por qué no enciende mi secadora?", "Breaker, puerta, fusible térmico o tarjeta; empieza por el breaker y la puerta."), ("¿Necesita circuito propio?", "Las eléctricas sí: usan 220 V en la mayoría de países.")])

G["sec_olor"] = dict(
 resumen="El olor o la pelusa en la ropa seca vienen de filtro y ducto sucios o de residuos acumulados dentro del tambor.",
 pasos=["Limpia el filtro de pelusas y lávalo con agua y jabón.", "Limpia el tambor con un paño húmedo y vinagre.", "Revisa el ducto y la salida exterior.", "Evita sobrecargar y no dejes ropa húmeda dentro por horas.", "Haz un ciclo vacío corto para ventilar."],
 causas=[("Filtro con residuos", "Pelusa y olor", "Limpiar el filtro", T), ("Ducto sucio", "Olor a humedad o quemado", "Limpiar el ducto", T), ("Tambor con residuos", "Manchas y olor", "Limpiar el tambor", T)],
 nohacer=["No uses la secadora con olor a quemado.", "No dejes ropa húmeda dentro.", "No uses ambientadores dentro."],
 llamar=["Olor a quemado persistente.", "El olor sigue tras limpiar.", "Salen chispas."],
 visita="El técnico revisa ducto, filtro y calentamiento, y descarta recalentamiento.", tiempo="Menos de 1 hora.", costo="Normalmente limpieza; se informa antes de cualquier cambio.",
 prevencion=["Limpia el filtro cada carga.", "Limpia el ducto cada año.", "No sobrecargues."],
 faq=[("¿Por qué mi ropa huele a quemado?", "Ducto o filtro tapados o una resistencia sobrecalentada; deja de usarla hasta revisarla."), ("¿Cómo quito el olor a humedad?", "Limpia filtro y tambor y ventila el ducto.")])

G["sec_puerta"] = dict(
 resumen="Si la puerta de la secadora no cierra o se abre sola, normalmente es la bisagra, el pestillo o una prenda atrapada.",
 pasos=["Revisa que no haya una prenda atrapada en el borde.", "Limpia el pestillo y el marco de pelusa.", "Revisa que la bisagra no esté floja ni doblada.", "Prueba cerrar con suavidad hasta oír el clic.", "Anota si el panel marca «puerta abierta»."],
 causas=[("Prenda atrapada o suciedad", "No cierra completo", "Limpiar", T), ("Pestillo o bisagra dañados", "La puerta se abre sola", "Cambio del pestillo/bisagra", X), ("Interruptor de puerta", "El panel no detecta el cierre", "Cambio del interruptor", X)],
 nohacer=["No uses la secadora con la puerta mal cerrada.", "No fuerces la puerta.", "No pongas peso sobre la puerta abierta."],
 llamar=["La puerta no queda cerrada.", "Se abre sola.", "El panel dice «puerta abierta» con ella cerrada."],
 visita="El técnico revisa pestillo, bisagras e interruptor y cambia lo dañado.", tiempo="Menos de 1 hora.", costo="Piezas pequeñas de costo bajo a medio; se informa antes.",
 prevencion=["Cierra con suavidad.", "No te apoyes en la puerta.", "Limpia el marco."],
 faq=[("¿Por qué no cierra la puerta?", "Una prenda atrapada, suciedad en el pestillo o bisagra dañada."), ("¿Funciona con la puerta abierta?", "No debería: el interruptor la detiene por seguridad.")])

# ───────────────────────── mapeo ─────────────────────────
_NEV = [("family hub|pantalla", "nev_pantalla"), ("instaview|no se ilumina", "nev_instaview"), ("codigo de error en el panel", "nev_codigo_panel"), ("compresor", "nev_compresor"),
        ("no enfria", "nev_nofria"), ("escarcha", "nev_escarcha"), ("gotea", "nev_gotea"), ("ruido|zumbido", "nev_ruido"), ("dispensador", "nev_dispensador"), ("hielo", "nev_hielo"),
        ("luz del filtro|alarma", "nev_filtro_alarma"), ("prende sola|breaker", "nev_breaker"), ("huele", "nev_huele")]
_LAV = [("\\bapp\\b|smartthings|thinq|conecta", "lav_app"), ("addwash", "lav_gotea"), ("codigo (5e|se|oe)", "lav_nodesagua"), ("codigo (4e|ie)", "lav_nollena"), ("codigo le", "lav_cod_motor"),
        ("codigo ue|vibra|desbalancea", "lav_vibra"), ("no centrifuga", "lav_nocentrifuga"), ("no desagua", "lav_nodesagua"), ("no llena", "lav_nollena"), ("gotea|se sale", "lav_gotea"),
        ("puerta", "lav_puerta"), ("huele", "lav_huele"), ("no enciende|se apaga", "lav_noenciende"), ("pelusas|residuos", "lav_pelusas")]
_SEC = [("aviso de ventilacion|d80|ducto o filtro saturado", "sec_tarda"), ("sensor dry|no seca", "sec_noseca"), ("no calienta", "sec_nocalienta"), ("tarda", "sec_tarda"), ("ruido|golpea", "sec_ruido"),
        ("se detiene", "sec_detiene"), ("no enciende", "sec_noenciende"), ("olor|pelusa", "sec_olor"), ("puerta", "sec_puerta")]
_MAP = {"neveras": _NEV, "lavadoras": _LAV, "secadoras": _SEC}

def guia(titulo, k):
    t = _n(titulo)
    for rx, key in _MAP.get(k, []):
        if re.search(rx, t): return G[key]
    return None
