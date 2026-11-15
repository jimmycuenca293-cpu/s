# Más autoridad temática: guías de intención de búsqueda, líneas de nevera y bloque ampliado para cada ficha de filtro.
_g2 = []


def _g(sl, titulo, desc, resumen, cuerpo, preg):
    _g2.append((sl, titulo, desc, resumen, cuerpo, preg))


_pasos = lambda l: "<ol>" + "".join(f"<li>{x}</li>" for x in l) + "</ol>"
_P1, _P2, _PX = PS[0], PS[1], PS[-1]

_g("como-quitar-el-filtro-de-agua-de-la-nevera-lg-atascado",
   "Cómo quitar el filtro de agua de la nevera LG cuando está atascado",
   "El filtro viejo de tu nevera LG no sale: cómo girarlo, qué hacer si está duro y cuándo no forzarlo para no dañar el alojamiento.",
   "Para sacar un filtro LG atascado, cierra el agua, gíralo despacio hacia la izquierda (sentido contrario a las agujas del reloj) y tira recto. Si está duro, humedece el contorno con agua tibia y espera unos minutos; no uses herramientas metálicas ni lo fuerces.",
   _h("Antes de empezar", "Cierra la llave de paso del agua y ten a mano un trapo: al retirarlo puede salir un poco de agua.")
   + _h("Paso a paso") + _pasos(["Identifica si el filtro es interno o externo.", "Gíralo suavemente a la izquierda hasta que suelte las guías.", "Jala recto, sin torcer, para no dañar el sello del alojamiento.",
                                 "Si está duro, aplica agua tibia alrededor y espera 5 minutos; repite el giro.", "Instala el nuevo y purga unos 6 litros de agua."])
   + _h("Lo que no debes hacer", "No uses pinzas, alicates ni palancas: pueden romper el alojamiento. Si después de varios intentos no sale, llama a un técnico autorizado.") + _CTA(_P2),
   [("¿Para qué lado se gira el filtro LG?", "Normalmente hacia la izquierda para soltarlo; confirma en el manual de tu modelo."), ("¿Puedo usar herramientas?", "No; pueden dañar el alojamiento."), ("¿Qué hago si no sale?", "Aplica agua tibia, espera y vuelve a intentar; si no cede, llama a un técnico.")])

_g("error-filtro-nevera-lg-replace-filter",
   "Mensaje «Replace Filter» o «Cambiar filtro» en la nevera LG: qué significa",
   "Qué significa el aviso «Replace Filter» o «Cambiar filtro» en el panel de tu nevera LG, cuándo aparece y cómo quitarlo.",
   "«Replace Filter» o «Cambiar filtro» es el aviso de que se cumplió el ciclo de uso del filtro de agua (alrededor de 6 meses). No es una falla del equipo: cambia el filtro y reinicia el aviso manteniendo presionado el botón del filtro unos segundos.",
   _h("Por qué aparece", "El panel cuenta el tiempo de uso del filtro; al cumplirse, enciende el indicador sin medir el estado real del cartucho.")
   + _h("Qué hacer") + _pasos(["Compra la referencia correcta de tu modelo (mira el código del filtro viejo).", "Cámbialo y purga unos 6 litros.", "Reinicia el aviso con el botón «Filtro» (3 a 5 segundos)."])
   + _h("Si el aviso no se va", "Revisa la guía <a href=\"luz-del-filtro-de-la-nevera-lg-no-se-apaga.html\">luz del filtro que no se apaga</a>.") + _CTA(_P1),
   [("¿«Replace Filter» es una falla?", "No, es el aviso de cambio programado."), ("¿Cuándo aparece?", "Cuando se cumple el ciclo de uso, de unos 6 meses."), ("¿Cómo lo quito?", "Cambiando el filtro y reiniciando el aviso desde el panel.")])

_g("como-saber-si-el-filtro-de-la-nevera-lg-esta-vencido",
   "Cómo saber si el filtro de la nevera LG está vencido",
   "Señales de que el filtro de agua de tu nevera LG ya venció: aviso del panel, sabor, olor, hielo y caudal.",
   "El filtro de una nevera LG está vencido si pasaron unos 6 meses desde el cambio o si notas sabor u olor raro en el agua, hielo turbio o menos caudal en el dispensador. El aviso del panel se enciende por tiempo, no por estado.",
   _h("Señales claras") + _ul(["Pasaron 6 meses o más desde la instalación.", "El agua sabe o huele diferente.", "El hielo sale turbio o con sedimentos.", "El dispensador entrega menos agua.", "El panel muestra «Replace Filter»."])
   + _h("Cómo llevar el control", "Anota la fecha del cambio en el mismo filtro o en tu calendario. Si vives en una zona con agua con muchos sedimentos, cámbialo antes.") + _CTA(_P2),
   [("¿Cuánto dura el filtro LG?", "Unos 6 meses de uso normal."), ("¿El panel avisa siempre?", "Avisa por tiempo, no por el estado real; si hay síntomas, cámbialo antes."), ("¿Qué pasa si no lo cambio?", "El agua y el hielo pierden calidad y el caudal baja.")])

_g("agua-con-sabor-raro-despues-de-cambiar-el-filtro-lg",
   "Agua con sabor raro o burbujas después de cambiar el filtro de la nevera LG",
   "Por qué el agua sale con burbujas, turbia o con sabor raro justo después de instalar un filtro nuevo en la nevera LG y cómo solucionarlo.",
   "Es normal que el agua salga con burbujas o ligeramente turbia las primeras veces tras instalar un filtro nuevo: es aire atrapado. Purga unos 6 litros por el dispensador y desecha el primer hielo. Si el sabor raro continúa, revisa que el filtro sea la referencia correcta.",
   _h("Qué pasa al instalarlo", "El filtro nuevo trae aire en su interior y partículas finas del carbón activado; al principio salen con el agua.")
   + _h("Cómo solucionarlo") + _pasos(["Saca unos 6 litros de agua por el dispensador, en tandas.", "Vacía el depósito de hielo y deja que se forme hielo nuevo.", "Espera 24 horas antes de juzgar el sabor final."])
   + _h("Si persiste", "Confirma que instalaste la referencia de tu modelo y que quitaste las tapas protectoras. Si el sabor sigue, revisa el agua de entrada.") + _CTA(_P2),
   [("¿Es normal que salgan burbujas?", "Sí, es aire del filtro nuevo; desaparece al purgar."), ("¿Cuánta agua debo sacar?", "Unos 6 litros."), ("¿Cuánto tarda en normalizarse el hielo?", "Alrededor de 24 horas.")])

_g("como-guardar-un-filtro-de-repuesto-para-la-nevera-lg",
   "Cómo guardar un filtro de repuesto de la nevera LG sin que se dañe",
   "Dónde y cómo almacenar el filtro de agua de repuesto de tu nevera LG para que esté en buen estado cuando toque instalarlo.",
   "Guarda el filtro de repuesto en su empaque sellado, en un lugar fresco, seco y lejos de la luz directa del sol y de químicos. Ábrelo solo en el momento de instalarlo.",
   _h("Recomendaciones") + _ul(["Mantén el empaque sellado hasta usarlo.", "Almacénalo en un lugar fresco y seco, sin sol directo.", "Aléjalo de productos químicos de limpieza.", "No lo guardes en el congelador.", "Anota la fecha de compra y de cambio."])
   + _h("Cuándo comprarlo", "Pide el repuesto cuando faltan unas semanas para el cambio: así evitas pasar días con el agua sin filtrar. Con envío gratis a toda Colombia llega en 1 a 7 días hábiles.") + _CTA(_P1),
   [("¿Puedo guardar el filtro en la nevera?", "No es necesario; guárdalo sellado en un sitio fresco y seco."), ("¿Se vence el repuesto sellado?", "Mientras esté sellado y bien almacenado se mantiene en buen estado hasta su uso."), ("¿Cuándo pedir el repuesto?", "Unas semanas antes del cambio.")])

_g("nevera-lg-hace-ruido-al-sacar-agua-filtro",
   "La nevera LG hace ruido o vibra al sacar agua: ¿es el filtro?",
   "Ruido, golpeteo o vibración al usar el dispensador de la nevera LG: causas comunes, aire en el sistema y cuándo revisar el filtro.",
   "El ruido o el golpeteo al sacar agua suele deberse a aire atrapado, sobre todo después de cambiar el filtro. Purga unos 6 litros; si el ruido sigue con el filtro bien asentado, revisa la manguera y la presión del agua.",
   _h("Causas comunes") + _ul(["Aire en el sistema tras un cambio de filtro.", "Filtro mal asentado o sin las tapas retiradas.", "Presión de agua baja o llave a medio abrir.", "Manguera doblada."])
   + _h("Qué hacer", "Purga el sistema, reinstala el filtro hasta que quede firme y revisa la manguera. Si el ruido es del compresor y no del dispensador, es otro tema: llama a un técnico.") + _CTA(_P2),
   [("¿Por qué suena al sacar agua?", "Casi siempre por aire atrapado; purga unos 6 litros."), ("¿El filtro puede causar vibración?", "Si está mal asentado, sí."), ("¿Cuándo llamar a un técnico?", "Si persiste con filtro correcto, bien instalado y agua suficiente.")])


def _linea(sl, nombre, desc_linea):
    _g(sl, f"Filtro de agua para nevera LG {nombre}: cuál es y dónde comprarlo",
       f"Qué filtro de agua usa una nevera LG {nombre}, cómo identificar el código y dónde comprarlo con envío a toda Colombia.",
       f"Las neveras LG {nombre} usan distintos filtros según el modelo exacto; no hay uno solo para toda la línea. Busca el código impreso en el filtro viejo o el modelo del equipo y compara con la tabla: los filtros LG que vendemos cuestan {RANGO} con envío gratis.",
       _h("Qué filtro usa", f"{desc_linea} La referencia depende del modelo y del año; por eso lo seguro es mirar el código del filtro viejo o la etiqueta del modelo (LF, LM, LR, LS o GR).")
       + _h("Referencias que manejamos") + _ul([f"<a href=\"{p['url']}\">{esc(p['nombre'])}</a> · {cop(p['precio'])}" for p in PS])
       + _h("Cómo confirmarlo", "Usa la <a href=\"cual-es-mi-filtro.html\">tabla de modelos y códigos</a> o escribe tu modelo en el buscador de la tienda.") + _CTA(_P2),
       [(f"¿Qué filtro usa la nevera LG {nombre}?", "Depende del modelo exacto; confirma con el código del filtro viejo."), ("¿Dónde veo el modelo?", "En la etiqueta dentro del refrigerador."), ("¿Hay envío gratis?", "Sí, a toda Colombia.")])


_linea("filtro-de-agua-nevera-lg-french-door", "French door", "En las neveras de dos puertas arriba y cajón de congelador abajo, el filtro suele estar dentro del refrigerador.")
_linea("filtro-de-agua-nevera-lg-side-by-side", "side by side", "En las neveras de refrigerador y congelador lado a lado, el filtro puede ir dentro del refrigerador o en la línea de agua.")
_linea("filtro-de-agua-nevera-lg-instaview", "InstaView", "En las neveras con ventana InstaView, el filtro depende del modelo y se instala igual que en el resto de neveras LG.")
ARTS += _g2


def extra_producto(p):
    """Bloque largo y propio de cada filtro: identificación, compatibilidad, mantenimiento y preguntas."""
    eq = ", ".join(p["refs"][1:]) or p["ref"]
    ext = p["ubic"] == "externo"
    mod = ", ".join(p["modelos"])
    s1 = _h(f"Cómo saber si necesitas el {p['corto']}", f"Mira el código impreso en el filtro que tienes: si dice {esc(p['ref'])} o alguno de sus equivalentes ({esc(eq)}), es este. "
            + (f"También lo usan los nevecones {esc(mod)}. " if mod else "") + "Si no puedes leer el código, escribe el modelo de tu nevera en el buscador o escríbenos por WhatsApp con una foto.")
    s2 = _h("Cuándo cambiarlo", "Cada 6 meses de uso normal. Cámbialo antes si el agua cambia de sabor u olor, el hielo sale turbio o el dispensador entrega menos agua. Después de cada cambio purga unos 6 litros y reinicia el aviso del panel.")
    s3 = _h("Cómo se instala", ("Es un filtro externo: se conecta a la manguera del agua. Cierra la llave de paso, retira el filtro viejo, conecta el nuevo en el sentido del flujo (flecha) y revisa que no gotee." if ext
                                else "Es un filtro interno: se instala dentro del refrigerador. Retira el viejo con un giro suave, instala el nuevo hasta que quede firme y purga el sistema.")
            + ' Paso a paso: <a href="cambio-e-instalacion.html">cómo cambiar el filtro</a>.')
    s4 = _h("Compra con garantía de cambio", f"Despachamos con envío gratis a toda Colombia, confirmamos que sea el filtro de tu nevecón antes de enviarlo y tienes 5 días hábiles de retracto con el filtro sin usar. Precio: {cop2(p['precio'])}.")
    preg = [(f"¿El {p['ref']} es igual al {p['refs'][1] if len(p['refs']) > 1 else p['ref']}?", f"Sí, son códigos de la misma pieza: {eq}."), (f"¿Puedo usar el {p['ref']} en otro modelo de nevera LG?", "No es recomendable: cada referencia corresponde a modelos específicos. Confirma con el código de tu filtro viejo."),
            (f"¿Qué pasa si no cambio el {p['ref']}?", "El filtro pierde capacidad: el agua y el hielo pueden cambiar de sabor y el caudal baja."), (f"¿Dónde comprar el {p['ref']} con envío gratis?", f"Aquí, con pago en línea o contra entrega: {cop2(p['precio'])}."),
            (f"¿Cómo sé si mi filtro es el {p['ref']}?", "Por el código impreso en el cuerpo del filtro o por el modelo de tu nevera.")]
    return seccion("Todo sobre el filtro " + esc(p["corto"]), s1 + s2 + s3 + s4), preg
