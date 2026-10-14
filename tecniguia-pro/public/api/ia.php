<?php
declare(strict_types=1);
require __DIR__ . '/lib.php';
require __DIR__ . '/vendor/autoload.php';

use Anthropic\Client;
use Anthropic\Core\Exceptions\APIConnectionException;
use Anthropic\Core\Exceptions\APIStatusException;
use Anthropic\Core\Exceptions\AuthenticationException;
use Anthropic\Core\Exceptions\BadRequestException;
use Anthropic\Core\Exceptions\RateLimitException;

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    fail('Método no permitido.', 405);
}
require_write();
$u = require_user();
if (!plan_ok($u)) {
    $msg = $u['estado'] === 'prueba'
        ? 'Tu prueba gratis terminó. Para seguir usando el diagnóstico, activa tu plan.'
        : 'Tu plan no está activo. Para seguir usando el diagnóstico, actívalo.';
    out(['error' => 'plan', 'mensaje' => $msg, 'whatsapp' => WHATSAPP_SOPORTE], 402);
}
// Cerrar la sesión ya: la llamada a la IA tarda y no debe bloquear otras peticiones del mismo técnico.
session_write_close();

$uid = (int) $u['id'];
$hoy = date('Y-m-d');
$st = db()->prepare('SELECT llamadas FROM uso WHERE usuario_id = ? AND dia = ?');
$st->execute([$uid, $hoy]);
if (!modo_personal() && (int) $st->fetchColumn() >= LIMITE_DIARIO) {
    fail('Llegaste al límite de consultas de hoy. Se reinicia mañana.', 429, 'rate_limited');
}

// ---------- Entrada ----------
$b = body();
$tier = in_array($b['tier'] ?? '', ['complex', 'default', 'quick'], true) ? $b['tier'] : 'default';
$quiereJson = !empty($b['json']);

$imagenes = [];
foreach (array_slice(is_array($b['images'] ?? null) ? $b['images'] : [], 0, 8) as $img) {
    $tipo = $img['mediaType'] ?? '';
    $data = $img['data'] ?? '';
    if (!in_array($tipo, ['image/jpeg', 'image/png', 'image/webp', 'image/gif'], true) || !is_string($data) || $data === '' || strlen($data) > 8 * 1024 * 1024) {
        fail('Una imagen no es válida.', 400, 'image_rejected');
    }
    $imagenes[] = ['type' => 'image', 'source' => ['type' => 'base64', 'mediaType' => $tipo, 'data' => $data]];
}

// input: texto, o lista de turnos {role, content} que empieza y termina en "user"
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
        // Une turnos seguidos del mismo rol
        if ($turnos && end($turnos)['role'] === $rol) {
            $turnos[count($turnos) - 1]['text'] .= "\n\n" . $txt;
        } else {
            $turnos[] = ['role' => $rol, 'text' => $txt];
        }
    }
}
if (!$turnos || $turnos[0]['role'] !== 'user' || end($turnos)['role'] !== 'user') {
    fail('Conversación no válida.');
}
$total = array_sum(array_map(fn ($t) => strlen($t['text']), $turnos));
if ($total === 0 || $total > 300 * 1024) {
    fail('El texto es demasiado largo.', 413, 'too_large');
}

$mensajes = [];
foreach ($turnos as $i => $t) {
    $esUltimo = $i === count($turnos) - 1;
    $contenido = $esUltimo ? array_merge($imagenes, [['type' => 'text', 'text' => $t['text']]]) : [['type' => 'text', 'text' => $t['text']]];
    $mensajes[] = ['role' => $t['role'], 'content' => $contenido];
}

$sistema = 'Eres el asistente de ' . NOMBRE_APP . ', una herramienta para técnicos profesionales de neveras, nevecones, lavadoras y secadoras en Colombia y Latinoamérica. Responde siempre en español.';
if ($quiereJson) {
    $sistema .= ' Tu respuesta la lee un programa: responde SOLO con un valor JSON válido, sin texto antes ni después y sin bloques de código.';
}

// ---------- Llamada a Claude ----------
set_time_limit(300);
$cliente = new Client(
    apiKey: ANTHROPIC_API_KEY,
    baseUrl: ANTHROPIC_BASE_URL ?: null,
    requestOptions: ['timeout' => 280.0, 'maxRetries' => 1],
);

try {
    $resp = $cliente->beta->messages->create(
        model: MODELOS[$tier],
        maxTokens: 16000,
        system: $sistema,
        messages: $mensajes,
        outputConfig: ['effort' => ESFUERZO[$tier]],
        // Si una respuesta se rechaza por los filtros de seguridad, el servidor reintenta con otro modelo.
        fallbacks: 'default',
        betas: ['server-side-fallback-2026-07-01'],
    );
} catch (RateLimitException $e) {
    fail('El servicio de IA está ocupado. Intenta de nuevo en un minuto.', 503, 'rate_limited');
} catch (AuthenticationException $e) {
    error_log('TecniGuía: clave de Anthropic inválida');
    fail('El servicio de IA no está configurado. Avísale al administrador.', 500, 'upstream');
} catch (BadRequestException $e) {
    error_log('TecniGuía: petición rechazada: ' . $e->getMessage());
    fail('El servicio de IA rechazó la consulta (puede ser una imagen). Intenta sin fotos o con otra.', 400, 'bad_request');
} catch (APIStatusException $e) {
    error_log('TecniGuía: error de la API: ' . $e->getMessage());
    fail('El servicio de IA no respondió bien. Intenta de nuevo.', 502, 'upstream');
} catch (APIConnectionException $e) {
    error_log('TecniGuía: sin conexión con la API: ' . $e->getMessage());
    fail('No hubo conexión con el servicio de IA. Intenta de nuevo.', 502, 'upstream');
}

// ---------- Registrar consumo ----------
$tin = (int) $resp->usage->inputTokens + (int) ($resp->usage->cacheReadInputTokens ?? 0) + (int) ($resp->usage->cacheCreationInputTokens ?? 0);
$tout = (int) $resp->usage->outputTokens;
$st = db()->prepare('UPDATE uso SET llamadas = llamadas + 1, tokens_entrada = tokens_entrada + ?, tokens_salida = tokens_salida + ? WHERE usuario_id = ? AND dia = ?');
$st->execute([$tin, $tout, $uid, $hoy]);
if ($st->rowCount() === 0) {
    db()->prepare('INSERT INTO uso (usuario_id, dia, llamadas, tokens_entrada, tokens_salida) VALUES (?, ?, 1, ?, ?)')->execute([$uid, $hoy, $tin, $tout]);
}

if ($resp->stopReason === 'refusal') {
    fail('El asistente no pudo responder esa consulta. Cambia la descripción.', 422, 'refused');
}

$texto = '';
foreach ($resp->content as $bloque) {
    if ($bloque->type === 'text') {
        $texto .= $bloque->text;
    }
}
if (trim($texto) === '') {
    fail('El asistente no devolvió respuesta. Intenta de nuevo.', 502, 'empty');
}
out(['text' => $texto, 'truncated' => $resp->stopReason === 'max_tokens']);
