#!/usr/bin/env python3
"""Agrega la tienda de instalación (Cali, Jamundí, Yumbo, Palmira) a un public_html ya armado.
Uso: python3 armar_instalacion.py <carpeta_public_html> [clave_admin]"""
import re, shutil, sys
from pathlib import Path
AQUI = Path(__file__).parent
pub = Path(sys.argv[1])
clave_admin = sys.argv[2] if len(sys.argv) > 2 else ""
for f in (AQUI / "api").glob("*.php"): shutil.copy(f, pub / "filtrosnevecones-api" / f.name)
shutil.copy(AQUI / "web" / "admin-instalaciones.php", pub / "admin-instalaciones.php")
shutil.copytree(AQUI / "web" / "instalacion-nevecon-cali", pub / "instalacion-nevecon-cali", dirs_exist_ok=True)

def rep(path, a, b):
    s = path.read_text(encoding="utf-8"); assert a in s, (path, a[:70]); path.write_text(s.replace(a, b, 1), encoding="utf-8")
p = pub / "partes.php"
s = p.read_text(encoding="utf-8")
if "instalacion-nevecon-cali" not in s:
    rep(p, '<a href="/kits-instalacion-nevecones/">Kits</a>', '<a href="/kits-instalacion-nevecones/">Kits</a><a href="/instalacion-nevecon-cali/">Instalación en Cali</a>')
    rep(p, '<a href="/kits-instalacion-nevecones/">Kits de instalación del nevecón</a>', '<a href="/kits-instalacion-nevecones/">Kits de instalación del nevecón</a><a href="/instalacion-nevecon-cali/">Instalación a domicilio en Cali</a>')
# sitemap: la tienda de kits y la de instalación
sm = pub / "sitemap.php"
t = sm.read_text(encoding="utf-8")
if "instalacion-nevecon-cali" not in t:
    linea = "$urls['/kits-instalacion-nevecones/'] = '0.9'; $urls['/instalacion-nevecon-cali/'] = '0.9';\nforeach (glob(__DIR__ . '/kits-instalacion-nevecones/*/index.php') ?: [] as $f) $urls['/kits-instalacion-nevecones/' . basename(dirname($f)) . '/'] = '0.8';\n"
    marca = "echo '<?xml version"
    assert marca in t; sm.write_text(t.replace(marca, linea + marca, 1), encoding="utf-8")
# ajustes
a = pub / "filtrosnevecones-api" / "ajustes.php"; t = a.read_text(encoding="utf-8")
if "'instalacion'" not in t:
    bloque = """
    // Clave para entrar a tudominio.com/admin-instalaciones.php (panel de reservas de instalación) y a /admin.php
    'admin_clave' => '%s',

    // Instalación a domicilio: pega aquí los 4 links de pago de Wompi de la RESERVA (uno por servicio). Los precios están en instalacion-lib.php.
    // 'bloqueados' = fechas sin servicio, por ejemplo ['2026-12-08', '2026-12-25'].
    'instalacion' => [
        'links' => ['basica' => '', 'filtro-samsung' => '', 'filtro-lg' => '', 'filtro-whirlpool' => ''],
        'bloqueados' => [],
    ],
""" % clave_admin
    i = t.rindex("];"); t = t[:i] + bloque + t[i:]; a.write_text(t, encoding="utf-8")
print("instalación agregada a", pub)
