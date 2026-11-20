#!/usr/bin/env python3
"""Mejoras de enlazado interno del sitio de una ciudad (se ejecuta DESPUÉS de st_samsung.py).
Uso: python3 st_cali_mejoras.py <carpeta_del_sitio>
- Cada página «falla × barrio» recibe «La misma falla en otros barrios» y «Otras fallas en este barrio» (así ninguna queda con 1 solo enlace entrante).
- Las guías sin enlaces entrantes se enlazan desde el índice de guías.
"""
import html, os, re, sys, pathlib, collections
R = pathlib.Path(sys.argv[1])
H1 = re.compile(r"<h1[^>]*>(.*?)</h1>", re.S)
h1 = lambda f: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", H1.search(f.read_text(encoding="utf-8")).group(1))).strip()
FALLA = re.compile(r"-(no|con|hace)-")
barrios = sorted(d.name for d in R.iterdir() if d.is_dir() and (d / "nevera-no-enfria" / "index.html").exists())
orden = [d for d in barrios]            # el orden alfabético reparte los enlaces de forma pareja
fallas = sorted(x.name for x in (R / orden[0]).iterdir() if x.is_dir() and FALLA.search(x.name) and (x / "index.html").exists())
tit = {(b, f): h1(R / b / f / "index.html") for b in orden for f in fallas if (R / b / f / "index.html").exists()}
SEC = '<section class="aq-sec chap{alt}"><div class="wrap"><h2>{h2}</h2><div class="city-tags">{links}</div></div></section>'
hechas = 0
for i, b in enumerate(orden):
    for j, f in enumerate(fallas):
        p = R / b / f / "index.html"
        if not p.exists():
            continue
        t = p.read_text(encoding="utf-8")
        if "st-mejora-enlaces" in t:
            continue
        vec = [orden[(i + k) % len(orden)] for k in (1, 2, 3, -1, -2, -3, 5, -5)]
        l1 = "".join(f'<a href="../../{v}/{f}/">{html.escape(tit[(v, f)])}</a>' for v in vec if (v, f) in tit)
        misma = [g for g in fallas if g != f and g.split("-")[0] == f.split("-")[0]] + [g for g in fallas if g != f and g.split("-")[0] != f.split("-")[0]]
        l2 = "".join(f'<a href="../{g}/">{html.escape(tit[(b, g)])}</a>' for g in misma[:6] if (b, g) in tit)
        bloque = '<!--st-mejora-enlaces-->' + SEC.format(alt="", h2="La misma falla en otros barrios de Cali", links=l1) + SEC.format(alt=" alt", h2="Otras fallas que atendemos en este barrio", links=l2)
        k = t.rfind('<footer')
        if k < 0:
            continue
        p.write_text(t[:k] + bloque + t[k:], encoding="utf-8"); hechas += 1
# guías huérfanas -> índice de guías
guias = R / "guias" / "index.html"
if guias.exists():
    todas = sorted(d for d in (R / "guias").iterdir() if d.is_dir() and (d / "index.html").exists())
    ref = guias.read_text(encoding="utf-8")
    faltan = [d for d in todas if f'href="{d.name}/' not in ref and f'/guias/{d.name}/' not in ref]
    if faltan:
        l = "".join(f'<a href="{d.name}/">{html.escape(h1(d / "index.html"))}</a>' for d in faltan)
        k = ref.rfind("<footer")
        guias.write_text(ref[:k] + SEC.format(alt="", h2="Más guías y códigos de error Samsung", links=l) + ref[k:], encoding="utf-8")
print(f"enlaces añadidos en {hechas} páginas; guías huérfanas enlazadas: {len(faltan) if guias.exists() else 0}")
