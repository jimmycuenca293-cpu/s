# Enlazado interno extra, HowTo y sitemap con imágenes. Se ejecuta dentro de ads_lg_paginas.py cuando ya están escritas todas las páginas.
import hashlib as _hl

_ciu_pag = {R_CIU(s): s for s in CIUDAD}
_prod_pag = {p["url"]: p for p in PS}
_mod_pag = {R_MOD(m): (m, p) for m, p in MODELOS}
_ref_pag = {R_REF(r): (r, p) for r, p in REFS}
_precio_pag = {R_PRECIO(s): s for s in GRANDES_S if s in CIUDAD}
_art = [(sl, t, d) for sl, t, d, *_ in ARTS]
_gen = [a for a in _art]


def _pick(clave, lista, n):
    r = random.Random(int(_hl.md5(clave.encode()).hexdigest()[:8], 16))
    l = list(lista)
    r.shuffle(l)
    return l[:n]


def _guias(clave, n=4):
    return "".join(f'<a href="{U(sl)}">{esc(t)}</a>' for sl, t, d in _pick(clave, _gen, n))


def _bloque(h, cuerpo):
    return f'<section class="aq-sec"><div class="wrap"><h2>{h}</h2><div class="city-tags">{cuerpo}</div></div></section>'


def _insertar(nombre, html):
    f = OUT / nombre
    t = f.read_text(encoding="utf-8")
    i = t.rfind('<footer class="aq-f">')
    if i < 0:
        return
    f.write_text(t[:i] + html + t[i:], encoding="utf-8")


ANC = ["Filtro LG {c} en {k}", "Comprar {c} en {k}", "Filtro de agua LG {c} · {k}", "{c} con envío a {k}", "Precio del {c} en {k}"]
for nombre, p in _prod_pag.items():
    cs = _pick("p" + nombre, TOP + list(CIUDAD), 14)
    ciud = "".join(f'<a href="{R_CIU(s)}">{esc(ANC[i % 5].format(c=p["corto"], k=CIUDAD[s][0].split(" (")[0]))}</a>' for i, s in enumerate(cs))
    mods = "".join(f'<a href="{R_MOD(m)}">Filtro para el nevecón LG {esc(m)}</a>' for m in p["modelos"])
    otras = "".join(f'<a href="{x["url"]}">{esc(x["nombre"])}</a>' for x in PS if x is not p)
    _insertar(nombre, _bloque(f"Envío del {esc(p['corto'])} a tu ciudad", ciud) + _bloque("Otras referencias y guías", mods + otras + _guias(nombre)))
for nombre, (m, p) in _mod_pag.items():
    cs = _pick("m" + nombre, TOP + list(CIUDAD), 10)
    _insertar(nombre, _bloque(f"Filtro para la nevera LG {esc(m)} en tu ciudad", "".join(f'<a href="{R_CIU(s)}">Filtro {esc(m)} en {esc(CIUDAD[s][0].split(" (")[0])}</a>' for s in cs)) + _bloque("Guías relacionadas", f'<a href="{p["url"]}">Ficha del {esc(p["corto"])}</a>' + _guias(nombre)))
for nombre, (r, p) in _ref_pag.items():
    _insertar(nombre, _bloque("Guías relacionadas", f'<a href="{p["url"]}">Ficha del {esc(p["corto"])}</a>' + "".join(f'<a href="{R_MOD(m)}">Nevecón {esc(m)}</a>' for m in p["modelos"]) + _guias(nombre)))
for nombre, s in _ciu_pag.items():
    nom = CIUDAD[s][0].split(" (")[0]
    prods = "".join(f'<a href="{p["url"]}">{esc(ANC[(i + len(s)) % 5].format(c=p["corto"], k=nom))}</a>' for i, p in enumerate(PS))
    mods = "".join(f'<a href="{R_MOD(m)}">Filtro nevecón LG {esc(m)}</a>' for m, p in _pick("cm" + s, MODELOS, 4))
    extra = f'<a href="{R_PRECIO(s)}">Precio del filtro LG en {esc(nom)}</a>' if s in GRANDES_S else ""
    _insertar(nombre, _bloque(f"Filtros LG que enviamos a {esc(nom)}", prods + extra + mods + _guias("c" + s, 3)))
for nombre in _precio_pag:
    s = _precio_pag[nombre]
    _insertar(nombre, _bloque("Más información", "".join(f'<a href="{p["url"]}">{esc(p["nombre"])}</a>' for p in PS[:3]) + _guias(nombre)))

# HowTo en la guía de instalación y en cada ficha de filtro interno
_pasos_how = [("Ubica el filtro", "Abre el refrigerador y localiza el filtro de agua."), ("Retira el viejo", "Gíralo suavemente y sácalo."), ("Instala el nuevo", "Quita las tapas protectoras y colócalo hasta que quede firme."),
              ("Purga el sistema", "Saca unos 6 litros de agua por el dispensador."), ("Reinicia el aviso", "Mantén presionado el botón del filtro unos segundos.")]
_how = {"@context": "https://schema.org", "@type": "HowTo", "name": "Cómo cambiar el filtro de agua de una nevera LG", "totalTime": "PT10M", "supply": [{"@type": "HowToSupply", "name": "Filtro de agua LG nuevo"}],
        "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": d} for i, (n, d) in enumerate(_pasos_how)]}
for nombre in ["cambio-e-instalacion.html"]:
    f = OUT / nombre
    t = f.read_text(encoding="utf-8")
    f.write_text(t.replace("</head>", '<script type="application/ld+json">' + json.dumps(_how, ensure_ascii=False) + "</script></head>", 1), encoding="utf-8")

# Sitemap con imágenes de producto
IMG_MAP = {p["url"]: f"{DOMINIO}/{p['img']}" for p in PS}
IMG_MAP["index.html"] = f"{DOMINIO}/{PS[0]['img']}"
