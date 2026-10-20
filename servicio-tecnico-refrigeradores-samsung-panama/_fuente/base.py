# -*- coding: utf-8 -*-
"""Datos generales del sitio de servicio técnico de refrigeradoras Samsung en Panamá."""
DOMINIO = "https://refrigeradorsamsungpanama.click"
NOMBRE = "Refrigeradoras Samsung Panamá"
TEL = "+507 6933-7976"
WA = "50769337976"
HORARIO = "Lun a Sáb 7:00am–6:00pm"
GTM_ID = ""
VERIFICACION = ""

TIPOS = [
 ("side-by-side", "Side by Side", "dos puertas verticales", "RS", "Las refrigeradoras Side by Side tienen el congelador a un lado y la refrigeración al otro. Suelen traer dispensador de agua y hielo en la puerta.",
  ["Dispensador de agua y hielo", "Ventiladores para el congelador y la refrigeración", "Sistemas de descongelación automática", "Tarjetas de control y pantalla"],
  ["No hace hielo o el dispensador no saca agua", "Escarcha en el congelador", "Ruido del ventilador", "Agua bajo la refrigeradora"]),
 ("french-door", "French Door", "puertas dobles arriba y cajón de congelador abajo", "RF", "Las French Door tienen dos puertas abatibles en la parte de refrigeración y un cajón de congelador abajo. Son comunes en apartamentos modernos y cocinas empotradas.",
  ["Fábrica de hielo y dispensador (según modelo)", "Compresor inverter", "Varios sensores de temperatura", "Cajón del congelador con rieles"],
  ["El cajón del congelador no cierra bien", "Fábrica de hielo congelada", "Falla de sensor o tarjeta", "Condensación en las puertas"]),
 ("congelador-superior", "Congelador superior (Top Mount)", "congelador arriba y refrigeración abajo", "RT", "Es el diseño clásico: congelador arriba y refrigeración abajo. Es el más común en casas y apartamentos, con o sin dispensador de agua.",
  ["Ventilador del evaporador", "Descongelación por resistencia", "Termostato y sensores", "Empaques de puerta"],
  ["No enfría la parte de abajo", "Escarcha en el fondo del congelador", "Gotea agua dentro", "Ruido del compresor"]),
 ("congelador-inferior", "Congelador inferior (Bottom Mount)", "refrigeración arriba y cajón de congelador abajo", "RB", "Con la refrigeración arriba, los alimentos de uso diario quedan a la altura de los ojos. El congelador va abajo en un cajón.",
  ["Compresor y condensador", "Ventilador del congelador", "Rieles del cajón", "Sensores de temperatura"],
  ["El cajón se traba o no sella", "No congela bien", "Hielo en el cajón", "Alarma de puerta"]),
 ("family-hub", "Family Hub y modelos con pantalla", "con pantalla táctil integrada", "RF", "Algunos modelos Samsung incluyen pantalla táctil, cámaras internas y conexión Wi-Fi. Además de la parte de refrigeración, requieren revisar la electrónica y la conexión.",
  ["Pantalla táctil y tarjeta electrónica", "Conexión Wi-Fi", "Sensores y cámaras", "Sistema de enfriamiento tradicional"],
  ["La pantalla no enciende o se congela", "No conecta a la red", "Falla de sensor", "Errores tras un corte de luz"]),
 ("con-dispensador", "Refrigeradoras con dispensador de agua y hielo", "agua fría y hielo en la puerta", "", "Los dispensadores de agua y hielo son cómodos, pero dependen de un filtro, una válvula, mangueras y una fábrica de hielo que pueden fallar o congelarse.",
  ["Filtro de agua", "Válvula de entrada de agua", "Manguera y conexión", "Fábrica de hielo y sensor"],
  ["No sale agua", "No hace hielo", "Agua con mal sabor", "Fuga en la conexión"]),
]

SERVICIOS = {
 "reparacion-refrigeradoras-samsung-panama": ("Reparación de refrigeradoras Samsung a domicilio en Panamá", "Reparación a domicilio",
   "Vamos a tu casa o apartamento, revisamos tu refrigeradora Samsung, te explicamos la falla y te damos el costo antes de reparar.",
   ["Revisión del equipo en tu casa", "Explicación clara de la falla y su causa", "Costo confirmado antes de reparar", "Reparación en la misma visita cuando hay repuesto", "Garantía sobre la pieza y la mano de obra"]),
 "mantenimiento-refrigeradoras-samsung-panama": ("Mantenimiento preventivo de refrigeradoras Samsung en Panamá", "Mantenimiento preventivo",
   "Un mantenimiento a tiempo evita daños mayores: limpieza del condensador, revisión de ventiladores, empaques, desagües y sensores.",
   ["Limpieza del condensador y del compresor", "Revisión de ventiladores y descongelación", "Revisión de empaques y bisagras", "Limpieza del desagüe de descongelación", "Recomendaciones de temperatura y uso"]),
 "diagnostico-refrigeradoras-samsung-panama": ("Diagnóstico a domicilio: ¿vale la pena reparar tu refrigeradora Samsung?", "Diagnóstico a domicilio",
   "Si no sabes qué le pasa a tu refrigeradora o si conviene repararla, hacemos un diagnóstico honesto: qué falla, cuánto cuesta y si vale la pena.",
   ["Revisión completa del síntoma", "Medición de temperaturas y voltaje", "Causa probable explicada", "Costo estimado y opinión honesta", "Sin compromiso de reparar"]),
 "cambio-filtro-agua-refrigeradora-samsung-panama": ("Cambio de filtro de agua de refrigeradoras Samsung en Panamá", "Cambio de filtro de agua",
   "Cambiamos el filtro de agua de tu refrigeradora Samsung y revisamos el dispensador, la manguera y el flujo de agua.",
   ["Cambio del filtro de agua", "Prueba de flujo en el dispensador", "Revisión de mangueras y conexiones", "Purga del sistema", "Recomendación de frecuencia de cambio"]),
 "fabrica-de-hielo-refrigeradora-samsung-panama": ("Reparación de la fábrica de hielo de refrigeradoras Samsung en Panamá", "Fábrica de hielo",
   "Si tu refrigeradora Samsung no hace hielo, hace poco o el hielo sale con mal sabor, revisamos la fábrica de hielo, la válvula y el sensor.",
   ["Revisión de la fábrica de hielo", "Prueba de válvula de agua", "Revisión de sensor y temperatura", "Limpieza y descongelación", "Reparación o cambio de piezas"]),
 "reparacion-fuga-refrigeradora-samsung-panama": ("Reparación de fugas de agua y de gas en refrigeradoras Samsung en Panamá", "Fugas de agua y de gas",
   "Ubicamos la causa de una fuga de agua (desagüe, manguera, válvula) o de una pérdida de enfriamiento por fuga de gas refrigerante.",
   ["Ubicación del origen de la fuga", "Desagüe, mangueras y válvulas", "Revisión del sistema de enfriamiento", "Explicación clara de las opciones", "Garantía del trabajo realizado"]),
}

ZONAS = [
 ("San Francisco", "torres", "Ciudad de Panamá"), ("Bella Vista", "torres", "Ciudad de Panamá"), ("El Cangrejo", "mixto", "Ciudad de Panamá"),
 ("Obarrio", "torres", "Ciudad de Panamá"), ("Marbella", "torres", "Ciudad de Panamá"), ("Costa del Este", "torres", "Ciudad de Panamá"),
 ("Punta Pacífica", "torres", "Ciudad de Panamá"), ("Paitilla", "torres", "Ciudad de Panamá"), ("Avenida Balboa", "torres", "Ciudad de Panamá"),
 ("Calidonia", "mixto", "Ciudad de Panamá"), ("Casco Antiguo", "mixto", "Ciudad de Panamá"), ("Betania", "casas", "Ciudad de Panamá"),
 ("Villa de las Fuentes", "casas", "Ciudad de Panamá"), ("Altos del Golf", "casas", "Ciudad de Panamá"), ("Brisas del Golf", "casas", "Ciudad de Panamá"),
 ("Condado del Rey", "casas", "Ciudad de Panamá"), ("Villa Lucre", "casas", "San Miguelito"), ("San Miguelito", "popular", "San Miguelito"),
 ("Las Cumbres", "popular", "Ciudad de Panamá"), ("Chilibre", "popular", "Ciudad de Panamá"), ("Pueblo Nuevo", "mixto", "Ciudad de Panamá"),
 ("Parque Lefevre", "mixto", "Ciudad de Panamá"), ("Río Abajo", "mixto", "Ciudad de Panamá"), ("Juan Díaz", "mixto", "Ciudad de Panamá"),
 ("Pedregal", "mixto", "Ciudad de Panamá"), ("Tocumen", "mixto", "Ciudad de Panamá"), ("Albrook", "mixto", "Ciudad de Panamá"),
 ("Clayton", "torres", "Ciudad de Panamá"), ("Ancón", "casas", "Ciudad de Panamá"), ("Costa Verde", "casas", "Panamá Oeste"),
 ("Arraiján", "casas", "Panamá Oeste"), ("Vista Alegre", "casas", "Panamá Oeste"), ("La Chorrera", "casas", "Panamá Oeste"),
 ("Panamá Pacífico", "casas", "Panamá Oeste"), ("Chame", "casas", "Panamá Oeste"), ("Coronado", "casas", "Panamá Oeste"),
]
TIPO_TXT = {
 "torres": ("En esta zona predominan los edificios y torres de apartamentos. Antes de ir coordinamos con la administración el horario, el ingreso de herramientas y el uso del ascensor de servicio, para que la visita no tenga contratiempos.",
            "En apartamentos las refrigeradoras suelen estar empotradas en la cocina, con poco espacio detrás: revisamos la ventilación del condensador y la nivelación, causas frecuentes de ruido y de sobrecalentamiento."),
 "casas": ("Aquí hay muchas casas y residenciales, a veces con refrigeradora adicional en la terraza o la lavandería. Revisamos también las condiciones del lugar: ventilación, humedad, tomacorrientes y calor.",
           "En casas, las variaciones de voltaje y los cortes de luz son causas frecuentes de daños a tarjetas y compresores; te explicamos cómo proteger tu refrigeradora."),
 "popular": ("Atendemos viviendas y apartamentos de la zona con el mismo diagnóstico claro: te explicamos la falla, el costo y las opciones antes de reparar.",
             "Muchas veces el problema se resuelve con una pieza accesible (ventilador, sensor, empaque o descongelación); si el equipo ya no vale la pena reparar, te lo decimos con honestidad."),
 "mixto": ("Es una zona con casas, apartamentos y negocios pequeños. Adaptamos la visita al lugar: coordinamos acceso, estacionamiento y horario contigo.",
           "Revisamos la refrigeradora en el sitio, medimos temperaturas, explicamos la falla y confirmamos el costo antes de empezar cualquier reparación."),
}

FAQ_GENERAL = [
 ("¿Son servicio técnico autorizado de Samsung?", "No. Somos un servicio técnico independiente especializado en refrigeradoras Samsung. Si tu equipo está en garantía de fábrica, te lo decimos para que la hagas valer donde corresponda."),
 ("¿Qué modelos de refrigeradora Samsung reparan?", "Side by Side, French Door, congelador superior, congelador inferior, modelos con dispensador de agua y hielo, y modelos con pantalla."),
 ("¿Por qué mi refrigeradora Samsung no enfría?", "Las causas más comunes son ventilador del evaporador con hielo, falla del sistema de descongelación, sensor de temperatura, tarjeta de control o compresor. El diagnóstico a domicilio ubica la causa exacta."),
 ("¿Dónde dan servicio?", "En Ciudad de Panamá, San Miguelito y Panamá Oeste: San Francisco, Bella Vista, Obarrio, Costa del Este, Punta Pacífica, Betania, Albrook, Arraiján, La Chorrera y más."),
 ("¿Cuánto tardan en llegar?", "Coordinamos visitas en 24 a 48 horas en la mayoría de las zonas; te confirmamos disponibilidad por WhatsApp."),
 ("¿Cuánto cuesta la reparación?", "Depende de la falla y de la pieza. Te confirmamos el costo de la visita por WhatsApp antes de ir y el costo de la reparación antes de empezar."),
 ("¿Dan garantía?", "Sí, cada reparación incluye garantía sobre la pieza reemplazada y sobre la mano de obra. El plazo se confirma antes de empezar."),
 ("¿Cuál es el horario?", "De lunes a sábado, de 7:00am a 6:00pm."),
]
