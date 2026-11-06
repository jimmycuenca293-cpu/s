"""Genera la campaña de Google Ads para la tienda de mangueras para lavadora (SIN marcas: sirve para todas las lavadoras).
Está dentro del mismo dominio de las otras tiendas (filtrosparalavadoras.click/mangueras-para-lavadora/), con la misma etiqueta de Tag Manager y el mismo evento «whatsapp».
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


GEN_H = ["Pago contra Entrega", "Pedido por WhatsApp", "Asesor Te Confirma la Correcta", "Envío a Toda Colombia", "Mangueras para Lavadora", "Escríbenos por WhatsApp",
         "Cambio Paso a Paso", "Precio por WhatsApp", "Atención por WhatsApp", "Envía la Foto de tu Manguera", "Te Decimos Cuál Necesitas"]
GEN_D = ["Dinos qué manguera necesitas por WhatsApp y te confirmamos el largo y el precio.",
         "Envía una foto de la manguera vieja y el asesor te dice cuál es.",
         "Cada manguera trae su paso a paso para cambiarla. Revisa la guía antes de pedir.",
         "Pago contra entrega: pagas cuando recibes el paquete. Envío con número de guía."]
G = []


def grupo(nombre, destino, path1, path2, titulos, descripciones, claves, nota=""):
    G.append(dict(nombre=nombre, url=destino, path1=path1, path2=path2, titulos=titulos, descripciones=descripciones, claves=claves, nota=nota))


def con_generales(esp):
    return esp + [h for h in GEN_H if h not in esp]


grupo("Entrada de agua", url("mangueras-de-entrada-de-agua-para-lavadora"), "Mangueras", "Entrada",
      con_generales(["Manguera de Entrada Lavadora", "Manguera de Agua Lavadora", "Manguera Entrada de Agua", "Mangueras de Entrada", "Manguera de Alimentación", "Manguera de Llenado", "Sirve para Todas las Lavadoras"]),
      ["Manguera de entrada de agua para lavadora: azul, naranja o negra. Sirve para todas.", GEN_D[0], GEN_D[1], GEN_D[3]],
      ["manguera de entrada lavadora", "manguera entrada de agua lavadora", "manguera de agua lavadora", "manguera de alimentacion lavadora", "manguera de llenado lavadora", "manguera de entrada de agua para lavadora",
       "manguera para lavadora", "comprar manguera lavadora", "manguera de conexion lavadora", "manguera de abastecimiento lavadora", "manguera de entrada para todas las lavadoras", "manguera de agua para cualquier lavadora",
       "manguera de entrada para lavadora", "precio manguera de entrada lavadora", "donde comprar manguera de agua para lavadora"])
grupo("Agua fría y caliente", url("manguera-agua-fria-y-caliente-lavadora-azul-y-naranja"), "Mangueras", "AzulNaranja",
      con_generales(["Manguera Azul Lavadora", "Manguera Naranja Lavadora", "Manguera Agua Fría", "Manguera Agua Caliente", "Manguera Azul y Naranja", "Azul Fría, Naranja Caliente", "Mangueras de Colores"]),
      ["Manguera azul para agua fría y naranja para agua caliente. Pídelas por WhatsApp.", GEN_D[0], GEN_D[1], GEN_D[3]],
      ["manguera azul lavadora", "manguera naranja lavadora", "manguera agua fria lavadora", "manguera agua caliente lavadora", "manguera azul y naranja lavadora", "manguera de agua caliente para lavadora",
       "manguera de agua fria para lavadora", "mangueras azul y naranja para lavadora", "manguera lavadora azul", "manguera lavadora naranja"])
grupo("Negra con rosca", url("manguera-negra-con-rosca-lavadora-carga-frontal"), "Mangueras", "NegraRosca",
      con_generales(["Manguera Negra con Rosca", "Manguera Negra Lavadora", "Manguera Carga Frontal", "Manguera con Rosca Lavadora", "Manguera de Caucho Lavadora", "Entrada Carga Frontal", "Manguera Negra Entrada"]),
      ["Manguera negra con rosca para lavadora de carga frontal. Más fina. Pídela por WhatsApp.", GEN_D[0], GEN_D[1], GEN_D[3]],
      ["manguera negra lavadora", "manguera negra con rosca lavadora", "manguera de entrada negra lavadora", "manguera lavadora carga frontal", "manguera de agua lavadora carga frontal", "manguera con rosca lavadora",
       "manguera de caucho lavadora", "manguera negra para lavadora", "manguera de entrada lavadora carga frontal", "manguera negra entrada de agua lavadora"])
grupo("Desagüe", url("mangueras-de-desague-para-lavadora"), "Mangueras", "Desague",
      con_generales(["Manguera de Desagüe Lavadora", "Manguera Desagüe", "Manguera de Drenaje", "Manguera Corrugada Lavadora", "Alargue Manguera Desagüe", "Manguera Desagüe con Codo", "Mangueras de Desagüe"]),
      ["Manguera de desagüe para lavadora: corrugada, larga o con funda. Pídela por WhatsApp.", GEN_D[0], GEN_D[1], GEN_D[3]],
      ["manguera de desague lavadora", "manguera desague lavadora", "manguera de desagüe lavadora", "manguera de drenaje lavadora", "manguera para desague lavadora", "manguera de desague para lavadora",
       "comprar manguera desague lavadora", "extension manguera desague lavadora", "manguera de salida de agua lavadora", "manguera de evacuacion lavadora", "manguera corrugada lavadora", "manguera de desague con codo lavadora",
       "manguera de desague lavadora colombia"])
grupo("Desagüe largo carga frontal", url("desague-largo-para-lavadora-de-carga-frontal"), "Mangueras", "DesagueLargo",
      con_generales(["Desagüe Largo Lavadora", "Manguera Desagüe Larga", "Desagüe Carga Frontal", "Manguera Larga Lavadora", "Manguera de Desagüe 2 m", "Extensión de Desagüe", "Desagüe con Extensión"]),
      ["Manguera de desagüe larga para lavadora de carga frontal. Te confirmamos el largo.", GEN_D[0], GEN_D[1], GEN_D[3]],
      ["manguera de desague larga lavadora", "manguera desague larga lavadora", "manguera de desague lavadora carga frontal", "manguera de desague para lavadora de carga frontal", "extension de desague lavadora",
       "manguera larga para desague de lavadora", "manguera desague lavadora 2 metros", "alargue de desague lavadora"])
grupo("Tina-bomba", url("manguera-tina-bomba-para-lavadora"), "Mangueras", "TinaBomba",
      con_generales(["Manguera Tina Bomba", "Manguera Tina-Bomba Lavadora", "Manguera de la Tina", "Manguera Interna Lavadora", "Manguera Tina a Bomba", "Manguera Bomba Lavadora", "Mangueras Internas"]),
      ["Manguera tina-bomba para lavadora: la que une la tina con la bomba de desagüe.", GEN_D[0], GEN_D[1], GEN_D[3]],
      ["manguera tina bomba lavadora", "manguera tina-bomba lavadora", "manguera de la tina lavadora", "manguera tina a bomba lavadora", "manguera interna lavadora", "manguera de la bomba lavadora",
       "manguera bomba de desague lavadora", "manguera entre tina y bomba lavadora", "manguera de tina lavadora", "manguera fuelle lavadora"])
grupo("Mangueras en general", url(""), "Mangueras", "Lavadora",
      con_generales(["Mangueras para Lavadora", "Manguera Lavadora", "Repuesto Manguera Lavadora", "Mangueras de Lavadora", "Todas las Mangueras", "Entrada, Desagüe y Más", "Sirven para Todas"]),
      ["Mangueras para lavadora: entrada, desagüe y tina-bomba. Pídela por WhatsApp.", GEN_D[0], GEN_D[1], GEN_D[3]],
      ["mangueras lavadora", "mangueras para lavadora", "manguera lavadora", "repuesto manguera lavadora", "repuestos mangueras lavadora", "donde comprar manguera lavadora", "precio manguera lavadora",
       "manguera lavadora carga superior", "mangueras para lavadoras colombia", "manguera lavadora envio a toda colombia", "mangueras de lavadora", "manguera para lavadora colombia"])

for M, c in (("Samsung", "samsung"), ("LG", "lg")):
    m = c
    grupo(f"Presostato {M}", url(f"presostato-lavadora-{c}-inverter-dc32-00025a" if c == "samsung" else "presostato-lavadora-lg-inverter-con-manguerita"), "Presostato", M,
          con_generales([f"Presostato Lavadora {M}", f"Presostato {M} Inverter", f"Sensor de Nivel {M}", f"Presostato para {M}", f"Presostato de Lavadora", f"Sensor Nivel de Agua {M}", f"Presostatos {M}"]),
          [f"Presostato para lavadora {M} inverter. Pídelo por WhatsApp.", GEN_D[0], GEN_D[1], GEN_D[3]],
          [f"presostato lavadora {m}", f"presostato para lavadora {m}", f"presostato {m} inverter", f"presostato lavadora {m} inverter", f"sensor de nivel lavadora {m}", f"sensor de nivel de agua lavadora {m}",
           f"presostato {m}", f"comprar presostato lavadora {m}", f"precio presostato lavadora {m}", f"repuesto presostato lavadora {m}", f"presostato de lavadora {m} colombia", f"donde comprar presostato lavadora {m}",
           f"presostato lavadora inverter {m}", f"presostato nivel de agua {m}", f"presostato lavadora {m} carga frontal", f"presostato lavadora {m} carga superior", f"presostato {m} lavadora"],
          "No es genérico: va por marca. Cada marca tiene su asesor de WhatsApp (Samsung 305 479 6329, LG 320 510 2995).")

NEGATIVAS = ["usado", "usada", "segunda mano", "casero", "casera", "reciclar", "manual", "pdf", "descargar", "video", "youtube", "curso", "empleo", "trabajo", "vacante", "gratis",
             "comprar lavadora", "lavadora nueva", "precio de lavadora", "lavadoras en oferta", "oferta lavadora", "falabella", "exito", "alkosto", "homecenter", "ktronix", "olx", "mercadolibre",
             "amazon", "alibaba", "aliexpress", "temu", "reparacion", "reparar", "servicio tecnico", "tecnico", "tecnico a domicilio", "tarjeta electronica", "compresor", "correa", "rodamiento",
             "empaque", "amortiguador", "nevera", "refrigerador", "aire acondicionado", "patente", "dibujo", "juguete",
             # mangueras que no son de lavadora
             "jardin", "riego", "piscina", "incendio", "bombero", "gas", "gas natural", "cocina", "estufa", "radiador", "refrigerante", "hidraulica", "hidraulico", "combustible", "gasolina",
             "aire comprimido", "compresor de aire", "ducha", "lavamanos", "lavaplatos", "lavavajillas", "sanitario", "inodoro", "calentador", "cafetera", "aspiradora", "hidrolavadora",
             "carro", "automovil", "moto", "bicicleta", "acuario", "pecera", "pozo", "tanque", "cisterna", "industrial", "alta presion", "por metro", "por metros", "rollo", "carrete",
             "sumergible", "presurizadora", "bomba de agua carro", "bomba de piscina", "bomba de presion", "bomba periferica", "bomba centrifuga", "bomba de achique", "bomba de desague lavadora",
             "bomba de agua lavadora", "motobomba", "filtro de pelusas", "filtro de lavadora"]
SITELINKS = [("Entrada de agua", "Azul, naranja y negra", "Sirven para todas", url("mangueras-de-entrada-de-agua-para-lavadora")),
             ("Mangueras de desagüe", "Corrugada, larga y con funda", "El asesor te confirma", url("mangueras-de-desague-para-lavadora")),
             ("Manguera tina-bomba", "La que va por dentro", "El asesor te confirma", url("manguera-tina-bomba-para-lavadora")),
             ("Azul y naranja", "Agua fría y agua caliente", "Cómo conectarlas", url("manguera-agua-fria-y-caliente-lavadora-azul-y-naranja")),
             ("Negra con rosca", "Para carga frontal", "Más fina, de caucho", url("manguera-negra-con-rosca-lavadora-carga-frontal")),
             ("Desagüe largo", "Para carga frontal", "Cómo elegir el largo", url("desague-largo-para-lavadora-de-carga-frontal")),
             ("¿Cuál es mi manguera?", "Elige por tipo", "El asesor te confirma", url("cual-es-mi-manguera")),
             ("Lavadora gotea", "Qué manguera revisar", "Guía paso a paso", url("lavadora-gotea-agua-por-la-manguera")),
             ("Lavadora no desagua", "Qué revisar", "Guía paso a paso", url("lavadora-no-desagua")),
             ("Cómo cambiar la manguera", "Paso a paso", "Revisa la guía antes de pedir", url("cambio-e-instalacion")),
             ("Presostato Samsung", "Sensor de nivel inverter", "Pregunta por WhatsApp", url("presostato-lavadora-samsung-inverter-dc32-00025a")),
             ("Presostato LG", "Sensor de nivel inverter", "Pregunta por WhatsApp", url("presostato-lavadora-lg-inverter-con-manguerita"))]
CALLOUTS = ["Pedido por WhatsApp", "Asesor por WhatsApp", "Envío a Toda Colombia", "Confirmamos la Correcta", "Pago contra Entrega", "Número de Guía", "Sirven para Todas", "Guía de Cambio"]
SNIPPET = ("Tipos", ["Manguera de entrada", "Manguera de desagüe", "Manguera tina-bomba", "Agua fría (azul)", "Agua caliente (naranja)", "Presostato"])

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
    + f"\n\n## Fragmento estructurado\n**{SNIPPET[0]}:** {', '.join(SNIPPET[1])}\n\n## Llamadas\n- Mangueras: 305 479 6329. Presostato Samsung: 305 479 6329. Presostato LG: 320 510 2995. Agrégalos como recursos de llamada y limítalos al horario de atención.\n\n## Imágenes\n- Usa las fotos de las mangueras de la tienda (cuadradas 1:1 y 1,91:1).\n", encoding="utf-8")
ng = sum(len(g["claves"]) for g in G)
(QUI / "datos.json").write_text(json.dumps(dict(grupos=G, negativas=NEGATIVAS, sitelinks=SITELINKS, destacados=CALLOUTS, fragmento=SNIPPET, dominio=DOM, campana=CAMP, total_claves=ng), ensure_ascii=False, indent=1), encoding="utf-8")
print(f"OK: {len(G)} grupos, {ng} palabras clave, {len(NEGATIVAS)} negativas, {len(SITELINKS)} enlaces")
