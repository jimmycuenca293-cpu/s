#!/usr/bin/env python3
"""Arma el public_html completo: tienda de filtros (del zip subido) + arreglo de correos/WhatsApp + tienda de kits con la misma estructura.
Uso: python3 armar_public_html.py <public_html_13.zip> <salida.zip>
No incluye config.php ni pedidos.sqlite: se conservan los del servidor."""
import shutil, subprocess, sys, tempfile, zipfile
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
rep(p, '<nav class="topnav"><a href="/filtrosnevecones-tienda/">Tienda</a>', '<nav class="topnav"><a href="/filtrosnevecones-tienda/">Tienda</a><a href="/kits-instalacion-nevecones/">Kits de instalación</a>')
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
subprocess.run([sys.executable, str(AQUI / "kits_php.py"), str(t / "overlay"), str(b / "index.php")], check=True)
shutil.copytree(t / "overlay", b, dirs_exist_ok=True)
(b / "LEEME-SUBIR.txt").write_text(open(AQUI / "LEEME-SUBIR.txt", encoding="utf-8").read(), encoding="utf-8")
if zout.exists(): zout.unlink()
with zipfile.ZipFile(zout, "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(b.rglob("*")):
        if f.is_file(): z.write(f, f.relative_to(b))
print("listo", zout, sum(1 for _ in b.rglob("*") if _.is_file()), "archivos")
shutil.copytree(b, Path(sys.argv[3]), dirs_exist_ok=True) if len(sys.argv) > 3 else None
