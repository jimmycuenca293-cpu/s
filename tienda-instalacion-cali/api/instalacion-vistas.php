<?php
declare(strict_types=1);
// Páginas de la tienda de instalación: inicio, una página por combo y la página de reserva (pago).
require_once __DIR__ . '/instalacion-lib.php';
require_once __DIR__ . '/../partes.php';

const INST_V = '20261030a';

function inst_slugs(): array
{
    return ['basica' => 'instalacion-basica-nevecon', 'filtro-samsung' => 'instalacion-nevecon-con-filtro-samsung',
        'filtro-lg' => 'instalacion-nevecon-con-filtro-lg', 'filtro-whirlpool' => 'instalacion-nevecon-con-filtro-whirlpool'];
}

function inst_url_producto(string $id): string
{
    return '/instalacion-nevecon-cali/' . (inst_slugs()[$id] ?? '') . '/';
}

function inst_url_reservar(string $id, string $zona = 'cali', string $forma = 'reserva'): string
{
    return '/instalacion-nevecon-cali/reservar/?s=' . rawurlencode($id) . '&z=' . rawurlencode($zona) . '&f=' . rawurlencode($forma);
}

// Datos públicos que usa el JavaScript de la tienda (nunca claves ni links de pago)
function inst_pub(): array
{
    $C = inst_config();
    $ids = array_keys($C['servicios']); $zs = array_keys($C['zonas']);
    return ['servicios' => array_map(fn($s) => ['nombre' => $s['nombre'], 'corto' => $s['corto'], 'precio' => $s['precio'], 'reserva' => $s['reserva']], $C['servicios']),
        'total_online' => array_map(fn($sid) => array_map(fn($zid) => inst_total_online($sid, $zid)[0], array_combine($zs, $zs)), array_combine($ids, $ids)),
        'zonas' => $C['zonas'], 'metro_extra' => $C['metro_extra'], 'franjas' => count($C['franjas']), 'anticipacion' => $C['anticipacion_horas'],
        'atencion' => [$C['franjas'][0][0], end($C['franjas'])[2]], 'slugs' => array_map(fn($id) => inst_url_producto($id), array_combine($ids, $ids))];
}

function inst_picture(string $id, string $alt, int $w): string
{
    return '<picture><source srcset="/instalacion-nevecon-cali/img/combo-' . $id . '.webp" type="image/webp"><img src="/instalacion-nevecon-cali/img/combo-' . $id . '.jpg" alt="' . h($alt) . '" width="' . $w . '" height="' . $w . '" loading="lazy"></picture>';
}

function inst_foto(string $id, string $alt, int $w = 96): string
{
    return '<picture><source srcset="/filtrosnevecones-img/' . $id . '-400.webp" type="image/webp"><img src="/filtrosnevecones-img/' . $id . '.jpg" alt="' . h($alt) . '" width="' . $w . '" height="' . $w . '" loading="lazy"></picture>';
}

function inst_nb(int $x): string
{
    return str_replace(' ', "\u{00A0}", cop($x));
}

function inst_nombres_zonas(): string
{
    $n = array_column(inst_config()['zonas'], 'nombre');
    return count($n) > 1 ? implode(', ', array_slice($n, 0, -1)) . ' y ' . end($n) : (string) ($n[0] ?? '');
}

function inst_recargos(): string
{
    return implode(' · ', array_map(fn($z) => $z['nombre'] . ' +' . cop((int) $z['recargo']), array_filter(inst_config()['zonas'], fn($z) => $z['recargo'] > 0)));
}

function inst_cabecera(string $titulo, string $desc, string $ruta, array $ld = [], bool $indexar = true): void
{
    $extra = '<link rel="stylesheet" href="/instalacion-nevecon-cali/instalacion.css?v=' . INST_V . '">'
        . ($ld ? '<script type="application/ld+json">' . json_encode($ld, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_HEX_TAG) . '</script>' : '');
    cabeza($titulo, $desc, $ruta, $extra, $indexar);
}

function inst_texto(string $id): array
{
    $C = inst_config(); $s = $C['servicios'][$id]; $f = $s['filtro'];
    $comun = [
        ['Servicio', 'Instalación a domicilio por un técnico de nuestro equipo'],
        ['Zonas', inst_nombres_zonas() . ' (recargo por zona: ' . inst_recargos() . ')'],
        ['Llave', 'Galápago profesional, con racores'],
        ['Manguera', 'De 1/4", hasta 5 metros incluidos (cada 5 m extra: ' . cop($C['metro_extra']) . ')'],
    ];
    $cierre = [['Garantía', '1 año en la instalación'], ['Pago', 'Todo ahora o en 2 partes (el resto, en efectivo al técnico al terminar)'], ['Atención', 'Lunes a sábado, de 8:00 a. m. a 5:00 p. m.']];
    $pasos = ['Escoges tu zona, el día y la hora, y pagas hoy en línea (todo, o una primera parte).', 'Un asesor te escribe por WhatsApp para confirmar tu instalación y darte los datos del técnico.',
        'El técnico llega en tu horario, instala, prueba que no haya fugas y te muestra el agua funcionando.', 'Si pagaste en 2 partes, le pagas el resto en efectivo. Tienes 1 año de garantía.'];
    if (!$f) return [
        'h1' => 'Instalación básica de agua para tu nevecón',
        'resumen' => 'La conexión del agua de tu nevecón: llave galápago profesional, manguera de 1/4" hasta 5 metros, prueba de fugas y purga. Sin filtro.',
        'parrafos' => ['Esta es la instalación base. Un técnico de nuestro equipo va a tu casa, toma el agua de tu punto con una llave galápago profesional, tiende la manguera de 1/4" (hasta 5 metros) hasta el nevecón y la conecta.',
            'Antes de irse revisa que no haya fugas y purga el sistema para que el primer vaso de agua salga limpio. Si tu nevecón tiene dispensador de agua o máquina de hielo, quedan funcionando.'],
        'ideal' => 'Tu nevecón no tiene el agua conectada, te mudaste, o necesitas cambiar una conexión vieja, y no quieres filtro externo (o ya tienes uno). Sirve para nevecones de cualquier marca con dispensador de agua.',
        'incluye' => ['Instalación a domicilio por un técnico de nuestro equipo', 'Llave galápago profesional con racores', 'Manguera de 1/4" hasta 5 metros', 'Conexión al nevecón', 'Prueba de fugas y purga del agua', '1 año de garantía en la instalación'],
        'no_incluye' => ['Filtro externo (lo encuentras en los combos con filtro)', 'Trabajos nuevos de tubería en tu casa; si hacen falta, el técnico te los cotiza antes de empezar', 'Metros extra de manguera (cada 5 m: ' . cop($C['metro_extra']) . ')'],
        'specs' => array_merge($comun, [['Filtro externo', 'No incluye']], $cierre), 'piezas' => [['k-man14-5', 'Manguera 1/4" hasta 5 m'], ['k-galapago', 'Llave galápago profesional']],
        'pasos' => $pasos, 'meta' => 'Instalación básica del agua de tu nevecón a domicilio en Cali y Jamundí: llave galápago y manguera de hasta 5 m. Pagas todo hoy o en 2 partes. 1 año de garantía.',
    ];
    $m = $f['marca']; $r = $f['ref'];
    return [
        'h1' => 'Instalación de agua con filtro externo ' . $m . ' para tu nevecón',
        'resumen' => 'Todo lo de la instalación básica más el filtro externo ' . $m . ' ' . $r . ' instalado en la línea de agua, para que el agua del dispensador y del hielo llegue filtrada.',
        'parrafos' => ['Un técnico de nuestro equipo va a tu casa, instala la llave galápago profesional, tiende la manguera de 1/4" (hasta 5 metros) y conecta el filtro externo ' . $m . ' ' . $r . ' en la línea de agua, por fuera del nevecón.',
            'Revisa que no haya fugas y purga el sistema para que el agua salga limpia desde el primer vaso. Te explica cada cuánto conviene cambiar el filtro; en general se recomienda cada 6 meses, según el uso y la calidad del agua.'],
        'ideal' => 'Quieres agua filtrada en el dispensador y en el hielo, y prefieres que te dejemos todo instalado de una vez: llave, manguera y filtro. El filtro externo va por fuera del nevecón, así que también sirve en nevecones de otras marcas que tengan dispensador (lo confirmamos contigo por WhatsApp antes de la visita).',
        'incluye' => ['Instalación a domicilio por un técnico de nuestro equipo', 'Llave galápago profesional con racores', 'Manguera de 1/4" hasta 5 metros', 'Filtro externo ' . $m . ' ' . $r . ' instalado', 'Conexión al nevecón', 'Prueba de fugas y purga del agua', '1 año de garantía en la instalación'],
        'no_incluye' => ['Trabajos nuevos de tubería en tu casa; si hacen falta, el técnico te los cotiza antes de empezar', 'Metros extra de manguera (cada 5 m: ' . cop($C['metro_extra']) . ')'],
        'specs' => array_merge($comun, [['Filtro externo', $m . ' ' . $r . ' (incluido e instalado)']], $cierre),
        'piezas' => [['k-man14-5', 'Manguera 1/4" hasta 5 m'], ['k-galapago', 'Llave galápago profesional'], [$f['img'], 'Filtro externo ' . $m . ' ' . $r]],
        'pasos' => $pasos, 'meta' => 'Instalación del agua de tu nevecón con filtro externo ' . $m . ' ' . $r . ', a domicilio en Cali y Jamundí. Llave galápago y manguera incluidas. 1 año de garantía.',
    ];
}

// ---------------------------------------------------------------- portada de la tienda de instalación
function inst_vista_home(): void
{
    $C = inst_config(); $n = cfg()['negocio']; $tel = $n['telefono'] ?? '301 381 0242'; $wa = inst_tel_wa();
    $m = fn(int $x) => cop($x); $zs = inst_nombres_zonas(); $rec = inst_recargos();
    $ld = ['@context' => 'https://schema.org', '@type' => 'ItemList', 'name' => 'Instalación de agua para nevecón a domicilio', 'itemListElement' => []];
    $i = 0;
    foreach ($C['servicios'] as $id => $sv) $ld['itemListElement'][] = ['@type' => 'ListItem', 'position' => ++$i, 'url' => base_url() . inst_url_producto($id), 'name' => $sv['nombre']];
    inst_cabecera('Instalación de agua para nevecón a domicilio en Cali y Jamundí | ' . $n['nombre'],
        'Un técnico de nuestro equipo instala el agua de tu nevecón en tu casa: llave galápago, manguera y filtro externo. Escoge el día y la hora; paga todo hoy o en 2 partes. 1 año de garantía.', '/instalacion-nevecon-cali/', $ld);
    ?>
<div class="ic">
<section class="ic-hero ic-hero-c"><div class="in">
  <div>
    <span class="eyebrow">Instalación a domicilio · <?= h($zs) ?></span>
    <h1>Instalación de agua para tu nevecón, a domicilio</h1>
    <p class="lead">Un técnico de nuestro equipo llega el día y la hora que tú escoges y deja el agua de tu nevecón funcionando. Escoge tu instalación, reserva y paga en línea.</p>
    <div class="acc"><a class="btn" href="#combos">Ver las instalaciones</a><a class="btn wa" href="https://wa.me/57<?= h($wa) ?>?text=<?= rawurlencode('Hola, quiero una instalación de agua para mi nevecón.') ?>" target="_blank" rel="noopener">💬 WhatsApp <?= h($tel) ?></a></div>
    <p class="ahora-co" id="ahora-co"><span class="punto" aria-hidden="true"></span><span id="ahora-co-t">Hora de Colombia: cargando…</span></p>
    <p class="proximo" id="proximo" hidden></p>
  </div>
  <ul class="ic-confia"><li><b>1 año de garantía</b><span>en la instalación</span></li><li><b>Pagas como prefieras</b><span>todo hoy, o en 2 partes</span></li><li><b>Un asesor te escribe</b><span>por WhatsApp para confirmar</span></li><li><b>Pago seguro</b><span>con Wompi</span></li></ul>
</div></section>

<section class="ic-sec" id="combos"><span class="eyebrow">Nuestras instalaciones</span><h2>Escoge la que necesitas</h2>
  <div class="ic-zonasel" role="group" aria-label="Ver precios por zona"><span>Precios en:</span><?php $zi = 0; foreach ($C['zonas'] as $zid => $z): ?><button type="button" data-zona="<?= h($zid) ?>" aria-pressed="<?= $zi++ === 0 ? 'true' : 'false' ?>"><?= h($z['nombre']) ?><?= $z['recargo'] ? ' (+' . $m($z['recargo']) . ')' : '' ?></button><?php endforeach; ?></div>
  <div class="ic-combos">
  <?php foreach ($C['servicios'] as $id => $sv): $f = $sv['filtro']; $t = inst_texto($id); ?>
    <article class="ic-combo<?= $f ? '' : ' base' ?>">
      <a class="foto" href="<?= h(inst_url_producto($id)) ?>"><?= inst_picture($id, $sv['nombre'] . ': manguera, llave galápago' . ($f ? ' y filtro externo' : ''), 320) ?></a>
      <div class="cuerpo"><h3><a href="<?= h(inst_url_producto($id)) ?>"><?= h($sv['corto']) ?></a></h3>
        <p class="m"><?= h($t['resumen']) ?></p>
        <ul><li>Llave galápago y manguera de hasta 5 m</li><?php if ($f): ?><li>Filtro externo <?= h($f['marca']) ?> <?= h($f['ref']) ?></li><?php endif; ?><li>Prueba de fugas y 1 año de garantía</li></ul></div>
      <div class="cobro"><b data-s="<?= h($id) ?>" data-k="precio"><?= $m($sv['precio']) ?></b><small>Total en <span data-zn>Cali</span> · pagas todo hoy o en 2 partes</small>
        <a class="btn" href="<?= h(inst_url_reservar($id)) ?>" data-r="<?= h($id) ?>">Reservar esta instalación</a>
        <a class="btn ghost" href="<?= h(inst_url_producto($id)) ?>">Ver detalles</a></div>
    </article>
  <?php endforeach; ?></div>
  <div class="ic-extras"><span><b>Más manguera:</b> cada 5 m extra <?= $m($C['metro_extra']) ?></span><span><b>Recargo por zona:</b> <?= h($rec) ?></span><span><b>Otra marca de nevecón:</b> también puedes pedir el combo con filtro</span></div>
</section>

<section class="ic-sec"><span class="eyebrow">Cómo funciona</span><h2>Cuatro pasos, sin sorpresas</h2>
  <div class="ic-grid">
    <div class="ic-card"><span class="n">1</span><h3>Escoges y reservas</h3><p>Tu instalación, tu zona, el día y la hora. El precio final lo ves antes de pagar.</p></div>
    <div class="ic-card"><span class="n">2</span><h3>Pagas hoy, en línea</h3><p>Todo, o solo una primera parte, con Wompi (tarjeta, PSE o Nequi). Tu horario queda apartado.</p></div>
    <div class="ic-card"><span class="n">3</span><h3>Un asesor te escribe</h3><p>Por WhatsApp, para confirmar tu instalación y darte los datos del técnico que va a tu casa.</p></div>
    <div class="ic-card"><span class="n">4</span><h3>El técnico instala</h3><p>Instala, prueba que no haya fugas y te muestra el agua funcionando. Si pagaste en 2 partes, le pagas el resto en efectivo.</p></div>
  </div></section>

<section class="ic-sec" id="pagos"><span class="eyebrow">Formas de pago</span><h2>Dos formas de pagar. Tú escoges.</h2>
  <div class="ic-grid dos">
    <div class="ic-card ic-pago"><span class="tag">Pago completo</span><h3>Pagar todo ahora</h3><p>Pagas la instalación completa hoy, en línea con Wompi. Tu horario queda confirmado y al terminar no pagas nada más.</p></div>
    <div class="ic-card ic-pago"><span class="tag verde">Pago en 2 partes</span><h3>Una parte hoy y el resto al técnico</h3>
      <ol class="ic-pasos2"><li><b>Hoy</b> pagas una primera parte en línea. Tu día y tu hora quedan apartados.</li><li><b>El técnico</b> llega, instala y te muestra el agua funcionando.</li><li><b>Al terminar</b> le pagas el resto <b>en efectivo, directamente al técnico</b>.</li></ol></div>
  </div>
  <div class="ic-tabla"><table><thead><tr><th>Instalación (en Cali)</th><th>Pagar todo ahora</th><th>2 partes: hoy, en línea</th><th>2 partes: al técnico, en efectivo</th></tr></thead><tbody>
  <?php foreach ($C['servicios'] as $id => $sv): ?><tr><td><b><?= h($sv['corto']) ?></b></td><td><?= $m($sv['precio']) ?></td><td><?= $m($sv['reserva']) ?></td><td><?= $m($sv['precio'] - $sv['reserva']) ?></td></tr><?php endforeach; ?>
  </tbody></table></div>
  <p class="m">El recargo de zona (<?= h($rec) ?>) y los metros extra de manguera se suman al total. Los pagos en línea son con tarjeta débito o crédito, PSE o Nequi, en la página segura de Wompi; al terminar, efectivo al técnico.</p>
</section>

<section class="ic-sec" id="otras-marcas"><span class="eyebrow">Para cualquier marca de nevecón</span><h2>¿Tu nevecón es de otra marca? También lo instalamos</h2>
  <p>El filtro externo se conecta a la manguera <b>por fuera del nevecón</b>, antes de que el agua llegue al aparato. Por eso puedes ponerle a tu nevecón un filtro Whirlpool, Samsung o LG aunque sea Mabe, Haceb, Electrolux, GE, Midea u otra marca, siempre que tenga dispensador de agua. Antes de la visita te escribimos por WhatsApp para confirmar que le sirve.</p></section>

<section class="ic-sec"><span class="eyebrow">Preguntas frecuentes</span><h2>Lo que más nos preguntan</h2><div>
  <details class="ic-faq"><summary>¿Quién va a mi casa y cómo me confirman?</summary><p>Apenas haces tu compra, <b>un asesor te contacta por WhatsApp</b> al número que dejaste, para confirmar tu instalación y darte los datos del técnico que te va a atender.</p></details>
  <details class="ic-faq"><summary>¿Cuánto pago ahora y cuánto al terminar?</summary><p>Tienes dos formas: <b>pagar todo ahora</b> (y al terminar no pagas nada más) o <b>pagar en 2 partes</b>: hoy <?= $m($C['servicios']['basica']['reserva']) ?>, <?= $m($C['servicios']['filtro-samsung']['reserva']) ?> o <?= $m($C['servicios']['filtro-whirlpool']['reserva']) ?> en línea, y el resto en efectivo al técnico cuando termina. El recargo de zona y la manguera extra, si aplican, se pagan en efectivo al terminar.</p></details>
  <details class="ic-faq"><summary>¿Cuánto tarda y qué debo tener listo?</summary><p>Cada cita tiene un espacio de hora y media en la agenda. Ten a mano una persona adulta en casa, espacio para mover el nevecón y el punto de agua a la vista.</p></details>
  <details class="ic-faq"><summary>¿Puedo cambiar el día o la hora?</summary><p>Sí. Avísanos con 24 horas de anticipación por WhatsApp y lo reprogramamos sin costo.</p></details>
  <details class="ic-faq"><summary>¿Qué cubre la garantía de 1 año?</summary><p>Fugas y fallas causadas por la instalación. No cubre daños del nevecón, de las tuberías de tu casa ni mal uso.</p></details>
</div></section>

<section class="ic-contacto"><div><span class="eyebrow">¿Tienes dudas?</span><b class="num">WhatsApp <?= h($tel) ?></b><span class="m">Lunes a sábado, de 8:00 a. m. a 5:00 p. m.</span><span class="m" style="font-size:13px;display:block;margin-top:6px"><?= identificacion() ?></span></div>
  <a class="btn wa" href="https://wa.me/57<?= h($wa) ?>?text=<?= rawurlencode('Hola, tengo una pregunta sobre la instalación del agua de mi nevecón.') ?>" target="_blank" rel="noopener">💬 Escribir por WhatsApp</a></section>
</div>
<script>window.INST = <?= json_encode(inst_pub(), JSON_UNESCAPED_UNICODE | JSON_HEX_TAG) ?>;</script>
<script src="/instalacion-nevecon-cali/tienda.js?v=<?= INST_V ?>" defer></script>
<?php
    pie();
}

// ---------------------------------------------------------------- página de cada instalación (como la ficha de un producto)
function inst_vista_producto(string $id): void
{
    $C = inst_config();
    if (!isset($C['servicios'][$id])) { http_response_code(404); echo 'No encontrado'; return; }
    $sv = $C['servicios'][$id]; $f = $sv['filtro']; $t = inst_texto($id); $n = cfg()['negocio']; $tel = $n['telefono'] ?? '301 381 0242'; $wa = inst_tel_wa();
    $m = fn(int $x) => cop($x); $rec = inst_recargos();
    $ld = ['@context' => 'https://schema.org', '@type' => 'Service', 'name' => $sv['nombre'], 'description' => $t['meta'], 'serviceType' => 'Instalación de agua para nevecón',
        'areaServed' => array_map(fn($z) => ['@type' => 'City', 'name' => $z['nombre']], array_values($C['zonas'])), 'provider' => ['@type' => 'LocalBusiness', 'name' => $n['nombre'], 'telephone' => '+57' . $wa],
        'offers' => ['@type' => 'Offer', 'priceCurrency' => 'COP', 'price' => $sv['precio'], 'availability' => 'https://schema.org/InStock', 'url' => base_url() . inst_url_producto($id)]];
    inst_cabecera($sv['nombre'] . ' a domicilio en Cali y Jamundí | ' . $n['nombre'], $t['meta'], inst_url_producto($id), $ld);
    ?>
<div class="ic ic-ficha">
<nav class="miga"><a href="/">Inicio</a> › <a href="/instalacion-nevecon-cali/">Instalación en Cali y Jamundí</a> › <?= h($sv['corto']) ?></nav>
<div class="ic-prod">
  <div class="ic-galeria">
    <div class="principal"><?= inst_picture($id, $sv['nombre'] . ': manguera, llave galápago' . ($f ? ' y filtro externo' : ''), 640) ?></div>
    <div class="piezas"><?php foreach ($t['piezas'] as [$foto, $et]): ?><figure><?= inst_foto($foto, $et, 120) ?><figcaption><?= h($et) ?></figcaption></figure><?php endforeach; ?></div>
  </div>
  <div class="ic-compra">
    <span class="m">Instalación a domicilio · <?= h(inst_nombres_zonas()) ?></span>
    <h1><?= h($t['h1']) ?></h1>
    <p class="m"><?= h($t['resumen']) ?></p>
    <div class="ic-zonasel" role="group" aria-label="Zona"><span>Precio en:</span><?php $zi = 0; foreach ($C['zonas'] as $zid => $z): ?><button type="button" data-zona="<?= h($zid) ?>" aria-pressed="<?= $zi++ === 0 ? 'true' : 'false' ?>"><?= h($z['nombre']) ?><?= $z['recargo'] ? ' (+' . $m($z['recargo']) . ')' : '' ?></button><?php endforeach; ?></div>
    <div class="ic-precio-g"><b data-s="<?= h($id) ?>" data-k="precio"><?= $m($sv['precio']) ?></b><small>Total en <span data-zn>Cali</span>. Manguera, llave y mano de obra incluidas.</small></div>
    <div class="ic-opciones ic-fp" role="radiogroup" aria-label="Cómo quieres pagar">
      <label class="ic-op"><input type="radio" name="fp" value="total"><span><b>Pagar todo ahora</b><small><b data-s="<?= h($id) ?>" data-k="online"><?= inst_nb($sv['precio']) ?></b> hoy, en línea con Wompi. <span data-s="<?= h($id) ?>" data-k="s2total">Al terminar no pagas nada más.</span></small></span></label>
      <label class="ic-op"><input type="radio" name="fp" value="reserva" checked><span><b>Pagar en 2 partes</b><small><b><?= inst_nb($sv['reserva']) ?></b> hoy, en línea + <b data-s="<?= h($id) ?>" data-k="resto"><?= inst_nb($sv['precio'] - $sv['reserva']) ?></b> en efectivo al técnico, al terminar.</small></span></label>
    </div>
    <a class="btn ic-cta" id="cta" href="<?= h(inst_url_reservar($id)) ?>" data-r="<?= h($id) ?>">Reservar esta instalación</a>
    <p class="m" style="font-size:13.5px">En el siguiente paso escoges el día y la hora en el calendario y dejas tus datos. Un asesor te escribe por WhatsApp para confirmar y darte los datos del técnico.</p>
    <ul class="ic-sellos"><li>🔒 Pago seguro con Wompi</li><li>🛠 1 año de garantía</li><li>↺ Reprogramación gratis</li></ul>
  </div>
</div>

<section class="ic-sec"><h2>Descripción</h2>
  <?php foreach ($t['parrafos'] as $p): ?><p><?= h($p) ?></p><?php endforeach; ?>
  <p><b>Ideal si:</b> <?= h($t['ideal']) ?></p></section>

<section class="ic-sec ic-dos-col">
  <div><h2>Qué incluye</h2><ul class="ic-incl uno"><?php foreach ($t['incluye'] as $x): ?><li><?= h($x) ?></li><?php endforeach; ?></ul></div>
  <div><h2>Qué no incluye</h2><ul class="ic-noincl"><?php foreach ($t['no_incluye'] as $x): ?><li><?= h($x) ?></li><?php endforeach; ?></ul></div>
</section>

<section class="ic-sec"><h2>Especificaciones</h2><div class="ic-tabla"><table><tbody><?php foreach ($t['specs'] as [$k, $v]): ?><tr><th><?= h($k) ?></th><td><?= h($v) ?></td></tr><?php endforeach; ?></tbody></table></div></section>

<section class="ic-sec"><h2>Cómo es el servicio, paso a paso</h2><ol class="ic-pasos2"><?php foreach ($t['pasos'] as $x): ?><li><?= h($x) ?></li><?php endforeach; ?></ol></section>

<section class="ic-sec"><h2>Preguntas sobre esta instalación</h2><div>
  <details class="ic-faq"><summary>¿Cuánto cuesta y cómo se paga?</summary><p><?= $m($sv['precio']) ?> en Cali (en Jamundí se suman <?= h(preg_replace('/^.*?\+/', '+', $rec)) ?>). Pagas todo ahora, o <?= $m($sv['reserva']) ?> hoy en línea y el resto en efectivo al técnico cuando termina.</p></details>
  <details class="ic-faq"><summary>¿Qué pasa si necesito más manguera?</summary><p>Incluye hasta 5 metros. Cada 5 metros adicionales cuestan <?= $m($C['metro_extra']) ?> y se pagan en efectivo al terminar. Si no sabes la distancia, el técnico la mide antes de empezar.</p></details>
  <details class="ic-faq"><summary>¿Mi nevecón es de otra marca, me sirve?</summary><p><?= $f ? 'El filtro externo va conectado a la manguera, por fuera del nevecón, así que sirve en otras marcas con dispensador de agua. Te escribimos por WhatsApp para confirmarlo antes de la visita.' : 'Sí: la instalación básica sirve para nevecones de cualquier marca con dispensador de agua.' ?></p></details>
  <details class="ic-faq"><summary>¿Quién va a mi casa?</summary><p>Un técnico de nuestro equipo. Apenas pagas, un asesor te escribe por WhatsApp para confirmar y darte sus datos.</p></details>
</div></section>

<section class="ic-sec"><h2>Otras instalaciones</h2><div class="ic-otras-lista">
  <?php foreach ($C['servicios'] as $oid => $o): if ($oid === $id) continue; ?>
    <a class="ic-mini" href="<?= h(inst_url_producto($oid)) ?>"><?= inst_picture($oid, $o['nombre'], 96) ?><span><b><?= h($o['corto']) ?></b><small data-s="<?= h($oid) ?>" data-k="precio"><?= $m($o['precio']) ?></small></span></a>
  <?php endforeach; ?></div></section>

<div class="ic-barra ic-barra-p"><span><b data-s="<?= h($id) ?>" data-k="precio"><?= $m($sv['precio']) ?></b><small><?= h($sv['corto']) ?></small></span><a class="btn" href="<?= h(inst_url_reservar($id)) ?>" data-r="<?= h($id) ?>">Reservar</a></div>
</div>
<script>window.INST = <?= json_encode(inst_pub(), JSON_UNESCAPED_UNICODE | JSON_HEX_TAG) ?>;</script>
<script src="/instalacion-nevecon-cali/tienda.js?v=<?= INST_V ?>" defer></script>
<?php
    pie();
}

// ---------------------------------------------------------------- página de reserva y pago (la "compra")
function inst_vista_checkout(): void
{
    $C = inst_config(); $n = cfg()['negocio']; $tel = $n['telefono'] ?? '301 381 0242'; $wa = inst_tel_wa();
    $m = fn(int $x) => cop($x); $zs = inst_nombres_zonas();
    $sel = isset($C['servicios'][$_GET['s'] ?? '']) ? (string) $_GET['s'] : 'basica';
    $zon = isset($C['zonas'][$_GET['z'] ?? '']) ? (string) $_GET['z'] : '';
    $fp = ($_GET['f'] ?? '') === 'total' ? 'total' : 'reserva';
    inst_cabecera('Reserva tu instalación | ' . $n['nombre'], 'Escoge el día y la hora, deja tus datos y paga tu instalación de agua para nevecón.', '/instalacion-nevecon-cali/reservar/', [], false);
    try { $dias = inst_agenda(); $errAg = ''; } catch (Throwable $e) { $dias = null; $errAg = 'E-' . substr(md5(get_class($e)), 0, 4); }
    ?>
<div class="ic ic-checkout">
<nav class="miga"><a href="/">Inicio</a> › <a href="/instalacion-nevecon-cali/">Instalación en Cali y Jamundí</a> › <a href="<?= h(inst_url_producto($sel)) ?>"><?= h($C['servicios'][$sel]['corto']) ?></a> › Reservar</nav>
<header class="ic-cab"><h1>Reserva tu instalación</h1><p class="m">Último paso: escoge el día y la hora, deja tus datos y paga. Tu horario queda apartado y un asesor te escribe por WhatsApp para confirmar.</p></header>
<form id="f" class="ic-form" novalidate autocomplete="on">
  <div class="ic-pasos">
    <section class="ic-paso" id="p1"><h3><i>1</i>Tu instalación</h3>
      <div class="ic-opciones" role="radiogroup" aria-label="Instalación">
      <?php foreach ($C['servicios'] as $id => $s): ?>
        <label class="ic-op"><input type="radio" name="servicio" value="<?= h($id) ?>" <?= $id === $sel ? 'checked' : '' ?>><?= inst_picture($id, $s['nombre'], 76) ?>
          <span><b><?= h($s['corto']) ?></b><small><?= $s['filtro'] ? 'Llave galápago + 5 m de manguera + filtro externo ' . h($s['filtro']['marca']) . ' ' . h($s['filtro']['ref']) : 'Llave galápago + hasta 5 m de manguera' ?></small><span class="pr"><?= $m($s['precio']) ?></span></span></label>
      <?php endforeach; ?></div>
      <p class="m" style="font-size:13.5px">¿Tu nevecón es de otra marca? Puedes escoger cualquiera: el filtro externo sirve en otras marcas con dispensador de agua. Lo confirmamos contigo por WhatsApp antes de la visita.</p></section>
    <section class="ic-paso" id="p2"><h3><i>2</i>¿En qué zona vives?</h3>
      <div class="ic-opciones" role="radiogroup" aria-label="Zona">
      <?php foreach ($C['zonas'] as $id => $z): ?>
        <label class="ic-op"><input type="radio" name="zona" value="<?= h($id) ?>" <?= $id === $zon ? 'checked' : '' ?>><span><b><?= h($z['nombre']) ?></b><small><?= $z['recargo'] ? 'Recargo por desplazamiento +' . $m($z['recargo']) : 'Sin recargo' ?></small></span></label>
      <?php endforeach; ?></div>
      <p class="m" style="font-size:13.5px">Por ahora atendemos solo en <?= h($zs) ?>. Si estás en otro lugar, escríbenos por WhatsApp y vemos si podemos ir.</p></section>
    <section class="ic-paso" id="p3"><h3><i>3</i>¿Qué tan lejos está el punto de agua del nevecón?</h3>
      <div class="ic-campos"><label class="ancho"><span>Distancia aproximada</span><select name="metros" id="metros">
        <option value="5">Hasta 5 metros (incluidos en el precio)</option>
        <option value="10">Hasta 10 metros (+<?= $m($C['metro_extra']) ?>)</option>
        <option value="15">Hasta 15 metros (+<?= $m($C['metro_extra'] * 2) ?>)</option>
        <option value="20">Hasta 20 metros (+<?= $m($C['metro_extra'] * 3) ?>)</option>
        <option value="nose">No lo sé: que el técnico la mida</option></select>
        <small>Si escoges «No lo sé» y se necesita más de 5 m, cada 5 m extra son <?= $m($C['metro_extra']) ?> y se pagan en efectivo al terminar.</small></label></div></section>
    <section class="ic-paso" id="p4"><h3><i>4</i>¿Qué día y a qué hora?</h3>
      <div class="ic-reloj"><span class="punto" aria-hidden="true"></span><span id="reloj">Hora de Colombia: cargando…</span></div>
      <div class="ic-cal" id="cal" role="group" aria-label="Calendario de disponibilidad"><span class="m">Cargando los días disponibles…</span></div>
      <div class="ic-leyenda"><span><i class="lib"></i>Disponible</span><span><i class="poc"></i>Pocos cupos</span><span><i class="lle"></i>Lleno o sin servicio</span></div>
      <p class="ic-aviso" id="aviso-horario" role="status"></p>
      <div class="ic-horas" id="horas" role="group" aria-label="Hora"></div>
      <p class="m" style="font-size:13.5px">Atendemos de lunes a sábado, de 8:00 a. m. a 5:00 p. m. La agenda se actualiza sola: si alguien reserva un horario, desaparece al instante. Solo ves horarios que empiezan dentro de <?= (int) $C['anticipacion_horas'] ?> horas o más desde ahora. ¿Lo necesitas más pronto? Escríbenos por WhatsApp.</p></section>
    <section class="ic-paso" id="p5"><h3><i>5</i>¿Cómo quieres pagar? <small style="font-weight:500;color:var(--muted)">(los montos se ajustan a tu pedido)</small></h3>
      <div class="ic-opciones" role="radiogroup" aria-label="Forma de pago">
        <label class="ic-op"><input type="radio" name="forma_pago" value="total" <?= $fp === 'total' ? 'checked' : '' ?>><span><b>Pagar todo ahora</b><small id="fp-total">Pagas el combo completo hoy, en línea con Wompi. Al terminar no pagas nada más.</small></span></label>
        <label class="ic-op"><input type="radio" name="forma_pago" value="reserva" <?= $fp === 'reserva' ? 'checked' : '' ?>><span><b>Pagar en 2 partes</b><small id="fp-dos">Una parte hoy en línea y el resto en efectivo al técnico, al terminar.</small></span></label></div></section>
    <section class="ic-paso" id="p6"><h3><i>6</i>Tus datos y la dirección</h3>
      <div class="ic-campos">
        <label>Nombre completo<input name="nombre" autocomplete="name" maxlength="80" required></label>
        <label>Celular (WhatsApp)<small style="font-weight:500;color:var(--muted)">Aquí te escribe el asesor para confirmar y darte los datos del técnico</small><input name="tel" type="tel" inputmode="numeric" autocomplete="tel" placeholder="300 123 4567" maxlength="16" required></label>
        <label class="ancho">Correo (te llega la confirmación)<input name="email" type="email" inputmode="email" autocomplete="email" placeholder="tucorreo@gmail.com" maxlength="120" required></label>
        <label>Marca del nevecón<select name="marca_nevecon" required><option value="">Escoge la marca</option><?php foreach (['Samsung', 'LG', 'Whirlpool', 'GE', 'KitchenAid', 'Mabe', 'Electrolux', 'Haceb', 'Otra'] as $mm) echo '<option>' . h($mm) . '</option>'; ?></select></label>
        <label id="otra-marca" hidden>¿De qué marca es?<input name="marca_otra" maxlength="30" placeholder="Por ejemplo: Mabe, Haceb, Electrolux"></label>
        <label>Modelo (opcional)<input name="modelo" maxlength="40" placeholder="Está en la etiqueta del nevecón"></label>
        <label class="ancho">¿Dónde está el punto de agua?<select name="toma"><option value="llave">Llave o toma de agua visible en la cocina</option><option value="lavaplatos">Debajo del lavaplatos</option><option value="tubo">Tubo de agua en la pared</option><option value="nose">No lo sé</option></select></label>
        <label>Barrio<input name="barrio" maxlength="80" required></label>
        <label>Dirección<input name="dir" autocomplete="street-address" maxlength="160" placeholder="Calle 5 # 66-20" required></label>
        <label class="ancho">Torre, apartamento o conjunto (opcional)<input name="detalle" maxlength="160" placeholder="Torre 2, apto 301, portería"></label>
        <label class="ancho">Algo más que debamos saber (opcional)<textarea name="notas" maxlength="300" placeholder="Por ejemplo: el nevecón está en el balcón, hay mascotas, llamar antes de llegar"></textarea></label>
        <input class="ic-trampa" name="web" tabindex="-1" autocomplete="off" aria-hidden="true">
      </div>
      <label class="ic-check"><input type="checkbox" name="acepto" required><span>Acepto las <a href="#condiciones">condiciones del servicio</a>, los <a href="/terminos.php" target="_blank" rel="noopener">términos</a> y la <a href="/privacidad.php" target="_blank" rel="noopener">política de datos</a>.</span></label></section>
  </div>
  <aside class="ic-res" aria-live="polite"><h3>Tu reserva</h3>
    <div id="lineas"></div>
    <div class="tot"><span>Total</span><span id="total">—</span></div>
    <div class="ahora"><span id="ahora-t">Pagas ahora para reservar</span><b id="reserva">—</b><span class="m" id="ahora-s">Y el resto de <b id="saldo" style="display:inline;font-size:inherit">—</b> en efectivo al técnico, al terminar.</span></div>
    <p class="ic-falta" id="falta"></p>
    <div class="ic-err" id="err" role="alert"></div>
    <button class="btn" type="submit" id="enviar">Reservar y pagar</button>
    <div class="ic-sellos"><span>🔒 Pago seguro con Wompi</span><span>🛠 1 año de garantía</span><span>↺ Reprogramación gratis</span></div>
  </aside>
</form>

<section class="ic-sec" id="condiciones"><span class="eyebrow">Condiciones del servicio</span><h2>Lo que debes saber antes de reservar</h2>
  <div class="ic-grid">
    <div class="ic-card"><h3>Cómo se paga</h3><p>Puedes pagar todo ahora en línea, o en 2 partes: una primera parte en línea que aparta tu horario y el resto en efectivo al técnico al terminar, cuando ya verificaste que todo funciona.</p></div>
    <div class="ic-card"><h3>Cambios y cancelaciones</h3><p>Avisando con 24 horas, reprogramamos sin costo o te devolvemos lo que pagaste en línea. Si el técnico llega y no hay nadie para recibirlo, no se devuelve la reserva (la primera parte del pago); si pagaste todo, te escribimos para reprogramar.</p></div>
    <div class="ic-card"><h3>Garantía de 1 año</h3><p>Cubre fugas y fallas causadas por la instalación. No cubre daños del nevecón, de las tuberías de tu casa ni mal uso.</p></div>
    <div class="ic-card"><h3>Tu punto de agua</h3><p>Instalamos desde un punto de agua que ya exista y esté en buen estado. Si hace falta trabajo adicional en tuberías, el técnico te lo cotiza antes de empezar.</p></div>
  </div>
  <p class="m"><?= identificacion() ?> · WhatsApp <?= h($tel) ?></p></section>

<div class="ic-barra" id="barra"><span><b id="barra-r">Reserva —</b><small id="barra-t">Total —</small></span><a class="btn" href="#p6" id="barra-b">Continuar</a></div>
</div>
<script>window.INST = <?= json_encode(inst_pub(), JSON_UNESCAPED_UNICODE | JSON_HEX_TAG) ?>; window.INST_DIAS = <?= json_encode($dias, JSON_UNESCAPED_UNICODE | JSON_HEX_TAG) ?>; window.INST_TS = <?= time() ?>; window.INST_ERR = <?= json_encode($errAg) ?>;</script>
<script src="/instalacion-nevecon-cali/instalacion.js?v=<?= INST_V ?>" defer></script>
<?php
    pie();
}
