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


# ---- Datos clave (lo que los asistentes de IA citan) dentro de cada «Respuesta rápida»
def _datos(nombre, filas):
    f = OUT / nombre
    t = f.read_text(encoding="utf-8")
    if 'class="qa-datos"' in t or '<p class="qa-meta">' not in t:
        return
    ul = '<ul class="qa-datos">' + "".join(f"<li><b>{esc(k)}</b>{esc(v)}</li>" for k, v in filas) + "</ul>"
    f.write_text(t.replace('<p class="qa-meta">', ul + '<p class="qa-meta">', 1), encoding="utf-8")


_DATOS_COM = [("Envío", "Gratis a toda Colombia"), ("Pago", "Wompi o contra entrega"), ("Retracto", "5 días hábiles")]
_datos("index.html", [("Filtros", f"{len(PS)} referencias LG"), ("Precios", RANGO), ("Cobertura", f"{len(CIU)} ciudades y municipios"), ("Entrega", "1 a 7 días hábiles")] + _DATOS_COM)
for nombre, p in _prod_pag.items():
    _datos(nombre, [("Código", p["ref"]), ("Equivale a", ", ".join(p["refs"][1:4]) or p["ref"]), ("Nevecones", ", ".join(p["modelos"][:3]) or "Confirmar con el código viejo"), ("Tipo", "Externo" if p["ubic"] == "externo" else "Interno"), ("Precio", cop2(p["precio"]) + " COP"), ("Cambio", "Cada 6 meses")] + _DATOS_COM[:1])
for nombre, (m, p) in _mod_pag.items():
    _datos(nombre, [("Modelo", m), ("Filtro", p["corto"]), ("Código", p["ref"]), ("Precio", cop2(p["precio"]) + " COP"), ("Cambio", "Cada 6 meses")] + _DATOS_COM[:1])
for nombre, (r, p) in _ref_pag.items():
    _datos(nombre, [("Código consultado", r), ("Es el filtro", p["corto"]), ("Código principal", p["ref"]), ("Precio", cop2(p["precio"]) + " COP")] + _DATOS_COM[:1])
for nombre, s_ in _ciu_pag.items():
    c_ = CIUDAD[s_]
    _datos(nombre, [("Ciudad", c_[0]), ("Departamento", c_[1]), ("Entrega", ciudad_unica.dias_de(c_)), ("Precios", RANGO)] + _DATOS_COM[:2])
for nombre, s_ in _precio_pag.items():
    c_ = CIUDAD[s_]
    _datos(nombre, [("Ciudad", c_[0]), ("Desde", cop2(PREC[0])), ("Hasta", cop2(PREC[-1])), ("Entrega", ciudad_unica.dias_de(c_))] + _DATOS_COM[:1])
