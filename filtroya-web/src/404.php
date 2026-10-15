<?php http_response_code(404); require __DIR__ . '/partes.php'; cabeza('Página no encontrada | ' . cfg()['negocio']['nombre'], 'Página no encontrada.', '/404.php', '', false); ?>
<h1>No encontramos esa página</h1>
<p>Puede que el filtro haya cambiado de dirección. Búscalo por su referencia:</p>
<div style="display:flex;gap:8px;flex-wrap:wrap"><a class="btn" href="/#catalogo">Ir a la tienda</a><a class="btn ghost" href="/referencias/">Buscar por referencia</a><a class="btn ghost" href="/neveras/">Buscar por modelo</a></div>
<?php pie(); ?>
