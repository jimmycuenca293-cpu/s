# -*- coding: utf-8 -*-
"""Catálogo de la tienda de EE. UU. (inglés). Sale de la tienda de Colombia: mismas referencias, alias y modelos, con textos nuevos.
Precios en dólares: se llenan en prices.csv (mientras estén vacíos, la página manda al cliente a WhatsApp o al correo)."""
import json, re, unicodedata
from pathlib import Path

AQUI = Path(__file__).resolve().parent
COL = json.loads((AQUI / "catalogo_colombia.json").read_text(encoding="utf-8"))


def slug(s):
    s = unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


BRANDS = {
    "samsung": {"name": "Samsung", "reset": "Press and hold the Water Filter button (or the Alarm / Filter Reset button, depending on the control panel) for about 3 seconds until the filter light turns off.",
                "series": "French door and side-by-side refrigerators with a water dispenser"},
    "lg": {"name": "LG", "reset": "Press and hold the Water Filter button (or Filter Reset) for about 3 seconds until the indicator light turns off or the display confirms the reset.",
           "series": "French door, side-by-side and top-freezer refrigerators with a water dispenser"},
    "whirlpool": {"name": "Whirlpool", "reset": "Press and hold the Water Filter (or Reset Water Filter) button for about 3 seconds until the indicator light turns off. On some models the reset is in the touch display menu.",
                  "series": "Whirlpool, Maytag, KitchenAid, Jenn-Air and Amana refrigerators"},
    "ge": {"name": "GE", "reset": "Press and hold the Reset Water Filter (or Filter) pad for about 3 seconds until the filter light turns off.",
           "series": "GE, GE Profile and Cafe refrigerators"},
}

# Datos propios de cada filtro (inglés). kind: internal = cartucho dentro del refrigerador; external = filtro en línea en la manguera de agua.
INFO = {
    "sam-cin-o": dict(line="HAF-CIN", kind="internal", short="Samsung HAF-CIN", also="Samsung HAF-CIN/EXP, DA29-00020A"),
    "sam-qin-o": dict(line="HAF-QIN", kind="internal", short="Samsung HAF-QIN", also="Samsung HAF-QIN/EXP, DA97-08006C"),
    "sam-cu1-o": dict(line="Aqua-Pure Plus HAF-CU1", kind="internal", short="Samsung Aqua-Pure Plus HAF-CU1", also="HAFCU1/XAA, HAFIN2/EXP, DA29-00003B, DA29-00003F"),
    "sam-ex-o": dict(line="HAF-EX", kind="external", short="Samsung HAF-EX external", also="HAFEX/EXP, WSF-100"),
    "lg-1000-o": dict(line="LT1000P", kind="internal", short="LG LT1000P", also="LT1000PC, LT1000PCS, ADQ74793501, ADQ74793502, MDJ64844601"),
    "lg-700-o": dict(line="LT700P", kind="internal", short="LG LT700P", also="LT700PC, ADQ36006101, ADQ36006102"),
    "lg-800-o": dict(line="LT800P", kind="internal", short="LG LT800P", also="LT800PC, LT800PCS, ADQ73613401, ADQ73613402"),
    "lg-500-o": dict(line="LT500P", kind="internal", short="LG LT500P", also="5231JA2002A, 5231JA2002B, ADQ72910901"),
    "lg-600-o": dict(line="LT600P", kind="internal", short="LG LT600P", also="5231JA2006A, 5231JA2006B, 5231JA2006F"),
    "lg-ex-o": dict(line="FSS-002", kind="external", short="LG external", also="FSS002, 5231JA2012A, 5231JA2012B"),
    "wp-1-o": dict(line="EveryDrop Filter 1", kind="internal", short="Whirlpool EveryDrop 1", also="W10295370A, W10295370, FILTER1, P4RFWB"),
    "wp-2-o": dict(line="EveryDrop Filter 2", kind="internal", short="Whirlpool EveryDrop 2", also="W10413645A, W10413645, FILTER2, P8RFWB2L"),
    "wp-3-o": dict(line="EveryDrop Filter 3", kind="internal", short="Whirlpool EveryDrop 3", also="4396841, 4396710, W10193691, FILTER3, P1RFWB"),
    "wp-4-o": dict(line="EveryDrop Filter 4", kind="internal", short="Whirlpool EveryDrop 4", also="UKF8001, UKF8001AXX, 4396395, FILTER4"),
    "wp-5-o": dict(line="EveryDrop Filter 5", kind="internal", short="Whirlpool EveryDrop 5", also="4396508, 4396509, 4396510, FILTER5, NLC240V"),
    "wp-ex-o": dict(line="Inline external", kind="external", short="Whirlpool external inline", also="4378411, WHKF-IMPL"),
    "ge-mwf-o": dict(line="MWF SmartWater", kind="internal", short="GE MWF SmartWater", also="MWFP, MWFA, MWFINT, GWF, GWFA, HWF, HWFA"),
    "ge-xwf-o": dict(line="XWF", kind="internal", short="GE XWF", also="XWF-1"),
}
# Notas sobre a qué refrigeradores va (de la tienda de Colombia, traducidas)
NOTES = {
    "sam-ex-o": "An external inline filter: it mounts on the water line outside the refrigerator, so it also suits dispenser models that do not have an internal filter.",
    "lg-600-o": "A long internal filter. To be sure it is the right one, send us a photo of the old filter or of the model label inside your refrigerator.",
    "lg-ex-o": "An external inline filter: it mounts on the water line outside the refrigerator, for LG models with a dispenser and no internal filter.",
    "wp-2-o": "Used in Whirlpool, Maytag, KitchenAid and Amana refrigerators. To confirm, send us a photo of the old filter or of the model label.",
    "wp-3-o": "Used in Whirlpool, Maytag, KitchenAid, Jenn-Air and Amana refrigerators. To confirm, send us a photo of the old filter or of the model label.",
    "wp-5-o": "Used in Whirlpool, Maytag, KitchenAid, Jenn-Air and Amana refrigerators. To confirm, send us a photo of the old filter or of the model label.",
    "wp-ex-o": "An external inline filter for refrigerators and ice makers, including Whirlpool, KitchenAid, Maytag, Amana and Estate.",
    "ge-mwf-o": "The filter used inside many GE two-door and French door refrigerators, in the upper right of the fresh-food compartment. To confirm, send us a photo of the old filter or of the model label.",
    "ge-xwf-o": "The filter used in newer GE French door refrigerators. It is not the same as the XWFE. To confirm, send us a photo of the old filter or of the model label.",
}


def load():
    P = []
    for pid, v in COL.items():
        i = INFO[pid]; b = BRANDS[v["brand_dir"]]
        ref = v["ref"]
        title = f"{i['short']} {ref} Refrigerator Water Filter" if ref.upper() not in i["short"].upper() and ref.upper() != i["line"].upper() else f"{i['short']} Refrigerator Water Filter"
        p = dict(id=pid, brand=v["brand_dir"], brand_name=b["name"], line=i["line"], kind=i["kind"], ref=ref, aliases=list(dict.fromkeys(v["alias"])), models=v["modelos"],
                 title=title, short=i["short"], also=i["also"], note=NOTES.get(pid, ""), photo=pid,
                 slug=slug(f"{i['short']} water filter" if slug(ref) in slug(i["short"]) else f"{i['short']} {ref} water filter"))
        P.append(p)
    return P


def prices():
    f = AQUI.parent / "prices.csv"
    out = {}
    if f.exists():
        for ln in f.read_text(encoding="utf-8").splitlines()[1:]:
            c = [x.strip() for x in ln.split(",")]
            if len(c) >= 2 and c[0]:
                out[c[0]] = dict(price=float(c[1]) if c[1] else None, pack=float(c[2]) if len(c) > 2 and c[2] else None, stock=(c[3].lower() != "no") if len(c) > 3 and c[3] else True)
    return out
