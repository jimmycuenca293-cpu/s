"""Genera la campaña de Google Ads de Filtros Nevecones Colombia (archivos para Google Ads Editor + documentos).
Basada en la tienda real: direcciones, referencias y precios salen del catálogo. Solo pago en línea (sin contra entrega).
Sin las palabras «original», «genuino» ni «compatible»."""
import csv, json, os, re, sys, zipfile
from pathlib import Path

QUI = Path(__file__).resolve().parent
RAIZ = QUI.parent
WEB = RAIZ.parent / "filtroya-web"
sys.path.insert(0, str(WEB))
import ads_marcas as A  # catálogo

DOM = "https://filtrosaguanevecones.com"
P = "purofiltro-"
CAMP = "Filtros Nevecones - Búsqueda - Colombia"
PROHIBIDAS = re.compile(r"original|genuin|compatib|100 ?%|mejor |garantiz|contra entrega", re.I)

cat = A.catalogo()
por_marca = {}
for p in cat:
    por_marca.setdefault(p["marca"], []).append(p)
PMIN = min(p["precio"] for p in cat)
cop = lambda n: "$" + f"{n:,}".replace(",", ".")

def url(ruta):
    d = WEB / "public_html" / (P + ruta.strip("/").split("/", 1)[0])
    assert d.exists(), ruta
    return f"{DOM}/{P}{ruta.strip('/')}/"

GEN_H = ["Envío Gratis a Toda Colombia", "Paga con PSE, Nequi o Tarjeta", "Asesoría por WhatsApp", "Llega en 2 a 3 Días Hábiles", "Pack Anual de 2 Filtros",
         "Busca por Referencia o Modelo", "Instálalo Tú en Minutos", "Precio Final, Envío Incluido", "Tienda Filtros Nevecones", "Compra en Línea Segura"]
GEN_D = ["Filtros de agua para nevecón con envío gratis a toda Colombia. Compra fácil y segura en línea.",
         "¿No sabes cuál es el tuyo? Búscalo por referencia o modelo y te asesoramos por WhatsApp.",
         "Paga en línea con tarjeta, PSE, Nequi o botón Bancolombia. Precio final, sin sorpresas.",
         "Recibe en tu casa con número de guía. Cada filtro trae su paso a paso para cambiarlo."]

def refs_de(p, n=3):
    return [r for r in p["refs"] if r.lower() != p["ref"].lower()][:n]

G = []   # grupos
def grupo(nombre, destino, path1, path2, titulos, descripciones, claves, nota=""):
    G.append(dict(nombre=nombre, url=destino, path1=path1, path2=path2, titulos=titulos, descripciones=descripciones, claves=claves, nota=nota))

# ---------------- grupos por marca de la tienda ----------------
def kw_marca(marca, extra=()):
    m = marca.lower()
    base = [f"filtro nevecon {m}", f"filtro de agua {m}", f"filtro nevera {m}", f"filtro agua nevera {m}", f"filtro refrigerador {m}", f"filtro de agua para nevera {m}",
            f"comprar filtro {m} nevera", f"precio filtro nevera {m}", f"filtro externo nevera {m}"]
    for p in por_marca[marca]:
        base += [f"filtro {m} {p['ref'].lower()}", p["ref"].lower()] + [r.lower() for r in refs_de(p, 4)]
    return list(dict.fromkeys(base + list(extra)))

samsung = por_marca["Samsung"]; lg = por_marca["LG"]; wp = por_marca["Whirlpool"]; ge = por_marca["GE"]
grupo("Samsung", url("marca/samsung"), "Filtros", "Samsung",
      ["Filtros Samsung para Nevecón", "Filtro HAF-CIN DA29-00020B", "Filtro HAF-QIN DA97-17376B", "Filtro Samsung Aqua-Pure Plus", f"Filtro Samsung desde {cop(min(p['precio'] for p in samsung))}", "Filtro Externo Samsung"] + GEN_H[:9],
      ["Filtros para nevecón Samsung: HAF-CIN, HAF-QIN, Aqua-Pure Plus y externo. Envío gratis.", "Escribe la referencia del filtro viejo o el modelo de tu Samsung y te mostramos el tuyo."] + GEN_D[2:],
      kw_marca("Samsung", ["haf cin", "haf-cin", "haf-qin", "haf qin", "aqua pure plus samsung", "filtro samsung rf28", "filtro samsung french door", "filtro samsung side by side"]))
grupo("LG", url("marca/lg"), "Filtros", "LG",
      ["Filtros LG para Nevecón", "Filtro LG LT1000P", "Filtro LG LT700P y LT800P", "Filtro LG LT500P y LT600P", f"Filtro LG desde {cop(min(p['precio'] for p in lg))}", "Filtro Externo LG"] + GEN_H[:9],
      ["Filtros para nevecón LG: LT1000P, LT700P, LT800P, LT500P, LT600P y externo. Envío gratis.", "Escribe la referencia del filtro viejo o el modelo de tu LG y te mostramos el tuyo."] + GEN_D[2:],
      kw_marca("LG", ["lt1000p", "lt700p", "lt800p", "lt500p", "lt600p", "filtro lg french door", "filtro lg instaview", "filtro lg side by side"]))
grupo("Whirlpool EveryDrop", url("marca/whirlpool"), "Filtros", "Whirlpool",
      ["Filtros Whirlpool para Nevecón", "Filtro EveryDrop 1 EDR1RXD1", "Filtro EveryDrop 2 EDR2RXD1", "Filtro EveryDrop 3 EDR3RXD1", "Filtro EveryDrop 4 y 5", f"Filtro Whirlpool desde {cop(min(p['precio'] for p in wp))}"] + GEN_H[:9],
      ["Filtros EveryDrop del 1 al 5 y externo para nevecón Whirlpool. Envío gratis a Colombia.", "Mira el número en la caja del filtro viejo (1 a 5) o escribe el modelo y verás el tuyo."] + GEN_D[2:],
      kw_marca("Whirlpool", ["everydrop", "filtro everydrop", "everydrop filtro 1", "everydrop filtro 2", "everydrop filtro 3", "everydrop filtro 4", "everydrop filtro 5", "ukf8001", "filtro ukf8001", "w10295370a", "4396841", "filtro whirlpool french door"]))
grupo("GE", url("marca/ge"), "Filtros", "GE",
      ["Filtros GE para Nevecón", "Filtro GE MWF", "Filtro GE XWF", f"Filtro GE desde {cop(min(p['precio'] for p in ge))}", "Filtro GE Profile y Café"] + GEN_H[:10],
      ["Filtros GE MWF y XWF para nevecón GE, GE Profile y Café. Envío gratis a toda Colombia.", "Escribe la referencia del filtro viejo o el modelo de tu GE y te mostramos el tuyo."] + GEN_D[2:],
      kw_marca("GE", ["mwf", "xwf", "filtro mwf", "filtro xwf", "filtro ge mwf", "filtro ge xwf", "filtro general electric nevera", "filtro ge profile", "filtro ge cafe"]))

# ---------------- grupos de otras marcas (páginas nuevas de la tienda) ----------------
OM = "otras-marcas/"
def otra(nombre, slug_, aliases, modelos=()):
    m = nombre.lower()
    k = [f"filtro nevera {m}", f"filtro agua {m}", f"filtro refrigerador {m}", f"filtro de agua para nevera {m}", f"filtro nevecon {m}", f"comprar filtro {m}", f"precio filtro nevera {m}"]
    for al in aliases:
        k += [f"filtro nevera {al.lower()}", f"filtro {al.lower()}", f"filtro agua nevera {al.lower()}"]
    k += [f"filtro {m} {x.lower()}" for x in modelos] + [f"filtro everydrop {m}"]
    grupo(nombre, url(f"otras-marcas/filtro-para-nevera-{slug_}"), "Filtros", nombre.replace("-", ""),
          [f"Filtro para Nevera {nombre}", f"Filtros {nombre} con Envío", f"Filtro EveryDrop {nombre}", "Filtro de Agua para Nevecón", f"Filtro {nombre} {cop(85900)}"] + GEN_H[:10],
          [f"Filtros para neveras {nombre}: mira cuál sirve a tu modelo. Envío gratis a Colombia.", "Compara la referencia del filtro viejo o el modelo de tu nevera y te decimos cuál es."] + GEN_D[2:],
          list(dict.fromkeys(k)), "Marca nombrada con permiso de uso de marca de revendedor: si Google la limita, usa los títulos por referencia.")
otra("KitchenAid", "kitchenaid", ["Kitchen Aid", "Kitchen Eye", "Kichen Aid"], ["KRFF305ESS", "KRFF507ESS"])
otra("Maytag", "maytag", ["MyTag", "Maitag"], ["MFI2570FEZ"])
otra("Jenn-Air", "jenn-air", ["Jenn Air", "Jennair"])
otra("Amana", "amana", ["Amana"])
grupo("Kenmore", url("otras-marcas/filtro-para-nevera-kenmore"), "Filtros", "Kenmore",
      ["Filtro para Nevera Kenmore", "Filtro Kenmore 46-9930", "Filtro Kenmore 46-9081", "Filtro Kenmore 46-9030", "Filtro Kenmore 46-9006", "Filtro Kenmore 46-9010", "Equivalencias Kenmore 46-9xxx"] + GEN_H[:8],
      ["Filtros con equivalencia para Kenmore 46-9930, 46-9081, 46-9030, 46-9006 y 46-9010.", "Busca tu referencia Kenmore y mira el filtro equivalente con su precio. Envío gratis."] + GEN_D[2:],
      ["filtro kenmore nevera", "filtro agua kenmore", "filtro refrigerador kenmore", "filtro kenmore 46-9930", "46-9930", "filtro kenmore 46-9081", "46-9081", "filtro kenmore 46-9030", "46-9030", "filtro kenmore 46-9006", "46-9006",
       "filtro kenmore 46-9010", "46-9010", "filtro kenmore 9930", "filtro kenmore 9006", "filtro kenmore 9081"])
ext = por_marca["Whirlpool"][-1]
grupo("Filtro externo", url("tienda"), "Filtros", "Externos",
      ["Filtro Externo para Nevera", "Filtro de Manguera para Nevera", f"Filtro Externo desde {cop(PMIN)}", "Filtro en Línea para Nevecón", "Instalación en 10 a 15 Minutos"] + GEN_H[:10],
      ["Filtros externos de manguera para nevera con dispensador. Se instalan sin herramientas.", "Para neveras Samsung, LG, Whirlpool, GE, Mabe, Haceb y otras. Envío gratis."] + GEN_D[2:],
      ["filtro externo nevera", "filtro externo para nevera", "filtro de manguera nevera", "filtro en linea nevera", "filtro externo refrigerador", "filtro externo nevecon", "filtro agua nevera manguera",
       "filtro externo samsung", "filtro externo lg", "filtro externo whirlpool", "4378411rb", "da29-10105j", "adq73693903", "filtro externo mabe", "filtro externo haceb", "filtro externo nevera electrolux"])

# ---------------- genéricos y ciudades ----------------
grupo("Filtro de agua para nevera", url("tienda"), "Tienda", "Filtros",
      ["Filtros de Agua para Nevera", "Filtro para Nevecón con Envío", "Samsung, LG, Whirlpool y GE", f"Filtros desde {cop(PMIN)}", "Todas las Marcas de Nevera", "Filtro Nevera con Dispensador"] + GEN_H[:9],
      ["Filtros para nevera y nevecón: Samsung, LG, Whirlpool, GE, KitchenAid y más. Envío gratis.", GEN_D[1], GEN_D[2], GEN_D[3]],
      ["filtro de agua para nevera", "filtro agua nevera", "filtro de nevera", "filtro para nevera", "filtro nevecon", "filtro de agua para nevecon", "filtro refrigerador agua", "filtro de agua nevera colombia",
       "comprar filtro de nevera", "comprar filtro de agua para nevera", "precio filtro de agua para nevera", "filtro de agua para nevera con dispensador", "filtro nevera con dispensador de agua y hielo",
       "filtro de agua para refrigerador", "filtro agua para nevera colombia", "filtros para neveras", "filtros de agua para neveras", "donde comprar filtro de nevera", "tienda de filtros para nevera", "filtro nevera envio a toda colombia"])
ciudades = ["Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena", "Bucaramanga", "Pereira", "Manizales", "Cúcuta", "Ibagué", "Santa Marta", "Villavicencio"]
kc = []
for c in ciudades:
    kc += [f"filtro nevera {c.lower()}", f"filtro de agua para nevera {c.lower()}", f"comprar filtro nevera {c.lower()}", f"filtro nevecon {c.lower()}"]
grupo("Ciudades principales", url("envios"), "Envios", "Colombia",
      ["Filtros de Nevera en Colombia", "Envío Gratis a tu Ciudad", "Filtros de Agua con Envío", "Consulta el Tiempo de Entrega", "Bogotá, Medellín, Cali y más"] + GEN_H[:10],
      ["Filtros para nevera con envío gratis a Bogotá, Medellín, Cali, Barranquilla y más.", "Mira el tiempo de entrega a tu ciudad y escoge tu filtro. Pago seguro en línea.", GEN_D[2], GEN_D[3]],
      kc, "Si quieres anuncios por ciudad, crea una campaña aparte por región y baja la puja en las ciudades que no vendan.")
grupo("Cambio e instalación", url("guia/como-cambiar-el-filtro-de-agua-del-nevecon"), "Guia", "Cambiar-Filtro",
      ["Cambiar Filtro de Nevera", "Cada Cuánto Cambiar el Filtro", "Luz del Filtro: Cómo Apagarla", "Cambio de Filtro Paso a Paso", "Filtro de Nevera Envío Gratis"] + GEN_H[:10],
      ["Aprende a cambiar el filtro de tu nevecón en minutos, sin técnico. Compra el tuyo aquí.", "¿Se prendió la luz del filtro? Te explicamos cómo reiniciarla y qué filtro necesitas.", GEN_D[2], GEN_D[3]],
      ["como cambiar el filtro de la nevera", "como cambiar filtro de agua nevera", "cada cuanto se cambia el filtro de la nevera", "cuando cambiar filtro de nevera", "luz del filtro nevera", "apagar luz del filtro nevera",
       "reiniciar luz filtro nevera", "nevera no saca agua filtro", "agua de la nevera sabe mal", "hielo de la nevera sabe feo", "cambiar filtro nevecon", "filtro de nevera vencido"],
      "Intención más informativa: puja más baja que los grupos de compra.")

NEGATIVAS = ["contra entrega", "pago contra entrega", "gratis", "usado", "segunda mano", "casero", "casera", "reciclar", "manual", "pdf", "descargar", "video", "youtube", "curso", "empleo", "trabajo", "vacante",
             "lavadora", "secadora", "aire acondicionado", "purificador", "botellon", "jarra", "pitcher", "bomba", "olx", "mercadolibre", "amazon", "alibaba", "aliexpress", "temu", "cerca de mi", "tienda fisica",
             "reparacion", "reparar", "tecnico", "repuesto nevera", "compresor", "termostato", "empaque", "motor", "tarjeta electronica", "mabe repuestos", "wikipedia", "que es", "patente", "dibujo", "juguete",
             "para casa de muñecas", "acuario", "piscina", "ducha", "grifo", "llave"]
SITELINKS = [("Filtros Samsung", "HAF-CIN, HAF-QIN y Aqua-Pure", "Con envío gratis a Colombia", url("marca/samsung")), ("Filtros LG", "LT1000P, LT700P, LT800P", "Con envío gratis a Colombia", url("marca/lg")),
             ("Filtros Whirlpool", "EveryDrop 1 al 5", "Con envío gratis a Colombia", url("marca/whirlpool")), ("Filtros GE", "MWF y XWF", "Con envío gratis a Colombia", url("marca/ge")),
             ("Otras marcas", "KitchenAid, Maytag, Kenmore", "Filtros EveryDrop y externos", url("otras-marcas")), ("Buscar por modelo", "Qué filtro usa tu nevera", "Mira la referencia correcta", url("neveras")),
             ("Cómo instalarlo", "Paso a paso por referencia", "Sin técnico ni herramientas", url("instalacion")), ("Envíos por ciudad", "Tiempo de entrega a tu ciudad", "Envío gratis", url("envios")),
             ("Preguntas frecuentes", "Respuestas rápidas", "Precios, pagos y envíos", url("otras-marcas/preguntas-frecuentes")), ("Contáctanos", "Asesoría por WhatsApp", "Te ayudamos a escoger", f"{DOM}/contacto.php")]
CALLOUTS = ["Envío Gratis a Colombia", "Pago Seguro en Línea", "Asesoría por WhatsApp", "Pack Anual de 2 Filtros", "Llega con Número de Guía", "Cambio Paso a Paso", "PSE, Nequi y Tarjeta", "Precio Final con Envío"]
SNIPPET = ("Marcas", ["Samsung", "LG", "Whirlpool", "GE", "KitchenAid", "Maytag", "Jenn-Air", "Amana", "Kenmore"])

# ---------------- validación ----------------
err = []
for g in G:
    t, d = g["titulos"], g["descripciones"]
    t = list(dict.fromkeys(t))[:15]; g["titulos"] = t
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
    if len(x) > 25: err.append(f"destacado largo: {x}")
for s in SITELINKS:
    if len(s[0]) > 25 or len(s[1]) > 35 or len(s[2]) > 35: err.append(f"sitelink largo: {s}")
if err:
    print("\n".join(err)); sys.exit(1)

# ---------------- salidas ----------------
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
            elif " " not in k and any(c.isdigit() for c in k):
                w.writerow([CAMP, g["nombre"], k, "Exact"])
            else:
                w.writerow([CAMP, g["nombre"], k, "Phrase"]); w.writerow([CAMP, g["nombre"], k, "Exact"])
with open(out / "palabras-negativas.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f); w.writerow(["Campaign", "Keyword", "Criterion Type"])
    for k in NEGATIVAS: w.writerow([CAMP, k, "Campaign negative phrase"])
with open(out / "enlaces-de-sitio.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f); w.writerow(["Campaign", "Link text", "Description line 1", "Description line 2", "Final URL"])
    for s in SITELINKS: w.writerow([CAMP] + list(s))
(RAIZ / "08-palabras-clave-para-copiar.txt").write_text("\n\n".join(f"# {g['nombre']}\n" + "\n".join(g["claves"]) for g in G), encoding="utf-8")

# grupos en markdown
gd = RAIZ / "02-grupos-de-anuncios"; gd.mkdir(exist_ok=True)
for f in gd.glob("*.md"): f.unlink()
for i, g in enumerate(G, 1):
    md = [f"# Grupo {i}: {g['nombre']}", "", f"**Página de destino:** {g['url']}  ", f"**Rutas visibles:** {DOM}/{g['path1']}/{g['path2']}", ""]
    if g["nota"]: md += [f"> {g['nota']}", ""]
    md += ["## Títulos (máximo 30 caracteres)"] + [f"{j}. {t} ({len(t)})" for j, t in enumerate(g["titulos"], 1)]
    md += ["", "## Descripciones (máximo 90 caracteres)"] + [f"{j}. {d} ({len(d)})" for j, d in enumerate(g["descripciones"], 1)]
    md += ["", f"## Palabras clave ({len(g['claves'])}, en frase y exacta)"] + [f"- {k}" for k in g["claves"]]
    (gd / f"{i:02d}-{re.sub('[^a-z0-9]+', '-', g['nombre'].lower()).strip('-')}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
(RAIZ / "03-palabras-negativas.md").write_text("# 3. Palabras negativas (a nivel de campaña)\n\nSon búsquedas por las que NO quieres pagar. Ya vienen en `05-archivos-para-importar/palabras-negativas.csv`.\n\n"
    "La tienda **no vende contra entrega**, por eso se excluye. Revisa el informe de **Términos de búsqueda** cada semana y agrega las que no te sirvan.\n\n" + "\n".join(f"- {k}" for k in NEGATIVAS) + "\n", encoding="utf-8")
ng = sum(len(g["claves"]) for g in G)
datos = dict(grupos=G, negativas=NEGATIVAS, sitelinks=SITELINKS, destacados=CALLOUTS, fragmento=SNIPPET, dominio=DOM, campana=CAMP, total_claves=ng)
(QUI / "datos.json").write_text(json.dumps(datos, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"OK: {len(G)} grupos, {ng} palabras clave ({ng*2} filas), {len(NEGATIVAS)} negativas, {len(SITELINKS)} enlaces")
