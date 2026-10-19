<?php
require __DIR__ . '/api/sitio.php';
header('Content-Type: text/plain; charset=utf-8');
echo str_replace('__BASE__', sitio()['base'], <<<'TXT'
# Filtros para lavadoras Samsung y LG

> Filtros de pelusas y bolsas de malla para lavadoras Samsung y LG, y filtro para secadora LG, con envío a toda Colombia. El precio y el modelo correcto se confirman con un asesor por WhatsApp.

## Samsung (WhatsApp 305 479 6329)
- [Filtros para lavadora Samsung](__BASE__/samsung/)
- [Filtro de pelusas azul para lavadora Samsung](__BASE__/samsung/filtro-pelusas-lavadora-samsung-azul/): Carga superior.
- [Filtro de pelusas gris tipo panal para lavadora Samsung](__BASE__/samsung/filtro-pelusas-lavadora-samsung-gris-panal/): Carga superior.
- [Filtro de pelusas negro con malla de triángulos para lavadora Samsung](__BASE__/samsung/filtro-pelusas-lavadora-samsung-negro-triangulos/): Carga superior.
- [Filtro de pelusas verde para lavadora Samsung](__BASE__/samsung/filtro-pelusas-lavadora-samsung-verde/): Carga superior.
- [Bolsa de malla para pelusas para lavadora Samsung](__BASE__/samsung/bolsa-malla-pelusas-lavadora-samsung/): Bolsa de malla.
- [Filtro para lavadora de carga frontal para lavadora Samsung](__BASE__/samsung/filtro-pelusas-lavadora-samsung-carga-frontal/): Carga frontal.
- [Cuál filtro necesita mi lavadora](__BASE__/samsung/cual-es-mi-filtro/)
- [Cómo limpiar y cambiar el filtro](__BASE__/samsung/cambio-e-instalacion/)

## LG (WhatsApp 320 510 2995)
- [Filtros para lavadora LG](__BASE__/lg/)
- [Bolsa de malla para pelusas para lavadora LG](__BASE__/lg/bolsa-malla-pelusas-lavadora-lg/): Bolsa de malla.
- [Filtro de pelusas redondo azul para lavadora LG](__BASE__/lg/filtro-pelusas-redondo-lavadora-lg/): Filtro redondo.
- [Filtro de pelusas gris con círculos y rejillas para lavadora LG](__BASE__/lg/filtro-pelusas-gris-circulos-lavadora-lg/): Filtro rectangular.
- [Filtro de pelusas gris con tapa de flechas para lavadora LG](__BASE__/lg/filtro-pelusas-gris-tapa-flechas-lavadora-lg/): Filtro rectangular.
- [Filtro de pelusas para secadora LG](__BASE__/lg/filtro-pelusas-secadora-lg/): Secadora.
- [Cuál filtro necesita mi lavadora](__BASE__/lg/cual-es-mi-filtro/)
- [Cómo limpiar y cambiar el filtro](__BASE__/lg/cambio-e-instalacion/)
TXT);
