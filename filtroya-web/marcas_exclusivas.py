"""Tiendas exclusivas por marca para posicionamiento orgánico: cada marca es un sitio aparte, con su
propio dominio (build.py las deja en sitios/<marca>/).

Cada tienda tiene su propio diseño (colores, letra y formas), solo muestra filtros de su marca y solo
enlaza a sus propias páginas. Usa el mismo carrito, los mismos precios y el mismo pago que la tienda.
Sin las palabras original ni compatible (Google Ads).
El negocio es distribuidor autorizado de cada marca: cada sitio lleva solo el logo de su marca (carpeta logos/);
el nombre del negocio sale de config.php y solo aparece donde la ley lo pide (pie, términos, recibos).

Páginas de cada marca:
  /                        portada
  /<filtro>/      una por filtro
  /cual-es-mi-filtro/      buscar por modelo de nevecón o referencia
  /cambio-e-instalacion/   cuándo cambiarlo y cómo instalar cada filtro
"""
import html
import json
import sys

import marcas_seo

import instalacion

esc = lambda s: html.escape(str(s), quote=True)
cop = lambda n: "$ " + f"{n:,}".replace(",", ".")
PREFIJO = "filtrosnevecones-"

FUENTES = "https://fonts.googleapis.com/css2?"
MARCAS_INFO = {
    "Samsung": {
        "tema": "#071338", "fuentes": FUENTES + "family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap",
        "intro": "Filtros de agua Samsung para nevecones de dos puertas, French door, Bespoke y Family Hub: HAF-CIN, HAF-QIN, Aqua-Pure Plus y el filtro externo de manguera.",
        "etiqueta": "El modelo está en una etiqueta dentro del refrigerador, en una pared lateral o en el techo. En los nevecones Samsung suele empezar por RF, RS o RH (por ejemplo, RF28HMEDBSR).",
        "aviso": "En los nevecones Samsung el indicador del filtro cambia de color o aparece «Filter» o «Replace Filter» en el panel o en la pantalla cuando ya toca cambiarlo.",
        "lineas": "French door, side by side, Bespoke y Family Hub",
        "externos": [('Samsung Colombia', 'https://www.samsung.com/co/', 'productos y soporte de la marca'), ('Superintendencia de Industria y Comercio', 'https://www.sic.gov.co/', 'derechos del consumidor en Colombia')],
    },
    "LG": {
        "tema": "#a50034", "fuentes": FUENTES + "family=Outfit:wght@400;500;600;700;800&display=swap",
        "intro": "Filtros de agua LG para nevecones French door y de dos puertas: LT1000P, LT700P, LT800P, LT500P, LT600P y el filtro externo de manguera.",
        "etiqueta": "El modelo está en una etiqueta dentro del refrigerador, en la pared lateral o detrás del cajón de las verduras. En los nevecones LG suele empezar por LF, LM, LR, LS o GR.",
        "aviso": "En los nevecones LG se prende la luz «Replace Filter» o «Filter» en el panel cuando ya toca cambiarlo.",
        "lineas": "French door, side by side e InstaView",
        "externos": [('LG Colombia', 'https://www.lg.com/co/', 'productos y soporte de la marca'), ('Superintendencia de Industria y Comercio', 'https://www.sic.gov.co/', 'derechos del consumidor en Colombia')],
    },
    "Whirlpool": {
        "tema": "#17181b", "fuentes": FUENTES + "family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=DM+Sans:wght@400;500;600;700;800&display=swap",
        "intro": "Filtros de agua Whirlpool EveryDrop del 1 al 5 y el filtro externo de manguera, para nevecones Whirlpool, Maytag, KitchenAid, Jenn-Air y Amana.",
        "etiqueta": "El modelo está en una etiqueta dentro del refrigerador, en la pared lateral de arriba. En los nevecones Whirlpool suele empezar por WRF, WRS o WRX; en Maytag por MFI o MSS y en KitchenAid por KRF.",
        "aviso": "En los nevecones Whirlpool la luz del filtro pasa a «Order» (pide el filtro) y luego a «Replace» (cámbialo ya).",
        "lineas": "French door, side by side y de congelador abajo",
        "externos": [('Whirlpool Colombia', 'https://www.whirlpool.com.co/', 'productos y soporte de la marca'), ('EveryDrop', 'https://www.everydropwater.com/', 'los filtros de agua EveryDrop'), ('Superintendencia de Industria y Comercio', 'https://www.sic.gov.co/', 'derechos del consumidor en Colombia')],
    },
    "GE": {
        "tema": "#0f3d7a", "fuentes": FUENTES + "family=Lexend:wght@400;500;600;700;800&display=swap",
        "intro": "Filtros de agua GE MWF y XWF para nevecones GE, GE Profile y Café de dos puertas y French door.",
        "etiqueta": "El modelo está en una etiqueta dentro del refrigerador, en la pared lateral o en el techo. En los nevecones GE suele empezar por GFE, GNE, GSS, PFE, PYE o CFE.",
        "aviso": "En los nevecones GE se prende la luz «Replace Filter» o «Reset Water Filter» en el panel cuando ya toca cambiarlo.",
        "lineas": "French door y side by side",
        "externos": [('GE Appliances', 'https://www.geappliances.com/', 'electrodomésticos GE'), ('Superintendencia de Industria y Comercio', 'https://www.sic.gov.co/', 'derechos del consumidor en Colombia')],
    },
}


def generar_marca(marca, dir_, base, CATALOGO, slug, norm, ubic, foto, php_str, CIUDADES_CO, logo=None):
    """Escribe la tienda de una marca en dir_, con sus páginas colgando de base ("/" en su propio dominio).
    Devuelve las rutas para el mapa del sitio y los datos de la marca para el encabezado."""
    info = MARCAS_INFO[marca]
    ps = [p for p in CATALOGO if p["marca"] == marca]
    s = slug(marca)
    for p in ps:
        p["slug_o"] = p["slug"]
    M = {"nombre": marca, "clase": s, "base": base, "tema": info["tema"], "fuentes": info["fuentes"], "tienda": f"Filtros {marca}", **(logo or {}),
         "productos": [[p["nombre_largo"] + "", p["slug_o"]] for p in ps]}
    R = marcas_seo.rutas(marca, ps, base, slug, norm, ubic, CIUDADES_CO)
    _rutas = [p["slug_o"] + "/" for p in ps] + [r for r, _ in R["temas"]] + [v[2] for v in R["refs"].values()] + [v[2] for v in R["modelos"].values()]
    _dup = {x for x in _rutas if _rutas.count(x) > 1}
    assert not _dup, f"rutas repetidas en {marca}: {_dup}"
    M["guias"] = [[r, n] for r, n in R["temas"]]
    M["ciudades"] = [[n, r] for n, (_, r) in list(R["ciudades"].items())[:14]]
    M["hub"] = R["hub"]
    if R.get("extra"):
        X = R["extra"]
        M["compat"] = [[n, X["familia"][n][0][0]] for n in X["familia"]] + [["Kenmore", X["kenmore"][0][0]], ["Todas las marcas", X["hub"]]]
        M["extra"] = [["Preguntas frecuentes", X["faq"]], ["Blog", X["blog"]]]
    M["externos"] = [[n, u] for n, u, _ in info.get("externos", [])]
    ctx = dict(marca=marca, info=info, ps=ps, base=base, M=M, slug=slug, norm=norm, ubic=ubic, foto=foto, php_str=php_str, ciudades=[c[0] for c in CIUDADES_CO[:30]], R=R, datos=instalacion.datos)
    rutas = [base]
    escribir(dir_ / "index.php", portada(**ctx))
    for p in ps:
        escribir(dir_ / p["slug_o"] / "index.php", producto(p, **ctx)); rutas.append(base + p["slug_o"] + "/")
    escribir(dir_ / "cual-es-mi-filtro" / "index.php", cual(**ctx)); rutas.append(base + "cual-es-mi-filtro/")
    escribir(dir_ / "cambio-e-instalacion" / "index.php", guia(**ctx)); rutas.append(base + "cambio-e-instalacion/")
    rutas += marcas_seo.generar(R, escribir, dir_, ctx, sys.modules[__name__])
    return rutas, M


def escribir(f, texto):
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(texto, encoding="utf-8")


# ---------- piezas comunes ----------
def inicio(M, php_str, titulo, desc, ruta, ld, extra_php="", extra_head=""):
    """Comienzo de la página: datos de la marca, datos estructurados y encabezado propio."""
    return (f"<?php require __DIR__ . '/{'../' * len([x for x in ruta.split('/') if x])}filtrosnevecones-marcas.php';\n"
            f"$M = json_decode(<<<'JSON'\n{json.dumps(M, ensure_ascii=False)}\nJSON, true);\n"
            f"$ld = json_decode(<<<'JSON'\n{json.dumps(ld, ensure_ascii=False)}\nJSON, true);\n{extra_php}"
            "foreach ($ld['@graph'] ?? [] as $i => $g) if (($g['sameAs'] ?? null) === '__REDES__') { $r = array_values(array_filter((array) (cfg()['redes'] ?? []))); if ($r) $ld['@graph'][$i]['sameAs'] = $r; else unset($ld['@graph'][$i]['sameAs']); }\n"
            "$tel = preg_replace('/\\D/', '', (string) (cfg()['whatsapp'] ?? ''));\n"
            "$json = str_replace(['__BASE__', '__NOMBRE__', '__TEL__'], [sitio()['base'], addslashes(cfg()['negocio']['nombre']), $tel ? '+57' . substr($tel, -10) : ''], json_encode($ld, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_HEX_TAG));\n"
            f"cabeza_marca($M, {php_str(titulo)}, {php_str(desc)}, {php_str(ruta)}, str_replace('__BASE__', sitio()['base'], {php_str(extra_head)}) . '<script type=\"application/ld+json\">' . $json . '</script>'); ?>\n")


def miga(items):
    h = '<nav class="m-miga">' + " › ".join(f'<a href="{r}">{esc(n)}</a>' if r else esc(n) for n, r in items) + "</nav>"
    ld = {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, **({"item": f"__BASE__{r}"} if r else {})} for i, (n, r) in enumerate(items)]}
    return h, ld


def faq(preguntas):
    h = "".join(f'<details class="m-faq"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in preguntas)
    ld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in preguntas]}
    return h, ld


def tarjeta(p, base, foto, ubic):
    return (f'<article class="m-card"><span class="m-badge">✔ Autorizado</span><span class="m-tipo">{"Externo" if ubic(p) == "externo" else "Interno"}</span>'
            f'<span class="im">{foto(p, p["nombre_largo"] + "", mini=True)}</span>'
            f'<div class="tx"><h3><a href="{base}{p["slug_o"]}/">{esc(p["nombre_largo"])}</a></h3><span class="ref">Referencia {esc(p["ref"])}</span>'
            f'<span class="pr">{cop(p["precio"])}<small>Envío gratis</small></span>'
            f'<button class="m-btn block" type="button" data-add="{p["id"]}">Agregar al carrito</button></div></article>')


def caja(p, base, foto):
    """Bloque de compra de un filtro dentro de una subpágina."""
    ahorro = p["precio"] * 2 - p["pack"]
    return (f'<div class="m-caja-prod"><a class="foto" href="{base}{p["slug_o"]}/"><span class="m-badge">✔ Autorizado</span>{foto(p, p["nombre_largo"] + "", mini=True)}</a>'
            f'<div class="tx"><h2><a href="{base}{p["slug_o"]}/">{esc(p["nombre_largo"])}</a></h2><span class="m-mut">Referencia {esc(p["ref"])}</span>'
            f'<span class="precio">{cop(p["precio"])}<small>Envío gratis a toda Colombia</small></span>'
            f'<div class="compra"><button class="m-btn" type="button" data-add="{p["id"]}">Agregar al carrito</button><button class="m-btn sec" type="button" data-add="{p["id"]}" data-ir="1">Comprar ahora</button></div>'
            f'<button class="m-link" type="button" data-add="{p["id"]}" data-pack="1">+ Pack de 2 por {cop(p["pack"])} (ahorras {cop(ahorro)})</button></div></div>')


def enlace(mapa, clave, texto):
    """Texto enlazado a su subpágina si existe (mapa: clave → (nombre, filtro, ruta))."""
    return f'<a href="{mapa[clave][2]}">{texto}</a>' if clave in mapa else texto


def producto_ld(p, ruta, nombre, marca):
    return {"@type": "Product", "name": nombre, "image": f"__BASE__/img/{p['id']}.jpg", "sku": p["ref"], "mpn": p["ref"], "brand": {"@type": "Brand", "name": marca},
            "offers": {"@type": "Offer", "url": f"__BASE__{ruta}", "priceCurrency": "COP", "price": str(p["precio"]), "itemCondition": "https://schema.org/NewCondition",
                       "availability": "https://schema.org/InStock" if p.get("stock") else "https://schema.org/BackOrder"}}


def verificar(marca):
    return [("📦", "Empaque de fábrica sellado", f"Llega en su caja {marca}, sellada, con la referencia y el código de barras impresos."),
            ("🔎", "Referencia impresa en el filtro", "El número de referencia viene grabado en el filtro: compáralo con el de tu filtro viejo."),
            ("📸", "Fotos reales antes de comprar", "¿Quieres verlo primero? Pídenos por WhatsApp fotos del filtro y su caja, sin compromiso."),
            ("🔒", "Pago seguro y número de guía", "Pagas en una página de pago segura, recibes el comprobante en tu correo y te enviamos la guía del envío.")]


def preguntas_marca(marca, ps):
    refs = ", ".join(p["ref"] if norm_ok(p) else p["nombre_largo"] for p in ps)
    return [
        (f"¿Quién vende estos filtros {marca}?", f"Somos distribuidor autorizado {marca} en Colombia: todos los filtros son de fábrica, nuevos y en su empaque sellado. Si quieres, antes de pagar te mandamos fotos reales por WhatsApp."),
        (f"¿Qué filtro {marca} necesito?", f"Busca la referencia impresa en tu filtro viejo o el modelo de tu nevecón en la etiqueta de adentro y compáralo en la página «¿Cuál es el mío?». Si tienes dudas, mándanos una foto por WhatsApp. Referencias disponibles: {refs}."),
        ("¿Cuánto cuesta el envío?", "Nada. El envío es gratis a toda Colombia y llega en 2 a 3 días hábiles a las principales ciudades; a otros municipios puede tardar un poco más."),
        ("¿Cómo pago?", "En línea, en una página de pago segura: tarjeta débito o crédito, PSE, Nequi o botón Bancolombia. El pedido se despacha cuando se confirma el pago."),
        (f"¿Cada cuánto se cambia el filtro {marca}?", "Cada 6 meses, o antes si el agua cambia de sabor, de olor o sale con poca presión. Con el pack de 2 filtros tienes el año completo y ahorras."),
        ("¿Y si me equivoco de filtro?", "Tienes 5 días hábiles para retractarte con el filtro sin instalar y en su empaque. Por eso te recomendamos confirmar por WhatsApp antes de comprar."),
    ]


def norm_ok(p):
    return p["ref"].upper() in p["nombre_largo"].upper()


def confianza(marca):
    items = [("✔", "Distribuidor autorizado", f"Filtros {marca}"), ("🚚", "Envío gratis", "A toda Colombia"), ("🔒", "Pago seguro", "Tarjeta, PSE o Nequi"), ("💬", "Asesoría", "Te ayudamos por WhatsApp")]
    return '<section class="m-confianza"><div class="m-wrap">' + "".join(f'<div><span class="ic">{i}</span><span><b>{esc(t)}</b><small>{esc(d)}</small></span></div>' for i, t, d in items) + "</div></section>"


def cta_wa(marca):
    return (f'<div class="m-cta"><div><h2>¿No sabes cuál es tu filtro {esc(marca)}?</h2><p>Mándanos una foto del filtro viejo o de la etiqueta del nevecón y te decimos cuál es.</p></div>'
            f'<a class="m-btn" data-wa-marca href="#" target="_blank" rel="noopener">💬 Escríbenos por WhatsApp</a></div>'
            "<?php $w = preg_replace('/\\D/', '', (string) (cfg()['whatsapp'] ?? '')); if ($w !== ''): ?><script>document.querySelectorAll('[data-wa-marca]').forEach(a => a.href = 'https://wa.me/57<?= substr($w, -10) ?>?text=' + encodeURIComponent("
            f"{json.dumps('Hola, quiero saber cuál filtro ' + marca + ' le sirve a mi nevecón.', ensure_ascii=False)}));</script><?php endif; ?>")


def sec(cuerpo, alt=False, id_=""):
    return f'<section class="m-sec{" alt" if alt else ""}"{f" id={chr(34)}{id_}{chr(34)}" if id_ else ""}><div class="m-wrap">{cuerpo}</div></section>'


def cab(eyebrow, titulo, texto="", h="h2"):
    return f'<div class="m-cab"><span class="eyebrow">{esc(eyebrow)}</span><{h}>{esc(titulo)}</{h}>{f"<p>{texto}</p>" if texto else ""}</div>'


# ---------- portada de la marca ----------
def portada(marca, info, ps, base, M, slug, norm, ubic, foto, php_str, ciudades, R=None, datos=None):
    destacados = sorted(ps, key=lambda p: ubic(p) == "externo")[:3]
    preg = preguntas_marca(marca, ps)
    faq_h, faq_ld = faq(preg)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": f"Filtros de agua {marca}", "url": f"__BASE__{base}", "description": info["intro"], "inLanguage": "es-CO",
         "about": {"@type": "Brand", "name": marca},
         "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"__BASE__{base}{p['slug_o']}/", "name": p["nombre_largo"] + ""} for i, p in enumerate(ps)]}},
        faq_ld,
        {"@type": "OnlineStore", "@id": f"__BASE__{base}#tienda", "name": "__NOMBRE__", "alternateName": f"Filtros {marca} Colombia", "url": f"__BASE__{base}",
         "logo": f"__BASE__{M.get('logo', '')}", "description": f"Distribuidor autorizado de filtros de agua {marca} en Colombia.",
         "areaServed": {"@type": "Country", "name": "Colombia"}, "currenciesAccepted": "COP", "paymentAccepted": "Tarjeta de crédito, tarjeta débito, PSE, Nequi",
         "contactPoint": {"@type": "ContactPoint", "telephone": "__TEL__", "contactType": "customer service", "areaServed": "CO", "availableLanguage": "es"}, "sameAs": "__REDES__"},
        {"@type": "WebSite", "name": f"Filtros {marca}", "url": f"__BASE__{base}", "inLanguage": "es-CO", "publisher": {"@id": f"__BASE__{base}#tienda"}}]}
    titulo = f"Filtros de agua {marca} para nevera | Envío gratis"
    desc = f"{info['intro']} Envío gratis a toda Colombia y pago seguro con tarjeta, PSE o Nequi."
    fotos = "".join(f'<span class="f f{i + 1}">{foto(p, p["nombre_largo"] + "", lazy=False)}</span>' for i, p in enumerate(destacados))
    pasos = [("Encuentra tu filtro", f"Por la referencia del filtro viejo o el modelo de tu nevecón {marca}."), ("Paga en línea", "Con tarjeta, PSE o Nequi en página segura."), ("Recíbelo en casa", "Envío gratis a toda Colombia con número de guía.")]
    senales = ["El agua o el hielo saben o huelen raro (a cloro, a tierra o a encerrado).", "El dispensador bota menos agua o sale con poca presión.", "El hielo sale turbio, pequeño o la máquina de hielo produce menos.", "Ya pasaron 6 meses desde el último cambio."]
    return inicio(M, php_str, titulo, desc, base, ld) + f"""
<section class="m-hero"><div class="m-wrap">
  <div>
    <span class="m-hero-logo"><?= logo_marca_html($M) ?><span><b>Distribuidor autorizado</b>Filtros en Colombia</span></span>
    <h1>Filtros de agua {esc(marca)} para tu nevecón</h1>
    <p class="lead">{esc(info["intro"])}</p>
    <div class="acc"><a class="m-btn" href="#filtros">Ver los filtros {esc(marca)}</a><a class="m-btn sec" href="{base}cual-es-mi-filtro/">¿Cuál es el mío?</a></div>
    <ul><li>100 %</li><li>Empaque sellado</li><li>Envío gratis</li><li>Pago seguro</li></ul>
  </div>
  <div class="m-fotos">{fotos}<span class="sello-o"><span><b>Distribuidor</b>autorizado<br>{esc(marca)}</span></span></div>
</div></section>
{confianza(marca)}
{sec(cab("Catálogo " + marca, f"Filtros {marca}", f"{len(ps)} referencias {esc(marca)}, nuevas y en su empaque. Todas con envío gratis a toda Colombia.") + '<div class="m-grid">' + "".join(tarjeta(p, base, foto, ubic) for p in ps) + "</div>", id_="filtros")}
{sec(cab("Compra con confianza", f"¿Qué recibo con mi filtro {marca}?", "Esto es lo que recibes y lo que puedes revisar tú mismo.") + '<div class="m-cols">' + "".join(f'<div class="m-bloque"><div class="ic">{i}</div><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for i, t, d in verificar(marca)) + "</div>", alt=True)}
{sec(cab("Encuentra el tuyo", f"¿Cuál filtro {marca} le sirve a mi nevecón?", esc(info["etiqueta"])) + '<div class="m-chips">' + "".join(f'<a href="{base}{p["slug_o"]}/">{esc(p["ref"])} <small>· {esc(p["nombre_largo"])}</small></a>' for p in ps) + f'</div><p style="margin-top:18px"><a class="m-btn sec" href="{base}cual-es-mi-filtro/">Buscar por modelo de nevecón {esc(marca)}</a></p>')}
{sec(cab("Mantenimiento", f"¿Cuándo cambiar el filtro de tu nevecón {marca}?", esc(info["aviso"])) + '<ul class="m-ok">' + "".join(f"<li>{esc(x)}</li>" for x in senales) + f'</ul><p style="margin-top:18px"><a href="{base}cambio-e-instalacion/">Cómo instalar cada filtro {esc(marca)}, paso a paso →</a></p>', alt=True)}
{sec(cab("Así de fácil", "Compra en 3 pasos") + '<div class="m-cols m-num">' + "".join(f'<div class="m-bloque"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t, d in pasos) + "</div>")}
{sec(cab("Resolvemos tus dudas", f"Preguntas frecuentes sobre filtros {marca}") + faq_h, alt=True, id_="preguntas")}
{sec(cab("Envíos", f"Enviamos filtros {marca} a toda Colombia", "Envío gratis con número de guía. Llega en 2 a 3 días hábiles a las principales ciudades.") + '<div class="m-chips">' + "".join(f'<a href="{r}">{esc(n)}</a>' for n, (_, r) in list(R["ciudades"].items())[:40]) + f'<a href="{R["hub"]}"><b>Ver las {len(R["ciudades"])} ciudades →</b></a></div>')}
{sec(cab("Para consultar", f"Fuentes oficiales sobre filtros y nevecones {marca}", "Sitios de la marca y de la autoridad de consumo en Colombia.") + '<div class="m-cols">' + "".join(f'<a class="m-bloque m-guia" href="{esc(u)}" target="_blank" rel="noopener"><h3>{esc(n)} ↗</h3><p>{esc(d[0].upper() + d[1:])}.</p></a>' for n, u, d in info.get("externos", [])) + "</div>")}
{sec(cab("Guías " + marca, f"Lo que más buscan sobre filtros {marca}") + '<div class="m-cols">' + "".join(f'<a class="m-bloque m-guia" href="{r}"><h3>{esc(n)}</h3><p>Leer →</p></a>' for r, n in R["temas"]) + "</div>", alt=True)}
{sec(cta_wa(marca))}
</main>
<?php pie_marca($M); ?>
"""


# ---------- página de cada filtro ----------
def producto(p, marca, info, ps, base, M, slug, norm, ubic, foto, php_str, ciudades, R=None, datos=None):
    url = f"{base}{p['slug_o']}/"
    nombre = p["nombre_largo"] + ""
    alias = [r for r in p["refs"] if norm(r) != norm(p["ref"])]
    otros = [x for x in ps if x["id"] != p["id"]]
    externo = ubic(p) == "externo"
    ahorro = p["precio"] * 2 - p["pack"]
    d = instalacion.datos(p)
    miga_h, miga_ld = miga([(f"Filtros {marca}", base), (p["nombre_largo"], None)])
    preg = [
        (f"¿Quién vende el {p['nombre_largo']}?", f"Sí. Somos distribuidor autorizado {marca} y es el filtro de fábrica, referencia {p['ref']}, nuevo y en su empaque sellado."),
        (f"¿Qué otras referencias reemplaza el {p['ref']}?", ("También aparece como " + ", ".join(alias) + ".") if alias else f"Búscalo por la referencia {p['ref']} impresa en tu filtro viejo."),
        ("¿Cada cuánto se cambia?", "Cada 6 meses, o antes si el agua cambia de sabor, de olor o sale con poca presión."),
        ("¿Cuánto tarda en llegar?", "El envío es gratis y llega en 2 a 3 días hábiles a las principales ciudades de Colombia."),
    ]
    faq_h, faq_ld = faq(preg)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Product", "name": nombre, "image": f"__BASE__/img/{p['id']}.jpg", "sku": p["ref"], "mpn": p["ref"], "brand": {"@type": "Brand", "name": marca},
         "description": f"Filtro de agua {marca}, referencia {p['ref']}. {p.get('desc') or ''}".strip(),
         "offers": {"@type": "Offer", "url": f"__BASE__{url}", "priceCurrency": "COP", "price": str(p["precio"]),
                    "availability": "https://schema.org/InStock" if p.get("stock") else "https://schema.org/BackOrder", "itemCondition": "https://schema.org/NewCondition",
                    "shippingDetails": {"@type": "OfferShippingDetails", "shippingRate": {"@type": "MonetaryAmount", "value": "0", "currency": "COP"},
                                        "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "CO"},
                                        "deliveryTime": {"@type": "ShippingDeliveryTime", "handlingTime": {"@type": "QuantitativeValue", "minValue": 0, "maxValue": 1, "unitCode": "DAY"},
                                                         "transitTime": {"@type": "QuantitativeValue", "minValue": 1, "maxValue": 3, "unitCode": "DAY"}}},
                    "hasMerchantReturnPolicy": {"@type": "MerchantReturnPolicy", "applicableCountry": "CO", "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
                                                "merchantReturnDays": 5, "returnMethod": "https://schema.org/ReturnByMail", "returnFees": "https://schema.org/ReturnFeesCustomerResponsibility"}}},
        miga_ld, faq_ld, instalacion.tutorial_ld(p, f"__BASE__{url}", p["nombre_largo"])]}
    resenas_php = (f"$R = resenas({php_str(p['id'])});\n"
                   "if ($R['n']) {\n"
                   "    $ld['@graph'][0]['aggregateRating'] = ['@type' => 'AggregateRating', 'ratingValue' => $R['prom'], 'reviewCount' => $R['n'], 'bestRating' => 5, 'worstRating' => 1];\n"
                   "    $ld['@graph'][0]['review'] = array_map(fn($r) => ['@type' => 'Review', 'author' => ['@type' => 'Person', 'name' => $r['nombre']], 'datePublished' => substr($r['creado'], 0, 10),\n"
                   "        'reviewRating' => ['@type' => 'Rating', 'ratingValue' => (int) $r['estrellas'], 'bestRating' => 5], 'reviewBody' => $r['texto']], array_slice($R['lista'], 0, 5));\n"
                   "}\n")
    head = f'<link rel="preload" as="image" href="/img/{p["id"]}.webp"><meta property="og:image" content="__BASE__/img/{p["id"]}.jpg">'
    titulo = f"{nombre} | Envío gratis Colombia" if len(nombre) < 40 else nombre
    desc = (f"Compra el {nombre} a {cop(p['precio'])}: nuevo, en empaque sellado y con envío gratis a toda Colombia en 2 a 3 días hábiles."
            + (f" Reemplaza {', '.join(alias[:3])}." if alias else "") + " Paga con tarjeta, PSE o Nequi.")
    ficha = [("Marca", marca), ("Referencia", p["ref"]), ("Condición", "Nuevo, en empaque sellado de fábrica"), ("Tipo", "Externo, va en la manguera" if externo else "Interno, va dentro del nevecón"),
             ("Dónde va", d["donde"]), ("Instalación", d["tiempo"] + " · " + d["herramientas"]), ("Duración", "6 meses de uso normal"),
             ("Precio", f"{cop(p['precio'])} (pack de 2: {cop(p['pack'])})"), ("Envío", "Gratis a toda Colombia, 2 a 3 días hábiles en las principales ciudades")]
    if alias:
        ficha.insert(2, ("También aparece como", ", ".join(alias)))
    return inicio(M, php_str, titulo, desc, url, ld, resenas_php, head) + f"""<div class="m-wrap">
{miga_h}
<div class="m-prod">
  <div class="foto"><span class="m-badge">✔ {esc(marca)}</span>{foto(p, nombre, lazy=False)}</div>
  <div class="info">
    <span class="m-prod-logo"><?= logo_marca_html($M) ?><small>Distribuidor autorizado</small></span>
    <h1>{esc(nombre)}</h1>
    <span class="sub">Filtro de agua {esc(marca)} · {"Externo" if externo else "Interno"} · Referencia <b>{esc(p["ref"])}</b></span>
    <?php if ($R['n']) echo '<a href="#opiniones" style="text-decoration:none;color:inherit">' . estrellas_html($R['prom']) . ' <b>' . $R['prom'] . '</b> <span class="m-mut">(' . $R['n'] . ($R['n'] === 1 ? ' opinión' : ' opiniones') . ')</span></a>'; ?>
    <span class="precio">{cop(p["precio"])}<small>Envío gratis a toda Colombia</small></span>
    <div class="m-aviso"><span style="font-size:22px">✔</span><span><b>Filtro {esc(marca)} · {esc(p["ref"])}</b>Somos distribuidor autorizado {esc(marca)}. Nuevo, en su caja sellada de fábrica con la referencia {esc(p["ref"])} impresa. ¿Quieres verlo? Te mandamos fotos reales por WhatsApp.</span></div>
    <div class="compra"><button class="m-btn block" type="button" data-add="{p["id"]}">Agregar al carrito</button><button class="m-btn sec block" type="button" data-add="{p["id"]}" data-ir="1">Comprar ahora</button><button class="m-link" type="button" data-add="{p["id"]}" data-pack="1">+ Pack anual de 2 por {cop(p["pack"])} (ahorras {cop(ahorro)})</button></div>
    <ul class="m-ok"><li><b>Envío gratis</b>: llega en 2 a 3 días hábiles a las principales ciudades.</li><li><b>Fácil de instalar</b>: {"10 a 15 minutos en la manguera del agua" if externo else "2 minutos, sin herramientas"}. Paso a paso abajo.</li><li><b>Pago seguro</b> en línea; el comprobante llega a tu correo.</li></ul>
    <span class="m-mut" style="font-size:14px">Paga con tarjeta débito o crédito, PSE, Nequi o botón Bancolombia.</span><?= medios_pago_html() ?>
  </div>
</div>
</div>
{sec('<div class="m-texto">' + cab("Descripción", f"Filtro de agua {marca} {p['ref']}") + f'<p>{esc(p.get("desc") or ("Filtro de agua para nevecones " + marca + "."))}</p><p>Retiene el cloro, el sedimento y las partículas que le dan mal sabor y mal olor al agua y al hielo, y protege la válvula y la máquina de hielo de tu nevecón {esc(marca)}. Con la referencia correcta encaja exacto, no gotea y el nevecón lo reconoce sin problema. Rinde unos 6 meses de uso normal.</p>' + (f'<p>Si tu filtro viejo dice <b>{esc(p["ref"])}</b> o alguna de estas referencias, este es el tuyo:</p><div class="m-chips">' + "".join(f'<a href="{R["refs"][norm(r)][2]}">{esc(r)}</a>' if norm(r) in R["refs"] else f"<span>{esc(r)}</span>" for r in alias) + "</div>" if alias else f'<p>Si tu filtro viejo dice <b>{esc(p["ref"])}</b>, este es el tuyo.</p>') + (f'<p>{esc(p["nota"])}</p>' if p.get("nota") else "") + "</div>", alt=True)}
{sec(cab("Ficha técnica", f"Datos del {p['nombre_largo']}") + '<dl class="m-ficha">' + "".join(f"<dt>{esc(a)}</dt><dd>{esc(b)}</dd>" for a, b in ficha) + "</dl>")}
{sec(cab("Nevecones", f"Nevecones {marca} que usan este filtro", esc(info["etiqueta"])) + ('<div class="m-chips">' + "".join(f'<a href="{R["modelos"][norm(m)][2]}">{esc(m)}</a>' for m in p["modelos"]) + "</div><p class=\"m-mut\" style=\"margin-top:12px\">Y otros modelos. Si el tuyo no aparece, compara la referencia del filtro viejo o escríbenos.</p>" if p["modelos"] else '<p>Compara la referencia impresa en tu filtro viejo o escríbenos por WhatsApp con el modelo de tu nevecón.</p>'), alt=True)}
{sec(instalacion.tutorial_html(p, p["nombre_largo"]))}
{sec(cab("Compra con confianza", "Qué revisar al recibirlo") + '<div class="m-cols">' + "".join(f'<div class="m-bloque"><div class="ic">{i}</div><h3>{esc(t)}</h3><p>{esc(dd)}</p></div>' for i, t, dd in verificar(marca)) + "</div>", alt=True)}
<section class="m-sec" id="opiniones"><div class="m-wrap">{cab("Opiniones", "Lo que dicen los compradores")}
<?php if ($R['n']): ?><p><?= estrellas_html($R['prom']) ?> <b><?= $R['prom'] ?> de 5</b> · <?= $R['n'] ?> <?= $R['n'] === 1 ? 'opinión' : 'opiniones' ?> de compradores reales</p>
<?php foreach ($R['lista'] as $r): ?><div class="resena"><?= estrellas_html((float) $r['estrellas']) ?> <b><?= h($r['nombre']) ?></b> <span class="m-mut">· <?= h($r['ciudad']) ?> · <?= h(date('d/m/Y', strtotime($r['creado']))) ?></span><?= $r['texto'] !== '' ? '<p style="margin:4px 0 0">' . h($r['texto']) . '</p>' : '' ?></div><?php endforeach; ?>
<?php else: ?><p class="m-mut">Todavía no hay opiniones de este filtro. Después de tu compra te pediremos la tuya por correo.</p><?php endif; ?>
</div></section>
{sec(cab("Preguntas", f"Preguntas sobre el {p['nombre_largo']}") + faq_h, alt=True)}
{sec(cab("Más de " + marca, f"Otros filtros {marca}") + '<div class="m-grid">' + "".join(tarjeta(x, base, foto, ubic) for x in otros) + "</div>") if otros else ""}
{sec(marcas_seo.relacionadas(R, url, marca, M, base), alt=True)}
{sec(cta_wa(marca))}
<div class="m-barra"><span><small>{esc(nombre)}</small><b>{cop(p["precio"])}</b></span><button class="m-btn" type="button" data-add="{p["id"]}">Agregar al carrito</button></div>
</main>
<?php pie_marca($M); ?>
"""


# ---------- ¿cuál es mi filtro? ----------
def cual(marca, info, ps, base, M, slug, norm, ubic, foto, php_str, ciudades, R=None, datos=None):
    url = base + "cual-es-mi-filtro/"
    miga_h, miga_ld = miga([(f"Filtros {marca}", base), ("¿Cuál es mi filtro?", None)])
    filas_mod = "".join(f'<tr><td><a href="{R["modelos"][norm(m)][2]}"><b>{esc(m)}</b></a></td><td><a href="{base}{p["slug_o"]}/">{esc(p["nombre_largo"])}</a></td><td>{cop(p["precio"])}</td></tr>'
                        for p in ps for m in p["modelos"])
    filas_ref = "".join(f'<tr><td>{enlace(R["refs"], norm(r), f"<b>{esc(r)}</b>")}</td><td><a href="{base}{p["slug_o"]}/">{esc(p["nombre_largo"])}</a></td><td>{"Externo" if ubic(p) == "externo" else "Interno"}</td></tr>'
                        for p in ps for r in p["refs"])
    preg = [(f"¿Dónde está el modelo de mi nevecón {marca}?", info["etiqueta"]),
            (f"¿Dónde está la referencia del filtro {marca}?", "Impresa en el filtro viejo, en la etiqueta o grabada en el cuerpo. Sácalo y míralo con buena luz."),
            ("¿Y si no encuentro mi modelo?", "Mándanos por WhatsApp una foto de la etiqueta del nevecón o del filtro viejo y te decimos cuál es.")]
    faq_h, faq_ld = faq(preg)
    ld = {"@context": "https://schema.org", "@graph": [{"@type": "WebPage", "name": f"¿Cuál filtro {marca} es el mío?", "url": f"__BASE__{url}", "inLanguage": "es-CO"}, miga_ld, faq_ld]}
    titulo = f"¿Qué filtro {marca} usa mi nevecón? Busca por modelo o referencia"
    desc = f"Encuentra el filtro de agua {marca} de tu nevecón por el modelo o por la referencia del filtro viejo. Tabla de referencias y envío gratis a toda Colombia."
    return inicio(M, php_str, titulo, desc, url, ld) + f"""<div class="m-wrap">{miga_h}</div>
{sec(cab("Referencias " + marca, f"¿Qué filtro {marca} usa mi nevecón?", esc(info["etiqueta"]) + " También puedes buscar la referencia impresa en tu filtro viejo.", h="h1") + '<div class="m-cols">' + "".join(f'<div class="m-bloque"><div class="ic">{i}</div><h3>{esc(t)}</h3><p>{esc(dd)}</p></div>' for i, t, dd in [("🏷️", "1. Mira la etiqueta", info["etiqueta"]), ("🔎", "2. O mira el filtro viejo", "La referencia viene impresa en el filtro. Compárala con la tabla de abajo."), ("💬", "3. ¿Dudas? Escríbenos", "Mándanos una foto por WhatsApp y te confirmamos el filtro correcto.")]) + "</div>")}
{sec(cab("Por modelo", f"Modelos de nevecón {marca} y su filtro", "Escribe Ctrl+F (o «Buscar en la página» en el celular) y busca tu modelo.") + f'<div class="m-tabla-wrap"><table class="m-tabla"><thead><tr><th>Modelo de nevecón</th><th>Filtro</th><th>Precio</th></tr></thead><tbody>{filas_mod}</tbody></table></div>', alt=True) if filas_mod else ""}
{sec(cab("Por referencia", f"Referencias de filtros {marca} y su equivalente") + f'<div class="m-tabla-wrap"><table class="m-tabla"><thead><tr><th>Referencia en el filtro viejo</th><th>Filtro</th><th>Tipo</th></tr></thead><tbody>{filas_ref}</tbody></table></div>')}
{sec(cab("Catálogo", f"Todos los filtros {marca}") + '<div class="m-grid">' + "".join(tarjeta(p, base, foto, ubic) for p in ps) + "</div>", alt=True)}
{sec(cab("Preguntas", "Preguntas frecuentes") + faq_h)}
{sec(cta_wa(marca), alt=True)}
</main>
<?php pie_marca($M); ?>
"""


# ---------- cuándo cambiarlo y cómo instalarlo ----------
def guia(marca, info, ps, base, M, slug, norm, ubic, foto, php_str, ciudades, R=None, datos=None):
    url = base + "cambio-e-instalacion/"
    miga_h, miga_ld = miga([(f"Filtros {marca}", base), ("Cambio e instalación", None)])
    senales = [("👅", "Sabor u olor raro", "El agua o el hielo saben a cloro, a tierra o a encerrado."), ("💧", "Menos presión", "El dispensador bota menos agua o tarda más en llenar el vaso."),
               ("🧊", "Hielo turbio", "El hielo sale turbio, pequeño o la máquina produce menos."), ("📅", "Pasaron 6 meses", "Aunque todo se vea bien, el filtro ya está saturado.")]
    tutoriales = "".join(sec(instalacion.tutorial_html(p, p["nombre_largo"]).replace('id="instalacion"', f'id="{p["slug_o"]}"')
                             + f'<p style="margin-top:12px"><a class="m-btn sec" href="{base}{p["slug_o"]}/">Ver el {esc(p["nombre_largo"])} · {cop(p["precio"])}</a></p>', alt=i % 2 == 0)
                         for i, p in enumerate(ps))
    ld = {"@context": "https://schema.org", "@graph": [{"@type": "Article", "headline": f"Cuándo cambiar el filtro de agua del nevecón {marca} y cómo instalarlo", "url": f"__BASE__{url}", "inLanguage": "es-CO"}, miga_ld]}
    titulo = f"Cómo cambiar el filtro de agua del nevecón {marca}: paso a paso"
    desc = f"Cuándo cambiar el filtro de agua de tu nevecón {marca}, cómo instalar cada referencia y cómo reiniciar el aviso del filtro. Guía paso a paso."
    return inicio(M, php_str, titulo, desc, url, ld) + f"""<div class="m-wrap">{miga_h}</div>
{sec(cab("Guía " + marca, f"Cómo cambiar el filtro de agua de tu nevecón {marca}", esc(info["aviso"]) + " Abajo tienes el paso a paso de cada filtro.", h="h1") + '<div class="m-cols">' + "".join(f'<div class="m-bloque"><div class="ic">{i}</div><h3>{esc(t)}</h3><p>{esc(dd)}</p></div>' for i, t, dd in senales) + "</div>" + '<div class="m-chips" style="margin-top:24px">' + "".join(f'<a href="#{p["slug_o"]}">{esc(p["nombre_largo"])}</a>' for p in ps) + "</div>")}
{tutoriales}
{sec(cta_wa(marca))}
</main>
<?php pie_marca($M); ?>
"""
