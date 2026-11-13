"""Páginas de búsqueda de la tienda nacional de una marca: departamentos, regiones, áreas metropolitanas, ciudades de la A a la Z, glosario y mapa del sitio.
Cada una responde a una búsqueda real y enlaza a las páginas de ciudad, de modo que Google llega a todas por varios caminos."""
import html
import re
import unicodedata

import ads22_hubs

esc = lambda s: html.escape(str(s), quote=True)
cop = lambda v: "$ " + f"{int(v):,}".replace(",", ".")


def slug(n):
    n = unicodedata.normalize("NFKD", n).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", n).strip("-")


def generar(pagina, ctx, h, R, hechas):
    marca, ps, base, M = ctx["marca"], ctx["ps"], ctx["base"], ctx["M"]
    ms = slug(marca)
    ciudades = R["ciudades"]  # nombre -> ([nombre, depto, ...], ruta)
    por_depto = {}
    for nombre, (c, ruta) in ciudades.items():
        por_depto.setdefault(c[1], []).append((nombre, ruta))
    for v in por_depto.values():
        v.sort()
    precios = sorted(p["precio"] for p in ps)
    rango = f"{cop(precios[0])} a {cop(precios[-1])}"
    tarjetas = '<div class="m-grid">' + "".join(h.tarjeta(p, base, ctx["foto"], ctx["ubic"]) for p in ps) + "</div>"
    tabla = ('<div class="m-tabla-wrap"><table class="m-tabla"><thead><tr><th>Filtro</th><th>Código</th><th>Precio</th></tr></thead><tbody>'
             + "".join(f'<tr><td><a href="{base}{p["slug_o"]}/">{esc(p["nombre_largo"])}</a></td><td>{esc(p["ref"])}</td><td><b>{cop(p["precio"])}</b></td></tr>' for p in ps) + "</tbody></table></div>")
    pre_comun = [("¿Cómo pago?", "Solo en línea, en la pasarela segura de Wompi: tarjeta, PSE, Nequi o Bancolombia. Recibes la confirmación por correo."),
                 ("¿El envío tiene costo?", "No, el envío es gratis a toda Colombia.")]

    def cities_chips(lista):
        return '<div class="m-chips">' + "".join(f'<a href="{r}">{esc(n)}</a>' for n, r in lista) + "</div>"

    # ---------- departamentos ----------
    for dept, lista in sorted(por_depto.items()):
        ruta = f"{base}filtros-{ms}-{slug(dept)}/"
        n = len(lista)
        rk = ads22_hubs
        preg = [(f"¿Envían filtros {marca} a {dept}?", f"Sí, enviamos gratis a {n} {'ciudad' if n == 1 else 'ciudades'} de {dept} y a otros municipios del departamento."),
                (f"¿Cuánto cuesta el filtro {marca} en {dept}?", f"Entre {rango}, según la referencia, con envío gratis.")] + pre_comun
        pagina(ruta, f"Filtros {marca} en {dept}: envío y precios"[:62], f"Compra filtros de agua {marca} con envío gratis en {dept}: {n} {'ciudad' if n == 1 else 'ciudades'}, precios de {rango} y pago en línea.",
               f"Filtros de agua {marca} en {dept}", f"Cobertura · {dept}",
               f"Enviamos el filtro de tu nevecón {esc(marca)} a {n} {'ciudad' if n == 1 else 'ciudades'} de {esc(dept)}, con envío gratis y pago seguro en línea.",
               f'<h2 style="font-size:22px;margin:6px 0 12px">Ciudades de {esc(dept)} donde enviamos</h2>' + cities_chips(lista) + '<h2 style="font-size:22px;margin:26px 0 12px">Filtros disponibles</h2>' + tabla
               + f'<p class="m-mut" style="margin-top:14px">Mira <a href="{R["hub"]}">todas las ciudades</a> o escoge tu filtro con el <a href="{base}cual-es-mi-filtro/">buscador por modelo</a>.</p>', preg, miga_nombre=f"Filtros en {dept}")

    # ---------- regiones ----------
    regiones = {}
    for clave, (nombre_r, deptos, grandes) in ads22_hubs.REGIONES.items():
        presentes = [d for d in deptos if d in por_depto]
        if not presentes:
            continue
        ruta = f"{base}filtros-{ms}-region-{slug(clave)}/"
        regiones[clave] = ruta
        n_ciu = sum(len(por_depto[d]) for d in presentes)
        filas = "".join(f'<tr><td><a href="{base}filtros-{ms}-{slug(d)}/">{esc(d)}</a></td><td>{len(por_depto[d])}</td><td>{esc(", ".join(x.split(" (")[0] for x, _ in por_depto[d][:4]))}…</td></tr>' for d in presentes)
        preg = [(f"¿Envían filtros {marca} a la {nombre_r}?", f"Sí, enviamos gratis a {n_ciu} ciudades de la {nombre_r}, entre ellas {grandes}."),
                (f"¿Cuánto cuesta el filtro {marca} en la {nombre_r}?", f"Entre {rango}, con envío gratis.")] + pre_comun
        pagina(ruta, f"Filtro de agua {marca} en la {nombre_r}"[:62], f"Filtros de agua {marca} con envío gratis a {n_ciu} ciudades de la {nombre_r} ({len(presentes)} departamentos). Paga en línea con Wompi.",
               f"Filtros de agua {marca} en la {nombre_r}", f"Cobertura · {nombre_r}",
               f"Envío gratis a {n_ciu} ciudades de {len(presentes)} {'departamento' if len(presentes) == 1 else 'departamentos'}: {esc(grandes)} y más.",
               '<h2 style="font-size:22px;margin:6px 0 12px">Departamentos donde entregamos</h2><div class="m-tabla-wrap"><table class="m-tabla"><thead><tr><th>Departamento</th><th>Ciudades</th><th>Algunas</th></tr></thead><tbody>' + filas + "</tbody></table></div>"
               + '<h2 style="font-size:22px;margin:26px 0 12px">Filtros disponibles</h2>' + tarjetas, preg, miga_nombre=nombre_r)

    # ---------- áreas metropolitanas ----------
    for clave, (corto, largo, slugs) in ads22_hubs.AREAS.items():
        cs = [(n, r) for n, (c, r) in ciudades.items() if slug(n.split(" (")[0]) in slugs]
        if len(cs) < 3:
            continue
        ruta = f"{base}filtro-nevera-{ms}-{clave}/"
        lista = ", ".join(n.split(" (")[0] for n, _ in cs)
        preg = [(f"¿Entregan filtros {marca} en {largo}?", f"Sí, enviamos gratis a {lista}."), (f"¿Cuánto cuesta el filtro {marca} en {corto}?", f"Entre {rango}, con envío gratis.")] + pre_comun
        pagina(ruta, f"Filtro de agua {marca} en {corto}: envío gratis"[:62], f"Filtros de agua {marca} en {largo}: {lista}. Envío gratis y pago en línea.",
               f"Filtro de agua {marca} en {largo}", f"Cobertura · {corto}", f"Envío gratis a {len(cs)} municipios, con pago seguro en línea.",
               f'<h2 style="font-size:22px;margin:6px 0 12px">Municipios de {esc(corto)} con envío</h2>' + cities_chips(cs) + '<h2 style="font-size:22px;margin:26px 0 12px">Escoge tu filtro</h2>' + tarjetas, preg, miga_nombre=corto)

    # ---------- A–Z ----------
    por_letra = {}
    for nombre, (c, ruta) in sorted(ciudades.items(), key=lambda x: slug(x[0])):
        por_letra.setdefault(slug(nombre)[0].upper(), []).append((nombre, ruta, c[1]))
    letras = "".join(f'<a href="#letra-{l}">{l}</a>' for l in sorted(por_letra))
    cuerpo = "".join(f'<h3 id="letra-{l}" style="margin:22px 0 8px">{l}</h3><div class="m-chips">' + "".join(f'<a href="{r}" title="{esc(d)}">{esc(n)}</a>' for n, r, d in v) + "</div>" for l, v in sorted(por_letra.items()))
    pagina(f"{base}ciudades-con-filtros-{ms}-a-z/", f"Filtros {marca} por ciudad de la A a la Z", f"Lista alfabética de las {len(ciudades)} ciudades y municipios donde enviamos filtros de agua {marca} con envío gratis.",
           f"Filtros {marca} en {len(ciudades)} ciudades, de la A a la Z", "Cobertura · A–Z", "Busca tu ciudad por su inicial y entra a su página con tiempo de entrega y precios.",
           '<div class="m-chips" style="margin-bottom:16px">' + letras + "</div>" + cuerpo, [], miga_nombre="Ciudades de la A a la Z")

    # ---------- glosario ----------
    terminos = [(f"{p['nombre_largo']}", f"Filtro {marca} de código {p['ref']}. Equivale a {', '.join(p['refs'][:5])}." + (f" Usado en nevecones como {', '.join(p['modelos'][:4])}." if p["modelos"] else "")) for p in ps]
    terminos += [("Referencia o código", "Número impreso en el filtro que identifica la pieza exacta. Es la forma más segura de pedir el filtro correcto."),
                 ("Equivalencia", "Una misma pieza puede aparecer con varios códigos. Todos los códigos equivalentes corresponden al mismo filtro."),
                 ("Nevecón", "Forma colombiana de llamar a un refrigerador grande de dos puertas con dispensador de agua y hielo."),
                 ("French door", "Nevecón con dos puertas de refrigerador arriba y un cajón de congelador abajo."),
                 ("Side by side", "Nevecón con refrigerador y congelador lado a lado, cada uno con su puerta vertical."),
                 ("Luz o aviso del filtro", "Indicador del panel que se enciende cuando toca cambiar el filtro; se reinicia después de instalar el nuevo."),
                 ("Purga", "Dejar correr unos 6 litros de agua por el dispensador tras el cambio para sacar el aire del filtro nuevo."),
                 ("Retracto", "Derecho a devolver el producto sin usar dentro de 5 días hábiles desde la entrega.")]
    pagina(f"{base}glosario-filtro-nevera-{ms}/", f"Glosario: códigos y términos del filtro {marca}", f"Qué significa cada código y término del filtro de agua {marca}: " + ", ".join(p["ref"] for p in ps[:5]) + ", luz del filtro, purga y retracto.",
           f"Glosario del filtro de agua para nevecón {marca}", "Glosario", "Qué significa cada código y cada término que verás al comprar o cambiar el filtro.",
           '<dl class="m-ficha">' + "".join(f"<dt>{esc(a)}</dt><dd>{esc(b)}</dd>" for a, b in terminos) + "</dl>", [(a, b) for a, b in terminos[:6]], miga_nombre="Glosario")

    # ---------- mapa del sitio ----------
    bloque = lambda t, items: f'<h2 style="font-size:22px;margin:22px 0 10px">{esc(t)}</h2><ul class="m-ok">' + "".join(f'<li><a href="{u}">{esc(n)}</a></li>' for n, u in items) + "</ul>"
    cuerpo = (bloque("Filtros", [(f'{p["nombre_largo"]} · {cop(p["precio"])}', f'{base}{p["slug_o"]}/') for p in ps]) + bloque("Guías", [(t, r) for r, t in R["temas"]])
              + bloque("Regiones", [(ads22_hubs.REGIONES[k][0], r) for k, r in regiones.items()]) + bloque("Departamentos", [(f"Filtros {marca} en {d}", f"{base}filtros-{ms}-{slug(d)}/") for d in sorted(por_depto)])
              + bloque("Ciudades", [("Todas las ciudades por departamento", R["hub"]), ("Ciudades de la A a la Z", f"{base}ciudades-con-filtros-{ms}-a-z/")])
              + bloque("Ayuda", [("Glosario", f"{base}glosario-filtro-nevera-{ms}/"), ("Cómo cambiar e instalar", f"{base}cambio-e-instalacion/"), ("¿Cuál es mi filtro?", f"{base}cual-es-mi-filtro/")]))
    pagina(f"{base}mapa-del-sitio/", f"Mapa del sitio | Filtros {marca}", f"Todas las páginas de la tienda de filtros de agua {marca}: filtros, guías, regiones, departamentos, ciudades, códigos y modelos.", f"Mapa del sitio: filtros {marca}",
           "Mapa del sitio", "Todas las páginas de la tienda en un solo lugar.", cuerpo, [], miga_nombre="Mapa del sitio")
    return regiones
