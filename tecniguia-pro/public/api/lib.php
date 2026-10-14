<?php
declare(strict_types=1);

if (!is_file(__DIR__ . '/config.php')) {
    http_response_code(500);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode(['error' => 'config', 'mensaje' => 'Falta api/config.php. Copia config.sample.php como config.php y llénalo.']);
    exit;
}
require __DIR__ . '/config.php';

function db(): PDO
{
    static $pdo = null;
    if ($pdo === null) {
        $opts = [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC];
        if (str_starts_with(DB_DSN, 'mysql')) {
            // Que UPDATE cuente filas encontradas aunque no cambien (necesario para los upsert)
            $opts[PDO::MYSQL_ATTR_FOUND_ROWS] = true;
        }
        $pdo = new PDO(DB_DSN, DB_USER, DB_PASS, $opts);
    }
    return $pdo;
}

function now(): string
{
    return date('Y-m-d H:i:s');
}

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

/** Cuerpo JSON de la petición. */
function body(): array
{
    $raw = file_get_contents('php://input', false, null, 0, MAX_BODY + 1);
    if ($raw !== false && strlen($raw) > MAX_BODY) {
        fail('La petición es demasiado grande. Envía menos fotos.', 413, 'too_large');
    }
    $j = json_decode($raw ?: '{}', true);
    return is_array($j) ? $j : [];
}

/** Las escrituras exigen la cabecera X-TG: otro sitio no puede enviarla (protección CSRF). */
function require_write(): void
{
    if (($_SERVER['HTTP_X_TG'] ?? '') !== '1') {
        fail('Petición no permitida.', 403, 'forbidden');
    }
}

function start_session(): void
{
    if (session_status() === PHP_SESSION_ACTIVE) {
        return;
    }
    $https = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off')
        || (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https');
    $vida = 60 * 60 * 24 * 30;
    ini_set('session.gc_maxlifetime', (string) $vida);
    ini_set('session.use_strict_mode', '1');
    session_name('tgsid');
    session_set_cookie_params([
        'lifetime' => $vida,
        'path' => '/',
        'secure' => $https,
        'httponly' => true,
        'samesite' => 'Lax',
    ]);
    session_start();
}

function current_user(): ?array
{
    start_session();
    $uid = $_SESSION['uid'] ?? null;
    if (!$uid) {
        return null;
    }
    $st = db()->prepare('SELECT * FROM usuarios WHERE id = ?');
    $st->execute([$uid]);
    $u = $st->fetch();
    return $u ?: null;
}

function require_user(): array
{
    $u = current_user();
    if (!$u) {
        fail('Inicia sesión para continuar.', 401, 'auth');
    }
    return $u;
}

/** Modo personal: una sola cuenta, sin pruebas, pagos ni límites. */
function modo_personal(): bool
{
    return defined('MODO_PERSONAL') && MODO_PERSONAL;
}

/** En modo personal solo se puede crear la primera cuenta. */
function registro_abierto(): bool
{
    if (!modo_personal()) {
        return true;
    }
    return (int) db()->query('SELECT COUNT(*) FROM usuarios')->fetchColumn() === 0;
}

function is_admin(array $u): bool
{
    if (modo_personal()) {
        return true;
    }
    return in_array(strtolower($u['email']), array_map('strtolower', ADMIN_EMAILS), true);
}

/** ¿Puede usar la IA? Admin siempre; los demás con prueba o plan vigente. */
function plan_ok(array $u): bool
{
    if (is_admin($u)) {
        return true;
    }
    return in_array($u['estado'], ['prueba', 'activo'], true) && $u['vence'] && $u['vence'] > now();
}

function public_user(array $u): array
{
    $dias = null;
    if ($u['vence']) {
        $dias = (int) ceil((strtotime($u['vence']) - time()) / 86400);
    }
    return [
        'id' => (int) $u['id'],
        'email' => $u['email'],
        'nombre' => $u['nombre'],
        'estado' => $u['estado'],
        'vence' => $u['vence'],
        'dias_restantes' => $dias,
        'admin' => is_admin($u),
        'plan_ok' => plan_ok($u),
    ];
}

function client_ip(): string
{
    return substr((string) ($_SERVER['REMOTE_ADDR'] ?? '0'), 0, 64);
}

function cfg_publica(): array
{
    return ['nombre_app' => NOMBRE_APP, 'whatsapp' => WHATSAPP_SOPORTE, 'dias_prueba' => DIAS_PRUEBA, 'personal' => modo_personal(), 'registro' => registro_abierto()];
}
