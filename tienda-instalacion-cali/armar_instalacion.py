#!/usr/bin/env python3
"""Arma el paquete de la instalación (Cali, Jamundí, Yumbo, Palmira): SOLO archivos nuevos, no toca ningún archivo de la tienda principal.
Uso: python3 armar_instalacion.py <carpeta_salida> <clave_panel> [4 links de reserva] [8 links de pago total: basica-cali basica-jamundi samsung-cali samsung-jamundi lg-cali lg-jamundi whirlpool-cali whirlpool-jamundi]"""
import shutil, sys
from pathlib import Path
AQUI = Path(__file__).parent
out = Path(sys.argv[1]); clave = sys.argv[2]; links = (sys.argv[3:7] + [""] * 4)[:4]
tot = (sys.argv[7:15] + [""] * 8)[:8]
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
    // Links de pago de Wompi por el TOTAL (uno por servicio y zona). Si un link está vacío, la página le pide al cliente el link por WhatsApp.
    'links_total' => [
        'basica' => ['cali' => '%s', 'jamundi' => '%s'],             // $137.900 / $157.900
        'filtro-samsung' => ['cali' => '%s', 'jamundi' => '%s'],     // $169.900 / $189.900
        'filtro-lg' => ['cali' => '%s', 'jamundi' => '%s'],          // $169.900 / $189.900
        'filtro-whirlpool' => ['cali' => '%s', 'jamundi' => '%s'],   // $179.900 / $199.900
    ],
    // Fechas sin servicio, por ejemplo ['2026-12-08', '2026-12-25'].
    'bloqueados' => [],
];
""" % (clave, *links, *tot), encoding="utf-8")
print("paquete en", out)
