#!/usr/bin/env python3
"""Genera imágenes de referencia (ilustraciones de estudio) de cada clase de manguera de lavadora,
mientras no haya fotos reales. Reemplázalas poniendo la foto real con el mismo nombre en
imagenes-mangueras/<marca>/manguera-N.png y vuelve a correr mangueras.py."""
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

AQUI = Path(__file__).resolve().parent
SS = 3            # supersampling
W = 1000 * SS


def lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def bez(p0, p1, p2, p3, n=400):
    pts = []
    for i in range(n + 1):
        t = i / n; u = 1 - t
        pts.append((u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0], u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1]))
    return pts


def chain(*segs):
    out = []
    for s in segs: out += s
    return out


def tubo(img, pts, r, base, hi=None, costilla=0, costilla_col=None):
    """Dibuja un tubo siguiendo pts con volumen (borde oscuro, centro claro) y costillas opcionales."""
    d = ImageDraw.Draw(img)
    r *= SS
    dark = lerp(base, (0, 0, 0), 0.45); light = hi or lerp(base, (255, 255, 255), 0.45)
    for k in (1.0, 0.82, 0.62, 0.42, 0.22):
        col = lerp(dark, light, 1 - k) if k < 1 else dark
        rr = r * k
        off = r * (1 - k) * 0.35
        for (x, y) in pts:
            d.ellipse((x*SS - rr - off*0.4, y*SS - rr - off, x*SS + rr - off*0.4, y*SS + rr - off*0.2), fill=col)
    if costilla:
        cc = costilla_col or lerp(base, (0, 0, 0), 0.38)
        step = max(1, int(len(pts) / (costilla)))
        for i in range(step, len(pts) - 1, step):
            x0, y0 = pts[i - 1]; x1, y1 = pts[i + 1]
            dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy) or 1
            nx, ny = -dy / L, dx / L
            x, y = pts[i]
            d.line([((x - nx*r/SS*0.96)*SS, (y - ny*r/SS*0.96)*SS), ((x + nx*r/SS*0.96)*SS, (y + ny*r/SS*0.96)*SS)], fill=cc, width=int(3.2*SS))


def tuerca(img, c, ang, r=46, color=(188, 194, 204), largo=92):
    """Tuerca metálica hexagonal en el extremo de una manguera."""
    d = ImageDraw.Draw(img)
    cx, cy = c; ca, sa = math.cos(ang), math.sin(ang)
    def P(u, v): return ((cx + u*ca - v*sa)*SS, (cy + u*sa + v*ca)*SS)
    d.polygon([P(-largo/2, -r), P(largo/2, -r), P(largo/2, r), P(-largo/2, r)], fill=color, outline=lerp(color, (0, 0, 0), 0.5))
    for k in range(1, 4):
        d.line([P(-largo/2, -r + k*r/2), P(largo/2, -r + k*r/2)], fill=lerp(color, (0, 0, 0), 0.25 if k != 2 else 0.1), width=2*SS)
    d.line([P(-largo/2 + 4, -r + 4), P(-largo/2 + 4, r - 4)], fill=(255, 255, 255), width=3*SS)
    d.polygon([P(largo/2, -r*0.62), P(largo/2 + 14, -r*0.62), P(largo/2 + 14, r*0.62), P(largo/2, r*0.62)], fill=lerp(color, (0, 0, 0), 0.35))


def abraz(img, c, r=60, color=(190, 196, 206)):
    d = ImageDraw.Draw(img)
    cx, cy = c
    for k, (rr, col) in enumerate([(r, lerp(color, (0, 0, 0), 0.5)), (r - 6, color), (r - 18, (0, 0, 0, 0))]):
        pass
    d.ellipse(((cx - r)*SS, (cy - r)*SS, (cx + r)*SS, (cy + r)*SS), fill=lerp(color, (0, 0, 0), 0.45))
    d.ellipse(((cx - r + 7)*SS, (cy - r + 7)*SS, (cx + r - 7)*SS, (cy + r - 7)*SS), fill=color)
    d.ellipse(((cx - r + 22)*SS, (cy - r + 22)*SS, (cx + r - 22)*SS, (cy + r - 22)*SS), fill=(0, 0, 0, 0))
    d.rectangle(((cx + r - 18)*SS, (cy - 22)*SS, (cx + r + 46)*SS, (cy + 22)*SS), fill=lerp(color, (0, 0, 0), 0.2), outline=lerp(color, (0, 0, 0), 0.5))
    d.ellipse(((cx + r + 8)*SS, (cy - 12)*SS, (cx + r + 32)*SS, (cy + 12)*SS), fill=(70, 74, 84))
    for k in range(5): d.line([((cx + r - 12 + k*10)*SS, (cy - 20)*SS), ((cx + r - 12 + k*10)*SS, (cy + 20)*SS)], fill=lerp(color, (0, 0, 0), 0.4), width=2*SS)


def nuevo():
    return Image.new("RGBA", (W, W), (0, 0, 0, 0))


def sombra(img, desplaz=(0, 26)):
    a = img.split()[3].filter(ImageFilter.GaussianBlur(22*SS))
    sh = Image.new("RGBA", img.size, (30, 36, 60, 0)); sh.putalpha(a.point(lambda v: int(v * 0.32)))
    base = Image.new("RGBA", img.size, (0, 0, 0, 0)); base.alpha_composite(sh, desplaz); base.alpha_composite(img)
    return base


def guardar(img, destino):
    img = sombra(img).resize((1000, 1000), Image.LANCZOS)
    destino.parent.mkdir(parents=True, exist_ok=True)
    img.save(destino)


GRIS = (176, 182, 190); NEGRO = (46, 48, 54); BLANCO = (232, 235, 240); AZUL = (40, 110, 190); CLARO = (205, 224, 235)


def i1():   # desagüe corrugada con codo
    im = nuevo()
    p = chain(bez((170, 760), (140, 300), (460, 220), (560, 460), 220), bez((560, 460), (640, 640), (800, 760), (840, 560), 220))
    tubo(im, p, 46, GRIS, costilla=70)
    tubo(im, bez((840, 560), (860, 470), (830, 380), (760, 330), 60), 46, GRIS, costilla=18)
    return im


def i2():   # extensión larga con lazo
    im = nuevo()
    p = chain(bez((120, 800), (80, 380), (330, 200), (470, 360), 200), bez((470, 360), (600, 520), (330, 700), (500, 760), 200), bez((500, 760), (690, 810), (900, 600), (880, 230), 240))
    tubo(im, p, 40, BLANCO, costilla=90)
    return im


def i3():   # entrada con tuercas
    im = nuevo()
    p = chain(bez((210, 780), (130, 380), (420, 160), (560, 380), 230), bez((560, 380), (680, 560), (820, 640), (840, 330), 230))
    tubo(im, p, 34, NEGRO, hi=(120, 124, 136))
    tuerca(im, (200, 770), math.radians(75)); tuerca(im, (845, 300), math.radians(-85))
    return im


def i4():   # entrada con válvula anti inundación
    im = nuevo()
    p = chain(bez((200, 790), (110, 430), (330, 190), (520, 330), 200), bez((520, 330), (640, 420), (700, 640), (860, 560), 200))
    tubo(im, p, 34, NEGRO, hi=(120, 124, 136))
    tuerca(im, (190, 780), math.radians(75)); tuerca(im, (880, 540), math.radians(-30))
    d = ImageDraw.Draw(im)
    x, y = 640, 520
    d.rounded_rectangle(((x - 70)*SS, (y - 60)*SS, (x + 70)*SS, (y + 60)*SS), radius=26*SS, fill=lerp(AZUL, (0, 0, 0), 0.35), outline=(20, 40, 80))
    d.rounded_rectangle(((x - 62)*SS, (y - 52)*SS, (x + 62)*SS, (y + 52)*SS), radius=22*SS, fill=AZUL)
    d.rounded_rectangle(((x - 50)*SS, (y - 44)*SS, (x + 20)*SS, (y - 20)*SS), radius=12*SS, fill=lerp(AZUL, (255, 255, 255), 0.35))
    d.ellipse(((x - 18)*SS, (y - 8)*SS, (x + 18)*SS, (y + 28)*SS), fill=(230, 236, 245), outline=(20, 40, 80))
    return im


def i5():   # tina-bomba: corta, gruesa, con abrazaderas
    im = nuevo()
    p = chain(bez((190, 620), (250, 420), (450, 360), (560, 430), 200), bez((560, 430), (650, 490), (700, 620), (830, 560), 160))
    tubo(im, p, 70, NEGRO, hi=(110, 114, 126), costilla=26, costilla_col=(24, 26, 30))
    abraz(im, (225, 600), 72); abraz(im, (820, 568), 72)
    return im


def i6():   # presostato: tubo delgado transparente en espiral con conector
    im = nuevo()
    p = chain(bez((160, 780), (120, 420), (360, 300), (470, 460), 200), bez((470, 460), (560, 590), (700, 700), (830, 540), 200), bez((830, 540), (910, 440), (850, 300), (760, 250), 120))
    tubo(im, p, 22, CLARO, hi=(250, 253, 255))
    tubo(im, bez((160, 780), (162, 770), (165, 760), (168, 745), 20), 30, (70, 74, 82))
    tubo(im, bez((760, 250), (750, 244), (740, 238), (728, 232), 20), 30, (70, 74, 82))
    return im


def i7():   # dispensador: manguera mediana gris con dos puntas
    im = nuevo()
    p = chain(bez((200, 740), (130, 420), (350, 250), (520, 400), 200), bez((520, 400), (650, 520), (760, 700), (850, 470), 200))
    tubo(im, p, 36, (150, 156, 168), costilla=60)
    tubo(im, bez((200, 740), (200, 760), (206, 780), (214, 800), 20), 44, (222, 228, 236))
    tubo(im, bez((850, 470), (850, 440), (840, 420), (826, 400), 20), 44, (222, 228, 236))
    return im


def i8():   # abrazaderas y codo
    im = nuevo()
    abraz(im, (300, 360), 120); abraz(im, (640, 330), 100); abraz(im, (480, 650), 110)
    tubo(im, chain(bez((700, 760), (760, 760), (830, 730), (850, 660), 60)), 46, GRIS, costilla=14)
    return im


def presostato(acento):
    """Presostato de lavadora: cuerpo redondo de plástico, boquilla para la manguera de aire y conector eléctrico."""
    im = nuevo(); d = ImageDraw.Draw(im)
    cx, cy, r = 500, 520, 250
    for k, col in enumerate([lerp((70, 74, 84), (0, 0, 0), 0.2), (96, 100, 112), (122, 127, 140), (150, 155, 168)]):
        d.ellipse(((cx - r + k*16)*SS, (cy - r + k*16)*SS, (cx + r - k*16)*SS, (cy + r - k*16)*SS), fill=col)
    d.ellipse(((cx - 150)*SS, (cy - 150)*SS, (cx + 150)*SS, (cy + 150)*SS), fill=(176, 181, 194), outline=(70, 74, 84))
    d.ellipse(((cx - 62)*SS, (cy - 62)*SS, (cx + 62)*SS, (cy + 62)*SS), fill=acento, outline=(30, 34, 44))
    d.ellipse(((cx - 24)*SS, (cy - 24)*SS, (cx + 24)*SS, (cy + 24)*SS), fill=(230, 234, 242))
    # boquilla de la manguera de aire
    d.rounded_rectangle(((cx + r - 40)*SS, (cy - 46)*SS, (cx + r + 150)*SS, (cy + 46)*SS), radius=22*SS, fill=(105, 110, 124), outline=(50, 54, 64))
    for k in range(4): d.line([((cx + r + 40 + k*28)*SS, (cy - 44)*SS), ((cx + r + 40 + k*28)*SS, (cy + 44)*SS)], fill=(70, 74, 84), width=4*SS)
    # conector eléctrico
    d.rounded_rectangle(((cx - 120)*SS, (cy + r - 40)*SS, (cx + 120)*SS, (cy + r + 110)*SS), radius=20*SS, fill=(236, 238, 244), outline=(120, 124, 136))
    for k in range(3): d.rounded_rectangle(((cx - 84 + k*62)*SS, (cy + r + 4)*SS, (cx - 46 + k*62)*SS, (cy + r + 84)*SS), radius=8*SS, fill=(190, 150, 70), outline=(110, 84, 30))
    # tornillo de ajuste
    d.ellipse(((cx - 210)*SS, (cy - 200)*SS, (cx - 150)*SS, (cy - 140)*SS), fill=(190, 194, 204), outline=(80, 84, 96))
    d.line([((cx - 200)*SS, (cy - 170)*SS), ((cx - 160)*SS, (cy - 170)*SS)], fill=(80, 84, 96), width=5*SS)
    return im


def generar():
    dest = AQUI / "imagenes-mangueras" / "todas"
    guardar(presostato((40, 110, 190)), dest / "manguera-8.png")     # Samsung: acento azul
    guardar(presostato((190, 40, 70)), dest / "manguera-9.png")      # LG: acento rojo


if __name__ == "__main__":
    generar()
    print("Imágenes de referencia de presostatos generadas en imagenes-mangueras/todas/")
