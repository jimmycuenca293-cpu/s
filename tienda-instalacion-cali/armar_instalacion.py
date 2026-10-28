#!/usr/bin/env python3
"""Arma el paquete de la instalación (Cali, Jamundí, Yumbo, Palmira): SOLO archivos nuevos, no toca ningún archivo de la tienda principal.
Uso: python3 armar_instalacion.py <carpeta_salida> <clave_panel> [url_basica url_samsung url_lg url_whirlpool]"""
import shutil, sys
from pathlib import Path
AQUI = Path(__file__).parent
out = Path(sys.argv[1]); clave = sys.argv[2]; links = (sys.argv[3:7] + ["", "", "", ""])[:4]
if out.exists(): shutil.rmtree(out)
(out / "filtrosnevecones-api").mkdir(parents=True)
for f in (AQUI / "api").glob("*.php"): shutil.copy(f, out / "filtrosnevecones-api" / f.name)
shutil.copy(AQUI / "web" / "admin-instalaciones.php", out / "admin-instalaciones.php")
shutil.copytree(AQUI / "web" / "instalacion-nevecon-cali", out / "instalacion-nevecon-cali")
(out / "filtrosnevecones-api" / "instalacion-ajustes.php").write_text("""<?php
// Ajustes de la instalación a domicilio. Se edita solo este archivo.
return [
    // Clave para entrar al panel: tudominio.com/admin-instalaciones.php
    'clave_panel' => '%s',
    // Links de pago de Wompi de la RESERVA (uno por servicio). Mientras estén vacíos, la página le pide al cliente pagar por WhatsApp.
    'links' => [
        'basica' => '%s',            // reserva $60.000
        'filtro-samsung' => '%s',    // reserva $90.000
        'filtro-lg' => '%s',         // reserva $90.000
        'filtro-whirlpool' => '%s',  // reserva $100.000
    ],
    // Fechas sin servicio, por ejemplo ['2026-12-08', '2026-12-25'].
    'bloqueados' => [],
];
""" % (clave, *links), encoding="utf-8")
print("paquete en", out)
