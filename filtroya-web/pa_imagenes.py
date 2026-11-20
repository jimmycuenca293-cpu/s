#!/usr/bin/env python3
"""Imágenes más nítidas para un sitio generado (ST_SOLO): amplía con IA (EDSR x4) las pequeñas y reafina todas.
Uso: python3 pa_imagenes.py <carpeta_img_del_sitio> <carpeta_cache_sr> [lado_maximo_SR=830]
Fase 1 (lenta, cacheada): EDSR solo en las imágenes cuyo lado mayor sea < lado_maximo_SR.
Fase 2 (rápida): regenera todas con LANCZOS + máscara de enfoque y WebP de alta calidad; las variantes -s/-m salen del archivo mejorado."""
import os, sys, pathlib, re
from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageFilter
IMG, SR = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); LADO = int(sys.argv[3]) if len(sys.argv) > 3 else 830
MODELO = pathlib.Path(__file__).resolve().parent / "tienda" / ".modelos" / "EDSR_x4.pb"
SR.mkdir(parents=True, exist_ok=True)
base = [f for f in sorted(IMG.glob("*.webp")) if not re.search(r"-(s|m|400)\.webp$", f.name)]
def sr_uno(f):
    import cv2
    destino = SR / (f.stem + ".png")
    if destino.exists(): return f.name
    im = Image.open(f); a = None
    if im.mode in ("RGBA", "LA"):
        a = im.getchannel("A"); fondo = Image.new("RGB", im.size, (255, 255, 255)); fondo.paste(im.convert("RGB"), mask=a); im = fondo
    im = im.convert("RGB")
    m = cv2.dnn_superres.DnnSuperResImpl_create(); m.readModel(str(MODELO)); m.setModel("edsr", 4)
    out = Image.fromarray(cv2.cvtColor(m.upsample(cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)), cv2.COLOR_BGR2RGB))
    if a is not None:
        out = out.convert("RGBA"); out.putalpha(a.resize(out.size, Image.LANCZOS))
    out.save(destino)
    return f.name
def fase2(f, destino_ancho):
    src = SR / (f.stem + ".png")
    im = Image.open(src if src.exists() else f)
    w, h = im.size; k = destino_ancho / max(w, h)
    nuevo = im.resize((max(1, round(w * k)), max(1, round(h * k))), Image.LANCZOS)
    rgb = nuevo.convert("RGB").filter(ImageFilter.UnsharpMask(radius=1.1, percent=70, threshold=2))
    if nuevo.mode == "RGBA":
        rgb = rgb.convert("RGBA"); rgb.putalpha(nuevo.getchannel("A"))
    rgb.save(f, "WEBP", quality=92, method=6)
    for suf, lado in (("-m", 460), ("-s", 240)):
        v = IMG / f"{f.stem}{suf}.webp"
        if v.exists():
            kk = lado / max(rgb.size); rgb.resize((max(1, round(rgb.width * kk)), max(1, round(rgb.height * kk))), Image.LANCZOS).save(v, "WEBP", quality=90, method=6)
if __name__ == "__main__":
    pequenas = [f for f in base if max(Image.open(f).size) < LADO]
    print(len(pequenas), "imágenes por ampliar con IA:", [f.name for f in pequenas], flush=True)
    with Pool(min(4, os.cpu_count() or 2)) as p:
        for n in p.imap_unordered(sr_uno, pequenas): print("listo", n, flush=True)
    for f in base:
        fase2(f, 1600 if (Image.open(f).width / max(1, Image.open(f).height)) > 1.2 else 1200)
    print("fase 2 terminada", flush=True)
