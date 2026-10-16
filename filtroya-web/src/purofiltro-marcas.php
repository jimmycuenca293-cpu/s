<?php
declare(strict_types=1);
// Encabezado y pie de las tiendas exclusivas por marca (Samsung, LG, Whirlpool, GE).
// Cada tienda solo enlaza a sus propias páginas: no se mezclan marcas.
require_once __DIR__ . '/partes.php';

function cabeza_marca(array $M, string $titulo, string $desc, string $ruta, string $extra = ''): void
{
    $S = sitio();
    $canon = $S['base'] . $ruta;
    $b = $M['base'];
    echo '<!doctype html><html lang="es-CO"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        . '<title>' . h($titulo) . '</title><meta name="description" content="' . h($desc) . '"><link rel="canonical" href="' . h($canon) . '">'
        . '<meta property="og:type" content="website"><meta property="og:title" content="' . h($titulo) . '"><meta property="og:description" content="' . h($desc) . '"><meta property="og:url" content="' . h($canon) . '"><meta property="og:locale" content="es_CO"><meta property="og:site_name" content="' . h($n = $S['negocio']['nombre']) . '">'
        . '<meta name="theme-color" content="' . h($M['tema']) . '"><link rel="icon" href="/img/icono.svg" type="image/svg+xml">'
        . '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="' . h($M['fuentes']) . '">'
        . '<link rel="stylesheet" href="/purofiltro-marcas.css"><script src="/carrito.js" defer></script>'
        . verificacion_html() . analytics_html() . $extra . '</head><body class="m-' . h($M['clase']) . '">' . gtm_body_html()
        . '<div class="m-anuncio"><span>✔ Filtros ' . h($M['nombre']) . ' 100 % originales</span><span>🚚 Envío gratis a toda Colombia</span><span>🔒 Pago seguro en línea</span></div>'
        . '<header class="m-top"><div class="m-wrap">'
        . '<a class="m-logo" href="' . h($b) . '" aria-label="Filtros ' . h($M['nombre']) . ' originales · ' . h($n) . '"><img src="/img/icono.svg" alt="" width="28" height="28"><span class="m-pf">Puro<b>Filtro</b></span><i aria-hidden="true"></i><span class="m-sello"><b>' . h($M['nombre']) . '</b><small>Filtros originales</small></span></a>'
        . '<nav class="m-nav"><a href="' . h($b) . '#filtros">Filtros</a><a href="' . h($b) . 'cual-es-mi-filtro/" class="m-ancho">¿Cuál es el mío?</a><a href="' . h($b) . 'cambio-e-instalacion/" class="m-ancho">Instalación</a>'
        . '<a class="m-cart" href="/carrito.php" aria-label="Ver carrito"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 4h2l2.2 10.5a1.5 1.5 0 0 0 1.5 1.2h8.6a1.5 1.5 0 0 0 1.5-1.1L21 8H6.2"/><circle cx="9.5" cy="19.5" r="1.4"/><circle cx="17" cy="19.5" r="1.4"/></svg><span data-cart-n hidden></span></a></nav>'
        . '</div></header><main>';
}

function pie_marca(array $M): void
{
    $S = sitio();
    $n = $S['negocio'];
    $b = $M['base'];
    $tel = preg_replace('/\D/', '', (string) (cfg()['whatsapp'] ?? ''));
    $h = '</main><footer class="m-pie"><div class="m-wrap m-pie-top">'
        . '<div><a class="m-logo" href="' . h($b) . '"><img src="/img/icono.svg" alt="" width="28" height="28"><span class="m-pf">Puro<b>Filtro</b></span><i aria-hidden="true"></i><span class="m-sello"><b>' . h($M['nombre']) . '</b><small>Filtros originales</small></span></a>'
        . '<p>Filtros de agua ' . h($M['nombre']) . ' originales para tu nevecón, con envío gratis a toda Colombia y pago seguro en línea.</p>'
        . ($tel ? '<a class="m-pie-wa" href="https://wa.me/57' . substr($tel, -10) . '" target="_blank" rel="noopener">💬 WhatsApp ' . h($n['telefono']) . '</a>' : '')
        . '<span class="m-pie-hora">' . h(ucfirst($n['horario'])) . '</span></div>'
        . '<nav><b>Filtros ' . h($M['nombre']) . '</b>';
    foreach ($M['productos'] as $p) $h .= '<a href="' . h($b . $p[1]) . '/">' . h($p[0]) . '</a>';
    $h .= '</nav><nav><b>Ayuda</b><a href="' . h($b) . 'cual-es-mi-filtro/">¿Cuál filtro es el mío?</a><a href="' . h($b) . 'cambio-e-instalacion/">Cuándo cambiarlo y cómo instalarlo</a><a href="' . h($b) . '#preguntas">Preguntas frecuentes</a><a href="/carrito.php">Mi carrito</a></nav>'
        . '<nav><b>Compra segura</b><a href="/terminos.php">Términos y condiciones</a><a href="/privacidad.php">Tratamiento de datos</a><a href="/garantia-y-retracto.php">Garantía y retracto</a><a href="/quienes-somos.php">Quiénes somos</a></nav>'
        . '</div><div class="m-wrap m-pie-medios"><span>🔒 Pagos procesados en página segura</span>' . medios_pago_html() . '</div>'
        . '<div class="m-wrap m-pie-base"><span>© ' . date('Y') . ' ' . h($n['nombre']) . '. Precios en pesos colombianos con envío incluido.</span>'
        . '<span>' . h($M['nombre']) . ' es una marca registrada de su dueño. ' . h($n['nombre']) . ' es un comercio independiente que vende filtros ' . h($M['nombre']) . ' originales; no somos la tienda oficial de la marca.</span></div></footer>';
    echo $h . whatsapp_html() . '</body></html>';
}
