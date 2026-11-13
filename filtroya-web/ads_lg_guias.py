# Guías extra (problemas frecuentes y comparativas) para la tienda LG. Se ejecuta dentro de ads_lg_paginas.py.
def _h(t, *ps):
    return f"<h2>{esc(t)}</h2>" + "".join(f"<p>{x}</p>" for x in ps)


def _ul(items):
    return "<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>"


_P = {p["corto"]: p for p in PS}
_CTA = lambda p: f'<p><a href="{p["url"]}"><b>Ver el filtro {esc(p["corto"])} ({cop(p["precio"])})</b></a> · envío gratis a toda Colombia.</p>'
EXTRA = []


def _g(sl, titulo, desc, resumen, cuerpo, preg):
    EXTRA.append((sl, titulo, desc, resumen, cuerpo, preg))


_g("luz-del-filtro-de-la-nevera-lg-no-se-apaga",
   "Luz del filtro de la nevera LG naranja o roja que no se apaga: qué hacer",
   "Cambiaste el filtro y la luz de la nevera LG sigue encendida. Por qué pasa, cómo reiniciar el aviso y cuándo revisar que el filtro sea el correcto.",
   "La luz del filtro de una nevera LG es un temporizador, no un sensor: se apaga solo si reinicias el aviso después de instalar el filtro nuevo, normalmente manteniendo presionado el botón del filtro unos 3 a 5 segundos. Si sigue encendida, revisa que el filtro quede bien asentado y que sea la referencia de tu modelo.",
   _h("Por qué sigue encendida", "En la mayoría de los nevecones LG el indicador cuenta el tiempo de uso (alrededor de 6 meses) y no detecta si el filtro es nuevo. Por eso, aunque instales uno nuevo, la luz continúa hasta que tú la reinicias en el panel.")
   + _h("Cómo reiniciarla", "Con el filtro nuevo instalado, mantén presionado el botón «Filtro» (o «Water Filter» / «Reset») entre 3 y 5 segundos hasta que el indicador cambie o se apague. En algunos modelos hay que presionar el botón de agua y el de hielo a la vez; confirma en el manual de tu modelo.")
   + _h("Si no se apaga después de reiniciar") + _ul(["Saca el filtro y vuelve a instalarlo hasta sentir que queda firme y alineado.", "Confirma que la referencia corresponde a tu modelo: <a href=\"cual-es-mi-filtro.html\">busca tu modelo o código aquí</a>.",
                                                     "Desconecta el nevecón unos minutos y vuelve a conectarlo para reiniciar el panel.", "Purga unos 6 litros de agua para sacar el aire y repite el reinicio."])
   + _h("Y si el filtro es genérico", "Algunos filtros no originales no encajan al 100 % y el nevecón muestra errores. Si pasó justo después del cambio, compara el código impreso con el de tu equipo antes de culpar al panel.") + _CTA(PS[1]),
   [("¿La luz del filtro LG se apaga sola?", "No. Es un temporizador que debes reiniciar manualmente después del cambio."), ("¿Cuánto se mantiene presionado el botón?", "Normalmente de 3 a 5 segundos; algunos modelos usan una combinación de botones."), ("¿Puedo ignorar la luz?", "Puedes, pero el filtro vencido deja de retener bien y el agua y el hielo pueden cambiar de sabor.")])

_g("hielo-turbio-o-con-mal-sabor-nevera-lg-filtro",
   "Hielo turbio, con mal olor o sabor en la nevera LG: causas y solución",
   "Por qué el hielo o el agua de tu nevera LG salen turbios o con mal sabor, y cuándo la causa es el filtro de agua vencido.",
   "Si el agua o el hielo de tu nevera LG salen turbios, con olor o con sabor raro, lo más común es un filtro vencido (más de 6 meses) o aire atrapado después de un cambio. Cambia el filtro, purga unos 6 litros y desecha el hielo viejo del depósito.",
   _h("Causas más comunes", "Un filtro con más de 6 meses o con mucho consumo pierde capacidad de retener sedimentos, cloro y olores. También pasa tras un cambio si no se purga el aire: el agua sale lechosa por unos minutos.")
   + _h("Qué hacer paso a paso") + _ul(["Cambia el filtro por la referencia exacta de tu nevecón.", "Saca unos 6 litros de agua por el dispensador hasta que salga transparente.", "Vacía el depósito de hielo y deja que se forme hielo nuevo (puede tardar 24 horas).",
                                         "Limpia el depósito con agua tibia y jabón neutro si conserva olor."])
   + _h("Cuándo no es el filtro", "Si el problema continúa con filtro nuevo, revisa la calidad del agua de entrada, la manguera de conexión y que el hielo no esté absorbiendo olores de alimentos mal tapados del congelador.") + _CTA(PS[0]),
   [("¿Por qué el hielo sale blanco o turbio?", "Suele ser aire o sedimento; cambiar el filtro y purgar el sistema lo corrige en la mayoría de los casos."), ("¿Cuánto tarda en salir hielo limpio?", "Alrededor de 24 horas después de vaciar el depósito y purgar."), ("¿Cada cuánto cambio el filtro para evitarlo?", "Cada 6 meses de uso normal.")])

_g("dispensador-nevera-lg-sale-poca-agua-filtro",
   "El dispensador de la nevera LG saca poca agua: ¿es el filtro?",
   "Poco caudal en el dispensador de agua de la nevera LG: cuándo se debe a un filtro tapado o mal instalado y qué revisar primero.",
   "Poca presión en el dispensador de una nevera LG suele venir de un filtro saturado o mal asentado. Cámbialo por la referencia correcta, purga unos 6 litros y revisa que la manguera no esté doblada ni la llave de paso cerrada.",
   _h("Revisa en este orden") + _ul(["Llave de paso del agua abierta y manguera sin dobleces.", "Filtro instalado hasta el fondo y alineado.", "Filtro con más de 6 meses: cámbialo.", "Si instalaste uno nuevo, purga unos 6 litros: el aire reduce el caudal.", "Compara el código con el de tu modelo en la <a href=\"cual-es-mi-filtro.html\">tabla de equivalencias</a>."])
   + _h("Por qué un filtro vencido baja el caudal", "A medida que retiene partículas, el cartucho se va saturando y opone más resistencia al paso del agua. Por eso el cambio periódico mantiene un caudal normal.")
   + _h("Si persiste", "Con filtro nuevo bien instalado y poca agua, el problema puede estar en la válvula de entrada o en la presión de la red; ahí conviene llamar a un técnico.") + _CTA(PS[1]),
   [("¿El filtro puede reducir el agua del dispensador?", "Sí, cuando está saturado o mal asentado."), ("¿Cuánta agua debo purgar?", "Unos 6 litros después de cada cambio."), ("¿Cuándo llamar a un técnico?", "Si con filtro nuevo, bien instalado y llave abierta sigue saliendo poca agua.")])

_g("filtro-lg-original-vs-generico",
   "Filtro LG original vs genérico: cómo reconocer el correcto",
   "Cómo distinguir un filtro de agua para nevera LG correcto de uno que no encaja: código impreso, empaque, ajuste y qué pedir al vendedor.",
   "Para no equivocarte, compra por el código impreso de tu filtro viejo o por el modelo de tu nevecón, y pide que el vendedor te confirme la referencia antes de despachar. Un filtro que no corresponde puede no encajar, gotear o generar errores en el panel.",
   _h("Señales de que es el filtro correcto") + _ul(["La referencia (por ejemplo LT1000P, LT700P) está impresa en el cuerpo del filtro.", "Llega nuevo, sellado y con empaque claro.", "Encaja con un giro suave y queda firme, sin holgura.", "El vendedor te confirma que corresponde a tu modelo antes de enviarlo."])
   + _h("Riesgos de uno que no corresponde", "Un cartucho de otra referencia puede no asentar, dejar pasar agua sin filtrar o hacer que el panel marque error. Ahorrar unos pesos no compensa si hay que repetir la compra.")
   + _h("Cómo comprar con tranquilidad", f"Nosotros confirmamos el modelo antes de despachar y tienes 5 días hábiles de retracto con el filtro sin usar. Busca tu referencia en <a href=\"cual-es-mi-filtro.html\">cómo identificar mi filtro</a> o escríbela en el buscador.") + _CTA(PS[0]),
   [("¿Cómo sé si un filtro LG es el correcto?", "Por la referencia impresa y porque corresponde al modelo de tu nevecón."), ("¿Qué pasa si instalo uno que no es?", "Puede no encajar, gotear o dar error en el panel."), ("¿Pueden cambiarme el filtro si me equivoco?", "Sí, con el filtro sin usar dentro de los 5 días hábiles de retracto.")])

_g("se-puede-usar-la-nevera-lg-sin-filtro-de-agua",
   "¿Se puede usar la nevera LG sin filtro de agua?",
   "Qué pasa si usas tu nevera LG sin filtro o con el filtro vencido, y cómo hacerlo temporalmente con el tapón (bypass) si tu modelo lo trae.",
   "Muchos nevecones LG pueden funcionar un tiempo con un tapón de derivación (bypass) en lugar del filtro, pero el agua y el hielo no pasan por filtración. Lo recomendable es instalar un filtro nuevo; si no lo tienes, usa el tapón solo temporalmente.",
   _h("Con el tapón (bypass)", "Si tu modelo incluye tapón, puedes colocarlo en el alojamiento del filtro para que el dispensador funcione. El agua llega sin filtrar y el aviso del panel seguirá encendido.")
   + _h("Sin tapón ni filtro", "Dejar el alojamiento vacío puede cortar el flujo en algunos modelos. Confirma en el manual del tuyo.")
   + _h("Qué recomendamos", "Cambia el filtro cada 6 meses. Si ya venció y necesitas uno ya, puedes <a href=\"index.html#filtros\">pedirlo con envío gratis</a> y pagar en línea o contra entrega.") + _CTA(PS[1]),
   [("¿Es malo usar el nevecón sin filtro?", "El equipo funciona, pero el agua y el hielo no se filtran."), ("¿Qué es el tapón bypass?", "Una pieza que ocupa el lugar del filtro para dejar pasar el agua sin filtrar."), ("¿Cada cuánto se cambia el filtro?", "Cada 6 meses.")])

_g("filtro-de-nevera-lg-gotea-o-tiene-fuga",
   "El filtro de la nevera LG gotea o tiene fuga: causas y qué revisar",
   "Fuga o goteo alrededor del filtro de la nevera LG: instalación incompleta, o-ring, referencia equivocada y cuándo llamar a un técnico.",
   "Un goteo junto al filtro casi siempre se debe a que el cartucho no quedó bien asentado, a una referencia que no corresponde o a un sello dañado. Retíralo, revisa que no tenga el sello fuera de lugar, vuelve a instalarlo hasta que quede firme y purga el sistema.",
   _h("Revisa") + _ul(["Que el filtro quedó asentado y alineado, sin holgura.", "Que quitaste las tapas protectoras del filtro nuevo.", "Que el sello (o-ring) esté en su sitio y sin daños.", "Que la referencia sea la de tu modelo.", "Si el filtro es externo, que las mangueras estén bien conectadas y en el sentido del flujo."])
   + _h("Después de arreglarlo", "Purga unos 6 litros, seca la zona y vigila unas horas. Si la fuga sigue con un filtro correcto bien instalado, desconecta el agua y llama a un técnico.") + _CTA(PS[-1]),
   [("¿Por qué gotea el filtro nuevo?", "Casi siempre por instalación incompleta o referencia equivocada."), ("¿Debo cerrar el agua si hay fuga?", "Sí, cierra la llave de paso mientras revisas."), ("¿Puedo devolver un filtro que no encaja?", "Sí, si no está usado y dentro de los 5 días hábiles.")])

_g("filtro-interno-o-externo-nevera-lg",
   "¿Mi nevera LG usa filtro interno o externo? Cómo saberlo",
   "Cómo identificar si tu nevecón LG tiene filtro interno (dentro del refrigerador) o externo (en la manguera) y qué referencia corresponde.",
   f"La mayoría de nevecones LG usan filtro interno, dentro del refrigerador (LT1000P, LT700P, LT800P, LT500P, LT600P). Los equipos con filtro externo lo llevan en la manguera del agua, por fuera, y usan la referencia {PS[-1]['ref']}.",
   _h("Filtro interno", "Se ubica dentro del compartimento del refrigerador, normalmente arriba a la derecha o en la pared del fondo. Se retira con un giro y no requiere herramientas.")
   + _h("Filtro externo", f"Va conectado en la línea de agua por la parte trasera o lateral. El código {esc(PS[-1]['ref'])} equivale a {esc(', '.join(PS[-1]['refs'][1:]))}. Es el que se cambia aflojando las conexiones de la manguera.")
   + _h("Cómo confirmarlo", "Mira el filtro viejo: el código impreso te lo dice. También puedes escribir el modelo de tu nevera (etiqueta interior) en el buscador de la tienda.") + _CTA(PS[-1]),
   [("¿Dónde está el filtro de mi nevera LG?", "Dentro del refrigerador si es interno; en la manguera del agua si es externo."), (f"¿Qué filtro externo vende?", f"El {PS[-1]['nombre']} ({PS[-1]['ref']})."), ("¿Cómo sé cuál es el mío?", "Por el código impreso en el filtro viejo o por el modelo de tu nevecón.")])

_g("cuanto-dura-el-filtro-de-agua-lg",
   "¿Cuánto dura el filtro de agua LG y de qué depende?",
   "Duración del filtro de agua de la nevera LG: 6 meses de uso normal, y qué factores (consumo, calidad del agua) lo acortan.",
   "El filtro de agua de una nevera LG dura alrededor de 6 meses de uso normal. Se acorta si en tu casa se consume mucha agua o hielo, o si el agua de entrada trae muchos sedimentos; conviene cambiarlo antes si notas sabor raro o poco caudal.",
   _h("Qué lo acorta") + _ul(["Familias numerosas o mucho consumo de hielo.", "Agua con muchos sedimentos o cloro.", "Equipos que pasan temporadas sin uso (el filtro igual envejece)."])
   + _h("Señales de que toca cambiarlo", "Luz del filtro encendida, agua con sabor u olor, hielo turbio o caudal reducido.") + _h("Cómo planear el cambio", "Anota la fecha de instalación y programa un recordatorio a los 6 meses. Así lo tienes en casa antes de que venza.") + _CTA(PS[0]),
   [("¿Cuánto dura un filtro LG?", "Unos 6 meses de uso normal."), ("¿Se puede estirar más?", "No es recomendable: pierde capacidad y puede dar mal sabor."), ("¿Cómo sé que ya venció?", "La luz del panel, el sabor del agua o la baja presión.")])

_g("filtro-lg-nuevo-no-encaja",
   "El filtro LG nuevo no encaja en mi nevera: por qué y cómo solucionarlo",
   "Si el filtro de agua nuevo no gira ni queda firme en tu nevecón LG, probablemente es otra referencia o está mal alineado.",
   "Si el filtro nuevo no encaja en tu nevera LG, lo más probable es que la referencia no corresponda al modelo o que no esté alineado con las guías del alojamiento. Verifica el código impreso y compara con la tabla de modelos antes de forzarlo.",
   _h("No lo fuerces", "Un filtro correcto entra con un giro suave. Forzarlo puede dañar el alojamiento o el sello.")
   + _h("Revisa") + _ul(["Código del filtro viejo vs. el nuevo.", "Que retiraste las tapas protectoras.", "Que el alojamiento esté limpio y sin restos del sello anterior.", "Que corresponda a tu modelo: <a href=\"cual-es-mi-filtro.html\">tabla de modelos y códigos</a>."])
   + _h("Si pediste la referencia equivocada", "Tienes 5 días hábiles de retracto con el filtro sin usar para cambiarlo por el correcto.") + _CTA(PS[1]),
   [("¿Por qué no entra el filtro?", "Referencia equivocada o desalineado."), ("¿Puedo cambiarlo si me equivoqué?", "Sí, sin usar y dentro de 5 días hábiles."), ("¿Cómo confirmo la referencia?", "Con el código impreso del filtro viejo o el modelo de tu nevecón.")])

_g("checklist-comprar-filtro-lg-en-colombia",
   "Checklist para comprar un filtro de nevera LG en Colombia sin equivocarte",
   "Lista de 8 puntos antes de comprar el filtro de agua de tu nevera LG: referencia, precio, envío, pago, retracto y soporte.",
   "Antes de comprar, confirma la referencia de tu modelo, que el producto sea nuevo y sellado, el precio final con envío, las formas de pago seguras y la política de retracto. Con eso evitas el error más común: pedir un filtro que no encaja.",
   _h("Los 8 puntos") + "<ol>" + "".join(f"<li>{x}</li>" for x in ["Identifica tu referencia por el filtro viejo o por el modelo del nevecón.", "Compara el precio final: aquí el envío es gratis a toda Colombia.", "Confirma que el filtro sea nuevo y venga sellado.", "Revisa las formas de pago: Wompi (tarjeta, PSE, Nequi, Bancolombia) o contra entrega.",
                                                                                        "Pide confirmación de que corresponde a tu modelo.", "Verifica la política de retracto (5 días hábiles, sin usar).", "Guarda el correo de confirmación del pedido.", "Programa el próximo cambio a los 6 meses."]) + "</ol>"
   + _h("Por qué importa", "Los filtros se parecen mucho entre sí; la diferencia está en el código. La tabla de <a href=\"cual-es-mi-filtro.html\">modelos y códigos</a> te ayuda a acertar.") + _CTA(PS[0]),
   [("¿Qué debo verificar antes de comprar?", "La referencia, el precio final, el estado del producto, el pago y el retracto."), ("¿Dónde veo mi referencia?", "Impresa en el filtro viejo o en la tabla de modelos de la tienda."), ("¿Es seguro pagar en línea?", "Sí, con Wompi (Bancolombia); también puedes pagar contra entrega.")])


def _cmp(a, b, extra):
    A, B = _P[a], _P[b]
    mod = lambda p: ", ".join(p["modelos"]) or "confirma con el código del filtro viejo"
    tabla = ('<div class="tbl-wrap"><table class="spec-table"><tr><th></th><th>' + esc(A["corto"]) + "</th><th>" + esc(B["corto"]) + "</th></tr>"
             f"<tr><td><b>Código</b></td><td>{esc(A['ref'])}</td><td>{esc(B['ref'])}</td></tr>"
             f"<tr><td><b>Equivale a</b></td><td>{esc(', '.join(A['refs'][1:4]))}</td><td>{esc(', '.join(B['refs'][1:4]))}</td></tr>"
             f"<tr><td><b>Nevecones</b></td><td>{esc(mod(A))}</td><td>{esc(mod(B))}</td></tr>"
             f"<tr><td><b>Tipo</b></td><td>{'Externo' if A['ubic'] == 'externo' else 'Interno'}</td><td>{'Externo' if B['ubic'] == 'externo' else 'Interno'}</td></tr>"
             f"<tr><td><b>Precio</b></td><td>{cop(A['precio'])}</td><td>{cop(B['precio'])}</td></tr><tr><td><b>Cambio</b></td><td>6 meses</td><td>6 meses</td></tr></table></div>")
    _g(f"comparativa-filtro-lg-{slug(A['corto'])}-vs-{slug(B['corto'])}", f"Filtro LG {A['corto']} vs {B['corto']}: diferencias y cuál elegir",
       f"Comparativa del filtro de agua LG {A['corto']} y {B['corto']}: códigos equivalentes, nevecones compatibles, precio y cuál elegir.",
       f"El {A['corto']} y el {B['corto']} no son intercambiables: cada uno corresponde a modelos distintos de nevecón LG. {A['corto']} cuesta {cop2(A['precio'])} y {B['corto']} {cop2(B['precio'])}; el correcto es el de tu modelo, no el más barato.",
       _h("Resumen", f"{extra} La forma segura de elegir es por el modelo de tu nevecón o por el código impreso en tu filtro viejo.") + tabla
       + _h(f"¿Cuándo elegir el {A['corto']}?", f"Si tu nevecón es {esc(mod(A))} o tu filtro viejo dice {esc(A['corto'])} o alguno de sus equivalentes ({esc(', '.join(A['refs'][1:4]))}).")
       + _h(f"¿Cuándo elegir el {B['corto']}?", f"Si tu nevecón es {esc(mod(B))} o tu filtro viejo dice {esc(B['corto'])} o {esc(', '.join(B['refs'][1:4]))}.") + _CTA(A) + _CTA(B),
       [(f"¿El {A['corto']} sirve en lugar del {B['corto']}?", "No. Son referencias distintas para modelos distintos; usa la de tu nevecón."), (f"¿Cuál es más barato?", f"El {min((A, B), key=lambda x: x['precio'])['ref']}, por {cop2(min(A['precio'], B['precio']))}."), ("¿Cómo sé cuál necesito?", "Por el código impreso en el filtro viejo o por el modelo del nevecón.")])


_cmp("LT1000P", "LT700P", "Ambos son filtros internos de reemplazo cada 6 meses, pero se instalan en familias distintas de nevecón.")
_cmp("LT700P", "LT800P", "Tienen el mismo precio y se parecen, pero sus códigos de equivalencia y modelos son diferentes.")
_cmp("LT700P", "LT500P", "Dos referencias internas muy buscadas; cambia la serie de nevecón que usa cada una.")
_cmp("LT500P", "LT600P", "El LT600P es un filtro interno más largo; confirma con foto de tu filtro viejo si dudas entre los dos.")
_cmp("LT1000P", PS[-1]["corto"], "El LT1000P va dentro del refrigerador; el ADQ73693903 es externo y se conecta a la manguera del agua.")
ARTS += EXTRA
