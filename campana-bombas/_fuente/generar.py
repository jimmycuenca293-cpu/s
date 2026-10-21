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
for M, TELEF, REF, REFURL, CODIGOS, FAM_SUP, FAM_FRO in [
        ("Samsung", "305 479 6329", "DC31-00181C", "samsung/bomba-desague-lavadora-samsung-dc31-00181c", ["5e", "se", "5c"], ["wa"], ["ww", "wf"]),
        ("LG", "320 510 2995", "4681EA2001T", "lg/bomba-desague-lavadora-lg-motor-negro-4681ea2001t", ["oe"], ["wt"], ["wm", "wd"])]:
    c = M.lower(); R = REF.lower()
    grupo(f"{M} - Bomba de agua", url(c), "Bombas", M,
          [f"Bomba de Agua Lavadora {M}", f"Bomba de Desagüe {M}", f"Bomba para Lavadora {M}", f"Motobomba Lavadora {M}", f"Bomba de Drenaje {M}", f"Bomba {M} Colombia", f"Bombas para Lavadora {M}"] + GEN_H[:8],
          [f"Bomba de desagüe (bomba de agua) para lavadora {M}. Pide la tuya por WhatsApp.", GEN_D[0], GEN_D[2], GEN_D[3]],
          kw(M, *BASE_KW))
    grupo(f"{M} - Carga superior", url(f"{c}/bomba-lavadora-{c}-carga-superior"), M, "Carga-Superior",
          [f"Bomba {M} Carga Superior", f"Bomba de Agua {M} Superior", f"Bomba Desagüe {M} Superior", f"Bomba para Lavadora {M}", "Elige tu Bomba por Modelo", "Cambio Paso a Paso"] + GEN_H[:9],
          [f"Bomba de desagüe para lavadora {M} de carga superior. El asesor confirma el modelo.", GEN_D[1], GEN_D[2], GEN_D[3]],
          kw(M, "bomba lavadora {m} carga superior", "bomba de agua lavadora {m} carga superior", "bomba desague lavadora {m} carga superior", "bomba lavadora {m} superior",
             "bomba de agua {m} lavadora superior", "comprar bomba lavadora {m} carga superior") + [f"bomba lavadora {c} {f}" for f in FAM_SUP] + [f"bomba desague lavadora {c} {f}" for f in FAM_SUP])
    grupo(f"{M} - Carga frontal", url(f"{c}/bomba-lavadora-{c}-carga-frontal"), M, "Carga-Frontal",
          [f"Bomba {M} Carga Frontal", f"Bomba de Agua {M} Frontal", f"Bomba Desagüe {M} Frontal", f"Bomba para Lavadora {M}", "Elige tu Bomba por Modelo", "Cambio Paso a Paso"] + GEN_H[:9],
          [f"Bomba de desagüe para lavadora {M} de carga frontal. El asesor confirma el modelo.", GEN_D[1], GEN_D[2], GEN_D[3]],
          kw(M, "bomba lavadora {m} carga frontal", "bomba de agua lavadora {m} carga frontal", "bomba desague lavadora {m} carga frontal", "bomba lavadora {m} frontal",
             "bomba de agua {m} lavadora frontal", "bomba lavadora {m} puerta frontal", "comprar bomba lavadora {m} carga frontal") + [f"bomba lavadora {c} {f}" for f in FAM_FRO] + [f"bomba desague lavadora {c} {f}" for f in FAM_FRO])
    grupo(f"{M} - Referencia {REF}", url(REFURL), "Bombas", REF,
          [f"Bomba {REF}", f"Bomba Desagüe {REF}", f"Bomba {M} {REF}", "Consulta por WhatsApp", "Te Confirmamos el Modelo", "Bomba de Agua Lavadora"] + GEN_H[:9],
          [f"Bomba de desagüe referencia {REF} para lavadora {M}. Consulta por WhatsApp.", GEN_D[1], GEN_D[2], GEN_D[3]],
          [f"{R}", f"bomba {R}", f"bomba desague {R}", f"bomba lavadora {R}", f"bomba {R.replace('-', ' ')}", f"{R.replace('-', ' ')} bomba", f"comprar bomba {R}", f"bomba de agua {R}"],
          f"La referencia sale de la etiqueta de la foto del producto. Si cambias de proveedor y la referencia deja de aplicar, pausa este grupo.")
    grupo(f"{M} - Lavadora no desagua", url(f"{c}/lavadora-{c}-no-desagua"), M, "No-Desagua",
          [f"Lavadora {M} No Desagua", f"Falla de Desagüe {M}", "¿Será la Bomba de Agua?", "Qué Revisar Antes de Cambiar", "Cambia la Bomba Paso a Paso", f"Bomba de Agua {M}"] + GEN_H[:9],
          [f"¿Tu lavadora {M} no desagua? Mira qué revisar y pide la bomba por WhatsApp.", GEN_D[1], GEN_D[2], GEN_D[3]],
          kw(M, "lavadora {m} no desagua", "lavadora {m} no saca el agua", "lavadora {m} no vacia el agua", "lavadora {m} no centrifuga", "lavadora {m} hace ruido al desaguar",
              "lavadora {m} se queda con agua", "lavadora {m} no escurre", "bomba de lavadora {m} danada", "como saber si la bomba de la lavadora {m} esta danada")
          + [f"lavadora {c} error {k}" for k in CODIGOS] + [f"lavadora {c} codigo {k}" for k in CODIGOS],
          "Búsquedas informativas: puja 30 % más baja que los grupos de compra. Solo concordancia de frase.")
# ---------------- genéricos ----------------
grupo("Bomba de lavadora - Samsung y LG", url(""), "Bombas", "Lavadoras",
      ["Bomba de Agua para Lavadora", "Bomba de Desagüe Lavadora", "Bombas para Lavadoras", "Bomba Lavadora Samsung y LG", "Elige tu Marca: Samsung o LG", "Motobomba para Lavadora"] + GEN_H[:9],
      ["Bombas de desagüe para lavadoras Samsung y LG. Elige tu marca y pregunta al asesor.", GEN_D[0], GEN_D[2], GEN_D[3]],
      ["bomba de agua lavadora", "bomba de agua para lavadora", "bomba de desague lavadora", "bomba desague lavadora", "bomba de drenaje lavadora", "motobomba lavadora", "bomba de lavadora",
       "bomba lavadora", "comprar bomba lavadora", "bomba lavadora colombia", "bomba de agua lavadora colombia", "repuesto bomba lavadora", "donde comprar bomba de lavadora",
       "bomba de desague lavadora carga frontal", "bomba de desague lavadora carga superior"],
      "Búsquedas sin marca: pueden traer gente con otras marcas. Vigila «Términos de búsqueda» la primera semana.")
grupo("Ciudades principales", url(""), "Bombas", "Ciudades",
      ["Bombas Lavadora en Colombia", "Envío a Tu Ciudad", "Bomba de Agua Lavadora", "Bogotá, Medellín, Cali y más", "Consulta el Envío a tu Ciudad", "Bombas Samsung y LG"] + GEN_H[:9],
      ["Bomba de desagüe para lavadora con envío a Bogotá, Medellín, Cali y todo el país.", GEN_D[0], GEN_D[2], GEN_D[3]],
      [f"bomba lavadora {c}" for c in ["bogota", "medellin", "cali", "barranquilla", "cartagena", "bucaramanga", "pereira", "manizales", "cucuta", "ibague", "santa marta", "villavicencio"]]
      + [f"bomba de agua lavadora {c}" for c in ["bogota", "medellin", "cali", "barranquilla"]],
      "Búsquedas por ciudad. Si una ciudad rinde más, sepárala en su propio grupo.")
grupo("Cambio de la bomba", url("samsung/cambio-e-instalacion"), "Bombas", "Cambio",
      ["Cambia la Bomba de Lavadora", "Cómo Cambiar la Bomba", "Bomba de Agua Dañada", "Instalación Paso a Paso", "Bombas Samsung y LG", "Pide tu Bomba por WhatsApp"] + GEN_H[:9],
      ["¿Bomba dañada? Mira cómo cambiarla paso a paso y pide la nueva por WhatsApp.", GEN_D[1], GEN_D[2], GEN_D[3]],
      ["como cambiar bomba de desague lavadora", "como cambiar la bomba de agua de la lavadora", "cambiar bomba de lavadora", "como saber si la bomba de la lavadora esta danada",
       "bomba de lavadora danada", "lavadora no desagua bomba", "donde esta la bomba de la lavadora", "bomba de desague lavadora como funciona", "lavadora no desagua que hacer"],
      "Intención más informativa: puja más baja que los grupos de compra. Solo concordancia de frase. La página de destino es la de Samsung; si prefieres, crea uno igual para LG apuntando a su guía.")

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

INFORMATIVOS = ("Cambio", "Samsung - Lavadora no", "LG - Lavadora no")
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
            if not g["nombre"].startswith(INFORMATIVOS):
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
