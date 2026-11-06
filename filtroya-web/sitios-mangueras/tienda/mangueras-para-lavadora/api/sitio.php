<?php
declare(strict_types=1);
// Datos públicos para las páginas (nunca las llaves).
require_once __DIR__ . '/lib.php';
function sitio(): array
{
    $n = cfg()['negocio'];
    return ['base' => base_url(), 'negocio' => $n, 'web' => ['api' => '/api/', 'correo' => $n['correo'], 'negocio' => ['nombre' => $n['nombre'], 'horario' => $n['horario']]]];
}
