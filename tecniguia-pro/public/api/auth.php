<?php
declare(strict_types=1);
require __DIR__ . '/lib.php';

$a = $_GET['a'] ?? '';

switch ($a) {
    case 'yo':
        $u = current_user();
        if (!$u) {
            out(['usuario' => null, 'cfg' => cfg_publica()], 401);
        }
        out(['usuario' => public_user($u), 'cfg' => cfg_publica()]);

    case 'registro':
        require_write();
        $b = body();
        $nombre = trim((string) ($b['nombre'] ?? ''));
        $email = strtolower(trim((string) ($b['email'] ?? '')));
        $tel = trim((string) ($b['telefono'] ?? ''));
        $clave = (string) ($b['clave'] ?? '');
        if (mb_strlen($nombre) < 2 || mb_strlen($nombre) > 120) {
            fail('Escribe tu nombre.');
        }
        if (!filter_var($email, FILTER_VALIDATE_EMAIL) || strlen($email) > 190) {
            fail('Escribe un correo válido.');
        }
        if (strlen($clave) < 8) {
            fail('La contraseña debe tener mínimo 8 caracteres.');
        }
        if (!registro_abierto()) {
            fail('Esta app es personal y ya tiene su cuenta. Entra con tu correo y contraseña.', 403, 'closed');
        }
        if (empty($b['acepto']) && !modo_personal()) {
            fail('Debes aceptar los términos de uso.');
        }
        $st = db()->prepare('SELECT id FROM usuarios WHERE email = ?');
        $st->execute([$email]);
        if ($st->fetch()) {
            fail('Ya existe una cuenta con ese correo. Entra con tu contraseña.', 409, 'exists');
        }
        $vence = date('Y-m-d H:i:s', time() + DIAS_PRUEBA * 86400);
        $st = db()->prepare('INSERT INTO usuarios (email, nombre, telefono, clave_hash, estado, vence, creado, ultimo_acceso) VALUES (?, ?, ?, ?, ?, ?, ?, ?)');
        $st->execute([$email, $nombre, mb_substr($tel, 0, 40), password_hash($clave, PASSWORD_DEFAULT), 'prueba', $vence, now(), now()]);
        $id = (int) db()->lastInsertId();
        start_session();
        session_regenerate_id(true);
        $_SESSION['uid'] = $id;
        out(['usuario' => public_user(current_user()), 'cfg' => cfg_publica()]);

    case 'login':
        require_write();
        $b = body();
        $email = strtolower(trim((string) ($b['email'] ?? '')));
        $clave = (string) ($b['clave'] ?? '');
        $ip = client_ip();
        $desde = date('Y-m-d H:i:s', time() - 15 * 60);
        $st = db()->prepare('SELECT COUNT(*) FROM intentos WHERE (ip = ? OR email = ?) AND momento > ?');
        $st->execute([$ip, $email, $desde]);
        if ((int) $st->fetchColumn() >= 10) {
            fail('Demasiados intentos. Espera 15 minutos.', 429, 'rate_limited');
        }
        $st = db()->prepare('SELECT * FROM usuarios WHERE email = ?');
        $st->execute([$email]);
        $u = $st->fetch();
        if (!$u || !password_verify($clave, $u['clave_hash'])) {
            db()->prepare('INSERT INTO intentos (ip, email, momento) VALUES (?, ?, ?)')->execute([$ip, $email, now()]);
            fail('Correo o contraseña incorrectos.', 401, 'auth');
        }
        if (password_needs_rehash($u['clave_hash'], PASSWORD_DEFAULT)) {
            db()->prepare('UPDATE usuarios SET clave_hash = ? WHERE id = ?')->execute([password_hash($clave, PASSWORD_DEFAULT), $u['id']]);
        }
        db()->prepare('UPDATE usuarios SET ultimo_acceso = ? WHERE id = ?')->execute([now(), $u['id']]);
        start_session();
        session_regenerate_id(true);
        $_SESSION['uid'] = (int) $u['id'];
        out(['usuario' => public_user($u), 'cfg' => cfg_publica()]);

    case 'salir':
        require_write();
        start_session();
        $_SESSION = [];
        session_destroy();
        setcookie('tgsid', '', ['expires' => time() - 3600, 'path' => '/']);
        out(['ok' => true]);

    case 'clave':
        require_write();
        $u = require_user();
        $b = body();
        if (!password_verify((string) ($b['actual'] ?? ''), $u['clave_hash'])) {
            fail('La contraseña actual no es correcta.', 400);
        }
        $nueva = (string) ($b['nueva'] ?? '');
        if (strlen($nueva) < 8) {
            fail('La contraseña nueva debe tener mínimo 8 caracteres.');
        }
        db()->prepare('UPDATE usuarios SET clave_hash = ? WHERE id = ?')->execute([password_hash($nueva, PASSWORD_DEFAULT), $u['id']]);
        out(['ok' => true]);

    default:
        fail('Acción no válida.', 404);
}
