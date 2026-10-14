<?php
declare(strict_types=1);
require __DIR__ . '/lib.php';

$u = require_user();
$uid = (int) $u['id'];
$metodo = $_SERVER['REQUEST_METHOD'];

if ($metodo === 'GET') {
    $st = db()->prepare('SELECT datos FROM visitas WHERE usuario_id = ? ORDER BY id DESC LIMIT 300');
    $st->execute([$uid]);
    $lista = [];
    foreach ($st->fetchAll() as $r) {
        $v = json_decode($r['datos'], true);
        if (is_array($v)) {
            $lista[] = $v;
        }
    }
    out($lista);
}

require_write();

if ($metodo === 'POST') {
    $v = body()['visita'] ?? null;
    if (!is_array($v) || !isset($v['id']) || !is_numeric($v['id']) || (int) $v['id'] <= 0) {
        fail('Visita no válida.');
    }
    $id = (int) $v['id'];
    $json = json_encode($v, JSON_UNESCAPED_UNICODE);
    if ($json === false || strlen($json) > 2 * 1024 * 1024) {
        fail('La visita es demasiado grande.', 413, 'too_large');
    }
    $st = db()->prepare('UPDATE visitas SET datos = ?, actualizado = ? WHERE usuario_id = ? AND id = ?');
    $st->execute([$json, now(), $uid, $id]);
    if ($st->rowCount() === 0) {
        db()->prepare('INSERT INTO visitas (usuario_id, id, datos, actualizado) VALUES (?, ?, ?, ?)')->execute([$uid, $id, $json, now()]);
    }
    out(['ok' => true]);
}

if ($metodo === 'DELETE') {
    if (!empty($_GET['todo'])) {
        db()->prepare('DELETE FROM visitas WHERE usuario_id = ?')->execute([$uid]);
        out(['ok' => true]);
    }
    $id = (int) ($_GET['id'] ?? 0);
    if ($id <= 0) {
        fail('Falta el id.');
    }
    db()->prepare('DELETE FROM visitas WHERE usuario_id = ? AND id = ?')->execute([$uid, $id]);
    out(['ok' => true]);
}

fail('Método no permitido.', 405);
