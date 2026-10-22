# -*- coding: utf-8 -*-
"""Hoja de precios de venta (USD) para la tienda de EE. UU.: costo del proveedor + costos de operar = precio mínimo, objetivo y recomendado frente al mercado.
Lee la lista del proveedor (xlsx) y escribe precios/precios-de-venta.xlsx (con fórmulas editables) y ../prices.csv para el sitio."""
import csv, math, sys
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
LISTA = Path(sys.argv[1])

# supuestos (editables en la hoja «Supuestos»)
A = dict(fee_pct=0.054, fee_fijo=0.30, flete_pct=0.08, envio=5.60, envio_pack=6.50, ganancia_min=6.0, margen_min=0.15, piso=4.0)

# producto de la tienda -> (fila del proveedor, precio de la calle USD, rango visto, fuente/nota)
MERCADO = {
    "DA29-00020B / HAF-CIN": (34.99, "Lista 59.99; Allfilters 34.99; eBay desde 18.99", "allfilters.com, ebay.com"),
    "DA97-17376B / HAF-QIN": (36.99, "Genuino 34–44; Allfilters 36.99; terceros 28.99 por 3", "allfilters.com, slickdeals.net"),
    "DA29-10105J / HAF-EX": (19.0, "eBay 15–18 + envío; filtro en línea 4378411RB a 23.49 (Slyman)", "ebay, slymanbros.com"),
    "LT1000P": (54.99, "Genuino 54.99; terceros desde 12.95", "allfilters.com, star-power.com"),
    "LT800P": (54.97, "PC Richard 54.97", "pcrichard.com"),
    "LT700P": (49.99, "Walmart 50.99; Atomic 44.95; genérico 11–25", "walmart.com, atomicfilters.com"),
    "LT500P": (54.99, "Allfilters 54.99; terceros 12.95", "allfilters.com"),
    "EDR1RXD1": (49.98, "Amazon 49.98; lista 59.99; ofertas 30–33", "slickdeals.net, walmart.com"),
    "EDR2RXD1": (49.49, "Similar a EDR3/4/5 (49–57)", "allfilters.com"),
    "EDR3RXD1": (49.49, "Allfilters 49.49; Walmart 48; Sears 56.57", "allfilters.com, walmart.com"),
    "EDR4RXD1": (49.49, "Allfilters 49.49; Walmart 50.80–52", "allfilters.com, walmart.com"),
    "EDR5RXD1": (49.95, "Allfilters 49.95; lista 59.99", "allfilters.com"),
    "4378411RB": (23.49, "Slyman Bros 23.49", "slymanbros.com"),
    "MWF": (45.0, "Genuino 36–50 (Sears 37.14; Walmart 35.99; Allfilters 45.99)", "searspartsdirect.com, allfilters.com"),
    "XWFE": (None, "Solo genéricos a 18–25; sin precio del genuino", "walmart.com"),
}
# a qué producto de la tienda corresponde cada fila del proveedor
TIENDA = {"DA29-00020B / HAF-CIN": "sam-cin-o", "DA97-17376B / HAF-QIN": "sam-qin-o", "DA29-00003G / HAF-CU1 / HAF-FIN2": "sam-cu1-o", "DA29-10105J / HAF-EX": "sam-ex-o",
          "LT1000P": "lg-1000-o", "LT800P": "lg-800-o", "LT700P": "lg-700-o", "LT600P": "lg-600-o", "LT500P": "lg-500-o", "ADQ73693903 / FSS-002": "lg-ex-o",
          "EDR1RXD1": "wp-1-o", "EDR2RXD1": "wp-2-o", "EDR3RXD1": "wp-3-o", "EDR4RXD1": "wp-4-o", "EDR5RXD1": "wp-5-o", "4378411RB": "wp-ex-o", "MWF": "ge-mwf-o"}

wb0 = openpyxl.load_workbook(LISTA, data_only=True); ws0 = wb0.active
marca = None; filas = []
for r in ws0.iter_rows(min_row=2, values_only=True):
    if r[0] is None: continue
    if r[1] is None and r[2] is None:
        marca = str(r[0]).replace(" (with T codes)", ""); continue
    filas.append((marca, str(r[0]).strip(), r[1], r[2], r[3], (r[4] or "") if len(r) > 4 else ""))


def up99(x): return math.ceil(x) - 0.01 if x > 0 else 0


def calcular(costo):
    L = costo * (1 + A["flete_pct"]); C = L + A["envio"]; r = A["fee_pct"]; f = A["fee_fijo"]
    piso = (C + f + A["piso"]) / (1 - r)
    obj = max((C + f) / (1 - r - A["margen_min"]), (C + f + A["ganancia_min"]) / (1 - r))
    return L, C, piso, obj


def recomendado(costo, calle):
    L, C, piso, obj = calcular(costo)
    if calle is None: return up99(obj), "Sin precio de mercado: precio objetivo"
    if obj <= calle * 1.12: return up99(obj), "Competitivo"
    if piso <= calle * 1.10: return max(up99(piso), up99(calle * 1.04)), "Ganancia justa: igualar al mercado"
    return None, "No vender suelto: el mercado está casi al precio de costo"


out = RAIZ / "precios"; out.mkdir(exist_ok=True)
wb = openpyxl.Workbook()
s = wb.active; s.title = "Supuestos"
s.append(["Supuesto (cámbialo y la hoja se recalcula)", "Valor", "Qué es"])
rows = [("Comisión de PayPal (%)", A["fee_pct"], "Comisión por venta. Verifica la de tu cuenta: es una suposición conservadora para una cuenta en Colombia."),
        ("Comisión fija por venta (USD)", A["fee_fijo"], "Cargo fijo por transacción."),
        ("Flete y gastos hasta tu depósito (%)", A["flete_pct"], "Sobre el precio del proveedor: flete, aranceles, almacenaje. Pon el real."),
        ("Envío al cliente, 1 filtro (USD)", A["envio"], "Etiqueta + empaque. Si el precio incluye envío gratis, se suma al costo."),
        ("Envío al cliente, paquete de 2 (USD)", A["envio_pack"], "Etiqueta + empaque."),
        ("Ganancia mínima por pedido (USD)", A["ganancia_min"], "Para el precio objetivo."),
        ("Margen mínimo sobre el precio (%)", A["margen_min"], "Para el precio objetivo."),
        ("Ganancia mínima absoluta (USD)", A["piso"], "Para el precio mínimo (el piso).")]
for rw in rows: s.append(list(rw))
SUP = {k: f"Supuestos!$B${i + 2}" for i, k in enumerate(["fee", "fijo", "flete", "envio", "envio2", "gan", "marg", "piso"])}
for c, w in zip("ABC", (46, 12, 90)): s.column_dimensions[c].width = w

p = wb.create_sheet("Precios de venta")
H = ["Marca", "Referencia", "Producto en la tienda", "Costo proveedor (USD)", "Costo puesto en depósito", "Costo + envío al cliente", "Precio mínimo (ganancia ≥ piso)", "Precio objetivo", "Precio de la calle (mercado)", "PRECIO DE VENTA 1 filtro",
     "Ganancia por filtro (USD)", "Margen %", "Precio paquete de 2", "Ganancia paquete (USD)", "Veredicto", "Precios vistos en el mercado", "Fuente", "Cartón", "Nota del proveedor"]
p.append(H)
datos = []
r0 = 2
for i, (m, ref, costo, carton, pallet, nota) in enumerate(filas):
    if costo is None: continue
    key = ref.split(" without")[0] if False else ref
    mk = MERCADO.get(ref)
    calle = mk[0] if mk else None
    pid = TIENDA.get(ref)
    rec, verd = recomendado(costo, calle)
    rr = len(datos) + r0
    extra = ""
    if ref == "LT700P without T code": extra = "Variante sin código T: confirma con el proveedor qué significa antes de venderla como LG."
    if ref.startswith("XWFE") or m == "GE" and ref == "XWFE": extra = "Tu tienda de Colombia vende el XWF (no es igual al XWFE): confirma cuál vas a vender."
    datos.append(dict(m=m, ref=ref, pid=pid, costo=costo, calle=calle, rec=rec, verd=verd, mk=mk, carton=carton, nota=extra or str(nota).replace("\n", " ").strip()))
    p.append([m, ref, pid or "", costo,
              f"=D{rr}*(1+{SUP['flete']})", f"=E{rr}+{SUP['envio']}",
              f"=ROUNDUP((F{rr}+{SUP['fijo']}+{SUP['piso']})/(1-{SUP['fee']}),0)-0.01",
              f"=ROUNDUP(MAX((F{rr}+{SUP['fijo']})/(1-{SUP['fee']}-{SUP['marg']}),(F{rr}+{SUP['fijo']}+{SUP['gan']})/(1-{SUP['fee']})),0)-0.01",
              calle if calle else None,
              (rec if rec else None),
              (f"=J{rr}-J{rr}*{SUP['fee']}-{SUP['fijo']}-F{rr}" if rec else None),
              (f"=K{rr}/J{rr}" if rec else None),
              ((f"=ROUNDUP(MAX(2*J{rr}*0.92,(2*E{rr}+{SUP['envio2']}+{SUP['fijo']}+8)/(1-{SUP['fee']})),0)-0.01") if rec else None),
              ((f"=M{rr}-M{rr}*{SUP['fee']}-{SUP['fijo']}-2*E{rr}-{SUP['envio2']}") if rec else None),
              verd, (mk[1] if mk else "Sin datos de mercado"), (mk[2] if mk else ""), carton, datos[-1]["nota"]])
fmt_usd = '"$"#,##0.00'
head = PatternFill("solid", fgColor="0A5EA8"); thin = Side(style="thin", color="D9E4EE")
for c in range(1, len(H) + 1):
    x = p.cell(1, c); x.font = Font(bold=True, color="FFFFFF"); x.fill = head; x.alignment = Alignment(wrap_text=True, vertical="center")
    p.column_dimensions[get_column_letter(c)].width = [11, 32, 14, 12, 12, 12, 13, 12, 13, 15, 12, 9, 13, 13, 34, 52, 30, 8, 40][c - 1]
p.row_dimensions[1].height = 48
for rr in range(2, len(datos) + 2):
    for c in (4, 5, 6, 7, 8, 9, 10, 11, 13, 14): p.cell(rr, c).number_format = fmt_usd
    p.cell(rr, 12).number_format = "0.0%"
    p.cell(rr, 10).fill = PatternFill("solid", fgColor="E3F6EC"); p.cell(rr, 10).font = Font(bold=True)
    v = p.cell(rr, 15).value or ""
    if v.startswith("No vender"): p.cell(rr, 15).fill = PatternFill("solid", fgColor="FDE2E2")
    elif v.startswith("Ganancia justa"): p.cell(rr, 15).fill = PatternFill("solid", fgColor="FFF3CD")
p.freeze_panes = "C2"
n = wb.create_sheet("Cómo leer")
for t in ["Cómo se calcula el precio",
          "1. Costo puesto en depósito = precio del proveedor + flete y gastos (%).",
          "2. Costo + envío al cliente = lo anterior + etiqueta y empaque. El precio de venta incluye envío (envío gratis para el cliente).",
          "3. Precio mínimo: el menor precio con el que ganas el «piso» (USD) después de la comisión de PayPal.",
          "4. Precio objetivo: el menor precio que deja al menos la ganancia mínima y el margen mínimo.",
          "5. Precio de la calle: lo que he visto que cobran otras tiendas por el filtro original (capturas de búsqueda, pueden haber cambiado: verifícalos en Amazon, Walmart y Home Depot antes de publicar).",
          "6. PRECIO DE VENTA: el objetivo si es competitivo; si no, se iguala al mercado siempre que quede ganancia; si el mercado está casi al precio de costo, no conviene venderlo suelto.",
          "7. Paquete de 2: descuento de 8 % (mínimo $8 de ganancia): invita a comprar de a 2 y diluye el envío.",
          "",
          "Aviso: los precios de mercado son capturas de internet de 2025–2026; cambian a diario. Los costos de flete, aranceles y la comisión de PayPal son supuestos tuyos que debes ajustar en la hoja «Supuestos»."]:
    n.append([t])
n.column_dimensions["A"].width = 150; n["A1"].font = Font(bold=True, size=13)
wb.move_sheet("Supuestos", offset=1)
wb.save(out / "precios-de-venta.xlsx")

# prices.csv del sitio: solo los que sí conviene vender
tienda = {d["pid"]: d for d in datos if d["pid"] and d["rec"]}
ids = [l.split(",")[0] for l in (RAIZ / "prices.csv").read_text().splitlines()[1:]]
with open(RAIZ / "prices.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["id", "price_usd", "pack2_usd", "in_stock"])
    for i in ids:
        d = tienda.get(i)
        if d:
            L, C, piso, obj = calcular(d["costo"])
            pk = max(2 * d["rec"] * 0.92, (2 * L + A["envio_pack"] + A["fee_fijo"] + 8) / (1 - A["fee_pct"]))
            w.writerow([i, f"{d['rec']:.2f}", f"{up99(pk):.2f}", "yes"])
        else:
            w.writerow([i, "", "", "yes"])
for d in datos:
    if d["pid"] or d["mk"]:
        L, C, piso, obj = calcular(d["costo"])
        g = (d["rec"] - d["rec"] * A["fee_pct"] - A["fee_fijo"] - C) if d["rec"] else None
        print(f"{d['ref'][:34]:34} costo {d['costo']:6.2f} | piso {up99(piso):6.2f} obj {up99(obj):6.2f} calle {d['calle'] or 0:6.2f} -> VENTA {d['rec'] or 0:6.2f} gan {g if g is None else round(g,2)} | {d['verd']}")
