<?php
declare(strict_types=1);
// Aviso automático de Wompi (URL de eventos). Wompi llama aquí cada vez que cambia un pago.
require __DIR__ . '/lib.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') fail('Método no permitido.', 405);
$raw = file_get_contents('php://input', false, null, 0, 100001);
$e = json_decode((string) $raw, true);
if (!is_array($e) || !is_array($e['data'] ?? null) || !is_array($e['signature']['properties'] ?? null)) fail('Evento no válido.');

// Verificación: SHA-256 de los valores de "properties" + timestamp + secreto de eventos
$cadena = '';
foreach ($e['signature']['properties'] as $prop) $cadena .= valor_ruta($e['data'], (string) $prop);
$calc = hash('sha256', $cadena . ($e['timestamp'] ?? '') . cfg()['wompi']['eventos']);
$recibido = strtolower((string) ($e['signature']['checksum'] ?? ($_SERVER['HTTP_X_EVENT_CHECKSUM'] ?? '')));
$bitacora = fn(string $res) => db()->prepare('INSERT INTO eventos_wompi (recibido, evento, ref, estado, resultado) VALUES (?,?,?,?,?)')
    ->execute([date('c'), (string) ($e['event'] ?? ''), (string) ($e['data']['transaction']['reference'] ?? ''), (string) ($e['data']['transaction']['status'] ?? ''), $res]);
if (!hash_equals($calc, $recibido)) { $bitacora('firma no válida'); fail('Firma no válida.', 401); }
// Un aviso viejo (más de 2 días) no puede cambiar un pedido: evita que repitan un aviso antiguo
if (abs(time() - (int) ($e['timestamp'] ?? 0)) > 172800) { $bitacora('aviso vencido'); fail('Aviso vencido.', 400); }

if (($e['event'] ?? '') === 'transaction.updated' && is_array($e['data']['transaction'] ?? null)) {
    $p = aplicar_transaccion($e['data']['transaction']);
    $bitacora($p ? 'pedido ' . $p['ref'] . ' → ' . $p['estado'] : 'pedido no encontrado');
} else {
    $bitacora('ignorado');
}
out(['ok' => true]);
