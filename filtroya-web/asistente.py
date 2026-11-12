"""Asistente de chat para encontrar el filtro: el cliente escribe el modelo de su nevecón (o la referencia del filtro viejo)
y el asistente le dice cuál filtro es, con precio y enlace. Funciona solo, 24 horas, sin servidor: los datos van dentro del archivo.
Si no encuentra el modelo, pasa la conversación a WhatsApp con el modelo ya escrito (ahí contesta una persona)."""
import json

JS = r"""(function () {
  var D = __DATOS__;
  if (!D.length || document.getElementById('fn-chat')) return;
  var n = function (s) { return String(s || '').toUpperCase().replace(/[^A-Z0-9]/g, ''); };
  var cop = function (v) { return '$ ' + String(v).replace(/\B(?=(\d{3})+(?!\d))/g, '.'); };
  var correo = '__CORREO__';
  var INFO = __INFO__;
  var wa = (document.querySelector('a[href*="wa.me/"]') || {}).href || '';
  wa = (wa.match(/wa\.me\/(\d+)/) || [])[1] || '';
  var css = '#fn-chat-b{position:fixed;left:14px;bottom:14px;z-index:60;display:flex;align-items:center;gap:8px;border:0;border-radius:99px;padding:12px 16px;background:#17181b;color:#fff;font:700 14px system-ui,sans-serif;box-shadow:0 8px 24px rgba(0,0,0,.28);cursor:pointer}'
    + '#fn-chat-b i{font-style:normal;width:10px;height:10px;border-radius:50%;background:#25d366;box-shadow:0 0 0 3px rgba(37,211,102,.3)}'
    + '#fn-chat{position:fixed;left:14px;bottom:70px;z-index:61;width:min(370px,calc(100vw - 28px));height:min(520px,calc(100vh - 100px));background:#fff;color:#1b1b1b;border-radius:16px;box-shadow:0 20px 60px rgba(0,0,0,.35);display:none;flex-direction:column;overflow:hidden;font:15px/1.45 system-ui,sans-serif}'
    + '#fn-chat.on{display:flex}#fn-chat header{background:#17181b;color:#fff;padding:12px 14px;display:flex;justify-content:space-between;align-items:center;gap:8px}'
    + '#fn-chat header b{display:block;font-size:15px}#fn-chat header small{opacity:.8;font-size:12px}#fn-chat header button{background:none;border:0;color:#fff;font-size:22px;cursor:pointer;line-height:1}'
    + '#fn-m{flex:1;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:8px;background:#f6f5f2}'
    + '.fn-b{max-width:88%;padding:9px 12px;border-radius:14px;word-wrap:break-word}.fn-b.bot{background:#fff;border:1px solid #e6e2d8;align-self:flex-start;border-bottom-left-radius:4px}.fn-b.yo{background:#eeb111;color:#231f20;align-self:flex-end;border-bottom-right-radius:4px;font-weight:600}'
    + '.fn-b a.fn-bt{display:inline-block;margin:6px 6px 0 0;padding:8px 12px;border-radius:8px;background:#17181b;color:#fff;text-decoration:none;font-weight:700;font-size:14px}.fn-b a.fn-bt.wa{background:#25d366}'
    + '.fn-b .fn-pr{font-weight:800;font-size:17px}.fn-q{display:flex;flex-wrap:wrap;gap:6px;padding:0 12px 8px;background:#f6f5f2}.fn-q button{border:1px solid #cfc8b6;background:#fff;border-radius:99px;padding:6px 11px;font:600 13px system-ui,sans-serif;cursor:pointer}'
    + '#fn-f{display:flex;gap:6px;padding:10px;border-top:1px solid #e6e2d8;background:#fff}#fn-f input{flex:1;min-width:0;border:1px solid #cfc8b6;border-radius:10px;padding:10px;font:16px system-ui,sans-serif}#fn-f button{border:0;border-radius:10px;padding:0 14px;background:#eeb111;color:#231f20;font-weight:800;cursor:pointer}'
    + '.fn-dots i{display:inline-block;width:7px;height:7px;border-radius:50%;background:#9aa0aa;margin:0 2px;animation:fnd 1s infinite}.fn-dots i:nth-child(2){animation-delay:.15s}.fn-dots i:nth-child(3){animation-delay:.3s}@keyframes fnd{50%{transform:translateY(-4px);opacity:.5}}'
    + '.fn-b button.fn-bt{display:inline-block;margin:6px 6px 0 0;padding:9px 13px;border-radius:8px;border:0;background:#1428a0;color:#fff;font:700 14px system-ui,sans-serif;cursor:pointer}'
    + '@media (max-width:520px){#fn-chat-b span{display:none}#fn-chat-b{padding:13px}}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
  var b = document.createElement('button'); b.id = 'fn-chat-b'; b.type = 'button'; b.setAttribute('aria-label', 'Abrir el asistente para encontrar tu filtro'); b.innerHTML = '<i></i><span>¿Cuál filtro es el mío?</span>';
  var w = document.createElement('div'); w.id = 'fn-chat'; w.setAttribute('role', 'dialog'); w.setAttribute('aria-label', 'Asistente para encontrar tu filtro');
  w.innerHTML = '<header><div><b>Asistente de filtros</b><small>Te digo qué filtro le sirve a tu nevecón</small></div><button type="button" aria-label="Cerrar">×</button></header><div id="fn-m" aria-live="polite"></div><div class="fn-q" id="fn-q"></div><form id="fn-f"><input type="text" id="fn-i" placeholder="Modelo de tu nevecón, ej. WRF555SDFZ" autocomplete="off" aria-label="Modelo de tu nevecón o referencia del filtro"><button type="submit">Enviar</button></form>';
  document.body.appendChild(b); document.body.appendChild(w);
  var M = w.querySelector('#fn-m'), Q = w.querySelector('#fn-q'), I = w.querySelector('#fn-i'), abierto = false, saludo = false;
  function ev(a, d) { try { (window.dataLayer = window.dataLayer || []).push({event: 'chat_filtro', chat_accion: a, chat_dato: d || ''}); } catch (e) {} }
  function msg0(h, quien) { var d = document.createElement('div'); d.className = 'fn-b ' + quien; d.innerHTML = h; M.appendChild(d); M.scrollTop = M.scrollHeight; return d; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]; }); }
  var pend = Promise.resolve();
  function msg(h, quien) {
    if (quien !== 'bot') return msg0(h, quien);
    pend = pend.then(function () { return new Promise(function (r) { var d = msg0('<span class="fn-dots"><i></i><i></i><i></i></span>', 'bot'); setTimeout(function () { d.innerHTML = h; M.scrollTop = M.scrollHeight; r(); }, Math.min(900, 380 + String(h).length * 2)); }); });
  }
  function chips(l) { pend = pend.then(function () { chips0(l); }); }
  function chips0(l) { Q.innerHTML = ''; setTimeout(function () { M.scrollTop = M.scrollHeight; }, 0); l.forEach(function (x) { var c = document.createElement('button'); c.type = 'button'; c.textContent = x[0]; c.onclick = function () { x[1](); }; Q.appendChild(c); }); }
  function forma(f, txt) {
    msg(txt, 'yo');
    var p = D.filter(function (x) { return x.f === f; })[0];
    if (!p) { msg('No tengo ese tipo en la tienda.', 'bot'); return; }
    ev('forma', f);
    msg(tarjeta(p, f === 'externo' ? 'Si va afuera, en la manguera del agua, es el <b>filtro externo</b>:' : f === 'redondo' ? 'Un cartucho <b>redondo, que se saca girándolo</b>, es este:' : 'Un cartucho <b>cuadrado, que se saca empujando</b>, es este:') + '<br><small>Confirma el código impreso en tu filtro viejo: debe ser <b>' + esc(p.r) + '</b>.</small>', 'bot');
    chips([['Ver otra forma', viejo], ['Escribir mi modelo', modelo], ['¿Cómo pago?', pago]]);
  }
  function viejo() { msg('Tengo el filtro viejo', 'yo'); msg('Perfecto. Míralo y dime <b>¿cómo es?</b>', 'bot'); chips([['Redondo (se gira)', function () { forma('redondo', 'Es redondo'); }], ['Cuadrado (se empuja)', function () { forma('cuadrado', 'Es cuadrado'); }], ['Va en la manguera del agua', function () { forma('externo', 'Va en la manguera'); }]]); }
  function modelo() { msg('Sé el modelo de mi nevecón', 'yo'); msg('Escríbelo aquí abajo (por ejemplo <b>RF28HMEDBSR</b> o <b>RF28R7351SR</b>) y te digo cuál filtro es.', 'bot'); I.focus(); }
  function pago() { msg('¿Cómo pago?', 'yo'); msg(INFO.pago || 'Pagas en línea, en la pasarela segura de Wompi, con tarjeta, PSE, Nequi o Bancolombia.', 'bot'); chips([['Ver cómo es mi filtro', viejo], ['¿Cuánto tarda?', entrega]]); }
  function entrega() { msg('¿Cuánto tarda?', 'yo'); msg(INFO.entrega || 'El tiempo de entrega depende de tu ciudad; lo ves en la página de tu ciudad.', 'bot'); chips([['Ver cómo es mi filtro', viejo], ['¿Cómo pago?', pago]]); }
  function precios() { msg('¿Cuánto cuesta?', 'yo'); msg(D.map(function (p) { return '<b>' + esc(p.n) + '</b>: ' + cop(p.p); }).join('<br>') + (INFO.packs ? '<br><small>También en pack de 2, con ahorro.</small>' : ''), 'bot'); chips([['Ver cómo es mi filtro', viejo], ['¿Cómo pago?', pago]]); }
  function menuBase() { if (INFO.guiado) { chips([['Tengo el filtro viejo', viejo], ['Sé el modelo de mi nevecón', modelo], ['No sé cuál es', donde], ['¿Cuánto cuesta?', precios], ['¿Cómo pago?', pago], ['¿Cuánto tarda?', entrega]]); return; } chips([['¿Dónde está el modelo?', donde], ['Tengo la referencia del filtro viejo', function () { msg('Tengo la referencia del filtro viejo', 'yo'); msg('Escríbela aquí abajo. Está impresa en el filtro, por ejemplo <b>W10295370</b>, <b>EDR3RXD1</b> o <b>LT1000P</b>.', 'bot'); I.focus(); }], [wa || !correo ? 'Hablar con una persona' : 'Escribir por correo', persona]]); }
  function donde() { msg('¿Dónde está el modelo?', 'yo'); msg('El modelo está en una <b>etiqueta dentro del refrigerador</b>, en la pared lateral (arriba) o detrás del cajón de las verduras. Suele empezar por letras y números, por ejemplo <b>WRF555SDFZ</b>, <b>RF28HMEDBSR</b> o <b>LFXS26973S</b>. Escríbelo aquí y te digo cuál filtro es.', 'bot'); I.focus(); }
  function persona(txt) {
    ev('whatsapp', txt || '');
    var t = 'Hola, necesito saber qué filtro le sirve a mi nevecón.' + (txt ? ' Modelo o referencia: ' + txt : '');
    if (!wa) { msg(correo ? 'Con gusto. Escríbenos y una persona te responde por correo' + (txt ? ' (ya va escrito tu modelo)' : '') + ':<br><a class="fn-bt" href="mailto:' + correo + '?subject=' + encodeURIComponent('¿Qué filtro necesita mi nevecón?') + '&body=' + encodeURIComponent(t) + '">✉ Escribir por correo</a>' : 'Escríbenos al correo de la tienda y una persona te responde.', 'bot'); return; }
    msg('Con gusto. Toca el botón y te contesta una persona por WhatsApp' + (txt ? ' (ya va escrito tu modelo)' : '') + ':<br><a class="fn-bt wa" target="_blank" rel="noopener" href="https://wa.me/' + wa + '?text=' + encodeURIComponent(t) + '">💬 Escribir por WhatsApp</a>', 'bot');
  }
  function tarjeta(p, motivo) {
    ev('recomienda', p.ref);
    return motivo + '<br><br><b>' + esc(p.n) + '</b><br><span class="fn-pr">' + cop(p.p) + '</span>' + (INFO.guiado ? '' : ' · envío gratis a toda Colombia') + '<br>' + (p.i ? '<button type="button" class="fn-bt" data-add="' + p.i + '">🛒 Agregar al carrito</button>' : '') + '<a class="fn-bt" href="' + p.u + '">' + (p.i ? 'Ver ficha' : 'Ver y comprar') + '</a>';
  }
  function buscar(q) {
    var t = n(q); if (t.length < 3) return null;
    var exacto = [], ref = [], parecido = [];
    D.forEach(function (p) {
      if (p.m.some(function (m) { return n(m) === t; })) exacto.push([p, 'modelo']);
      else if (n(p.r) === t || p.a.some(function (a) { return n(a) === t; })) ref.push(p);
      else if (t.length >= 6 && p.m.some(function (m) { var k = n(m); return k.indexOf(t) === 0 || t.indexOf(k) === 0; })) parecido.push(p);
    });
    return {exacto: exacto, ref: ref, parecido: parecido};
  }
  function responder(q) {
    var t = n(q);
    var e = t.match(/EDR([1-5])/) || (/EVERYDROP/i.test(q) && String(q).match(/([1-5])/));
    var r = buscar(q);
    if (r && r.exacto.length) { var p = r.exacto[0][0]; msg(tarjeta(p, 'Tu nevecón <b>' + esc(String(q).trim().toUpperCase()) + '</b> usa este filtro:'), 'bot'); chips([['Buscar otro modelo', function () { I.focus(); }], [wa || !correo ? 'Hablar con una persona' : 'Escribir por correo', persona]]); return; }
    if (r && r.ref.length) { var p2 = r.ref[0]; msg(tarjeta(p2, 'Esa referencia equivale a este filtro:'), 'bot'); chips([['Buscar otro modelo', function () { I.focus(); }]]); return; }
    if (r && r.parecido.length) { var p3 = r.parecido[0]; msg(tarjeta(p3, 'No tengo ese modelo exacto, pero uno muy parecido usa este filtro. <b>Confírmalo con la etiqueta de tu nevecón</b> o con una persona:'), 'bot'); chips([[wa || !correo ? 'Hablar con una persona' : 'Escribir por correo', function () { persona(q); }], ['Buscar otro modelo', function () { I.focus(); }]]); return; }
    if (e) { var h = D.filter(function (p) { return n(p.r).indexOf('EDR' + e[1]) === 0; })[0]; if (h) { msg(tarjeta(h, 'Ese es el <b>EveryDrop ' + e[1] + '</b>:'), 'bot'); return; } }
    msg('No encontré <b>' + esc(String(q).trim()) + '</b> en mi lista. Revisa que esté bien escrito (sin espacios) o mira la etiqueta del refrigerador. Si quieres, una persona lo revisa contigo' + (wa ? ' por WhatsApp.' : ' por correo.') + '', 'bot');
    chips([[wa || !correo ? 'Hablar con una persona' : 'Escribir por correo', function () { persona(q); }], ['¿Dónde está el modelo?', donde]]);
  }
  function abrir() {
    abierto = !abierto; w.classList.toggle('on', abierto); b.setAttribute('aria-expanded', abierto);
    if (abierto) { ev('abrir'); if (!saludo) { saludo = true; msg(INFO.guiado ? '¡Hola! 👋 Soy el <b>asistente de filtros</b>' + (INFO.ciudad ? ' de ' + esc(INFO.ciudad) : '') + '. Te ayudo a escoger el filtro de tu nevecón Samsung en un minuto. ¿Cómo prefieres?' : '¡Hola! 👋 Soy el asistente de la tienda. Escríbeme el <b>modelo de tu nevecón</b> o la <b>referencia del filtro viejo</b> y te digo cuál filtro es. Funciono las 24 horas; si prefieres, te paso con una persona' + (wa ? ' por WhatsApp.' : ' por correo.') + '', 'bot'); menuBase(); } setTimeout(function () { I.focus(); }, 50); }
  }
  // Buscador del encabezado y de la portada: sugerencias por modelo o referencia; si no hay coincidencia, lo contesta el asistente
  function sugerir(q) {
    var t = n(q), r = [];
    if (t.length < 3) return r;
    D.forEach(function (p) {
      var hit = p.m.filter(function (m) { return n(m).indexOf(t) === 0 || (t.length >= 4 && n(m).indexOf(t) > -1); })[0];
      if (!hit && (n(p.r).indexOf(t) > -1 || p.a.some(function (a) { return n(a).indexOf(t) > -1; }))) hit = p.r;
      if (!hit && t.length >= 3 && n(p.n).indexOf(t) > -1) hit = p.r;
      if (hit) r.push({p: p, t: hit});
    });
    return r.slice(0, 6);
  }
  document.querySelectorAll('form[data-buscador]').forEach(function (f) {
    var i = f.querySelector('input'), s = f.querySelector('.m-sug');
    function pintar() {
      var r = sugerir(i.value);
      if (i.value.trim().length < 3) { s.classList.remove('on'); s.innerHTML = ''; return; }
      s.innerHTML = r.length ? r.map(function (x) { return '<a href="' + x.p.u + '"><span>' + esc(x.t) + ' → ' + esc(x.p.r) + '</span><small>' + cop(x.p.p) + '</small></a>'; }).join('')
        : '<div class="m-nada">No lo encuentro en la lista. Toca Enter y te ayuda el asistente.</div>';
      s.classList.add('on');
    }
    i.addEventListener('input', pintar);
    i.addEventListener('focus', pintar);
    document.addEventListener('click', function (e) { if (!f.contains(e.target)) s.classList.remove('on'); });
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var q = i.value.trim(); if (!q) return;
      var r = sugerir(q);
      ev('buscador', q.slice(0, 40));
      if (r.length === 1) { location.href = r[0].p.u; return; }
      if (!abierto) abrir();
      i.value = ''; s.classList.remove('on');
      msg(esc(q), 'yo'); setTimeout(function () { responder(q); }, 300);
    });
  });
  b.onclick = abrir; w.querySelector('header button').onclick = abrir;
  w.querySelector('#fn-f').onsubmit = function (x) { x.preventDefault(); var q = I.value.trim(); if (!q) return; I.value = ''; msg(esc(q), 'yo'); ev('busca', q.slice(0, 40)); setTimeout(function () { responder(q); }, 350); };
})();
"""


def generar(productos, url, correo='', info=None):
    """productos: lista del catálogo; url(p) -> enlace de la página del producto."""
    forma = {"DA29-00020B": "redondo", "DA97-17376B": "cuadrado", "DA29-10105J": "externo"}
    datos = [{"n": p["nombre_largo"] + "", "r": p["ref"], "p": p["precio"], "u": url(p), "a": [x for x in p["refs"] if x != p["ref"]], "m": p["modelos"],
              **({"i": p["id"], "f": forma.get(p["ref"], "")} if info and info.get("guiado") else {})} for p in productos]
    return (JS.replace("__DATOS__", json.dumps(datos, ensure_ascii=False, separators=(",", ":"))).replace("__CORREO__", correo)
            .replace("__INFO__", json.dumps(info or {}, ensure_ascii=False, separators=(",", ":"))))
