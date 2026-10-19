<?php
require __DIR__ . '/api/sitio.php';
header('Content-Type: text/plain; charset=utf-8');
echo str_replace('__BASE__', sitio()['base'], <<<'TXT'
# Filtros para lavadora Samsung

> Filtros de pelusas y bolsas de malla para lavadoras Samsung de carga superior y frontal, con envío a toda Colombia. El precio y el modelo correcto se confirman con un asesor por WhatsApp (305 479 6329).

## Productos
- [Filtro de pelusas azul para lavadora Samsung](__BASE__/filtro-pelusas-lavadora-samsung-azul/): Carga superior.
- [Filtro de pelusas gris tipo panal para lavadora Samsung](__BASE__/filtro-pelusas-lavadora-samsung-gris-panal/): Carga superior.
- [Filtro de pelusas negro con malla de triángulos para lavadora Samsung](__BASE__/filtro-pelusas-lavadora-samsung-negro-triangulos/): Carga superior.
- [Filtro de pelusas verde Magic Filter para lavadora Samsung](__BASE__/filtro-pelusas-lavadora-samsung-verde/): Carga superior.
- [Bolsa de malla para pelusas para lavadora Samsung](__BASE__/bolsa-malla-pelusas-lavadora-samsung/): Bolsa de malla.
- [Filtro para lavadora de carga frontal para lavadora Samsung](__BASE__/filtro-pelusas-lavadora-samsung-carga-frontal/): Carga frontal.

## Guías
- [Cuál filtro necesita mi lavadora](__BASE__/cual-es-mi-filtro/)
- [Cómo limpiar y cambiar el filtro](__BASE__/cambio-e-instalacion/)
TXT);
