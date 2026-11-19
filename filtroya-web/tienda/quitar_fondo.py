#!/usr/bin/env python3
"""Quita el fondo blanco de fotos de repuestos y las deja cuadradas (800x800, PNG/WebP transparente).
Uso: python3 quitar_fondo.py carpeta_entrada carpeta_salida
Funciona con fondo blanco o casi blanco (foto de estudio). Requiere Pillow: pip install pillow"""
import sys, os
from collections import deque
from PIL import Image, ImageFilter
UMBRAL = 246  # qué tan blanco debe ser un píxel para contarse como fondo
def procesar(ruta, destino, lado=1200):
    im = Image.open(ruta)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA"); _b = Image.new("RGBA", im.size, (255, 255, 255, 255)); _b.alpha_composite(im); im = _b
    im = im.convert("RGB"); w, h = im.size; px = im.load()
    fondo = [[False] * w for _ in range(h)]
    q = deque()
    for x in range(w):
        q.append((x, 0)); q.append((x, h - 1))
    for y in range(h):
        q.append((0, y)); q.append((w - 1, y))
    while q:
        x, y = q.popleft()
        if x < 0 or y < 0 or x >= w or y >= h or fondo[y][x]: continue
        r, g, b = px[x, y]
        if min(r, g, b) < UMBRAL: continue
        fondo[y][x] = True
        q.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    mask = Image.new("L", (w, h), 255); mp = mask.load()
    for y in range(h):
        for x in range(w):
            if fondo[y][x]: mp[x, y] = 0
    mask = mask.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
    out = im.convert("RGBA"); out.putalpha(mask)
    bb = out.getbbox()
    if bb: out = out.crop(bb)
    s = int(lado * 0.88); e = s / max(out.size)
    out = out.resize((max(1, round(out.width * e)), max(1, round(out.height * e))), Image.LANCZOS)
    if e > 1:
        rgb = out.convert("RGB").filter(ImageFilter.UnsharpMask(radius=1.6, percent=90, threshold=2)); rgb.putalpha(out.getchannel("A")); out = rgb
    lienzo = Image.new("RGBA", (lado, lado), (0, 0, 0, 0))
    lienzo.paste(out, ((lado - out.width) // 2, (lado - out.height) // 2), out)
    lienzo.save(destino)
if __name__ == "__main__":
    ent, sal = sys.argv[1], sys.argv[2]; os.makedirs(sal, exist_ok=True)
    for f in sorted(os.listdir(ent)):
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            procesar(os.path.join(ent, f), os.path.join(sal, os.path.splitext(f)[0] + ".webp")); print("listo", f)
