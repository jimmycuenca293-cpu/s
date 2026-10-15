"""Genera la campaña de búsqueda de Google Ads para filtrosdeaguanevecon.com (CSV para Google Ads Editor + guía)."""
import csv
D = "https://filtrosdeaguanevecon.com"
CAMP = "PuroFiltro - Búsqueda - Colombia"
COMUNES_T = ["Envío Gratis a Toda Colombia", "Paga con PSE, Nequi o Tarjeta", "Asesoría por WhatsApp", "Llega en 2 a 3 Días Hábiles", "Pack Anual con Descuento", "Pago 100 % Seguro en Línea"]
COMUNES_D = ["Te ayudamos por WhatsApp a confirmar que es el de tu nevecón antes de comprar.",
             "Paga en línea con tarjeta, PSE, Nequi o botón Bancolombia. Precio final, sin sorpresas."]
GRUPOS = [
 {"nombre": "Samsung", "url": "/purofiltro-marca/samsung/", "p1": "Filtros", "p2": "Samsung",
  "t": ["Filtros Samsung para Nevecón", "Filtro HAF-CIN DA29-00020B", "Filtro HAF-QIN DA97-17376B", "Filtro Samsung Aqua-Pure", "Filtro Samsung desde $81.900", "Busca por Modelo de Nevecón", "Tutorial de Instalación", "Filtro Externo Samsung", "Compra en 2 Minutos"],
  "d": ["Filtros de agua para nevecón Samsung: HAF-CIN, HAF-QIN, Aqua-Pure y externo. Envío gratis.",
        "¿No sabes cuál es el tuyo? Búscalo por la referencia o el modelo de tu nevecón Samsung."],
  "kw": ["filtro nevecon samsung", "filtro de agua samsung", "filtro nevera samsung", "haf-cin", "haf cin", "da29-00020b", "haf-qin", "da97-17376b", "da29-00003g", "filtro samsung haf-cin", "filtro samsung haf-qin", "filtro externo samsung", "haf-cin/exp", "filtro agua nevera samsung"]},
 {"nombre": "LG", "url": "/purofiltro-marca/lg/", "p1": "Filtros", "p2": "LG",
  "t": ["Filtros LG para Nevecón", "Filtro LG LT1000P", "Filtro LG LT700P y LT800P", "Filtro LG LT500P y LT600P", "Filtro LG desde $81.900", "Busca por Modelo de Nevecón", "Tutorial de Instalación", "Filtro Externo LG", "Compra en 2 Minutos"],
  "d": ["Filtros de agua para nevecón LG: LT1000P, LT700P, LT800P, LT500P, LT600P y externo.",
        "¿No sabes cuál es el tuyo? Búscalo por la referencia o por el modelo de tu nevecón LG."],
  "kw": ["filtro nevecon lg", "filtro de agua lg", "filtro nevera lg", "lt1000p", "lt1000pc", "lt700p", "lt800p", "lt500p", "lt600p", "adq747935", "adq36006101", "filtro lg lt1000p", "filtro externo lg", "filtro agua nevera lg"]},
 {"nombre": "Whirlpool", "url": "/purofiltro-marca/whirlpool/", "p1": "Filtros", "p2": "Whirlpool",
  "t": ["Filtros Whirlpool EveryDrop", "EveryDrop 1, 2, 3, 4 y 5", "Filtro EDR1RXD1 EveryDrop 1", "Filtro UKF8001 EveryDrop 4", "Filtro Externo Whirlpool", "Para Maytag y KitchenAid", "Busca por Modelo de Nevecón", "Tutorial de Instalación", "Compra en 2 Minutos"],
  "d": ["Filtros EveryDrop 1 al 5 y externo 4378411RB para Whirlpool, Maytag, KitchenAid y Amana.",
        "¿No sabes cuál es el tuyo? Búscalo por la referencia o por el modelo de tu nevecón."],
  "kw": ["filtro whirlpool", "filtro nevecon whirlpool", "everydrop", "filtro everydrop", "edr1rxd1", "edr2rxd1", "edr3rxd1", "edr4rxd1", "edr5rxd1", "ukf8001", "w10295370a", "4378411rb", "filtro externo whirlpool", "filtro maytag", "filtro kitchenaid"]},
 {"nombre": "GE", "url": "/purofiltro-marca/ge/", "p1": "Filtros", "p2": "GE",
  "t": ["Filtros GE para Nevecón", "Filtro GE MWF", "Filtro GE XWF", "General Electric MWF y XWF", "Filtro MWF SmartWater", "Busca por Modelo de Nevecón", "Tutorial de Instalación", "Compra en 2 Minutos", "Filtros GE $158.900"],
  "d": ["Filtros de agua MWF y XWF para nevecones GE General Electric. Envío gratis a Colombia.",
        "¿Tu filtro dice MWF, MWFP o XWF? Te mostramos cuál es el tuyo y cómo instalarlo."],
  "kw": ["filtro ge mwf", "mwf", "mwfp", "smartwater mwf", "filtro xwf", "xwf", "filtro nevecon ge", "filtro general electric", "filtro nevera general electric", "filtro de agua ge"]},
 {"nombre": "Genérico", "url": "/", "p1": "Filtros", "p2": "Nevecon",
  "t": ["Filtros de Agua para Nevecón", "Samsung, LG, Whirlpool y GE", "Encuentra el Filtro Exacto", "Busca por Referencia", "Cambia tu Filtro Cada 6 Meses", "Agua y Hielo sin Mal Sabor", "Tutorial de Instalación", "Filtros desde $81.900", "Compra en 2 Minutos"],
  "d": ["Escribe la referencia de tu filtro o el modelo de tu nevecón y te mostramos el tuyo.",
        "Filtros para nevecón Samsung, LG, Whirlpool y GE con envío gratis a toda Colombia."],
  "kw": ["filtro de agua para nevecon", "filtro nevecon", "filtro de agua nevera", "filtro para nevera", "filtro nevera dispensador", "filtro refrigerador", "filtro de agua refrigerador", "cambiar filtro nevecon", "filtro agua nevecon", "repuesto filtro nevera"]},
]
NEGATIVAS = ["gratis", "pdf", "como hacer", "casero", "usado", "segunda", "olx", "empleo", "trabajo", "curso", "piscina", "acuario", "aire acondicionado", "lavadora", "carro", "moto", "jarra", "brita", "grifo", "ducha", "osmosis", "purificador de agua para casa", "filtro de aceite", "filtro de aire", "manual", "que es", "imagenes", "dibujo"]

errores = []
def ok(txt, n, que):
    if len(txt) > n: errores.append(f"{que} ({len(txt)}>{n}): {txt}")
    return txt
filas = []
for g in GRUPOS:
    T = g["t"] + COMUNES_T
    T = T[:15]
    Dd = g["d"] + COMUNES_D
    for x in T: ok(x, 30, "Título")
    for x in Dd: ok(x, 90, "Descripción")
    ok(g["p1"], 15, "Ruta"); ok(g["p2"], 15, "Ruta")
    g["T"], g["D"] = T, Dd
    fila = {"Campaign": CAMP, "Ad group": g["nombre"], "Ad type": "Responsive search ad", "Final URL": D + g["url"], "Path 1": g["p1"], "Path 2": g["p2"]}
    for i, x in enumerate(T, 1): fila[f"Headline {i}"] = x
    for i, x in enumerate(Dd, 1): fila[f"Description {i}"] = x
    filas.append(fila)
assert not errores, "\n".join(errores)
cols = ["Campaign", "Ad group", "Ad type", "Final URL", "Path 1", "Path 2"] + [f"Headline {i}" for i in range(1, 16)] + [f"Description {i}" for i in range(1, 5)]
with open("anuncios.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(filas)
with open("palabras-clave.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["Campaign", "Ad group", "Keyword", "Criterion Type"])
    for g in GRUPOS:
        for k in g["kw"]:
            w.writerow([CAMP, g["nombre"], k, "Phrase"]); w.writerow([CAMP, g["nombre"], k, "Exact"])
    for n in NEGATIVAS: w.writerow([CAMP, "", n, "Campaign Negative Phrase"])
import json; json.dump(GRUPOS, open("grupos.json", "w"), ensure_ascii=False)
print("ok", len(filas), "anuncios,", sum(len(g["kw"]) for g in GRUPOS) * 2, "palabras clave,", len(NEGATIVAS), "negativas")
