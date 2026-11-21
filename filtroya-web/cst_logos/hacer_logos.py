# -*- coding: utf-8 -*-
"""Genera los logos PNG con fondo transparente: <marca>.png (color, para fondo claro) y <marca>-blanco.png (para fondo oscuro)."""
import numpy as np, pathlib
from PIL import Image
from collections import deque
AQUI = pathlib.Path(__file__).resolve().parent
S = pathlib.Path("/home/user/s")
SRC = {"samsung": S / "servicio-tecnico-samsung-panama/images/logo/samsung-marca.png", "lg": S / "servicio-tecnico-lg-panama/images/logo/lg-marca.png",
       "whirlpool": S / "servicio-tecnico-whirlpool-panama/images/logo/whirlpool-marca.png", "mabe": S / "mabe-quito/img/mabe-logo.png",
       "electrolux": pathlib.Path("/tmp/cst_src/electrolux/logo-electrolux.webp"), "frigidaire": pathlib.Path("/tmp/claude-0/-home-user-s/7394aa38-735a-5cd1-af51-c01a7780d2eb/images/54.webp"),
       "general-electric": pathlib.Path("/tmp/claude-0/-home-user-s/7394aa38-735a-5cd1-af51-c01a7780d2eb/images/53.png"),
       "haceb": pathlib.Path("/tmp/cst_src/haceb/logo-haceb.webp"), "kitchenaid": pathlib.Path("/tmp/cst_src/kitchenaid/logo-kitchenaid.webp")}
def procesar(m, f):
    im = Image.open(f).convert("RGBA"); a = np.array(im).astype(np.float32)
    rgb, al = a[..., :3], a[..., 3] / 255
    comp = rgb * al[..., None] + 255 * (1 - al[..., None])          # sobre blanco
    mn = comp.min(axis=2)
    h, w = mn.shape
    cercano = (mn > 236)
    fuera = np.zeros((h, w), bool); q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if cercano[y, x] and not fuera[y, x]: fuera[y, x] = True; q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if cercano[y, x] and not fuera[y, x]: fuera[y, x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and cercano[ny, nx] and not fuera[ny, nx]: fuera[ny, nx] = True; q.append((ny, nx))
    # color: el fondo exterior pasa a transparente (con suavizado en el borde); lo blanco interior se conserva
    from PIL import ImageFilter
    suave = np.array(Image.fromarray((fuera * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))).astype(np.float32) / 255
    alfa = np.clip(1 - suave, 0, 1) * al
    color = np.dstack([rgb, alfa * 255]).astype(np.uint8)
    # blanco: lo coloreado pasa a blanco, lo blanco interior queda transparente
    a_b = np.clip((236 - mn) / (236 - 150), 0, 1)
    a_b = np.where(fuera, 0, a_b)
    blanco = np.dstack([np.full((h, w, 3), 255), a_b * 255]).astype(np.uint8)
    out = {}
    for nombre, arr in (("", color), ("-blanco", blanco)):
        img = Image.fromarray(arr, "RGBA"); bb = img.getbbox()
        if bb: img = img.crop((max(bb[0] - 2, 0), max(bb[1] - 2, 0), min(bb[2] + 2, img.width), min(bb[3] + 2, img.height)))
        img.thumbnail((600, 200)); img.save(AQUI / f"{m}{nombre}.png", optimize=True)
if __name__ == "__main__":
    import sys
    solo = sys.argv[1:] or list(SRC)
    for m, f in SRC.items():
        if m in solo: procesar(m, f); print("ok", m)
