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
if (!hash_equals($calc, $recibido)) fail('Firma no válida.', 401);

if (($e['event'] ?? '') === 'transaction.updated' && is_array($e['data']['transaction'] ?? null)) {
    aplicar_transaccion($e['data']['transaction']);
}
out(['ok' => true]);
