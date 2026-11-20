# -*- coding: utf-8 -*-
"""Contenido adicional por electrodoméstico: hacerlo tú mismo, qué no hacer, señales de mala instalación y vida útil."""

EXTRA = {
 "refrigeradoras": dict(
  vida="12 a 15 años",
  diy=["Desconecta la refrigeradora y saca los alimentos delicados a una nevera portátil con hielo.", "Aspira o pasa un cepillo suave por el condensador (atrás o debajo) y por las rejillas.", "Limpia los empaques de las puertas con agua tibia y un poco de jabón, y sécalos bien.", "Lava las bandejas y cajones con agua y jabón suave; evita el agua muy caliente en el vidrio frío.", "Vuelve a conectar, ajusta la temperatura (4 °C en refrigerador y -18 °C en congelador son referencias habituales) y espera unas horas antes de volver a cargarla."],
  nohacer=["No uses cuchillos ni objetos metálicos para quitar el hielo: pueden perforar el evaporador.", "No desconectes y conectes la refrigeradora repetidamente: el compresor necesita unos minutos de reposo.", "No cubras las rejillas ni apiles cosas encima del equipo.", "No intentes recargar gas ni abrir el circuito de refrigerante."],
  mala_inst=["Ruido y vibración porque no está nivelada.", "Hielo en el congelador por falta de reposo antes de encender.", "Fugas en la manguera de agua del dispensador.", "El compresor se calienta porque no hay ventilación atrás."],
  cuando_cambiar=["el compresor falla en un equipo con más de 12 años", "hay fugas de gas en el evaporador o el serpentín", "la reparación y el repuesto se acercan a la mitad del precio de una nueva"],
  cuando_reparar=["falla un ventilador, un sensor, la resistencia de deshielo o el empaque", "la placa falla por un pico de voltaje y el equipo es relativamente nuevo"],
 ),
 "lavadoras": dict(
  vida="8 a 12 años",
  diy=["Desconecta la lavadora y cierra las llaves de agua.", "Limpia el filtro de la bomba (normalmente abajo, detrás de una tapa pequeña) con una bandeja debajo para recoger el agua.", "Retira y lava el dispensador de jabón con agua tibia, y limpia la cavidad donde va.", "Limpia el sello de la puerta (carga frontal), incluyendo los pliegues donde se acumula moho, con un paño y un poco de vinagre o limpiador suave.", "Haz un ciclo en caliente en vacío con un limpiador de lavadoras y deja la puerta abierta al terminar."],
  nohacer=["No sobrecargues el tambor, aunque la ropa parezca poca: el desbalance daña rodamientos y amortiguadores.", "No uses más jabón del indicado: la espuma aumenta fallas de nivel y de desagüe.", "No abras la puerta a la fuerza durante el ciclo.", "No muevas la lavadora sin colocar los tornillos de transporte si te mudas."],
  mala_inst=["Vibración y golpes al centrifugar.", "Fugas en las mangueras o el desagüe.", "Ciclos que se cortan por mala toma de agua.", "Ruido de gorgoteo en el desagüe."],
  cuando_cambiar=["el tambor o la tina están rotos o con óxido pasado", "los rodamientos fallan junto con el sello en un equipo con muchos años", "la reparación supera la mitad del precio de una nueva"],
  cuando_reparar=["falla la bomba, el filtro, la cerradura, el interruptor de tapa o la electroválvula", "la placa o el motor fallan en un equipo con pocos años"],
 ),
 "secadoras": dict(
  vida="10 a 13 años",
  diy=["Limpia el filtro de pelusa con las manos o un cepillo, y lávalo con agua si tiene residuos de suavizante.", "Aspira el espacio donde va el filtro y el interior del tambor.", "Desconecta la secadora y desmonta el ducto de escape para aspirar la pelusa acumulada.", "Limpia las barras del sensor de humedad con un paño con alcohol.", "Revisa que el ducto no esté aplastado ni doblado y que la salida exterior esté libre."],
  nohacer=["No seques ropa con restos de aceite, gasolina o solventes: es inflamable.", "No uses la secadora sin filtro de pelusa.", "No sobrecargues el tambor.", "No ignores el olor a quemado: apaga y desconecta."],
  mala_inst=["Ciclos largos porque el ducto es muy largo o tiene curvas.", "La secadora gira pero no calienta por conexión de 220 V incompleta.", "Humedad en el cuarto porque el aire sale dentro de la casa.", "Pelusa acumulada en lugares inesperados."],
  cuando_cambiar=["el tambor está deformado o oxidado", "la placa y el motor fallan a la vez", "la reparación supera la mitad del precio de una nueva"],
  cuando_reparar=["falla la resistencia, la correa, el termostato o el sensor de humedad", "el ducto de pelusa está tapado y el equipo se recalienta"],
 ),
 "cocinas-y-hornos": dict(
  vida="15 a 20 años",
  diy=["Con la cocina fría y el gas cerrado, retira rejillas y tapas de quemadores y lávalas con agua tibia y desengrasante suave.", "Limpia los orificios de los quemadores con un palillo o un cepillo de cerdas, sin forzarlos.", "Seca bien las tapas antes de volver a colocarlas para no humedecer las bujías.", "Limpia el interior del horno con un paño húmedo y producto adecuado, evitando mojar resistencias y sensores.", "Revisa la manguera de gas: busca grietas, resequedad o fechas vencidas y cámbiala si hace falta."],
  nohacer=["No uses la cocina si hay olor a gas: cierra la llave, ventila y llama.", "No uses el horno para calefaccionar la cocina.", "No cubras el piso del horno con papel de aluminio.", "No rocíes líquidos sobre perillas, bujías o paneles de inducción."],
  mala_inst=["Olor a gas por conexiones sin probar con jabón.", "Llama amarilla por mala mezcla de aire.", "Cocina desnivelada que derrama grasa.", "Placa de inducción que se apaga por circuito insuficiente."],
  cuando_cambiar=["el horno tiene la cavidad oxidada o la puerta deformada", "la placa o la mesa de inducción está agrietada", "faltan repuestos del modelo"],
  cuando_reparar=["falla un quemador, una bujía, el módulo de encendido o la resistencia", "el termostato o la válvula del horno no regula bien"],
 ),
 "aires-acondicionados": dict(
  vida="10 a 15 años",
  diy=["Apaga el aire y desconecta el breaker. Abre el panel frontal y retira los filtros.", "Lava los filtros con agua tibia y jabón suave, enjuaga y déjalos secar a la sombra.", "Pasa un paño suave por las rejillas y la carcasa de la unidad interior.", "Con el equipo apagado, limpia con una escoba suave el polvo y las hojas alrededor de la unidad exterior sin mojar la electrónica.", "Vuelve a colocar los filtros y comprueba que el drenaje esté libre."],
  nohacer=["No laves el serpentín con agua a presión.", "No abras el equipo con corriente conectada.", "No uses el aire con los filtros quitados.", "No intentes recargar gas por tu cuenta."],
  mala_inst=["Goteo dentro de la casa por mala pendiente del drenaje.", "Mala eficiencia por tubería muy larga o doblada.", "Vibración por soportes flojos en la unidad exterior.", "Humedad en el circuito por falta de vacío."],
  cuando_cambiar=["el compresor falla en un equipo con muchos años y gas antiguo", "el serpentín tiene varias fugas", "la placa exterior se daña seguido por mala instalación eléctrica"],
  cuando_reparar=["falla la placa, un sensor o el ventilador", "hay una fuga localizable o falta limpieza y gas"],
 ),
 "lavavajillas": dict(
  vida="9 a 12 años",
  diy=["Retira las bandejas y el filtro del fondo, y lávalos con agua tibia y un cepillo suave.", "Retira los brazos rociadores y limpia sus orificios con un palillo.", "Limpia el sello de la puerta y el borde de la tina con un paño húmedo.", "Haz un ciclo en caliente con un limpiador específico para lavavajillas.", "Revisa la sal y el abrillantador y ajusta la dureza del agua según el manual."],
  nohacer=["No uses jabón de lavar platos a mano: produce demasiada espuma.", "No cargues platos con restos grandes de comida.", "No bloquees los brazos rociadores con ollas altas.", "No fuerces la puerta si no cierra: revisa primero qué la bloquea."],
  mala_inst=["Fugas por conexiones sin revisar.", "Agua que vuelve del fregadero por falta de curva en la manguera.", "Equipo desnivelado que no cierra bien.", "Ciclos incompletos por poca presión de agua."],
  cuando_cambiar=["la tina tiene fugas o está oxidada", "la bomba y la placa fallan a la vez", "la reparación supera la mitad del precio de una nueva"],
  cuando_reparar=["falla la bomba, el filtro, un brazo rociador o el sello de la puerta", "hay sarro o residuos que bloquean el paso del agua"],
 ),
 "microondas": dict(
  vida="7 a 10 años",
  diy=["Desconecta el microondas y retira el plato giratorio y su aro.", "Limpia el interior con un paño húmedo y un poco de jabón suave; los restos de grasa carbonizada producen chispas.", "Limpia el borde de la puerta y el sello para que cierre bien.", "Lava el plato giratorio y el aro con agua y jabón y sécalos antes de colocarlos.", "Deja la puerta abierta unos minutos para ventilar antes de volver a usarlo."],
  nohacer=["No uses el microondas vacío.", "No pongas recipientes metálicos ni con borde dorado.", "No abras la carcasa: el capacitor guarda alto voltaje.", "No tapes las rejillas de ventilación."],
  mala_inst=["Sobrecalentamiento por falta de ventilación.", "Fallas por conectarlo con extensiones.", "Vibración por instalarlo en una superficie inestable.", "Humedad en la electrónica por estar cerca del fregadero."],
  cuando_cambiar=["el magnetrón falla y el equipo ya es antiguo", "la cavidad está oxidada o con chispas por daño en la pared interior", "el costo de la pieza se acerca al de uno nuevo"],
  cuando_reparar=["falla el plato giratorio, el fusible o la cerradura de la puerta", "el panel o el fusible de alta tensión necesitan cambio"],
 ),
}
