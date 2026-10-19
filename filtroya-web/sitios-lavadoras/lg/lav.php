<?php
// Piezas comunes de la tienda de filtros para lavadoras (generado por lavadoras.py)
require_once __DIR__ . '/marcas.php';
$M = json_decode(file_get_contents(__DIR__ . '/marca.json'), true);
function lav_cabeza(string $titulo, string $desc, string $ruta, string $extra, string $json): void
{
    global $M;
    $ld = $json !== '' ? '<script type="application/ld+json">' . str_replace('__BASE__', sitio()['base'], $json) . '</script>' : '';
    cabeza_marca($M, $titulo, $desc, $ruta, $extra . $ld);
}
function lav_pie(): void { global $M; pie_marca($M); }
