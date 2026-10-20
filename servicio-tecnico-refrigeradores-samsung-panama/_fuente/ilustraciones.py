# -*- coding: utf-8 -*-
"""Ilustraciones vectoriales (SVG) de refrigeradoras. Se usan mientras no haya fotos propias en _fuente/fotos/."""
GRAD = '''<defs><linearGradient id="{p}c" x1="0" x2="1"><stop offset="0" stop-color="#e9edf5"/><stop offset=".5" stop-color="#f8fafd"/><stop offset="1" stop-color="#cfd6e6"/></linearGradient>
<linearGradient id="{p}d" x1="0" x2="1"><stop offset="0" stop-color="#d6dcea"/><stop offset=".55" stop-color="#f4f6fb"/><stop offset="1" stop-color="#bcc5da"/></linearGradient>
<linearGradient id="{p}s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b2e8f"/><stop offset="1" stop-color="#0a1460"/></linearGradient></defs>'''

def _door(x, y, w, h, p, r=10):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#{p}c)" stroke="#aab4cc" stroke-width="1.5"/>'

def _handle(x, y, h, vertical=True):
    return f'<rect x="{x}" y="{y}" width="{6 if vertical else h}" height="{h if vertical else 6}" rx="3" fill="#8e99b5"/>'

def fridge(kind, uid="a"):
    p = uid
    W, H = 300, 360
    body = f'<ellipse cx="150" cy="346" rx="105" ry="9" fill="#0a1460" opacity=".12"/>'
    if kind == "side-by-side":
        s = (_door(60, 20, 84, 316, p) + _door(148, 20, 92, 316, p) + _handle(131, 150, 70) + _handle(152, 150, 70)
             + f'<rect x="72" y="70" width="60" height="120" rx="8" fill="#e1e6f2" stroke="#aab4cc"/><rect x="84" y="82" width="36" height="14" rx="3" fill="url(#{p}s)"/><rect x="88" y="130" width="28" height="44" rx="5" fill="#cfd8f0"/><path d="M96 138h12v26H96z" fill="#8fb8ff" opacity=".7"/>')
    elif kind == "french-door":
        s = (_door(50, 20, 98, 214, p) + _door(152, 20, 98, 214, p) + _door(50, 238, 200, 98, p) + _handle(132, 90, 70) + _handle(162, 90, 70) + _handle(120, 252, 60, False)
             + f'<circle cx="100" cy="60" r="4" fill="#1b2e8f"/>')
    elif kind == "top-mount":
        s = (_door(70, 20, 160, 100, p) + _door(70, 124, 160, 212, p) + _handle(212, 60, 40) + _handle(212, 150, 70))
    elif kind == "bottom-mount":
        s = (_door(70, 20, 160, 232, p) + _door(70, 256, 160, 80, p) + _handle(212, 90, 80) + _handle(110, 268, 80, False))
    elif kind == "family-hub":
        s = (_door(50, 20, 98, 214, p) + _door(152, 20, 98, 214, p) + _door(50, 238, 200, 98, p) + _handle(132, 90, 60) + _handle(162, 150, 60)
             + f'<rect x="172" y="48" width="62" height="88" rx="6" fill="url(#{p}s)"/><rect x="178" y="56" width="50" height="10" rx="2" fill="#8fb8ff"/><rect x="178" y="72" width="22" height="22" rx="3" fill="#3a56d4"/><rect x="204" y="72" width="24" height="22" rx="3" fill="#6f86ee"/><rect x="178" y="100" width="50" height="8" rx="2" fill="#3a56d4"/>')
    else:  # con-dispensador
        s = (_door(60, 20, 84, 316, p) + _door(148, 20, 92, 316, p) + _handle(131, 170, 70) + _handle(152, 170, 70)
             + f'<rect x="70" y="60" width="64" height="150" rx="10" fill="#dfe5f3" stroke="#aab4cc"/><rect x="82" y="72" width="40" height="12" rx="3" fill="url(#{p}s)"/><rect x="84" y="150" width="36" height="46" rx="4" fill="#fff" stroke="#aab4cc"/><path d="M92 158h20v28H92z" fill="#8fb8ff" opacity=".6"/><circle cx="102" cy="124" r="5" fill="#8fb8ff"/><circle cx="116" cy="130" r="4" fill="#bcd4ff"/>')
    return f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img">{GRAD.format(p=p)}{body}{s}</svg>'

def hero(uid="h"):
    p = uid
    f = fridge("french-door", p + "f").replace('<svg viewBox="0 0 300 360" xmlns="http://www.w3.org/2000/svg" role="img">', '').replace("</svg>", "")
    return (f'<svg viewBox="0 0 520 440" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Refrigeradora Samsung con servicio técnico a domicilio">'
            f'<defs><radialGradient id="{p}bg" cx=".5" cy=".4" r=".7"><stop offset="0" stop-color="#ffffff" stop-opacity=".25"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient></defs>'
            f'<circle cx="260" cy="210" r="200" fill="url(#{p}bg)"/><circle cx="260" cy="210" r="168" fill="none" stroke="#ffffff" stroke-opacity=".18" stroke-width="2"/><circle cx="260" cy="210" r="120" fill="none" stroke="#ffffff" stroke-opacity=".12" stroke-width="2"/>'
            f'<g transform="translate(110 30) scale(1.0)">{f}</g>'
            f'<g transform="translate(60 60)"><circle r="34" fill="#25d366"/><path d="M-12 8l-4 14 15-4a18 18 0 1 0-11-10z" fill="none" stroke="#fff" stroke-width="3" stroke-linejoin="round"/></g>'
            f'<g transform="translate(450 110)"><circle r="34" fill="#fff"/><g fill="none" stroke="#1428a0" stroke-width="3" stroke-linecap="round"><path d="M0-18v36M-16-9l32 18M-16 9l32-18"/><path d="M-5-14l5 4 5-4M-5 14l5-4 5 4"/></g></g>'
            f'<g transform="translate(430 330)"><circle r="38" fill="#1428a0" stroke="#fff" stroke-width="3"/><path d="M-12 -4a9 9 0 0 1 12-8l-5 6 3 4 5-1 5-5a9 9 0 0 1-8 12l-14 14-5-5z" fill="#fff"/></g>'
            f'<g transform="translate(90 330)"><rect x="-44" y="-26" width="88" height="52" rx="14" fill="#fff"/><path d="M-22 0l9 9 18-18" fill="none" stroke="#1fa855" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/><text x="14" y="6" font-family="sans-serif" font-size="13" font-weight="800" fill="#0b1440">OK</text></g>'
            f'</svg>')

def pieza(uid="p"):
    return (f'<svg viewBox="0 0 300 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Piezas de refrigeradora"><rect width="300" height="220" rx="18" fill="#e6eaf8"/>'
            f'<g fill="none" stroke="#1428a0" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"><circle cx="95" cy="110" r="46"/><circle cx="95" cy="110" r="10"/><path d="M95 64v26M95 130v26M49 110h26M115 110h26M62 77l18 18M110 125l18 18M128 77l-18 18M80 125l-18 18"/></g>'
            f'<g fill="#fff" stroke="#1428a0" stroke-width="4"><rect x="170" y="62" width="96" height="66" rx="8"/></g><g fill="#1428a0"><rect x="182" y="76" width="30" height="8" rx="2"/><rect x="182" y="92" width="52" height="6" rx="2"/><rect x="182" y="106" width="40" height="6" rx="2"/><circle cx="248" cy="80" r="5"/></g>'
            f'<path d="M180 160c14-14 28 14 42 0s28 14 42 0" fill="none" stroke="#1428a0" stroke-width="5" stroke-linecap="round"/></svg>')

def mapa_zona(uid="m"):
    return (f'<svg viewBox="0 0 300 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Zona de cobertura en Panamá"><rect width="300" height="200" rx="18" fill="#e6eaf8"/>'
            f'<path d="M20 120c40-10 60 20 100 10s60-40 100-30 50 20 60 10" fill="none" stroke="#b6c0e4" stroke-width="22" stroke-linecap="round"/>'
            f'<g fill="#1428a0"><circle cx="90" cy="110" r="9"/><circle cx="150" cy="96" r="9"/><circle cx="215" cy="88" r="9"/><circle cx="125" cy="140" r="7"/><circle cx="185" cy="120" r="7"/></g><circle cx="150" cy="96" r="18" fill="none" stroke="#1428a0" stroke-width="3"/></svg>')
