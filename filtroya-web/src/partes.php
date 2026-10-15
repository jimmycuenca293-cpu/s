<?php
declare(strict_types=1);
// Encabezado y pie de las páginas de producto, marca, legales y de pago.
require_once __DIR__ . '/api/sitio.php';

function cabeza(string $titulo, string $desc, string $ruta, string $extra = '', bool $indexar = true): void
{
    $S = sitio();
    $canon = $S['base'] . $ruta;
    $n = $S['negocio'];
    echo '<!doctype html><html lang="es-CO"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        . '<title>' . h($titulo) . '</title><meta name="description" content="' . h($desc) . '">'
        . ($indexar ? '<link rel="canonical" href="' . h($canon) . '">' : '<meta name="robots" content="noindex">')
        . '<meta property="og:type" content="website"><meta property="og:title" content="' . h($titulo) . '"><meta property="og:description" content="' . h($desc) . '"><meta property="og:url" content="' . h($canon) . '"><meta property="og:locale" content="es_CO">'
        . '<meta name="theme-color" content="#0a2a2e"><link rel="icon" href="/img/icono.svg" type="image/svg+xml"><link rel="stylesheet" href="/estilo.css">' . $extra . '</head><body>'
        . '<header class="top"><div class="wrap"><a class="logo" href="/"><img src="/img/icono.svg" alt="" width="26" height="26">Filtro<span>Ya</span></a><a class="btn sm" href="/#catalogo">Ver filtros</a></div></header><main class="wrap">';
}

function pie(): void
{
    $S = sitio();
    $n = $S['negocio'];
    $marcas = catalogo()['marcas'];
    echo '</main><footer class="pie"><div class="wrap"><nav><b>Filtros por marca</b>';
    foreach ($marcas as $m) echo '<a href="/marca/' . h($m['slug']) . '/">Filtros ' . h($m['nombre']) . '</a>';
    echo '</nav><nav><b>Ayuda</b><a href="/referencias/">Buscar por referencia</a><a href="/neveras/">Filtro por modelo de nevecón</a><a href="/guia/">Guías</a><a href="/cali/">Instalación gratis en Cali</a>';
    echo '</nav><nav><b>Información</b><a href="/terminos.php">Términos y condiciones</a><a href="/privacidad.php">Tratamiento de datos</a><a href="/terminos.php#garantia">Garantía y retracto</a></nav>'
        . '<p>' . h($n['nombre']) . ' · ' . h($n['titular']) . ' · ' . h($n['documento']) . '<br>' . h($n['direccion']) . ' · ' . h($n['telefono']) . ' · ' . h($n['correo']) . '<br>'
        . 'Precios en pesos colombianos, con envío incluido. Las marcas mencionadas pertenecen a sus dueños; somos un comercio independiente.</p></div></footer></body></html>';
}
