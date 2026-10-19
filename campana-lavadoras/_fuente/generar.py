"""Genera la campaña de Google Ads para la tienda de filtros para lavadoras Samsung y LG (un solo dominio).
Sin las palabras «original», «genuino» ni «compatible». Sin precios ni promesas: el precio lo da el asesor por WhatsApp."""
import csv, json, re, sys
from pathlib import Path

QUI = Path(__file__).resolve().parent
RAIZ = QUI.parent
WEB = RAIZ.parent / "filtroya-web" / "sitios-lavadoras" / "tienda"
DOM = "https://filtrosparalavadoras.click"
CAMP = "Filtros Lavadoras - Búsqueda - Colombia"
PROHIBIDAS = re.compile(r"original|genuin|compatib|100 ?%|mejor |garantiz|gratis", re.I)


def url(ruta):
    r = ruta.strip("/")
    assert (WEB / r / "index.php").exists() if r else (WEB / "index.php").exists(), ruta
    return f"{DOM}/{r}/" if r else f"{DOM}/"


GEN_H = ["Pago contra Entrega", "Pedido por WhatsApp", "Asesor Te Confirma el Modelo", "Envío a Toda Colombia", "Filtros para Samsung y LG", "Escríbenos por WhatsApp",
         "Cambio Paso a Paso", "Precio por WhatsApp", "Atención por WhatsApp", "Envía la Foto de tu Filtro", "Te Decimos Cuál Necesitas"]
GEN_D = ["Dinos el modelo de tu lavadora por WhatsApp y te confirmamos el filtro que necesitas.",
         "Envía una foto del filtro viejo y el asesor te dice cuál es. Pedido por WhatsApp.",
         "Cada filtro trae su paso a paso para cambiarlo. Sin técnico y sin herramientas.",
         "Pago contra entrega: pagas cuando recibes el paquete. Envío con número de guía."]

G = []


def grupo(nombre, destino, path1, path2, titulos, descripciones, claves, nota=""):
    G.append(dict(nombre=nombre, url=destino, path1=path1, path2=path2, titulos=titulos, descripciones=descripciones, claves=claves, nota=nota))


def kw(marca, *frases):
    m = marca.lower()
    return [f.replace("{m}", m) for f in frases]


# ---------------- Samsung ----------------
grupo("Samsung - Filtro de lavadora", url("samsung"), "Filtros", "Samsung",
      ["Filtro para Lavadora Samsung", "Filtro de Pelusas Samsung", "Filtros de Lavadora Samsung", "Bolsa de Malla Samsung", "Filtro Samsung Carga Superior", "Filtro Samsung Carga Frontal",
       "Filtro de Lavadora Samsung"] + GEN_H[:8],
      ["Filtros de pelusas y bolsas de malla para lavadora Samsung. Pide el tuyo por WhatsApp.", GEN_D[0], GEN_D[2], GEN_D[3]],
      kw("Samsung", "filtro lavadora {m}", "filtro para lavadora {m}", "filtro de pelusas lavadora {m}", "filtro pelusas {m}", "filtro de lavadora {m}", "comprar filtro lavadora {m}",
         "filtro malla lavadora {m}", "malla filtro lavadora {m}", "filtro atrapa pelusas lavadora {m}", "filtro lavadora {m} repuesto", "filtro tina lavadora {m}",
         "donde comprar filtro lavadora {m}", "filtro para lavadora {m} colombia", "bolsa filtro lavadora {m}", "filtro lavadora {m} carga superior"))
grupo("Samsung - Carga frontal", url("samsung/filtro-pelusas-lavadora-samsung-carga-frontal"), "Samsung", "Carga-Frontal",
      ["Filtro Samsung Frontal", "Filtro Samsung Carga Frontal", "Filtro de Pelusas con Asa", "Filtro para Lavadora Samsung", "Cambia el Filtro Lavadora", "Instalación Paso a Paso"] + GEN_H[:9],
      ["Filtro de pelusas con asa para lavadora Samsung de carga frontal. Consulta por WhatsApp.", GEN_D[1], GEN_D[2], GEN_D[3]],
      kw("Samsung", "filtro lavadora {m} carga frontal", "filtro pelusas lavadora {m} carga frontal", "filtro lavadora {m} frontal", "filtro de lavadora {m} puerta frontal",
         "filtro pelusas {m} frontal", "comprar filtro lavadora {m} carga frontal", "filtro lavadora frontal {m}"))
grupo("Samsung - Carga superior", url("samsung/filtro-lavadora-samsung-carga-superior"), "Samsung", "Carga-Superior",
      ["Filtro Samsung Superior", "Filtro Samsung Carga Superior", "Filtros de Pelusas Samsung", "Bolsa de Malla para Lavadora", "Filtro para Lavadora Samsung", "Elige tu Filtro por Modelo"] + GEN_H[:9],
      ["Filtros de pelusas para lavadora Samsung de carga superior. El asesor confirma el modelo.", GEN_D[1], GEN_D[2], GEN_D[3]],
      kw("Samsung", "filtro lavadora {m} carga superior", "filtro pelusas lavadora {m} carga superior", "filtro lavadora {m} superior", "filtro de lavadora {m} tina",
         "filtro lavadora {m} agitador", "comprar filtro lavadora {m} carga superior", "filtro lavadora superior {m}"))
grupo("Samsung - Bolsa de malla", url("samsung/bolsa-malla-pelusas-lavadora-samsung"), "Samsung", "Bolsa-de-Malla",
      ["Bolsa de Malla para Samsung", "Bolsa Filtro Lavadora", "Malla para Pelusas Samsung", "Bolsa de Pelusas Samsung", "Filtro de Malla Samsung", "Cambia tu Bolsa de Malla"] + GEN_H[:9],
      ["Bolsa de malla con marco para atrapar pelusas en tu lavadora Samsung. Pide por WhatsApp.", GEN_D[0], GEN_D[2], GEN_D[3]],
      kw("Samsung", "bolsa de malla lavadora {m}", "bolsa filtro lavadora {m}", "malla pelusas lavadora {m}", "bolsa pelusas lavadora {m}", "bolsa atrapa pelusas lavadora {m}",
         "comprar bolsa malla lavadora {m}", "bolsa de malla para lavadora"))
# ---------------- LG ----------------
grupo("LG - Filtro de lavadora", url("lg"), "Filtros", "LG",
      ["Filtro para Lavadora LG", "Filtro de Pelusas LG", "Filtros de Lavadora LG", "Bolsa de Malla LG", "Filtro Redondo LG", "Filtro Rectangular LG", "Filtro de Lavadora LG"] + GEN_H[:8],
      ["Filtros de pelusas y bolsas de malla para lavadora LG. Pide el tuyo por WhatsApp.", GEN_D[0], GEN_D[2], GEN_D[3]],
      kw("LG", "filtro lavadora {m}", "filtro para lavadora {m}", "filtro de pelusas lavadora {m}", "filtro pelusas {m}", "filtro de lavadora {m}", "comprar filtro lavadora {m}",
         "filtro malla lavadora {m}", "malla filtro lavadora {m}", "filtro atrapa pelusas lavadora {m}", "filtro lavadora {m} repuesto", "filtro tina lavadora {m}",
         "donde comprar filtro lavadora {m}", "filtro para lavadora {m} colombia", "bolsa filtro lavadora {m}", "filtro lavadora {m} carga superior"))
grupo("LG - Secadora", url("lg/filtro-pelusas-secadora-lg"), "LG", "Secadora",
      ["Filtro de Secadora LG", "Filtro Pelusas Secadora LG", "Filtro para Secadora LG", "Malla Filtro Secadora LG", "Cambia el Filtro de Pelusas", "Instalación Paso a Paso"] + GEN_H[:9],
      ["Filtro de pelusas para secadora LG. Dinos tu modelo por WhatsApp y te confirmamos.", GEN_D[1], GEN_D[2], GEN_D[3]],
      kw("LG", "filtro secadora {m}", "filtro de secadora {m}", "filtro pelusas secadora {m}", "filtro de pelusas secadora {m}", "malla filtro secadora {m}", "filtro para secadora {m}",
         "comprar filtro secadora {m}", "filtro secadora {m} colombia", "filtro pelusa secadora", "filtro de pelusas para secadora", "donde comprar filtro secadora {m}"))
grupo("LG - Bolsa de malla", url("lg/bolsa-malla-pelusas-lavadora-lg"), "LG", "Bolsa-de-Malla",
      ["Bolsa de Malla Lavadora LG", "Bolsa Filtro Lavadora LG", "Malla para Pelusas LG", "Bolsa de Pelusas LG", "Filtro de Malla LG", "Cambia tu Bolsa de Malla"] + GEN_H[:9],
      ["Bolsa de malla con marco para atrapar pelusas en tu lavadora LG. Pide por WhatsApp.", GEN_D[0], GEN_D[2], GEN_D[3]],
      kw("LG", "bolsa de malla lavadora {m}", "bolsa filtro lavadora {m}", "malla pelusas lavadora {m}", "bolsa pelusas lavadora {m}", "bolsa atrapa pelusas lavadora {m}",
         "comprar bolsa malla lavadora {m}"))
grupo("LG - Filtro redondo y rectangular", url("lg/filtro-pelusas-redondo-lavadora-lg"), "LG", "Filtro-Redondo",
      ["Filtro Redondo Lavadora LG", "Filtro de Pelusas Redondo LG", "Filtro Rectangular Lavadora LG", "Filtro de Pelusas LG", "Filtro para Lavadora LG", "Elige tu Filtro por Modelo"] + GEN_H[:9],
      ["Filtros de pelusas redondos y rectangulares para lavadora LG. El asesor confirma.", GEN_D[1], GEN_D[2], GEN_D[3]],
      kw("LG", "filtro redondo lavadora {m}", "filtro pelusas redondo lavadora {m}", "filtro rectangular lavadora {m}", "filtro lavadora {m} redondo", "filtro lavadora {m} azul",
         "filtro lavadora {m} gris", "filtro de lavadora {m} con tapa", "comprar filtro redondo lavadora {m}"))
# ---------------- genéricos ----------------
grupo("Filtro de pelusas - Todas las marcas", url(""), "Filtros", "Lavadoras",
      ["Filtro de Pelusas Lavadora", "Filtros para Lavadoras", "Filtro Lavadora Samsung y LG", "Bolsa de Malla Lavadora", "Filtro Atrapa Pelusas", "Elige tu Marca: Samsung o LG"] + GEN_H[:9],
      ["Filtros de pelusas para lavadoras Samsung y LG. Elige tu marca y pregunta al asesor.", GEN_D[0], GEN_D[2], GEN_D[3]],
      ["filtro de pelusas lavadora", "filtro pelusas lavadora", "filtro para lavadora", "filtro de lavadora", "filtro atrapa pelusas lavadora", "bolsa de malla lavadora", "malla filtro lavadora",
       "bolsa filtro lavadora", "comprar filtro lavadora", "filtro lavadora colombia", "filtro pelusas lavadora colombia", "donde comprar filtro de pelusas lavadora", "filtro de tina lavadora",
       "filtro lavadora carga superior", "filtro lavadora carga frontal"])
grupo("Ciudades principales", url(""), "Filtros", "Ciudades",
      ["Filtros Lavadora en Colombia", "Envío a Tu Ciudad", "Filtro Pelusas para Lavadora", "Bogotá, Medellín, Cali y más", "Consulta el Envío a tu Ciudad", "Filtros Samsung y LG"] + GEN_H[:9],
      ["Filtros de pelusas para lavadora con envío a Bogotá, Medellín, Cali y todo el país.", GEN_D[0], GEN_D[2], GEN_D[3]],
      [f"filtro lavadora {c}" for c in ["bogota", "medellin", "cali", "barranquilla", "cartagena", "bucaramanga", "pereira", "manizales", "cucuta", "ibague", "santa marta", "villavicencio"]]
      + [f"filtro pelusas lavadora {c}" for c in ["bogota", "medellin", "cali", "barranquilla"]],
      "Búsquedas por ciudad. Si una ciudad rinde más, sepárala en su propio grupo.")
grupo("Cambio y limpieza del filtro", url(""), "Filtros", "Cambio",
      ["Cambia el Filtro Lavadora", "Limpieza del Filtro de Pelusas", "Cómo Cambiar el Filtro", "Filtro Roto o Tapado", "Instalación Paso a Paso", "Filtros Samsung y LG"] + GEN_H[:9],
      ["¿Filtro roto o tapado? Mira cómo limpiarlo o cambiarlo, y pide el nuevo por WhatsApp.", GEN_D[1], GEN_D[2], GEN_D[3]],
      ["como cambiar filtro lavadora", "como limpiar filtro de pelusas lavadora", "cambiar filtro de pelusas lavadora", "filtro lavadora roto", "lavadora deja pelusas en la ropa", "lavadora suelta pelusas",
       "donde esta el filtro de pelusas de la lavadora", "cada cuanto limpiar filtro lavadora", "filtro de pelusas tapado lavadora"],
      "Intención más informativa: puja más baja que los grupos de compra. Solo concordancia de frase.")

NEGATIVAS = ["usado", "usada", "segunda mano", "casero", "casera", "reciclar", "manual", "pdf", "descargar", "video", "youtube", "curso", "empleo", "trabajo", "vacante", "gratis",
             "comprar lavadora", "lavadora nueva", "precio de lavadora", "lavadoras en oferta", "oferta lavadora", "falabella", "exito", "alkosto", "homecenter", "ktronix", "olx", "mercadolibre",
             "amazon", "alibaba", "aliexpress", "temu", "reparacion", "reparar", "servicio tecnico", "tecnico", "motor", "bomba", "tarjeta electronica", "compresor", "correa", "rodamiento",
             "empaque", "amortiguador", "mabe", "whirlpool", "haceb", "electrolux", "challenger", "kalley", "midea", "nevera", "refrigerador", "aire acondicionado", "pdf manual", "patente", "dibujo", "juguete"]
SITELINKS = [("Filtros Samsung", "Carga superior y frontal", "Pide el tuyo por WhatsApp", url("samsung")), ("Filtros LG", "Lavadoras y secadoras", "Pide el tuyo por WhatsApp", url("lg")),
             ("Filtro de secadora LG", "Filtro de pelusas", "Consulta por WhatsApp", url("lg/filtro-pelusas-secadora-lg")), ("Bolsa de malla Samsung", "Atrapa pelusas", "Consulta por WhatsApp", url("samsung/bolsa-malla-pelusas-lavadora-samsung")),
             ("Carga frontal Samsung", "Filtro con asa", "Consulta por WhatsApp", url("samsung/filtro-pelusas-lavadora-samsung-carga-frontal")), ("¿Cuál es mi filtro?", "Samsung: elige por tipo y modelo", "El asesor te confirma", url("samsung/cual-es-mi-filtro")),
             ("¿Cuál es mi filtro? LG", "LG: elige por tipo y modelo", "El asesor te confirma", url("lg/cual-es-mi-filtro")), ("Cómo cambiar el filtro", "Paso a paso", "Sin técnico ni herramientas", url("samsung/cambio-e-instalacion")),
             ("Envíos por ciudad", "Samsung: todas las ciudades", "Transportadora con guía", url("samsung/filtros-lavadora-samsung-por-ciudad")), ("Envíos por ciudad LG", "LG: todas las ciudades", "Transportadora con guía", url("lg/filtros-lavadora-lg-por-ciudad"))]
CALLOUTS = ["Pedido por WhatsApp", "Asesor por WhatsApp", "Envío a Toda Colombia", "Te Confirmamos el Modelo", "Instalación Paso a Paso", "Número de Guía", "Samsung y LG", "Sin Técnico"]
SNIPPET = ("Tipos", ["Filtro de pelusas", "Bolsa de malla", "Carga superior", "Carga frontal", "Secadora"])

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
            if g["nombre"].startswith("Cambio"):
                w.writerow([CAMP, g["nombre"], k, "Phrase"])
            else:
                w.writerow([CAMP, g["nombre"], k, "Phrase"]); w.writerow([CAMP, g["nombre"], k, "Exact"])
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
    md = [f"# Grupo {i}: {g['nombre']}", "", f"**Página de destino:** {g['url']}  ", f"**Rutas visibles:** {DOM}/{g['path1']}/{g['path2']}", ""]
    if g["nota"]: md += [f"> {g['nota']}", ""]
    md += ["## Títulos (máximo 30 caracteres)"] + [f"{j}. {t} ({len(t)})" for j, t in enumerate(g["titulos"], 1)]
    md += ["", "## Descripciones (máximo 90 caracteres)"] + [f"{j}. {d} ({len(d)})" for j, d in enumerate(g["descripciones"], 1)]
    md += ["", f"## Palabras clave ({len(g['claves'])})"] + [f"- {k}" for k in g["claves"]]
    (gd / f"{i:02d}-{re.sub('[^a-z0-9]+', '-', g['nombre'].lower()).strip('-')}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
(RAIZ / "03-palabras-negativas.md").write_text("# 3. Palabras negativas (a nivel de campaña)\n\nSon búsquedas por las que NO quieres pagar. Ya vienen en `05-archivos-para-importar/palabras-negativas.csv`. "
    "Incluyen las de quien busca comprar una lavadora (no un filtro) y otras marcas. Revisa el informe de **Términos de búsqueda** cada semana y agrega las que no te sirvan.\n\n" + "\n".join(f"- {k}" for k in NEGATIVAS) + "\n", encoding="utf-8")
ng = sum(len(g["claves"]) for g in G)
(QUI / "datos.json").write_text(json.dumps(dict(grupos=G, negativas=NEGATIVAS, sitelinks=SITELINKS, destacados=CALLOUTS, fragmento=SNIPPET, dominio=DOM, campana=CAMP, total_claves=ng), ensure_ascii=False, indent=1), encoding="utf-8")
print(f"OK: {len(G)} grupos, {ng} palabras clave, {len(NEGATIVAS)} negativas, {len(SITELINKS)} enlaces")
