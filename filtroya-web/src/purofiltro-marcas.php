<?php
declare(strict_types=1);
// Encabezado y pie de las tiendas exclusivas por marca (Samsung, LG, Whirlpool, GE).
// Cada tienda solo enlaza a sus propias páginas: no se mezclan marcas.
require_once __DIR__ . '/partes.php';

// $legado: páginas comunes (carrito, pago, legales) que usan la hoja de estilo de la tienda principal
function cabeza_marca(array $M, string $titulo, string $desc, string $ruta, string $extra = '', bool $indexar = true, bool $legado = false): void
{
    $S = sitio();
    $canon = $S['base'] . $ruta;
    $b = $M['base'];
    echo '<!doctype html><html lang="es-CO"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        . '<title>' . h($titulo) . '</title><meta name="description" content="' . h($desc) . '">' . ($indexar ? '<link rel="canonical" href="' . h($canon) . '">' : '<meta name="robots" content="noindex">')
        . '<meta property="og:type" content="website"><meta property="og:title" content="' . h($titulo) . '"><meta property="og:description" content="' . h($desc) . '"><meta property="og:url" content="' . h($canon) . '"><meta property="og:locale" content="es_CO"><meta property="og:site_name" content="Filtros ' . h($M['nombre']) . '">'
        . '<meta name="theme-color" content="' . h($M['tema']) . '"><link rel="icon" href="' . h($M['icono'] ?? '/img/icono.svg') . '">'
        . '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="' . h($M['fuentes']) . '">'
        . ($legado ? '<link rel="stylesheet" href="/estilo.css">' : '') . '<link rel="stylesheet" href="/purofiltro-marcas.css"><script src="/carrito.js" defer></script>'
        . verificacion_html() . analytics_html() . $extra . '</head><body class="m-' . h($M['clase']) . ($legado ? ' m-legado' : '') . '">' . gtm_body_html()
        . '<div class="m-anuncio"><span>✔ Distribuidor autorizado ' . h($M['nombre']) . ' en Colombia</span><span>🚚 Envío gratis a toda Colombia</span><span>🔒 Pago seguro en línea</span></div>'
        . '<header class="m-top"><div class="m-wrap">'
        . '<a class="m-logo" href="' . h($b) . '" aria-label="Filtros ' . h($M['nombre']) . ', distribuidor autorizado"><span class="m-sello">' . logo_marca_html($M) . '<small>Distribuidor autorizado</small></span></a>'
        . menu_marca($M)
        . '</div></header><main' . ($legado ? ' class="wrap m-legado-main"' : '') . '>';
}

// Menú del encabezado: desplegables (filtros, guías, ciudades) en computador y menú «hamburguesa» en el celular
function menu_marca(array $M): string
{
    $b = $M['base'];
    $filtros = '';
    foreach ($M['productos'] as $p) $filtros .= '<a href="' . h($b . $p[1]) . '/">' . h($p[0]) . '</a>';
    $guias = '';
    foreach ($M['guias'] ?? [] as $g) $guias .= '<a href="' . h($g[0]) . '">' . h($g[1]) . '</a>';
    $ciudades = '';
    foreach ($M['ciudades'] ?? [] as $c) $ciudades .= '<a href="' . h($c[1]) . '">' . h($c[0]) . '</a>';
    if (!empty($M['hub'])) $ciudades .= '<a class="m-todas" href="' . h($M['hub']) . '">Ver todas las ciudades →</a>';
    $compat = '';
    foreach ($M['compat'] ?? [] as $c) $compat .= '<a href="' . h($c[1]) . '">' . (str_starts_with($c[0], 'Todas') ? '' : 'Neveras ') . h($c[0]) . '</a>';
    $mas = '';
    foreach ($M['extra'] ?? [] as $c) $mas .= '<a href="' . h($c[1]) . '">' . h($c[0]) . '</a>';
    $cart = '<a class="m-cart" href="/carrito.php" aria-label="Ver carrito"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 4h2l2.2 10.5a1.5 1.5 0 0 0 1.5 1.2h8.6a1.5 1.5 0 0 0 1.5-1.1L21 8H6.2"/><circle cx="9.5" cy="19.5" r="1.4"/><circle cx="17" cy="19.5" r="1.4"/></svg><span data-cart-n hidden></span></a>';
    $dd = fn(string $t, string $links) => $links === '' ? '' : '<div class="m-dd"><a href="#" onclick="return false" aria-haspopup="true">' . $t . ' <i aria-hidden="true">▾</i></a><div class="m-panel">' . $links . '</div></div>';
    return '<nav class="m-nav" aria-label="Principal">' . $dd('Filtros', $filtros) . $dd('Guías', $guias) . $dd('Ciudades', $ciudades) . $dd('Marcas', $compat) . $dd('Más', $mas)
        . '<a class="m-ancho" href="' . h($b) . 'cual-es-mi-filtro/">¿Cuál es el mío?</a><a class="m-ancho" href="' . h($b) . 'cambio-e-instalacion/">Instalación</a>' . $cart
        . '<details class="m-burger"><summary aria-label="Abrir el menú"><span></span></summary><div class="m-bmenu">'
        . '<b>Filtros</b>' . $filtros . '<b>Guías</b>' . $guias . '<b>Ciudades</b>' . $ciudades . ($compat ? '<b>Marcas compatibles</b>' . $compat : '') . ($mas ? '<b>Más</b>' . $mas : '')
        . '<b>Ayuda</b><a href="' . h($b) . 'cual-es-mi-filtro/">¿Cuál es el mío?</a><a href="' . h($b) . 'cambio-e-instalacion/">Instalación</a></div></details></nav>';
}

// Logo de la marca (somos distribuidor autorizado); si no hay logo, el nombre en texto
function logo_marca_html(array $M, string $clase = 'm-logo-marca'): string
{
    if (empty($M['logo'])) return '<b>' . h($M['nombre']) . '</b>';
    return '<img class="' . h($clase) . '" src="' . h($M['logo']) . '" alt="' . h($M['nombre']) . '" width="' . (int) $M['logo_w'] . '" height="' . (int) $M['logo_h'] . '">';
}

function pie_marca(array $M): void
{
    $S = sitio();
    $n = $S['negocio'];
    $b = $M['base'];
    $tel = preg_replace('/\D/', '', (string) (cfg()['whatsapp'] ?? ''));
    $h = '<footer class="m-pie"><div class="m-wrap m-pie-top">'
        . '<div><a class="m-logo" href="' . h($b) . '"><span class="m-sello">' . logo_marca_html($M) . '<small>Distribuidor autorizado</small></span></a>'
        . '<p>Distribuidor autorizado de filtros de agua ' . h($M['nombre']) . ' en Colombia, con envío gratis a todo el país y pago seguro en línea.</p>'
        . ($tel ? '<a class="m-pie-wa" href="https://wa.me/57' . substr($tel, -10) . '" target="_blank" rel="noopener">💬 WhatsApp ' . h($n['telefono']) . '</a>' : '')
        . '<span class="m-pie-hora">' . h(ucfirst($n['horario'])) . '</span></div>'
        . '<nav><b>Filtros ' . h($M['nombre']) . '</b>';
    foreach ($M['productos'] as $p) $h .= '<a href="' . h($b . $p[1]) . '/">' . h($p[0]) . '</a>';
    $h .= '</nav><nav><b>Guías</b>';
    foreach ($M['guias'] ?? [] as $g) $h .= '<a href="' . h($g[0]) . '">' . h($g[1]) . '</a>';
    if (!empty($M['compat'])) {
        $h .= '</nav><nav><b>Marcas compatibles</b>';
        foreach ($M['compat'] as $c) $h .= '<a href="' . h($c[1]) . '">' . (str_starts_with($c[0], 'Todas') ? '' : 'Neveras ') . h($c[0]) . '</a>';
        foreach ($M['extra'] ?? [] as $c) $h .= '<a href="' . h($c[1]) . '"><b>' . h($c[0]) . '</b></a>';
    }
    $h .= '</nav><nav><b>Envíos</b>';
    foreach (array_slice($M['ciudades'] ?? [], 0, 8) as $c) $h .= '<a href="' . h($c[1]) . '">Filtros ' . h($M['nombre']) . ' en ' . h($c[0]) . '</a>';
    if (!empty($M['hub'])) $h .= '<a href="' . h($M['hub']) . '"><b>Todas las ciudades →</b></a>';
    $h .= '</nav><nav><b>Ayuda</b><a href="' . h($b) . 'cual-es-mi-filtro/">¿Cuál filtro es el mío?</a><a href="' . h($b) . 'cambio-e-instalacion/">Cuándo cambiarlo y cómo instalarlo</a><a href="' . h($b) . '#preguntas">Preguntas frecuentes</a><a href="/carrito.php">Mi carrito</a>';
    foreach ($M['externos'] ?? [] as $e) $h .= '<a href="' . h($e[1]) . '" target="_blank" rel="noopener">' . h($e[0]) . ' ↗</a>';
    $h .= '</nav>'
        . '<nav><b>Compra segura</b><a href="/terminos.php">Términos y condiciones</a><a href="/privacidad.php">Tratamiento de datos</a><a href="/garantia-y-retracto.php">Garantía y retracto</a><a href="/quienes-somos.php">Quiénes somos</a></nav>'
        . '</div><div class="m-wrap m-pie-medios"><span>🔒 Pagos procesados en página segura</span>' . medios_pago_html() . '</div>'
        . '<div class="m-wrap m-pie-base"><span>© ' . date('Y') . ' ' . h($n['nombre']) . '. Precios en pesos colombianos con envío incluido.</span>'
        . '<span>Distribuidor autorizado de filtros de agua ' . h($M['nombre']) . ' en Colombia. ' . h($M['nombre']) . ' y su logo son marcas registradas de su dueño y se usan con autorización.</span></div></footer>';
    echo $h . whatsapp_html() . '</body></html>';
}
