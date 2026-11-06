"""Genera la campaña de Google Ads para la tienda de mangueras para lavadoras Samsung y LG.
Está dentro del mismo dominio de la tienda de filtros (filtrosparalavadoras.click/mangueras-para-lavadora/), con la misma etiqueta de Tag Manager y el mismo evento «whatsapp».
Sin las palabras «original», «genuino» ni «compatible». Sin precios ni promesas: el precio lo da el asesor por WhatsApp."""
import csv, json, re, sys
from pathlib import Path

QUI = Path(__file__).resolve().parent
RAIZ = QUI.parent
WEB = RAIZ.parent / "filtroya-web" / "sitios-mangueras" / "tienda" / "mangueras-para-lavadora"
DOM = "https://filtrosparalavadoras.click/mangueras-para-lavadora"
CAMP = "Mangueras Lavadoras - Búsqueda - Colombia"
PROHIBIDAS = re.compile(r"original|genuin|compatib|100 ?%|mejor |garantiz|gratis", re.I)


def url(ruta):
    r = ruta.strip("/")
    assert ((WEB / r / "index.php").exists() if r else (WEB / "index.php").exists()), ruta
    return f"{DOM}/{r}/" if r else f"{DOM}/"


GEN_H = ["Pago contra Entrega", "Pedido por WhatsApp", "Asesor Te Confirma la Correcta", "Envío a Toda Colombia", "Mangueras para Samsung y LG", "Escríbenos por WhatsApp",
         "Cambio Paso a Paso", "Precio por WhatsApp", "Atención por WhatsApp", "Envía la Foto de tu Manguera", "Te Decimos Cuál Necesitas"]
GEN_D = ["Dinos el modelo de tu lavadora por WhatsApp y te confirmamos la manguera que necesita.",
         "Envía una foto de la manguera vieja y el asesor te dice cuál es.",
         "Cada manguera trae su paso a paso para cambiarla. Revisa la guía antes de pedir.",
         "Pago contra entrega: pagas cuando recibes el paquete. Envío con número de guía."]
G = []


def grupo(nombre, destino, path1, path2, titulos, descripciones, claves, nota=""):
    G.append(dict(nombre=nombre, url=destino, path1=path1, path2=path2, titulos=titulos, descripciones=descripciones, claves=claves, nota=nota))


def kw(marca, *frases):
    return [f.replace("{m}", marca.lower()) for f in frases]


# (clave de grupo, ruta de destino por marca, títulos específicos, descripción propia, frases)
TIPOS = [
    ("Desagüe", "{c}/manguera-de-desague-lavadora-{c}", "Desague",
     ["Manguera de Desagüe {M}", "Manguera Desagüe {M}", "Manguera de Drenaje {M}", "Manguera de Desagüe Corrugada", "Alargue Manguera Desagüe", "Manguera Desagüe Lavadora", "Mangueras de Desagüe {M}"],
     "Manguera de desagüe para lavadora {M}. Las largas son para carga frontal.",
     ["manguera de desague lavadora {m}", "manguera desague lavadora {m}", "manguera de desagüe lavadora {m}", "manguera de drenaje lavadora {m}", "manguera para desague lavadora {m}",
      "manguera de desague para lavadora {m}", "comprar manguera desague lavadora {m}", "manguera desague lavadora {m} carga frontal", "manguera desague lavadora {m} carga superior",
      "extension manguera desague lavadora {m}", "manguera de salida de agua lavadora {m}", "manguera de evacuacion lavadora {m}", "manguera de desague lavadora {m} colombia"]),
    ("Entrada", "{c}/manguera-de-entrada-lavadora-{c}", "Entrada",
     ["Manguera de Entrada {M}", "Manguera Agua Lavadora {M}", "Manguera Alimentación {M}", "Manguera con Tuercas", "Manguera Entrada Blanca", "Manguera de Llenado {M}", "Mangueras de Entrada {M}"],
     "Manguera de entrada para lavadora {M}: sirve para todas las lavadoras. Elige el largo.",
     ["manguera de entrada lavadora {m}", "manguera de entrada para lavadora", "manguera de entrada para todas las lavadoras", "manguera de agua para cualquier lavadora", "manguera entrada agua lavadora {m}", "manguera de agua lavadora {m}", "manguera de alimentacion lavadora {m}", "manguera de llenado lavadora {m}",
      "manguera de entrada de agua lavadora {m}", "manguera para lavadora {m}", "comprar manguera lavadora {m}", "manguera de conexion lavadora {m}", "manguera anti inundacion lavadora {m}",
      "manguera de abastecimiento lavadora {m}", "manguera lavadora {m} colombia", "manguera de agua para lavadora {m}"]),
    ("Tina-Bomba", "{c}/manguera-tina-bomba-lavadora-{c}", "TinaBomba",
     ["Manguera Tina Bomba {M}", "Manguera Tina-Bomba Lavadora", "Manguera de la Tina {M}", "Manguera Interna {M}", "Manguera Tina a Bomba", "Manguera Bomba {M}", "Mangueras Internas {M}"],
     "Manguera tina-bomba para lavadora {M}: la que une la tina con la bomba de desagüe.",
     ["manguera tina bomba lavadora {m}", "manguera tina-bomba lavadora {m}", "manguera de la tina lavadora {m}", "manguera tina a bomba lavadora {m}", "manguera interna lavadora {m}",
      "manguera de la bomba lavadora {m}", "manguera bomba de desague lavadora {m}", "manguera entre tina y bomba lavadora {m}", "manguera de tina lavadora {m}"]),
    ("Presostato y Dispensador", "{c}/manguera-lavadora-{c}-modelo-{f}", "Presostato",
     ["Manguera Presostato {M}", "Manguera Nivel Agua {M}", "Manguera del Dispensador", "Manguera Caja Detergente", "Manguera Nivel de Agua", "Manguera Interna Lavadora", "Mangueras Lavadora {M}"],
     "Manguera del presostato o dispensador para lavadora {M}. Consulta por WhatsApp.",
     ["manguera presostato lavadora {m}", "manguera del presostato lavadora {m}", "manguera sensor de nivel lavadora {m}", "manguera nivel de agua lavadora {m}", "manguera dispensador lavadora {m}",
      "manguera del dispensador lavadora {m}", "manguera caja detergente lavadora {m}", "manguera de la caja de jabon lavadora {m}", "manguera presostato {m}"]),
    ("Mangueras", "{c}", "Mangueras",
     ["Mangueras Lavadora {M}", "Manguera Lavadora {M}", "Repuesto Manguera {M}", "Mangueras Lavadora {M}", "Manguera Superior {M}", "Manguera Carga Frontal {M}", "Manguera {M} Lavadora"],
     "Mangueras para lavadora {M}: desagüe, entrada y más. Pídela por WhatsApp.",
     ["mangueras lavadora {m}", "mangueras para lavadora {m}", "manguera lavadora {m}", "repuesto manguera lavadora {m}", "repuestos mangueras lavadora {m}", "donde comprar manguera lavadora {m}",
      "precio manguera lavadora {m}", "manguera lavadora {m} carga frontal", "manguera lavadora {m} carga superior", "mangueras para lavadoras {m} colombia", "manguera lavadora {m} envio a toda colombia"]),
]
for M, c, fam in [("Samsung", "samsung", "wa"), ("LG", "lg", "wt")]:
    for nom, ruta, p2, tits, desc, frases in TIPOS:
        dest = url(ruta.format(c=c, f=fam))
        claves = [f.replace("{m}", c) for f in frases]
        grupo(f"{M} - {nom}", dest, "Mangueras", M if p2 in ("Mangueras",) else p2,
              [t.replace("{M}", M) for t in tits] + GEN_H[:8], [desc.replace("{M}", M), GEN_D[0], GEN_D[1], GEN_D[3]], claves)

NEGATIVAS = ["usado", "usada", "segunda mano", "casero", "casera", "reciclar", "manual", "pdf", "descargar", "video", "youtube", "curso", "empleo", "trabajo", "vacante", "gratis",
             "comprar lavadora", "lavadora nueva", "precio de lavadora", "lavadoras en oferta", "oferta lavadora", "falabella", "exito", "alkosto", "homecenter", "ktronix", "olx", "mercadolibre",
             "amazon", "alibaba", "aliexpress", "temu", "reparacion", "reparar", "servicio tecnico", "tecnico", "tecnico a domicilio", "tarjeta electronica", "compresor", "correa", "rodamiento",
             "empaque", "amortiguador", "mabe", "whirlpool", "haceb", "electrolux", "challenger", "kalley", "midea", "frigidaire", "general electric", "nevera", "refrigerador", "aire acondicionado",
             "patente", "dibujo", "juguete",
             # mangueras que no son de lavadora
             "jardin", "riego", "piscina", "incendio", "bombero", "gas", "gas natural", "cocina", "estufa", "radiador", "refrigerante", "hidraulica", "hidraulico", "combustible", "gasolina",
             "aire comprimido", "compresor de aire", "ducha", "lavamanos", "lavaplatos", "lavavajillas", "sanitario", "inodoro", "calentador", "cafetera", "aspiradora", "hidrolavadora",
             "carro", "automovil", "moto", "bicicleta", "acuario", "pecera", "pozo", "tanque", "cisterna", "industrial", "alta presion", "por metro", "por metros", "rollo", "carrete",
             "sumergible", "presurizadora", "bomba de agua carro", "bomba de piscina", "bomba de presion", "bomba periferica", "bomba centrifuga", "bomba de achique", "bomba de desague lavadora",
             "bomba de agua lavadora", "motobomba"]
SITELINKS = [("Mangueras Samsung", "Desagüe, entrada y más", "Pide la tuya por WhatsApp", url("samsung")), ("Mangueras LG", "Desagüe, entrada y más", "Pide la tuya por WhatsApp", url("lg")),
             ("Desagüe Samsung", "Corrugada y extensión", "El asesor te confirma", url("samsung/manguera-de-desague-lavadora-samsung")),
             ("Desagüe LG", "Corrugada y extensión", "El asesor te confirma", url("lg/manguera-de-desague-lavadora-lg")),
             ("Entrada de agua Samsung", "Negra o blanca, con tuercas", "El asesor te confirma", url("samsung/manguera-de-entrada-lavadora-samsung")),
             ("Entrada de agua LG", "Negra o blanca, con tuercas", "El asesor te confirma", url("lg/manguera-de-entrada-lavadora-lg")),
             ("Manguera tina-bomba", "La que va por dentro", "El asesor te confirma", url("samsung/manguera-tina-bomba-lavadora-samsung")),
             ("¿Cuál es mi manguera?", "Elige por tipo y modelo", "El asesor te confirma", url("samsung/cual-es-mi-manguera")),
             ("Lavadora gotea", "Qué manguera revisar", "Guía paso a paso", url("samsung/lavadora-samsung-gotea-agua-por-la-manguera")),
             ("Cómo cambiar la manguera", "Paso a paso", "Revisa la guía antes de pedir", url("samsung/cambio-e-instalacion"))]
CALLOUTS = ["Pedido por WhatsApp", "Asesor por WhatsApp", "Envío a Toda Colombia", "Confirmamos la Correcta", "Pago contra Entrega", "Número de Guía", "Samsung y LG", "Guía de Cambio"]
SNIPPET = ("Tipos", ["Manguera de desagüe", "Manguera de entrada", "Manguera tina-bomba", "Manguera del presostato", "Manguera del dispensador"])

err = []
for g in G:
    t, d = list(dict.fromkeys(g["titulos"]))[:15], g["descripciones"]; g["titulos"] = t
    if len(t) < 12: err.append(f"{g['nombre']}: solo {len(t)} títulos")
    for x in t:
        if len(x) > 30: err.append(f"{g['nombre']}: título largo ({len(x)}): {x}")
        if PROHIBIDAS.search(x): err.append(f"título prohibido: {x}")
    for x in d:
        if len(x) > 90: err.append(f"{g['nombre']}: descripción larga ({len(x)}): {x}")
        if PROHIBIDAS.search(x): err.append(f"descripción prohibida: {x}")
    g["claves"] = list(dict.fromkeys(g["claves"]))
    for k in g["claves"]:
        if PROHIBIDAS.search(k): err.append(f"clave prohibida: {k}")
    for p1 in (g["path1"], g["path2"]):
        if len(p1) > 15: err.append(f"ruta larga: {p1}")
for x in CALLOUTS:
    if len(x) > 25 or PROHIBIDAS.search(x): err.append(f"destacado: {x}")
for s in SITELINKS:
    if len(s[0]) > 25 or len(s[1]) > 35 or len(s[2]) > 35 or PROHIBIDAS.search(" ".join(s[:3])): err.append(f"sitelink: {s}")
if err:
    print("\n".join(err)); sys.exit(1)

INFORMATIVOS = ()
out = RAIZ / "05-archivos-para-importar"; out.mkdir(exist_ok=True)
with open(out / "anuncios.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["Campaign", "Ad group", "Ad type", "Final URL", "Path 1", "Path 2"] + [f"Headline {i}" for i in range(1, 16)] + [f"Description {i}" for i in range(1, 5)])
    for g in G:
        w.writerow([CAMP, g["nombre"], "Responsive search ad", g["url"], g["path1"], g["path2"]] + g["titulos"] + [""] * (15 - len(g["titulos"])) + g["descripciones"] + [""] * (4 - len(g["descripciones"])))
with open(out / "palabras-clave.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f); w.writerow(["Campaign", "Ad group", "Keyword", "Criterion Type"])
    for g in G:
        for k in g["claves"]:
            w.writerow([CAMP, g["nombre"], k, "Phrase"])
            if True:
                w.writerow([CAMP, g["nombre"], k, "Exact"])
with open(out / "palabras-negativas.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f); w.writerow(["Campaign", "Keyword", "Criterion Type"])
    for k in NEGATIVAS: w.writerow([CAMP, k, "Campaign negative phrase"])
with open(out / "enlaces-de-sitio.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f); w.writerow(["Campaign", "Link text", "Description line 1", "Description line 2", "Final URL"])
    for s in SITELINKS: w.writerow([CAMP] + list(s))
(RAIZ / "08-palabras-clave-para-copiar.txt").write_text("\n\n".join(f"# {g['nombre']}\n" + "\n".join(g["claves"]) for g in G), encoding="utf-8")
gd = RAIZ / "02-grupos-de-anuncios"; gd.mkdir(exist_ok=True)
for f in gd.glob("*.md"): f.unlink()
for i, g in enumerate(G, 1):
    md = [f"# Grupo {i}: {g['nombre']}", "", f"**Página de destino:** {g['url']}  ", f"**Rutas visibles:** filtrosparalavadoras.click/{g['path1']}/{g['path2']}", ""]
    if g["nota"]: md += [f"> {g['nota']}", ""]
    md += ["## Títulos (máximo 30 caracteres)"] + [f"{j}. {t} ({len(t)})" for j, t in enumerate(g["titulos"], 1)]
    md += ["", "## Descripciones (máximo 90 caracteres)"] + [f"{j}. {d} ({len(d)})" for j, d in enumerate(g["descripciones"], 1)]
    md += ["", f"## Palabras clave ({len(g['claves'])})"] + [f"- {k}" for k in g["claves"]]
    (gd / f"{i:02d}-{re.sub('[^a-z0-9]+', '-', g['nombre'].lower()).strip('-')}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
(RAIZ / "03-palabras-negativas.md").write_text("# 3. Palabras negativas (a nivel de campaña)\n\nSon búsquedas por las que NO quieres pagar. Ya vienen en `05-archivos-para-importar/palabras-negativas.csv`. "
    "Incluyen las de quien busca comprar una lavadora (no una manguera), otras marcas y otras clases de manguera (jardín, gas, piscina, carro, industrial…). Revisa el informe de **Términos de búsqueda** cada semana y agrega las que no te sirvan.\n\n" + "\n".join(f"- {k}" for k in NEGATIVAS) + "\n", encoding="utf-8")
(RAIZ / "04-recursos-extensiones.md").write_text("# Recursos (extensiones) a nivel de campaña\n\n## Enlaces de sitio (título ≤25, descripciones ≤35)\n"
    + "\n".join(f"- **{s[0]}** — {s[1]} / {s[2]} → {s[3]}" for s in SITELINKS) + "\n\n## Textos destacados (≤25)\n" + "\n".join(f"- {c}" for c in CALLOUTS)
    + f"\n\n## Fragmento estructurado\n**{SNIPPET[0]}:** {', '.join(SNIPPET[1])}\n\n## Llamadas\n- Samsung: 305 479 6329 · LG: 320 510 2995. Agrega los dos como recurso de llamada y limítalos al horario de atención.\n\n## Imágenes\n- Usa las fotos de las mangueras de la tienda (cuadradas 1:1 y 1,91:1).\n", encoding="utf-8")
ng = sum(len(g["claves"]) for g in G)
(QUI / "datos.json").write_text(json.dumps(dict(grupos=G, negativas=NEGATIVAS, sitelinks=SITELINKS, destacados=CALLOUTS, fragmento=SNIPPET, dominio=DOM, campana=CAMP, total_claves=ng), ensure_ascii=False, indent=1), encoding="utf-8")
print(f"OK: {len(G)} grupos, {ng} palabras clave, {len(NEGATIVAS)} negativas, {len(SITELINKS)} enlaces")
