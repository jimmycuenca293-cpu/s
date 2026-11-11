"""Logos de las marcas (los que mandó el dueño): PNG transparente, recortado y nítido.
Lee logos/originales/<marca>-nuevo.* y escribe logos/<marca>-web.png (para el encabezado) y logos/<marca>-icono.png (cuadrado, para el ícono)."""
import pathlib
import numpy as np
from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
ORIG = AQUI / "originales"
ALTO = 200


def recortar(im, margen=0):
    a = np.array(im.getchannel("A"))
    ys, xs = np.where(a > 8)
    return im.crop((max(xs.min() - margen, 0), max(ys.min() - margen, 0), xs.max() + 1 + margen, ys.max() + 1 + margen))


def samsung(im):
    """Letras azules sobre gris claro: el fondo se vuelve transparente con bordes suaves y se conserva el azul exacto del logo."""
    px = np.array(im.convert("RGB")).astype(float)
    fondo, tinta = 247.0, 20.0  # canal rojo: gris claro del fondo y azul del logo
    alfa = np.clip((fondo - px[..., 0]) / (fondo - tinta), 0, 1)
    out = np.zeros(px.shape[:2] + (4,), np.uint8)
    out[..., 0], out[..., 1], out[..., 2] = 20, 40, 160  # azul Samsung
    out[..., 3] = (alfa * 255).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def cuadrado(im, lado=256, relleno=0.12):
    im = im.copy()
    k = lado * (1 - 2 * relleno) / max(im.size)
    im = im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)
    lienzo = Image.new("RGBA", (lado, lado), (0, 0, 0, 0))
    lienzo.paste(im, ((lado - im.width) // 2, (lado - im.height) // 2), im)
    return lienzo


for marca, archivo in (("samsung", "samsung-nuevo.png"), ("lg", "lg-nuevo.webp"), ("whirlpool", "whirlpool-nuevo.webp"), ("ge", "ge-nuevo.png")):
    im = Image.open(ORIG / archivo)
    im = samsung(im) if marca == "samsung" else im.convert("RGBA")
    im = recortar(im, 2)
    web = im.resize((round(im.width * ALTO / im.height), ALTO), Image.LANCZOS) if im.height > ALTO else im
    web.save(AQUI / f"{marca}-web.png", optimize=True)
    icono = im
    if marca == "lg":  # el círculo LG solo, para el ícono
        icono = recortar(im.crop((0, 0, round(im.width * 0.45), im.height)))
    cuadrado(icono).save(AQUI / f"{marca}-icono.png", optimize=True)
    print(marca, web.size)
