#!/usr/bin/env python3
"""Amplía con inteligencia artificial (EDSR x4, OpenCV) las fotos pequeñas de repuestos/fotos y las guarda en repuestos/sr/.
Uso: python3 mejorar_fotos.py carpeta_fotos carpeta_salida [lado_maximo=700]
Necesita opencv-contrib-python-headless==4.10.0.84 y el modelo tienda/.modelos/EDSR_x4.pb
(https://raw.githubusercontent.com/Saafke/EDSR_Tensorflow/master/models/EDSR_x4.pb). Es lento: ~1 minuto por cada 200.000 píxeles."""
import os, sys, pathlib
from multiprocessing import Pool
import numpy as np
from PIL import Image
MODELO = pathlib.Path(__file__).resolve().parent / ".modelos" / "EDSR_x4.pb"
def trabajo(a):
    import cv2
    ruta, destino = a
    im = Image.open(ruta)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA"); b = Image.new("RGBA", im.size, (255, 255, 255, 255)); b.alpha_composite(im); im = b
    im = im.convert("RGB")
    sr = cv2.dnn_superres.DnnSuperResImpl_create(); sr.readModel(str(MODELO)); sr.setModel("edsr", 4)
    out = sr.upsample(cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR))
    Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB)).save(destino)
    return os.path.basename(ruta)
if __name__ == "__main__":
    ent, sal = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); lado = int(sys.argv[3]) if len(sys.argv) > 3 else 700
    sal.mkdir(parents=True, exist_ok=True); tareas = []
    for f in sorted(ent.iterdir()):
        if f.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp"): continue
        d = sal / (f.stem + ".png")
        if d.exists(): continue
        if max(Image.open(f).size) < lado: tareas.append((str(f), str(d)))
    print(len(tareas), "fotos por ampliar", flush=True)
    with Pool(min(len(tareas) or 1, os.cpu_count() or 2)) as p:
        for n in p.imap_unordered(trabajo, tareas): print("listo", n, flush=True)
