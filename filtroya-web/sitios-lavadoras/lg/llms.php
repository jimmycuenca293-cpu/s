<?php
require __DIR__ . '/api/sitio.php';
header('Content-Type: text/plain; charset=utf-8');
echo str_replace('__BASE__', sitio()['base'], <<<'TXT'
# Filtros para lavadora LG

> Filtros de pelusas y bolsas de malla para lavadoras LG de carga superior y frontal, con envío a toda Colombia. El precio y el modelo correcto se confirman con un asesor por WhatsApp (320 510 2995).

## Productos
- [Bolsa de malla para pelusas para lavadora LG](__BASE__/bolsa-malla-pelusas-lavadora-lg/): Bolsa de malla.
- [Filtro de pelusas redondo azul para lavadora LG](__BASE__/filtro-pelusas-redondo-lavadora-lg/): Filtro redondo.
- [Filtro de pelusas gris con círculos y rejillas para lavadora LG](__BASE__/filtro-pelusas-gris-circulos-lavadora-lg/): Filtro rectangular.
- [Filtro de pelusas gris con tapa de flechas para lavadora LG](__BASE__/filtro-pelusas-gris-tapa-flechas-lavadora-lg/): Filtro rectangular.

## Guías
- [Cuál filtro necesita mi lavadora](__BASE__/cual-es-mi-filtro/)
- [Cómo limpiar y cambiar el filtro](__BASE__/cambio-e-instalacion/)
TXT);
