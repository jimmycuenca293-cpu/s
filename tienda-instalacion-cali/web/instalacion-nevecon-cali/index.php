<?php
declare(strict_types=1);
require __DIR__ . '/../partes.php';
require_once __DIR__ . '/../filtrosnevecones-api/instalacion-lib.php';
$C = inst_config(); $n = cfg()['negocio']; $tel = $n['telefono'] ?? '301 381 0242'; $wa = inst_tel_wa();
$V = '20261029a';
$pub = ['servicios' => array_map(fn($s) => ['nombre' => $s['nombre'], 'corto' => $s['corto'], 'precio' => $s['precio'], 'reserva' => $s['reserva']], $C['servicios']),
    'zonas' => $C['zonas'], 'metro_extra' => $C['metro_extra'], 'franjas' => count($C['franjas'])];
$ld = ['@context' => 'https://schema.org', '@type' => 'Service', 'name' => 'Instalación de agua para nevecón a domicilio', 'serviceType' => 'Instalación de llave, manguera y filtro externo para nevecón',
    'areaServed' => array_map(fn($z) => ['@type' => 'City', 'name' => $z['nombre']], array_values($C['zonas'])),
    'provider' => ['@type' => 'LocalBusiness', 'name' => $n['nombre'], 'telephone' => '+57' . $wa],
    'offers' => ['@type' => 'AggregateOffer', 'priceCurrency' => 'COP', 'lowPrice' => $C['servicios']['basica']['precio'], 'highPrice' => $C['servicios']['filtro-whirlpool']['precio'] + 40000, 'offerCount' => 4]];
cabeza('Instalación de nevecón a domicilio en Cali y Jamundí | ' . $n['nombre'],
    'Un técnico instala el agua de tu nevecón en tu casa: llave galápago, manguera y filtro externo. Escoge el día y la hora, reserva en línea y paga el saldo al terminar. 1 año de garantía.',
    '/instalacion-nevecon-cali/', '<link rel="stylesheet" href="/instalacion-nevecon-cali/instalacion.css?v=' . $V . '"><script type="application/ld+json">' . json_encode($ld, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_HEX_TAG) . '</script>');
$img = fn(string $id, string $alt, int $w = 58) => '<picture><source srcset="/filtrosnevecones-img/' . $id . '-400.webp" type="image/webp"><img src="/filtrosnevecones-img/' . $id . '.jpg" alt="' . h($alt) . '" width="' . $w . '" height="' . $w . '" loading="lazy"></picture>';
$fotos = ['basica' => 'k-galapago', 'filtro-samsung' => 'sam-ex-o', 'filtro-lg' => 'lg-ex-o', 'filtro-whirlpool' => 'wp-ex-o'];
$m = fn(int $x) => cop($x);
?>
<div class="ic">
<section class="ic-hero"><div class="in">
  <div>
    <span class="eyebrow">Instalación a domicilio · Cali y Jamundí</span>
    <h1>Instalación de agua para tu nevecón, a domicilio</h1>
    <p class="lead">Un técnico llega el día y la hora que tú escoges, conecta tu nevecón con llave galápago profesional y manguera, y pone el filtro externo si lo quieres. El saldo lo pagas al terminar, cuando ya ves el agua funcionando.</p>
    <div class="acc"><a class="btn" href="#combos">Ver combos y reservar</a><a class="btn wa" href="https://wa.me/57<?= h($wa) ?>?text=<?= rawurlencode('Hola, quiero una instalación de agua para mi nevecón.') ?>" target="_blank" rel="noopener">💬 WhatsApp <?= h($tel) ?></a></div>
    <ul><li>1 año de garantía en la instalación</li><li>Reservas en línea y pagas el saldo al terminar</li><li>Cambias el día o la hora gratis, avisando con 24 horas</li></ul>
  </div>
  <aside class="ic-precio" aria-label="Precios de la instalación en Cali">
    <span class="eyebrow" style="color:#9fe8ff">Precios en Cali</span>
    <div class="fila"><span>Instalación básica</span><b><?= $m($C['servicios']['basica']['precio']) ?></b></div>
    <div class="fila"><span>Con filtro Samsung o LG</span><b><?= $m($C['servicios']['filtro-samsung']['precio']) ?></b></div>
    <div class="fila"><span>Con filtro Whirlpool</span><b><?= $m($C['servicios']['filtro-whirlpool']['precio']) ?></b></div>
    <small>En Jamundí +<?= $m($C['zonas']['jamundi']['recargo']) ?>. El precio ya incluye la llave, la manguera de hasta 5 m y la mano de obra.</small>
  </aside>
</div></section>

<section class="ic-sec" id="combos"><span class="eyebrow">Nuestros combos</span><h2>Escoge el servicio que necesitas</h2>
  <p class="m">Todos incluyen la instalación a domicilio, llave galápago profesional con racores, hasta 5 m de manguera de 1/4", prueba de fugas y 1 año de garantía. Precios en Cali.</p>
  <div class="ic-combos">
  <?php foreach ($C['servicios'] as $id => $sv): $f = $sv['filtro']; ?>
    <article class="ic-combo<?= $f ? '' : ' base' ?>">
      <div class="foto"><?= $img($fotos[$id], $sv['nombre'], 120) ?></div>
      <div class="cuerpo"><h3><?= h($sv['corto']) ?></h3>
        <p class="m"><?= $f ? 'Incluye el filtro externo ' . h($f['marca']) . ' ' . h($f['ref']) . ' instalado en la línea de agua.' : 'La conexión del agua del nevecón, sin filtro. Sirve para cualquier marca.' ?></p>
        <ul><li>Llave galápago y racores</li><li>Hasta 5 m de manguera</li><li><?= $f ? 'Filtro externo ' . h($f['marca']) : 'Prueba de fugas y purga' ?></li></ul></div>
      <div class="cobro"><b><?= $m($sv['precio']) ?></b><small>Reservas con <?= $m($sv['reserva']) ?></small>
        <a class="btn" href="#reservar" data-pick="<?= h($id) ?>">Quiero este</a></div>
    </article>
  <?php endforeach; ?></div>
  <div class="ic-extras"><span><b>Más manguera:</b> cada 5 m extra <?= $m($C['metro_extra']) ?></span><span><b>Zonas:</b> Jamundí +<?= $m($C['zonas']['jamundi']['recargo']) ?></span><span><b>Otra marca de nevecón:</b> escoge la instalación básica</span></div>
</section>

<section class="ic-sec"><span class="eyebrow">Qué incluye</span><h2>Todo lo necesario para que salga agua del dispensador</h2>
  <ul class="ic-incl">
    <li><b>Llave galápago profesional</b> con sus racores, para tomar el agua sin cortar el tubo.</li>
    <li><b>Hasta 5 metros de manguera</b> de 1/4". Si tu nevecón queda más lejos, cada 5 m extra cuesta <?= $m($C['metro_extra']) ?>.</li>
    <li><b>Conexión al nevecón</b> y revisión de que el dispensador y la máquina de hielo reciban agua.</li>
    <li><b>Prueba de fugas y purga</b> del agua antes de irnos, para que la tomes limpia desde el primer vaso.</li>
    <li><b>Filtro externo</b> instalado en la línea, si escoges el servicio con filtro (Samsung, LG o Whirlpool).</li>
    <li><b>1 año de garantía</b> en la instalación: si hay una fuga o falla por la instalación, la corregimos sin costo.</li>
  </ul></section>

<section class="ic-sec"><span class="eyebrow">Cómo funciona</span><h2>Cuatro pasos, sin sorpresas</h2>
  <div class="ic-grid">
    <div class="ic-card"><span class="n">1</span><h3>Escoges tu servicio</h3><p>Tu zona, tu marca de filtro, el día y la hora que más te sirven. El precio final lo ves antes de pagar.</p></div>
    <div class="ic-card"><span class="n">2</span><h3>Pagas la reserva</h3><p>Una parte en línea, con Wompi (tarjeta, PSE o Nequi), o el total si prefieres. Así tu horario queda apartado solo para ti.</p></div>
    <div class="ic-card"><span class="n">3</span><h3>El técnico llega</h3><p>En el horario que escogiste. Instala, prueba que no haya fugas y te muestra el agua funcionando.</p></div>
    <div class="ic-card"><span class="n">4</span><h3>Pagas el saldo al terminar</h3><p>En efectivo al técnico, solo cuando todo quedó bien. Te queda 1 año de garantía en la instalación.</p></div>
  </div></section>

<section class="ic-sec" id="pagos"><span class="eyebrow">Formas de pago</span><h2>Tú escoges cómo pagar</h2>
  <div class="ic-grid">
    <div class="ic-card ic-pago"><span class="tag">La más usada</span><h3>Reservas y pagas el resto al terminar</h3>
      <p>Pagas en línea una <b>reserva</b> (<?= $m($C['servicios']['basica']['reserva']) ?> en la básica, <?= $m($C['servicios']['filtro-samsung']['reserva']) ?> con filtro Samsung o LG, <?= $m($C['servicios']['filtro-whirlpool']['reserva']) ?> con filtro Whirlpool). Esa reserva aparta tu día y tu hora para tomar el servicio.</p>
      <p>Cuando el técnico termina y ves el agua funcionando, le pagas el <b>saldo en efectivo</b>, directamente a él.</p></div>
    <div class="ic-card ic-pago"><h3>Pagas el total en línea</h3>
      <p>Si prefieres no manejar efectivo, paga <b>todo</b> por adelantado. Escoges esta opción al reservar y te enviamos por WhatsApp el link de pago por el valor exacto. Al terminar no pagas nada más.</p></div>
    <div class="ic-card ic-pago"><h3>Medios de pago en línea</h3>
      <p>Tarjeta débito o crédito, PSE y Nequi, en la página segura de Wompi. Nosotros nunca vemos los datos de tu tarjeta.</p>
      <p>Al terminar la instalación: <b>efectivo</b> al técnico.</p></div>
  </div></section>

<section class="ic-sec" id="reservar"><span class="eyebrow">Reserva tu instalación</span><h2>Escoge el servicio, el día y la hora</h2>
<form id="f" class="ic-form" novalidate autocomplete="on">
  <div class="ic-pasos">
    <section class="ic-paso" id="p1"><h3><i>1</i>¿Qué necesitas?</h3>
      <div class="ic-opciones" role="radiogroup" aria-label="Servicio">
      <?php foreach ($C['servicios'] as $id => $s): ?>
        <label class="ic-op"><input type="radio" name="servicio" value="<?= h($id) ?>" <?= $id === 'basica' ? 'checked' : '' ?>><?= $img($fotos[$id], $s['nombre']) ?>
          <span><b><?= h($s['corto']) ?></b><small><?= $s['filtro'] ? 'Incluye filtro externo ' . h($s['filtro']['marca']) . ' ' . h($s['filtro']['ref']) : 'Llave galápago y hasta 5 m de manguera' ?></small><span class="pr"><?= $m($s['precio']) ?></span></span></label>
      <?php endforeach; ?></div>
      <p class="m" style="font-size:13.5px">¿Tu nevecón es de otra marca? Escoge la instalación básica o escríbenos por WhatsApp y te decimos qué filtro le sirve.</p></section>
    <section class="ic-paso" id="p2"><h3><i>2</i>¿En qué zona vives?</h3>
      <div class="ic-opciones" role="radiogroup" aria-label="Zona">
      <?php foreach ($C['zonas'] as $id => $z): ?>
        <label class="ic-op"><input type="radio" name="zona" value="<?= h($id) ?>"><span><b><?= h($z['nombre']) ?></b><small><?= $z['recargo'] ? 'Recargo por desplazamiento +' . $m($z['recargo']) : 'Sin recargo' ?></small></span></label>
      <?php endforeach; ?></div></section>
    <section class="ic-paso" id="p3"><h3><i>3</i>¿Qué tan lejos está el punto de agua del nevecón?</h3>
      <div class="ic-campos"><label class="ancho"><span>Distancia aproximada</span><select name="metros" id="metros">
        <option value="5">Hasta 5 metros (incluidos en el precio)</option>
        <option value="10">Hasta 10 metros (+<?= $m($C['metro_extra']) ?>)</option>
        <option value="15">Hasta 15 metros (+<?= $m($C['metro_extra'] * 2) ?>)</option>
        <option value="20">Hasta 20 metros (+<?= $m($C['metro_extra'] * 3) ?>)</option>
        <option value="nose">No lo sé: que el técnico la mida</option></select>
        <small>Si escoges «No lo sé» y se necesita más de 5 m, cada 5 m extra son <?= $m($C['metro_extra']) ?> y se pagan al terminar.</small></label></div></section>
    <section class="ic-paso" id="p4"><h3><i>4</i>¿Qué día y a qué hora?</h3>
      <div class="ic-fechas" id="fechas" role="group" aria-label="Día"><span class="m">Cargando los días disponibles…</span></div>
      <div class="ic-horas" id="horas" role="group" aria-label="Hora"></div>
      <p class="m" style="font-size:13.5px">Atendemos de lunes a sábado, de 8:00 a. m. a 5:00 p. m. ¿Lo necesitas hoy o mañana mismo? Escríbenos por WhatsApp.</p></section>
        <section class="ic-paso" id="p5"><h3><i>5</i>¿Cómo quieres pagar?</h3>
      <div class="ic-opciones" role="radiogroup" aria-label="Forma de pago">
        <label class="ic-op"><input type="radio" name="forma_pago" value="reserva" checked><span><b>Reserva ahora y el resto al terminar</b><small>Pagas la reserva en línea y el saldo en efectivo al técnico cuando termine.</small></span></label>
        <label class="ic-op"><input type="radio" name="forma_pago" value="total"><span><b>Pago el total en línea</b><small>Te enviamos por WhatsApp el link para pagar todo. Al terminar no pagas nada más.</small></span></label></div></section>
    <section class="ic-paso" id="p6"><h3><i>6</i>Tus datos y la dirección</h3>
      <div class="ic-campos">
        <label>Nombre completo<input name="nombre" autocomplete="name" maxlength="80" required></label>
        <label>Celular (WhatsApp)<input name="tel" type="tel" inputmode="numeric" autocomplete="tel" placeholder="300 123 4567" maxlength="16" required></label>
        <label class="ancho">Correo (te llega la confirmación)<input name="email" type="email" inputmode="email" autocomplete="email" placeholder="tucorreo@gmail.com" maxlength="120" required></label>
        <label>Marca del nevecón<select name="marca_nevecon" required><option value="">Escoge la marca</option><?php foreach (['Samsung', 'LG', 'Whirlpool', 'GE', 'KitchenAid', 'Mabe', 'Electrolux', 'Haceb', 'Otra'] as $mm) echo '<option>' . h($mm) . '</option>'; ?></select></label>
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
    <div class="ahora"><span id="ahora-t">Pagas ahora para reservar</span><b id="reserva">—</b><span class="m" id="ahora-s">Y el saldo de <b id="saldo" style="display:inline;font-size:inherit">—</b> en efectivo al técnico, al terminar.</span></div>
    <div class="ic-err" id="err" role="alert"></div>
    <button class="btn" type="submit" id="enviar">Reservar y pagar</button>
    <div class="ic-sellos"><span>🔒 Pago seguro con Wompi</span><span>🛠 1 año de garantía</span><span>↺ Reprogramación gratis</span></div>
  </aside>
</form></section>

<div class="ic-barra" id="barra"><span><b id="barra-r">Reserva —</b><small id="barra-t">Total —</small></span><a class="btn" href="#reservar" id="barra-b">Continuar</a></div>

<section class="ic-sec" id="condiciones"><span class="eyebrow">Condiciones del servicio</span><h2>Lo que debes saber antes de reservar</h2>
  <div class="ic-grid">
    <div class="ic-card"><h3>Reserva y saldo</h3><p>La reserva se paga en línea y aparta tu horario. El saldo se paga en efectivo al técnico al terminar, cuando ya verificaste que todo funciona. También puedes pagar el total en línea.</p></div>
    <div class="ic-card"><h3>Cambios y cancelaciones</h3><p>Avisando con 24 horas, reprogramamos sin costo o te devolvemos la reserva. Si el técnico llega y no hay nadie para recibirlo, la reserva no se devuelve.</p></div>
    <div class="ic-card"><h3>Garantía de 1 año</h3><p>Cubre fugas y fallas causadas por la instalación. No cubre daños del nevecón, de las tuberías de tu casa ni mal uso.</p></div>
    <div class="ic-card"><h3>Tu punto de agua</h3><p>Instalamos desde un punto de agua que ya exista y esté en buen estado. Si hace falta trabajo adicional en tuberías, el técnico te lo cotiza antes de empezar.</p></div>
  </div></section>

<section class="ic-sec"><span class="eyebrow">Preguntas frecuentes</span><h2>Lo que más nos preguntan</h2><div>
  <details class="ic-faq"><summary>¿Cuánto cuesta en total?</summary><p>En Cali, <?= $m($C['servicios']['basica']['precio']) ?> la instalación básica, <?= $m($C['servicios']['filtro-samsung']['precio']) ?> con filtro Samsung o LG y <?= $m($C['servicios']['filtro-whirlpool']['precio']) ?> con filtro Whirlpool. En Jamundí se suman <?= $m($C['zonas']['jamundi']['recargo']) ?>. El total exacto lo ves en tu reserva antes de pagar.</p></details>
  <details class="ic-faq"><summary>¿Cuánto pago ahora y cuánto al terminar?</summary><p>Ahora pagas una reserva de <?= $m($C['servicios']['basica']['reserva']) ?> (básica), <?= $m($C['servicios']['filtro-samsung']['reserva']) ?> (con filtro Samsung o LG) o <?= $m($C['servicios']['filtro-whirlpool']['reserva']) ?> (con filtro Whirlpool). El resto lo pagas al terminar.</p></details>
  <details class="ic-faq"><summary>¿Cómo pago el saldo?</summary><p>En efectivo, directamente al técnico, cuando termina la instalación y ves el agua funcionando. Si prefieres no manejar efectivo, escoge «Pago el total en línea» al reservar.</p></details>
  <details class="ic-faq"><summary>¿Qué pasa si necesito más manguera?</summary><p>La instalación incluye hasta 5 metros. Cada 5 metros adicionales cuestan <?= $m($C['metro_extra']) ?>. Si no sabes la distancia, el técnico la mide en tu casa antes de empezar.</p></details>
  <details class="ic-faq"><summary>¿Cómo sé qué filtro externo necesita mi nevecón?</summary><p>El servicio con filtro incluye el filtro de la marca que escojas (Samsung, LG o Whirlpool). Si tienes dudas, escríbenos por WhatsApp al <?= h($tel) ?> con la marca y el modelo de tu nevecón y te lo confirmamos.</p></details>
  <details class="ic-faq"><summary>¿Puedo cambiar el día o la hora?</summary><p>Sí. Avísanos con 24 horas de anticipación por WhatsApp y lo reprogramamos sin costo.</p></details>
</div></section>

<section class="ic-contacto"><div><span class="eyebrow">¿Tienes dudas?</span><b class="num">WhatsApp <?= h($tel) ?></b><span class="m">Lunes a sábado, de 8:00 a. m. a 5:00 p. m.</span></div>
  <a class="btn wa" href="https://wa.me/57<?= h($wa) ?>?text=<?= rawurlencode('Hola, tengo una pregunta sobre la instalación del agua de mi nevecón.') ?>" target="_blank" rel="noopener">💬 Escribir por WhatsApp</a></section>
</div>
<script>window.INST = <?= json_encode($pub, JSON_UNESCAPED_UNICODE | JSON_HEX_TAG) ?>;</script>
<script src="/instalacion-nevecon-cali/instalacion.js?v=<?= $V ?>" defer></script>
<?php pie(); ?>
