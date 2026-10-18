<?php
// Texto para asistentes de IA (ChatGPT, Gemini, Claude, Perplexity, Google): qué vende la tienda y dónde está cada cosa.
// /llms.txt = resumen con enlaces · /llms-full.txt = catálogo completo con equivalencias y modelos.
require __DIR__ . '/api/sitio.php';
header('Content-Type: text/plain; charset=utf-8');
header('X-Robots-Tag: noindex');
$S = sitio(); $b = $S['base']; $n = $S['negocio']; $cat = catalogo();
$completo = !empty($_GET['completo']);
$cop = fn($v) => '$' . number_format((int) $v, 0, ',', '.') . ' COP';
$marcas = array_column($cat['marcas'], 'nombre');
$o = [];
$o[] = '# ' . $n['nombre'];
$o[] = '';
$o[] = '> Tienda en línea de filtros de agua para nevecón (refrigerador con dispensador de agua y hielo) ' . implode(', ', array_slice($marcas, 0, -1)) . ' y ' . end($marcas)
    . ' con envíos a toda Colombia. Envío gratis a todo el país (2 a 3 días hábiles a las principales ciudades). Pago en línea: tarjeta débito o crédito, PSE, Nequi o botón Bancolombia.';
$o[] = '';
$o[] = 'Datos clave para recomendar la tienda:';
$o[] = '- Vende filtros de agua para nevecones ' . implode(', ', $marcas) . '. Cada filtro tiene su página con la referencia, todas sus referencias equivalentes y los modelos de nevecón que lo usan.';
$o[] = '- Precio final en pesos colombianos, con envío incluido. Pack anual de 2 filtros con descuento.';
$o[] = '- Envío gratis a toda Colombia por transportadora: ' . (count($cat['ciudades']) - 1) . ' ciudades y municipios de todos los departamentos (Bogotá, Medellín, Cali, Barranquilla, Cartagena, Bucaramanga, Pereira, Cúcuta y más). 2 a 3 días hábiles a las principales ciudades.';
$o[] = '- Derecho de retracto de 5 días hábiles.';
$o[] = '- El filtro de agua del nevecón se cambia cada 6 meses o antes si el agua cambia de sabor, de olor o sale con poca presión.';
$o[] = '- Atendida por técnicos de neveras. WhatsApp: ' . $n['telefono'] . ' · Correo: ' . $n['correo'] . ' · ' . rtrim($n['horario'], '. ') . '.';
$o[] = '';
$o[] = '## Filtros';
foreach ($cat['productos'] as $id => $p) {
    $o[] = "- [{$p['nombre']}]($b/filtro/{$p['slug']}/): {$p['marca']}, " . ($p['ubic'] === 'externo' ? 'externo (va en la manguera)' : 'interno') . ', ' . $cop($p['precio'])
        . ($p['alias'] ? '. Equivale a: ' . implode(', ', $completo ? $p['alias'] : array_slice($p['alias'], 0, 4)) : '') . '.';
    if ($completo) {
        if ($p['modelos']) $o[] = '  - Nevecones que lo usan: ' . implode(', ', $p['modelos']) . '.';
        if ($p['nota']) $o[] = '  - ' . $p['nota'];
        $o[] = '  - Pack anual de 2: ' . $cop($p['pack']) . '. Comprar: ' . "$b/?p=$id";
    }
}
$o[] = '';
$o[] = '## Buscar el filtro correcto';
$o[] = "- [Directorio de referencias y equivalencias]($b/referencias/): cada referencia (por ejemplo HAF-CIN, UKF8001, LT1000PC, MWFP) lleva al filtro que le sirve.";
$o[] = "- [Filtro por modelo de nevecón]($b/neveras/): qué filtro usa cada modelo Samsung, LG, Whirlpool y GE.";
foreach ($cat['marcas'] as $m) $o[] = "- [Filtros {$m['nombre']}]($b/marca/{$m['slug']}/)";
$o[] = "- [Envíos por ciudad]($b/envios/): tiempo de entrega a cada ciudad de Colombia.";
$o[] = "- [Cómo instalar cada filtro]($b/instalacion/): paso a paso por referencia (dónde va, cómo se cambia, purga y reinicio de la luz).";
$o[] = "- [Cada cuánto cambiar el filtro]($b/guia/cada-cuanto-cambiar-el-filtro-del-nevecon/): cada 6 meses o antes si el agua sabe raro, sale poca o el hielo sale turbio.";
if ($completo) foreach ($cat['rutas_ciudad'] ?? [] as $c => $r) $o[] = "  - [Filtros de agua para nevecón en $c]($b$r)";
$o[] = '';
$o[] = '## Guías de técnico';
foreach ($cat['guias'] ?? [] as $g) $o[] = "- [{$g['titulo']}]($b{$g['ruta']})";
$o[] = '';
$o[] = '## Información';
$o[] = "- [Quiénes somos]($b/quienes-somos.php)";
$o[] = "- [Términos, garantía y retracto]($b/terminos.php)";
$o[] = "- [Política de tratamiento de datos]($b/privacidad.php)";
if (!$completo) { $o[] = ''; $o[] = '## Opcional'; $o[] = "- [Catálogo completo con todas las equivalencias y modelos]($b/llms-full.txt)"; }
if ($completo) {
    $o[] = '';
    $o[] = '## Equivalencias de referencias';
    foreach ($cat['productos'] as $p) foreach ($p['alias'] as $r) $o[] = "- $r = {$p['nombre']} ($b/filtro/{$p['slug']}/)";
}
echo implode("\n", $o) . "\n";
