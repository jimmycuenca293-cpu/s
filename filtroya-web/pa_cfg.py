"""Configuración por sitio para pa_diseno.py y pa_contenido.py. Se elige con la variable de entorno SITIO (panama | cali)."""
import os
SITIO = os.environ.get("SITIO", "panama")
CFG = {
 "panama": dict(
    dom="https://samsungpanamaserviciotecnico.com", nombre="Servicio Técnico Samsung Panamá", ciudad="Ciudad de Panamá", corto="Panamá", pais="Panamá",
    dir="Vía España, Panamá, Provincia de Panamá", tel="+507 6933-7976", tel_link="+50769337976", wa="50769337976", horario="Abierto las 24 horas",
    cobertura="Ciudad de Panamá y alrededores (50 barrios y corregimientos)", eq_slug={"Refrigeradoras": "refrigeradoras", "Lavadoras": "lavadoras", "Secadoras": "secadoras", "Lavavajillas": "lavavajillas", "Estufas y hornos": "estufas-y-hornos", "Microondas": "microondas"},
    eq_clave=("Refrigeradoras", "Lavadoras", "Secadoras", "Lavavajillas", "Estufas y hornos", "Microondas"), eq_nombre_falla={"Estufa": "Estufas y hornos", "Horno": "Estufas y hornos"}, voltaje="110-120 V a 60 Hz", cats_clima="Energía y clima en Panamá",
    ley_datos="la Ley 81 de 2019 sobre protección de datos personales de la República de Panamá y su reglamentación", autoridad_datos="la autoridad de protección de datos personales de Panamá (ANTAI)",
    ley_consumo="la Ley 45 de 2007 sobre protección al consumidor", autoridad_consumo="la Autoridad de Protección al Consumidor y Defensa de la Competencia (ACODECO)", ley_aplicable="las leyes de la República de Panamá",
    derechos="acceder a tus datos, rectificarlos, cancelarlos u oponerte a su tratamiento, y a pedir la portabilidad cuando corresponda", humedad=True, extras_links=[]),
 "cali": dict(
    dom="https://samsungcaliserviciotecnico.com", nombre="Servicio Técnico Samsung Cali", ciudad="Cali", corto="Cali", pais="Colombia",
    dir="Cl. 65, Las Ceibas, Cali, Valle del Cauca", tel="+57 301 381 0242", tel_link="+573013810242", wa="573013810242", horario="Abierto las 24 horas",
    cobertura="Cali y Jamundí, Yumbo y alrededores (barrios y comunas de Cali)", eq_slug={"Neveras": "neveras", "Lavadoras": "lavadoras", "Secadoras": "secadoras", "Lavavajillas": "lavavajillas", "Estufas y hornos": "estufas-y-hornos", "Microondas": "microondas"},
    eq_clave=("Neveras", "Lavadoras", "Secadoras", "Lavavajillas", "Estufas y hornos", "Microondas"), eq_nombre_falla={"Estufa": "Estufas y hornos", "Horno": "Estufas y hornos"}, voltaje="110 V a 60 Hz", cats_clima="Energía y clima en Cali",
    ley_datos="la Ley 1581 de 2012 de protección de datos personales de Colombia y sus decretos reglamentarios", autoridad_datos="la Superintendencia de Industria y Comercio (SIC), autoridad de protección de datos personales de Colombia",
    ley_consumo="la Ley 1480 de 2011 (Estatuto del Consumidor)", autoridad_consumo="la Superintendencia de Industria y Comercio (SIC)", ley_aplicable="las leyes de la República de Colombia",
    derechos="conocer, actualizar y rectificar tus datos, solicitar la supresión y revocar tu autorización cuando corresponda", humedad=False, extras_links=[("comunas/", "Comunas de Cali"), ("diagnostico-rapido-samsung/", "Diagnóstico rápido"), ("conviene-reparar-o-cambiar-samsung/", "¿Reparar o cambiar?")]),
}[SITIO]
