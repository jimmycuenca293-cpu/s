"""Genera la campaña de Google Ads para la tienda de bombas de agua (bombas de desagüe) para lavadoras Samsung y LG.
Está dentro del mismo dominio de la tienda de filtros (filtrosparalavadoras.click/bombas-de-agua/), con la misma etiqueta de Tag Manager y el mismo evento «whatsapp».
Sin las palabras «original», «genuino» ni «compatible». Sin precios ni promesas: el precio lo da el asesor por WhatsApp."""
import csv, json, re, sys
from pathlib import Path

QUI = Path(__file__).resolve().parent
RAIZ = QUI.parent
WEB = RAIZ.parent / "filtroya-web" / "sitios-bombas" / "tienda" / "bombas-de-agua"
DOM = "https://filtrosparalavadoras.click/bombas-de-agua"
CAMP = "Bombas Lavadoras - Búsqueda - Colombia"
PROHIBIDAS = re.compile(r"original|genuin|compatib|100 ?%|mejor |garantiz|gratis", re.I)


def url(ruta):
    r = ruta.strip("/")
    assert ((WEB / r / "index.php").exists() if r else (WEB / "index.php").exists()), ruta
    return f"{DOM}/{r}/" if r else f"{DOM}/"


GEN_H = ["Pago contra Entrega", "Pedido por WhatsApp", "Asesor Te Confirma el Modelo", "Envío a Toda Colombia", "Bombas para Samsung y LG", "Escríbenos por WhatsApp",
         "Cambio Paso a Paso", "Precio por WhatsApp", "Atención por WhatsApp", "Envía la Foto de tu Bomba", "Te Decimos Cuál Necesitas"]
GEN_D = ["Dinos el modelo de tu lavadora por WhatsApp y te confirmamos la bomba que necesita.",
         "Envía la etiqueta del modelo o una foto de la bomba vieja y el asesor te dice cuál es.",
         "Cada bomba trae su paso a paso para cambiarla. Revisa la guía antes de pedir.",
         "Pago contra entrega: pagas cuando recibes el paquete. Envío con número de guía."]
G = []


def grupo(nombre, destino, path1, path2, titulos, descripciones, claves, nota=""):
    G.append(dict(nombre=nombre, url=destino, path1=path1, path2=path2, titulos=titulos, descripciones=descripciones, claves=claves, nota=nota))


def kw(marca, *frases):
    return [f.replace("{m}", marca.lower()) for f in frases]


BASE_KW = ["bomba de agua lavadora {m}", "bomba de agua para lavadora {m}", "bomba agua lavadora {m}", "bomba de desague lavadora {m}", "bomba desague lavadora {m}",
           "bomba de drenaje lavadora {m}", "bomba de vaciado lavadora {m}", "motobomba lavadora {m}", "bomba lavadora {m}", "bomba para lavadora {m}", "comprar bomba lavadora {m}",
           "repuesto bomba lavadora {m}", "bomba lavadora {m} colombia", "donde comprar bomba lavadora {m}", "precio bomba lavadora {m}", "bomba de agua {m} lavadora carga frontal",
           "bomba de agua {m} lavadora carga superior"]
for M, REF, FAM in [("Samsung", "DC31-00181C", ["wa", "ww", "wf"]), ("LG", "4681EA2001T", ["wt", "wm", "wd"])]:
    c = M.lower(); R = REF.lower()
    claves = (kw(M, *BASE_KW)
              + kw(M, "bomba lavadora {m} carga superior", "bomba lavadora {m} carga frontal", "bomba desague lavadora {m} carga superior", "bomba desague lavadora {m} carga frontal")
              + [f"bomba lavadora {c} {f}" for f in FAM] + [f"bomba desague lavadora {c} {f}" for f in FAM]
              + [R, f"bomba {R}", f"bomba desague {R}", f"bomba {R.replace('-', ' ')}"])
    grupo(f"{M} - Bomba", url(c), "Bombas", M,
          [f"Bomba de Agua Lavadora {M}", f"Bomba de Desagüe {M}", f"Bomba para Lavadora {M}", f"Motobomba Lavadora {M}", f"Bomba {M} Carga Superior", f"Bomba {M} Carga Frontal",
           f"Bomba {M} {REF}", f"Bombas para Lavadora {M}"] + GEN_H[:7],
          [f"Bomba de desagüe (bomba de agua) para lavadora {M}. Pide la tuya por WhatsApp.", GEN_D[0], GEN_D[1], GEN_D[3]],
          claves)

NEGATIVAS = ["usado", "usada", "segunda mano", "casero", "casera", "reciclar", "manual", "pdf", "descargar", "video", "youtube", "curso", "empleo", "trabajo", "vacante", "gratis",
             "comprar lavadora", "lavadora nueva", "precio de lavadora", "lavadoras en oferta", "oferta lavadora", "falabella", "exito", "alkosto", "homecenter", "ktronix", "olx", "mercadolibre",
             "amazon", "alibaba", "aliexpress", "temu", "reparacion", "reparar", "servicio tecnico", "tecnico", "tecnico a domicilio", "tarjeta electronica", "compresor", "correa", "rodamiento",
             "empaque", "amortiguador", "mabe", "whirlpool", "haceb", "electrolux", "challenger", "kalley", "midea", "frigidaire", "general electric", "nevera", "refrigerador", "aire acondicionado",
             "pdf manual", "patente", "dibujo", "juguete",
             # bombas que no son de lavadora
             "piscina", "sumergible", "presurizadora", "hidroneumatico", "hidroneumatica", "jardin", "riego", "acuario", "pecera", "pozo", "tanque", "cisterna", "bomba de vacio",
             "bomba de calor", "bomba de gasolina", "bomba de combustible", "bomba de agua carro", "bomba de agua automovil", "radiador", "motor de carro", "bomba de aire", "bomba hidraulica",
             "bomba de presion", "bomba de achique", "bomba periferica", "bomba centrifuga", "lavavajillas", "lavaplatos", "dispensador", "bicicleta", "moto"]
SITELINKS = [("Bombas Samsung", "Carga superior y frontal", "Pide la tuya por WhatsApp", url("samsung")), ("Bombas LG", "Carga superior y frontal", "Pide la tuya por WhatsApp", url("lg")),
             ("Referencia DC31-00181C", "Bomba de desagüe Samsung", "Consulta por WhatsApp", url("samsung/bomba-desague-lavadora-samsung-dc31-00181c")),
             ("Referencia 4681EA2001T", "Bomba de desagüe LG", "Consulta por WhatsApp", url("lg/bomba-desague-lavadora-lg-motor-negro-4681ea2001t")),
             ("Samsung no desagua", "Qué revisar y qué bomba", "El asesor te confirma", url("samsung/lavadora-samsung-no-desagua")),
             ("LG no desagua", "Qué revisar y qué bomba", "El asesor te confirma", url("lg/lavadora-lg-no-desagua")),
             ("¿Cuál es mi bomba?", "Samsung: elige por tipo y modelo", "El asesor te confirma", url("samsung/cual-es-mi-bomba")),
             ("¿Cuál es mi bomba? LG", "LG: elige por tipo y modelo", "El asesor te confirma", url("lg/cual-es-mi-bomba")),
             ("Cómo cambiar la bomba", "Paso a paso", "Revisa la guía antes de pedir", url("samsung/cambio-e-instalacion")),
             ("Envíos por ciudad", "Samsung y LG: todo el país", "Transportadora con guía", url("samsung/bombas-lavadora-samsung-por-ciudad"))]
CALLOUTS = ["Pedido por WhatsApp", "Asesor por WhatsApp", "Envío a Toda Colombia", "Te Confirmamos el Modelo", "Pago contra Entrega", "Número de Guía", "Samsung y LG", "Guía de Cambio"]
SNIPPET = ("Tipos", ["Bomba de desagüe", "Carga superior", "Carga frontal", "Motobomba"])

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
    "Incluyen las de quien busca comprar una lavadora (no una bomba), otras marcas y otras clases de bomba (piscina, pozo, carro, presurizadora…). Revisa el informe de **Términos de búsqueda** cada semana y agrega las que no te sirvan.\n\n" + "\n".join(f"- {k}" for k in NEGATIVAS) + "\n", encoding="utf-8")
(RAIZ / "04-recursos-extensiones.md").write_text("# Recursos (extensiones) a nivel de campaña\n\n## Enlaces de sitio (título ≤25, descripciones ≤35)\n"
    + "\n".join(f"- **{s[0]}** — {s[1]} / {s[2]} → {s[3]}" for s in SITELINKS) + "\n\n## Textos destacados (≤25)\n" + "\n".join(f"- {c}" for c in CALLOUTS)
    + f"\n\n## Fragmento estructurado\n**{SNIPPET[0]}:** {', '.join(SNIPPET[1])}\n\n## Llamadas\n- Samsung: 305 479 6329 · LG: 320 510 2995. Agrega los dos como recurso de llamada y limítalos al horario de atención.\n\n## Imágenes\n- Usa las fotos de las bombas de la tienda (cuadradas 1:1 y 1,91:1).\n", encoding="utf-8")
ng = sum(len(g["claves"]) for g in G)
(QUI / "datos.json").write_text(json.dumps(dict(grupos=G, negativas=NEGATIVAS, sitelinks=SITELINKS, destacados=CALLOUTS, fragmento=SNIPPET, dominio=DOM, campana=CAMP, total_claves=ng), ensure_ascii=False, indent=1), encoding="utf-8")
print(f"OK: {len(G)} grupos, {ng} palabras clave, {len(NEGATIVAS)} negativas, {len(SITELINKS)} enlaces")
