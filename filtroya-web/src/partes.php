<?php
declare(strict_types=1);
// Encabezado y pie de las páginas de producto, marca, legales y de pago.
require_once __DIR__ . '/api/sitio.php';

// En los sitios de una sola marca (filtrosnevecones-marca.json existe) el encabezado y el pie son los de la marca
function marca_sitio(): ?array
{
    static $m = false;
    if ($m === false) {
        $f = __DIR__ . '/filtrosnevecones-marca.json';
        $m = is_file($f) ? json_decode((string) file_get_contents($f), true) : null;
        if ($m) require_once __DIR__ . '/filtrosnevecones-marcas.php';
    }
    return $m ?: null;
}

// Google corta los títulos a ~60 caracteres y las descripciones a ~155: se ajustan en la palabra o frase completa
function seo_titulo(string $t): string
{
    while (mb_strlen($t) > 62 && str_contains($t, ' | ')) $t = mb_substr($t, 0, mb_strrpos($t, ' | '));
    if (mb_strlen($t) > 66) { $t = mb_substr($t, 0, 64); $t = preg_replace('/[\s,:;·|-]+\S*$/u', '', $t); }
    return $t;
}
function seo_desc(string $d): string
{
    if (mb_strlen($d) <= 158) return $d;
    $c = mb_substr($d, 0, 158);
    if (preg_match('/^(.{90,}[.!?])\s/us', $c . ' ', $m)) return $m[1];
    return rtrim(preg_replace('/[\s,;:·-]+\S*$/u', '', $c), ' ,;:.') . '.';
}

function cabeza(string $titulo, string $desc, string $ruta, string $extra = '', bool $indexar = true): void
{
    $titulo = seo_titulo($titulo);
    $desc = seo_desc($desc);
    if ($M = marca_sitio()) {
        cabeza_marca($M, $titulo, $desc, $ruta, $extra, $indexar, true);
        return;
    }
    $S = sitio();
    $canon = $S['base'] . $ruta;
    $n = $S['negocio'];
    echo '<!doctype html><html lang="es-CO"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        . '<title>' . h($titulo) . '</title><meta name="description" content="' . h($desc) . '">'
        . ($indexar ? '<link rel="canonical" href="' . h($canon) . '"><meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"><link rel="alternate" hreflang="es-CO" href="' . h($canon) . '"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="' . h($titulo) . '"><meta name="twitter:description" content="' . h($desc) . '"><meta name="geo.region" content="CO"><meta name="geo.placename" content="Colombia">' : '<meta name="robots" content="noindex">')
        . '<meta property="og:type" content="website"><meta property="og:title" content="' . h($titulo) . '"><meta property="og:description" content="' . h($desc) . '"><meta property="og:url" content="' . h($canon) . '"><meta property="og:locale" content="es_CO"><meta property="og:site_name" content="' . h($n['nombre']) . '">'
        . (str_contains($extra, 'og:image') ? '' : '<meta property="og:image" content="' . h($S['base']) . '/img/compartir.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">')
        . '<link rel="manifest" href="/manifest.webmanifest"><link rel="apple-touch-icon" href="/img/apple-touch-icon.png">'
        . '<script src="/carrito.js" defer></script><script src="/filtrosnevecones-asistente.js" defer></script><meta name="theme-color" content="#0b1f6b"><link rel="icon" href="/img/icono.svg" type="image/svg+xml"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Manrope:wght@400;500;600;700;800&display=swap"><link rel="stylesheet" href="/estilo.css">' . verificacion_html() . analytics_html() . $extra . '</head><body>' . gtm_body_html()
        . cabecera_tienda() . '<main class="wrap">';
}

// Cabecera de la tienda (estilo gran almacén): franja de promoción, una sola fila con logo, menú de marcas, enlaces, WhatsApp y carrito
function cabecera_tienda(): string
{
    $n = sitio()['negocio'];
    $tel = preg_replace('/\D/', '', (string) (cfg()['whatsapp'] ?? ''));
    $cat = catalogo();
    $slug = [];
    foreach ($cat['marcas'] as $m) $slug[$m['nombre']] = $m['slug'];
    $mega = '';
    foreach ($slug as $nombre => $s) {
        $mega .= '<div><a class="fx-mh" href="/' . h($s) . '/">Filtros ' . h($nombre) . '</a>';
        foreach ($cat['productos'] as $p) if ($p['marca'] === $nombre) $mega .= '<a href="/' . h($s) . '/' . h($p['slug']) . '/">' . h($p['ref']) . ' <small>' . h(cop((int) $p['precio'])) . '</small></a>';
        $mega .= '</div>';
    }
    $marcas = '';
    foreach ($slug as $nombre => $s) $marcas .= '<a href="/' . h($s) . '/">' . h($nombre) . '</a>';
    return '<div class="fx-util"><div class="fx-wrap"><span>Envío gratis a toda Colombia · Pago seguro con tarjeta, PSE y Nequi</span><nav aria-label="Ayuda"><a href="/envios/">Envíos</a><a href="/guia/">Guías</a><a href="/contacto.php">Contacto</a></nav></div></div>'
        . '<header class="fx-head"><div class="fx-wrap fx-head-in"><a class="fx-logo" href="/" aria-label="FiltrosNevecones, inicio"><img src="/img/icono.svg" alt="" width="40" height="40"><span>filtros<b>nevecones</b><small>.com</small></span></a>'
        . '<details class="fx-todas"><summary>Marcas y filtros</summary><div class="fx-mega">' . $mega . '</div></details>'
        . '<nav class="fx-menu" aria-label="Principal">' . $marcas . '<a href="/tienda/">Todos los filtros</a><a href="/instalacion/">Instalación</a><a href="/guia/">Guías</a></nav>'
        . ($tel ? '<a class="fx-wa" href="https://wa.me/57' . substr($tel, -10) . '" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3a9 9 0 0 0-7.7 13.6L3 21l4.5-1.2A9 9 0 1 0 12 3z"/></svg><span>' . h($n['telefono']) . '</span></a>' : '')
        . '<a class="fx-carro" href="/carrito.php" aria-label="Ver carrito"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 4h2l2.2 10.5a1.5 1.5 0 0 0 1.5 1.2h8.6a1.5 1.5 0 0 0 1.5-1.1L21 8H6.2"/><circle cx="9.5" cy="19.5" r="1.4"/><circle cx="17" cy="19.5" r="1.4"/></svg><b>Carrito</b><span data-cart-n hidden></span></a></div></header>';
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
    $h = '<footer class="fx-pie"><div class="fx-wrap fx-pie-top">'
        . '<div class="fx-pie-m"><a class="fx-logo" href="/"><img src="/img/icono.svg" alt="" width="40" height="40"><span>filtros<b>nevecones</b><small>.com</small></span></a>'
        . '<p>Filtros de agua para nevera Samsung, LG, Whirlpool, GE, KitchenAid, Maytag, Jenn-Air, Amana y Kenmore, con envío gratis a toda Colombia.</p>'
        . ($tel ? '<a class="fx-pie-wa" href="https://wa.me/57' . substr($tel, -10) . '" target="_blank" rel="noopener">WhatsApp ' . h($n['telefono']) . '</a>' : '')
        . '<span class="fx-pie-h">' . h(ucfirst($n['horario'])) . '</span></div>'
        . '<nav><b>Marcas</b>';
    foreach (catalogo()['marcas'] as $m) $h .= '<a href="/' . h($m['slug']) . '/">Filtros ' . h($m['nombre']) . '</a>';
    $h .= '<a href="/tienda/">Toda la tienda</a></nav>'
        . '<nav><b>Ayuda</b><a href="/referencias/">Buscar por referencia</a><a href="/neveras/">Filtro por modelo de nevera</a><a href="/guia/cada-cuanto-cambiar-el-filtro-del-nevecon/">Cuándo cambiar el filtro</a><a href="/instalacion/">Cómo instalar</a><a href="/guia/">Guías</a><a href="/envios/">Envíos</a></nav>'
        . '<nav><b>Empresa</b><a href="/quienes-somos.php">Quiénes somos</a><a href="/contacto.php">Contacto</a><a href="/terminos.php">Términos y condiciones</a><a href="/privacidad.php">Tratamiento de datos</a><a href="/garantia-y-retracto.php">Garantía y retracto</a><a href="/politica-de-envios.php">Política de envíos</a></nav>'
        . '</div><div class="fx-wrap fx-pie-pago"><span>Pagos en página segura</span>' . medios_pago_html() . '</div>'
        . '<div class="fx-wrap fx-pie-base"><span>© ' . date('Y') . ' ' . h($n['nombre']) . '. Precios en pesos colombianos con envío incluido.</span><span>Las marcas mencionadas pertenecen a sus dueños y se usan solo para indicar para qué neveras sirve cada filtro. Somos un comercio independiente. <a href="https://www.sic.gov.co/" target="_blank" rel="noopener">Superintendencia de Industria y Comercio</a>.</span></div></footer>';
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
