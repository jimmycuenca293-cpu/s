# -*- coding: utf-8 -*-
"""Ensambla centroserviciopanama.com: Samsung en la raíz y LG en /lg/ (una sola URL).
Uso: ejecutar generar.py en servicio-tecnico-samsung-panama/_fuente y servicio-tecnico-lg-panama/_fuente, luego:  python3 ensamblar.py"""
import shutil, zipfile, datetime
from pathlib import Path
AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
S = RAIZ.parent / "servicio-tecnico-samsung-panama"
L = RAIZ.parent / "servicio-tecnico-lg-panama"
DOM = "https://centroserviciopanama.com"
HOY = datetime.date.today().isoformat()
SKIP = {"_fuente", "README.md", "__pycache__"}

def limpiar():
    for p in RAIZ.iterdir():
        if p.name in ("_fuente", "README.md"): continue
        shutil.rmtree(p) if p.is_dir() else p.unlink()

def copiar(origen, destino, excluir=()):
    for p in origen.rglob("*"):
        rel = p.relative_to(origen)
        if rel.parts[0] in SKIP or rel.as_posix() in excluir or not p.is_file(): continue
        d = destino / rel
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, d)

limpiar()
copiar(S, RAIZ, excluir=("sitemap.xml",))
copiar(L, RAIZ / "lg", excluir=("robots.txt", "sitemap.xml"))
# sitemaps por marca + índice en la raíz
shutil.copy2(S / "sitemap.xml", RAIZ / "sitemap-samsung.xml")
shutil.copy2(L / "sitemap.xml", RAIZ / "lg" / "sitemap-lg.xml")
(RAIZ / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    f'<sitemap><loc>{DOM}/sitemap-samsung.xml</loc><lastmod>{HOY}</lastmod></sitemap>\n<sitemap><loc>{DOM}/lg/sitemap-lg.xml</loc><lastmod>{HOY}</lastmod></sitemap>\n</sitemapindex>\n', encoding="utf-8")
robots = (RAIZ / "robots.txt").read_text(encoding="utf-8")
import re
robots = re.sub(r"Sitemap:.*", f"Sitemap: {DOM}/sitemap.xml", robots)
(RAIZ / "robots.txt").write_text(robots, encoding="utf-8")
# llms.txt raíz: Samsung + referencia a LG
ll = (RAIZ / "llms.txt").read_text(encoding="utf-8")
ll = ll.replace("# Servicio Técnico Samsung Panamá", "# Centro de Servicio Panamá (Samsung y LG)", 1)
ll += f"\n## Servicio técnico LG en Panamá\n- [Servicio técnico LG Panamá]({DOM}/lg/index.html)\n- [llms.txt de LG]({DOM}/lg/llms.txt)\n"
(RAIZ / "llms.txt").write_text(ll, encoding="utf-8")
# zip
z = RAIZ.parent / "entrega" / "centro-servicio-panama.zip"
z.parent.mkdir(exist_ok=True)
n = 0
with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
    for p in RAIZ.rglob("*"):
        if p.is_file() and "_fuente" not in p.parts and p.name != "README.md":
            zf.write(p, p.relative_to(RAIZ).as_posix()); n += 1
print(f"OK: {n} archivos → {z.name}")
