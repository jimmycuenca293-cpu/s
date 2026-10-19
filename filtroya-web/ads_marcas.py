#!/usr/bin/env python3
"""Páginas de Google Ads por marca: pago contra entrega, sin precios y sin logos de las marcas.

Quedan en las MISMAS direcciones de la tienda de filtrosdeaguanevecon.com para no tocar los anuncios:
  /purofiltro-marca/<marca>/        portada de la marca (la que usan los anuncios)
  /purofiltro-filtro/<filtro>/      una página por referencia, con cuándo cambiarlo, la alerta del display y la instalación
  /purofiltro-contraentrega/        términos y datos del pago contra entrega
  /purofiltro-img/                  las fotos (mismos nombres que en la tienda)

Cada página es un archivo estático (index.html y una copia index.php, para pisar la página vieja sin tocar nada más).
El pedido se hace por WhatsApp: cada marca tiene su número. Evento «whatsapp» y etiqueta de Google Tag Manager,
verificación de Search Console y canónica con el dominio real.

Uso:  python3 build.py   (deja las fotos en public_html/)   y luego   python3 ads_marcas.py
Sale: sitios-ads/ y anuncios-contra-entrega.zip (se descomprime en public_html de Hostinger).
"""
import html
import json
import pathlib
import re
import shutil
import subprocess
import sys
import unicodedata
from urllib.parse import quote

import instalacion
import marcas_exclusivas

AQUI = pathlib.Path(__file__).resolve().parent
APP = (AQUI.parent / "filtros-app" / "index.html").read_text(encoding="utf-8")
FOTOS = AQUI / "public_html" / "purofiltro-img"
SALIDA = AQUI / "sitios-ads"

# ---------- lo que cambia el dueño ----------
BASE = "https://filtrosdeaguanevecon.com"
NEGOCIO = "Filtros de Agua Nevecón"       # nombre que ve el cliente (sin marcas registradas)
HORARIO = "Lunes a sábado, 8:00 a. m. a 6:00 p. m."
GTM = "GTM-N39G66VJ"                      # el mismo contenedor de la tienda; evento «whatsapp» al tocar cualquier botón de WhatsApp
VERIFICACION = "HN_wbFxOz4Yeyfr0Oao1VfSO6mPB_I4k_uMqoVR5jZo"   # Search Console (etiqueta HTML)
ENVIO_GRATIS = True                       # False si el envío contra entrega lo paga el cliente
MARCAS = {  # número de WhatsApp de cada marca (10 dígitos, sin +57)
    "Samsung": {"whatsapp": "3054796329", "fuente": "Plus Jakarta Sans", "pri": "#1428a0", "pri2": "#0a1460", "acento": "#a9b8ff", "suave": "#e8ecfb", "gris": "#545c78",
                "display": ("Replace Filter", "Cambiar filtro"),
                "lineas": "French door, side by side, Bespoke y Family Hub", "etiqueta": "dentro de la nevera, en una pared lateral o en el techo; empieza por RF, RS o RH"},
    "LG": {"whatsapp": "3205102995", "fuente": "Outfit", "pri": "#a50034", "pri2": "#4f4f53", "acento": "#ff9bb8", "suave": "#fbe8ee", "gris": "#6b6b6b",
           "display": ("Replace Filter", "Cambiar filtro"),
           "lineas": "French door, side by side e InstaView", "etiqueta": "dentro de la nevera, en la pared lateral o detrás del cajón de las verduras; empieza por LF, LM, LR, LS o GR"},
    "Whirlpool": {"whatsapp": "3107147299", "fuente": "DM Sans", "pri": "#2b2724", "pri2": "#141211", "acento": "#eeb111", "suave": "#fcefc9", "gris": "#5f5b58",
                  "eye": "#8a6400", "chip": "#eeb111", "chip_ink": "#231f20", "gota": "#eeb111", "subrayado": "#eeb111",
                  "display": ("Order  →  Replace", "Pide el filtro  →  cámbialo"),
                  "lineas": "French door, side by side y congelador abajo", "etiqueta": "dentro de la nevera, en la pared lateral de arriba; empieza por WRF, WRS o WRX"},
    "GE": {"whatsapp": "3107147299", "fuente": "Lexend", "pri": "#3b73b9", "pri2": "#1d3f6e", "acento": "#cfe2ff", "suave": "#e2ecf8", "gris": "#5a6b80",
           "display": ("Replace Filter", "Cambiar filtro"),
           "lineas": "French door y side by side", "etiqueta": "dentro de la nevera, en la pared lateral o en el techo; empieza por GFE, GNE, GSS, PFE, PYE o CFE"},
}

esc = lambda s: html.escape(str(s), quote=True)
norm = lambda s: re.sub(r"[^A-Z0-9]", "", s.upper())


def slug(s):
    s = unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def js(expr_var):
    m = re.search(r"\nconst " + expr_var + r" = (\[.*?\n\]|\[[^\n]*\]);", APP, re.S)
    r = subprocess.run(["node", "-e", f"process.stdout.write(JSON.stringify({m.group(1)}))"], capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


def catalogo():
    cat = js("CATALOGO")
    for p in cat:  # mismo nombre y misma dirección que en la tienda (build.py)
        p["largo"] = p["nombre"] if norm(p["ref"]) in norm(p["nombre"]) else f'{p["nombre"]} {p["ref"]}'
        p["slug"] = slug(p["largo"])
        p["externo"] = "-ex-" in p["id"]
        p["datos"] = instalacion.datos(p)
    return cat


def ciudades():
    return [(c[0], c[1]) for c in js("CIUDADES_CO")]


def wa(numero, texto):
    return f"https://wa.me/57{numero}?text={quote(texto)}"


def json_ld(obj):
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")


# fotos del dueño (imagenes-ads/): se publican en /purofiltro-img/ con WebP liviano y JPG de respaldo
IMAGENES = {
    "alerta": ("alerta-display", "ads-alerta-display", "Pantalla del nevecón con la alerta «Cambiar filtro» encendida"),
    "agua": ("agua-dispensador", "ads-agua-dispensador", "Hombre sirviéndose un vaso de agua del dispensador del nevecón"),
    "entrega": ("entrega-contra-entrega", "ads-entrega-contra-entrega", "Mensajero entregando el paquete del filtro y recibiendo el pago en efectivo en la puerta de la casa"),
}


LEYENDAS = {"alerta": "🔔 Así avisa tu nevecón", "agua": "💧 Listo: agua limpia otra vez", "entrega": "💵 Pagas al recibir"}


def figura(clave, eager=False):
    _, nombre, alt = IMAGENES[clave]
    return (f'<figure class="foto-ads"><picture><source srcset="/purofiltro-img/{nombre}-640.webp 640w, /purofiltro-img/{nombre}.webp 1024w" sizes="(max-width:860px) 92vw, 560px" type="image/webp">'
            f'<img src="/purofiltro-img/{nombre}.jpg" alt="{esc(alt)}" width="1024" height="572" {"fetchpriority=" + chr(34) + "high" + chr(34) if eager else "loading=" + chr(34) + "lazy" + chr(34)}></picture><figcaption>{LEYENDAS[clave]}</figcaption></figure>')


ICONO_WA = '<svg viewBox="0 0 32 32" aria-hidden="true"><path fill="currentColor" d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 23.6c-2 0-4-.6-5.7-1.6l-.4-.2-3.9 1 1-3.8-.3-.4A10.6 10.6 0 1 1 16 26.6zm5.8-7.9c-.3-.2-1.9-.9-2.2-1-.3-.1-.5-.2-.7.2l-1 1.2c-.2.2-.4.2-.7.1a8.7 8.7 0 0 1-4.3-3.8c-.3-.6.3-.5 1-1.7.1-.2 0-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.1-1.2 2.8s1.2 3.2 1.4 3.5c.2.2 2.4 3.7 5.8 5.1 2.2.9 3 1 4.1.8.7-.1 1.9-.8 2.2-1.5.3-.8.3-1.4.2-1.5-.1-.2-.3-.3-.6-.4z"/></svg>'

# ---------- hoja de estilos ----------
CSS = """
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font-family:var(--f);color:var(--ink);background:var(--fondo);font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased;overflow-x:hidden;text-rendering:optimizeLegibility;font-feature-settings:"kern","liga"}
img{max-width:100%;height:auto;display:block}a{color:var(--pri)}
h1,h2,h3{line-height:1.12;margin:0;letter-spacing:-.02em;text-wrap:balance}h2{font-size:clamp(26px,3.6vw,38px)}p{margin:0;text-wrap:pretty}
.w{max-width:1160px;margin:0 auto;padding:0 16px}
.sec{padding:clamp(52px,7vw,92px) 0}.sec.alt{background:var(--panel);border-block:1px solid var(--line)}
#cual,#filtros,#cuando,#alerta,#instalar{scroll-margin-top:84px}
.cab{max-width:760px;display:flex;flex-direction:column;gap:10px;margin-bottom:30px}.cab.c{margin-inline:auto;text-align:center;align-items:center}
.cab h2::after,.cab h1::after{content:"";display:block;width:56px;height:4px;border-radius:4px;background:var(--linea);margin-top:16px}.cab.c h2::after{margin-inline:auto}
.eye{font-size:13px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--eye)}.cab p{color:var(--muted);font-size:17px}
:focus-visible{outline:3px solid color-mix(in srgb,var(--pri) 55%,#fff);outline-offset:3px;border-radius:12px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;font:inherit;font-weight:800;font-size:16px;letter-spacing:.005em;text-decoration:none;border:0;cursor:pointer;border-radius:14px;padding:15px 24px;min-height:52px;transition:transform .15s,box-shadow .15s;touch-action:manipulation}
.btn:hover{transform:translateY(-2px)}.btn:active{transform:translateY(0)}.btn svg{width:22px;height:22px;flex:0 0 auto}
.btn.wa{background:linear-gradient(180deg,#19a057,var(--wa));color:#fff;box-shadow:0 1px 0 rgba(255,255,255,.25) inset,0 12px 24px -8px rgba(20,140,72,.55)}.btn.wa:hover{background:linear-gradient(180deg,#169650,var(--wa2))}
.btn.claro{background:rgba(255,255,255,.14);color:#fff;box-shadow:inset 0 0 0 2px rgba(255,255,255,.55)}
.btn.borde{background:#fff;color:var(--pri);box-shadow:inset 0 0 0 2px var(--pri)}
.barra{background:var(--pri2);color:#fff;font-size:13.5px;font-weight:600;letter-spacing:.01em;text-align:center;padding:8px 16px;display:flex;flex-wrap:wrap;justify-content:center;gap:4px 26px}
header{position:sticky;top:0;z-index:40;background:rgba(255,255,255,.93);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);box-shadow:0 1px 0 var(--line),0 8px 24px -18px rgba(18,23,38,.4)}
header .w{display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:68px}
.marca{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--ink)}
.marca svg{width:34px;height:34px;flex:0 0 auto}.marca b{display:block;font-size:18px;letter-spacing:-.01em;line-height:1.1}.marca small{display:block;font-size:12px;font-weight:700;color:var(--eye);letter-spacing:.04em;text-transform:uppercase;line-height:1.2}

.card .im,.foto{position:relative}
.lupa-btn{position:absolute;right:12px;top:12px;z-index:2;width:46px;height:46px;border-radius:50%;border:0;background:var(--pri);color:#fff;display:grid;place-items:center;cursor:pointer;box-shadow:0 8px 20px -6px rgba(18,23,38,.55);transition:transform .15s}
.lupa-btn:hover{transform:scale(1.08)}.lupa-btn:focus-visible,.lupa-x:focus-visible{outline:3px solid var(--acento);outline-offset:2px}
dialog.lupa{border:0;padding:0;border-radius:24px;width:min(680px,calc(100% - 24px));max-height:calc(100dvh - 24px);background:#fff;color:var(--ink);box-shadow:0 30px 80px -20px rgba(0,0,0,.6)}
dialog.lupa::backdrop{background:rgba(10,14,24,.62);backdrop-filter:blur(3px)}
.lupa-in{padding:26px 24px 24px;display:flex;flex-direction:column;gap:14px;overflow:auto;max-height:calc(100dvh - 24px)}
.lupa-x{position:sticky;top:0;align-self:flex-end;margin-bottom:-34px;z-index:3;width:42px;height:42px;border-radius:50%;border:1px solid var(--line);background:#fff;font-size:26px;line-height:1;cursor:pointer;color:var(--ink)}
.lupa-top{display:grid;grid-template-columns:130px 1fr;gap:16px;align-items:center}.lupa-top img{width:130px;height:130px;object-fit:contain;background:var(--panel);border-radius:18px}
.lupa-top h3{margin:2px 0 6px;font-size:21px}.lupa-top p{margin:0;color:var(--muted);font-size:14.5px}
.lupa-in h4{margin:6px 0 0;font-size:16px}
@media (max-width:520px){.lupa-top{grid-template-columns:90px 1fr}.lupa-top img{width:90px;height:90px}.lupa-in{padding:22px 16px 18px}}
header .mnav{border-top:1px solid var(--line)}
.mnav .w{display:flex;align-items:center;gap:6px;overflow-x:auto;white-space:nowrap;padding-top:8px;padding-bottom:8px;scrollbar-width:thin}
.mnav a{flex:none;text-decoration:none;color:var(--ink);font-size:14px;font-weight:600;padding:7px 13px;border-radius:999px;background:#fff;border:1px solid var(--line)}
.mnav a:hover{border-color:var(--pri)}.mnav a[aria-current]{background:var(--pri);color:#fff;border-color:var(--pri)}
.mnav .sep{flex:none;width:1px;height:22px;background:var(--line);margin:0 6px}
header .btn{padding:10px 16px;min-height:44px;font-size:15px}
@media (max-width:560px){header .btn span{display:none}header .btn{padding:10px 12px}.barra span+span+span{display:none}}
.hero{position:relative;overflow:hidden;color:#fff;background:radial-gradient(900px 420px at 85% 0%,color-mix(in srgb,var(--acento) 45%,transparent),transparent 60%),linear-gradient(150deg,var(--pri2),var(--pri))}
.hero::before{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.16) 1.2px,transparent 1.6px);background-size:24px 24px;-webkit-mask-image:linear-gradient(115deg,#000 0,transparent 62%);mask-image:linear-gradient(115deg,#000 0,transparent 62%)}
.hero::after{content:"";position:absolute;inset:auto -10% -1px -10%;height:80px;background:var(--fondo);border-radius:50% 50% 0 0/100% 100% 0 0}
.hero .w{position:relative;z-index:1;display:grid;grid-template-columns:1.1fr .9fr;gap:40px;align-items:center;padding-top:56px;padding-bottom:110px}
.cod{display:inline-flex;align-items:center;gap:10px;background:#fff;color:var(--pri2);border-radius:999px;padding:8px 16px 8px 8px;font-weight:800;font-size:14px;box-shadow:0 10px 30px rgba(0,0,0,.18);margin-bottom:20px}
.cod i{font-style:normal;display:grid;place-items:center;width:30px;height:30px;border-radius:50%;background:var(--wa);color:#fff;font-size:16px}
.hero h1{font-size:clamp(36px,5.6vw,62px);font-weight:800;letter-spacing:-.03em;line-height:1.04}.hero h1 em{font-style:normal;color:var(--acento)}
.hero .lead{font-size:19px;opacity:.92;margin:18px 0 28px;max-width:560px;line-height:1.55}
.hero .acc{display:flex;flex-wrap:wrap;gap:12px}
.hero ul{list-style:none;margin:26px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:8px 22px;font-size:15px;font-weight:600}
.hero ul li::before{content:"✓";display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:rgba(255,255,255,.18);margin-right:8px;font-size:12px}
.vis{position:relative;aspect-ratio:1/1;max-width:440px;width:100%;justify-self:center}
.vis .f{position:absolute;background:#fff;border-radius:28px;box-shadow:0 40px 70px -20px rgba(0,0,0,.45);display:grid;place-items:center}
.vis .f picture{position:absolute;inset:9%}.vis .f img{width:100%;height:100%;object-fit:contain}
.vis .f1{inset:0 18% 18% 0}.vis .f2{width:46%;height:46%;right:0;bottom:6%}
.vis .globo{position:absolute;left:-4%;bottom:-2%;z-index:2;background:#fff;color:var(--ink);border-radius:18px;padding:14px 16px;box-shadow:0 20px 40px rgba(0,0,0,.25);max-width:250px;font-size:14px;line-height:1.35}
.vis .globo b{display:block;color:var(--wa);font-size:13px;margin-bottom:4px}.vis .globo::after{content:"";position:absolute;left:28px;top:-8px;border:8px solid transparent;border-top:0;border-bottom-color:#fff}
@media (max-width:860px){.hero .w{grid-template-columns:1fr;padding-top:36px;gap:36px}.vis{max-width:330px}.vis .globo{left:0}}
.franja{margin-top:-58px;position:relative;z-index:2}
.franja .w>div{display:grid;grid-template-columns:repeat(4,1fr);background:#fff;border-radius:22px;box-shadow:0 30px 60px -24px rgba(18,23,38,.35);border:1px solid var(--line);overflow:hidden}
.franja .it{display:flex;gap:12px;align-items:center;padding:20px 18px;border-right:1px solid var(--line)}.franja .it:last-child{border-right:0}
.franja .ic{flex:0 0 46px;height:46px;border-radius:14px;background:var(--suave);display:grid;place-items:center;font-size:22px}
.franja b{display:block;font-size:15px;line-height:1.25}.franja small{color:var(--muted);font-size:13px}
@media (max-width:860px){.franja .w>div{grid-template-columns:1fr 1fr}.franja .it:nth-child(2){border-right:0}.franja .it:nth-child(-n+2){border-bottom:1px solid var(--line)}}
.picks{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:14px}
.pick{font:inherit;display:flex;flex-direction:column;align-items:center;gap:6px;background:#fff;border:2px solid var(--line);border-radius:20px;padding:16px 12px;cursor:pointer;box-shadow:var(--sombra);transition:border-color .15s,transform .15s,box-shadow .15s;touch-action:manipulation}
.pick:hover{transform:translateY(-3px)}.pick img{width:110px;height:110px;object-fit:contain}.pick b{font-size:15px}.pick small{color:var(--muted);font-size:12.5px}
.pick[aria-pressed="true"]{border-color:var(--pri);box-shadow:0 0 0 4px var(--suave)}
.pick.nose{border-style:dashed;justify-content:center;background:var(--suave);color:var(--pri2)}.pick.nose span{font-size:40px;line-height:1}
.elegido{margin-top:20px;display:flex;flex-wrap:wrap;gap:14px;align-items:center;justify-content:space-between;background:#fff;border:1px solid var(--line);border-radius:20px;padding:18px 20px;box-shadow:var(--sombra)}.elegido[hidden]{display:none}.elegido p{font-weight:600}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:20px}
.card{position:relative;display:flex;flex-direction:column;background:#fff;border:1px solid color-mix(in srgb,var(--line) 70%,#fff);border-radius:22px;overflow:hidden;box-shadow:var(--sombra);transition:transform .2s,box-shadow .2s}
.card:hover{transform:translateY(-4px);box-shadow:0 1px 2px rgba(18,23,38,.05),0 28px 50px -18px rgba(18,23,38,.3)}
.card .im{aspect-ratio:1/1;position:relative;background:radial-gradient(circle at 50% 38%,#fff 52%,var(--panel));border-bottom:1px solid var(--line)}
.card .im picture{position:absolute;inset:7% 9% 17% 9%}.card .im img{width:100%;height:100%;object-fit:contain}
.card .tipo{position:absolute;top:14px;left:14px;z-index:1;background:#fff;color:var(--pri2);font-size:12px;font-weight:800;padding:5px 11px;border-radius:999px;box-shadow:0 4px 12px rgba(18,23,38,.12)}
.cod-card{position:absolute;left:0;right:0;bottom:0;z-index:2;display:flex;align-items:center;justify-content:center;gap:6px;background:#0d5c36;color:#fff;font-size:13.5px;font-weight:800;letter-spacing:.01em;padding:9px 12px}
.card .tx{display:flex;flex-direction:column;gap:6px;padding:18px 20px 20px;flex:1}
.card h3{font-size:19px;letter-spacing:-.015em}.card h3 a{color:inherit;text-decoration:none}.card .ref{font-size:13px;color:var(--muted)}.card p{font-size:14.5px;color:var(--muted);flex:1}
.card .btn{margin-top:10px;font-size:15px;padding:12px 16px;min-height:48px}
.card .mas{font-size:14px;font-weight:700;text-align:center;padding:8px 0 0}
.pie-card{display:flex;flex-wrap:wrap;gap:4px 16px;font-size:13px;font-weight:700;color:#0d5c36;border-top:1px dashed var(--line);padding-top:12px;margin-top:8px}
.cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px}
.bloque{background:#fff;border:1px solid var(--line);border-radius:22px;padding:24px;box-shadow:var(--sombra)}
.bloque .ic{width:48px;height:48px;border-radius:14px;background:var(--suave);display:grid;place-items:center;font-size:24px;margin-bottom:12px}
.bloque h3{font-size:19px;margin-bottom:6px}.bloque p,.bloque li{color:var(--muted);font-size:15px}.bloque ul{margin:8px 0 0;padding-left:18px;display:flex;flex-direction:column;gap:4px}
.stat{font-size:54px;font-weight:800;line-height:1;color:var(--pri);margin-bottom:6px}
.alerta{display:grid;grid-template-columns:.85fr 1.15fr;gap:30px;align-items:center}
.display{background:#0e1117;color:#e8f1ff;border-radius:24px;padding:30px 28px;display:flex;gap:18px;align-items:center;box-shadow:0 30px 60px -28px rgba(0,0,0,.6),inset 0 0 0 1px rgba(255,255,255,.08)}
.display .led{flex:0 0 18px;height:18px;border-radius:50%;background:#ff5a4d;box-shadow:0 0 0 6px rgba(255,90,77,.18),0 0 22px #ff5a4d;animation:parpadeo 1.6s ease-in-out infinite}
.display small{display:block;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:#8fa1b8;margin-bottom:6px}
.display b{display:block;font:700 clamp(20px,3vw,28px)/1.15 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.05em;text-transform:uppercase;color:#fff}.display em{display:block;font-style:normal;color:#9db4d2;margin-top:6px;font-size:15px}
@keyframes parpadeo{50%{opacity:.35}}
.nota{font-size:14px;color:var(--muted);margin-top:12px}
.tw{overflow-x:auto;border-radius:18px;border:1px solid var(--line);background:#fff;box-shadow:var(--sombra)}
.tabla{width:100%;border-collapse:collapse;font-size:15px;min-width:560px}.tabla th,.tabla td{text-align:left;padding:12px 14px;border-bottom:1px solid var(--line);vertical-align:top}
.tabla th{background:var(--suave);font-size:12px;letter-spacing:.07em;text-transform:uppercase;color:var(--pri2)}.tabla tr:last-child td{border-bottom:0}
@media (max-width:860px){.alerta{grid-template-columns:1fr}}
details{background:#fff;border:1px solid var(--line);border-radius:18px;padding:0 20px;box-shadow:var(--sombra)}details+details{margin-top:10px}details[open]{border-color:color-mix(in srgb,var(--pri) 45%,var(--line))}
summary{cursor:pointer;list-style:none;padding:18px 34px 18px 0;font-weight:700;position:relative;font-size:17px}summary::-webkit-details-marker{display:none}
summary::after{content:"+";position:absolute;right:0;top:12px;font-size:26px;color:var(--pri);transition:transform .2s}details[open] summary::after{transform:rotate(45deg)}
details>p{padding:0 0 18px;color:var(--muted)}
details.inst summary{display:flex;align-items:center;gap:14px;padding:12px 34px 12px 0}details.inst summary::after{top:50%;margin-top:-18px}
details.inst summary img{width:58px;height:58px;object-fit:contain;background:#fff;border:1px solid var(--line);border-radius:12px;padding:4px;flex:0 0 auto}
details.inst summary b{display:block;font-size:17px;line-height:1.25}details.inst summary small{color:var(--muted);font-size:13px;font-weight:500}
.cuerpo{padding:4px 0 22px;display:flex;flex-direction:column;gap:16px}
.datos{display:grid;grid-template-columns:auto 1fr;gap:6px 16px;margin:0;font-size:15px}.datos dt{font-weight:800}.datos dd{margin:0;color:var(--muted)}
ol.pasos2{margin:0;padding:0;list-style:none;counter-reset:q;display:flex;flex-direction:column;gap:12px}
ol.pasos2 li{counter-increment:q;position:relative;padding:3px 0 3px 48px;min-height:36px}
ol.pasos2 li::before{content:counter(q);position:absolute;left:0;top:0;width:36px;height:36px;border-radius:50%;background:var(--chip);color:var(--chip-ink);font-weight:800;display:grid;place-items:center;font-size:15px}
.reset{background:var(--suave);border-radius:14px;padding:14px 16px;font-size:15px;color:var(--ink)}.reset b{color:var(--pri2)}
.acc2{display:flex;flex-wrap:wrap;gap:10px}.acc2 .btn{padding:12px 18px;min-height:46px;font-size:15px}
.sint{display:grid;grid-template-columns:1.1fr .9fr;gap:28px;align-items:start}
.checks{display:flex;flex-direction:column;gap:10px}
.checks label{display:flex;gap:14px;align-items:center;background:#fff;border:2px solid var(--line);border-radius:16px;padding:14px 16px;cursor:pointer;font-weight:600;transition:border-color .15s}
.checks input{width:22px;height:22px;accent-color:var(--pri);flex:0 0 auto}.checks label:has(input:checked){border-color:var(--pri);background:var(--suave)}
.veredicto{position:sticky;top:90px;background:linear-gradient(150deg,var(--pri2),var(--pri));color:#fff;border-radius:24px;padding:28px;display:flex;flex-direction:column;gap:14px;box-shadow:0 30px 60px -28px rgba(18,23,38,.55)}
.veredicto .n{font-size:56px;font-weight:800;line-height:1}.veredicto p{opacity:.92}
@media (max-width:860px){.sint{grid-template-columns:1fr}.veredicto{position:static}}
.pasos{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;counter-reset:p}
.paso{background:#fff;border:1px solid var(--line);border-radius:24px;padding:26px;box-shadow:var(--sombra)}
.paso::before{counter-increment:p;content:counter(p);display:grid;place-items:center;width:46px;height:46px;border-radius:14px;background:var(--chip);color:var(--chip-ink);font-weight:800;font-size:20px;margin-bottom:14px}
.paso h3{font-size:20px;margin-bottom:6px}.paso p{color:var(--muted)}
@media (max-width:760px){.pasos{grid-template-columns:1fr}}
.promo{display:grid;grid-template-columns:auto 1fr auto;gap:22px;align-items:center;background:#fff;border:2px dashed var(--pri);border-radius:26px;padding:26px 28px;box-shadow:var(--sombra)}
.promo .sello{width:92px;height:92px;border-radius:50%;background:var(--chip);color:var(--chip-ink);display:grid;place-items:center;text-align:center;font-weight:800;font-size:13px;line-height:1.1;transform:rotate(-8deg)}.promo .sello b{display:block;font-size:30px}
.promo h3{font-size:24px;margin-bottom:6px}.promo p{color:var(--muted)}
@media (max-width:760px){.promo{grid-template-columns:1fr;text-align:center;justify-items:center}}
.chips{display:flex;flex-wrap:wrap;gap:8px}.chips span,.chips a{background:#fff;border:1px solid var(--line);border-radius:999px;padding:7px 14px;font-size:14px;font-weight:600;color:var(--ink);text-decoration:none}.chips a:hover{border-color:var(--pri);color:var(--pri)}
.final{background:linear-gradient(150deg,var(--pri2),var(--pri));color:#fff;border-radius:30px;padding:44px 32px;text-align:center;display:flex;flex-direction:column;align-items:center;gap:14px;box-shadow:0 30px 60px -28px rgba(18,23,38,.55)}
.final h2{color:#fff}.final p{opacity:.9;max-width:560px}
.todas{margin-top:18px;text-align:center;background:none;border:0;box-shadow:none;padding:0}.todas summary::after{display:none}.todas summary{display:inline-block;cursor:pointer;font-weight:800;color:var(--pri);padding:10px 20px;border:2px solid var(--pri);border-radius:999px;list-style:none}
.todas summary::-webkit-details-marker{display:none}.todas[open] summary{margin-bottom:16px}
.cab h2{letter-spacing:-.02em;text-wrap:balance}.cab p{max-width:62ch}.cab.c p{margin-inline:auto}
footer .cols3{display:grid;grid-template-columns:1.3fr 1fr 1fr;gap:28px}footer .cols3>div{display:flex;flex-direction:column;gap:8px;min-width:0}
footer h4{margin:0 0 4px;color:#fff;font-size:13px;letter-spacing:.09em;text-transform:uppercase;opacity:.75}
@media (max-width:760px){footer .cols3{grid-template-columns:1fr}}
footer{background:#0f1320;color:rgba(255,255,255,.75);padding:44px 0 110px;font-size:14px;border-top:4px solid var(--acento)}
footer .w{display:flex;flex-direction:column;gap:12px}footer a{color:#fff}footer b{color:#fff;font-size:17px}
footer .leg{font-size:12.5px;color:rgba(255,255,255,.55);border-top:1px solid rgba(255,255,255,.12);padding-top:14px}
.migas{font-size:14px;color:var(--muted);padding:22px 0 0}.migas a{color:var(--muted)}
.pdp{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:start}
.pdp .foto{position:sticky;top:96px;aspect-ratio:1/1;background:radial-gradient(circle at 50% 38%,#fff 52%,var(--panel));border:1px solid var(--line);border-radius:28px;box-shadow:var(--sombra)}
.pdp .foto picture{position:absolute;inset:8%}.pdp .foto img{width:100%;height:100%;object-fit:contain}
.pdp .info{display:flex;flex-direction:column;gap:16px}.pdp h1{font-size:clamp(28px,3.8vw,42px);font-weight:800;letter-spacing:-.03em}
.pdp .sub{color:var(--muted)}
.cod-big{display:flex;gap:14px;align-items:center;background:#e8f5ee;border:1px solid #bfe3cf;color:#0d5c36;border-radius:18px;padding:14px 16px}.cod-big>span:first-child{font-size:30px}.cod-big b{display:block;font-size:17px}.cod-big small{font-size:14px;color:#25704b}
.lista{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:8px}.lista li{position:relative;padding-left:28px}.lista li::before{content:"✓";position:absolute;left:0;top:2px;width:20px;height:20px;border-radius:50%;background:var(--suave);color:var(--pri);font-weight:900;font-size:12px;display:grid;place-items:center}
@media (max-width:860px){.pdp{grid-template-columns:1fr}.pdp .foto{position:relative;top:0;max-width:420px;width:100%;justify-self:center}}
.foto-ads{position:relative;margin:0;border-radius:24px;overflow:hidden;border:1px solid var(--line);box-shadow:var(--sombra);background:#fff}.foto-ads img{width:100%;height:auto;display:block}
.foto-ads figcaption{position:absolute;left:14px;bottom:14px;background:rgba(255,255,255,.95);color:var(--ink);font-weight:700;font-size:14px;line-height:1.2;padding:9px 15px;border-radius:999px;box-shadow:0 8px 22px rgba(0,0,0,.22)}
.dos{display:grid;grid-template-columns:1.05fr .95fr;gap:36px;align-items:center;margin-bottom:34px}.dos .cab{margin-bottom:0}
.entrega{display:grid;grid-template-columns:.95fr 1.05fr;gap:36px;align-items:center}.entrega .cab{margin-bottom:22px}.entrega .pasos{grid-template-columns:1fr;gap:12px}
.entrega .paso{display:grid;grid-template-columns:auto 1fr;column-gap:16px;align-items:center;padding:18px 20px}.entrega .paso::before{margin:0;grid-row:span 2}.entrega .paso h3{font-size:18px;margin:0}.entrega .paso p{font-size:15px}
@media (max-width:860px){.dos,.entrega{grid-template-columns:1fr;gap:24px}.dos .foto-ads{order:-1}}
.fija{position:fixed;left:0;right:0;bottom:0;z-index:50;background:#fff;border-top:1px solid var(--line);box-shadow:0 -10px 30px rgba(0,0,0,.08);padding:10px 16px calc(10px + env(safe-area-inset-bottom));display:flex;align-items:center;gap:12px}
.fija span{flex:1;font-size:13.5px;line-height:1.25;font-weight:600}.fija span small{display:block;color:var(--muted);font-weight:500}.fija .btn{padding:12px 18px;min-height:48px;font-size:15px;animation:pulso 2.6s ease-out infinite}
@keyframes pulso{0%{box-shadow:0 0 0 0 rgba(20,140,72,.5)}70%{box-shadow:0 0 0 14px rgba(20,140,72,0)}100%{box-shadow:0 0 0 0 rgba(20,140,72,0)}}
@media (min-width:861px){.fija{left:auto;right:22px;bottom:22px;border-radius:18px;border:1px solid var(--line);max-width:430px}}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important;scroll-behavior:auto!important}}
"""


def css(cfg):
    raiz = (f":root{{--pri:{cfg['pri']};--pri2:{cfg['pri2']};--acento:{cfg['acento']};--suave:{cfg['suave']};--gris:{cfg.get('gris', '#5b6273')};"
            f"--eye:{cfg.get('eye', cfg['pri'])};--chip:{cfg.get('chip', cfg['pri'])};--chip-ink:{cfg.get('chip_ink', '#fff')};--linea:{cfg.get('subrayado', cfg['pri'])};"
            f"--ink:#121726;--muted:#596074;--line:#e3e6ee;--fondo:#ffffff;--panel:#f5f7fb;--wa:#148c48;--wa2:#0f7a3d;"
            f"--sombra:0 1px 2px rgba(18,23,38,.05),0 12px 28px -14px rgba(18,23,38,.22);--f:\"{cfg['fuente']}\",system-ui,-apple-system,\"Segoe UI\",sans-serif}}")
    return raiz + CSS


# ---------- piezas comunes ----------
def gota(cfg):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true"><rect width="24" height="24" rx="7" fill="{cfg["pri"]}"/><path d="M12 4.2C9.4 7.6 6.9 10.3 6.9 13.5a5.1 5.1 0 0 0 10.2 0c0-3.2-2.5-5.9-5.1-9.3z" fill="{cfg.get("gota", "#fff")}"/></svg>'


MENU = {}  # marca -> [(referencia, slug)]; se llena en main()


def menu(marca, ruta):
    def a(href, txt, extra=""):
        act = ' aria-current="page"' if ruta.rstrip("/") == href.rstrip("/") else ""
        return f'<a href="{href}"{act}{extra}>{esc(txt)}</a>'
    propios = "".join(a(f"/purofiltro-filtro/{sl}/", f"Filtro {ref}") for ref, sl in MENU.get(marca, []))
    return (f'<nav class="mnav" aria-label="Filtros {esc(marca)}"><div class="w">'
            f'{a(f"/purofiltro-marca/{slug(marca)}/", f"Filtros {marca}")}<span class="sep"></span>{propios}</div></nav>')


def cabeza(marca, cfg, titulo, desc, ruta, ld, imagen):
    n = cfg["whatsapp"]
    envio = "Envío gratis" if ENVIO_GRATIS else "Envío"
    hola = f"Hola, quiero un filtro de agua para mi nevecón {marca} con pago contra entrega."
    svg = gota(cfg).replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ')
    return f"""<!doctype html>
<html lang="es-CO">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(titulo)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{BASE}{ruta}">
<meta name="google-site-verification" content="{VERIFICACION}">
<meta name="theme-color" content="{cfg['pri']}">
<meta property="og:type" content="website"><meta property="og:locale" content="es_CO"><meta property="og:site_name" content="{esc(NEGOCIO)}">
<meta property="og:title" content="{esc(titulo)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{BASE}{ruta}"><meta property="og:image" content="{BASE}{imagen}">
<link rel="icon" href="data:image/svg+xml,{quote(svg)}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={cfg['fuente'].replace(' ', '+')}:wght@400;500;600;700;800&display=swap">
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','{GTM}');</script>
<script type="application/ld+json">{json_ld(ld)}</script>
<style>{css(cfg)}</style>
</head>
<body>
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM}" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<div class="barra"><span>💵 Pagas al recibir</span><span>🚚 {envio} a toda Colombia</span><span>💬 Asesoría por WhatsApp</span></div>
<header><div class="w">
  <a class="marca" href="/purofiltro-marca/{slug(marca)}/">{gota(cfg)}<span><b>{esc(NEGOCIO)}</b><small>Nevecones {esc(marca)}</small></span></a>
  <a class="btn wa" data-wa="encabezado" href="{esc(wa(n, hola))}" target="_blank" rel="noopener">{ICONO_WA}<span>Escríbenos</span></a>
</div>{menu(marca, ruta)}</header>
"""


def pie(marca, cfg, fija_texto="Te decimos cuál es tu filtro"):
    n = cfg["whatsapp"]
    tel = f"{n[:3]} {n[3:6]} {n[6:]}"
    hola = f"Hola, quiero un filtro de agua para mi nevecón {marca} con pago contra entrega."
    return f"""
<footer><div class="w">
  <div class="cols3">
    <div><b>{esc(NEGOCIO)}</b><span>Distribuidor autorizado de filtros de agua para nevecones {esc(marca)}. Pagas al recibir, en toda Colombia.</span></div>
    <div><h4>Filtros {esc(marca)}</h4>{"".join(f'<a href="/purofiltro-filtro/{sl}/">Filtro {esc(r)}</a>' for r, sl in MENU.get(marca, []))}</div>
    <div><h4>Contacto</h4><span>WhatsApp: <a data-wa="pie" href="{esc(wa(n, hola))}" target="_blank" rel="noopener">{tel}</a></span><span>{esc(HORARIO)}</span><a href="/purofiltro-contraentrega/datos.html">Tratamiento de datos</a><a href="/purofiltro-contraentrega/terminos.html">Términos del pago contra entrega</a></div>
  </div>
  <span class="leg">© <span id="anio">2026</span> {esc(NEGOCIO)}. {esc(marca)} es una marca registrada de su dueño; la usamos solo para indicar en qué nevecones sirven los filtros.</span>
</div></footer>
<div class="fija"><span>Pagas al recibir<small>{esc(fija_texto)}</small></span><a class="btn wa" data-wa="barra" href="{esc(wa(n, hola))}" target="_blank" rel="noopener">{ICONO_WA}WhatsApp</a></div>
"""


def script(marca, cfg, con_picks=False, con_sintomas=False, total_sintomas=0):
    n = cfg["whatsapp"]
    s = f"""
<script>
(() => {{
  const N = "57{n}", MARCA = {json.dumps(marca)};
  const wa = t => "https://wa.me/" + N + "?text=" + encodeURIComponent(t);
  window.dataLayer = window.dataLayer || [];
  // Conversión «whatsapp» (la misma de la tienda) en Google Tag Manager, con el botón que se tocó
  document.addEventListener("click", e => {{ const a = e.target.closest('a[href*="wa.me/"]'); if (a) dataLayer.push({{ event: "whatsapp", ubicacion: a.dataset.wa || "enlace", marca: MARCA, pagina: location.pathname }}); }}, true);
  document.getElementById("anio").textContent = new Date().getFullYear();
  document.querySelectorAll("[data-lupa]").forEach(b => b.addEventListener("click", () => {{ const d = document.getElementById(b.dataset.lupa); if (d && d.showModal) d.showModal(); }}));
  document.querySelectorAll("dialog.lupa").forEach(d => {{ d.addEventListener("click", e => {{ if (e.target === d || e.target.closest("[data-cerrar]")) d.close(); }}); }});
"""
    if con_picks:
        s += """
  const box = document.getElementById("elegido");
  document.querySelectorAll(".pick").forEach(b => b.addEventListener("click", () => {
    document.querySelectorAll(".pick").forEach(x => x.setAttribute("aria-pressed", x === b ? "true" : "false"));
    box.hidden = false;
    document.getElementById("elegido-txt").textContent = b.classList.contains("nose") ? "Escríbenos y mándanos la foto: te decimos cuál es." : "Elegiste el " + b.querySelector("b").textContent + ". Te confirmamos si es el de tu nevecón y el precio de hoy.";
    document.getElementById("elegido-btn").href = wa(b.dataset.msg);
    box.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }));
"""
    if con_sintomas:
        s += f"""
  const checks = [...document.querySelectorAll("#checks input")], total = {total_sintomas};
  const pintar = () => {{
    const m = checks.filter(c => c.checked).map(c => c.value);
    document.getElementById("v-n").textContent = m.length + "/" + total;
    document.getElementById("v-t").textContent = m.length === 0 ? "Marca lo que te pasa" : m.length === 1 ? "Ya es hora de cambiarlo" : "Tu filtro está saturado: cámbialo ya";
    document.getElementById("v-p").textContent = m.length === 0 ? "Si marcas una o más, tu filtro ya está saturado y el agua y el hielo no se están filtrando bien." : "El filtro ya no retiene el cloro ni el sedimento. Escríbenos y te decimos cuál es el tuyo y el precio de hoy, con pago contra entrega.";
    document.getElementById("v-btn").href = wa("Hola, a mi nevecón " + MARCA + " le pasa: " + (m.join("; ") || "quiero revisar el filtro") + ". Quiero cambiar el filtro con pago contra entrega.");
  }};
  checks.forEach(c => c.addEventListener("change", pintar));
"""
    return s + "})();\n</script>\n</body>\n</html>\n"


def faq_html(preguntas):
    return "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in preguntas)


def faq_ld(preguntas):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in preguntas]}


def miga_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, **({"item": BASE + r} if r else {})} for i, (n, r) in enumerate(items)]}


SINTOMAS = ["El agua o el hielo saben a cloro o a tierra", "El hielo sale turbio o con mal olor", "El dispensador bota menos agua", "Se prendió la alerta del filtro en la pantalla", "Hace más de 6 meses que no lo cambio"]


def sec(cuerpo, alt=False, id_="", estilo=""):
    return f'<section class="sec{" alt" if alt else ""}"{f" id={chr(34)}{id_}{chr(34)}" if id_ else ""}{f" style={chr(34)}{estilo}{chr(34)}" if estilo else ""}><div class="w">{cuerpo}</div></section>\n'


def cab(eye, titulo, texto="", centrado=False, h="h2"):
    return f'<div class="cab{" c" if centrado else ""}"><span class="eye">{esc(eye)}</span><{h}>{esc(titulo)}</{h}>{f"<p>{texto}</p>" if texto else ""}</div>'


def bloque_porque(marca):
    items = [("💵", "Pagas cuando lo recibes", "Sin transferencias ni adelantos: el pago es en efectivo al recibir tu pedido."),
             ("📸", "Te decimos cuál es el tuyo", f"Con una foto del filtro viejo o el modelo de tu nevecón {marca} confirmamos la referencia correcta."),
             ("🔧", "Lo instalas tú, sin técnico", "Cada filtro trae su paso a paso: se cambia en 2 minutos los internos y en 10 a 15 los externos."),
             ("💬", "Atención directa por WhatsApp", "Resolvemos tus dudas antes y después de recibir el filtro, sin llamadas ni formularios.")]
    return sec(cab("Por qué pedir con nosotros", "Pedir tu filtro es simple y sin riesgo", "Distribuidor autorizado. Tú solo escoges, nosotros nos encargamos del resto.", True)
               + '<div class="cols">' + "".join(f'<div class="bloque"><div class="ic">{i}</div><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for i, t, d in items) + "</div>")


def bloque_cuando(marca, cfg):
    info = marcas_exclusivas.MARCAS_INFO[marca]
    return sec(f'<div class="dos"><div>{cab("Mantenimiento", f"¿Cuándo cambiar el filtro de tu nevecón {marca}?", "Un filtro de agua se cambia <b>cada 6 meses</b>. Antes, si tu familia es grande, usan mucho hielo o el agua de tu ciudad trae sedimento.")}</div>{figura("alerta")}</div>' + f'''
  <div class="cols">
    <div class="bloque"><div class="stat">6</div><h3>meses de uso normal</h3><p>Pasado ese tiempo el carbón del filtro se satura y ya no retiene el cloro, los olores ni el sedimento, aunque el agua se vea transparente.</p></div>
    <div class="bloque"><div class="ic">👀</div><h3>Señales de que ya toca</h3><ul><li>El agua o el hielo saben o huelen raro (cloro, tierra, encerrado).</li><li>El dispensador bota menos agua o tarda más en llenar el vaso.</li><li>El hielo sale turbio, pequeño o se produce menos.</li><li>Apareció la alerta del filtro en la pantalla.</li></ul></div>
    <div class="bloque"><div class="ic">⚠️</div><h3>Si no lo cambias</h3><ul><li>El agua y el hielo no se filtran bien.</li><li>Baja la presión del agua en el dispensador.</li><li>La suciedad puede llegar a la válvula y a la máquina de hielo.</li></ul></div>
  </div>
  <p class="nota">Consejo: apunta la fecha del cambio con un marcador en el filtro nuevo y en tu calendario. {esc(info["aviso"])}</p>''', alt=True, id_="cuando")


def display_mock(cfg, marca):
    en, es = cfg["display"]
    return (f'<div class="display" role="img" aria-label="Ejemplo de la alerta del filtro en la pantalla del nevecón {esc(marca)}"><span class="led"></span>'
            f'<div><small>Así suele salir en tu {esc(marca)}</small><b>{esc(en)}</b><em>{esc(es)}</em></div></div>'
            '<p class="nota">El texto exacto cambia según el modelo; a veces es solo una luz o un ícono de gota.</p>')


def bloque_alerta(marca, cfg, ps):
    info = marcas_exclusivas.MARCAS_INFO[marca]
    filas = "".join(f'<tr><td><b>{esc(p["ref"])}</b></td><td>{esc(p["datos"]["reset"])}</td></tr>' for p in ps)
    return sec(f'''<div class="alerta">
    <div>{display_mock(cfg, marca)}</div>
    <div>{cab("Pantalla del nevecón", f"La alerta del filtro en tu nevecón {marca}", esc(info["aviso"]) + " El nevecón no mide qué tan sucio está el filtro: cuenta el tiempo de uso. Por eso, <b>después de cambiarlo hay que reiniciar el aviso</b>.")}</div>
  </div>
  <h3 style="margin:34px 0 14px;font-size:22px">Cómo apagar la alerta según tu filtro</h3>
  <div class="tw"><table class="tabla"><thead><tr><th>Referencia</th><th>Cómo reiniciar el aviso</th></tr></thead><tbody>{filas}</tbody></table></div>
  <p class="nota">Si la alerta no se apaga, mantén el botón un poco más (hasta 5 segundos) o revisa en el manual el botón «Filter». Los filtros externos de manguera no prenden ninguna alerta.</p>''', id_="alerta")


def detalle_instalacion(p, marca, cfg):
    d = p["datos"]
    n = cfg["whatsapp"]
    msg = f'Hola, quiero el precio de hoy del {p["largo"]} para mi nevecón {marca}, con pago contra entrega.'
    return f'''<details class="inst">
    <summary><img src="/purofiltro-img/{p["id"]}-400.webp" alt="" width="58" height="58" loading="lazy"><span><b>{esc(p["largo"])}</b><small>{"Externo, va en la manguera" if p["externo"] else "Interno"} · {esc(d["tiempo"])}</small></span></summary>
    <div class="cuerpo">
      <dl class="datos"><dt>Dónde va</dt><dd>{esc(d["donde"])}</dd><dt>Tiempo</dt><dd>{esc(d["tiempo"])}</dd><dt>Herramientas</dt><dd>{esc(d["herramientas"])}</dd></dl>
      <ol class="pasos2">{"".join(f"<li>{esc(x)}</li>" for x in d["pasos"])}</ol>
      <div class="reset"><b>Último paso:</b> {esc(d["reset"])}</div>
      <div class="acc2"><a class="btn borde" href="/purofiltro-filtro/{p["slug"]}/">Ver la ficha de la referencia</a><a class="btn wa" data-wa="instalacion" href="{esc(wa(n, msg))}" target="_blank" rel="noopener">{ICONO_WA}Pedirlo contra entrega</a></div>
    </div>
  </details>'''


ICONO_LUPA = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/><path d="M10.5 8v5M8 10.5h5" stroke-width="2"/></svg>'


def lupa_btn(p):
    return f'<button type="button" class="lupa-btn" data-lupa="lupa-{p["id"]}" aria-label="Ver especificaciones y cómo se instala el {esc(p["largo"])}">{ICONO_LUPA}</button>'


def lupa_dialog(p, marca, cfg):
    d = p["datos"]
    n = cfg["whatsapp"]
    msg = f'Hola, quiero el precio de hoy del {p["largo"]} para mi nevecón {marca}, con pago contra entrega.'
    otras = [r for r in p["refs"] if r != p["ref"]]
    filas = [("Marca", marca), ("Referencia", p["ref"])]
    if otras:
        filas.append(("También aparece como", ", ".join(otras)))
    filas += [("Tipo", "Externo, va en la manguera del agua" if p["externo"] else "Interno, va dentro del nevecón"),
              ("Dónde va", d["donde"]), ("Tiempo de cambio", d["tiempo"]), ("Herramientas", d["herramientas"]), ("Se cambia", "Cada 6 meses, o antes si el agua cambia de sabor")]
    if p.get("modelos"):
        filas.append(("Nevecones que lo usan", ", ".join(p["modelos"][:8]) + (" y otros" if len(p["modelos"]) > 8 else "")))
    dl = "".join(f"<dt>{esc(a)}</dt><dd>{esc(b)}</dd>" for a, b in filas)
    return f'''<dialog class="lupa" id="lupa-{p["id"]}" aria-label="{esc(p["largo"])}">
    <div class="lupa-in">
      <button type="button" class="lupa-x" data-cerrar aria-label="Cerrar">&times;</button>
      <div class="lupa-top"><picture><source srcset="/purofiltro-img/{p["id"]}-400.webp" type="image/webp"><img src="/purofiltro-img/{p["id"]}.jpg" alt="{esc(p["largo"])}" width="400" height="400" loading="lazy"></picture>
        <div><span class="eye">Para nevecón {esc(marca)}</span><h3>{esc(p["largo"])}</h3><p>{esc((p.get("desc") or "").split(". ")[0])}.</p></div></div>
      <h4>Especificaciones</h4><dl class="datos">{dl}</dl>
      <h4>Cómo se instala</h4><ol class="pasos2">{"".join(f"<li>{esc(x)}</li>" for x in d["pasos"])}</ol>
      <div class="reset"><b>Último paso:</b> {esc(d["reset"])}</div>
      <div class="acc2"><a class="btn borde" href="/purofiltro-filtro/{p["slug"]}/">Ver la ficha completa</a><a class="btn wa" data-wa="lupa" href="{esc(wa(n, msg))}" target="_blank" rel="noopener">{ICONO_WA}Pedirlo contra entrega</a></div>
    </div>
  </dialog>'''


def bloque_entrega():
    return sec(f'''<div class="entrega">{figura("entrega")}<div>{cab("Así de fácil", "Pides hoy, pagas cuando te llega")}<div class="pasos">
    <div class="paso"><h3>Escríbenos</h3><p>Por WhatsApp, con el filtro que tocaste o una foto del tuyo.</p></div>
    <div class="paso"><h3>Confirmamos</h3><p>Te decimos cuál es, el precio de hoy y tomamos tu dirección.</p></div>
    <div class="paso"><h3>Recibe y paga</h3><p>Te llega en 2 a 3 días hábiles y le pagas en efectivo al mensajero.</p></div></div></div></div>''', alt=True)


def tabla_compat(ps):
    filas = ""
    for p in ps:
        otras = [r for r in p["refs"] if norm(r) != norm(p["ref"])]
        filas += (f'<tr><td><b><a href="/purofiltro-filtro/{p["slug"]}/">{esc(p["ref"])}</a></b><br><span style="color:var(--muted)">{"Externo" if p["externo"] else "Interno"}</span></td>'
                  f'<td>{esc(", ".join(otras)) if otras else "—"}</td><td>{esc(", ".join(p["modelos"])) if p["modelos"] else "Se instala en la manguera del agua; sirve para varias marcas y modelos."}</td></tr>')
    return f'<div class="tw"><table class="tabla"><thead><tr><th>Referencia</th><th>También aparece como</th><th>Nevecones que lo usan</th></tr></thead><tbody>{filas}</tbody></table></div>'


# ---------- portada de la marca ----------
def pagina_marca(marca, cfg, ps, ciud):
    n = cfg["whatsapp"]
    envio = "Envío gratis" if ENVIO_GRATIS else "Envío"
    hola = f"Hola, quiero un filtro de agua para mi nevecón {marca} con pago contra entrega."
    ruta = f"/purofiltro-marca/{slug(marca)}/"
    titulo = f"Filtro de agua para nevecón {marca} | Paga contra entrega"
    desc = (f"Filtros de agua para nevecones {marca} ({', '.join(p['ref'] for p in ps)}). Pagas al recibir, {envio.lower()} a toda Colombia. "
            "Cuándo cambiarlo, qué significa la alerta de la pantalla y cómo instalar cada referencia.")
    tarjetas = "".join(f'''
      <article class="card">
        <span class="tipo">{"Externo · manguera" if p["externo"] else "Interno"}</span>
        <div class="im"><picture><source srcset="/purofiltro-img/{p["id"]}-400.webp" type="image/webp"><img src="/purofiltro-img/{p["id"]}.jpg" alt="{esc(p["largo"])} para nevecón {esc(marca)}" width="400" height="400" loading="lazy"></picture>{lupa_btn(p)}<span class="cod-card">💵 Paga contra entrega</span></div>
        <div class="tx">
          <h3><a href="/purofiltro-filtro/{p["slug"]}/">{esc(p["largo"])}</a></h3>
          <span class="ref">Ref. {esc(p["ref"])}{(" · también " + esc(", ".join([r for r in p["refs"] if r != p["ref"]][:2]))) if len(p["refs"]) > 1 else ""}</span>
          <p>{esc((p.get("desc") or "").split(". ")[0])}.</p>
          <a class="btn wa" data-wa="tarjeta" href="{esc(wa(n, f'Hola, quiero el precio de hoy del {p["largo"]} para mi nevecón {marca}, con pago contra entrega.'))}" target="_blank" rel="noopener">{ICONO_WA}Precio de hoy por WhatsApp</a>
          <a class="mas" href="/purofiltro-filtro/{p["slug"]}/">Ver ficha, instalación y cuándo cambiarlo →</a>
          <div class="pie-card"><span>💵 Pagas al recibir</span><span>🚚 {envio}</span></div>
        </div>
        {lupa_dialog(p, marca, cfg)}
      </article>''' for p in ps)
    elegir = "".join(f'''<button type="button" class="pick" data-msg="{esc(f'Hola, mi filtro se parece al {p["largo"]}. ¿Me confirman si es el de mi nevecón {marca} y el precio de hoy con pago contra entrega?')}"><img src="/purofiltro-img/{p["id"]}-400.webp" alt="" width="120" height="120" loading="lazy"><b>{esc(p["ref"])}</b><small>{"Va en la manguera" if p["externo"] else "Va adentro"}</small></button>''' for p in ps)
    preguntas = [
        ("¿Cómo funciona el pago contra entrega?", "Nos escribes por WhatsApp, confirmamos cuál es tu filtro y tu dirección, y te lo enviamos. Le pagas en efectivo a la transportadora cuando te llega. No pagas nada antes."),
        ("¿Por qué no está el precio en la página?", "Porque te damos el precio del día y las promociones vigentes (como el pack de 2 filtros) directamente por WhatsApp, después de confirmar que es el filtro correcto para tu nevecón. Así no compras uno equivocado."),
        ("¿Cada cuánto se cambia el filtro de agua del nevecón?", "Cada 6 meses, o antes si el agua o el hielo cambian de sabor u olor, si el dispensador bota menos agua o si aparece la alerta en la pantalla."),
        (f"¿Qué significa la alerta del filtro en mi nevecón {marca}?", f"{marcas_exclusivas.MARCAS_INFO[marca]['aviso']} Significa que el filtro ya cumplió su tiempo: hay que cambiarlo y reiniciar el aviso."),
        ("¿Cómo apago la alerta después de cambiar el filtro?", "Se reinicia desde el panel del nevecón, normalmente dejando presionado 3 segundos el botón del filtro («Filter» o «Reset»). En esta página tienes el paso exacto de cada referencia."),
        ("¿Cómo sé cuál es mi filtro?", f"Toca en esta página el filtro que se parece al tuyo, o mándanos por WhatsApp una foto del filtro viejo o de la etiqueta del nevecón. La etiqueta está {cfg['etiqueta']}."),
        ("¿Es difícil de cambiar?", "No. Los internos se cambian en 2 minutos sin herramientas y los externos en 10 a 15 minutos. Abajo tienes el paso a paso de cada referencia."),
        ("¿Cuánto tarda en llegar?", "A las principales ciudades llega en 2 a 3 días hábiles; a otros municipios puede tardar un poco más. Te mandamos el número de guía para que sigas el paquete."),
    ]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": f"Filtros de agua para nevecón {marca}", "url": BASE + ruta, "inLanguage": "es-CO", "description": desc,
         "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{BASE}/purofiltro-filtro/{p['slug']}/", "name": p["largo"]} for i, p in enumerate(ps)]}},
        miga_ld([("Inicio", "/"), (f"Filtros {marca}", None)]), faq_ld(preguntas)]}
    c = cabeza(marca, cfg, titulo, desc, ruta, ld, f"/purofiltro-img/{ps[0]['id']}.jpg")
    c += f"""
<section class="hero"><div class="w">
  <div>
    <span class="cod"><i>💵</i>Distribuidor autorizado · Pago contra entrega</span>
    <h1>Filtro de agua para tu nevecón <em>{esc(marca)}</em></h1>
    <p class="lead">Recibe el filtro en tu casa y págalo en efectivo cuando llegue. No adelantas nada. Por WhatsApp te confirmamos cuál es el que necesita tu nevecón.</p>
    <div class="acc"><a class="btn wa" data-wa="portada" href="{esc(wa(n, hola))}" target="_blank" rel="noopener">{ICONO_WA}Pedir por WhatsApp</a><a class="btn claro" href="#cual">¿Cuál es mi filtro?</a></div>
    <ul><li>Pagas al recibir</li><li>{envio}</li><li>Asesoría gratis</li><li>Para {esc(cfg["lineas"])}</li></ul>
  </div>
  <div class="vis">
    <span class="f f1"><picture><source srcset="/purofiltro-img/{ps[0]['id']}.webp" type="image/webp"><img src="/purofiltro-img/{ps[0]['id']}.jpg" alt="Filtro de agua para nevecón {esc(marca)}" width="600" height="600" fetchpriority="high"></picture></span>
    <span class="f f2"><picture><source srcset="/purofiltro-img/{ps[1]['id']}-400.webp" type="image/webp"><img src="/purofiltro-img/{ps[1]['id']}.jpg" alt="" width="400" height="400"></picture></span>
    <span class="globo"><b>● WhatsApp</b>Mándanos una foto de tu filtro viejo y te decimos cuál es y el precio de hoy.</span>
  </div>
</div></section>

<section class="franja"><div class="w"><div>
  <div class="it"><span class="ic">💵</span><span><b>Pagas al recibir</b><small>Efectivo, sin adelantos</small></span></div>
  <div class="it"><span class="ic">🚚</span><span><b>{envio}</b><small>A toda Colombia</small></span></div>
  <div class="it"><span class="ic">📸</span><span><b>Te asesoramos</b><small>Mándanos una foto del filtro</small></span></div>
  <div class="it"><span class="ic">⏱️</span><span><b>Llega en 2 a 3 días</b><small>Principales ciudades</small></span></div>
</div></div></section>
"""
    c += sec(cab("Encuéntralo en 10 segundos", "¿A cuál se parece tu filtro?", f"Toca el que se parece al de tu nevecón {esc(marca)}. Te confirmamos por WhatsApp que sea el correcto y te damos el precio de hoy. Si no sabes cuál es, mándanos una foto.", True)
             + f'<div class="picks">{elegir}<button type="button" class="pick nose" data-msg="{esc(f"Hola, no sé cuál es el filtro de mi nevecón {marca}. Les mando una foto del filtro viejo o de la etiqueta para que me digan cuál es y el precio contra entrega.")}"><span>📷</span><b>No sé cuál es</b><small>Te mando una foto</small></button></div>'
             + f'<div class="elegido" id="elegido" hidden><p id="elegido-txt"></p><a class="btn wa" data-wa="elegir" id="elegido-btn" href="#" target="_blank" rel="noopener">{ICONO_WA}Confirmar por WhatsApp</a></div>', id_="cual")
    c += sec(cab(f"Catálogo {marca}", "Escoge tu filtro y pide el precio de hoy", f"Internos y externos para {esc(cfg['lineas'])}. Toca la lupa de cada foto para ver sus especificaciones y cómo se instala. Todos con pago contra entrega.") + f'<div class="grid">{tarjetas}</div>', alt=True, id_="filtros")
    c += bloque_porque(marca)
    c += bloque_cuando(marca, cfg)
    c += sec(f'''<div class="sint"><div>{cab("Revisa en 20 segundos", "¿Ya le toca el cambio a tu filtro?", "Marca lo que le pasa a tu nevecón.")}
    <div class="checks" id="checks">{"".join(f'<label><input type="checkbox" value="{esc(s)}">{esc(s)}</label>' for s in SINTOMAS)}</div></div>
    <div class="veredicto"><span class="n" id="v-n">0/{len(SINTOMAS)}</span><b id="v-t" style="font-size:20px">Marca lo que te pasa</b><p id="v-p">Si marcas una o más, tu filtro ya está saturado y el agua y el hielo no se están filtrando bien.</p>
      <a class="btn wa" data-wa="sintomas" id="v-btn" href="{esc(wa(n, hola))}" target="_blank" rel="noopener">{ICONO_WA}Quiero cambiarlo</a></div></div>''')
    c += bloque_alerta(marca, cfg, ps)
    c += sec(f'<div class="dos"><div>{cab("Paso a paso", f"Cómo instalar cada filtro de nevecón {marca}", "Toca tu referencia y sigue los pasos. Cada una trae dónde va, cuánto tarda, qué necesitas y cómo apagar la alerta. Al terminar, el agua y el hielo salen limpios otra vez.")}</div>{figura("agua")}</div>'
             + "".join(detalle_instalacion(p, marca, cfg) for p in ps), alt=True, id_="instalar")
    c += sec(cab("Referencias", f"Referencias, equivalencias y nevecones {marca}", f"Busca la referencia impresa en tu filtro viejo o el modelo de tu nevecón. La etiqueta del modelo está {esc(cfg['etiqueta'])}.") + tabla_compat(ps))
    c += bloque_entrega()
    c += sec(f'''<div class="promo"><span class="sello"><span><b>2x</b>Pack anual</span></span>
    <div><h3>Pregunta por el pack de 2 filtros</h3><p>Un filtro dura 6 meses: con el pack tienes agua limpia todo el año y pagas menos por cada uno. El precio especial te lo damos por WhatsApp.</p></div>
    <a class="btn wa" data-wa="pack" href="{esc(wa(n, f'Hola, quiero el precio del pack de 2 filtros para mi nevecón {marca} con pago contra entrega.'))}" target="_blank" rel="noopener">{ICONO_WA}Precio del pack</a></div>''')
    c += sec(cab("Preguntas frecuentes", "Resolvemos tus dudas", centrado=True) + faq_html(preguntas), alt=True)
    c += sec(cab("Envíos contra entrega", "Llegamos a tu ciudad", f"Toca tu ciudad para ver cómo recibir tu filtro {esc(marca)} y pagar al recibir. Y llegamos a más municipios de Colombia.", True) + '<div class="chips" style="justify-content:center">' + "".join(f'<a href="/purofiltro-marca/{slug(marca)}/{slug(x)}/">{esc(x)}</a>' for x, _ in ciud[:24]) + '</div><details class="todas"><summary>Ver las ' + str(len(ciud)) + ' ciudades</summary><div class="chips" style="justify-content:center">' + "".join(f'<a href="/purofiltro-marca/{slug(marca)}/{slug(x)}/">{esc(x)}</a>' for x, _ in ciud[24:]) + "<span>y más municipios</span></div></details>")
    c += sec(f'''<div class="final"><h2>¿Listo para tener agua limpia otra vez?</h2><p>Escríbenos y te decimos cuál es tu filtro y el precio de hoy. Pagas cuando te llega.</p>
    <a class="btn wa" data-wa="final" href="{esc(wa(n, hola))}" target="_blank" rel="noopener">{ICONO_WA}Escribir por WhatsApp</a></div>''', estilo="padding-top:0")
    return c + pie(marca, cfg) + script(marca, cfg, con_picks=True, con_sintomas=True, total_sintomas=len(SINTOMAS))


def pagina_ciudad(marca, cfg, ps, ciudad, depto, ciud):
    n = cfg["whatsapp"]
    envio = "Envío gratis" if ENVIO_GRATIS else "Envío"
    hola = f"Hola, quiero un filtro de agua para mi nevecón {marca} con pago contra entrega en {ciudad}."
    base = f"/purofiltro-marca/{slug(marca)}/"
    ruta = f"{base}{slug(ciudad)}/"
    dias = "2 a 3 días hábiles"
    titulo = f"Filtro de agua nevecón {marca} en {ciudad} | Paga contra entrega"
    desc = f"Filtros de agua para nevecones {marca} en {ciudad}, {depto}: pagas al recibir y llega en {dias}. Te decimos cuál es tu filtro por WhatsApp."
    preguntas = [
        (f"¿Puedo pagar contra entrega en {ciudad}?", f"Sí. Te lo llevamos a {ciudad} y le pagas en efectivo al mensajero cuando lo recibes. No pagas nada por adelantado."),
        (f"¿Cuánto tarda en llegar a {ciudad}?", f"Normalmente {dias} después de confirmar tu pedido por WhatsApp. Te mandamos el número de guía para que sigas el paquete."),
        (f"¿Qué filtro usa mi nevecón {marca}?", f"Mándanos por WhatsApp una foto del filtro viejo o de la etiqueta del nevecón y te decimos cuál es. La etiqueta del modelo está {cfg['etiqueta']}."),
        ("¿Cada cuánto se cambia el filtro?", "Cada 6 meses, o antes si el agua cambia de sabor, si el dispensador bota menos agua o si aparece la alerta en la pantalla."),
    ]
    tarjetas = "".join(f'''
      <article class="card">
        <span class="tipo">{"Externo · manguera" if p["externo"] else "Interno"}</span>
        <div class="im"><picture><source srcset="/purofiltro-img/{p["id"]}-400.webp" type="image/webp"><img src="/purofiltro-img/{p["id"]}.jpg" alt="{esc(p["largo"])} para nevecón {esc(marca)}" width="400" height="400" loading="lazy"></picture>{lupa_btn(p)}</div>
        <div class="tx">
          <h3><a href="/purofiltro-filtro/{p["slug"]}/">{esc(p["largo"])}</a></h3>
          <span class="ref">Ref. {esc(p["ref"])}</span>
          <a class="btn wa" data-wa="tarjeta" href="{esc(wa(n, f'Hola, quiero el precio de hoy del {p["largo"]} para mi nevecón {marca}, con pago contra entrega en {ciudad}.'))}" target="_blank" rel="noopener">{ICONO_WA}Pedir en {esc(ciudad)}</a>
          <a class="mas" href="/purofiltro-filtro/{p["slug"]}/">Ver ficha, instalación y cuándo cambiarlo →</a>
          <div class="pie-card"><span>💵 Pagas al recibir</span><span>🚚 {envio}</span></div>
        </div>
        {lupa_dialog(p, marca, cfg)}
      </article>''' for p in ps)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "name": titulo, "url": BASE + ruta, "inLanguage": "es-CO", "description": desc},
        miga_ld([("Inicio", "/"), (f"Filtros {marca}", base), (ciudad, None)]), faq_ld(preguntas)]}
    c = cabeza(marca, cfg, titulo, desc, ruta, ld, f"/purofiltro-img/{ps[0]['id']}.jpg")
    c += f"""
<section class="hero"><div class="w">
  <div>
    <span class="cod"><i>💵</i>Pago contra entrega en {esc(ciudad)}</span>
    <h1>Filtro de agua para tu nevecón <em>{esc(marca)}</em> en {esc(ciudad)}</h1>
    <p class="lead">Recibe el filtro en {esc(ciudad)} ({esc(depto)}) y págalo en efectivo cuando llegue. No adelantas nada. Por WhatsApp te confirmamos cuál es el que necesita tu nevecón.</p>
    <div class="acc"><a class="btn wa" data-wa="portada" href="{esc(wa(n, hola))}" target="_blank" rel="noopener">{ICONO_WA}Pedir por WhatsApp</a><a class="btn claro" href="{base}">Ver todos los filtros {esc(marca)}</a></div>
    <ul><li>Pagas al recibir</li><li>{envio}</li><li>Llega en {dias}</li><li>Para {esc(cfg["lineas"])}</li></ul>
  </div>
  <div class="vis">
    <span class="f f1"><picture><source srcset="/purofiltro-img/{ps[0]['id']}.webp" type="image/webp"><img src="/purofiltro-img/{ps[0]['id']}.jpg" alt="Filtro de agua para nevecón {esc(marca)} en {esc(ciudad)}" width="600" height="600"></picture></span>
    <span class="globo"><b>● WhatsApp</b>Mándanos una foto de tu filtro viejo y te decimos cuál es y el precio de hoy.</span>
  </div>
</div></section>
"""
    c += sec(cab(f"Catálogo {marca} en {ciudad}", "Escoge tu filtro y pide el precio de hoy", f"Internos y externos para {esc(cfg['lineas'])}. Toca la lupa de cada foto para ver sus especificaciones y cómo se instala. Pagas al recibir en {esc(ciudad)}.") + f'<div class="grid">{tarjetas}</div>')
    c += bloque_entrega()
    c += sec(cab("Preguntas frecuentes", f"Filtros {marca} en {ciudad}", centrado=True) + faq_html(preguntas), alt=True)
    otras = "".join(f'<a href="{base}{slug(x)}/">{esc(x)}</a>' for x, _ in ciud if x != ciudad)
    c += sec(cab("Más ciudades", f"Filtros {marca} en otras ciudades de Colombia", "Pagas al recibir en todas.") + f'<div class="chips">{otras}</div><p style="margin-top:16px"><a href="{base}">← Volver a todos los filtros {esc(marca)}</a></p>')
    c += sec(f'''<div class="final"><h2>¿Listo para tener agua limpia otra vez?</h2><p>Escríbenos y te decimos cuál es tu filtro y el precio de hoy. Pagas cuando te llega a {esc(ciudad)}.</p>
    <a class="btn wa" data-wa="final" href="{esc(wa(n, hola))}" target="_blank" rel="noopener">{ICONO_WA}Escribir por WhatsApp</a></div>''', estilo="padding-top:0")
    return c + pie(marca, cfg) + script(marca, cfg)


# ---------- página de cada filtro ----------
def pagina_producto(p, marca, cfg, ps):
    n = cfg["whatsapp"]
    d = p["datos"]
    envio = "Envío gratis" if ENVIO_GRATIS else "Envío"
    ruta = f"/purofiltro-filtro/{p['slug']}/"
    alias = [r for r in p["refs"] if norm(r) != norm(p["ref"])]
    otros = [x for x in ps if x["id"] != p["id"]]
    info = marcas_exclusivas.MARCAS_INFO[marca]
    msg = f'Hola, quiero el precio de hoy del {p["largo"]} para mi nevecón {marca}, con pago contra entrega.'
    titulo = f'{p["largo"]} para nevecón {marca} | Paga contra entrega'
    desc = (f'Filtro de agua {p["largo"]} para nevecón {marca}: pagas al recibir y {envio.lower()} a toda Colombia. Cuándo cambiarlo, qué significa la alerta '
            f'de la pantalla y cómo se instala paso a paso.')
    preguntas = [
        (f"¿Para qué nevecones sirve el {p['ref']}?", (f"Sirve en nevecones {marca} como: {', '.join(p['modelos'])}, entre otros. " if p["modelos"] else "") + "Compara la referencia impresa en tu filtro viejo o escríbenos por WhatsApp con el modelo de tu nevecón."),
        (f"¿Qué otras referencias son iguales al {p['ref']}?", ("También aparece como " + ", ".join(alias) + ".") if alias else f"Búscalo por la referencia {p['ref']} impresa en tu filtro viejo."),
        ("¿Cada cuánto se cambia?", "Cada 6 meses, o antes si el agua cambia de sabor u olor, baja la presión del dispensador o aparece la alerta en la pantalla."),
        ("¿Cómo apago la alerta del filtro después de cambiarlo?", d["reset"]),
        ("¿Cómo funciona el pago contra entrega?", "Nos escribes por WhatsApp, confirmamos tu filtro y tu dirección, y te lo enviamos. Le pagas en efectivo al mensajero cuando lo recibes. No pagas nada antes."),
        ("¿Cuánto cuesta?", "Te damos el precio del día por WhatsApp, junto con la promoción del pack de 2 filtros, después de confirmar que es el filtro de tu nevecón."),
    ]
    tut = instalacion.tutorial_ld(p, BASE + ruta, p["largo"])
    tut["step"] = [{**s, "url": BASE + ruta + "#instalacion"} for s in tut["step"]]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Product", "name": p["largo"], "image": f"{BASE}/purofiltro-img/{p['id']}.jpg", "sku": p["ref"], "mpn": p["ref"], "brand": {"@type": "Brand", "name": marca},
         "description": f"Filtro de agua para nevecón {marca}, referencia {p['ref']}. " + (p.get("desc") or "")},
        miga_ld([("Inicio", "/"), (f"Filtros {marca}", f"/purofiltro-marca/{slug(marca)}/"), (p["largo"], None)]), tut, faq_ld(preguntas)]}
    c = cabeza(marca, cfg, titulo, desc, ruta, ld, f"/purofiltro-img/{p['id']}.jpg")
    c += f'''<div class="w"><nav class="migas"><a href="/">Inicio</a> › <a href="/purofiltro-marca/{slug(marca)}/">Filtros {esc(marca)}</a> › {esc(p["largo"])}</nav></div>
<section class="sec" style="padding-top:22px"><div class="w pdp">
  <div class="foto"><picture><source srcset="/purofiltro-img/{p["id"]}.webp" type="image/webp"><img src="/purofiltro-img/{p["id"]}.jpg" alt="{esc(p["largo"])} para nevecón {esc(marca)}" width="600" height="600" fetchpriority="high"></picture>{lupa_btn(p)}{lupa_dialog(p, marca, cfg)}</div>
  <div class="info">
    <span class="eye">Filtro de agua para nevecón {esc(marca)} · {"Externo, va en la manguera" if p["externo"] else "Interno"}</span>
    <h1>{esc(p["largo"])}</h1>
    <p class="sub">Referencia <b>{esc(p["ref"])}</b>{(" · también aparece como " + esc(", ".join(alias[:4]))) if alias else ""}</p>
    <div class="cod-big"><span>💵</span><span><b>Paga contra entrega</b><small>Pagas en efectivo cuando te llega. {envio} a toda Colombia.</small></span></div>
    <a class="btn wa" data-wa="ficha" href="{esc(wa(n, msg))}" target="_blank" rel="noopener">{ICONO_WA}Precio de hoy por WhatsApp</a>
    <p>{esc(p.get("desc") or "")}</p>
    <ul class="lista"><li>Te confirmamos por WhatsApp que es el de tu nevecón antes de enviarlo.</li><li>{"Se instala en 10 a 15 minutos en la manguera del agua" if p["externo"] else "Se cambia en 2 minutos y sin herramientas"}: paso a paso más abajo.</li><li>Llega en 2 a 3 días hábiles a las principales ciudades.</li></ul>
    {f'<p class="nota" style="margin:0">{esc(p["nota"])}</p>' if p.get("nota") else ""}
  </div>
</div></section>
'''
    c += sec(f'<div class="dos"><div>{cab("Mantenimiento", f"¿Cuándo cambiar el {p['ref']}?", "Cada <b>6 meses</b> de uso normal, o antes si notas alguna de estas señales.")}</div>{figura("alerta")}</div>' + f'''<div class="cols">
    <div class="bloque"><div class="ic">👅</div><h3>Sabor u olor raro</h3><p>El agua o el hielo saben a cloro, a tierra o a encerrado.</p></div>
    <div class="bloque"><div class="ic">💧</div><h3>Menos presión</h3><p>El dispensador bota menos agua o tarda más en llenar el vaso.</p></div>
    <div class="bloque"><div class="ic">🧊</div><h3>Hielo turbio</h3><p>El hielo sale turbio, pequeño o la máquina produce menos.</p></div>
    <div class="bloque"><div class="ic">🔔</div><h3>Alerta en la pantalla</h3><p>{esc(info["aviso"])}</p></div></div>''', alt=True, id_="cuando")
    c += sec(f'''<div class="alerta"><div>{display_mock(cfg, marca)}</div>
    <div>{cab("Pantalla del nevecón", "Cómo apagar la alerta del filtro", "Después de cambiar el filtro hay que reiniciar el aviso, porque el nevecón cuenta el tiempo de uso y no sabe que ya pusiste uno nuevo.")}
    <div class="reset"><b>Para el {esc(p["ref"])}:</b> {esc(d["reset"])}</div></div></div>''', id_="alerta")
    c += sec(f'<div class="dos"><div>{cab("Paso a paso", f"Cómo instalar el filtro {p['ref']}", esc(d["donde"]) + " Al terminar, el agua y el hielo salen limpios otra vez.")}</div>{figura("agua")}</div>' + f'''<div class="bloque" id="instalacion" style="display:flex;flex-direction:column;gap:16px">
    <dl class="datos"><dt>Dónde va</dt><dd>{esc(d["donde"])}</dd><dt>Tiempo</dt><dd>{esc(d["tiempo"])}</dd><dt>Herramientas</dt><dd>{esc(d["herramientas"])}</dd></dl>
    <ol class="pasos2">{"".join(f"<li>{esc(x)}</li>" for x in d["pasos"])}</ol>
    <div class="reset"><b>Último paso:</b> {esc(d["reset"])}</div>
    <p class="nota" style="margin:0">Los primeros vasos de agua pueden salir turbios o con burbujas: es normal y se aclara en unos minutos. Bota el primer hielo que salga después del cambio. Si gotea, saca el filtro y vuelve a meterlo derecho hasta que quede firme.</p>
    <div class="acc2"><a class="btn wa" data-wa="instalacion" href="{esc(wa(n, msg))}" target="_blank" rel="noopener">{ICONO_WA}Pedirlo contra entrega</a></div></div>''', alt=True)
    if p["modelos"] or alias:
        c += sec(cab("Nevecones", f"Nevecones y referencias del {p['ref']}") + (f'<p style="margin-bottom:10px;font-weight:700">Nevecones {esc(marca)} que lo usan, entre otros:</p><div class="chips">{"".join(f"<span>{esc(m)}</span>" for m in p["modelos"])}</div>' if p["modelos"] else "")
                 + (f'<p style="margin:22px 0 10px;font-weight:700">También aparece como:</p><div class="chips">{"".join(f"<span>{esc(r)}</span>" for r in alias)}</div>' if alias else "")
                 + f'<p class="nota">La etiqueta con el modelo de tu nevecón está {esc(cfg["etiqueta"])}.</p>')
    c += bloque_entrega()
    c += sec(cab("Preguntas frecuentes", f"Preguntas sobre el {p['ref']}", centrado=True) + faq_html(preguntas))
    if otros:
        c += sec(cab(f"Más filtros {marca}", "Otras referencias para tu nevecón") + '<div class="chips">' + "".join(f'<a href="/purofiltro-filtro/{x["slug"]}/">{esc(x["ref"])}</a>' for x in otros) + f'<a href="/purofiltro-marca/{slug(marca)}/#filtros">Ver todos los filtros {esc(marca)}</a></div>')
    c += sec(f'''<div class="final"><h2>Pide tu {esc(p["ref"])} y paga cuando te llegue</h2><p>Escríbenos, confirmamos que es el de tu nevecón y te decimos el precio de hoy.</p>
    <a class="btn wa" data-wa="final" href="{esc(wa(n, msg))}" target="_blank" rel="noopener">{ICONO_WA}Escribir por WhatsApp</a></div>''', estilo="padding-top:0")
    return c + pie(marca, cfg, f"Pide tu {p['ref']}") + script(marca, cfg)


def legal(tipo):
    n = MARCAS["Whirlpool"]["whatsapp"]  # teléfono general de la tienda: el 321
    tel = f"{n[:3]} {n[3:6]} {n[6:]}"
    if tipo == "datos":
        titulo, cuerpo = "Tratamiento de datos personales", f"""
<p>{esc(NEGOCIO)} usa tu nombre, celular, dirección y ciudad solo para confirmar tu pedido, enviarlo y darte asesoría sobre tu filtro, según la Ley 1581 de 2012.</p>
<p>No vendemos ni compartimos tus datos con terceros, salvo con la transportadora que entrega tu pedido. No te enviaremos publicidad si no la pides.</p>
<p>Puedes conocer, actualizar o pedir que borremos tus datos escribiéndonos por WhatsApp al {tel}.</p>
<p>Estas páginas usan Google Tag Manager para medir cuántas personas nos escriben por WhatsApp; no guarda tu nombre ni tus mensajes.</p>"""
    else:
        titulo, cuerpo = "Términos del pago contra entrega", f"""
<p><b>Pedido:</b> se hace por WhatsApp. Antes de enviarlo te confirmamos la referencia del filtro, el precio total y la dirección.</p>
<p><b>Pago:</b> pagas en efectivo a la transportadora cuando recibes el paquete. No pedimos pagos por adelantado.</p>
<p><b>Envío:</b> {"gratis " if ENVIO_GRATIS else ""}a toda Colombia. A las principales ciudades llega en 2 a 3 días hábiles; a otros municipios puede tardar más. Te enviamos el número de guía.</p>
<p><b>Retracto y garantía:</b> tienes 5 días hábiles para retractarte con el filtro sin instalar y en su empaque, y la garantía legal de la Ley 1480 de 2011 si llega con un defecto de fábrica. Escríbenos por WhatsApp.</p>
<p><b>Marcas:</b> Samsung, LG, Whirlpool y GE son marcas registradas de sus dueños; las mencionamos solo para indicar en qué nevecones sirve cada filtro.</p>"""
    return f"""<!doctype html><html lang="es-CO"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titulo} | {esc(NEGOCIO)}</title><meta name="robots" content="noindex"><meta name="google-site-verification" content="{VERIFICACION}">
<style>body{{margin:0;font-family:system-ui,-apple-system,"Segoe UI",sans-serif;color:#121726;background:#f5f7fb;line-height:1.65}}main{{max-width:760px;margin:0 auto;padding:40px 16px 60px}}
h1{{font-size:30px;line-height:1.15;margin:0 0 18px}}p{{margin:0 0 14px}}a{{color:#1428a0;font-weight:700}}.c{{background:#fff;border:1px solid #e3e6ee;border-radius:18px;padding:24px}}</style></head>
<body><main><p><a href="/">← Volver a la tienda</a></p><div class="c"><h1>{titulo}</h1>{cuerpo}</div></main></body></html>"""


def escribir(carpeta, contenido):
    """index.html y una copia index.php: la copia pisa la página vieja de la tienda sin tocar nada más."""
    assert "<?" not in contenido, "el HTML no puede traer «<?» (PHP lo leería como código)"
    carpeta.mkdir(parents=True, exist_ok=True)
    (carpeta / "index.html").write_text(contenido, encoding="utf-8")
    (carpeta / "index.php").write_text(contenido, encoding="utf-8")


def main():
    if not FOTOS.exists():
        sys.exit("Primero corre build.py: faltan las fotos en public_html/purofiltro-img")
    cat, ciud = catalogo(), ciudades()
    if SALIDA.exists():
        shutil.rmtree(SALIDA)
    (SALIDA / "purofiltro-img").mkdir(parents=True)
    paginas = 0
    for m in MARCAS:
        MENU[m] = [(p["ref"], p["slug"]) for p in cat if p["marca"] == m]
    for marca, cfg in MARCAS.items():
        ps = [p for p in cat if p["marca"] == marca]
        for p in ps:
            for suf in (".jpg", ".webp", "-400.webp"):
                shutil.copy(FOTOS / f"{p['id']}{suf}", SALIDA / "purofiltro-img" / f"{p['id']}{suf}")
            escribir(SALIDA / "purofiltro-filtro" / p["slug"], pagina_producto(p, marca, cfg, ps)); paginas += 1
        escribir(SALIDA / "purofiltro-marca" / slug(marca), pagina_marca(marca, cfg, ps, ciud)); paginas += 1
        for ciudad, depto in ciud:
            escribir(SALIDA / "purofiltro-marca" / slug(marca) / slug(ciudad), pagina_ciudad(marca, cfg, ps, ciudad, depto, ciud)); paginas += 1
        print(f"{marca}: portada + {len(ps)} filtros · WhatsApp {cfg['whatsapp']}")
    from PIL import Image
    for archivo, nombre, _ in IMAGENES.values():
        im = Image.open(AQUI / "imagenes-ads" / f"{archivo}.jpg").convert("RGB")
        im.save(SALIDA / "purofiltro-img" / f"{nombre}.jpg", quality=84, optimize=True, progressive=True)
        im.save(SALIDA / "purofiltro-img" / f"{nombre}.webp", "WEBP", quality=80, method=6)
        im.resize((640, round(640 * im.height / im.width)), Image.LANCZOS).save(SALIDA / "purofiltro-img" / f"{nombre}-640.webp", "WEBP", quality=80, method=6)
    d = SALIDA / "purofiltro-contraentrega"
    d.mkdir(parents=True)
    (d / "datos.html").write_text(legal("datos"), encoding="utf-8")
    (d / "terminos.html").write_text(legal("terminos"), encoding="utf-8")
    (SALIDA / "LEEME.txt").write_text(
        "PÁGINAS DE GOOGLE ADS (PAGO CONTRA ENTREGA)\n\n"
        "1. En Hostinger abre el Administrador de archivos > public_html y sube este zip.\n"
        "2. Extráelo AHÍ MISMO y di que sí a reemplazar los archivos. Quedan en las mismas direcciones de tus anuncios:\n"
        "   /purofiltro-marca/samsung/  /lg/  /whirlpool/  /ge/   y   /purofiltro-filtro/<filtro>/\n"
        "3. Abre las 4 direcciones en el celular y revisa que salga la página nueva (sello «Paga contra entrega»).\n"
        "4. En Search Console pide indexar de nuevo esas 4 direcciones.\n\n"
        "Cada marca usa su número de WhatsApp (se cambia en ads_marcas.py y se vuelve a generar).\n"
        "Para volver a la página anterior de una marca, genera de nuevo la tienda con build.py y sube esa carpeta.\n", encoding="utf-8")
    shutil.make_archive(str(AQUI / "anuncios-contra-entrega"), "zip", SALIDA)
    print(f"Listo: {paginas} páginas en sitios-ads/ y anuncios-contra-entrega.zip")


if __name__ == "__main__":
    main()
