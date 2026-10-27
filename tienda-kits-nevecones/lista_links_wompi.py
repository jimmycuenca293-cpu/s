#!/usr/bin/env python3
"""Lista de los links de pago de Wompi que hay que crear (nombre, descripción, monto exacto e imagen de cada producto).
Uso: python3 lista_links_wompi.py <carpeta_salida> <carpeta_con_filtrosnevecones-img>
Genera <salida>/links-de-pago-kits.xlsx, <salida>/imagenes/<codigo>.jpg y <salida>/imagenes-links-wompi.zip"""
import io, sys, zipfile, contextlib
from pathlib import Path
from PIL import Image
import openpyxl
from openpyxl.drawing.image import Image as XImg
from openpyxl.styles import Alignment, Font, PatternFill

AQUI = Path(__file__).parent
OUT = Path(sys.argv[1]); IMG = Path(sys.argv[2])
sys.argv = ["x", "/tmp/_kk"]
src = (AQUI / "kits_php.py").read_text(encoding="utf-8").replace("\nmain()\n", "\n")
g = {"__file__": str(AQUI / "kits_php.py"), "__name__": "x"}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src, "kits_php.py", "exec"), g)
PROD, FILTROS = g["PROD"], g["FILTROS"]
cop = lambda n: "$ " + f"{n:,}".replace(",", ".")

def nombre_corto(p):
    if p.get("grupo"):
        q = '1/4' if p["grupo"] == "man14" else '5/16'
        return f'Manguera {q}" nevecón {p["metros"]} metros'
    return {"k-galapago": "Llave galápago para nevecón", "k-plastica": "Llave plástica acople rápido", "k-acople14": 'Acople rápido manguera 1/4"',
            "k-acople516": 'Acople rápido manguera 5/16"', "k-kit-basico": "Kit básico: manguera 5 m + llave galápago",
            "k-kit-plastica": "Kit: manguera 5 m + llave plástica", "k-kit-516": 'Kit: manguera 5/16" 5 m + llave galápago',
            "k-kit-acoples": "Kit básico + 2 acoples rápidos", "k-kit-sam": "Kit completo nevecón Samsung",
            "k-kit-lg": "Kit completo nevecón LG", "k-kit-wp": "Kit completo nevecón Whirlpool"}[p["pid"]]

ENVIO = "Envío gratis a toda Colombia."
def descripcion(p):
    if p.get("grupo"):
        q = '1/4' if p["grupo"] == "man14" else '5/16'
        return f'Manguera de {q} de pulgada de {p["metros"]} metros para conectar el agua de tu nevecón. {ENVIO}'
    d = {"k-galapago": "Llave galápago con racores, anillo y tuerca para tomar el agua del tubo y conectar la manguera de 1/4 de pulgada de tu nevecón.",
         "k-plastica": "Llave plástica blanca con acople rápido azul y tuerca para conectar la manguera de agua de tu nevecón.",
         "k-acople14": 'Acople rápido de unión recta para empalmar manguera de 1/4 de pulgada, sin herramientas.',
         "k-acople516": 'Acople rápido de unión recta para empalmar manguera de 5/16 de pulgada, sin herramientas.'}
    if p["pid"] in d: return d[p["pid"]] + " " + ENVIO
    partes = []
    for c, n in p["comp"]:
        partes.append(f"{n} × " + (FILTROS[c][4] if c in FILTROS else PROD[c]["nombre"]))
    return "Incluye: " + "; ".join(partes) + ". " + ENVIO

(OUT / "imagenes").mkdir(parents=True, exist_ok=True)
wb = openpyxl.Workbook(); ws = wb.active; ws.title = "Links de Wompi"
ws.append(["N°", "Imagen", "Nombre del link (máx. 50 letras)", "Descripción para el cliente", "Monto EXACTO a cobrar", "Archivo de imagen", "Código", "Pega aquí el link que te dé Wompi"])
for c in ws[1]: c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor="1236A8"); c.alignment = Alignment(wrap_text=True, vertical="center")
for i, p in enumerate(PROD.values(), 1):
    f = IMG / f"{p['pid']}.jpg"
    im = Image.open(f).convert("RGB"); s = max(im.size); lienzo = Image.new("RGB", (s, s), "white")
    lienzo.paste(im, ((s - im.width) // 2, (s - im.height) // 2)); lienzo.thumbnail((800, 800))
    ruta = OUT / "imagenes" / f"{i:02d}-{p['pid']}.jpg"; lienzo.save(ruta, quality=88, optimize=True)
    nom = nombre_corto(p); assert len(nom) <= 50, nom
    ws.append([i, "", nom, descripcion(p), p["precio"], ruta.name, p["pid"], ""])
    t = lienzo.copy(); t.thumbnail((110, 110)); tp = OUT / "imagenes" / f"_mini{i}.png"; t.save(tp)
    xi = XImg(str(tp)); ws.add_image(xi, f"B{i + 1}"); ws.row_dimensions[i + 1].height = 86
    ws.cell(i + 1, 5).number_format = '$ #,##0'
    for col in (3, 4): ws.cell(i + 1, col).alignment = Alignment(wrap_text=True, vertical="top")
for col, wd in zip("ABCDEFGH", (5, 17, 36, 60, 16, 30, 16, 40)): ws.column_dimensions[col].width = wd
ws.freeze_panes = "A2"
wb.save(OUT / "links-de-pago-kits.xlsx")
with zipfile.ZipFile(OUT / "imagenes-links-wompi.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted((OUT / "imagenes").glob("[0-9]*.jpg")): z.write(f, f.name)
for f in (OUT / "imagenes").glob("_mini*"): f.unlink()
print(len(PROD), "links")
for i, p in enumerate(PROD.values(), 1): print(f"{i:2d} {nombre_corto(p):52s} {p['precio']}")
