"""Prepara los logos de las marcas (PuroFiltro es distribuidor autorizado) para los sitios por marca.

Lee logos/originales/<marca>.png (las imágenes que mandó el dueño, sin tocar) y deja logos/<marca>.png:
PNG con fondo transparente, recortado al borde del logo y en alta resolución (nítido en pantallas retina).
No se cambia la forma ni los colores del logo, solo se quita el fondo blanco que sobra.

Uso:  python3 logos/preparar_logos.py
"""
import pathlib
from collections import deque

import numpy as np
from PIL import Image, ImageDraw

AQUI = pathlib.Path(__file__).resolve().parent
ALTO_MAX = 360  # px: el logo más grande en la página mide unos 64 px de alto, así queda nítido hasta en 4x


def recortar(im):
    a = np.array(im.getchannel("A"))
    ys, xs = np.where(a > 8)
    return im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))


def fondo_por_relleno(im):
    """Quita el blanco del fondo rellenando desde las esquinas (sirve cuando el logo cierra su borde, como GE)."""
    im = im.convert("RGBA")
    px = np.array(im)
    h, w = px.shape[:2]
    blanco = (px[..., 3] < 10) | ((px[..., 0] > 235) & (px[..., 1] > 235) & (px[..., 2] > 235))
    visto = np.zeros((h, w), bool)
    q = deque([(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)])
    while q:
        x, y = q.popleft()
        if 0 <= x < w and 0 <= y < h and not visto[y, x] and blanco[y, x]:
            visto[y, x] = True
            q.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    px[visto, 3] = 0
    return Image.fromarray(px)


def casco(puntos):
    """Envolvente convexa (cadena monótona)."""
    puntos = sorted(set(puntos))
    def cruz(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    abajo, arriba = [], []
    for p in puntos:
        while len(abajo) >= 2 and cruz(abajo[-2], abajo[-1], p) <= 0:
            abajo.pop()
        abajo.append(p)
    for p in reversed(puntos):
        while len(arriba) >= 2 and cruz(arriba[-2], arriba[-1], p) <= 0:
            arriba.pop()
        arriba.append(p)
    return abajo[:-1] + arriba[:-1]


def fondo_por_ovalo(im):
    """Samsung: las letras blancas tocan el borde del óvalo, así que el fondo se quita con la silueta del óvalo azul."""
    im = im.convert("RGBA")
    px = np.array(im).astype(int)
    azul = (px[..., 2] > 120) & (px[..., 2] - px[..., 0] > 60)
    ys, xs = np.where(azul)
    borde = {}
    for x, y in zip(xs, ys):  # extremos de cada columna bastan para la envolvente
        lo, hi = borde.get(x, (y, y))
        borde[x] = (min(lo, y), max(hi, y))
    pts = [(x, lo) for x, (lo, _) in borde.items()] + [(x, hi) for x, (_, hi) in borde.items()]
    s = 4  # máscara con suavizado para que el borde no quede serruchado
    mascara = Image.new("L", (im.width * s, im.height * s), 0)
    ImageDraw.Draw(mascara).polygon([(x * s + s / 2, y * s + s / 2) for x, y in casco(pts)], fill=255)
    mascara = mascara.resize(im.size, Image.LANCZOS)
    im.putalpha(mascara)
    return im


for marca, metodo in [("lg", None), ("whirlpool", None), ("samsung", fondo_por_ovalo), ("ge", fondo_por_relleno)]:
    im = Image.open(AQUI / "originales" / f"{marca}.png")
    im = metodo(im) if metodo else im.convert("RGBA")
    im = recortar(im)
    if im.height > ALTO_MAX:
        im = im.resize((round(im.width * ALTO_MAX / im.height), ALTO_MAX), Image.LANCZOS)
    im.save(AQUI / f"{marca}.png", optimize=True)
    print(marca, im.size)
