<?php
// Piezas comunes de la tienda de bombas para lavadoras (generado por bombas.py)
require_once __DIR__ . '/marcas.php';
$MARCA = preg_replace('/[^a-z]/', '', (string) ($MARCA ?? 'home'));
$M = json_decode(file_get_contents(__DIR__ . "/marca-$MARCA.json"), true);
function lav_cabeza(string $titulo, string $desc, string $ruta, string $extra, string $json): void
{
    global $M;
    $ld = $json !== '' ? '<script type="application/ld+json">' . str_replace('__BASE__', sitio()['base'], $json) . '</script>' : '';
    cabeza_marca($M, $titulo, $desc, $ruta, $extra . $ld . lav_evento_whatsapp());
}
function lav_pie(): void { global $M; pie_marca($M); }
// Evento para Google Tag Manager: «whatsapp» al tocar cualquier enlace de WhatsApp
function lav_evento_whatsapp(): string
{
    global $M;
    return '<script>window.dataLayer=window.dataLayer||[];document.addEventListener("click",function(e){var a=e.target.closest(\'a[href*="wa.me/"]\');if(a){dataLayer.push({event:"whatsapp",ubicacion:a.classList.contains("wa-flot")?"boton_flotante":"enlace",boton:(a.textContent||"").trim().slice(0,60),pagina:location.pathname,marca:' . json_encode($M['nombre']) . '})}},true);</script>';
}
