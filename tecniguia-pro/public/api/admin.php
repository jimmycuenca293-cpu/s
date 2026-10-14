<?php
declare(strict_types=1);
require __DIR__ . '/lib.php';

$u = require_user();
if (!is_admin($u)) {
    fail('Solo el administrador puede entrar aquí.', 403, 'forbidden');
}

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $desde = date('Y-m-d', time() - 30 * 86400);
    $usuarios = db()->query('SELECT id, email, nombre, telefono, estado, vence, creado, ultimo_acceso FROM usuarios ORDER BY creado DESC')->fetchAll();
    $st = db()->prepare('SELECT usuario_id, SUM(llamadas) AS llamadas, SUM(tokens_entrada) AS tin, SUM(tokens_salida) AS tout FROM uso WHERE dia >= ? GROUP BY usuario_id');
    $st->execute([$desde]);
    $uso = [];
    foreach ($st->fetchAll() as $r) {
        $uso[(int) $r['usuario_id']] = $r;
    }
    $vis = [];
    foreach (db()->query('SELECT usuario_id, COUNT(*) AS n FROM visitas GROUP BY usuario_id')->fetchAll() as $r) {
        $vis[(int) $r['usuario_id']] = (int) $r['n'];
    }
    foreach ($usuarios as &$x) {
        $id = (int) $x['id'];
        $r = $uso[$id] ?? ['llamadas' => 0, 'tin' => 0, 'tout' => 0];
        $x['id'] = $id;
        $x['llamadas_30d'] = (int) $r['llamadas'];
        $x['costo_30d_usd'] = round(((int) $r['tin'] * PRECIO_ENTRADA_USD + (int) $r['tout'] * PRECIO_SALIDA_USD) / 1e6, 2);
        $x['visitas'] = $vis[$id] ?? 0;
        $x['admin'] = is_admin($x);
        $x['plan_ok'] = $x['admin'] || (in_array($x['estado'], ['prueba', 'activo'], true) && $x['vence'] > now());
    }
    out(['usuarios' => $usuarios, 'hoy' => now()]);
}

require_write();
$b = body();
$id = (int) ($b['id'] ?? 0);
$st = db()->prepare('SELECT * FROM usuarios WHERE id = ?');
$st->execute([$id]);
$obj = $st->fetch();
if (!$obj) {
    fail('Ese técnico no existe.', 404);
}

switch ($b['accion'] ?? '') {
    case 'activar':
        $dias = max(1, min(400, (int) ($b['dias'] ?? 30)));
        $base = ($obj['vence'] && $obj['vence'] > now()) ? strtotime($obj['vence']) : time();
        $vence = date('Y-m-d H:i:s', $base + $dias * 86400);
        db()->prepare('UPDATE usuarios SET estado = ?, vence = ? WHERE id = ?')->execute(['activo', $vence, $id]);
        out(['ok' => true, 'vence' => $vence]);

    case 'suspender':
        db()->prepare('UPDATE usuarios SET estado = ? WHERE id = ?')->execute(['suspendido', $id]);
        out(['ok' => true]);

    case 'clave':
        // Contraseña temporal para el técnico que la olvidó (se la das por WhatsApp)
        $abc = 'abcdefghjkmnpqrstuvwxyz23456789';
        $tmp = '';
        for ($i = 0; $i < 10; $i++) {
            $tmp .= $abc[random_int(0, strlen($abc) - 1)];
        }
        db()->prepare('UPDATE usuarios SET clave_hash = ? WHERE id = ?')->execute([password_hash($tmp, PASSWORD_DEFAULT), $id]);
        out(['ok' => true, 'clave' => $tmp]);

    default:
        fail('Acción no válida.');
}
