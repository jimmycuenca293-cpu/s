#!/usr/bin/env python3
"""Arma el public_html completo: tienda de filtros (del zip subido) + arreglo de correos/WhatsApp + tienda de kits con la misma estructura.
Uso: python3 armar_public_html.py <public_html_13.zip> <salida.zip>
No incluye config.php ni pedidos.sqlite: se conservan los del servidor."""
import re, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path
AQUI = Path(__file__).parent
ARREGLO = AQUI.parent / "filtrosnevecones-arreglo"
zin, zout = Path(sys.argv[1]), Path(sys.argv[2])
t = Path(tempfile.mkdtemp()); b = t / "pub"
zipfile.ZipFile(zin).extractall(b)
for f in list((b / "filtrosnevecones-data").glob("pedidos.sqlite*")): f.unlink()
shutil.copytree(ARREGLO / "filtrosnevecones-api", b / "filtrosnevecones-api", dirs_exist_ok=True)
shutil.copy(ARREGLO / "index.php", b / "index.php")

def rep(path, a, c, veces=1):
    s = path.read_text(encoding="utf-8"); assert a in s, (path, a[:60]); path.write_text(s.replace(a, c, veces), encoding="utf-8")

p = b / "partes.php"
rep(p, '<a href="/filtrosnevecones-instalacion/">Cómo instalar tu filtro</a>', '<a href="/filtrosnevecones-instalacion/">Cómo instalar tu filtro</a><a href="/kits-instalacion-nevecones/">Kits de instalación del nevecón</a>')
rep(p, '<nav class="topnav"><a href="/filtrosnevecones-tienda/">Tienda</a>', '<nav class="topnav"><a href="/filtrosnevecones-tienda/">Tienda</a><a href="/kits-instalacion-nevecones/">Kits</a>')
# celulares angostos: el menú de arriba pasa a una segunda fila en vez de encimarse con el logo
css = b / "filtrosnevecones-estilo.css"
css.write_text(css.read_text(encoding="utf-8") + '\n/* ===== encabezado y pasarela: versión celular ===== */\n.tn-links{display:flex;align-items:center;gap:4px}\n.tn-links>a{color:#dfeeea;text-decoration:none;font-weight:600;font-size:15px;padding:8px 12px;border-radius:10px;transition:background .15s,color .15s}\n.tn-links>a:hover{background:rgba(255,255,255,.08);color:#fff}\nbody{overflow-x:clip}\n@media (max-width:760px){\n  header.top .wrap{display:flex;flex-wrap:wrap;align-items:center;gap:8px 10px;padding-block:10px}\n  header.top .logo{order:1;flex:1 1 auto;min-width:0}\n  header.top .logo .lg-t{font-size:18px}\n  header.top .topnav{display:contents}\n  header.top .cartbtn{order:2;margin:0 0 0 auto;flex:0 0 auto}\n  header.top .tn-links{order:3;flex:1 0 100%;gap:8px;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none;padding:2px 0 4px}\n  header.top .tn-links::-webkit-scrollbar{display:none}\n  header.top .tn-links>a,header.top .tn-links .marcas-nav a{flex:0 0 auto;white-space:nowrap;background:rgba(255,255,255,.12);border-radius:999px;padding:8px 15px;font-size:14px;font-weight:700;color:#fff}\n  header.top .tn-links .marcas-nav{display:contents!important}\n  header.top .tn-links .solo-ancho{display:inline-flex!important}\n  header.top .tn-links .marcas-nav.solo-ancho{display:contents!important}\n}\n/* pasarela de pago (carrito) */\n.seguro-tira{display:flex;flex-wrap:wrap;gap:6px 16px;margin:-4px 0 4px;font-size:13.5px;font-weight:700;color:#1d7a46}\n@media (max-width:760px){.seguro-tira{flex-wrap:nowrap;overflow-x:auto;gap:14px;font-size:12.5px;scrollbar-width:none}.seguro-tira::-webkit-scrollbar{display:none}.seguro-tira span{white-space:nowrap}}\n.checkout .caja.paso,.checkout .resumen{box-shadow:0 8px 26px rgba(11,31,107,.08);border-radius:18px}\n.checkout input,.checkout select{min-height:48px;font-size:16px;border-radius:12px}\n.checkout label>span{font-weight:700}\n.checkout input:focus,.checkout select:focus{outline:3px solid rgba(26,92,255,.28);outline-offset:1px}\n@media (min-width:761px){.checkout .resumen{position:sticky;top:92px}}\n.nota-envio{margin:8px 0 0;font-size:13px;color:#566287}\n.paybar{position:fixed;left:0;right:0;bottom:0;z-index:40;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:10px max(16px,env(safe-area-inset-right,0px)) calc(10px + env(safe-area-inset-bottom,0px)) max(16px,env(safe-area-inset-left,0px));background:#fff;border-top:1px solid #d9e2fa;box-shadow:0 -8px 24px rgba(11,31,107,.12)}\n.paybar[hidden]{display:none}\n.paybar .pb-t{display:flex;flex-direction:column;line-height:1.15}.paybar small{font-size:12px;color:#566287}.paybar b{font-size:20px;color:#0b1a45}\n.paybar .btn{flex:0 0 52%;min-height:50px;font-size:16px}\n.con-paybar .wa-flot{bottom:calc(84px + env(safe-area-inset-bottom,0px))}\n.con-paybar main{padding-bottom:90px}\n', encoding="utf-8")
l = b / "filtrosnevecones-api" / "lib.php"
rep(l, "function calcular_items(array $items): array\n{\n    $cat = catalogo()['productos'];",
    "// Productos que se pueden comprar: filtros + kits de instalación (catalogo-kits.php)\nfunction productos_compra(): array\n{\n    static $p = null;\n    if ($p === null) { $f = __DIR__ . '/catalogo-kits.php'; $p = catalogo()['productos'] + (is_file($f) ? require $f : []); }\n    return $p;\n}\n\nfunction calcular_items(array $items): array\n{\n    $cat = productos_compra();")
rep(l, "    if ($entrega !== 'instalacion') return 0;\n    $cat = catalogo()['productos'];", "    if ($entrega !== 'instalacion') return 0;\n    $cat = productos_compra();")
c = b / "carrito.php"
rep(c, "'slug' => $p['slug'], 'ubic' => $p['ubic']], $cat['productos'])", "'slug' => $p['slug'], 'ubic' => $p['ubic'], 'url' => $p['url'] ?? ''], productos_compra())")
rep(c, 'href="/filtrosnevecones-filtro/${p.slug}/"><b>', 'href="${p.url || \'/filtrosnevecones-filtro/\' + p.slug + \'/\'}"><b>')
rep(c, 'href="/filtrosnevecones-filtro/${p.slug}/"', 'href="${p.url || \'/filtrosnevecones-filtro/\' + p.slug + \'/\'}"')
rep(c, "${!l.pack ? `<button type=\"button\" class=\"link\" data-topack", "${!l.pack && p.pack ? `<button type=\"button\" class=\"link\" data-topack")
rep(c, '$("#totales").innerHTML = `<div class="tl"><span>${n} ${n === 1 ? "filtro" : "filtros"}</span>',
    '$("#c-rec").closest("label").hidden = L.every(l => P[l.pid].ubic === "kit");\n    const solo = L.every(l => P[l.pid].ubic === "kit");\n    $("#totales").innerHTML = `<div class="tl"><span>${n} ${solo ? (n === 1 ? "producto" : "productos") : (n === 1 ? "filtro" : "filtros")}</span>')
# pasarela (carrito.php): más clara y fácil en celular, con barra de pago fija abajo
rep(c, '<h1>Tu carrito</h1>', '<h1>Tu carrito</h1>\n<div class="seguro-tira"><span>🔒 Pago seguro con Wompi</span><span>🚚 Envío gratis a toda Colombia</span><span>📦 Llega en 2 a 3 días hábiles</span></div>')
rep(c, '<input id="c-barrio" maxlength="80"', '<input id="c-barrio" autocomplete="address-level3" enterkeyhint="next" maxlength="80"')
rep(c, '<button class="btn block" type="button" id="pagar">Pagar</button>', '<button class="btn block" type="button" id="pagar">Pagar</button>\n      <p class="m nota-envio">Al pagar recibes el recibo y el número de guía en tu correo. Tus datos solo se usan para el envío.</p>')
rep(c, '<?php pie(); ?>', '''<div class="paybar" id="paybar" hidden><div class="pb-t"><small>Total a pagar</small><b id="pb-total"></b></div><button type="button" class="btn" id="pb-btn">Pagar</button></div>
<script>
(function(){
  var bar=document.getElementById("paybar"),co=document.getElementById("checkout"),real=document.getElementById("pagar"),tot=document.getElementById("totales"),inView=false;
  function txt(){var t=tot.querySelector(".total span:last-child");document.getElementById("pb-total").textContent=t?t.textContent:"";}
  function vis(){var s=!co.hidden&&window.matchMedia("(max-width:760px)").matches&&!inView;bar.hidden=!s;document.body.classList.toggle("con-paybar",s);}
  if("IntersectionObserver" in window)new IntersectionObserver(function(e){inView=e[0].isIntersecting;vis();}).observe(real);
  new MutationObserver(function(){txt();vis();}).observe(tot,{childList:true,subtree:true});
  new MutationObserver(vis).observe(co,{attributes:true,attributeFilter:["hidden"]});
  document.getElementById("pb-btn").addEventListener("click",function(){real.click();});
  window.addEventListener("resize",vis);txt();vis();
})();
</script>
<?php pie(); ?>''')
# pedido.php: los links de pago por producto también valen para los kits
pe = b / "filtrosnevecones-api" / "pedido.php"
rep(pe, "$link = (count($C['lineas']) === 1 && $C['unidades'] === 1) ? (string) ($cat['productos'][$l0['pid']]['link_pago'] ?? '') : '';", "$link = (count($C['lineas']) === 1 && $C['unidades'] === 1) ? (string) (productos_compra()[$l0['pid']]['link_pago'] ?? '') : '';")
rep(pe, "empty($cat['productos'][$l0['pid']]['link_pago'])", "empty(productos_compra()[$l0['pid']]['link_pago'])")
rep(pe, "'Por ahora el pago en línea es de un filtro a la vez. Deja una sola unidad en el carrito.'", "'Por ahora el pago en línea es de un producto a la vez. Deja solo uno en el carrito, págalo y luego compra el siguiente. (Si pones las llaves de Wompi, puedes pagar varios juntos.)'")
rep(pe, "'Este filtro todavía no tiene pago en línea.", "'Este producto todavía no tiene pago en línea.")
rep(c, '<h2><span class="np">4</span>Resumen y pago</h2>', '<h2>Resumen de tu pedido</h2>')
# link de pago (sin llaves de Wompi): con varios productos se paga uno a la vez, y el carrito conserva el resto
rep(c, '$("#pagar").textContent = `Pagar ${cop(t)}`;', '$("#pagar").textContent = `Pagar ${cop(t)}`;\n' + r"""    if (C.pago_link && (L.length > 1 || L[0].cant > 1)) {
      const l0 = L[0], p0 = P[l0.pid], u0 = l0.pack ? p0.pack : p0.precio, resto = total() - u0;
      $("#totales").innerHTML = `<div class="tl"><span>Pagas ahora</span><span>${cop(u0)}</span></div><div class="tl"><span>Envío</span><span class="gratis">Gratis</span></div><div class="tl total"><span>Total de este pago</span><span>${cop(u0)}</span></div><div class="note info" style="margin-top:8px">Hoy el pago en línea es de un producto a la vez. Pagas <b>${esc(p0.nombre)}</b> y después vuelves al carrito por lo demás (quedan ${cop(resto)}).</div>`;
      $("#pagar").textContent = `Pagar ${cop(u0)}`;
    }""")
rep(c, 'const L = lineas(), t = total() + (C.pago_link ? 0 : instalacion());', 'const L0 = lineas(), sec = C.pago_link && (L0.length > 1 || L0[0].cant > 1);\n      const L = sec ? [{ pid: L0[0].pid, pack: L0[0].pack, cant: 1 }] : L0;\n      const t = sec ? (L0[0].pack ? P[L0[0].pid].pack : P[L0[0].pid].precio) : total() + (C.pago_link ? 0 : instalacion());')
rep(c, 'ls.set("fy_orders", o.slice(0, 50));', 'ls.set("fy_orders", o.slice(0, 50));\n      if (sec) { const c2 = lineas(); if (c2[0].cant > 1) c2[0].cant--; else c2.splice(0, 1); FYCart.guardar(c2); }')
# mejoras de la tienda (animaciones, barra de compra, fecha de entrega, vistos recientemente, zoom): un archivo nuevo cargado junto al del carrito
shutil.copy(AQUI / "filtrosnevecones-mejoras.js", b / "filtrosnevecones-mejoras.js")
_cj = '<script src="/filtrosnevecones-carrito.js" defer></script>'
for _f in ("partes.php", "index.php", "filtrosnevecones-marcas.php"):
    rep(b / _f, _cj, _cj + '<script src="/filtrosnevecones-mejoras.js" defer></script>')

# menú: los enlaces van dentro de .tn-links (en celular quedan en una fila deslizable) y el carrito junto al logo
_p = b / "partes.php"; _t = _p.read_text(encoding="utf-8")
_t, _n1 = re.subn(r"<nav class=\"topnav\">", '<nav class="topnav"><div class="tn-links">', _t, count=1)
_t, _n2 = re.subn(r"(Guías</a>')(\s*\. '<a class=\"cartbtn\")", lambda m: "Guías</a></div>'" + m.group(2), _t, count=1)
assert _n1 == 1 and _n2 == 1, (_n1, _n2)
_p.write_text(_t, encoding="utf-8")
# cada vez que cambie un archivo de estilo o de scripts se sube la versión: así los celulares no usan la copia vieja guardada
VER = "20261028c"
for _f in ("partes.php", "filtrosnevecones-marcas.php", "index.php"):
    _x = (b / _f).read_text(encoding="utf-8")
    _x = _x.replace('href="/filtrosnevecones-estilo.css"', f'href="/filtrosnevecones-estilo.css?v={VER}"').replace('src="/filtrosnevecones-mejoras.js"', f'src="/filtrosnevecones-mejoras.js?v={VER}"')
    (b / _f).write_text(_x, encoding="utf-8")
subprocess.run([sys.executable, str(AQUI / "kits_php.py"), str(t / "overlay"), str(b / "index.php")], check=True)
shutil.copytree(t / "overlay", b, dirs_exist_ok=True)
_k = b / "kits-instalacion-nevecones" / "index.php"; _k.write_text(_k.read_text(encoding="utf-8").replace('src="/filtrosnevecones-mejoras.js"', f'src="/filtrosnevecones-mejoras.js?v={VER}"'), encoding="utf-8")
# portada de la tienda de filtros: se avisa que también hay kits (sin tocar nada más)
bh = (t / "overlay" / "_bloque-home.html").read_text(encoding="utf-8"); (b / "_bloque-home.html").unlink(missing_ok=True)
ix = b / "index.php"
# los filtros siguen primero: los kits van DEBAJO del catálogo de filtros, y en «Explora la tienda» hay un acceso directo
rep(ix, '<div class="grid" id="grid"></div>', '<div class="grid" id="grid"></div>\n' + bh)
rep(ix, '<a href="/filtrosnevecones-tienda/"><b>🛒 Tienda</b>', '<a href="/kits-instalacion-nevecones/"><b>🔧 Kits de instalación</b><span>Manguera, llaves, acoples y combos</span></a>\n<a href="/filtrosnevecones-tienda/"><b>🛒 Tienda</b>')
rep(ix, '<nav class="hero-nav"><a href="/filtrosnevecones-tienda/">Tienda</a>', '<nav class="hero-nav"><a href="/filtrosnevecones-tienda/">Tienda</a><a href="/kits-instalacion-nevecones/">Kits</a>')
(b / "filtrosnevecones-api" / "hoja-de-pedidos-google.txt").write_text(open(AQUI / "hoja-de-pedidos-google.txt", encoding="utf-8").read(), encoding="utf-8")
(b / "LEEME-SUBIR.txt").write_text(open(AQUI / "LEEME-SUBIR.txt", encoding="utf-8").read(), encoding="utf-8")
if zout.exists(): zout.unlink()
with zipfile.ZipFile(zout, "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(b.rglob("*")):
        if f.is_file(): z.write(f, f.relative_to(b))
print("listo", zout, sum(1 for _ in b.rglob("*") if _.is_file()), "archivos")
shutil.copytree(b, Path(sys.argv[3]), dirs_exist_ok=True) if len(sys.argv) > 3 else None
