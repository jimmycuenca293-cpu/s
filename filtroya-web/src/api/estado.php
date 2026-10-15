<?php
declare(strict_types=1);
// Estado del pago al volver de Wompi (gracias.php). Consulta la transacción en Wompi y actualiza el pedido.
require __DIR__ . '/lib.php';

$id = preg_replace('/[^A-Za-z0-9\-_]/', '', (string) ($_GET['id'] ?? ''));
if ($id === '') fail('Falta el número de la transacción.');
$ch = curl_init(wompi_api() . '/transactions/' . rawurlencode($id));
curl_setopt_array($ch, [CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 15]);
$res = curl_exec($ch);
$code = (int) curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);
$tx = $code === 200 ? (json_decode((string) $res, true)['data'] ?? null) : null;
if (!is_array($tx)) fail('No pudimos consultar el pago. Revisa tu correo en unos minutos.', 502);
$p = aplicar_transaccion($tx);
if (!$p) fail('No encontramos el pedido.', 404);
out(['ref' => $p['ref'], 'estado' => $p['estado'], 'tx' => $tx['status'] ?? '', 'producto' => $p['producto'], 'unidades' => (int) $p['unidades'],
    'total' => (int) $p['total'], 'entrega' => $p['entrega'], 'ciudad' => $p['ciudad'], 'email' => $p['email'], 'pid' => $p['pid'],
    'items' => array_map(fn($l) => ['pid' => $l['pid'], 'texto' => linea_txt($l)], lineas_pedido($p))]);
