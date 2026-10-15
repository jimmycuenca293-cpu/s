<?php
declare(strict_types=1);
// Crea el pedido con el precio del servidor y devuelve el enlace al pago seguro de Wompi.
require __DIR__ . '/lib.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') fail('Método no permitido.', 405);
$raw = file_get_contents('php://input', false, null, 0, 20001);
if ($raw === false || strlen($raw) > 20000) fail('Petición no válida.');
$b = json_decode($raw, true);
if (!is_array($b)) fail('Petición no válida.');

$cat = catalogo();
// Carrito: varias líneas. (Compatibilidad: un solo producto con pid/cantidad/pack.)
$items = is_array($b['items'] ?? null) ? $b['items']
    : [['pid' => $b['pid'] ?? '', 'pack' => !empty($b['pack']), 'cant' => !empty($b['pack']) ? 1 : (int) ($b['cantidad'] ?? 1)]];
$C = calcular_items($items);
if (!$C['lineas']) fail('Tu carrito está vacío o los productos ya no están disponibles. Recarga la página.');
$total = $C['total'];
// Si el cliente tenía la página abierta con un precio viejo, se le avisa en vez de cobrar otro valor
if ((int) ($b['total'] ?? -1) !== $total) fail('El precio se actualizó. Recarga la página para ver el valor correcto.', 409);

// Sin llaves de Wompi en config.php se usa el link de pago fijo del producto (vale 1 unidad)
$w = cfg()['wompi'];
$con_llaves = str_starts_with($w['public_key'], 'pub_') && !str_contains($w['public_key'], 'XXXX') && $w['integridad'] !== '' && !str_contains($w['integridad'], 'XXXX');
$link = '';
if (!$con_llaves) {
    $l0 = $C['lineas'][0];
    $link = (count($C['lineas']) === 1 && $C['unidades'] === 1) ? (string) ($cat['productos'][$l0['pid']]['link_pago'] ?? '') : '';
    if ($link === '') fail(count($C['lineas']) === 1 && $C['unidades'] === 1 && empty($cat['productos'][$l0['pid']]['link_pago'])
        ? 'Este filtro todavía no tiene pago en línea. Escríbenos a ' . cfg()['negocio']['correo'] . ' y te lo vendemos.'
        : 'Por ahora el pago en línea es de un filtro a la vez. Deja una sola unidad en el carrito.');
}

$c = is_array($b['cliente'] ?? null) ? $b['cliente'] : [];
$t = fn(string $k, int $max = 160) => mb_substr(trim((string) ($c[$k] ?? '')), 0, $max);
$cli = ['nombre' => $t('nombre', 80), 'email' => $t('email', 120), 'tel' => preg_replace('/\D/', '', $t('tel', 20)), 'ciudad' => $t('ciudad', 60),
    'barrio' => $t('barrio', 80), 'dir' => $t('dir', 160), 'indicaciones' => $t('indicaciones', 200), 'modelo' => $t('modelo', 40)];
if (strlen($cli['tel']) === 12 && str_starts_with($cli['tel'], '57')) $cli['tel'] = substr($cli['tel'], 2);
if (mb_strlen($cli['nombre']) < 3) fail('Escribe tu nombre.');
if (!filter_var($cli['email'], FILTER_VALIDATE_EMAIL)) fail('Escribe un correo válido.');
if (!preg_match('/^3\d{9}$/', $cli['tel'])) fail('Escribe un celular válido (10 dígitos que empiezan por 3).');
if (!in_array($cli['ciudad'], $cat['ciudades'], true)) fail('Escoge tu ciudad.');
if ($cli['barrio'] === '' || mb_strlen($cli['dir']) < 5) fail('Escribe el barrio y la dirección.');
$entrega = (string) ($b['entrega'] ?? '');
$ok = $cli['ciudad'] === 'Cali' ? ['instalacion', 'domicilio'] : ['transportadora'];
if (!in_array($entrega, $ok, true)) $entrega = $ok[0];

$ip = $_SERVER['REMOTE_ADDR'] ?? '';
// Freno simple contra abusos: máximo 15 pedidos sin pagar por hora desde la misma conexión
$st = db()->prepare("SELECT COUNT(*) FROM pedidos WHERE ip = ? AND estado = 'pendiente' AND creado > ?");
$st->execute([$ip, date('c', time() - 3600)]);
if ((int) $st->fetchColumn() >= 15) fail('Demasiados intentos. Espera un rato e intenta de nuevo.', 429);

$ref = 'PF-' . date('ymd') . '-' . strtoupper(substr(bin2hex(random_bytes(4)), 0, 6));
db()->prepare('INSERT INTO pedidos (ref, creado, pid, producto, refprod, unidades, pack, total, entrega, ciudad, nombre, email, tel, barrio, dir, indicaciones, modelo, recordar, ip)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)')->execute([
    $ref, date('c'), $C['lineas'][0]['pid'], $C['lineas'][0]['nombre'] . (count($C['lineas']) > 1 ? ' y ' . (count($C['lineas']) - 1) . ' más' : ''),
    implode(', ', array_unique(array_column($C['lineas'], 'ref'))), $C['unidades'], (int) in_array(true, array_column($C['lineas'], 'pack'), true), $total, $entrega,
    $cli['ciudad'], $cli['nombre'], $cli['email'], $cli['tel'], $cli['barrio'], $cli['dir'], $cli['indicaciones'], $cli['modelo'], !empty($c['recordar']) ? 1 : 0, $ip]);
db()->prepare('UPDATE pedidos SET items = ? WHERE ref = ?')->execute([json_encode($C['lineas'], JSON_UNESCAPED_UNICODE), $ref]);

if ($link !== '') {
    // Con link de pago el pedido no se marca solo como pagado: te avisamos para que revises el pago en tu panel de Wompi
    $st = db()->prepare('SELECT * FROM pedidos WHERE ref = ?'); $st->execute([$ref]);
    enviar_correo(cfg()['correo_avisos'], "Nuevo pedido {$ref} — revisa el pago de " . cop($total),
        '<h2 style="margin:0 0 8px">Nuevo pedido con link de pago</h2><p>El cliente fue al link de pago de ' . cop($total) . '. Confirma en tu panel de Wompi que el pago quedó aprobado antes de despachar.</p>'
        . tabla_pedido($st->fetch(), true) . '<p><a href="' . h(base_url()) . '/admin.php">Ver todos los pedidos</a></p>');
    out(['ref' => $ref, 'total' => $total, 'url' => $link]);
}

$centavos = $total * 100;
$q = http_build_query([
    'public-key' => cfg()['wompi']['public_key'], 'currency' => 'COP', 'amount-in-cents' => $centavos, 'reference' => $ref,
    'signature:integrity' => firma_integridad($ref, $centavos), 'redirect-url' => base_url() . '/gracias.php',
    'customer-data:email' => $cli['email'], 'customer-data:full-name' => $cli['nombre'],
    'customer-data:phone-number' => $cli['tel'], 'customer-data:phone-number-prefix' => '+57',
]);
out(['ref' => $ref, 'total' => $total, 'url' => 'https://checkout.wompi.co/p/?' . $q]);
