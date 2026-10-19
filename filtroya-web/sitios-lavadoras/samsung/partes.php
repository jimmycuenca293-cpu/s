<?php
declare(strict_types=1);
// Encabezado y pie de las páginas de producto, marca, legales y de pago.
require_once __DIR__ . '/api/sitio.php';

// En los sitios de una sola marca (marca.json existe) el encabezado y el pie son los de la marca
function marca_sitio(): ?array
{
    static $m = false;
    if ($m === false) {
        $f = __DIR__ . '/marca.json';
        $m = is_file($f) ? json_decode((string) file_get_contents($f), true) : null;
        if ($m) require_once __DIR__ . '/marcas.php';
    }
    return $m ?: null;
}

function cabeza(string $titulo, string $desc, string $ruta, string $extra = '', bool $indexar = true): void
{
    if ($M = marca_sitio()) {
        cabeza_marca($M, $titulo, $desc, $ruta, $extra, $indexar, true);
        return;
    }
    $S = sitio();
    $canon = $S['base'] . $ruta;
    $n = $S['negocio'];
    echo '<!doctype html><html lang="es-CO"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        . '<title>' . h($titulo) . '</title><meta name="description" content="' . h($desc) . '">'
        . ($indexar ? '<link rel="canonical" href="' . h($canon) . '">' : '<meta name="robots" content="noindex">')
        . '<meta property="og:type" content="website"><meta property="og:title" content="' . h($titulo) . '"><meta property="og:description" content="' . h($desc) . '"><meta property="og:url" content="' . h($canon) . '"><meta property="og:locale" content="es_CO"><meta property="og:site_name" content="' . h($n['nombre']) . '"><meta name="twitter:card" content="summary_large_image">'
        . (str_contains($extra, 'og:image') ? '' : '<meta property="og:image" content="' . h($S['base']) . '/img/compartir.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">')
        . '<link rel="manifest" href="/manifest.webmanifest"><link rel="apple-touch-icon" href="/img/apple-touch-icon.png">'
        . '<script src="/carrito.js" defer></script><meta name="theme-color" content="#0b1f6b"><link rel="icon" href="/img/icono.svg" type="image/svg+xml"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Manrope:wght@400;500;600;700;800&display=swap"><link rel="stylesheet" href="/estilo.css">' . verificacion_html() . analytics_html() . $extra . '</head><body>' . gtm_body_html()
        . anuncio_html()
        . '<header class="top"><div class="wrap"><a class="logo" href="/"><img src="/img/icono.svg" alt="" width="34" height="34"><span class="lg-t">Filtros<b>Lavadoras</b><small>Colombia</small></span></a>'
        . '<nav class="topnav"><a href="/tienda/">Tienda</a><span class="marcas-nav solo-ancho"><a href="/marca/samsung/">Samsung</a><a href="/marca/lg/">LG</a><a href="/marca/whirlpool/">Whirlpool</a><a href="/marca/ge/">GE</a></span><a href="/instalacion/" class="solo-ancho">Instalación</a><a href="/guia/">Guías</a>'
        . '<a class="cartbtn" href="/carrito.php" aria-label="Ver carrito"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 4h2l2.2 10.5a1.5 1.5 0 0 0 1.5 1.2h8.6a1.5 1.5 0 0 0 1.5-1.1L21 8H6.2"/><circle cx="9.5" cy="19.5" r="1.4"/><circle cx="17" cy="19.5" r="1.4"/></svg><span data-cart-n hidden></span></a></nav>'
        . '</div></header><main class="wrap">';
}

// Barra superior con los beneficios (la usan todas las páginas, también la de inicio)
function anuncio_html(): string
{
    return '<div class="anuncio"><span>🚚 Envío gratis a toda Colombia</span><span>🔒 Pago seguro en línea</span><span>💬 Asesoría por WhatsApp</span></div>';
}

// Pie de página (también lo usa la página de inicio)
function pie_html(): string
{
    $S = sitio();
    $n = $S['negocio'];
    $tel = preg_replace('/\D/', '', (string) (cfg()['whatsapp'] ?? ''));
    $h = '<footer class="pie"><div class="wrap pie-top">'
        . '<div class="pie-marca"><a class="logo" href="/"><img src="/img/icono.svg" alt="" width="34" height="34"><span class="lg-t">Filtros<b>Lavadoras</b><small>Colombia</small></span></a>'
        . '<p>Filtros de pelusas para lavadoras Samsung, LG, Whirlpool, GE, KitchenAid, Maytag, Jenn-Air, Amana, Kenmore y más marcas. Te ayudamos a encontrar el tuyo y te llega a la puerta de tu casa en toda Colombia.</p>'
        . ($tel ? '<a class="pie-wa" href="https://wa.me/57' . substr($tel, -10) . '" target="_blank" rel="noopener">💬 WhatsApp ' . h($n['telefono']) . '</a>' : '')
        . '<span class="pie-hora">' . h(ucfirst($n['horario'])) . '</span></div>'
        . '<nav><b>Filtros</b>';
    foreach (catalogo()['marcas'] as $m) $h .= '<a href="/marca/' . h($m['slug']) . '/">Filtros ' . h($m['nombre']) . '</a>';
    $h .= '<a href="/tienda/">Ver toda la tienda</a></nav>'
        . '<nav><b>Ayuda</b><a href="/referencias/">Buscar por referencia</a><a href="/lavadoras/">Filtro por modelo de lavadora</a><a href="/guia/cada-cuanto-cambiar-el-filtro-del-lavadora/">Cuándo cambiar el filtro</a><a href="/instalacion/">Cómo instalar tu filtro</a><a href="/guia/">Guías</a><a href="/envios/">Envíos a toda Colombia</a></nav>'
        . '<nav><b>Marcas y blog</b>' . implode('', array_map(fn($c) => '<a href="' . h($c['ruta']) . '">' . h($c['titulo']) . '</a>', catalogo()['compat'] ?? [])) . '</nav>'
        . '<nav><b>Empresa</b><a href="/quienes-somos.php">Quiénes somos</a><a href="/contacto.php">Contacto</a><a href="/terminos.php">Términos y condiciones</a><a href="/privacidad.php">Tratamiento de datos</a><a href="/garantia-y-retracto.php">Garantía y retracto</a><a href="/politica-de-envios.php">Política de envíos</a></nav>'
        . '</div><div class="wrap pie-medios"><span class="pie-seguro">🔒 Pagos procesados en página segura</span>' . medios_pago_html() . '</div>'
        . '<div class="wrap pie-base"><span>© ' . date('Y') . ' ' . h($n['nombre']) . '. Precios en pesos colombianos con envío incluido.</span><span>Las marcas mencionadas pertenecen a sus dueños y se usan solo para indicar para qué lavadoras sirve cada filtro; somos un comercio independiente. Autoridad de protección al consumidor: <a href="https://www.sic.gov.co/" target="_blank" rel="noopener">Superintendencia de Industria y Comercio</a>.</span></div></footer>';
    return $h;
}

function pie(): void
{
    if ($M = marca_sitio()) {
        echo '</main>';
        pie_marca($M);
        return;
    }
    echo '</main>' . pie_html() . whatsapp_html() . '</body></html>';
}
