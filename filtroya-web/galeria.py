"""Imágenes informativas propias para la galería de cada filtro (identificar, instalación y ficha técnica).
No son fotos de otros vendedores: se dibujan con los datos del catálogo. Las fotos reales del producto (frente, atrás, lado, en mano) se suman en la misma carpeta."""
import pathlib
from PIL import Image, ImageDraw, ImageFont

SALIDA = pathlib.Path(__file__).resolve().parent / "galeria"
F = "/usr/share/fonts/opentype/inter/"
AZUL, TINTA, GRIS, FONDO, LINEA, VERDE = (20, 35, 160), (17, 24, 39), (95, 105, 125), (244, 247, 252), (214, 222, 236), (22, 130, 70)
TAM = 900


def fuente(n, b=False):
    for ruta in (F + ("Inter-Bold.otf" if b else "Inter-Regular.otf"), "/usr/share/fonts/truetype/dejavu/DejaVuSans" + ("-Bold" if b else "") + ".ttf"):
        try:
            return ImageFont.truetype(ruta, n)
        except OSError:
            continue
    return ImageFont.load_default()


PRODUCTOS = {
    "cin": dict(corto="HAF-CIN/EXP", ref="DA29-00020B", forma="Redondo", como="Se instala girando", tipo="Interno (dentro del nevecón)",
                alias=["DA29-00020A", "HAF-CIN", "HAF-CIN/EXP", "46-9101"], modelos=["RF28HMEDBSR", "RF263BEAESR", "RF28HFEDBSR", "RF4287HARS", "RF26J7500SR", "RF23J9011SR"],
                pasos=["Gira el filtro viejo a la izquierda y retíralo.", "Quita las tapas del filtro nuevo.", "Insértalo y gíralo a la derecha hasta que quede firme.", "Saca unos 6 litros de agua para purgar el aire.", "Reinicia la luz del filtro."]),
    "qin": dict(corto="HAF-QIN/EXP", ref="DA97-17376B", forma="Cuadrado", como="Se instala empujando", tipo="Interno (dentro del nevecón)",
                alias=["DA97-08006C", "HAF-QIN", "HAF-QIN/EXP"], modelos=["RF28R7351SR", "RF22R7351SG", "RF28R7201SR", "RF23M8070SR"],
                pasos=["Abre la tapa del filtro y retira el viejo.", "Quita las tapas del filtro nuevo.", "Empújalo hasta el fondo hasta que encaje.", "Cierra la tapa y saca unos 6 litros de agua.", "Reinicia la luz del filtro."]),
    "ext": dict(corto="Externo DA29-10105J", ref="DA29-10105J", forma="Cilíndrico", como="Se conecta a la manguera del agua", tipo="Externo (en la línea de agua)",
                alias=["DA29-10105J", "HAFEX", "HAFEX/EXP", "WSF-100"], modelos=[],
                pasos=["Cierra la llave de paso del agua.", "Desconecta el filtro viejo de las mangueras.", "Conecta el filtro nuevo en el mismo sentido del flujo.", "Abre la llave y revisa que no gotee.", "Saca unos 6 litros de agua para purgar."]),
}


def base(titulo, sub):
    im = Image.new("RGB", (TAM, TAM), FONDO)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, TAM, 150], fill=AZUL)
    d.text((48, 38), titulo, font=fuente(46, True), fill="white")
    d.text((48, 98), sub, font=fuente(26), fill=(205, 215, 255))
    return im, d


def tarjeta_blanca(d, x, y, w, h):
    d.rounded_rectangle([x, y, x + w, y + h], radius=22, fill="white", outline=LINEA, width=2)


def partir(d, txt, f, ancho):
    lineas, act = [], ""
    for pal in txt.split():
        prueba = (act + " " + pal).strip()
        if d.textlength(prueba, font=f) <= ancho:
            act = prueba
        else:
            lineas.append(act)
            act = pal
    return lineas + [act]


def identificar(k, p):
    im, d = base("¿Es el filtro de tu nevecón?", f"Samsung {p['corto']} · código {p['ref']}")
    tarjeta_blanca(d, 48, 190, 804, 200)
    d.text((80, 215), "Código del filtro", font=fuente(24), fill=GRIS)
    d.text((80, 252), p["ref"], font=fuente(70, True), fill=AZUL)
    d.text((80, 340), f"{p['forma']}  ·  {p['como']}  ·  {p['tipo']}", font=fuente(24), fill=TINTA)
    tarjeta_blanca(d, 48, 410, 804, 190)
    d.text((80, 432), "También aparece como", font=fuente(24), fill=GRIS)
    y = 470
    for l in partir(d, "  ·  ".join(p["alias"]), fuente(32, True), 740)[:3]:
        d.text((80, y), l, font=fuente(32, True), fill=TINTA)
        y += 44
    tarjeta_blanca(d, 48, 630, 804, 220)
    if p["modelos"]:
        d.text((80, 652), "Se usa en nevecones como", font=fuente(24), fill=GRIS)
        y = 692
        for l in partir(d, "  ·  ".join(p["modelos"]), fuente(30, True), 740)[:3]:
            d.text((80, y), l, font=fuente(30, True), fill=TINTA)
            y += 42
    else:
        d.text((80, 652), "Úsalo si tu nevecón", font=fuente(24), fill=GRIS)
        d.text((80, 692), "tiene sistema de filtrado externo.", font=fuente(32, True), fill=TINTA)
        d.text((80, 742), "Mira el código en tu filtro viejo.", font=fuente(28), fill=TINTA)
    return im


def instalacion(k, p):
    im, d = base("Cómo se instala", f"{p['como']} · 10 a 15 minutos, sin herramientas")
    y = 190
    for i, paso in enumerate(p["pasos"], 1):
        tarjeta_blanca(d, 48, y, 804, 118)
        d.ellipse([72, y + 27, 136, y + 91], fill=AZUL)
        d.text((104 - d.textlength(str(i), font=fuente(36, True)) / 2, y + 36), str(i), font=fuente(36, True), fill="white")
        for j, l in enumerate(partir(d, paso, fuente(29), 640)[:2]):
            d.text((164, y + (36 if len(partir(d, paso, fuente(29), 640)) == 1 else 20) + j * 38), l, font=fuente(29), fill=TINTA)
        y += 134
    return im


def ficha(k, p):
    im, d = base("Ficha técnica", f"Filtro de agua Samsung {p['corto']}")
    filas = [("Referencia Samsung", p["ref"]), ("Tipo", p["tipo"]), ("Forma", p["forma"]), ("Instalación", p["como"]), ("Cambio", "Cada 6 meses de uso normal"),
             ("Producto", "Nuevo, en su empaque sellado"), ("Garantía", "5 días hábiles de retracto, sin instalar")]
    y = 190
    for a, b in filas:
        tarjeta_blanca(d, 48, y, 804, 88)
        d.text((78, y + 14), a, font=fuente(22), fill=GRIS)
        d.text((78, y + 42), b, font=fuente(30, True), fill=TINTA)
        y += 100
    return im


def generar():
    SALIDA.mkdir(exist_ok=True)
    for k, p in PRODUCTOS.items():
        for nombre, fn in (("identificar", identificar), ("instalacion", instalacion), ("ficha", ficha)):
            fn(k, p).save(SALIDA / f"{k}-{nombre}.jpg", quality=88, optimize=True)
    return sorted(x.name for x in SALIDA.iterdir())


if __name__ == "__main__":
    print(generar())
