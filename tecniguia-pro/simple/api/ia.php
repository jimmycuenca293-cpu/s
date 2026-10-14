<?php
declare(strict_types=1);
// TecniGuía personal sencilla: puente entre la app y Claude. Sin cuentas ni base de datos.

require __DIR__ . '/clave.php';

function out(mixed $data, int $code = 200): never
{
    http_response_code($code);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store');
    header('X-Content-Type-Options: nosniff');
    echo json_encode($data, JSON_UNESCAPED_UNICODE);
    exit;
}
function fail(string $mensaje, int $code = 400, string $error = 'error'): never
{
    out(['error' => $error, 'mensaje' => $mensaje], $code);
}

$hayClave = str_starts_with(trim((string) ANTHROPIC_API_KEY), 'sk-ant-');
$hayCodigo = trim((string) CODIGO_ACCESO) !== '';

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    out(['ia' => $hayClave, 'codigo' => $hayCodigo]);
}
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    fail('Método no permitido.', 405);
}
if (($_SERVER['HTTP_X_TG'] ?? '') !== '1') {
    fail('Petición no permitida.', 403, 'forbidden');
}
if ($hayCodigo && !hash_equals(trim((string) CODIGO_ACCESO), (string) ($_SERVER['HTTP_X_CODIGO'] ?? ''))) {
    fail('Código de acceso incorrecto.', 401, 'codigo');
}
if (!$hayClave) {
    fail('Falta tu clave de la IA en api/clave.php.', 503, 'sin_clave');
}

// ---------- Entrada ----------
$raw = file_get_contents('php://input', false, null, 0, 40 * 1024 * 1024 + 1);
if ($raw !== false && strlen($raw) > 40 * 1024 * 1024) {
    fail('La petición es demasiado grande. Envía menos fotos.', 413, 'too_large');
}
$b = json_decode($raw ?: '{}', true);
if (!is_array($b)) {
    fail('Petición no válida.');
}
$tier = in_array($b['tier'] ?? '', ['complex', 'default', 'quick'], true) ? $b['tier'] : 'default';
$esfuerzo = ['complex' => 'high', 'default' => 'medium', 'quick' => 'low'][$tier];

$imagenes = [];
foreach (array_slice(is_array($b['images'] ?? null) ? $b['images'] : [], 0, 8) as $img) {
    $tipo = $img['mediaType'] ?? '';
    $data = $img['data'] ?? '';
    if (!in_array($tipo, ['image/jpeg', 'image/png', 'image/webp', 'image/gif'], true) || !is_string($data) || $data === '' || strlen($data) > 8 * 1024 * 1024) {
        fail('Una imagen no es válida.', 400, 'image_rejected');
    }
    $imagenes[] = ['type' => 'image', 'source' => ['type' => 'base64', 'mediaType' => $tipo, 'data' => $data]];
}

$turnos = [];
$input = $b['input'] ?? '';
if (is_string($input)) {
    $turnos[] = ['role' => 'user', 'text' => $input];
} elseif (is_array($input)) {
    foreach ($input as $t) {
        $rol = $t['role'] ?? '';
        $txt = $t['content'] ?? '';
        if (!in_array($rol, ['user', 'assistant'], true) || !is_string($txt) || trim($txt) === '') {
            fail('Conversación no válida.');
        }
        if ($turnos && end($turnos)['role'] === $rol) {
            $turnos[count($turnos) - 1]['text'] .= "\n\n" . $txt;
        } else {
            $turnos[] = ['role' => $rol, 'text' => $txt];
        }
    }
}
if (!$turnos || $turnos[0]['role'] !== 'user' || end($turnos)['role'] !== 'user' || trim(end($turnos)['text']) === '') {
    fail('Conversación no válida.');
}
$mensajes = [];
foreach ($turnos as $i => $t) {
    $texto = [['type' => 'text', 'text' => $t['text']]];
    $mensajes[] = ['role' => $t['role'], 'content' => $i === count($turnos) - 1 ? array_merge($imagenes, $texto) : $texto];
}
$sistema = 'Eres el asistente de TecniGuía, una herramienta para un técnico profesional de neveras, nevecones, lavadoras y secadoras en Colombia. Responde siempre en español.';
if (!empty($b['json'])) {
    $sistema .= ' Tu respuesta la lee un programa: responde SOLO con un valor JSON válido, sin texto antes ni después y sin bloques de código.';
}

// ---------- Llamada a Claude ----------
require __DIR__ . '/vendor/autoload.php';
set_time_limit(300);

$cliente = new Anthropic\Client(
    apiKey: trim((string) ANTHROPIC_API_KEY),
    requestOptions: ['timeout' => 280.0, 'maxRetries' => 1],
);
try {
    $resp = $cliente->beta->messages->create(
        model: 'claude-opus-5-5',
        maxTokens: 16000,
        system: $sistema,
        messages: $mensajes,
        outputConfig: ['effort' => $esfuerzo],
        // Si los filtros de seguridad rechazan una respuesta, el servidor reintenta con otro modelo.
        fallbacks: 'default',
        betas: ['server-side-fallback-2026-07-01'],
    );
} catch (Anthropic\Core\Exceptions\RateLimitException $e) {
    fail('La IA está ocupada. Intenta de nuevo en un minuto.', 503, 'rate_limited');
} catch (Anthropic\Core\Exceptions\AuthenticationException $e) {
    fail('Tu clave de la IA no es válida. Revisa api/clave.php.', 503, 'sin_clave');
} catch (Anthropic\Core\Exceptions\BadRequestException $e) {
    error_log('TecniGuía: petición rechazada: ' . $e->getMessage());
    fail('La IA rechazó la consulta (puede ser una imagen). Intenta sin fotos o con otra.', 400, 'bad_request');
} catch (Anthropic\Core\Exceptions\APIStatusException $e) {
    error_log('TecniGuía: error de la API: ' . $e->getMessage());
    fail('La IA no respondió bien. Revisa tu saldo en console.anthropic.com e intenta de nuevo.', 502, 'upstream');
} catch (Anthropic\Core\Exceptions\APIConnectionException $e) {
    fail('No hubo conexión con la IA. Intenta de nuevo.', 502, 'upstream');
}

if ($resp->stopReason === 'refusal') {
    fail('La IA no pudo responder esa consulta. Cambia la descripción.', 422, 'refused');
}
$texto = '';
foreach ($resp->content as $bloque) {
    if ($bloque->type === 'text') {
        $texto .= $bloque->text;
    }
}
if (trim($texto) === '') {
    fail('La IA no devolvió respuesta. Intenta de nuevo.', 502, 'empty');
}
out(['text' => $texto, 'truncated' => $resp->stopReason === 'max_tokens']);
