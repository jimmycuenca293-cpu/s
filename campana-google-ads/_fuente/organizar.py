"""Arma la carpeta campana-google-ads/ ordenada para revisar e importar la campaña.
Se corre desde esta carpeta: python3 organizar.py"""
import csv, pathlib, shutil, runpy
g = runpy.run_path("generar.py")  # valida largos y deja anuncios.csv / palabras-clave.csv
D, CAMP, GRUPOS, NEG = g["D"], g["CAMP"], g["GRUPOS"], g["NEGATIVAS"]
OUT = pathlib.Path(__file__).resolve().parent.parent  # la carpeta campana-google-ads
for c in ("02-grupos-de-anuncios", "05-archivos-para-importar"): (OUT / c).mkdir(parents=True, exist_ok=True)
w = lambda ruta, txt: (OUT / ruta).write_text(txt.strip() + "\n", encoding="utf-8")

w("00-LEEME.md", f"""# Campaña de Google Ads — PuroFiltro
**Sitio:** {D}  ·  **Campaña:** {CAMP}

Revisa los archivos en este orden:

| # | Archivo | Qué tiene |
|---|---|---|
| 1 | `01-configuracion.md` | Tipo de campaña, ubicación, presupuesto, puja y horario |
| 2 | `02-grupos-de-anuncios/` | Un archivo por grupo: títulos, descripciones, palabras clave y página de destino |
| 3 | `03-palabras-negativas.md` | Búsquedas por las que NO quieres pagar |
| 4 | `04-recursos-extensiones.md` | Enlaces a sitios, textos destacados, marcas, llamada y precios |
| 5 | `05-archivos-para-importar/` | `anuncios.csv` y `palabras-clave.csv` para Google Ads Editor |
| 6 | `06-conversiones-tag-manager.md` | Cómo medir las ventas (pago_wompi) y los clics a WhatsApp |
| 7 | `07-como-subirla.md` | Paso a paso para publicar la campaña |

**Resumen:** {len(GRUPOS)} grupos de anuncios · {len(GRUPOS)} anuncios con 15 títulos y 4 descripciones cada uno · {sum(len(x['kw']) for x in GRUPOS)} palabras clave (en frase y exacta: {sum(len(x['kw']) for x in GRUPOS)*2}) · {len(NEG)} negativas.

Todos los títulos tienen máximo 30 caracteres y las descripciones máximo 90 (el número entre paréntesis es el largo).
""")

w("01-configuracion.md", """# 1. Configuración de la campaña

| Opción | Qué poner |
|---|---|
| Tipo | **Búsqueda** (Search). Quita la Red de Display y los socios de búsqueda. |
| Objetivo | Ventas. Conversión principal: **pago_wompi**. Secundaria: **whatsapp**. |
| Ubicación | **Colombia**, con "Presencia: personas que están o suelen estar en las ubicaciones". El grupo «Cali instalación» se limita a Cali (radio 20 km). |
| Idioma | Español |
| Presupuesto | Empieza con **$25.000 a $35.000 al día** (unos $750.000 a $1.050.000 al mes). Súbelo cuando veas ventas. |
| Puja | Semanas 1 a 4: **Maximizar clics** con límite de CPC de $1.500. Con 15 o más conversiones pago_wompi: **Maximizar conversiones** y luego **CPA objetivo** de $25.000. |
| Horario | Todos los días, de 6:00 a. m. a 11:00 p. m. |
| Concordancia | Frase y exacta (ya vienen en el archivo). No uses concordancia amplia al comienzo. |
""")

for i, x in enumerate(GRUPOS, 1):
    nombre = x["nombre"].lower().replace(" ", "-").replace("é", "e").replace("ó", "o")
    t = "\n".join(f"{j}. {h} ({len(h)})" for j, h in enumerate(x["T"], 1))
    d = "\n".join(f"{j}. {h} ({len(h)})" for j, h in enumerate(x["D"], 1))
    kw = "\n".join(f"| {k} | \"{k}\" | [{k}] |" for k in x["kw"])
    w(f"02-grupos-de-anuncios/{i:02d}-{nombre}.md", f"""# Grupo {i}: {x['nombre']}

**Página de destino:** {D}{x['url']}
**Ruta visible:** filtrosdeaguanevecon.com/{x['p1']}/{x['p2']}{chr(10) + '**Ubicación:** ' + x['geo'] if x.get('geo') else ''}

## Títulos (máx. 30 caracteres)
{t}

## Descripciones (máx. 90 caracteres)
{d}

## Palabras clave ({len(x['kw'])})
| Palabra | Frase | Exacta |
|---|---|---|
{kw}
""")

w("03-palabras-negativas.md", "# 3. Palabras clave negativas (toda la campaña)\n\nSe agregan como \"concordancia de frase\" a nivel de campaña.\n\n" + "\n".join(f"- {n}" for n in NEG) +
  "\n\nRevisa cada semana el informe **Términos de búsqueda** y agrega como negativas las búsquedas que no tienen que ver con filtros de nevecón.")

w("04-recursos-extensiones.md", f"""# 4. Recursos (extensiones)

## Enlaces a sitios
| Texto | Página | Línea 1 | Línea 2 |
|---|---|---|---|
| Cómo instalar tu filtro | {D}/purofiltro-instalacion/ | Paso a paso por referencia | En minutos y sin herramientas |
| ¿Cuándo cambiar el filtro? | {D}/purofiltro-guia/cada-cuanto-cambiar-el-filtro-del-nevecon/ | Las señales de que ya toca | Cada 6 meses o antes |
| Busca por referencia | {D}/purofiltro-referencias/ | Todas las equivalencias | Encuentra el tuyo fácil |
| Envíos a toda Colombia | {D}/purofiltro-envios/ | Tiempo de entrega a tu ciudad | Envío gratis |
| Instalación en Cali | {D}/purofiltro-cali/ | Gratis en filtros internos | Agendamos día y hora |
| Ver la tienda | {D}/purofiltro-tienda/ | Todos los filtros y precios | Samsung, LG, Whirlpool, GE |

## Textos destacados
Envío gratis · Pago seguro en línea · PSE, Nequi y tarjeta · Asesoría por WhatsApp · Llega en 2 a 3 días · Pack anual con descuento · Tutorial de instalación · Técnicos de neveras

## Fragmentos estructurados
Marcas: Samsung, LG, Whirlpool, GE, Maytag, KitchenAid

## Llamada
321 799 6144 (solo en horario de atención)

## Precios (cada uno a su página de producto)
| Producto | Precio | Página |
|---|---|---|
| Filtro Samsung HAF-CIN | $115.900 | {D}/purofiltro-filtro/filtro-samsung-haf-cin-da29-00020b/ |
| Filtro LG LT1000P | $112.900 | {D}/purofiltro-filtro/filtro-lg-lt1000p/ |
| Whirlpool EveryDrop 1 | $145.900 | {D}/purofiltro-filtro/filtro-whirlpool-everydrop-1-edr1rxd1/ |
| Filtro GE MWF | $158.900 | {D}/purofiltro-filtro/filtro-ge-mwf/ |
| Filtros externos | desde $81.900 | {D}/purofiltro-tienda/ |
""")

w("06-conversiones-tag-manager.md", """# 6. Conversiones en Google Tag Manager (GTM-N39G66VJ)

La tienda ya manda estos eventos:

| Evento | Cuándo | Datos |
|---|---|---|
| `whatsapp` | El cliente toca el botón de WhatsApp | ubicacion, pagina |
| `pago_wompi` | El cliente toca "Pagar" y va a la página de pago | value (total), currency (COP), transaction_id (pedido) |

1. En Google Ads crea 2 conversiones (Objetivos → Conversiones → Nueva → Sitio web → manual): **Compra (pago_wompi)** como principal y **Contacto WhatsApp** como secundaria. Copia el ID y la etiqueta de cada una.
2. En Tag Manager → **Activadores → Nuevo → Evento personalizado**: uno con nombre `pago_wompi` y otro con `whatsapp`.
3. **Etiquetas → Nueva → Seguimiento de conversiones de Google Ads** para cada una, con su activador. En la de pago_wompi: valor = variable de capa de datos `value`, moneda `COP`, ID de transacción = `transaction_id`.
4. Agrega la etiqueta **Vinculador de conversiones** con el activador "All Pages".
5. Prueba con **Vista previa** de Tag Manager y luego **Enviar → Publicar**.
""")

w("07-como-subirla.md", f"""# 7. Cómo subir la campaña

1. Verifica que la tienda ya esté en línea en {D} y que las conversiones del archivo 06 estén publicadas.
2. Instala **Google Ads Editor** (gratis) y descarga tu cuenta.
3. Crea la campaña **{CAMP}** con la configuración del archivo 01.
4. **Cuenta → Importar → Desde archivo**: primero `05-archivos-para-importar/palabras-clave.csv` y luego `05-archivos-para-importar/anuncios.csv`.
5. Agrega los recursos del archivo 04.
6. Revisa que no haya errores y dale **Publicar**.

## Ojo con las marcas
Samsung, LG, Whirlpool y GE son marcas registradas. Google deja que los revendedores las usen cuando la página vende ese producto, pero a veces el anuncio queda "Aprobado (limitado)". Si alguno sale rechazado por marca, pide revisión o cambia el título por la referencia (por ejemplo "Filtro LT1000P"). No uses «original» ni «genuino».
""")

shutil.copy("anuncios.csv", OUT / "05-archivos-para-importar" / "anuncios.csv")
shutil.copy("palabras-clave.csv", OUT / "05-archivos-para-importar" / "palabras-clave.csv")
print("listo")
