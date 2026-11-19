#!/usr/bin/env python3
"""Quita el fondo blanco de fotos de repuestos y las deja cuadradas (800x800, PNG/WebP transparente).
Uso: python3 quitar_fondo.py carpeta_entrada carpeta_salida
Funciona con fondo blanco o casi blanco (foto de estudio). Requiere Pillow: pip install pillow"""
import sys, os
from collections import deque
from PIL import Image, ImageFilter
UMBRAL = 232  # qué tan blanco debe ser un píxel para contarse como fondo
def procesar(ruta, destino, lado=800):
    im = Image.open(ruta).convert("RGB"); w, h = im.size; px = im.load()
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
    s = int(lado * 0.86); out.thumbnail((s, s), Image.LANCZOS)
    lienzo = Image.new("RGBA", (lado, lado), (0, 0, 0, 0))
    lienzo.paste(out, ((lado - out.width) // 2, (lado - out.height) // 2), out)
    lienzo.save(destino)
if __name__ == "__main__":
    ent, sal = sys.argv[1], sys.argv[2]; os.makedirs(sal, exist_ok=True)
    for f in sorted(os.listdir(ent)):
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            procesar(os.path.join(ent, f), os.path.join(sal, os.path.splitext(f)[0] + ".webp")); print("listo", f)
