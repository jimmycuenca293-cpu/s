# -*- coding: utf-8 -*-
"""Consejo propio de cada falla: (qué puede probar el usuario, cuándo llamar).
Códigos de «llamar»: ya = riesgo, no usar; tec = falla de componente, requiere técnico; vuelve = probar primero, si regresa llamar."""
LLAMAR = {
    "ya": "Sí, ya: no uses el equipo hasta que lo revise un técnico.",
    "tec": "Sí: es una falla de componente y requiere técnico.",
    "vuelve": "Primero prueba lo indicado; si la falla vuelve, llama.",
}
USAR = {
    "ya": "No. Apaga el equipo, desconéctalo y no lo uses hasta que lo revise un técnico.",
    "tec": "Mejor no insistir: apaga el equipo y llama al técnico; seguir usándolo puede dañar más piezas.",
    "vuelve": "Sí, mientras pruebas lo indicado. Si la falla vuelve, deja de usar el equipo y llama.",
}
C = {}
def a(k, probar, cod): C[k] = (probar, cod)

# ---------------- SAMSUNG
a("samsung|neveras|0", "Desconecta la refrigeradora 24 horas para que se descongele el hielo del fondo del congelador y vuelve a enchufarla. Revisa también que ningún alimento tape las rejillas de aire del refrigerador.", "vuelve")
a("samsung|neveras|1", "Aleja la refrigeradora unos 5 cm de la pared y revisa que nada roce la parte trasera. Si el ruido viene del congelador, suele ser hielo en el ventilador.", "vuelve")
a("samsung|neveras|2", "Anota el código exacto que aparece, desconecta la refrigeradora 5 minutos y vuelve a conectarla.", "vuelve")
a("samsung|neveras|3", "Cambia el filtro de agua si pasaron seis meses, abre bien la llave de agua y revisa que la manguera de la parte trasera no esté doblada.", "vuelve")
a("samsung|neveras|4", "Desconéctala 5 minutos y vuelve a conectarla. Si empezó después de una tormenta o un apagón, no la reinicies varias veces seguidas.", "tec")
a("samsung|lavadoras|0", "Detén el ciclo, reacomoda la ropa para que no quede toda de un lado y revisa que la lavadora esté nivelada y firme en el piso.", "vuelve")
a("samsung|lavadoras|1", "Con la lavadora apagada y desconectada, limpia el filtro de la bomba (abajo, al frente) y revisa que la manguera de desagüe no esté doblada.", "vuelve")
a("samsung|lavadoras|2", "Cierra la llave de agua, revisa que las mangueras estén bien ajustadas y mira si hay agua en la base. Apaga y desconecta antes de tocar nada.", "vuelve")
a("samsung|lavadoras|3", "Espera un par de minutos después de terminar el ciclo, porque la puerta queda bloqueada, y revisa que no haya ropa atrapada en el cierre.", "vuelve")
a("samsung|lavadoras|4", "Apaga, reduce la carga y reacomoda la ropa. Prueba un ciclo solo de centrifugado.", "tec")
a("samsung|secadoras|0", "Limpia el filtro de pelusa y el depósito o condensador, y no sobrecargues el tambor.", "vuelve")
a("samsung|secadoras|1", "Apágala y límpiale el filtro. Revisa que el ducto de salida no esté aplastado antes de volver a usarla.", "vuelve")
a("samsung|secadoras|2", "Abre la puerta y revisa que no haya monedas, botones u objetos dentro; confirma que el equipo esté nivelado.", "vuelve")
a("samsung|secadoras|3", "Vacía el depósito de agua de condensado y revisa que la manguera no esté doblada.", "vuelve")
a("samsung|aires|0", "Lava los filtros, confirma que el control esté en modo frío y mantén las ventanas cerradas.", "vuelve")
a("samsung|aires|1", "Apaga el aire y seca el piso. Revisa que el desagüe no esté tapado ni la manguera doblada.", "vuelve")
a("samsung|aires|2", "Anota el código, apaga el aire y desconéctalo unos minutos antes de encenderlo de nuevo.", "vuelve")
a("samsung|aires|3", "Desconecta el aire durante tormentas fuertes y espera unos minutos tras un apagón antes de encenderlo.", "tec")
a("samsung|cocinas|0", "Confirma que el horno esté bien cerrado y que elegiste la función correcta. Evita abrirlo seguido mientras se calienta.", "vuelve")
a("samsung|cocinas|1", "Seca la cocina y limpia con un cepillo suave los quemadores y las bujías. Si hueles gas, cierra la llave y ventila.", "vuelve")
a("samsung|cocinas|2", "Usa ollas de base plana y de material magnético, y revisa que la zona esté limpia y ventilada.", "vuelve")
a("samsung|lavavajillas|0", "Limpia el filtro del fondo y revisa que la manguera de desagüe no esté doblada.", "vuelve")
a("samsung|lavavajillas|1", "Limpia los brazos rociadores y el filtro. Usa sal y abrillantador si tu modelo los lleva.", "vuelve")
a("samsung|microondas|0", "No lo uses vacío. Prueba con un vaso de agua un minuto: si el plato gira pero el agua no se calienta, hay una pieza dañada.", "tec")
a("samsung|microondas|1", "Apágalo, retira metales o envolturas y limpia el interior. Si hace chispas con el microondas vacío, no lo uses.", "ya")

# ---------------- LG
a("lg|neveras|0", "Confirma que esté enchufada y que el control no esté apagado. Si no hace ni ruido, probablemente falla la placa o el compresor.", "tec")
a("lg|neveras|1", "Aleja la refrigeradora de la pared y revisa que nada roce atrás. Un zumbido leve que sube y baja con el compresor inverter es normal; uno fuerte, no.", "vuelve")
a("lg|neveras|2", "Anota el código, desconecta la refrigeradora 5 minutos y vuelve a conectarla.", "vuelve")
a("lg|neveras|3", "El hielo puede estar tapando el desagüe del evaporador: desconecta la refrigeradora 24 horas para descongelarla.", "vuelve")
a("lg|neveras|4", "Cambia el filtro de agua si pasaron seis meses, abre la llave de agua y revisa que la manguera no esté doblada.", "vuelve")
a("lg|lavadoras|0", "Limpia el filtro de la bomba (abajo, al frente) con la lavadora apagada y desconectada, y revisa que la manguera de desagüe no esté doblada.", "vuelve")
a("lg|lavadoras|1", "Abre la llave de agua, revisa que las mangueras no estén dobladas y limpia las mallas de entrada.", "vuelve")
a("lg|lavadoras|2", "Reacomoda la carga: no mezcles prendas muy pesadas con livianas ni laves una sola prenda grande.", "vuelve")
a("lg|lavadoras|3", "Cierra bien la puerta y revisa que no haya ropa atrapada en el empaque.", "vuelve")
a("lg|lavadoras|4", "Apaga y desconecta 5 minutos, prueba un ciclo vacío y revisa que no haya exceso de espuma.", "tec")
a("lg|lavadoras|5", "Nivela la lavadora, reacomoda la carga y revisa que no haya objetos dentro del tambor.", "vuelve")
a("lg|secadoras|0", "Limpia el filtro, el condensador y el ducto, y no sobrecargues el tambor.", "vuelve")
a("lg|secadoras|1", "Revisa el enchufe y el breaker, y que la puerta esté bien cerrada.", "vuelve")
a("lg|secadoras|2", "Vacía el depósito de condensado y limpia el filtro.", "vuelve")
a("lg|centro-lavado|0", "Apaga el equipo desde el breaker 5 minutos, enciéndelo y prueba cada unidad por separado.", "tec")
a("lg|centro-lavado|1", "Desconéctalo 5 minutos. Si el panel sigue sin responder, no insistas con los botones.", "tec")
a("lg|aires|0", "Anota el código, apaga y desconecta el aire unos minutos antes de encenderlo otra vez.", "vuelve")
a("lg|aires|1", "Lava los filtros, deja libre el frente de la unidad y mantén las ventanas cerradas.", "vuelve")
a("lg|aires|2", "Apaga el aire y revisa que el desagüe no esté tapado ni doblado.", "vuelve")
a("lg|lavavajillas|0", "Limpia el filtro del fondo y revisa la manguera de desagüe.", "vuelve")
a("lg|lavavajillas|1", "Limpia los brazos rociadores y el filtro, y no sobrecargues los racks.", "vuelve")

# ---------------- WHIRLPOOL
a("whirlpool|neveras|0", "Desconecta la refrigeradora 24 horas para descongelar. Si el hielo reaparece, el ciclo de deshielo no está funcionando.", "vuelve")
a("whirlpool|neveras|1", "Aleja la refrigeradora de la pared y limpia el polvo del condensador en la parte trasera.", "vuelve")
a("whirlpool|neveras|2", "Abre la llave de agua, cambia el filtro si pasaron seis meses y revisa que la manguera no esté doblada.", "vuelve")
a("whirlpool|neveras|3", "Limpia el condensador y deja espacio de ventilación a los lados y atrás.", "tec")
a("whirlpool|lavadoras|0", "Si llena de agua con la tapa cerrada pero el agitador no se mueve, no sigas forzando: puede ser el embrague o la transmisión.", "tec")
a("whirlpool|lavadoras|1", "Cierra la tapa firmemente y revisa que no haya ropa atrapada en el borde.", "vuelve")
a("whirlpool|lavadoras|2", "Anota el código F, apaga la lavadora 5 minutos y revisa la llave de agua y la manguera de desagüe.", "vuelve")
a("whirlpool|lavadoras|3", "Reacomoda la carga y nivela la lavadora.", "vuelve")
a("whirlpool|secadoras|0", "Limpia el filtro de pelusa y el ducto. Si es eléctrica, confirma en el breaker que lleguen los dos polos.", "tec")
a("whirlpool|secadoras|1", "Abre la puerta: si el tambor no gira ni con la mano, no insistas con el motor.", "tec")
a("whirlpool|secadoras|2", "Limpia el filtro y el ducto de salida: el sobrecalentamiento corta el ciclo.", "vuelve")
a("whirlpool|cocinas|0", "Confirma que elegiste la función correcta y deja precalentar el tiempo completo.", "vuelve")
a("whirlpool|cocinas|1", "Prueba con otro quemador y limpia los contactos. Revisa que el selector esté bien colocado.", "vuelve")
a("whirlpool|lavavajillas|0", "Revisa que la puerta cierre bien, que ningún plato impida el cierre y que el sello esté limpio.", "vuelve")
a("whirlpool|lavavajillas|1", "Limpia el filtro del fondo y revisa la manguera de desagüe.", "vuelve")

# ---------------- MABE
a("mabe|neveras|0", "Desconecta la refrigeradora 24 horas para descongelar y revisa que nada tape las salidas de aire.", "vuelve")
a("mabe|neveras|1", "Limpia el polvo del condensador y deja espacio de ventilación. Si el compresor se calienta demasiado, desconecta la refrigeradora.", "tec")
a("mabe|neveras|2", "Prueba el empaque con una hoja de papel: si sale sin resistencia, ya no sella. Límpialo con agua tibia.", "vuelve")
a("mabe|lavadoras|0", "Si llena de agua pero no agita, no sigas forzando: puede ser la transmisión o la correa.", "tec")
a("mabe|lavadoras|1", "Limpia el filtro de la bomba y revisa la manguera de desagüe.", "vuelve")
a("mabe|lavadoras|2", "Cierra bien la tapa y reacomoda la carga.", "vuelve")
a("mabe|lavadoras|3", "Cierra la llave de agua y desconecta la lavadora. No la uses hasta ubicar de dónde sale el agua.", "ya")
a("mabe|centro-lavado|0", "Revisa el breaker y el tomacorriente: las dos unidades comparten la alimentación eléctrica.", "vuelve")
a("mabe|centro-lavado|1", "Limpia el filtro de pelusa y el ducto de salida.", "vuelve")
a("mabe|aires|0", "Lava los filtros y confirma que el control esté en modo frío.", "vuelve")
a("mabe|aires|1", "Después de una tormenta no lo reinicies varias veces. Protege el aire con un protector de voltaje.", "tec")
a("mabe|cocinas|0", "Revisa que la llave del gas esté abierta y el selector en su posición. Si hueles gas, cierra la llave y ventila.", "vuelve")
a("mabe|cocinas|1", "Limpia el quemador con un cepillo suave y seca las bujías.", "vuelve")

# ---------------- FRIGIDAIRE
a("frigidaire|neveras|0", "Desconecta la refrigeradora 5 minutos y vuelve a conectarla; revisa que el panel esté limpio y seco.", "vuelve")
a("frigidaire|neveras|1", "Revisa que nada tape las rejillas de aire y que la puerta cierre bien.", "vuelve")
a("frigidaire|neveras|2", "Aleja la refrigeradora de la pared y revisa que no haya hielo ni objetos rozando el ventilador.", "vuelve")
a("frigidaire|lavadoras|0", "Limpia el filtro de la bomba y revisa la manguera de desagüe.", "vuelve")
a("frigidaire|lavadoras|1", "Abre la llave de agua y limpia las mallas de entrada.", "vuelve")
a("frigidaire|lavadoras|2", "Cierra bien la puerta y revisa que no haya ropa atrapada.", "vuelve")
a("frigidaire|lavadoras|3", "Nivela la lavadora y reacomoda la carga.", "vuelve")
a("frigidaire|secadoras|0", "Revisa el breaker y que la puerta cierre bien; limpia el filtro de pelusa.", "tec")
a("frigidaire|secadoras|1", "Limpia el filtro y el ducto de ventilación, que suele ser largo y acumula pelusa.", "vuelve")
a("frigidaire|cocinas|0", "Confirma la función elegida y deja precalentar el tiempo completo.", "vuelve")
a("frigidaire|cocinas|1", "Prueba la función de convección con el horno vacío; si el ventilador no gira, no sigas usándola.", "tec")
a("frigidaire|centro-lavado|0", "Apaga desde el breaker 5 minutos y prueba cada unidad por separado.", "tec")
a("frigidaire|centro-lavado|1", "Limpia el filtro de pelusa y el ducto de la secadora.", "vuelve")

# ---------------- ELECTROLUX
a("electrolux|neveras|0", "Revisa el enchufe y el breaker. Si el compresor no arranca ni hace ruido, no la reinicies varias veces.", "tec")
a("electrolux|neveras|1", "Aleja la refrigeradora de la pared y revisa que no haya hielo ni objetos en el ventilador.", "vuelve")
a("electrolux|neveras|2", "Cierra bien la puerta y revisa que el empaque no esté deformado ni que algo la trabe.", "vuelve")
a("electrolux|lavadoras|0", "Abre la llave de agua y limpia las mallas de entrada.", "vuelve")
a("electrolux|lavadoras|1", "Limpia el filtro de la bomba y revisa la manguera de desagüe.", "vuelve")
a("electrolux|lavadoras|2", "Cierra bien la puerta y revisa el empaque.", "vuelve")
a("electrolux|lavadoras|3", "Nivela la lavadora y reacomoda la carga.", "vuelve")
a("electrolux|cocinas|0", "Revisa que las rejillas de ventilación de la placa no estén tapadas y usa ollas de base plana.", "vuelve")
a("electrolux|cocinas|1", "Confirma la función elegida y deja precalentar el tiempo completo.", "vuelve")
a("electrolux|secadoras|0", "Limpia el filtro y el condensador.", "vuelve")
a("electrolux|secadoras|1", "Limpia el filtro y revisa que el ducto no esté aplastado.", "vuelve")

# ---------------- GENERAL ELECTRIC
a("general-electric|neveras|0", "Revisa que el hielo no esté trabado en el molde y que la llave de agua esté abierta.", "vuelve")
a("general-electric|neveras|1", "Revisa que nada tape las rejillas de aire y que la puerta cierre bien.", "vuelve")
a("general-electric|neveras|2", "Seca el piso, cierra la llave de agua y mira si la humedad viene del desagüe o de la manguera.", "vuelve")
a("general-electric|lavadoras|0", "Si llena de agua pero no agita, no sigas forzando: puede ser el acople del motor.", "tec")
a("general-electric|lavadoras|1", "Limpia el filtro de la bomba y revisa la manguera de desagüe.", "vuelve")
a("general-electric|lavavajillas|0", "Limpia el filtro y revisa el triturador, siempre con el equipo desconectado.", "vuelve")
a("general-electric|lavavajillas|1", "Limpia los brazos rociadores y el filtro.", "vuelve")
a("general-electric|cocinas|0", "Confirma la función elegida y deja precalentar el tiempo completo.", "vuelve")
a("general-electric|cocinas|1", "Seca y limpia las bujías. Si hueles gas, cierra la llave y ventila.", "vuelve")
a("general-electric|centro-lavado|0", "Limpia el filtro de pelusa y el ducto de salida.", "vuelve")
a("general-electric|centro-lavado|1", "Cierra bien la tapa y reacomoda la carga.", "vuelve")

# ---------------- HACEB
a("haceb|neveras|0", "Aleja la nevera de la pared y revisa que nada tape las salidas de aire.", "vuelve")
a("haceb|neveras|1", "Desconecta la nevera 24 horas para que se descongele la escarcha.", "vuelve")
a("haceb|lavadoras|0", "Cierra bien la tapa y reacomoda la carga.", "vuelve")
a("haceb|lavadoras|1", "Limpia el filtro de la bomba y revisa la manguera de desagüe.", "vuelve")
a("haceb|secadoras|0", "Limpia el filtro de pelusa y el ducto de salida, y no sobrecargues el tambor.", "vuelve")
a("haceb|secadoras|1", "Revisa el breaker o la conexión; si el tambor gira pero no calienta, hay una pieza de calentamiento dañada.", "tec")
a("haceb|secadoras|2", "Limpia el filtro y el ducto: el sobrecalentamiento hace que se apague sola.", "vuelve")
a("haceb|secadoras|3", "Revisa que no haya objetos dentro del tambor y que la secadora esté nivelada.", "vuelve")
a("haceb|cocinas|0", "Seca y limpia las bujías. Si hueles gas, cierra la llave y ventila.", "vuelve")
a("haceb|cocinas|1", "Confirma la función elegida y deja precalentar el tiempo completo.", "vuelve")
a("haceb|aires|0", "Lava los filtros y confirma que el control esté en modo frío.", "vuelve")
a("haceb|aires|1", "Apaga el aire y revisa que el desagüe no esté tapado ni doblado.", "vuelve")

# ---------------- KITCHENAID
a("kitchenaid|batidoras|0", "Apaga y desconecta la batidora ya. No la uses hasta que se abra la caja de engranes y se cambie la grasa.", "ya")
a("kitchenaid|batidoras|1", "Usa una velocidad menor, reduce la cantidad de masa y no la sobrecargues.", "vuelve")
a("kitchenaid|batidoras|2", "Detén la batidora: el rechinado indica falta de grasa o engranes dañados.", "tec")
a("kitchenaid|batidoras|3", "Con la batidora apagada, ajusta el tornillo de altura del batidor en la cabeza.", "vuelve")
a("kitchenaid|neveras|0", "Revisa que nada tape las rejillas de aire y que la puerta cierre bien.", "vuelve")
a("kitchenaid|neveras|1", "Cambia el filtro de agua si pasaron seis meses y revisa que la llave de agua esté abierta.", "vuelve")

def consejo_de(m, e, k):
    return C[f"{m}|{e}|{k}"]
